"""Nature props (props/nature.png). Modelled in metres, pivot on the ground at the origin,
rendered with the standard camera (35 degrees, light from the upper left), 1 m of height = 36 px.
"""
from __future__ import annotations

import json
import math
import random

import bpy
import bmesh
from mathutils import Vector

import wt_common as C
from wt_common import mat, blob, cyl, cone, tube, blade, box, poly_flat, plane, SS


def rng(*k):
    return random.Random("|".join(map(str, k)))


# --------------------------------------------------------------------------- helpers
def crown(col, c, r, ramp, n, seed, flat=0.8, steps=(0, 1, 2), size=(0.45, 0.7), spread=1.0, smooth=True, emit=0.0):
    """A leafy mass: n blobs inside a squashed sphere. Low blobs are dark, high/left ones light."""
    rnd = rng("crown", seed)
    cx, cy, cz = c
    for i in range(n):
        a = rnd.uniform(0, 6.283)
        e = rnd.uniform(-0.2, 1.0) if i else 0.6
        d = rnd.uniform(0.15, 1.0) * r * spread
        x = cx + math.cos(a) * d * math.cos(e) * 0.9
        y = cy + math.sin(a) * d * math.cos(e) * 0.6
        z = cz + math.sin(e) * r * flat * rnd.uniform(0.3, 1.0)
        # lighter towards the upper left of the screen (-x, +z), darker low and right
        t = (-(x - cx) / r + (z - cz) / (r * flat)) * 0.5
        st = steps[0] if t < -0.25 else (steps[1] if t < 0.3 else steps[2])
        s = rnd.uniform(*size) * r
        blob(col, "puff", (x, y, z), (s, s * 0.9, s * 0.85), mat(ramp, st, emit=emit), seed=rnd.randrange(999),
             rough=0.15, subdiv=2, smooth=smooth)


def trunk(col, pts, radii, ramp="bark", step=1):
    return tube(col, "trunk", pts, radii, mat(ramp, step), seg=7, smooth=True)


def leaf(col, base, ang, ln, wd, material, droop=0.0, rise=0.0):
    x, y, z = base
    tip = (x + math.cos(ang) * ln, y + math.sin(ang) * ln * 0.7, z + rise - droop)
    blade(col, "leaf", base, tip, wd, material, bend=0.04)


def ring_points(n, r, ph=0.0):
    return [(math.cos(ph + 6.283 * i / n) * r, math.sin(ph + 6.283 * i / n) * r) for i in range(n)]


# --------------------------------------------------------------------------- bamboo
def bamboo(col, v):
    rnd = rng("bamboo", v)
    n = (4, 5, 3)[v]
    hs = [(1.55, 1.35, 1.2, 1.45, 1.1), (1.35, 1.6, 1.15, 1.25, 1.0), (1.5, 1.25, 1.38)][v]
    for i in range(n):
        ang = i * 6.283 / n + v
        x, y = math.cos(ang) * 0.12 * (1 if i else 0.2), math.sin(ang) * 0.07
        h = hs[i]
        lean = (rnd.uniform(-0.05, 0.05), rnd.uniform(-0.02, 0.02))
        pts = [(x + lean[0] * k / 6 * h, y + lean[1] * k / 6 * h, h * k / 6) for k in range(7)]
        tube(col, "culm", pts, [0.046, 0.044, 0.041, 0.038, 0.034, 0.03, 0.022], mat("jade", 2 if i % 2 else 1), seg=6, smooth=True)
        for k in range(1, 6):                                   # nodes
            px, py, pz = pts[k]
            cyl(col, "node", (px, py, pz - 0.015), 0.056, 0.056, 0.03, mat("jade", 0), seg=6)
        # leaf sprays at the upper nodes
        for k in (3, 4, 5, 6):
            px, py, pz = pts[k]
            for j in range(3 if k < 6 else 4):
                a = rnd.uniform(0, 6.283)
                st = rnd.choice((1, 2, 2, 3))
                leaf(col, (px, py, pz), a, rnd.uniform(0.3, 0.46), 0.11, mat("jade" if st < 3 else "olive", st if st < 3 else 2),
                     droop=rnd.uniform(0.04, 0.16), rise=0.02)
    cyl(col, "base", (0, 0, 0), 0.16, 0.1, 0.05, mat("foliage", 0), seg=8)


