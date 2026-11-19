"""The six MONSTERS_A creatures: model, rig and six clips each (runs inside Blender).

Each `build_<id>()` makes the meshes, the armature `ARM_<id>`, parents/skins the parts and
writes the actions idle / walk / windup / attack / hit / die. Units are metres, the
creature faces -y, origin on the ground. Numbers only: rerunning gives the same .blend.

Pose tables use rig.set_pose conventions: r = (deg about x, y, z) in armature axes, applied
in the parent's posed frame; +x rotation tips the top of an upright bone FORWARD (-y) and
swings the tip of a hanging bone BACKWARD (+y); +y rotation moves the tip of an upright
bone toward +x; l = offset in armature axes; s = scale.
"""
from __future__ import annotations

import math

from rig import (aim, armature, attach, ball, box, clip, cone, ground_holdout, lerp_pose,
                 material, merge, place, prism, set_root_offset, shadow, skin, tube,
                 use_collection)

TAU = 2 * math.pi
FPS = {"idle": 6, "walk": 10, "windup": 8, "attack": 14, "hit": 12, "die": 10}


def S(i, n, phase=0.0):
    return math.sin(TAU * i / n + phase)


def C(i, n, phase=0.0):
    return math.cos(TAU * i / n + phase)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


# =============================================================== Kiếm Linh
def build_kiem_linh():
    use_collection("COL_kiem_linh")
    ghost = material("MAT_kl_ghost", (0.81, 0.80, 0.83), (0.52, 0.34, 0.75), ramp=("bone", "purple"))
    ghost_dk = material("MAT_kl_ghost_wisp", (0.39, 0.53, 0.77), (0.36, 0.21, 0.56), ramp=("blue", "purple"))
    steel = material("MAT_kl_blade", (0.58, 0.65, 0.73), (0.27, 0.24, 0.30), ramp=("steel", "hair"), metal=True)
    bronze = material("MAT_kl_guard", (0.73, 0.51, 0.10), (0.73, 0.51, 0.10), ramp="gold", metal=True)
    wrap = material("MAT_kl_grip", (0.34, 0.20, 0.13), (0.18, 0.16, 0.20), ramp=("wood", "hair"))
    tassel = material("MAT_kl_tassel", (0.58, 0.19, 0.16), (0.90, 0.72, 0.23), ramp=("red", "gold"))
    eye = material("MAT_kl_eye", (0.35, 0.88, 0.96), (1.0, 0.68, 0.23), emit=5.0, glow=("spirit", "flame"))
    rune = material("MAT_kl_rune", (0.35, 0.88, 0.96), (1.0, 0.68, 0.23), emit=4.0, glow=("spirit", "flame"))
    mouth = material("MAT_kl_mouth", (0.14, 0.23, 0.42), (0.23, 0.13, 0.38), ramp=("blue", "purple"))

    arm = armature("kiem_linh", [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("body", (0, 0, 0.72), (0, 0, 0.85), "root"),
        ("ghost", (0, 0, 0.78), (0, 0, 0.95), "body"),
        ("tail1", (0, 0.06, 0.86), (0, 0.15, 0.80), "ghost"),
        ("tail2", (0, 0.15, 0.80), (0, 0.26, 0.76), "tail1"),
        ("arm_l", (0.09, -0.03, 0.85), (0.15, -0.04, 0.76), "ghost"),
        ("arm_r", (-0.09, -0.03, 0.85), (-0.15, -0.04, 0.76), "ghost"),
        ("sword", (0, 0, 0.72), (0, 0, 0.85), "body"),
        ("tassel", (0.17, 0, 0.73), (0.19, 0.02, 0.62), "sword"),
    ])

    # --- the sword is the creature: a big chipped blade, point down, guard at the
    # spirit's chin; two chips bitten out of the edges
    blade = prism("kl_blade", [
        (0.0, 0.03), (0.075, 0.15), (0.075, 0.30), (0.045, 0.335), (0.068, 0.37),
        (0.075, 0.37), (0.075, 0.70), (-0.075, 0.70), (-0.075, 0.53), (-0.045, 0.50),
        (-0.075, 0.47), (-0.075, 0.15)], 0.03, steel)
    ridge = prism("kl_ridge", [(0.0, 0.06), (0.018, 0.15), (0.018, 0.69), (-0.018, 0.69),
                               (-0.018, 0.15)], 0.04, steel)
    runes = []
    for k, z in enumerate((0.24, 0.40, 0.56)):          # abstract dashes down the fuller
        for y in (-0.021, 0.021):
            runes.append(box(f"kl_rune{k}{y > 0}", (0.02, 0.004, 0.065), (0, y, z), rune))
    for side in (-1, 1):                                # the arrow chevron near the tip
        for y in (-0.021, 0.021):
            runes.append(box(f"kl_chev{side}{y > 0}", (0.018, 0.004, 0.075),
                             (side * 0.022, y, 0.12), rune, rot=(0, side * 40, 0)))
    guard = box("kl_guard", (0.34, 0.07, 0.06), (0, 0, 0.73), bronze, bevel=0.014)
    gtips = [cone(f"kl_guardtip{s}", 0.04, 0.0, 0.10, (s * 0.20, 0, 0.765), bronze,
                  rot=(0, s * 35, 0), seg=6) for s in (-1, 1)]
    gem = box("kl_gem", (0.045, 0.08, 0.045), (0, 0, 0.73), rune)
    grip = box("kl_grip", (0.045, 0.045, 0.15), (0, 0, 0.83), wrap)
    pommel = ball("kl_pommel", (0.04, 0.04, 0.04), (0, 0, 0.92), bronze, seg=10, rings=6)
    att(arm, "sword", blade, ridge, guard, gem, grip, pommel, *gtips, *runes)
    tas = aim("kl_tassel", tassel, (0.17, 0, 0.72), (0.19, 0.02, 0.61), 0.014, 0.036, seg=6)
    att(arm, "tassel", tas)
    shade = material("MAT_kl_shadow", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    shadow("kl_shadow", 0.10, 0.08, shade, arm)
    ground_holdout()

    # --- the spirit: a small round wisp wrapped round the hilt, its two eyes just above
    # the guard, a flame tip curling up, ribbons spiralling down round the blade, and a
    # wispy tail streaming back
    zs = [0.98, 0.965, 0.93, 0.885, 0.84, 0.80, 0.77, 0.75]
    ys = [0.0, 0.0, 0.0, 0.0, 0.0, 0.005, 0.01, 0.02]
    rs = [0.02, 0.07, 0.105, 0.12, 0.118, 0.105, 0.085, 0.06]

    def hem(i, a):
        return 1.0 + (0.18 * math.sin(4 * a + i * 0.9) if i >= 5 else 0.0)
    body = tube("kl_ghost", [(0, y, z) for y, z in zip(ys, zs)], rs, ghost, seg=16,
                up=(0, -1, 0), wobble=hem)
    skin(body, arm, ["ghost", "tail1"], power=3)
    helix = []
    for k in range(15):
        u = k / 14
        ang = 0.6 + u * 3.4 * math.pi
        rr = 0.085 - 0.02 * u
        helix.append((rr * math.cos(ang), rr * math.sin(ang), 0.78 - 0.34 * u))
    ribbon = tube("kl_ribbon", helix, [0.024 - 0.016 * k / 14 for k in range(15)], ghost_dk,
                  seg=8, up=(0, 0, 1))
    tail = tube("kl_tail", [(0, 0.04, 0.88), (0, 0.11, 0.84), (0, 0.18, 0.80),
                            (0, 0.25, 0.775), (0, 0.30, 0.765)],
                [0.07, 0.058, 0.042, 0.026, 0.01], ghost_dk, seg=12, up=(0, 0, 1))
    skin(tail, arm, ["ghost", "tail1", "tail2"], power=3)
    att(arm, "ghost", ribbon)
    eyes = [ball(f"kl_eye{s}", (0.032, 0.016, 0.042), (s * 0.05, -0.112, 0.865), eye,
                 seg=10, rings=6) for s in (-1, 1)]
    eyes.append(aim("kl_flame", ghost, (0, 0.0, 0.95), (0, 0.07, 1.06), 0.05, 0.0, seg=10,
                    smooth=True))
    mth = ball("kl_mouth", (0.018, 0.01, 0.012), (0, -0.117, 0.82), mouth, seg=8, rings=5)
    att(arm, "ghost", *eyes, mth)
    for s, b in ((1, "arm_l"), (-1, "arm_r")):
        a = aim(f"kl_arm{s}", ghost, (s * 0.09, -0.03, 0.85), (s * 0.15, -0.04, 0.76),
                0.04, 0.018, seg=10, smooth=True)
        att(arm, b, a)

    # --- clips (the tail bones point backward: +x rotation lifts the tail, z sways it)
    def base(i=0, n=4, bob=0.03, lean=0.0):
        return {
            "body": {"l": (0, 0, bob * (0.5 + 0.5 * S(i, n))), "r": (lean, 0, 0)},
            "tail1": {"r": (6 * C(i, n), 0, 14 * S(i, n))},
            "tail2": {"r": (10 * C(i, n, -1.2), 0, 18 * S(i, n, -1.2))},
            "arm_l": {"r": (0, -12 * S(i, n, 0.6), 0)},
            "arm_r": {"r": (0, 12 * S(i, n, 0.6), 0)},
            "tassel": {"r": (8 * C(i, n, -1.0), 6 * S(i, n, -1.5), 0)},
            "sword": {"r": (0, 3 * S(i, n), 0)},
        }
    idle = [base(i) for i in range(4)]
    walk = []
    for i in range(6):
        p = base(i, 6, bob=0.04, lean=12)
        p["tail1"]["r"] = (-6 + 6 * C(i, 6), 0, 16 * S(i, 6))
        p["tail2"]["r"] = (-4 + 8 * C(i, 6, -1.4), 0, 20 * S(i, 6, -1.4))
        p["arm_l"]["r"] = (30, -10 * S(i, 6), 0)
        p["arm_r"]["r"] = (30, 10 * S(i, 6), 0)
        p["tassel"]["r"] = (35, 8 * S(i, 6, -1.5), 0)
        walk.append(p)
    # windup: leans back, the blade swings up to point straight at the target, the tail
    # curls up behind like a drawn bowstring
    coil = {
        "body": {"l": (0, 0.10, -0.02), "r": (-12, 0, 0)},
        "sword": {"l": (0, 0.04, 0.0), "r": (-46, 34, 0)},
        "ghost": {"s": (1.08, 1.04, 1.08), "r": (10, 0, 0)},
        "tail1": {"r": (40, 0, 0)}, "tail2": {"r": (45, 0, 0)},
        "arm_l": {"r": (-50, 25, 0)}, "arm_r": {"r": (-50, -25, 0)},
        "tassel": {"r": (60, 0, 0)},
    }
    windup = [
        lerp_pose(base(0), coil, 0.45),
        coil,
        merge(coil, {"body": {"l": (0.008, 0.11, -0.015)}, "tassel": {"r": (55, 8, 0)},
                     "tail2": {"r": (50, 0, 6)}}),
        merge(coil, {"body": {"l": (-0.008, 0.11, -0.02)}, "tassel": {"r": (62, -8, 0)},
                     "tail2": {"r": (50, 0, -6)}}),
    ]
    attack = [
        {"root": {"l": (0, 0.0, 0)}, "body": {"r": (6, 0, 0), "l": (0, 0.18, -0.10)},
         "sword": {"r": (-88, 14, 0), "l": (0, 0.0, 0)}, "ghost": {"s": (0.92, 0.95, 1.2), "r": (-6, 0, 0)},
         "tail1": {"r": (-8, 0, 0)}, "tail2": {"r": (-6, 0, 0)},
         "arm_l": {"r": (-60, 0, 0)}, "arm_r": {"r": (-60, 0, 0)}, "tassel": {"r": (80, 0, 0)}},
        {"root": {"l": (0, 0.0, 0)}, "body": {"r": (8, 0, 0), "l": (0, 0.15, -0.12)},
         "sword": {"r": (-92, 20, 0), "l": (0, 0.0, 0)}, "ghost": {"s": (0.9, 0.95, 1.25), "r": (-10, 0, 0)},
         "tail1": {"r": (-12, 0, 6)}, "tail2": {"r": (-10, 0, -8)},
         "arm_l": {"r": (-70, -10, 0)}, "arm_r": {"r": (-70, 10, 0)}, "tassel": {"r": (95, 0, 0)}},
        {"root": {"l": (0, 0.0, 0)}, "body": {"r": (4, 0, 0), "l": (0, 0.07, -0.01)},
         "sword": {"r": (-58, 0, 0), "l": (0, 0.0, 0)},
         "tail1": {"r": (14, 0, -10)}, "tail2": {"r": (24, 0, -6)},
         "arm_l": {"r": (-20, 0, 0)}, "arm_r": {"r": (-20, 0, 0)}, "tassel": {"r": (40, 10, 0)}},
        {"root": {"l": (0, 0.0, 0)}, "body": {"l": (0, 0.02, 0.0)},
         "sword": {"r": (-16, 0, 0)},
         "tail1": {"r": (8, 0, 8)}, "tail2": {"r": (-12, 0, 10)},
         "tassel": {"r": (-20, 0, 0)}},
    ]
    hit = [
        {"body": {"r": (-26, 8, 0), "l": (0, 0.08, 0.03)}, "ghost": {"s": (1.12, 0.88, 1.1)},
         "sword": {"r": (0, 10, 0)}, "tail1": {"r": (30, 0, 0)}, "tail2": {"r": (25, 0, 0)},
         "arm_l": {"r": (0, -40, 0)}, "arm_r": {"r": (0, 40, 0)}, "tassel": {"r": (-40, 0, 0)}},
        {"body": {"r": (-10, 3, 0), "l": (0, 0.04, 0.02)}, "ghost": {"s": 1.03},
         "sword": {"r": (0, 4, 0)}, "tail1": {"r": (-10, 0, 0)}, "tail2": {"r": (-12, 0, 0)},
         "arm_l": {"r": (0, -15, 0)}, "arm_r": {"r": (0, 15, 0)}, "tassel": {"r": (30, 0, 0)}},
    ]
    die = [
        {"body": {"r": (-22, 10, 0), "l": (0, 0.06, 0.05)}, "ghost": {"s": 1.12},
         "tail1": {"r": (30, 0, 0)}, "arm_l": {"r": (0, -50, 0)}, "arm_r": {"r": (0, 50, 0)}},
        {"body": {"r": (-10, 22, 0), "l": (0, 0.04, 0.04)}, "ghost": {"s": 1.15},
         "tail1": {"r": (45, 0, 0)}, "arm_l": {"r": (0, -70, 0)}, "arm_r": {"r": (0, 70, 0)},
         "tassel": {"r": (0, -30, 0)}},
        # the spirit thins out; the empty sword drops point first and drives into the
        # ground, left standing at a tilt like a grave marker (the holdout ground cuts it)
        {"body": {"r": (0, 8, 0), "l": (0, 0.02, 0.04)}, "ghost": {"s": 0.6},
         "tassel": {"r": (20, -10, 0)}},
        {"body": {"r": (0, 5, 0), "l": (0, 0, -0.22)}, "ghost": {"s": 0.25},
         "tassel": {"r": (-25, 0, 0)}},
        {"body": {"r": (0, 16, 0), "l": (0, 0, -0.31)}, "ghost": {"s": 0.05},
         "tassel": {"r": (10, -20, 0)}},
        {"body": {"r": (0, 13, 0), "l": (0, 0, -0.29)}, "ghost": {"s": 0.0},
         "tassel": {"r": (0, -12, 0)}},
    ]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
    return arm


def plant_feet(pose, legs=("leg_l", "leg_r")):
    """The golem's legs hang from its hips: when the hips sink or shift, move the legs
    the other way so the feet stay where they are on the ground (they slide up into the
    hip block, which reads as bent knees on a block body)."""
    h = pose.get("hips", {}).get("l")
    if not h:
        return pose
    for leg in legs:
        spec = pose.setdefault(leg, {})
        x, y, z = spec.get("l", (0, 0, 0))
        spec["l"] = (x - h[0], y - h[1], z - h[2])
    return pose


def write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame):
    clip(arm, "idle", idle, FPS["idle"], True)
    clip(arm, "walk", walk, FPS["walk"], True)
    clip(arm, "windup", windup, FPS["windup"], False)
    clip(arm, "attack", attack, FPS["attack"], False, hit=hit_frame)
    clip(arm, "hit", hit, FPS["hit"], False)
    clip(arm, "die", die, FPS["die"], False)
    arm.animation_data.action = None


