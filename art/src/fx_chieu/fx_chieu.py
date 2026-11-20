"""fx_chieu: the chiêu thức (combat skill) FX.  Runs INSIDE Blender.

One builder per sheet; each returns a ready CFx scene (flat emissive meshes built from numbers, keyframed,
orthographic camera).  Everything in px relative to the pivot, y up (see chieu_lib).  Directional FX point RIGHT.
"""
import math
import random

from chieu_lib import *            # noqa: F401,F403
from chieu_lib import CFx, MB, EL, RAMP, WHITE, KY, P, D, TAU, PI, sat, ease_out, ease_in, bump, ramp_up, \
    sword, blade_core, ring_e, ellipse_pts, spike, spike_facet, offset_poly, leaf, curve_strip, bezier, bolt, \
    star4, rune_marks, flame_tongue, crack, rot_pts, set_u_range
from ids import ALL

REG = {}


def reg(id):
    def deco(fn):
        REG[id] = fn
        return fn
    return deco


THUNDER = RAMP["thunder"]
HOLY = RAMP["holy"]
ICE = RAMP["ice"]
FLAME = RAMP["flame"]
COSMIC = RAMP["cosmic"]
VERD = RAMP["verdant"]


def diamond_mb(L, W):
    return MB().diamond(0, 0, L, W)


def star_mb(r, thin=0.2):
    return star4(MB(), 0, 0, r, thin)


def disc_mb(r, seg=16, soft=False):
    return MB().disc(0, 0, r, seg, 1.0, 0.0 if soft else 1.0)


# ============================================================================ tụ khí (charge-up), 6 elements
TU_NAME = {"kim": "Kim", "moc": "Mộc", "thuy": "Thủy", "hoa": "Hỏa", "tho": "Thổ", "loi": "Lôi"}


def make_tu_khi(el):
    r = EL[el]
    fx = CFx("tu_khi_" + el, px=96, frames=6, fps=12, loop=True, halo=0.6,
             name_vi="Tụ khí %s" % TU_NAME[el],
             where="qi gathering on the caster while a skill is channelled; pivot = the centre of gathering")
    rng = random.Random(len(el) * 7 + ord(el[0]))
    core_c = r[3] if el != "tho" else "#fff0a0"
    halo = fx.mat("halo", r[1], 0, grad=dict(src="attr", pow=1.6), opacity=0.9)
    glow = fx.mat("glow", r[2], 1, grad=dict(src="attr", pow=1.0))
    core = fx.mat("core", core_c, 4)
    stream = fx.mat("stream", r[2], 2)
    head = fx.mat("head", r[3], 3)
    mote2 = fx.mat("mote2", r[2], 2.5)

    # the gathering core: soft glow + white-hot heart, breathing with the loop
    fx.still(MB().disc(0, 0, 12, 24, 1.0, 0.0), "halo", halo, lambda t, i: dict(s=1.0 + 0.12 * math.sin(TAU * t)))
    fx.still(MB().disc(0, 0, 6, 20, 1.0, 0.25), "glow", glow, lambda t, i: dict(s=1.0 + 0.15 * math.sin(TAU * t + 0.6)))
    fx.still(star4(MB().disc(0, 0, 2.6, 12), 0, 0, 6.5, 0.18), "core", core,
             lambda t, i: dict(s=0.85 + 0.25 * (0.5 + 0.5 * math.sin(TAU * t + 0.6)), rot=0.0))

    # thin streams spiralling in: each is a dash travelling along a spiral from r=42 to r=6 (one trip per loop)
    NS = 7
    spirals = []
    for k in range(NS):
        a0 = TAU * k / NS + rng.uniform(-0.25, 0.25)
        turn = rng.choice((1, 1, -1)) * rng.uniform(0.9, 1.4)
        R0 = rng.uniform(36, 42)
        ph = (k * 3 % NS) / NS
        spirals.append((a0, turn, R0, ph))

    def spiral_pt(a0, turn, R0, s):
        rr = 6 + (R0 - 6) * (1 - s) ** 1.15
        a = a0 + turn * s
        return rr * math.cos(a), rr * math.sin(a) * 0.92

    def streams(t, i, heads=False):
        mb = MB()
        for (a0, turn, R0, ph) in spirals:
            s1 = (t + ph) % 1.0
            s0 = max(0.0, s1 - 0.38)
            if s1 < 0.08:
                continue
            m = 10
            pts = [spiral_pt(a0, turn, R0, s0 + (s1 - s0) * q / m) for q in range(m + 1)]
            if heads:
                x, y = pts[-1]
                mb.disc(x, y, 1.3, 8)
            else:
                curve_strip(mb, pts, 0.4, 1.9 + 0.6 * s1, pw=0.7)
        return mb
    fx.pf("stream", stream, streams)
    fx.pf("head", head, lambda t, i: streams(t, i, True))

    # motes (element flavoured) drifting inwards on spirals, recycled every loop
    def mote_shape(k):
        if el == "moc":
            return leaf(MB(), -2.4, 0, 0, 4.8, 2.2)
        if el == "thuy":
            return MB().drop(0, 0, 4.2, 2.2)
        if el == "tho":
            return MB().poly([(-1.6, -1.2), (1.4, -1.6), (1.8, 1.0), (-0.6, 1.8), (-1.9, 0.4)])
        if el == "loi":
            return MB().poly([(-2.2, 0.6), (0.2, 1.4), (-0.2, 0.2), (2.4, -0.6), (-0.1, -1.4), (0.3, -0.2)])
        if el == "kim" and k % 2 == 0:
            return star4(MB(), 0, 0, 2.6, 0.22)
        return MB().diamond(0, 0, 4.2, 1.6)
    NM = 14
    for k in range(NM):
        a0 = rng.uniform(0, TAU)
        turn = rng.uniform(0.5, 1.1) * (1 if k % 3 else -1)
        R0 = rng.uniform(26, 42)
        ph = k / NM + rng.uniform(-0.02, 0.02)
        fm = head if k % 3 == 0 else mote2

        def fn(t, i, a0=a0, turn=turn, R0=R0, ph=ph):
            s = (t + ph) % 1.0
            rr = 7 + (R0 - 7) * (1 - s) ** 1.2
            a = a0 + turn * s
            x, y = rr * math.cos(a), rr * math.sin(a)
            if el == "hoa":
                y += 3 * s                     # embers drift up a little while they are drawn in
            sc = 0.55 + 0.6 * math.sin(PI * min(1.0, s * 1.15)) if s < 0.87 else 0.0
            rot = math.atan2(-y, -x) if el in ("moc", "thuy", "loi", "hoa") or (el == "kim" and k % 2) else 0.0
            return (x, y, sc, rot)
        fx.particle("mote%d" % k, fm, mote_shape(k), fn)

    # a dashed ring tightening once per loop (the pull of the technique)
    ringm = fx.mat("ring", r[2], 1.5)

    def ring(t, i):
        mb = MB()
        rr = 40 - 20 * t
        w = 1.6 - 0.7 * t
        for k in range(6):
            a = TAU * k / 6 + 0.6 * t
            ring_e(mb, 0, 0, rr, rr * 0.92, w, a, a + 0.55)
        return mb
    fx.pf("ring", ringm, ring)
    if el == "loi":                     # little arcs crackling around the heart
        am = fx.mat("arc", THUNDER[3], 3.5)

        def arcs(t, i):
            mb = MB()
            rr = random.Random(500 + i)
            for k in range(3):
                a = rr.uniform(0, TAU)
                p0 = (6 * math.cos(a), 6 * math.sin(a))
                p1 = (16 * math.cos(a + 0.4), 16 * math.sin(a + 0.4))
                bolt(mb, p0, p1, rr, 1.2, 5, 2.5, 0)
            return mb
        fx.pf("arc", am, arcs)
    return fx


