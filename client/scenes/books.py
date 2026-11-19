"""Tàng Thư Các shelf of phổ (spec 9.3): every book of things met, caught and owned with its %
and milestone rewards, the titles and portrait frames those give, the Bảo Vật Phổ, and the
Thủ Thư's đan phương. The math scrolls of the library are scenes/math_library.py."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from .base import Scene

BOOK_ICON = {"monster": "Yêu", "bee": "Ong", "fish": "Cá", "treasure": "Bảo", "pet": "Thú"}


def portrait_frame(ui, frame: str | None, x: float, y: float, w: float, h: float) -> None:
    """The avatar frame chosen on the shelf, drawn around a portrait box."""
    col = T.FRAME_COLORS.get(frame or "")
    if col:
        ui.border(x - 1, y - 1, w + 2, h + 2, col, 2)
        ui.fill(x - 2, y - 2, 4, 4, col)
        ui.fill(x + w - 2, y + h - 2, 4, 4, col)


def title_after(ui, title: str | None, rect, y: float) -> None:
    """The chosen title, small and golden, right after the character's name."""
    if title:
        ui.text(f"«{title}»", rect.right + 2, y, 6, "#B8862E")


class BooksScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.reload()

    def reload(self) -> None:
        self.api.get("/books", lambda d: setattr(self, "data", d), self.game.api_error)

    def on_resume(self) -> None:
        self.reload()

    def claim(self, book: str, pct: int) -> None:
        def ok(r):
            self.data = r
            c = r["claimed"]
            name = next(b["name_vi"] for b in r["books"] if b["id"] == c["book"])
            self.game.toast(T.LIBRARY_GOT.format(p=c["pct"], book=name, r=c["reward_vi"]), "#C99A3A")
            self.game.audio.play("coin")
            self.game.refresh_me()
        self.api.post("/books/claim", {"book": book, "pct": pct}, ok, self.game.api_error)

    def open_book(self, book: str) -> None:
        g = self.game
        if book == "monster":
            from .rpg import MonsterBookScene
            g.push(MonsterBookScene(g))
        elif book == "bee":
            g.open_bee_book()
        elif book == "fish":
            from .fishing import FishBookScene
            g.push(FishBookScene(g))
        elif book == "treasure":
            g.push(TreasureBookScene(g))
        elif book == "pet":
            from .pets import PetBookScene
            g.push(PetBookScene(g))

    def open_scrolls(self) -> None:
        from .math_library import LibraryListScene
        self.game.push(LibraryListScene(self.game))

    def wear(self, title: str | None = None, frame: str | None = None) -> None:
        body = {k: v for k, v in (("title", title), ("frame", frame)) if v is not None}

        def ok(r):
            self.data = r
            self.game.state.me["title"], self.game.state.me["frame"] = r.get("title"), r.get("frame")
        self.api.post("/books/wear", body, ok, self.game.api_error)

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 20, 14, 440, 244
        ui.panel(x, y, w, h, T.BOOKS_TITLE)
        ui.text(T.BOOKS_HINT, x + 12, y + 10, 7, "#5A5A5A")
        if ui.button("books_scrolls", x + w - 106, y + 6, 94, 15, T.BOOKS_SCROLLS, size=7, style="gold"):
            self.open_scrolls()
            return
        d = self.data
        if d:
            rh = 26
            for i, b in enumerate(d["books"]):
                ry = y + 28 + i * rh
                bw = w - 24
                ui.fill(x + 12, ry, bw, rh - 2, "#FFFDF7")
                ui.border(x + 12, ry, bw, rh - 2)
                ui.text(BOOK_ICON.get(b["id"], "?"), x + 26, ry + 12, 6, "#BC4749", anchor="center")
                ui.text(b["name_vi"], x + 42, ry + 1, 9)
                ui.text(T.LIBRARY_BOOK_ROW.format(f=b["found"], t=b["total"], p=b["pct"]), x + 42, ry + 13, 7, "#5A5A5A")
                ui.progress(x + 110, ry + 15, 60, 4, b["pct"] / 100, "#6A994E")
                mx = x + 176
                for m in b["milestones"]:
                    wid = f"lib_claim_{b['id']}_{m['pct']}"
                    label = f"{m['pct']}%"
                    if m["claimed"]:
                        ui.button(wid, mx, ry + 5, 30, 13, label + "✓", size=6, enabled=False,
                                  tooltip=f"{T.LIBRARY_CLAIMED}: {m['reward_vi']}")
                    elif ui.button(wid, mx, ry + 5, 30, 13, label, size=6, style="gold" if m["ready"] else "normal",
                                   enabled=m["ready"], tooltip=m["reward_vi"]):
                        self.claim(b["id"], m["pct"])
                    mx += 32
                if ui.button(f"lib_open_{b['id']}", x + 12 + bw - 46, ry + 5, 40, 13, T.LIBRARY_OPEN, size=7,
                             style="primary"):
                    self.open_book(b["id"])
                    return
            self.draw_badges(ui, x + 12, y + 28 + len(d["books"]) * rh + 4)
        if d and ui.button("lib_shop", x + w - 160, y + h - 22, 70, 15, T.LIBRARY_SHOP):
            self.game.push(BooksShopScene(self.game, self))
        if ui.button("books_close", x + w - 84, y + h - 22, 70, 15, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_badges(self, ui, x, y):
        """Titles and avatar frames earned from milestones: pick the one to show."""
        d = self.data
        if d["titles"]:
            ui.text(T.LIBRARY_TITLE_PICK, x, y + 3, 7, "#8B5A2B")
            bx = x + 50
            for i, t in enumerate([""] + d["titles"]):
                label = t or T.LIBRARY_NONE
                bw = ui.text_size(label, 6)[0] + 8
                if ui.button(f"lib_title_{i}", bx, y, bw, 11, label, size=6, selected=(d.get("title") or "") == t):
                    self.wear(title=t)
                bx += bw + 2
            y += 13
        if d["frames"]:
            ui.text(T.LIBRARY_FRAME_PICK, x, y + 3, 7, "#8B5A2B")
            bx = x + 50
            for i, f in enumerate([{"id": "", "name_vi": T.LIBRARY_NONE}] + d["frames"]):
                bw = ui.text_size(f["name_vi"], 6)[0] + 8
                if ui.button(f"lib_frame_{i}", bx, y, bw, 11, f["name_vi"], size=6,
                             selected=(d.get("frame") or "") == f["id"]):
                    self.wear(frame=f["id"])
                bx += bw + 2


class BooksShopScene(Scene):
    """The Thủ Thư's shelf (spec 8.4, 12.3): đan phương are bought at the Tàng Thư Các."""
    PER = 8

    def __init__(self, game, host: BooksScene):
        super().__init__(game)
        self.host = host
        self.page = 0

    def buy(self, item_id: str) -> None:
        def ok(r):
            self.host.data = r
            self.game.toast(T.LIBRARY_BOUGHT.format(name=r["name_vi"]), "#6A994E")
            self.game.audio.play("coin")
            self.game.refresh_me()
            self.game.refresh_inv()
        self.api.post("/books/buy", {"item_id": item_id}, ok, self.game.api_error)

    def draw_ui(self, ui):
        ui.dim(160)
        d = self.host.data or {}
        x, y, w, h = 50, 24, 380, 224
        ui.panel(x, y, w, h, T.LIBRARY_SHOP_TITLE)
        ui.text(T.LIBRARY_SHOP_HINT_RECIPES, x + 12, y + 10, 7, "#5A5A5A", max_w=w - 120)
        at = d.get("at_desk")
        if not at:
            ui.text(T.LIBRARY_SHOP_FAR, x + 12, y + 36, 7, "#BC4749", max_w=w - 24)
        rows = d.get("shop", [])
        pages = max(1, (len(rows) + self.PER - 1) // self.PER)
        self.page = min(self.page, pages - 1)
        if pages > 1:
            if ui.button("lib_shop_prev", x + w - 92, y + 8, 22, 13, "<", size=7, enabled=self.page > 0):
                self.page -= 1
            ui.text(f"{self.page + 1}/{pages}", x + w - 56, y + 14, 7, "#5A5A5A", anchor="center")
            if ui.button("lib_shop_next", x + w - 42, y + 8, 22, 13, ">", size=7, enabled=self.page < pages - 1):
                self.page += 1
        for i, it in enumerate(rows[self.page * self.PER:(self.page + 1) * self.PER]):
            ry = y + 48 + i * 20
            ui.fill(x + 12, ry, w - 24, 18, "#FFFDF7")
            ui.border(x + 12, ry, w - 24, 18)
            ui.text(it["name_vi"], x + 18, ry + 9, 8, anchor="midleft")
            if ui.hover(x + 12, ry, w - 130, 18):
                ui.set_tooltip(it["desc_vi"])
            owned = it["have"] > 0
            if owned:
                ui.text(T.LIBRARY_SHOP_OWNED, x + w - 108, ry + 9, 6, "#6A994E", anchor="midright")
            if ui.button(f"lib_buy_{it['item_id']}", x + w - 102, ry + 2, 84, 14,
                         T.LIBRARY_SHOP_BUY.format(p=it["price"]), size=7, style="gold",
                         enabled=bool(at) and not owned):
                self.buy(it["item_id"])
        if ui.button("lib_shop_close", x + w / 2 - 35, y + h - 20, 70, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()


class TreasureBookScene(Scene):
    """Bảo Vật Phổ: equipment, pills and rods ever owned."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.api.get("/codex/treasure", lambda d: setattr(self, "data", d), game.api_error)

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 30, 20, 420, 232
        ui.panel(x, y, w, h, T.TREASURE_TITLE)
        d = self.data
        if d:
            ui.text(T.TREASURE_FOUND.format(f=d["found"], t=d["total"]), x + 12, y + 10, 7, "#BC4749")
            for i, e in enumerate(d["entries"][:24]):
                cx = x + 12 + (i % 4) * 100
                cy = y + 24 + (i // 4) * 30
                ui.fill(cx, cy, 96, 27, "#FFFDF7" if e["found"] else "#E3D5BA")
                ui.border(cx, cy, 96, 27, "#2B2B2B" if e["found"] else "#B8AE9C")
                ui.text(e["kind_vi"], cx + 4, cy + 2, 6, "#8E877A")
                ui.text(e["name_vi"] if e["found"] else "? ? ?", cx + 4, cy + 12, 8,
                        "#2B2B2B" if e["found"] else "#8E877A", max_w=90)
                ui.widgets[f"tr_{e['id']}"] = ui.rect(cx, cy, 96, 27)
                if ui.hover(cx, cy, 96, 27):
                    ui.set_tooltip(e.get("desc_vi") if e["found"] else T.TREASURE_UNKNOWN)
        if ui.button("tr_close", x + w / 2 - 35, y + h - 20, 70, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()
