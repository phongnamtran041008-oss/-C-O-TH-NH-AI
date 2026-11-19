"""Realm auras for the v2 characters (96x96 frames, 48 px per metre, camera 15 deg above the horizon).

Every aura is TWO sheets, 128x128, pivot (64,104) = the character's feet, 8 frames, 10 fps, loop:
  aura_<realm>_back   drawn behind the character
  aura_<realm>_front  drawn in front: only a few light elements (motes, a thin ribbon crossing the
                      legs, low flames at the front of a ground ring) - never over the face or torso.
Orbiting things (ribbons, shards, puffs, flame rings) are split by depth: the half that passes
behind the body goes to `back`, the half in front to `front`, so they wrap the character.
Units: metres.  Frame centre = (0,0); the feet are at y = FY.
"""
import math
from fxlib import *
from fx_realm import mote, star4

PPU = 48.0
FY = -40 / PPU                    # feet (pivot 64,104 -> 40 px below the frame centre)
HEAD = FY + 51 / PPU              # top of the topknot
BC = FY + 0.52                    # body centre
KY = math.sin(math.radians(15))   # ground circles are squashed to this by the 15 degree camera
SH = BC + 0.30                    # shoulder height (wing roots)
REG = {}
REALMS = ["luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua"]
VI = {"luyen_khi": "Luyen Khi", "truc_co": "Truc Co", "ket_dan": "Ket Dan", "nguyen_anh": "Nguyen Anh",
      "hoa_than": "Hoa Than", "luyen_hu": "Luyen Hu", "hop_the": "Hop The", "dai_thua": "Dai Thua"}


def new(realm, layer, idea):
    fx = Fx("aura_%s_%s" % (realm, layer), view="front", frames=8, fps=10, loop=True, px=128, pivot=(64, 104), ppu=PPU,
            zoom=1.05, halo=0.0, mode="alpha", alpha_levels=5, name_vi="Hao quang %s (%s)" % (VI[realm], "sau" if layer == "back" else "truoc"),
            where="%s aura, drawn %s the character: %s" % (VI[realm], "behind" if layer == "back" else "in front of", idea))
    fx.extra = {"layer": layer, "ppu": 48,
                "draw": "normal alpha blit (straight alpha, NOT additive): palette colours keep their hue on any ground; "
                        + ("draw before (behind) the character" if layer == "back" else "draw after (in front of) the character")}
    fx.layer = layer
    return fx


def is_back(fx):
    return fx.layer == "back"


# ---------------------------------------------------------------- orbit helpers
def orbit(t, cx, yc, rx, ky, tilt, span, dirn, ph, n=30, rise=0.0, ry_extra=0.0):
    pts, dep = [], []
    for k in range(n + 1):
        s = k / n
        ang = ph + dirn * TAU * t + s * span
        d = math.sin(ang)
        pts.append((cx + rx * math.cos(ang), yc + ky * rx * d + tilt * math.cos(ang) + rise * (s - 0.5)))
        dep.append(d)
    return pts, dep


def ribbon_mesh(fx, t, widths_fn, **kw):
    """the part of an orbiting ribbon that belongs to this layer."""
    pts, dep = orbit(t, **kw)
    n = len(pts)
    mb = MB()
    cur = []
    for k in range(n):
        ok = (dep[k] >= 0) == is_back(fx)
        w = widths_fn(k / (n - 1))
        if not is_back(fx):                     # in front only the sides: fade out before the torso / face
            ax = abs(pts[k][0])
            f = sat((ax - 0.2) / 0.16)
            ok = ok and f > 0.05
            w *= f
        if ok:
            cur.append((pts[k], w))
        else:
            if len(cur) > 1:
                mb.strip([p for p, _ in cur], [w for _, w in cur], soft=True)
            cur = []
    if len(cur) > 1:
        mb.strip([p for p, _ in cur], [w for _, w in cur], soft=True)
    return mb


def taper(w, power=0.7):
    return lambda s: w * math.sin(PI * s) ** power + 0.004