# --------------------------------------------------------------------------- trees
def pine(col, v):
    h = (1.75, 1.45)[v]
    trunk(col, [(0, 0, 0), (0.0, 0, h * 0.3), (0.01, 0, h * 0.55)], [0.075, 0.055, 0.03])
    tiers = 4 if v == 0 else 3
    step = (h - 0.55) / tiers
    for i in range(tiers):
        r = (0.5 - 0.1 * i) * (1.0 if v == 0 else 0.9)
        z0 = 0.28 + i * step
        st = 1 if i % 2 == 0 else 2
        cyl(col, "skirt", (0, 0, z0), r, r * 0.82, 0.1, mat("foliage", 0 if st == 1 else 1), seg=9, smooth=False)
        cone(col, "tier", (0, 0, z0 + 0.1), r * 0.82, step * 1.25 + 0.08, mat("foliage", 0 if st == 1 else 1), seg=9, smooth=False)
    cone(col, "tip", (0, 0, 0.28 + tiers * step - 0.02), 0.1, 0.3, mat("foliage", 1), seg=6)


def broadleaf(col, v):
    rnd = rng("broad", v)
    ramp = ("foliage", "olive")[v]
    th = (0.8, 0.7)[v]
    trunk(col, [(0, 0, 0), (0.02, 0, th * 0.5), (0.0, 0.02, th)], [0.1, 0.075, 0.06])
    for dx in (-0.12, 0.13):                               # roots
        tube(col, "root", [(dx * 0.4, 0, 0.1), (dx, -0.02, 0.0)], [0.045, 0.03], mat("bark", 1), seg=5)
    cz = th + 0.6
    crown(col, (0, 0, cz), 0.62 if v == 0 else 0.7, ramp, 16, 10 + v, flat=0.8, size=(0.45, 0.65), steps=(0, 1, 2))
    # a couple of dark gaps/branches showing through the underside
    blob(col, "under", (0.05, -0.05, th + 0.05), (0.3, 0.22, 0.12), mat(ramp, 0), seed=1, rough=0.1, subdiv=1, smooth=True)


def blossom(col, v=0):
    rnd = rng("blossom")
    trunk(col, [(0, 0, 0), (0.06, 0.0, 0.3), (-0.04, 0.02, 0.6), (0.05, 0.0, 0.85)], [0.1, 0.075, 0.06, 0.04])
    tube(col, "branch", [(0.03, 0, 0.62), (-0.3, 0, 0.9), (-0.45, 0, 1.0)], [0.04, 0.03, 0.02], mat("bark", 2), seg=5)
    tube(col, "branch", [(0.05, 0, 0.72), (0.35, 0, 0.95), (0.5, 0, 1.05)], [0.04, 0.03, 0.02], mat("bark", 1), seg=5)
    crown(col, (0.0, 0, 1.25), 0.72, "blossom", 18, 21, flat=0.7, size=(0.4, 0.6), steps=(0, 1, 1))
    crown(col, (-0.42, 0.0, 1.05), 0.34, "blossom", 6, 22, flat=0.7, size=(0.5, 0.7), steps=(0, 1, 1))
    crown(col, (0.45, 0.0, 1.1), 0.34, "blossom", 6, 23, flat=0.7, size=(0.5, 0.7), steps=(0, 1, 1))
    for i in range(7):                                      # a few bright petals and fallen ones
        a = rnd.uniform(0, 6.283)
        d = rnd.uniform(0.2, 0.7)
        blob(col, "petal", (math.cos(a) * d - 0.05, math.sin(a) * d * 0.6, 1.2 + rnd.uniform(-0.2, 0.5)), (0.07, 0.07, 0.05),
             mat("blossom", 3, emit=0.4), seed=i, rough=0, subdiv=1)
    for i in range(5):
        a = rnd.uniform(0, 6.283)
        d = rnd.uniform(0.25, 0.6)
        blob(col, "fallen", (math.cos(a) * d, math.sin(a) * d * 0.7 - 0.1, 0.01), (0.06, 0.045, 0.01), mat("blossom", 2), seed=i, rough=0, subdiv=1)


