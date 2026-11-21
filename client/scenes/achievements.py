"""Thành Tựu Lục: the achievements (server systems/achievements.py, GET /achievements).

Tabs along the top: the seven categories and "Danh Hiệu". A category is a scrolling list of
rows - the icon, the name with its tier pips, the description, a progress bar with numbers,
the reward of the next tier to claim (or to reach) and "Nhận". Hidden achievements read "???"
until they are earned. The header shows the Đạo Tâm points, the next milestone and "Nhận hết".
The Danh Hiệu tab lists every title the player owns (Thành Tựu's and the library's) and wears
one through POST /books/wear, the route the library already uses.

Keys: V or Esc close, Left / Right change tab, Up / Down or the wheel scroll."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..engine import art2
from ..ui.mathdraw import fit
from .base import Scene

INK = "#2B2B2B"
GREY = "#5A5A5A"
PALE = "#8E877A"
GOLD_TEXT = "#B8862E"
GREEN = "#6A994E"
X, Y, W, H = 8, 8, 464, 256
ROW = 36
TITLES = "danh_hieu"


def tier_pips(e: dict) -> list[str]:
    """One state per tier: 'claimed', 'ready' (reached, not claimed), 'open' (not reached)."""
    return ["claimed" if t["claimed"] else ("ready" if t["reached"] else "open") for t in e["tiers"]]


def focus_tier(e: dict) -> dict | None:
    """The tier the row talks about: the lowest one to claim, else the next to reach, else the last."""
    tiers = e["tiers"]
    return (next((t for t in tiers if t["claimable"]), None) or next((t for t in tiers if not t["reached"]), None)
            or (tiers[-1] if tiers else None))


def row_state(e: dict) -> str:
    """claim | locked (reached, waiting for tu vi) | done (every tier, all claimed) | progress."""
    if e["claimable"]:
        return "claim"
    if any(t["reached"] and not t["claimed"] for t in e["tiers"]):
        return "locked"
    if e["done"]:
        return "done"
    return "progress"


class AchievementsScene(Scene):
    def __init__(self, game, tab: str | None = None):
        super().__init__(game)
        self.v: dict | None = None
        self.tab = tab
        self.first = 0
        self.busy = False
        self.reload()

    # ------------------------------------------------------------ server
    def reload(self) -> None:
        self.api.get("/achievements", self._got, self.game.api_error)

    def _got(self, v: dict) -> None:
        self.v = v
        if self.tab is None:     # open on the first category with something to claim
            c = next((c for c in v["categories"] if c["claimable"]), v["categories"][0])
            self.tab = c["id"]

    def _after_claim(self, r: dict) -> None:
        self.busy = False
        got = []
        for c in r.get("claimed", []):
            got += c.get("rewards_vi", [])
        if r.get("milestone"):
            r.setdefault("milestones", []).append(r["milestone"])
        for m in r.get("milestones", []):
            got += m.get("rewards_vi", [])
        if got:
            self.game.toast(fit(self.game.ui, T.ACH_GOT.format(r=", ".join(got)), 9, 440), "#6A994E")
        self.game.audio.play("coin")
        if r.get("view"):
            self.v = r["view"]
        self.game.refresh_me()
        self.game.refresh_inv()

    def _err(self, e) -> None:
        self.busy = False
        self.game.api_error(e)

    def claim(self, aid: str, tier: int) -> None:
        self.busy = True
        self.api.post("/achievements/claim", {"id": aid, "tier": tier}, self._after_claim, self._err)

    def claim_all(self) -> None:
        self.busy = True
        self.api.post("/achievements/claim-all", {}, self._after_claim, self._err)

    def claim_milestone(self, points: int) -> None:
        self.busy = True
        self.api.post("/achievements/milestone", {"points": points}, self._after_claim, self._err)

    def wear(self, title: str) -> None:
        self.busy = True

        def ok(r):
            self.busy = False
            self.game.state.me["title"] = r.get("title")
            if self.v is not None:
                self.v["title"] = r.get("title")
            self.game.toast(T.ACH_TITLE_SET.format(t=r["title"]) if r.get("title") else T.ACH_TITLE_OFF, "#B8862E")
            self.game.refresh_me()
        self.api.post("/books/wear", {"title": title}, ok, self._err)

    # ------------------------------------------------------------ drawing
    def tabs(self) -> list[tuple[str, str, int]]:
        cats = [(c["id"], c["name_vi"], c["claimable"]) for c in (self.v or {}).get("categories", [])]
        return cats + [(TITLES, T.ACH_TAB_TITLES, 0)]

    def draw_ui(self, ui):
        if ui.key(pygame.K_v):
            self.close()
            return
        ui.dim()
        ui.panel(X, Y, W, H, T.ACH_TITLE)
        v = self.v
        if v is None:
            ui.text(T.ACH_LOADING, X + W / 2, Y + H / 2, 9, GREY, anchor="center")
        else:
            self.draw_tabs(ui)
            self.draw_header(ui, v)
            if self.tab == TITLES:
                self.draw_titles(ui, v)
            else:
                self.draw_list(ui, v)
        if ui.button("ach_close", X + W - 58, Y + H - 19, 48, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_tabs(self, ui) -> None:
        tabs = self.tabs()
        ids = [t[0] for t in tabs]
        move = (1 if ui.key(pygame.K_RIGHT) else 0) - (1 if ui.key(pygame.K_LEFT) else 0)
        if move and self.tab in ids:
            self.tab, self.first = ids[(ids.index(self.tab) + move) % len(ids)], 0
        n = len(tabs)
        gap = 2
        tw = (W - 16 - gap * (n - 1)) / n
        for i, (tid, label, claimable) in enumerate(tabs):
            tx = X + 8 + i * (tw + gap)
            if ui.button(f"ach_tab_{tid}", tx, Y + 9, tw, 14, fit(ui, label, 7, tw - 4), size=7,
                         selected=self.tab == tid):
                self.tab, self.first = tid, 0
            if claimable:        # a gold mark: something inside waits to be claimed
                ui.fill(tx + tw - 5, Y + 10, 4, 4, UICOL["gold"])
                ui.border(tx + tw - 5, Y + 10, 4, 4, INK)

    def draw_header(self, ui, v) -> None:
        y = Y + 27
        ui.fill(X + 8, y, W - 16, 22, "#EDE4D2")
        ui.border(X + 8, y, W - 16, 22, "#C9B48A")
        pts = T.ACH_POINTS.format(name=v["points_name_vi"], n=v["points"])
        ui.text(pts, X + 13, y + 3, 8, GOLD_TEXT)
        ui.text(T.ACH_DONE.format(d=v["done"], t=v["total"]), X + 13, y + 13, 6, GREY)
        nxt = v.get("next_milestone")
        ms_ready = next((m for m in v["milestones"] if m["claimable"]), None)
        right = X + W - 12
        if v.get("claimable"):
            if ui.button("ach_claim_all", right - 52, y + 4, 52, 14, T.ACH_CLAIM_ALL, size=7, style="gold",
                         enabled=not self.busy):
                self.claim_all()
            right -= 56
        if ms_ready:
            if ui.button(f"ach_ms_{ms_ready['points']}", right - 52, y + 4, 52, 14, T.ACH_CLAIM_MS, size=7,
                         style="green", enabled=not self.busy):
                self.claim_milestone(ms_ready["points"])
            right -= 56
        mx = X + 92
        room = right - mx - 4
        if nxt:
            prev = max([m["points"] for m in v["milestones"] if m["reached"]] or [0])
            frac = (v["points"] - prev) / max(1, nxt["points"] - prev)
            ui.text(fit(ui, T.ACH_NEXT_MS.format(p=nxt["points"], r=", ".join(nxt["reward_vi"])), 7, room),
                    mx, y + 3, 7, INK)
            ui.progress(mx, y + 13, room, 5, frac, UICOL["gold"], back="#CFC6B4")
        else:
            ui.text(fit(ui, T.ACH_ALL_MS.format(name=v["points_name_vi"]), 7, room), mx, y + 7, 7, GREEN)

    # -------- a category
    def rows(self, v) -> list[dict]:
        """The rows of the tab: what can be claimed first, then what is under way, what has not
        started, and what is complete last (the data order inside each group)."""
        c = next((c for c in v["categories"] if c["id"] == self.tab), None)
        if not c:
            return []
        rank = {"claim": 0, "locked": 1, "done": 4}
        return sorted(c["achievements"], key=lambda e: rank.get(row_state(e), 2 if e["tier"] > 0 else 3))

    def draw_list(self, ui, v) -> None:
        rows = self.rows(v)
        top, bottom = Y + 53, Y + H - 23
        shown = int((bottom - top) // ROW)
        most = max(0, len(rows) - shown)
        if ui.hover(X + 8, top, W - 16, bottom - top) and ui.inp.wheel:
            self.first -= ui.inp.wheel
            ui.inp.wheel = 0
        self.first += (1 if ui.key(pygame.K_DOWN) else 0) - (1 if ui.key(pygame.K_UP) else 0)
        self.first = max(0, min(self.first, most))
        rw = W - 16 - (6 if most else 0)
        for n, e in enumerate(rows[self.first:self.first + shown]):
            self.draw_row(ui, e, X + 8, top + n * ROW, rw)
        if most:
            area = shown * ROW - 2
            ui.fill(X + W - 11, top, 3, area, "#DCD2BC")
            frac = shown / len(rows)
            ui.fill(X + W - 11, top + area * (1 - frac) * self.first / most, 3, max(8.0, area * frac),
                    UICOL["accent"])

    def draw_row(self, ui, e: dict, x: float, y: float, w: float) -> None:
        h = ROW - 2
        state = row_state(e)
        back = {"claim": "#F7E7B4", "done": "#E6EBD9", "locked": "#F1E8D6"}.get(state, "#FFFDF7")
        if not e["revealed"]:
            back = "#E4DDD0"
        ui.fill(x, y, w, h, back)
        ui.border(x, y, w, h, UICOL["gold"] if state == "claim" else "#D3C3A0")
        # the icon on a small dark plate
        ui.fill(x + 3, y + 3, 28, 28, "#3A342C" if e["revealed"] else "#6B6358")
        img = art2.icon(*e["icon"]) if e["revealed"] else None
        if img is not None:
            ui.image(img, x + 17, y + 17, zoom=0.8, anchor="center")
        else:
            ui.text("?", x + 17, y + 17, 12, "#E3D5BA", anchor="center")
        rx = x + w - 112                       # the right column: reward and button
        tx, tw = x + 36, rx - x - 40
        # name and pips
        pips = tier_pips(e)
        pw = len(pips) * 6 if len(pips) > 1 else 0
        name_w = tw - pw - 4
        ui.text(fit(ui, e["name_vi"], 8, name_w), tx, y + 1, 8, INK if e["revealed"] else GREY)
        if pw:
            px = tx + min(ui.text_size(fit(ui, e["name_vi"], 8, name_w), 8)[0] + 5, name_w + 4)
            for i, st in enumerate(pips):
                col = {"claimed": GREEN, "ready": UICOL["gold"]}.get(st)
                if col:
                    ui.fill(px + i * 6, y + 6, 4, 4, col)
                ui.border(px + i * 6, y + 6, 4, 4, INK if col else PALE)
        hov = ui.hover(x, y, w, h)
        desc = e["desc_vi"]
        if e.get("reveal_vi"):
            desc = e["reveal_vi"]
        ui.text(fit(ui, desc, 6, tw), tx, y + 13, 6, GREY)
        if hov and (ui.text_size(desc, 6)[0] > tw or e.get("reveal_vi")):
            ui.set_tooltip(e["desc_vi"] + ("\n" + e["reveal_vi"] if e.get("reveal_vi") else ""))
        # progress
        bw = tw - 112
        ui.progress(tx, y + 24, bw, 5, e["frac"], GREEN if e["done"] else UICOL["blue"], back="#CFC6B4")
        ui.text(fit(ui, e["progress_vi"], 6, 108), tx + bw + 4, y + 22, 6, INK)
        # reward and claim
        t = focus_tier(e)
        if t is not None:
            if e["max"] > 1:
                head = T.ACH_REWARD_TIER.format(n=t["n"], r="")
                ui.text(head.rstrip(": ").rstrip(), rx, y + 2, 6, PALE)
            reward = ", ".join(t["reward_vi"])
            lines = ui.f.wrap(reward, 6, int(108 * ui.s), ui.s)
            if len(lines) > 2:
                lines = [lines[0], fit(ui, " ".join(lines[1:]), 6, 108)]
            ui.text("\n".join(lines), rx, y + 10, 6, GOLD_TEXT if e["revealed"] else PALE, line_gap=1.0)
            if hov and len(ui.f.wrap(reward, 6, int(108 * ui.s), ui.s)) > 2:
                ui.set_tooltip(reward)
        if state == "claim":
            if ui.button(f"ach_claim_{e['id']}", x + w - 46, y + h - 15, 42, 12, T.ACH_CLAIM, size=7, style="gold",
                         enabled=not self.busy):
                self.claim(e["id"], t["n"])
        elif state == "locked":
            ui.text(T.ACH_LOCKED_TIER, x + w - 4, y + h - 9, 6, "#BC4749", anchor="midright")
            if hov:
                ui.set_tooltip(next((x_["req_vi"] for x_ in e["tiers"] if x_["req_vi"] and x_["reached"]), ""))
        elif state == "done":
            ui.text(T.ACH_COMPLETE, x + w - 4, y + h - 9, 7, GREEN, anchor="midright")
        elif e["tier"] > 0:
            ui.text(T.ACH_TIER.format(n=e["tier"], t=e["max"]), x + w - 4, y + h - 9, 6, GREY, anchor="midright")

    # -------- the titles
    def draw_titles(self, ui, v) -> None:
        top = Y + 53
        worn = v.get("title")
        ui.text(T.ACH_WORN.format(t=worn) if worn else T.ACH_WORN_NONE, X + 12, top, 8,
                GOLD_TEXT if worn else GREY)
        ui.text(T.ACH_TITLES_HINT, X + 12, top + 11, 6, GREY)
        if worn and ui.button("ach_unwear", X + W - 92, top - 2, 80, 13, T.ACH_UNWEAR, size=7, enabled=not self.busy):
            self.wear("")
        titles = v.get("titles") or []
        if not titles:
            ui.text(T.ACH_EMPTY_TITLES, X + 12, top + 30, 8, GREY, max_w=W - 24)
            return
        cols, cw, ch = 3, (W - 24 - 8) / 3, 24
        area_top, bottom = top + 24, Y + H - 23
        per = cols * int((bottom - area_top) // ch)
        most = max(0, (len(titles) - per + cols - 1) // cols)
        if ui.hover(X + 8, area_top, W - 16, bottom - area_top) and ui.inp.wheel:
            self.first -= ui.inp.wheel
            ui.inp.wheel = 0
        self.first = max(0, min(self.first, most))
        for n, t in enumerate(titles[self.first * cols:self.first * cols + per]):
            cx = X + 12 + (n % cols) * (cw + 4)
            cy = area_top + (n // cols) * ch
            on = t["title"] == worn
            ui.fill(cx, cy, cw, ch - 3, "#F7E7B4" if on else "#FFFDF7")
            ui.border(cx, cy, cw, ch - 3, UICOL["gold"] if on else "#D3C3A0")
            ui.text(fit(ui, f"«{t['title']}»", 7, cw - 40), cx + 4, cy + 2, 7, INK)
            ui.text(T.ACH_SOURCE.get(t["source"], ""), cx + 4, cy + 12, 6, PALE)
            if on:
                ui.text(T.ACH_WEARING, cx + cw - 4, cy + 10, 6, GREEN, anchor="midright")
            elif ui.button(f"ach_wear_{n + self.first * cols}", cx + cw - 34, cy + 4, 30, 13, T.ACH_WEAR, size=7,
                           enabled=not self.busy):
                self.wear(t["title"])
