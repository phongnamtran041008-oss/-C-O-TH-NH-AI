"""Ma Trận Thú (guardian lion, elite) and Phong Lang (wind wolf): one quadruped rig, one
clip generator, two bodies. Runs inside Blender; see creatures.py for the pose conventions.

Leg bones hang down: +x rotation swings the paw BACKWARD. The spine bones point forward:
+x rotation dips the front end. Head bones stand upright: +x tips the face down/forward.
The jaw points forward: +x opens the mouth.

Stances are chibi-compact on purpose: seen from 35 degrees, whatever touches the ground in
front of (or behind) the origin draws below the pivot, and the kit's QC allows only a few
pixels there. Legs are posed by a two-bone IK (leg_ik) so paws stay planted on the ground
while the body crouches, bobs or recoils, instead of sliding or sinking.
"""
from __future__ import annotations

import math

from rig import (aim, armature, attach, ball, box, clip, lerp_pose, material, merge,
                 set_root_offset, use_collection)

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def quad_armature(name, P, extra=()):
    """P: h (spine height), yf / yb (front / back leg y), x (leg x), knee (z of the knee),
    head (y, z of the neck base), hlen, jaw (y, z), tail ((y,z), (y,z), (y,z))."""
    h, yf, yb, x, kz = P["h"], P["yf"], P["yb"], P["x"], P["knee"]
    hy, hz = P["head"]
    jy, jz = P["jaw"]
    t0, t1, t2 = P["tail"]
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.1), None),
        ("pelvis", (0, yb, h), (0, (yb + yf) / 2, h), "root"),
        ("chest", (0, (yb + yf) / 2, h), (0, yf - 0.04, h + 0.02), "pelvis"),
        ("head", (0, hy, hz), (0, hy, hz + P["hlen"]), "chest"),
        ("jaw", (0, jy, jz), (0, jy - 0.14, jz), "head"),
        ("tail1", (0, *t0), (0, *t1), "pelvis"),
        ("tail2", (0, *t1), (0, *t2), "tail1"),
    ]
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y, par in (("f", yf, "chest"), ("b", yb, "pelvis")):
            bones.append((f"{leg}{side}1", (sx * x, y, h - 0.06), (sx * x, y, kz), par))
            bones.append((f"{leg}{side}2", (sx * x, y, kz), (sx * x, y, 0.035), f"{leg}{side}1"))
            # the paw: counter-rotated by the IK so it stays flat on the ground
            bones.append((f"{leg}{side}3", (sx * x, y, 0.035), (sx * x, y - 0.06, 0.035),
                          f"{leg}{side}2"))
    bones += list(extra)
    return armature(name, bones)


def leg_ik(a, b, ty, tz):
    """Two-bone leg in the y-z plane, hip at the origin, target (ty, tz). Returns the
    upper and lower +x rotations in degrees (0, 0 = hanging straight down)."""
    d = max(1e-4, min(math.hypot(ty, tz), a + b - 1e-4))
    phi = math.atan2(ty, -tz)
    gam = math.acos(max(-1.0, min(1.0, (a * a + d * d - b * b) / (2 * a * d))))
    kap = math.acos(max(-1.0, min(1.0, (a * a + b * b - d * d) / (2 * a * b))))
    return math.degrees(phi - gam), math.degrees(math.pi - kap)


