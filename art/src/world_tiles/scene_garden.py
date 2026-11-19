"""Abode garden: build and render the garden set (props/garden.png). Run through build.py (--parts garden).
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
import wt_garden as G
import wt_render as R
import wt_village as V

ARGS = sys.argv[1:]
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None


def main():
    kit.clear_scene()
    sp = G.specs()
    if ONLY:
        sp = [s for s in sp if s["name"] in ONLY or s.get("extra", {}).get("family") in ONLY]
    else:
        kit.save_blend("art/blender/world_tiles/garden.blend") if False else None
    R.render_set("garden", sp, before=lambda s: V.CUR.__setitem__(slice(None), [s["W"], s["H"]]),
                 note="2x the old sprites. plants: <family>_<stage> (stages 0-2) and <family>_<stage>_<rarity> (stages 3-5), 2 frames of sway "
                      "laid side by side (frame i at rect.x + i * rect.w); pivot = ground point, bottom centre of the rect")


main()
