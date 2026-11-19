"""Combat FX, 64x64, front view. One builder per effect; each returns a ready Fx scene."""
import math
from fxlib import *

PIXEL = 1 / 32.0
REG = {}


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


# ---------------------------------------------------------------- small shapes (2D, origin centred)
def sh_diamond(mb, s):
    mb.diamond(0, 0, s * 1.7, s * 0.75)


def sh_star4(mb, s):
    mb.star(0, 0, 4, s, s * 0.2, PI / 2)


def sh_disc(mb, s):
    mb.disc(0, 0, s * 0.5, 10)


def sh_leaf(mb, s):
    mb.diamond(0, 0, s * 1.9, s * 0.8)
    mb.line((-s * 0.95, 0), (-s * 1.25, 0), s * 0.15)


def sh_drop(mb, s):
    mb.drop(0, 0, s * 1.9, s * 0.9)


def sh_rock(mb, s):
    rng = random.Random(int(s * 1000))
    pts = [(s * 0.6 * math.cos(TAU * i / 6) * rng.uniform(0.7, 1.1), s * 0.6 * math.sin(TAU * i / 6) * rng.uniform(0.7, 1.1))
           for i in range(6)]
    mb.fan(0, 0, pts)


def sh_bolt(mb, s):
    mb.poly([(-s * .3, s), (s * .45, s * .05), (s * .05, s * .05), (s * .3, -s), (-s * .45, -s * .05), (-s * .05, -s * .05)])


SHAPES = dict(diamond=sh_diamond, star=sh_star4, disc=sh_disc, leaf=sh_leaf, drop=sh_drop, rock=sh_rock, bolt=sh_bolt)

FLAVOUR = {  # element -> (shape, gravity, count)
    "tho": ("rock", -2.4, 7), "kim": ("star", 0.0, 6), "hoa": ("diamond", 1.1, 9),
    "moc": ("leaf", -0.6, 8), "thuy": ("drop", -1.6, 8), "loi": ("bolt", 0.0, 6),
}


def particle(fx, name, fm, shape, size, fn):
    """one small object animated by fn(t) -> (x, y, scale, rot) or None."""
    mb = MB()
    SHAPES[shape](mb, size)
    ob = mb.build(fx, name, fm)

    def f(t, i):
        r = fn(t)
        if r is None:
            return None
        x, y, s, rot = r
        return dict(x=x, y=y, s=max(s, 1e-3), rot=rot)
    return fx.track(ob, f)


def flight(x0, y0, vx, vy, t0, life, g=0.0, size0=1.0, spin=0.0, fade_pow=0.6):
    """Ballistic particle born at t0 living `life` (in 0..1 clip time)."""
    def fn(t):
        age = (t - t0) / life
        if age < 0 or age > 1:
            return None
        x = x0 + vx * age
        y = y0 + vy * age + 0.5 * g * age * age
        return (x, y, size0 * (1 - age) ** fade_pow, spin * age)
    return fn


# ================================================================= slash
SLASH_W = {"tho": 1.3, "kim": 0.8, "hoa": 1.15, "moc": 1.0, "thuy": 1.05, "loi": 0.85}
VI_EL = {"tho": "Tho", "kim": "Kim", "hoa": "Hoa", "moc": "Moc", "thuy": "Thuy", "loi": "Loi"}


def make_slash(el):
    body, core = ELEM[el]
    fx = Fx("slash_" + el, frames=5, fps=18, halo=0.7, name_vi="Kiem quang " + VI_EL[el],
            where="melee slash overlay when the player's blade attack lands (rotate to the swing)")
    rng = fx.rng
    cx, cy, R = 0.0, -0.5, 0.9
    a0, a1 = math.radians(160), math.radians(22)
    n = 40
    jit = {"loi": 0.045}.get(el, 0.0)

    def crescent(wm, soft, off=0.0):
        pts, ws = [], []
        for k in range(n + 1):
            u = k / n
            a = a0 + (a1 - a0) * u
            rr = R + off + (rng.uniform(-jit, jit) if 0 < k < n else 0)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            ws.append(wm * 0.46 * math.sin(PI * u) ** 0.75 * (0.25 + 0.75 * u ** 0.8) + 0.012)
        return MB().strip(pts, ws, soft=soft)

    wm = SLASH_W[el]
    glow = fx.mat("glow", body, grad=dict(src="attr", pow=1.3), window=True)
    mid = fx.mat("mid", body, window=True, grad=dict(src="attr", pow=0.15))
    cor = fx.mat("core", core, window=True)
    HEAD = [0.5, 0.92, 1.1, 1.1, 1.1]
    TAIL = [-0.25, -0.05, 0.12, 0.45, 0.85]
    OP = [1.0, 1.0, 0.85, 0.5, 0.22]
    for nm, mb, fm, k in (("glow", crescent(wm * 1.55, True), glow, 0.8), ("mid", crescent(wm, False), mid, 1.0),
                          ("core", crescent(wm * 0.3, False, 0.01), cor, 1.0)):
        ob = mb.build(fx, nm, fm)
        fx.track(ob, lambda t, i, k=k: dict(op=OP[i] * k, head=HEAD[i], tail=TAIL[i]))
    if el == "kim":                                  # parallel hair-lines + tip glint
        for off in (-0.2, 0.19):
            mb = MB()
            pts = [(cx + (R + off) * math.cos(a0 + (a1 - a0) * u / 20 * 0.8), cy + (R + off) * math.sin(a0 + (a1 - a0) * u / 20 * 0.8)) for u in range(21)]
            mb.strip(pts, [0.02 + 0.03 * math.sin(PI * u / 20) for u in range(21)])
            ob = mb.build(fx, "hair%d" % int(off * 100), cor)
            fx.track(ob, lambda t, i: dict(op=OP[i] * 0.8, head=HEAD[i] * 0.85, tail=TAIL[i] + 0.1))
        tip = (cx + R * math.cos(a1), cy + R * math.sin(a1))
        mb = MB().star(0, 0, 4, 0.5, 0.06, PI / 2)
        ob = mb.build(fx, "tip", cor)
        fx.track(ob, lambda t, i: dict(x=tip[0] - 0.05, y=tip[1], s=[0.2, 0.9, 1.0, 0.6, 0.0][i] + 0.001, rot=0))
    # flavour bits flung from the arc
    shape, g, cnt = FLAVOUR[el]
    bm = fx.mat("bits", core if el in ("kim", "loi") else body)
    for j in range(cnt):
        u = 0.45 + 0.5 * j / max(cnt - 1, 1) + rng.uniform(-0.03, 0.03)
        a = a0 + (a1 - a0) * u
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        out = (math.cos(a), math.sin(a))
        sp = rng.uniform(0.25, 0.5)
        particle(fx, "bit%d" % j, bm, shape, rng.uniform(0.07, 0.11),
                 flight(px, py, out[0] * sp * 0.6 + 0.05, out[1] * sp + (0.35 if el == "hoa" else 0.0), 0.2 + 0.45 * (1 - u) + 0.1, 0.55,
                        g * 0.3, 1.0, rng.uniform(-3, 3)))
    return fx


