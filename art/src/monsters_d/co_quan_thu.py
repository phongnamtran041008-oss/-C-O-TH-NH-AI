"""Cơ Quan Thú (normal, 48): a clockwork hound of the workshop quarter, sibling of the
Cơ Quan Nhân puppet (same woods, bronze, gold gears and lantern eyes, same dị chủng).

Body: two barrels of wooden staves bound with bronze hoops (chest and rump), a big gold
gear standing on its back that turns all the time and a wind-up key in its rump; a boxy
wooden head with a bronze muzzle, a hinged bronze jaw with teeth, lantern eyes in bronze
rims and bronze plate ears; wooden leg segments on bronze ball joints, bronze feet; a
two-joint bronze tail.

Rig: the shared quadruped rig of MONSTERS_A (quadrupeds.quad_armature, Legs IK) plus a
`gear` and a `key` bone. Motion is deliberately stiff and stepped: a trot on diagonal pairs
with little knee bend, the head ticking from pose to pose. Windup: crouched on its haunches,
head low, jaw wide, the gear racing. Attack: a lunge and a snap (hit frame 1). Die: the
spring runs down, the legs splay, the gear pops off its axle.
"""
from __future__ import annotations

import math

from common import C, S, att, six
from quadrupeds import Legs, quad_armature, gait
from rig import aim, ball, box, cone, lerp_pose, material, merge, set_root_offset, tube, use_collection

TAU = 2 * math.pi


def gear_x(name, center, r, mat, teeth=8, thick=0.03, tooth=0.04):
    """A gear seen from the side: a disc with square teeth, axis along x."""
    cx, cy, cz = center
    parts = [cone(name, r, r, thick, center, mat, rot=(0, 90, 0), seg=16)]
    for k in range(teeth):
        a = TAU * k / teeth
        parts.append(box(f"{name}_t{k}", (thick, tooth, tooth),
                         (cx, cy + (r + tooth * 0.35) * math.cos(a), cz + (r + tooth * 0.35) * math.sin(a)), mat,
                         rot=(math.degrees(a), 0, 0)))
    return parts


def hoop_y(name, center, r, thick, mat, n=18):
    """A bronze hoop round a barrel lying along y."""
    cx, cy, cz = center
    pts = [(cx + r * math.cos(TAU * k / n), cy, cz + r * math.sin(TAU * k / n)) for k in range(n + 1)]
    return tube(name, pts, [thick] * (n + 1), mat, seg=6, up=(0, 1, 0))


