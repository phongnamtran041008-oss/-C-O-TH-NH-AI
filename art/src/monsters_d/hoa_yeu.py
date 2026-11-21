"""Hoa Yêu (normal, 48): a man-eating flower demon of the maze forest.

A big crimson bloom of seven petals round a dark toothed maw, two glowing eyes on its upper
lip, on a thick thorny stem (one tube skinned to three bones) that rises from a root bulb
on four creeping root-feet. Two broad leaves hang from the stem like arms.

Rig: root, base (bulb), stem1-3, bloom (the head, facing forward and a little up), one bone
per petal (they open and snap shut about their own tangent), two two-bone leaves and four
two-bone roots. Clips: idle sways and breathes; walk creeps on the roots in turn; windup
coils the stem back with the bloom flared wide; attack lunges with the bloom and snaps the
petals shut on the hit frame; die wilts and lays the bloom on the ground.
"""
from __future__ import annotations

import math

from mathutils import Quaternion, Vector

from common import S, att, basis, oriented_ball, six
from rig import aim, armature, ball, cone, lerp_pose, material, merge, prism, skin, tube, use_collection

N_PET = 7
BLOOM_C = Vector((0, -0.10, 0.75))
TILT = math.radians(24)                    # the bloom faces forward and this much up
NRM = Vector((0, -math.cos(TILT), math.sin(TILT)))
UPV = Vector((0, math.sin(TILT), math.cos(TILT)))   # "up" in the bloom's plane
ROOTS = {"rt_fl": (0.11, -0.075), "rt_fr": (-0.11, -0.075), "rt_bl": (0.10, 0.095), "rt_br": (-0.10, 0.095)}
CUP = math.radians(50)


def _radial(k):
    a = math.pi / 2 + math.tau * k / N_PET          # petal 0 at the top
    return (UPV * math.sin(a) + Vector((1, 0, 0)) * math.cos(a)).normalized()


def _petal_q(k, deg):
    """Open (+) / close (-) petal k about its tangent, as an armature-axes quaternion."""
    u = _radial(k)
    axis = u.cross(NRM).normalized()
    return tuple(Quaternion(axis, math.radians(-deg)))


def _root_q(name, deg):
    """Lift (+) a root about the horizontal axis across it."""
    x, y = ROOTS[name]
    h = Vector((x, y, 0)).normalized()
    axis = h.cross(Vector((0, 0, 1))).normalized()
    return tuple(Quaternion(axis, math.radians(deg)))