# ================================================================= bolt (projectile, points right)
def make_bolt(el):
    body, core = ELEM[el]
    fx = Fx("bolt_" + el, frames=4, fps=14, loop=True, halo=0.8, name_vi="Phap cau " + VI_EL[el],
            where="projectile of a cast spell; sprite points right, the game rotates it")
    rng = fx.rng
    glow = fx.mat("glow", body, grad=dict(src="radial", pow=1.6), opacity=0.9)
    fl = fx.mat("body", body, grad=dict(src="radial", pow=0.35, cpow=5.0), core=core)
    cor = fx.mat("core", core)
    hx = 0.38      # head centre x
    # tail: tapered ribbon running left, flickering width via 4 variants
    def tail(t, i):
        pts = [(hx - 0.1 - k * 0.07, math.sin((k * 0.9) - TAU * t) * 0.045 * (k / 9)) for k in range(10)]
        ws = [0.34 * (1 - k / 10) ** 1.1 * (1 + 0.1 * math.sin(TAU * t + k)) for k in range(10)]
        return MB().strip(pts, ws, soft=True)
    fx.per_frame("tail", glow, tail)
    fx.per_frame("tail2", fl, lambda t, i: MB().strip([(hx - 0.05 - k * 0.055, math.sin(k * 0.9 - TAU * t) * 0.03 * (k / 9)) for k in range(9)],
                                                      [0.2 * (1 - k / 9) ** 1.2 for k in range(9)], soft=True))
    # head by element
    mb = MB()
    if el == "tho":
        sh_rock(mb, 0.55)
    elif el == "kim":
        mb.diamond(0, 0, 0.95, 0.3)
    elif el == "hoa":
        mb.disc(0, 0, 0.2, 18)
    elif el == "moc":
        mb.diamond(0, 0, 0.62, 0.26)
    elif el == "thuy":
        mb.drop(0, 0, 0.74, 0.36)
    else:
        mb.disc(0, 0, 0.17, 16)
    head = mb.build(fx, "head", fl, x=hx)
    fx.track(head, lambda t, i: dict(x=hx, rot=(TAU * t if el in ("tho", "moc") else 0.0), s=1.0))
    halo = MB().disc(0, 0, 0.5, 24, g_c=1, g_e=0).build(fx, "halo", glow, x=hx)
    fx.track(halo, lambda t, i: dict(x=hx, s=1.0 + 0.1 * math.sin(TAU * t), op=0.55))
    ci = MB()
    if el == "kim":
        ci.diamond(0, 0, 0.6, 0.12)
    elif el == "tho":
        ci.disc(-0.04, 0.05, 0.08, 8)
    elif el == "moc":
        ci.diamond(0, 0, 0.4, 0.07)
    else:
        ci.disc(0, 0, 0.1, 12)
    c = ci.build(fx, "corehead", cor, x=hx)
    fx.track(c, lambda t, i: dict(x=hx, rot=(TAU * t if el == "moc" else 0)))
    if el == "hoa":                         # flame tongue behind the fireball
        fx.per_frame("fl", fl, lambda t, i: MB().poly([(hx + 0.05, 0.17), (hx - 0.5 - 0.06 * math.sin(TAU * t), 0.07), (hx - 0.28, 0.0), (hx - 0.55 - 0.08 * math.cos(TAU * t), -0.09), (hx + 0.05, -0.17)]))
    if el == "loi":                         # crackling arcs around the orb
        def arcs(t, i):
            mb = MB()
            r = random.Random(i * 7 + 3)
            for _ in range(3):
                a = r.uniform(0, TAU)
                mb.strip(jag((hx + 0.1 * math.cos(a), 0.1 * math.sin(a)), (hx + 0.34 * math.cos(a + r.uniform(-.5, .5)), 0.34 * math.sin(a + r.uniform(-.5, .5))), r, 5, 0.06), 0.035)
            return mb
        fx.per_frame("arcs", cor, arcs)
    if el == "thuy":
        ring = MB().ring(0, 0, 0.3, 0.035, soft=False)
        r = ring.build(fx, "ripple", cor, x=hx)
        fx.track(r, lambda t, i: dict(x=hx, sx=0.55 + 0.7 * t, sy=0.55 + 0.7 * t, op=1 - t))
    if el == "tho":
        for j in range(5):
            particle(fx, "dust%d" % j, fx.mat("d%d" % j, body), "rock", 0.06 + 0.02 * (j % 2),
                     (lambda j: lambda t: (hx - 0.2 - ((t + j / 5.0) % 1) * 0.9, 0.14 * math.sin(j * 2.1) * (1 + (t + j / 5.0) % 1), 0.8 * math.sin(PI * ((t + j / 5.0) % 1)) + 0.01, TAU * t))(j))
    else:
        shape = {"kim": "star", "hoa": "diamond", "moc": "leaf", "thuy": "drop", "loi": "bolt"}[el]
        sm = fx.mat("bits", core if el in ("kim", "loi") else body)
        for j in range(5):
            particle(fx, "tr%d" % j, sm, shape, 0.06 if el != "moc" else 0.07,
                     (lambda j: lambda t: (hx - 0.25 - ((t + j / 5.0) % 1) * 0.95, 0.13 * math.sin(j * 2.3 + 1) * (0.5 + (t + j / 5.0) % 1), (1 - ((t + j / 5.0) % 1)) ** 0.7 * 1.0 + 0.001, TAU * t * 0.0))(j))
    return fx


