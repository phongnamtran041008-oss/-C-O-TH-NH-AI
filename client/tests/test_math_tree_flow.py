"""Đạo Thụ through the real client UI: the math hub lists the nodes of the curriculum tree, not
floors. A new player sees where they stand (Luyện Khí) and the four first math nodes under
"Nên học"; a node's card shows why, what it needs and the recommended source (the browser opens
only when the button is pressed); a branch tab lists its nodes by stage, a node of two floors
has two rows, a locked node cannot be started and a vacant one says "Đang biên soạn"; the list
scrolls. A sitting runs on a node, its gate opens the Thiên kiếp nhỏ, and passing it opens the
nodes that waited for it - one of them in another branch."""
from __future__ import annotations

import json
import tempfile
import webbrowser
from pathlib import Path

import httpx
import pygame

from client import strings_vi as T
from client.scenes import math_tree as MT
from client.tests.driver import Driver, ServerProcess
from client.tests.test_linh_phong_flow import abode
from client.tests.test_math_flow import answer_math, meet_gate, top, wait_question
from client.tests.test_world_flow import make_account

FIRST_FOUR = ["ds_ngon_ngu", "gt_ham_so", "tr_logic_dem", "xs_dem_su_kien"]
NODE = "ds_ngon_ngu"
NEXT_NODE = "ds_vecto_ma_tran"
OTHER_BRANCH_NODE = "lt_cau_truc_du_lieu"          # Lập Trình: needs Python nhập môn and Tập hợp và ánh xạ
TWO_FLOORS = "gt_gioi_han"
VACANT = "tc_python_nang_cao"                    # a Lập Trình node with nothing written yet (Trúc Cơ; NumPy got content)


def drawn_text(drv: Driver) -> list[str]:
    """Every string the hub draws in the next frames (the screen is pixels, not widgets)."""
    ui = drv.game.ui
    seen: list[str] = []
    real = ui.text

    def spy(txt, *args, **kwargs):
        seen.append(txt)
        return real(txt, *args, **kwargs)
    ui.text = spy
    try:
        drv.step(2)
    finally:
        del ui.text
    return seen


def python_basics_done(server: ServerProcess, uid: int) -> None:
    """Python nhập môn (the first Lập Trình node of Luyện Khí) done: every exercise of it handed in with
    every hidden test right. These flows are about the maths nodes; the exercises themselves are tested
    in server/tests/test_math_tree_progress.py and test_lt_exercises.py."""
    tree = json.loads((Path(__file__).resolve().parents[2] / "server" / "data" / "math" / "tree.json").read_text("utf-8"))
    node = next(n for n in tree["nodes"] if n["id"] == "lt_python_co_ban")
    for pid in node["problems"]:
        server.sql("insert into math_submissions(user_id, problem_id, subject_id, floor, tier, verdict, passed, "
                   "total, ms, xp_gained, code, created_at, judged_at) "
                   "values (?, ?, 'x', 1, 1, 'AC', 5, 5, 1, 0, '', datetime('now'), datetime('now'))", (uid, pid))


def open_hub(drv: Driver) -> None:
    drv.click("hud_math")
    drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math hub")


def close_hub(drv: Driver) -> None:
    drv.click("math_close")
    drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode")


