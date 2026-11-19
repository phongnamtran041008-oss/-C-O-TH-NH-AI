"""dan_duoc atlas: 8 pills on dishes (dan_<g>) and 8 containers (binh_<g>)."""
import math
import random

from lib import W, leaf, sparkle, stars_at

GRADE_VI = {1: "Phàm", 2: "Hoàng", 3: "Huyền", 4: "Địa", 5: "Linh", 6: "Bảo", 7: "Tiên", 8: "Thiên"}
IDS = ["%s_%d" % (f, g) for g in range(1, 9) for f in ("dan", "binh")]


# ----------------------------------------------------------------- pills
def dish(w, key, R=0.19, h=0.045, rim=None):
    w.lathe(key, [(0.0, 0.0), (R * 0.68, 0.0), (R, h * 0.9), (R * 0.93, h), (R * 0.62, h * 0.45), (0.0, h * 0.4)],
            seg=14)
    if rim:
        w.torus(rim, (0, 0, h * 0.92), R * 0.96, 0.009, seg=14, tseg=4)


def pill(w, key, c, r, seg_sub=1, squash=0.92):
    w.ico(key, c, r, (1, 1, squash), sub=seg_sub + 1)


def dan(g):
    w = W("dan_%d" % g, GRADE_VI[g] + " Đan", g)
    w.pose = dict(angle=0, spin=0)
    z0 = 0.04
    if g == 1:  # three plain dull-brown pills on a hemp wrap
        w.box("cloth_b", (0, 0, 0.01), (0.30, 0.26, 0.022), rot=(0, 0, 8), bevel=0.004)
        w.box("clay", (0.0, 0.0, 0.026), (0.26, 0.22, 0.01), rot=(0, 0, 8), bevel=0.002)
        for c, r in (((-0.1, -0.05, 0.1), 0.062), ((0.1, -0.05, 0.1), 0.062), ((0.0, 0.07, 0.15), 0.062)):
            w.sph("clay_d", c, r, seg=10)
        w.box("clay", (-0.115, -0.108, 0.12), (0.02, 0.012, 0.016), bevel=0)
    elif g == 2:  # two or three grey-blue pills on a wooden dish
        dish(w, "wood", 0.17, 0.05)
        for c, r in (((-0.1, -0.05, 0.11), 0.062), ((0.1, -0.05, 0.11), 0.062), ((0.0, 0.07, 0.16), 0.062)):
            w.sph("iron_d", c, r, seg=10)
        w.box("bone_d", (-0.115, -0.108, 0.13), (0.02, 0.012, 0.016), bevel=0)
    elif g == 3:  # three jade-green pills with a tiny highlight, on a leaf
        with w.at((0, 0, 0.012), (90, 0, 0)):
            leaf(w, "leaf", (0.0, -0.17), 0, 0.34, 0.26, thick=0.024, y=0)
            w.box("leaf_d", (0, 0, 0.0), (0.012, 0.03, 0.30), bevel=0)
        for c, r in (((-0.1, -0.05, 0.1), 0.062), ((0.1, -0.05, 0.1), 0.062), ((0.0, 0.07, 0.15), 0.062)):
            w.sph("jade_l", c, r, seg=10)
        for c in ((-0.115, -0.108, 0.12), (0.085, -0.108, 0.12), (-0.015, -0.01, 0.17)):
            w.box("bone", c, (0.02, 0.012, 0.016), bevel=0)
    elif g == 4:  # gold pill with teal specks on a bronze plate
        dish(w, "bronze", 0.18, 0.05, rim="gold")
        pill(w, "gold", (0, 0, z0 + 0.11), 0.125)
        for p in ((-0.05, -0.11, 0.18), (0.055, -0.1, 0.14), (-0.02, -0.123, 0.11)):
            w.box("teal", p, (0.03, 0.02, 0.03), bevel=0)
    elif g == 5:  # blue pill, glowing spirit swirl, jade dish, thin aura
        dish(w, "jade", 0.18, 0.05, rim="jade_l")
        pill(w, "blue_l", (0, 0, z0 + 0.11), 0.125)
        w.torus("cyan_hi", (0, -0.10, z0 + 0.11), 0.055, 0.011, rot=(90, 0, 0), seg=12, tseg=4)
        w.sph("violet", (0, -0.115, z0 + 0.11), 0.026, scale=(1, 0.5, 1), seg=6)
        w.torus("teal", (0, 0, z0 + 0.11), 0.19, 0.007, rot=(72, 0, 0), seg=16, tseg=4)
        sparkle(w, "cyan_hi", (0.16, -0.1, 0.27), 0.028)
    elif g == 6:  # red pill with flame, dark gold stand
        dish(w, "gold_dk", 0.18, 0.06, rim="gold")
        pill(w, "red_l", (0, 0, z0 + 0.11), 0.125)
        w.cyl("flame_y", (0, -0.1, z0 + 0.11), 0.05, 0.0, 0.11, rot=(0, 0, 0), seg=4)
        for dx, hh in ((-0.07, 0.10), (0.0, 0.17), (0.07, 0.10)):
            w.cyl("flame", (dx, 0, z0 + 0.22 + hh / 2 - 0.02), 0.04, 0.0, hh, seg=5)
        w.cyl("flame_y", (0, 0, z0 + 0.25), 0.02, 0.0, 0.1, seg=4)
    elif g == 7:  # pale ice pill on a lotus of petals, tiny wings
        for k in range(8):
            with w.at((0, 0, 0.03), (0, 0, k * 45)):
                w.cyl("ice_w", (0.12, 0, 0.0), 0.05, 0.0, 0.16, rot=(0, 90, 0), seg=4)
        pill(w, "blue_l", (0, 0, 0.15), 0.11)
        w.ico("ice_hi", (-0.03, -0.05, 0.17), 0.05, sub=1)
        for sx in (-1, 1):
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.1, 0.16 + k * 0.014), sx * (68 + k * 16), 0.14 - k * 0.02, 0.055,
                     thick=0.012, y=0.04)
        sparkle(w, "ice_hi", (0.17, -0.08, 0.29), 0.03)
        sparkle(w, "ice_hi", (-0.19, -0.08, 0.22), 0.022)
    else:  # cosmic pill on an ornate gold base
        dish(w, "gold", 0.14, 0.04, rim="gold_e")
        for sx in (-1, 1):  # gold horns
            w.cyl("gold", (sx * 0.16, 0, 0.06), 0.035, 0.0, 0.17, rot=(0, sx * 35, 0), seg=5)
            w.cyl("gold", (sx * 0.2, 0, 0.11), 0.026, 0.0, 0.12, rot=(0, sx * 70, 0), seg=5)
        pill(w, "purple", (0, 0, 0.17), 0.125)
        w.torus("gold_e", (0, -0.10, 0.17), 0.065, 0.009, rot=(90, 0, 0), seg=12, tseg=4)
        w.sph("star", (0, -0.115, 0.17), 0.026, seg=6)
        stars_at(w, "star", [(-0.07, -0.105, 0.24), (0.075, -0.105, 0.12), (0.055, -0.115, 0.24)], 0.012)
        sparkle(w, "star", (0.18, -0.07, 0.31), 0.028)
    return w


