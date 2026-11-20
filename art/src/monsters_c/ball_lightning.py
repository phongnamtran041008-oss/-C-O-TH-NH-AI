"""Lôi Linh: a ball-lightning sprite (Lôi Kiếp Đài, normal 48, hovers).

Runs inside Blender. A glowing core with a face - two dark slanted eyes and a fanged grin
- bristling with short crackling spikes, three broken rings of zigzag lightning orbiting it
on different tilts with sparks at their ends, and a trail of sparks when it moves. Drawn
hovering above its ground pivot with a small contact shadow.

Rings spin about their own tilted axes (quaternion poses); the core jitters by a fixed
pseudo-random sequence, so every build gives the same frames. A `discharge` bone carries
the bolts it fires; `trail` the sparks it leaves; both exist only in their clips.

Clips: idle (rings orbit, the core jitters), walk (zips along, rings spinning faster,
sparks trailing), windup (charges: swells, rings pulled in tight and fast, spikes standing
long, eyes narrowed - held), attack (discharges: bolts lash forward to the ground and the
rings blow outward = hit), hit (squashed, rings scattered), die (flickers, shrinks and pops
into a last spark on the ground).
"""
from __future__ import annotations

import math

from mathutils import Euler, Quaternion, Vector

from common import (hx, C, S, aim, armature, att, ball, bolt, hover_shadow, material, merge,
                    plate, use_collection, write_clips, zigzag)

TINY = 0.001
CC = Vector((0, 0, 0.56))
RINGS = {"orb1": (22, 0, 0), "orb2": (-62, 0, -30)}
JIT = [(0.0, 0.0, 0.0), (0.012, -0.004, 0.008), (-0.01, 0.006, -0.006), (0.006, 0.0, 0.012),
       (-0.008, -0.006, 0.004), (0.01, 0.004, -0.01), (-0.004, 0.008, 0.006), (0.008, -0.008, -0.004)]


def _normal(tilt):
    return Euler([math.radians(a) for a in tilt], "XYZ").to_matrix() @ Vector((0, 0, 1))