for _el in ("kim", "moc", "thuy", "hoa", "tho", "loi"):
    reg("tu_khi_" + _el)((lambda e: (lambda: make_tu_khi(e)))(_el))


# ============================================================================ 1. Ngự Kiếm Thuật
@reg("ngu_kiem")
def ngu_kiem():
    fx = CFx("ngu_kiem", px=96, frames=4, fps=14, loop=True, halo=0.7, name_vi="Ngự Kiếm Thuật - phi kiếm",
             where="flying sword with a light trail, travelling right (projectile); pivot = the sword's guard")
    L, W = 30, 5.2
    trail_o = fx.mat("trail_o", HOLY[1], 0, grad=dict(src="attr", pow=1.2), opacity=0.9)
    trail_i = fx.mat("trail_i", HOLY[2], 1, grad=dict(src="attr", pow=0.8))
    trail_c = fx.mat("trail_c", WHITE, 2)
    halo = fx.mat("halo", HOLY[1], 2.5, grad=dict(src="attr", pow=1.3))
    ghost = fx.mat("ghost", HOLY[2], 3)
    body = fx.mat("body", HOLY[2], 4)
    guard = fx.mat("guard", HOLY[1], 4.5)
    core = fx.mat("core", WHITE, 5)
    tipm = fx.mat("tip", WHITE, 6)
    X0 = -4                                  # guard position (px from the pivot): the sword's centre of mass

    def trail(t, i, layer):
        mb = MB()
        m = 16
        Ltr = 32
        pts, ws = [], []
        for q in range(m + 1):
            s = q / m
            x = X0 - 8 - Ltr * s
            y = 1.6 * math.sin(TAU * (t + s * 0.9)) * s
            pts.append((x, y))
            base = {"o": 11.0, "i": 5.0, "c": 1.6}[layer]
            ws.append(base * (1 - s) ** 0.9 + 0.3)
        mb.strip(pts, ws, soft=(layer != "c"))
        if layer == "i":                     # two thin speed streaks above and below
            for k, yy in enumerate((5.5, -5.5)):
                o = ((t * 1.0 + k * 0.5) % 1.0)
                xa = X0 - 10 - 30 * o
                mb.line((xa, yy * (1 - 0.3 * o)), (xa - 14, yy * (1 - 0.3 * o)), 0.9)
        return mb
    fx.pf("trail_o", trail_o, lambda t, i: trail(t, i, "o"))
    fx.pf("trail_i", trail_i, lambda t, i: trail(t, i, "i"))
    fx.pf("trail_c", trail_c, lambda t, i: trail(t, i, "c"))

    bob = lambda t: 0.6 * math.sin(TAU * t)
    hm = MB().strip([(X0 - 9, 0), (X0 + L * 0.5, 0), (X0 + L + 3, 0)], [7, 11, 2], soft=True)
    fx.still(hm, "halo", halo, lambda t, i: dict(y=bob(t)))
    # two after-images of the blade (the sword is moving very fast)
    for k, dx in enumerate((-9, -17)):
        g = MB()
        g.poly(rot_pts([(0, -W * 0.35), (L * 0.8, -W * 0.25), (L, 0), (L * 0.8, W * 0.25), (0, W * 0.35)], 0, X0 + dx, 0))
        fx.still(g, "ghost%d" % k, ghost, lambda t, i: dict(y=bob(t)))
    fx.still(sword(MB(), X0, 0, 0, L, W, guard=False, grip=True), "body", body, lambda t, i: dict(y=bob(t)))
    fx.still(MB().poly([(X0 - 1.4, -6.5), (X0 + 1.4, -6.5), (X0 + 1.4, 6.5), (X0 - 1.4, 6.5)]), "guard", guard,
             lambda t, i: dict(y=bob(t)))
    fx.still(blade_core(MB(), X0, 0, 0, L, W), "core", core, lambda t, i: dict(y=bob(t)))
    fx.still(star4(MB(), 0, 0, 6, 0.16), "tip", tipm,
             lambda t, i: dict(x=X0 + L - 1, y=bob(t), s=[1.0, 0.6, 0.85, 0.5][i], rot=0.0))
    # glints shed behind the sword
    sp = fx.mat("spark", HOLY[3], 6)
    for k in range(5):
        ph = k / 5
        yy = [-4, 3, -2, 5, 1][k]

        def fn(t, i, ph=ph, yy=yy):
            s = (t + ph) % 1.0
            return (X0 - 6 - 34 * s, yy + 2 * s * (1 if yy > 0 else -1), 1.0 - s, 0.0)
        fx.particle("sp%d" % k, sp, star4(MB(), 0, 0, 2.4, 0.22) if k % 2 else MB().diamond(0, 0, 3.6, 1.4), fn)
    return fx