class Legs:
    def __init__(self, P):
        self.H = P["h"] - 0.06
        self.a = self.H - P["knee"]
        self.b = P["knee"]
        self.half = (P["yb"] - P["yf"]) / 2     # chest pivot -> front hips

    def plant(self, drop=0.0, front=(0.0, 0.0), back=(0.0, 0.0), pitch=0.0, lift=None):
        """Pose all four legs so each paw lands at (dy, lift) from under its hip after the
        body sank by `drop` and the chest pitched by `pitch` degrees (+ = front dips).
        front/back: (dy left, dy right). lift: {"fl": z, ...} raises single paws."""
        lift = lift or {}
        front_drop = self.half * math.sin(math.radians(pitch))
        out = {}
        for k, dy, dd, pt in (("fl", front[0], front_drop, pitch), ("fr", front[1], front_drop, pitch),
                              ("bl", back[0], 0.0, 0.0), ("br", back[1], 0.0, 0.0)):
            ty, tz = dy, -(self.H - drop - dd) + lift.get(k, 0.0)
            c, s_ = math.cos(math.radians(pt)), math.sin(math.radians(pt))
            # the front legs hang from the pitched chest: express the target in its frame
            u, lo = leg_ik(self.a, self.b, ty * c + tz * s_, -ty * s_ + tz * c)
            out[k + "1"] = {"r": (u, 0, 0)}
            out[k + "2"] = {"r": (lo, 0, 0)}
            curl = 25.0 * lift.get(k, 0.0) / 0.05     # a lifted paw curls a little
            out[k + "3"] = {"r": (-(u + lo + pt) + curl, 0, 0)}
        return out

    @staticmethod
    def air(fl, fr, bl, br):
        out = {}
        for k, (u, lo) in (("fl", fl), ("fr", fr), ("bl", bl), ("br", br)):
            out[k + "1"] = {"r": (u, 0, 0)}
            out[k + "2"] = {"r": (lo, 0, 0)}
            out[k + "3"] = {"r": (20 if k[0] == "f" else -20, 0, 0)}
        return out


def gait(phase, s, lift):
    """Paw offset along the stride for one leg: stance (paw drifts back on the ground)
    for the first half, swing (paw lifted, carried forward) for the second."""
    p = phase % 1.0
    if p < 0.5:
        return -s + 4 * s * p, 0.0
    q = (p - 0.5) / 0.5
    return s - 2 * s * q, lift * math.sin(math.pi * q)


