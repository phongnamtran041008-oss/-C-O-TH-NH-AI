"""Base tileset builders: the 21 drop-in tiles of client/art/build.py TILESET.

Every builder fills a collection with geometry in tile space (0..16 on both axes, seen from
straight above). Features that cross a tile edge are repeated on the opposite side
(`wraps`), so a tile repeats with itself without seams.
"""
from __future__ import annotations

import math
import random

import wt_common as C
from wt_common import *   # noqa: F401,F403
from wt_common import T, wraps, wraps_x, mat, plane, box, blob, blade, cyl, tube, poly_flat


def rng(*key):
    return random.Random("|".join(map(str, key)))


def ground(col, ramp, step=1, z=0.0):
    return plane(col, "ground", -6, -6, T + 6, T + 6, z, mat(ramp, step))


def tuft(col, x, y, r, ramp, rnd, n=5, h=3.0, lean=2.0, width=1.15, light=(2, 2, 3, 1), z=0.0, seed_tuft=1):
    """A small fan of blades: the pixel-art grass mark."""
    if C.KIT:                       # the kit drops marks thinner than ~2 px; tone comes from the light, not the ramp step
        width, lean, h, n = width * 1.0, lean * 0.85, h * 0.85, min(n, 4)
        light = (1, 1, 2, 1) if seed_tuft % 3 == 0 else (1, 1, 1, 1)
    if C.DETAIL > 1:
        width, lean, h = width * 0.78, lean * 0.7, h * 0.78
    patch(col, x + 0.5, y - 0.7, lean * 0.95, lean * 0.5, mat(ramp, 0), rnd.random(), rot=0.0)
    for dx, dy in wraps(x, y, lean + 1):
        a0 = rnd.uniform(0, 6.28)
        for i in range(n):
            a = a0 + i * 6.28 / n + rnd.uniform(-0.3, 0.3)
            ln = lean * rnd.uniform(0.7, 1.15)
            hh = h * rnd.uniform(0.75, 1.15)
            st = light[i % len(light)]
            C.grass_blade(col, (x + dx, y + dy, z), (x + dx + math.cos(a) * ln, y + dy + math.sin(a) * ln, z + hh),
                          width, mat(ramp, st, emit=C.lit(0.4)))


def lump(col, x, y, sx, sy, sz, material, seed, z=0.0, smooth=False, rough=0.18, subdiv=1, rot=0.0):
    for dx, dy in wraps(x, y, max(sx, sy)):
        blob(col, "lump", (x + dx, y + dy, z), (sx, sy, sz), material, seed=seed, rough=rough, subdiv=subdiv,
             smooth=smooth, rot_z=rot)


_PZ = [0.0]


def patch(col, x, y, rx, ry, material, seed, z=None, rot=0.0):
    """Flat irregular patch (a tone change in the ground, not a bump)."""
    _PZ[0] += 0.012
    if z is None:
        z = 0.02 + (_PZ[0] % 0.1)
    rnd = rng("patch", seed)
    pts = []
    n = 9
    for i in range(n):
        a = 2 * math.pi * i / n
        k = rnd.uniform(0.75, 1.1)
        px, py = math.cos(a) * rx * k, math.sin(a) * ry * k
        pts.append((x + px * math.cos(rot) - py * math.sin(rot), y + px * math.sin(rot) + py * math.cos(rot)))
    for dx, dy in wraps(x, y, max(rx, ry) + 1):
        poly_flat(col, "patch", [(px + dx, py + dy) for px, py in pts], z, material)


# --------------------------------------------------------------------------- grass
def b_grass(col, variant=0, ramp="grass", flowers=False, tufts=4, seed_off=0, base_step=1):
    rnd = rng("grass", ramp, variant + seed_off)
    ground(col, ramp, base_step)
    if C.DETAIL > 1:
        tufts = int(tufts * 2)
    pts = _spread(rnd, tufts, 5.4 if C.DETAIL <= 1 else 3.6)
    for i, (x, y) in enumerate(pts):
        tuft(col, x, y, 1.6, ramp, rnd, n=5, h=2.6, lean=1.8, width=1.0, seed_tuft=i, light=(2, 2, 2, 3, 2) if i % 3 else (1, 2, 2, 2, 2))
    return pts