def run_tree_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    real_open = webbrowser.open
    try:
        url = server.url
        token, uid = make_account(url, "cay_sinh", "Cây Sinh")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        python_basics_done(server, uid)
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "cay_sinh", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- a new player: the stage and "Nên học" with the four first math nodes
        open_hub(drv)
        hub = top(drv)
        assert hub.tab == "next" and [t["id"] for t in hub.tabs][:3] == ["next", "ds", "gt"]
        assert [t["id"] for t in hub.tabs] == ["next", "ds", "gt", "xs", "tr", "lt", "ud"]
        assert all(drv.has(f"math_tab_{t['id']}") for t in hub.tabs)
        stage = hub.tree["stage"]
        assert (stage["realm_name_vi"], stage["stage"], stage["stages"]) == ("Luyện Khí", 0, 9)
        assert hub.tree["next"] == FIRST_FOUR
        assert all(drv.has(f"math_node_{n}_1") for n in FIRST_FOUR)
        assert all(drv.has(f"math_info_{n}") for n in FIRST_FOUR)
        assert not drv.has(f"math_trial_{NODE}_1")                    # the gate is closed
        text = drawn_text(drv)
        assert MT.header_text(stage) in text and "Tầng 1" in text
        assert T.TREE_STAGE_PROGRESS.format(d=1, t=5, n=1) in text    # "đã xong 1/5 nút của tầng 1": Python nhập môn
        drv.shot("tree_next")

        # ---- the card of a node: why, what it needs, the source - and the browser only on a press
        opened: list[str] = []
        webbrowser.open = lambda u, *a, **k: opened.append(u) or True
        drv.click(f"math_info_{NODE}")
        drv.wait(lambda: drv.top_is("NodeCardScene"), 5, "the node card")
        card = top(drv)
        node = card.node
        assert node["id"] == NODE and node["why_vi"] and node["source"]["url"].startswith("http")
        kinds = {k for k, _ in MT.card_blocks(node, str)}
        assert {"h", "t", "b"} <= kinds
        drv.step(3)
        assert any(node["source"]["title"] in s for _, s in card.lines) or card.lines
        text = drawn_text(drv)
        assert T.NODE_SOURCE in text and node["source"]["title"] in text and node["why_vi"].split()[0] in " ".join(text)
        assert opened == [], "the card never opens a URL by itself"
        drv.shot("tree_node_card")
        drv.click("math_src_open")
        assert opened == [node["source"]["url"]]
        webbrowser.open = lambda u, *a, **k: False                       # no browser: a message, no crash
        n_toasts = len(drv.toast_log)
        drv.click("math_src_open")
        assert drv.toast_log[n_toasts:] == [T.NODE_SRC_FAILED]
        drv.click("math_info_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")
        webbrowser.open = real_open

        # ---- the card of a node that is not open yet says what it needs
        drv.click("math_tab_ds")
        assert top(drv).tab == "ds"
        drv.click(f"math_info_{NEXT_NODE}")
        drv.wait(lambda: drv.top_is("NodeCardScene"), 5, "the second card")
        lines = [t for _, t in MT.card_blocks(top(drv).node, top(drv).name_of)]
        assert f"{top(drv).node['requires'][0]['name_vi']} - {T.NODE_REQ_TODO}" in lines
        assert top(drv).node["requires"][0]["id"] == NODE and top(drv).node["state"] == "locked"
        drv.shot("tree_card_locked")
        drv.click("math_info_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub again")

        # ---- a branch tab: rows by stage, a locked row says what is needed, optional nodes last
        rows = MT.node_rows(top(drv).tree, "ds")
        assert [r.node["id"] for r in rows][:3] == [NODE, NEXT_NODE, "ds_nhan_ma_tran"]
        mains = [r for r in rows if r.node["status"] == "chinh"]
        assert rows[-1].node["status"] == "phu" and rows[:len(mains)] == mains
        assert drv.has(f"math_node_{NODE}_1") and not drv.has(f"math_node_{NEXT_NODE}_3")
        text = drawn_text(drv)
        assert T.TREE_NEEDS.format(name=top(drv).tree["nodes"][0]["name_vi"]) in text, text
        assert f"math_place_dai_so_tuyen_tinh" in drv.game.ui.widgets and drv.has("math_code_dai_so_tuyen_tinh")
        drv.shot("tree_branch_ds")

        # ---- the list scrolls: nine rows are shown, there are more
        total, shown = len(rows), top(drv).SHOWN
        assert total > shown and top(drv).first == 0
        assert drv.has(f"math_info_{rows[0].node['id']}") and not drv.has(f"math_info_{rows[-1].node['id']}")
        for _ in range(total - shown):
            drv.press(pygame.K_DOWN)
        drv.press(pygame.K_DOWN)                                       # (one more does nothing)
        assert top(drv).first == total - shown
        assert not drv.has(f"math_info_{rows[0].node['id']}") and drv.has(f"math_info_{rows[-1].node['id']}")
        assert any(f"{total} " in s and "trong" in s for s in drawn_text(drv))
        drv.shot("tree_scrolled")
        for _ in range(total):
            drv.press(pygame.K_UP)
        assert top(drv).first == 0

        # ---- a node of two floors has two rows, both locked; a locked node cannot be started
        drv.click("math_tab_gt")
        two = [r for r in MT.node_rows(top(drv).tree, "gt") if r.node["id"] == TWO_FLOORS]
        assert [(r.index, r.part["floor"]) for r in two] == [(1, 2), (2, 3)]
        assert drv.has(f"math_info_{TWO_FLOORS}") and drv.has(f"math_info_{TWO_FLOORS}_2")
        assert not any(drv.has(f"math_node_{TWO_FLOORS}_{f}") for f in (2, 3))
        assert not any(drv.has(f"math_trial_{TWO_FLOORS}_{f}") for f in (2, 3))
        text = drawn_text(drv)
        assert "Cần xong: " + top(drv).tree["nodes"][1]["name_vi"] in text      # Hàm số, hàm hợp, mũ và logarit
        assert any(s.endswith("(1/2)") for s in text) and any(s.endswith("(2/2)") for s in text)
        drv.shot("tree_two_floors_locked")
        refused = httpx.post(url + "/math/node/start", json={"node_id": TWO_FLOORS},
                             headers={"Authorization": f"Bearer {token}"})
        assert refused.status_code == 403 and refused.json()["error"]["code"] == "node_locked"
        n_toasts = len(drv.toast_log)
        top(drv).start(TWO_FLOORS, 2)                                  # what a stray call from the UI would do
        drv.wait(lambda: len(drv.toast_log) > n_toasts, 5, "the refusal")
        assert drv.toast_log[n_toasts] == refused.json()["error"]["message_vi"] and top(drv).run is None
        top(drv).start(TWO_FLOORS, 3, trial=True)
        drv.wait(lambda: len(drv.toast_log) > n_toasts + 1, 5, "the refusal of the trial")
        assert top(drv).run is None and not top(drv).busy

        # ---- a vacant node says "Đang biên soạn" and cannot be started
        drv.click("math_tab_lt")
        vacant = [r for r in MT.node_rows(top(drv).tree, "lt") if r.node["id"] == VACANT][0]
        assert vacant.node["state"] == "vacant" and MT.row_state(vacant) == "vacant"
        assert not any(w.startswith(f"math_node_{VACANT}") or w.startswith(f"math_trial_{VACANT}")
                       for w in drv.game.ui.widgets)
        assert T.TREE_VACANT == "Đang biên soạn" and text.count(T.TREE_VACANT) == 0
        assert drawn_text(drv).count(T.TREE_VACANT) >= 1
        drv.shot("tree_branch_lt_vacant")

        # ---- a sitting on a node
        drv.click("math_tab_next")
        drv.click(f"math_node_{NODE}_1")
        q = wait_question(drv)
        assert q["math"]["floor"] == 1 and top(drv).run["node_id"] == NODE
        assert top(drv).run["node_name_vi"] == node["name_vi"]
        res = answer_math(drv, server, correct=True)
        assert res["correct"]
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
        assert top(drv).summary["node_id"] == NODE
        text = drawn_text(drv)
        assert node["name_vi"] in text                                 # the summary names the node
        assert any(s.startswith("Cổng thuần thục") for s in text)       # and what the gate of its part still wants
        drv.shot("tree_summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the hub")
        assert server.sql("select node_id from math_runs where user_id=?", (uid,)) == [(NODE,)]

        # ---- the gate opens the Thiên kiếp nhỏ of the node; passing it opens what waited for it
        skills = [k["id"] for k in node["parts"][0]["skills"]]
        meet_gate(server, uid, skills, floor=1)
        close_hub(drv)
        open_hub(drv)
        assert drv.has(f"math_trial_{NODE}_1")
        drv.shot("tree_gate_open")
        drv.click(f"math_trial_{NODE}_1")
        last = None
        for n in range(1, len(skills) + 1):
            q = wait_question(drv, last)
            last = q["session_id"]
            assert top(drv).run["mode"] == "trial" and top(drv).run["node_id"] == NODE
            res = answer_math(drv, server, correct=True)
            if n < len(skills):
                drv.click("math_next")
        verdict = res["math"]["trial"]
        assert verdict["passed"] and verdict["node_done"]
        assert NEXT_NODE in verdict["opened"] and OTHER_BRANCH_NODE in verdict["opened"]
        drv.click("math_next")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the verdict")
        drv.wait(lambda: top(drv).tree["nodes"] and NEXT_NODE in top(drv).tree["next"], 10, "the reloaded tree")
        names = MT.names_of(top(drv).tree, top(drv).trial["opened"])
        assert len(names) == len(verdict["opened"]) and names
        text = drawn_text(drv)
        assert T.TREE_NODE_DONE_LINE.format(name=node["name_vi"]) in text
        assert T.TREE_OPENED.format(names=", ".join(names)) in text
        drv.shot("tree_trial_verdict")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the hub after the verdict")

        # ---- the node that opened is in "Nên học" and playable; the one of another branch is open too
        tree = top(drv).tree
        assert NODE not in tree["next"] and NEXT_NODE in tree["next"] and OTHER_BRANCH_NODE in tree["next"]
        assert next(n for n in tree["nodes"] if n["id"] == NODE)["state"] == "done"
        assert next(n for n in tree["nodes"] if n["id"] == OTHER_BRANCH_NODE)["branch"] == "lt"
        drv.click("math_tab_next")
        assert drv.has(f"math_node_{NEXT_NODE}_3") and drv.has(f"math_info_{OTHER_BRANCH_NODE}")
        drv.click("math_tab_ds")
        text = drawn_text(drv)
        assert T.MATH_CLEARED in text                                  # the passed node says so
        assert drv.has(f"math_node_{NODE}_1")                          # and can still be practised
        drv.shot("tree_after_trial")
        drv.click("math_tab_lt")
        row = [r for r in MT.node_rows(top(drv).tree, "lt") if r.node["id"] == OTHER_BRANCH_NODE][0]
        assert MT.row_state(row) == "code"
        assert T.TREE_CODE_ONLY in drawn_text(drv)
        drv.shot("tree_other_branch_opened")

        # ---- the stage line moves with every node: two of the five done, so "đã xong 2/5 nút của tầng 1"
        assert top(drv).tree["stage"]["progress"] == {"stage": 1, "done": 2, "total": 5}
        drv.click("math_tab_next")
        assert T.TREE_STAGE_PROGRESS.format(d=2, t=5, n=1) in drawn_text(drv)
        drv.game.toasts.clear()                                       # (the guide's "Xong" toasts hide the line)
        drv.shot("tree_stage_progress")

        # ---- a programming node's card has its own "Làm bài": it opens that node's exercises only
        drv.click("math_tab_lt")
        drv.click(f"math_info_{OTHER_BRANCH_NODE}")
        drv.wait(lambda: drv.top_is("NodeCardScene"), 5, "the programming node's card")
        code_node = top(drv).node
        assert code_node["state"] == "open" and code_node["problems"] and MT.exercises_open(code_node)
        assert T.NODE_DO_PROBLEMS in drawn_text(drv) and drv.has("math_info_code")
        drv.game.toasts.clear()
        drv.shot("tree_node_card_code")
        drv.click("math_info_code")
        drv.wait(lambda: drv.top_is("ProblemListScene") and top(drv).data is not None, 10, "the node's exercises")
        listed = [p["id"] for f in top(drv).shown_floors() for p in f["problems"]]
        assert listed == [p["id"] for p in code_node["problems"]], listed
        assert all(drv.has(f"code_open_{pid}") for pid in listed)
        drv.game.toasts.clear()
        drv.shot("tree_node_exercises")
        drv.click("code_close")
        drv.wait(lambda: drv.top_is("NodeCardScene"), 5, "back on the card")
        drv.click("math_info_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub at the end")
        close_hub(drv)
        drv.close()
    finally:
        webbrowser.open = real_open
        server.stop()


def test_tree_hub_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_tree_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "tree"
    with tempfile.TemporaryDirectory() as tmp:
        run_tree_flow(Path(tmp), out)
    print("screenshots in", out)