def dead_tree(col, v=0):
    rnd = rng("dead")
    m = mat("bark", 1)
    trunk(col, [(0, 0, 0), (0.04, 0, 0.4), (-0.03, 0.02, 0.85), (0.02, 0, 1.3)], [0.11, 0.085, 0.06, 0.03], step=1)
    tube(col, "b1", [(0.0, 0, 0.7), (-0.25, 0, 0.95), (-0.5, 0, 1.2), (-0.62, 0, 1.4)], [0.05, 0.035, 0.02, 0.01], mat("bark", 2), seg=5)
    tube(col, "b2", [(0.01, 0, 0.9), (0.28, 0, 1.15), (0.45, 0, 1.2)], [0.045, 0.03, 0.012], mat("bark", 1), seg=5)
    tube(col, "b3", [(0.0, 0, 1.15), (-0.08, 0.02, 1.5), (-0.2, 0, 1.72)], [0.04, 0.025, 0.01], mat("bark", 2), seg=5)
    tube(col, "b4", [(0.28, 0, 1.15), (0.4, 0, 1.4)], [0.025, 0.01], mat("bark", 1), seg=4)
    for dx in (-0.13, 0.12):
        tube(col, "root", [(dx * 0.4, 0, 0.12), (dx, 0.0, 0.0)], [0.05, 0.03], mat("bark", 0), seg=5)
    blob(col, "hollow", (-0.02, -0.095, 0.45), (0.05, 0.02, 0.1), mat("bark", 0), seed=1, rough=0, subdiv=1)


# --------------------------------------------------------------------------- bushes, rocks, plants
def bush(col, v):
    rnd = rng("bush", v)
    ramp = ("foliage", "grass_d")[v]
    crown(col, (0, 0, 0.17), 0.36, ramp, 9, 30 + v, flat=0.6, size=(0.5, 0.7), steps=(0, 1, 2))
    if v == 1:
        for i in range(6):
            a = rnd.uniform(0, 6.283)
            d = rnd.uniform(0.1, 0.34)
            blob(col, "berry", (math.cos(a) * d - 0.05, math.sin(a) * d * 0.6 - 0.1, 0.18 + rnd.uniform(0, 0.15)), (0.035, 0.035, 0.035),
                 mat("red", 1), seed=i, rough=0, subdiv=1)
    else:
        for i in range(4):
            a = rnd.uniform(0, 6.283)
            d = rnd.uniform(0.15, 0.34)
            blob(col, "bloom", (math.cos(a) * d - 0.05, math.sin(a) * d * 0.6 - 0.08, 0.2 + rnd.uniform(0, 0.12)), (0.04, 0.04, 0.03),
                 mat("white", 2), seed=i, rough=0, subdiv=1)


def rock(col, v):
    rnd = rng("rock", v)
    sizes = [(0.3, 0.22, 0.2), (0.4, 0.28, 0.26), (0.26, 0.2, 0.3)][v]
    ramp = "stone"
    blob(col, "rock", (0, 0, sizes[2] * 0.55), sizes, mat(ramp, 1), seed=40 + v, rough=0.3, subdiv=1)
    blob(col, "rock2", (-sizes[0] * 0.2, 0.0, sizes[2] * 0.9), (sizes[0] * 0.6, sizes[1] * 0.6, sizes[2] * 0.55), mat(ramp, 2), seed=50 + v,
         rough=0.2, subdiv=1)
    if v == 2:
        blob(col, "moss", (-0.05, -0.02, sizes[2] * 1.45), (0.17, 0.12, 0.05), mat("foliage", 1), seed=3, rough=0.15, subdiv=1, smooth=True)
        blob(col, "pebble", (0.32, -0.12, 0.05), (0.09, 0.07, 0.05), mat("stone", 2), seed=3, rough=0.1, subdiv=1)
    elif v == 1:
        blob(col, "pebble", (0.3, 0.0, 0.05), (0.1, 0.07, 0.05), mat("stone", 2), seed=3, rough=0.1, subdiv=1)


