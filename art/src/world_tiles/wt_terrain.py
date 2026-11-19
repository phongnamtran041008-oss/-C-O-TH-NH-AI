"""Extended tiles (terrain.png): transitions, shores, plateau + cliff, stairs, bridge, biomes.

Edge naming: the suffix says where the *outer* material lies (grass_path_n = grass to the
north of the path). Corners `_nw` etc. are convex corners of the inner blob, `_in_nw` the
concave ones (a notch of the outer material in that corner).
Cliffs use the oblique game projection: the model is built in true 3D and then sheared
(screen y = y + z), so a face of height 32 fills two tile rows.
"""
from __future__ import annotations

import math
import random

import wt_common as C
from wt_common import T, mat, plane, box, blob, blade, cyl, tube, poly_flat, heightfield, wraps, wraps_x
import wt_base
from wt_base import rng, ground, tuft, lump, patch, pebbles, _spread, b_water

D_IN = 5.0          # where the blob edge lies inside the tile ring
R_OUT = 8.0         # corner radius of the blob (convex corners)
R_IN = 4.0          # corner radius of the notch (concave corners)


def rrect(px, py, x0, y0, x1, y1, r):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    qx, qy = abs(px - cx) - hx, abs(py - cy) - hy
    return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - r


def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


ROLES = {   # role -> (ix, iy) of the 3x3 block (iy 0 = top row)
    "nw": (0, 0), "n": (1, 0), "ne": (2, 0), "w": (0, 1), "e": (2, 1), "sw": (0, 2), "s": (1, 2), "se": (2, 2),
}
INNER = {"in_nw": (False, False), "in_ne": (True, False), "in_sw": (False, True), "in_se": (True, True)}


EXTRA_ROLES = ["island", "h", "v", "cap_n", "cap_s", "cap_e", "cap_w"]
_EX = {   # shapes for isolated cells: a 10 px round island, 8 px strips and rounded strip ends
    "island": (2.5, 2.5, 13.5, 13.5, 5.5), "h": (-40, 4, 56, 12, 4), "v": (4, -40, 12, 56, 4),
    "cap_n": (4, -40, 12, 12, 4), "cap_s": (4, 4, 12, 56, 4), "cap_e": (-40, 4, 12, 12, 4), "cap_w": (4, 4, 56, 12, 4),
}


def region_fn(role):
    """s(x, y) < 0 inside the blob (the inner material)."""
    if role in _EX:
        x0, y0, x1, y1, r = _EX[role]
        return lambda x, y: rrect(x, y, x0, y0, x1, y1, r)
    if role in ROLES:
        ix, iy = ROLES[role]
        return lambda x, y: rrect(x + 16 * ix, y + 16 * (2 - iy), D_IN, D_IN, 48 - D_IN, 48 - D_IN, R_OUT)
    fx, fy = INNER[role]

    def f(x, y):
        xx = 16 - x if fx else x
        yy = 16 - y if fy else y
        return -rrect(xx, yy, -40, 16 - D_IN, D_IN, 56, R_IN)
    return f


def periodic_axes(role):
    if role == "h":
        return (True, False)
    if role == "v":
        return (False, True)
    if role in ("n", "s"):
        return (True, False)
    if role in ("w", "e"):
        return (False, True)
    return (False, False)


