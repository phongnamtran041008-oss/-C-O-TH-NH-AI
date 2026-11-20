"""MONSTERS_C inside headless Blender (started by build.py through kit.launcher).

    scene.py --id loi_ung [--no-render] [--fit] [--clips idle,windup] [--base-only]

Builds one creature from numbers, saves art/blender/monsters_c/<id>.blend, optionally runs
the MONSTERS_A fit check (every vertex of every frame projected through the kit camera),
then renders it through the shared kit twice: the normal look as `<id>` and the dị chủng
variant (same model, the materials' second colour/ramp set) as `<id>_di`, both into
client/assets/v2/monsters. --clips / --base-only are for quick look rounds only (the
contract needs every clip, so a full build never uses them).
"""
from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common  # noqa: E402,F401  (puts monsters_a on sys.path)
import kit.api as kit  # noqa: E402

import creatures_c  # noqa: E402
import rig  # noqa: E402

OUT = "client/assets/v2/monsters"
KIND = {48: "monster", 64: "elite", 96: "boss"}
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die")


def clips_from_actions(only=None) -> dict:
    out = {}
    for name in CLIPS:
        act = bpy.data.actions.get(name)
        if act is None or (only and name not in only):
            continue
        c = {"frames": int(act["frames"]), "fps": float(act["fps"]), "loop": bool(act["loop"]),
             "action": name}
        if "hit" in act:
            c["events"] = {"hit": int(act["hit"])}
        out[name] = c
    return out


def mark_priority():
    """Small features must survive the 6x downscale: glowing eyes win any pixel block they
    touch, dark facial marks almost as surely; thin glowing lines (bolts, runes, wing
    curls) keep their pixels but get no halo (a halo round a 1 px line floods the part)."""
    lines = ("rune", "line", "bolt", "curl", "vein", "edge", "tip")
    for m in bpy.data.materials:
        if "col_base" not in m:
            continue
        if "kit_priority" in m:
            continue
        if any(k in m.name for k in lines):
            m["kit_priority"] = 2.0
            m["kit_halo"] = 0
        elif "eye" in m.name or "pupil" in m.name:
            m["kit_priority"] = 3.0
        elif any(k in m.name for k in ("mouth", "nose", "socket", "brow", "fang", "tooth", "face")):
            m["kit_priority"] = 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--clips", default="")
    ap.add_argument("--base-only", action="store_true")
    a = ap.parse_args(kit.args())
    name_vi, frame, fn, opts = creatures_c._table()[a.id]
    rig.reset()
    bpy.context.scene.render.fps = 10
    arm = fn()
    if not any("holdout" in o.name for o in bpy.data.objects):
        rig.ground_holdout()        # whatever dips below the ground is cut cleanly
    arm["monster_id"] = a.id
    arm["name_vi"] = name_vi
    arm["frame"] = frame
    mark_priority()
    rig.apply_variant("base")
    bpy.context.scene.frame_set(1)
    kit.save_blend(f"art/blender/monsters_c/{a.id}.blend")
    kit.log(f"saved art/blender/monsters_c/{a.id}.blend")
    if a.fit:
        runpy.run_path(str(common.MA / "fitcheck.py"), run_name="__fit__")
    if a.no_render:
        return
    hold = [o for o in bpy.data.objects if "holdout" in o.name]
    clips = clips_from_actions([c for c in a.clips.split(",") if c])
    looks = [("base", a.id, name_vi), ("di", f"{a.id}_di", f"{name_vi} Dị Chủng")]
    if a.base_only:
        looks = looks[:1]
    ground = opts.get("ground")
    for variant, out_id, label in looks:
        rig.apply_variant(variant)
        kw = {"ground_clips": ground} if ground else {}
        kit.render_animated(arm, out_id, clips, OUT, name_vi=label, kind=KIND[frame],
                            holdout=hold or None, **kw)


main()
