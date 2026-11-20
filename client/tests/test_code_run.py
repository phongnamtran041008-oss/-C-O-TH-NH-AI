"""M6: running the learner's own program, and the little code editor.

No server and no window here: this is the part of the game that takes a .py file, feeds it
a test on stdin and reports what happened (client/engine/coderun.py), plus the text editing
of client/ui/codebox.py.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from client.engine import coderun  # noqa: E402
from client.ui.codebox import CodeBox  # noqa: E402

ECHO = "import sys\nprint(sum(int(x) for x in sys.stdin.read().split()))\n"
CRASH = "raise IndexError('hong roi')\n"
FOREVER = "while True:\n    pass\n"
BROKEN = "def f(:\n    pass\n"


@pytest.fixture
def workdir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


def write(workdir: Path, code: str) -> Path:
    return coderun.write_solution(workdir / "bai_lam.py", code)


# ------------------------------------------------------------------ the compile check
def test_code_that_does_not_compile_is_caught_without_running_it():
    assert coderun.compile_problem(ECHO) == ""
    problem = coderun.compile_problem(BROKEN)
    assert "SyntaxError" in problem and "dòng 1" in problem


def test_the_compile_check_runs_nothing(workdir):
    """Compiling must not execute the module: a file that would delete something is safe."""
    flag = workdir / "touched.txt"
    assert coderun.compile_problem(f"open(r'{flag}', 'w').write('x')\n") == ""
    assert not flag.exists()


# ------------------------------------------------------------------ one run
def test_a_program_gets_the_test_on_stdin_and_its_output_comes_back(workdir):
    path = write(workdir, ECHO)
    result = coderun.run_one(path, "1 2 3\n")
    assert result.ok and result.output.split() == ["6"]
    assert result.ms >= 0


def test_a_program_that_crashes_is_re_with_the_last_lines_of_the_error(workdir):
    result = coderun.run_one(write(workdir, CRASH), "\n")
    assert result.status == coderun.RE and "IndexError" in result.error


# ------------------------------------------------------------------ Xạ Trường: the training log
TRAIN = ("import sys\n"
         "for i in range(5):\n"
         "    print('#loss', i, 10 / (i + 1), file=sys.stderr)\n"
         "    print('#val', i, 12 / (i + 1), file=sys.stderr)\n"
         "print('ghi chu khac', file=sys.stderr)\n"
         "print(1)\n")


def test_the_loss_lines_on_stderr_become_the_training_log():
    log = coderun.parse_log("#loss 0 2.5\nnoise\n#loss 1 1.25\n#val 1 1.5\n#loss x 3\n#lossy 1 2\n#loss 2 nan\n")
    assert log["loss"] == [(0.0, 2.5), (1.0, 1.25), (2.0, float("inf"))]     # a blown-up loss is kept as inf
    assert log["val"] == [(1.0, 1.5)]
    assert coderun.parse_log("") == {"loss": [], "val": []}


def test_a_very_long_log_is_thinned_but_keeps_its_ends():
    log = coderun.parse_log("".join(f"#loss {i} {1 / (i + 1)}\n" for i in range(5000)))["loss"]
    assert len(log) == coderun.MAX_LOG_POINTS and log[0] == (0.0, 1.0) and log[-1][0] == 4999.0


def test_a_run_brings_its_log_back_and_its_output_stays_clean(workdir):
    result = coderun.run_one(write(workdir, TRAIN), "")
    assert result.ok and result.output.split() == ["1"]
    assert [v for _, v in result.log["loss"]] == [10.0, 5.0, 10 / 3, 2.5, 2.0] and len(result.log["val"]) == 5


def test_the_error_text_of_a_crash_leaves_the_log_out(workdir):
    result = coderun.run_one(write(workdir, TRAIN + "raise ValueError('nan roi')\n"), "")
    assert result.status == coderun.RE and "ValueError" in result.error and "#loss" not in result.error
    assert len(result.log["loss"]) == 5


def test_an_attempt_shows_the_longest_log(workdir):
    path = write(workdir, "import sys\nn = int(input())\nfor i in range(n):\n    print('#loss', i, 1, file=sys.stderr)\n")
    attempt = coderun.run_tests(path, ["2\n", "6\n", "3\n"])
    run, log = attempt.log
    assert run == 2 and len(log["loss"]) == 6
    assert coderun.run_tests(path, ["0\n"]).log == (0, {})


def test_the_web_build_path_reads_the_same_log():
    result = coderun.run_in_process(TRAIN, "")
    assert result.ok and result.output.split() == ["1"] and len(result.log["loss"]) == 5


def test_a_program_that_never_stops_is_tle(workdir):
    result = coderun.run_one(write(workdir, FOREVER), "\n", time_limit_ms=300)
    assert result.status == coderun.TLE and result.ms == 300


def test_a_flood_of_output_is_cut_short(workdir):
    path = write(workdir, "print('x' * 100000)\n")
    result = coderun.run_one(path, "\n", max_output_chars=100)
    assert result.ok and len(result.output) == 100


def test_the_run_does_not_see_the_game_s_environment(workdir):
    """-I and a cleaned environment: a run is the same on every machine."""
    path = write(workdir, "import os, sys\nprint(len([k for k in os.environ if k.startswith('PYTHON')]))\n"
                          "print(int(sys.flags.isolated))\n")
    result = coderun.run_one(path, "\n")
    assert result.ok and result.output.split() == ["0", "1"]


def test_a_program_may_print_vietnamese_whatever_the_code_page_is(workdir):
    """-X utf8, because -I makes the interpreter ignore PYTHONIOENCODING."""
    result = coderun.run_one(write(workdir, "print('Tầng Thư, điểm số: 10')\n"), "\n")
    assert result.ok and result.output.strip() == "Tầng Thư, điểm số: 10"


# ------------------------------------------------------------------ a whole attempt
def test_every_test_runs_and_the_answers_come_back_in_order(workdir):
    attempt = coderun.run_tests(write(workdir, ECHO), ["1 1\n", "2 2\n", "3 3\n"])
    assert attempt.status == coderun.OK
    assert [o.split() for o in attempt.outputs] == [["2"], ["4"], ["6"]]
    assert len(attempt.times_ms) == 3


def test_an_attempt_stops_at_the_first_test_that_breaks(workdir):
    code = "import sys\nn = int(sys.stdin.read())\nprint(1 // n)\n"
    attempt = coderun.run_tests(write(workdir, code), ["1\n", "0\n", "1\n"])
    assert attempt.status == coderun.RE
    assert len(attempt.outputs) == 2 and "ZeroDivisionError" in attempt.error


def test_an_attempt_that_does_not_compile_never_runs_a_test(workdir):
    attempt = coderun.run_tests(write(workdir, BROKEN), ["1\n", "2\n"])
    assert attempt.status == coderun.CE and attempt.outputs == [] and "SyntaxError" in attempt.error


def test_the_solution_file_is_written_where_the_player_can_open_it(workdir):
    path = coderun.write_solution(workdir / "bai_lam" / "x.py", "print(1)\n")
    assert path.is_file() and path.read_text("utf-8") == "print(1)\n"
    assert "\r" not in path.read_bytes().decode()


def test_without_a_python_interpreter_the_game_says_so(monkeypatch):
    monkeypatch.setattr(coderun.sys, "frozen", True, raising=False)
    monkeypatch.setattr(coderun.shutil, "which", lambda name: None)
    with pytest.raises(coderun.NoPython):
        coderun.interpreter()


def test_a_python_named_in_the_config_is_used(monkeypatch):
    monkeypatch.setattr(coderun.shutil, "which", lambda name: "/usr/bin/python9" if name == "python9" else None)
    assert coderun.interpreter("python9") == "/usr/bin/python9"
    with pytest.raises(coderun.NoPython):
        coderun.interpreter("khong-co-dau")


# ------------------------------------------------------------------ the editor
def test_typing_inserts_at_the_caret():
    box = CodeBox("ab")
    box.col = 1
    box.insert("X")
    assert box.text == "aXb" and box.col == 2


def test_enter_keeps_the_python_indent():
    box = CodeBox("    print(1)")
    box.col = len(box.lines[0])
    box.insert("\n")
    assert box.lines == ["    print(1)", "    "] and (box.row, box.col) == (1, 4)


def test_enter_in_the_middle_of_a_line_carries_the_rest_down():
    box = CodeBox("abcd")
    box.col = 2
    box.insert("\n")
    assert box.lines == ["ab", "cd"] and (box.row, box.col) == (1, 0)


def test_backspace_eats_a_whole_indent_but_one_letter_otherwise():
    box = CodeBox("        x")
    box.col = 8
    box.backspace()
    assert box.lines == ["    x"] and box.col == 4
    box = CodeBox("abc")
    box.col = 3
    box.backspace()
    assert box.lines == ["ab"]


def test_backspace_at_the_start_of_a_line_joins_it_to_the_one_above():
    box = CodeBox("ab\ncd")
    box.row, box.col = 1, 0
    box.backspace()
    assert box.text == "abcd" and (box.row, box.col) == (0, 2)


def test_delete_takes_the_character_after_the_caret():
    box = CodeBox("abc")
    box.col = 1
    box.delete()
    assert box.text == "ac"
    box = CodeBox("ab\ncd")
    box.col = 2
    box.delete()
    assert box.text == "abcd"


def test_the_editor_never_grows_past_its_limit():
    box = CodeBox("", max_chars=5)
    box.insert("123456789")
    assert len(box.text) == 5


def test_text_set_from_a_file_with_windows_line_ends_is_read_as_lines():
    box = CodeBox("a\r\nb\r\nc")
    assert box.lines == ["a", "b", "c"] and box.text == "a\nb\nc"
