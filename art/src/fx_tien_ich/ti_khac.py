"""D. trac_linh_thach (the spirit-testing stone, alpha), thanh_tuu (achievement seal, additive),
uy_ap (realm-pressure shockwave on the ground, alpha)."""
import math
from tilib import *
from ti_phi import puffs

REG = {}


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


# ------------------------------------------------------------------------------ trac_linh_thach
def arch_pts(w0, w1, y0, y1, r, n=14, grow=0.0):
    """outline of an arched stele: bottom width w0, shoulder width w1, flat bottom at y0, arch centre at y1."""
    pts = [(-w0 / 2 - grow, y0 - grow), (-w1 / 2 - grow, y1)]
    rr = w1 / 2 + grow
    for k in range(1, n):
        a = PI - PI * k / n
        pts.append((rr * math.cos(a), y1 + (r + grow) * math.sin(a)))
    pts += [(w1 / 2 + grow, y1), (w0 / 2 + grow, y0 - grow)]
    return pts


@reg("trac_linh_thach")
def trac_linh_thach():
    fx = FxP("trac_linh_thach", frames=6, fps=6, loop=True, mode="alpha", px=96, pivot=(48, 84), alpha_levels=3,
             name_vi="Trắc Linh Thạch",
             where="the spirit-testing stone: carved stele on two plinth steps, rune face glowing gently (pivot = base centre)")
    M = lambda n, c, **kw: fx.mat(n, c, **kw)
    ink, shade, base, lit, hi = M("ink", "#0b0a10"), M("shade", "#3a3d48"), M("base", "#5e636f"), M("lit", "#888e98"), M("hi", "#b8bdc3")
    pan, pan2 = M("pan", "#262a34"), M("pan2", "#3a3d48")
    cy_lo, cy_mid, cy_hi = M("c1", "#18a0c8"), M("c2", "#5ae0f4"), M("c3", "#d8fcff")
    halo = M("halo", "#5ae0f4", grad=dict(src="attr", pow=1.2), opacity=0.55)
    pulse = lambda t, ph=0.0: 0.5 + 0.5 * math.sin(TAU * t + ph)

    def box(name, mat, x0, x1, y0, y1):
        return MB().poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]).build(fx, name, mat)

    G = 0.04
    # outline first (one dark silhouette under everything)
    sil = MB()
    sil.poly([(-0.95 - G, -G), (0.95 + G, -G), (0.95 + G, 0.28), (-0.95 - G, 0.28)])
    sil.poly([(-0.75 - G, 0.2), (0.75 + G, 0.2), (0.75 + G, 0.56), (-0.75 - G, 0.56)])
    sil.poly(arch_pts(1.1, 0.96, 0.5, 1.78, 0.5, grow=G))
    sil.build(fx, "outline", ink)
    # plinth steps: front face shade, top-lit strip
    box("s1", base, -0.95, 0.95, 0.0, 0.28)
    box("s1t", lit, -0.95, 0.95, 0.2, 0.28)
    box("s1s", shade, 0.55, 0.95, 0.0, 0.2)
    box("s2", base, -0.75, 0.75, 0.28, 0.56)
    box("s2t", lit, -0.75, 0.75, 0.48, 0.56)
    box("s2s", shade, 0.4, 0.75, 0.28, 0.48)
    # the stele: base body, lit left edge, shaded right edge, top highlight
    MB().poly(arch_pts(1.1, 0.96, 0.52, 1.78, 0.5)).build(fx, "body", base)
    le = [(-0.55, 0.55), (-0.48, 1.78)] + [(-0.48 * math.cos(PI * k / 14), 1.78 + 0.5 * math.sin(PI * k / 14)) for k in range(0, 8)]
    MB().strip(le, 0.17).build(fx, "litedge", lit)
    re = [(0.55, 0.55), (0.48, 1.78)] + [(0.48 * math.cos(PI * k / 14), 1.78 + 0.5 * math.sin(PI * k / 14)) for k in range(0, 6)]
    MB().strip(re, 0.22).build(fx, "shadeedge", shade)
    MB().strip([(-0.34, 2.18), (-0.2, 2.25), (-0.05, 2.28)], 0.05).build(fx, "tophi", hi)
    MB().strip([(-0.3, 1.72), (0.3, 1.72)], 0.035).build(fx, "band", shade)
    # recessed rune panel
    MB().poly(arch_pts(0.74, 0.7, 0.78, 1.62, 0.36, n=12)).build(fx, "panel", pan)
    MB().strip([(-0.35, 0.8), (0.35, 0.8)], 0.04).build(fx, "panelsill", pan2)
    # cracks and chips
    MB().strip([(0.38, 0.6), (0.33, 0.75), (0.4, 0.9)], 0.03).build(fx, "crack1", ink)
    MB().strip([(-0.5, 1.45), (-0.43, 1.35), (-0.46, 1.2)], 0.03).build(fx, "crack2", ink)
    # glowing face: soft halo behind the orb, ring, 4 strokes, 3 small marks
    h = glow_disc(0.62, 28).build(fx, "glow", halo)
    fx.track(h, lambda t, i: dict(y=1.28, s=0.9 + 0.2 * pulse(t), op=0.5 + 0.5 * pulse(t)))
    ring_a = MB().ring(0, 0, 0.3, 0.05, seg=36).build(fx, "ring", cy_mid)
    fx.track(ring_a, lambda t, i: dict(y=1.28, op=1.0))
    ring_b = MB().ring(0, 0, 0.3, 0.05, seg=36).build(fx, "ringlit", cy_hi)
    fx.track(ring_b, lambda t, i: dict(y=1.28, op=1.0, show=pulse(t) > 0.62))
    rn = MB()
    rr = random.Random(11)
    runes(rn, 0, 0, 0.3, 4, 0.2, rr, 0.03, tangent=False, rot0=PI / 4)
    fx.pose(rn.build(fx, "runes", cy_mid), None, y=1.28)
    orb = MB().disc(0, 0, 0.12, 16).build(fx, "orb", cy_hi)
    fx.track(orb, lambda t, i: dict(y=1.28, s=0.8 + 0.4 * pulse(t, 0.5)))
    mk = MB()
    for q in range(3):
        runes(mk, (q - 1) * 0.2, 0.98, 0.0, 1, 0.13, random.Random(30 + q), 0.026, tangent=False)
    mk.build(fx, "marks", cy_lo)
    # two motes of spirit light rising off the stone
    for j, (x0, ph) in enumerate(((-0.28, 0.0), (0.3, 0.5))):
        mote(fx, "m%d" % j, cy_hi, "disc", 0.045, rising(x0, 1.7, 0.5, ph, 0.04, 1.0, 0.8))
    return fx