def ribbon(fx, name, glow, core, wglow, wcore, **kw):
    fx.per_frame(name + "g", glow, lambda t, i: ribbon_mesh(fx, t, taper(wglow), **kw))
    if core is not None:
        fx.per_frame(name + "c", core, lambda t, i: ribbon_mesh(fx, t, taper(wcore), **kw))


def depth_objects(fx, name, fm, mbfn, n, cx, cy, rx, ky, speed, dirn=1.0, size=1.0, bob=0.0):
    """n identical small objects on an orbit; each is shown in `back` or `front` depending on where it is."""
    for j in range(n):
        a0 = TAU * j / n
        ob = mbfn(j).build(fx, "%s%d" % (name, j), fm)

        def f(t, i, a0=a0, j=j):
            ang = a0 + dirn * TAU * t * speed
            d = math.sin(ang)
            return dict(x=cx + rx * math.cos(ang), y=cy + ky * rx * d + bob * math.sin(TAU * t + j), s=size * (0.85 + 0.15 * d),
                        rot=ang, show=((d >= 0) == is_back(fx)))
        fx.track(ob, f)


def glow_disc(fx, name, fm, x, y, r, sx=1.0, sy=1.0, pulse=0.0, ph=0.0, op=1.0):
    ob = MB().disc(0, 0, r, 28, 1, 0).build(fx, name, fm)
    fx.track(ob, lambda t, i: dict(x=x, y=y, sx=sx, sy=sy, op=op * (1 + pulse * math.sin(TAU * t + ph))))
    return ob


def wing_glows(fx, base, core, r=0.5, op=0.3, cop=0.4):
    r = r * 0.7; op = op * 0.75
    """warm light behind the wings (back layer only)."""
    gm = fx.mat("wg", base, grad=dict(src="radial", pow=1.5), opacity=op)
    cm = fx.mat("wgc", core, grad=dict(src="radial", pow=1.6), opacity=cop)
    for sgn in (-1, 1):
        glow_disc(fx, "wing%+d" % sgn, gm, sgn * 0.46, SH + 0.04, r, sx=0.8, sy=1.25, pulse=0.12, ph=sgn)
        glow_disc(fx, "wingc%+d" % sgn, cm, sgn * 0.42, SH + 0.02, r * 0.45, pulse=0.15, ph=sgn * 2)


def rising(fx, name, fm, n, x_lo, x_hi, y0, y1, size, shape="disc", sway=0.05, ph0=0.0, seed=0):
    rng = random.Random(seed + 7)
    for j in range(n):
        x0 = rng.uniform(x_lo, x_hi)
        sw = rng.uniform(0.5, 1.0) * sway
        ph = (j + ph0) / n
        mote(fx, "%s%d" % (name, j), fm, size, (lambda x0, sw, ph, j: lambda t: (
            x0 + sw * math.sin(TAU * (t + ph) + j), y0 + (y1 - y0) * ((t + ph) % 1), math.sin(PI * ((t + ph) % 1)) ** 0.7 + 0.001))(x0, sw, ph, j), shape)


def flame_mesh(mb, x, y, h, w, t, k, rot=0.0, sway=0.07, flick=0.16, varied=False):
    ph = TAU * (t + (((k * 0.37) % 1.0) if varied else (k % 3) / 3.0))
    f = MB().flame(0, 0, h * (1 + flick * math.sin(ph)), w, sway=sway * math.sin(ph + 1.0), lean=0.04 * math.cos(ph))
    mb.merge(f, x, y, 1.0, rot)


def ring_pts_mesh(mb, cx, cy, r, w, rot=0.0, soft=False, seg=48, a0=0.0, a1=TAU):
    mb.ring(0, 0, r, w, a0, a1, seg=seg, soft=soft)


def strokes_ring(fx_rng, r, n, size, w):
    mb = MB()
    runes(mb, 0, 0, r, n, size, fx_rng, w)
    return mb


