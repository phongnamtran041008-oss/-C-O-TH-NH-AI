"""The pure logic of the Lộ Trình board (client/scenes/guide.py), on plain dicts: no server, no window."""
from __future__ import annotations

from client import strings_vi as T
from client.scenes import guide as G


def step(sid, state="active", progress=0, count=1, optional=False, nodes=None, goto="math", help_="dao_thu",
         chapter="c1"):
    return {"id": sid, "chapter_id": chapter, "title_vi": "Bước " + sid, "desc_vi": "Mô tả", "how_vi": ["Làm thế này"],
            "goto": goto, "help": help_, "optional": optional, "state": state, "progress": progress, "count": count,
            "rewards_vi": ["10 Linh Thạch"], "nodes": nodes or []}


def chapter(cid, steps, state="active", rewards=("50 Linh Thạch",)):
    req = [s for s in steps if not s["optional"]]
    return {"id": cid, "title_vi": "Chương " + cid, "intro_vi": "Giới thiệu", "state": state,
            "done": sum(s["state"] != "active" for s in req), "total": len(req), "rewards_vi": list(rewards),
            "steps": steps}


def view(chapters, current=None, claimable=0, study=None):
    return {"title_vi": "Lộ Trình", "welcome": {"seen": True, "speaker_vi": "Trúc Lão", "lines_vi": ["a"]},
            "chapters": chapters, "current": current, "claimable": claimable, "study": study, "stage": None,
            "handbook": []}


def cur(chapter_id, step_id, progress=0, count=1, hint="Bấm M"):
    return {"chapter_id": chapter_id, "step_id": step_id, "title_vi": "Bước " + step_id, "hint_vi": hint,
            "progress": progress, "count": count, "goto": "math"}


# ------------------------------------------------------------------ selection
def test_board_opens_on_the_current_step():
    c1 = chapter("c1", [step("a", "claimed"), step("b", "claimed")], "claimed")
    c2 = chapter("c2", [step("c", "claimed"), step("d")])
    v = view([c1, c2], current=cur("c2", "d"))
    assert G.default_selection(v) == ("c2", "d")


def test_with_no_current_step_the_first_chapter_with_something_to_do_is_chosen():
    c1 = chapter("c1", [step("a", "claimed")], "claimed")
    c2 = chapter("c2", [step("b", "done"), step("c", "claimed")], "done")
    assert G.default_selection(view([c1, c2])) == ("c2", "b")
    c3 = chapter("c3", [step("x", "claimed")], "claimed")
    assert G.default_selection(view([c1, c3])) == ("c1", "a")          # all claimed: the first chapter


def test_picking_a_chapter_prefers_required_active_then_claimable_then_bonus_then_optional():
    assert G.chapter_pick(chapter("c", [step("o", optional=True), step("r")]), None) == "r"
    assert G.chapter_pick(chapter("c", [step("a", "claimed"), step("d", "done")]), None) == "d"
    assert G.chapter_pick(chapter("c", [step("a", "claimed")], "done"), None) == G.BONUS
    assert G.chapter_pick(chapter("c", [step("a", "claimed"), step("o", optional=True)], "active"), None) == "o"
    assert G.chapter_pick(chapter("c", [step("a", "claimed")], "claimed"), None) == "a"
    # the current step wins when it lives in this chapter
    assert G.chapter_pick(chapter("c", [step("r"), step("s")]), cur("c", "s")) == "s"


def test_rows_are_the_steps_and_then_the_bonus_when_there_is_one():
    assert G.list_items(chapter("c", [step("a"), step("b")])) == ["a", "b", G.BONUS]
    assert G.list_items(chapter("c", [step("a")], rewards=())) == ["a"]


def test_gold_mark_when_something_inside_is_claimable():
    assert G.chapter_claimable(chapter("c", [step("a", "done"), step("b")]))
    assert G.chapter_claimable(chapter("c", [step("a", "claimed")], "done"))
    assert not G.chapter_claimable(chapter("c", [step("a", "claimed"), step("b")]))


