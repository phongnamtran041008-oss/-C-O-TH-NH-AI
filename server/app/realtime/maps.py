"""Reads the Tiled maps in server/maps (the same files the client draws) for what the
server needs: collision, portals, spawn points, monster areas and water to fish in."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from ..config import SERVER_DIR
from .movement import Collider

MAP_DIR = SERVER_DIR / "maps"


@dataclass
class Area:
    name: str
    x: float
    y: float
    w: float
    h: float
    props: dict = field(default_factory=dict)

    def contains(self, px: float, py: float) -> bool:
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h


@dataclass
class ZoneMap:
    name: str
    width_px: int
    height_px: int
    collider: Collider
    spawns: dict[str, tuple[float, float]]
    portals: list[Area]
    monster_areas: list[Area]
    npcs: dict[str, tuple[float, float]] = field(default_factory=dict)   # npc id -> feet position
    fishing: list[Area] = field(default_factory=list)   # water: area objects of kind pond/fishing (prop pool)
    rooms: dict[str, Area] = field(default_factory=dict)  # bí cảnh (stage 9): room kind -> its floor
    realm_objs: list[Area] = field(default_factory=list)  # puzzle props: pedestals, tiles, pillars...
    interacts: dict[str, tuple[float, float]] = field(default_factory=dict)  # action -> foot of the prop
    ground: list[int] = field(default_factory=list)       # the ground layer: one Tiled gid per tile, row by row
    tile: int = 16
    khu: list[Area] = field(default_factory=list)         # Đại Địa Đồ: the sub-areas of a land (realtime/dia_do.py)
    pois: list[Area] = field(default_factory=list)        # Đại Địa Đồ: named places the big map lists

    def spawn(self, name: str | None) -> tuple[float, float]:
        return self.spawns.get(name or "spawn") or self.spawns.get("spawn") or (self.width_px / 2, self.height_px / 2)

    def tile_name(self, tx: int, ty: int) -> str | None:
        """What the ground of tile (tx, ty) is ('water', 'ink', 'grass'...), None off the map."""
        cols = self.width_px // self.tile
        if not (0 <= tx < cols and 0 <= ty < self.height_px // self.tile) or not self.ground:
            return None
        gid = self.ground[ty * cols + tx]
        return TILE_NAMES[gid - 1] if 0 < gid <= len(TILE_NAMES) else None


# The ground tiles by Tiled gid - 1: the names of client/art/build.py TILESET, in the same order
# (client/tests check the two agree). Đạp Kiếm Lướt glides over the ones world_plan.json names.
TILE_NAMES = ("grass", "grass", "grass", "flowers", "flowers", "path", "path", "water", "bamboo_floor", "stone",
              "wood", "plaza", "plaza", "dirt", "dark_grass", "dark_grass", "ink", "ink", "realm_floor",
              "realm_floor", "realm_wall")


def parse(path: Path) -> ZoneMap:
    data = json.loads(path.read_text("utf-8"))
    tw, th = data["tilewidth"], data["tileheight"]
    solids, spawns, portals, areas, npcs, water = [], {}, [], [], {}, []
    rooms, realm_objs, interacts = {}, [], {}
    khu, pois = [], []
    ground: list[int] = []
    for layer in data["layers"]:
        if layer["type"] == "tilelayer" and layer.get("name") == "ground":
            ground = list(layer.get("data") or [])
        if layer["type"] != "objectgroup":
            continue
        for o in layer["objects"]:
            props = {p["name"]: p["value"] for p in o.get("properties", [])}
            if layer["name"] == "collision":
                solids.append((int(o["x"]), int(o["y"]), int(o["width"]), int(o["height"])))
            elif o.get("type") == "spawn":
                spawns[o.get("name") or "spawn"] = (float(o["x"]), float(o["y"]))
            elif o.get("type") == "portal":
                portals.append(Area(o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
            elif o.get("type") == "monster_area":
                areas.append(Area(o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
            elif o.get("type") == "npc" and props.get("npc"):
                npcs[props["npc"]] = (o["x"] + o["width"] / 2, o["y"] + o["height"])
            elif o.get("type") == "area" and props.get("kind") in ("pond", "fishing"):
                water.append(Area(o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
            elif o.get("type") == "interact" and props.get("action"):
                interacts.setdefault(props["action"], (o["x"] + o["width"] / 2, o["y"] + o["height"]))
            elif o.get("type") == "realm_room":
                rooms[props.get("kind", o.get("name", ""))] = Area(o.get("name", ""), o["x"], o["y"], o["width"],
                                                                   o["height"], props)
            elif o.get("type") == "realm_obj":
                realm_objs.append(Area(o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
            elif o.get("type") == "khu":
                khu.append(Area(props.get("khu") or o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
            elif o.get("type") == "poi":
                pois.append(Area(o.get("name", ""), o["x"], o["y"], o["width"], o["height"], props))
    w, h = data["width"] * tw, data["height"] * th
    return ZoneMap(path.stem, w, h, Collider(w, h, solids), spawns, portals, areas, npcs, water, rooms, realm_objs,
                   interacts, ground, tw, khu, pois)


@lru_cache(maxsize=None)
def load(name: str) -> ZoneMap:
    return parse(MAP_DIR / f"{name}.tmj")
