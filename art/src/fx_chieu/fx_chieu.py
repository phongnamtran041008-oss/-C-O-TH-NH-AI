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


LIGHT_RAMPS = ("spirit", "flame", "ice", "cosmic", "holy", "verdant", "thunder",
               "steel", "stone", "bone", "hair", "blue", "purple", "teal", "jade", "gold")   # = chieu_post.LIGHT
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
    if el == "hoa":            # red-orange, kept apart from kim's pale gold and tho's ochre
        r = [FLAME[0], FLAME[0], FLAME[1], FLAME[2]]
    if el == "tho":            # ochre earth light
        r = ["#573420", "#ad7a48", "#d6a970", "#fff0a0"]
    fx = CFx("tu_khi_" + el, px=96, frames=6, fps=12, loop=True, halo=0.6,
             ramps=(LIGHT_RAMPS + ("wood", "earth")) if el == "tho" else None,
             name_vi="Tụ khí %s" % TU_NAME[el],
             where="qi gathering on the caster while a skill is channelled; pivot = the centre of gathering")
    rng = random.Random(len(el) * 7 + ord(el[0]))
    core_c = {"tho": "#fff0a0", "hoa": FLAME[3]}.get(el, r[3])
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
            s0 = max(0.0, s1 - 0.3)
            if s1 < 0.08:
                continue
            m = 10
            pts = [spiral_pt(a0, turn, R0, s0 + (s1 - s0) * q / m) for q in range(m + 1)]
            if heads:
                x, y = pts[-1]
                mb.disc(x, y, 1.3, 8)
            else:
                curve_strip(mb, pts, 0.3, 1.1 + 0.5 * s1, pw=0.7)
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
                xa = X0 - 8 - 20 * o
                mb.line((xa, yy * (1 - 0.3 * o)), (xa - 12, yy * (1 - 0.3 * o)), 0.9)
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
    born = {k: 0.0 + 0.55 * order.index(k) / N for k in range(N)}
    front = fx.mat("front_body", HOLY[2], 4)
    mats_f = light_sword_layers(fx, "f_", z0=4)
    mats_b = light_sword_layers(fx, "b_", z0=1)
    mats_b["body"] = fx.mat("b_body2", HOLY[1], 2)
    ringm = fx.mat("ring", HOLY[2], 0.5)
    runem = fx.mat("rune", HOLY[1], 0.6)
    glint = fx.mat("glint", WHITE, 7)

    def ring(t, i):
        g = 0.12 + 0.88 * ease_out(ramp_up(t, 0.0, 0.35))
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
            q = (t - tb + 0.1) / 0.22
            if q <= 0 or q >= 1:
                return None
            return (x, y + 8, math.sin(PI * q) * 1.0, 0.0)
        fx.particle("gl%d" % k, glint, star4(MB(), 0, 0, 6, 0.15), fn)
    return fx