# ================================================================ the eight realms
def make_luyen_khi(layer):
    fx = new("luyen_khi", layer, "a few faint grey-white breath wisps rising from the ground")
    wm = fx.mat("wisp", "#cfd8e6", grad=dict(src="attr", pow=1.0), opacity=0.85)
    wm2 = fx.mat("wisp2", "#ffffff", grad=dict(src="attr", pow=1.6), opacity=0.55)
    if is_back(fx):
        xs = [-0.26, -0.07, 0.13, 0.3]

        def b(wmul):
            def f(t, i):
                mb = MB()
                for k, x0 in enumerate(xs):
                    ph = (t + k / 4.0) % 1.0
                    env = math.sin(PI * ph) ** 1.6
                    y0 = FY + 0.02 + ph * 0.3
                    pts = [(x0 + 0.015 * math.sin(TAU * (ph * 1.1 + k * 0.23) + s * 3.2) * (0.3 + s), y0 + s * 0.12) for s in [j / 8 for j in range(9)]]
                    mb.strip(pts, [wmul * (0.01 + 0.035 * env) * (1 - abs(j / 8 - 0.5) * 1.1) for j in range(9)], soft=True)
                return mb
            return f
        fx.per_frame("w", wm, b(2.2))
        fx.per_frame("w2", wm2, b(0.8))
    else:
        for j in range(3):
            mote(fx, "m%d" % j, wm2, 0.018, (lambda j: lambda t: (-0.22 + 0.22 * j, FY + 0.05 + 0.55 * ((t + j / 3.0) % 1), math.sin(PI * ((t + j / 3.0) % 1)) + 0.001))(j))
    return fx


def make_truc_co(layer):
    fx = new("truc_co", layer, "two thin blue-white qi ribbons orbit the body like flowing water; soft mist ring at the feet")
    glow = fx.mat("rg", "#3a80ff", grad=dict(src="attr", pow=1.0), opacity=0.8)
    core = fx.mat("rc", "#d8f0ff", grad=dict(src="attr", pow=0.6), opacity=1.0)
    puff = fx.mat("puff", "#6aa0ff", grad=dict(src="radial", pow=1.6), opacity=0.3)
    wh = fx.mat("wh", "#e8f6ff")
    ribbon(fx, "r1", glow, core, 0.2, 0.05, cx=0, yc=BC + 0.12, rx=0.56, ky=KY, tilt=0.13, span=1.5 * PI, dirn=1, ph=0.0, rise=0.15)
    ribbon(fx, "r2", glow, core, 0.17, 0.04, cx=0, yc=BC - 0.06, rx=0.62, ky=KY, tilt=-0.15, span=1.4 * PI, dirn=1, ph=PI, rise=-0.12)
    fog = fx.mat("fog", "#a8ccff", grad=dict(src="attr", pow=1.3), opacity=0.6)
    FOG = [(0.03, 0.95, -0.05, 1, 0.09), (0.10, 0.7, 0.22, 2, 0.07), (0.06, 1.05, 0.08, 1, 0.08), (0.15, 0.62, -0.22, 2, 0.06), (0.02, 0.8, 0.18, 2, 0.07)]

    def fogmesh(t, i):
        mb = MB()
        for k, (yy, L, x0, sp, w) in enumerate(FOG):
            if (k % 2 == 0) != is_back(fx):
                continue
            cx = x0 + 0.12 * math.sin(TAU * t * sp + k)
            pts = [(cx + L * (j / 10 - 0.5), FY + yy + 0.012 * math.sin(TAU * (t * sp + j / 10) + k)) for j in range(11)]
            mb.strip(pts, [w * math.sin(PI * j / 10) ** 0.8 + 0.004 for j in range(11)], soft=True)
        return mb
    fx.per_frame("fog", fog, fogmesh)
    if is_back(fx):
        rising(fx, "wisp", wh, 3, -0.4, 0.4, FY + 0.05, FY + 0.7, 0.018, "diamond", seed=3)
    else:
        rising(fx, "wf", wh, 2, -0.3, 0.3, FY + 0.1, FY + 0.6, 0.016, "disc", seed=5)
    return fx