@reg("ngu_kiem_xuyen")
def ngu_kiem_xuyen():
    fx = CFx("ngu_kiem_xuyen", px=64, frames=6, fps=18, halo=0.7, name_vi="Ngự Kiếm Thuật - xuyên thấu",
             where="flash on each target the flying sword pierces (one-shot); pivot = the hit point")
    line_o = fx.mat("line_o", HOLY[1], 0, grad=dict(src="attr", pow=1.0))
    line = fx.mat("line", WHITE, 3)
    ringm = fx.mat("ring", HOLY[2], 2)
    flash = fx.mat("flash", HOLY[2], 1, grad=dict(src="attr", pow=1.2))
    star = fx.mat("star", WHITE, 5)
    sp = fx.mat("spark", HOLY[3], 4)
    LEN = [38, 46, 46, 40, 30, 18]
    WID = [5, 4, 3, 2.2, 1.4, 0.9]

    def ln(t, i, outer):
        L, w = LEN[i], WID[i] * (2.2 if outer else 0.8)
        x0 = -L * 0.45 + 3 * i
        mb = MB()
        mb.strip([(x0, 0), (x0 + L * 0.5, 0), (x0 + L, 0)], [w * 0.2, w, w * 0.15], soft=outer)
        return mb
    fx.pf("line_o", line_o, lambda t, i: ln(t, i, True))
    fx.pf("line", line, lambda t, i: ln(t, i, False))
    fx.still(MB().disc(0, 0, 9, 20, 1.0, 0.0), "flash", flash,
             lambda t, i: dict(s=[1.0, 1.3, 0.9, 0.5, 0.25, 0.0][i]) if i < 5 else None)

    def rings(t, i):
        if i == 0 or i > 4:
            return None
        mb = MB()
        k = i / 4
        rx, ry = 3 + 4 * k, 9 + 14 * k
        ring_e(mb, 2 + 6 * k, 0, rx, ry, 2.2 - 1.6 * k)
        if i >= 2:
            ring_e(mb, 10 + 8 * k, 0, rx * 0.7, ry * 0.65, 1.2 - 0.6 * k)
        return mb
    fx.pf("ring", ringm, rings)
    fx.still(star4(MB(), 0, 0, 12, 0.12), "star", star,
             lambda t, i: dict(s=[0.8, 1.0, 0.65, 0.3, 0.0, 0.0][i], rot=D(45) * (i == 0)) if i < 4 else None)
    rng = fx.rng
    for k in range(7):
        ang = rng.uniform(-0.55, 0.55)
        sp_ = rng.uniform(16, 24)

        def fn(t, i, ang=ang, sp_=sp_):
            a = ramp_up(t, 0.1, 1.0)
            if a <= 0:
                return None
            d = 4 + sp_ * ease_out(a)
            return (d * math.cos(ang), d * math.sin(ang), (1 - a) ** 0.7, ang)
        fx.particle("sp%d" % k, sp, MB().diamond(0, 0, 5, 1.3), fn)
    return fx


# ============================================================================ 4. Chưởng Tâm Lôi
@reg("loi_xich")
def loi_xich():
    # 96x32 strip: endpoints at (3,16) and (92,16) every frame, so segments chain end to end
    fx = CFx("loi_xich", px=96, h=32, pivot=(3, 16), frames=4, fps=16, loop=True, halo=0.65,
             name_vi="Chưởng Tâm Lôi - xích lôi",
             where="one horizontal lightning segment; the game stretches + rotates it between two points; "
                   "pivot = left end, right end at x=92")
    halo = fx.mat("halo", COSMIC[1], 0, grad=dict(src="attr", pow=1.4), opacity=0.9)
    body = fx.mat("body", COSMIC[2], 2)
    core = fx.mat("core", THUNDER[3], 4)
    side = fx.mat("side", THUNDER[2], 1)
    L = 89.0

    def path(i, seed, amp):
        r = random.Random(seed + i * 31)
        n = 11
        pts = [(0.0, 0.0)]
        for k in range(1, n):
            s = k / n
            env = math.sin(PI * s) ** 0.6
            pts.append((L * s + r.uniform(-2, 2), r.uniform(-amp, amp) * env))
        pts.append((L, 0.0))
        return pts

    def lay(t, i, layer):
        mb = MB()
        pts = path(i, 7, 7.5)
        w = {"halo": 7.5, "body": 3.0, "core": 1.2}[layer]
        mb.strip(pts, [w] * len(pts), soft=(layer == "halo"))
        if layer != "halo":
            r = random.Random(90 + i)
            for _ in range(2):          # short forks off the main bolt
                k = r.randint(2, len(pts) - 3)
                x, y = pts[k]
                ang = r.choice((-1, 1)) * r.uniform(0.6, 1.2)
                l2 = r.uniform(6, 10)
                q = jag((x, y), (x + l2 * math.cos(ang), y + l2 * math.sin(ang)), r, 3, 2)
                mb.strip(q, [w * 0.7, w * 0.5, w * 0.35, w * 0.2])
        return mb
    fx.pf("halo", halo, lambda t, i: lay(t, i, "halo"))
    fx.pf("body", body, lambda t, i: lay(t, i, "body"))
    fx.pf("core", core, lambda t, i: lay(t, i, "core"))
    # a thinner second strand braided around the first
    fx.pf("side", side, lambda t, i: MB().strip(path(i, 300, 5.5), [1.0] * 12))
    return fx


