"""Chỉ Đường's two screens (docs/CHI_DUONG.md):

* `NavPicker` (N): where to go - the khu that fits the player's tu vi (the server's
  recommendation, GET /nav/destinations, with its reason), the other open lands, the locked ones
  with why, Về Động Phủ, Về Trúc Lâm Thôn, Thiên Địa Đồ, Tắt chỉ đường.
* `WorldMapScene` (M), Thiên Địa Đồ: the zone in full with its khu named and tinted by band and
  the stages they fit, the gates, the named places, the player and the way; and the world: every
  land round the village with open / locked and why. Choosing a khu or a land sets the arrow.
"""
from __future__ import annotations

import math

import pygame

from .. import strings_nav_vi as N
from .. import strings_vi as T
from ..engine import chi_duong
from ..engine import minimap as MM
from ..engine import navigator as nv
from .base import Scene

BAND_COLOURS = {0: (110, 170, 220), 1: (120, 190, 100), 2: (230, 180, 70), 3: (215, 85, 80)}
GOLD = "#C99A3A"
GOLD_TEXT = "#8A6414"
GREY = "#6E675C"
RED = "#A23B3D"
GREEN = "#4F7A38"
POI_COLOURS = {"gate": "#8CB8DA", "camp": "#F2C14E", "bi_canh": "#8E5AC8", "npc": "#F4EBD9",
               "beast": "#B5D67A", "boss": "#F08A8C", "landmark": "#E3D5BA"}


def fit(ui, text: str, size: float, w: float) -> str:
    if ui.text_size(text, size)[0] <= w:
        return text
    while text and ui.text_size(text + "...", size)[0] > w:
        text = text[:-1]
    return text.rstrip() + "..."


def range_vi(realm: str, lo, hi) -> str:
    if lo is None:
        return ""
    return f"{realm} tầng {lo}" if lo == hi else f"{realm} tầng {lo}-{hi}"


def dest_line(d: dict) -> str:
    """'Ngoại Vi · Kiếm Trủng Sơn' for a khu, the land's name for a land without khu."""
    if d.get("khu") and d.get("land_vi") and d.get("land_vi") != d.get("name_vi"):
        return f"{d['name_vi']} · {d['land_vi']}"
    return d.get("name_vi") or d.get("land_vi") or ""