def quad_clips(arm, P, A):
    """A: stride (half length, m), lift, hop, crouch, drop, lunge."""
    L = Legs(P)
    s, lift, hop, cr, lunge = A["stride"], A["lift"], A["hop"], A["crouch"], A["lunge"]
    idle = []
    for i in range(4):
        breath = 0.006 * (0.5 - 0.5 * C(i, 4))
        p = L.plant(drop=breath)
        p.update({
            "pelvis": {"l": (0, 0, -breath)},
            "chest": {"r": (-1.5 * S(i, 4), 0, 0)},
            "head": {"r": (2 * S(i, 4, 0.6), 0, 6 * S(i, 4, -0.5))},
            "jaw": {"r": (3 + 3 * S(i, 4, 0.6), 0, 0)},
            "tail1": {"r": (4 * C(i, 4), 0, 14 * S(i, 4))},
            "tail2": {"r": (6 * C(i, 4, -1), 0, 20 * S(i, 4, -1.1))},
        })
        idle.append(p)
    walk = []
    for i in range(6):
        ph = i / 6
        legs = {}
        lifts = {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(ph + off, s, lift)
        bob = 0.012 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]),
                    lift=lifts)
        p.update({
            "pelvis": {"l": (0, 0, bob), "r": (0, 3 * S(i, 6), 0)},
            "chest": {"r": (0, -4 * S(i, 6), 0)},
            "head": {"r": (4 * abs(S(i, 6)) - 2, 0, -5 * S(i, 6))},
            "jaw": {"r": (4, 0, 0)},
            "tail1": {"r": (-8, 0, 16 * S(i, 6, 0.8))},
            "tail2": {"r": (-6, 0, 22 * S(i, 6, -0.3))},
        })
        walk.append(p)
    # windup: crouch low on coiled hind legs, front dipped, head down and level, jaw
    # parted, tail up and lashing - held while the strike zone fills
    coil = L.plant(drop=cr, front=(0.01, 0.01), back=(-0.03, -0.03), pitch=9)
    coil.update({
        "pelvis": {"l": (0, 0, -cr), "r": (-4, 0, 0)},
        "chest": {"r": (9, 0, 0)},
        "head": {"r": (-12, 0, 0), "l": (0, 0, -0.02)},
        "jaw": {"r": (20, 0, 0)},
        "tail1": {"r": (42, 0, 0)}, "tail2": {"r": (35, 0, 0)},
    })
    windup = [lerp_pose(idle[0], coil, 0.55), coil,
              merge(coil, {"tail2": {"r": (30, 0, 16)}, "head": {"r": (-12, 0, 3)}}),
              merge(coil, {"tail2": {"r": (30, 0, -16)}, "head": {"r": (-12, 0, -3)}})]
    leap = L.air((-70, -5), (-64, 0), (48, 22), (46, 20))
    leap.update({
        "root": {"l": (0, -lunge * 0.5, hop)},
        "pelvis": {"r": (-10, 0, 0)}, "chest": {"r": (-6, 0, 0)},
        "head": {"r": (-4, 0, 0)}, "jaw": {"r": (34, 0, 0)},
        "tail1": {"r": (-20, 0, 0)}, "tail2": {"r": (-10, 0, 0)},
    })
    strike = L.plant(drop=0.03, front=(0.016, 0.022), back=(0.02, 0.02), pitch=12)
    strike.update({
        "root": {"l": (0, -lunge, 0)},
        "pelvis": {"l": (0, 0, -0.03)}, "chest": {"r": (12, 0, 0)},
        "head": {"r": (10, 0, 0), "l": (0, -0.02, 0.01)}, "jaw": {"r": (46, 0, 0)},
        "tail1": {"r": (-6, 0, 12)}, "tail2": {"r": (18, 0, 18)},
    })
    settle = lerp_pose(strike, idle[0], 0.45)
    settle["root"] = {"l": (0, -lunge * 0.8, 0)}
    settle["jaw"] = {"r": (8, 0, 0)}
    settle.update(L.plant(drop=0.015, front=(0.012, 0.016), back=(0.01, 0.01), pitch=6.6))
    back = lerp_pose(strike, idle[0], 0.85)
    back["root"] = {"l": (0, -lunge * 0.3, 0)}
    back.update(L.plant(drop=0.005, pitch=1.8))
    attack = [leap, strike, settle, back]
    hit = [merge(L.plant(drop=0.02, front=(0.02, 0.02), back=(0.0, 0.0), pitch=-10),
                 {"pelvis": {"l": (0, 0.0, -0.02)}, "chest": {"r": (-10, 0, 6)},
                  "head": {"r": (-22, 0, 10)}, "jaw": {"r": (24, 0, 0)},
                  "tail1": {"r": (30, 0, 0)}, "tail2": {"r": (20, 0, 0)}}),
           merge(L.plant(drop=0.008, front=(0.008, 0.008), pitch=-4),
                 {"pelvis": {"l": (0, 0, -0.008)}, "chest": {"r": (-4, 0, 2)},
                  "head": {"r": (-8, 0, 4)}, "jaw": {"r": (8, 0, 0)}})]
    dr = A["drop"]
    down = merge(L.plant(drop=dr, front=(0.01, 0.02), back=(0.02, 0.03), pitch=2),
                 {"pelvis": {"l": (0, 0, -dr)}, "chest": {"r": (2, 0, 0)},
                  "head": {"r": (8, 0, 40), "l": (0, 0.02, -0.03)}, "jaw": {"r": (12, 0, 0)},
                  "tail1": {"r": (-12, 0, 56)}, "tail2": {"r": (-8, 0, 36)}})
    buckle = merge(L.plant(drop=dr * 0.2, front=(-0.02, -0.02), pitch=16),
                   {"chest": {"r": (16, 0, 0)}, "pelvis": {"l": (0, 0, -dr * 0.2)},
                    "head": {"r": (4, 0, 22)}, "jaw": {"r": (20, 0, 0)},
                    "tail1": {"r": (-10, 0, 0)}})
    die = [
        merge(L.plant(drop=0.01, pitch=-8), {"head": {"r": (-28, 0, 0)}, "jaw": {"r": (36, 0, 0)},
                                   "pelvis": {"l": (0, 0, -0.01)},
                                   "chest": {"r": (-8, 0, 0)}, "tail1": {"r": (30, 0, 0)}}),
        buckle,
        lerp_pose(buckle, down, 0.7),
        down,
        merge(down, {"head": {"r": (12, 0, 46), "l": (0, 0.03, -0.05)},
                     "tail1": {"r": (-14, 0, 64)}, "tail2": {"r": (-8, 0, 40)}}),
        merge(down, {"head": {"r": (13, 0, 48), "l": (0, 0.03, -0.055)},
                     "tail1": {"r": (-16, 0, 68)}, "tail2": {"r": (-10, 0, 44)},
                     "jaw": {"r": (4, 0, 0)}}),
    ]
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, A.get("walk_fps", 10), True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=1)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    arm.animation_data.action = None


