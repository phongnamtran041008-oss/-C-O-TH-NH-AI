"""Vong Hồn Kiếm Sĩ: the ghost of a fallen swordsman (Kiếm Trủng Sơn, elite 64).

Runs inside Blender. Hollow armour held up by nothing: a general's helmet with a red
plume and a gold crescent, an empty black face with two cold glowing eyes, a lamellar
cuirass with a gold heart-mirror plate, layered pauldrons, a torn blood-red cape and
tabard, armoured arms - and below the waist no legs, only a glowing spirit wisp trailing
off behind. Its right hand holds a sword snapped a third of the way down.

Clips: idle (hovers and bobs, cape and wisp lag), walk (glides, leaning in, cape and wisp
streaming back), windup (a thrust stance: twists the sword shoulder back, blade levelled
at the target, the free hand aiming, eyes flaring), attack (a straight lunging thrust in a
line = hit, held, recovers), hit, die (the spirit leaves; the empty armour collapses to
the ground in a heap, eyes going out).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (C, S, aim, armature, att, ball, box, cone, hover_shadow, lerp_pose,
                    material, merge, plate, skin, tube, use_collection, write_clips)

BLADE = [(-0.034, 0.075), (0.034, 0.075), (0.034, 0.36), (0.014, 0.41), (0.0, 0.375),
         (-0.016, 0.43), (-0.034, 0.34)]
GUARD = [(-0.085, 0.0), (0.085, 0.0), (0.10, 0.03), (0.06, 0.045), (-0.06, 0.045), (-0.10, 0.03)]
GRIP = [(-0.017, -0.13), (0.017, -0.13), (0.017, 0.0), (-0.017, 0.0)]


def build_vong_hon_kiem_si():
    use_collection("COL_vong_hon_kiem_si")
    steel = material("MAT_vh_steel", (0.36, 0.43, 0.53), (0.18, 0.16, 0.20), ramp=("steel", "hair"), metal=True)
    steel_dk = material("MAT_vh_steel_dark", (0.21, 0.25, 0.35), (0.11, 0.10, 0.13), ramp=("steel", "hair"))
    gold = material("MAT_vh_gold", (0.73, 0.51, 0.10), (0.73, 0.51, 0.10), ramp="gold", metal=True)
    cloth = material("MAT_vh_cloth", (0.36, 0.10, 0.11), (0.23, 0.13, 0.38), ramp=("red", "purple"))
    plume = material("MAT_vh_plume", (0.58, 0.19, 0.16), (0.36, 0.21, 0.56), ramp=("red", "purple"))
    void = material("MAT_vh_socket", (0.06, 0.05, 0.07), (0.06, 0.05, 0.07), ramp="hair")
    eye = material("MAT_vh_eye", (0.85, 0.97, 1.0), (1.0, 0.89, 0.48), emit=7.0, glow=("ice", "holy"))
    ghost = material("MAT_vh_ghost", (0.35, 0.88, 0.96), (1.0, 0.45, 0.20), emit=1.6, glow=("spirit", "flame"))
    blade = material("MAT_vh_blade", (0.58, 0.65, 0.73), (0.58, 0.65, 0.73), ramp="steel", metal=True)
    grip = material("MAT_vh_grip", (0.18, 0.16, 0.20), (0.36, 0.10, 0.11), ramp=("hair", "red"))
    cloth["kit_light"] = 0.86          # deep faded red, lit only along the top folds
    steel_dk["kit_light"] = 0.6

    arm = armature("vong_hon_kiem_si", [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hover", (0, 0, 0.55), (0, 0, 0.65), "root"),
        ("waist", (0, 0, 0.64), (0, 0, 0.76), "hover"),
        ("chest", (0, 0, 0.76), (0, 0, 0.98), "waist"),
        ("head", (0, 0, 0.99), (0, 0, 1.2), "chest"),
        ("eyes", (0, -0.12, 1.07), (0, -0.12, 1.12), "head"),
        ("plume", (0, 0.07, 1.22), (0, 0.17, 1.10), "head"),
        ("cape1", (0, 0.11, 0.96), (0, 0.15, 0.74), "chest"),
        ("cape2", (0, 0.15, 0.74), (0, 0.22, 0.50), "cape1"),
        ("tab_f", (0, -0.13, 0.66), (0, -0.14, 0.46), "waist"),
        ("tab_b", (0, 0.12, 0.66), (0, 0.14, 0.46), "waist"),
        ("wisp1", (0, 0.0, 0.64), (0, 0.03, 0.46), "waist"),
        ("wisp2", (0, 0.03, 0.46), (0, 0.10, 0.30), "wisp1"),
        ("wisp3", (0, 0.10, 0.30), (0, 0.20, 0.17), "wisp2"),
        ("arm_l", (0.19, 0, 0.93), (0.23, -0.01, 0.77), "chest"),
        ("fore_l", (0.23, -0.01, 0.77), (0.24, -0.04, 0.63), "arm_l"),
        ("hand_l", (0.24, -0.04, 0.63), (0.24, -0.06, 0.58), "fore_l"),
        ("arm_r", (-0.19, 0, 0.93), (-0.23, -0.01, 0.77), "chest"),
        ("fore_r", (-0.23, -0.01, 0.77), (-0.24, -0.04, 0.63), "arm_r"),
        ("hand_r", (-0.24, -0.04, 0.63), (-0.24, -0.06, 0.58), "fore_r"),
    ])

    # --- helmet: dome, ridge, gold crescent, cheek guards, empty face, cold eyes, plume
    hd = [ball("vh_helm", (0.13, 0.13, 0.125), (0, 0.0, 1.11), steel, seg=14, rings=9),
          cone("vh_brim", 0.145, 0.135, 0.035, (0, 0.0, 1.06), steel_dk, seg=14),
          box("vh_ridge", (0.026, 0.24, 0.03), (0, 0.0, 1.235), gold),
          ball("vh_face", (0.095, 0.045, 0.078), (0, -0.112, 1.05), void, seg=10, rings=6),
          aim("vh_crescl", gold, (0.0, -0.12, 1.15), (0.07, -0.12, 1.22), 0.016, 0.006, seg=5),
          aim("vh_crescr", gold, (0.0, -0.12, 1.15), (-0.07, -0.12, 1.22), 0.016, 0.006, seg=5),
          ball("vh_gem", (0.022, 0.014, 0.022), (0, -0.128, 1.15), plume, seg=8, rings=5),
          ball("vh_knob", (0.03, 0.03, 0.03), (0, 0.0, 1.245), gold, seg=8, rings=5)]
    for sx in (-1, 1):
        hd.append(plate(f"vh_cheek{sx}", [(-0.05, 0.0), (0.05, 0.0), (0.04, -0.11), (-0.02, -0.13)],
                        steel_dk, (sx * 0.115, -0.03, 1.07), (0, -1, 0), (sx * 0.25, 0, 1), thick=0.018))
    att(arm, "head", *hd)
    att(arm, "eyes", *[ball(f"vh_eye{s}", (0.032, 0.012, 0.024), (s * 0.044, -0.158, 1.066), eye, seg=8, rings=5)
                       for s in (-1, 1)])
    att(arm, "plume", aim("vh_plume1", plume, (0, 0.05, 1.25), (0, 0.15, 1.17), 0.04, 0.022, seg=8),
        aim("vh_plume2", plume, (0, 0.15, 1.17), (0, 0.19, 1.05), 0.024, 0.008, seg=8))
    # --- hollow neck: only the spirit shows between helmet and cuirass
    att(arm, "chest", ball("vh_neck", (0.075, 0.075, 0.05), (0, 0.0, 0.99), ghost, seg=10, rings=6))
    # --- cuirass: lamellar bands, gold heart-mirror, layered pauldrons
    att(arm, "chest",
        cone("vh_torso", 0.145, 0.175, 0.26, (0, 0.0, 0.86), steel, seg=14),
        cone("vh_band1", 0.155, 0.16, 0.022, (0, 0.0, 0.79), steel_dk, seg=14),
        cone("vh_band2", 0.165, 0.17, 0.022, (0, 0.0, 0.85), steel_dk, seg=14),
        ball("vh_mirror", (0.07, 0.02, 0.07), (0, -0.168, 0.89), gold, seg=12, rings=6),
        ball("vh_mirror_in", (0.04, 0.012, 0.04), (0, -0.184, 0.89), steel, seg=10, rings=5),
        cone("vh_collar", 0.13, 0.10, 0.05, (0, 0.0, 0.985), steel_dk, seg=14))
    for sx, side in ((1, "l"), (-1, "r")):
        att(arm, "chest",
            ball(f"vh_paul{side}1", (0.115, 0.12, 0.06), (sx * 0.20, 0.0, 0.965), steel, rot=(0, sx * 28, 0)),
            ball(f"vh_paul{side}2", (0.10, 0.11, 0.05), (sx * 0.235, 0.0, 0.91), steel_dk, rot=(0, sx * 38, 0)),
            ball(f"vh_paul{side}3", (0.085, 0.10, 0.04), (sx * 0.26, 0.0, 0.86), gold, rot=(0, sx * 46, 0)))
        att(arm, f"arm_{side}", aim(f"vh_upper{side}", steel_dk, (sx * 0.20, 0, 0.92), (sx * 0.23, -0.01, 0.77),
                                    0.05, 0.048, seg=8, smooth=True))
        att(arm, f"fore_{side}", aim(f"vh_vamb{side}", steel, (sx * 0.23, -0.01, 0.78), (sx * 0.24, -0.04, 0.64),
                                     0.056, 0.05, seg=8),
            ball(f"vh_elbow{side}", (0.05, 0.05, 0.05), (sx * 0.23, -0.01, 0.775), gold, seg=8, rings=5))
        att(arm, f"hand_{side}", ball(f"vh_gaunt{side}", (0.05, 0.05, 0.055), (sx * 0.24, -0.05, 0.6), steel_dk,
                                      seg=8, rings=5))
    # --- belt, side tassets, torn tabard front and back, torn cape
    att(arm, "waist", cone("vh_belt", 0.15, 0.148, 0.05, (0, 0.0, 0.70), cloth, seg=14),
        box("vh_buckle", (0.07, 0.03, 0.05), (0, -0.155, 0.70), gold),
        plate("vh_tasset_l", [(-0.06, 0.0), (0.06, 0.0), (0.07, -0.13), (-0.05, -0.15)], steel,
              (0.15, 0.0, 0.69), (0, -1, 0), (0.35, 0, 1), thick=0.02),
        plate("vh_tasset_r", [(-0.06, 0.0), (0.06, 0.0), (0.05, -0.15), (-0.07, -0.13)], steel,
              (-0.15, 0.0, 0.69), (0, -1, 0), (-0.35, 0, 1), thick=0.02))
    rag = [(-0.08, 0.0), (0.08, 0.0), (0.075, -0.16), (0.04, -0.21), (0.02, -0.17), (-0.01, -0.23),
           (-0.04, -0.18), (-0.075, -0.2)]
    att(arm, "tab_f", plate("vh_tab_f", rag, cloth, (0, -0.15, 0.67), (1, 0, 0), (0, -0.05, 1), thick=0.016))
    att(arm, "tab_b", plate("vh_tab_b", rag, cloth, (0, 0.14, 0.67), (1, 0, 0), (0, 0.08, 1), thick=0.016))

    def hem(i, a):
        return 1.0 + (0.22 * math.sin(5 * a + 1.0) if i >= 4 else 0.0)
    cape = tube("vh_cape", [(0, 0.12, 0.97), (0, 0.15, 0.86), (0, 0.17, 0.74), (0, 0.20, 0.62),
                            (0, 0.23, 0.52), (0, 0.245, 0.47)],
                [0.17, 0.19, 0.2, 0.2, 0.19, 0.17], cloth, seg=14, up=(0, -1, 0),
                squash=[(0.16, 1.0)] * 6, wobble=hem)
    skin(cape, arm, ["chest", "cape1", "cape2"], power=3)

    # --- no legs: a glowing spirit wisp from the waist, trailing back and thinning out
    zs = [0.67, 0.58, 0.47, 0.37, 0.28, 0.21, 0.16]
    ys = [0.0, 0.01, 0.04, 0.08, 0.13, 0.19, 0.25]
    rs = [0.135, 0.13, 0.105, 0.08, 0.055, 0.03, 0.008]

    def curl(i, a):
        return 1.0 + (0.15 * math.sin(4 * a + i * 1.1) if i >= 2 else 0.0)
    wisp = tube("vh_wisp", [(0, y, z) for y, z in zip(ys, zs)], rs, ghost, seg=14, up=(0, -1, 0), wobble=curl)
    skin(wisp, arm, ["waist", "wisp1", "wisp2", "wisp3"], power=3)

    # --- the broken sword in the right hand, held low, levelled forward-down
    g = Vector((-0.24, -0.06, 0.60))
    v = Vector((0, -0.72, -0.69)).normalized()
    u = Vector((0, -v.z, v.y))           # width in the vertical plane: the flat shows from the side
    sw = [plate("vh_blade", BLADE, blade, g, u, v, thick=0.02),
          plate("vh_guard", GUARD, gold, g, u, v, thick=0.05),
          plate("vh_grip", GRIP, grip, g, u, v, thick=0.035),
          ball("vh_pommel", (0.026, 0.026, 0.026), tuple(g - v * 0.14), gold, seg=8, rings=5)]
    att(arm, "hand_r", *sw)
    hover_shadow("vh_shadow", 0.15, 0.12, arm)
    _clips(arm)
    return arm


def _clips(arm):
    def base(i, n, bob=0.025, lean=0.0):
        return {
            "hover": {"l": (0, 0, bob * S(i, n))},
            "waist": {"r": (lean, 0, 0)},
            "chest": {"r": (-1.5 * S(i, n), 0, 0)},
            "head": {"r": (2 * S(i, n, -0.6), 0, 3 * S(i, n, 0.4))},
            "plume": {"r": (8 * S(i, n, -1.2), 0, 6 * S(i, n, -1.5))},
            "cape1": {"r": (4 + 4 * S(i, n, -0.9), 0, 3 * S(i, n, -1.0))},
            "cape2": {"r": (6 + 6 * S(i, n, -1.7), 0, 5 * S(i, n, -1.8))},
            "tab_f": {"r": (3 * S(i, n, -1.0), 0, 0)}, "tab_b": {"r": (4 * S(i, n, -1.2), 0, 0)},
            "wisp1": {"r": (6 + 4 * S(i, n, -0.8), 0, 6 * S(i, n, -0.8))},
            "wisp2": {"r": (10 + 8 * S(i, n, -1.6), 0, 16 * S(i, n, -1.6))},
            "wisp3": {"r": (14 + 10 * S(i, n, -2.4), 0, 26 * S(i, n, -2.4))},
            "arm_l": {"r": (4 * S(i, n, -0.5), -6, 0)}, "arm_r": {"r": (4 * S(i, n, -0.5), 6, 0)},
            "fore_l": {"r": (-10, 0, 0)}, "fore_r": {"r": (-14, 0, 0)},
        }
    idle = [base(i, 4) for i in range(4)]
    walk = []
    for i in range(6):
        p = base(i, 6, bob=0.03, lean=10)
        p["cape1"]["r"] = (24 + 4 * S(i, 6), 0, 4 * S(i, 6, -1))
        p["cape2"]["r"] = (20 + 6 * S(i, 6, -1.4), 0, 6 * S(i, 6, -1.6))
        p["tab_f"]["r"] = (20 + 6 * S(i, 6, -1), 0, 0)
        p["tab_b"]["r"] = (26 + 6 * S(i, 6, -1.3), 0, 0)
        p["wisp1"]["r"] = (26 + 4 * S(i, 6), 0, 8 * S(i, 6, -0.8))
        p["wisp2"]["r"] = (24, 0, 14 * S(i, 6, -1.6))
        p["wisp3"]["r"] = (18, 0, 22 * S(i, 6, -2.4))
        p["plume"]["r"] = (34 + 6 * S(i, 6, -1.2), 0, 6 * S(i, 6, -1.5))
        p["arm_l"]["r"] = (16 * S(i, 6), -6, 0)
        p["arm_r"]["r"] = (-10 * S(i, 6), 6, 0)
        walk.append(p)

    # windup: the thrust stance - sword shoulder twisted back, blade drawn back at the hip
    # and levelled at the target, the free hand thrust forward to aim, leaning back,
    # eyes flaring - held while the line fills
    stance = {
        "hover": {"l": (0, 0.05, 0.02)},
        "waist": {"r": (-8, 0, 0)},
        "chest": {"r": (-4, 0, -34)},
        "head": {"r": (4, 0, 30)}, "eyes": {"s": 1.45},
        "arm_r": {"r": (40, -10, 0)}, "fore_r": {"r": (-100, 0, 0)}, "hand_r": {"r": (16, 0, 0)},
        "arm_l": {"r": (-70, -8, 0)}, "fore_l": {"r": (-12, 0, 0)},
        "plume": {"r": (-10, 0, 10)},
        "cape1": {"r": (-6, 0, 12)}, "cape2": {"r": (-4, 0, 8)},
        "tab_f": {"r": (6, 0, 0)}, "tab_b": {"r": (-6, 0, 0)},
        "wisp1": {"r": (-8, 0, 10)}, "wisp2": {"r": (-6, 0, 18)}, "wisp3": {"r": (4, 0, 26)},
    }
    windup = [lerp_pose(idle[0], stance, 0.5), stance,
              merge(stance, {"hover": {"l": (0, 0.055, 0.025)}, "wisp3": {"r": (4, 0, 34)}}),
              merge(stance, {"hover": {"l": (0, 0.05, 0.018)}, "wisp3": {"r": (4, 0, 18)}})]

    # attack: the whole body lunges along the line, sword arm driving straight through
    # (f1 = hit, arm fully extended), held a beat (f2), drawn back (f3)
    thrust = {
        "hover": {"l": (0, -0.12, -0.01)},
        "waist": {"r": (14, 0, 0)},
        "chest": {"r": (6, 0, 26)},
        "head": {"r": (-4, 0, -22)}, "eyes": {"s": 1.3},
        "arm_r": {"r": (-84, 6, 0)}, "fore_r": {"r": (-4, 0, 0)}, "hand_r": {"r": (44, 0, 0)},
        "arm_l": {"r": (36, -26, 0)}, "fore_l": {"r": (-20, 0, 0)},
        "plume": {"r": (50, 0, 0)},
        "cape1": {"r": (40, 0, -6)}, "cape2": {"r": (30, 0, -6)},
        "tab_f": {"r": (30, 0, 0)}, "tab_b": {"r": (40, 0, 0)},
        "wisp1": {"r": (40, 0, -6)}, "wisp2": {"r": (30, 0, -10)}, "wisp3": {"r": (24, 0, -14)},
    }
    attack = [lerp_pose(stance, thrust, 0.55),
              thrust,
              merge(thrust, {"hover": {"l": (0, -0.11, -0.005)}, "cape2": {"r": (40, 0, 4)},
                             "wisp3": {"r": (34, 0, 6)}, "plume": {"r": (36, 0, 8)}}),
              lerp_pose(thrust, idle[0], 0.65)]

    hit = [merge(base(0, 4), {"hover": {"l": (0, 0.07, 0.02)}, "waist": {"r": (-16, 0, 0)},
                              "chest": {"r": (-8, 0, 8)}, "head": {"r": (-18, 0, 12)}, "eyes": {"s": 0.6},
                              "arm_l": {"r": (20, -30, 0)}, "arm_r": {"r": (20, 30, 0)},
                              "wisp1": {"r": (-20, 0, 0)}, "wisp2": {"r": (-14, 0, 0)},
                              "cape1": {"r": (-20, 0, 0)}, "plume": {"r": (-30, 0, 0)}}),
           merge(base(1, 4), {"hover": {"l": (0, 0.03, 0.01)}, "waist": {"r": (-6, 0, 0)},
                              "head": {"r": (-6, 0, 4)}, "cape1": {"r": (12, 0, 0)}})]

    # die: the spirit leaves and the empty armour falls in a heap, eyes going out
    die = [
        merge(base(0, 4), {"hover": {"l": (0, 0.05, 0.03)}, "waist": {"r": (-18, 0, 0)},
                           "head": {"r": (-24, 0, 0)}, "eyes": {"s": 1.4},
                           "arm_l": {"r": (-20, -40, 0)}, "arm_r": {"r": (-20, 40, 0)}}),
        merge(base(1, 4), {"hover": {"l": (0, 0.02, -0.08)}, "waist": {"r": (18, 0, 6)},
                           "head": {"r": (26, 0, 10)}, "eyes": {"s": 0.8},
                           "wisp1": {"s": 0.7}, "arm_l": {"r": (10, -10, 0)}, "arm_r": {"r": (10, 10, 0)}}),
        {"hover": {"l": (0, 0.0, -0.22)}, "waist": {"r": (30, 0, 10)}, "head": {"r": (30, 0, 14)},
         "eyes": {"s": 0.5}, "wisp1": {"s": 0.4}, "arm_l": {"r": (20, -20, 0)}, "arm_r": {"r": (20, 20, 0)},
         "cape1": {"r": (-20, 0, 0)}},
        {"hover": {"l": (0, 0.04, -0.40)}, "waist": {"r": (55, 0, 14)}, "head": {"r": (24, 0, 30), "l": (0, -0.02, -0.02)},
         "eyes": {"s": 0.25}, "wisp1": {"s": 0.15}, "arm_l": {"r": (-30, -40, 0)}, "arm_r": {"r": (-30, 40, 0)},
         "cape1": {"r": (-40, 0, 0)}, "tab_f": {"r": (-40, 0, 0)}},
        {"hover": {"l": (0, 0.06, -0.47)}, "waist": {"r": (70, 0, 18)}, "head": {"r": (14, 0, 40), "l": (0.04, -0.02, -0.06)},
         "eyes": {"s": 0.05}, "wisp1": {"s": 0.02}, "arm_l": {"r": (-50, -60, 0)}, "arm_r": {"r": (-40, 60, 0)},
         "cape1": {"r": (-60, 0, 0)}, "cape2": {"r": (-30, 0, 0)}, "tab_f": {"r": (-60, 0, 0)}},
        {"hover": {"l": (0, 0.06, -0.48)}, "waist": {"r": (72, 0, 18)}, "head": {"r": (12, 0, 44), "l": (0.05, -0.02, -0.07)},
         "eyes": {"s": 0.001}, "wisp1": {"s": 0.001}, "arm_l": {"r": (-52, -62, 0)}, "arm_r": {"r": (-42, 62, 0)},
         "cape1": {"r": (-62, 0, 0)}, "cape2": {"r": (-32, 0, 0)}, "tab_f": {"r": (-62, 0, 0)}},
    ]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
