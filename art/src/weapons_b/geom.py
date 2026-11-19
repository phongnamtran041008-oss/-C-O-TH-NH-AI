"""Geometry helpers for the WEAPONS_B models (bmesh only, no bpy.ops, headless-safe).

A Builder collects faces per material name, then `finish()` turns them into ONE mesh object
named SM_<id> with one slot per material (MAT_<id>_<name>).  Everything is numbers and code.
"""
import math
import bpy
import bmesh
from mathutils import Matrix, Vector


def srgb(hexstr):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def mat_spec(hexstr, metal=0.0, rough=0.7, em=None, es=0.0, ramp=None, glow=None, prio=None):
    return {"base": hexstr, "metal": metal, "rough": rough, "em": em, "es": es, "ramp": ramp, "glow": glow, "prio": prio}


def make_material(name, spec):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    col = srgb(spec["base"]) + (1.0,)
    bsdf.inputs["Base Color"].default_value = col
    bsdf.inputs["Metallic"].default_value = spec["metal"]
    bsdf.inputs["Roughness"].default_value = spec["rough"]
    if spec["es"] > 0:
        bsdf.inputs["Emission Color"].default_value = srgb(spec["em"] or spec["base"]) + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = spec["es"]
        m["kit_halo"] = 1
    m.diffuse_color = col
    if spec.get("ramp"):
        m["kit_ramp"] = spec["ramp"]
    if spec.get("glow") is not None:
        m["kit_glow"] = spec["glow"]
    if spec.get("prio"):
        m["kit_priority"] = spec["prio"]
    return m


def _frame(p0, p1):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    ln = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized()) if ln > 1e-9 else Matrix.Identity(3).to_quaternion()
    return (Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()), ln


class Builder:
    def __init__(self, wid, palette):
        self.wid = wid
        self.palette = palette
        self.bms = {}

    def _bm(self, mat):
        if mat not in self.bms:
            self.bms[mat] = bmesh.new()
        return self.bms[mat]

    @staticmethod
    def _smooth(ret, smooth):
        for f in {f for v in ret["verts"] for f in v.link_faces}:
            f.smooth = smooth

    def cyl(self, p0, p1, r0, r1, mat, seg=10, smooth=True, cap=True):
        bm = self._bm(mat)
        M, ln = _frame(p0, p1)
        ret = bmesh.ops.create_cone(bm, cap_ends=cap, cap_tris=False, segments=seg,
                                    radius1=r0, radius2=r1, depth=ln, matrix=M)
        self._smooth(ret, smooth)

    def sph(self, c, r, mat, seg=10, rings=6, rot=None, smooth=True):
        bm = self._bm(mat)
        s = (r, r, r) if not isinstance(r, (tuple, list)) else tuple(r)
        M = Matrix.Translation(c)
        if rot is not None:
            M = M @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[2], 4, 'Z')
        M = M @ Matrix.Diagonal((s[0], s[1], s[2], 1.0))
        ret = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0, matrix=M)
        self._smooth(ret, smooth)

    def box(self, c, size, mat, rot=(0, 0, 0)):
        bm = self._bm(mat)
        M = Matrix.Translation(c) @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[2], 4, 'Z')
        M = M @ Matrix.Diagonal((size[0], size[1], size[2], 1.0))
        ret = bmesh.ops.create_cube(bm, size=1.0, matrix=M)
        self._smooth(ret, False)

    def tor(self, c, R, r, normal, mat, seg=20, tseg=6, smooth=True):
        bm = self._bm(mat)
        n = Vector(normal).normalized()
        q = Vector((0, 0, 1)).rotation_difference(n)
        M = Matrix.Translation(c) @ q.to_matrix().to_4x4()
        rings = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            ring = []
            for j in range(tseg):
                b = 2 * math.pi * j / tseg
                x = (R + r * math.cos(b)) * math.cos(a)
                y = (R + r * math.cos(b)) * math.sin(a)
                z = r * math.sin(b)
                ring.append(bm.verts.new(M @ Vector((x, y, z))))
            rings.append(ring)
        for i in range(seg):
            for j in range(tseg):
                f = bm.faces.new((rings[i][j], rings[(i + 1) % seg][j],
                                  rings[(i + 1) % seg][(j + 1) % tseg], rings[i][(j + 1) % tseg]))
                f.smooth = smooth

    def prism(self, pts, thick, mat, n=(0, 1, 0)):
        """Flat plate: polygon `pts` (3D, roughly coplanar) extruded +-thick/2 along n."""
        bm = self._bm(mat)
        n = Vector(n).normalized() * (thick / 2)
        top = [bm.verts.new(Vector(p) + n) for p in pts]
        bot = [bm.verts.new(Vector(p) - n) for p in pts]
        k = len(pts)
        bm.faces.new(top)
        bm.faces.new(list(reversed(bot)))
        for i in range(k):
            j = (i + 1) % k
            bm.faces.new((top[i], bot[i], bot[j], top[j]))

    def leaf(self, base, ang, length, width, mat, thick=0.012, y=0.0):
        """Leaf / feather in the XZ plane. ang = degrees from +Z toward +X."""
        a = math.radians(ang)
        d = Vector((math.sin(a), 0, math.cos(a)))
        p = Vector((d.z, 0, -d.x))
        b = Vector(base)
        pts = [b, b + d * length * 0.45 + p * width, b + d * length, b + d * length * 0.45 - p * width]
        pts = [Vector((q.x, y, q.z)) for q in pts]
        self.prism(pts, thick, mat)

    def finish(self):
        wid = self.wid
        mesh = bpy.data.meshes.new("SM_" + wid + "_mesh")
        big = bmesh.new()
        order = list(self.bms.keys())
        for idx, name in enumerate(order):
            bm = self.bms[name]
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            tmp = bpy.data.meshes.new("tmp")
            bm.to_mesh(tmp)
            bm.free()
            before = len(big.faces)
            big.from_mesh(tmp)
            bpy.data.meshes.remove(tmp)
            big.faces.ensure_lookup_table()
            for f in big.faces[before:]:
                f.material_index = idx
        big.to_mesh(mesh)
        big.free()
        obj = bpy.data.objects.new("SM_" + wid, mesh)
        for name in order:
            obj.data.materials.append(make_material("MAT_%s_%s" % (wid, name), self.palette[name]))
        return obj
