"""M10, hầm ngục through the real client UI against a real server: open the math hub from the
abode, go through its "Hầm Ngục" door, type a seed, and play that dungeon room by room to the
chest - one wrong answer on the way, one trip back to the map in the middle of a room - then
replay the same seed from the result screen and lose it by answering wrong.

    python -m client.tests.test_math_dungeon_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account


def top(drv: Driver):
    return drv.game.top


def dungeon(drv: Driver):
    from client.scenes.math_dungeon import MathDungeonScene
    return next((s for s in drv.game.scenes if isinstance(s, MathDungeonScene)), None)


def wait_question(drv: Driver, not_session: str | None = None) -> dict:
    drv.wait(lambda: drv.top_is("DungeonQuizScene") and top(drv).q["session_id"] != not_session
             and not top(drv).result, 10, "a dungeon question")
    return top(drv).q


def answer(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    q = top(drv).q
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("DungeonQuizScene") and top(drv).result, 10, "the result")
    return top(drv).result


def at_map(drv: Driver) -> bool:
    s = dungeon(drv)
    return drv.top_is("MathDungeonScene") and not s.busy and (s.run is not None or s.result is not None)


def short_seed(url: str, token: str) -> tuple[int, dict]:
    """A seed whose floor-1 dungeon has the fewest rooms the data allows (a quick test)."""
    h = {"Authorization": f"Bearer {token}"}
    best = None
    for seed in range(1000, 1060):
        lay = httpx.get(url + "/math/dungeon/layout", params={"seed": seed, "floor": 1}, headers=h).json()["layout"]
        if best is None or len(lay["rooms"]) < len(best[1]["rooms"]):
            best = (seed, lay)
    return best


def run_dungeon_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "ham_nguc", "Hầm Ngục Khách")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "ham_nguc", "server_url": url}))
        seed, layout = short_seed(url, token)
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the hub's door
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math hub")
        drv.click("math_hub_dungeon")
        drv.wait(lambda: drv.top_is("MathDungeonScene") and top(drv).data is not None, 10, "the dungeon gate")
        data = top(drv).data
        assert data["own_floor"] == 1 and data["run"] is None and top(drv).floor == 1
        assert [f["open"] for f in data["floors"][:4]] == [True, False, False, False]
        drv.shot("dungeon_gate")

        # ---- a typed seed opens exactly the dungeon that seed describes
        drv.click("dungeon_seed")
        drv.type(str(seed))
        drv.click("dungeon_start")
        drv.wait(lambda: at_map(drv) and dungeon(drv).run is not None, 10, "the map")
        run = dungeon(drv).run
        assert run["seed"] == seed and [r["kind"] for r in run["rooms"]] == [r["kind"] for r in layout["rooms"]]
        hearts = run["hearts"]
        stones_before = server.sql("select spirit_stones from users where id=?", (uid,))[0][0]
        drv.shot("dungeon_map")

        # ---- room by room to the chest
        last, wrong_done, map_trip_done, n = None, False, False, 0
        drv.click("dungeon_enter")
        while True:
            q = wait_question(drv, last)
            last = q["session_id"]
            room = dungeon(drv).run["rooms"][dungeon(drv).run["room"]]
            assert q["qtype"] == room["kind"] and q["math"]["floor"] == 1
            n += 1
            if n == 1:
                drv.shot("dungeon_question")
            good = wrong_done or n < 2                     # the second question is answered wrong
            res = answer(drv, server, good)
            wrong_done = True if n >= 2 else wrong_done
            assert res["correct"] == good
            d = res["dungeon"]
            if not good:
                assert d["heart_lost"] and d["run"]["hearts"] == hearts - 1
                drv.shot("dungeon_heart_lost")
                if not map_trip_done:                      # back to the map mid-room, then in again
                    map_trip_done = True
                    drv.click("math_stop")
                    drv.wait(lambda: at_map(drv), 10, "the map mid-room")
                    assert dungeon(drv).run["hearts"] == hearts - 1
                    drv.click("dungeon_enter")
                    continue
            if d["room_cleared"] and not d["run"]["ended"]:
                if d["run"]["room"] == 1:
                    drv.shot("dungeon_room_cleared")
                drv.click("math_next")                     # "Về bản đồ"
                drv.wait(lambda: at_map(drv), 10, "the map after a room")
                assert dungeon(drv).run["rooms"][d["run"]["room"] - 1]["state"] == "cleared"
                drv.click("dungeon_enter")
                continue
            if d["run"]["ended"]:
                assert d["chest"] and d["run"]["state"] == "cleared"
                drv.shot("dungeon_chest")
                drv.click("math_next")                     # "Xem kết quả"
                break
            drv.click("math_next")                         # "Câu tiếp"
        drv.wait(lambda: at_map(drv) and dungeon(drv).result is not None, 10, "the result")
        r = dungeon(drv).result
        want = layout["room_reward"]["stones"] * (len(layout["rooms"]) - 1) + layout["chest"]["stones"]
        assert r["state"] == "cleared" and r["stones_gained"] == want and r["xp_gained"] > 0
        assert r["hearts"] == hearts - 1 and r["asked"] == n
        assert server.sql("select spirit_stones from users where id=?", (uid,))[0][0] - stones_before == want
        assert server.sql("select count(*) from math_answers where user_id=? and run_id is null", (uid,))[0][0] == n
        drv.shot("dungeon_result")

        # ---- the same seed again, lost
        drv.click("dungeon_replay")
        drv.wait(lambda: at_map(drv) and dungeon(drv).run is not None, 10, "the replayed map")
        assert dungeon(drv).run["seed"] == seed and dungeon(drv).run["rooms"][0]["kind"] == layout["rooms"][0]["kind"]
        drv.click("dungeon_enter")
        last = None
        for i in range(hearts):
            q = wait_question(drv, last)
            last = q["session_id"]
            res = answer(drv, server, False)
            if i < hearts - 1:
                drv.click("math_next")
        assert res["dungeon"]["run"]["state"] == "failed"
        drv.shot("dungeon_lost_question")
        drv.click("math_next")
        drv.wait(lambda: at_map(drv) and dungeon(drv).result is not None, 10, "the lost result")
        assert dungeon(drv).result["state"] == "failed" and dungeon(drv).result["stones_gained"] == 0
        drv.shot("dungeon_lost")
        drv.click("dungeon_back")
        drv.wait(lambda: at_map(drv) or (drv.top_is("MathDungeonScene") and dungeon(drv).result is None
                                         and dungeon(drv).run is None), 10, "the gate again")
        assert server.sql("select state from math_dungeon_runs where user_id=? order by id", (uid,)) == \
            [("cleared",), ("failed",)]
        drv.click("dungeon_close")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "the hub")
        drv.close()
    finally:
        server.stop()


def test_a_seeded_dungeon_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_dungeon_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "dungeon"
    with tempfile.TemporaryDirectory() as tmp:
        run_dungeon_flow(Path(tmp), out)
    print("screenshots in", out)
