"""Bài tập lập trình (milestone M6): read the statement, write a solution, Chạy thử on the
samples, Nộp bài on the hidden tests.

The solution runs here, on the player's own machine (client/engine/coderun.py), in a thread
so the game keeps drawing while it runs. What goes back to the server is only what the
program printed; the server keeps the expected answers and decides AC / WA / TLE / RE / CE.

The code also lives in a real file under the game's data folder, so anyone who would rather
write Python in their own editor can do that and press Chạy thử here.

Xạ Trường (docs/THUC_CHIEN_TRONG_GAME.md): a scored exercise trains a model. Its result is
a score and a grade (hạ / trung / thượng phẩm) instead of a verdict per test, and the
statement panel can switch to the target view: the grade, each set's score against the
bars, and the training log the program printed to stderr ("#loss <step> <value>"), drawn
as a curve. The log stays on this machine.
"""
from __future__ import annotations

import math
import threading
from pathlib import Path

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..engine import coderun
from ..ui.codebox import CodeBox
from .base import MessageBox, Scene
from .math_library import scroll_rows

GREY = "#5A5A5A"
VERDICT_COLOUR = {"AC": UICOL["green"], "WA": UICOL["accent"], "TLE": "#C99A3A",
                  "RE": UICOL["accent"], "CE": UICOL["accent"], "-": "#9A9387"}
STARTER = """# {title}
# Doc du lieu tu stdin, in ket qua ra stdout.
import sys

data = sys.stdin.read().split()
"""


def solution_dir(game) -> "Path":
    """Where the solutions live: a bai_lam folder beside the player's own session.json, so
    they can be opened in any editor - and so a test run keeps to its own folder."""
    return game.session.path.parent / "bai_lam"


def solution_file(game, problem_id: str) -> "Path":
    return solution_dir(game) / f"{problem_id}.py"


def verdict_text(v: str) -> str:
    name = T.CODE_VERDICTS.get(v, v)
    return name if v == "-" else f"{v} - {name}"


GRADE_COLOUR = ("#9A9387", "#8C6A3A", "#3F7FB5", UICOL["green"])     # chưa đạt, hạ, trung, thượng


def score_text(value, metric: str) -> str:
    """92,5% for accuracy, 0,512 for an error, Vietnamese decimal comma."""
    if value is None:
        return T.XT_NO_SCORE
    if metric == "do_chinh_xac":
        return f"{value * 100:.1f}%".replace(".", ",")
    return f"{value:.3f}".replace(".", ",")


def bar_text(value, metric: str) -> str:
    """A bar, as short as it can be: 82% or 1,2."""
    if metric == "do_chinh_xac":
        return f"{value * 100:g}%".replace(".", ",")
    return f"{value:g}".replace(".", ",")


def metric_text(value, metric: str) -> str:
    return (T.XT_ACCURACY if metric == "do_chinh_xac" else T.XT_ERROR).format(v=score_text(value, metric))


def set_note(test: dict) -> str:
    """Why one set could not be scored, from the server's note."""
    note = test.get("note") or ""
    if note.startswith("count:"):
        _, want, got = note.split(":")
        return T.XT_BAD_COUNT.format(want=want, got=got)
    if note == "not_number":
        return T.XT_NOT_NUMBER
    return ""


def grade_of(score, bars: list, higher: bool) -> int:
    if score is None:
        return 0
    return sum(1 for b in bars if (score >= b if higher else score <= b))


