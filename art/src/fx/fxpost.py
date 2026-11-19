"""Render result -> pixel art -> FX sheet.  Runs inside Blender's Python (numpy available).

Steps per frame (all on the 6x render):
  1. area-average down to the target size (this is the 6x -> 1x scale-down of the contract)
  2. additive sheets: a 1-2 px halo (blur added back), then quantise: hue snapped to the FX
     palette, intensity to `levels` steps  -> crisp, saturated, posterised glow
     alpha sheets: straight colour snapped to the palette, alpha to `alpha_levels` steps
  3. pack frames into one sheet + JSON (the format of ART_PIPELINE section 4)
Additive sheets store PREMULTIPLIED colour (rgb already scaled by alpha), so they can be drawn
with BLEND_ADD (alpha ignored) or with normal alpha blending.
"""
import json
import os
import struct
import zlib
import colorsys
import numpy as np
import bpy

R = 6


def write_png(path, arr):
    arr = np.ascontiguousarray(arr.astype(np.uint8))
    h, w, _ = arr.shape
    raw = b"".join(b"\x00" + arr[y].tobytes() for y in range(h))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def read_png(path):
    """-> float32 HxWx4 (top row first), raw values, no colour management."""
    img = bpy.data.images.load(path, check_existing=False)
    img.colorspace_settings.name = "Non-Color"
    img.alpha_mode = "CHANNEL_PACKED"
    w, h = img.size
    buf = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(buf)
    bpy.data.images.remove(img)
    return buf.reshape(h, w, 4)[::-1].copy()


