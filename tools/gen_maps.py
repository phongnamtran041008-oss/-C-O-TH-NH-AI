#!/usr/bin/env python3
"""Generate the Tiled maps (.tmj, Tiled JSON 1.10) used by the client.

The abode map is laid out by code so it can be regenerated, and it opens in the Tiled
editor (https://www.mapeditor.org) for hand editing afterwards. Tile ids refer to
client/assets/sprites/tiles.png (written by tools/gen_sprites.py); props and areas are
rectangle objects whose `sprite`/`kind` property the client understands.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "client" / "assets" / "maps"
sys.path.insert(0, str(ROOT))

from client.art.build import TILESET  # noqa: E402

T = 16
GID = {f"{n}{v}": i + 1 for i, (n, v) in enumerate(TILESET)}


def abode() -> dict:
    W, H = 40, 24
    rng = random.Random("abode")
    ground = []
    for y in range(H):
        for x in range(W):
            r = rng.random()
            g = GID["grass0"] if r < 0.6 else GID["grass1"] if r < 0.85 else GID["grass2"]
            if r > 0.96:
                g = GID["flowers0"] if r > 0.98 else GID["flowers1"]
            if x < 2 or x >= W - 2 or y < 2 or y >= H - 2:
                g = GID["bamboo_floor0"]
            ground.append(g)

    def setg(x, y, gid):
        if 0 <= x < W and 0 <= y < H:
            ground[y * W + x] = gid

    def path(x0, y0, x1, y1):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                setg(x, y, GID["path0"] if (x + y) % 3 else GID["path1"])

    # the courtyard at tiles (14..23, 7..16), framed by a path
    gx, gy = 14, 7
    path(gx - 1, gy - 1, gx + 10, gy - 1)
    path(gx - 1, gy + 10, gx + 10, gy + 10)
    path(gx - 1, gy - 1, gx - 1, gy + 10)
    path(gx + 10, gy - 1, gx + 10, gy + 10)
    path(19, gy + 10, 20, H - 3)          # to the gate
    path(8, 8, gx - 1, 8)                 # to the hut
    path(gx + 10, 8, 30, 8)               # to the shrine
    # pond (ao nhỏ), bottom-left
    for y in range(16, 20):
        for x in range(4, 10):
            setg(x, y, GID["water0"])
    for x in range(3, 11):
        setg(x, 15, GID["stone0"])
        setg(x, 20, GID["stone0"])
    for y in range(15, 21):
        setg(3, y, GID["stone0"])
        setg(10, y, GID["stone0"])
    # wooden deck in front of the hut
    for x in range(4, 9):
        setg(x, 7, GID["wood0"])

    objects, collision = [], []
    oid = [1]

    def obj(name, otype, x, y, w, h, **props):
        o = {"id": oid[0], "name": name, "type": otype, "x": x, "y": y, "width": w, "height": h,
             "rotation": 0, "visible": True,
             "properties": [{"name": k, "type": "string", "value": str(v)} for k, v in props.items()]}
        oid[0] += 1
        objects.append(o)
        return o

    def solid(x, y, w, h):
        collision.append({"id": oid[0], "name": "", "type": "solid", "x": x, "y": y, "width": w,
                          "height": h, "rotation": 0, "visible": True})
        oid[0] += 1

    # bamboo ring
    for x in range(0, W * T, T):
        obj("bamboo", "prop", x, -12, 16, 40, sprite="bamboo", variant=x // T)
        if not (18 * T <= x <= 21 * T):  # gap for the gate
            obj("bamboo", "prop", x, (H - 2) * T - 8, 16, 40, sprite="bamboo", variant=x // T + 50)
    for y in range(2 * T, (H - 2) * T, T):
        obj("bamboo", "prop", 0, y - 8, 16, 40, sprite="bamboo", variant=y // T + 100)
        obj("bamboo", "prop", (W - 1) * T, y - 8, 16, 40, sprite="bamboo", variant=y // T + 200)
    solid(0, 0, W * T, 2 * T)
    solid(0, (H - 2) * T, 18 * T, 2 * T)
    solid(22 * T, (H - 2) * T, (W - 22) * T, 2 * T)
    solid(0, 0, 2 * T, H * T)
    solid((W - 2) * T, 0, 2 * T, H * T)

    obj("hut", "prop", 3 * T, 4 * T - 8, 64, 56, sprite="hut")
    solid(3 * T + 6, 4 * T + 16, 52, 30)
    obj("Trúc Lão", "npc", 9 * T, 6 * T, 16, 24, npc="truc_lao")
    solid(9 * T + 2, 6 * T + 14, 12, 10)
    obj("Thiên Cơ Đài", "interact", 30 * T, 5 * T, 32, 44, sprite="shrine", action="gacha")
    solid(30 * T + 2, 5 * T + 30, 28, 14)
    obj("Bàn đả tọa", "interact", 30 * T, 15 * T, 24, 16, sprite="mat", action="meditate")
    obj("Linh Phong Sào", "interact", 27 * T, 11 * T, 24, 32, sprite="hive", action="hive")
    solid(27 * T + 7, 11 * T + 24, 10, 8)
    obj("Đan Lô", "interact", 34 * T, 16 * T, 24, 28, sprite="furnace", action="alchemy")   # stage 8
    solid(34 * T + 3, 16 * T + 16, 18, 12)
    obj("Cổng tre", "interact", 18 * T + 8, (H - 3) * T - 4, 32, 32, sprite="gate", action="exit")
    obj("pond", "area", 4 * T, 16 * T, 6 * T, 4 * T, kind="pond")
    solid(4 * T, 16 * T, 6 * T, 4 * T)
    for (x, y) in ((27, 17), (34, 11), (12, 18)):
        obj("rock", "prop", x * T, y * T, 16, 12, sprite="rock")
        solid(x * T + 2, y * T + 4, 12, 8)
    obj("spawn", "spawn", 19 * T + 8, (H - 5) * T, 1, 1)

    return {
        "compressionlevel": -1, "height": H, "width": W, "infinite": False,
        "orientation": "orthogonal", "renderorder": "right-down", "tiledversion": "1.10.2",
        "tileheight": T, "tilewidth": T, "type": "map", "version": "1.10",
        "nextlayerid": 4, "nextobjectid": oid[0],
        "properties": [{"name": "zone", "type": "string", "value": "abode"},
                       {"name": "name_vi", "type": "string", "value": "Động Phủ"}],
        "layers": [
            {"id": 1, "name": "ground", "type": "tilelayer", "width": W, "height": H, "x": 0, "y": 0,
             "opacity": 1, "visible": True, "data": ground},
            {"id": 2, "name": "objects", "type": "objectgroup", "draworder": "topdown", "opacity": 1,
             "visible": True, "x": 0, "y": 0, "objects": objects},
            {"id": 3, "name": "collision", "type": "objectgroup", "draworder": "topdown", "opacity": 1,
             "visible": False, "x": 0, "y": 0, "objects": collision},
        ],
        "tilesets": [{"firstgid": 1, "name": "tiles", "image": "../sprites/tiles.png",
                      "imagewidth": 128, "imageheight": 16 * ((len(TILESET) + 7) // 8), "tilewidth": T, "tileheight": T,
                      "tilecount": len(TILESET), "columns": 8, "margin": 0, "spacing": 0}],
    }


class MapBuilder:
    """Small helper for the stage 3 zones: ground grid + objects + collision rectangles."""

    def __init__(self, zone: str, name_vi: str, w: int, h: int, seed: str):
        self.zone, self.name_vi, self.W, self.H = zone, name_vi, w, h
        self.rng = random.Random(seed)
        self.ground = [0] * (w * h)
        self.objects: list[dict] = []
        self.collision: list[dict] = []
        self.oid = 1
        self.blocked_tiles: set[tuple[int, int]] = set()   # where scatter props may not go

    def setg(self, x, y, key):
        if 0 <= x < self.W and 0 <= y < self.H:
            self.ground[y * self.W + x] = GID[key]

    def fill(self, x0, y0, x1, y1, keys, reserve=True):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                k = keys if isinstance(keys, str) else keys[(x * 7 + y * 3) % len(keys)]
                self.setg(x, y, k)
                if reserve:
                    self.blocked_tiles.add((x, y))

    def obj(self, name, otype, x, y, w, h, **props):
        o = {"id": self.oid, "name": name, "type": otype, "x": x, "y": y, "width": w, "height": h,
             "rotation": 0, "visible": True,
             "properties": [{"name": k, "type": "string", "value": str(v)} for k, v in props.items()]}
        self.oid += 1
        self.objects.append(o)
        return o

    def solid(self, x, y, w, h):
        self.collision.append({"id": self.oid, "name": "", "type": "solid", "x": x, "y": y, "width": w,
                               "height": h, "rotation": 0, "visible": True})
        self.oid += 1

    def reserve(self, x, y, w, h, pad=1):
        """Mark tiles under a building so trees are not scattered into it."""
        for ty in range(int(y // T) - pad, int((y + h) // T) + pad + 1):
            for tx in range(int(x // T) - pad, int((x + w) // T) + pad + 1):
                self.blocked_tiles.add((tx, ty))

    def building(self, name, sprite, tx, ty, w, h, foot_h, otype="prop", **props):
        """Places a sprite whose bottom `foot_h` pixels are solid."""
        x, y = tx * T, ty * T
        self.obj(name, otype, x, y, w, h, sprite=sprite, **props)
        self.solid(x + 2, y + h - foot_h, w - 4, foot_h)
        self.reserve(x, y, w, h)

    def npc(self, name, look, tx, ty, **props):
        self.obj(name, "npc", tx * T, ty * T, 16, 24, npc=look, **props)
        self.solid(tx * T + 2, ty * T + 14, 12, 10)
        self.reserve(tx * T, ty * T, 16, 24, pad=1)

    def tree(self, tx, ty, sprite="tree"):
        x, y = tx * T - 8, ty * T - 24
        self.obj("tree", "prop", x, y, 32, 40, sprite=sprite, variant=self.rng.randrange(1000))
        self.solid(x + 12, y + 32, 9, 7)

    def ring(self, sprite, gaps):
        """Border of trees/bamboo with openings; gaps = set of (side, tile index)."""
        W, H = self.W, self.H
        for x in range(0, W):
            for side, yy in (("n", 0), ("s", H - 1)):
                if (side, x) in gaps:
                    continue
                if sprite == "bamboo":
                    self.obj("bamboo", "prop", x * T, yy * T - 24 + (8 if side == "n" else -8), 16, 40,
                             sprite="bamboo", variant=x + (0 if side == "n" else 300))
                elif x % 2 == 0:
                    self.tree(x, 1 if side == "n" else H - 1, sprite)
        for y in range(1, H - 1):
            for side, xx in (("w", 0), ("e", W - 1)):
                if (side, y) in gaps:
                    continue
                if sprite == "bamboo":
                    self.obj("bamboo", "prop", xx * T, y * T - 24, 16, 40, sprite="bamboo",
                             variant=y + (600 if side == "w" else 900))
                elif y % 2 == 0:
                    self.tree(xx, y + 1, sprite)
        # border collision with the gaps left open
        def runs(side, n):
            start = None
            for i in range(n + 1):
                open_ = i == n or (side, i) in gaps
                if not open_ and start is None:
                    start = i
                if open_ and start is not None:
                    yield start, i
                    start = None
        for a, b in runs("n", W):
            self.solid(a * T, 0, (b - a) * T, T + 8)
        for a, b in runs("s", W):
            self.solid(a * T, (H - 1) * T - 4, (b - a) * T, T + 4)
        for a, b in runs("w", H):
            self.solid(0, a * T, T, (b - a) * T)
        for a, b in runs("e", H):
            self.solid((W - 1) * T, a * T, T, (b - a) * T)

    def scatter_trees(self, n, sprite="tree", area=None):
        x0, y0, x1, y1 = area or (2, 2, self.W - 3, self.H - 3)
        placed = 0
        for _ in range(n * 30):
            if placed >= n:
                break
            tx, ty = self.rng.randrange(x0, x1 + 1), self.rng.randrange(y0, y1 + 1)
            near = {(tx + dx, ty + dy) for dx in (-1, 0, 1) for dy in (-2, -1, 0, 1)}
            if near & self.blocked_tiles:
                continue
            self.tree(tx, ty, sprite)
            self.blocked_tiles |= near
            placed += 1

    # ---- Thiên Địa Đồ (2026-11-20): helpers of the lands of Luyện Khí
    def clear(self, x0, y0, x1, y1):
        """Takes away the trees and rocks whose foot stands in tiles x0..x1, y0..y1 (both
        inclusive) and their collision, so a road or a gate added after the scatter is free.
        The rest of the map keeps exactly the place it had."""
        keep, gone = [], []
        for o in self.objects:
            if o["type"] == "prop" and o["name"] in ("tree", "rock"):
                foot = ((o["x"] + o["width"] / 2) // T, (o["y"] + o["height"] - 1) // T)
                if x0 <= foot[0] <= x1 and y0 <= foot[1] <= y1:
                    gone.append(o)
                    continue
            keep.append(o)
        self.objects = keep
        marks = set()
        for o in gone:
            if o["name"] == "tree":
                marks.add((o["x"] + 12, o["y"] + 32, 9, 7))
            else:
                marks.add((o["x"] + 2, o["y"] + 4, 12, 8))
        self.collision = [c for c in self.collision if (c["x"], c["y"], c["width"], c["height"]) not in marks]

    def thing(self, name, sprite, tx, ty, w, h, foot=None, otype="prop", **props):
        """A prop whose rect's bottom-centre stands on the bottom-centre of tile (tx, ty);
        `foot` = (w, h) of the solid part at its base (None: walk-through)."""
        x, y = tx * T + T // 2 - w // 2, (ty + 1) * T - h
        o = self.obj(name, otype, x, y, w, h, sprite=sprite, **props)
        if foot:
            fw, fh = foot
            self.solid(tx * T + T // 2 - fw // 2, (ty + 1) * T - fh, fw, fh)
        self.blocked_tiles.add((tx, ty))
        return o

    def sign(self, name, text, tx, ty):
        self.obj(name, "sign", tx * T, ty * T, 16, 20, sprite="sign", text=text)
        self.solid(tx * T + 6, ty * T + 14, 4, 6)
        self.blocked_tiles.add((tx, ty))

    def water(self, tiles, bridges=()):
        """Water tiles, solid in runs along each row except where a bridge (wood) crosses."""
        bridges = set(bridges)
        for (x, y) in tiles:
            self.setg(x, y, "wood0" if (x, y) in bridges else "water0")
            self.blocked_tiles.add((x, y))
        wet = set(tiles) - bridges
        for y in sorted({y for _, y in wet}):
            xs = sorted(x for x, yy in wet if yy == y)
            start = prev = xs[0]
            for x in xs[1:] + [None]:
                if x is not None and x == prev + 1:
                    prev = x
                    continue
                self.solid(start * T, y * T, (prev - start + 1) * T, T)
                if x is not None:
                    start = prev = x

    def pit(self, tiles, key="ink0"):
        """Solid ground nobody walks on (a chasm, the deep): drawn as `key`, blocked in row runs."""
        for (x, y) in tiles:
            self.setg(x, y, key)
            self.blocked_tiles.add((x, y))
        for y in sorted({y for _, y in tiles}):
            xs = sorted(x for x, yy in tiles if yy == y)
            start = prev = xs[0]
            for x in xs[1:] + [None]:
                if x is not None and x == prev + 1:
                    prev = x
                    continue
                self.solid(start * T, y * T, (prev - start + 1) * T, T)
                if x is not None:
                    start = prev = x

    def gate(self, side, a, target, target_spawn, name="Cổng"):
        """A gate on the map's edge over tiles a..a+3 of that side (n, s, w, e)."""
        W, H = self.W, self.H
        if side == "n":
            self.obj(name, "prop", a * T, 0, 32, 40, sprite="portal")
            self.obj(f"to_{target}", "portal", a * T, -8, 4 * T, T + 10, target=target, target_spawn=target_spawn)
        elif side == "s":
            self.obj(name, "prop", a * T, (H - 2) * T - 8, 32, 40, sprite="portal")
            self.obj(f"to_{target}", "portal", a * T, (H - 1) * T - 2, 4 * T, T + 10, target=target,
                     target_spawn=target_spawn)
        elif side == "w":
            self.obj(name, "prop", 0, a * T - 8, 32, 40, sprite="portal")
            self.obj(f"to_{target}", "portal", -8, a * T, T + 12, 4 * T, target=target, target_spawn=target_spawn)
        else:
            self.obj(name, "prop", (W - 2) * T, a * T - 8, 32, 40, sprite="portal")
            self.obj(f"to_{target}", "portal", (W - 1) * T - 4, a * T, T + 12, 4 * T, target=target,
                     target_spawn=target_spawn)

    def build(self, extra_props: dict | None = None) -> dict:
        props = [{"name": "zone", "type": "string", "value": self.zone},
                 {"name": "name_vi", "type": "string", "value": self.name_vi}]
        for k, v in (extra_props or {}).items():
            props.append({"name": k, "type": "string", "value": str(v)})
        W, H = self.W, self.H
        return {
            "compressionlevel": -1, "height": H, "width": W, "infinite": False,
            "orientation": "orthogonal", "renderorder": "right-down", "tiledversion": "1.10.2",
            "tileheight": T, "tilewidth": T, "type": "map", "version": "1.10",
            "nextlayerid": 4, "nextobjectid": self.oid, "properties": props,
            "layers": [
                {"id": 1, "name": "ground", "type": "tilelayer", "width": W, "height": H, "x": 0, "y": 0,
                 "opacity": 1, "visible": True, "data": self.ground},
                {"id": 2, "name": "objects", "type": "objectgroup", "draworder": "topdown", "opacity": 1,
                 "visible": True, "x": 0, "y": 0, "objects": self.objects},
                {"id": 3, "name": "collision", "type": "objectgroup", "draworder": "topdown", "opacity": 1,
                 "visible": False, "x": 0, "y": 0, "objects": self.collision},
            ],
            "tilesets": [{"firstgid": 1, "name": "tiles", "image": "../sprites/tiles.png",
                          "imagewidth": 128, "imageheight": 16 * ((len(TILESET) + 7) // 8),
                          "tilewidth": T, "tileheight": T, "tilecount": len(TILESET), "columns": 8,
                          "margin": 0, "spacing": 0}],
        }


def village() -> dict:
    """Trúc Lâm Thôn: the safe hub (spec 7.1). Gate south -> abode, east -> Rừng Mực Loang."""
    m = MapBuilder("truc_lam_thon", "Trúc Lâm Thôn", 56, 36, "village")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.6 else "grass1" if r < 0.85 else
                   ("flowers0" if r > 0.98 else "flowers1" if r > 0.96 else "grass2"))
    south_gap = set(range(26, 30))
    east_gap = set(range(16, 20))
    west_gap = set(range(16, 20))
    north_gap = set(range(16, 20))        # M7: north to Loạn Số Cốc
    # roads and the square
    m.fill(26, 24, 29, H - 1, ["path0", "path1", "path0"])            # south road to the abode
    m.fill(36, 16, W - 1, 19, ["path0", "path1", "path0"])            # east road to the forest
    m.fill(26, 8, 29, 11, ["path0", "path1"])                         # north to Thiên Cơ Các
    m.fill(10, 16, 19, 19, ["path0", "path1"])                        # west to the market
    m.fill(16, 0, 19, 15, ["path0", "path1"])                         # M7: north to Loạn Số Cốc
    m.fill(0, 16, 9, 19, ["path0", "path1", "path0"])                 # stage 6: west road to Hồ Nghiên Mực
    m.fill(20, 12, 35, 23, ["plaza0", "plaza1"])                      # the square
    m.fill(30, 24, 31, 27, ["path0", "path1"])
    m.fill(32, 27, 45, 28, ["path0", "path1"])                        # to the Thủ Thành gate
    m.fill(8, 9, 11, 15, ["path0", "path1"])                          # to Trúc Lão's house
    m.fill(36, 10, 39, 15, ["path0", "path1"])                        # to the library
    # pond in the south-west corner
    for y in range(26, 31):
        for x in range(4, 11):
            m.setg(x, y, "water0")
    m.solid(4 * T, 26 * T, 7 * T, 5 * T)
    m.reserve(4 * T, 26 * T, 7 * T, 5 * T)
    # Thiên Địa Đồ (2026-11-20): four more gates, one per new land of Luyện Khí (roads after the scatter)
    land_gaps = ({("n", x) for x in range(45, 49)} | {("n", x) for x in range(2, 6)}
                 | {("w", y) for y in range(9, 13)} | {("e", y) for y in range(26, 30)})
    m.ring("bamboo", {("s", x) for x in south_gap} | {("e", y) for y in east_gap}
           | {("w", y) for y in west_gap} | {("n", x) for x in north_gap} | land_gaps)
    # buildings and service points (actions are handled by the client; spec 7.1)
    m.building("Thiên Cơ Các", "pavilion", 25, 3, 64, 64, 22, otype="interact", action="gacha")
    m.building("Tàng Thư Các", "library", 36, 4, 64, 56, 24, otype="interact", action="library")
    m.building("Nhà Trúc Lão", "hut", 6, 4, 64, 56, 30)
    m.npc("Trúc Lão", "truc_lao", 10, 8, action="talk_master")
    m.building("Sạp Tạp Hóa", "stall", 11, 13, 40, 32, 12, otype="interact", action="shop", variant=0)
    m.npc("Bà Chủ Sạp", "shopkeeper", 13, 11, action="shop")
    m.building("Sạp Vải", "stall", 11, 20, 40, 32, 12, otype="interact", action="cloth", variant=1)
    m.building("Lò Luyện Đan", "furnace", 16, 25, 24, 28, 14, otype="interact", action="alchemy")
    m.npc("Đan Sư", "alchemist", 14, 25, action="alchemy")
    m.building("Lò Rèn", "anvil", 21, 27, 24, 20, 10, otype="interact", action="forge")
    m.npc("Thợ Rèn", "smith", 23, 26, action="forge")
    m.building("Bảng Nhiệm Vụ", "board", 32, 10, 24, 28, 8, otype="interact", action="quests")
    m.building("Cổng Thủ Thành", "td_gate", 44, 24, 40, 40, 6, otype="interact", action="td")
    m.obj("Giếng", "prop", 27 * T + 4, 16 * T, 24, 24, sprite="well")
    m.solid(27 * T + 6, 16 * T + 12, 20, 12)
    m.npc("Tiểu Lan", "guide", 30, 29, action="talk_guide")
    m.npc("Thủ Thư", "librarian", 41, 9, action="library")
    for i, (tx, ty) in enumerate(((20, 12), (35, 12), (20, 23), (35, 23), (25, 24), (30, 24))):
        m.obj("lantern", "prop", tx * T + 4, ty * T - 16, 8, 24, sprite="lantern", variant=i)
        m.solid(tx * T + 6, ty * T + 4, 4, 4)
    for i, (tx, ty) in enumerate(((44, 6), (49, 10), (42, 31), (49, 31), (3, 19), (36, 30))):
        m.building("Nhà dân", "house", tx, ty, 48, 48, 20, variant=i)
    m.obj("sign", "prop", 33 * T, 18 * T - 4, 16, 20, sprite="sign")
    m.obj("Đi Mê Đồ Lâm", "sign", 52 * T, 14 * T, 16, 20, sprite="sign",
          text="Mê Đồ Lâm →")
    m.solid(52 * T + 6, 14 * T + 14, 4, 6)
    m.scatter_trees(26)
    # zone exits (server checks the player stands inside before moving them)
    m.obj("to_abode", "portal", 26 * T, (H - 1) * T - 2, 4 * T, T + 10, target="abode", target_spawn="spawn")
    m.obj("Cổng Đông", "prop", (W - 2) * T, 16 * T - 8, 32, 40, sprite="portal")
    m.obj("to_forest", "portal", (W - 1) * T - 4, 16 * T, T + 12, 4 * T, target="rung_muc_loang",
          target_spawn="from_village")
    m.obj("spawn", "spawn", 28 * T, 21 * T, 1, 1)
    m.obj("from_abode", "spawn", 28 * T, (H - 3) * T, 1, 1)
    m.obj("from_forest", "spawn", (W - 4) * T, 18 * T, 1, 1)
    # M7: the gate north to Loạn Số Cốc, where the mistakes themselves walk around
    m.obj("Cổng Bắc", "prop", 16 * T, 0, 32, 40, sprite="portal")
    m.obj("to_loan_so_coc", "portal", 16 * T, -8, 4 * T, T + 10, target="loan_so_coc",
          target_spawn="from_village")
    m.obj("Đi Kiếm Trủng Sơn", "sign", 20 * T, 3 * T, 16, 20, sprite="sign",
          text="↑ Kiếm Trủng Sơn")
    m.solid(20 * T + 6, 3 * T + 14, 4, 6)
    m.obj("from_loan_so_coc", "spawn", 17 * T, 3 * T, 1, 1)
    # stage 6: the pond can be fished (spec 11.1), the west gate leads to Hồ Nghiên Mực
    m.obj("pond", "area", 4 * T, 26 * T, 7 * T, 5 * T, kind="pond", pool="ao")
    m.obj("Cổng Tây", "prop", 0, 16 * T - 8, 32, 40, sprite="portal")
    m.obj("to_lake", "portal", -8, 16 * T, T + 12, 4 * T, target="ho_nghien_muc", target_spawn="from_village")
    m.obj("Đi Vạn Tượng Trạch", "sign", 3 * T, 14 * T, 16, 20, sprite="sign", text="← Vạn Tượng Trạch")
    m.solid(3 * T + 6, 14 * T + 14, 4, 6)
    m.obj("from_lake", "spawn", 3 * T, 18 * T, 1, 1)
    # stage 9: Cổng Bí Cảnh on the square (secret realms, spec 14)
    m.building("Cổng Bí Cảnh", "realm_gate", 21, 12, 40, 40, 6, otype="interact", action="realm")
    m.obj("from_realm", "spawn", 22 * T + 4, 16 * T + 4, 1, 1)
    village_lands(m)
    return m.build({"music": "village", "safe": "true"})