# ------------------------------------------------------------------------------ thanh_tuu
@reg("thanh_tuu")
def thanh_tuu():
    fx = FxP("thanh_tuu", frames=10, fps=12, loop=False, px=96, halo=0.85, name_vi="Thành tựu",
             where="achievement unlocked: a golden seal flashes into being with rays and a ribbon of light (centre pivot)")
    gold, mid, core = fx.mat("gold", "#e8b02a", opacity=0.9), fx.mat("mid", "#ffe27a"), fx.mat("core", "#fffbe4")
    soft = fx.mat("soft", "#e8b02a", grad=dict(src="attr", pow=1.2), opacity=0.9)
    face = fx.mat("face", "#b9821a", opacity=0.8)
    SC = [0.0, 0.4, 0.75, 1.1, 1.15, 1.06, 1.0, 1.0, 1.0, 1.0]
    FLH = [0.5, 1.0, 0.9, 0.6, 0.4, 0.3, 0.25, 0.22, 0.2, 0.2]
    RAY = [0.0, 0.0, 0.7, 1.0, 1.0, 0.75, 0.5, 0.3, 0.0, 0.0]
    sc = lambda i: SC[i] + 0.001

    g = glow_disc(1.45, 32).build(fx, "flash", soft)
    fx.track(g, lambda t, i: dict(s=0.45 + 0.5 * (FLH[i]), op=FLH[i]))
    # medallion: dim gold face, bright rim, notched edge, inner ring, 8-petal lotus star, centre jewel
    parts = []
    fc = MB().disc(0, 0, 0.93, 40).build(fx, "face", face)
    fx.track(fc, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    rim = MB().ring(0, 0, 1.0, 0.1, seg=48).build(fx, "rim", mid)
    fx.track(rim, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    nb = MB()
    for k in range(16):
        a = TAU * k / 16
        nb.diamond(1.1 * math.cos(a), 1.1 * math.sin(a), 0.2, 0.12, a)
    nbo = nb.build(fx, "notch", mid)
    fx.track(nbo, lambda t, i: dict(s=sc(i), rot=0.0, show=SC[i] > 0))
    ir = MB().ring(0, 0, 0.74, 0.045, seg=40).build(fx, "inner", core)
    fx.track(ir, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    rn = runes(MB(), 0, 0, 0.87, 12, 0.14, random.Random(5), 0.028).build(fx, "runes", gold)
    fx.track(rn, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    st = MB().star(0, 0, 8, 0.56, 0.26, PI / 8).build(fx, "lotus", mid)
    fx.track(st, lambda t, i: dict(s=sc(i), rot=0.0, show=SC[i] > 0))
    st2 = MB().star(0, 0, 4, 0.4, 0.07, PI / 2).build(fx, "cross", core)
    fx.track(st2, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    jw = MB().disc(0, 0, 0.11, 16).build(fx, "jewel", core)
    fx.track(jw, lambda t, i: dict(s=sc(i), show=SC[i] > 0))
    # a glint band sweeping across the face in the last frames
    gl = MB().diamond(0, 0, 0.95, 0.07, PI / 3).build(fx, "glint", core)
    fx.track(gl, lambda t, i: dict(x=-0.6 + 1.2 * sat((i - 5) / 4.0), y=-0.15 + 0.3 * sat((i - 5) / 4.0), show=5 <= i <= 9, s=1.0))
    # rays
    for j in range(12):
        a = TAU * j / 12 + 0.13
        L = 1.35 if j % 2 == 0 else 0.9
        ob = MB().diamond(0, 0, 1.0, 0.1, 0).build(fx, "ray%d" % j, mid)
        fx.track(ob, lambda t, i, a=a, L=L: dict(x=math.cos(a) * (0.75 + L * 0.3 * RAY[i]), y=math.sin(a) * (0.75 + L * 0.3 * RAY[i]), rot=a,
                                                  sx=max(L * 0.45 * RAY[i], 0.001), show=RAY[i] > 0.01))
    # ribbon of light looping around the seal (tilted ellipse), head advancing, tail trailing
    rb = fx.mat("ribbon", "#ffe27a", grad=dict(src="attr", pow=0.6), core="#fffbe4")

    def ribbon(t, i):
        if not (2 <= i <= 8):
            return MB().strip([(0, 0), (0.01, 0)], 0.01)
        head = -PI * 0.9 + TAU * 0.95 * (i - 2) / 6.0
        span = 1.5 + 0.8 * math.sin(PI * (i - 2) / 6.0)
        pts, ws = [], []
        for k in range(21):
            s = k / 20.0
            a = head - span * (1 - s)
            x, y = 1.35 * math.cos(a), 0.5 * math.sin(a)
            ca, sa = math.cos(-0.35), math.sin(-0.35)
            pts.append((x * ca - y * sa, x * sa + y * ca))
            ws.append(0.16 * s ** 0.8 + 0.01)
        return MB().strip(pts, ws, soft=True)
    obs = fx.per_frame("ribbon", rb, ribbon)
    for i, ob in enumerate(obs):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and 2 <= i <= 8)))
    # sparkles
    for j in range(6):
        a = TAU * j / 6 + 0.4
        mote(fx, "sp%d" % j, core if j % 2 else mid, "star", 0.1,
             (lambda a, j: lambda t: None if t < 0.25 else (1.25 * math.cos(a) + 0.05 * math.sin(TAU * t * 3 + j), 1.25 * math.sin(a),
                                      max(0.2, math.sin(PI * min(1, max(0.0, (t - 0.25 - 0.06 * j) / 0.7))) ** 0.8)))(a, j))
    sp = MB().star(0, 0, 4, 0.5, 0.07, PI / 2).build(fx, "spark0", core)
    fx.track(sp, lambda t, i: dict(s=[0.5, 1.0, 0.5, 0, 0, 0, 0, 0, 0, 0][i] + 0.001, show=i < 3))
    return fx


# ------------------------------------------------------------------------------ uy_ap
@reg("uy_ap")
def uy_ap():
    fx = FxP("uy_ap", view="ground", frames=8, fps=10, loop=False, mode="alpha", px=128, ground=True, alpha_levels=4,
             name_vi="Uy áp", where="realm pressure: a heavy dark-violet shockwave ring spreads along the ground (one-shot, centre pivot)")
    ink = fx.mat("ink", "#0b0a10", opacity=0.95)
    d1 = fx.mat("d1", "#3a2160", opacity=0.95)
    d2 = fx.mat("d2", "#5c3690", opacity=0.95)
    crest = fx.mat("crest", "#b892e4")
    shock = fx.mat("shock", "#2a1648", grad=dict(src="attr", pow=0.8), opacity=0.7)
    R = lambda t, d=0.0: 0.28 + 1.55 * ease_out(sat((t - d) / (1 - d)))
    W = lambda t: 0.5 * (1 - t) ** 1.3 + 0.1
    OP = [1, 1, 1, 0.95, 0.85, 0.7, 0.5, 0.3]
    # impact bruise in the middle at the start
    ctr = glow_disc(1.0, 32).build(fx, "bruise", shock)
    fx.track(ctr, lambda t, i: dict(s=[1.0, 1.1, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1][i], op=[1, 1, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0][i], show=i < 7))
    # cracks running out along the ground
    for j in range(9):
        a = TAU * j / 9 + 0.25
        rng = random.Random(j)
        L = 1.2 + 0.5 * rng.random()
        pts = jag((0, 0), (L * math.cos(a), L * math.sin(a)), rng, 8, 0.16)
        o = MB().strip(pts, [0.07] * len(pts)).build(fx, "crack%d" % j, ink)
        fx.track(o, lambda t, i: dict(sx=sat(i / 3.0) + 0.001, sy=sat(i / 3.0) + 0.001, op=[1, 1, 1, 0.9, 0.8, 0.6, 0.4, 0.2][i]))
    # the shockwave: ink outline, dark body, mid body, bright crest
    fx.per_frame("o", ink, lambda t, i: MB().ring(0, 0, R(t) + W(t) * 0.5 + 0.03, 0.06, seg=64))
    fx.per_frame("b1", d1, lambda t, i: MB().ring(0, 0, R(t), W(t), seg=64))
    fx.per_frame("b2", d2, lambda t, i: MB().ring(0, 0, R(t) + W(t) * 0.12, W(t) * 0.5, seg=64))
    fx.per_frame("cr", crest, lambda t, i: MB().ring(0, 0, R(t) + W(t) * 0.36, 0.045, seg=64))
    # a second echo behind the first
    fx.per_frame("e1", d1, lambda t, i: MB().ring(0, 0, R(t, 0.3) * 0.85, W(t) * 0.45, seg=64))
    fx.per_frame("e2", crest, lambda t, i: MB().ring(0, 0, R(t, 0.3) * 0.85 + W(t) * 0.1, 0.03, seg=64))
    for ob in fx.col.objects:
        if ob.name.startswith("SM_uy_ap_e1_") or ob.name.startswith("SM_uy_ap_e2_"):
            i = int(ob.name.split("_")[-1])
            fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and 2 <= i <= 7)))
    puffs(fx, "d", 9, 0.4, 1.45, 0.12, 0.22, 0.2, [0.9, 1, 1, 0.9, 0.7, 0.5, 0.3, 0.15], ang0=0.1, jit=0.15)
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