# ================================================================= burst (impact)
def make_burst(el):
    body, core = ELEM[el]
    fx = Fx("burst_" + el, frames=6, fps=16, halo=0.8, name_vi="Bao pha " + VI_EL[el],
            where="impact of a spell / projectile on the target")
    rng = fx.rng
    glow = fx.mat("glow", body, grad=dict(src="radial", pow=2.4))
    flash = fx.mat("flash", body, grad=dict(src="radial", pow=0.5), core=core)
    cor = fx.mat("core", core)
    bodym = fx.mat("body", body)
    F = MB().disc(0, 0, 1.0, 32, g_c=1, g_e=0).build(fx, "flash", glow)
    fx.track(F, lambda t, i: dict(s=[0.55, 0.8, 0.95, 1.0, 1.0, 0.9][i], op=[1, 0.9, 0.55, 0.3, 0.12, 0.0][i]))
    D = MB().disc(0, 0, 0.5, 28, g_c=1, g_e=0.0).build(fx, "disc", flash)
    fx.track(D, lambda t, i: dict(s=[0.8, 1.0, 0.8, 0.5, 0.25, 0.1][i], op=[1, 1, 0.85, 0.6, 0.3, 0.0][i]))
    # explicit shockwave ring (hard edge), thickness shrinks as it grows
    def ringb(i):
        r = [0.2, 0.38, 0.56, 0.7, 0.8, 0.86][i]
        w = [0.2, 0.16, 0.12, 0.08, 0.05, 0.035][i]
        if i < 4:
            return MB().ring(0, 0, r, w, seg=40)
        rr = random.Random(11 + i)
        mb = MB()
        if i == 4:                                    # the ring starts to break: 8 arcs, small gaps
            for k in range(8):
                a = TAU * k / 8 + 0.1
                mb.ring(0, 0, r, w, a, a + TAU / 8 - 0.22, seg=8)
        else:                                         # last frame: a few arcs and sparks drifting out
            for k in range(5):
                a = rr.uniform(0, TAU)
                mb.ring(0, 0, r + rr.uniform(-0.04, 0.05), w, a, a + rr.uniform(0.25, 0.55), seg=6)
            for k in range(7):
                a = rr.uniform(0, TAU)
                rad = r + rr.uniform(0.02, 0.1)
                mb.diamond(rad * math.cos(a), rad * math.sin(a), 0.08, 0.035, a)
        return mb
    objs = fx.per_frame("ring", cor, lambda t, i: ringb(i))
    objs2 = fx.per_frame("ringb", bodym, lambda t, i: ringb(i), post=None)
    for i, ob in enumerate(objs2):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i), s=1.07, op=[1, 1, 0.9, 0.7, 0.45, 0.2][ii]))
    # radial shards
    n = 10
    for j in range(n):
        a = TAU * j / n + rng.uniform(-0.12, 0.12)
        L = rng.uniform(0.28, 0.42)
        mb = MB().diamond(0, 0, L, 0.1 + 0.04 * (j % 2), 0)
        ob = mb.build(fx, "shard%d" % j, cor if j % 2 == 0 else bodym)
        far = rng.uniform(0.7, 0.95)
        fx.track(ob, lambda t, i, a=a, far=far: dict(
            x=math.cos(a) * far * ease_out(min(1, t * 1.25)) * 0.9 + 0.0, y=math.sin(a) * far * ease_out(min(1, t * 1.25)) * 0.9,
            rot=a, s=max(0.001, (1 - t) ** 0.8) * (0.4 + 0.6 * min(1, t * 6)), show=t < 0.95))
    # flavour debris
    shape, g, cnt = FLAVOUR[el]
    sm = fx.mat("bits", core if el in ("kim", "loi") else body)
    for j in range(cnt):
        a = TAU * (j + 0.5) / cnt + rng.uniform(-0.2, 0.2)
        sp = rng.uniform(0.45, 0.8)
        particle(fx, "bit%d" % j, sm, shape, rng.uniform(0.09, 0.14),
                 flight(0.1 * math.cos(a), 0.1 * math.sin(a), math.cos(a) * sp, math.sin(a) * sp + (0.25 if g > 0 else 0), 0.05, 0.9, g * 0.45, 1.0, rng.uniform(-4, 4)))
    return fx


