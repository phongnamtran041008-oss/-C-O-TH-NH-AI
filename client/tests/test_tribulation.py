"""M11 đợt 2, Thiên kiếp (tribulation) on the client, with no server and no window: the state of
the input (parts answered one at a time, kept until the end), the widget (mouse, keys, moving
between parts), the card that sends {"parts": [...]}, and long Vietnamese parts and solutions
that must stay inside the card. The real server and the real UI together are in
test_tribulation_flow.py."""
import pygame
import pytest

from client.tests.test_skill_fx import LONG, frame, make_game, make_ui
from client.ui import mathinputs as MI

PARTS = [
    {"text": "a) Sau hai bước khử, phương trình cuối có dạng (m - k)*z = 0. Tìm k.", "input": "number",
     "options": None},
    {"text": "b) Với m = 2, hệ có bao nhiêu nghiệm?", "input": "choice",
     "options": [{"id": "a", "text": "Đúng một nghiệm"}, {"id": "b", "text": "Vô nghiệm"},
                 {"id": "c", "text": "Vô số nghiệm"}]},
    {"text": "c) Có ít nhất một giá trị thực của m làm hệ vô nghiệm.", "input": "truefalse", "options": None},
]
SITUATION = ("Cho hệ có tham số m: (1) x + 2y - z = 1, (2) 2x + 5y + z = 4, (3) x + 3y + mz = 3. "
             "Con khử x khỏi (2) và (3), rồi khử y khỏi phương trình cuối.")
KEYS = [{"numbers": ["2"], "unordered": False, "tolerance": 1e-06}, {"option": "c"}, {"value": False}]
MATRIX = [{"name": "A", "rows": [["1", "1", "1", "6"], ["2", "3", "1", "11"], ["1", "-1", "2", "5"]]}]


def typed(ui, text: str) -> None:
    """Type into the focused box over one frame (TEXTINPUT events, as SDL sends them)."""
    ui.begin([pygame.event.Event(pygame.TEXTINPUT, text=c) for c in text], 0.016)


# ------------------------------------------------------------------ the state
def test_the_state_keeps_each_part_and_is_complete_only_with_every_part():
    st = MI.TribulationState(PARTS)
    assert st.n == 3 and st.cur == 0 and st.input == "number" and not st.complete
    st.set_text(0, "  2 ")
    assert st.answered(0) and st.answers[0] == {"text": "2"}
    st.next()
    st.choose("c")
    st.choose(True)                                   # a bool is not an option id: ignored on a choice part
    assert st.answers[1] == {"option": "c"}
    st.next()
    st.choose(False)
    st.choose("a")                                    # an option id means nothing on a true/false part
    assert st.answers[2] == {"value": False} and st.complete
    st.next()                                         # past the last part: stays
    assert st.cur == 2
    st.go(1)
    st.choose("a")                                    # going back and changing an answer
    assert st.answer() == {"parts": [{"text": "2"}, {"option": "a"}, {"value": False}]}
    st.set_text(0, "   ")                             # emptying a box takes that part's answer away
    assert not st.answered(0) and not st.complete
    st.set_text(1, "5")                               # a box only exists on a number part
    assert st.answers[1] == {"option": "a"}
    st.prev(), st.prev(), st.prev()
    assert st.cur == 0


def test_part_right_follows_the_server_rules():
    assert MI.part_right({"value": True}, {"value": True}) and not MI.part_right({"value": True}, {"value": 1})
    assert MI.part_right({"option": "b"}, {"option": "b"}) and not MI.part_right({"option": "b"}, {"option": "a"})
    key = {"numbers": ["-3", "2", "0"], "unordered": False, "tolerance": 1e-06}
    assert MI.part_right(key, {"text": "-3, 2, 0"}) and MI.part_right(key, {"text": "-6/2; 2.0; 0"})
    assert not MI.part_right(key, {"text": "2, -3, 0"}) and not MI.part_right(key, {"text": "-3, 2"})
    assert MI.part_right({**key, "unordered": True}, {"text": "0, 2, -3"})
    rounded = {"numbers": ["247/20"], "unordered": False, "tolerance": 0.005}
    assert MI.part_right(rounded, {"text": "12.35"}) and MI.part_right(rounded, {"text": "12.354"})
    assert not MI.part_right(rounded, {"text": "12.36"}) and not MI.part_right(rounded, {"text": "12,35"})
    for bad in (None, {}, {"text": 5}, {"text": "x"}, {"text": "1/0"}, []):
        assert not MI.part_right(key, bad)


