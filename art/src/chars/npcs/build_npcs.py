#!/usr/bin/env python3
"""Village NPCs on the v2 player body: build, render (idle 4, walk 8, talk 4; four facings)
through the kit, QC, and the preview art/preview/npcs.png.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/npcs/build_npcs.py [--only id ...] [--gate] [--sheet-only]

--gate renders idle only into art/render/chars/npc_gate/ and writes the idle-down line-up
art/preview/npcs.png (self-review before the clips).
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

from kit import launcher  # noqa: E402

NPCS = ["shopkeeper", "alchemist", "smith", "librarian", "guide", "fisher", "truc_lao", "villager"]
OUT = "client/assets/v2/npcs"
GATE = "art/render/chars/npc_gate"
PLAYER = "client/assets/v2/chars/dao_si_luyen_khi.json"
SHEET = ROOT / "art" / "preview" / "npcs.png"
Z = 4


def build_one(npc: str, out: str, clips: str = "") -> int:
    args = ["--npc", npc, "--out", f"art/blender/chars/npc_{npc}.blend", "--render", out]
    if clips:
        args += ["--clips", clips]
    code = launcher.run_blender(HERE / "npc_main.py", "chars", args)
    print(f"[npcs] {npc}: {'ok' if code == 0 else f'FAILED ({code})'}", flush=True)
    return code


def _pg():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    return pygame


def _cell(pg, js, clip, d, i):
    doc = json.loads(js.read_text("utf-8"))
    sh = pg.image.load(str(js.with_name(doc["sheet"])))
    fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
    n = doc["clips"][clip]["frames"][d][i]
    c = sh.subsurface(((n % cols) * fw, (n // cols) * fh, fw, fh))
    return pg.transform.scale(c, (fw * Z, fh * Z)), doc.get("name_vi", js.stem)


def sheet(folder: str, gate: bool) -> None:
    pg = _pg()
    font = pg.font.SysFont(None, 30)
    cw = 96 * Z
    if gate:
        picks = [("idle", "down", 0)]
        cols = len(NPCS) + 1
        surf = pg.Surface((cols * cw, cw + 40))
        surf.fill((14, 13, 18))
        cells = [(_cell(pg, ROOT / PLAYER, "idle", "down", 0))] + [
            _cell(pg, ROOT / folder / f"{n}.json", *picks[0]) for n in NPCS if (ROOT / folder / f"{n}.json").exists()]
        for j, (c, name) in enumerate(cells):
            surf.blit(font.render(name, True, (190, 186, 200)), (j * cw + 8, 8))
            surf.blit(c, (j * cw, 40))
    else:
        picks = [("idle", "down", 0), ("idle", "right", 0), ("idle", "up", 0), ("idle", "left", 0),
                 ("walk", "right", 2), ("talk", "down", 1)]
        labels = ["idle down", "idle right", "idle up", "idle left", "walk right", "talk down"]
        surf = pg.Surface(((len(picks) + 1) * cw, 40 + len(NPCS) * (cw + 30)))
        surf.fill((14, 13, 18))
        for j, t in enumerate(["(player, for scale)"] + labels):
            surf.blit(font.render(t, True, (190, 186, 200)), (j * cw + 8, 8))
        y = 40
        for r, n in enumerate(NPCS):
            js = ROOT / folder / f"{n}.json"
            if not js.exists():
                continue
            if r == 0:
                pc, _ = _cell(pg, ROOT / PLAYER, "idle", "down", 0)
                surf.blit(pc, (0, y + 30))
            for j, (c, d, i) in enumerate(picks):
                cell, name = _cell(pg, js, c, d, i)
                surf.blit(cell, ((j + 1) * cw, y + 30))
            surf.blit(font.render(name, True, (170, 166, 180)), (cw + 8, y + 4))
            y += cw + 30
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    pg.image.save(surf, str(SHEET))
    print(f"[npcs] {SHEET}")


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--sheet-only", action="store_true")
    a = ap.parse_args(argv)
    ids = a.only or NPCS
    folder = GATE if a.gate else OUT
    if not a.sheet_only:
        with ThreadPoolExecutor(max_workers=4) as ex:
            codes = list(ex.map(lambda n: build_one(n, folder, "idle" if a.gate else ""), ids))
        if any(codes):
            return 1
    problems = 0
    if not a.gate:
        from kit import qc
        problems = qc.report(ROOT / OUT)
    sheet(folder, a.gate)
    print(f"[npcs] QC problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
