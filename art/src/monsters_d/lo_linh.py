"""Lò Linh (elite, 64): a living alchemy furnace of the workshop quarter.

A round bronze cauldron (a three-legged ding) waddling on three stubby beast-legs. A band of
green patina runs round its belly with bronze bosses; two upright loop handles stand on the
rim; two slanted vents on its front glow like angry eyes, four round vents on its shoulders
puff smoke. The domed lid with its flame finial is hinged at the back and lifts like a jaw:
under it the fire burns.

Rig: root, body, lid (hinged at the back), fire (scales and flickers), blast (a jet of fire
that only exists in the attack), three legs, four smoke puffs. Clips: idle simmers (fire
flicker, lid rattle, smoke); walk is a rolling waddle, one leg lifting at a time; windup
throws the lid wide open, leans back and builds the fire high; attack lurches forward and
blasts a jet of fire out of the open mouth (hit frame 1), then slams the lid; die: the lid
blows off, the fire gutters out and the pot tips over onto its side.
"""
from __future__ import annotations

import math

from common import S, att, six
from rig import aim, armature, ball, cone, lerp_pose, material, merge, tube, use_collection

SC = 1.5
LEGS = {"leg_f_l": (0.065, -0.04), "leg_f_r": (-0.065, -0.04), "leg_b": (0.0, 0.075)}
VENTS = [(0.16, 0.07), (-0.16, 0.07)]
Z = 0.045                        # the pot stands this much higher than at first, to show its legs
BODY_C = (0, 0, 0.40 + Z)
R = 0.25


