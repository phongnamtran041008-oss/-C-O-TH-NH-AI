"""Cơ duyên (M10): an old cultivator who poses one hard question, a sealed chest that wants a
short chain answered, and the rare reward for getting it right.

The hub's "Cơ Duyên" door opens this scene. It shows the open offer (intro, Nhận / Bỏ qua), or
- with none - how cơ duyên come and today's count; the questions are played with the ordinary
math card (`MathQuizScene`), and the card of the last one is followed by the reward or the loss
text. Nothing is lost by a wrong answer or by walking away: the texts say so.

`notice(game, response)` is the toast for an offer that has just appeared: whoever receives the
answer of a math question calls it with the `/quiz/answer` response."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from .base import Scene
from .math_practice import MathQuizScene

GREY = "#8E877A"
GOLD = "#C99A3A"
RED = "#BC4749"
GREEN = "#6A994E"


def notice(game, response: dict | None) -> bool:
    """Toast an offer carried by a `/quiz/answer` response (`math.fortune_offer`). True when
    there was one."""
    offer = ((response or {}).get("math") or {}).get("fortune_offer")
    if not offer:
        return False
    game.toast(T.FORTUNE_TOAST.format(name=offer.get("name_vi", "")), GOLD, 4.0)
    return True


class FortuneQuizScene(MathQuizScene):
    """The math card, with the cơ duyên it belongs to named along the bottom."""

    can_stop = False     # a cơ duyên is not a sitting: there is nothing for "Nghỉ" to end

    def __init__(self, game, question: dict, on_result=None):
        super().__init__(game, question, run=None, on_result=on_result)
        self.fortune = question.get("fortune") or {}

    def draw_run(self, ui, x, y, w, h):
        self.draw_line(ui, x, y, w, h, w - 40)

    def draw_line(self, ui, x, y, w, h, max_w: float):
        f = self.fortune
        if f:
            n, t = f.get("progress", [0, 1])
            ui.text(T.FORTUNE_CARD.format(name=f.get("name_vi", ""), n=min(t, n + 1), t=t),
                    x + 12, y + h - 12, 7, GOLD, anchor="midleft", max_w=max_w)

    def draw_math_result(self, ui, x, y, w, h):
        super().draw_math_result(ui, x, y, w, h)
        self.draw_line(ui, x, y, w, h, w - 270)


class MathFortuneScene(Scene):
    """The open offer, today's count and the recent log."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.result: dict | None = None      # the block of the event just finished
        self.busy = False
        self.t = 0.0
        self.load()

    # ------------------------------------------------------------ server calls
    def load(self) -> None:
        self.busy = True

        def ok(r):
            self.data, self.busy, self.t = r, False, 0.0
        self.api.get("/math/fortune", ok, self.fail)

    def fail(self, err) -> None:
        self.busy = False
        self.game.api_error(err)

    def accept(self) -> None:
        if self.busy:
            return
        self.busy = True
        self.result = None

        def ok(res):
            self.busy = False
            if res.get("question"):
                self.ask(res["question"])
            else:                                # nothing to ask any more: the server says why
                self.game.toast(res.get("message_vi", ""), GOLD)
                self.load()
        self.api.post("/math/fortune/accept", {}, ok, self.fail)

    def decline(self) -> None:
        if self.busy:
            return
        self.busy = True

        def ok(r):
            self.data, self.busy, self.t = r, False, 0.0
        self.api.post("/math/fortune/decline", {}, ok, self.fail)

    def ask(self, question: dict) -> None:
        self.game.push(FortuneQuizScene(self.game, question, on_result=self.on_answer))

    def on_answer(self, res: dict, stop: bool = False) -> None:
        f = res.get("fortune") or {}
        if f.get("next"):
            self.ask(f["next"])
        else:
            if f.get("done"):
                self.result = f
            self.load()

    # ------------------------------------------------------------ drawing
    def update(self, dt, top):
        self.t += dt

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.FORTUNE_TITLE)
        if self.data is None:
            ui.text(T.FORTUNE_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        elif self.result:
            self.draw_result(ui, x, y, w, h)
        elif self.data["offer"]:
            self.draw_offer(ui, x, y, w, h, self.data["offer"])
        else:
            self.draw_idle(ui, x, y, w, h)
        if self.data is not None and not self.data["offer"] or self.result:
            self.draw_log(ui, x, y + (138 if self.result else 108), w)
        if self.data is not None:
            d = self.data["today"]
            ui.text(T.FORTUNE_TODAY.format(n=d["offers"], limit=d["limit"]), x + 12, y + h - 20, 7, GOLD)
        if ui.button("fortune_close", x + w - 62, y + h - 20, 50, 14, T.FORTUNE_CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_idle(self, ui, x, y, w, h):
        ui.text(T.FORTUNE_NONE, x + 14, y + 28, 9, "#2B2B2B", max_w=w - 28)
        ui.text(self.data["how_vi"], x + 14, y + 46, 8, GREY, max_w=w - 28)
        p = self.data["progress"]
        ui.text(T.FORTUNE_PROGRESS.format(n=p["right"], need=p["need"]), x + 14, y + 86, 8, GREEN)

    def draw_offer(self, ui, x, y, w, h, o: dict):
        kind = T.FORTUNE_ELDER if o["kind"] == "elder" else T.FORTUNE_CHEST
        ui.text(f"{kind}: {o['name_vi']}", x + 14, y + 26, 10, "#2B2B2B", max_w=w - 28)
        cy = y + 44
        cy += ui.text(o["intro_vi"], x + 14, cy, 8, "#2B2B2B", max_w=w - 28).h + 6
        total = o["progress"][1]
        ui.text(T.FORTUNE_ONE_QUESTION if o["kind"] == "elder" else T.FORTUNE_QUESTIONS.format(n=total),
                x + 14, cy, 8, UICOL["accent"])
        left = max(0, o["expires_in"] - int(self.t))
        if not o["accepted"]:
            ui.text(T.FORTUNE_EXPIRES.format(m=left // 60, s=left % 60), x + 14, cy + 14, 7, GREY)
        label = T.FORTUNE_RESUME if o["accepted"] else T.FORTUNE_ACCEPT
        if ui.button("fortune_accept", x + 14, y + h - 46, 96, 20, label, style="primary", enabled=not self.busy):
            self.accept()
        if not o["accepted"] and ui.button("fortune_decline", x + 120, y + h - 46, 80, 20, T.FORTUNE_DECLINE,
                                           enabled=not self.busy):
            self.decline()

    def draw_result(self, ui, x, y, w, h):
        f = self.result
        won = f.get("won")
        ui.text(T.FORTUNE_WON if won else T.FORTUNE_LOST, x + 14, y + 26, 11, GREEN if won else RED)
        cy = y + 46
        cy += ui.text(f.get("text_vi", ""), x + 14, cy, 8, "#2B2B2B", max_w=w - 28).h + 6
        if not won:                       # (the loss text of the event already says nothing is lost)
            return
        r = f.get("rewards") or {}
        if r.get("spirit_stones"):
            cy += ui.text(T.FORTUNE_STONES.format(n=r["spirit_stones"]), x + 14, cy, 9, GOLD).h + 2
        for i in r.get("items", []):
            line = T.FORTUNE_ITEM.format(n=i["qty"], name=i["name_vi"]) + (f" {T.FORTUNE_RARE}" if i["rare"] else "")
            cy += ui.text(line, x + 14, cy, 9, UICOL["accent"] if i["rare"] else "#2B2B2B").h + 2

    def draw_log(self, ui, x, y, w):
        ui.text(T.FORTUNE_LOG, x + 14, y, 8, "#2B2B2B")
        log = self.data["log"]
        if not log:
            ui.text(T.FORTUNE_LOG_EMPTY, x + 14, y + 14, 7, GREY)
            return
        for n, row in enumerate(log[:5]):
            col = GREEN if row["outcome"] == "won" else GREY
            ui.text(f"· {row['name_vi']} - {T.FORTUNE_OUTCOME.get(row['outcome'], row['outcome'])}",
                    x + 14, y + 14 + n * 11, 7, col, max_w=w - 28)
