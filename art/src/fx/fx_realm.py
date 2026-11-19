"""Realm and story FX, 96x96, front view.  The character stands at the centre (body about 1.1 units
tall = 36 px); the pivot is the character's feet (48, 66)."""
import math
from fxlib import *

REG = {}
FEET = (48, 66)


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


def rfx(id, name_vi, where, frames=6, fps=8, loop=True, **kw):
    kw.setdefault("halo", 0.85)
    return Fx(id, view="front", frames=frames, fps=fps, loop=loop, px=96, pivot=FEET, name_vi=name_vi, where=where, **kw)


def star4(fx, name, fm, size, fn):
    mb = MB().star(0, 0, 4, size, size * 0.2, PI / 2)
    ob = mb.build(fx, name, fm)

    def f(t, i):
        r = fn(t)
        if r is None:
            return None
        x, y, s = r
        return dict(x=x, y=y, s=max(s, 1e-3))
    return fx.track(ob, f)


def mote(fx, name, fm, size, fn, shape="disc"):
    mb = MB()
    if shape == "disc":
        mb.disc(0, 0, size, 8)
    elif shape == "diamond":
        mb.diamond(0, 0, size * 2.2, size)
    else:
        mb.star(0, 0, 4, size, size * 0.2, PI / 2)
    ob = mb.build(fx, name, fm)

    def f(t, i):
        r = fn(t)
        if r is None:
            return None
        x, y, s = r
        return dict(x=x, y=y, s=max(s, 1e-3))
    return fx.track(ob, f)


def flame_ring(fx, name, layers, rx, ry, n, h, w, rot_sym=None, lean_up=0.6, y0=0.0, amp=0.14, ang0=0.0, skip_bottom=False):
    """flames standing on an elliptical outline, pointing outwards/up; one mesh per frame per layer.
    layers = [(material, height_scale, width_scale)]"""
    for li, (fm, hs, ws) in enumerate(layers):
        def b(t, i, hs=hs, ws=ws, li=li):
            mb = MB()
            for k in range(n):
                a = ang0 + TAU * k / n
                px, py = rx * math.cos(a), y0 + ry * math.sin(a)
                if skip_bottom and math.sin(a) < -0.3:
                    continue
                nx, ny = math.cos(a) / rx, math.sin(a) / ry
                na = math.atan2(ny, nx)                      # outward normal
                tilt = (na - PI / 2)
                tilt = tilt * (1 - lean_up)                 # keep them rising
                ph = TAU * (t + (k % 3) / 3.0 + li * 0.1)
                f = MB().flame(0, 0, h * hs * (1 + 0.16 * math.sin(ph)), w * ws, sway=0.07 * math.sin(ph + 1.0), lean=0.04 * math.cos(ph))
                mb.merge(f, px, py, 1.0, tilt)
            return mb
        fx.per_frame("%s%d" % (name, li), fm, b)


# ================================================================ auras
@reg("aura_luyen_khi")
def aura_luyen_khi():
    fx = rfx("aura_luyen_khi", "Hao quang Luyen Khi", "behind a Luyen Khi cultivator: faint grey-white breath wisps", halo=0.5)
    wm = fx.mat("wisp", "#dfe6f2", grad=dict(src="attr", pow=0.8), opacity=0.8)
    wm2 = fx.mat("wisp2", "#ffffff", grad=dict(src="attr", pow=1.4), opacity=0.7)
    xs = [-0.62, -0.3, 0.3, 0.62, 0.0]

    def b(wmul, mat_k):
        def f(t, i):
            mb = MB()
            for k, x0 in enumerate(xs):
                ph = (t + k / 5.0) % 1.0
                env = math.sin(PI * ph) ** 0.8
                y0 = -0.75 + ph * 1.25
                pts = [(x0 + (0.1 + 0.03 * k % 3) * math.sin(TAU * (ph * 1.2 + k * 0.17) + s * 3.0) * (0.3 + s), y0 + s * 0.55) for s in [j / 8 for j in range(9)]]
                ws = [wmul * (0.02 + 0.1 * env) * (1 - abs(j / 8 - 0.5) * 1.2) for j in range(9)]
                mb.strip(pts, ws, soft=True)
            return mb
        return f
    fx.per_frame("w", wm, b(1.6, 0))
    fx.per_frame("w2", wm2, b(0.7, 1))
    for j in range(5):
        mote(fx, "m%d" % j, wm2, 0.025, (lambda j: lambda t: (-0.5 + 0.25 * j, -0.6 + 1.2 * ((t + j / 5.0) % 1), math.sin(PI * ((t + j / 5.0) % 1)) + 0.001))(j))
    return fx


