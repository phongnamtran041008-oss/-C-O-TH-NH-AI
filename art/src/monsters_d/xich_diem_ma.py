"""Xích Diễm Mã (elite, 64): the flame horse of the archery grassland.

A lean horse in red-bronze with a mane and a tail of fire. Built on real horse lines: a deep
chest and a sloping shoulder, the withers a little higher than the croup, a round rump and
haunch, a long arched neck carrying a wedge-shaped head (wide cheek, long face, dark muzzle,
small pointed ears, ember eyes). Forelegs: forearm, knee, cannon, fetlock, pastern, hoof;
hind legs: gaskin angled back to the hock, then a near-vertical cannon. Dark socks and
hooves; at each hoof a little ember that flares when that hoof lands.

Rig: root, body (pitches about the hips), two neck bones, head, two mane bones and a
forelock that lag behind the neck, three tail bones; each leg is a two-bone limb (forearm +
cannon / gaskin + cannon) posed by the planar IK of common.py, front knees bending forward,
hocks backward, pasterns kept flat on the ground in stance and flipped back in the swing.

Clips: idle breathes, the flames flicker and the head and tail swing; walk is a real
four-beat walk (left hind, left fore, right hind, right fore, a quarter cycle apart) with the
head nodding at each fore footfall and embers at the landing hoof; windup rears on the hind
legs with the forelegs tucked and the mane flaring; attack drops into a charge, neck
stretched, forelegs striking out (hit frame 1); die buckles to the knees and lies down as the
fire dies.
"""
from __future__ import annotations

import math

from common import Limb, S, att, posed, rest_table, six
from rig import (aim, armature, ball, cone, lerp_pose, material, merge, set_root_offset, shadow,
                 shadow_material, use_collection)

SC = 1.15
BODY_H = (0.18, 0.52)
FX, HX = 0.085, 0.09          # half track of the fore and hind legs

BONES = [
    ("root", (0, 0, 0), (0, 0, 0.1), None),
    ("shadow", (0, 0.0225, 0.0), (0, -0.08, 0.0), "root"),
    ("body", (0, 0.18, 0.52), (0, -0.20, 0.56), "root"),
    ("neck1", (0, -0.22, 0.58), (0, -0.32, 0.74), "body"),
    ("neck2", (0, -0.32, 0.74), (0, -0.41, 0.86), "neck1"),
    ("head", (0, -0.41, 0.86), (0, -0.59, 0.71), "neck2"),
    ("mane1", (0, -0.24, 0.66), (0, -0.16, 0.76), "neck1"),
    ("mane2", (0, -0.34, 0.80), (0, -0.27, 0.90), "neck2"),
    ("forelock", (0, -0.42, 0.90), (0, -0.46, 0.97), "head"),
    ("tail1", (0, 0.30, 0.57), (0, 0.38, 0.62), "body"),
    ("tail2", (0, 0.38, 0.62), (0, 0.46, 0.58), "tail1"),
    ("tail3", (0, 0.46, 0.58), (0, 0.52, 0.47), "tail2"),
]
for _s, _x in (("l", 1), ("r", -1)):
    BONES += [
        (f"fu_{_s}", (_x * FX, -0.20, 0.38), (_x * FX, -0.20, 0.20), "body"),
        (f"fc_{_s}", (_x * FX, -0.20, 0.20), (_x * FX, -0.205, 0.065), f"fu_{_s}"),
        (f"fh_{_s}", (_x * FX, -0.205, 0.065), (_x * FX, -0.225, 0.0), f"fc_{_s}"),
        (f"hu_{_s}", (_x * HX, 0.15, 0.40), (_x * HX, 0.27, 0.22), "body"),
        (f"hc_{_s}", (_x * HX, 0.27, 0.22), (_x * HX, 0.25, 0.065), f"hu_{_s}"),
        (f"hh_{_s}", (_x * HX, 0.25, 0.065), (_x * HX, 0.23, 0.0), f"hc_{_s}"),
        (f"emf_{_s}", (_x * FX, -0.21, 0.02), (_x * FX, -0.21, 0.08), f"fh_{_s}"),
        (f"emh_{_s}", (_x * HX, 0.245, 0.02), (_x * HX, 0.245, 0.08), f"hh_{_s}"),
    ]
