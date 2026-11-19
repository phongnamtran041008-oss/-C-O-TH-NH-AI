#!/usr/bin/env python3
"""v2 look-dev of the player: build + render Luyện Khí and Hóa Thần (idle, walk, slash) at
96x96 / 15 degrees through the kit, QC the folder, write art/preview/chars_lookdev.png.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/lookdev/build_lookdev.py [--only id ...] [--sheet-only]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher, qc  # noqa: E402

OUT = "client/assets/v2/_lookdev"
LOOKS = ["dao_si_luyen_khi", "dao_si_hoa_than"]
REF = ROOT / "art" / "reference" / "nhan_vat" / "nhan_vat_8_canh_gioi.webp"
SHEET = ROOT / "art" / "preview" / "chars_lookdev.png"
Z = 4                       # zoom of the comparison sheet
FIG_PX = 48                 # our standing figure height in final pixels


def build_one(look_id: str) -> int:
    return launcher.run_blender(HERE / "ld_main.py", "chars", [
        "--look", look_id, "--out", f"art/blender/chars/lookdev_{look_id}.blend", "--render", OUT])


def sheet() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    bg = (14, 13, 18)
    ref = pygame.image.load(str(REF))
    # reference rows 1 and 5: figures are ~104 px tall in 128 px cells -> scale to FIG_PX
    k = FIG_PX / 104.0
    rows = []
    for r in (0, 4):
        strip = ref.subsurface((0, r * 128, 1024, 128))
        small = pygame.transform.smoothscale(strip, (round(1024 * k), round(128 * k)))
        rows.append(pygame.transform.scale(small, (small.get_width() * Z, small.get_height() * Z)))
    picks = [("idle", "down", 0), ("idle", "right", 0), ("idle", "up", 0), ("idle", "left", 0),
             ("walk", "down", 2), ("walk", "right", 2),
             ("slash", "right", 1), ("slash", "right", 3), ("slash", "right", 5),
             ("slash", "down", 1), ("slash", "down", 3), ("slash", "down", 5)]
    ours = []
    for lid in LOOKS:
        js = ROOT / OUT / f"{lid}.json"
        if not js.exists():
            continue
        doc = json.loads(js.read_text("utf-8"))
        sh = pygame.image.load(str(js.with_name(doc["sheet"])))
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        cells = []
        for c, d, i in picks:
            n = doc["clips"][c]["frames"][d][i]
            cell = sh.subsurface(((n % cols) * fw, (n // cols) * fh, fw, fh))
            cells.append(pygame.transform.scale(cell, (fw * Z, fh * Z)))
        ours.append(cells)
    cw = 96 * Z
    width = max(max(r.get_width() for r in rows), len(picks) * cw)
    height = sum(r.get_height() for r in rows) + len(ours) * 96 * Z + 40
    out = pygame.Surface((width, height))
    out.fill(bg)
    font = pygame.font.SysFont(None, 28)
    y = 0
    for r in rows:
        out.blit(r, (0, y))
        y += r.get_height()
    labels = ["idle down", "idle right", "idle up", "idle left", "walk down", "walk right",
              "slash R wind", "slash R strike", "slash R recover", "slash D wind", "slash D strike", "slash D recover"]
    for j, t in enumerate(labels):
        out.blit(font.render(t, True, (170, 166, 180)), (j * cw + 8, y + 8))
    y += 40
    for cells in ours:
        for j, c in enumerate(cells):
            out.blit(c, (j * cw, y))
        y += 96 * Z
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(out, str(SHEET))
    print(f"[lookdev] sheet: {SHEET} {out.get_size()}")


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--sheet-only", action="store_true")
    a = ap.parse_args(argv)
    if not a.sheet_only:
        ids = a.only or LOOKS
        with ThreadPoolExecutor(max_workers=2) as ex:
            codes = list(ex.map(build_one, ids))
        if any(codes):
            return 1
    problems = qc.report(ROOT / OUT)
    sheet()
    print(f"[lookdev] QC problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
