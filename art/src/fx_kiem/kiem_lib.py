"""Shape helpers for the fx_kiem batch.  Runs INSIDE Blender (imports art/src/fx/fxlib.py, never edits it).

All shapes are 2D (x right, y up) in Blender units; 1 unit = 32 sprite px (Fx(..., zoom=1.0)).
Every builder here adds geometry to an fxlib.MB with a per-vertex `u` (0..1 along the swing), so the
material sweep window (head / tail keys) reveals and eats the whole swing, spikes and all, together.
"""
import math
import random
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FXDIR = os.path.join(HERE, "..", "fx")
if FXDIR not in sys.path:
    sys.path.insert(0, FXDIR)
from fxlib import *          # noqa: F401,F403  (MB, Fx, TAU, PI, jag, ease_out, ...)

P = 1 / 32.0                 # one sprite pixel in units


# ----------------------------------------------------------------------------- palette (art/palette.json only)
RAMP = {   # glow ramps [halo far, halo near, glow edge, glow core]
    "spirit": ["#0e5a78", "#18a0c8", "#5ae0f4", "#d8fcff"],
    "flame": ["#8a2a08", "#e0601a", "#ffae3a", "#fff2b0"],
    "ice": ["#3a6ab0", "#6aa8e8", "#b0dcff", "#f2fbff"],
    "cosmic": ["#4a1890", "#8a3ce0", "#c88cff", "#f6e6ff"],
    "holy": ["#9a6410", "#e8b02a", "#ffe27a", "#fffbe4"],
    "verdant": ["#0e6a3a", "#22b05a", "#7aec9a", "#e4ffe8"],
    "thunder": ["#34349a", "#6a6af0", "#b8c0ff", "#f8f8ff"],
    "steel": ["#34405a", "#5d6e86", "#94a6ba", "#dbe6ef"],      # solid ramp entries 1..4 (low tiers: no glow)
    "bone": ["#5a5866", "#9894a2", "#cfcbd3", "#f6f4f7"],
}


# ----------------------------------------------------------------------------- arc geometry
ARC_K = [1.0, 1.0]          # the swing is an ellipse: x / y stretch of every arc point (set by the builder)


def arc_point(R, a0, a1, u):
    a = a0 + (a1 - a0) * u
    return R * math.cos(a) * ARC_K[0], R * math.sin(a) * ARC_K[1], a


def wisps(mb, R, a0, a1, wmax, n, rng, prof, w_px=1.5, length=0.22, inward=0.9, u0=0.22, u1=0.97):
    """Streaks peeling off the inner edge of the crescent and trailing back against the swing:
    the drawn speed of manhua sword qi.  Each streak tapers to a point; u follows the swing."""
    for j in range(n):
        us = u0 + (u1 - u0) * (j + rng.uniform(0.1, 0.9)) / n
        L = length * rng.uniform(0.6, 1.0)
        m = 10
        pts, ws, us_ = [], [], []
        for k in range(m + 1):
            s = k / m
            u = max(0.0, us - L * s)
            w = wmax * prof(us)
            r = R - w * (0.15 + inward * s * rng.uniform(0.7, 1.0)) * (0.6 + 0.4 * math.sin(PI * s * 0.5))
            x, y, _ = arc_point(r, a0, a1, u)
            pts.append((x, y))
            ws.append(w_px * P * (1 - s) ** 0.8 + 0.004)
            us_.append(u)
        b = len(mb.v)
        mb.strip(pts, ws)
        for k in range(m + 1):
            for q in range(3):
                mb.u[b + 3 * k + q] = us_[k]
    return mb