# =============================================================== Thạch Khôi
def build_thach_khoi():
    use_collection("COL_thach_khoi")
    stone_a = material("MAT_tk_stone_a", (0.53, 0.56, 0.60), (0.27, 0.24, 0.30), ramp=("stone", "hair"))
    stone_b = material("MAT_tk_stone_b", (0.42, 0.35, 0.28), (0.18, 0.16, 0.20), ramp=("earth", "hair"))
    moss = material("MAT_tk_moss", (0.37, 0.58, 0.20), (0.58, 0.19, 0.16), ramp=("leaf", "red"))
    core = material("MAT_tk_core", (0.35, 0.88, 0.96), (1.0, 0.68, 0.23), emit=5.0, glow=("spirit", "flame"))
    eye = material("MAT_tk_eye", (0.35, 0.88, 0.96), (1.0, 0.68, 0.23), emit=5.0, glow=("spirit", "flame"))

    arm = armature("thach_khoi", [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hips", (0, 0, 0.2), (0, 0, 0.3), "root"),
        ("chest", (0, 0, 0.3), (0, 0, 0.42), "hips"),
        ("row0", (0, 0, 0.31), (0, 0, 0.40), "chest"),
        ("row1", (0, 0, 0.42), (0, 0, 0.51), "chest"),
        ("row2", (0, 0, 0.53), (0, 0, 0.62), "chest"),
        ("head", (0, 0, 0.64), (0, 0, 0.86), "row2"),
        ("arm_l", (0.25, 0, 0.59), (0.25, 0, 0.40), "row2"),
        ("fist_l", (0.25, 0, 0.38), (0.25, 0, 0.2), "arm_l"),
        ("arm_r", (-0.25, 0, 0.59), (-0.25, 0, 0.40), "row2"),
        ("fist_r", (-0.25, 0, 0.38), (-0.25, 0, 0.2), "arm_r"),
        ("leg_l", (0.07, 0, 0.2), (0.07, 0, 0.02), "hips"),
        ("leg_r", (-0.07, 0, 0.2), (-0.07, 0, 0.02), "hips"),
    ])
    # the body is a 3x3 matrix of blocks, one bone per row; the centre cell is the core
    for r, z in enumerate((0.36, 0.47, 0.58)):
        for c, x in enumerate((-0.117, 0.0, 0.117)):
            if (r, c) == (1, 1):
                o = box("tk_core", (0.078, 0.255, 0.078), (x, 0, z), core)
                frame = box("tk_coreframe", (0.11, 0.21, 0.11), (x, 0.02, z), stone_b, bevel=0.01)
                att(arm, f"row{r}", o, frame)
                continue
            m = stone_a if (r + c) % 2 == 0 else stone_b
            o = box(f"tk_b{r}{c}", (0.105, 0.25, 0.105), (x, 0, z), m, bevel=0.014)
            att(arm, f"row{r}", o)
        att(arm, f"row{r}", box(f"tk_moss{r}", (0.31, 0.2, 0.1), (0, 0.01, z), moss))
    att(arm, "row2",
        box("tk_tuft1", (0.08, 0.12, 0.022), (-0.11, 0.0, 0.64), moss),
        box("tk_tuft2", (0.05, 0.07, 0.03), (0.13, -0.03, 0.638), moss),
        box("tk_jointl", (0.07, 0.11, 0.1), (0.18, 0, 0.585), moss),
        box("tk_jointr", (0.07, 0.11, 0.1), (-0.18, 0, 0.585), moss))
    att(arm, "row0", box("tk_tuft3", (0.06, 0.08, 0.02), (0.11, -0.06, 0.305), moss))
    att(arm, "hips", box("tk_hips", (0.28, 0.21, 0.07), (0, 0, 0.27), stone_b, bevel=0.012))
    att(arm, "head",
        box("tk_head", (0.30, 0.25, 0.22), (0, -0.005, 0.75), stone_a, bevel=0.024),
        box("tk_brow", (0.31, 0.06, 0.05), (0, -0.125, 0.81), stone_b, bevel=0.01),
        box("tk_jaw", (0.2, 0.06, 0.05), (0, -0.12, 0.67), stone_b, bevel=0.01),
        box("tk_eyel", (0.064, 0.02, 0.034), (0.065, -0.132, 0.755), eye),
        box("tk_eyer", (0.064, 0.02, 0.034), (-0.065, -0.132, 0.755), eye),
        box("tk_cap", (0.24, 0.19, 0.03), (0.02, 0.01, 0.872), moss),
        box("tk_cap2", (0.07, 0.07, 0.045), (-0.08, 0.03, 0.89), moss))
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"arm_{side}",
            box(f"tk_shoulder{side}", (0.14, 0.17, 0.13), (s * 0.25, 0, 0.59), stone_b, bevel=0.015),
            box(f"tk_upper{side}", (0.1, 0.13, 0.12), (s * 0.25, 0, 0.455), stone_a, bevel=0.012))
        att(arm, f"fist_{side}",
            box(f"tk_fist{side}", (0.17, 0.19, 0.15), (s * 0.26, -0.01, 0.29), stone_b, bevel=0.016),
            box(f"tk_wrist{side}", (0.09, 0.09, 0.03), (s * 0.255, 0, 0.375), moss),
            box(f"tk_knuck{side}", (0.12, 0.03, 0.03), (s * 0.26, -0.107, 0.26), stone_a))
        att(arm, f"leg_{side}",
            box(f"tk_leg{side}", (0.10, 0.14, 0.13), (s * 0.07, 0, 0.135), stone_a, bevel=0.012),
            box(f"tk_foot{side}", (0.11, 0.18, 0.06), (s * 0.07, -0.01, 0.03), stone_b, bevel=0.01))

    idle = []
    for i in range(4):
        b = -0.01 * (0.5 - 0.5 * C(i, 4))
        idle.append({
            "chest": {"l": (0, 0, b)},
            "row1": {"l": (0.004 * S(i, 4), 0, 0)},
            "row2": {"l": (-0.004 * S(i, 4), 0, 0.002 * C(i, 4))},
            "head": {"r": (0, 0, 3 * S(i, 4))},
            "arm_l": {"r": (3 * S(i, 4), -2, 0)}, "arm_r": {"r": (3 * S(i, 4), 2, 0)},
        })
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append({
            "hips": {"l": (0, 0, -0.012 + 0.018 * abs(s))},
            "chest": {"r": (6, 6 * s, 0)},
            "head": {"r": (-4, -4 * s, 0)},
            "leg_l": {"r": (-28 * s, 0, 0), "l": (0, 0, 0.04 * max(0.0, s))},
            "leg_r": {"r": (28 * s, 0, 0), "l": (0, 0, 0.04 * max(0.0, -s))},
            "arm_l": {"r": (22 * s, -3, 0)}, "arm_r": {"r": (-22 * s, 3, 0)},
            "row1": {"l": (0.006 * s, 0, 0)}, "row2": {"l": (-0.006 * s, 0, 0)},
        })
    raised = {
        "hips": {"l": (0, 0.03, -0.035)},
        "chest": {"r": (-16, 0, 0)},
        "head": {"r": (8, 0, 0)},
        "arm_l": {"r": (160, -22, 0)}, "arm_r": {"r": (160, 22, 0)},
        "fist_l": {"r": (0, -15, 0)}, "fist_r": {"r": (0, 15, 0)},
        "row2": {"l": (0, 0.01, 0.01)},
    }
    windup = [
        {"hips": {"l": (0, -0.01, -0.02)}, "chest": {"r": (8, 0, 0)},
         "arm_l": {"r": (-95, -10, 0)}, "arm_r": {"r": (-95, 10, 0)}},
        raised,
        merge(raised, {"chest": {"r": (-19, 2, 0)}, "arm_l": {"r": (166, -22, 0)},
                       "arm_r": {"r": (166, 22, 0)}, "row1": {"l": (0.008, 0, 0)}}),
        merge(raised, {"chest": {"r": (-18, -2, 0)}, "arm_l": {"r": (164, -22, 0)},
                       "arm_r": {"r": (164, 22, 0)}, "row1": {"l": (-0.008, 0, 0)}}),
    ]
    attack = [
        {"hips": {"l": (0, -0.03, -0.03)}, "chest": {"r": (22, 0, 0)}, "head": {"r": (-12, 0, 0)},
         "arm_l": {"r": (-75, 0, -20)}, "arm_r": {"r": (-75, 0, 20)}},
        {"hips": {"l": (0, -0.02, -0.07)}, "chest": {"r": (30, 0, 0)}, "head": {"r": (-22, 0, 0)},
         "arm_l": {"r": (-26, 0, -34)}, "arm_r": {"r": (-26, 0, 34)},
         "fist_l": {"r": (-20, 0, 0)}, "fist_r": {"r": (-20, 0, 0)},
         "row2": {"l": (0, -0.012, -0.01)}, "row1": {"l": (0, -0.006, -0.006)}},
        {"hips": {"l": (0, -0.02, -0.06)}, "chest": {"r": (27, 0, 0)}, "head": {"r": (-18, 0, 0)},
         "arm_l": {"r": (-30, 0, -32)}, "arm_r": {"r": (-30, 0, 32)},
         "fist_l": {"r": (-15, 0, 0)}, "fist_r": {"r": (-15, 0, 0)},
         "row2": {"l": (0, 0.006, 0.004)}},
        {"hips": {"l": (0, -0.02, -0.02)}, "chest": {"r": (12, 0, 0)}, "head": {"r": (-6, 0, 0)},
         "arm_l": {"r": (-20, 0, -8)}, "arm_r": {"r": (-20, 0, 8)}},
    ]
    hit = [
        {"hips": {"l": (0, 0.03, 0)}, "chest": {"r": (-14, 5, 0)}, "head": {"r": (-12, 0, 6)},
         "arm_l": {"r": (25, -12, 0)}, "arm_r": {"r": (25, 12, 0)},
         "row2": {"l": (0, 0.015, 0)}, "row1": {"l": (0, 0.008, 0)}},
        {"hips": {"l": (0, 0.015, 0)}, "chest": {"r": (-6, 2, 0)}, "head": {"r": (-4, 0, 2)},
         "arm_l": {"r": (10, -5, 0)}, "arm_r": {"r": (10, 5, 0)}},
    ]
    die = [
        {"chest": {"r": (-10, 8, 0)}, "head": {"r": (0, 0, 10)},
         "arm_l": {"r": (15, -10, 0)}, "arm_r": {"r": (15, 10, 0)},
         "row2": {"l": (0.015, 0, 0)}, "row1": {"l": (-0.012, 0, 0)}},
        {"hips": {"l": (0, 0, -0.08)}, "chest": {"r": (6, -10, 0)},
         "head": {"l": (0.02, 0, 0.01), "r": (0, 16, 12)},
         "arm_l": {"r": (10, 0, 0)}, "arm_r": {"r": (10, 0, 0)},
         "row2": {"l": (0.03, 0, -0.01)}, "row1": {"l": (-0.02, 0, -0.005)}},
        {"hips": {"l": (0, 0, -0.06)}, "chest": {"r": (0, -5, 0)},
         "head": {"l": (0.02, 0.02, -0.08), "r": (0, 24, 12)},
         "arm_l": {"r": (0, 26, 0), "l": (-0.06, 0.0, -0.05)}, "arm_r": {"r": (0, -26, 0), "l": (0.06, 0.0, -0.05)},
         "row2": {"l": (0.03, 0.0, -0.08), "r": (0, 15, 0)}, "row1": {"l": (-0.03, 0.0, -0.05), "r": (0, -10, 0)},
         "row0": {"l": (0, 0, -0.02)}},
    ]
    # the rubble: the stumps of the legs stay planted, the rows slump onto them, the head
    # rolls off to one side, the arms fall back; the core still glows in the pile
    rubble = {"hips": {"l": (0, 0, -0.10)},
              "head": {"l": (-0.05, 0.0, -0.14), "r": (0, 0, 25)},
              "arm_l": {"r": (0, 34, 0), "l": (-0.11, 0.0, -0.07)},
              "arm_r": {"r": (0, -34, 0), "l": (0.11, 0.0, -0.07)},
              "row2": {"l": (0.04, 0.0, -0.20), "r": (0, 0, 12)},
              "row1": {"l": (-0.04, 0.0, -0.12), "r": (0, 0, -15)},
              "row0": {"l": (0, 0.0, -0.05)}}
    die += [lerp_pose(die[2], rubble, 0.7),
            merge(rubble, {"row2": {"l": (0.04, 0.0, -0.19)}}), rubble]
    for clip_frames in (idle, walk, windup, attack, hit, die):
        for p in clip_frames:
            plant_feet(p)
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
    return arm