@reg("loi_cham")
def loi_cham():
    fx = CFx("loi_cham", px=64, frames=6, fps=18, halo=0.7, name_vi="Chưởng Tâm Lôi - lôi chấn",
             where="spark burst where the chain lightning hits (one-shot); pivot = the hit point")
    flash = fx.mat("flash", COSMIC[1], 0, grad=dict(src="attr", pow=1.2))
    disc = fx.mat("disc", THUNDER[3], 4)
    forks = fx.mat("fork", COSMIC[2], 2)
    forkc = fx.mat("forkc", THUNDER[3], 3)
    ringm = fx.mat("ring", THUNDER[2], 1)
    FL = [1.0, 1.25, 0.9, 0.55, 0.3, 0.15]
    fx.still(MB().disc(0, 0, 13, 24, 1.0, 0.0), "flash", flash, lambda t, i: dict(s=FL[i]) if FL[i] > 0 else None)
    fx.still(star4(MB().disc(0, 0, 4, 14), 0, 0, 9, 0.2), "disc", disc,
             lambda t, i: dict(s=[1.0, 1.1, 0.7, 0.4, 0.0, 0.0][i], rot=D(20) * i) if i < 4 else None)
    LN = [14, 22, 26, 22, 14, 0]

    def fk(t, i, w):
        if LN[i] <= 0:
            return None
        r = random.Random(40 + i * 7)
        mb = MB()
        n = 6
        for k in range(n):
            a = TAU * k / n + r.uniform(-0.3, 0.3)
            L = LN[i] * r.uniform(0.7, 1.0)
            p0 = (3 * math.cos(a), 3 * math.sin(a))
            p1 = (L * math.cos(a), L * math.sin(a))
            bolt(mb, p0, p1, r, w * (1.0 - 0.15 * i), 5, L * 0.2, 1 if k % 2 else 0, 0.7, 0.45)
        return mb
    fx.pf("fork", forks, lambda t, i: fk(t, i, 2.4))
    fx.pf("forkc", forkc, lambda t, i: fk(t, i, 0.9))

    def rg(t, i):
        if not 1 <= i <= 4:
            return None
        mb = MB()
        rr = 10 + 5 * i
        for k in range(5):
            a = TAU * k / 5 + i * 0.4
            ring_e(mb, 0, 0, rr, rr, 1.6 - 0.25 * i, a, a + 0.8)
        return mb
    fx.pf("ring", ringm, rg)
    sp = fx.mat("spark", THUNDER[3], 5)
    rng = fx.rng
    for k in range(8):
        a = TAU * k / 8 + rng.uniform(-0.3, 0.3)
        v = rng.uniform(18, 26)

        def fn(t, i, a=a, v=v):
            q = ramp_up(t, 0.05, 1.0)
            if q <= 0:
                return None
            d = 6 + v * ease_out(q)
            return (d * math.cos(a), d * math.sin(a), (1 - q) ** 0.6, a)
        fx.particle("sp%d" % k, sp, MB().diamond(0, 0, 4.5, 1.2), fn)
    return fx


# ============================================================================ hero: Thiên Lôi Giáng
@reg("thien_loi_giang")
def thien_loi_giang():
    fx = CFx("thien_loi_giang", px=128, pivot=(64, 108), frames=8, fps=16, halo=0.75,
             name_vi="Thiên Lôi Giáng",
             where="heavenly lightning from the top of the frame down to the pivot on the ground (one-shot)")
    TOP = 102                                    # px above the pivot (frame y = 6)
    halo = fx.mat("halo", COSMIC[1], 0, grad=dict(src="attr", pow=1.3))
    body = fx.mat("body", COSMIC[2], 2)
    core = fx.mat("core", THUNDER[3], 4)
    gfl = fx.mat("gflash", COSMIC[1], 0.5, grad=dict(src="attr", pow=1.0))
    gcore = fx.mat("gcore", THUNDER[3], 3)
    gring = fx.mat("gring", THUNDER[2], 1.5)
    garc = fx.mat("garc", COSMIC[2], 2.5)
    # per frame: (main width scale, amplitude) ; 0 = no main bolt
    MAIN = [0.35, 1.0, 0.9, 0.55, 0.3, 0.18, 0.0, 0.0]

    def strike(i, layer):
        k = MAIN[i]
        if k <= 0:
            return None
        r = random.Random(11 + i * 3 if i != 2 else 11 + 3)    # frame 2 repeats frame 1's path (persistence)
        mb = MB()
        w = {"halo": 16.0, "body": 6.5, "core": 2.6}[layer] * k
        n = 10
        pts = [(r.uniform(-6, 6), TOP)]
        for q in range(1, n):
            s = q / n
            pts.append((r.uniform(-11, 11) * math.sin(PI * s) ** 0.5, TOP * (1 - s)))
        pts.append((0.0, 0.0))
        mb.strip(pts, [w * (0.65 + 0.35 * q / n) + 0.4 for q in range(n + 1)], soft=(layer == "halo"))
        if layer != "halo" and k >= 0.5:         # branches
            for b in range(3):
                q = 2 + b * 2 + r.randint(0, 1)
                x, y = pts[q]
                ang = -PI / 2 + r.choice((-1, 1)) * r.uniform(0.45, 0.9)
                l2 = r.uniform(16, 28)
                qq = jag((x, y), (x + l2 * math.cos(ang), y + l2 * math.sin(ang)), r, 4, 3.5)
                mb.strip(qq, [w * 0.55 * (1 - 0.7 * j / 4) + 0.3 for j in range(5)])
        if layer == "halo" and i in (1, 2):      # the sky splits: a flare where the bolt leaves the clouds
            mb.strip([(-26, TOP - 2), (0, TOP - 1), (26, TOP - 2)], [1, 9, 1], soft=True)
        return mb
    fx.pf("halo", halo, lambda t, i: strike(i, "halo"))
    fx.pf("body", body, lambda t, i: strike(i, "body"))
    fx.pf("core", core, lambda t, i: strike(i, "core"))
    # the ground flash (an ellipse on the 35 deg ground) and its shock ring
    GF = [0.35, 1.0, 1.15, 0.8, 0.5, 0.3, 0.18, 0.1]
    fx.still(MB().disc(0, 0, 34, 32, 1.0, 0.0, KY * 0.6), "gflash", gfl, lambda t, i: dict(s=GF[i]) if GF[i] else None)
    fx.still(MB().disc(0, 0, 11, 20, 1.0, 1.0, KY * 0.6), "gcore", gcore,
             lambda t, i: dict(s=[0.5, 1.0, 1.0, 0.6, 0.3, 0.0, 0, 0][i]) if i < 5 else None)

    def gr(t, i):
        if not 1 <= i <= 6:
            return None
        mb = MB()
        k = (i - 1) / 5
        rx = 16 + 30 * ease_out(k)
        ring_e(mb, 0, 0, rx, rx * KY * 0.6, 3.0 - 2.3 * k)
        return mb
    fx.pf("gring", gring, gr)

    def ga(t, i):                                # little arcs crawling over the ground after the strike
        if not 2 <= i <= 6:
            return None
        r = random.Random(70 + i)
        mb = MB()
        for k in range(4):
            a = r.uniform(0, TAU)
            d0, d1 = r.uniform(6, 12), r.uniform(20, 40) * (1 - 0.1 * (i - 2))
            p0 = (d0 * math.cos(a), d0 * math.sin(a) * KY * 0.6)
            p1 = (d1 * math.cos(a), d1 * math.sin(a) * KY * 0.6)
            bolt(mb, p0, p1, r, 1.3, 5, 2.5, 0)
        return mb
    fx.pf("garc", garc, ga)
    sp = fx.mat("spark", THUNDER[3], 5)
    rng = fx.rng
    for k in range(12):
        a = rng.uniform(0.15, PI - 0.15)
        v = rng.uniform(22, 40)
        t0 = rng.uniform(0.1, 0.25)

        def fn(t, i, a=a, v=v, t0=t0):
            q = (t - t0) / 0.7
            if q < 0 or q > 1:
                return None
            x = v * math.cos(a) * ease_out(q)
            y = v * math.sin(a) * 0.8 * ease_out(q) - 14 * q * q + 2
            return (x, y, (1 - q) ** 0.5, math.atan2(math.sin(a) - q, math.cos(a)))
        fx.particle("sp%d" % k, sp, MB().diamond(0, 0, 4.6, 1.3), fn)
    return fx