def build():
    use_collection("COL_hoa_yeu")
    petal = material("MAT_hy_petal", (0.58, 0.19, 0.16), (0.36, 0.21, 0.56), ramp=("red", "purple"))
    petal["kit_light"] = 0.86
    petal_in = material("MAT_hy_petal_inner", (0.78, 0.33, 0.23), (0.52, 0.34, 0.75), ramp=("red", "purple"))
    stem = material("MAT_hy_stem", (0.23, 0.42, 0.15), (0.11, 0.31, 0.25), ramp=("leaf", "jade"))
    stem_dk = material("MAT_hy_sepal", (0.13, 0.25, 0.11), (0.11, 0.31, 0.25), ramp=("leaf", "jade"))
    leaf = material("MAT_hy_leaf", (0.37, 0.58, 0.20), (0.18, 0.48, 0.35), ramp=("leaf", "jade"))
    bulb = material("MAT_hy_bulb", (0.34, 0.20, 0.13), (0.18, 0.16, 0.20), ramp=("wood", "hair"))
    root = material("MAT_hy_root", (0.51, 0.32, 0.18), (0.27, 0.24, 0.30), ramp=("wood", "hair"))
    thorn = material("MAT_hy_thorn", (0.83, 0.75, 0.62), (0.90, 0.72, 0.23), ramp=("bone", "gold"))
    heart = material("MAT_hy_heart", (0.36, 0.10, 0.11), (0.23, 0.13, 0.38), ramp=("red", "purple"))
    maw = material("MAT_hy_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    tooth = material("MAT_hy_tooth", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")
    eye = material("MAT_hy_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=6.0, glow=("holy", "flame"))

    top = (0, -0.05, 0.68)
    bones = [("root", (0, 0, 0), (0, 0, 0.08), None),
             ("base", (0, 0, 0.06), (0, 0, 0.18), "root"),
             ("stem1", (0, 0, 0.18), (0, -0.005, 0.36), "base"),
             ("stem2", (0, -0.005, 0.36), (0, -0.02, 0.53), "stem1"),
             ("stem3", (0, -0.02, 0.53), top, "stem2"),
             ("bloom", top, tuple(Vector(top) + NRM * 0.12), "stem3"),
             ("leaf_l1", (0.04, -0.01, 0.40), (0.15, -0.03, 0.42), "stem1"),
             ("leaf_l2", (0.15, -0.03, 0.42), (0.30, -0.06, 0.36), "leaf_l1"),
             ("leaf_r1", (-0.04, -0.01, 0.40), (-0.15, -0.03, 0.42), "stem1"),
             ("leaf_r2", (-0.15, -0.03, 0.42), (-0.30, -0.06, 0.36), "leaf_r1")]
    for k in range(N_PET):
        u = _radial(k)
        h = BLOOM_C + u * 0.07
        d = (u * math.cos(CUP) + NRM * math.sin(CUP)).normalized()
        bones.append((f"pet{k}", tuple(h), tuple(h + d * 0.16), "bloom"))
    for name, (x, y) in ROOTS.items():
        bones.append((name + "1", (x * 0.45, y * 0.45, 0.09), (x * 0.8, y * 0.8, 0.045), "base"))
        bones.append((name + "2", (x * 0.8, y * 0.8, 0.045), (x, y, 0.012), name + "1"))
    arm = armature("hoa_yeu", bones)

    # ---- the root bulb and the root-feet
    att(arm, "base", ball("hy_bulb", (0.10, 0.10, 0.07), (0, 0, 0.085), bulb, seg=10, rings=7),
        *[ball(f"hy_knob{k}", (0.05, 0.05, 0.045), (0.07 * x / 0.11, 0.07 * y / 0.09, 0.06), bulb, seg=8, rings=5)
          for k, (x, y) in enumerate(ROOTS.values())],
        ball("hy_bulbtop", (0.08, 0.08, 0.05), (0, 0, 0.15), stem_dk, seg=12, rings=6))
    for name in ROOTS:
        b1, b2 = arm.data.bones[name + "1"], arm.data.bones[name + "2"]
        att(arm, name + "1", aim(f"hy_{name}1", root, tuple(b1.head_local), tuple(b1.tail_local), 0.05, 0.036, seg=7))
        att(arm, name + "2", aim(f"hy_{name}2", root, tuple(b2.head_local), tuple(b2.tail_local), 0.036, 0.014, seg=7))

    # ---- the stem: one tube skinned to the three stem bones, thorns on the bones
    pts = [(0, 0, 0.14), (0, 0, 0.22), (0, -0.003, 0.30), (0, -0.008, 0.38), (0, -0.014, 0.46),
           (0, -0.022, 0.54), (0, -0.034, 0.61), (0, -0.05, 0.69)]
    rads = [0.072, 0.066, 0.06, 0.056, 0.052, 0.05, 0.05, 0.052]
    st = tube("hy_stem", pts, rads, stem, seg=12, up=(0, -1, 0))
    skin(st, arm, ["base", "stem1", "stem2", "stem3"], power=3.0)
    for k, (z, a, b) in enumerate(((0.28, 50, "stem1"), (0.33, 200, "stem1"), (0.47, 120, "stem2"),
                                   (0.52, 310, "stem2"), (0.62, 20, "stem3"))):
        r = 0.055
        c = Vector((r * math.cos(math.radians(a)), -0.01 + r * math.sin(math.radians(a)), z))
        o = c + Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0.5)).normalized() * 0.05
        att(arm, b, aim(f"hy_thorn{k}", thorn, tuple(c), tuple(o), 0.016, 0.0, seg=5))

    # ---- the bloom: sepal cup behind, maw, teeth, eyes; petals on their own bones
    c = BLOOM_C
    # a deep green calyx behind the bloom gives it a head-like mass from the side, with
    # five pointed sepals reaching back between the petals
    bloom_parts = [oriented_ball("hy_cup", (0.115, 0.115, 0.075), tuple(c - NRM * 0.045),
                                 (1, 0, 0), tuple(NRM), stem_dk, seg=14, rings=8)]
    for k in range(5):
        a = math.pi / 2 + math.tau * (k + 0.5) / 5
        u = (UPV * math.sin(a) + Vector((1, 0, 0)) * math.cos(a)).normalized()
        bloom_parts.append(aim(f"hy_sepal{k}", stem_dk, tuple(c + u * 0.07 - NRM * 0.05),
                               tuple(c + u * 0.2 - NRM * 0.12), 0.035, 0.0, seg=5))
    # maw: a dark hollow in the middle of the bloom
    # the face in the heart of the bloom: a pale pistil disc, two slanted glowing eyes in
    # its upper half and a wide fanged maw in its lower half
    bloom_parts.append(oriented_ball("hy_heart", (0.10, 0.10, 0.03), tuple(c + NRM * 0.0),
                                     (1, 0, 0), tuple(NRM), heart, seg=16, rings=6))
    mc = c - UPV * 0.03 + NRM * 0.018
    bloom_parts.append(oriented_ball("hy_maw2", (0.075, 0.05, 0.025), tuple(mc),
                                     (1, 0, 0), tuple(NRM), maw, seg=16, rings=6))
    for k in range(7):
        a = math.tau * (k + 0.5) / 7
        u = (UPV * math.sin(a) * 0.68 + Vector((1, 0, 0)) * math.cos(a))
        base = mc + u * 0.078 + NRM * 0.008
        tip = mc + u * 0.03 + NRM * 0.03
        bloom_parts.append(aim(f"hy_tooth{k}", tooth, tuple(base), tuple(tip), 0.024, 0.0, seg=5))
    for s in (1, -1):
        p = c + UPV * 0.058 + Vector((s * 0.042, 0, 0)) + NRM * 0.032
        bloom_parts.append(oriented_ball(f"hy_eye{s}", (0.036, 0.022, 0.014), tuple(p),
                                         (1, 0, -0.5 * s), tuple(NRM), eye, seg=10, rings=6))
    att(arm, "bloom", *bloom_parts)

    # petals: thick spoon-shaped lobes (they read from the side as well as from the front),
    # crimson outside with a lighter lip toward the maw
    for k in range(N_PET):
        u = _radial(k)
        h = c + u * 0.07
        d = (u * math.cos(CUP) + NRM * math.sin(CUP)).normalized()
        t = u.cross(NRM)
        front = d.cross(t) * -1                       # the petal's inner face
        att(arm, f"pet{k}",
            oriented_ball(f"hy_pet{k}", (0.068, 0.11, 0.03), tuple(h + d * 0.095), tuple(t), tuple(front),
                          petal, seg=12, rings=8),
            oriented_ball(f"hy_petin{k}", (0.04, 0.06, 0.02), tuple(h + d * 0.06 + front * 0.016), tuple(t),
                          tuple(front), petal_in, seg=10, rings=6))

    # ---- leaves: a stalk and a broad blade on each side
    for side, s in (("l", 1), ("r", -1)):
        b1, b2 = arm.data.bones[f"leaf_{side}1"], arm.data.bones[f"leaf_{side}2"]
        att(arm, f"leaf_{side}1", aim(f"hy_stalk{side}", stem, tuple(b1.head_local), tuple(b1.tail_local), 0.022, 0.018, seg=6))
        h2, t2 = b2.head_local, b2.tail_local
        mid = (h2 + t2) / 2 + Vector((0, 0, 0.01))
        along = (t2 - h2).normalized()
        nrm = Vector((0, -0.5, 1)).normalized()          # the blade faces up and forward
        att(arm, f"leaf_{side}2",
            oriented_ball(f"hy_leaf{side}", (0.075, 0.024, 0.13), tuple(mid),
                          tuple(nrm.cross(along).normalized()), tuple(along), leaf, seg=12, rings=8),
            aim(f"hy_rib{side}", stem_dk, tuple(h2), tuple(t2 - along * 0.03), 0.013, 0.006, seg=5))

    # ------------------------------------------------------------------ poses
    def petals(deg, wave=0.0, ph=0.0):
        return {f"pet{k}": {"q": _petal_q(k, deg + wave * math.sin(ph + k * 1.3))} for k in range(N_PET)}

    def roots(lifts=None):
        lifts = lifts or {}
        out = {}
        for name in ROOTS:
            v = lifts.get(name, 0.0)
            out[name + "1"] = {"q": _root_q(name, 30 * v), "l": (0, 0, 0.0)}
            out[name + "2"] = {"q": _root_q(name, -18 * v)}
        return out

    def stem_pose(fx=(0, 0, 0), sy=(0, 0, 0), bloom=(0, 0, 0)):
        return {"stem1": {"r": (fx[0], sy[0], 0)}, "stem2": {"r": (fx[1], sy[1], 0)},
                "stem3": {"r": (fx[2], sy[2], 0)}, "bloom": {"r": bloom}}

    def leaves(l1=(0, 0, 0), l2=(0, 0, 0), r1=None, r2=None):
        r1 = r1 if r1 is not None else (l1[0], -l1[1], -l1[2])
        r2 = r2 if r2 is not None else (l2[0], -l2[1], -l2[2])
        return {"leaf_l1": {"r": l1}, "leaf_l2": {"r": l2}, "leaf_r1": {"r": r1}, "leaf_r2": {"r": r2}}

    idle = []
    for i in range(4):
        p = merge(stem_pose((1.5 * S(i, 4, 1.2), 2 * S(i, 4, 0.6), 2 * S(i, 4)),
                            (3 * S(i, 4), 4 * S(i, 4, -0.7), 5 * S(i, 4, -1.4)),
                            (-3 * S(i, 4, 0.6), 0, 5 * S(i, 4, -1.6))),
                  petals(4 + 6 * S(i, 4, -0.8), 3.0, i * 1.6))
        p.update(leaves((0, -6 * S(i, 4, -1.0), 6 * S(i, 4, -1.4)), (0, -8 * S(i, 4, -1.8), 0)))
        p.update(roots())
        p["base"] = {"s": (1 + 0.02 * S(i, 4), 1 + 0.02 * S(i, 4), 1 - 0.03 * S(i, 4))}
        idle.append(p)

    walk = []
    order = (("rt_fl", 0.0), ("rt_br", 0.5), ("rt_fr", 0.25), ("rt_bl", 0.75))
    for i in range(6):
        ph = i / 6
        lifts = {n: max(0.0, math.sin(math.tau * (ph - o))) ** 1.5 for n, o in order}
        s = S(i, 6)
        p = merge(stem_pose((5 + 3 * S(i, 6, 1.0), 3 + 2 * S(i, 6, 0.4), -1), (6 * s, 7 * S(i, 6, -0.7), 8 * S(i, 6, -1.4)),
                            (-4 + 3 * S(i, 6, 0.4), 0, 4 * S(i, 6, -1.5))),
                  petals(10, 2.0, i * 1.1))
        p.update(leaves((10 * S(i, 6, -1.0), -10 * s, 8 * S(i, 6, -1.5)), (8 * S(i, 6, -1.6), -12 * S(i, 6, -1.6), 0),
                        (-10 * S(i, 6, -1.0), 10 * s, -8 * S(i, 6, 1.6)), (-8 * S(i, 6, -1.6), 12 * S(i, 6, 1.6), 0)))
        p.update(roots(lifts))
        p["base"] = {"l": (0, 0, 0.012 * abs(S(i, 3))), "r": (0, 5 * s, 0)}
        walk.append(p)

    # windup: the stem coils back like a drawn bow, the bloom rears and flares wide open,
    # leaves thrown up and out; held with a tremble
    coil = merge(stem_pose((-10, -16, -18), (0, 0, 0), (-16, 0, 0)), petals(38))
    coil.update(leaves((0, -32, 28), (0, -24, 0)))
    coil.update(roots())
    coil["base"] = {"s": (1.05, 1.05, 0.93), "l": (0, 0, -0.006)}
    windup = [lerp_pose(idle[0], coil, 0.55), coil,
              merge(coil, merge(petals(42, 4, 0.0), {"bloom": {"r": (-17, 0, 3)}})),
              merge(coil, merge(petals(40, 4, 2.0), {"bloom": {"r": (-16, 0, -3)}}))]

    # attack: a whip-fast lunge, the bloom snapping shut on the hit frame
    lunge = merge(stem_pose((7, 12, 10), (0, 0, 0), (6, 0, 0)), petals(30))
    lunge.update(leaves((0, 20, -20), (0, 10, 0)))
    lunge.update(roots())
    snap = merge(stem_pose((10, 14, 12), (0, 0, 0), (10, 0, 0)), petals(-26))
    snap.update(leaves((0, 30, -10), (0, 20, 0)))
    snap.update(roots())
    snap["base"] = {"s": (1.04, 1.04, 0.95)}
    back = lerp_pose(snap, idle[0], 0.55)
    back.update(petals(-6))
    attack = [lunge, snap, back, lerp_pose(snap, idle[0], 0.9)]

    hit = [merge(merge(stem_pose((-12, -10, -6), (4, 6, 8), (-14, 0, 8)), petals(-12)),
                 merge(leaves((0, -20, 20), (0, -26, 0)), roots())),
           merge(merge(stem_pose((-5, -4, -2), (2, 2, 3), (-6, 0, 3)), petals(0)), merge(leaves(), roots()))]

    wilt = merge(stem_pose((4, 10, 14), (16, 16, 12), (30, 0, 6)), petals(45, 8, 0.5))
    wilt.update(leaves((40, 30, -40), (30, 30, 0), (40, -30, 40), (30, -30, 0)))
    wilt.update(roots())
    wilt["base"] = {"s": (1.06, 1.06, 0.85), "l": (0, 0, -0.01)}
    wilt["bloom"] = {"r": (40, 0, 10), "s": 0.97}
    die = [merge(merge(stem_pose((-14, -12, -8), (6, 8, 10), (-20, 0, 12)), petals(48)), merge(leaves((0, -30, 30), (0, -30, 0)), roots())),
           merge(merge(stem_pose((-4, 4, 6), (10, 12, 14), (6, 0, 6)), petals(30)), merge(leaves((10, -10, 10), (10, -10, 0)), roots())),
           lerp_pose(idle[0], wilt, 0.45), lerp_pose(idle[0], wilt, 0.85), wilt,
           merge(wilt, {"bloom": {"r": (44, 0, 12), "s": 0.96}})]
    arm.scale = (1.1, 1.1, 1.1)        # a big bloom that fills its frame like its neighbours
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=8)
    return arm


def _shift(dy):
    from mathutils import Matrix
    return Matrix.Translation((0, dy, 0))
