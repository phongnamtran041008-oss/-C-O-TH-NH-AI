#!/usr/bin/env python3
"""Rebuild the MONSTERS_C batch: models, rigs, clips, .blend files, sprite sheets, QC and
contact sheets. Run with the game's venv python:

    python art/src/monsters_c/build.py                    # all seven creatures
    python art/src/monsters_c/build.py --only loi_ung     # one (or a comma list)
    python art/src/monsters_c/build.py --jobs 2           # Blenders at once (default 2)
    python art/src/monsters_c/build.py --no-render        # only the .blend files
    python art/src/monsters_c/build.py --fit              # print the fit check per clip too

Each creature is built and rendered in its own headless Blender (scene.py through
kit.launcher). Output:

    art/blender/monsters_c/<id>.blend
    client/assets/v2/monsters/<id>.png/.json and <id>_di.png/.json
    art/preview/monsters_c_<id>.png    every clip x every facing, both looks (x3)
    art/preview/monsters_c.png         all seven: every frame of every clip, facing right,
                                       normal and dị chủng, with the player for scale (x3)
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

IDS = ["thiet_giap_thu", "vong_hon_kiem_si", "van_diep", "loi_ung", "u_minh_dang",
       "huyet_ngac", "loi_linh"]
OUT = ROOT / "client" / "assets" / "v2" / "monsters"
PREVIEW = ROOT / "art" / "preview"
SCENE = Path(__file__).with_name("scene.py")
CLIP_ORDER = ("idle", "walk", "windup", "attack", "hit", "die")


def build_one(mid: str, extra: list[str]) -> int:
    code = launcher.run_blender(SCENE, "monsters_c", ["--id", mid] + extra)
    print(f"[monsters_c] {mid}: blender exit {code}", flush=True)
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
    print(f"qc monsters_c: {'FAIL' if bad else 'OK'} ({2 * len(ids)} sheets, {bad} problem(s))")
    return bad


def _player():
    import pygame
    pj = ROOT / "client" / "assets" / "v2" / "chars" / "dao_si_luyen_khi.json"
    if not pj.exists():
        return None
    pd = json.loads(pj.read_text("utf-8"))
    ps = pygame.image.load(str(pj.parent / pd["sheet"]))
    cell = contact._cell(ps, pd["clips"]["idle"]["frames"]["right"][0], pd["cols"],
                         pd["frame"]["w"], pd["frame"]["h"])
    return cell, (pd["pivot"]["x"], pd["pivot"]["y"])


def overview(ids, out: Path, facing: str = "right"):
    """One facing, every frame of every clip, normal look then dị chủng, each row starting
    with the Luyện Khí player at the same scale standing on the same ground line."""
    import pygame
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    Z, pad, lab, gap = 3, 6, 150, 10
    player = _player()
    rows = []
    for mid in ids:
        for name in (mid, f"{mid}_di"):
            f = OUT / f"{name}.json"
            if not f.exists():
                continue
            doc = json.loads(f.read_text("utf-8"))
            sheet = pygame.image.load(str(OUT / doc["sheet"]))
            fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
            groups = []
            for c in CLIP_ORDER:
                ids_ = doc["clips"][c]["frames"][facing]
                groups.append((c, [contact._cell(sheet, i, cols, fw, fh) for i in ids_]))
            hit = doc.get("events", {}).get("attack", {}).get("hit")
            rows.append((doc.get("name_vi", name), (fw, fh), (doc["pivot"]["x"], doc["pivot"]["y"]),
                         groups, hit))
    if not rows:
        return
    pw = player[0].get_width() * Z if player else 0
    ph_above = (player[1][1] * Z) if player else 0
    width = lab + pw + pad
    heights = []
    for _, (fw, fh), (px, py), groups, _ in rows:
        w = lab + pw + pad + sum(len(g) * (fw * Z + 2) + gap for _, g in groups)
        width = max(width, w)
        heights.append(max(fh * Z, ph_above - py * Z + fh * Z) + 22)
    height = 34 + sum(heights) + pad
    img = pygame.Surface((width, height))
    img.fill(contact.BG)
    ft, f = contact._font(15), contact._font(12)
    img.blit(ft.render(f"MONSTERS_C  every clip, facing {facing}  (x{Z})  "
                       "idle | walk | windup | attack (* = hit frame) | hit | die   "
                       "- player (Luyện Khí) at the same scale on the left", True, contact.TEXT), (pad, 8))
    y = 34
    for (name, (fw, fh), (px, py), groups, hit), rh in zip(rows, heights):
        top = y + 18 + max(0, ph_above - py * Z)        # frame top, so pivots share a line
        ground = top + py * Z
        img.blit(f.render(name, True, contact.DIM), (pad, y + 2))
        if player:
            pc, (ppx, ppy) = player
            img.blit(pygame.transform.scale(pc, (pc.get_width() * Z, pc.get_height() * Z)),
                     (lab, ground - ppy * Z))
        x = lab + pw + pad
        for c, cells in groups:
            img.blit(f.render(c, True, contact.DIM), (x, y + 2))
            for k, s in enumerate(cells):
                pygame.draw.rect(img, contact.PANEL, (x, top, fw * Z, fh * Z))
                img.blit(pygame.transform.scale(s, (fw * Z, fh * Z)), (x, top))
                if c == "attack" and k == hit:
                    img.blit(f.render("*", True, contact.PIVOT), (x + 2, top + 2))
                x += fw * Z + 2
            x += gap
        y += rh
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"overview: {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--clips", default="", help="look rounds only: render a subset of clips")
    ap.add_argument("--base-only", action="store_true", help="look rounds only: skip the _di look")
    a = ap.parse_args()
    ids = [i for i in a.only.split(",") if i] or IDS
    for i in ids:
        if i not in IDS:
            sys.exit(f"unknown id {i!r}; one of {IDS}")
    extra = (["--no-render"] if a.no_render else []) + (["--fit"] if a.fit else []) \
        + (["--clips", a.clips] if a.clips else []) + (["--base-only"] if a.base_only else [])
    with ThreadPoolExecutor(max_workers=max(1, min(2, a.jobs))) as ex:
        codes = list(ex.map(lambda m: build_one(m, extra), ids))
    if any(codes):
        print("[monsters_c] some Blender runs failed; see art/render/monsters_c/*.log")
        return 1
    if a.no_render or a.clips or a.base_only:
        return 0
    bad = run_qc(ids)
    for mid in ids:
        out = PREVIEW / f"monsters_c_{mid}.png"
        contact.write([OUT / f"{n}.json" for n in (mid, f"{mid}_di")], out, title=f"monsters_c {mid}")
        print(f"contact sheet: {out}")
    overview([m for m in IDS if (OUT / f"{m}.json").exists()], PREVIEW / "monsters_c.png")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
