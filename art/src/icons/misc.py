"""misc atlas: spirit stones, beast egg, capture talisman, chests, key, flying-sword token,
realm-breakthrough pill."""
import math

from lib import W, leaf, sparkle, stars_at

# id, name_vi, grade
ITEMS = [
    ("linh_thach_1", "Hạ Phẩm Linh Thạch", 1),
    ("linh_thach_2", "Trung Phẩm Linh Thạch", 3),
    ("linh_thach_3", "Thượng Phẩm Linh Thạch", 5),
    ("trung_linh_thu", "Trứng Linh Thú", 3),
    ("phong_an_phu", "Phong Ấn Phù", 3),
    ("ruong_dong", "Rương Đồng", 3),
    ("ruong_mo", "Rương Đồng Mở", 3),
    ("chia_khoa", "Chìa Khóa", 2),
    ("ngu_kiem_lenh", "Ngự Kiếm Lệnh", 5),
    ("pha_canh_dan", "Phá Cảnh Đan", 6),
]
IDS = [i[0] for i in ITEMS]


def crystal(w, body, core, c, r, h, rot=(0, 0, 0), tip=0.45):
    with w.at(c, rot):
        w.cyl(body, (0, 0, h / 2), r, r, h, seg=6)
        w.cyl(body, (0, 0, h + h * tip / 2), r, 0.0, h * tip, seg=6)
        if core:
            w.cyl(core, (0, -r * 0.6, h * 0.45), r * 0.3, r * 0.3, h * 0.75, seg=4)


def linh_thach(w, n):
    w.pose = dict(angle=0, spin=15)
    if n == 1:  # dull grey chips
        for c, r, h, rot in (((0, 0, 0), 0.08, 0.22, (0, 8, 0)), ((-0.13, -0.02, 0.0), 0.06, 0.14, (0, -22, 0)),
                             ((0.12, 0.0, 0.0), 0.055, 0.12, (0, 25, 0))):
            crystal(w, "stone", None, c, r, h, rot, tip=0.35)
        w.sph("stone_d", (0.0, -0.1, 0.01), 0.05, scale=(1.4, 1, 0.6), seg=6)
        w.box("steel", (-0.02, -0.075, 0.12), (0.025, 0.01, 0.04), bevel=0)
    elif n == 2:  # bright blue crystals with a cyan facet
        for c, r, h, rot in (((0, 0, 0), 0.085, 0.2, (0, 6, 0)), ((-0.14, -0.02, 0.0), 0.065, 0.13, (0, -24, 0)),
                             ((0.13, 0.0, 0.0), 0.06, 0.14, (0, 22, 0))):
            crystal(w, "blue_l", "cyan", c, r, h, rot, tip=0.45)
        w.sph("stone_d", (0.0, -0.1, 0.01), 0.05, scale=(1.5, 1, 0.5), seg=6)
        sparkle(w, "cyan_hi", (0.17, -0.1, 0.27), 0.026)
    else:  # radiant: big cluster that glows
        for c, r, h, rot in (((0, 0, 0), 0.095, 0.24, (0, 5, 0)), ((-0.15, -0.02, 0.0), 0.07, 0.16, (0, -26, 0)),
                             ((0.15, 0.0, 0.0), 0.065, 0.17, (0, 24, 0)), ((0.05, 0.07, 0.0), 0.055, 0.19, (0, 10, 0))):
            crystal(w, "cyan", "cyan_hi", c, r, h, rot, tip=0.5)
        w.sph("stone_d", (0.0, -0.11, 0.01), 0.055, scale=(1.5, 1, 0.5), seg=6)
        sparkle(w, "cyan_hi", (0.2, -0.1, 0.3), 0.032)
        sparkle(w, "cyan_hi", (-0.2, -0.1, 0.22), 0.024)


