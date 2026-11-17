"""Math question loop (milestone M2): pick a floor of a math bí cảnh, then answer one
question after another. Each question has a countdown; when it runs out the server counts
a wrong answer. After a wrong answer the card shows the solution step by step.

M5: the floor list says which floors are open, which are cleared and how far the mastery
gate of the floor being played has come; a floor whose gate is open offers its Thiên kiếp
nhỏ, a sitting of one question per micro-skill that ends in a verdict. Questions that come
from a floor below say so ("Ôn xoắn ốc").

The client never knows the answer: it sends what the player chose or typed and shows what
the server reveals afterwards (the same rule as QuizScene)."""
from __future__ import annotations

import math

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui.mathdraw import draw_matrices, fit
from .base import Scene
from .math_code import ProblemListScene
from .math_library import DocScene, LibraryListScene
from .quiz import KEYS, CombatCard, QuizScene

GREY = "#5A5A5A"
OPTION_KEYS = KEYS + [pygame.K_5, pygame.K_6]


def tiers_text(lo: int, hi: int) -> str:
    return T.MATH_TIER_ONE.format(lo=lo) if lo == hi else T.MATH_TIERS.format(lo=lo, hi=hi)


class MathQuizScene(QuizScene):
    """One math question: true/false, multiple choice or a typed number."""

    in_combat = False        # M7: the card a quái lỗi sai opens closes itself

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
        top = y + 36
        badge = (T.MATH_PARALLEL if m.get("parallel") else       # rule 6a: the idea just missed
                 T.MATH_REVIEW.format(n=m.get("floor", "?")) if m.get("review") else "")
        if badge:                                   # rule 6b: a question from a floor below
            ui.text(badge, x + w / 2, y + 32, 7, UICOL["accent"], anchor="midtop")
            top = y + 42
        ui.text(self.q.get("instruction_vi", ""), x + w / 2, top, 7, GREY, anchor="midtop", max_w=w - 30)
        prompt = self.q.get("prompt", {})
        text = prompt.get("text", "")
        cy = top + 16
        cy += ui.text(text, x + w / 2, cy, 10 if len(text) <= 110 else 9, anchor="midtop", max_w=w - 36).h
        if prompt.get("matrices"):
            cy = draw_matrices(ui, prompt["matrices"], x + w / 2, cy + 6)
        inp = self.q.get("input")
        if inp == "truefalse":
            self.draw_true_false(ui, x, max(y + 126, cy + 12), w)
        elif inp == "choice":
            self.draw_options(ui, x, max(y + 104, cy + 8), w)
        elif inp == "number":
            self.draw_number(ui, x, max(y + 124, cy + 26), w)
        self.draw_run(ui, x, y, w, h)


    def run_line(self, r: dict, answered: bool) -> str:
        """The line along the bottom of the card: how the sitting is going, or - in a Thiên
        kiếp nhỏ - which question of the trial this is and how many misses are left."""
        if r.get("mode") == "trial":
            t = r.get("trial") or {}
            total = t.get("total", 0)
            n = min(total, r.get("asked", 0) + (0 if answered else 1))
            left = max(0, t.get("max_wrong", 0) - t.get("wrong", 0))
            return f"{T.MATH_TRIAL_PROGRESS.format(n=n, t=total)}   {T.MATH_TRIAL_ALLOWED.format(n=left)}"
        return (f"{T.MATH_COMBO.format(n=r.get('combo', 0))}   "
                f"{T.MATH_SCORE.format(c=r.get('correct', 0), a=r.get('asked', 0))}")

    def draw_run(self, ui, x, y, w, h):
        if self.run:
            ui.text(self.run_line(self.run, answered=False), x + 12, y + h - 12, 7, GREY, anchor="midleft")

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
        if m.get("parallel_waiting"):
            notes.append(T.MATH_WILL_RETURN)
        elif good and m.get("parallel"):
            notes.append(T.MATH_PARALLEL_CLEARED)
        verdict = (m.get("trial") or {}).get("passed")
        if verdict is not None:
            notes.append(T.MATH_TRIAL_PASSED if verdict else T.MATH_TRIAL_FAILED)
        ui.text("   ".join(notes), x + w - 18, y + 31, 9, "#C99A3A", anchor="midright")

        cy = y + 48
        prompt = self.q.get("prompt", {})
        cy += ui.text(prompt.get("text", ""), x + 16, cy, 8, GREY, max_w=w - 32).h + 3
        if prompt.get("matrices"):
            cy = draw_matrices(ui, prompt["matrices"], x + 20, cy + 1, centered=False) + 4
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
            ui.text(self.run_line(run, answered=True), x + 12, y + h - 12, 7, GREY, anchor="midleft")
        doc = (self.q.get("math") or {}).get("doc")
        if doc and ui.button("math_doc", x + w - 252, y + h - 22, 70, 16, T.LIB_OPEN, size=7, style="gold",
                             key=pygame.K_t):
            self.game.push(DocScene(self.game, doc["id"], doc.get("block", 0)))
        if self.in_combat:          # the fight is waiting: no "stop" and no "next"
            return
        over = verdict is not None                  # the trial is decided: no more questions
        if not over and ui.button("math_stop", x + w - 176, y + h - 22, 60, 16, T.MATH_STOP,
                                  key=pygame.K_ESCAPE):
            self.finish(stop=True)
            return
        if ui.button("math_next", x + w - 108, y + h - 22, 96, 16, T.MATH_RESULT if over else T.MATH_NEXT,
                     style="primary") or ui.key(pygame.K_RETURN) or ui.key(pygame.K_SPACE):
            self.finish(stop=over)