# ============================================================================ sword helpers (kim)
def light_sword_layers(fx, prefix, ramp=HOLY, z0=2.0, guard_c=None):
    """materials for a sword of light: halo / blade / guard / white ridge."""
    return dict(
        halo=fx.mat(prefix + "halo", ramp[1], z0, grad=dict(src="attr", pow=1.3), opacity=0.85),
        body=fx.mat(prefix + "body", ramp[2], z0 + 1),
        guard=fx.mat(prefix + "guard", guard_c or HOLY[1], z0 + 1.5),
        core=fx.mat(prefix + "core", ramp[3] if ramp is not HOLY else WHITE, z0 + 2),
    )


def add_sword(mbs, x, y, ang, L, W, s=1.0, halo_w=2.6):
    """append one sword of light to the four layer meshes in mbs (dict of MB)."""
    L, W = L * s, W * s
    ca, sa = math.cos(ang), math.sin(ang)
    hx0, hy0 = x - ca * L * 0.25, y - sa * L * 0.25
    mbs["halo"].strip([(hx0, hy0), (x + ca * L * 0.45, y + sa * L * 0.45), (x + ca * (L + 2), y + sa * (L + 2))],
                      [W * halo_w * 0.6, W * halo_w, W * 0.8], soft=True)
    sword(mbs["body"], x, y, ang, L, W, guard=False, grip=True)
    g = [(-W * 0.4, -W * 1.4), (W * 0.4, -W * 1.4), (W * 0.4, W * 1.4), (-W * 0.4, W * 1.4)]
    mbs["guard"].poly(rot_pts(g, ang, x, y))
    blade_core(mbs["core"], x, y, ang, L, W)


def new_layers():
    return dict(halo=MB(), body=MB(), guard=MB(), core=MB())


# ============================================================================ 2. Vạn Kiếm Quy Tông
@reg("van_kiem_troi")
def van_kiem_troi():
    """swords materialising one by one on a ring overhead, all pointing down; pivot = the ground centre."""
    fx = CFx("van_kiem_troi", px=128, pivot=(64, 120), frames=8, fps=14, halo=0.7,
             name_vi="Vạn Kiếm Quy Tông - kiếm trận trên trời",
             where="swords of light forming in a ring above the target area (one-shot); pivot = area centre on the ground")
    CY_, RX, RY = 78, 48, 13                      # ring centre height above the pivot, ring radii
    N = 12
    order = [0, 6, 3, 9, 1, 7, 4, 10, 2, 8, 5, 11]
    born = {k: 0.06 + 0.5 * order.index(k) / N for k in range(N)}
    front = fx.mat("front_body", HOLY[2], 4)
    mats_f = light_sword_layers(fx, "f_", z0=4)
    mats_b = light_sword_layers(fx, "b_", z0=1)
    mats_b["body"] = fx.mat("b_body2", HOLY[1], 2)
    ringm = fx.mat("ring", HOLY[2], 0.5)
    runem = fx.mat("rune", HOLY[1], 0.6)
    glint = fx.mat("glint", WHITE, 7)

    def ring(t, i):
        g = ease_out(ramp_up(t, 0.0, 0.35))
        if g <= 0:
            return None
        mb = MB()
        a1 = -PI / 2 + TAU * g
        ring_e(mb, 0, CY_, RX * (0.85 + 0.15 * g), RY, 1.5, -PI / 2, a1)
        ring_e(mb, 0, CY_, RX * 0.62, RY * 0.62, 1.0, -PI / 2 - PI * g, -PI / 2 + PI * g)
        return mb
    fx.pf("ring", ringm, ring)

    def runes(t, i):
        if t < 0.15:
            return None
        mb = MB()
        r = random.Random(5)
        pa = []
        for k in range(10):
            a = TAU * k / 10 + 0.3 * t
            pa.append((RX * 0.8 * math.cos(a), CY_ + RY * 0.8 * math.sin(a), 0.0))
        rune_marks(mb, pa, 4.2, r, 0.9)
        return mb
    fx.pf("rune", runem, runes)

    def swords(t, i, back):
        L = new_layers()
        for k in range(N):
            a = TAU * k / N + D(8)
            sy = math.sin(a)
            if (sy > 0) != back:
                continue
            q = ramp_up(t, born[k], born[k] + 0.16)
            if q <= 0:
                continue
            s = (0.75 if back else 1.0) * (0.35 + 0.65 * ease_out(q)) * (1.0 + 0.12 * bump(q, 0.6, 1.01))
            x = RX * math.cos(a)
            y = CY_ + RY * sy + 12 * s                    # guard above, blade points down to the ring
            drop = 4 * ease_in(ramp_up(t, 0.85, 1.0))     # the whole array dips: ready to fall
            add_sword(L, x, y - drop, -PI / 2, 22, 3.8, s)
        return L
    for back, mats in ((True, mats_b), (False, mats_f)):
        for lay in ("halo", "body", "guard", "core"):
            fx.pf(("b" if back else "f") + lay, mats[lay], (lambda b, ly: (lambda t, i: swords(t, i, b)[ly]))(back, lay))

    # a glint where each sword is born
    for k in range(N):
        a = TAU * k / N + D(8)
        x, y = RX * math.cos(a), CY_ + RY * math.sin(a) + 2
        tb = born[k]

        def fn(t, i, x=x, y=y, tb=tb):
            q = (t - tb + 0.07) / 0.2
            if q < 0 or q > 1:
                return None
            return (x, y + 8, math.sin(PI * q) * 1.0, 0.0)
        fx.particle("gl%d" % k, glint, star4(MB(), 0, 0, 6, 0.15), fn)
    return fx