def trung(w):
    w.pose = dict(angle=0, spin=0)
    w.torus("wood_l", (0, 0, 0.0), 0.17, 0.04, seg=12, tseg=5, scale=(1, 0.75, 1))
    w.torus("wood_d", (0, 0, 0.012), 0.12, 0.03, seg=10, tseg=4, scale=(1, 0.75, 1))
    for a in (20, 70, 120, 200, 250, 310):
        r = math.radians(a)
        w.bar("wood_d", (math.cos(r) * 0.12, math.sin(r) * 0.09, 0.015), (math.cos(r) * 0.22, math.sin(r) * 0.16, 0.05),
              0.01, seg=4)
    w.sph("bone", (0, 0, 0.19), 0.15, scale=(1, 1, 1.28), seg=12)
    for p, r in (((-0.07, -0.13, 0.22), 0.032), ((0.06, -0.135, 0.15), 0.028), ((0.0, -0.14, 0.31), 0.026),
                 ((-0.09, -0.115, 0.1), 0.022), ((0.09, -0.11, 0.26), 0.022)):
        w.sph("leaf_l", p, r, scale=(1.2, 0.5, 1), seg=5)
    w.box("teal", (0.0, -0.152, 0.2), (0.07, 0.01, 0.014), bevel=0)
    sparkle(w, "cyan_hi", (0.16, -0.1, 0.34), 0.026)


def phong_an(w):
    w.pose = dict(angle=0, spin=0)
    w.poly("paper", [(-0.1, 0.22), (0.1, 0.22), (0.1, -0.2), (0.0, -0.25), (-0.1, -0.2)], -0.01, 0.01, bevel=0.002)
    w.box("red_l", (0, -0.014, 0.19), (0.2, 0.01, 0.045), bevel=0)
    w.box("red_l", (0, -0.014, -0.15), (0.2, 0.01, 0.03), bevel=0)
    # abstract seal: a ring, a crossing and dashes (never letters)
    w.torus("red_l", (0, -0.014, 0.05), 0.055, 0.011, rot=(90, 0, 0), seg=12, tseg=4)
    w.sph("red_l", (0, -0.016, 0.05), 0.022, scale=(1, 0.4, 1), seg=6)
    for z, wd in ((-0.04, 0.12), (-0.075, 0.09), (-0.11, 0.12)):
        w.box("red_l", (0, -0.014, z), (wd, 0.01, 0.014), bevel=0)
    w.bar("red", (0, 0, 0.22), (0.0, 0, 0.3), 0.012, seg=4)
    w.torus("red", (0, 0, 0.3), 0.03, 0.008, rot=(90, 0, 0), seg=8, tseg=4)


def ruong_base(w, lid=True):
    w.box("wood_d", (0, 0, 0.0), (0.38, 0.26, 0.17), bevel=0.01)
    for sx in (-1, 1):
        w.box("gold_d", (sx * 0.13, 0, 0.0), (0.04, 0.275, 0.18), bevel=0.004)
    w.box("gold_d", (0, -0.133, -0.075), (0.38, 0.012, 0.025), bevel=0)


def ruong_dong(w):
    w.pose = dict(angle=0, spin=22)
    ruong_base(w)
    w.cyl("wood", (0, 0, 0.085), 0.13, 0.13, 0.38, rot=(0, 90, 0), seg=12)
    w.box("wood", (0, 0, 0.04), (0.38, 0.26, 0.09), bevel=0.01)
    for sx in (-1, 1):
        w.cyl("gold_d", (sx * 0.13, 0, 0.085), 0.138, 0.138, 0.04, rot=(0, 90, 0), seg=12)
    w.box("gold", (0, -0.135, 0.07), (0.06, 0.02, 0.09), bevel=0.004)
    w.box("wood_d", (0, -0.147, 0.06), (0.015, 0.008, 0.03), bevel=0)


def ruong_mo(w):
    w.pose = dict(angle=0, spin=22)
    ruong_base(w)
    w.box("wood_d", (0, -0.0, 0.082), (0.31, 0.2, 0.02), bevel=0)   # inside, dark
    # treasure heap: gold ingots, a gem and coins, glowing a little
    w.ico("gold_e", (0.0, 0.0, 0.12), 0.11, scale=(1.5, 1.0, 0.7), sub=2)
    for p in ((-0.09, -0.04, 0.17), (0.07, -0.06, 0.16), (0.0, -0.08, 0.14), (0.12, 0.02, 0.15)):
        w.cyl("gold", p, 0.035, 0.035, 0.012, rot=(70, 0, 0), seg=8)
    w.ico("cyan", (-0.04, -0.05, 0.2), 0.035, sub=1)
    # lid thrown back on the hinge
    with w.at((0, 0.13, 0.085), (-105, 0, 0)):
        w.box("wood", (0, -0.13, 0.025), (0.38, 0.26, 0.05), bevel=0.008)
        w.box("wood_d", (0, -0.13, -0.012), (0.33, 0.21, 0.02), bevel=0.004)
        for sx in (-1, 1):
            w.box("gold_d", (sx * 0.13, -0.13, 0.025), (0.04, 0.275, 0.06), bevel=0.004)
    sparkle(w, "star", (0.17, -0.1, 0.3), 0.03)
    sparkle(w, "gold_e", (-0.17, -0.1, 0.24), 0.024)


