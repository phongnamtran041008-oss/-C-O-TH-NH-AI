"""The question card never cuts, covers or overflows a text (client/ui/audit.py records what it
draws). A fast, deterministic sample of the real bank - every question type, the longest
prompts, the longest options, the most solution steps, matching with a matrix, Thiên kiếp - in
both cards, before and after a wrong answer. The whole bank is checked by tools/audit_layout.py.
Also: the audit itself, the scrolling prompt, the combat card that waits to be read, and toasts
that keep off a card's text."""
import sys
from pathlib import Path

import pygame
import pytest

from client.tests.test_skill_fx import frame, make_game, make_ui
from client.ui import audit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "server"))


def sample_ids() -> list[str]:
    from app.learning import math_items
    items = sorted(math_items.bank().values(), key=lambda i: i.id)
    out: list[str] = []
    for qtype in sorted({i.qtype for i in items}):
        out += [i.id for i in items if i.qtype == qtype][:2]
    by = lambda key, n, pool=items: [i.id for i in sorted(pool, key=key, reverse=True)[:n]]
    out += by(lambda i: len(i.prompt_vi), 4)                                         # the longest prompts
    out += by(lambda i: max((len(o) for o in i.options_vi), default=0), 3)          # the longest options
    out += by(lambda i: (len(i.solution_vi), sum(map(len, i.solution_vi))), 3)      # the most steps
    out += by(lambda i: len(i.options_vi), 2)                                       # six options
    out += by(lambda i: len(i.pairs_vi), 2, [i for i in items if i.qtype == "matching" and i.matrices])
    out += by(lambda i: sum(len(p.prompt_vi) for p in i.parts) + len(i.prompt_vi), 2,
              [i for i in items if i.qtype == "tribulation"])
    out += by(lambda i: sum(map(len, i.lines_vi)), 2, [i for i in items if i.qtype == "find_mistake"])
    gens = sorted(math_items.generators())
    out += gens[::60]                                                               # a few generators
    return list(dict.fromkeys(out))


@pytest.fixture(scope="module")
def audit_layout():
    import audit_layout as AL
    return AL


@pytest.mark.parametrize("scale", [2, 3])
def test_a_sample_of_the_bank_fits_both_cards(audit_layout, scale):
    AL = audit_layout
    ids = set(sample_ids())
    found, _scrolls, n = AL.run([scale], 1, only=ids, write=False, quiet=True)
    assert n >= len(ids) - 2
    hard = [f"{cid} {kind}/{state}: {p.describe()}" for cid, kind, state, _s, p in found if p.kind in audit.HARD]
    assert not hard, "\n".join(hard[:20])


# ------------------------------------------------------------------ the audit itself
def test_the_audit_finds_overlaps_cuts_and_text_off_its_button():
    ui = make_ui()
    ui.audit = []
    ui.begin([], 0.016)
    ui.panel(20, 20, 200, 100)
    ui.text("Một dòng chữ dài", 30, 30, 9)
    ui.text("đè lên nó", 40, 32, 9)                                  # overlaps the line above
    ui.button("b1", 30, 60, 60, 16, "Nút")
    ui.text("chữ chạy qua mép nút", 70, 62, 8)                       # half on the button
    ui.text("ngoài khung", 210, 110, 9)                               # leaves the panel
    ui.push_clip(30, 90, 100, 6)
    ui.text("bị cắt bởi vùng cắt", 30, 88, 9)
    ui.pop_clip()
    ui.note_cut("một câu bị cắt…")
    kinds = audit.summary(audit.problems(ui.audit, panel=(20, 20, 200, 100)))
    ui.audit = None
    assert kinds.get("overlap") and kinds.get("over_button") and kinds.get("outside_panel")
    assert kinds.get("clipped") and kinds.get("cut")


def test_a_label_on_its_own_button_is_no_problem():
    ui = make_ui()
    ui.audit = []
    ui.begin([], 0.016)
    ui.button("ok", 100, 100, 80, 20, "Đồng ý")
    ui.button("blank", 100, 130, 200, 30, "")
    ui.text("chữ vẽ trên nút trống", 110, 140, 8)
    found = audit.problems(ui.audit)
    ui.audit = None
    assert found == []


# ------------------------------------------------------------------ the scrolling prompt
def long_question(inp="choice"):
    text = " ".join(["Một đề bài rất dài với x^2 + y_1 <= 10 và nhiều điều kiện phụ cần đọc kỹ."] * 9)
    return {"session_id": "s1", "time_limit": 60, "input": inp, "instruction_vi": "Chọn một đáp án đúng",
            "options": [{"id": c, "text": f"Đáp án {c} khá dài để xuống dòng " * 3} for c in "abcd"],
            "prompt": {"text": text},
            "math": {"subject_name_vi": "Giải Tích", "floor": 2, "skill_name_vi": "Giới hạn", "tier": 3,
                     "tier_name_vi": "Vận dụng", "mistake_vi": "Quên điều kiện.", "monster_vi": "Mặc Quái"}}


def test_a_prompt_too_long_for_the_combat_card_scrolls_and_never_covers_the_options():
    from client.scenes.math_practice import MathCombatQuizScene
    ui = make_ui()
    card = MathCombatQuizScene(make_game(ui), long_question(), "m1")
    ui.audit = []
    frame(ui, lambda: card.draw_ui(ui))
    found = audit.problems(ui.audit, panel=card.panel_rect())
    ui.audit = None
    assert card.prompt_scrolls and not found, [p.describe() for p in found]
    area = ui.rect(*card.panel_rect())
    assert all(area.contains(ui.widgets[f"opt_{c}"]) for c in "abcd")
    frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_DOWN, pygame.K_DOWN])
    assert card.prompt_scroll == 2


def test_the_reveal_shows_every_solution_step_by_scrolling():
    from client.scenes.math_practice import MathCombatQuizScene
    ui = make_ui()
    card = MathCombatQuizScene(make_game(ui), long_question(), "m1")
    steps = [f"Bước số {n}: biến đổi x^{n} theo quy tắc rồi rút gọn hai vế cho gọn." for n in range(1, 7)]
    card.sent, card.given = True, {"option": "a"}
    card.result = {"correct": False, "reveal": {"answer_text": "Đáp án b", "solution_vi": steps},
                   "combat": {"mac_kich": 9}}
    seen = set()
    for _ in range(40):
        drawn = []
        real = ui.text

        def text(*a, **k):
            drawn.append(a[0])
            return real(*a, **k)
        ui.text = text
        frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_DOWN])
        ui.text = type(ui).text.__get__(ui)
        seen |= {t for t in drawn}
    for n in range(1, 7):
        assert f"{n}." in seen                       # every step's number came into view
    assert card.reveal_scrolls


# ------------------------------------------------------------------ toasts keep off the card's text
def test_free_slot_keeps_off_the_text_of_a_panel_and_prefers_outside_it():
    ui = make_ui()
    ui.begin([], 0.016)
    ui.panel(24, 56, 432, 202)
    ui.text("Tiêu đề của thẻ câu hỏi", 36, 62, 7)
    ui.text("Một dòng đề bài ở giữa thẻ", 60, 120, 10)
    y = ui.free_slot(200, 14, 70)
    assert y is not None and y + 14 <= 56          # above the card, not on its header
    ui.begin([], 0.016)
    ui.panel(24, 18, 432, 246, "Tiêu đề")
    ui.text("chữ ở đầu khung", 36, 24, 7)
    y = ui.free_slot(200, 14, 4)
    assert y is not None and not any(y < my + mh and y + 14 > my and 140 < mx + mw and 340 > mx
                                     for mx, my, mw, mh in ui.obstacles())
