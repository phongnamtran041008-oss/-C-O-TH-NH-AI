"""Lôi Ưng: a thunder hawk (Lưu Vân Cốc, elite 64, hovers).

Runs inside Blender. A raptor held in a hover: storm-blue back and broad wings, a pale
barred chest, a dark-crowned head with a hooked gold beak, a fierce glowing eye under a hard
brow and a crest of swept-back feathers, a fanned tail, gold legs with dark talons. The
wings are two-bone (arm, hand): broad coverts on the arm, five separate primaries fanned
on the hand like fingers - the hawk silhouette - and every primary and crest tip glows with
lightning. A `spark` bone carries crackling bolts that only show while it charges.

Clips: idle (hovering wingbeats, the hand lagging the arm, head held still), walk (flying
forward, pitched in), windup (rises, folds its wings tight into a stoop, head down at the
target, lightning crackling round it - held), attack (dives, flares its wings to brake and
strikes with its talons thrust forward = hit, beats back up), hit, die (tumbles down and
lies on its side, wings spread).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (hx, C, S, aim, armature, att, ball, bolt, cone, hover_shadow, lerp_pose,
                    material, merge, plate, use_collection, write_clips, zigzag)

TINY = 0.001
COVERT = [(0.0, -0.045), (0.12, -0.05), (0.25, -0.04), (0.26, 0.06), (0.22, 0.12), (0.10, 0.15), (0.0, 0.13)]
SECOND = [(0.0, 0.10), (0.25, 0.04), (0.255, 0.13), (0.20, 0.20), (0.12, 0.215), (0.0, 0.19)]
FEATHER = [(-0.021, 0.0), (0.021, 0.0), (0.023, 0.2), (0.015, 0.27), (0.0, 0.30), (-0.017, 0.26)]
TIP = [(-0.019, 0.245), (0.02, 0.24), (0.015, 0.275), (0.0, 0.31), (-0.017, 0.27)]
SHOULDER = 0.07
ARM_LEN = 0.24


def build_loi_ung():
    use_collection("COL_loi_ung")
    back = material("MAT_lu_back", hx("#3c5e9c"), hx("#463c4c"), ramp=("blue", "hair"))
    dark = material("MAT_lu_dark", hx("#243a6a"), hx("#1d1922"), ramp=("blue", "hair"))
    chest = material("MAT_lu_chest", hx("#cfcbd3"), hx("#94302a"), ramp=("bone", "red"))
    slate = material("MAT_lu_slate", hx("#243a6a"), hx("#2e2834"), ramp=("blue", "hair"))
    bar = material("MAT_lu_bar_line", hx("#3c5e9c"), hx("#2e2834"), ramp=("blue", "hair"))
    gold = material("MAT_lu_gold", hx("#e6b83a"), hx("#e6b83a"), ramp="gold")
    talon = material("MAT_lu_talon", hx("#1d1922"), hx("#cfcbd3"), ramp=("hair", "bone"))
    eye = material("MAT_lu_eye", (1.0, 0.89, 0.48), (1.0, 0.45, 0.2), emit=7.0, glow=("holy", "flame"))
    brow = material("MAT_lu_brow", hx("#1d1922"), hx("#1d1922"), ramp="hair")
    tip = material("MAT_lu_tip", (0.72, 0.75, 1.0), (1.0, 0.89, 0.48), emit=5.0, glow=("thunder", "holy"))
    tip["kit_priority"] = 2.5
    tip["kit_halo"] = 0
    bolt_m = material("MAT_lu_bolt", (0.72, 0.75, 1.0), (1.0, 0.89, 0.48), emit=6.0, glow=("thunder", "holy"))
    for m in (back, dark, slate):
        m["kit_light"] = 0.66

    bones = [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hover", (0, 0, 0.78), (0, 0, 0.88), "root"),
        ("body", (0, 0.04, 0.72), (0, -0.04, 0.92), "hover"),
        ("head", (0, -0.06, 0.94), (0, -0.08, 1.05), "body"),
        ("tail", (0, 0.07, 0.70), (0, 0.17, 0.52), "body"),
        ("spark", (0, 0, 0.8), (0, 0, 0.9), "body"),
    ]
    for sx, side in ((1, "l"), (-1, "r")):
        bones += [
            (f"arm_{side}", (sx * SHOULDER, -0.01, 0.88), (sx * (SHOULDER + ARM_LEN), 0.0, 0.88), "body"),
            (f"hand_{side}", (sx * (SHOULDER + ARM_LEN), 0.0, 0.88), (sx * (SHOULDER + ARM_LEN + 0.2), 0.02, 0.88),
             f"arm_{side}"),
            (f"leg_{side}", (sx * 0.05, 0.0, 0.70), (sx * 0.05, -0.02, 0.60), "body"),
            (f"foot_{side}", (sx * 0.05, -0.02, 0.60), (sx * 0.05, -0.04, 0.53), f"leg_{side}"),
        ]
    arm = armature("loi_ung", bones)

    # --- body: storm-blue back, pale barred chest, tilted like a hovering raptor
    att(arm, "body", ball("lu_back", (0.11, 0.12, 0.16), (0, 0.025, 0.81), slate, rot=(-22, 0, 0)),
        ball("lu_chest", (0.098, 0.085, 0.14), (0, -0.045, 0.80), chest, rot=(-22, 0, 0)),
        *[aim(f"lu_bar{k}", bar, (-0.06 + 0.005 * k, -0.105 + 0.006 * k, z), (0.06 - 0.005 * k, -0.105 + 0.006 * k, z),
              0.011, 0.011, seg=5) for k, z in enumerate((0.84, 0.79, 0.74))],
        ball("lu_neck", (0.075, 0.07, 0.07), (0, -0.05, 0.92), chest))
    # --- head: dark crown, pale cheek, hooked gold beak, glowing eye under a hard brow,
    # a crest of swept-back feathers with lightning tips
    hd = [ball("lu_head", (0.088, 0.095, 0.082), (0, -0.085, 0.995), back),
          ball("lu_crown", (0.075, 0.08, 0.045), (0, -0.075, 1.04), slate),
          ball("lu_throat", (0.06, 0.05, 0.05), (0, -0.125, 0.955), chest),
          aim("lu_beak", gold, (0, -0.16, 0.99), (0, -0.225, 0.975), 0.032, 0.01, seg=8),
          aim("lu_hook", gold, (0, -0.215, 0.982), (0, -0.228, 0.945), 0.013, 0.0, seg=6)]
    for sx in (-1, 1):
        hd += [ball(f"lu_eye{sx}", (0.026, 0.016, 0.022), (sx * 0.056, -0.145, 1.008), eye, seg=8, rings=5),
               aim(f"lu_brow{sx}", brow, (sx * 0.02, -0.165, 1.036), (sx * 0.085, -0.12, 1.03), 0.016, 0.012, seg=5),
               aim(f"lu_stripe{sx}", brow, (sx * 0.075, -0.125, 1.0), (sx * 0.085, -0.04, 0.975), 0.014, 0.008, seg=5)]
    for k, (x, z, ang) in enumerate(((0.0, 1.06, 0), (0.035, 1.05, 18), (-0.035, 1.05, -18))):
        d = Vector((math.sin(math.radians(ang)) * 0.4, 1.0, 0.35)).normalized()
        o = Vector((x, -0.05, z))
        u = d.cross(Vector((0, 0, 1))).normalized()
        hd.append(plate(f"lu_crest{k}", [(x_ * 0.9, y_ * 0.6) for x_, y_ in FEATHER], slate, o, u, d, thick=0.014))
        hd.append(plate(f"lu_crest_tip{k}", [(x_ * 0.9, y_ * 0.6) for x_, y_ in TIP], tip, o, u, d, thick=0.02))
    att(arm, "head", *hd)

    # --- wings: arm (coverts + secondaries), hand (five fanned primaries, glowing tips)
    for sx, side in ((1, "l"), (-1, "r")):
        U, V = Vector((sx, 0, 0)), Vector((0, 1, 0))
        o = Vector((sx * SHOULDER, -0.01, 0.88))
        att(arm, f"arm_{side}", plate(f"lu_covert{side}", COVERT, back, o, U, V, thick=0.03),
            plate(f"lu_second{side}", SECOND, slate, o - Vector((0, 0, 0.006)), U, V, thick=0.02))
        h = Vector((sx * (SHOULDER + ARM_LEN), 0.0, 0.88))
        prim = [ball(f"lu_wrist{side}", (0.05, 0.06, 0.025), tuple(h + Vector((0, 0.02, 0))), back, seg=8, rings=5)]
        for k, ang in enumerate((0, 14, 28, 42, 57)):
            a = math.radians(ang)
            d = (U * math.cos(a) + V * math.sin(a)).normalized()       # fanned outward then back
            u = d.cross(Vector((0, 0, 1))) * sx
            ln = 1.15 - 0.06 * k
            sh = [(x_, y_ * ln) for x_, y_ in FEATHER]
            st = [(x_, y_ * ln) for x_, y_ in TIP]
            base = h + V * (0.012 * k) - Vector((0, 0, 0.004 * k))
            prim.append(plate(f"lu_prim{side}{k}", sh, slate, base, u, d, thick=0.014))
            prim.append(plate(f"lu_prim_tip{side}{k}", st, tip, base, u, d, thick=0.02))
        att(arm, f"hand_{side}", *prim)
        # legs: feathered thigh, gold shank, three talons forward and one back
        att(arm, f"leg_{side}", ball(f"lu_thigh{side}", (0.045, 0.05, 0.06), (sx * 0.05, -0.005, 0.68), chest),
            aim(f"lu_shank{side}", gold, (sx * 0.05, -0.01, 0.65), (sx * 0.05, -0.02, 0.59), 0.019, 0.016, seg=6))
        ft = []
        for c, dx in enumerate((-0.022, 0.0, 0.022)):
            ft.append(aim(f"lu_toe{side}{c}", gold, (sx * 0.05, -0.02, 0.585), (sx * 0.05 + dx, -0.055, 0.565),
                          0.012, 0.01, seg=5))
            ft.append(aim(f"lu_talon{side}{c}", talon, (sx * 0.05 + dx, -0.055, 0.565), (sx * 0.05 + dx * 1.1, -0.07, 0.54),
                          0.01, 0.0, seg=5))
        ft.append(aim(f"lu_heel{side}", talon, (sx * 0.05, -0.01, 0.585), (sx * 0.05, 0.03, 0.555), 0.01, 0.0, seg=5))
        att(arm, f"foot_{side}", *ft)

    # --- tail: a fan of six feathers, pale bands, glowing tips
    tl = []
    for k, ang in enumerate((-30, -18, -6, 6, 18, 30)):
        a = math.radians(ang)
        d = Vector((math.sin(a) * 0.9, math.cos(a) * 0.55, -math.cos(a) * 0.83)).normalized()
        u = Vector((math.cos(a), 0, 0.0)) if abs(d.x) < 0.99 else Vector((0, 1, 0))
        u = (u - d * u.dot(d)).normalized()
        o = Vector((0, 0.08, 0.70))
        tl.append(plate(f"lu_tailf{k}", [(x_ * 1.2, y_ * 0.62) for x_, y_ in FEATHER],
                        slate if k in (0, 5) else back, o + Vector((0, 0.004 * abs(k - 2.5), 0)), u, d, thick=0.016))
        tl.append(plate(f"lu_tail_tip{k}", [(x_ * 1.2, y_ * 0.62) for x_, y_ in TIP], tip,
                        o + Vector((0, 0.004 * abs(k - 2.5), 0)), u, d, thick=0.022))
    att(arm, "tail", *tl)

    # --- crackling lightning round it while it charges
    bl = []
    for k, (a, b) in enumerate((((0.12, -0.04, 1.10), (0.32, 0.0, 0.88)), ((-0.12, -0.04, 1.08), (-0.30, 0.02, 0.84)),
                                ((0.14, -0.08, 0.74), (0.30, -0.04, 0.56)), ((-0.12, -0.10, 0.72), (-0.28, -0.06, 0.54)),
                                ((0.0, -0.06, 1.16), (0.06, -0.02, 1.32)), ((0.20, 0.06, 0.96), (0.36, 0.10, 1.08)),
                                ((-0.20, 0.06, 0.94), (-0.34, 0.10, 1.06)))):
        bl += bolt(f"lu_bolt{k}_", zigzag(a, b, 4, 0.035, seed=k, side=(0, -1, 0)), 0.015, bolt_m)
    att(arm, "spark", *bl)
    hover_shadow("lu_shadow", 0.16, 0.12, arm)
    _clips(arm)
    return arm


def wings(up, hand=0.0, sweep=0.0, hsweep=0.0, twist=0.0):
    """up: arm raised (deg) from level; hand: extra raise of the hand; sweep: arm swung
    back (deg); hsweep: hand folded back on the arm; twist: leading edge pitched down."""
    return {"arm_l": {"r": (twist, -up, sweep)}, "arm_r": {"r": (twist, up, -sweep)},
            "hand_l": {"r": (0, -hand, hsweep)}, "hand_r": {"r": (0, hand, -hsweep)}}


def _clips(arm):
    off = {"spark": {"s": TINY}}
    up4 = [44, 6, -34, 2]
    hand4 = [-14, 18, 10, -26]          # the hand trails: bent down on the upstroke, up on the downstroke
    idle = []
    for i in range(4):
        p = merge(off, wings(up4[i], hand4[i], sweep=4))
        p.update({"hover": {"l": (0, 0, 0.03 * -math.sin(math.radians(up4[i])))},
                  "body": {"r": (-6, 0, 0)}, "head": {"r": (6 + 3 * math.sin(math.radians(up4[i])), 0, 0)},
                  "tail": {"r": (6 * S(i, 4, -1.0), 0, 6 * C(i, 4))},
                  "leg_l": {"r": (14 + 6 * S(i, 4, -1), 0, 0)}, "leg_r": {"r": (14 + 6 * S(i, 4, -1.3), 0, 0)}})
        idle.append(p)
    up6 = [46, 28, -8, -36, -16, 20]
    hand6 = [-16, 4, 20, 8, -18, -26]
    walk = []
    for i in range(6):
        p = merge(off, wings(up6[i], hand6[i], sweep=10, twist=6))
        p.update({"hover": {"l": (0, 0, 0.035 * -math.sin(math.radians(up6[i])))},
                  "body": {"r": (24, 0, 0)}, "head": {"r": (-20, 0, 0)},
                  "tail": {"r": (-20 + 5 * S(i, 6, -1), 0, 5 * S(i, 6))},
                  "leg_l": {"r": (50, 0, 0)}, "leg_r": {"r": (50, 0, 0)}})
        walk.append(p)

    # windup: rises and folds its wings tight back into a stoop, pitched head-down at the
    # target, talons drawn up, lightning crackling round it - held
    fold = merge(wings(-18, -10, sweep=62, hsweep=105, twist=10),
                 {"hover": {"l": (0, 0.06, 0.14)}, "body": {"r": (30, 0, 0)}, "head": {"r": (-6, 0, 0)},
                  "tail": {"r": (-26, 0, 0)}, "leg_l": {"r": (70, 0, 0)}, "leg_r": {"r": (70, 0, 0)},
                  "foot_l": {"r": (40, 0, 0)}, "foot_r": {"r": (40, 0, 0)}, "spark": {"s": 1.0}})
    windup = [merge(merge(off, wings(60, -20, sweep=20, hsweep=20)),
                    {"hover": {"l": (0, 0.03, 0.08)}, "body": {"r": (6, 0, 0)}, "tail": {"r": (-10, 0, 0)},
                     "leg_l": {"r": (40, 0, 0)}, "leg_r": {"r": (40, 0, 0)}}),
              fold,
              merge(fold, {"hover": {"l": (0.006, 0.06, 0.15)}, "spark": {"s": 1.08, "r": (0, 0, 30)}}),
              merge(fold, {"hover": {"l": (-0.006, 0.06, 0.14)}, "spark": {"s": 0.95, "r": (0, 0, -30)}})]

    # attack: drops into the dive (f0), flares its wings to brake and rakes with its talons
    # thrust forward at the target (f1 = hit), beats back up (f2), recovers (f3)
    dive = merge(merge(off, wings(-10, -6, sweep=50, hsweep=80, twist=14)),
                 {"hover": {"l": (0, -0.08, -0.10)}, "body": {"r": (52, 0, 0)}, "head": {"r": (-26, 0, 0)},
                  "tail": {"r": (-20, 0, 0)}, "leg_l": {"r": (60, 0, 0)}, "leg_r": {"r": (60, 0, 0)}})
    strike = merge(merge(off, wings(58, -24, sweep=-10, hsweep=-6, twist=-20)),
                   {"hover": {"l": (0, -0.12, -0.20)}, "body": {"r": (-28, 0, 0)}, "head": {"r": (22, 0, 0)},
                    "tail": {"r": (24, 0, 0)}, "leg_l": {"r": (-72, 0, 0)}, "leg_r": {"r": (-66, 0, 0)},
                    "foot_l": {"r": (-20, 0, 0)}, "foot_r": {"r": (-20, 0, 0)}})
    beat = merge(merge(off, wings(-30, 16, sweep=0)),
                 {"hover": {"l": (0, -0.08, -0.10)}, "body": {"r": (-12, 0, 0)}, "head": {"r": (10, 0, 0)},
                  "tail": {"r": (12, 0, 0)}, "leg_l": {"r": (-20, 0, 0)}, "leg_r": {"r": (-14, 0, 0)}})
    attack = [dive, strike, beat, lerp_pose(beat, idle[0], 0.6)]

    hit = [merge(merge(off, wings(64, -30, sweep=-14)),
                 {"hover": {"l": (0, 0.07, 0.03)}, "body": {"r": (-34, 0, 10)}, "head": {"r": (-24, 0, 14)},
                  "tail": {"r": (20, 0, 0)}, "leg_l": {"r": (-20, 0, 0)}, "leg_r": {"r": (-10, 0, 0)}}),
           merge(merge(off, wings(24, 6)), {"hover": {"l": (0, 0.03, 0.01)}, "body": {"r": (-14, 0, 4)},
                                            "head": {"r": (-6, 0, 4)}})]

    folded = wings(-10, 0, sweep=60, hsweep=100)
    die = [hit[0],
           merge(merge(off, wings(70, 30, sweep=-6)), {"hover": {"l": (0, 0.05, -0.18)}, "body": {"r": (-50, 0, 30)},
                                                       "head": {"r": (30, 0, 20)}, "leg_l": {"r": (-40, 0, 0)}}),
           merge(merge(off, wings(10, 0, sweep=50, hsweep=85)), {"hover": {"l": (0, 0.0, -0.40)},
                                                                  "body": {"r": (-70, 40, 40)}, "head": {"r": (40, 0, 30)},
                                                                  "leg_l": {"r": (-50, 0, 0)}}),
           merge(merge(off, folded), {"hover": {"l": (0, 0.05, -0.60)}, "body": {"r": (50, 0, 10)},
                                      "head": {"r": (40, 0, 40)}, "tail": {"r": (20, 0, 0)},
                                      "leg_l": {"r": (50, 0, 0)}, "leg_r": {"r": (60, 0, 0)}}),
           merge(merge(off, folded), {"hover": {"l": (0, 0.0, -0.66)}, "body": {"r": (42, 0, 16)},
                                      "head": {"r": (36, 0, 52)}, "tail": {"r": (-55, 0, 6)},
                                      "leg_l": {"r": (70, 0, 0)}, "leg_r": {"r": (70, 0, 0)}}),
           merge(merge(off, folded), {"hover": {"l": (0, 0.0, -0.67)}, "body": {"r": (44, 0, 18)},
                                      "head": {"r": (40, 0, 58)}, "tail": {"r": (-58, 0, 8)},
                                      "leg_l": {"r": (72, 0, 0)}, "leg_r": {"r": (72, 0, 0)}})]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