def _spread(rnd, n, min_d):
    """n points in the tile, at least min_d apart (measured around the wrap)."""
    pts = []
    tries = 0
    while len(pts) < n and tries < 400:
        tries += 1
        p = (rnd.uniform(0.5, T - 0.5), rnd.uniform(0.5, T - 0.5))
        ok = True
        for q in pts:
            dx = abs(p[0] - q[0])
            dy = abs(p[1] - q[1])
            dx = min(dx, T - dx)
            dy = min(dy, T - dy)
            if dx * dx + dy * dy < min_d * min_d:
                ok = False
                break
        if ok:
            pts.append(p)
    return pts


def flower(col, x, y, ramp, rnd, z=0.0):
    FL = 1.0 if C.DETAIL <= 1 else 0.72
    for dx, dy in wraps(x, y, 2.2):
        cx, cy = x + dx, y + dy
        blade(col, "stem", (cx, cy, z), (cx + 0.2, cy - 0.1, z + 0.9), 0.5, mat("grass", 0))
        for i in range(5):
            a = i * 6.283 / 5 + 0.5
            blob(col, "petal", (cx + math.cos(a) * 0.9 * FL, cy + math.sin(a) * 0.9 * FL, z + 1.0), (0.7 * FL, 0.7 * FL, 0.3),
                 mat(ramp, 2, prio=2.0), seed=i, rough=0.0, subdiv=1)
        blob(col, "core", (cx, cy, z + 1.2), (0.55 * FL, 0.55 * FL, 0.35), mat("yellow", 1, prio=3.0), seed=1, rough=0.0, subdiv=1)


def b_flowers(col, variant=0):
    pts = b_grass(col, variant, seed_off=7, tufts=3)
    rnd = rng("flowers", variant)
    kinds = [["white", "blossom", "yellow"], ["violet", "yellow", "white"]][variant % 2]
    spots = _spread(rnd, 4, 4.6)
    spots = [p for p in spots if all(min(abs(p[0] - q[0]), T - abs(p[0] - q[0])) > 2.4 or
                                     min(abs(p[1] - q[1]), T - abs(p[1] - q[1])) > 2.4 for q in pts)][:4]
    for i, (x, y) in enumerate(spots):
        flower(col, x, y, kinds[i % 3], rnd)


# --------------------------------------------------------------------------- path
def pebbles(col, rnd, n, ramps=("path", "stone"), z=0.0, size=(0.7, 1.3)):
    if C.DETAIL > 1:
        n, size = int(n * 1.8), (size[0] * 0.7, size[1] * 0.7)
    for i in range(n):
        x, y = rnd.uniform(0.5, T - 0.5), rnd.uniform(0.5, T - 0.5)
        sx = rnd.uniform(*size)
        sy = sx * rnd.uniform(0.6, 0.9)
        ramp = ramps[i % len(ramps)]
        st = rnd.choice((1, 2, 2))
        lump(col, x, y, sx, sy, rnd.uniform(0.35, 0.55), mat(ramp, st), rnd.randrange(999), z=z,
             rot=rnd.uniform(0, 3), subdiv=1)


def b_path(col, variant=0):
    rnd = rng("path", variant)
    ground(col, "path", C.kit_or(2, 1))
    f = 1.0 if C.DETAIL <= 1 else 0.68
    for i in range(5 if f == 1.0 else 10):
        x, y = rnd.uniform(0.5, T - 0.5), rnd.uniform(0.5, T - 0.5)
        s = rnd.uniform(1.0, 1.6) * f
        stone = i % 3 == 2
        lump(col, x, y, s, s * 0.7, 0.55, mat("stone" if stone else "path", C.kit_or(1, 2) if not stone else 1), rnd.randrange(999),
             rot=rnd.uniform(0, 3), subdiv=2, smooth=True, rough=0.12)
    for _ in range(5 if f == 1.0 else 12):                # grit
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        lump(col, x, y, 0.45, 0.35, 0.2, mat("path", 0), rnd.randrange(99), subdiv=1)
    for _ in range(2):                                   # scuffs
        x, y = rnd.uniform(2, 14), rnd.uniform(2, 14)
        box(col, "scuff", (x, y, 0.04), (rnd.uniform(2.5, 4), 0.45, 0.06), mat("path", 0), rot_z=rnd.uniform(-0.3, 0.3))


