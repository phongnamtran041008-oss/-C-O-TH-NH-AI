"""Thảo Nhân (normal, 48): a straw archery dummy of the archery grassland, come alive.

A bundle of straw bound with rope at the waist and neck, a frayed straw skirt, standing on a
single wooden pole-leg. A painted target (white and red rings) on its chest with arrows stuck
in it and in its shoulder and hat. Straw arms bundled round a crossbar, frayed straw hands. A
sackcloth face with two glowing eyes and a stitched grin; a patched conical straw hat.

Rig: root, hop (everything but the ground shadow), body, head, hat, two two-bone arms.
It hops on its pole: a flat contact shadow parented to the armature object stays on the
ground and keeps the sprite's lowest row on the pivot (as Kiếm Linh's does), so the hop can
leave the ground. Clips: idle wobbles on the pole; walk is a hop with the arms flailing up at
the top and the straw squashing on landing; windup leans back, squats on its pole and throws
both arms up and wide; attack springs forward and slaps both arms down (hit frame 1); die:
the hat flies off, the body slides down its pole and keels over into a heap.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import S, att, six
from rig import aim, armature, ball, box, cone, lerp_pose, material, merge, shadow, shadow_material, use_collection

SC = 1.1


def arrow(name, tip, direction, length, shaft, feather, head):
    """An arrow stuck at `tip` (its point buried), shaft leaving along `direction`."""
    t = Vector(tip)
    d = Vector(direction).normalized()
    end = t + d * length
    side = d.cross(Vector((0, 0, 1)))
    if side.length < 1e-3:
        side = Vector((1, 0, 0))
    side.normalize()
    up = side.cross(d)
    return [aim(f"{name}_shaft", shaft, tuple(t - d * 0.02), tuple(end), 0.014, 0.014, seg=5),
            box(f"{name}_f1", (0.012, 0.012, 0.012), tuple(end), head),
            aim(f"{name}_fl", feather, tuple(end - d * 0.055 + side * 0.004), tuple(end + side * 0.03), 0.018, 0.0, seg=4),
            aim(f"{name}_fr", feather, tuple(end - d * 0.055 - side * 0.004), tuple(end - side * 0.03), 0.018, 0.0, seg=4),
            aim(f"{name}_fu", feather, tuple(end - d * 0.055), tuple(end + up * 0.03), 0.018, 0.0, seg=4)]


def build():
    use_collection("COL_thao_nhan")
    straw = material("MAT_tn_straw", (0.73, 0.51, 0.10), (0.27, 0.24, 0.30), ramp=("gold", "hair"))
    straw_dk = material("MAT_tn_straw_dark", (0.48, 0.30, 0.05), (0.18, 0.16, 0.20), ramp=("gold", "hair"))
    rope = material("MAT_tn_rope", (0.51, 0.32, 0.18), (0.58, 0.19, 0.16), ramp=("wood", "red"))
    pole = material("MAT_tn_pole", (0.34, 0.20, 0.13), (0.27, 0.24, 0.30), ramp=("wood", "hair"))
    ring_w = material("MAT_tn_target_white", (0.93, 0.87, 0.70), (0.81, 0.80, 0.83), ramp=("paper", "bone"))
    ring_r = material("MAT_tn_target_red", (0.58, 0.19, 0.16), (0.36, 0.21, 0.56), ramp=("red", "purple"))
    ring_r["kit_priority"] = 2.0
    cloth = material("MAT_tn_cloth", (0.77, 0.68, 0.52), (0.53, 0.56, 0.60), ramp=("paper", "stone"))
    eye = material("MAT_tn_eye", (1.0, 0.68, 0.23), (0.78, 0.55, 1.0), emit=6.0, glow=("flame", "cosmic"))
    stitch = material("MAT_tn_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    hat = material("MAT_tn_hat", (0.42, 0.35, 0.28), (0.36, 0.10, 0.11), ramp=("earth", "red"))
    patch = material("MAT_tn_patch", (0.24, 0.37, 0.61), (0.58, 0.19, 0.16), ramp=("blue", "red"))
    shaft = material("MAT_tn_shaft", (0.68, 0.48, 0.28), (0.68, 0.48, 0.28), ramp="wood")
    feather = material("MAT_tn_feather", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")
    head_m = material("MAT_tn_arrowhead", (0.58, 0.65, 0.73), (0.58, 0.65, 0.73), ramp="steel", metal=True)
    shade = shadow_material("MAT_tn_shadow")

    AZ = 0.53
    arm = armature("thao_nhan", [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("hop", (0, 0, 0.0), (0, 0, 0.12), "root"),
        ("body", (0, 0, 0.27), (0, 0, 0.58), "hop"),
        ("head", (0, 0, 0.58), (0, 0, 0.76), "body"),
        ("hat", (0, 0, 0.77), (0, 0, 0.87), "head"),
        ("arm_l", (0.07, 0, AZ), (0.18, 0, AZ - 0.02), "body"),
        ("hand_l", (0.18, 0, AZ - 0.02), (0.29, 0, AZ - 0.06), "arm_l"),
        ("arm_r", (-0.07, 0, AZ), (-0.18, 0, AZ - 0.02), "body"),
        ("hand_r", (-0.18, 0, AZ - 0.02), (-0.29, 0, AZ - 0.06), "arm_r"),
    ])
    shadow("tn_shadow", 0.10, 0.08, shade, arm)

    # pole-leg: a wooden stake, pointed at the foot
    att(arm, "hop", aim("tn_pole", pole, (0, 0, 0.03), (0, 0, 0.30), 0.024, 0.022, seg=8),
        aim("tn_poletip", pole, (0, 0, 0.035), (0, 0, 0.0), 0.024, 0.006, seg=8))
    # straw torso, frayed skirt, rope bands, the target and its arrows
    body = [cone("tn_torso", 0.105, 0.115, 0.26, (0, 0, 0.42), straw, seg=14),
            cone("tn_skirt", 0.14, 0.10, 0.07, (0, 0, 0.285), straw_dk, seg=14),
            cone("tn_waist", 0.112, 0.112, 0.025, (0, 0, 0.32), rope, seg=14),
            cone("tn_neck", 0.10, 0.10, 0.022, (0, 0, 0.56), rope, seg=14),
            cone("tn_bar", 0.018, 0.018, 0.50, (0, 0.02, AZ), pole, rot=(0, 90, 0), seg=6)]
    for k in range(9):
        a = math.tau * k / 9 + 0.2
        body.append(aim(f"tn_fray{k}", straw_dk if k % 2 else straw, (0.10 * math.cos(a), 0.10 * math.sin(a), 0.28),
                        (0.17 * math.cos(a), 0.17 * math.sin(a), 0.215), 0.022, 0.0, seg=4))
    for k in range(4):
        a = math.tau * (k + 0.5) / 4 + math.pi / 4
        body.append(box(f"tn_ridge{k}", (0.016, 0.016, 0.20), (0.112 * math.cos(a), 0.112 * math.sin(a), 0.44), straw_dk,
                        rot=(0, 0, math.degrees(a))))
    for k, (r, m) in enumerate(((0.085, ring_w), (0.064, ring_r), (0.043, ring_w), (0.022, ring_r))):
        body.append(cone(f"tn_ring{k}", r, r, 0.012 + 0.006 * k, (0, -0.112 - 0.004 * k, 0.43), m, rot=(90, 0, 0), seg=18))
    body += arrow("tn_arrow1", (0.025, -0.13, 0.44), (0.35, -1.0, 0.25), 0.16, shaft, feather, head_m)
    body += arrow("tn_arrow2", (-0.05, -0.12, 0.40), (-0.45, -1.0, -0.15), 0.14, shaft, feather, head_m)
    body += arrow("tn_arrow3", (-0.09, 0.03, 0.52), (-0.6, 0.5, 0.6), 0.14, shaft, feather, head_m)
    att(arm, "body", *body)

    # head: straw ball, sackcloth face, glowing eyes, stitched grin
    att(arm, "head", ball("tn_head", (0.10, 0.095, 0.095), (0, 0, 0.665), straw, seg=12, rings=8),
        ball("tn_face", (0.075, 0.03, 0.07), (0, -0.075, 0.655), cloth, seg=12, rings=8),
        ball("tn_eyel", (0.022, 0.012, 0.024), (0.032, -0.102, 0.672), eye, seg=8, rings=5),
        ball("tn_eyer", (0.022, 0.012, 0.024), (-0.032, -0.102, 0.672), eye, seg=8, rings=5),
        box("tn_mouth", (0.07, 0.012, 0.012), (0, -0.103, 0.625), stitch),
        *[box(f"tn_stitch{k}", (0.008, 0.012, 0.03), (x, -0.104, 0.625), stitch) for k, x in enumerate((-0.025, 0.0, 0.025))],
        *[aim(f"tn_tuft{k}", straw_dk, (x, 0.0, 0.72), (x * 2.2, 0.03, 0.79), 0.018, 0.0, seg=4)
          for k, x in enumerate((0.05, -0.05))])
    # the patched straw hat, an arrow through its brim
    att(arm, "hat", cone("tn_hat", 0.15, 0.012, 0.10, (0, 0.01, 0.82), hat, rot=(-10, 0, 0), seg=16),
        cone("tn_hatband", 0.10, 0.09, 0.02, (0, 0.012, 0.79), rope, rot=(-10, 0, 0), seg=16),
        box("tn_patch", (0.055, 0.055, 0.012), (0.055, -0.045, 0.825), patch, rot=(25, -25, 0)),
        *arrow("tn_arrow4", (0.09, 0.03, 0.81), (0.9, 0.2, 0.5), 0.12, shaft, feather, head_m))
    # straw arms on the crossbar, frayed hands
    for s, side in ((1, "l"), (-1, "r")):
        att(arm, f"arm_{side}", aim(f"tn_arm{side}", straw, (s * 0.06, 0, AZ), (s * 0.19, 0, AZ - 0.02), 0.045, 0.04, seg=8),
            cone(f"tn_cuff{side}", 0.045, 0.045, 0.02, (s * 0.15, 0, AZ - 0.015), rope, rot=(0, 90, 0), seg=8))
        hand = [aim(f"tn_fore{side}", straw, (s * 0.18, 0, AZ - 0.02), (s * 0.26, 0, AZ - 0.05), 0.04, 0.032, seg=8)]
        for k, (dy, dz) in enumerate(((-0.03, 0.02), (0.0, -0.01), (0.03, 0.02), (0.0, -0.04))):
            hand.append(aim(f"tn_finger{side}{k}", straw_dk, (s * 0.25, dy * 0.5, AZ - 0.05),
                            (s * 0.34, dy, AZ - 0.07 + dz), 0.016, 0.0, seg=4))
        att(arm, f"hand_{side}", *hand)

    clips(arm)
    arm.scale = (SC, SC, SC)
    return arm


def clips(arm):
    def arms(l1=(0, 0), l2=(0, 0), r1=None, r2=None):
        """(raise, forward) in degrees per segment, left then right (mirrored if omitted).
        The arm bones point sideways: about y they rise and fall, about z they swing."""
        r1 = r1 if r1 is not None else l1
        r2 = r2 if r2 is not None else l2
        return {"arm_l": {"r": (0, -l1[0], -l1[1])}, "hand_l": {"r": (0, -l2[0], -l2[1])},
                "arm_r": {"r": (0, r1[0], r1[1])}, "hand_r": {"r": (0, r2[0], r2[1])}}

    idle = []
    for i in range(4):
        p = {"hop": {"r": (0, 3 * S(i, 4), 0)}, "body": {"s": (1, 1, 1 - 0.02 * S(i, 4, 0.8))},
             "head": {"r": (0, -5 * S(i, 4, 0.6), 4 * S(i, 4))}, "hat": {"r": (0, 4 * S(i, 4, -0.8), 0)}}
        p.update(arms((-14 + 6 * S(i, 4, -0.6), 0), (-16 + 8 * S(i, 4, -1.3), 0)))
        idle.append(p)

    # walk: a hop on the pole; z of the hop, squash of the straw, arm flail
    hops = [(0.0, 0.88, -25, -20, 0), (0.05, 1.08, 10, 20, -4), (0.10, 1.04, 35, 40, -6),
            (0.08, 1.0, 25, 30, -4), (0.03, 1.02, 0, 0, 0), (0.0, 0.9, -30, -30, 3)]
    walk = []
    for i, (z, sq, a1, a2, lean) in enumerate(hops):
        p = {"hop": {"l": (0, 0, z), "r": (lean, 4 * S(i, 6), 0)},
             "body": {"s": (1 + (1 - sq) * 0.6, 1 + (1 - sq) * 0.6, sq)},
             "head": {"r": (-lean, 0, 6 * S(i, 6))},
             "hat": {"r": (-10 * (sq - 1), 6 * S(i, 6, -1), 0), "l": (0, 0, 0.03 * max(0.0, 1 - sq))}}
        p.update(arms((a1, 0), (a2, 0)))
        walk.append(p)

    coil = {"hop": {"r": (-14, 0, 0)}, "body": {"s": (1.08, 1.08, 0.86)},
            "head": {"r": (-12, 0, 0)}, "hat": {"r": (-10, 0, 0), "l": (0, 0, 0.02)}}
    coil.update(arms((62, -10), (40, 0)))
    windup = [lerp_pose(idle[0], coil, 0.5), coil,
              merge(coil, arms((70, -14), (52, 0), (56, -6), (34, 0))),
              merge(coil, arms((56, -6), (34, 0), (70, -14), (52, 0)))]

    spring = {"hop": {"r": (10, 0, 0), "l": (0, -0.02, 0.05)}, "body": {"s": (0.95, 0.95, 1.08)},
              "head": {"r": (6, 0, 0)}, "hat": {"r": (-14, 0, 0), "l": (0, 0.01, 0.025)}}
    spring.update(arms((40, 30), (24, 20)))
    slap = {"hop": {"r": (18, 0, 0), "l": (0, -0.03, 0.01)}, "body": {"s": (1.04, 1.04, 0.95)},
            "head": {"r": (10, 0, 0)}, "hat": {"r": (12, 0, 0)}}
    slap.update(arms((-30, 70), (-20, 30)))
    recoil = lerp_pose(slap, idle[0], 0.5)
    attack = [spring, slap, recoil, lerp_pose(slap, idle[0], 0.88)]

    hit = [merge({"hop": {"r": (-16, 0, 6)}, "body": {"s": (1.06, 1.06, 0.92)}, "head": {"r": (-14, 0, 10)},
                  "hat": {"r": (-16, 10, 0), "l": (0, 0.02, 0.03)}}, arms((30, -20), (30, 0))),
           merge({"hop": {"r": (-6, 0, 2)}, "head": {"r": (-5, 0, 3)}}, arms((-4, 0), (-6, 0)))]

    heap = {"hop": {"r": (-20, 18, 0), "l": (0.0, 0.0, -0.06)}, "body": {"s": (1.1, 1.1, 0.7), "l": (0, 0, -0.10)},
            "head": {"r": (10, 0, 20)}, "hat": {"r": (0, -100, 30), "l": (-0.08, 0.10, -0.42)}}
    heap.update(arms((-50, 0), (-30, 0), (10, 0), (20, 0)))
    die = [merge({"hop": {"r": (-14, 0, 0)}, "head": {"r": (-20, 0, 0)}, "hat": {"r": (-30, 0, 0), "l": (0, 0, 0.08)}},
                 arms((50, 0), (40, 0))),
           merge({"hop": {"r": (-6, 10, 0), "l": (0, 0, -0.02)}, "body": {"l": (0, 0, -0.04)}, "head": {"r": (10, 0, 10)},
                  "hat": {"r": (-60, -30, 0), "l": (0.02, 0.06, 0.14)}}, arms((10, 0), (0, 0))),
           merge(lerp_pose(idle[0], heap, 0.4), {"hat": {"r": (-90, -60, 20), "l": (-0.03, 0.10, 0.02)}}),
           lerp_pose(idle[0], heap, 0.8),
           heap,
           merge(heap, {"head": {"r": (12, 0, 24)}})]
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=10)
