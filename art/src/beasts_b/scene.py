"""BEASTS_B inside headless Blender (started by build.py through kit.launcher).

    scene.py --id ngoc_tho [--no-render] [--clips idle,walk]

Builds one spirit beast from numbers, saves art/blender/beasts_b/<id>.blend, then renders
it through the shared kit into client/assets/v2/beasts/<id>.png/.json (kind "beast",
48x48, pivot 24,42, 38 px per metre, camera 35 degrees, four facings).
`--clips` renders only those clips into art/render/beasts_b/wip/ (look rounds), never
into the game folder.
"""
from __future__ import annotations

import argparse
import os
import importlib
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kit.api as kit  # noqa: E402

import common  # noqa: E402,F401  (puts monsters_a on sys.path)
import rig  # noqa: E402

OUT = "client/assets/v2/beasts"
WIP = "art/render/beasts_b/wip"
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die", "happy", "sleep")

# id -> (name_vi, module with build())
BEASTS = {
    "ngoc_tho": ("Ngọc Thố", "ngoc_tho"),
    "tam_bao_thu": ("Tầm Bảo Thử", "tam_bao_thu"),
    "kim_thiem": ("Bích Nhãn Kim Thiềm", "kim_thiem"),
    "bach_ho_con": ("Bạch Hổ Con", "bach_ho_con"),
    "cuu_vi_ho": ("Cửu Vĩ Hồ", "cuu_vi_ho"),
    "kim_si_dieu": ("Kim Sí Điểu", "kim_si_dieu"),
}


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
    """Eyes, catch-lights and pips win the pixel blocks they touch; dark facial marks
    (nose, mouth, stripes, whiskers) almost as surely, so the 6x downscale keeps them."""
    for m in bpy.data.materials:
        if "col_base" not in m or "kit_priority" in m:
            continue
        if "eye" in m.name or "pip" in m.name:
            m["kit_priority"] = 3.0
        elif any(k in m.name for k in ("mouth", "nose", "brow", "fang", "tooth", "stripe",
                                        "whisker", "mark", "talon", "claw")):
            m["kit_priority"] = 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--clips", default="")
    a = ap.parse_args(kit.args())
    name_vi, modname = BEASTS[a.id]
    mod = importlib.import_module(modname)
    rig.reset()
    bpy.context.scene.render.fps = 10
    arm = mod.build()
    if not any("holdout" in o.name for o in bpy.data.objects):
        rig.ground_holdout()
    arm["monster_id"] = a.id
    arm["name_vi"] = name_vi
    arm["frame"] = 48
    mark_priority()
    rig.apply_variant("base")
    bpy.context.scene.frame_set(1)
    kit.save_blend(f"art/blender/beasts_b/{a.id}.blend")
    kit.log(f"saved art/blender/beasts_b/{a.id}.blend")
    if a.no_render:
        return
    hold = [o for o in bpy.data.objects if "holdout" in o.name]
    only = [c for c in a.clips.split(",") if c]
    hide = [h for h in os.environ.get("BEASTS_B_HIDE", "").split(",") if h]
    if hide and only:       # look-round debugging: drop parts by name (WIP renders only)
        for o in [o for o in bpy.data.objects if any(h in o.name for h in hide)]:
            bpy.data.objects.remove(o)
    clips = clips_from_actions(only)
    big = {}
    if only and os.environ.get("BEASTS_B_BIG"):     # look-round debugging: 2x resolution WIP
        big = {"frame": (96, 96), "pivot": (48, 84), "ppm": 76.0}
    kit.render_animated(arm, a.id, clips, WIP if only else OUT, name_vi=name_vi, kind="beast",
                        holdout=hold or None, **big)


main()
