"""World <-> screen for a scene's camera: the one place that knows the world zoom.

With the v2 art (client/assets/v2/) the world is drawn at 2x: one 16 px map tile is 32 screen
pixels, every world coordinate is doubled on screen, and the v2 sprites (rendered for that
size) are drawn at their native resolution at the doubled position. The logical screen stays
480x270 and the HUD is not scaled, so the camera shows a 240x135 world-pixel window.

Everything a scene draws in the world, and everything that turns the mouse back into a world
point, goes through a `View`:

    view.to_screen(wx, wy)   -> screen pixel of a world point
    view.to_world(sx, sy)    -> world point under a screen pixel (mouse picking)
    view.len(r)              -> a world length (a radius) on screen
    view.img(surface)        -> old art scaled to the zoom (2x nearest, cached)

Gameplay never sees any of this: positions, the collider, radii and what goes to the server
stay in world pixels. With zoom 1 (a checkout without the v2 art) `to_screen` is exactly the
old `int(x) - cam_x`, so the old drawing is unchanged.
"""
from __future__ import annotations

import math
from collections import OrderedDict

import pygame

_X2: OrderedDict = OrderedDict()
X2_MAX = 3000


def zoomed(img: pygame.Surface, zoom: int) -> pygame.Surface:
    """`img` scaled by an integer zoom with nearest neighbour, cached on the surface itself."""
    if zoom == 1:
        return img
    key = (img, zoom)
    s = _X2.get(key)
    if s is None:
        s = pygame.transform.scale(img, (img.get_width() * zoom, img.get_height() * zoom))
        _X2[key] = s
        if len(_X2) > X2_MAX:
            _X2.popitem(last=False)
    else:
        _X2.move_to_end(key)
    return s


class View:
    def __init__(self, zoom: int = 1):
        self.zoom = zoom
        self.ox = 0                 # the camera's top-left in zoomed screen pixels (whole pixels)
        self.oy = 0

    # ------------------------------------------------------------ the camera
    @property
    def x(self) -> float:
        """The camera's top-left in world pixels."""
        return self.ox / self.zoom

    @property
    def y(self) -> float:
        return self.oy / self.zoom

    @property
    def cam(self) -> list:
        """[x, y] of the camera in world pixels (what scenes kept in `self.cam`)."""
        return [self.x, self.y] if self.zoom != 1 else [self.ox, self.oy]

    def set(self, wx: float, wy: float) -> None:
        """Put the camera's top-left on a world point."""
        self.ox, self.oy = int(math.floor(wx * self.zoom)), int(math.floor(wy * self.zoom))

    def span(self, sw: int, sh: int) -> tuple[float, float]:
        """How much of the world a sw x sh screen shows."""
        return sw / self.zoom, sh / self.zoom

    def follow(self, tx: float, ty: float, map_w: int, map_h: int, sw: int, sh: int,
               bounds: pygame.Rect | None = None) -> None:
        """Centre on (tx, ty), kept inside the map (or `bounds`, a world rect); a map or room
        smaller than the screen is centred instead."""
        vw, vh = self.span(sw, sh)
        b = bounds or pygame.Rect(0, 0, map_w, map_h)
        x, y = tx - vw / 2, ty - vh / 2
        x = b.centerx - vw / 2 if b.w <= vw else max(b.left, min(b.right - vw, x))
        y = b.centery - vh / 2 if b.h <= vh else max(b.top, min(b.bottom - vh, y))
        self.set(x, y)

    def shake(self, dx: int, dy: int) -> None:
        self.ox += dx
        self.oy += dy

    # ------------------------------------------------------------ conversions
    def to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        z = self.zoom
        return int(wx * z) - self.ox, int(wy * z) - self.oy

    def sx(self, wx: float) -> int:
        return int(wx * self.zoom) - self.ox

    def sy(self, wy: float) -> int:
        return int(wy * self.zoom) - self.oy

    def to_world(self, sx: float, sy: float) -> tuple[float, float]:
        return (sx + self.ox) / self.zoom, (sy + self.oy) / self.zoom

    def len(self, r: float) -> float:
        return r * self.zoom

    def rect(self, r: pygame.Rect) -> pygame.Rect:
        """A world rect on screen."""
        x, y = self.to_screen(r.x, r.y)
        return pygame.Rect(x, y, r.w * self.zoom, r.h * self.zoom)

    def img(self, surface: pygame.Surface) -> pygame.Surface:
        """Old art (made for 1x) at this zoom."""
        return zoomed(surface, self.zoom)

    def blit_old(self, surf: pygame.Surface, img: pygame.Surface, wx: float, wy: float, flags: int = 0) -> None:
        """Old art whose top-left was at world (wx, wy)."""
        surf.blit(self.img(img), self.to_screen(wx, wy), None, flags)

    def visible(self, wx: float, wy: float, sw: int, sh: int, margin: float = 0) -> bool:
        x, y = self.to_screen(wx, wy)
        return -margin <= x <= sw + margin and -margin <= y <= sh + margin