@reg("van_kiem_roi")
def van_kiem_roi():
    """the rain: swords streak down and stab into the area, flash, then burst into light."""
    fx = CFx("van_kiem_roi", px=128, pivot=(64, 112), frames=10, fps=16, halo=0.7,
             name_vi="Vạn Kiếm Quy Tông - vạn kiếm rơi",
             where="rain of swords striking the target area (one-shot, ~10 frames); pivot = area centre on the ground")
    rng = random.Random(77)
    N = 16
    RX, RY = 44, 15
    pts = []
    while len(pts) < N:                             # landing points spread over the area ellipse
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y <= 1 and all((x - a) ** 2 + (y - b) ** 2 > 0.09 for a, b, _ in pts):
            pts.append((x, y, 0))
    land = []
    for k, (x, y, _) in enumerate(pts):
        land.append((x * RX, y * RY, 1 + (k * 5) % 6))     # land on frames 1..6
    land.sort(key=lambda p: -p[1])                          # back (higher y) first
    streak = fx.mat("streak", HOLY[1], 1, grad=dict(src="attr", pow=1.0))
    streakc = fx.mat("streakc", HOLY[3], 1.5)
    mats = light_sword_layers(fx, "s_", z0=3)
    flash = fx.mat("flash", HOLY[2], 2, grad=dict(src="attr", pow=1.0))
    ringm = fx.mat("ring", HOLY[2], 2.2)
    mote = fx.mat("mote", WHITE, 7)
    TOPY = 110

    def frame_parts(t, i):
        L = new_layers()
        st, stc, fl, rg = MB(), MB(), MB(), MB()
        for (x, y, f) in land:
            if i < f - 2:
                continue
            if i < f:                                   # falling: a long streak with the sword at its head
                k = (i - (f - 2) + 1) / 2.0             # 0.5, 1.0
                ytip = y + (TOPY - y) * (1 - k) + 6
                st.strip([(x, min(TOPY, ytip + 60)), (x, ytip + 18)], [0.6, 4.5], soft=True)
                stc.strip([(x, min(TOPY, ytip + 50)), (x, ytip + 18)], [0.3, 1.2])
                add_sword(L, x, ytip + 18, -PI / 2, 18, 3.2, 1.0, 1.8)
            else:                                       # stuck in the ground: blade half buried, guard up
                age = i - f
                if age > 4:
                    continue
                add_sword(L, x, y + 9, -PI / 2, 12, 3.2, 1.0, 1.6 if age < 2 else 1.0)
                if age <= 1:
                    fl.disc(x, y, 7 - 2 * age, 14, 1.0, 0.0, KY)
                if age <= 2:
                    ring_e(rg, x, y, 4 + 4 * age, (4 + 4 * age) * KY * 0.7, 1.4 - 0.4 * age)
        return dict(L=L, st=st, stc=stc, fl=fl, rg=rg)
    cache = {}

    def part(i, key, sub=None):
        if i not in cache:
            cache[i] = frame_parts(fx.T(i), i)
        v = cache[i][key]
        return v[sub] if sub else v
    fx.pf("streak", streak, lambda t, i: part(i, "st"))
    fx.pf("streakc", streakc, lambda t, i: part(i, "stc"))
    for lay in ("halo", "body", "guard", "core"):
        fx.pf("s" + lay, mats[lay], (lambda ly: (lambda t, i: part(i, "L", ly)))(lay))
    fx.pf("flash", flash, lambda t, i: part(i, "fl"))
    fx.pf("ring", ringm, lambda t, i: part(i, "rg"))
    # the stuck swords burst into rising light motes at the end
    for k, (x, y, f) in enumerate(land):
        for j in range(2):
            t0 = (f + 3.5 + 0.5 * j) / 9.0

            def fn(t, i, x=x, y=y, t0=t0, j=j):
                q = (t - t0) / 0.3
                if q < 0 or q > 1:
                    return None
                return (x + (j - 0.5) * 4 * q, y + 8 + 18 * q, (1 - q) ** 0.5, 0.0)
            fx.particle("m%d_%d" % (k, j), mote, star4(MB(), 0, 0, 2.6, 0.22) if j else MB().diamond(0, 0, 1.6, 3.6), fn)
    return fx


def sigil_swords(mb, n, r0, r1, w, inward=True, ky=1.0, rot=0.0):
    """flat sword marks on a ground circle (plane coordinates): blade from r0 to r1."""
    for k in range(n):
        a = rot + TAU * k / n
        ca, sa = math.cos(a), math.sin(a)
        if inward:
            x, y, ang = r1 * ca, r1 * sa, a + PI
        else:
            x, y, ang = r0 * ca, r0 * sa, a
        sword(mb, x, y, ang, abs(r1 - r0), w, guard=True, grip=True)
    return mb


