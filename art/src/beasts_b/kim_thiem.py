"""Bích Nhãn Kim Thiềm: the golden wealth toad with jade-green eyes. Runs inside Blender
(see scene.py).

Built for the side view first (lead review): a wide, low body clearly longer and broader
than it is tall; a blunt wedge of a head in front, its two eye domes bulging ABOVE the head
line with glowing jade irises and slit pupils turned out so they read in profile; a dark
mouth line that runs from the blunt snout back under each eye; a pale throat sac that puffs
in idle and a pale belly; a short front leg planted under the chest; and on each flank the
folded hind leg as its own darker shape (a big thigh, the shin folded under it, a long foot
forward on the ground). The hind legs are skinned tubes between a thigh bone on the body
and a foot bone on the root, so in the hop they really unfold as the body springs up and
fold again on landing. A square-holed gold coin sits in its lips (the toad of the stories)
and three coins run down its back; warts are bright gold bumps on gold skin.

The brief allowed three legs "if it can read, otherwise four"; one centred hind leg never
read from the side, so it has four.
"""
from __future__ import annotations

import math

from common import (S, armature, att, ball, box, cone, eye_mats, finish, glow, hexc, lerp_pose, mat,
                    merge, set_root_offset, skin, tube, use_collection)


def coin(name, m, hole, centre, normal_rot, r=0.05, t=0.016):
    """A round coin with a square hole: a short cylinder turned by normal_rot (degrees)
    from +z, and a dark square through it."""
    c = cone(name, r, r, t, centre, m, rot=normal_rot, seg=12)
    h = box(name + "_hole", (r * 0.42, r * 0.42, t * 1.3), centre, hole, rot=normal_rot)
    return [c, h]


