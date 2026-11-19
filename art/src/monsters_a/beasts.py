"""The six catchable spirit beasts (linh thú): companions, so appealing first. Big heads,
big shiny eyes, round clean silhouettes, a little spirit glow. Runs inside Blender.

Each has idle 4, walk 6, windup 4, attack 4 (events.hit), hit 2, die 6 (faints, lies
down), plus happy 4 (hop and spin, loops; played when tamed or petted) and sleep 4
(curled up, breathing, loops). One look each (no dị chủng). Output kind "beast", 48x48.

Linh Hồ, Tiểu Long and Kỳ Lân Con use the shared quadruped rig and clip generator
(quadrupeds.py) with an extra `eyes` bone for blinking; Huyền Quy, Bạch Hạc and Hỏa Tước
have their own rigs.
"""
from __future__ import annotations

import math

from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material, merge,
                 place, use_collection)
from quadrupeds import Legs, quad_armature, quad_clips

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def eye_mats(prefix, iris_col=None, glow=None):
    """Iris (glowing if `glow`), pupil and the white catch-light that makes eyes shine."""
    if glow:
        iris = material(f"MAT_{prefix}_eye", iris_col, iris_col, emit=4.0, glow=glow)
    else:
        iris = material(f"MAT_{prefix}_eye_iris", iris_col, iris_col, ramp="earth")
        iris["kit_priority"] = 3.0
    pupil = material(f"MAT_{prefix}_pupil", (0.06, 0.05, 0.07), (0.06, 0.05, 0.07), ramp="hair")
    pupil["kit_priority"] = 3.0
    shine = material(f"MAT_{prefix}_shine_pip", (0.97, 0.96, 0.97), (0.97, 0.96, 0.97), ramp="bone")
    shine["kit_priority"] = 3.0
    return iris, pupil, shine


def cute_eyes(prefix, x, y, z, r, mats, look=(0, -1, 0)):
    """A pair of big eyes at (±x, y, z): iris, pupil, and a catch-light up-left."""
    iris, pupil, shine = mats
    out = []
    for s in (1, -1):
        out.append(ball(f"{prefix}_iris{s}", (r, r * 0.5, r * 1.1), (s * x, y, z), iris, seg=10, rings=6))
        out.append(ball(f"{prefix}_pupil{s}", (r * 0.55, r * 0.3, r * 0.65), (s * x, y - r * 0.32, z - r * 0.08), pupil, seg=8, rings=5))
        out.append(ball(f"{prefix}_shine{s}", (r * 0.3,) * 3, (s * x - r * 0.3, y - r * 0.5, z + r * 0.4), shine, seg=6, rings=4))
    return out


def extra_quad_clips(arm, P, drop, tail_wrap=70.0, head_rest=(18, 0, 55)):
    """happy (hop and quarter-turn spin, loops) and sleep (curled, breathing) for a
    quadruped beast built on quadrupeds.py."""
    L = Legs(P)
    happy = []
    for i, (z, tuck) in enumerate(((0.0, 0.0), (0.05, 1.0), (0.07, 1.0), (0.02, 0.4))):
        p = L.plant(drop=0.02) if tuck == 0 else L.air((-30 * tuck, 50 * tuck), (-30 * tuck, 50 * tuck),
                                                        (30 * tuck, -40 * tuck), (30 * tuck, -40 * tuck))
        p.update({"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)},
                  "pelvis": {"l": (0, 0, -0.02 if tuck == 0 else 0.0)},
                  "head": {"r": (-14, 0, 8 * S(i, 4))}, "jaw": {"r": (22, 0, 0)},
                  "eyes": {"s": (1, 0.35, 1)},
                  "tail1": {"r": (30, 0, 30 * S(i, 4))}, "tail2": {"r": (20, 0, 40 * S(i, 4, -1))}})
        happy.append(p)
    curl = L.plant(drop=drop, front=(-0.02, -0.02), back=(0.03, 0.03), pitch=4)
    sleep = []
    for i in range(4):
        b = 0.006 * S(i, 4)
        p = dict(curl)
        p.update({"pelvis": {"l": (0, 0, -drop + b)}, "chest": {"r": (4, 0, 0), "s": 1.0 + 0.02 * S(i, 4)},
                  "head": {"r": head_rest, "l": (0, 0.02, -0.05)}, "jaw": {"r": (0, 0, 0)},
                  "eyes": {"s": (1, 0.12, 1)},
                  "tail1": {"r": (-12, 0, tail_wrap)}, "tail2": {"r": (-6, 0, tail_wrap * 0.8)}})
        sleep.append(p)
    clip(arm, "happy", happy, 8, True)
    clip(arm, "sleep", sleep, 4, True)
    arm.animation_data.action = None


def eyes_bone(hy, hz):
    return ("eyes", (0, hy, hz - 0.03), (0, hy, hz + 0.05), "head")


