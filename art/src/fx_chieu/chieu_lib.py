"""Building blocks for the fx_chieu batch.  Runs INSIDE Blender (headless).

Imports art/src/fx/fxlib.py and art/src/fx_kiem/kiem_lib.py (both read only, never edited).

Conventions of this batch
- Shapes are built in SPRITE PIXELS, relative to the sheet's pivot, y up (MB in px); `CFx.obj` scales the mesh by
  1/32 (1 unit = 32 px, zoom 1.0) and puts its origin on the pivot.  Every animated value given to `CFx.anim` is in px
  relative to the pivot too.
- Layers inside a scene are alpha-blended in the render (emission over transparent, z order per material) so a white
  core sits ON a coloured body instead of adding to it (stacked additive colours drift to pink / mud in the palette
  snap; see fx_kiem's README).  The packed sheet is blend 'add' or 'alpha' as declared.
- Frames need not be square: CFx(..., px=96, h=32) renders a 96x32 strip (loi_xich).
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for d in (os.path.join(HERE, "..", "fx"), os.path.join(HERE, "..", "fx_kiem")):
    if d not in sys.path:
        sys.path.insert(0, d)
from fxlib import *            # noqa: F401,F403  MB, Fx, TAU, PI, jag, ease_out, ...
from fxlib import Fx, MB, TAU, PI, jag
from kiem_lib import RAMP, crack, star4, rune_marks, flame_tongue, bolt_line   # noqa: F401

P = 1 / 32.0
KY = math.sin(math.radians(35))        # a ground circle seen from 35 deg: y squashed by this
D = math.radians

# element -> glow ramp [halo far, halo near, glow edge, glow core]  (art/palette.json glow ramps)
EL = {
    "kim": RAMP["holy"],
    "moc": RAMP["verdant"],
    "thuy": RAMP["ice"],
    "hoa": RAMP["flame"],
    "tho": ["#7a4c0e", "#b9821a", "#e6b83a", "#fff0a0"],          # gold solid ramp: ochre earth light
    "loi": RAMP["cosmic"],
}
WHITE = "#fffbe4"


class CFx(Fx):
    def __init__(self, id, px=96, h=None, pivot=None, mode="alpha", view="front", frames=6, fps=12, loop=False,
                 ground=False, halo=0.6, name_vi="", ramps=None, alpha_levels=4, gamma=1.0, where=""):
        super().__init__(id, view=view, frames=frames, fps=fps, loop=loop, mode=mode, px=px, ground=ground,
                         pivot=pivot, halo=halo, name_vi=name_vi, alpha_levels=alpha_levels, gamma=gamma, zoom=1.0,
                         where=where)
        self.w = px
        self.h = h or px
        if h:
            self.sc.render.resolution_y = self.h * 6
        self.pivot = pivot or (self.w // 2, self.h // 2)
        self.ox = (self.pivot[0] - self.w / 2) * P
        self.oy = (self.h / 2 - self.pivot[1]) * P
        if view != "front":
            # ground / top view: the plane is world XY, the frame's vertical maps to Y (squashed by sin35 on ground)
            self.oy /= (KY if view == "ground" else 1.0)
        self.ramps = ramps
        self.rng = random.Random(sum(ord(c) * (i + 3) for i, c in enumerate(id)))

    # materials: alpha layering inside the scene, z order given explicitly
    def mat(self, name, color, z=0.0, **kw):
        kw.setdefault("mode", "alpha")
        fm = super().mat(name, color, **kw)
        # front: depth along the camera axis (no screen shift, ortho); ground/top: a hair above the plane
        # (lifting more would shift the shape up on screen)
        fm.z = (z * 0.005) if self.view != "front" else -z * 0.05
        return fm

    def reg(self, ob, fm, x, y, z):
        super().reg(ob, fm, x, y, getattr(fm, "z", z))

    # objects in px
    def obj(self, mb, name, fm):
        mb.xform(sx=P, sy=P)
        return mb.build(self, name, fm, self.ox, self.oy)

    def _conv(self, d):
        if d is None:
            return dict(show=False)
        d = dict(d)
        d["x"] = self.ox + d.get("x", 0.0) * P
        d["y"] = self.oy + d.get("y", 0.0) * P
        for k in ("s", "sx", "sy"):
            if k in d:
                d[k] = max(d[k], 1e-3)
        return d

    def anim(self, ob, fn):
        """fn(t, i) -> dict(x, y [px from pivot], s, sx, sy, rot, op, head, tail, show, dz) or None (hidden).
        dz = extra depth for this object (bigger = nearer the camera), on top of its material's z order: used to
        sort whole objects (each spike / rock) front to back."""
        z0 = self.state[ob.name]["fm"].z

        def f(t, i):
            d = fn(t, i)
            if d is not None and "dz" in d:
                d = dict(d)
                dz = d.pop("dz")
                d["z"] = z0 + (dz * 0.004 if self.view != "front" else -dz * 0.3)
            return self._conv(d)
        return self.track(ob, f)

    def still(self, mb, name, fm, fn=None):
        ob = self.obj(mb, name, fm)
        self.anim(ob, fn or (lambda t, i: {}))
        return ob

    def pf(self, name, fm, builder):
        """one mesh per frame: builder(t, i) -> MB in px (or None), visible only on its own frame."""
        obs = []
        for i in range(self.N):
            mb = builder(self.T(i), i)
            if mb is None or not mb.v:
                continue
            ob = self.obj(mb, "%s_%02d" % (name, i), fm)
            self.anim(ob, (lambda ii: (lambda t, i2: {} if i2 == ii else None))(i))
            obs.append(ob)
        return obs

    def particle(self, name, fm, mb, fn):
        """small object; fn(t, i) -> (x, y, scale, rot) in px or None."""
        ob = self.obj(mb, name, fm)

        def f(t, i):
            r = fn(t, i)
            if r is None:
                return None
            x, y, s, rot = r
            if s <= 0.02:
                return None
            return dict(x=x, y=y, s=s, rot=rot)
        return self.anim(ob, f)


# ----------------------------------------------------------------------------- timing helpers
def sat(x):
    return max(0.0, min(1.0, x))


def ease_out(t):
    return 1 - (1 - sat(t)) ** 3


def ease_in(t):
    return sat(t) ** 2


def bump(t, a, b):
    """0 outside [a, b], sin bump inside."""
    if t <= a or t >= b:
        return 0.0
    return math.sin(PI * (t - a) / (b - a))


def ramp_up(t, a, b):
    return sat((t - a) / max(b - a, 1e-6))


# ----------------------------------------------------------------------------- shapes (all in px, y up)
def rot_pts(pts, ang, dx=0.0, dy=0.0, sx=1.0, sy=1.0):
    ca, sa = math.cos(ang), math.sin(ang)
    return [((x * ca - y * sa) * sx + dx, (x * sa + y * ca) * sy + dy) for x, y in pts]


def sword_pts(L, W):
    """blade of a jian pointing +x: from the guard (x=0) to the tip (x=L), width W, a sharp point."""
    return [(0, -W / 2), (L * 0.80, -W / 2), (L, 0), (L * 0.80, W / 2), (0, W / 2)]


def sword(mb, x, y, ang, L, W, guard=True, grip=True, scale=1.0):
    """a whole sword (blade, guard, grip, pommel) along `ang` with the guard at (x, y)."""
    L, W = L * scale, W * scale
    mb.poly(rot_pts(sword_pts(L, W), ang, x, y))
    if guard:
        g = [(-W * 0.45, -W * 1.5), (W * 0.45, -W * 1.5), (W * 0.45, W * 1.5), (-W * 0.45, W * 1.5)]
        mb.poly(rot_pts(g, ang, x, y))
    if grip:
        gl = L * 0.22
        g = [(-gl, -W * 0.32), (0, -W * 0.32), (0, W * 0.32), (-gl, W * 0.32)]
        mb.poly(rot_pts(g, ang, x, y))
        cx, cy = rot_pts([(-gl - W * 0.35, 0)], ang, x, y)[0]
        mb.diamond(cx, cy, W * 1.0, W * 1.0, ang)
    return mb


def blade_core(mb, x, y, ang, L, W, scale=1.0):
    """the white-hot ridge line of a blade."""
    L, W = L * scale, W * scale
    pts = [(L * 0.04, -W * 0.16), (L * 0.84, -W * 0.12), (L * 0.97, 0), (L * 0.84, W * 0.12), (L * 0.04, W * 0.16)]
    return mb.poly(rot_pts(pts, ang, x, y))


def ellipse_pts(cx, cy, rx, ry, n=40, a0=0.0, a1=TAU):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def ring_e(mb, cx, cy, rx, ry, w, a0=0.0, a1=TAU, soft=False, n=None):
    n = n or max(12, int(64 * abs(a1 - a0) / TAU))
    pts = ellipse_pts(cx, cy, rx, ry, n, a0, a1)
    if abs(abs(a1 - a0) - TAU) < 1e-6:
        pts[-1] = pts[0]
    return mb.strip(pts, w, soft=soft)


def spike(mb, x, y, h, w, lean=0.0, facet=None):
    """a crystal / earth spike standing on (x, y), tip up (lean tilts the tip sideways)."""
    pts = [(x - w / 2, y), (x + w / 2, y), (x + lean + w * 0.06, y + h), (x + lean - w * 0.06, y + h)]
    mb.poly(pts)
    return mb


def spike_facet(mb, x, y, h, w, lean=0.0):
    """the lit left facet of a spike."""
    pts = [(x - w / 2 + w * 0.1, y + h * 0.04), (x - w * 0.02, y + h * 0.04), (x + lean - w * 0.02, y + h * 0.92)]
    return mb.poly(pts)


def grow_poly(mb, pts, k):
    """polygon scaled by k about its first point (used for 1px dark outlines behind a shape: k > 1)."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return mb.poly([(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts])


