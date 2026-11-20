"""A. Ngu kiem phi hanh (sword flight): shadow, wake, wind, clouds, take-off, landing."""
import math
from tilib import *

REG = {}


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


# ------------------------------------------------------------------------------ phi_bong
@reg("phi_bong")
def phi_bong():
    fx = FxP("phi_bong", view="ground", frames=4, fps=6, loop=True, mode="alpha", px=64, ground=True,
             alpha_levels=4, name_vi="Bóng phi hành",
             where="soft shadow on the ground under a flyer (scale by height)")
    soft = fx.mat("soft", "#14101c", grad=dict(src="attr", pow=1.1), opacity=0.42)
    hard = fx.mat("hard", "#0b0a10", opacity=0.32)
    a = glow_disc(0.92, 36).build(fx, "soft", soft)
    b = MB().disc(0, 0, 0.55, 30).build(fx, "hard", hard)
    fx.track(a, lambda t, i: dict(s=1.0 + 0.035 * math.sin(TAU * t), op=0.42 + 0.03 * math.sin(TAU * t)))
    fx.track(b, lambda t, i: dict(s=1.0 + 0.05 * math.sin(TAU * t + 0.6), op=0.3))
    return fx


# ------------------------------------------------------------------------------ phi_vet
@reg("phi_vet")
def phi_vet():
    fx = FxP("phi_vet", frames=6, fps=12, loop=True, px=96, pivot=(80, 48), halo=0.6, levels=4,
             name_vi="Vệt kiếm quang",
             where="thin tapering ribbon of light behind the flying sword (trails LEFT, pivot = the sword's tail, fades out in ~50 px)")
    L = 1.75
    N = 16
    glow = fx.mat("glow", "#18a0c8", grad=dict(src="attr", pow=0.9), opacity=0.6)
    mid = fx.mat("mid", "#5ae0f4", grad=dict(src="attr", pow=0.4), opacity=0.9)
    core = fx.mat("core", "#d8fcff")
    silk = fx.mat("silk", "#5ae0f4", grad=dict(src="attr", pow=0.6), opacity=0.6)

    def ribbon(L_, amp, w0, ph, freq, y0=0.0, soft=True, wpow=1.1):
        def b(t, i):
            pts, ws = [], []
            for k in range(N + 1):
                s = k / N
                pts.append((-s * L_, y0 + amp * s * math.sin(TAU * (freq * s - t) + ph)))
                ws.append(w0 * (1 - s) ** wpow * (0.5 + 0.5 * min(1.0, s / 0.12)) + 0.006)
            return MB().strip(pts, ws, soft=soft)
        return b

    fx.per_frame("glow", glow, ribbon(L, 0.05, 0.27, 0.0, 1.0))
    fx.per_frame("mid", mid, ribbon(L * 0.85, 0.045, 0.12, 0.0, 1.0))
    fx.per_frame("core", core, ribbon(L * 0.55, 0.03, 0.04, 0.0, 1.0, soft=False))
    fx.per_frame("silk_a", silk, ribbon(L * 0.5, 0.1, 0.05, 1.2, 1.5, y0=0.1))
    fx.per_frame("silk_b", silk, ribbon(L * 0.4, 0.09, 0.045, 3.4, 1.5, y0=-0.1))
    for j in range(4):
        mote(fx, "sp%d" % j, core, "star" if j % 2 else "diamond", 0.045,
             (lambda ph, y: lambda t: (-0.2 - 1.3 * ((t + ph) % 1), y * (1 + 0.8 * ((t + ph) % 1)),
                                       math.sin(PI * ((t + ph) % 1)) ** 0.6))(j / 4.0, (-0.1, 0.12, -0.05, 0.08)[j]))
    return fx


