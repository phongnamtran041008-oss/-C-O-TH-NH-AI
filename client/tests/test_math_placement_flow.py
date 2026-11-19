"""M11 through the real client UI: the math hub shows one bí cảnh at a time (a tab per
subject, mouse and keyboard), a subject offers its bài kiểm tra đầu vào, the explanation comes
first, the questions come on the ordinary math card, the result says where the player starts
and why, and the start floor is playable straight away while the floors below it read as
skipped. Run with a folder argument to keep the screenshots:
`python -m client.tests.test_math_placement_flow <dir>`."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account


def top(drv: Driver):
    return drv.game.top


def hub(drv: Driver):
    return next(s for s in drv.game.scenes if type(s).__name__ == "MathPracticeScene")


def answer(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    q = top(drv).q
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("PlacementQuizScene") and top(drv).result, 10, "the result")
    return top(drv).result


def run_placement_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        token, uid = make_account(server.url, "dau_vao", "Đầu Vào")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "dau_vao",
                                                          "server_url": server.url}))
        drv = Driver(server.url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the hub: a tab per subject, opened on the first one that can be played
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math path")
        subjects = top(drv).path["subjects"]
        assert len(subjects) >= 2
        first = next(i for i, s in enumerate(subjects) if any(f["playable"] for f in s["floors"]))
        assert top(drv).tab == first
        assert all(drv.has(f"math_tab_{s['id']}") for s in subjects)
        assert drv.has(f"math_floor_{subjects[first]['id']}_1")
        assert all(drv.has(d) for d in ("math_library", "math_close", "math_hub_dungeon", "math_hub_td",
                                        "math_hub_fortune"))
        drv.shot("hub_first_subject")

        # keyboard: Right shows the next subject, Left comes back
        drv.press(pygame.K_RIGHT)
        assert top(drv).tab == (first + 1) % len(subjects)
        assert not drv.has(f"math_floor_{subjects[first]['id']}_1")
        drv.shot("hub_next_subject")
        drv.press(pygame.K_LEFT)
        assert top(drv).tab == first

        # a subject with no questions still lists its floors, as "chưa có câu hỏi"
        empty = [s for s in subjects if not any(f["has_questions"] for f in s["floors"])]
        if empty:
            drv.click(f"math_tab_{empty[0]['id']}")
            assert top(drv).subject()["id"] == empty[0]["id"]
            assert not any(drv.has(f"math_floor_{empty[0]['id']}_{f['floor']}") for f in empty[0]["floors"])
            drv.shot("hub_subject_without_questions")

        # ---- switch to another subject that offers the bài kiểm tra đầu vào (the first one
        # if no other subject is written yet)
        offered = [s for s in subjects if (s.get("placement") or {}).get("offered")]
        assert offered, "no subject offers the placement test"
        target = next((s for s in offered if s["id"] != subjects[first]["id"]), offered[0])
        sid = target["id"]
        drv.click(f"math_tab_{sid}")
        assert top(drv).subject()["id"] == sid
        assert drv.has(f"math_place_{sid}")
        drv.shot("hub_target_subject")

        drv.click(f"math_place_{sid}")
        drv.wait(lambda: drv.top_is("PlacementScene") and top(drv).state is not None, 10, "the explanation")
        st = top(drv).state
        assert st["offered"] and st["status"] == "offered" and 10 <= st["planned"] <= 15
        drv.shot("placement_intro")
        drv.click("math_place_go")

        # ---- the sitting: everything right on floor 1, everything wrong from floor 2 up -> start
        # on floor 2, however many floors are written (the climb may jump past floor 2 and then
        # step back down to confirm it)
        seen = []
        for n in range(20):
            drv.wait(lambda: drv.top_is("PlacementQuizScene") and not top(drv).result, 10, "a placement question")
            q = top(drv).q
            seen.append((q["math"]["floor"], q["math"]["tier"]))
            assert q["context"] == "math_placement" and q["math"]["subject"] == sid
            if n == 0:
                drv.shot("placement_question")
            res = answer(drv, server, correct=q["math"]["floor"] < 2)
            if n == 0:
                drv.shot("placement_answered")
            if res["math"].get("placement_result"):
                break
            drv.click("math_next")
        assert len(seen) <= st["planned"] <= 15
        first_miss = next(i for i, (f, _) in enumerate(seen) if f >= 2)
        assert seen[:first_miss + 1] == sorted(seen[:first_miss + 1])     # rising until the first miss
        floors_after = [f for f, _ in seen[first_miss:]]
        assert floors_after == sorted(floors_after, reverse=True)         # then only down, to confirm
        assert [f for f, _ in seen].count(2) == 1 and floors_after[-1] == 2   # floor 2: one miss decides it
        drv.click("math_next")
        drv.wait(lambda: drv.top_is("PlacementScene") and top(drv).result is not None, 10, "the result")
        result = top(drv).result
        assert result["start_floor"] == 2 and result["skipped"] == [1] and not result["abandoned"]
        assert [(f["floor"], f["met"]) for f in result["floors"][:2]] == [(1, True), (2, False)]
        assert all(not f["met"] for f in result["floors"][1:])             # (floors asked above 2: missed too)
        drv.shot("placement_result")

        # ---- back in the hub: floor 1 skipped, floor 2 open and playable
        drv.click("math_place_back")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None and
                 top(drv).subject()["placement"]["status"] == "done", 10, "the hub again")
        s = top(drv).subject()
        assert s["id"] == sid and s["cleared"] == [1] and s["next_floor"] == 2
        assert [f["cleared_by"] for f in s["floors"][:3]] == ["placement", None, None]
        assert [f["state"] for f in s["floors"][:3]] == ["cleared", "open", "locked"]
        assert not drv.has(f"math_place_{sid}")                             # one sitting per subject
        assert drv.has(f"math_floor_{sid}_2")
        drv.shot("hub_after_placement")

        drv.click(f"math_floor_{sid}_2")
        drv.wait(lambda: drv.top_is("MathQuizScene") and not top(drv).result, 10, "a question of floor 2")
        assert top(drv).q["math"]["floor"] == 2 and top(drv).q["math"]["subject"] == sid
        drv.shot("start_floor_question")
        q = top(drv).q
        key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
        fill_math_answer(drv, q, key, True)
        drv.wait(lambda: top(drv).result, 10, "the answer")
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the floors")
        assert top(drv).subject()["id"] == sid                              # the hub stays on that subject

        # ---- the library opens on the subject the hub shows (when it has documents)
        drv.click("math_library")
        drv.wait(lambda: drv.top_is("LibraryListScene") and top(drv).data is not None, 10, "the library")
        lib = top(drv)
        ids = [x["id"] for x in lib.data["subjects"]]
        assert ids and lib.tab == (ids.index(sid) if sid in ids else 0)
        assert all(drv.has(f"lib_tab_{i}") for i in ids)
        drv.shot("library_tabs")
        drv.click("lib_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")

        runs = server.sql("select mode, passed, floor from math_runs where user_id=? and mode='placement'", (uid,))
        assert runs == [("placement", 1, 2)]
        drv.click("math_close")
        drv.close()
    finally:
        server.stop()


def test_placement_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_placement_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "math_placement"
    with tempfile.TemporaryDirectory() as tmp:
        run_placement_flow(Path(tmp), out)
    print("screenshots in", out)