def make_ket_dan(layer):
    fx = new("ket_dan", layer, "green spirit ribbons spiral upward with golden motes, golden core glow at the belly")
    glow = fx.mat("gg", "#28c060", grad=dict(src="attr", pow=1.0), opacity=0.85)
    core = fx.mat("gc", "#a8f4a8", grad=dict(src="attr", pow=0.6), opacity=1.0)
    gold = fx.mat("gold", "#ffd860")
    gglow = fx.mat("gglow", "#ffb830", grad=dict(src="radial", pow=1.6), opacity=0.7)
    for k, ph in enumerate((0.0, PI)):
        ribbon(fx, "h%d" % k, glow, core, 0.2, 0.05, cx=0, yc=BC + 0.05, rx=0.52, ky=KY * 1.3, tilt=0.0, span=1.5 * PI, dirn=1, ph=ph, rise=0.85, n=36)
    if is_back(fx):
        rising(fx, "gm", gold, 9, -0.5, 0.5, FY + 0.05, HEAD + 0.15, 0.025, "star", sway=0.08, seed=11)
        glow_disc(fx, "belly_b", gglow, 0, FY + 0.45, 0.24, pulse=0.15, op=0.3)
    else:
        rising(fx, "gm", gold, 4, -0.5, 0.5, FY + 0.1, HEAD, 0.022, "diamond", sway=0.08, seed=13)
        py = FY + 0.45
        halo = fx.mat("pearl_halo", "#ffc040", grad=dict(src="radial", pow=1.2), opacity=0.75)
        glow_disc(fx, "belly_halo", halo, 0, py, 0.2, pulse=0.15, op=1.0)
        pm = fx.mat("pearl", "#ffe27a", grad=dict(src="radial", pow=0.5, cpow=2.0), core="#fffbe4", opacity=1.0)
        pe = fx.mat("pearl_rim", "#e8b02a", opacity=1.0)
        ob = MB().disc(0, 0, 0.085, 18).build(fx, "pearl_rim", pe)
        fx.track(ob, lambda t, i: dict(x=0, y=py, s=1.0 + 0.08 * math.sin(TAU * t)))
        ob = MB().disc(0, 0, 0.065, 18, 1, 0.6).build(fx, "pearl", pm)
        fx.track(ob, lambda t, i: dict(x=0, y=py, s=1.0 + 0.08 * math.sin(TAU * t)))
        wm = fx.mat("pearl_hl", "#ffffff", opacity=1.0)
        ob = MB().disc(0, 0, 0.022, 8).build(fx, "pearl_hl", wm)
        fx.track(ob, lambda t, i: dict(x=-0.02, y=py + 0.025))
        rays = fx.mat("pearl_ray", "#fff0a0", opacity=1.0)
        for j in range(5):
            ob = MB().diamond(0, 0, 0.2, 0.034, 0).build(fx, "pray%d" % j, rays)
            a0 = TAU * j / 5 + PI / 2
            fx.track(ob, lambda t, i, a0=a0, j=j: dict(x=math.cos(a0 + TAU * t / 5) * 0.16, y=py + math.sin(a0 + TAU * t / 5) * 0.16, rot=a0 + TAU * t / 5,
                                                         s=0.75 + 0.35 * (0.5 + 0.5 * math.sin(TAU * t * 2 + j * 1.3))))
    return fx


def flame_set(fx, name, mats, positions, t, scale=1.0, wscale=1.0, flick=0.16, varied=False):
    """one mesh with many flames; positions = (x, y, h, w, rot)."""
    mb = MB()
    for k, (x, y, h, w, rot) in enumerate(positions):
        flame_mesh(mb, x, y, h * scale, w * wscale, t, k, rot, flick=flick, varied=varied)
    return mb


def body_flame_positions(n, rx, ry, cy, h, w, lo=-0.55):
    out = []
    for k in range(n):
        a = TAU * k / n
        if math.sin(a) < lo:
            continue
        x, y = rx * math.cos(a), cy + ry * math.sin(a)
        nx, ny = math.cos(a) / rx, math.sin(a) / ry
        na = math.atan2(ny, nx)
        tilt = (na - PI / 2) * 0.35
        out.append((x, y, h * (0.75 + 0.25 * abs(math.sin(a))), w, tilt))
    return out


