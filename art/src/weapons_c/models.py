"""WEAPONS_C models: the six "kỳ binh" (kich, roi, am_khi, luan, phu, cam) x grades 1..8,
built from numbers (runs inside Blender). One function per type; every grade changes the shape.

Convention: grip at the origin, length along +Z, broad side faces -Y (width along X),
1 unit = 1 m, character 1.0 m tall. Root = empty SM_<id>; see geom.py for pose meshes.
"""
import math
import os
import random

import bpy

import geom
from geom import W, wraps, tassel, stars, wings, leaf_pts

NAMES = {1: "Mộc", 2: "Thiết", 3: "Bích Ngọc", 4: "Kim Lam", 5: "Linh Quang", 6: "Hỏa Diệm",
         7: "Băng Dực", 8: "Tinh Không"}
TYPES = ["kich", "roi", "am_khi", "luan", "phu", "cam"]
TYPE_VI = {"kich": "Kích", "roi": "Roi", "am_khi": "Ám Khí", "luan": "Luân", "phu": "Phủ", "cam": "Cầm"}
ALL_IDS = ["%s_%d" % (t, g) for t in TYPES for g in range(1, 9)]

# grade themes (shared with weapons_a / weapons_b): blade, light edge, shaft, fittings, grip, cord, gem, inlay
TH = {
    1: dict(blade="stone", edge="stone_l", haft="wood", trim="wood_d", grip="hemp", cord="hemp", gem=None, hi=None),
    2: dict(blade="iron", edge="steel", haft="wood_d", trim="iron_d", grip="leather", cord="red", gem=None, hi=None),
    3: dict(blade="jade", edge="jade_l", haft="wood_d", trim="bronze", grip="leather", cord="jade", gem="jade_d", hi="jade_d"),
    4: dict(blade="steel", edge="steel_l", haft="iron_d", trim="gold", grip="leather", cord="red", gem="teal", hi="teal"),
    5: dict(blade="cyan", edge="cyan_hi", haft="gold_dk", trim="gold", grip="leather", cord="violet", gem="violet", hi="cyan_hi"),
    6: dict(blade="flame", edge="flame_y", haft="gold_dk", trim="gold_dk", grip="leather", cord="flame", gem="flame_y", hi="flame_y"),
    7: dict(blade="ice", edge="ice_hi", haft="ice_w", trim="gold", grip="leather", cord="cyan", gem="cyan", hi="ice_hi"),
    8: dict(blade="purple", edge="purple_l", haft="purple", trim="gold", grip="leather", cord="violet", gem="star", hi="gold_e"),
}


def shaft(w, key, z0, z1, r, seg=8):
    w.cyl(key, (0, 0, (z0 + z1) / 2), r, r, z1 - z0, seg=seg)


