"""Abode realm: build and render the realm set (props/realm.png). Run through build.py (--parts realm).
    sys.argv[1:]: optional "--only name,name" (sprite names, or a family such as herb)"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy
import kit.api as kit
import wt_common as C

C.KIT = True
import wt_realm as G
import wt_render as R
import wt_village as V

ARGS = sys.argv[1:]
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None


def main():
    kit.clear_scene()
    sp = G.specs()
    if ONLY:
        sp = [s for s in sp if s["name"] in ONLY or False]
    else:
        kit.save_blend("art/blender/world_tiles/realm.blend") if False else None
    R.render_set("realm", sp, before=lambda s: V.CUR.__setitem__(slice(None), [s["W"], s["H"]]),
                 note="2x the old sprites (rift, pedestal, rune, pillar, statue, mirror, exit, chest). Frames sit side by side: frame i at rect.x + i * rect.w. "
                      "pivot = bottom centre of the rect (ground point); rune_* are drawn straight down like tiles")


main()
