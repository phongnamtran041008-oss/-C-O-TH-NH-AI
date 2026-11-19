"""Draw weapon layers over character sheets (venv python, pygame): the proof that the layers
fit, and the contact sheets art/preview/weapon_layers*.png.

    python composite.py <weapon_id> <char_id> clip:dir[:frame] ... [--dir <weapon folder>] [--out x.png]

Library use: `Sheets` loads a sheet + json and hands out 64x64 frames; `compose()` draws a
frame of a weapon layer over the same frame of a character (what the game does).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
CHARS = ROOT / "client" / "assets" / "v2" / "chars"
WEAPONS = ROOT / "client" / "assets" / "v2" / "weapons"
REALMS = ["luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua"]
REALM_NAME = ["Luyện Khí", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần", "Luyện Hư", "Hợp Thể", "Đại Thừa"]

pygame.init()
pygame.display.set_mode((1, 1))
_cache = {}


class Sheet:
    def __init__(self, json_path: Path):
        self.doc = json.loads(json_path.read_text("utf-8"))
        self.img = pygame.image.load(str(json_path.parent / self.doc["sheet"])).convert_alpha()
        self.fw, self.fh = self.doc["frame"]["w"], self.doc["frame"]["h"]
        self.cols = self.doc["cols"]

    def index(self, clip, direction, k):
        ids = self.doc["clips"][clip]["frames"][direction]
        if k == "hit":
            k = self.doc.get("events", {}).get(clip, {}).get("hit", 0)
        elif k == "last":
            k = len(ids) - 1
        return ids[int(k)]

    def frame(self, clip, direction, k):
        n = self.index(clip, direction, k)
        s = pygame.Surface((self.fw, self.fh), pygame.SRCALPHA)
        s.blit(self.img, (0, 0), ((n % self.cols) * self.fw, (n // self.cols) * self.fh, self.fw, self.fh))
        return s

    def count(self, clip):
        return len(next(iter(self.doc["clips"][clip]["frames"].values())))


def load(kind_dir: Path, sid: str) -> Sheet:
    key = (str(kind_dir), sid)
    if key not in _cache:
        _cache[key] = Sheet(kind_dir / f"{sid}.json")
    return _cache[key]


def compose(weapon: str, char: str, clip: str, direction: str, k, weapon_dir: Path = WEAPONS,
            under: bool = False) -> pygame.Surface:
    c = load(CHARS, char)
    w = load(weapon_dir, weapon)
    out = pygame.Surface((c.fw, c.fh), pygame.SRCALPHA)
    if clip not in w.doc["clips"]:
        return c.frame(clip, direction, k)
    if under:
        out.blit(w.frame(clip, direction, k), (0, 0))
        out.blit(c.frame(clip, direction, k), (0, 0))
    else:
        out.blit(c.frame(clip, direction, k), (0, 0))
        out.blit(w.frame(clip, direction, k), (0, 0))
    return out


def sheet_of_cells(cells, cols, scale=3, bg=(18, 18, 24), pad=2, labels=None, label_w=0, title=None,
                   cell=96):
    """cells: list of Surfaces (or None) laid in a grid."""
    rows = -(-len(cells) // cols)
    top = 16 if title else 0
    W = label_w + cols * (cell * scale + pad) + pad
    H = top + rows * (cell * scale + pad) + pad
    img = pygame.Surface((W, H))
    img.fill((10, 10, 14))
    font = pygame.font.SysFont("arial", 11)
    if title:
        img.blit(font.render(title, True, (170, 170, 190)), (4, 1))
    for n, c in enumerate(cells):
        x = label_w + (n % cols) * (cell * scale + pad) + pad
        y = top + (n // cols) * (cell * scale + pad) + pad
        pygame.draw.rect(img, bg, (x, y, cell * scale, cell * scale))
        if c is not None:
            img.blit(pygame.transform.scale(c, (cell * scale, cell * scale)), (x, y))
    if labels:
        for r, text in enumerate(labels):
            if text:
                y = top + r * (cell * scale + pad) + pad + 4
                img.blit(font.render(text, True, (150, 150, 170)), (4, y))
    return img


def main(argv):
    wdir = WEAPONS
    out = ROOT / "art" / "render" / "weapon_layers" / "peek.png"
    if "--dir" in argv:
        i = argv.index("--dir")
        wdir = Path(argv[i + 1]) if Path(argv[i + 1]).is_absolute() else ROOT / argv[i + 1]
        del argv[i:i + 2]
    if "--out" in argv:
        i = argv.index("--out")
        out = Path(argv[i + 1])
        del argv[i:i + 2]
    weapon, char, *specs = argv
    cells = []
    for sp in specs:
        parts = sp.split(":")
        clip, d = parts[0], parts[1]
        ks = parts[2] if len(parts) > 2 else "all"
        n = load(wdir, weapon).count(clip) if clip in load(wdir, weapon).doc["clips"] else load(CHARS, char).count(clip)
        for k in (range(n) if ks == "all" else [ks]):
            cells.append(compose(weapon, char, clip, d, k, wdir))
    cols = max(1, min(len(cells), 8))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(sheet_of_cells(cells, cols, scale=3), str(out))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
