"""Per-frame, per-facing bottom/side extents of one clip (runs inside Blender).

    blender -b art/blender/monsters_c/<id>.blend --python art/src/monsters_c/fitdir.py -- die

Like the MONSTERS_A fit check, but prints every frame of the named clip for the four
facings: the lowest projected row below the pivot (px, + = below; the frame bottom is
frame - pivot_y px away) and the left/right extents, so a lying pose can be balanced
between the facing that sees its front and the one that sees its back.
"""
import math
import sys

import bpy
import numpy as np

PPM = 38.0
EL = math.radians(35.0)
PIVOT = {48: (24, 42), 64: (32, 56), 96: (48, 86)}
DIRS = {"down": 0.0, "left": 270.0, "up": 180.0, "right": 90.0}


def main():
    want = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "die"
    scene = bpy.context.scene
    arm = next(o for o in scene.objects if o.type == "ARMATURE")
    size = int(arm.get("frame", 48))
    px, py = PIVOT[size]
    meshes = [o for o in scene.objects if o.type == "MESH" and "holdout" not in o.name]
    act = bpy.data.actions[want]
    arm.animation_data.action = act
    print(f"[fitdir] {arm.name} {want}: bottom limit {size - 1 - py}px below pivot, width 0..{size - 1}")
    for f in range(1, int(act["frames"]) + 1):
        scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        pts, own = [], []
        for o in meshes:
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            if len(me.vertices):
                co = np.empty(len(me.vertices) * 3, np.float32)
                me.vertices.foreach_get("co", co)
                co = co.reshape(-1, 3)
                M = np.array(ev.matrix_world)
                pts.append(co @ M[:3, :3].T + M[:3, 3])
                own += [o.name] * len(co)
            ev.to_mesh_clear()
        P = np.concatenate(pts)
        own = np.array(own)
        keep = P[:, 2] >= -0.002
        P, own = P[keep], own[keep]
        row = []
        for d, yaw in DIRS.items():
            c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
            x = P[:, 0] * c - P[:, 1] * s
            y = P[:, 0] * s + P[:, 1] * c
            up = P[:, 2] * math.cos(EL) + y * math.sin(EL)
            sx = px + x * PPM
            sy = py - up * PPM
            row.append(f"{d}: low {sy.max() - py + 1.5:+5.1f} ({own[int(sy.argmax())][3:14]}) "
                       f"x {sx.min():5.1f}..{sx.max():5.1f}")
        print(f"[fitdir] f{f}  " + " | ".join(row))


main()