PAIRS = {
    # outer ramp, inner ramp, tuft ramp (outer), height of outer bank, inner level
    "path":  dict(inner=("path", C.kit_or(2, 1)), bank=("grass", 0), edge_in=("path", 0), zb=1.0, zi=0.0),
    "dirt":  dict(inner=("dirt", 1), bank=("grass", 0 if C.DETAIL <= 1 else 1), edge_in=("dirt", 0 if C.DETAIL <= 1 else 1), zb=1.0, zi=0.0),
    "shore": dict(inner=("water", 1), bank=("dirt", 2), edge_in=("water", 3), zb=1.1, zi=-0.7),
    # 32 px extras: stone and plaza against grass, grass against dark grass, dark grass against ink ground
    "stone": dict(inner=("stone", 1), bank=("grass", 1), edge_in=("stone", 0), zb=1.0, zi=0.0, kind="stone"),
    "plaza": dict(inner=("stone", 1), bank=("grass", 1), edge_in=("stone", 0), zb=0.6, zi=0.0, kind="plaza"),
    "dark":  dict(inner=("grass_d", 1), bank=("grass", 1), edge_in=("grass_d", 1), zb=0.5, zi=0.0, kind="tuft", in_tuft="grass_d"),
    "ink":   dict(outer=("grass_d", 1), inner=("ink", 1), bank=("grass_d", 1), edge_in=("ink", 1), zb=0.5, zi=0.0, kind="ink",
                  out_tuft="grass_d"),
}


def build_transition(col, pair, role):
    P = PAIRS[pair]
    s_fn = region_fn(role)
    rnd = rng("tr", pair, role)
    zb, zi = P["zb"], P["zi"]
    m_out = mat(*P.get("outer", ("grass", 1)))
    kind = P.get("kind")
    m_bank = mat(*P["bank"])
    m_in = mat(*P["inner"])
    m_edge = mat(*P["edge_in"], emit=C.lit(0.5) if pair == "shore" else 0.0)
    m_shadow = mat(*P["edge_in"]) if pair != "shore" else mat("water", 0)
    mats = [m_out, m_bank, m_in, m_edge, m_shadow, mat("stone", 0)]

    def z_fn(x, y):
        s = s_fn(x, y)
        if pair == "shore":
            return zi + (zb - zi) * smooth(-0.6, 0.5, s)
        return zb * smooth(-0.3, 0.9, s)

    def m_fn(x, y):
        s = s_fn(x, y)
        if s > 1.0:
            return 0
        if s > 0.0:
            return 1
        if pair == "shore":
            return 3 if s > -1.3 else 2
        if kind == "plaza" and (abs(x - 8.0) < 0.3 or abs(y - 8.0) < 0.3 or x < 0.3 or y < 0.3 or x > T - 0.3 or y > T - 0.3):
            return 5
        return 4 if s > -1.1 else 2

    heightfield(col, "terrain", 0, 0, T, T, 128, z_fn, m_fn, mats)
    # --- scatter: outer tufts, inner pebbles / glints, kept away from the tile border unless periodic
    px_, py_ = periodic_axes(role)

    def ok(x, y, region, margin):
        s = s_fn(x, y)
        if region == "out" and s < 2.2:
            return False
        if region == "in" and s > -2.0:
            return False
        if not px_ and not (2.0 <= x <= T - 2.0):
            return False
        if not py_ and not (2.0 <= y <= T - 2.0):
            return False
        return True

    for i, (x, y) in enumerate(_spread(rnd, 7 if C.DETAIL <= 1 else 14, 4.2 if C.DETAIL <= 1 else 3.0)):
        if ok(x, y, "out", 2):
            xs = wraps_x(x, 2.5) if px_ else [0.0]
            ys = wraps_x(y, 2.5) if py_ else [0.0]
            for dx in xs:
                for dy in ys:
                    _tuft_at(col, x + dx, y + dy, zb, rnd, i, ramp=P.get("out_tuft", "grass"))
    if kind == "stone":
        for (x, y) in _spread(rnd, 9, 3.6):
            if ok(x, y, "in", 2):
                blob(col, "cobble", (x, y, 0.0), (rnd.uniform(1.3, 1.9), rnd.uniform(1.0, 1.4), 0.8), mat("stone", 2),
                     seed=rnd.randrange(99), rough=0.1, subdiv=1, smooth=True)
    elif kind == "plaza":
        pass
    elif kind == "tuft":
        for i, (x, y) in enumerate(_spread(rnd, 9, 3.4)):
            if ok(x, y, "in", 2):
                _tuft_at(col, x, y, 0.0, rnd, i, ramp=P["in_tuft"])
    elif kind == "ink":
        for (x, y) in _spread(rnd, 6, 3.2):
            if ok(x, y, "in", 2):
                blob(col, "spark", (x, y, 0.4), (0.5, 0.5, 0.3), mat("mist", 3, emit=2.0, prio=2.0), seed=1, rough=0, subdiv=1)
    elif pair == "shore":
        for (x, y) in _spread(rnd, 3, 5.0):
            if ok(x, y, "in", 2):
                blob(col, "glint", (x, y, zi + 0.2), (1.2, 0.4, 0.1), mat("water", 2), seed=1, rough=0, subdiv=1)
    if pair in ("path", "dirt"):
        for (x, y) in _spread(rnd, 6 if C.DETAIL <= 1 else 12, 3.6 if C.DETAIL <= 1 else 2.6):
            if ok(x, y, "in", 2):
                if C.DETAIL > 1:
                    if pair == "path":
                        s = rnd.uniform(0.6, 0.95)
                        blob(col, "pebble", (x, y, 0.0), (s, s * 0.7, 0.4), mat("path" if rnd.random() < 0.7 else "stone", C.kit_or(1, 2)),
                             seed=rnd.randrange(99), rough=0.1, subdiv=1, smooth=True)
                    else:
                        lump(col, x, y, rnd.uniform(0.35, 0.7), rnd.uniform(0.25, 0.45), 0.16, mat("dirt", rnd.choice((0, 2))),
                             rnd.randrange(999), rough=0.1, subdiv=1)
                    continue
                if pair == "path":
                    s = rnd.uniform(0.9, 1.4)
                    blob(col, "pebble", (x, y, 0.0), (s, s * 0.7, 0.5), mat("path" if rnd.random() < 0.7 else "stone", C.kit_or(1, 2)),
                         seed=rnd.randrange(99), rough=0.1, subdiv=2, smooth=True)
                else:
                    blob(col, "clod", (x, y, 0.0), (rnd.uniform(1.0, 1.6), rnd.uniform(0.8, 1.2), 0.5),
                         mat("dirt", rnd.choice((0, 2))), seed=rnd.randrange(99), rough=0.22, subdiv=1)