# ---------------------------------------------------------------- palette (art/palette.json)
def _oklab(rgb):
    """rgb float 0..1 (N,3) -> OKLab (N,3)."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    l = 0.4122214708 * c[:, 0] + 0.5363325363 * c[:, 1] + 0.0514459929 * c[:, 2]
    m = 0.2119034982 * c[:, 0] + 0.6806995451 * c[:, 1] + 0.1073969566 * c[:, 2]
    s = 0.0883024619 * c[:, 0] + 0.2817188376 * c[:, 1] + 0.6299787005 * c[:, 2]
    l, m, s = np.cbrt(l), np.cbrt(m), np.cbrt(s)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], 1)


def _load_palette():
    here = os.path.dirname(os.path.abspath(__file__))
    doc = json.load(open(os.path.join(here, "..", "..", "palette.json"), encoding="utf-8"))
    cols = [doc.get("ink", "#0b0a10")]
    for r in doc["ramps"].values():
        cols += r["colors"]
    arr = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in cols], np.float32) / 255.0
    return arr


PAL = _load_palette()                       # index 0 = ink
PAL_LAB = _oklab(PAL)
BLACK_LAB = _oklab(np.zeros((1, 3), np.float32))


def snap_palette(rgb, with_black=False):
    """nearest master-palette colour (OKLab).  with_black: also allow 'nothing' -> returns mask."""
    flat = rgb.reshape(-1, 3)
    lab = _oklab(np.clip(flat, 0, 1))
    d = ((lab[:, None, :] - PAL_LAB[None, :, :]) ** 2).sum(-1)
    idx = d.argmin(1)
    best = d[np.arange(len(idx)), idx]
    out = PAL[idx].reshape(rgb.shape)
    if with_black:
        db = ((lab - BLACK_LAB) ** 2).sum(-1)
        nothing = db < best * 0.8
        return out, nothing.reshape(rgb.shape[:-1])
    return out


def blur(a, sigma):
    """cheap separable gaussian on HxWxC."""
    rad = max(1, int(sigma * 3))
    k = np.exp(-0.5 * (np.arange(-rad, rad + 1) / sigma) ** 2)
    k /= k.sum()
    p = np.pad(a, ((rad, rad), (rad, rad), (0, 0)), mode="constant")
    t = sum(k[i] * p[i:i + a.shape[0] + 0, :, :] for i in range(len(k)))[:, :, :]
    t = t[: a.shape[0] + 2 * rad - 2 * rad + 0]
    # horizontal
    out = sum(k[i] * t[:, i:i + a.shape[1], :] for i in range(len(k)))
    return out


def process(frame6, mode, px, halo, levels, alpha_levels, gamma=1.0):
    h = frame6.shape[0] // R
    if mode == "add":
        # the render is the light the effect ADDS to the screen: its colours are snapped straight to
        # the master palette (the glow ramps are the 4 intensity steps) and black becomes alpha 0.
        # Draw these sheets with BLEND_ADD.
        rgb = np.clip(frame6[..., :3], 0, 1)
        f = rgb.reshape(h, R, h, R, 3).mean((1, 3))
        if halo > 0:
            f = np.maximum(f, halo * 1.25 * blur(f, 1.3))      # glow spills outwards, never brightens a filled area
            f = np.maximum(f, halo * 0.8 * blur(f, 2.6))
        f = np.clip(f, 0, 1) ** gamma
        col, nothing = snap_palette(f, True)
        nothing |= f.max(-1) < 0.09
        out = np.zeros((h, h, 4), np.float32)
        out[..., :3] = col
        out[..., 3] = 1.0
        out[nothing] = 0
        return (out * 255 + 0.5).astype(np.uint8)
    a6 = frame6[..., 3:4]
    rgb = frame6[..., :3] * a6
    A = a6.reshape(h, R, h, R, 1).mean((1, 3))
    C = rgb.reshape(h, R, h, R, 3).mean((1, 3)) / np.maximum(A, 1e-6)
    C = snap_palette(np.clip(C, 0, 1))
    A = np.clip(A[..., 0], 0, 1)
    Aq = np.round(A * alpha_levels) / alpha_levels
    out = np.zeros((h, h, 4), np.float32)
    out[..., :3] = C
    out[..., 3] = Aq
    out[Aq == 0] = 0
    return (out * 255 + 0.5).astype(np.uint8)


def pack(fx, frame_paths, outdir):
    frames = []
    for p in frame_paths:
        frames.append(process(read_png(p), fx.mode, fx.px, fx.halo, fx.levels, fx.alpha_levels, fx.gamma))
    n = len(frames)
    cols = n if n <= 8 else (5 if n % 5 == 0 else 6 if n % 6 == 0 else 8)
    rows = (n + cols - 1) // cols
    sheet = np.zeros((rows * fx.px, cols * fx.px, 4), np.uint8)
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols)
        sheet[r * fx.px:(r + 1) * fx.px, c * fx.px:(c + 1) * fx.px] = fr
    write_png(os.path.join(outdir, fx.id + ".png"), sheet)
    meta = {
        "id": fx.id, "name_vi": fx.name_vi,
        "frame": {"w": fx.px, "h": fx.px}, "pivot": {"x": fx.pivot[0], "y": fx.pivot[1]},
        "sheet": fx.id + ".png", "cols": cols, "frames": n, "fps": fx.fps, "loop": bool(fx.loop),
        "blend": fx.mode, "ground": bool(fx.ground),
    }
    if getattr(fx, "extra", None):
        meta.update(fx.extra)
    with open(os.path.join(outdir, fx.id + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return frames


# ---------------------------------------------------------------- contact sheets
GLYPHS = {
    "a": "010101111101101", "b": "110101110101110", "c": "011100100100011", "d": "110101101101110",
    "e": "111100110100111", "f": "111100110100100", "g": "011100101101011", "h": "101101111101101",
    "i": "111010010010111", "j": "001001001101010", "k": "101101110101101", "l": "100100100100111",
    "m": "101111111101101", "n": "110101101101101", "o": "010101101101010", "p": "110101110100100",
    "q": "010101101111011", "r": "110101110101101", "s": "011100010001110", "t": "111010010010010",
    "u": "101101101101111", "v": "101101101101010", "w": "101101111111101", "x": "101101010101101",
    "y": "101101010010010", "z": "111001010100111", "0": "111101101101111", "1": "010110010010111",
    "2": "110001010100111", "3": "110001010001110", "4": "101101111001001", "5": "111100110001110",
    "6": "011100111101111", "7": "111001010010010", "8": "111101111101111", "9": "111101111001110",
    "_": "000000000000111", "-": "000000111000000", " ": "000000000000000",
}


def draw_text(img, x, y, text, color=(200, 200, 215), scale=2):
    for ch in text.lower():
        g = GLYPHS.get(ch, GLYPHS[" "])
        for i, b in enumerate(g):
            if b == "1":
                r, c = divmod(i, 3)
                img[y + r * scale:y + (r + 1) * scale, x + c * scale:x + (c + 1) * scale, :3] = color
        x += 4 * scale


def load_sheet(outdir, id):
    meta = json.load(open(os.path.join(outdir, id + ".json"), encoding="utf-8"))
    arr = (read_png(os.path.join(outdir, id + ".png")) * 255 + 0.5).astype(np.uint8)
    return meta, arr


def contact(outdir, ids, path, width=2200, zoom=3, bg=(14, 14, 24), checker_ground=False):
    items = []
    for id in ids:
        try:
            meta, arr = load_sheet(outdir, id)
        except Exception:
            continue
        px, n, cols = meta["frame"]["w"], meta["frames"], meta["cols"]
        frames = []
        for i in range(n):
            r, c = divmod(i, cols)
            fr = arr[r * px:(r + 1) * px, c * px:(c + 1) * px].astype(np.float32) / 255
            base = np.zeros((px, px, 3), np.float32) + np.array(bg, np.float32) / 255
            if meta["blend"] == "add":
                comp = np.clip(base + fr[..., :3] * fr[..., 3:4], 0, 1)
            else:
                comp = base * (1 - fr[..., 3:4]) + fr[..., :3] * fr[..., 3:4]
            comp = (comp * 255 + 0.5).astype(np.uint8)
            frames.append(np.repeat(np.repeat(comp, zoom, 0), zoom, 1))
        items.append((id, px * zoom, frames))
    gap, lab = 10, 14
    width = max([width] + [s * len(fr) + 2 * gap for _, s, fr in items])
    x = y = gap
    rowh = 0
    placed = []
    for id, s, frames in items:
        w = s * len(frames)
        if x + w > width and x > gap:
            x = gap
            y += rowh + gap
            rowh = 0
        placed.append((x, y, id, s, frames))
        x += w + gap
        rowh = max(rowh, s + lab)
    H = y + rowh + gap
    img = np.zeros((H, width, 3), np.uint8) + np.array(bg, np.uint8)
    for x, y, id, s, frames in placed:
        draw_text(img, x, y, id, scale=2)
        for i, fr in enumerate(frames):
            img[y + lab:y + lab + s, x + i * s:x + (i + 1) * s] = fr
            img[y + lab:y + lab + s, x + i * s] = (40, 40, 60)
    rgba = np.concatenate([img, np.full((H, width, 1), 255, np.uint8)], 2)
    write_png(path, rgba)


# ---------------------------------------------------------------- warnings on real ground
def warn_on_ground(root, outdir, path):
    """art/preview/fx_warn_on_ground.png: warn_circle / cone / line (charge + release) at 1x, 2x, 3x
    stretch over grass, path, stone and water tiles of client/assets/v2/tiles/base.png."""
    tiles = (read_png(os.path.join(root, "client", "assets", "v2", "tiles", "base.png")) * 255 + 0.5).astype(np.uint8)
    cols = 8

    def tile(i):
        r, c = divmod(i, cols)
        return tiles[r * 16:(r + 1) * 16, c * 16:(c + 1) * 16, :3].astype(np.float32)

    grounds = [("grass", [0, 1, 2, 1, 0, 2]), ("path", [5, 6, 5, 6]), ("stone", [9, 9, 9, 9]), ("water", [21, 22, 7, 23])]
    kinds = [("warn_circle_charge", 1), ("warn_circle_release", 0), ("warn_cone_charge", 1), ("warn_cone_release", 0),
             ("warn_line_charge", 1), ("warn_line_release", 0)]
    sheets = {}
    for k, _ in kinds:
        meta, arr = load_sheet(outdir, k)
        sheets[k] = (meta, arr)

    def frame(k, idx, s):
        meta, arr = sheets[k]
        px, cols_ = meta["frame"]["w"], meta["cols"]
        r, c = divmod(idx, cols_)
        fr = arr[r * px:(r + 1) * px, c * px:(c + 1) * px].astype(np.float32) / 255
        return np.repeat(np.repeat(fr, s, 0), s, 1)

    blocks = []
    gap = 10
    for s in (1, 2, 3):
        cell = 96 * s
        W = len(kinds) * (cell + gap) + gap
        H = len(grounds) * (cell + gap) + gap + 16
        img = np.zeros((H, W, 3), np.float32) + 0.05
        for gi, (gname, idxs) in enumerate(grounds):
            y0 = 16 + gap + gi * (cell + gap)
            for ki, (k, fi) in enumerate(kinds):
                x0 = gap + ki * (cell + gap)
                bg = np.zeros((cell, cell, 3), np.float32)
                for ty in range(0, cell, 16):
                    for tx in range(0, cell, 16):
                        bg[ty:ty + 16, tx:tx + 16] = tile(idxs[((tx // 16) + (ty // 16) * 3) % len(idxs)])
                bg /= 255.0
                fr = frame(k, fi, s)
                a = fr[..., 3:4]
                comp = bg * (1 - a) + fr[..., :3] * a
                img[y0:y0 + cell, x0:x0 + cell] = comp
        out = (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)
        draw_text(out, gap, 2, "stretch %dx   grass / path / stone / water   circle charge release  cone charge release  line charge release" % s, scale=1 if s == 1 else 2)
        blocks.append(out)
    W = max(b.shape[1] for b in blocks)
    H = sum(b.shape[0] for b in blocks)
    canvas = np.zeros((H, W, 3), np.uint8) + 12
    y = 0
    for b in blocks:
        canvas[y:y + b.shape[0], :b.shape[1]] = b
        y += b.shape[0]
    write_png(path, np.concatenate([canvas, np.full((H, W, 1), 255, np.uint8)], 2))
