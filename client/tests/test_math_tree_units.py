"""The pure helpers of the Đạo Thụ hub (client/scenes/math_tree.py): tabs, rows, their order,
the shortened names, the reason a node is locked, the lines of a node card and the guard in
front of the system browser. No server, no window: a tree view written out by hand."""
from __future__ import annotations

from client import strings_vi as T
from client.scenes import math_tree as MT


class FakeUi:
    """Every character is 4 units wide, so a width means a number of characters."""

    def text_size(self, text, size=8, kind="ui"):
        return len(text) * 4.0, 8.0


def part(floor, passed=False, tier=(1, 2), gate=None):
    return {"subject_id": "s", "floor": floor, "questions": 10, "tier_min": tier[0], "tier_max": tier[1],
            "passed": passed, "open": not passed, "gate": gate, "trial_total": 6, "doc_id": f"doc{floor}",
            "skills": [{"id": f"k{floor}", "name_vi": f"Kỹ năng {floor}"}]}


def node(nid, branch, stage, state="open", status="chinh", parts=(), requires=(), realm="luyen_khi", **extra):
    return {"id": nid, "branch": branch, "realm": realm, "stage": stage, "status": status, "kind": "toan",
            "name_vi": extra.pop("name_vi", nid), "why_vi": "", "topics_vi": [], "state": state,
            "state_vi": None, "requires": list(requires), "reinforces": [], "parts": list(parts),
            "problems": [], "source": None, **extra}


def sample_tree():
    nodes = [
        node("ds_a", "ds", 1, parts=[part(1)]),
        node("gt_a", "gt", 1, parts=[part(1)]),
        node("lt_a", "lt", 1, state="vacant"),
        node("ds_b", "ds", 2, state="locked", parts=[part(3)],
             requires=[{"id": "ds_a", "name_vi": "Tập hợp", "done": False}]),
        node("gt_b", "gt", 2, state="locked", parts=[part(2), part(3)],
             requires=[{"id": "gt_a", "name_vi": "Hàm số", "done": True},
                       {"id": "ds_a", "name_vi": "Tập hợp", "done": False}]),
        node("ds_opt", "ds", None, state="open", status="phu", parts=[part(2)]),
        node("ds_c", "ds", 3, state="locked", parts=[part(4)]),
        node("tc_x", "ml", 1, state="vacant", realm="truc_co"),
    ]
    # the server lists the optional node before a later main node: sorting must not trust that
    nodes[5], nodes[6] = nodes[6], nodes[5]
    return {"wired": True,
            "stage": {"realm": "luyen_khi", "realm_name_vi": "Luyện Khí", "stage": 2, "stages": 9},
            "branches": [{"id": "ds", "name_vi": "Đại Số Tuyến Tính", "subject": "dai_so"},
                         {"id": "gt", "name_vi": "Giải Tích", "subject": "giai_tich"},
                         {"id": "lt", "name_vi": "Lập Trình", "subject": None},
                         {"id": "ml", "name_vi": "Học Máy", "subject": None}],
            "nodes": nodes, "next": ["gt_a", "ds_a"], "run": None}


def test_tabs_are_next_then_the_branches_of_the_current_realm():
    tabs = MT.tab_list(sample_tree())
    assert [t["id"] for t in tabs] == ["next", "ds", "gt", "lt"]          # "ml" has nothing in Luyện Khí
    assert [t["name_vi"] for t in tabs] == ["Chính đạo", "Đại Số", "Giải Tích", "Lập Trình"]
    assert [t["subject"] for t in tabs] == [None, "dai_so", "giai_tich", None]


def test_the_realm_decides_which_branches_have_a_tab():
    tree = sample_tree()
    tree["stage"] = {"realm": "truc_co", "realm_name_vi": "Trúc Cơ", "stage": 1, "stages": 3}
    assert [t["id"] for t in MT.tab_list(tree)] == ["next", "ml"]


def test_next_tab_keeps_the_order_the_server_gave():
    rows = MT.node_rows(sample_tree(), "next")
    assert [r.node["id"] for r in rows] == ["gt_a", "ds_a"]


def test_branch_rows_sort_by_stage_with_optional_nodes_last_and_one_row_per_part():
    rows = MT.node_rows(sample_tree(), "ds")
    assert [(r.node["id"], r.part["floor"]) for r in rows] == [("ds_a", 1), ("ds_b", 3), ("ds_c", 4), ("ds_opt", 2)]
    two = MT.node_rows(sample_tree(), "gt")
    assert [(r.node["id"], r.index, r.count, r.first) for r in two] == [
        ("gt_a", 1, 1, True), ("gt_b", 1, 2, True), ("gt_b", 2, 2, False)]


