"""Abode garden art (props/garden.png): beds, six spirit-herb families x six growth stages x four rarities, seed packets, tag,
eggs, decorations. Sprite pixels like wt_village (see its docstring); frames 48x48 for plants (2x the old 24x24).
"""
from __future__ import annotations

import math
import random

import bpy
import bmesh
from mathutils import Vector

import wt_common as C
from wt_common import mat
import wt_village as V
from wt_village import X, Y, Z, bx, cy, bl, tubep, shadow

RARITIES = ("common", "rare", "epic", "legendary")
FAMILIES = ("herb", "flower", "root", "vine", "shroom", "shrub")
FAMILY_VI = {"herb": "Linh thảo lá", "flower": "Linh hoa", "root": "Linh căn", "vine": "Linh đằng", "shroom": "Linh chi", "shrub": "Linh quả"}
HT = (0, 11, 20, 28, 34, 38)                      # height of each stage in sprite px
ACC = {"common": ("blossom", 1), "rare": ("water", 3), "epic": ("violet", 2), "legendary": ("yellow", 2)}
GLOW = {"rare": "glow_b", "epic": "crys_v", "legendary": "glow_y"}


def acc(rar, step=0, glow=0.0):
    ramp, base = ACC[rar]
    if glow and rar in GLOW:
        return mat(GLOW[rar], 2, emit=glow, prio=2.0)
    return mat(ramp, min(3, base + step))


def sway(f, z):
    return (1.3 if f else -1.3) * (max(z, 0) / 38.0) ** 1.4


def leaf(col, x0, d0, z0, dx, dz, w, m, dd=0.0):
    import wt_common
    wt_common.blade(col, "leaf", (X(x0), Y(d0), Z(z0)), (X(x0 + dx), Y(d0 + dd), Z(z0 + dz)), X(w), m, bend=Z(1.2))


def mound(col, w=15.0, h=5.0):
    bl(col, 0, 3, h / 2 - 0.5, w / 2, h / 2 + 0.5, mat("dirt", 1), sub=1, ry=w * 0.3)
    bl(col, -3, 2.0, h * 0.8, 3, 1.6, mat("dirt", 2), sub=1)
    bx(col, 0, 0, 0, 0.1, 0.1, 0.1, mat("dirt", 1))


def sparkles(col, rar, f, z0, n=3, r=9):
    if rar == "common":
        return
    for k in range(n):
        a = f * 1.3 + k * 2.1
        bl(col, r * math.cos(a), 3 + 2 * math.sin(a), z0 + 5 * math.sin(a * 1.7) + k * 3, 0.9, 0.9,
           mat(GLOW[rar], 3, emit=2.4, prio=4.0), sub=1)


def seed_stage(col, f):
    mound(col)
    g = 1.6 if f else 0.9
    bl(col, 1, 2.4, 6.2, g, g, mat("glow_y", 2, emit=1.8, prio=4.0), sub=1)


def fam_herb(col, s, rar, f):
    n, L = (0, 3, 5, 7, 8, 9)[s], (0, 7, 11, 14, 15, 16)[s]
    mound(col, 13)
    for k in range(n):
        a = k * 2 * math.pi / n + 0.4
        dx, dd = math.cos(a) * L * 0.95, math.sin(a) * L * 0.4
        dz = L * (0.5 + 0.2 * math.sin(a * 2)) + 2
        leaf(col, 0, 3, 3, dx + sway(f, dz + 3), dz, 6.0 + s * 0.8, mat("foliage", 1 if dd < 0 else 2), dd)
    if s >= 3:
        h = HT[s]
        tubep(col, [(0, 3, 4), (sway(f, h * .5), 3, h * .5), (sway(f, h), 3, h)], 1.3, mat("foliage", 1), seg=5)
        top = sway(f, h)
        if s == 3:
            bl(col, top, 3, h + 2, 2.6, 3.4, acc(rar), sub=1)
        else:
            for k in range(6 if s == 5 else 5):
                a = k * 2 * math.pi / (6 if s == 5 else 5)
                bl(col, top + math.cos(a) * (3.6 + (s == 5)), 3 + math.sin(a) * 2, h + 2 + math.sin(a) * 1.2, 2.2 + (s == 5) * .6, 2.6,
                   acc(rar, 1 if k % 2 else 0, glow=1.0 if s == 5 else 0), sub=1)
            bl(col, top, 3, h + 2.5, 1.9, 1.9, mat("glow_y", 2, emit=1.4 if s == 5 else 0.0) if s == 5 else mat("gold", 2), sub=1)
    if s >= 4:
        sparkles(col, rar, f, HT[s], 3 if s == 4 else 5)


