"""MONSTERS_A inside headless Blender (started by build.py through kit.launcher).

    scene.py --id kiem_linh [--no-render]

Builds one creature from numbers (creatures.py and friends), saves
art/blender/monsters/<id>.blend, then renders it through the shared kit twice: the normal
look as `<id>` and the dị chủng variant (same model, the materials' second colour/ramp set)
as `<id>_di`, both into client/assets/v2/monsters.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import kit.api as kit  # noqa: E402

import creatures  # noqa: E402
import rig  # noqa: E402

OUT = "client/assets/v2/monsters"
KIND = {48: "monster", 64: "elite", 96: "boss"}
CLIPS = ("idle", "walk", "windup", "attack", "hit", "die", "special", "happy", "sleep")


def clips_from_actions() -> dict:
    """The six monster clips with the frame counts, fps and hit frame the actions carry."""
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
    """Small features must survive the 6x downscale: glowing eyes win any pixel block they
    touch, dark facial marks almost as surely. Thin glowing lines (blade runes, grid lines,
    blade edges, flow dots) keep their pixels but get no halo: a halo round a line on a
    4 px blade floods the whole blade with glow."""
    lines = ("rune", "grid", "edge", "flow", "mark", "line", "bolt")
    for m in bpy.data.materials:
        if "col_base" not in m:
            continue
        if any(k in m.name for k in lines):
            m["kit_priority"] = 2.0
            m["kit_halo"] = 0
        elif "eye" in m.name or "pip" in m.name:
            m["kit_priority"] = 3.0
        elif any(k in m.name for k in ("mouth", "nose", "socket", "brow", "fang", "tooth")):
            m["kit_priority"] = 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args(kit.args())
    beasts, pets = creatures._beasts(), creatures._pets()
    pet = a.id in pets
    beast = a.id in beasts or pet          # pets live with the beasts, one look, kind "pet"
    name_vi, frame, fn = (pets if pet else beasts if beast else creatures.BUILD)[a.id]
    folder = "beasts" if beast else "monsters"
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
    kit.save_blend(f"art/blender/{folder}/{a.id}.blend")
    kit.log(f"saved art/blender/{folder}/{a.id}.blend")
    if a.no_render:
        return
    hold = [o for o in bpy.data.objects if "holdout" in o.name]
    clips = clips_from_actions()
    looks = [("base", a.id, name_vi)]
    if not beast:            # spirit beasts have one look; monsters add the dị chủng
        looks.append(("di", f"{a.id}_di", f"{name_vi} Dị Chủng"))
    for variant, out_id, label in looks:
        rig.apply_variant(variant)
        if pet:      # kind "pet": QC asks for no combat clips; framed like a beast
            kit.render_animated(arm, out_id, clips, f"client/assets/v2/{folder}", name_vi=label,
                                kind="pet", frame=(48, 48), pivot=(24, 42), ppm=38.0, holdout=hold or None)
            continue
        kit.render_animated(arm, out_id, clips, f"client/assets/v2/{folder}", name_vi=label,
                            kind="beast" if beast else KIND[frame], holdout=hold or None)


main()