@reg("aura_truc_co")
def aura_truc_co():
    fx = rfx("aura_truc_co", "Hao quang Truc Co", "drifting blue mist: a low ring of soft cloud puffs around the feet that slowly turns, a few wisps rise")
    puff = fx.mat("puff", "#4a90ff", grad=dict(src="radial", pow=1.3), opacity=0.42)
    puff2 = fx.mat("puff2", "#9cc8ff", grad=dict(src="radial", pow=1.8), opacity=0.55)
    wisp = fx.mat("wisp", "#8cc0ff", grad=dict(src="attr", pow=1.0), opacity=0.55)
    cy, rx, ry = -0.5, 1.05, 0.4
    rng = fx.rng
    N = 8
    for j in range(N):
        a0 = TAU * j / N
        sz = 0.2 + 0.05 * (j % 3)
        mb = MB().disc(0, 0, sz, 18, 1, 0).merge(MB().disc(0, 0, sz * 0.7, 14, 1, 0), sz * 0.55, 0.05).merge(MB().disc(0, 0, sz * 0.6, 14, 1, 0), -sz * 0.5, -0.03)
        ob = mb.build(fx, "puff%d" % j, puff)
        fx.track(ob, lambda t, i, a0=a0, j=j: dict(x=rx * math.cos(a0 + TAU * t / N * 2), y=cy + ry * math.sin(a0 + TAU * t / N * 2) + 0.03 * math.sin(TAU * t + j),
                                                     s=1.0 + 0.1 * math.sin(TAU * t + j * 1.7)))
        hl = MB().disc(0, 0, sz * 0.5, 12, 1, 0).build(fx, "hl%d" % j, puff2)
        fx.track(hl, lambda t, i, a0=a0, j=j: dict(x=rx * math.cos(a0 + TAU * t / N * 2) - 0.04, y=cy + ry * math.sin(a0 + TAU * t / N * 2) + 0.07, s=1.0))
    # rising wisps (strips shown on their own frame)
    for k in range(3):
        x0 = (-0.55, 0.0, 0.55)[k]

        def wb(t, i, k=k, x0=x0):
            ph = (t + k / 3.0) % 1.0
            env = math.sin(PI * ph) ** 0.8
            pts = [(x0 + 0.12 * math.sin(TAU * (ph + k * 0.2) + s * 3.0), -0.5 + ph * 0.9 + s * 0.5) for s in [j / 8 for j in range(9)]]
            return MB().strip(pts, [0.02 + 0.09 * env * (1 - abs(j / 8 - 0.5) * 1.2) for j in range(9)], soft=True)
        fx.per_frame("wisp%d" % k, wisp, wb)
    return fx


@reg("aura_ket_dan")
def aura_ket_dan():
    fx = rfx("aura_ket_dan", "Hao quang Ket Dan", "green swirling ribbons with a small golden core")
    gm = fx.mat("gm", "#32c860", grad=dict(src="attr", pow=1.0), opacity=0.75)
    gc = fx.mat("gc", "#8cf090", grad=dict(src="attr", pow=0.6), core="#e8ffd0", opacity=1.0)
    gold = fx.mat("gold", "#ffb830", grad=dict(src="radial", pow=1.2, cpow=4.0), core="#fff2b0", opacity=0.9)

    def helix(k, wmul):
        def f(t, i):
            pts, ws = [], []
            n = 22
            for j in range(n + 1):
                u = j / n
                y = -0.85 + 1.7 * u
                ph = TAU * (t + k / 3.0) + u * TAU * 1.0
                x = 0.7 * math.sin(ph) * (0.85 + 0.15 * math.cos(u * PI))
                depth = 0.5 + 0.5 * math.cos(ph)
                pts.append((x, y))
                ws.append(wmul * (0.04 + 0.1 * depth) * (1 - abs(u - 0.5) * 1.1))
            return MB().strip(pts, ws, soft=True)
        return f
    for k in range(3):
        fx.per_frame("hg%d" % k, gm, helix(k, 2.0))
        fx.per_frame("hc%d" % k, gc, helix(k, 0.8))
    g = MB().disc(0, 0, 0.3, 20, 1, 0).build(fx, "core", gold, y=0.05)
    fx.track(g, lambda t, i: dict(y=0.05, s=1.0 + 0.12 * math.sin(TAU * t), op=0.9))
    star4(fx, "cs", fx.mat("cs", "#fff6c0"), 0.2, lambda t: (0, 0.05, 0.8 + 0.2 * math.sin(TAU * t)))
    return fx