# =============================================================== Linh Hồ
def build_linh_ho():
    use_collection("COL_linh_ho")
    fur = material("MAT_lh_fur", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")
    fur_sh = material("MAT_lh_fur_shade", (0.60, 0.58, 0.64), (0.60, 0.58, 0.64), ramp="bone")
    ear_tip = material("MAT_lh_eartip", (0.39, 0.53, 0.77), (0.39, 0.53, 0.77), ramp="blue")
    inner = material("MAT_lh_inner", (0.95, 0.72, 0.78), (0.95, 0.72, 0.78), ramp="pink")
    flame = material("MAT_lh_flame", (0.35, 0.88, 0.96), (0.35, 0.88, 0.96), emit=4.0, glow="spirit")
    nose = material("MAT_lh_nose", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    mats = eye_mats("lh", (1.0, 0.89, 0.48), glow="holy")

    HY, HZ = -0.19, 0.49
    P = {"h": 0.30, "yf": -0.06, "yb": 0.09, "x": 0.085, "knee": 0.14,
         "head": (-0.12, 0.36), "hlen": 0.2, "jaw": (-0.27, 0.445),
         "tail": ((0.15, 0.33), (0.25, 0.42), (0.30, 0.56))}
    arm = quad_armature("linh_ho", P, extra=[eyes_bone(HY - 0.1, 0.51)])
    att(arm, "chest", ball("lh_chest", (0.12, 0.12, 0.11), (0, -0.03, 0.32), fur),
        ball("lh_ruff", (0.12, 0.07, 0.10), (0, -0.10, 0.35), fur))
    att(arm, "pelvis", ball("lh_rump", (0.10, 0.10, 0.10), (0, 0.08, 0.31), fur))
    att(arm, "head", ball("lh_head", (0.17, 0.15, 0.14), (0, HY, HZ), fur),
        ball("lh_cheekl", (0.07, 0.06, 0.06), (0.12, HY - 0.02, HZ - 0.06), fur, seg=10, rings=6),
        ball("lh_cheekr", (0.07, 0.06, 0.06), (-0.12, HY - 0.02, HZ - 0.06), fur, seg=10, rings=6),
        aim("lh_muzzle", fur, (0, HY - 0.08, HZ - 0.04), (0, HY - 0.19, HZ - 0.06), 0.06, 0.03, seg=10, smooth=True),
        ball("lh_nose", (0.024, 0.02, 0.02), (0, HY - 0.19, HZ - 0.05), nose, seg=8, rings=5),
        aim("lh_earl", fur, (0.08, HY + 0.02, HZ + 0.10), (0.16, HY + 0.06, HZ + 0.31), 0.07, 0.0, seg=6),
        aim("lh_earr", fur, (-0.08, HY + 0.02, HZ + 0.10), (-0.16, HY + 0.06, HZ + 0.31), 0.07, 0.0, seg=6),
        aim("lh_earil", inner, (0.085, HY + 0.005, HZ + 0.12), (0.145, HY + 0.035, HZ + 0.26), 0.035, 0.0, seg=6),
        aim("lh_earir", inner, (-0.085, HY + 0.005, HZ + 0.12), (-0.145, HY + 0.035, HZ + 0.26), 0.035, 0.0, seg=6),
        aim("lh_eartl", ear_tip, (0.14, HY + 0.05, HZ + 0.24), (0.165, HY + 0.062, HZ + 0.33), 0.034, 0.0, seg=6),
        aim("lh_eartr", ear_tip, (-0.14, HY + 0.05, HZ + 0.24), (-0.165, HY + 0.062, HZ + 0.33), 0.034, 0.0, seg=6))
    att(arm, "eyes", *cute_eyes("lh", 0.068, HY - 0.115, HZ + 0.02, 0.042, mats))
    att(arm, "jaw", aim("lh_jaw", fur_sh, (0, HY - 0.08, HZ - 0.08), (0, HY - 0.17, HZ - 0.09), 0.04, 0.022, seg=8))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"lh_{leg}{side}up", fur, (x, y, 0.27), (x, y, 0.14), 0.045, 0.035, seg=8))
            att(arm, f"{leg}{side}2", aim(f"lh_{leg}{side}lo", fur, (x, y, 0.15), (x, y, 0.035), 0.032, 0.03, seg=8))
            att(arm, f"{leg}{side}3", ball(f"lh_{leg}{side}paw", (0.04, 0.045, 0.028), (x, y - 0.005, 0.025), fur_sh, seg=8, rings=5))
    # the great fluffy tail, tipped with blue spirit flame
    att(arm, "tail1", ball("lh_tail1", (0.07, 0.09, 0.07), (0, 0.20, 0.38), fur))
    att(arm, "tail2", ball("lh_tail2", (0.11, 0.11, 0.13), (0, 0.27, 0.49), fur),
        ball("lh_tailtip", (0.085, 0.085, 0.07), (0, 0.29, 0.59), flame),
        aim("lh_flame", flame, (0, 0.29, 0.62), (0.0, 0.32, 0.74), 0.06, 0.0, seg=8))
    quad_clips(arm, P, {"stride": 0.03, "lift": 0.045, "hop": 0.06, "crouch": 0.06, "drop": 0.15,
                        "lunge": 0.02, "walk_fps": 12})
    extra_quad_clips(arm, P, drop=0.15)
    return arm


