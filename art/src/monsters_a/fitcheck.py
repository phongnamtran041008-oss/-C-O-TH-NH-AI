"""Does every frame of every clip fit the sprite frame? (runs inside Blender)

    blender -b art/blender/monsters/<id>.blend --python art/src/monsters_a/fitcheck.py

Projects every deformed vertex through the kit's ground camera (35 degrees, 38 px per
metre, frame/pivot of the creature's size class) for the four facings and prints the worst
overhang per clip. Run before rendering so a lunge that leaves the frame is caught in the
pose tables, not after a render.
"""
import math

import bpy
import numpy as np

PPM = 38.0
EL = math.radians(35.0)
PIVOT = {48: (24, 42), 64: (32, 56), 96: (48, 86)}
DIRS = {"down": 0.0, "left": 270.0, "up": 180.0, "right": 90.0}
MARGIN = 1  # px kept free for the outline
# kit qc: in these clips the lowest drawn row must sit within max(4, h/12) px of the pivot
STEADY_Y = ("idle", "walk", "hit", "windup", "attack")      # not die / special


def main():
    scene = bpy.context.scene
    arm = next(o for o in scene.objects if o.type == "ARMATURE")
    size = int(arm.get("frame", 48))
    px, py = arm.get("pivot", PIVOT[size])
    foot = max(4.0, size / 12)
    meshes = [o for o in scene.objects if o.type == "MESH" and "holdout" not in o.name]
    worst_all = 0.0
    for act in sorted(bpy.data.actions, key=lambda a: a.name):
        arm.animation_data.action = act
        n = int(act["frames"])
        worst = (0.0, "")
        sink = (0.0, "")
        span = [1e9, -1e9, 1e9, -1e9]
        for f in range(1, n + 1):
            scene.frame_set(f)
            dg = bpy.context.evaluated_depsgraph_get()
            pts, owner = [], []
            for o in meshes:
                ev = o.evaluated_get(dg)
                me = ev.to_mesh()
                if len(me.vertices):
                    co = np.empty(len(me.vertices) * 3, np.float32)
                    me.vertices.foreach_get("co", co)
                    co = co.reshape(-1, 3)
                    M = np.array(ev.matrix_world)
                    co = co @ M[:3, :3].T + M[:3, 3]
                    pts.append(co)
                    owner += [o.name] * len(co)
                ev.to_mesh_clear()
            P = np.concatenate(pts)
            owner = np.array(owner)
            keep = P[:, 2] >= -0.002          # below ground is cut by the holdout
            P, owner = P[keep], owner[keep]
            if act.name == "idle" and f == 1:
                g = P[P[:, 2] < 0.06]
                if len(g):
                    print(f"[fit] {arm.name} footprint x {g[:, 0].min():+.3f}..{g[:, 0].max():+.3f}"
                          f"  y {g[:, 1].min():+.3f}..{g[:, 1].max():+.3f}  centre "
                          f"({(g[:, 0].min() + g[:, 0].max()) / 2:+.3f}, "
                          f"{(g[:, 1].min() + g[:, 1].max()) / 2:+.3f})")
            for d, yaw in DIRS.items():
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
                # +1.6: the outline under the silhouette plus the block rounding of the 6x
                # downscale (calibrated against the kit's own QC on real renders)
                low = sy.max() + 1.6 - py
                if act.name in STEADY_Y and abs(low) > foot - 0.2 and abs(low) > abs(sink[0]):
                    sink = (low, f"frame {f} {d} {owner[int(sy.argmax())]}")
        worst_all = max(worst_all, worst[0], abs(sink[0]))
        flag = "OVER" if worst[0] > 0 else ("SINK" if sink[0] else "ok  ")
        print(f"[fit] {arm.name} {act.name:7s} {flag} {worst[0]:5.1f}px {worst[1]:16s} "
              f"x {span[0]:5.1f}..{span[1]:5.1f}  y {span[2]:5.1f}..{span[3]:5.1f}"
              + (f"  lowest {sink[0]:+.1f}px {sink[1]}" if sink[0] else ""))
    print(f"[fit] {arm.name} worst overhang {worst_all:.1f}px (frame {size}, pivot {px},{py})")


main()
