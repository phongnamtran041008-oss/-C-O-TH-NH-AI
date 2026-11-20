"""WEAPONS_C geometry kit (runs inside Blender; bmesh only, headless-safe).

`W` collects geometry per (pose, material key). `build()` turns it into a root empty SM_<id>
(custom props name_vi, grade, type, pose_default, poses) with one child mesh per material and
pose: SM_<id>_<mat> (every pose) or SM_<id>_<pose>_<mat> (custom prop "pose" = <pose>).

Pose meshes are how a flexible or thrown weapon changes shape between animation frames: the
whip is coiled / swung back / lashed out, the hidden darts are a fan in the fist or a spread
in flight. Only one pose is visible at a time (the weapon-layer hook switches them; the icon
shows `pose_default`).

Convention: grip at the origin, length along +Z, flat side faces -Y, 1 unit = 1 m.
"""
import math

import bmesh
import bpy
from mathutils import Matrix, Vector

# ----------------------------------------------------------------- materials
# key: (srgb hex, metallic, roughness, emission strength)
LIB = {
    "wood": ("8a5a30", 0.0, 0.85, 0), "wood_d": ("5a3a22", 0.0, 0.85, 0),
    "wood_l": ("b07a44", 0.0, 0.85, 0),
    "hemp": ("e6d6a4", 0.0, 0.95, 0), "rope": ("a8885a", 0.0, 0.95, 0),
    "leather": ("55322a", 0.0, 0.8, 0), "leather_l": ("7a4a30", 0.0, 0.8, 0),
    "stone": ("7d7d8a", 0.0, 0.9, 0), "stone_l": ("a4a4ae", 0.0, 0.9, 0), "bone": ("d8cfb0", 0.0, 0.9, 0),
    "iron": ("b8c0cc", 0.4, 0.45, 0), "iron_d": ("6a7080", 0.4, 0.5, 0),
    "steel": ("dce4f2", 0.4, 0.3, 0), "steel_l": ("f4f8ff", 0.4, 0.25, 0),
    "red": ("be2830", 0.0, 0.7, 0), "lacquer": ("8a2a1c", 0.0, 0.5, 0), "lacq_d": ("4a1610", 0.0, 0.6, 0),
    "black": ("2a201c", 0.2, 0.6, 0),
    "jade": ("50c88c", 0.0, 0.3, 0), "jade_d": ("28906a", 0.0, 0.35, 0), "jade_l": ("9ae8c0", 0.0, 0.3, 0),
    "bronze": ("b2763a", 0.3, 0.45, 0), "gold": ("ffd24a", 0.3, 0.3, 0),
    "gold_dk": ("5a4830", 0.3, 0.5, 0),
    "string": ("f2ead0", 0.0, 0.6, 0),
    "teal": ("28e6d2", 0.0, 0.2, 2.0),
    "cyan": ("5ad2ff", 0.0, 0.3, 1.5), "cyan_hi": ("d2faff", 0.0, 0.2, 3.0),
    "violet": ("a064ff", 0.0, 0.3, 2.5),
    "flame": ("ff5a19", 0.0, 0.3, 1.6), "flame_y": ("ffcd46", 0.0, 0.2, 3.0), "ember": ("ff3a10", 0.0, 0.3, 2.2),
    "ice": ("5cb4ff", 0.0, 0.25, 1.1), "ice_hi": ("f0fcff", 0.0, 0.2, 2.0),
    "ice_w": ("e6f6ff", 0.2, 0.3, 0.0),
    "purple": ("34248a", 0.1, 0.4, 0.12), "purple_l": ("7a46c8", 0.1, 0.4, 0.3),
    "gold_e": ("ffc850", 0.0, 0.2, 2.6), "star": ("fff0c8", 0.0, 0.2, 5.0),
}
RAMP = {"wood": "wood", "wood_d": "wood", "wood_l": "wood", "hemp": "earth", "rope": "earth",
        "leather": "wood", "leather_l": "wood", "stone": "stone", "stone_l": "stone", "bone": "bone",
        "lacquer": "red", "lacq_d": "red", "string": "paper", "black": "stone"}
PRIO = {"teal": 3.0, "star": 3.0, "gold_e": 2.0, "violet": 2.0, "flame_y": 2.0, "cyan_hi": 2.0,
        "string": 1.5}
GLOW = {"purple": 0, "purple_l": 0, "star": "cosmic", "gold_e": "holy", "violet": "cosmic"}
NO_METAL = {"string": 0}


def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


_mat_cache = {}


def mat(key):
    if key in _mat_cache and _mat_cache[key].name in bpy.data.materials:
        return _mat_cache[key]
    hx, met, rou, em = LIB[key]
    m = bpy.data.materials.new("MAT_" + key)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = lin(hx)
    b.inputs["Metallic"].default_value = met
    b.inputs["Roughness"].default_value = rou
    if em > 0:
        b.inputs["Emission Color"].default_value = lin(hx)
        b.inputs["Emission Strength"].default_value = em
    m.diffuse_color = lin(hx)
    if key in RAMP:
        m["kit_ramp"] = RAMP[key]
    if key in PRIO:
        m["kit_priority"] = PRIO[key]
    if key in GLOW:
        m["kit_glow"] = GLOW[key]
    if key in NO_METAL:
        m["kit_metal"] = NO_METAL[key]
    _mat_cache[key] = m
    return m


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


