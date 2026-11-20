"""B. Loot glow by rarity: roi_cot_<r> (light column on a dropped weapon), roi_vong_<r> (pulsing ground ring),
roi_nhat (pick-up flash).  5 rarities, told apart by hue AND by shape AND by strength:

  pham   grey     faint shimmer: two twinkling glints + a haze, NO column;  dashed ring
  linh   green    short soft column, 3 round motes;                           plain ring
  huyen  blue     taller column + bright core line, diamond motes;           ring + 4 ticks
  dia    purple   tall column + two crossing side blades, star motes;        double ring + 6 nodes
  thien  gold     tallest column, slow orbiting halo, crown star, ground star; double ring + 8-ray star

Units: 1 unit = 28.6 px here (the camera has a 12 % margin).  Column base = the sprite pivot (48, 84)."""
import math
from tilib import *

REG = {}
RAR = ("pham", "linh", "huyen", "dia", "thien")
C = {  # body (glow edge), mid, core -> all are glow-ramp colours; the palette snap picks the exact step
    "pham": dict(vi="Phàm", body="#8a8f9c", mid="#b8bdc3", core="#e8ecf0"),
    "linh": dict(vi="Linh", body="#22b05a", mid="#7aec9a", core="#e4ffe8"),
    "huyen": dict(vi="Huyền", body="#6aa8e8", mid="#b0dcff", core="#f2fbff"),
    "dia": dict(vi="Địa", body="#8a3ce0", mid="#c88cff", core="#f6e6ff"),
    "thien": dict(vi="Thiên", body="#e8b02a", mid="#ffe27a", core="#fffbe4"),
}
HEIGHT = dict(pham=0.9, linh=1.4, huyen=1.85, dia=2.25, thien=2.6)
WIDTH = dict(pham=0.5, linh=0.62, huyen=0.74, dia=0.84, thien=0.92)


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


def sliver(fx, name, fm, x0, h, ph, size=0.1, y0=0.1):  # noqa
    return mote(fx, name, fm, "diamond", size,
                lambda t: (x0, y0 + h * ((t + ph) % 1), math.sin(PI * ((t + ph) % 1)) ** 0.8, PI / 2))