def _flames(id, name_vi, where, cols, rx, ry, n, h, w, embers=None, **kw):
    fx = rfx(id, name_vi, where, fps=10, **kw)
    mats = []
    for i, (c, hs, ws) in enumerate(cols):
        mats.append((fx.mat("f%d" % i, c, grad=dict(src="attr", pow=0.4), opacity=0.9 if i == 0 else 1.0), hs, ws))
    flame_ring(fx, "fl", mats, rx, ry, n, h, w, y0=-0.05, skip_bottom=True)
    if embers:
        em = fx.mat("ember", embers)
        for j in range(8):
            x0 = -0.6 + 0.17 * j + 0.05 * (j % 2)
            mote(fx, "e%d" % j, em, 0.035, (lambda x0, j: lambda t: (x0 + 0.08 * math.sin(TAU * (t + j / 8.0)), -0.2 + 1.15 * ((t + j / 8.0) % 1), (1 - ((t + j / 8.0) % 1)) ** 0.6))(x0, j), "diamond")
    return fx


@reg("aura_nguyen_anh")
def aura_nguyen_anh():
    return _flames("aura_nguyen_anh", "Hao quang Nguyen Anh", "teal-gold flame outline around the cultivator",
                   [("#18c8b0", 1.0, 1.0), ("#5ee8c8", 0.7, 0.7), ("#ffd868", 0.4, 0.45)], 0.6, 0.78, 12, 0.52, 0.36)


@reg("aura_hoa_than")
def aura_hoa_than():
    fx = rfx("aura_hoa_than", "Hao quang Hoa Than", "violet light pillar (see-through, glowing edges) with a thin halo ring and rising sparks")
    edge = fx.mat("edge", "#9a60ff", grad=dict(src="attr", pow=0.9), opacity=0.9, ufade=0.9)
    edge2 = fx.mat("edge2", "#e6d4ff", grad=dict(src="attr", pow=1.4), opacity=0.9, ufade=1.0)
    haze = fx.mat("haze", "#7a44ff", grad=dict(src="attr", pow=1.6), opacity=0.05, ufade=1.1)
    hard = fx.mat("hard", "#efe0ff")
    soft = fx.mat("soft", "#8a50ff", grad=dict(src="attr", pow=1.2), opacity=0.5)
    spk = fx.mat("spk", "#f4eaff")
    y0, y1 = -0.85, 1.3
    n = 10
    for sgn in (-1, 1):
        def beam(w, x):
            return MB().strip([(x, y0 + (y1 - y0) * k / n) for k in range(n + 1)], w, soft=True)
        ob = beam(0.26, sgn * 0.5).build(fx, "e%d" % sgn, edge)
        fx.track(ob, lambda t, i, sgn=sgn: dict(x=0, op=0.85 + 0.15 * math.sin(TAU * t + sgn)))
        ob = beam(0.09, sgn * 0.5).build(fx, "c%d" % sgn, edge2)
        fx.track(ob, lambda t, i: dict(op=0.9))
    # light motes drifting up inside the beam
    hy = 0.95
    MB().ring(0, hy, 0.55, 0.14, soft=True, ky=0.28).build(fx, "halo_s", soft)
    ob = MB().ring(0, hy, 0.55, 0.035, ky=0.28).build(fx, "halo_h", hard)
    fx.track(ob, lambda t, i: dict(op=0.95))
    for j in range(5):
        a0 = TAU * j / 5
        star4(fx, "hs%d" % j, spk, 0.1, lambda t, a0=a0: (0.55 * math.cos(a0 + TAU * t), hy + 0.55 * 0.28 * math.sin(a0 + TAU * t), 0.6 + 0.4 * math.sin(TAU * t + a0 * 2) ** 2))
    for j in range(10):
        x0 = -0.5 + j / 9.0
        mote(fx, "r%d" % j, spk, 0.032, (lambda x0, j: lambda t: (x0 + 0.06 * math.sin(j + TAU * t), -0.75 + 1.9 * ((t + j * 0.27) % 1), math.sin(PI * ((t + j * 0.27) % 1)) + 0.001))(x0, j), "diamond" if j % 2 else "star")
    return fx


