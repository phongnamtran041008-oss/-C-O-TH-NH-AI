"""Túi đồ: stack items (use, read, sell), equipment (equip) and the weapons of Thiên Địa Đồ
(tab Binh Khí: the ones the player holds, with what they do, and where the others lie)."""
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
        self.wpn = None             # GET /weapons
        self.scroll = 0
        self.reload()

    def reload(self):
        def inv(r):
            self.inv = r
            self.game.state.inv = r
        self.api.get("/inventory", inv, self.game.api_error)

        def wpn(r):
            self.wpn = r
        self.api.get("/weapons", wpn, lambda e: None)     # an old server has no weapons: the tab stays empty

    def _money(self, r):
        if "spirit_stones" in r:
            self.game.state.me["spirit_stones"] = r["spirit_stones"]
            self.game.audio.play("coin")
        self.reload()

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 50, 24, 380, 226
        ui.panel(x, y, w, h, T.BAG_TITLE)
        tabs = [("items", T.BAG_ITEMS), ("gear", T.BAG_GEAR), ("weapons", T.BAG_WEAPONS)]
        for i, (k, label) in enumerate(tabs):
            if ui.button(f"bag_tab_{k}", x + 12 + i * 71, y + 12, 68, 14, label, selected=self.tab == k):
                self.tab, self.scroll = k, 0
        lx, ly, lw = x + 12, y + 32, w - 24
        if self.tab == "weapons":
            self.draw_weapons(ui, x, y, w, h, lx, ly, lw)
            if ui.button("bag_close", x + w / 2 - 35, y + h - 22, 70, 14, T.CLOSE, key=pygame.K_ESCAPE):
                self.close()
            return
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

    # ---------------------------------------------------------------- Binh Khí (Thiên Địa Đồ)
    def weapon_rows(self) -> list[tuple[str, object]]:
        d = self.wpn or {}
        mine = [w for w in d.get("weapons", []) if w.get("weapon")]
        rows: list[tuple[str, object]] = [("head", T.WPN_MINE)]
        rows += [("mine", w) for w in mine] or [("note", T.WPN_NONE)]
        rows.append(("head", T.WPN_PLACED))
        order = {"available": 0, "locked": 1, "taken": 2}
        rows += [("spot", p) for p in sorted(d.get("placed", []), key=lambda p: order.get(p["state"], 3))]
        return rows

    def draw_weapons(self, ui, x, y, w, h, lx, ly, lw):
        if self.wpn is None:
            ui.text("...", 240, ly + 30, 10, anchor="center")
            return
        lw = lw - 98                                   # the right column shows the weapon in hand
        rows = self.weapon_rows()
        per = 8
        if ui.inp.wheel and ui.enabled:
            self.scroll = max(0, min(max(0, len(rows) - per), self.scroll - ui.inp.wheel))
        for i, (kind, r) in enumerate(rows[self.scroll:self.scroll + per]):
            ry = ly + i * 20
            if kind == "head":
                ui.text(r, lx, ry + 10, 8, "#6A4C2A", anchor="midleft")
                continue
            ui.fill(lx, ry, lw, 18, "#FFFDF7" if i % 2 else "#F8F1E3")
            if kind == "note":
                ui.text(fit(ui, r, 7, lw - 8), lx + 4, ry + 9, 7, "#8E877A", anchor="midleft")
            elif kind == "mine":
                self.row_weapon(ui, r, lx, ry, lw)
            else:
                self.row_spot(ui, r, lx, ry, lw)
        if len(rows) > per:
            ui.text(f"{self.scroll + 1}–{min(len(rows), self.scroll + per)}/{len(rows)} (cuộn chuột)",
                    lx + lw, y + h - 30, 7, "#8E877A", anchor="topright")
        self.draw_hand(ui, lx + lw + 8, ly, 90)

    def row_weapon(self, ui, r, lx, ry, lw):
        wv = r["weapon"]
        tx = self.row_icon(ui, r, lx, ry, r["color"])
        lvl = f" +{r['enhance']}" if r["enhance"] else ""
        ui.text(r["name_vi"] + lvl, tx, ry + 5, 8, r["color"], anchor="midleft")
        ui.text(fit(ui, T.WPN_LINE.format(type=wv["type_vi"], grade=wv["grade"], quality=wv.get("quality_vi", ""),
                                          atk=r["stats"].get("atk", 0)), 6, lw - (tx - lx) - 58),
                tx, ry + 14, 6, "#5A5A5A", anchor="midleft")
        if ui.hover(lx, ry, lw - 56, 16):
            ui.set_tooltip(T.WPN_TIP.format(name=r["name_vi"], quality=wv.get("quality_vi", ""),
                                            effect=wv["effect_vi"], branch=wv["branch_vi"], why=wv["why_vi"]))
        if r.get("equipped"):
            if ui.button(f"wuneq_{r['id']}", lx + lw - 54, ry + 3, 50, 12, T.UNEQUIP, size=7, selected=True):
                self.api.post("/weapons/unequip", {}, self._after(), self.game.api_error)
        elif ui.button(f"weq_{r['id']}", lx + lw - 54, ry + 3, 50, 12, T.EQUIP, size=7, style="green"):
            self.api.post("/weapons/equip", {"instance_id": r["id"]}, self._after(), self.game.api_error)

    def row_spot(self, ui, p, lx, ry, lw):
        from ..engine import art2
        img = art2.weapon_icon(p["weapon"]) if art2.on() else None
        tx = lx + 8
        if img is not None:
            ui.image(img, lx, ry + 1, zoom=0.5)
            tx = lx + 20
        colour = {"available": "#6A994E", "taken": "#8E877A", "locked": "#BC4749"}.get(p["state"], "#5A5A5A")
        ui.text(f"{p['name_vi']} · {p.get('quality_vi', '')}", tx, ry + 5, 8, "#2B2B2B", anchor="midleft")
        detail = p["reason_vi"] if p["state"] == "locked" else T.WPN_WHERE.format(land=p["land_vi"], spot=p["spot_vi"])
        ui.text(fit(ui, detail, 6, lw - (tx - lx) - 4), tx, ry + 14, 6,
                colour if p["state"] == "locked" else "#5A5A5A", anchor="midleft")
        ui.text(T.WPN_STATE.get(p["state"], p["state"]), lx + lw - 4, ry + 5, 7, colour, anchor="midright")
        if ui.hover(lx, ry, lw, 16):
            tip = T.WPN_TIP.format(name=p["name_vi"], quality=p.get("quality_vi", ""), effect=p["effect_vi"],
                                   branch=p["branch_vi"], why=p["why_vi"])
            where = T.WPN_WHERE.format(land=p["land_vi"], spot=p["spot_vi"])
            ui.set_tooltip(f"{tip}\n{where}" + (f"\n{p['reason_vi']}" if p["reason_vi"] else ""))

    def draw_hand(self, ui, x, y, w):
        """The character holding the equipped weapon: the same layers the world draws."""
        from ..engine import art2
        d = self.wpn or {}
        held = next((r for r in d.get("weapons", []) if r["id"] == d.get("equipped")), None)
        ui.fill(x, y, w, 104, "#E3D5BA")
        ui.text(T.WPN_HAND, x + w / 2, y + 4, 7, "#6A4C2A", anchor="midtop")
        pic = hand_picture((self.game.state.character or {}).get("realm"), held["kind"] if held else None,
                           ui.time) if art2.on() else None
        if pic is not None:
            ui.image(pic, x + w / 2, y + 96, zoom=1, anchor="midbottom")
        name = held["name_vi"] if held else T.NO_WEAPON
        ui.text(name, x + w / 2, y + 110, 7, "#2B2B2B", anchor="midtop", max_w=w)
        tv = d.get("tu_vi")
        if tv:
            ui.text(T.WPN_TU_VI.format(realm=tv["realm_vi"], stage=tv["stage"]), x + w / 2, y + 122, 6,
                    "#6A994E", anchor="midtop", max_w=w)