def boulder(col, v=0):
    blob(col, "boulder", (0, 0, 0.3), (0.55, 0.4, 0.38), mat("stone", 1), seed=61, rough=0.25, subdiv=1)
    blob(col, "b2", (-0.2, 0.0, 0.5), (0.34, 0.26, 0.25), mat("stone", 2), seed=62, rough=0.25, subdiv=1)
    blob(col, "b3", (0.38, -0.12, 0.12), (0.18, 0.13, 0.12), mat("stone", 1), seed=63, rough=0.2, subdiv=2)
    blob(col, "moss", (-0.12, 0.05, 0.72), (0.28, 0.2, 0.08), mat("foliage", 1), seed=3, rough=0.15, subdiv=2, smooth=True)
    for i in range(3):
        blob(col, "moss2", (0.1 + i * 0.1, -0.2, 0.2 + i * 0.1), (0.07, 0.05, 0.05), mat("foliage", 2), seed=i, rough=0.1, subdiv=1)


def herb(col, v):
    rnd = rng("herb", v)
    if v == 0:      # blue star flower, glowing
        for i in range(5):
            a = i * 1.26 + 0.3
            leaf(col, (0, 0, 0.02), a, 0.2, 0.07, mat("foliage", 2), rise=0.05, droop=0.0)
        tube(col, "stem", [(0, 0, 0.0), (0.01, 0, 0.18), (0, 0.0, 0.3)], [0.012, 0.01, 0.008], mat("foliage", 1), seg=4)
        for i in range(6):
            a = i * 1.047
            blade(col, "petal", (0, 0, 0.32), (math.cos(a) * 0.17, math.sin(a) * 0.12, 0.36), 0.07, mat("glow_b", 1, emit=0.55))
        blob(col, "core", (0, 0, 0.33), (0.045, 0.045, 0.035), mat("glow_y", 2, emit=1.6), seed=1, rough=0, subdiv=1)
    elif v == 1:    # green sprout with glowing buds
        for i in range(7):
            a = i * 0.9 + 0.2
            leaf(col, (0, 0, 0.0), a, 0.22, 0.07, mat("glow_g", 1, emit=0.45), rise=0.2)
        for i in range(3):
            a = i * 2.1 + 0.5
            blob(col, "bud", (math.cos(a) * 0.1, math.sin(a) * 0.06, 0.32 + i * 0.03), (0.04, 0.04, 0.05), mat("glow_g", 2, emit=1.0),
                 seed=i, rough=0, subdiv=1)
    elif v == 2:    # glowing mushroom cluster
        for i, (dx, dy, h, r) in enumerate([(0, 0, 0.26, 0.13), (-0.14, 0.05, 0.17, 0.09), (0.13, 0.02, 0.2, 0.1)]):
            cyl(col, "stem", (dx, dy, 0), 0.03, 0.025, h, mat("cream", 2, emit=0.2), seg=6)
            blob(col, "cap", (dx, dy, h + 0.01), (r, r * 0.9, r * 0.55), mat("glow_p" if i != 1 else "glow_b", 1, emit=0.6), seed=i,
                 rough=0.04, subdiv=2, smooth=True)
            blob(col, "dot", (dx - r * 0.3, dy - r * 0.3, h + r * 0.5), (0.02, 0.02, 0.015), mat("glow_p", 3, emit=2.0), seed=1, rough=0, subdiv=1)
    else:           # golden herb: tall spiky leaves
        for i in range(8):
            a = i * 0.8
            leaf(col, (0, 0, 0.0), a, 0.14 + (i % 3) * 0.04, 0.06, mat("glow_y", 1, emit=0.5), rise=0.26 - (i % 3) * 0.03)
        for i in range(4):
            a = i * 1.6 + 0.4
            blob(col, "seed", (math.cos(a) * 0.1, math.sin(a) * 0.07, 0.3 + (i % 2) * 0.05), (0.03, 0.03, 0.03), mat("glow_y", 2, emit=1.2),
                 seed=i, rough=0, subdiv=1)
    # 1 px sparkles in the glow colour of the herb
    sp = ("glow_b", "glow_g", "glow_p", "glow_y")[v]
    for i in range(3):
        blob(col, "mote", (rnd.uniform(-0.2, 0.2), rnd.uniform(-0.1, 0.1), 0.3 + rnd.uniform(0, 0.28)), (0.017, 0.017, 0.017),
             mat(sp, 3, emit=2.5, prio=4.0), seed=i, rough=0, subdiv=1)


