"""The code editor (client/ui/codebox.py) and the exercise screen (client/scenes/math_code.py):
one cell per character, sideways scrolling, nothing drawn outside the box, a statement that
scrolls whole lines, results and tracebacks that stay in their panel - at window scales 2 and 3.

Run as a script with an output folder to get screenshots:
    python -m client.tests.test_code_editor <outdir>
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

import pygame  # noqa: E402
import pytest  # noqa: E402

from client.engine.display import Display  # noqa: E402
from client.engine.text import Fonts  # noqa: E402
from client.ui import audit  # noqa: E402
from client.ui.codebox import CodeBox  # noqa: E402
from client.ui.kit import UI  # noqa: E402
from client.ui.mono import cell, clean_text, one_cell, wrap_cells  # noqa: E402

pygame.init()
FONTS = Fonts()
WIDE = "ư"                                 # VT323 draws it a pixel wider than a digit
LONG = "x = [" + ", ".join(str(i * 7) for i in range(80)) + "]  # danh sách dài, có chữ ư ừ ự"
TRACEBACK = "\n".join(
    ["Traceback (most recent call last):",
     '  File "C:/Users/nguoi_choi/AppData/Roaming/ToanTuTien/bai_lam/nhan_ma_tran_rat_dai_ten.py", line 12, in <module>',
     "    print(nhan(doc_ma_tran(sys.stdin.read().split()), doc_ma_tran(sys.stdin.read().split())))",
     '  File "C:/Users/nguoi_choi/AppData/Roaming/ToanTuTien/bai_lam/nhan_ma_tran_rat_dai_ten.py", line 7, in nhan',
     "    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]",
     "IndexError: list index out of range - chỉ số vượt quá kích thước của danh sách khi nhân hai ma trận không khớp cỡ"])


def make_ui(scale: int) -> UI:
    return UI(Display(0, False, size=(480 * scale, 270 * scale)), FONTS)


def frame(ui: UI, draw, events=(), mouse=None) -> list:
    ui.audit = []
    ui.begin(list(events), 0.016)
    if mouse is not None:
        ui.inp.mouse = mouse
    draw()
    rec, ui.audit = ui.audit, None
    return rec


def hard(found) -> list:
    return [p for p in found if p.kind in audit.HARD]


# ------------------------------------------------------------------ the scene, faked
class _Api:
    def get(self, *a, **k): ...

    def post(self, *a, **k): ...


def fake_game(ui: UI, tmp: Path):
    return SimpleNamespace(ui=ui, api=_Api(), session=SimpleNamespace(path=tmp / "session.json"),
                           toast=lambda *a, **k: None, push=lambda *a: None, pop=lambda *a: None,
                           on_xp=lambda *a: None, api_error=lambda *a: None, scenes=[], audio=None)


def longest_problem() -> dict:
    """The exercise of the bank with the longest statement, as the server sends it."""
    from app.learning import math_problems
    best = max(math_problems.bank().values(),
               key=lambda p: sum(len(s) for s in p.statement_vi) + len(p.input_vi) + len(p.output_vi)
               + sum(len(s.data) + len(s.expected) for s in p.fixed_samples))
    return best.view()


def failing_result(problem: dict) -> dict:
    n = len(problem["samples"])
    tests = [{"test": i + 1, "verdict": "RE" if i == n - 1 else ("WA" if i else "AC"), "ms": 30} for i in range(n)]
    return {"mode": "run", "problem_id": problem["id"],
            "result": {"verdict": "RE", "passed": 1, "total": n, "share": 0.0, "ms": 31,
                       "error": TRACEBACK, "tests": tests}}


def code_scene(ui: UI, tmp: Path, problem: dict | None = None, code: str | None = None):
    from client.scenes.math_code import ProblemScene
    scene = ProblemScene(fake_game(ui, tmp), "audit")
    scene.problem = problem or longest_problem()
    scene.box = CodeBox(code if code is not None else "import sys\n" + LONG + "\nprint(x)\n")
    ui.focus = "code"
    return scene


def scene_problems(ui: UI, scene) -> list:
    rec = frame(ui, lambda: scene.draw_ui(ui))
    return audit.problems(rec, panel=(6, -4, 468, 270))


# ------------------------------------------------------------------ cells
def test_every_character_takes_one_cell_wide_letters_included():
    ui = make_ui(3)
    cw, _ = cell(ui, 7)
    assert not one_cell(ui, WIDE, 7)            # the case this is all about
    box = CodeBox("# " + WIDE * 10 + "abc")
    rec = frame(ui, lambda: box.draw(ui, 10, 10, 300, 100))
    xs = [r["rect"][0] for r in rec if r.get("kind") == "text" and r["text"] == WIDE]
    assert len(xs) == 10
    steps = {round(b - a, 3) for a, b in zip(xs, xs[1:])}
    assert steps == {round(cw, 3)}
    box.row, box.col = 0, 12                    # just after the wide letters: under the "a"
    frame(ui, lambda: box.draw(ui, 10, 10, 300, 100))
    cx, _ = box.caret_xy()
    g = box.geometry
    assert cx == pytest.approx(g["text_x"] + 12 * cw)
    assert box.cell_at(cx + 0.2, g["text_y"] + 1) == (0, 12)


def test_a_click_lands_on_the_cell_under_the_mouse():
    ui = make_ui(2)
    box = CodeBox("ưưư = 1\nb = 2")
    frame(ui, lambda: box.draw(ui, 10, 10, 300, 100))
    g = box.geometry
    pos = ui.d.to_window(g["text_x"] + 2 * g["cw"] + 0.3, g["text_y"] + g["line_h"] * 1.5)
    up = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos)
    frame(ui, lambda: box.draw(ui, 10, 10, 300, 100), [up])
    assert (box.row, box.col) == (1, 2)


def test_a_long_line_scrolls_sideways_and_never_draws_outside_the_box():
    for scale in (2, 3):
        ui = make_ui(scale)
        box = CodeBox("a = 1\n" + "y" * 320 + "\n")
        box.row, box.col = 1, 320                       # the end of the long line
        rec = frame(ui, lambda: box.draw(ui, 20, 20, 200, 80))
        assert box.left > 0 and box.caret_xy() is not None
        assert hard(audit.problems(rec, panel=(20, 20, 200, 80))) == []
        texts = [r for r in rec if r.get("kind") == "text" and set(r["text"]) == {"y"}]
        assert texts and all(r["ink"][0] + r["ink"][2] <= 20 + 200 for r in texts)
        assert sum(len(r["text"]) for r in texts) == box.cols_shown or \
            sum(len(r["text"]) for r in texts) == 320 - box.left
        box.row, box.col = 0, 0                         # back home: the view follows the caret
        frame(ui, lambda: box.draw(ui, 20, 20, 200, 80))
        assert box.left == 0


def test_marks_show_a_line_goes_on_left_or_right():
    ui = make_ui(2)
    box = CodeBox("z" * 300)
    box.col = 150
    frame(ui, lambda: box.draw(ui, 20, 20, 200, 80))
    g = box.geometry
    accent = pygame.Color("#C0392B") if False else None
    x_left = ui.d.to_window(g["text_x"] - 2, g["text_y"] + 3)
    x_right = ui.d.to_window(g["text_x"] + box.cols_shown * g["cw"] + 1.5, g["text_y"] + 3)
    bg = ui.win.get_at(ui.d.to_window(g["text_x"] - 2, g["text_y"] + 3 + g["line_h"] * 2))
    assert ui.win.get_at(x_left) != bg and ui.win.get_at(x_right) != bg
    del accent


def test_tabs_empty_files_and_control_characters():
    box = CodeBox("if x:\n\treturn 1\x00\x07")
    assert box.lines == ["if x:", "    return 1"]
    assert CodeBox("").lines == [""]
    ui = make_ui(2)
    box = CodeBox("")
    rec = frame(ui, lambda: box.draw(ui, 10, 10, 200, 80))
    assert hard(audit.problems(rec)) == []
    assert clean_text("a\tb") == "a   b" and wrap_cells("abcdef", 4) == [("abcd", True), ("ef", False)]


def test_five_hundred_lines_scroll_with_the_caret():
    ui = make_ui(2)
    box = CodeBox("\n".join(f"print({i})" for i in range(500)))
    frame(ui, lambda: box.draw(ui, 10, 10, 200, 120))
    box.row = 499
    rec = frame(ui, lambda: box.draw(ui, 10, 10, 200, 120))
    assert box.top == 500 - box.rows_shown
    assert hard(audit.problems(rec, panel=(10, 10, 200, 120))) == []
    up = pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=5, flipped=False)
    frame(ui, lambda: box.draw(ui, 10, 10, 200, 120), [up], mouse=(50, 50))
    assert box.top == 500 - box.rows_shown - 15      # the wheel scrolls; the caret does not pull it back
    frame(ui, lambda: box.draw(ui, 10, 10, 200, 120))
    assert box.top == 500 - box.rows_shown - 15


def test_pasting_a_block_keeps_its_own_indent_and_the_limit():
    box = CodeBox("def f():\n    ")
    box.row, box.col = 1, 4
    box.paste("if x:\n\tprint(1)\nreturn 2")
    assert box.lines == ["def f():", "    if x:", "    print(1)", "return 2"]
    assert (box.row, box.col) == (3, 8)
    box = CodeBox("", max_chars=10)
    box.paste("a\nb\nc\nd\ne\nf\ng")
    assert len(box.text) == 10


def test_enter_after_a_colon_indents_one_step_more():
    box = CodeBox("    for i in range(3):")
    box.col = len(box.lines[0])
    box.insert("\n")
    assert box.lines[1] == "        " and box.col == 8


def test_selection_copy_cut_and_typing_over_it():
    box = CodeBox("abc\ndef")
    box.anchor, box.row, box.col = (0, 1), 1, 2
    assert box.selected_text() == "bc\nde"
    box.insert("X")
    assert box.lines == ["aXf"] and box.col == 2
    box.select_all()
    assert box.selected_text() == "aXf"
    box.backspace()
    assert box.lines == [""]


def test_the_selection_is_drawn_under_the_cells():
    ui = make_ui(2)
    box = CodeBox("hello world")
    box.anchor, box.col = (0, 0), 5
    frame(ui, lambda: box.draw(ui, 10, 10, 200, 60))
    g = box.geometry
    inside = ui.win.get_at(ui.d.to_window(g["text_x"] + 0.5, g["text_y"] + g["line_h"] - 0.6))
    outside = ui.win.get_at(ui.d.to_window(g["text_x"] + 8 * g["cw"] + 0.5, g["text_y"] + g["line_h"] - 0.6))
    assert inside != outside


# ------------------------------------------------------------------ the exercise screen
@pytest.mark.parametrize("scale", [2, 3])
def test_the_exercise_screen_with_the_longest_statement_and_a_long_line(scale, tmp_path):
    ui = make_ui(scale)
    scene = code_scene(ui, tmp_path)
    found = hard(scene_problems(ui, scene))
    assert found == [], [p.describe() for p in found]
    pane = scene.statement_pane
    assert pane.scrolls and pane.max_first > 0
    ui.focus = None                                   # PgDn reaches the statement once the editor lets go
    down = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_PAGEDOWN, mod=0, unicode="", scancode=0)
    frame(ui, lambda: scene.draw_ui(ui), [down])
    assert pane.first > 0
    pane.first = 10 ** 6                              # the very end: every row drawn whole
    found = hard(scene_problems(ui, scene))
    assert found == [], [p.describe() for p in found]


@pytest.mark.parametrize("scale", [2, 3])
def test_a_failing_run_with_a_long_traceback_stays_in_its_panel(scale, tmp_path):
    ui = make_ui(scale)
    scene = code_scene(ui, tmp_path)
    scene.result = failing_result(scene.problem)
    scene.outputs = ["9 9 9\n" * 3 + "x" * 200] * len(scene.problem["samples"])
    for detail in (False, True):
        scene.show_detail = detail
        found = hard(scene_problems(ui, scene))
        assert found == [], (detail, [p.describe() for p in found])
    scene.detail_pane.first = 10 ** 6
    found = hard(scene_problems(ui, scene))
    assert found == [], [p.describe() for p in found]
    shown = " ".join(r["text"] for r in scene.detail_pane.rows)
    assert "IndexError" in shown                       # the whole traceback is there to scroll to


def test_the_exercise_list_shows_long_titles_whole(tmp_path):
    from client.scenes.math_code import ProblemListScene
    ui = make_ui(2)
    scene = ProblemListScene(fake_game(ui, tmp_path), "s")
    title = "Nhân hai ma trận vuông cấp n rồi tính vết của tích, với các phần tử nguyên lớn"
    scene.data = {"floors": [{"floor": 3, "title_vi": "Ma trận và định thức",
                              "problems": [{"id": f"p{i}", "title_vi": title if i % 2 else "Cộng", "tier": 2,
                                            "tests": 12, "best": {"verdict": "WA", "passed": 3, "total": 12}}
                                           for i in range(14)]}]}
    rec = frame(ui, lambda: scene.draw_ui(ui))
    found = hard(audit.problems(rec, panel=(60, 18, 360, 230)))
    assert found == [], [p.describe() for p in found]
    words = " ".join(r["text"] for r in rec if r.get("kind") == "text")
    assert "lớn" in words and "..." not in words


def shots(outdir: Path) -> None:
    """Screenshots of the cases above."""
    import tempfile
    outdir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    for scale in (2, 3):
        ui = make_ui(scale)
        scene = code_scene(ui, tmp)
        scene.box.row, scene.box.col = 1, len(LONG) - 5
        frame(ui, lambda: scene.draw_ui(ui))
        frame(ui, lambda: scene.draw_ui(ui))
        pygame.image.save(ui.win, str(outdir / f"01_editor_long_line_x{scale}.png"))
        scene.statement_pane.first = 10 ** 6
        frame(ui, lambda: scene.draw_ui(ui))
        pygame.image.save(ui.win, str(outdir / f"02_statement_scrolled_x{scale}.png"))
        scene.statement_pane.first = 0
        scene.result = failing_result(scene.problem)
        scene.outputs = ["9 9 9\n" * 3] * len(scene.problem["samples"])
        frame(ui, lambda: scene.draw_ui(ui))
        pygame.image.save(ui.win, str(outdir / f"03_result_line_x{scale}.png"))
        scene.show_detail = True
        frame(ui, lambda: scene.draw_ui(ui))
        pygame.image.save(ui.win, str(outdir / f"04_detail_top_x{scale}.png"))
        scene.detail_pane.first = 10 ** 6
        frame(ui, lambda: scene.draw_ui(ui))
        pygame.image.save(ui.win, str(outdir / f"05_traceback_x{scale}.png"))
        print(scale, [p.describe() for p in hard(scene_problems(ui, scene))])


if __name__ == "__main__":
    shots(Path(sys.argv[1] if len(sys.argv) > 1 else "code_shots"))