class MathCombatQuizScene(CombatCard, MathQuizScene):
    """The card a quái lỗi sai opens (M7): the math card of Động Phủ, but low on the screen
    with the fight still visible, and it closes itself after the explanation the way the word
    card does (spec 8.1). The monster's own mistake is named above the question, so the player
    can see what they are arguing with."""
    modal = False
    draws_world = False
    toast_y = 70
    in_combat = True

    def panel_rect(self):
        return (24, 56, 432, 202)

    def __init__(self, game, question: dict, monster_id: str, on_result=None):
        super().__init__(game, question, run=None, on_result=None)
        self.monster_id = monster_id
        self.on_combat_result = on_result
        self.close_after = 2.0

    def update(self, dt, top):
        super().update(dt, top)
        if self.result and self.result_t >= self.close_after:
            self.finish()

    def finish(self, stop: bool = False):
        self.close()
        if self.on_combat_result and self.result:
            self.on_combat_result(self.result)

    def draw_ui(self, ui):
        super().draw_ui(ui)
        if self.result:
            return
        x, y, w, h = self.panel_rect()
        m = self.q.get("math", {})
        if m.get("mistake_vi"):
            ui.text(f"{m.get('monster_vi', '')}: {m['mistake_vi']}", x + w / 2, y + h - 12, 7,
                    UICOL["accent"], anchor="midbottom", max_w=w - 30)
        ui.text(T.HOI_THE, x + w - 12, y + 20, 7, UICOL["green"], anchor="topright")

    def draw_math_result(self, ui, x, y, w, h):
        super().draw_math_result(ui, x, y, w, h)
        c = (self.result or {}).get("combat") or {}
        if c.get("shield_broken"):
            txt = f"{T.SHIELD_BROKEN} {T.NGO_DAO} -{c.get('damage', 0)}" + (" (chí mạng!)" if c.get("crit") else "")
            ui.text(txt, x + w - 12, y + h - 12, 8, UICOL["green"], anchor="bottomright")
            self.close_after = 1.2          # a right answer gets back to the fight a little faster
        elif c.get("mac_kich"):
            ui.text(f"{T.MAC_KICH} -{c['mac_kich']}", x + w - 12, y + h - 12, 8, UICOL["accent"],
                    anchor="bottomright")


