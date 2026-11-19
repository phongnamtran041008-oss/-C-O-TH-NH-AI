"""Shared helpers for the MONSTERS_A creatures (runs inside Blender).

Everything here is numbers -> geometry. A creature is built from simple solids (boxes,
balls, cones, extruded outlines, tubes); hard parts are parented rigidly to one bone, soft
parts (ghost bodies, serpent body, smoke) are tubes skinned to a bone chain with weights
computed from the distance to each bone. Poses are written in *armature axes* (x = right of
the picture when the creature faces the camera, y = away from the camera / behind the
creature, z = up) and converted to each bone's own frame here, so the clip tables in
creatures.py read like a choreography sheet instead of bone-roll arithmetic.
"""
from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

# ------------------------------------------------------------------ materials
_MATS: dict[str, bpy.types.Material] = {}


def material(name: str, base, di=None, emit: float = 0.0, emit_di: float | None = None,
             emit_col=None, emit_col_di=None, ramp=None, glow=None,
             metal: bool = False) -> bpy.types.Material:
    """A plain Principled material that remembers its normal and dị chủng colours.

    base / di: RGB of the normal and the variant look. emit > 0 makes the part glow with
    its own colour (or emit_col). ramp / glow: (normal, dị chủng) palette ramp names the
    kit must snap this material to (kit_ramp / kit_glow). The variant values live as custom
    properties on the material so the .blend alone can switch look (apply_variant)."""
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    di = di if di is not None else base
    emit_di = emit if emit_di is None else emit_di
    m["col_base"] = list(base)[:3]
    m["col_di"] = list(di)[:3]
    m["emit_base"] = float(emit)
    m["emit_di"] = float(emit_di)
    m["ecol_base"] = list(emit_col or base)[:3]
    m["ecol_di"] = list(emit_col_di or emit_col or di)[:3]
    if ramp:
        m["ramp_base"], m["ramp_di"] = (ramp, ramp) if isinstance(ramp, str) else ramp
    if glow:
        m["glow_base"], m["glow_di"] = (glow, glow) if isinstance(glow, str) else glow
    if metal:
        m["kit_metal"] = True
    _MATS[name] = m
    _set_mat(m, "base")
    return m


def _bsdf(m):
    return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")


def _input(node, *names):
    for n in names:
        if n in node.inputs:
            return node.inputs[n]
    return None


def _set_mat(m, variant: str):
    col = list(m[f"col_{variant}"]) + [1.0]
    emit = float(m[f"emit_{variant}"])
    ecol = list(m[f"ecol_{variant}"]) + [1.0]
    b = _bsdf(m)
    b.inputs["Base Color"].default_value = col
    ec = _input(b, "Emission Color", "Emission")
    es = _input(b, "Emission Strength")
    if ec is not None:
        ec.default_value = ecol if emit > 0 else (0, 0, 0, 1)
    if es is not None:
        es.default_value = emit
    rough = _input(b, "Roughness")
    if rough is not None:
        rough.default_value = 0.6
    m.diffuse_color = col if emit <= 0 else ecol
    if f"ramp_{variant}" in m:
        m["kit_ramp"] = m[f"ramp_{variant}"]
    if f"glow_{variant}" in m:
        m["kit_glow"] = m[f"glow_{variant}"]
    m["variant"] = variant


def apply_variant(variant: str) -> None:
    """Switch every MAT_ in the file to 'base' or 'di' (dị chủng)."""
    for m in bpy.data.materials:
        if "col_base" in m:
            _set_mat(m, variant)


def reset():
    _MATS.clear()
    ROOT_OFF["v"] = Vector((0, 0, 0))
    bpy.ops.wm.read_factory_settings(use_empty=True)


# ------------------------------------------------------------------ collections
def collection(name: str) -> bpy.types.Collection:
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


_COL = {"cur": None}


def use_collection(name: str):
    _COL["cur"] = collection(name)


def _link(obj):
    (_COL["cur"] or bpy.context.scene.collection).objects.link(obj)