# ================================================================= misc combat
@reg("hit_spark")
def hit_spark():
    fx = Fx("hit_spark", frames=4, fps=18, halo=0.7, name_vi="Tia lua va cham", where="any normal hit on a target")
    rng = fx.rng
    gl = fx.mat("glow", "#ffcc55", grad=dict(src="radial", pow=1.4))
    cor = fx.mat("core", "#fffbe8")
    am = fx.mat("amber", "#ffb030")
    d = MB().disc(0, 0, 0.5, 20, 1, 0).build(fx, "flash", gl)
    fx.track(d, lambda t, i: dict(s=[0.6, 0.8, 0.6, 0.3][i], op=[1, 0.8, 0.4, 0.0][i]))
    st = MB().star(0, 0, 4, 0.55, 0.09, PI / 4).build(fx, "star", cor)
    fx.track(st, lambda t, i: dict(s=[0.6, 1.0, 0.7, 0.2][i], rot=0.2 * i))
    for j in range(8):
        a = TAU * j / 8 + 0.2
        ob = MB().diamond(0, 0, 0.3, 0.07).build(fx, "ray%d" % j, cor if j % 2 else am)
        r0 = [0.15, 0.32, 0.5, 0.62][0:4]
        fx.track(ob, lambda t, i, a=a: dict(x=math.cos(a) * [0.15, 0.34, 0.52, 0.64][i], y=math.sin(a) * [0.15, 0.34, 0.52, 0.64][i], rot=a, s=[0.9, 1.0, 0.8, 0.35][i]))
    return fx


@reg("hit_crit")
def hit_crit():
    fx = Fx("hit_crit", frames=5, fps=16, halo=0.9, name_vi="Bao kich", where="critical hit (bigger, star-shaped)")
    rng = fx.rng
    gl = fx.mat("glow", "#ff7a1c", grad=dict(src="radial", pow=1.2))
    cor = fx.mat("core", "#fffbe0")
    am = fx.mat("amber", "#ffc23a")
    rd = fx.mat("red", "#ff3b22")
    d = MB().disc(0, 0, 1.0, 28, 1, 0).build(fx, "flash", gl)
    fx.track(d, lambda t, i: dict(s=[0.6, 0.9, 1.0, 0.9, 0.7][i], op=[1, 0.9, 0.6, 0.3, 0.1][i]))
    big = MB().star(0, 0, 8, 0.95, 0.12, 0).build(fx, "star8", am)
    fx.track(big, lambda t, i: dict(s=[0.5, 1.0, 0.9, 0.6, 0.25][i], rot=[0, 0.1, 0.2, 0.3, 0.4][i] * 0.5))
    sm = MB().star(0, 0, 4, 1.0, 0.14, PI / 4).build(fx, "star4", cor)
    fx.track(sm, lambda t, i: dict(s=[0.4, 0.95, 0.85, 0.5, 0.2][i], rot=[0, 0.05, 0.1, 0.15, 0.2][i]))
    c = MB().disc(0, 0, 0.26, 16).build(fx, "core", cor)
    fx.track(c, lambda t, i: dict(s=[1.0, 1.1, 0.8, 0.4, 0.1][i]))
    for j in range(10):
        a = TAU * j / 10 + 0.15
        ob = MB().diamond(0, 0, 0.34, 0.07).build(fx, "ray%d" % j, rd if j % 2 else am)
        fx.track(ob, lambda t, i, a=a: dict(x=math.cos(a) * [0.3, 0.55, 0.75, 0.88, 0.95][i], y=math.sin(a) * [0.3, 0.55, 0.75, 0.88, 0.95][i], rot=a, s=[0.8, 1.0, 0.9, 0.55, 0.25][i]))
    return fx


@reg("parry")
def parry():
    fx = Fx("parry", frames=5, fps=16, halo=0.9, name_vi="Do don", where="player answered right: the blow is deflected")
    rng = fx.rng
    gl = fx.mat("glow", "#6ad8ff", grad=dict(src="radial", pow=1.4))
    cor = fx.mat("core", "#ffffff")
    bl = fx.mat("blue", "#42b4ff")
    d = MB().disc(0, 0, 0.9, 28, 1, 0).build(fx, "flash", gl)
    fx.track(d, lambda t, i: dict(s=[0.5, 0.9, 1.0, 0.9, 0.7][i], op=[1, 0.8, 0.5, 0.25, 0.08][i]))
    objs = fx.per_frame("ring", cor, lambda t, i: MB().ring(0, 0, [0.22, 0.45, 0.62, 0.74, 0.82][i], [0.17, 0.13, 0.09, 0.06, 0.03][i], seg=40))
    objs2 = fx.per_frame("ringb", bl, lambda t, i: MB().ring(0, 0, [0.22, 0.45, 0.62, 0.74, 0.82][i], [0.17, 0.13, 0.09, 0.06, 0.03][i], seg=40))
    for i, ob in enumerate(objs2):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i), s=1.1))
    hz = MB().diamond(0, 0, 1.9, 0.09).build(fx, "hline", cor)     # horizontal glint of steel on steel
    fx.track(hz, lambda t, i: dict(s=[0.6, 1.0, 0.8, 0.4, 0.0][i] + 0.001, rot=-0.35))
    x4 = MB().star(0, 0, 4, 0.5, 0.07, PI / 2).build(fx, "x", cor)
    fx.track(x4, lambda t, i: dict(s=[0.8, 1.0, 0.6, 0.3, 0.0][i] + 0.001, rot=PI / 4))
    for j in range(8):
        a = TAU * j / 8 + 0.4
        ob = MB().diamond(0, 0, 0.2, 0.05).build(fx, "sp%d" % j, cor if j % 2 else bl)
        rr = [0.35, 0.55, 0.7, 0.8, 0.86]
        fx.track(ob, lambda t, i, a=a: dict(x=math.cos(a) * rr[i], y=math.sin(a) * rr[i], rot=a + PI / 2 * 0, s=[1, 1, 0.8, 0.5, 0.2][i]))
    return fx