# ------------------------------------------------------------------ the widget
def board(ui, st, sent=False, prompt=None, box=(24, 48, 432, 242)):
    x, y, w, bottom = box
    return MI.draw_tribulation(ui, st, prompt or {"text": SITUATION, "parts": PARTS}, x, y, w, bottom, sent)


def test_widget_mouse_answers_each_part_and_sends_them_together():
    ui = make_ui()
    st = MI.TribulationState(PARTS)
    draw = lambda: board(ui, st)
    frame(ui, draw)
    assert "trib_text_0" in ui.widgets and ui.focus == "trib_text_0"     # a number part has its box, focused
    assert not ui.widgets.get("trib_prev") is None
    typed(ui, "2")
    draw()
    assert st.answers[0] == {"text": "2"}
    frame(ui, draw, click="trib_next")
    frame(ui, draw)
    assert st.cur == 1 and ui.focus is None and "trib_opt_c" in ui.widgets
    assert frame(ui, draw, click="mq_submit") is None                    # not every part answered yet
    frame(ui, draw, click="trib_opt_c")
    frame(ui, draw, click="trib_part_2")                                 # the tab of part c
    frame(ui, draw)
    assert st.cur == 2 and "trib_true" in ui.widgets
    frame(ui, draw, click="trib_false")
    assert st.complete
    frame(ui, draw, click="trib_part_0")                                 # back to part a: its text is kept
    frame(ui, draw)
    assert ui.value("trib_text_0") == "2" and st.answers[0] == {"text": "2"}
    assert frame(ui, draw, click="mq_submit") == {"parts": [{"text": "2"}, {"option": "c"}, {"value": False}]}


def test_widget_keys_move_choose_and_enter_sends_only_from_the_last_part():
    ui = make_ui()
    st = MI.TribulationState(PARTS)
    draw = lambda sent=False: board(ui, st, sent)
    frame(ui, draw)
    typed(ui, "3/2")
    draw()
    frame(ui, draw, keys=[pygame.K_RETURN])                              # Enter: on to the next part
    assert st.cur == 1
    frame(ui, draw, keys=[pygame.K_3])
    assert st.answers[1] == {"option": "c"}
    frame(ui, draw, keys=[pygame.K_2])                                   # another key changes the choice
    assert st.answers[1] == {"option": "b"}
    frame(ui, draw, keys=[pygame.K_RIGHT])
    assert st.cur == 2
    assert frame(ui, draw, keys=[pygame.K_RETURN]) is None               # part c has no answer yet
    frame(ui, draw, keys=[pygame.K_1])
    assert st.answers[2] == {"value": True}
    frame(ui, draw, keys=[pygame.K_LEFT])
    assert st.cur == 1
    frame(ui, draw, keys=[pygame.K_RETURN])                              # not the last part: Enter moves on
    assert st.cur == 2
    assert frame(ui, draw, keys=[pygame.K_RETURN]) == {"parts": [{"text": "3/2"}, {"option": "b"}, {"value": True}]}
    assert frame(ui, lambda: draw(True), keys=[pygame.K_RETURN, pygame.K_LEFT, pygame.K_2]) is None
    assert st.cur == 2 and st.answers[2] == {"value": True}             # nothing moves after it was sent


def collect(ui):
    """Every rect ui.text draws from now on (base units)."""
    rects = []
    real = ui.text

    def text(*a, **k):
        r = real(*a, **k)
        rects.append((a[0], r))
        return r
    ui.text = text
    return rects


LONG_PARTS = [{"text": "a) " + LONG[0], "input": "number", "options": None},
              {"text": "b) " + LONG[0], "input": "choice",
               "options": [{"id": i, "text": LONG[0][:90 + 7 * n]} for n, i in enumerate("abcd")]},
              {"text": "c) " + LONG[0], "input": "truefalse", "options": None},
              {"text": "d) " + LONG[0], "input": "choice",
               "options": [{"id": "a", "text": "Có"}, {"id": "b", "text": "Không"}]}]


