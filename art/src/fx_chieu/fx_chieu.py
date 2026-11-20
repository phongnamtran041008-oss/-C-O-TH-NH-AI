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


# ============================================================================ fire helpers
def blob(mb, cx, cy, r, rng, n=18, amp=0.18, phase=0.0, kx=1.0, soft=False):
    """a noisy round flame body (star-shaped fan)."""
    pts = []
    ph = [rng.uniform(0, TAU) for _ in range(3)]
    for k in range(n):
        a = TAU * k / n
        rr = r * (1 + amp * (0.6 * math.sin(3 * a + ph[0] + phase) + 0.4 * math.sin(5 * a + ph[1] - phase)))
        pts.append((cx + rr * math.cos(a) * kx, cy + rr * math.sin(a)))
    return mb.fan(cx, cy, pts, 1.0, 0.0 if soft else 1.0)


def tongue(mb, base, ang, h, w, sway):
    return flame_tongue(mb, base, ang, h, w, sway)


# ============================================================================ 5. Hỏa Long Thuật
HEAD = [(0, 10), (8, 14), (16, 15), (24, 12), (32, 9), (40, 8), (43, 5), (42, 2), (34, 1), (24, 1), (16, -1),
        (26, -4), (36, -6), (38, -9), (28, -12), (16, -13), (6, -12), (0, -9)]
HEAD_LIT = [(2, 9), (9, 12), (16, 13), (24, 10), (32, 7), (39, 6), (40, 4), (30, 5), (20, 6), (10, 6), (3, 5)]