@reg("guard_break")
def guard_break():
    fx = Fx("guard_break", frames=5, fps=14, halo=0.8, name_vi="Pha khien", where="wrong answer: the guard shatters")
    rng = fx.rng
    bl = fx.mat("blue", "#52b8ff", grad=dict(src="radial", pow=0.4), core="#e8f8ff")
    gl = fx.mat("glow", "#2a7cff", grad=dict(src="radial", pow=1.4))
    cor = fx.mat("core", "#ffffff")
    rd = fx.mat("red", "#ff4a3a")
    # kite shield outline, 10 points
    out = []
    for k in range(13):
        a = PI * k / 12
        out.append((-0.62 * math.cos(a), 0.6 + 0.08 * math.sin(a) - (0.0)))   # curved top edge, left->right below
    out = [(-0.62, 0.55), (-0.3, 0.68), (0.3, 0.68), (0.62, 0.55), (0.6, 0.0), (0.38, -0.45), (0.0, -0.78), (-0.38, -0.45), (-0.6, 0.0)]
    cx, cy = 0.0, 0.0
    d = MB().disc(0, 0, 0.9, 28, 1, 0).build(fx, "flash", gl)
    fx.track(d, lambda t, i: dict(s=[0.7, 0.9, 1.0, 0.9, 0.8][i], op=[0.25, 0.7, 0.3, 0.0, 0.0][i]))
    pieces = []
    m = len(out)
    cen = [(0.05, 0.08), (-0.18, 0.2), (0.2, -0.12)]
    for k in range(m):
        p, q = out[k], out[(k + 1) % m]
        c = (p[0] * 0.25 + q[0] * 0.25 + 0.0, p[1] * 0.25 + q[1] * 0.25 + 0.05)
        pieces.append((p, q, c))
        mb = MB().poly([c, p, q])
        ob = mb.build(fx, "shard%d" % k, bl)
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        ang = math.atan2(mid[1], mid[0])
        spd = rng.uniform(0.35, 0.6)
        rot = rng.uniform(-1.5, 1.5)
        fx.track(ob, lambda t, i, ang=ang, spd=spd, rot=rot: dict(
            x=(0 if i < 2 else math.cos(ang) * spd * (i - 1.4) * 0.3), y=(0 if i < 2 else math.sin(ang) * spd * (i - 1.4) * 0.3 - 0.02 * (i - 1.5) ** 2 * (i > 1)),
            rot=(0 if i < 2 else rot * (i - 1) * 0.4), s=[1.0, 1.0, 1.0, 0.9, 0.7][i] * (0.96 if i < 2 else 1.0), op=[1, 1, 0.95, 0.6, 0.25][i]))
        # bright edge on every shard
        e = MB().strip([p, q], 0.045).build(fx, "edge%d" % k, cor)
        fx.track(e, lambda t, i, ang=ang, spd=spd, rot=rot: dict(
            x=(0 if i < 2 else math.cos(ang) * spd * (i - 1.4) * 0.3), y=(0 if i < 2 else math.sin(ang) * spd * (i - 1.4) * 0.3 - 0.02 * (i - 1.5) ** 2 * (i > 1)),
            rot=(0 if i < 2 else rot * (i - 1) * 0.4), s=[1.0, 1.0, 1.0, 0.9, 0.7][i], op=[0.7, 1, 0.95, 0.6, 0.25][i]))
    # cracks: jagged bright lines from the centre, appear frames 0-1
    def cracks(t, i):
        r = random.Random(5)
        mb = MB()
        for j in range(6):
            a = TAU * j / 6 + 0.3
            L = [0.25, 0.55][min(i, 1)] * r.uniform(0.9, 1.2)
            mb.strip(jag((0, 0), (math.cos(a) * L, math.sin(a) * L), r, 5, 0.07), 0.035)
        return mb
    objs = fx.per_frame("crack", cor, cracks)
    for i, ob in enumerate(objs):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and i < 2)))
    ring = fx.per_frame("ring", rd, lambda t, i: MB().ring(0, 0, [0.3, 0.5, 0.75, 0.9, 1.0][i], [0.12, 0.1, 0.07, 0.05, 0.03][i], seg=36))
    for i, ob in enumerate(ring):
        fx.track(ob, lambda t, ii, i=i: dict(show=False))
    return fx


@reg("dust_step")
def dust_step():
    fx = Fx("dust_step", frames=4, fps=10, mode="alpha", name_vi="Bui buoc chan", where="footstep puff under the feet",
            pivot=(32, 52), alpha_levels=4)
    m = fx.mat("dust", "#cdb893", opacity=0.75)
    m2 = fx.mat("dust2", "#e9ddc2", opacity=0.8)
    for j, (x0, y0, r0, dx, dy) in enumerate(((-0.15, -0.55, 0.2, -0.3, 0.12), (0.12, -0.58, 0.18, 0.28, 0.14), (0.0, -0.5, 0.25, 0.0, 0.25), (-0.32, -0.6, 0.14, -0.4, 0.06), (0.3, -0.6, 0.14, 0.4, 0.07))):
        mb = MB().disc(0, 0, r0, 14)
        ob = mb.build(fx, "puff%d" % j, m if j % 2 == 0 else m2)
        fx.track(ob, lambda t, i, x0=x0, y0=y0, dx=dx, dy=dy: dict(
            x=x0 + dx * ease_out(t), y=y0 + dy * ease_out(t), s=0.5 + 1.1 * ease_out(t) + 0.3 * t, op=[0.9, 0.8, 0.5, 0.2][i]))
    return fx


