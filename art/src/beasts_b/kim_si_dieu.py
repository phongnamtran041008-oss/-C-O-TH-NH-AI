"""Kim Sí Điểu: a young golden-winged roc. Runs inside Blender (see scene.py).

A proud, upright eagle chick standing on strong orange legs with dark talons: a gold body
with a cream chest, a gold head with a hooked steel-blue beak, a stern brow over glowing
amber eyes, and a crest of three swept-back red feathers with flame tips. The wings are
built feather by feather (a covert pad on the shoulder bone, five primaries on the hand
bone, each primary's tip glowing flame-bright) so they fold neatly at rest and fan open
in windup and happy; a fan of five tail feathers with flame tips. It walks on the ground
like bach_hac / hoa_tuoc; attack is a lunging peck behind a forward wing sweep.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import (S, aim, armature, att, ball, box, cute_eyes, eye_mats, finish, glow, hexc, lerp_pose,
                    mat, merge, set_ramp, use_collection)


def feather(name, m, tipm, start, direction, length, width, tip_frac=0.32):
    """A flat tapered feather from `start` along `direction` (a cone squashed flat) with a
    glowing flame tip."""
    d = Vector(direction).normalized()
    s = Vector(start)
    mid = s + d * length * (1 - tip_frac)
    end = s + d * length
    body = aim(name, m, tuple(s), tuple(mid + d * 0.01), width * 0.6, width, seg=8)
    tip = aim(name + "_tip", tipm, tuple(mid), tuple(end), width, 0.0, seg=8)
    return [body, tip]


def build():
    use_collection("COL_kim_si_dieu")
    gold = mat("MAT_ks_gold", "#b9821a", "gold")
    gold_lt = mat("MAT_ks_gold_light", "#e6b83a", "gold", metal=True)
    cream = mat("MAT_ks_chest", "#ead9b0", "paper")
    crest = mat("MAT_ks_crest", "#c8553a", "red")
    beak = mat("MAT_ks_beak", "#94a6ba", "steel")
    brow = mat("MAT_ks_brow", "#7a4c0e", "gold")
    leg = mat("MAT_ks_leg", "#ad7a48", "wood")
    talon = mat("MAT_ks_talon", "#2e2834", "hair")
    flame = glow("MAT_ks_flame", "#fff2b0", "flame", 4.0, halo=1)
    deep = mat("MAT_ks_gold_deep", "#7a4c0e", "gold")
    eyes = eye_mats("ks", hexc("#463c4c"))
    set_ramp(eyes[0], "hair")          # dark eagle eyes with a white shine: glowing amber vanished on gold

    bones = [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0.05, 0.24), (0, -0.03, 0.42), "root"),
        ("neck", (0, -0.03, 0.42), (0, -0.045, 0.50), "body"),
        ("head", (0, -0.045, 0.50), (0, -0.05, 0.62), "neck"),
        ("eyes", (0, -0.13, 0.56), (0, -0.13, 0.62), "head"),
        ("crest", (0, -0.02, 0.64), (0, 0.06, 0.73), "head"),
        ("tail", (0, 0.10, 0.25), (0, 0.24, 0.16), "body"),
        ("wing_l", (0.10, -0.03, 0.44), (0.125, 0.10, 0.34), "body"),
        ("wing_l2", (0.125, 0.10, 0.34), (0.12, 0.25, 0.22), "wing_l"),
        ("wing_r", (-0.10, -0.03, 0.44), (-0.125, 0.10, 0.34), "body"),
        ("wing_r2", (-0.125, 0.10, 0.34), (-0.12, 0.25, 0.22), "wing_r"),
        ("leg_l1", (0.055, 0.03, 0.25), (0.055, 0.0, 0.12), "body"),
        ("leg_l2", (0.055, 0.0, 0.12), (0.055, 0.01, 0.02), "leg_l1"),
        ("leg_r1", (-0.055, 0.03, 0.25), (-0.055, 0.0, 0.12), "body"),
        ("leg_r2", (-0.055, 0.0, 0.12), (-0.055, 0.01, 0.02), "leg_r1"),
    ]
    arm = armature("kim_si_dieu", bones)

    att(arm, "body", ball("ks_body", (0.125, 0.12, 0.16), (0, 0.03, 0.34), gold, rot=(-18, 0, 0)),
        ball("ks_chest", (0.095, 0.07, 0.13), (0, -0.07, 0.36), cream, rot=(-10, 0, 0)),
        ball("ks_thighl", (0.06, 0.065, 0.07), (0.06, 0.02, 0.24), gold, seg=10, rings=6),
        ball("ks_thighr", (0.06, 0.065, 0.07), (-0.06, 0.02, 0.24), gold, seg=10, rings=6))
    att(arm, "neck", aim("ks_neck", gold, (0, -0.02, 0.42), (0, -0.045, 0.53), 0.07, 0.065, seg=10, smooth=True),
        ball("ks_neckc", (0.05, 0.03, 0.06), (0, -0.085, 0.47), cream, seg=10, rings=6))
    HY, HZ = -0.06, 0.575
    att(arm, "head", ball("ks_head", (0.11, 0.11, 0.10), (0, HY, HZ), gold_lt),
        ball("ks_cheekl", (0.05, 0.04, 0.04), (0.06, HY - 0.07, HZ - 0.04), cream, seg=8, rings=5),
        ball("ks_cheekr", (0.05, 0.04, 0.04), (-0.06, HY - 0.07, HZ - 0.04), cream, seg=8, rings=5),
        aim("ks_beak", beak, (0, HY - 0.085, HZ + 0.01), (0, HY - 0.205, HZ - 0.01), 0.045, 0.014, seg=8),
        aim("ks_hook", beak, (0, HY - 0.198, HZ - 0.0), (0, HY - 0.21, HZ - 0.06), 0.022, 0.0, seg=6),
        box("ks_browl", (0.055, 0.02, 0.014), (0.05, HY - 0.08, HZ + 0.058), brow, rot=(0, -18, 0)),
        box("ks_browr", (0.055, 0.02, 0.014), (-0.05, HY - 0.08, HZ + 0.058), brow, rot=(0, 18, 0)))
    att(arm, "eyes", *cute_eyes("ks", 0.058, HY - 0.092, HZ + 0.008, 0.042, eyes))
    cr = []
    for k, (x, up) in enumerate(((0.0, 0.0), (0.035, -0.03), (-0.035, -0.03))):
        cr += feather(f"ks_crest{k}", crest, flame, (x, HY + 0.03, HZ + 0.07),
                      (x * 2.5, 1.0, 0.45 + up * 5), 0.17 + up, 0.026, tip_frac=0.35)
    att(arm, "crest", *cr)
    # wings: covert pad on the shoulder bone, five primaries on the hand bone
    for s, b in ((1, "wing_l"), (-1, "wing_r")):
        att(arm, b, ball(f"ks_{b}_covert", (0.045, 0.12, 0.10), (s * 0.135, 0.03, 0.38), gold_lt, rot=(-28, 0, 0)))
        prim = []
        for k in range(5):
            a = math.radians(-12 + 8 * k)
            d = Vector((s * 0.06, math.cos(a), -0.45 + math.sin(a)))
            prim += feather(f"ks_{b}_prim{k}", deep if k % 2 else gold, flame,
                            (s * 0.14, 0.09 + 0.012 * k, 0.35 - 0.012 * k), d, 0.24 - 0.02 * k, 0.034, tip_frac=0.28)
        att(arm, b + "2", *prim)
    tail = []
    for k, x in enumerate((-0.05, -0.025, 0.0, 0.025, 0.05)):
        tail += feather(f"ks_tail{k}", deep if k % 2 else gold, flame, (x * 0.6, 0.10, 0.25),
                        (x * 3.0, 1.0, -0.30 + (0.06 if x == 0 else 0.0)), 0.20 - abs(x) * 0.6, 0.034, tip_frac=0.28)
    att(arm, "tail", *tail)
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"leg_{side}1", aim(f"ks_shank{side}", leg, (s * 0.055, 0.02, 0.20), (s * 0.055, 0.0, 0.12), 0.022, 0.02, seg=6))
        att(arm, f"leg_{side}2", aim(f"ks_shin{side}", leg, (s * 0.055, 0.0, 0.125), (s * 0.055, 0.01, 0.025), 0.02, 0.018, seg=6),
            *[aim(f"ks_toe{side}{k}", leg, (s * 0.055, 0.008, 0.018), (s * 0.055 + (k - 1) * 0.03, -0.045, 0.012), 0.013, 0.01, seg=5)
              for k in range(3)],
            *[aim(f"ks_talon{side}{k}", talon, (s * 0.055 + (k - 1) * 0.03, -0.043, 0.014), (s * 0.055 + (k - 1) * 0.034, -0.062, 0.002), 0.008, 0.0, seg=4)
              for k in range(3)],
            aim(f"ks_backtoe{side}", leg, (s * 0.055, 0.01, 0.018), (s * 0.055, 0.05, 0.01), 0.01, 0.006, seg=4))

    # ------------------------------------------------------------------ poses
    def wings(up=0.0, out=0.0, flap=0.0, hand=0.0):
        """up: raise (deg), out: swing outward, hand: open the hand (primaries fan out)."""
        return {"wing_l": {"r": (up + flap, 0, -out)}, "wing_r": {"r": (up + flap, 0, out)},
                "wing_l2": {"r": (hand * 0.6, 0, -hand)}, "wing_r2": {"r": (hand * 0.6, 0, hand)}}

    def legs(l1=0.0, l2=0.0, r1=0.0, r2=0.0, lz=0.0, rz=0.0):
        return {"leg_l1": {"r": (l1, 0, 0), "l": (0, 0, lz)}, "leg_l2": {"r": (l2, 0, 0)},
                "leg_r1": {"r": (r1, 0, 0), "l": (0, 0, rz)}, "leg_r2": {"r": (r2, 0, 0)}}

    idle = [merge({"body": {"l": (0, 0, 0.004 * S(i, 4)), "s": (1, 1 + 0.015 * S(i, 4), 1)},
                   "neck": {"r": (2 * S(i, 4), 0, 0)}, "head": {"r": (0, 0, 8 * S(i, 4, 1))},
                   "crest": {"r": (6 * S(i, 4, -1), 0, 5 * S(i, 4, -0.5))},
                   "tail": {"r": (0, 0, 6 * S(i, 4))}, "eyes": {"s": (1, 0.2 if i == 3 else 1.0, 1)}},
                  wings(flap=2 * S(i, 4))) for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append(merge(merge({"body": {"l": (0, 0, 0.012 * abs(s)), "r": (0, 0, 4 * s)},
                                 "neck": {"r": (8 * s, 0, 0)}, "head": {"r": (-8 * s, 0, -4 * s)},
                                 "crest": {"r": (-10 * abs(s), 0, 0)}, "tail": {"r": (6 * abs(s), 0, -10 * s)}},
                                legs(-18 * s, 26 * max(0.0, s), 18 * s, 26 * max(0.0, -s),
                                     -0.012 * abs(s), -0.012 * abs(s))),
                          wings(flap=5 * s)))
    # windup: wings flung up and open in a great V, crest raised, head drawn back, on its toes
    spread = merge(merge({"body": {"r": (-10, 0, 0), "l": (0, 0, 0.015)}, "neck": {"r": (-12, 0, 0)},
                          "head": {"r": (8, 0, 0)}, "crest": {"r": (-20, 0, 0), "s": 1.2}, "tail": {"r": (16, 0, 0)}},
                         legs(0, 0, 0, 0, -0.015, -0.015)), wings(up=60, out=55, hand=30))
    windup = [lerp_pose(idle[0], spread, 0.5), spread, merge(spread, wings(up=66, out=58, hand=34)),
              merge(spread, wings(up=62, out=54, hand=30))]
    # attack: wings sweep forward as it lunges and pecks (hit = frame 1)
    attack = [merge(merge({"body": {"r": (14, 0, 0)}, "neck": {"r": (10, 0, 0)}, "head": {"r": (-6, 0, 0)}},
                          legs(-10, 0, -10, 0)), wings(up=20, out=80, hand=20)),
              merge(merge({"body": {"r": (24, 0, 0), "l": (0, -0.02, 0)}, "neck": {"r": (20, 0, 0)},
                           "head": {"r": (14, 0, 0)}, "crest": {"r": (-24, 0, 0)}, "tail": {"r": (24, 0, 0)}},
                          legs(-22, 10, -22, 10)), wings(up=-10, out=40, hand=10)),
              merge(merge({"body": {"r": (10, 0, 0), "l": (0, -0.01, 0)}, "neck": {"r": (6, 0, 0)}},
                          legs(-10, 4, -10, 4)), wings(up=0, out=15)),
              merge({"body": {"r": (3, 0, 0)}}, wings(out=4))]
    hit = [merge({"body": {"r": (-14, 0, 6), "l": (0, 0.015, 0)}, "neck": {"r": (-14, 0, 8)},
                  "crest": {"r": (-30, 0, 10)}, "eyes": {"s": (1, 0.25, 1)}}, wings(up=40, out=40, hand=20)),
           merge({"body": {"r": (-5, 0, 2)}}, wings(up=10, out=12))]
    # die: staggers, sits down on its folded legs and keels over, wings spilling open
    sit = merge(merge({"body": {"l": (0, 0, -0.11), "r": (6, 0, 0)}, "neck": {"r": (20, 0, 0)},
                       "head": {"r": (20, 0, 0)}, "eyes": {"s": (1, 0.5, 1)}, "tail": {"r": (42, 0, 0)}},
                      legs(-66, 132, -66, 132, 0.10, 0.10)), wings(up=15, out=10))
    down = merge(sit, merge({"root": {"r": (0, -30, 0), "l": (0.07, -0.03, 0.04)}, "neck": {"r": (30, 0, 20)},
                             "head": {"r": (20, 0, 30)}, "eyes": {"s": (1, 0.12, 1)},
                             "crest": {"r": (30, 0, 0), "s": 0.85}}, wings(up=34, out=10, hand=6)))
    die = [merge({"body": {"r": (-12, 0, 0)}, "neck": {"r": (-12, 0, 0)}, "eyes": {"s": 1.15}}, wings(up=40, out=40)),
           merge({"body": {"r": (0, 0, 12)}, "head": {"r": (0, 0, 16)}, "eyes": {"s": (1, 0.5, 1)}}, wings(up=10, out=20)),
           sit, lerp_pose(sit, down, 0.6), down,
           merge(down, wings(up=32, out=12, hand=8))]
    # happy: wings spread wide, a hop and quarter-turn spins, crest flared
    happy = [merge(merge({"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)}, "neck": {"r": (-10, 0, 0)},
                          "head": {"r": (-10, 0, 0)}, "eyes": {"s": (1, 0.35, 1)}, "crest": {"s": 1.2}},
                         legs(0, 40 if z else 0, 0, 40 if z else 0)),
                   wings(up=40 + 25 * S(i, 4), out=75, hand=30)) for i, z in enumerate((0.0, 0.05, 0.06, 0.02))]
    # sleep: sits down on its legs, head turned back and tucked onto its back, wings folded
    sleep = []
    for i in range(4):
        b = S(i, 4)
        sleep.append(merge(merge({"body": {"l": (0, 0, -0.11 + 0.004 * b), "r": (8, 0, 0), "s": (1, 1 + 0.015 * b, 1)},
                                  "neck": {"r": (-40, 0, 60)}, "head": {"r": (30, 0, 50)}, "eyes": {"s": (1, 0.12, 1)},
                                  "crest": {"r": (20, 0, 0), "s": 0.9}, "tail": {"r": (24, 0, 0)}},
                                 legs(-66, 132, -66, 132, 0.10, 0.10)), wings(flap=2 * b)))
    finish(arm, {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die,
                 "happy": happy, "sleep": sleep})
    return arm
