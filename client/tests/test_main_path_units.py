"""Chính đạo, the main quest, in the client: the helpers that turn GET /math/tree `main` into the
hub card, the HUD box and the board entry (client/scenes/math_tree.py, client/scenes/guide.py),
and the card itself drawn by the real UI with no server: the one button and its label, Enter,
nothing cut, nothing outside the panel, also for a long stage with a long name.

`python -m client.tests.test_main_path_units <folder>` also saves PNGs of the drawn card."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pygame

from client import strings_vi as T
from client.engine.display import Display
from client.engine.text import Fonts
from client.scenes import guide as G
from client.scenes import math_tree as MT
from client.scenes.math_practice import MathPracticeScene
from client.ui.kit import UI

STAGE_1 = [("ds_a", "Tập hợp và ánh xạ"), ("tr_a", "Logic mệnh đề và quy tắc đếm"), ("lt_a", "Python nhập môn"),
           ("gt_a", "Hàm số, hàm hợp, mũ và logarit"), ("xs_a", "Sự kiện và phép đếm")]


def main(step="hoc", node="ds_a", name="Tập hợp và ánh xạ", index=1, states=None, **more):
    names = dict(STAGE_1)
    states = states or ["now"] + ["later"] * 4
    out = {"node_id": node, "path": index - 1, "name_vi": name, "why_vi": "Mọi mô hình là một ánh xạ.",
           "branch": "ds", "branch_vi": "Đại Số Tuyến Tính", "kind": "toan", "realm": "luyen_khi",
           "realm_name_vi": "Luyện Khí", "stage": 1, "index": index, "total": 5, "step": step,
           "done": {"hieu": step != "hoc", "luyen": step == "kiep", "kiep": False},
           "part": {"subject_id": "s", "floor": 1, "index": 1, "count": 1},
           "gate": {"done": 2, "total": 4, "ok": step == "kiep"}, "doc_id": "doc1", "block": 3,
           "subject_id": "s", "floor": 1, "problems": [], "problems_done": 0, "problems_total": 0, "resume": None,
           "stage_nodes": [{"id": i, "name_vi": names[i], "branch": i[:2], "branch_vi": "", "kind": "toan",
                            "state": s} for (i, _), s in zip(STAGE_1, states)],
           "path_done": 0, "path_total": 58}
    out.update(more)
    return out


def tree_with(m, nodes=None):
    nodes = nodes if nodes is not None else [
        {"id": i, "branch": i[:2], "realm": "luyen_khi", "stage": 1, "status": "chinh", "kind": "toan",
         "name_vi": n, "why_vi": "", "topics_vi": [], "state": "open", "requires": [], "reinforces": [],
         "parts": [], "problems": [], "source": None, "path": k} for k, (i, n) in enumerate(STAGE_1)]
    return {"wired": True, "stage": {"realm": "luyen_khi", "realm_name_vi": "Luyện Khí", "stage": 0, "stages": 9},
            "branches": [{"id": "ds", "name_vi": "Đại Số Tuyến Tính", "subject": None}],
            "nodes": nodes, "next": [], "main": m, "run": None}


# ------------------------------------------------------------------ the pure helpers
def test_the_button_label_follows_the_step():
    assert [MT.main_label(main(s)) for s in ("hoc", "luyen", "kiep", "code")] == \
        ["Học bài", "Luyện", "Độ Thiên kiếp nhỏ", "Làm bài tập"]
    assert MT.main_label(main("luyen", resume="practice")) == "Luyện tiếp"
    assert MT.main_label(main("kiep", resume="trial")) == "Độ kiếp tiếp"


def test_the_chips_show_which_steps_are_done():
    assert MT.main_chips(main("hoc")) == [("Hiểu", "now"), ("Luyện", "later"), ("Vượt cổng", "later")]
    assert MT.main_chips(main("luyen")) == [("Hiểu", "done"), ("Luyện", "now"), ("Vượt cổng", "later")]
    assert MT.main_chips(main("kiep")) == [("Hiểu", "done"), ("Luyện", "done"), ("Vượt cổng", "now")]
    code = main("code", problems_done=2, problems_total=5)
    assert MT.main_chips(code) == [("Bài tập 2/5", "now")]


def test_progress_and_the_hud_line():
    assert MT.main_progress(main("hoc")) == ""
    assert MT.main_progress(main("luyen")) == "Cổng 2/4"
    two = main("luyen", part={"subject_id": "s", "floor": 2, "index": 1, "count": 2})
    assert MT.main_progress(two) == "Phần 1/2 · Cổng 2/4"
    assert MT.main_step_line(main("luyen")) == "Luyện · Cổng 2/4"
    assert MT.main_step_line(main("hoc")) == "Học bài"
    assert MT.main_step_line(main("code", problems_done=1, problems_total=3)) == "Làm bài tập 1/3"
    assert MT.main_head(main()) == "Chính đạo · Luyện Khí tầng 1 · nút 1/5"


def test_nodes_ahead_on_the_path_are_marked_later():
    t = tree_with(main(index=2, node="tr_a"))
    t["nodes"][0]["state"] = "done"
    assert MT.later_ids(t) == {"lt_a", "gt_a", "xs_a"}
    t["nodes"][3]["state"] = "done"                       # done ahead of the path: nothing to mark
    assert MT.later_ids(t) == {"lt_a", "xs_a"}
    assert MT.later_ids(tree_with(main("done", node=None, path=None))) == set()
    assert MT.later_ids({"nodes": []}) == set() and MT.main_step({"nodes": []}) is None


def test_the_hub_opens_on_the_main_tab_unless_a_sitting_waits_elsewhere():
    t = tree_with(main())
    t["branches"] = [{"id": "ds", "name_vi": "Đại Số", "subject": None}, {"id": "gt", "name_vi": "GT", "subject": None}]
    assert MT.first_tab(t) == "next"
    t["run"] = {"node_id": "ds_a"}
    assert MT.first_tab(t) == "next"                      # the sitting is the current step: the card resumes it
    t["run"] = {"node_id": "gt_a"}
    assert MT.first_tab(t) == "gt"


def guide_view(lead="main", m=None, claimable=0):
    return {"chapters": [{"id": "c1", "title_vi": "Nhập Môn", "intro_vi": "", "state": "active", "done": 0,
                          "total": 1, "rewards_vi": [], "steps": []}],
            "current": {"chapter_id": "c1", "step_id": "g_x", "title_vi": "Mở Đạo Thụ", "hint_vi": "Bấm M",
                        "progress": 0, "count": 1, "goto": "math"},
            "claimable": claimable, "study": None, "lead": lead, "main": m if m is not None else main("luyen")}


def test_the_hud_box_leads_with_the_main_step_once_the_welcome_is_done():
    box = G.tracker_model(guide_view())
    assert box["main"] and box["header"] == "Chính đạo 1/5 · F1"
    assert box["title"] == "Tập hợp và ánh xạ" and box["hint"] == "Luyện · Cổng 2/4" and box["claim"] == ""
    assert G.tracker_model(guide_view(claimable=2))["claim"] == "Nhận 2"
    old = G.tracker_model(guide_view(lead="steps"))
    assert not old["main"] and old["title"] == "Mở Đạo Thụ"
    done = G.tracker_model(guide_view(m=main("done")))
    assert done["body"] == T.PATH_DONE_TITLE


def test_the_board_opens_on_chinh_dao_and_shows_the_same_step():
    assert G.default_selection(guide_view()) == (G.MAIN, G.MAIN)
    assert G.default_selection(guide_view(lead="steps")) == ("c1", "g_x")
    d = G.main_detail(guide_view())
    assert d["title"] == "Tập hợp và ánh xạ" and d["step"] == "Luyện" and d["goto"]
    assert d["stage"].startswith("Luyện Khí tầng 1: nút 1/5")
    assert G.main_detail({"main": None}) is None


# ------------------------------------------------------------------ the card, drawn
def make_ui() -> UI:
    return UI(Display(0, False, size=(960, 540)), Fonts())


def hub_for(m, nodes=None) -> MathPracticeScene:
    game = SimpleNamespace(api=None, push=lambda s: None, game=None)
    hub = MathPracticeScene(game)
    hub.tree, hub.path = tree_with(m, nodes), {"subjects": []}
    hub.tabs, hub.tab = MT.tab_list(hub.tree), "next"
    return hub


def draw(ui: UI, hub: MathPracticeScene, keys=(), click: str | None = None) -> list[tuple[str, pygame.Rect]]:
    """One frame of the hub; returns every text drawn with its rect."""
    events = [pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="", scancode=0) for k in keys]
    if click:
        events.append(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=ui.widgets[click].center))
    ui.begin(events, 0.016)
    seen: list[tuple[str, pygame.Rect]] = []
    real = ui.text

    def spy(txt, *a, **k):
        r = real(txt, *a, **k)
        seen.append((txt, r))
        return r
    ui.text = spy
    try:
        hub.draw_ui(ui)
    finally:
        del ui.text
    return seen


def inside(seen, x0=40, y0=16, x1=440, y1=254):
    for txt, r in seen:
        assert x0 <= r.x and r.right <= x1 + 1 and y0 - 12 <= r.y and r.bottom <= y1 + 1, (txt, r)


def test_the_card_has_one_primary_button_that_enter_presses():
    ui, hub = make_ui(), hub_for(main("luyen"))
    done = []
    hub.do_main = lambda m=None: done.append(m["step"])
    seen = draw(ui, hub)
    texts = [t for t, _ in seen]
    assert "math_main_go" in ui.widgets and "math_main_read" in ui.widgets and "math_main_info" in ui.widgets
    assert "Tập hợp và ánh xạ" in texts and "Luyện" in texts and "Cổng 2/4" in texts
    assert T.PATH_LIST.format(n=1) in texts and texts.count(T.PATH_STATE["later"]) == 4
    assert all(f"math_path_{i}" in ui.widgets for i, _ in STAGE_1)
    assert not any(w.startswith("math_node_") for w in ui.widgets)      # no row of five buttons any more
    inside(seen)
    draw(ui, hub, keys=[pygame.K_RETURN])
    assert done == ["luyen"]
    draw(ui, hub)
    draw(ui, hub, click="math_main_go")
    assert done == ["luyen", "luyen"]


def test_a_lesson_step_has_no_second_read_button():
    ui, hub = make_ui(), hub_for(main("hoc"))
    draw(ui, hub)
    assert "math_main_go" in ui.widgets and "math_main_read" not in ui.widgets


def test_side_modes_are_drawn_small_under_luyen_them():
    ui, hub = make_ui(), hub_for(main())
    texts = [t for t, _ in draw(ui, hub)]
    assert T.PATH_SIDE in texts
    go, door = ui.widgets["math_main_go"], ui.widgets["math_hub_dungeon"]
    assert door.height < go.height and door.width < go.width


LONG = [("ds_k", "Không gian vectơ: bao tuyến tính, cơ sở, số chiều"), ("gt_k", "Kỳ vọng, phương sai và các phân phối quen thuộc"),
        ("lt_k", "Đo độ phức tạp, tìm kiếm và sắp xếp"), ("ud_k", "Khớp đường thẳng bằng hạ gradient"),
        ("ud_l", "Lọc thư rác bằng Bayes"), ("tr_k", "Tìm kiếm theo chiều rộng và chiều sâu"),
        ("ds_l", "Định thức, hạng và nghịch đảo"), ("gt_l", "Khai triển Taylor"), ("xs_k", "Biến ngẫu nhiên rời rạc")]
WHY = ("Mọi thư viện học sâu nghĩ theo kiểu NumPy: một dòng cho cả bảng số liệu, không vòng lặp. Game chạy bằng "
       "Python thuần, không cài NumPy, nên bạn tự viết bằng danh sách đúng những việc NumPy làm giùm: hình dạng, "
       "phát sóng, tổng theo trục, X @ w + b, X.T @ X.")


def long_stage():
    m = main("luyen", node="ds_k", name=LONG[0][1] + " và những điều khác nữa", why_vi=WHY, index=1, stage=5)
    m["total"] = len(LONG)
    m["stage_nodes"] = [{"id": i, "name_vi": n, "branch": i[:2], "branch_vi": "", "kind": "toan",
                         "state": "now" if k == 0 else "later"} for k, (i, n) in enumerate(LONG)]
    return m


def test_a_long_stage_with_a_long_name_and_why_fits_and_cuts_no_name():
    ui, hub = make_ui(), hub_for(long_stage())
    seen = draw(ui, hub)
    inside(seen)
    texts = [t.replace("\n", " ") for t, _ in seen]
    for _, name in LONG:
        assert name in texts, name                          # whole, never "..."
    assert not any(t.endswith("...") for t in texts)
    go = ui.widgets["math_main_go"]
    rows = [ui.widgets[f"math_path_{i}"] for i, _ in LONG]
    assert go.bottom <= rows[0].top and rows[-1].bottom <= ui.widgets["math_library"].top


def test_the_end_of_the_path_says_so():
    ui, hub = make_ui(), hub_for(main("done", node=None, name=None, stage_nodes=[]))
    texts = [t for t, _ in draw(ui, hub)]
    assert T.PATH_DONE_TITLE in texts and "math_main_go" not in ui.widgets


def save_shots(out: Path) -> None:
    """The card at the start, mid-stage at the gate, and a long stage - for a person to look at."""
    out.mkdir(parents=True, exist_ok=True)
    cases = {"card_start": main("hoc"),
             "card_gate_open": main("kiep", node="tr_a", name=STAGE_1[1][1], index=2,
                                    states=["done", "now", "done", "later", "later"]),
             "card_code": main("code", node="lt_a", name="Python nhập môn", index=3, problems_done=2, problems_total=5,
                               states=["done", "done", "now", "later", "later"], part=None, gate=None),
             "card_long_stage": long_stage()}
    for name, m in cases.items():
        ui, hub = make_ui(), hub_for(m)
        draw(ui, hub)
        draw(ui, hub)
        pygame.image.save(ui.win, str(out / f"{name}.png"))


if __name__ == "__main__":
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((480, 270))
    save_shots(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "main_path")
