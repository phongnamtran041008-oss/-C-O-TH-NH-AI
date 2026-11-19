"""MONSTERS_B, part 1: Đầu Tử Oa (dice toad), Hồ Lô Tinh (gourd imp), Mộc Yêu (stump
sapling), Cơ Quan Nhân (clockwork puppet). Runs inside Blender; pose conventions as in
creatures.py (armature axes; +x tips an upright bone forward and swings a hanging bone's
tip back; +y tilts an upright bone's top toward +x).

All four stand on compact feet: whatever touches the ground in front of the origin draws
below the sprite pivot, and the kit's QC allows only a few pixels there.
"""
from __future__ import annotations

import math

from mathutils import Euler, Matrix, Vector

from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material, merge,
                 set_root_offset, tube, use_collection)

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def six(arm, idle, walk, windup, attack, hit, die, walk_fps=10, hit_frame=1):
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, walk_fps, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=hit_frame)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    arm.animation_data.action = None


# =============================================================== Đầu Tử Oa
PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)]}


def die_block(name, center, size, rot, mat, pip_mat, faces):
    """A die-shaped wart: a cube with dot pips (dots only, never numerals).
    faces: {"top"/"front"/"left"/"right"/"back": pip count}."""
    out = [box(name, (size,) * 3, center, mat, rot=rot, bevel=size * 0.12)]
    R = Euler([math.radians(a) for a in rot], "XYZ").to_matrix()
    c = Vector(center)
    h = size / 2
    axes = {"top": (Vector((0, 0, 1)), Vector((1, 0, 0)), Vector((0, 1, 0))),
            "front": (Vector((0, -1, 0)), Vector((1, 0, 0)), Vector((0, 0, 1))),
            "back": (Vector((0, 1, 0)), Vector((1, 0, 0)), Vector((0, 0, 1))),
            "left": (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))),
            "right": (Vector((-1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))}
    for face, n in faces.items():
        nrm, u, v = axes[face]
        for k, (a, b) in enumerate(PIPS[n]):
            p = c + R @ (nrm * (h + 0.002) + u * a * size * 0.27 + v * b * size * 0.27)
            out.append(ball(f"{name}_pip{face}{k}", (0.025, 0.025, 0.025), tuple(p), pip_mat,
                            seg=8, rings=5))
    return out


