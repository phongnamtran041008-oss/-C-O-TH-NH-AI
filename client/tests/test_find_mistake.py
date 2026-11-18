"""M11, Tìm chỗ sai (find_mistake) on the client, with no server and no window: the state of the
input, the widget (mouse, number keys, Enter), long Vietnamese lines that must stay inside the
card, and the card that sends {"line": i} and shows the reveal. The real server and the real UI
together are in test_find_mistake_flow.py."""
import pygame
import pytest

from client.tests.test_skill_fx import LONG, frame, make_game, make_ui
from client.ui import mathinputs as MI

LINES = ["Đặt y = 2x + 1.",
         "Chuyển vế: 2x = y - 1.",
         "Chia cho 3: x = (y - 1)/3, vì hệ số của x là 3.",
         "Vậy g(x) = (x - 1)/3."]


# ------------------------------------------------------------------ the state
def test_the_state_picks_one_line_and_changing_the_choice_replaces_it():
    st = MI.FindMistakeState(4)
    assert not st.complete and st.sel is None
    st.click(2)
    assert st.complete and st.answer() == {"line": 2}
    st.click(0)                                       # another line: the choice changes, no second choice
    assert st.sel == 0 and st.answer() == {"line": 0}
    st.click(0)                                       # the same line again keeps it
    assert st.sel == 0
    for bad in (-1, 4, 99):
        st.click(bad)
    assert st.sel == 0
    st.undo()
    assert st.sel is None and not st.complete
    st.click(3)
    st.clear()
    assert st.sel is None


def test_the_answer_is_a_real_int_and_given_text_names_the_step():
    st = MI.FindMistakeState(3)
    st.click(1)
    assert type(st.answer()["line"]) is int
    assert MI.given_text("find_mistake", {"line": 1}) == "Bước 2"
    assert MI.given_text("find_mistake", {"timed_out": True}) == ""


# ------------------------------------------------------------------ the widget
def test_widget_mouse_choose_change_and_send():
    ui = make_ui()
    st = MI.FindMistakeState(4)
    draw = lambda: MI.draw_find_mistake(ui, st, LINES, 24, 60, 432, 250, False)
    frame(ui, draw)
    assert frame(ui, draw, click="mq_submit") is None                 # disabled until a line is chosen
    frame(ui, draw, click="fm_line_2")
    assert st.sel == 2
    frame(ui, draw, click="fm_line_1")                                # "press again to change"
    assert st.sel == 1
    assert frame(ui, draw, click="mq_submit") == {"line": 1}
    frame(ui, draw, click="mq_clear")
    assert st.sel is None


def test_widget_number_keys_enter_and_backspace():
    ui = make_ui()
    st = MI.FindMistakeState(4)

    def draw(sent=False):
        return MI.draw_find_mistake(ui, st, LINES, 24, 60, 432, 250, sent)

    frame(ui, draw)
    assert frame(ui, draw, keys=[pygame.K_RETURN]) is None            # nothing chosen: Enter does nothing
    frame(ui, draw, keys=[pygame.K_3])
    assert st.sel == 2
    frame(ui, draw, keys=[pygame.K_4])
    assert st.sel == 3
    frame(ui, draw, keys=[pygame.K_6])                                # no sixth line: ignored
    assert st.sel == 3
    frame(ui, draw, keys=[pygame.K_BACKSPACE])
    assert st.sel is None
    frame(ui, draw, keys=[pygame.K_1])
    assert frame(ui, draw, keys=[pygame.K_RETURN]) == {"line": 0}
    assert frame(ui, lambda: draw(sent=True), keys=[pygame.K_RETURN]) is None
    frame(ui, lambda: draw(sent=True), keys=[pygame.K_2])             # nothing changes after it was sent
    assert st.sel == 0


def test_a_number_key_pressed_on_the_card_does_not_reach_the_world_after_it():
    """1-6 also cast a chiêu in the world scene, which draws first with its input off while a card
    is on top; the card takes the key out of the frame, so nothing later can see it."""
    ui = make_ui()
    st = MI.FindMistakeState(4)
    frame(ui, lambda: MI.draw_find_mistake(ui, st, LINES, 24, 60, 432, 250, False))
    ui.begin([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2, mod=0, unicode="2", scancode=0)], 0.016)
    ui.enabled = False                                                # the world below, drawn first
    assert not ui.key(pygame.K_2)
    ui.enabled = True                                                 # the card on top
    MI.draw_find_mistake(ui, st, LINES, 24, 60, 432, 250, False)
    assert st.sel == 1
    assert not ui.key(pygame.K_2)                                     # the key is gone for anyone after it


