"""fx_kiem batch: kiếm khí (sword qi) and basic-attack FX that grow with tu vi.  Runs INSIDE Blender.

Every sheet is one Blender scene of flat emissive meshes built from numbers (crescents, spikes, bolts,
cracks, flames, shards), keyframed, seen by an orthographic camera, rendered by EEVEE at 6x and packed
by fxpost (palette snap to the glow ramps, black -> alpha 0, blend 'add').
Directional FX point RIGHT (+x).  1 unit = 32 sprite px (Fx(..., zoom=1.0)).
"""
import math
import random
from kiem_lib import *          # noqa: F401,F403
from kiem_lib import ARC_K, wisps
from kiem_lib import RAMP, P, crescent, torn_edge, speed_lines, lightning_on_arc, bolt_line, crack, star4, \
    rune_marks, flame_tongue, set_u, arc_point
import fx_combat                 # reuse particle() / flight() / SHAPES (read only)

particle = fx_combat.particle
D = math.radians

# draw order inside a scene (bigger = nearer the camera).  The layers are blended with ALPHA inside the
# render (emission over transparent, black world) so a white core sits ON the violet body instead of adding
# to it: stacked additive layers turned violet+white into pink, which the palette snap read as the `pink`
# skin ramp (mud).  The packed sheet is still blend 'add' (black -> alpha 0).
ZORD = [("halo", 0), ("glow", 0), ("flash", 0), ("stream", 0.5), ("trail", 0.5), ("lines", 1), ("echo", 1),
        ("wave2", 1.5), ("body", 2), ("fin", 2.5), ("ring", 2.5), ("runes", 3), ("flamec", 3.5), ("flame", 3),
        ("crackcore", 5), ("crackc", 5), ("crack", 4.5), ("core", 4), ("white", 4.5), ("tip", 5.5), ("bolt", 5),
        ("acc", 5), ("stars", 6), ("star", 6)]


class KFx(Fx):
    """fxlib.Fx with alpha-layered materials (see ZORD).  The sheet itself stays blend 'add'."""

    def mat(self, name, color, **kw):
        kw.setdefault("mode", "alpha")
        fm = super().mat(name, color, **kw)
        z = next((v for k, v in ZORD if name.startswith(k)), 6.0)
        fm.z = (z * 0.04) if self.view == "ground" else -z * 0.05
        return fm

    def reg(self, ob, fm, x, y, z):
        super().reg(ob, fm, x, y, getattr(fm, "z", z))


Fx = KFx

# ============================================================================ tier tables
# tier -> realm aura family.  T1-T3 Luyện Khí (steel -> bone-white -> ice), then one realm per tier.
TIER = {
    1: dict(px=64, R=28, W=3.2, ramp="steel", acc="#dbe6ef", halo=0.35, realm="Phàm Nhân / Luyện Khí sơ"),
    2: dict(px=64, R=30, W=5.0, ramp="bone", acc="#f6f4f7", halo=0.55, realm="Luyện Khí trung"),
    3: dict(px=64, R=31, W=7.5, ramp="ice", acc="#f2fbff", halo=0.7, realm="Luyện Khí hậu"),
    4: dict(px=96, R=37, W=10.0, ramp="thunder", acc="#f8f8ff", halo=0.8, realm="Trúc Cơ"),
    5: dict(px=96, R=39, W=11.0, ramp="verdant", acc="#ffe27a", halo=0.8, realm="Kết Đan"),
    6: dict(px=96, R=40, W=12.0, ramp="spirit", acc="#ffe27a", halo=0.85, realm="Nguyên Anh"),
    7: dict(px=96, R=42, W=13.0, ramp="cosmic", acc="#ffe27a", halo=0.85, realm="Hóa Thần"),
    8: dict(px=128, R=50, W=16.0, ramp="flame", acc="#fffbe4", halo=0.9, realm="Luyện Hư"),
    9: dict(px=128, R=52, W=17.0, ramp="ice", acc="#b8c0ff", halo=0.9, realm="Hợp Thể"),
    10: dict(px=128, R=54, W=19.0, ramp="cosmic", acc="#ffe27a", halo=0.95, realm="Đại Thừa"),
}
PIV = {64: (16, 35), 96: (22, 50), 128: (30, 66)}            # kiem_khi pivot = the sword hand
GROUP = {1: "ice", 2: "spirit", 3: "cosmic", 4: "holy"}        # weapon families / impacts by tier group
GPX = {1: 64, 2: 64, 3: 96, 4: 128}

A0, A1 = D(70), D(-60)          # swing: from upper right (u=0) down to lower right (u=1), clockwise
KHI_K = (1.08, 0.82)            # ... on an ellipse: wider than tall, so the sweep reads as an arc, not a bracket


def U(px):
    return px * P


def frame_lim(fx, margin_px=4):
    """half extent (units) the art may reach from the frame centre."""
    return U(fx.px / 2 - margin_px)


def clamp_travel(fx, x0, y0, vx, vy, margin=5):
    """scale a particle's travel so it ends inside the frame (no edge clipping)."""
    lim = frame_lim(fx, margin)
    k = 1.0
    for p, v in ((x0, vx), (y0, vy)):
        e = p + v
        if abs(e) > lim and abs(v) > 1e-6:
            k = min(k, max(0.0, (math.copysign(lim, e) - p) / v))
    return vx * k, vy * k


def per_frame_opt(fx, name, fm, builder, x=0.0, y=0.0):
    """like Fx.per_frame, but builder may return None (nothing on that frame)."""
    obs = []
    for i in range(fx.N):
        mb = builder(fx.T(i), i)
        if mb is None or not mb.v:
            continue
        ob = mb.build(fx, "%s_%02d" % (name, i), fm, x, y)
        fx.track(ob, (lambda ii: (lambda t, i2: dict(show=(i2 == ii), x=x, y=y)))(i))
        obs.append(ob)
    return obs


def spark(fx, name, fm, shape, size_px, x0, y0, vx, vy, t0, life, g=0.0, spin=0.0):
    vx, vy = clamp_travel(fx, x0, y0, vx, vy)
    return particle(fx, name, fm, shape, U(size_px), fx_combat.flight(x0, y0, vx, vy, t0, life, g, 1.0, spin, 0.7))


# ============================================================================ kiem_khi: the swing
HEAD = [0.55, 1.0, 1.15, 1.15, 1.15, 1.15, 1.15]
TAIL = [-0.38, -0.3, -0.1, 0.16, 0.42, 0.68, 0.96]
GROW = [0.96, 1.0, 1.02, 1.035, 1.05, 1.06, 1.07]
OPA = [0.95, 1.0, 1.0, 1.0, 0.92, 0.82, 0.7]


def prof_swing(u):
    return math.sin(PI * u) ** 0.7 * (0.3 + 0.7 * u ** 0.9)


