"""Huyết Ngạc: a blood-red marsh crocodile (Vạn Tượng Trạch, elite 64).

Runs inside Blender. Low, long and heavy: a broad flat skull with raised eye turrets, a
heavy lower jaw with a toothy grin showing even when shut, a chunky body with two rows of
dark armour scutes, sprawling legs (the shared quadruped IK keeps the feet planted) and a
tall flat tail with a crest that merges into one row. Moss strands on its back.

The body is long, so facing the camera its snout draws well below the pivot: that is the
true projection of a 1.4 m footprint centred on the monster's position. The batch declares
all its clips as ground clips for the kit QC (README, "My choices").

Clips: idle (basking, the jaw drifts open, tail sways), walk (high walk with a side-to-side
body wave), windup (crouches, head thrown up, jaws gaping wide, tail cocked), attack (lunges
and snaps shut = hit, head twist, settles), hit, die (rolls belly-up, legs in the air).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (hx, C, S, about, aim, att, ball, box, cone, lerp_pose, material, merge,
                    plate, set_root_offset, skin, tube, use_collection, write_clips)
from quadrupeds import Legs, gait, quad_armature


def build_huyet_ngac():
    use_collection("COL_huyet_ngac")
    set_root_offset((0, 0.015, 0))
    hide = material("MAT_hn_hide", hx("#94302a"), hx("#2e2834"), ramp=("red", "hair"))
    scute = material("MAT_hn_scute", hx("#5c1a1c"), hx("#94302a"), ramp=("red", "red"))
    scute["kit_shadow"] = 0.45
    belly = material("MAT_hn_belly", hx("#c9805c"), hx("#9894a2"), ramp=("skin", "bone"))
    tooth = material("MAT_hn_tooth", hx("#cfcbd3"), hx("#cfcbd3"), ramp="bone")
    mouth = material("MAT_hn_mouth", hx("#e88aa6"), hx("#e88aa6"), ramp="pink")
    eye = material("MAT_hn_eye", (1.0, 0.89, 0.48), (0.48, 0.93, 0.60), emit=6.0, glow=("holy", "verdant"))
    brow = material("MAT_hn_brow", hx("#5c1a1c"), hx("#1d1922"), ramp=("red", "hair"))
    moss = material("MAT_hn_moss", hx("#3a6a26"), hx("#3a6a26"), ramp="leaf")
    for m in (hide, scute):
        m["kit_light"] = 0.8           # mostly base and shadow: a deep blood red, lit along the top

    P = {"h": 0.24, "yf": -0.14, "yb": 0.15, "x": 0.15, "knee": 0.12,
         "head": (-0.26, 0.25), "hlen": 0.1, "jaw": (-0.26, 0.175),
         "tail": ((0.30, 0.235), (0.40, 0.235), (0.50, 0.235))}
    # the tail sweeps round to one side (a basking croc): its bones follow the curve
    tp = [(0, 0.22, 0.235), (0.03, 0.36, 0.236), (0.10, 0.46, 0.238), (0.20, 0.525, 0.24),
          (0.31, 0.55, 0.242), (0.40, 0.545, 0.244)]
    arm = quad_armature("huyet_ngac", P, extra=[
        ("tc1", tp[0], tp[1], "pelvis"), ("tc2", tp[1], tp[2], "tc1"),
        ("tc3", tp[2], tp[3], "tc2"), ("tc4", tp[3], tp[5], "tc3"),
        ("ripple", (0, 0, 0.0), (0, 0, 0.1), "root")])

    # --- body: chunky, flat-bellied, two rows of dark scutes and moss on the back
    att(arm, "chest", ball("hn_chest", (0.162, 0.18, 0.115), (0, -0.10, 0.225), hide),
        ball("hn_neck", (0.125, 0.10, 0.10), (0, -0.24, 0.225), hide),
        ball("hn_bellyf", (0.13, 0.17, 0.05), (0, -0.10, 0.13), belly))
    att(arm, "pelvis", ball("hn_rump", (0.172, 0.18, 0.12), (0, 0.10, 0.225), hide),
        ball("hn_bellyb", (0.135, 0.17, 0.05), (0, 0.10, 0.13), belly))
    for k, y in enumerate([-0.26 + 0.065 * i for i in range(8)]):
        bone = "chest" if y < 0.0 else "pelvis"
        z = 0.225 + 0.115 * math.sqrt(max(0.0, 1 - ((y - (-0.10 if y < 0 else 0.10)) / 0.21) ** 2))
        for sx in (-1, 1):
            att(arm, bone, cone(f"hn_sc{k}{sx}", 0.032, 0.012, 0.05, (sx * 0.048, y, z + 0.005),
                                scute, seg=4, rot=(0, 0, 45)))
            if 1 <= k <= 6:
                att(arm, bone, cone(f"hn_sco{k}{sx}", 0.024, 0.01, 0.035, (sx * 0.112, y + 0.03, z - 0.035),
                                    scute, seg=4, rot=(0, sx * 30, 45)))
    att(arm, "pelvis",
        aim("hn_moss1", moss, (0.07, 0.02, 0.33), (0.16, 0.10, 0.27), 0.03, 0.008, seg=5),
        aim("hn_moss2", moss, (-0.05, 0.14, 0.33), (-0.15, 0.21, 0.26), 0.026, 0.006, seg=5))
    att(arm, "chest", aim("hn_moss3", moss, (-0.06, -0.14, 0.33), (-0.15, -0.08, 0.25), 0.026, 0.006, seg=5))

    # --- head: a broad flat skull tapering to the snout, eye turrets, nostril knob
    hy = [-0.24, -0.35, -0.47, -0.57, -0.65, -0.68]
    head = tube("hn_skull", [(0, y, z) for y, z in zip(hy, (0.245, 0.24, 0.228, 0.218, 0.214, 0.214))],
                [0.13, 0.115, 0.092, 0.074, 0.064, 0.03], hide, seg=14, up=(0, 0, 1),
                squash=[(0.62, 1.0), (0.55, 1.0), (0.5, 1.0), (0.5, 1.0), (0.52, 1.0), (0.6, 1.0)])
    hd = [head, box("hn_palate", (0.15, 0.34, 0.012), (0, -0.47, 0.188), mouth),
          ball("hn_nostril", (0.035, 0.03, 0.02), (0, -0.635, 0.25), brow, seg=8, rings=5)]
    for sx in (-1, 1):
        hd += [ball(f"hn_turret{sx}", (0.048, 0.055, 0.045), (sx * 0.075, -0.31, 0.30), hide, seg=10, rings=6),
               ball(f"hn_eye{sx}", (0.034, 0.016, 0.026), (sx * 0.078, -0.355, 0.312), eye, seg=8, rings=5),
               box(f"hn_brow{sx}", (0.075, 0.03, 0.018), (sx * 0.08, -0.35, 0.345), brow, rot=(0, sx * -18, 0))]
        # upper teeth along the lip, pointing down
        for k, y in enumerate((-0.37, -0.43, -0.49, -0.55, -0.61)):
            w = 0.11 - (-0.37 - y) * 0.17
            hd.append(cone(f"hn_ut{sx}{k}", 0.016, 0.0, 0.045, (sx * (w * 0.9), y, 0.175), tooth,
                           seg=5, rot=(180, 0, 0)))
    att(arm, "head", *hd)
    jy = [-0.25, -0.37, -0.49, -0.59, -0.665]
    jaw = [tube("hn_jaw", [(0, y, z) for y, z in zip(jy, (0.165, 0.16, 0.155, 0.152, 0.152))],
                [0.115, 0.10, 0.082, 0.066, 0.04], hide, seg=12, up=(0, 0, 1),
                squash=[(0.42, 1.0)] * 5),
           box("hn_tongue", (0.13, 0.30, 0.012), (0, -0.44, 0.19), mouth),
           ball("hn_chin", (0.10, 0.19, 0.03), (0, -0.40, 0.135), belly)]
    for sx in (-1, 1):
        for k, y in enumerate((-0.40, -0.46, -0.52, -0.58, -0.64)):
            w = 0.098 - (-0.40 - y) * 0.15
            jaw.append(cone(f"hn_lt{sx}{k}", 0.015, 0.0, 0.042, (sx * w * 0.92, y, 0.195), tooth, seg=5))
    att(arm, "jaw", *jaw)

    # --- tail: tall and flat, crest plates in two rows merging into one
    tr = [0.135, 0.11, 0.088, 0.064, 0.04, 0.016]
    t = tube("hn_tail", tp, tr, hide, seg=12, up=(0, 0, 1), squash=[(1.0, 0.72)] * 6)
    skin(t, arm, ["pelvis", "tc1", "tc2", "tc3", "tc4"], power=3)
    bones = ["tc1", "tc1", "tc2", "tc3", "tc4"]
    for k in range(5):
        a, b = Vector(tp[k]), Vector(tp[k + 1])
        mid = (a + b) / 2
        top = mid.z + tr[k] * 0.95 - 0.01
        h = 0.07 - 0.009 * k
        rows = (-0.04, 0.04) if k < 2 else (0.0,)
        along = (b - a).normalized()
        across = along.cross(Vector((0, 0, 1))).normalized()
        for sx in rows:
            crest = plate(f"hn_crest{k}{sx > 0}", [(-0.05, 0.0), (0.05, 0.0), (0.03, h * 0.5), (-0.02, h)],
                          scute, tuple(Vector((mid.x, mid.y, top)) + across * sx * (1 - k * 0.25)),
                          tuple(along), (0, 0, 1), thick=0.02)
            att(arm, bones[k], crest)

    # --- sprawling legs: upper limb out to the side, lower limb down, broad clawed feet
    for side_, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            big = 1.0 if leg == "f" else 1.12
            att(arm, f"{leg}{side_}1", aim(f"hn_{leg}{side_}up", hide, (x * 0.8, y, 0.21),
                                           (x + sx * 0.055, y, 0.125), 0.06 * big, 0.048 * big, seg=8, smooth=True))
            att(arm, f"{leg}{side_}2", aim(f"hn_{leg}{side_}lo", hide, (x + sx * 0.055, y, 0.13),
                                           (x + sx * 0.05, y - 0.01, 0.03), 0.046 * big, 0.04, seg=8, smooth=True))
            ft = [ball(f"hn_{leg}{side_}foot", (0.055, 0.06, 0.024), (x + sx * 0.055, y - 0.025, 0.022), hide,
                       seg=8, rings=5)]
            for c, a_ in enumerate((-35, 0, 35)):
                ang = math.radians(a_)
                d = Vector((math.sin(ang) * sx, -math.cos(ang), 0))
                b0 = Vector((x + sx * 0.055, y - 0.04, 0.02))
                ft.append(aim(f"hn_{leg}{side_}claw{c}", tooth, tuple(b0 + d * 0.03), tuple(b0 + d * 0.075 - Vector((0, 0, 0.01))),
                              0.013, 0.0, seg=5))
            att(arm, f"{leg}{side_}3", *ft)

    # mud ripples for its death, sinking into the marsh (scaled away in every other pose)
    mud = material("MAT_hn_ripple", hx("#1b5040"), hx("#1b5040"), ramp="jade")
    for k, (rx, ry) in enumerate(((0.22, 0.15), (0.30, 0.21))):
        pts = [(rx * math.cos(2 * math.pi * i / 24), ry * math.sin(2 * math.pi * i / 24) - 0.02, 0.012)
               for i in range(25)]
        att(arm, "ripple", tube(f"hn_ripple{k}", pts, [0.018 - 0.004 * k] * 25, mud, seg=6, up=(0, 0, 1)))
    arm.scale = (0.8, 0.8, 0.8)       # after parenting: attach/skin keep world size
    _clips(arm, P)
    return arm


LIFT = -30.0
TINY = 0.001      # the head is carried raised: crocodile on the high walk, alert


def _clips(arm, P):
    L = Legs(P)

    def H(x=0.0, y=0.0, z=0.0):
        return {"r": (LIFT + x, y, z)}

    def tail(i, n, amp, lag=1.0, lift=0.0, bias=0.0):
        """Sway round the swept-aside rest curve; `bias` > 0 curls it further aside."""
        return {"tc1": {"r": (lift, 0, bias + amp * S(i, n))},
                "tc2": {"r": (lift * 0.5, 0, bias + amp * 1.1 * S(i, n, -0.9 * lag))},
                "tc3": {"r": (0, 0, bias + amp * 1.2 * S(i, n, -1.8 * lag))},
                "tc4": {"r": (0, 0, bias + amp * 1.3 * S(i, n, -2.6 * lag))}}

    idle = []
    for i in range(4):
        br = 0.006 * (0.5 - 0.5 * C(i, 4))
        p = L.plant(drop=br)
        p.update({"pelvis": {"l": (0, 0, -br)}, "chest": {"r": (-1.0 * S(i, 4), 0, 0)},
                  "head": H(-2 * S(i, 4, 0.6), 0, 3 * S(i, 4, -0.3)),
                  "jaw": {"r": (3 + 5 * (0.5 - 0.5 * C(i, 4, -0.8)), 0, 0)}})
        p.update(tail(i, 4, 5, bias=-6, lift=6))
        idle.append(p)

    walk = []
    for i in range(6):
        legs, lifts = {}, {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(i / 6 + off, 0.04, 0.045)
        bob = 0.008 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]), lift=lifts)
        p.update({"pelvis": {"l": (0, 0, bob), "r": (0, 3 * S(i, 6), 7 * S(i, 6))},
                  "chest": {"r": (0, -3 * S(i, 6), -12 * S(i, 6))},
                  "head": H(0, 0, 8 * S(i, 6)), "jaw": {"r": (4, 0, 0)}})
        p.update(tail(i, 6, 8, bias=-8, lift=6))
        walk.append(p)

    # windup: rears its front up, throws the head back and gapes - lower jaw level, upper
    # jaw thrown up, teeth bared, tail curled hard aside - held while the hit zone fills
    gape = L.plant(drop=0.03, front=(0.0, 0.0), back=(-0.02, -0.02), pitch=-8)
    gape.update({"pelvis": {"l": (0, 0, -0.03), "r": (-3, 0, 0)}, "chest": {"r": (-8, 0, 0)},
                 "head": H(-40), "jaw": {"r": (50, 0, 0)}})
    gape.update(tail(0, 4, 0, bias=-14, lift=8))
    windup = [lerp_pose(idle[0], gape, 0.5), gape,
              merge(gape, {"head": H(-42, 0, 3), "tc4": {"r": (0, 0, -22)}}),
              merge(gape, {"head": H(-41, 0, -3), "tc4": {"r": (0, 0, -8)}})]

    # attack: lunges with the jaws still wide (f0), snaps them shut on the target (f1 =
    # hit), wrenches its head sideways - the start of a death roll (f2), settles (f3)
    lunge = L.plant(drop=0.01, front=(0.03, 0.03), back=(0.04, 0.04), pitch=-4)
    lunge.update({"root": {"l": (0, -0.015, 0)}, "pelvis": {"l": (0, 0, -0.01)},
                  "chest": {"r": (-4, 0, 0)}, "head": H(-24), "jaw": {"r": (38, 0, 0)}})
    lunge.update(tail(0, 4, 0, bias=-2, lift=6))
    snap = L.plant(drop=0.02, front=(0.04, 0.04), back=(0.05, 0.05), pitch=0)
    snap.update({"root": {"l": (0, -0.02, 0)}, "pelvis": {"l": (0, 0, -0.02)},
                 "head": H(2), "jaw": {"r": (0, 0, 0)}})
    snap.update(tail(0, 4, 0, bias=4, lift=6))
    wrench = merge(snap, {"root": {"l": (0, -0.02, 0)}, "head": H(0, 26, -18),
                          "chest": {"r": (2, 8, -8)}})
    wrench.update(tail(0, 4, 0, bias=-14, lift=6))
    settle = lerp_pose(wrench, idle[0], 0.6)
    settle.update(L.plant(drop=0.01, front=(0.02, 0.02), back=(0.02, 0.02)))
    settle["root"] = {"l": (0, -0.015, 0)}
    settle["head"] = H(0, 4, -4)
    attack = [lunge, snap, wrench, settle]

    hit = [merge(L.plant(drop=0.012, front=(0.03, 0.03), back=(0.0, 0.0), pitch=-6),
                 {"root": {"l": (0, 0.015, 0)}, "pelvis": {"l": (0, 0, -0.012)},
                  "chest": {"r": (-6, 0, 8)}, "head": H(-14, 0, 14), "jaw": {"r": (22, 0, 0)},
                  "tc1": {"r": (6, 0, -8)}, "tc2": {"r": (4, 0, -10)}}),
           merge(L.plant(drop=0.005, front=(0.012, 0.012), pitch=-2),
                 {"root": {"l": (0, 0.01, 0)}, "pelvis": {"l": (0, 0, -0.005)}, "chest": {"r": (-2, 0, 3)},
                  "head": H(-5, 0, 5), "jaw": {"r": (8, 0, 0)}})]

    # die: a last thrash with the jaws thrown up, then it sinks into the marsh (the
    # holdout ground cuts what goes under), jaws to the sky, in a ring of mud ripples
    def sink(z, head, jaw, rip, tl=1.0):
        p = L.plant(drop=0.04, pitch=-6)
        p.update({"root": {"l": (0, 0.45 * z, -z)}, "pelvis": {"l": (0, 0, -0.04)}, "chest": {"r": (-6, 0, 0)},
                  "head": H(head), "jaw": {"r": (jaw, 0, 0)}, "ripple": {"l": (0, -0.45 * z, z), "s": rip}})
        p.update(tail(0, 4, 0, bias=-4, lift=-50))   # the tail goes under first
        p["tc1"]["s"] = tl
        return p
    thrash = merge(hit[0], {"head": H(-36, 0, 20), "jaw": {"r": (40, 0, 0)}})
    die = [hit[0], thrash, sink(0.06, -40, 40, 0.7, 0.4), sink(0.16, -50, 32, 0.9, 0.15),
           sink(0.26, -56, 22, 1.0, TINY), sink(0.34, -58, 12, 1.0, TINY)]
    for clip_poses in (idle, walk, windup, attack, hit, die):
        for p in clip_poses:
            p.setdefault("ripple", {"s": TINY})
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