def tall_grass(col, v=0):
    rnd = rng("tall")
    for i in range(14):
        a = rnd.uniform(0, 6.283)
        d = rnd.uniform(0.0, 0.12)
        h = rnd.uniform(0.28, 0.5)
        ln = rnd.uniform(0.04, 0.17)
        blade(col, "blade", (math.cos(a) * d, math.sin(a) * d * 0.6, 0), (math.cos(a) * (d + ln), math.sin(a) * (d + ln) * 0.6, h),
              0.05, mat("foliage", (1, 2, 2, 3, 0)[i % 5], emit=C.lit(0.15)), bend=0.04)


def lotus(col, v=0):
    rnd = rng("lotus")
    for (x, y, r) in [(0.0, 0.0, 0.22), (-0.34, 0.1, 0.17), (0.33, -0.1, 0.19), (0.1, 0.28, 0.14)]:
        cyl(col, "pad", (x, y, 0.0), r, r, 0.02, mat("jade", 2 if r > 0.18 else 1), seg=12)
        poly_flat(col, "notch", [(x, y), (x + r * 1.05, y + r * 0.2), (x + r * 1.05, y - r * 0.2)], 0.03, mat("water", 1))
    for i in range(8):
        a = i * 0.785
        blade(col, "petal", (0.0, 0.0, 0.04), (math.cos(a) * 0.12, math.sin(a) * 0.1, 0.18), 0.07, mat("blossom", 2 if i % 2 else 3))
    blob(col, "heart", (0, 0, 0.1), (0.05, 0.05, 0.04), mat("yellow", 2, emit=0.8), seed=1, rough=0, subdiv=1)


def stump(col, v=0):
    cyl(col, "stump", (0, 0, 0), 0.17, 0.15, 0.26, mat("bark", 1), seg=10, smooth=True)
    cyl(col, "top", (0, 0, 0.255), 0.15, 0.15, 0.02, mat("wood", 3), seg=10)
    cyl(col, "ring", (0, 0, 0.275), 0.085, 0.085, 0.01, mat("wood", 2), seg=10)
    for a in (0.4, 2.6, 4.4):
        tube(col, "root", [(math.cos(a) * 0.1, math.sin(a) * 0.06, 0.1), (math.cos(a) * 0.26, math.sin(a) * 0.16, 0.0)], [0.045, 0.02], mat("bark", 1), seg=5)
    blob(col, "moss", (-0.08, -0.04, 0.2), (0.07, 0.05, 0.05), mat("foliage", 1), seed=1, rough=0.1, subdiv=1, smooth=True)


