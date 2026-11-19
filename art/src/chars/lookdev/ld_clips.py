"""Look-dev v2 clips: idle, walk, slash, built from the reference's poses (runs inside
Blender). Same conventions as ../clips.py: rot in rest axes (rx + tips the top forward,
rz + turns to the left), arm `aim`s in the chest's frame, `blade` = where the held sword
points, legs = ankle targets. The figure faces -Y; its right hand (-X) holds the sword."""
from __future__ import annotations

import math

from mathutils import Vector

import clips as C
import rig as R

AZ = R.RIG_BONES["foot.L"][0][2]
FOOT_FLAT = Vector((0, -0.93, -0.36))


def V(*a):
    return Vector(a)


def setrot(p, bone, q):
    p.setdefault(bone, {})["rot"] = q


def stance() -> dict:
    """The reference's ready stance: feet apart, the left foot a little forward, knees
    soft, weight on the back leg, the body turned a touch to the right, the sword held low
    and forward in the right hand, the left arm loose and slightly away from the body."""
    p = {
        "neck": {},                                     # the 15 degree camera sees the face
        "hips": {"loc": V(-0.012, 0.0, -0.04), "rot": R.euler(z=-12, y=-2)},
        "spine": {"rot": R.euler(z=4)},
        "chest": {"rot": R.euler(z=6, x=2)},
        "head": {"rot": R.euler(z=4, x=-8)},             # chin up: the face, not the fringe
        "upper_arm.L": {"aim": V(0.32, 0.0, -1)},
        "forearm.L": {"aim": V(0.22, -0.35, -1)},
        "upper_arm.R": {"aim": V(-0.30, -0.12, -1)},
        "forearm.R": {"aim": V(-0.12, -0.75, -0.75)},
        "hand.R": {"blade": V(-0.50, -0.62, -0.55)},
        "legs": {"L": {"ankle": V(0.125, -0.05, AZ), "pole": V(0.45, -1, 0), "foot": V(0.3, -0.93, -0.36)},
                 "R": {"ankle": V(-0.115, 0.05, AZ), "pole": V(-0.45, -1, 0), "foot": V(-0.35, -0.9, -0.36)}},
        "wind": V(0, 0, 0),
        "wing": (0.0, 0.0, 0.0, 0.0),
        "qi_angle": 0.0,
    }
    return p


def idle(i, n):
    p = stance()
    b = math.cos(math.tau * i / n)
    lag = math.cos(math.tau * (i - 1) / n)
    p["hips"]["loc"] = V(-0.012 - 0.004 * b, 0.0, -0.04 + 0.005 * b)
    setrot(p, "chest", R.euler(z=6, x=2 - 1.5 * b))
    setrot(p, "head", R.euler(z=4, x=-8 + 1.5 * lag))
    p["upper_arm.L"]["aim"] = V(0.32 + 0.03 * b, 0.0, -1)
    p["forearm.R"]["aim"] = V(-0.12, -0.75 - 0.05 * b, -0.75)
    p["wind"] = V(0.0, 0.08 * math.sin(math.tau * i / n), 0)
    return p


def walk(i, n):
    """A real stride: heel strike on frames 0 and 4, down, passing, up; opposite arm swing;
    the planted foot moves back at walking speed (in place)."""
    p = stance()
    ph = i / n
    S = 0.10
    for s, off in (("L", 0.0), ("R", 0.5)):
        q = (ph + off) % 1.0
        x = 0.05 if s == "L" else -0.05
        if q < 0.5:                         # planted
            t = q / 0.5
            y = -S + 2 * S * t
            z = AZ
            foot = V(0, -1, 0.12) if t < 0.12 else (FOOT_FLAT if t < 0.75 else V(0, -0.93, -0.42))
        else:                               # swing
            t = (q - 0.5) / 0.5
            y = S - 2 * S * (t * t * (3 - 2 * t))
            z = AZ + 0.065 * math.sin(math.pi * t)
            foot = V(0, -0.93, -0.45) if t < 0.4 else V(0, -1, 0.1)
        p["legs"][s] = {"ankle": V(x, y, z), "pole": V(0.15 if s == "L" else -0.15, -1, 0), "foot": foot}
    bob = [-0.004, -0.018, -0.006, 0.004][i % 4]
    c = math.cos(math.tau * ph)
    p["hips"] = {"loc": V(0, 0, -0.012 + bob), "rot": R.euler(z=-9 * c, y=3 * math.sin(math.tau * ph * 2))}
    setrot(p, "spine", R.euler(x=3, z=4 * c))
    setrot(p, "chest", R.euler(z=9 * c, x=2))
    setrot(p, "head", R.euler(z=-5 * c, x=-8))
    p["upper_arm.L"]["aim"] = V(0.24, 0.55 * c, -1)
    p["forearm.L"]["aim"] = V(0.16, 0.35 * c - 0.35, -1)
    p["upper_arm.R"]["aim"] = V(-0.24, -0.35 * c - 0.05, -1)
    p["forearm.R"]["aim"] = V(-0.10, -0.75 - 0.25 * max(0.0, -c), -0.8)
    p["hand.R"] = {"blade": V(-0.45, -0.72 - 0.12 * c, -0.12)}
    p["wind"] = V(0, 0.35, 0)
    return p