@reg("dash_trail")
def dash_trail():
    fx = Fx("dash_trail", frames=4, fps=16, halo=0.6, name_vi="Vet luot", where="behind a dodging / dashing player (streaks point left)")
    rng = fx.rng
    cor = fx.mat("core", "#f2fcff", window=True)
    bl = fx.mat("blue", "#6cc8ff", window=True, grad=dict(src="attr", pow=0.6))
    for j, (y, L, w) in enumerate(((0.28, 0.9, 0.09), (0.0, 1.35, 0.15), (-0.3, 1.0, 0.1), (0.5, 0.6, 0.05), (-0.52, 0.65, 0.06))):
        pts = [(0.3 - 0.75 * L * k / 10, y) for k in range(11)]
        for nm, fm, wm in (("b", bl, 1.7), ("c", cor, 0.8)):
            mb = MB().strip(pts, [w * wm * (0.2 + 0.8 * (1 - k / 10) ** 0.6) for k in range(11)], soft=(nm == "b"))
            ob = mb.build(fx, "st%d%s" % (j, nm), fm)
            # u runs along the streak from the front (u=0) to the tail (u=1)
            fx.track(ob, lambda t, i, j=j: dict(x=-0.04 * i, head=1.05, tail=[-0.4, -0.1, 0.25, 0.6][i] + 0.0, op=[1, 0.9, 0.6, 0.3][i]))
    return fx


@reg("heal")
def heal():
    fx = Fx("heal", frames=6, fps=10, loop=True, halo=0.7, name_vi="Hoi phuc", where="HP restored: rising green-gold motes")
    rng = fx.rng
    gr = fx.mat("green", "#4ee06a")
    gd = fx.mat("gold", "#ffe27a")
    wh = fx.mat("white", "#f4ffe6")
    gl = fx.mat("glow", "#38c860", grad=dict(src="radial", pow=2.2), opacity=0.5)
    g = MB().disc(0, 0, 0.8, 28, 1, 0).build(fx, "glow", gl, y=-0.45)
    fx.track(g, lambda t, i: dict(y=-0.4, sx=1.0, sy=0.55, op=0.5 + 0.2 * math.sin(TAU * t)))
    for j in range(9):
        ph = j / 9.0
        x0 = rng.uniform(-0.55, 0.55)
        sw = rng.uniform(0.05, 0.12)
        sz = rng.uniform(0.07, 0.11)
        shape = "star" if j % 3 == 0 else "disc"
        fm = (gd, gr, wh)[j % 3]
        particle(fx, "mote%d" % j, fm, shape, sz * (1.4 if shape == "star" else 1.0),
                 (lambda x0, sw, ph, sz: lambda t: (x0 + sw * math.sin(TAU * (t + ph)), -0.55 + 1.35 * ((t + ph) % 1), math.sin(PI * ((t + ph) % 1)) ** 0.7 + 0.001, 0))(x0, sw, ph, sz))
    # plus signs
    for j, (x0, ph) in enumerate(((-0.3, 0.1), (0.32, 0.55))):
        mb = MB().poly([(-0.04, 0.16), (0.04, 0.16), (0.04, 0.04), (0.16, 0.04), (0.16, -0.04), (0.04, -0.04), (0.04, -0.16), (-0.04, -0.16), (-0.04, -0.04), (-0.16, -0.04), (-0.16, 0.04), (-0.04, 0.04)])
        ob = mb.build(fx, "plus%d" % j, wh)
        fx.track(ob, lambda t, i, x0=x0, ph=ph: dict(x=x0, y=-0.4 + 1.2 * ((t + ph) % 1), s=math.sin(PI * ((t + ph) % 1)) ** 0.7 + 0.001))
    return fx


@reg("linh_thuan")
def linh_thuan():
    fx = Fx("linh_thuan", frames=6, fps=8, loop=True, halo=0.6, name_vi="Linh thuan", where="translucent spirit-shield dome around the player (correct streak); mostly empty inside")
    rng = fx.rng
    rim = fx.mat("rim", "#3ab8ff", grad=dict(src="rim", pow=14.0, cpow=8.0), core="#d8f8ff", opacity=1.0)
    body = fx.mat("body", "#2a90ff", grad=dict(src="rim", pow=4.5), opacity=0.07)
    gd = fx.mat("gold", "#ffe6a0")
    wh = fx.mat("white", "#ffffff")
    facet = fx.mat("facet", "#68d0ff", opacity=0.9)
    lit = fx.mat("lit", "#a8e8ff", opacity=0.5)
    b = MB().disc(0, 0, 0.88, 40).build(fx, "bubble", body)
    fx.track(b, lambda t, i: dict(s=1.0 + 0.025 * math.sin(TAU * t), op=0.9))
    r = MB().disc(0, 0, 0.88, 40).build(fx, "rim", rim)
    fx.track(r, lambda t, i: dict(s=1.0 + 0.025 * math.sin(TAU * t)))
    # honeycomb facets: thin hex outlines, a few of them catch the light and pulse
    hexes = []
    R = 0.25
    for q in range(-3, 4):
        for p in range(-3, 4):
            cx = (q + p * 0.5) * R * 1.75
            cy = p * R * 1.52
            if math.hypot(cx, cy) < 0.66:
                hexes.append((cx, cy))
    mb = MB()
    for cx, cy in hexes:
        mb.ring(cx, cy, R * 0.98, 0.016, seg=6, a0=PI / 6, a1=PI / 6 + TAU - 1e-6)
    ob = mb.build(fx, "facets", facet)
    fx.track(ob, lambda t, i: dict(s=1.0 + 0.025 * math.sin(TAU * t), op=0.35))
    for j, (cx, cy) in enumerate(hexes):
        if (j * 5) % 7 == 0:
            f = MB().fan(0, 0, [(R * 0.9 * math.cos(PI / 6 + TAU * k / 6), R * 0.9 * math.sin(PI / 6 + TAU * k / 6)) for k in range(6)])
            o = f.build(fx, "lit%d" % j, lit)
            fx.track(o, lambda t, i, cx=cx, cy=cy, j=j: dict(x=cx, y=cy, op=0.55 * (0.5 + 0.5 * math.sin(TAU * t + j * 1.3)), s=1.0))
    for nm, (a0, a1, rad, w) in {"h1": (110, 165, 0.72, 0.06), "h2": (176, 188, 0.72, 0.04), "h3": (-30, -5, 0.72, 0.035)}.items():
        ob = MB().ring(0, 0, rad, w, math.radians(a0), math.radians(a1), soft=False).build(fx, nm, wh)
        fx.track(ob, lambda t, i: dict(s=1.0 + 0.025 * math.sin(TAU * t), op=0.7 + 0.3 * math.sin(TAU * t)))
    for j in range(3):
        a0 = TAU * j / 3
        particle(fx, "gl%d" % j, wh, "star", 0.1, (lambda a0: lambda t: (0.84 * math.cos(a0 + TAU * t / 3), 0.84 * math.sin(a0 + TAU * t / 3), 0.5 + 0.5 * math.sin(TAU * t * 2 + a0 * 3) ** 2, 0))(a0))
    return fx


