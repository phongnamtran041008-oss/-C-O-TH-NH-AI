"""The map builder every land shares: a ground grid of TILESET keys, objects and collision
rectangles, written as Tiled JSON 1.10 (open them in https://www.mapeditor.org).

Tile ids refer to client/assets/sprites/tiles.png (written by tools/gen_sprites.py); props and
areas are rectangle objects whose `sprite`/`kind` property the client understands. The toolkit
for the giant lands (Đại Địa Đồ) builds on this class: tools/mapgen/giant.py.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from client.art.build import TILESET  # noqa: E402

T = 16
GID = {f"{n}{v}": i + 1 for i, (n, v) in enumerate(TILESET)}


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