def slash(i, n):
    """Wind-up with the body coiled to the right and the sword cocked over the right
    shoulder (0-1), the lunge onto the front (right) leg as the arm sweeps over (2), the
    strike with the arm and sword fully extended forward on the hit frame (3), the
    follow-through low across to the left (4), the recovery (5)."""
    p = stance()
    K = [  # turn, lean, hips (x, y, z), upper.R, fore.R, blade, L ankle (x,y), R ankle (x,y)
        (-40, -6, (0.0, 0.03, -0.04), (-0.65, 0.35, 0.65), (-0.30, 0.35, 0.95), (-0.25, 0.15, 0.95),
         (0.10, -0.06), (-0.10, 0.08)),
        (-55, -10, (0.0, 0.05, -0.05), (-0.55, 0.55, 0.65), (-0.05, 0.75, 0.70), (-0.05, 0.22, 0.97),
         (0.10, -0.06), (-0.10, 0.09)),
        (-10, 8, (0.0, -0.02, -0.06), (-0.40, -0.85, 0.45), (-0.20, -1.0, 0.40), (-0.05, -0.55, 0.85),
         (0.10, 0.0), (-0.09, -0.05)),
        (35, 16, (0.0, -0.045, -0.10), (0.05, -1.0, -0.05), (0.08, -1.0, -0.08), (0.30, -0.85, -0.42),
         (0.11, 0.08), (-0.08, -0.17)),
        (50, 20, (0.0, -0.075, -0.105), (0.45, -0.75, -0.40), (0.65, -0.45, -0.55), (0.75, 0.10, -0.40),
         (0.11, 0.08), (-0.08, -0.17)),
        (15, 6, (0.0, -0.03, -0.05), (-0.20, -0.45, -0.85), (-0.10, -0.85, -0.50), (-0.35, -0.70, -0.38),
         (0.10, 0.02), (-0.09, -0.08)),
    ]
    turn, lean, (hx, hy, hz), ua, fa, blade, la, ra = K[i]
    p["hips"] = {"loc": V(hx, hy, hz), "rot": R.euler(z=turn * 0.35)}
    setrot(p, "spine", R.euler(x=lean * 0.5, z=turn * 0.3))
    setrot(p, "chest", R.euler(x=lean * 0.5, z=turn * 0.35))
    setrot(p, "head", R.euler(x=-lean * 0.4 - 6, z=-turn * 0.6))
    p["upper_arm.R"]["aim"] = V(*ua)
    p["forearm.R"]["aim"] = V(*fa)
    p["hand.R"] = {"blade": V(*blade)}
    # the free arm: forward to aim on the wind-up, flung back for balance on the strike
    L = [((0.40, -0.80, -0.20), (0.30, -0.95, 0.10)), ((0.45, -0.85, -0.05), (0.35, -0.95, 0.2)),
         ((0.55, 0.10, -0.80), (0.40, 0.30, -0.85)), ((0.70, 0.55, -0.35), (0.65, 0.65, -0.35)),
         ((0.70, 0.55, -0.35), (0.65, 0.65, -0.35)), ((0.35, 0.10, -1), (0.20, -0.30, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*L[0]), V(*L[1])
    p["legs"]["L"] = {"ankle": V(la[0], la[1], AZ), "pole": V(0.6, -1, 0), "foot": V(0.45, -0.85, -0.3)}
    p["legs"]["R"] = {"ankle": V(ra[0], ra[1], AZ + (0.05 if i == 2 else 0.0)), "pole": V(-0.3, -1, 0),
                      "foot": V(-0.15, -0.95, -0.3)}
    p["wind"] = V(0, [0.0, 0.1, 0.5, 0.8, 0.5, 0.1][i], 0)
    return p


CLIPS = {
    "idle": (4, 6, True, None, idle),
    "walk": (8, 10, True, None, walk),
    "slash": (6, 14, False, 3, slash),
}
CLIPS_KIT = {"idle": dict(frames=4, fps=6, loop=True), "walk": dict(frames=8, fps=10, loop=True),
             "slash": dict(frames=6, fps=14, loop=False, events={"hit": 3})}


def install():
    C.CLIPS.clear()
    C.CLIPS.update(CLIPS)


install()
