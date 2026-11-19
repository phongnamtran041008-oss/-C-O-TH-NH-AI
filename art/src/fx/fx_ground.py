"""Ground FX, 96x96.
 tran_1..8  formation circles (ground camera, 35 deg above the horizon -> ellipses)
 warn_*     hit-zone telegraphs (top view, the sheet is stretched by the game to the real size)
 crack_ground  slam mark (ground camera, alpha)"""
import math
from fxlib import *

REG = {}


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


R0 = 1.42          # outer radius that fits the 96 px frame with margin (units: 32 px)


def gfx(id, m, name_vi, where, **kw):
    kw.setdefault("halo", 0.9)
    fx = Fx(id, view="ground", frames=8, fps=6, loop=True, px=96, ground=True, name_vi=name_vi, where=where, **kw)
    fx.sym = m
    return fx


def spin(fx, ob, extra=None, pulse=0.0, base=0.0, rev=1.0):
    """slow rotation by one symmetry step per loop (clean loop) + optional glow pulse."""
    def f(t, i):
        d = dict(rot=base + rev * TAU * t / fx.sym)
        if pulse:
            d["op"] = 0.85 + pulse * math.sin(TAU * t)
        if extra:
            d.update(extra(t, i))
        return d
    return fx.track(ob, f)


def two(fx, name, mb, body, core, pulse=0.12, rev=1.0, soft_mb=None):
    """glow layer + crisp layer from the same mesh."""
    gl = fx.mat(name + "g", body, grad=dict(src="attr", pow=1.0), opacity=0.7)
    cr = fx.mat(name + "c", core)
    if soft_mb is not None:
        spin(fx, soft_mb.build(fx, name + "_g", gl), pulse=pulse, rev=rev)
    spin(fx, mb.build(fx, name + "_c", cr), pulse=pulse * 0.5, rev=rev)


def ring_pair(mb_soft, mb_hard, r, w, soft_mult=3.2, **kw):
    mb_soft.ring(0, 0, r, w * soft_mult, soft=True, **kw)
    mb_hard.ring(0, 0, r, w, **kw)


def node(mb, x, y, r):
    mb.disc(x, y, r, 12)


def dot_ring(mb, r, n, rad, rot0=0.0):
    for k in range(n):
        a = rot0 + TAU * k / n
        mb.disc(r * math.cos(a), r * math.sin(a), rad, 8)


# ================================================================ circles
@reg("tran_1")
def tran_1():
    fx = gfx("tran_1", 4, "Phap tran so cap", "formation circle, realm grade 1 (Luyen Khi): plain thin ring, four rune marks")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 1.28, 0.06)
    h.ring(0, 0, 0.98, 0.03)
    for k in range(4):
        a = TAU * k / 4
        h.diamond(1.28 * math.cos(a), 1.28 * math.sin(a), 0.3, 0.2, a)
    runes(h, 0, 0, 1.0, 4, 0.3, rng, 0.04, rot0=PI / 4 * 0 + 0.0)
    runes(h, 0, 0, 0.62, 4, 0.2, rng, 0.03, rot0=PI / 4)
    two(fx, "ring", h, "#a8683a", "#d9a46a", pulse=0.08, soft_mb=s)
    return fx


@reg("tran_2")
def tran_2():
    fx = gfx("tran_2", 4, "Phap tran nhi cap", "formation circle, grade 2 (Truc Co): double ring around a square")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 1.34, 0.06)
    h.ring(0, 0, 1.1, 0.04)
    sq = 0.8
    h.ring(0, 0, sq * math.sqrt(2), 0.05, seg=4, a0=PI / 4, a1=PI / 4 + TAU - 1e-6)
    for k in range(4):
        a = PI / 4 + TAU * k / 4
        h.disc(sq * math.sqrt(2) * math.cos(a), sq * math.sqrt(2) * math.sin(a), 0.1, 10)
    runes(h, 0, 0, 1.22, 8, 0.15, rng, 0.03)
    runes(h, 0, 0, 0.35, 4, 0.2, rng, 0.03, rot0=0.0)
    h.ring(0, 0, 0.55, 0.025)
    two(fx, "ring", h, "#2fa6c4", "#9fe6f2", soft_mb=s)
    return fx


