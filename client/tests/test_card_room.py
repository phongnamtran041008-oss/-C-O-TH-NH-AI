"""A low card (the one a monster, a Trận Nhãn or a fish opens) must leave its board enough room.

Found by the bí cảnh flow: "Cho ma trận A như hình. Ghép mỗi phần tử của A^T với giá trị của nó"
has a two-line statement, a matrix and five pairs. On the low card the five rows were crushed to
a few pixels each, slid under the Hoàn tác / Làm lại / Trả lời buttons, and the last pair could
not be clicked. The card now grows upwards when its board would not fit.
"""
import pytest

from client.scenes.math_practice import MathCombatQuizScene, MathQuizScene
from client.tests.test_skill_fx import frame, make_game, make_ui

LEFT = ["hàng 1, cột 2 của A^T", "hàng 2, cột 1 của A^T", "hàng 2, cột 2 của A^T",
        "hàng 3, cột 1 của A^T", "hàng 3, cột 2 của A^T"]
RIGHT = ["-3", "5", "8", "0", "2"]
STEPS = ["Viết lại hàng 1 của A thành cột 1", "Viết lại hàng 2 của A thành cột 2",
         "Đếm số hàng của kết quả", "Đếm số cột của kết quả", "So với cỡ của A"]


def question(inp: str, **math) -> dict:
    prompt = {"text": "Cho ma trận A như hình. Ghép mỗi phần tử của A^T với giá trị của nó (hàng trước, cột sau).",
              "matrices": [{"name": "A", "rows": [["1", "-3", "0"], ["2", "8", "5"]]}]}
    if inp == "matching":
        prompt.update(left=LEFT, right=RIGHT)
    elif inp == "ordering":
        prompt["steps"] = STEPS
    else:
        prompt["lines"] = STEPS
    return {"session_id": "s1", "context": "math_combat", "time_limit": 80, "input": inp, "options": None,
            "instruction_vi": "Ghép mỗi vế trái với một vế phải cho đúng", "prompt": prompt,
            "math": {"subject_name_vi": "Đại Số Tuyến Tính", "floor": 3, "skill_name_vi": "Ma trận chuyển vị A^T",
                     "tier": 2, "tier_name_vi": "Cơ bản", **math}}


def rows_and_buttons(ui, prefixes):
    rows = [r for wid, r in ui.widgets.items() if wid.startswith(prefixes)]
    buttons = [r for wid, r in ui.widgets.items() if wid.startswith("mq_")]
    return rows, buttons


@pytest.mark.parametrize("inp, prefixes, n", [("matching", ("match_l_", "match_r_"), 10),
                                              ("ordering", ("ord_step_",), 5),
                                              ("find_mistake", ("fm_line_",), 5)])
@pytest.mark.parametrize("mistake", ["", "Trận Nhãn: phá ấn bằng một câu ở tầng của con."])
def test_the_low_card_grows_until_every_row_is_readable_and_clear_of_the_buttons(inp, prefixes, n, mistake):
    ui = make_ui()
    card = MathCombatQuizScene(make_game(ui), question(inp, mistake_vi=mistake), "m1")
    frame(ui, lambda: card.draw_ui(ui))
    x, y, w, h = card.panel_rect()
    assert y < card.card_rect()[1]                      # it had to grow: the low card was too small
    assert y >= MathQuizScene.CARD_TOP and y + h == sum(card.card_rect()[1::2])   # upwards only, bottom edge fixed
    rows, buttons = rows_and_buttons(ui, prefixes)
    assert len(rows) == n and buttons
    area = ui.rect(x, y, w, h)
    for r in rows:
        assert area.contains(r), (r, area)
        assert r.height >= 12 * ui.s, r                 # a row a player can read and hit
    assert max(r.bottom for r in rows) <= min(b.top for b in buttons)


def test_a_card_that_already_fits_stays_where_it_is():
    ui = make_ui()
    q = question("matching")
    q["prompt"] = {"text": "Ghép mỗi khái niệm với mô tả của nó.", "left": LEFT[:3], "right": RIGHT[:3]}
    card = MathCombatQuizScene(make_game(ui), q, "m1")
    frame(ui, lambda: card.draw_ui(ui))
    assert card.panel_rect() == card.card_rect()
    for inp in ("truefalse", "choice", "number"):       # a card with no board never moves
        other = MathCombatQuizScene(make_game(ui), {**question("matching"), "input": inp}, "m1")
        assert other.panel_rect() == other.card_rect()


def test_the_full_card_never_moves_and_the_pairs_can_be_made_and_sent():
    ui = make_ui()
    game = make_game(ui)
    full = MathQuizScene(game, question("matching"))
    assert full.panel_rect() == full.card_rect()
    card = MathCombatQuizScene(game, question("matching"), "m1")
    draw = lambda: card.draw_ui(ui)
    frame(ui, draw)
    for k in range(5):                                  # the very clicks the flow test makes
        frame(ui, draw, click=f"match_l_{k}")
        frame(ui, draw, click=f"match_r_{k}")
    frame(ui, draw, click="mq_submit")
    assert game.api.posts and game.api.posts[-1][1]["answer"] == {"pairs": [0, 1, 2, 3, 4]}