@reg("aura_luyen_hu")
def aura_luyen_hu():
    return _flames("aura_luyen_hu", "Hao quang Luyen Hu", "roaring red-gold flame around the cultivator",
                   [("#e02010", 1.0, 1.0), ("#ff7a1c", 0.72, 0.75), ("#ffe070", 0.42, 0.5)], 0.62, 0.8, 12, 0.78, 0.36, embers="#ffb040")


@reg("aura_hop_the")
def aura_hop_the():
    fx = rfx("aura_hop_the", "Hao quang Hop The", "ice-blue crystal storm orbiting the cultivator")
    body = fx.mat("body", "#4aa8ff")
    edge = fx.mat("edge", "#c8ecff")
    gl = fx.mat("gl", "#2a70ff", grad=dict(src="radial", pow=2.0), opacity=0.35)
    swirl = fx.mat("sw", "#6ac0ff", grad=dict(src="attr", pow=0.9), opacity=0.8)

    def arc(a0, r, span):
        pts = [(r * math.cos(a0 + span * k / 14), r * 0.62 * math.sin(a0 + span * k / 14)) for k in range(15)]
        return MB().strip(pts, [0.04 + 0.1 * math.sin(PI * k / 14) for k in range(15)], soft=True)
    for k in range(3):
        ob = arc(TAU * k / 3, 0.9, 1.9).build(fx, "arc%d" % k, swirl)
        fx.track(ob, lambda t, i, k=k: dict(rot=TAU * t))
    rng = fx.rng
    for j in range(10):
        a0 = TAU * j / 10
        rx = 0.7 + 0.28 * ((j * 7) % 3) / 2
        ry = rx * 0.7
        sp = 1 if j % 2 == 0 else -1
        L = 0.28 + 0.1 * (j % 3)
        mb = MB().diamond(0, 0, L * 1.2, L * 0.5, PI / 2)
        ob = mb.build(fx, "cr%d" % j, body)
        hi = MB().diamond(-L * 0.06, L * 0.1, L * 0.55, L * 0.16, PI / 2).build(fx, "hi%d" % j, edge)
        fx.track(ob, lambda t, i, a0=a0, rx=rx, ry=ry, sp=sp, j=j: dict(x=rx * math.cos(a0 + sp * TAU * t), y=-0.05 + ry * math.sin(a0 + sp * TAU * t),
                                                                          rot=TAU * t * sp * (1 + j % 2) + j, s=0.85 + 0.2 * math.sin(a0 + sp * TAU * t)))
        fx.track(hi, lambda t, i, a0=a0, rx=rx, ry=ry, sp=sp, j=j: dict(x=rx * math.cos(a0 + sp * TAU * t), y=-0.05 + ry * math.sin(a0 + sp * TAU * t),
                                                                          rot=TAU * t * sp * (1 + j % 2) + j, s=0.85 + 0.2 * math.sin(a0 + sp * TAU * t)))
        g = MB().disc(0, 0, 0.2, 10, 1, 0).build(fx, "cg%d" % j, gl)
        fx.track(g, lambda t, i, a0=a0, rx=rx, ry=ry, sp=sp: dict(x=rx * math.cos(a0 + sp * TAU * t), y=-0.05 + ry * math.sin(a0 + sp * TAU * t)))
    for j in range(5):
        star4(fx, "gl%d" % j, edge, 0.09, lambda t, j=j: (0.9 * math.cos(j * 1.3 + TAU * t * -1), -0.05 + 0.6 * math.sin(j * 1.3 + TAU * t * -1), 0.5 + 0.5 * math.sin(TAU * t * 2 + j) ** 2))
    return fx