# ------------------------------------------------------------------------------ phi_gio
@reg("phi_gio")
def phi_gio():
    fx = FxP("phi_gio", frames=6, fps=12, loop=True, px=64, halo=0.6, levels=4,
             name_vi="Gió vút", where="wind streaks rushing past the flyer (subtle, streaks head LEFT)")
    body = fx.mat("b", "#6aa8e8", grad=dict(src="attr", pow=0.6), opacity=0.9)
    core = fx.mat("c", "#d8ecff", grad=dict(src="attr", pow=0.4), opacity=0.9)
    spec = ((0.62, 0.8, 0.045, 0.00), (0.22, 0.6, 0.04, 0.37), (-0.18, 0.85, 0.05, 0.71),
            (-0.55, 0.55, 0.035, 0.18), (0.78, 0.45, 0.03, 0.55))
    for j, (y, L, w, ph) in enumerate(spec):
        for nm, fm, wm, lm in (("b", body, 1.8, 1.0), ("c", core, 0.7, 0.7)):
            pts = [(L / 2 * lm - L * lm * k / 8, y) for k in range(9)]
            mb = MB().strip(pts, [w * wm * (0.3 + 0.7 * (k < 3 or (1 - (k - 3) / 5))) for k in range(9)], soft=True)
            ob = mb.build(fx, "s%d%s" % (j, nm), fm)

            def f(t, i, ph=ph):
                s = (t + ph) % 1.0
                return dict(x=0.58 - 1.16 * s, sx=math.sin(PI * s) ** 0.5 + 0.001, sy=1.0)
            fx.track(ob, f)
    # two tiny curls
    for j, (y, ph) in enumerate(((0.4, 0.2), (-0.38, 0.62))):
        ob = MB().ring(0, 0, 0.1, 0.035, -0.4, PI * 1.25, seg=10).build(fx, "curl%d" % j, core)
        fx.track(ob, lambda t, i, y=y, ph=ph: dict(x=0.5 - 1.0 * ((t + ph) % 1), y=y,
                                                   s=math.sin(PI * ((t + ph) % 1)) ** 0.5 + 0.001, rot=-TAU * t))
    return fx


# ------------------------------------------------------------------------------ phi_may
def cloud(mb_lo, mb_hi, w, h):
    """flat-bottomed cloud of overlapping puffs; lo = shade body, hi = lit top (offset up-left)."""
    xs = (-0.5, -0.22, 0.05, 0.3, 0.52)
    rs = (0.45, 0.72, 0.9, 0.68, 0.4)
    for x, r in zip(xs, rs):
        mb_lo.disc(x * w, r * h * 0.5, r * h * 0.5 + 0.02, 14)
    for x, r in zip(xs[1:4], rs[1:4]):
        mb_hi.disc(x * w - 0.04, r * h * 0.5 + h * 0.12, r * h * 0.34, 12)


@reg("phi_may")
def phi_may():
    fx = FxP("phi_may", frames=6, fps=8, loop=True, mode="alpha", px=96, pivot=(48, 56), alpha_levels=3,
             name_vi="Gió mây dưới kiếm", where="thin flat wisps of mist streaking LEFT under the flying sword (pivot = feet)")
    mist = fx.mat("mist", "#cfdbe8", grad=dict(src="attr", pow=0.7), opacity=0.55)
    lite = fx.mat("lite", "#f2fbff", grad=dict(src="attr", pow=0.5), opacity=0.6)
    # (y, length, thickness, phase, passes per loop, light?)
    spec = ((-0.1, 1.2, 0.1, 0.0, 1, 0), (-0.26, 0.7, 0.075, 0.4, 2, 1), (-0.38, 1.3, 0.11, 0.7, 1, 0),
            (-0.52, 0.8, 0.07, 0.2, 2, 1), (-0.2, 0.5, 0.06, 0.65, 2, 0), (-0.66, 0.95, 0.09, 0.5, 1, 0))
    for j, (y, L, th, ph, m, lt) in enumerate(spec):
        pts = [(-L / 2 + L * k / 8, y) for k in range(9)]
        mb = MB().strip(pts, [th * (0.25 + 0.75 * math.sin(PI * (k + 0.5) / 9.0) ** 0.8) for k in range(9)], soft=True)
        ob = mb.build(fx, "w%d" % j, lite if lt else mist)

        def f(t, i, y=y, ph=ph, m=m):
            s = (t * m + ph) % 1.0
            e = min(1.0, 1.7 * math.sin(PI * s) ** 0.8)
            return dict(x=1.0 - 2.0 * s, sx=e + 0.001, show=e > 0.2)
        fx.track(ob, f)
    return fx


