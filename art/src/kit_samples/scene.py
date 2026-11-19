"""Kit samples, Blender side: build every sample model by script, save the .blend, then
render and pack through the kit. Started by build.py via kit.launcher.

    sys.argv[1:]: optional "--only sword|figure|fx|tiles|prop"
"""
from __future__ import annotations

import math
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

import kit.api as kit

OUT = "client/assets/v2/_samples"
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None


def want(part):
    return ONLY is None or ONLY == part


# ------------------------------------------------------------------ helpers
def mat(name, base, metal=0.0, rough=0.6, emit=None, strength=0.0, **props):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value = (*base, 1.0)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1.0)
        p.inputs["Emission Strength"].default_value = strength
    for k, v in props.items():
        m[k] = v
    return m


def srgb(h):
    """'#rrggbb' -> linear rgb (Principled colours are linear)."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = h.lstrip("#")
    return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def new_obj(name, bm, material=None, smooth=True, coll=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    (coll or bpy.context.scene.collection).objects.link(o)
    if material:
        me.materials.append(material)
    for poly in me.polygons:
        poly.use_smooth = smooth
    return o


def sphere(name, r, loc, scale=(1, 1, 1), material=None, seg=24, rings=14, smooth=True, coll=None):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    bmesh.ops.scale(bm, vec=Vector(scale), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(loc), verts=bm.verts)
    return new_obj(name, bm, material, smooth, coll)


def cone(name, r1, r2, z0, z1, material=None, seg=24, loc=(0, 0), smooth=True, coll=None, scale=(1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=z1 - z0)
    bmesh.ops.scale(bm, vec=Vector((scale[0], scale[1], 1)), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector((loc[0], loc[1], (z0 + z1) / 2)), verts=bm.verts)
    return new_obj(name, bm, material, smooth, coll)


def box(name, size, loc, material=None, coll=None):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(loc), verts=bm.verts)
    return new_obj(name, bm, material, False, coll)


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    return c


# ------------------------------------------------------------------ sword (3 grades)
def blade(name, length, width, thick, z0, tip, material, coll, steps=6):
    """Diamond-section blade along +Z from z0, tapering into a tip of length `tip`."""
    bm = bmesh.new()
    rings = []
    body = length - tip
    for i in range(steps + 1):
        z = z0 + body * i / steps
        rings.append([bm.verts.new(v) for v in ((-width / 2, 0, z), (0, -thick / 2, z),
                                                (width / 2, 0, z), (0, thick / 2, z))])
    top = bm.verts.new((0, 0, z0 + length))
    for a, b in zip(rings, rings[1:]):
        for k in range(4):
            bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
    for k in range(4):
        bm.faces.new((rings[-1][k], rings[-1][(k + 1) % 4], top))
    bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, material, False, coll)


def build_sword(grade: int, coll):
    """Modelled along +Z, grip centred on the origin (the hand socket), facing -Y."""
    parts = []
    if grade == 1:          # crude wooden practice sword
        wood = mat("MAT_wood_blade", srgb("#8a5a34"))
        dark = mat("MAT_wood_dark", srgb("#5a3622"))
        wrap = mat("MAT_cloth_wrap", srgb("#6c5a47"))
        parts.append(blade("SM_kiem_go_blade", 0.50, 0.075, 0.03, 0.07, 0.06, wood, coll, 4))
        parts.append(box("SM_kiem_go_guard", (0.12, 0.05, 0.04), (0, 0, 0.065), dark, coll))
        parts.append(cone("SM_kiem_go_grip", 0.022, 0.022, -0.08, 0.05, wrap, 8, coll=coll))
    elif grade == 2:        # forged steel
        steel = mat("MAT_steel_blade", srgb("#a8b8c8"), metal=1.0, rough=0.3)
        iron = mat("MAT_iron_guard", srgb("#4a5768"), metal=1.0, rough=0.4)
        red = mat("MAT_red_wrap", srgb("#94302a"))
        parts.append(blade("SM_kiem_thep_blade", 0.56, 0.055, 0.014, 0.075, 0.09, steel, coll))
        parts.append(box("SM_kiem_thep_guard", (0.15, 0.045, 0.035), (0, 0, 0.065), iron, coll))
        parts.append(cone("SM_kiem_thep_grip", 0.019, 0.019, -0.08, 0.05, red, 8, coll=coll))
        parts.append(sphere("SM_kiem_thep_pommel", 0.026, (0, 0, -0.095), material=iron, seg=10, rings=6, coll=coll))
    else:                   # spirit blade: glowing cyan, gold guard with a jade stone
        glow = mat("MAT_spirit_blade", srgb("#9ae8f4"), emit=srgb("#5ae0f4"), strength=4.0)
        gold = mat("MAT_gold_guard", srgb("#e6b83a"), metal=1.0, rough=0.25)
        jade = mat("MAT_jade_stone", srgb("#4fa678"), kit_priority=2.0)
        blue = mat("MAT_blue_wrap", srgb("#3c5e9c"))
        parts.append(blade("SM_kiem_linh_blade", 0.58, 0.06, 0.016, 0.08, 0.10, glow, coll))
        g = box("SM_kiem_linh_guard", (0.17, 0.05, 0.04), (0, 0, 0.065), gold, coll)
        bm = bmesh.new()
        bm.from_mesh(g.data)
        for v in bm.verts:      # swept-up wings on the guard
            if abs(v.co.x) > 0.05:
                v.co.z += 0.03 * (abs(v.co.x) / 0.085)
        bm.to_mesh(g.data)
        bm.free()
        parts.append(g)
        parts.append(sphere("SM_kiem_linh_gem", 0.022, (0, -0.026, 0.065), material=jade, seg=10, rings=6, coll=coll))
        parts.append(cone("SM_kiem_linh_grip", 0.019, 0.019, -0.08, 0.05, blue, 8, coll=coll))
        parts.append(sphere("SM_kiem_linh_pommel", 0.03, (0, 0, -0.10), material=gold, seg=10, rings=6, coll=coll))
    root = bpy.data.objects.new(f"SM_kiem_g{grade}", None)
    coll.objects.link(root)
    for p in parts:
        p.parent = root
    return root


# ------------------------------------------------------------------ chibi figure
def build_figure(coll):
    skin = mat("MAT_skin", srgb("#e8a882"))
    hair = mat("MAT_hair", srgb("#2e2834"))
    eye = mat("MAT_eye", srgb("#120e16"), kit_priority=4.0, kit_ramp="hair")
    robe = mat("MAT_robe", srgb("#3c5e9c"))
    under = mat("MAT_robe_inner", srgb("#cfcbd3"))
    sash = mat("MAT_sash", srgb("#94302a"))
    boot = mat("MAT_boot", srgb("#46352a"))
    tie = mat("MAT_hair_tie", srgb("#c8553a"))

    # armature: root, torso, head, arms
    arm_data = bpy.data.armatures.new("ARM_figure")
    rig = bpy.data.objects.new("ARM_figure", arm_data)
    coll.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones

    def bone(name, head, tail, parent=None, roll=0.0):
        b = eb.new(name)
        b.head, b.tail, b.roll = Vector(head), Vector(tail), roll
        if parent:
            b.parent = eb[parent]
        return b

    bone("root", (0, 0, 0), (0, 0, 0.12))
    bone("torso", (0, 0, 0.40), (0, 0, 0.60), "root")
    bone("head", (0, 0, 0.60), (0, 0, 0.98), "torso")
    bone("arm.R", (-0.15, 0, 0.57), (-0.20, 0, 0.38), "torso")
    bone("arm.L", (0.15, 0, 0.57), (0.20, 0, 0.38), "torso")
    bpy.ops.object.mode_set(mode="OBJECT")

    parts = {}
    # lower robe (skirt) and boots
    parts["skirt"] = (cone("SM_robe_skirt", 0.20, 0.135, 0.06, 0.44, robe, 24, loc=(0, 0.0), scale=(1, 0.85)), "root")
    parts["boot.L"] = (sphere("SM_boot_L", 0.06, (0.07, -0.05, 0.04), (1, 1.4, 0.7), boot, 12, 8), "root")
    parts["boot.R"] = (sphere("SM_boot_R", 0.06, (-0.07, -0.05, 0.04), (1, 1.4, 0.7), boot, 12, 8), "root")
    # torso, collar, sash
    parts["torso"] = (cone("SM_robe_top", 0.145, 0.12, 0.40, 0.62, robe, 24, scale=(1, 0.8)), "torso")
    parts["collar"] = (cone("SM_robe_collar", 0.06, 0.03, 0.555, 0.625, under, 12, loc=(0, -0.085), scale=(1, 0.5)), "torso")
    parts["sash"] = (cone("SM_sash", 0.152, 0.152, 0.41, 0.46, sash, 24, scale=(1, 0.82)), "torso")
    # head, hair, bun, eyes
    parts["head"] = (sphere("SM_head", 0.19, (0, 0, 0.80), (1, 0.95, 1), skin, 24, 16), "head")
    h = sphere("SM_hair", 0.205, (0, 0.012, 0.825), (1.0, 0.98, 1.0), hair, 24, 16)
    bm = bmesh.new()
    bm.from_mesh(h.data)
    kill = [v for v in bm.verts if v.co.y < -0.06 and v.co.z < 0.86 + 0.25 * (abs(v.co.x) - 0.02)]
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(h.data)
    bm.free()
    parts["hair"] = (h, "head")
    parts["bun"] = (sphere("SM_hair_bun", 0.085, (0, 0.03, 1.035), (1, 1, 0.9), hair, 16, 10), "head")
    parts["tie"] = (cone("SM_hair_tie", 0.06, 0.06, 0.975, 1.0, tie, 16, loc=(0, 0.03)), "head")
    for side, x in (("L", 0.072), ("R", -0.072)):
        parts[f"eye.{side}"] = (sphere(f"SM_eye_{side}", 0.03, (x, -0.168, 0.79), (0.75, 0.5, 1.15), eye, 10, 8), "head")
    # arms: sleeve + hand
    for side, sx in (("L", 1), ("R", -1)):
        sl = cone(f"SM_sleeve_{side}", 0.05, 0.075, 0.40, 0.58, robe, 16, loc=(sx * 0.175, 0))
        parts[f"sleeve.{side}"] = (sl, f"arm.{side}")
        parts[f"hand.{side}"] = (sphere(f"SM_hand_{side}", 0.045, (sx * 0.20, -0.01, 0.37), (1, 1, 1), skin, 12, 8), f"arm.{side}")

    bpy.context.view_layer.update()
    for key, (o, b) in parts.items():
        o.users_collection[0].objects.unlink(o)
        coll.objects.link(o)
        mw = o.matrix_world.copy()
        o.parent = rig
        o.parent_type = "BONE"
        o.parent_bone = b
        bpy.context.view_layer.update()
        o.matrix_world = mw
    return rig


def key_pose(rig, frame, poses):
    """poses: {bone: dict(rot=(x,y,z) degrees, loc=(x,y,z))}"""
    for bname, p in poses.items():
        pb = rig.pose.bones[bname]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = [math.radians(a) for a in p.get("rot", (0, 0, 0))]
        pb.location = p.get("loc", (0, 0, 0))
        pb.keyframe_insert("rotation_euler", frame=frame)
        pb.keyframe_insert("location", frame=frame)


def new_action(rig, name):
    rig.animation_data_create()
    rig.animation_data.action = None
    act = bpy.data.actions.new(name)
    rig.animation_data.action = act
    return act


def animate_figure(rig):
    bones = ("root", "torso", "head", "arm.R", "arm.L")
    rest = {b: {} for b in bones}
    # idle: breathe (torso sinks 1 px), arms sway, head follows late
    new_action(rig, "idle")
    idle = [
        (1, {}),
        (7, {"torso": dict(loc=(0, -0.012, 0)), "arm.R": dict(rot=(4, 0, -3)), "arm.L": dict(rot=(4, 0, 3))}),
        (13, {"torso": dict(loc=(0, -0.022, 0)), "head": dict(rot=(-3, 0, 0)), "arm.R": dict(rot=(6, 0, -5)),
              "arm.L": dict(rot=(6, 0, 5))}),
        (19, {"torso": dict(loc=(0, -0.010, 0)), "head": dict(rot=(-2, 0, 0)), "arm.R": dict(rot=(3, 0, -2)),
              "arm.L": dict(rot=(3, 0, 2))}),
        (25, {}),
    ]
    for f, p in idle:
        key_pose(rig, f, {**rest, **p})
    # slash: ready -> wind-up (raise and twist back) -> hold -> strike -> follow -> recover
    new_action(rig, "slash")
    slash = [
        (1, {"arm.R": dict(rot=(-20, 0, 0))}),
        (3, {"torso": dict(rot=(0, 18, 0)), "arm.R": dict(rot=(-150, 0, -25)), "arm.L": dict(rot=(-20, 0, 15)),
             "head": dict(rot=(0, 8, 0))}),
        (5, {"torso": dict(rot=(0, 24, 0)), "arm.R": dict(rot=(-165, 0, -35)), "arm.L": dict(rot=(-25, 0, 20)),
             "head": dict(rot=(0, 10, 0))}),
        (7, {"torso": dict(rot=(0, -22, 0)), "arm.R": dict(rot=(-70, 0, 40)), "arm.L": dict(rot=(10, 0, 10)),
             "head": dict(rot=(0, -6, 0)), "root": dict(loc=(0, 0, 0))}),
        (9, {"torso": dict(rot=(0, -30, 0)), "arm.R": dict(rot=(-30, 0, 55)), "arm.L": dict(rot=(15, 0, 8)),
             "head": dict(rot=(0, -8, 0))}),
        (11, {"torso": dict(rot=(0, -8, 0)), "arm.R": dict(rot=(-15, 0, 10))}),
    ]
    for f, p in slash:
        key_pose(rig, f, {**rest, **p})


def hold_sword(rig, sword_root):
    """Parent a sword to the right hand (bone arm.R tail), pointing down and forward."""
    bpy.context.view_layer.update()
    hand = rig.matrix_world @ rig.pose.bones["arm.R"].tail
    d = Vector((-0.75, -0.45, 0.05)).normalized()
    rot = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    sword_root.matrix_world = Matrix.Translation(hand + Vector((0, -0.01, 0))) @ rot
    bpy.context.view_layer.update()
    mw = sword_root.matrix_world.copy()
    sword_root.parent = rig
    sword_root.parent_type = "BONE"
    sword_root.parent_bone = "arm.R"
    bpy.context.view_layer.update()
    sword_root.matrix_world = mw


# ------------------------------------------------------------------ slash FX
def build_slash_fx(coll):
    m = mat("MAT_fx_slash", (0, 0, 0), emit=srgb("#5ae0f4"), strength=1.8)
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    attr = nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "fade"
    nt.links.new(attr.outputs["Color"], p.inputs["Alpha"])
    stages = [  # (start deg, end deg, max width, alpha)
        (200, 250, 0.05, 0.7), (190, 300, 0.11, 1.0), (215, 340, 0.12, 1.0),
        (260, 350, 0.07, 0.65), (300, 355, 0.045, 0.6)]
    objs = []
    for k, (a0, a1, wmax, alpha) in enumerate(stages):
        bm = bmesh.new()
        col = bm.loops.layers.color.new("fade")
        n = 24
        ring = []
        for i in range(n + 1):
            t = i / n
            a = math.radians(a0 + (a1 - a0) * t)
            w = wmax * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7 + 0.004
            r_out, r_in = 0.52, 0.52 - w
            ring.append((bm.verts.new((math.cos(a) * r_out, math.sin(a) * r_out, 0)),
                         bm.verts.new((math.cos(a) * r_in, math.sin(a) * r_in, 0)), t))
        for (o1, i1, t1), (o2, i2, t2) in zip(ring, ring[1:]):
            f = bm.faces.new((o1, o2, i2, i1))
            for loop in f.loops:
                outer = loop.vert in (o1, o2)
                t = t1 if loop.vert in (o1, i1) else t2
                fade = alpha * (0.35 + 0.65 * t) * (1.0 if outer else 0.55)
                loop[col] = (fade, fade, fade, 1.0)
        o = new_obj(f"SM_fx_slash_{k}", bm, m, False, coll)
        o.rotation_euler = (math.radians(70), 0, math.radians(-15))
        o.location = (0, -0.25, 0.5)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=1)
        for f in range(1, 6):
            o.hide_render = (f != k + 1)
            o.keyframe_insert("hide_render", frame=f)
        objs.append(o)
    return objs


# ------------------------------------------------------------------ grass tiles
def build_grass_tile(seed, coll, tile_m):
    """Calm mid-green ground with a few sparse accents (like the world mock-up): small
    faceted tufts that catch the key light, one darker patch, rare flowers / pebbles."""
    rnd = random.Random(seed * 7 + 3)
    ground = mat("MAT_grass_ground", srgb("#5e9432"))
    dark = mat("MAT_grass_dark", srgb("#3a6a26"), kit_ramp="leaf")
    tuft = mat("MAT_grass_tuft", srgb("#68a038"), kit_ramp="leaf", kit_priority=2.5)
    pebble = mat("MAT_pebble", srgb("#888e98"))
    flowers = [mat("MAT_flower_y", srgb("#eed27a"), kit_priority=3.0, kit_ramp="gold"),
               mat("MAT_flower_w", srgb("#f6f4f7"), kit_priority=3.0),
               mat("MAT_flower_p", srgb("#b892e4"), kit_priority=3.0)]
    parts = [box(f"SM_grass_{seed}_ground", (tile_m, tile_m, 0.02), (0, 0, -0.01), ground, coll)]
    half = tile_m / 2

    def spot():
        return rnd.uniform(-half, half), rnd.uniform(-half, half)

    if seed % 2 == 1:
        x, y = spot()
        parts.append(cone(f"SM_grass_{seed}_patch", rnd.uniform(0.035, 0.05), 0.02, 0.0, 0.004, dark, 8,
                          loc=(x, y), smooth=False, coll=coll, scale=(1, 0.7)))
    for i in range(2 + seed % 2):   # tufts: a few small blades, lit from the upper left
        x, y = spot()
        parts.append(cone(f"SM_grass_{seed}_tuft{i}", 0.026, 0.0, 0.0, 0.03, tuft, 5,
                          loc=(x, y), smooth=False, coll=coll))
    if seed == 2:
        x, y = spot()
        parts.append(sphere(f"SM_grass_{seed}_pebble", 0.022, (x, y, 0.0), (1.3, 1, 0.6), pebble, 8, 5, False, coll))
    for i in range(seed % 3):
        x, y = spot()
        parts.append(sphere(f"SM_grass_{seed}_flower{i}", 0.015, (x, y, 0.012), (1, 1, 0.6),
                            flowers[(seed + i) % 3], 8, 5, True, coll))
    return parts


# ------------------------------------------------------------------ rock prop
def build_rock(coll):
    rnd = random.Random(7)
    stone = mat("MAT_rock", srgb("#7a7f8a"))
    moss = mat("MAT_moss", srgb("#4f8234"))
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.25)
    for v in bm.verts:
        v.co *= 1.0 + rnd.uniform(-0.12, 0.12)
    bmesh.ops.scale(bm, vec=Vector((1.25, 1.0, 0.75)), verts=bm.verts)
    zmin = min(v.co.z for v in bm.verts)
    for v in bm.verts:
        v.co.z = max(v.co.z - zmin - 0.03, 0.0)
    rock = new_obj("SM_rock", bm, stone, False, coll)
    rock.data.materials.append(moss)
    for poly in rock.data.polygons:
        if poly.normal.z > 0.72:
            poly.material_index = 1
    tufts = [cone(f"SM_rock_tuft{i}", 0.03, 0.0, 0.0, 0.07, mat("MAT_grass_tuft", srgb("#64983a")), 5,
                  loc=(x, y), smooth=False, coll=coll) for i, (x, y) in enumerate(((0.3, -0.12), (-0.28, -0.1)))]
    # hard contact shadow: no outline ring around it (kit_outline = 0), always the shadow tone
    shade = mat("MAT_rock_contact", srgb("#3a6a26"), kit_ramp="leaf", kit_outline=0, kit_shadow=2.0, kit_light=3.0)
    shadow = cone("SM_rock_contact", 0.36, 0.36, 0.0, 0.002, shade, 24, smooth=False, coll=coll, scale=(1, 0.75))
    root = bpy.data.objects.new("SM_rock_root", None)
    coll.objects.link(root)
    for o in [rock, shadow] + tufts:
        o.parent = root
    return root


# ------------------------------------------------------------------ main
def main():
    kit.clear_scene()
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 25
    c_sword, c_fig, c_fx = collection("COL_swords"), collection("COL_figure"), collection("COL_fx")
    c_tiles, c_prop = collection("COL_tiles"), collection("COL_prop")
    swords = [build_sword(g, c_sword) for g in (1, 2, 3)]
    rig = build_figure(c_fig)
    animate_figure(rig)
    held = build_sword(2, c_fig)
    held.name = "SM_kiem_thep_held"
    hold_sword(rig, held)
    fx = build_slash_fx(c_fx)
    tile_m = kit.TILE_M
    tiles = [build_grass_tile(s, c_tiles, tile_m) for s in range(4)]
    rock = build_rock(c_prop)
    kit.save_blend("art/blender/kit_samples/kit_samples.blend")

    if want("sword"):
        names = ["Kiếm Gỗ", "Kiếm Thép", "Linh Kiếm"]
        kit.render_icons("kiem_mau", [
            {"id": f"kiem_{k}", "objects": s, "name_vi": n, "grade": g}
            for k, s, n, g in zip(("go", "thep", "linh"), swords, names, (1, 2, 5))], f"{OUT}/icons")
    if want("figure"):
        clips = {"idle": kit.PLAYER_CLIPS["idle"], "slash": kit.PLAYER_CLIPS["slash"]}
        kit.render_animated(rig, "nhan_vat_mau", clips, f"{OUT}/chars", name_vi="Nhân Vật Mẫu",
                            kind="sample", exclude=held)
        kit.render_layer(held, rig, f"{OUT}/chars/nhan_vat_mau.json", f"{OUT}/weapons", "kiem_thep_mau",
                         name_vi="Kiếm Thép")
        # v1.3: the player camera (15 degrees, 96x96), face snapped to the pixel grid
        kit.render_animated(rig, "nhan_vat_mau_15", clips, f"{OUT}/chars", name_vi="Nhân Vật Mẫu (15°)",
                            kind="sample", exclude=held, frame=(96, 96), pivot=(48, 84), ppm=44,
                            elevation=15.0, snap=True, snap_to="head")
        kit.render_layer(held, rig, f"{OUT}/chars/nhan_vat_mau_15.json", f"{OUT}/weapons",
                         "kiem_thep_mau_15", name_vi="Kiếm Thép (15°)")
        # v1.4: sword baked into the sheet, left out of the feet / lowest-row checks
        kit.render_animated(rig, "nhan_vat_mau_15_kiem", {"idle": kit.PLAYER_CLIPS["idle"]}, f"{OUT}/chars",
                            name_vi="Nhân Vật Mẫu cầm kiếm", kind="sample", frame=(96, 96), pivot=(48, 84),
                            ppm=44, elevation=15.0, snap=True, qc_ignore=held)
    if want("fx"):
        kit.render_fx("chem_mau", fx, f"{OUT}/fx", frames=[1, 2, 3, 4, 5], size=64, fps=14, blend="add")
    if want("tiles"):
        kit.render_tiles("co_mau", {"grass": tiles}, f"{OUT}/tiles", tile_m=tile_m)
    if want("prop"):
        kit.render_props("da_mau", [{"name": "tang_da", "objects": rock, "solid": [4, 10, 16, 6]}],
                         f"{OUT}/props")


main()
