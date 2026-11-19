"""ICONS batch: shared modelling kit (runs inside headless Blender).

Everything is built from numbers.  One `W` per icon; `W.build()` makes a root empty
SM_<id> with one mesh child per material (SM_<id>_<mat>).  Ordinary Principled materials;
glow = emission.  Objects are modelled ~0.3-0.5 m big: the icon renderer fits every icon to
26 px, so a 0.015 m feature is already about 1 px.

Convention: upright things stand on z=0 (or are centred), face -Y, +Z up, +X right.
"""
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

# ----------------------------------------------------------------- materials
# key: (srgb hex, metallic, roughness, emission strength, kit_ramp or None, kit_glow or None, prio)
LIB = {
    # paper / cloth / wood / earth (dull, low grades)
    "paper":    ("ecd9a0", 0.0, 0.95, 0, "gold", None, 0),
    "paper_d":  ("c8ac70", 0.0, 0.95, 0, "gold", None, 0),
    "paper_ice": ("d8ecff", 0.0, 0.9, 0, "steel", None, 0),
    "paper_pu": ("6a50a8", 0.0, 0.9, 0.0, "purple", None, 0),
    "straw":    ("d6b45c", 0.0, 0.95, 0, "gold", None, 0),
    "wood":     ("8a5a30", 0.0, 0.85, 0, "wood", None, 0),
    "wood_d":   ("573420", 0.0, 0.85, 0, "wood", None, 0),
    "wood_l":   ("ad7a48", 0.0, 0.85, 0, "wood", None, 0),
    "leather":  ("6c4a34", 0.0, 0.8, 0, "wood", None, 0),
    "cloth_b":  ("7a5c40", 0.0, 0.95, 0, "earth", None, 0),
    "cloth_d":  ("47392d", 0.0, 0.95, 0, "earth", None, 0),
    "cloth_g":  ("5e636f", 0.0, 0.95, 0, "stone", None, 0),
    "clay":     ("958065", 0.0, 0.95, 0, "earth", None, 0),
    "clay_d":   ("6c5a47", 0.0, 0.95, 0, "earth", None, 0),
    "stone":    ("7d7d8a", 0.0, 0.9, 0, "stone", None, 0),
    "stone_d":  ("3a3d48", 0.0, 0.9, 0, "stone", None, 0),
    "iron":     ("94a6ba", 0.45, 0.45, 0, "steel", None, 0),
    "iron_d":   ("5d6e86", 0.45, 0.5, 0, "steel", None, 0),
    "steel":    ("dce4f2", 0.5, 0.3, 0, "steel", None, 0),
    "bone":     ("cfcbd3", 0.0, 0.7, 0, "bone", None, 0),
    "bone_d":   ("9894a2", 0.0, 0.7, 0, "bone", None, 0),
    "porcelain": ("f0eef6", 0.0, 0.25, 0, "bone", None, 0),
    "blue":     ("3c5e9c", 0.0, 0.5, 0, "blue", None, 0),
    "blue_d":   ("243a6a", 0.0, 0.5, 0, "blue", None, 0),
    "blue_l":   ("6488c4", 0.0, 0.4, 0, "blue", None, 0),
    "red":      ("94302a", 0.0, 0.7, 0, "red", None, 0),
    "red_l":    ("c8553a", 0.0, 0.6, 0, "red", None, 0),
    "red_d":    ("5c1a1c", 0.0, 0.7, 0, "red", None, 0),
    "skin":     ("c9805c", 0.0, 0.7, 0, "skin", None, 0),
    # greens
    "leaf":     ("3a6a26", 0.0, 0.7, 0, "leaf", None, 0),
    "leaf_l":   ("5e9432", 0.0, 0.6, 0, "leaf", None, 0),
    "leaf_d":   ("22401c", 0.0, 0.7, 0, "leaf", None, 0),
    "jade":     ("2e7a5a", 0.0, 0.3, 0, "jade", None, 0),
    "jade_l":   ("4fa678", 0.0, 0.3, 0, "jade", None, 0),
    "jade_d":   ("1b5040", 0.0, 0.35, 0, "jade", None, 0),
    "bronze":   ("b2763a", 0.3, 0.45, 0, "wood", None, 0),
    "gold":     ("e6b83a", 0.4, 0.3, 0, "gold", None, 0),
    "gold_d":   ("b9821a", 0.4, 0.4, 0, "gold", None, 0),
    "gold_dk":  ("7a4c0e", 0.3, 0.5, 0, "gold", None, 0),
    "ink":      ("26201a", 0.0, 0.9, 0, "earth", None, 3.0),
    # glow
    "teal":     ("28e6d2", 0.0, 0.2, 2.0, None, "spirit", 3.0),
    "cyan":     ("5ad2ff", 0.0, 0.3, 0.8, None, "spirit", 2.0),
    "cyan_hi":  ("d2faff", 0.0, 0.2, 3.0, None, "spirit", 2.0),
    "violet":   ("a064ff", 0.0, 0.3, 2.5, None, "cosmic", 3.0),
    "pink":     ("ff7ac8", 0.0, 0.3, 1.6, None, "cosmic", 2.0),
    "flame":    ("ff5a19", 0.0, 0.3, 1.6, None, "flame", 2.0),
    "flame_y":  ("ffcd46", 0.0, 0.2, 3.0, None, "flame", 3.0),
    "ice":      ("5cb4ff", 0.0, 0.25, 1.1, None, "ice", 2.0),
    "ice_hi":   ("f0fcff", 0.0, 0.2, 2.0, None, "ice", 3.0),
    "ice_w":    ("e6f6ff", 0.2, 0.3, 0.0, "steel", None, 0),
    "purple":   ("5c3690", 0.1, 0.4, 0.0, "purple", None, 0),
    "purple_l": ("8456be", 0.1, 0.4, 0.0, "purple", None, 0),
    "gold_e":   ("ffc850", 0.0, 0.2, 2.6, None, "holy", 2.0),
    "star":     ("fff0c8", 0.0, 0.2, 5.0, None, "cosmic", 3.0),
    "verdant":  ("7aec9a", 0.0, 0.2, 1.8, None, "verdant", 2.0),
    "thunder":  ("b8c0ff", 0.0, 0.2, 1.1, None, "thunder", 3.0),
    "holy":     ("ffe27a", 0.0, 0.2, 2.2, None, "holy", 2.0),
}


