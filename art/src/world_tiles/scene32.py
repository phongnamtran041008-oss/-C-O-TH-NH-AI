"""WORLD_TILES at 32 px (the game draws the world at 2x): the same scenes as scene.py, rendered at twice the
pixels per metre with smaller, more numerous marks (wt_common.DETAIL = 1.6). Runs inside Blender via the kit launcher.

The kit's render_tiles is fixed at 16 px, so this file repeats its loop with a 32 px camera (it uses the kit's own
camera, staging, material and pixel functions) and packs with the kit's packer.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy
from mathutils import Matrix

import kit.api as kit
from kit import pack
from kit.api import _pal, _render_frames, _wrap_copies, out_path, wrap_check
from kit.scene import Cam, Staging, expand, prepare_materials, setup_render

import wt_common as C

C.KIT = True
ARGS = sys.argv[1:]
SET = ARGS[ARGS.index("--set") + 1] if "--set" in ARGS else "world"
C.DETAIL = 1.25 if SET == "td" else 1.6
ONLY = set(ARGS[ARGS.index("--only") + 1].split(",")) if "--only" in ARGS else None
OUT_TILES = "client/assets/v2/tiles"
PX = 24 if SET == "td" else 32
S_TILE = kit.TILE_M / C.T


def build(mod):
    out = {}
    for a in mod.assets():
        if ONLY and a["id"] not in ONLY and not any(s[0] in ONLY for s in a["slices"]):
            continue
        col = C.collection(a["id"])
        a["build"](col)
        out[a["id"]] = (a, col)
    return out


_DONE: dict = {}


def tile_entry(a, col, name, tx, ty):
    if name in _DONE:
        return _DONE[name]
    cx = tx * C.T + C.T / 2
    cy = (a["h"] - 1 - ty) * C.T + C.T / 2
    M = Matrix.Scale(S_TILE, 4) @ Matrix.Translation((-cx, -cy, 0))
    if a["w"] == 1 and a["h"] == 1:
        for ob in col.objects:
            ob.matrix_basis = M @ ob.matrix_basis
        _DONE[name] = col
        return col
    import bpy as _b
    dup = _b.data.collections.new(f"COL_{name}")
    _b.context.scene.collection.children.link(dup)
    for ob in col.objects:
        o2 = _b.data.objects.new(ob.name, ob.data)
        o2.matrix_basis = M @ ob.matrix_basis
        dup.objects.link(o2)
    _DONE[name] = dup
    return dup


def render_tiles32(region, entries):
    """entries: {name: [ {"objects", "wrap"} ]} -> packs client/assets/v2/tiles/<region>.png at 32 px per tile."""
    pal = _pal(None)
    scene = setup_render()
    cam = Cam("top", PX, PX, PX / kit.TILE_M, (PX / 2, PX / 2))
    images, names, scores = [], {}, {}
    kit.log(f"render_tiles32 {region}: {sum(len(v) for v in entries.values())} tiles")
    for name, lst in entries.items():
        names[name] = []
        for k, e in enumerate(lst):
            objs = expand(e["objects"])
            w = e["wrap"]
            copies = _wrap_copies(objs, kit.TILE_M) if w else []
            try:
                with Staging(scene, objs + copies) as st:
                    cam.apply(scene)
                    mats = prepare_materials(objs + copies, cam)
                    opts = dict(outline=False, inner_lines=False, wrap=w)
                    img = _render_frames(scene, st, cam, mats, pal, None, opts, [lambda: None])[0]
            finally:
                for c in copies:
                    bpy.data.objects.remove(c)
            if w:
                scores[f"{name}[{k}]"] = round(wrap_check(img), 2)
            names[name].append(len(images))
            images.append(img)
    doc = pack.pack_tiles(out_path(OUT_TILES), region, images, names, 8,
                          extra={"cell": PX, "render": {"tile_m": kit.TILE_M, "px_per_tile": PX, "wrap_check": scores}})
    # pack_tiles writes "tile": 16; this sheet is 32 px
    import json
    jp = out_path(OUT_TILES) / f"{region}.json"
    d = json.loads(jp.read_text("utf-8"))
    d["tile"] = PX
    jp.write_text(json.dumps(d, indent=1, ensure_ascii=False), "utf-8")
    bad = {k: v for k, v in scores.items() if v > 2.0}
    kit.log(f"wrote {region}.png; wrap check {scores}" + (f"  SEAM WARNING {bad}" if bad else ""))


def collect(groups, order, wrap_names):
    slices = {}
    for aid, (a, col) in groups.items():
        for (name, tx, ty) in a["slices"]:
            slices[name] = (a, col, tx, ty)
    entries = {}
    for key, names in order.items():
        lst = []
        for n in names:
            if (ONLY and n not in ONLY) or n not in slices:
                continue
            a, col, tx, ty = slices[n]
            lst.append({"objects": tile_entry(a, col, n, tx, ty), "wrap": n in wrap_names})
        if lst:
            entries[key] = lst
    return entries


def td_path_cell(col, sides):
    """A TD path cell: the whole cell is path; a bank of grass (with a dark lip) lies along every side listed in `sides`."""
    import wt_base
    from wt_common import mat, box
    wt_base.b_path(col, 0)
    for sd in sides:
        horiz = sd in "ns"
        sign = 1 if sd in "ne" else -1
        d = 3.2
        cx = 8 if horiz else (16 - d / 2 if sign > 0 else d / 2)
        cy_ = (16 - d / 2 if sign > 0 else d / 2) if horiz else 8
        w, h = (16, d) if horiz else (d, 16)
        box(col, "bank", (cx, cy_, 0.7), (w, h, 1.4), mat("grass", 1), bevel=0.7)
        lipx = cx - (0 if horiz else sign * (d / 2 + 0.4) * -1) if False else cx
        off = -sign * (d / 2 + 0.2)
        box(col, "lip", ((cx + (0 if horiz else off)), (cy_ + (off if horiz else 0)), 0.3), ((16 if horiz else 0.7), (0.7 if horiz else 16), 0.6), mat("grass", 0))


def main():
    import wt_base, wt_terrain
    from build_lists import TERRAIN32_ORDER, TERRAIN_WRAP
    kit.clear_scene()
    base = build(wt_base)
    terr = build(wt_terrain)
    if SET == "td":
        import itertools
        want = {"grass_0", "grass_1", "path_0", "path_1"}
        base = {k: v for k, v in base.items() if k in want}
        order = {"grass": ["grass_0", "grass_1"], "path": ["path_0", "path_1"]}
        wrapped = {"grass_0", "grass_1", "path_0", "path_1"}
        groups = dict(base)
        for r in range(0, 5):
            for combo in itertools.combinations("nesw", r):
                letters = "".join(combo)
                nm = f"td_path_{letters or 'none'}"
                a = dict(id=nm, w=1, h=1, slices=[(nm, 0, 0)], build=(lambda col, L=letters: td_path_cell(col, L)))
                colx = C.collection(nm)
                a["build"](colx)
                groups[nm] = (a, colx)
                order[nm] = [nm]
        e = collect(groups, order, wrapped)
        render_tiles32("td24", e)
        return
    order = {}
    for n, v in wt_base.BASE:
        order.setdefault(n, []).append(f"{n}_{v}" if n != "water" else "water_f0")
    order["water_anim"] = [f"water_f{i}" for i in range(4)]
    order["stone_alt"] = ["stone_1"]
    order["plaza_alt"] = ["plaza_2"]
    order["dirt_alt"] = ["dirt_1", "dirt_2"]
    wrapped = {s[0] for _, (a, _c) in base.items() for s in a["slices"]}
    e = collect(base, order, wrapped)
    if e:
        render_tiles32("base32", e)
    t_order = {}
    for n in TERRAIN32_ORDER:
        t_order.setdefault("plateau_top" if n.startswith("plateau_top_") else n, []).append(n)
    e = collect(terr, t_order, TERRAIN_WRAP)
    if e:
        render_tiles32("terrain32", e)


main()
