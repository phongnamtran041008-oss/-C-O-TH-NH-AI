"""Xạ Trường through the real client UI (docs/THUC_CHIEN_TRONG_GAME.md, tier 1): a Thực Chiến
node of Đạo Thụ opens its exercises from its card, a scored exercise ("khớp đường thẳng bằng
hạ gradient") shows its practice set summed up instead of printed, starts the editor with its
own starter code, and the reference solution - saved as the player's own file, the way someone
who writes in their own editor does - is run on the samples (Bắn tập) and handed in on the
hidden sets (Bắn thật). The result is a score and a grade, the target view shows each set
against the bars and the training loss the program printed to stderr, Tu Vi is paid, and the
list remembers the grade.

    python -m client.tests.test_xa_truong_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pygame

from client import strings_vi as T
from client.tests.driver import Driver, ServerProcess
from client.tests.test_linh_phong_flow import abode
from client.tests.test_math_flow import top
from client.tests.test_world_flow import make_account

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "server"))        # the test reads the tree and the parts the server ships
from app.learning import math_problems  # noqa: E402
from app.systems import math_tree_progress as tp  # noqa: E402

NODE = "ud_hoi_quy_1_bien"
EXERCISE = "xt_hq_khop_duong_thang"


def ancestors(node_id: str) -> list[str]:
    tree = tp.tree()
    seen: list[str] = []
    todo = list(tree.nodes[node_id].requires)
    while todo:
        nid = todo.pop()
        if nid not in seen:
            seen.append(nid)
            todo += tree.nodes[nid].requires
    return seen


def open_node(server: ServerProcess, uid: int, node_id: str) -> None:
    """Every node `node_id` waits for, done: each part's Thiên kiếp nhỏ passed and each exercise
    solved, written straight into the save (the flows of those nodes are tested elsewhere)."""
    tree = tp.tree()
    for nid in ancestors(node_id):
        for part in tp.parts(nid):
            server.sql("insert into math_runs(user_id, subject_id, node_id, floor, mode, tier, correct_streak, "
                       "wrong_streak, combo, best_combo, asked, correct, review_asked, xp_gained, ladders, passed, "
                       "started_at, ended_at) values (?, ?, ?, ?, 'trial', 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, "
                       "datetime('now'), datetime('now'))", (uid, part.subject_id, nid, part.floor))
        for pid in tree.nodes[nid].problems:
            server.sql("insert into math_submissions(user_id, problem_id, subject_id, floor, tier, verdict, passed, "
                       "total, ms, xp_gained, code, created_at, judged_at) "
                       "values (?, ?, 'x', 1, 1, 'AC', 5, 5, 1, 0, '', datetime('now'), datetime('now'))", (uid, pid))


def run_xa_truong_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "xa_thu", "Xạ Thủ")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        open_node(server, uid, NODE)
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "xa_thu", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the node's card on the Thực Chiến tab: open, with its three exercises
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math hub")
        drv.click("math_tab_ud")
        drv.click(f"math_info_{NODE}")
        drv.wait(lambda: drv.top_is("NodeCardScene"), 5, "the node card")
        node = top(drv).node
        assert node["state"] == "open" and [p["id"] for p in node["problems"]][-1] == EXERCISE
        drv.game.toasts.clear()
        drv.shot("xt_node_card")
        drv.click("math_info_code")
        drv.wait(lambda: drv.top_is("ProblemListScene") and top(drv).data is not None, 10, "the node's exercises")
        listed = [p for f in top(drv).shown_floors() for p in f["problems"]]
        assert [p["id"] for p in listed] == [p["id"] for p in node["problems"]]
        assert next(p for p in listed if p["id"] == EXERCISE)["scored"]

        # ---- the exercise: its own starter, the practice set summed up, the bars in the statement
        drv.click(f"code_open_{EXERCISE}")
        drv.wait(lambda: drv.top_is("ProblemScene") and top(drv).problem is not None, 10, "the statement")
        scene = top(drv)
        p = scene.problem
        assert p["scored"] and p["checker"] == "sai_so" and p["grades"] == [2.0, 1.5, 1.2]
        assert scene.box.text == p["starter"] and "#loss" in p["starter"]
        assert any(s.get("big") for s in p["samples"]) and not all(s.get("big") for s in p["samples"])
        drv.game.toasts.clear()
        drv.shot("xt_statement")
        drv.click("code_back")
        drv.wait(lambda: drv.top_is("ProblemListScene"), 5, "the list again")

        # the player writes the model in their own editor: the file the game keeps for this exercise
        reference = math_problems.solution_path("giai_tich", EXERCISE).read_text("utf-8")
        mine = workdir / "bai_lam" / f"{EXERCISE}.py"
        mine.parent.mkdir(parents=True, exist_ok=True)
        mine.write_text(reference, "utf-8")
        drv.click(f"code_open_{EXERCISE}")
        drv.wait(lambda: drv.top_is("ProblemScene") and top(drv).problem is not None, 10, "the statement again")
        scene = top(drv)
        assert scene.box.text.replace("\r\n", "\n") == reference.replace("\r\n", "\n")

        # ---- Bắn tập: the samples, the practice set included; the target view opens by itself
        drv.click("code_run")
        drv.wait(lambda: top(drv).result is not None, 60, "Chạy thử")
        res = top(drv).result
        assert res["mode"] == "run" and res["result"]["scored"] and res["result"]["grade"] == 3, res["result"]
        assert scene.show_target and drv.has("code_statement") and drv.has("code_target")
        run, log = scene.log
        assert run >= 1 and len(log["loss"]) >= 10 and log["loss"][-1][1] < log["loss"][0][1]
        drv.game.toasts.clear()
        drv.shot("xt_ban_tap")

        # ---- Bắn thật: the hidden sets, scored on the server, thượng phẩm and Tu Vi
        xp_before = server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0]
        drv.click("code_submit")
        drv.wait(lambda: (top(drv).result or {}).get("mode") == "submit", 90, "Nộp bài")
        res = top(drv).result
        r = res["result"]
        assert r["scored"] and r["metric"] == "sai_so" and r["grade"] == 3 and r["verdict"] == "AC", r
        assert r["grade_vi"] == "Thượng phẩm" and r["score"] <= 1.2 and len(r["tests"]) == 4
        assert all(t["score"] is not None for t in r["tests"])
        assert res["xp_gained"] > 0
        assert scene.show_target and len(scene.log[1]["loss"]) >= 10
        text = drawn_text(drv)
        assert T.XT_TARGET_HIDDEN in text and "Thượng phẩm" in text
        assert any(t.startswith(T.XT_LOSS_TITLE.split("(")[0]) for t in text)
        drv.game.toasts.clear()
        drv.shot("xt_ban_that")
        rows = server.sql("select verdict, passed, total, xp_gained from math_submissions "
                          "where user_id=? and problem_id=?", (uid, EXERCISE))
        assert rows == [("AC", 3, 3, res["xp_gained"])]
        xp_after = server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0]
        assert xp_after - xp_before == res["xp_gained"]

        # ---- back to the statement and to the list, which shows the grade
        drv.click("code_statement")
        assert not top(drv).show_target
        drv.click("code_back")
        drv.wait(lambda: drv.top_is("ProblemListScene") and any(
            (p.get("best") or {}).get("grade") == 3 for f in (top(drv).data or {}).get("floors", [])
            for p in f["problems"]), 15, "the list showing the grade")
        drv.game.toasts.clear()
        drv.shot("xt_list_graded")
        drv.close()
    finally:
        server.stop()


def drawn_text(drv: Driver) -> list[str]:
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


def test_xa_truong_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_xa_truong_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "xa_truong"
    with tempfile.TemporaryDirectory() as tmp:
        run_xa_truong_flow(Path(tmp), out)
    print("screenshots in", out)
