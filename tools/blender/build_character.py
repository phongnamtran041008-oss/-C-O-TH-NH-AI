#!/usr/bin/env python3
"""Build the chibi character and its clips inside Blender, then save the .blend (M8,
kế hoạch 7.1 bước 1-2).

    blender -b --factory-startup --python tools/blender/build_character.py -- --id dao_si

Why a script and not a hand-modelled file: the project's rule is that content is data or
code, so the figure is built from numbers that can be read and changed, and anyone can
rebuild the exact same .blend from scratch. The result is still an ordinary .blend - open
`art/blender/<id>.blend` in Blender and move things by hand if you want; only re-running
this script overwrites it.

The rig is deliberately plain: one armature of eight bones, and each piece of the body is a
box **parented to a bone**, not skinned to it. Rigid parenting cannot go wrong the way bad
weights can, and for a blocky chibi it looks the same. Every character that reuses this rig
can reuse these clips (plan 7.1 bước 1).

Three clips for M8 (plan 7.4): `idle`, `walk`, `slash`.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
BLEND_DIR = ROOT / "art" / "blender"

# ---------------------------------------------------------------- the figure, in metres
SKIN = (0.93, 0.80, 0.66, 1.0)
ROBE = (0.27, 0.35, 0.45, 1.0)
SASH = (0.74, 0.60, 0.23, 1.0)
HAIR = (0.11, 0.11, 0.13, 1.0)
STEEL = (0.78, 0.80, 0.84, 1.0)

BONES = {               # name: (head, tail, parent)
    "root": ((0, 0, 0), (0, 0, 0.08), None),
    "hips": ((0, 0, 0.30), (0, 0, 0.52), "root"),
    "chest": ((0, 0, 0.52), (0, 0, 0.78), "hips"),
    "head": ((0, 0, 0.78), (0, 0, 1.02), "chest"),
    "arm_l": ((0.14, 0, 0.74), (0.26, 0, 0.50), "chest"),
    "arm_r": ((-0.14, 0, 0.74), (-0.26, 0, 0.50), "chest"),
    "leg_l": ((0.07, 0, 0.30), (0.07, 0, 0.0), "hips"),
    "leg_r": ((-0.07, 0, 0.30), (-0.07, 0, 0.0), "hips"),
}
# ---------------------------------------------------------------- the eight looks
# One design per cultivation realm, read off the reference sheet the author drew
# (Downloads/file model .../nhân vật). The rule from their note: **this is only how the
# character is meant to look at that realm** - the fine robes and the wings are gear that
# has to be crafted, not something a realm hands out. So these are outfits a piece of
# equipment can point at, not a reward for cultivating.
#
# robe/sash/trim/blade are colours; the flags add parts (cape, shoulders, halo, wings).
OUTFITS = {
    "luyen_khi": {      # Luyện Khí: rough hemp, a plain wooden sword, nothing shines
        "name_vi": "Luyện Khí", "robe": (0.42, 0.35, 0.27, 1), "sash": (0.30, 0.25, 0.19, 1),
        "trim": (0.34, 0.29, 0.22, 1), "blade": (0.55, 0.42, 0.28, 1), "hair": (0.16, 0.13, 0.11, 1),
    },
    "truc_co": {        # Trúc Cơ: the first proper robe, blue over white, a steel sword
        "name_vi": "Trúc Cơ", "robe": (0.33, 0.46, 0.66, 1), "sash": (0.88, 0.89, 0.92, 1),
        "trim": (0.80, 0.84, 0.90, 1), "blade": (0.80, 0.83, 0.88, 1),
    },
    "ket_dan": {        # Kết Đan: green silk with ribbons
        "name_vi": "Kết Đan", "robe": (0.22, 0.47, 0.33, 1), "sash": (0.85, 0.80, 0.52, 1),
        "trim": (0.45, 0.72, 0.50, 1), "blade": (0.72, 0.86, 0.74, 1), "ribbon": True,
    },
    "nguyen_anh": {     # Nguyên Anh: teal and gold, shoulder guards, a sword that glows
        "name_vi": "Nguyên Anh", "robe": (0.16, 0.40, 0.46, 1), "sash": (0.85, 0.68, 0.24, 1),
        "trim": (0.92, 0.78, 0.35, 1), "blade": (0.62, 0.86, 0.95, 1), "shoulders": True,
    },
    "hoa_than": {       # Hóa Thần: a cape, and the golden ring behind the head
        "name_vi": "Hóa Thần", "robe": (0.38, 0.26, 0.52, 1), "sash": (0.35, 0.72, 0.68, 1),
        "trim": (0.95, 0.82, 0.40, 1), "blade": (0.93, 0.96, 1.00, 1),
        "shoulders": True, "cape": (0.33, 0.62, 0.60, 1), "halo": (0.98, 0.84, 0.35, 1),
    },
    "luyen_hu": {       # Luyện Hư: red and gold, wings of fire
        "name_vi": "Luyện Hư", "robe": (0.55, 0.14, 0.14, 1), "sash": (0.95, 0.72, 0.25, 1),
        "trim": (0.98, 0.60, 0.18, 1), "blade": (1.00, 0.55, 0.15, 1),
        "shoulders": True, "cape": (0.62, 0.17, 0.12, 1), "halo": (1.00, 0.63, 0.20, 1),
        "wings": (1.00, 0.52, 0.12, 1),
    },
    "hop_the": {        # Hợp Thể: dark armour, wings of ice and star-light
        "name_vi": "Hợp Thể", "robe": (0.16, 0.19, 0.33, 1), "sash": (0.70, 0.78, 0.92, 1),
        "trim": (0.62, 0.74, 0.95, 1), "blade": (0.72, 0.88, 1.00, 1),
        "shoulders": True, "cape": (0.12, 0.15, 0.30, 1), "halo": (0.55, 0.72, 1.00, 1),
        "wings": (0.70, 0.88, 1.00, 1),
    },
    "dai_thua": {       # Đại Thừa: purple and gold, the big wings, everything lit
        "name_vi": "Đại Thừa", "robe": (0.34, 0.20, 0.52, 1), "sash": (0.98, 0.82, 0.36, 1),
        "trim": (1.00, 0.88, 0.45, 1), "blade": (1.00, 0.92, 0.55, 1),
        "shoulders": True, "cape": (0.28, 0.15, 0.45, 1), "halo": (1.00, 0.90, 0.45, 1),
        "wings": (0.95, 0.85, 0.55, 1), "big_wings": True,
    },
}


def _COS(deg: float) -> float:
    return math.cos(math.radians(deg))


def _SIN(deg: float) -> float:
    return math.sin(math.radians(deg))


# A part: (bone, kind, scale, offset from the bone's head, colour, [rotation°], [subsurf])
# kinds: sphere, cylinder, cone, torus, cube.
#
# These numbers were not guessed. They were pushed around in a live Blender over the MCP
# with `look` after every change, until the figure read as a chibi from the front, the side
# and three-quarters - then written down here so the headless build makes the same thing.
def parts_for(outfit: dict) -> list[tuple]:
    """The shapes that make up the figure wearing this outfit.

    The body is identical for every realm - one rig, one silhouette, so every clip keeps
    working for every look (plan 7.1 bước 1) - and the realm only changes colours and what
    is added on top.
    """
    robe = outfit.get("robe", ROBE)
    sash = outfit.get("sash", SASH)
    trim = outfit.get("trim", sash)
    blade = outfit.get("blade", STEEL)
    hair = outfit.get("hair", HAIR)
    boot = outfit.get("boot", (0.14, 0.13, 0.15, 1.0))
    parts = [
        # ---- head: big and round, the way the reference sheet draws it
        ("head", "sphere", (0.22, 0.20, 0.21), (0, 0, 0.02), SKIN, (0, 0, 0), 1),
        ("head", "sphere", (0.235, 0.20, 0.175), (0, 0.035, 0.095), hair, (0, 0, 0), 1),
        ("head", "sphere", (0.20, 0.09, 0.07), (0, -0.14, 0.105), hair, (0, 0, 0), 1),     # fringe
        ("head", "sphere", (0.07, 0.07, 0.09), (0, 0.06, 0.22), hair, (0, 0, 0), 1),       # topknot
        ("head", "sphere", (0.030, 0.022, 0.040), (0.075, -0.175, 0.02), hair, (0, 0, 0), 1),
        ("head", "sphere", (0.030, 0.022, 0.040), (-0.075, -0.175, 0.02), hair, (0, 0, 0), 1),
        # ---- body: a short torso over a bell of a skirt, belted
        ("chest", "cylinder", (0.155, 0.12, 0.17), (0, 0, -0.05), robe, (0, 0, 0), 1),
        ("chest", "cylinder", (0.05, 0.125, 0.165), (0, -0.01, -0.05), trim, (0, 0, 0), 1),   # collar band
        ("hips", "cone", (0.27, 0.21, 0.22), (0, 0, -0.08), robe, (0, 0, 0), 1),
        ("hips", "torus", (0.165, 0.128, 0.16), (0, 0, 0.075), sash, (0, 0, 0), 0),
        # ---- arms and hands
        ("arm_l", "cylinder", (0.05, 0.05, 0.155), (0.035, 0, -0.27), robe, (0, 8, 0), 1),
        ("arm_r", "cylinder", (0.05, 0.05, 0.155), (-0.035, 0, -0.27), robe, (0, -8, 0), 1),
        ("arm_l", "sphere", (0.045, 0.045, 0.045), (0.06, -0.01, -0.41), SKIN, (0, 0, 0), 1),
        ("arm_r", "sphere", (0.045, 0.045, 0.045), (-0.06, -0.01, -0.41), SKIN, (0, 0, 0), 1),
        # ---- boots under the hem
        ("leg_l", "cube", (0.058, 0.095, 0.030), (0.005, -0.045, -0.27), boot, (0, 0, 0), 1),
        ("leg_r", "cube", (0.058, 0.095, 0.030), (-0.005, -0.045, -0.27), boot, (0, 0, 0), 1),
        # ---- the sword, hanging low at the right hand so it never crosses the face
        ("arm_r", "cylinder", (0.022, 0.022, 0.055), (-0.075, -0.030, -0.40), hair, (10, 0, -10), 0),
        ("arm_r", "cube", (0.075, 0.035, 0.018), (-0.082, -0.045, -0.445), trim, (10, 0, -10), 0),
        # the tip stops just above the ground: a blade that dips below the feet makes the
        # sprite's lowest pixel sit under the pivot, and the character then floats in game
        ("arm_r", "cone", (0.020, 0.020, 0.20), (-0.110, -0.085, -0.56), blade, (164, 0, -10), 0),
    ]
    if outfit.get("ribbon"):
        parts += [("chest", "cube", (0.035, 0.03, 0.30), (0.13, 0.07, -0.06), trim, (0, 0, 10), 0),
                  ("chest", "cube", (0.035, 0.03, 0.30), (-0.13, 0.07, -0.06), trim, (0, 0, -10), 0)]
    if outfit.get("shoulders"):
        parts += [("arm_l", "sphere", (0.085, 0.085, 0.05), (0.02, 0, -0.14), trim, (0, 0, 0), 1),
                  ("arm_r", "sphere", (0.085, 0.085, 0.05), (-0.02, 0, -0.14), trim, (0, 0, 0), 1)]
    if outfit.get("halo"):
        r = 0.27
        parts.append(("head", "torus", (r, 0.02, r), (0, 0.10, 0.06), outfit["halo"], (90, 0, 0), 0))
    if outfit.get("cape"):
        parts.append(("chest", "cube", (0.30, 0.035, 0.46), (0, 0.11, -0.06), outfit["cape"], (-6, 0, 0), 1))
    if outfit.get("wings"):
        # broad overlapping plates, not slats: thin sticks read as antlers at 32 pixels
        k = 1.25 if outfit.get("big_wings") else 1.0
        for side in (1, -1):
            for dx, dz, lift, w, h in ((0.13, 0.08, 22, 0.30, 0.17),
                                       (0.22, 0.20, 38, 0.25, 0.15),
                                       (0.28, 0.31, 54, 0.19, 0.13)):
                parts.append(("chest", "cube", (w * k, 0.035, h * k),
                              (side * dx * k, 0.12, dz * k), outfit["wings"],
                              (0, -lift * side, 0), 1))
    return parts


# clip: (frames, {bone: [(frame, (rx, ry, rz) in degrees, (dx, dy, dz) in metres), ...]})
CLIPS = {
    "idle": (4, {
        "chest": [(0, (0, 0, 0), (0, 0, 0)), (1, (0, 0, 0), (0, 0, 0.012)),
                  (2, (0, 0, 0), (0, 0, 0.018)), (3, (0, 0, 0), (0, 0, 0.012))],
        "head": [(0, (0, 0, 0), (0, 0, 0)), (2, (3, 0, 0), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
        "arm_l": [(0, (0, 0, 0), (0, 0, 0)), (2, (0, 6, 0), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
        "arm_r": [(0, (0, 0, 0), (0, 0, 0)), (2, (0, -6, 0), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
    }),
    "walk": (6, {
        "leg_l": [(0, (25, 0, 0), (0, 0, 0)), (1, (8, 0, 0), (0, 0, 0)), (2, (-18, 0, 0), (0, 0, 0)),
                  (3, (-25, 0, 0), (0, 0, 0)), (4, (-8, 0, 0), (0, 0, 0)), (5, (18, 0, 0), (0, 0, 0))],
        "leg_r": [(0, (-25, 0, 0), (0, 0, 0)), (1, (-8, 0, 0), (0, 0, 0)), (2, (18, 0, 0), (0, 0, 0)),
                  (3, (25, 0, 0), (0, 0, 0)), (4, (8, 0, 0), (0, 0, 0)), (5, (-18, 0, 0), (0, 0, 0))],
        "arm_l": [(0, (-16, 0, 0), (0, 0, 0)), (3, (16, 0, 0), (0, 0, 0)), (5, (-8, 0, 0), (0, 0, 0))],
        "arm_r": [(0, (16, 0, 0), (0, 0, 0)), (3, (-16, 0, 0), (0, 0, 0)), (5, (8, 0, 0), (0, 0, 0))],
        "hips": [(0, (0, 0, 0), (0, 0, 0)), (1, (0, 0, 0), (0, 0, 0.015)),
                 (3, (0, 0, 0), (0, 0, 0)), (4, (0, 0, 0), (0, 0, 0.015))],
        "chest": [(0, (0, 0, 4), (0, 0, 0)), (3, (0, 0, -4), (0, 0, 0)), (5, (0, 0, 2), (0, 0, 0))],
    }),
    "slash": (4, {
        "arm_r": [(0, (-35, -40, 0), (0, 0, 0)), (1, (-55, -95, 0), (0, 0, 0)),
                  (2, (30, 35, 0), (0, 0, 0)), (3, (0, 5, 0), (0, 0, 0))],
        "chest": [(0, (0, 0, -14), (0, 0, 0)), (1, (0, 0, -22), (0, 0, 0)),
                  (2, (0, 0, 18), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
        "arm_l": [(0, (0, 10, 0), (0, 0, 0)), (2, (0, -14, 0), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
        "hips": [(0, (0, 0, -6), (0, 0, 0)), (2, (0, 0, 8), (0, 0, 0)), (3, (0, 0, 0), (0, 0, 0))],
    }),
}


def clear_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name: str, rgba) -> bpy.types.Material:
    """A flat colour that both Workbench (object colour) and EEVEE can show."""
    mat = bpy.data.materials.new(name)
    try:
        mat.use_nodes = True                       # gone in Blender 6: nodes are always on
    except (AttributeError, DeprecationWarning):
        pass
    nodes = getattr(getattr(mat, "node_tree", None), "nodes", [])
    bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is not None:
        bsdf.inputs["Base Color"].default_value = rgba
        for key in ("Roughness", "Specular IOR Level", "Specular"):
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = 0.85 if key == "Roughness" else 0.1
    mat.diffuse_color = rgba                      # Workbench / viewport
    return mat


def build_rig() -> bpy.types.Object:
    arm = bpy.data.armatures.new("rig")
    rig = bpy.data.objects.new("rig", arm)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    made: dict[str, bpy.types.EditBone] = {}
    for name, (head, tail, parent) in BONES.items():
        b = arm.edit_bones.new(name)
        b.head, b.tail = Vector(head), Vector(tail)
        if parent:
            b.parent = made[parent]
        made[name] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    return rig


SHAPES = {"sphere": ("primitive_uv_sphere_add", {"segments": 20, "ring_count": 12}),
          "cylinder": ("primitive_cylinder_add", {"vertices": 16}),
          "cone": ("primitive_cone_add", {"vertices": 12, "radius1": 1.0, "radius2": 0.25}),
          "torus": ("primitive_torus_add", {"major_segments": 20, "minor_segments": 8,
                                            "major_radius": 1.0, "minor_radius": 0.13}),
          "cube": ("primitive_cube_add", {"size": 1.0})}


def build_body(rig: bpy.types.Object, outfit: dict) -> None:
    """One shape per body part, rigidly parented to a bone and left exactly where it was put.

    A bone-parented child hangs off the bone's **tail**, so parenting would normally teleport
    it. The parent inverse below is the "keep transform" that Blender's own parent operator
    computes, which lets the numbers in parts_for stay readable as offsets from the bone head.
    """
    for n, part in enumerate(parts_for(outfit)):
        bone, kind, size, offset, colour = part[:5]
        rot = part[5] if len(part) > 5 else (0, 0, 0)
        sub = part[6] if len(part) > 6 else 0
        op, kwargs = SHAPES[kind]
        getattr(bpy.ops.mesh, op)(location=(0, 0, 0), **kwargs)
        ob = bpy.context.active_object
        ob.name = f"part_{n:02d}_{bone}"
        ob.scale = Vector(size)
        ob.rotation_euler = Euler([math.radians(a) for a in rot], "XYZ")
        ob.location = Vector(BONES[bone][0]) + Vector(offset)
        ob.color = colour
        ob.data.materials.append(material(f"m_{n:02d}", colour))
        if sub:
            md = ob.modifiers.new("sub", "SUBSURF")
            md.levels = md.render_levels = int(sub)
            bpy.ops.object.shade_smooth()
        ob.parent = rig
        ob.parent_type = "BONE"
        ob.parent_bone = bone
        pb = rig.pose.bones[bone]
        tail = rig.matrix_world @ pb.matrix @ Matrix.Translation((0.0, pb.length, 0.0))
        ob.matrix_parent_inverse = tail.inverted()


def action_fcurves(action: bpy.types.Action) -> list:
    """Every curve of an action, on old and new Blender alike.

    Up to 4.3 an action simply had `.fcurves`; the slotted actions of 4.4+ keep them in
    layers -> strips -> channelbags, and `.fcurves` is gone (Blender 5.x raises
    AttributeError). This project has to build the same character on whatever Blender the
    person has, so read both shapes.
    """
    if hasattr(action, "fcurves"):
        return list(action.fcurves)
    out = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for bag in getattr(strip, "channelbags", []):
                out += list(bag.fcurves)
    return out


def make_action(rig: bpy.types.Object, name: str, frames: int, moves: dict) -> bpy.types.Action:
    action = bpy.data.actions.new(name)
    rig.animation_data_create()
    rig.animation_data.action = action
    for bone, keys in moves.items():
        pb = rig.pose.bones[bone]
        pb.rotation_mode = "XYZ"
        for frame, rot, loc in keys:
            pb.rotation_euler = Euler([math.radians(a) for a in rot], "XYZ")
            pb.location = Vector(loc)
            pb.keyframe_insert("rotation_euler", frame=frame + 1)
            pb.keyframe_insert("location", frame=frame + 1)
    for fc in action_fcurves(action):              # straight lines between poses
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    action.use_fake_user = True
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames
    return action


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--id", default="dao_si")
    ap.add_argument("--outfit", default="truc_co", choices=sorted(OUTFITS),
                    help="which cultivation realm's look to wear")
    ap.add_argument("--out", default="")
    args = ap.parse_args(argv)

    outfit = OUTFITS[args.outfit]
    clear_scene()
    rig = build_rig()
    build_body(rig, outfit)
    actions = {}
    for clip, (frames, moves) in CLIPS.items():
        rig.animation_data_clear()
        actions[clip] = make_action(rig, clip, frames, moves)
    rig.animation_data_create()
    rig.animation_data.action = actions["idle"]

    out = Path(args.out) if args.out else BLEND_DIR / f"{args.id}.blend"
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(f"built {args.id} as {outfit['name_vi']}: {len(BONES)} bones, "
          f"{len(parts_for(outfit))} parts, "
          f"clips {', '.join(f'{c} x{n}' for c, (n, _) in CLIPS.items())}")
    print(f"saved {out}")
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