def build():
    use_collection("COL_co_quan_thu")
    set_root_offset((0, 0.0, 0))
    wood = material("MAT_cqt_wood", (0.51, 0.32, 0.18), (0.36, 0.43, 0.53), ramp=("wood", "steel"))
    wood_lt = material("MAT_cqt_wood_light", (0.68, 0.48, 0.28), (0.58, 0.65, 0.73), ramp=("wood", "steel"))
    wood_dk = material("MAT_cqt_wood_dark", (0.34, 0.20, 0.13), (0.20, 0.25, 0.35), ramp=("wood", "steel"))
    bronze = material("MAT_cqt_bronze", (0.73, 0.51, 0.10), (0.58, 0.19, 0.16), ramp=("gold", "red"), metal=True)
    bronze_dk = material("MAT_cqt_bronze_dark", (0.48, 0.30, 0.05), (0.36, 0.10, 0.11), ramp=("gold", "red"), metal=True)
    cog = material("MAT_cqt_gear", (0.90, 0.72, 0.23), (0.78, 0.33, 0.23), ramp=("gold", "red"))
    cog["kit_metal"] = 0
    cog["kit_priority"] = 2.5
    eye = material("MAT_cqt_eye", (1.0, 0.68, 0.23), (0.78, 0.55, 1.0), emit=6.0, glow=("flame", "cosmic"))
    dark = material("MAT_cqt_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    tooth = material("MAT_cqt_tooth", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")

    P = {"h": 0.33, "yf": -0.075, "yb": 0.09, "x": 0.08, "knee": 0.16,
         "head": (-0.15, 0.39), "hlen": 0.2, "jaw": (-0.25, 0.42),
         "tail": ((0.15, 0.37), (0.22, 0.43), (0.27, 0.52))}
    arm = quad_armature("co_quan_thu", P, extra=[
        ("gear", (0, 0.03, 0.52), (0.06, 0.03, 0.52), "pelvis"),
        ("key", (0, 0.12, 0.43), (0, 0.12, 0.52), "pelvis"),
    ])

    # chest barrel and rump barrel (staves lying along y), dark bronze hoops
    def barrel(prefix, center, r, length, n=12):
        cx, cy, cz = center
        out = []
        for k in range(n):
            a = TAU * (k + 0.5) / n
            out.append(box(f"{prefix}_st{k}", (2 * r * math.sin(math.pi / n) * 1.04, length, 0.026),
                           (cx + r * math.cos(a), cy, cz + r * math.sin(a)), wood if k % 2 else wood_lt,
                           rot=(0, -math.degrees(a) + 90, 0)))
        out.append(cone(f"{prefix}_core", r * 0.92, r * 0.92, length * 0.98, center, wood_dk, rot=(90, 0, 0), seg=12))
        return out

    att(arm, "chest", *barrel("cqt_chest", (0, -0.05, 0.35), 0.11, 0.16),
        hoop_y("cqt_hoop1", (0, -0.12, 0.35), 0.117, 0.013, bronze_dk),
        hoop_y("cqt_hoop2", (0, 0.025, 0.35), 0.117, 0.013, bronze_dk),
        ball("cqt_shl", (0.04,) * 3, (0.095, -0.075, 0.29), bronze, seg=10, rings=6),
        ball("cqt_shr", (0.04,) * 3, (-0.095, -0.075, 0.29), bronze, seg=10, rings=6),
        hoop_y("cqt_collar", (0, -0.135, 0.38), 0.075, 0.02, bronze))
    att(arm, "pelvis", box("cqt_waist", (0.07, 0.10, 0.07), (0, 0.05, 0.36), wood_dk, bevel=0.01),
        *barrel("cqt_rump", (0, 0.10, 0.345), 0.088, 0.11),
        hoop_y("cqt_hoop3", (0, 0.152, 0.345), 0.094, 0.012, bronze_dk),
        ball("cqt_hipl", (0.038,) * 3, (0.088, 0.09, 0.285), bronze, seg=10, rings=6),
        ball("cqt_hipr", (0.038,) * 3, (-0.088, 0.09, 0.285), bronze, seg=10, rings=6),
        cone("cqt_axle", 0.018, 0.018, 0.09, (0, 0.03, 0.52), bronze_dk, rot=(0, 90, 0), seg=8),
        box("cqt_mount", (0.04, 0.06, 0.10), (0, 0.03, 0.46), bronze_dk, bevel=0.01))
    # the big gear standing on its back, turning about x; the wind-up key in the rump
    att(arm, "gear", *gear_x("cqt_gear", (0, 0.03, 0.52), 0.08, cog, teeth=6, thick=0.026, tooth=0.055),
        cone("cqt_hub", 0.045, 0.045, 0.034, (0, 0.03, 0.52), wood_dk, rot=(0, 90, 0), seg=10),
        ball("cqt_hubpin", (0.03, 0.016, 0.016), (0, 0.03, 0.52), bronze, seg=8, rings=5))
    att(arm, "key", aim("cqt_keyshaft", bronze, (0, 0.12, 0.40), (0, 0.12, 0.51), 0.018, 0.018, seg=6),
        ball("cqt_keybl", (0.06, 0.018, 0.045), (0.05, 0.12, 0.53), bronze, seg=12, rings=6),
        ball("cqt_keybr", (0.06, 0.018, 0.045), (-0.05, 0.12, 0.53), bronze, seg=12, rings=6),
        ball("cqt_keyhub", (0.024,) * 3, (0, 0.12, 0.53), bronze_dk, seg=8, rings=5))

    # head: wooden skull, a long bronze muzzle, lantern eyes in rims, tall plate ears
    HY, HZ = -0.21, 0.48
    att(arm, "head",
        box("cqt_skull", (0.16, 0.14, 0.13), (0, HY, HZ), wood_lt, bevel=0.03),
        box("cqt_brow", (0.17, 0.035, 0.03), (0, HY - 0.07, HZ + 0.06), wood_dk, bevel=0.008),
        box("cqt_muzzle", (0.085, 0.16, 0.06), (0, HY - 0.13, HZ - 0.03), bronze, bevel=0.018),
        box("cqt_nose", (0.045, 0.03, 0.03), (0, HY - 0.21, HZ - 0.005), dark, bevel=0.006),
        *[box(f"cqt_uptooth{k}", (0.016, 0.02, 0.028), (x, HY - 0.19, HZ - 0.065), tooth)
          for k, x in enumerate((-0.026, 0.026))],
        ball("cqt_eyel", (0.036, 0.02, 0.034), (0.048, HY - 0.075, HZ + 0.025), eye, seg=10, rings=6),
        ball("cqt_eyer", (0.036, 0.02, 0.034), (-0.048, HY - 0.075, HZ + 0.025), eye, seg=10, rings=6),
        hoop_rim("cqt_riml", (0.048, HY - 0.073, HZ + 0.025), bronze_dk),
        hoop_rim("cqt_rimr", (-0.048, HY - 0.073, HZ + 0.025), bronze_dk),
        aim("cqt_earl", bronze_dk, (0.055, HY + 0.03, HZ + 0.055), (0.075, HY + 0.06, HZ + 0.19), 0.038, 0.0, seg=4),
        aim("cqt_earr", bronze_dk, (-0.055, HY + 0.03, HZ + 0.055), (-0.075, HY + 0.06, HZ + 0.19), 0.038, 0.0, seg=4),
        aim("cqt_earil", wood_lt, (0.055, HY + 0.018, HZ + 0.06), (0.072, HY + 0.045, HZ + 0.16), 0.022, 0.0, seg=4),
        aim("cqt_earir", wood_lt, (-0.055, HY + 0.018, HZ + 0.06), (-0.072, HY + 0.045, HZ + 0.16), 0.022, 0.0, seg=4),
        cone("cqt_bolt", 0.02, 0.02, 0.18, (0, HY + 0.02, HZ - 0.02), bronze_dk, rot=(0, 90, 0), seg=8))
    att(arm, "jaw", box("cqt_jaw", (0.075, 0.14, 0.03), (0, HY - 0.125, HZ - 0.075), bronze_dk, bevel=0.01),
        *[box(f"cqt_lotooth{k}", (0.016, 0.02, 0.026), (x, HY - 0.185, HZ - 0.055), tooth)
          for k, x in enumerate((-0.02, 0.02))])

    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", box(f"cqt_{leg}{side}up", (0.055, 0.065, 0.12), (x, y, 0.225), wood, bevel=0.01))
            att(arm, f"{leg}{side}2", ball(f"cqt_{leg}{side}knee", (0.034,) * 3, (x, y, 0.16), bronze, seg=8, rings=5),
                box(f"cqt_{leg}{side}lo", (0.045, 0.05, 0.11), (x, y, 0.09), wood_lt, bevel=0.008))
            att(arm, f"{leg}{side}3", box(f"cqt_{leg}{side}foot", (0.06, 0.07, 0.032), (x, y - 0.008, 0.016),
                                          bronze_dk, bevel=0.008))
    att(arm, "tail1", aim("cqt_tail1", bronze_dk, (0, 0.15, 0.37), (0, 0.22, 0.43), 0.022, 0.02, seg=6),
        ball("cqt_tailj", (0.026,) * 3, (0, 0.22, 0.43), bronze, seg=8, rings=5))
    att(arm, "tail2", aim("cqt_tail2", bronze_dk, (0, 0.22, 0.43), (0, 0.27, 0.52), 0.018, 0.012, seg=6),
        ball("cqt_tailtip", (0.03,) * 3, (0, 0.275, 0.53), cog, seg=8, rings=5))


    clips(arm, P)
    arm.scale = (1.15, 1.15, 1.15)
    return arm


