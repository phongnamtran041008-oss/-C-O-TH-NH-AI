"""Tri Chu Tinh: the graph-land spider (elite 64). Runs inside Blender.

Eight two-bone legs fan out radially from the cephalothorax, knees high, feet planted in a
tight ring (whatever touches the ground in front of the origin draws below the pivot, and
the kit allows only a few pixels there). Legs are posed by a planar two-bone IK with an
up-and-out knee pole, written as quaternions in armature axes ("q" in rig.set_pose). The
abdomen carries a small glowing graph: six nodes joined by lines.
"""
from __future__ import annotations

import math

from mathutils import Euler, Quaternion, Vector

from rig import aim, armature, attach, ball, clip, material, merge, use_collection

TAU = 2 * math.pi
HIP_C = Vector((0, -0.04, 0.27))       # centre of the hip ring
FOOT_C = Vector((0, 0.005, 0.0))       # centre of the foot ring
BODY_HEAD = Vector((0, -0.06, 0.22))   # body bone pivot
ANGLES = (40, 75, 110, 145)            # leg directions, degrees from straight ahead
LEGS = [(f"{side}{i}", sx, a) for side, sx in (("l", 1), ("r", -1)) for i, a in enumerate(ANGLES)]


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def leg_dir(sx, a):
    r = math.radians(a)
    return Vector((sx * math.sin(r), -math.cos(r), 0.0))


def rest_points(sx, a):
    d = leg_dir(sx, a)
    hip = HIP_C + d * 0.08
    knee = HIP_C + d * 0.33 + Vector((0, 0, 0.22))     # high, wide knees: the arch
    foot = FOOT_C + d * 0.13
    return hip, knee, foot


class SpiderIK:
    def __init__(self):
        self.rest = {n: rest_points(sx, a) for n, sx, a in LEGS}
        self.dir = {n: leg_dir(sx, a) for n, sx, a in LEGS}

    def pose(self, t=(0, 0, 0), pitch=0.0, feet=None, extra=None):
        """Body moved by t and pitched by `pitch` degrees (+ = front dips); feet: leg ->
        world target (default: the rest foot). Returns a pose dict."""
        feet = feet or {}
        R = Euler((math.radians(pitch), 0, 0), "XYZ").to_quaternion()
        T = Vector(t)
        out = {"body": {"l": tuple(T), "r": (pitch, 0, 0)}}
        for n, (h0, k0, f0) in self.rest.items():
            hip = BODY_HEAD + T + R @ (h0 - BODY_HEAD)
            foot = Vector(feet.get(n, f0))
            a, b = (k0 - h0).length, (f0 - k0).length
            v = foot - hip
            d = max(1e-4, min(v.length, a + b - 1e-4))
            u = v.normalized()
            along = (a * a - b * b + d * d) / (2 * d)
            hh = math.sqrt(max(0.0, a * a - along * along))
            pole = (self.dir[n] * 0.6 + Vector((0, 0, 1.0)))
            w = (pole - u * pole.dot(u)).normalized()
            knee = hip + u * along + w * hh
            q1 = (k0 - h0).normalized().rotation_difference(R.inverted() @ (knee - hip).normalized())
            par = R @ q1
            q2 = (f0 - k0).normalized().rotation_difference(par.inverted() @ (foot - knee).normalized())
            out[f"leg_{n}a"] = {"q": tuple(q1)}
            out[f"leg_{n}b"] = {"q": tuple(q2)}
        if extra:
            out = merge(out, extra)
        return out

    def foot(self, n, dy=0.0, lift=0.0, scale=1.0):
        f = self.rest[n][2]
        return (FOOT_C + (f - FOOT_C) * scale) + Vector((0, dy, lift))