def make_kiem_khi(t):
    S = TIER[t]
    px = S["px"]
    pv = PIV[px]
    fx = Fx("kiem_khi_%d" % t, frames=7, fps=20, halo=S["halo"], px=px, pivot=pv, zoom=1.0,
            name_vi="Kiếm khí bậc %d (%s)" % (t, S["realm"]),
            where="melee swing arc at the sword hand; one-shot from the slash hit frame")
    rng = fx.rng
    ARC_K[:] = KHI_K
    hx, hy = U(pv[0] - px / 2), U(px / 2 - pv[1])
    R, W = U(S["R"]), U(S["W"])
    ramp = RAMP[S["ramp"]]
    acc = S["acc"]

    def win_track(ob, head_d=0.0, tail_d=0.0, op_k=1.0, grow_k=1.0):
        fx.track(ob, lambda tt, i: dict(x=hx, y=hy, s=1 + (GROW[i] - 1) * grow_k,
                                        head=HEAD[i] + head_d, tail=TAIL[i] + tail_d, op=OPA[i] * op_k))

    # --- main crescent: halo, body, white-hot core (the core rides the outer, cutting edge)
    if t >= 2:
        halo = fx.mat("halo", ramp[1] if t >= 3 else ramp[0], grad=dict(src="attr", pow=1.4), window=True,
                      opacity=0.55 if t == 2 else 0.85)
        win_track(crescent(MB(), R, A0, A1, W * 1.9, soft=True, prof=prof_swing).build(fx, "halo", halo))
    jit = U(0.6) if t >= 8 else 0.0
    # body: bright hue on the cutting (outer) edge, deepening and fading towards the inside: a crescent moon
    if t == 1:                                   # a mortal's swing: dull steel, no glow (contrast is the progression)
        body = fx.mat("body", ramp[1], window=True)
        mb = crescent(MB(), R, A0, A1, W, prof=prof_swing)
    else:
        body = fx.mat("body", ramp[1] if t >= 3 else ramp[0], core=ramp[2], window=True,
                      grad=dict(src="attr", pow=0.55, cpow=1.2))
        mb = crescent(MB(), R, A0, A1, W, prof=prof_swing, jit=jit, rng=random.Random(t * 13), gside="out")
    if t >= 4:                                   # torn outer edge: the qi is ripped by its own speed
        cnt, ln, lean, wid = {4: (9, 5, 0.6, 0.6), 5: (11, 6, 0.7, 0.6), 6: (13, 8, 0.8, 0.55), 7: (14, 8, 0.8, 0.55),
                              8: (15, 10, 1.0, 0.6), 9: (17, 12, 0.15, 0.32), 10: (18, 12, 0.9, 0.5)}[t]
        torn_edge(mb, R, A0, A1, W, cnt, U(ln), random.Random(t * 7 + 1), prof=prof_swing, side=1, lean=lean, width=wid)
        if t >= 6:
            torn_edge(mb, R, A0, A1, W, cnt // 2, U(ln * 0.6), random.Random(t * 7 + 2), prof=prof_swing, side=-1,
                      lean=lean, width=wid)
    win_track(mb.build(fx, "body", body))
    n_w = {3: 3, 4: 5, 5: 6, 6: 8, 7: 9, 8: 11, 9: 12, 10: 14}.get(t, 0)
    if n_w:                                      # streaks peeling off the inner edge, trailing the swing
        wm = fx.mat("echo2", ramp[2], window=True)
        win_track(wisps(MB(), R, A0, A1, W, n_w, random.Random(t * 5 + 9), prof_swing,
                        w_px=1.2 + 0.12 * t, length=0.16 + 0.012 * t, inward=0.9 + 0.05 * t).build(fx, "echo2", wm),
                  tail_d=0.05)
    core = fx.mat("core", ramp[3] if t > 1 else ramp[2], window=True)
    coff = W * 0.24 if t >= 2 else 0.0
    win_track(crescent(MB(), R + coff, A0, A1, W * (0.36 if t >= 2 else 0.4), prof=prof_swing).build(fx, "core", core))

    # --- echo crescents: the wave behind the wave (lagging sweep)
    if t >= 2:
        echo = fx.mat("echo", ramp[2] if t < 6 else ramp[1], window=True, grad=dict(src="attr", pow=0.3))
        offs = [(-W * 0.75, 0.12, 0.8)]
        if t >= 3:
            offs.append((W * 0.95, 0.25, 0.92))
        if t >= 8:
            offs.append((-W * 1.2, 0.2, 0.75))
        lw = U(1.1 if t < 6 else 1.6)
        win_track(speed_lines(MB(), R, A0, A1, offs, lw).build(fx, "lines", echo), head_d=-0.06, tail_d=0.06)
    if t in (6, 7, 9):                           # a second, thinner crescent outside: a double wave
        # (T8 burns instead: flames are its outer layer; T10 tears space instead: void cracks)
        e2 = fx.mat("wave2", ramp[2], window=True, grad=dict(src="attr", pow=0.2))
        R2 = R + W * (0.95 if t < 8 else 1.05)
        a2 = (A0 - D(6), A1 + D(4))
        mb2 = crescent(MB(), R2, a2[0], a2[1], W * 0.4, prof=prof_swing)
        if t >= 8:
            torn_edge(mb2, R2, a2[0], a2[1], W * 0.4, 9, U(4), random.Random(t * 7 + 3), prof=prof_swing, lean=0.8)
        win_track(mb2.build(fx, "wave2", e2), head_d=-0.12, tail_d=0.1)

    # --- runes riding the body (Hóa Thần): abstract strokes, never glyphs
    if t == 7:
        rm = fx.mat("runes", acc, window=True)
        mbr = MB()
        rr = random.Random(77)
        for k in range(7):
            u = 0.3 + 0.6 * k / 6
            x, y, a = arc_point(R - W * 0.05, A0, A1, u)
            b = len(mbr.v)
            rune_marks(mbr, [(x, y, a - PI / 2)], U(7), rr, U(1.4))
            set_u(mbr, b, u)
        win_track(mbr.build(fx, "runes", rm), head_d=-0.05, tail_d=0.1)

    # --- tip glint at the blade tip (start of the swing = anticipation)
    tip = fx.mat("tip", ramp[3] if t > 1 else "#dbe6ef")
    tx, ty, _ = arc_point(R + coff, A0, A1, 0.55)
    ts = U(3 + 1.3 * t)
    ex, ey, _ = arc_point(R + coff, A0, A1, 0.97)
    st = star4(MB(), 0, 0, ts, 0.16).build(fx, "tip", tip)
    fx.track(st, lambda tt, i: dict(x=hx + (tx if i == 0 else ex), y=hy + (ty if i == 0 else ey),
                                    s=[1.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0][i] + 0.001, rot=0.0, show=i < 2))

    # --- lightning crawling on the wave (Trúc Cơ and up)
    if t >= 4:
        lm = fx.mat("bolt", acc if t not in (4, 9) else ("#f8f8ff" if t == 4 else "#b8c0ff"))
        nb = {4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4}[t]

        def bolts(tt, i):
            if not 1 <= i <= 4:
                return None
            r = random.Random(t * 100 + i)
            lo = max(0.15, TAIL[i] + 0.3)
            hi = min(0.95, HEAD[i] - 0.05)
            if hi - lo < 0.12:
                return None
            return lightning_on_arc(MB(), R * GROW[i], A0, A1, W, r, nb, U(1.2 if t < 8 else 1.6), span=0.3,
                                    prof=prof_swing, ulo=lo, uhi=hi)
        per_frame_opt(fx, "bolt", lm, bolts, hx, hy)

    # --- flames on the outer edge (Luyện Hư)
    if t == 8:
        fo = fx.mat("flame", ramp[1])
        fm_ = fx.mat("flamec_mid", ramp[2])
        fc = fx.mat("flamecore", ramp[3])

        def flames(tt, i, inner=False, k_h=1.0, k_w=1.0):
            if i > 5:
                return None
            r = random.Random(800 + i)
            mbf = MB()
            lo = max(0.15, TAIL[i] + 0.22)
            hi = min(0.97, HEAD[i] - 0.03)
            for k in range(9):
                u = lo + (hi - lo) * (k + r.uniform(0.2, 0.8)) / 9
                w = W * prof_swing(u)
                x, y, a = arc_point(R * GROW[i] + w * 0.35, A0, A1, u)
                h = U(r.uniform(15, 24)) * (0.45 + 0.55 * prof_swing(u)) * (1.0 - 0.1 * i) * k_h
                flame_tongue(mbf, (x, y), a + 0.42, h, U(8.5) * (0.6 + 0.4 * prof_swing(u)) * k_w,
                             U(r.uniform(-3, 3)) * k_h)
            return mbf
        per_frame_opt(fx, "flame", fo, flames, hx, hy)
        per_frame_opt(fx, "flamecm", fm_, lambda tt, i: flames(tt, i, k_h=0.7, k_w=0.6), hx, hy)
        per_frame_opt(fx, "flamec", fc, lambda tt, i: flames(tt, i, k_h=0.4, k_w=0.3), hx, hy)

    # --- void cracks + stars (Đại Thừa): space splits along the cut
    if t == 10:
        cm = fx.mat("crack", ramp[2])
        cc = fx.mat("crackcore", ramp[3])
        seeds = [(0.22, 0.3), (0.4, -0.15), (0.55, 0.3), (0.7, -0.25), (0.84, 0.2), (0.96, -0.1)]
        GR = [0.0, 0.55, 0.9, 1.0, 1.0, 0.85, 0.0]
        WD = [0.0, 1.0, 1.0, 0.9, 0.7, 0.45, 0.0]

        def cracks(tt, i, core_=False):
            if GR[i] <= 0:
                return None
            mbc = MB()
            for k, (u, da) in enumerate(seeds):
                x, y, a = arc_point(R * GROW[i] + W * prof_swing(u) * 0.45, A0, A1, u)
                crack(mbc, (x, y), a + da, U(19 + 6 * (k % 2)) * GR[i], random.Random(1000 + k),
                      U((2.0 if not core_ else 0.9) * WD[i]), 2)
            return mbc
        per_frame_opt(fx, "crack", cm, cracks, hx, hy)
        per_frame_opt(fx, "crackc", cc, lambda tt, i: cracks(tt, i, True), hx, hy)

    # --- sparks / embers / shards / stars flung off the swing
    n_sp = {1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 13, 8: 16, 9: 16, 10: 18}[t]
    sm = fx.mat("spark", ramp[3] if t > 1 else ramp[2])
    am = fx.mat("spark2", acc if t > 1 else ramp[2])
    for j in range(n_sp):
        u = 0.25 + 0.72 * (j + rng.uniform(0.1, 0.9)) / n_sp
        x, y, a = arc_point(R + W * prof_swing(u) * 0.3, A0, A1, u)
        out = rng.uniform(0.35, 0.75) * R * (0.6 if t == 1 else 1.0)
        tang = rng.uniform(0.0, 0.5) * R
        # the swing goes clockwise: its tangent is (sin a, -cos a)
        vx = math.cos(a) * out + math.sin(a) * tang
        vy = math.sin(a) * out - math.cos(a) * tang
        t0 = max(0.0, (u - 0.55) / 0.45 / 6.0) + rng.uniform(0.0, 0.12)
        life = rng.uniform(0.5, 0.8)
        shape = "diamond"
        size = rng.uniform(1.2, 1.8) if t <= 3 else rng.uniform(1.6, 2.6) + (0.6 if t >= 8 else 0)
        fm = sm if j % 2 == 0 else am
        g = 0.0
        if t == 8:
            g = U(10)                      # embers rise
        if t == 9 and j % 2 == 0:
            shape, size = "diamond", size * 1.5           # frost shards: long thin diamonds
        if t in (5, 6, 7, 10) and j % 3 == 1:
            shape, size = "star", size * 1.3
        if t == 1:
            size = 1.0
        spark(fx, "sp%d" % j, fm, shape, size, hx + x, hy + y, vx, vy, t0, life, g, rng.uniform(-3, 3) if shape != "diamond" else 0.0)
        # diamonds point along their travel
        ob = fx.col.objects["SM_%s_sp%d" % (fx.id, j)]
        _rotate_track(fx, ob, math.atan2(vy + g * 0.5, vx) if shape == "diamond" else None)
    if t == 9:                                     # snow motes drifting off the cold wave
        sn = fx.mat("snow", ramp[3])
        for j in range(8):
            u = rng.uniform(0.3, 0.95)
            x, y, a = arc_point(R + W * 0.8, A0, A1, u)
            spark(fx, "sn%d" % j, sn, "disc", 1.6, hx + x, hy + y, rng.uniform(0.05, 0.4), -rng.uniform(0.1, 0.3),
                  0.15 + rng.uniform(0, 0.3), 0.75)
    if t == 10:                                    # star glints in the torn sky
        stm = fx.mat("stars", RAMP["holy"][3])
        for j in range(7):
            u = 0.2 + 0.75 * j / 6
            x, y, a = arc_point(R + W * rng.uniform(0.9, 1.6), A0, A1, u)
            t0 = 0.12 + 0.1 * (j % 3)
            ob = star4(MB(), 0, 0, U(rng.uniform(3, 5)), 0.15).build(fx, "star%d" % j, stm)
            fx.track(ob, lambda tt, i, x=x, y=y, t0=t0: dict(
                x=hx + x, y=hy + y, s=max(0.001, math.sin(PI * min(1, max(0, (tt - t0) / 0.75)))), rot=0.0))
    return fx


