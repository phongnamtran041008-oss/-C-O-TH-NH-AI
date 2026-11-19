from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..engine import art2, sprites
from .base import Scene
from .menu import TitleBackground


class CreateCharScene(Scene):
    draws_world = True

    def __init__(self, game):
        super().__init__(game)
        self.bg = TitleBackground()
        # One model for everybody: the Blender-built Đạo Sĩ. The old hair colour / hair style /
        # body pickers are gone because they no longer change what is drawn; the server still
        # stores an `appearance`, so the one fixed look is sent.
        self.app = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}
        self.t = 0.0
        self.dt = 0.0
        self.busy = False
        self.error = ""
        game.ui.set_focus("cc_name")

    def update(self, dt, top):
        self.t += dt
        self.dt = dt

    def draw_world(self, surf):
        self.bg.draw(surf, self.dt)

    def draw_ui(self, ui):
        ui.fill(0, 0, 480, 270, (20, 18, 15, 130))
        x, y, w, h = 60, 22, 360, 226
        ui.panel(x, y, w, h, T.CREATE_TITLE)
        # preview: turns around slowly and walks in place
        frames = sprites.character(self.app)
        d = ("down", "left", "up", "right")[int(self.t / 1.5) % 4]
        f = (0, 1, 0, 2)[int(self.t * 6) % 4]
        ui.fill(x + 20, y + 22, 90, 110, "#E3D5BA")
        ui.border(x + 20, y + 22, 90, 110)
        v2 = art2.char_for("pham_nhan")
        if v2 is not None:      # the v2 Đạo Sĩ a newcomer starts as (hair and body do not change it yet)
            fr = v2.frame(v2.index("walk", self.t, d))
            ui.image(fr, x + 65 - v2.pivot[0] * 2, y + 128 - v2.pivot[1] * 2, zoom=2)
        else:
            ui.image(frames[(d, f)], x + 65, y + 125, zoom=4, anchor="midbottom")
        ui.text("Áo Vải Phàm Nhân", x + 65, y + 140, 7, "#5A5A5A", anchor="center")
        rx = x + 125
        ui.text(T.CHAR_NAME, rx, y + 20, 8)
        ui.input_box("cc_name", rx, y + 31, 210, 16, max_len=16)
        ui.text(T.CREATE_NOTE, rx, y + 58, 8, "#5A5A5A", max_w=w - 145)
        if self.error:
            ui.text(self.error, 240, y + 184, 8, "#BC4749", anchor="center")
        name = ui.value("cc_name").strip()
        go = ui.button("cc_go", 240 - 60, y + h - 26, 120, 18, T.CREATE_GO, style="primary",
                       enabled=bool(name) and not self.busy)
        if (go or (ui.submitted("cc_name") and name)) and not self.busy:
            self.create(name)
        if ui.button("cc_back", x + 10, y + h - 24, 60, 14, T.BACK, key=pygame.K_ESCAPE):
            self.game.set_token(None)
            from .menu import MenuScene
            self.game.replace_all(MenuScene(self.game))

    def create(self, name: str) -> None:
        self.busy, self.error = True, ""

        def ok(ch):
            self.busy = False
            self.game.state.character = ch
            self.game.enter_game()

        def err(e):
            self.busy = False
            self.error = e.message_vi
        self.api.post("/character/create", {"display_name": name, "appearance": dict(self.app)}, ok, err)
