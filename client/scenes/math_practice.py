"""Math question loop (milestone M2): pick a floor of a math bí cảnh, then answer one
question after another. Each question has a countdown; when it runs out the server counts
a wrong answer. After a wrong answer the card shows the solution step by step.

The client never knows the answer: it sends what the player chose or typed and shows what
the server reveals afterwards (the same rule as QuizScene)."""
from __future__ import annotations

import math

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from .base import Scene
from .quiz import KEYS, QuizScene

GREY = "#5A5A5A"
OPTION_KEYS = KEYS + [pygame.K_5, pygame.K_6]


def fit(ui, text: str, size: float, max_w: float) -> str:
    """The text, cut with "..." when it is wider than max_w."""
    if ui.text_size(text, size)[0] <= max_w:
        return text
    while text and ui.text_size(text + "...", size)[0] > max_w:
        text = text[:-1]
    return text.rstrip() + "..."


def tiers_text(lo: int, hi: int) -> str:
    return T.MATH_TIER_ONE.format(lo=lo) if lo == hi else T.MATH_TIERS.format(lo=lo, hi=hi)


class MathQuizScene(QuizScene):
    """One math question: true/false, multiple choice or a typed number."""

    def panel_rect(self):
        return (24, 12, 432, 246)

    def __init__(self, game, question: dict, run: dict | None = None, on_result=None):
        super().__init__(game, question, on_result=None, show_timer=True)
        self.run = run or {}
        self.on_math_result = on_result
        self.given: dict = {}
        self.timed_out = False
        if question.get("input") == "number":
            game.ui.set_focus("quiz_text")

    # ------------------------------------------------------------ actions
    def submit(self, answer: dict):
        if not self.sent:
            self.given = answer
        super().submit(answer)

    def update(self, dt, top):
        self.t += dt
        if self.result:
            self.result_t += dt
        elif not self.sent and self.t > self.limit:
            self.timed_out = True                       # the server counts it as a wrong answer
            self.submit({"timed_out": True})

    def finish(self, stop: bool = False):
        self.close()
        if self.on_math_result and self.result:
            self.on_math_result(self.result, stop)

    def seconds_left(self) -> int:
        return max(0, math.ceil(self.limit - self.t))

    def given_text(self) -> str:
        g = self.given
        if "value" in g:
            return T.MATH_TRUE if g["value"] else T.MATH_FALSE
        if "option" in g:
            return next((o["text"] for o in self.q.get("options") or [] if o["id"] == g["option"]), "")
        return str(g.get("text", ""))

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim(150)
        x, y, w, h = self.panel_rect()
        ui.panel(x, y, w, h)
        m = self.q.get("math", {})
        ui.text(f"{m.get('subject_name_vi', '')} · {T.MATH_FLOOR.format(n=m.get('floor', '?'))} · "
                f"{m.get('skill_name_vi', '')}", x + 12, y + 8, 7, GREY, max_w=w - 130)
        ui.text(T.MATH_TIER_LABEL.format(n=m.get("tier", "?"), name=m.get("tier_name_vi", "")),
                x + w - 12, y + 8, 7, UICOL["accent"], anchor="topright")
        if self.result:
            self.draw_math_result(ui, x, y, w, h)
            return
        frac = max(0.0, 1 - self.t / self.limit)
        ui.progress(x + 12, y + 22, w - 74, 4, frac, "#BC4749" if frac < 0.3 else "#6A994E")
        ui.text(T.MATH_SECONDS.format(n=self.seconds_left()), x + w - 12, y + 24, 8,
                "#BC4749" if frac < 0.3 else GREY, anchor="midright")
        ui.text(self.q.get("instruction_vi", ""), x + w / 2, y + 36, 7, GREY, anchor="midtop", max_w=w - 30)
        prompt = self.q.get("prompt", {}).get("text", "")
        ui.text(prompt, x + w / 2, y + 52, 10 if len(prompt) <= 110 else 9, anchor="midtop", max_w=w - 36)
        inp = self.q.get("input")
        if inp == "truefalse":
            self.draw_true_false(ui, x, y + 126, w)
        elif inp == "choice":
            self.draw_options(ui, x, y + 104, w)
        elif inp == "number":
            self.draw_number(ui, x, y + 124, w)
        self.draw_run(ui, x, y, w, h)

    def draw_run(self, ui, x, y, w, h):
        r = self.run
        if r:
            ui.text(f"{T.MATH_COMBO.format(n=r.get('combo', 0))}   "
                    f"{T.MATH_SCORE.format(c=r.get('correct', 0), a=r.get('asked', 0))}",
                    x + 12, y + h - 12, 7, GREY, anchor="midleft")

    def draw_true_false(self, ui, x, y, w):
        for i, (wid, label, value) in enumerate((("math_true", T.MATH_TRUE, True),
                                                 ("math_false", T.MATH_FALSE, False))):
            bx = x + w / 2 - 126 + i * 132
            if ui.button(wid, bx, y, 120, 28, label, size=10, key=KEYS[i] if not self.sent else None,
                         enabled=not self.sent, style="green" if value else "primary"):
                self.submit({"value": value})
            ui.text(str(i + 1), bx + 5, y + 4, 7, "#FFFFFF")

    def draw_options(self, ui, x, y, w):
        opts = self.q.get("options") or []
        bh = 22 if len(opts) <= 4 else 17
        for i, o in enumerate(opts):
            by = y + i * (bh + 5)
            clicked = ui.button(f"opt_{o['id']}", x + 16, by, w - 32, bh, "", enabled=not self.sent,
                                key=OPTION_KEYS[i] if not self.sent else None)
            ui.text(str(i + 1), x + 22, by + bh / 2, 7, "#8E877A", anchor="midleft")
            ui.text(o["text"], x + 36, by + bh / 2, 8, "#2B2B2B", anchor="midleft", max_w=w - 76, line_gap=1.0)
            if clicked and not self.sent:
                self.submit({"option": o["id"]})

    def draw_number(self, ui, x, y, w):
        ui.text(T.MATH_NUMBER_HINT, x + w / 2, y - 14, 7, "#8E877A", anchor="center", max_w=w - 30)
        val = ui.input_box("quiz_text", x + w / 2 - 130, y, 180, 20, placeholder=T.MATH_NUMBER_PLACEHOLDER,
                           max_len=60)
        go = ui.button("quiz_submit", x + w / 2 + 58, y, 72, 20, T.QUIZ_SUBMIT, style="primary",
                       enabled=bool(val.strip()) and not self.sent)
        if (go or ui.submitted("quiz_text")) and val.strip() and not self.sent:
            self.submit({"text": val.strip()})

    def draw_math_result(self, ui, x, y, w, h):
        res = self.result
        good = res.get("correct")
        col = UICOL["green"] if good else UICOL["accent"]
        timed_out = res.get("timed_out") or self.timed_out
        title = T.QUIZ_CORRECT if good else (T.QUIZ_TIMEOUT if timed_out else T.QUIZ_WRONG)
        ui.fill(x + 10, y + 20, w - 20, 22, "#E8F2DC" if good else "#F6E0DE")
        ui.border(x + 10, y + 20, w - 20, 22, col, 2)
        ui.text(title, x + 18, y + 31, 12, col, anchor="midleft")
        m = res.get("math") or {}
        notes = []
        if (res.get("xp") or {}).get("gained"):
            notes.append(T.MATH_XP.format(n=res["xp"]["gained"]))
        run = m.get("run") or {}
        if m.get("tier_change", 0) > 0:
            notes.append(T.MATH_TIER_UP.format(name=run.get("tier_name_vi", "")))
        elif m.get("tier_change", 0) < 0:
            notes.append(T.MATH_TIER_DOWN.format(name=run.get("tier_name_vi", "")))
        ui.text("   ".join(notes), x + w - 18, y + 31, 9, "#C99A3A", anchor="midright")

        cy = y + 48
        cy += ui.text(self.q.get("prompt", {}).get("text", ""), x + 16, cy, 8, GREY, max_w=w - 32).h + 3
        rv = res.get("reveal") or {}
        if not good and not timed_out and self.given_text():
            cy += ui.text(T.MATH_YOUR_ANSWER.format(a=self.given_text()), x + 16, cy, 8, UICOL["accent"],
                          max_w=w - 32).h + 2
        cy += ui.text(T.QUIZ_ANSWER_WAS.format(a=rv.get("answer_text", "")), x + 16, cy, 9, UICOL["green"],
                      max_w=w - 32).h + 4
        if not good and rv.get("solution_vi"):      # rule 6: after a wrong answer, the steps
            cy += ui.text(T.MATH_SOLUTION, x + 16, cy, 8, "#2B2B2B").h + 2
            for n, step in enumerate(rv["solution_vi"], 1):
                if cy > y + h - 40:
                    break
                ui.text(f"{n}.", x + 18, cy, 8, GREY)
                cy += ui.text(step, x + 32, cy, 8, "#2B2B2B", max_w=w - 52).h + 2
        if run:
            ui.text(f"{T.MATH_COMBO.format(n=run.get('combo', 0))}   "
                    f"{T.MATH_SCORE.format(c=run.get('correct', 0), a=run.get('asked', 0))}",
                    x + 12, y + h - 12, 7, GREY, anchor="midleft")
        if ui.button("math_stop", x + w - 176, y + h - 22, 60, 16, T.MATH_STOP, key=pygame.K_ESCAPE):
            self.finish(stop=True)
            return
        if ui.button("math_next", x + w - 108, y + h - 22, 96, 16, T.MATH_NEXT, style="primary") or \
                ui.key(pygame.K_RETURN) or ui.key(pygame.K_SPACE):
            self.finish(stop=False)


