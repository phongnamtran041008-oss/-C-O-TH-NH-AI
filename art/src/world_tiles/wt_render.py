"""Blender side: render sets of fixed-size sprites (props with frames) through the kit and pack them as a props atlas.

A spec is a dict: name, W, H, frames, build(col, frame) -> None, mode ('ground' = the standard 35 degree camera, 'top' = straight
down), base (px between the origin and the bottom of the frame, 'ground' mode), ppm, solid (dx, dy, w, h relative to the pivot),
vi (Vietnamese name), extra (dict merged into the json entry), pivot (override, default (W/2, H)).
"""
from __future__ import annotations

import json

import bpy
import numpy as np

import kit.api as kit
from kit import pack
from kit.api import _pal, _render_frames, out_path
from kit.scene import Cam, Staging, expand, prepare_materials, setup_render

import wt_common as C


def build_one(builder, frame):
    C._MATS.clear()                      # fresh materials: the kit rewrites them in memory when it renders
    col = C.collection(f"b{len(bpy.data.collections)}")
    builder(col, frame)
    return col


def render_set(region, specs, out="client/assets/v2/props", ppm=47.0, before=None, note=""):
    pal = _pal(None)
    scene = setup_render()
    packed, notes = [], []
    for sp in specs:
        W, H = sp["W"], sp["H"]
        imgs = []
        for f in range(sp.get("frames", 1)):
            if before:
                before(sp)
            col = build_one(sp["build"], f)
            objs = expand(col)
            mode = sp.get("mode", "ground")
            p = sp.get("ppm", ppm)
            if mode == "top":
                cam = Cam("top", W, H, p, (W / 2, H / 2))
            else:
                cam = Cam("ground", W, H, p, (W / 2, H - sp.get("base", 5)))
            with Staging(scene, objs) as st:
                cam.apply(scene)
                mats = prepare_materials(objs, cam)
                img = _render_frames(scene, st, cam, mats, pal, None, {}, [lambda: None])[0]
            imgs.append(img)
            a = img[..., 3] > 0
            if a.any():
                ys, xs = np.nonzero(a)
                if xs.min() == 0 or ys.min() == 0 or xs.max() == W - 1 or ys.max() == H - 1:
                    notes.append(f"{sp['name']}[{f}] touches the frame: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} of {W}x{H}")
            for ob in list(col.objects):
                bpy.data.objects.remove(ob)
            bpy.data.collections.remove(col)
        sol = None
        if sp.get("solid"):
            s = sp["solid"]
            sol = [int(W / 2 + s[0]), int(H + s[1]), int(s[2]), int(s[3])]
        packed.append({"name": sp["name"], "frames": imgs, "pivot": sp.get("pivot", (W // 2, H)), "solid": sol, "sp": sp})
    for n in notes:
        kit.log("EDGE " + n)
    pack.pack_props(out_path(out), region, [{k: v for k, v in p.items() if k != "sp"} for p in packed])
    jp = out_path(out) / f"{region}.json"
    d = json.loads(jp.read_text("utf-8"))
    for p in packed:
        e = d["props"][p["name"]]
        if p["sp"].get("vi"):
            e["name_vi"] = p["sp"]["vi"]
        e.update(p["sp"].get("extra", {}))
    d["id"] = region
    d["note"] = note
    jp.write_text(json.dumps(d, indent=1, ensure_ascii=False), "utf-8")
    return d