# --------------------------------------------------------------------------- water
def b_water(col, frame=0):
    ground(col, "water", 1)
    rnd = rng("water")
    # streak layout is periodic; every frame shifts it by a quarter tile, so 4 frames loop
    streaks = [(2.0, 2.0, 4.5, "water", 2), (10.5, 3.2, 3.6, "water", 2), (6.0, 6.6, 3.0, "water", 0),
               (12.5, 8.8, 4.2, "water", 2), (3.0, 10.4, 3.8, "water", 0), (8.5, 12.8, 4.6, "water", 2),
               (14.0, 14.4, 2.6, "water", 3), (5.0, 14.8, 2.2, "water", 0)]
    sh = 4.0 * frame
    for x, y, ln, ramp, st in streaks:
        xx = (x + sh) % T
        wob = 0.25 * math.sin((frame + y) * 1.6)
        for dx in wraps_x(xx, ln):
            m = mat(ramp, st, emit=0.0)
            box(col, "streak", (xx + dx + ln / 2, y + wob, 0.12), (ln, 1.3 if C.KIT else 0.75, 0.3), m)
    # a glint that hops between four spots
    gx, gy = [(4.5, 4.5), (12, 6), (9, 11.5), (2.5, 13)][frame % 4]
    blob(col, "glint", (gx, gy, 0.3), (0.55, 0.55, 0.2), mat("water", 3, emit=C.lit(1.0)), seed=1, rough=0, subdiv=1)


# --------------------------------------------------------------------------- bamboo floor
def leaf_flat(col, x, y, ang, ln, wd, material, z=0.1):
    c, s = math.cos(ang), math.sin(ang)
    pts = [(-ln / 2, 0), (0, wd / 2), (ln / 2, 0), (0, -wd / 2)]
    for dx, dy in wraps(x, y, ln):
        poly_flat(col, "leaf", [(x + dx + px * c - py * s, y + dy + px * s + py * c) for px, py in pts], z, material)


def b_bamboo_floor(col, variant=0):
    rnd = rng("bf", variant)
    ground(col, "jade", 0)
    for i in range(9 if C.DETAIL <= 1 else 16):
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        ramp, st = rnd.choice([("olive", 1), ("olive", 2), ("jade", 1), ("jade", 2), ("bark", 2), ("olive", 2)])
        leaf_flat(col, x, y, rnd.uniform(0, 3.14), rnd.uniform(3.0, 4.2) * (1 if C.DETAIL <= 1 else 0.75), 0.9 * (1 if C.DETAIL <= 1 else 0.75), mat(ramp, st), z=0.12 + i * 0.008)
    for (x, y) in _spread(rnd, 2, 7):
        tuft(col, x, y, 1.5, "jade", rnd, n=4, h=2.6, lean=1.8, light=(2, 1, 3, 2))


# --------------------------------------------------------------------------- stone / flags
def slab(col, x, y, w, h, z, material, bevel=0.5, height=1.1, rot=0.0):
    for dx, dy in wraps(x, y, max(w, h) / 2 + 1):
        box(col, "slab", (x + dx, y + dy, z + height / 2), (w, h, height), material, rot_z=rot, bevel=bevel)