class MathPracticeScene(Scene):
    """The floors of the math bí cảnh, and the sitting that runs on the chosen floor."""

    def __init__(self, game):
        super().__init__(game)
        self.path: dict | None = None
        self.run: dict | None = None
        self.summary: dict | None = None
        self.busy = False

    def on_enter(self):
        self.load()

    # ------------------------------------------------------------ server calls
    def load(self):
        self.busy = True

        def ok(data):
            self.busy = False
            self.path = data
        self.api.get("/math/path", ok, self.fail)

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def start(self, subject_id: str, floor: int):
        if self.busy:
            return
        self.busy = True

        def ok(res):
            self.run = res["run"]
            self.next_question()
        self.api.post("/math/run/start", {"subject_id": subject_id, "floor": floor}, ok, self.fail)

    def resume(self, run: dict):
        if self.busy:
            return
        self.busy = True
        self.run = run
        self.next_question()

    def next_question(self):
        self.busy = True
        self.summary = None

        def ok(res):
            self.busy = False
            self.run = res["run"]
            self.game.push(MathQuizScene(self.game, res["question"], res["run"], on_result=self.on_result))
        self.api.post("/math/run/next", {"run_id": self.run["run_id"]}, ok, self.fail)

    def on_result(self, res: dict, stop: bool):
        self.run = (res.get("math") or {}).get("run") or self.run
        if stop:
            self.end()
        else:
            self.next_question()

    def end(self):
        self.busy = True

        def ok(res):
            self.busy = False
            self.summary = res["run"]
            self.run = None
            self.load()
        self.api.post("/math/run/end", {"run_id": self.run["run_id"]}, ok, self.fail)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.MATH_TITLE)
        if self.summary:
            self.draw_summary(ui, x, y, w, h)
        elif self.path is None:
            ui.text(T.MATH_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            self.draw_floors(ui, x, y, w, h)
        if ui.button("math_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_floors(self, ui, x, y, w, h):
        open_run = self.path.get("run")
        cy = y + 22
        for s in self.path["subjects"]:
            ui.text(s["name_vi"], x + 12, cy, 10, UICOL["accent"])
            cy += 15
            for f in s["floors"]:
                mine = bool(open_run) and open_run["subject_id"] == s["id"] and open_run["floor"] == f["floor"]
                label = T.MATH_HIDDEN_FLOOR if f["hidden"] else T.MATH_FLOOR.format(n=f["floor"])
                ink = "#2B2B2B" if f["playable"] else "#9A9387"
                ui.text(label, x + 12, cy + 7, 8, ink, anchor="midleft")
                ui.text(fit(ui, f["title_vi"], 8, 206), x + 58, cy + 7, 8, ink, anchor="midleft")
                ui.text(tiers_text(f["tier_min"], f["tier_max"]), x + 270, cy + 7, 7, GREY, anchor="midleft")
                if f["playable"]:
                    ui.text(T.MATH_QUESTIONS.format(n=f["questions"]), x + w - 74, cy + 7, 7, GREY,
                            anchor="midright")
                    if ui.button(f"math_floor_{s['id']}_{f['floor']}", x + w - 68, cy, 56, 13,
                                 T.MATH_RESUME if mine else T.MATH_PLAY, size=7, style="primary",
                                 enabled=not self.busy):
                        if mine:
                            self.resume(open_run)
                        else:
                            self.start(s["id"], f["floor"])
                else:
                    ui.text(T.MATH_NO_QUESTIONS, x + w - 12, cy + 7, 7, "#9A9387", anchor="midright")
                cy += 17

    def draw_summary(self, ui, x, y, w, h):
        r = self.summary
        ui.text(T.MATH_SUMMARY, x + w / 2, y + 44, 12, UICOL["accent"], anchor="center")
        lines = [T.MATH_SUMMARY_SCORE.format(c=r["correct"], a=r["asked"]),
                 T.MATH_SUMMARY_COMBO.format(n=r["best_combo"]),
                 T.MATH_SUMMARY_XP.format(n=r["xp_gained"]),
                 T.MATH_SUMMARY_TIER.format(name=r["tier_name_vi"])]
        for i, line in enumerate(lines):
            ui.text(line, x + w / 2, y + 76 + i * 18, 9, "#2B2B2B", anchor="center")
        if ui.button("math_back", x + w / 2 - 45, y + 160, 90, 16, T.MATH_BACK, style="primary",
                     key=pygame.K_RETURN):
            self.summary = None
