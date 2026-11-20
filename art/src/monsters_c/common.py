"""Shared bits for the MONSTERS_C creatures (runs inside Blender).

The solids, materials, armature, skinning and pose tables come from the MONSTERS_A helpers
(`art/src/monsters_a/rig.py`, `quadrupeds.py`), imported read-only through sys.path; this
batch never edits that folder. What is new here: flat outlined plates placed on any plane
(wings, scales, sword shards), zigzag bolts, hover shadows and a pose for rotating the whole
creature about a point (rolling, tumbling).

Pose tables follow rig.set_pose: r = (deg about x, y, z) in armature axes; x = picture
right when the creature faces the camera (its own left), y = behind it, z = up. +x tips an
upright bone forward and swings a hanging bone's tip backward; for a bone pointing
backward (+y) it lifts the tip; +z turns a forward-pointing bone toward +x.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MA = HERE.parent / "monsters_a"
for p in (str(HERE), str(MA)):
    if p not in sys.path:
        sys.path.insert(0, p)

import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Euler, Vector  # noqa: E402

import rig  # noqa: E402,F401
from rig import (_finish, aim, armature, attach, ball, box, clip, cone, lerp_pose,  # noqa: E402,F401
                 material, merge, place, prism, set_root_offset, shadow_material, skin, tube,
                 use_collection)

TAU = 2 * math.pi
FPS = {"idle": 6, "walk": 10, "windup": 8, "attack": 14, "hit": 12, "die": 10}


def hx(code: str):
    """A palette colour '#rrggbb' as the *linear* RGB Blender wants in Base Color. The kit
    converts base colours to sRGB before snapping them to the palette, so giving the hex
    of the wanted palette entry here lands exactly on that entry (it then becomes the
    base tone; the cel shadow and light take its ramp neighbours)."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    code = code.lstrip("#")
    return tuple(lin(int(code[i:i + 2], 16)) for i in (0, 2, 4))


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1, fps=None):
    f = dict(FPS, **(fps or {}))
    clip(arm, "idle", idle, f["idle"], True)
    clip(arm, "walk", walk, f["walk"], True)
    clip(arm, "windup", windup, f["windup"], False)
    clip(arm, "attack", attack, f["attack"], False, hit=hit_frame)
    clip(arm, "hit", hit, f["hit"], False)
    clip(arm, "die", die, f["die"], False)
    arm.animation_data.action = None


def plate(name, outline, mat, origin, u, v, thick=0.012):
    """A flat plate: the 2-D outline [(a, b), ...] is laid out as origin + a*u + b*v and
    given `thick` along u x v. Wings, scales, feathers, sword shards."""
    o, U, V = Vector(origin), Vector(u).normalized(), Vector(v).normalized()
    N = U.cross(V).normalized() * (thick / 2)
    bm = bmesh.new()
    front = [bm.verts.new(o + U * a + V * b + N) for a, b in outline]
    back = [bm.verts.new(o + U * a + V * b - N) for a, b in outline]
    n = len(outline)
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((front[i], front[j], back[j], back[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    caps = [f for f in bm.faces if len(f.verts) == n]
    bmesh.ops.triangulate(bm, faces=caps)
    return _finish(name, bm, mat)


def zigzag(a, b, n, amp, seed=0, side=(0, 0, 1)):
    """Points of a lightning bolt from a to b: n kinks, alternating sideways by amp."""
    A, B = Vector(a), Vector(b)
    d = B - A
    s = Vector(side)
    s = (s - d.normalized() * s.dot(d.normalized()))
    if s.length < 1e-6:
        s = d.orthogonal()
    s.normalize()
    pts = [A]
    for k in range(1, n):
        t = k / n
        w = amp * (1 if (k + seed) % 2 else -1) * (0.6 + 0.4 * ((k * 7 + seed * 3) % 5) / 4)
        pts.append(A + d * t + s * w)
    pts.append(B)
    return [tuple(p) for p in pts]


def bolt(name, pts, r, mat):
    """A thin glowing bolt through zigzag points: one aimed cone per segment."""
    out = []
    for k in range(len(pts) - 1):
        out.append(aim(f"{name}{k}", mat, pts[k], pts[k + 1], r, r * 0.8, seg=5))
    return out


def hover_shadow(name, rx, ry, arm):
    """Flat contact shadow under a hovering creature, parented to the armature object."""
    return rig.shadow(name, rx, ry, shadow_material("MAT_" + name), arm)


def about(center, r, extra=None):
    """Root pose that turns the whole creature by r (deg, armature axes) about `center`."""
    R = Euler([math.radians(a) for a in r], "XYZ").to_matrix()
    c = Vector(center)
    l = c - R @ c
    if extra:
        l += Vector(extra)
    return {"r": tuple(r), "l": tuple(l)}


def glow_mat(name, col, col_di, strength, glow, glow_di):
    return material(name, col, col_di, emit=strength, glow=(glow, glow_di))


def tone(m, light=None, shadow=None):
    """Move the cel thresholds of a material (dark bodies keep a lit rim)."""
    if light is not None:
        m["kit_light"] = light
    if shadow is not None:
        m["kit_shadow"] = shadow
    return m
