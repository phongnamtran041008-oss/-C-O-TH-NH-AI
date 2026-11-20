"""Bích Nhãn Kim Thiềm: the three-legged golden wealth toad with jade-green eyes. Runs inside
Blender (see scene.py).

Squat and wide, warty gold skin with a hard metal glint, a cream throat and belly, two
bulging eye domes on top with glowing jade irises and slit pupils, a wide smile, and a
square-holed gold coin held in its lips (the toad of the stories). Three gold coins sit on
its back along the spine. Two front legs (skinned between shoulder and hand bones, so the
hands stay planted) and ONE big hind leg in the middle at the back: from behind and in
profile the three legs read; from the front the body hides the hind leg. It hops heavily
(big squash on landing), puffs up in windup and spits its coin in attack.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (S, armature, att, ball, box, cone, finish, glow, hexc, lerp_pose, mat, merge,
                    skin, tube, use_collection, eye_mats, set_ramp, set_root_offset)


def coin(name, m, hole, centre, normal_rot, r=0.05, t=0.016):
    """A round coin with a square hole: a short cylinder whose axis is turned by
    normal_rot (degrees) from +z, and a dark square on each face."""
    c = cone(name, r, r, t, centre, m, rot=normal_rot, seg=12)
    h = box(name + "_hole", (r * 0.42, r * 0.42, t * 1.3), centre, hole, rot=normal_rot)
    return [c, h]


def build():
    use_collection("COL_kim_thiem")
    set_root_offset((0, -0.012, 0))       # the tilted body sits back: centre the footprint on the pivot
    gold = mat("MAT_kt_skin", "#7a4c0e", "gold")
    wart = mat("MAT_kt_wart", "#e6b83a", "gold")
    belly = mat("MAT_kt_belly", "#ead9b0", "paper")
    mouth = mat("MAT_kt_mouth", "#2e2834", "hair")
    coinm = mat("MAT_kt_coin", "#e6b83a", "gold", metal=True)
    coinm["kit_priority"] = 2.5
    hole = mat("MAT_kt_coin_hole_mark", "#3a2208", "gold")
    hole["kit_priority"] = 3.0
    mcoin = glow("MAT_kt_mouthcoin", "#ffe27a", "holy", 2.0, halo=0)
    mcoin["kit_priority"] = 2.5
    iris = glow("MAT_kt_eye", "#7aec9a", "verdant", 4.0, halo=0)
    _, pupil, shine = eye_mats("kt", hexc("#2e2834"))
    blush = mat("MAT_kt_blush", "#f6b0c4", "pink")

    bones = [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0.03, 0.05), (0, 0.03, 0.20), "root"),
        ("head", (0, -0.05, 0.15), (0, -0.07, 0.28), "body"),
        ("jaw", (0, -0.04, 0.135), (0, -0.20, 0.135), "head"),
        ("eyes", (0, -0.10, 0.29), (0, -0.10, 0.35), "head"),
        ("throat", (0, -0.11, 0.08), (0, -0.11, 0.13), "head"),
        ("coin", (0, -0.20, 0.15), (0, -0.28, 0.15), "head"),
        ("shL", (0.10, -0.05, 0.14), (0.085, -0.07, 0.08), "body"),
        ("shR", (-0.10, -0.05, 0.14), (-0.085, -0.07, 0.08), "body"),
        ("handL", (0.08, -0.07, 0.05), (0.08, -0.07, 0.0), "root"),
        ("handR", (-0.08, -0.07, 0.05), (-0.08, -0.07, 0.0), "root"),
        ("hind", (0, 0.09, 0.06), (0, 0.04, 0.01), "root"),
    ]
    arm = armature("kim_thiem", bones)

    # body: a wide squat dome; warts on the flanks, three coins down the spine
    parts = [ball("kt_body", (0.19, 0.145, 0.125), (0, 0.02, 0.135), gold),
             ball("kt_belly", (0.15, 0.09, 0.07), (0, -0.04, 0.085), belly),
             ball("kt_thigh", (0.085, 0.08, 0.07), (0, 0.10, 0.085), gold)]
    for k, (x, y, z) in enumerate(((0.13, 0.0, 0.20), (-0.13, 0.0, 0.20), (0.16, 0.08, 0.14), (-0.16, 0.08, 0.14),
                                   (0.09, 0.12, 0.22), (-0.09, 0.12, 0.22), (0.17, -0.03, 0.12), (-0.17, -0.03, 0.12))):
        parts.append(ball(f"kt_wart{k}", (0.022, 0.022, 0.018), (x, y, z), wart, seg=8, rings=5))
    for k, (y, z, tilt) in enumerate(((-0.01, 0.255, -18), (0.07, 0.25, 8), (0.14, 0.215, 34))):
        parts += coin(f"kt_bcoin{k}", coinm, hole, (0, y, z), (tilt, 0, 0), r=0.036, t=0.012)
    att(arm, "body", *parts)
    # head: merged into the front of the body, eye domes on top, a wide smile
    smile = []
    for k in range(9):
        x = -0.12 + 0.03 * k
        smile.append((x, -0.05 - 0.125 * math.sqrt(max(0.0, 1 - (x / 0.15) ** 2)), 0.148 + 0.35 * x * x))
    att(arm, "head", ball("kt_head", (0.16, 0.12, 0.095), (0, -0.07, 0.19), gold),
        ball("kt_domeL", (0.065, 0.06, 0.065), (0.085, -0.085, 0.275), gold, seg=12, rings=8),
        ball("kt_domeR", (0.065, 0.06, 0.065), (-0.085, -0.085, 0.275), gold, seg=12, rings=8),
        ball("kt_blushl", (0.03, 0.01, 0.016), (0.11, -0.155, 0.185), blush, seg=6, rings=4),
        ball("kt_blushr", (0.03, 0.01, 0.016), (-0.11, -0.155, 0.185), blush, seg=6, rings=4),
        ball("kt_nostl", (0.01,) * 3, (0.025, -0.188, 0.205), mouth, seg=6, rings=4),
        ball("kt_nostr", (0.01,) * 3, (-0.025, -0.188, 0.205), mouth, seg=6, rings=4),
        tube("kt_mouth", smile, [0.013] * len(smile), mouth, seg=6))
    att(arm, "jaw", ball("kt_jaw", (0.15, 0.10, 0.04), (0, -0.09, 0.125), belly))
    att(arm, "throat", ball("kt_sac", (0.09, 0.06, 0.05), (0, -0.115, 0.095), belly, seg=12, rings=8))
    eyes = []
    for s in (1, -1):
        eyes += [ball(f"kt_iris{s}", (0.046, 0.026, 0.044), (s * 0.088, -0.13, 0.29), iris, rot=(0, 0, -s * 20), seg=10, rings=6),
                 box(f"kt_pupil{s}", (0.045, 0.012, 0.014), (s * 0.09, -0.155, 0.288), pupil, rot=(0, 0, -s * 20)),
                 ball(f"kt_shine{s}", (0.013,) * 3, (s * 0.075, -0.153, 0.31), shine, seg=6, rings=4)]
    att(arm, "eyes", *eyes)
    att(arm, "coin", *coin("kt_coin", mcoin, hole, (0, -0.205, 0.155), (90, 0, 0), r=0.058, t=0.016))
    for side, sx in (("L", 1), ("R", -1)):
        x = sx * 0.085
        leg = tube(f"kt_arm{side}", [(sx * 0.11, -0.04, 0.15), (sx * 0.11, -0.07, 0.08), (x, -0.075, 0.035)],
                   [0.04, 0.034, 0.03], gold, seg=10)
        skin(leg, arm, [f"sh{side}", f"hand{side}"], power=3.0)
        att(arm, f"hand{side}", ball(f"kt_hand{side}", (0.045, 0.04, 0.018), (x, -0.07, 0.018), wart, seg=10, rings=6),
            *[ball(f"kt_toe{side}{k}", (0.014, 0.022, 0.012), (x + (k - 1) * 0.028, -0.09, 0.012), wart, seg=6, rings=4)
              for k in range(3)])
    att(arm, "hind", ball("kt_foot", (0.055, 0.06, 0.02), (0, 0.05, 0.02), wart, seg=10, rings=6),
        ball("kt_shin", (0.05, 0.06, 0.04), (0, 0.08, 0.05), gold, seg=10, rings=6))

    # ------------------------------------------------------------------ poses
    def body(z=0.0, pitch=0.0, sq=1.0, head=0.0, puff=1.0):
        w = puff / math.sqrt(sq)
        # rest: nose up 12 degrees, propped on straight front legs (a sitting toad's wedge)
        return {"body": {"l": (0, 0, z + 0.012), "r": (pitch - 12, 0, 0), "s": (w, sq * puff, w)},
                "head": {"r": (head - pitch * 0.5 + 4, 0, 0)}}

    def limbs(hy=0.0, hz=0.0, by=0.0, bz=0.0):
        return {"handL": {"l": (0, hy, hz)}, "handR": {"l": (0, hy, hz)}, "hind": {"l": (0, by, bz)}}

    idle = []
    for i in range(4):
        p = body(0.003 * S(i, 4), 0, 1.0 + 0.02 * S(i, 4), 2 * S(i, 4, 1))
        p["throat"] = {"s": 1.0 + 0.25 * max(0.0, S(i, 4, 1.2))}
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
        p["coin"] = {"r": (0, 4 * S(i, 4), 0)}
        idle.append(p)
    W = [  # z, pitch, squash, hands (y, z), hind (y, z): the hind foot only skims
        (-0.015, 0, 0.90, (0.015, 0.0), (-0.004, 0.0)),     # gather
        (0.020, -8, 1.10, (-0.010, 0.02), (0.004, 0.0)),    # push (nose up)
        (0.042, -4, 1.12, (-0.020, 0.025), (0.006, 0.008)), # flight
        (0.012, 10, 0.96, (-0.018, 0.0), (-0.008, 0.012)),  # front lands
        (-0.028, 2, 0.84, (-0.006, 0.0), (-0.010, 0.0)),    # heavy landing: splat
        (-0.012, 0, 0.94, (0.005, 0.0), (-0.007, 0.0)),     # recover
    ]
    walk = []
    for z, pt, sq, hd, hn in W:
        p = body(z, pt, sq)
        p.update(limbs(hd[0], hd[1], hn[0], hn[1]))
        p["throat"] = {"s": 1.0 + 0.15 * (1 - sq) / 0.2}
        p["jaw"] = {"r": (4 if sq < 0.9 else 0, 0, 0)}
        walk.append(p)
    # windup: puffs itself up, rears back on its front legs, throat sac swelling
    puff = body(0.02, -14, 1.0, -4, 1.14)
    puff["throat"] = {"s": 1.7}
    puff["eyes"] = {"s": 1.1}
    puff["coin"] = {"s": 1.15}
    puff.update(limbs(0.0, 0.0, 0.0, 0.0))
    windup = [lerp_pose(idle[0], puff, 0.5), puff, merge(puff, {"throat": {"s": 1.85}, "body": {"s": (1.18, 1.16, 1.18)}}),
              merge(puff, {"throat": {"s": 1.75}})]
    # attack: spits the coin straight ahead (hit = frame 1), then a new one appears
    spit0 = body(0.0, 2, 0.97, -2)
    spit0["jaw"] = {"r": (26, 0, 0)}
    spit0["coin"] = {"l": (0, -0.05, 0.01), "s": 1.1}
    spit1 = body(-0.005, 4, 0.95, 4)
    spit1["jaw"] = {"r": (32, 0, 0)}
    spit1["coin"] = {"l": (0, -0.06, 0.08), "s": 1.25, "r": (0, 0, 40)}
    spit1["throat"] = {"s": 0.8}
    spit2 = body(0.0, -4, 1.04, -2)
    spit2["jaw"] = {"r": (18, 0, 0)}
    spit2["coin"] = {"s": 0.01}
    spit3 = body(0.0, 0, 1.0, 0)
    spit3["coin"] = {"s": 0.7}
    attack = [spit0, spit1, spit2, spit3]
    hit = [merge(body(-0.01, -4, 0.89, -8), {"eyes": {"s": (1, 0.2, 1)}, "coin": {"r": (0, 20, 0)}}),
           merge(body(0, -4, 0.95, -3), {"coin": {"r": (0, -8, 0)}})]
    # die: shocked, wobbles, keels over and flops onto its back, cream belly up, legs in the air
    flip = body(0, 0, 1.0, 0)
    flip.update(limbs(0.0, 0.03, 0.0, 0.04))
    flip["root"] = {"r": (0, 178, 0), "l": (0, 0, 0.27)}
    flip["eyes"] = {"s": (1, 0.12, 1)}
    flip["jaw"] = {"r": (14, 0, 0)}
    tip = body(0, 0, 1.0, 0)
    tip["root"] = {"r": (0, 100, 0), "l": (-0.12, 0, 0.19)}
    tip["eyes"] = {"s": (1, 0.3, 1)}
    die = [merge(body(0.01, -8, 1.08, -6, 1.06), {"eyes": {"s": 1.25}, "throat": {"s": 1.4}}),
           merge(body(0, 0, 0.96), {"root": {"r": (0, 18, 0)}, "eyes": {"s": (1, 0.5, 1)}}),
           tip, flip,
           merge(flip, {"handL": {"l": (0, 0.0, 0.05)}, "hind": {"l": (0, 0, 0.02)}}),
           merge(flip, {"handR": {"l": (0, 0.0, 0.05)}})]
    happy = []
    for i, (z, sq) in enumerate(((0.0, 0.86), (0.07, 1.12), (0.09, 1.06), (0.02, 0.94))):
        p = body(0, 0, sq, -6)
        p["root"] = {"r": (0, 0, 90 * i), "l": (0, 0, z)}
        p.update(limbs(0, z * 0.5, 0, z * 0.4))
        p["jaw"] = {"r": (20, 0, 0)}
        p["eyes"] = {"s": (1, 0.35, 1)}
        p["coin"] = {"s": 1.1 + 0.1 * S(i, 4)}
        happy.append(p)
    sleep = []
    for i in range(4):
        b = S(i, 4)
        p = body(-0.02, 4, 0.86 + 0.02 * b, 10)
        p["throat"] = {"s": 1.0 + 0.3 * max(0.0, b)}
        p["eyes"] = {"s": (1, 0.12, 1)}
        sleep.append(p)
    finish(arm, {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die,
                 "happy": happy, "sleep": sleep})
    return arm
