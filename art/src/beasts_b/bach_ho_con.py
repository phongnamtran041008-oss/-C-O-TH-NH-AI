"""Bạch Hổ Con: the white tiger cub, child of one of the four sacred beasts. Runs inside
Blender (see scene.py).

A chunky kitten-proportioned tiger: big round head with fluffy cheek ruffs, small round
ears, a wide white muzzle with a pink nose, glowing ice-blue eyes (the metal-white aura of
the White Tiger), a small glowing diamond on the brow, dark stripes (arcs over the back,
brow and cheek strokes, rings on the tail and a dark tail tip), thick legs and big paws.
Built on the shared quadruped rig (monsters_a/quadrupeds.py: IK legs, paws kept level);
the clip poses come from common.quad_poses and get a cat's butt-wiggle before the pounce.
"""
from __future__ import annotations

import math

from common import (S, att, aim, ball, box, cute_eyes, eye_mats, eyes_bone, finish, glow, hexc, mat,
                    merge, quad_armature, quad_extra_poses, quad_poses, set_ramp, tube, use_collection)


def arc_stripe(name, m, y, zc, rx, rz, a0=28, a1=152, r=0.011, n=9):
    """A stripe over the back: an arc in the x-z plane at depth y round (0, y, zc)."""
    pts = []
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / (n - 1))
        pts.append((rx * math.cos(a), y, zc + rz * math.sin(a)))
    return tube(name, pts, [r * (0.6 if k in (0, n - 1) else 1.0) for k in range(n)], m, seg=6)