@reg("hoa_long")
def hoa_long():
    fx = CFx("hoa_long", px=128, frames=6, fps=12, loop=True, halo=0.6, name_vi="Hỏa Long Thuật - hỏa long",
             where="a dragon of fire surging right (projectile, loop); pivot = frame centre (the dragon's chest)")
    HX = 6                                    # where the head joins the neck
    halo = fx.mat("halo", FLAME[1], 0, grad=dict(src="attr", pow=1.3), opacity=0.5)
    outl = fx.mat("outline", FLAME[0], 1)
    body = fx.mat("body", FLAME[1], 2)
    belly = fx.mat("belly", FLAME[2], 2.6)
    spine = fx.mat("spine", FLAME[3], 3)
    scal = fx.mat("scales", FLAME[0], 3.2)
    fin = fx.mat("fin", FLAME[2], 1.6)
    fino = fx.mat("fino", FLAME[1], 1.5)
    head_o = fx.mat("head_o", FLAME[0], 4)
    head = fx.mat("head", FLAME[1], 4.5)
    head_l = fx.mat("head_l", FLAME[2], 5)
    horn = fx.mat("horn", FLAME[2], 4.2)
    eye = fx.mat("eye", FLAME[3], 6)
    teeth = fx.mat("teeth", FLAME[3], 5.5)
    whisk = fx.mat("whisker", FLAME[2], 5.2)
    breath = fx.mat("breath", FLAME[2], 3.5)
    breathc = fx.mat("breathc", FLAME[3], 3.8)
    mane = fx.mat("mane", FLAME[1], 3.9)
    manec = fx.mat("manec", FLAME[2], 4.0)

    def hy(t):
        return 4 + 1.6 * math.sin(TAU * t)

    def spinept(t, s):
        x = HX + 2 - 56 * s
        env = sat(s / 0.25) ** 1.2
        y = hy(t) * (1 - s) - 2 * s + 9 * env * math.sin(TAU * (s * 1.15) - TAU * t + 0.6)
        return x, y

    def width(s):
        return 20 * (1 - s) ** 0.75 + 1.5

    def body_mb(t, i, k=1.0, dy=0.0, soft=False, n=30):
        pts = [spinept(t, q / n) for q in range(n + 1)]
        pts = [(x, y + dy * width(q / n) / 20) for q, (x, y) in enumerate(pts)]
        return MB().strip(pts, [width(q / n) * k + 0.3 for q in range(n + 1)], soft=soft)
    fx.pf("halo", halo, lambda t, i: body_mb(t, i, 1.6, soft=True))
    fx.pf("outline", outl, lambda t, i: body_mb(t, i, 1.0).merge(body_mb(t, i, 1.0)))
    fx.pf("body", body, lambda t, i: body_mb(t, i, 0.78))
    fx.pf("belly", belly, lambda t, i: body_mb(t, i, 0.36, dy=-3.2))
    fx.pf("spine", spine, lambda t, i: body_mb(t, i, 0.1, dy=-3.0))

    def scales(t, i):
        mb = MB()
        for q in range(3, 22, 2):
            s = q / 30
            x, y = spinept(t, s)
            x2, y2 = spinept(t, s + 0.02)
            ang = math.atan2(y2 - y, x2 - x)
            w = width(s) * 0.32
            nx, ny = -math.sin(ang), math.cos(ang)
            # a chevron pointing towards the head
            a = (x + nx * w - math.cos(ang) * 2.5, y + ny * w - math.sin(ang) * 2.5)
            c = (x + nx * 0.2 * w, y + ny * 0.2 * w)
            mb.strip([a, (x - math.cos(ang) * 0.8, y - math.sin(ang) * 0.8), c], [0.9, 1.1, 0.7])
        return mb
    fx.pf("scales", scal, scales)

    def fins(t, i, inner):
        r = random.Random(40 + i)
        mb = MB()
        for q in range(2, 28, 3):
            s = q / 30
            x, y = spinept(t, s)
            x2, y2 = spinept(t, s - 0.02)
            ang = math.atan2(y2 - y, x2 - x)          # towards the head
            nx, ny = -math.sin(ang), math.cos(ang)
            if ny < 0:
                nx, ny = -nx, -ny
            w = width(s)
            base = (x + nx * w * 0.4, y + ny * w * 0.4)
            h = (8 + 9 * (1 - s)) * (0.85 + 0.25 * math.sin(TAU * t * 2 + q)) * (0.55 if inner else 1.0)
            back = ang + PI                           # tongues stream back (towards the tail) and up
            a = math.atan2(ny * 0.9 + math.sin(back) * 0.6, nx * 0.9 + math.cos(back) * 0.6)
            tongue(mb, base, a, h, (6 + 4 * (1 - s)) * (0.5 if inner else 1.0), r.uniform(-2, 2))
        # the tail ends in a fan of fire
        x, y = spinept(t, 1.0)
        for k in range(3):
            tongue(mb, (x + 2, y), PI + (k - 1) * 0.45 + 0.15 * math.sin(TAU * t + k), (11 - 2 * abs(k - 1)) * (0.6 if inner else 1),
                   5 * (0.5 if inner else 1), 1.5)
        return mb
    fx.pf("fino", fino, lambda t, i: fins(t, i, False))
    fx.pf("fin", fin, lambda t, i: fins(t, i, True))

    # the head
    def head_at(t, pts):
        return [(HX + x, hy(t) + y) for x, y in pts]
    fx.pf("head_o", head_o, lambda t, i: MB().poly(offset_poly(head_at(t, HEAD), 1.6)))
    fx.pf("head", head, lambda t, i: MB().poly(head_at(t, HEAD)))
    fx.pf("head_l", head_l, lambda t, i: MB().poly(head_at(t, HEAD_LIT)))

    def horns(t, i):
        mb = MB()
        y0 = hy(t)
        for (p0, p1, p2, p3, w0) in (((14, 13), (6, 22), (-6, 27), (-18, 27), 4.6), ((6, 12), (0, 17), (-8, 20), (-14, 19), 3.2)):
            pts = bezier(*[(HX + x, y0 + y) for x, y in (p0, p1, p2, p3)], n=10)
            curve_strip(mb, pts, w0, 0.6)
        # brow spike
        mb.poly([(HX + 20, y0 + 13), (HX + 28, y0 + 11), (HX + 15, y0 + 19)])
        return mb
    fx.pf("horn", horn, horns)
    fx.pf("eye", eye, lambda t, i: MB().diamond(HX + 26, hy(t) + 8.5, 6, 2.6, -0.15))

    def teeth_(t, i):
        mb = MB()
        y0 = hy(t)
        for x in (27, 33, 38):
            mb.poly([(HX + x - 1.5, y0 + 1.2), (HX + x + 1.5, y0 + 1.2), (HX + x, y0 - 2)])
        for x in (28, 34):
            mb.poly([(HX + x - 1.5, y0 - 4.6 - (x - 28) * 0.2), (HX + x + 1.5, y0 - 4.8 - (x - 28) * 0.2), (HX + x, y0 - 1.6)])
        return mb
    fx.pf("teeth", teeth, teeth_)

    def whiskers(t, i):
        mb = MB()
        y0 = hy(t)
        sw = 2.5 * math.sin(TAU * t + 1)
        for (p0, p1, p2, p3) in (((40, 3), (30, -6), (14, -14 + sw), (-4, -18 + sw)),
                                 ((36, -8), (26, -16), (10, -22 - sw), (-2, -22 - sw))):
            pts = bezier(*[(HX + x, y0 + y) for x, y in (p0, p1, p2, p3)], n=12)
            curve_strip(mb, pts, 1.6, 0.5)
        return mb
    fx.pf("whisker", whisk, whiskers)

    def manes(t, i, inner):
        r = random.Random(60 + i)
        mb = MB()
        y0 = hy(t)
        for k in range(5):
            base = (HX + 2 + k * 2.5, y0 + 6 + k * 1.6 - (k > 2) * 2)
            a = D(150 - k * 8) + 0.12 * math.sin(TAU * t + k)
            h = (17 + 4 * math.sin(TAU * t * 2 + k * 1.3) - k) * (0.6 if inner else 1.0)
            tongue(mb, base, a, h, 7 * (0.55 if inner else 1.0), r.uniform(-2.5, 2.5))
        return mb
    fx.pf("mane", mane, lambda t, i: manes(t, i, False))
    fx.pf("manec", manec, lambda t, i: manes(t, i, True))

    def breath_(t, i, inner):
        mb = MB()
        y0 = hy(t)
        for k in range(2):
            h = (9 + 3 * math.sin(TAU * t * 2 + k * 2)) * (0.6 if inner else 1.0)
            tongue(mb, (HX + 32, y0 - 2.0 - k * 1.5), -0.08 - 0.2 * k, h + 6, 5 * (0.55 if inner else 1.0), 1.2)
        return mb
    fx.pf("breath", breath, lambda t, i: breath_(t, i, False))
    fx.pf("breathc", breathc, lambda t, i: breath_(t, i, True))
    # embers shed by the body
    em = fx.mat("ember", FLAME[3], 6)
    for k in range(8):
        ph = k / 8
        s0 = 0.15 + 0.1 * (k % 7)

        def fn(t, i, ph=ph, s0=s0, k=k):
            q = (t + ph) % 1.0
            x, y = spinept(0.0, s0)
            return (x - 18 * q, y + (6 + 10 * q) * (1 if k % 2 else -0.6), (1 - q) ** 0.6 * 1.1, D(45))
        fx.particle("em%d" % k, em, MB().diamond(0, 0, 2.6, 2.6), fn)
    return fx