ELEM_NODE = [("#ffd96a", "#fff6c8"), ("#4ee06a", "#d8ffc0"), ("#3aa8ff", "#d0f4ff"), ("#ff5a28", "#ffd890"), ("#d79a3c", "#ffe9b0")]


@reg("tran_3")
def tran_3():
    fx = gfx("tran_3", 5, "Phap tran tam cap", "formation circle, grade 3 (Ket Dan): five-element pentagon")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 1.36, 0.05)
    h.ring(0, 0, 0.5, 0.03)
    pts = [(1.02 * math.cos(PI / 2 + TAU * k / 5), 1.02 * math.sin(PI / 2 + TAU * k / 5)) for k in range(5)]
    for k in range(5):                                  # pentagon edges
        h.line(pts[k], pts[(k + 1) % 5], 0.045)
    for k in range(5):                                  # pentagram diagonals (thin)
        h.line(pts[k], pts[(k + 2) % 5], 0.02)
    two(fx, "pent", h, "#b08a48", "#e8c880", soft_mb=s)
    # element nodes: coloured ring + disc + rune, each its own colour
    for k, (bc, cc) in enumerate(ELEM_NODE):
        n1, n2 = MB(), MB()
        n1.disc(0, 0, 0.34, 20, 1, 0)
        n2.ring(0, 0, 0.2, 0.05)
        runes(n2, 0, 0, 0, 1, 0.22, random.Random(40 + k), 0.04, tangent=False)
        ga = fx.mat("ng%d" % k, bc, grad=dict(src="attr", pow=1.0), opacity=0.8)
        ca = fx.mat("nc%d" % k, cc)
        for nm, mb, fm in (("g", n1, ga), ("c", n2, ca)):
            ob = mb.build(fx, "node%d%s" % (k, nm), fm)
            px, py = pts[k]
            fx.track(ob, lambda t, i, px=px, py=py: dict(
                x=px * math.cos(TAU * t / 5) - py * math.sin(TAU * t / 5), y=px * math.sin(TAU * t / 5) + py * math.cos(TAU * t / 5),
                op=0.85 + 0.15 * math.sin(TAU * t)))
    runes(MB(), 0, 0, 1, 1, 1, rng)
    return fx


def taiji(mb_a, mb_b, r):
    """mb_a: the 'yang' half (bright). mb_b: the yin half."""
    n = 28
    up = [(0.0, r)]
    right = [(r * math.cos(PI / 2 - PI * k / n), r * math.sin(PI / 2 - PI * k / n)) for k in range(n + 1)]       # top -> bottom via right
    low = [(0.5 * r * math.cos(-PI / 2 + PI * k / n), -0.5 * r + 0.5 * r * math.sin(-PI / 2 + PI * k / n)) for k in range(n + 1)]  # bottom -> centre via right
    topc = [(-0.5 * r * math.sin(PI * k / n) * 1.0, 0.5 * r - 0.5 * r * math.cos(PI * k / n)) for k in range(n + 1)]   # placeholder (replaced below)
    # top small circle's left half, from the centre up to the top
    topc = [(0.5 * r * math.cos(-PI / 2 - PI * k / n), 0.5 * r + 0.5 * r * math.sin(-PI / 2 - PI * k / n)) for k in range(n + 1)]
    yang = right + low[1:] + topc[1:]
    mb_a.poly(yang)
    mb_b.poly([(-x, -y) for (x, y) in yang])
    return mb_a


