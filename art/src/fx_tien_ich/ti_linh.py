"""C. Linh can awakening.  A cultivator lays a hand on the Trac Linh Thach and a light answers.
Nine giai (1 Pham .. 9 Hon Don): `linh_can_<n>` = the one-shot reveal burst (11 frames, 12 fps), and
`linh_can_tru_<n>` = the looping pillar / aura that stays afterwards (8 frames, 10 fps).
128 px frames, pivot (64, 108) = the base of the stone; the light comes out of the stone's face, Y0 = 1.0 unit
(28.6 px) above the pivot.  The LAST burst frame equals the pillar's steady state so the game can hand over.

Ladder (weak -> strong) by hue AND structure:
 1 grey flicker only | 2 ochre low glow + ground ring | 3 blue column + 2 rings + short rays
 4 purple column + blades + rune ring | 5 gold tall column + orbiting halo + crown + 3 rings
 6 white-gold fan of beams + big halo + whiteout | 7 jade-cyan helix + lotus petals
 8 flame column + ring of flames | 9 cosmic vortex, stars, cracks, screen-filling whiteout."""
import math
from tilib import *

REG = {}
Y0 = 1.0
VI = ["", "Phàm", "Hoàng", "Huyền", "Địa", "Thiên", "Thánh", "Tiên", "Thần", "Hỗn Độn"]
ID = ["", "pham", "hoang", "huyen", "dia", "thien", "thanh", "tien", "than", "hon_don"]
# colours: body (glow edge), mid, core; snapped to the glow ramps by the post step
CFG = {
    1: dict(c=("#8a8f9c", "#b8bdc3", "#f6f4f7"), TH=0.0, W=0.0, fl=0.42, rings=0, rr=0.0, rays=0, rl=0.0, motes=3, kind="disc"),
    2: dict(c=("#c8861a", "#ffae3a", "#fff2b0"), TH=0.95, W=0.55, fl=0.6, rings=1, rr=1.1, rays=0, rl=0.0, motes=4, kind="disc"),
    3: dict(c=("#4a86d0", "#b0dcff", "#f2fbff"), TH=1.5, W=0.7, fl=0.75, rings=2, rr=1.35, rays=6, rl=0.7, motes=6, kind="diamond"),
    4: dict(c=("#8a3ce0", "#c88cff", "#f6e6ff"), TH=1.95, W=0.82, fl=0.9, rings=2, rr=1.55, rays=8, rl=1.0, motes=8, kind="star"),
    5: dict(c=("#e8b02a", "#ffe27a", "#fffbe4"), TH=2.5, p=0.5, W=0.95, fl=1.05, rings=3, rr=1.62, rays=10, rl=1.4, motes=9, kind="star"),
    6: dict(c=("#ffd45a", "#fff2b0", "#ffffff"), TH=2.55, p=0.45, W=1.2, fl=1.2, rings=3, rr=1.68, rays=12, rl=1.7, motes=10, kind="star8"),
    7: dict(c=("#18a0c8", "#7aec9a", "#e4fffa"), TH=2.55, p=0.45, W=0.9, fl=1.0, rings=3, rr=1.68, rays=0, rl=0.0, motes=10, kind="diamond"),
    8: dict(c=("#e0601a", "#ffae3a", "#fff2b0"), TH=2.5, p=0.6, W=1.0, fl=1.05, rings=3, rr=1.68, rays=10, rl=1.5, motes=10, kind="diamond"),
    9: dict(c=("#8a3ce0", "#c88cff", "#f6e6ff"), TH=2.55, p=0.45, W=1.1, fl=1.2, rings=3, rr=1.68, rays=0, rl=0.0, motes=8, kind="star"),
}
# burst timeline (11 frames)
HF = [0.0, 0.2, 0.8, 1.2, 1.15, 1.08, 1.04, 1.02, 1.0, 1.0, 1.0]
WF = [0.0, 0.5, 1.5, 1.9, 1.5, 1.25, 1.1, 1.05, 1.0, 1.0, 1.0]
FL = [0.25, 0.65, 1.0, 1.0, 0.8, 0.55, 0.38, 0.28, 0.22, 0.2, 0.2]
RF = [0.0, 0.5, 1.0, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0]       # rays
GROW = [0.0, 0.0, 0.3, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]       # halo / specials fade-in
FLICK = [0.4, 0.9, 0.35, 1.0, 0.5, 0.8, 0.4, 0.6, 0.35, 0.3, 0.3]    # giai 1