def test_a_node_without_parts_has_one_row_and_other_realms_are_left_out():
    rows = MT.node_rows(sample_tree(), "lt")
    assert len(rows) == 1 and rows[0].part is None and MT.row_state(rows[0]) == "vacant"
    assert MT.node_rows(sample_tree(), "ml") == []                        # truc_co is not the realm of the player


def test_row_state_and_what_may_be_played():
    rows = {(r.node["id"], r.index): r for t in ("ds", "gt", "lt") for r in MT.node_rows(sample_tree(), t)}
    assert MT.row_state(rows["ds_a", 1]) == "part" and MT.part_playable(rows["ds_a", 1])
    assert MT.row_state(rows["ds_b", 1]) == "locked" and not MT.part_playable(rows["ds_b", 1])
    assert not MT.part_playable(MT.Row(rows["ds_a", 1].node, None, 1, 1, True))
    done = node("d", "ds", 1, state="done", parts=[part(1, passed=True)])
    assert MT.part_playable(MT.rows_of(done)[0])
    code_only = node("c", "lt", 2, state="open")
    assert MT.row_state(MT.rows_of(code_only)[0]) == "code"
    passed_in_open_node = node("o", "ds", 1, state="open", parts=[part(1, passed=True), part(2)])
    assert all(MT.part_playable(r) for r in MT.rows_of(passed_in_open_node))


def test_locked_reason_names_the_first_unfinished_requirement():
    n = sample_tree()["nodes"]
    gt_b = next(x for x in n if x["id"] == "gt_b")
    assert MT.locked_reason(gt_b) == "Cần xong: Tập hợp"               # "Hàm số" is done, so it is skipped
    assert MT.locked_reason(node("x", "ds", 1, state="locked")) == T.MATH_LOCKED


def test_stage_header_and_row_stage():
    stage = sample_tree()["stage"]
    assert MT.header_text(stage) == "Luyện Khí tầng 2/9"
    assert MT.header_text({**stage, "stage": 0}) == "Luyện Khí: chưa qua tầng nào"
    assert MT.stage_text(node("a", "ds", 4)) == "Tầng 4"
    assert MT.stage_text(node("a", "ds", None, status="phu")) == "Bàng môn"


def test_the_stage_progress_line_and_its_shorter_form():
    ui = FakeUi()
    stage = {**sample_tree()["stage"], "progress": {"stage": 3, "done": 1, "total": 4}}
    assert MT.progress_text(ui, stage, 400) == "đã xong 1/4 nút của tầng 3"
    short = MT.progress_text(ui, stage, 4 * len("xong 1/4 nút tầng 3") + 1)         # the long form does not fit
    assert short == "xong 1/4 nút tầng 3"
    assert MT.progress_text(ui, stage, 10) == ""                                   # neither fits: say nothing
    assert MT.progress_text(ui, {**stage, "progress": None}, 400) == ""            # the last stage is reached
    assert MT.progress_text(ui, sample_tree()["stage"], 400) == ""                 # an older server sent none


def test_the_exercise_button_needs_exercises_in_a_node_that_is_not_locked():
    problems = [{"id": "p1", "title_vi": "Đếm", "solved": False, "subject_id": "dai_so_tuyen_tinh"},
                {"id": "p2", "title_vi": "Chuyển vị", "solved": True, "subject_id": "dai_so_tuyen_tinh"}]
    assert MT.exercises_open(node("a", "lt", 2, state="open", problems=problems))
    assert MT.exercises_open(node("a", "lt", 2, state="done", problems=problems))
    assert not MT.exercises_open(node("a", "lt", 2, state="locked", problems=problems))
    assert not MT.exercises_open(node("a", "ds", 1, state="open"))                  # no exercises, no button
    assert MT.exercises_subject(node("a", "lt", 2, problems=problems)) == "dai_so_tuyen_tinh"
    assert MT.exercises_subject(node("a", "ds", 1)) is None


def test_a_review_question_names_the_node_it_comes_from():
    from client.scenes.math_practice import review_badge
    assert review_badge({"floor": 1, "review": True, "review_node_vi": "Xác suất cơ bản"}) == "Ôn lại: Xác suất cơ bản"
    assert review_badge({"floor": 2, "review": True}) == "Ôn xoắn ốc: tầng 2"     # a sitting from before Đạo Thụ