def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


_mat_cache = {}


def mat(key):
    if key in _mat_cache and _mat_cache[key].name in bpy.data.materials:
        return _mat_cache[key]
    hx, met, rou, em, ramp, glow, prio = LIB[key]
    m = bpy.data.materials.new("MAT_" + key)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = lin(hx)
    b.inputs["Metallic"].default_value = met
    b.inputs["Roughness"].default_value = rou
    if em > 0:
        b.inputs["Emission Color"].default_value = lin(hx)
        b.inputs["Emission Strength"].default_value = em
    if ramp:
        m["kit_ramp"] = ramp
    if glow:
        m["kit_glow"] = glow
    if prio:
        m["kit_priority"] = prio
    _mat_cache[key] = m
    return m


# ----------------------------------------------------------------- geometry
class W:
    def __init__(s, wid, name_vi="", grade=1):
        s.id, s.name_vi, s.grade = wid, name_vi, grade
        s.geo = {}
        s.T = Matrix.Identity(4)
        s._stack = []
        s.pose = {}  # icon pose overrides: angle / spin / tilt / size

    # transform stack: with w.at(loc, rot, scale): ...
    def at(s, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        return _Xf(s, W.M(loc, rot, scale))

    @staticmethod
    def M(loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        r = (Matrix.Rotation(math.radians(rot[2]), 4, 'Z') @ Matrix.Rotation(math.radians(rot[1]), 4, 'Y')
             @ Matrix.Rotation(math.radians(rot[0]), 4, 'X'))
        sc = Matrix.Diagonal((scale[0], scale[1], scale[2], 1))
        return Matrix.Translation(loc) @ r @ sc

    def _push(s, key, bm, bevel=0.0):
        if bevel:
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1,
                            affect='EDGES', clamp_overlap=True)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        verts, faces = s.geo.setdefault(key, [[], []])
        idx = {}
        for v in bm.verts:
            idx[v.index] = len(verts)
            verts.append(tuple(s.T @ v.co))
        flip = s.T.determinant() < 0
        for f in bm.faces:
            ids = [idx[v.index] for v in f.verts]
            faces.append(ids[::-1] if flip else ids)
        bm.free()

    def box(s, key, c, size, rot=(0, 0, 0), bevel=0.004):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0, matrix=W.M(c, rot, size))
        s._push(key, bm, bevel)

    def cyl(s, key, c, r1, r2, h, rot=(0, 0, 0), seg=10, bevel=0.0):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2,
                              depth=h, matrix=W.M(c, rot))
        s._push(key, bm, bevel)

    def sph(s, key, c, r, scale=(1, 1, 1), seg=8, rot=(0, 0, 0)):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg // 2 + 1), radius=r,
                                  matrix=W.M(c, rot, scale))
        s._push(key, bm, 0)

    def ico(s, key, c, r, scale=(1, 1, 1), rot=(0, 0, 0), sub=1):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r, matrix=W.M(c, rot, scale))
        s._push(key, bm, 0)

    def poly(s, key, pts, y0, y1, bevel=0.003):
        """Extrude a simple XZ outline between y0 and y1 (convex or mildly concave)."""
        bm = bmesh.new()
        a = [bm.verts.new((x, y0, z)) for x, z in pts]
        b = [bm.verts.new((x, y1, z)) for x, z in pts]
        bm.faces.new(a)
        bm.faces.new(b[::-1])
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([a[i], a[j], b[j], b[i]])
        s._push(key, bm, bevel)

    def lathe(s, key, prof, c=(0, 0, 0), seg=14, bevel=0.0, rot=(0, 0, 0), scale=(1, 1, 1)):
        """Solid of revolution about Z.  prof = [(radius, z), ...] bottom to top (closed
        with flat caps on the axis when the first/last radius is > 0)."""
        bm = bmesh.new()
        rings = []
        for r, z in prof:
            ring = []
            for i in range(seg):
                a = 2 * math.pi * i / seg
                ring.append(bm.verts.new((math.cos(a) * r, math.sin(a) * r, z)))
            rings.append(ring)
        for k in range(len(rings) - 1):
            for i in range(seg):
                j = (i + 1) % seg
                if prof[k][0] == 0 and prof[k + 1][0] == 0:
                    continue
                q = [rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]]
                try:
                    if prof[k][0] == 0:
                        bm.faces.new([rings[k][0], rings[k + 1][j], rings[k + 1][i]])
                    elif prof[k + 1][0] == 0:
                        bm.faces.new([rings[k][i], rings[k][j], rings[k + 1][0]])
                    else:
                        bm.faces.new(q)
                except ValueError:
                    pass
        if prof[0][0] > 0:
            bm.faces.new(rings[0][::-1])
        if prof[-1][0] > 0:
            bm.faces.new(rings[-1])
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-5)
        bmesh.ops.transform(bm, matrix=W.M(c, rot, scale), verts=list(bm.verts))
        s._push(key, bm, bevel)

    def torus(s, key, c, R, r, rot=(0, 0, 0), seg=14, tseg=6, scale=(1, 1, 1)):
        prof = []
        for i in range(tseg):
            a = 2 * math.pi * i / tseg
            prof.append((R + r * math.cos(a), r * math.sin(a)))
        # closed profile loop: build manually
        bm = bmesh.new()
        rings = []
        for rr, z in prof:
            rings.append([bm.verts.new((math.cos(2 * math.pi * i / seg) * rr,
                                        math.sin(2 * math.pi * i / seg) * rr, z)) for i in range(seg)])
        for k in range(tseg):
            k2 = (k + 1) % tseg
            for i in range(seg):
                j = (i + 1) % seg
                bm.faces.new([rings[k][i], rings[k][j], rings[k2][j], rings[k2][i]])
        bmesh.ops.transform(bm, matrix=W.M(c, rot, scale), verts=list(bm.verts))
        s._push(key, bm, 0)

    def bar(s, key, p0, p1, r0, r1=None, seg=5):
        """Cylinder (tapered) from p0 to p1."""
        a, b = Vector(p0), Vector(p1)
        d = b - a
        L = d.length
        if L < 1e-6:
            return
        q = d.to_track_quat('Z', 'Y')
        M = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4()
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r0,
                              radius2=r0 if r1 is None else r1, depth=L, matrix=M)
        s._push(key, bm, 0)

    def path(s, key, pts, r0, r1=None, seg=5):
        n = len(pts) - 1
        for i in range(n):
            ra = r0 + (0 if r1 is None else (r1 - r0) * i / n)
            rb = r0 + (0 if r1 is None else (r1 - r0) * (i + 1) / n)
            s.bar(key, pts[i], pts[i + 1], ra, rb, seg)
            if i:
                s.sph(key, pts[i], ra, seg=5)

    def build(s):
        root = bpy.data.objects.new("SM_" + s.id, None)
        root.empty_display_type = 'ARROWS'
        root.empty_display_size = 0.1
        root["name_vi"] = s.name_vi
        root["grade"] = s.grade
        col = bpy.data.collections.new("COL_" + s.id)
        bpy.context.scene.collection.children.link(col)
        col.objects.link(root)
        tris = 0
        for key, (verts, faces) in s.geo.items():
            me = bpy.data.meshes.new("SM_%s_%s" % (s.id, key))
            me.from_pydata(verts, [], faces)
            me.update()
            me.materials.append(mat(key))
            ob = bpy.data.objects.new("SM_%s_%s" % (s.id, key), me)
            col.objects.link(ob)
            ob.parent = root
            tris += sum(len(f) - 2 for f in faces)
        root["tris"] = tris
        return root


