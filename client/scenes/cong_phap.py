"""Công Pháp (Chiêu Thức II): which six chiêu sit on keys 1-6.

Seventeen chiêu do not fit six keys. This card lists every chiêu (learned ones bright, the others
grey with what Đạo Thụ still asks for), and the six slots of the bar under them. Pick a learned
chiêu, then a slot (or press 1-6); right-click a slot to empty it; "Lưu" sends the six to the
server (POST /math/skills/loadout), which checks them and stores them. Opened from the world
by U or a click on the bar.

The slot rules are pure functions (`assign`, `clear`) so the tests need no window."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui.mathdraw import fit
from .base import Scene

SLOTS = 6
COLS = 6
CELL_W, CELL_H = 64, 38
EL_RGB = {"kim": "#E9C46A", "moc": "#6A994E", "thuy": "#4A7CC8", "hoa": "#E5533D", "tho": "#C99A3A",
          "loi": "#9B6BE8"}
INK = "#2B2B2B"
GREY = "#8E877A"


def assign(slots: list, i: int, sid: str) -> list:
    """`sid` on slot i; if it sat on another slot, that one is emptied (a chiêu is on one slot)."""
    out = [None if s == sid else s for s in slots]
    out[i] = sid
    return out


def clear(slots: list, i: int) -> list:
    out = list(slots)
    out[i] = None
    return out


class CongPhapScene(Scene):
    PANEL = (24, 8, 432, 254)

    def __init__(self, game, world):
        super().__init__(game)
        self.world = world
        self.skills: list[dict] = list(world.mskills or [])
        lo = list(getattr(world, "mskill_loadout", None) or [s["id"] for s in self.skills[:SLOTS]])
        self.slots: list = (lo + [None] * SLOTS)[:SLOTS]
        self.saved = list(self.slots)
        self.pick: str | None = None             # the chiêu chosen to be placed
        self.look: str | None = self.slots[0]    # the chiêu whose details are shown
        self.busy = False

    def by_id(self, sid: str | None) -> dict | None:
        return next((s for s in self.skills if s["id"] == sid), None) if sid else None

    def place(self, i: int) -> None:
        if self.pick is not None:
            self.slots = assign(self.slots, i, self.pick)
            self.look, self.pick = self.pick, None
        else:
            self.look = self.slots[i] or self.look

    def save(self) -> None:
        if self.busy:
            return
        self.busy = True

        def ok(d):
            self.busy = False
            self.world.apply_mskills(d)
            self.game.toast(T.CONG_PHAP_SAVED, "#6A994E")
            self.close()

        def err(e):
            self.busy = False
            self.game.api_error(e)
        self.game.api.post("/math/skills/loadout", {"slots": list(self.slots)}, ok, err)

    # ------------------------------------------------------------ drawing
    def draw_cell(self, ui, sk: dict, x: float, y: float) -> None:
        learned = sk.get("unlocked", True)
        sel = sk["id"] in (self.pick, self.look)
        ui.fill(x, y, CELL_W - 2, CELL_H - 2, "#F4EBD9" if learned else "#D8CFBE")
        ui.border(x, y, CELL_W - 2, CELL_H - 2, UICOL["accent"] if sel else "#B8A98C", 2 if sk["id"] == self.pick else 1)
        ui.fill(x + 2, y + 2, 3, CELL_H - 6, EL_RGB.get(sk.get("element"), GREY))
        self.world.draw_mskill_icon(ui, sk, x + 6, y + 2, not learned)
        if not learned:
            ui.fill(x + 6, y + 2, 22, 22, (0, 0, 0, 110))
        short = fit(ui, sk["name_vi"], 6, CELL_W - 10)
        ui.text(short, x + 6, y + 26, 6, INK if learned else GREY)
        if short != sk["name_vi"] and ui.hover(x, y, CELL_W - 2, CELL_H - 2):
            ui.set_tooltip(sk["name_vi"])       # a long name, cut in its cell: whole on hover and in the details
        if sk["id"] in self.slots:
            ui.text(str(self.slots.index(sk["id"]) + 1), x + CELL_W - 6, y + 3, 8, UICOL["accent"], anchor="topright")
        elif not learned:
            ui.text(T.CONG_PHAP_LOCKED, x + 30, y + 8, 6, GREY, max_w=CELL_W - 34)

    def draw_ui(self, ui):
        ui.dim()
        x0, y0, w, h = self.PANEL
        ui.panel(x0, y0, w, h, T.CONG_PHAP_TITLE)
        learned = sum(1 for s in self.skills if s.get("unlocked", True))
        ui.text(T.CONG_PHAP_COUNT.format(n=learned, t=len(self.skills)), x0 + w - 12, y0 + 4, 7, UICOL["accent"],
                anchor="topright")
        ui.text(T.CONG_PHAP_HINT, x0 + 12, y0 + 16, 7, GREY, max_w=w - 24)
        gx, gy = x0 + 12, y0 + 30
        for n, sk in enumerate(self.skills):
            cx, cy = gx + (n % COLS) * CELL_W + 4, gy + (n // COLS) * CELL_H
            self.draw_cell(ui, sk, cx, cy)
            ui.widgets[f"cp_skill_{sk['id']}"] = ui.rect(cx, cy, CELL_W - 2, CELL_H - 2)
            if ui.click_in(cx, cy, CELL_W - 2, CELL_H - 2):
                self.look = sk["id"]
                self.pick = sk["id"] if sk.get("unlocked", True) else None
        # the details of the chiêu looked at
        rows = (len(self.skills) + COLS - 1) // COLS
        dy = gy + rows * CELL_H + 2
        sk = self.by_id(self.look)
        if sk is None:
            ui.text(T.CONG_PHAP_NONE, gx, dy, 8, GREY)
        else:
            ui.text(sk["name_vi"], gx, dy, 9, INK)
            ui.text(T.CONG_PHAP_STATS.format(kind=sk.get("kind_vi", ""), el=T.ELEMENT_VI.get(sk.get("element"), ""),
                                             qi=sk.get("qi", 0), cd=sk.get("cooldown", 0), qtype=sk.get("qtype_vi", "")),
                    gx + 2 + ui.text_size(sk["name_vi"] + "  ", 9)[0], dy + 2, 7, UICOL["accent"],
                    max_w=w - 40 - ui.text_size(sk["name_vi"], 9)[0])
            body = sk.get("desc_vi", "") if sk.get("unlocked", True) else (sk.get("locked_vi") or "")
            ui.text(body, gx, dy + 13, 7, INK if sk.get("unlocked", True) else "#9A4A3A", max_w=w - 24)
        # the six slots
        sy = y0 + h - 46
        for i in range(SLOTS):
            sx = gx + i * 30
            s = self.by_id(self.slots[i])
            ui.widgets[f"cp_slot_{i}"] = ui.rect(sx, sy, 26, 26)
            ui.fill(sx, sy, 26, 26, (20, 18, 15, 200))
            ui.border(sx, sy, 26, 26, UICOL["accent"] if self.pick and ui.hover(sx, sy, 26, 26) else "#8B5A2B")
            ui.text(str(i + 1), sx + 2, sy + 1, 6, "#E9E4D8")
            if s is not None:
                self.world.draw_mskill_icon(ui, s, sx + 2, sy + 2, not s.get("unlocked", True))
            if ui.click_in(sx, sy, 26, 26):
                self.place(i)
            elif ui.inp.right_clicked and ui.hover(sx, sy, 26, 26):
                ui.inp.right_clicked = False
                self.slots = clear(self.slots, i)
            if self.pick is not None and ui.key(pygame.K_1 + i):
                self.place(i)
        changed = self.slots != self.saved
        if ui.button("cp_save", x0 + w - 124, y0 + h - 22, 56, 15, T.CONG_PHAP_SAVE, style="primary",
                     enabled=changed and not self.busy, key=pygame.K_RETURN):
            self.save()
        if ui.button("cp_close", x0 + w - 62, y0 + h - 22, 50, 15, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()