@reg("hoa_long_vet")
def hoa_long_vet():
    fx = CFx("hoa_long_vet", px=96, pivot=(48, 60), frames=6, fps=10, loop=True, ground=True, halo=0.6,
             name_vi="Hỏa Long Thuật - vết lửa",
             where="burning trail left on the ground by the fire dragon (loop, under the characters); "
                   "pivot = the trail centre on the ground; long axis horizontal (rotate to the path)")
    scorch = fx.mat("scorch", FLAME[0], 0, grad=dict(src="attr", pow=1.0), opacity=0.8)
    lava = fx.mat("lava", FLAME[2], 1)
    lavac = fx.mat("lavac", FLAME[3], 1.5)
    fo = fx.mat("fo", FLAME[1], 2)
    fm_ = fx.mat("fm", FLAME[2], 2.5)
    fc = fx.mat("fc", FLAME[3], 3)
    fx.still(MB().disc(0, 0, 42, 32, 1.0, 0.0, 0.2), "scorch", scorch)
    r0 = random.Random(9)
    lv = [(-36 + 72 * k / 12, r0.uniform(-2, 2) if 0 < k < 12 else 0) for k in range(13)]
    fx.still(MB().strip(lv, [0.6] + [2.6] * 11 + [0.6]), "lava", lava)
    fx.still(MB().strip(lv, [0.3] + [0.9] * 11 + [0.3]), "lavac", lavac)
    pos = [(-30, 1, 10), (-21, -2, 15), (-12, 2, 19), (-3, -1, 24), (7, 2, 21), (16, -2, 17), (25, 1, 13), (33, 0, 9)]

    def flames(t, i, kh, kw):
        mb = MB()
        r = random.Random(i * 5 + 1)
        for k, (x, y, h) in enumerate(pos):
            hh = h * (0.75 + 0.3 * math.sin(TAU * (t * (1 + k % 2) + k * 0.37))) * kh
            tongue(mb, (x, y), PI / 2 + 0.12 * math.sin(TAU * t + k), hh, 8.5 * kw, r.uniform(-2.5, 2.5))
        return mb
    fx.pf("fo", fo, lambda t, i: flames(t, i, 1.0, 1.0))
    fx.pf("fm", fm_, lambda t, i: flames(t, i, 0.65, 0.6))
    fx.pf("fc", fc, lambda t, i: flames(t, i, 0.32, 0.3))
    em = fx.mat("ember", FLAME[3], 4)
    for k in range(6):
        x0 = -30 + 12 * k

        def fn(t, i, x0=x0, k=k):
            q = (t + k / 6) % 1.0
            return (x0 + 3 * math.sin(TAU * q), 14 + 24 * q, (1 - q) ** 0.6, D(45))
        fx.particle("em%d" % k, em, MB().diamond(0, 0, 2.4, 2.4), fn)
    return fx