class ProblemListScene(Scene):
    """The exercises of a subject, floor by floor. Locked floors are not in the answer."""

    def __init__(self, game, subject_id: str, floor: int | None = None, only: list[str] | None = None):
        super().__init__(game)
        self.subject_id, self.floor = subject_id, floor
        self.only = only            # the exercises of one node (its card's "Làm bài"): None lists them all
        self.data: dict | None = None
        self.busy = False
        self.first = 0              # M11: the first row shown, when the list scrolls

    def on_enter(self):
        self.load()

    def on_resume(self):
        self.load()

    def load(self):
        self.busy = True
        query = f"/math/problems?subject_id={self.subject_id}"
        if self.floor:
            query += f"&floor={self.floor}"
        if self.only:                   # a node's exercises may come from several subjects
            query += "&ids=" + ",".join(self.only)

        def ok(data):
            self.busy, self.data = False, data
        self.api.get(query, ok, self.fail)

    def shown_floors(self) -> list[dict]:
        """The floors with the exercises to show: every one, or only the ones in `only`."""
        floors = (self.data or {}).get("floors") or []
        if self.only is None:
            return floors
        order = {pid: i for i, pid in enumerate(self.only)}      # the node's own order: they build up
        cut = [{**f, "problems": sorted((p for p in f["problems"] if p["id"] in order), key=lambda p: order[p["id"]])}
               for f in floors]
        return sorted((f for f in cut if f["problems"]), key=lambda f: order[f["problems"][0]["id"]])

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 60, 24, 360, 222
        ui.panel(x, y, w, h, T.CODE_TITLE)
        floors = self.shown_floors()
        if self.data is None:
            ui.text(T.CODE_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        elif not floors:
            ui.text(T.CODE_NONE, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            ui.text(T.CODE_RUN_HINT, x + 12, y + 21, 7, GREY, max_w=w - 24)
            # M11: one row per floor title and per exercise; more than fit scroll (wheel, Up / Down)
            rows = [(f, p) for f in floors for p in [None] + list(f["problems"])]
            top, bottom = y + 34, y + h - 24
            shown = int((bottom - top) // 16)
            self.first = scroll_rows(ui, self.first, len(rows), shown, x, top, w, bottom - top)
            cy = top
            for f, p in rows[self.first:self.first + shown]:
                if p is None:
                    ui.text(f"{T.MATH_FLOOR.format(n=f['floor'])} · {f['title_vi']}", x + 12, cy + 2, 8,
                            UICOL["accent"], max_w=w - 24)
                    cy += 16
                    continue
                best = p.get("best") or {}
                ui.text(p["title_vi"], x + 18, cy + 7, 8, "#2B2B2B", anchor="midleft", max_w=148)
                ui.text(T.MATH_TIER_ONE.format(lo=p["tier"]), x + 176, cy + 7, 7, GREY, anchor="midleft")
                if best and "grade" in best:        # a scored exercise: its best grade instead of the count
                    ui.text(best["grade_vi"], x + 212, cy + 7, 7, GRADE_COLOUR[best["grade"]], anchor="midleft")
                else:
                    ui.text((T.XT_HIDDEN_SETS if p.get("scored") else T.CODE_HIDDEN_TESTS).format(n=p["tests"]),
                            x + 212, cy + 7, 7, GREY, anchor="midleft")
                if best and "grade" in best:
                    pass
                elif best:
                    ui.text(best["verdict"], x + w - 84, cy + 7, 7,
                            VERDICT_COLOUR.get(best["verdict"], GREY), anchor="midright")
                if ui.button(f"code_open_{p['id']}", x + w - 78, cy, 66, 13, T.CODE_OPEN, size=7,
                             style="primary", enabled=not self.busy):
                    self.game.push(ProblemScene(self.game, p["id"]))
                cy += 16
            if len(rows) > shown:
                ui.text(T.MATH_LIST_MORE.format(a=self.first + 1, b=min(len(rows), self.first + shown),
                                                t=len(rows)), x + 12, y + h - 13, 7, GREY, anchor="midleft")
        if ui.button("code_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()


class ProblemScene(Scene):
    """One exercise: the statement, the editor, and what the tests said."""

    def __init__(self, game, problem_id: str):
        super().__init__(game)
        self.problem_id = problem_id
        self.problem: dict | None = None
        self.box: CodeBox | None = None
        self.result: dict | None = None
        self.mode = ""                      # "run" | "submit" while one is going
        self.note = ""
        self.scroll = 0.0
        self.height = 0.0                   # how tall the statement is, for scrolling
        self.busy = False
        self._done: list[tuple] = []        # filled by the worker thread, read in update()
        self.log: tuple[int, dict] = (0, {})    # Xạ Trường: (which run, its training log)
        self.show_target = False            # Xạ Trường: the target view instead of the statement

    @property
    def scored(self) -> bool:
        return bool(self.problem and self.problem.get("scored"))

    # ------------------------------------------------------------ loading
    def on_enter(self):
        self.busy = True

        def ok(data):
            self.busy = False
            self.problem = data["problem"]
            path = solution_file(self.game, self.problem_id)
            try:
                text = path.read_text("utf-8")
            except OSError:
                text = self.problem.get("starter") or STARTER.format(title=self.problem["title_vi"])
            self.box = CodeBox(text, max_chars=self.problem.get("max_code_chars", 20000))
            self.game.ui.set_focus("code")
        self.api.get(f"/math/problem/{self.problem_id}", ok, self.fail)

    def fail(self, err):
        self.busy, self.mode, self.note = False, "", ""
        self.game.api_error(err)

    def save(self) -> None:
        if self.box is not None:
            coderun.write_solution(solution_file(self.game, self.problem_id), self.box.text)

    # ------------------------------------------------------------ running
    def _start(self, inputs: list[str], limit_ms: int, attempt_id: int | None) -> None:
        """Run the solution on these inputs in a thread, then send what it printed."""
        self.save()
        path, code = solution_file(self.game, self.problem_id), self.box.text

        def work():
            try:
                attempt = coderun.run_tests(path, inputs, limit_ms, code=code)
            except coderun.NoPython:
                self._done.append(("no_python", None, None))
                return
            self._done.append(("judge", attempt, attempt_id))
        threading.Thread(target=work, daemon=True, name="coderun").start()

    def run_samples(self):
        if self.busy or not self.problem:
            return
        self.busy, self.mode, self.result, self.note = True, "run", None, T.CODE_RUNNING
        self._start([s["in"] for s in self.problem["samples"]], self.problem["time_limit_ms"], None)

    def submit(self):
        if self.busy or not self.problem:
            return
        self.busy, self.mode, self.result, self.note = True, "submit", None, T.CODE_RUNNING

        def ok(data):
            self._start(data["inputs"], data["time_limit_ms"], data["attempt_id"])
        self.api.post(f"/math/problem/{self.problem_id}/tests", {}, ok, self.fail)

    def update(self, dt, top):
        while self._done:
            kind, attempt, attempt_id = self._done.pop(0)
            if kind == "no_python":
                self.busy, self.mode, self.note = False, "", ""
                self.game.push(MessageBox(self.game, T.CODE_NO_PYTHON, T.CODE_TITLE))
                continue
            self.note = T.CODE_SENDING
            self.log = attempt.log                      # stays here: the server never sees it
            body = {"outputs": attempt.outputs, "status": attempt.status,
                    "times_ms": attempt.times_ms, "error": attempt.error,
                    "code": self.box.text if attempt_id else ""}
            if attempt_id:
                body["attempt_id"] = attempt_id

            def ok(data):
                self.busy, self.mode, self.note = False, "", ""
                self.result = data
                self.show_target = bool(data.get("result", {}).get("scored"))
                self.game.on_xp(data.get("xp"))         # the HUD hears about the Tu Vi at once
                if data.get("xp_gained"):
                    self.game.toast(T.MATH_XP.format(n=data["xp_gained"]), UICOL["green"])
                if data.get("best"):
                    self.problem["best"] = data["best"]
            self.api.post(f"/math/problem/{self.problem_id}/judge", body, ok, self.fail)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 6, 4, 468, 262
        ui.panel(x, y, w, h, T.CODE_TITLE)
        if self.problem is None:
            ui.text(T.CODE_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
            if ui.button("code_back", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
                self.close()
            return
        p = self.problem
        ui.text(p["title_vi"], x + 10, y + 17, 10, UICOL["accent"], max_w=240)
        ui.text(f"{T.MATH_FLOOR.format(n=p['floor'])} · "
                f"{T.MATH_TIER_LABEL.format(n=p['tier'], name=p['tier_name_vi'])}",
                x + w - 10, y + 22, 7, GREY, anchor="midright")
        if self.show_target and self.result and self.result["result"].get("scored"):
            self.draw_target(ui, x + 10, y + 32, 196, 194)
        else:
            self.draw_statement(ui, x + 10, y + 32, 196, 194)
        self.draw_editor(ui, x + 214, y + 32, w - 224, 140)     # the buttons sit just under it
        self.draw_results(ui, x + 214, y + 192, w - 224, 44)
        ui.text(T.CODE_FILE.format(path=solution_file(self.game, self.problem_id).name), x + 10, y + h - 13, 7,
                "#9A9387", anchor="midleft")
        if ui.button("code_back", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.save()
            self.close()

    def draw_statement(self, ui, x, y, w, h):
        p = self.problem
        if ui.hover(x, y, w, h) and ui.inp.wheel:
            self.scroll = max(0.0, self.scroll - ui.inp.wheel * 8)
            ui.inp.wheel = 0
        ui.fill(x, y, w, h, "#F8F1E3")
        ui.border(x, y, w, h, "#C9BFA8")
        cy = y + 4 - self.scroll
        blocks: list[tuple[str, str, float]] = []
        for para in p["statement_vi"]:
            blocks.append(("text", para, 8))
        for label, body in ((T.CODE_INPUT, p["input_vi"]), (T.CODE_OUTPUT, p["output_vi"]),
                            (T.CODE_LIMITS, p["limits_vi"])):
            if body:
                blocks.append(("head", label, 8))
                blocks.append(("text", body, 7))
        for n, s in enumerate(p["samples"], 1):
            blocks.append(("head", T.CODE_SAMPLE.format(n=n), 8))
            if s.get("big"):                    # a generated practice set: too long to print
                blocks.append(("note", T.XT_PRACTICE.format(note=s.get("note_vi", "")), 7))
                continue
            blocks.append(("mono", s["in"].rstrip("\n"), 7))
            blocks.append(("arrow", s["out"].rstrip("\n"), 7))
            if s.get("note_vi"):
                blocks.append(("note", s["note_vi"], 7))
        if p.get("scored"):
            bars = " / ".join(bar_text(b, "do_chinh_xac" if p.get("higher_better") else "sai_so")
                              for b in p.get("grades", []))
            blocks.append(("note", T.XT_BARS.format(bars=bars), 7))
        style = {"head": (4, UICOL["accent"], 2), "mono": (8, "#2B2B2B", 1),
                 "arrow": (8, UICOL["green"], 2), "note": (8, GREY, 3), "text": (4, "#2B2B2B", 3)}
        clip = ui.win.get_clip()
        ui.win.set_clip(ui.rect(x, y + 1, w, h - 2))     # a long statement scrolls inside its box
        try:
            for kind, text, size in blocks:
                indent, colour, gap = style[kind]
                if kind == "arrow":
                    text = "-> " + text.replace("\n", " / ")
                block_h = self._height(ui, text, size, w - indent - 4)
                if y - block_h < cy < y + h - 2:        # only what the window can show is drawn
                    ui.text(text, x + indent, cy, size, colour, max_w=w - indent - 4)
                cy += block_h + gap
        finally:
            ui.win.set_clip(clip)
        self.height = (cy + self.scroll) - (y + 4)  # the whole statement, scrolled or not
        self.scroll = max(0.0, min(self.scroll, max(0.0, self.height - h + 8)))

    @staticmethod
    def _height(ui, text: str, size: float, max_w: float) -> float:
        """How tall ui.text will draw this, without drawing it: the same sum ui.text makes,
        over the same rendered lines (cached), so a line with stacked Vietnamese marks,
        taller than "Ag", is counted at its real height."""
        lines = ui.f.wrap(text, size, int(max_w * ui.s), ui.s) or [""]
        heights = [ui.f.render(line, size, "#2B2B2B", ui.s).get_height() for line in lines]
        lh = max(heights) * (1.15 if len(heights) > 1 else 1)
        return (lh * (len(heights) - 1) + heights[-1]) / ui.s

    def draw_editor(self, ui, x, y, w, h):
        focused = ui.focus == "code" and not self.busy
        if ui.click_in(x, y, w, h):
            ui.set_focus("code")
            focused = True
        if focused:
            self.box.handle(ui)
        self.box.draw(ui, x, y, w, h, focused)
        by = y + h + 4
        if ui.button("code_run", x, by, 70, 14, T.CODE_RUN, size=7, style="primary",
                     enabled=not self.busy, key=pygame.K_F5):
            self.run_samples()
        if ui.button("code_submit", x + 76, by, 70, 14, T.CODE_SUBMIT, size=7, style="gold",
                     enabled=not self.busy, key=pygame.K_F9):
            self.submit()
        if ui.button("code_save", x + 152, by, 50, 14, T.CODE_SAVE, size=7, enabled=not self.busy):
            self.save()
            self.game.toast(T.CODE_SAVED)
        best = self.problem.get("best") or {}
        if best and "grade" in best:
            pass                        # a scored exercise shows its best grade under the buttons
        elif best:
            ui.text(T.CODE_BEST.format(v=best["verdict"], p=best["passed"], t=best["total"]),
                    x + w, by + 7, 7, VERDICT_COLOUR.get(best["verdict"], GREY), anchor="midright")

    def draw_results(self, ui, x, y, w, h):
        if self.note:
            ui.text(self.note, x, y + 6, 8, "#C99A3A")
            return
        if not self.result:
            limit = T.XT_TIME_LIMIT if self.scored else T.CODE_TIME_LIMIT
            ui.text(limit.format(n=round(self.problem["time_limit_ms"] / 1000, 1)), x, y + 6, 7, GREY)
            best = self.problem.get("best") or {}
            if "grade" in best:
                ui.text(T.XT_BEST.format(g=best["grade_vi"]), x, y + 18, 7, GRADE_COLOUR[best["grade"]])
            return
        res = self.result["result"]
        sample = self.result.get("mode") == "run"
        if res.get("scored"):
            self.draw_scored_line(ui, res, x, y, w, h)
            return
        colour = VERDICT_COLOUR.get(res["verdict"], GREY)
        ui.text(verdict_text(res["verdict"]), x, y + 6, 10, colour, anchor="midleft")
        tail = T.CODE_PASSED.format(p=res["passed"], t=res["total"])
        if res.get("ms"):
            tail += "   " + T.MATH_SECONDS.format(n=round(res["ms"] / 1000, 2))
        ui.text(tail, x + w, y + 6, 7, GREY, anchor="midright")
        cy = y + 16
        line = "   ".join(
            (T.CODE_SAMPLE_LINE if sample else T.CODE_TEST_LINE).format(n=t["test"], v=t["verdict"])
            for t in res["tests"][:8])
        cy += ui.text(line, x, cy, 7, GREY, max_w=w).h + 2
        if res.get("error"):
            ui.text(res["error"].strip().splitlines()[-1][:120], x, cy, 7, UICOL["accent"], max_w=w)

    # ------------------------------------------------------------ Xa Truong: scored results
    def draw_scored_line(self, ui, res: dict, x, y, w, h):
        """Under the editor: the grade, the score and the switch to the target view."""
        ui.text(res.get("grade_vi", ""), x, y + 6, 10, GRADE_COLOUR[res.get("grade", 0)], anchor="midleft")
        ui.text(metric_text(res.get("score"), res.get("metric", "")), x + w, y + 6, 7, GREY, anchor="midright")
        label = T.XT_SHOW_STATEMENT if self.show_target else T.XT_SHOW_TARGET
        if ui.button("code_target", x, y + 16, 60, 13, label, size=7):
            self.show_target = not self.show_target
        if res.get("error"):
            ui.text(res["error"].strip().splitlines()[-1][:120], x + 66, y + 17, 7, UICOL["accent"], max_w=w - 66)

    def draw_target(self, ui, x, y, w, h):
        """The target view of a scored result: grade, each set against the bars, loss curve."""
        res = self.result["result"]
        metric, bars, higher = res.get("metric", ""), res.get("grades", []), res.get("higher_better", True)
        ui.fill(x, y, w, h, "#F8F1E3")
        ui.border(x, y, w, h, "#C9BFA8")
        sample = self.result.get("mode") == "run"
        ui.text(T.XT_TARGET_PRACTICE if sample else T.XT_TARGET_HIDDEN, x + 4, y + 4, 8, UICOL["accent"])
        ui.text(res.get("grade_vi", ""), x + 4, y + 22, 12, GRADE_COLOUR[res.get("grade", 0)], anchor="midleft")
        ui.text(metric_text(res.get("score"), metric), x + w - 4, y + 22, 8, "#2B2B2B", anchor="midright")
        cy = y + 32 + ui.text(T.XT_BARS.format(bars=" / ".join(bar_text(b, metric) for b in bars)), x + 4, y + 32,
                              7, GREY, max_w=w - 8).h + 3
        for t in res.get("tests", [])[:6]:
            score = t.get("score")
            if score is None and t["verdict"] not in ("AC", "WA"):
                value = verdict_text(t["verdict"])
            else:
                value = set_note(t) or score_text(score, metric)
            ring = GRADE_COLOUR[grade_of(score, bars, higher)]
            ui.fill(x + 6, cy + 1, 7, 7, ring, radius=3)           # a small target per set
            ui.fill(x + 8, cy + 3, 3, 3, "#F8F1E3", radius=1)
            line = (T.XT_SAMPLE_SET_LINE if sample else T.XT_SET_LINE).format(n=t["test"], v=value)
            ui.text(line, x + 17, cy, 7, "#2B2B2B", max_w=w - 22)
            cy += 10
        self.draw_loss(ui, x + 4, cy + 4, w - 8, y + h - (cy + 4) - 18)
        if ui.button("code_statement", x + w - 58, y + h - 16, 54, 13, T.XT_SHOW_STATEMENT, size=7):
            self.show_target = False

    def draw_loss(self, ui, x, y, w, h):
        """The training log as a curve: loss in the accent colour, #val lighter."""
        run, log = self.log
        loss = log.get("loss", []) if log else []
        if h < 30 or not loss:
            ui.text(T.XT_LOSS_NONE, x, y + 2, 7, GREY, max_w=w)
            return
        where = (T.XT_WHERE_SAMPLE if self.result.get("mode") == "run" else T.XT_WHERE_SET).format(n=run)
        ui.text(T.XT_LOSS_TITLE.format(where=where), x, y, 7, UICOL["accent"])
        cx, cy, cw, ch = x + 2, y + 11, w - 4, h - 22
        ui.fill(cx, cy, cw, ch, "#FFFDF7")
        ui.border(cx, cy, cw, ch, "#D8CFBA")
        val = log.get("val", [])
        finite = [v for _, v in loss + val if math.isfinite(v)]
        steps = [s for s, _ in loss + val]
        blown = any(not math.isfinite(v) for _, v in loss + val)
        if finite and len(steps) >= 2:
            # a loss that falls by orders of magnitude is drawn on a log scale, or the first
            # steps flatten everything after them
            log_scale = min(finite) > 0 and max(finite) / min(finite) > 20
            ys = [math.log10(v) for v in finite] if log_scale else finite
            lo, hi = min(ys), max(ys)
            s0, s1 = min(steps), max(steps)
            span_v, span_s = (hi - lo) or 1.0, (s1 - s0) or 1.0

            def to_px(s, v):
                v = math.log10(v) if log_scale else v
                return ui.d.to_window(cx + 2 + (s - s0) / span_s * (cw - 4),
                                      cy + ch - 2 - (v - lo) / span_v * (ch - 4))
            if log_scale:
                ui.text(T.XT_LOSS_LOG, cx + cw - 3, cy + 2, 6, GREY, anchor="topright")
            for points, colour in ((val, "#C9A27A"), (loss, UICOL["accent"])):
                pts = [to_px(s, v) for s, v in points if math.isfinite(v)]
                if len(pts) >= 2:
                    pygame.draw.lines(ui.win, pygame.Color(colour), False, pts, max(1, ui.s))
            first = next(v for _, v in loss if math.isfinite(v)) if any(math.isfinite(v) for _, v in loss) else None
            last = next((v for _, v in reversed(loss) if math.isfinite(v)), None)
            if first is not None and last is not None:
                text = T.XT_LOSS_RANGE.format(a=f"{first:.4g}".replace(".", ","), b=f"{last:.4g}".replace(".", ","),
                                              n=len(loss))
                if val:
                    text += " · " + T.XT_LOSS_VAL
                ui.text(text, x, cy + ch + 2, 7, GREY, max_w=w)
        if blown:
            ui.text(T.XT_LOSS_BLOWN, cx + 4, cy + 4, 7, UICOL["accent"], max_w=cw - 8)
