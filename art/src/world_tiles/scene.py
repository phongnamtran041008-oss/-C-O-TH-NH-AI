"""WORLD_TILES, Blender side: builds every model by script, saves the .blend files, then renders
and packs through the kit (tools/blender/kit). Started by build.py via kit.launcher.

    sys.argv[1:]: optional "--only name,name" (tile / prop names), "--no-blend"
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy
from mathutils import Matrix

import kit.api as kit
import wt_common as C

C.KIT = True
ARGS = sys.argv[1:]
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None
SAVE = "--no-blend" not in ARGS and ONLY is None
OUT_TILES = "client/assets/v2/tiles"
OUT_PROPS = "client/assets/v2/props"
S_TILE = kit.TILE_M / C.T            # tile units (16 per tile) -> metres


def build(mod, group):
    out = {}
    for a in mod.assets():
        if ONLY and a["id"] not in ONLY and not any(s[0] in ONLY for s in a["slices"]):
            continue
        col = C.collection(a["id"])
        a["build"](col)
        if a.get("scale", 1.0) != 1.0:
            for ob in col.objects:
                ob.matrix_basis = Matrix.Scale(a["scale"], 4) @ ob.matrix_basis
        out[a["id"]] = (a, col)
    return out


_DONE: dict = {}


def tile_entry(a, col, name, tx, ty):
    """The objects of one 16 px slice, moved so the slice is centred on the origin and scaled to metres."""
    if name in _DONE:
        return _DONE[name]
    _DONE[name] = _tile_entry(a, col, name, tx, ty)
    return _DONE[name]


def _tile_entry(a, col, name, tx, ty):
    cx = tx * C.T + C.T / 2
    cy = (a["h"] - 1 - ty) * C.T + C.T / 2
    M = Matrix.Scale(S_TILE, 4) @ Matrix.Translation((-cx, -cy, 0))
    if a["w"] == 1 and a["h"] == 1:
        for ob in col.objects:
            ob.matrix_basis = M @ ob.matrix_basis
        return col
    dup = bpy.data.collections.new(f"COL_{name}")
    bpy.context.scene.collection.children.link(dup)
    for ob in col.objects:
        o2 = bpy.data.objects.new(ob.name, ob.data)
        o2.matrix_basis = M @ ob.matrix_basis
        dup.objects.link(o2)
    return dup


def render_tiles(region, groups, order, wrap_names):
    """groups: dict of asset id -> (a, col); order: {tile name: [slice names]} (the sheet order)."""
    slices = {}
    for aid, (a, col) in groups.items():
        for (name, tx, ty) in a["slices"]:
            slices[name] = (a, col, tx, ty)
    entries = {}
    for key, names in order.items():
        lst = []
        for n in names:
            if ONLY and n not in ONLY:
                continue
            if n not in slices:
                continue
            a, col, tx, ty = slices[n]
            lst.append({"objects": tile_entry(a, col, n, tx, ty), "wrap": n in wrap_names})
        if lst:
            entries[key] = lst
    if entries:
        return kit.render_tiles(region, entries, OUT_TILES)


def main():
    import wt_base, wt_terrain, wt_props
    kit.clear_scene()
    base = build(wt_base, "base")
    terr = build(wt_terrain, "terrain")
    props = build(wt_props, "props")
    if SAVE:
        for name, grp in (("base", base), ("terrain", terr), ("props", props)):
            keep = {c.name for _, c in grp.values()}
            for c in bpy.context.scene.collection.children:
                c.hide_viewport = c.name not in keep
            kit.save_blend(f"art/blender/world_tiles/{name}.blend")
        for c in bpy.context.scene.collection.children:
            c.hide_viewport = False
    # ---------------------------------------------------------------- base.png (TILESET order + extras)
    order = {}
    for n, v in wt_base.BASE:
        order.setdefault(n, []).append(f"{n}_{v}" if n != "water" else "water_f0")
    order["water_anim"] = [f"water_f{i}" for i in range(4)]
    order["stone_alt"] = ["stone_1"]
    order["plaza_alt"] = ["plaza_2"]
    wrapped = {s for k, g in base.items() for s in [x[0] for x in g[0]["slices"]]}
    render_tiles("base", base, order, wrapped)
    # ---------------------------------------------------------------- terrain.png
    from build_lists import TERRAIN_ORDER, TERRAIN_WRAP
    t_order = {}
    for n in TERRAIN_ORDER:
        t_order.setdefault("plateau_top" if n.startswith("plateau_top_") else n, []).append(n)
    render_tiles("terrain", terr, t_order, TERRAIN_WRAP)
    # ---------------------------------------------------------------- nature.png
    plist = []
    for p in wt_props.PROPS:
        if p["id"] in props:
            plist.append({"name": p["id"], "objects": props[p["id"]][1], "solid": None,
                          "ppm": wt_props.KIT_PPM})
    if plist:
        kit.render_props("nature", plist, OUT_PROPS)


main()