@reg("aura_dai_thua")
def aura_dai_thua():
    fx = rfx("aura_dai_thua", "Hao quang Dai Thua", "cosmic purple-gold nebula with stars", halo=0.7)
    rng = fx.rng
    cols = ["#7a3cf0", "#c040d8", "#4a60e8", "#a050ff"]
    for k in range(4):
        m = fx.mat("neb%d" % k, cols[k], grad=dict(src="radial", pow=1.6), opacity=0.22)
        for side in (0, 1):
            a0 = TAU * k / 4 / 2 + side * PI
            ob = MB().disc(0, 0, 0.62, 24, 1, 0).build(fx, "neb%d_%d" % (k, side), m)
            fx.track(ob, lambda t, i, a0=a0, k=k: dict(x=0.62 * math.cos(a0 + PI * t) * (1.0 if k % 2 == 0 else 0.8), y=0.7 * 0.62 * math.sin(a0 + PI * t) * (1.0 if k % 2 == 0 else 0.8) + 0.0, s=1.0 + 0.1 * math.sin(TAU * t * 2 + k)))

    def arm(a0, wm):
        pts, ws = [], []
        for k in range(26):
            u = k / 25
            r = 0.12 + 0.95 * u
            a = a0 + 3.0 * u
            pts.append((r * math.cos(a), 0.8 * r * math.sin(a)))
            ws.append(wm * (0.05 + 0.18 * math.sin(PI * u) ** 0.8))
        return MB().strip(pts, ws, soft=True)
    gold = fx.mat("armg", "#ffc84a", grad=dict(src="attr", pow=1.0), opacity=0.55)
    pur = fx.mat("armp", "#9050ff", grad=dict(src="attr", pow=1.0), opacity=0.32)
    for k in range(2):
        for nm, wm, fm in (("p", 1.7, pur), ("g", 0.8, gold)):
            ob = arm(PI * k, wm).build(fx, "arm%s%d" % (nm, k), fm)
            fx.track(ob, lambda t, i: dict(rot=-PI * t))
    core = fx.mat("core", "#ffc040", grad=dict(src="radial", pow=1.2, cpow=4.0), core="#fffbe0", opacity=0.85)
    ob = MB().disc(0, 0, 0.26, 20, 1, 0).build(fx, "core", core)
    fx.track(ob, lambda t, i: dict(s=1.0 + 0.1 * math.sin(TAU * t)))
    sm = [fx.mat("s1", "#fff4d0"), fx.mat("s2", "#d0c8ff")]
    for j in range(22):
        r = 0.2 + 1.15 * math.sqrt(rng.random())
        a = rng.uniform(0, TAU)
        ph = rng.random()
        mb = MB().star(0, 0, 4, 0.1 if j % 5 == 0 else 0.06, 0.02, PI / 2)
        ob = mb.build(fx, "st%d" % j, sm[j % 2])
        fx.track(ob, lambda t, i, r=r, a=a, ph=ph: dict(x=r * math.cos(a), y=0.9 * r * math.sin(a), s=0.15 + 0.85 * (0.5 + 0.5 * math.sin(TAU * (t + ph))) ** 1.5 + 0.001))
    return fx


