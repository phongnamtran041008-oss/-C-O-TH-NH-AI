"""M10 cơ duyên through the real client UI against a real server: with nothing on offer the
scene explains how cơ duyên come; with an elder's offer (put in the player's state the way a
roll would) the player reads it, accepts, answers right through the math card and sees the
reward; a declined offer goes away and is logged; a chest takes a chain of questions.

    python -m client.tests.test_math_fortune_flow <screenshot dir>"""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account


def force(server: ServerProcess, uid: int, event_id: str) -> None:
    """An open offer of this event, as a roll would leave it."""
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    old = json.loads(server.sql("select flags from users where id=?", (uid,))[0][0])
    old["math_fortune"] = {
        "date": (now + dt.timedelta(hours=7)).date().isoformat(), "offers": 1, "count": 0,
        "log": (old.get("math_fortune") or {}).get("log", []),
        "open": {"event": event_id, "expires_at": (now + dt.timedelta(minutes=10)).isoformat(),
                 "accepted": False, "step": 0, "sid": None}}
    server.sql("update users set flags=? where id=?", (json.dumps(old), uid))


def stones(server: ServerProcess, uid: int) -> int:
    return server.sql("select spirit_stones from users where id=?", (uid,))[0][0]


def open_scene(drv: Driver) -> None:
    drv.click("math_hub_fortune")
    drv.wait(lambda: drv.top_is("MathFortuneScene") and drv.game.top.data is not None, 10, "the cơ duyên scene")


def answer_card(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    drv.wait(lambda: drv.top_is("FortuneQuizScene") and not drv.game.top.result, 10, "a cơ duyên question")
    q = drv.game.top.q
    assert q["context"] == "math_fortune"
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("FortuneQuizScene") and drv.game.top.result, 10, "the result")
    return drv.game.top.result


def run_fortune_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "co_duyen", "Cơ Duyên")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "co_duyen", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and drv.game.top.path is not None, 10, "the math hub")

        # ---- nothing on offer: the scene says how cơ duyên come
        open_scene(drv)
        assert drv.game.top.data["offer"] is None and drv.has("fortune_close")
        assert not drv.has("fortune_accept")
        drv.shot("fortune_idle")

        # ---- the toast of an offer that has just appeared
        from client.scenes.math_fortune import notice
        assert notice(drv.game, {"math": {"fortune_offer": {"name_vi": "Lão nhân bên suối"}}})
        assert not notice(drv.game, {"math": {"tier": 1}}) and not notice(drv.game, None)
        assert any("Lão nhân bên suối" in t for t in drv.toast_log)

        # ---- an elder: read it, accept, answer right, see the reward
        drv.click("fortune_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")
        force(server, uid, "lao_nhan_ben_suoi")
        before = stones(server, uid)
        open_scene(drv)
        assert drv.game.top.data["offer"]["id"] == "lao_nhan_ben_suoi" and drv.has("fortune_accept")
        assert drv.has("fortune_decline")
        drv.shot("fortune_offer")
        drv.click("fortune_accept")
        res = answer_card(drv, server, True)
        assert res["fortune"]["done"] and res["fortune"]["won"], res["fortune"]
        drv.shot("fortune_question_result")
        drv.click("math_next")
        drv.wait(lambda: drv.top_is("MathFortuneScene") and drv.game.top.result and drv.game.top.data["offer"] is None,
                 10, "the reward")
        won = drv.game.top.result
        assert won["rewards"]["spirit_stones"] > 0 and stones(server, uid) - before == won["rewards"]["spirit_stones"]
        drv.shot("fortune_reward")
        assert drv.game.top.data["log"][0]["outcome"] == "won"

        # ---- a declined one goes away and costs nothing
        force(server, uid, "lao_nhan_dai_lo")
        before = stones(server, uid)
        drv.click("fortune_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")
        open_scene(drv)
        assert drv.game.top.data["offer"]["id"] == "lao_nhan_dai_lo"
        drv.click("fortune_decline")
        drv.wait(lambda: drv.game.top.data["offer"] is None and not drv.game.top.busy, 10, "the offer gone")
        assert drv.game.top.data["log"][0]["outcome"] == "declined" and stones(server, uid) == before
        assert not drv.has("fortune_accept")

        # ---- a chest: two questions, the second one wrong -> no reward, nothing lost
        force(server, uid, "ruong_go_cu")
        drv.click("fortune_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")
        open_scene(drv)
        drv.click("fortune_accept")
        res = answer_card(drv, server, True)
        assert not res["fortune"]["done"] and res["fortune"]["progress"] == [1, 2]
        drv.click("math_next")
        res = answer_card(drv, server, False)
        assert res["fortune"]["done"] and not res["fortune"]["won"] and res["fortune"]["rewards"] is None
        drv.click("math_next")
        drv.wait(lambda: drv.top_is("MathFortuneScene") and drv.game.top.result and not drv.game.top.busy,
                 10, "the loss")
        assert stones(server, uid) == before
        drv.shot("fortune_lost")
        assert drv.game.top.data["log"][0]["outcome"] == "lost"
        drv.close()
    finally:
        server.stop()


def test_math_fortune_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_m10f_") as tmp:
        run_fortune_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "math_fortune"
    with tempfile.TemporaryDirectory() as tmp:
        run_fortune_flow(Path(tmp), out)
    print("screenshots in", out)