@pytest.mark.parametrize("matrices", [None, MATRIX])
@pytest.mark.parametrize("box", [(24, 48, 432, 242), (24, 105, 432, 226)])     # the practice card / a combat card
def test_long_parts_and_situations_stay_inside_their_rectangle(matrices, box):
    ui = make_ui()
    x, y, w, bottom = box
    prompt = {"text": " ".join(LONG[:3]), "parts": LONG_PARTS, **({"matrices": matrices} if matrices else {})}
    st = MI.TribulationState(LONG_PARTS)
    area = ui.rect(x, y, w, bottom - y)
    for k in range(4):
        st.go(k)
        frame(ui, lambda: board(ui, st, prompt=prompt, box=box))
        rects = collect(ui)
        frame(ui, lambda: board(ui, st, prompt=prompt, box=box))
        ui.text = type(ui).text.__get__(ui)
        widgets = {wid: r for wid, r in ui.widgets.items() if wid.startswith(("trib_", "mq_"))}
        for wid, r in widgets.items():
            assert area.contains(r), (k, wid, r, area)
        for txt, r in rects:
            assert area.contains(ui.rect(r.x, r.y, r.w - 1, r.h - 1)), (k, txt[:30], r)
        nav = min(r.top for wid, r in widgets.items() if wid in ("trib_prev", "trib_next", "mq_submit"))
        body = [r for wid, r in widgets.items() if wid.startswith(("trib_opt_", "trib_true", "trib_false", "trib_text_"))]
        assert body and max(r.bottom for r in body) <= nav, k
        for a in body:
            for b in body:
                assert a is b or not a.colliderect(b), (a, b)


def test_a_long_situation_scrolls_with_the_wheel_and_the_arrow_keys():
    ui = make_ui()
    st = MI.TribulationState(PARTS)
    prompt = {"text": " ".join(LONG), "parts": PARTS}
    draw = lambda: board(ui, st, prompt=prompt, box=(24, 105, 432, 226))
    frame(ui, draw)
    assert st.scroll == 0
    frame(ui, draw, keys=[pygame.K_DOWN, pygame.K_DOWN])
    assert st.scroll == 2
    ui.begin([pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=1, flipped=False)], 0.016)
    draw()
    assert st.scroll == 1
    for _ in range(80):
        frame(ui, draw, keys=[pygame.K_DOWN])
    end = st.scroll
    frame(ui, draw, keys=[pygame.K_DOWN])
    assert st.scroll == end > 1                                          # it stops at the last line
    frame(ui, draw, keys=[pygame.K_UP])
    assert st.scroll == end - 1


# ------------------------------------------------------------------ the card around it
def question(parts=PARTS, matrices=None, **math) -> dict:
    prompt = {"text": SITUATION, "parts": parts, **({"matrices": matrices} if matrices else {})}
    return {"session_id": "s1", "context": "math_practice", "time_limit": 480, "input": "tribulation",
            "options": None, "qtype": "tribulation",
            "instruction_vi": "Thiên kiếp: trả lời đúng mọi phần của bài tổng hợp", "prompt": prompt,
            "math": {"subject_name_vi": "Đại Số Tuyến Tính", "floor": 5, "skill_name_vi": "Biện luận số nghiệm",
                     "tier": 4, "tier_name_vi": "Nâng cao", **math}}


SOLUTION = ["a) (2) - 2*(1): y + 3z = 2. (3) - (1): y + (m + 1)z = 2. Trừ hai phương trình này: (m - 2)z = 0, "
            "nên k = 2."] + [f"Bước {n}: " + LONG[0] for n in range(1, 7)]


def reveal(card, correct=False, timed_out=False):
    card.result = {"correct": correct, "timed_out": timed_out,
                   "reveal": {"answer_text": "a) 2; b) Vô số nghiệm; c) Sai", "solution_vi": SOLUTION,
                              "parts": [{"answer_text": "2", "key": KEYS[0]},
                                        {"answer_text": "Vô số nghiệm", "key": KEYS[1]},
                                        {"answer_text": "Sai", "key": KEYS[2]}]}}


def answer_all(ui, card, wrong_b=False):
    draw = lambda: card.draw_ui(ui)
    frame(ui, draw)
    typed(ui, "2")
    draw()
    frame(ui, draw, click="trib_next")
    frame(ui, draw)
    frame(ui, draw, click="trib_opt_a" if wrong_b else "trib_opt_c")
    frame(ui, draw, click="trib_next")
    frame(ui, draw)
    frame(ui, draw, click="trib_false")
    frame(ui, draw, click="mq_submit")