def build_dau_tu_oa():
    use_collection("COL_dau_tu_oa")
    set_root_offset((0, 0.02, 0))
    skin = material("MAT_dt_skin", (0.23, 0.42, 0.15), (0.36, 0.21, 0.56), ramp=("leaf", "purple"))
    spot = material("MAT_dt_spot", (0.13, 0.25, 0.11), (0.23, 0.13, 0.38), ramp=("leaf", "purple"))
    belly = material("MAT_dt_belly", (0.93, 0.87, 0.70), (0.95, 0.70, 0.72), ramp=("paper", "pink"))
    dice = material("MAT_dt_dice", (0.93, 0.87, 0.70), (0.90, 0.72, 0.23), ramp=("paper", "gold"))
    pip = material("MAT_dt_pip", (0.11, 0.10, 0.13), (0.58, 0.19, 0.16), ramp=("hair", "red"))
    eye = material("MAT_dt_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=5.0, glow=("holy", "flame"))
    pupil = material("MAT_dt_pupil_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    tongue = material("MAT_dt_tongue", (0.90, 0.55, 0.62), (0.90, 0.55, 0.62), ramp="pink")

    arm = armature("dau_tu_oa", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0.03, 0.08), (0, 0.03, 0.3), "root"),
        ("head", (0, -0.08, 0.22), (0, -0.08, 0.40), "body"),
        ("jaw", (0, -0.10, 0.215), (0, -0.26, 0.215), "head"),
        ("sac", (0, -0.14, 0.19), (0, -0.14, 0.26), "head"),
        ("tongue", (0, -0.19, 0.235), (0, -0.31, 0.235), "head"),
        ("eye_l", (0.09, -0.10, 0.34), (0.09, -0.10, 0.44), "head"),
        ("eye_r", (-0.09, -0.10, 0.34), (-0.09, -0.10, 0.44), "head"),
        ("dice", (0, 0.07, 0.30), (0, 0.07, 0.44), "body"),
        ("leg_fl", (0.08, -0.05, 0.14), (0.08, -0.07, 0.02), "body"),
        ("leg_fr", (-0.08, -0.05, 0.14), (-0.08, -0.07, 0.02), "body"),
        ("leg_bl", (0.14, 0.09, 0.14), (0.075, 0.03, 0.02), "body"),
        ("leg_br", (-0.14, 0.09, 0.14), (-0.075, 0.03, 0.02), "body"),
    ])
    att(arm, "body", ball("dt_body", (0.21, 0.20, 0.15), (0, 0.03, 0.19), skin),
        ball("dt_belly", (0.16, 0.13, 0.10), (0, -0.05, 0.14), belly),
        *[ball(f"dt_spot{k}", (0.045, 0.04, 0.018), p, spot, rot=r, seg=10, rings=5)
          for k, (p, r) in enumerate((((0.17, 0.02, 0.24), (0, 60, 0)), ((-0.18, 0.06, 0.22), (0, -60, 0)),
                                      ((0.12, 0.16, 0.26), (-40, 40, 0)), ((-0.10, 0.17, 0.27), (-40, -40, 0))))])
    att(arm, "head", ball("dt_head", (0.19, 0.15, 0.11), (0, -0.10, 0.26), skin),
        box("dt_mouth", (0.25, 0.02, 0.018), (0, -0.238, 0.232), pupil),
        box("dt_mouthl", (0.04, 0.02, 0.016), (0.13, -0.215, 0.245), pupil, rot=(0, -30, 0)),
        box("dt_mouthr", (0.04, 0.02, 0.016), (-0.13, -0.215, 0.245), pupil, rot=(0, 30, 0)))
    att(arm, "jaw", ball("dt_jaw", (0.16, 0.12, 0.045), (0, -0.15, 0.205), belly))
    att(arm, "sac", ball("dt_sac", (0.09, 0.06, 0.07), (0, -0.17, 0.18), belly))
    att(arm, "tongue", aim("dt_tongue", tongue, (0, -0.19, 0.235), (0, -0.29, 0.235), 0.026, 0.022, seg=8),
        ball("dt_tonguetip", (0.035, 0.03, 0.03), (0, -0.30, 0.235), tongue, seg=8, rings=5))
    for s, b in ((1, "eye_l"), (-1, "eye_r")):
        att(arm, b, ball(f"dt_bulge{b}", (0.06, 0.06, 0.055), (s * 0.09, -0.10, 0.37), skin),
            ball(f"dt_eyeball{b}", (0.042, 0.02, 0.042), (s * 0.09, -0.153, 0.38), eye, seg=10, rings=6),
            box(f"dt_pupil{b}", (0.014, 0.012, 0.036), (s * 0.09, -0.172, 0.38), pupil))
    # the warty back: three die-shaped warts stacked up, pips only
    blocks = (die_block("dt_die1", (-0.07, 0.06, 0.33), 0.125, (0, 15, 20), dice, pip,
                        {"top": 3, "front": 2, "right": 1})
              + die_block("dt_die2", (0.08, 0.08, 0.32), 0.115, (10, -10, -15), dice, pip,
                          {"top": 2, "front": 1, "left": 3})
              + die_block("dt_die3", (0.0, 0.11, 0.44), 0.105, (20, 30, 10), dice, pip,
                          {"top": 1, "front": 3}))
    att(arm, "dice", *blocks)
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"leg_f{side}", aim(f"dt_arm{side}", skin, (s * 0.08, -0.05, 0.14), (s * 0.08, -0.07, 0.03), 0.036, 0.03, seg=8),
            box(f"dt_hand{side}", (0.06, 0.055, 0.022), (s * 0.07, -0.078, 0.012), skin))
        att(arm, f"leg_b{side}", ball(f"dt_thigh{side}", (0.07, 0.10, 0.07), (s * 0.13, 0.08, 0.125), skin),
            box(f"dt_foot{side}", (0.065, 0.08, 0.022), (s * 0.075, 0.0, 0.012), skin))

    def base(i, n, sac=1.0, blink=False):
        return {"body": {"l": (0, 0, 0.004 * S(i, n))},
                "sac": {"s": sac},
                "eye_l": {"s": (1, 0.25, 1) if blink else 1.0},
                "eye_r": {"s": (1, 0.25, 1) if blink else 1.0},
                "dice": {"r": (2 * S(i, n, 1), 0, 3 * S(i, n))}}
    idle = [base(i, 4, sac=1.0 + 0.35 * (0.5 - 0.5 * C(i, 4)), blink=(i == 3)) for i in range(4)]
    hop = [(0.0, -0.02, 0, 0), (-0.02, 0.0, 6, -10), (0.035, 0.05, -10, 30),
           (0.05, 0.04, -4, 20), (0.0, -0.02, 6, -5), (-0.015, 0.0, 2, 0)]
    walk = []
    for i, (z, legz, tilt, kick) in enumerate(hop):
        p = base(i, 6, sac=1.0)
        p["body"] = {"l": (0, 0, z), "r": (tilt, 0, 0)}
        p["leg_bl"] = {"r": (kick, 0, 0), "l": (0, 0, -z if z < 0 else -z * 0.6)}
        p["leg_br"] = {"r": (kick, 0, 0), "l": (0, 0, -z if z < 0 else -z * 0.6)}
        p["leg_fl"] = {"r": (-kick * 0.6, 0, 0), "l": (0, 0, -z * 0.8)}
        p["leg_fr"] = {"r": (-kick * 0.6, 0, 0), "l": (0, 0, -z * 0.8)}
        walk.append(p)
    # windup: squats low, head tipped up, the throat sac swelling to twice its size
    puff = merge(base(0, 4), {
        "body": {"l": (0, -0.01, 0.0), "r": (-6, 0, 0), "s": (1.06, 1.0, 1.0)},
        "head": {"r": (-14, 0, 0)}, "jaw": {"r": (10, 0, 0)}, "sac": {"s": 1.85},
        "leg_fl": {"l": (0, 0, 0.03)}, "leg_fr": {"l": (0, 0, 0.03)},
        "leg_bl": {"l": (0, 0, 0.03)}, "leg_br": {"l": (0, 0, 0.03)},
        "eye_l": {"s": 1.15}, "eye_r": {"s": 1.15}})
    windup = [lerp_pose(idle[0], puff, 0.5), puff, merge(puff, {"sac": {"s": 1.95}}),
              merge(puff, {"sac": {"s": 1.9}, "dice": {"r": (0, 0, 4)}})]
    # attack: the tongue lashes out in a straight line, slightly upward
    attack = [
        merge(base(0, 4), {"body": {"r": (4, 0, 0)}, "head": {"r": (-24, 0, 0)},
                           "jaw": {"r": (36, 0, 0)}, "tongue": {"s": (1, 1.9, 1)}, "sac": {"s": 1.2}}),
        merge(base(0, 4), {"body": {"r": (4, 0, 0)}, "head": {"r": (-30, 0, 0)},
                           "jaw": {"r": (42, 0, 0)}, "tongue": {"s": (1.15, 2.3, 1.15)}, "sac": {"s": 0.8}}),
        merge(base(0, 4), {"body": {"r": (4, 0, 0)}, "head": {"r": (-8, 0, 0)},
                           "jaw": {"r": (24, 0, 0)}, "tongue": {"s": (1, 1.3, 1)}, "sac": {"s": 0.9}}),
        merge(base(0, 4), {"jaw": {"r": (4, 0, 0)}, "sac": {"s": 1.0}}),
    ]
    hit = [merge(base(0, 4), {"body": {"r": (-10, 0, 5), "l": (0, -0.01, 0.015), "s": (1.06, 1, 0.92)},
                              "head": {"r": (-10, 0, 0)}, "eye_l": {"s": (1, 0.4, 1)},
                              "eye_r": {"s": (1, 0.4, 1)}, "jaw": {"r": (14, 0, 0)}}),
           merge(base(0, 4), {"body": {"r": (-5, 0, 2)}, "eye_l": {"s": (1, 0.7, 1)}, "eye_r": {"s": (1, 0.7, 1)}})]
    flat = merge(base(0, 4), {"body": {"l": (0, 0, -0.035), "s": (1.12, 1.05, 0.62)},
                              "head": {"r": (14, 0, 12)}, "sac": {"s": 0.5}, "jaw": {"r": (12, 0, 0)},
                              "eye_l": {"s": (1, 0.15, 1)}, "eye_r": {"s": (1, 0.15, 1)},
                              "dice": {"l": (0.03, 0.03, -0.08), "r": (0, 40, 25)},
                              "leg_fl": {"r": (-30, 0, 0)}, "leg_fr": {"r": (-30, 0, 0)}})
    die = [merge(base(0, 4), {"body": {"l": (0, 0, 0.03), "r": (-10, 0, 0)}, "jaw": {"r": (30, 0, 0)},
                              "sac": {"s": 1.6}}),
           merge(base(0, 4), {"body": {"r": (6, 0, 8)}, "sac": {"s": 0.8}, "head": {"r": (10, 0, 8)}}),
           lerp_pose(base(0, 4), flat, 0.6), flat,
           merge(flat, {"dice": {"l": (0.035, 0.035, -0.09), "r": (0, 46, 30)}}),
           merge(flat, {"dice": {"l": (0.035, 0.035, -0.09), "r": (0, 46, 30)}})]
    arm.scale = (1.3, 1.3, 1.3)        # a fat toad that fills its frame
    six(arm, idle, walk, windup, attack, hit, die)
    return arm