@reg("tran_4")
def tran_4():
    fx = gfx("tran_4", 8, "Phap tran tu cap", "formation circle, grade 4 (Nguyen Anh): yin-yang bagua octagon")
    rng = fx.rng
    s, h, tg = MB(), MB(), MB()
    ring_pair(s, h, 1.34, 0.06, seg=8, a0=PI / 8, a1=PI / 8 + TAU - 1e-6)
    h.ring(0, 0, 0.78, 0.035)
    # trigrams: 3 stacked bars each, broken or whole
    for k in range(8):
        a = TAU * k / 8
        bits = [(k >> b) & 1 for b in range(3)]
        for j, bit in enumerate(bits):
            r = 0.9 + j * 0.13
            L = 0.28
            ca, sa = math.cos(a), math.sin(a)
            tx, ty = -sa, ca
            px, py = r * ca, r * sa
            if bit:
                tg.line((px - tx * L / 2, py - ty * L / 2), (px + tx * L / 2, py + ty * L / 2), 0.065)
            else:
                for sgn in (-1, 1):
                    tg.line((px + tx * sgn * 0.04, py + ty * sgn * 0.04), (px + tx * sgn * L / 2, py + ty * sgn * L / 2), 0.065)
    two(fx, "oct", h, "#d89a3a", "#ffd88a", soft_mb=s)
    two(fx, "tri", tg, "#d89a3a", "#ffe6a8")
    yang, yin = MB(), MB()
    taiji(yang, yin, 0.7)
    gy = fx.mat("yin", "#4a62d8", opacity=0.9)
    gg = fx.mat("yang", "#ffe08a")
    d = fx.mat("dot1", "#ffe08a")
    d2 = fx.mat("dot2", "#2a2f66")
    ob = yin.build(fx, "yin", gy)
    fx.track(ob, lambda t, i: dict(op=0.9))
    ob = yang.build(fx, "yang", gg, z=0.01)
    fx.track(ob, lambda t, i: dict(op=0.9 + 0.1 * math.sin(TAU * t)))
    for nm, y, fm in (("a", 0.35, d2), ("b", -0.35, d)):
        o = MB().disc(0, 0, 0.1, 12).build(fx, "dot" + nm, fm, y=y, z=0.02)
        fx.track(o, lambda t, i, y=y: dict(y=y))
    rim = MB().ring(0, 0, 0.7, 0.04).build(fx, "rim", fx.mat("rimc", "#fff0b8"), z=0.03)
    fx.track(rim, lambda t, i: dict(op=0.9))
    return fx


@reg("tran_5")
def tran_5():
    fx = gfx("tran_5", 8, "Phap tran ngu cap", "formation circle, grade 5 (Hoa Than): ornate violet star mandala")
    rng = fx.rng
    s, h, m = MB(), MB(), MB()
    ring_pair(s, h, 1.34, 0.06)
    h.ring(0, 0, 1.18, 0.03)
    h.ring(0, 0, 0.62, 0.04)
    h.ring(0, 0, 0.35, 0.025)
    for off in (0.0, PI / 4):
        h.ring(0, 0, 1.12 * 1.0, 0.04, seg=4, a0=off + PI / 4, a1=off + PI / 4 + TAU - 1e-6)
    runes(h, 0, 0, 1.29, 16, 0.12, rng, 0.025)
    dot_ring(h, 0.62, 8, 0.07)
    m.star(0, 0, 8, 0.3, 0.12, 0)
    two(fx, "star", h, "#8a52ff", "#d8b8ff", soft_mb=s)
    cg = fx.mat("cg", "#ff6ad8", grad=dict(src="radial", pow=1.0), opacity=0.9)
    cc = fx.mat("cc", "#ffe6ff")
    spin(fx, MB().disc(0, 0, 0.5, 24, 1, 0).build(fx, "cglow", cg), pulse=0.15, rev=0)
    spin(fx, m.build(fx, "cstar", cc), rev=-1.0)
    return fx


@reg("tran_6")
def tran_6():
    fx = gfx("tran_6", 12, "Phap tran luc cap", "formation circle, grade 6 (Luyen Hu): blazing sun mandala")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 0.78, 0.07)
    h.ring(0, 0, 0.5, 0.04)
    runes(h, 0, 0, 0.64, 12, 0.13, rng, 0.028)
    # rays of the inner sun
    for k in range(12):
        a = TAU * k / 12 + TAU / 24
        h.diamond(0.32 * math.cos(a), 0.32 * math.sin(a), 0.22, 0.07, a)
    two(fx, "sun", h, "#e8801c", "#ffd070", soft_mb=s)
    core = fx.mat("core", "#ffcf50", grad=dict(src="radial", pow=0.8), core="#fff6c0", opacity=0.95)
    spin(fx, MB().disc(0, 0, 0.26, 20).build(fx, "sundisc", core), pulse=0.12, rev=0)
    red = fx.mat("fl1", "#ff3a14", grad=dict(src="attr", pow=0.5), opacity=0.9)
    org = fx.mat("fl2", "#ffa02a")
    gld = fx.mat("fl3", "#ffe58a")

    def tongues(scale, n, rad):
        def b(t, i):
            mb = MB()
            for k in range(n):
                a = TAU * k / n
                ph = TAU * (t + (k % 3) / 3.0)
                f = MB().flame(0, 0, 0.5 * scale * (1 + 0.14 * math.sin(ph)), 0.3 * scale, sway=0.08 * math.sin(ph + 1), lean=0.05 * math.cos(ph))
                mb.merge(f, rad * math.cos(a), rad * math.sin(a), 1.0, a - PI / 2)
            return mb
        return b
    fx.per_frame("flame_r", red, tongues(1.0, 12, 0.82))
    fx.per_frame("flame_o", org, tongues(0.62, 12, 0.82))
    fx.per_frame("flame_g", gld, tongues(0.32, 12, 0.83))
    return fx