# ------------------------------------------------------------------------------ take-off / landing
DUST_A, DUST_B = "#cdb893", "#e9ddc2"


# a puff = a little cloud of three bumps: shade layer (low, darker) under a lit layer (same bumps, smaller, up)
BUMPS = [("s0", "lo", 0.62, -0.5, -0.15), ("s1", "lo", 0.58, 0.5, -0.15), ("s2", "lo", 0.7, 0.0, 0.1),
         ("l0", "hi", 0.5, -0.5, -0.02), ("l1", "hi", 0.46, 0.5, -0.02), ("l2", "hi", 0.58, 0.0, 0.25)]


def puffs(fx, tag, n, r0, r1, s0, s1, rise, ops, ang0=0.0, jit=0.0):
    """ring of billboard dust puffs flying outward (shade disc + lit highlight disc, two tones);
    sizes s0->s1 (radius, units), per-frame opacity list `ops`."""
    rng = fx.rng
    lo = fx.mat(tag + "lo", "#b8a47c", opacity=0.8)
    hi = fx.mat(tag + "hi", "#eadfc0", opacity=0.85)
    for j in range(n):
        a = ang0 + TAU * j / n + rng.uniform(-jit, jit)
        rr = rng.uniform(0.92, 1.08)
        k = 0.8 + 0.4 * ((j * 7) % 3) / 2
        for nm, fm, r, dx, dy in BUMPS:
            fm = lo if fm == "lo" else hi
            ob = MB().disc(0, 0, r, 14).build(fx, "%s%s%d" % (tag, nm, j), fm)
            fx.billboard(ob)

            def f(t, i, a=a, rr=rr, k=k, dx=dx, dy=dy):
                s = (s0 + (s1 - s0) * ease_out(t)) * k
                rad = (r0 + (r1 - r0) * ease_out(t)) * rr
                return dict(x=math.cos(a) * rad + dx * s, y=math.sin(a) * rad,
                            z=rise * ease_out(t) + 0.04 + dy * s, s=s, op=ops[i], show=ops[i] > 0.01)
            fx.track(ob, f)