@reg("van_kiem_vong")
def van_kiem_vong():
    fx = CFx("van_kiem_vong", px=128, view="ground", frames=8, fps=8, loop=True, ground=True, halo=0.6,
             name_vi="Vạn Kiếm Quy Tông - kiếm ấn trên đất",
             where="sigil marking the struck area on the ground (loop, drawn under the characters); pivot = area centre")
    # plane coordinates (px), the camera squashes y by sin 35
    outer = fx.mat("outer", HOLY[2], 2)
    outerh = fx.mat("outerh", HOLY[1], 0, grad=dict(src="attr", pow=1.2), opacity=0.8)
    inner = fx.mat("inner", HOLY[1], 1.5)
    runem = fx.mat("runes", HOLY[2], 2.5)
    swm = fx.mat("swords", HOLY[2], 3)
    swc = fx.mat("swordc", WHITE, 3.5)
    centre = fx.mat("centre", WHITE, 4)
    fx.still(ring_e(MB(), 0, 0, 58, 58, 9, soft=True), "outerh", outerh,
             lambda t, i: dict(s=1.0 + 0.02 * math.sin(TAU * t)))
    fx.still(ring_e(ring_e(MB(), 0, 0, 58, 58, 2.2), 0, 0, 53, 53, 1.0), "outer", outer)
    fx.still(ring_e(ring_e(MB(), 0, 0, 40, 40, 1.4), 0, 0, 18, 18, 1.4), "inner", inner)
    r = random.Random(3)
    rb = MB()
    for k in range(16):                       # 4 distinct marks repeated: the band rotates by a quarter per loop
        rr = random.Random(10 + k % 4)
        a = TAU * k / 16
        rune_marks(rb, [(47 * math.cos(a), 47 * math.sin(a), a - PI / 2)], 5.0, rr, 1.1)
    fx.still(rb, "runes", runem, lambda t, i: dict(rot=TAU / 4 * t))
    # eight swords pointing inwards at the centre (the target), and a cross star
    fx.still(sigil_swords(MB(), 8, 20, 38, 3.6, inward=True), "swords", swm,
             lambda t, i: dict(rot=-TAU / 8 * t))
    core = MB()
    for k in range(8):
        a = TAU * k / 8
        x, y = 38 * math.cos(a), 38 * math.sin(a)
        blade_core(core, x, y, a + PI, 18, 3.6)
    fx.still(core, "swordc", swc, lambda t, i: dict(rot=-TAU / 8 * t))
    fx.still(star4(MB(), 0, 0, 13, 0.16).merge(MB().disc(0, 0, 3, 10)), "centre", centre,
             lambda t, i: dict(s=0.85 + 0.2 * math.sin(TAU * t) ** 2))
    return fx


# ============================================================================ 10. Kiếm Vực
@reg("kiem_vuc")
def kiem_vuc():
    fx = CFx("kiem_vuc", px=128, view="ground", frames=8, fps=8, loop=True, ground=True, halo=0.6,
             name_vi="Kiếm Vực - vùng kiếm",
             where="the sword domain circle on the ground around the caster (loop, under the characters); pivot = centre")
    outerh = fx.mat("outerh", ICE[0], 0, grad=dict(src="attr", pow=1.2), opacity=0.85)
    outer = fx.mat("outer", ICE[2], 2)
    outerc = fx.mat("outerc", ICE[3], 2.5)
    gold = fx.mat("gold", HOLY[2], 2.2)
    runem = fx.mat("runes", HOLY[2], 2.6)
    swm = fx.mat("swords", ICE[2], 3)
    swg = fx.mat("swordg", HOLY[1], 3.2)
    swc = fx.mat("swordc", ICE[3], 3.5)
    fill = fx.mat("fill", ICE[0], -1, grad=dict(src="attr", pow=1.0), opacity=0.5)
    fx.still(MB().disc(0, 0, 60, 48, 0.0, 1.0), "fill", fill)
    fx.still(ring_e(MB(), 0, 0, 60, 60, 8, soft=True), "outerh", outerh)
    fx.still(ring_e(MB(), 0, 0, 59, 59, 2.4), "outer", outer)
    fx.still(ring_e(MB(), 0, 0, 59, 59, 0.9), "outerc", outerc)
    # gold inner circle with rune band, counter-rotating
    fx.still(ring_e(ring_e(MB(), 0, 0, 30, 30, 1.3), 0, 0, 22, 22, 1.0), "gold", gold)
    rb = MB()
    for k in range(12):
        rr = random.Random(30 + k % 3)
        a = TAU * k / 12
        rune_marks(rb, [(26 * math.cos(a), 26 * math.sin(a), a - PI / 2)], 4.2, rr, 1.0)
    fx.still(rb, "runes", runem, lambda t, i: dict(rot=-TAU / 4 * t))
    # twelve swords lying on the ground, pointing outwards (the domain's edge), turning with the domain
    sw, sg, sc = MB(), MB(), MB()
    for k in range(12):
        a = TAU * k / 12
        ca, sa = math.cos(a), math.sin(a)
        x, y = 36 * ca, 36 * sa
        sword(sw, x, y, a, 18, 4.0, guard=False, grip=True)
        gq = [(-1.6, -5.5), (1.6, -5.5), (1.6, 5.5), (-1.6, 5.5)]
        sg.poly(rot_pts(gq, a, x, y))
        blade_core(sc, x, y, a, 18, 4.0)
    for mb, nm, fm in ((sw, "swords", swm), (sg, "swordg", swg), (sc, "swordc", swc)):
        fx.still(mb, nm, fm, lambda t, i: dict(rot=TAU / 12 * t))
    # small sword-intent glints pulsing on the rim
    gl = fx.mat("glint", ICE[3], 4)
    for k in range(4):
        a = TAU * k / 4 + D(45)
        fx.particle("gl%d" % k, gl, star4(MB(), 0, 0, 5, 0.15),
                    lambda t, i, a=a, k=k: (59 * math.cos(a + TAU / 12 * t), 59 * math.sin(a + TAU / 12 * t),
                                            max(0.0, math.sin(TAU * (t + k * 0.25))), 0.0))
    return fx


