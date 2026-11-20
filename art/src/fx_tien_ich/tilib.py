"""Shared helpers of the fx_tien_ich batch.  Runs INSIDE Blender.  Imports the FX library of art/src/fx
(fxlib.py, fxpost.py) by path and never edits it: everything new is a subclass or a helper here.

FxP        = Fx whose local (0, 0) is the sprite PIVOT (not the frame centre), so builders can think in
             "units from the pivot" (1 unit = 32 px, y up).  Ground-view objects can be made billboards
             (they face the 35 degree camera, so dust puffs stay round instead of becoming flat ellipses).
column()   = a soft light column mesh (width across, fade along).
mote()     = one small particle animated by fn(t) -> (x, y, s[, rot[, z]]) | None.
"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fx"))
from fxlib import *          # noqa: E402,F401  (Fx, MB, make_mat, ELEM, runes, jag, ease_*, sat, PI, TAU, math, random, np, bpy)

TILT = math.radians(90 - 35)  # a plane turned to face the 35 degree ground camera


class FxP(Fx):
    def __init__(self, id, **kw):
        super().__init__(id, **kw)
        self.ppu = self.px / self.sc.camera.data.ortho_scale
        self.ox = (self.pivot[0] - self.px / 2) / self.ppu
        self.oy = (self.px / 2 - self.pivot[1]) / self.ppu
        self.bb = set()

    def billboard(self, ob):
        self.bb.add(ob.name)
        self._place(ob)
        return ob

    def _place(self, ob):
        s = self.state[ob.name]
        if self.view == "front":
            ob.location = (s["x"] + self.ox, s["z"], s["y"] + self.oy)
            ob.rotation_euler = (PI / 2, 0, s["rot"])
        elif ob.name in self.bb:
            ob.location = (s["x"], s["y"], s["z"])
            ob.rotation_euler = (TILT, 0, s["rot"])
        else:
            ob.location = (s["x"], s["y"], s["z"])
            ob.rotation_euler = (0, 0, s["rot"])
        ob.scale = (s["sx"], s["sy"], 1.0)


def px(n):
    """pixels -> units"""
    return n / PXU


# ------------------------------------------------------------------------------------ shapes
def column(w, h, rows=10, taper=0.4, p=1.0, spine=1.0, base=1.0, y0=0.0, rise=0.35):
    """soft light column, base at y = 0 going up to y = h.  g: 0 at both sides, `spine` on the middle
    line, multiplied by (1 - row/rows)^p so it fades towards the top."""
    mb = MB()
    verts, g, u, faces = [], [], [], []
    for k in range(rows + 1):
        s = k / rows
        hw = w * 0.5 * (1 - taper * s)
        y = y0 + h * s
        f = spine * (1 - s) ** p * (base + (1 - base) * min(1.0, s / rise)) * min(1.0, (1 - s) / 0.18)
        verts += [(-hw, y), (0, y), (hw, y)]
        g += [0.0, f, 0.0]
        u += [s] * 3
    for k in range(rows):
        a = k * 3
        faces += [(a, a + 1, a + 4, a + 3), (a + 1, a + 2, a + 5, a + 4)]
    return mb._add(verts, faces, g, u)


def glow_disc(r, seg=28):
    return MB().disc(0, 0, r, seg, 1.0, 0.0)


def shape(mb, kind, size):
    if kind == "disc":
        mb.disc(0, 0, size, 10)
    elif kind == "diamond":
        mb.diamond(0, 0, size * 2.2, size)
    elif kind == "star":
        mb.star(0, 0, 4, size, size * 0.2, PI / 2)
    elif kind == "star8":
        mb.star(0, 0, 8, size, size * 0.3, PI / 8)
    elif kind == "leaf":
        mb.diamond(0, 0, size * 2.6, size * 1.1)
    elif kind == "drop":
        mb.drop(0, 0, size * 2.2, size)
    return mb


def mote(fx, name, fm, kind, size, fn, billboard=False):
    ob = shape(MB(), kind, size).build(fx, name, fm)
    if billboard:
        fx.billboard(ob)

    def f(t, i):
        r = fn(t)
        if r is None:
            return None
        d = dict(x=r[0], y=r[1], s=max(r[2], 1e-3))
        if len(r) > 3:
            d["rot"] = r[3]
        if len(r) > 4:
            d["z"] = r[4]
        return d
    return fx.track(ob, f)


def rising(x0, y0, h, ph, sway=0.05, size=1.0, pw=0.7):
    """loops cleanly: born at y0, climbs h, shrinks away (phase ph)."""
    def fn(t):
        s = (t + ph) % 1.0
        return (x0 + sway * math.sin(TAU * (t + ph) * 1.0), y0 + h * s, size * math.sin(PI * s) ** pw)
    return fn


def burst_mote(x0, y0, vx, vy, t0, life, g=0.0, size=1.0, pw=0.6, spin=0.0):
    """one-shot ballistic particle born at t0 (0..1), lives `life`."""
    def fn(t):
        a = (t - t0) / life
        if a < 0 or a > 1:
            return None
        return (x0 + vx * a, y0 + vy * a + 0.5 * g * a * a, size * (1 - a) ** pw, spin * a)
    return fn


def ring_arcs(mb, r, w, n, gap, a0=0.0, ky=1.0):
    """n dashes around a circle, `gap` = fraction of each slot left empty."""
    for k in range(n):
        s = a0 + TAU * k / n
        mb.ring(0, 0, r, w, s, s + TAU / n * (1 - gap), seg=10, ky=ky)
    return mb
