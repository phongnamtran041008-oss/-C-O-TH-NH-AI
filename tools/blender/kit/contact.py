#!/usr/bin/env python3
"""Contact sheet of kit output: every frame at 3x nearest-neighbour on a dark background,
with small labels. Needs pygame (the game's venv has it).

    python tools/blender/kit/contact.py art/preview/my_batch.png client/assets/v2/chars [...]

Animated sheets: one row per clip x facing. FX: one row. Icons: the grid with ids.
Tiles: each tile, plus a 4x4 tiled preview of every tile name (seams show up there).
Props: each prop with its pivot marked.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame  # noqa: E402

ZOOM = 3
BG = (12, 11, 16)
PANEL = (22, 21, 28)
TEXT = (200, 196, 210)
DIM = (120, 116, 132)
PIVOT = (255, 60, 90)
PAD = 6
MAX_W = 2400


def _font(size=13):
    """A system font with Vietnamese letters (the pygame default font lacks them)."""
    pygame.font.init()
    for name in ("segoeui", "arial", "tahoma", "dejavusans", "notosans"):
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.Font(None, size + 4)


def _scaled(surf):
    return pygame.transform.scale(surf, (surf.get_width() * ZOOM, surf.get_height() * ZOOM))


class Canvas:
    """Rows of labelled strips, stacked; drawn at the end."""

    def __init__(self):
        self.items = []         # (kind, payload)

    def title(self, text):
        self.items.append(("title", text))

    def strip(self, label, surfs, marks=None, add=False):
        self.items.append(("strip", (label, surfs, marks or [None] * len(surfs), add)))

    def render(self) -> pygame.Surface:
        f, ft = _font(12), _font(15)
        label_w = 110
        rows, width, height = [], 0, PAD
        for kind, p in self.items:
            if kind == "title":
                rows.append((kind, p, height))
                height += 26
                continue
            label, surfs, marks, add = p
            # wrap long strips
            x = label_w
            line_h = 0
            pos = []
            y = height
            for s in surfs:
                w, h = s.get_width() * ZOOM, s.get_height() * ZOOM
                if x + w > MAX_W and x > label_w:
                    x, y = label_w, y + line_h + 2
                    line_h = 0
                pos.append((x, y))
                x += w + 2
                line_h = max(line_h, h)
                width = max(width, x)
            rows.append((kind, (label, surfs, marks, pos, add), height))
            height = y + line_h + 4
        img = pygame.Surface((max(width + PAD, 400), height + PAD), pygame.SRCALPHA)
        img.fill(BG + (255,))
        for kind, p, y in rows:
            if kind == "title":
                img.blit(ft.render(p, True, TEXT), (PAD, y + 4))
                continue
            label, surfs, marks, pos, add = p
            img.blit(f.render(label, True, DIM), (PAD, y + 4))
            for s, (x, yy), m in zip(surfs, pos, marks):
                z = _scaled(s)
                pygame.draw.rect(img, PANEL, (x, yy, z.get_width(), z.get_height()))
                if add:     # additive FX: what the game shows is rgb x alpha added on top
                    pm = z.convert_alpha().premul_alpha()
                    flat = pygame.Surface(pm.get_size())
                    flat.blit(pm, (0, 0))
                    img.blit(flat, (x, yy), special_flags=pygame.BLEND_RGB_ADD)
                else:
                    img.blit(z, (x, yy))
                if m is not None:
                    mx, my = x + m[0] * ZOOM, yy + m[1] * ZOOM
                    pygame.draw.line(img, PIVOT, (mx - 3, my), (mx + 3, my))
                    pygame.draw.line(img, PIVOT, (mx, my - 3), (mx, my + 3))
        return img


def _cell(sheet, i, cols, w, h):
    return sheet.subsurface(((i % cols) * w, (i // cols) * h, w, h))


def add_doc(cv: Canvas, path: Path):
    doc = json.loads(path.read_text("utf-8"))
    sheet = pygame.image.load(str(path.parent / doc["sheet"]))
    rel = path.stem
    if "clips" in doc:
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        pv = (doc["pivot"]["x"], doc["pivot"]["y"])
        cv.title(f"{doc.get('name_vi', rel)}  [{rel}]  {fw}x{fh}  {doc['frames']} frames")
        for clip, c in doc["clips"].items():
            for d, ids in c["frames"].items():
                ev = doc.get("events", {}).get(clip, {})
                tag = f"{clip}/{d}" + (" *" if ev else "")
                cv.strip(tag, [_cell(sheet, i, cols, fw, fh) for i in ids], [pv] * len(ids))
    elif "blend" in doc:
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        pv = (doc["pivot"]["x"], doc["pivot"]["y"])
        cv.title(f"FX {rel}  {fw}x{fh}  blend={doc['blend']} ground={doc['ground']}")
        cv.strip(rel, [_cell(sheet, i, cols, fw, fh) for i in range(doc["frames"])], [pv] * doc["frames"],
                 add=doc["blend"] == "add")
    elif "icons" in doc:
        c, cols = doc["cell"], doc["cols"]
        cv.title(f"icons {rel}")
        items = sorted(doc["icons"].items(), key=lambda kv: kv[1]["index"])
        cv.strip(" ".join(k for k, _ in items)[:40], [_cell(sheet, v["index"], cols, c, c) for _, v in items])
    elif "tiles" in doc:
        cols = doc["cols"]
        cv.title(f"tiles {rel}")
        for name, ids in doc["tiles"].items():
            tiles = [_cell(sheet, i, cols, 16, 16) for i in ids]
            big = pygame.Surface((64, 64), pygame.SRCALPHA)
            for y in range(4):
                for x in range(4):
                    big.blit(tiles[(x * 3 + y * 5 + (x * y)) % len(tiles)], (x * 16, y * 16))
            same = pygame.Surface((48, 48), pygame.SRCALPHA)
            for y in range(3):
                for x in range(3):
                    same.blit(tiles[0], (x * 16, y * 16))
            cv.strip(name, tiles + [same, big])
    elif "props" in doc:
        cv.title(f"props {rel}")
        surfs, marks = [], []
        for name, p in doc["props"].items():
            x, y, w, h = p["rect"]
            for k in range(p.get("frames", 1)):
                surfs.append(sheet.subsurface((x + k * w, y, w, h)))
                marks.append(tuple(p["pivot"]))
        cv.strip(" ".join(doc["props"])[:18], surfs, marks)


def write(folders, out: Path, title: str = "") -> Path:
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    cv = Canvas()
    if title:
        cv.title(f"{title}  (x{ZOOM})")
    for d in folders:
        d = Path(d)
        files = [d] if d.suffix == ".json" else sorted(d.rglob("*.json"))
        for f in files:
            try:
                add_doc(cv, f)
            except (KeyError, ValueError, pygame.error, FileNotFoundError) as e:
                cv.title(f"{f.name}: cannot show ({e})")
    img = cv.render()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    print(write(argv[1:], Path(argv[0]), title=Path(argv[0]).stem))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