@reg("pickup_glow")
def pickup_glow():
    fx = Fx("pickup_glow", frames=6, fps=8, loop=True, halo=0.9, name_vi="Anh sang nhat do", where="soft light pillar over a weapon lying on the ground",
            pivot=(32, 50))
    rng = fx.rng
    gl = fx.mat("glow", "#ffc040", grad=dict(src="radial", pow=1.6), opacity=0.7)
    pil = fx.mat("pillar", "#ffcf58", grad=dict(src="attr", pow=1.3), opacity=0.45)
    cor = fx.mat("core", "#fff8dc")
    d = MB().disc(0, 0, 0.9, 30, 1, 0).build(fx, "base", gl)
    fx.track(d, lambda t, i: dict(y=-0.62, sx=1.0, sy=0.38, op=0.8 + 0.15 * math.sin(TAU * t)))
    # pillar: vertical strip, soft sides, fading upward
    def pillar(w):
        m = MB()
        m.strip([(0, -0.6 + 1.5 * k / 8) for k in range(9)], [w * (1 - 0.35 * k / 8) for k in range(9)], soft=True)
        return m
    p = pillar(0.8).build(fx, "pillar", pil)
    fx.track(p, lambda t, i: dict(sx=1.0 + 0.05 * math.sin(TAU * t), op=0.55 + 0.2 * math.sin(TAU * t + 1)))
    p2 = pillar(0.3).build(fx, "pillar2", pil)
    fx.track(p2, lambda t, i: dict(op=0.55))
    ring = MB().ring(0, 0, 0.75, 0.05).build(fx, "ring", cor)
    fx.track(ring, lambda t, i: dict(y=-0.6, sx=1.0 + 0.1 * math.sin(TAU * t), sy=(1.0 + 0.1 * math.sin(TAU * t)) * 0.38, op=0.9))
    for j in range(6):
        ph = j / 6.0
        x0 = rng.uniform(-0.4, 0.4)
        particle(fx, "m%d" % j, cor, "star" if j % 2 else "disc", 0.09, (lambda x0, ph: lambda t: (x0, -0.55 + 1.3 * ((t + ph) % 1), math.sin(PI * ((t + ph) % 1)) ** 0.7 + 0.001, 0))(x0, ph))
    return fx


@reg("chest_open")
def chest_open():
    fx = Fx("chest_open", frames=6, fps=10, halo=0.9, name_vi="Mo ruong", where="treasure chest opens: a fan of golden light",
            pivot=(32, 44))
    rng = fx.rng
    gl = fx.mat("glow", "#ffb030", grad=dict(src="radial", pow=2.2))
    fan = fx.mat("fan", "#ffd060", grad=dict(src="attr", pow=0.8), opacity=0.9)
    cor = fx.mat("core", "#fff4cc")
    g = MB().disc(0, 0, 0.9, 30, 1, 0).build(fx, "glow", gl)
    fx.track(g, lambda t, i: dict(y=-0.15, s=[0.25, 0.45, 0.6, 0.65, 0.55, 0.4][i], op=[0.5, 0.7, 0.8, 0.7, 0.5, 0.25][i]))
    # beams: tapered fan blades from the chest mouth, growing then fading
    for j in range(7):
        a = PI / 2 + (j - 3) * 0.26
        mb = MB().strip([(0, 0), (0.5 * math.cos(a), 0.5 * math.sin(a)), (1.25 * math.cos(a), 1.25 * math.sin(a))], [0.26, 0.2, 0.02], soft=True)
        ob = mb.build(fx, "beam%d" % j, fan)
        fx.track(ob, lambda t, i, a=a, j=j: dict(y=-0.25, sx=[0.0, 0.5, 1.0, 1.0, 0.9, 0.6][i] + 0.001, sy=[0.0, 0.6, 1.0, 1.0, 0.9, 0.6][i] + 0.001,
                                                    op=[0, 0.8, 1.0, 0.9, 0.6, 0.25][i] * (0.7 + 0.3 * math.sin(j * 2.3 + i))))
    box = MB().disc(0, 0, 0.35, 20, 1, 0.2).build(fx, "mouth", cor)
    fx.track(box, lambda t, i: dict(y=-0.25, sx=[0.2, 0.7, 1.0, 0.9, 0.6, 0.3][i] + 0.001, sy=[0.1, 0.3, 0.4, 0.4, 0.3, 0.2][i] + 0.001, op=[0.6, 1, 1, 0.8, 0.5, 0.2][i]))
    for j in range(7):
        x0 = rng.uniform(-0.45, 0.45)
        y0 = -0.2 + rng.uniform(0, 0.1)
        particle(fx, "sp%d" % j, cor, "star" if j % 2 else "diamond", 0.1, flight(x0 * 0.3, y0, x0 * 1.0, rng.uniform(0.7, 1.15), 0.15 + 0.08 * j * 0.5, 0.7, -0.5, 1.0, 0))
    return fx


