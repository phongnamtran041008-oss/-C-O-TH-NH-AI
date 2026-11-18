"""Bài kiểm tra đầu vào (M11, learning-path rule 7), opened from the math hub.

One scene over the hub: a short explanation first (what the test is, that it is optional,
that the start floor's gate still applies), then the questions one by one on the ordinary
math card, then the result - where the player starts and why, floor by floor. "Nghỉ" on the
card pauses the sitting (the hub then offers "Làm tiếp kiểm tra"); "Bỏ dở" gives it up.
The server decides everything (server/app/systems/math_placement.py)."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from .base import Scene
from .math_practice import MathQuizScene

GREY = "#5A5A5A"
INK = "#2B2B2B"


class PlacementQuizScene(MathQuizScene):
    """The math card, with the sitting's progress along the bottom."""

    def run_line(self, r: dict, answered: bool) -> str:
        p = r.get("placement") or {}
        if not p:
            return super().run_line(r, answered)
        n = min(p.get("total", 0), p.get("asked", 0) + (0 if answered else 1))
        return (f"{T.MATH_PLACE_PROGRESS.format(n=n, t=p.get('total', 0))}   "
                f"{T.MATH_SCORE.format(c=p.get('correct', 0), a=p.get('asked', 0))}")


class PlacementScene(Scene):
    """Intro -> questions -> result, for one subject. `brief` is the subject's `placement`
    block of /math/path; `on_close` is told when the scene goes (the hub reloads)."""

    def __init__(self, game, subject: dict, on_close=None):
        super().__init__(game)
        self.subject = subject
        self.brief = subject.get("placement") or {}
        self.on_close = on_close
        self.run_id: int | None = self.brief.get("run_id")
        self.state: dict | None = None          # GET /math/placement
        self.result: dict | None = None         # the outcome, once decided
        self.busy = False

    def on_enter(self):
        self.busy = True

        def ok(st):
            self.busy, self.state = False, st
            if st.get("run"):
                self.run_id = st["run"]["run_id"]
        self.api.get(f"/math/placement?subject_id={self.subject['id']}", ok, self.fail)

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def leave(self):
        self.close()
        if self.on_close:
            self.on_close()

    # ------------------------------------------------------------ server calls
    def begin(self):
        self.busy = True

        def ok(res):
            self.run_id = res["run"]["run_id"]
            self.next_question()
        self.api.post("/math/placement/start", {"subject_id": self.subject["id"]}, ok, self.fail)

    def next_question(self):
        self.busy = True

        def ok(res):
            self.busy = False
            if res.get("question") is None:     # decided (e.g. an unanswered question ran out)
                self.result = res.get("result")
                return
            self.game.push(PlacementQuizScene(self.game, res["question"], res["run"], on_result=self.on_result))
        self.api.post("/math/placement/next", {"run_id": self.run_id}, ok, self.fail)

    def on_result(self, res: dict, stop: bool):
        m = res.get("math") or {}
        if m.get("placement_result"):
            self.result = m["placement_result"]
        elif stop:
            self.leave()                        # paused: the hub offers to go on
        else:
            self.next_question()

    def abandon(self):
        self.busy = True

        def ok(st):
            self.busy = False
            self.result = st.get("result")
        self.api.post("/math/placement/abandon", {"run_id": self.run_id}, ok, self.fail)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 50, 18, 380, 234
        ui.panel(x, y, w, h, T.MATH_PLACE_RESULT if self.result else T.MATH_PLACE_TITLE)
        if self.result:
            self.draw_result(ui, x, y, w, h)
        elif self.state is None:
            ui.text(T.MATH_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            self.draw_intro(ui, x, y, w, h)

    def draw_intro(self, ui, x, y, w, h):
        st = self.state
        ui.text(self.subject["name_vi"], x + w / 2, y + 16, 10, UICOL["accent"], anchor="midtop")
        cy = y + 34
        going = st.get("status") == "in_progress"
        if going:
            p = st.get("progress") or {}
            cy += ui.text(T.MATH_PLACE_RESUME_INTRO.format(a=p.get("asked", 0), t=p.get("total", 0)),
                          x + 16, cy, 8, UICOL["green"], max_w=w - 32).h + 6
        intro = T.MATH_PLACE_INTRO
        lines = [intro[0].format(name=self.subject["name_vi"]), intro[1].format(n=st.get("planned", 0)),
                 intro[2].format(pct=st.get("pass_pct", 80)), *intro[3:]]
        for line in lines:
            ui.text("-", x + 16, cy, 8, GREY)
            cy += ui.text(line, x + 26, cy, 8, INK, max_w=w - 42).h + 4
        by = y + h - 24
        if going:
            if ui.button("math_place_go", x + w / 2 - 128, by, 80, 16, T.MATH_PLACE_GO_ON, style="primary",
                         key=pygame.K_RETURN, enabled=not self.busy):
                self.next_question()
            if ui.button("math_place_abandon", x + w / 2 - 40, by, 80, 16, T.MATH_PLACE_ABANDON,
                         enabled=not self.busy):
                self.abandon()
        elif st.get("offered"):
            if ui.button("math_place_go", x + w / 2 - 128, by, 80, 16, T.MATH_PLACE_START, style="primary",
                         key=pygame.K_RETURN, enabled=not self.busy):
                self.begin()
        if ui.button("math_place_later", x + w / 2 + 48, by, 80, 16, T.MATH_PLACE_LATER, key=pygame.K_ESCAPE):
            self.leave()

    def draw_result(self, ui, x, y, w, h):
        r = self.result
        start = r["start_floor"]
        ui.text(T.MATH_PLACE_START_AT.format(n=start), x + w / 2, y + 22, 12, UICOL["green"], anchor="midtop")
        cy = y + 44
        why = []
        if r.get("abandoned"):
            why.append(T.MATH_PLACE_ABANDONED.format(n=start))
        else:
            if r.get("skipped"):
                why.append(T.MATH_PLACE_SKIPPED.format(floors=", ".join(T.MATH_FLOOR.format(n=n)
                                                                        for n in r["skipped"])))
            here = next((f for f in r["floors"] if f["floor"] == start), None)
            if here and here["asked"] and here["correct"] < here["needed"]:
                why.append(T.MATH_PLACE_WHY_STOP.format(n=start, need=here["needed"], planned=here["planned"]))
            else:
                why.append(T.MATH_PLACE_WHY_TOP.format(n=start))
        for line in why:
            cy += ui.text(line, x + w / 2, cy, 8, INK, anchor="midtop", max_w=w - 40).h + 3
        cy += 6
        for f in r["floors"]:
            if not f["asked"]:
                text, colour = T.MATH_PLACE_FLOOR_NOT_ASKED.format(n=f["floor"]), GREY
                mark = ""
            else:
                text = T.MATH_PLACE_FLOOR.format(n=f["floor"], c=f["correct"], a=f["asked"],
                                                 need=f["needed"], planned=f["planned"])
                ok = f["met"]
                colour, mark = (UICOL["green"], T.MATH_PLACE_MET) if ok else (UICOL["accent"], T.MATH_PLACE_NOT_MET)
            ui.text(text, x + 40, cy, 8, colour)
            if mark:
                ui.text(mark, x + w - 40, cy, 8, colour, anchor="topright")
            cy += 14
        ui.text(T.MATH_PLACE_GATE_NOTE.format(n=start), x + w / 2, y + h - 44, 8, GREY, anchor="midtop",
                max_w=w - 40)
        if ui.button("math_place_back", x + w / 2 - 45, y + h - 24, 90, 16, T.MATH_PLACE_BACK, style="primary",
                     key=pygame.K_RETURN):
            self.leave()