REST = rest_table(BONES)
FRONT = {s: Limb((f"fu_{s}", f"fc_{s}", f"fh_{s}"), REST, bend=-1) for s in "lr"}
HIND = {s: Limb((f"hu_{s}", f"hc_{s}", f"hh_{s}"), REST, bend=+1) for s in "lr"}


def build():
    use_collection("COL_xich_diem_ma")
    set_root_offset((0, -0.0225, 0))          # the middle of the hooves on the pivot
    coat = material("MAT_xd_coat", (0.58, 0.19, 0.16), (0.18, 0.16, 0.20), ramp=("red", "hair"))
    coat2 = material("MAT_xd_coat_limb", (0.58, 0.19, 0.16), (0.18, 0.16, 0.20), ramp=("red", "hair"))
    sock = material("MAT_xd_sock", (0.36, 0.10, 0.11), (0.11, 0.10, 0.13), ramp=("red", "hair"))
    hoof = material("MAT_xd_hoof", (0.18, 0.16, 0.20), (0.73, 0.51, 0.10), ramp=("hair", "gold"))
    muzzle = material("MAT_xd_nose", (0.18, 0.16, 0.20), (0.27, 0.24, 0.30), ramp=("hair", "hair"))
    flame = material("MAT_xd_flame", (1.0, 0.68, 0.23), (0.35, 0.88, 0.96), emit=4.0, glow=("flame", "spirit"))
    flame["kit_halo"] = 1
    core = material("MAT_xd_flame_core", (1.0, 0.95, 0.70), (0.85, 0.98, 1.0), emit=6.0, glow=("flame", "spirit"))
    ember = material("MAT_xd_ember", (1.0, 0.68, 0.23), (0.35, 0.88, 0.96), emit=5.0, glow=("flame", "spirit"))
    eye = material("MAT_xd_eye", (1.0, 0.89, 0.48), (0.85, 0.98, 1.0), emit=6.0, glow=("holy", "spirit"))

    arm = armature("xich_diem_ma", BONES)

    # ---- trunk: barrel, deep chest, sloping shoulder, withers, croup, rump and haunches
    att(arm, "body",
        ball("xd_barrel", (0.14, 0.29, 0.135), (0, 0.0, 0.48), coat, seg=16, rings=10),
        ball("xd_chest", (0.135, 0.12, 0.14), (0, -0.19, 0.49), coat, seg=14, rings=8),
        aim("xd_shoulder", coat, (0, -0.15, 0.62), (0, -0.27, 0.46), 0.075, 0.06, seg=10, smooth=True),
        ball("xd_withers", (0.065, 0.09, 0.05), (0, -0.15, 0.60), coat, seg=10, rings=6),
        ball("xd_rump", (0.145, 0.13, 0.13), (0, 0.20, 0.51), coat, seg=14, rings=8),
        ball("xd_croup", (0.10, 0.10, 0.05), (0, 0.17, 0.595), coat, seg=10, rings=6),
        aim("xd_haunchl", coat, (0.05, 0.20, 0.53), (HX, 0.12, 0.39), 0.075, 0.05, seg=10, smooth=True),
        aim("xd_haunchr", coat, (-0.05, 0.20, 0.53), (-HX, 0.12, 0.39), 0.075, 0.05, seg=10, smooth=True),
        aim("xd_elbowl", coat, (FX * 0.8, -0.24, 0.47), (FX, -0.20, 0.37), 0.05, 0.04, seg=8, smooth=True),
        aim("xd_elbowr", coat, (-FX * 0.8, -0.24, 0.47), (-FX, -0.20, 0.37), 0.05, 0.04, seg=8, smooth=True))

    # ---- neck and head
    att(arm, "neck1", aim("xd_neck1", coat, (0, -0.19, 0.54), (0, -0.33, 0.75), 0.10, 0.07, seg=12, smooth=True))
    att(arm, "neck2", aim("xd_neck2", coat, (0, -0.32, 0.73), (0, -0.41, 0.86), 0.072, 0.056, seg=12, smooth=True),
        ball("xd_throat", (0.05, 0.05, 0.06), (0, -0.40, 0.79), coat, seg=8, rings=5))
    att(arm, "head",
        ball("xd_cheek", (0.062, 0.07, 0.065), (0, -0.445, 0.83), coat, seg=12, rings=8),
        aim("xd_face", coat, (0, -0.44, 0.85), (0, -0.585, 0.715), 0.052, 0.036, seg=10, smooth=True),
        ball("xd_muzzle", (0.04, 0.045, 0.042), (0, -0.585, 0.71), muzzle, seg=10, rings=6),
        ball("xd_eyel", (0.016, 0.022, 0.016), (0.052, -0.47, 0.84), eye, seg=8, rings=5),
        ball("xd_eyer", (0.016, 0.022, 0.016), (-0.052, -0.47, 0.84), eye, seg=8, rings=5),
        aim("xd_earl", coat, (0.03, -0.41, 0.89), (0.045, -0.39, 0.975), 0.022, 0.0, seg=5),
        aim("xd_earr", coat, (-0.03, -0.41, 0.89), (-0.045, -0.39, 0.975), 0.022, 0.0, seg=5))
    # ---- fire: mane along the crest, forelock, tail
    m1 = [aim(f"xd_mane1_{k}", flame, (0, y, z), (0, y + 0.07, z + 0.10), r, 0.0, seg=6)
          for k, (y, z, r) in enumerate(((-0.17, 0.62, 0.045), (-0.22, 0.66, 0.05), (-0.27, 0.71, 0.05)))]
    m1.append(aim("xd_mane1_core", core, (0, -0.23, 0.66), (0, -0.19, 0.72), 0.025, 0.0, seg=5))
    att(arm, "mane1", *m1)
    m2 = [aim(f"xd_mane2_{k}", flame, (0, y, z), (0, y + 0.075, z + 0.095), r, 0.0, seg=6)
          for k, (y, z, r) in enumerate(((-0.31, 0.76, 0.048), (-0.355, 0.81, 0.045), (-0.395, 0.86, 0.04)))]
    m2.append(aim("xd_mane2_core", core, (0, -0.34, 0.79), (0, -0.30, 0.85), 0.022, 0.0, seg=5))
    att(arm, "mane2", *m2)
    att(arm, "forelock", aim("xd_forelock", flame, (0, -0.43, 0.89), (0, -0.46, 0.98), 0.035, 0.0, seg=6))
    att(arm, "tail1", aim("xd_tail1", flame, (0, 0.29, 0.57), (0, 0.39, 0.64), 0.04, 0.06, seg=8),
        aim("xd_tailroot", coat, (0, 0.27, 0.57), (0, 0.33, 0.60), 0.035, 0.03, seg=6))
    att(arm, "tail2", aim("xd_tail2", flame, (0, 0.38, 0.63), (0, 0.47, 0.57), 0.065, 0.05, seg=8),
        aim("xd_tail2c", core, (0, 0.39, 0.62), (0, 0.45, 0.58), 0.025, 0.0, seg=5))
    att(arm, "tail3", aim("xd_tail3", flame, (0, 0.46, 0.58), (0, 0.53, 0.44), 0.055, 0.0, seg=8))

    # ---- legs
    for s, x in (("l", 1), ("r", -1)):
        att(arm, f"fu_{s}", aim(f"xd_forearm{s}", coat2, (x * FX, -0.20, 0.40), (x * FX, -0.20, 0.205), 0.038, 0.025, seg=8, smooth=True))
        att(arm, f"fc_{s}", ball(f"xd_knee{s}", (0.027, 0.03, 0.03), (x * FX, -0.20, 0.20), sock, seg=8, rings=5),
            aim(f"xd_fcannon{s}", sock, (x * FX, -0.20, 0.20), (x * FX, -0.205, 0.07), 0.021, 0.02, seg=8),
            ball(f"xd_ffetlock{s}", (0.026, 0.03, 0.026), (x * FX, -0.205, 0.065), sock, seg=8, rings=5))
        att(arm, f"fh_{s}", aim(f"xd_fpastern{s}", sock, (x * FX, -0.205, 0.065), (x * FX, -0.215, 0.03), 0.02, 0.022, seg=8),
            cone(f"xd_fhoof{s}", 0.03, 0.025, 0.035, (x * FX, -0.222, 0.0175), hoof, seg=10))
        att(arm, f"hu_{s}", aim(f"xd_gaskin{s}", coat2, (x * HX, 0.15, 0.40), (x * HX, 0.27, 0.225), 0.045, 0.028, seg=8, smooth=True))
        att(arm, f"hc_{s}", ball(f"xd_hock{s}", (0.026, 0.035, 0.03), (x * HX, 0.272, 0.22), sock, seg=8, rings=5),
            aim(f"xd_hcannon{s}", sock, (x * HX, 0.27, 0.22), (x * HX, 0.25, 0.07), 0.022, 0.02, seg=8),
            ball(f"xd_hfetlock{s}", (0.026, 0.03, 0.026), (x * HX, 0.25, 0.065), sock, seg=8, rings=5))
        att(arm, f"hh_{s}", aim(f"xd_hpastern{s}", sock, (x * HX, 0.25, 0.065), (x * HX, 0.24, 0.03), 0.02, 0.022, seg=8),
            cone(f"xd_hhoof{s}", 0.03, 0.025, 0.035, (x * HX, 0.233, 0.0175), hoof, seg=10))
        att(arm, f"emf_{s}", *_embers(f"xd_emf{s}", x * FX, -0.215, ember))
        att(arm, f"emh_{s}", *_embers(f"xd_emh{s}", x * HX, 0.24, ember))

    # a flat contact shadow under the hooves (its own bone, so the rearing windup can draw
    # it in): grounds the horse and keeps the middle of the lowest rows on the pivot while
    # a hoof is in the air
    sh = shadow("xd_shadow", 0.14, 0.27, shadow_material("MAT_xd_shadow"), arm)
    att(arm, "shadow", sh)
    clips(arm)
    arm.scale = (SC, SC, SC)
    # the hooves span more than the ground band when it faces the camera or away from it
    arm["shift_down"] = 0.21
    arm["shift_up"] = 0.18
    arm["shift_side"] = 0.03
    arm["shift_down_windup"] = 0.08     # rearing: only the hind hooves touch the ground
    return arm


