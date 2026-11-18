"""Bài tập lập trình (milestone M6): read the statement, write a solution, Chạy thử on the
samples, Nộp bài on the hidden tests.

The solution runs here, on the player's own machine (client/engine/coderun.py), in a thread
so the game keeps drawing while it runs. What goes back to the server is only what the
program printed; the server keeps the expected answers and decides AC / WA / TLE / RE / CE.

The code also lives in a real file under the game's data folder, so anyone who would rather
write Python in their own editor can do that and press Chạy thử here.
"""
from __future__ import annotations

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


class ProblemListScene(Scene):
    """The exercises of a subject, floor by floor. Locked floors are not in the answer."""

    def __init__(self, game, subject_id: str, floor: int | None = None):
        super().__init__(game)
        self.subject_id, self.floor = subject_id, floor
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

        def ok(data):
            self.busy, self.data = False, data
        self.api.get(query, ok, self.fail)

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 60, 24, 360, 222
        ui.panel(x, y, w, h, T.CODE_TITLE)
        floors = (self.data or {}).get("floors") or []
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
                ui.text(T.CODE_HIDDEN_TESTS.format(n=p["tests"]), x + 212, cy + 7, 7, GREY,
                        anchor="midleft")
                if best:
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
                text = STARTER.format(title=self.problem["title_vi"])
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
            body = {"outputs": attempt.outputs, "status": attempt.status,
                    "times_ms": attempt.times_ms, "error": attempt.error,
                    "code": self.box.text if attempt_id else ""}
            if attempt_id:
                body["attempt_id"] = attempt_id

            def ok(data):
                self.busy, self.mode, self.note = False, "", ""
                self.result = data
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
        ui.text(p["title_vi"], x + 10, y + 20, 10, UICOL["accent"], max_w=240)
        ui.text(f"{T.MATH_FLOOR.format(n=p['floor'])} · "
                f"{T.MATH_TIER_LABEL.format(n=p['tier'], name=p['tier_name_vi'])}",
                x + w - 10, y + 22, 7, GREY, anchor="midright")
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
            blocks.append(("mono", s["in"].rstrip("\n"), 7))
            blocks.append(("arrow", s["out"].rstrip("\n"), 7))
            if s.get("note_vi"):
                blocks.append(("note", s["note_vi"], 7))
        style = {"head": (4, UICOL["accent"], 2), "mono": (8, "#2B2B2B", 1),
                 "arrow": (8, UICOL["green"], 2), "note": (8, GREY, 3), "text": (4, "#2B2B2B", 3)}
        for kind, text, size in blocks:
            indent, colour, gap = style[kind]
            if kind == "arrow":
                text = "-> " + text.replace("\n", " / ")
            block_h = self._height(ui, text, size, w - indent - 4)
            if y - block_h < cy < y + h - 2:        # only what the window can show is drawn
                ui.text(text, x + indent, cy, size, colour, max_w=w - indent - 4)
            cy += block_h + gap
        self.height = (cy + self.scroll) - (y + 4)  # the whole statement, scrolled or not
        self.scroll = max(0.0, min(self.scroll, max(0.0, self.height - h + 8)))

    @staticmethod
    def _height(ui, text: str, size: float, max_w: float) -> float:
        """How tall ui.text will draw this, without drawing it."""
        lines = ui.f.wrap(text, size, int(max_w * ui.s), ui.s) or [""]
        line_h = ui.text_size("Ag", size)[1]
        return line_h * (1.15 * (len(lines) - 1) + 1)

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
        if best:
            ui.text(T.CODE_BEST.format(v=best["verdict"], p=best["passed"], t=best["total"]),
                    x + w, by + 7, 7, VERDICT_COLOUR.get(best["verdict"], GREY), anchor="midright")

    def draw_results(self, ui, x, y, w, h):
        if self.note:
            ui.text(self.note, x, y + 6, 8, "#C99A3A")
            return
        if not self.result:
            ui.text(T.CODE_TIME_LIMIT.format(n=round(self.problem["time_limit_ms"] / 1000, 1)),
                    x, y + 6, 7, GREY)
            return
        res = self.result["result"]
        sample = self.result.get("mode") == "run"
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