def fam_flower(col, s, rar, f):
    mound(col, 12)
    h = HT[s]
    if s >= 1:
        tubep(col, [(0, 3, 4), (sway(f, h * .5), 3, h * .5), (sway(f, h), 3, h)], 1.5 + 0.12 * s, mat("jade", 1), seg=5)
        for k in range(min(4, 1 + s)):
            z = 5 + k * h * 0.22
            sd = -1 if k % 2 else 1
            leaf(col, sway(f, z) * 0.6, 3, z, sd * (6 + s), 4 + s * 0.4, 4.6, mat("jade", 2 if k % 2 else 1))
    if s == 3:
        bl(col, sway(f, h), 3, h + 3, 3.2, 4.4, acc(rar), sub=1)
        for sd in (-1, 1):
            leaf(col, sway(f, h), 3, h - 1, sd * 3, 3, 2, mat("jade", 2))
    if s >= 4:
        top = sway(f, h)
        np_ = 6 if s == 4 else 8
        for k in range(np_):
            a = k * 2 * math.pi / np_
            r = 5.0 if s == 4 else 7.0
            leaf(col, top, 3, h + 1, math.cos(a) * r, 2.5 + 2.2 * math.sin(a), 3.6 if s == 4 else 4.4, acc(rar, k % 2, glow=1.2 if s == 5 else 0),
                 math.sin(a) * 2.2)
        bl(col, top, 2.5, h + 2.5, 2.0, 2.0, mat("glow_y", 2, emit=1.6) if s == 5 else mat("gold", 2), sub=1)
        sparkles(col, rar, f, h, 3 if s == 4 else 5)