@reg("van_kiem_roi")
def van_kiem_roi():
    """the rain: swords streak down and stab into the area, flash, then burst into light."""
    fx = CFx("van_kiem_roi", px=128, pivot=(64, 104), frames=10, fps=16, halo=0.7,
             name_vi="Vạn Kiếm Quy Tông - vạn kiếm rơi",
             where="rain of swords striking the target area (one-shot, ~10 frames); pivot = area centre on the ground")
    rng = random.Random(77)
    N = 16
    RX, RY = 44, 12
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
    TOPY = 101

    def frame_parts(t, i):
        L = new_layers()
        st, stc, fl, rg = MB(), MB(), MB(), MB()
        if 0 <= i <= 6:                                 # countless thinner swords of light behind: the rain itself
            rr = random.Random(300 + i)
            for k in range(14):
                x = rr.uniform(-48, 48)
                y1 = rr.uniform(10, 90)
                L_ = rr.uniform(18, 34)
                st.strip([(x, min(TOPY, y1 + L_)), (x, y1)], [0.4, 2.4], soft=True)
                stc.strip([(x, min(TOPY, y1 + L_ * 0.7)), (x, y1)], [0.2, 0.9])
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
    fill = fx.mat("fill", ICE[1], -1, grad=dict(src="attr", pow=1.0), opacity=0.35)
    fx.still(ring_e(MB(), 0, 0, 52, 52, 14, soft=True), "fill", fill)
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
        x, y = 34 * ca, 34 * sa
        sword(sw, x, y, a, 21, 5.2, guard=False, grip=True)
        gq = [(-1.8, -6.5), (1.8, -6.5), (1.8, 6.5), (-1.8, 6.5)]
        sg.poly(rot_pts(gq, a, x, y))
        blade_core(sc, x, y, a, 21, 5.2)
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
    CY_, RX, RY = 22, 44, 12
    # gold-white swords over the ice-blue domain circle, so the two layers never merge
    trailm = fx.mat("trail", HOLY[1], 0.5, grad=dict(src="attr", pow=1.0), opacity=0.8)
    mats_b = dict(halo=fx.mat("b_halo", HOLY[0], 1, grad=dict(src="attr", pow=1.3), opacity=0.6),
                  body=fx.mat("b_body", HOLY[1], 1.5), guard=fx.mat("b_guard", HOLY[0], 1.6),
                  core=fx.mat("b_core", HOLY[2], 1.7))
    mats_f = dict(halo=fx.mat("f_halo", HOLY[1], 4, grad=dict(src="attr", pow=1.3), opacity=0.8),
                  body=fx.mat("f_body", HOLY[2], 4.5), guard=fx.mat("f_guard", HOLY[1], 4.6),
                  core=fx.mat("f_core", WHITE, 4.7))

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
            s = 0.72 + 0.28 * (0.5 - 0.5 * sa)            # nearer = bigger
            # upright swords of light, tip up, leaning into the direction they travel (a sword cage)
            lean = -0.32 * math.sin(a + PI / 2) * (1 if sa < 0 else -1)
            add_sword(L, x, y - 9 * s, PI / 2 + lean, 22, 4.2, s, 2.0)
            # light trail behind it along the orbit
            tp = [pos(a - 0.06 * q) for q in range(9)]
            tr.strip(tp[::-1], [0.3 + 2.6 * s * (q / 8) for q in range(9)], soft=True)
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
    starh = fx.mat("starh", HOLY[2], 5, grad=dict(src="attr", pow=1.0), opacity=0.7)
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
    fx.still(MB().disc(0, 0, 9, 20, 1.0, 0.0), "starh", starh,
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
# a dragon head in profile: domed brow, long tapering snout with a raised nose, open jaws (the notch is the mouth)
HEAD = [(0, 10), (6, 15), (13, 18), (20, 16), (26, 11), (34, 8), (41, 8), (46, 6), (46, 2), (37, 1), (27, 1),
        (18, -1), (28, -5), (38, -7), (41, -10), (31, -13), (17, -13), (6, -12), (0, -9), (-4, -5), (-5, 1), (-3, 6)]
HEAD_LIT = [(3, 10), (8, 14), (13, 16), (19, 14), (25, 10), (34, 6.5), (41, 6.5), (44, 4.5), (33, 4.5), (22, 6), (10, 7)]
JAW = [(18, -2), (28, -6), (38, -8), (40, -10), (31, -12), (17, -12), (8, -10)]
SOCKET = [(15, 12), (22, 13), (26, 9.5), (19, 8)]


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
    mane = fx.mat("mane", FLAME[1], 5.6)            # over the back of the head: a mane, not a box edge
    manec = fx.mat("manec", FLAME[2], 5.7)

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
    jaw = fx.mat("jaw", FLAME[0], 4.7)
    fx.pf("jaw", jaw, lambda t, i: MB().poly(head_at(t, JAW)).poly(head_at(t, SOCKET))
          .disc(HX + 44, hy(t) + 5, 1.0, 6))                       # shaded lower jaw, eye socket, nostril

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
    fx.pf("eye", eye, lambda t, i: MB().diamond(HX + 21, hy(t) + 11, 7, 3.0, -0.25))

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
    RB = [10, 22, 29, 32, 30, 26, 0, 0]
    HEAT = [1.0, 1.0, 0.85, 0.6, 0.35, 0.18, 0, 0]
    halo = fx.mat("halo", FLAME[1], 0, grad=dict(src="attr", pow=1.1), opacity=0.5)
    outer = fx.mat("outer", FLAME[1], 2)
    mid = fx.mat("mid", FLAME[2], 2.5)
    core = fx.mat("core", FLAME[3], 3)
    ringm = fx.mat("ring", FLAME[2], 1)
    tongm = fx.mat("tongue", FLAME[1], 1.8)
    smoke = fx.mat("smoke", "#888e98", 0.5, grad=dict(src="attr", pow=0.6), opacity=0.5)
    smoke2 = fx.mat("smoke2", "#b8bdc3", 0.6, grad=dict(src="attr", pow=0.8), opacity=0.45)

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
        rr = [0, 28, 38, 44, 48][i]
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
        for k in range(5):                    # one soft cloud of overlapping puffs rising off the blast
            a = TAU * k / 5 + 0.4
            d = 8 + 8 * q
            rad = (13 + 3 * q) * k2
            blob(mb, d * math.cos(a), d * math.sin(a) * 0.6 + 10 + 14 * q, rad, r, 14, 0.15, soft=True)
        return mb
    fx.pf("smoke", smoke, lambda t, i: smk(t, i, 1.0))
    fx.pf("smoke2", smoke2, lambda t, i: smk(t, i, 0.55))
    em = fx.mat("ember", FLAME[3], 5)
    em2 = fx.mat("ember2", FLAME[2], 4.8)
    rng = fx.rng
    for k in range(16):
        a = TAU * k / 16 + rng.uniform(-0.2, 0.2)
        v = rng.uniform(26, 42)

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
    # a ring of spikes round the target (the middle stays clear so the monster is not hidden): tall at the back
    # corners, short in front
    SP = [(-18, 7, 36, 11, -5), (19, 7, 40, 12, 5), (-28, 3, 26, 10, -7), (29, 2, 24, 9, 7), (-35, -3, 14, 7, -5),
          (35, -4, 13, 7, 5), (-12, -8, 12, 8, -3), (11, -9, 11, 8, 3), (0, -11, 8, 7, 0)]
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


# ============================================================================ 6. Địa Liệt Trảm (thổ)
EARTH = ["#26201a", "#47392d", "#6c5a47", "#958065", "#bfab8a"]
WOOD = ["#2c1a10", "#573420", "#82522f", "#ad7a48", "#d6a970"]
GOLD = ["#3a2208", "#7a4c0e", "#b9821a", "#e6b83a", "#fff0a0"]
EARTH_RAMPS = ("earth", "wood", "gold", "holy", "stone", "hair")


def rock_layers(fx, prefix, z0):
    return spike_layers(fx, prefix, z0, body=WOOD[2], facet=WOOD[3], hi=WOOD[4], outl=WOOD[0])


def rock_mb(r, rng, n=7):
    pts = []
    for k in range(n):
        a = TAU * k / n + rng.uniform(-0.2, 0.2)
        rr = r * rng.uniform(0.7, 1.1)
        pts.append((rr * math.cos(a), rr * math.sin(a) * 0.85))
    return pts


@reg("dia_liet")
def dia_liet():
    fx = CFx("dia_liet", px=128, pivot=(8, 64), frames=8, fps=16, ground=True, halo=0.0, ramps=EARTH_RAMPS,
             name_vi="Địa Liệt Trảm - đất nứt",
             where="a fissure racing right along the ground, glowing from inside (one-shot, under the characters); "
                   "pivot = where it starts, it reaches x = +112")
    lip = fx.mat("lip", EARTH[3], 0, opacity=0.85)
    gap = fx.mat("gap", EARTH[0], 1)
    glow = fx.mat("glow", GOLD[3], 2)
    core = fx.mat("core", HOLY[3], 3)
    shaft = fx.mat("shaft", HOLY[2], 4, grad=dict(src="attr", pow=1.0), opacity=0.8)
    r0 = random.Random(21)
    N = 24
    MAIN = [(0.0, 0.0)] + [(112 * k / N + r0.uniform(-1.5, 1.5), r0.uniform(-4.5, 4.5)) for k in range(1, N)] + [(112.0, 0.0)]
    BR = []
    for k in (4, 9, 13, 17, 21):
        x, y = MAIN[k]
        ang = r0.choice((-1, 1)) * r0.uniform(0.35, 0.8)
        L = r0.uniform(8, 15)
        BR.append((k, jag((x, y), (x + L * math.cos(ang), y + L * math.sin(ang) * 0.55), r0, 3, 1.5)))
    HEADF = [0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0]
    WK = [1.0, 1.0, 1.0, 1.0, 1.0, 1.15, 1.05, 0.8]
    GK = [0.8, 0.9, 1.0, 1.0, 1.0, 1.5, 1.2, 0.6]

    def crackmb(i, w0, kk):
        n = max(2, int(round(HEADF[i] * N)))
        pts = MAIN[:n + 1]
        mb = MB()
        ws = [w0 * kk * (0.35 + 0.65 * math.sin(PI * min(1.0, (q + 0.5) / (n + 0.5))) ** 0.5) for q in range(len(pts))]
        ws[-1] = 0.4
        mb.strip(pts, ws)
        for (k, b) in BR:
            if k < n - 1:
                mb.strip(b, [w0 * kk * 0.6, w0 * kk * 0.45, w0 * kk * 0.3, 0.3])
        return mb
    fx.pf("lip", lip, lambda t, i: crackmb(i, 11.0, WK[i]))
    fx.pf("gap", gap, lambda t, i: crackmb(i, 6.5, WK[i]))
    fx.pf("glow", glow, lambda t, i: crackmb(i, 3.0, GK[i]))
    fx.pf("core", core, lambda t, i: crackmb(i, 1.1, GK[i]) if i >= 3 else None)

    def shafts(t, i):                     # light bursting out of the opened crack
        if i < 4 or i > 6:
            return None
        mb = MB()
        r = random.Random(i)
        for k in range(3, N - 1, 3):
            x, y = MAIN[k]
            h = r.uniform(8, 18) * (1.0 if i == 5 else 0.6)
            mb.strip([(x, y), (x + r.uniform(-1, 1), y + h)], [3.2, 0.5], soft=True)
        return mb
    fx.pf("shaft", shaft, shafts)
    # rock chips and dust thrown up at the racing head
    rk = rock_layers(fx, "r", 6)
    dust = fx.mat("dust", EARTH[3], 5, grad=dict(src="attr", pow=0.8), opacity=0.7)

    def dusts(t, i):
        if i > 5:
            return None
        hx = 112 * min(HEADF[i], 1.0)
        mb = MB()
        r = random.Random(i + 40)
        for k in range(3):
            blob(mb, hx - 4 - 5 * k, 3 + 2 * k, 4.5 - k, r, 10, 0.2, soft=True)
        return mb
    fx.pf("dust", dust, dusts)
    rng = fx.rng
    for k in range(10):
        fb = k % 5                       # thrown when the head passes
        hx = 112 * HEADF[fb] - rng.uniform(0, 6)
        vx, vy = rng.uniform(-6, 6), rng.uniform(10, 18)
        pts = rock_mb(rng.uniform(1.6, 2.6), rng)

        def fn(t, i, fb=fb, hx=hx, vx=vx, vy=vy, k=k):
            q = (i - fb) / 2.5
            if q < 0 or q > 1:
                return None
            return (hx + vx * q, 2 + vy * q - 18 * q * q, 1.0, k + q * 3)
        fx.particle("rk%d" % k, rk["b"] if k % 2 else rk["f"], MB().poly(pts), fn)
    return fx


@reg("dia_liet_no")
def dia_liet_no():
    fx = CFx("dia_liet_no", px=96, pivot=(48, 80), frames=8, fps=14, halo=0.0, ramps=EARTH_RAMPS,
             name_vi="Địa Liệt Trảm - đất bùng",
             where="rock slabs and earth light erupting upward (one-shot); pivot = the ground centre")
    dust = fx.mat("dust", EARTH[3], 0, grad=dict(src="attr", pow=0.8), opacity=0.7)
    crk = fx.mat("crk", EARTH[0], 0.5)
    crkg = fx.mat("crkg", GOLD[3], 0.7)
    pil_o = fx.mat("pil_o", GOLD[3], 1, grad=dict(src="attr", pow=1.0), opacity=0.75)
    pil = fx.mat("pil", HOLY[2], 1.3)
    pilc = fx.mat("pilc", HOLY[3], 1.5)
    R = rock_layers(fx, "s", 3)
    # ground cracks radiating from the centre
    r0 = random.Random(8)
    cr, crg = MB(), MB()
    for k in range(7):
        a = TAU * k / 7 + r0.uniform(-0.2, 0.2)
        L = r0.uniform(18, 30)
        p = jag((0, 0), (L * math.cos(a), L * math.sin(a) * KY * 0.7), r0, 4, 2)
        cr.strip(p, [3.0, 2.4, 1.6, 1.0, 0.4])
        crg.strip(p[:4], [1.0, 0.8, 0.5, 0.3])
    fx.still(cr, "crk", crk)
    fx.still(crg, "crkg", crkg, lambda t, i: dict() if 1 <= i <= 5 else None)

    PW = [0.0, 1.0, 1.0, 0.7, 0.45, 0.25, 0.0, 0.0]
    PH = [0, 46, 62, 66, 66, 60, 0, 0]

    def pillar(t, i, w):
        if PW[i] <= 0:
            return None
        h = PH[i]
        return MB().strip([(0, 0), (0, h * 0.5), (0, h)], [w * PW[i], w * PW[i] * 0.9, 0.5], soft=(w > 10))
    fx.pf("pil_o", pil_o, lambda t, i: pillar(t, i, 26))
    fx.pf("pil", pil, lambda t, i: pillar(t, i, 9))
    fx.pf("pilc", pilc, lambda t, i: pillar(t, i, 3.5))
    # rock slabs heave up through the ground around the pillar, then sink back
    SL = [(-17, 4, 24, 11, -6), (16, 5, 27, 12, 6), (-27, -2, 15, 9, -7), (26, -1, 17, 9, 7), (-7, -7, 10, 9, -3),
          (8, -8, 9, 8, 3)]
    for k, (x, y, h, w, lean) in enumerate(SL):
        ms = spike_meshes(h, w, lean)

        def fn(t, i, k=k, x=x, y=y):
            q = ramp_up(t, 0.02 * k, 0.02 * k + 0.2)
            if q <= 0:
                return None
            sy = ease_out(q) * (1 + 0.12 * bump(q, 0.5, 1.01))
            if i >= 5:
                sy *= [0.8, 0.5, 0.22][i - 5]
            return dict(x=x, y=y, sy=max(sy, 0.05), sx=1.0, dz=(10 - y) * 0.5)
        for lay in ("o", "b", "f", "h"):
            fx.still(ms[lay], "sl%d%s" % (k, lay), R[lay], fn)

    def dust_(t, i):
        if i < 1:
            return None
        q = (i - 1) / 6
        mb = MB()
        r = random.Random(5)
        for k in range(10):
            a = TAU * k / 10
            d = 18 + 18 * ease_out(q)
            blob(mb, d * math.cos(a), d * math.sin(a) * KY * 0.7 + 3 + 6 * q, (6 + 3 * q) * (1 - 0.4 * q), r, 10, 0.2,
                 soft=True)
        return mb
    fx.pf("dust", dust, dust_)
    rc = rock_layers(fx, "c", 7)
    rng = fx.rng
    for k in range(12):
        a = rng.uniform(0.25, PI - 0.25)
        v = rng.uniform(26, 44)
        pts = rock_mb(rng.uniform(2.0, 3.4), rng)

        def fn(t, i, a=a, v=v, k=k):
            q = ramp_up(t, 0.08, 1.0)
            if q <= 0:
                return None
            x = v * 0.75 * math.cos(a) * q
            y = 6 + v * 1.6 * math.sin(a) * q - 66 * q * q
            if y < -4:
                return None
            return (x, y, 1.0, k + 5 * q)
        fx.particle("o%d" % k, rc["o"], MB().poly(offset_poly(pts, 1.2)), fn)
        fx.particle("c%d" % k, rc["b"] if k % 3 else rc["f"], MB().poly(pts), fn)
    return fx


# ============================================================================ 7. Thanh Đằng Triền (mộc)
LEAF = ["#10200f", "#22401c", "#3a6a26", "#5e9432", "#9cc452"]
VINE_RAMPS = ("leaf", "jade", "verdant", "earth", "holy", "bone")


def vine_mats(fx, prefix, z0):
    return dict(o=fx.mat(prefix + "o", LEAF[0], z0), b=fx.mat(prefix + "b", LEAF[2], z0 + 0.2),
                h=fx.mat(prefix + "h", VERD[2], z0 + 0.4), lo=fx.mat(prefix + "lo", LEAF[0], z0 + 0.6),
                l=fx.mat(prefix + "l", VERD[1], z0 + 0.8), th=fx.mat(prefix + "th", LEAF[0], z0 + 0.7))


def vine_add(M, pts, w0, w1, leaves=(), thorns=0, rng=None):
    """one vine along pts into the layer meshes M (o, b, h, lo, l, th)."""
    n = len(pts) - 1
    if n < 1:
        return
    ws = [w0 + (w1 - w0) * (k / n) for k in range(n + 1)]
    M["o"].strip(pts, [w + 2.2 for w in ws])
    M["b"].strip(pts, ws)
    hp = []
    for k in range(n + 1):                    # a lit edge on the upper-left side
        x0, y0 = pts[max(0, k - 1)]
        x1, y1 = pts[min(n, k + 1)]
        L = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        if nx > 0 or (nx == 0 and ny < 0):
            nx, ny = -nx, -ny
        hp.append((pts[k][0] + nx * ws[k] * 0.28, pts[k][1] + ny * ws[k] * 0.28))
    M["h"].strip(hp, [max(0.6, w * 0.3) for w in ws])
    for (u, side, L) in leaves:
        k = int(u * n)
        if k >= n:
            continue
        x, y = pts[k]
        x1, y1 = pts[k + 1]
        ang = math.atan2(y1 - y, x1 - x) + side * 1.0
        leaf(M["lo"], x, y, ang, L + 2, L * 0.55 + 2)
        leaf(M["l"], x + math.cos(ang) * 1.0, y + math.sin(ang) * 1.0, ang, L, L * 0.55)
    if thorns and rng:
        for j in range(thorns):
            k = int((j + 0.5) / thorns * n)
            if k >= n:
                continue
            x, y = pts[k]
            x1, y1 = pts[k + 1]
            ang = math.atan2(y1 - y, x1 - x) + (1 if j % 2 else -1) * 1.2
            w = ws[k] * 0.5
            M["th"].poly([(x - math.sin(ang) * 0.9, y + math.cos(ang) * 0.9), (x + math.sin(ang) * 0.9, y - math.cos(ang) * 0.9),
                          (x + math.cos(ang) * (w + 2.5), y + math.sin(ang) * (w + 2.5))])


def new_vine():
    return dict(o=MB(), b=MB(), h=MB(), lo=MB(), l=MB(), th=MB())


@reg("thanh_dang")
def thanh_dang():
    fx = CFx("thanh_dang", px=96, pivot=(48, 78), frames=8, fps=12, halo=0.0, ramps=VINE_RAMPS,
             name_vi="Thanh Đằng Triền - dây leo trồi lên",
             where="vines bursting out of the ground in a patch and curling up (one-shot); pivot = the patch centre")
    soil = fx.mat("soil", EARTH[1], 0, grad=dict(src="attr", pow=0.7), opacity=0.7)
    fx.still(MB().disc(0, 0, 32, 28, 1.0, 0.0, KY * 0.5), "soil", soil,
             lambda t, i: dict(s=0.5 + 0.5 * ease_out(ramp_up(t, 0, 0.3))))
    # base x, base y (depth), height, curl side, start time
    # vines rise round the target and lean in to grab it; the middle stays clear, front vines short
    VS = [(-24, 5, 42, 1, 0.0), (24, 4, 46, -1, 0.04), (-32, -1, 30, 1, 0.1), (32, -2, 28, -1, 0.12),
          (-14, -7, 16, 1, 0.18), (14, -8, 15, -1, 0.2), (0, -10, 11, 1, 0.24)]
    VS.sort(key=lambda v: -v[1])
    layers = [vine_mats(fx, "v%d" % k, 1 + 1.2 * k) for k in range(len(VS))]

    def path(k, t, g):
        x, y, H, side, t0 = VS[k]
        sway = 2.2 * math.sin(TAU * t * 1.0 + k)
        p = bezier((x, y), (x - side * 6, y + H * 0.35), (x + side * 10 + sway, y + H * 0.7), (x + side * 4 + sway, y + H), 18)
        # curl at the tip: a small spiral
        cx, cy = p[-1][0] - side * 4, p[-1][1]
        for q in range(1, 9):
            a = (0 if side > 0 else PI) + side * PI * q / 6
            rr = 4.0 * (1 - q / 11)
            p.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        n = max(2, int(len(p) * g))
        return p[:n]

    def build(k, t, i):
        x, y, H, side, t0 = VS[k]
        g = ease_out(ramp_up(t, t0, t0 + 0.5))
        if g <= 0.02:
            return None
        M = new_vine()
        pts = path(k, t, g)
        r = random.Random(k)
        lv = [(0.3, 1, 6), (0.5, -1, 7), (0.7, 1, 5.5)]
        lv = [(u * len(pts) / 26, s, L * min(1.0, g * 1.4)) for u, s, L in lv if u * 26 < len(pts) - 1]
        vine_add(M, pts, 5.2, 1.3, lv, thorns=4, rng=r)
        return M
    cache = {}
    for k in range(len(VS)):
        for lay in ("o", "b", "h", "lo", "l", "th"):
            def b(t, i, k=k, lay=lay):
                key = (k, i)
                if key not in cache:
                    cache[key] = build(k, t, i)
                M = cache[key]
                return None if M is None else M[lay]
            fx.pf("v%d%s" % (k, lay), layers[k][lay], b)
    # dirt bursting at the roots, glowing green motes
    rk = rock_layers(fx, "d", 12)
    rng = fx.rng
    for k in range(8):
        v = VS[k % len(VS)]
        vx, vy = rng.uniform(-10, 10), rng.uniform(8, 14)

        def fn(t, i, v=v, vx=vx, vy=vy, k=k):
            q = (t - v[4]) / 0.35
            if q < 0 or q > 1:
                return None
            y = v[1] + vy * q - 16 * q * q
            if y < v[1] - 2:                  # back on the ground: gone
                return None
            return (v[0] + vx * q, y, 1.0, k + 4 * q)
        fx.particle("dirt%d" % k, rk["b"], MB().poly(rock_mb(1.8, rng)), fn)
    mo = fx.mat("mote", VERD[3], 14)
    for k in range(7):
        x0 = rng.uniform(-24, 24)

        def fn(t, i, x0=x0, k=k):
            q = (t - 0.3 - 0.05 * k) / 0.6
            if q < 0 or q > 1:
                return None
            return (x0 + 3 * math.sin(TAU * q + k), 8 + 40 * q, math.sin(PI * q) * 1.1, D(45))
        fx.particle("mo%d" % k, mo, MB().diamond(0, 0, 2.8, 2.8), fn)
    return fx


@reg("thanh_dang_troi")
def thanh_dang_troi():
    fx = CFx("thanh_dang_troi", px=64, pivot=(32, 56), frames=4, fps=8, loop=True, halo=0.0, ramps=VINE_RAMPS,
             name_vi="Thanh Đằng Triền - dây leo trói",
             where="vines wrapped around a held monster (loop, drawn over it); pivot = the monster's feet; made for a "
                   "48 px monster, scale by monster frame / 48")
    BANDS = [((-21, 3), (-6, 13), (8, 5), (21, 13)), ((20, 15), (6, 23), (-8, 17), (-20, 26)),
             ((-17, 28), (-4, 36), (8, 29), (17, 36))]
    POSTS = [((-20, -1), (-25, 8), (-22, 18), (-21, 3)), ((20, -1), (25, 6), (22, 11), (20, 15))]
    M_back = vine_mats(fx, "p", 1)
    M_front = vine_mats(fx, "f", 3)

    def build(t, i, front):
        M = new_vine()
        sq = 0.6 * math.sin(TAU * t)
        r = random.Random(3)
        if not front:
            for k, (a, b, c, d) in enumerate(POSTS):
                vine_add(M, bezier(a, b, c, d, 10), 4.6, 3.6, [(0.5, 1 if k else -1, 5)])
            return M
        for k, (a, b, c, d) in enumerate(BANDS):
            pts = bezier(a, (b[0], b[1] - sq), (c[0], c[1] + sq), d, 16)
            w = 3.8 + 0.5 * math.sin(TAU * t + k)
            lv = [(0.35, 1, 5 + 0.6 * math.sin(TAU * t + k)), (0.75, -1, 4.5)]
            vine_add(M, pts, w * 0.7, w, lv, thorns=3, rng=r)
        return M
    for front, mats in ((False, M_back), (True, M_front)):
        for lay in ("o", "b", "h", "lo", "l", "th"):
            fx.pf(("f" if front else "p") + lay, mats[lay], (lambda fr, ly: (lambda t, i: build(t, i, fr)[ly]))(front, lay))
    mo = fx.mat("mote", VERD[3], 8)
    for k in range(4):
        x0 = [-14, 10, -4, 16][k]

        def fn(t, i, x0=x0, k=k):
            q = (t + k / 4) % 1.0
            return (x0, 10 + 30 * q, math.sin(PI * q), D(45))
        fx.particle("mo%d" % k, mo, MB().diamond(0, 0, 2.6, 2.6), fn)
    return fx


# ============================================================================ 11. Hồi Xuân Thuật (mộc, heal)
@reg("hoi_xuan")
def hoi_xuan():
    fx = CFx("hoi_xuan", px=96, pivot=(48, 84), frames=10, fps=12, halo=0.0, ramps=VINE_RAMPS + ("teal",),
             name_vi="Hồi Xuân Thuật",
             where="healing: a rising swirl of green life light with leaves and petals (one-shot); pivot = the feet")
    ring = fx.mat("ring", VERD[2], 1)
    fill = fx.mat("fill", VERD[1], 0, grad=dict(src="attr", pow=0.8), opacity=0.55)
    rib_b = fx.mat("rib_b", VERD[1], 1.5, opacity=0.75)
    rib_f = fx.mat("rib_f", VERD[2], 5)
    rib_c = fx.mat("rib_c", VERD[3], 5.5)
    lf_o = fx.mat("lf_o", LEAF[1], 6)
    lf = fx.mat("lf", "#4fa678", 6.3)
    pet = fx.mat("petal", "#f6f4f7", 7)
    gold = fx.mat("gold", HOLY[2], 7.5)
    bloom = fx.mat("bloom", VERD[3], 4, grad=dict(src="attr", pow=1.0), opacity=0.9)
    bloomc = fx.mat("bloomc", "#f6f4f7", 4.5)
    RS = [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.7, 0.4]
    fx.still(ring_e(MB(), 0, 0, 25, 25 * KY * 0.55, 1.6), "ring", ring, lambda t, i: dict(s=RS[i]))
    fx.still(MB().disc(0, 0, 25, 28, 0.0, 1.0, KY * 0.55), "fill", fill, lambda t, i: dict(s=RS[i]) if i < 9 else None)
    HEADS = [0.15, 0.32, 0.5, 0.66, 0.8, 0.92, 1.02, 1.12, 1.24, 1.36]

    def helix(k, s, t):
        a = TAU * k / 3 + 2.4 * PI * s + 1.2 * t
        r = 21 * (1 - 0.45 * s)
        return r * math.cos(a), 2 + 66 * s + r * math.sin(a) * 0.3, math.sin(a)

    def ribbons(t, i, front, w):
        mb = MB()
        hd = HEADS[i]
        tl = max(0.0, hd - 0.55)
        for k in range(3):
            seg = []
            m = 26
            for q in range(m + 1):
                s = tl + (min(hd, 1.0) - tl) * q / m
                if s > 1.0:
                    break
                x, y, sn = helix(k, s, t)
                if (sn < 0) == front:
                    seg.append((x, y, q / m))
                else:
                    if len(seg) > 1:
                        mb.strip([(a, b) for a, b, _ in seg], [w * (0.3 + 0.7 * u) for _, _, u in seg])
                    seg = []
            if len(seg) > 1:
                mb.strip([(a, b) for a, b, _ in seg], [w * (0.3 + 0.7 * u) for _, _, u in seg])
        return mb if mb.v else None
    fx.pf("rib_b", rib_b, lambda t, i: ribbons(t, i, False, 1.8) if i < 9 else None)
    fx.pf("rib_f", rib_f, lambda t, i: ribbons(t, i, True, 3.0) if i < 9 else None)
    fx.pf("rib_c", rib_c, lambda t, i: ribbons(t, i, True, 1.0) if i < 9 else None)
    # the bloom of life at the chest
    BL = [0, 0, 0, 0.5, 1.0, 1.15, 1.0, 0.7, 0.35, 0]

    def bl(t, i, core_):
        if BL[i] <= 0:
            return None
        mb = MB()
        for k in range(5):
            a = PI / 2 + TAU * k / 5 + 0.15 * i
            if core_:
                leaf(mb, 0, 30, a, 7 * BL[i], 3.4 * BL[i])
            else:
                leaf(mb, 0, 30, a, 13 * BL[i], 7 * BL[i])
        if core_:
            mb.disc(0, 30, 2.4 * BL[i], 10)
        return mb
    fx.pf("bloom", bloom, lambda t, i: bl(t, i, False))
    fx.pf("bloomc", bloomc, lambda t, i: bl(t, i, True))
    rng = fx.rng
    for k in range(9):                    # leaves riding up the swirl
        t0 = 0.05 + 0.05 * k
        a0 = rng.uniform(0, TAU)

        def fn(t, i, t0=t0, a0=a0, k=k):
            q = (t - t0) / 0.6
            if q < 0 or q > 1:
                return None
            a = a0 + 3.2 * q
            r = 22 * (1 - 0.4 * q)
            return (r * math.cos(a), 4 + 62 * q + r * math.sin(a) * 0.3, min(1.0, 4 * (1 - q)), a + PI / 2)
        lm = MB()
        leaf(lm, -3.5, 0, 0, 7, 3.6)
        lo = MB()
        leaf(lo, -4.5, 0, 0, 9, 5.4)
        fx.particle("lfo%d" % k, lf_o, lo, fn)
        fx.particle("lf%d" % k, lf, lm, fn)
    for k in range(10):                   # white petals and golden motes drifting up
        t0 = 0.2 + 0.05 * k
        x0 = rng.uniform(-22, 22)

        def fn(t, i, t0=t0, x0=x0, k=k):
            q = (t - t0) / 0.5
            if q < 0 or q > 1:
                return None
            return (x0 + 4 * math.sin(TAU * q + k), 10 + 50 * q + 4 * k % 7, math.sin(PI * min(1, q * 1.4)), 0.5 * k + q)
        fx.particle("pt%d" % k, pet if k % 2 else gold,
                    MB().diamond(0, 0, 3.6, 2.2) if k % 2 else star4(MB(), 0, 0, 2.6, 0.22), fn)
    return fx


# ============================================================================ 8. Phong Nhận Thuật (wind)
WIND = ["#1f6e70", "#2f9c9a", "#4cc2b6", "#9ae6d6", "#f6f4f7"]
WIND_RAMPS = ("teal", "bone", "ice", "spirit", "jade", "steel")


@reg("phong_nhan")
def phong_nhan():
    fx = CFx("phong_nhan", px=64, frames=4, fps=16, loop=True, halo=0.0, ramps=WIND_RAMPS,
             name_vi="Phong Nhận Thuật - phong nhận",
             where="one wind blade, a pale crescent of air flying right (projectile, loop; fire 3-5 in a fan); "
                   "pivot = frame centre")
    CXc, R = -16, 26
    a0, a1 = D(62), D(-62)
    soft = fx.mat("soft", WIND[2], 0, grad=dict(src="attr", pow=1.0), opacity=0.6)
    out = fx.mat("out", WIND[1], 1)
    body = fx.mat("body", WIND[3], 2)
    core = fx.mat("core", WIND[4], 3)
    streak = fx.mat("streak", WIND[3], 1.5, opacity=0.75)

    def cres(t, i, k, off=0.0):
        n = 24
        fl = 1 + 0.06 * math.sin(TAU * t)
        pts, ws = [], []
        for q in range(n + 1):
            u = q / n
            a = a0 + (a1 - a0) * u
            pts.append((CXc + (R + off) * math.cos(a), (R + off) * math.sin(a)))
            ws.append(7.0 * k * fl * math.sin(PI * u) ** 0.8 + 0.3)
        return MB().strip(pts, ws, soft=(k > 1.2))
    fx.pf("soft", soft, lambda t, i: cres(t, i, 2.0, -2))
    fx.pf("out", out, lambda t, i: cres(t, i, 1.0, 0))
    fx.pf("body", body, lambda t, i: cres(t, i, 0.68, 0.6))
    fx.pf("core", core, lambda t, i: cres(t, i, 0.25, 2.0))

    def streaks(t, i):
        mb = MB()
        for k, (rr, ua, ub) in enumerate(((R - 7, 0.15, 0.85), (R - 12, 0.25, 0.75), (R - 17, 0.32, 0.68), (R + 5, 0.2, 0.8))):
            o = (t + k * 0.27) % 1.0
            pts = []
            for q in range(13):
                u = ua + (ub - ua) * q / 12
                a = a0 + (a1 - a0) * u
                pts.append((CXc - 4 * o + rr * math.cos(a) - 3 * o, rr * math.sin(a)))
            mb.strip(pts, [0.3 + 1.1 * math.sin(PI * q / 12) * (1 - 0.5 * o) for q in range(13)])
        # tip curls: tiny swirls where the blade's horns are
        for sgn in (1, -1):
            x, y = CXc + R * math.cos(a0) - 1, sgn * R * math.sin(a0)
            pts = [(x - 3 * q / 6 - 2 * math.sin(PI * q / 6 + TAU * t), y - sgn * (2.5 * math.sin(PI * q / 6))) for q in range(7)]
            mb.strip(pts, [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3])
        return mb
    fx.pf("streak", streak, streaks)
    return fx


@reg("phong_xoay")
def phong_xoay():
    fx = CFx("phong_xoay", px=64, pivot=(32, 58), frames=7, fps=16, halo=0.0, ramps=WIND_RAMPS + ("leaf", "earth"),
             name_vi="Phong Nhận Thuật - lốc xoáy",
             where="a small whirlwind where the wind blade lands (one-shot); pivot = the ground point")
    back = fx.mat("back", WIND[1], 1, opacity=0.75)
    front = fx.mat("front", WIND[3], 3)
    frontc = fx.mat("frontc", WIND[4], 3.5)
    base = fx.mat("base", WIND[2], 0.5, grad=dict(src="attr", pow=0.8), opacity=0.6)
    LV = 7
    SHOW = [3, 5, 7, 7, 7, 7, 5]
    SPREAD = [1.0, 1.0, 1.0, 1.05, 1.1, 1.3, 1.5]
    THIN = [1.0, 1.0, 1.0, 1.0, 0.85, 0.6, 0.4]

    def level(t, i, fr, w):
        mb = MB()
        for j in range(min(SHOW[i], LV)):
            y = 3 + 6.6 * j + (2 * (i - 4) if i > 4 else 0)
            r = (4 + 3.2 * j) * SPREAD[i]
            ph = 1.6 * i + 0.7 * j
            for seg in range(2):
                sa = ph + PI * seg
                aa = [sa + 0.85 * PI * q / 10 for q in range(11)]
                pts = [(r * math.cos(a) + 1.2 * math.sin(j * 0.9 + i), y + r * 0.28 * math.sin(a)) for a in aa]
                fr_flags = [math.sin(a) < 0 for a in aa]
                sel = [p for p, f in zip(pts, fr_flags) if f == fr]
                if len(sel) > 1:
                    mb.strip(sel, [w * THIN[i] * (0.4 + 0.6 * math.sin(PI * q / max(1, len(sel) - 1))) + 0.2
                                   for q in range(len(sel))])
        return mb if mb.v else None
    fx.pf("back", back, lambda t, i: level(t, i, False, 1.5))
    fx.pf("front", front, lambda t, i: level(t, i, True, 2.4))
    fx.pf("frontc", frontc, lambda t, i: level(t, i, True, 0.8))
    fx.still(MB().disc(0, 0, 13, 20, 1.0, 0.0, 0.3), "base", base,
             lambda t, i: dict(s=[0.6, 1.0, 1.1, 1.1, 1.1, 1.2, 0.9][i]))
    lf_ = fx.mat("leafbit", LEAF[3], 4)
    db = fx.mat("dustbit", EARTH[3], 4)
    for k in range(6):
        a0 = TAU * k / 6
        y0 = 6 + 6 * k

        def fn(t, i, a0=a0, y0=y0, k=k):
            a = a0 + 2.0 * i
            r = (6 + 2.4 * y0 / 6) * SPREAD[i] + 3
            if i > 5 and k % 2:
                return None
            return (r * math.cos(a), y0 + r * 0.28 * math.sin(a) + 2 * i * (i > 4), 1.0, a)
        fx.particle("bit%d" % k, lf_ if k % 2 else db,
                    leaf(MB(), -2, 0, 0, 4, 2) if k % 2 else MB().poly([(-1.2, -1), (1.3, -0.8), (0.6, 1.2)]), fn)
    return fx


# ============================================================================ 9. Kim Chung Tráo (golden bell)
BELL_R = [(22, 0), (19.5, 3), (17.5, 8), (16.6, 18), (16.2, 30), (15.4, 41), (13.6, 49), (10, 55), (5, 58.5), (0, 60)]


def bell_outline():
    """closed polygon of the bell (lip at y=0, crown at y=60)."""
    right = BELL_R
    left = [(-x, y) for x, y in BELL_R[::-1]][1:]
    return right + left


def bell_rim_side(g, side):
    """polyline along one side of the bell from the lip up to fraction g of the way to the crown."""
    n = len(BELL_R) - 1
    m = g * n
    pts = []
    for k in range(n + 1):
        if k <= m:
            x, y = BELL_R[k]
            pts.append((side * x, y))
        else:
            x0, y0 = BELL_R[k - 1]
            x1, y1 = BELL_R[k]
            f = m - (k - 1)
            pts.append((side * (x0 + (x1 - x0) * f), y0 + (y1 - y0) * f))
            break
    return pts


def bell_hw(y):
    for (x0, y0), (x1, y1) in zip(BELL_R, BELL_R[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return 0.0


def bell_band(mb, y, w, inset=0.6):
    hw = bell_hw(y) - inset
    pts = [(-hw + 2 * hw * q / 10, y - 1.6 * math.sin(PI * q / 10)) for q in range(11)]    # curved: a cylinder seen a bit from above
    mb.strip(pts, [w] * 11)
    return mb


def bell_runes(mb, ph, y0=33, y1=40, n=8):
    """abstract rune strokes on the bell's waist, sliding round the cylinder with phase ph."""
    r = random.Random(12)
    for k in range(n):
        th = TAU * k / n + ph
        c = math.cos(th)
        if c < 0.2:
            continue
        hw = bell_hw((y0 + y1) / 2) - 2
        x = hw * math.sin(th)
        rr = random.Random(100 + k)
        rune_marks(mb, [(x, (y0 + y1) / 2 - 1.2 * c, 0.0)], 5.0 * (0.55 + 0.45 * c), rr, 0.9)
    return mb


@reg("kim_chung")
def kim_chung():
    fx = CFx("kim_chung", px=96, pivot=(48, 86), frames=8, fps=14, halo=0.0,
             name_vi="Kim Chung Tráo - chuông vàng hiện",
             where="the golden bell of light forming over the caster (one-shot, then kim_chung_tru); pivot = the feet")
    circ = fx.mat("circ", HOLY[2], 0.5)
    runes = fx.mat("runes", HOLY[1], 0.6)
    ray = fx.mat("ray", HOLY[3], 1, grad=dict(src="attr", pow=1.0), opacity=0.85)
    fill = fx.mat("fill", HOLY[2], 0, opacity=0.3)
    rim = fx.mat("rim", HOLY[2], 2)
    rimc = fx.mat("rimc", WHITE, 2.5)
    band = fx.mat("band", HOLY[1], 2.2)
    star = fx.mat("star", WHITE, 4)
    G = [0.0, 0.35, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0]
    FO = [0, 0, 0, 0.75, 0.55, 0.4, 0.3, 0.3]
    CS = [1.0, 1.0, 0.9, 0.8, 0, 0, 0, 0]
    fx.still(ring_e(ring_e(MB(), 0, 0, 27, 27 * KY * 0.5, 1.6), 0, 0, 21, 21 * KY * 0.5, 1.0), "circ", circ,
             lambda t, i: dict(s=[0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0][i]))
    rb = MB()
    for k in range(10):
        a = TAU * k / 10
        rune_marks(rb, [(24 * math.cos(a), 24 * KY * 0.5 * math.sin(a), 0.0)], 3.2, random.Random(k), 0.8)
    fx.still(rb, "runes", runes, lambda t, i: dict() if i < 6 else None)

    def rays(t, i):
        if not 1 <= i <= 3:
            return None
        mb = MB()
        for k in range(9):
            x = -20 + 5 * k
            h = 60 * G[i] + 6
            mb.strip([(x, 0), (x * 0.8, h)], [2.6, 0.4], soft=True)
        return mb
    fx.pf("ray", ray, rays)
    fx.still(MB().poly(bell_outline()), "fill", fill, lambda t, i: dict(op=FO[i]) if FO[i] else None)

    def rimmb(t, i, w):
        g = G[i]
        if g <= 0:
            return None
        mb = MB()
        L, Rr = bell_rim_side(g, -1), bell_rim_side(g, 1)
        mb.strip(L, [w] * len(L))
        mb.strip(Rr, [w] * len(Rr))
        if g >= 1:
            ring_e(mb, 0, 63, 3, 3, w * 0.8)
        return mb
    fx.pf("rim", rim, lambda t, i: rimmb(t, i, 2.2))
    fx.pf("rimc", rimc, lambda t, i: rimmb(t, i, 0.8))

    def bands(t, i):
        if i < 3:
            return None
        mb = MB()
        bell_band(mb, 3, 1.6)
        bell_band(mb, 30, 1.2)
        bell_band(mb, 43, 1.2)
        bell_runes(mb, 0.0)
        return mb
    fx.pf("band", band, bands)
    fx.still(star4(MB(), 0, 0, 14, 0.1), "star", star,
             lambda t, i: dict(x=-9, y=50, s=[0, 0, 0, 1.0, 0.6, 0.2, 0, 0][i], rot=0.0) if 3 <= i <= 5 else None)
    return fx


@reg("kim_chung_tru")
def kim_chung_tru():
    fx = CFx("kim_chung_tru", px=96, pivot=(48, 86), frames=6, fps=8, loop=True, halo=0.0,
             name_vi="Kim Chung Tráo - chuông vàng hộ thể",
             where="the golden bell standing over the caster, translucent (loop); pivot = the feet")
    fill = fx.mat("fill", HOLY[2], 0, opacity=0.28)
    sweep = fx.mat("sweep", HOLY[3], 0.5, opacity=0.45)
    spec = fx.mat("spec", WHITE, 1, opacity=0.5)
    band = fx.mat("band", HOLY[1], 2)
    rim = fx.mat("rim", HOLY[2], 2.5)
    rimc = fx.mat("rimc", WHITE, 3)
    circ = fx.mat("circ", HOLY[2], -0.5)
    fx.still(ring_e(MB(), 0, 0, 25, 25 * KY * 0.45, 1.2), "circ", circ)
    fx.still(MB().poly(bell_outline()), "fill", fill)

    def sw(t, i):
        y = 4 + 52 * t
        hw = bell_hw(y) - 0.8
        if hw <= 1:
            return None
        return MB().strip([(-hw, y), (hw, y)], [4.0, 4.0])
    fx.pf("sweep", sweep, sw)
    fx.still(MB().strip([(-11, 9), (-11.5, 30), (-10, 46)], [2.4, 2.6, 1.6]), "spec", spec)

    def bands(t, i):
        mb = MB()
        bell_band(mb, 3, 1.6)
        bell_band(mb, 30, 1.1)
        bell_band(mb, 43, 1.1)
        bell_runes(mb, TAU / 8 * t)
        return mb
    fx.pf("band", band, bands)
    full = bell_outline() + [bell_outline()[0]]
    fx.still(MB().strip(BELL_R[::-1] + [(-x, y) for x, y in BELL_R][1:], [2.0] * (2 * len(BELL_R) - 1))
             .merge(ring_e(MB(), 0, 63, 3, 3, 1.6)), "rim", rim)
    fx.still(MB().strip(BELL_R[::-1] + [(-x, y) for x, y in BELL_R][1:], [0.7] * (2 * len(BELL_R) - 1)), "rimc", rimc,
             lambda t, i: dict(s=1.0))
    gl = fx.mat("glint", WHITE, 5)
    fx.still(star4(MB(), 0, 0, 5, 0.15), "glint", gl,
             lambda t, i: dict(x=[-12, -15, 13, 15, -6, 8][i], y=[50, 20, 44, 14, 57, 30][i],
                               s=[1.0, 0.0, 0.8, 0.0, 0.9, 0.0][i], rot=0.0) if i % 2 == 0 else None)
    return fx


@reg("kim_chung_vang")
def kim_chung_vang():
    fx = CFx("kim_chung_vang", px=96, pivot=(48, 86), frames=6, fps=18, halo=0.0,
             name_vi="Kim Chung Tráo - chuông rung",
             where="ring of light when the bell takes a blow (one-shot, over kim_chung_tru); pivot = the feet")
    rimf = fx.mat("rimf", WHITE, 3)
    rim = fx.mat("rim", HOLY[3], 2.5)
    rip = fx.mat("rip", HOLY[2], 2)
    ripc = fx.mat("ripc", WHITE, 2.2)
    inner = fx.mat("inner", HOLY[3], 1, opacity=0.5)
    W = [2.6, 2.2, 1.4, 0.9, 0, 0]
    rimpath = BELL_R[::-1] + [(-x, y) for x, y in BELL_R][1:]
    fx.pf("rimf", rimf, lambda t, i: MB().strip(rimpath, [W[i]] * len(rimpath)) if i < 2 else None)
    fx.pf("rim", rim, lambda t, i: MB().strip(rimpath, [W[i]] * len(rimpath)) if 2 <= i < 4 else None)

    def rings(t, i, w0):
        mb = MB()
        for k, delay in enumerate((0, 1.5)):
            q = (i - delay) / 4.5
            if q < 0 or q > 1:
                continue
            rx = 22 + 19 * ease_out(q)
            ring_e(mb, 0, 28, rx, rx * 0.3, w0 * (1 - 0.75 * q) + 0.3)
        return mb if mb.v else None
    fx.pf("rip", rip, lambda t, i: rings(t, i, 3.0))
    fx.pf("ripc", ripc, lambda t, i: rings(t, i, 1.0))

    def ripples(t, i):
        if i > 3:
            return None
        mb = MB()
        for sgn in (1, -1):
            y = 28 + sgn * (4 + 7 * i)
            if 2 < y < 56:
                bell_band(mb, y, 1.4 - 0.25 * i, inset=1.5)
        return mb
    fx.pf("inner", inner, ripples)
    sp = fx.mat("spark", HOLY[3], 4)
    for k in range(10):
        a = TAU * k / 10 + 0.2
        def fn(t, i, a=a):
            q = ramp_up(t, 0.0, 0.85)
            if q >= 1:
                return None
            d = 20 + 22 * ease_out(q)
            return (d * math.cos(a), 30 + d * 0.6 * math.sin(a), (1 - q) ** 0.5, a)
        fx.particle("sp%d" % k, sp, MB().diamond(0, 0, 4, 1.3), fn)
    return fx


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
