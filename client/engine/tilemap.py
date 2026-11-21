"""Loads Tiled JSON maps (.tmj) and draws them (spec 2: maps made in Tiled).

Built for the giant lands of Đại Địa Đồ (320 x 240 tiles) as much as for the small maps:

* **The ground in chunks.** Nothing holds a picture of the whole map. The ground is cut into
  square chunks of CHUNK_PX screen pixels (32 tiles at 16 px, 16 tiles at 32 px - the 2x
  autotiled ground of the v2 art), each built the first time it comes near the view and kept
  in one cache shared by every map and both zooms, bounded by CACHE_BYTES (least recently
  drawn chunks go first). A chunk is built cell by cell exactly as the old whole-map surface
  was, so the picture is the same pixel for pixel (client/tests/test_giant_map_units.py
  renders whole maps both ways). After each draw the chunks round the view - those the camera
  moves toward first - are built ahead within BUILD_BUDGET_S, and a chunk can be left half
  built and finished on a later frame, so walking never waits for a whole row of chunks.
* **Water** ripples only on the cells of the chunks on screen (each chunk keeps its own list).
* **Objects in buckets.** The objects that can be drawn, the ones a player can talk to and
  the solids are put in spatial buckets once per map; the world scene asks for what is near
  the view (`drawables_in`, `interactables_near`) instead of walking every object. Objects of
  a type that is only data (`khu`, `poi`: Đại Địa Đồ, server/app/realtime/dia_do.py) are never
  drawn, picked or collided with.
* `load_map` keeps the last MAX_MAPS maps, not every map ever visited.
"""
from __future__ import annotations

import itertools
import json
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

import pygame

from ..art import build as B
from . import autotile

CHUNK_PX = 512                  # side of a ground chunk in screen pixels, at either zoom
CACHE_BYTES = 24 * 2 ** 20      # every ground chunk of every map, both zooms (24 chunks of 512 x 512)
BUILD_BUDGET_S = 0.003          # building ahead after a frame: at most this long
BUCKET = 256                    # world pixels: the side of an object bucket
MAX_MAPS = 4                    # maps load_map keeps (the abode, the village, the land, one more)
NEVER_DRAWN = frozenset({"khu", "poi"})      # rectangles with properties only: never drawn or picked
INTERACT_TYPES = ("npc", "interact", "sign")


@dataclass
class MapObject:
    id: int
    name: str
    type: str
    x: float
    y: float
    w: float
    h: float
    props: dict = field(default_factory=dict)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    @property
    def foot_y(self) -> float:
        return self.y + self.h


def can_draw(o: MapObject) -> bool:
    """Can the world draw anything for this object? (a prop or sign with its sprite, an NPC, a
    Blender character); the world's cull test then decides whether it is on screen."""
    if o.type in NEVER_DRAWN:
        return False
    return bool(o.props.get("sprite")) or o.type in ("npc", "char")


# ------------------------------------------------------------------ the chunk cache
class _Chunk:
    __slots__ = ("surf", "water", "cell", "done", "nbytes", "auto")

    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.water: list = []        # (x, y) tiles of the cells that ripple
        self.cell = 0                # the next cell to build (row by row inside the chunk)
        self.done = False
        self.auto = 0                # cells drawn with transition tiles (the 2x ground)
        self.nbytes = surf.get_width() * surf.get_height() * surf.get_bytesize()


_CACHE: OrderedDict = OrderedDict()     # (map uid, zoom, cx, cy) -> _Chunk
STATS = {"build_s": 0.0, "cells": 0, "chunks": 0}     # ground building so far (tools/bench_giant_map.py)
_cache_bytes = 0
_UIDS = itertools.count(1)


def _cache_put(key, chunk: _Chunk) -> None:
    global _cache_bytes
    _CACHE[key] = chunk
    _cache_bytes += chunk.nbytes
    while _cache_bytes > CACHE_BYTES and len(_CACHE) > 1:
        _k, old = _CACHE.popitem(last=False)
        _cache_bytes -= old.nbytes


def _cache_drop(uid: int) -> None:
    global _cache_bytes
    for k in [k for k in _CACHE if k[0] == uid]:
        _cache_bytes -= _CACHE.pop(k).nbytes


def cache_bytes() -> int:
    """Bytes of ground pixels held right now, all maps."""
    return _cache_bytes