def grip_block(w, g, r, z0=-0.08, z1=0.08, h=0.2):
    T = TH[g]
    w.cyl(T["grip"] if g > 1 else "hemp", (0, 0, 0), r, r, h, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", z0, z1, r, 4)


def mirror(pts):
    return [(-x, z) for x, z in pts][::-1]


# ======================================================================= KICH (halberd, ~1.45 m)
def crescent(s, zc, R, th, alpha=65.0, gap=0.02, x0=0.036, n=12, teeth=0):
    """A ji crescent on side s (+1 = +X): its convex back faces the shaft, the horns point away.
    Returns (back polyline, edge polyline) for W.strip, both bottom -> top."""
    # back: circle radius R centred at cx; edge: a wider circle (R2, centred d further out) that
    # meets the back at the horn tips, `th` thick in the middle -> a true crescent moon
    al = math.radians(alpha)
    d = (2 * R * th - th * th) / (2 * (R * (1 - math.cos(al)) - th))
    R2 = d + R - th
    cx = x0 + gap + R
    back, edge = [], []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        a = al * t
        bx, bz = cx - R * math.cos(a), zc + R * math.sin(a)
        dz = bz - zc
        ex = cx + d - math.sqrt(max(0.0, R2 * R2 - dz * dz))
        ex = max(ex, bx + 0.006)
        if teeth and 0 < i < n and i % 2 == 0:
            ex += teeth
        back.append((s * bx, bz))
        edge.append((s * ex, bz))
    return back, edge


def kich(w, g):
    T = TH[g]
    sk = {1: "wood", 2: "wood_d", 3: "wood_d", 4: "iron_d", 5: "gold_dk", 6: "gold_dk", 7: "ice_w", 8: "purple"}[g]
    base = 1.0
    shaft(w, sk, -0.24, base + 0.04, 0.036)
    grip_block(w, g, 0.03)
    butt = {1: "wood_d", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    w.cyl(butt, (0, 0, -0.25), 0.042, 0.026, 0.06, seg=8)
    if g >= 4:
        w.sph(butt, (0, 0, -0.29), 0.032, seg=6)
    ty = 0.024
    blade, edge = T["blade"], T["edge"]
    # socket collar
    sock = {1: "hemp", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    w.cyl(sock, (0, 0, base + 0.02), 0.048, 0.04, 0.1, seg=8)
    zc = base + 0.12
    # spear point
    tip = {1: 1.42, 2: 1.45, 3: 1.46, 4: 1.5, 5: 1.52, 6: 1.52, 7: 1.52, 8: 1.56}[g]
    hw = {1: 0.06, 2: 0.055, 3: 0.06, 4: 0.05, 5: 0.06, 6: 0.065, 7: 0.055, 8: 0.065}[g]
    if g == 6:      # wavy flame point
        pts = [(0.0, tip), (0.045, tip - 0.12), (0.02, tip - 0.15), (0.065, tip - 0.24), (0.035, tip - 0.27),
               (0.05, base + 0.2), (0.025, base + 0.07)]
        w.poly(blade, mirror(pts) + pts[::-1], -0.016, 0.016, 0.004)
        w.poly(edge, [(0, tip - 0.06), (0.018, tip - 0.2), (0, base + 0.1), (-0.018, tip - 0.2)], -0.022, -0.012, 0)
    else:
        pts = [(hw * 0.4, base + 0.06), (hw, base + 0.12 + (tip - base) * 0.12), (hw * 0.55, tip - 0.1)]
        out = [(-x, z) for x, z in pts] + [(0.0, tip)] + [(x, z) for x, z in pts[::-1]]
        if g == 8:   # violet halo around the point
            w.poly("violet", [(-x * 1.5, z) for x, z in pts] + [(0.0, tip + 0.04)] + [(x * 1.5, z) for x, z in pts[::-1]],
                   0.008, 0.014, 0)
        w.poly(blade, out, -0.015, 0.015, 0.005 if g > 1 else 0.008)
        if g >= 3:   # ridge / core line
            w.poly(T["hi"] if g >= 4 else "jade_d", [(-0.01, base + 0.14), (-0.01, tip - 0.1), (0, tip - 0.06),
                                                    (0.01, tip - 0.1), (0.01, base + 0.14)], -0.022, -0.012, 0)
    # crescent side blades: one ("thanh long kich") up to grade 3, two ("phuong thien kich") from 4
    sides = (1,) if g <= 3 else (1, -1)
    R = {1: 0.17, 2: 0.19, 3: 0.2, 4: 0.19, 5: 0.2, 6: 0.2, 7: 0.19, 8: 0.21}[g]
    th = {1: 0.08, 2: 0.07, 3: 0.075, 4: 0.068, 5: 0.07, 6: 0.065, 7: 0.068, 8: 0.072}[g]
    alpha = {1: 66, 2: 74, 3: 76, 4: 76, 5: 80, 6: 76, 7: 76, 8: 82}[g]
    for s in sides:
        back, ed = crescent(s, zc, R, th, alpha, teeth=0.03 if g == 6 else 0)
        if g == 8:
            b2, e2 = crescent(s, zc, R + 0.015, th + 0.025, alpha, gap=0.0)
            w.strip("violet", b2, [(x + s * 0.0, z) for x, z in e2], 0.008, 0.014)
        w.strip(blade, back, ed, -ty / 2, ty / 2)
        # bright cutting edge along the concave side
        inner = [(x - s * 0.012, z) for x, z in ed]
        if g in (2, 4, 5, 7, 8):
            w.strip(edge if g != 8 else "gold_e", inner, ed, -ty / 2 - 0.004, -ty / 2 + 0.004)
        # two bars tie the crescent to the shaft
        for dz in (-0.05, 0.05):
            w.box(T["trim"] if g > 1 else "hemp", (s * 0.045, 0, zc + dz), (0.05, 0.03, 0.022), bevel=0.003)
        if g == 1:   # hemp lashing over the stone
            w.box("hemp", (s * 0.06, 0, zc), (0.05, 0.034, 0.05), bevel=0.004)
        if g == 7:
            wings(w, "ice_w", zc - 0.14, 3, 0.13, 0.045, rise0=-60, step=18, base_x=0.04, sides=(s,))
    if g == 1:
        w.cyl("hemp", (0, 0, base + 0.09), 0.05, 0.05, 0.03, seg=8)
    # gems, tassels, extras
    if T["gem"] and g >= 3:
        gk = T["gem"]
        if g in (5, 6, 7):
            w.ico(gk, (0, -0.045, zc), 0.028)
        else:
            w.sph(gk, (0, -0.042, zc), 0.032 if g != 3 else 0.022, seg=6)
    if g >= 2:
        tcol = {2: "red", 3: "jade", 4: "red", 5: "violet", 6: "flame", 7: "cyan", 8: "violet"}[g]
        tassel(w, tcol, (0, 0, base - 0.02), n=5, length=0.17 + 0.01 * (g >= 4), spread=0.03)
    if g == 5:
        wings(w, "gold", base + 0.0, 2, 0.13, 0.05, rise0=-40, step=24, base_x=0.04)
        w.sph("cyan_hi", (0, -0.03, tip - 0.2), 0.014, seg=5)
    if g == 6:
        for s in (-1, 1):
            w.cyl("gold_dk", (s * 0.05, 0, base + 0.02), 0.022, 0.0, 0.09, rot=(0, s * 60, 0), seg=4)
    if g == 8:
        stars(w, "star", [(-0.02, 1.3), (0.015, 1.4), (0.0, 1.22), (0.17, zc + 0.12), (-0.17, zc - 0.1)], -0.026, 0.015)


# ======================================================================= PHU (battle axe, ~0.95 m)
def axe_blade(s, hc, x_out, z_top, z_bot, bulge, neck=0.05, x0=0.03, n=10, teeth=0.0):
    """Axe blade outline on side s: neck at the haft, flaring to a convex cutting edge.
    Returns (outline, edge polyline top->bottom)."""
    edge = []
    for i in range(n + 1):
        u = i / n
        z = z_top + (z_bot - z_top) * u
        x = x_out + bulge * math.sin(math.pi * u)
        if teeth and 0 < i < n and i % 2 == 1:
            x += teeth
        edge.append((s * x, z))
    top = [(s * x0, hc + neck), (s * (x0 + (x_out - x0) * 0.45), hc + neck + (z_top - hc - neck) * 0.25)]
    bot = [(s * (x0 + (x_out - x0) * 0.45), hc - neck + (z_bot - hc + neck) * 0.4), (s * x0, hc - neck)]
    out = top + edge + bot
    if s < 0:
        out = out[::-1]
    return out, edge


def edge_band(w, key, edge, s, depth, y0, y1):
    inner = [(x - s * depth, z) for x, z in edge]
    w.strip(key, inner, edge, y0, y1)


def phu(w, g):
    T = TH[g]
    sk = {1: "wood", 2: "wood_d", 3: "wood_d", 4: "iron_d", 5: "gold_dk", 6: "gold_dk", 7: "ice_w", 8: "purple"}[g]
    hc = 0.64
    shaft(w, sk, -0.22, hc + 0.1, 0.032)
    grip_block(w, g, 0.036)
    butt = {1: "wood_d", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    w.sph(butt, (0, 0, -0.23), 0.042, seg=7)
    if g >= 2:
        tassel(w, T["cord"], (0, 0, -0.26), n=3, length=0.13)
    tb = 0.034
    blade, edge = T["blade"], T["edge"]
    # socket (eye of the axe)
    sock = {1: "hemp", 2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    if g == 1:
        # stone wedge lashed to the haft
        out, ed = axe_blade(1, hc, 0.17, hc + 0.08, hc - 0.08, 0.025, neck=0.055)
        w.poly("stone", out, -0.03, 0.03, 0.012)
        w.poly("stone", [(-0.03, hc + 0.05), (-0.03, hc - 0.05), (-0.075, hc - 0.03), (-0.075, hc + 0.03)], -0.026, 0.026, 0.01)
        edge_band(w, "stone_l", ed, 1, 0.022, -0.032, 0.032)
        for dz in (-0.045, 0.0, 0.045):
            w.cyl("hemp", (0, 0, hc + dz), 0.05, 0.05, 0.022, seg=8)
        w.box("hemp", (0.0, 0, hc), (0.07, 0.068, 0.03), rot=(0, 35, 0), bevel=0.004)
        return
    w.box(sock, (0, 0, hc), (0.085, 0.07, 0.16), bevel=0.008)
    if g == 2:    # bearded iron axe
        out, ed = axe_blade(1, hc, 0.21, hc + 0.1, hc - 0.18, 0.03, neck=0.05)
        w.poly(blade, out, -tb / 2, tb / 2, 0.006)
        edge_band(w, edge, ed, 1, 0.024, -tb / 2 - 0.004, tb / 2 + 0.004)
        w.box("iron_d", (-0.065, 0, hc), (0.06, 0.06, 0.07), bevel=0.008)      # hammer poll
        w.cyl("red", (0, 0, hc - 0.12), 0.04, 0.04, 0.03, seg=8)
    elif g == 3:  # round jade crescent, bronze back spike
        out, ed = axe_blade(1, hc, 0.21, hc + 0.16, hc - 0.16, 0.06, neck=0.06)
        w.poly(blade, out, -tb / 2, tb / 2, 0.006)
        edge_band(w, edge, ed, 1, 0.02, -tb / 2 - 0.004, tb / 2 + 0.004)
        w.poly("bronze", [(-0.04, hc + 0.04), (-0.17, hc + 0.0), (-0.04, hc - 0.04)], -0.02, 0.02, 0.004)
        w.sph("jade_d", (0.11, -tb / 2 - 0.004, hc), 0.03, scale=(1, 0.4, 1), seg=8)
        w.cyl("bronze", (0, 0, hc + 0.1), 0.04, 0.03, 0.04, seg=8)
    elif g == 4:  # double-bit steel, gold, teal gem
        for s in (1, -1):
            out, ed = axe_blade(s, hc, 0.19, hc + 0.14, hc - 0.14, 0.045, neck=0.06)
            w.poly(blade, out, -tb / 2, tb / 2, 0.006)
            edge_band(w, edge, ed, s, 0.02, -tb / 2 - 0.004, tb / 2 + 0.004)
            w.box("gold", (s * 0.075, 0, hc), (0.03, tb + 0.012, 0.15), bevel=0.004)
        w.sph("teal", (0, -0.045, hc), 0.04, seg=6)
        w.cyl("gold", (0, 0, hc + 0.13), 0.035, 0.0, 0.1, seg=4)
    elif g == 5:  # glowing crescent, gold back with feather wings
        out, ed = axe_blade(1, hc, 0.22, hc + 0.2, hc - 0.2, 0.06, neck=0.06)
        w.poly(blade, out, -tb / 2, tb / 2, 0.006)
        edge_band(w, edge, ed, 1, 0.022, -tb / 2 - 0.004, tb / 2 + 0.004)
        w.box("gold", (0.06, 0, hc), (0.04, tb + 0.012, 0.16), bevel=0.004)
        wings(w, "gold", hc - 0.02, 3, 0.15, 0.055, rise0=-20, step=26, base_x=0.04, sides=(-1,))
        w.ico("violet", (0, -0.045, hc), 0.032)
        w.cyl("gold", (0, 0, hc + 0.12), 0.03, 0.0, 0.08, seg=4)
    elif g == 6:  # flame: jagged burning edge on blackened gold
        out, ed = axe_blade(1, hc, 0.2, hc + 0.18, hc - 0.18, 0.05, neck=0.06, n=12, teeth=0.035)
        w.poly("gold_dk", out, -tb / 2, tb / 2, 0.006)
        inner = [(x * 0.82, z * 0.97 + hc * 0.03) for x, z in ed]
        w.strip(blade, inner, ed, -tb / 2 - 0.005, tb / 2 + 0.005)
        edge_band(w, edge, [(x * 0.82, z * 0.97 + hc * 0.03) for x, z in ed], 1, 0.018, -tb / 2 - 0.007, -tb / 2 + 0.0)
        for k, dz in enumerate((-0.06, 0.0, 0.06)):
            w.cyl("gold_dk", (-0.08, 0, hc + dz), 0.026, 0.0, 0.1, rot=(0, -90 + (k - 1) * 25, 0), seg=4)
        w.ico("flame_y", (0, -0.045, hc), 0.03)
        for dx, ln in ((-0.02, 0.1), (0.02, 0.14)):
            w.cyl("flame", (dx, 0, hc + 0.1 + ln / 2), 0.03, 0.0, ln, seg=4)
    elif g == 7:  # ice crystal blade, small wings on the back
        out, ed = axe_blade(1, hc, 0.21, hc + 0.17, hc - 0.17, 0.05, neck=0.06)
        w.poly(blade, out, -tb / 2, tb / 2, 0.006)
        edge_band(w, edge, ed, 1, 0.024, -tb / 2 - 0.004, tb / 2 + 0.004)
        w.box("gold", (0.06, 0, hc), (0.035, tb + 0.012, 0.15), bevel=0.004)
        wings(w, "ice_w", hc - 0.02, 3, 0.16, 0.055, rise0=0, step=26, base_x=0.04, sides=(-1,))
        w.ico("cyan", (0, -0.045, hc), 0.028)
        for z, l in ((hc + 0.22, 0.1),):
            w.cyl("ice_hi", (0.0, 0, z - 0.04), 0.03, 0.0, l, seg=4)
    else:         # cosmic double crescent, gold edges, stars
        for s in (1, -1):
            big = s > 0
            out, ed = axe_blade(s, hc, 0.23 if big else 0.16, hc + (0.22 if big else 0.13),
                                hc - (0.22 if big else 0.13), 0.06 if big else 0.04, neck=0.065)
            halo, _ = axe_blade(s, hc, (0.23 if big else 0.16) + 0.02, hc + (0.24 if big else 0.15),
                                hc - (0.24 if big else 0.15), 0.06 if big else 0.04, neck=0.07)
            w.poly("violet", halo, tb / 2 - 0.002, tb / 2 + 0.006, 0)
            w.poly(blade, out, -tb / 2, tb / 2, 0.006)
            edge_band(w, "gold_e", ed, s, 0.02, -tb / 2 - 0.004, tb / 2 + 0.004)
        w.sph("star", (0, -0.045, hc), 0.04, seg=6)
        w.cyl("gold", (0, 0, hc + 0.14), 0.04, 0.0, 0.12, seg=4)
        stars(w, "star", [(0.13, hc + 0.1), (0.17, hc - 0.06), (0.1, hc - 0.14), (-0.1, hc + 0.05)], -tb / 2 - 0.008, 0.015)


# ======================================================================= ROI (whip / nine-section chain whip)
WHIP_LEN = 0.62
H_TOP = 0.15     # top of the handle


def _resample(poly, n):
    """n+1 points evenly spaced along a polyline of (x, z)."""
    d = [0.0]
    for a, b in zip(poly, poly[1:]):
        d.append(d[-1] + math.dist(a, b))
    L = d[-1]
    out = []
    j = 0
    for i in range(n + 1):
        t = L * i / n
        while j < len(d) - 2 and d[j + 1] < t:
            j += 1
        f = (t - d[j]) / max(1e-9, d[j + 1] - d[j])
        a, b = poly[j], poly[j + 1]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out


def whip_path(pose, length=WHIP_LEN):
    """The whip's centre line (x, z) from the top of the handle, ~`length` long."""
    pts = []
    N = 80
    if pose == "lash":        # thrown out straight, a travelling wave toward the tip
        for i in range(N + 1):
            t = i / N
            pts.append((0.035 * math.sin(t * math.pi * 2.2) * t, H_TOP + length * 1.02 * t))
    elif pose == "arc":       # swung back: up and over in a hook, tail trailing down
        R = 0.15
        for i in range(N + 1):
            a = math.radians(200 * i / N)
            pts.append((-R + R * math.cos(a), H_TOP + 0.04 + R * 1.15 * math.sin(a)))
        pts = [(0.0, H_TOP)] + pts
        x, z = pts[-1]
        for i in range(1, 12):
            pts.append((x + 0.004 * i, z - 0.02 * i))
    else:                     # coil: one big loop beside the handle, the tip dangling below
        cx, cz, r = 0.085, H_TOP + 0.02, 0.085
        for i in range(N + 1):
            a = math.radians(180 - 330 * i / N)
            pts.append((cx + r * math.cos(a), cz + r * 1.1 * math.sin(a)))
        x, z = pts[-1]
        for i in range(1, 9):
            pts.append((x - 0.006 * i, z - 0.018 * i))
    return _resample(pts, 200)


def _arc_len(p):
    return sum(math.dist(a, b) for a, b in zip(p, p[1:]))


def roi_body(w, g, pose):
    """The flexible part, built along whip_path(pose). Same segment count for every pose."""
    T = TH[g]
    path = whip_path(pose)
    L = _arc_len(path)
    total = WHIP_LEN
    path = [(x, z) for x, z in path]
    yoff = {"coil": 0.0}.get(pose, 0.0)

    def at(t):                       # point at arc fraction t, and tangent
        k = min(len(path) - 2, int(t * (len(path) - 1)))
        a, b = path[k], path[k + 1]
        f = t * (len(path) - 1) - k
        p = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        d = (b[0] - a[0], b[1] - a[1])
        n = math.hypot(*d) or 1.0
        return p, (d[0] / n, d[1] / n)

    def P(p, i=0):
        # loops of the coil get a little depth so overlapping turns do not z-fight
        y = (-0.012 if (pose == "coil" and i % 2) else 0.0) + yoff
        return (p[0], y, p[1])

    tip_t = 0.9
    if g == 1:   # braided leather rope, tapering, a few knots, hemp tuft
        n = 30
        for i in range(n):
            t0, t1 = tip_t * 1.08 * i / n, tip_t * 1.08 * (i + 1) / n
            (a, _), (b, _) = at(min(t0, 0.99)), at(min(t1, 0.995))
            r0 = 0.032 - 0.014 * t0
            r1 = 0.032 - 0.014 * t1
            w.seg("leather_l" if (i // 3) % 2 else "leather", P(a, i // 6), P(b, i // 6), r0, r1, 7)
        for t in (0.25, 0.55):
            p, _ = at(t)
            w.sph("leather", P(p), 0.026, seg=6)
        p, d = at(0.97)
        tassel_dir(w, "hemp", p, d, 3, 0.07)
        return
    nseg = {2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7}[g]
    seg_key = {2: "iron", 3: "jade", 4: "steel", 5: "cyan", 6: "flame", 7: "ice", 8: "purple"}[g]
    ring_key = {2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold_e"}[g]
    r = {2: 0.028, 3: 0.03, 4: 0.03, 5: 0.03, 6: 0.032, 7: 0.03, 8: 0.032}[g]
    gapt = 0.012 / total
    for i in range(nseg):
        t0, t1 = tip_t * i / nseg + gapt, tip_t * (i + 1) / nseg - gapt
        (a, _), (b, _) = at(t0), at(t1)
        rr = r * (1 - 0.15 * i / nseg)
        w.seg(seg_key, P(a, i), P(b, i), rr, rr, 8)
        if g == 6:     # little flame licks on every other link
            if i % 2:
                (m, d) = at((t0 + t1) / 2)
                nx, nz = -d[1], d[0]
                w.seg("flame_y", P(m, i), P((m[0] + nx * 0.05, m[1] + nz * 0.05), i), 0.016, 0.002, 4)
        p, _ = at(tip_t * (i + 1) / nseg)
        w.sph(ring_key, P(p, i), r * 1.2, seg=6)
    # the dart at the tip
    p, d = at(tip_t)
    ang = math.degrees(math.atan2(d[0], d[1]))
    ln = {2: 0.08, 3: 0.09, 4: 0.1, 5: 0.1, 6: 0.11, 7: 0.1, 8: 0.11}[g]
    wd = {2: 0.03, 3: 0.034, 4: 0.04, 5: 0.036, 6: 0.04, 7: 0.036, 8: 0.042}[g]
    tipk = {2: "steel", 3: "bronze", 4: "steel", 5: "cyan_hi", 6: "flame_y", 7: "ice_hi", 8: "gold_e"}[g]
    w.poly(tipk, leaf_pts(p, ang, ln, wd, widest=0.3, back=0.05), -0.012, 0.012, 0.003)
    if g == 7:
        for s in (-1, 1):
            w.poly("ice_w", leaf_pts(p, ang + 180 + s * 35, 0.07, 0.02), -0.01, 0.01, 0.002)
    if g in (2, 3, 4, 5):    # tassel behind the dart
        tassel_dir(w, {2: "red", 3: "jade", 4: "red", 5: "violet"}[g], at(tip_t - 0.02)[0],
                   (-d[0], -d[1]), 3, 0.06, side=True)
    if g == 8:
        for t in (0.2, 0.45, 0.7):
            p, _ = at(t)
            w.box("star", (p[0] + 0.03, -0.03, p[1] + 0.02), (0.03, 0.024, 0.03), bevel=0)


def tassel_dir(w, key, p, d, n, length, side=False):
    """Little tassel hanging from point p along direction d (or across it if side)."""
    if side:
        d = (-d[1], d[0]) if d[0] >= 0 else (d[1], -d[0])
    for k in range(n):
        a = (k - (n - 1) / 2) * 0.35
        dx = d[0] * math.cos(a) - d[1] * math.sin(a)
        dz = d[0] * math.sin(a) + d[1] * math.cos(a)
        w.seg(key, (p[0], 0, p[1]), (p[0] + dx * length, 0, p[1] + dz * length), 0.008, 0.004, 5)
    w.sph(key, (p[0], 0, p[1]), 0.016, seg=6)


def roi(w, g):
    T = TH[g]
    # handle (shared by all poses)
    hk = {1: "wood", 2: "wood_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    w.cyl(T["grip"] if g > 1 else "hemp", (0, 0, 0.04), 0.03, 0.03, 0.14, seg=8)
    wraps(w, T["cord"] if g > 1 else "wood_d", -0.02, 0.1, 0.03, 4)
    w.cyl(hk, (0, 0, H_TOP - 0.01), 0.026, 0.036, 0.04, seg=8)
    w.sph(hk, (0, 0, -0.045), 0.036, seg=7)
    if g >= 4:
        w.sph(T["gem"], (0, -0.03, -0.045), 0.024, seg=6)
    if g >= 2 and g not in (4,):
        tassel(w, T["cord"], (0, 0, -0.07), n=3, length=0.1)
    for pose in ("coil", "arc", "lash"):
        w.pose = pose
        roi_body(w, g, pose)
    w.pose = None


# ======================================================================= AM KHI (a fan of throwing blades)
def dart(w, g, base, ang, flying=False):
    """One throwing blade along angle `ang` from `base` (x, z), the ring/tail at the base."""
    a = math.radians(ang)
    d = (math.sin(a), math.cos(a))

    def p(t):
        return (base[0] + d[0] * t, base[1] + d[1] * t)
    T = TH[g]
    bl = {1: "wood_l", 2: "iron", 3: "jade", 4: "steel", 5: "cyan", 6: "flame", 7: "ice", 8: "purple"}[g]
    L = {1: 0.3, 2: 0.3, 3: 0.31, 4: 0.32, 5: 0.33, 6: 0.32, 7: 0.32, 8: 0.34}[g]
    if g == 1:   # sharpened bamboo dart, hemp fletching
        h0 = p(0.0)
        w.seg("wood_l", (h0[0], 0, h0[1]), (p(L * 0.8)[0], 0, p(L * 0.8)[1]), 0.016, 0.016, 6)
        w.seg("wood_d", (p(L * 0.8)[0], 0, p(L * 0.8)[1]), (p(L)[0], 0, p(L)[1]), 0.016, 0.002, 6)
        tip = p(0.0)
        for s in (-1, 1):
            w.poly("hemp", leaf_pts(tip, ang + 180 + s * 22, 0.06, 0.016), -0.008, 0.008, 0.002)
        for t in (0.12, 0.62):
            q = p(L * t)
            w.sph("hemp", (q[0], 0, q[1]), 0.02, scale=(1, 1, 0.6), seg=6)
        return
    # ring pommel / tail
    q = p(-0.015)
    ring = {2: "iron_d", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    if g in (3, 4):
        w.tor(ring, (q[0], 0, q[1]), 0.018, 0.007, (0, 1, 0), seg=10, tseg=4)
    # grip
    w.seg(T["grip"] if g != 5 else "gold_dk", (p(0)[0], 0, p(0)[1]), (p(0.07)[0], 0, p(0.07)[1]), 0.014, 0.016, 6)
    # small guard
    if g >= 3:
        gp = p(0.075)
        w.box(ring, (gp[0], 0, gp[1]), (0.055, 0.026, 0.016), rot=(0, ang, 0), bevel=0.003)
    # blade
    if g == 6:   # flame-shaped blade
        base_b = p(0.07)
        w.poly(bl, leaf_pts(base_b, ang, L - 0.07, 0.034, widest=0.25), -0.012, 0.012, 0.003)
        for s in (-1, 1):
            w.poly("flame", leaf_pts(p(0.12), ang + s * 16, 0.12, 0.016), -0.01, 0.01, 0.002)
        w.poly("flame_y", leaf_pts(p(0.1), ang, 0.12, 0.012), -0.02, -0.012, 0)
    elif g == 5:  # glowing needle
        w.poly(bl, leaf_pts(p(0.07), ang, L - 0.07, 0.02, widest=0.15), -0.01, 0.01, 0.002)
        w.poly("cyan_hi", leaf_pts(p(0.09), ang, L - 0.13, 0.008, widest=0.15), -0.016, -0.008, 0)
        q = p(0.0)
        w.ico("violet", (q[0], -0.012, q[1]), 0.018)
    elif g == 7:  # ice shard with a pair of tiny wings at the tail
        w.poly(bl, leaf_pts(p(0.07), ang, L - 0.07, 0.03, widest=0.5), -0.012, 0.012, 0.002)
        w.poly("ice_hi", leaf_pts(p(0.1), ang, L - 0.15, 0.01, widest=0.5), -0.02, -0.012, 0)
        for s in (-1, 1):
            w.poly("ice_w", leaf_pts(p(0.01), ang + 180 + s * 38, 0.08, 0.022), -0.01, 0.01, 0.002)
    elif g == 8:  # star blade
        w.poly(bl, leaf_pts(p(0.07), ang, L - 0.07, 0.034, widest=0.4), -0.012, 0.012, 0.003)
        w.poly("gold_e", leaf_pts(p(0.1), ang, L - 0.14, 0.01, widest=0.4), -0.02, -0.012, 0)
        q = p(0.0)
        w.sph("star", (q[0], -0.012, q[1]), 0.02, seg=6)
        q = p(L * 0.6)
        w.box("star", (q[0] + 0.03, -0.02, q[1]), (0.028, 0.02, 0.028), bevel=0)
    else:         # willow-leaf throwing knife
        wd = {2: 0.036, 3: 0.04, 4: 0.04}[g]
        w.poly(bl, leaf_pts(p(0.07), ang, L - 0.07, wd, widest=0.35), -0.012, 0.012, 0.003)
        if g >= 3:
            w.poly(T["hi"] if g == 4 else "jade_d", leaf_pts(p(0.1), ang, L - 0.15, 0.009, widest=0.35),
                   -0.02, -0.012, 0)
    # tails (cloth streamers) on the ring
    if g in (2, 4):
        tc = {2: "red", 3: "jade", 4: "red"}[g]
        q = p(-0.02)
        for s in (-1, 1):
            w.seg(tc, (q[0], 0, q[1]), (q[0] - d[0] * 0.07 + s * d[1] * 0.025, 0, q[1] - d[1] * 0.07 - s * d[0] * 0.025),
                  0.01, 0.005, 5)
    if flying and g >= 5:     # speed streak behind a flying blade
        sk = {5: "cyan", 6: "flame", 7: "ice", 8: "violet"}[g]
        q0, q1 = p(-0.04), p(-0.2)
        w.seg(sk, (q0[0], 0.01, q0[1]), (q1[0], 0.01, q1[1]), 0.008, 0.001, 4)


def am_khi(w, g):
    n = {1: 3, 2: 3, 3: 4, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}[g]
    spread = {1: 50, 2: 56, 3: 62, 4: 70, 5: 72, 6: 72, 7: 72, 8: 76}[g]
    # in the hand: a fan between the fingers
    w.pose = "hand"
    for k in range(n):
        a = -spread / 2 + spread * k / max(1, n - 1)
        w.xf = geom.Matrix.Translation((0, (k % 2) * 0.012 - 0.006, 0))
        dart(w, g, (math.sin(math.radians(a)) * 0.02, -0.02), a)
    w.xf = geom.Matrix.Identity(4)
    if g >= 4:   # hub ornament where the blades cross
        hub = {4: "teal", 5: "violet", 6: "flame_y", 7: "cyan", 8: "star"}[g]
        w.sph(hub, (0, -0.03, -0.01), 0.022, seg=6)
    # in flight: the blades spread side by side, pointing the same way
    w.pose = "fly"
    for k in range(n):
        off = (k - (n - 1) / 2)
        w.xf = geom.Matrix.Translation((0, (k % 2) * 0.012 - 0.006, 0))
        dart(w, g, (off * 0.075, -abs(off) * 0.05), off * 5.0, flying=True)
    w.xf = geom.Matrix.Identity(4)
    w.pose = None


# ======================================================================= LUAN (chakram)
def luan(w, g):
    T = TH[g]
    R = {1: 0.15, 2: 0.15, 3: 0.16, 4: 0.17, 5: 0.17, 6: 0.17, 7: 0.17, 8: 0.18}[g]
    c = (0.0, R)          # the ring stands on the grip at the origin
    th = 0.028
    ring = {1: "wood", 2: "iron", 3: "jade", 4: "gold", 5: "cyan", 6: "gold_dk", 7: "ice", 8: "purple"}[g]
    rin = R - {1: 0.045, 2: 0.04, 3: 0.04, 4: 0.035, 5: 0.03, 6: 0.04, 7: 0.035, 8: 0.035}[g]
    # grip: wrapped part of the ring at the bottom
    gk = "hemp" if g == 1 else T["grip"]
    w.ring(gk, (c[0], c[1]), rin - 0.006, R + 0.006, -th / 2 - 0.005, th / 2 + 0.005, n=8, a0=240, a1=300)
    if g >= 2:
        for a in (238, 302):
            aa = math.radians(a)
            w.ring(T["cord"] if g != 4 else "gold", (c[0], c[1]), rin - 0.01, R + 0.01, -th / 2 - 0.008, th / 2 + 0.008,
                   n=2, a0=a - 3, a1=a + 3)
    # the wheel
    if g == 1:     # plain bent-wood hoop, hemp lashed in two places
        w.ring("wood", c, rin, R, -th / 2, th / 2, n=28, a0=-60, a1=240)
        for a in (20, 160):
            w.ring("hemp", c, rin - 0.008, R + 0.008, -th / 2 - 0.006, th / 2 + 0.006, n=3, a0=a - 6, a1=a + 6)
        return
    # blades: rout as a function of angle
    if g == 2:       # six short iron teeth
        def ro(a): return R + 0.045 * max(0.0, 1 - abs(((a + 30) % 60) - 30) / 12)
        w.ring(ring, c, rin, ro, -th / 2, th / 2, n=60, a0=-60, a1=240)
    elif g == 3:     # jade ring, four bronze leaf blades
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        for a in (0, 90, 180):
            aa = math.radians(a)
            base = (c[0] + R * 0.95 * math.cos(aa), c[1] + R * 0.95 * math.sin(aa))
            w.poly("bronze", leaf_pts(base, 90 - a, 0.09, 0.03, widest=0.35), -0.012, 0.012, 0.003)
        w.ring("bronze", c, rin - 0.012, rin, -th / 2 - 0.004, th / 2 + 0.004, n=30, a0=-60, a1=240)
    elif g == 4:     # sun-and-moon wheel: gold ring, two steel crescents, teal gem
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        for a0, a1 in ((10, 170),):
            w.ring("steel", c, R, lambda a: R + 0.06 * math.sin(math.radians((a - a0) / (a1 - a0) * 180)) + 0.004,
                   -0.012, 0.012, n=24, a0=a0, a1=a1)
        for a0, a1 in ((190, 230), (-50, -10)):
            w.ring("steel", c, R, lambda a, a0=a0, a1=a1: R + 0.045 * math.sin(math.radians((a - a0) / (a1 - a0) * 180)) + 0.004,
                   -0.012, 0.012, n=12, a0=a0, a1=a1)
        w.sph("teal", (c[0], -0.03, c[1] + R), 0.032, seg=6)
        w.ring("steel_l", c, R + 0.04, R + 0.06 + 0.004, -0.016, -0.01, n=16, a0=45, a1=135)
    elif g == 5:     # glowing double ring, gold crescent, violet gem
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        w.ring("gold", c, rin - 0.03, rin - 0.012, -0.012, 0.012, n=30, a0=-40, a1=220)
        w.ring("gold", c, R, lambda a: R + 0.06 * math.sin(math.radians((a - 20) / 140 * 180)) + 0.004, -0.012, 0.012,
               n=24, a0=20, a1=160)
        w.ico("violet", (c[0], -0.03, c[1] + R), 0.028)
        for a in (200, -20):
            aa = math.radians(a)
            w.sph("cyan_hi", (c[0] + (R + 0.03) * math.cos(aa), -0.01, c[1] + (R + 0.03) * math.sin(aa)), 0.014, seg=5)
    elif g == 6:     # wind-fire wheel: flames all round a blackened ring
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        for k, a in enumerate(range(-40, 230, 30)):
            aa = math.radians(a)
            base = (c[0] + R * 0.9 * math.cos(aa), c[1] + R * 0.9 * math.sin(aa))
            ln = 0.1 if k % 2 else 0.075
            w.poly("flame" if k % 2 else "ember", leaf_pts(base, 90 - a - 20, ln, 0.03, widest=0.3), -0.012, 0.012, 0.002)
        w.ring("ember", c, rin - 0.006, rin + 0.008, -th / 2 - 0.004, th / 2 + 0.004, n=30, a0=-60, a1=240)
        w.ico("flame_y", (c[0], -0.03, c[1] + R), 0.028)
    elif g == 7:     # ice ring, crystal points, two small wings
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        for a in (30, 90, 150):
            aa = math.radians(a)
            base = (c[0] + R * 0.95 * math.cos(aa), c[1] + R * 0.95 * math.sin(aa))
            w.poly("ice_hi", leaf_pts(base, 90 - a, 0.08, 0.022, widest=0.3), -0.012, 0.012, 0.002)
        for s in (-1, 1):
            wings(w, "ice_w", c[1] - 0.02, 3, 0.12, 0.04, rise0=-30, step=24, base_x=R + 0.0, sides=(s,))
        w.ico("cyan", (c[0], -0.03, c[1] + R), 0.026)
    else:            # cosmic: purple ring, gold rim, eight star points, gold core
        w.ring("violet", c, rin - 0.01, R + 0.016, 0.01, 0.016, n=40, a0=-60, a1=240)
        w.ring(ring, c, rin, R, -th / 2, th / 2, n=40, a0=-60, a1=240)
        w.ring("gold_e", c, R - 0.012, R + 0.002, -th / 2 - 0.004, -th / 2 + 0.003, n=40, a0=-60, a1=240)
        for a in range(-30, 211, 30):
            aa = math.radians(a)
            base = (c[0] + R * math.cos(aa), c[1] + R * math.sin(aa))
            w.poly("purple_l", leaf_pts(base, 90 - a, 0.07, 0.022, widest=0.2), -0.01, 0.01, 0.002)
        w.sph("star", (c[0], -0.03, c[1] + R), 0.032, seg=6)
        stars(w, "star", [(c[0] + 0.12, c[1] + 0.05), (c[0] - 0.11, c[1] - 0.04), (c[0] - 0.05, c[1] + 0.13)], -0.024, 0.015)
        w.sph("gold_e", (c[0], -0.01, c[1]), 0.03, seg=8)
        for a in (90, 210, 330):
            aa = math.radians(a)
            w.seg("gold", (c[0], -0.004, c[1]), (c[0] + rin * math.cos(aa), -0.004, c[1] + rin * math.sin(aa)), 0.008, 0.008, 5)
    if g in (2, 3):
        tassel(w, T["cord"], (0, 0, -0.02), n=3, length=0.1)


# ======================================================================= CAM (zither, ~0.8 m)
def zither_outline(g, L=0.4, Wd=0.085):
    """The board seen from above: head (+Z) round, waist notches, tail shapes per grade."""
    pts = []
    if g == 1:      # plain plank
        return [(-Wd, -L), (Wd, -L), (Wd, L - 0.02), (Wd - 0.02, L), (-Wd + 0.02, L), (-Wd, L - 0.02)]
    head_r = Wd
    right = []
    zs = [-L + 0.02, -L * 0.6, -L * 0.2, L * 0.05, L * 0.35, L * 0.55, L * 0.62, L * 0.7]
    for z in zs:
        hw = Wd * (0.86 if z < -L * 0.5 else 1.0)
        if g >= 2 and abs(z - L * 0.62) < 1e-6:
            hw = Wd * 0.8   # neck notch (the "waist" of a guqin)
        right.append((hw, z))
    for i in range(7):  # round head
        a = math.radians(i * 90 / 6)
        right.append((head_r * math.cos(a), L * 0.7 + head_r * 0.9 * math.sin(a) + (L * 0.3 - head_r * 0.9) * (i / 6)))
    tail = [(Wd * 0.86, -L - 0.0), (-Wd * 0.86, -L - 0.0)]
    pts = [(x, z) for x, z in right] + [(-x, z) for x, z in right[::-1]]
    return [tail[1], tail[0]] + pts


def cam(w, g):
    T = TH[g]
    L, Wd = 0.42, 0.11
    body = {1: "wood", 2: "wood_d", 3: "jade", 4: "lacquer", 5: "purple_l", 6: "black", 7: "ice", 8: "purple"}[g]
    side = {1: "wood", 2: "lacq_d", 3: "jade_d", 4: "lacq_d", 5: "purple", 6: "black", 7: "ice_w", 8: "purple"}[g]
    th = 0.05
    out = zither_outline(g, L, Wd)
    w.poly(side, out, -0.0, th / 2, 0.006)              # the underside / sides
    w.poly(body, out, -th / 2, -0.0, 0.006)            # the soundboard faces -Y
    # rims along the long edges (gold from grade 4)
    rim = {1: None, 2: None, 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "gold", 8: "gold"}[g]
    if rim:
        for s in (-1, 1):
            w.box(rim, (s * (Wd - 0.008), -th / 2 - 0.002, -0.02), (0.016, 0.012, 2 * L * 0.88), bevel=0.002)
    # bridge near the head and nut at the tail
    br = {1: "wood_d", 2: "bone", 3: "bronze", 4: "gold", 5: "gold", 6: "gold_dk", 7: "ice_hi", 8: "gold"}[g]
    w.box(br, (0, -th / 2 - 0.008, L * 0.55), (Wd * 1.7, 0.018, 0.026), bevel=0.003)
    w.box(br, (0, -th / 2 - 0.008, -L * 0.85), (Wd * 1.5, 0.016, 0.022), bevel=0.003)
    # strings
    skey = {1: "hemp", 2: "string", 3: "string", 4: "string", 5: "cyan_hi", 6: "ember", 7: "ice_hi", 8: "gold_e"}[g]
    nstr = 3 if g == 1 else 4
    for i in range(nstr):
        x = (i - (nstr - 1) / 2) * 0.05
        w.box(skey, (x, -th / 2 - 0.016, -L * 0.15), (0.022, 0.008, L * 1.42), bevel=0)
    # hui studs along the near edge (grade 2+)
    if g >= 2:
        hk = {2: "bone", 3: "jade_l", 4: "teal", 5: "violet", 6: "flame_y", 7: "cyan", 8: "star"}[g]
        for k in range(5):
            z = -L * 0.7 + k * L * 0.3
            w.sph(hk, (Wd - 0.018, -th / 2 - 0.006, z), 0.013, seg=5)
    # tuning pegs + tassels at the head
    if g == 1:
        for s in (-1, 1):
            w.cyl("wood_d", (s * 0.04, 0, L + 0.01), 0.014, 0.014, 0.04, seg=6)
        w.cyl("hemp", (0, 0, -L - 0.03), 0.01, 0.01, 0.06, seg=5)
        return
    tc = {2: "red", 3: "jade", 4: "red", 5: "violet", 6: "flame", 7: "cyan", 8: "violet"}[g]
    for s in (-1, 1):
        w.cyl(T["trim"], (s * 0.035, 0.01, -L - 0.01), 0.016, 0.016, 0.03, seg=6)
    tassel(w, tc, (0.0, 0.0, -L - 0.03), n=3, length=0.12 if g < 4 else 0.15)
    if g == 3:
        w.sph("jade_d", (0, -th / 2 - 0.004, L * 0.82), 0.03, scale=(1, 0.4, 1), seg=8)
    elif g == 4:   # carved cloud head, gold disc, teal gem
        w.cyl("gold", (0, -th / 2 - 0.004, L * 0.82), 0.045, 0.045, 0.012, rot=(90, 0, 0), seg=10)
        w.sph("teal", (0, -th / 2 - 0.012, L * 0.82), 0.026, seg=6)
        for s in (-1, 1):
            w.poly("gold", [(s * Wd * 0.9, L * 0.6), (s * (Wd + 0.04), L * 0.66), (s * (Wd + 0.03), L * 0.78),
                            (s * Wd * 0.95, L * 0.72)][::s], -0.012, 0.012, 0.003)
    elif g == 5:   # crystal on the head, glowing strings
        w.ico("violet", (0, -th / 2 - 0.01, L * 0.84), 0.034, scale=(1, 0.6, 1.4))
        for s in (-1, 1):
            w.cyl("cyan_hi", (s * 0.05, 0, L + 0.04), 0.018, 0.0, 0.07, rot=(0, s * 25, 0), seg=4)
    elif g == 6:   # flames licking from the tail, ember gem
        w.ico("flame_y", (0, -th / 2 - 0.01, L * 0.82), 0.03)
        for k, (dx, ln) in enumerate(((-0.06, 0.1), (-0.02, 0.15), (0.03, 0.13), (0.07, 0.09))):
            w.poly("flame" if k % 2 else "ember", leaf_pts((dx, -L + 0.02), 180 + dx * 200, ln, 0.03, widest=0.3),
                   -0.012, 0.012, 0.002)
        for s in (-1, 1):
            w.cyl("gold_dk", (s * (Wd + 0.01), 0, L * 0.7), 0.022, 0.0, 0.08, rot=(0, s * 70, 0), seg=4)
    elif g == 7:   # wings at the head
        wings(w, "ice_w", L * 0.62, 3, 0.15, 0.045, rise0=10, step=24, base_x=Wd - 0.01)
        w.ico("cyan", (0, -th / 2 - 0.01, L * 0.82), 0.026)
    elif g == 8:   # star field board, gold core ring
        w.tor("gold", (0, -th / 2 - 0.006, L * 0.82), 0.05, 0.01, (0, 1, 0), seg=16, tseg=4)
        w.sph("star", (0, -th / 2 - 0.012, L * 0.82), 0.03, seg=6)
        stars(w, "star", [(-0.05, -0.25), (0.045, -0.05), (-0.04, 0.12), (0.05, -0.32), (0.0, 0.0)], -th / 2 - 0.014, 0.013)
        w.poly("violet", [(x * 1.18, z * 1.05) for x, z in out], th / 2 - 0.004, th / 2 + 0.004, 0)


# ======================================================================= build
BUILD = {"kich": kich, "roi": roi, "am_khi": am_khi, "luan": luan, "phu": phu, "cam": cam}
DEFAULT_POSE = {"roi": "coil", "am_khi": "hand"}
clear_all = geom.clear_all


def make(wid):
    """Build one weapon into the current scene; returns its root empty."""
    t, g = wid.rsplit("_", 1)
    g = int(g)
    w = W(wid)
    BUILD[t](w, g)
    return w.build(NAMES[g] + " " + TYPE_VI[t], g, t, DEFAULT_POSE.get(t))


def build_one(wid, out_dir):
    clear_all()
    root = make(wid)
    path = os.path.join(out_dir, wid + ".blend")
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    print("MODEL", wid, "tris", root["tris"], "poses", root["poses"] or "-", "->", path)