# ============================================================================ hero: Hỏa Cầu
@reg("hoa_cau_lon")
def hoa_cau_lon():
    fx = CFx("hoa_cau_lon", px=96, frames=4, fps=14, loop=True, halo=0.6, name_vi="Hỏa Cầu Thuật - đại hỏa cầu",
             where="a big fireball with a roaring tail flying right (projectile, loop); pivot = frame centre")
    BX = 16
    halo = fx.mat("halo", FLAME[1], 0, grad=dict(src="attr", pow=1.2), opacity=0.5)
    to = fx.mat("tail_o", FLAME[1], 1)
    ti = fx.mat("tail_i", FLAME[2], 1.5)
    outer = fx.mat("outer", FLAME[1], 2)
    mid = fx.mat("mid", FLAME[2], 2.5)
    core = fx.mat("core", FLAME[3], 3)
    bow = fx.mat("bow", FLAME[2], 3.5)

    def tail(t, i, k):
        mb = MB()
        r = random.Random(i + 3)
        for j in range(7):
            yy = (j - 3) * 3.2
            L = (36 + 18 * (1 - abs(j - 3) / 3) + 5 * math.sin(TAU * t + j * 1.9)) * k
            ang = PI + yy * 0.022 + 0.06 * math.sin(TAU * t * 2 + j)
            tongue(mb, (BX - 4, yy * 0.9), ang, L, (12 - abs(j - 3) * 1.5) * k, r.uniform(-4, 4) * k)
        return mb
    fx.pf("halo", halo, lambda t, i: blob(MB(), BX, 0, 22, random.Random(i), amp=0.1, phase=TAU * t, soft=True))
    fx.pf("tail_o", to, lambda t, i: tail(t, i, 1.0))
    fx.pf("tail_i", ti, lambda t, i: tail(t, i, 0.55))
    fx.pf("outer", outer, lambda t, i: blob(MB(), BX, 0, 15, random.Random(10 + i), amp=0.15, phase=TAU * t))
    fx.pf("mid", mid, lambda t, i: blob(MB(), BX + 1.5, 0.5, 10.5, random.Random(20 + i), amp=0.12, phase=TAU * t))
    fx.pf("core", core, lambda t, i: blob(MB(), BX + 3, 1, 5.5, random.Random(30 + i), amp=0.1))

    def bow_(t, i):
        mb = MB()
        pts = ellipse_pts(BX - 4, 0, 21, 18, 14, -D(50), D(50))
        mb.strip(pts, [0.3 + 1.0 * math.sin(PI * q / 14) for q in range(15)])
        return mb
    fx.pf("bow", bow, bow_)
    em = fx.mat("ember", FLAME[3], 4)
    for k in range(6):
        yy = [-9, 6, -3, 10, 2, -12][k]

        def fn(t, i, yy=yy, k=k):
            q = (t + k / 6) % 1.0
            return (BX - 14 - 30 * q, yy + 3 * math.sin(TAU * q + k), (1 - q) ** 0.5 * 1.2, D(45))
        fx.particle("em%d" % k, em, MB().diamond(0, 0, 2.6, 2.6), fn)
    return fx


