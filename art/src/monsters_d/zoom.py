#!/usr/bin/env python3
"""Zoomed crops of packed sheets, for judging creatures at sprite scale (venv python).

    python art/src/monsters_d/zoom.py OUT.png ROW [ROW ...] [--scale 5] [--player]

A ROW is `<sheet id or json path>:<clip>:<dir>[:<i,j,...>]` (all frames of the clip when
no indices are given), e.g. `hoa_yeu:windup:right` or `bach_vien_di:attack:down:1`.
Bare ids are looked up in client/assets/v2/monsters, then client/assets/v2/beasts.
`--player` puts the Luyện Khí player (idle, down) at the head of every row at the same
scale, standing on the same ground line, so size can be judged against the hero.
Frames are drawn nearest-neighbour on the dark panel colour of the contact sheets, with a
1-px grid tick on the pivot.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

import pygame  # noqa: E402

from kit import contact  # noqa: E402

V2 = ROOT / "client" / "assets" / "v2"


def find(ref: str) -> Path:
    p = Path(ref)
    if p.suffix == ".json":
        return p if p.is_absolute() else ROOT / p
    for sub in ("monsters", "beasts", "chars"):
        f = V2 / sub / f"{ref}.json"
        if f.exists():
            return f
    sys.exit(f"no sheet {ref!r}")


def frames(ref: str, clip: str, d: str, picks=None):
    f = find(ref)
    doc = json.loads(f.read_text("utf-8"))
    sheet = pygame.image.load(str(f.parent / doc["sheet"]))
    idx = doc["clips"][clip]["frames"][d]
    if picks is not None:
        idx = [idx[k] for k in picks]
    fw, fh = doc["frame"]["w"], doc["frame"]["h"]
    return [contact._cell(sheet, i, doc["cols"], fw, fh) for i in idx], (doc["pivot"]["x"], doc["pivot"]["y"])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("rows", nargs="+")
    ap.add_argument("--scale", type=int, default=5)
    ap.add_argument("--player", action="store_true")
    a = ap.parse_args(argv)
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    Z = a.scale
    rows = []
    for spec in a.rows:
        parts = spec.split(":")
        picks = [int(x) for x in parts[3].split(",")] if len(parts) > 3 and parts[3] else None
        cells, pv = frames(parts[0], parts[1], parts[2], picks)
        rows.append((spec, cells, pv))
    player = None
    if a.player:
        pc, ppv = frames("dao_si_luyen_khi", "idle", "down", [0])
        player = (pc[0], ppv)
    # every row shares one ground line
    above = max(pv[1] for _, _, pv in rows)
    below = max(c[0].get_height() - pv[1] for _, c, pv in rows)
    if player:
        above = max(above, player[1][1])
        below = max(below, player[0].get_height() - player[1][1])
    rh = (above + below) * Z + 22
    widths = []
    for _, cells, _ in rows:
        w = sum(c.get_width() * Z + 4 for c in cells)
        if player:
            w += player[0].get_width() * Z + 4
        widths.append(w)
    img = pygame.Surface((max(widths) + 12, len(rows) * rh + 8))
    img.fill(contact.BG)
    font = contact._font(13)
    for r, (label, cells, pv) in enumerate(rows):
        y0 = r * rh + 4
        img.blit(font.render(label, True, contact.TEXT), (6, y0))
        gy = y0 + 18 + above * Z
        x = 6
        seq = ([(player[0], player[1])] if player else []) + [(c, pv) for c in cells]
        for surf, p in seq:
            w, h = surf.get_width() * Z, surf.get_height() * Z
            top = gy - p[1] * Z
            pygame.draw.rect(img, contact.PANEL, (x, top, w, h))
            img.blit(pygame.transform.scale(surf, (w, h)), (x, top))
            pygame.draw.line(img, (60, 56, 70), (x, gy), (x + w - 1, gy))
            x += w + 4
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"zoom: {out}")


if __name__ == "__main__":
    main()