def make_cot(r):
    c = C[r]
    fx = FxP("roi_cot_" + r, frames=8, fps=8, loop=True, px=96, pivot=(48, 84), halo=0.5,
             name_vi="Ánh quang rơi đồ " + c["vi"],
             where="soft column of light standing on a dropped weapon of grade %s (pivot = base of the column)" % c["vi"])
    rng = fx.rng
    H, W = HEIGHT[r], WIDTH[r]
    body = fx.mat("body", c["body"], grad=dict(src="attr", pow=1.0, cpow=2.2), core=c["mid"])
    core = fx.mat("core", c["core"], grad=dict(src="attr", pow=0.6))
    solid = fx.mat("solid", c["core"])
    midm = fx.mat("mid", c["mid"], grad=dict(src="attr", pow=0.7))
    bloom = fx.mat("bloom", c["body"], grad=dict(src="attr", pow=1.3))
    pulse = lambda t, ph=0.0: 0.5 + 0.5 * math.sin(TAU * t + ph)

    if r == "pham":
        # a faint haze and two twinkling glints: a shimmer, no pillar
        o = column(0.42, 0.75, taper=0.6, p=0.9, spine=0.4).build(fx, "haze", body)
        fx.track(o, lambda t, i: dict(op=0.4 + 0.2 * pulse(t)))
        for j, (x, y, ph) in enumerate(((-0.3, 0.55, 0.0), (0.28, 0.95, 0.5))):
            mote(fx, "gl%d" % j, solid, "star", 0.2,
                 (lambda x, y, ph: lambda t: (x, y, 0.15 + 0.85 * math.sin(PI * ((t + ph) % 1)) ** 2))(x, y, ph))
        mote(fx, "m0", midm, "disc", 0.045, rising(0.05, 0.15, 0.9, 0.2, 0.04, 1.0))
        return fx

    # ground bloom under the item
    bl = MB().disc(0, 0, 0.8, 28, 1.0, 0.0).xform(sy=0.3)
    ob = bl.build(fx, "bloom", bloom)
    fx.track(ob, lambda t, i: dict(op=0.55 + 0.2 * pulse(t, 1.0)))

    # the column: wide soft body + thin bright core
    cb = column(W, H, taper=0.5, p=0.85, base=0.35).build(fx, "col", body)
    fx.track(cb, lambda t, i: dict(sx=1.0 + 0.06 * math.sin(TAU * t + 0.5), op=0.8 + 0.2 * math.sin(TAU * t + 1.0)))
    if r != "linh":
        cc = column(W * 0.26, H * 0.86 - 0.85, taper=0.7, p=1.0, y0=0.85).build(fx, "core", core)
        fx.track(cc, lambda t, i: dict(op=0.75 + 0.25 * math.sin(TAU * t)))
    else:
        cc = column(W * 0.22, 0.45, taper=0.7, p=1.0, y0=0.8).build(fx, "core", core)
        fx.track(cc, lambda t, i: dict(op=0.7 + 0.2 * math.sin(TAU * t)))

    kind = dict(linh="disc", huyen="diamond", dia="star", thien="star")[r]
    n = dict(linh=3, huyen=4, dia=6, thien=8)[r]
    for j in range(n):
        x0 = (j / max(n - 1, 1) - 0.5) * W * 0.9 + rng.uniform(-0.05, 0.05)
        k = kind if not (r == "thien" and j % 3 == 0) else "star8"
        mote(fx, "m%d" % j, solid if j % 2 else midm, k, 0.055 if kind == "disc" else (0.09 if kind == "diamond" else 0.11),
             rising(x0, 0.12, H * 0.95, j / n, 0.06, 1.0, 0.7))
    if r in ("huyen", "dia", "thien"):
        for j in range(2 if r == "huyen" else 3):
            sliver(fx, "sl%d" % j, solid, (j - 0.5 * (1 if r == "huyen" else 2)) * W * 0.28, H * 0.6, 0.3 * j + 0.1, 0.1, y0=0.85)

    if r in ("dia", "thien"):
        # two long blades crossing behind the column (a wing-like V)
        bm = fx.mat("blade", c["body"], grad=dict(src="attr", pow=0.8), core=c["mid"])
        for sgn in (-1, 1):
            L = 1.7 if r == "dia" else 2.1
            mb = MB().strip([(0.42, 0.0), (0.42 + 0.45 * L * math.sin(0.34), 0.45 * L), (0.42 + L * math.sin(0.34), L * 0.97)], [0.3, 0.2, 0.02], soft=True)
            mb.xform(sx=sgn)
            o = mb.build(fx, "blade%d" % sgn, bm)
            fx.track(o, lambda t, i: dict(sy=1.0 + 0.05 * math.sin(TAU * t), op=0.38 + 0.12 * math.sin(TAU * t + 2.0)))

    if r == "thien":
        # slow orbiting halo above the column's waist, crown star on top, flat star burst on the ground
        hy, rx, ky = 1.55, 0.72, 0.28
        ring = MB().ring(0, hy, rx, 0.035, seg=40, ky=ky).build(fx, "halo", solid)
        fx.track(ring, lambda t, i: dict(op=0.85))
        halo_g = MB().ring(0, hy, rx, 0.14, seg=40, ky=ky, soft=True).build(fx, "halog", midm)
        fx.track(halo_g, lambda t, i: dict(op=0.7))
        for j in range(6):
            def f(t, j=j):
                a = TAU * (t / 6.0 + j / 6.0)
                depth = -math.sin(a)                       # +1 = in front (lower on screen)
                return (rx * math.cos(a), hy + rx * ky * math.sin(a), 0.55 + 0.35 * depth, a)
            mote(fx, "bead%d" % j, solid, "diamond", 0.09, f)
        crown = MB().star(0, 0, 4, 0.34, 0.06, PI / 2).build(fx, "crown", solid)
        fx.track(crown, lambda t, i: dict(y=H * 0.96, s=0.65 + 0.35 * pulse(t, 0.3)))
        sm = fx.mat("star", c["mid"], opacity=0.8)
        fx.per_frame("burst", sm, lambda t, i: MB().star(0, 0, 8, 0.95, 0.12, TAU * t / 8.0).xform(sy=0.3))
    return fx


for _r in RAR:
    REG["roi_cot_" + _r] = (lambda r: lambda: make_cot(r))(_r)


# ------------------------------------------------------------------------------ rings
RING_R = dict(pham=0.58, linh=0.66, huyen=0.72, dia=0.78, thien=0.8)