# =============================================================== Ma Trận Thú
def grid_cage(name, size, center, mat, xs=(), ys=(), zs=(), w=0.014):
    """Glowing grid lines on a box: thin slabs slightly larger than the box, so only
    their rims show, wrapping the surface as lines."""
    sx, sy, sz = size
    cx, cy, cz = center
    out = []
    for k, x in enumerate(xs):
        out.append(box(f"{name}_x{k}", (w, sy + 0.012, sz + 0.012), (cx + x, cy, cz), mat))
    for k, y in enumerate(ys):
        out.append(box(f"{name}_y{k}", (sx + 0.012, w, sz + 0.012), (cx, cy + y, cz), mat))
    for k, z in enumerate(zs):
        out.append(box(f"{name}_z{k}", (sx + 0.012, sy + 0.012, w), (cx, cy, cz + z), mat))
    return out


def build_ma_tran_thu():
    use_collection("COL_ma_tran_thu")
    jade = material("MAT_mt_jade", (0.18, 0.48, 0.35), (0.36, 0.21, 0.56), ramp=("jade", "purple"))
    jade_dk = material("MAT_mt_jade_dark", (0.11, 0.31, 0.25), (0.23, 0.13, 0.38), ramp=("jade", "purple"))
    muzzle = material("MAT_mt_muzzle", (0.31, 0.65, 0.47), (0.52, 0.34, 0.75), ramp=("jade", "purple"))
    gold = material("MAT_mt_plate", (0.90, 0.72, 0.23), (0.81, 0.80, 0.83), ramp=("gold", "bone"), metal=True)
    gold_dk = material("MAT_mt_plate_dark", (0.73, 0.51, 0.10), (0.60, 0.58, 0.64), ramp=("gold", "bone"), metal=True)
    grid = material("MAT_mt_grid", (0.35, 0.88, 0.96), (0.78, 0.55, 1.0), emit=4.0, glow=("spirit", "cosmic"))
    eye = material("MAT_mt_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=6.0, glow=("holy", "flame"))
    dark = material("MAT_mt_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    tooth = material("MAT_mt_tooth", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")

    P = {"h": 0.40, "yf": -0.08, "yb": 0.12, "x": 0.11, "knee": 0.17,
         "head": (-0.19, 0.48), "hlen": 0.26, "jaw": (-0.34, 0.52),
         "tail": ((0.24, 0.46), (0.33, 0.60), (0.37, 0.76))}
    arm = quad_armature("ma_tran_thu", P)
    HY = -0.30   # centre of the head block

    att(arm, "chest", box("mt_chest", (0.37, 0.25, 0.29), (0, -0.04, 0.44), jade, bevel=0.03),
        *grid_cage("mt_gc", (0.37, 0.25, 0.29), (0, -0.04, 0.44), grid,
                   xs=(-0.07, 0.07), ys=(0.0,)))
    att(arm, "pelvis", box("mt_rump", (0.33, 0.23, 0.26), (0, 0.13, 0.42), jade, bevel=0.03),
        box("mt_belly", (0.26, 0.36, 0.05), (0, 0.04, 0.29), jade_dk),
        *grid_cage("mt_gr", (0.33, 0.23, 0.26), (0, 0.13, 0.42), grid,
                   xs=(-0.07, 0.07), ys=(0.03,)))
    # head: a big blocky guardian face, glowing eyes under gold brows
    hd = [box("mt_head", (0.38, 0.30, 0.32), (0, HY, 0.64), jade, bevel=0.035),
          box("mt_muzzle", (0.23, 0.12, 0.13), (0, HY - 0.17, 0.58), muzzle, bevel=0.02),
          box("mt_nose", (0.09, 0.04, 0.05), (0, HY - 0.235, 0.625), dark, bevel=0.01),
          box("mt_eyel", (0.075, 0.02, 0.05), (0.09, HY - 0.152, 0.695), eye),
          box("mt_eyer", (0.075, 0.02, 0.05), (-0.09, HY - 0.152, 0.695), eye),
          box("mt_browl", (0.12, 0.04, 0.035), (0.09, HY - 0.158, 0.745), gold, rot=(0, -16, 0)),
          box("mt_browr", (0.12, 0.04, 0.035), (-0.09, HY - 0.158, 0.745), gold, rot=(0, 16, 0)),
          box("mt_mark", (0.016, 0.02, 0.07), (0, HY - 0.153, 0.78), grid),
          box("mt_earl", (0.08, 0.06, 0.08), (0.17, HY + 0.03, 0.81), jade_dk, bevel=0.01),
          box("mt_earr", (0.08, 0.06, 0.08), (-0.17, HY + 0.03, 0.81), jade_dk, bevel=0.01),
          box("mt_lip", (0.21, 0.03, 0.03), (0, HY - 0.175, 0.525), dark)]
    # the mane: two rings of square plates set like diamonds round the face
    for k in range(10):
        a = TAU * k / 10 + 0.31
        hd.append(box(f"mt_mane{k}", (0.13, 0.05, 0.13),
                      (0.25 * math.cos(a), HY + 0.08, 0.63 + 0.25 * math.sin(a)),
                      gold if k % 2 == 0 else gold_dk, rot=(0, 45 - math.degrees(a), 0),
                      bevel=0.01))
    for k in range(8):
        a = TAU * k / 8
        hd.append(box(f"mt_manein{k}", (0.10, 0.05, 0.10),
                      (0.20 * math.cos(a), HY + 0.14, 0.64 + 0.20 * math.sin(a)), gold_dk,
                      rot=(0, 45 - math.degrees(a), 0)))
    att(arm, "head", *hd)
    att(arm, "jaw", box("mt_jaw", (0.20, 0.13, 0.05), (0, HY - 0.14, 0.505), jade_dk, bevel=0.01),
        box("mt_fangl", (0.03, 0.025, 0.04), (0.065, HY - 0.19, 0.54), tooth),
        box("mt_fangr", (0.03, 0.025, 0.04), (-0.065, HY - 0.19, 0.54), tooth))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1",
                box(f"mt_{leg}{side}up", (0.13, 0.13, 0.19), (x, y, 0.26), jade, bevel=0.02))
            att(arm, f"{leg}{side}2",
                box(f"mt_{leg}{side}lo", (0.10, 0.10, 0.12), (x, y, 0.11), jade_dk, bevel=0.015),
                box(f"mt_{leg}{side}cuff", (0.12, 0.12, 0.03), (x, y, 0.155), gold))
            att(arm, f"{leg}{side}3",
                box(f"mt_{leg}{side}paw", (0.13, 0.12, 0.07), (x, y - 0.005, 0.035), jade, bevel=0.015),
                box(f"mt_{leg}{side}claw", (0.11, 0.03, 0.03), (x, y - 0.06, 0.02), gold_dk))
    att(arm, "tail1", box("mt_tail1", (0.08, 0.08, 0.17), (0, 0.285, 0.53), jade_dk, rot=(-33, 0, 0)))
    att(arm, "tail2", box("mt_tail2", (0.07, 0.07, 0.16), (0, 0.35, 0.68), jade_dk, rot=(-14, 0, 0)),
        box("mt_tuft1", (0.11, 0.05, 0.11), (0, 0.37, 0.78), gold, rot=(0, 45, 0)),
        box("mt_tuft2", (0.08, 0.05, 0.08), (0.06, 0.38, 0.72), gold_dk, rot=(0, 45, 0)),
        box("mt_tuft3", (0.08, 0.05, 0.08), (-0.06, 0.38, 0.72), gold_dk, rot=(0, 45, 0)))
    quad_clips(arm, P, {"stride": 0.04, "lift": 0.05, "hop": 0.07, "crouch": 0.09, "drop": 0.2,
                        "lunge": 0.02, "walk_fps": 9})
    return arm