def b_stone(col, variant=0):
    """Cobbles. Variant 0: three rows of two; variant 1: a looser pattern of big and small stones."""
    rnd = rng("stone", variant)
    ground(col, "stone", 0)
    if variant == 0:
        layout = []
        rows = 3
        rh = T / rows
        for r in range(rows):
            o = (r % 2) * (T / 4)
            for k in range(2):
                layout.append((o + (k + 0.5) * (T / 2), (r + 0.5) * rh, T / 4 - 0.5, rh / 2 - 0.45))
    else:
        layout = [(3.0, 3.2, 3.6, 2.4), (10.0, 2.6, 3.9, 2.2), (4.2, 8.6, 2.6, 3.0), (11.0, 8.2, 3.4, 2.6),
                  (15.4, 11.6, 2.4, 3.2), (7.5, 13.4, 3.6, 2.2), (0.6, 14.0, 2.2, 2.0), (14.6, 2.0, 1.6, 1.4)]
    for (cx, cy, rx, ry) in layout:
        cx += rnd.uniform(-0.3, 0.3)
        cy += rnd.uniform(-0.3, 0.3)
        st = 2 if rnd.random() < 0.25 else 1
        for dx, dy in wraps(cx, cy, 5):
            blob(col, "cobble", (cx + dx, cy + dy, 0.0), (rx + rnd.uniform(-0.2, 0.2), ry, 1.5),
                 mat("stone", st), seed=rnd.randrange(99), rough=0.08, subdiv=2, smooth=True)
    for _ in range(2):
        lump(col, rnd.uniform(1, 15), rnd.uniform(1, 15), 0.9, 0.6, 0.35, mat("grass", 0), rnd.randrange(99), z=0.15)


def b_wood(col, variant=0):
    rnd = rng("wood", variant)
    ground(col, "wood", 0)
    shades = [1, 2, 1, 1]
    for r in range(4):
        y0 = r * 4.0
        joint = rnd.uniform(1, 15)
        st = shades[(r + variant) % 4]
        # one board per row wraps around the tile, so rows repeat without a visible end
        xs = joint + 0.25
        for off in (0.0, -T):
            box(col, "plank", (xs + off + (T - 0.5) / 2, y0 + 2.0, 0.55), (T - 0.5, 3.35, 1.1), mat("wood", st), bevel=0.28)
        for g in range(2 if C.DETAIL <= 1 else 4):     # grain
            gy = y0 + rnd.uniform(0.9, 3.1)
            gx = rnd.uniform(0, T)
            ln = rnd.uniform(4, 8)
            for dx in wraps_x(gx, ln):
                box(col, "grain", (gx + dx + ln / 2, gy, 1.12), (ln, 0.22, 0.08), mat("wood", 0))
        for nx in (joint + 1.2, joint - 1.2):          # nail heads by the joint
            nx %= T
            cyl(col, "nail", (nx, y0 + 0.9, 1.1), 0.34, 0.3, 0.2, mat("stone", 0), seg=6)
            cyl(col, "nail", (nx, y0 + 3.1, 1.1), 0.34, 0.3, 0.2, mat("stone", 0), seg=6)


def b_plaza(col, variant=0):
    """Flagstones. 0 / 1: square slabs, joints at 0 or 8; 2: long and short slabs."""
    rnd = rng("plaza", variant)
    ground(col, "stone", 0)
    if variant < 2:
        off = 8.0 if variant % 2 else 0.0
        rows = [(4.0, [(off + 4.0, 7.3), (off + 12.0, 7.3)]), (12.0, [(off + 8.0, 7.3), (off + 16.0, 7.3)])]
    else:
        rows = [(4.0, [(2.667 + 5.333 * k, 4.9) for k in range(3)]), (12.0, [(5.333 * k, 4.9) for k in range(3)])]
    for cy, slabs in rows:
        for cx, w in slabs:
            slab(col, cx % T if variant < 2 else cx, cy, w, 7.3, 0.0, mat("stone", 1), bevel=0.55, height=1.0 + rnd.uniform(0, 0.25))
    for _ in range(2):
        lump(col, rnd.uniform(0, T), rnd.choice([0.2, 8.0]), 0.9, 0.6, 0.3, mat("grass", 0), rnd.randrange(99), z=0.2)
    x, y = rnd.uniform(2, 14), rnd.choice([4.0, 12.0]) + rnd.uniform(-1.5, 1.5)
    box(col, "crack", (x, y, 1.15), (2.6, 0.25, 0.1), mat("stone", 0), rot_z=rnd.uniform(-1, 1))


