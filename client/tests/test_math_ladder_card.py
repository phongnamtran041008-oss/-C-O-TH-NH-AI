"""M11 đợt 2, rule 8 on the math card: a rung says which step of the ladder it is, a tier-5
miss that opens a ladder says so, and the summary of a sitting counts the ladders climbed.
(The server side is server/tests/test_math_ladder.py.)"""
from __future__ import annotations

from client import strings_vi as T
from client.scenes.math_practice import MathQuizScene

RUN = {"mode": "practice", "combo": 0, "correct": 3, "asked": 5}


def card(q_math: dict, result: dict | None = None) -> MathQuizScene:
    scene = object.__new__(MathQuizScene)          # (no game needed for the run line)
    scene.q = {"math": q_math}
    scene.result = result
    return scene


def test_a_rung_shows_its_step_in_the_run_line():
    line = card({"ladder": {"of": "x", "step": 2, "steps": 3}}).run_line(RUN, answered=False)
    assert line.startswith("Bậc thang 2/3 dẫn tới câu vừa sai")
    assert T.MATH_SCORE.format(c=3, a=5) in line


def test_a_tier5_miss_announces_the_ladder_and_an_ordinary_card_says_nothing():
    res = {"math": {"ladder": {"of": "x", "step": 0, "steps": 3, "started": True}}}
    assert card({}, res).run_line(RUN, answered=True).startswith(T.MATH_LADDER_OPENED.format(t=3))
    assert "Bậc thang" not in card({}, {"math": {}}).run_line(RUN, answered=True)
    assert "Bậc thang" not in card({}).run_line(RUN, answered=False)


def test_the_summary_string_counts_ladders():
    assert T.MATH_LADDER_COUNT.format(n=2) == "Bậc thang đã leo: 2"