def crescent(mb, R, a0, a1, wmax, n=48, off=0.0, prof=None, jit=0.0, rng=None, soft=False, gside=None):
    """Swing crescent around the origin (the hand), from angle a0 (u=0, start of the swing) to a1 (u=1).
    prof(u) -> 0..1 width profile (default: thin start, fat 2/3 of the way, sharp end).
    gside='out': g = 1 on the outer (cutting) edge, fading to 0 on the inner edge (a crescent-moon smear);
    valid for clockwise arcs (a1 < a0), whose strip normal points outwards."""
    prof = prof or (lambda u: math.sin(PI * u) ** 0.7 * (0.3 + 0.7 * u ** 0.9))
    pts, ws = [], []
    for k in range(n + 1):
        u = k / n
        r = R + off + ((rng.uniform(-jit, jit) if (rng and 0 < k < n) else 0.0))
        x, y, a = arc_point(r, a0, a1, u)
        pts.append((x, y))
        ws.append(wmax * prof(u) + 0.006)
    b = len(mb.v)
    mb.strip(pts, ws, soft=soft)
    if gside == "out":
        for k in range(n + 1):
            mb.g[b + 3 * k], mb.g[b + 3 * k + 1], mb.g[b + 3 * k + 2] = 1.0, 0.72, 0.0
    return mb


def torn_edge(mb, R, a0, a1, wmax, count, length, rng, prof=None, side=1, u0=0.12, u1=0.97, lean=0.0, width=0.6):
    """Ragged spikes on the outer (side=1) or inner (side=-1) edge of a crescent: the torn edge of the qi.
    Each spike is a triangle whose base sits on the crescent edge; `u` follows the swing."""
    prof = prof or (lambda u: math.sin(PI * u) ** 0.7 * (0.3 + 0.7 * u ** 0.9))
    for j in range(count):
        u = u0 + (u1 - u0) * (j + rng.uniform(0.15, 0.85)) / count
        w = wmax * prof(u)
        if w < 0.02:
            continue
        x, y, a = arc_point(R + side * w * 0.42, a0, a1, u)
        nx, ny = math.cos(a) * side, math.sin(a) * side
        tx, ty = -math.sin(a), math.cos(a)                    # along the swing direction (a decreasing = clockwise)
        if a1 < a0:
            tx, ty = -tx, -ty
        L = length * rng.uniform(0.45, 1.0) * (0.4 + 0.6 * prof(u))
        bw = max(w * width, 1.6 * P) * rng.uniform(0.6, 1.0)
        # tip leans back against the swing (wind-torn)
        tipx = x + nx * L - tx * L * lean
        tipy = y + ny * L - ty * L * lean
        b0 = (x - tx * bw / 2 - nx * w * 0.2, y - ty * bw / 2 - ny * w * 0.2)
        b1 = (x + tx * bw / 2 - nx * w * 0.2, y + ty * bw / 2 - ny * w * 0.2)
        mb._add([b0, b1, (tipx, tipy)], [(0, 1, 2)], [1.0] * 3, [u] * 3)
    return mb


def speed_lines(mb, R, a0, a1, offs, w, u_span=(0.05, 0.85)):
    """Thin parallel hair-lines inside / outside the crescent (the drawn speed of the swing)."""
    for off, ua, ub in offs:
        n = 24
        pts, ws, us = [], [], []
        for k in range(n + 1):
            s = k / n
            u = ua + (ub - ua) * s
            x, y, a = arc_point(R + off, a0, a1, u)
            pts.append((x, y))
            ws.append(w * math.sin(PI * s) ** 0.6 + 0.004)
        b = len(mb.v)
        mb.strip(pts, ws)
        # re-write u to follow the swing (strip() writes 0..1 along its own length)
        for k in range(n + 1):
            u = ua + (ub - ua) * k / n
            for q in range(3):
                mb.u[b + k * 3 + q] = u
    return mb


def lightning_on_arc(mb, R, a0, a1, wmax, rng, n_bolts=2, w=0.035, span=0.35, prof=None, branch=True, ulo=0.15, uhi=0.95):
    """Jagged bolts crawling along the body of the crescent (a fresh pattern per call), inside u in [ulo, uhi]."""
    prof = prof or (lambda u: math.sin(PI * u) ** 0.7 * (0.3 + 0.7 * u ** 0.9))
    span = min(span, max(0.08, uhi - ulo))
    for _ in range(n_bolts):
        ua = rng.uniform(ulo, max(ulo, uhi - span))
        ub = ua + span * rng.uniform(0.7, 1.0)
        m = 9
        pts = []
        for k in range(m + 1):
            u = ua + (ub - ua) * k / m
            off = rng.uniform(-0.5, 0.5) * wmax * prof(u) * 1.25 if 0 < k < m else 0.0
            x, y, _ = arc_point(R + off, a0, a1, u)
            pts.append((x, y))
        mb.strip(pts, [w] * len(pts))
        if branch and rng.random() < 0.8:
            k = rng.randint(2, m - 2)
            x, y = pts[k]
            ang = math.atan2(y, x) + rng.uniform(-0.5, 0.5)
            L = wmax * rng.uniform(0.9, 1.6)
            mb.strip(jag((x, y), (x + L * math.cos(ang), y + L * math.sin(ang)), rng, 4, L * 0.25), [w * 0.8, w * 0.7, w * 0.6, w * 0.45, w * 0.3])
    return mb