V = Vector


def rot_m(rot):
    return (Matrix.Rotation(math.radians(rot[2]), 4, 'Z') @ Matrix.Rotation(math.radians(rot[1]), 4, 'Y')
            @ Matrix.Rotation(math.radians(rot[0]), 4, 'X'))


def M(loc, rot=(0, 0, 0), scale=(1, 1, 1)):
    return Matrix.Translation(loc) @ rot_m(rot) @ Matrix.Diagonal((scale[0], scale[1], scale[2], 1))


# ----------------------------------------------------------------- the builder
class W:
    def __init__(s, wid):
        s.id = wid
        s.geo = {}            # (pose, key) -> [verts, faces]
        s.pose = None         # current pose (None = shared by all poses)
        s.xf = Matrix.Identity(4)   # transform applied to everything pushed (sub-assemblies)

    # -- bookkeeping
    def _push(s, key, bm, bevel=0.0):
        if bevel:
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1,
                            affect='EDGES', clamp_overlap=True)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        verts, faces = s.geo.setdefault((s.pose, key), [[], []])
        idx = {}
        for v in bm.verts:
            idx[v.index] = len(verts)
            verts.append(tuple(s.xf @ v.co))
        for f in bm.faces:
            faces.append([idx[v.index] for v in f.verts])
        bm.free()

    # -- primitives
    def box(s, key, c, size, rot=(0, 0, 0), bevel=0.004):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0, matrix=M(c, rot, size))
        s._push(key, bm, bevel)

    def cyl(s, key, c, r1, r2, h, rot=(0, 0, 0), seg=10, bevel=0.0):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2,
                              depth=h, matrix=M(c, rot))
        s._push(key, bm, bevel)

    def seg(s, key, p0, p1, r0, r1, n=8):
        """Cylinder (cone) between two points."""
        p0, p1 = V(p0), V(p1)
        d = p1 - p0
        if d.length < 1e-6:
            return
        q = V((0, 0, 1)).rotation_difference(d.normalized())
        m = Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=n, radius1=r0, radius2=r1,
                              depth=d.length, matrix=m)
        s._push(key, bm, 0)

    def sph(s, key, c, r, scale=(1, 1, 1), seg=8, rot=(0, 0, 0)):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(4, seg // 2 + 1), radius=r,
                                  matrix=M(c, rot, scale))
        s._push(key, bm, 0)

    def ico(s, key, c, r, scale=(1, 1, 1), rot=(0, 0, 0)):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r, matrix=M(c, rot, scale))
        s._push(key, bm, 0)

    def poly(s, key, pts, y0, y1, bevel=0.004):
        """Extrude an XZ outline between y0 and y1 (convex or star-shaped around its first point
        works best; any simple polygon is accepted)."""
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

    def strip(s, key, inner, outer, y0, y1):
        """A band between two matching XZ polylines (quads only, no ngons): edges, crescents."""
        bm = bmesh.new()
        n = len(inner)
        A = [[bm.verts.new((x, y, z)) for x, z in inner] for y in (y0, y1)]
        B = [[bm.verts.new((x, y, z)) for x, z in outer] for y in (y0, y1)]
        for i in range(n - 1):
            bm.faces.new([A[0][i], B[0][i], B[0][i + 1], A[0][i + 1]])
            bm.faces.new([A[1][i + 1], B[1][i + 1], B[1][i], A[1][i]])
            bm.faces.new([A[0][i + 1], A[1][i + 1], A[1][i], A[0][i]])
            bm.faces.new([B[0][i], B[1][i], B[1][i + 1], B[0][i + 1]])
        bm.faces.new([A[0][0], A[1][0], B[1][0], B[0][0]])
        bm.faces.new([B[0][-1], B[1][-1], A[1][-1], A[0][-1]])
        s._push(key, bm, 0)

    def ring(s, key, c, rin, rout, y0, y1, n=24, a0=0.0, a1=360.0):
        """Annulus in the XZ plane around c=(x, z); rout may be a function of the angle (deg).
        a0..a1 < 360 gives an arc band."""
        full = abs(a1 - a0) >= 359.9
        k = n if full else n + 1
        angs = [a0 + (a1 - a0) * i / n for i in range(k)]
        ro = rout if callable(rout) else (lambda a, r=rout: r)
        ri = rin if callable(rin) else (lambda a, r=rin: r)
        inner = [(c[0] + ri(a) * math.cos(math.radians(a)), c[1] + ri(a) * math.sin(math.radians(a))) for a in angs]
        outer = [(c[0] + ro(a) * math.cos(math.radians(a)), c[1] + ro(a) * math.sin(math.radians(a))) for a in angs]
        if full:
            inner.append(inner[0])
            outer.append(outer[0])
        s.strip(key, inner, outer, y0, y1)

    def tor(s, key, c, R, r, normal=(0, 1, 0), seg=20, tseg=6):
        bm = bmesh.new()
        n = V(normal).normalized()
        q = V((0, 0, 1)).rotation_difference(n)
        m = Matrix.Translation(c) @ q.to_matrix().to_4x4()
        rings = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            ring = []
            for j in range(tseg):
                b = 2 * math.pi * j / tseg
                ring.append(bm.verts.new(m @ V(((R + r * math.cos(b)) * math.cos(a),
                                                 (R + r * math.cos(b)) * math.sin(a), r * math.sin(b)))))
            rings.append(ring)
        for i in range(seg):
            for j in range(tseg):
                bm.faces.new((rings[i][j], rings[(i + 1) % seg][j], rings[(i + 1) % seg][(j + 1) % tseg],
                              rings[i][(j + 1) % tseg]))
        s._push(key, bm, 0)

    # -- output
    def build(s, name_vi, grade, wtype, default_pose=None):
        root = bpy.data.objects.new("SM_" + s.id, None)
        root.empty_display_type = 'ARROWS'
        root.empty_display_size = 0.1
        root["name_vi"] = name_vi
        root["grade"] = grade
        root["type"] = wtype
        poses = sorted({p for p, _ in s.geo if p})
        root["poses"] = ",".join(poses)
        root["pose_default"] = default_pose or ""
        col = bpy.data.collections.new("COL_" + s.id)
        bpy.context.scene.collection.children.link(col)
        col.objects.link(root)
        tris = 0
        for (pose, key), (verts, faces) in sorted(s.geo.items(), key=lambda kv: (kv[0][0] or "", kv[0][1])):
            name = "SM_%s_%s" % (s.id, key) if pose is None else "SM_%s_%s_%s" % (s.id, pose, key)
            me = bpy.data.meshes.new(name)
            me.from_pydata(verts, [], faces)
            me.update()
            me.materials.append(mat(key))
            ob = bpy.data.objects.new(name, me)
            if pose:
                ob["pose"] = pose
                ob.hide_render = pose != default_pose
            col.objects.link(ob)
            ob.parent = root
            t = sum(len(f) - 2 for f in faces)
            if pose in (None, default_pose):
                tris += t
        root["tris"] = tris
        return root


