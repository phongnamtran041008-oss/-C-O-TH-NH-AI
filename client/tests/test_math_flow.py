"""M2 through the real client UI: open the Bí Cảnh Toán from the abode, start floor 1 of
Đại Số Tuyến Tính, answer right (Tu Vi), answer wrong (the solution is shown), let the
countdown run out, stop, read the summary, and find the answers in the database."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account

FLOOR_1 = "math_floor_dai_so_tuyen_tinh_1"


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
    if q["input"] == "truefalse":
        drv.click("math_true" if key["value"] == correct else "math_false")
    elif q["input"] == "choice":
        drv.click(f"opt_{key['option']}" if correct
                  else "opt_" + next(o["id"] for o in q["options"] if o["id"] != key["option"]))
    else:
        drv.click("quiz_text")
        drv.type(", ".join(key["numbers"]) if correct else "987654")
        drv.press(pygame.K_RETURN)
    drv.wait(lambda: drv.top_is("MathQuizScene") and top(drv).result, 10, "the result")
    return top(drv).result


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
        floors = top(drv).path["subjects"][0]["floors"]
        assert floors[0]["playable"] and not floors[1]["playable"]
        assert drv.has(FLOOR_1) and not drv.has("math_floor_dai_so_tuyen_tinh_2")
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

        # ---- stop on the next result: the summary
        wait_question(drv, q3["session_id"])
        answer_math(drv, server, correct=True)
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
        s = top(drv).summary
        assert (s["asked"], s["correct"], s["best_combo"], s["xp_gained"], s["ended"]) == (4, 2, 1, 6, True)
        drv.shot("math_summary")
        drv.click("math_back")
        drv.wait(lambda: top(drv).summary is None and top(drv).path is not None and top(drv).path["run"] is None,
                 10, "the floors again")
        drv.click("math_close")
        drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode again")

        # ---- what the server kept
        rows = server.sql("select correct, timed_out, tier, floor from math_answers where user_id=? order by id",
                          (uid,))
        assert rows == [(1, 0, 1, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1)]
        assert server.sql("select count(*) from math_runs where user_id=? and ended_at is null", (uid,))[0][0] == 0
        assert server.sql("select cultivation_xp from characters where user_id=?", (uid,))[0][0] == 6
        assert abode(drv).game.state.cult.get("xp") == 6      # the HUD heard about it
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