@reg("tran_7")
def tran_7():
    fx = gfx("tran_7", 8, "Phap tran that cap", "formation circle, grade 7 (Hop The): swirling ice vortex with a sword ring")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 1.35, 0.04)
    sw = MB()
    for k in range(8):                                            # radial swords, tip outward
        a = TAU * k / 8
        ca, sa = math.cos(a), math.sin(a)
        sw.diamond(1.02 * ca, 1.02 * sa, 0.62, 0.12, a)
        sw.diamond(0.73 * ca, 0.73 * sa, 0.07, 0.3, a + PI / 2 * 0 + 0.0)    # crossguard
        sw.line((0.62 * ca, 0.62 * sa), (0.7 * ca, 0.7 * sa), 0.06)
    two(fx, "ice", h, "#58b0ff", "#e8fbff", soft_mb=s)
    two(fx, "sword", sw, "#6ac0ff", "#f4feff")
    # vortex arms
    def arm(a0, widthmul):
        pts, ws = [], []
        n = 28
        for k in range(n + 1):
            u = k / n
            r = 0.1 + 0.95 * u
            a = a0 + 2.4 * u * 1.15 + 1.0 * u * u
            pts.append((r * math.cos(a), r * math.sin(a)))
            ws.append(widthmul * (0.05 + 0.28 * math.sin(PI * min(1, u * 1.15)) ** 0.8))
        return MB().strip(pts, ws, soft=True)
    am = fx.mat("arm", "#38a0f0", grad=dict(src="attr", pow=0.8), core="#c8f0ff", opacity=0.9)
    ag = fx.mat("armg", "#2a70e0", grad=dict(src="attr", pow=1.2), opacity=0.6)
    for k in range(4):
        spin(fx, arm(TAU * k / 4, 1.7).build(fx, "armg%d" % k, ag), rev=-1.0 * 2)
        spin(fx, arm(TAU * k / 4, 1.0).build(fx, "arm%d" % k, am), rev=-1.0 * 2)
    cg = fx.mat("cg", "#c8f4ff", grad=dict(src="radial", pow=1.0), opacity=0.9)
    spin(fx, MB().disc(0, 0, 0.3, 20, 1, 0).build(fx, "core", cg), pulse=0.15, rev=0)
    return fx


