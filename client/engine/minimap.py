"""The minimap of the world HUD and the picture of the big map (Thiên Địa Đồ).

`overview(tmap)` is the whole map at one pixel per tile, coloured by the average colour of each
ground tile, a tile under a solid darkened - built from the tile ids, never by drawing the map
(a 320 x 240 tile map would be a 5120 x 3840 surface). `MiniMap` keeps the HUD's place and
footprint (at most MAX_W x MAX_H, top right): a small map is shown whole, scaled to fit as it
always was; a big one is a window at one pixel per tile that follows the player.
"""
from __future__ import annotations

import math

import pygame

MAX_W, MAX_H = 100, 64
DARK = 0.68                        # a tile under a solid
PORTAL = "#8CB8DA"
ROUTE = (242, 193, 78)
ROUTE_EDGE = (43, 29, 14)

_COLOURS: dict | None = None
_OVERVIEWS: dict = {}


def tile_colours() -> dict[int, tuple[int, int, int]]:
    """Tiled gid -> the average colour of its tile (the old 16 px tiles; the v2 art keeps them)."""
    global _COLOURS
    if _COLOURS is None:
        from ..art import build as B
        out = {}
        for i, (name, variant) in enumerate(B.TILESET):
            c = pygame.transform.average_color(B.tile(name, variant))
            out[i + 1] = (int(c[0]), int(c[1]), int(c[2]))
        _COLOURS = out
    return _COLOURS


def blocked_tiles(tmap) -> bytearray:
    """1 for every tile whose centre lies under a solid."""
    w, h, tw, th = tmap.w, tmap.h, tmap.tw, tmap.th
    out = bytearray(w * h)
    for r in tmap.solids:
        x0 = max(0, int(math.ceil((r[0] - tw / 2) / tw)))
        x1 = min(w - 1, int(math.floor((r[0] + r[2] - tw / 2 - 0.01) / tw)))
        y0 = max(0, int(math.ceil((r[1] - th / 2) / th)))
        y1 = min(h - 1, int(math.floor((r[1] + r[3] - th / 2 - 0.01) / th)))
        if x0 > x1:
            continue
        ones = b"\x01" * (x1 - x0 + 1)
        for y in range(y0, y1 + 1):
            out[y * w + x0: y * w + x1 + 1] = ones
    return out


def overview(tmap) -> pygame.Surface:
    """The map at one pixel per tile (cached per map)."""
    key = (id(tmap), tmap.w, tmap.h)
    s = _OVERVIEWS.get(key)
    if s is not None:
        return s
    cols = tile_colours()
    light = {g: bytes(c) for g, c in cols.items()}
    dark = {g: bytes(int(v * DARK) for v in c) for g, c in cols.items()}
    none = bytes((20, 18, 15))
    solid = blocked_tiles(tmap)
    ground = tmap.ground or [0] * (tmap.w * tmap.h)
    buf = b"".join((dark if solid[i] else light).get(g, none) for i, g in enumerate(ground))
    s = pygame.image.frombuffer(buf, (tmap.w, tmap.h), "RGB").copy()
    _OVERVIEWS[key] = s
    while len(_OVERVIEWS) > 6:
        _OVERVIEWS.pop(next(iter(_OVERVIEWS)))
    return s