# ------------------------------------------------------------------ the picker
class NavPicker(Scene):
    """The list of places Chỉ Đường can lead to. Every choice is a button `nav_pick_<n>`."""

    W = 270
    toast_y = 252                     # under the panel: the toasts never cover its title or rows

    def __init__(self, game, scene):
        super().__init__(game)
        self.scene = scene
        self.nav = chi_duong.of(game)
        self.nav.refresh(force=True)

    def rows(self) -> list[tuple]:
        """(widget id, label, sub-line, destination or action, enabled, style, tooltip)."""
        nav, data = self.nav, self.nav.data or {}
        out = []
        rec = data.get("recommended")
        if rec:
            out.append(("nav_pick_rec", f"{N.RECOMMENDED}: {dest_line(rec)}",
                        rec.get("reason_vi") or rec.get("fit_vi") or "", rec, True, "gold", rec.get("reason_vi")))
        for d in data.get("lands") or []:
            out.append((f"nav_pick_{d.get('land')}", dest_line(d), d.get("fit_vi") or "", d, True, "normal",
                        d.get("reason_vi")))
        for d in data.get("locked") or []:
            out.append((f"nav_lock_{d.get('land')}", d.get("name_vi", ""), d.get("reason_vi") or "", None, False,
                        "normal", d.get("reason_vi")))
        out.append(("nav_pick_home", f"{N.GO_HOME} (H)" if hasattr(self.scene, "zone_id") else N.GO_HOME, "",
                    nav.pick("home"), chi_duong.scene_zone(self.scene) != chi_duong.HOME, "normal", None))
        out.append(("nav_pick_village", N.GO_VILLAGE, "", nav.pick("village"), True, "normal", None))
        out.append(("nav_open_map", f"{N.OPEN_MAP} (M)" if hasattr(self.scene, "zone_id") else N.OPEN_MAP, "",
                    "map", True, "normal", None))
        if nav.dest is not None:
            out.append(("nav_off", N.TURN_OFF, "", "off", True, "dark", None))
        return out

    def choose(self, what) -> None:
        nav = self.nav
        self.close()
        if what == "off":
            nav.set_dest(None)
        elif what == "map":
            from ..ui.nav_hud import open_map
            open_map(self.scene)
        elif isinstance(what, dict):
            here = chi_duong.scene_zone(self.scene)
            if what.get("kind") not in ("home",) and what.get("zone") == here and not what.get("khu") \
                    and what.get("kind") != "village":
                self.game.toast(N.ALREADY_THERE.format(name=what.get("name_vi", "")), "#8E877A")
                return
            nav.set_dest(what, here)

    def draw_ui(self, ui):
        ui.dim(110)
        rows = self.rows()
        x, w = (480 - self.W) / 2, self.W
        tw = w - 30                                     # the text width inside a row
        subs = []
        for r in rows:
            lines = ui.f.wrap(r[2], 7, int(tw * ui.s), ui.s) if r[2] else []
            if len(lines) > 2 or (len(lines) == 2 and r[0] != "nav_pick_rec"):
                lines = [fit(ui, lines[0] + " " + lines[1], 7, tw)] if r[0] != "nav_pick_rec" else \
                    [lines[0], fit(ui, lines[1] + " ...", 7, tw)]
            subs.append(lines)
        heights = [14 + 9 * len(s) for s in subs]
        h = min(262, 28 + sum(heights) + 4 + (14 if self.nav.data is None else 0))
        y = max(4, (270 - h) / 2)
        ui.panel(x, y, w, h, N.TITLE)
        ui.text(N.PICK_HINT, x + w / 2, y + 10, 7, GREY, anchor="midtop")
        cy = y + 22
        if self.nav.data is None:
            ui.text(N.ASK_FAILED if self.nav.failed else N.ASKING, x + w / 2, cy + 2, 8, GREY, anchor="midtop")
            cy += 14
        n = 0
        for (wid, label, sub, what, enabled, style, tip), lines, rh in zip(rows, subs, heights):
            if cy + rh > y + h - 3:
                break
            n += 1 if enabled else 0
            key = getattr(pygame, f"K_{n}") if enabled and n <= 9 else None
            bh = rh - 2
            shown = f"{n}  {label}" if enabled and n <= 9 else label
            if ui.button(wid, x + 10, cy, w - 20, bh, "", key=key, enabled=enabled, style=style, tooltip=tip):
                self.choose(what)
                return
            col = "#FFFFFF" if style == "dark" else ("#8E877A" if not enabled else "#2B2B2B")
            if lines:
                ui.text(fit(ui, shown, 8, tw), x + 15, cy + 1, 8, col)
                for k, line in enumerate(lines):
                    ui.text(line, x + 15, cy + 12 + 9 * k, 7, RED if not enabled else GOLD_TEXT)
            else:
                ui.text(fit(ui, shown, 8, tw), x + 15, cy + bh / 2, 8, col, anchor="midleft")
            cy += rh
        if ui.key(pygame.K_ESCAPE) or ui.key(pygame.K_n) or (ui.inp.clicked and not ui.hover(x, y, w, h)):
            self.close()