@reg("tran_8")
def tran_8():
    fx = gfx("tran_8", 3, "Phap tran bat cap", "formation circle, grade 8 (Dai Thua): cosmic galaxy mandala with stars")
    rng = fx.rng
    s, h = MB(), MB()
    ring_pair(s, h, 1.35, 0.04)
    h.ring(0, 0, 1.2, 0.02)
    runes(h, 0, 0, 1.3, 12, 0.12, rng, 0.022)
    # constellation lines: a few connected points on the outer band
    for k in range(3):
        a = TAU * k / 3
        pts = [(1.08 * math.cos(a + d), 1.08 * math.sin(a + d)) for d in (-0.35, -0.12, 0.1, 0.3)]
        for q in range(3):
            h.line(pts[q], pts[q + 1], 0.02)
        for p in pts:
            h.disc(p[0], p[1], 0.05, 8)
    two(fx, "gal", h, "#e8b84a", "#fff0b0", soft_mb=s)

    def arm(a0, widthmul):
        pts, ws = [], []
        n = 32
        for k in range(n + 1):
            u = k / n
            r = 0.08 + 1.05 * u ** 0.9
            a = a0 + 3.4 * u
            pts.append((r * math.cos(a), r * math.sin(a)))
            ws.append(widthmul * (0.06 + 0.3 * math.sin(PI * min(1, u * 1.1)) ** 0.7))
        return MB().strip(pts, ws, soft=True)
    cols = [("#7a3cf0", "#d8b0ff"), ("#4a60e8", "#b8d0ff"), ("#c040d8", "#ffc8f4")]
    for k in range(3):
        mg = fx.mat("armg%d" % k, cols[k][0], grad=dict(src="attr", pow=1.1), opacity=0.7)
        mc = fx.mat("arm%d" % k, cols[k][0], grad=dict(src="attr", pow=0.7), core=cols[k][1], opacity=0.95)
        spin(fx, arm(TAU * k / 3, 1.9).build(fx, "armg%d" % k, mg), rev=-1)
        spin(fx, arm(TAU * k / 3, 0.9).build(fx, "arm%d" % k, mc), rev=-1)
    cg = fx.mat("cg", "#ffd060", grad=dict(src="radial", pow=0.9), core="#fffbe0", opacity=0.95)
    spin(fx, MB().disc(0, 0, 0.42, 22, 1, 0).build(fx, "core", cg), pulse=0.12, rev=0)
    sm = fx.mat("star", "#fff4d0")
    sm2 = fx.mat("star2", "#c8c0ff")
    for j in range(30):
        r = 0.25 + 1.1 * math.sqrt(rng.random())
        a = rng.uniform(0, TAU)
        ph = rng.random()
        big = j % 6 == 0
        mb = MB().star(0, 0, 4, 0.1 if big else 0.06, 0.02, PI / 2)
        ob = mb.build(fx, "star%d" % j, sm if j % 2 else sm2)
        fx.track(ob, lambda t, i, r=r, a=a, ph=ph: dict(x=r * math.cos(a), y=r * math.sin(a),
                                                          s=0.2 + 0.8 * (0.5 + 0.5 * math.sin(TAU * (t + ph))) ** 1.5 + 0.001))
    return fx


# ================================================================ hit-zone warnings (top view)
RED = "#e0501a"
HOT = "#ffd29a"
HW = 1.46            # half extent of the frame in units


def warn(id, frames, fps, loop, name_vi, where, **kw):
    fx = Fx(id, view="top", frames=frames, fps=fps, loop=loop, mode="alpha", px=96, ground=True, name_vi=name_vi, where=where,
            alpha_levels=6, zoom=1.05, **kw)
    return fx


def fan_pts(r0, r1, a0, a1, n=24):
    ox = -HW
    pts = []
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        pts.append((ox + r0 * math.cos(a), r0 * 0.7071 / 0.7071 * math.sin(a)))
    return pts


def cone_xy(u, a):
    """point of the 90-degree fan at radius fraction u, angle a (-45..45 deg). The fan is drawn
    stretched so its bounding box fills the frame (the game stretches it back)."""
    return (-HW + 2 * HW * u * math.cos(a), HW * u * math.sin(a) / math.sin(PI / 4))


def sector(u0, u1, n=28):
    top = [cone_xy(u1, -PI / 4 + (PI / 2) * k / n) for k in range(n + 1)]
    bot = [cone_xy(u0, PI / 4 - (PI / 2) * k / n) for k in range(n + 1)]
    return top + bot


def arc_strip(u, w, n=28):
    pts = [cone_xy(u, -PI / 4 + (PI / 2) * k / n) for k in range(n + 1)]
    return MB().strip(pts, w)


def warn_materials(fx):
    fx.dark = fx.mat("dark", "#3a0a0a", opacity=0.92)
    return (fx.mat("fill", RED, opacity=0.5), fx.mat("edge", "#ff6a2e", opacity=1.0), fx.mat("hot", HOT, opacity=1.0),
            fx.mat("fillhot", "#ff9a52", opacity=0.9))


