"""Tâm Ma (inner demon). Runs inside Blender; see creatures.py for the pose
conventions."""
from __future__ import annotations

import math

from mathutils import Vector

from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material, merge,
                 place, prism, set_root_offset, shadow, skin, tube, use_collection)

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


# =============================================================== Tâm Ma
def build_tam_ma():
    use_collection("COL_tam_ma")
    face = material("MAT_tm_face", (0.52, 0.34, 0.75), (0.78, 0.33, 0.23), ramp=("purple", "red"))
    hair = material("MAT_tm_hair", (0.23, 0.13, 0.38), (0.18, 0.16, 0.20), ramp=("purple", "hair"))
    robe = material("MAT_tm_robe", (0.36, 0.21, 0.56), (0.58, 0.19, 0.16), ramp=("purple", "red"))
    robe_lt = material("MAT_tm_collar", (0.52, 0.34, 0.75), (0.90, 0.72, 0.23), ramp=("purple", "gold"))
    sash = material("MAT_tm_sash", (0.18, 0.16, 0.20), (0.18, 0.16, 0.20), ramp="hair")
    smoke = material("MAT_tm_smoke", (0.23, 0.13, 0.38), (0.36, 0.10, 0.11), ramp=("purple", "red"))
    smoke_lt = material("MAT_tm_smoke_light", (0.36, 0.21, 0.56), (0.58, 0.19, 0.16), ramp=("purple", "red"))
    eye = material("MAT_tm_eye", (0.85, 0.97, 1.0), (1.0, 0.89, 0.48), emit=7.0, glow=("ice", "holy"))
    trim = material("MAT_tm_trim_edge", (0.78, 0.55, 1.0), (1.0, 0.68, 0.23), emit=3.0,
                    glow=("cosmic", "flame"))
    # dark, but with form: the light band of the cel shading starts earlier on the robe,
    # face and smoke, so the shade keeps a lit rim instead of reading as a flat blot
    for m in (face, robe, robe_lt, smoke, smoke_lt, hair):
        m["kit_light"] = 0.55
        m["kit_shadow"] = 0.12
    socket = material("MAT_tm_socket", (0.06, 0.05, 0.07), (0.06, 0.05, 0.07), ramp="hair")
    pin = material("MAT_tm_pin", (0.81, 0.80, 0.83), (0.90, 0.72, 0.23), ramp=("bone", "gold"))
    blade = material("MAT_tm_blade", (0.18, 0.16, 0.20), (0.18, 0.16, 0.20), ramp="hair")
    edge = material("MAT_tm_edge", (0.78, 0.55, 1.0), (1.0, 0.68, 0.23), emit=6.0, glow=("cosmic", "flame"))

    arm = armature("tam_ma", [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hips", (0, 0, 0.44), (0, 0, 0.55), "root"),
        ("chest", (0, 0, 0.55), (0, 0, 0.72), "hips"),
        ("head", (0, 0, 0.72), (0, 0, 1.0), "chest"),
        ("ribbon", (0, 0.08, 1.06), (0, 0.16, 0.92), "head"),
        ("arm_l", (0.13, 0, 0.69), (0.25, -0.02, 0.49), "chest"),
        ("hand_l", (0.25, -0.02, 0.49), (0.28, -0.03, 0.42), "arm_l"),
        ("arm_r", (-0.13, 0, 0.69), (-0.25, -0.02, 0.49), "chest"),
        ("hand_r", (-0.25, -0.02, 0.49), (-0.28, -0.03, 0.42), "arm_r"),
        ("smoke1", (0, 0, 0.44), (0, 0.02, 0.30), "hips"),
        ("smoke2", (0, 0.02, 0.30), (0, 0.06, 0.17), "smoke1"),
        ("smoke3", (0, 0.06, 0.17), (0, 0.12, 0.05), "smoke2"),
    ])
    # head (big chibi head), hair cap, bangs, side locks, bun with a pin and ribbons
    hd = [ball("tm_head", (0.20, 0.19, 0.19), (0, -0.01, 0.86), face),
          ball("tm_hair", (0.212, 0.2, 0.17), (0, 0.05, 0.95), hair),
          ball("tm_bun", (0.095, 0.09, 0.085), (0, 0.06, 1.11), hair, seg=12, rings=8),
          aim("tm_pin", pin, (-0.14, 0.06, 1.12), (0.15, 0.06, 1.14), 0.014, 0.014, seg=6),
          ball("tm_sockl", (0.052, 0.014, 0.064), (0.075, -0.176, 0.85), socket, seg=10, rings=6),
          ball("tm_sockr", (0.052, 0.014, 0.064), (-0.075, -0.176, 0.85), socket, seg=10, rings=6),
          ball("tm_eyel", (0.034, 0.012, 0.046), (0.075, -0.186, 0.848), eye, seg=10, rings=6),
          ball("tm_eyer", (0.034, 0.012, 0.046), (-0.075, -0.186, 0.848), eye, seg=10, rings=6)]
    for k, x in enumerate((-0.10, -0.035, 0.035, 0.10)):
        hd.append(aim(f"tm_bang{k}", hair, (x, -0.165, 0.99), (x * 1.15, -0.205, 0.905),
                      0.045, 0.0, seg=6))
    for sx in (-1, 1):
        hd.append(aim(f"tm_lock{sx}", hair, (sx * 0.175, -0.06, 0.93), (sx * 0.20, -0.07, 0.72),
                      0.045, 0.012, seg=6))
    att(arm, "head", *hd)
    att(arm, "ribbon", aim("tm_rib1", smoke_lt, (0.03, 0.08, 1.07), (0.07, 0.18, 0.92), 0.02, 0.006, seg=5),
        aim("tm_rib2", smoke_lt, (-0.03, 0.08, 1.07), (-0.05, 0.19, 0.95), 0.02, 0.006, seg=5))
    # robe torso, crossed collar, sash
    folds = [aim(f"tm_fold{k}", smoke, (x, -0.15 + abs(x) * 0.3, 0.47), (x * 0.6, -0.10, 0.66),
                 0.016, 0.006, seg=5) for k, x in enumerate((-0.10, -0.045, 0.045, 0.10))]
    att(arm, "chest", cone("tm_torso", 0.165, 0.10, 0.28, (0, 0, 0.59), robe, seg=14), *folds,
        box("tm_collarl", (0.03, 0.02, 0.17), (0.03, -0.135, 0.635), robe_lt, rot=(-12, 28, 0)),
        box("tm_collarr", (0.03, 0.02, 0.17), (-0.03, -0.135, 0.635), robe_lt, rot=(-12, -28, 0)))
    att(arm, "hips", cone("tm_sash", 0.17, 0.16, 0.05, (0, 0, 0.50), sash, seg=14),
        box("tm_knot", (0.05, 0.03, 0.04), (0.05, -0.165, 0.50), sash),
        aim("tm_knottail", sash, (0.05, -0.17, 0.49), (0.08, -0.18, 0.38), 0.018, 0.01, seg=5))
    # smoke instead of legs, skinned to a three-bone tail so it trails and curls
    zs = [0.50, 0.45, 0.38, 0.30, 0.22, 0.15, 0.09, 0.05]
    ys = [0.0, 0.0, 0.01, 0.025, 0.045, 0.07, 0.10, 0.13]
    rs = [0.16, 0.20, 0.19, 0.155, 0.115, 0.08, 0.045, 0.012]

    def lumps(i, a):
        return 1.0 + (0.16 * math.sin(5 * a + i * 1.3) if i >= 2 else 0.0)
    sm = tube("tm_smoke", [(0, y, z) for y, z in zip(ys, zs)], rs, smoke, seg=18,
              up=(0, -1, 0), wobble=lumps)
    skin(sm, arm, ["hips", "smoke1", "smoke2", "smoke3"], power=3)
    att(arm, "smoke1", aim("tm_wispl", smoke_lt, (0.12, 0.0, 0.36), (0.22, 0.06, 0.22), 0.05, 0.0, seg=8),
        aim("tm_wispr", smoke_lt, (-0.12, 0.0, 0.36), (-0.21, 0.07, 0.24), 0.05, 0.0, seg=8))
    # wide sleeves, small hands
    for side, sx in (("l", 1), ("r", -1)):
        att(arm, f"arm_{side}",
            aim(f"tm_sleeve{side}", robe, (sx * 0.12, 0, 0.69), (sx * 0.26, -0.02, 0.47), 0.05, 0.09, seg=10),
            ball(f"tm_cuff{side}", (0.07, 0.07, 0.025), (sx * 0.26, -0.02, 0.47), smoke, rot=(0, sx * -30, 0), seg=10, rings=5),
            ball(f"tm_trim{side}", (0.088, 0.088, 0.012), (sx * 0.262, -0.02, 0.475), trim, rot=(0, sx * -30, 0), seg=12, rings=4))
        att(arm, f"hand_{side}", ball(f"tm_hand{side}", (0.04,) * 3, (sx * 0.27, -0.03, 0.44), face, seg=10, rings=6))
    # the shadow blade, held low and out from the right hand
    grip_at = Vector((-0.27, -0.05, 0.44))
    d = Vector((-0.12, -0.08, -0.99)).normalized()
    M = place(d, grip_at)
    bl = [prism("tm_blade", [(-0.034, 0.03), (0.034, 0.03), (0.034, 0.31), (0.0, 0.37), (-0.034, 0.31)],
                0.02, blade, matrix=M),
          prism("tm_edgel", [(0.03, 0.05), (0.044, 0.05), (0.044, 0.31), (0.0, 0.385), (0.03, 0.30)],
                0.012, edge, matrix=M),
          prism("tm_edger", [(-0.044, 0.05), (-0.03, 0.05), (-0.03, 0.30), (0.0, 0.385), (-0.044, 0.31)],
                0.012, edge, matrix=M),
          prism("tm_guard", [(-0.075, -0.0), (0.075, -0.0), (0.06, 0.03), (-0.06, 0.03)], 0.04, sash, matrix=M),
          prism("tm_grip", [(-0.016, -0.11), (0.016, -0.11), (0.016, 0.0), (-0.016, 0.0)], 0.03, hair, matrix=M)]
    att(arm, "hand_r", *bl)
    shade = material("MAT_tm_shadow", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    shadow("tm_shadow", 0.13, 0.11, shade, arm)
    set_root_offset((0, 0, 0.08))      # floats a hand's breadth higher than it stands

    # --- clips. Arms hang down-out: +x swings the hand back, -x lifts it forward.
    def float_pose(i, n, bob=0.025, lean=0.0):
        return {
            "hips": {"l": (0, 0, bob * S(i, n)), "r": (lean, 0, 0)},
            "chest": {"r": (-1.5 * S(i, n), 0, 0)},
            "head": {"r": (2 * S(i, n, -0.6), 0, 3 * S(i, n, 0.3))},
            "smoke1": {"r": (6 + 4 * S(i, n, -0.8), 0, 0), "s": 1.0},
            "smoke2": {"r": (12 + 10 * S(i, n, -1.6), 0, 20 * S(i, n, -1.6))},
            "smoke3": {"r": (18 + 14 * S(i, n, -2.4), 0, 32 * S(i, n, -2.4))},
            "arm_l": {"r": (4 * S(i, n, -0.5), -3, 0)}, "arm_r": {"r": (4 * S(i, n, -0.5), 3, 0)},
            "hand_r": {"r": (0, -18, 0)},
            "ribbon": {"r": (10 * S(i, n, -1.2), 0, 8 * S(i, n, -1.5))},
        }
    idle = [float_pose(i, 4) for i in range(4)]
    walk = []
    for i in range(6):
        p = float_pose(i, 6, bob=0.03, lean=10)
        p["smoke1"]["r"] = (28 + 5 * S(i, 6), 0, 0)
        p["smoke2"]["r"] = (22, 0, 12 * S(i, 6, -1.2))
        p["smoke3"]["r"] = (16, 0, 18 * S(i, 6, -2.0))
        p["arm_l"]["r"] = (18 * S(i, 6), -3, 0)
        p["arm_r"]["r"] = (-18 * S(i, 6), 3, 0)
        p["ribbon"]["r"] = (35, 0, 10 * S(i, 6, -1.5))
        walk.append(p)
    # windup: blade raised high behind the head, body twisted and leaning back, the free
    # hand thrust forward to aim — the classic "about to cut" pose
    raised = {
        "hips": {"l": (0, 0.03, 0.04), "r": (-6, 0, 0)},
        "chest": {"r": (-12, 0, 24)},
        "head": {"r": (8, 0, -18)},
        "arm_r": {"r": (146, -22, 0)}, "hand_r": {"r": (34, 0, 0)},
        "arm_l": {"r": (-65, 25, 0)},
        "smoke1": {"r": (-10, 0, 0)}, "smoke2": {"r": (-14, 0, 8)}, "smoke3": {"r": (-10, 0, 16)},
        "ribbon": {"r": (-20, 0, 15)},
    }
    windup = [lerp_pose(idle[0], raised, 0.45), raised,
              merge(raised, {"smoke3": {"r": (-10, 0, 24)}, "hips": {"l": (0, 0.03, 0.05)}}),
              merge(raised, {"smoke3": {"r": (-10, 0, 8)}, "hips": {"l": (0, 0.03, 0.045)}})]
    # attack: the blade comes over the top (f1), cuts down across the body to the other
    # hip (f2 = hit), the twist carries through (f3) and it settles (f4)
    attack = [
        {"hips": {"l": (0, -0.03, 0.03), "r": (6, 0, 0)}, "chest": {"r": (6, 0, 6)},
         "head": {"r": (0, 0, -4)},
         "arm_r": {"r": (-140, -8, 0)}, "hand_r": {"r": (0, 0, 0)},
         "arm_l": {"r": (20, 20, 0)},
         "smoke1": {"r": (30, 0, 0)}, "smoke2": {"r": (22, 0, -8)}, "smoke3": {"r": (18, 0, -16)},
         "ribbon": {"r": (40, 0, 0)}},
        {"hips": {"l": (0, -0.06, 0.0), "r": (14, 0, 0)}, "chest": {"r": (14, 0, -32)},
         "head": {"r": (0, 0, 18)},
         "arm_r": {"r": (-62, 0, -55)}, "hand_r": {"r": (-20, 0, 0)},
         "arm_l": {"r": (30, 30, 0)},
         "smoke1": {"r": (36, 0, 8)}, "smoke2": {"r": (26, 0, -14)}, "smoke3": {"r": (22, 0, -26)},
         "ribbon": {"r": (50, 0, -20)}},
        {"hips": {"l": (0, -0.05, 0.0), "r": (10, 0, 0)}, "chest": {"r": (10, 0, -38)},
         "head": {"r": (0, 0, 16)},
         "arm_r": {"r": (-40, 10, -70)}, "hand_r": {"r": (-20, 0, 0)}, "arm_l": {"r": (16, 20, 0)},
         "smoke1": {"r": (22, 0, 4)}, "smoke2": {"r": (14, 0, -6)}, "smoke3": {"r": (10, 0, -14)},
         "ribbon": {"r": (20, 0, -30)}},
        {"hips": {"l": (0, -0.015, 0.0), "r": (3, 0, 0)}, "chest": {"r": (3, 0, -10)},
         "head": {"r": (0, 0, 4)},
         "arm_r": {"r": (-12, 4, -16)}, "arm_l": {"r": (5, 5, 0)},
         "smoke1": {"r": (10, 0, 0)}, "smoke2": {"r": (4, 0, 4)}, "smoke3": {"r": (0, 0, 8)},
         "ribbon": {"r": (-10, 0, -10)}},
    ]
    hit = [{"hips": {"l": (0, 0.07, 0.02), "r": (-14, 0, 0)}, "chest": {"r": (-12, 0, 6)},
            "head": {"r": (-16, 0, 10)}, "arm_l": {"r": (20, -30, 0)}, "arm_r": {"r": (20, 30, 0)},
            "smoke1": {"r": (-20, 0, 0)}, "smoke2": {"r": (-10, 0, 0)}, "ribbon": {"r": (-30, 0, 0)}},
           {"hips": {"l": (0, 0.03, 0.01), "r": (-5, 0, 0)}, "chest": {"r": (-4, 0, 2)},
            "head": {"r": (-6, 0, 4)}, "arm_l": {"r": (8, -10, 0)}, "arm_r": {"r": (8, 10, 0)},
            "smoke1": {"r": (10, 0, 0)}, "ribbon": {"r": (20, 0, 0)}}]
    die = [
        {"hips": {"l": (0, 0.05, 0.02), "r": (-16, 0, 0)}, "head": {"r": (-24, 0, 0)},
         "arm_l": {"r": (-20, -40, 0)}, "arm_r": {"r": (-20, 40, 0)}, "smoke1": {"r": (-20, 0, 0)}},
        {"hips": {"l": (0, 0.0, -0.10), "r": (20, 0, 0)}, "chest": {"r": (18, 0, 0)},
         "head": {"r": (20, 0, 0)}, "arm_l": {"r": (-30, 10, 0)}, "arm_r": {"r": (-30, -10, 0)},
         "smoke1": {"r": (40, 0, 0)}, "smoke2": {"r": (30, 0, 0)}},
        {"hips": {"l": (0, 0.0, 0.04), "r": (-8, 0, 0), "s": 1.0}, "head": {"r": (-30, 0, 0)},
         "arm_l": {"r": (0, -38, 0)}, "arm_r": {"r": (0, 38, 0)},
         "smoke1": {"r": (-10, 0, 0)}, "smoke2": {"r": (-10, 0, 0)}, "ribbon": {"r": (-40, 0, 0)}},
        {"hips": {"l": (0, 0.0, 0.10), "s": 0.7}, "head": {"r": (-20, 0, 0)},
         "arm_l": {"r": (0, -70, 0)}, "arm_r": {"r": (0, 70, 0)}, "smoke1": {"s": 1.2}},
        {"hips": {"l": (0, 0.0, 0.16), "s": 0.35}, "arm_l": {"r": (0, -80, 0)},
         "arm_r": {"r": (0, 80, 0)}, "smoke1": {"s": 1.3}},
        {"hips": {"l": (0, 0.0, 0.2), "s": 0.0}},
    ]
    arm.scale = (1.07, 1.07, 1.07)      # elite: fill the 64 px frame
    for frames in (idle, walk, windup, attack, hit):
        for p in frames:          # blade held a little inward, tip clear of the ground
            p.setdefault("hand_r", {"r": (0, -18, 0)})
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 10, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=1)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    arm.animation_data.action = None
    return arm
