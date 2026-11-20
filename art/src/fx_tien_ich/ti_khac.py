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
CORE_Y = 1.2          # height of the glowing core = hand-print height; the linh can lights rise from here (ti_linh.Y0)


@reg("trac_linh_thach")
def trac_linh_thach():
    fx = FxP("trac_linh_thach", frames=6, fps=6, loop=True, mode="alpha", px=96, pivot=(48, 84), alpha_levels=3,
             name_vi="Trắc Linh Thạch",
             where="the spirit-testing stone: a tall faceted spirit crystal on a round rune altar, floating shards; core at hand height (pivot = altar centre, base)")
    M = lambda n, c, **kw: fx.mat(n, c, **kw)
    ink, ssh, sbs, slt = M("ink", "#0b0a10"), M("ssh", "#3a3d48"), M("sbs", "#5e636f"), M("slt", "#888e98")
    tsh, tbs, tlt, thi = M("tsh", "#1f6e70"), M("tbs", "#2f9c9a"), M("tlt", "#4cc2b6"), M("thi", "#9ae6d6")
    c2, c3 = M("c2", "#5ae0f4"), M("c3", "#d8fcff")
    halo = M("halo", "#5ae0f4", grad=dict(src="attr", pow=1.2), opacity=0.5)
    pulse = lambda t, ph=0.0: 0.5 + 0.5 * math.sin(TAU * t + ph)

    def ell(name, mat, rx, ry, cy):
        return MB().disc(0, cy, rx, 44, ky=ry / rx).build(fx, name, mat)

    G = 0.045
    # ---- one dark silhouette under everything (outline)
    crystal = [(-0.32, 0.42), (-0.42, 1.1), (-0.28, 1.95), (0.0, 2.45), (0.28, 1.95), (0.42, 1.1), (0.32, 0.42)]
    out = MB()
    out.poly([(x * 1.0 + (G if x > 0 else -G if x < 0 else 0.0), y + (G if y > 2 else -G * 0.2)) for x, y in crystal])
    out.build(fx, "outline_c", ink)
    ell("outline_a", ink, 1.1 + G, 0.3 + G, 0.36)
    MB().poly([(-1.1 - G, 0.16), (1.1 + G, 0.16), (1.1 + G, 0.36), (-1.1 - G, 0.36)]).build(fx, "outline_s", ink)
    ell("outline_b", ink, 1.1 + G, 0.3 + G, 0.16)
    # ---- round altar: lower rim, drum, top disc, inset with rune ring
    ell("rim", ssh, 1.1, 0.3, 0.16)
    MB().poly([(-1.1, 0.16), (1.1, 0.16), (1.1, 0.36), (-1.1, 0.36)]).build(fx, "drum", sbs)
    MB().poly([(-1.1, 0.16), (-0.6, 0.16), (-0.6, 0.36), (-1.1, 0.36)]).build(fx, "drum_l", slt)
    MB().poly([(0.6, 0.16), (1.1, 0.16), (1.1, 0.36), (0.6, 0.36)]).build(fx, "drum_r", ssh)
    ell("top", slt, 1.1, 0.3, 0.36)
    ell("inset", sbs, 0.9, 0.24, 0.38)
    rn = runes(MB(), 0, 0.38, 0.72, 8, 0.15, random.Random(21), 0.024, ky=0.24)
    fx.track(rn.build(fx, "altar_runes", c2), lambda t, i: dict(op=0.6 + 0.4 * pulse(t, PI)))
    MB().ring(0, 0.38, 0.9, 0.03, seg=44, ky=0.24 / 0.9).build(fx, "altar_ring", c2)
    ell("seat", ssh, 0.5, 0.13, 0.42)
    # ---- the crystal: three facets (lit / body / shade), edge highlight, setting
    facets = (("fl", tlt, [(-0.32, 0.42), (-0.1, 0.42), (-0.1, 1.1), (-0.06, 1.95), (0.0, 2.45), (-0.28, 1.95), (-0.42, 1.1)]),
              ("fm", tbs, [(-0.1, 0.42), (0.12, 0.42), (0.12, 1.1), (0.08, 1.95), (0.0, 2.45), (-0.06, 1.95), (-0.1, 1.1)]),
              ("fr", tsh, [(0.12, 0.42), (0.32, 0.42), (0.42, 1.1), (0.28, 1.95), (0.0, 2.45), (0.08, 1.95), (0.12, 1.1)]))
    for nm, mt, pts in facets:
        MB().poly(pts).build(fx, nm, mt)
    MB().strip([(-0.36, 0.7), (-0.4, 1.1), (-0.27, 1.9), (-0.04, 2.38)], 0.045).build(fx, "edge_hi", thi)
    MB().strip([(0.02, 2.4), (0.06, 1.9), (0.09, 1.1)], 0.025).build(fx, "ridge", thi)
    MB().poly([(-0.44, 0.4), (0.44, 0.4), (0.4, 0.58), (-0.4, 0.58)]).build(fx, "collar", slt)
    MB().strip([(-0.42, 0.42), (0.42, 0.42)], 0.04).build(fx, "collar_sh", ssh)
    # ---- veins and the core at hand height
    veins = [[(0, CORE_Y), (-0.09, 1.55), (0.05, 1.95), (0.0, 2.3)], [(0, CORE_Y), (0.11, 0.85), (-0.04, 0.55)], [(0, 1.45), (0.2, 1.72)],
             [(0, 1.0), (-0.2, 0.8)]]
    vm = MB()
    for v in veins:
        vm.strip(v, 0.035)
    fx.track(vm.build(fx, "veins", c2), lambda t, i: dict(op=0.7 + 0.3 * pulse(t)))
    vm2 = MB()
    for v in veins[:2]:
        vm2.strip(v, 0.016)
    fx.track(vm2.build(fx, "veins_hi", c3), lambda t, i: dict(show=pulse(t) > 0.55))
    h = glow_disc(0.6, 28).build(fx, "glow", halo)
    fx.track(h, lambda t, i: dict(y=CORE_Y, s=0.85 + 0.25 * pulse(t), op=0.35 + 0.35 * pulse(t)))
    orb = MB().disc(0, 0, 0.13, 16).build(fx, "orb", c3)
    fx.track(orb, lambda t, i: dict(y=CORE_Y, s=0.8 + 0.4 * pulse(t, 0.5)))
    ring = MB().ring(0, 0, 0.2, 0.025, seg=24).build(fx, "orbring", c2)
    fx.track(ring, lambda t, i: dict(y=CORE_Y, s=0.9 + 0.2 * pulse(t, 1.0)))
    # ---- three shards orbiting the crystal (smaller when behind it), two spirit motes off the tip
    for j in range(3):
        def f(t, j=j):
            a = TAU * (t + j / 3.0)
            depth = -math.sin(a)
            return (0.82 * math.cos(a), 1.5 + 0.16 * math.sin(a) + 0.12 * math.sin(a * 2 + j), 0.7 + 0.3 * depth, PI / 2 + 0.25 * math.cos(a))
        mote(fx, "shard%d" % j, thi if j % 2 else tlt, "diamond", 0.12, f)
    for j, (x0, ph) in enumerate(((-0.12, 0.0), (0.14, 0.5))):
        mote(fx, "m%d" % j, c3, "disc", 0.04, rising(x0, 2.15, 0.5, ph, 0.04, 1.0, 0.8))
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
