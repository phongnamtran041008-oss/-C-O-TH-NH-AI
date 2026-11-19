"""The ten player clips on the v2 rig (runs inside Blender), empty-handed.

Poses follow the reference and the approved look-dev. The right fist keeps a grip pose and a
`blade` direction in every clip, so a weapon layer rendered later on SOCKET_weapon_r lands
naturally (bare-handed the slash reads as a sword-finger / palm strike). Conventions as in
../clips.py: rot in rest axes (rx + tips the top forward, rz + turns left), arm `aim`s in the
chest's frame, legs = ankle targets; the figure faces -Y; wings = (flap, fold, lag, yaw).
"""
from __future__ import annotations

import math

from mathutils import Vector

import clips as C
import rig as R
from ld_clips import AZ, FOOT_FLAT, V, setrot

HIP_Z = R.RIG_BONES["hips"][0][2]           # 0.47


def stance() -> dict:
    """Relaxed ready stance: feet apart, left foot a little forward, knees soft, the body a
    touch turned, the right hand a loose fist by the hip (a held weapon would point low and
    forward), the left arm loose and away from the body; head level so the face shows."""
    return {
        "neck": {},
        "hips": {"loc": V(-0.006, 0.0, -0.035), "rot": R.euler(z=-10, y=-2)},
        "spine": {"rot": R.euler(z=4)},
        "chest": {"rot": R.euler(z=6, x=2)},
        "head": {"rot": R.euler(z=4, x=-8)},
        "upper_arm.L": {"aim": V(0.34, 0.0, -1)},
        "forearm.L": {"aim": V(0.24, -0.35, -1)},
        "upper_arm.R": {"aim": V(-0.30, -0.06, -1)},
        "forearm.R": {"aim": V(-0.16, -0.55, -0.85)},
        "hand.R": {"blade": V(-0.50, -0.62, -0.55)},
        "legs": {"L": {"ankle": V(0.11, -0.045, AZ), "pole": V(0.4, -1, 0), "foot": V(0.3, -0.93, -0.36)},
                 "R": {"ankle": V(-0.105, 0.045, AZ), "pole": V(-0.4, -1, 0), "foot": V(-0.35, -0.9, -0.36)}},
        "wind": V(0, 0, 0),
        "wing": (0.0, 0.0, 0.0, 0.0),
        "qi_angle": 0.0,
    }


def idle(i, n):
    p = stance()
    b = math.cos(math.tau * i / n)
    lag = math.cos(math.tau * (i - 1) / n)
    p["hips"]["loc"] = V(-0.006 - 0.004 * b, 0.0, -0.035 + 0.005 * b)
    setrot(p, "chest", R.euler(z=6, x=2 - 1.5 * b))
    setrot(p, "head", R.euler(z=4, x=-8 + 1.5 * lag))
    p["upper_arm.L"]["aim"] = V(0.34 + 0.03 * b, 0.0, -1)
    p["wind"] = V(0.0, 0.08 * math.sin(math.tau * i / n), 0)
    p["wing"] = (22 * b, 6, -8 * math.sin(math.tau * i / n), 0)         # slow breathing flap (~12 deg)
    return p


def walk(i, n):
    """A real stride: heel strike on frames 0 and 4, down, passing, up; opposite arm swing."""
    p = stance()
    ph = i / n
    S = 0.10
    for s, off in (("L", 0.0), ("R", 0.5)):
        q = (ph + off) % 1.0
        x = 0.05 if s == "L" else -0.05
        if q < 0.5:
            t = q / 0.5
            y, z = -S + 2 * S * t, AZ
            foot = V(0, -1, 0.12) if t < 0.12 else (FOOT_FLAT if t < 0.75 else V(0, -0.93, -0.42))
        else:
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
    p["upper_arm.R"]["aim"] = V(-0.24, -0.45 * c - 0.05, -1)
    p["forearm.R"]["aim"] = V(-0.12, -0.45 * c - 0.45, -0.9)
    p["hand.R"] = {"blade": V(-0.45, -0.72 - 0.12 * c, -0.25)}
    p["wind"] = V(0, 0.35, 0)
    p["wing"] = (6 * math.cos(math.tau * ph * 2), 22, -5 * math.sin(math.tau * ph * 2), 0)   # swept back
    return p


