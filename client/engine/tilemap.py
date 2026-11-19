"""Loads Tiled JSON maps (.tmj) and draws them (spec 2: maps made in Tiled)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pygame

from ..art import build as B


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


class TileMap:
    def __init__(self, path: Path):
        data = json.loads(Path(path).read_text("utf-8"))
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
        if v2 is not None:          # the Blender tileset: same tiles, same order (gid = index + 1)
            self._tiles = {i + 1: t for i, t in enumerate(v2.tiles)}
            self._water_frames = list(v2.water) or [self._tiles[self._water_gid]]
            self._water_fps = v2.water_fps
        else:
            self._tiles = {i + 1: B.tile(n, v) for i, (n, v) in enumerate(B.TILESET)}
            self._water_frames = [B.tile("water", 0, f) for f in range(4)]
            self._water_fps = 2.0
        self.water_cells = [(i % self.w, i // self.w) for i, g in enumerate(self.ground) if g == self._water_gid]
        self.surface = pygame.Surface((self.px_w, self.px_h))
        for i, gid in enumerate(self.ground):
            t = self._tiles.get(gid)
            if t is not None and v2 is not None:      # stone / plaza have extra variants: vary them
                t = v2.pick(gid - 1, i % self.w, i // self.w)
            if t:
                self.surface.blit(t, ((i % self.w) * self.tw, (i // self.w) * self.th))

    # ------------------------------------------------------------ the 2x ground (v2 art)
    def ground32(self) -> pygame.Surface | None:
        """The ground at 32 px per tile, autotiled (soft path edges, shores, round dirt patches),
        built once; None without the v2 tiles."""
        if getattr(self, "_g32", None) is None and not getattr(self, "_g32_tried", False):
            self._g32_tried = True
            from . import art2, autotile
            ts = art2.tileset32(len(B.TILESET)) if art2.on() else None
            if ts is None:
                return None
            terrain, _native = art2.terrain32()
            rules = art2.wiring().get("autotile") or {}
            names = [n for n, _ in B.TILESET]
            w, h, g = self.w, self.h, self.ground

            def cls(x, y):
                gid = g[y * w + x]
                return names[gid - 1] if 0 < gid <= len(names) else None
            surf = pygame.Surface((w * 32, h * 32))
            self.water_open: list = []              # water cells with no shore: these ripple
            self.autotiled = 0
            for i, gid in enumerate(g):
                if not 0 < gid <= len(names):
                    continue
                x, y = i % w, i // w
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
                    self.autotiled += 1
                elif gid == self._water_gid:
                    self.water_open.append((x, y))
                surf.blit(tile, (x * 32, y * 32))
            self._g32 = surf
            self._water32 = list(ts.water) or None
            self._water32_fps = ts.water_fps
        return getattr(self, "_g32", None)

    def draw_ground_view(self, target: pygame.Surface, view, t: float) -> None:
        """The ground through a View: the old 16 px surface at zoom 1, the autotiled 32 px one at 2."""
        g = self.ground32() if view.zoom == 2 else None
        if g is None:
            self.draw_ground(target, (view.ox, view.oy), t)
            return
        target.blit(g, (0, 0), pygame.Rect(view.ox, view.oy, target.get_width(), target.get_height()))
        if self._water32:
            frame = self._water32[int(t * self._water32_fps) % len(self._water32)]
            for x, y in self.water_open:
                px, py = x * 32 - view.ox, y * 32 - view.oy
                if -32 < px < target.get_width() and -32 < py < target.get_height():
                    target.blit(frame, (px, py))

    def find(self, otype: str | None = None, name: str | None = None) -> list[MapObject]:
        return [o for o in self.objects if (otype is None or o.type == otype) and (name is None or o.name == name)]

    def draw_ground(self, target: pygame.Surface, cam: tuple[int, int], t: float) -> None:
        cx, cy = cam
        target.blit(self.surface, (0, 0), pygame.Rect(cx, cy, target.get_width(), target.get_height()))
        frame = self._water_frames[int(t * self._water_fps) % len(self._water_frames)]
        for x, y in self.water_cells:
            px, py = x * self.tw - cx, y * self.th - cy
            if -16 < px < target.get_width() and -16 < py < target.get_height():
                target.blit(frame, (px, py))

    def blocked(self, r: pygame.Rect) -> bool:
        if r.left < 0 or r.top < 0 or r.right > self.px_w or r.bottom > self.px_h:
            return True
        return r.collidelist(self.solids) != -1


_MAPS: dict[str, TileMap] = {}


def load_map(name: str) -> TileMap:
    from ..config import assets_dir
    if name not in _MAPS:
        _MAPS[name] = TileMap(assets_dir() / "maps" / f"{name}.tmj")
    return _MAPS[name]
