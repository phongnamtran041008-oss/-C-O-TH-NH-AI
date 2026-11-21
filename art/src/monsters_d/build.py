#!/usr/bin/env python3
"""Rebuild the MONSTERS_D batch: models, rigs, clips, .blend files, sprite sheets, QC and
contact sheets. Run with the game's venv python:

    python art/src/monsters_d/build.py                  # all six creatures
    python art/src/monsters_d/build.py --only hoa_yeu   # one (or a comma list)
    python art/src/monsters_d/build.py --jobs 1         # Blenders at once (default 2, max 2)
    python art/src/monsters_d/build.py --no-render      # only the .blend files
    python art/src/monsters_d/build.py --fit            # also run fitcheck.py on each .blend

Output:
    art/blender/monsters_d/<id>.blend
    client/assets/v2/monsters/<id>.png/.json and <id>_di.png/.json
    art/preview/monsters_d_<id>.png   every clip x every facing, both looks (3x)
    art/preview/monsters_d.png        all six facing right, every clip, both looks, with
                                      the player at the same scale (3x)
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import contact, launcher, qc  # noqa: E402
from kit import palette as P  # noqa: E402

IDS = ["hoa_yeu", "bach_vien", "co_quan_thu", "lo_linh", "thao_nhan", "xich_diem_ma"]
OUT = ROOT / "client" / "assets" / "v2" / "monsters"
PREVIEW = ROOT / "art" / "preview"
HERE = Path(__file__).resolve().parent
SCENE = HERE / "scene.py"
FIT = HERE / "fitcheck.py"
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die")


def build_one(mid: str, no_render: bool, fit: bool) -> int:
    args = ["--id", mid] + (["--no-render"] if no_render else [])
    code = launcher.run_blender(SCENE, "monsters_d", args)
    print(f"[monsters_d] {mid}: blender exit {code}", flush=True)
    if code == 0 and fit:
        code = launcher.run_blender(FIT, "monsters_d", [], blend=f"art/blender/monsters_d/{mid}.blend")
    return code


def run_qc(ids) -> int:
    colors = P.load().color_set
    bad = 0
    for mid in ids:
        for name in (mid, f"{mid}_di"):
            f = OUT / f"{name}.json"
            if not f.exists():
                print(f" - {name}: missing")
                bad += 1
                continue
            probs = qc.check_file(f, colors)
            for p in probs:
                print(f" - {p}")
            bad += len(probs)
    print(f"qc monsters_d: {'FAIL' if bad else 'OK'} ({2 * len(ids)} sheets, {bad} problem(s))")
    return bad


def overview(ids, out: Path, Z: int = 3):
    """One row per sheet: every frame of every clip facing right, on the shared ground
    line, with the Luyện Khí player (idle, down) at the head of the first row."""
    import pygame
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    rows = []
    for mid in ids:
        for name in (mid, f"{mid}_di"):
            f = OUT / f"{name}.json"
            if not f.exists():
                continue
            doc = json.loads(f.read_text("utf-8"))
            sheet = pygame.image.load(str(OUT / doc["sheet"]))
            fw, fh = doc["frame"]["w"], doc["frame"]["h"]
            cells = []
            for c in CLIPS:
                cells.append([contact._cell(sheet, i, doc["cols"], fw, fh)
                              for i in doc["clips"][c]["frames"]["right"]])
            rows.append((doc.get("name_vi", name), cells, (doc["pivot"]["x"], doc["pivot"]["y"])))
    pj = ROOT / "client" / "assets" / "v2" / "chars" / "dao_si_luyen_khi.json"
    pd = json.loads(pj.read_text("utf-8"))
    ps = pygame.image.load(str(pj.parent / pd["sheet"]))
    pf = contact._cell(ps, pd["clips"]["idle"]["frames"]["down"][0], pd["cols"], pd["frame"]["w"], pd["frame"]["h"])
    ppv = (pd["pivot"]["x"], pd["pivot"]["y"])
    lab = 150
    gap = 10
    row_h = 64 * Z + 8
    widths = [lab + pf.get_width() * Z + sum(sum(c.get_width() * Z + 2 for c in cl) + gap for cl in cells)
              for _, cells, _ in rows]
    img = pygame.Surface((max(widths) + 8, 34 + len(rows) * row_h))
    img.fill(contact.BG)
    img.blit(contact._font(14).render(
        "MONSTERS_D  facing right: idle | walk | windup | attack | hit | die   (x3; player x3 = in-game scale)",
        True, contact.TEXT), (8, 8))
    font = contact._font(12)
    for r, (name, cells, pv) in enumerate(rows):
        y0 = 34 + r * row_h
        gy = y0 + 58 * Z
        img.blit(font.render(name, True, contact.DIM), (8, y0 + 6))
        x = lab
        if r % 2 == 0:
            pw = pf.get_width() * Z
            img.blit(pygame.transform.scale(pf, (pw, pf.get_height() * Z)), (x, gy - ppv[1] * Z))
        x += pf.get_width() * Z
        for cl in cells:
            for s in cl:
                w, h = s.get_width() * Z, s.get_height() * Z
                top = gy - pv[1] * Z
                pygame.draw.rect(img, contact.PANEL, (x, top, w, h))
                img.blit(pygame.transform.scale(s, (w, h)), (x, top))
                x += w + 2
            x += gap
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"overview: {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--fit", action="store_true")
    a = ap.parse_args()
    ids = [i for i in a.only.split(",") if i] or IDS
    for i in ids:
        if i not in IDS:
            sys.exit(f"unknown id {i!r}; one of {IDS}")
    with ThreadPoolExecutor(max_workers=max(1, min(2, a.jobs))) as ex:
        codes = list(ex.map(lambda m: build_one(m, a.no_render, a.fit), ids))
    if any(codes):
        print("[monsters_d] some Blender runs failed; see art/render/monsters_d/*.log")
        return 1
    if a.no_render:
        return 0
    bad = run_qc(ids)
    for mid in ids:
        out = PREVIEW / f"monsters_d_{mid}.png"
        contact.write([OUT / f"{n}.json" for n in (mid, f"{mid}_di")], out, title=f"monsters_d {mid}")
        print(f"contact sheet: {out}")
    overview([m for m in IDS if (OUT / f"{m}.json").exists()], PREVIEW / "monsters_d.png")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
