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

    # ------------------------------------------------------------ drawing
    def draw(self, ui) -> None:
        g = self.game
        if self.current is not None and g.now - self.born > SHOW:
            self.current = None
        if self.current is None:
            if not self.queue or blocked(g):
                return
            self._start(self.queue.pop(0))
        u, age = self.current, g.now - self.born
        k = min(1.0, age / SLIDE, max(0.0, (SHOW - age) / SLIDE))
        k = 1 - (1 - k) ** 2
        x, y = 240 - W / 2, TOP - (H + 6) * (1 - k)
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

    def _fx(self, ui, cx: float, cy: float, age: float) -> None:
        """The thanh_tuu burst behind the icon (window pixels, additive); a soft ring without art."""
        from ..engine import art2
        wx, wy = ui.d.to_window(cx, cy)
        if art2.fx(FX) is not None:      # the sheet plays once; afterwards only the icon stays
            art2.draw_fx(ui.win, FX, age, wx, wy, scale=ui.s * 0.5)
            return
        r = 10 + 4 * math.sin(age * 6)
        ui.border(cx - r, cy - r, 2 * r, 2 * r, (233, 196, 106))