def dirt_specks(col, rnd, ox=0.0, oy=0.0, cells=9, keep=0.55, region=None):
    """Fine worked-earth texture: tiny flat specks on a jittered grid, darker and lighter than the soil, nothing at the centre."""
    cs = T / cells
    for gy in range(cells):
        for gx in range(cells):
            if rnd.random() > keep:
                continue
            x = (gx + rnd.uniform(0.15, 0.85)) * cs
            y = (gy + rnd.uniform(0.15, 0.85)) * cs
            if region and not region(x + ox, y + oy):
                continue
            st = 0 if rnd.random() < 0.5 else 2
            lump(col, x, y, rnd.uniform(0.35, 0.75), rnd.uniform(0.25, 0.5), 0.16, mat("dirt", st), rnd.randrange(999),
                 rough=0.1, subdiv=1, rot=rnd.uniform(0, 3))


def b_dirt(col, variant=0):
    """Dirt. 16 px sheet: the old tile. 32 px sheet: three plain variants that tile with each other (no centred object)."""
    if C.DETAIL <= 1:
        rnd = rng("dirt", variant)
        ground(col, "dirt", 1)
        patch(col, rnd.uniform(2, 14), rnd.uniform(2, 14), 4.2, 2.4, mat("dirt", 2), rnd.random(), rot=rnd.uniform(0, 3))
        patch(col, rnd.uniform(2, 14), rnd.uniform(2, 14), 3.6, 2.2, mat("dirt", 0), rnd.random(), rot=rnd.uniform(0, 3))
        for i in range(4):
            lump(col, rnd.uniform(0, T), rnd.uniform(0, T), rnd.uniform(1.0, 1.7), rnd.uniform(0.8, 1.4), rnd.uniform(0.4, 0.7),
                 mat("dirt", rnd.choice((0, 2, 2))), rnd.randrange(999), rough=0.25, subdiv=1)
        pebbles(col, rnd, 3, ramps=("stone", "path"), size=(0.5, 0.9))
        return
    rnd = rng("dirt32", variant)
    ground(col, "dirt", 1)
    dirt_specks(col, rnd, cells=10, keep=0.4 + 0.04 * variant)
    if variant == 2:                                     # two tiny off-centre stones, only in this variant
        for (x, y, s) in ((3.0, 12.6, 0.42), (13.2, 3.4, 0.34)):
            lump(col, x, y, s, s * 0.75, 0.2, mat("stone", 2), int(x * 7), subdiv=1)


def b_dark_grass(col, variant=0):
    pts = b_grass(col, variant, ramp="grass_d", seed_off=31, tufts=5)


def b_ink(col, variant=0):
    rnd = rng("ink", variant)
    ground(col, "ink", 1)
    # cold wisps: slow waves across the whole tile (period = tile width, so they run on into the next tile)
    ys = [4.0, 10.5] if variant == 0 else [6.5, 13.0]
    for i, y0 in enumerate(ys):
        amp = 1.3 if i == 0 else 1.0
        ph = rnd.uniform(0, 6.28)
        pts = [(16.0 * t / 10, y0 + amp * math.sin(ph + 2 * math.pi * t / 10), 0.35) for t in range(11)]
        glow = (i == 0)
        rad = [0.42 if glow else 0.3] * 11
        for dx in (-T, 0.0, T):
            tube(col, "wisp", [(px + dx, py, pz) for px, py, pz in pts], rad,
                 mat("mist", 1 if glow else 0, emit=1.2 if glow else 0.0), seg=4, smooth=True)
    for _ in range(4):                                   # sparks
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        for dx, dy in wraps(x, y, 1):
            blob(col, "spark", (x + dx, y + dy, 0.5), (0.5, 0.5, 0.3), mat("mist", 3, emit=2.0), seed=1, rough=0, subdiv=1)
    for _ in range(2):                                   # faint raised bumps of denser mist
        lump(col, rnd.uniform(0, T), rnd.uniform(0, T), 2.4, 1.3, 0.4, mat("ink", 2), rnd.randrange(99), subdiv=1, smooth=True)