def chia_khoa(w):
    w.pose = dict(angle=40, spin=0)
    w.torus("gold", (0, 0, 0.2), 0.075, 0.026, rot=(90, 0, 0), seg=12, tseg=5, scale=(1, 1, 1.3))
    w.sph("jade_l", (0, -0.02, 0.2), 0.03, seg=5)
    w.cyl("gold", (0, 0, 0.02), 0.026, 0.026, 0.3, seg=8)
    w.cyl("gold_d", (0, 0, 0.12), 0.04, 0.04, 0.03, seg=8)
    for z, ln in ((-0.12, 0.09), (-0.065, 0.065)):
        w.box("gold", (ln / 2 + 0.01, 0, z), (ln, 0.045, 0.03), bevel=0.003)
    w.box("gold_d", (0.0, -0.025, 0.0), (0.012, 0.006, 0.26), bevel=0)


def ngu_kiem_lenh(w):
    w.pose = dict(angle=0, spin=0)
    w.cyl("jade", (0, 0, 0.0), 0.17, 0.17, 0.035, rot=(90, 0, 0), seg=16)
    w.torus("gold", (0, 0, 0.0), 0.17, 0.014, rot=(90, 0, 0), seg=16, tseg=4)
    w.torus("cyan", (0, -0.02, 0.0), 0.12, 0.008, rot=(90, 0, 0), seg=16, tseg=4)
    # abstract little sword emblem
    w.poly("gold_e", [(-0.012, -0.05), (0.012, -0.05), (0.02, 0.08), (0.0, 0.12), (-0.02, 0.08)], -0.03, -0.018,
           bevel=0)
    w.box("gold_e", (0, -0.024, -0.06), (0.09, 0.012, 0.016), bevel=0)
    w.box("gold_e", (0, -0.024, -0.09), (0.015, 0.012, 0.05), bevel=0)
    # loop and tassel
    w.torus("gold", (0, 0, 0.2), 0.03, 0.01, rot=(90, 0, 0), seg=8, tseg=4)
    w.bar("violet", (0, 0, -0.17), (0, 0, -0.26), 0.014, seg=4)
    w.sph("violet", (0, 0, -0.27), 0.022, seg=6)
    for dx in (-0.025, 0, 0.025):
        w.bar("violet", (0, 0, -0.27), (dx * 2, 0, -0.36), 0.008, 0.004, seg=4)
    sparkle(w, "cyan_hi", (0.19, -0.05, 0.16), 0.028)


def pha_canh_dan(w):
    w.pose = dict(angle=0, spin=0)
    w.lathe("red_d", [(0, 0), (0.16, 0), (0.2, 0.05), (0.18, 0.06), (0.12, 0.03), (0, 0.03)], seg=14)
    w.torus("gold", (0, 0, 0.05), 0.185, 0.011, seg=14, tseg=4)
    w.ico("gold", (0, 0, 0.17), 0.13, scale=(1, 1, 0.95), sub=2)
    w.ico("gold_e", (-0.03, -0.05, 0.2), 0.065, sub=1)
    w.torus("holy", (0, 0, 0.17), 0.19, 0.01, rot=(78, 0, 0), seg=16, tseg=4)
    for k, dz in enumerate((0.0, 0.055)):  # rising chevrons
        for sx in (-1, 1):
            w.box("flame_y", (sx * 0.035, -0.03, 0.34 + dz), (0.075, 0.02, 0.022), rot=(0, -sx * 35, 0), bevel=0)
    sparkle(w, "star", (0.19, -0.06, 0.3), 0.03)
    sparkle(w, "holy", (-0.2, -0.06, 0.18), 0.024)


def make(wid):
    name, grade = next((i[1], i[2]) for i in ITEMS if i[0] == wid)
    w = W(wid, name, grade)
    w.pose = dict(angle=0, spin=0)
    if wid.startswith("linh_thach"):
        linh_thach(w, int(wid[-1]))
    else:
        {"trung_linh_thu": trung, "phong_an_phu": phong_an, "ruong_dong": ruong_dong, "ruong_mo": ruong_mo,
         "chia_khoa": chia_khoa, "ngu_kiem_lenh": ngu_kiem_lenh, "pha_canh_dan": pha_canh_dan}[wid](w)
    return w
