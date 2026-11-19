"""Blender entry for the v2 player: build one look (or rig_base), save it, render it.

    (via kit.launcher) v2_main.py --look <id>|rig_base --out <blend> [--render DIR] [--clips idle,walk]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import v2_rig  # noqa: E402  (bone table first)
import bpy  # noqa: E402
import rig as R  # noqa: E402
import clips  # noqa: E402
import v2_clips  # noqa: E402
import v2_looks  # noqa: E402


def build(look_id: str, out: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    col_rig = bpy.data.collections.new("COL_dao_si")
    scene.collection.children.link(col_rig)
    arm = R.build_armature(col_rig)
    R.add_sockets(arm, col_rig)
    actions = clips.build_actions(arm)
    if look_id == "rig_base":
        col = bpy.data.collections.new("COL_body")
        scene.collection.children.link(col)
        objs = v2_looks.build_base(arm, col)
        name_vi = "Đạo Sĩ (thân gốc)"
    else:
        col = bpy.data.collections.new(f"COL_outfit_{look_id}")
        scene.collection.children.link(col)
        objs = v2_looks.build(arm, col, look_id)
        name_vi = v2_looks.LOOKS[look_id]
    arm.animation_data.action = actions["idle"]
    scene.frame_set(R.FRAME0)
    scene["char_id"] = look_id
    scene["name_vi"] = name_vi
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    print(f"CHARS v2 built {look_id}: {len(objs)} pieces, {len(actions)} actions -> {out}")
    return arm, name_vi


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--look", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--render", default="")
    ap.add_argument("--clips", default="")
    a = ap.parse_args(argv)
    arm, name_vi = build(a.look, Path(a.out))
    if a.render:
        import kit.api as kit
        clip_spec = dict(kit.PLAYER_CLIPS)
        kind = "player"
        if a.clips:
            clip_spec = {c: clip_spec[c] for c in a.clips.split(",")}
            kind = "lookdev"          # a partial sheet (gate render): no all-clips rule
        kit.render_animated(arm, a.look, clip_spec, a.render, name_vi=name_vi, kind=kind,
                            frame=v2_rig.FRAME, pivot=v2_rig.PIVOT, ppm=v2_rig.PPM,
                            elevation=v2_rig.ELEVATION, snap=True, snap_to="head", ground_clips=["die"])


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