class MiniMap:
    """The HUD minimap of one map. `frame` is a surface of the minimap's size (its place and
    footprint: what the world scene's layout reads)."""

    def __init__(self, tmap):
        self.map = tmap
        self.ov = overview(tmap)
        w, h = tmap.w, tmap.h
        s = min(MAX_W / w, MAX_H / h)
        self.whole = s >= 1.0
        if self.whole:            # the old rule: the whole map, as large as the footprint allows
            k = min(MAX_W / tmap.px_w, MAX_H / tmap.px_h)
            self.size = (max(1, int(tmap.px_w * k)), max(1, int(tmap.px_h * k)))
            self.k = k                       # minimap px per world px
            self.frame = pygame.transform.smoothscale(self.ov, self.size)
        else:                     # a window at one pixel per tile
            self.size = (min(MAX_W, w), min(MAX_H, h))
            self.k = 1.0 / tmap.tw
            self.frame = pygame.Surface(self.size)
        self.ox = self.oy = 0.0              # the window's top-left (world px)

    # ---- the window
    def follow(self, x: float, y: float) -> None:
        if self.whole:
            return
        vw, vh = self.size[0] / self.k, self.size[1] / self.k
        self.ox = max(0.0, min(self.map.px_w - vw, x - vw / 2))
        self.oy = max(0.0, min(self.map.px_h - vh, y - vh / 2))

    def to_mm(self, x: float, y: float) -> tuple[float, float]:
        """World px -> minimap px (from its top-left)."""
        return (x - self.ox) * self.k, (y - self.oy) * self.k

    def inside(self, mx: float, my: float, pad: float = 0) -> bool:
        return -pad <= mx <= self.size[0] + pad and -pad <= my <= self.size[1] + pad

    def picture(self) -> pygame.Surface:
        if self.whole:
            return self.frame
        tx, ty = int(self.ox / self.map.tw), int(self.oy / self.map.th)
        r = pygame.Rect(tx, ty, self.size[0], self.size[1]).clip(self.ov.get_rect())
        return self.ov.subsurface(r)

    # ---- drawing
    def draw(self, ui, x: float, y: float, scene) -> None:
        """The minimap at (x, y): ground, gates, players, the Linh Hồ's finds, Chỉ Đường's way and
        goal, me, and its frame."""
        p = scene.player
        self.follow(p.x, p.y)
        if not self.whole:            # the window slides a tile at a time: keep the marks on the tiles
            self.ox = int(self.ox / self.map.tw) * self.map.tw
            self.oy = int(self.oy / self.map.th) * self.map.th
        w, h = self.size
        ui.fill(x - 2, y - 2, w + 4, h + 4, "#3A342C")
        ui.image(self.picture(), x, y)
        k = self.k
        clip = ui.win.get_clip()
        ui.win.set_clip(ui.rect(x, y, w, h))
        for o in self.map.objects:
            if o.type == "portal":
                mx, my = self.to_mm(o.x, o.y)
                ui.fill(x + mx, y + my, max(2, o.w * k), max(2, o.h * k), PORTAL)
        for e in getattr(scene, "entities", {}).values():
            mx, my = self.to_mm(e.pos[0], e.pos[1])
            if e.kind == "p":
                ui.fill(x + mx - 1, y + my - 1, 2, 2, "#FFFFFF")
            elif e.kind == "r":
                ui.fill(x + mx - 1.5, y + my - 1.5, 3, 3, "#8E5AC8")
        for f in getattr(scene, "sniffed", None) or []:          # what the Linh Hồ smells
            mx, my = self.to_mm(f["pos"][0] * 16 + 8, f["pos"][1] * 16 + 12)
            ui.fill(x + mx - 1.5, y + my - 1.5, 3, 3, "#F4A261")
        from . import chi_duong
        chi_duong.of(scene.game).draw_on_minimap(ui, self, x, y, scene)
        mx, my = self.to_mm(p.x, p.y)
        ui.fill(x + mx - 1.5, y + my - 1.5, 3, 3, "#E9C46A")
        ui.win.set_clip(clip)
        ui.border(x - 2, y - 2, w + 4, h + 4, "#8B5A2B")


def polyline(ui, pts, color, width: int = 1) -> None:
    """A line through logical points, drawn at window resolution with a dark edge."""
    if len(pts) < 2:
        return
    win = [ui.d.to_window(px, py) for px, py in pts]
    s = ui.s
    pygame.draw.lines(ui.win, ROUTE_EDGE, False, win, max(1, (width + 1) * s))
    pygame.draw.lines(ui.win, color, False, win, max(1, width * s))