def village_lands(m: MapBuilder) -> None:
    """Thiên Địa Đồ (2026-11-20): the gates of the four new lands of Luyện Khí. Laid after the
    scatter, so every tree of the village keeps its place except the few on the new roads."""
    W = m.W
    # north-east: Lưu Vân Cốc
    m.clear(44, 0, 49, 15)
    m.fill(45, 0, 48, 4, ["path0", "path1"], reserve=False)
    m.fill(47, 5, 48, 15, ["path0", "path1"], reserve=False)
    m.gate("n", 45, "luu_van_coc", "from_village", "Cổng Mây")
    m.sign("Đi Lưu Vân Cốc", "↑ Lưu Vân Cốc", 44, 3)
    m.obj("from_luu_van_coc", "spawn", 47 * T, 3 * T, 1, 1)
    # north-west: Lôi Kiếp Đài, the trial at the end of the realm
    m.clear(0, 0, 6, 12)
    m.fill(2, 0, 5, 3, ["path0", "path1"], reserve=False)
    m.fill(2, 4, 4, 8, ["path0", "path1"], reserve=False)
    m.gate("n", 2, "loi_kiep_dai", "from_village", "Cổng Lôi")
    m.sign("Đi Lôi Kiếp Đài", "↑ Lôi Kiếp Đài", 6, 2)
    m.obj("from_loi_kiep_dai", "spawn", 3 * T + 8, 3 * T, 1, 1)
    # west, above the lake road: Thiên Công Phường
    m.fill(0, 9, 8, 11, ["path0", "path1", "path0"], reserve=False)
    m.gate("w", 9, "thien_cong_phuong", "from_village", "Cổng Thợ")
    m.sign("Đi Thiên Công Phường", "← Thiên Công Phường", 5, 12)
    m.obj("from_thien_cong_phuong", "spawn", 3 * T, 10 * T + 8, 1, 1)
    # east, past the Thủ Thành gate: Linh Xạ Nguyên
    m.clear(46, 25, W - 1, 30)
    m.fill(46, 27, W - 1, 28, ["path0", "path1"], reserve=False)
    m.gate("e", 26, "linh_xa_nguyen", "from_village", "Cổng Xạ")
    m.sign("Đi Linh Xạ Nguyên", "Linh Xạ Nguyên →", 52, 25)
    m.obj("from_linh_xa_nguyen", "spawn", (W - 4) * T, 28 * T, 1, 1)


