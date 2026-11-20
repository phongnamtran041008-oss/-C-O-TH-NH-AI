"""Trắc Linh Đài: the linh căn (server systems/linh_can.py, GET /linh-can).

The testing stone on the left with the light pillar of the root carried; on the right the
root card (its name in the colour of its giai, what it does in numbers), or - after a pill roll
- the old and the new root side by side with "keep" and "take"; the tẩy linh pills with their
odds (inside the realm's cap) and pity; the giai ladder with the locked ones and the tu vi
that opens them; and the đồ giám of every root ("???" until it has been seen).

FX: `trac_linh_thach` (the stone, looping), `linh_can_tru_<giai>` (the pillar, looping) and
`linh_can_<giai>` (the one-shot reveal burst) come from art2 when their sheets exist; until
then the stone is the crystal on a lit pedestal, the pillar the aura of a realm and the burst
dot_pha / thang_cap. Nothing here is drawn by hand beyond panels, bars and text."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..engine import art2
from .base import Scene

PANEL = "#1D1A22"          # the night behind the stone: every giai colour reads on it
CARD = "#2A2631"
INK_LIGHT = "#EDE6D6"
INK_DIM = "#9C93A3"
AURAS = ("luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua")
REVEAL_SECONDS = 2.4
STONE_ZOOM = 1.4
X, Y, W, H = 8, 20, 464, 244


def _rgb(color: str, k: float = 1.0) -> tuple[int, int, int]:
    c = pygame.Color(color)
    return int(c.r * k), int(c.g * k), int(c.b * k)


def short_name(name: str) -> str:
    return name.replace(" Linh Căn", "").replace("Linh Căn", "").strip() or name


class LinhCanScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.v: dict | None = None
        self.tab = "main"
        self.busy = False
        self.sel_pill: str | None = None
        self.reveal: dict | None = None        # {"root", "t", "then"}: the burst after a test
        self.t = 0.0
        self.reload()

    # ------------------------------------------------------------ server
    def reload(self) -> None:
        self.api.get("/linh-can", self._got, self.game.api_error)

    def _got(self, v: dict) -> None:
        self.v = v
        if self.sel_pill is None and v.get("pills"):
            have = [p for p in v["pills"] if p.get("have")]
            self.sel_pill = (have or v["pills"])[0]["id"]

    def _call(self, path: str, body: dict | None, then) -> None:
        if self.busy:
            return
        self.busy = True

        def ok(r):
            self.busy = False
            if r.get("view"):
                self.v = r["view"]
            then(r)

        def err(e):
            self.busy = False
            self.game.api_error(e)
        self.api.post(path, body or {}, ok, err)

    def awaken(self) -> None:
        self._call("/linh-can/awaken", None, lambda r: self._reveal(r["root"], None))

    def roll(self, pill: str) -> None:
        def then(r):
            msg = T.LC_SAME.format(name=r["rolled"]["name_vi"]) if r.get("same") else None
            self._reveal(r["rolled"], msg)
        self._call("/linh-can/roll", {"pill": pill}, then)

    def choose(self, keep: bool) -> None:
        def then(r):
            root = r.get("root") or {}
            if r.get("took"):
                self.game.toast(T.LC_TOOK.format(name=root.get("name_vi", "")), root.get("color", "#C99A3A"))
                self.game.audio.play("discover")
            else:
                self.game.toast(T.LC_KEPT.format(name=root.get("name_vi", "")), "#6A994E")
            self.game.refresh_cult()
        self._call("/linh-can/choose", {"keep": keep}, then)

    def _reveal(self, root: dict, then_msg: str | None) -> None:
        self.reveal = {"root": root, "t": 0.0, "msg": then_msg}
        self.game.audio.play("discover")
        self.game.refresh_cult()

    # ------------------------------------------------------------ loop
    def update(self, dt, top):
        self.t += dt
        if self.reveal is not None:
            self.reveal["t"] += dt

    def _end_reveal(self) -> None:
        r = self.reveal
        self.reveal = None
        if r and r.get("msg"):
            self.game.toast(r["msg"], "#9C93A3")

    # ------------------------------------------------------------ drawing helpers
    def _fx(self, ui, fid: str, t: float, x: float, y: float, scale: float = 1.0) -> bool:
        """An FX sheet with its pivot on (x, y) in base units, at the display scale."""
        if art2.fx(fid) is None:
            return False
        wx, wy = ui.d.to_window(x, y)
        return art2.draw_fx(ui.win, fid, t, wx, wy, scale=scale * ui.s)

    def _stone(self, ui, cx: float, base: float, giai: int, k: float = 1.0) -> None:
        """The light pillar of a giai, then the Trắc Linh Thạch on top of it (k: size)."""
        aura = AURAS[min(len(AURAS) - 1, max(0, giai - 2))]
        own = bool(giai) and self._fx(ui, f"linh_can_tru_{giai}", self.t, cx, base, k)
        if giai and not own:
            self._fx(ui, f"aura_{aura}_back", self.t, cx, base - 4, (1.0 + giai * 0.06) * k)
        z = STONE_ZOOM * k
        if not self._fx(ui, "trac_linh_thach", self.t, cx, base, z):
            self._stone_props(ui, cx, base, z)
        if giai and not own:
            self._fx(ui, f"aura_{aura}_front", self.t, cx, base - 4, (0.8 + giai * 0.05) * k)

    def _stone_props(self, ui, cx: float, base: float, z: float) -> None:
        """Until the stone has its own sheet: the crystal standing on a lit pedestal."""
        ped = art2.prop("pedestal_lit", "realm") or art2.prop("pedestal_on", "realm")
        top = base
        if ped is not None:
            ui.image(ped.at(self.t), cx, base, zoom=z, anchor="midbottom")
            top = base - (ped.img.get_height() - ped.img.get_bounding_rect().top) * z + 6 * z
        crystal = art2.prop("crystal_2", "nature") or art2.prop("crystal_1", "nature")
        if crystal is not None:
            pad = crystal.img.get_height() - crystal.img.get_bounding_rect().bottom
            ui.image(crystal.at(self.t), cx, top + pad * z, zoom=z, anchor="midbottom")

    def _card(self, ui, root: dict | None, x: float, y: float, w: float, h: float, title: str | None = None,
              cols: int = 2) -> None:
        ui.fill(x, y, w, h, CARD)
        ui.border(x, y, w, h, _rgb(root["color"], 0.8) if root else "#4A4452")
        ty = y + 4
        if title:
            ui.text(title, x + 6, ty, 6, INK_DIM)
            ty += 9
        if root is None:
            ui.text(T.LC_NONE, x + w / 2, y + h / 2 - 8, 10, INK_DIM, anchor="center")
            ui.text(T.LC_NONE_HINT, x + w / 2, y + h / 2 + 4, 7, INK_DIM, anchor="midtop", max_w=w - 16)
            return
        r = ui.text(root["name_vi"], x + 6, ty, 9, root["color"], max_w=w - 12)
        ty = r.bottom + 2
        he = T.LC_HE.format(he=", ".join(root["he_vi"])) if root.get("he_vi") else T.LC_HE_NONE
        r = ui.text(f"{T.LC_KIND.format(giai=root['giai_vi'], loai=root['loai_vi'])} · {he}", x + 6, ty, 6, INK_DIM,
                    max_w=w - 12)
        ty = r.bottom + 3
        effs = root.get("effects_vi") or []
        cols = 1 if len(effs) <= 4 else cols
        cw = (w - 12) / cols
        rows = (len(effs) + cols - 1) // cols
        for i, e in enumerate(effs):
            ex = x + 6 + (i // rows) * cw if cols > 1 else x + 6
            ey = ty + (i % rows) * 9 if cols > 1 else ty + i * 9
            ui.text(f"+ {e}", ex, ey, 6, "#B9E08C" if i == 0 else INK_LIGHT, max_w=cw - 4)
        ty += rows * 9 + 2 if cols > 1 else len(effs) * 9 + 2
        if ty < y + h - 10:
            r = ui.text(root["desc_vi"], x + 6, ty, 6, INK_DIM, max_w=w - 12)
            lore = root.get("lore_vi")
            if lore and r.bottom + 2 + ui.text_size(lore, 6)[1] * 2 < y + h - 2:
                ui.text(lore, x + 6, r.bottom + 2, 6, "#7D7486", max_w=w - 12)

    def _odds_bar(self, ui, odds: list[dict], x: float, y: float, w: float, h: float) -> None:
        colors = {g["id"]: g["color"] for g in self.v["giai"]}
        ui.fill(x, y, w, h, "#0F0D12")
        cx = x
        for o in odds:
            ow = max(1.0, w * o["p"])
            ui.fill(cx, y, min(ow, x + w - cx), h, colors.get(o["giai"], "#888888"))
            cx += ow
            if cx >= x + w:
                break

    def _odds_text(self, odds: list[dict]) -> str:
        parts = []
        for o in odds:
            p = o["p"] * 100
            ps = f"{p:.0f}%" if p >= 1 else (f"{p:.1f}%" if p >= 0.1 else f"{p:.2f}%")
            parts.append(f"{T.LC_SHORT.get(o['giai'], o['giai'])} {ps}")
        return " · ".join(parts)

    # ------------------------------------------------------------ the screen
    def draw_ui(self, ui):
        ui.dim(170)
        ui.panel(X, Y, W, H, T.LC_TITLE, color=PANEL, edge="#6B5E7A")
        v = self.v
        if ui.button("lc_close", X + W - 50, Y + 8, 42, 13, T.CLOSE, size=7, key=pygame.K_ESCAPE):
            self.close()
            return
        if v is None:
            ui.text("...", 240, 135, 10, INK_LIGHT, anchor="center")
            return
        if ui.button("lc_tab_main", X + 8, Y + 8, 70, 13, T.LC_TAB_MAIN, size=7, selected=self.tab == "main"):
            self.tab = "main"
        if ui.button("lc_tab_book", X + 82, Y + 8, 90, 13, T.LC_TAB_BOOK.format(n=v["discovered"], t=v["total"]),
                     size=7, selected=self.tab == "book"):
            self.tab = "book"
        ui.text(T.LC_CAP.format(giai=v["cap"]["name_vi"]), X + W - 56, Y + 11, 7,
                next(g["color"] for g in v["giai"] if g["id"] == v["cap"]["giai"]), anchor="topright")
        if self.tab == "book":
            self.draw_book(ui)
        else:
            self.draw_main(ui)
        self.draw_ladder(ui)
        if self.reveal is not None:
            self.draw_reveal(ui)

    def draw_main(self, ui):
        v = self.v
        root, pending = v.get("root"), v.get("pending")
        # the stone and the pillar of the root carried
        sx, sy = X + 82, Y + 196
        self._stone(ui, sx, sy, (root or {}).get("giai_index", 0))
        if root:
            ui.text(root["name_vi"], sx, sy + 5, 8, root["color"], anchor="midtop", max_w=150)
        rx, rw = X + 168, W - 176
        if not v["awakened"]:
            self._card(ui, None, rx, Y + 28, rw, 92)
            ui.text(T.LC_AWAKEN_ODDS.format(odds=self._odds_text(v["awaken_odds"])), rx, Y + 128, 7, INK_DIM,
                    max_w=rw)
            if ui.button("lc_awaken", sx - 60, Y + 166, 120, 16, T.LC_AWAKEN, style="gold",
                         enabled=not self.busy and self.reveal is None, key=pygame.K_RETURN):
                self.awaken()
            return
        if pending:
            ui.text(T.LC_CHOOSE, rx, Y + 28, 7, INK_LIGHT, max_w=rw)
            cw = (rw - 6) / 2
            self._card(ui, root, rx, Y + 40, cw, 150, T.LC_OLD, cols=1)
            self._card(ui, pending, rx + cw + 6, Y + 40, cw, 150, T.LC_NEW, cols=1)
            ok = not self.busy and self.reveal is None
            if ui.button("lc_keep", rx + cw / 2 - 36, Y + 194, 72, 15, T.LC_KEEP, enabled=ok):
                self.choose(True)
            if ui.button("lc_take", rx + cw + 6 + cw / 2 - 36, Y + 194, 72, 15, T.LC_TAKE, style="gold",
                         enabled=ok):
                self.choose(False)
            return
        self._card(ui, root, rx, Y + 28, rw, 84)
        self.draw_pills(ui, rx, Y + 118, rw)

    def draw_pills(self, ui, x: float, y: float, w: float) -> None:
        v = self.v
        ui.text(T.LC_PILLS, x, y, 7, "#E9C46A")
        row_h = 16
        sel = None
        for i, p in enumerate(v["pills"]):
            ry = y + 10 + i * row_h
            chosen = p["id"] == self.sel_pill
            if chosen:
                sel = p
                ui.fill(x, ry - 1, w, row_h - 1, "#3A3442")
            if ui.click_in(x, ry - 1, w - 44, row_h - 1):
                self.sel_pill = p["id"]
            icon = art2.item_icon({"item_id": p["id"], "kind": "pill"}) if art2.on() else None
            if icon is not None:
                ui.image(icon, x + 1, ry, zoom=0.4)
            ui.text(p["name_vi"], x + 17, ry, 7, INK_LIGHT if p["have"] else INK_DIM)
            ui.text(T.LC_HAVE.format(n=p["have"]), x + 128, ry, 6, "#E9C46A" if p["have"] else INK_DIM)
            self._odds_bar(ui, p["odds"], x + 17, ry + 9, 100, 3)
            pity = p.get("pity")
            if pity:
                txt = (T.LC_PITY_NOW.format(giai=pity["floor_vi"]) if pity["left"] <= 1 else
                       T.LC_PITY.format(n=pity["left"], giai=pity["floor_vi"]))
                ui.text(txt, x + 128, ry + 7, 6, INK_DIM)
            if ui.hover(x, ry - 1, w - 44, row_h - 1):
                ui.set_tooltip(f"{p['desc_vi']}\n{self._odds_text(p['odds'])}")
            if ui.button(f"lc_roll_{p['id']}", x + w - 40, ry, 38, 12, T.LC_USE, size=7, style="gold",
                         enabled=bool(p["have"]) and not self.busy and self.reveal is None):
                self.sel_pill = p["id"]
                self.roll(p["id"])
        if sel is not None:
            oy = y + 12 + len(v["pills"]) * row_h
            line = (T.LC_ODDS.format(pill=sel["name_vi"], odds=self._odds_text(sel["odds"])) if sel["have"] else
                    T.LC_NO_PILL.format(dp=sel.get("recipe_vi", "")))
            ui.text(line, x, oy, 6, INK_LIGHT if sel["have"] else INK_DIM, max_w=w)

    def draw_ladder(self, ui):
        """The nine giai: the colour of each, the ones above the cap dimmed with the tu vi that opens them."""
        v = self.v
        n = len(v["giai"])
        gw = (W - 16) / n
        y = Y + H - 17
        for i, g in enumerate(v["giai"]):
            gx = X + 8 + i * gw
            col = _rgb(g["color"], 1.0 if g["open"] else 0.35)
            ui.fill(gx + 1, y, gw - 2, 11, col)
            ui.text(T.LC_SHORT.get(g["id"], g["name_vi"]), gx + gw / 2, y + 5.5, 6,
                    "#1D1A22" if g["open"] else "#8E8496", anchor="center")
            if not g["open"] and ui.hover(gx, y, gw, 11):
                ui.set_tooltip(T.LC_LOCKED_AT.format(giai=g["name_vi"], need=g.get("need_vi") or ""))

    def draw_book(self, ui):
        v = self.v
        ui.text(T.LC_BOOK_HINT, X + 8, Y + 25, 6, INK_DIM, max_w=W - 16)
        rows: dict[str, list[dict]] = {}
        for b in v["book"]:
            rows.setdefault(b["giai"], []).append(b)
        y0, lw, cw, ch = Y + 35, 34, 45, 20
        for i, g in enumerate(v["giai"]):
            ry = y0 + i * (ch + 1)
            ui.text(T.LC_SHORT.get(g["id"], g["name_vi"]), X + 8, ry + ch / 2, 6, g["color"], anchor="midleft")
            for k, b in enumerate(rows.get(g["id"], [])):
                bx = X + 8 + lw + k * cw
                seen = b["discovered"]
                ui.fill(bx, ry, cw - 2, ch, _rgb(g["color"], 0.42) if seen else "#25212B")
                ui.border(bx, ry, cw - 2, ch, _rgb(g["color"], 0.9) if seen else "#3A3442")
                mine = (v.get("root") or {}).get("id") == b["id"]
                label = (b.get("short_vi") or short_name(b["name_vi"])) if seen else T.LC_UNKNOWN
                ui.text(label, bx + (cw - 2) / 2, ry + ch / 2, 6, "#FFFFFF" if seen else "#5E5666",
                        anchor="center", max_w=cw - 4, line_gap=1.0)
                if mine:
                    ui.border(bx - 1, ry - 1, cw, ch + 2, "#FFFFFF")
                if seen and ui.hover(bx, ry, cw - 2, ch):
                    ui.set_tooltip(f"{b['name_vi']}\n{b['giai_vi']} · {b['loai_vi']}\n" + "\n".join(b["effects_vi"]))

    def draw_reveal(self, ui):
        """A stage of its own: the stone in the middle, the pillar of the giai that came out
        rising behind it, the burst on the stone (bigger for a higher giai) with a flash in the
        giai's colour, then the name."""
        r = self.reveal
        root, t = r["root"], r["t"]
        g = root["giai_index"]
        ui.fill(0, 0, 480, 270, (10, 8, 14, 235))
        cx, base = 240, 182
        grow = min(1.0, t / 0.5)
        self._stone(ui, cx, base, g if t > 0.15 else 0, 1.0 + 0.1 * grow)
        scale = 0.7 + 0.14 * g
        if not self._fx(ui, f"linh_can_{g}", t, cx, base - 26, scale):
            self._fx(ui, "dot_pha", t, cx, base - 26, scale)
        flash = max(0.0, 1.0 - t / 0.5)
        if flash > 0:
            ui.fill(0, 0, 480, 270, (*_rgb(root["color"]), int((60 + 12 * g) * flash)))
        if t > 0.6:
            size = 10 + min(6, g)
            ui.text(root["name_vi"], cx + 0.7, base + 12.7, size, "#0A080E", anchor="midtop")
            ui.text(root["name_vi"], cx, base + 12, size, root["color"], anchor="midtop")
            ui.text(f"{root['giai_vi']} · {root['loai_vi']}", cx, base + 16 + size * 1.3, 7, INK_LIGHT,
                    anchor="midtop")
        if t > 1.2:
            ui.text(T.LC_REVEAL_SKIP, cx, 258, 6, INK_DIM, anchor="center")
        if (t > REVEAL_SECONDS or (t > 0.4 and (ui.consume_click() or ui.key(pygame.K_RETURN)
                                                 or ui.key(pygame.K_SPACE)))):
            self._end_reveal()
