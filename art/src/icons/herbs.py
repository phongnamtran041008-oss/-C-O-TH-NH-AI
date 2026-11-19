"""linh_thao atlas: 12 spirit herbs, low grades dull and green, high grades glowing.

Flat-ish plants are modelled in the XZ plane and the whole plant is laid back 30 degrees so
the 35 degree camera sees it nearly face-on, the way the reference sheet draws them.
"""
import math

from lib import W, leaf, sparkle, stars_at

# id, name_vi, grade
HERBS = [
    ("co_linh", "Cỏ Linh", 1),
    ("nam_do", "Nấm Đỏ", 2),
    ("nhan_sam", "Nhân Sâm", 3),
    ("qua_do", "Quả Chu Hồng", 3),
    ("chuong_xanh", "Hoa Chuông Lam", 4),
    ("sen_ngoc", "Sen Ngọc", 4),
    ("day_loi", "Dây Lôi Đằng", 5),
    ("hoa_diem", "Hỏa Diệm Hoa", 6),
    ("lan_nguyet", "Nguyệt Lan", 7),
    ("sen_bang", "Băng Liên", 7),
    ("qua_tinh", "Quả Tinh Tú", 8),
    ("la_long", "Long Lân Diệp", 8),
]
IDS = [h[0] for h in HERBS]
LAY = (-30, 0, 0)


def petals(w, key, c, n, length, width, a0=0.0, spread=360.0, thick=0.02, y=0.0):
    for k in range(n):
        a = a0 + (k * spread / n if spread >= 360 else (k - (n - 1) / 2) * spread / max(1, n - 1))
        leaf(w, key, c, a, length, width, thick=thick, y=y)


def stem(w, key, pts, r0=0.016, r1=None):
    w.path(key, pts, r0, r1, seg=5)


def co_linh(w):
    for ang, ln, key in ((-42, 0.30, "leaf"), (-24, 0.38, "leaf_l"), (-8, 0.43, "leaf"), (8, 0.40, "leaf_l"),
                         (24, 0.36, "leaf"), (42, 0.28, "leaf_l"), (0, 0.32, "leaf_d")):
        leaf(w, key, (0, -0.19), ang, ln, 0.085, thick=0.022, y=0.0 if key != "leaf_d" else 0.02)
    w.sph("leaf_d", (0, 0, -0.19), 0.04, scale=(1.6, 0.8, 0.8), seg=6)


def nam_do(w):
    def mush(cx, base, rc, hs, cap="red_l", dots=True):
        w.cyl("bone", (cx, 0, base + hs / 2), rc * 0.38, rc * 0.5, hs, seg=8)
        w.lathe(cap, [(0.0, base + hs - 0.01), (rc, base + hs - 0.01), (rc * 1.0, base + hs + rc * 0.2),
                      (rc * 0.8, base + hs + rc * 0.62), (rc * 0.4, base + hs + rc * 0.88), (0.0, base + hs + rc * 0.95)],
              c=(cx, 0, 0), seg=10)
        w.cyl("bone_d", (cx, 0, base + hs - 0.012), rc * 0.95, rc * 0.95, 0.012, seg=10)
        if dots:
            for dx, dz in ((-0.4, 0.45), (0.15, 0.7), (0.5, 0.35), (-0.05, 0.25)):
                w.sph("bone", (cx + dx * rc, -rc * 0.7 * math.sqrt(max(0.0, 1 - (dx * dx)) + 0.2) * 0.85,
                               base + hs + rc * dz * 0.95), rc * 0.17, seg=5)
    mush(-0.02, -0.19, 0.14, 0.17)
    mush(0.17, -0.19, 0.075, 0.09)
    w.box("leaf_d", (0, 0.02, -0.2), (0.4, 0.05, 0.03), bevel=0.004)


def nhan_sam(w):
    root = "wood_l"
    w.path(root, [(0, 0, 0.1), (0.0, 0, 0.0), (-0.01, 0, -0.1)], 0.095, 0.06, seg=8)
    w.sph(root, (0, 0, 0.11), 0.1, seg=8, scale=(1, 1, 0.9))
    for k, (x1, z1, x2, z2) in enumerate(((-0.11, -0.15, -0.17, -0.2), (0.11, -0.16, 0.15, -0.22),
                                          (0.0, -0.18, 0.02, -0.25))):
        w.path(root, [(0.0 if k == 2 else x1 * 0.4, 0, -0.07), (x1, 0, z1), (x2, 0, z2)], 0.05, 0.02, seg=5)
    for dz in (0.05, 0.1, 0.15):  # rings
        w.torus("clay", (0, 0, dz), 0.098, 0.009, seg=9, tseg=4)
    for z in (-0.02, 0.01):
        w.box("clay", (0.05, -0.05, z), (0.04, 0.012, 0.008), bevel=0)
    stem(w, "leaf", [(0, 0, 0.17), (0, 0, 0.25)], 0.016)
    for ang, key in ((-60, "leaf_l"), (0, "leaf"), (60, "leaf_l")):
        leaf(w, key, (0, 0.25), ang, 0.19, 0.09, thick=0.02)
    w.sph("red_l", (0.0, -0.01, 0.22), 0.022, seg=5)