@pytest.mark.parametrize("combat", [False, True])
def test_the_card_sends_every_part_at_once_and_the_reveal_marks_each_part(combat):
    from client.scenes.math_practice import MathCombatQuizScene, MathQuizScene
    ui = make_ui()
    game = make_game(ui)
    q = question(matrices=MATRIX, mistake_vi="Mặc Quái nói: hệ nào cũng có nghiệm duy nhất." if combat else "")
    card = MathCombatQuizScene(game, q, "m1") if combat else MathQuizScene(game, q)
    assert card.trib is not None and card.mistake is None
    answer_all(ui, card, wrong_b=True)
    sent = {"parts": [{"text": "2"}, {"option": "a"}, {"value": False}]}
    assert game.api.posts == [("/quiz/answer", {"session_id": "s1", "answer": sent})]
    assert card.given == sent
    if combat:            # the board stays above the monster's mistake line
        x, y, w, h = card.panel_rect()
        assert card.input_margin() == 32
    rows = MI.tribulation_reveal_rows(q["prompt"]["parts"], {**{"parts": [{"answer_text": "2", "key": KEYS[0]},
                                                                       {"answer_text": "Vô số nghiệm", "key": KEYS[1]},
                                                                       {"answer_text": "Sai", "key": KEYS[2]}]},
                                                               "solution_vi": ["x"]}, sent, False, False)
    texts = [t for t, _, _ in rows]
    assert texts[0] == "a) Đúng: 2" and texts[1] == "b) Sai. Đáp án: Vô số nghiệm"
    assert texts[2] == "con trả lời: Đúng một nghiệm" and texts[3] == "c) Đúng: Sai"
    assert texts[4] == "Lời giải từng bước" and texts[5] == "1. x"
    reveal(card)
    x, y, w, h = card.panel_rect()
    for _ in range(3):
        rects = collect(ui)
        frame(ui, lambda: card.draw_ui(ui))
        ui.text = type(ui).text.__get__(ui)
        steps = [r for t, r in rects if t.startswith(("a) ", "b) ", "c) ", "con trả", "Lời giải", "1. ", "2. ", "Bước"))]
        assert steps
        bottom = ui.rect(x, y, w, h - card.solution_margin + 12).bottom
        assert max(r.bottom for r in steps) <= bottom + 1                   # the long solution stops above the buttons
        for wid in ("math_next",):
            if wid in ui.widgets:
                assert max(r.bottom for r in steps) <= ui.widgets[wid].top + ui.s
    first = card.reveal_scroll
    frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_DOWN, pygame.K_DOWN])
    assert card.reveal_scroll == first + 2                                  # the reveal scrolls


def test_a_right_answer_shows_every_part_right_and_no_solution():
    from client.scenes.math_practice import MathQuizScene
    ui = make_ui()
    game = make_game(ui)
    card = MathQuizScene(game, question())
    answer_all(ui, card)
    assert game.api.posts[-1][1]["answer"] == {"parts": [{"text": "2"}, {"option": "c"}, {"value": False}]}
    reveal(card, correct=True)
    rects = collect(ui)
    frame(ui, lambda: card.draw_ui(ui))
    ui.text = type(ui).text.__get__(ui)
    shown = [t for t, _ in rects]
    assert "a) Đúng: 2" in shown and "c) Đúng: Sai" in shown and "Lời giải từng bước" not in shown


def test_a_timeout_reveal_says_which_parts_had_no_answer():
    rows = MI.tribulation_reveal_rows(PARTS, {"parts": [{"answer_text": "2", "key": KEYS[0]},
                                                        {"answer_text": "Vô số nghiệm", "key": KEYS[1]},
                                                        {"answer_text": "Sai", "key": KEYS[2]}],
                                              "solution_vi": []}, {"timed_out": True}, False, True)
    assert [t for t, _, _ in rows] == ["a) Chưa trả lời. Đáp án: 2", "b) Chưa trả lời. Đáp án: Vô số nghiệm",
                                       "c) Chưa trả lời. Đáp án: Sai"]


# ------------------------------------------------------------------ the combat card of a missed Thiên kiếp
def test_a_missed_thien_kiep_stays_up_long_enough_to_read_and_closes_on_enter():
    """An ordinary combat card closes itself after two seconds; the reveal of a Thiên kiếp (which
    part went wrong, a long solution) needs longer, and the player can close it when done."""
    from pathlib import Path

    from client.scenes import math_practice as mp
    assert mp.TRIBULATION_REVEAL_SECONDS >= 15
    src = (Path(mp.__file__)).read_text("utf-8")
    block = src[src.index("class MathCombatQuizScene"):src.index("# M10: (widget id, label, module, scene class)")]
    assert 'self.q.get("input") == "tribulation"' in block and "TRIBULATION_REVEAL_SECONDS" in block
    assert "ui.key(pygame.K_RETURN) or ui.key(pygame.K_ESCAPE)" in block and "self.finish()" in block
