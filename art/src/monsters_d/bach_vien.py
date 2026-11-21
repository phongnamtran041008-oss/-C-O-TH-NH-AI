"""Bạch Viên (elite, 64): the great white ape of the maze forest.

A heavy knuckle-walker: a huge chest and shoulder hump leaning forward over short bent legs,
long arms coming down to the knuckles, the head carried low in front of the shoulders. White
fur, grey skin on the face, chest, hands and feet. The face is old and wise: a heavy brow
with long white eyebrows that sweep back, a white beard, small gold eyes, and a scar across
its right eye. A string of dark prayer beads hangs round its neck.

Rig: root, pelvis (legs hang from it), chest (arms, head), head, jaw; arms and legs are
two-bone limbs posed by the planar IK of common.py (elbows point back, knees forward), with
hands and feet kept flat on the ground. Clips: idle breathes and looks about; walk is a
four-beat knuckle-walk (left hand, right foot, right hand, left foot); windup rears up on the
hind legs with both fists raised high overhead and the mouth open in a roar; attack brings
both fists down in a ground slam in front (hit frame 1); die sinks to the haunches and topples
forward onto its chest.
"""
from __future__ import annotations

import math

from common import C, Limb, S, att, posed, rest_table, six
from quadrupeds import gait
from rig import aim, armature, ball, box, lerp_pose, material, merge, shadow, shadow_material, use_collection

SC = 1.45                       # the whole ape is built at 1/SC and scaled up
PELVIS_H = (0.15, 0.40)         # (y, z) head of the pelvis bone
CHEST_H = (0.0, 0.58)

# A gorilla's lines: high shoulders and a hump, the back sloping down to a low rump, the
# head slung forward in front of the shoulders, long arms reaching down ahead of the legs.
BONES = [
    ("root", (0, 0, 0), (0, 0, 0.1), None),
    ("pelvis", (0, 0.15, 0.40), (0, 0.0, 0.58), "root"),
    ("chest", (0, 0.0, 0.58), (0, -0.12, 0.74), "pelvis"),
    ("head", (0, -0.16, 0.68), (0, -0.20, 0.84), "chest"),
    ("jaw", (0, -0.26, 0.68), (0, -0.33, 0.66), "head"),
]
for _s, _x in (("l", 1), ("r", -1)):
    BONES += [
        (f"ua_{_s}", (_x * 0.21, -0.08, 0.68), (_x * 0.23, -0.035, 0.40), "chest"),
        (f"fa_{_s}", (_x * 0.23, -0.035, 0.40), (_x * 0.10, -0.10, 0.12), f"ua_{_s}"),
        (f"hand_{_s}", (_x * 0.10, -0.10, 0.12), (_x * 0.10, -0.105, 0.03), f"fa_{_s}"),
        (f"th_{_s}", (_x * 0.10, 0.15, 0.38), (_x * 0.12, 0.06, 0.22), "pelvis"),
        (f"sh_{_s}", (_x * 0.12, 0.06, 0.22), (_x * 0.105, 0.11, 0.07), f"th_{_s}"),
        (f"ft_{_s}", (_x * 0.105, 0.11, 0.07), (_x * 0.105, 0.02, 0.03), f"sh_{_s}"),
    ]
REST = rest_table(BONES)