def build_tri_chu_tinh():
    use_collection("COL_tri_chu_tinh")
    shell = material("MAT_tc_shell", (0.18, 0.16, 0.20), (0.36, 0.10, 0.11), ramp=("hair", "red"))
    abdo = material("MAT_tc_abdomen", (0.23, 0.13, 0.38), (0.58, 0.19, 0.16), ramp=("purple", "red"))
    leg = material("MAT_tc_leg", (0.36, 0.21, 0.56), (0.58, 0.19, 0.16), ramp=("purple", "red"))
    joint = material("MAT_tc_joint", (0.52, 0.34, 0.75), (0.78, 0.33, 0.23), ramp=("purple", "red"))
    fang = material("MAT_tc_fang", (0.81, 0.80, 0.83), (0.90, 0.72, 0.23), ramp=("bone", "gold"))
    eye = material("MAT_tc_eye", (1.0, 0.68, 0.23), (0.35, 0.88, 0.96), emit=6.0, glow=("flame", "spirit"))
    node = material("MAT_tc_node", (0.35, 0.88, 0.96), (1.0, 0.89, 0.48), emit=5.0, glow=("spirit", "holy"))
    node["kit_priority"] = 3.0
    edge = material("MAT_tc_line", (0.35, 0.88, 0.96), (1.0, 0.89, 0.48), emit=3.0, glow=("spirit", "holy"))

    bones = [("root", (0, 0, 0), (0, 0, 0.08), None),
             ("body", tuple(BODY_HEAD), tuple(BODY_HEAD + Vector((0, 0, 0.14))), "root"),
             ("abdomen", (0, 0.08, 0.31), (0, 0.24, 0.38), "body"),
             ("fang_l", (0.035, -0.19, 0.28), (0.032, -0.23, 0.20), "body"),
             ("fang_r", (-0.035, -0.19, 0.28), (-0.032, -0.23, 0.20), "body")]
    for n, sx, a in LEGS:
        h, k, f = rest_points(sx, a)
        bones.append((f"leg_{n}a", tuple(h), tuple(k), "body"))
        bones.append((f"leg_{n}b", tuple(k), tuple(f), f"leg_{n}a"))
    arm = armature("tri_chu_tinh", bones)

    eyes = [ball("tc_eyel", (0.04, 0.022, 0.04), (0.045, -0.212, 0.335), eye, seg=8, rings=5),
            ball("tc_eyer", (0.04, 0.022, 0.04), (-0.045, -0.212, 0.335), eye, seg=8, rings=5)]
    for k, (x, z) in enumerate(((0.095, 0.36), (-0.095, 0.36), (0.03, 0.39), (-0.03, 0.39))):
        eyes.append(ball(f"tc_eyes{k}", (0.024,) * 3, (x, -0.195 + abs(x) * 0.3, z), eye, seg=6, rings=4))
    att(arm, "body", ball("tc_ceph", (0.14, 0.15, 0.10), (0, -0.08, 0.31), shell),
        ball("tc_ridge", (0.05, 0.11, 0.03), (0, -0.07, 0.405), joint, seg=10, rings=5), *eyes,
        ball("tc_waist", (0.06, 0.06, 0.05), (0, 0.075, 0.31), joint, seg=8, rings=5),
        aim("tc_palpl", joint, (0.06, -0.19, 0.29), (0.10, -0.25, 0.22), 0.02, 0.012, seg=6),
        aim("tc_palpr", joint, (-0.06, -0.19, 0.29), (-0.10, -0.25, 0.22), 0.02, 0.012, seg=6))
    att(arm, "fang_l", aim("tc_fangl", fang, (0.035, -0.19, 0.28), (0.03, -0.235, 0.20), 0.024, 0.0, seg=6))
    att(arm, "fang_r", aim("tc_fangr", fang, (-0.035, -0.19, 0.28), (-0.03, -0.235, 0.20), 0.024, 0.0, seg=6))
    # abdomen with the glowing graph on its back: six nodes, seven edges
    ac = Vector((0, 0.25, 0.39))
    rad = Vector((0.17, 0.21, 0.15))
    tilt = Euler((math.radians(-8), 0, 0), "XYZ").to_matrix()

    def surf(u, v, out=1.03):
        """Point on the abdomen surface: u around (deg, 0 = top), v along (deg from back)."""
        uu, vv = math.radians(u), math.radians(v)
        p = Vector((math.sin(uu) * math.sin(vv), math.cos(vv), math.cos(uu) * math.sin(vv)))
        p = Vector((p.x * rad.x, p.y * rad.y, p.z * rad.z)) * out
        return ac + tilt @ p
    nodes = [surf(0, 80), surf(-45, 55), surf(45, 55), surf(-35, 110), surf(35, 110), surf(0, 135)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (0, 5), (1, 2)]
    parts = [ball("tc_abdomen", tuple(rad), tuple(ac), abdo, rot=(-8, 0, 0)),
             ball("tc_spinner", (0.05, 0.05, 0.05), tuple(surf(0, 175, 0.95)), joint, seg=8, rings=5)]
    for k, p in enumerate(nodes):
        parts.append(ball(f"tc_node{k}", (0.03,) * 3, tuple(p), node, seg=8, rings=5))
    for k, (i, j) in enumerate(edges):
        parts.append(aim(f"tc_edge{k}", edge, tuple(nodes[i]), tuple(nodes[j]), 0.013, 0.013, seg=5))
    att(arm, "abdomen", *parts)
    for n, sx, a in LEGS:
        h, k, f = rest_points(sx, a)
        att(arm, f"leg_{n}a", aim(f"tc_femur{n}", leg, tuple(h), tuple(k), 0.036, 0.03, seg=7),
            ball(f"tc_knee{n}", (0.042,) * 3, tuple(k), joint, seg=8, rings=5))
        att(arm, f"leg_{n}b", aim(f"tc_tibia{n}", leg, tuple(k), tuple(f + Vector((0, 0, 0.01))), 0.03, 0.013, seg=7))

    ik = SpiderIK()
    TAU4 = [TAU * i / 4 for i in range(4)]
    idle = [ik.pose((0, 0, 0.006 * math.sin(ph)), 0.0, extra={
        "abdomen": {"r": (-3 * math.sin(ph), 0, 2 * math.cos(ph)), "s": 1.0 + 0.02 * math.sin(ph)},
        "fang_l": {"r": (6 * max(0.0, math.sin(ph)), 0, 0)}, "fang_r": {"r": (6 * max(0.0, math.sin(ph)), 0, 0)}})
        for ph in TAU4]
    walk = []
    group_a = {"l0", "r1", "l2", "r3"}
    for i in range(6):
        ph = i / 6
        feet = {}
        for n, _, _ in LEGS:
            p = (ph + (0.0 if n in group_a else 0.5)) % 1.0
            if p < 0.5:
                dy, lift = -0.022 + 0.088 * p, 0.0
            else:
                q = (p - 0.5) / 0.5
                dy, lift = 0.022 - 0.044 * q, 0.06 * math.sin(math.pi * q)
            feet[n] = ik.foot(n, dy, lift)
        walk.append(ik.pose((0, 0, 0.01 * abs(math.sin(TAU * ph * 2))), 2.0, feet,
                            extra={"abdomen": {"r": (0, 0, 4 * math.sin(TAU * ph))}}))
    # windup: rears up, front legs raised high and spread, fangs open, abdomen cocked
    rear_feet = {"l0": (0.17, -0.20, 0.62), "r0": (-0.17, -0.20, 0.62),
                 "l1": (0.27, -0.16, 0.34), "r1": (-0.27, -0.16, 0.34)}
    rear = ik.pose((0, 0.03, 0.07), -26.0, rear_feet, extra={
        "abdomen": {"r": (34, 0, 0)}, "fang_l": {"r": (-30, 0, -14)}, "fang_r": {"r": (-30, 0, 14)}})
    rear_b = ik.pose((0.004, 0.03, 0.075), -27.0, {k: tuple(Vector(v) + Vector((0, 0, 0.015))) for k, v in rear_feet.items()},
                     extra={"abdomen": {"r": (35, 0, 3)}, "fang_l": {"r": (-34, 0, -16)}, "fang_r": {"r": (-34, 0, 16)}})
    windup = [ik.pose((0, 0.015, 0.035), -12.0, {k: tuple((Vector(v) + Vector(ik.rest[k][2])) / 2) for k, v in rear_feet.items()},
                      extra={"abdomen": {"r": (10, 0, 0)}}), rear, rear_b, rear]
    # attack: pounce, the front legs stabbing down just ahead, fangs snapping shut
    attack = [
        ik.pose((0, -0.02, 0.07), 8.0, {"l0": (0.13, -0.30, 0.34), "r0": (-0.13, -0.30, 0.34),
                                        "l1": (0.22, -0.20, 0.18), "r1": (-0.22, -0.20, 0.18)},
                extra={"abdomen": {"r": (-8, 0, 0)}, "fang_l": {"r": (-30, 0, -12)}, "fang_r": {"r": (-30, 0, 12)}}),
        ik.pose((0, -0.03, -0.04), 16.0, {"l0": (0.08, -0.11, 0.0), "r0": (-0.08, -0.11, 0.0)},
                extra={"abdomen": {"r": (-14, 0, 0)}, "fang_l": {"r": (16, 0, 0)}, "fang_r": {"r": (16, 0, 0)}}),
        ik.pose((0, -0.02, -0.02), 9.0, extra={"abdomen": {"r": (-6, 0, 0)},
                                                "fang_l": {"r": (8, 0, 0)}, "fang_r": {"r": (8, 0, 0)}}),
        ik.pose((0, 0, 0), 2.0)]
    hit = [ik.pose((0, 0.02, 0.02), -14.0, extra={"abdomen": {"r": (20, 0, 8), "s": (1.04, 0.96, 1.04)},
                                                   "fang_l": {"r": (-20, 0, 0)}, "fang_r": {"r": (-20, 0, 0)}}),
           ik.pose((0, 0.01, 0.01), -5.0, extra={"abdomen": {"r": (5, 0, 3)}})]
    curled = {}
    for n, sx, a in LEGS:
        d = leg_dir(sx, a)
        curled[n] = tuple(HIP_C + Vector((0, 0, -0.04)) + d * 0.03 + Vector((0, 0, 0.42)))
    dead = ik.pose((0, 0, -0.04), 4.0, curled, extra={"abdomen": {"r": (-10, 0, 10)},
                                                    "fang_l": {"r": (10, 0, 0)}, "fang_r": {"r": (10, 0, 0)}})
    half = ik.pose((0, 0, -0.06), 0.0, {n: tuple((Vector(ik.rest[n][2]) + Vector(curled[n])) / 2 + Vector((0, 0, 0.05)))
                                         for n, _, _ in LEGS})
    die = [ik.pose((0, 0.02, 0.05), -18.0, {"l0": (0.17, -0.2, 0.5), "r0": (-0.17, -0.2, 0.5)},
                   extra={"fang_l": {"r": (-34, 0, 0)}, "fang_r": {"r": (-34, 0, 0)}}),
           ik.pose((0, 0, -0.02), 6.0, extra={"abdomen": {"r": (-6, 0, 8)}}),
           half, dead, dead, dead]
    arm.scale = (1.12, 1.12, 1.12)     # elite: fill the 64 px frame
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 12, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=1)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    arm.animation_data.action = None
    return arm