# =============================================================== Hồ Lô Tinh
def build_ho_lo_tinh():
    use_collection("COL_ho_lo_tinh")
    gourd = material("MAT_hl_gourd", (0.68, 0.48, 0.28), (0.52, 0.34, 0.75), ramp=("wood", "purple"))
    gourd_dk = material("MAT_hl_gourd_dark", (0.51, 0.32, 0.18), (0.36, 0.21, 0.56), ramp=("wood", "purple"))
    cord = material("MAT_hl_cord", (0.78, 0.33, 0.23), (0.90, 0.72, 0.23), ramp=("red", "gold"))
    leaf = material("MAT_hl_leaf", (0.37, 0.58, 0.20), (0.31, 0.65, 0.47), ramp=("leaf", "jade"))
    cork = material("MAT_hl_cork", (0.42, 0.35, 0.28), (0.42, 0.35, 0.28), ramp="earth")
    eye = material("MAT_hl_eye", (1.0, 0.89, 0.48), (0.78, 0.55, 1.0), emit=6.0, glow=("holy", "cosmic"))
    dark = material("MAT_hl_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    beads = [material(f"MAT_hl_bead_{g}", c, c, emit=4.0, glow=g)
             for g, c in (("spirit", (0.35, 0.88, 0.96)), ("flame", (1.0, 0.68, 0.23)),
                          ("verdant", (0.48, 0.92, 0.6)), ("cosmic", (0.78, 0.55, 1.0)))]
    for b in beads:
        b["kit_halo"] = 1

    arm = armature("ho_lo_tinh", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0, 0.04), (0, 0, 0.30), "root"),
        ("upper", (0, 0, 0.30), (0, 0, 0.52), "body"),
        ("eyes", (0, -0.10, 0.42), (0, -0.10, 0.50), "upper"),
        ("cork", (0, 0, 0.58), (0, 0, 0.66), "upper"),
        ("spray", (0, -0.03, 0.60), (0, -0.20, 0.60), "upper"),
        ("arm_l", (0.15, -0.02, 0.27), (0.24, -0.04, 0.19), "body"),
        ("arm_r", (-0.15, -0.02, 0.27), (-0.24, -0.04, 0.19), "body"),
        ("leg_l", (0.075, 0, 0.09), (0.08, -0.02, 0.0), "body"),
        ("leg_r", (-0.075, 0, 0.09), (-0.08, -0.02, 0.0), "body"),
    ])
    ring = [(0.088 * math.cos(TAU * k / 16), 0.088 * math.sin(TAU * k / 16), 0.335) for k in range(17)]
    att(arm, "body", ball("hl_lower", (0.18, 0.17, 0.17), (0, 0, 0.20), gourd),
        ball("hl_stripe", (0.185, 0.03, 0.15), (0, 0, 0.20), gourd_dk, rot=(0, 0, 40)),
        tube("hl_cord", ring, [0.016] * 17, cord, seg=6, up=(0, 0, 1)),
        aim("hl_cordend", cord, (0.06, -0.06, 0.33), (0.09, -0.09, 0.22), 0.014, 0.01, seg=5),
        ball("hl_tassel", (0.025, 0.025, 0.035), (0.09, -0.09, 0.205), cord, seg=8, rings=5))
    att(arm, "upper", ball("hl_upper", (0.125, 0.12, 0.12), (0, 0, 0.44), gourd),
        cone("hl_neck", 0.065, 0.045, 0.08, (0, 0, 0.565), gourd_dk, seg=12),
        ball("hl_leaf1", (0.10, 0.025, 0.045), (0.08, 0.02, 0.60), leaf, rot=(0, -30, 20)),
        ball("hl_leaf2", (0.08, 0.025, 0.04), (-0.07, 0.03, 0.62), leaf, rot=(0, 35, -25)),
        aim("hl_stem", gourd_dk, (0.0, 0.03, 0.57), (0.04, 0.07, 0.68), 0.012, 0.006, seg=5),
        box("hl_grin", (0.07, 0.015, 0.014), (0, -0.117, 0.395), dark),
        box("hl_grinl", (0.022, 0.015, 0.012), (0.04, -0.113, 0.403), dark, rot=(0, -35, 0)),
        box("hl_grinr", (0.022, 0.015, 0.012), (-0.04, -0.113, 0.403), dark, rot=(0, 35, 0)))
    att(arm, "eyes", ball("hl_eyel", (0.032, 0.016, 0.042), (0.048, -0.112, 0.455), eye, rot=(0, 0, 15), seg=10, rings=6),
        ball("hl_eyer", (0.032, 0.016, 0.042), (-0.048, -0.112, 0.455), eye, rot=(0, 0, -15), seg=10, rings=6))
    att(arm, "cork", cone("hl_cork", 0.05, 0.056, 0.06, (0, 0, 0.625), cork, seg=10))
    spray = []
    for k, (dy, dx, dz) in enumerate(((0.06, 0.0, 0.0), (0.12, 0.04, 0.03), (0.13, -0.05, -0.02),
                                      (0.19, 0.0, 0.05), (0.20, 0.08, -0.01), (0.21, -0.09, 0.02),
                                      (0.27, 0.04, -0.03), (0.28, -0.04, 0.06), (0.30, 0.11, 0.04))):
        r = 0.026 + 0.004 * (k % 3)
        spray.append(ball(f"hl_bead{k}", (r, r, r), (dx, -0.03 - dy, 0.60 + dz), beads[k % 4], seg=8, rings=5))
    att(arm, "spray", *spray)
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"arm_{side}", aim(f"hl_arm{side}", gourd_dk, (s * 0.15, -0.02, 0.27), (s * 0.24, -0.04, 0.19), 0.036, 0.03, seg=8),
            ball(f"hl_hand{side}", (0.036,) * 3, (s * 0.245, -0.045, 0.185), gourd, seg=8, rings=5))
        att(arm, f"leg_{side}", ball(f"hl_foot{side}", (0.045, 0.05, 0.04), (s * 0.08, -0.02, 0.036), gourd_dk, seg=10, rings=6))

    def base(i, n, bob=0.008):
        return {"body": {"l": (0, 0, bob * S(i, n)), "s": (1 + 0.02 * S(i, n), 1, 1 - 0.02 * S(i, n))},
                "upper": {"r": (0, 5 * S(i, n, -0.8), 0)},
                "cork": {"r": (0, 4 * S(i, n, -1.6), 0)},
                "arm_l": {"r": (8 * S(i, n), -6, 0)}, "arm_r": {"r": (-8 * S(i, n), 6, 0)},
                "spray": {"s": 0.0},
                "leg_l": {"l": (0, 0, -bob * S(i, n))}, "leg_r": {"l": (0, 0, -bob * S(i, n))}}
    idle = [base(i, 4) for i in range(4)]
    walk = []
    for i in range(6):
        p = base(i, 6, bob=0.0)
        s = S(i, 6)
        p["body"] = {"l": (0, 0, 0.012 * abs(s)), "r": (0, 10 * s, 0)}
        p["upper"] = {"r": (0, -8 * s, 0)}
        p["leg_l"] = {"l": (0, 0, 0.03 * max(0.0, s) - 0.012 * abs(s))}
        p["leg_r"] = {"l": (0, 0, 0.03 * max(0.0, -s) - 0.012 * abs(s))}
        p["arm_l"] = {"r": (20 * s, -10, 0)}
        p["arm_r"] = {"r": (-20 * s, 10, 0)}
        walk.append(p)
    # windup: rears back, hugs itself, the cork working loose and the gourd swelling
    rear = merge(base(0, 4), {
        "body": {"r": (-14, 0, 0), "s": (1.08, 1.08, 1.05), "l": (0, 0.02, 0)},
        "upper": {"r": (-12, 0, 0), "s": 1.08}, "cork": {"l": (0, 0, 0.045), "r": (0, 18, 0)},
        "arm_l": {"r": (-60, 40, 0)}, "arm_r": {"r": (-60, -40, 0)},
        "leg_l": {"l": (0, -0.02, 0)}, "leg_r": {"l": (0, -0.02, 0)}})
    windup = [lerp_pose(idle[0], rear, 0.5), rear, merge(rear, {"cork": {"r": (0, -18, 0)}}),
              merge(rear, {"cork": {"r": (0, 20, 0)}, "upper": {"r": (-13, 0, 0)}})]
    # attack: the cork pops, the gourd tips forward and sprays a cone of spirit beads
    attack = [
        merge(base(0, 4), {"body": {"r": (14, 0, 0)}, "upper": {"r": (16, 0, 0)},
                           "cork": {"l": (0, 0.06, 0.20), "r": (70, 0, 30)}, "spray": {"s": 0.55},
                           "arm_l": {"r": (30, 0, 0)}, "arm_r": {"r": (30, 0, 0)}}),
        merge(base(0, 4), {"body": {"r": (18, 0, 0)}, "upper": {"r": (20, 0, 0)},
                           "cork": {"l": (0, 0.12, 0.28), "r": (160, 0, 50)}, "spray": {"s": 0.75},
                           "arm_l": {"r": (40, 0, 0)}, "arm_r": {"r": (40, 0, 0)}}),
        merge(base(0, 4), {"body": {"r": (10, 0, 0)}, "upper": {"r": (10, 0, 0)},
                           "cork": {"l": (0, 0.10, 0.16), "r": (250, 0, 60)}, "spray": {"s": (0.82, 0.82, 0.82)}}),
        merge(base(0, 4), {"body": {"r": (2, 0, 0)}, "cork": {"l": (0, 0.0, 0.01), "r": (0, 0, 10)},
                           "spray": {"s": 0.0}}),
    ]
    hit = [merge(base(0, 4), {"body": {"r": (-14, 0, 8), "s": (1.08, 1, 0.92)}, "upper": {"r": (-10, 0, 0)},
                              "eyes": {"s": (1, 0.4, 1)}, "cork": {"l": (0, 0, 0.02)}}),
           merge(base(0, 4), {"body": {"r": (-5, 0, 3)}, "eyes": {"s": (1, 0.7, 1)}})]
    plain = merge(base(0, 4), {"arm_l": {"s": 0.0}, "arm_r": {"s": 0.0}, "eyes": {"s": 0.0},
                               "leg_l": {"s": 0.3}, "leg_r": {"s": 0.3}, "body": {"l": (0, 0, -0.01), "r": (0, 6, 0)}})
    die = [merge(base(0, 4), {"body": {"r": (-12, 0, 0)}, "cork": {"l": (0, 0, 0.05)}, "eyes": {"s": 1.2}}),
           merge(base(0, 4), {"body": {"r": (0, 9, 0)}, "upper": {"r": (0, -10, 0)}, "eyes": {"s": (1, 0.5, 1)}}),
           merge(base(0, 4), {"body": {"r": (0, -7, 0)}, "arm_l": {"s": 0.5}, "arm_r": {"s": 0.5},
                              "eyes": {"s": (1, 0.3, 1)}}),
           lerp_pose(base(0, 4), plain, 0.8), plain, plain]
    arm.scale = (1.15, 1.15, 1.15)
    six(arm, idle, walk, windup, attack, hit, die)
    return arm