@pytest.mark.parametrize("texts", [LONG[:6], LONG[:3], LINES, LINES[:3]])
def test_long_vietnamese_lines_stay_inside_the_card_and_clear_of_the_buttons(texts):
    ui = make_ui()
    x, y, w, bottom = 24, 62, 432, 186                       # the compact combat card leaves this much
    st = MI.FindMistakeState(len(texts))
    frame(ui, lambda: MI.draw_find_mistake(ui, st, texts, x, y, w, bottom, False))
    area = ui.rect(x, y, w, bottom - y)
    rows = [r for wid, r in ui.widgets.items() if wid.startswith("fm_line_")]
    assert len(rows) == len(texts)
    for r in rows:
        assert area.contains(r), (r, area)
    assert max(r.bottom for r in rows) <= min(r.top for wid, r in ui.widgets.items() if wid.startswith("mq_"))
    for a in rows:
        for b in rows:
            if a is not b:
                assert not a.colliderect(b), (a, b)


# ------------------------------------------------------------------ the card around it
def question(lines=LINES, **math) -> dict:
    return {"session_id": "s1", "context": "math_combat", "time_limit": 120, "input": "find_mistake", "options": None,
            "instruction_vi": "Tìm bước đầu tiên bị sai trong lời giải",
            "prompt": {"text": "Lời giải sau tìm hàm ngược của f(x) = 2x + 1. Bước đầu tiên bị sai là bước nào?",
                       "lines": list(lines)},
            "math": {"subject_name_vi": "Đại số", "floor": 3, "skill_name_vi": "Ma trận", "tier": 2,
                     "tier_name_vi": "Cơ bản", **math}}


def reveal(card, lines, wrong):
    card.result = {"correct": False,
                   "reveal": {"answer_text": f"Bước {wrong + 1}: {lines[wrong]}",
                              "solution_vi": ["Hệ số của x là 2 chứ không phải 3, nên phải chia cho 2.",
                                              "Đúng ra: x = (y - 1)/2."]},
                   "combat": {"cast": "x", "missed": True, "correct": False}}


@pytest.mark.parametrize("combat", [False, True])
def test_the_card_sends_the_line_and_the_reveal_names_the_wrong_step(combat):
    from client.scenes.math_practice import MathCombatQuizScene, MathQuizScene
    ui = make_ui()
    game = make_game(ui)
    q = question(mistake_vi="Mặc Quái nói: bước nào cũng đúng cả." if combat else "")
    card = MathCombatQuizScene(game, q, "m1") if combat else MathQuizScene(game, q)
    assert card.mistake is not None and card.match is None and card.ordering is None
    draw = lambda: card.draw_ui(ui)
    frame(ui, draw)
    rows = {w: r for w, r in ui.widgets.items() if w.startswith("fm_line_")}
    assert len(rows) == 4
    if combat:            # the mistake line along the bottom of the card stays clear of the board
        x, y, w, h = card.panel_rect()
        assert max(r.bottom for r in rows.values()) <= ui.rect(x, y, w, h - card.input_margin()).bottom
        assert card.input_margin() == 32
    frame(ui, draw, click="fm_line_2")
    frame(ui, draw, click="mq_submit")
    assert game.api.posts == [("/quiz/answer", {"session_id": "s1", "answer": {"line": 2}})]
    assert card.given == {"line": 2}
    reveal(card, LINES, 1)
    ui.begin([], 0.016)
    card.draw_ui(ui)                                    # the reveal after a wrong answer draws without raising
    assert card.given_text() == "Bước 3"


def test_the_card_with_six_very_long_lines_draws_and_sends_the_sixth():
    from client.scenes.math_practice import MathQuizScene
    ui = make_ui()
    game = make_game(ui)
    card = MathQuizScene(game, question(lines=[f"Bước tính thứ {n}: " + LONG[0] for n in range(1, 7)]))
    draw = lambda: card.draw_ui(ui)
    frame(ui, draw)
    x, y, w, h = card.panel_rect()
    for wid, r in ui.widgets.items():
        if wid.startswith(("fm_line_", "mq_")):
            assert ui.rect(x, y, w, h).contains(r), (wid, r)
    frame(ui, draw, keys=[pygame.K_6])
    frame(ui, draw, keys=[pygame.K_RETURN])
    assert game.api.posts[-1][1]["answer"] == {"line": 5}
