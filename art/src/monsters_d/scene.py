"""MONSTERS_D inside headless Blender (started by build.py through kit.launcher).

    scene.py --id hoa_yeu [--no-render]

Builds one creature from numbers (bestiary_d.py), saves art/blender/monsters_d/<id>.blend,
then renders it through the shared kit twice: the normal look as `<id>` and the dị chủng
variant (same model, the materials' second colour/ramp set) as `<id>_di`, both into
client/assets/v2/monsters.

The helpers of art/src/monsters_a (rig.py, quadrupeds.py) are imported from that folder
as they are; nothing there is edited.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "monsters_a"))
sys.path.insert(0, str(HERE))

import kit.api as kit  # noqa: E402

import bestiary_d  # noqa: E402
import rig  # noqa: E402

OUT = "client/assets/v2/monsters"
KIND = {48: "monster", 64: "elite"}
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die")


def clips_from_actions() -> dict:
    out = {}
    for name in CLIPS:
        act = bpy.data.actions.get(name)
        if act is None:
            continue
        c = {"frames": int(act["frames"]), "fps": float(act["fps"]), "loop": bool(act["loop"]),
             "action": name}
        if "hit" in act:
            c["events"] = {"hit": int(act["hit"])}
        out[name] = c
    return out


def mark_priority():
    """Small features must survive the 6x downscale (same rules as MONSTERS_A): glowing eyes
    win any block they touch, dark facial marks almost as surely; thin glowing lines keep
    their pixels but get no halo."""
    lines = ("rune", "grid", "edge", "line", "vent")
    for m in bpy.data.materials:
        if "col_base" not in m or "kit_priority" in m:
            continue
        if any(k in m.name for k in lines):
            m["kit_priority"] = 2.0
            m["kit_halo"] = 0
        elif "eye" in m.name or "pip" in m.name:
            m["kit_priority"] = 3.0
        elif any(k in m.name for k in ("mouth", "nose", "socket", "brow", "fang", "tooth", "scar")):
            m["kit_priority"] = 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args(kit.args())
    name_vi, frame, fn = bestiary_d.BUILD[a.id]
    rig.reset()
    bpy.context.scene.render.fps = 10
    arm = fn()
    if not any("holdout" in o.name for o in bpy.data.objects):
        rig.ground_holdout()
    arm["monster_id"] = a.id
    arm["name_vi"] = name_vi
    arm["frame"] = frame
    mark_priority()
    rig.apply_variant("base")
    bpy.context.scene.frame_set(1)
    kit.save_blend(f"art/blender/monsters_d/{a.id}.blend")
    kit.log(f"saved art/blender/monsters_d/{a.id}.blend")
    if a.no_render:
        return
    hold = [o for o in bpy.data.objects if "holdout" in o.name]
    clips = clips_from_actions()
    # The big elites stand on a footprint wider than the kit's ground band (a few px under
    # the pivot): per facing, the armature object slides straight away from the camera by
    # shift_<dir> metres, so the limbs nearest the camera stand on the pivot row and the
    # far ones draw higher, as they should. See fitcheck.py and README.
    # A clip may override it (`shift_<dir>_<clip>`): a rearing horse has only its hind
    # hooves on the ground.

    def away(d, clip_name):
        key = "side" if d in ("left", "right") else d
        v = float(arm.get(f"shift_{key}_{clip_name}", arm.get(f"shift_{key}", 0.0)))
        return {"down": (0.0, v), "up": (0.0, -v), "right": (v, 0.0), "left": (-v, 0.0)}[d]

    def on_frame(clip_name, d, i):
        x, y = away(d, clip_name)
        arm.location = (x, y, 0.0)
        bpy.context.view_layer.update()

    hook = on_frame if any(k.startswith("shift_") for k in arm.keys()) else None
    for variant, out_id, label in (("base", a.id, name_vi), ("di", f"{a.id}_di", f"{name_vi} Dị Chủng")):
        rig.apply_variant(variant)
        kit.render_animated(arm, out_id, clips, OUT, name_vi=label, kind=KIND[frame],
                            holdout=hold or None, on_frame=hook)
    arm.location = (0, 0, 0)


main()
