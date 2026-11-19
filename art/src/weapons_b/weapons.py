"""WEAPONS_B: 4 types x 8 grades.  Convention: grip at origin, length along +Z, broad side faces -Y,
1 unit = 1 m, character 1.0 m tall (chibi-thick).  One function per type, shape varies per grade."""
import math
import random
from mathutils import Vector
from geom import Builder, mat_spec as M

TYPES = {"truong": "Trượng", "cung": "Cung", "phien": "Phiến", "ho_lo": "Hồ Lô"}
PREFIX = {1: "Mộc", 2: "Thiết", 3: "Bích Ngọc", 4: "Kim Lam", 5: "Linh Quang",
          6: "Hỏa Diệm", 7: "Băng Dực", 8: "Tinh Không"}


def name_vi(t, g):
    return "%s %s" % (PREFIX[g], TYPES[t])


# ---------------------------------------------------------------- palettes (sRGB hex)
BASE = {
    1: dict(main=M("6b4423", 0, .9), dark=M("4a2e16", 0, .95), metal=M("a08a55", 0, .95), trim=M("a08a55", 0, .95),
            cord=M("a08a55", 0, .95)),
    2: dict(main=M("6a4426", 0, .85), dark=M("46301a", 0, .9), metal=M("8c9199", .8, .45), trim=M("5f646c", .8, .5),
            cord=M("c0201a", 0, .8)),
    3: dict(main=M("3fb078", 0, .35), dark=M("1f7a52", 0, .4), metal=M("b87333", .8, .4), trim=M("8a5524", .8, .45),
            cord=M("2a8a5e", 0, .7), gem=M("7be8b4", 0, .2, "7be8b4", .4)),
    4: dict(main=M("4a2216", 0, .6), dark=M("2e140d", 0, .6), metal=M("f2c14e", 1, .3), trim=M("d9a52e", 1, .35),
            cord=M("1aa6a0", 0, .6), gem=M("19e6d8", 0, .15, "19e6d8", 1.6)),
    5: dict(main=M("5a48c8", 0, .4, ramp="purple", glow=0), dark=M("2c2270", 0, .5, ramp="purple", glow=0), metal=M("f2c14e", 1, .3),
            trim=M("d9a52e", 1, .35), cord=M("9fe6ff", 0, .3, "9fe6ff", 2.5),
            gem=M("9fe6ff", 0, .1, "9fe6ff", 4.5), glow=M("b57bff", 0, .2, "b57bff", 3.5)),
    6: dict(main=M("231710", .3, .6), dark=M("120c08", .2, .7), metal=M("4a3414", .9, .4), trim=M("6a4a1c", .9, .4),
            cord=M("ff6a10", 0, .5, "ff6a10", 4), gem=M("ff2a10", 0, .2, "ff2a10", 7),
            flame=M("ff6a10", 0, .3, "ff6a10", 5.5), glow=M("ffc830", 0, .3, "ffc830", 6), ember=M("ff3a10", 0, .3, "ff3a10", 4.5)),
    7: dict(main=M("9fd0f5", .1, .25, ramp="blue", glow=0), dark=M("5f9bd0", .1, .3, ramp="blue", glow=0), metal=M("dfeeff", .6, .3),
            trim=M("c7e3ff", .6, .3), cord=M("e8fbff", 0, .3, "e8fbff", 1.8), gem=M("6fdcff", 0, .1, "6fdcff", 4.5),
            wing=M("f4ffff", 0, .3, "f4ffff", 1.6), frost=M("d8f0ff", 0, .4, ramp="blue", glow=0), glow=M("bff4ff", 0, .3, "bff4ff", 3)),
    8: dict(main=M("4a1a8a", .2, .4, ramp="purple", glow=0), dark=M("1b0840", .2, .5, ramp="purple", glow=0), metal=M("f2c14e", 1, .3), trim=M("d9a52e", 1, .35),
            cord=M("e8d8ff", 0, .4, glow=0), gem=M("b45cff", 0, .2, "b45cff", 3.5),
            core=M("ffd36a", 0, .2, "ffd36a", 7, prio=2.0), star=M("fff4ff", 0, .2, "fff4ff", 9, prio=3.0),
            glow=M("b45cff", 0, .2, "b45cff", 3.5)),
}
OVERRIDE = {
    "phien": {
        1: dict(main=M("e6d3a0", 0, .95), dark=M("c9b27a", 0, .95), metal=M("8a6a3a", 0, .9), trim=M("8a6a3a", 0, .9)),
        2: dict(main=M("c3c8cf", 0, .9), dark=M("8a9099", 0, .9)),
        3: dict(main=M("4fc886", 0, .8), dark=M("2a8c5a", 0, .8)),
        4: dict(main=M("4a2a52", 0, .8), dark=M("2a1632", 0, .8)),
        5: dict(main=M("a6e4ff", 0, .6, ramp="blue", glow=0), dark=M("b79cff", 0, .6, ramp="purple", glow=0)),
        6: dict(main=M("d8381a", 0, .6, ramp="red", glow=0), dark=M("ff9a1a", 0, .6, ramp="gold", glow=0)),
        7: dict(main=M("b4e0ff", 0, .6, ramp="blue", glow=0), dark=M("6aaee8", 0, .6, ramp="blue", glow=0)),
        8: dict(main=M("2a0f55", 0, .6), dark=M("140630", 0, .6)),
    },
    "ho_lo": {
        1: dict(main=M("a0692a", 0, .9), dark=M("6e4418", 0, .95), trim=M("5a3a1a", 0, .95)),
        2: dict(main=M("7a4a20", 0, .8), dark=M("4e2e12", 0, .9)),
        3: dict(main=M("4fd09a", 0, .3, ramp="jade", glow=0), dark=M("2a9070", 0, .3, ramp="jade", glow=0)),
        4: dict(main=M("7a4220", 0, .5), dark=M("4a2410", 0, .6)),
        5: dict(main=M("a8e4f4", 0, .2, ramp="blue", glow=0), dark=M("9a80ff", 0, .2, ramp="purple", glow=0)),
        6: dict(main=M("5a1612", 0, .5, ramp="red", glow=0), dark=M("1a0a0a", 0, .6, ramp="red", glow=0)),
        7: dict(main=M("9fd4f5", 0, .2, ramp="blue", glow=0), dark=M("6aaee8", 0, .3, ramp="blue", glow=0)),
        8: dict(main=M("4a1a8a", .2, .35, ramp="purple", glow=0), dark=M("1b0840", .2, .5, ramp="purple", glow=0)),
    },
}