# =============================================================== Mộc Yêu
BRANCHES = [("br0", (0, 0, 0.44), (0, 0, 0.58), "trunk"),
            ("br_l", (0, 0, 0.58), (0.12, 0, 0.71), "br0"),
            ("br_r", (0, 0, 0.58), (-0.12, 0, 0.71), "br0"),
            ("br_ll", (0.12, 0, 0.71), (0.21, 0, 0.83), "br_l"),
            ("br_lr", (0.12, 0, 0.71), (0.06, 0, 0.87), "br_l"),
            ("br_rl", (-0.12, 0, 0.71), (-0.06, 0, 0.87), "br_r"),
            ("br_rr", (-0.12, 0, 0.71), (-0.21, 0, 0.83), "br_r")]
ROOTS = {"rt_l": (0.10, -0.06), "rt_r": (-0.10, -0.06), "rt_b": (0.0, 0.11)}


def build_moc_yeu():
    use_collection("COL_moc_yeu")
    set_root_offset((0, -0.02, 0))
    bark = material("MAT_my_bark", (0.51, 0.32, 0.18), (0.18, 0.16, 0.20), ramp=("wood", "hair"))
    bark_dk = material("MAT_my_bark_dark", (0.34, 0.20, 0.13), (0.11, 0.10, 0.13), ramp=("wood", "hair"))
    rings = material("MAT_my_rings", (0.93, 0.87, 0.70), (0.83, 0.75, 0.62), ramp=("paper", "bone"))
    twig = material("MAT_my_twig", (0.68, 0.48, 0.28), (0.27, 0.24, 0.30), ramp=("wood", "hair"))
    leaf = material("MAT_my_leaf", (0.37, 0.58, 0.20), (0.78, 0.33, 0.23), ramp=("leaf", "red"))
    blossom = material("MAT_my_blossom", (0.95, 0.72, 0.78), (0.90, 0.72, 0.23), ramp=("pink", "gold"))
    hole = material("MAT_my_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    eye = material("MAT_my_eye", (0.48, 0.92, 0.60), (1.0, 0.68, 0.23), emit=6.0, glow=("verdant", "flame"))

    bones = [("root", (0, 0, 0), (0, 0, 0.08), None),
             ("trunk", (0, 0, 0.12), (0, 0, 0.44), "root"),
             ("eyes", (0, -0.14, 0.30), (0, -0.14, 0.36), "trunk"),
             ("burst", (0, 0, 0.70), (0, 0, 0.80), "root")]
    bones += BRANCHES
    for name, (x, y) in ROOTS.items():
        bones.append((name + "1", (x * 0.6, y * 0.6, 0.15), (x * 1.15, y * 1.15, 0.07), "trunk"))
        bones.append((name + "2", (x * 1.15, y * 1.15, 0.07), (x, y, 0.0), name + "1"))
    arm = armature("moc_yeu", bones)

    att(arm, "trunk", cone("my_trunk", 0.155, 0.13, 0.32, (0, 0, 0.28), bark, seg=9),
        cone("my_top", 0.132, 0.132, 0.02, (0, 0, 0.445), rings, seg=9),
        cone("my_ring", 0.085, 0.085, 0.024, (0, 0, 0.446), bark_dk, seg=9),
        cone("my_core", 0.04, 0.04, 0.028, (0, 0, 0.447), rings, seg=8),
        *[box(f"my_ridge{k}", (0.025, 0.02, 0.24), (0.15 * math.sin(a), -0.15 * math.cos(a), 0.27), bark_dk,
              rot=(0, 0, math.degrees(a))) for k, a in enumerate((0.9, -0.9, 2.2, -2.3, 3.1))],
        ball("my_eyehl", (0.038, 0.014, 0.05), (0.055, -0.138, 0.33), hole, seg=10, rings=6),
        ball("my_eyehr", (0.038, 0.014, 0.05), (-0.055, -0.138, 0.33), hole, seg=10, rings=6),
        ball("my_mouth", (0.055, 0.014, 0.032), (0, -0.142, 0.215), hole, rot=(0, 8, 0), seg=10, rings=6),
        ball("my_knob", (0.035, 0.03, 0.03), (0.11, -0.10, 0.38), bark_dk, seg=8, rings=5),
        ball("my_moss", (0.07, 0.05, 0.03), (-0.12, -0.06, 0.40), leaf, rot=(0, -40, 0), seg=10, rings=5))
    att(arm, "eyes", ball("my_eyel", (0.02, 0.012, 0.024), (0.055, -0.148, 0.33), eye, seg=8, rings=5),
        ball("my_eyer", (0.02, 0.012, 0.024), (-0.055, -0.148, 0.33), eye, seg=8, rings=5))
    tips = {"br_ll": (0.21, 0, 0.83), "br_lr": (0.06, 0, 0.87), "br_rl": (-0.06, 0, 0.87), "br_rr": (-0.21, 0, 0.83)}
    for name, h, t, _ in BRANCHES:
        r1 = 0.035 if name == "br0" else (0.026 if len(name) == 4 else 0.018)
        parts = [aim(f"my_{name}", twig, h, t, r1, r1 * 0.75, seg=6)]
        if name in tips:
            x, y, z = tips[name]
            parts.append(ball(f"my_leaves_{name}", (0.075, 0.065, 0.06), (x, y, z + 0.02), leaf, seg=10, rings=6))
            parts.append(ball(f"my_leaves2_{name}", (0.05, 0.05, 0.045), (x * 0.8, y - 0.03, z - 0.04), leaf, seg=8, rings=5))
            if name in ("br_ll", "br_rl"):
                parts.append(ball(f"my_blossom_{name}", (0.03,) * 3, (x, y - 0.06, z + 0.03), blossom, seg=8, rings=5))
        att(arm, name, *parts)
    for name in ROOTS:
        b1 = arm.data.bones[name + "1"]
        b2 = arm.data.bones[name + "2"]
        att(arm, name + "1", aim(f"my_{name}1", bark, tuple(b1.head_local), tuple(b1.tail_local), 0.045, 0.035, seg=7))
        att(arm, name + "2", aim(f"my_{name}2", bark_dk, tuple(b2.head_local), tuple(b2.tail_local), 0.035, 0.018, seg=7))
    # a burst of leaves thrown up by the slam (scaled away except on the impact frames)
    leafs = []
    for k in range(7):
        a = TAU * k / 7 + 0.3
        leafs.append(ball(f"my_flying{k}", (0.035, 0.012, 0.025),
                          (0.26 * math.cos(a), 0.18 * math.sin(a), 0.62 + 0.12 * math.sin(3 * a)), leaf,
                          rot=(0, math.degrees(a), 30), seg=8, rings=4))
    att(arm, "burst", *leafs)

    def sway(i, n, amp=1.0):
        return {"br0": {"r": (0, 4 * amp * S(i, n), 0)},
                "br_l": {"r": (0, 5 * amp * S(i, n, -0.6), 0)}, "br_r": {"r": (0, 5 * amp * S(i, n, -0.6), 0)},
                "br_ll": {"r": (0, 7 * amp * S(i, n, -1.2), 0)}, "br_lr": {"r": (0, 6 * amp * S(i, n, -1.2), 0)},
                "br_rl": {"r": (0, 6 * amp * S(i, n, -1.2), 0)}, "br_rr": {"r": (0, 7 * amp * S(i, n, -1.2), 0)},
                "burst": {"s": 0.0}}
    idle = [merge(sway(i, 4), {"trunk": {"l": (0, 0, 0.004 * S(i, 4))}}) for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        p = sway(i, 6, 1.6)
        p["trunk"] = {"r": (4, 8 * s, 0), "l": (0, 0, 0.012 * abs(s))}
        for name, ph in (("rt_l", 0.0), ("rt_r", math.pi), ("rt_b", math.pi / 2)):
            lift = max(0.0, S(i, 6, ph))
            p[name + "1"] = {"l": (0, 0, 0.03 * lift - 0.012 * abs(s)), "r": (-12 * lift, 0, 0)}
        walk.append(p)
    # windup: rises up on its roots, crown flung wide and high, leaning back
    rise = merge(sway(0, 4), {
        "trunk": {"l": (0, 0.02, 0.05), "r": (-10, 0, 0)},
        "br0": {"r": (-8, 0, 0), "s": 1.1}, "br_l": {"r": (0, 22, 0)}, "br_r": {"r": (0, -22, 0)},
        "br_ll": {"r": (0, 18, 0)}, "br_rr": {"r": (0, -18, 0)},
        "rt_l1": {"l": (0, 0, -0.05)}, "rt_r1": {"l": (0, 0, -0.05)}, "rt_b1": {"l": (0, 0, -0.05)},
        "rt_l2": {"r": (-14, 0, 0)}, "rt_r2": {"r": (-14, 0, 0)}, "rt_b2": {"r": (14, 0, 0)}})
    windup = [lerp_pose(idle[0], rise, 0.5), rise, merge(rise, {"br_ll": {"r": (0, 22, 0)}}),
              merge(rise, {"br_rr": {"r": (0, -22, 0)}})]
    # attack: slams down, roots stab into the earth, the crown whips forward and leaves fly
    slam = merge(sway(0, 4), {
        "trunk": {"l": (0, 0, -0.035), "r": (8, 0, 0)},
        "br0": {"r": (22, 0, 0)}, "br_l": {"r": (12, -6, 0)}, "br_r": {"r": (12, 6, 0)},
        "rt_l1": {"l": (0, 0, 0.035)}, "rt_r1": {"l": (0, 0, 0.035)}, "rt_b1": {"l": (0, 0, 0.035)},
        "burst": {"s": 1.0}})
    attack = [merge(slam, {"trunk": {"l": (0, 0, -0.01)}, "burst": {"s": 0.5}}), slam,
              merge(slam, {"burst": {"s": 1.25, "l": (0, 0, 0.05)}, "br0": {"r": (12, 0, 0)}}),
              merge(sway(0, 4), {"trunk": {"r": (2, 0, 0)}})]
    hit = [merge(sway(1, 4, 2.5), {"trunk": {"r": (-12, 0, 6)}, "eyes": {"s": (1, 0.4, 1)}}),
           merge(sway(2, 4, 1.5), {"trunk": {"r": (-4, 0, 2)}})]
    wilt = {"trunk": {"r": (0, 8, 0), "l": (0, 0, -0.02)}, "eyes": {"s": 0.0},
            "br0": {"r": (24, 10, 0)}, "br_l": {"r": (30, 0, 0)}, "br_r": {"r": (30, 0, 0)},
            "br_ll": {"r": (40, 0, 0), "s": 0.7}, "br_lr": {"r": (30, 0, 0), "s": 0.6},
            "br_rl": {"r": (30, 0, 0), "s": 0.6}, "br_rr": {"r": (40, 0, 0), "s": 0.7},
            "burst": {"s": 0.0}, "rt_l1": {"l": (0, 0, 0.02)}, "rt_r1": {"l": (0, 0, 0.02)}, "rt_b1": {"l": (0, 0, 0.02)}}
    die = [merge(sway(1, 4, 3), {"trunk": {"r": (-10, 0, 0)}}),
           merge(sway(3, 4, 3), {"burst": {"s": 0.8, "l": (0, 0, -0.1)}, "eyes": {"s": (1, 0.5, 1)}}),
           merge(lerp_pose(sway(0, 4), wilt, 0.5), {"burst": {"s": 0.7, "l": (0, 0, -0.3)}}),
           wilt, wilt, wilt]
    six(arm, idle, walk, windup, attack, hit, die)
    return arm


# =============================================================== Cơ Quan Nhân
def gear(name, center, r, mat, teeth=8, thick=0.022, tooth=0.024):
    """A gear seen from the front: a disc with square teeth, axis along y."""
    parts = [cone(name, r, r, thick, center, mat, rot=(90, 0, 0), seg=16)]
    cx, cy, cz = center
    for k in range(teeth):
        a = TAU * k / teeth
        parts.append(box(f"{name}_t{k}", (tooth, thick, tooth),
                         (cx + (r + tooth * 0.35) * math.cos(a), cy, cz + (r + tooth * 0.35) * math.sin(a)), mat,
                         rot=(0, -math.degrees(a), 0)))
    return parts


def ring(name, center, r, thick, mat, axis="z", n=20):
    """A torus-like hoop made of a closed tube."""
    cx, cy, cz = center
    pts = []
    for k in range(n + 1):
        a = TAU * k / n
        if axis == "z":
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a), cz))
        else:                       # hoop facing the camera (axis y)
            pts.append((cx + r * math.cos(a), cy, cz + r * math.sin(a)))
    return tube(name, pts, [thick] * (n + 1), mat, seg=6, up=(0, 0, 1) if axis == "z" else (0, 1, 0))


