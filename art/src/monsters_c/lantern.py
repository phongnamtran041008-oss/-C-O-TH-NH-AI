"""U Minh Đăng: a ghost lantern (Vạn Tượng Trạch, normal 48, hovers).

Runs inside Blender. An old paper lantern come alive: a round paper body with dark ribs and
lacquered caps, a ring on top, a torn patch, a face burning through the paper (two slanted
eyes and a jagged grin, lit by the pale ghost flame inside), a pale flame curling out of the
top, three red tassels with gold beads hanging from the bottom cap, and a wisp of a tail.
Drawn hovering above its ground pivot with a small contact shadow.

Clips: idle (bobs, sways, tassels and wisp lag, the flame flickers), walk (drifts tilted
in, tassels and flame streaming back), windup (draws a breath: swells, tilts back, the
flame sucked down small and hard, eyes narrowed - held), attack (lunges, the grin gapes and
the flame flares out in a burst of ghost fire = hit), hit (knocked, the flame gutters), die
(the flame gutters out, the eyes go dark and the lantern drops and rolls onto its side).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (hx, C, S, aim, armature, att, ball, cone, hover_shadow, lerp_pose, material,
                    merge, plate, skin, tube, use_collection, write_clips)

TINY = 0.001
LC = Vector((0, 0, 0.60))       # lantern centre
LR = (0.15, 0.15, 0.155)         # its radii


def _ring(name, z, mat, r=0.011, grow=1.0):
    dz = (z - LC.z) / LR[2]
    rad = LR[0] * math.sqrt(max(0.0, 1 - dz * dz)) * grow
    pts = [(rad * math.cos(2 * math.pi * k / 16), rad * math.sin(2 * math.pi * k / 16), z) for k in range(17)]
    return tube(name, pts, [r] * 17, mat, seg=6, up=(0, 0, 1))


def build_u_minh_dang():
    use_collection("COL_u_minh_dang")
    paper = material("MAT_um_paper", hx("#ead9b0"), hx("#5c3690"), ramp=("paper", "purple"))
    rib = material("MAT_um_rib", hx("#573420"), hx("#1d1922"), ramp=("wood", "hair"))
    cap = material("MAT_um_cap", hx("#2e2834"), hx("#1d1922"), ramp="hair")
    tear = material("MAT_um_tear", hx("#1d1922"), hx("#1d1922"), ramp="hair")
    face = material("MAT_um_face", (0.35, 0.88, 0.96), (0.48, 0.93, 0.60), emit=5.0, glow=("spirit", "verdant"))
    face["kit_priority"] = 3.0
    face["kit_halo"] = 0
    flame = material("MAT_um_flame", (0.69, 0.86, 1.0), (0.48, 0.93, 0.60), emit=3.0, glow=("ice", "verdant"))
    core = material("MAT_um_flame_core", (0.35, 0.88, 0.96), (0.89, 1.0, 0.91), emit=6.0, glow=("spirit", "verdant"))
    cord = material("MAT_um_cord", hx("#94302a"), hx("#b9821a"), ramp=("red", "gold"))
    bead = material("MAT_um_bead", hx("#e6b83a"), hx("#94302a"), ramp=("gold", "red"), metal=True)
    wisp_m = material("MAT_um_wisp", (0.69, 0.86, 1.0), (0.48, 0.93, 0.60), emit=1.3, glow=("ice", "verdant"))

    tas = [("tas_l", (0.085, -0.05)), ("tas_r", (-0.085, -0.05)), ("tas_b", (0.0, 0.09))]
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("hover", (0, 0, 0.50), (0, 0, 0.60), "root"),
        ("lantern", tuple(LC), tuple(LC + Vector((0, 0, 0.15))), "hover"),
        ("flame", (0, 0, 0.75), (0, 0, 0.86), "lantern"),
        ("eyes", (0, -0.16, 0.64), (0, -0.16, 0.70), "lantern"),
        ("mouth", (0, -0.16, 0.565), (0, -0.16, 0.62), "lantern"),
        ("burst", (0, -0.26, 0.60), (0, -0.26, 0.70), "lantern"),
        ("wisp1", (0, 0.0, 0.46), (0, 0.04, 0.36), "lantern"),
        ("wisp2", (0, 0.04, 0.36), (0, 0.12, 0.27), "wisp1"),
    ]
    for name, (x, y) in tas:
        bones.append((name, (x, y, 0.45), (x, y, 0.37), "lantern"))
    arm = armature("u_minh_dang", bones)

    # --- the lantern: paper, ribs, caps, ring, a torn patch
    body = [ball("um_paper", LR, tuple(LC), paper, seg=18, rings=12),
            *[_ring(f"um_rib{k}", z, rib) for k, z in enumerate((0.515, 0.555, 0.645, 0.685))],
            cone("um_cap_top", 0.10, 0.075, 0.045, (0, 0, 0.745), cap, seg=14),
            cone("um_cap_bot", 0.075, 0.10, 0.045, (0, 0, 0.455), cap, seg=14),
            cone("um_rim_top", 0.105, 0.105, 0.012, (0, 0, 0.725), rib, seg=14),
            cone("um_rim_bot", 0.105, 0.105, 0.012, (0, 0, 0.475), rib, seg=14)]
    ring = [(0.04 * math.cos(math.pi * k / 8), 0.0, 0.77 + 0.045 * math.sin(math.pi * k / 8)) for k in range(9)]
    body.append(tube("um_ring", ring, [0.01] * 9, cap, seg=6, up=(0, -1, 0)))
    body.append(plate("um_tear", [(-0.03, 0.0), (0.02, 0.02), (0.035, -0.02), (0.01, -0.05), (-0.025, -0.035)],
                      tear, (0.128, 0.06, 0.63), (-0.3, 1, 0), (0, 0, 1), thick=0.02))
    att(arm, "lantern", *body)
    # --- the face burning through the paper: slanted eyes, a jagged grin
    eyes = []
    for sx in (-1, 1):
        # slanted down toward the middle: an angry glare
        pts = [(x * sx, z) for x, z in ((-0.026, -0.014), (0.026, -0.014), (0.028, 0.024), (-0.026, 0.004))]
        eyes.append(plate(f"um_eye{sx}", pts, face, (sx * 0.06, -0.146, 0.645), (1, 0.4 * sx, 0), (0, 0, 1),
                          thick=0.02))
    att(arm, "eyes", *eyes)
    grin = [(-0.07, 0.01), (-0.045, -0.012), (-0.022, 0.004), (0.0, -0.014), (0.022, 0.004), (0.045, -0.012),
            (0.07, 0.01), (0.05, -0.036), (0.0, -0.05), (-0.05, -0.036)]
    att(arm, "mouth", plate("um_mouth", grin, face, (0, -0.148, 0.575), (1, 0, 0), (0, 0, 1), thick=0.02))
    # --- the pale ghost flame curling out of the top
    fl = tube("um_flame_tube", [(0, 0, 0.75), (0, -0.005, 0.79), (0, 0.01, 0.835), (0.012, 0.04, 0.875),
                                (0.02, 0.075, 0.9), (0.012, 0.1, 0.93)],
              [0.058, 0.055, 0.04, 0.026, 0.014, 0.004], flame, seg=10, up=(0, -1, 0))
    att(arm, "flame", fl, ball("um_flame_core", (0.028, 0.028, 0.034), (0, 0, 0.79), core, seg=8, rings=6))
    # --- a burst of ghost fire breathed out on the attack (scaled away otherwise)
    att(arm, "burst", ball("um_burst1", (0.06, 0.05, 0.055), (0, -0.25, 0.60), flame, seg=10, rings=6),
        ball("um_burst2", (0.045, 0.04, 0.042), (0.05, -0.32, 0.64), flame, seg=10, rings=6),
        ball("um_burst3", (0.04, 0.035, 0.038), (-0.05, -0.33, 0.56), flame, seg=10, rings=6),
        ball("um_burst_core", (0.03, 0.03, 0.03), (0, -0.26, 0.60), core, seg=8, rings=5))
    # --- tassels: cord, gold bead, flared red tassel
    for name, (x, y) in tas:
        att(arm, name, aim(f"um_{name}_cord", cord, (x, y, 0.45), (x, y, 0.40), 0.01, 0.01, seg=5),
            ball(f"um_{name}_bead", (0.024, 0.024, 0.024), (x, y, 0.395), bead, seg=8, rings=5),
            aim(f"um_{name}_tuft", cord, (x, y, 0.38), (x, y, 0.285), 0.016, 0.036, seg=6))
    # --- a wisp of a tail
    w = tube("um_wisp", [(0, 0, 0.47), (0, 0.025, 0.40), (0, 0.065, 0.33), (0, 0.12, 0.28), (0, 0.17, 0.255)],
             [0.06, 0.05, 0.033, 0.016, 0.004], wisp_m, seg=10, up=(0, -1, 0))
    skin(w, arm, ["lantern", "wisp1", "wisp2"], power=3)
    hover_shadow("um_shadow", 0.11, 0.085, arm)
    _clips(arm)
    return arm


def _clips(arm):
    off = {"burst": {"s": TINY}}

    def tassels(i, n, amp=8.0, back=0.0, side=0.0):
        out = {}
        for k, name in enumerate(("tas_l", "tas_r", "tas_b")):
            out[name] = {"r": (back + amp * S(i, n, -1.2 - 0.4 * k), side + amp * 0.7 * C(i, n, -1.4 - 0.3 * k), 0)}
        return out

    idle = []
    for i in range(4):
        p = dict(off)
        p.update({"hover": {"l": (0, 0, 0.025 * S(i, 4))},
                  "lantern": {"r": (2 * S(i, 4, 0.5), 5 * S(i, 4, -0.4), 0)},
                  "flame": {"r": (6 * S(i, 4, -0.9), 4 * C(i, 4, -1.1), 0), "s": (1.0, 1.0 + 0.12 * S(i, 4, 1.0), 1.0)},
                  "wisp1": {"r": (8 + 6 * S(i, 4, -1.0), 0, 10 * S(i, 4, -1.0))},
                  "wisp2": {"r": (10 + 8 * S(i, 4, -1.8), 0, 18 * S(i, 4, -1.8))}})
        p.update(tassels(i, 4))
        idle.append(p)
    walk = []
    for i in range(6):
        p = dict(off)
        p.update({"hover": {"l": (0, 0, 0.03 * S(i, 6))},
                  "lantern": {"r": (10, 4 * S(i, 6), 0)},
                  "flame": {"r": (-28 + 6 * S(i, 6, -0.9), 4 * C(i, 6), 0), "s": (1.0, 1.0 + 0.1 * S(i, 6, 1.0), 1.0)},
                  "wisp1": {"r": (30 + 4 * S(i, 6, -1.0), 0, 8 * S(i, 6, -1.0))},
                  "wisp2": {"r": (24 + 6 * S(i, 6, -1.8), 0, 14 * S(i, 6, -1.8))}})
        p.update(tassels(i, 6, amp=6, back=28))
        walk.append(p)

    # windup: draws a breath - swells, tilts back, the flame sucked down small and hard,
    # eyes narrowed to slits, tassels flaring out - held
    breath = dict(off)
    breath.update({"hover": {"l": (0, 0.04, 0.05)}, "lantern": {"r": (-14, 0, 0), "s": 1.12},
                   "flame": {"s": (0.75, 0.45, 0.75)}, "eyes": {"s": (1.15, 0.45, 1.0)},
                   "mouth": {"s": (0.8, 0.6, 1.0)},
                   "wisp1": {"r": (-20, 0, 20)}, "wisp2": {"r": (-26, 0, 30)},
                   "tas_l": {"r": (-20, -30, 0)}, "tas_r": {"r": (-20, 30, 0)}, "tas_b": {"r": (30, 0, 0)}})
    windup = [lerp_pose(idle[0], breath, 0.5), breath,
              merge(breath, {"lantern": {"r": (-15, 3, 0), "s": 1.14}, "hover": {"l": (0.005, 0.04, 0.055)}}),
              merge(breath, {"lantern": {"r": (-15, -3, 0), "s": 1.13}, "hover": {"l": (-0.005, 0.04, 0.05)}})]
    windup[0]["burst"] = {"s": TINY}

    # attack: lunges, the grin gapes and the flame flares out forward in a burst of ghost
    # fire (f1 = hit), the fire drifts on (f2), it settles (f3)
    flare = {"hover": {"l": (0, -0.06, 0.02)}, "lantern": {"r": (16, 0, 0), "s": 1.0},
             "flame": {"r": (55, 0, 0), "s": (1.6, 1.9, 1.6)}, "eyes": {"s": (1.2, 1.3, 1.0)},
             "mouth": {"s": (1.25, 2.2, 1.0)}, "burst": {"s": 1.0},
             "wisp1": {"r": (40, 0, 0)}, "wisp2": {"r": (30, 0, 0)},
             "tas_l": {"r": (40, 0, 0)}, "tas_r": {"r": (40, 0, 0)}, "tas_b": {"r": (50, 0, 0)}}
    attack = [merge(off, {"hover": {"l": (0, -0.03, 0.03)}, "lantern": {"r": (8, 0, 0)},
                          "flame": {"r": (20, 0, 0), "s": (1.2, 1.5, 1.2)}, "mouth": {"s": (1.1, 1.6, 1.0)},
                          "tas_l": {"r": (20, 0, 0)}, "tas_r": {"r": (20, 0, 0)}, "tas_b": {"r": (24, 0, 0)}}),
              flare,
              merge(flare, {"burst": {"s": 1.3, "l": (0, -0.06, 0.02)}, "flame": {"r": (30, 0, 0), "s": (1.3, 1.6, 1.3)},
                            "mouth": {"s": (1.15, 1.6, 1.0)}, "tas_b": {"r": (30, 0, 0)}}),
              merge(off, lerp_pose(flare, idle[0], 0.7))]
    attack[3]["burst"] = {"s": TINY}

    hit = [merge(off, {"hover": {"l": (0, 0.06, 0.02)}, "lantern": {"r": (-26, 10, 0)},
                       "flame": {"r": (-40, 0, 20), "s": (0.8, 0.5, 0.8)}, "eyes": {"s": (1.0, 0.3, 1.0)},
                       "mouth": {"s": (0.9, 0.5, 1.0)},
                       "tas_l": {"r": (-40, 0, 0)}, "tas_r": {"r": (-40, 0, 0)}, "tas_b": {"r": (-30, 0, 0)},
                       "wisp1": {"r": (-20, 0, 0)}}),
           merge(off, {"hover": {"l": (0, 0.025, 0.01)}, "lantern": {"r": (-8, 4, 0)},
                       "flame": {"r": (14, 0, -6), "s": (0.95, 0.85, 0.95)},
                       "tas_l": {"r": (20, 0, 0)}, "tas_r": {"r": (20, 0, 0)}, "tas_b": {"r": (16, 0, 0)}})]

    # die: the flame gutters out, the eyes go dark, the lantern drops and rolls onto its
    # side on the ground
    die = [merge(off, {"hover": {"l": (0, 0.04, 0.02)}, "lantern": {"r": (-20, 0, 0)},
                       "flame": {"s": (0.8, 0.55, 0.8), "r": (-20, 0, 0)}, "eyes": {"s": (1.0, 1.2, 1.0)},
                       "mouth": {"s": (1.0, 1.6, 1.0)}}),
           merge(off, {"hover": {"l": (0, 0.02, -0.06)}, "lantern": {"r": (10, 8, 0)},
                       "flame": {"s": (0.5, 0.35, 0.5)}, "eyes": {"s": (1.0, 0.6, 1.0)},
                       "tas_l": {"r": (-20, 0, 0)}, "tas_r": {"r": (-20, 0, 0)}}),
           merge(off, {"hover": {"l": (0, 0.0, -0.22)}, "lantern": {"r": (20, 30, 0)},
                       "flame": {"s": (0.3, 0.2, 0.3)}, "eyes": {"s": (1.0, 0.3, 1.0)},
                       "wisp1": {"s": 0.5}, "tas_l": {"r": (-50, 0, 0)}, "tas_r": {"r": (-40, 0, 0)},
                       "tas_b": {"r": (-50, 0, 0)}}),
           merge(off, {"hover": {"l": (0, 0.0, -0.40)}, "lantern": {"r": (10, 70, 0)},
                       "flame": {"s": TINY}, "eyes": {"s": (1.0, 0.1, 1.0)}, "mouth": {"s": (1.0, 0.4, 1.0)},
                       "wisp1": {"s": 0.2}, "tas_l": {"r": (0, -40, 0)}, "tas_r": {"r": (0, -60, 0)}}),
           merge(off, {"hover": {"l": (0, 0.0, -0.44)}, "lantern": {"r": (6, 90, 0)},
                       "flame": {"s": TINY}, "eyes": {"s": TINY}, "mouth": {"s": TINY},
                       "wisp1": {"s": TINY}, "tas_l": {"r": (60, 0, 0), "s": 0.5}, "tas_r": {"r": (60, 0, 0), "s": 0.5},
                       "tas_b": {"r": (50, 0, 0), "s": 0.5}}),
           merge(off, {"hover": {"l": (0, 0.0, -0.44)}, "lantern": {"r": (4, 92, 0)},
                       "flame": {"s": TINY}, "eyes": {"s": TINY}, "mouth": {"s": TINY},
                       "wisp1": {"s": TINY}, "tas_l": {"r": (62, 0, 0), "s": 0.5}, "tas_r": {"r": (62, 0, 0), "s": 0.5},
                       "tas_b": {"r": (52, 0, 0), "s": 0.5}})]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