def qua_do(w):
    bpts = [(-0.19, 0, -0.17), (-0.08, 0, -0.08), (0.0, 0, -0.02), (0.1, 0, 0.07), (0.19, 0, 0.17)]
    w.path("wood_d", bpts, 0.022, 0.012, seg=5)
    for (x, z), ang in (((-0.1, -0.09), -75), ((0.02, -0.01), 60), ((0.1, 0.07), -55), ((-0.02, -0.04), 85)):
        leaf(w, "leaf_l" if ang > 0 else "leaf", (x, z), ang, 0.17, 0.075, thick=0.02, y=0.01)
    for x, z in ((-0.07, -0.13), (0.01, -0.1), (0.07, 0.0), (0.15, 0.08), (0.12, -0.0)):
        w.sph("red_l", (x, -0.03, z), 0.045, seg=7)
        w.sph("red", (x + 0.012, -0.065, z + 0.012), 0.012, seg=4)
        w.box("bone", (x - 0.013, -0.075, z + 0.016), (0.014, 0.008, 0.014), bevel=0)


def chuong_xanh(w):
    stem(w, "leaf", [(0, 0, -0.2), (0.0, 0, -0.05), (0, 0, 0.02)], 0.016)
    leaf(w, "leaf_l", (0, -0.17), -62, 0.17, 0.07, thick=0.02)
    leaf(w, "leaf", (0, -0.14), 62, 0.17, 0.07, thick=0.02)
    petals(w, "blue_l", (0, 0.06), 5, 0.19, 0.09, a0=0, thick=0.025)
    w.sph("gold", (0, -0.02, 0.06), 0.035, seg=6)
    w.sph("gold_d", (0, -0.035, 0.06), 0.012, seg=4)


def sen_ngoc(w):
    for sx in (-1, 1):  # lily pad leaves
        leaf(w, "leaf", (sx * 0.02, -0.15), sx * 76, 0.2, 0.10, thick=0.02, y=0.02)
    petals(w, "porcelain", (0, -0.1), 5, 0.27, 0.1, a0=0, spread=110, thick=0.02, y=0.0)
    petals(w, "red_l", (0, -0.1), 3, 0.23, 0.095, a0=0, spread=70, thick=0.02, y=-0.012)
    w.sph("gold", (0, -0.03, 0.0), 0.034, scale=(1.4, 0.6, 1), seg=6)
    for dx in (-0.025, 0.025):
        w.sph("gold_d", (dx, -0.04, 0.02), 0.014, seg=4)


def day_loi(w):
    w.path("leaf", [(-0.12, 0, -0.2), (-0.1, 0, -0.08), (-0.14, 0, 0.04), (-0.08, 0, 0.14), (-0.1, 0, 0.22)], 0.03, 0.018)
    leaf(w, "leaf_l", (-0.11, -0.12), 70, 0.2, 0.09, thick=0.02)
    leaf(w, "leaf", (-0.13, 0.02), -70, 0.18, 0.09, thick=0.02)
    # lightning bolt in glowing thunder colour (a zig-zag of fat segments, not a blob)
    w.path("thunder", [(0.11, 0, 0.25), (0.04, 0, 0.1), (0.15, 0, 0.06), (0.05, 0, -0.1), (0.13, 0, -0.2)],
           0.028, 0.02, seg=5)
    w.path("thunder", [(0.22, 0, 0.0), (0.18, 0, -0.06), (0.25, 0, -0.1)], 0.016, 0.01, seg=4)
    for (x, z) in ((-0.02, 0.22), (0.25, 0.16)):
        sparkle(w, "thunder", (x, -0.03, z), 0.03)
    w.sph("thunder", (-0.1, -0.03, 0.22), 0.026, seg=6)


def hoa_diem(w):
    leaf(w, "leaf", (0, -0.19), -65, 0.18, 0.08, thick=0.02)
    leaf(w, "leaf", (0, -0.19), 65, 0.18, 0.08, thick=0.02)
    stem(w, "leaf", [(0, 0, -0.2), (0, 0, -0.04)], 0.018)
    w.cyl("red_d", (0, 0, -0.02), 0.07, 0.1, 0.05, seg=6)
    for ang, ln, wd in ((-74, 0.2, 0.07), (-44, 0.3, 0.08), (-14, 0.38, 0.08), (16, 0.36, 0.08), (46, 0.29, 0.08),
                        (76, 0.2, 0.07)):
        leaf(w, "flame", (0, -0.02), ang, ln, wd, thick=0.026)
    for ang, ln in ((-26, 0.2), (0, 0.24), (26, 0.2)):
        leaf(w, "flame_y", (0, 0.0), ang, ln, 0.05, thick=0.03, y=-0.012)