@reg("hoa_cau_no")
def hoa_cau_no():
    fx = CFx("hoa_cau_no", px=128, frames=8, fps=16, halo=0.6, name_vi="Hỏa Cầu Thuật - hỏa cầu nổ",
             where="the big fireball's explosion (one-shot); pivot = the impact point")
    RB = [12, 28, 38, 42, 40, 34, 0, 0]
    HEAT = [1.0, 1.0, 0.85, 0.6, 0.35, 0.0, 0, 0]
    halo = fx.mat("halo", FLAME[1], 0, grad=dict(src="attr", pow=1.1), opacity=0.5)
    outer = fx.mat("outer", FLAME[1], 2)
    mid = fx.mat("mid", FLAME[2], 2.5)
    core = fx.mat("core", FLAME[3], 3)
    ringm = fx.mat("ring", FLAME[2], 1)
    tongm = fx.mat("tongue", FLAME[1], 1.8)
    smoke = fx.mat("smoke", "#5e636f", 0.5, grad=dict(src="attr", pow=0.8), opacity=0.55)
    smoke2 = fx.mat("smoke2", "#888e98", 0.6, grad=dict(src="attr", pow=1.0), opacity=0.45)

    def ball(t, i, layer):
        R = RB[i]
        if R <= 0:
            return None
        r = random.Random(i * 7 + len(layer))
        h = HEAT[i]
        if layer == "halo":
            return blob(MB(), 0, 0, R * 1.25, r, amp=0.1, soft=True)
        if layer == "outer":
            if i >= 4:                               # the ball breaks into billows
                mb = MB()
                for k in range(7):
                    a = TAU * k / 7 + i
                    blob(mb, R * 0.62 * math.cos(a), R * 0.62 * math.sin(a) + 3 * (i - 3), R * 0.38, r, 12, 0.2)
                return mb
            return blob(MB(), 0, 0, R, r, 22, 0.16)
        if h <= 0:
            return None
        if layer == "mid":
            return blob(MB(), 0, 0, R * 0.68 * h ** 0.5, r, 18, 0.15)
        return blob(MB(), 0, 0, R * 0.38 * h, r, 14, 0.12)
    for lay, fm in (("halo", halo), ("outer", outer), ("mid", mid), ("core", core)):
        fx.pf(lay, fm, (lambda ly: (lambda t, i: ball(t, i, ly)))(lay))

    def ring(t, i):
        if not 1 <= i <= 4:
            return None
        rr = [0, 36, 50, 56, 59][i]
        return ring_e(MB(), 0, 0, rr, rr * 0.92, [0, 3.2, 2.2, 1.4, 0.8][i])
    fx.pf("ring", ringm, ring)

    def tongues(t, i):
        if not 1 <= i <= 4:
            return None
        r = random.Random(80 + i)
        mb = MB()
        R = RB[i]
        for k in range(11):
            a = TAU * k / 11 + r.uniform(-0.2, 0.2)
            L = R * (0.5 - 0.06 * i) + r.uniform(4, 9)
            tongue(mb, (R * 0.75 * math.cos(a), R * 0.75 * math.sin(a)), a, L, 9 - i, r.uniform(-2, 2))
        return mb
    fx.pf("tongue", tongm, tongues)

    def smk(t, i, k2):
        if i < 4:
            return None
        r = random.Random(3)
        mb = MB()
        q = (i - 4) / 3
        for k in range(9):
            a = TAU * k / 9 + 0.4
            d = 16 + 12 * q + 6 * (k % 2)
            rad = (10 + 3 * q) * (1 - 0.3 * q) * k2
            blob(mb, d * math.cos(a), d * math.sin(a) * 0.75 + 16 * q + 4, rad, r, 12, 0.2, soft=True)
        return mb
    fx.pf("smoke", smoke, lambda t, i: smk(t, i, 1.0))
    fx.pf("smoke2", smoke2, lambda t, i: smk(t, i, 0.55))
    em = fx.mat("ember", FLAME[3], 5)
    em2 = fx.mat("ember2", FLAME[2], 4.8)
    rng = fx.rng
    for k in range(16):
        a = TAU * k / 16 + rng.uniform(-0.2, 0.2)
        v = rng.uniform(34, 52)

        def fn(t, i, a=a, v=v):
            q = ramp_up(t, 0.1, 1.0)
            if q <= 0 or q >= 0.98:
                return None
            d = 10 + v * ease_out(q)
            return (d * math.cos(a), d * math.sin(a) - 10 * q * q, (1 - q) ** 0.4 * 1.2, a)
        fx.particle("em%d" % k, em if k % 2 else em2, MB().diamond(0, 0, 4, 1.6), fn)
    return fx