@reg("warn_circle_charge")
def warn_circle_charge():
    fx = warn("warn_circle_charge", 4, 8, True, "Canh bao vong (tich luc)", "ground telegraph of a circular blow while it charges (stretch to the zone)")
    fill, edge, hot, _ = warn_materials(fx)
    disc = MB().disc(0, 0, HW - 0.04, 48).build(fx, "fill", fill, z=-0.01)
    fx.track(disc, lambda t, i: dict(op=0.30 + 0.16 * (0.5 + 0.5 * math.sin(TAU * t))))
    MB().ring(0, 0, HW - 0.09, 0.27, seg=64).build(fx, "edged", fx.dark, z=-0.03)
    MB().ring(0, 0, HW - 0.09, 0.14, seg=64).build(fx, "edge", edge)
    inner = MB().ring(0, 0, HW - 0.3, 0.07, seg=64).build(fx, "edge2", edge)
    fx.track(inner, lambda t, i: dict(op=0.7))
    for k in range(8):                                                   # inward ticks, they breathe
        a = TAU * k / 8
        tri = MB().poly([(0, 0.0), (0.2, -0.36), (-0.2, -0.36)]).build(fx, "tick%d" % k, edge)
        fx.track(tri, lambda t, i, a=a: dict(x=(HW - 0.2 - 0.16 * (0.5 + 0.5 * math.sin(TAU * t))) * math.cos(a), y=(HW - 0.2 - 0.16 * (0.5 + 0.5 * math.sin(TAU * t))) * math.sin(a),
                                              rot=a + PI / 2, s=0.55, op=0.9))
    pr = MB().ring(0, 0, 1.0, 0.07, seg=64).build(fx, "pulse", hot)
    fx.track(pr, lambda t, i: dict(s=0.15 + 0.85 * t, op=(1 - t) ** 0.8 * 0.9))
    return fx


@reg("warn_circle_release")
def warn_circle_release():
    fx = warn("warn_circle_release", 3, 14, False, "Canh bao vong (tung don)", "flash when the circular blow lands")
    fill, edge, hot, fh = warn_materials(fx)
    disc = MB().disc(0, 0, HW - 0.04, 48).build(fx, "fill", fh, z=-0.01)
    fx.track(disc, lambda t, i: dict(op=[1.0, 0.75, 0.3][i]))
    MB().ring(0, 0, HW - 0.09, 0.3, seg=64).build(fx, "ringd", fx.dark, z=-0.03)
    ring = MB().ring(0, 0, HW - 0.09, 0.2, seg=64).build(fx, "ring", hot)
    fx.track(ring, lambda t, i: dict(op=[1, 1, 0.8][i]))
    core = MB().disc(0, 0, 1.0, 40).build(fx, "core", hot)
    fx.track(core, lambda t, i: dict(s=[0.9, 0.6, 0.3][i], op=[0.9, 0.5, 0.0][i]))
    return fx


@reg("warn_cone_charge")
def warn_cone_charge():
    fx = warn("warn_cone_charge", 4, 8, True, "Canh bao hinh quat (tich luc)", "telegraph of a 90 degree cone while it charges; apex at the left-centre, bbox = R x 1.41R")
    fx.pivot = (4, 48)
    fill, edge, hot, _ = warn_materials(fx)
    ob = MB().poly(sector(0.0, 0.97)).build(fx, "fill", fill, z=-0.01)
    fx.track(ob, lambda t, i: dict(op=0.30 + 0.16 * (0.5 + 0.5 * math.sin(TAU * t))))
    for nm, a_ in (("d1", -PI / 4), ("d2", PI / 4)):
        MB().strip([cone_xy(0.0, 0), cone_xy(0.97, a_)], 0.26).build(fx, nm, fx.dark, z=-0.03)
    arc_strip(0.95, 0.26).build(fx, "arcd", fx.dark, z=-0.03)
    MB().strip([cone_xy(0.0, 0), cone_xy(0.97, -PI / 4)], 0.13).build(fx, "e1", edge)
    MB().strip([cone_xy(0.0, 0), cone_xy(0.97, PI / 4)], 0.13).build(fx, "e2", edge)
    arc_strip(0.95, 0.14).build(fx, "arc", edge)
    pulse = fx.per_frame("pulse", hot, lambda t, i: arc_strip(0.12 + 0.8 * t, 0.07 + 0.03 * t))
    for i, o in enumerate(pulse):
        fx.track(o, lambda t, ii, i=i: dict(show=(ii == i), op=(1 - t) ** 0.8))
    return fx


