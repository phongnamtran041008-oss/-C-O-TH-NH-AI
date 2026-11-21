"""Tàng Thư Các read one page per micro-skill (client/scenes/math_library.DocScene).

The whole library is laid out and drawn headlessly, every page, at window scales 3 and 2,
with the self-check answers hidden and shown (tools/shot_library.py): nothing may leave the
content box, sit on something else, be wider than its column, or stick out of its figure.
The reader's own behaviour (turning pages, opening at a block, showing an answer, the
"Luyện ngay" button) is driven here with real key and mouse events, without a server.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pygame
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import shot_library  # noqa: E402

from app.learning import math_library  # noqa: E402  (shot_library put server/ on the path)
from client.scenes.math_library import DocScene  # noqa: E402


class Game(shot_library._Game):
    def __init__(self):
        super().__init__(math_library.documents())
        self.popped = []

    def pop(self, scene) -> None:
        self.popped.append(scene)


@pytest.fixture(scope="module")
def ui():
    return shot_library._ui(3)


def frame(ui, scene, *events) -> None:
    ui.begin(list(events), 1 / 60)
    ui.win.fill((0, 0, 0))
    scene.draw_ui(ui)
    ui.end()


def key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="", scancode=0)


def click(ui, x: float, y: float) -> pygame.event.Event:
    wx, wy = ui.d.to_window(x, y)
    return pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(int(wx) + 1, int(wy) + 1))


def test_every_page_of_every_document_fits():
    problems, pages = shot_library.check_documents()
    assert problems == [], "\n".join(problems[:40])
    assert pages >= sum(len(d.skills) for d in math_library.documents().values())


def test_one_page_per_micro_skill_and_the_arrows_turn_them(ui):
    game = Game()
    doc = math_library.documents()["gt_lib_t4"]
    scene = DocScene(game, doc.id)
    assert len(scene.pages) == len(doc.skills) and scene.page == 0
    frame(ui, scene)
    first = [it["text"] for it in scene.items if it["kind"] == "text"]
    frame(ui, scene, key(pygame.K_RIGHT))
    frame(ui, scene)
    assert scene.page == 1 and scene.current_section() == 1
    assert [it["text"] for it in scene.items if it["kind"] == "text"] != first
    frame(ui, scene, key(pygame.K_LEFT))
    frame(ui, scene, key(pygame.K_LEFT))                    # no page before the first
    assert scene.page == 0
    frame(ui, scene, key(pygame.K_END))
    assert scene.page == len(doc.skills) - 1
    frame(ui, scene, key(pygame.K_RIGHT))                   # nor after the last
    assert scene.page == len(doc.skills) - 1
    frame(ui, scene, key(pygame.K_HOME))
    assert scene.page == 0 and scene.scroll == 0


def test_page_down_reads_to_the_end_of_a_page_then_turns_it(ui):
    scene = DocScene(Game(), "dstt_lib_t3")
    frame(ui, scene)
    _, _, _, ch = scene.content_box()
    assert scene.total > ch, "this page is meant to be taller than the panel"
    seen = 0
    while scene.page == 0 and seen < 20:
        frame(ui, scene, key(pygame.K_PAGEDOWN))
        seen += 1
    assert scene.page == 1 and scene.scroll == 0 and seen >= 2
    frame(ui, scene, key(pygame.K_PAGEUP))                  # back to the end of the page before
    frame(ui, scene)
    assert scene.page == 0 and scene.at_bottom()


@pytest.mark.parametrize("doc_id", ["dstt_lib_t3", "gt_lib_t4", "xs_lib_t1", "tr_lib_t10"])
def test_opening_at_a_block_opens_its_page(doc_id):
    if doc_id not in math_library.documents():
        pytest.skip("no such document")
    doc = math_library.documents()[doc_id]
    for n, skill in enumerate(doc.skills):
        block = doc.section_of(skill)
        assert DocScene(Game(), doc_id, block).page == n
        assert DocScene(Game(), doc_id, block + 1).page == n       # a block inside the section too


def test_a_self_check_answer_shows_on_enter_or_on_a_click(ui):
    scene = DocScene(Game(), "gt_lib_t4")
    frame(ui, scene)
    checks = [it for it in scene.items if it.get("check") is not None]
    assert len(checks) == 1
    answer = scene.doc["blocks"][checks[0]["check"]]["answer"]
    assert not any(answer[:12] in it.get("text", "") for it in scene.items)
    frame(ui, scene, key(pygame.K_RETURN))
    frame(ui, scene)
    assert scene.revealed == {checks[0]["check"]}
    assert any(it.get("text", "").startswith("Đáp án") for it in scene.items)
    assert scene.page == 0                                   # Enter did not turn the page

    scene = DocScene(Game(), "gt_lib_t4")
    frame(ui, scene, key(pygame.K_END))
    frame(ui, scene)
    box = next(it for it in scene.items if it.get("check") is not None)
    cx, cy, _, ch = scene.content_box()
    top = cy + box["y"] - scene.scroll
    assert cy <= top + 4 <= cy + ch
    frame(ui, scene, click(ui, cx + box["x"] + 10, top + 4))
    assert scene.revealed == {box["check"]}


def test_the_last_page_offers_practice_when_the_caller_wants_it(ui):
    calls = []
    game = Game()
    scene = DocScene(game, "dstt_lib_t3", on_practice=lambda: calls.append("go"))
    frame(ui, scene)
    assert "doc_practice" not in ui.widgets                 # only on the last page
    frame(ui, scene, key(pygame.K_END))
    frame(ui, scene)
    assert "doc_practice" in ui.widgets
    r = ui.widgets["doc_practice"]
    frame(ui, scene, pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=r.center))
    assert calls == ["go"] and game.popped == [scene]

    plain = DocScene(Game(), "dstt_lib_t3")
    frame(ui, plain, key(pygame.K_END))
    frame(ui, plain)
    assert "doc_practice" not in ui.widgets


def test_an_old_document_still_reads_page_by_page(ui):
    old = [d for d in math_library.documents().values() if d.format == 1]
    if not old:
        pytest.skip("every document is a card now")
    scene = DocScene(Game(), old[0].id)
    frame(ui, scene)
    assert len(scene.pages) == len(old[0].skills)
    assert scene.layout_problems(ui) == []
    assert any(it["kind"] == "text" for it in scene.items)


def test_a_heading_inside_a_section_is_a_page_of_its_own(ui):
    """A `###` heading splits a micro-skill into short pages; the section stays the same one."""
    src = (ROOT / "server/data/math/library/giai_tich/t4_dao_ham.md").read_text("utf-8")
    marker = "Biết hệ số góc thì viết được tiếp tuyến"
    assert marker in src
    doc, problems = math_library.parse_document(src.replace(marker, "### Tiếp tuyến\n\n" + marker, 1))
    assert doc is not None and problems == [], problems
    game = Game()
    game.api.docs = {doc.id: doc}
    scene = DocScene(game, doc.id)
    assert len(scene.pages) == len(doc.skills) + 1
    assert scene.page_section[:3] == [0, 0, 1]
    frame(ui, scene)
    assert scene.part_of_section() == (1, 2)
    frame(ui, scene, key(pygame.K_RIGHT))
    frame(ui, scene)
    assert scene.page == 1 and scene.current_section() == 0 and scene.part_of_section() == (2, 2)
    assert any(it["kind"] == "text" and "Tiếp tuyến" in it["text"] for it in scene.items)
    assert scene.layout_problems(ui) == []
    # a question still opens the page of its micro-skill
    assert DocScene(game, doc.id, doc.section_of(doc.skills[1])).page == 2