def build_co_quan_nhan():
    use_collection("COL_co_quan_nhan")
    wood = material("MAT_cq_wood", (0.51, 0.32, 0.18), (0.36, 0.43, 0.53), ramp=("wood", "steel"))
    wood_lt = material("MAT_cq_wood_light", (0.68, 0.48, 0.28), (0.58, 0.65, 0.73), ramp=("wood", "steel"))
    wood_dk = material("MAT_cq_wood_dark", (0.34, 0.20, 0.13), (0.20, 0.25, 0.35), ramp=("wood", "steel"))
    bronze = material("MAT_cq_bronze", (0.73, 0.51, 0.10), (0.58, 0.19, 0.16), ramp=("gold", "red"), metal=True)
    bronze_dk = material("MAT_cq_bronze_dark", (0.48, 0.30, 0.05), (0.36, 0.10, 0.11), ramp=("gold", "red"), metal=True)
    cog = material("MAT_cq_gear", (0.90, 0.72, 0.23), (0.78, 0.33, 0.23), ramp=("gold", "red"), metal=True)
    cog["kit_priority"] = 3.0
    eye = material("MAT_cq_eye", (1.0, 0.68, 0.23), (0.78, 0.55, 1.0), emit=6.0, glow=("flame", "cosmic"))
    core = material("MAT_cq_core", (1.0, 0.89, 0.48), (0.78, 0.55, 1.0), emit=3.0, glow=("holy", "cosmic"))
    dark = material("MAT_cq_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")

    LX, AX = 0.06, 0.19
    arm = armature("co_quan_nhan", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("hips", (0, 0, 0.28), (0, 0, 0.36), "root"),
        ("chest", (0, 0, 0.36), (0, 0, 0.62), "hips"),
        ("head", (0, 0, 0.63), (0, 0, 0.88), "chest"),
        ("eyes", (0, -0.11, 0.72), (0, -0.11, 0.78), "head"),
        ("key", (0, 0.15, 0.50), (0, 0.30, 0.50), "chest"),
        ("gear1", (0, -0.04, 0.50), (0, -0.14, 0.50), "chest"),
        ("gear2", (0.075, -0.02, 0.42), (0.075, -0.12, 0.42), "chest"),
        ("arm_l", (AX, 0, 0.57), (AX, 0, 0.44), "chest"),
        ("fore_l", (AX, 0, 0.44), (AX, 0, 0.30), "arm_l"),
        ("arm_r", (-AX, 0, 0.57), (-AX, 0, 0.44), "chest"),
        ("fore_r", (-AX, 0, 0.44), (-AX, 0, 0.30), "arm_r"),
        ("leg_l", (LX, 0, 0.28), (LX, 0, 0.15), "hips"),
        ("shin_l", (LX, 0, 0.15), (LX, 0, 0.02), "leg_l"),
        ("leg_r", (-LX, 0, 0.28), (-LX, 0, 0.15), "hips"),
        ("shin_r", (-LX, 0, 0.15), (-LX, 0, 0.02), "leg_r"),
    ])
    att(arm, "hips", box("cq_pelvis", (0.22, 0.15, 0.09), (0, 0, 0.31), wood, bevel=0.015),
        ball("cq_hipl", (0.045,) * 3, (LX, 0, 0.28), bronze, seg=8, rings=5),
        ball("cq_hipr", (0.045,) * 3, (-LX, 0, 0.28), bronze, seg=8, rings=5))
    # a barrel chest of staves with an open window in front; inside, one big gear
    staves = []
    for k in range(16):
        a = TAU * k / 16
        front = abs(math.atan2(math.cos(a), -math.sin(a)))       # 0 = facing the camera
        if front < math.radians(42):
            continue
        staves.append(box(f"cq_stave{k}", (0.064, 0.028, 0.25), (0.155 * math.cos(a), 0.155 * math.sin(a), 0.50),
                          wood if k % 2 else wood_lt, rot=(0, 0, math.degrees(a) + 90)))
    att(arm, "chest", *staves,
        cone("cq_inside", 0.14, 0.14, 0.24, (0, 0.0, 0.50), dark, seg=14),
        ring("cq_hoop_top", (0, 0, 0.615), 0.165, 0.018, bronze),
        ring("cq_hoop_bot", (0, 0, 0.385), 0.165, 0.018, bronze),
        ball("cq_core", (0.06, 0.02, 0.06), (0, 0.02, 0.50), core, seg=10, rings=6),
        ball("cq_shl", (0.055,) * 3, (AX, 0, 0.58), bronze, seg=10, rings=6),
        ball("cq_shr", (0.055,) * 3, (-AX, 0, 0.58), bronze, seg=10, rings=6))
    att(arm, "gear1", *gear("cq_gear1", (0, -0.075, 0.50), 0.075, cog, teeth=8, thick=0.03, tooth=0.042),
        ball("cq_axle", (0.025, 0.02, 0.025), (0, -0.095, 0.50), bronze_dk, seg=8, rings=5))
    att(arm, "gear2", *gear("cq_gear2", (0.075, -0.05, 0.42), 0.038, bronze_dk, teeth=6, thick=0.024, tooth=0.028))
    # a big wind-up key in the back, reads from the side and from behind
    att(arm, "key", aim("cq_keyshaft", bronze, (0, 0.14, 0.50), (0, 0.30, 0.50), 0.024, 0.024, seg=6),
        ball("cq_keybl", (0.08, 0.022, 0.065), (0.065, 0.31, 0.50), bronze, seg=12, rings=6),
        ball("cq_keybr", (0.08, 0.022, 0.065), (-0.065, 0.31, 0.50), bronze, seg=12, rings=6),
        ball("cq_keyhub", (0.03,) * 3, (0, 0.31, 0.50), bronze_dk, seg=8, rings=5))
    att(arm, "head", box("cq_head", (0.26, 0.22, 0.22), (0, -0.005, 0.745), wood_lt, bevel=0.045),
        box("cq_brow", (0.26, 0.05, 0.035), (0, -0.11, 0.815), wood_dk, bevel=0.01),
        ring("cq_riml", (0.062, -0.115, 0.745), 0.046, 0.013, bronze, axis="y", n=16),
        ring("cq_rimr", (-0.062, -0.115, 0.745), 0.046, 0.013, bronze, axis="y", n=16),
        box("cq_mouth", (0.10, 0.015, 0.018), (0, -0.115, 0.67), dark),
        box("cq_hinge", (0.15, 0.03, 0.022), (0, -0.105, 0.65), bronze_dk),
        cone("cq_cap", 0.07, 0.035, 0.05, (0, 0, 0.875), bronze, seg=10),
        ball("cq_knob", (0.03,) * 3, (0, 0, 0.91), bronze_dk, seg=8, rings=5),
        cone("cq_earl", 0.05, 0.05, 0.025, (0.135, 0, 0.745), bronze, rot=(0, 90, 0), seg=12),
        cone("cq_earr", 0.05, 0.05, 0.025, (-0.135, 0, 0.745), bronze, rot=(0, 90, 0), seg=12))
    att(arm, "eyes", ball("cq_eyel", (0.04, 0.02, 0.04), (0.062, -0.112, 0.745), eye, seg=12, rings=6),
        ball("cq_eyer", (0.04, 0.02, 0.04), (-0.062, -0.112, 0.745), eye, seg=12, rings=6))
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"arm_{side}", box(f"cq_up{side}", (0.085, 0.085, 0.12), (s * AX, 0, 0.50), wood, bevel=0.012),
            ball(f"cq_elb{side}", (0.05,) * 3, (s * AX, 0, 0.44), bronze, seg=10, rings=6))
        att(arm, f"fore_{side}", box(f"cq_fore{side}", (0.08, 0.08, 0.11), (s * AX, 0, 0.375), wood_lt, bevel=0.012),
            box(f"cq_hand{side}", (0.09, 0.09, 0.07), (s * AX, -0.005, 0.295), bronze, bevel=0.015))
        att(arm, f"leg_{side}", box(f"cq_thigh{side}", (0.085, 0.085, 0.11), (s * LX, 0, 0.215), wood, bevel=0.012),
            ball(f"cq_knee{side}", (0.048,) * 3, (s * LX, 0, 0.15), bronze, seg=10, rings=6))
        att(arm, f"shin_{side}", box(f"cq_shin{side}", (0.08, 0.08, 0.10), (s * LX, 0, 0.09), wood_lt, bevel=0.012),
            box(f"cq_foot{side}", (0.09, 0.13, 0.04), (s * LX, -0.02, 0.02), wood_dk, bevel=0.008))

    def works(i, n=4):
        """Gears turn and the key winds every frame, whatever the body does."""
        return {"gear1": {"r": (0, 45 * i * 4 / n, 0)}, "gear2": {"r": (0, -60 * i * 4 / n, 0)},
                "key": {"r": (0, 45 * i * 4 / n, 0)}}
    idle = [merge(works(i), {"chest": {"l": (0, 0, 0.004 * S(i, 4))},
                             "head": {"r": (0, 0, 6 if i == 1 else (-6 if i == 3 else 0))},
                             "arm_l": {"r": (0, -4, 0)}, "arm_r": {"r": (0, 4, 0)}}) for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append(merge(works(i, 6), {
            "hips": {"l": (0, 0, 0.01 * abs(s))},
            "chest": {"r": (0, 0, 6 * s)}, "head": {"r": (0, 0, -6 * s)},
            "leg_l": {"r": (-24 * s, 0, 0), "l": (0, 0, -0.01 * abs(s))},
            "leg_r": {"r": (24 * s, 0, 0), "l": (0, 0, -0.01 * abs(s))},
            "shin_l": {"r": (20 * max(0.0, s), 0, 0)}, "shin_r": {"r": (20 * max(0.0, -s), 0, 0)},
            "arm_l": {"r": (26 * s, -4, 0)}, "arm_r": {"r": (-26 * s, 4, 0)},
            "fore_l": {"r": (-14, 0, 0)}, "fore_r": {"r": (-14, 0, 0)}}))
    # windup: arms flung straight out like a spinning top, torso twisted far back
    tpose = merge(works(2), {
        "hips": {"l": (0, 0, -0.02)}, "chest": {"r": (0, 0, 55)}, "head": {"r": (0, 0, -40)},
        "arm_l": {"r": (0, -88, 0)}, "arm_r": {"r": (0, 88, 0)},
        "fore_l": {"r": (0, -6, 0)}, "fore_r": {"r": (0, 6, 0)},
        "leg_l": {"r": (-10, 0, 0), "l": (0, 0, 0.02)}, "leg_r": {"r": (10, 0, 0), "l": (0, 0, 0.02)}})
    windup = [lerp_pose(idle[0], tpose, 0.5), tpose, merge(tpose, works(3)), merge(tpose, works(4))]
    # attack: a full spin, arms out; the hit lands as the right arm sweeps across the front
    attack = []
    for k, (rz, lean) in enumerate(((-20, 6), (-110, 10), (-210, 6), (-330, 2))):
        attack.append(merge(works(k), {
            "hips": {"l": (0, 0, -0.02)}, "chest": {"r": (lean, 0, rz)}, "head": {"r": (0, 0, -rz * 0.15)},
            "arm_l": {"r": (0, -86, 0)}, "arm_r": {"r": (0, 86, 0)},
            "leg_l": {"l": (0, 0, 0.02)}, "leg_r": {"l": (0, 0, 0.02)}}))
    hit = [merge(works(0), {"chest": {"r": (-14, 0, 8)}, "head": {"r": (-14, 0, 14)},
                            "arm_l": {"r": (20, -20, 0)}, "arm_r": {"r": (20, 20, 0)}, "eyes": {"s": (1, 0.4, 1)}}),
           merge(works(0), {"chest": {"r": (-5, 0, 3)}, "head": {"r": (-4, 0, 6)}})]
    slump = {"hips": {"l": (0, 0.02, -0.12)}, "chest": {"r": (24, 0, 6)}, "head": {"r": (30, 0, 20)},
             "leg_l": {"r": (-70, 0, 0), "l": (0, 0, 0.12)}, "leg_r": {"r": (-62, 0, 0), "l": (0, 0, 0.12)},
             "shin_l": {"r": (80, 0, 0)}, "shin_r": {"r": (72, 0, 0)},
             "arm_l": {"r": (10, -10, 0)}, "arm_r": {"r": (14, 14, 0)},
             "eyes": {"s": 0.0}, "gear1": {"l": (0.03, -0.02, -0.04), "r": (0, 30, 0)},
             "key": {"r": (0, 20, 0)}}
    die = [merge(works(0), {"chest": {"r": (-10, 0, 10)}, "head": {"r": (-20, 0, 0)}, "eyes": {"s": 1.2}}),
           merge(works(1), {"chest": {"r": (6, 0, -8)}, "head": {"r": (10, 0, 30)}, "eyes": {"s": (1, 0.5, 1)}}),
           lerp_pose(works(1), slump, 0.6), slump, slump, slump]
    arm.scale = (1.15, 1.15, 1.15)     # a chunky puppet filling its frame
    six(arm, idle, walk, windup, attack, hit, die)
    return arm