# ------------------------------------------------------------------ meshes
def _finish(name, bm, mat, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new("SM_" + name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = smooth
    me.materials.append(mat)
    ob = bpy.data.objects.new("SM_" + name, me)
    ob.location = loc
    ob.rotation_euler = Euler([math.radians(a) for a in rot], "XYZ")
    _link(ob)
    return ob


def box(name, size, loc, mat, rot=(0, 0, 0), bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    ob = _finish(name, bm, mat, loc, rot)
    if bevel > 0:
        md = ob.modifiers.new("bevel", "BEVEL")
        md.width = bevel
        md.segments = 1
        md.limit_method = "NONE"
    return ob


def ball(name, radii, loc, mat, rot=(0, 0, 0), seg=16, rings=10, smooth=True):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    bmesh.ops.scale(bm, vec=Vector(radii), verts=bm.verts)
    return _finish(name, bm, mat, loc, rot, smooth)


def cone(name, r1, r2, depth, loc, mat, rot=(0, 0, 0), seg=12, smooth=False):
    """Axis along local +z, base (r1) at -depth/2, top (r2) at +depth/2."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r1, radius2=r2, depth=depth)
    return _finish(name, bm, mat, loc, rot, smooth)


def aim(name, mat, start, end, r1, r2, seg=10, smooth=False):
    """A cone from point start (radius r1) to point end (radius r2)."""
    s, e = Vector(start), Vector(end)
    d = e - s
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r1, radius2=r2, depth=d.length)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=q.to_matrix())
    bmesh.ops.translate(bm, verts=bm.verts, vec=(s + e) / 2)
    return _finish(name, bm, mat, smooth=smooth)


def prism(name, outline, thickness, mat, matrix=None):
    """Extrude a 2-D outline [(x, z), ...] (counter-clockwise, convex or not) by
    `thickness` along y, then place it with `matrix`."""
    bm = bmesh.new()
    t = thickness / 2
    front = [bm.verts.new((x, -t, z)) for x, z in outline]
    back = [bm.verts.new((x, t, z)) for x, z in outline]
    n = len(outline)
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((front[i], front[j], back[j], back[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # non-convex outlines: triangulate the two caps so they render cleanly
    caps = [f for f in bm.faces if len(f.verts) == n]
    bmesh.ops.triangulate(bm, faces=caps)
    if matrix is not None:
        bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)
    return _finish(name, bm, mat)


def tube(name, points, radii, mat, seg=14, up=(0, -1, 0), squash=None, smooth=True,
         wobble=None):
    """A closed tube through `points` with a radius per point.

    squash: optional per-point (sx, sy) scale of the ring in its own frame.
    wobble: optional f(i, angle) -> radius multiplier (wavy hems, cloud lumps)."""
    pts = [Vector(p) for p in points]
    bm = bmesh.new()
    rings = []
    upv = Vector(up)
    for i, p in enumerate(pts):
        if i == 0:
            t = pts[1] - pts[0]
        elif i == len(pts) - 1:
            t = pts[-1] - pts[-2]
        else:
            t = (pts[i + 1] - pts[i - 1])
        t.normalize()
        a = upv - t * upv.dot(t)
        if a.length < 1e-4:
            a = Vector((1, 0, 0)) - t * t.x
        a.normalize()
        b = t.cross(a)
        sx, sy = squash[i] if squash else (1.0, 1.0)
        ring = []
        for k in range(seg):
            ang = 2 * math.pi * k / seg
            r = radii[i] * (wobble(i, ang) if wobble else 1.0)
            ring.append(bm.verts.new(p + (a * math.cos(ang) * sx + b * math.sin(ang) * sy) * r))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
    c0 = bm.verts.new(pts[0] - (pts[1] - pts[0]).normalized() * radii[0] * 0.3)
    c1 = bm.verts.new(pts[-1] + (pts[-1] - pts[-2]).normalized() * radii[-1] * 0.3)
    for k in range(seg):
        k2 = (k + 1) % seg
        bm.faces.new((rings[0][k2], rings[0][k], c0))
        bm.faces.new((rings[-1][k], rings[-1][k2], c1))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _finish(name, bm, mat, smooth=smooth)


def shadow(name, rx, ry, mat, arm):
    """Flat ground shadow under a hovering creature (z just above 0), parented to the
    armature object so it stays on the ground point whatever the bones do. It keeps the
    sprite's lowest row on the pivot, so a floating body reads as floating, not sliding."""
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False, segments=16, radius=1.0)
    bmesh.ops.scale(bm, vec=Vector((rx, ry, 1.0)), verts=bm.verts)
    ob = _finish(name, bm, mat, loc=(0, 0, 0.004))
    ob.parent = arm
    return ob


def shadow_material(name):
    """Flat contact shadow (kit v1.1): one shadow tone, no outline ring."""
    m = material(name, (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    m["kit_outline"] = 0
    m["kit_shadow"] = 2.0
    m["kit_light"] = 3.0
    return m


def ground_holdout():
    """A ground plane drawn as a hole: whatever sinks below z = 0 (a sword driven into the
    earth) is cut away cleanly. Passed to the kit as `holdout`, never part of the asset."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.5)
    me = bpy.data.meshes.new("SM_ground_holdout")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("SM_ground_holdout", me)
    collection("COL_holdout").objects.link(ob)
    ob.hide_render = True
    return ob


def place(direction, origin):
    """Matrix taking local +z to `direction` and the origin to `origin`."""
    q = Vector((0, 0, 1)).rotation_difference(Vector(direction).normalized())
    return Matrix.Translation(Vector(origin)) @ q.to_matrix().to_4x4()


# ------------------------------------------------------------------ armature
def armature(name: str, bones: list[tuple]) -> bpy.types.Object:
    """bones: (name, head, tail, parent or None)."""
    data = bpy.data.armatures.new("ARM_" + name)
    arm = bpy.data.objects.new("ARM_" + name, data)
    _link(arm)
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for bname, head, tail, parent in bones:
        eb = data.edit_bones.new(bname)
        eb.head = head
        eb.tail = tail
        eb.roll = 0.0
        if parent:
            eb.parent = data.edit_bones[parent]
            eb.use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    data.display_type = "STICK"
    return arm


def attach(obj, arm, bone):
    """Rigid parenting: the part follows `bone` exactly."""
    bpy.context.view_layer.update()
    mw = obj.matrix_world.copy()
    obj.parent = arm
    obj.parent_type = "BONE"
    obj.parent_bone = bone
    bpy.context.view_layer.update()
    obj.matrix_world = mw


def _seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (a + ab * t - p).length


def skin(obj, arm, bone_names, power=4.0, top=2):
    """Deform `obj` with the armature; weights fall off with distance to each bone."""
    obj.parent = arm
    obj.matrix_parent_inverse = arm.matrix_world.inverted()
    md = obj.modifiers.new("armature", "ARMATURE")
    md.object = arm
    groups = {b: obj.vertex_groups.new(name=b) for b in bone_names}
    segs = {b: (arm.data.bones[b].head_local.copy(), arm.data.bones[b].tail_local.copy())
            for b in bone_names}
    mw = obj.matrix_world
    for v in obj.data.vertices:
        p = mw @ v.co
        ws = []
        for b, (h, t) in segs.items():
            d = _seg_dist(p, h, t)
            ws.append((1.0 / (d + 0.01) ** power, b))
        ws.sort(reverse=True)
        ws = ws[:top]
        s = sum(w for w, _ in ws)
        for w, b in ws:
            groups[b].add([v.index], w / s, "REPLACE")


# ------------------------------------------------------------------ posing
def _rest_q(arm, bone) -> Quaternion:
    return arm.data.bones[bone].matrix_local.to_3x3().to_quaternion()


ROOT_OFF = {"v": Vector((0, 0, 0))}


def set_root_offset(xyz):
    """Constant offset of the `root` bone in every pose: puts the middle of a long
    creature's footprint on the origin (= the sprite pivot) without re-modelling it."""
    ROOT_OFF["v"] = Vector(xyz)


def set_pose(arm, pose: dict):
    """pose: bone -> dict(r=(deg x, y, z) in armature axes, l=(x, y, z) armature axes,
    s=uniform or (x, y, z) in bone axes). Bones not named go back to rest."""
    for pb in arm.pose.bones:
        spec = pose.get(pb.name, {})
        rq = _rest_q(arm, pb.name)
        if "q" in spec:                     # a rotation already in armature axes
            q = Quaternion(spec["q"])
        else:
            r = spec.get("r", (0, 0, 0))
            q = Euler([math.radians(a) for a in r], "XYZ").to_quaternion()
        pb.rotation_quaternion = rq.inverted() @ q @ rq
        l = Vector(spec.get("l", (0, 0, 0)))
        if pb.name == "root":
            l = l + ROOT_OFF["v"]
        pb.location = rq.inverted() @ l
        s = spec.get("s", 1.0)
        pb.scale = (s, s, s) if isinstance(s, (int, float)) else s


def clip(arm, name: str, frames: list[dict], fps: float, loop: bool, hit: int | None = None):
    """One action per clip; frame i of the sprite clip = action frame i + 1. A looping clip
    gets its first pose again at frame n + 1 so the action's range closes the loop (the kit
    samples n frames over the range of a loop) and the curves wrap smoothly."""
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    if arm.animation_data is None:
        arm.animation_data_create()
    arm.animation_data.action = act
    keyed = list(frames) + ([frames[0]] if loop else [])
    for i, pose in enumerate(keyed):
        set_pose(arm, pose)
        f = i + 1
        for pb in arm.pose.bones:
            pb.keyframe_insert("location", frame=f, group=pb.name)
            pb.keyframe_insert("rotation_quaternion", frame=f, group=pb.name)
            pb.keyframe_insert("scale", frame=f, group=pb.name)
    act.use_frame_range = True
    act.frame_start = 1
    act.frame_end = len(keyed)
    act["fps"] = fps
    act["loop"] = loop
    act["frames"] = len(frames)
    if hit is not None:
        act["hit"] = hit
    return act


def merge(a: dict, b: dict) -> dict:
    """Combine two pose dicts (b wins per bone)."""
    out = {k: dict(v) for k, v in a.items()}
    for k, v in b.items():
        out.setdefault(k, {}).update(v)
    return out


def lerp_pose(a: dict, b: dict, t: float) -> dict:
    out = {}
    for k in set(a) | set(b):
        sa, sb = a.get(k, {}), b.get(k, {})
        d = {}
        if "q" in sa or "q" in sb:
            qa = Quaternion(sa["q"]) if "q" in sa else Euler(
                [math.radians(x) for x in sa.get("r", (0, 0, 0))], "XYZ").to_quaternion()
            qb = Quaternion(sb["q"]) if "q" in sb else Euler(
                [math.radians(x) for x in sb.get("r", (0, 0, 0))], "XYZ").to_quaternion()
            d["q"] = tuple(qa.slerp(qb, t))
        for key, zero in ((("r", (0, 0, 0)),) if "q" not in d else ()) + (("l", (0, 0, 0)),):
            va, vb = sa.get(key, zero), sb.get(key, zero)
            d[key] = tuple(x + (y - x) * t for x, y in zip(va, vb))
        s0, s1 = sa.get("s", 1.0), sb.get("s", 1.0)
        if isinstance(s0, (int, float)) and isinstance(s1, (int, float)):
            d["s"] = s0 + (s1 - s0) * t
        else:
            s0 = (s0,) * 3 if isinstance(s0, (int, float)) else s0
            s1 = (s1,) * 3 if isinstance(s1, (int, float)) else s1
            d["s"] = tuple(x + (y - x) * t for x, y in zip(s0, s1))
        out[k] = d
    return out
