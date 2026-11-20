"""Shared helpers for BEASTS_B (runs inside Blender).

The solids, armature, skinning and clip helpers come from art/src/monsters_a (rig.py,
beasts.py, quadrupeds.py), imported read-only through sys.path: other batches build on them
at the same time, so nothing there is edited. What had to change is copied here:

* `quad_clips` / `extra_quad_clips`: the quadruped clip generator of monsters_a with a
  `deco(clip, i, n, pose)` hook, so a beast can add its own bones (nine tails, ear flicks,
  a butt wiggle) to every generated pose.
* `hexc`: palette colours by hex, so a base colour sits exactly on the ramp entry it means.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MON = HERE.parent / "monsters_a"
for p in (str(HERE), str(MON)):
    if p not in sys.path:
        sys.path.insert(0, p)

from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material,  # noqa: E402,F401
                 merge, place, prism, set_root_offset, shadow_material, skin, tube,
                 use_collection)
from beasts import cute_eyes, eye_mats  # noqa: E402,F401
from quadrupeds import Legs, gait, quad_armature  # noqa: E402,F401

TAU = 2 * math.pi


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def hexc(h: str):
    h = h.lstrip("#")
    return tuple(int(h[k:k + 2], 16) / 255.0 for k in (0, 2, 4))


def mat(name, hx, ramp, **kw):
    """A one-look material on palette colour `hx`, pinned to `ramp`."""
    c = hexc(hx)
    return material(name, c, c, ramp=ramp, **kw)


def set_ramp(m, ramp):
    """Pin a material's palette ramp (survives rig.apply_variant, which re-applies ramp_base)."""
    m["ramp_base"] = m["ramp_di"] = ramp
    m["kit_ramp"] = ramp


def glow(name, hx, ramp, strength=3.0, halo=None):
    c = hexc(hx)
    m = material(name, c, c, emit=strength, glow=ramp)
    if halo is not None:
        m["kit_halo"] = halo
    return m


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def eyes_bone(hy, hz, parent="head"):
    return ("eyes", (0, hy, hz - 0.03), (0, hy, hz + 0.05), parent)


def finish(arm, clips: dict, scale=1.0, hit_frame=1, walk_fps=10):
    """Key the eight beast clips (contract: idle 6 fps loop, walk, windup 8, attack 14 with
    events.hit, hit 12, die 10, happy 8 loop, sleep 4 loop)."""
    arm.scale = (scale,) * 3
    spec = (("idle", 6, True), ("walk", walk_fps, True), ("windup", 8, False), ("attack", 14, False),
            ("hit", 12, False), ("die", 10, False), ("happy", 8, True), ("sleep", 4, True))
    for name, fps, loop in spec:
        clip(arm, name, clips[name], fps, loop, hit=hit_frame if name == "attack" else None)
    arm.animation_data.action = None


# ------------------------------------------------------------------ quadruped clips
def quad_poses(P, A):
    """The quadruped clip poses of monsters_a/quadrupeds.quad_clips (idle 4, walk 6, windup
    4, attack 4, hit 2, die 6), returned as lists instead of keyed, so a beast can decorate
    them. A: stride, lift, hop, crouch, drop, lunge."""
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
        legs, lifts = {}, {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(ph + off, s, lift)
        bob = 0.012 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]), lift=lifts)
        p.update({
            "pelvis": {"l": (0, 0, bob), "r": (0, 3 * S(i, 6), 0)},
            "chest": {"r": (0, -4 * S(i, 6), 0)},
            "head": {"r": (4 * abs(S(i, 6)) - 2, 0, -5 * S(i, 6))},
            "jaw": {"r": (4, 0, 0)},
            "tail1": {"r": (-8, 0, 16 * S(i, 6, 0.8))},
            "tail2": {"r": (-6, 0, 22 * S(i, 6, -0.3))},
        })
        walk.append(p)
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
    return {"idle": idle, "walk": walk, "windup": windup, "attack": attack, "hit": hit, "die": die}


def quad_extra_poses(P, drop, tail_wrap=70.0, head_rest=(18, 0, 55)):
    """happy (hop and quarter-turn spin) and sleep (curled, breathing), as in
    monsters_a/beasts.extra_quad_clips, returned as lists."""
    L = Legs(P)
    happy = []
    for i, (z, tuck) in enumerate(((0.0, 0.0), (0.05, 1.0), (0.07, 1.0), (0.02, 0.4))):
        p = L.plant(drop=0.02) if tuck == 0 else L.air((-30 * tuck, 50 * tuck), (-30 * tuck, 50 * tuck),
                                                        (30 * tuck, -40 * tuck), (30 * tuck, -40 * tuck))
        p.update({"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)},
                  "pelvis": {"l": (0, 0, -0.02 if tuck == 0 else 0.0)},
                  "head": {"r": (-14, 0, 8 * S(i, 4))}, "jaw": {"r": (22, 0, 0)},
                  "eyes": {"s": (1, 0.35, 1)},
                  "tail1": {"r": (30, 0, 30 * S(i, 4))}, "tail2": {"r": (20, 0, 40 * S(i, 4, -1))}})
        happy.append(p)
    curl = L.plant(drop=drop, front=(-0.02, -0.02), back=(0.03, 0.03), pitch=4)
    sleep = []
    for i in range(4):
        b = 0.006 * S(i, 4)
        p = dict(curl)
        p.update({"pelvis": {"l": (0, 0, -drop + b)}, "chest": {"r": (4, 0, 0), "s": 1.0 + 0.02 * S(i, 4)},
                  "head": {"r": head_rest, "l": (0, 0.02, -0.05)}, "jaw": {"r": (0, 0, 0)},
                  "eyes": {"s": (1, 0.12, 1)},
                  "tail1": {"r": (-12, 0, tail_wrap)}, "tail2": {"r": (-6, 0, tail_wrap * 0.8)}})
        sleep.append(p)
    return {"happy": happy, "sleep": sleep}