def build_loi_linh():
    use_collection("COL_loi_linh")
    core = material("MAT_ll_core", hx("#3c5e9c"), hx("#b9821a"), ramp=("blue", "gold"), metal=True)
    core["kit_light"] = 0.55
    inner = material("MAT_ll_core_spark", (0.72, 0.75, 1.0), (1.0, 0.89, 0.48), emit=4.0, glow=("thunder", "holy"))
    inner["kit_halo"] = 0
    arc = material("MAT_ll_bolt", (0.72, 0.75, 1.0), (1.0, 0.89, 0.48), emit=5.0, glow=("thunder", "holy"))
    spark = material("MAT_ll_spark", (0.89, 0.95, 1.0), (1.0, 0.97, 0.80), emit=6.0, glow=("ice", "holy"))
    spark["kit_halo"] = 0
    # the face is the hottest spark on the ball: white-hot eyes and grin
    dark = material("MAT_ll_eye", (0.97, 0.97, 1.0), (1.0, 0.98, 0.89), emit=9.0, glow=("ice", "holy"))
    dark["kit_halo"] = 0
    mouth = material("MAT_ll_mouth", (0.97, 0.97, 1.0), (1.0, 0.98, 0.89), emit=9.0, glow=("ice", "holy"))
    mouth["kit_halo"] = 0
    fang = material("MAT_ll_fang", hx("#cfcbd3"), hx("#cfcbd3"), ramp="bone")
    fang["kit_priority"] = 2.5

    bones = [("root", (0, 0, 0), (0, 0, 0.1), None),
             ("hover", (0, 0, 0.46), (0, 0, 0.56), "root"),
             ("core", tuple(CC), tuple(CC + Vector((0, 0, 0.12))), "hover"),
             ("face", (0, -0.15, 0.56), (0, -0.15, 0.62), "core"),
             ("spikes", tuple(CC), tuple(CC + Vector((0, 0, 0.1))), "core"),
             ("discharge", tuple(CC), tuple(CC + Vector((0, -0.1, 0))), "hover"),
             ("trail", (0, 0.12, 0.56), (0, 0.22, 0.56), "hover")]
    for name, tilt in RINGS.items():
        n = _normal(tilt)
        bones.append((name, tuple(CC), tuple(CC + n * 0.1), "hover"))
    arm = armature("loi_linh", bones)

    # --- the core and its face
    att(arm, "core", ball("ll_core", (0.15, 0.15, 0.15), tuple(CC), core, seg=16, rings=10),
        *bolt("ll_crack_a", zigzag((0.07, -0.07, 0.69), (0.14, 0.02, 0.50), 3, 0.02, seed=1), 0.012, inner),
        *bolt("ll_crack_b", zigzag((-0.08, -0.06, 0.68), (-0.14, 0.03, 0.51), 3, 0.02, seed=2), 0.012, inner))
    # the face: white-hot slanted eyes and a grin, each set in a dark socket so they read
    sock = material("MAT_ll_socket", hx("#1d1922"), hx("#5c1a1c"), ramp=("hair", "red"))
    fc = []
    for sx in (-1, 1):
        pts = [(x * sx, z) for x, z in ((-0.036, -0.016), (0.04, -0.012), (0.04, 0.03), (-0.036, 0.008))]
        big = [(x * 1.45, z * 1.45 + 0.002) for x, z in pts]
        fc.append(plate(f"ll_sock{sx}", big, sock, (sx * 0.055, -0.140, 0.59), (1, 0.4 * sx, 0), (0, 0, 1),
                        thick=0.02))
        fc.append(plate(f"ll_eye{sx}", pts, dark, (sx * 0.055, -0.150, 0.59), (1, 0.4 * sx, 0), (0, 0, 1),
                        thick=0.02))
    grin = [(-0.06, 0.004), (0.06, 0.004), (0.045, -0.028), (0.0, -0.04), (-0.045, -0.028)]
    fc.append(plate("ll_msock", [(x * 1.35, z * 1.4 + 0.004) for x, z in grin], sock, (0, -0.143, 0.53),
                    (1, 0, 0), (0, 0, 1), thick=0.02))
    fc.append(plate("ll_mouth", grin, mouth, (0, -0.152, 0.53), (1, 0, 0), (0, 0, 1), thick=0.02))
    att(arm, "face", *fc)
    # --- short crackling spikes standing off the surface
    sp = []
    for k, (th, ph) in enumerate(((0, 70), (60, 40), (130, 75), (200, 35), (260, 70), (320, 30), (95, 110),
                                  (230, 115), (20, 130))):
        d = Vector((math.cos(math.radians(th)) * math.sin(math.radians(ph)),
                    math.sin(math.radians(th)) * math.sin(math.radians(ph)), math.cos(math.radians(ph))))
        if d.y < -0.55 and d.z < 0.6:
            continue                       # keep the face clear
        a = CC + d * 0.14
        sp += bolt(f"ll_spike{k}_", zigzag(tuple(a), tuple(CC + d * 0.24), 2, 0.018, seed=k), 0.013, arc)
    att(arm, "spikes", *sp)
    # --- three broken rings of zigzag lightning (two opposite arcs each, so a half turn
    # brings a ring back to the same look and the loops close), a spark at each end
    for r, (name, tilt) in enumerate(RINGS.items()):
        M = Euler([math.radians(a) for a in tilt], "XYZ").to_matrix()
        parts = []
        for half in (0, 1):
            pts = []
            n = 8
            for k in range(n + 1):
                ang = math.radians(180 * half + 30 * r + 115 * k / n)
                rr = 0.30 + (0.02 if k % 2 else -0.016)
                pts.append(tuple(CC + M @ Vector((rr * math.cos(ang), rr * math.sin(ang), 0))))
            parts += bolt(f"ll_ring{r}{half}_", pts, 0.012, arc)
            parts.append(ball(f"ll_rspark{r}{half}", (0.025,) * 3, pts[-1], spark, seg=8, rings=5))
        att(arm, name, *parts)
    # --- the discharge: three bolts lashing forward and down to the ground ahead
    ds = []
    for k, (end, s) in enumerate((((0.0, -0.13, 0.03), (1, 0, 0)), ((0.12, -0.42, 0.36), (0, 0, 1)),
                                  ((-0.11, -0.40, 0.30), (0, 0, 1)))):
        ds += bolt(f"ll_dis{k}_", zigzag(tuple(CC + Vector((0, -0.1, -0.02))), end, 5, 0.03, seed=k, side=s),
                   0.015, arc)
        ds.append(ball(f"ll_dspark{k}", (0.03,) * 3, end, spark, seg=8, rings=5))
    att(arm, "discharge", *ds)
    # --- sparks left behind when it moves
    att(arm, "trail", ball("ll_trail1", (0.035,) * 3, (0, 0.20, 0.57), spark, seg=8, rings=5),
        ball("ll_trail2", (0.026,) * 3, (0.03, 0.28, 0.54), spark, seg=8, rings=5),
        ball("ll_trail3", (0.02,) * 3, (-0.02, 0.35, 0.58), spark, seg=8, rings=5))
    hover_shadow("ll_shadow", 0.10, 0.08, arm)
    _clips(arm)
    return arm


def spin(name, deg, s=1.0):
    q = Quaternion(_normal(RINGS[name]), math.radians(deg))
    return {"q": tuple(q), "s": s}


def rings(a1, a2, a3=0.0, s=1.0):
    return {"orb1": spin("orb1", a1, s), "orb2": spin("orb2", a2, s)}


