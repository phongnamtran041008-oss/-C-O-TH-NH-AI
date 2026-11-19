"""Thiên Kiếp Lôi Long: the tribulation thunder dragon (boss 96). Runs inside Blender.

A thick eastern dragon boiling up out of a dark storm cloud. Eighteen skinned body bones:
two rise out of the cloud, twelve throw one full upright loop (seen face-on as a big ring,
so it reads as a coiling dragon, not a pole), four rise to a big head with a long snout,
open jaw and teeth, antler horns, a flowing white mane and long whiskers. Bright
violet-white lightning fins run down the spine; two arms with big gold claws. The cloud
is violet-grey billows on a flat underside, with lightning flickering inside and small
bolts dropping from it.

Seven clips: the monster six plus `special` (rears to the full frame height, roars at the
sky and calls a lightning strike down onto its horns; events.hit = 4).
"""
from __future__ import annotations

import math

from mathutils import Vector

from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material, merge,
                 prism, place, skin, tube, use_collection)

TAU = 2 * math.pi
N = 20
SEG = 0.15
BASE = Vector((0, 0.02, 0.34))
RISE, LOOP = 4, 10                       # bones before the loop, bones in the loop
LEAN = -20.0                             # the rise leans left so the ring sits central
NECK_STRAIGHTEN = (5, 10, 15, 20, 20, 20)
HS = 1.45                                # head scale


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def radius(k):
    """Body radius at bone k (0 = base): thick in the coil, tapering to the neck."""
    return 0.215 - 0.0048 * k


def body(loop=1.0, wave=0.0, phase=0.0, neck=(0, 0, 0, 0, 0, 0), lift=0.0, head=(0.0, 0.0), jaw=8.0,
         helix=3.0):
    """Body pose. The loop bones turn their sideways heading through 360 * loop degrees
    (a full upright ring at 1.0); `wave` adds a travelling ripple; `helix` tips the loop
    forward a little per bone so the body passes in front of itself where the ring
    closes; `neck` = forward tilts of the last four bones; `lift` = backward lean of the
    rising base (rearing). The head cancels the accumulated tilts and looks ahead."""
    out, prev_y, pitch = {}, 0.0, 0.0
    for k in range(1, N + 1):
        if k <= RISE:
            th, rx = LEAN, -lift
        elif k <= RISE + LOOP:
            u = (k - RISE) / LOOP
            th, rx = LEAN + 360.0 * loop * u, helix
        else:
            j = k - RISE - LOOP - 1
            th, rx = LEAN + 360.0 * loop + NECK_STRAIGHTEN[j], neck[j]
        th += wave * math.sin(phase - k * 0.7)
        out[f"d{k}"] = {"r": (rx, th - prev_y, 0)}
        prev_y = th
        pitch += rx
    out["head"] = {"r": (-pitch + head[0], -prev_y, head[1])}
    out["jaw"] = {"r": (jaw, 0, 0)}
    return out