def make_nguyen_anh(layer):
    fx = new("nguyen_anh", layer, "teal-gold energy rising like a flame outline around the body (dense behind, open in front), gold sparks")
    g = dict(src="attr", pow=0.6)
    deep = fx.mat("t0", "#0e5a78", grad=g, opacity=0.9)
    body = fx.mat("t1", "#18a0c8", grad=g, opacity=0.95)
    mid = fx.mat("t2", "#5ae0f4", grad=g, opacity=0.95)
    core = fx.mat("t3", "#fff2b0", grad=g, opacity=0.95)
    spark = fx.mat("sp", "#ffe890")
    if is_back(fx):
        rx, ry, cy = 0.46, 0.62, BC + 0.02
        pos = []

        def at(deg, h, w):
            a = math.radians(deg)
            x, y = rx * math.cos(a), cy + ry * math.sin(a)
            na = math.atan2(math.sin(a) / ry, math.cos(a) / rx)
            pos.append((x, y, h, w, (na - PI / 2) * 0.35))
        for deg in range(25, 160, 13):                 # dense, tall arc behind the head and shoulders
            at(deg, 0.58 - 0.12 * abs(deg - 90) / 65, 0.24)
        for deg in (6, 174, -14, 194):                 # sides, medium
            at(deg, 0.36, 0.2)
        for deg in (-38, 218):                         # a couple of low licks, the front stays open
            at(deg, 0.24, 0.16)
        for x0, h in ((-0.26, 0.66), (-0.1, 0.78), (0.1, 0.78), (0.26, 0.66)):     # second row right behind the shoulders
            pos.append((x0, SH + 0.02, h, 0.22, 0.0))
        for nm, fm, sc, ws in (("0", deep, 1.0, 1.15), ("1", body, 0.88, 1.0), ("2", mid, 0.64, 0.7), ("3", core, 0.4, 0.4)):
            fx.per_frame("fl" + nm, fm, lambda t, i, sc=sc, ws=ws: flame_set(fx, "", None, pos, t, sc, ws, flick=0.3, varied=True))
        rising(fx, "sp", spark, 10, -0.5, 0.5, FY + 0.1, HEAD + 0.3, 0.022, "diamond", sway=0.07, seed=21)
    else:
        rising(fx, "sp", spark, 5, -0.45, 0.45, FY + 0.15, HEAD + 0.1, 0.02, "diamond", sway=0.07, seed=22)
    return fx


def make_hoa_than(layer):
    fx = new("hoa_than", layer, "soft see-through violet light column with drifting runes of light and a faint larger halo ring")
    edge = fx.mat("edge", "#8a50ff", grad=dict(src="attr", pow=1.7), opacity=0.55, ufade=1.0)
    edge2 = fx.mat("edge2", "#c8a8ff", grad=dict(src="attr", pow=2.0), opacity=0.6, ufade=1.0)
    ring = fx.mat("ring", "#8a50ff", grad=dict(src="attr", pow=1.2), opacity=0.5)
    ringc = fx.mat("ringc", "#c0a0ff", opacity=0.7)
    rune_m = fx.mat("rune", "#e6d0ff")
    spk = fx.mat("spk", "#f4eaff")
    rng = fx.rng
    y0, y1 = FY - 0.02, 1.2
    n = 10
    if is_back(fx):
        col = MB().strip([(0, y0 + (y1 - y0) * k / n) for k in range(n + 1)], 1.15, soft=True)
        ob = col.build(fx, "col", edge)
        fx.track(ob, lambda t, i: dict(op=0.8 + 0.2 * math.sin(TAU * t)))
        ob = MB().strip([(0, y0 + (y1 - y0) * k / n) for k in range(n + 1)], 0.35, soft=True).build(fx, "colc", edge2)
        fx.track(ob, lambda t, i: dict(op=0.9))
        for rr, op in ((0.9, 1.0), (1.08, 0.5)):
            MB().ring(0, FY + 0.02, rr, 0.12, soft=True, ky=KY, seg=64).build(fx, "gs%d" % int(rr * 10), ring)
            MB().ring(0, FY + 0.02, rr, 0.014, ky=KY, seg=64).build(fx, "gc%d" % int(rr * 10), ringc)
        for j in range(5):
            xx = rng.uniform(-0.55, 0.55)
            r = runes(MB(), 0, 0, 0, 1, 0.17, random.Random(70 + j), 0.012, tangent=False, strokes=(3, 4))
            ob = r.build(fx, "rune%d" % j, rune_m)
            ph = j / 5.0
            fx.track(ob, lambda t, i, xx=xx, ph=ph: dict(x=xx + 0.04 * math.sin(TAU * (t + ph)), y=FY + 0.1 + 1.15 * ((t + ph) % 1),
                                                           s=math.sin(PI * ((t + ph) % 1)) ** 0.8 + 0.001))
        rising(fx, "r", spk, 8, -0.5, 0.5, FY + 0.05, 1.1, 0.02, "diamond", sway=0.06, seed=31)
    else:
        for j in range(2):
            r = runes(MB(), 0, 0, 0, 1, 0.14, random.Random(90 + j), 0.012, tangent=False, strokes=(3, 4))
            ob = r.build(fx, "rune%d" % j, rune_m)
            fx.track(ob, lambda t, i, j=j: dict(x=(-0.5 if j == 0 else 0.5) + 0.03 * math.sin(TAU * t + j), y=FY + 0.1 + 0.9 * ((t + j * 0.5) % 1),
                                                s=math.sin(PI * ((t + j * 0.5) % 1)) ** 0.8 + 0.001))
        rising(fx, "r", spk, 4, -0.55, 0.55, FY + 0.1, 0.9, 0.018, "star", sway=0.05, seed=33)
    return fx