class _Xf:
    def __init__(s, w, M):
        s.w, s.M = w, M

    def __enter__(s):
        s.w._stack.append(s.w.T)
        s.w.T = s.w.T @ s.M
        return s.w

    def __exit__(s, *a):
        s.w.T = s.w._stack.pop()


def clear_all():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)
    _mat_cache.clear()


# ----------------------------------------------------------------- shared shapes
def leaf(w, key, base, ang, length, width, thick=0.02, y=0.0, bevel=0.002):
    """Flat leaf in the XZ plane (faces -Y), growing from `base` (x,z) at `ang` degrees from +Z
    (positive = to +X)."""
    a = math.radians(ang)
    dx, dz = math.sin(a), math.cos(a)
    nx, nz = dz, -dx
    pts = []
    prof = [(0.0, 0.0), (0.22, 0.55), (0.55, 0.9), (0.85, 0.6), (1.0, 0.0), (0.85, -0.6),
            (0.55, -0.9), (0.22, -0.55)]
    # leaf outline: along the axis t (0..1), half-width h
    shape = [(0.0, 0.0), (0.18, 0.62), (0.5, 1.0), (0.8, 0.7), (1.0, 0.0), (0.8, -0.7), (0.5, -1.0),
             (0.18, -0.62)]
    for t, h in shape:
        pts.append((base[0] + dx * length * t + nx * width / 2 * h, base[1] + dz * length * t + nz * width / 2 * h))
    w.poly(key, pts, y - thick / 2, y + thick / 2, bevel=bevel)