def make_vong(r):
    c = C[r]
    R = RING_R[r]
    fx = FxP("roi_vong_" + r, view="ground", frames=6, fps=8, loop=True, px=64, ground=True, halo=0.75,
             name_vi="Vòng sáng rơi đồ " + c["vi"],
             where="pulsing ring of light on the ground under an item of grade %s" % c["vi"])
    body = fx.mat("body", c["body"], grad=dict(src="attr", pow=1.0), opacity=0.9)
    mid = fx.mat("mid", c["mid"])
    core = fx.mat("core", c["core"])
    glow = fx.mat("glow", c["body"], grad=dict(src="attr", pow=1.4), opacity={"pham": 0.2, "linh": 0.35, "huyen": 0.45, "dia": 0.5, "thien": 0.55}[r])
    pulse = lambda t, ph=0.0: math.sin(TAU * t + ph)

    gd = glow_disc(R * 0.98, 36).build(fx, "glow", glow)
    fx.track(gd, lambda t, i: dict(s=1.0 + 0.05 * pulse(t), op=0.85 + 0.15 * pulse(t, 1.0)))

    def spin(ob, sym, rev=1.0, **kw):
        fx.track(ob, lambda t, i: dict(rot=rev * TAU * t / sym, s=1.0 + 0.045 * pulse(t, 0.4), **kw))

    if r == "pham":
        spin(ring_arcs(MB(), R, 0.05, 10, 0.45).build(fx, "dash", body), 10)
        return fx
    if r == "linh":
        spin(MB().ring(0, 0, R, 0.07, seg=48).build(fx, "ring", mid), 1)
        return fx
    spin(MB().ring(0, 0, R, 0.07, seg=48).build(fx, "ring", mid), 1)
    if r == "huyen":
        mb = MB()
        for k in range(4):
            a = TAU * k / 4
            mb.diamond(R * math.cos(a) * 1.13, R * math.sin(a) * 1.13, 0.3, 0.17, a)
        spin(mb.build(fx, "ticks", core), 4)
        return fx
    if r == "dia":
        spin(MB().ring(0, 0, R * 0.7, 0.045, seg=40).build(fx, "inner", body), 1, rev=-1.0)
        mb = MB()
        for k in range(6):
            a = TAU * k / 6
            mb.diamond(R * math.cos(a), R * math.sin(a), 0.34, 0.2, a)
        spin(mb.build(fx, "nodes", core), 6)
        return fx
    # thien
    spin(MB().ring(0, 0, R * 0.8, 0.04, seg=48).build(fx, "inner", mid), 1, rev=-1.0)
    spin(MB().star(0, 0, 8, R * 1.0, R * 0.55, 0.0).build(fx, "star", fx.mat("starm", c["body"], opacity=0.55)), 8)
    mb = MB()
    for k in range(8):
        a = TAU * k / 8
        mb.diamond(R * 1.04 * math.cos(a), R * 1.04 * math.sin(a), 0.3, 0.16, a)
    spin(mb.build(fx, "tips", core), 8, rev=-1.0)
    return fx


for _r in RAR:
    REG["roi_vong_" + _r] = (lambda r: lambda: make_vong(r))(_r)


# ------------------------------------------------------------------------------ pick-up flash
@reg("roi_nhat")
def roi_nhat():
    fx = FxP("roi_nhat", frames=6, fps=14, loop=False, px=64, halo=0.9, name_vi="Nhặt vật phẩm",
             where="pick-up flash (neutral white-gold), one-shot, centre pivot")
    gold = fx.mat("gold", "#ffe27a")
    white = fx.mat("white", "#fffbe4")
    glow = fx.mat("glow", "#e8b02a", grad=dict(src="attr", pow=1.1), opacity=0.9)
    g = glow_disc(0.95, 28).build(fx, "glow", glow)
    fx.track(g, lambda t, i: dict(s=[0.35, 0.85, 0.7, 0.5, 0.3, 0.12][i], op=[0.9, 1.0, 0.8, 0.55, 0.3, 0.12][i]))
    st = MB().star(0, 0, 4, 0.92, 0.09, PI / 2).build(fx, "star", white)
    fx.track(st, lambda t, i: dict(s=[0.3, 1.0, 0.6, 0.3, 0.0, 0.0][i] + 0.001, show=i < 4))
    st2 = MB().star(0, 0, 4, 0.6, 0.08, PI / 4).build(fx, "star2", gold)
    fx.track(st2, lambda t, i: dict(s=[0.0, 0.7, 0.8, 0.45, 0.0, 0.0][i] + 0.001, show=1 <= i < 4))
    rings = fx.per_frame("ring", gold, lambda t, i: MB().ring(0, 0, [0.2, 0.4, 0.6, 0.78, 0.9, 0.95][i], [0.1, 0.1, 0.07, 0.05, 0.03, 0.02][i], seg=36))
    for j in range(8):
        a = TAU * j / 8 + 0.3
        mote(fx, "sp%d" % j, white if j % 2 else gold, "star" if j % 2 else "diamond", 0.07,
             burst_mote(0.0, 0.0, math.cos(a) * 0.8, math.sin(a) * 0.8 + 0.25, 0.1, 0.9, -0.3, 1.0, 0.5, 0.0))
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
