"""Minimal PNG read/write (8-bit RGBA / RGB / grey / palette, non-interlaced). Pure Python
(zlib + struct), so it runs in Blender and in the game's venv alike."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path


def _chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def write(path, w: int, h: int, rgba) -> None:
    """rgba: bytes-like of length w*h*4, rows top to bottom (or a numpy uint8 HxWx4)."""
    try:                                   # numpy array
        rgba = rgba.astype("uint8").tobytes()
    except AttributeError:
        rgba = bytes(rgba)
    stride = w * 4
    raw = b"".join(b"\x00" + rgba[y * stride:(y + 1) * stride] for y in range(h))
    data = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def read(path) -> tuple[int, int, bytearray]:
    """(w, h, RGBA bytes). Handles 8-bit colour types 0, 2, 3, 4, 6 and all filters."""
    b = Path(path).read_bytes()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos, idat, plte, trns = 8, b"", None, None
    w = h = ctype = depth = 0
    while pos < len(b):
        n, tag = struct.unpack(">I4s", b[pos:pos + 8])
        data = b[pos + 8:pos + 8 + n]
        pos += 12 + n
        if tag == b"IHDR":
            w, h, depth, ctype, _, _, inter = struct.unpack(">IIBBBBB", data)
            if depth != 8 or inter:
                raise ValueError(f"{path}: only 8-bit non-interlaced PNG is supported")
        elif tag == b"PLTE":
            plte = data
        elif tag == b"tRNS":
            trns = data
        elif tag == b"IDAT":
            idat += data
        elif tag == b"IEND":
            break
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(idat)
    stride = w * bpp
    out = bytearray(stride * h)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        f = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                c = prev[x - bpp] if x >= bpp else 0
                p = a + prev[x] - c
                pa, pb, pc = abs(p - a), abs(p - prev[x]), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (prev[x] if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    if ctype == 6:
        return w, h, out
    rgba = bytearray(w * h * 4)
    for p in range(w * h):
        if ctype == 2:
            rgba[p * 4:p * 4 + 3] = out[p * 3:p * 3 + 3]
            rgba[p * 4 + 3] = 255
        elif ctype == 0:
            rgba[p * 4:p * 4 + 3] = bytes((out[p],) * 3)
            rgba[p * 4 + 3] = 255
        elif ctype == 4:
            rgba[p * 4:p * 4 + 3] = bytes((out[p * 2],) * 3)
            rgba[p * 4 + 3] = out[p * 2 + 1]
        else:                                   # palette
            k = out[p]
            rgba[p * 4:p * 4 + 3] = plte[k * 3:k * 3 + 3]
            rgba[p * 4 + 3] = trns[k] if trns and k < len(trns) else 255
    return w, h, rgba
