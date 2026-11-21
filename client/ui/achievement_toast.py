"""The Thành Tựu unlock banner: one at a time at the top of the screen, with the achievement's
icon, the FX sheet `thanh_tuu` (one-shot, additive) burning behind it, "Thành tựu: <name>", the
tier and the Đạo Tâm it gave.

Where unlocks come from: the websocket message {"t": "achievement", "unlocks": [...]} (any scene,
since the socket is open from login on) and GET /achievements/new right after login (what was
reached while offline). Each unlock has a key "id:tier"; a key is queued once per session and
acknowledged with POST /achievements/seen when its banner starts, so the server never sends it
again. While a question card is open (a quiz scene on top) the queue waits: the banner never
covers a question or the middle of a fight."""
from __future__ import annotations

import math

from .. import strings_vi as T

W, H = 236, 36                 # the banner
CH = 14                        # the one-line banner, where a panel leaves no room for the whole one
TOP = 3
SLIDE = 0.25                   # seconds to slide in and out
SHOW = 3.4                     # seconds on screen in all
FX = "thanh_tuu"
GOLD = "#E9C46A"
PAPER = "#F4EBD9"


def blocked(game) -> bool:
    """A question card is open: hold the banners until it closes."""
    top = game.top
    return top is not None and (getattr(top, "in_combat", False) or type(top).__name__.endswith("QuizScene"))


