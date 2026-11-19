"""Village buildings: build every model by script, save the .blend, render fixed-size frames through the kit and pack
client/assets/v2/props/buildings.png/.json. Frames of one animated prop sit side by side, frame 0 first (rect = frame 0).

    sys.argv[1:]: optional "--only name,name" (sprite names such as house, stall, portal)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy
import numpy as np

import kit.api as kit
from kit import pack
from kit.api import _pal, _render_frames, out_path
from kit.scene import Cam, Staging, expand, prepare_materials, setup_render

import wt_common as C

C.KIT = True
import wt_village as V

ARGS = sys.argv[1:]
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None
OUT = "client/assets/v2/props"


def names_for(name, variants):
    return [name] if variants == 1 else [f"{name}_{v}" for v in range(variants)]


def build_one(builder, variant, frame):
    C._MATS.clear()                       # fresh materials: the kit rewrites them in memory when it renders
    col = C.collection(f"b{len(bpy.data.collections)}")
    builder(col, variant, frame)
    return col


def main():
    kit.clear_scene()
    # 1. the .blend (frame 0 of every variant), saved before anything is rendered
    keep = []
    for name, wh, builder, variants, frames, solid, vi in V.BUILDINGS:
        for v, nm in enumerate(names_for(name, variants)):
            C._MATS.clear()
            col = C.collection(nm)
            builder(col, v, 0)
            keep.append(col)
    if ONLY is None:
        kit.save_blend("art/blender/world_tiles/village.blend")
    for c in keep:
        for ob in list(c.objects):
            bpy.data.objects.remove(ob)
        bpy.data.collections.remove(c)
    pal = _pal(None)
    scene = setup_render()
    packed = []
    notes = []
    for name, (W, H), builder, variants, frames, solid, vi in V.BUILDINGS:
        if ONLY and name not in ONLY:
            continue
        for v, nm in enumerate(names_for(name, variants)):
            imgs = []
            for f in range(frames):
                V.CUR[:] = [W, H]
                col = build_one(builder, v, f)
                objs = expand(col)
                cam = Cam("ground", W, H, V.PPM, (W / 2, H - 5))
                with Staging(scene, objs) as st:
                    cam.apply(scene)
                    mats = prepare_materials(objs, cam)
                    img = _render_frames(scene, st, cam, mats, pal, None, {}, [lambda: None])[0]
                imgs.append(img)
                a = img[..., 3] > 0
                edges = [a[0].any(), a[:, 0].any(), a[:, -1].any()]
                ys, xs = np.nonzero(a)
                notes.append(f"{nm}[{f}] {W}x{H} bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}" + ("  TOUCHES EDGE" if any(edges) else ""))
                for ob in list(col.objects):
                    bpy.data.objects.remove(ob)
                bpy.data.collections.remove(col)
            sol = None
            if solid:
                sol = [int(W / 2 + solid[0]), int(H + solid[1]), int(solid[2]), int(solid[3])]
            packed.append({"name": nm, "frames": imgs, "pivot": (W // 2, H), "solid": sol, "vi": vi})
    for n in notes:
        kit.log(n)
    if not packed:
        return
    doc = pack.pack_props(out_path(OUT), "buildings", [{k: v for k, v in p.items() if k != "vi"} for p in packed])
    jp = out_path(OUT) / "buildings.json"
    d = json.loads(jp.read_text("utf-8"))
    for p in packed:
        d["props"][p["name"]]["name_vi"] = p["vi"]
    d["id"] = "buildings"
    d["note"] = ("each rect is exactly 2x the old code-drawn sprite; pivot = bottom-centre of the rect; animated props lay "
                 "their frames side by side: frame i is at rect.x + i * rect.w; solid = [x, y, w, h] relative to the rect")
    jp.write_text(json.dumps(d, indent=1, ensure_ascii=False), "utf-8")


main()
