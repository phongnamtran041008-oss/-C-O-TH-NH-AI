"""Does every frame of every clip fit the sprite frame? (runs inside Blender)

    blender -b art/blender/monsters_d/<id>.blend --python art/src/monsters_d/fitcheck.py

A copy of art/src/monsters_a/fitcheck.py that also honours the per-facing slide of the
big elites (`shift_down` / `shift_up` / `shift_side` on the armature, see scene.py) and
prints, per clip, the lowest row against the pivot for every facing (lo/hi in px).
Projects every deformed vertex through the kit's ground camera (35 degrees, 38 px per
metre) for the four facings and prints the worst overhang and the lowest row per clip.
"""
import math

import bpy
import numpy as np

PPM = 38.0
EL = math.radians(35.0)
PIVOT = {48: (24, 42), 64: (32, 56), 96: (48, 86)}
DIRS = {"down": 0.0, "left": 270.0, "up": 180.0, "right": 90.0}
MARGIN = 1
STEADY_Y = ("idle", "walk", "hit", "windup", "attack")


def main():
    scene = bpy.context.scene
    arm = next(o for o in scene.objects if o.type == "ARMATURE")
    size = int(arm.get("frame", 48))
    px, py = PIVOT[size]
    foot = max(4.0, size / 12)
    def away(d, clip_name):
        key = "side" if d in ("left", "right") else d
        v = float(arm.get(f"shift_{key}_{clip_name}", arm.get(f"shift_{key}", 0.0)))
        return {"down": (0.0, v), "up": (0.0, -v), "right": (v, 0.0), "left": (-v, 0.0)}[d]
    meshes = [o for o in scene.objects if o.type == "MESH" and "holdout" not in o.name]
    worst_all = 0.0
    for act in sorted(bpy.data.actions, key=lambda a: a.name):
        arm.animation_data.action = act
        n = int(act["frames"])
        worst = (0.0, "")
        sink = (0.0, "")
        span = [1e9, -1e9, 1e9, -1e9]
        lows = {d: [] for d in DIRS}
        for f in range(1, n + 1):
            scene.frame_set(f)
            dg = bpy.context.evaluated_depsgraph_get()
            pts = []
            names = []
            for o in meshes:
                ev = o.evaluated_get(dg)
                me = ev.to_mesh()
                if len(me.vertices):
                    co = np.empty(len(me.vertices) * 3, np.float32)
                    me.vertices.foreach_get("co", co)
                    co = co.reshape(-1, 3)
                    M = np.array(ev.matrix_world)
                    pts.append(co @ M[:3, :3].T + M[:3, 3])
                    names += [o.name] * len(co)
                ev.to_mesh_clear()
            P0 = np.concatenate(pts)
            names = np.array(names)
            keep = P0[:, 2] >= -0.002
            P0, names = P0[keep], names[keep]
            for d, yaw in DIRS.items():
                P = P0.copy()
                ox, oy = away(d, act.name)
                P[:, 0] += ox
                P[:, 1] += oy
                c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
                x = P[:, 0] * c - P[:, 1] * s
                y = P[:, 0] * s + P[:, 1] * c
                up = P[:, 2] * math.cos(EL) + y * math.sin(EL)
                sx = px + x * PPM
                sy = py - up * PPM
                span = [min(span[0], sx.min()), max(span[1], sx.max()),
                        min(span[2], sy.min()), max(span[3], sy.max())]
                over = max(MARGIN - sx.min(), sx.max() - (size - MARGIN),
                           MARGIN - sy.min(), sy.max() + 0.8 - (size - MARGIN), 0.0)
                if over > worst[0]:
                    worst = (over, f"frame {f} {d}")
                low = sy.max() + 1.6 - py
                lows[d].append(low)
                if act.name in STEADY_Y and abs(low) > foot - 0.2 and abs(low) > abs(sink[0]):
                    sink = (low, f"frame {f} {d} {names[int(sy.argmax())]}")
        worst_all = max(worst_all, worst[0], abs(sink[0]))
        flag = "OVER" if worst[0] > 0 else ("SINK" if sink[0] else "ok  ")
        print(f"[fit] {arm.name} {act.name:7s} {flag} {worst[0]:5.1f}px {worst[1]:16s} "
              f"x {span[0]:5.1f}..{span[1]:5.1f}  y {span[2]:5.1f}..{span[3]:5.1f}"
              + (f"  lowest {sink[0]:+.1f}px {sink[1]}" if sink[0] else ""))
        print("[fit]      " + "  ".join(f"{d} {min(v):+.1f}..{max(v):+.1f}" for d, v in lows.items()))
    print(f"[fit] {arm.name} worst {worst_all:.1f}px (frame {size}, pivot {px},{py})")


main()