def forest() -> dict:
    """Rừng Mực Loang: first zone with Mặc Quái (spec 7.1). West gate -> Trúc Lâm Thôn."""
    m = MapBuilder("rung_muc_loang", "Mê Đồ Lâm", 60, 40, "forest")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "dark_grass0" if r < 0.6 else "dark_grass1" if r < 0.96 else
                   ("ink0" if r > 0.985 else "ink1"))
    west_gap = set(range(18, 22))
    # a winding dirt trail
    y = 19
    for x in range(0, W - 6):
        if x % 6 == 0 and x > 4:
            ny = max(6, min(H - 9, y + m.rng.choice((-2, -1, 0, 1, 2))))
            m.fill(x, min(y, ny), x + 2, max(y, ny) + 2, "dirt0")
            y = ny
        m.fill(x, y, x, y + 2, "dirt0")
    for y in range(8, 30):  # side trail north-south
        m.fill(38, y, 39, y, "dirt0")
    # a clearing where the ink is thickest
    for yy in range(26, 33):
        for xx in range(42, 54):
            m.setg(xx, yy, "ink0" if m.rng.random() < 0.3 else "ink1" if m.rng.random() < 0.3 else "dark_grass0")
            m.blocked_tiles.add((xx, yy))
    m.ring("ink_tree", {("w", y) for y in west_gap})
    m.obj("Cổng Tây", "prop", 0, 18 * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", -8, 18 * T, T + 12, 4 * T, target="truc_lam_thon", target_spawn="from_forest")
    m.obj("Về Trúc Lâm Thôn", "sign", 3 * T, 15 * T, 16, 20, sprite="sign", text="← Trúc Lâm Thôn")
    m.solid(3 * T + 6, 15 * T + 14, 4, 6)
    m.reserve(0, 15 * T, 6 * T, 8 * T, pad=0)
    for i, (tx, ty) in enumerate(((14, 8), (30, 32), (52, 10), (24, 14))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # where the monsters roam (stage 3: they wander; Vấn Đạo combat comes in stage 4)
    m.obj("slimes_entrance", "monster_area", 12 * T, 14 * T, 14 * T, 12 * T, monster="ink_slime", count=6)
    m.obj("wisps_north", "monster_area", 30 * T, 4 * T, 18 * T, 10 * T, monster="tone_wisp", count=4)
    m.obj("clearing", "monster_area", 42 * T, 24 * T, 12 * T, 9 * T, monster="ink_slime", count=5)
    m.obj("clearing_wisps", "monster_area", 42 * T, 24 * T, 12 * T, 9 * T, monster="tone_wisp", count=2)
    m.obj("fox_den", "monster_area", 44 * T, 26 * T, 8 * T, 6 * T, monster="ink_fox", count=1)
    m.scatter_trees(45, "ink_tree")
    m.scatter_trees(15, "tree")
    m.obj("spawn", "spawn", 4 * T, 20 * T, 1, 1)
    m.obj("from_village", "spawn", 4 * T, 20 * T, 1, 1)
    maze_spots(m)
    return m.build({"music": "forest", "safe": "false"})


def lake() -> dict:
    """Hồ Nghiên Mực: the main fishing lake (spec 7.1, 11) with Ngư Ông on his dock and a few
    Mặc Quái on the shores. East gate -> Trúc Lâm Thôn."""
    m = MapBuilder("ho_nghien_muc", "Vạn Tượng Trạch", 56, 38, "lake")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.55 else "grass1" if r < 0.85 else
                   ("flowers1" if r > 0.97 else "grass2"))
    east_gap = set(range(17, 21))
    water = [(14, 7, 41, 25), (10, 12, 13, 19), (42, 10, 45, 16)]   # inclusive tile rects
    dock = (27, 19, 28, 26)
    for x0, y0, x1, y1 in water:   # stone shore first, water over it
        m.fill(x0 - 1, y0 - 1, x1 + 1, y1 + 1, "stone0")
    for x0, y0, x1, y1 in water:
        m.fill(x0, y0, x1, y1, "water0")
    m.fill(dock[0], dock[1], dock[2], dock[3], "wood0")
    # Thiên Địa Đồ: the misty island in the middle of the swamp, reached on a boardwalk from the
    # dock, and the islet of the old tree in the deep west water, on a plank from the shore
    walk = {(x, y) for x in (27, 28) for y in range(15, 19)} | {(x, y) for x in (29, 30, 31) for y in (15, 16)}
    island = {(x, y) for x in range(32, 36) for y in range(13, 18)}
    islet = {(x, y) for x in (11, 12) for y in (15, 16)} | {(10, 15), (10, 16)}
    for (x, y) in walk | {(10, 15), (10, 16)}:
        m.setg(x, y, "wood0")
    for (x, y) in island | islet - {(10, 15), (10, 16)}:
        m.setg(x, y, "stone0")
    wet = set()
    for x0, y0, x1, y1 in water:
        wet |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    wet -= walk | island | islet | {(x, y) for x in (27, 28) for y in range(dock[1], dock[3] + 1)}
    for y in sorted({y for _, y in wet}):     # the water is solid, row by row
        xs = sorted(x for x, yy in wet if yy == y)
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            m.solid(start * T, y * T, (prev - start + 1) * T, T)
            if x is not None:
                start = prev = x
    for i, (x0, y0, x1, y1) in enumerate(water):   # where a fishing line can go (server checks it)
        m.obj(f"lake_{i}", "area", x0 * T, y0 * T, (x1 - x0 + 1) * T, (y1 - y0 + 1) * T, kind="fishing", pool="ho")
    m.fill(29, 26, 50, 27, ["path0", "path1"])                         # shore path to the east gate
    m.fill(50, 17, W - 1, 20, ["path0", "path1", "path0"])
    m.fill(50, 21, 51, 27, ["path0", "path1"])
    m.building("Lều Ngư Ông", "hut", 18, 28, 64, 56, 30)
    m.npc("Ngư Ông", "fisher", 25, 27, action="fisher")
    m.obj("Bảng Ngư Phổ", "interact", 31 * T, 28 * T, 16, 24, sprite="tablet", action="fish_book")
    m.solid(31 * T + 2, 28 * T + 16, 12, 8)
    m.reserve(31 * T, 28 * T, 16, 24)
    for i, (tx, ty) in enumerate(((26, 26), (29, 26))):
        m.obj("lantern", "prop", tx * T + 4, ty * T - 16, 8, 24, sprite="lantern", variant=i)
    m.ring("tree", {("e", y) for y in east_gap})
    m.obj("Cổng Đông", "prop", (W - 2) * T, 17 * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", (W - 1) * T - 4, 17 * T, T + 12, 4 * T, target="truc_lam_thon",
          target_spawn="from_lake")
    m.obj("Về Trúc Lâm Thôn", "sign", 51 * T, 15 * T, 16, 20, sprite="sign", text="Trúc Lâm Thôn →")
    m.solid(51 * T + 6, 15 * T + 14, 4, 6)
    m.reserve(48 * T, 14 * T, 8 * T, 8 * T, pad=0)
    m.reserve(16 * T, 26 * T, 18 * T, 6 * T, pad=0)
    for i, (tx, ty) in enumerate(((8, 24), (47, 20), (12, 5))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # Mặc Quái along the shores, away from Ngư Ông's dock
    # Thiên Địa Đồ: the creatures of Xác Suất along the shores (Vạn Tượng Trạch)
    m.obj("oa_west", "monster_area", 2 * T, 22 * T, 10 * T, 12 * T, monster="dau_tu_oa", count=5)
    m.obj("ho_lo_north", "monster_area", 18 * T, 1 * T, 24 * T, 5 * T, monster="ho_lo_tinh", count=2)
    m.obj("oa_east", "monster_area", 46 * T, 26 * T, 8 * T, 9 * T, monster="dau_tu_oa", count=3)
    m.scatter_trees(34)
    swamp_spots(m)
    m.obj("spawn", "spawn", (W - 4) * T, 19 * T, 1, 1)
    m.obj("from_village", "spawn", (W - 4) * T, 19 * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


REALM_ROOM_W, REALM_ROOM_H = 22, 16
REALM_LAYOUT = (("compose", 0, 0), ("sentence", 1, 0), ("tone", 2, 0), ("mirror", 0, 1), ("maze", 1, 1), ("boss", 2, 1))


def math_valley() -> dict:
    """Loạn Số Cốc (M7): the valley where the mistakes themselves walk around. Three stretches,
    one per floor of Đại Số Tuyến Tính, so a player meets the mistakes of the floor they are on
    first. South gate -> Trúc Lâm Thôn; Lò Toán stands just inside the gate."""
    m = MapBuilder("loan_so_coc", "Kiếm Trủng Sơn", 56, 44, "loan_so_coc")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            # the floor is bare stone where the numbers fell apart, grass where it is still quiet
            if y < 14:
                m.setg(x, y, "stone0" if r < 0.7 else "ink1" if r < 0.9 else "dirt0")
            elif y < 29:
                m.setg(x, y, "dirt0" if r < 0.5 else "stone0" if r < 0.8 else "dark_grass0")
            else:
                m.setg(x, y, "dark_grass0" if r < 0.6 else "dark_grass1" if r < 0.93 else "dirt0")
    south_gap = set(range(26, 30))
    # the one road: it runs the length of the valley, floor 1 at the gate, floor 3 at the far end
    for y in range(2, H - 1):
        m.fill(27, y, 28, y, ["path0", "path1"], reserve=False)
    m.fill(20, 30, 35, 33, ["path0", "path1"], reserve=False)      # the clearing by the gate
    m.fill(18, 18, 37, 20, ["path0", "path1"], reserve=False)      # the middle crossing
    m.fill(16, 5, 39, 7, ["path0", "path1"], reserve=False)        # the far end
    m.ring("ink_tree", {("s", x) for x in south_gap})
    # Lò Toán: the furnace that turns what the mistakes drop into equipment (data/math/crafting.json)
    m.building("Lò Toán", "furnace", 22, 34, 24, 28, 14, otype="interact", action="math_craft")
    m.obj("Lò Toán", "sign", 20 * T, 35 * T, 16, 20, sprite="sign", text="Lò Toán")
    m.solid(20 * T + 6, 35 * T + 14, 4, 6)
    # M8: the Đạo Sĩ practising by the furnace is a character rendered out of Blender;
    # the client draws him from client/assets/chars/, and skips him when not rendered yet.
    m.obj("Đạo Sĩ Luyện Kiếm", "char", 33 * T, 34 * T, 16, 24, sheet="dao_si_truc_co", facing="down")
    m.obj("Bảng chỉ dẫn", "sign", 30 * T, 35 * T, 16, 20, sprite="sign",
          text="Tầng 1 gần cổng, tầng 3 cuối cốc")
    m.solid(30 * T + 6, 35 * T + 14, 4, 6)
    # rocks to break the sight lines
    for i, (tx, ty) in enumerate(((12, 26), (44, 24), (16, 10), (40, 9), (22, 16), (34, 38))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # floor 1 (tập hợp và ánh xạ): just inside the gate
    m.obj("t1_phan_tu", "monster_area", 8 * T, 29 * T, 16 * T, 11 * T, monster="dstt_phan_tu_ma", count=5)
    m.obj("t1_nghich_hieu", "monster_area", 32 * T, 29 * T, 16 * T, 11 * T,
          monster="dstt_nghich_hieu_ma", count=4)
    m.obj("t1_anh_trung", "monster_area", 20 * T, 24 * T, 14 * T, 6 * T, monster="dstt_anh_trung_ma", count=1)
    # floor 2 (số phức): the middle of the valley
    m.obj("t2_phan_ao", "monster_area", 6 * T, 15 * T, 18 * T, 10 * T, monster="dstt_phan_ao_ma", count=4)
    m.obj("t2_binh_phuong", "monster_area", 32 * T, 15 * T, 18 * T, 10 * T,
          monster="dstt_binh_phuong_ma", count=4)
    m.obj("t2_modun", "monster_area", 22 * T, 12 * T, 14 * T, 6 * T, monster="dstt_modun_ma", count=1)
    # floor 3 (vectơ và ma trận): the far end, where the stone is bare
    m.obj("t3_chi_so", "monster_area", 6 * T, 2 * T, 18 * T, 10 * T, monster="dstt_chi_so_ma", count=4)
    m.obj("t3_chuyen_vi", "monster_area", 32 * T, 2 * T, 18 * T, 10 * T, monster="dstt_chuyen_vi_ma", count=4)
    m.obj("t3_doi_xung", "monster_area", 20 * T, 2 * T, 16 * T, 6 * T, monster="dstt_doi_xung_ma", count=1)
    m.scatter_trees(34, "ink_tree")
    m.scatter_trees(12, "tree")
    sword_mountain_spots(m)
    # the way home
    m.obj("Cổng Nam", "prop", 26 * T, (H - 2) * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", 26 * T, (H - 1) * T - 2, 4 * T, T + 10, target="truc_lam_thon",
          target_spawn="from_loan_so_coc")
    m.obj("spawn", "spawn", 27 * T + 8, (H - 5) * T, 1, 1)
    m.obj("from_village", "spawn", 27 * T + 8, (H - 5) * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


def secret_realm() -> dict:
    """Bí cảnh (spec 14): six walled rooms, one per puzzle kind plus the boss's den. A run
    uses 3-5 of the puzzle rooms in a random order; the server moves the party from room to
    room (they are not joined by corridors). Puzzle props are `realm_obj` objects whose
    `kind` the server and the client both understand; their state is sent at run time."""
    RW, RH = REALM_ROOM_W, REALM_ROOM_H
    m = MapBuilder("bi_canh", "Bí Cảnh", RW * 3, RH * 2, "realm")

    def ro(kind, x, y, w, h, room, **props):
        m.obj(f"{room}_{kind}{props.get('n', props.get('slot', props.get('tone', '')))}", "realm_obj", x, y, w, h,
              kind=kind, room=room, **props)

    for room, col, row in REALM_LAYOUT:
        x0, y0 = col * RW, row * RH
        for y in range(y0, y0 + RH):
            for x in range(x0, x0 + RW):
                edge = x in (x0, x0 + RW - 1) or y in (y0, y0 + RH - 1)
                m.setg(x, y, "realm_wall0" if edge else ("realm_floor0" if (x + y) % 3 else "realm_floor1"))
        m.solid(x0 * T, y0 * T, RW * T, T + 6)
        m.solid(x0 * T, (y0 + RH - 1) * T - 2, RW * T, T + 2)
        m.solid(x0 * T, y0 * T, T, RH * T)
        m.solid((x0 + RW - 1) * T, y0 * T, T, RH * T)
        m.obj(room, "realm_room", (x0 + 1) * T, (y0 + 1) * T, (RW - 2) * T, (RH - 2) * T, kind=room)
        cx, cy = x0 + 11, y0 + 7
        entry = ((x0 + 11) * T, (y0 + RH - 3) * T + 8)
        exit_tile = (x0 + 10, y0 + 1)
        if room == "compose":
            for slot, (tx, ty) in (("top", (cx, cy - 3)), ("bottom", (cx, cy + 3)), ("left", (cx - 4, cy)),
                                   ("right", (cx + 4, cy))):
                ro("pedestal", tx * T - 4, ty * T - 4, 24, 24, room, slot=slot)
        elif room == "sentence":
            for i in range(1, 9):
                tx = cx - 7 + 2 * (i - 1)
                ro("tile", tx * T - 2, cy * T - 2, 20, 20, room, n=i)
        elif room == "tone":
            for tone, (tx, ty) in ((1, (cx - 5, cy - 3)), (2, (cx + 5, cy - 3)), (3, (cx - 5, cy + 3)),
                                   (4, (cx + 5, cy + 3))):
                ro("pillar", tx * T, ty * T - 16, 16, 32, room, tone=tone)
                m.solid(tx * T + 2, ty * T + 6, 12, 10)
            ro("statue", cx * T - 4, (cy - 2) * T, 24, 32, room)
            m.solid(cx * T - 2, (cy - 2) * T + 22, 20, 10)
        elif room == "mirror":
            ro("mirror", (cx - 1) * T, (cy - 4) * T, 3 * T, 2 * T, room)
        elif room == "maze":
            # a perfect maze on the interior: cells on odd sub-tiles, walls between them
            gw, gh = RW - 3, RH - 3                      # 19 x 13 sub-grid
            open_ = {(i, j) for i in range(1, gw, 2) for j in range(1, gh, 2)}
            seen, stack = {(1, gh - 2)}, [(1, gh - 2)]
            while stack:
                ci, cj = stack[-1]
                nxt = [(ci + di, cj + dj, di, dj) for di, dj in ((2, 0), (-2, 0), (0, 2), (0, -2))
                       if (ci + di, cj + dj) in open_ and (ci + di, cj + dj) not in seen]
                if not nxt:
                    stack.pop()
                    continue
                ni, nj, di, dj = m.rng.choice(nxt)
                open_.add((ci + di // 2, cj + dj // 2))
                seen.add((ni, nj))
                stack.append((ni, nj))
            open_ |= {(1, gh - 1), (1, gh), (gw - 2, 0)}  # the way in (bottom left) and out (top right)
            for j in range(RH - 2):
                run = None
                for i in range(RW - 1):
                    wall = i < RW - 2 and (i, j) not in open_
                    tx, ty = x0 + 1 + i, y0 + 1 + j
                    if wall:
                        m.setg(tx, ty, "realm_wall0")
                        if run is None:
                            run = i
                    elif run is not None:
                        m.solid((x0 + 1 + run) * T, ty * T, (i - run) * T, T)
                        run = None
            entry = ((x0 + 2) * T + 8, (y0 + RH - 2) * T + 12)
            exit_tile = (x0 + 1 + gw - 2, y0 + 1)
            ro("maze_exit", exit_tile[0] * T - 4, exit_tile[1] * T, T + 8, T + 4, room)
        elif room == "boss":
            ro("boss_spawn", cx * T, (cy - 3) * T, 16, 16, room)
            ro("chest", cx * T - 4, (cy - 1) * T, 24, 18, room)
        ro("exit", exit_tile[0] * T, exit_tile[1] * T - 8, 2 * T if room != "maze" else T, T + 8, room)
        m.obj(f"{room}_entry", "spawn", *entry, 1, 1)
    m.obj("spawn", "spawn", 11 * T, (RH - 3) * T + 8, 1, 1)
    return m.build({"music": "forest", "safe": "false", "dark": "true"})


# ------------------------------------------------------------------ Thiên Địa Đồ (2026-11-20)
# The lands of Luyện Khí (server/data/math/world_plan.json "lands"). Three reuse the old wild maps
# and get the spots where their weapons lie (`pos` in weapons_placed is a tile of these maps);
# four are new. Every new land is told apart by its ground, its border and its props, all of them
# tiles and props that already exist in client/assets/v2.
def swamp_spots(m: MapBuilder) -> None:
    """Vạn Tượng Trạch (ho_nghien_muc): the willow at the landing stage, the misty island, the
    sunken shrine on the north shore and the old tree on its islet in the deep west water."""
    m.clear(21, 25, 24, 27)
    m.tree(23, 26, "tree")                                   # the willow by Ngư Ông's dock
    m.thing("Sương", "cloud_puff", 33, 14, 32, 20, variant=0)
    m.thing("Sương", "cloud_puff", 35, 16, 32, 20, variant=1)
    m.thing("Đèn đảo", "lantern", 32, 16, 8, 24, variant=3)
    m.clear(36, 2, 40, 5)
    m.thing("Miếu Chìm", "shrine", 38, 4, 32, 44, foot=(28, 12))
    m.clear(10, 14, 13, 17)
    m.tree(12, 15, "tree")                                   # the old tree in the deep water


def maze_spots(m: MapBuilder) -> None:
    """Mê Đồ Lâm (rung_muc_loang): the fork, the dead end, the hollow of the mother tree and
    the lowest hollow of the forest, plus the creatures of Thuật Toán và Tối Ưu."""
    dirt = GID["dirt0"]
    rows = [y for y in range(m.H) if m.ground[y * m.W + 37] == dirt]
    fy = rows[len(rows) // 2]
    m.clear(35, fy - 3, 41, fy + 2)
    m.sign("Ngã ba", "Ngã ba: mỗi lối là một cạnh của đồ thị", 40, fy - 2)
    m.clear(36, 5, 41, 9)                                    # the dead end at the top of the side trail
    m.clear(48, 2, 57, 12)                                   # the mother tree and the ring around its hollow
    m.tree(53, 5, "tree")
    for tx, ty in ((50, 5), (51, 3), (55, 3), (56, 5), (56, 8), (50, 8), (51, 10), (55, 10)):
        m.tree(tx, ty, "ink_tree")
    m.obj("moc_yeu_hoc_cay", "monster_area", 49 * T, 3 * T, 9 * T, 9 * T, monster="moc_yeu", count=1)
    m.obj("tri_chu_bac", "monster_area", 14 * T, 3 * T, 12 * T, 9 * T, monster="tri_chu_tinh", count=4)
    m.obj("tri_chu_nam", "monster_area", 26 * T, 24 * T, 10 * T, 10 * T, monster="tri_chu_tinh", count=3)


def sword_mountain_spots(m: MapBuilder) -> None:
    """Kiếm Trủng Sơn (loan_so_coc): the stone tablet at the gate, the cave behind the falls,
    the field of broken swords and the peak beyond the chasm, plus Kiếm Linh, Thạch Khôi and
    Ma Trận Thú over the old stretches of the valley."""
    m.clear(23, 38, 26, 42)
    m.thing("Bia Kiếm", "tablet", 25, 40, 16, 24, foot=(12, 8))
    m.clear(1, 15, 9, 23)
    m.fill(3, 18, 6, 19, "stone0")                         # the cave behind the falls
    m.water({(x, y) for x in range(3, 7) for y in range(20, 23)})
    for tx in (3, 6):
        m.obj("rock", "prop", tx * T, 17 * T, 16, 12, sprite="rock", variant=tx)
        m.solid(tx * T + 2, 17 * T + 4, 12, 8)
    m.obj("thach_khoi_thac", "monster_area", 2 * T, 15 * T, 12 * T, 12 * T, monster="thach_khoi", count=3)
    m.clear(38, 8, 50, 14)
    for i, (tx, ty) in enumerate(((39, 9), (41, 12), (47, 12), (49, 9))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i + 7)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
    for tx, ty in ((42, 9), (46, 9), (44, 12)):
        m.thing("Mộ kiếm", "tablet", tx, ty, 16, 24, foot=(12, 8))
    m.obj("ma_tran_bai_kiem", "monster_area", 38 * T, 8 * T, 12 * T, 6 * T, monster="ma_tran_thu", count=1)
    m.clear(46, 1, 54, 7)
    peak = {(x, y) for x in range(50, 53) for y in range(2, 4)}
    m.pit({(x, y) for x in range(48, 55) for y in range(1, 6)} - peak, "ink0")
    m.fill(50, 2, 52, 3, "stone0")
    m.obj("kiem_linh_cong", "monster_area", 8 * T, 25 * T, 40 * T, 4 * T, monster="kiem_linh", count=4)


def cloud_valley() -> dict:
    """Lưu Vân Cốc (Giải Tích): a green valley crossed by one winding stream - a sine that falls
    out of a pool under the falls in the north - with a stone plateau, the highest crag of the
    valley, in the north-east. South gate -> Trúc Lâm Thôn."""
    import math as _m
    m = MapBuilder("luu_van_coc", "Lưu Vân Cốc", 60, 40, "luu_van_coc")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.6 else "grass1" if r < 0.88 else ("flowers1" if r > 0.97 else "grass2"))
    for y in range(1, 14):                    # the plateau: bare stone
        for x in range(38, 59):
            if (x - 49) ** 2 / 100 + (y - 7) ** 2 / 30 <= 1:
                m.setg(x, y, "stone0")
    south_gap = set(range(28, 32))
    # the trail: north from the gate, a branch west to the falls, east up to the plateau
    trail = {(x, y) for x in (29, 30) for y in range(7, H)}
    trail |= {(x, y) for x in range(24, 31) for y in (7, 8)}
    trail |= {(x, y) for x in range(31, 45) for y in (8, 9)}
    trail |= {(x, y) for x in range(6, 29) for y in (20, 21)}
    for (x, y) in trail:
        m.setg(x, y, "path0" if (x + y) % 3 else "path1")
    # the stream: x = 18 + 7 sin((y - 6) / 4.5), two tiles wide, then west out of the valley
    stream = set()
    for y in range(6, H - 6):
        cx = round(18 + 7 * _m.sin((y - 6) / 4.5))
        stream |= {(cx, y), (cx + 1, y)}
        if y > 6:
            px = round(18 + 7 * _m.sin((y - 7) / 4.5))
            for x in range(min(px, cx), max(px, cx) + 1):
                stream |= {(x, y), (x + 1, y)}
    for x in range(1, 16):
        stream |= {(x, H - 7), (x, H - 6)}
    pool = {(x, y) for x in range(17, 25) for y in range(2, 6)}
    ledge = {(20, 3), (21, 3)}                       # in the clouds above the falls
    wet = stream | pool
    for (x, y) in wet:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n not in wet and n not in trail and 0 < n[0] < W - 1 and 0 < n[1] < H - 1:
                    m.setg(n[0], n[1], "stone0")
    m.water(wet - ledge, stream & trail)
    for (x, y) in ledge:
        m.setg(x, y, "stone0")
    for (x, y) in trail:
        m.blocked_tiles.add((x, y))
    m.ring("pine", {("s", x) for x in south_gap})
    # the head of the stream: a boulder, and the clouds over the falls
    m.thing("Đá đầu suối", "boulder", 25, 6, 32, 24, foot=(26, 10))
    for i, (tx, ty) in enumerate(((19, 2), (22, 2), (21, 4), (18, 5))):
        m.thing("Mây", "cloud_puff", tx, ty, 32, 20, variant=i)
    # the highest crag: boulders around the top of the plateau
    for i, (tx, ty) in enumerate(((46, 5), (52, 5), (46, 9), (52, 9), (49, 3))):
        m.thing("Mỏm đá", "boulder", tx, ty, 32, 24, foot=(26, 10), variant=i)
    for i, (tx, ty) in enumerate(((42, 3), (56, 4), (40, 11), (57, 10))):
        m.thing("Mây", "cloud_puff", tx, ty, 32, 20, variant=i + 4)
    m.sign("Suối", "Suối uốn theo đường sin: khúc cong nhất là nơi đạo hàm đổi dấu", 32, 30)
    m.obj("van_xa_bac", "monster_area", 8 * T, 10 * T, 20 * T, 12 * T, monster="van_xa", count=5)
    m.obj("van_xa_nam", "monster_area", 4 * T, 22 * T, 24 * T, 9 * T, monster="van_xa", count=4)
    m.obj("phong_lang_dinh", "monster_area", 40 * T, 2 * T, 17 * T, 10 * T, monster="phong_lang", count=1)
    m.obj("phong_lang_dong", "monster_area", 38 * T, 18 * T, 16 * T, 12 * T, monster="phong_lang", count=1)
    m.reserve(26 * T, (H - 6) * T, 8 * T, 6 * T, pad=0)
    m.scatter_trees(30, "pine")
    m.scatter_trees(10, "tree")
    m.gate("s", 28, "truc_lam_thon", "from_luu_van_coc", "Cổng Nam")
    m.sign("Về Trúc Lâm Thôn", "↓ Trúc Lâm Thôn", 32, H - 4)
    m.obj("spawn", "spawn", 29 * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", 29 * T + 8, (H - 4) * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


def workshop() -> dict:
    """Thiên Công Phường (Lập Trình): an abandoned quarter of workshops on dirt and stone,
    plaza streets, a cold forge, a great furnace, a fenced gear yard and the yard where the
    leader of the Cơ Quan Nhân stands. East gate -> Trúc Lâm Thôn."""
    m = MapBuilder("thien_cong_phuong", "Thiên Công Phường", 56, 40, "thien_cong_phuong")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "dirt0" if r < 0.55 else "stone0" if r < 0.85 else "dark_grass0")
    east_gap = set(range(18, 22))
    m.fill(1, 18, W - 1, 21, ["plaza0", "plaza1"])              # the main street, from the gate
    m.fill(26, 2, 29, H - 3, ["plaza0", "plaza1"])              # the cross street
    m.fill(4, 3, 14, 8, ["stone0", "plaza1"])                   # the forge yard
    m.fill(37, 2, 48, 7, "stone0")                              # under the great furnace
    m.fill(36, 28, 50, 36, ["plaza0", "plaza1"])                # the leader's yard
    m.fill(4, 28, 16, 36, "wood0")                              # the gear yard's floor
    m.ring("ink_tree", {("e", y) for y in east_gap})
    for i, (tx, ty) in enumerate(((8, 13), (14, 13), (20, 13), (33, 13), (39, 13), (45, 13),
                                  (8, 23), (14, 23), (33, 23), (39, 23))):
        m.building("Xưởng", "house", tx, ty, 48, 48, 20, variant=i)
    # the cold forge: anvils and a dead furnace
    m.thing("Đe nguội", "anvil", 7, 5, 24, 20, foot=(20, 8))
    m.thing("Đe nguội", "anvil", 11, 5, 24, 20, foot=(20, 8))
    m.thing("Lò nguội", "furnace", 9, 3, 24, 28, foot=(18, 12))
    # the great furnace: three mouths side by side
    for tx in (41, 43, 45):
        m.thing("Lò Lớn", "furnace", tx, 4, 24, 28, foot=(20, 12))
    m.sign("Lò Lớn", "Lò Lớn: chỉ cháy lại khi đủ công lực", 39, 5)
    # the gear yard, behind its gate: a bamboo fence with one opening to the north
    for x in range(3, 18):
        if x in (9, 10, 11):
            continue
        m.obj("bamboo", "prop", x * T, 27 * T - 24, 16, 40, sprite="bamboo", variant=x + 400)
    for y in range(28, 38):
        for xx in (3, 17):
            m.obj("bamboo", "prop", xx * T, y * T - 24, 16, 40, sprite="bamboo", variant=y + 500 + xx)
    for x in range(4, 17):
        m.obj("bamboo", "prop", x * T, 37 * T - 24, 16, 40, sprite="bamboo", variant=x + 700)
    m.solid(3 * T, 27 * T, 6 * T, T)
    m.solid(12 * T, 27 * T, 6 * T, T)
    m.solid(3 * T, 27 * T, T, 11 * T)
    m.solid(17 * T, 27 * T, T, 11 * T)
    m.solid(3 * T, 37 * T, 15 * T, T)
    m.reserve(3 * T, 27 * T, 15 * T, 11 * T, pad=0)
    m.thing("Cơ Quan Cửa", "gate", 10, 27, 32, 32)
    for i, (tx, ty) in enumerate(((6, 30), (14, 30), (6, 35), (14, 35))):
        m.thing("Bánh xe gỗ", "log" if i % 2 else "stump", tx, ty, 24, 16, foot=(18, 8), variant=i)
    # the leader's yard
    for i, (tx, ty) in enumerate(((37, 29), (49, 29), (37, 35), (49, 35))):
        m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i)
    m.thing("Giếng", "well", 27, 25, 24, 24, foot=(20, 12))
    for i, tx in enumerate((4, 12, 20, 34, 42, 50)):
        m.thing("Đèn", "lantern", tx, 17, 8, 24, foot=(4, 4), variant=i + 4)
    m.thing("Sạp bỏ hoang", "stall", 21, 23, 40, 32, foot=(36, 12), variant=0)
    m.thing("Bảng thợ", "board", 50, 23, 24, 28, foot=(20, 8))
    m.obj("co_quan_tay", "monster_area", 2 * T, 15 * T, 20 * T, 10 * T, monster="co_quan_nhan", count=4)
    m.obj("co_quan_dong", "monster_area", 32 * T, 15 * T, 18 * T, 10 * T, monster="co_quan_nhan", count=3)
    m.obj("co_quan_bac", "monster_area", 16 * T, 2 * T, 20 * T, 8 * T, monster="co_quan_nhan", count=3)
    m.obj("co_quan_dau_dan", "monster_area", 38 * T, 29 * T, 11 * T, 7 * T, monster="co_quan_nhan_dau_dan",
          count=1)
    for i, (tx, ty) in enumerate(((22, 30), (31, 33), (52, 9), (20, 6), (33, 6))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    m.scatter_trees(12, "ink_tree")
    m.gate("e", 18, "truc_lam_thon", "from_thien_cong_phuong", "Cổng Đông")
    m.sign("Về Trúc Lâm Thôn", "Trúc Lâm Thôn →", W - 5, 16)
    m.obj("spawn", "spawn", (W - 4) * T, 20 * T, 1, 1)
    m.obj("from_village", "spawn", (W - 4) * T, 20 * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


def archery_plain() -> dict:
    """Linh Xạ Nguyên (Thực Chiến): a bright grassland of shooting lanes, two rows of stone
    targets, a bow rack at the start and the far field where one's own Tâm Ma waits. West
    gate -> Trúc Lâm Thôn."""
    m = MapBuilder("linh_xa_nguyen", "Linh Xạ Nguyên", 64, 36, "linh_xa_nguyen")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.5 else "flowers0" if r < 0.62 else "flowers1" if r < 0.72
                   else "grass1" if r < 0.94 else "grass2")
    west_gap = set(range(16, 20))
    m.fill(0, 16, 8, 19, ["path0", "path1"])
    for ly in (8, 17, 26):                                   # three shooting lanes
        m.fill(6, ly, 56, ly + 1, "dirt0")
    m.fill(50, 11, 60, 24, ["dirt0", "dark_grass0"])        # the far field
    m.ring("peach", {("w", y) for y in west_gap})
    m.thing("Giá Cung", "board", 8, 12, 24, 28, foot=(20, 8))
    for row_x in (30, 44):                                   # the two rows of targets
        for ty in (6, 11, 15, 20, 24, 29):
            m.thing("Bia bắn", "tablet", row_x, ty, 16, 24, foot=(12, 8))
    for i, (tx, ty) in enumerate(((9, 5), (9, 29), (52, 11), (58, 11), (52, 24), (58, 24))):
        m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i)
    m.sign("Trường bắn", "Nhắm, bắn, xem lệch bao nhiêu rồi chỉnh lại: đó là huấn luyện", 11, 14)
    m.obj("tam_ma_bac", "monster_area", 12 * T, 3 * T, 16 * T, 11 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_nam", "monster_area", 12 * T, 21 * T, 16 * T, 11 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_giua", "monster_area", 33 * T, 4 * T, 9 * T, 27 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_chap_niem", "monster_area", 51 * T, 12 * T, 9 * T, 12 * T, monster="tam_ma_chap_niem",
          count=1)
    rng = m.rng
    for i in range(40):                                     # tall grass and bushes, to walk through
        tx, ty = rng.randrange(3, W - 3), rng.randrange(3, H - 3)
        if (tx, ty) in m.blocked_tiles:
            continue
        m.thing("Cỏ", "tall_grass" if i % 3 else "bush", tx, ty, 24, 16, variant=i)
    m.scatter_trees(10, "peach")
    m.gate("w", 16, "truc_lam_thon", "from_linh_xa_nguyen", "Cổng Tây")
    m.sign("Về Trúc Lâm Thôn", "← Trúc Lâm Thôn", 3, 14)
    m.obj("spawn", "spawn", 4 * T, 18 * T, 1, 1)
    m.obj("from_village", "spawn", 4 * T, 18 * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


def tribulation_terrace() -> dict:
    """Lôi Kiếp Đài: the arena at the end of Luyện Khí. A round stone terrace on a dark plain,
    crystals around it, Thiên Kiếp Lôi Long in the middle. South gate -> Trúc Lâm Thôn."""
    import math as _m
    m = MapBuilder("loi_kiep_dai", "Lôi Kiếp Đài", 40, 30, "loi_kiep_dai")
    W, H = m.W, m.H
    cx, cy = 20, 13
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            r = m.rng.random()
            if d <= 7.5:
                m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
            elif d <= 9:
                m.setg(x, y, "plaza0" if r < 0.6 else "plaza1")
            else:
                m.setg(x, y, "ink0" if r < 0.45 else "ink1" if r < 0.85 else "dark_grass0")
    south_gap = set(range(18, 22))
    m.fill(19, 22, 20, H - 1, ["plaza0", "plaza1"])
    m.ring("ink_tree", {("s", x) for x in south_gap})
    for i in range(8):
        a = i * _m.pi / 4 + _m.pi / 8
        tx, ty = round(cx + 10.5 * _m.cos(a)), round(cy + 10.5 * _m.sin(a))
        m.thing("Lôi Tinh", "crystal", tx, ty, 24, 32, foot=(14, 8), variant=i)
    for i, ty in enumerate((24, 27)):
        for tx in (18, 21):
            m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i * 2 + tx)
    m.sign("Lôi Kiếp Đài", "Thiên Kiếp Luyện Khí: chỉ Phản Đòn mới phá được khiên của Lôi Long", 22, 23)
    m.obj("loi_long", "monster_area", (cx - 5) * T, (cy - 5) * T, 10 * T, 10 * T, monster="loi_long", count=1)
    m.reserve((cx - 9) * T, (cy - 9) * T, 18 * T, 18 * T, pad=0)
    m.scatter_trees(10, "ink_tree")
    m.gate("s", 18, "truc_lam_thon", "from_loi_kiep_dai", "Cổng Nam")
    m.obj("spawn", "spawn", 19 * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", 19 * T + 8, (H - 4) * T, 1, 1)
    return m.build({"music": "forest", "safe": "false"})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    server_maps = ROOT / "server" / "maps"
    server_maps.mkdir(parents=True, exist_ok=True)
    for name, fn in (("abode", abode), ("truc_lam_thon", village), ("rung_muc_loang", forest),
                     ("ho_nghien_muc", lake), ("loan_so_coc", math_valley),
                     ("bi_canh", secret_realm), ("luu_van_coc", cloud_valley),
                     ("thien_cong_phuong", workshop), ("linh_xa_nguyen", archery_plain),
                     ("loi_kiep_dai", tribulation_terrace)):
        m = fn()
        data = json.dumps(m, ensure_ascii=False, indent=1).encode("utf-8")   # LF on every OS
        (OUT / f"{name}.tmj").write_bytes(data)
        (server_maps / f"{name}.tmj").write_bytes(data)
        print("wrote", (OUT / f"{name}.tmj").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