def slash(i, n):
    """Coiled wind-up with the fist cocked over the right shoulder (0-1), the lunge as the
    arm sweeps over (2), the strike fully extended forward on the hit frame (3), the
    follow-through low to the left (4), recovery (5). Wings spread wide on the hit."""
    p = stance()
    K = [  # turn, lean, hips (x, y, z), upper.R, fore.R, blade, L ankle, R ankle
        (-40, -6, (0.0, 0.03, -0.045), (-0.65, 0.35, 0.65), (-0.30, 0.35, 0.95), (-0.25, 0.15, 0.95),
         (0.10, -0.06), (-0.10, 0.08)),
        (-55, -10, (0.0, 0.05, -0.055), (-0.55, 0.55, 0.65), (-0.05, 0.75, 0.70), (-0.05, 0.22, 0.97),
         (0.10, -0.06), (-0.10, 0.09)),
        (-10, 8, (0.0, -0.02, -0.065), (-0.40, -0.85, 0.45), (-0.20, -1.0, 0.40), (-0.05, -0.55, 0.85),
         (0.10, 0.0), (-0.09, -0.05)),
        (35, 16, (0.0, -0.045, -0.10), (0.05, -1.0, -0.05), (0.08, -1.0, -0.08), (0.30, -0.85, -0.42),
         (0.11, 0.08), (-0.08, -0.17)),
        (50, 20, (0.0, -0.05, -0.105), (0.45, -0.75, -0.40), (0.65, -0.45, -0.55), (0.75, 0.10, -0.40),
         (0.11, 0.08), (-0.08, -0.17)),
        (15, 6, (0.0, -0.03, -0.055), (-0.20, -0.45, -0.85), (-0.10, -0.85, -0.50), (-0.35, -0.70, -0.38),
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
    L = [((0.40, -0.80, -0.20), (0.30, -0.95, 0.10)), ((0.45, -0.85, -0.05), (0.35, -0.95, 0.2)),
         ((0.55, 0.10, -0.80), (0.40, 0.30, -0.85)), ((0.70, 0.55, -0.35), (0.65, 0.65, -0.35)),
         ((0.70, 0.55, -0.35), (0.65, 0.65, -0.35)), ((0.35, 0.10, -1), (0.20, -0.30, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*L[0]), V(*L[1])
    p["legs"]["L"] = {"ankle": V(la[0], la[1], AZ), "pole": V(0.6, -1, 0), "foot": V(0.45, -0.85, -0.3)}
    p["legs"]["R"] = {"ankle": V(ra[0], ra[1], AZ + (0.05 if i == 2 else 0.0)), "pole": V(-0.3, -1, 0),
                      "foot": V(-0.15, -0.95, -0.3)}
    p["wind"] = V(0, [0.0, 0.1, 0.5, 0.8, 0.5, 0.1][i], 0)
    p["wing"] = ([-8, -14, 10, 26, 18, 4][i], [14, 18, 0, -16, -8, 6][i], [4, 8, -12, -6, 6, 4][i], -0.7 * turn)
    return p


def cast(i, n):
    """Hand seal at the chest (0), raised to the chin while gathering (1), the left palm
    drawn back (2), a lunge and a decisive palm thrust at full reach on frame 3, held (4),
    recover (5). The right fist stays low and back (a held weapon points down-back)."""
    p = stance()
    turn = [0, 0, 28, -30, -34, -8][i]
    lean = [2, -4, -2, 14, 18, 4][i]
    hz = [-0.04, -0.06, -0.06, -0.09, -0.095, -0.04][i]
    hy = [0, 0.01, 0.02, -0.04, -0.05, -0.015][i]
    p["hips"] = {"loc": V(0, hy, hz), "rot": R.euler(z=turn * 0.3)}
    setrot(p, "spine", R.euler(x=lean * 0.5, z=turn * 0.3))
    setrot(p, "chest", R.euler(x=lean * 0.5, z=turn * 0.4))
    setrot(p, "head", R.euler(x=-lean * 0.5 - 6 + (6 if i == 1 else 0), z=-turn * 0.6))
    seal_l = ((-0.2, -0.75, -0.6), (-0.8, -0.45, 0.45))
    seal_r = ((0.2, -0.75, -0.6), (0.8, -0.45, 0.45))
    Lp = [seal_l, ((-0.15, -0.85, -0.3), (-0.6, -0.4, 0.8)), ((0.5, 0.5, -0.7), (0.3, 0.2, -1)),
          ((0.3, -1.0, 0.18), (0.3, -1.0, 0.2)), ((0.3, -1.0, 0.22), (0.3, -1.0, 0.25)),
          ((0.3, -0.5, -0.8), (0.2, -0.8, -0.4))][i]
    Rp = [seal_r, ((0.15, -0.85, -0.3), (0.6, -0.4, 0.8)), seal_r, ((-0.5, 0.5, -0.7), (-0.2, 0.3, -1)),
          ((-0.5, 0.55, -0.65), (-0.2, 0.35, -1)), ((-0.35, 0.1, -1), (-0.1, -0.5, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*Lp[0]), V(*Lp[1])
    p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(*Rp[0]), V(*Rp[1])
    p["hand.L"] = {"rot": R.euler(x=[0, 0, 0, -75, -80, -20][i])}
    p["hand.R"] = {"blade": [V(-0.3, 0.35, -0.9), V(-0.35, 0.4, -0.85), V(-0.3, 0.45, -0.85), V(-0.3, 0.55, -0.75),
                             V(-0.3, 0.6, -0.7), V(-0.35, -0.3, -0.85)][i]}
    if i >= 3:
        p["legs"]["L"] = {"ankle": V(0.11, -0.12 if i < 5 else -0.06, AZ), "pole": V(0.4, -1, 0), "foot": FOOT_FLAT.copy()}
        p["legs"]["R"] = {"ankle": V(-0.11, 0.08 if i < 5 else 0.04, AZ), "pole": V(-0.4, -1, 0), "foot": FOOT_FLAT.copy()}
    p["wing"] = ([4, 14, 6, 24, 18, -4][i], [4, -4, 8, -14, -8, 2][i], [2, 6, -8, -10, 4, 6][i], -0.7 * turn)
    p["qi_angle"] = [0, 40, 70, 160, 200, 230][i]
    return p


def shoot(i, n):
    """Bow draw: the left arm out holding the bow, the right hand pulls to the cheek, the
    body turned side-on; release on frame 3, follow-through, lower."""
    p = stance()
    turn = [-14, -40, -45, -42, -36, -12][i]
    p["hips"] = {"loc": V(0, 0.0, -0.035), "rot": R.euler(z=turn * 0.4)}
    setrot(p, "spine", R.euler(z=turn * 0.3, x=-2))
    setrot(p, "chest", R.euler(z=turn * 0.3, x=-3 if i in (2, 3) else 0))
    setrot(p, "head", R.euler(z=-turn * 0.85, x=-6))
    p["legs"]["L"] = {"ankle": V(0.12, -0.08, AZ), "pole": V(0.5, -1, 0), "foot": FOOT_FLAT.copy()}
    p["legs"]["R"] = {"ankle": V(-0.12, 0.07, AZ), "pole": V(-0.5, -1, 0), "foot": FOOT_FLAT.copy()}
    bow = [((0.25, -0.8, -0.45), (0.15, -1, -0.15)), ((0.12, -1, 0.0), (0.05, -1, 0.08)),
           ((0.1, -1, 0.06), (0.04, -1, 0.1)), ((0.1, -1, 0.12), (0.04, -1, 0.2)),
           ((0.12, -1, 0.08), (0.06, -1, 0.1)), ((0.3, -0.6, -0.7), (0.15, -0.8, -0.5))][i]
    draw = [((0.15, -0.9, -0.45), (0.5, -0.8, 0.1)), ((-0.55, 0.15, 0.05), (0.55, -0.6, 0.25)),
            ((-0.75, 0.35, 0.12), (0.65, -0.35, 0.3)), ((-0.7, 0.6, 0.15), (-0.45, 0.85, 0.05)),
            ((-0.6, 0.55, -0.1), (-0.4, 0.6, -0.5)), ((-0.3, 0.1, -1), (-0.1, -0.5, -1))][i]
    for side, (ua, fa) in (("L", bow), ("R", draw)):
        p[f"upper_arm.{side}"] = {"waim": V(*ua)}
        p[f"forearm.{side}"] = {"waim": V(*fa)}
    p["hand.L"] = {"rot": R.euler(x=-80 if 1 <= i <= 4 else 0)}
    p["hand.R"] = {}
    p["wing"] = ([0, -6, -8, 18, 10, 2][i], [6, 10, 12, -6, 0, 4][i], [2, 4, 2, -10, 4, 2][i], -0.7 * turn)
    return p


def hit(i, n):
    p = stance()
    k = [0.85, 1.0, 0.4][i]
    p["hips"] = {"loc": V(0, 0.045 * k, -0.03 - 0.035 * k), "rot": R.euler(x=-6 * k)}
    setrot(p, "spine", R.euler(x=-12 * k))
    setrot(p, "chest", R.euler(x=-16 * k, y=6 * k))
    setrot(p, "head", R.euler(x=-20 * k - 4, z=8 * k))
    p["upper_arm.L"]["aim"] = V(0.30 + 0.7 * k, 0.3 * k, -1 + 0.6 * k)
    p["forearm.L"]["aim"] = V(0.2 + 0.6 * k, -0.3, -1 + 0.9 * k)
    p["upper_arm.R"]["aim"] = V(-0.30 - 0.7 * k, 0.25 * k, -1 + 0.6 * k)
    p["forearm.R"]["aim"] = V(-0.2 - 0.6 * k, -0.4, -1 + 0.9 * k)
    p["legs"]["L"]["ankle"] = V(0.10, 0.03 * k, AZ)
    p["legs"]["R"]["ankle"] = V(-0.10, -0.02 * k, AZ)
    p["wing"] = ([18, 24, 8][i], -6 * k, [10, 6, -6][i], 0)
    return p


def die(i, n):
    """Stagger (0), knees buckle (1), kneel (2), topple backwards (3, 4), lying still (5):
    on the back, knees up, a little diagonal, centred over the pivot; the wings close up
    along the spine and fade."""
    p = stance()
    yaw = [0, 0, 0, 15, 30, 30][i]
    turn = R.euler(z=yaw)
    lying = turn @ V(0, -0.16, 0)
    hips = [((0, 0.03, -0.05), 0), ((0, 0.0, -0.14), 8), ((0, 0.0, -0.23), 5),
            ((0, -0.06, -0.30), -40), ((lying.x, lying.y, -0.36), -80), ((lying.x, lying.y, -0.37), -88)][i]
    p["hips"] = {"loc": V(*hips[0]), "rot": R.euler(x=hips[1], z=yaw)}
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
    legs = [((0.09, 0.03, AZ), (-0.09, 0.0, AZ)), ((0.10, 0.0, AZ), (-0.10, 0.02, AZ)),
            ((0.10, 0.08, AZ - 0.01), (-0.10, 0.09, AZ - 0.01)), ((0.10, -0.06, AZ), (-0.10, -0.03, AZ)),
            ((0.11, -0.40, AZ), (-0.11, -0.40, AZ)), ((0.11, -0.40, AZ), (-0.12, -0.41, AZ))][i]
    poles = [V(0, -1, 0), V(0, -1, 0), V(0, -1, -0.2), V(0, -0.5, 1), V(0, -0.3, 1), V(0, -0.3, 1)][i]
    for s, a in zip("LR", legs):
        a = V(*a)
        if i >= 3:
            a = turn @ V(a.x, a.y, 0) + V(0, 0, a.z)
        p["legs"][s] = {"ankle": a, "pole": turn @ (poles + V(0.3 if s == "L" else -0.3, 0, 0)),
                        "foot": turn @ [FOOT_FLAT, FOOT_FLAT, V(0, 0.2, -1), V(0, -0.5, -0.3), FOOT_FLAT, FOOT_FLAT][i]}
    p["wing"] = ([18, 0, -12, 90, 110, 110][i], [-6, 4, 14, -10, 35, 35][i], [8, -8, -6, 20, 30, 30][i], 0)
    p["wing_scale"] = [1.0, 1.0, 0.9, 0.6, 0.45, 0.4][i]
    if i >= 3:
        feet = turn @ V(0, -1, 0)
        p["hem"] = {b: feet + V(0, 0, -0.1) for b in ("hem_F", "hem_B", "hem.L", "hem.R")}
        p["cape_dir"] = feet + V(0, 0, -0.2)
        p["hem_scale"] = [1.0, 1.0, 1.0, 0.85, 0.65, 0.6][i]
    p["qi_angle"] = [10, 20, 30, 40, 45, 45][i]
    return p


def meditate(i, n):
    """Lotus seat: sat on the ground, legs crossed, hands resting on the knees palms up,
    breathing; robe pooled round the legs, hair and ribbons lifted by rising qi."""
    p = stance()
    b = math.cos(math.tau * i / n)
    p["hips"] = {"loc": V(0, 0.01, -0.335 + 0.004 * b)}
    setrot(p, "spine", R.euler(x=-1.5 * b))
    setrot(p, "chest", R.euler(x=-1.5 * b))
    setrot(p, "head", R.euler(x=-4 + 1.5 * math.cos(math.tau * (i - 1) / n)))
    p["legs"]["L"] = {"ankle": V(-0.05, -0.17, 0.05), "pole": V(1, -0.35, 0.35), "foot": V(-0.9, -0.3, 0.25)}
    p["legs"]["R"] = {"ankle": V(0.05, -0.14, 0.085), "pole": V(-1, -0.35, 0.35), "foot": V(0.9, -0.3, 0.25)}
    p["upper_arm.L"]["aim"] = V(0.40, -0.40, -1)
    p["forearm.L"]["aim"] = V(0.25, -1.0, -0.35)
    p["upper_arm.R"]["aim"] = V(-0.40, -0.40, -1)
    p["forearm.R"]["aim"] = V(-0.25, -1.0, -0.35)
    p["hand.L"] = {"rot": R.euler(x=-40)}
    p["hand.R"] = {"rot": R.euler(x=-40)}
    p["hem"] = {"hem_F": V(0, -1, -0.45), "hem_B": V(0, 1, -0.6), "hem.L": V(1, -0.2, -0.5), "hem.R": V(-1, -0.2, -0.5)}
    p["cape_ground"] = True
    p["wind"] = V(0, 0, 0.25 + 0.1 * b)
    p["wing"] = (12 + 5 * b, -6, -4 * math.sin(math.tau * i / n), 0)
    p["qi_angle"] = 120.0 * i / n
    return p


def fly(i, n):
    """Standing on the flying sword (SOCKET_mount, a separate layer), raised above the ground
    point: a wide steady stance, robe, hair, cape streaming back, wings swept back."""
    p = stance()
    ph = math.tau * i / n
    lift = 0.12 + 0.012 * math.sin(ph)
    p["mount"] = {"loc": V(0, 0, lift)}
    p["hips"] = {"loc": V(0, 0.0, lift - 0.06), "rot": R.euler(z=-12)}
    setrot(p, "spine", R.euler(x=6, z=4))
    setrot(p, "chest", R.euler(x=4, z=6))
    setrot(p, "head", R.euler(x=-10, z=4))
    p["legs"]["L"] = {"ankle": V(0.13, -0.10, lift + AZ), "pole": V(0.6, -1, 0), "foot": V(0.25, -0.9, -0.38)}
    p["legs"]["R"] = {"ankle": V(-0.12, 0.10, lift + AZ), "pole": V(-0.6, -1, 0), "foot": V(-0.35, -0.85, -0.38)}
    p["upper_arm.L"]["aim"] = V(0.85, 0.35, -0.45)
    p["forearm.L"]["aim"] = V(0.85, 0.3, -0.25)
    p["upper_arm.R"]["aim"] = V(-0.35, -0.85, -0.25)
    p["forearm.R"]["aim"] = V(-0.1, -1.0, 0.35)
    p["hand.R"] = {"rot": R.euler(x=-30)}
    p["wind"] = V(0, 1.15 + 0.25 * math.sin(ph * 2), 0.05 * math.cos(ph * 2))
    p["wing"] = (8 * math.cos(ph), 40, -8 * math.sin(ph), 0)
    p["qi_angle"] = 120.0 * i / n
    return p


def dodge(i, n):
    """A short low dash forward: crouch (0), launch low and leaning (1), glide (2), recover."""
    p = stance()
    lean = [14, 38, 30, 8][i]
    p["hips"] = {"loc": V(0, [0.0, -0.06, -0.05, -0.01][i], [-0.08, -0.13, -0.14, -0.05][i]), "rot": R.euler(x=lean * 0.3)}
    setrot(p, "spine", R.euler(x=lean * 0.35))
    setrot(p, "chest", R.euler(x=lean * 0.35))
    setrot(p, "head", R.euler(x=-lean * 0.7 - 6))
    arms = [((0.4, 0.4, -0.8), (0.2, 0.2, -1)), ((0.4, 0.95, -0.15), (0.25, 1.0, 0.05)),
            ((0.4, 0.85, -0.4), (0.25, 0.9, -0.3)), ((0.3, 0.0, -1), (0.12, -0.4, -1))][i]
    p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(*arms[0]), V(*arms[1])
    p["upper_arm.R"]["aim"] = V(-arms[0][0], arms[0][1], arms[0][2])
    p["forearm.R"]["aim"] = V(-arms[1][0], arms[1][1], arms[1][2])
    p["hand.R"] = {"blade": V(-0.2, 0.6, -0.75)}
    legs = [((0.10, -0.04, AZ), (-0.10, 0.05, AZ)), ((0.10, -0.15, AZ), (-0.10, 0.22, AZ + 0.07)),
            ((0.10, -0.12, AZ), (-0.10, 0.18, AZ + 0.03)), ((0.09, -0.05, AZ), (-0.09, 0.04, AZ))][i]
    for s, a in zip("LR", legs):
        p["legs"][s] = {"ankle": V(*a), "pole": V(0.2 if s == "L" else -0.2, -1, 0), "foot": FOOT_FLAT.copy()}
    if i in (1, 2):
        p["legs"]["R"]["foot"] = V(0, -0.5, -1)
    p["wind"] = V(0, [0.2, 1.3, 1.0, 0.2][i], 0)
    p["wing"] = ([-6, 6, 4, 6][i], [8, 30, 26, 6][i], [4, -8, 4, 8][i], 0)
    p["qi_angle"] = 20.0 * i
    return p


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


def install():
    C.CLIPS.clear()
    C.CLIPS.update(CLIPS)


install()