# ================================================================ story FX
@reg("dot_pha")
def dot_pha():
    fx = rfx("dot_pha", "Dot pha", "realm breakthrough: light gathers inward, then bursts upward", frames=10, fps=10, loop=False, halo=0.95)
    rng = fx.rng
    gold = fx.mat("gold", "#ffd860")
    white = fx.mat("white", "#fffbe8")
    glow = fx.mat("glow", "#ffc850", grad=dict(src="radial", pow=1.2))
    core = fx.mat("core", "#ffe890", grad=dict(src="radial", pow=0.6, cpow=3.0), core="#ffffff")
    beam = fx.mat("beam", "#ffe070", grad=dict(src="attr", pow=0.7), core="#ffffff", ufade=0.7)
    beamw = fx.mat("beamw", "#ffffff", grad=dict(src="attr", pow=0.8), ufade=0.6)
    TG = 0.55
    N = 16
    for j in range(N):
        a0 = TAU * j / N + rng.uniform(-0.1, 0.1)
        d = (j % 8) / 8.0 * 0.22
        r0 = rng.uniform(1.0, 1.25)

        def f(t, j=j, a0=a0, d=d, r0=r0):
            tt = sat((t - d) / (TG - d))
            if t > TG + 0.02 or tt <= 0:
                return None
            r = r0 * (1 - tt) ** 1.4 + 0.12
            a = a0 + 1.9 * tt
            return (r * math.cos(a), 0.9 * r * math.sin(a), 0.5 + 0.7 * math.sin(PI * min(1, tt * 1.1)) + 0.001)
        mote(fx, "in%d" % j, white if j % 2 else gold, 0.06, f, "diamond" if j % 3 == 0 else "star")
    g = MB().disc(0, 0, 1.0, 32, 1, 0).build(fx, "gglow", glow)
    fx.track(g, lambda t, i: dict(s=0.15 + 0.7 * sat(t / TG) if t <= TG + 0.03 else 0.0, op=0.3 + 0.7 * sat(t / TG), show=t <= TG + 0.05))
    c = MB().disc(0, 0, 0.5, 24, 1, 0).build(fx, "gcore", core)
    fx.track(c, lambda t, i: dict(s=0.1 + 0.6 * sat(t / TG) ** 1.2, op=0.4 + 0.6 * sat(t / TG), show=t <= TG + 0.05))
    rr = fx.per_frame("gring", gold, lambda t, i: MB().ring(0, 0, 1.1 * (1 - sat(t / TG)) ** 1.3 + 0.25, 0.05 + 0.03 * sat(t / TG), seg=40, ky=0.9))
    for i, ob in enumerate(rr):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and t <= TG + 0.03), op=0.4 + 0.6 * sat(t / TG)))
    # release (frames 6..9): bright core beam with rays; it fades by getting thinner and sparser
    FL_S = [0.01] * 6 + [0.45, 0.55, 0.35, 0.01]
    fl = MB().disc(0, 0, 1.0, 36, 1, 0).build(fx, "flash", glow)
    fx.track(fl, lambda t, i: dict(s=FL_S[i], op=0.55, show=i in (6, 7, 8)))
    fc = MB().disc(0, 0, 0.5, 24, 1, 0.5).build(fx, "fcore", white)
    fx.track(fc, lambda t, i: dict(s=([0.01] * 6 + [0.45, 0.35, 0.2, 0.01])[i], op=0.9, show=i in (6, 7, 8)))
    BW = [0.01] * 6 + [0.9, 1.0, 0.6, 0.01]
    for nm, w, fm, wm in (("b", 0.7, beam, 1.0), ("bw", 0.22, beamw, 1.0)):
        mb = MB().strip([(0, -0.55 + 1.85 * k / 10) for k in range(11)], w, soft=True)
        ob = mb.build(fx, nm, fm)
        fx.track(ob, lambda t, i, wm=wm: dict(sx=BW[i], op=1.0, show=BW[i] > 0.05))
    # rays fanning up from the heart
    for j in range(9):
        a = PI / 2 + (j - 4) * 0.27
        ob = MB().diamond(0, 0, 0.9, 0.07).build(fx, "ray%d" % j, gold if j % 2 else white)
        vis = [6, 7, 8] if j % 2 == 0 else [6, 7]
        fx.track(ob, lambda t, i, a=a, vis=vis: dict(x=0.4 * math.cos(a), y=0.4 * math.sin(a) - 0.1, rot=a, s=[1.0, 1.0, 0.7][vis.index(i)] if i in vis else 0.001, show=i in vis))
    for i in (6, 7, 8):
        pass
    sh = fx.per_frame("shock", gold, lambda t, i: MB().ring(0, -0.5, 0.3 + 0.25 * max(0, i - 5) if i >= 6 else 0.3, 0.09 - 0.02 * max(0, i - 6), seg=40, ky=0.32))
    for i, ob in enumerate(sh):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and 6 <= i <= 8), op=0.95))
    for j in range(14):
        a = rng.uniform(-0.7, 0.7)
        x0 = rng.uniform(-0.45, 0.45)
        vy = rng.uniform(0.9, 1.5)
        t0 = 0.62 + 0.03 * (j % 4)

        def f(t, x0=x0, a=a, vy=vy, t0=t0):
            age = (t - t0) / 0.42
            if age < 0 or age > 1.0:
                return None
            return (x0 + a * age, -0.2 + vy * age * 0.85, 0.35 + 0.65 * (1 - age) ** 0.5)
        mote(fx, "up%d" % j, white if j % 2 else gold, 0.06, f, "star" if j % 3 == 0 else "diamond")
    return fx


