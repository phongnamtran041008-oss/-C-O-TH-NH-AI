"""Mesh building blocks for the chibi cultivator (runs inside Blender).

Everything is generated from numbers: lathes (a profile turned round the Z axis), sweeps (a
ring dragged along a path) and ellipsoids. No primitive operators, no selection state, so a
build is the same every time. Shapes are made in the rig's rest space (metres, faces -Y,
+X is the character's own left, origin on the ground between the feet).

Each builder returns (verts, faces); `mesh_object` turns that into an object with a
material, smooth shading and optional solidify / subdivision.
"""
from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector

TAU = math.tau


# ---------------------------------------------------------------- materials
def material(name: str, rgb, *, rough: float = 0.8, metal: float = 0.0,
             emit=None, emit_strength: float = 0.0, **kit) -> bpy.types.Material:
    """An ordinary Principled material (the kit turns it into toon at render time).
    kit: optional kit hints stored as custom properties (ramp="gold" -> kit_ramp, glow=,
    priority=, halo=, metal=)."""
    mat = bpy.data.materials.get(name)
    if mat is not None:
        return mat
    mat = bpy.data.materials.new(name)
    try:
        mat.use_nodes = True
    except (AttributeError, DeprecationWarning):
        pass
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    rgba = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit is not None and emit_strength > 0:
        bsdf.inputs["Emission Color"].default_value = (emit[0], emit[1], emit[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    mat.diffuse_color = rgba
    if emit is not None and emit_strength > 0:     # Workbench preview: show glow bright
        mat.diffuse_color = (min(1, emit[0] * 1.1), min(1, emit[1] * 1.1), min(1, emit[2] * 1.1), 1)
    mat.metallic = metal
    mat.roughness = rough
    for k, v in kit.items():
        if v is not None:
            mat["kit_" + k] = v
    return mat


# ---------------------------------------------------------------- objects
def mesh_object(name: str, verts, faces, mat, collection, *, smooth: bool = True,
                subsurf: int = 1, solidify: float = 0.0, flat: bool = False, face_mats=None,
                lining: bool = False) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    if face_mats is not None:
        for p, m in zip(me.polygons, face_mats):
            p.material_index = m
    me.validate(clean_customdata=False)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = smooth and not flat
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    if isinstance(mat, (list, tuple)):
        for m in mat:
            me.materials.append(m)
    else:
        me.materials.append(mat)
    if solidify:
        md = ob.modifiers.new("solidify", "SOLIDIFY")
        md.thickness = solidify
        md.offset = 0.0
        md.use_even_offset = False   # even thickness explodes where cloth folds flat
        if lining:
            md.material_offset = 1
    if subsurf:
        md = ob.modifiers.new("subsurf", "SUBSURF")
        md.levels = md.render_levels = subsurf
    return ob


def merge(*parts):
    """Concatenate several (verts, faces) into one."""
    verts, faces = [], []
    for v, f in parts:
        base = len(verts)
        verts += list(v)
        faces += [tuple(i + base for i in face) for face in f]
    return verts, faces


def transform(part, matrix: Matrix):
    v, f = part
    return [matrix @ Vector(p) for p in v], f


def moved(part, offset):
    v, f = part
    o = Vector(offset)
    return [Vector(p) + o for p in v], f


# ---------------------------------------------------------------- lathe
def lathe(profile, segs: int = 16, *, gap: float = 0.0, cap_bottom=True, cap_top=True,
          phase: float = 0.0, gap_at: float = -math.pi / 2):
    """Turn a profile round Z.

    profile: list of (z, rx, ry[, dy[, dz_back]]) from bottom to top. rx/ry are the ring's
    half widths (x, y), dy shifts the ring along Y, dz_back lowers the back of the ring (a
    robe hangs longer behind). A ring of radius 0 is a pole.
    gap: an opening (radians) centred on the front (-Y): the ring is open there (open robes).
    """
    verts, faces = [], []
    rings = []
    if gap > 0:
        a0, a1 = gap_at + gap / 2, gap_at + TAU - gap / 2
        angles = [a0 + (a1 - a0) * i / segs for i in range(segs + 1)]
        closed = False
    else:
        angles = [phase - math.pi / 2 + TAU * i / segs for i in range(segs)]
        closed = True
    for entry in profile:
        z, rx, ry = entry[0], entry[1], entry[2]
        dy = entry[3] if len(entry) > 3 else 0.0
        dzb = entry[4] if len(entry) > 4 else 0.0
        if rx <= 1e-6 and ry <= 1e-6:
            verts.append(Vector((0, dy, z)))
            rings.append(("pole", len(verts) - 1))
            continue
        idx = []
        for a in angles:
            x, y = math.cos(a) * rx, math.sin(a) * ry
            back = max(0.0, math.sin(a))                 # 1 at the back (+Y), 0 at front
            verts.append(Vector((x, y + dy, z - dzb * back)))
            idx.append(len(verts) - 1)
        rings.append(("ring", idx))
    n = len(angles)
    span = n if closed else n - 1
    for (ka, ra), (kb, rb) in zip(rings, rings[1:]):
        if ka == "ring" and kb == "ring":
            for i in range(span):
                j = (i + 1) % n
                faces.append((ra[i], ra[j], rb[j], rb[i]))
        elif ka == "pole" and kb == "ring":
            for i in range(span):
                faces.append((ra, rb[(i + 1) % n], rb[i]))
        elif ka == "ring" and kb == "pole":
            for i in range(span):
                faces.append((ra[i], ra[(i + 1) % n], rb))
    if closed:
        if cap_bottom and rings[0][0] == "ring":
            faces.append(tuple(reversed(rings[0][1])))
        if cap_top and rings[-1][0] == "ring":
            faces.append(tuple(rings[-1][1]))
    return verts, faces


def ellipsoid(center, radii, segs: int = 16, rings: int = 10, shape=None):
    """A UV ellipsoid. shape(v) may reshape each vertex (v is relative to the centre)."""
    rx, ry, rz = radii
    prof = [(-rz, 0, 0)]
    for k in range(1, rings):
        t = math.pi * k / rings
        prof.append((-rz * math.cos(t), rx * math.sin(t), ry * math.sin(t)))
    prof.append((rz, 0, 0))
    v, f = lathe(prof, segs)
    c = Vector(center)
    out = []
    for p in v:
        p = Vector(p)
        if shape is not None:
            p = shape(p)
        out.append(p + c)
    return out, f


# ---------------------------------------------------------------- sweep
def _frames(points, up=None):
    """Tangent/normal/binormal along a polyline (parallel transport)."""
    pts = [Vector(p) for p in points]
    tans = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        tans.append((b - a).normalized())
    ref = Vector(up) if up is not None else Vector((0, 0, 1))
    if abs(ref.dot(tans[0])) > 0.95:
        ref = Vector((0, 1, 0)) if abs(tans[0].y) < 0.9 else Vector((1, 0, 0))
    n = (ref - tans[0] * ref.dot(tans[0])).normalized()
    out = []
    for i, t in enumerate(tans):
        if i > 0:
            n = (n - t * n.dot(t)).normalized()
        out.append((t, n, t.cross(n)))
    return pts, out


def sweep(points, radii, segs: int = 10, *, flat: float = 1.0, up=None, cap=True,
          tip=True, twist: float = 0.0):
    """A tube along a path. radii: one per point (or one for all). flat squeezes the ring
    along its normal (0.2 = a flat lock of hair / a ribbon). The last point closes to a tip
    when tip is True, otherwise both ends get a flat cap."""
    pts, frames = _frames(points, up)
    if not isinstance(radii, (list, tuple)):
        radii = [radii] * len(pts)
    verts, faces, rings = [], [], []
    last = len(pts) - 1
    for i, (p, (t, n, b)) in enumerate(zip(pts, frames)):
        r = radii[i]
        if isinstance(r, (list, tuple)):
            rw, rt = r
        else:
            rw, rt = r, r * flat
        if i == last and tip:
            verts.append(p)
            rings.append(("pole", len(verts) - 1))
            continue
        idx = []
        tw = math.radians(twist) * (i / max(last, 1))
        for k in range(segs):
            a = TAU * k / segs + tw
            verts.append(p + b * (math.cos(a) * rw) + n * (math.sin(a) * rt))
            idx.append(len(verts) - 1)
        rings.append(("ring", idx))
    for (ka, ra), (kb, rb) in zip(rings, rings[1:]):
        if kb == "pole":
            for k in range(segs):
                faces.append((ra[k], ra[(k + 1) % segs], rb))
        else:
            for k in range(segs):
                kk = (k + 1) % segs
                faces.append((ra[k], ra[kk], rb[kk], rb[k]))
    if cap:
        faces.append(tuple(reversed(rings[0][1])))
        if rings[-1][0] == "ring":
            faces.append(tuple(rings[-1][1]))
    return verts, faces


def sheet(rows, *, cols=None):
    """A grid surface from rows of points (each row the same length)."""
    verts, faces = [], []
    w = len(rows[0])
    for row in rows:
        verts += [Vector(p) for p in row]
    for r in range(len(rows) - 1):
        for c in range(w - 1):
            a = r * w + c
            faces.append((a, a + 1, a + w + 1, a + w))
    return verts, faces


def leaf(base, direction, length, width, *, side=None, thick=0.012, bend=0.0, segs=6,
         shape="leaf", tip_curl=0.0):
    """A flat feather / flame tongue / crystal: a lens shape along `direction`.

    side: the in-plane width direction; the leaf is thin across direction x side.
    shape: 'leaf' (rounded), 'flame' (wide base, wavy, sharp tip), 'shard' (diamond),
    'feather' (long, slightly widening, round tip).
    """
    d = Vector(direction).normalized()
    s = Vector(side if side is not None else (1, 0, 0))
    s = (s - d * s.dot(d)).normalized()
    nrm = d.cross(s).normalized()
    base = Vector(base)
    pts, rad = [], []
    for i in range(segs + 1):
        t = i / segs
        if shape == "flame":
            w = width * (math.sin(math.pi * min(1, t * 1.15)) ** 0.7) * (1 - t) ** 0.4
        elif shape == "shard":
            w = width * (t / 0.35 if t < 0.35 else (1 - t) / 0.65)
        elif shape == "feather":
            w = width * (0.55 + 0.45 * t) * (1 - t ** 6) ** 0.5
        elif shape == "plume":      # a broad flight feather: full blade, rounded-pointed tip
            w = width * (0.55 + 0.45 * math.sin(math.pi / 2 * min(1.0, t * 1.6))) * max(0.0, 1 - t ** 2.5) ** 0.7
        elif shape == "covert":     # a small rounded covert feather
            w = width * math.sin(math.pi * min(1.0, 0.25 + 0.75 * t)) ** 0.6
        else:
            w = width * math.sin(math.pi * t) ** 0.8
        off = s * (bend * math.sin(math.pi * t) + tip_curl * t * t)
        pts.append(base + d * (length * t) + off)
        rad.append((max(w, 0.003), thick))
    return sweep(pts, rad, segs=6 if shape != "shard" else 4, up=nrm, tip=True)