def log(col, v=0):
    L = 0.9
    t = tube(col, "log", [(-L / 2, 0, 0.13), (L / 2, 0, 0.13)], [0.13, 0.13], mat("bark", 1), seg=9)
    # the cut end faces the viewer's right: a flat disc
    tube(col, "end", [(L / 2 - 0.005, 0, 0.13), (L / 2 + 0.03, 0, 0.13)], [0.118, 0.118], mat("wood", 3), seg=9)
    for i in range(3):
        blob(col, "moss", (-0.25 + i * 0.22, -0.02, 0.255), (0.1, 0.06, 0.035), mat("foliage", 1 if i != 1 else 2), seed=i, rough=0.1, subdiv=1, smooth=True)
    tube(col, "twig", [(-0.1, 0.0, 0.2), (-0.15, 0.2, 0.3)], [0.02, 0.01], mat("bark", 2), seg=4)


def crystal(col, v):
    ramp = ("crys_c", "crys_v")[v]
    base = (("stone", 1), ("slate", 2))[v]
    blob(col, "base", (0, 0, 0.05), (0.3, 0.2, 0.09), mat(base[0], base[1]), seed=70 + v, rough=0.2, subdiv=2)
    spec = [(0.0, 0.0, 0.62, 0.075, 0.0), (-0.14, 0.02, 0.42, 0.06, -0.18), (0.13, 0.0, 0.34, 0.055, 0.2),
            (-0.04, 0.07, 0.26, 0.045, 0.0), (0.06, -0.06, 0.22, 0.04, 0.1)]
    for i, (x, y, h, r, lean) in enumerate(spec):
        cyl(col, "prism", (x, y, 0.06), r, r * 0.85, h * 0.75, mat(ramp, 1 if i % 2 else 2, emit=0.9), seg=6, tilt=(lean, 0))
        top = Vector((x + lean * h * 0.75, y, 0.06 + h * 0.75))
        cone(col, "tip", (top.x, top.y, top.z), r * 0.85, h * 0.28, mat(ramp, 3, emit=1.4), seg=6)


def cloud_puff(col, v):
    rnd = rng("cloud", v)
    n = (6, 8)[v]
    w = (0.45, 0.65)[v]
    for i in range(n):
        x = (i / (n - 1) - 0.5) * 2 * w + rnd.uniform(-0.06, 0.06)
        s = 0.2 + 0.16 * (1 - abs(x) / w) + rnd.uniform(0, 0.05)
        z = s * 0.7 + 0.08
        t = -x / w + 0.2
        blob(col, "puff", (x, rnd.uniform(-0.05, 0.05), z), (s * 1.1, s * 0.9, s * 0.85), mat("cloud", 3 if t > 0.1 else 2), seed=i,
             rough=0.08, subdiv=2, smooth=True)
    blob(col, "under", (0, 0, 0.1), (w * 1.0, 0.2, 0.09), mat("cloud", 1), seed=1, rough=0.05, subdiv=2, smooth=True)


def mushroom_ring(col, v=0):
    rnd = rng("ring")
    for i, (x, y) in enumerate(ring_points(9, 0.38)):
        h = rnd.uniform(0.07, 0.13)
        r = rnd.uniform(0.045, 0.075)
        cyl(col, "stem", (x, y * 0.7, 0), 0.016, 0.014, h, mat("cream", 2), seg=5)
        blob(col, "cap", (x, y * 0.7, h + 0.005), (r, r, r * 0.55), mat("shroom", 1 if i % 3 else 2), seed=i, rough=0.03, subdiv=1, smooth=True)
        blob(col, "dot", (x - r * 0.2, y * 0.7 - r * 0.3, h + r * 0.45), (0.012, 0.012, 0.008), mat("white", 3), seed=1, rough=0, subdiv=1)
    for i in range(10):
        a = i * 0.63
        blob(col, "gleam", (math.cos(a) * 0.38, math.sin(a) * 0.26, 0.02), (0.02, 0.02, 0.012), mat("glow_p", 2, emit=1.6), seed=i, rough=0, subdiv=1)