def offset_poly(pts, d):
    """grow a convex-ish polygon outwards by d px along its vertex normals (for outlines)."""
    n = len(pts)
    out = []
    for i in range(n):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        e1 = (x1 - x0, y1 - y0)
        e2 = (x2 - x1, y2 - y1)
        def nrm(e):
            L = math.hypot(*e) or 1.0
            return (e[1] / L, -e[0] / L)
        n1, n2 = nrm(e1), nrm(e2)
        nx, ny = n1[0] + n2[0], n1[1] + n2[1]
        L = math.hypot(nx, ny) or 1.0
        nx, ny = nx / L, ny / L
        dot = max(0.35, nx * n1[0] + ny * n1[1])
        out.append((x1 + nx * d / dot, y1 + ny * d / dot))
    # (e_y, -e_x) points outwards for a counter-clockwise polygon (positive area); clockwise -> flip
    area = sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(n))
    if area < 0:
        out = [(2 * pts[i][0] - out[i][0], 2 * pts[i][1] - out[i][1]) for i in range(n)]
    return out


def leaf(mb, x, y, ang, L, W):
    """a pointed leaf (lens) from (x, y) along ang."""
    n = 8
    up, dn = [], []
    for k in range(n + 1):
        s = k / n
        w = W / 2 * math.sin(PI * s) ** 0.8
        up.append((L * s, w))
        dn.append((L * s, -w))
    pts = up + dn[::-1][1:-1]
    return mb.poly(rot_pts(pts, ang, x, y))