def ground_bytes(tm: "TileMap") -> int:
    """Bytes of ground pixels held for one map (its chunks, and the whole-map picture of
    ground32() if a test or tool asked for it)."""
    n = sum(c.nbytes for k, c in _CACHE.items() if k[0] == tm.uid)
    g = getattr(tm, "_g32", None)
    if g is not None:
        n += g.get_width() * g.get_height() * g.get_bytesize()
    return n


class _Buckets:
    """Objects in square buckets of BUCKET world pixels, each object in every bucket its
    rectangle (or point) touches. Queries give the objects in map order."""

    def __init__(self):
        self.cells: dict[tuple[int, int], list] = {}
        self._last = (None, [])

    def add(self, i: int, o, x0: float, y0: float, x1: float, y1: float) -> None:
        for by in range(int(y0 // BUCKET), int(y1 // BUCKET) + 1):
            for bx in range(int(x0 // BUCKET), int(x1 // BUCKET) + 1):
                self.cells.setdefault((bx, by), []).append((i, o))

    def query(self, x0: float, y0: float, x1: float, y1: float) -> list:
        key = (int(x0 // BUCKET), int(y0 // BUCKET), int(x1 // BUCKET), int(y1 // BUCKET))
        if key == self._last[0]:
            return self._last[1]
        found: dict = {}
        for by in range(key[1], key[3] + 1):
            for bx in range(key[0], key[2] + 1):
                for i, o in self.cells.get((bx, by), ()):
                    found[i] = o
        out = [found[i] for i in sorted(found)]
        self._last = (key, out)
        return out


class TileMap:
    def __init__(self, path: Path):
        data = json.loads(Path(path).read_text("utf-8"))
        self.uid = next(_UIDS)
        self.w, self.h = data["width"], data["height"]
        self.tw, self.th = data["tilewidth"], data["tileheight"]
        self.props = {p["name"]: p["value"] for p in data.get("properties", [])}
        self.ground: list[int] = []
        self.objects: list[MapObject] = []
        self.solids: list[pygame.Rect] = []
        for layer in data["layers"]:
            if layer["type"] == "tilelayer" and layer["name"] == "ground":
                self.ground = layer["data"]
            elif layer["type"] == "objectgroup":
                for o in layer["objects"]:
                    props = {p["name"]: p["value"] for p in o.get("properties", [])}
                    mo = MapObject(o["id"], o.get("name", ""), o.get("type", ""), o["x"], o["y"],
                                   o["width"], o["height"], props)
                    if layer["name"] == "collision":
                        self.solids.append(mo.rect)
                    else:
                        self.objects.append(mo)
        self.px_w, self.px_h = self.w * self.tw, self.h * self.th
        self._water_gid = next(i + 1 for i, (n, _) in enumerate(B.TILESET) if n == "water")
        from . import art2
        v2 = art2.tileset(len(B.TILESET)) if art2.on() else None
        self._v2 = v2
        if v2 is not None:          # the Blender tileset: same tiles, same order (gid = index + 1)
            self._tiles = {i + 1: t for i, t in enumerate(v2.tiles)}
            self._water_frames = list(v2.water) or [self._tiles[self._water_gid]]
            self._water_fps = v2.water_fps
        else:
            self._tiles = {i + 1: B.tile(n, v) for i, (n, v) in enumerate(B.TILESET)}
            self._water_frames = [B.tile("water", 0, f) for f in range(4)]
            self._water_fps = 2.0
        self._ts32 = None           # the 2x tiles (v2 art), looked up the first time they are needed
        self._ts32_tried = False
        self.autotiled = 0          # cells of the 2x ground drawn with transition tiles (built so far)
        self._seen32: set = set()   # 2x chunks counted in `autotiled` already
        self._ahead: tuple | None = None    # (zoom, camera x, camera y) of the last draw: the walking direction
        self._index()

    # ------------------------------------------------------------ objects
    def _index(self) -> None:
        self._by_type: dict[str, list[MapObject]] = {}
        self._draw = _Buckets()
        self._talk = _Buckets()
        for i, o in enumerate(self.objects):
            self._by_type.setdefault(o.type, []).append(o)
            if can_draw(o):
                self._draw.add(i, o, o.x, o.y, o.x + o.w, o.y + o.h)
            if o.type in INTERACT_TYPES:
                ax, ay = o.x + o.w / 2, o.y + o.h
                self._talk.add(i, o, ax, ay, ax, ay)
        self._grid: dict[tuple[int, int], list[pygame.Rect]] = {}
        for r in self.solids:
            for gy in range(r.y // 64, (r.y + r.h) // 64 + 1):
                for gx in range(r.x // 64, (r.x + r.w) // 64 + 1):
                    self._grid.setdefault((gx, gy), []).append(r)
        self._collider = None

    def find(self, otype: str | None = None, name: str | None = None) -> list[MapObject]:
        objs = self.objects if otype is None else self._by_type.get(otype, [])
        return [o for o in objs if name is None or o.name == name]

    def drawables_in(self, x0: float, y0: float, x1: float, y1: float) -> list[MapObject]:
        """The objects that can be drawn and whose rectangle may touch the world rect
        [x0, x1] x [y0, y1], in map order (a superset: the caller keeps its own exact test)."""
        return self._draw.query(x0, y0, x1, y1)

    def interactables_near(self, x: float, y: float, r: float) -> list[MapObject]:
        """NPCs, signs and interact objects whose foot point (bottom centre) may lie within r
        of (x, y), in map order (a superset)."""
        return self._talk.query(x - r, y - r, x + r, y + r)

    def collider(self):
        """The movement collider of this map (engine/movement.py, a grid like the server's),
        built once."""
        if self._collider is None:
            from . import movement as mv
            self._collider = mv.Collider(self.px_w, self.px_h, [(r.x, r.y, r.w, r.h) for r in self.solids])
        return self._collider

    def blocked(self, r: pygame.Rect) -> bool:
        if r.left < 0 or r.top < 0 or r.right > self.px_w or r.bottom > self.px_h:
            return True
        near: dict = {}
        for gy in range(r.y // 64, (r.y + r.h) // 64 + 1):
            for gx in range(r.x // 64, (r.x + r.w) // 64 + 1):
                for s in self._grid.get((gx, gy), ()):
                    near[id(s)] = s
        return bool(near) and r.collidelist(list(near.values())) != -1

    # ------------------------------------------------------------ the 2x tiles
    def _tiles32(self):
        """(tileset32, terrain, autotile rules, tile names) of the v2 art, or None."""
        if not self._ts32_tried:
            self._ts32_tried = True
            from . import art2
            ts = art2.tileset32(len(B.TILESET)) if art2.on() else None
            if ts is not None:
                terrain, _native = art2.terrain32()
                rules = art2.wiring().get("autotile") or {}
                self._ts32 = (ts, terrain, rules, [n for n, _ in B.TILESET])
                self._water32 = list(ts.water) or None
                self._water32_fps = ts.water_fps
        return self._ts32

    @property
    def water_cells(self) -> list:
        """Every water tile (x, y) of the map (tests and tools; the drawing uses the chunks')."""
        return [(i % self.w, i // self.w) for i, g in enumerate(self.ground) if g == self._water_gid]

    # ------------------------------------------------------------ chunks
    def _span(self, zoom: int) -> int:
        """Tiles per chunk side at this zoom."""
        return max(1, CHUNK_PX // (self.tw * zoom))

    def _chunk(self, zoom: int, cx: int, cy: int, finish: bool = True, deadline: float | None = None) -> _Chunk:
        key = (self.uid, zoom, cx, cy)
        ch = _CACHE.get(key)
        if ch is None:
            n = self._span(zoom)
            tw, th = min(n, self.w - cx * n), min(n, self.h - cy * n)
            ch = _Chunk(pygame.Surface((tw * self.tw * zoom, th * self.th * zoom)))
            _cache_put(key, ch)
        else:
            _CACHE.move_to_end(key)
        if not ch.done:
            self._build(ch, zoom, cx, cy, None if finish else deadline)
        return ch

    def _build(self, ch: _Chunk, zoom: int, cx: int, cy: int, deadline: float | None) -> None:
        n = self._span(zoom)
        x0, y0 = cx * n, cy * n
        cw, chh = min(n, self.w - x0), min(n, self.h - y0)
        total = cw * chh
        if zoom != 1 and self._tiles32() is None:
            raise ValueError("no 2x ground without the v2 tiles")
        cell = self._cell16 if zoom == 1 else self._cell32
        t0 = time.perf_counter()
        start = ch.cell
        try:
            while ch.cell < total:
                k = ch.cell
                cell(ch, x0 + k % cw, y0 + k // cw, x0, y0)
                ch.cell = k + 1
                if deadline is not None and (k & 15) == 15 and time.perf_counter() > deadline:
                    return
        finally:
            STATS["build_s"] += time.perf_counter() - t0
            STATS["cells"] += ch.cell - start
        ch.done = True
        STATS["chunks"] += 1
        if zoom == 2 and (cx, cy) not in self._seen32:     # counted once, however often it is rebuilt
            self._seen32.add((cx, cy))
            self.autotiled += ch.auto

    def _cell16(self, ch: _Chunk, x: int, y: int, x0: int, y0: int) -> None:
        """One cell of the 16 px ground, as the old whole-map surface drew it."""
        gid = self.ground[y * self.w + x]
        t = self._tiles.get(gid)
        if t is not None and self._v2 is not None:      # stone / plaza have extra variants: vary them
            t = self._v2.pick(gid - 1, x, y)
        if t:
            ch.surf.blit(t, ((x - x0) * self.tw, (y - y0) * self.th))
        if gid == self._water_gid:
            ch.water.append((x, y))

    def _cell32(self, ch: _Chunk, x: int, y: int, x0: int, y0: int) -> None:
        """One cell of the 2x autotiled ground (soft path edges, shores, round dirt patches)."""
        ts, terrain, rules, names = self._ts32
        w, h, g = self.w, self.h, self.ground
        gid = g[y * w + x]
        if not 0 < gid <= len(names):
            return

        def cls(cx, cy):
            v = g[cy * w + cx]
            return names[v - 1] if 0 < v <= len(names) else None
        tile = ts.pick(gid - 1, x, y)
        rule = rules.get(names[gid - 1])
        outer = set(rule.get("outer", [])) if isinstance(rule, dict) else None
        pieces = autotile.cell_pieces(cls, x, y, w, h, outer) if outer else (None,) * 4
        shape = autotile.whole(cls, x, y, w, h, outer) if outer else None
        special = terrain.get(f"{rule['pair']}_{shape}") if shape else None
        if special or any(pieces):
            # the ground round it (the commonest outer neighbour) shows through the
            # transition's grass, so a dirt patch on dark grass is ringed by dark grass
            near = [g[ny * w + nx] for nx, ny in ((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                    if 0 <= nx < w and 0 <= ny < h and cls(nx, ny) in outer]
            og = max(set(near), key=near.count) if near else None
            painted = rule.get("painted", "grass")
            same = og is None or names[og - 1] == painted or (
                painted == "grass" and names[og - 1] in ("grass", "flowers"))
            # only a sheet painted with grass can have its grass swapped for another ground
            under = ts.pick(og - 1, x, y) if (not same and painted == "grass") else None
            whole_tile = special[(x * 3 + y) % len(special)] if special else None
            tile, _ok = autotile.compose(tile, pieces, terrain, rule["pair"], x * 3 + y, under, whole_tile)
            ch.auto += 1
        elif gid == self._water_gid:
            ch.water.append((x, y))             # water with no shore: it ripples
        ch.surf.blit(tile, ((x - x0) * 32, (y - y0) * 32))

    def _range(self, zoom: int, ox: int, oy: int, sw: int, sh: int) -> tuple[int, int, int, int]:
        """The chunks (inclusive) a sw x sh view with its top-left at screen pixel (ox, oy) shows."""
        n = self._span(zoom)
        size_x, size_y = n * self.tw * zoom, n * self.th * zoom
        ncx, ncy = -(-self.w // n), -(-self.h // n)
        return (max(0, ox // size_x), max(0, oy // size_y),
                min(ncx - 1, (ox + sw - 1) // size_x), min(ncy - 1, (oy + sh - 1) // size_y))

    def _draw_chunks(self, target: pygame.Surface, zoom: int, ox: int, oy: int, t: float) -> None:
        sw, sh = target.get_size()
        n = self._span(zoom)
        size_x, size_y = n * self.tw * zoom, n * self.th * zoom
        cx0, cy0, cx1, cy1 = self._range(zoom, ox, oy, sw, sh)
        shown = []
        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                ch = self._chunk(zoom, cx, cy)
                target.blit(ch.surf, (cx * size_x - ox, cy * size_y - oy))
                shown.append(ch)
        if zoom == 1:
            frames, fps, ts = self._water_frames, self._water_fps, self.tw
        else:
            frames, fps, ts = self._water32, self._water32_fps, 32
        if frames:
            frame = frames[int(t * fps) % len(frames)]
            for ch in shown:
                for x, y in ch.water:
                    px, py = x * ts - ox, y * ts - oy
                    if -ts < px < sw and -ts < py < sh:
                        target.blit(frame, (px, py))
        self._build_ahead(zoom, ox, oy, sw, sh, (cx0, cy0, cx1, cy1))

    def _build_ahead(self, zoom: int, ox: int, oy: int, sw: int, sh: int, shown: tuple) -> None:
        """Build the chunks round the view, those the camera moves toward first, for at most
        BUILD_BUDGET_S (a chunk may be left half built: the next frame goes on with it)."""
        last, self._ahead = self._ahead, (zoom, ox, oy)
        if sw * sh > 4 * CHUNK_PX * CHUNK_PX:          # a whole-map picture (an overview): nothing ahead
            return
        mx = my = 0
        if last is not None and last[0] == zoom:
            mx, my = ox - last[1], oy - last[2]
        cx0, cy0, cx1, cy1 = shown
        n = self._span(zoom)
        ncx, ncy = -(-self.w // n), -(-self.h // n)
        todo = []
        for cy in range(max(0, cy0 - 1), min(ncy - 1, cy1 + 1) + 1):
            for cx in range(max(0, cx0 - 1), min(ncx - 1, cx1 + 1) + 1):
                if cx0 <= cx <= cx1 and cy0 <= cy <= cy1:
                    continue
                key = (self.uid, zoom, cx, cy)
                c = _CACHE.get(key)
                if c is not None and c.done:
                    continue
                dx = -1 if cx < cx0 else (1 if cx > cx1 else 0)
                dy = -1 if cy < cy0 else (1 if cy > cy1 else 0)
                todo.append((-(dx * mx + dy * my), abs(dx) + abs(dy), cy, cx))
        if not todo:
            return
        todo.sort()
        deadline = time.perf_counter() + BUILD_BUDGET_S
        for _ahead, _d, cy, cx in todo:
            self._chunk(zoom, cx, cy, finish=False, deadline=deadline)
            if time.perf_counter() > deadline:
                return

    # ------------------------------------------------------------ the 2x ground (v2 art)
    def has_ground32(self) -> bool:
        return self._tiles32() is not None

    def ground32(self) -> pygame.Surface | None:
        """The whole 2x autotiled ground as one surface, None without the v2 tiles. For tests
        and tools only: a giant map's would be hundreds of MB; the drawing uses the chunks."""
        if getattr(self, "_g32", None) is None:
            if self._tiles32() is None:
                return None
            surf = pygame.Surface((self.w * 32, self.h * 32))
            n = self._span(2)
            for cy in range(-(-self.h // n)):
                for cx in range(-(-self.w // n)):
                    surf.blit(self._chunk(2, cx, cy).surf, (cx * n * 32, cy * n * 32))
            self._g32 = surf
        return self._g32

    def draw_ground_view(self, target: pygame.Surface, view, t: float) -> None:
        """The ground through a View: the 16 px ground at zoom 1, the autotiled 32 px one at 2."""
        if view.zoom != 2 or self._tiles32() is None:
            self.draw_ground(target, (view.ox, view.oy), t)
            return
        self._draw_chunks(target, 2, view.ox, view.oy, t)

    def draw_ground(self, target: pygame.Surface, cam: tuple[int, int], t: float) -> None:
        self._draw_chunks(target, 1, int(cam[0]), int(cam[1]), t)

    def release(self) -> None:
        """Drop this map's ground chunks (it left load_map's cache)."""
        _cache_drop(self.uid)
        self._g32 = None


_MAPS: OrderedDict = OrderedDict()


def load_map(name: str) -> TileMap:
    from ..config import assets_dir
    m = _MAPS.get(name)
    if m is None:
        m = _MAPS[name] = TileMap(assets_dir() / "maps" / f"{name}.tmj")
        while len(_MAPS) > MAX_MAPS:
            _MAPS.popitem(last=False)[1].release()
    else:
        _MAPS.move_to_end(name)
    return m