def b_realm_floor(col, variant=0):
    rnd = rng("rf", variant)
    ground(col, "slate", 0)
    if C.DETAIL > 1:      # 32 px sheet: joints sit on the tile edge or well inside it, so the tile repeats cleanly
        if variant == 0:
            rows = [(4.0, [(4.0, 7.3), (12.0, 7.3)]), (12.0, [(0.0, 7.3), (8.0, 7.3)])]
        else:
            rows = [(4.0, [(2.667 + 5.333 * k, 4.9) for k in range(3)]), (12.0, [(5.333 * k, 4.9) for k in range(3)])]
        for cy_, slabs in rows:
            for cx_, w in slabs:
                slab(col, cx_, cy_, w, 7.3, 0.0, mat("slate", 1), bevel=0.55, height=0.9)
        x, y = rnd.uniform(3, 12), rnd.uniform(3, 12)
        box(col, "crack", (x, y, 1.0), (3.4, 0.3, 0.1), mat("mist", 0, emit=0.9), rot_z=rnd.uniform(-1, 1))
        return
    jx = (7.0, 15.0)[variant % 2]
    for r, cy in enumerate((4.0, 12.0)):
        jj = (jx + 8.0 * r) % T
        for k in range(2):
            cx = (jj + 4.0 + 8.0 * k) % T
            slab(col, cx, cy, 7.3, 7.3, 0.0, mat("slate", 1), bevel=0.55, height=0.9)
    # ink-stained crack with a faint glow
    x, y = rnd.uniform(3, 12), rnd.uniform(3, 12)
    box(col, "crack", (x, y, 1.0), (3.4, 0.3, 0.1), mat("mist", 0, emit=0.9), rot_z=rnd.uniform(-1, 1))


def b_realm_wall(col, variant=0):
    rnd = rng("rw", variant)
    ground(col, "ink", 0)
    rows = 4
    rh = T / rows
    for r in range(rows):
        o = 0.0 if r % 2 == 0 else 4.0
        for k in range(2):
            cx = (o + 4.0 + 8.0 * k) % T
            slab(col, cx, r * rh + rh / 2, 7.4, rh - 0.6, 0.0, mat("slate", 1 if (r + k) % 3 else 2), bevel=0.55,
                 height=2.4)
    for x in (rnd.uniform(2, 6), rnd.uniform(10, 14)):    # ink running down the blocks
        box(col, "drip", (x, rnd.uniform(5, 11), 2.5), (0.7, rnd.uniform(3, 6), 0.15), mat("ink", 0))
    box(col, "rim", (8, T - 0.3, 2.7), (T, 0.6, 0.2), mat("slate", 3))


BASE = [
    # (tile name, variant, builder-name)
    ("grass", 0), ("grass", 1), ("grass", 2), ("flowers", 0), ("flowers", 1),
    ("path", 0), ("path", 1), ("water", 0), ("bamboo_floor", 0), ("stone", 0), ("wood", 0),
    ("plaza", 0), ("plaza", 1), ("dirt", 0), ("dark_grass", 0), ("dark_grass", 1), ("ink", 0), ("ink", 1),
    ("realm_floor", 0), ("realm_floor", 1), ("realm_wall", 0),
]

BUILDERS = {
    "grass": b_grass, "flowers": b_flowers, "path": b_path, "bamboo_floor": b_bamboo_floor, "stone": b_stone,
    "wood": b_wood, "plaza": b_plaza, "dirt": b_dirt, "dark_grass": b_dark_grass, "ink": b_ink,
    "realm_floor": b_realm_floor, "realm_wall": b_realm_wall,
}


def tile_id(name, variant):
    return f"{name}_{variant}"


def assets():
    """Asset list for the runner: (asset_id, tiles_w, tiles_h, builder(col), slices)"""
    out = []
    for name, v in BASE:
        if name == "water":
            continue
        out.append(dict(id=tile_id(name, v), w=1, h=1, build=(lambda col, n=name, v=v: BUILDERS[n](col, v)),
                        slices=[(tile_id(name, v), 0, 0)], group="base"))
    extra = [("stone", 1), ("plaza", 2)] + ([("dirt", 1), ("dirt", 2)] if C.DETAIL > 1 else [])
    for n, v in extra:
        out.append(dict(id=tile_id(n, v), w=1, h=1, build=(lambda col, n=n, v=v: BUILDERS[n](col, v)),
                        slices=[(tile_id(n, v), 0, 0)], group="base"))
    for f in range(4):
        out.append(dict(id=f"water_f{f}", w=1, h=1, build=(lambda col, f=f: b_water(col, f)),
                        slices=[(f"water_f{f}", 0, 0)], group="base"))
    return out
