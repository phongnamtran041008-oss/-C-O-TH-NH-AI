"""Vân Điệp: a cloud butterfly (Lưu Vân Cốc, normal 48, hovers).

Runs inside Blender. Wide soft cloud-white wings (a rounded forewing and a swallowtailed
hindwing per side) with blue veins and a glowing cloud-curl spiral on each, a small furry
thorax, a round head with big dark eyes, curled antennae with glowing club tips, and a body
that thins into a trailing tail of mist. Drawn hovering above its ground pivot with a small
contact shadow, like Kiếm Linh.

Wings: one bone per wing, rotated about the body axis (flap) and about z (sweep); the
hindwings lag the forewings by a frame for follow-through. A `gust` bone carries a puff of
cloud that only exists on the attack's impact frames.

Clips: idle (slow wingbeats, body bobbing against them), walk (faster beats, tilted into
the flight), windup (rears back, wings raised high and swept back, held, the tail curling),
attack (a great downward clap of the wings throwing a gust of cloud forward = hit), hit
(knocked tumbling), die (flutters down and lies with its wings spread flat, the mist gone).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (hx, C, S, aim, armature, att, ball, hover_shadow, lerp_pose, material, merge,
                    plate, skin, tube, use_collection, write_clips)

TINY = 0.001
FORE = [(0.0, -0.03), (0.08, -0.11), (0.20, -0.185), (0.33, -0.21), (0.415, -0.165),
        (0.425, -0.085), (0.36, -0.005), (0.22, 0.03), (0.08, 0.035), (0.0, 0.02)]
HIND = [(0.0, 0.02), (0.12, 0.035), (0.24, 0.07), (0.29, 0.15), (0.25, 0.23), (0.215, 0.34),
        (0.17, 0.27), (0.10, 0.20), (0.04, 0.14), (0.0, 0.08)]
SH = Vector((0.0, 0.0, 0.575))          # wing root (both sides meet on the thorax)
REST_UP = 28.0                           # wings rest in a shallow V


def _frame(sx):
    """Wing axes at rest: s outward and up REST_UP degrees, t back along the body."""
    a = math.radians(REST_UP)
    return Vector((sx * math.cos(a), 0.0, math.sin(a))), Vector((0, 1, 0))


def _spiral(c, r0, turns, n=14):
    pts = []
    for k in range(n):
        u = k / (n - 1)
        ang = 0.5 + u * turns * 2 * math.pi
        r = r0 * (1 - 0.72 * u)
        pts.append((c[0] + r * math.cos(ang), c[1] + r * math.sin(ang)))
    return pts


def build_van_diep():
    use_collection("COL_van_diep")
    wing = material("MAT_vd_wing", hx("#cfcbd3"), hx("#f6b0c4"), ramp=("bone", "pink"))
    wing["kit_light"] = 0.5
    wing["kit_shadow"] = 0.02
    vein = material("MAT_vd_wing_vein", hx("#3c5e9c"), hx("#5c3690"), ramp=("blue", "purple"))
    curl = material("MAT_vd_curl", (0.35, 0.88, 0.96), (1.0, 0.89, 0.48), emit=3.0, glow=("spirit", "holy"))
    fur = material("MAT_vd_fur", hx("#9894a2"), hx("#c4688a"), ramp=("bone", "pink"))
    mist = material("MAT_vd_mist", (0.69, 0.86, 1.0), (0.78, 0.55, 1.0), emit=1.4, glow=("ice", "cosmic"))
    eye = material("MAT_vd_eye", hx("#1d1922"), hx("#1d1922"), ramp="hair")
    glint = material("MAT_vd_eye_glint", hx("#cfcbd3"), hx("#cfcbd3"), ramp="bone")
    tip = material("MAT_vd_antenna_tip", (0.35, 0.88, 0.96), (1.0, 0.89, 0.48), emit=4.0, glow=("spirit", "holy"))
    tip["kit_halo"] = 1
    stalk = material("MAT_vd_antenna", hx("#243a6a"), hx("#3a2160"), ramp=("blue", "purple"))

    arm = armature("van_diep", [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hover", (0, 0, 0.50), (0, 0, 0.60), "root"),
        ("body", (0, 0.0, 0.52), (0, -0.02, 0.62), "hover"),
        ("head", (0, -0.03, 0.62), (0, -0.05, 0.70), "body"),
        ("ant", (0, -0.05, 0.66), (0, -0.07, 0.74), "head"),
        ("abd", (0, 0.01, 0.53), (0, 0.06, 0.45), "body"),
        ("mist", (0, 0.06, 0.45), (0, 0.2, 0.375), "abd"),
        ("fw_l", tuple(SH + Vector((0.02, -0.01, 0))), tuple(SH + Vector((0.2, -0.01, 0))), "body"),
        ("hw_l", tuple(SH + Vector((0.02, 0.02, -0.01))), tuple(SH + Vector((0.2, 0.02, -0.01))), "body"),
        ("fw_r", tuple(SH + Vector((-0.02, -0.01, 0))), tuple(SH + Vector((-0.2, -0.01, 0))), "body"),
        ("hw_r", tuple(SH + Vector((-0.02, 0.02, -0.01))), tuple(SH + Vector((-0.2, 0.02, -0.01))), "body"),
        ("gust", (0, -0.24, 0.42), (0, -0.24, 0.52), "root"),
    ])

    # --- wings: plate, veins from the root, a glowing cloud-curl spiral
    for sx, side in ((1, "l"), (-1, "r")):
        u, v = _frame(sx)
        o = SH + Vector((sx * 0.02, 0, 0))

        def at(s, t, o=o, u=u, v=v):
            return tuple(o + u * s + v * t)
        fw = [plate(f"vd_fw{side}", FORE, wing, o, u, v, thick=0.012)]
        for k, (s, t) in enumerate(((0.40, -0.15), (0.33, -0.03), (0.22, -0.17))):
            fw.append(aim(f"vd_fv{side}{k}", vein, at(0.02, -0.0), at(s, t), 0.011, 0.007, seg=5))
        fw += [aim(f"vd_fc{side}{k}", curl, at(*p), at(*q), 0.0135, 0.0135, seg=5)
               for k, (p, q) in enumerate(zip(_spiral((0.27, -0.11), 0.075, 1.15)[:-1],
                                              _spiral((0.27, -0.11), 0.075, 1.15)[1:]))]
        att(arm, f"fw_{side}", *fw)
        hw = [plate(f"vd_hw{side}", HIND, wing, o + v * 0.015 - Vector((0, 0, 0.004)), u, v, thick=0.012)]
        for k, (s, t) in enumerate(((0.27, 0.16), (0.21, 0.31))):
            hw.append(aim(f"vd_hv{side}{k}", vein, at(0.02, 0.05), at(s, t), 0.011, 0.007, seg=5))
        sp = _spiral((0.17, 0.13), 0.05, 1.0, n=10)
        hw += [aim(f"vd_hc{side}{k}", curl, at(*sp[k]), at(*sp[k + 1]), 0.0135, 0.0135, seg=5)
               for k in range(len(sp) - 1)]
        att(arm, f"hw_{side}", *hw)

    # --- body: furry thorax, round head with big dark eyes, curled antennae
    att(arm, "body", ball("vd_thorax", (0.052, 0.06, 0.06), (0, 0.0, 0.565), fur),
        ball("vd_collar", (0.045, 0.04, 0.03), (0, -0.03, 0.605), mist, seg=10, rings=6))
    att(arm, "head", ball("vd_head", (0.062, 0.058, 0.06), (0, -0.05, 0.655), fur),
        *[ball(f"vd_eye{s}", (0.036, 0.028, 0.04), (s * 0.04, -0.088, 0.66), eye, seg=10, rings=6)
          for s in (-1, 1)],
        *[ball(f"vd_eye_glint{s}", (0.014, 0.008, 0.014), (s * 0.034, -0.118, 0.675), glint, seg=6, rings=4)
          for s in (-1, 1)])
    ants = []
    for s in (-1, 1):
        pts = [(s * 0.02, -0.08, 0.70), (s * 0.045, -0.105, 0.77), (s * 0.08, -0.115, 0.84),
               (s * 0.115, -0.095, 0.875)]
        ants.append(tube(f"vd_ant{s}", pts, [0.009, 0.008, 0.008, 0.008], stalk, seg=6, up=(0, 0, 1)))
        ants.append(ball(f"vd_antip{s}", (0.022, 0.022, 0.022), pts[-1], tip, seg=8, rings=5))
    att(arm, "ant", *ants)
    # the body thins into a tail of mist
    ab = tube("vd_abd", [(0, 0.0, 0.54), (0, 0.03, 0.49), (0, 0.06, 0.45), (0, 0.10, 0.41),
                         (0, 0.15, 0.385), (0, 0.20, 0.375)],
              [0.04, 0.036, 0.03, 0.022, 0.012, 0.004], mist, seg=10, up=(0, -1, 0))
    skin(ab, arm, ["body", "abd", "mist"], power=3)

    # --- the gust of cloud thrown by the wing clap (exists only on the impact frames)
    g = [ball("vd_gust1", (0.08, 0.06, 0.06), (0, -0.26, 0.44), mist, seg=10, rings=6),
         ball("vd_gust2", (0.06, 0.05, 0.05), (0.08, -0.22, 0.47), mist, seg=10, rings=6),
         ball("vd_gust3", (0.06, 0.05, 0.05), (-0.08, -0.22, 0.47), mist, seg=10, rings=6)]
    sp = _spiral((0.0, 0.46), 0.06, 1.0, n=10)
    g += [aim(f"vd_gustcurl{k}", curl, (sp[k][0], -0.30, sp[k][1]), (sp[k + 1][0], -0.30, sp[k + 1][1]),
              0.0135, 0.0135, seg=5) for k in range(len(sp) - 1)]
    att(arm, "gust", *g)
    hover_shadow("vd_shadow", 0.11, 0.08, arm)
    _clips(arm)
    return arm


def wings(fore, hind=None, sweep=0.0, hsweep=None, twist=0.0):
    """Flap angles (deg up from the rest V) for both sides; sweep > 0 swings them back;
    twist > 0 turns the wing faces forward (trailing edge up), toward the target."""
    hind = fore if hind is None else hind
    hsweep = sweep if hsweep is None else hsweep
    return {"fw_l": {"r": (twist, -fore, sweep)}, "fw_r": {"r": (twist, fore, -sweep)},
            "hw_l": {"r": (twist, -hind, hsweep)}, "hw_r": {"r": (twist, hind, -hsweep)}}


def _clips(arm):
    off = {"gust": {"s": TINY}}
    beat4 = [22, 4, -20, 2]                   # up, coming down, down, coming up
    idle = []
    for i in range(4):
        p = merge(off, wings(beat4[i], beat4[i - 1]))
        p.update({"hover": {"l": (0, 0, 0.025 * -math.sin(math.radians(beat4[i])) + 0.01)},
                  "body": {"r": (-4 + 3 * S(i, 4), 0, 0)},
                  "abd": {"r": (6 * S(i, 4, -1.0), 0, 0)}, "mist": {"r": (10 * S(i, 4, -1.8), 0, 8 * C(i, 4))},
                  "ant": {"r": (6 * S(i, 4, -1.2), 0, 0)}})
        idle.append(p)
    beat6 = [26, 14, -6, -24, -12, 12]
    walk = []
    for i in range(6):
        p = merge(off, wings(beat6[i], beat6[i - 1], sweep=6))
        p.update({"hover": {"l": (0, 0, 0.03 * -math.sin(math.radians(beat6[i])) + 0.015)},
                  "body": {"r": (14, 0, 0)},
                  "abd": {"r": (-18 + 6 * S(i, 6, -1), 0, 0)}, "mist": {"r": (-14 + 10 * S(i, 6, -1.8), 0, 8 * S(i, 6))},
                  "ant": {"r": (14, 0, 0)}})
        walk.append(p)

    # windup: rears back, wings thrown high and swept back (a drawn bow), the tail curling
    # forward under it, antennae pointing at the target - held
    # (a threat display: wings opened flat and turned to face the target, the glowing
    # curls held up like a pair of great eyes, body reared back, antennae forward)
    rear = merge(off, wings(-16, -22, sweep=-6, hsweep=4, twist=60))
    rear.update({"hover": {"l": (0, 0.04, 0.06)}, "body": {"r": (-14, 0, 0)},
                 "abd": {"r": (-24, 0, 0)}, "mist": {"r": (-24, 0, 0)}, "ant": {"r": (44, 0, 0)}})
    windup = [lerp_pose(idle[0], rear, 0.5), rear,
              merge(rear, wings(-18, -24, sweep=-7, hsweep=3, twist=63)),
              merge(rear, wings(-15, -21, sweep=-5, hsweep=5, twist=58))]
    windup[0]["gust"] = {"s": TINY}

    # attack: a great downward clap, wings sweeping forward, body pitching into it and a
    # gust of cloud thrown ahead (f1 = hit), the gust drifting on (f2), recovering (f3)
    clap = merge(wings(-40, -28, sweep=-20, hsweep=-12),
                 {"hover": {"l": (0, -0.05, 0.06)}, "body": {"r": (22, 0, 0)},
                  "abd": {"r": (20, 0, 0)}, "mist": {"r": (24, 0, 0)}, "ant": {"r": (-20, 0, 0)},
                  "gust": {"s": 1.0, "l": (0, -0.02, 0)}})
    attack = [merge(merge(off, wings(44, 50, sweep=4, hsweep=16)),
                    {"hover": {"l": (0, -0.02, 0.06)}, "body": {"r": (6, 0, 0)}, "abd": {"r": (0, 0, 0)}}),
              clap,
              merge(clap, merge(wings(-30, -38, sweep=-12, hsweep=-18),
                                {"gust": {"s": 1.35, "l": (0, -0.07, 0.03)}, "hover": {"l": (0, -0.04, 0.04)}})),
              merge(off, merge(wings(14, -6), {"hover": {"l": (0, -0.01, 0.02)}, "body": {"r": (6, 0, 0)}}))]

    hit = [merge(off, merge(wings(58, 70, sweep=-10, hsweep=-14),
                            {"hover": {"l": (0, 0.06, 0.03)}, "body": {"r": (-34, 0, 12)},
                             "abd": {"r": (30, 0, 0)}, "mist": {"r": (20, 0, 0)}, "ant": {"r": (-30, 0, 0)}})),
           merge(off, merge(wings(20, 36),
                            {"hover": {"l": (0, 0.03, 0.015)}, "body": {"r": (-12, 0, 4)},
                             "abd": {"r": (10, 0, 0)}}))]

    die = [hit[0],
           merge(off, merge(wings(-10, 10, sweep=-6), {"hover": {"l": (0, 0.03, -0.12)}, "body": {"r": (-20, 0, 20)},
                                                       "abd": {"r": (20, 0, 0)}, "ant": {"r": (-20, 0, 0)}})),
           merge(off, merge(wings(30, 20), {"hover": {"l": (0, 0.02, -0.28)}, "body": {"r": (10, 0, -16)},
                                            "abd": {"r": (10, 0, 0)}, "mist": {"s": 0.7}})),
           merge(off, merge(wings(30, 20), {"hover": {"l": (0, 0.0, -0.44)}, "body": {"r": (20, 0, 10)},
                                              "abd": {"r": (20, 0, 0)}, "mist": {"s": 0.4}, "ant": {"r": (30, 0, 0)}})),
           merge(off, merge(wings(58, 52), {"hover": {"l": (0, 0.0, -0.475)}, "body": {"r": (6, 0, 4)},
                                              "abd": {"r": (10, 0, 0)}, "mist": {"s": 0.15}, "ant": {"r": (40, 0, 0)}})),
           merge(off, merge(wings(60, 54), {"hover": {"l": (0, 0.0, -0.48)}, "body": {"r": (4, 0, 4)},
                                              "abd": {"r": (10, 0, 0)}, "mist": {"s": TINY}, "ant": {"r": (50, 0, 0)}}))]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