def build():
    use_collection("COL_bach_vien")
    fur = material("MAT_bv_fur", (0.60, 0.58, 0.64), (0.27, 0.24, 0.30), ramp=("bone", "hair"))
    # the limbs carry their own (same-coloured) material so the kit draws an inner line
    # where an arm crosses the body
    limb = material("MAT_bv_fur_limb", (0.60, 0.58, 0.64), (0.27, 0.24, 0.30), ramp=("bone", "hair"))
    fur_sh = material("MAT_bv_fur_shade", (0.62, 0.60, 0.66), (0.18, 0.16, 0.20), ramp=("bone", "hair"))
    skin = material("MAT_bv_skin", (0.37, 0.39, 0.44), (0.58, 0.19, 0.16), ramp=("stone", "red"))
    skin_lt = material("MAT_bv_skin_light", (0.53, 0.56, 0.60), (0.78, 0.33, 0.23), ramp=("stone", "red"))
    brow = material("MAT_bv_brow", (0.97, 0.96, 0.97), (0.40, 0.36, 0.43), ramp=("bone", "hair"))
    eye = material("MAT_bv_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=5.0, glow=("holy", "flame"))
    scar = material("MAT_bv_scar", (0.36, 0.10, 0.11), (0.93, 0.87, 0.70), ramp=("red", "paper"))
    mouth = material("MAT_bv_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    bead = material("MAT_bv_bead", (0.34, 0.20, 0.13), (0.90, 0.72, 0.23), ramp=("wood", "gold"))
    jade = material("MAT_bv_jade", (0.31, 0.65, 0.47), (0.58, 0.19, 0.16), ramp=("jade", "red"))

    arm = armature("bach_vien", BONES)

    # ---- trunk: low rump, belly, deep chest, the shoulder hump, a bare grey chest
    att(arm, "pelvis", ball("bv_rump", (0.15, 0.14, 0.12), (0, 0.13, 0.42), fur),
        ball("bv_belly", (0.13, 0.12, 0.11), (0, 0.04, 0.49), fur_sh))
    att(arm, "chest", ball("bv_chest", (0.19, 0.17, 0.17), (0, -0.05, 0.61), fur),
        ball("bv_hump", (0.17, 0.15, 0.10), (0, 0.0, 0.74), fur),
        ball("bv_pec", (0.115, 0.05, 0.10), (0, -0.20, 0.57), skin),
        *[ball(f"bv_shag{k}", (0.06, 0.06, 0.045), (x, 0.08, z), fur_sh, seg=8, rings=5)
          for k, (x, z) in enumerate(((0.11, 0.68), (-0.11, 0.68), (0.0, 0.78)))])
    beads = []
    for k in range(11):
        a = math.tau * k / 11 - math.pi / 2
        p = (0.13 * math.cos(a), -0.17 + 0.08 * math.sin(a), 0.645 + 0.05 * math.sin(a))
        beads.append(ball(f"bv_bead{k}", (0.026,) * 3, p, jade if k == 0 else bead, seg=8, rings=5))
    att(arm, "chest", *beads)

    # ---- head: slung forward; big grey face, white brows sweeping back, white beard,
    # small gold eyes deep under the brow, a scar across its right eye
    HY, HZ = -0.22, 0.72
    att(arm, "head",
        ball("bv_skull", (0.11, 0.10, 0.10), (0, HY, HZ), fur),
        ball("bv_crest", (0.075, 0.08, 0.06), (0, HY + 0.04, HZ + 0.075), fur, seg=10, rings=6),
        ball("bv_face", (0.09, 0.06, 0.085), (0, HY - 0.08, HZ - 0.01), skin, seg=12, rings=8),
        ball("bv_muzzle", (0.065, 0.05, 0.048), (0, HY - 0.125, HZ - 0.055), skin_lt, seg=10, rings=6),
        box("bv_brow", (0.16, 0.045, 0.032), (0, HY - 0.115, HZ + 0.04), brow, bevel=0.01),
        aim("bv_browl", brow, (0.06, HY - 0.11, HZ + 0.045), (0.17, HY - 0.05, HZ + 0.02), 0.024, 0.0, seg=5),
        aim("bv_browr", brow, (-0.06, HY - 0.11, HZ + 0.045), (-0.17, HY - 0.05, HZ + 0.02), 0.024, 0.0, seg=5),
        ball("bv_eyel", (0.024, 0.012, 0.019), (0.037, HY - 0.125, HZ + 0.012), eye, seg=8, rings=5),
        ball("bv_eyer", (0.024, 0.012, 0.019), (-0.037, HY - 0.125, HZ + 0.012), eye, seg=8, rings=5),
        box("bv_scar", (0.013, 0.012, 0.09), (-0.04, HY - 0.13, HZ + 0.012), scar, rot=(0, 28, 0)),
        box("bv_nostril", (0.036, 0.012, 0.01), (0, HY - 0.155, HZ - 0.04), mouth),
        ball("bv_earl", (0.025, 0.03, 0.035), (0.11, HY, HZ), skin, seg=8, rings=5),
        ball("bv_earr", (0.025, 0.03, 0.035), (-0.11, HY, HZ), skin, seg=8, rings=5),
        ball("bv_cheekl", (0.05, 0.05, 0.06), (0.09, HY - 0.05, HZ - 0.04), brow, seg=8, rings=5),
        ball("bv_cheekr", (0.05, 0.05, 0.06), (-0.09, HY - 0.05, HZ - 0.04), brow, seg=8, rings=5))
    att(arm, "jaw", ball("bv_jaw", (0.055, 0.045, 0.03), (0, HY - 0.095, HZ - 0.09), skin, seg=10, rings=6),
        box("bv_mouth", (0.065, 0.012, 0.012), (0, HY - 0.15, HZ - 0.08), mouth),
        aim("bv_beard", brow, (0, HY - 0.10, HZ - 0.10), (0, HY - 0.12, HZ - 0.22), 0.05, 0.0, seg=8),
        aim("bv_beardl", brow, (0.04, HY - 0.08, HZ - 0.09), (0.06, HY - 0.08, HZ - 0.18), 0.032, 0.0, seg=6),
        aim("bv_beardr", brow, (-0.04, HY - 0.08, HZ - 0.09), (-0.06, HY - 0.08, HZ - 0.18), 0.032, 0.0, seg=6))

    # ---- limbs (massive forearms, knuckles on the ground)
    for s, x in (("l", 1), ("r", -1)):
        b = {n: arm.data.bones[f"{n}_{s}"] for n in ("ua", "fa", "hand", "th", "sh", "ft")}
        h, t = b["ua"].head_local, b["ua"].tail_local
        att(arm, f"ua_{s}", aim(f"bv_ua{s}", limb, tuple(h), tuple(t), 0.085, 0.068, seg=10, smooth=True),
            ball(f"bv_delt{s}", (0.085, 0.09, 0.09), tuple(h), limb, seg=10, rings=6),
            aim(f"bv_elbtuft{s}", fur_sh, tuple(t), (x * 0.24, 0.05, 0.43), 0.04, 0.0, seg=6))
        h, t = b["fa"].head_local, b["fa"].tail_local
        att(arm, f"fa_{s}", aim(f"bv_fa{s}", limb, tuple(h), tuple(t), 0.078, 0.056, seg=10, smooth=True),
            ball(f"bv_wristfur{s}", (0.055, 0.055, 0.05), (x * 0.11, -0.095, 0.16), fur_sh, seg=8, rings=5))
        att(arm, f"hand_{s}", ball(f"bv_fist{s}", (0.048, 0.055, 0.052), (x * 0.10, -0.105, 0.055), skin, seg=10, rings=6),
            box(f"bv_knuck{s}", (0.06, 0.035, 0.028), (x * 0.10, -0.125, 0.028), skin_lt, bevel=0.01))
        h, t = b["th"].head_local, b["th"].tail_local
        att(arm, f"th_{s}", aim(f"bv_th{s}", limb, tuple(h), tuple(t), 0.08, 0.06, seg=10, smooth=True))
        h, t = b["sh"].head_local, b["sh"].tail_local
        att(arm, f"sh_{s}", aim(f"bv_sh{s}", limb, tuple(h), tuple(t), 0.06, 0.045, seg=10, smooth=True))
        att(arm, f"ft_{s}", box(f"bv_foot{s}", (0.07, 0.12, 0.04), (x * 0.105, 0.075, 0.02), skin, bevel=0.015))


    # a flat contact shadow under the footprint: grounds the heavy body and keeps the middle
    # of the lowest rows on the pivot while a hand or foot is lifted
    shadow("bv_shadow", 0.155, 0.14, shadow_material("MAT_bv_shadow"), arm)
    clips(arm)
    arm.scale = (SC, SC, SC)
    # a footprint wider than the ground band: slide away from the camera per facing
    arm["shift_down"] = 0.09
    arm["shift_up"] = 0.09
    arm["shift_side"] = 0.11
    return arm


# ------------------------------------------------------------------ animation
ARMS = {s: Limb((f"ua_{s}", f"fa_{s}", f"hand_{s}"), REST, bend=+1) for s in "lr"}
LEGS = {s: Limb((f"th_{s}", f"sh_{s}", f"ft_{s}"), REST, bend=-1) for s in "lr"}


def body(t=(0.0, 0.0), p=0.0, c=0.0, hands=None, feet=None, arms_fk=None, head=(0, 0, 0), jaw=0.0,
         roll=0.0, twist=0.0):
    """One pose. t: pelvis shift (y, z); p: pelvis pitch (+ = leans further forward);
    c: chest pitch on top. hands / feet: {side: (dy, lift)} offsets of planted knuckles and
    feet from rest; arms_fk: {side: (upper, lower)} absolute changes of angle instead of IK."""
    hands, feet = hands or {}, feet or {}
    out = {"pelvis": {"l": (0, t[0], t[1]), "r": (p, roll, 0)},
           "chest": {"r": (c, 0, twist)},
           "head": {"r": (head[0] - p - c, head[1], head[2] - twist)},
           "jaw": {"r": (jaw, 0, 0)}}
    for s in "lr":
        hip = posed(LEGS[s].hip, PELVIS_H, t, p)
        dy, lift = feet.get(s, (0.0, 0.0))
        e = LEGS[s].end
        out.update(LEGS[s].solve(hip, (e[0] + dy, e[1] + lift), p, foot_world=-20 * lift / 0.05))
        sh = posed(posed(ARMS[s].hip, CHEST_H, (0, 0), c), PELVIS_H, t, p)
        if arms_fk and s in arms_fk:
            out.update(ARMS[s].fk(*arms_fk[s], parent_delta=p + c))
        else:
            dy, lift = hands.get(s, (0.0, 0.0))
            e = ARMS[s].end
            out.update(ARMS[s].solve(sh, (e[0] + dy, e[1] + lift), p + c, foot_world=10 * lift / 0.05))
    return out


def clips(arm):
    idle = []
    for i in range(4):
        b = 0.006 * (0.5 - 0.5 * C(i, 4))
        idle.append(body(t=(0, -b), c=-1.5 * S(i, 4), head=(2 * S(i, 4, 0.8), 0, (0, 12, 12, 0)[i]),
                         jaw=(0, 0, 6, 0)[i]))

    walk = []
    s_arm, s_leg, lift = 0.035, 0.03, 0.05
    for i in range(6):
        ph = i / 6
        hands, feet = {}, {}
        for side, off in (("l", 0.0), ("r", 0.5)):
            hands[side] = gait(ph + off, s_arm, lift)
        for side, off in (("r", 0.25), ("l", 0.75)):
            feet[side] = gait(ph + off, s_leg, lift * 0.7)
        bob = 0.012 * abs(S(i, 3))
        walk.append(body(t=(0, -bob), p=2 * S(i, 6), c=0, hands=hands, feet=feet,
                         roll=3 * S(i, 6), twist=6 * S(i, 6), head=(0, 0, 0), jaw=0))

    # windup: rears up on its hind legs, both fists raised high overhead, roaring
    crouch = body(t=(0.0, -0.03), p=6, c=4, hands={"l": (0.02, 0), "r": (0.02, 0)}, jaw=10)
    rear = body(t=(0.04, -0.08), p=-8, c=-6, arms_fk={"l": (-100, -200), "r": (-100, -200)},
                head=(-14, 0, 0), jaw=34)
    windup = [crouch, rear,
              merge(rear, body(t=(0.04, -0.085), p=-9, c=-7, arms_fk={"l": (-104, -204), "r": (-96, -196)},
                               head=(-16, 0, 4), jaw=38)),
              merge(rear, body(t=(0.04, -0.08), p=-8, c=-6, arms_fk={"l": (-96, -196), "r": (-104, -204)},
                               head=(-15, 0, -4), jaw=36))]
    # attack: the double-fist ground slam just in front of it
    swing = body(t=(0.02, -0.04), p=-4, c=4, arms_fk={"l": (-62, -168), "r": (-62, -168)}, head=(-6, 0, 0), jaw=24)
    slam = body(t=(-0.01, -0.06), p=14, c=10, hands={"l": (-0.025, 0.0), "r": (-0.025, 0.0)}, head=(10, 0, 0), jaw=30)
    shake = body(t=(-0.01, -0.055), p=13, c=9, hands={"l": (-0.025, 0.0), "r": (-0.025, 0.0)}, head=(6, 0, 0), jaw=12)
    recover = lerp_pose(slam, idle[0], 0.7)
    attack = [swing, slam, shake, recover]

    hit = [body(t=(0.03, -0.01), p=-12, c=-6, hands={"l": (0.03, 0.03), "r": (0.03, 0.02)}, head=(-20, 0, 12), jaw=20),
           body(t=(0.01, -0.005), p=-4, c=-2, hands={"l": (0.01, 0.0), "r": (0.01, 0.0)}, head=(-6, 0, 4), jaw=6)]

    sit = body(t=(0.03, -0.17), p=-6, c=6, hands={"l": (0.04, 0.0), "r": (0.04, 0.0)}, head=(10, 0, 10), jaw=10)
    slump = body(t=(0.06, -0.19), p=8, c=6, arms_fk={"l": (2, 10), "r": (4, 12)}, head=(0, 0, 50), jaw=14)
    die = [body(t=(0.03, -0.01), p=-14, c=-8, hands={"l": (0.03, 0.03), "r": (0.03, 0.03)}, head=(-26, 0, 0), jaw=34),
           sit,
           lerp_pose(sit, slump, 0.45),
           slump,
           merge(slump, {"head": {"r": (-30, 0, 46)}}),
           merge(slump, {"head": {"r": (-30, 0, 48)}, "jaw": {"r": (4, 0, 0)}})]
    six(arm, idle, walk, windup, attack, hit, die, walk_fps=9, fps={"idle": 5})