def _more():
    from quadrupeds import build_ma_tran_thu, build_phong_lang
    from serpent import build_van_xa
    from serpent_shade import build_tam_ma
    return {
        "ma_tran_thu": ("Ma Trận Thú", 64, build_ma_tran_thu),
        "van_xa": ("Vân Xà", 48, build_van_xa),
        "phong_lang": ("Phong Lang", 48, build_phong_lang),
        "tam_ma": ("Tâm Ma", 64, build_tam_ma),
        **_set_b(),
    }


def _beasts():
    from beasts import BEASTS as table
    return table


def _pets():
    from pets import PETS as table
    return table


def _set_b():
    from bestiary_b import build_co_quan_nhan, build_dau_tu_oa, build_ho_lo_tinh, build_moc_yeu
    from dragon import build_loi_long
    from spider import build_tri_chu_tinh
    return {
        "dau_tu_oa": ("Đầu Tử Oa", 48, build_dau_tu_oa),
        "ho_lo_tinh": ("Hồ Lô Tinh", 48, build_ho_lo_tinh),
        "tri_chu_tinh": ("Tri Chu Tinh", 64, build_tri_chu_tinh),
        "moc_yeu": ("Mộc Yêu", 48, build_moc_yeu),
        "co_quan_nhan": ("Cơ Quan Nhân", 48, build_co_quan_nhan),
        "loi_long": ("Thiên Kiếp Lôi Long", 96, build_loi_long),
    }


BUILD = {
    "kiem_linh": ("Kiếm Linh", 48, build_kiem_linh),
    "thach_khoi": ("Thạch Khôi", 48, build_thach_khoi),
    **_more(),
}