# ----------------------------------------------------------------- containers
def binh(g):
    w = W("binh_%d" % g, GRADE_VI[g] + " Bình", g)
    w.pose = dict(angle=0, spin=0)
    if g == 1:  # rough clay jar, cork + twine
        w.lathe("clay", [(0, 0), (0.095, 0), (0.14, 0.07), (0.155, 0.17), (0.12, 0.26), (0.09, 0.30), (0.10, 0.325),
                         (0.08, 0.335), (0.0, 0.335)], seg=12)
        w.cyl("wood", (0, 0, 0.35), 0.075, 0.07, 0.05, seg=8)
        w.torus("clay_d", (0, 0, 0.29), 0.095, 0.011, seg=12, tseg=4)
        w.box("clay_d", (0.06, -0.14, 0.15), (0.05, 0.02, 0.07), bevel=0)  # chip / patch
    elif g == 2:  # grey clay jar, red cloth stopper tied with cord
        w.lathe("clay_d", [(0, 0), (0.09, 0), (0.135, 0.07), (0.15, 0.17), (0.12, 0.26), (0.085, 0.30),
                           (0.10, 0.32), (0.0, 0.32)], seg=12)
        w.cyl("red", (0, 0, 0.35), 0.10, 0.065, 0.07, seg=8)
        w.torus("red_l", (0, 0, 0.32), 0.092, 0.014, seg=12, tseg=4)
        w.box("paper", (0, -0.152, 0.16), (0.10, 0.012, 0.12), bevel=0.001)
        w.box("cloth_d", (0, -0.16, 0.16), (0.04, 0.008, 0.07), bevel=0)
    elif g == 3:  # porcelain bottle, blue bands, wooden cork
        w.lathe("porcelain", [(0, 0), (0.08, 0), (0.125, 0.05), (0.145, 0.15), (0.115, 0.25), (0.05, 0.31),
                              (0.045, 0.41), (0.06, 0.42), (0.0, 0.42)], seg=14)
        w.torus("blue", (0, 0, 0.12), 0.147, 0.015, seg=14, tseg=4)
        w.torus("blue", (0, 0, 0.19), 0.139, 0.012, seg=14, tseg=4)
        w.cyl("wood", (0, 0, 0.445), 0.05, 0.045, 0.05, seg=8)
        w.sph("blue_l", (0, -0.145, 0.155), 0.03, scale=(1, 0.4, 1), seg=6)
    elif g == 4:  # porcelain, gold neck + cap, teal gem
        w.lathe("porcelain", [(0, 0), (0.08, 0), (0.125, 0.05), (0.145, 0.15), (0.115, 0.25), (0.05, 0.31),
                              (0.045, 0.40), (0.06, 0.41), (0.0, 0.41)], seg=14)
        w.torus("gold", (0, 0, 0.11), 0.145, 0.014, seg=14, tseg=4)
        w.torus("gold", (0, 0, 0.21), 0.131, 0.014, seg=14, tseg=4)
        w.cyl("gold", (0, 0, 0.425), 0.07, 0.05, 0.05, seg=8)
        w.sph("gold", (0, 0, 0.465), 0.04, seg=8)
        w.sph("teal", (0, -0.14, 0.16), 0.034, scale=(1, 0.5, 1), seg=6)
    elif g == 5:  # jade gourd with spirit glow
        w.sph("jade", (0, 0, 0.13), 0.145, scale=(1, 1, 0.95), seg=12)
        w.sph("jade_l", (0, 0, 0.30), 0.095, seg=10)
        w.cyl("jade", (0, 0, 0.225), 0.06, 0.06, 0.05, seg=8)
        w.cyl("gold_d", (0, 0, 0.40), 0.035, 0.035, 0.04, seg=8)
        w.torus("violet", (0, 0, 0.245), 0.07, 0.013, seg=12, tseg=4)
        w.sph("teal", (0, -0.135, 0.14), 0.04, scale=(1, 0.4, 1), seg=6)
        w.torus("cyan", (0, 0, 0.17), 0.19, 0.007, rot=(72, 0, 0), seg=16, tseg=4)
        sparkle(w, "cyan_hi", (0.17, -0.1, 0.36), 0.03)
    elif g == 6:  # fire gourd: glowing glass, gold fittings, tongue of flame
        w.sph("red_l", (0, 0, 0.13), 0.15, scale=(1, 1, 0.95), seg=12)
        w.sph("red_l", (0, 0, 0.30), 0.098, seg=10)
        w.sph("flame_y", (0, -0.12, 0.13), 0.07, scale=(1, 0.4, 1.2), seg=8)
        w.torus("gold", (0, 0, 0.225), 0.075, 0.014, seg=12, tseg=4)
        w.cyl("gold", (0, 0, 0.395), 0.045, 0.04, 0.05, seg=8)
        w.cyl("flame", (0, 0, 0.46), 0.04, 0.0, 0.11, seg=5)
        w.cyl("flame_y", (0, 0, 0.455), 0.022, 0.0, 0.07, seg=4)
        w.cyl("gold_dk", (0, 0, 0.005), 0.11, 0.12, 0.03, seg=10)
    elif g == 7:  # ice crystal vial with small wings
        w.cyl("blue_l", (0, 0, 0.17), 0.10, 0.14, 0.26, seg=6)
        w.cyl("blue_l", (0, 0, 0.34), 0.06, 0.10, 0.10, seg=6)
        w.cyl("ice_hi", (0, -0.07, 0.17), 0.03, 0.04, 0.20, seg=6)
        w.cyl("ice_w", (0, 0, 0.405), 0.05, 0.05, 0.04, seg=6)
        w.cyl("gold", (0, 0, 0.445), 0.04, 0.03, 0.04, seg=6)
        w.cyl("gold", (0, 0, 0.03), 0.15, 0.17, 0.04, seg=6)
        for sx in (-1, 1):
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.12, 0.2 + k * 0.012), sx * (58 + k * 16), 0.18 - k * 0.03, 0.07,
                     thick=0.014, y=0.07)
        sparkle(w, "ice_hi", (0.17, -0.1, 0.4), 0.03)
    else:  # cosmic crystal vial: purple glass, gold base and stopper, stars
        w.lathe("purple", [(0, 0.03), (0.10, 0.03), (0.15, 0.12), (0.14, 0.22), (0.08, 0.30), (0.05, 0.36),
                           (0.05, 0.40), (0.0, 0.40)], seg=12)
        w.sph("purple_l", (0.0, -0.02, 0.14), 0.10, scale=(1, 0.9, 1.1), seg=8)
        w.cyl("gold", (0, 0, 0.02), 0.14, 0.17, 0.04, seg=10)
        w.cyl("gold", (0, 0, 0.42), 0.065, 0.05, 0.05, seg=8)
        w.sph("star", (0, 0, 0.47), 0.035, seg=6)
        w.torus("gold", (0, 0, 0.375), 0.06, 0.012, seg=12, tseg=4)
        stars_at(w, "star", [(-0.05, -0.12, 0.2), (0.06, -0.115, 0.12), (0.0, -0.13, 0.29), (-0.07, -0.12, 0.08)],
                 0.013)
        for sx in (-1, 1):
            w.cyl("gold", (sx * 0.17, 0, 0.12), 0.025, 0.0, 0.14, rot=(0, sx * 25, 0), seg=5)
        sparkle(w, "star", (0.19, -0.08, 0.36), 0.028)
    return w


def make(wid):
    f, g = wid.split("_")
    return (dan if f == "dan" else binh)(int(g))