@reg("warn_cone_release")
def warn_cone_release():
    fx = warn("warn_cone_release", 3, 14, False, "Canh bao hinh quat (tung don)", "flash when the cone blow lands")
    fx.pivot = (4, 48)
    fill, edge, hot, fh = warn_materials(fx)
    ob = MB().poly(sector(0.0, 0.97)).build(fx, "fill", fh, z=-0.01)
    fx.track(ob, lambda t, i: dict(op=[1.0, 0.75, 0.3][i]))
    for nm, a_ in (("d1", -PI / 4), ("d2", PI / 4)):
        MB().strip([cone_xy(0.0, 0), cone_xy(0.97, a_)], 0.3).build(fx, nm, fx.dark, z=-0.03)
    arc_strip(0.94, 0.32).build(fx, "arcd", fx.dark, z=-0.03)
    MB().strip([cone_xy(0.0, 0), cone_xy(0.97, -PI / 4)], 0.2).build(fx, "e1", hot)
    MB().strip([cone_xy(0.0, 0), cone_xy(0.97, PI / 4)], 0.2).build(fx, "e2", hot)
    arc_strip(0.94, 0.22).build(fx, "arc", hot)
    return fx


def lane_rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


@reg("warn_line_charge")
def warn_line_charge():
    fx = warn("warn_line_charge", 4, 8, True, "Canh bao duong thang (tich luc)", "telegraph of a lane blow while it charges; points right, the lane fills the frame")
    fx.pivot = (4, 48)
    fill, edge, hot, _ = warn_materials(fx)
    ob = MB().poly(lane_rect(-HW + 0.03, HW - 0.03, -HW + 0.03, HW - 0.03)).build(fx, "fill", fill, z=-0.01)
    fx.track(ob, lambda t, i: dict(op=0.30 + 0.16 * (0.5 + 0.5 * math.sin(TAU * t))))
    for nm, r in (("dtop", lane_rect(-HW, HW, HW - 0.3, HW - 0.01)), ("dbot", lane_rect(-HW, HW, -HW + 0.01, -HW + 0.3)),
                  ("dend", lane_rect(HW - 0.3, HW - 0.01, -HW, HW)), ("dbeg", lane_rect(-HW + 0.01, -HW + 0.3, -HW, HW))):
        MB().poly(r).build(fx, nm, fx.dark, z=-0.03)
    MB().poly(lane_rect(-HW, HW, HW - 0.17, HW - 0.03)).build(fx, "top", edge)
    MB().poly(lane_rect(-HW, HW, -HW + 0.03, -HW + 0.17)).build(fx, "bot", edge)
    MB().poly(lane_rect(HW - 0.17, HW - 0.03, -HW, HW)).build(fx, "end", edge)
    MB().poly(lane_rect(-HW + 0.03, -HW + 0.17, -HW, HW)).build(fx, "beg", edge)
    for k in range(3):                                                   # chevrons running along the lane
        chev = MB().strip([(-0.32, 0.55), (0.18, 0.0), (-0.32, -0.55)], 0.17).build(fx, "chev%d" % k, hot)
        fx.track(chev, lambda t, i, k=k: dict(x=-HW + 0.5 + ((t + k / 3.0) % 1) * (2 * HW - 0.8), op=0.9 * math.sin(PI * ((t + k / 3.0) % 1)) ** 0.5 + 0.001))
    return fx


@reg("warn_line_release")
def warn_line_release():
    fx = warn("warn_line_release", 3, 14, False, "Canh bao duong thang (tung don)", "flash when the lane blow lands")
    fx.pivot = (4, 48)
    fill, edge, hot, fh = warn_materials(fx)
    ob = MB().poly(lane_rect(-HW + 0.03, HW - 0.03, -HW + 0.03, HW - 0.03)).build(fx, "fill", fh, z=-0.01)
    fx.track(ob, lambda t, i: dict(op=[1.0, 0.75, 0.3][i]))
    for nm, r in (("dtop", lane_rect(-HW, HW, HW - 0.34, HW - 0.01)), ("dbot", lane_rect(-HW, HW, -HW + 0.01, -HW + 0.34)),
                  ("dend", lane_rect(HW - 0.34, HW - 0.01, -HW, HW)), ("dbeg", lane_rect(-HW + 0.01, -HW + 0.34, -HW, HW))):
        MB().poly(r).build(fx, nm, fx.dark, z=-0.03)
    for nm, r in (("top", lane_rect(-HW, HW, HW - 0.24, HW - 0.03)), ("bot", lane_rect(-HW, HW, -HW + 0.03, -HW + 0.24)),
                  ("end", lane_rect(HW - 0.24, HW - 0.03, -HW, HW)), ("beg", lane_rect(-HW + 0.03, -HW + 0.24, -HW, HW))):
        MB().poly(r).build(fx, nm, hot)
    mid = MB().poly(lane_rect(-HW, HW, -0.5, 0.5)).build(fx, "mid", hot)
    fx.track(mid, lambda t, i: dict(op=[0.9, 0.5, 0.0][i]))
    return fx