def bolt_line(mb, p0, p1, rng, w, n=7, amp=None, branches=1):
    """Free lightning bolt from p0 to p1 with tapering width and small branches."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    pts = jag(p0, p1, rng, n, amp if amp is not None else L * 0.18)
    mb.strip(pts, [w * (1 - 0.6 * k / n) for k in range(len(pts))])
    for _ in range(branches):
        k = rng.randint(1, n - 2)
        x, y = pts[k]
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + rng.choice((-1, 1)) * rng.uniform(0.5, 1.1)
        l2 = L * rng.uniform(0.25, 0.45)
        q = jag((x, y), (x + l2 * math.cos(ang), y + l2 * math.sin(ang)), rng, 4, l2 * 0.25)
        mb.strip(q, [w * 0.6 * (1 - 0.7 * k2 / 4) for k2 in range(len(q))])
    return mb


def crack(mb, p0, ang, L, rng, w, depth=2):
    """A branching crack in space (void crack): jagged, forks once or twice."""
    p1 = (p0[0] + L * math.cos(ang), p0[1] + L * math.sin(ang))
    pts = jag(p0, p1, rng, 5, L * 0.16)
    mb.strip(pts, [w * (1 - 0.75 * k / 5) for k in range(len(pts))])
    if depth > 0:
        k = rng.randint(2, 4)
        crack(mb, pts[k], ang + rng.choice((-1, 1)) * rng.uniform(0.45, 0.9), L * rng.uniform(0.35, 0.55), rng, w * 0.6, depth - 1)
    return mb


def star4(mb, cx, cy, r, thin=0.18, rot=PI / 2):
    return mb.star(cx, cy, 4, r, r * thin, rot)


def rune_marks(mb, pts_angles, size, rng, w):
    """Abstract rune strokes (random strokes on a 3x3 grid, never glyphs) at the given (x, y, angle)."""
    grid = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for (px, py, rot) in pts_angles:
        ca, sa = math.cos(rot), math.sin(rot)
        used = set()
        for _ in range(rng.randint(2, 4)):
            p, q = rng.sample(grid, 2)
            if (p, q) in used or (q, p) in used:
                continue
            used.add((p, q))
            a = (px + (p[0] * ca - p[1] * sa) * size * 0.5, py + (p[0] * sa + p[1] * ca) * size * 0.5)
            b = (px + (q[0] * ca - q[1] * sa) * size * 0.5, py + (q[0] * sa + q[1] * ca) * size * 0.5)
            mb.line(a, b, w)
    return mb


def flame_tongue(mb, base, ang, h, w, sway, u=0.0):
    """Flame tongue standing on `base`, pointing along `ang` (radians), S-bent by sway (a tapered strip)."""
    seg = 8
    ca, sa = math.cos(ang), math.sin(ang)
    pts, ws = [], []
    for i in range(seg + 1):
        s = i / seg
        ws.append(w * (math.sin(PI * min(1.0, s * 0.85 + 0.15)) ** 0.8) * (1 - s) ** 0.6 + w * 0.03)
        lx, ly = h * s, sway * math.sin(s * PI * 1.3) * s
        pts.append((base[0] + lx * ca - ly * sa, base[1] + lx * sa + ly * ca))
    b = len(mb.v)
    mb.strip(pts, ws)
    for k in range(b, len(mb.v)):
        mb.u[k] = u
    return mb


def set_u(mb, b, u):
    for k in range(b, len(mb.v)):
        mb.u[k] = u
