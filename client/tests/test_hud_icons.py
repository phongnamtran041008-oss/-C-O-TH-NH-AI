"""The hotbar and the ability row keep their scaled icons (scenes/world.py `hud_icon`): the same
pixels as `UI.image(..., anchor="center")`, which scaled them anew every frame."""
from __future__ import annotations

import pygame

from client.scenes import world as W
from client.ui.kit import UI


class _D:
    def __init__(self, scale: float, ox: int = 7, oy: int = 3):
        self.scale, self.ox, self.oy = scale, ox, oy

    def to_window(self, x, y):
        return int(self.ox + x * self.scale), int(self.oy + y * self.scale)


class _Ui:
    def __init__(self, scale: float):
        self.s, self.d = scale, _D(scale)
        self.win = pygame.Surface((1440, 810), pygame.SRCALPHA)
        self.win.fill((20, 30, 40, 255))


def _icon(seed: int) -> pygame.Surface:
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    for y in range(32):
        for x in range(32):
            s.set_at((x, y), ((x * 7 + seed) % 256, (y * 5 + seed) % 256, (x * y + seed) % 256, (x + y) * 4 % 256))
    return s


def test_a_cached_icon_is_drawn_with_the_same_pixels_as_ui_image():
    W._HUD_ICONS.clear()
    for scale in (3.0, 2.0, 2.5):
        for zoom in (0.625, 18 / 32, 1.0):
            img = _icon(int(scale * 10 + zoom * 100))
            old, new = _Ui(scale), _Ui(scale)
            UI.image(old, img, 404.0 + 11, 200.0 + 11, zoom=zoom, anchor="center")
            W.hud_icon(_Ui(scale), img, 404.0 + 11, 200.0 + 11, zoom)   # the first draw scales it
            W.hud_icon(new, img, 404.0 + 11, 200.0 + 11, zoom)          # the next one reuses it
            assert pygame.image.tobytes(old.win, "RGBA") == pygame.image.tobytes(new.win, "RGBA"), (scale, zoom)


def test_an_icon_cut_anew_from_its_sheet_each_frame_is_scaled_once():
    W._HUD_ICONS.clear()
    sheet = _icon(3)
    ui = _Ui(3.0)
    calls = []
    real = pygame.transform.scale
    pygame.transform.scale = lambda s, size: (calls.append(size), real(s, size))[1]
    try:
        for _ in range(10):
            sub = sheet.subsurface((0, 0, 16, 16))              # what icons.icon() returns each call
            W.hud_icon(ui, sub, 100, 100, 0.625, ("icon", id(sub.get_parent()), sub.get_offset()))
            img = _icon(9)                                      # a picture whose surface is kept
            W.hud_icon(ui, img, 140, 100, 0.625)
    finally:
        pygame.transform.scale = real
    assert calls.count((30, 30)) == 1                           # the sheet's cell, once
    assert len(calls) == 11                                      # the fresh picture: 10, one each (new surfaces)
    assert len(W._HUD_ICONS) <= W.HUD_ICONS_MAX
