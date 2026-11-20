"""Ngọc Thố: the jade moon rabbit. Runs inside Blender (see scene.py).

A sitting rabbit with a big round head, long two-bone ears whose tips glow soft jade, a
small golden crescent on the brow, a red cord with a jade bead at the throat, big hind feet
and a cotton tail. Front legs are skinned tubes between a shoulder bone (on the chest) and a
paw bone (on the root), so the paws stay planted while the body bobs and stretch when they
reach. Walk is a real hop cycle (gather - push - flight - front landing - hind swing - hind
landing) with squash and stretch on the haunch bone and ears that lag a frame behind.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import (S, hexc, set_ramp, armature, att, ball, cute_eyes, eye_mats, eyes_bone, finish, glow, lerp_pose,
                    mat, merge, prism, skin, tube, use_collection)


def crescent(name, m, centre, tilt_deg, R=0.042):
    """A cup-shaped crescent (horns up) in the x-z plane, tilted back to lie on the brow."""
    pts = []
    for k in range(13):                      # outer arc, through the bottom
        a = math.radians(200 + 140 * k / 12)
        pts.append((R * math.cos(a), R * math.sin(a)))
    r2, up = R * 0.80, R * 0.42
    for k in range(13):                      # inner arc back, centre raised
        a = math.radians(340 - 140 * k / 12)
        x, z = r2 * math.cos(a), up + r2 * math.sin(a)
        pts.append((x, z))
    # keep only points whose inner arc stays inside the outer one (no self-crossing)
    M = Matrix.Translation(Vector(centre)) @ Matrix.Rotation(math.radians(-tilt_deg), 4, "X")
    return prism(name, pts, 0.01, m, M)


def side_eyes(prefix, x, y, z, r, mats, turn):
    """Big round eyes set on the sides of the head (turned out by `turn` degrees), so they
    read from the front and in profile: iris, pupil, and a catch-light up-front."""
    iris, pupil, shine = mats
    out = []
    for s in (1, -1):
        rz = s * turn
        a = math.radians(rz)
        fwd = Vector((s * math.sin(abs(a)), -math.cos(a), 0))      # outward-forward
        c = Vector((s * x, y, z))
        out.append(ball(f"{prefix}_iris{s}", (r, r * 0.5, r * 1.1), tuple(c), iris, rot=(0, 0, -rz), seg=10, rings=6))
        out.append(ball(f"{prefix}_pupil{s}", (r * 0.6, r * 0.3, r * 0.7), tuple(c + fwd * r * 0.32 + Vector((0, 0, -r * 0.05))),
                        pupil, rot=(0, 0, -rz), seg=8, rings=5))
        out.append(ball(f"{prefix}_shine{s}", (r * 0.32,) * 3, tuple(c + fwd * r * 0.5 + Vector((0, 0, r * 0.4))),
                        shine, seg=6, rings=4))
    return out


def build():
    use_collection("COL_ngoc_tho")
    fur = mat("MAT_nt_fur", "#cfcbd3", "bone")
    fur_sh = mat("MAT_nt_fur_shade", "#9894a2", "bone")
    inner = mat("MAT_nt_inner", "#f6b0c4", "pink")
    nose = mat("MAT_nt_nose", "#e88aa6", "pink")
    cord = mat("MAT_nt_cord", "#94302a", "red")
    bead = mat("MAT_nt_bead", "#4fa678", "jade")
    tip = glow("MAT_nt_eartip", "#7aec9a", "verdant", 2.0, halo=0)
    moon = glow("MAT_nt_moon_mark", "#ffe27a", "holy", 3.0, halo=0)
    moon["kit_priority"] = 3.0
    eyes = eye_mats("nt", hexc("#463c4c"))
    set_ramp(eyes[0], "hair")            # big dark eyes with a white shine: the face on white fur
    blush = mat("MAT_nt_blush", "#f6b0c4", "pink")

    HY, HZ = -0.09, 0.43
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.08), None),
        ("hips", (0, 0.05, 0.06), (0, 0.05, 0.20), "root"),
        ("chest", (0, 0.0, 0.18), (0, -0.05, 0.30), "hips"),
        ("head", (0, -0.06, 0.30), (0, -0.07, 0.46), "chest"),
        eyes_bone(HY - 0.10, HZ),
        ("tail", (0, 0.18, 0.14), (0, 0.24, 0.15), "hips"),
    ]
    ears = {}
    for side, sx in (("L", 1), ("R", -1)):
        base = Vector((sx * 0.055, HY + 0.015, HZ + 0.10))
        mid = base + Vector((sx * 0.025, 0.02, 0.16))
        top = mid + Vector((sx * 0.02, 0.03, 0.15))
        ears[side] = (base, mid, top)
        bones += [(f"ear{side}1", tuple(base), tuple(mid), "head"),
                  (f"ear{side}2", tuple(mid), tuple(top), f"ear{side}1"),
                  (f"arm{side}", (sx * 0.038, -0.07, 0.22), (sx * 0.038, -0.08, 0.15), "chest"),
                  (f"paw{side}", (sx * 0.038, -0.075, 0.05), (sx * 0.038, -0.075, 0.0), "root"),
                  (f"foot{side}", (sx * 0.066, 0.05, 0.05), (sx * 0.066, -0.05, 0.03), "root")]
    arm = armature("ngoc_tho", bones)

    att(arm, "hips", ball("nt_haunch", (0.13, 0.14, 0.13), (0, 0.05, 0.16), fur))
    att(arm, "chest", ball("nt_chest", (0.105, 0.10, 0.12), (0, -0.035, 0.245), fur),
        tube("nt_cord", [(0.085 * math.sin(math.radians(a)), -0.035 - 0.082 * math.cos(math.radians(a)),
                          0.315 - 0.03 * math.cos(math.radians(a))) for a in range(-110, 111, 20)],
             [0.011] * 12, cord, seg=6),
        ball("nt_bead", (0.026, 0.02, 0.03), (0, -0.125, 0.265), bead, seg=10, rings=6))
    att(arm, "head", ball("nt_head", (0.17, 0.145, 0.145), (0, HY, HZ), fur),
        ball("nt_cheekl", (0.06, 0.05, 0.05), (0.08, HY - 0.07, HZ - 0.08), fur, seg=10, rings=6),
        ball("nt_cheekr", (0.06, 0.05, 0.05), (-0.08, HY - 0.07, HZ - 0.08), fur, seg=10, rings=6),
        ball("nt_padl", (0.03, 0.025, 0.025), (0.022, HY - 0.14, HZ - 0.05), fur, seg=8, rings=5),
        ball("nt_padr", (0.03, 0.025, 0.025), (-0.022, HY - 0.14, HZ - 0.05), fur, seg=8, rings=5),
        ball("nt_nose", (0.02, 0.012, 0.014), (0, HY - 0.158, HZ - 0.025), nose, seg=8, rings=5),
        ball("nt_blushl", (0.03, 0.01, 0.016), (0.095, HY - 0.125, HZ - 0.045), blush, seg=6, rings=4),
        ball("nt_blushr", (0.03, 0.01, 0.016), (-0.095, HY - 0.125, HZ - 0.045), blush, seg=6, rings=4),
        crescent("nt_moon", moon, (0, HY - 0.098, HZ + 0.112), 52, R=0.036))
    att(arm, "eyes", *side_eyes("nt", 0.075, HY - 0.124, HZ + 0.0, 0.054, eyes, 20))
    for side, sx in (("L", 1), ("R", -1)):
        base, mid, top = ears[side]
        d1, d2 = (mid - base), (top - mid)
        rx1 = -math.degrees(math.atan2(d1.y, d1.z))
        ry1 = sx * math.degrees(math.atan2(abs(d1.x), d1.z))
        rx2 = -math.degrees(math.atan2(d2.y, d2.z))
        ry2 = sx * math.degrees(math.atan2(abs(d2.x), d2.z))
        c1, c2 = base + d1 * 0.55, mid + d2 * 0.45
        att(arm, f"ear{side}1",
            ball(f"nt_ear{side}1", (0.056, 0.026, 0.10), tuple(c1), fur, rot=(rx1, ry1, sx * 18)),
            ball(f"nt_eari{side}1", (0.03, 0.012, 0.08), tuple(c1 + Vector((0, -0.016, 0.005))), inner,
                 rot=(rx1, ry1, sx * 18), seg=10, rings=6))
        att(arm, f"ear{side}2",
            ball(f"nt_ear{side}2", (0.052, 0.024, 0.095), tuple(c2), fur, rot=(rx2, ry2, sx * 18)),
            ball(f"nt_eari{side}2", (0.026, 0.011, 0.06), tuple(c2 + Vector((0, -0.015, -0.02))), inner,
                 rot=(rx2, ry2, sx * 18), seg=10, rings=6),
            ball(f"nt_tip{side}", (0.03, 0.02, 0.03), tuple(top - d2 * 0.12), tip, rot=(rx2, ry2, sx * 18),
                 seg=10, rings=6))
        x = sx * 0.038
        leg = tube(f"nt_leg{side}", [(x, -0.07, 0.23), (x, -0.078, 0.14), (x, -0.075, 0.045)],
                   [0.032, 0.028, 0.027], fur, seg=10)
        skin(leg, arm, [f"arm{side}", f"paw{side}"], power=3.0)
        att(arm, f"paw{side}", ball(f"nt_paw{side}", (0.032, 0.038, 0.024), (x, -0.08, 0.022), fur_sh, seg=10, rings=6))
        att(arm, f"foot{side}", ball(f"nt_foot{side}", (0.04, 0.085, 0.03), (sx * 0.066, 0.0, 0.03), fur_sh, seg=10, rings=6),
            ball(f"nt_thigh{side}", (0.05, 0.08, 0.06), (sx * 0.075, 0.06, 0.08), fur, seg=10, rings=6))
    att(arm, "tail", ball("nt_tail", (0.055, 0.05, 0.055), (0, 0.205, 0.15), fur, seg=10, rings=6))

    # ------------------------------------------------------------------ poses
    def ears_pose(f1=0.0, f2=0.0, out=0.0, outR=None):
        """f1 / f2: +x tips the ear forward, - lays it back; out: spread sideways."""
        oR = out if outR is None else outR
        # rest asymmetry: the left ear stands, the right one leans back a little
        return {"earL1": {"r": (f1 + 4, out, 0)}, "earL2": {"r": (f2, 0, 0)},
                "earR1": {"r": (f1 - 14, -oR - 4, 0)}, "earR2": {"r": (f2 + 10, 0, 0)}}

    def body(z=0.0, pitch=0.0, sq=1.0, head=0.0, yaw=0.0):
        """Haunch bone: rise, forward pitch, squash (<1) / stretch (>1) along the spine."""
        w = 1.0 / math.sqrt(sq)
        return {"hips": {"l": (0, 0, z), "r": (pitch, 0, yaw), "s": (w, sq, w)},
                "head": {"r": (head - pitch * 0.6, 0, 0)}}

    def feet(fy=0.0, fz=0.0, hy=0.0, hz=0.0, fyR=None, fzR=None):
        fyR = fy if fyR is None else fyR
        fzR = fz if fzR is None else fzR
        return {"pawL": {"l": (0, fy, fz)}, "pawR": {"l": (0, fyR, fzR)},
                "footL": {"l": (0, hy, hz)}, "footR": {"l": (0, hy, hz)}}

    idle = []
    for i in range(4):
        p = merge(body(z=0.004 * S(i, 4), sq=1.0 + 0.02 * S(i, 4), head=2 * S(i, 4, 0.8)),
                  ears_pose(-4 * S(i, 4, -0.8), -7 * S(i, 4, -1.8), 4))
        if i == 2:            # one ear flicks
            p["earR1"] = {"r": (-10, -14, 0)}
            p["earR2"] = {"r": (-12, 0, 0)}
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
        p["tail"] = {"r": (0, 0, 10 * S(i, 4))}
        idle.append(p)

    # hop cycle: one pair of feet is always on the ground; planted feet drift back on the
    # ground (the game moves the beast), lifted ones swing forward
    W = [  # z, pitch, squash, ears f1, ears f2, front (y, z), hind (y, z)
        (-0.020, 4, 0.90, 10, 10, (0.025, 0.0), (-0.020, 0.0)),     # gather (squash)
        (0.022, 16, 1.08, -12, -14, (0.035, 0.03), (-0.003, 0.0)),  # push off the hind feet
        (0.048, 10, 1.12, -20, -22, (-0.035, 0.03), (0.014, 0.0)),  # flight, front reaching
        (0.026, 18, 1.00, -6, -16, (-0.040, 0.0), (0.030, 0.03)),   # front feet land
        (0.004, 8, 0.95, 8, 0, (-0.020, 0.0), (-0.005, 0.04)),      # hind feet swing through
        (-0.022, 2, 0.88, 14, 14, (0.000, 0.0), (-0.035, 0.0)),     # hind land (squash)
    ]
    walk = []
    for i, (z, pt, sq, e1, e2, fr, hd) in enumerate(W):
        p = merge(body(z, pt, sq), ears_pose(e1, e2, 6))
        p.update(feet(fr[0], fr[1], hd[0], hd[1]))
        p["tail"] = {"r": (-10 * (sq - 1) * 10, 0, 0)}
        walk.append(p)

    # windup: rears up on the hind feet, ears tall, paws raised like a boxer
    rear = merge(body(0.03, -10, 1.10, 6), ears_pose(-4, 4, 10))
    rear.update(feet(-0.02, 0.15, 0.0, 0.0))
    rear["chest"] = {"r": (-12, 0, 0)}
    rear2 = merge(rear, {"pawL": {"l": (0, -0.04, 0.17)}, "pawR": {"l": (0, -0.01, 0.13)}})
    rear3 = merge(rear, {"pawL": {"l": (0, -0.01, 0.13)}, "pawR": {"l": (0, -0.04, 0.17)}})
    windup = [lerp_pose(idle[0], rear, 0.5), rear, rear2, rear3]
    # attack: a hop-lunge and a double paw strike (hit on frame 1)
    leap = merge(body(0.05, 24, 1.12, -6), ears_pose(-30, -20, 6))
    leap.update(feet(-0.06, 0.12, 0.01, 0.03))
    leap["root"] = {"l": (0, -0.01, 0)}
    strike = merge(body(0.02, 32, 1.06, -10), ears_pose(-40, -24, 8))
    strike.update(feet(-0.10, 0.10, 0.01, 0.0))
    strike["root"] = {"l": (0, -0.02, 0)}
    settle = merge(body(-0.015, 10, 0.92, 0), ears_pose(16, 18, 6))
    settle.update(feet(-0.03, 0.0, 0.0, 0.0))
    settle["root"] = {"l": (0, -0.015, 0)}
    attack = [leap, strike, settle, lerp_pose(settle, idle[0], 0.6)]
    hit = [merge(body(0.0, -6, 0.93, -10), merge(ears_pose(-40, -30, 16), {"eyes": {"s": (1, 0.25, 1)},
                                                                             "root": {"l": (0, -0.01, 0)}})),
           merge(body(0.0, -5, 0.96, -4), ears_pose(-14, -10, 8))]
    hit[0].update(feet(0.0, 0.02, 0.0, 0.0))
    # die: a startled jolt, a wobble, then it flops down flat with the ears laid back
    # the bunny flop: it keels over onto its side, legs out, ears trailing on the ground
    flat = merge(body(0.0, 0, 0.94, 10), ears_pose(-95, -10, 8))
    flat.update(feet(-0.03, 0.02, 0.02, 0.03))
    flat["eyes"] = {"s": (1, 0.12, 1)}
    flat["root"] = {"r": (0, 72, 0), "l": (-0.16, 0, 0.10)}
    die = [merge(body(0.02, -6, 1.08, -8), merge(ears_pose(-6, 0, 18), {"eyes": {"s": 1.15}})),
           merge(body(0.0, 0, 0.96, 6), merge(ears_pose(-24, -10, 20), {"root": {"r": (0, -10, 0)},
                                                                         "eyes": {"s": (1, 0.5, 1)}})),
           lerp_pose({}, flat, 0.6), flat,
           merge(flat, {"earL2": {"r": (-20, 0, 0)}}), merge(flat, {"earL2": {"r": (-16, 0, 0)}})]
    # happy: a binky - crouch, leap with a twist, ears flying, quarter-turn spins like the others
    happy = []
    for i, (z, sq) in enumerate(((0.0, 0.9), (0.09, 1.12), (0.11, 1.05), (0.03, 0.95))):
        p = merge(body(0, 0, sq, -8, 18 * S(i, 4)), ears_pose(-18 - 14 * S(i, 4), -10 + 16 * S(i, 4, 1), 16))
        p["root"] = {"r": (0, 0, 90 * i), "l": (0, 0, z)}
        p.update(feet(-0.01, z * 0.7 if z else 0.0, 0.01, z * 0.6 if z else 0.0))
        if z:
            p["pawL"] = {"l": (0, -0.01, z + 0.04)}
            p["pawR"] = {"l": (0, -0.01, z + 0.04)}
        p["eyes"] = {"s": (1, 0.35, 1)}
        p["tail"] = {"r": (20, 0, 0)}
        happy.append(p)
    # sleep: a loaf, ears laid flat along the back, paws tucked, breathing
    sleep = []
    for i in range(4):
        b = S(i, 4)
        p = merge(body(-0.05 + 0.004 * b, 2, 0.80 + 0.015 * b, 14), ears_pose(-78, -8, 14))
        p.update(feet(0.015, 0.02, 0.0, 0.0))
        p["head"] = {"r": (16, 0, 0), "l": (0, 0.01, -0.05)}
        p["eyes"] = {"s": (1, 0.12, 1)}
        sleep.append(p)
    finish(arm, {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die,
                 "happy": happy, "sleep": sleep})
    return arm
