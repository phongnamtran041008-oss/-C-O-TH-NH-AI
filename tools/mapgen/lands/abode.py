"""Động Phủ: the abode, laid out by code."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "abode"


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


build = abode