# ------------------------------------------------------------------ row labels
def test_row_labels_for_each_state():
    assert G.row_parts(step("a", progress=2, count=5)) == ("Bước a", "", "2/5")
    assert G.row_parts(step("a", "done", 5, 5))[2] == T.GUIDE_MARK_CLAIM == "Nhận"
    assert G.row_parts(step("a", "claimed", 5, 5))[2] == T.GUIDE_MARK_DONE == "Xong"
    assert G.row_parts(step("a", optional=True))[1] == "(tuỳ chọn)"
    ch = chapter("c", [step("a", "claimed"), step("b")])
    assert G.bonus_mark(ch) == "1/2"
    assert G.bonus_mark({**ch, "state": "done"}) == "Nhận" and G.bonus_mark({**ch, "state": "claimed"}) == "Xong"


# ------------------------------------------------------------------ detail
def nodes(*pairs):
    return [{"id": f"n{i}", "name_vi": name, "branch": "ds", "branch_vi": "Đại Số", "state": st}
            for i, (name, st) in enumerate(pairs)]


def test_remaining_line_lists_nodes_not_done_and_skips_vacant():
    s = step("c4_s1", nodes=nodes(("Tập hợp", "open"), ("Hàm số", "done"), ("Lập trình", "vacant"),
                                  ("Logic", "locked")))
    assert G.remaining_line(s) == "Còn: Tập hợp, Logic"
    assert G.remaining_line(step("x")) == ""
    assert G.remaining_line(step("y", nodes=nodes(("A", "done"), ("B", "vacant")))) == ""


def test_detail_of_a_step_and_of_the_bonus():
    ch = chapter("c", [step("a", "done", 1, 1), step("b", goto="nowhere", help_=None)], "active")
    d = G.detail_of(ch, "a")
    assert d["claim"] == "a" and d["goto"] == "math" and d["help"] == "dao_thu" and d["title"] == "Bước a"
    d = G.detail_of(ch, "b")
    assert d["claim"] is None and d["goto"] is None and d["help"] is None      # an unknown goto has no button
    done = {**ch, "state": "done"}
    b = G.detail_of(done, G.BONUS)
    assert b["claim"] == "c" and b["title"] == "Thưởng chương" and (b["progress"], b["count"]) == (1, 2)
    assert G.detail_of(ch, G.BONUS)["claim"] is None
    assert G.detail_of(ch, "missing") is None


def test_steps_that_became_done_are_reported_but_never_on_the_first_load():
    old = view([chapter("c", [step("a"), step("b", "done"), step("c")])])
    new = view([chapter("c", [step("a", "done"), step("b", "claimed"), step("c")])])
    assert G.newly_done(old, new) == ["Bước a"]
    assert G.newly_done(None, new) == []
    assert G.newly_done(new, new) == []


# ------------------------------------------------------------------ the HUD box
def test_tracker_shows_the_current_step_with_progress_only_when_there_is_more_than_one():
    c = chapter("c1", [step("a", progress=2, count=5)])
    m = G.tracker_model(view([c], current=cur("c1", "a", 2, 5, "Bấm M ở Động Phủ")))
    assert m["header"] == "Việc tiếp theo · F1" and m["title"] == "Bước a" and m["count"] == "2/5"
    assert m["hint"] == "Bấm M ở Động Phủ" and m["body"] == ""
    assert G.tracker_model(view([c], current=cur("c1", "a")))["count"] == ""


def test_tracker_header_asks_to_claim_when_something_waits():
    c = chapter("c1", [step("a")])
    m = G.tracker_model(view([c], current=cur("c1", "a"), claimable=3))
    assert m["header"] == "Nhận thưởng (3) · F1" and m["title"] == "Bước a"


def test_tracker_without_a_current_step_shows_the_study_line_or_all_done():
    study = {"action": "practice", "node_id": "n", "name_vi": "N", "branch_vi": "B", "floor": 1,
             "text_vi": "Học nút «N»: luyện cho tới khi mở Thiên kiếp nhỏ"}
    m = G.tracker_model(view([], study=study))
    assert m["body"] == study["text_vi"] and m["header"] == "Đang học · F1" and m["title"] == ""
    m = G.tracker_model(view([]))
    assert m["body"] == T.GUIDE_HUD_ALL_DONE and m["header"] == "Việc tiếp theo · F1"
    assert G.tracker_model(view([], study=study, claimable=1))["header"] == "Nhận thưởng (1) · F1"


def test_stage_line():
    assert G.stage_line({"realm_name_vi": "Luyện Khí", "stage": 2, "stages": 9}) == "Luyện Khí tầng 2/9"
    assert G.stage_line({"realm_name_vi": "Luyện Khí", "stage": 0, "stages": 9}) == "Luyện Khí tầng 0/9"
    assert G.stage_line(None) == ""