def _tuft_at(col, x, y, z, rnd, i, dark=False, ramp="grass"):
    patch(col, x + 0.5, y - 0.7, 1.9, 1.0, mat(ramp, 0), rnd.random(), z=z + 0.03 + (i % 7) * 0.004)
    a0 = rnd.uniform(0, 6.28)
    for k in range(5):
        a = a0 + k * 6.28 / 5 + rnd.uniform(-0.3, 0.3)
        ln = 2.0 * rnd.uniform(0.7, 1.15)
        st = (2, 2, 3, 2, 2)[k] if i % 3 else (1, 2, 2, 3, 2)[k]
        if dark:                      # on the lighter plateau top the marks are darker than the ground
            st = (1, 1, 0, 1, 1)[k]
        if C.KIT:
            ln, hgt, wd = ln * 0.85, 2.6, 1.3
            st = 0 if dark else 1
            if C.DETAIL > 1:
                ln, hgt, wd = ln * 0.72, hgt * 0.8, wd * 0.78
        else:
            hgt, wd = 3.0, 1.15
        C.grass_blade(col, (x, y, z), (x + math.cos(a) * ln, y + math.sin(a) * ln, z + hgt * rnd.uniform(0.75, 1.15)),
                      wd, mat(ramp, st, emit=C.lit(0.4)))


