"""The ten player clips on ARM_dao_si (runs inside Blender).

Every rendered frame is a pose written out here (pose-to-pose, the way pixel animation is
drawn), then a follow-through pass hangs the hair, ribbons, sleeves, cape and robe hem off
the body with gravity, wind and a lag behind the body's motion (each link of a chain one
frame later than the one above it). Every bone is keyed on every frame of every action, so
no action depends on what another left behind.

Conventions (see rig.py): rot = rest-axis rotation relative to the parent
(rx + tips the top forward, ry + tips it to the character's left, rz + turns to the left);
aim = direction in the parent's frame, waim = world direction; forward is -Y, the
character's left is +X, up is +Z. Legs are ankle targets solved by two-bone IK.
"""
from __future__ import annotations

import math

from mathutils import Quaternion, Vector

import rig as R

FOOT_FLAT = Vector((0, -0.92, -0.38))
AZ = R.RIG_BONES["foot.L"][0][2]          # ankle height in the rest pose
ANKLE = {"L": Vector((0.08, 0.0, AZ)), "R": Vector((-0.08, 0.0, AZ))}


def V(*a):
    return Vector(a)


def stance() -> dict:
    """The ready stance: knees soft, the sword hand a little forward so a weapon sits
    naturally in it, the free hand relaxed."""
    return {
        "hips": {"loc": V(0, 0, -0.014)},
        "upper_arm.L": {"aim": V(0.30, 0.03, -1)},
        "forearm.L": {"aim": V(0.12, -0.42, -1)},
        "upper_arm.R": {"aim": V(-0.30, -0.02, -1)},
        "forearm.R": {"aim": V(-0.06, -0.62, -1)},
        "hand.R": {"blade": V(-0.35, -0.6, -0.72)},
        "legs": {s: {"ankle": ANKLE[s].copy(), "pole": V(0.15 if s == "L" else -0.15, -1, 0),
                     "foot": FOOT_FLAT.copy()} for s in "LR"},
        "wind": V(0, 0, 0),
        "wing": (0.0, 0.0),      # (flap degrees, fold degrees)
        "qi_angle": 0.0,
    }


def setrot(p, bone, q):
    p.setdefault(bone, {})["rot"] = q


def lerp(a, b, t):
    return a + (b - a) * t


def wings(p, flap, fold=0.0, lag=0.0, yaw=0.0):
    """flap (+ raises), fold (+ sweeps both wings back), lag (wing tip), yaw (turns both
    wings about the spine, used to keep them square to the camera while the body twists)."""
    p["wing"] = (flap, fold, lag, yaw)


def clamp_cone(d, axis, deg):
    """Keep direction d within `deg` degrees of `axis`."""
    d = Vector(d).normalized()
    axis = Vector(axis).normalized()
    if d.angle(axis) <= math.radians(deg):
        return d
    rot_axis = axis.cross(d)
    if rot_axis.length < 1e-6:
        return axis
    return Quaternion(rot_axis.normalized(), math.radians(deg)) @ axis


def above_ground(head, length, d, floor=0.03):
    """Bend a hanging bone so its tail stays above the ground (robes, hair and capes lie
    on the floor instead of sinking into it when the body sits or falls)."""
    d = Vector(d).normalized()
    min_z = (floor - head.z) / max(length, 1e-6)
    if d.z >= min_z:
        return d
    min_z = max(-1.0, min(1.0, min_z))
    flat = Vector((d.x, d.y, 0))
    if flat.length < 1e-6:
        flat = Vector((0, 1, 0))
    flat.normalize()
    return flat * math.sqrt(max(0.0, 1 - min_z * min_z)) + Vector((0, 0, min_z))


# ---------------------------------------------------------------- clips
def idle(i, n):
    p = stance()
    b = math.cos(math.tau * i / n)            # 1 = breath in
    b_lag = math.cos(math.tau * (i - 1) / n)
    p["hips"]["loc"] = V(0, 0, -0.016 + 0.006 * b)
    setrot(p, "spine", R.euler(x=-1.0 * b))
    setrot(p, "chest", R.euler(x=-1.5 * b))
    setrot(p, "head", R.euler(x=2.0 * b_lag))
    p["upper_arm.L"]["aim"] = V(0.30 + 0.03 * b, 0.03, -1)
    p["upper_arm.R"]["aim"] = V(-0.30 - 0.03 * b, -0.02, -1)
    p["wind"] = V(0.0, 0.08 * math.sin(math.tau * i / n), 0)
    wings(p, 6 * b, 0, -4 * math.sin(math.tau * i / n))
    p["qi_angle"] = 120.0 * i / n
    return p