def spiral_qi(w, key, c, R, h, turns=1.5, n=16, r=0.012, tilt=0.0, phase=0.0, taper=True, ry=None):
    """Swirling ribbon of small segments (emissive) winding round a centre."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = phase + 2 * math.pi * turns * t
        rr = R * (0.55 + 0.45 * math.sin(math.pi * t)) if taper else R
        x, y, z = math.cos(a) * rr, math.sin(a) * rr * (ry if ry else 0.6), -h / 2 + h * t
        pts.append((c[0] + x, c[1] + y, c[2] + z))
    w.path(key, pts, r, r * 0.6, seg=5)


def stars_at(w, key, pts, r=0.014):
    for p in pts:
        w.box(key, p, (r * 2, r * 1.4, r * 2), bevel=0)


def sparkle(w, key, c, r=0.03):
    """Four-point glint facing -Y."""
    w.box(key, c, (r * 2, 0.012, r * 0.55), bevel=0)
    w.box(key, c, (r * 0.55, 0.012, r * 2), bevel=0)


def swirl2d(w, key, c, r0, r1, a0, a1, n=14, r=0.014, y=0.06, squash=1.0):
    """Flat spiral ribbon in the XZ plane at depth y (behind a book): radius r0 -> r1."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(a0 + (a1 - a0) * t)
        rr = r0 + (r1 - r0) * t
        pts.append((c[0] + math.cos(a) * rr, y, c[2] + math.sin(a) * rr * squash))
    w.path(key, pts, r, r * 0.55, seg=5)