def fam_root(col, s, rar, f):
    mound(col, 13)
    if s >= 1:
        n = (0, 2, 3, 3, 4, 4)[s]
        for k in range(n):
            a = (k - (n - 1) / 2) * 0.85
            h = HT[s] * (0.55 + 0.1 * (k % 2))
            x1 = math.sin(a) * h * 0.55 + sway(f, h)
            tubep(col, [(0, 3, 4), (x1 * 0.5, 3 + k % 2, h * 0.5), (x1, 3 + k % 2, h)], 0.7, mat("olive", 1), seg=4)
            for j in range(3 if s >= 2 else 1):
                aj = j * 2.1 + k
                leaf(col, x1, 3 + k % 2, h, math.cos(aj) * (3 + s), 2 + s * 0.6, 3.0 + s * 0.4, mat("foliage", 1 + (j % 2)), math.sin(aj))
    if s >= 4:
        top = sway(f, HT[s] * 0.6)
        for k in range(4 if s == 4 else 6):
            bl(col, top + (k % 3 - 1) * 2.4, 3 + k // 3, HT[s] * 0.6 + 4 + (k // 3) * 1.6, 1.5, 1.5, acc(rar, 0, glow=1.2 if s == 5 else 0), sub=1)
    if s == 5:
        bl(col, 0, 1.0, 5.2, 5.2, 4.8, mat("paper", 2), sub=1)                  # the ginseng-like root crowns out of the soil
        for k in range(3):
            tubep(col, [(-3 + k * 3, 0.2, 3), (-4 + k * 3.6, -0.5, 0.6)], 0.5, mat("paper", 1), seg=4)
        sparkles(col, rar, f, 18, 4)


def fam_vine(col, s, rar, f):
    mound(col, 12)
    h = HT[s]
    if s >= 1:
        tubep(col, [(0, 3, 3), (0, 3, h + 3)], 0.9, mat("wood", 1), seg=4)
        if s >= 2:
            bx(col, 0, 2, h + 2, 8, 2, 1.6, mat("wood", 1))
        turns = 1 + s * 0.45
        pts = []
        for i in range(14):
            t = i / 13
            a = t * turns * 2 * math.pi
            z = 4 + t * (h - 2)
            pts.append((math.cos(a) * 3.6 + sway(f, z), 3 + math.sin(a) * 1.8, z))
        tubep(col, pts, 0.75, mat("jade", 1), seg=4)
        for i in range(2, 14, 3 - (s >= 3)):
            px, pd, pz = pts[i]
            leaf(col, px, pd, pz, (4 if i % 2 else -4), 2.0, 3.0, mat("jade", 2), 0)
    if s >= 3:
        n = {3: 3, 4: 5, 5: 8}[s]
        for k in range(n):
            px, pd, pz = pts[3 + k * 10 // n]
            if s == 3:
                bl(col, px, pd - 1, pz, 1.6, 2.0, acc(rar), sub=1)
            else:
                C.cyl(bpy.data.collections[-1] if False else col, "bell", (X(px), Y(pd - 1), Z(pz - 2.5)), X(0.9), X(2.4), Z(4.5),
                      acc(rar, k % 2, glow=1.1 if s == 5 else 0), seg=6)
    if s >= 4:
        sparkles(col, rar, f, h * 0.8, 3 if s == 4 else 5)


def fam_shroom(col, s, rar, f):
    mound(col, 14)
    n = (0, 3, 3, 4, 5, 6)[s]
    sizes = (0, 2.2, 3.6, 5.0, 6.2, 7.2)[s]
    pos = [(-5, 2), (4, 3), (0, 4.5), (-9, 4), (8, 1.5), (-2, 0.5)]
    for k in range(n):
        x, d = pos[k]
        r = sizes * (1.0 - 0.18 * (k % 3))
        h = r * (1.0 + 0.5 * (k % 2)) + 1
        cy_ = r * 0.35
        cy(col, x + sway(f, h) * 0.3, d, 3, max(0.8, r * 0.28), h, mat("cream", 2), seg=6)
        capm = acc(rar, 0 if k % 2 else 1, glow=1.0 if s >= 4 else 0) if (rar != "common" or s != 1) else mat("paper", 2)
        if rar == "common":
            capm = mat("shroom", 1 if k % 2 else 2)
        bl(col, x + sway(f, h), d, 3 + h, r, r * 0.65, capm, sub=1, ry=r * 0.9)
        if s >= 3 and k % 2 == 0:
            for j in range(3):
                bl(col, x + sway(f, h) + (j - 1) * r * 0.5, d - r * 0.5, 3 + h + r * 0.45, 0.75, 0.75, mat("white", 3), sub=1)
    if s >= 4:
        sparkles(col, rar, f, HT[s] * 0.6, 3 if s == 4 else 5, 10)
    if s == 5 and rar == "common":
        for k in range(3):
            bl(col, -6 + k * 6, 3, 18 + k * 3, 0.9, 0.9, mat("glow_y", 3, emit=2.0, prio=4.0), sub=1)


def fam_shrub(col, s, rar, f):
    mound(col, 14)
    R = (0, 4.5, 7.5, 10, 12, 13)[s]
    if s >= 1:
        rnd = random.Random(7)
        n = (0, 2, 5, 8, 9, 9)[s]
        for k in range(n):
            a = k * 2 * math.pi / n + 0.5
            r = R * (0.45 + 0.2 * (k % 2))
            x, d = math.cos(a) * R * 0.55, 3 + math.sin(a) * 2
            z = 3 + R * (0.55 + 0.35 * math.sin(a + 1.0)) + 1
            bl(col, x + sway(f, z) * 0.7, d, z, r, r * 0.9, mat("foliage", 0 if z < R * 0.55 else (1 if k % 3 else 2)), sub=1, ry=r)
        bl(col, sway(f, R) * 0.6, 3, 3 + R * 0.9, R * 0.55, R * 0.55, mat("foliage", 1), sub=1)
    if s >= 3:
        for k in range(5 if s == 3 else 7):
            a = k * 1.7 + 0.3
            x, z = math.cos(a) * R * 0.7 + sway(f, 3 + R), 3 + R * (0.7 + 0.4 * math.sin(a * 1.3))
            if s == 3:
                bl(col, x, 0.5 + math.sin(a), z, 1.4, 1.4, acc(rar), sub=1)
            elif s == 4:
                bl(col, x, 0.5 + math.sin(a), z, 1.7, 1.7, mat("foliage", 3), sub=1)
            else:
                bl(col, x, 0.5 + math.sin(a), z, 2.2, 2.2, acc(rar, k % 2, glow=1.2), sub=1)
    if s >= 4:
        sparkles(col, rar, f, R, 3 if s == 4 else 5, 11)


BUILD = {"herb": fam_herb, "flower": fam_flower, "root": fam_root, "vine": fam_vine, "shroom": fam_shroom, "shrub": fam_shrub}


def plant_builder(fam, s, rar):
    def b(col, f):
        shadow(col, 0, 3, 9 + s, 5)
        if s == 0:
            seed_stage(col, f)
        else:
            BUILD[fam](col, s, rar, f)
    return b


# --------------------------------------------------------------------------- beds
def tb(col, cx, d, z0, w, dd, h, m, bevel=0.0, rot=0.0):
    """Box for the top-down beds: x and y both in sprite px (no depth foreshortening)."""
    return C.box(col, "b", (X(cx), X(d), Z(z0 + h / 2)), (X(w), X(dd), Z(h)), m, rot_z=rot, bevel=X(bevel))


def tbl(col, cx, d, zc, rx, rz, m, ry=None, rough=0.0):
    return C.blob(col, "o", (X(cx), X(d), Z(zc)), (X(rx), X(ry if ry is not None else rx), Z(rz)), m, seed=3, rough=rough, subdiv=1, smooth=True)


def bed_locked(col, f=0):
    tb(col, 0, 0, 0, 62, 62, 1, mat("grass", 0), bevel=0.4)
    rnd = random.Random(3)
    for k in range(9):                                       # weeds
        x, d = rnd.uniform(-24, 24), rnd.uniform(-24, 24)
        tbl(col, x, d, 3, rnd.uniform(3, 5), rnd.uniform(3, 5), mat("foliage", rnd.choice((0, 1, 2))), ry=4)
    for (x, d, r) in ((-18, -14, 7), (16, 10, 8), (-4, 18, 6), (20, -20, 5)):     # rocks
        tbl(col, x, d, r * 0.6, r, r * 0.7, mat("stone", 1), ry=r * 0.8, rough=0.2)
        tbl(col, x - r * 0.2, d, r * 0.9, r * 0.6, r * 0.45, mat("stone", 2), ry=r * 0.5)
    for k in range(10):                                      # a ragged rim of stones
        a = k * 0.628
        tbl(col, 27 * math.cos(a), 27 * math.sin(a), 2, 3.2, 2.2, mat("stone", 1), ry=3)


def bed_open(col, f=0, dry=False):
    wood = mat("wood", 1)
    for (x, d, w, h) in ((0, -29, 62, 4), (0, 29, 62, 4), (-29, 0, 4, 62), (29, 0, 4, 62)):
        tb(col, x, d, 0, w, h, 5, wood, bevel=0.6)
    tb(col, 0, 0, 0, 56, 56, 2, mat("earth", 2) if dry else mat("dirt", 1), bevel=0.4)
    rnd = random.Random(11)
    for k in range(5):                                       # furrows
        tb(col, 0, -21 + k * 10.5, 2, 52, 4.0, 1.6, mat("earth", 2) if dry else mat("dirt", 2), bevel=0.6)
        tb(col, 0, -18.5 + k * 10.5, 2, 52, 1.2, 1.0, mat("earth", 0) if dry else mat("dirt", 0))
    for k in range(10 if dry else 6):
        x, d = rnd.uniform(-23, 23), rnd.uniform(-23, 23)
        if dry:
            tb(col, x, d, 3, rnd.uniform(5, 11), 0.9, 0.9, mat("earth", 0), rot=rnd.uniform(0, 3))
        else:
            tbl(col, x, d, 3, 1.6, 1.0, mat("dirt", 0), ry=1.2)
    for (x, d) in ((-29, -29), (29, -29), (-29, 29), (29, 29)):
        tb(col, x, d, 0, 5, 5, 7, mat("wood", 0), bevel=0.7)


# --------------------------------------------------------------------------- seeds, tag, eggs, decorations
def seed_packet(rar):
    def b(col, f):
        shadow(col, 0, 2, 8, 3)
        z = (0, 1.2, 0)[f % 3]
        bl(col, 0, 3, 7 + z, 7.5, 7.5, mat("paper", 2), sub=1, ry=4)
        bx(col, 0, 1.2, 12 + z, 9, 2.4, 2.4, mat("paper", 1), bevel=0.6)               # folded top
        bx(col, 0, 0.6, 7 + z, 1.2, 1.2, 9, mat("wood", 0))
        ramp, step = ACC[rar]
        bl(col, 0, 0.3, 7.5 + z, 3.1, 3.1, mat(ramp, step), sub=1, ry=1.2)                # seal in the rarity colour
        if rar != "common":
            bl(col, 0, -0.5, 7.5 + z, 1.2, 1.2, mat(GLOW[rar], 3, emit=2.0, prio=3.0), sub=1)
        if f == 1:
            bl(col, 6, 1, 12, 0.9, 0.9, mat("glow_y", 3, emit=2.5, prio=4.0), sub=1)
    return b


def tag_build(col, f):
    shadow(col, 0, 2, 6, 3)
    bx(col, 0, 3, 0, 2.6, 2.6, 18, mat("wood", 1), bevel=0.4)
    bx(col, 0, 1.5, 9, 18, 1.6, 15, mat("paper", 2), bevel=0.6)
    bx(col, 0, 0.8, 21, 3, 1.0, 1.4, mat("red", 1))
    for k in range(3):                                       # three blank ruling lines, no writing
        bx(col, 0, 0.6, 12 + k * 3.4, 12, 0.5, 0.7, mat("paper", 1))


def egg_build(rar):
    def b(col, f):
        shadow(col, 0, 3, 9, 4)
        ramp, step = ACC[rar] if rar != "common" else ("bone", 2)
        shell = mat(ramp, step)
        if f == 0:
            bl(col, 0, 3, 12, 9.5, 12.5, shell, sub=2, ry=7)
            bl(col, -3, 0.3, 17, 2.6, 3.4, mat(ramp, min(3, step + 1)), sub=1)
            for k in range(3):
                bx(col, -4 + k * 4, -3, 8, 2.2, 0.8, 2.2, mat(ramp, max(0, step - 1)))
        elif f == 1:
            bl(col, 0, 3, 12, 9.5, 12.5, shell, sub=2, ry=7)
            tubep(col, [(-8, 0, 12), (-4, 0, 16), (0, 0, 11), (4, 0, 16), (8, 0, 12)], 0.8, mat("basalt", 0), seg=4)
        else:
            bl(col, 0, 3, 8, 9.5, 7.5, shell, sub=2, ry=7)
            bl(col, 0, 3, 12.5, 7.5, 3.2, mat("glow_y", 2, emit=1.6), sub=1, ry=5)
            bl(col, 7, 2, 22, 4.6, 4.6, shell, sub=1, ry=3)
    return b


def lotus_bowl(col, f):
    shadow(col, 0, 3, 12, 5)
    cy(col, 0, 5, 0, 11, 8, mat("stone", 1), seg=14, r1=12)
    cy(col, 0, 5, 8, 11, 1.2, mat("water", 1), seg=14)
    for k in range(5):
        a = k * 2 * math.pi / 5 + f * 0.2
        bl(col, math.cos(a) * 5, 5 + math.sin(a) * 2.5, 12.5, 3.6, 2.4, mat("foliage", 1 + k % 2), sub=1, ry=3)
    for k in range(3):
        leaf(col, (k - 1) * 3, 5, 9.5, (k - 1) * 2, 7, 3.6, mat("blossom", 1 + (k != 1)), 0)
    bl(col, 0, 5, 12.5, 1.6, 1.6, mat("glow_y", 2, emit=1.2), sub=1)


def wind_chime(col, f):
    shadow(col, 0, 2, 6, 3)
    sw = (-1.2, 0, 1.2, 0)[f % 4]
    bx(col, 0, 2, 33, 14, 2, 2, mat("wood", 1))
    bx(col, 0, 2.5, 25, 1, 1, 9, mat("wood", 0))
    cy(col, 0, 2.5, 25, 1.5, 4, mat("gold", 2), seg=6, r1=4)
    for k, (x, ln) in enumerate(((-5, 12), (0, 16), (5, 10))):
        o = sw * (1 if k % 2 else -1)
        tubep(col, [(x, 2.5, 33), (x + o, 2.5, 33 - ln)], 0.45, mat("steel", 2), seg=4)
        bl(col, x + o, 2.5, 33 - ln - 1, 1.1, 1.1, mat("gold", 3, emit=0.0), sub=1)
    bl(col, 0, 2.5, 6, 3, 2.2, mat("gold", 2), sub=1)


def banner_pole(col, f):
    shadow(col, 0, 2, 6, 3)
    sw = (0, 1.5, 0, -1.5)[f % 4]
    bx(col, 0, 2, 0, 2.6, 2.6, 49, mat("wood", 1), bevel=0.4)
    bl(col, 0, 2.4, 51, 2.2, 2.2, mat("gold", 2), sub=1)
    pts = [(1, 2, 44), (6 + sw * .3, 1.5, 43), (11 + sw, 1, 41)]
    for k in range(7):
        t = k / 6
        x = 1.5 + t * 10 + sw * t
        bx(col, x, 1, 24 + t * 2 - (t * t) * 2 + sw * 0.4 * t, 2.4, 0.8, 19 - t * 3 + (1 if k % 2 else -1) * 0.5, mat("red", 1 if k % 2 else 2), bevel=0.2)
    bl(col, 5, 0.2, 34, 1.6, 1.6, mat("gold", 2), sub=1)


def specs():
    out = []
    mk = lambda **k: out.append(k)
    mk(name="plot_locked", W=64, H=64, mode="top", build=bed_locked, vi="Luống đất hoang", pivot=(32, 64),
       extra={"old": "plot_bed(True)"})
    mk(name="plot_open", W=64, H=64, mode="top", build=lambda c, f: bed_open(c, f, False), vi="Luống đất", pivot=(32, 64),
       extra={"old": "plot_bed(False)"})
    mk(name="plot_dry", W=64, H=64, mode="top", build=lambda c, f: bed_open(c, f, True), vi="Luống đất khô cằn", pivot=(32, 64),
       extra={"old": "plot_bed(False) when the plant is withered"})
    for fam in FAMILIES:
        for s in range(6):
            rs = ("common",) if s < 3 else RARITIES
            for rar in rs:
                nm = f"{fam}_{s}" if s < 3 else f"{fam}_{s}_{rar}"
                mk(name=nm, W=48, H=48, frames=2, base=4, ppm=40, build=plant_builder(fam, s, rar), vi=f"{FAMILY_VI[fam]}, giai đoạn {s}",
                   extra={"family": fam, "stage": s, "rarity": rar if s >= 3 else None})
    for rar in RARITIES:
        mk(name=f"seed_{rar}", W=32, H=32, frames=3, base=5, ppm=40, build=seed_packet(rar), vi="Túi hạt giống", extra={"rarity": rar, "old": "seed_frames"})
    mk(name="tag", W=26, H=26, base=3, ppm=38, build=tag_build, vi="Thẻ tên cây")
    for rar in RARITIES:
        mk(name=f"egg_{rar}", W=24, H=32, frames=3, base=4, ppm=36, build=egg_build(rar), vi="Trứng ong", extra={"rarity": rar})
    mk(name="hoa_sen", W=28, H=24, frames=4, base=3, ppm=40, build=lotus_bowl, vi="Chậu sen", extra={"old": "decoration('hoa_sen')"})
    mk(name="chuong_gio", W=20, H=36, frames=4, base=2, ppm=34, build=wind_chime, vi="Chuông gió", extra={"old": "decoration('chuong_gio')"})
    mk(name="co_phuong", W=20, H=52, frames=4, base=2, ppm=36, build=banner_pole, vi="Cờ phướn", extra={"old": "decoration('co_phuong')"})
    return out