def walk(i, n):
    p = stance()
    ph = i / n
    S = 0.04
    for s, off in (("L", 0.0), ("R", 0.5)):
        q = (ph + off) % 1.0
        a = ANKLE[s].copy()
        a.x *= 0.55                         # feet walk close to one line
        if q < 0.5:                         # planted: slides back at walking speed
            t = q / 0.5
            a.y = -S + 2 * S * t
            foot = FOOT_FLAT.copy() if t < 0.75 else V(0, -0.85, -0.6)
        else:                               # swing: lift, pass, reach
            t = (q - 0.5) / 0.5
            a.y = S - 2 * S * (t * t * (3 - 2 * t))
            a.z += 0.04 * math.sin(math.pi * t)
            foot = V(0, -1, -0.9) if t < 0.4 else V(0, -1, -0.05)
        p["legs"][s]["ankle"] = a
        p["legs"][s]["foot"] = foot
    bob = [0.0, -0.013, 0.004, 0.010][i % 4]
    p["hips"]["loc"] = V(0, 0, -0.020 + bob)
    c = math.cos(math.tau * ph)
    setrot(p, "hips", R.euler(z=-8 * c, y=2.5 * math.sin(math.tau * ph * 2)))
    setrot(p, "spine", R.euler(x=4, z=4 * c))
    setrot(p, "chest", R.euler(z=8 * c))
    setrot(p, "head", R.euler(x=-3 * bob / 0.013, z=-4 * c))
    p["upper_arm.L"]["aim"] = V(0.28, 0.50 * c, -1)
    p["forearm.L"]["aim"] = V(0.10, -0.35 - 0.35 * max(0.0, -c), -1)
    p["upper_arm.R"]["aim"] = V(-0.28, 0.30 * c - 0.05, -1)
    p["forearm.R"]["aim"] = V(-0.06, -0.62 - 0.2 * max(0.0, c), -1)
    p["wind"] = V(0, 0.30, 0)
    wings(p, 8 * math.cos(math.tau * ph * 2), 6, -6 * math.sin(math.tau * ph * 2))
    p["qi_angle"] = 120.0 * i / n
    return p


def slash(i, n):
    """A big diagonal cut, readable with an empty hand (the weapon layer rides in it):
    wide stance and the body wound right with the hand high behind the right shoulder (0-1),
    a lunge as the arm sweeps over and across (2), fully extended to the front left on the
    hit frame 3, follow-through low left (4), recovery (5)."""
    p = stance()
    K = [  # turn, lean, hips (y, z), upper.R, fore.R, blade, L ankle, R ankle, upper.L, fore.L
        (-35, -4, (0.02, -0.05), (-0.6, 0.2, 0.75), (-0.3, 0.15, 1.0), (-0.4, 0.3, 0.85),
         (0.13, -0.03), (-0.12, 0.04), (0.35, -0.8, -0.25), (0.3, -0.95, 0.15)),
        (-50, -8, (0.03, -0.06), (-0.5, 0.45, 0.75), (-0.1, 0.55, 0.85), (-0.55, 0.55, 0.6),
         (0.13, -0.03), (-0.12, 0.04), (0.4, -0.85, -0.1), (0.35, -0.9, 0.25)),
        (-5, 8, (-0.02, -0.07), (-0.4, -0.85, 0.4), (-0.15, -1.0, 0.3), (0.1, -0.8, 0.6),
         (0.13, 0.0), (-0.11, -0.05), (0.55, 0.2, -0.75), (0.4, 0.4, -0.85)),
        (40, 18, (-0.05, -0.085), (0.35, -0.94, -0.05), (0.4, -0.92, -0.05), (0.85, -0.5, -0.1),
         (0.13, 0.04), (-0.11, -0.10), (0.6, 0.6, -0.4), (0.5, 0.7, -0.45)),
        (52, 22, (-0.055, -0.09), (0.65, -0.6, -0.45), (0.75, -0.4, -0.55), (0.55, 0.3, -0.8),
         (0.13, 0.04), (-0.11, -0.10), (0.6, 0.6, -0.4), (0.5, 0.7, -0.45)),
        (15, 6, (-0.02, -0.04), (-0.2, -0.5, -0.85), (-0.1, -0.85, -0.5), (-0.3, -0.7, -0.6),
         (0.11, 0.02), (-0.10, -0.07), (0.35, 0.1, -1), (0.15, -0.3, -1)),
    ]
    turn, lean, (hy, hz), ua, fa, blade, la, ra, ual, fal = K[i]
    p["hips"]["loc"] = V(0, hy, hz)
    setrot(p, "hips", R.euler(z=turn * 0.35))
    setrot(p, "spine", R.euler(x=lean * 0.5, z=turn * 0.3))
    setrot(p, "chest", R.euler(x=lean * 0.5, z=turn * 0.35))
    setrot(p, "head", R.euler(x=-lean * 0.4, z=-turn * 0.55))
    p["upper_arm.R"]["aim"] = V(*ua)
    p["forearm.R"]["aim"] = V(*fa)
    p["hand.R"] = {"blade": V(*blade)}
    p["upper_arm.L"]["aim"] = V(*ual)
    p["forearm.L"]["aim"] = V(*fal)
    p["legs"]["L"]["ankle"] = V(la[0], la[1], AZ)
    p["legs"]["R"]["ankle"] = V(ra[0], ra[1], AZ + (0.05 if i == 2 else 0))
    p["legs"]["L"]["pole"] = V(0.6, -1, 0)
    p["legs"]["R"]["pole"] = V(-0.6, -1, 0)
    p["legs"]["L"]["foot"] = V(0.35, -0.85, -0.38)
    p["legs"]["R"]["foot"] = V(-0.2, -0.9, -0.38)
    wings(p, [-10, -16, 18, 26, 14, 2][i], [10, 14, -4, -8, -2, 4][i], [4, 8, -14, -10, 6, 4][i],
          yaw=-0.7 * turn)
    p["qi_angle"] = 15.0 * i
    return p


