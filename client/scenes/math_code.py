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
from ..ui.mathtext import pretty
from ..ui.mono import TextPane, wrap_prose
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


def fit_title(ui, text: str, max_w: float, sizes=(8, 7)) -> tuple[float, list[str]]:
    """The largest size at which `text` fits on one line of `max_w`; failing that, the
    smallest size on as many lines as it needs - a title is never cut with "..."."""
    for size in sizes:
        lines = wrap_prose(ui, text, size, max_w)
        if len(lines) == 1:
            return size, lines
    return sizes[-1], wrap_prose(ui, text, sizes[-1], max_w)


def head_lines(text: str, keep: int = 40) -> tuple[str, int]:
    """The first `keep` lines of a program's output (what a long output shows) and how many
    lines are left out."""
    lines = (text or "").rstrip("\n").split("\n")
    return "\n".join(lines[:keep]), max(0, len(lines) - keep)


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
            # a long title takes a second line (at a size smaller) instead of being cut, so rows
            # differ in height: the list scrolls by rows, and shows the ones that fit whole
            rows = []
            for f in floors:
                head = f"{T.MATH_FLOOR.format(n=f['floor'])} · {f['title_vi']}"
                hs, hl = fit_title(ui, head, w - 24, sizes=(8, 7))
                rows.append((f, None, hs, hl, 6 + 9 * len(hl) if len(hl) > 1 else 16))
                for p in f["problems"]:
                    ts, tl = fit_title(ui, p["title_vi"], 152, sizes=(8, 7))
                    rows.append((f, p, ts, tl, 16 if len(tl) == 1 else 4 + 9 * len(tl)))
            top, bottom = y + 34, y + h - 24

            def fits(start):
                used, k = 0, 0
                for r in rows[start:]:
                    if used + r[4] > bottom - top:
                        break
                    used, k = used + r[4], k + 1
                return k
            last_first = 0
            while last_first < len(rows) and fits(last_first) < len(rows) - last_first:
                last_first += 1
            shown = fits(min(self.first, last_first))
            self.first = min(last_first, scroll_rows(ui, self.first, len(rows), shown, x, top, w, bottom - top))
            shown = fits(self.first)
            cy = top
            for f, p, size, lines, rh in rows[self.first:self.first + shown]:
                if p is None:
                    for k, line in enumerate(lines):
                        ui.text(line, x + 12, cy + 2 + 9 * k, size, UICOL["accent"])
                    cy += rh
                    continue
                best = p.get("best") or {}
                mid = cy + rh / 2 - 1
                for k, line in enumerate(lines):
                    ui.text(line, x + 18, mid + (k - (len(lines) - 1) / 2) * 9, size, "#2B2B2B",
                            anchor="midleft")
                ui.text(T.MATH_TIER_ONE.format(lo=p["tier"]), x + 176, mid, 7, GREY, anchor="midleft")
                if best and "grade" in best:        # a scored exercise: its best grade instead of the count
                    ui.text(best["grade_vi"], x + 212, mid, 7, GRADE_COLOUR[best["grade"]], anchor="midleft")
                else:
                    ui.text((T.XT_HIDDEN_SETS if p.get("scored") else T.CODE_HIDDEN_TESTS).format(n=p["tests"]),
                            x + 212, mid, 7, GREY, anchor="midleft")
                if best and "grade" in best:
                    pass
                elif best:
                    ui.text(best["verdict"], x + w - 84, mid, 7,
                            VERDICT_COLOUR.get(best["verdict"], GREY), anchor="midright")
                if ui.button(f"code_open_{p['id']}", x + w - 78, mid - 7, 66, 13, T.CODE_OPEN, size=7,
                             style="primary", enabled=not self.busy):
                    self.game.push(ProblemScene(self.game, p["id"]))
                cy += rh
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
        self.show_detail = False            # the result in full (each test, what was printed, the error)
        self.outputs: list[str] = []        # what the program printed on the samples (Chạy thử)
        self.statement_pane = TextPane()
        self.detail_pane = TextPane()
        self.result_pane = TextPane()

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
            self.outputs = [] if attempt_id else list(attempt.outputs)
            body = {"outputs": attempt.outputs, "status": attempt.status,
                    "times_ms": attempt.times_ms, "error": attempt.error,
                    "code": self.box.text if attempt_id else ""}
            if attempt_id:
                body["attempt_id"] = attempt_id

            def ok(data):
                self.busy, self.mode, self.note = False, "", ""
                self.result = data
                self.show_target = bool(data.get("result", {}).get("scored"))
                # a crash or a compile error: its message is what to read next, in full
                self.show_detail = not self.show_target and bool((data.get("result") or {}).get("error"))
                self.detail_pane.first = 0
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
        where = (f"{T.MATH_FLOOR.format(n=p['floor'])} · "
                 f"{T.MATH_TIER_LABEL.format(n=p['tier'], name=p['tier_name_vi'])}")
        ui.text(where, x + w - 10, y + 22, 7, GREY, anchor="midright")
        room = w - 30 - ui.text_size(where, 7)[0]           # the title, as large as fits on its line
        size, lines = fit_title(ui, p["title_vi"], room, sizes=(10, 9, 8, 7))
        if len(lines) == 1:
            ui.text(lines[0], x + 10, y + 22, size, UICOL["accent"], anchor="midleft")
        else:                                               # two small lines in the same band
            for k, line in enumerate(lines[:2]):
                ui.text(line, x + 10, y + 13 + 9 * k, 7, UICOL["accent"])
        if self.show_detail and self.result:
            self.draw_detail(ui, x + 10, y + 32, 196, 194)
        elif self.show_target and self.result and self.result["result"].get("scored"):
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

    def statement_blocks(self) -> tuple:
        """The statement as TextPane blocks: prose with its maths drawn as maths (pretty), the
        samples verbatim in monospace boxes."""
        p = self.problem
        ink, x_ink = "#2B2B2B", UICOL["accent"]
        blocks = [("text", pretty(para), 8, ink, 2, 3) for para in p["statement_vi"]]
        for label, body in ((T.CODE_INPUT, p["input_vi"]), (T.CODE_OUTPUT, p["output_vi"]),
                            (T.CODE_LIMITS, p["limits_vi"])):
            if body:
                blocks.append(("text", label, 8, x_ink, 2, 1))
                blocks.append(("text", pretty(body), 7, ink, 6, 3))
        for n, s in enumerate(p["samples"], 1):
            blocks.append(("text", T.CODE_SAMPLE.format(n=n), 8, x_ink, 2, 1))
            if s.get("big"):                    # a generated practice set: too long to print
                blocks.append(("text", pretty(T.XT_PRACTICE.format(note=s.get("note_vi", ""))), 7, GREY, 6, 3))
                continue
            blocks.append(("text", T.CODE_SAMPLE_IN, 7, GREY, 6, 1))
            blocks.append(("mono", s["in"].rstrip("\n"), 7, ink, 8, 2))
            blocks.append(("text", T.CODE_SAMPLE_OUT, 7, GREY, 6, 1))
            blocks.append(("mono", s["out"].rstrip("\n"), 7, "#2F6B3A", 8, 2))
            if s.get("note_vi"):
                blocks.append(("text", pretty(s["note_vi"]), 7, GREY, 6, 3))
        if p.get("scored"):
            bars = " / ".join(bar_text(b, "do_chinh_xac" if p.get("higher_better") else "sai_so")
                              for b in p.get("grades", []))
            blocks.append(("text", T.XT_BARS.format(bars=bars), 7, GREY, 2, 3))
        return tuple(blocks)

    def draw_statement(self, ui, x, y, w, h):
        """The statement scrolls inside its box: the wheel over it, PgUp / PgDn while the
        editor does not have the keys (a click on the statement takes them), a scrollbar."""
        if ui.click_in(x, y, w, h):
            ui.set_focus("statement")
        ui.fill(x, y, w, h, "#F8F1E3")
        ui.border(x, y, w, h, "#C9BFA8")
        pane = self.statement_pane
        pane.draw(ui, x + 2, y + 1, w - 3, h - 2, self.statement_blocks(), keys=ui.focus != "code")
        self.scroll, self.height = pane.first, len(pane.rows)

    def detail_blocks(self) -> tuple:
        """The last result in full: each test, on the samples what the program printed against
        the right answer, and the whole error message, verbatim."""
        res = self.result["result"]
        sample = self.result.get("mode") == "run"
        colour = VERDICT_COLOUR.get(res["verdict"], GREY)
        blocks = [("text", verdict_text(res["verdict"]), 9, colour, 0, 1),
                  ("text", self.tail_text(res), 7, GREY, 0, 3)]
        tests = res.get("tests", [])
        if sample:
            samples = self.problem.get("samples", [])
            for t in tests:
                blocks.append(("text", T.CODE_SAMPLE_LINE.format(n=t["test"], v=verdict_text(t["verdict"])), 7,
                               VERDICT_COLOUR.get(t["verdict"], GREY), 0, 1))
                k = t["test"] - 1
                if t["verdict"] == "WA" and 0 <= k < len(samples) and not samples[k].get("big"):
                    got, more = head_lines(self.outputs[k] if k < len(self.outputs) else "")
                    want, more_w = head_lines(samples[k]["out"])
                    blocks.append(("text", T.CODE_GOT, 7, GREY, 4, 1))
                    blocks.append(("mono", got if got.strip() else T.CODE_PRINTED_NOTHING, 7, "#2B2B2B", 6, 1))
                    if more:
                        blocks.append(("text", T.CODE_MORE_LINES.format(n=more), 7, GREY, 6, 1))
                    blocks.append(("text", T.CODE_WANT, 7, GREY, 4, 1))
                    blocks.append(("mono", want, 7, "#2F6B3A", 6, 1))
                    if more_w:
                        blocks.append(("text", T.CODE_MORE_LINES.format(n=more_w), 7, GREY, 6, 1))
                    blocks.append(("text", "", 4, GREY, 0, 1))
        elif tests:
            line = "   ".join(T.CODE_TEST_LINE.format(n=t["test"], v=t["verdict"]) for t in tests)
            blocks.append(("text", line, 7, GREY, 0, 3))
        if res.get("error"):
            blocks.append(("text", T.CODE_ERROR, 7, UICOL["accent"], 0, 1))
            blocks.append(("mono", res["error"].strip("\n"), 7, "#8A2E1F", 2, 2))
        return tuple(blocks)

    def draw_detail(self, ui, x, y, w, h):
        if ui.click_in(x, y, w, h - 18):
            ui.set_focus("statement")
        ui.fill(x, y, w, h, "#F8F1E3")
        ui.border(x, y, w, h, "#C9BFA8")
        ui.text(T.CODE_DETAIL_TITLE, x + 4, y + 3, 8, UICOL["accent"])
        self.detail_pane.draw(ui, x + 2, y + 14, w - 3, h - 34, self.detail_blocks(), keys=ui.focus != "code")
        if ui.button("code_statement", x + w - 58, y + h - 16, 54, 13, T.XT_SHOW_STATEMENT, size=7):
            self.show_detail = False

    @staticmethod
    def tail_text(res: dict) -> str:
        tail = T.CODE_PASSED.format(p=res["passed"], t=res["total"])
        if res.get("ms"):
            tail += "   " + T.MATH_SECONDS.format(n=round(res["ms"] / 1000, 2))
        return tail

    def draw_editor(self, ui, x, y, w, h):
        focused = ui.focus == "code" and not self.busy
        if ui.hover(x, y, w, h) and (ui.inp.clicked or ui.inp.mouse_down):
            ui.set_focus("code")            # (the box itself takes the click: it moves the caret)
            focused = not self.busy
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
        if ui.button("code_detail", x + w - 50, y, 50, 12, T.CODE_DETAIL, size=7, selected=self.show_detail):
            self.show_detail = not self.show_detail
            self.detail_pane.first = 0
        line = "   ".join(
            (T.CODE_SAMPLE_LINE if sample else T.CODE_TEST_LINE).format(n=t["test"], v=t["verdict"])
            for t in res["tests"])
        blocks = [("text", self.tail_text(res) + "   " + line, 7, GREY, 0, 1)]
        if res.get("error"):            # the last line first: the name of the error; Chi tiết has it all
            last = res["error"].strip().splitlines()[-1] if res["error"].strip() else ""
            blocks.append(("mono", last, 7, "#8A2E1F", 2, 1))
        self.result_pane.draw(ui, x - 2, y + 13, w + 2, h - 13, tuple(blocks))

    # ------------------------------------------------------------ Xa Truong: scored results
    def draw_scored_line(self, ui, res: dict, x, y, w, h):
        """Under the editor: the grade, the score and the switch to the target view."""
        ui.text(res.get("grade_vi", ""), x, y + 6, 10, GRADE_COLOUR[res.get("grade", 0)], anchor="midleft")
        ui.text(metric_text(res.get("score"), res.get("metric", "")), x + w, y + 6, 7, GREY, anchor="midright")
        label = T.XT_SHOW_STATEMENT if self.show_target else T.XT_SHOW_TARGET
        if ui.button("code_target", x, y + 16, 60, 13, label, size=7):
            self.show_target = not self.show_target
        if res.get("error"):
            last = res["error"].strip().splitlines()[-1] if res["error"].strip() else ""
            self.result_pane.draw(ui, x + 64, y + 14, w - 64, h - 14, (("mono", last, 7, "#8A2E1F", 2, 1),))

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
