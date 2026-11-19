"""Blender entry for one village NPC on the v2 body: build, save, render through the kit.

    (via kit.launcher) npc_main.py --npc <id> --out art/blender/chars/npc_<id>.blend [--render DIR] [--clips idle]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "v2"))
sys.path.insert(0, str(HERE))

import v2_rig  # noqa: E402  (bone table first)
import bpy  # noqa: E402
import rig as R  # noqa: E402
import clips  # noqa: E402
import v2_clips  # noqa: E402,F401
import npc_looks  # noqa: E402
import npc_clips  # noqa: E402


def build(npc_id: str, out: Path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    col_rig = bpy.data.collections.new("COL_dao_si")
    scene.collection.children.link(col_rig)
    arm = R.build_armature(col_rig)
    R.add_sockets(arm, col_rig)
    npc_clips.install(npc_id)
    actions = clips.build_actions(arm)
    col = bpy.data.collections.new(f"COL_npc_{npc_id}")
    scene.collection.children.link(col)
    objs = npc_looks.build(arm, col, npc_id)
    arm.animation_data.action = actions["idle"]
    scene.frame_set(R.FRAME0)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    print(f"NPC built {npc_id}: {len(objs)} pieces -> {out}")
    return arm


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--npc", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--render", default="")
    ap.add_argument("--clips", default="")
    a = ap.parse_args(argv)
    arm = build(a.npc, Path(a.out))
    if a.render:
        import kit.api as kit
        spec = dict(npc_clips.KIT_CLIPS)
        if a.clips:
            spec = {c: spec[c] for c in a.clips.split(",")}
        kit.render_animated(arm, a.npc, spec, a.render, name_vi=npc_looks.NPCS[a.npc], kind="npc",
                            frame=v2_rig.FRAME, pivot=v2_rig.PIVOT, ppm=v2_rig.PPM,
                            elevation=v2_rig.ELEVATION, snap=True, snap_to="head")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