KIT_PPM = 36.0
# contact shadow half-sizes in metres (before the prop's own scale): (rx, ry)
SHADOWS = {"bamboo_1": (0.3, 0.16), "bamboo_2": (0.3, 0.16), "bamboo_3": (0.26, 0.14), "pine_1": (0.45, 0.26),
           "pine_2": (0.4, 0.24), "tree_1": (0.42, 0.22), "tree_2": (0.46, 0.24), "peach_tree": (0.46, 0.24),
           "dead_tree": (0.3, 0.16), "bush_1": (0.4, 0.2), "bush_2": (0.4, 0.2), "rock_1": (0.3, 0.16),
           "rock_2": (0.42, 0.22), "rock_3": (0.3, 0.17), "boulder": (0.62, 0.34), "stump": (0.24, 0.13),
           "log": (0.5, 0.2), "crystal_1": (0.3, 0.16), "crystal_2": (0.3, 0.16), "linh_thao_1": (0.16, 0.09),
           "linh_thao_2": (0.17, 0.09), "linh_thao_3": (0.2, 0.1), "linh_thao_4": (0.14, 0.08), "tall_grass": (0.14, 0.08)}


# --------------------------------------------------------------------------- registry
# canvas = square px of the render, base = px between the pivot and the canvas bottom
# solid = (dx, dy, w, h) in px relative to the pivot (dy is up, negative = above): footprint that blocks walking
PROPS = [
    dict(id="bamboo_1", scale=0.8, fn=lambda c: bamboo(c, 0), canvas=96, solid=(-6, -4, 12, 4), name="Trúc cao"),
    dict(id="bamboo_2", scale=0.8, fn=lambda c: bamboo(c, 1), canvas=96, solid=(-6, -4, 12, 4), name="Khóm trúc"),
    dict(id="bamboo_3", scale=0.85, fn=lambda c: bamboo(c, 2), canvas=96, solid=(-5, -4, 10, 4), name="Trúc thấp"),
    dict(id="pine_1", scale=0.9, fn=lambda c: pine(c, 0), canvas=96, solid=(-3, -4, 6, 4), name="Cây tùng cao"),
    dict(id="pine_2", scale=0.9, fn=lambda c: pine(c, 1), canvas=96, solid=(-3, -4, 6, 4), name="Cây tùng"),
    dict(id="tree_1", scale=0.82, fn=lambda c: broadleaf(c, 0), canvas=96, solid=(-4, -5, 8, 5), name="Cây lá rộng"),
    dict(id="tree_2", scale=0.82, fn=lambda c: broadleaf(c, 1), canvas=96, solid=(-4, -5, 8, 5), name="Cây lá vàng"),
    dict(id="peach_tree", scale=0.82, fn=blossom, canvas=96, solid=(-4, -5, 8, 5), name="Cây đào"),
    dict(id="dead_tree", scale=0.85, fn=dead_tree, canvas=96, solid=(-4, -5, 8, 5), name="Cây khô"),
    dict(id="bush_1", scale=1.2, fn=lambda c: bush(c, 0), canvas=48, solid=(-8, -5, 16, 5), name="Bụi cây"),
    dict(id="bush_2", scale=1.2, fn=lambda c: bush(c, 1), canvas=48, solid=(-8, -5, 16, 5), name="Bụi quả đỏ"),
    dict(id="rock_1", scale=1.25, fn=lambda c: rock(c, 0), canvas=48, solid=(-8, -5, 16, 5), name="Đá nhỏ"),
    dict(id="rock_2", scale=1.25, fn=lambda c: rock(c, 1), canvas=48, solid=(-9, -6, 18, 6), name="Đá vừa"),
    dict(id="rock_3", scale=1.25, fn=lambda c: rock(c, 2), canvas=48, solid=(-7, -5, 14, 5), name="Đá rêu"),
    dict(id="boulder", scale=1.1, fn=boulder, canvas=64, solid=(-14, -8, 28, 8), name="Tảng đá lớn"),
    dict(id="linh_thao_1", scale=1.9, fn=lambda c: herb(c, 0), canvas=48, solid=None, name="Lam Tinh Thảo"),
    dict(id="linh_thao_2", scale=1.7, fn=lambda c: herb(c, 1), canvas=48, solid=None, name="Thanh Lộ Thảo"),
    dict(id="linh_thao_3", scale=1.8, fn=lambda c: herb(c, 2), canvas=48, solid=None, name="Dạ Quang Nấm"),
    dict(id="linh_thao_4", scale=1.8, fn=lambda c: herb(c, 3), canvas=48, solid=None, name="Kim Tuệ Thảo"),
    dict(id="tall_grass", scale=2.2, fn=tall_grass, canvas=48, solid=None, name="Cỏ cao"),
    dict(id="lotus", scale=1.0, fn=lotus, canvas=64, solid=None, name="Lá sen"),
    dict(id="stump", scale=1.25, fn=stump, canvas=48, solid=(-6, -4, 12, 4), name="Gốc cây"),
    dict(id="log", scale=1.2, fn=log, canvas=64, solid=(-15, -5, 30, 5), name="Thân cây đổ"),
    dict(id="crystal_1", scale=1.35, fn=lambda c: crystal(c, 0), canvas=48, solid=(-7, -4, 14, 4), name="Tinh thạch lam"),
    dict(id="crystal_2", scale=1.35, fn=lambda c: crystal(c, 1), canvas=48, solid=(-7, -4, 14, 4), name="Tinh thạch tím"),
    dict(id="cloud_puff_1", fn=lambda c: cloud_puff(c, 0), canvas=96, solid=None, name="Cụm mây nhỏ"),
    dict(id="cloud_puff_2", fn=lambda c: cloud_puff(c, 1), canvas=96, solid=None, name="Cụm mây lớn"),
    dict(id="mushroom_ring", scale=1.8, fn=mushroom_ring, canvas=48, solid=None, name="Vòng nấm"),
]