def build_loi_long():
    use_collection("COL_loi_long")
    scale = material("MAT_ll_scale", (0.24, 0.37, 0.61), (0.58, 0.19, 0.16), ramp=("blue", "red"))
    scale_dk = material("MAT_ll_scale_dark", (0.14, 0.23, 0.42), (0.36, 0.10, 0.11), ramp=("blue", "red"))
    belly = material("MAT_ll_belly", (0.93, 0.87, 0.70), (0.90, 0.72, 0.23), ramp=("paper", "gold"))
    horn = material("MAT_ll_horn", (0.90, 0.72, 0.23), (0.27, 0.24, 0.30), ramp=("gold", "hair"), metal=True)
    mane = material("MAT_ll_mane", (0.81, 0.80, 0.83), (0.11, 0.10, 0.13), ramp=("bone", "hair"))
    cloud = material("MAT_ll_cloud", (0.27, 0.24, 0.30), (0.18, 0.16, 0.20), ramp="hair")
    cloud_lt = material("MAT_ll_cloud_light", (0.36, 0.21, 0.56), (0.36, 0.10, 0.11), ramp=("purple", "red"))
    cloud_dk = material("MAT_ll_cloud_dark", (0.18, 0.16, 0.20), (0.11, 0.10, 0.13), ramp="hair")
    spark = material("MAT_ll_spark", (0.97, 0.97, 1.0), (1.0, 0.89, 0.48), emit=5.0, glow=("thunder", "flame"))
    flick = material("MAT_ll_flicker", (0.72, 0.75, 1.0), (1.0, 0.68, 0.23), emit=3.0, glow=("thunder", "flame"))
    flick["kit_halo"] = 1
    bolt = material("MAT_ll_bolt", (0.97, 0.97, 1.0), (1.0, 0.89, 0.48), emit=8.0, glow=("thunder", "flame"))
    bolt["kit_halo"] = 2
    eye = material("MAT_ll_eye", (1.0, 0.89, 0.48), (0.78, 0.55, 1.0), emit=6.0, glow=("holy", "cosmic"))
    tooth = material("MAT_ll_tooth", (0.81, 0.80, 0.83), (0.81, 0.80, 0.83), ramp="bone")
    dark = material("MAT_ll_mouth", (0.36, 0.10, 0.11), (0.11, 0.10, 0.13), ramp=("red", "hair"))

    top = BASE + Vector((0, 0, N * SEG))
    neck_bone = f"d{RISE + LOOP + 1}"
    shoulder_z = BASE.z + (RISE + LOOP + 0.6) * SEG
    bones = [("root", (0, 0, 0), (0, 0, 0.1), None),
             ("cloud", (0, 0, 0.05), (0, 0, 0.30), "root"),
             ("flick_a", (0, 0, 0.12), (0, 0, 0.2), "cloud"),
             ("flick_b", (0, 0, 0.12), (0, 0, 0.2), "cloud"),
             ]
    for k in range(1, N + 1):
        h = BASE + Vector((0, 0, (k - 1) * SEG))
        bones.append((f"d{k}", tuple(h), tuple(h + Vector((0, 0, SEG))), "cloud" if k == 1 else f"d{k - 1}"))
    bones += [("head", tuple(top), tuple(top + Vector((0, 0, 0.3))), f"d{N}"),
              ("bolt", tuple(top + Vector((0, 0.1, 0.6))), tuple(top + Vector((0, 0.1, 0.8))), "head"),
              ("jaw", tuple(top + Vector((0, -0.10 * HS, 0.03 * HS))), tuple(top + Vector((0, -0.42 * HS, 0.0))), "head"),
              ("whisk_l", tuple(top + Vector((0.08, -0.36, 0.08)) * HS), tuple(top + Vector((0.32, -0.22, -0.08)) * HS), "head"),
              ("whisk_r", tuple(top + Vector((-0.08, -0.36, 0.08)) * HS), tuple(top + Vector((-0.32, -0.22, -0.08)) * HS), "head"),
              ("arm_l", (0.14, BASE.y - 0.1, shoulder_z), (0.30, BASE.y - 0.26, shoulder_z - 0.16), neck_bone),
              ("arm_r", (-0.14, BASE.y - 0.1, shoulder_z), (-0.30, BASE.y - 0.26, shoulder_z - 0.16), neck_bone),
              ("aura", (0, 0.1, 1.2), (0, 0.1, 1.4), "cloud")]
    arm = armature("loi_long", bones)

    # --- the storm cloud: a flat dark underside, violet-grey billows heaped above it
    cp = [cone("ll_cloudbase", 0.26, 0.40, 0.10, (0, 0.03, 0.13), cloud_dk, seg=16)]
    billows = [((0, 0.06, 0.34), 0.30, cloud), ((0.32, 0.08, 0.30), 0.22, cloud_lt), ((-0.32, 0.08, 0.30), 0.22, cloud_lt),
               ((0.18, -0.16, 0.26), 0.19, cloud), ((-0.18, -0.16, 0.26), 0.19, cloud), ((0.0, 0.30, 0.30), 0.21, cloud_lt),
               ((0.24, 0.26, 0.42), 0.17, cloud), ((-0.24, 0.27, 0.44), 0.16, cloud), ((0.38, -0.02, 0.26), 0.13, cloud_dk),
               ((-0.38, -0.02, 0.26), 0.13, cloud_dk), ((0.0, -0.22, 0.20), 0.15, cloud_lt)]
    for k, (c, r, m) in enumerate(billows):
        cp.append(ball(f"ll_billow{k}", (r, r * 0.9, r * 0.7), c, m, seg=14, rings=8))
    att(arm, "cloud", *cp)
    zig = [(0.0, 0.0), (0.035, -0.05), (-0.02, -0.09), (0.03, -0.14)]

    def zigzag(name, x0, y0, z0, sx, mat, n=3, step=1.0):
        parts, pts = [], [(x0 + sx * dx * step, y0, z0 + dz * step) for dx, dz in zig[:n + 1]]
        for j in range(len(pts) - 1):
            parts.append(aim(f"{name}{j}", mat, pts[j], pts[j + 1], 0.016, 0.016, seg=4))
        return parts
    # inner flickers on the billows and small bolts dropping from the underside; two sets
    # that blink alternately
    fa = (zigzag("ll_fla", 0.20, -0.30, 0.36, 1, flick) + zigzag("ll_flb", -0.30, -0.12, 0.40, -1, flick)
          + zigzag("ll_drop_a", 0.33, -0.10, 0.18, 1, bolt, n=3, step=0.75))
    fb = (zigzag("ll_flc", -0.12, -0.32, 0.30, -1, flick) + zigzag("ll_fld", 0.36, 0.0, 0.42, 1, flick)
          + zigzag("ll_drop_b", -0.33, -0.08, 0.18, -1, bolt, n=3, step=0.75))
    att(arm, "flick_a", *fa)
    att(arm, "flick_b", *fb)

    # --- the body: one thick skinned tube from inside the cloud up to the neck
    pts = [tuple(BASE + Vector((0, 0, -0.12)))]
    rad = [radius(0)]
    for k in range(1, N + 1):
        pts.append(tuple(BASE + Vector((0, 0, k * SEG))))
        rad.append(radius(k))
    tb = tube("ll_body", pts, rad, scale, seg=18, up=(0, -1, 0))
    skin(tb, arm, [f"d{k}" for k in range(1, N + 1)] + ["cloud"], power=4)
    for k in range(1, N + 1):
        z = BASE.z + (k - 0.5) * SEG
        r = radius(k)
        parts = [ball(f"ll_belly{k}", (r * 0.5, 0.04, SEG * 0.42), (0, BASE.y - r * 0.9, z), belly, seg=10, rings=6)]
        M = place((0, 0.45, 1.0), (0, BASE.y + r * 0.88, z - SEG * 0.35))
        parts.append(prism(f"ll_fin{k}", [(-0.05, 0.0), (0.05, 0.0), (0.016, 0.09), (0.055, 0.105),
                                          (0.0, 0.22), (-0.016, 0.12), (-0.055, 0.115)], 0.03, spark, matrix=M))
        if k % 3 == 0:
            parts.append(ball(f"ll_band{k}", (r * 1.03, r * 1.03, 0.028), (0, BASE.y, z + SEG * 0.3), scale_dk, seg=16, rings=4))
        if k > RISE + LOOP:      # the mane flows down the back of the neck
            parts.append(ball(f"ll_neckmane{k}", (0.10, 0.09, 0.12), (0, BASE.y + r * 0.95, z), mane, seg=10, rings=6))
        att(arm, f"d{k}", *parts)

    # --- head: long snout, open jaw with teeth, antler horns, mane, whiskers
    def H(x, y, z):
        return (top.x + x * HS, top.y + y * HS, top.z + z * HS)
    hd = [ball("ll_skull", (0.17 * HS, 0.18 * HS, 0.15 * HS), H(0, -0.05, 0.12), scale),
          box("ll_snout", (0.17 * HS, 0.30 * HS, 0.10 * HS), H(0, -0.29, 0.11), scale, bevel=0.05),
          ball("ll_nose", (0.09 * HS, 0.05 * HS, 0.055 * HS), H(0, -0.44, 0.15), scale_dk, seg=10, rings=6),
          box("ll_brow", (0.27 * HS, 0.08 * HS, 0.05 * HS), H(0, -0.15, 0.21), scale_dk, bevel=0.03),
          ball("ll_eyel", (0.05 * HS, 0.03 * HS, 0.032 * HS), H(0.09, -0.19, 0.17), eye, seg=8, rings=5),
          ball("ll_eyer", (0.05 * HS, 0.03 * HS, 0.032 * HS), H(-0.09, -0.19, 0.17), eye, seg=8, rings=5),
          box("ll_mouth", (0.15 * HS, 0.24 * HS, 0.025 * HS), H(0, -0.31, 0.055), dark)]
    for k, x in enumerate((0.06, 0.025, -0.025, -0.06)):
        hd.append(aim(f"ll_tooth{k}", tooth, H(x, -0.40 + abs(x) * 0.5, 0.065), H(x, -0.40 + abs(x) * 0.5, 0.0), 0.02 * HS, 0.0, seg=5))
    for s in (1, -1):
        hd += [aim(f"ll_horn{s}", horn, H(s * 0.07, -0.02, 0.22), H(s * 0.19, 0.18, 0.46), 0.04 * HS, 0.014 * HS, seg=6),
               aim(f"ll_tine{s}", horn, H(s * 0.13, 0.07, 0.33), H(s * 0.28, 0.04, 0.42), 0.024 * HS, 0.0, seg=5),
               aim(f"ll_tine2{s}", horn, H(s * 0.165, 0.14, 0.41), H(s * 0.19, 0.30, 0.52), 0.02 * HS, 0.0, seg=5),
               aim(f"ll_tine3{s}", horn, H(s * 0.10, 0.03, 0.27), H(s * 0.20, -0.06, 0.34), 0.018 * HS, 0.0, seg=5)]
    for k, (x, y, z, r) in enumerate(((0, 0.10, 0.20, 0.10), (0.12, 0.08, 0.08, 0.08), (-0.12, 0.08, 0.08, 0.08),
                                      (0, 0.17, 0.05, 0.09), (0.09, 0.14, 0.26, 0.07), (-0.09, 0.14, 0.26, 0.07),
                                      (0.15, 0.16, 0.0, 0.07), (-0.15, 0.16, 0.0, 0.07))):
        hd.append(ball(f"ll_mane{k}", (r * HS, r * HS, r * 0.9 * HS), H(x, y, z), mane, seg=10, rings=6))
    att(arm, "head", *hd)
    att(arm, "jaw", box("ll_jaw", (0.15 * HS, 0.26 * HS, 0.05 * HS), H(0, -0.26, 0.02), belly, bevel=0.025),
        *[aim(f"ll_ltooth{k}", tooth, H(x, -0.36, 0.04), H(x, -0.36, 0.085), 0.017 * HS, 0.0, seg=5)
          for k, x in enumerate((0.045, -0.045))])
    for s, b in ((1, "whisk_l"), (-1, "whisk_r")):
        att(arm, b, aim(f"ll_{b}1", mane, H(s * 0.08, -0.36, 0.08), H(s * 0.24, -0.30, 0.0), 0.024 * HS, 0.018 * HS, seg=6),
            aim(f"ll_{b}2", mane, H(s * 0.24, -0.30, 0.0), H(s * 0.38, -0.12, -0.14), 0.018 * HS, 0.006, seg=6))
    for s, b in ((1, "arm_l"), (-1, "arm_r")):
        sh = Vector((s * 0.14, BASE.y - 0.1, shoulder_z))
        hand = Vector((s * 0.30, BASE.y - 0.26, shoulder_z - 0.16))
        att(arm, b, aim(f"ll_{b}", scale, tuple(sh), tuple(hand), 0.07, 0.055, seg=8),
            ball(f"ll_{b}palm", (0.06,) * 3, tuple(hand), scale_dk, seg=8, rings=5),
            *[aim(f"ll_{b}claw{k}", horn, tuple(hand + Vector((s * 0.035 * (k - 1), -0.03, 0))),
                  tuple(hand + Vector((s * 0.06 * (k - 1), -0.13, -0.07))), 0.024, 0.0, seg=5) for k in range(3)])
    # lightning crackling round the body (windup / special) and the bolt from the sky
    aura = []
    for k in range(5):
        a = TAU * k / 5 + 0.3
        c = Vector((0.48 * math.cos(a), 0.12 + 0.18 * math.sin(a), 0.75 + 0.4 * (k % 2)))
        prev = c
        for j in range(3):
            nxt = prev + Vector((0.06 * (-1) ** j, 0.0, 0.16))
            aura.append(aim(f"ll_arc{k}{j}", bolt, tuple(prev), tuple(nxt), 0.018, 0.018, seg=4))
            prev = nxt
    att(arm, "aura", *aura)
    bz = [(0, 0.94), (0.07, 0.86), (-0.03, 0.78), (0.06, 0.70), (-0.02, 0.62), (0.02, 0.54)]
    att(arm, "bolt", *[aim(f"ll_bolt{j}", bolt, H(bz[j][0], 0.07, bz[j][1]), H(bz[j + 1][0], 0.07, bz[j + 1][1]),
                           0.035, 0.035, seg=5) for j in range(len(bz) - 1)])

    def fx(i, aura=0.0, bolt_s=0.0):
        on = i % 2 == 0
        return {"aura": {"s": aura}, "bolt": {"s": bolt_s, "r": (46, 0, 0)},   # bolt kept vertical while the head rears back
               
                "flick_a": {"s": 1.0 if on else 0.0}, "flick_b": {"s": 0.0 if on else 1.0}}

    def wh(i, n, a=10):
        return {"whisk_l": {"r": (0, 0, a * math.sin(TAU * i / n))}, "whisk_r": {"r": (0, 0, -a * math.sin(TAU * i / n))}}
    NECK = (4, 6, 8, 8, 6, 2)
    idle = [merge(merge(body(wave=6, phase=TAU * i / 4, neck=NECK), wh(i, 4)),
                  merge(fx(i), {"cloud": {"l": (0, 0, 0.012 * math.sin(TAU * i / 4))},
                                "arm_l": {"r": (8 * math.sin(TAU * i / 4), 0, 0)},
                                "arm_r": {"r": (-8 * math.sin(TAU * i / 4), 0, 0)}})) for i in range(4)]
    walk = [merge(merge(body(wave=10, phase=TAU * i / 6, neck=(5, 7, 9, 9, 6, 2)), wh(i, 6, 16)),
                  merge(fx(i), {"cloud": {"r": (0, 0, 5 * math.sin(TAU * i / 6)),
                                          "l": (0, 0, 0.015 * abs(math.sin(TAU * i / 6)))}})) for i in range(6)]
    # windup: rears to the full frame height, loop drawn tight, head thrown back, jaw wide,
    # arms spread, lightning crackling all round
    rear = merge(merge(body(loop=1.0, helix=1.0, neck=(-3, -4, -4, -3, -2, 0), lift=3, head=(-12, 0), jaw=36),
                       {"arm_l": {"r": (-50, -30, 0)}, "arm_r": {"r": (-50, 30, 0)},
                        "whisk_l": {"r": (0, 0, 28)}, "whisk_r": {"r": (0, 0, -28)}}),
                 merge(fx(0, aura=1.0), {"cloud": {"s": 1.04}}))
    windup = [merge(lerp_pose(idle[0], rear, 0.5), fx(1, 0.5)), rear,
              merge(rear, merge(fx(1, 1.05), {"aura": {"r": (0, 0, 20)}})), merge(rear, fx(2, 1.0))]
    # attack: the head lunges down and forward in a crackling bite
    strike = merge(body(neck=(10, 16, 20, 20, 14, 8), helix=4, head=(24, 0), jaw=44),
                   merge(fx(1), {"arm_l": {"r": (-60, 0, 0)}, "arm_r": {"r": (-60, 0, 0)},
                                 "whisk_l": {"r": (0, 0, 32)}, "whisk_r": {"r": (0, 0, -32)}}))
    attack = [merge(body(neck=(8, 12, 14, 14, 10, 6), head=(10, 0), jaw=38), fx(0)), strike,
              merge(body(neck=(6, 10, 10, 10, 8, 4), head=(6, 0), jaw=10), fx(0)),
              merge(body(wave=6, phase=1.0, neck=NECK), fx(1))]
    hit = [merge(body(wave=12, phase=0.5, neck=(-2, -4, -4, 0, 0, 0), head=(-20, 10), jaw=30), fx(0)),
           merge(body(wave=8, phase=0.9, neck=(2, 4, 6, 6, 4, 2), head=(-6, 4), jaw=12), fx(1))]
    # die: the loop sags, the body slumps down onto the cloud, head resting on the heap
    slump = body(loop=0.95, helix=2, neck=(-12, -16, -16, -12, -6, 0), lift=6, head=(40, 25), jaw=14)
    slump = merge(slump, merge(fx(0), {"cloud": {"s": 0.9, "l": (0, 0, -0.04)}, "flick_a": {"s": 0.0},
                                       "arm_l": {"r": (30, 0, 0)}, "arm_r": {"r": (30, 0, 0)}}))
    for k in range(1, RISE + 1):
        slump[f"d{k}"]["l"] = (0, 0, -0.05)
    die = [merge(body(wave=14, phase=0.4, neck=(-4, -4, -4, -2, 0, 0), head=(-26, 0), jaw=44), fx(0)),
           merge(body(wave=16, phase=1.2, neck=(8, 10, 12, 10, 8, 4), head=(10, 10), jaw=24), fx(1)),
           lerp_pose(merge(body(neck=NECK), fx(0)), slump, 0.5),
           slump, merge(slump, {"cloud": {"s": 0.85, "l": (0, 0, -0.05)}}),
           merge(slump, {"cloud": {"s": 0.85, "l": (0, 0, -0.05)}})]
    # special: rears to the full frame height, roars at the sky, the bolt strikes its horns
    sky = body(loop=1.0, helix=0.0, neck=(-2, -3, -3, -3, -2, 0), lift=3, head=(-18, 0), jaw=42)
    up_arms = {"arm_l": {"r": (-120, -25, 0)}, "arm_r": {"r": (-120, 25, 0)}}
    special = [
        merge(lerp_pose(idle[0], rear, 0.5), fx(0)),
        merge(rear, fx(1, 0.6)),
        merge(merge(sky, up_arms), fx(0, 1.0)),
        merge(merge(sky, up_arms), fx(1, 1.05, 0.6)),
        merge(merge(sky, up_arms), merge(fx(0, 1.12, 0.88), {"aura": {"r": (0, 0, 25)}})),
        merge(merge(sky, up_arms), merge(fx(1, 1.08, 1.0), {"aura": {"r": (0, 0, -20)}, "bolt": {"s": 0.88, "r": (46, 0, 10)}})),
        merge(lerp_pose(sky, idle[0], 0.4), fx(0, 0.6)),
        merge(lerp_pose(sky, idle[0], 0.85), fx(1)),
    ]
    arm.scale = (0.86, 0.86, 0.86)     # fills ~80 % of the 96 px frame, rearing to its top
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 8, True)
    clip(arm, "windup", windup, 8, False)
    clip(arm, "attack", attack, 12, False, hit=1)
    clip(arm, "hit", hit, 12, False)
    clip(arm, "die", die, 10, False)
    clip(arm, "special", special, 10, False, hit=4)
    arm.animation_data.action = None
    return arm