@reg("loi_kiep")
def loi_kiep():
    fx = rfx("loi_kiep", "Loi kiep", "tribulation lightning striking down on the cultivator", frames=8, fps=12, loop=False, halo=1.0)
    rng = fx.rng
    vio = fx.mat("vio", "#7a40ff", grad=dict(src="attr", pow=1.3), opacity=0.8)
    mid = fx.mat("mid", "#b8a0ff")
    core = fx.mat("core", "#ffffff")
    glow = fx.mat("glow", "#8a60ff", grad=dict(src="radial", pow=1.3))
    wcore = fx.mat("wcore", "#f4eaff", grad=dict(src="radial", pow=0.7), opacity=1.0)
    top, foot = (0.12, 1.2), (0.0, -0.56)
    WM = [0.0, 1.0, 1.15, 1.0, 0.7, 0.5, 0.3, 0.12]
    OPB = [0.0, 1.0, 1.0, 1.0, 0.85, 0.65, 0.4, 0.2]

    def bolt(t, i):
        r = random.Random(100 + i * 13)
        pts = jag(top, foot, r, 13, 0.16)
        mb = MB()
        mb.strip(pts, WM[i] * 0.34, soft=True)
        return mb

    def boltc(w):
        def f(t, i):
            r = random.Random(100 + i * 13)
            pts = jag(top, foot, r, 13, 0.16)
            mb = MB()
            ws = [w * WM[i] * (0.7 + 0.3 * math.sin(k)) for k in range(14)]
            mb.strip(pts, ws)
            for b in range(3):
                j = r.randint(3, 9)
                p0 = pts[j]
                ang = -PI / 2 + r.choice((-1, 1)) * r.uniform(0.5, 1.0)
                p1 = (p0[0] + 0.5 * math.cos(ang), p0[1] + 0.5 * math.sin(ang))
                mb.strip(jag(p0, p1, r, 5, 0.07), [w * WM[i] * 0.5 * (1 - k / 5) + 0.01 for k in range(6)])
            return mb
        return f
    fx.per_frame("bg", vio, bolt, post=None)
    fx.per_frame("bm", mid, boltc(0.14))
    fx.per_frame("bc", core, boltc(0.06))
    # flash at the top and at the strike point
    tg = MB().disc(0, 0, 0.55, 24, 1, 0).build(fx, "topglow", glow, y=1.05)
    fx.track(tg, lambda t, i: dict(y=1.05, s=[0.4, 0.7, 0.8, 0.7, 0.55, 0.4, 0.25, 0.1][i], op=OPB[i] * 0.45))
    fg = MB().disc(0, 0, 1.0, 32, 1, 0).build(fx, "footglow", glow)
    fx.track(fg, lambda t, i: dict(y=-0.56, sx=0.7, sy=0.4, op=[0.0, 0.8, 0.8, 0.6, 0.4, 0.25, 0.1, 0.0][i]))
    wc = MB().disc(0, 0, 0.5, 24, 1, 0).build(fx, "footcore", wcore)
    fx.track(wc, lambda t, i: dict(y=-0.56, sx=[0.01, 0.6, 0.7, 0.5, 0.3, 0.2, 0.1, 0.01][i], sy=[0.01, 0.35, 0.4, 0.3, 0.2, 0.1, 0.06, 0.01][i], op=1.0))
    sh = fx.per_frame("shock", core, lambda t, i: MB().ring(0, -0.56, [0.2, 0.3, 0.5, 0.72, 0.95, 1.1, 1.2, 1.25][i], [0.05, 0.12, 0.1, 0.08, 0.06, 0.04, 0.03, 0.02][i], seg=40, ky=0.32))
    for i, ob in enumerate(sh):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and i >= 1), op=[0, 1, 1, 0.9, 0.7, 0.5, 0.3, 0.1][i]))
    for j in range(10):
        a = rng.uniform(0, PI)
        sp = rng.uniform(0.5, 1.0)

        def f(t, a=a, sp=sp, j=j):
            age = (t - 0.15 - 0.02 * (j % 3)) / 0.6
            if age < 0 or age > 1:
                return None
            return (0.9 * sp * math.cos(a) * age, -0.5 + 1.0 * sp * math.sin(a) * age - 0.3 * age * age, (1 - age) ** 0.6)
        mote(fx, "sp%d" % j, core if j % 2 else mid, 0.05, f, "diamond")
    return fx


