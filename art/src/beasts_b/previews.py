#!/usr/bin/env python3
"""Look-round pictures for BEASTS_B (venv python, pygame only).

    python art/src/beasts_b/previews.py                 # overview + line-up + zooms
    python art/src/beasts_b/previews.py zoom ngoc_tho   # 5x key frames of one beast
    python art/src/beasts_b/previews.py wip ngoc_tho    # 4x every frame of a --clips render

Writes:
    art/preview/beasts_b.png          the six, facing right, every frame of every clip (x3)
    art/preview/beasts_b_lineup.png   the six existing beasts and the six new ones, idle,
                                      facing down and right (x4), the Luyện Khí player at
                                      the same scale for size
    art/preview/beasts_b_zoom_<id>.png  5x crops of the key frames (idle in four facings,
                                      walk right, held windup, attack hit, happy, sleep, die)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
from kit import contact  # noqa: E402

BEASTS = ROOT / "client" / "assets" / "v2" / "beasts"
WIP = ROOT / "art" / "render" / "beasts_b" / "wip"
PREVIEW = ROOT / "art" / "preview"
NEW = ["ngoc_tho", "tam_bao_thu", "kim_thiem", "bach_ho_con", "cuu_vi_ho", "kim_si_dieu"]
OLD = ["linh_ho", "huyen_quy", "bach_hac", "hoa_tuoc", "tieu_long", "ky_lan_con"]
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die", "happy", "sleep")
DIRS = ("down", "left", "up", "right")


def _init():
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))


def load(path: Path):
    doc = json.loads(path.read_text("utf-8"))
    sheet = pygame.image.load(str(path.parent / doc["sheet"]))
    return doc, sheet


def cell(doc, sheet, clip, d, k):
    i = doc["clips"][clip]["frames"][d][k]
    return contact._cell(sheet, i, doc["cols"], doc["frame"]["w"], doc["frame"]["h"])


def zoomed(s, z):
    return pygame.transform.scale(s, (s.get_width() * z, s.get_height() * z))


def overview(ids, out: Path, d="right"):
    _init()
    cv = contact.Canvas()
    cv.title(f"BEASTS_B  every clip facing {d}: idle | walk | windup | attack | hit | die | happy | sleep  (x3)")
    for mid in ids:
        f = BEASTS / f"{mid}.json"
        if not f.exists():
            continue
        doc, sheet = load(f)
        cells = []
        for c in CLIPS:
            if c in doc["clips"]:
                cells += [cell(doc, sheet, c, d, k) for k in range(len(doc["clips"][c]["frames"][d]))]
        cv.strip(doc.get("name_vi", mid), cells, [(doc["pivot"]["x"], doc["pivot"]["y"])] * len(cells))
    img = cv.render()
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"overview: {out}")


def lineup(out: Path, Z=4):
    """Old six then new six, idle frame 0, down and right, on one ground line, with the
    Luyện Khí player for scale."""
    _init()
    font = contact._font(13)
    items = []
    pj = ROOT / "client" / "assets" / "v2" / "chars" / "dao_si_luyen_khi.json"
    if pj.exists():
        pd, ps = load(pj)
        items.append(("người chơi", [cell(pd, ps, "idle", "down", 0)], (pd["pivot"]["x"], pd["pivot"]["y"])))
    for mid in OLD + NEW:
        f = BEASTS / f"{mid}.json"
        if not f.exists():
            continue
        doc, sheet = load(f)
        items.append((doc.get("name_vi", mid), [cell(doc, sheet, "idle", "down", 0), cell(doc, sheet, "idle", "right", 0)],
                      (doc["pivot"]["x"], doc["pivot"]["y"])))
    ground = 20 + 80 * Z           # screen y of the shared ground line
    x = 10
    placed = []
    for name, cells, pv in items:
        w = max(c.get_width() for c in cells)
        for c in cells:
            placed.append((zoomed(c, Z), x, ground - pv[1] * Z, name if c is cells[0] else None))
            x += w * Z + 4
        x += 14
    img = pygame.Surface((x + 10, ground + 14 * Z + 30))
    img.fill(contact.BG)
    pygame.draw.line(img, (40, 38, 50), (0, ground), (x + 10, ground))
    for s, px, py, name in placed:
        img.blit(s, (px, py))
        if name:
            img.blit(font.render(name, True, contact.TEXT), (px, ground + 8))
    img.blit(font.render("LINE-UP  idle frame 0, facing down | right, x4 (player at the same scale; the first six are the existing beasts)", True, contact.TEXT), (10, 4))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"line-up: {out}")


def zoom(mid: str, out: Path, Z=5, folder=BEASTS):
    """Key frames at 5x on a mid-grey and a dark panel (outline read on both)."""
    _init()
    doc, sheet = load(folder / f"{mid}.json")
    cl = doc["clips"]
    hit = doc.get("events", {}).get("attack", {}).get("hit", 1)
    picks = [("idle", d, 0) for d in DIRS]
    if "walk" in cl:
        picks += [("walk", "right", k) for k in range(len(cl["walk"]["frames"]["right"]))]
    picks += [(c, d, k) for c, d, k in (("windup", "down", -1), ("windup", "right", -1), ("attack", "right", hit),
                                         ("attack", "down", hit), ("hit", "right", 0), ("happy", "down", 1),
                                         ("happy", "right", 0), ("sleep", "right", 0), ("die", "right", -1))
              if c in cl]
    cols = 6
    fw, fh = doc["frame"]["w"], doc["frame"]["h"]
    cw, ch = fw * Z, fh * Z
    font = contact._font(13)
    rows = (len(picks) + cols - 1) // cols
    img = pygame.Surface((cols * (cw + 4) + 8, rows * (ch + 22) + 30))
    img.fill(contact.BG)
    img.blit(font.render(f"{doc.get('name_vi', mid)}  key frames x{Z}", True, contact.TEXT), (6, 6))
    for n, (c, d, k) in enumerate(picks):
        x = 6 + (n % cols) * (cw + 4)
        y = 28 + (n // cols) * (ch + 22)
        pygame.draw.rect(img, (70, 72, 64) if n % 2 else contact.PANEL, (x, y, cw, ch))
        img.blit(zoomed(cell(doc, sheet, c, d, k), Z), (x, y))
        img.blit(font.render(f"{c} {d} {k}", True, contact.DIM), (x + 2, y + ch + 2))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"zoom: {out}")


def wip(mid: str, Z=4):
    """Every frame of a partial (--clips) render, all four facings, at 4x."""
    _init()
    doc, sheet = load(WIP / f"{mid}.json")
    cv = contact.Canvas()
    for c in CLIPS:
        if c not in doc["clips"]:
            continue
        for d in DIRS:
            fr = doc["clips"][c]["frames"][d]
            cv.strip(f"{c} {d}", [zoomed(cell(doc, sheet, c, d, k), Z // 3 or 1) for k in range(len(fr))])
    img = cv.render()
    out = ROOT / "art" / "render" / "beasts_b" / f"wip_{mid}.png"
    pygame.image.save(img, str(out))
    print(f"wip: {out}")


def main(argv):
    if argv and argv[0] == "zoom":
        for mid in argv[1:] or NEW:
            zoom(mid, PREVIEW / f"beasts_b_zoom_{mid}.png")
        return 0
    if argv and argv[0] == "close":          # 8x faces, into art/render (not a deliverable)
        _init()
        for mid in argv[1:]:
            doc, sheet = load(BEASTS / f"{mid}.json")
            cells = [cell(doc, sheet, "idle", d, 0) for d in DIRS] + [cell(doc, sheet, "happy", "down", 1),
                                                                       cell(doc, sheet, "sleep", "down", 0)]
            img = pygame.Surface((len(cells) * (48 * 8 + 4), 48 * 8))
            img.fill(contact.PANEL)
            for n, c in enumerate(cells):
                img.blit(zoomed(c, 8), (n * (48 * 8 + 4), 0))
            out = ROOT / "art" / "render" / "beasts_b" / f"close_{mid}.png"
            pygame.image.save(img, str(out))
            print(f"close: {out}")
        return 0
    if argv and argv[0] == "wip":
        for mid in argv[1:]:
            wip(mid)
            zoom(mid, ROOT / "art" / "render" / "beasts_b" / f"wipzoom_{mid}.png", folder=WIP)
        return 0
    overview(NEW, PREVIEW / "beasts_b.png")
    lineup(PREVIEW / "beasts_b_lineup.png")
    for mid in NEW:
        if (BEASTS / f"{mid}.json").exists():
            zoom(mid, PREVIEW / f"beasts_b_zoom_{mid}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