# ============================================================================ 3. Băng Phong Thuật
ICE_RAMPS = ("ice", "blue", "steel", "bone", "spirit", "thunder")
OUTL_ICE = "#243a6a"


def spike_layers(fx, prefix, z0, body=ICE[1], facet=ICE[2], hi=ICE[3], outl=OUTL_ICE):
    return dict(o=fx.mat(prefix + "o", outl, z0), b=fx.mat(prefix + "b", body, z0 + 0.3),
                f=fx.mat(prefix + "f", facet, z0 + 0.6), h=fx.mat(prefix + "h", hi, z0 + 0.9))


def spike_meshes(h, w, lean):
    """one crystal spike standing on the origin: outline, body, lit facet, highlight edge."""
    body = [(-w / 2, 0), (w / 2, 0), (w * 0.08 + lean, h), (-w * 0.08 + lean, h)]
    if w < 7:
        body = [(-w / 2, 0), (w / 2, 0), (lean, h)]
    facet = [(-w / 2 + w * 0.12, h * 0.03), (-w * 0.05, h * 0.03), (lean - w * 0.04, h * 0.93)]
    hil = [(-w / 2 + w * 0.12, h * 0.05), (lean - w * 0.04, h * 0.95)]
    return dict(o=MB().poly(offset_poly(body, 1.4)), b=MB().poly(body), f=MB().poly(facet),
                h=MB().strip(hil, [1.0, 0.6]))


@reg("bang_phong")
def bang_phong():
    fx = CFx("bang_phong", px=96, pivot=(48, 76), frames=8, fps=14, halo=0.0, ramps=ICE_RAMPS,
             name_vi="Băng Phong Thuật - băng thứ",
             where="ice spikes bursting from the ground in a patch, then shattering (one-shot); "
                   "pivot = the patch centre on the ground")
    patch = fx.mat("patch", ICE[3], 0, grad=dict(src="attr", pow=0.6), opacity=0.6)
    rim = fx.mat("rim", ICE[3], 0.3)
    L = spike_layers(fx, "s", 1)
    # x, depth (y on the ground, + = back), height, width, lean
    SP = [(-6, 6, 42, 12, -2), (10, 5, 34, 11, 4), (-21, 4, 27, 10, -6), (24, 2, 23, 9, 7), (-31, -2, 15, 7, -6),
          (1, -3, 31, 11, 1), (17, -5, 21, 9, 5), (-14, -6, 23, 9, -4), (31, -7, 13, 7, 5)]
    order = sorted(range(len(SP)), key=lambda k: abs(SP[k][0]))
    GROW = [0.0] * len(SP)
    for n, k in enumerate(order):
        GROW[k] = 0.0 + 0.045 * n

    def pt(t, i):
        g = ease_out(ramp_up(t, 0.0, 0.25))
        return dict(s=0.4 + 0.6 * g) if i < 7 else dict(s=1.05)
    fx.still(MB().disc(0, 0, 36, 28, 0.9, 0.0, KY * 0.55), "patch", patch,
             lambda t, i: dict(s=0.4 + 0.6 * ease_out(ramp_up(t, 0.0, 0.25))) if i < 7 else None)
    fx.still(ring_e(MB(), 0, 0, 34, 34 * KY * 0.55, 1.0), "rim", rim,
             lambda t, i: dict(s=0.4 + 0.6 * ease_out(ramp_up(t, 0.0, 0.25))) if i < 7 else None)
    for k, (x, y, h, w, lean) in enumerate(SP):
        ms = spike_meshes(h, w, lean)
        rank = 10 - y                                  # nearer (lower y) = drawn later

        def fn(t, i, k=k, x=x, y=y, rank=rank):
            q = ramp_up(t, GROW[k], GROW[k] + 0.2)
            if q <= 0 or i >= 7:
                return None
            sy = ease_out(q) * (1 + 0.14 * bump(q, 0.55, 1.01))
            if i == 6:
                sy *= 0.92
            return dict(x=x, y=y * 1.0, sx=0.75 + 0.25 * ease_out(q), sy=max(sy, 0.05), dz=rank * 0.5)
        for lay in ("o", "b", "f", "h"):
            fx.still(ms[lay], "sp%d%s" % (k, lay), L[lay], fn)
    # cracks over the spikes just before they shatter, then the shards
    cr = fx.mat("crack", ICE[3], 9)

    def cracks(t, i):
        if i != 6:
            return None
        mb = MB()
        r = random.Random(4)
        for (x, y, h, w, lean) in SP:
            if h < 20:
                continue
            p0 = (x + lean * 0.3, y + h * 0.3)
            p1 = (x + lean * 0.7 + r.uniform(-2, 2), y + h * 0.75)
            mb.strip(jag(p0, p1, r, 3, 1.5), [0.8] * 4)
        return mb
    fx.pf("crack", cr, cracks)
    sh = spike_layers(fx, "sh", 8)
    rng = fx.rng
    for k in range(14):
        x0, y0 = rng.uniform(-28, 28), rng.uniform(6, 30)
        vx, vy = x0 * rng.uniform(0.3, 0.6), rng.uniform(4, 12)

        def fn(t, i, x0=x0, y0=y0, vx=vx, vy=vy, k=k):
            if i < 6:
                return None
            q = (i - 5) / 2.0
            return (x0 + vx * q, y0 + vy * q - 16 * q * q, 1.0 - 0.25 * q, k * 0.7 + q)
        m = MB().poly([(-3, -1.2), (2.6, -1.6), (3.4, 1.0), (-1, 2.0)])
        fx.particle("shd%d" % k, sh["b"] if k % 3 else sh["h"], m, fn)
    return fx