def test_names_are_cut_to_fit_and_a_second_part_keeps_its_tail():
    ui = FakeUi()
    short = MT.rows_of(node("a", "ds", 1, name_vi="Tập hợp", parts=[part(1)]))[0]
    assert MT.row_label(ui, short, 100) == "Tập hợp"
    long = MT.rows_of(node("a", "ds", 1, name_vi="Hàm số, hàm hợp, mũ và logarit", parts=[part(1)]))[0]
    label = MT.row_label(ui, long, 60)                                    # 15 characters
    assert label.endswith("...") and ui.text_size(label)[0] <= 60
    two = MT.rows_of(node("a", "gt", 2, name_vi="Giới hạn và liên tục", parts=[part(2), part(3)]))
    labels = [MT.row_label(ui, r, 60) for r in two]
    assert labels[0].endswith(" (1/2)") and labels[1].endswith(" (2/2)")
    assert all(ui.text_size(x)[0] <= 60 for x in labels)


def test_break_long_cuts_a_url_into_lines_that_fit():
    ui = FakeUi()
    url = "https://example.org/" + "a" * 60
    pieces = MT.break_long(ui, url, 8, 80)
    assert "".join(pieces) == url and all(ui.text_size(p)[0] <= 80 for p in pieces) and len(pieces) > 1


def test_first_tab_follows_the_sitting_left_open():
    tree = sample_tree()
    assert MT.first_tab(tree) == "next"
    tree["run"] = {"run_id": 1, "node_id": "gt_a", "floor": 1}
    assert MT.first_tab(tree) == "gt"
    tree["run"] = {"run_id": 1, "node_id": "no_such_node", "floor": 1}
    assert MT.first_tab(tree) == "next"


def test_names_of_skips_unknown_ids():
    assert MT.names_of(sample_tree(), ["ds_b", "nope", "gt_a"]) == ["ds_b", "gt_a"]
    assert MT.names_of(None, ["ds_b"]) == []


def test_card_blocks_say_why_source_requirements_reviews_topics_and_exercises():
    n = node("ds_b", "ds", 2, name_vi="Vectơ và ma trận", state="locked", parts=[part(3)],
             requires=[{"id": "ds_a", "name_vi": "Tập hợp", "done": True},
                       {"id": "gt_a", "name_vi": "Hàm số", "done": False}],
             reinforces=["ds_a"], why_vi="Vì ma trận là ngôn ngữ của dữ liệu.", topics_vi=["Vectơ", "Ma trận"],
             problems=[{"id": "p1", "title_vi": "Đếm phần tử", "solved": True},
                       {"id": "p2", "title_vi": "Chuyển vị", "solved": False}],
             source={"title": "Essence of linear algebra", "author": "3Blue1Brown", "url": "https://x.org/v",
                     "where": "Chương 1-3", "lang": "en", "kind": "video"})
    blocks = MT.card_blocks(n, lambda i: {"ds_a": "Tập hợp"}[i])
    kinds = [k for k, _ in blocks]
    heads = [t for k, t in blocks if k == "h"]
    assert heads == [T.NODE_SOURCE, T.NODE_REQUIRES, T.NODE_REINFORCES, T.NODE_TOPICS, T.NODE_PROBLEMS]
    text = "\n".join(t for _, t in blocks)
    assert "Vì ma trận" in text and "3Blue1Brown" in text and "Chương 1-3" in text
    assert "tiếng Anh · video" in text and "https://x.org/v" in text and "u" in kinds
    assert "Tập hợp - đã xong" in text and "Hàm số - chưa xong" in text
    assert "Đếm phần tử - đã giải" in text and "Chuyển vị - chưa giải" in text
    assert ("b", "Tập hợp") in blocks                                     # what it reviews, by name


def test_card_blocks_without_source_requirements_or_topics():
    n = node("a", "ds", 1, parts=[part(1)])
    blocks = MT.card_blocks(n, str)
    assert (("t", T.NODE_SRC_NONE) in blocks) and (("t", T.NODE_NO_REQUIRES) in blocks)
    assert ("b", "Kỹ năng 1") in blocks                                   # no topics: the micro-skills of its parts


def test_only_web_addresses_reach_the_browser(monkeypatch):
    opened = []
    monkeypatch.setattr("webbrowser.open", lambda url, *a, **k: opened.append(url) or True)
    assert MT.safe_url("https://example.org/a") and MT.safe_url("http://example.org")
    for bad in (None, "", "file:///C:/x", "javascript:alert(1)", "example.org", "https://"):
        assert not MT.safe_url(bad) and not MT.open_in_browser(bad)
    assert opened == []
    assert MT.open_in_browser("https://example.org/a") and opened == ["https://example.org/a"]


def test_a_browser_that_fails_only_reports_false(monkeypatch):
    def boom(url, *a, **k):
        raise OSError("no browser")
    monkeypatch.setattr("webbrowser.open", boom)
    assert MT.open_in_browser("https://example.org/") is False
    monkeypatch.setattr("webbrowser.open", lambda url, *a, **k: False)
    assert MT.open_in_browser("https://example.org/") is False
