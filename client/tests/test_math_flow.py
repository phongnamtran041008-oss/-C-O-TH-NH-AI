"""M2 through the real client UI: open the Bí Cảnh Toán from the abode, start floor 1 of
Đại Số Tuyến Tính, answer right (Tu Vi), answer wrong (the solution is shown), let the
countdown run out, stop, read the summary, and find the answers in the database.
M3: the mistake comes back as a parallel question, and floor 3 shows a matrix question.
M5: floors above the first are locked, the mastery gate opens the Thiên kiếp nhỏ, passing it
clears the floor and opens the next, and a sitting there mixes in review questions.
M6: a programming exercise is written in the game's own editor, run on the samples, handed
in on the hidden tests, and pays Tu Vi."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account

SUBJECT = "dai_so_tuyen_tinh"
CODE_LIST = "math_code_dai_so_tuyen_tinh"
EXERCISE = "dstt_bt_dem_phan_tu"
FLOOR_1 = "math_floor_dai_so_tuyen_tinh_1"
FLOOR_2 = "math_floor_dai_so_tuyen_tinh_2"
FLOOR_3 = "math_floor_dai_so_tuyen_tinh_3"
TRIAL_1 = "math_trial_dai_so_tuyen_tinh_1"


def top(drv: Driver):
    return drv.game.top


def wait_question(drv: Driver, not_session: str | None = None) -> dict:
    drv.wait(lambda: drv.top_is("MathQuizScene") and top(drv).q["session_id"] != not_session
             and not top(drv).result, 10, "a math question")
    return top(drv).q


def answer_math(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    """Reads the answer key from the server database (test only) and answers through the UI."""
    q = top(drv).q
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("MathQuizScene") and top(drv).result, 10, "the result")
    return top(drv).result


def meet_gate(server: ServerProcess, uid: int, skills: list[str], floor: int, tiers=(1, 2)) -> None:
    """Write the answer log the mastery gate wants (M5): every micro-skill of the floor
    answered right five times at every tier of the floor. Answering 60 questions through
    the UI would say nothing more than the six the Thiên kiếp nhỏ itself asks."""
    rows, n = [], 0
    for skill in skills:
        for tier in tiers:
            for _ in range(5):
                n += 1
                rows.append((uid, SUBJECT, skill, floor, tier, f"seed_{n}", "numeric", f"seedfp_{n}"))
    values = ", ".join(["(?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0, 900, '2025-12-01 00:00:00')"] * len(rows))
    server.sql("insert into math_answers (user_id, subject_id, skill_id, floor, tier, item_id, qtype, "
               f"fingerprint, correct, timed_out, review, answer_ms, answered_at) values {values}",
               [v for row in rows for v in row])


def lapse(server: ServerProcess, uid: int, skill: str, floor: int, tier: int = 1) -> None:
    """A wrong answer on a micro-skill of an earlier floor, so the spiral review has
    something due: a lapse comes back at once instead of waiting a day (M5, rule 6)."""
    server.sql("insert into math_answers (user_id, subject_id, skill_id, floor, tier, item_id, qtype, "
               "fingerprint, correct, timed_out, review, answer_ms, answered_at) "
               "values (?, ?, ?, ?, ?, 'lapse', 'numeric', 'lapsefp', 0, 0, 0, 900, '2025-12-02 00:00:00')",
               (uid, SUBJECT, skill, floor, tier))


def clear_floor(server: ServerProcess, uid: int, floor: int) -> None:
    """A passed Thiên kiếp nhỏ, so the floor above opens (M5)."""
    server.sql("insert into math_runs (user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
               "combo, best_combo, asked, correct, review_asked, xp_gained, passed, started_at, ended_at) "
               "values (?, ?, ?, 'trial', 2, 0, 0, 0, 0, 1, 1, 0, 0, 1, '2025-12-01', '2025-12-01')",
               (uid, SUBJECT, floor))


def reopen_floors(drv: Driver) -> dict:
    """Close the bí cảnh and open it again, so the floor list is read from the server."""
    drv.click("math_close")
    drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode")
    drv.click("hud_math")
    drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math path")
    return top(drv).path["subjects"][0]


def run_math_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "toan_sinh", "Toán Sinh")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "toan_sinh", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the floors
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math path")
        subject = top(drv).path["subjects"][0]
        floors = subject["floors"]
        assert [f["has_questions"] for f in floors] == [True] * 9 + [False]      # floors 1-9 are written
        assert [f["state"] for f in floors[:3]] == ["open", "locked", "locked"]      # M5
        assert [f["playable"] for f in floors[:4]] == [True, False, False, False]
        assert subject["cleared"] == [] and subject["next_floor"] == 1
        assert drv.has(FLOOR_1) and not drv.has(FLOOR_2) and not drv.has(TRIAL_1)
        drv.shot("math_floors")

        # ---- a right answer: Tu Vi by tier
        drv.click(FLOOR_1)
        q = wait_question(drv)
        assert q["math"]["floor"] == 1 and q["math"]["tier"] == 1
        scene = top(drv)
        assert scene.limit == q["time_limit"] and 0 < scene.seconds_left() <= q["time_limit"]
        drv.shot("math_question")
        res = answer_math(drv, server, correct=True)
        assert res["correct"] and res["xp"]["gained"] == 3
        assert res["math"]["run"]["combo"] == 1
        drv.shot("math_right")
        drv.click("math_next")

        # ---- a wrong answer: the solution is shown step by step
        q2 = wait_question(drv, q["session_id"])
        res = answer_math(drv, server, correct=False)
        assert not res["correct"] and res["reveal"]["solution_vi"] and "xp" not in res
        assert res["math"]["run"]["combo"] == 0
        drv.shot("math_wrong")
        drv.press(pygame.K_RETURN)                      # Enter = next question

        # ---- the countdown runs out: a wrong answer, nothing typed
        q3 = wait_question(drv, q2["session_id"])
        scene = top(drv)
        scene.t = scene.limit - 0.2                     # (skip the wait, not the rule)
        drv.wait(lambda: scene.result is not None, 10, "the timeout result")
        assert scene.timed_out and not scene.result["correct"] and scene.result["math"]["timed_out"]
        drv.shot("math_timeout")
        drv.click("math_next")

        # ---- the mistake comes back (rule 6): same micro-skill and tier, other numbers
        q4 = wait_question(drv, q3["session_id"])
        assert q4["math"]["parallel"]
        assert (q4["math"]["skill"], q4["math"]["tier"]) == (q2["math"]["skill"], q2["math"]["tier"])
        drv.shot("math_parallel")
        res = answer_math(drv, server, correct=True)
        assert res["correct"] and res["math"]["parallel"] and not res["math"]["parallel_waiting"]
        drv.shot("math_parallel_cleared")

        # ---- stop on that result: the summary
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
        s = top(drv).summary
        assert (s["asked"], s["correct"], s["best_combo"], s["xp_gained"], s["ended"]) == (4, 2, 1, 6, True)
        drv.shot("math_summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None and top(drv).path["run"] is None,
                 10, "the floors again")
        rows = server.sql("select correct, timed_out, tier, floor from math_answers where user_id=? order by id",
                          (uid,))
        assert rows == [(1, 0, 1, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1)]
        retries = server.sql("select cleared_at is not null from math_retries where user_id=? order by id", (uid,))
        assert retries == [(1,), (0,)]          # the wrong answer was made good; the timeout still waits

        # ---- M5: the mastery gate opens the Thiên kiếp nhỏ of floor 1
        skills = [k["id"] for k in floors[0]["skills"]]
        meet_gate(server, uid, skills, floor=1)
        subject = reopen_floors(drv)
        gate = subject["floors"][0]["gate"]
        assert gate["ok"] and not gate["weak"] and len(gate["skills"]) == len(skills)
        assert drv.has(TRIAL_1), "the Thiên kiếp nhỏ button"
        drv.shot("math_gate_open")

        drv.click(TRIAL_1)
        last, seen = None, []
        for n in range(1, len(skills) + 1):
            q = wait_question(drv, last)
            last = q["session_id"]
            seen.append(q["math"]["skill"])
            run = top(drv).run
            assert run["mode"] == "trial" and run["trial"]["total"] == len(skills)
            assert q["math"]["tier"] == 2 and not q["math"]["review"]
            if n == 1:
                drv.shot("math_trial_question")
            res = answer_math(drv, server, correct=True)
            trial = res["math"]["trial"]
            assert (trial["asked"], trial["left"]) == (n, len(skills) - n)
            if n < len(skills):
                assert trial["passed"] is None
                drv.click("math_next")
        assert seen == skills                            # one question per micro-skill, in path order
        assert (trial["passed"], trial["unlocked"]) == (True, 2)
        drv.shot("math_trial_passed")
        drv.click("math_next")                           # "Xem kết quả"
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the verdict")
        assert top(drv).trial["passed"] and top(drv).trial["unlocked"] == 2
        drv.shot("math_trial_summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the floors again")
        subject = reopen_floors(drv)
        assert [f["state"] for f in subject["floors"][:3]] == ["cleared", "open", "locked"]
        assert subject["cleared"] == [1] and subject["next_floor"] == 2
        assert drv.has(FLOOR_2)
        drv.shot("math_floor_cleared")

        # ---- M5: a sitting on floor 2 brings floor 1 back (rule 6, ôn xoắn ốc)
        # Every micro-skill of floor 1 was just answered right in the trial, so none is due
        # for a day; one wrong answer on the first of them is what the review slot is for.
        lapse(server, uid, skills[0], floor=1)
        drv.click(FLOOR_2)
        last, reviewed = None, None
        for n in range(1, 5):
            q = wait_question(drv, last)
            last = q["session_id"]
            if q["math"]["review"]:
                reviewed = q
                drv.shot("math_review")
            else:
                assert q["math"]["floor"] == 2
            answer_math(drv, server, correct=True)
            if n < 4:
                drv.click("math_next")
        assert reviewed is not None, "no review question in four"
        assert reviewed["math"]["floor"] == 1 and reviewed["math"]["skill"] == skills[0]
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
        assert top(drv).summary["review_asked"] == 1 and top(drv).trial is None
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the floors")

        # ---- floor 3: a question that shows matrices
        clear_floor(server, uid, 2)                      # floor 3 needs floor 2 behind it
        reopen_floors(drv)
        drv.click(FLOOR_3)
        last = None
        for _ in range(20):
            q = wait_question(drv, last)
            if q["prompt"].get("matrices"):
                break
            last = q["session_id"]
            answer_math(drv, server, correct=True)
            drv.click("math_next")
        assert q["prompt"]["matrices"] and q["math"]["floor"] == 3 and q["math"]["tier"] in (2, 3)
        drv.shot("math_matrix")
        res = answer_math(drv, server, correct=False)
        assert not res["correct"] and res["reveal"]["solution_vi"]
        drv.shot("math_matrix_wrong")
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the second summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None, 10, "the floors once more")
        # ---- M6: a programming exercise, written and handed in through the game
        drv.click(CODE_LIST)
        drv.wait(lambda: drv.top_is("ProblemListScene") and top(drv).data is not None, 10, "the exercises")
        floors = top(drv).data["floors"]
        assert [f["floor"] for f in floors] == [1, 2, 3]          # every open floor that has exercises
        assert any(p["id"] == EXERCISE for p in floors[0]["problems"])
        assert all(p["best"] is None for f in floors for p in f["problems"])
        drv.shot("code_list")

        drv.click(f"code_open_{EXERCISE}")
        drv.wait(lambda: drv.top_is("ProblemScene") and top(drv).problem is not None, 10, "the statement")
        scene = top(drv)
        total = scene.problem["tests"]
        assert scene.problem["samples"] and isinstance(total, int) and total >= 3
        drv.shot("code_statement")

        # the starter the game offers reads stdin but answers nothing yet
        drv.click("code_run")
        drv.wait(lambda: top(drv).result is not None, 30, "the first Chạy thử")
        assert top(drv).result["result"]["verdict"] == "WA"
        drv.shot("code_first_try")

        for _ in range(8):                                        # to the end of the starter
            drv.press(pygame.K_DOWN)
        drv.press(pygame.K_END)
        drv.press(pygame.K_RETURN)
        drv.type("print(len({int(x) for x in data[1:]}))")
        assert "print(len(" in top(drv).box.text
        drv.shot("code_written")

        drv.click("code_run")
        drv.wait(lambda: (top(drv).result or {}).get("result", {}).get("verdict") == "AC",
                 30, "Chạy thử passing")
        assert top(drv).result["mode"] == "run"
        assert top(drv).result["result"]["passed"] == len(scene.problem["samples"])
        drv.shot("code_run_ok")

        xp_before = server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0]
        drv.click("code_submit")
        drv.wait(lambda: (top(drv).result or {}).get("mode") == "submit", 60, "Nộp bài")
        res = top(drv).result
        assert res["result"]["verdict"] == "AC"
        assert res["result"]["passed"] == res["result"]["total"] == total
        assert res["xp_gained"] > 0
        drv.shot("code_accepted")

        saved = Path(drv.game.session.path).parent / "bai_lam" / f"{EXERCISE}.py"
        assert saved.is_file() and "print(len(" in saved.read_text("utf-8")
        rows = server.sql("select verdict, passed, total, xp_gained from math_submissions where user_id=?",
                          (uid,))
        assert rows == [("AC", total, total, res["xp_gained"])]
        xp_after = server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0]
        assert xp_after - xp_before == res["xp_gained"]

        drv.click("code_back")
        drv.wait(lambda: drv.top_is("ProblemListScene") and any(
            p.get("best") for f in (top(drv).data or {}).get("floors", []) for p in f["problems"]),
            15, "the list showing the verdict")
        drv.shot("code_list_solved")
        drv.click("code_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 10, "the floors")

        drv.click("math_close")
        drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode again")

        # ---- what the server kept
        assert server.sql("select count(*) from math_runs where user_id=? and ended_at is null", (uid,))[0][0] == 0
        xp = server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0]
        assert xp == (server.sql("select sum(xp_gained) from math_runs where user_id=?", (uid,))[0][0]
                      + server.sql("select sum(xp_gained) from math_submissions where user_id=?",
                                   (uid,))[0][0])
        assert abode(drv).game.state.cult.get("xp") == xp     # the HUD heard about it
        drv.close()
    finally:
        server.stop()


def test_math_loop_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_math_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "math"
    with tempfile.TemporaryDirectory() as tmp:
        run_math_flow(Path(tmp), out)
    print("screenshots in", out)