# =============================================================== Phong Lang
def build_phong_lang():
    use_collection("COL_phong_lang")
    set_root_offset((0, -0.009, 0))
    fur = material("MAT_pl_fur", (0.58, 0.65, 0.73), (0.36, 0.21, 0.56), ramp=("steel", "purple"))
    fur_lt = material("MAT_pl_fur_light", (0.81, 0.80, 0.83), (0.52, 0.34, 0.75), ramp=("bone", "purple"))
    fur_dk = material("MAT_pl_fur_dark", (0.36, 0.43, 0.53), (0.23, 0.13, 0.38), ramp=("steel", "purple"))
    tuft = material("MAT_pl_wind", (0.35, 0.88, 0.96), (0.72, 0.75, 1.0), emit=2.0, glow=("spirit", "thunder"))
    eye = material("MAT_pl_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=6.0, glow=("holy", "flame"))
    nose = material("MAT_pl_nose", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    fang = material("MAT_pl_fang", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")

    P = {"h": 0.33, "yf": -0.07, "yb": 0.10, "x": 0.095, "knee": 0.15,
         "head": (-0.13, 0.40), "hlen": 0.22, "jaw": (-0.27, 0.455),
         "tail": ((0.18, 0.37), (0.28, 0.43), (0.38, 0.46))}
    arm = quad_armature("phong_lang", P)
    att(arm, "chest", ball("pl_chest", (0.15, 0.13, 0.13), (0, -0.03, 0.35), fur),
        ball("pl_ruff", (0.16, 0.09, 0.14), (0, -0.11, 0.39), fur_lt),
        aim("pl_shoul", tuft, (0.12, -0.04, 0.42), (0.22, 0.04, 0.50), 0.04, 0.0, seg=6),
        aim("pl_shour", tuft, (-0.12, -0.04, 0.42), (-0.22, 0.04, 0.50), 0.04, 0.0, seg=6),
        aim("pl_tuft1", tuft, (0, -0.08, 0.46), (0, 0.08, 0.59), 0.05, 0.0, seg=8),
        aim("pl_tuft2", tuft, (0, 0.01, 0.45), (0, 0.16, 0.55), 0.045, 0.0, seg=8))
    att(arm, "pelvis", ball("pl_rump", (0.125, 0.11, 0.11), (0, 0.10, 0.34), fur),
        aim("pl_tuft3", tuft, (0, 0.09, 0.43), (0, 0.22, 0.50), 0.04, 0.0, seg=8))
    HY = -0.21
    hd = [ball("pl_head", (0.19, 0.16, 0.155), (0, HY, 0.55), fur),
          ball("pl_muzzle", (0.10, 0.08, 0.07), (0, HY - 0.12, 0.505), fur_lt),
          aim("pl_snout", fur_lt, (0, HY - 0.08, 0.51), (0, HY - 0.235, 0.49), 0.08, 0.045, seg=10),
          ball("pl_nose", (0.035, 0.028, 0.028), (0, HY - 0.24, 0.505), nose, seg=8, rings=5),
          ball("pl_eyel", (0.046, 0.016, 0.034), (0.08, HY - 0.135, 0.585), eye, rot=(0, 0, 20), seg=8, rings=5),
          ball("pl_eyer", (0.046, 0.016, 0.034), (-0.08, HY - 0.135, 0.585), eye, rot=(0, 0, -20), seg=8, rings=5),
          box("pl_browl", (0.08, 0.024, 0.022), (0.08, HY - 0.135, 0.625), fur_dk, rot=(0, -20, 0)),
          box("pl_browr", (0.08, 0.024, 0.022), (-0.08, HY - 0.135, 0.625), fur_dk, rot=(0, 20, 0)),
          aim("pl_earl", fur, (0.09, HY + 0.02, 0.63), (0.17, HY + 0.07, 0.82), 0.065, 0.0, seg=6),
          aim("pl_earr", fur, (-0.09, HY + 0.02, 0.63), (-0.17, HY + 0.07, 0.82), 0.065, 0.0, seg=6),
          aim("pl_earil", fur_dk, (0.09, HY + 0.0, 0.64), (0.16, HY + 0.045, 0.78), 0.036, 0.0, seg=6),
          aim("pl_earir", fur_dk, (-0.09, HY + 0.0, 0.64), (-0.16, HY + 0.045, 0.78), 0.036, 0.0, seg=6),
          aim("pl_cheekl", tuft, (0.12, HY - 0.02, 0.50), (0.28, HY + 0.08, 0.53), 0.055, 0.0, seg=6),
          aim("pl_cheekr", tuft, (-0.12, HY - 0.02, 0.50), (-0.28, HY + 0.08, 0.53), 0.055, 0.0, seg=6),
          aim("pl_crest", tuft, (0, HY + 0.03, 0.66), (0, HY + 0.18, 0.74), 0.05, 0.0, seg=6),
          aim("pl_fangl", fang, (0.035, HY - 0.19, 0.48), (0.035, HY - 0.19, 0.445), 0.014, 0.0, seg=5),
          aim("pl_fangr", fang, (-0.035, HY - 0.19, 0.48), (-0.035, HY - 0.19, 0.445), 0.014, 0.0, seg=5)]
    att(arm, "head", *hd)
    att(arm, "jaw", aim("pl_jaw", fur_lt, (0, HY - 0.06, 0.45), (0, HY - 0.20, 0.45), 0.05, 0.028, seg=8))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            up = aim(f"pl_{leg}{side}up", fur, (x, y, 0.30), (x, y, 0.15),
                     0.058 if leg == "b" else 0.05, 0.04, seg=8)
            att(arm, f"{leg}{side}1", up)
            att(arm, f"{leg}{side}2",
                aim(f"pl_{leg}{side}lo", fur_lt if leg == "f" else fur, (x, y, 0.16), (x, y, 0.03),
                    0.036, 0.03, seg=8))
            att(arm, f"{leg}{side}3",
                ball(f"pl_{leg}{side}paw", (0.04, 0.045, 0.028), (x, y - 0.005, 0.026), fur_lt,
                     seg=8, rings=5))
    att(arm, "tail1", aim("pl_tail1", fur, (0, 0.18, 0.37), (0, 0.28, 0.43), 0.04, 0.06, seg=8))
    att(arm, "tail2", ball("pl_tail2", (0.07, 0.11, 0.07), (0, 0.34, 0.45), fur, rot=(-20, 0, 0)),
        aim("pl_tailtip", tuft, (0, 0.39, 0.46), (0, 0.49, 0.50), 0.06, 0.0, seg=8))
    quad_clips(arm, P, {"stride": 0.035, "lift": 0.05, "hop": 0.06, "crouch": 0.07, "drop": 0.17,
                        "lunge": 0.02, "walk_fps": 12})
    return arm
