"""Túi đồ: stack items (use, read, sell) and equipment (equip)."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from .base import Scene


class BagScene(Scene):
    def __init__(self, game, abode=None):
        super().__init__(game)
        self.abode = abode
        self.tab = "items"
        self.inv = None
        self.scroll = 0
        self.reload()

    def reload(self):
        def inv(r):
            self.inv = r
            self.game.state.inv = r
        self.api.get("/inventory", inv, self.game.api_error)

    def _money(self, r):
        if "spirit_stones" in r:
            self.game.state.me["spirit_stones"] = r["spirit_stones"]
            self.game.audio.play("coin")
        self.reload()

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 50, 24, 380, 226
        ui.panel(x, y, w, h, T.BAG_TITLE)
        tabs = [("items", T.BAG_ITEMS), ("gear", T.BAG_GEAR)]
        for i, (k, label) in enumerate(tabs):
            if ui.button(f"bag_tab_{k}", x + 12 + i * 71, y + 12, 68, 14, label, selected=self.tab == k):
                self.tab, self.scroll = k, 0
        lx, ly, lw = x + 12, y + 32, w - 24
        inv = self.inv or {}
        rows = {"items": inv.get("items") if self.inv else None,
                "gear": inv.get("equipment") if self.inv else None}[self.tab]
        if rows is None:
            ui.text("...", 240, ly + 30, 10, anchor="center")
        elif not rows:
            ui.text(T.EMPTY_LIST, lx, ly + 6, 8, max_w=lw)
        else:
            per = 9
            if ui.inp.wheel and ui.enabled:
                self.scroll = max(0, min(max(0, len(rows) - per), self.scroll - ui.inp.wheel))
            for i, r in enumerate(rows[self.scroll:self.scroll + per]):
                ry = ly + i * 18
                ui.fill(lx, ry, lw, 16, "#FFFDF7" if i % 2 else "#F8F1E3")
                getattr(self, f"row_{self.tab}")(ui, r, lx, ry, lw)
            if len(rows) > per:
                ui.text(f"{self.scroll + 1}–{min(len(rows), self.scroll + per)}/{len(rows)} (cuộn chuột)",
                        x + w - 14, y + h - 30, 7, "#8E877A", anchor="topright")
        if ui.button("bag_close", x + w / 2 - 35, y + h - 22, 70, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    # ---------------------------------------------------------------- stage 4
    def _after(self, msg: str | None = None):
        def ok(r):
            if msg:
                self.game.toast(msg, "#6A994E")
            self.game.refresh_cult()
            self.reload()
        return ok

    def _read_note(self, r: dict) -> None:
        """Open Tàng Thư Các at the section this ghi chú explains (M7)."""
        from .math_library import DocScene
        doc = r.get("doc") or {}
        if doc.get("id"):
            self.game.push(DocScene(self.game, doc["id"], doc.get("block", 0)))

    def row_icon(self, ui, r, lx, ry, fallback: str) -> float:
        """Draw the item's icon (M8) and say where its text should start.

        The icons are rendered from 3D models by a tool that needs Blender, so a
        checkout without them falls back to the colour bar this row always had."""
        from ..engine import art2, icons
        img = art2.item_icon(r) if art2.on() else None      # the v2 atlases first
        if img is None:
            img = icons.for_item(r)
        if img is None:
            ui.fill(lx, ry, 3, 16, fallback)
            return lx + 8
        ui.image(img, lx, ry - 1, zoom=0.5)      # 32 px icon, drawn at 16
        return lx + 20

    def row_items(self, ui, r, lx, ry, lw):
        colour = ("#BC4749" if r.get("kind") == "pill"
                  else "#C99A3A" if r.get("kind") in ("egg", "food")
                  else "#6A994E" if r.get("kind") == "note" else "#8E877A")
        tx = self.row_icon(ui, r, lx, ry, colour)
        ui.text(r["name_vi"], tx, ry + 8, 8, anchor="midleft")
        ui.text(f"x{r['qty']}", lx + 170, ry + 8, 8, anchor="midleft")
        if ui.hover(lx, ry, lw - 70, 16):
            ui.set_tooltip(r.get("desc_vi", ""))
        if r.get("kind") == "note" and ui.button(f"read_{r['item_id']}", lx + lw - 70, ry + 2, 66, 12,
                                                 T.NOTE_READ, size=7):
            # M7: a ghi chú lỗi sai is read, not spent - it opens its part of Tàng Thư Các
            self.api.post("/inventory/use", {"item_id": r["item_id"]}, self._read_note,
                          self.game.api_error)
        elif r.get("usable") and ui.button(f"use_{r['item_id']}", lx + lw - 70, ry + 2, 66, 12, T.USE, size=7):
            self.api.post("/inventory/use", {"item_id": r["item_id"]}, self._after(), self.game.api_error)
        elif r.get("kind") == "egg":
            ui.text(T.EGG_HINT, lx + lw - 6, ry + 8, 7, "#6A994E", anchor="midright")
        elif r.get("sell_price") and ui.button(f"sell_item_{r['item_id']}", lx + lw - 70, ry + 2, 66, 12,
                                               T.SELL_ITEM.format(p=r["sell_price"]), size=7,
                                               tooltip=f"{r['sell_price']} Linh Thạch mỗi cái"):
            self.api.post("/inventory/sell", {"item_id": r["item_id"], "qty": 1}, self._money, self.game.api_error)

    def row_gear(self, ui, r, lx, ry, lw):
        tx = self.row_icon(ui, r, lx, ry, r["color"])
        lvl = f" +{r['enhance']}" if r["enhance"] else ""
        ui.text(r["name_vi"] + lvl, tx, ry + 8, 8, r["color"], anchor="midleft")
        stats = " ".join(f"{T.STATS_VI.get(k, k)} {v}" for k, v in r["stats"].items())
        ui.text(f"{r['slot_vi']} · {stats}", lx + 130, ry + 8, 7, "#5A5A5A", anchor="midleft")
        if ui.hover(lx, ry, lw - 70, 16):
            ui.set_tooltip(f"{r['name_vi']} · {r['rarity_vi']}\n{r.get('desc_vi', '')}")
        if r.get("equipped"):
            if ui.button(f"uneq_{r['id']}", lx + lw - 70, ry + 2, 66, 12, T.UNEQUIP, size=7, selected=True):
                self.api.post("/equipment/unequip", {"slot": r["equipped"]}, self._after(), self.game.api_error)
        elif ui.button(f"eq_{r['id']}", lx + lw - 70, ry + 2, 66, 12, T.EQUIP, size=7, style="green"):
            self.api.post("/equipment/equip", {"instance_id": r["id"]}, self._after(), self.game.api_error)