# =============================================================== Tiểu Long
def build_tieu_long():
    use_collection("COL_tieu_long")
    jade = material("MAT_tl_jade", (0.18, 0.48, 0.35), (0.18, 0.48, 0.35), ramp="jade")
    jade_lt = material("MAT_tl_jade_light", (0.31, 0.65, 0.47), (0.31, 0.65, 0.47), ramp="jade")
    cream = material("MAT_tl_belly", (0.93, 0.87, 0.70), (0.93, 0.87, 0.70), ramp="paper")
    horn = material("MAT_tl_horn", (0.90, 0.72, 0.23), (0.90, 0.72, 0.23), ramp="gold", metal=True)
    spine = material("MAT_tl_spine", (0.48, 0.92, 0.60), (0.48, 0.92, 0.60), emit=2.5, glow="verdant")
    nose = material("MAT_tl_nose", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    mats = eye_mats("tl", (1.0, 0.89, 0.48), glow="holy")

    HY, HZ = -0.21, 0.44
    P = {"h": 0.24, "yf": -0.07, "yb": 0.10, "x": 0.09, "knee": 0.11,
         "head": (-0.15, 0.33), "hlen": 0.2, "jaw": (-0.29, 0.395),
         "tail": ((0.18, 0.26), (0.28, 0.31), (0.35, 0.42))}
    arm = quad_armature("tieu_long", P, extra=[eyes_bone(HY - 0.1, HZ + 0.03)])
    att(arm, "chest", ball("tl_chest", (0.12, 0.12, 0.11), (0, -0.05, 0.25), jade),
        ball("tl_bellyf", (0.09, 0.08, 0.07), (0, -0.09, 0.19), cream),
        *[cone(f"tl_spinec{k}", 0.03, 0.0, 0.06, (0, y, 0.365), spine, seg=5) for k, y in enumerate((-0.07, 0.0))])
    att(arm, "pelvis", ball("tl_rump", (0.11, 0.12, 0.10), (0, 0.09, 0.24), jade),
        ball("tl_bellyb", (0.08, 0.09, 0.06), (0, 0.06, 0.18), cream),
        *[cone(f"tl_spinep{k}", 0.028, 0.0, 0.055, (0, y, 0.345), spine, seg=5) for k, y in enumerate((0.07, 0.14))])
    att(arm, "head", ball("tl_head", (0.17, 0.16, 0.14), (0, HY, HZ), jade),
        box("tl_snout", (0.13, 0.15, 0.085), (0, HY - 0.13, HZ - 0.04), jade_lt, bevel=0.035),
        ball("tl_nostl", (0.018,) * 3, (0.035, HY - 0.205, HZ - 0.01), nose, seg=6, rings=4),
        ball("tl_nostr", (0.018,) * 3, (-0.035, HY - 0.205, HZ - 0.01), nose, seg=6, rings=4),
        aim("tl_hornl", horn, (0.07, HY + 0.03, HZ + 0.11), (0.11, HY + 0.09, HZ + 0.22), 0.025, 0.008, seg=6),
        aim("tl_hornr", horn, (-0.07, HY + 0.03, HZ + 0.11), (-0.11, HY + 0.09, HZ + 0.22), 0.025, 0.008, seg=6),
        aim("tl_tinel", horn, (0.095, HY + 0.07, HZ + 0.18), (0.15, HY + 0.07, HZ + 0.21), 0.014, 0.0, seg=5),
        aim("tl_tiner", horn, (-0.095, HY + 0.07, HZ + 0.18), (-0.15, HY + 0.07, HZ + 0.21), 0.014, 0.0, seg=5),
        ball("tl_mane1", (0.07, 0.06, 0.06), (0, HY + 0.12, HZ + 0.08), cream, seg=10, rings=6),
        ball("tl_mane2", (0.05,) * 3, (0.07, HY + 0.1, HZ + 0.04), cream, seg=8, rings=5),
        ball("tl_mane3", (0.05,) * 3, (-0.07, HY + 0.1, HZ + 0.04), cream, seg=8, rings=5),
        aim("tl_whiskl", cream, (0.06, HY - 0.19, HZ - 0.03), (0.17, HY - 0.15, HZ - 0.07), 0.014, 0.004, seg=5),
        aim("tl_whiskr", cream, (-0.06, HY - 0.19, HZ - 0.03), (-0.17, HY - 0.15, HZ - 0.07), 0.014, 0.004, seg=5))
    att(arm, "eyes", *cute_eyes("tl", 0.07, HY - 0.115, HZ + 0.03, 0.045, mats))
    att(arm, "jaw", box("tl_jaw", (0.11, 0.13, 0.03), (0, HY - 0.12, HZ - 0.09), cream, bevel=0.012))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"tl_{leg}{side}up", jade, (x, y, 0.20), (x, y, 0.11), 0.05, 0.04, seg=8))
            att(arm, f"{leg}{side}2", aim(f"tl_{leg}{side}lo", jade, (x, y, 0.12), (x, y, 0.035), 0.038, 0.034, seg=8))
            att(arm, f"{leg}{side}3", ball(f"tl_{leg}{side}paw", (0.045, 0.05, 0.03), (x, y - 0.01, 0.028), jade_lt, seg=8, rings=5),
                *[aim(f"tl_{leg}{side}claw{k}", cream, (x + (k - 1) * 0.02, y - 0.04, 0.02), (x + (k - 1) * 0.022, y - 0.06, 0.01), 0.008, 0.0, seg=4)
                  for k in range(3)])
    att(arm, "tail1", aim("tl_tail1", jade, (0, 0.18, 0.26), (0, 0.28, 0.31), 0.075, 0.055, seg=10, smooth=True))
    att(arm, "tail2", aim("tl_tail2", jade, (0, 0.28, 0.31), (0, 0.35, 0.42), 0.055, 0.025, seg=10, smooth=True),
        ball("tl_tailtuft", (0.05, 0.05, 0.06), (0, 0.36, 0.45), cream, seg=10, rings=6),
        cone("tl_spinet", 0.025, 0.0, 0.05, (0, 0.27, 0.37), spine, seg=5))
    quad_clips(arm, P, {"stride": 0.03, "lift": 0.04, "hop": 0.05, "crouch": 0.05, "drop": 0.11,
                        "lunge": 0.02, "walk_fps": 11})
    extra_quad_clips(arm, P, drop=0.11, tail_wrap=80.0, head_rest=(-6, 0, 60))
    return arm


# =============================================================== Kỳ Lân Con
def build_ky_lan_con():
    use_collection("COL_ky_lan_con")
    coat = material("MAT_kl2_coat", (0.93, 0.87, 0.70), (0.93, 0.87, 0.70), ramp="paper")
    coat_sh = material("MAT_kl2_coat_shade", (0.82, 0.70, 0.52), (0.82, 0.70, 0.52), ramp="paper")
    scale = material("MAT_kl2_scale", (0.90, 0.72, 0.23), (0.90, 0.72, 0.23), ramp="gold", metal=True)
    horn = material("MAT_kl2_horn", (0.31, 0.65, 0.47), (0.31, 0.65, 0.47), ramp="jade")
    mane = material("MAT_kl2_mane", (1.0, 0.89, 0.48), (1.0, 0.89, 0.48), emit=2.0, glow="holy")
    mane["kit_halo"] = 1
    hoof = material("MAT_kl2_hoof", (0.73, 0.51, 0.10), (0.73, 0.51, 0.10), ramp="gold", metal=True)
    blush = material("MAT_kl2_blush", (0.95, 0.72, 0.78), (0.95, 0.72, 0.78), ramp="pink")
    mats = eye_mats("kl2", (0.42, 0.35, 0.28))

    HY, HZ = -0.21, 0.66
    P = {"h": 0.42, "yf": -0.06, "yb": 0.09, "x": 0.07, "knee": 0.20,
         "head": (-0.12, 0.50), "hlen": 0.25, "jaw": (-0.29, 0.62),
         "tail": ((0.16, 0.44), (0.23, 0.50), (0.30, 0.56))}
    arm = quad_armature("ky_lan_con", P, extra=[eyes_bone(HY - 0.09, HZ + 0.02)])
    att(arm, "chest", ball("kl2_chest", (0.11, 0.11, 0.11), (0, -0.03, 0.44), coat),
        aim("kl2_neck", coat, (0, -0.08, 0.48), (0, -0.15, 0.62), 0.06, 0.05, seg=10, smooth=True),
        *[box(f"kl2_scale{k}", (0.07, 0.05, 0.02), (0, y, 0.545 - 0.004 * k), scale, rot=(-10, 0, 45))
          for k, y in enumerate((-0.07, -0.02))])
    att(arm, "pelvis", ball("kl2_rump", (0.10, 0.11, 0.10), (0, 0.08, 0.43), coat),
        *[box(f"kl2_scalep{k}", (0.065, 0.05, 0.02), (0, y, 0.53), scale, rot=(0, 0, 45))
          for k, y in enumerate((0.03, 0.09))])
    hd = [ball("kl2_head", (0.12, 0.12, 0.11), (0, HY, HZ), coat),
          aim("kl2_muzzle", coat_sh, (0, HY - 0.07, HZ - 0.04), (0, HY - 0.16, HZ - 0.07), 0.055, 0.04, seg=10, smooth=True),
          aim("kl2_horn", horn, (0, HY - 0.02, HZ + 0.10), (0, HY + 0.01, HZ + 0.22), 0.024, 0.0, seg=6),
          aim("kl2_earl", coat, (0.08, HY + 0.02, HZ + 0.06), (0.17, HY + 0.05, HZ + 0.10), 0.03, 0.0, seg=6),
          aim("kl2_earr", coat, (-0.08, HY + 0.02, HZ + 0.06), (-0.17, HY + 0.05, HZ + 0.10), 0.03, 0.0, seg=6),
          ball("kl2_blushl", (0.025, 0.01, 0.015), (0.07, HY - 0.105, HZ - 0.03), blush, seg=6, rings=4),
          ball("kl2_blushr", (0.025, 0.01, 0.015), (-0.07, HY - 0.105, HZ - 0.03), blush, seg=6, rings=4)]
    for k, (y, z) in enumerate(((0.02, 0.08), (0.08, 0.02), (0.13, -0.06))):
        hd.append(aim(f"kl2_mane{k}", mane, (0, HY + y, HZ + z), (0, HY + y + 0.09, HZ + z + 0.06), 0.04, 0.0, seg=6))
    att(arm, "head", *hd)
    att(arm, "eyes", *cute_eyes("kl2", 0.055, HY - 0.095, HZ + 0.015, 0.035, mats))
    att(arm, "jaw", aim("kl2_jaw", coat_sh, (0, HY - 0.07, HZ - 0.08), (0, HY - 0.14, HZ - 0.09), 0.03, 0.02, seg=8))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"kl2_{leg}{side}up", coat, (x, y, 0.38), (x, y, 0.20), 0.04 if leg == "f" else 0.048, 0.028, seg=8))
            att(arm, f"{leg}{side}2", aim(f"kl2_{leg}{side}lo", coat_sh, (x, y, 0.21), (x, y, 0.05), 0.025, 0.022, seg=8),
                ball(f"kl2_{leg}{side}fire", (0.04, 0.04, 0.03), (x, y + 0.01, 0.08), mane, seg=8, rings=5))
            att(arm, f"{leg}{side}3", box(f"kl2_{leg}{side}hoof", (0.045, 0.05, 0.04), (x, y - 0.005, 0.02), hoof, bevel=0.008))
    att(arm, "tail1", aim("kl2_tail1", coat, (0, 0.16, 0.44), (0, 0.23, 0.50), 0.025, 0.02, seg=6))
    att(arm, "tail2", aim("kl2_tailfire", mane, (0, 0.22, 0.49), (0, 0.32, 0.58), 0.05, 0.0, seg=8))
    quad_clips(arm, P, {"stride": 0.035, "lift": 0.05, "hop": 0.06, "crouch": 0.07, "drop": 0.22,
                        "lunge": 0.02, "walk_fps": 11})
    extra_quad_clips(arm, P, drop=0.22, tail_wrap=40.0, head_rest=(30, 0, 50))
    return arm