def flat(mb, ky=0.28):
    return mb.xform(sy=ky)


def build_fx(gi, burst):
    cfg = CFG[gi]
    c0, c1, c2 = cfg["c"]
    N = 11 if burst else 8
    nm = ("linh_can_%d" if burst else "linh_can_tru_%d") % gi
    fx = FxP(nm, frames=N, fps=12 if burst else 10, loop=not burst, px=128, pivot=(64, 108), halo=0.6,
             name_vi=("Linh căn %s - bùng sáng" if burst else "Linh căn %s - trụ sáng") % VI[gi],
             where=("linh can giai %d (%s): one-shot reveal burst over the Trac Linh Thach" if burst
                    else "linh can giai %d (%s): looping pillar / aura left after the reveal") % (gi, VI[gi]))
    rng = fx.rng
    TH, W = cfg["TH"], cfg["W"]
    k = max(0.0, min(1.0, (2.55 / max(TH, 0.1) - 1) / 0.2))

    def hf(i, t):
        if burst:
            return HF[i] if HF[i] <= 1 else 1 + (HF[i] - 1) * k
        return 1.0 + 0.03 * math.sin(TAU * t)

    def wf(i, t):
        return WF[i] if burst else 1.0 + 0.07 * math.sin(TAU * t + 1.0)

    def fl(i, t):
        return FL[i] if burst else 0.22 + 0.06 * math.sin(TAU * t)

    def grow(i):
        return GROW[i] if burst else 1.0

    body = fx.mat("body", c0, grad=dict(src="attr", pow=1.0, cpow=2.2), core=c1)
    core = fx.mat("core", c2, grad=dict(src="attr", pow=0.6))
    solid = fx.mat("solid", c2)
    midm = fx.mat("mid", c1)
    mids = fx.mat("mids", c1, grad=dict(src="attr", pow=0.8), opacity=0.9)
    glowm = fx.mat("glow", c0, grad=dict(src="attr", pow=1.2), opacity=0.8)
    pls = lambda t, ph=0.0: math.sin(TAU * t + ph)

    # ---- the flash at the stone's face (also the whole of giai 1)
    fb = glow_disc(1.0, 32).build(fx, "flash", glowm)
    if gi == 1:
        fx.track(fb, lambda t, i: dict(y=Y0, s=cfg["fl"] * (0.75 + 0.25 * (FLICK[i] if burst else 0.5 + 0.5 * pls(t))),
                                       op=(FLICK[i] if burst else 0.5 + 0.35 * pls(t)) * 0.9))
        sd = MB().disc(0, 0, 0.12, 12).build(fx, "spark", solid)
        fx.track(sd, lambda t, i: dict(y=Y0, s=(0.5 + 0.8 * (FLICK[i] if burst else 0.5 + 0.5 * pls(t, 1.0))), op=1.0))
        for j in range(cfg["motes"] - 1):
            mote(fx, "m%d" % j, solid, "disc", 0.04, rising(-0.2 + 0.4 * j, Y0 + 0.15, 0.7, j / 3.0 + 0.1, 0.05, 1.0, 0.8))
        return fx
    fx.track(fb, lambda t, i: dict(y=Y0, s=cfg["fl"] * fl(i, t) * (1.15 if burst else 1.0), op=0.95))
    hard = MB().disc(0, 0, 0.5, 24).build(fx, "hard", solid)
    fx.track(hard, lambda t, i: dict(y=Y0, s=cfg["fl"] * 0.5 * (FL[i] if burst else 0.0) + 0.001, op=1.0,
                                     show=burst and FL[i] > 0.5 and gi >= 3))

    # ---- whiteout (the core blows out): gi >= 5 in frames 2-4
    if burst and gi >= 5:
        WR = {5: 0.8, 6: 1.1, 7: 0.9, 8: 0.95, 9: 1.35}[gi]
        wg = glow_disc(1.0, 36).build(fx, "whiteglow", fx.mat("whiteg", c1, grad=dict(src="attr", pow=0.7)))
        fx.track(wg, lambda t, i: dict(y=Y0, s=WR * 1.2 * [0, 0, 0.6, 1.0, 0.7, 0.3, 0, 0, 0, 0, 0][i] + 0.001, op=1.0, show=2 <= i <= 5))
        wo = MB().disc(0, 0, 1.0, 36).build(fx, "white", fx.mat("whitem", "#ffffff"))
        fx.track(wo, lambda t, i: dict(y=Y0, s=WR * 0.4 * [0, 0, 0.55, 1.0, 0.6, 0, 0, 0, 0, 0, 0][i] + 0.001, show=2 <= i <= 4))

    # ---- ground bloom + rising ground rings
    if gi >= 2:
        bl = flat(MB().disc(0, 0, 1.0, 32, 1.0, 0.0)).build(fx, "bloom", glowm)
        fx.track(bl, lambda t, i: dict(y=0.0, s=cfg["rr"] * 0.55 * (0.3 + 0.7 * grow(i)) * (1 + 0.04 * (0 if burst else pls(t))), op=0.75))
        rm = fx.mat("rm", c1)
        for r_ in range(cfg["rings"]):
            if burst:
                obs = fx.per_frame("ring%d" % r_, rm, (lambda r_: lambda t, i: flat(MB().ring(
                    0, 0, cfg["rr"] * (0.25 + 0.75 * ease_out(sat((i - 1 - r_) / 6.0))), 0.13 * (1 - sat((i - 1 - r_) / 6.0)) + 0.035, seg=48)))(r_))
                for i, ob in enumerate(obs):
                    fx.track(ob, lambda t, ii, i=i, r_=r_: dict(show=(ii == i and 0 <= i - 1 - r_ <= 6)))
            else:
                obs = fx.per_frame("ring%d" % r_, rm, (lambda r_: lambda t, i: flat(MB().ring(
                    0, 0, cfg["rr"] * (0.3 + 0.7 * ((t + r_ / cfg["rings"]) % 1)), 0.1 * (1 - ((t + r_ / cfg["rings"]) % 1)) + 0.035, seg=48)))(r_))

    # ---- the column (giai 2+)
    cb = column(1.0, 1.0, rows=12, taper=0.45 if gi < 5 else 0.3, p=cfg.get("p", 0.85), base=0.4).build(fx, "col", body)
    fx.track(cb, lambda t, i: dict(y=Y0, sx=max(W * wf(i, t), 0.001), sy=max(TH * hf(i, t), 0.001), op=0.9, show=hf(i, t) > 0.01))
    cc = column(1.0, 1.0, rows=12, taper=0.7, p=cfg.get("p", 0.85) + 0.15, base=0.55).build(fx, "corecol", core)
    fx.track(cc, lambda t, i: dict(y=Y0, sx=max(W * 0.28 * wf(i, t), 0.001), sy=max(TH * 0.9 * hf(i, t), 0.001), op=0.85 + 0.15 * pls(t),
                                   show=hf(i, t) > 0.01))

    # ---- rays from the face
    if cfg["rays"]:
        n = cfg["rays"]
        rm2 = fx.mat("raym", c1 if gi != 8 else c1, opacity=0.9)
        for j in range(n):
            a = TAU * j / n + 0.2
            ob = MB().diamond(0, 0, 1.0, 0.1 + 0.03 * (j % 2), 0).build(fx, "ray%d" % j, rm2)
            Lj = cfg["rl"] * (1.0 if j % 2 == 0 else 0.62)
            if math.sin(a) < -0.3:
                Lj *= 0.4        # rays pointing down stay above the frame's bottom edge

            def f(t, i, a=a, Lj=Lj, j=j):
                rf = RF[i] if burst else (0.5 + 0.0 * t if gi >= 5 else 0.0)
                aa = a + (0.06 * i if burst else 0.0) + (TAU * t / n if not burst else 0.0)
                r = 0.25 + Lj * 0.5 * rf
                return dict(x=math.cos(aa) * r, y=Y0 + math.sin(aa) * r, rot=aa, sx=max(Lj * rf, 0.001), sy=1.0, show=rf > 0.01,
                            op=0.9 if burst else 0.5)
            if burst or gi >= 5 and gi != 8:
                fx.track(ob, f)
            else:
                fx.track(ob, lambda t, i: dict(show=False))

    # ---- motes: a few climb the column in both modes, a burst of ballistic ones in the reveal
    n = cfg["motes"]
    kind = cfg["kind"]
    for j in range(n):
        x0 = (j / max(n - 1, 1) - 0.5) * W * 0.8 + rng.uniform(-0.05, 0.05)
        fn = rising(x0, Y0 + 0.1, TH * 1.0, j / n, 0.07, 1.0, 0.7)
        kk = kind if not (gi in (5, 6) and j % 3 == 0) else "star8"
        mote(fx, "m%d" % j, solid if j % 2 else midm, kk, 0.06 if kind in ("disc", "diamond") else 0.1,
             (lambda fn: lambda t: (lambda r: None if (burst and t < 0.25) else r)(fn(t)))(fn))
    if burst:
        for j in range(6 + gi):
            a = PI / 2 + rng.uniform(-1.0, 1.0)
            sp = rng.uniform(0.7, 1.5) * (0.6 + 0.12 * gi)
            mote(fx, "b%d" % j, solid if j % 2 else midm, "star" if j % 2 else kind, 0.07,
                 burst_mote(0.0, Y0, math.cos(a) * sp, math.sin(a) * sp, 0.12 + 0.03 * (j % 4), 0.55, -0.9, 1.0, 0.5))

    # ======================================================= specials
    if gi == 4:
        # V blades + rune circle on the ground
        bm = fx.mat("blade", c0, grad=dict(src="attr", pow=0.8), core=c1)
        for sgn in (-1, 1):
            L = 1.7
            mb = MB().strip([(0.3, 0.0), (0.3 + 0.45 * L * math.sin(0.4), 0.45 * L), (0.3 + L * math.sin(0.4), L * 0.97)], [0.34, 0.2, 0.02], soft=True)
            mb.xform(sx=sgn)
            o = mb.build(fx, "blade%d" % sgn, bm)
            fx.track(o, lambda t, i: dict(y=Y0 - 0.9, sy=max(grow(i), 0.001) * (1.0 + 0.05 * (0 if burst else pls(t))), op=0.7))
        rn = fx.mat("rune", c1)

        def rune_f(t, i):
            mb = runes(MB(), 0, 0, 1.15, 10, 0.34, random.Random(7), 0.045, rot0=TAU * t / 10.0 if not burst else 0.04 * i)
            return flat(mb)
        obs = fx.per_frame("runes", rn, rune_f)
        for i, ob in enumerate(obs):
            fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and grow(i) > 0.2), y=0.0))
    if gi == 5:
        hy, rx, ky = 2.75, 0.95, 0.28
        ring = MB().ring(0, hy, rx, 0.04, seg=40, ky=ky).build(fx, "halo", solid)
        fx.track(ring, lambda t, i: dict(sx=max(grow(i), 0.001), sy=max(grow(i), 0.001), y=hy * (1 - grow(i)) * 0.0, op=0.9, show=grow(i) > 0.05))
        hg = MB().ring(0, hy, rx, 0.18, seg=40, ky=ky, soft=True).build(fx, "halog", mids)
        fx.track(hg, lambda t, i: dict(op=0.7, show=grow(i) > 0.05))
        for j in range(6):
            def f(t, j=j):
                a = TAU * (t / 6.0 + j / 6.0)
                return (rx * math.cos(a), hy + rx * ky * math.sin(a), (0.55 + 0.35 * (-math.sin(a))) * max(0.001, GROW[min(10, int(round(t * 10)))] if burst else 1.0), a)
            mote(fx, "bead%d" % j, solid, "diamond", 0.1, f)
        cr = MB().star(0, 0, 4, 0.38, 0.07, PI / 2).build(fx, "crown", solid)
        fx.track(cr, lambda t, i: dict(y=Y0 + TH * min(hf(i, t), 1.0) * 0.9, s=max(0.6 + 0.3 * pls(t, 0.3), 0.001) * min(1.0, hf(i, t) * 1.2) * 0.8, show=hf(i, t) > 0.3))
    if gi == 6:
        fm = fx.mat("fan", c0, grad=dict(src="attr", pow=0.8), core=c1, opacity=0.85)
        for j in range(7):
            a = PI / 2 + (j - 3) * 0.3
            L = 2.0 - 0.18 * abs(j - 3)
            mb = MB().strip([(0, 0), (0.5 * L * math.cos(a), 0.5 * L * math.sin(a)), (L * math.cos(a), L * math.sin(a))], [0.36, 0.26, 0.02], soft=True)
            o = mb.build(fx, "beam%d" % j, fm)
            fx.track(o, lambda t, i, j=j: dict(y=Y0 + 0.1, sx=max(grow(i), 0.001), sy=max(grow(i), 0.001),
                                               op=(0.55 + 0.3 * pls(t, j * 1.3)) if not burst else 0.8 * RF[i] + 0.35 * (i >= 6) + 0.001))
        hc = 2.5
        for nm2, rr_, w_, mat_ in (("o", 0.95, 0.05, solid), ("i", 0.78, 0.025, midm)):
            o = MB().ring(0, 0, rr_, w_, seg=48).build(fx, "halo" + nm2, mat_)
            fx.track(o, lambda t, i: dict(y=hc, s=max(grow(i), 0.001) * (1 + 0.03 * (0 if burst else pls(t))), show=grow(i) > 0.05, op=0.95))
        dots = MB()
        for q in range(12):
            a = TAU * q / 12
            dots.diamond(0.87 * math.cos(a), 0.87 * math.sin(a), 0.2, 0.1, a + PI / 2)
        o = dots.build(fx, "halodots", solid)
        fx.track(o, lambda t, i: dict(y=hc, rot=(0.1 * i if burst else TAU * t / 12), s=max(grow(i), 0.001), show=grow(i) > 0.05))
    if gi == 7:
        jade = fx.mat("jade", "#7aec9a", grad=dict(src="attr", pow=0.5), opacity=0.9)
        cy = fx.mat("cyan", "#5ae0f4", grad=dict(src="attr", pow=0.5), opacity=0.9)
        for q, (mt, ph0) in enumerate(((cy, 0.0), (jade, PI))):
            def hel(t, i, ph0=ph0):
                Hh = TH * hf(i, t) * 0.95
                pts, ws = [], []
                for s_ in range(25):
                    s = s_ / 24.0
                    env = 0.2 + 0.65 * math.sin(PI * min(1, s * 1.1)) ** 0.7
                    ph = ph0 + TAU * (2.0 * s) - (0.25 * i if burst else TAU * t)
                    pts.append((0.55 * env * math.sin(ph) * wf(i, t) ** 0.3, Y0 + 0.05 + Hh * s))
                    ws.append(0.13 * (1 - s) + 0.03)
                return MB().strip(pts, ws, soft=True) if Hh > 0.05 else MB().strip([(0, Y0), (0, Y0 + 0.05)], 0.01)
            obs = fx.per_frame("helix%d" % q, mt, hel)
            for i, ob in enumerate(obs):
                fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and hf(i, t) > 0.05)))
        # lotus: a fan of petals standing on the ground, opening
        pm = fx.mat("petal", c1, grad=dict(src="attr", pow=0.7), core=c2)
        for j in range(9):
            a = PI / 2 + (j - 4) * 0.27
            L = 0.95 - 0.07 * abs(j - 4)
            mb = MB().strip([(0, 0), (0.5 * L * math.cos(a), 0.5 * L * math.sin(a)), (L * math.cos(a), L * math.sin(a))], [0.3, 0.3, 0.02], soft=True)
            o = mb.build(fx, "petal%d" % j, pm)
            fx.track(o, lambda t, i, j=j: dict(y=-0.05, sx=max(0.3 + 0.7 * grow(i), 0.001), sy=max(grow(i) * (1 + 0.04 * (0 if burst else pls(t, j))), 0.001), op=0.9, show=grow(i) > 0.05))
    if gi == 8:
        fo = fx.mat("fo", "#e0601a", opacity=0.95)
        fm_ = fx.mat("fm", "#ffae3a")
        fc = fx.mat("fc", "#fff2b0")
        for q, (mt, ws, hs) in enumerate(((fo, 1.0, 1.0), (fm_, 0.66, 0.84), (fc, 0.34, 0.62))):
            def col(t, i, ws=ws, hs=hs, q=q):
                Hh = TH * hf(i, t) * hs
                if Hh < 0.1:
                    return MB().disc(0, Y0, 0.01, 6)
                mb = MB()
                for z in range(3):
                    off = (z - 1) * 0.28 * W * ws
                    mb.flame(off, Y0 + 0.02, Hh * (1.0 if z == 1 else 0.72), W * 0.62 * ws * wf(i, t) ** 0.5,
                             sway=0.18 * math.sin(TAU * t * (1 if not burst else 0.5) + z * 2.0 + q), lean=(z - 1) * 0.12)
                return mb
            obs = fx.per_frame("flame%d" % q, mt, col)
            for i, ob in enumerate(obs):
                fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and hf(i, t) > 0.05)))
        # ring of flame tongues on the ground
        def ground_flames(mt, hs, ws):
            def b(t, i):
                mb = MB()
                for z in range(11):
                    a = TAU * z / 11 + 0.3
                    mb.flame(1.25 * math.cos(a), 0.0 + 0.28 * 1.25 * math.sin(a), 0.7 * hs * (0.8 + 0.4 * ((z * 5) % 3) / 2) * max(grow(i), 0.001),
                             0.32 * ws, sway=0.1 * math.sin(TAU * t + z), lean=0.0)
                return mb
            return b
        for q, (mt, hs, ws) in enumerate(((fo, 1.0, 1.0), (fm_, 0.65, 0.6))):
            obs = fx.per_frame("gflame%d" % q, mt, ground_flames(mt, hs, ws))
            for i, ob in enumerate(obs):
                fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and grow(i) > 0.1)))
    if gi == 9:
        dk = fx.mat("dark", "#4a1890", grad=dict(src="attr", pow=0.7), opacity=0.95)
        vi = fx.mat("vio", "#8a3ce0", grad=dict(src="attr", pow=0.6))
        lt = fx.mat("lt", "#c88cff")
        # three spiral arms swirling on the ground
        def arms(mt, wmul, rot_off):
            def b(t, i):
                mb = MB()
                for a_ in range(3):
                    pts, ws = [], []
                    for s_ in range(26):
                        s = s_ / 25.0
                        ang = a_ * TAU / 3 + rot_off + 3.2 * s + (-0.3 * i if burst else -TAU * t / 3.0)
                        r = 0.15 + 1.75 * s
                        pts.append((r * math.cos(ang), r * math.sin(ang)))
                        ws.append((0.22 * (1 - s) + 0.04) * wmul)
                    mb.strip(pts, ws, soft=(wmul > 1))
                return flat(mb)
            return b
        for q, (mt, wm, ro) in enumerate(((dk, 2.0, 0.0), (vi, 1.0, 0.0), (lt, 0.3, 0.0))):
            obs = fx.per_frame("arm%d" % q, mt, arms(mt, wm, ro))
            for i, ob in enumerate(obs):
                fx.track(ob, lambda t, ii, i=i: dict(show=(ii == i and grow(i) > 0.05), y=0.0))
        # a dark halo ring behind the column and a ring of orbiting stars
        hr = MB().ring(0, 0, 1.05, 0.1, seg=48).build(fx, "darkring", dk)
        fx.track(hr, lambda t, i: dict(y=2.3, s=max(grow(i), 0.001), op=0.9, show=grow(i) > 0.05))
        hr2 = MB().ring(0, 0, 1.05, 0.03, seg=48).build(fx, "vring", lt)
        fx.track(hr2, lambda t, i: dict(y=2.3, s=max(grow(i), 0.001), show=grow(i) > 0.05))
        for j in range(10):
            def f(t, j=j):
                a = TAU * (t / 10.0 + j / 10.0)
                return (1.05 * math.cos(a), 2.3 + 1.05 * math.sin(a), (0.6 + 0.4 * math.sin(TAU * 2 * t + j)) * (min(1.0, t * 4) if burst else 1.0), a)
            mote(fx, "orb%d" % j, solid, "star", 0.1, f)
        for j in range(14):
            x0 = rng.uniform(-1.6, 1.6)
            y0 = rng.uniform(0.7, 3.2)
            ph = rng.random()
            mote(fx, "tw%d" % j, solid, "star", 0.075,
                 (lambda x0, y0, ph: lambda t: (x0, y0, (math.sin(PI * ((t + ph) % 1)) ** 2) * (1.0 if not burst or t > 0.3 else 0.0)))(x0, y0, ph))
        if burst:
            # cracks run out along the ground
            for j in range(7):
                a = TAU * j / 7 + 0.3
                pts = jag((0, 0), (1.85 * math.cos(a), 1.85 * math.sin(a)), random.Random(j), 8, 0.2)
                o = flat(MB().strip(pts, [0.07] * len(pts))).build(fx, "crack%d" % j, lt)
                fx.track(o, lambda t, i: dict(y=0.0, sx=sat((i - 1) / 3.0) + 0.001, sy=sat((i - 1) / 3.0) + 0.001, show=2 <= i <= 6))
    return fx


for _g in range(1, 10):
    REG["linh_can_%d" % _g] = (lambda g: lambda: build_fx(g, True))(_g)
    REG["linh_can_tru_%d" % _g] = (lambda g: lambda: build_fx(g, False))(_g)


def all_ids():
    return list(REG)


def make(id):
    return REG[id]()
