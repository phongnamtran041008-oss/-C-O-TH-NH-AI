"""Shared bits for MONSTERS_D (runs inside Blender).

The solids, materials, armature, rigid attach, skinning, pose tables and clips come from
art/src/monsters_a/rig.py (imported as is, never edited). This file adds what the six new
creatures need on top: a planar two-bone IK that works in *absolute* bone angles (so legs
of any rest direction, hocks bending backward and knees bending forward, all use one
solver), the clip writer, and small helpers.

Angles: in the y-z plane of the armature (y = behind the creature, z = up) a bone's angle
is atan2(dy, -dz) of its head->tail direction, so a bone hanging straight down is 0 and a
positive angle swings its tip backward. A pose entry {"r": (d, 0, 0)} rotates a bone by d
degrees on top of its parent, so the *relative* delta of a bone is its own change of angle
minus its parent's change of angle (planar rotations add).
"""
from __future__ import annotations

import math

from rig import attach, clip

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)
    return objs


def ang(head, tail):
    """Angle (deg) of a bone in the y-z plane, from (y, z) head/tail."""
    return math.degrees(math.atan2(tail[0] - head[0], -(tail[1] - head[1])))


def rot(p, deg, about=(0.0, 0.0)):
    """Rotate the (y, z) point p by +x `deg` about `about` (the armature's +x rotation)."""
    a = math.radians(deg)
    y, z = p[0] - about[0], p[1] - about[1]
    return (about[0] + y * math.cos(a) - z * math.sin(a), about[1] + y * math.sin(a) + z * math.cos(a))


def ik2(hip, target, a, b, bend):
    """Two-bone IK in the y-z plane. bend=+1 puts the joint behind the hip-target line
    (a hock), -1 in front of it (a knee). Returns (upper angle, lower angle, joint)."""
    dy, dz = target[0] - hip[0], target[1] - hip[1]
    L = max(abs(a - b) + 1e-4, min(math.hypot(dy, dz), a + b - 1e-4))
    phi = math.atan2(dy, -dz)
    g = math.acos(max(-1.0, min(1.0, (a * a + L * L - b * b) / (2 * a * L))))
    u = phi + bend * g
    jy, jz = hip[0] + a * math.sin(u), hip[1] - a * math.cos(u)
    lo = math.atan2(target[0] - jy, -(target[1] - jz))
    return math.degrees(u), math.degrees(lo), (jy, jz)


class Limb:
    """A two-bone limb (+ optional foot bone kept at a fixed world angle).

    names: (upper, lower[, foot]); rest: {bone: ((y,z) head, (y,z) tail)} from the armature
    table; bend as in ik2."""

    def __init__(self, names, rest, bend):
        self.names = names
        self.bend = bend
        (h1, t1), (h2, t2) = rest[names[0]], rest[names[1]]
        self.hip = h1
        self.a = math.dist(h1, t1)
        self.b = math.dist(h2, t2)
        self.rest = [ang(h1, t1), ang(h2, t2)]
        self.foot_rest = ang(*rest[names[2]]) if len(names) > 2 else None
        self.end = t2                                    # rest position of the foot joint

    def solve(self, hip_now, target, parent_delta=0.0, foot_world=None):
        """hip_now: posed (y, z) of the limb's head; target: (y, z) of the foot joint.
        parent_delta: the parent's change of angle (body pitch). foot_world: change of
        angle of the foot bone in the world (0 = as modelled, e.g. a hoof kept flat)."""
        u, lo, _ = ik2(hip_now, target, self.a, self.b, self.bend)
        du = u - self.rest[0]
        dl = lo - self.rest[1]
        out = {self.names[0]: {"r": (du - parent_delta, 0, 0)},
               self.names[1]: {"r": (dl - du, 0, 0)}}
        if self.foot_rest is not None:
            fw = 0.0 if foot_world is None else foot_world
            out[self.names[2]] = {"r": (fw - dl, 0, 0)}
        return out

    def fk(self, upper, lower, parent_delta=0.0, foot_world=None):
        """Pose by absolute changes of angle (deg) instead of a target."""
        out = {self.names[0]: {"r": (upper - parent_delta, 0, 0)},
               self.names[1]: {"r": (lower - upper, 0, 0)}}
        if self.foot_rest is not None:
            fw = lower if foot_world is None else foot_world
            out[self.names[2]] = {"r": (fw - lower, 0, 0)}
        return out


def posed(point, body_head, shift=(0.0, 0.0), pitch=0.0):
    """Where a rest (y, z) point carried by a body bone (head body_head) ends up after the
    body moved by `shift` (y, z) and pitched by `pitch` degrees."""
    p = rot(point, pitch, body_head)
    return (p[0] + shift[0], p[1] + shift[1])


def six(arm, idle, walk, windup, attack, hit, die, walk_fps=10, hit_frame=1,
        fps=None):
    f = {"idle": 6, "windup": 8, "attack": 14, "hit": 12, "die": 10}
    f.update(fps or {})
    clip(arm, "idle", idle, f["idle"], True)
    clip(arm, "walk", walk, walk_fps, True)
    clip(arm, "windup", windup, f["windup"], False)
    clip(arm, "attack", attack, f["attack"], False, hit=hit_frame)
    clip(arm, "hit", hit, f["hit"], False)
    clip(arm, "die", die, f["die"], False)
    arm.animation_data.action = None


def basis(origin, X, Y, Z):
    """4x4 matrix with columns X, Y, Z (made orthonormal and right-handed from Z and X)
    placed at origin."""
    from mathutils import Matrix, Vector
    z = Vector(Z).normalized()
    x = (Vector(X) - z * Vector(X).dot(z)).normalized()
    y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4()
    m.translation = Vector(origin)
    return m


def oriented_ball(name, radii, center, X, Z, mat, seg=12, rings=8):
    """An ellipsoid with radii along its own X, Y, Z axes, placed in a frame given by X and
    Z (Y = Z x X)."""
    import bmesh
    from mathutils import Vector
    from rig import _finish
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    bmesh.ops.scale(bm, vec=Vector(radii), verts=bm.verts)
    bmesh.ops.transform(bm, matrix=basis(center, X, None, Z), verts=bm.verts)
    return _finish(name, bm, mat, smooth=True)


def rest_table(bones):
    """{bone: ((y, z) head, (y, z) tail)} from an armature table (x ignored)."""
    return {n: ((h[1], h[2]), (t[1], t[2])) for n, h, t, _ in bones}
