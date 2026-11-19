"""TD kit (props/td.png). Run through build.py (--parts td).
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
import wt_td as G
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
        kit.save_blend("art/blender/world_tiles/garden.blend") if False else None
    R.render_set("td", sp, before=lambda s: V.CUR.__setitem__(slice(None), [s["W"], s["H"]]),
                 note="native 24 px board cell. towers: tower_<role>_<level>; frames sit side by side (frame i at rect.x + i * rect.w); pivot = ground point")


main()
