#!/usr/bin/env python3
"""Build the items no asset library had, and export them as .glb (M8).

    blender -b --factory-startup --python tools/blender/build_items.py

Three things the free libraries simply do not have, drawn from the author's own reference
sheets (`Downloads/file model cho vũ khí, trang bị, pháp trận, đan dược`):

* **quạt** - a folding fan. Searching a model library for "fan" returns ceiling fans.
* **hồ lô** - a calabash gourd. "gourd" returns onions and corn.
* **áo giáp** - a chest piece. Every armour query returns crates and shields.

The numbers below were pushed around in a live Blender and looked at after every change,
which is how the fan stopped being a disc and the chest stopped being a ball: a cube with
two levels of subdivision *is* a sphere, so the armour is bevelled instead, and a slat
centred on the pivot sweeps a full circle, so each one starts at the pivot and runs out.

The .glb files land in art/models/ beside the downloaded ones and are rendered by the same
tools/blender/render_item.py. They are the project's own work - no licence to carry.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "art" / "models"

COLOURS = {
    "paper": (0.90, 0.82, 0.62, 1), "bamboo": (0.45, 0.33, 0.18, 1),
    "gourd": (0.63, 0.40, 0.20, 1), "cord": (0.52, 0.17, 0.15, 1),
    "cork": (0.80, 0.66, 0.42, 1), "cloth": (0.42, 0.28, 0.18, 1),
    "plate": (0.55, 0.58, 0.64, 1), "belt": (0.30, 0.20, 0.12, 1),
    "dark": (0.13, 0.10, 0.09, 1),
}


def material(key: str) -> bpy.types.Material:
    m = bpy.data.materials.get(key)
    if m:
        return m
    m = bpy.data.materials.new(key)
    try:
        m.use_nodes = True
    except (AttributeError, DeprecationWarning):
        pass
    nodes = getattr(getattr(m, "node_tree", None), "nodes", [])
    b = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
    if b:
        b.inputs["Base Color"].default_value = COLOURS[key]
        b.inputs["Roughness"].default_value = 0.85
    m.diffuse_color = COLOURS[key]
    return m


def add(kind, name, loc, scale, key, rot=(0, 0, 0), sub=0, bevel=0.0, **kw):
    getattr(bpy.ops.mesh, kind)(location=loc, **kw)
    o = bpy.context.active_object
    o.name, o.scale = name, scale
    o.rotation_euler = [math.radians(a) for a in rot]
    o.data.materials.append(material(key))
    if bevel:
        b = o.modifiers.new("b", "BEVEL")
        b.width, b.segments = bevel, 2
    if sub:
        md = o.modifiers.new("s", "SUBSURF")
        md.levels = md.render_levels = sub
        bpy.ops.object.shade_smooth()
    return o


def clear() -> None:
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def build_quat() -> str:
    """A folding fan: the paper is a web of overlapping slats, each running out from the
    rivet, with bamboo ribs over it and a handle below."""
    r = 0.36
    for i in range(19):
        a = math.radians(-84 + i * 168 / 18)
        add("primitive_cube_add", f"fan_slat_{i}",
            (math.sin(a) * r / 2, 0, math.cos(a) * r / 2 + 0.26),
            (0.075, 0.010, r), "paper", rot=(0, math.degrees(a), 0), size=1.0)
    for i in range(10):
        a = math.radians(-80 + i * 160 / 9)
        add("primitive_cube_add", f"fan_rib_{i}",
            (math.sin(a) * r / 2, -0.012, math.cos(a) * r / 2 + 0.26),
            (0.015, 0.012, r * 1.02), "bamboo", rot=(0, math.degrees(a), 0), size=1.0)
    add("primitive_cylinder_add", "fan_rivet", (0, -0.02, 0.25), (0.05, 0.05, 0.035),
        "bamboo", rot=(90, 0, 0), vertices=10)
    add("primitive_cone_add", "fan_handle", (0, 0, 0.12), (0.06, 0.035, 0.15), "bamboo",
        vertices=8, radius1=1.0, radius2=0.5)
    return "fan_"


def build_ho_lo() -> str:
    """A calabash: small bulb over a big one, a waist between them, a cork and a cord."""
    add("primitive_uv_sphere_add", "gourd_bottom", (0, 0, 0.26), (0.30, 0.30, 0.30),
        "gourd", sub=1, segments=20, ring_count=12)
    add("primitive_uv_sphere_add", "gourd_top", (0, 0, 0.62), (0.185, 0.185, 0.185),
        "gourd", sub=1, segments=20, ring_count=12)
    add("primitive_cylinder_add", "gourd_waist", (0, 0, 0.47), (0.115, 0.115, 0.05),
        "gourd", sub=1, vertices=16)
    add("primitive_cylinder_add", "gourd_neck", (0, 0, 0.80), (0.075, 0.075, 0.045),
        "cork", vertices=12)
    add("primitive_torus_add", "gourd_cord", (0, 0, 0.50), (0.145, 0.145, 0.145), "cord",
        major_segments=16, minor_segments=6, major_radius=1.0, minor_radius=0.12)
    return "gourd_"


def build_ao_giap() -> str:
    """A chest piece: bevelled boxes, wide at the shoulders, pinched at the waist, with
    pauldrons, a dark collar and a belt."""
    add("primitive_cube_add", "armour_chest", (0, 0, 0.47), (0.50, 0.25, 0.40), "plate",
        bevel=0.06, size=1.0)
    add("primitive_cube_add", "armour_waist", (0, 0, 0.21), (0.38, 0.22, 0.20), "plate",
        bevel=0.05, size=1.0)
    add("primitive_cube_add", "armour_neck", (0, -0.03, 0.67), (0.19, 0.19, 0.08), "dark",
        bevel=0.03, size=1.0)
    for side in (1, -1):
        add("primitive_cube_add", f"armour_pauldron_{side}", (side * 0.255, 0, 0.60),
            (0.17, 0.24, 0.13), "plate", bevel=0.05, rot=(0, side * 10, 0), size=1.0)
        add("primitive_cube_add", f"armour_v_{side}", (side * 0.05, -0.128, 0.55),
            (0.05, 0.02, 0.26), "cloth", rot=(0, side * -15, 0), size=1.0)
    add("primitive_cube_add", "armour_belt", (0, 0, 0.16), (0.42, 0.24, 0.08), "belt",
        bevel=0.02, size=1.0)
    add("primitive_cube_add", "armour_buckle", (0, -0.125, 0.16), (0.10, 0.03, 0.09),
        "cork", size=1.0)
    return "armour_"


ITEMS = {"vu_khi/quat": build_quat, "vu_khi/ho_lo": build_ho_lo,
         "trang_bi/ao_giap": build_ao_giap}


def main() -> int:
    made = []
    for rel, build in ITEMS.items():
        clear()
        prefix = build()
        objs = [o for o in bpy.data.objects if o.name.startswith(prefix)]
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        path = OUT / f"{rel}.glb"
        path.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=str(path), use_selection=True,
                                  export_format="GLB", export_apply=True)
        made.append((rel, len(objs), path.stat().st_size // 1024))
    for rel, n, kb in made:
        print(f"built {rel}: {n} parts -> {kb} KB")
    print(f"{len(made)} item(s) exported to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