_HAND: dict = {}         # hand_picture by the frames it is made of


def fit(ui, txt: str, size: float, max_w: float) -> str:
    """`txt` cut with "..." to fit one line of max_w (the whole text stays in the tooltip)."""
    if ui.text_size(txt, size)[0] <= max_w:
        return txt
    while txt and ui.text_size(txt + "...", size)[0] > max_w:
        txt = txt[:-1]
    return txt.rstrip(" ,.:;") + "..."


def hand_picture(realm: str | None, weapon: str | None, t: float, facing: str = "right") -> pygame.Surface | None:
    """One surface of the v2 character idling with `weapon` in hand (art2.char_layers), cut to
    its pixels; None without v2 art."""
    from ..engine import art2
    layers = art2.char_layers(realm, "idle", t, facing, weapon, aura=False)
    if not layers:
        return None
    key = tuple((id(img), ox, oy, flags) for img, (ox, oy), flags in layers)   # sheet frames are cached
    if key in _HAND:
        return _HAND[key]
    x0 = min(ox for _, (ox, oy), _ in layers)
    y0 = min(oy for _, (ox, oy), _ in layers)
    x1 = max(ox + img.get_width() for img, (ox, oy), _ in layers)
    y1 = max(oy + img.get_height() for img, (ox, oy), _ in layers)
    surf = pygame.Surface((x1 - x0, y1 - y0), pygame.SRCALPHA)
    for img, (ox, oy), flags in layers:
        surf.blit(img, (ox - x0, oy - y0), special_flags=flags)
    if len(_HAND) > 64:
        _HAND.clear()
    _HAND[key] = art2.trim(surf)
    return _HAND[key]