@reg("bang_ket")
def bang_ket():
    fx = CFx("bang_ket", px=64, pivot=(32, 56), frames=4, fps=6, loop=True, halo=0.0, ramps=ICE_RAMPS,
             name_vi="Băng Phong Thuật - đóng băng",
             where="frost crystals clinging to a frozen monster (loop, drawn over the monster); pivot = the monster's "
                   "feet; made for a 48 px monster, scale by monster frame / 48")
    shell = fx.mat("shell", ICE[1], 0, opacity=0.3)
    rim = fx.mat("rim", ICE[3], 0.5, opacity=0.75)
    facet = fx.mat("facet", ICE[3], 0.6, opacity=0.5)
    L = spike_layers(fx, "c", 2)
    HULL = [(-21, 0), (21, 0), (24, 14), (17, 33), (0, 40), (-17, 33), (-24, 14)]
    fx.still(MB().poly(HULL), "shell", shell)
    rimpts = HULL + [HULL[0]]
    fx.still(MB().strip(rimpts, [1.0] * len(rimpts)), "rim", rim)
    fm = MB()
    for a, b in (((0, 40), (4, 20)), ((4, 20), (21, 0)), ((4, 20), (-24, 14)), ((17, 33), (4, 20))):
        fm.strip([a, b], [0.8, 0.8])
    fx.still(fm, "facet", facet)
    # crystal clusters on the feet and the flanks
    CL = [(-18, 2, 13, 7, -4), (-11, -1, 9, 6, -2), (-4, -2, 6, 5, 0), (6, -2, 8, 5, 2), (13, -1, 12, 7, 3),
          (19, 3, 16, 7, 4), (-22, 12, 10, 5, -4), (22, 16, 9, 5, 4)]
    for k, (x, y, h, w, lean) in enumerate(CL):
        ms = spike_meshes(h, w, lean)
        for lay in ("o", "b", "f", "h"):
            fx.still(ms[lay], "c%d%s" % (k, lay), L[lay], lambda t, i, x=x, y=y, k=k: dict(x=x, y=y, dz=-y * 0.5))
    gl = fx.mat("glint", ICE[3], 8)
    G = [(-14, 30), (12, 24), (-6, 12), (19, 8)]
    fx.still(star4(MB(), 0, 0, 5, 0.15), "glint", gl, lambda t, i: dict(x=G[i][0], y=G[i][1], rot=0.0))
    sn = fx.mat("snow", ICE[3], 7)
    for k in range(5):
        x0 = -20 + 10 * k

        def fn(t, i, x0=x0, k=k):
            q = (t + k / 5) % 1.0
            return (x0 + 2 * math.sin(TAU * q + k), 42 - 30 * q, 1.0 if q < 0.85 else 0.0, 0.0)
        fx.particle("sn%d" % k, sn, MB().diamond(0, 0, 2.0, 2.0), fn)
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
