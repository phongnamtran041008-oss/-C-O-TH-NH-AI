"""The master palette (art/palette.json): loading, OKLab matching, ramp lookups, palette swaps.

Pure Python at import time; numpy is used when present (inside Blender) and never required
(the game's venv has no numpy), so qc.py and contact.py can import this too.

A palette is a set of named *ramps*. Solid ramps have 5 entries
[outline, shadow, base, light, highlight]; glow ramps have 4 entries
[halo far, halo near, glow edge, glow core].
"""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

from .paths import ROOT

PALETTE_PATH = ROOT / "art" / "palette.json"


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    """sRGB 0..255 -> OKLab (L 0..1)."""
    r, g, b = (_lin(v / 255.0) for v in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


class Palette:
    """All colours of art/palette.json, flattened, with their (ramp, index) address."""

    def __init__(self, doc: dict):
        self.doc = doc
        self.ink = hex_rgb(doc.get("ink", "#0b0a10"))
        self.ramps: dict[str, list[int]] = {}      # ramp name -> global colour indices
        self.kind: dict[str, str] = {}
        self.colors: list[tuple[int, int, int]] = []
        self.where: list[tuple[str, int]] = []     # global index -> (ramp, position)
        for name, r in doc["ramps"].items():
            self.kind[name] = r.get("kind", "solid")
            ids = []
            for i, h in enumerate(r["colors"]):
                ids.append(len(self.colors))
                self.colors.append(hex_rgb(h))
                self.where.append((name, i))
            self.ramps[name] = ids
        self.ink_index = len(self.colors)
        self.colors.append(self.ink)
        self.where.append(("ink", 0))
        self.lab = [oklab(c) for c in self.colors]
        self.color_set = set(self.colors)

    # ---- lookups
    def solid_ramps(self) -> list[str]:
        return [n for n, k in self.kind.items() if k == "solid"]

    def glow_ramps(self) -> list[str]:
        return [n for n, k in self.kind.items() if k == "glow"]

    def at(self, ramp: str, pos: int) -> int:
        """Global index of ramp[pos], clamped to the ramp."""
        ids = self.ramps[ramp]
        return ids[max(0, min(len(ids) - 1, pos))]

    def nearest(self, rgb, candidates: list[int] | None = None) -> int:
        """Global index of the palette colour nearest to rgb (0..255) in OKLab."""
        lab = oklab(tuple(int(v) for v in rgb[:3]))
        best, bi = 1e9, 0
        for i in (candidates if candidates is not None else range(len(self.colors))):
            q = self.lab[i]
            d = (lab[0] - q[0]) ** 2 + (lab[1] - q[1]) ** 2 + (lab[2] - q[2]) ** 2
            if d < best:
                best, bi = d, i
        return bi

    def base_candidates(self, ramps: list[str] | None = None) -> list[int]:
        """Entries a material's base colour may snap to: 1..3 of each solid ramp."""
        out = []
        for n in (ramps or self.solid_ramps()):
            if self.kind.get(n) == "solid":
                out += self.ramps[n][1:4]
            elif n in self.ramps:
                out += self.ramps[n]
        return out

    def glow_ramp_for(self, rgb) -> str:
        """Which glow ramp an emission colour belongs to (by its edge colour)."""
        names = self.glow_ramps()
        i = self.nearest(rgb, [self.at(n, 2) for n in names] + [self.at(n, 1) for n in names])
        return self.where[i][0]


@lru_cache(maxsize=4)
def _load(path: str, mtime: float) -> Palette:
    return Palette(json.loads(Path(path).read_text("utf-8")))


def load(path: Path | None = None) -> Palette:
    p = Path(path or PALETTE_PATH)
    return _load(str(p), p.stat().st_mtime)


# ---------------------------------------------------------------- palette swap
def swap_map(mapping: dict[str, str], pal: Palette | None = None) -> dict[tuple, tuple]:
    """{(r,g,b): (r,g,b)} that moves every colour of ramp A to the same position of ramp B,
    e.g. {"red": "purple"} turns a red-robed monster into a purple variant."""
    pal = pal or load()
    out = {}
    for a, b in mapping.items():
        for pos, gi in enumerate(pal.ramps[a]):
            out[pal.colors[gi]] = pal.colors[pal.at(b, pos)]
    return out


def swap_rgba_bytes(data: bytearray, cmap: dict[tuple, tuple]) -> bytearray:
    """Apply a swap_map to raw RGBA bytes (pure Python, works in the venv)."""
    out = bytearray(data)
    for i in range(0, len(out), 4):
        if out[i + 3]:
            c = (out[i], out[i + 1], out[i + 2])
            n = cmap.get(c)
            if n:
                out[i], out[i + 1], out[i + 2] = n
    return out


def swap_png(src: Path, dst: Path, mapping: dict[str, str]) -> None:
    """Write a recoloured copy of a packed PNG (the JSON next to it can be copied as is,
    with its id changed). Pure Python."""
    from . import png
    w, h, px = png.read(src)
    png.write(dst, w, h, swap_rgba_bytes(px, swap_map(mapping)))