def make_luyen_hu(layer):
    fx = new("luyen_hu", layer, "ring of fire on the ground, flames behind the shoulders and a warm glow behind the wings, embers")
    red = fx.mat("f1", "#d82010", grad=dict(src="attr", pow=0.7), opacity=0.8)
    org = fx.mat("f2", "#ff7a1c", grad=dict(src="attr", pow=0.8), opacity=0.8)
    gld = fx.mat("f3", "#ffd860", grad=dict(src="attr", pow=0.8), opacity=0.8)
    ember = fx.mat("em", "#ffb040")
    rx = 0.8
    N = 16
    pos = []
    for k in range(N):
        a = TAU * (k + 0.5) / N
        d = math.sin(a)
        if (d >= 0) == is_back(fx):
            pos.append((rx * math.cos(a), FY + 0.01 + KY * rx * d, 0.34 if d >= 0 else 0.22, 0.24, 0.0))
    fx.per_frame("rf1", red, lambda t, i: flame_set(fx, "", None, pos, t, 1.0))
    fx.per_frame("rf2", org, lambda t, i: flame_set(fx, "", None, pos, t, 0.68))
    fx.per_frame("rf3", gld, lambda t, i: flame_set(fx, "", None, pos, t, 0.38))
    if is_back(fx):
        sp = [(-0.3, SH - 0.02, 0.42, 0.2, 0.3), (-0.12, SH + 0.1, 0.5, 0.2, 0.08), (0.12, SH + 0.1, 0.5, 0.2, -0.08), (0.3, SH - 0.02, 0.42, 0.2, -0.3)]
        fx.per_frame("sh1", red, lambda t, i: flame_set(fx, "", None, sp, t, 1.0))
        fx.per_frame("sh2", org, lambda t, i: flame_set(fx, "", None, sp, t, 0.68))
        fx.per_frame("sh3", gld, lambda t, i: flame_set(fx, "", None, sp, t, 0.38))
        rising(fx, "e", ember, 12, -0.7, 0.7, FY + 0.05, HEAD + 0.3, 0.022, "diamond", sway=0.09, seed=41)
    else:
        rising(fx, "e", ember, 5, -0.6, 0.6, FY + 0.05, HEAD, 0.02, "diamond", sway=0.09, seed=43)
    return fx