def _embers(name, x, y, mat):
    return [ball(f"{name}a", (0.022,) * 3, (x + 0.02, y + 0.03, 0.03), mat, seg=6, rings=4),
            ball(f"{name}b", (0.016,) * 3, (x - 0.02, y + 0.05, 0.05), mat, seg=6, rings=4),
            ball(f"{name}c", (0.013,) * 3, (x + 0.005, y + 0.07, 0.075), mat, seg=6, rings=4)]


# ------------------------------------------------------------------ animation
def hoof_path(phase, s, lift, stance=0.75):
    """Hoof offset (dy back, lift) for one leg of a walk: on the ground and drifting back
    for `stance` of the cycle, then lifted and carried forward."""
    p = phase % 1.0
    if p < stance:
        return -s + 2 * s * p / stance, 0.0, 0.0
    q = (p - stance) / (1 - stance)
    return s - 2 * s * q, lift * math.sin(math.pi * q), q


def pose(t=(0.0, 0.0), p=0.0, fore=None, hind=None, fore_fk=None, hind_fk=None, neck=(0, 0), head=0.0,
         turn=0.0, mane=0.0, mane_s=1.0, tail=(0, 0, 0), tail_side=0.0, embers=None, root_y=0.0, fire=1.0,
         shadow_s=1.0):
    """fore / hind: {side: (dy, lift, flip)} hoof targets; *_fk: {side: (upper, lower, hoof)}
    absolute changes of angle. neck: (neck1, neck2) pitch; mane: lag pitch of the fire."""
    fore, hind = fore or {}, hind or {}
    out = {"root": {"l": (0, root_y, 0)}, "shadow": {"s": shadow_s},
           "body": {"l": (0, t[0], t[1]), "r": (p, 0, 0)},
           "neck1": {"r": (neck[0], 0, turn * 0.5)}, "neck2": {"r": (neck[1], 0, turn * 0.5)},
           "head": {"r": (head, 0, 0)},
           "mane1": {"r": (mane, 0, 0), "s": mane_s * fire}, "mane2": {"r": (mane * 1.2, 0, 0), "s": mane_s * fire},
           "forelock": {"r": (mane * 0.8, 0, 0), "s": fire},
           "tail1": {"r": (tail[0], 0, tail_side), "s": fire}, "tail2": {"r": (tail[1], 0, tail_side * 1.3)},
           "tail3": {"r": (tail[2], 0, tail_side * 1.6)}}
    for s in "lr":
        hip = posed(FRONT[s].hip, BODY_H, t, p)
        if fore_fk and s in fore_fk:
            u, lo, hf = fore_fk[s]
            out.update(FRONT[s].fk(u, lo, parent_delta=p, foot_world=hf))
        else:
            dy, lift, flip = fore.get(s, (0.0, 0.0, 0.0))
            e = FRONT[s].end
            out.update(FRONT[s].solve(hip, (e[0] + dy, e[1] + lift), p, foot_world=60 * flip))
        hip = posed(HIND[s].hip, BODY_H, t, p)
        if hind_fk and s in hind_fk:
            u, lo, hf = hind_fk[s]
            out.update(HIND[s].fk(u, lo, parent_delta=p, foot_world=hf))
        else:
            dy, lift, flip = hind.get(s, (0.0, 0.0, 0.0))
            e = HIND[s].end
            out.update(HIND[s].solve(hip, (e[0] + dy, e[1] + lift), p, foot_world=50 * flip))
    em = embers or {}
    for k in ("emf_l", "emf_r", "emh_l", "emh_r"):
        out[k] = {"s": em.get(k, 0.0)}
    return out


