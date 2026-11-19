"""WEAPONS_A models: kiem / dao / thuong / chuy, grades 1..8, built from numbers.

Run inside Blender (headless):
  blender -b --factory-startup --python models.py -- --out <dir> [--only kiem_3,dao_5]

Convention: grip at the origin, weapon length along +Z, broad flat side faces -Y
(blade width along X), 1 unit = 1 m, character 1.0 m tall.  Ordinary Principled
materials; glowing parts have emission.  Root = empty SM_<id>, children = one mesh
per material (SM_<id>_<mat>).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Matrix, Vector

# ----------------------------------------------------------------- materials
# key: (srgb hex, metallic, roughness, emission strength)
LIB = {
    "wood":    ("8a5a30", 0.0, 0.85, 0), "wood_d": ("5a3a22", 0.0, 0.85, 0),
    "hemp":    ("e6d6a4", 0.0, 0.95, 0), "leather": ("55322a", 0.0, 0.8, 0),
    "iron":    ("b8c0cc", 0.4, 0.45, 0), "iron_d": ("6a7080", 0.4, 0.5, 0),
    "steel":   ("dce4f2", 0.4, 0.3, 0), "red": ("be2830", 0.0, 0.7, 0),
    "jade":    ("50c88c", 0.0, 0.3, 0), "jade_d": ("28906a", 0.0, 0.35, 0),
    "bronze":  ("b2763a", 0.3, 0.45, 0), "gold": ("ffd24a", 0.3, 0.3, 0),
    "gold_dk": ("5a4830", 0.3, 0.5, 0), "stone": ("7d7d8a", 0.0, 0.9, 0),
    "teal":    ("28e6d2", 0.0, 0.2, 2.0),
    "cyan":    ("5ad2ff", 0.0, 0.3, 1.5), "cyan_hi": ("d2faff", 0.0, 0.2, 3.0),
    "violet":  ("a064ff", 0.0, 0.3, 2.5),
    "flame":   ("ff5a19", 0.0, 0.3, 1.6), "flame_y": ("ffcd46", 0.0, 0.2, 3.0),
    "ice":     ("5cb4ff", 0.0, 0.25, 1.1), "ice_hi": ("f0fcff", 0.0, 0.2, 2.0),
    "ice_w":   ("e6f6ff", 0.2, 0.3, 0.0),
    "purple":  ("34248a", 0.1, 0.4, 0.12), "purple_l": ("7a46c8", 0.1, 0.4, 0.3),
    "gold_e":  ("ffc850", 0.0, 0.2, 2.6), "star": ("fff0c8", 0.0, 0.2, 5.0),
}


# optional kit properties per material
RAMP = {"wood": "wood", "wood_d": "wood", "hemp": "earth", "leather": "wood"}
PRIO = {"teal": 3.0, "star": 3.0, "gold_e": 2.0, "violet": 2.0, "flame_y": 2.0, "cyan_hi": 2.0}
GLOW = {"purple": 0, "purple_l": 0, "star": "cosmic", "gold_e": "holy", "violet": "cosmic"}


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
    if key in RAMP:
        m["kit_ramp"] = RAMP[key]
    if key in PRIO:
        m["kit_priority"] = PRIO[key]
    if key in GLOW:
        m["kit_glow"] = GLOW[key]
    _mat_cache[key] = m
    return m


# ----------------------------------------------------------------- geometry kit
class W:
    def __init__(s, wid):
        s.id = wid
        s.geo = {}  # key -> [verts, faces]

    def _push(s, key, bm, bevel):
        if bevel:
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1,
                            affect='EDGES', clamp_overlap=True)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        verts, faces = s.geo.setdefault(key, [[], []])
        base = len(verts)
        idx = {}
        for v in bm.verts:
            idx[v.index] = len(verts)
            verts.append(tuple(v.co))
        for f in bm.faces:
            faces.append([idx[v.index] for v in f.verts])
        bm.free()

    @staticmethod
    def M(loc, rot=(0, 0, 0), scale=(1, 1, 1)):
        r = Matrix.Rotation(math.radians(rot[2]), 4, 'Z') @ Matrix.Rotation(math.radians(rot[1]), 4, 'Y') \
            @ Matrix.Rotation(math.radians(rot[0]), 4, 'X')
        sc = Matrix.Diagonal((scale[0], scale[1], scale[2], 1))
        return Matrix.Translation(loc) @ r @ sc

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

    def ico(s, key, c, r, scale=(1, 1, 1)):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r, matrix=W.M(c, (0, 0, 0), scale))
        s._push(key, bm, 0)

    def poly(s, key, pts, y0, y1, bevel=0.004):
        """Extrude a simple XZ outline between y0 and y1."""
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

    def build(s, out_dir, name_vi, grade):
        root = bpy.data.objects.new("SM_" + s.id, None)
        root.empty_display_type = 'ARROWS'
        root.empty_display_size = 0.1
        root["name_vi"] = name_vi
        root["grade"] = grade
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


# ----------------------------------------------------------------- helpers
def outline(prof, tipz, tipx=0.0):
    left = [(-hw, z) for z, hw in prof]
    right = [(hw, z) for z, hw in reversed(prof)]
    return left + [(tipx, tipz)] + right


def stars(w, key, n, seed, xr, zr, y, r=0.016):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(*xr)
        z = rnd.uniform(*zr)
        w.box(key, (x, y, z), (r * 2, r * 1.5, r * 2), bevel=0)


def wings(w, key, z, n, length, wid, thick=0.02, y=0.0, rise0=-8, step=20, base_x=0.035, y_off=0.0):
    """Feather wings spreading to both sides of the grip axis (flat in XZ, face -Y)."""
    for side in (-1, 1):
        for k in range(n):
            ang = math.radians(rise0 + step * k)
            L = length * (1.0 - 0.13 * k)
            dx, dz = math.cos(ang) * side, math.sin(ang)
            px, pz = -dz * side * wid / 2 * side, 0
            # perpendicular
            nx, nz = -math.sin(ang), math.cos(ang) * side
            nx, nz = -dz, dx  # perpendicular to (dx,dz)
            bx, bz = base_x * side, z + k * 0.004
            pts = [(bx + nx * wid / 2, bz + nz * wid / 2),
                   (bx + dx * L * 0.7 + nx * wid * 0.55, bz + dz * L * 0.7 + nz * wid * 0.55),
                   (bx + dx * L, bz + dz * L),
                   (bx + dx * L * 0.7 - nx * wid * 0.45, bz + dz * L * 0.7 - nz * wid * 0.45),
                   (bx - nx * wid / 2, bz - nz * wid / 2)]
            if side < 0:
                pts = pts[::-1]
            w.poly(key, pts, y - thick / 2 + y_off, y + thick / 2 + y_off, bevel=0.003)


def tassel(w, key, c, n=3, length=0.12, r=0.007, spread=0.02):
    for i in range(n):
        off = (i - (n - 1) / 2) * spread
        w.cyl(key, (c[0] + off, c[1], c[2] - length / 2), r, r * 0.6, length, rot=(0, off * 120, 0), seg=5)
    w.sph(key, (c[0], c[1], c[2] + 0.005), r * 2.2, seg=6)


def wraps(w, key, z0, z1, r, n):
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1)
        w.cyl(key, (0, 0, z), r + 0.004, r + 0.004, 0.014, seg=8)


# ----------------------------------------------------------------- themes
# main = blade/head, hi = inlay/core, guard = guard colour, trim = second metal,
# grip, cord, gem
TH = {
    1: dict(main="wood", hi=None, guard="wood_d", trim="hemp", grip="hemp", cord="hemp", gem=None),
    2: dict(main="iron", hi=None, guard="iron_d", trim="iron_d", grip="leather", cord="red", gem=None),
    3: dict(main="jade", hi="jade_d", guard="bronze", trim="bronze", grip="leather", cord="jade", gem=None),
    4: dict(main="steel", hi="teal", guard="gold", trim="gold", grip="leather", cord="red", gem="teal"),
    5: dict(main="cyan", hi="cyan_hi", guard="gold", trim="gold", grip="leather", cord="violet", gem="violet"),
    6: dict(main="flame", hi="flame_y", guard="gold_dk", trim="gold_dk", grip="leather", cord="flame", gem="flame_y"),
    7: dict(main="ice", hi="ice_hi", guard="ice_w", trim="gold", grip="leather", cord="cyan", gem="cyan"),
    8: dict(main="purple", hi="gold_e", guard="purple_l", trim="gold", grip="leather", cord="violet", gem="star"),
}

NAMES = {1: "Mộc", 2: "Thiết", 3: "Bích Ngọc", 4: "Kim Lam", 5: "Linh Quang", 6: "Hỏa Diệm",
         7: "Băng Dực", 8: "Tinh Không"}
TYPE_VI = {"kiem": "Kiếm", "dao": "Đao", "thuong": "Thương", "chuy": "Chùy"}


# ----------------------------------------------------------------- KIEM (sword, ~0.75 m)
SWORD_PROF = {
    1: ([(0.115, 0.050), (0.62, 0.056), (0.70, 0.044)], 0.75),
    2: ([(0.115, 0.050), (0.30, 0.056), (0.62, 0.058)], 0.76),
    3: ([(0.115, 0.040), (0.30, 0.062), (0.52, 0.068), (0.66, 0.048)], 0.77),
    4: ([(0.115, 0.058), (0.50, 0.072), (0.66, 0.066)], 0.78),
    5: ([(0.115, 0.050), (0.28, 0.060), (0.32, 0.084), (0.46, 0.070), (0.50, 0.092), (0.64, 0.074),
         (0.69, 0.088)], 0.80),
    6: ([(0.115, 0.052), (0.24, 0.056), (0.28, 0.090), (0.38, 0.064), (0.43, 0.100), (0.53, 0.072),
         (0.58, 0.104), (0.68, 0.070)], 0.81),
    7: ([(0.115, 0.054), (0.45, 0.074), (0.62, 0.070), (0.70, 0.050)], 0.80),
    8: ([(0.115, 0.046), (0.30, 0.078), (0.58, 0.076), (0.70, 0.054)], 0.82),
}


def kiem(w, g):
    T = TH[g]
    tb = 0.030
    wd = {1: 0.03, 2: 0.03, 3: 0.03, 4: 0.032, 5: 0.032, 6: 0.034, 7: 0.032, 8: 0.034}[g]
    # grip
    w.cyl(T["grip"], (0, 0, 0.0), 0.027, 0.027, 0.17, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", -0.07, 0.07, 0.027, 4)
    # pommel
    pz = -0.105
    if g == 1:
        w.sph("wood_d", (0, 0, pz), 0.04, seg=7)
    elif g == 2:
        w.sph("iron_d", (0, 0, pz), 0.038)
        tassel(w, "red", (0, 0, pz - 0.03), length=0.13)
    elif g == 3:
        w.sph("bronze", (0, 0, pz), 0.04)
        w.sph("jade", (0, -0.03, pz), 0.017, seg=6)
        tassel(w, "jade", (0, 0, pz - 0.03), length=0.14)
    elif g == 4:
        w.sph("gold", (0, 0, pz), 0.044)
        w.sph("teal", (0, -0.035, pz), 0.032, seg=6)
        tassel(w, "red", (0, 0, pz - 0.04), n=3, length=0.16)
    elif g == 5:
        w.sph("gold", (0, 0, pz), 0.045)
        w.ico("violet", (0, -0.03, pz), 0.022)
        tassel(w, "violet", (0, 0, pz - 0.04), n=3, length=0.14)
    elif g == 6:
        w.cyl("gold_dk", (0, 0, pz), 0.05, 0.025, 0.07, seg=6)
        w.ico("flame_y", (0, -0.03, pz), 0.02)
        tassel(w, "flame", (0, 0, pz - 0.04), n=3, length=0.16)
    elif g == 7:
        w.sph("gold", (0, 0, pz), 0.04)
        w.ico("cyan", (0, -0.03, pz), 0.02)
        tassel(w, "cyan", (0, 0, pz - 0.04), n=3, length=0.16)
    else:
        w.sph("gold", (0, 0, pz), 0.05)
        w.sph("star", (0, -0.035, pz), 0.022, seg=6)
        tassel(w, "violet", (0, 0, pz - 0.05), n=3, length=0.18)
    # guard
    gz = 0.10
    gy = 0.05
    if g == 1:
        w.box("wood_d", (0, 0, gz), (0.20, gy, 0.034))
    elif g == 2:
        w.box("iron_d", (0, 0, gz), (0.26, gy, 0.04))
        for sx in (-1, 1):
            w.box("iron_d", (sx * 0.125, 0, gz - 0.02), (0.035, gy, 0.07))
    elif g == 3:
        w.box("bronze", (0, 0, gz), (0.24, gy, 0.036))
        for sx in (-1, 1):
            w.box("bronze", (sx * 0.12, 0, gz + 0.025), (0.035, gy, 0.07), rot=(0, sx * 18, 0))
            w.sph("jade", (sx * 0.125, -0.02, gz + 0.06), 0.017, seg=6)
    elif g == 4:
        w.box("gold", (0, 0, gz), (0.40, gy, 0.05))
        for sx in (-1, 1):
            w.poly("gold", [(sx * 0.16, gz - 0.025), (sx * 0.22, gz + 0.09), (sx * 0.19, gz + 0.095),
                            (sx * 0.11, gz + 0.02)][::sx], -gy / 2, gy / 2, 0.003)
        w.cyl("gold", (0, 0, gz + 0.0), 0.06, 0.06, 0.06, rot=(90, 0, 0), seg=8)
        w.sph("teal", (0, -0.04, gz), 0.045, seg=6)
    elif g == 5:
        wings(w, "gold", gz, 3, 0.21, 0.07, y=0.0, rise0=-10, step=24)
        w.cyl("gold", (0, 0, gz), 0.042, 0.042, 0.06, rot=(90, 0, 0), seg=8)
        w.ico("violet", (0, -0.035, gz), 0.026)
    elif g == 6:
        w.box("gold_dk", (0, 0, gz), (0.28, gy, 0.045))
        for sx in (-1, 1):
            w.cyl("gold_dk", (sx * 0.15, 0, gz + 0.02), 0.03, 0.0, 0.14, rot=(0, sx * 55, 0), seg=5)
            w.cyl("gold_dk", (sx * 0.1, 0, gz - 0.045), 0.022, 0.0, 0.08, rot=(0, sx * 150, 0), seg=5)
        w.ico("flame_y", (0, -0.034, gz), 0.03)
    elif g == 7:
        wings(w, "ice_w", gz + 0.005, 3, 0.17, 0.06, rise0=-8, step=24)
        w.box("gold", (0, 0, gz - 0.005), (0.09, gy, 0.045))
        w.ico("cyan", (0, -0.034, gz), 0.026)
    else:
        w.box("gold", (0, 0, gz), (0.30, gy, 0.04))
        for sx in (-1, 1):
            w.poly("purple_l", [(sx * 0.13, gz - 0.03), (sx * 0.22, gz + 0.04), (sx * 0.20, gz + 0.12),
                                (sx * 0.12, gz + 0.065), (sx * 0.08, gz + 0.02)][::sx], -gy / 2, gy / 2, 0.003)
            w.poly("gold", [(sx * 0.2, gz + 0.045), (sx * 0.215, gz + 0.13), (sx * 0.185, gz + 0.085)][::sx],
                   -gy / 3, gy / 3, 0.002)
        w.sph("star", (0, -0.034, gz), 0.03, seg=6)
    # blade
    prof, tipz = SWORD_PROF[g]
    pts = outline(prof, tipz)
    w.poly(T["main"], pts, -tb / 2, tb / 2, bevel=0.010)
    if g == 8:  # violet halo rim behind the blade
        big = [(z, hw + 0.016) for z, hw in prof]
        w.poly("violet", outline(big, tipz + 0.035), tb / 2 - 0.004, tb / 2 + 0.004, 0)
    # inlay / core
    if T["hi"] and g >= 3:
        c0, c1 = 0.16, tipz - 0.12
        hw = {4: 0.014, 8: 0.016}.get(g, 0.011)
        if g == 3:
            w.poly(T["hi"], [(-hw, c0), (-hw, c1), (0, c1 + 0.04), (hw, c1), (hw, c0)], -tb / 2 - 0.004, -tb / 2 + 0.006, 0)
        else:
            w.poly(T["hi"], [(-hw, c0), (-hw, c1), (0, c1 + 0.05), (hw, c1), (hw, c0)], -tb / 2 - 0.005, -tb / 2 + 0.006, 0)
    if g == 4:  # gold trim along the base of the blade
        w.box("gold", (0, -tb / 2, 0.14), (0.15, 0.014, 0.05), bevel=0.002)
    if g == 8:
        stars(w, "star", 6, 8, (-0.04, 0.04), (0.22, 0.7), -tb / 2 - 0.009, 0.016)
    if g == 7:  # crystal frost shards on the ridge
        for z, sx in ((0.3, 1), (0.45, -1), (0.58, 1)):
            w.cyl("ice_hi", (sx * 0.075, -tb / 2, z), 0.018, 0.0, 0.08, rot=(0, -sx * 25, 0), seg=4)
    if g == 6:
        for z in (0.30, 0.46):
            w.ico("flame_y", (0, -tb / 2 - 0.003, z), 0.014, (1, 0.5, 1.8))


# ----------------------------------------------------------------- DAO (curved sabre, ~0.8 m)
def sabre_outline(curve, ew0, ew1, bw, z0, z1, tip_fwd, n=14, teeth=0, wave=0.0, tooth_depth=0.02):
    left, right = [], []
    for i in range(n + 1):
        s = i / n
        z = z0 + (z1 - z0) * s
        x = curve * s * s
        ew = ew0 + (ew1 - ew0) * s ** 1.3
        if wave:
            ew += wave * math.sin(s * math.pi * 5) * s
        left.append((x - ew, z))
        b = bw
        if teeth and 0.2 < s < 0.92 and i % 2 == 1:
            b += tooth_depth
        right.append((x + b, z))
    tip = (curve + 0.012, z1 + tip_fwd)
    return left + [tip] + right[::-1]


DAO_P = {  # curve, ew0, ew1, bw, teeth, wave
    1: (0.085, 0.034, 0.060, 0.018, 0, 0.0),
    2: (0.090, 0.034, 0.066, 0.016, 0, 0.0),
    3: (0.100, 0.032, 0.078, 0.018, 0, 0.0),
    4: (0.100, 0.034, 0.074, 0.020, 1, 0.0),
    5: (0.105, 0.034, 0.080, 0.018, 0, 0.0),
    6: (0.105, 0.036, 0.082, 0.020, 0, 0.012),
    7: (0.110, 0.034, 0.080, 0.018, 0, 0.0),
    8: (0.115, 0.034, 0.086, 0.020, 0, 0.0),
}


def dao(w, g):
    T = TH[g]
    tb = 0.030
    # handle (slightly longer than sword, two handed look)
    w.cyl(T["grip"], (0, 0, 0.0), 0.027, 0.03, 0.19, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", -0.08, 0.08, 0.028, 4)
    pz = -0.115
    pk = {1: ("wood_d", None), 2: ("iron_d", "red"), 3: ("bronze", "jade"), 4: ("gold", "red"),
          5: ("gold", "violet"), 6: ("gold_dk", "flame"), 7: ("gold", "cyan"), 8: ("gold", "violet")}[g]
    w.cyl(pk[0], (0, 0, pz), 0.04, 0.034, 0.04, seg=8)
    if pk[1]:
        tassel(w, pk[1], (0, 0, pz - 0.02), n=3, length=0.15)
    # guard (disc / tsuba)
    gz = 0.105
    gy = 0.04
    if g == 1:
        w.cyl("wood_d", (0, 0, gz), 0.065, 0.065, gy, rot=(90, 0, 0), seg=8)
    elif g == 2:
        w.cyl("iron_d", (0, 0, gz), 0.075, 0.075, gy, rot=(90, 0, 0), seg=10)
    elif g == 3:
        w.cyl("bronze", (0, 0, gz), 0.08, 0.08, gy, rot=(90, 0, 0), seg=10)
        w.cyl("jade", (0, -0.022, gz), 0.035, 0.035, 0.012, rot=(90, 0, 0), seg=8)
    elif g == 4:
        w.cyl("gold", (0, 0, gz), 0.11, 0.11, gy, rot=(90, 0, 0), seg=6)
        w.sph("teal", (0, -0.035, gz), 0.045, seg=6)
    elif g == 5:
        w.cyl("gold", (0, 0, gz), 0.07, 0.07, gy, rot=(90, 0, 0), seg=8)
        wings(w, "gold", gz, 3, 0.18, 0.065, rise0=-5, step=24, base_x=0.05, y_off=0.0)
        w.ico("violet", (0, -0.03, gz), 0.028)
    elif g == 6:
        w.cyl("gold_dk", (0, 0, gz), 0.085, 0.085, gy, rot=(90, 0, 0), seg=6)
        for k in range(6):
            a = k * 60
            w.cyl("gold_dk", (math.cos(math.radians(a)) * 0.09, 0, gz + math.sin(math.radians(a)) * 0.09), 0.02, 0,
                  0.05, rot=(0, 90 - a, 0), seg=4)
        w.ico("flame_y", (0, -0.03, gz), 0.028)
    elif g == 7:
        wings(w, "ice_w", gz, 3, 0.16, 0.06, rise0=-5, step=24)
        w.cyl("gold", (0, 0, gz), 0.05, 0.05, gy, rot=(90, 0, 0), seg=8)
        w.ico("cyan", (0, -0.03, gz), 0.026)
    else:
        w.cyl("gold", (0, 0, gz), 0.09, 0.09, gy, rot=(90, 0, 0), seg=10)
        w.cyl("purple_l", (0, -0.015, gz), 0.065, 0.065, 0.02, rot=(90, 0, 0), seg=10)
        w.sph("star", (0, -0.034, gz), 0.032, seg=6)
    curve, ew0, ew1, bw, teeth, wave = DAO_P[g]
    z0, z1 = 0.12, 0.76
    pts = sabre_outline(curve, ew0, ew1, bw, z0, z1, 0.06, teeth=teeth, wave=wave)
    w.poly(T["main"], pts, -tb / 2, tb / 2, bevel=0.009)
    if g == 8:
        rim = sabre_outline(curve - 0.004, ew0 + 0.016, ew1 + 0.016, bw + 0.016, z0 - 0.01, z1 + 0.01, 0.075)
        w.poly("violet", rim, tb / 2 - 0.004, tb / 2 + 0.004, 0)
    # spine band / inlay following the curve
    if T["hi"]:
        n = 10
        inner = []
        outer = []
        for i in range(n + 1):
            s = 0.1 + 0.62 * i / n
            z = z0 + (z1 - z0) * s
            x = curve * s * s
            inner.append((x - 0.004, z))
            outer.append((x + 0.014, z))
        w.poly(T["hi"], inner + outer[::-1], -tb / 2 - 0.005, -tb / 2 + 0.006, 0)
    if g == 4:
        w.box("gold", (0.004, -tb / 2, 0.14), (0.11, 0.012, 0.03), bevel=0.002)
        for z in (0.30, 0.45, 0.6):
            s = (z - z0) / (z1 - z0)
            w.sph("gold", (curve * s * s + 0.012, -tb / 2 - 0.004, z), 0.009, seg=5)
    if g == 8:
        stars(w, "star", 6, 18, (0.0, 0.12), (0.27, 0.72), -tb / 2 - 0.009, 0.016)
    if g == 7:
        for z, sx in ((0.3, 1), (0.5, 1), (0.64, 1)):
            s = (z - z0) / (z1 - z0)
            w.cyl("ice_hi", (curve * s * s + 0.03, -tb / 2, z), 0.016, 0.0, 0.07, rot=(0, -20, 0), seg=4)


# ----------------------------------------------------------------- THUONG (spear, ~1.5 m)
def shaft(w, key, z0, z1, r):
    w.cyl(key, (0, 0, (z0 + z1) / 2), r, r, z1 - z0, seg=8)


def leaf(w, key, z0, z1, hw, thick=0.026, widest=0.4, bevel=0.007):
    zm = z0 + (z1 - z0) * widest
    pts = outline([(z0, hw * 0.35 * 1.8), (zm, hw * 1.8), (z0 + (z1 - z0) * 0.78, hw * 0.55 * 1.8)], z1)
    w.poly(key, pts, -thick / 2, thick / 2, bevel)


def thuong(w, g):
    HP = lambda key, pts, y0, y1, bevel=0.004: w.poly(key, [(x * 1.8, z) for x, z in pts], y0, y1, bevel)
    T = TH[g]
    sk = {1: "wood_d", 2: "wood_d", 3: "wood_d", 4: "iron_d", 5: "gold_dk", 6: "gold_dk", 7: "ice_w",
          8: "purple"}[g]
    shaft(w, sk, -0.25, 1.12, 0.05)
    # hand grip wraps at the origin
    w.cyl(T["grip"] if g > 1 else "hemp", (0, 0, 0), 0.03, 0.03, 0.2, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", -0.08, 0.08, 0.03, 4)
    # butt cap
    butt = {1: "wood_d", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold",
            8: "gold"}[g]
    w.cyl(butt, (0, 0, -0.25), 0.04, 0.025, 0.06, seg=8)
    if g in (4, 5, 7, 8):
        w.sph(butt, (0, 0, -0.29), 0.035, seg=6)
    base = 1.08  # head base
    ty = 0.026
    if g == 1:  # sharpened wood tip, lashed
        leaf(w, "wood", 1.1, 1.62, 0.075, widest=0.3, thick=0.05, bevel=0.01)
        w.cyl("hemp", (0, 0, 1.07), 0.06, 0.06, 0.05, seg=8)
        w.cyl("hemp", (0, 0, 1.13), 0.07, 0.07, 0.03, seg=8)
    elif g == 2:
        w.cyl("iron_d", (0, 0, base + 0.03), 0.04, 0.032, 0.09, seg=8)
        leaf(w, "iron", base + 0.05, 1.62, 0.09, widest=0.35, thick=0.034)
        tassel(w, "red", (0, 0, base + 0.04), n=5, length=0.16, spread=0.03)
    elif g == 3:
        w.cyl("bronze", (0, 0, base + 0.03), 0.042, 0.034, 0.1, seg=8)
        leaf(w, "jade", base + 0.06, 1.64, 0.095, widest=0.35, thick=0.034)
        for sx in (-1, 1):  # side jade leaves
            HP("jade", [(sx * 0.03, base + 0.07), (sx * 0.115, base + 0.13), (sx * 0.075, base + 0.2),
                            (sx * 0.03, base + 0.14)][::sx], -ty / 2, ty / 2, 0.004)
        HP("jade_d", [(-0.01, base + 0.14), (-0.01, 1.5), (0, 1.54), (0.01, 1.5), (0.01, base + 0.14)],
               -ty / 2 - 0.004, -ty / 2 + 0.006, 0)
        tassel(w, "jade", (0, 0, base + 0.03), n=5, length=0.17, spread=0.03)
    elif g == 4:
        w.cyl("gold", (0, 0, base + 0.03), 0.045, 0.036, 0.1, seg=8)
        w.sph("teal", (0, -0.04, base + 0.05), 0.04, seg=6)
        leaf(w, "steel", base + 0.1, 1.63, 0.075, widest=0.3, thick=0.034)
        for sx in (-1, 1):  # side prongs, curved
            HP("steel", [(sx * 0.03, base + 0.08), (sx * 0.13, base + 0.14), (sx * 0.14, base + 0.31),
                             (sx * 0.1, base + 0.2), (sx * 0.045, base + 0.17)][::sx], -ty / 2, ty / 2, 0.004)
        HP("gold", [(-0.012, base + 0.13), (-0.012, 1.54), (0, 1.58), (0.012, 1.54), (0.012, base + 0.13)],
               -ty / 2 - 0.004, -ty / 2 + 0.006, 0)
        tassel(w, "red", (0, 0, base + 0.01), n=5, length=0.2, spread=0.035)
    elif g == 5:
        w.cyl("gold", (0, 0, base + 0.03), 0.05, 0.036, 0.1, seg=8)
        w.ico("violet", (0, -0.04, base + 0.05), 0.026)
        leaf(w, "cyan", base + 0.08, 1.66, 0.1, widest=0.28, thick=0.036)
        HP("cyan_hi", [(-0.012, base + 0.14), (-0.012, 1.52), (0, 1.58), (0.012, 1.52), (0.012, base + 0.14)],
               -0.02, -0.01, 0)
        wings(w, "gold", base + 0.07, 3, 0.26, 0.08, rise0=15, step=26, base_x=0.04)
        tassel(w, "violet", (0, 0, base + 0.01), n=5, length=0.2, spread=0.035)
    elif g == 6:
        w.cyl("gold_dk", (0, 0, base + 0.03), 0.05, 0.036, 0.1, seg=6)
        # wavy flame head
        pts = [(0.0, 1.68), (0.05, 1.54), (0.02, 1.5), (0.075, 1.4), (0.04, 1.36), (0.065, 1.24),
               (0.03, base + 0.07), (-0.03, base + 0.07), (-0.065, 1.24), (-0.04, 1.36), (-0.075, 1.4),
               (-0.02, 1.5), (-0.05, 1.54)]
        HP("flame", pts, -0.016, 0.016, 0.005)
        HP("flame_y", [(0.0, 1.46), (0.022, 1.32), (0.0, base + 0.1), (-0.022, 1.32)], -0.022, -0.012, 0)
        for sx in (-1, 1):
            HP("flame", [(sx * 0.03, base + 0.08), (sx * 0.13, base + 0.18), (sx * 0.15, base + 0.34),
                             (sx * 0.1, base + 0.24), (sx * 0.05, base + 0.2)][::sx], -0.014, 0.014, 0.004)
        w.ico("flame_y", (0, -0.04, base + 0.05), 0.024)
        tassel(w, "flame", (0, 0, base + 0.01), n=5, length=0.2, spread=0.035)
    elif g == 7:
        w.cyl("gold", (0, 0, base + 0.03), 0.045, 0.034, 0.1, seg=8)
        w.ico("cyan", (0, -0.04, base + 0.05), 0.024)
        leaf(w, "ice", base + 0.08, 1.65, 0.09, widest=0.3, thick=0.036)
        HP("ice_hi", [(-0.01, base + 0.14), (-0.01, 1.52), (0, 1.58), (0.01, 1.52), (0.01, base + 0.14)],
               -0.02, -0.01, 0)
        wings(w, "ice_w", base + 0.08, 3, 0.26, 0.08, rise0=8, step=22, base_x=0.04)
        tassel(w, "cyan", (0, 0, base + 0.01), n=5, length=0.2, spread=0.035)
    else:
        w.cyl("gold", (0, 0, base + 0.03), 0.05, 0.036, 0.1, seg=8)
        w.sph("star", (0, -0.04, base + 0.05), 0.026, seg=6)
        leaf(w, "violet", base + 0.05, 1.72, 0.115, widest=0.3, thick=0.01, bevel=0).__class__
        leaf(w, "violet", base + 0.05, 1.72, 0.12, widest=0.3, thick=0.012, bevel=0)
        leaf(w, "purple", base + 0.08, 1.68, 0.1, widest=0.3, thick=0.036)
        HP("gold_e", [(-0.012, base + 0.16), (-0.012, 1.56), (0, 1.62), (0.012, 1.56), (0.012, base + 0.16)],
               -0.02, -0.01, 0)
        for sx in (-1, 1):  # crescent side blades
            HP("purple_l", [(sx * 0.03, base + 0.07), (sx * 0.15, base + 0.12), (sx * 0.19, base + 0.30),
                                (sx * 0.12, base + 0.22), (sx * 0.05, base + 0.2)][::sx], -ty / 2, ty / 2, 0.004)
        stars(w, "star", 5, 28, (-0.05, 0.05), (1.25, 1.6), -0.026, 0.016)
        tassel(w, "violet", (0, 0, base + 0.01), n=5, length=0.22, spread=0.035)


# ----------------------------------------------------------------- CHUY (hammer / mace, ~0.9 m)
def chuy(w, g):
    T = TH[g]
    sk = {1: "wood", 2: "wood_d", 3: "bronze", 4: "iron_d", 5: "gold_dk", 6: "gold_dk", 7: "ice_w",
          8: "purple"}[g]
    shaft(w, sk, -0.22, 0.66, 0.03)
    w.cyl(T["grip"] if g > 1 else "hemp", (0, 0, 0), 0.036, 0.036, 0.2, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", -0.08, 0.08, 0.036, 4)
    butt = {1: "wood_d", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    w.sph(butt, (0, 0, -0.23), 0.045, seg=7)
    if g >= 2:
        tassel(w, T["cord"], (0, 0, -0.26), n=3, length=0.14)
    hz = 0.76  # head centre
    if g == 1:  # stone mace: lumpy stone with spikes
        w.ico("stone", (0, 0, hz), 0.16, (1.0, 1.0, 1.0))
        for a, b in ((0, 1), (90, 0), (-90, 0), (45, 1), (-45, 1), (180, 0)):
            ca = math.radians(a)
            w.cyl("stone", (math.sin(ca) * 0.16, 0, hz + math.cos(ca) * 0.16 * 0.9), 0.04, 0.0, 0.08,
                  rot=(0, a, 0), seg=5)
        w.cyl("hemp", (0, 0, hz - 0.14), 0.05, 0.05, 0.04, seg=8)
        w.cyl("hemp", (0, 0, hz - 0.18), 0.04, 0.04, 0.03, seg=8)
    elif g == 2:
        w.box("iron", (0, 0, hz), (0.38, 0.22, 0.24), bevel=0.012)
        for sx in (-1, 1):
            w.box("iron_d", (sx * 0.185, 0, hz), (0.05, 0.24, 0.26), bevel=0.01)
        w.box("iron_d", (0, 0, hz - 0.135), (0.16, 0.16, 0.05), bevel=0.006)
        tassel(w, "red", (0, 0, hz - 0.15), n=3, length=0.12)
    elif g == 3:
        w.cyl("jade", (0, 0, hz), 0.12, 0.12, 0.32, rot=(0, 90, 0), seg=10)
        for sx in (-1, 1):
            w.cyl("bronze", (sx * 0.17, 0, hz), 0.135, 0.135, 0.05, rot=(0, 90, 0), seg=10)
        w.cyl("bronze", (0, 0, hz), 0.128, 0.128, 0.04, rot=(0, 90, 0), seg=10)
        w.cyl("jade_d", (0, -0.1, hz), 0.05, 0.05, 0.03, rot=(90, 0, 0), seg=8)
        w.cyl("bronze", (0, 0, hz - 0.14), 0.05, 0.04, 0.05, seg=8)
    elif g == 4:
        w.box("steel", (0, 0, hz), (0.40, 0.23, 0.25), bevel=0.012)
        for sx in (-1, 1):
            w.box("gold", (sx * 0.14, 0, hz), (0.045, 0.245, 0.27), bevel=0.008)
            w.box("gold", (sx * 0.2, 0, hz), (0.03, 0.24, 0.27), bevel=0.006)
        w.sph("teal", (0, -0.125, hz), 0.06, seg=6)
        w.cyl("gold", (0, 0, hz - 0.15), 0.06, 0.045, 0.05, seg=8)
        w.cyl("gold", (0, 0, hz + 0.145), 0.05, 0.05, 0.03, seg=8)
    elif g == 5:
        w.cyl("gold", (0, 0, hz), 0.13, 0.13, 0.36, rot=(0, 90, 0), seg=10)
        for sx in (-1, 1):
            w.cyl("cyan", (sx * 0.185, 0, hz), 0.1, 0.1, 0.03, rot=(0, 90, 0), seg=10)
            w.cyl("gold_dk", (sx * 0.12, 0, hz), 0.14, 0.14, 0.03, rot=(0, 90, 0), seg=10)
        w.cyl("cyan_hi", (0, -0.13, hz), 0.045, 0.045, 0.02, rot=(90, 0, 0), seg=6)
        w.ico("violet", (0, -0.14, hz), 0.035)
        w.cyl("gold", (0, 0, hz - 0.15), 0.06, 0.045, 0.05, seg=8)
    elif g == 6:
        w.box("gold_dk", (0, 0, hz), (0.36, 0.22, 0.22), bevel=0.012)
        w.box("flame", (0, -0.005, hz), (0.30, 0.22, 0.17), bevel=0.01)
        w.box("flame_y", (0, -0.112, hz), (0.2, 0.01, 0.07), bevel=0.003)
        for sx in (-1, 1):
            w.box("gold_dk", (sx * 0.195, 0, hz), (0.045, 0.24, 0.26), bevel=0.008)
            for k, dz in enumerate((-0.07, 0.0, 0.07)):  # flame spikes
                w.cyl("flame", (sx * 0.27, 0, hz + dz), 0.035, 0.0, 0.1, rot=(0, sx * 90 + (k - 1) * sx * 20, 0), seg=4)
        for dx in (-0.1, 0.0, 0.1):
            w.cyl("flame", (dx, 0, hz + 0.16), 0.032, 0.0, 0.1, seg=4)
    elif g == 7:
        w.box("ice", (0, 0, hz), (0.30, 0.2, 0.22), bevel=0.012)
        for sx in (-1, 1):
            w.cyl("ice", (sx * 0.17, 0, hz), 0.11, 0.0, 0.14, rot=(0, sx * 90, 0), seg=6)
            w.box("gold", (sx * 0.145, 0, hz), (0.04, 0.215, 0.24), bevel=0.006)
        wings(w, "ice_w", hz + 0.05, 3, 0.18, 0.07, rise0=40, step=18, base_x=0.1, y_off=0.0)
        w.cyl("ice_hi", (0, -0.1, hz), 0.05, 0.05, 0.02, rot=(90, 0, 0), seg=6)
        w.ico("cyan", (0, -0.12, hz), 0.03)
    else:
        w.box("violet", (0, 0.02, hz), (0.42, 0.2, 0.34), bevel=0)
        w.box("purple", (0, 0, hz), (0.34, 0.22, 0.26), bevel=0.014)
        for sx in (-1, 1):
            w.box("gold", (sx * 0.17, 0, hz), (0.05, 0.24, 0.28), bevel=0.008)
            w.cyl("purple_l", (sx * 0.235, 0, hz), 0.1, 0.0, 0.1, rot=(0, sx * 90, 0), seg=4)
        w.box("gold_e", (0, -0.113, hz), (0.22, 0.012, 0.035), bevel=0.002)
        w.sph("star", (0, -0.125, hz), 0.045, seg=6)
        w.cyl("gold", (0, 0, hz + 0.15), 0.07, 0.0, 0.12, seg=4)
        stars(w, "star", 5, 38, (-0.12, 0.12), (hz - 0.08, hz + 0.08), -0.12, 0.016)


BUILD = {"kiem": kiem, "dao": dao, "thuong": thuong, "chuy": chuy}
ALL_IDS = ["%s_%d" % (t, g) for t in ("kiem", "dao", "thuong", "chuy") for g in range(1, 9)]


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


def make(wid):
    """Build one weapon into the current scene; returns its root empty."""
    t, g = wid.split("_")
    g = int(g)
    w = W(wid)
    BUILD[t](w, g)
    if t == "thuong":  # keep the whole spear within ~1.5 m (shaft -0.23 .. tip ~1.3)
        k = 0.78
        for key in w.geo:
            w.geo[key][0] = [(x * k, y * k, z * k) for x, y, z in w.geo[key][0]]
    root = w.build(None, NAMES[g] + " " + TYPE_VI[t], g)
    root["type"] = t
    return root


def build_one(wid, out_dir):
    clear_all()
    root = make(wid)
    path = os.path.join(out_dir, wid + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print("MODEL", wid, "tris", root["tris"], "->", path)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = "."
    only = ALL_IDS
    i = 0
    while i < len(argv):
        if argv[i] == "--out":
            out = argv[i + 1]; i += 2
        elif argv[i] == "--only":
            only = argv[i + 1].split(","); i += 2
        else:
            i += 1
    os.makedirs(out, exist_ok=True)
    for wid in only:
        build_one(wid, out)


if __name__ == "__main__":
    main()
