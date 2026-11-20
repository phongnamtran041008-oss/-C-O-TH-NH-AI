"""Thiết Giáp Thú: a pangolin armoured in broken sword shards (Kiếm Trủng Sơn, normal 48).

Runs inside Blender. Walking form: an arched body (chest and a higher rump) on the shared
quadruped rig of MONSTERS_A (IK legs that keep the paws planted), shingled with steel shards
that are each a broken blade tip, a dorsal row of blade stubs, the hilt of a sword still
stuck in its back, a small conical head with glowing eyes and a flicking tongue, short
thick legs with digging claws and a thick shard-covered tail curling up at the tip.

Rolled form: a pangolin rolls into a ball with its tail wrapped over it. A rolled ball of
the same shards with the tail band wrapped round it and the eyes peeking out under the tail
tip lives on its own `ball` bone; clips switch between the two forms by scaling the bones
(`pelvis` carries the whole walking body). The same trick hides nothing else.

Clips: idle (sniff, tongue flick, tail sway), walk (a low trundle), windup (hunches, then
rolls into the bristling ball and rocks back on it), attack (the ball rolls forward and
slams = hit, bursts open, settles), hit, die (staggers, rolls up, tips onto its side and
uncurls limp, eyes shut).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (hx, C, S, about, aim, att, ball, lerp_pose, material, merge, plate,
                    set_root_offset, skin, tube, use_collection, write_clips)
from quadrupeds import Legs, gait, quad_armature

# a broken blade tip: the scale shape (a across, b along the back)
SHARD = [(-0.056, -0.016), (0.056, -0.016), (0.052, 0.088), (0.02, 0.158), (-0.004, 0.124),
         (-0.03, 0.14), (-0.052, 0.078)]
STUB = [(-0.034, 0.0), (0.034, 0.0), (0.032, 0.09), (0.008, 0.14), (-0.01, 0.112),
        (-0.032, 0.124)]
TINY = 0.001
BALL_C = Vector((0, 0.02, 0.20))
BALL_R = 0.19


def _body_surface(theta, t, grow=1.0):
    """Point and normal on the arched body: theta round the spine from the top (deg, + =
    toward +x), t along it (-1 front .. 1 back). The rump stands higher than the chest."""
    th = math.radians(theta)
    k = math.sqrt(max(0.0, 1 - t * t))
    cy, cz = 0.03 + 0.225 * t, 0.275 + 0.035 * t
    rx, rz = 0.15 * (1 + 0.07 * t) * grow, 0.215 * (1 + 0.04 * t - 0.12 * t * t) * grow
    p = Vector((rx * k * math.sin(th), cy, cz + rz * k * math.cos(th)))
    n = Vector((math.sin(th) * k / max(rx, 1e-3), t / 0.225, math.cos(th) * k / max(rz, 1e-3)))
    return p, n.normalized()


def _shard(name, mat, p, n, back, lift=18.0, size=1.0, outline=SHARD):
    """A shard lying on the surface at p, pointing `back`, its rear edge lifted off the
    skin by `lift` degrees so the rows overlap like shingles."""
    v = (back - n * back.dot(n)).normalized()
    a = math.radians(lift)
    v = (v * math.cos(a) + n * math.sin(a)).normalized()
    u = v.cross(n).normalized()
    pts = [(x * size, y * size) for x, y in outline]
    return plate(name, pts, mat, p + n * 0.006, u, v, thick=0.016)


def build_thiet_giap_thu():
    use_collection("COL_thiet_giap_thu")
    set_root_offset((0, 0.03, 0))
    skin_m = material("MAT_tg_skin", hx("#6c5a47"), hx("#2e2834"), ramp=("earth", "hair"))
    belly = material("MAT_tg_belly", hx("#958065"), hx("#463c4c"), ramp=("earth", "hair"))
    sh_a = material("MAT_tg_shard_a", hx("#5d6e86"), hx("#b9821a"), ramp=("steel", "gold"), metal=True)
    sh_b = material("MAT_tg_shard_b", hx("#5e636f"), hx("#7a4c0e"), ramp=("stone", "gold"), metal=True)
    stub_m = material("MAT_tg_stub", hx("#94a6ba"), hx("#cfcbd3"), ramp=("steel", "bone"), metal=True)
    claw = material("MAT_tg_claw", hx("#cfcbd3"), hx("#cfcbd3"), ramp="bone")
    eye = material("MAT_tg_eye", (1.0, 0.89, 0.48), (1.0, 0.45, 0.2), emit=6.0, glow=("holy", "flame"))
    eye["kit_halo"] = 0
    nose = material("MAT_tg_nose", hx("#1d1922"), hx("#1d1922"), ramp="hair")
    tongue = material("MAT_tg_tongue", hx("#e88aa6"), hx("#e88aa6"), ramp="pink")
    grip = material("MAT_tg_grip", hx("#573420"), hx("#94302a"), ramp=("wood", "red"))
    guard = material("MAT_tg_guard", hx("#b9821a"), hx("#2e2834"), ramp=("gold", "hair"), metal=True)

    P = {"h": 0.22, "yf": -0.06, "yb": 0.06, "x": 0.09, "knee": 0.105,
         "head": (-0.19, 0.235), "hlen": 0.12, "jaw": (-0.33, 0.21),
         "tail": ((0.25, 0.30), (0.39, 0.35), (0.46, 0.405))}
    arm = quad_armature("thiet_giap_thu", P, extra=[
        ("tail3", (0, 0.46, 0.405), (0, 0.51, 0.50), "tail2"),
        ("eyes", (0, -0.31, 0.27), (0, -0.31, 0.33), "head"),
        ("ball", tuple(BALL_C), tuple(BALL_C + Vector((0, 0, 0.1))), "root"),
        ("beyes", (0, -0.17, 0.24), (0, -0.17, 0.30), "ball")])

    # ------------------------------------------------ walking form
    att(arm, "chest", ball("tg_chest", (0.135, 0.15, 0.17), (0, -0.06, 0.26), skin_m))
    att(arm, "pelvis", ball("tg_rump", (0.158, 0.17, 0.21), (0, 0.09, 0.30), skin_m),
        ball("tg_belly", (0.11, 0.2, 0.07), (0, 0.02, 0.15), belly))
    rows = [-0.8, -0.46, -0.12, 0.22, 0.56, 0.86]
    for r, t in enumerate(rows):
        thetas = (-80, -48, -16, 16, 48, 80) if r % 2 else (-64, -32, 0, 32, 64)
        for c, th in enumerate(thetas):
            p, n = _body_surface(th, t, 1.03)
            m = sh_a if r % 2 == 0 else sh_b       # rows of plates, as on a pangolin
            size = 0.78 + 0.3 * math.sqrt(max(0.0, 1 - t * t))
            att(arm, "chest" if p.y < 0.0 else "pelvis",
                _shard(f"tg_sh{r}_{c}", m, p, n, Vector((0, 1, -0.2)), size=size))
    for k, t in enumerate((-0.5, -0.12, 0.26)):
        p, n = _body_surface(0, t, 1.0)
        rake = Vector((0, 0.6, 1.0)).normalized()
        grow = (1.0, 1.25, 1.1)[k]
        st = plate(f"tg_stub{k}", [(x * grow, y * grow) for x, y in STUB], stub_m, p - n * 0.012,
                   Vector((0, rake.z, -rake.y)), rake, thick=0.018)
        att(arm, "chest" if p.y < 0.0 else "pelvis", st)
    base = Vector((0.07, 0.14, 0.45))
    g = Vector((0.3, 0.5, 1.0)).normalized()
    side = g.cross(Vector((0, 1, 0))).normalized()
    att(arm, "pelvis",
        aim("tg_hilt", grip, tuple(base), tuple(base + g * 0.14), 0.021, 0.019, seg=6),
        aim("tg_guard", guard, tuple(base + g * 0.012 - side * 0.08), tuple(base + g * 0.012 + side * 0.08),
            0.026, 0.026, seg=4),
        ball("tg_pommel", (0.028, 0.028, 0.028), tuple(base + g * 0.155), guard, seg=8, rings=5))

    # head: conical, a little big for the body (it must read from the front), glowing eyes
    HY, HZ = -0.255, 0.25
    hd = [ball("tg_head", (0.112, 0.112, 0.102), (0, HY, HZ + 0.01), skin_m),
          aim("tg_snout", skin_m, (0, HY - 0.06, HZ - 0.01), (0, HY - 0.135, HZ - 0.04), 0.066, 0.034, seg=10,
              smooth=True),
          ball("tg_nose", (0.032, 0.026, 0.026), (0, HY - 0.14, HZ - 0.042), nose, seg=8, rings=5)]
    for k, (x, y, z, th) in enumerate(((0.0, HY + 0.0, HZ + 0.075, 0), (0.05, HY + 0.02, HZ + 0.06, 42),
                                       (-0.05, HY + 0.02, HZ + 0.06, -42))):
        n = Vector((math.sin(math.radians(th)), -0.25, math.cos(math.radians(th)))).normalized()
        hd.append(_shard(f"tg_crown{k}", sh_a if k == 0 else sh_b, Vector((x, y - 0.03, z)), n,
                         Vector((0, 1, 0)), lift=24, size=0.62))
    att(arm, "head", *hd)
    att(arm, "eyes", *[ball(f"tg_eye{s}", (0.032, 0.018, 0.032), (s * 0.064, HY - 0.08, HZ + 0.03), eye,
                            seg=8, rings=5) for s in (-1, 1)])
    att(arm, "jaw", aim("tg_tongue", tongue, (0, -0.36, 0.208), (0, -0.48, 0.20), 0.013, 0.009, seg=6))

    # tail: a thick skinned core continuing the arch, shards along its top and sides
    tp = [(0, 0.20, 0.29), (0, 0.30, 0.315), (0, 0.39, 0.35), (0, 0.46, 0.405), (0, 0.50, 0.465),
          (0, 0.51, 0.52)]
    rads = [0.14, 0.12, 0.095, 0.07, 0.046, 0.022]
    core = tube("tg_tail", tp, rads, skin_m, seg=12, up=(0, 0, 1))
    skin(core, arm, ["pelvis", "tail1", "tail2", "tail3"], power=3)
    for k in range(len(tp) - 1):
        a, b = Vector(tp[k]), Vector(tp[k + 1])
        dirn = (b - a).normalized()
        mid = (a + b) / 2
        bone = ["pelvis", "tail1", "tail2", "tail3", "tail3"][k]
        up = Vector((0, 0, 1)) - dirn * dirn.z
        up.normalize()
        sidev = dirn.cross(up).normalized()
        for j, ang in enumerate((-80, -40, 0, 40, 80) if k < 3 else (-55, 0, 55)):
            n = (up * math.cos(math.radians(ang)) + sidev * math.sin(math.radians(ang))).normalized()
            att(arm, bone, _shard(f"tg_tsh{k}_{j}", sh_a if (k + j) % 2 else sh_b,
                                  mid + n * rads[k] * 0.85, n, dirn, lift=14, size=1.0 - 0.13 * k))

    for side_, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side_}1", aim(f"tg_{leg}{side_}up", skin_m, (x, y, 0.2), (x, y, 0.105),
                                           0.062, 0.05, seg=8, smooth=True))
            att(arm, f"{leg}{side_}2", aim(f"tg_{leg}{side_}lo", skin_m, (x, y, 0.11), (x, y, 0.035),
                                           0.05, 0.042, seg=8, smooth=True))
            paw = [ball(f"tg_{leg}{side_}paw", (0.048, 0.05, 0.028), (x, y - 0.006, 0.028), skin_m,
                        seg=8, rings=5)]
            reach = 0.045 if leg == "f" else 0.026
            for c, dx in enumerate((-0.026, 0.0, 0.026)):
                paw.append(aim(f"tg_{leg}{side_}claw{c}", claw, (x + dx, y - 0.035, 0.034),
                               (x + dx * 1.15, y - 0.035 - reach, 0.007), 0.014, 0.0, seg=5))
            att(arm, f"{leg}{side_}3", *paw)

    # ------------------------------------------------ rolled form (on the `ball` bone)
    bl = [ball("tg_ballcore", (BALL_R * 0.95,) * 3, tuple(BALL_C), skin_m, seg=14, rings=10)]
    for li, lat in enumerate((-62, -31, 0, 31, 62)):
        n_ring = 12 if abs(lat) < 40 else 8
        for k in range(n_ring):
            phi = math.radians(360 * k / n_ring + (15 if li % 2 else 0))
            la = math.radians(lat)
            n = Vector((math.sin(la), -math.cos(la) * math.sin(phi), math.cos(la) * math.cos(phi)))
            tang = Vector((0, -math.cos(phi), -math.sin(phi)))
            m = sh_a if (li + k) % 2 == 0 else sh_b
            bl.append(_shard(f"tg_bsh{li}_{k}", m, BALL_C + n * BALL_R, n, tang, lift=20,
                             size=0.95 if abs(lat) < 40 else 0.8))
    # the tail wrapped over the ball, from the back-bottom over the top to above the eyes
    for k in range(9):
        u = k / 8
        phi = math.radians(-105 + 160 * u)
        n = Vector((0, -math.sin(phi), math.cos(phi)))
        tang = Vector((0, -math.cos(phi), -math.sin(phi)))
        rr = BALL_R + 0.05 - 0.02 * u
        for j, dx in enumerate((-0.05, 0.05) if u < 0.75 else (0.0,)):
            bl.append(_shard(f"tg_band{k}_{j}", sh_a if (k + j) % 2 else stub_m,
                             BALL_C + n * rr + Vector((dx * (1.1 - 0.6 * u), 0, 0)), n, tang, lift=10,
                             size=1.1 - 0.45 * u))
    att(arm, "ball", *bl)
    att(arm, "beyes", *[ball(f"tg_beye{s}", (0.03, 0.018, 0.026),
                             (s * 0.06, BALL_C.y - BALL_R - 0.012, BALL_C.z + 0.035), eye, seg=8, rings=5)
                        for s in (-1, 1)])

    arm.scale = (0.82, 0.82, 0.82)     # set after parenting: attach/skin keep world size
    _clips(arm, P)
    return arm


def _walking(p):
    p = dict(p)
    p["ball"] = {"s": TINY}
    return p


def _rolled(rock=0.0, roll=0.0, fwd=0.0, shiver=0.0, squash=1.0, lift=0.05, eyes=1.0, tip=0.0):
    """The rolled ball (walking body hidden): rocked back by `rock`, rolled forward by
    `roll` degrees, moved `fwd` m forward, tipped onto its side by `tip` degrees."""
    s = (1.0 / squash ** 0.5, squash, 1.0 / squash ** 0.5)
    return {"pelvis": {"s": TINY, "l": (0, 0, -0.1)},
            "ball": {"r": (roll - rock, tip, shiver), "l": (0, -fwd, lift + (squash - 1) * BALL_R), "s": s},
            "beyes": {"s": (1, eyes, 1)}}


def _clips(arm, P):
    L = Legs(P)

    def tail(i, n, amp=12.0, lift=0.0):
        return {"tail1": {"r": (lift + 3 * C(i, n), 0, amp * S(i, n))},
                "tail2": {"r": (lift * 0.6 + 5 * C(i, n, -1.0), 0, amp * 1.3 * S(i, n, -1.0))},
                "tail3": {"r": (8 * C(i, n, -1.8), 0, amp * 1.5 * S(i, n, -1.8))}}

    idle = []
    for i in range(4):
        br = 0.005 * (0.5 - 0.5 * C(i, 4))
        p = L.plant(drop=br)
        p.update({"pelvis": {"l": (0, 0, -br)}, "chest": {"r": (-1.0 * S(i, 4), 0, 0)},
                  "head": {"r": (8 * S(i, 4, 0.8), 0, 10 * S(i, 4, -0.4))},
                  "jaw": {"s": (1, 1.0 if i == 2 else TINY, 1)},
                  "eyes": {"s": (1, 0.25 if i == 3 else 1.0, 1)}})
        p.update(tail(i, 4, 9))
        idle.append(_walking(p))

    walk = []
    for i in range(6):
        legs, lifts = {}, {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(i / 6 + off, 0.026, 0.035)
        bob = 0.008 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]), lift=lifts)
        p.update({"pelvis": {"l": (0, 0, bob), "r": (0, 5 * S(i, 6), 0)},
                  "chest": {"r": (0, -6 * S(i, 6), 0)},
                  "head": {"r": (12 + 4 * abs(S(i, 6)), 0, -8 * S(i, 6))},
                  "jaw": {"s": (1, TINY, 1)}})
        p.update(tail(i, 6, 15, lift=-4))
        walk.append(_walking(p))

    # windup: hunches (head tucked, back arched, tail swinging under), then it is a ball of
    # blades, rocked back on its heel and shivering - held while the hit zone fills
    hunch = L.plant(drop=0.015, front=(0.02, 0.02), back=(-0.02, -0.02), pitch=8)
    hunch.update({"pelvis": {"l": (0, 0, -0.015), "r": (-8, 0, 0)}, "chest": {"r": (8, 0, 0)},
                  "head": {"r": (14, 0, 0)}, "jaw": {"s": (1, TINY, 1)},
                  "tail1": {"r": (14, 0, 0)}, "tail2": {"r": (10, 0, 0)}, "tail3": {"r": (8, 0, 0)}})
    windup = [_walking(hunch), _rolled(rock=9), _rolled(rock=11, shiver=7), _rolled(rock=10, shiver=-7)]

    # attack: the ball rolls forward (f0), slams into the target squashed flat (f1 = hit),
    # bursts open into a low ram stance, head up and shards bristling (f2), settles (f3)
    open_ = L.plant(drop=0.03, front=(-0.02, -0.02), back=(0.02, 0.02), pitch=10)
    open_.update({"root": {"l": (0, -0.02, 0)}, "pelvis": {"l": (0, 0, -0.03)},
                  "chest": {"r": (6, 0, 0)}, "head": {"r": (-30, 0, 0)}, "jaw": {"s": (1, TINY, 1)},
                  "tail1": {"r": (26, 0, 0)}, "tail2": {"r": (22, 0, 10)}, "tail3": {"r": (16, 0, 16)}})
    settle = lerp_pose(open_, idle[0], 0.6)
    settle.update(L.plant(drop=0.012, pitch=4))
    settle["root"] = {"l": (0, -0.02, 0)}
    attack = [_rolled(roll=120, fwd=0.01, lift=0.06), _rolled(roll=360, fwd=0.015, squash=0.92, lift=0.06),
              _walking(open_), _walking(settle)]

    hit = [_walking(merge(L.plant(drop=0.012, front=(0.025, 0.025), back=(0.0, 0.0), pitch=-8),
                          {"root": {"l": (0, 0.02, 0)}, "pelvis": {"l": (0, 0, -0.012)},
                           "chest": {"r": (-8, 0, 5)}, "head": {"r": (-28, 0, 12)},
                           "jaw": {"s": (1, TINY, 1)}, "eyes": {"s": (1, 0.25, 1)},
                           "tail1": {"r": (26, 0, 0)}, "tail2": {"r": (18, 0, 0)}})),
           _walking(merge(L.plant(drop=0.005, front=(0.01, 0.01), pitch=-3),
                          {"root": {"l": (0, 0.008, 0)}, "pelvis": {"l": (0, 0, -0.005)},
                           "chest": {"r": (-3, 0, 2)}, "head": {"r": (-8, 0, 4)},
                           "jaw": {"s": (1, TINY, 1)}}))]

    # die: staggers, rolls up, tips onto its side, then lies uncurled and limp, eyes shut
    slump = merge(L.plant(drop=0.04, pitch=6),
                  {"pelvis": {"l": (0, 0, -0.04)}, "chest": {"r": (6, 0, 0)},
                   "head": {"r": (6, 0, 24)}, "jaw": {"s": (1, TINY, 1)}, "eyes": {"s": (1, 0.3, 1)},
                   "tail1": {"r": (-16, 0, 18)}, "tail2": {"r": (-10, 0, 18)}})
    limp = Legs.air((-40, 30), (-20, 20), (30, 10), (40, 0))
    limp.update({"root": about((0, 0.03, 0.10), (0, 84, 0), extra=(0, 0, -0.03)),
                 "chest": {"r": (8, 0, 0)}, "head": {"r": (24, 0, 20)}, "eyes": {"s": (1, 0.15, 1)},
                 "jaw": {"s": (1, 1.0, 1)},
                 "tail1": {"r": (-20, 0, 24)}, "tail2": {"r": (-12, 0, 20)}, "tail3": {"r": (-8, 0, 10)}})
    limp2 = merge(limp, {"fl1": {"r": (-55, 0, 0)}, "fr1": {"r": (-10, 0, 0)}, "head": {"r": (30, 0, 26)}})
    die = [hit[0], _walking(slump), _rolled(eyes=0.3), _rolled(tip=45, eyes=0.15),
           _rolled(tip=85, lift=0.02, eyes=0.08), _rolled(tip=88, lift=0.02, eyes=0.08, rock=-8)]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