@reg("thang_cap")
def thang_cap():
    fx = rfx("thang_cap", "Thang cap", "level-up: bright beam with rays, rising sparkle rings, sparkles", frames=6, fps=10, loop=False, halo=0.9)
    rng = fx.rng
    gold = fx.mat("gold", "#ffd860")
    white = fx.mat("white", "#fffbe8")
    green = fx.mat("green", "#7aec9a")
    soft = fx.mat("soft", "#ffc040", grad=dict(src="attr", pow=1.2), opacity=0.6)
    beam = fx.mat("beam", "#ffe070", grad=dict(src="attr", pow=0.7), core="#ffffff", ufade=0.6)
    beamw = fx.mat("beamw", "#ffffff", grad=dict(src="attr", pow=0.8), ufade=0.5)
    BW = [0.6, 1.0, 1.0, 0.7, 0.35, 0.0]
    for nm, w, fm in (("b", 0.55, beam), ("bw", 0.16, beamw)):
        ob = MB().strip([(0, -0.8 + 1.9 * k / 10) for k in range(11)], w, soft=True).build(fx, nm, fm)
        fx.track(ob, lambda t, i: dict(sx=BW[i] + 0.001, op=1.0, show=BW[i] > 0))
    VIS = [[0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7], [3, 4, 5, 6, 7], [4, 5, 6, 7], [5, 6, 7], [6, 7]]
    for j in range(9):
        a = PI / 2 + (j - 4) * 0.23
        ob = MB().diamond(0, 0, 0.8, 0.06).build(fx, "ray%d" % j, gold if j % 2 else white)
        life = [5, 4, 4, 3, 3, 3, 2, 2, 1][j] if False else (5 - abs(j - 4))      # centre rays live longest
        fx.track(ob, lambda t, i, a=a, life=life: dict(x=0.3 * math.cos(a), y=-0.25 + 0.3 * math.sin(a), rot=a, s=(1.0 - 0.1 * i), show=i < life))

    def ry(t, delay):
        tt = sat((t - delay) / (1 - delay))
        return -0.7 + 1.55 * ease_out(tt), tt
    for k, (delay, fm) in enumerate(((0.0, gold), (0.25, white))):
        for nm, w, mt, soft_ in (("h", 0.07, fm, False), ("g", 0.2, soft, True)):
            ob = MB().ring(0, 0, 0.8, w, seg=40, ky=0.3, soft=soft_).build(fx, "ring%s%d" % (nm, k), mt)
            fx.track(ob, lambda t, i, delay=delay: dict(y=ry(t, delay)[0], s=1.0 + 0.12 * ry(t, delay)[1], op=0.95,
                                                    show=(t >= delay - 1e-6 and ry(t, delay)[1] < 0.95)))
    for j in range(8):
        a0 = TAU * j / 8
        star4(fx, "sp%d" % j, green if j % 3 == 0 else (white if j % 2 else gold), 0.14,
              lambda t, a0=a0, j=j: (0.8 * math.cos(a0 + 0.6 * t), ry(t, 0.0)[0] + 0.8 * 0.3 * math.sin(a0 + 0.6 * t) + 0.25 * t,
                                     (math.sin(PI * min(1, t * 0.95 + 0.05)) ** 0.6) * (0.7 + 0.3 * (j % 2)) * (0.6 if t > 0.9 else 1.0) + 0.001))
    for j in range(10):
        x0 = rng.uniform(-0.6, 0.6)
        mote(fx, "m%d" % j, white if j % 2 else gold, 0.045, (lambda x0, j: lambda t: (x0, -0.7 + 1.5 * sat(t * 1.0 + j * 0.02), 0.35 + 0.65 * math.sin(PI * sat(t * 0.9 + (j % 3) * 0.05))))(x0, j), "star" if j % 2 else "diamond")
    return fx


def all_ids():
    return ["dot_pha", "loi_kiep", "thang_cap"]       # the realm auras moved to fx_aura.py (two sheets each, 128x128)


def make(id):
    return REG[id]()