# --------------------------------------------------------------------------- plateau top edge (back rows)
def build_plateau_edge(col, role):
    s_fn = region_fn(role)
    rnd = rng("plat", role)
    zt = 2.0                          # plateau top above the lower ground
    m_low, m_top, m_rim, m_dark, m_hi = mat("grass", 1), mat("grass", 2), mat("rock", 1), mat("grass", 0), mat("grass", 3)
    mats = [m_low, m_top, m_rim, m_dark, m_hi]
    shaded = role in ("e", "ne", "se")

    def z_fn(x, y):
        s = s_fn(x, y)
        return zt * smooth(-0.6, 0.4, -s)

    def m_fn(x, y):
        s = s_fn(x, y)
        if s > 3.4:
            return 0
        if s > 1.5:
            return 3 if shaded else 0       # the plateau throws its shadow to the right
        if s > -0.5:
            return 2                         # the rock lip, 2 px
        if s > -1.7:
            return 4                         # lit edge of the grass top
        return 1

    heightfield(col, "plateau", 0, 0, T, T, 128, z_fn, m_fn, mats)


def build_realm_edge(col, role):
    """Bi canh: slate floor outside, a raised wall block inside (the wall top seen from above, its rim lit)."""
    s_fn = region_fn(role)
    rnd = rng("realm_edge", role)
    mats = [mat("slate", 1), mat("slate", 2), mat("slate", 0), mat("ink", 0)]

    def z_fn(x, y):
        return 2.4 * smooth(-0.6, 0.4, -s_fn(x, y))

    def m_fn(x, y):
        s = s_fn(x, y)
        if s > 2.5:
            return 0
        if s > 0.5:
            return 2 if abs(x - 8) > 0 else 2
        if s > -0.8:
            return 1
        # mortar lines of the wall blocks
        if abs(((y + 0.0) % 4.0) - 2.0) > 1.75 or abs(((x + 4.0 * (int(y // 4) % 2)) % 8.0) - 4.0) > 3.75:
            return 2
        return 0 if False else 1

    heightfield(col, "realm_edge", 0, 0, T, T, 128, z_fn, m_fn, mats)


# --------------------------------------------------------------------------- cliff faces
RISE = 3.4          # height of one rock step in tile units (the face is a height-field seen from above)
LEDGES = [0.0, 6.6, 13.4, 19.8, 25.8]      # screen y of each ledge's foot (bottom to top)


def _pnoise(x, k, ph):
    """Smooth noise with period 16 in x."""
    return (math.sin(2 * math.pi * k * x / 16 + ph) + 0.5 * math.sin(2 * math.pi * (k + 1) * x / 16 + ph * 1.7)) / 1.5


def face_z(x, y, variant):
    """Height of the rock face at screen (x, y): stepped ledges with rounded risers, chipped by noise."""
    z = 0.0
    n = len(LEDGES)
    for k in range(n):
        foot = LEDGES[k] + 1.3 * _pnoise(x, 1 + (k + variant) % 2, k * 1.9 + variant * 3.1)
        if k + 1 < n:
            nxt = LEDGES[k + 1] + 1.3 * _pnoise(x, 1 + (k + 1 + variant) % 2, (k + 1) * 1.9 + variant * 3.1)
        else:
            nxt = 40.0
        if y < foot:
            break
        riser = 3.0 + 0.8 * _pnoise(x, 2, k + variant)
        t = y - foot
        if t < riser:
            u = t / riser
            return z + RISE * (u * u * (3 - 2 * u))
        z += RISE
        if y < nxt:
            return z + 0.7 * (t - riser) / max(nxt - foot - riser, 1.0)
        z += 0.7
    return z


def _crack(x, y, xc, y0, y1, w=0.4, d=1.3):
    if not (y0 < y < y1):
        return 0.0
    e = math.sin(math.pi * (y - y0) / (y1 - y0))
    return d * e * math.exp(-((x - xc) / w) ** 2)


def build_face(col, kind, variant):
    """16 wide x 32 tall column of cliff face (two tile rows): stepped natural rock seen from above."""
    rnd = rng("face", kind, variant)
    cracks = [(rnd.uniform(1.5, 14.5), rnd.uniform(3, 20)) for _ in range(3)]
    cracks = [(xc, y0, y0 + rnd.uniform(5, 8)) for xc, y0 in cracks]

    def wall(x, y):
        z = face_z(x, y, variant)
        for xc, y0, y1 in cracks:
            z -= _crack(x, y, xc, y0, y1)
        if kind == "l":
            z *= smooth(D_IN - 0.2, D_IN + 2.4, x)
        elif kind == "r":
            z *= 1.0 - smooth(T - D_IN - 2.4, T - D_IN + 0.2, x)
        return z

    mats = [mat("rock", 0), mat("rock", 1), mat("rock", 2), mat("grass", 1)]

    def m_fn(x, y):
        if kind == "l" and x < D_IN - 0.3:
            return 3
        if kind == "r" and x > T - D_IN + 0.3:
            return 3
        yy = y + 1.5 * _pnoise(x, 2, 0.7 + variant)       # darker at the base, lighter near the top
        return 0 if yy < 9.0 else 1 if yy < 21.0 else 2

    heightfield(col, "face", 0, 0, T, 32.0, 128, wall, m_fn, mats)
    # moss tufts on the ledges
    for k in range(3):
        x = rnd.uniform(2.5, 13.5)
        y = rnd.choice(LEDGES[1:4]) + rnd.uniform(4.2, 5.4)
        if kind == "l" and x < D_IN + 2:
            continue
        if kind == "r" and x > T - D_IN - 2:
            continue
        _tuft_at(col, x, y, wall(x, y), rnd, k)
    # the grass lip rolling over the top edge, and the lighter plateau top behind it
    for k in range(6):
        x = (k + 0.5) * T / 6 + rnd.uniform(-0.5, 0.5)
        if kind == "l" and x < D_IN + 1.2:
            continue
        if kind == "r" and x > T - D_IN - 1.2:
            continue
        blob(col, "lip", (x, 30.4, wall(x, 30.4) + 0.6), (2.9, 1.7, 1.3), mat("grass", 2 if k % 2 else 3), seed=k, rough=0.2,
             subdiv=1, smooth=True)
        blade(col, "hang", (x + 0.6, 29.6, wall(x, 29.6) + 0.5), (x + 0.9, 28.2, wall(x, 28.2) + 0.2), 1.1, mat("grass", 1))
    zt = wall(8.0 if kind == "mid" else (13.0 if kind == "l" else 3.0), 31.0)
    plane(col, "top", (D_IN if kind == "l" else 0.0), 31.0, (T - D_IN if kind == "r" else T), 40.0, zt + 0.9, mat("grass", 2))


def build_cliff_shadow(col, kind):
    """Grass at the foot of the face with the cast shadow of the cliff (a ragged dark band)."""
    rnd = rng("cshadow", kind)
    ground(col, "grass", 1)
    x0, x1 = (D_IN - 0.5, T + 1) if kind == "l" else ((-1.0, T - D_IN + 3.4) if kind == "r" else (-1.0, T + 1))
    pts_top = [(x0, T + 1), (x1, T + 1)]
    low = []
    n = 12
    for k in range(n + 1):
        x = x1 - (x1 - x0) * k / n
        edge = 10.6 + 1.4 * _pnoise(x, 2, 0.3)
        if kind == "r":
            edge -= 4.5 * smooth(T - D_IN, T - D_IN + 3.6, x)
        if kind == "l":
            edge -= 4.5 * (1 - smooth(D_IN - 0.5, D_IN + 3.0, x))
        low.append((x, edge))
    poly_flat(col, "shadow", pts_top + low, 0.05, mat("grass", 0))
    for (x, y) in _spread(rnd, 3, 5.5):
        if y < 9.0 and (kind == "mid" or (kind == "l" and x > D_IN + 2) or (kind == "r" and x < T - D_IN - 2)):
            _tuft_at(col, x, y, 0.0, rnd, 1)


def build_stairs(col, part):
    """Worn stone steps cut into the rock: 4 steps over two tile rows, rock walls either side, chipped edges."""
    rnd = rng("stairs", part)
    steps = 4
    foot0 = [1.0, 9.0, 17.0, 25.0]

    def zs(x, y):
        z = 0.0
        for k in range(steps):
            f = foot0[k] + 0.5 * math.sin(x * 0.9 + k * 2.1)     # chipped, uneven nosing
            if y < f:
                return z
            t = y - f
            if t < 3.2:
                u = t / 3.2
                return z + 2.7 * (u * u * (3 - 2 * u))
            z += 2.7
            if k + 1 >= steps or y < foot0[k + 1]:
                return z + 0.3 * (t - 3.2) / 4.0
        return z

    def z_fn(x, y):
        z = zs(x, y)
        d = min(x, T - x)
        wall = 1.0 - smooth(1.0, 2.8, d)
        return z + wall * (3.2 + 0.8 * math.sin(y * 0.7 + x))

    mats = [mat("rock", 2), mat("rock", 1), mat("rock", 0)]

    def m_fn(x, y):
        d = min(x, T - x)
        if d < 2.4:
            return 1 if (int(y / 3.5) + int(x)) % 3 else 2
        for k in range(steps):
            if foot0[k] <= y < foot0[k] + 3.2:
                return 1                                           # risers in shadow
        return 0

    heightfield(col, "stairs", 0, 0, T, 32.0, 128, z_fn, m_fn, mats)
    for xc in (4.2, 11.8):                                         # moss in the cracks between steps and walls
        _tuft_at(col, xc, rnd.uniform(5, 9), zs(xc, 6.0) + 0.5, rnd, 2)


# --------------------------------------------------------------------------- bridge
def build_bridge(col, vertical, end=None):
    """Plank bridge. Middle tiles carry a frame of water under the deck (the ground layer is opaque);
    end tiles (end = 'a' or 'b') sit on the shore: the bank of a `shore` tile with the deck laid on it."""
    if end:
        role = {("h", "a"): "w", ("h", "b"): "e", ("v", "a"): "n", ("v", "b"): "s"}[("v" if vertical else "h", end)]
        build_transition(col, "shore", role)
        z0 = 1.1
    else:
        plane(col, "water", -6, -6, T + 6, T + 6, -0.8, mat("water", 1))
        plane(col, "shadow", -6, 0.2, T + 6, 3.2, -0.7, mat("water", 0))
        z0 = 0.0
    n0 = len(col.objects)
    # the deck is modelled running east-west and turned afterwards for the vertical bridge
    # (for a shore end the bank is on the west side, so a 'b' end is mirrored)
    for k in range(8):                                       # planks across the bridge
        box(col, "plank", (k * 2.0 + 1.0, 8.0, z0 + 0.55), (1.75, 10.4, 0.6), mat("wood", 1 if k % 3 else 2), bevel=0.15)
    for y in (2.1, T - 2.1):                                 # side beams and posts
        box(col, "beam", (8, y, z0 + 1.4), (T, 0.9, 0.9), mat("wood", 0), bevel=0.15)
        for x in (1.0, 9.0):
            cyl(col, "post", (x, y, z0 + 0.2), 0.5, 0.45, 2.1, mat("wood", 0), seg=6)
            blob(col, "knob", (x, y, z0 + 2.4), (0.55, 0.55, 0.4), mat("wood", 2), seed=1, rough=0, subdiv=1)
    from mathutils import Matrix
    M = Matrix.Identity(4)
    if vertical:
        M = Matrix.Translation((8, 8, 0)) @ Matrix.Rotation(math.pi / 2, 4, "Z") @ Matrix.Translation((-8, -8, 0))
    for ob in list(col.objects)[n0:]:
        ob.matrix_basis = M @ ob.matrix_basis


# --------------------------------------------------------------------------- biome ground
def t_snow(col, v):
    rnd = rng("snow", v)
    ground(col, "snow", 1)
    for i in range(3):
        lump(col, rnd.uniform(0, T), rnd.uniform(0, T), rnd.uniform(3, 4.5), rnd.uniform(1.8, 2.6), 1.2, mat("snow", 2 + (i % 2)),
             rnd.randrange(99), smooth=True, subdiv=2, rough=0.1)
    for i in range(4):
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        for dx, dy in wraps(x, y, 1):
            blob(col, "spark", (x + dx, y + dy, 0.3), (0.45, 0.45, 0.2), mat("snow", 3, emit=C.lit(1.4)), seed=1, rough=0, subdiv=1)
    if v == 1:
        for (x, y) in _spread(rnd, 3, 6):
            tuft(col, x, y, 1.5, "olive", rnd, n=4, h=2.4, lean=1.6, light=(0, 1, 0, 1))
            tuft(col, x + 1.2, y + 0.6, 1.2, "bark", rnd, n=3, h=2.0, lean=1.2, light=(2, 1, 2))


def t_sand(col, v):
    rnd = rng("sand", v)
    ground(col, "sand", 1)
    for i in range(3):
        x, y = rnd.uniform(0, T), 2.5 + i * 5.2 + rnd.uniform(-0.6, 0.6)
        ln = rnd.uniform(6, 9)
        for dx in wraps_x(x, ln):
            blob(col, "ripple", (x + dx, y, 0.0), (ln / 2, 0.9, 0.55), mat("sand", 2), seed=i + v * 7, rough=0.15, subdiv=2, smooth=True)
    pebbles(col, rnd, 3 + v * 2, ramps=("sand", "stone"), size=(0.5, 0.9))
    if v == 1:
        for (x, y) in _spread(rnd, 2, 8):
            lump(col, x, y, 1.4, 1.0, 0.7, mat("cream", 1), rnd.randrange(99), smooth=True, subdiv=2, rough=0.05)


def t_lava(col, v):
    rnd = rng("lava", v)
    ground(col, "basalt", 1)
    for i in range(4):
        lump(col, rnd.uniform(0, T), rnd.uniform(0, T), rnd.uniform(2.6, 3.6), rnd.uniform(2.0, 3.0), 0.9, mat("basalt", rnd.choice((1, 2))),
             rnd.randrange(99), rough=0.3, subdiv=2)
    for i in range(2 + v):
        x0, y0 = rnd.uniform(0, T), rnd.uniform(0, T)
        pts = []
        x, y = x0, y0
        for k in range(7):
            pts.append((x, y, 0.15))
            x += rnd.uniform(0.8, 2.2)
            y += rnd.uniform(-1.6, 1.6)
        for dx, dy in wraps(x0 + 3, y0, 8):
            tube(col, "crack", [(px + dx, py + dy, pz) for px, py, pz in pts], [0.3, 0.55, 0.65, 0.6, 0.55, 0.4, 0.2], mat("lava", 2, emit=2.0), seg=4)
    for _ in range(3):
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        for dx, dy in wraps(x, y, 1):
            blob(col, "ember", (x + dx, y + dy, 0.5), (0.4, 0.4, 0.3), mat("lava", 3, emit=2.5), seed=1, rough=0, subdiv=1)


def t_cloud(col, v):
    rnd = rng("cloud", v)
    ground(col, "cloud", 1)
    for i in range(4):
        lump(col, rnd.uniform(0, T), rnd.uniform(0, T), rnd.uniform(3.0, 4.6), rnd.uniform(2.2, 3.2), 1.9, mat("cloud", 3 if i % 2 else 2),
             rnd.randrange(99), smooth=True, subdiv=2, rough=0.12)
    for _ in range(3):
        x, y = rnd.uniform(0.5, 15.5), rnd.uniform(0.5, 15.5)
        for dx, dy in wraps(x, y, 1):
            blob(col, "spark", (x + dx, y + dy, 1.0), (0.4, 0.4, 0.2), mat("cloud", 3, emit=C.lit(1.6)), seed=1, rough=0, subdiv=1)


# --------------------------------------------------------------------------- registry
SIDES = ["nw", "n", "ne", "w", "e", "sw", "s", "se"]
INNERS = ["in_nw", "in_ne", "in_sw", "in_se"]


def assets():
    out = []

    def add(id_, w, h, fn, slices):
        out.append(dict(id=id_, w=w, h=h, build=fn, slices=slices, group="terrain"))

    for pair, pre in (("path", "grass_path"), ("dirt", "grass_dirt"), ("shore", "shore")):
        for role in SIDES + INNERS:
            n = f"{pre}_{role}"
            add(n, 1, 1, (lambda col, pair=pair, role=role: build_transition(col, pair, role)), [(n, 0, 0)])
    if C.DETAIL > 1:
        for pair, pre in (("path", "grass_path"), ("dirt", "grass_dirt")):
            for role in EXTRA_ROLES:
                n = f"{pre}_{role}"
                add(n, 1, 1, (lambda col, pair=pair, role=role: build_transition(col, pair, role)), [(n, 0, 0)])
    if C.DETAIL > 1:
        for pair, pre in (("stone", "grass_stone"), ("plaza", "grass_plaza"), ("dark", "grass_dark"), ("ink", "dark_ink")):
            for role in SIDES + INNERS + EXTRA_ROLES:
                n = f"{pre}_{role}"
                add(n, 1, 1, (lambda col, pair=pair, role=role: build_transition(col, pair, role)), [(n, 0, 0)])
        for role in SIDES + INNERS:
            n = f"realm_edge_{role}"
            add(n, 1, 1, (lambda col, role=role: build_realm_edge(col, role)), [(n, 0, 0)])
    for role in ("nw", "n", "ne", "w", "e"):
        n = f"cliff_{role}"
        add(n, 1, 1, (lambda col, role=role: build_plateau_edge(col, role)), [(n, 0, 0)])
    for kind, v, suffix in (("mid", 0, ""), ("mid", 1, "2"), ("l", 0, "_l"), ("r", 0, "_r")):
        a, b = f"cliff_face_a{suffix}", f"cliff_face_b{suffix}"
        add(f"face{suffix or '1'}", 1, 2, (lambda col, kind=kind, v=v: build_face(col, kind, v)), [(a, 0, 0), (b, 0, 1)])
    add("stairs", 1, 2, (lambda col: build_stairs(col, 0)), [("stairs_a", 0, 0), ("stairs_b", 0, 1)])
    for kind, suffix in (("mid", ""), ("l", "_l"), ("r", "_r")):
        add(f"cshadow{suffix or '_m'}", 1, 1, (lambda col, kind=kind: build_cliff_shadow(col, kind)), [(f"cliff_shadow{suffix}", 0, 0)])
    for v in range(3):
        add(f"plateau_top_{v}", 1, 1, (lambda col, v=v: wt_base.b_grass(col, v, seed_off=77, base_step=2)), [(f"plateau_top_{v}", 0, 0)])
    add("bridge_h", 1, 1, (lambda col: build_bridge(col, False)), [("bridge_h", 0, 0)])
    add("bridge_v", 1, 1, (lambda col: build_bridge(col, True)), [("bridge_v", 0, 0)])
    for v, e, n in ((False, "a", "bridge_h_w"), (False, "b", "bridge_h_e"), (True, "a", "bridge_v_n"), (True, "b", "bridge_v_s")):
        add(n, 1, 1, (lambda col, v=v, e=e: build_bridge(col, v, e)), [(n, 0, 0)])
    for v in (0, 1):
        add(f"snow_{v}", 1, 1, (lambda col, v=v: t_snow(col, v)), [(f"snow_{v}", 0, 0)])
        add(f"sand_{v}", 1, 1, (lambda col, v=v: t_sand(col, v)), [(f"sand_{v}", 0, 0)])
        add(f"lava_rock_{v}", 1, 1, (lambda col, v=v: t_lava(col, v)), [(f"lava_rock_{v}", 0, 0)])
        add(f"cloud_{v}", 1, 1, (lambda col, v=v: t_cloud(col, v)), [(f"cloud_{v}", 0, 0)])
    return out
