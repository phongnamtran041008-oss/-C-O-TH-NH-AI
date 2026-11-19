"""The 18 spirit bees inside headless Blender (started by build.py through kit.launcher).

    bee_scene.py [--only muc,thao] [--no-render]

Builds the one bee rig (bee.py), saves art/blender/beasts/bee.blend, then renders one sheet
per species of server/data/creatures/bees.json as client/assets/v2/beasts/bee_<id>, with the
species' look colours on the shared materials. 32x32 frame, pivot (16,16) on the body
centre, camera at 12 degrees (side-on),
facings right and left, clips fly (4, loop) and sting (2, events.hit = 0).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kit.api as kit  # noqa: E402

import bee  # noqa: E402
import rig  # noqa: E402

CLIPS = {"fly": {"frames": 4, "fps": 12, "loop": True, "action": "fly"},
         "sting": {"frames": 2, "fps": 12, "loop": False, "action": "sting", "events": {"hit": 0}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args(kit.args())
    rig.reset()
    arm = bee.build_bee()
    bee.recolour(bee.DATA["hoang_kim"]["look"], bee.DATA["hoang_kim"]["element"], "hoang_kim")
    bpy.context.scene.frame_set(1)
    kit.save_blend("art/blender/beasts/bee.blend")
    if a.no_render:
        return
    ids = [i for i in a.only.split(",") if i] or list(bee.DATA)
    for sid in ids:
        spec = bee.DATA[sid]
        bee.recolour(spec["look"], spec.get("element", ""), sid)
        kit.render_animated(arm, f"bee_{sid}", CLIPS, "client/assets/v2/beasts", name_vi=spec.get("name_vi", sid),
                            kind="bee", frame=(32, 32), pivot=(16, 16), ppm=38.0, elevation=12.0,
                            dirs={"right": 90.0, "left": 270.0})


main()