def clips(arm):
    idle = []
    for i in range(4):
        b = 0.004 * S(i, 4)
        idle.append(pose(t=(0, -abs(b)), neck=(2 * S(i, 4, 0.5), 2 * S(i, 4, 0.9)), head=3 * S(i, 4, 1.2),
                         turn=(0, 8, 8, 0)[i], mane=-6 + 8 * S(i, 4), mane_s=1.0 + 0.1 * S(i, 4, 1.7),
                         tail=(8 * S(i, 4), 10 * S(i, 4, -0.8), 12 * S(i, 4, -1.6)), tail_side=14 * S(i, 4, -0.5),
                         fore={"l": (0.0, 0.0, 0.0), "r": (0.0, 0.0, 0.0)},
                         hind={"l": (0.0, 0.0, 0.0), "r": (0.012, 0.02 if i in (1, 2) else 0.0, 0.3 if i in (1, 2) else 0.0)}))

    # walk: lateral-sequence four-beat walk (LH, LF, RH, RF)
    walk = []
    s_f, s_h, lift = 0.045, 0.04, 0.07
    offs = {"hl": 0.0, "fl": 0.25, "hr": 0.5, "fr": 0.75}
    for i in range(6):
        ph = i / 6
        legs = {k: hoof_path(ph + o, s_f if k[0] == "f" else s_h, lift) for k, o in offs.items()}
        em = {}
        for k, o in offs.items():
            q = (ph + o) % 1.0
            if q < 0.2:                       # this hoof has just landed: a puff of embers
                em[("emf_" if k[0] == "f" else "emh_") + k[1]] = 1.0 - q * 3
        nod = math.cos(math.tau * (ph - 0.25) * 2)
        walk.append(pose(t=(0, -0.006 * (1 + nod) * 0.5), p=1.2 * math.sin(math.tau * ph * 2),
                         fore={"l": legs["fl"], "r": legs["fr"]}, hind={"l": legs["hl"], "r": legs["hr"]},
                         neck=(3 * nod, 2 * nod), head=2 * nod, mane=-14 - 4 * nod, mane_s=1.05,
                         tail=(-6, 6 * S(i, 6), 10 * S(i, 6, -0.9)), tail_side=10 * S(i, 6, -0.6), embers=em))

    # windup: rears on the hind legs, forelegs tucked, head up, mane and tail flaring
    rear = pose(t=(0.0, 0.0), p=-20, fore_fk={"l": (-95, -10, 30), "r": (-80, 0, 30)},
                hind={"l": (-0.035, 0.0, 0.0), "r": (-0.02, 0.0, 0.0)},
                neck=(14, 6), head=10, mane=-22, mane_s=1.35, tail=(28, 10, -6), tail_side=0, shadow_s=0.7)
    windup = [pose(t=(0.0, -0.01), p=-12, fore_fk={"l": (-60, 10, 30), "r": (-45, 15, 25)},
                   hind={"l": (-0.03, 0.0, 0.0), "r": (-0.02, 0.0, 0.0)},
                   neck=(8, 4), head=6, mane=-16, mane_s=1.2, tail=(16, 6, 0), shadow_s=0.7),
              rear,
              merge(rear, pose(t=(0.0, 0.0), p=-22, fore_fk={"l": (-80, 0, 30), "r": (-98, -14, 30)},
                               hind={"l": (-0.035, 0.0, 0.0), "r": (-0.02, 0.0, 0.0)},
                               neck=(12, 6), head=12, mane=-28, mane_s=1.45, tail=(30, 14, -10), tail_side=8, shadow_s=0.7)),
              merge(rear, pose(t=(0.0, 0.0), p=-21, fore_fk={"l": (-96, -12, 30), "r": (-82, 0, 30)},
                               hind={"l": (-0.035, 0.0, 0.0), "r": (-0.02, 0.0, 0.0)},
                               neck=(14, 6), head=10, mane=-24, mane_s=1.4, tail=(28, 10, -8), tail_side=-8, shadow_s=0.7))]

    # attack: drops out of the rear into a charge; the forelegs strike out on the hit frame
    lunge = pose(t=(0.0, -0.01), p=6, fore_fk={"l": (-82, -58, 20), "r": (-76, -46, 10)},
                 hind={"l": (0.03, 0.0, 0.0), "r": (0.045, 0.02, 0.3)},
                 neck=(14, 5), head=12, mane=-40, mane_s=1.4, tail=(-12, -6, 0), root_y=-0.01)
    strike = pose(t=(0.0, -0.025), p=8, fore={"l": (-0.015, 0.0, 0.0), "r": (0.0, 0.03, 0.5)},
                  hind={"l": (0.04, 0.0, 0.0), "r": (0.03, 0.0, 0.0)},
                  neck=(14, 6), head=12, mane=-44, mane_s=1.45, tail=(-14, -8, -4), root_y=-0.008,
                  embers={"emf_l": 1.0, "emf_r": 0.6})
    settle = pose(t=(0.0, -0.012), p=3, fore={"l": (-0.02, 0.0, 0.0), "r": (-0.01, 0.0, 0.0)},
                  hind={"l": (0.02, 0.0, 0.0), "r": (0.02, 0.0, 0.0)},
                  neck=(10, 4), head=6, mane=-24, mane_s=1.2, tail=(-8, -4, 0), root_y=-0.008,
                  embers={"emf_l": 0.5})
    attack = [lunge, strike, settle, lerp_pose(settle, idle[0], 0.7)]

    hit = [pose(t=(0.01, 0.0), p=-8, fore={"l": (0.0, 0.035, 0.5), "r": (0.01, 0.0, 0.0)},
                neck=(-8, -4), head=-6, mane=6, mane_s=0.8, tail=(14, 10, 6), turn=10),
           pose(t=(0.004, 0.0), p=-3, neck=(-6, -3), head=-4, mane=-2, mane_s=0.9, tail=(4, 4, 2), turn=4)]

    kneel = pose(t=(0.0, -0.20), p=10, fore_fk={"l": (-70, 95, 60), "r": (-66, 92, 60)},
                 hind_fk={"l": (26, -88, -90), "r": (24, -86, -90)},
                 neck=(20, 10), head=16, mane=-4, mane_s=0.6, tail=(10, 6, 4), fire=0.7)
    down = pose(t=(0.0, -0.33), p=4, fore_fk={"l": (-82, 100, 70), "r": (-78, 98, 70)},
                hind_fk={"l": (30, -92, -90), "r": (28, -90, -90)},
                neck=(30, 12), head=20, turn=30, mane=10, mane_s=0.25, tail=(10, 6, 4), tail_side=30, fire=0.35)
    die = [pose(t=(0.01, 0.0), p=-10, fore={"l": (0.0, 0.04, 0.6), "r": (0.0, 0.0, 0.0)},
                neck=(-10, -5), head=-8, mane=10, mane_s=1.2, tail=(20, 10, 10), turn=-10),
           pose(t=(0.0, -0.06), p=6, fore={"l": (-0.01, 0.0, 0.0), "r": (0.0, 0.0, 0.0)},
                neck=(12, 6), head=8, mane=-6, mane_s=1.0, tail=(16, 10, 6), fire=0.9),
           kneel,
           lerp_pose(kneel, down, 0.6),
           down,
           merge(down, {"mane1": {"s": 0.12}, "mane2": {"s": 0.12}, "forelock": {"s": 0.1}, "tail1": {"s": 0.2}})]
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=9, fps={"idle": 6})