@reg("phi_cat_canh")
def phi_cat_canh():
    fx = FxP("phi_cat_canh", view="ground", frames=7, fps=14, loop=False, mode="alpha", px=96, ground=True,
             alpha_levels=4, name_vi="Cất cánh",
             where="take-off: a ring of qi blasts outward on the ground with dust, then drifts up (one-shot)")
    ring = fx.mat("ring", "#5ae0f4", opacity=1.0)
    ringg = fx.mat("ringg", "#d8fcff", opacity=1.0)
    haze = fx.mat("haze", "#5ae0f4", grad=dict(src="attr", pow=0.8), opacity=0.8)
    wh = fx.mat("wh", "#f4feff", opacity=1.0)
    R = lambda t: 0.28 + 1.1 * ease_out(t)
    W = lambda t: 0.16 * (1 - t) + 0.035
    OPS = [1, 1, 0.95, 0.85, 0.7, 0.5, 0.3]
    # soft disc of light under the feet at the start
    hz = glow_disc(1.0, 32).build(fx, "haze", haze)
    fx.track(hz, lambda t, i: dict(s=[0.4, 0.7, 0.85, 0.8, 0.6, 0.45, 0.3][i], op=[0.8, 0.7, 0.5, 0.35, 0.2, 0.1, 0.0][i], show=i < 6))
    # the blast ring (hard, double)
    rings = fx.per_frame("ring", ring, lambda t, i: MB().ring(0, 0, R(t), W(t), seg=48))
    rings2 = fx.per_frame("ringc", ringg, lambda t, i: MB().ring(0, 0, R(t) - 0.02, W(t) * 0.38, seg=48))
    # radial speed strokes
    for j in range(6):
        a = TAU * j / 6 + 0.2
        ob = MB().line((0, 0), (0.4, 0), 0.05, taper=True).build(fx, "st%d" % j, ringg)
        fx.track(ob, lambda t, i, a=a: dict(x=math.cos(a) * (0.3 + 1.0 * ease_out(t)), y=math.sin(a) * (0.3 + 1.0 * ease_out(t)),
                                            rot=a, s=[0.6, 1.0, 1.0, 0.8, 0.5, 0.0, 0.0][i] + 0.001, show=i < 5))
    puffs(fx, "dA", 7, 0.35, 1.2, 0.09, 0.17, 0.12, [0.95, 1, 1, 0.85, 0.6, 0.35, 0.15], ang0=0.2, jit=0.1)
    puffs(fx, "dB", 4, 0.2, 0.75, 0.07, 0.12, 0.3, [0, 0.9, 0.9, 0.7, 0.45, 0.25, 0.1], ang0=1.1, jit=0.2)
    # qi motes lifting off
    for j in range(5):
        a = TAU * j / 5 + 0.5
        mote(fx, "m%d" % j, wh, "star" if j % 2 else "diamond", 0.07,
             (lambda a, j: lambda t: (math.cos(a) * 0.35 * (1 + t), math.sin(a) * 0.15, (math.sin(PI * min(1, t * 1.05)) ** 0.5) * (0.6 + 0.4 * (j % 2)) + 0.001,
                                      0.0, 0.1 + 1.45 * ease_out(t) * (0.6 + 0.1 * j)))(a, j), billboard=True)
    return fx


@reg("phi_ha_canh")
def phi_ha_canh():
    fx = FxP("phi_ha_canh", view="ground", frames=6, fps=14, loop=False, mode="alpha", px=96, ground=True,
             alpha_levels=4, name_vi="Hạ cánh", where="landing: dust ring and a soft flash (one-shot)")
    flash = fx.mat("flash", "#f4feff", grad=dict(src="attr", pow=0.9), opacity=0.95)
    ring = fx.mat("ring", "#b0f0ff", opacity=1.0)
    ringc = fx.mat("ringc", "#f4feff", opacity=1.0)
    fb = glow_disc(1.0, 32).build(fx, "flash", flash)
    fx.billboard(fb)
    fx.track(fb, lambda t, i: dict(y=0.0, z=0.18, s=[0.55, 1.0, 0.8, 0.5, 0.3, 0.1][i], op=[1, 0.8, 0.5, 0.3, 0.12, 0.0][i], show=i < 5))
    R = lambda t: 0.25 + 1.05 * ease_out(t)
    W = lambda t: 0.13 * (1 - t) + 0.03
    fx.per_frame("ring", ring, lambda t, i: MB().ring(0, 0, R(t), W(t), seg=48))
    fx.per_frame("ringc", ringc, lambda t, i: MB().ring(0, 0, R(t) - 0.02, W(t) * 0.35, seg=48))
    puffs(fx, "dA", 8, 0.3, 1.2, 0.11, 0.2, 0.15, [1, 1, 0.9, 0.7, 0.45, 0.25], ang0=0.1, jit=0.12)
    puffs(fx, "dB", 5, 0.15, 0.7, 0.08, 0.14, 0.25, [0.9, 0.9, 0.75, 0.5, 0.3, 0.15], ang0=0.5, jit=0.2)
    for j in range(6):
        a = TAU * j / 6 + 0.3
        mote(fx, "sp%d" % j, ringc, "star" if j % 2 else "diamond", 0.06,
             burst_mote(math.cos(a) * 0.3, math.sin(a) * 0.12, math.cos(a) * 0.6, math.sin(a) * 0.2, 0.0, 0.9, 0.0, 1.0, 0.5), billboard=True)
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
