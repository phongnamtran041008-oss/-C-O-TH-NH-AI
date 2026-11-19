"""Blender entry for the v2 look-dev: build one look, save it, render it through the kit.

    (via kit.launcher) ld_main.py --look dao_si_luyen_khi --out art/blender/chars/lookdev_x.blend [--render DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))

import bpy  # noqa: E402

import ld_rig  # noqa: E402,F401  (installs the v2 bone table into rig.py)
import rig as R  # noqa: E402
import clips  # noqa: E402
import ld_clips  # noqa: E402
import ld_looks  # noqa: E402

FRAME = (96, 96)
PIVOT = (48, 80)
ELEVATION = 15.0


def build(look_id: str, out: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    col_rig = bpy.data.collections.new("COL_dao_si")
    scene.collection.children.link(col_rig)
    arm = R.build_armature(col_rig)
    sockets = R.add_sockets(arm, col_rig)
    actions = clips.build_actions(arm)
    col = bpy.data.collections.new(f"COL_outfit_{look_id}")
    scene.collection.children.link(col)
    objs = ld_looks.build(arm, col, look_id)
    build.sword = ld_looks.sword(col, sockets["SOCKET_weapon_r"])
    arm.animation_data.action = actions["idle"]
    scene.frame_set(R.FRAME0)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    print(f"LOOKDEV built {look_id}: {len(objs)} pieces -> {out}")
    return arm


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--look", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--render", default="")
    a = ap.parse_args(argv)
    arm = build(a.look, Path(a.out))
    if a.render:
        import kit.api as kit
        kit.render_animated(arm, a.look, ld_clips.CLIPS_KIT, a.render, name_vi=ld_looks.LOOKS[a.look],
                            kind="lookdev", frame=FRAME, pivot=PIVOT, ppm=ld_rig.PPM,
                            elevation=ELEVATION, snap=True, snap_to="head", qc_ignore=build.sword)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