def build():
    use_collection("COL_bach_ho_con")
    fur = mat("MAT_bhc_fur", "#cfcbd3", "bone")
    fur_sh = mat("MAT_bhc_fur_shade", "#9894a2", "bone")
    stripe = mat("MAT_bhc_stripe", "#2e2834", "hair")
    inner = mat("MAT_bhc_inner", "#f6b0c4", "pink")
    nose = mat("MAT_bhc_nose", "#e88aa6", "pink")
    mark = glow("MAT_bhc_brow_mark", "#b0dcff", "ice", 3.0, halo=0)
    mark["kit_priority"] = 3.0
    eyes = eye_mats("bhc", hexc("#6488c4"))
    set_ramp(eyes[0], "blue")           # saturated blue cub eyes; on white fur a pale glow vanished

    HY, HZ = -0.18, 0.43
    P = {"h": 0.23, "yf": -0.06, "yb": 0.085, "x": 0.085, "knee": 0.11,
         "head": (-0.11, 0.30), "hlen": 0.2, "jaw": (-0.26, 0.38),
         "tail": ((0.14, 0.24), (0.25, 0.27), (0.33, 0.36))}
    arm = quad_armature("bach_ho_con", P, extra=[eyes_bone(HY - 0.1, HZ + 0.02)])
    att(arm, "chest", ball("bhc_chest", (0.14, 0.13, 0.125), (0, -0.03, 0.25), fur),
        ball("bhc_bib", (0.10, 0.06, 0.09), (0, -0.11, 0.23), fur),
        arc_stripe("bhc_st1", stripe, -0.01, 0.25, 0.143, 0.13, 50, 130))
    att(arm, "pelvis", ball("bhc_rump", (0.13, 0.12, 0.12), (0, 0.075, 0.24), fur),
        arc_stripe("bhc_st3", stripe, 0.06, 0.245, 0.133, 0.122, 42, 138),
        arc_stripe("bhc_st4", stripe, 0.125, 0.24, 0.115, 0.10, 55, 125))
    hd = [ball("bhc_head", (0.185, 0.16, 0.155), (0, HY, HZ), fur),
          ball("bhc_ruffl", (0.07, 0.07, 0.06), (0.125, HY + 0.01, HZ - 0.06), fur, seg=10, rings=6),
          ball("bhc_ruffr", (0.07, 0.07, 0.06), (-0.125, HY + 0.01, HZ - 0.06), fur, seg=10, rings=6),
          ball("bhc_padl", (0.045, 0.04, 0.036), (0.035, HY - 0.135, HZ - 0.065), fur, seg=10, rings=6),
          ball("bhc_padr", (0.045, 0.04, 0.036), (-0.035, HY - 0.135, HZ - 0.065), fur, seg=10, rings=6),
          ball("bhc_nose", (0.03, 0.02, 0.018), (0, HY - 0.165, HZ - 0.035), nose, seg=8, rings=5),
          box("bhc_mark", (0.03, 0.012, 0.03), (0, HY - 0.152, HZ + 0.075), mark, rot=(-30, 45, 0)),
          ]
    for s in (1, -1):
        # round ears: dark backs, pink fronts
        hd += [ball(f"bhc_ear{s}", (0.055, 0.026, 0.055), (s * 0.10, HY + 0.035, HZ + 0.155), stripe, rot=(0, s * 25, 0), seg=10, rings=6),
               ball(f"bhc_eari{s}", (0.042, 0.014, 0.04), (s * 0.098, HY + 0.017, HZ + 0.152), inner, rot=(0, s * 25, 0), seg=10, rings=6),
               ball(f"bhc_earw{s}", (0.03, 0.015, 0.022), (s * 0.104, HY + 0.012, HZ + 0.13), fur, rot=(0, s * 25, 0), seg=8, rings=5)]
        # brow strokes (diagonal, never a bar pattern) and two cheek strokes on each ruff
        hd.append(tube(f"bhc_brow_stripe{s}", [(s * 0.03, HY - 0.14, HZ + 0.085), (s * 0.055, HY - 0.13, HZ + 0.11),
                                                (s * 0.07, HY - 0.115, HZ + 0.125)], [0.007, 0.01, 0.006], stripe, seg=6))
        hd.append(tube(f"bhc_cheek_stripe{s}", [(s * 0.19, HY + 0.0, HZ - 0.05), (s * 0.17, HY - 0.05, HZ - 0.06)],
                       [0.008, 0.005], stripe, seg=6))
    att(arm, "head", *hd)
    att(arm, "eyes", *cute_eyes("bhc", 0.064, HY - 0.122, HZ + 0.015, 0.05, eyes))
    att(arm, "jaw", aim("bhc_jaw", fur_sh, (0, HY - 0.07, HZ - 0.09), (0, HY - 0.15, HZ - 0.10), 0.04, 0.024, seg=8))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"bhc_{leg}{side}up", fur, (x, y, 0.20), (x, y, 0.10), 0.06 if leg == "b" else 0.055, 0.046, seg=8),
                tube(f"bhc_{leg}{side}_stripe", [(x - 0.05, y - 0.03, 0.16), (x, y - 0.058, 0.15), (x + 0.05, y - 0.03, 0.16)],
                     [0.006, 0.01, 0.006], stripe, seg=6) if leg == "f" else
                tube(f"bhc_{leg}{side}_stripe", [(x + sx * 0.055, y - 0.03, 0.17), (x + sx * 0.062, y, 0.155), (x + sx * 0.055, y + 0.03, 0.165)],
                     [0.006, 0.01, 0.006], stripe, seg=6))
            att(arm, f"{leg}{side}2", aim(f"bhc_{leg}{side}lo", fur, (x, y, 0.11), (x, y, 0.035), 0.046, 0.044, seg=8))
            att(arm, f"{leg}{side}3", ball(f"bhc_{leg}{side}paw", (0.052, 0.058, 0.034), (x, y - 0.01, 0.03), fur, seg=10, rings=6),
                *[ball(f"bhc_{leg}{side}toe{k}", (0.012, 0.012, 0.012), (x + (k - 1) * 0.025, y - 0.064, 0.03), fur_sh, seg=6, rings=4)
                  for k in range(3)])
    # tail: white with two dark rings and a dark tip
    att(arm, "tail1", aim("bhc_tail1", fur, (0, 0.13, 0.24), (0, 0.25, 0.27), 0.038, 0.032, seg=8),
        aim("bhc_tailring1", stripe, (0, 0.185, 0.253), (0, 0.205, 0.258), 0.037, 0.035, seg=8))
    att(arm, "tail2", aim("bhc_tail2", fur, (0, 0.25, 0.27), (0, 0.33, 0.36), 0.032, 0.03, seg=8),
        aim("bhc_tailring2", stripe, (0, 0.28, 0.30), (0, 0.29, 0.313), 0.032, 0.031, seg=8),
        aim("bhc_tailtip", stripe, (0, 0.315, 0.34), (0, 0.345, 0.385), 0.03, 0.012, seg=8))

    A = {"stride": 0.032, "lift": 0.045, "hop": 0.06, "crouch": 0.065, "drop": 0.10, "lunge": 0.02}
    poses = quad_poses(P, A)
    poses.update(quad_extra_poses(P, drop=0.10, tail_wrap=75.0, head_rest=(12, 0, 55)))
    # a cat before the pounce: the rump wiggles side to side, tail tip twitching
    w = poses["windup"]
    w[2] = merge(w[2], {"pelvis": {"r": (-4, 0, 9)}, "tail2": {"r": (30, 0, 26)}})
    w[3] = merge(w[3], {"pelvis": {"r": (-4, 0, -9)}, "tail2": {"r": (30, 0, -26)}})
    for i, p in enumerate(poses["idle"]):
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
    for p in poses["die"][3:]:
        p["eyes"] = {"s": (1, 0.12, 1)}
    finish(arm, poses, walk_fps=11)
    return arm