# =============================================================== Huyền Quy
def build_huyen_quy():
    use_collection("COL_huyen_quy")
    skin = material("MAT_hq_skin", (0.37, 0.39, 0.44), (0.37, 0.39, 0.44), ramp="stone")
    skin_lt = material("MAT_hq_skin_light", (0.53, 0.56, 0.60), (0.53, 0.56, 0.60), ramp="stone")
    shell = material("MAT_hq_shell", (0.18, 0.48, 0.35), (0.18, 0.48, 0.35), ramp="jade")
    shell_dk = material("MAT_hq_shell_rim", (0.11, 0.31, 0.25), (0.11, 0.31, 0.25), ramp="jade")
    plate = material("MAT_hq_plate", (0.31, 0.65, 0.47), (0.31, 0.65, 0.47), ramp="jade")
    glowp = material("MAT_hq_plate_glow", (0.48, 0.92, 0.60), (0.48, 0.92, 0.60), emit=3.0, glow="verdant")
    dot = material("MAT_hq_dot_mark", (0.48, 0.92, 0.60), (0.48, 0.92, 0.60), emit=3.0, glow="verdant")
    belly = material("MAT_hq_plastron", (0.82, 0.70, 0.52), (0.82, 0.70, 0.52), ramp="paper")
    blush = material("MAT_hq_blush", (0.95, 0.72, 0.78), (0.95, 0.72, 0.78), ramp="pink")
    mats = eye_mats("hq", (0.97, 0.96, 0.97))
    mats[0]["kit_ramp"] = "bone"          # white eyes with big dark pupils

    arm = armature("huyen_quy", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("shell", (0, 0, 0.10), (0, 0, 0.30), "root"),
        ("head", (0, -0.15, 0.18), (0, -0.28, 0.24), "shell"),
        ("eyes", (0, -0.35, 0.34), (0, -0.35, 0.42), "head"),
        ("tail", (0, 0.20, 0.12), (0, 0.24, 0.11), "shell"),
        ("fl", (0.09, -0.07, 0.12), (0.09, -0.07, 0.0), "shell"),
        ("fr", (-0.09, -0.07, 0.12), (-0.09, -0.07, 0.0), "shell"),
        ("bl", (0.09, 0.09, 0.12), (0.09, 0.09, 0.0), "shell"),
        ("br", (-0.09, 0.09, 0.12), (-0.09, 0.09, 0.0), "shell"),
    ])
    parts = [ball("hq_dome", (0.21, 0.23, 0.16), (0, 0.02, 0.18), shell),
             cone("hq_rim", 0.215, 0.21, 0.045, (0, 0.02, 0.14), shell_dk, seg=16),
             ball("hq_plastron", (0.18, 0.20, 0.03), (0, 0.02, 0.11), belly)]
    # hexagon plates: one glowing at the crown, six around it
    import mathutils
    def on_dome(u, v):
        """Point and normal on the dome (u around, v from the top, degrees)."""
        uu, vv = math.radians(u), math.radians(v)
        n = mathutils.Vector((math.sin(vv) * math.sin(uu), -math.sin(vv) * math.cos(uu), math.cos(vv)))
        p = mathutils.Vector((0.22 * n.x, 0.02 + 0.24 * n.y, 0.17 + 0.16 * n.z))
        return p + n * 0.006, n
    p0, n0 = on_dome(0, 0)
    ob = cone("hq_plate0", 0.075, 0.065, 0.02, (0, 0, 0), glowp, seg=6)
    ob.matrix_world = place(n0, p0)
    parts.append(ob)
    for k in range(6):
        p, n = on_dome(60 * k + 30, 52)
        ob = cone(f"hq_plate{k + 1}", 0.06, 0.05, 0.018, (0, 0, 0), plate, seg=6)
        ob.matrix_world = place(n, p)
        parts.append(ob)
        parts.append(ball(f"hq_dot{k}", (0.016,) * 3, tuple(p + n * 0.012), dot, seg=6, rings=4))
    att(arm, "shell", *parts)
    att(arm, "head", ball("hq_head", (0.15, 0.13, 0.125), (0, -0.27, 0.30), skin),
        ball("hq_snout", (0.08, 0.04, 0.05), (0, -0.375, 0.265), skin_lt, seg=10, rings=6),
        box("hq_smile", (0.06, 0.012, 0.014), (0, -0.405, 0.25), skin),
        ball("hq_blushl", (0.028, 0.01, 0.018), (0.085, -0.36, 0.25), blush, seg=6, rings=4),
        ball("hq_blushr", (0.028, 0.01, 0.018), (-0.085, -0.36, 0.25), blush, seg=6, rings=4),
        aim("hq_neck", skin, (0, -0.14, 0.17), (0, -0.23, 0.25), 0.065, 0.065, seg=8))
    eyes = cute_eyes("hq", 0.064, -0.355, 0.375, 0.05, mats)
    eyes += [ball(f"hq_lid{s}", (0.05, 0.03, 0.022), (s * 0.064, -0.345, 0.414), skin, seg=8, rings=5) for s in (1, -1)]
    att(arm, "eyes", *eyes)
    att(arm, "tail", aim("hq_tail", skin, (0, 0.20, 0.13), (0, 0.25, 0.12), 0.03, 0.0, seg=6))
    for n, x, y in (("fl", 0.09, -0.07), ("fr", -0.09, -0.07), ("bl", 0.09, 0.09), ("br", -0.09, 0.09)):
        att(arm, n, ball(f"hq_leg{n}", (0.055, 0.055, 0.07), (x, y, 0.07), skin, seg=10, rings=6),
            ball(f"hq_foot{n}", (0.05, 0.055, 0.025), (x, y - 0.005, 0.022), skin_lt, seg=8, rings=5))

    tucked = {"head": {"l": (0, 0.09, -0.02), "s": 0.85}, "fl": {"s": 0.4}, "fr": {"s": 0.4},
              "bl": {"s": 0.4}, "br": {"s": 0.4}, "tail": {"s": 0.3}}
    idle = [{"shell": {"l": (0, 0, 0.004 * S(i, 4))}, "head": {"r": (4 * S(i, 4), 0, 4 * S(i, 4, 1))},
             "eyes": {"s": (1, 0.6 if i in (2,) else 1.0, 1)}} for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append({"shell": {"r": (0, 4 * s, 0), "l": (0, 0, 0.008 * abs(s))},
                     "head": {"r": (6 * abs(s), 0, -4 * s)},
                     "fl": {"r": (-20 * s, 0, 0), "l": (0, 0, 0.02 * max(0.0, s) - 0.008 * abs(s))},
                     "br": {"r": (-20 * s, 0, 0), "l": (0, 0, 0.02 * max(0.0, s) - 0.008 * abs(s))},
                     "fr": {"r": (20 * s, 0, 0), "l": (0, 0, 0.02 * max(0.0, -s) - 0.008 * abs(s))},
                     "bl": {"r": (20 * s, 0, 0), "l": (0, 0, 0.02 * max(0.0, -s) - 0.008 * abs(s))},
                     "tail": {"r": (0, 0, 20 * s)}})
    # windup: pulls head and legs into the shell, which rises and glows: a jade dome
    hide = merge(tucked, {"shell": {"l": (0, 0, 0.02), "r": (-6, 0, 0)}})
    windup = [lerp_pose(idle[0], hide, 0.5), hide, merge(hide, {"shell": {"r": (-6, 0, 6)}}),
              merge(hide, {"shell": {"r": (-6, 0, -6)}})]
    attack = [merge(tucked, {"shell": {"r": (0, 0, 100), "l": (0, 0, 0.03)}}),
              merge(tucked, {"shell": {"r": (0, 0, 220), "l": (0, 0, 0.02)}}),
              merge(tucked, {"shell": {"r": (0, 0, 330), "l": (0, 0, 0.01)}}),
              lerp_pose(tucked, idle[0], 0.6)]
    hit = [{"shell": {"r": (-5, 0, 6), "l": (0, 0.0, 0.01)}, "head": {"l": (0, 0.05, 0)}, "eyes": {"s": (1, 0.3, 1)}},
           {"shell": {"r": (-4, 0, 2)}, "eyes": {"s": (1, 0.7, 1)}}]
    faint = {"shell": {"l": (0, 0, -0.03)}, "head": {"r": (0, 0, 30), "l": (0, 0.03, -0.03)},
             "eyes": {"s": (1, 0.12, 1)}, "fl": {"r": (-40, 30, 0)}, "fr": {"r": (-40, -30, 0)},
             "bl": {"r": (40, 30, 0)}, "br": {"r": (40, -30, 0)}}
    die = [{"shell": {"r": (-10, 0, 0)}, "eyes": {"s": 1.15}},
           {"shell": {"r": (-4, 8, 0)}, "head": {"r": (0, 0, 10)}, "eyes": {"s": (1, 0.5, 1)}},
           lerp_pose({}, faint, 0.6), faint, faint, faint]
    happy = [{"shell": {"l": (0, 0, z), "r": (0, 0, 90 * i)}, "head": {"r": (-14, 0, 6 * S(i, 4))},
              "eyes": {"s": (1, 0.35, 1)},
              "fl": {"r": (-30 * S(i, 4), 0, 0)}, "fr": {"r": (30 * S(i, 4), 0, 0)}}
             for i, z in enumerate((0.0, 0.05, 0.06, 0.02))]
    sleep = [merge(tucked, {"shell": {"l": (0, 0, -0.01 + 0.004 * S(i, 4)), "s": 1.0 + 0.015 * S(i, 4)},
                            "head": {"l": (0, 0.06, -0.03), "s": 0.9}, "eyes": {"s": (1, 0.12, 1)}}) for i in range(4)]
    finish(arm, idle, walk, windup, attack, hit, die, happy, sleep, scale=1.12)
    return arm


def finish(arm, idle, walk, windup, attack, hit, die, happy, sleep, scale=1.0, hit_frame=1):
    arm.scale = (scale,) * 3
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 10, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=hit_frame)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    clip(arm, "happy", happy, 8, True)
    clip(arm, "sleep", sleep, 4, True)
    arm.animation_data.action = None


