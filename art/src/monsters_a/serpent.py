"""Vân Xà: the cloud-water serpent of the calculus land (runs inside Blender).

Built upright: a small ground coil carries a tall body that rises in a sine curve (three to
four bends, the calculus motif) to a big horned, whiskered chibi head. Upright because the
35-degree camera draws anything lying on the ground in front of the origin below the
pivot (the kit's QC allows only a few pixels there), while height and sideways sway are
free, so the S can fill the frame. Cloud puffs ride the back of the bends, the tail lifts
off the coil into mist.

Rig: root (coil), tail, ten body bones b1..b10 (one skinned tube), head (kept level), jaw.
The S is posed, not modelled: the body bones are straight up at rest and every pose sets
their sideways tilts from a travelling sine (body_s).
"""
from __future__ import annotations

import math

from mathutils import Vector

from rig import (aim, armature, attach, ball, clip, lerp_pose, material, merge, skin, tube,
                 use_collection)

TAU = 2 * math.pi
N = 10                     # body bones
SEG = 0.070                # body bone length
BASE = Vector((0, -0.03, 0.07))
TOP = BASE + Vector((0, 0, N * SEG))


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def body_s(amp, phase, step=1.2, lean=None, head=(0.0, 0.0)):
    """Pose b1..b10 on a sine curve: absolute sideways tilt of bone k is
    amp * sin(phase - k * step) degrees (+ = top toward +x). lean: optional list of
    per-bone forward tilts (+x rotation, + = toward the facing direction). The head
    cancels the body's sideways tilt so it stays level; head = (pitch, turn) on top."""
    out, prev = {}, 0.0
    for k in range(1, N + 1):
        th = amp * math.sin(phase - k * step)
        rx = lean[k - 1] if lean else 0.0
        out[f"b{k}"] = {"r": (rx, th - prev, 0)}
        prev = th
    out["head"] = {"r": (head[0], -prev, head[1])}
    return out