def palette(t, g):
    p = dict(BASE[g])
    p.update(OVERRIDE.get(t, {}).get(g, {}))
    return p


V = Vector


def wing(B, base, s, ang0, step, ln, w, y=0.0):
    """Three overlapping feathers fanning from one root. s mirrors the angle."""
    for k in range(3):
        B.leaf(base, s * (ang0 + k * step), ln * (1 - 0.14 * k), w, "wing", 0.014, y=y)


# ---------------------------------------------------------------- staff (truong)
def truong(B, g):
    top = 0.78
    if g == 1:  # crooked dried branch
        pts = [(0, 0, -0.32), (0.015, 0, 0.0), (-0.02, 0, 0.35), (0.012, 0, 0.62), (0, 0, 0.8)]
        for a, b in zip(pts, pts[1:]):
            B.cyl(a, b, 0.036, 0.034, "main", 8)
        for p in pts[1:-1]:
            B.sph(p, 0.04, "main", 8, 5)
        B.cyl((0, 0, 0.8), (0.1, 0, 1.0), 0.03, 0.02, "main", 7)
        B.cyl((0, 0, 0.8), (-0.075, 0, 0.98), 0.028, 0.018, "dark", 7)
        B.sph((0.1, 0, 1.0), 0.024, "main", 7, 4)
        B.cyl((0.01, 0, 0.5), (0.07, 0, 0.62), 0.02, 0.012, "dark", 6)
        B.cyl((0, 0, -0.1), (0, 0, 0.1), 0.045, 0.045, "cord", 8)
        return
    B.cyl((0, 0, -0.3), (0, 0, top), 0.034, 0.03, "main", 10)
    B.cyl((0, 0, -0.08), (0, 0, 0.1), 0.044, 0.044, "cord" if g <= 3 else "dark", 10)
    if g == 2:
        B.cyl((0, 0, -0.32), (0, 0, -0.22), 0.04, 0.036, "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.07), 0.052, 0.034, "metal")
        B.sph((0, 0, top + 0.12), 0.055, "metal", 10, 6)
        B.tor((0, 0, 0.6), 0.04, 0.012, (0, 0, 1), "metal")
        for dx, dz in ((0.03, -0.2), (-0.02, -0.25)):
            B.cyl((0.04, 0, 0.1), (0.05 + dx, 0, 0.1 + dz), 0.01, 0.01, "cord", 6)
        B.sph((0.045, 0, 0.1), 0.022, "cord", 7, 5)
    elif g == 3:
        B.cyl((0, 0, -0.32), (0, 0, -0.2), 0.042, 0.036, "metal")
        for z in (0.3, 0.55):
            B.tor((0, 0, z), 0.034, 0.011, (0, 0, 1), "metal")
        B.sph((0, 0, 0.95), 0.085, "gem", 12, 8)
        for k in range(3):
            a = math.radians(120 * k + 30)
            d = V((math.cos(a), math.sin(a), 0))
            B.cyl(V((0, 0, top)), V((0, 0, 0.92)) + d * 0.09, 0.016, 0.012, "metal", 6)
            B.cyl(V((0, 0, 0.92)) + d * 0.09, V((0, 0, 1.06)) + d * 0.04, 0.012, 0.007, "metal", 6)
        B.sph((0, 0, top), 0.04, "metal", 8, 5)
    elif g == 4:
        for z in (-0.2, 0.2, 0.45, 0.68):
            B.tor((0, 0, z), 0.036, 0.011, (0, 0, 1), "metal")
        B.cyl((0, 0, -0.32), (0, 0, -0.2), 0.04, 0.034, "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.07), 0.05, 0.03, "trim")
        B.tor((0, 0, 0.97), 0.095, 0.014, (0, 1, 0), "metal", 20, 6)
        B.sph((0, 0, 0.97), (0.055, 0.055, 0.11), "gem", 6, 4, smooth=False)
        for s in (-1, 1):
            B.cyl((0.0, 0, top + 0.05), (s * 0.12, 0, 0.95), 0.016, 0.01, "metal", 6)
            B.cyl((s * 0.12, 0, 0.95), (s * 0.1, 0, 1.08), 0.01, 0.005, "metal", 6)
        B.sph((0, 0, 1.1), 0.02, "metal", 6, 4)
        B.sph((0, 0, 0.15), 0.028, "gem", 6, 4, smooth=False)
    elif g == 5:
        for z in (-0.2, 0.3, 0.6):
            B.tor((0, 0, z), 0.038, 0.011, (0, 0, 1), "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.06), 0.05, 0.03, "metal")
        B.tor((0, 0, 0.96), 0.115, 0.014, (0, 1, 0), "metal", 22, 6)
        B.tor((0, 0, 0.96), 0.08, 0.01, (1, 0.3, 0), "glow", 20, 5)
        B.sph((0, 0, 0.96), 0.075, "gem", 12, 8)
        for k, ang in enumerate((-40, -15, 15, 40)):
            a = math.radians(ang)
            B.cyl(V((math.sin(a) * 0.1, 0, 0.96 + math.cos(a) * 0.1)), V((math.sin(a) * 0.17, 0, 0.96 + math.cos(a) * 0.19)),
                  0.02, 0.003, "glow", 5, smooth=False)
        B.cyl((0, 0, 1.03), (0, 0, 1.17), 0.02, 0.003, "glow", 5, smooth=False)
        for p in ((0.13, 0, 0.78), (-0.12, 0, 1.12), (0.09, 0, 1.15)):
            B.sph(p, 0.014, "glow", 6, 4)
    elif g == 6:  # brazier: cage of blackened rods around a fire
        for z in (-0.2, 0.3, 0.6):
            B.tor((0, 0, z), 0.038, 0.012, (0, 0, 1), "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.08), 0.052, 0.034, "metal")
        B.tor((0, 0, 0.9), 0.1, 0.016, (0, 0, 1), "metal", 20, 6)
        for k in range(5):
            a = math.radians(72 * k + 18)
            B.cyl(V((math.cos(a) * 0.1, math.sin(a) * 0.1, 0.9)), V((math.cos(a) * 0.045, math.sin(a) * 0.045, 1.14)), 0.016, 0.01, "metal", 6)
            B.cyl(V((0, 0, top + 0.04)), V((math.cos(a) * 0.1, math.sin(a) * 0.1, 0.9)), 0.012, 0.012, "metal", 5)
        B.tor((0, 0, 1.14), 0.045, 0.012, (0, 0, 1), "metal", 14, 5)
        B.sph((0, 0, 0.96), 0.06, "gem", 10, 7)
        for k, (ang, ln) in enumerate(((-34, .2), (-14, .3), (0, .38), (14, .3), (34, .2))):
            a = math.radians(ang)
            p0 = V((math.sin(a) * 0.03, 0, 0.98))
            B.cyl(p0, p0 + V((math.sin(a), 0, math.cos(a))) * ln, 0.05 if ln > .25 else 0.04, 0.004,
                  ("glow", "flame", "ember")[min(2, abs(k - 2))], 7, smooth=False)
    elif g == 7:
        for z in (-0.2, 0.3, 0.6):
            B.tor((0, 0, z), 0.038, 0.011, (0, 0, 1), "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.06), 0.05, 0.03, "metal")
        B.sph((0, 0, 1.02), (0.065, 0.065, 0.2), "gem", 6, 4, smooth=False)
        for s in (-1, 1):  # small wings
            wing(B, (s * 0.03, 0, 0.86), s, 25, 22, 0.26, 0.05)
        for p, r in (((0.06, 0.03, -0.3), .04), ((-0.04, 0.02, -0.28), .035), ((0.0, -0.03, -0.25), .03), ((0.1, 0.0, -0.22), .025)):
            B.sph(p, r, "frost", 7, 5)
        B.sph((0, 0, 1.18), 0.02, "glow", 6, 4)
    else:  # 8 cosmic: orb, two orbit rings, star specks
        for z in (-0.2, 0.3, 0.6):
            B.tor((0, 0, z), 0.038, 0.011, (0, 0, 1), "metal")
        B.cyl((0, 0, top - 0.02), (0, 0, top + 0.06), 0.052, 0.034, "metal")
        B.sph((0, 0, 0.98), 0.1, "main", 14, 9)
        B.sph((0, 0, 0.98), 0.05, "core", 10, 7)
        B.tor((0, 0, 0.98), 0.14, 0.014, (0, 1, 0), "metal", 24, 6)
        B.tor((0, 0, 0.98), 0.125, 0.012, (0.9, 0.2, 0.5), "metal", 24, 5)
        for k in range(4):
            a = math.radians(90 * k + 45)
            B.cyl(V((math.sin(a) * 0.05, 0, top + 0.05)), V((math.sin(a) * 0.1, 0, 0.9)), 0.014, 0.01, "metal", 5)
        random.seed(8)
        for k in range(9):
            a = random.uniform(0, 6.28)
            r = random.uniform(0.07, 0.16)
            B.sph((math.cos(a) * r, -0.06 - random.uniform(0, 0.03), 0.98 + math.sin(a) * r), 0.017, "star", 5, 3)
        B.cyl((0, 0, 1.1), (0, 0, 1.24), 0.02, 0.003, "core", 5, smooth=False)

# ---------------------------------------------------------------- bow (cung)
def _bowpath(t, g):
    h = 0.16 if g < 8 else 0.18
    x = h * (1 - t * t)
    x = x - h * 0.9 * max(0.0, abs(t) - 0.62) ** 2 * 2.4
    return V((x - h * 0.55, 0, 0.46 * t))


def cung(B, g):
    N = 16
    ts = [-1 + 2 * i / N for i in range(N + 1)]
    pts = [_bowpath(t, g) for t in ts]
    limb = "main"
    for i in range(N):
        t0, t1 = abs(ts[i]), abs(ts[i + 1])
        r0 = 0.055 - 0.028 * t0
        r1 = 0.055 - 0.028 * t1
        B.cyl(pts[i], pts[i + 1], r0, r1, limb, 8)
        B.sph(pts[i + 1], r1, limb, 8, 5)
    tipA, tipB = pts[0], pts[-1]
    strcol = "cord"
    B.cyl(tipA, tipB, 0.014, 0.014, strcol, 5)
    grip0, grip1 = V((pts[N // 2].x, 0, -0.08)), V((pts[N // 2].x, 0, 0.08))
    gcol = "cord" if g <= 2 else ("metal" if g in (3, 5, 8) else "dark")
    B.cyl(grip0, grip1, 0.07, 0.07, gcol, 10)
    c = pts[N // 2]
    if g == 2:
        for p in (tipA, tipB):
            B.sph(p, 0.026, "metal", 7, 5)
        B.cyl(c + V((0.0, 0, -0.07)), c + V((0.02, 0, -0.2)), 0.01, 0.01, "cord", 5)
        B.cyl(c + V((0.0, 0, -0.07)), c + V((-0.03, 0, -0.19)), 0.01, 0.01, "cord", 5)
        B.sph(c + V((0.02, 0, -0.2)), 0.02, "cord", 6, 4)
        B.tor(pts[N // 4], 0.03, 0.01, (0, 0, 1), "metal")
    elif g == 3:
        for p in (tipA, tipB):
            B.sph(p, 0.03, "metal", 7, 5)
        B.sph(c + V((0.0, -0.035, 0)), (0.04, 0.012, 0.05), "gem", 8, 5)
        for t in (-0.5, 0.5):
            B.tor(_bowpath(t, g), 0.032, 0.01, (0.2, 0, 1), "metal")
    elif g == 4:
        B.sph(c + V((0.0, -0.04, 0)), (0.045, 0.02, 0.06), "gem", 6, 4, smooth=False)
        for s, p in ((1, tipB), (-1, tipA)):
            B.cyl(p, p + V((0.05, 0, s * 0.07)), 0.018, 0.005, "metal", 6)
            B.cyl(p, p + V((-0.04, 0, s * 0.09)), 0.016, 0.005, "metal", 6)
        for t in (-0.55, -0.3, 0.3, 0.55):
            B.tor(_bowpath(t, g), 0.034, 0.01, (0.2 * t, 0, 1), "metal")
        for s in (-1, 1):
            B.cyl(c + V((0.03, 0, s * 0.1)), c + V((0.12, 0, s * 0.2)), 0.015, 0.004, "trim", 5)
    elif g == 5:
        for s, p in ((1, tipB), (-1, tipA)):
            B.leaf(p, 180 - 25 if s > 0 else 25 + 0, 0.14, 0.05, "glow", 0.014)
            B.sph(p, 0.03, "gem", 7, 5)
        B.sph(c + V((0.0, -0.035, 0)), (0.05, 0.02, 0.06), "gem", 8, 6)
        B.tor(c, 0.07, 0.01, (0, 1, 0), "glow", 20, 5)
        for t in (-0.5, 0.5):
            B.tor(_bowpath(t, g), 0.034, 0.011, (0.2, 0, 1), "metal")
    elif g == 6:
        random.seed(6)
        for i in range(3, N - 2, 3):
            p = pts[i]
            n = V((1, 0, 0))
            B.cyl(p + n * 0.02, p + n * (0.07 + 0.025 * (i % 4)) + V((0, 0, 0.03 * (1 if ts[i] > 0 else -1))),
                  0.026, 0.003, "flame" if i % 4 == 0 else "glow", 6, smooth=False)
        for s, p in ((1, tipB), (-1, tipA)):
            B.cyl(p, p + V((0.0, 0, s * 0.14)), 0.03, 0.003, "flame", 6, smooth=False)
        B.sph(c + V((0.0, -0.03, 0)), 0.04, "gem", 8, 6)
    elif g == 7:  # clean ice arc, small wing tips
        wing(B, tipB, 1, 5, 24, 0.13, 0.03)
        wing(B, tipA, 1, 175, -24, 0.13, 0.03)
        B.sph(c + V((0.0, -0.035, 0)), (0.035, 0.015, 0.055), "gem", 6, 4, smooth=False)
    elif g == 8:
        B.sph(c + V((0.0, -0.035, 0)), (0.045, 0.02, 0.045), "core", 10, 7)
        B.tor(c, 0.085, 0.01, (0, 1, 0), "metal", 22, 6)
        for p in (tipA, tipB):
            B.sph(p, 0.026, "metal", 7, 5)
        random.seed(8)
        for k in range(10):
            t = random.choice((-1, 1)) * random.uniform(0.2, 0.9)
            p = _bowpath(t, g)
            B.sph(p + V((random.uniform(0.0, 0.03), -random.uniform(0.045, 0.06), 0.0)), 0.017, "star", 5, 3)


# ---------------------------------------------------------------- folding fan (phien)
def phien(B, g):
    R = 0.24
    pivot = V((0, 0, 0.0))
    spread = 62
    n = {1: 7, 2: 8, 3: 9, 4: 9, 5: 9, 6: 9, 7: 9, 8: 9}[g]
    feather = False
    Rc = R * 0.76 if g == 6 else R
    angs = [-spread + 2 * spread * i / n for i in range(n + 1)]

    def pt(a, r, y=0.0):
        a = math.radians(a)
        return V((math.sin(a) * r, y, 0.02 + math.cos(a) * r))

    # handle
    B.cyl((0, 0, -0.17), (0, 0, 0.03), 0.026, 0.03, "metal" if g in (1, 2, 3, 4) else "dark", 8)
    B.sph((0, 0, -0.17), 0.03, "metal" if g != 6 else "trim", 7, 5)
    # cloth
    for i in range(n):
        y0 = 0.012 if i % 2 == 0 else -0.012
        y1 = -y0
        mat = "main" if i % 2 == 0 else "dark"
        if feather:
            mid = (angs[i] + angs[i + 1]) / 2
            c = abs(mid) / spread
            ln = R * (1.12 - 0.35 * c) if g == 6 else R * (1.05 - 0.15 * c)
            body = R * 0.85
            w = 8
            pts = [pivot + V((0, y0, 0.02)), pt(angs[i] - w, body, y0), pt(mid, ln, 0.0), pt(angs[i + 1] + w, body, y1)]
            B.prism(pts, 0.01, mat)
            if g in (5, 6):
                B.prism([pt(angs[i] * .5 + mid * .5, R * 0.5, -0.012), pt(mid, ln * 0.8, -0.012),
                         pt(angs[i + 1] * .5 + mid * .5, R * 0.5, -0.012)], 0.008, ("glow" if i % 2 else "flame") if g == 6 else ("gem" if i % 2 else "glow"))
        else:
            pts = [pivot + V((0, y0, 0.02)), pt(angs[i], Rc, y0), pt(angs[i + 1], Rc, y1)]
            B.prism(pts, 0.01, mat)
    # ribs
    for i in range(n + 1):
        edge = i in (0, n)
        r1 = Rc * (1.04 if edge else 0.98)
        if feather and not edge:
            continue
        B.cyl(pt(angs[i], 0.0), pt(angs[i], r1, 0.0), 0.014 if edge else 0.006, 0.012 if edge else 0.005,
              ("metal" if g in (2, 3, 4, 5, 8) else ("trim" if g == 6 else "dark")) if g != 1 else "metal", 6)
    # rim
    if g in (3, 4, 5, 8):
        rim = "glow" if g == 5 else "metal"
        for i in range(n):
            B.cyl(pt(angs[i], R), pt(angs[i + 1], R), 0.013, 0.013, rim, 6)
        for i in range(n + 1):
            B.sph(pt(angs[i], R), 0.017, "gem" if g == 5 else "metal", 6, 4)
        if g == 5:
            for i in range(n):
                B.prism([pt(angs[i], 0.1, -0.012), pt((angs[i] + angs[i + 1]) / 2, R * 0.8, -0.012), pt(angs[i + 1], 0.1, -0.012)], 0.006, "glow" if i % 2 else "gem")
    if g == 2:
        for i in range(n):
            B.cyl(pt(angs[i], R * 0.99), pt(angs[i + 1], R * 0.99), 0.008, 0.008, "metal", 5)
    B.sph(pivot + V((0, 0, 0.02)), 0.028, "metal" if g != 6 else "trim", 8, 6)
    # tassels
    if g in (2, 4):
        col = "cord"
        B.cyl((0.0, 0, -0.2), (0.015, 0, -0.3), 0.008, 0.008, col, 5)
        B.cyl((0.0, 0, -0.2), (-0.02, 0, -0.29), 0.008, 0.008, col, 5)
        B.sph((0.0, 0, -0.21), 0.022, col, 6, 4)
    if g == 4:
        B.sph((0, -0.026, 0.02), (0.03, 0.014, 0.04), "gem", 6, 4, smooth=False)
        B.tor((0.0, -0.016, 0.16), 0.032, 0.007, (0, 1, 0), "metal", 16, 5)
        B.sph((0.0, -0.016, 0.16), 0.014, "metal", 6, 4)
    if g == 3:
        B.sph((0, -0.026, 0.02), 0.026, "gem", 8, 5)
    if g == 5:
        B.sph((0, -0.026, 0.02), 0.026, "gem", 8, 5)
        for p in ((0.2, -0.03, 0.3), (-0.17, -0.03, 0.33), (0.0, -0.03, 0.4)):
            B.sph(p, 0.014, "glow", 6, 4)
    if g == 6:
        B.sph((0, -0.026, 0.02), 0.03, "gem", 8, 5)
        for k in range(7):  # flame-shaped feather tips, red at the edges -> yellow in the middle
            a = -54 + 18 * k
            c = abs(k - 3)
            B.leaf(pt(a, Rc * 0.88), a, R * (0.62 - 0.07 * c) , 0.05, ("glow", "flame", "ember", "ember")[c], 0.012, y=-0.004 if k % 2 else 0.004)
    if g == 7:
        B.sph((0, -0.026, 0.02), 0.026, "gem", 6, 4, smooth=False)
        for s in (-1, 1):
            wing(B, (s * 0.03, -0.02, -0.02), s, 100, 22, 0.17, 0.035, y=-0.02)
        for i in range(n + 1):  # crystal-pointed ribs
            B.cyl(pt(angs[i], R * 0.98), pt(angs[i], R * 1.2), 0.016, 0.002, "gem", 5, smooth=False)
    if g == 8:
        B.sph((0, -0.03, 0.02), 0.035, "core", 9, 6)
        random.seed(8)
        for k in range(16):
            a = random.uniform(-spread + 6, spread - 6)
            r = random.uniform(0.07, R * 0.92)
            B.sph(pt(a, r, -0.024), 0.011, "star", 5, 3)
        for s in (-1, 1):
            B.cyl(pt(s * 30, R * 0.3), pt(s * 30, R * 0.95, -0.016), 0.006, 0.004, "glow", 5)


# ---------------------------------------------------------------- gourd (ho_lo)
GOURD_PROFILE = [(0, -0.185), (0.04, -0.18), (0.075, -0.165), (0.1, -0.14), (0.115, -0.1), (0.115, -0.06),
                 (0.097, -0.02), (0.058, 0.0), (0.042, 0.02), (0.05, 0.04), (0.07, 0.06), (0.08, 0.085),
                 (0.075, 0.11), (0.056, 0.135), (0.036, 0.155), (0.03, 0.17), (0.0, 0.17)]


def lathe(B, prof, mat, seg=16):
    import bmesh
    bm = B._bm(mat)
    rings = []
    for r, z in prof:
        if r < 1e-6:
            rings.append([bm.verts.new(V((0, 0, z)))])
        else:
            rings.append([bm.verts.new(V((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)))
                          for k in range(seg)])
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        for k in range(seg):
            k2 = (k + 1) % seg
            if len(a) == 1:
                f = bm.faces.new((a[0], b[k2], b[k]))
            elif len(b) == 1:
                f = bm.faces.new((a[k], a[k2], b[0]))
            else:
                f = bm.faces.new((a[k], a[k2], b[k2], b[k]))
            f.smooth = True


def ho_lo(B, g):
    prof = GOURD_PROFILE
    if g == 3:  # slimmer jade bottle gourd
        prof = [(r * 0.92, z) for r, z in prof]
    lathe(B, prof, "main", 18)
    # stopper
    st_mat = {1: "dark", 2: "dark", 3: "metal", 4: "metal", 5: "metal", 7: "metal", 8: "metal"}.get(g)
    if st_mat:
        B.cyl((0, 0, 0.165), (0, 0, 0.215), 0.036, 0.042, st_mat, 10)
        B.sph((0, 0, 0.215), (0.042, 0.042, 0.02), st_mat, 10, 4)
    # cord around the waist + tails
    cord = "cord"
    B.tor((0, 0, 0.012), 0.058, 0.012, (0, 0, 1), "cord" if g != 6 else "trim", 18, 5)
    if g in (1, 2, 3, 4, 5):
        B.sph((0.062, -0.02, 0.012), 0.02, cord if g != 3 else "metal", 6, 4)
        B.cyl((0.062, -0.02, 0.012), (0.07, -0.025, -0.075), 0.009, 0.009, cord, 5)
        B.cyl((0.062, -0.02, 0.012), (0.045, -0.03, -0.06), 0.009, 0.009, cord, 5)
    # carrying loop over the stopper
    if g in (1, 2, 3, 4, 5, 7, 8):
        B.tor((0, 0, 0.19), 0.055, 0.007, (0, 1, 0), cord if g < 7 else ("wing" if g == 7 else "metal"), 16, 4)
    if g == 2:
        B.tor((0, 0, -0.17), 0.05, 0.012, (0, 0, 1), "metal", 18, 5)
        B.tor((0, 0, 0.012), 0.055, 0.009, (0, 0, 1), "metal", 18, 5)
    elif g == 3:
        B.tor((0, 0, -0.165), 0.06, 0.011, (0, 0, 1), "metal", 18, 5)
        B.tor((0, 0, 0.14), 0.04, 0.01, (0, 0, 1), "metal", 14, 5)
        B.sph((0.0, -0.11, -0.07), (0.035, 0.012, 0.05), "gem", 8, 5)
    elif g == 4:
        for z, rr in ((-0.165, 0.055), (-0.04, 0.115), (0.07, 0.078)):
            B.tor((0, 0, z), rr, 0.01, (0, 0, 1), "metal", 20, 5)
        B.sph((0.0, -0.118, -0.075), (0.045, 0.016, 0.055), "gem", 6, 4, smooth=False)
        B.sph((0, 0, 0.23), 0.018, "metal", 6, 4)
    elif g == 5:  # pale glass, one gold band, one small gem
        B.tor((0, 0, -0.165), 0.055, 0.013, (0, 0, 1), "metal", 20, 5)
        B.tor((0, 0, 0.012), 0.062, 0.016, (0, 0, 1), "metal", 20, 5)
        B.sph((0.0, -0.112, -0.07), (0.032, 0.014, 0.04), "gem", 8, 5)
        B.sph((0, 0, 0.235), 0.02, "gem", 7, 5)
        for p in ((0.13, -0.05, 0.12), (-0.12, -0.05, 0.02)):
            B.sph(p, 0.012, "glow", 6, 4)
    elif g == 6:  # lacquer body, ember cracks, small flame at the mouth
        B.tor((0, 0, -0.165), 0.058, 0.011, (0, 0, 1), "metal", 18, 5)
        B.tor((0, 0, 0.06), 0.077, 0.011, (0, 0, 1), "metal", 18, 5)
        for nrm, z in (((0.5, 0.2, 1), -0.09), ((-0.45, 0.3, 1), -0.07)):
            B.tor((0, 0, z), 0.117, 0.007, nrm, "ember", 22, 4)
        B.tor((0, 0, 0.085), 0.083, 0.006, (0.4, 0.2, 1), "ember", 18, 4)
        B.sph((0.0, -0.112, -0.07), (0.03, 0.012, 0.04), "glow", 8, 5)
        for k, (ang, ln, mat) in enumerate(((-30, .08, "ember"), (-8, .14, "flame"), (12, .17, "glow"), (34, .09, "ember"))):
            a = math.radians(ang)
            p0 = V((math.sin(a) * 0.015, 0.0, 0.165))
            B.cyl(p0, p0 + V((math.sin(a) * 0.9, 0, math.cos(a))) * ln, 0.026, 0.003, mat, 7, smooth=False)
    elif g == 7:  # ice crystal body, two small wings at the neck, frost only at the base
        B.tor((0, 0, -0.165), 0.058, 0.01, (0, 0, 1), "metal", 18, 5)
        for s in (-1, 1):
            wing(B, (s * 0.04, 0, 0.06), s, 70, -22, 0.14, 0.035)
        for p, r in (((0.0, -0.06, -0.185), .035), ((0.09, -0.03, -0.185), .03), ((-0.09, -0.03, -0.185), .03)):
            B.sph(p, r, "frost", 7, 5)
    elif g == 8:
        B.tor((0, 0, -0.165), 0.056, 0.011, (0, 0, 1), "metal", 18, 5)
        B.tor((0.0, -0.01, -0.06), 0.128, 0.009, (0, 1, 0.0), "metal", 22, 5)
        B.sph((0.0, -0.11, -0.07), 0.034, "core", 9, 6)
        random.seed(8)
        for k in range(14):
            a = random.uniform(0, 6.28)
            z = random.uniform(-0.15, 0.12)
            rr = 0.118 if z < -0.02 else 0.082
            B.sph((math.cos(a) * rr * 1.04, -abs(math.sin(a)) * rr * 1.04, z), 0.011, "star", 5, 3)
        B.sph((0, 0, 0.235), 0.02, "core", 7, 5)
    else:
        pass


SCALE = {"truong": 0.82, "cung": 0.92, "phien": 1.0, "ho_lo": 1.0}
XY = {"truong": 1.0, "cung": 1.0, "phien": 1.0, "ho_lo": 1.0}
BUILD = {"truong": truong, "cung": cung, "phien": phien, "ho_lo": ho_lo}


def ids():
    return ["%s_%d" % (t, g) for t in TYPES for g in range(1, 9)]


def build(wid):
    t, g = wid.rsplit("_", 1)
    g = int(g)
    B = Builder(wid, palette(t, g))
    BUILD[t](B, g)
    obj = B.finish()
    from mathutils import Matrix
    k = 2.1 if g >= 6 else 1.8
    if t == "truong":  # chibi-thick shaft: widen only the pole, not the head ornaments
        for v in obj.data.vertices:
            if v.co.z < 0.74 and (v.co.x ** 2 + v.co.y ** 2) ** 0.5 < 0.065:
                v.co.x *= k
                v.co.y *= k
    obj.data.transform(Matrix.Diagonal((SCALE[t] * XY[t], SCALE[t] * XY[t], SCALE[t], 1.0)))
    return obj
