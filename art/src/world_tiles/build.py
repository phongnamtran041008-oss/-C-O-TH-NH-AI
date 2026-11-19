"""WORLD_TILES batch: base tileset, extended terrain tiles, nature props, previews. All rendering goes
through the shared kit (tools/blender/kit).

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/world_tiles/build.py [--only a,b] [--no-render]

1. `scene.py` runs inside headless Blender: builds every model, saves art/blender/world_tiles/*.blend,
   renders tiles and props with kit.render_tiles / kit.render_props (client/assets/v2/).
2. This script patches the packed json (see `post_*`), runs the kit QC and writes the previews.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
sys.path.insert(0, str(HERE))

from kit import launcher  # noqa: E402
import build_lists as L  # noqa: E402

TILES = ROOT / "client" / "assets" / "v2" / "tiles"
PROPS = ROOT / "client" / "assets" / "v2" / "props"


def _pg():
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    pygame.display.set_mode((8, 8))
    return pygame


def strip_first(region: str) -> None:
    """The first tile of a kit render_tiles call is a throw-away copy (scene.py); cut it out and renumber."""
    pygame = _pg()
    jp = TILES / f"{region}.json"
    doc = json.loads(jp.read_text("utf-8"))
    if "_first" not in doc["tiles"]:
        return
    img = pygame.image.load(str(TILES / doc["sheet"])).convert_alpha()
    cols = doc["cols"]
    n_old = max(i for v in doc["tiles"].values() for i in v) + 1
    n_new = n_old - 1
    ncols = min(8, n_new)
    out = pygame.Surface((ncols * 16, ((n_new + ncols - 1) // ncols) * 16), pygame.SRCALPHA)
    for i in range(1, n_old):
        j = i - 1
        out.blit(img, ((j % ncols) * 16, (j // ncols) * 16), ((i % cols) * 16, (i // cols) * 16, 16, 16))
    pygame.image.save(out, str(TILES / doc["sheet"]))
    del doc["tiles"]["_first"]
    doc["tiles"] = {k: [i - 1 for i in v] for k, v in doc["tiles"].items()}
    doc["cols"] = ncols
    doc["count"] = n_new
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")


def post_base() -> None:
    jp = TILES / "base.json"
    doc = json.loads(jp.read_text("utf-8"))
    t = doc["tiles"]
    for alt, main in (("stone_alt", "stone"), ("plaza_alt", "plaza")):
        if alt in t:
            t.setdefault(main, []).extend(t.pop(alt))
    doc["id"] = "base"
    doc["note"] = ("indices 0..20 are the TILESET of client/art/build.py in the same order and grid (gid = index + 1); "
                   "water_anim = 4 frames; stone / plaza list their extra variants after the original index")
    if "water_anim" in t:
        doc["water_anim"] = {"frames": t["water_anim"], "fps": 2}
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")


def post_terrain() -> None:
    jp = TILES / "terrain.json"
    doc = json.loads(jp.read_text("utf-8"))
    doc["id"] = "terrain"
    doc["autotile"] = {
        "naming": "suffix = where the OUTER material lies (grass_path_n has grass to the north of the path); nw/ne/sw/se are "
                  "convex corners of the inner blob, in_nw.. concave (notch) corners. Blob edge is 5 px inside the tile ring.",
        "pairs": {"grass_path": "path", "grass_dirt": "dirt", "shore": "water (static frame; use base water_anim inside)"},
        "plateau": "cliff_nw..cliff_e = back and side edges of raised land (lighter top); the front is cliff_face_a (upper, with the "
                   "grass lip) over cliff_face_b, ends _l/_r, variants a2/b2, then cliff_shadow(_l/_r) on the ground below; "
                   "stairs_a/b are worn steps cut into the face (put a face tile on each side)",
        "bridge": "bridge_h / bridge_v middle tiles carry a frame of water (the ground layer is opaque); bridge_h_w/e and "
                  "bridge_v_n/s sit on the shore bank"}
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")


def post_props() -> None:
    jp = PROPS / "nature.json"
    doc = json.loads(jp.read_text("utf-8"))
    for name, p in doc["props"].items():
        s = L.PROP_SOLID.get(name)
        if s:
            px, py = p["pivot"]
            p["solid"] = [px + s[0], py + s[1], s[2], s[3]]
        p["name_vi"] = L.PROP_NAME_VI.get(name, name)
    doc["id"] = "nature"
    doc["note"] = "pivot = ground point at the base and solid = [x, y, w, h] (walk-blocking footprint), both relative to rect"
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")


def post_32() -> None:
    jp = TILES / "base32.json"
    doc = json.loads(jp.read_text("utf-8"))
    t = doc["tiles"]
    for alt, main in (("stone_alt", "stone"), ("plaza_alt", "plaza"), ("dirt_alt", "dirt")):
        if alt in t:
            t.setdefault(main, []).extend(t.pop(alt))
    doc["id"] = "base32"
    doc["note"] = ("32 px per tile. Indices 0..20 are the TILESET of client/art/build.py (same order as base.png, gid = index + 1); "
                   "water_anim = 4 frames; stone / plaza / dirt list their extra variants after the original index "
                   "(dirt has 3 variants that tile with each other; only the third has two tiny off-centre stones)")
    if "water_anim" in t:
        doc["water_anim"] = {"frames": t["water_anim"], "fps": 2}
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")
    jp = TILES / "terrain32.json"
    doc = json.loads(jp.read_text("utf-8"))
    doc["id"] = "terrain32"
    doc["autotile"] = {
        "naming": "suffix = where the OUTER material lies (grass_path_n has grass to the north of the path); nw/ne/sw/se are convex "
                  "corners, in_nw.. concave (notch) corners. The blob edge is 5 px (of 16) inside the tile ring.",
        "pairs": {"grass_path": "path (centre tile: base32 'path')", "grass_dirt": "dirt (centre tiles: base32 'dirt')",
                  "shore": "water (static frame; use base32 water_anim inside)",
                  "grass_stone": "cobbles (centre: base32 'stone')", "grass_plaza": "flagstones (centre: base32 'plaza')",
                  "grass_dark": "dark_grass inside grass (centre: base32 'dark_grass')",
                  "dark_ink": "ink ground inside dark_grass (outer = dark_grass, centre: base32 'ink')",
                  "realm_edge": "bi canh: slate floor outside, wall block inside (12 tiles: 8 sides + 4 inner corners); wall interior = base32 realm_wall"},
        "isolated_cells": {"island": "all four sides grass: a soft round 10 px patch",
                           "h": "grass north and south: a horizontal strip 8 px wide", "v": "grass east and west: a vertical strip",
                           "cap_n/cap_s/cap_e/cap_w": "end of a strip; the name is the side that is open (grass), e.g. cap_e ends the strip on its east side"},
        "rule": ["n, s, e, w = the 4 neighbours belong to the same material",
                 "0 neighbours -> <pair>_island",
                 "1 neighbour -> N present: _cap_s | S present: _cap_n | E present: _cap_w | W present: _cap_e",
                 "2 opposite neighbours -> N+S: _v | E+W: _h",
                 "2 adjacent neighbours (a corner) -> _ + the missing sides in the order n s w e: _nw _ne _sw _se",
                 "3 neighbours -> _ + the missing side: _n _s _w _e",
                 "4 neighbours -> the first missing diagonal in the order nw ne sw se gives _in_<it>; none missing -> the centre tile",
                 "1-wide strips are 8 px wide and blob edges 11 px: paint paths at least 2 cells wide where they turn, branch or meet a wider area"],
        "plateau": "cliff_nw..cliff_e = back and side edges of raised land (lighter top: plateau_top); the front is cliff_face_a (upper, "
                   "with the grass lip) over cliff_face_b, ends _l/_r, variants a2/b2, then cliff_shadow(_l/_r); stairs_a/b are worn "
                   "steps cut into the face (put a face tile on each side)",
        "bridge": "bridge_h / bridge_v middle tiles carry a frame of water; bridge_h_w/e and bridge_v_n/s sit on the shore bank"}
    jp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), "utf-8")


def pad_td24() -> None:
    """The kit QC reads tile sheets on a 16 px grid: pad the 24 px sheet to an even number of rows (a multiple of 16 px tall)."""
    pygame = _pg()
    png = TILES / "td24.png"
    if not png.exists():
        return
    img = pygame.image.load(str(png)).convert_alpha()
    h = img.get_height()
    if h % 16:
        out = pygame.Surface((img.get_width(), h + 24), pygame.SRCALPHA)
        out.blit(img, (0, 0))
        pygame.image.save(out, str(png))


def main() -> int:
    args = sys.argv[1:]
    parts = {"16", "32", "village", "garden", "realm", "td"}
    if "--parts" in args:
        parts = set(args[args.index("--parts") + 1].split(","))
    only = ["--only", args[args.index("--only") + 1]] if "--only" in args else []
    if "--no-render" not in args:
        for part, script, extra in (("16", "scene.py", []), ("32", "scene32.py", []), ("village", "scene_village.py", []),
                                    ("garden", "scene_garden.py", []), ("realm", "scene_realm.py", []),
                                    ("td", "scene_td_props.py", []), ("td", "scene32.py", ["--set", "td"])):
            if part in parts:
                code = launcher.run_blender(HERE / script, "world_tiles", only + extra)
                if code:
                    return code
    if not only:
        if "16" in parts:
            post_base()
            post_terrain()
            post_props()
        if "32" in parts:
            post_32()
        if "td" in parts:
            pad_td24()
    import wt_preview
    import wt_preview32
    import wt_preview_extra
    if (TILES / "base.json").exists():
        wt_preview.make_all()
    wt_preview32.make_all()
    wt_preview_extra.make_all()
    if not only:
        problems = launcher.finish("world_tiles", ["client/assets/v2/tiles", "client/assets/v2/props"], preview_name="world_kit_qc")
        print("kit QC problems:", problems)
    return 0


if __name__ == "__main__":
    sys.exit(main())
