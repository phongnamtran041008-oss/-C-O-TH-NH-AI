#!/usr/bin/env python3
"""Rebuild BEASTS_B: six spirit beasts (models, rigs, clips, .blend files, sprite sheets,
QC and contact sheets). Run with the game's venv python:

    python art/src/beasts_b/build.py                    # all six
    python art/src/beasts_b/build.py --only ngoc_tho    # one (or a comma list)
    python art/src/beasts_b/build.py --jobs 2           # Blenders at once (default 2)
    python art/src/beasts_b/build.py --no-render        # only the .blend files
    python art/src/beasts_b/build.py --only x --clips idle,walk   # look round: those clips
                                          into art/render/beasts_b/wip/, never the game

Output:
    art/blender/beasts_b/<id>.blend
    client/assets/v2/beasts/<id>.png/.json
    art/preview/beasts_b_<id>.png        every clip x every facing (x3)
    art/preview/beasts_b.png             the six, facing right, every clip (x3)
    art/preview/beasts_b_lineup.png      the old six and the new six side by side (x4)
    art/preview/beasts_b_zoom_<id>.png   5x key frames
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
sys.path.insert(0, str(HERE))

from kit import contact, launcher, qc  # noqa: E402
from kit import palette as P  # noqa: E402

import previews  # noqa: E402

IDS = previews.NEW
OUT = ROOT / "client" / "assets" / "v2" / "beasts"
PREVIEW = ROOT / "art" / "preview"
SCENE = HERE / "scene.py"


def build_one(mid: str, no_render: bool, clips: str) -> int:
    args = ["--id", mid] + (["--no-render"] if no_render else []) + (["--clips", clips] if clips else [])
    code = launcher.run_blender(SCENE, "beasts_b", args)
    print(f"[beasts_b] {mid}: blender exit {code}", flush=True)
    return code


def run_qc(ids) -> int:
    colors = P.load().color_set
    bad = 0
    for mid in ids:
        f = OUT / f"{mid}.json"
        if not f.exists():
            print(f" - {mid}: missing")
            bad += 1
            continue
        probs = qc.check_file(f, colors)
        for p in probs:
            print(f" - {p}")
        bad += len(probs)
    print(f"qc beasts_b: {'FAIL' if bad else 'OK'} ({len(ids)} sheets, {bad} problem(s))")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--clips", default="")
    a = ap.parse_args()
    ids = [i for i in a.only.split(",") if i] or IDS
    for i in ids:
        if i not in IDS:
            sys.exit(f"unknown id {i!r}; one of {IDS}")
    with ThreadPoolExecutor(max_workers=max(1, min(2, a.jobs))) as ex:
        codes = list(ex.map(lambda m: build_one(m, a.no_render, a.clips), ids))
    if any(codes):
        print("[beasts_b] some Blender runs failed; see art/render/beasts_b/*.log")
        return 1
    if a.no_render:
        return 0
    if a.clips:
        previews.main(["wip"] + ids)
        return 0
    bad = run_qc(ids)
    for mid in ids:
        out = PREVIEW / f"beasts_b_{mid}.png"
        contact.write([OUT / f"{mid}.json"], out, title=f"beasts_b {mid}")
        print(f"contact sheet: {out}")
    previews.main([])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