@reg("crack_ground")
def crack_ground():
    fx = Fx("crack_ground", view="ground", frames=5, fps=12, loop=False, mode="alpha", px=96, ground=True,
            name_vi="Vet nut dat", where="the mark a heavy slam leaves in the ground", alpha_levels=4)
    rng = fx.rng
    dark = fx.mat("dark", "#2b1a10", window=True, opacity=0.95)
    ember = fx.mat("ember", "#ff8a30", window=True, opacity=1.0)
    rim = fx.mat("rim", "#7a6044", window=True, opacity=0.9)
    cracks = MB(), MB(), MB()
    n = 8
    for k in range(n):
        a = TAU * k / n + rng.uniform(-0.2, 0.2)
        L = rng.uniform(1.3, 1.62)
        pts = jag((0.0, 0.0), (L * math.cos(a), L * math.sin(a)), rng, 9, 0.16)
        ws = [0.24 * (1 - i / 9) ** 0.7 + 0.03 for i in range(10)]
        for mb, wm in ((cracks[0], 1.9), (cracks[1], 1.0), (cracks[2], 0.4)):
            mb.strip(pts, [w * wm for w in ws])
        for j in (3, 6):                                   # side branches
            if rng.random() < 0.8:
                p0 = pts[j]
                b = a + rng.choice((-1, 1)) * rng.uniform(0.5, 0.9)
                p1 = (p0[0] + 0.6 * math.cos(b), p0[1] + 0.6 * math.sin(b))
                bp = jag(p0, p1, rng, 4, 0.08)
                bw = [0.07 * (1 - i / 4) + 0.012 for i in range(5)]
                for mb, wm in ((cracks[0], 1.9), (cracks[1], 1.0), (cracks[2], 0.4)):
                    mb.strip(bp, [w * wm for w in bw])
    HEAD = [0.35, 0.7, 1.05, 1.05, 1.05]
    for nm, mb, fm, op in (("rim", cracks[0], rim, [1, 1, 1, 1, 0.95]), ("dark", cracks[1], dark, [1, 1, 1, 1, 1]),
                           ("ember", cracks[2], ember, [1, 0.9, 0.6, 0.3, 0.12])):
        ob = mb.build(fx, nm, fm, z={"rim": 0.0, "dark": 0.01, "ember": 0.02}[nm])
        fx.track(ob, lambda t, i, op=op: dict(head=HEAD[i], tail=-1.0, op=op[i]))
    # dust chunks
    chip = fx.mat("chip", "#8a7456", opacity=1.0)
    for j in range(8):
        a = rng.uniform(0, TAU)
        d = rng.uniform(0.3, 1.1)
        ob = MB().disc(0, 0, 0.06, 6).build(fx, "chip%d" % j, chip)
        fx.track(ob, lambda t, i, a=a, d=d: dict(x=d * math.cos(a) * (0.4 + 0.6 * ease_out(min(1, t * 2))), y=d * math.sin(a) * (0.4 + 0.6 * ease_out(min(1, t * 2))),
                                                  z=0.0, s=1.0 - t * 0.6, show=t < 0.95))
    return fx


def all_ids():
    return ["tran_%d" % i for i in range(1, 9)] + ["warn_circle_charge", "warn_circle_release", "warn_cone_charge", "warn_cone_release",
                                                    "warn_line_charge", "warn_line_release", "crack_ground"]


def make(id):
    return REG[id]()