@reg("capture_seal")
def capture_seal():
    fx = Fx("capture_seal", frames=8, fps=12, halo=0.9, name_vi="An phong linh thu", where="talisman ring closes around a spirit beast, then flashes")
    rng = fx.rng
    rd = fx.mat("red", "#ff5a3c")
    gd = fx.mat("gold", "#ffd060")
    cor = fx.mat("core", "#fff6d6")
    gl = fx.mat("glow", "#ffcf60", grad=dict(src="radial", pow=1.4))
    # six talisman tags (paper strips with stroke marks) closing from radius 1.0 to 0.52
    RAD = [0.84, 0.78, 0.7, 0.62, 0.55, 0.5, 0.5, 0.5]
    for j in range(6):
        a = TAU * j / 6 + PI / 6

        def tag():
            mb = MB().poly([(-0.1, -0.2), (0.1, -0.2), (0.1, 0.2), (0.0, 0.26), (-0.1, 0.2)])
            return mb
        paper = tag().build(fx, "tag%d" % j, rd)
        fx.track(paper, lambda t, i, a=a: dict(x=math.cos(a) * RAD[i] * 0.95, y=math.sin(a) * RAD[i] * 0.95, rot=a - PI / 2, s=[0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.15, 0.0][i] + 0.001,
                                                  op=[0.5, 0.8, 1, 1, 1, 1, 1, 0][i]))
        st = MB()
        for q in range(3):
            st.line((-0.05, -0.12 + 0.1 * q), (0.05, -0.12 + 0.1 * q + (0.03 if q % 2 else -0.02)), 0.025)
        ink = st.build(fx, "ink%d" % j, gd)
        fx.track(ink, lambda t, i, a=a: dict(x=math.cos(a) * RAD[i] * 0.95, y=math.sin(a) * RAD[i] * 0.95, rot=a - PI / 2, s=[0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.15, 0.0][i] + 0.001))
    # ring drawn in as the tags close (arc sweep), complete at frame 5
    arcs = fx.per_frame("ring", gd, lambda t, i: MB().ring(0, 0, 0.5, 0.07, 0, max(0.01, min(1.0, i / 5.0)) * TAU - 0.001, seg=40))
    for i, ob in enumerate(arcs):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and 1 <= i <= 6)))
    r2 = fx.per_frame("ring2", cor, lambda t, i: MB().ring(0, 0, 0.5, 0.025, seg=40))
    for i, ob in enumerate(r2):
        fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and 4 <= i <= 6)))
    rn = runes(MB(), 0, 0, 0.7, 12, 0.11, rng, 0.02)
    ob = rn.build(fx, "runes", gd)
    fx.track(ob, lambda t, i: dict(rot=-0.5 * t, s=[1.3, 1.1, 1.0, 0.95, 0.9, 0.85, 0.85, 0.0][i] + 0.001, op=[0.2, 0.6, 0.9, 1, 1, 1, 1, 0][i]))
    fl = MB().disc(0, 0, 1.0, 30, 1, 0).build(fx, "flash", gl)
    fx.track(fl, lambda t, i: dict(s=[0.01, 0.01, 0.01, 0.01, 0.01, 0.4, 0.75, 0.01][i], op=[0, 0, 0, 0, 0, 0.5, 0.6, 0.12][i]))
    wh = MB().disc(0, 0, 0.5, 24, 1, 0.6).build(fx, "white", cor)
    fx.track(wh, lambda t, i: dict(s=[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.6, 0.01][i], op=[0, 0, 0, 0, 0, 0, 0.9, 0.15][i]))
    for j in range(8):
        a = TAU * j / 8 + 0.2
        particle(fx, "sp%d" % j, cor, "star" if j % 2 else "diamond", 0.1, flight(0, 0, math.cos(a) * 0.8, math.sin(a) * 0.8 + 0.2, 0.6, 0.5, 0, 1.0, 0))
    return fx


@reg("sword_trail")
def sword_trail():
    fx = Fx("sword_trail", frames=4, fps=14, loop=True, halo=0.8, name_vi="Vet kiem bay", where="light streak behind a flying sword (streak trails to the left)")
    gl = fx.mat("glow", "#6ad4ff", grad=dict(src="attr", pow=1.2))
    cor = fx.mat("core", "#f4feff")
    bl = fx.mat("blue", "#52c0ff", grad=dict(src="attr", pow=0.5), core="#ffffff")

    def streak(y, L, w, ph, wob):
        def f(t, i):
            pts = [(0.45 - L * k / 12, y + wob * math.sin(TAU * (t + ph) + k * 0.7) * (k / 12)) for k in range(13)]
            ws = [w * (1 - k / 12) ** 0.9 + 0.004 for k in range(13)]
            return MB().strip(pts, ws, soft=True)
        return f
    for nm, y, L, w, ph, fm in (("a", 0.0, 1.5, 0.3, 0.0, gl), ("b", 0.0, 1.3, 0.16, 0.25, bl), ("c", 0.0, 1.1, 0.07, 0.5, cor),
                                ("d", 0.17, 0.9, 0.06, 0.1, bl), ("e", -0.17, 0.95, 0.06, 0.6, bl)):
        fx.per_frame(nm, fm, streak(y, L, w, ph, 0.03))
    for j in range(4):
        particle(fx, "m%d" % j, cor, "star", 0.07, (lambda j: lambda t: (0.1 - ((t + j / 4.0) % 1) * 1.3, 0.2 * math.sin(j * 2.4), (1 - (t + j / 4.0) % 1) ** 0.7 + 0.001, 0))(j))
    return fx


def all_ids():
    ids = []
    for el in ELEM:
        ids += ["slash_" + el, "bolt_" + el, "burst_" + el]
    ids += list(REG)
    return ids


def make(id):
    if id.startswith("slash_"):
        return make_slash(id[6:])
    if id.startswith("bolt_"):
        return make_bolt(id[5:])
    if id.startswith("burst_"):
        return make_burst(id[6:])
    return REG[id]()
