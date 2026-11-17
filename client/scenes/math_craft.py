"""Lò Toán (M7): the furnace in Loạn Số Cốc that turns what the mistakes dropped into
equipment.

A recipe shows two lists, because it asks for two different things: materials, which are
spent, and ghi chú lỗi sai, which are only checked - the note stays in the bag, so the line
under them says so rather than letting the player guess.
"""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from .base import Scene

GREY = "#8E877A"
RED = "#BC4749"
GREEN = "#6A994E"


class MathCraftScene(Scene):
    """The recipe list, one panel per recipe, scrolled with the mouse wheel."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.scroll = 0.0
        self.busy = False
        self.load()

    def load(self) -> None:
        self.api.get("/math/craft", self.loaded, self.game.api_error)

    def loaded(self, r: dict) -> None:
        self.data, self.busy = r, False

    def forge(self, recipe_id: str, name_vi: str) -> None:
        if self.busy:
            return
        self.busy = True

        def ok(r):
            self.game.toast(T.CRAFT_DONE.format(name=r["equipment"]["name_vi"]), "#C99A3A")
            self.game.audio.play("correct")
            self.load()

        def err(e):
            self.busy = False
            self.game.api_error(e)
        self.api.post("/math/craft", {"recipe_id": recipe_id}, ok, err)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.CRAFT_TITLE)
        if self.data is None:
            ui.text(T.CRAFT_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        elif not self.data["recipes"]:
            ui.text(T.CRAFT_EMPTY, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            self.scroll = max(0.0, self.scroll - ui.inp.wheel * 24)
            self.draw_recipes(ui, x, y, w, h)
        ui.text(f"{self.data['spirit_stones'] if self.data else 0} Linh Thạch",
                x + 12, y + h - 20, 7, "#C99A3A")
        if ui.button("craft_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_recipes(self, ui, x, y, w, h):
        top, bottom = y + 22, y + h - 24
        cy = top - self.scroll
        total = 0.0
        for r in self.data["recipes"]:
            card_h = 62
            total += card_h + 4
            if cy + card_h > top - 2 and cy < bottom:
                self.draw_recipe(ui, r, x + 10, cy, w - 20, card_h, clipped=cy < top)
            cy += card_h + 4
        self.scroll = min(self.scroll, max(0.0, total - (bottom - top)))

    def draw_recipe(self, ui, r, x, y, w, h, clipped: bool):
        made = r["makes"]
        ui.fill(x, y, w, h, "#F4EBD9" if r["can"] else "#EDE6D6")
        ui.border(x, y, w, h, UICOL["accent"] if r["can"] else "#D6CDBA", 1)
        if clipped:                       # scrolled half off the top: no text, just the frame
            return
        ui.text(f"{T.MATH_FLOOR.format(n=r['floor'])} · {r['name_vi']}", x + 8, y + 6, 9, "#2B2B2B")
        slot = T.CRAFT_SLOT.get(made["slot"], made["slot"] or "")
        stats = "  ".join(f"{k} +{v}" for k, v in sorted(made["stats"].items()))
        ui.text(f"{T.CRAFT_MAKES}: {made['name_vi']} ({slot})  {stats}", x + 8, y + 18, 7, GREY, max_w=w - 100)
        ui.text(T.CRAFT_NEEDS + ": " + "  ".join(
            f"{i['name_vi']} {T.CRAFT_HAVE.format(have=i['have'], need=i['qty'])}" for i in r["ingredients"]),
            x + 8, y + 30, 7, "#2B2B2B", max_w=w - 100)
        notes = r["notes"]
        if notes:
            ui.text(T.CRAFT_NOTES + ": " + "  ".join(
                ("✓ " if n["enough"] else "✗ ") + n["name_vi"] for n in notes),
                x + 8, y + 41, 7, GREEN if all(n["enough"] for n in notes) else RED, max_w=w - 100)
        ui.text(T.CRAFT_FEE.format(n=r["fee"]), x + 8, y + 52, 7, "#C99A3A")
        if ui.button(f"craft_{r['id']}", x + w - 76, y + h - 24, 66, 18, T.CRAFT_DO,
                     style="primary", enabled=r["can"] and not self.busy):
            self.forge(r["id"], r["name_vi"])