@reg("kiem_vuc_xoay")
def kiem_vuc_xoay():
    fx = CFx("kiem_vuc_xoay", px=128, pivot=(64, 104), frames=8, fps=12, loop=True, halo=0.6,
             name_vi="Kiếm Vực - kiếm xoay quanh thân",
             where="ring of swords orbiting the caster at body height (loop); pivot = the caster's feet")
    N = 8
    CY_, RX, RY = 26, 46, 13
    trailm = fx.mat("trail", ICE[1], 0.5, grad=dict(src="attr", pow=1.0), opacity=0.9)
    mats_b = dict(halo=fx.mat("b_halo", ICE[0], 1, grad=dict(src="attr", pow=1.3), opacity=0.7),
                  body=fx.mat("b_body", ICE[1], 1.5), guard=fx.mat("b_guard", HOLY[0], 1.6),
                  core=fx.mat("b_core", ICE[2], 1.7))
    mats_f = dict(halo=fx.mat("f_halo", ICE[1], 4, grad=dict(src="attr", pow=1.3), opacity=0.85),
                  body=fx.mat("f_body", ICE[2], 4.5), guard=fx.mat("f_guard", HOLY[1], 4.6),
                  core=fx.mat("f_core", ICE[3], 4.7))

    def pos(a):
        return RX * math.cos(a), CY_ + RY * math.sin(a)

    def parts(t, i, back):
        L = new_layers()
        tr = MB()
        for k in range(N):
            a = TAU * k / N + TAU / N * t                # counter-clockwise seen from above: front moves right
            sa = math.sin(a)
            if (sa > 0) != back:
                continue
            x, y = pos(a)
            dx, dy = -RX * math.sin(a), RY * math.cos(a)
            ang = math.atan2(dy, dx)
            s = 0.78 + 0.22 * (-sa if not back else -sa)  # nearer = bigger
            s = 0.72 + 0.28 * (0.5 - 0.5 * sa)
            add_sword(L, x - math.cos(ang) * 8 * s, y - math.sin(ang) * 8 * s, ang, 20, 3.6, s, 2.2)
            # light trail behind it along the orbit
            tp = [pos(a - 0.05 * q) for q in range(9)]
            tr.strip(tp[::-1], [0.3 + 2.4 * s * (q / 8) for q in range(9)], soft=True)
        return L, tr
    for back, mats in ((True, mats_b), (False, mats_f)):
        for lay in ("halo", "body", "guard", "core"):
            fx.pf(("b" if back else "f") + lay, mats[lay],
                  (lambda b, ly: (lambda t, i: parts(t, i, b)[0][ly]))(back, lay))
    fx.pf("trail", trailm, lambda t, i: parts(t, i, False)[1].merge(parts(t, i, True)[1]))
    return fx


# ============================================================================ hero: Phá Mê Kiếm Quyết
@reg("pha_me_kiem")
def pha_me_kiem():
    fx = CFx("pha_me_kiem", px=128, pivot=(10, 64), frames=7, fps=20, halo=0.75,
             name_vi="Phá Mê Kiếm Quyết",
             where="one decisive straight sword-light cut with a cross glint, pointing right (one-shot); "
                   "pivot = the sword hand")
    halo = fx.mat("halo", HOLY[1], 0, grad=dict(src="attr", pow=1.2), opacity=0.9)
    edge = fx.mat("edge", HOLY[2], 2)
    core = fx.mat("core", WHITE, 4)
    split = fx.mat("split", HOLY[2], 2.5)
    star = fx.mat("star", WHITE, 6)
    starh = fx.mat("starh", HOLY[2], 5)
    END = [46, 112, 112, 112, 112, 112, 112]
    BEG = [2, 4, 8, 18, 34, 56, 80]
    TH = [1.2, 1.0, 0.8, 0.55, 0.38, 0.25, 0.15]
    XS = 74                                      # where the cross glint flashes

    def cut(t, i, layer):
        x0, x1, k = BEG[i], END[i], TH[i]
        mb = MB()
        if layer == "split":                     # the cut opens: two hair lines drifting apart
            if i < 2:
                return None
            d = 2.0 + 2.5 * (i - 2)
            for sgn in (1, -1):
                xa = x0 + (x1 - x0) * 0.1
                mb.strip([(xa, sgn * d), ((xa + x1) / 2, sgn * d * 1.15), (x1 - 4, sgn * d * 0.6)],
                         [0.3, 1.1 * k + 0.3, 0.3])
            return mb
        w = {"halo": 13.0, "edge": 4.6, "core": 1.8}[layer] * k
        pts = [(x0, 0), (x0 + (x1 - x0) * 0.25, 0), (x0 + (x1 - x0) * 0.7, 0), (x1, 0)]
        mb.strip(pts, [w * 0.15 + 0.2, w, w * 0.9, 0.3], soft=(layer == "halo"))
        return mb
    for lay, fm in (("halo", halo), ("edge", edge), ("core", core), ("split", split)):
        fx.pf(lay, fm, (lambda ly: (lambda t, i: cut(t, i, ly)))(lay))
    SS = [0.0, 1.0, 1.25, 0.9, 0.55, 0.25, 0.0]
    fx.still(star4(MB(), 0, 0, 22, 0.08).merge(star4(MB(), 0, 0, 11, 0.14), rot=D(45)), "star", star,
             lambda t, i: dict(x=XS, s=SS[i], rot=0.0) if SS[i] else None)
    fx.still(MB().disc(0, 0, 12, 20, 1.0, 0.0), "starh", starh,
             lambda t, i: dict(x=XS, s=SS[i]) if SS[i] else None)
    sp = fx.mat("spark", HOLY[3], 5.5)
    rng = fx.rng
    for k in range(10):
        x0 = rng.uniform(30, 104)
        vy = rng.choice((-1, 1)) * rng.uniform(6, 16)
        vx = rng.uniform(4, 14)
        t0 = 0.15 + 0.4 * (x0 - 30) / 74

        def fn(t, i, x0=x0, vx=vx, vy=vy, t0=t0):
            q = (t - t0) / 0.55
            if q < 0 or q > 1:
                return None
            return (x0 + vx * ease_out(q), vy * ease_out(q), (1 - q) ** 0.6, math.atan2(vy, vx))
        fx.particle("sp%d" % k, sp, MB().diamond(0, 0, 4.4, 1.2), fn)
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