def curve_strip(mb, pts, w0, w1, soft=False, pw=1.0):
    n = len(pts) - 1
    ws = [w0 + (w1 - w0) * (k / n) ** pw for k in range(n + 1)]
    return mb.strip(pts, ws, soft=soft)


def bezier(p0, p1, p2, p3, n=16):
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def set_u_range(mb, b, u):
    for k in range(b, len(mb.v)):
        mb.u[k] = u


def bolt(mb, p0, p1, rng, w, n=8, amp=None, branches=1, taper=0.6, blen=0.35):
    """jagged lightning from p0 to p1 (px)."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    pts = jag(p0, p1, rng, n, amp if amp is not None else L * 0.12)
    mb.strip(pts, [w * (1 - taper * k / n) + 0.3 for k in range(len(pts))])
    for _ in range(branches):
        k = rng.randint(1, n - 2)
        x, y = pts[k]
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + rng.choice((-1, 1)) * rng.uniform(0.5, 1.0)
        l2 = L * rng.uniform(0.5, 1.0) * blen
        q = jag((x, y), (x + l2 * math.cos(ang), y + l2 * math.sin(ang)), rng, 4, l2 * 0.25)
        mb.strip(q, [w * 0.55 * (1 - 0.7 * k2 / 4) + 0.3 for k2 in range(len(q))])
    return pts