# =============================================================== Bạch Hạc
def build_bach_hac():
    use_collection("COL_bach_hac")
    white = material("MAT_bh_white", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")
    black = material("MAT_bh_black", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    crown = material("MAT_bh_crown", (0.78, 0.33, 0.23), (0.78, 0.33, 0.23), ramp="red")
    beak = material("MAT_bh_beak", (0.90, 0.72, 0.23), (0.90, 0.72, 0.23), ramp="gold")
    leg = material("MAT_bh_leg", (0.27, 0.24, 0.30), (0.27, 0.24, 0.30), ramp="hair")
    aura = material("MAT_bh_aura_mark", (0.72, 0.75, 1.0), (0.72, 0.75, 1.0), emit=2.0, glow="ice")
    mats = eye_mats("bh", (0.42, 0.35, 0.28))

    arm = armature("bach_hac", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0.06, 0.44), (0, -0.07, 0.50), "root"),
        ("neck1", (0, -0.07, 0.52), (0, -0.09, 0.66), "body"),
        ("neck2", (0, -0.09, 0.66), (0, -0.10, 0.80), "neck1"),
        ("head", (0, -0.10, 0.80), (0, -0.10, 0.92), "neck2"),
        ("eyes", (0, -0.15, 0.84), (0, -0.15, 0.90), "head"),
        ("wing_l", (0.09, -0.02, 0.53), (0.09, 0.18, 0.50), "body"),
        ("wing_r", (-0.09, -0.02, 0.53), (-0.09, 0.18, 0.50), "body"),
        ("tail", (0, 0.14, 0.50), (0, 0.26, 0.48), "body"),
        ("leg_l1", (0.045, 0.02, 0.43), (0.045, 0.0, 0.22), "body"),
        ("leg_l2", (0.045, 0.0, 0.22), (0.045, 0.02, 0.02), "leg_l1"),
        ("leg_r1", (-0.045, 0.02, 0.43), (-0.045, 0.0, 0.22), "body"),
        ("leg_r2", (-0.045, 0.0, 0.22), (-0.045, 0.02, 0.02), "leg_r1"),
    ])
    att(arm, "body", ball("bh_body", (0.12, 0.17, 0.10), (0, 0.03, 0.50), white, rot=(-12, 0, 0)),
        ball("bh_chest", (0.09, 0.08, 0.09), (0, -0.08, 0.52), white))
    att(arm, "tail", aim("bh_tail1", black, (0.03, 0.15, 0.51), (0.05, 0.28, 0.47), 0.04, 0.0, seg=6),
        aim("bh_tail2", black, (-0.03, 0.15, 0.51), (-0.05, 0.28, 0.47), 0.04, 0.0, seg=6))
    att(arm, "neck1", aim("bh_neck1", white, (0, -0.07, 0.52), (0, -0.09, 0.67), 0.045, 0.04, seg=8, smooth=True))
    att(arm, "neck2", aim("bh_neck2", white, (0, -0.09, 0.66), (0, -0.10, 0.81), 0.04, 0.038, seg=8, smooth=True),
        aim("bh_neckband", black, (0, -0.09, 0.70), (0, -0.095, 0.77), 0.042, 0.04, seg=8))
    att(arm, "head", ball("bh_head", (0.08, 0.085, 0.075), (0, -0.12, 0.86), white),
        ball("bh_crown", (0.04, 0.04, 0.025), (0, -0.11, 0.935), crown, seg=10, rings=6),
        ball("bh_face", (0.05, 0.03, 0.035), (0, -0.19, 0.84), black, seg=8, rings=5),
        aim("bh_beak", beak, (0, -0.19, 0.85), (0, -0.33, 0.81), 0.022, 0.003, seg=6))
    att(arm, "eyes", *cute_eyes("bh", 0.045, -0.175, 0.875, 0.026, mats))
    for s, b in ((1, "wing_l"), (-1, "wing_r")):
        att(arm, b, ball(f"bh_{b}", (0.04, 0.15, 0.075), (s * 0.10, 0.06, 0.52), white, rot=(-8, 0, 0)),
            aim(f"bh_{b}tip", black, (s * 0.10, 0.16, 0.51), (s * 0.10, 0.30, 0.47), 0.05, 0.0, seg=6),
            ball(f"bh_{b}glow", (0.012,) * 3, (s * 0.12, 0.02, 0.56), aura, seg=6, rings=4))
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"leg_{side}1", aim(f"bh_thigh{side}", leg, (s * 0.045, 0.02, 0.45), (s * 0.045, 0.0, 0.22), 0.024, 0.02, seg=6),
            ball(f"bh_knee{side}", (0.026,) * 3, (s * 0.045, 0.0, 0.22), leg, seg=6, rings=4))
        att(arm, f"leg_{side}2", aim(f"bh_shin{side}", leg, (s * 0.045, 0.0, 0.22), (s * 0.045, 0.02, 0.02), 0.02, 0.02, seg=6),
            *[aim(f"bh_toe{side}{k}", leg, (s * 0.045, 0.02, 0.012), (s * 0.045 + (k - 1) * 0.03, -0.04, 0.008), 0.012, 0.006, seg=4)
              for k in range(3)])

    def wings(up=0.0, out=0.0, flap=0.0):
        return {"wing_l": {"r": (up + flap, 0, -out)}, "wing_r": {"r": (up + flap, 0, out)}}
    idle = [merge({"body": {"l": (0, 0, 0.005 * S(i, 4))}, "neck1": {"r": (3 * S(i, 4), 0, 0)},
                   "neck2": {"r": (-3 * S(i, 4), 0, 4 * S(i, 4, 1))}, "head": {"r": (0, 0, -4 * S(i, 4, 1))},
                   "eyes": {"s": (1, 0.2 if i == 3 else 1.0, 1)}}, wings(flap=3 * S(i, 4))) for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append(merge({"body": {"l": (0, 0, 0.01 * abs(s))},
                           "neck1": {"r": (6 * s, 0, 0)}, "neck2": {"r": (-8 * s, 0, 0)},
                           "leg_l1": {"r": (-15 * s, 0, 0), "l": (0, 0, -0.01 * abs(s))},
                           "leg_l2": {"r": (24 * max(0.0, s), 0, 0)},
                           "leg_r1": {"r": (15 * s, 0, 0), "l": (0, 0, -0.01 * abs(s))},
                           "leg_r2": {"r": (24 * max(0.0, -s), 0, 0)}}, wings(flap=4 * s)))
    # windup: both wings raised high in a V, neck drawn back
    raise_ = merge({"body": {"r": (-8, 0, 0)}, "neck1": {"r": (-14, 0, 0)}, "neck2": {"r": (-6, 0, 0)},
                    "head": {"r": (10, 0, 0)}}, wings(up=70, out=40))
    windup = [lerp_pose(idle[0], raise_, 0.5), raise_, merge(raise_, wings(up=74, out=42)),
              merge(raise_, wings(up=72, out=38))]
    # attack: a great downbeat that throws a gust ahead
    attack = [merge({"body": {"r": (8, 0, 0)}, "neck1": {"r": (10, 0, 0)}}, wings(up=10, out=70)),
              merge({"body": {"r": (12, 0, 0)}, "neck1": {"r": (14, 0, 0)}, "neck2": {"r": (6, 0, 0)}},
                    wings(up=-20, out=55)),
              merge({"body": {"r": (6, 0, 0)}}, wings(up=-10, out=30)),
              merge({}, wings(up=0, out=8))]
    hit = [merge({"body": {"r": (-12, 0, 6), "l": (0, 0.02, 0)}, "neck1": {"r": (-14, 0, 8)},
                  "eyes": {"s": (1, 0.3, 1)}}, wings(up=40, out=50)),
           merge({"body": {"r": (-4, 0, 2)}}, wings(up=10, out=15))]
    faint = merge({"body": {"l": (0, 0, -0.30), "r": (6, 0, 0)},
                   "leg_l1": {"r": (-80, 0, 0), "l": (0, 0, 0.30)}, "leg_r1": {"r": (-80, 0, 0), "l": (0, 0, 0.30)},
                   "leg_l2": {"r": (150, 0, 0)}, "leg_r2": {"r": (150, 0, 0)},
                   "neck1": {"r": (40, 0, 20)}, "neck2": {"r": (40, 0, 10)}, "head": {"r": (-20, 0, 20)},
                   "eyes": {"s": (1, 0.12, 1)}}, wings(up=-10, out=30))
    die = [merge({"body": {"r": (-12, 0, 0)}, "neck1": {"r": (-10, 0, 0)}, "eyes": {"s": 1.15}}, wings(up=40, out=50)),
           merge({"body": {"l": (0, 0, -0.08)}, "leg_l1": {"r": (-20, 0, 0), "l": (0, 0, 0.08)},
                  "leg_r1": {"r": (-20, 0, 0), "l": (0, 0, 0.08)}, "leg_l2": {"r": (40, 0, 0)},
                  "leg_r2": {"r": (40, 0, 0)}, "neck1": {"r": (20, 0, 0)}, "eyes": {"s": (1, 0.5, 1)}}, wings()),
           lerp_pose({}, faint, 0.6), faint, faint, faint]
    happy = [merge({"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)}, "neck1": {"r": (-10, 0, 0)},
                    "head": {"r": (-10, 0, 0)}, "eyes": {"s": (1, 0.35, 1)},
                    "leg_l2": {"r": (40 if z else 0, 0, 0)}, "leg_r2": {"r": (40 if z else 0, 0, 0)}},
                   wings(up=30 + 30 * S(i, 4), out=80)) for i, z in enumerate((0.0, 0.05, 0.06, 0.02))]
    sleep = [merge({"body": {"l": (0, 0, 0.004 * S(i, 4))},
                    "leg_r1": {"r": (-70, 0, 0)}, "leg_r2": {"r": (140, 0, 0)},
                    "neck1": {"r": (-50, 0, 0)}, "neck2": {"r": (-70, 0, 20)}, "head": {"r": (40, 0, 30)},
                    "eyes": {"s": (1, 0.12, 1)}}, wings(flap=2 * S(i, 4))) for i in range(4)]
    finish(arm, idle, walk, windup, attack, hit, die, happy, sleep)
    return arm


# =============================================================== Hỏa Tước
def build_hoa_tuoc():
    use_collection("COL_hoa_tuoc")
    red = material("MAT_ht_feather", (0.78, 0.33, 0.23), (0.78, 0.33, 0.23), ramp="red")
    red_dk = material("MAT_ht_feather_dark", (0.58, 0.19, 0.16), (0.58, 0.19, 0.16), ramp="red")
    belly = material("MAT_ht_belly", (0.90, 0.72, 0.23), (0.90, 0.72, 0.23), ramp="gold")
    beak = material("MAT_ht_beak", (0.73, 0.51, 0.10), (0.73, 0.51, 0.10), ramp="gold")
    fire = material("MAT_ht_flame", (1.0, 0.68, 0.23), (1.0, 0.68, 0.23), emit=4.0, glow="flame")
    fire["kit_halo"] = 1
    blush = material("MAT_ht_blush", (0.95, 0.72, 0.78), (0.95, 0.72, 0.78), ramp="pink")
    mats = eye_mats("ht", (0.42, 0.35, 0.28))

    arm = armature("hoa_tuoc", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("body", (0, 0, 0.06), (0, 0, 0.30), "root"),
        ("eyes", (0, -0.17, 0.28), (0, -0.17, 0.34), "body"),
        ("crest", (0, -0.03, 0.42), (0, 0.0, 0.55), "body"),
        ("tail", (0, 0.17, 0.24), (0, 0.30, 0.30), "body"),
        ("wing_l", (0.18, 0.0, 0.29), (0.23, 0.06, 0.18), "body"),
        ("wing_r", (-0.18, 0.0, 0.29), (-0.23, 0.06, 0.18), "body"),
        ("leg_l", (0.06, -0.02, 0.08), (0.06, -0.03, 0.0), "body"),
        ("leg_r", (-0.06, -0.02, 0.08), (-0.06, -0.03, 0.0), "body"),
        ("fireball", (0, -0.24, 0.27), (0, -0.34, 0.27), "body"),
    ])
    att(arm, "body", ball("ht_body", (0.20, 0.19, 0.19), (0, 0.0, 0.25), red),
        ball("ht_belly", (0.14, 0.08, 0.13), (0, -0.12, 0.21), belly),
        ball("ht_blushl", (0.03, 0.012, 0.02), (0.11, -0.15, 0.25), blush, seg=6, rings=4),
        ball("ht_blushr", (0.03, 0.012, 0.02), (-0.11, -0.15, 0.25), blush, seg=6, rings=4),
        aim("ht_beak", beak, (0, -0.18, 0.28), (0, -0.25, 0.265), 0.035, 0.0, seg=6))
    att(arm, "eyes", *cute_eyes("ht", 0.075, -0.165, 0.315, 0.04, mats))
    crest = []
    for k, (x, tilt) in enumerate(((0.0, 0.0), (0.05, 25), (-0.05, -25))):
        top = (x + 0.06 * math.sin(math.radians(tilt)), 0.02, 0.56 - abs(x))
        crest.append(aim(f"ht_crest{k}", red_dk, (x * 0.6, -0.03, 0.42), top, 0.035, 0.012, seg=6))
        crest.append(aim(f"ht_crestf{k}", fire, top, (top[0] * 1.2, top[1] + 0.03, top[2] + 0.06), 0.022, 0.0, seg=6))
    att(arm, "crest", *crest)
    tail = []
    for k, x in enumerate((-0.06, 0.0, 0.06)):
        end = (x * 1.6, 0.31, 0.33 + (0.04 if x == 0 else 0.0))
        tail.append(aim(f"ht_tail{k}", red_dk, (x * 0.4, 0.15, 0.25), end, 0.035, 0.015, seg=6))
        tail.append(aim(f"ht_tailf{k}", fire, end, (end[0] * 1.15, end[1] + 0.06, end[2] + 0.04), 0.022, 0.0, seg=6))
    att(arm, "tail", *tail)
    for s, b in ((1, "wing_l"), (-1, "wing_r")):
        att(arm, b, ball(f"ht_{b}", (0.04, 0.08, 0.1), (s * 0.19, 0.03, 0.24), red_dk, rot=(0, s * -20, 0)),
            aim(f"ht_{b}tip", fire, (s * 0.21, 0.08, 0.18), (s * 0.23, 0.12, 0.15), 0.02, 0.0, seg=5))
    for s, b in ((1, "leg_l"), (-1, "leg_r")):
        att(arm, b, *[aim(f"ht_{b}toe{k}", beak, (s * 0.06, -0.02, 0.05), (s * 0.06 + (k - 1) * 0.025, -0.07, 0.008), 0.014, 0.006, seg=4)
                      for k in range(3)])
    att(arm, "fireball", ball("ht_fireball", (0.07,) * 3, (0, -0.32, 0.27), fire, seg=10, rings=6),
        aim("ht_firetrail", fire, (0, -0.30, 0.27), (0, -0.20, 0.30), 0.05, 0.0, seg=6))

    off = {"fireball": {"s": 0.0}}
    idle = [merge(off, {"body": {"l": (0, 0, 0.006 * S(i, 4)), "s": (1, 1, 1 + 0.02 * S(i, 4))},
                        "crest": {"r": (6 * S(i, 4, 1), 0, 6 * S(i, 4, 2))}, "tail": {"r": (0, 0, 10 * S(i, 4))},
                        "eyes": {"s": (1, 0.2 if i == 2 else 1.0, 1)}}) for i in range(4)]
    walk = []
    for i in range(6):
        z = 0.04 * abs(S(i, 3))
        walk.append(merge(off, {"body": {"l": (0, 0, z), "r": (6, 0, 0)},
                                "leg_l": {"l": (0, 0, -z * 0.5)}, "leg_r": {"l": (0, 0, -z * 0.5)},
                                "wing_l": {"r": (0, -25 * abs(S(i, 3)), 0)}, "wing_r": {"r": (0, 25 * abs(S(i, 3)), 0)},
                                "crest": {"r": (-10 * abs(S(i, 3)), 0, 0)}, "tail": {"r": (10 * abs(S(i, 3)), 0, 0)}}))
    # windup: puffs itself up, crest flaring tall, wings out, rocking back
    puff = merge(off, {"body": {"s": (1.12, 1.1, 1.08), "r": (-12, 0, 0)}, "crest": {"s": 1.45, "r": (-10, 0, 0)},
                       "wing_l": {"r": (0, -45, 0)}, "wing_r": {"r": (0, 45, 0)}, "tail": {"s": 1.2, "r": (20, 0, 0)}})
    windup = [lerp_pose(idle[0], puff, 0.5), puff, merge(puff, {"crest": {"s": 1.55}}), merge(puff, {"crest": {"s": 1.5}})]
    # attack: spits a fireball straight ahead
    attack = [merge(puff, {"body": {"r": (4, 0, 0), "s": 1.0}, "fireball": {"s": 0.6, "l": (0, 0.03, 0.06)}}),
              merge(off, {"body": {"r": (6, 0, 0)}, "fireball": {"s": 1.0, "l": (0, -0.04, 0.10)},
                          "crest": {"r": (20, 0, 0)}, "wing_l": {"r": (0, -30, 0)}, "wing_r": {"r": (0, 30, 0)}}),
              merge(off, {"body": {"r": (2, 0, 0)}, "fireball": {"s": 0.6, "l": (0, -0.06, 0.12)}}),
              merge(off, {})]
    hit = [merge(off, {"body": {"s": (1.1, 1.0, 0.85), "r": (-14, 0, 8)}, "eyes": {"s": (1, 0.3, 1)},
                       "crest": {"r": (-20, 0, 10)}}),
           merge(off, {"body": {"s": (1.03, 1.0, 0.96), "r": (-5, 0, 3)}})]
    faint = merge(off, {"body": {"s": (1.12, 1.08, 0.72), "l": (0, 0, -0.01), "r": (0, 0, 12)},
                        "crest": {"s": 0.7, "r": (40, 0, 20)}, "eyes": {"s": (1, 0.12, 1)},
                        "wing_l": {"r": (0, 40, 0)}, "wing_r": {"r": (0, -40, 0)}, "tail": {"r": (-20, 0, 0)}})
    die = [merge(off, {"body": {"l": (0, 0, 0.03)}, "eyes": {"s": 1.2}, "crest": {"s": 1.2}}),
           merge(off, {"body": {"r": (0, 14, 0)}, "eyes": {"s": (1, 0.5, 1)}}),
           lerp_pose(off, faint, 0.6), faint, faint, faint]
    happy = [merge(off, {"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)}, "eyes": {"s": (1, 0.35, 1)},
                         "wing_l": {"r": (0, -70 - 20 * S(i, 4), 0)}, "wing_r": {"r": (0, 70 + 20 * S(i, 4), 0)},
                         "crest": {"s": 1.2}}) for i, z in enumerate((0.0, 0.06, 0.07, 0.02))]
    sleep = [merge(off, {"body": {"s": (1.06 + 0.02 * S(i, 4), 1.05, 0.95 + 0.02 * S(i, 4))}, "eyes": {"s": (1, 0.12, 1)},
                         "crest": {"s": 0.65, "r": (30, 0, 0)}, "tail": {"r": (-15, 0, 0)},
                         "wing_l": {"r": (0, 10, 0)}, "wing_r": {"r": (0, -10, 0)}}) for i in range(4)]
    finish(arm, idle, walk, windup, attack, hit, die, happy, sleep, scale=1.25)
    return arm


BEASTS = {
    "linh_ho": ("Linh Hồ", 48, build_linh_ho),
    "huyen_quy": ("Huyền Quy", 48, build_huyen_quy),
    "bach_hac": ("Bạch Hạc", 48, build_bach_hac),
    "hoa_tuoc": ("Hỏa Tước", 48, build_hoa_tuoc),
    "tieu_long": ("Tiểu Long", 48, build_tieu_long),
    "ky_lan_con": ("Kỳ Lân Con", 48, build_ky_lan_con),
}