def with_shadow(fn, sh):
    def f(col):
        fn(col)
        if sh:
            contact_shadow(col, *sh)
    return f


def contact_shadow(col, rx, ry):
    """One flat darker-grass blob under the prop, a little down-right of the base, no outline ring (kit recipe)."""
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=14, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * rx * 0.8, v.co.y * ry * 0.8, 0.0))
    m = mat("grass", 1, name="MAT_contact_shadow", extra={"kit_outline": 0, "kit_shadow": 2.0, "kit_light": 3.0})
    ob = C.mesh_obj("contact_shadow", bm, m, col)
    ob.location = (rx * 0.18, -ry * 0.22, 0.004)
    return ob


def assets():
    out = []
    for p in PROPS:
        out.append(dict(id=p["id"], w=1, h=1, build=with_shadow(p["fn"], SHADOWS.get(p["id"])), slices=[(p["id"], 0, 0)], group="props",
                        canvas=p["canvas"], base=6, scale=p.get("scale", 1.0), solid=p["solid"], name_vi=p["name"]))
    return out


def render_prop(a, ox, oy, raw_dir, px_dir):
    S, base = a["canvas"], a["base"]
    cam = C.prop_camera(S, base)
    cam.location = Vector((cam.location.x + ox, cam.location.y + oy, cam.location.z))
    sc = C.setup_render(S * SS, S * SS, True)
    for l in bpy.data.lights:
        l.energy = 1.7
    sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.62
    raw = raw_dir / f"{a['id']}.png"
    C.render_png(raw)
    px = C.pixelise(C.load_rgba(raw), S, S, outline=True, ramps=a["ramps"] + ["bark"])
    C.save_png(px, px_dir / f"{a['id']}.png")
    (px_dir / f"{a['id']}.json").write_text(json.dumps(
        {"canvas": S, "pivot": [S // 2, S - base], "solid": a["solid"], "name_vi": a["name_vi"]}), "utf-8")