def build():
    use_collection("COL_kim_thiem")
    set_root_offset((0, -0.005, 0))
    gold = mat("MAT_kt_skin", "#e6b83a", "gold")
    leg = mat("MAT_kt_leg", "#82522f", "wood")             # darker: the limbs separate from the flank
    wart = mat("MAT_kt_wart", "#7a4c0e", "gold")
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
        ("body", (0, 0.04, 0.05), (0, 0.04, 0.18), "root"),
        ("head", (0, -0.07, 0.12), (0, -0.09, 0.22), "body"),
        ("jaw", (0, -0.06, 0.115), (0, -0.20, 0.115), "head"),
        ("eyes", (0, -0.12, 0.23), (0, -0.12, 0.29), "head"),
        ("throat", (0, -0.12, 0.07), (0, -0.12, 0.11), "head"),
        ("coin", (0, -0.21, 0.13), (0, -0.28, 0.13), "head"),
    ]
    for side, sx in (("L", 1), ("R", -1)):
        bones += [(f"sh{side}", (sx * 0.10, -0.07, 0.13), (sx * 0.095, -0.085, 0.07), "body"),
                  (f"hand{side}", (sx * 0.09, -0.085, 0.04), (sx * 0.09, -0.085, 0.0), "root"),
                  (f"thigh{side}", (sx * 0.17, 0.17, 0.13), (sx * 0.18, 0.0, 0.075), "body"),
                  (f"foot{side}", (sx * 0.12, 0.075, 0.03), (sx * 0.115, -0.06, 0.012), "root")]
    arm = armature("kim_thiem", bones)

    # body: wide and low (0.40 across, 0.33 long, 0.20 tall), back sloping up to the head
    parts = [ball("kt_body", (0.15, 0.17, 0.095), (0, 0.05, 0.13), gold, rot=(-6, 0, 0)),
             # the pale underside: a light band along the whole bottom, throat to rump, in profile
             ball("kt_belly", (0.148, 0.15, 0.05), (0, 0.0, 0.082), belly)]
    for k, (x, y, z) in enumerate(((0.07, 0.02, 0.215), (-0.07, 0.02, 0.215), (0.06, 0.12, 0.205), (-0.06, 0.12, 0.205))):
        parts.append(ball(f"kt_wart{k}", (0.018, 0.018, 0.014), (x, y, z), wart, seg=8, rings=5))
    for k, (y, z, tilt) in enumerate(((-0.01, 0.222, -12), (0.06, 0.222, 4), (0.13, 0.20, 22))):
        parts += coin(f"kt_bcoin{k}", coinm, hole, (0, y, z), (tilt, 0, 0), r=0.034, t=0.012)
    att(arm, "body", *parts)
    # head: a blunt wedge in front, eye domes bulging above its line, mouth line running back
    mline = [(0.0, -0.222, 0.122)]
    for k in range(1, 7):
        t = k / 6
        x = 0.135 * math.sin(t * math.pi / 2)
        mline.append((x, -0.222 + 0.17 * (1 - math.cos(t * math.pi / 2)), 0.122 + 0.02 * t))
    mouthR = [(-x, y, z) for x, y, z in mline]
    att(arm, "head", ball("kt_head", (0.13, 0.11, 0.075), (0, -0.12, 0.155), gold, rot=(6, 0, 0)),
        ball("kt_snout", (0.09, 0.05, 0.045), (0, -0.19, 0.145), gold, seg=12, rings=8),
        ball("kt_domeL", (0.055, 0.055, 0.058), (0.075, -0.115, 0.24), gold, seg=12, rings=8),
        ball("kt_domeR", (0.055, 0.055, 0.058), (-0.075, -0.115, 0.24), gold, seg=12, rings=8),
        ball("kt_blushl", (0.026, 0.01, 0.014), (0.105, -0.185, 0.16), blush, seg=6, rings=4),
        ball("kt_blushr", (0.026, 0.01, 0.014), (-0.105, -0.185, 0.16), blush, seg=6, rings=4),
        ball("kt_nostl", (0.01,) * 3, (0.022, -0.235, 0.165), mouth, seg=6, rings=4),
        ball("kt_nostr", (0.01,) * 3, (-0.022, -0.235, 0.165), mouth, seg=6, rings=4),
        ball("kt_mouth", (0.137, 0.118, 0.011), (0, -0.12, 0.128), mouth, seg=24, rings=4))
    att(arm, "jaw", ball("kt_jaw", (0.12, 0.09, 0.028), (0, -0.13, 0.105), belly))
    att(arm, "throat", ball("kt_sac", (0.09, 0.06, 0.045), (0, -0.13, 0.08), belly, seg=12, rings=8))
    eyes = []
    for s in (1, -1):
        # iris on the dome, turned 35 degrees out so the profile sees it; horizontal slit pupil
        eyes += [ball(f"kt_iris{s}", (0.042, 0.03, 0.04), (s * 0.093, -0.142, 0.25), iris, rot=(0, 0, -s * 35), seg=10, rings=6),
                 box(f"kt_pupil{s}", (0.04, 0.012, 0.012), (s * 0.099, -0.162, 0.248), pupil, rot=(0, 0, -s * 35)),
                 ball(f"kt_shine{s}", (0.012,) * 3, (s * 0.083, -0.168, 0.265), shine, seg=6, rings=4)]
    att(arm, "eyes", *eyes)
    att(arm, "coin", *coin("kt_coin", mcoin, hole, (0, -0.215, 0.13), (90, 0, 0), r=0.05, t=0.016))
    for side, sx in (("L", 1), ("R", -1)):
        # short front leg planted under the chest (skinned: the hand stays on the ground)
        fl = tube(f"kt_arm{side}", [(sx * 0.11, -0.06, 0.13), (sx * 0.105, -0.085, 0.075), (sx * 0.09, -0.09, 0.03)],
                  [0.032, 0.028, 0.024], leg, seg=10)
        skin(fl, arm, [f"sh{side}", f"hand{side}"], power=3.0)
        att(arm, f"hand{side}", ball(f"kt_hand{side}", (0.04, 0.035, 0.015), (sx * 0.09, -0.09, 0.015), leg, seg=10, rings=6),
            *[ball(f"kt_toe{side}{k}", (0.012, 0.02, 0.01), (sx * 0.09 + (k - 1) * 0.024, -0.108, 0.01), wart, seg=6, rings=4)
              for k in range(3)])
        # the folded hind leg on the flank, its own dark shape: a big thigh outside the body,
        # the shin folded forward under it and back to the heel, a long foot forward on the ground
        att(arm, f"thigh{side}", ball(f"kt_thigh{side}", (0.05, 0.095, 0.058), (sx * 0.168, 0.075, 0.12), leg,
                                     rot=(18, 0, 0), seg=12, rings=8))
        hl = tube(f"kt_shin{side}", [(sx * 0.17, 0.0, 0.088), (sx * 0.155, 0.05, 0.052), (sx * 0.125, 0.085, 0.026)],
                  [0.032, 0.026, 0.02], leg, seg=10)
        skin(hl, arm, [f"thigh{side}", f"foot{side}"], power=3.0)
        att(arm, f"foot{side}", ball(f"kt_foot{side}", (0.026, 0.075, 0.013), (sx * 0.115, 0.015, 0.013), leg, seg=10, rings=6),
            *[ball(f"kt_htoe{side}{k}", (0.011, 0.02, 0.009), (sx * 0.115 + (k - 1) * 0.02, -0.06, 0.01), wart, seg=6, rings=4)
              for k in range(3)])

    # ------------------------------------------------------------------ poses
    def body(z=0.0, pitch=0.0, sq=1.0, head=0.0, puff=1.0):
        w = puff / math.sqrt(sq)
        return {"body": {"l": (0, 0, z), "r": (pitch - 5, 0, 0), "s": (w, sq * puff, w)},
                "head": {"r": (head - pitch * 0.5 + 3, 0, 0)}}

    def limbs(hy=0.0, hz=0.0, fy=0.0, fz=0.0):
        return {"handL": {"l": (0, hy, hz)}, "handR": {"l": (0, hy, hz)},
                "footL": {"l": (0, fy, fz)}, "footR": {"l": (0, fy, fz)}}

    idle = []
    for i in range(4):
        p = body(0.003 * S(i, 4), 0, 1.0 + 0.02 * S(i, 4), 2 * S(i, 4, 1))
        p["throat"] = {"s": (1.0 + 0.3 * max(0.0, S(i, 4, 1.2)),) * 3}
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
        p["coin"] = {"r": (0, 4 * S(i, 4), 0)}
        idle.append(p)
    # the hop: gather, the hind legs unfold as it springs, a short flight, the front lands,
    # the heavy splat, recover. Planted feet drift back on the ground (the game moves it).
    W = [  # z, pitch, squash, hands (y, z), hind feet (y, z)
        (-0.012, 0, 0.92, (0.012, 0.0), (0.004, 0.0)),      # gather
        (0.045, -6, 1.12, (-0.012, 0.03), (0.006, 0.0)),    # push: body springs, hind legs stretch out
        (0.060, -4, 1.10, (-0.022, 0.03), (0.0, 0.006)),    # flight: feet trail, just off the ground
        (0.020, 10, 0.98, (-0.020, 0.0), (-0.006, 0.01)),   # front lands, hind legs folding in
        (-0.022, 2, 0.88, (-0.008, 0.0), (-0.006, 0.0)),    # heavy landing: splat
        (-0.010, 0, 0.95, (0.004, 0.0), (-0.003, 0.0)),     # recover
    ]
    walk = []
    for z, pt, sq, hd, hn in W:
        p = body(z, pt, sq)
        p.update(limbs(hd[0], hd[1], hn[0], hn[1]))
        p["throat"] = {"s": 1.0 + 0.15 * max(0.0, (1 - sq)) / 0.14}
        p["jaw"] = {"r": (4 if sq < 0.9 else 0, 0, 0)}
        walk.append(p)
    # windup: puffs itself up, rears back on its front legs, throat sac swelling
    puff = body(0.025, -12, 1.0, -4, 1.12)
    puff["throat"] = {"s": 1.7}
    puff["eyes"] = {"s": 1.1}
    puff["coin"] = {"s": 1.15}
    windup = [lerp_pose(idle[0], puff, 0.5), puff, merge(puff, {"throat": {"s": 1.85}}), merge(puff, {"throat": {"s": 1.75}})]
    # attack: spits the coin straight ahead (hit = frame 1), then a new one appears
    spit0 = body(0.0, 2, 0.97, -2)
    spit0["jaw"] = {"r": (18, 0, 0)}
    spit0["coin"] = {"l": (0, -0.04, 0.02), "s": 1.1}
    spit1 = body(-0.005, 4, 0.95, 4)
    spit1["jaw"] = {"r": (20, 0, 0)}
    spit1["coin"] = {"l": (0, -0.03, 0.14), "s": 1.2, "r": (0, 0, 40)}
    spit1["throat"] = {"s": 0.8}
    spit2 = body(0.0, -4, 1.04, -2)
    spit2["jaw"] = {"r": (12, 0, 0)}
    spit2["coin"] = {"s": 0.01}
    spit3 = body(0.0, 0, 1.0, 0)
    spit3["coin"] = {"s": 0.7}
    attack = [spit0, spit1, spit2, spit3]
    hit = [merge(body(-0.004, -3, 0.94, -8), {"eyes": {"s": (1, 0.2, 1)}, "coin": {"r": (0, 20, 0)}}),
           merge(body(0, -3, 0.96, -3), {"coin": {"r": (0, -8, 0)}})]
    # die: shocked, wobbles, keels over and flops onto its back, pale belly up, legs in the air
    flip = body(0, 0, 1.0, 0)
    flip.update(limbs(0.0, 0.03, 0.0, 0.04))
    flip["root"] = {"r": (0, 178, 0), "l": (0, 0, 0.25)}
    flip["eyes"] = {"s": (1, 0.12, 1)}
    flip["jaw"] = {"r": (14, 0, 0)}
    tip = body(0, 0, 1.0, 0)
    tip["root"] = {"r": (0, 95, 0), "l": (-0.10, 0, 0.19)}
    tip["eyes"] = {"s": (1, 0.3, 1)}
    die = [merge(body(0.01, -8, 1.06, -6, 1.04), {"eyes": {"s": 1.25}, "throat": {"s": 1.4}}),
           merge(body(0, 0, 0.96), {"root": {"r": (0, 8, 0)}, "eyes": {"s": (1, 0.5, 1)}}),
           tip, flip,
           merge(flip, {"handL": {"l": (0, 0.0, 0.05)}, "footL": {"l": (0, 0, 0.03)}}),
           merge(flip, {"handR": {"l": (0, 0.0, 0.05)}})]
    happy = []
    for i, (z, sq) in enumerate(((0.0, 0.88), (0.07, 1.12), (0.09, 1.06), (0.02, 0.95))):
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
        p = body(-0.015, 3, 0.9 + 0.02 * b, 10)
        p["throat"] = {"s": 1.0 + 0.3 * max(0.0, b)}
        p["eyes"] = {"s": (1, 0.12, 1)}
        sleep.append(p)
    finish(arm, {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die,
                 "happy": happy, "sleep": sleep})
    return arm
