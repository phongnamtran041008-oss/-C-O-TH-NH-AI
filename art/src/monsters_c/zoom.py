#!/usr/bin/env python3
"""5x crops of key frames for the look rounds (venv python, needs pygame).

    python art/src/monsters_c/zoom.py thiet_giap_thu                # key frames, both looks
    python art/src/monsters_c/zoom.py thiet_giap_thu --clips windup,attack --dirs down,right
    python art/src/monsters_c/zoom.py loi_ung --all --z 4           # every frame
    python art/src/monsters_c/zoom.py van_diep --vs kiem_linh,phong_lang

Writes art/render/monsters_c/zoom_<id>.png (git-ignored): each requested frame at Z x
nearest-neighbour on the dark panel colour, the pivot marked, and optionally the first idle
frame of existing monsters (--vs) at the same zoom so size and finish can be compared.
Key frames by default: idle 0, walk 0 and 3, windup held (last), attack hit, hit 0, die last.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
import pygame  # noqa: E402

from kit import contact  # noqa: E402

MON = ROOT / "client" / "assets" / "v2" / "monsters"


def frames_of(doc, clip, d, every):
    ids = doc["clips"][clip]["frames"][d]
    if every:
        return list(enumerate(ids))
    hit = doc.get("events", {}).get("attack", {}).get("hit", 1)
    pick = {"idle": [0], "walk": [0, 3], "windup": [len(ids) - 1], "attack": [hit],
            "hit": [0], "die": [len(ids) - 1]}.get(clip, [0])
    return [(k, ids[k]) for k in pick]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--clips", default="idle,walk,windup,attack,hit,die")
    ap.add_argument("--dirs", default="down,left,up,right")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--z", type=int, default=5)
    ap.add_argument("--vs", default="")
    ap.add_argument("--base-only", action="store_true")
    a = ap.parse_args()
    pygame.init()
    pygame.display.set_mode((1, 1))
    Z = a.z
    f = contact._font(14)
    names = [a.id] if a.base_only else [a.id, f"{a.id}_di"]
    rows = []
    for name in names:
        p = MON / f"{name}.json"
        if not p.exists():
            continue
        doc = json.loads(p.read_text("utf-8"))
        sheet = pygame.image.load(str(MON / doc["sheet"]))
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        pv = (doc["pivot"]["x"], doc["pivot"]["y"])
        for d in a.dirs.split(","):
            cells = []
            for c in a.clips.split(","):
                for k, i in frames_of(doc, c, d, a.all):
                    cells.append((f"{c}{k}", contact._cell(sheet, i, cols, fw, fh)))
            rows.append((f"{name} {d}", cells, pv))
    for vs in [v for v in a.vs.split(",") if v]:
        doc = json.loads((MON / f"{vs}.json").read_text("utf-8"))
        sheet = pygame.image.load(str(MON / doc["sheet"]))
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        cells = [(f"{vs} {d}", contact._cell(sheet, doc["clips"]["idle"]["frames"][d][0], cols, fw, fh))
                 for d in ("down", "right")]
        rows.append((f"vs {vs}", cells, (doc["pivot"]["x"], doc["pivot"]["y"])))
    W = max(sum(c.get_width() * Z + 4 for _, c in cells) for _, cells, _ in rows) + 8
    H = sum(max(c.get_height() for _, c in cells) * Z + 26 for _, cells, _ in rows) + 8
    img = pygame.Surface((W, H))
    img.fill(contact.BG)
    y = 4
    for label, cells, pv in rows:
        img.blit(f.render(label, True, contact.TEXT), (4, y))
        y += 20
        x = 4
        for tag, c in cells:
            w, h = c.get_width() * Z, c.get_height() * Z
            pygame.draw.rect(img, contact.PANEL, (x, y, w, h))
            img.blit(pygame.transform.scale(c, (w, h)), (x, y))
            img.blit(contact._font(11).render(tag, True, contact.DIM), (x + 2, y + 2))
            mx, my = x + pv[0] * Z, y + pv[1] * Z
            pygame.draw.line(img, contact.PIVOT, (mx - 4, my), (mx + 4, my))
            x += w + 4
        y += max(c.get_height() for _, c in cells) * Z + 6
    out = ROOT / "art" / "render" / "monsters_c" / f"zoom_{a.id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(out)


if __name__ == "__main__":
    main()