def _clips(arm):
    off = {"discharge": {"s": TINY}, "trail": {"s": TINY}}

    def j(i, k=1.0):
        x, y, z = JIT[i % len(JIT)]
        return (x * k, y * k, z * k)

    # loops close on themselves: per-ring steps chosen so n steps make whole turns
    idle = [merge(off, merge(rings(45 * i, -45 * i, 45 * i),
                             {"hover": {"l": (0, 0, 0.02 * S(i, 4))}, "core": {"l": j(i)},
                              "spikes": {"r": (0, 0, 90 * i)}}))
            for i in range(4)]
    walk = [merge({"discharge": {"s": TINY}, "trail": {"s": 1.0, "l": (0, 0.0, 0.02 * S(i, 6, 1.0))}},
                  merge(rings(30 * i, -30 * i, 30 * i),
                        {"hover": {"l": (0, 0, 0.025 * S(i, 6))}, "core": {"l": j(i + 2, 1.3), "r": (12, 0, 0)},
                         "spikes": {"r": (0, 0, 60 * i)}}))
            for i in range(6)]

    # windup: charges - swells, rings drawn in tight and spinning hard, spikes standing
    # long, eyes narrowed - held while the hit zone fills
    def charge(i):
        return merge(off, merge(rings(80 * i, -100 * i, 70 * i, s=0.72),
                                {"hover": {"l": (0, 0.03, 0.03)}, "core": {"s": 1.18, "l": j(i + 1, 1.6)},
                                 "spikes": {"s": 1.45, "r": (0, 0, 50 * i)}, "face": {"s": (1.1, 0.7, 1.0)}}))
    windup = [merge(off, merge(rings(20, -30, 15, s=0.88), {"core": {"s": 1.08}, "spikes": {"s": 1.2}})),
              charge(1), charge(2), charge(3)]

    # attack: compresses (f0), discharges - bolts lashing forward to the ground, rings blown
    # outward (f1 = hit), the bolts flicker on (f2), it recovers (f3)
    attack = [merge(off, merge(rings(40, -60, 30, s=0.6), {"core": {"s": 0.88}, "spikes": {"s": 0.7},
                                                         "hover": {"l": (0, 0.02, 0.02)}})),
              merge({"trail": {"s": TINY}, "discharge": {"s": 1.0}},
                    merge(rings(100, -120, 90, s=1.45), {"core": {"s": 1.12, "l": (0, -0.03, 0)}, "spikes": {"s": 1.5},
                                                        "face": {"s": (1.1, 1.25, 1.0)},
                                                        "hover": {"l": (0, -0.03, 0.0)}})),
              merge({"trail": {"s": TINY}, "discharge": {"s": 0.85, "r": (0, 0, 8)}},
                    merge(rings(130, -150, 120, s=1.25), {"core": {"s": 1.04, "l": j(5)}, "spikes": {"s": 1.2},
                                                         "hover": {"l": (0, -0.02, 0.0)}})),
              merge(off, merge(rings(160, -180, 150, s=1.05), {"core": {"l": j(3)}}))]

    hit = [merge(off, merge(rings(-30, 40, -50, s=1.3), {"hover": {"l": (0, 0.05, 0.03)},
                                                        "core": {"s": (1.2, 1.2, 0.78)}, "face": {"s": (1.0, 0.4, 1.0)},
                                                        "spikes": {"s": 0.6}})),
           merge(off, merge(rings(-15, 20, -25, s=1.1), {"hover": {"l": (0, 0.02, 0.01)}, "core": {"s": (0.94, 0.94, 1.08)}}))]

    die = [merge(off, merge(rings(40, -40, 40, s=1.3), {"core": {"s": 1.2, "l": j(1, 2)}, "spikes": {"s": 1.6},
                                                       "face": {"s": (1.1, 1.3, 1.0)}})),
           merge(off, merge(rings(90, -80, 70, s=1.3), {"core": {"s": 0.8, "l": j(4, 2)}, "spikes": {"s": 0.8},
                                                       "face": {"s": (1.0, 0.3, 1.0)}, "hover": {"l": (0, 0, -0.08)}})),
           merge(off, merge(rings(120, -110, 100, s=1.2), {"core": {"s": 0.5, "l": j(6, 2)}, "spikes": {"s": 0.5},
                                                          "face": {"s": (1.0, 0.2, 1.0)}, "hover": {"l": (0, 0, -0.2)}})),
           merge(off, merge(rings(150, -140, 130, s=0.4), {"core": {"s": 0.28}, "spikes": {"s": 0.3},
                                                          "face": {"s": TINY}, "hover": {"l": (0, 0, -0.34)}})),
           merge(off, merge(rings(170, -160, 150, s=TINY), {"core": {"s": 0.14}, "spikes": {"s": TINY},
                                                           "face": {"s": TINY}, "hover": {"l": (0, 0, -0.42)}})),
           merge(off, merge(rings(180, -170, 160, s=TINY), {"core": {"s": 0.08}, "spikes": {"s": TINY},
                                                           "face": {"s": TINY}, "hover": {"l": (0, 0, -0.46)}}))]
    write_clips(arm, idle, walk, windup, attack, hit, die, hit_frame=1)