def build():
    use_collection("COL_lo_linh")
    # a deep bronze (the darkest gold), so the fire and the eyes carry the light
    bronze = material("MAT_ll_bronze", (0.48, 0.30, 0.05), (0.20, 0.25, 0.35), ramp=("gold", "steel"), metal=True)
    bronze_dk = material("MAT_ll_bronze_dark", (0.34, 0.20, 0.13), (0.09, 0.11, 0.17), ramp=("wood", "steel"), metal=True)
    patina = material("MAT_ll_patina", (0.18, 0.48, 0.35), (0.58, 0.19, 0.16), ramp=("jade", "red"))
    boss = material("MAT_ll_boss", (0.90, 0.72, 0.23), (0.78, 0.33, 0.23), ramp=("gold", "red"), metal=True)
    inside = material("MAT_ll_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    mask = material("MAT_ll_mask", (0.18, 0.16, 0.20), (0.18, 0.16, 0.20), ramp="hair")
    fire = material("MAT_ll_fire", (1.0, 0.68, 0.23), (0.35, 0.88, 0.96), emit=4.0, glow=("flame", "spirit"))
    fire["kit_halo"] = 1
    core = material("MAT_ll_fire_core", (1.0, 0.95, 0.70), (0.85, 0.98, 1.0), emit=6.0, glow=("flame", "spirit"))
    eye = material("MAT_ll_eye", (1.0, 0.68, 0.23), (0.35, 0.88, 0.96), emit=6.0, glow=("flame", "spirit"))
    smoke = material("MAT_ll_smoke", (0.81, 0.80, 0.83), (0.60, 0.58, 0.64), ramp=("bone", "bone"))

    bones = [("root", (0, 0, 0), (0, 0, 0.1), None),
             ("body", (0, 0, 0.12 + Z), (0, 0, 0.40 + Z), "root"),
             ("lid", (0, 0.20, 0.625 + Z), (0, -0.20, 0.625 + Z), "body"),
             ("fire", (0, 0, 0.56 + Z), (0, 0, 0.72 + Z), "body"),
             ("blast", (0, -0.18, 0.56 + Z), (0, -0.34, 0.55 + Z), "body")]
    for name, (x, y) in LEGS.items():
        bones.append((name, (x * 2.3, y * 2.3, 0.30), (x, y, 0.03), "body"))
    for k, (x, y) in enumerate(VENTS):
        bones.append((f"puff{k}", (x, y, 0.56 + Z), (x * 1.2, y * 1.2, 0.68 + Z), "body"))
    arm = armature("lo_linh", bones)

    # ---- the cauldron: round belly, patina band with bosses, rim collar, handles
    parts = [ball("ll_belly", (R, R, 0.23), BODY_C, bronze, seg=20, rings=12),
             cone("ll_band", R + 0.012, R + 0.012, 0.07, (0, 0, 0.37 + Z), patina, seg=20),
             cone("ll_neck", 0.19, 0.205, 0.09, (0, 0, 0.58 + Z), bronze_dk, seg=18),
             cone("ll_rim", 0.215, 0.215, 0.03, (0, 0, 0.615 + Z), boss, seg=18),
             cone("ll_hole", 0.17, 0.17, 0.035, (0, 0, 0.618 + Z), inside, seg=16)]
    for k in range(10):
        a = math.tau * (k + 0.5) / 10
        if abs(math.sin(a) + 1) < 0.35:          # leave the face clear
            continue
        parts.append(ball(f"ll_boss{k}", (0.026,) * 3, ((R + 0.012) * math.cos(a), (R + 0.012) * math.sin(a), 0.37 + Z),
                          boss, seg=8, rings=5))
    for s in (1, -1):
        pts = [(s * 0.19, 0.055 * math.cos(t), 0.63 + Z + 0.10 * math.sin(t))
               for t in [math.pi * k / 10 for k in range(11)]]
        parts.append(tube(f"ll_handle{s}", pts, [0.022] * 11, boss, seg=6, up=(1, 0, 0)))
    # the face: a dark beast-mask plate on the front with two slanted glowing eyes, a heavy
    # brow over them and three bronze fangs under them
    parts.append(ball("ll_maskplate", (0.16, 0.04, 0.10), (0, -0.215, 0.47 + Z), mask, seg=14, rings=8))
    for s in (1, -1):
        parts.append(_slit(f"ll_eye{s}", (s * 0.07, -0.248, 0.485 + Z), s, eye))
        parts.append(aim(f"ll_brow{s}", boss, (s * 0.015, -0.255, 0.53 + Z), (s * 0.15, -0.215, 0.555 + Z), 0.024, 0.016, seg=6))
    for k, x in enumerate((-0.05, 0.0, 0.05)):
        parts.append(aim(f"ll_fang{k}", boss, (x, -0.25, 0.43 + Z), (x, -0.255, 0.395 + Z), 0.018, 0.0, seg=5))
    for k, (x, y) in enumerate(VENTS):
        parts.append(ball(f"ll_vent{k}", (0.036, 0.036, 0.022), (x, y, 0.53 + Z), inside, seg=8, rings=5))
    att(arm, "body", *parts)

    # ---- the lid: dome, lip and a flame-bud finial
    att(arm, "lid", ball("ll_lid", (0.205, 0.205, 0.085), (0, 0, 0.635 + Z), bronze, seg=18, rings=8),
        cone("ll_lip", 0.22, 0.22, 0.022, (0, 0, 0.635 + Z), boss, seg=18),
        cone("ll_stem", 0.03, 0.025, 0.06, (0, 0, 0.73 + Z), bronze_dk, seg=8),
        ball("ll_bud", (0.05, 0.05, 0.06), (0, 0, 0.78 + Z), boss, seg=10, rings=6),
        aim("ll_budtip", boss, (0, 0, 0.82 + Z), (0, 0, 0.87 + Z), 0.03, 0.0, seg=6),
        *[ball(f"ll_lidstud{k}", (0.02,) * 3, (0.15 * math.cos(a), 0.15 * math.sin(a), 0.675 + Z), boss, seg=6, rings=4)
          for k, a in enumerate(math.tau * j / 6 + 0.5 for j in range(6))])

    # ---- the fire inside, the blast, the smoke puffs
    att(arm, "fire", ball("ll_flamebed", (0.15, 0.15, 0.05), (0, 0, 0.6 + Z), fire, seg=12, rings=6),
        aim("ll_flame0", fire, (0, 0, 0.58 + Z), (0, 0.01, 0.80 + Z), 0.09, 0.0, seg=8),
        aim("ll_flame1", fire, (0.07, 0.02, 0.58 + Z), (0.10, 0.03, 0.73 + Z), 0.06, 0.0, seg=7),
        aim("ll_flame2", fire, (-0.07, -0.02, 0.58 + Z), (-0.10, -0.03, 0.74 + Z), 0.06, 0.0, seg=7),
        ball("ll_core", (0.06, 0.06, 0.06), (0, 0, 0.64 + Z), core, seg=8, rings=5))
    att(arm, "blast", aim("ll_jet", fire, (0, -0.18, 0.57 + Z), (0, -0.33, 0.56 + Z), 0.08, 0.12, seg=10),
        ball("ll_jethead", (0.12, 0.08, 0.11), (0, -0.35, 0.56 + Z), fire, seg=10, rings=6),
        aim("ll_jetcore", core, (0, -0.18, 0.57 + Z), (0, -0.32, 0.56 + Z), 0.04, 0.06, seg=8))
    for k, (x, y) in enumerate(VENTS):
        att(arm, f"puff{k}", ball(f"ll_puff{k}a", (0.07,) * 3, (x * 1.05, y * 1.05, 0.62 + Z), smoke, seg=10, rings=6),
            ball(f"ll_puff{k}b", (0.055,) * 3, (x * 1.15, y * 1.15, 0.72 + Z), smoke, seg=8, rings=5))

    # ---- stubby beast-legs angled in under the belly, clawed feet
    for name, (x, y) in LEGS.items():
        top = (x * 2.3, y * 2.3, 0.30)
        att(arm, name, aim(f"ll_{name}", bronze_dk, top, (x, y, 0.06), 0.055, 0.04, seg=10, smooth=True),
            ball(f"ll_{name}knee", (0.055, 0.055, 0.05), (x * 1.7, y * 1.7, 0.18), bronze, seg=8, rings=5),
            ball(f"ll_{name}foot", (0.04, 0.045, 0.03), (x, y - 0.005, 0.03), bronze, seg=8, rings=5),
            *[aim(f"ll_{name}claw{k}", boss, (x + d, y - 0.03, 0.025), (x + d * 1.2, y - 0.055, 0.008), 0.012, 0.0, seg=4)
              for k, d in enumerate((-0.022, 0.0, 0.022))])


    clips(arm)
    arm.scale = (SC, SC, SC)
    for d in ("down", "up", "side"):     # tripod wider than the ground band, see scene.py
        arm[f"shift_{d}"] = 0.04
    return arm


def _slit(name, center, s, mat):
    """A slanted glowing eye slit (an ellipsoid tilted down toward the middle)."""
    return ball(name, (0.045, 0.02, 0.018), center, mat, rot=(0, -22 * s, 0), seg=10, rings=6)


def clips(arm):
    def puffs(t, big=1.0):
        """Smoke puffs cycle out of the vents at staggered phases (t in quarter cycles)."""
        out = {}
        for k in range(len(VENTS)):
            ph = (t + k * 0.5) % 1.0
            out[f"puff{k}"] = {"s": big * (0.35 + 0.9 * ph) if ph < 0.85 else 0.0, "l": (0, 0, 0.06 * ph)}
        return out

    def base(i, n=4, fire_s=0.75, lid=0.0):
        p = {"body": {"s": (1 + 0.015 * S(i, n), 1 + 0.015 * S(i, n), 1 - 0.015 * S(i, n))},
             "fire": {"s": fire_s * (1 + 0.12 * S(i, n, 1.3)), "r": (0, 0, 25 * S(i, n))},
             "blast": {"s": 0.0},
             "lid": {"r": (lid, 0, 0)}}
        p.update(puffs(i / n))
        return p

    idle = [merge(base(i, lid=(0, -4, 0, -2)[i]), {}) for i in range(4)]

    walk = []
    order = ("leg_f_l", "leg_b", "leg_f_r")
    for i in range(6):
        p = base(i, 6, lid=-3 * abs(S(i, 3)))
        up = order[(i // 2) % 3]
        lift = (0.6, 1.0)[i % 2]
        x, y = LEGS[up]
        roll = 7 * (1 if x < 0 else -1 if x > 0 else 0) * lift
        pitch = (6 if y > 0 else -4) * lift if x == 0 else -3 * lift
        p["body"] = {"r": (pitch, roll, 5 * S(i, 6)), "l": (0, 0, 0.008 * lift)}
        for name in LEGS:
            # the lifted leg comes off the ground; the others stay planted under the roll
            p[name] = {"l": (0, 0, 0.026 * lift if name == up else -0.008 * lift)}
        walk.append(p)

    gape = base(0, fire_s=1.5, lid=-68)
    gape["body"] = {"r": (-9, 0, 0), "s": (1.04, 1.04, 1.04), "l": (0, 0.02, 0)}
    gape.update(puffs(0.6, 1.4))
    windup = [merge(base(0, fire_s=1.1, lid=-30), {"body": {"r": (-4, 0, 0)}}), gape,
              merge(gape, {"fire": {"s": 1.65, "r": (0, 0, 30)}, "lid": {"r": (-70, 0, 0)}}),
              merge(gape, merge(puffs(0.9, 1.4), {"fire": {"s": 1.55, "r": (0, 0, -20)}, "lid": {"r": (-66, 0, 0)}}))]

    lurch = base(0, fire_s=1.2, lid=-58)
    lurch["body"] = {"r": (10, 0, 0), "l": (0, -0.02, 0)}
    lurch["blast"] = {"s": (0.8, 0.55, 0.8)}
    blast = base(1, fire_s=1.0, lid=-60)
    blast["body"] = {"r": (12, 0, 0), "l": (0, -0.025, 0)}
    blast["blast"] = {"s": 1.0}
    blast.update(puffs(0.3, 1.5))
    fade = base(2, fire_s=0.8, lid=-30)
    fade["body"] = {"r": (5, 0, 0)}
    fade["blast"] = {"s": (0.6, 1.05, 0.6), "l": (0, -0.04, 0.02)}
    slam = base(3, fire_s=0.6, lid=2)
    slam["body"] = {"r": (1, 0, 0), "s": (1.04, 1.04, 0.96)}
    attack = [lurch, blast, fade, slam]

    hit = [merge(base(0, fire_s=1.2, lid=-24), merge(puffs(0.5, 1.5), {"body": {"r": (-10, 0, 6), "l": (0, 0.02, 0.01)}})),
           merge(base(1, fire_s=0.9, lid=-6), {"body": {"r": (-4, 0, 2)}})]

    tip = {"body": {"r": (24, 22, 0), "l": (-0.05, -0.02, -0.08)}, "lid": {"r": (-150, 0, 0), "l": (0, 0.05, -0.36)},
           "fire": {"s": 0.0}, "blast": {"s": 0.0},
           "leg_f_l": {"l": (0, 0, 0.02)}, "leg_f_r": {"r": (0, 0, 0), "l": (0, 0, 0.0)}}
    for k in range(len(VENTS)):
        tip[f"puff{k}"] = {"s": 0.0}
    die = [merge(base(0, fire_s=1.5, lid=-40), merge(puffs(0.7, 1.6), {"body": {"r": (-10, 0, 0)}})),
           merge(base(1, fire_s=1.3, lid=-110), merge(puffs(0.2, 1.8), {"lid": {"r": (-95, 0, 0), "l": (0, 0.04, 0.0)},
                                                                         "body": {"r": (-6, 6, 0)}})),
           merge(base(2, fire_s=0.6, lid=-140), {"lid": {"r": (-140, 0, 0), "l": (0, 0.07, -0.10)}, "body": {"r": (0, 14, 0)}}),
           merge(lerp_pose(base(0), tip, 0.7), {"fire": {"s": 0.25}}),
           merge(tip, {"puff0": {"s": 0.8, "l": (0, 0, 0.08)}, "puff1": {"s": 0.6, "l": (0, 0, 0.04)}}),
           merge(tip, {"puff0": {"s": 1.0, "l": (0, 0, 0.14)}, "puff1": {"s": 0.8, "l": (0, 0, 0.10)}})]
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=8)