class AchievementToasts:
    def __init__(self, game):
        self.game = game
        self.queue: list[dict] = []
        self.known: set[str] = set()    # keys queued this session (never twice)
        self.current: dict | None = None
        self.born = 0.0
        self.shown: list[str] = []      # keys whose banner started (tests read it)

    # ------------------------------------------------------------ feeding
    def add(self, unlocks) -> None:
        for u in unlocks or []:
            k = u.get("key")
            if k and k not in self.known:
                self.known.add(k)
                self.queue.append(u)

    def fetch_missed(self) -> None:
        """After login: what was reached while the player was away."""
        self.game.api.get("/achievements/new", lambda r: self.add((r or {}).get("unlocks")), lambda e: None)

    def reset(self) -> None:
        self.queue, self.known, self.current = [], set(), None

    def _start(self, u: dict) -> None:
        g = self.game
        self.current, self.born = u, g.now
        self.shown.append(u["key"])
        g.audio.play("thanh_tuu")
        g.api.post("/achievements/seen", {"keys": [u["key"]]}, lambda r: None, lambda e: None)
        if u.get("title"):
            g.refresh_me()

    def clear_y(self) -> float:
        """Where the ordinary toasts may start while a banner is up (0: anywhere)."""
        return self.y + (CH if self.compact else H) + 4 if self.current is not None else 0

    def rects(self) -> list[tuple[float, float, float, float]]:
        """The banner's rectangle while it is on screen (toasts keep off it)."""
        h = CH if self.compact else H
        return [(240 - W / 2, self.y, W, h)] if self.current is not None and self.shown_now else []

    # ------------------------------------------------------------ drawing
    y = TOP                    # where the banner stands (TOP, unless that covers a card's or panel's text)
    shown_now = False
    compact = False
    _clock = None

    def draw(self, ui) -> None:
        """The banner at the top - or, when that would cover the text of the open panel, in the
        nearest strip that covers none. With no such strip it waits, its time standing still."""
        g = self.game
        last = self._clock if self._clock is not None else g.now
        self._clock = g.now
        self.shown_now = False
        if self.current is not None and g.now - self.born > SHOW:
            self.current = None
        slot, self.compact = None, False
        if self.current is not None or self.queue:
            slot = ui.free_slot(W, H, TOP)
            if slot is None:                 # an open panel leaves no 36-px strip: the one-line banner
                slot = ui.free_slot(W, CH, TOP)
                self.compact = slot is not None
        if self.current is None:
            if not self.queue or blocked(g) or slot is None:
                return
            self.y = slot
            self._start(self.queue.pop(0))
        elif slot is None:
            self.born += max(0.0, g.now - last)          # no room now: the banner waits
            return
        else:
            self.y = slot
        self.shown_now = True
        u, age = self.current, g.now - self.born
        if self.compact:
            self._draw_compact(ui, u)
            return
        k = min(1.0, age / SLIDE, max(0.0, (SHOW - age) / SLIDE))
        k = 1 - (1 - k) ** 2
        x, y = 240 - W / 2, self.y - (H + 6) * (1 - k) if self.y <= TOP else self.y
        ui.fill(x + 2, y + 2, W, H, (0, 0, 0, 110))
        ui.fill(x, y, W, H, (36, 30, 24, 238))
        ui.border(x, y, W, H, GOLD)
        ui.border(x + 2, y + 2, W - 4, H - 4, (140, 105, 50))
        cx, cy = x + 20, y + H / 2
        self._fx(ui, cx, cy, age)
        from ..engine import art2
        img = art2.icon(*(u.get("icon") or [None, None]))
        if img is not None:
            ui.image(img, cx, cy, zoom=0.8, anchor="center")
        from .mathdraw import fit
        head = (T.ACH_HIDDEN_HEAD if u.get("hidden") else T.ACH_TOAST_HEAD).format(name=u["name_vi"])
        ui.text(fit(ui, head, 8, W - 44), x + 38, y + 4, 8, GOLD)
        tier = (T.ACH_TOAST_TIER.format(n=u["tier"], t=u["tiers"], tier=u["tier_name_vi"]) if u["tiers"] > 1
                else T.ACH_TOAST_ONE.format(tier=u["tier_name_vi"]))
        pts = T.ACH_TOAST_POINTS.format(n=u.get("points", 0))
        pw = ui.text_size(pts, 7)[0]
        ui.text(fit(ui, tier, 7, W - 48 - pw), x + 38, y + 15, 7, PAPER)
        ui.text(pts, x + W - 6, y + 15, 7, "#B5D67A", anchor="topright")
        line = T.ACH_TOAST_TITLE.format(t=u["title"]) if u.get("title") else (u.get("reveal_vi") or "")
        if line:
            ui.text(fit(ui, line, 6, W - 44), x + 38, y + 25, 6, "#D8C9A6")
        # a glint running along the top edge
        gx = x + (W + 40) * ((age * 0.8) % 1.0) - 20
        if x < gx < x + W - 12:
            ui.fill(gx, y, 12, 1, (255, 240, 190, 200))

    def _draw_compact(self, ui, u: dict) -> None:
        """The banner in one line (where an open panel leaves no room for the whole one)."""
        from .mathdraw import fit
        x, y = 240 - W / 2, self.y
        ui.fill(x, y, W, CH, (36, 30, 24, 238))
        ui.border(x, y, W, CH, GOLD)
        pts = T.ACH_TOAST_POINTS.format(n=u.get("points", 0))
        pw = ui.text_size(pts, 7)[0]
        head = (T.ACH_HIDDEN_HEAD if u.get("hidden") else T.ACH_TOAST_HEAD).format(name=u["name_vi"])
        ui.text(fit(ui, head, 8, W - 16 - pw), x + 5, y + CH / 2, 8, GOLD, anchor="midleft")
        ui.text(pts, x + W - 5, y + CH / 2, 7, "#B5D67A", anchor="midright")

    def _fx(self, ui, cx: float, cy: float, age: float) -> None:
        """The thanh_tuu burst behind the icon (window pixels, additive); a soft ring without art."""
        from ..engine import art2
        wx, wy = ui.d.to_window(cx, cy)
        if art2.fx(FX) is not None:      # the sheet plays once; afterwards only the icon stays
            art2.draw_fx(ui.win, FX, age, wx, wy, scale=ui.s * 0.5)
            return
        r = 10 + 4 * math.sin(age * 6)
        ui.border(cx - r, cy - r, 2 * r, 2 * r, (233, 196, 106))