def build_van_xa():
    use_collection("COL_van_xa")
    water = material("MAT_vx_water", (0.24, 0.37, 0.61), (0.36, 0.21, 0.56), ramp=("blue", "purple"))
    belly = material("MAT_vx_belly", (0.39, 0.53, 0.77), (0.52, 0.34, 0.75), ramp=("blue", "purple"))
    cloud = material("MAT_vx_cloud", (0.81, 0.80, 0.83), (0.60, 0.58, 0.64), ramp="bone")
    horn = material("MAT_vx_horn", (0.90, 0.72, 0.23), (0.90, 0.72, 0.23), ramp="gold", metal=True)
    eye = material("MAT_vx_eye", (1.0, 0.89, 0.48), (1.0, 0.68, 0.23), emit=6.0, glow=("holy", "flame"))
    dot = material("MAT_vx_flow", (0.35, 0.88, 0.96), (0.72, 0.75, 1.0), emit=3.0, glow=("spirit", "thunder"))
    mouth = material("MAT_vx_mouth", (0.11, 0.10, 0.13), (0.11, 0.10, 0.13), ramp="hair")
    fang = material("MAT_vx_fang", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")

    bones = [("root", (0, 0, 0), (0, 0, 0.08), None),
             ("tail", (0.05, 0.06, 0.07), (0.10, 0.14, 0.16), "root")]
    for k in range(1, N + 1):
        h = BASE + Vector((0, 0, (k - 1) * SEG))
        bones.append((f"b{k}", tuple(h), tuple(h + Vector((0, 0, SEG))),
                      "root" if k == 1 else f"b{k - 1}"))
    bones += [("head", tuple(TOP), tuple(TOP + Vector((0, 0, 0.18))), f"b{N}"),
              ("jaw", tuple(TOP + Vector((0, -0.09, 0.03))), tuple(TOP + Vector((0, -0.24, 0.02))), "head")]
    arm = armature("van_xa", bones)

    # ground coil: a small ring of body, open at the front where the body rises
    ring = []
    for k in range(13):
        a = math.radians(-60 + k * 25)            # starts front-left, goes round the back
        ring.append((0.075 * math.sin(a), -0.075 * math.cos(a), 0.06))
    coil = tube("vx_coil", ring, [0.06 - 0.002 * k for k in range(13)], water, seg=12, up=(0, 0, 1))
    att(arm, "root", coil)
    # the tail lifts off the end of the coil and frays into mist
    att(arm, "tail", aim("vx_tail", water, (0.05, 0.06, 0.07), (0.11, 0.15, 0.17), 0.035, 0.012, seg=8),
        ball("vx_mist1", (0.05, 0.05, 0.045), (0.12, 0.16, 0.19), cloud, seg=10, rings=6),
        ball("vx_mist2", (0.035,) * 3, (0.17, 0.17, 0.24), cloud, seg=8, rings=5),
        ball("vx_mist3", (0.022,) * 3, (0.20, 0.19, 0.29), cloud, seg=8, rings=5))

    # the rising body: one tube through the chain, skinned
    pts = [tuple(BASE + Vector((0, 0, -0.02)))]
    rad = [0.066]
    for k in range(1, N + 1):
        pts.append(tuple(BASE + Vector((0, 0, k * SEG))))
        rad.append(0.066 - 0.0022 * k)
    body = tube("vx_body", pts, rad, water, seg=14, up=(0, -1, 0))
    skin(body, arm, [f"b{k}" for k in range(1, N + 1)] + ["root"], power=4)
    # pale belly scales down the front, glowing flow dots, cloud puffs on the back of the
    # bends (alternating sides, so they show from the front as well)
    for k in range(1, N + 1):
        z = BASE.z + (k - 0.5) * SEG
        r = 0.066 - 0.0022 * k
        parts = [ball(f"vx_belly{k}", (r * 0.7, 0.02, SEG * 0.42), (0, BASE.y - r * 0.88, z), belly,
                      seg=10, rings=6)]
        if k % 2 == 0:
            parts.append(ball(f"vx_dot{k}", (0.016,) * 3, (0, BASE.y - r * 1.0, z + 0.02), dot,
                              seg=6, rings=4))
        if k in (2, 4, 6, 8):
            sx = 1 if k % 4 == 2 else -1
            parts.append(ball(f"vx_puff{k}", (0.06, 0.055, 0.05),
                              (sx * r * 0.85, BASE.y + r * 0.6, z + 0.01), cloud, seg=10, rings=6))
        att(arm, f"b{k}", *parts)

    # head: big round chibi dragon-snake head, cloud brows and crest, horns, whiskers
    def H(x, y, z):            # offsets from the top of the neck
        return (TOP.x + x, TOP.y + y, TOP.z + z)
    hd = [ball("vx_head", (0.15, 0.155, 0.12), H(0, -0.07, 0.10), water),
          ball("vx_snout", (0.10, 0.11, 0.065), H(0, -0.195, 0.075), water),
          ball("vx_eyel", (0.036, 0.022, 0.032), H(0.083, -0.172, 0.135), eye, seg=8, rings=5),
          ball("vx_eyer", (0.036, 0.022, 0.032), H(-0.083, -0.172, 0.135), eye, seg=8, rings=5),
          ball("vx_browl", (0.05, 0.045, 0.04), H(0.10, -0.12, 0.185), cloud, seg=10, rings=6),
          ball("vx_browr", (0.05, 0.045, 0.04), H(-0.10, -0.12, 0.185), cloud, seg=10, rings=6),
          ball("vx_crest1", (0.065,) * 3, H(0, 0.0, 0.225), cloud, seg=10, rings=6),
          ball("vx_crest2", (0.05,) * 3, H(0, 0.09, 0.17), cloud, seg=10, rings=6),
          ball("vx_cheekl", (0.045,) * 3, H(0.14, -0.05, 0.06), cloud, seg=10, rings=6),
          ball("vx_cheekr", (0.045,) * 3, H(-0.14, -0.05, 0.06), cloud, seg=10, rings=6),
          aim("vx_hornl", horn, H(0.06, -0.03, 0.20), H(0.13, 0.08, 0.31), 0.03, 0.0, seg=6),
          aim("vx_hornr", horn, H(-0.06, -0.03, 0.20), H(-0.13, 0.08, 0.31), 0.03, 0.0, seg=6),
          aim("vx_whiskl", cloud, H(0.07, -0.25, 0.07), H(0.24, -0.20, -0.04), 0.022, 0.008, seg=6),
          aim("vx_whiskr", cloud, H(-0.07, -0.25, 0.07), H(-0.24, -0.20, -0.04), 0.022, 0.008, seg=6),
          ball("vx_mouth", (0.08, 0.06, 0.012), H(0, -0.20, 0.025), mouth, seg=10, rings=5),
          aim("vx_fangl", fang, H(0.04, -0.255, 0.035), H(0.04, -0.255, 0.0), 0.014, 0.0, seg=5),
          aim("vx_fangr", fang, H(-0.04, -0.255, 0.035), H(-0.04, -0.255, 0.0), 0.014, 0.0, seg=5)]
    att(arm, "head", *hd)
    att(arm, "jaw", ball("vx_jaw", (0.085, 0.10, 0.035), H(-0.0, -0.18, 0.01), belly))

    # --- clips. b-bones stand upright: +x rotation tips them forward, +y sideways (+x).
    idle = [merge(body_s(50, TAU * i / 4), {
        "tail": {"r": (0, 0, 14 * S(i, 4, -1.0))},
        "jaw": {"r": (5 + 4 * S(i, 4, 0.6), 0, 0)}}) for i in range(4)]
    walk = [merge(body_s(54, TAU * i / 6, lean=[3] * N), {
        "root": {"l": (0, 0, 0.008 * abs(S(i, 6)))},
        "tail": {"r": (0, 0, 24 * S(i, 6, -1.0))},
        "jaw": {"r": (5, 0, 0)}}) for i in range(6)]
    # windup: rears up tall and coils back like a drawn bow, mouth wide, tail rattling
    rear = merge(body_s(26, 1.0, lean=[-6, -8, -8, -6, -2, 4, 8, 10, 10, 8], head=(10, 0)), {
        "jaw": {"r": (38, 0, 0)}, "root": {"l": (0, 0.02, 0)}})
    windup = [lerp_pose(idle[0], rear, 0.55), rear,
              merge(rear, {"tail": {"r": (0, 0, 30)}}),
              merge(rear, {"tail": {"r": (0, 0, -30)}})]
    # attack: whip-fast lunge, the body snapping nearly straight toward the target
    strike = merge(body_s(6, 2.0, lean=[8, 4, 3, 2, 2, 1, 1, 1, 0, 0], head=(14, 0)), {
        "jaw": {"r": (46, 0, 0)}, "tail": {"r": (0, 0, -20)}})
    attack = [
        merge(body_s(12, 1.6, lean=[7, 3, 2, 2, 2, 1, 1, 1, 0, 0], head=(-4, 0)), {
            "jaw": {"r": (40, 0, 0)}}),
        strike,
        merge(body_s(20, 2.4, lean=[8, 3, 2, 1, 1, 1, 0, 0, 0, 0]), {
            "jaw": {"r": (8, 0, 0)}, "tail": {"r": (0, 0, 10)}}),
        merge(body_s(36, 2.8, lean=[2, 1, 1, 0, 0, 0, 0, 0, 0, 0]), {"jaw": {"r": (4, 0, 0)}}),
    ]
    hit = [merge(body_s(30, 0.5, lean=[-10, -4, -2, 0, 0, 0, 0, 0, 0, 0], head=(-14, 0)), {
               "jaw": {"r": (28, 0, 0)}, "tail": {"r": (0, 0, 20)}}),
           merge(body_s(38, 0.9, lean=[-4, -1, 0, 0, 0, 0, 0, 0, 0, 0], head=(-4, 0)),
                 {"jaw": {"r": (10, 0, 0)}})]
    # die: sways, sags, and folds down onto its coil in a heap, head resting on top
    curl = {}
    prev = 0.0
    for k in range(1, N + 1):
        th = 72.0 if k % 2 else -72.0
        if k == 1:
            th = 40.0
        curl[f"b{k}"] = {"r": (0, th - prev, 0)}
        prev = th
    curl["head"] = {"r": (-20, -prev + 25, 15)}
    curl["jaw"] = {"r": (10, 0, 0)}
    die = [merge(body_s(44, 0.4, lean=[-8, -4, 0, 0, 0, 0, 0, 0, 0, 0]), {"jaw": {"r": (40, 0, 0)}}),
           merge(body_s(54, 1.2), {"jaw": {"r": (24, 0, 0)}}),
           lerp_pose(body_s(54, 1.2), curl, 0.5),
           curl,
           merge(curl, {"tail": {"r": (0, 0, 20)}, "jaw": {"r": (4, 0, 0)}}),
           merge(curl, {"tail": {"r": (0, 0, 24)}, "jaw": {"r": (2, 0, 0)}})]
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 10, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 14, False, hit=1)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    arm.animation_data.action = None
    return arm