def hoop_rim(name, center, mat, r=0.04, thick=0.011, n=14):
    cx, cy, cz = center
    pts = [(cx + r * math.cos(TAU * k / n), cy, cz + r * math.sin(TAU * k / n)) for k in range(n + 1)]
    return tube(name, pts, [thick] * (n + 1), mat, seg=5, up=(0, 1, 0))


def clips(arm, P):
    L = Legs(P)

    def works(t, speed=1.0):
        """Gear and key turn whatever the body does (t counts in quarter turns)."""
        return {"gear": {"r": (45 * t * speed, 0, 0)}, "key": {"r": (0, 0, 60 * t * speed)}}

    idle = []
    for i in range(4):
        tick = (0, 1, 1, 0)[i]               # the head ticks between two poses
        p = L.plant(drop=0.004 * tick)
        p.update(works(i))
        p.update({"pelvis": {"l": (0, 0, -0.004 * tick)},
                  "head": {"r": (-4 + 6 * tick, 0, (8, 8, -6, -6)[i])},
                  "jaw": {"r": ((0, 10, 0, 0)[i], 0, 0)},
                  "tail1": {"r": (10, 0, (14, 14, -14, -14)[i])}, "tail2": {"r": (6, 0, (10, 10, -10, -10)[i])}})
        idle.append(p)

    walk = []
    s, lift = 0.04, 0.045
    for i in range(6):
        ph = i / 6
        legs, lifts = {}, {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(ph + off, s, lift)
        bob = 0.012 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]), lift=lifts)
        p.update(works(i * 4 / 6, 1.5))
        p.update({"pelvis": {"l": (0, 0, bob), "r": (0, 2 * S(i, 6), 0)},
                  "chest": {"r": (0, -3 * S(i, 6), 0)},
                  "head": {"r": (2 - 3 * abs(S(i, 6)), 0, 0)},
                  "jaw": {"r": (6 if i % 3 == 0 else 0, 0, 0)},
                  "tail1": {"r": (14, 0, 14 * (1 if i % 2 else -1))}, "tail2": {"r": (10, 0, 10 * (1 if i % 2 else -1))}})
        walk.append(p)

    cr = 0.07
    coil = L.plant(drop=cr, front=(0.012, 0.012), back=(-0.03, -0.03), pitch=10)
    coil.update({"pelvis": {"l": (0, 0, -cr), "r": (-4, 0, 0)}, "chest": {"r": (10, 0, 0)},
                 "head": {"r": (-14, 0, 0), "l": (0, 0, -0.015)}, "jaw": {"r": (36, 0, 0)},
                 "tail1": {"r": (-40, 0, 0)}, "tail2": {"r": (-20, 0, 0)}})
    windup = [merge(lerp_pose(idle[0], coil, 0.55), works(1, 2)),
              merge(coil, works(2, 3)),
              merge(coil, merge(works(3, 3), {"head": {"r": (-14, 0, 3)}, "tail2": {"r": (-20, 0, 12)}})),
              merge(coil, merge(works(4, 3), {"head": {"r": (-14, 0, -3)}, "tail2": {"r": (-20, 0, -12)}}))]
    leap = L.air((-62, -4), (-58, 0), (44, 20), (42, 18))
    leap.update(works(1, 3))
    leap.update({"root": {"l": (0, -0.02, 0.055)}, "pelvis": {"r": (-8, 0, 0)}, "chest": {"r": (-4, 0, 0)},
                 "head": {"r": (-6, 0, 0)}, "jaw": {"r": (42, 0, 0)},
                 "tail1": {"r": (-30, 0, 0)}, "tail2": {"r": (-10, 0, 0)}})
    snap = L.plant(drop=0.03, front=(0.014, 0.018), back=(0.02, 0.02), pitch=12)
    snap.update(works(2, 3))
    snap.update({"root": {"l": (0, -0.02, 0)}, "pelvis": {"l": (0, 0, -0.03)}, "chest": {"r": (12, 0, 0)},
                 "head": {"r": (12, 0, 0), "l": (0, -0.015, 0.0)}, "jaw": {"r": (-2, 0, 0)},
                 "tail1": {"r": (10, 0, 14)}, "tail2": {"r": (12, 0, 14)}})
    settle = lerp_pose(snap, idle[0], 0.5)
    settle.update(L.plant(drop=0.015, front=(0.008, 0.01), back=(0.01, 0.01), pitch=6))
    settle.update(works(3))
    settle["root"] = {"l": (0, -0.016, 0)}
    settle["jaw"] = {"r": (14, 0, 0)}
    back = lerp_pose(snap, idle[0], 0.9)
    back.update(L.plant(drop=0.004, pitch=1))
    back.update(works(4))
    back["root"] = {"l": (0, -0.005, 0)}
    attack = [leap, snap, settle, back]

    hit = [merge(L.plant(drop=0.02, front=(0.02, 0.02), pitch=-10),
                 merge(works(0), {"pelvis": {"l": (0, 0, -0.02)}, "chest": {"r": (-10, 0, 8)},
                                  "head": {"r": (-24, 0, 14)}, "jaw": {"r": (26, 0, 0)},
                                  "tail1": {"r": (40, 0, 0)}, "tail2": {"r": (20, 0, 0)}})),
           merge(L.plant(drop=0.008, front=(0.008, 0.008), pitch=-4),
                 merge(works(0), {"pelvis": {"l": (0, 0, -0.008)}, "chest": {"r": (-4, 0, 3)},
                                  "head": {"r": (-8, 0, 5)}, "jaw": {"r": (8, 0, 0)}}))]

    dr = 0.14
    down = merge(L.plant(drop=dr, front=(0.03, 0.04), back=(0.04, 0.05), pitch=3),
                 {"pelvis": {"l": (0, 0, -dr)}, "chest": {"r": (3, 0, 0)},
                  "head": {"r": (-4, 0, 60), "l": (0, 0.03, -0.03)}, "jaw": {"r": (22, 0, 0)},
                  "tail1": {"r": (60, 0, 40)}, "tail2": {"r": (30, 0, 20)},
                  "gear": {"l": (0.12, 0.06, -0.06), "r": (200, 0, 80)}, "key": {"r": (0, 0, 30)}})
    sag = merge(L.plant(drop=dr * 0.3, front=(-0.01, -0.01), pitch=10),
                {"pelvis": {"l": (0, 0, -dr * 0.3)}, "chest": {"r": (10, 0, 0)},
                 "head": {"r": (10, 0, 14)}, "jaw": {"r": (12, 0, 0)}, "tail1": {"r": (30, 0, 0)},
                 "gear": {"l": (0, 0, 0.05), "r": (120, 0, 0)}, "key": {"r": (0, 0, 20)}})
    die = [merge(L.plant(drop=0.01, pitch=-8), merge(works(1, 2), {"head": {"r": (-26, 0, 0)}, "jaw": {"r": (40, 0, 0)},
                                                                     "pelvis": {"l": (0, 0, -0.01)}, "chest": {"r": (-8, 0, 0)}})),
           sag,
           merge(lerp_pose(sag, down, 0.6), {"gear": {"l": (0.06, 0.02, 0.06), "r": (160, 0, 40)}}),
           down,
           merge(down, {"head": {"r": (0, 0, 64), "l": (0, 0.03, -0.04)}}),
           merge(down, {"head": {"r": (0, 0, 64), "l": (0, 0.03, -0.04)}, "jaw": {"r": (16, 0, 0)}})]
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=10, fps={"idle": 5})