def _rotate_track(fx, ob, ang):
    """re-key a particle's rotation so diamonds point along their flight."""
    if ang is None:
        return
    for i in range(fx.N):
        fx.sc.frame_set(i + 1)
        ob.rotation_euler[2] = ang
        ob.keyframe_insert("rotation_euler", frame=i + 1)


# ============================================================================ kiem_song: the flying wave
SONG = {   # tier -> (crescent height px, thickness px)
    2: (32, 5.5), 3: (38, 7.5), 4: (50, 10.0), 5: (55, 11.5), 6: (60, 13.0), 7: (66, 14.5),
    8: (84, 18.0), 9: (92, 20.0), 10: (100, 22.0)}


def prof_wave(u):
    return math.sin(PI * u) ** 0.75


def make_kiem_song(t):
    S = TIER[t]
    px = S["px"]
    H, Wp = SONG[t]
    fx = Fx("kiem_song_%d" % t, frames=6, fps=14, loop=True, halo=S["halo"], px=px, pivot=(px // 2, px // 2), zoom=1.0,
            name_vi="Kiếm sóng bậc %d (%s)" % (t, S["realm"]),
            where="sword-qi wave flying right (projectile, the game moves and rotates it); pivot = wave centre")
    ramp = RAMP[S["ramp"]]
    acc = S["acc"]
    th = D(58)
    Rc = U(H) / (2 * math.sin(th))
    front = U(px * 0.30)
    cx = front - Rc                     # crescent centre (left of the wave)
    W = U(Wp) * 0.8
    a0, a1 = th, -th
    mats = dict(
        halo=fx.mat("halo", ramp[1] if t >= 3 else ramp[0], grad=dict(src="attr", pow=1.4), opacity=0.85),
        stream=fx.mat("stream", ramp[1], grad=dict(src="attr", pow=0.8)),
        body=fx.mat("body", ramp[1] if t >= 3 else ramp[0], core=ramp[2], grad=dict(src="attr", pow=1.0, cpow=1.0)),
        core=fx.mat("core", ramp[3]),
        acc=fx.mat("acc", acc),
    )

    def wave(tt, i, layer):
        r = random.Random(t * 1000 + i * 17 + sum(map(ord, layer)))
        fl = 1.0 + 0.07 * math.sin(TAU * tt) + 0.04 * math.sin(TAU * 2 * tt + 1)
        mb = MB()
        if layer == "halo":
            crescent(mb, Rc, a0, a1, W * 2.0 * fl, prof=prof_wave, soft=True)
            mb.xform(dx=cx)
            return mb
        if layer == "body":
            crescent(mb, Rc, a0, a1, W * fl, prof=prof_wave, gside="out")
            if t >= 4:      # torn back edge streaming behind the wave
                torn_edge(mb, Rc, a0, a1, W * fl, {4: 8, 5: 10, 6: 12, 7: 13, 8: 14, 9: 14, 10: 16}[t],
                          U(4 + 0.6 * t), r, prof=prof_wave, side=-1, lean=-0.2, width=0.55, u0=0.08, u1=0.92)
            if t >= 9:      # frost / void spikes on the front edge
                torn_edge(mb, Rc, a0, a1, W * fl, 9, U(6 if t == 9 else 5), r, prof=prof_wave, side=1, lean=0.0,
                          width=0.3, u0=0.15, u1=0.85)
            mb.xform(dx=cx)
            return mb
        if layer == "core":
            crescent(mb, Rc + W * 0.22, a0, a1, W * 0.36 * fl, prof=prof_wave)
            mb.xform(dx=cx)
            return mb
        if layer == "stream":     # streaming tail: tapered ribbons flowing back from the wave
            n = {2: 3, 3: 4, 4: 5, 5: 5, 6: 6, 7: 6, 8: 7, 9: 7, 10: 8}[t]
            rs = random.Random(t * 41)
            for k in range(n):
                u = 0.12 + 0.76 * (k + rs.uniform(-0.3, 0.3)) / max(n - 1, 1)
                x, y, a = arc_point(Rc - W * 0.2, a0, a1, u)
                L = U(px) * (0.2 + 0.26 * prof_wave(u)) * rs.uniform(0.6, 1.0) * (0.85 + 0.25 * math.sin(TAU * tt + k * 1.7))
                m = 10
                pts = [(cx + x - L * q / m, y + U(1.2) * math.sin(TAU * (tt + q / m * 0.8) + k) * q / m) for q in range(m + 1)]
                ws = [W * 0.45 * prof_wave(u) ** 0.5 * (1 - q / m) ** 1.2 + 0.004 for q in range(m + 1)]
                mb.strip(pts, ws, soft=True)
            return mb
        if layer == "acc":
            if t >= 4:            # lightning crawling over the wave
                for _ in range({4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3}[t]):
                    lightning_on_arc(mb, Rc, a0, a1, W, r, 1, U(1.2 if t < 8 else 1.5), span=0.35, prof=prof_wave, branch=False)
                mb.xform(dx=cx)
            # motes shed behind the wave, scrolling left (loop)
            n = {2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 8, 9: 8, 10: 9}[t]
            rr = random.Random(t * 31)
            for k in range(n):
                ph = rr.random()
                yy = rr.uniform(-0.45, 0.45) * U(H)
                s = (tt + ph) % 1.0
                x = cx + Rc * math.cos(math.asin(max(-1, min(1, yy / Rc)))) - U(4) - s * U(px) * 0.42
                sz = U(rr.uniform(1.2, 2.2) + 0.08 * t) * (1 - s) ** 0.5
                if t in (5, 6, 7, 10) and k % 3 == 0:
                    star4(mb, x, yy, sz * 1.6, 0.2)
                else:
                    mb.diamond(x, yy, sz * 2.2, sz * 0.9)
            if t == 7:            # runes riding the wave
                pa = []
                for k in range(4):
                    u = 0.2 + 0.6 * k / 3
                    x, y, a = arc_point(Rc - W * 0.1, a0, a1, u)
                    pa.append((cx + x, y, a - PI / 2 + 0.3 * math.sin(TAU * tt + k)))
                rune_marks(mb, pa, U(5), random.Random(70 + i), U(1.0))
            if t == 10:           # void cracks trailing from both tips + stars
                for k, (u, ang) in enumerate(((0.04, PI - 0.5), (0.96, PI + 0.5), (0.5, PI))):
                    x, y, a = arc_point(Rc - (W * 0.5 if k == 2 else 0.0), a0, a1, u)
                    crack(mb, (cx + x, y), ang, U(14 + 3 * math.sin(TAU * tt + k)), random.Random(500 + k), U(1.6), 2)
                for k in range(4):
                    ph = (tt + k / 4) % 1
                    star4(mb, cx + Rc * 0.6 - ph * U(40), (k - 1.5) * U(H) * 0.3, U(3.5) * math.sin(PI * ph) + U(0.3), 0.15)
            return mb
        return None

    for layer in ("halo", "stream", "body", "core", "acc"):
        if layer == "halo" and t < 2:
            continue
        per_frame_opt(fx, layer, mats[layer], lambda tt, i, layer=layer: wave(tt, i, layer))
    if t == 8:                         # flames burning off the back of the wave
        fo, fc = fx.mat("flame", ramp[2]), fx.mat("flamec", ramp[3])

        def flames(tt, i, inner):
            r = random.Random(880 + i)
            mbf = MB()
            for k in range(9):
                u = 0.1 + 0.8 * (k + r.uniform(0.2, 0.8)) / 9
                x, y, a = arc_point(Rc - W * prof_wave(u) * 0.3, a0, a1, u)
                h = U(r.uniform(9, 16)) * prof_wave(u) * (0.5 if inner else 1.0)
                flame_tongue(mbf, (cx + x, y), PI + a * 0.35 + r.uniform(-0.15, 0.15), h,
                             U(6 if not inner else 3) * prof_wave(u), U(r.uniform(-2.5, 2.5)))
            return mbf
        per_frame_opt(fx, "flame", fo, lambda tt, i: flames(tt, i, False))
        per_frame_opt(fx, "flamec", fc, lambda tt, i: flames(tt, i, True))
    if t == 9:                         # ice shards trailing
        sh = fx.mat("shard", ramp[3])

        def shards(tt, i):
            mbs = MB()
            rr = random.Random(99)
            for k in range(7):
                ph = rr.random()
                s = (tt + ph) % 1
                y = rr.uniform(-0.4, 0.4) * U(H)
                x = front - U(10) - s * U(px) * 0.45
                mbs.diamond(x, y, U(7) * (1 - s * 0.6), U(2.0) * (1 - s * 0.5), rr.uniform(-0.3, 0.3))
            return mbs
        per_frame_opt(fx, "shards", sh, shards)
    return fx


# ============================================================================ kiem_no: impact of the wave
def make_kiem_no(g):
    px = GPX[g]
    ramp = RAMP[GROUP[g]]
    fx = Fx("kiem_no_%d" % g, frames=6, fps=18, halo=0.7 + 0.08 * g, px=px, zoom=1.0,
            name_vi="Kiếm khí nổ %s" % ["nhỏ", "vừa", "lớn", "hủy diệt"][g - 1],
            where="impact where a sword-qi wave lands; one-shot, centred on the target")
    rng = fx.rng
    Rm = U(px * 0.40)
    glow = fx.mat("glow", ramp[1], grad=dict(src="radial", pow=1.8), opacity=0.9)
    body = fx.mat("body", ramp[2])
    core = fx.mat("core", ramp[3])
    acc = fx.mat("acc", RAMP["flame"][2] if g == 4 else ramp[3])
    F = MB().disc(0, 0, 1.0, 32, 1, 0).build(fx, "flash", glow)
    # the flash shrinks away instead of dimming (dim gold / violet snaps to a dark plate)
    fx.track(F, lambda t, i: dict(s=Rm * [0.55, 0.85, 0.75, 0.45, 0.2, 0.0][i] + 0.001, op=[1, 0.95, 0.85, 0.75, 0.6, 0.0][i] + 0.001,
                                  show=i < 5))
    C = MB().disc(0, 0, 1.0, 24).build(fx, "white", core)
    fx.track(C, lambda t, i: dict(s=Rm * [0.32, 0.26, 0.14, 0.06, 0.0, 0.0][i] + 0.001, show=i < 4))
    # the cut itself: an X of two blades of light (the wave's crescent breaks into a cross)
    for k, ang in enumerate((D(20), D(-62))):
        for nm, fm, wk in (("xb", body, 1.0), ("xc", core, 0.4)):
            ob = MB().diamond(0, 0, 2.0, 0.09 + 0.02 * g).build(fx, "%s%d" % (nm, k), fm)
            fx.track(ob, lambda t, i, ang=ang, wk=wk, k=k: dict(rot=ang, sx=Rm * [0.7, 1.0, 1.05, 0.95, 0.7, 0.0][i] * (1 if k == 0 else 0.85) + 0.001,
                                                               sy=Rm * wk * [1.0, 1.0, 0.7, 0.4, 0.2, 0.0][i] * 2.2 + 0.001,
                                                               show=i < 5))
    # shock ring(s)
    rings = [(1.0, 0.0)] + ([(0.7, 0.12)] if g >= 3 else [])

    def ring(t, i, r_k, lag, w_k):
        tt = max(0.0, t - lag)
        r = Rm * (0.25 + 0.75 * ease_out(min(1, tt * 1.15))) * r_k
        w = U(1 + g) * (1 - tt) ** 0.8 * w_k + U(0.6)
        if i == 0 and lag > 0:
            return None
        mb = MB()
        if tt < 0.55:
            mb.ring(0, 0, r, w, seg=48)
        else:
            rr = random.Random(int(r_k * 10) + i)
            n = 7 + g
            for k in range(n):
                a = TAU * k / n + rr.uniform(0, 0.3)
                mb.ring(0, 0, r, w, a, a + TAU / n * rr.uniform(0.35, 0.7), seg=6)
        return mb
    for j, (rk, lag) in enumerate(rings):
        per_frame_opt(fx, "ringb%d" % j, body, lambda t, i, rk=rk, lag=lag: ring(t, i, rk, lag, 1.0))
        per_frame_opt(fx, "ringc%d" % j, core, lambda t, i, rk=rk, lag=lag: ring(t, i, rk, lag, 0.4))
    # radial shards + sparks
    n = 8 + 3 * g
    for j in range(n):
        a = TAU * j / n + rng.uniform(-0.15, 0.15)
        far = Rm * rng.uniform(0.75, 1.0)
        L = U(rng.uniform(4, 7) + g)
        ob = MB().diamond(0, 0, L, L * 0.28).build(fx, "shard%d" % j, core if j % 2 else acc)
        fx.track(ob, lambda t, i, a=a, far=far: dict(x=math.cos(a) * far * ease_out(min(1, t * 1.2 + 0.1)),
                                                     y=math.sin(a) * far * ease_out(min(1, t * 1.2 + 0.1)), rot=a,
                                                     s=max(0.001, (1 - t) ** 0.7)))
    if g >= 2:     # lightning arcs out of the blast
        def bolts(t, i):
            if not 0 <= i <= 3:
                return None
            r = random.Random(40 + i)
            mb = MB()
            for k in range(g):
                a = r.uniform(0, TAU)
                L = Rm * r.uniform(0.6, 0.95)
                bolt_line(mb, (math.cos(a) * U(4), math.sin(a) * U(4)), (math.cos(a) * L, math.sin(a) * L), r, U(1.4 + 0.2 * g), 6)
            return mb
        per_frame_opt(fx, "bolt", core, bolts)
    if g == 4:     # space cracks and stars
        cm = fx.mat("crack", RAMP["cosmic"][2])

        def cracks(t, i):
            if i == 0:
                return None
            mb = MB()
            for k in range(5):
                a = TAU * k / 5 + 0.4
                crack(mb, (math.cos(a) * U(6), math.sin(a) * U(6)), a, Rm * 0.85 * [0, 0.6, 0.9, 1, 1, 1][i],
                      random.Random(60 + k), U(2.2 * [0, 1, 1, 0.8, 0.55, 0.35][i]), 2)
            return mb
        per_frame_opt(fx, "crack", cm, cracks)
        stm = fx.mat("stars", RAMP["holy"][3])
        for j in range(6):
            a = TAU * j / 6 + 0.25
            rr = Rm * rng.uniform(0.5, 0.9)
            ob = star4(MB(), 0, 0, U(4), 0.15).build(fx, "star%d" % j, stm)
            fx.track(ob, lambda t, i, a=a, rr=rr, j=j: dict(x=math.cos(a) * rr, y=math.sin(a) * rr,
                                                            s=[0.001, 0.6, 1.0, 0.8, 0.5, 0.25][i] * (0.7 + 0.3 * (j % 2)) + 0.001))
    return fx


# ============================================================================ kiem_ngan: the scar on the ground
NGAN = {1: (96, "ice", 0.55), 2: (96, "holy", 0.7), 3: (128, "flame", 0.8)}


def make_kiem_ngan(k):
    px, rname, halo = NGAN[k]
    ramp = RAMP[rname]
    fx = Fx("kiem_ngan_%d" % k, view="ground", frames=8, fps=12, halo=halo, px=px, ground=True, zoom=1.0,
            name_vi="Vết chém trên đất %d" % k,
            where="scar a sword-qi wave cuts into the ground (drawn under characters); points right; one-shot")
    L = U(px * 0.40)
    Wd = U([8, 11, 15][k - 1])
    n = 30

    def scar(wk, off=0.0, soft=False):
        pts, ws = [], []
        for j in range(n + 1):
            s = j / n
            x = -L + 2 * L * s
            y = U(px * 0.05) * math.sin(PI * s) + off               # a shallow crescent bowing away from the camera
            pts.append((x, y))
            ws.append(Wd * wk * math.sin(PI * s) ** 0.95 * (0.35 + 0.65 * s ** 0.7) + 0.005)
        return MB().strip(pts, ws, soft=soft)
    HD = [0.45, 1.05, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]
    TL = [-0.4, -0.4, -0.35, -0.3, -0.2, 0.0, 0.25, 0.55]
    SY = [1.0, 1.0, 0.95, 0.85, 0.7, 0.55, 0.45, 0.35]
    halo_m = fx.mat("halo", ramp[1], grad=dict(src="attr", pow=1.2), window=True, opacity=0.8)
    body = fx.mat("body", ramp[2], grad=dict(src="attr", pow=0.15), window=True)
    core = fx.mat("core", ramp[3], window=True)
    for nm, mb, fm, ck in (("halo", scar(2.2, soft=True), halo_m, 1.0), ("body", scar(1.0), body, 1.0),
                           ("core", scar(0.35), core, [1, 1, 1, 0.9, 0.6, 0.0, 0.0, 0.0])):
        ob = mb.build(fx, nm, fm)
        fx.track(ob, lambda t, i, ck=ck: dict(sy=SY[i] * (ck[i] if isinstance(ck, list) else 1) + 0.001, sx=1.0,
                                             head=HD[i], tail=TL[i], show=not (isinstance(ck, list) and ck[i] == 0)))
    if k >= 2:     # small side cracks branching off the scar
        cm = fx.mat("crack", ramp[2])

        def cracks(t, i):
            if not 1 <= i <= 6:
                return None
            mb = MB()
            r = random.Random(7)
            for j in range(4 + 2 * k):
                s = 0.15 + 0.8 * (j + 0.5) / (4 + 2 * k)
                x = -L + 2 * L * s
                y = U(px * 0.05) * math.sin(PI * s)
                side = 1 if j % 2 else -1
                ang = side * PI / 2 + r.uniform(-0.6, 0.6)
                crack(mb, (x, y), ang, U(6 + 2 * k) * r.uniform(0.6, 1.0) * [0, 0.7, 1, 1, 1, 1, 0.9, 0][i], r,
                      U(1.4 * [0, 1, 1, 0.9, 0.75, 0.6, 0.45, 0][i]), 1)
            return mb
        per_frame_opt(fx, "crack", cm, cracks)
    # embers rising from the scar (z = up in the ground view)
    em = fx.mat("ember", ramp[3])
    em2 = fx.mat("ember2", ramp[2])
    rng = fx.rng
    for j in range(6 + 4 * k):
        s = rng.uniform(0.1, 0.95)
        x = -L + 2 * L * s
        y = U(px * 0.05) * math.sin(PI * s)
        t0 = rng.uniform(0.05, 0.45)
        life = rng.uniform(0.4, 0.6)
        h = U(rng.uniform(8, 16) * (1 + 0.3 * k))
        dx = U(rng.uniform(-3, 5))
        ob = MB().diamond(0, 0, U(2.2), U(1.4)).build(fx, "em%d" % j, em if j % 2 else em2)
        fx.track(ob, lambda t, i, x=x, y=y, t0=t0, life=life, h=h, dx=dx: (
            None if not (0 <= (t - t0) / life <= 1) else
            dict(x=x + dx * (t - t0) / life, y=y, z=h * ease_out((t - t0) / life), s=max(0.001, 1 - ((t - t0) / life) ** 2))))
    return fx


# ============================================================================ weapon families
def make_thuong(g):
    px = GPX[g]
    ramp = RAMP[GROUP[g]]
    pv = (int(px * 0.12), px // 2)
    fx = Fx("thuong_dam_%d" % g, frames=6, fps=20, halo=0.7 + 0.07 * g, px=px, pivot=pv, zoom=1.0,
            name_vi="Thương đâm %d" % g, where="spear / halberd thrust: a lance of light stabbing right from the hand; one-shot")
    hx = U(pv[0] - px / 2)
    L = U(px * 0.68)
    Wl = U(3 + 2.5 * g)

    def lance(wk, soft=False):
        n = 24
        pts, ws = [], []
        for j in range(n + 1):
            s = j / n
            pts.append((L * s, 0.0))
            # thin shaft, a leaf-shaped head over the last 30 %, sharp point
            head = max(0.0, (s - 0.62) / 0.38)
            w = 0.28 + 0.72 * math.sin(PI * min(1, head * 1.0)) ** 0.8 * (1 - head) ** 0.25 if head > 0 else 0.28
            if s > 0.985:
                w = 0.04
            ws.append(Wl * wk * w + 0.004)
        return MB().strip(pts, ws, soft=soft)
    HD = [0.5, 1.05, 1.1, 1.1, 1.1, 1.1]
    TL = [-0.4, -0.35, -0.1, 0.3, 0.6, 0.88]
    SX = [0.75, 1.0, 1.04, 1.06, 1.07, 1.08]
    for nm, mb, fm in (("halo", lance(2.4, True), fx.mat("halo", ramp[1], grad=dict(src="attr", pow=1.3), window=True)),
                       ("body", lance(1.0), fx.mat("body", ramp[2], window=True)),
                       ("core", lance(0.38), fx.mat("core", ramp[3], window=True))):
        ob = mb.build(fx, nm, fm)
        fx.track(ob, lambda t, i: dict(x=hx, sx=SX[i], sy=[0.8, 1.0, 0.9, 0.75, 0.55, 0.4][i], head=HD[i], tail=TL[i]))
    # air-pierce rings (seen edge-on: tall thin ellipses) sliding along the shaft
    rm = fx.mat("ring", ramp[2])
    for j in range(g + 1):
        xr = L * (0.35 + 0.5 * j / max(g, 1))
        ob = MB().ring(0, 0, U(6 + 3 * g) * (0.7 + 0.3 * j / max(g, 1)), U(1.2), seg=28, kx=0.3).build(fx, "pierce%d" % j, rm)
        fx.track(ob, lambda t, i, xr=xr, j=j: dict(x=hx + xr + U(2.5) * i, s=[0.4, 0.8, 1.0, 1.1, 1.15, 1.2][i] + 0.001,
                                                   show=(1 <= i <= 3 - (1 if j % 2 else 0))))
    # tip flare and sparks
    tm = fx.mat("tip", ramp[3])
    st = star4(MB(), 0, 0, U(4 + 2 * g), 0.14, 0.0).build(fx, "tipstar", tm)
    fx.track(st, lambda t, i: dict(x=hx + L * SX[i] * min(1.0, HD[i]), s=[0.5, 1.0, 0.8, 0.5, 0.2, 0.0][i] + 0.001, show=i < 5))
    rng = fx.rng
    for j in range(4 + 2 * g):
        a = rng.uniform(-0.6, 0.6)
        sp = U(rng.uniform(8, 14))
        spark(fx, "sp%d" % j, tm if j % 2 else rm, "diamond", rng.uniform(1.4, 2.2) + 0.2 * g, hx + L * 0.95, 0.0,
              math.cos(a) * sp * 0.4 + U(2), math.sin(a) * sp, 0.12 + rng.uniform(0, 0.15), 0.7)
        _rotate_track(fx, fx.col.objects["SM_%s_sp%d" % (fx.id, j)], a * 0.6)
    if g >= 2:     # speed lines above and below the lance
        sl = fx.mat("lines", ramp[2], window=True, grad=dict(src="attr", pow=0.3))
        mb = MB()
        for off, a_, b_ in ((U(5 + 2 * g), 0.25, 0.85), (-U(5 + 2 * g), 0.15, 0.75), (U(9 + 3 * g), 0.4, 0.8)):
            nn = 10
            b0 = len(mb.v)
            mb.strip([(L * (a_ + (b_ - a_) * s / nn), off) for s in range(nn + 1)],
                     [U(1.1) * math.sin(PI * s / nn) ** 0.5 + 0.004 for s in range(nn + 1)])
            for q in range(nn + 1):
                for z in range(3):
                    mb.u[b0 + q * 3 + z] = a_ + (b_ - a_) * q / nn
        ob = mb.build(fx, "lines", sl)
        fx.track(ob, lambda t, i: dict(x=hx, sx=SX[i], head=HD[i] - 0.05, tail=TL[i] + 0.08))
    if g >= 3:     # lightning crawling along the lance
        bm = fx.mat("bolt", ramp[3])
        per_frame_opt(fx, "bolt", bm, lambda t, i: None if not 1 <= i <= 3 else
                      bolt_line(MB(), (hx + L * 0.15, 0), (hx + L * 0.9, 0), random.Random(i + 3), U(1.3), 8, U(5), 2))
    if g == 4:     # side fins of light + cracks of space at the point
        fin = fx.mat("fin", RAMP["flame"][2], window=True)
        mb = MB()
        for sgn in (1, -1):
            pts = [(L * (0.45 + 0.4 * s / 12), sgn * U(4 + 9 * math.sin(PI * s / 12) * (s / 12))) for s in range(13)]
            b0 = len(mb.v)
            mb.strip(pts, [U(2.2) * math.sin(PI * s / 12) + 0.004 for s in range(13)])
            for q in range(13):
                for z in range(3):
                    mb.u[b0 + q * 3 + z] = 0.45 + 0.4 * q / 12
        ob = mb.build(fx, "fins", fin)
        fx.track(ob, lambda t, i: dict(x=hx, sx=SX[i], head=HD[i], tail=TL[i]))
        cm = fx.mat("crack", RAMP["cosmic"][2])
        per_frame_opt(fx, "crack", cm, lambda t, i: None if not 1 <= i <= 4 else
                      _cracks_at(MB(), (hx + L * 1.0, 0), [D(30), D(-35), D(5)], U(12) * [0, 0.6, 1, 1, 0.9][i], U(1.6) * [0, 1, 1, 0.7, 0.45][i]))
    return fx


def _cracks_at(mb, p, angs, L, w):
    for k, a in enumerate(angs):
        crack(mb, p, a, L, random.Random(300 + k), w, 1)
    return mb


def make_chuy(g):
    px = GPX[g]
    ramp = RAMP[GROUP[g]]
    fx = Fx("chuy_chan_%d" % g, view="ground", frames=7, fps=16, halo=0.7 + 0.07 * g, px=px, ground=True, zoom=1.0,
            name_vi="Chùy chấn %d" % g, where="mace / axe smash: shock ring and cracks on the ground (under characters); one-shot")
    rng = fx.rng
    Rm = U(px * 0.42)
    glow = fx.mat("glow", ramp[1], grad=dict(src="radial", pow=1.6), opacity=0.9)
    body = fx.mat("body", ramp[2])
    core = fx.mat("core", ramp[3])
    F = MB().disc(0, 0, 1.0, 32, 1, 0).build(fx, "flash", glow)
    fx.track(F, lambda t, i: dict(s=Rm * [0.45, 0.7, 0.8, 0.75, 0.6, 0.4, 0.2][i], op=[1, 0.9, 0.65, 0.4, 0.25, 0.12, 0.0][i] + 0.001))
    C = MB().disc(0, 0, 1.0, 24).build(fx, "white", core)
    fx.track(C, lambda t, i: dict(s=Rm * [0.28, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0][i] + 0.001, show=i < 3))

    def ring(t, i, rk, w_k, lag=0.0):
        tt = t - lag
        if tt < 0:
            return None
        r = Rm * rk * (0.2 + 0.8 * ease_out(min(1, tt * 1.1)))
        w = U(1.5 + g) * (1 - tt) ** 0.7 * w_k + U(0.7)
        return MB().ring(0, 0, r, w, seg=56)
    for j, (rk, lag) in enumerate([(1.0, 0.0)] + ([(0.7, 0.18)] if g >= 2 else []) + ([(0.45, 0.35)] if g >= 4 else [])):
        per_frame_opt(fx, "ringb%d" % j, body, lambda t, i, rk=rk, lag=lag: ring(t, i, rk, 1.0, lag))
        per_frame_opt(fx, "ringc%d" % j, core, lambda t, i, rk=rk, lag=lag: ring(t, i, rk, 0.4, lag))
    GRW = [0.35, 0.75, 1.0, 1.0, 1.0, 1.0, 0.95]
    WD = [1.0, 1.0, 1.0, 0.85, 0.65, 0.45, 0.3]

    def cracks(t, i, w_k):
        mb = MB()
        n = 5 + 2 * g
        for k in range(n):
            a = TAU * k / n + 0.3
            crack(mb, (math.cos(a) * U(3), math.sin(a) * U(3)), a, Rm * random.Random(k).uniform(0.6, 0.95) * GRW[i],
                  random.Random(20 + k), U((1.6 + 0.3 * g) * WD[i] * w_k), 2 if g >= 2 else 1)
        return mb
    per_frame_opt(fx, "crack", body, lambda t, i: cracks(t, i, 1.0))
    per_frame_opt(fx, "crackc", core, lambda t, i: cracks(t, i, 0.4) if i < 4 else None)
    # debris thrown up (z = up)
    for j in range(5 + 3 * g):
        a = rng.uniform(0, TAU)
        rr = Rm * rng.uniform(0.2, 0.6)
        h = U(rng.uniform(8, 14) + 3 * g)
        ob = MB().diamond(0, 0, U(2.6), U(1.6), rng.uniform(0, PI)).build(fx, "deb%d" % j, core if j % 2 else body)
        fx.track(ob, lambda t, i, a=a, rr=rr, h=h: dict(x=math.cos(a) * rr * ease_out(t), y=math.sin(a) * rr * ease_out(t),
                                                         z=h * 4 * t * (1 - t), s=max(0.001, 1 - t ** 1.5)))
    if g >= 3:
        per_frame_opt(fx, "bolt", core, lambda t, i: None if not 0 <= i <= 3 else _ground_bolts(MB(), random.Random(i + 9), Rm, g))
    return fx


def _ground_bolts(mb, r, Rm, g):
    for k in range(g - 1):
        a = r.uniform(0, TAU)
        bolt_line(mb, (0, 0), (math.cos(a) * Rm * 0.8, math.sin(a) * Rm * 0.8), r, U(1.5), 6)
    return mb


def make_cung(g):
    px = GPX[g]
    ramp = RAMP[GROUP[g]]
    fx = Fx("cung_ten_%d" % g, frames=4, fps=14, loop=True, halo=0.7 + 0.07 * g, px=px, zoom=1.0,
            name_vi="Tiễn khí %d" % g, where="arrow of light flying right (bow, hidden weapons, chakram); the game moves it")
    head_x = U(px * 0.30)
    Ls = U(px * 0.45)
    Wh = U(3 + 1.6 * g)
    mats = dict(halo=fx.mat("halo", ramp[1], grad=dict(src="attr", pow=1.3), opacity=0.85),
                body=fx.mat("body", ramp[2]), core=fx.mat("core", ramp[3]),
                trail=fx.mat("trail", ramp[1], grad=dict(src="attr", pow=0.7)))

    def arrow(tt, i, layer):
        mb = MB()
        fl = 1 + 0.08 * math.sin(TAU * tt)
        if layer == "halo":
            mb.strip([(head_x + U(2) - Ls * 1.1 * s / 10, 0) for s in range(11)], [Wh * 1.7 * fl * (1 - 0.7 * s / 10) for s in range(11)], soft=True)
        elif layer == "trail":
            for k in range(2 + g):
                y = (k - (1 + g) / 2) * U(2.2 + 0.4 * g)
                L = U(px * (0.35 + 0.1 * math.sin(TAU * tt + k * 2.1)))
                x0 = head_x - U(6)
                mb.strip([(x0 - L * s / 10, y * (1 + 0.3 * s / 10) + U(0.8) * math.sin(TAU * tt + s)) for s in range(11)],
                         [U(1.6 + 0.3 * g) * (1 - s / 10) ** 1.1 + 0.004 for s in range(11)], soft=True)
        elif layer == "body":
            mb.poly([(head_x + U(3), 0), (head_x - U(5 + g), Wh * 0.9), (head_x - U(3 + g * 0.5), 0), (head_x - U(5 + g), -Wh * 0.9)])
            mb.strip([(head_x - U(3), 0), (head_x - Ls, 0)], [U(1.6 + 0.3 * g), U(0.8)])
            for k in range(2 + (g >= 3)):      # fletching chevrons of light
                x = head_x - Ls * (0.75 + 0.12 * k)
                for sg in (1, -1):
                    mb.strip([(x, 0), (x - U(4 + g), sg * U(3 + g))], [U(1.4), U(0.6)])
        elif layer == "core":
            mb.poly([(head_x + U(1.5), 0), (head_x - U(3 + g * 0.6), Wh * 0.35), (head_x - U(2.5), 0), (head_x - U(3 + g * 0.6), -Wh * 0.35)])
            mb.strip([(head_x - U(2), 0), (head_x - Ls * 0.7, 0)], [U(0.9), U(0.5)])
            # motes left behind
            rr = random.Random(g * 7)
            for k in range(3 + g):
                ph = rr.random()
                s = (tt + ph) % 1
                mb.diamond(head_x - U(10) - s * U(px * 0.42), rr.uniform(-1, 1) * U(3 + g), U(2.4) * (1 - s), U(1.0) * (1 - s) + 0.002)
        elif layer == "acc":
            if g >= 3:
                r = random.Random(g * 50 + i)
                bolt_line(mb, (head_x - U(2), 0), (head_x - Ls * 0.9, r.uniform(-1, 1) * U(2)), r, U(1.2), 7, U(4), 1)
            if g == 4:
                for k in range(3):
                    ph = (tt + k / 3) % 1
                    star4(mb, head_x - U(8) - ph * U(40), (k - 1) * U(7), U(3.5) * math.sin(PI * ph) + U(0.3), 0.15)
            if not mb.v:
                return None
        return mb
    accm = fx.mat("acc", RAMP["holy"][3] if g == 4 else ramp[3])
    mats["acc"] = accm
    for layer in ("halo", "trail", "body", "core", "acc"):
        per_frame_opt(fx, layer, mats[layer], lambda tt, i, layer=layer: arrow(tt, i, layer))
    return fx


def make_phap(g):
    px = GPX[g]
    ramp = RAMP[GROUP[g]]
    pv = (int(px * 0.62), px // 2)
    fx = Fx("phap_dan_%d" % g, frames=6, fps=12, loop=True, halo=0.75 + 0.06 * g, px=px, pivot=pv, zoom=1.0,
            name_vi="Pháp đạn %d" % g, where="spell orb with a tail flying right (gourd, staff, fan, zither); pivot = orb centre")
    ox = U(pv[0] - px / 2)
    Ro = U(3.5 + 2.2 * g)

    def orb(tt, i, layer):
        mb = MB()
        pul = 1 + 0.08 * math.sin(TAU * tt)
        if layer == "halo":
            mb.disc(ox, 0, Ro * 1.9 * pul, 28, 1, 0)
            mb.strip([(ox - Ro * 0.5 - U(px * 0.5) * s / 10, U(1) * math.sin(TAU * tt + s * 0.7) * s / 10) for s in range(11)],
                     [Ro * 2.2 * (1 - s / 10) ** 1.2 + 0.004 for s in range(11)], soft=True)
        elif layer == "body":
            mb.disc(ox, 0, Ro * pul, 24)
            for k in range(3):        # tail tongues streaming back
                y = (k - 1) * Ro * 0.5
                L = U(px * (0.32 + 0.08 * math.sin(TAU * tt + k * 2)))
                mb.strip([(ox - Ro * 0.6 - L * s / 10, y * (1 - s / 14) + U(1.2) * math.sin(TAU * tt + s * 0.9 + k)) for s in range(11)],
                         [Ro * 0.7 * (1 - s / 10) ** 1.3 + 0.004 for s in range(11)])
        elif layer == "core":
            mb.disc(ox + Ro * 0.15, 0, Ro * 0.55 * pul, 18)
            rr = random.Random(g * 5)
            for k in range(3 + g):
                ph = rr.random()
                s = (tt + ph) % 1
                mb.diamond(ox - Ro - s * U(px * 0.42), rr.uniform(-1, 1) * Ro * 0.9, U(2.4) * (1 - s), U(1.1) * (1 - s) + 0.002)
        elif layer == "ring":
            if g < 2:
                return None
            # orbit ring(s) seen at a slant, turning
            for k in range(1 if g < 4 else 2):
                ang = TAU * tt if k == 0 else -TAU * tt + 1.0      # a bead running round the orbit
                tilt = 0.6 if k == 0 else -0.5
                rad = Ro * (1.55 + 0.35 * k)
                m2 = MB().ring(0, 0, rad, U(1.1), seg=40, ky=0.35)
                ex, ey = rad * math.cos(ang), 0.35 * rad * math.sin(ang)
                m2.diamond(ex, ey, U(3.2), U(1.8), ang + PI / 2)
                m2.xform(rot=tilt)
                mb.merge(m2, dx=ox)
        elif layer == "acc":
            if g < 3:
                return None
            r = random.Random(g * 70 + i)
            for k in range(g - 1):
                a = r.uniform(0, TAU)
                bolt_line(mb, (ox + math.cos(a) * Ro * 0.6, math.sin(a) * Ro * 0.6),
                          (ox + math.cos(a) * Ro * 1.9, math.sin(a) * Ro * 1.9), r, U(1.1), 4, U(2), 0)
            if g >= 3:
                pa = []
                for k in range(5):
                    a = TAU * k / 5 + TAU * tt / 3
                    pa.append((ox + math.cos(a) * Ro * 1.35, math.sin(a) * Ro * 1.35, a + PI / 2))
                rune_marks(mb, pa, U(3.2 + 0.5 * g), random.Random(9), U(0.9))
            if g == 4:
                for k in range(3):
                    ph = (tt + k / 3) % 1
                    star4(mb, ox - Ro - ph * U(40), (k - 1) * Ro * 0.9, U(3.5) * math.sin(PI * ph) + U(0.3), 0.15)
        return mb
    mats = dict(halo=fx.mat("halo", ramp[1], grad=dict(src="attr", pow=1.4), opacity=0.8),
                body=fx.mat("body", ramp[2]), core=fx.mat("core", ramp[3]),
                ring=fx.mat("ring", ramp[2] if g < 4 else RAMP["flame"][2]),
                acc=fx.mat("acc", ramp[3] if g < 4 else RAMP["holy"][3]))
    for layer in ("halo", "body", "ring", "core", "acc"):
        per_frame_opt(fx, layer, mats[layer], lambda tt, i, layer=layer: orb(tt, i, layer))
    return fx


# ============================================================================ registry
def all_ids():
    return ([f"kiem_khi_{t}" for t in range(1, 11)] + [f"kiem_song_{t}" for t in range(2, 11)]
            + [f"kiem_no_{g}" for g in range(1, 5)] + [f"kiem_ngan_{k}" for k in range(1, 4)]
            + [f"{f}_{g}" for f in ("thuong_dam", "chuy_chan", "cung_ten", "phap_dan") for g in range(1, 5)])


def make(id):
    n = int(id.rsplit("_", 1)[1])
    ARC_K[:] = [1.0, 1.0]
    if id.startswith("kiem_khi_"):
        return make_kiem_khi(n)
    if id.startswith("kiem_song_"):
        return make_kiem_song(n)
    if id.startswith("kiem_no_"):
        return make_kiem_no(n)
    if id.startswith("kiem_ngan_"):
        return make_kiem_ngan(n)
    if id.startswith("thuong_dam_"):
        return make_thuong(n)
    if id.startswith("chuy_chan_"):
        return make_chuy(n)
    if id.startswith("cung_ten_"):
        return make_cung(n)
    if id.startswith("phap_dan_"):
        return make_phap(n)
    raise KeyError(id)