def lan_nguyet(w):
    stem(w, "leaf", [(0, 0, -0.2), (0.01, 0, -0.1), (0.0, 0, -0.04)], 0.016)
    leaf(w, "leaf_l", (0, -0.17), -62, 0.19, 0.06, thick=0.018)
    leaf(w, "leaf", (0, -0.15), 62, 0.19, 0.06, thick=0.018)
    petals(w, "purple_l", (0, -0.0), 5, 0.20, 0.09, a0=0, thick=0.022)
    petals(w, "porcelain", (0, -0.0), 3, 0.13, 0.07, a0=36, spread=108, thick=0.02, y=-0.014)
    w.sph("star", (0, -0.04, 0.0), 0.035, seg=6)
    # crescent moon above
    pts = []
    for i in range(9):
        a = math.radians(200 + i * 17)
        pts.append((0.0 + math.cos(a) * 0.085 - 0.005, 0, 0.3 + math.sin(a) * 0.085))
    w.path("holy", pts, 0.024, 0.01, seg=5)
    sparkle(w, "holy", (-0.17, -0.03, 0.15), 0.026)
    sparkle(w, "holy", (0.17, -0.03, 0.22), 0.022)


def sen_bang(w):
    for sx in (-1, 1):
        leaf(w, "ice_w", (sx * 0.02, -0.15), sx * 76, 0.2, 0.09, thick=0.02, y=0.02)
    for ang, ln in ((-62, 0.2), (-32, 0.28), (0, 0.33), (32, 0.28), (62, 0.2)):
        w.cyl("blue_l", (math.sin(math.radians(ang)) * ln * 0.5, 0, -0.12 + math.cos(math.radians(ang)) * ln * 0.5),
              0.06, 0.0, ln, rot=(0, -ang, 0), seg=4) if False else \
            leaf(w, "blue_l", (0, -0.12), ang, ln, 0.11, thick=0.028)
    for ang, ln in ((-30, 0.17), (0, 0.22), (30, 0.17)):
        leaf(w, "ice", (0, -0.1), ang, ln, 0.06, thick=0.03, y=-0.014)
    sparkle(w, "ice_hi", (0.2, -0.04, 0.17), 0.03)
    sparkle(w, "ice_hi", (-0.2, -0.04, 0.1), 0.022)


def qua_tinh(w):
    pts = []
    for i in range(10):  # five-pointed star cross-section
        a = math.radians(90 + i * 36)
        r = 0.2 if i % 2 == 0 else 0.11
        pts.append((math.cos(a) * r, 0.0 + math.sin(a) * r))
    w.poly("holy", pts, -0.045, 0.045, bevel=0.004)
    w.sph("verdant", (0, -0.05, 0.0), 0.075, scale=(1, 0.45, 1), seg=8)
    w.sph("star", (0, -0.075, 0.0), 0.03, scale=(1, 0.5, 1), seg=6)
    stem(w, "leaf", [(0, 0, 0.2), (0.02, 0, 0.26)], 0.014)
    leaf(w, "leaf_l", (0.02, 0.25), 55, 0.13, 0.06, thick=0.018, y=0.03)
    leaf(w, "leaf", (0.02, 0.25), -45, 0.1, 0.05, thick=0.018, y=0.03)
    stars_at(w, "star", [(-0.22, -0.05, 0.16), (0.23, -0.05, -0.05), (-0.18, -0.05, -0.17)], 0.014)
    sparkle(w, "star", (0.2, -0.06, 0.2), 0.03)


def la_long(w):
    leaf(w, "jade", (-0.02, -0.22), 6, 0.5, 0.34, thick=0.03)
    leaf(w, "jade_l", (-0.02, -0.2), 6, 0.43, 0.2, thick=0.03, y=-0.012)
    w.path("gold_e", [(-0.02, -0.03, -0.22), (0.0, -0.03, 0.0), (0.03, -0.03, 0.2)], 0.013, 0.009, seg=4)
    for row, z in enumerate((-0.12, -0.04, 0.04, 0.12, 0.19)):
        n = 3 if row < 4 else 1
        for k in range(n):
            x = 0.0 + (k - (n - 1) / 2) * 0.075 + 0.01 * row
            w.box("verdant", (x, -0.04, z), (0.045, 0.012, 0.035), rot=(0, 45, 0), bevel=0)
    stem(w, "leaf_d", [(-0.02, 0, -0.22), (-0.05, 0, -0.29)], 0.016)
    sparkle(w, "star", (0.2, -0.05, 0.22), 0.028)
    sparkle(w, "verdant", (-0.2, -0.05, -0.12), 0.022)


BUILD = {"co_linh": co_linh, "nam_do": nam_do, "nhan_sam": nhan_sam, "qua_do": qua_do,
         "chuong_xanh": chuong_xanh, "sen_ngoc": sen_ngoc, "day_loi": day_loi, "hoa_diem": hoa_diem,
         "lan_nguyet": lan_nguyet, "sen_bang": sen_bang, "qua_tinh": qua_tinh, "la_long": la_long}
FLAT = {"nam_do": False}


def make(wid):
    name, grade = next((h[1], h[2]) for h in HERBS if h[0] == wid)
    w = W(wid, name, grade)
    w.pose = dict(angle=0, spin=0)
    if FLAT.get(wid, True):
        with w.at((0, 0, 0), LAY):
            BUILD[wid](w)
    else:
        BUILD[wid](w)
    return w