def visible_children(root, pose=None):
    """The meshes of `root` shown in `pose` (default: its pose_default)."""
    pose = pose or root.get("pose_default") or None
    return [o for o in root.children if o.get("pose") in (None, pose)]


# ----------------------------------------------------------------- shared ornaments
def wraps(w, key, z0, z1, r, n):
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1)
        w.cyl(key, (0, 0, z), r + 0.004, r + 0.004, 0.014, seg=8)


def tassel(w, key, c, n=3, length=0.12, r=0.007, spread=0.02):
    for i in range(n):
        off = (i - (n - 1) / 2) * spread
        w.cyl(key, (c[0] + off, c[1], c[2] - length / 2), r, r * 0.6, length, rot=(0, off * 120, 0), seg=5)
    w.sph(key, (c[0], c[1], c[2] + 0.005), r * 2.2, seg=6)


def stars(w, key, pts, y, r=0.016):
    for x, z in pts:
        w.box(key, (x, y, z), (r * 2, r * 1.5, r * 2), bevel=0)


def wings(w, key, z, n, length, wid, thick=0.02, y=0.0, rise0=-8, step=20, base_x=0.035, sides=(-1, 1)):
    """Feather wings spreading to both sides of the axis (flat in XZ, face -Y)."""
    for side in sides:
        for k in range(n):
            ang = math.radians(rise0 + step * k)
            L = length * (1.0 - 0.13 * k)
            dx, dz = math.cos(ang) * side, math.sin(ang)
            nx, nz = -dz, dx
            bx, bz = base_x * side, z + k * 0.004
            pts = [(bx + nx * wid / 2, bz + nz * wid / 2),
                   (bx + dx * L * 0.7 + nx * wid * 0.55, bz + dz * L * 0.7 + nz * wid * 0.55),
                   (bx + dx * L, bz + dz * L),
                   (bx + dx * L * 0.7 - nx * wid * 0.45, bz + dz * L * 0.7 - nz * wid * 0.45),
                   (bx - nx * wid / 2, bz - nz * wid / 2)]
            if side < 0:
                pts = pts[::-1]
            w.poly(key, pts, y - thick / 2, y + thick / 2, bevel=0.003)


def leaf_pts(base, ang, length, width, widest=0.4, back=0.0):
    """Leaf / blade outline in XZ: from `base` along angle `ang` (deg from +Z toward +X)."""
    a = math.radians(ang)
    d = (math.sin(a), math.cos(a))
    p = (d[1], -d[0])
    bx, bz = base

    def at(t, off):
        return (bx + d[0] * length * t + p[0] * off, bz + d[1] * length * t + p[1] * off)
    return [at(-back, 0), at(0.02, width * 0.35), at(widest, width), at(0.8, width * 0.45), at(1.0, 0),
            at(0.8, -width * 0.45), at(widest, -width), at(0.02, -width * 0.35)]