def make_hop_the(layer):
    fx = new("hop_the", layer, "pale blue frost sphere (rim only), orbiting ice shards, snow motes and a cold glow behind the ice wings")
    rim = fx.mat("rim", "#9adcff", grad=dict(src="rim", pow=10.0, cpow=6.0), core="#f2fdff", opacity=0.95)
    body = fx.mat("body", "#5ab4ff", grad=dict(src="rim", pow=5.0), opacity=0.05)
    shard = fx.mat("shard", "#7ac8ff")
    shardh = fx.mat("shardh", "#f2fdff")
    snow = fx.mat("snow", "#e8f6ff")
    frost = fx.mat("frost", "#78b8ff", grad=dict(src="attr", pow=1.2), opacity=0.5)
    if is_back(fx):
        ob = MB().disc(0, 0, 0.8, 44).build(fx, "sphere", rim)
        fx.track(ob, lambda t, i: dict(y=BC + 0.1, s=1.0 + 0.015 * math.sin(TAU * t), op=1.0))
        for nm, (a0, a1, w) in {"h1": (105, 160, 0.05), "h2": (172, 186, 0.035), "h3": (-40, -15, 0.03)}.items():
            ob = MB().ring(0, 0, 0.7, w, math.radians(a0), math.radians(a1)).build(fx, nm, shardh)
            fx.track(ob, lambda t, i: dict(y=BC + 0.1, s=1.0 + 0.015 * math.sin(TAU * t), op=0.7 + 0.3 * math.sin(TAU * t)))
        MB().ring(0, FY + 0.02, 0.66, 0.14, soft=True, ky=KY).build(fx, "frost", frost)
        rising(fx, "sn", snow, 12, -0.7, 0.7, HEAD + 0.5, FY + 0.05, 0.016, "disc", sway=0.08, seed=51)
    else:
        rising(fx, "sn", snow, 5, -0.6, 0.6, HEAD + 0.3, FY + 0.1, 0.014, "disc", sway=0.08, seed=53)
    for k in range(2):
        depth_objects(fx, "sh%d" % k, shard, lambda j: MB().diamond(0, 0, 0.17, 0.065, 0).diamond(0, 0, 0.09, 0.03, 0), 5, 0, BC + (0.18 if k == 0 else -0.12), 0.7 + 0.08 * k, KY * 1.6,
                      speed=1.0 if k == 0 else -1.0, size=1.0)
    return fx


def magic_circle(t, rx_sq=KY):
    """golden magic circle on the ground: abstract geometry only (rings, two triangles, rune marks)."""
    rng = random.Random(5)
    mb = MB()
    mb.ring(0, 0, 0.96, 0.03, seg=64)
    mb.ring(0, 0, 0.82, 0.02, seg=64)
    mb.ring(0, 0, 0.36, 0.025, seg=48)
    for off in (PI / 2, -PI / 2):
        pts = [(0.82 * math.cos(off + TAU * k / 3), 0.82 * math.sin(off + TAU * k / 3)) for k in range(3)]
        for k in range(3):
            mb.line(pts[k], pts[(k + 1) % 3], 0.025)
    runes(mb, 0, 0, 0.89, 12, 0.1, rng, 0.016)
    for k in range(6):
        a = TAU * k / 6
        mb.disc(0.82 * math.cos(a), 0.82 * math.sin(a), 0.04, 8)
    return mb.xform(rot=TAU * t / 6, sy=rx_sq, dy=FY + 0.02)


