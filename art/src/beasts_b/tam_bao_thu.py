"""Tầm Bảo Thử: the treasure-seeking mouse. Runs inside Blender (see scene.py).

A round little mouse sitting up on its haunches like a hamster, hugging a glowing spirit
gem to its coin-gold belly. Big round ears with pink insides, a pointed snout with a pink
nose, two buck teeth and dark whiskers, a red treasure pouch tied at its hip with a gold
cord, and a long pink tail that curls up behind (three skinned bones, lagging). It scurries
on quick little steps; in windup it hoists the gem overhead, in attack it bonks forward with
it (the gem flares on the hit frame).
"""
from __future__ import annotations

import math

from common import (S, armature, att, ball, box, cone, cute_eyes, eye_mats, eyes_bone, finish, glow,
                    hexc, lerp_pose, mat, merge, set_ramp, skin, tube, use_collection, aim)


def build():
    use_collection("COL_tam_bao_thu")
    fur = mat("MAT_tb_fur", "#ad7a48", "wood")
    fur_dk = mat("MAT_tb_fur_dark", "#82522f", "wood")
    belly = mat("MAT_tb_belly", "#e6b83a", "gold")
    inner = mat("MAT_tb_inner", "#f6b0c4", "pink")
    pinkm = mat("MAT_tb_tail", "#e88aa6", "pink")
    nose = mat("MAT_tb_nose", "#c4688a", "pink")
    tooth = mat("MAT_tb_tooth", "#f6f4f7", "bone")
    whisk = mat("MAT_tb_whisker", "#cfcbd3", "bone")
    pouch = mat("MAT_tb_pouch", "#94302a", "red")
    cord = mat("MAT_tb_cord", "#e6b83a", "gold", metal=True)
    gem = glow("MAT_tb_gem", "#5ae0f4", "spirit", 4.0, halo=1)
    blush = mat("MAT_tb_blush", "#f6b0c4", "pink")
    eyes = eye_mats("tb", hexc("#463c4c"))
    set_ramp(eyes[0], "hair")

    HY, HZ = -0.045, 0.37
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("hips", (0, 0.01, 0.05), (0, 0.01, 0.19), "root"),
        ("chest", (0, 0.0, 0.19), (0, -0.02, 0.29), "hips"),
        ("head", (0, -0.03, 0.28), (0, -0.04, 0.44), "chest"),
        eyes_bone(HY - 0.10, HZ + 0.01),
        ("earL", (0.09, HY + 0.02, HZ + 0.08), (0.13, HY + 0.03, HZ + 0.17), "head"),
        ("earR", (-0.09, HY + 0.02, HZ + 0.08), (-0.13, HY + 0.03, HZ + 0.17), "head"),
        ("armL", (0.085, -0.05, 0.25), (0.045, -0.12, 0.20), "chest"),
        ("armR", (-0.085, -0.05, 0.25), (-0.045, -0.12, 0.20), "chest"),
        ("gem", (0.0, -0.145, 0.20), (0.0, -0.145, 0.26), "armL"),
        ("footL", (0.06, 0.02, 0.04), (0.06, -0.06, 0.02), "root"),
        ("footR", (-0.06, 0.02, 0.04), (-0.06, -0.06, 0.02), "root"),
        ("tail1", (0, 0.11, 0.07), (0, 0.18, 0.09), "hips"),
        ("tail2", (0, 0.18, 0.09), (0, 0.215, 0.18), "tail1"),
        ("tail3", (0, 0.215, 0.18), (0, 0.18, 0.29), "tail2"),
    ]
    arm = armature("tam_bao_thu", bones)

    att(arm, "hips", ball("tb_body", (0.135, 0.12, 0.125), (0, 0.01, 0.135), fur),
        ball("tb_belly", (0.11, 0.075, 0.115), (0, -0.06, 0.14), belly),
        ball("tb_pouch", (0.05, 0.045, 0.06), (0.125, 0.05, 0.13), pouch, seg=10, rings=6),
        ball("tb_pouchtie", (0.03, 0.03, 0.018), (0.128, 0.05, 0.19), cord, seg=8, rings=5),
        cone("tb_pouchneck", 0.018, 0.03, 0.03, (0.128, 0.05, 0.205), pouch, seg=8))
    att(arm, "chest", ball("tb_chest", (0.11, 0.10, 0.10), (0, -0.01, 0.235), fur),
        ball("tb_bellyup", (0.075, 0.05, 0.06), (0, -0.075, 0.225), belly, seg=10, rings=6))
    att(arm, "head", ball("tb_head", (0.15, 0.13, 0.13), (0, HY, HZ), fur),
        aim("tb_snout", fur, (0, HY - 0.07, HZ - 0.04), (0, HY - 0.205, HZ - 0.06), 0.07, 0.025, seg=10, smooth=True),
        ball("tb_muzzle", (0.045, 0.06, 0.03), (0, HY - 0.135, HZ - 0.08), belly, seg=10, rings=6),
        ball("tb_nose", (0.026, 0.022, 0.022), (0, HY - 0.21, HZ - 0.055), nose, seg=8, rings=5),
        box("tb_tooth", (0.03, 0.012, 0.026), (0, HY - 0.175, HZ - 0.105), tooth),
        ball("tb_blushl", (0.03, 0.01, 0.016), (0.085, HY - 0.105, HZ - 0.045), blush, seg=6, rings=4),
        ball("tb_blushr", (0.03, 0.01, 0.016), (-0.085, HY - 0.105, HZ - 0.045), blush, seg=6, rings=4),
        *[aim(f"tb_whisker{s}", whisk, (s * 0.035, HY - 0.18, HZ - 0.065),
              (s * 0.16, HY - 0.17, HZ - 0.09), 0.008, 0.004, seg=4) for s in (1, -1)])
    att(arm, "eyes", *cute_eyes("tb", 0.062, HY - 0.105, HZ + 0.015, 0.046, eyes))
    for side, sx in (("L", 1), ("R", -1)):
        att(arm, f"ear{side}",
            ball(f"tb_ear{side}", (0.095, 0.024, 0.09), (sx * 0.125, HY + 0.05, HZ + 0.125), fur, rot=(0, sx * 32, sx * 22)),
            ball(f"tb_eari{side}", (0.066, 0.012, 0.062), (sx * 0.12, HY + 0.03, HZ + 0.123), inner,
                 rot=(0, sx * 32, sx * 22), seg=10, rings=6))
        att(arm, f"arm{side}", aim(f"tb_arm{side}", fur, (sx * 0.085, -0.05, 0.25), (sx * 0.05, -0.12, 0.20), 0.03, 0.025, seg=8),
            ball(f"tb_hand{side}", (0.03, 0.028, 0.028), (sx * 0.045, -0.125, 0.205), fur_dk, seg=8, rings=5))
        att(arm, f"foot{side}", ball(f"tb_foot{side}", (0.038, 0.06, 0.024), (sx * 0.06, -0.035, 0.024), fur_dk, seg=10, rings=6),
            ball(f"tb_leg{side}", (0.05, 0.06, 0.06), (sx * 0.075, 0.0, 0.07), fur, seg=10, rings=6))
    # the gem: a faceted spirit stone with a gold setting
    att(arm, "gem", ball("tb_gem", (0.045, 0.04, 0.05), (0, -0.155, 0.215), gem, seg=6, rings=4, smooth=False),
        cone("tb_setting", 0.04, 0.028, 0.02, (0, -0.155, 0.17), cord, seg=8))
    tail = tube("tb_tailtube", [(0, 0.10, 0.07), (0, 0.17, 0.085), (0, 0.21, 0.14), (0, 0.215, 0.21),
                                (0, 0.19, 0.27), (0, 0.155, 0.30)],
                [0.02, 0.018, 0.016, 0.014, 0.012, 0.01], pinkm, seg=8)
    skin(tail, arm, ["tail1", "tail2", "tail3"], power=3.0)

    # ------------------------------------------------------------------ poses
    def tailp(a=0.0, b=0.0, c=0.0, up=0.0):
        return {"tail1": {"r": (up, 0, a)}, "tail2": {"r": (0, 0, b)}, "tail3": {"r": (0, 0, c)}}

    def arms(lift=0.0, fwd=0.0):
        """lift: degrees the arms (and the gem, held by the left) swing up; fwd pushes out."""
        return {"armL": {"r": (-lift, 0, 0), "l": (0, -fwd, 0)}, "armR": {"r": (-lift, 0, 0), "l": (0, -fwd, 0)}}

    def gem_up(lift, sc, up=0.20, fwd=-0.03):
        """The arms are short: when they swing up by `lift` degrees, slide the gem along
        so it rises clear above the brow. The offset is given in the arm's turned frame."""
        a = math.radians(lift)
        y = fwd * math.cos(a) - up * math.sin(a)
        z = fwd * math.sin(a) + up * math.cos(a)
        return {"gem": {"l": (0, y, z), "s": sc}}

    def body(z=0.0, lean=0.0, sq=1.0, head=0.0, yaw=0.0):
        w = 1.0 / math.sqrt(sq)
        return {"hips": {"l": (0, 0, z), "r": (lean, 0, yaw), "s": (w, sq, w)},
                "head": {"r": (head - lean * 0.5, 0, 0)}}

    idle = []
    for i in range(4):
        p = merge(body(0.003 * S(i, 4), 0, 1.0 + 0.025 * S(i, 4), 3 * S(i, 4, 0.7)),
                  tailp(14 * S(i, 4), 18 * S(i, 4, -1), 22 * S(i, 4, -2)))
        p.update(arms(4 * S(i, 4)))
        p["gem"] = {"s": 1.0 + 0.08 * S(i, 4, 1)}
        p["earL"] = {"r": (0, 6 * S(i, 4, 0.5), 0)}
        p["earR"] = {"r": (0, -6 * S(i, 4, 0.5) - (14 if i == 1 else 0), 0)}
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
        p["head"]["r"] = (3 * S(i, 4, 0.7), 0, 8 * S(i, 4, 0.3))
        idle.append(p)

    # scurry: quick alternating little steps, body bobbing and leaning in
    walk = []
    for i in range(6):
        s, c = S(i, 6), abs(math.cos(math.pi * i / 3))
        p = merge(body(0.014 * (1 - c), 14, 1.0 + 0.04 * (1 - c), -6, 6 * s),
                  tailp(-24 * s, 28 * S(i, 6, -1), 30 * S(i, 6, -2), up=-14))
        p.update(arms(10 + 6 * s))
        p["footL"] = {"l": (0, 0.035 * s, 0.03 * max(0.0, -s))}
        p["footR"] = {"l": (0, -0.035 * s, 0.03 * max(0.0, s))}
        p["earL"] = {"r": (-10 + 8 * c, 0, 0)}
        p["earR"] = {"r": (-10 + 8 * c, 0, 0)}
        walk.append(p)

    # windup: crouches, then hoists the gem high overhead; ears back, tail stiff and up
    hoist = merge(body(-0.015, -8, 0.9, -12), tailp(0, 10, 20, up=34))
    hoist.update(arms(112))
    hoist.update(gem_up(112, 1.3))
    hoist["earL"] = {"r": (-24, 0, 0)}
    hoist["earR"] = {"r": (-24, 0, 0)}
    windup = [merge(lerp_pose(idle[0], body(-0.03, 6, 0.86, 6), 1.0), arms(30)), hoist,
              merge(hoist, {**gem_up(112, 1.45), "hips": {"l": (0, 0, -0.012), "r": (-8, 0, 0), "s": (1.03, 0.94, 1.03)}}),
              merge(hoist, gem_up(112, 1.3))]
    # attack: bonks down and forward with the gem; it flares on the hit frame (1)
    swing = merge(body(0.02, 18, 1.08, 8), tailp(0, -20, -30, up=-30))
    swing.update(arms(70, 0.03))
    swing["gem"] = {"s": 1.6}
    swing["root"] = {"l": (0, -0.005, 0)}
    bonk = merge(body(-0.01, 18, 0.94, 14), tailp(10, -10, -20, up=-10))
    bonk.update(arms(50, 0.02))
    bonk["gem"] = {"s": 1.7}
    bonk["root"] = {"l": (0, -0.005, 0)}
    attack = [swing, bonk, merge(lerp_pose(bonk, idle[0], 0.5), {"gem": {"s": 1.2}}), lerp_pose(bonk, idle[0], 0.85)]
    hit = [merge(body(-0.01, -14, 0.88, -14), merge(tailp(30, 30, 30, up=20), {"eyes": {"s": (1, 0.25, 1)},
                                                                              "earL": {"r": (-40, 0, 0)},
                                                                              "earR": {"r": (-40, 0, 0)}})),
           merge(body(0, -5, 0.96, -5), tailp(10, 10, 10))]
    hit[0].update(arms(30))
    # die: totters, sits down hard and topples onto its round back, gem on its belly
    back = merge(body(0.0, 0, 0.92, 20), tailp(40, 40, 30))
    back.update(arms(40))
    back["root"] = {"r": (-78, 0, 0), "l": (0, -0.15, 0.11)}
    back["eyes"] = {"s": (1, 0.12, 1)}
    back["footL"] = {"l": (0, -0.02, 0.06)}
    back["footR"] = {"l": (0, -0.03, 0.04)}
    die = [merge(body(0.01, -6, 1.06, -10), merge(arms(20), {"eyes": {"s": 1.2}, "earL": {"r": (0, 10, 0)},
                                                              "earR": {"r": (0, -10, 0)}})),
           merge(body(-0.03, 4, 0.84, 10), merge(arms(10), {"root": {"r": (0, 0, 14)}, "eyes": {"s": (1, 0.5, 1)}})),
           lerp_pose({}, back, 0.55), back,
           merge(back, {"tail3": {"r": (0, 0, 50)}}), merge(back, {"tail3": {"r": (0, 0, 46)}})]
    # happy: hops and spins with the gem held high, sparkling
    happy = []
    for i, z in enumerate((0.0, 0.06, 0.08, 0.02)):
        p = merge(body(0, -4, 1.06 if z else 0.92, -10), tailp(30 * S(i, 4), 30 * S(i, 4, -1), 30, up=10))
        p.update(arms(108 + 8 * S(i, 4)))
        p["root"] = {"r": (0, 0, 90 * i), "l": (0, 0, z)}
        p["footL"] = {"l": (0, 0, z * 0.8)}
        p["footR"] = {"l": (0, 0, z * 0.8)}
        p.update(gem_up(108 + 8 * S(i, 4), 1.3 + 0.2 * S(i, 4)))
        p["eyes"] = {"s": (1, 0.35, 1)}
        happy.append(p)
    # sleep: a round ball, head bowed onto the gem, tail wrapped round the front
    sleep = []
    for i in range(4):
        b = S(i, 4)
        p = merge(body(-0.04 + 0.003 * b, 2, 0.84 + 0.02 * b, 22), tailp(70, 50, 40, up=-20))
        p.update(arms(10))
        p["gem"] = {"s": 0.9}
        p["eyes"] = {"s": (1, 0.12, 1)}
        p["earL"] = {"r": (-20, 0, 0)}
        p["earR"] = {"r": (-20, 0, 0)}
        p["head"]["l"] = (0, 0.0, -0.04)
        sleep.append(p)
    finish(arm, {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die,
                 "happy": happy, "sleep": sleep}, walk_fps=12)
    return arm