def cast(i, n):
    """Spell cast: a two-hand seal at the chest (0), raised to the chin while the body
    gathers (1), the left palm drawn back to the hip, body wound (2), then a lunge and a
    decisive palm thrust at full reach on the release frame 3, held (4), recover (5)."""
    p = stance()
    turn = [0, 0, 28, -30, -34, -8][i]
    lean = [2, -4, -2, 14, 18, 4][i]
    hz = [-0.03, -0.05, -0.05, -0.08, -0.085, -0.03][i]
    hy = [0, 0.01, 0.02, -0.04, -0.05, -0.015][i]
    p["hips"]["loc"] = V(0, hy, hz)
    setrot(p, "hips", R.euler(z=turn * 0.3))
    setrot(p, "spine", R.euler(x=lean * 0.5, z=turn * 0.3))
    setrot(p, "chest", R.euler(x=lean * 0.5, z=turn * 0.4))
    setrot(p, "head", R.euler(x=-lean * 0.5 + (6 if i == 1 else 0), z=-turn * 0.6))
    seal_l = ((-0.2, -0.75, -0.6), (-0.8, -0.45, 0.45))
    seal_r = ((0.2, -0.75, -0.6), (0.8, -0.45, 0.45))
    L = [seal_l, ((-0.15, -0.85, -0.3), (-0.6, -0.4, 0.8)),
         ((0.5, 0.5, -0.7), (0.3, 0.2, -1)),
         ((0.3, -1.0, 0.18), (0.3, -1.0, 0.2)),
         ((0.3, -1.0, 0.22), (0.3, -1.0, 0.25)),
         ((0.3, -0.5, -0.8), (0.2, -0.8, -0.4))][i]
    Rr = [seal_r, ((0.15, -0.85, -0.3), (0.6, -0.4, 0.8)), seal_r,
          ((-0.5, 0.5, -0.7), (-0.2, 0.3, -1)),
          ((-0.5, 0.55, -0.65), (-0.2, 0.35, -1)),
          ((-0.35, 0.1, -1), (-0.1, -0.5, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*L[0]), V(*L[1])
    p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(*Rr[0]), V(*Rr[1])
    p["hand.L"] = {"rot": R.euler(x=[0, 0, 0, -75, -80, -20][i])}
    p["hand.R"] = {"blade": [V(-0.3, 0.35, -0.9), V(-0.35, 0.4, -0.85), V(-0.3, 0.45, -0.85),
                             V(-0.3, 0.55, -0.75), V(-0.3, 0.6, -0.7), V(-0.35, -0.3, -0.85)][i]}
    if i >= 3:
        p["legs"]["L"]["ankle"] = V(0.11, -0.10 if i < 5 else -0.05, AZ)
        p["legs"]["R"]["ankle"] = V(-0.11, 0.05 if i < 5 else 0.03, AZ)
        p["legs"]["L"]["pole"] = V(0.4, -1, 0)
        p["legs"]["R"]["pole"] = V(-0.4, -1, 0)
    wings(p, [4, 14, 6, 12, 10, -4][i], [0, -6, 4, 6, 8, 2][i], [2, 6, -8, -10, 4, 6][i],
          yaw=-0.7 * turn)
    p["qi_angle"] = [0, 40, 70, 160, 200, 230][i]
    return p


def shoot(i, n):
    """Bow (or thrown gourd) in the left hand: raise (0), draw (1), full draw (2), release on
    frame 3, follow-through (4), lower (5). The body turns side-on to the target."""
    p = stance()
    turn = [-14, -40, -45, -42, -36, -12][i]
    p["hips"]["loc"] = V(0, 0.0, -0.025)
    setrot(p, "hips", R.euler(z=turn * 0.4))
    setrot(p, "spine", R.euler(z=turn * 0.3, x=-2))
    setrot(p, "chest", R.euler(z=turn * 0.3, x=-3 if i in (2, 3) else 0))
    setrot(p, "head", R.euler(z=-turn * 0.85))
    p["legs"]["L"]["ankle"] = V(0.10, -0.07, 0.06)
    p["legs"]["R"]["ankle"] = V(-0.10, 0.06, 0.06)
    p["legs"]["L"]["pole"] = V(0.5, -1, 0)
    p["legs"]["R"]["pole"] = V(-0.5, -1, 0)
    bow = [((0.25, -0.8, -0.45), (0.15, -1, -0.15)),
           ((0.12, -1, 0.0), (0.05, -1, 0.08)),
           ((0.1, -1, 0.06), (0.04, -1, 0.1)),
           ((0.1, -1, 0.12), (0.04, -1, 0.2)),
           ((0.12, -1, 0.08), (0.06, -1, 0.1)),
           ((0.3, -0.6, -0.7), (0.15, -0.8, -0.5))][i]
    draw = [((0.15, -0.9, -0.45), (0.5, -0.8, 0.1)),
            ((-0.55, 0.15, 0.05), (0.55, -0.6, 0.25)),
            ((-0.75, 0.35, 0.12), (0.65, -0.35, 0.3)),
            ((-0.7, 0.6, 0.15), (-0.45, 0.85, 0.05)),
            ((-0.6, 0.55, -0.1), (-0.4, 0.6, -0.5)),
            ((-0.3, 0.1, -1), (-0.1, -0.5, -1))][i]
    for side, (ua, fa) in (("L", bow), ("R", draw)):
        p.pop(f"upper_arm.{side}")
        p.pop(f"forearm.{side}")
        p[f"upper_arm.{side}"] = {"waim": V(*ua)}
        p[f"forearm.{side}"] = {"waim": V(*fa)}
    setrot(p, "hand.L", R.euler(x=-80 if 1 <= i <= 4 else 0))
    wings(p, [0, -6, -8, 12, 8, 2][i], [4, 8, 10, 2, 0, 2][i], [2, 4, 2, -10, 4, 2][i],
          yaw=-0.7 * turn)
    p["qi_angle"] = 15.0 * i
    return p


def hit(i, n):
    """A sharp flinch: snapped back on frame 0, deepest on 1, half recovered on 2."""
    p = stance()
    k = [0.85, 1.0, 0.4][i]
    p["hips"]["loc"] = V(0, 0.06 * k, -0.02 - 0.03 * k)
    setrot(p, "hips", R.euler(x=-6 * k))
    setrot(p, "spine", R.euler(x=-12 * k))
    setrot(p, "chest", R.euler(x=-16 * k, y=6 * k))
    setrot(p, "head", R.euler(x=-20 * k, z=8 * k))
    p["upper_arm.L"]["aim"] = V(0.30 + 0.7 * k, 0.3 * k, -1 + 0.6 * k)
    p["forearm.L"]["aim"] = V(0.2 + 0.6 * k, -0.3, -1 + 0.9 * k)
    p["upper_arm.R"]["aim"] = V(-0.30 - 0.7 * k, 0.25 * k, -1 + 0.6 * k)
    p["forearm.R"]["aim"] = V(-0.2 - 0.6 * k, -0.4, -1 + 0.9 * k)
    p["legs"]["L"]["ankle"] = V(0.09, 0.03 * k, AZ)
    p["legs"]["R"]["ankle"] = V(-0.09, -0.02 * k, AZ)
    wings(p, [16, 22, 8][i], -6 * k, [10, 6, -6][i])
    p["qi_angle"] = 10.0 * i
    return p


def die(i, n):
    """Stagger (0), knees buckle (1), kneel (2), topple backwards (3, 4), lying still (5).
    The fallen body lies on its back, diagonally, knees up, centred over the pivot: the
    camera sees the ground at 35 degrees, so anything more than ~0.4 m in front of the
    pivot would fall out of the bottom of the 64 px frame, whichever way it faces."""
    p = stance()
    yaw = [0, 0, 0, 20, 45, 45][i]
    turn = R.euler(z=yaw)
    lying = turn @ V(0, -0.14, 0)
    hips = [((0, 0.03, -0.04), 0), ((0, 0.0, -0.11), 8), ((0, 0.0, -0.18), 5),
            ((0, -0.06, -0.23), -40), ((lying.x, lying.y, -0.27), -80), ((lying.x, lying.y, -0.28), -88)][i]
    p["hips"]["loc"] = V(*hips[0])
    setrot(p, "hips", R.euler(x=hips[1], z=yaw))
    # once down, the back curls a little (head and shoulders off the floor): a shorter
    # footprint, and the face stays visible
    setrot(p, "spine", R.euler(x=[-8, 14, 10, -6, 12, 16][i]))
    setrot(p, "chest", R.euler(x=[-10, 14, 12, -8, 14, 18][i]))
    setrot(p, "head", R.euler(x=[-14, 18, 20, -14, 10, 12][i], z=[0, 0, 0, 10, 18, 22][i]))
    arms = [((0.7, 0.3, -0.6), (0.5, -0.2, -0.6), (-0.7, 0.3, -0.6), (-0.5, -0.2, -0.6)),
            ((0.25, -0.3, -1), (0.1, -0.5, -1), (-0.25, -0.3, -1), (-0.1, -0.5, -1)),
            ((0.3, -0.1, -1), (0.2, -0.2, -1), (-0.3, -0.1, -1), (-0.2, -0.2, -1)),
            ((0.8, -0.4, 0.2), (0.6, -0.6, 0.4), (-0.8, -0.4, 0.2), (-0.6, -0.6, 0.4)),
            ((0.9, 0.1, 0.1), (0.8, 0.2, 0.2), (-0.9, 0.1, 0.1), (-0.8, 0.2, 0.2)),
            ((0.95, 0.15, -0.1), (0.85, 0.25, -0.05), (-0.95, 0.15, -0.1), (-0.85, 0.25, -0.05))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*arms[0]), V(*arms[1])
    p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(*arms[2]), V(*arms[3])
    p["hand.R"] = {}
    legs = [((0.08, 0.03, 0.06), (-0.08, 0.0, 0.06)),
            ((0.09, 0.0, 0.06), (-0.09, 0.02, 0.06)),
            ((0.09, 0.07, 0.04), (-0.09, 0.08, 0.04)),
            ((0.09, -0.05, 0.05), (-0.09, -0.02, 0.05)),
            ((0.10, -0.31, AZ), (-0.10, -0.31, AZ)),
            ((0.10, -0.31, AZ), (-0.11, -0.32, AZ))][i]
    poles = [V(0, -1, 0), V(0, -1, 0), V(0, -1, -0.2), V(0, -0.5, 1), V(0, -0.3, 1), V(0, -0.3, 1)][i]
    for s, a in zip("LR", legs):
        a = V(*a)
        if i >= 3:                       # the legs go round with the body's yaw (knees up)
            a = turn @ V(a.x, a.y, 0) + V(0, 0, a.z)
        p["legs"][s]["ankle"] = a
        p["legs"][s]["pole"] = turn @ (poles + V(0.3 if s == "L" else -0.3, 0, 0))
        p["legs"][s]["foot"] = turn @ [FOOT_FLAT, FOOT_FLAT, V(0, 0.2, -1), V(0, -0.5, -0.3),
                                       FOOT_FLAT, FOOT_FLAT][i]
    # falling and lying: the wings close up along the spine (toward the head), so they
    # stay inside the body's own footprint on the floor
    wings(p, [18, 0, -12, 90, 110, 110][i], [-6, 4, 14, -10, 35, 35][i], [8, -8, -6, 20, 30, 30][i])
    if i >= 3:     # lying: robe, hair and cape fall along the body toward the feet / the floor
        feet = turn @ V(0, -1, 0)
        p["hem"] = {b: feet + V(0, 0, -0.1) for b in ("hem_F", "hem_B", "hem.L", "hem.R")}
        p["cape_dir"] = feet + V(0, 0, -0.2)
    p["qi_angle"] = [10, 20, 30, 40, 45, 45][i]
    p["wing_scale"] = [1.0, 1.0, 0.9, 0.6, 0.45, 0.4][i]
    if i >= 4:
        p["wind"] = V(0, -0.2, 0.0)
    return p


def meditate(i, n):
    """Lotus seat (the last column of the reference): sat on the ground, legs crossed, hands
    resting on the knees, breathing; the robe pools round the legs, the hair floats."""
    p = stance()
    b = math.cos(math.tau * i / n)
    p["hips"]["loc"] = V(0, 0.01, -0.235 + 0.004 * b)
    setrot(p, "spine", R.euler(x=-1.5 * b))
    setrot(p, "chest", R.euler(x=-1.5 * b))
    setrot(p, "head", R.euler(x=4 + 1.5 * math.cos(math.tau * (i - 1) / n)))
    p["legs"]["L"].update(ankle=V(-0.04, -0.15, 0.045), pole=V(1, -0.35, 0.35), foot=V(-0.9, -0.3, 0.25))
    p["legs"]["R"].update(ankle=V(0.04, -0.12, 0.075), pole=V(-1, -0.35, 0.35), foot=V(0.9, -0.3, 0.25))
    p["upper_arm.L"]["aim"] = V(0.40, -0.40, -1)
    p["forearm.L"]["aim"] = V(0.20, -1.0, -0.35)
    p["upper_arm.R"]["aim"] = V(-0.40, -0.40, -1)
    p["forearm.R"]["aim"] = V(-0.20, -1.0, -0.35)
    p["hand.L"] = {"rot": R.euler(x=-40)}
    p["hand.R"] = {"rot": R.euler(x=-40)}
    p["hem"] = {"hem_F": V(0, -1, -0.45), "hem_B": V(0, 1, -0.6), "hem.L": V(1, -0.2, -0.5),
                "hem.R": V(-1, -0.2, -0.5)}
    p["cape_ground"] = True
    p["wind"] = V(0, 0, 0.25 + 0.1 * b)       # qi rising: hair and ribbons float
    wings(p, 10 + 5 * b, -8, -4 * math.sin(math.tau * i / n))
    p["qi_angle"] = 120.0 * i / n
    return p


def fly(i, n):
    """Ngự kiếm: a wide, steady stance on the flying sword (SOCKET_mount, a separate layer),
    raised above the ground point; robe, hair, cape and sleeves stream back."""
    p = stance()
    ph = math.tau * i / n
    lift = 0.11 + 0.012 * math.sin(ph)
    p["mount"] = {"loc": V(0, 0, lift)}
    p["hips"]["loc"] = V(0, 0.0, lift - 0.045)
    setrot(p, "hips", R.euler(z=-10))
    setrot(p, "spine", R.euler(x=6, z=4))
    setrot(p, "chest", R.euler(x=4, z=4))
    setrot(p, "head", R.euler(x=-4, z=4))
    p["legs"]["L"].update(ankle=V(0.12, -0.08, lift + 0.055), pole=V(0.6, -1, 0))
    p["legs"]["R"].update(ankle=V(-0.11, 0.08, lift + 0.055), pole=V(-0.6, -1, 0))
    p["legs"]["L"]["foot"] = V(0.25, -0.9, -0.38)
    p["legs"]["R"]["foot"] = V(-0.35, -0.85, -0.38)
    p["upper_arm.L"]["aim"] = V(0.85, 0.35, -0.45)
    p["forearm.L"]["aim"] = V(0.85, 0.3, -0.25)
    p["upper_arm.R"]["aim"] = V(-0.35, -0.85, -0.25)
    p["forearm.R"]["aim"] = V(-0.1, -1.0, 0.35)
    p["hand.R"] = {"rot": R.euler(x=-30)}
    p["wind"] = V(0, 1.15 + 0.25 * math.sin(ph * 2), 0.05 * math.cos(ph * 2))
    wings(p, 8 * math.cos(ph), 40, -8 * math.sin(ph))
    p["qi_angle"] = 120.0 * i / n
    return p


def dodge(i, n):
    """A short low dash forward: crouch (0), launch low and leaning hard (1), glide (2),
    plant and recover (3). In place: the game moves the character."""
    p = stance()
    lean = [14, 40, 32, 8][i]
    p["hips"]["loc"] = V(0, [0.0, -0.06, -0.05, -0.01][i], [-0.07, -0.11, -0.12, -0.04][i])
    setrot(p, "hips", R.euler(x=lean * 0.3))
    setrot(p, "spine", R.euler(x=lean * 0.35))
    setrot(p, "chest", R.euler(x=lean * 0.35))
    setrot(p, "head", R.euler(x=-lean * 0.7))
    arms = [((0.4, 0.4, -0.8), (0.2, 0.2, -1)), ((0.4, 0.95, -0.15), (0.25, 1.0, 0.05)),
            ((0.4, 0.85, -0.4), (0.25, 0.9, -0.3)), ((0.3, 0.0, -1), (0.12, -0.4, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*arms[0]), V(*arms[1])
    p["upper_arm.R"]["aim"] = V(-arms[0][0], arms[0][1], arms[0][2])
    p["forearm.R"]["aim"] = V(-arms[1][0], arms[1][1], arms[1][2])
    legs = [((0.09, -0.03, AZ), (-0.09, 0.04, AZ)),
            ((0.09, -0.12, AZ), (-0.09, 0.20, AZ + 0.06)),
            ((0.09, -0.10, AZ), (-0.09, 0.16, AZ + 0.02)),
            ((0.08, -0.04, AZ), (-0.08, 0.03, AZ))][i]
    for s, a in zip("LR", legs):
        p["legs"][s]["ankle"] = V(*a)
    if i in (1, 2):
        p["legs"]["R"]["foot"] = V(0, -0.5, -1)
    p["wind"] = V(0, [0.2, 1.3, 1.0, 0.2][i], 0)
    wings(p, [-6, -30, -26, 6][i], [8, 25, 22, 6][i], [4, -6, 4, 8][i])
    p["qi_angle"] = 20.0 * i
    return p


# name: (frames, fps, loop, hit frame or None, pose fn)
CLIPS = {
    "idle": (4, 6, True, None, idle),
    "walk": (8, 10, True, None, walk),
    "slash": (6, 14, False, 3, slash),
    "cast": (6, 12, False, 3, cast),
    "shoot": (6, 12, False, 3, shoot),
    "hit": (3, 12, False, None, hit),
    "die": (6, 10, False, None, die),
    "meditate": (4, 5, True, None, meditate),
    "fly": (4, 8, True, None, fly),
    "dodge": (4, 14, False, None, dodge),
}

FOLLOW = {  # chain: (stiffness, drag, gravity weight)
    "hair": (0.55, 5.0, 1.0),
    "ribbon.L": (0.30, 7.0, 1.0),
    "ribbon.R": (0.30, 7.0, 1.0),
    "cape": (0.55, 4.0, 1.0),
    "sleeve.L": (0.55, 3.0, 0.8),
    "sleeve.R": (0.55, 3.0, 0.8),
}
WIND_GAIN = {"hair": 0.9, "ribbon.L": 1.3, "ribbon.R": 1.3, "cape": 1.0, "sleeve.L": 0.6,
             "sleeve.R": 0.6, "hem": 0.35}


def _delta(posed, bone):
    parent = R.BONES[bone][2]
    return posed[parent].to_quaternion() @ R.REST[parent].to_quaternion().inverted()


def _rest_dir(bone):
    return (Vector(R.RIG_BONES[bone][1]) - Vector(R.RIG_BONES[bone][0])).normalized()


def follow_through(frames: list[dict], loop: bool) -> list[dict]:
    """Pass 2: hang the secondary chains off pass-1 bodies, lagging behind their motion."""
    n = len(frames)
    first = [R.solve(p)[1] for p in frames]

    def vel(name, i, lag):
        j = i - lag
        if loop:
            j %= n
            a = first[j][name].translation
            b = first[(j - 1) % n][name].translation
        else:
            if j <= 0:
                return Vector()
            a = first[j][name].translation
            b = first[j - 1][name].translation
        return a - b

    out = []
    for i, p in enumerate(frames):
        p = dict(p)
        # the camera looks down 35 degrees: the neck tips the head back a little in every
        # pose so the face (not the crown) is what the sprite shows
        p.setdefault("neck", {"rot": R.euler(x=-9)})
        posed = first[i]
        wind = Vector(p.get("wind", Vector()))
        for chain, bones in R.CHAINS.items():
            stiff, drag, grav = FOLLOW[chain]
            for k, bone in enumerate(bones):
                rigid = _delta(posed, bone) @ _rest_dir(bone)
                if chain == "cape" and "cape_dir" in p:
                    d = Vector(p["cape_dir"])
                elif chain == "cape" and p.get("cape_ground") and k > 0:
                    d = V(0, 1, -0.45 if k == 1 else -0.05)
                else:
                    d = (rigid * stiff + V(0, 0, -1) * (1 - stiff) * grav
                         + wind * WIND_GAIN[chain] * (0.7 + 0.3 * k)
                         - vel(bones[0], i, k + 1) * drag)
                if chain == "cape":           # the cape never swings into the body
                    back = _delta(posed, "cape_01") @ V(0, 1, 0)
                    if d.dot(back) < 0.05:
                        d += back * (0.05 - d.dot(back) + 0.1)
                    if wind.y < 0.5 and not p.get("cape_ground") and not p.get("hem"):
                        # standing clips: a cape kicked far back draws below the feet
                        # in the up-facing sprite
                        d = clamp_cone(d, V(0, 0, -1), 12)
                d = above_ground(posed[bone].translation, R.LEN[bone] * (k + 1), d)
                p[bone] = {"waim": d}
        # robe hem: follows the thighs (the skirt is pushed by the legs), lags the hips
        hem = p.get("hem")
        th = {s: posed[f"thigh.{s}"].to_quaternion() @ V(0, 1, 0) for s in "LR"}
        hv = vel("hem_F", i, 1)
        for bone in R.HEMS:
            rigid = _delta(posed, bone) @ _rest_dir(bone)
            if hem and bone in hem:
                d = Vector(hem[bone])
            else:
                if bone == "hem_F":
                    leg = min(th.values(), key=lambda v: v.y)
                    push = V(0, min(0.0, leg.y) * 1.2, 0)
                elif bone == "hem_B":
                    leg = max(th.values(), key=lambda v: v.y)
                    push = V(0, max(0.0, leg.y) * 1.2, 0)
                else:
                    s = bone[-1]
                    push = V(th[s].x * 0.8, th[s].y * 0.5, 0)
                d = rigid + push - hv * 2.0 + wind * WIND_GAIN["hem"]
                # a long robe must not kick out in front of the feet (it would draw below
                # the pivot): keep every hem within 24 degrees of hanging straight down
                down = V(0, 0, -1)
                d.normalize()
                ang = d.angle(down)
                if ang > math.radians(24):
                    axis = down.cross(d)
                    if axis.length > 1e-6:
                        d = Quaternion(axis.normalized(), math.radians(24)) @ down
            d = above_ground(posed[bone].translation, R.LEN[bone], d)
            p[bone] = {"waim": d}
            if p.get("hem_scale"):           # a lying robe bunches up instead of spreading
                p[bone]["scale"] = p["hem_scale"]
        # wings: flap about the body's front-back axis, fold back, the tip lagging
        flap, fold, lag, yaw = (list(p.get("wing", (0, 0, 0, 0))) + [0, 0, 0, 0])[:4]
        flap, lag = flap * 0.55, lag * 0.6      # the 64 px frame has no room for big flaps
        for s, sg in (("L", 1), ("R", -1)):
            p[f"wing_01.{s}"] = {"rot": R.euler(y=-sg * flap, z=sg * fold + yaw)}
            p[f"wing_02.{s}"] = {"rot": R.euler(y=-sg * lag)}
            if f"wing_03.{s}" in R.BONES:             # the wing hand trails the forearm
                p[f"wing_03.{s}"] = {"rot": R.euler(y=-sg * lag * 1.4, z=sg * fold * 0.25)}
            if p.get("wing_scale", 1.0) != 1.0:      # the qi wings fade as he dies
                p[f"wing_01.{s}"]["scale"] = p["wing_scale"]
        p["qi"] = {"rot": R.euler(z=p.get("qi_angle", 0.0))}
        out.append(p)
    return out


def build_actions(rig) -> dict:
    """Make one action per clip on `rig`. Returns {clip: action}."""
    R.load_rest(rig)
    rig.animation_data_create()
    actions = {}
    for name, (n, fps, loop, hit_frame, fn) in CLIPS.items():
        poses = follow_through([fn(i, n) for i in range(n)], loop)
        act = __import__("bpy").data.actions.new(name)
        act.use_fake_user = True
        rig.animation_data.action = act
        prev = {}
        # a loop gets a closing key (= its first pose) one frame after the last, so the kit
        # samples frame_start + i * (end - start) / n on whole frames
        keyed = poses + ([poses[0]] if loop else [])
        for i, p in enumerate(keyed):
            basis, _ = R.solve(p)
            R.key_pose(rig, basis, R.FRAME0 + i, prev)
        act.use_frame_range = True
        act.frame_start = R.FRAME0
        act.frame_end = R.FRAME0 + len(keyed) - 1
        act.use_cyclic = loop
        act["frames"] = n
        act["fps"] = fps
        act["loop"] = loop
        if hit_frame is not None:
            act["hit"] = hit_frame
        actions[name] = act
    return actions