class MathPracticeScene(Scene):
    """The floors of the math bí cảnh, and the sitting that runs on the chosen floor."""

    def __init__(self, game):
        super().__init__(game)
        self.path: dict | None = None
        self.run: dict | None = None
        self.summary: dict | None = None
        self.trial: dict | None = None      # the verdict of the Thiên kiếp nhỏ just finished
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

    def start(self, subject_id: str, floor: int, trial: bool = False):
        """Open a sitting on this floor: ordinary practice, or its Thiên kiếp nhỏ (M5)."""
        if self.busy:
            return
        self.busy = True
        self.trial = None

        def ok(res):
            self.run = res["run"]
            self.next_question()
        self.api.post("/math/trial/start" if trial else "/math/run/start",
                      {"subject_id": subject_id, "floor": floor}, ok, self.fail)

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
        m = res.get("math") or {}
        self.run = m.get("run") or self.run
        trial = m.get("trial") or {}
        if trial.get("passed") is not None:         # the Thiên kiếp nhỏ is decided
            self.trial = trial
            self.end()
        elif stop:
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
        if ui.button("math_library", x + 12, y + h - 20, 76, 14, T.LIB_TITLE, size=7, style="gold",
                     enabled=self.path is not None):
            self.game.push(LibraryListScene(self.game))
        if ui.button("math_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_floors(self, ui, x, y, w, h):
        open_run = self.path.get("run")
        cy = y + 22
        for s in self.path["subjects"]:
            ui.text(s["name_vi"], x + 12, cy, 10, UICOL["accent"])
            if s.get("problems") and ui.button(f"math_code_{s['id']}", x + w - 78, cy - 1, 66, 13,
                                               T.CODE_SHORT, size=7, enabled=not self.busy):
                self.game.push(ProblemListScene(self.game, s["id"]))      # bài tập lập trình (M6)
            cy += 15
            for f in s["floors"]:
                mine = bool(open_run) and open_run["subject_id"] == s["id"] and open_run["floor"] == f["floor"]
                label = T.MATH_HIDDEN_FLOOR if f["hidden"] else T.MATH_FLOOR.format(n=f["floor"])
                ink = "#2B2B2B" if f["playable"] else "#9A9387"
                ui.text(label, x + 12, cy + 7, 8, ink, anchor="midleft")
                ui.text(fit(ui, f["title_vi"], 8, 104), x + 52, cy + 7, 8, ink, anchor="midleft")
                ui.text(tiers_text(f["tier_min"], f["tier_max"]), x + 160, cy + 7, 7, GREY, anchor="midleft")
                self.draw_floor_gate(ui, x, cy, w, s, f)
                if f["playable"]:
                    if ui.button(f"math_floor_{s['id']}_{f['floor']}", x + w - 76, cy, 64, 13,
                                 T.MATH_RESUME if mine else T.MATH_PLAY, size=7, style="primary",
                                 enabled=not self.busy):
                        if mine:
                            self.resume(open_run)
                        else:
                            self.start(s["id"], f["floor"])
                else:
                    ui.text(T.MATH_LOCKED if f["has_questions"] else T.MATH_NO_QUESTIONS,
                            x + w - 12, cy + 7, 7, "#9A9387", anchor="midright")
                if f.get("doc_id") and ui.button(f"math_doc_{s['id']}_{f['floor']}", x + w - 118, cy, 34, 13,
                                                 T.LIB_READ, size=7, style="gold"):
                    self.game.push(DocScene(self.game, f["doc_id"]))
                cy += 17

    def draw_floor_gate(self, ui, x, cy, w, subject: dict, f: dict):
        """The slot between the tiers and the Tàng Thư button (M5): how far the mastery gate
        has come, or the button for the Thiên kiếp nhỏ once the gate is open."""
        gate = f.get("gate")
        if f["state"] == "cleared":
            ui.text(T.MATH_CLEARED, x + w - 122, cy + 7, 7, "#C99A3A", anchor="midright")
        elif not f["playable"] or not gate:
            return                                  # a locked floor says so on the right
        elif gate["ok"]:
            if ui.button(f"math_trial_{subject['id']}_{f['floor']}", x + w - 180, cy, 58, 13,
                         T.MATH_TRIAL, size=7, style="gold", enabled=not self.busy):
                self.start(subject["id"], f["floor"], trial=True)
        else:
            done = sum(1 for k in gate["skills"] if k["ok"])
            ui.text(T.MATH_GATE.format(n=done, t=len(gate["skills"])), x + w - 122, cy + 7, 7, GREY,
                    anchor="midright")

    def gate_hint(self, run: dict) -> str:
        """What the floor just practised still wants before its Thiên kiếp nhỏ opens (M5),
        read from the floor list that was reloaded when the sitting ended."""
        for s in (self.path or {}).get("subjects", []):
            if s["id"] != run["subject_id"]:
                continue
            for f in s["floors"]:
                gate = f.get("gate")
                if f["floor"] == run["floor"] and gate and not gate["ok"] and gate["skills"]:
                    k = gate["skills"][0]
                    return T.MATH_GATE_HINT.format(need=k["needed"], window=k["window"], tier=k["top_tier"])
        return ""

    def draw_summary(self, ui, x, y, w, h):
        r = self.summary
        if self.trial is not None:                  # the verdict of a Thiên kiếp nhỏ
            t = self.trial
            title = T.MATH_TRIAL_PASSED if t["passed"] else T.MATH_TRIAL_FAILED
            colour = UICOL["green"] if t["passed"] else UICOL["accent"]
            lines = [T.MATH_SUMMARY_SCORE.format(c=t["correct"], a=t["asked"]),
                     T.MATH_SUMMARY_XP.format(n=r["xp_gained"]),
                     T.MATH_TRIAL_UNLOCKED.format(n=t["unlocked"]) if t.get("unlocked") else T.MATH_TRIAL_AGAIN]
        else:
            title, colour = T.MATH_SUMMARY, UICOL["accent"]
            lines = [T.MATH_SUMMARY_SCORE.format(c=r["correct"], a=r["asked"]),
                     T.MATH_SUMMARY_COMBO.format(n=r["best_combo"]),
                     T.MATH_SUMMARY_XP.format(n=r["xp_gained"]),
                     T.MATH_SUMMARY_TIER.format(name=r["tier_name_vi"])]
            if r.get("review_asked"):
                lines.append(T.MATH_REVIEW_COUNT.format(n=r["review_asked"]))
            hint = self.gate_hint(r)
            if hint:
                lines.append(hint)
        ui.text(title, x + w / 2, y + 44, 12, colour, anchor="center")
        for i, line in enumerate(lines):
            ui.text(line, x + w / 2, y + 70 + i * 18, 9, "#2B2B2B", anchor="center", max_w=w - 40)
        if ui.button("math_back", x + w / 2 - 45, y + 176, 90, 16, T.MATH_BACK, style="primary",
                     key=pygame.K_RETURN):
            self.summary = self.trial = None