def make_dai_thua(layer):
    fx = new("dai_thua", layer, "slowly turning galaxy swirl, golden magic circle on the ground, star motes, gold-violet glow behind the wings")
    rng = fx.rng
    gold = fx.mat("gold", "#ffc84a")
    goldg = fx.mat("goldg", "#ffb020", grad=dict(src="attr", pow=1.0), opacity=0.5)
    star_a = fx.mat("sa", "#fff4d0")
    star_b = fx.mat("sb", "#d0c8ff")
    if is_back(fx):
        # galaxy swirl behind the body
        cols = ["#7a3cf0", "#c040d8", "#4a60e8", "#a050ff"]
        for k in range(4):
            m = fx.mat("neb%d" % k, cols[k], grad=dict(src="radial", pow=1.8), opacity=0.17)
            for side in (0, 1):
                a0 = TAU * k / 8 + side * PI
                ob = MB().disc(0, 0, 0.3, 22, 1, 0).build(fx, "neb%d_%d" % (k, side), m)
                fx.track(ob, lambda t, i, a0=a0, k=k: dict(x=0.5 * math.cos(a0 + PI * t) * (1 if k % 2 == 0 else 0.75), y=BC + 0.12 + 0.5 * math.sin(a0 + PI * t) * (1 if k % 2 == 0 else 0.75), s=1.0))

        def arm(a0, wm):
            pts, ws = [], []
            for k in range(28):
                u = k / 27
                r = 0.1 + 0.88 * u
                a = a0 + 3.0 * u
                pts.append((r * math.cos(a), r * math.sin(a)))
                ws.append(wm * (0.04 + 0.15 * math.sin(PI * u) ** 0.8))
            return MB().strip(pts, ws, soft=True)
        pur = fx.mat("armp", "#9050ff", grad=dict(src="attr", pow=1.2), opacity=0.35)
        gl = fx.mat("armg", "#ffc84a", grad=dict(src="attr", pow=1.0), opacity=0.55)
        for k in range(2):
            for nm, wm, fm in (("p", 1.7, pur), ("g", 0.7, gl)):
                ob = arm(PI * k, wm).build(fx, "arm%s%d" % (nm, k), fm)
                fx.track(ob, lambda t, i: dict(y=BC + 0.12, rot=-PI * t))
        cm = fx.mat("core", "#ffc040", grad=dict(src="radial", pow=1.2, cpow=4.0), core="#fffbe0", opacity=0.8)
        glow_disc(fx, "core", cm, 0, BC + 0.12, 0.2, pulse=0.1)
        # golden magic circle on the ground
        fx.per_frame("mc_g", goldg, lambda t, i: magic_circle(t).merge(MB(), 0, 0))
        fx.per_frame("mc", gold, lambda t, i: magic_circle(t))
        for j in range(20):
            r = 0.3 + 0.95 * math.sqrt(rng.random())
            a = rng.uniform(0, TAU)
            ph = rng.random()
            mb = MB().star(0, 0, 4, 0.06 if j % 5 else 0.09, 0.015, PI / 2)
            ob = mb.build(fx, "st%d" % j, star_a if j % 2 else star_b)
            fx.track(ob, lambda t, i, r=r, a=a, ph=ph: dict(x=r * math.cos(a) * 0.9, y=BC + 0.15 + r * math.sin(a) * 0.95, s=0.15 + 0.85 * (0.5 + 0.5 * math.sin(TAU * (t + ph))) ** 1.5 + 0.001))
    else:
        ribbon(fx, "gr", goldg, gold, 0.09, 0.022, cx=0, yc=FY + 0.32, rx=0.55, ky=KY, tilt=0.06, span=1.3 * PI, dirn=1, ph=0.5, rise=0.12)
        for j in range(5):
            r = 0.5 + 0.3 * rng.random()
            a = rng.uniform(0, TAU)
            ph = rng.random()
            ob = MB().star(0, 0, 4, 0.07, 0.015, PI / 2).build(fx, "fs%d" % j, star_a)
            fx.track(ob, lambda t, i, r=r, a=a, ph=ph: dict(x=r * math.cos(a), y=BC - 0.1 + 0.8 * math.sin(a) * 0.7, s=0.15 + 0.85 * (0.5 + 0.5 * math.sin(TAU * (t + ph))) ** 1.5 + 0.001))
    return fx


BUILD = dict(luyen_khi=make_luyen_khi, truc_co=make_truc_co, ket_dan=make_ket_dan, nguyen_anh=make_nguyen_anh,
             hoa_than=make_hoa_than, luyen_hu=make_luyen_hu, hop_the=make_hop_the, dai_thua=make_dai_thua)


def all_ids():
    return ["aura_%s_%s" % (r, l) for r in REALMS for l in ("back", "front")]


def make(id):
    _, rest = id.split("aura_", 1)
    realm, layer = rest.rsplit("_", 1)
    return BUILD[realm](layer)