# ------------------------------------------------------------------ Thiên Địa Đồ
class WorldMapScene(Scene):
    """The big map. View "zone" (this zone in full) or "world" (the lands round the village)."""

    AREA = (8, 24, 464, 218)          # x, y, w, h of the map area
    toast_y = 40                      # toasts over the top of the map, not over its title or legend

    def __init__(self, game, scene, view: str = "zone"):
        super().__init__(game)
        self.scene = scene
        self.nav = chi_duong.of(game)
        self.nav.refresh(force=True)
        self.view = view if chi_duong.scene_zone(scene) not in (None, chi_duong.HOME) else "world"
        self.zone = chi_duong.scene_zone(scene)
        self._pic = None
        self.full_route: list = []
        self._route_for = None

    # ---- the zone view
    def zone_layout(self):
        """(picture, x, y, k): the zone's overview scaled into the area, k = screen px per world px."""
        if self._pic is None:
            tmap = self.scene.map
            ov = MM.overview(tmap)
            ax, ay, aw, ah = self.AREA
            s = min(aw / tmap.w, ah / tmap.h)
            if s >= 1:
                s = math.floor(s)
                pic = pygame.transform.scale(ov, (int(tmap.w * s), int(tmap.h * s)))
            else:
                pic = pygame.transform.smoothscale(ov, (max(1, int(tmap.w * s)), max(1, int(tmap.h * s))))
            px = ax + (aw - pic.get_width()) / 2
            py = ay + (ah - pic.get_height()) / 2
            self._pic = (pic, px, py, s / tmap.tw)
        return self._pic

    def route(self) -> list:
        """The whole way in this zone (computed once per opening, it is long on a giant map)."""
        nav = self.nav
        if nav.leg is None or not nav.leg.ready:
            return nav.route
        key = (id(nav.leg), int(self.scene.player.x) // 32, int(self.scene.player.y) // 32)
        if key != self._route_for:
            self._route_for = key
            r = nav.leg.read(self.scene.player.x, self.scene.player.y, route_cells=6000)
            self.full_route = r.route if r.mode == "path" else []
        return self.full_route

    def draw_zone(self, ui) -> None:
        tmap = self.scene.map
        pic, px, py, k = self.zone_layout()
        ui.fill(px - 2, py - 2, pic.get_width() + 4, pic.get_height() + 4, "#3A342C")
        ui.image(pic, px, py)
        hover_tip = None
        realm = self.nav.realm_vi
        ws = self.nav.working_stage
        khus = chi_duong.khu_objects(tmap)
        taken: list[pygame.Rect] = []                 # labels already drawn (the player's avoids them)
        for (rx, ry, rw, rh), props in khus:
            band = chi_duong.num(props.get("band"))
            col = BAND_COLOURS.get(band, BAND_COLOURS[1])
            sx, sy, sw, sh = px + rx * k, py + ry * k, rw * k, rh * k
            ui.fill(sx, sy, sw, sh, (*col, 60))
            ui.border(sx, sy, sw, sh, col)
            lo, hi = chi_duong.num(props.get("stage_min")), chi_duong.num(props.get("stage_max"))
            name = props.get("name_vi") or props.get("khu") or ""
            stage = N.SAFE if band == 0 else f"tầng {lo}-{hi}" if lo != hi else f"tầng {lo}"
            if sw > 40 and sh > 20:            # the name in the khu's top-left corner, the stages under it
                label = fit(ui, name, 8, sw - 6)
                warn = band > 0 and ws is not None and lo > ws
                lw = max(ui.text_size(label, 8)[0], ui.text_size(stage, 7)[0]) + 4
                ui.fill(sx + 1, sy + 1, lw, 18, (20, 18, 15, 150))
                taken.append(pygame.Rect(int(sx + 1), int(sy + 1), int(lw), 18))
                ui.text(label, sx + 3, sy + 1, 8, "#FFFFFF")
                ui.text(stage, sx + 3, sy + 10, 7, "#F08A8C" if warn else "#F4EBD9")
            if ui.hover(sx, sy, sw, sh):
                hover_tip = f"{name}\n{N.BAND_NAMES.get(band, '')} · " + (
                    N.SAFE if band == 0 else range_vi(realm, lo, hi)) + (
                    f"\n{props.get('desc_vi')}" if props.get("desc_vi") else "")
                if ui.click_in(sx, sy, sw, sh) and band > 0:
                    d = chi_duong.khu_dest(self.zone, (rx, ry, rw, rh), props,
                                           T.ZONE_NAMES.get(self.zone, self.zone))
                    self.close()
                    self.nav.set_dest(d, self.zone)
                    return
        clip = ui.win.get_clip()
        ui.win.set_clip(ui.rect(px, py, pic.get_width(), pic.get_height()))
        for o in tmap.find("portal"):
            sx, sy = px + o.x * k, py + o.y * k
            ui.fill(sx, sy, max(3, o.w * k), max(3, o.h * k), "#8CB8DA")
            ui.border(sx, sy, max(3, o.w * k), max(3, o.h * k), "#2B1D0E")
            name = T.ZONE_NAMES.get(o.props.get("target"), o.props.get("target", ""))
            tx = min(max(sx + o.w * k / 2, px + 30), px + pic.get_width() - 30)
            ty = min(max(sy + o.h * k / 2, py + 8), py + pic.get_height() - 8)
            nw = ui.text_size(name, 7)[0]
            ui.fill(tx - nw / 2 - 2, ty - 4, nw + 4, 9, (20, 18, 15, 170))
            ui.text(name, tx, ty, 7, "#D6ECFA", anchor="center")
            taken.append(pygame.Rect(int(tx - nw / 2 - 2), int(ty - 4), int(nw + 4), 9))
        for o in tmap.find("poi"):
            sx, sy = px + (o.x + o.w / 2) * k, py + (o.y + o.h / 2) * k
            c = POI_COLOURS.get(o.props.get("poi", "landmark"), "#E3D5BA")
            pygame.draw.polygon(ui.win, pygame.Color("#2B1D0E"), [ui.d.to_window(sx, sy - 4), ui.d.to_window(sx + 4, sy),
                                                                ui.d.to_window(sx, sy + 4), ui.d.to_window(sx - 4, sy)])
            pygame.draw.polygon(ui.win, pygame.Color(c), [ui.d.to_window(sx, sy - 3), ui.d.to_window(sx + 3, sy),
                                                        ui.d.to_window(sx, sy + 3), ui.d.to_window(sx - 3, sy)])
            name = o.props.get("name_vi") or o.name
            if ui.hover(sx - 5, sy - 5, 10, 10):
                hover_tip = name
            elif len(tmap.find("poi")) <= 24:
                ui.text(name, sx, sy + 5, 6, "#FFFFFF", anchor="midtop")
        pts = [(px + x * k, py + y * k) for x, y in self.route()]
        MM.polyline(ui, pts, MM.ROUTE, 1)
        if self.nav.leg is not None and self.nav.dest is not None:
            gx, gy = self.nav.leg.aim
            gx, gy = px + gx * k, py + gy * k
            r = 3 + (1 if int(self.game.now * 3) % 2 else 0)
            ui.fill(gx - r - 1, gy - r - 1, 2 * r + 2, 2 * r + 2, "#2B1D0E")
            ui.fill(gx - r, gy - r, 2 * r, 2 * r, "#F2C14E")
        p = self.scene.player
        mx, my = px + p.x * k, py + p.y * k
        ui.fill(mx - 3, my - 3, 6, 6, "#2B1D0E")
        ui.fill(mx - 2, my - 2, 4, 4, "#E9C46A" if int(self.game.now * 4) % 2 else "#FFFFFF")
        ui.win.set_clip(clip)
        yw, yh = ui.text_size(N.YOU, 7)
        spots = [(mx - yw / 2, my - 5 - yh), (mx - yw / 2, my + 5), (mx + 6, my - yh / 2), (mx - 6 - yw, my - yh / 2),
                 (mx + 6, my - 14 - yh), (mx - 6 - yw, my - 14 - yh), (mx + 6, my + 12), (mx - 6 - yw, my + 12),
                 (mx - yw / 2, my - 24 - yh), (mx - yw / 2, my + 22)]
        lx, ly = next(((sx, sy) for sx, sy in spots
                       if pygame.Rect(int(sx), int(sy), int(yw), int(yh)).collidelist(taken) == -1), spots[0])
        ui.fill(lx - 1, ly, yw + 2, yh, (20, 18, 15, 150))
        ui.text(N.YOU, lx, ly, 7, "#FFFFFF")
        ui.border(px - 2, py - 2, pic.get_width() + 4, pic.get_height() + 4, "#8B5A2B")
        # legend
        ax, ay, aw, ah = self.AREA
        ly = ay + ah + 2
        if khus:
            lx = ax
            for band in (1, 2, 3, 0):
                lo, hi = {1: (1, 3), 2: (4, 6), 3: (7, 9), 0: (0, 0)}[band]
                label = f"{N.BAND_NAMES[band]} " + ("" if band == 0 else f"tầng {lo}-{hi}")
                ui.fill(lx, ly + 2, 7, 7, BAND_COLOURS[band])
                ui.border(lx, ly + 2, 7, 7, "#2B1D0E")
                lx = ui.text(label.strip(), lx + 10, ly + 1, 7, "#F4EBD9").right + 10
        else:
            ui.text(N.NO_KHU, ax, ly + 1, 7, "#F4EBD9")
        if hover_tip:
            ui.set_tooltip(hover_tip)

    # ---- the world view
    def world_boxes(self) -> list[dict]:
        """Every land with a gate in the village, placed in the direction of its gate."""
        zones = nv.world_zones()
        hub = zones.get(chi_duong.HUB)
        data = self.nav.data or {}
        by_zone = {}
        rec = data.get("recommended")
        for d in ([rec] if rec else []) + list(data.get("lands") or []) + list(data.get("locked") or []):
            by_zone.setdefault(d.get("zone"), d)
        ax, ay, aw, ah = self.AREA
        cx, cy = ax + aw / 2, ay + ah / 2 + 4
        boxes = [{"zone": chi_duong.HUB, "name": T.ZONE_NAMES.get(chi_duong.HUB, ""), "x": cx, "y": cy,
                  "dest": self.nav.pick("village"), "open": True, "why": ""}]
        if hub is None:
            return boxes
        for g in hub.gates:
            gx, gy, gw, gh = g.rect
            rx = (gx + gw / 2) / hub.px_w * 2 - 1
            ry = (gy + gh / 2) / hub.px_h * 2 - 1
            m = max(abs(rx), abs(ry)) or 1.0
            rx, ry = rx / m, ry / m
            x = cx + rx * (aw / 2 - 52)
            y = cy + ry * (ah / 2 - 24)
            if g.target == chi_duong.HOME:
                boxes.append({"zone": chi_duong.HOME, "name": N.HOME_BOX, "x": x, "y": y,
                              "dest": self.nav.pick("home"), "open": True, "why": "", "home": True})
                continue
            d = by_zone.get(g.target)
            boxes.append({"zone": g.target, "name": T.ZONE_NAMES.get(g.target, g.target), "x": x, "y": y,
                          "dest": d if d and d.get("open", True) and d.get("kind") != "locked" else None,
                          "open": bool(d) and d.get("kind") != "locked",
                          "why": (d or {}).get("reason_vi") or "", "rec": d is rec and rec is not None,
                          "line": dest_line(d) if d and d.get("khu") else ""})
        self.spread(boxes[1:], cx, cy)
        return boxes

    BOX_W, BOX_H = 92, 26

    def spread(self, boxes: list[dict], cx: float, cy: float) -> None:
        """Gates side by side on one edge of the village give boxes that touch: push them apart
        along that edge, keeping them inside the area."""
        ax, ay, aw, ah = self.AREA
        for horizontal in (True, False):
            sides: dict = {}
            for b in boxes:
                on_top_or_bottom = abs(b["y"] - cy) >= (ah / 2 - 24) - 0.5
                if on_top_or_bottom == horizontal:
                    sides.setdefault(round(b["y"] if horizontal else b["x"]), []).append(b)
            for row in sides.values():
                key, gap = ("x", self.BOX_W + 6) if horizontal else ("y", self.BOX_H + 6)
                lo = (ax + self.BOX_W / 2 + 2) if horizontal else (ay + self.BOX_H / 2 + 2)
                hi = (ax + aw - self.BOX_W / 2 - 2) if horizontal else (ay + ah - self.BOX_H / 2 - 2)
                row.sort(key=lambda b: b[key])
                for a, b in zip(row, row[1:]):
                    b[key] = max(b[key], a[key] + gap)
                over = row[-1][key] - hi
                if over > 0:
                    for b in row:
                        b[key] -= over
                for a, b in zip(row[::-1][1:], row[::-1]):
                    a[key] = min(a[key], b[key] - gap)
                under = lo - row[0][key]
                if under > 0:
                    for b in row:
                        b[key] += under

    def draw_world_view(self, ui) -> None:
        boxes = self.world_boxes()
        hub = boxes[0]
        ax, ay, aw, ah = self.AREA
        ui.fill(ax, ay, aw, ah, (36, 44, 30, 255))
        ui.border(ax, ay, aw, ah, "#8B5A2B")
        for b in boxes[1:]:
            pygame.draw.line(ui.win, pygame.Color("#8B7A55"), ui.d.to_window(hub["x"], hub["y"]),
                             ui.d.to_window(b["x"], b["y"]), max(1, ui.s))
        tip = None
        for i, b in enumerate(boxes):
            w, h = self.BOX_W, self.BOX_H
            x, y = b["x"] - w / 2, b["y"] - h / 2
            here = b["zone"] == self.zone
            if b.get("rec"):
                edge, fillc = "#F2C14E", (60, 48, 20, 235)
            elif b["open"]:
                edge, fillc = "#B5D67A", (30, 40, 26, 235)
            else:
                edge, fillc = "#BC4749", (40, 26, 26, 235)
            ui.fill(x, y, w, h, fillc)
            ui.border(x, y, w, h, edge, 2 if b.get("rec") or here else 1)
            ui.text(fit(ui, b["name"], 8, w - 6), b["x"], y + 2, 8, "#FFFFFF", anchor="midtop")
            if b.get("rec"):
                status, col = N.RECOMMENDED, "#F2C14E"
            elif here:
                status, col = N.YOU, "#E9C46A"
            elif i == 0 or b.get("home"):
                status, col = "", "#B5D67A"
            else:
                status, col = (N.OPEN, "#B5D67A") if b["open"] else (N.LOCKED, "#F08A8C")
            if here and status != N.YOU:
                status = f"{status} · {N.YOU}" if status else N.YOU
            if status:
                ui.text(fit(ui, status, 7, w - 6), b["x"], y + 14, 7, col, anchor="midtop")
            wid = f"map_land_{b['zone']}"
            ui.widgets[wid] = ui.rect(x, y, w, h)
            if ui.hover(x, y, w, h):
                ui.fill(x, y, w, h, (255, 255, 255, 40))
                tip = b["why"] or (b.get("dest") or {}).get("reason_vi") or b.get("line") or b["name"]
                if ui.click_in(x, y, w, h) and b.get("dest"):
                    self.close()
                    if b["zone"] == self.zone and b.get("dest", {}).get("kind") not in ("home", "village") \
                            and not b["dest"].get("khu"):
                        self.game.toast(N.ALREADY_THERE.format(name=b["name"]), "#8E877A")
                        return
                    self.nav.set_dest(b["dest"], self.zone)
                    return
        if tip:
            ui.set_tooltip(tip)

    # ---- the frame
    def draw_ui(self, ui):
        ui.fill(0, 0, 480, 270, (20, 18, 15, 235))
        ui.text(N.MAP_TITLE, 10, 5, 10, "#F2C14E")
        can_zone = self.zone not in (None, chi_duong.HOME)
        bx = 300
        for view, label in (("zone", N.VIEW_ZONE), ("world", N.VIEW_WORLD)):
            if ui.button(f"map_view_{view}", bx, 5, 60, 13, label, selected=self.view == view,
                         enabled=view == "world" or can_zone):
                self.view = view
            bx += 64
        if ui.button("map_close", 432, 5, 40, 13, N.CLOSE, style="dark"):
            self.close()
            return
        if self.view == "zone" and can_zone:
            name = T.ZONE_NAMES.get(self.zone, self.zone)
            ui.text(name, 120, 6, 9, "#F4EBD9")
            self.draw_zone(ui)
            hint = N.MAP_HINT_ZONE
        else:
            self.draw_world_view(ui)
            hint = N.MAP_HINT_WORLD
        ui.text(hint, 240, 262, 7, "#B9B09E", anchor="center")
        if self.game.top is not self:
            return
        if ui.key(pygame.K_TAB) and can_zone:
            self.view = "world" if self.view == "zone" else "zone"
        if ui.key(pygame.K_ESCAPE) or ui.key(pygame.K_m):
            self.close()
