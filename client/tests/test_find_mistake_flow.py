"""M11, Tìm chỗ sai through the real client UI against a real server: a player whose floors 1 and 2
are cleared opens the hầm ngục on floor 3, where the first room is a Phòng Soi Lỗi (the room of the
find_mistake question), and answers its questions with the card's own widgets: a number key chooses
a line (and does not cast a chiêu), a wrong line shows the reveal, the right line is paid.

    python -m client.tests.test_find_mistake_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_math_dungeon_flow import at_map, dungeon, top, wait_question
from client.tests.test_math_flow import clear_floor
from client.tests.test_world_flow import make_account

FLOOR = 3


def find_seed(url: str, token: str) -> int:
    """A seed whose floor-3 dungeon starts with a find_mistake room."""
    h = {"Authorization": f"Bearer {token}"}
    for seed in range(5000, 5300):
        lay = httpx.get(url + "/math/dungeon/layout", params={"seed": seed, "floor": FLOOR}, headers=h).json()["layout"]
        if lay["rooms"][0]["kind"] == "find_mistake":
            return seed
    raise AssertionError("no seed gives a Phòng Soi Lỗi first on floor 3")


def run_find_mistake_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "soi_loi", "Soi Lỗi")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "soi_loi", "server_url": url}))
        for n in (1, 2):
            clear_floor(server, uid, n)
        seed = find_seed(url, token)
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math hub")
        drv.click("math_hub_dungeon")
        drv.wait(lambda: drv.top_is("MathDungeonScene") and top(drv).data is not None, 10, "the dungeon gate")
        assert top(drv).data["own_floor"] == FLOOR
        while top(drv).floor < FLOOR:
            drv.click("dungeon_floor_next")
            drv.step(2)
        drv.click("dungeon_seed")
        drv.type(str(seed))
        drv.click("dungeon_start")
        drv.wait(lambda: at_map(drv) and dungeon(drv).run is not None, 10, "the map")
        run = dungeon(drv).run
        assert run["rooms"][0]["kind"] == "find_mistake"
        drv.shot("find_mistake_map")
        drv.click("dungeon_enter")

        # ---- the card: the lines numbered, a number key chooses (and casts nothing)
        q = wait_question(drv)
        card = top(drv)
        lines = q["prompt"]["lines"]
        assert q["qtype"] == "find_mistake" and q["input"] == "find_mistake" and 3 <= len(lines) <= 6
        assert q["math"]["floor"] == FLOOR and q["math"]["tier"] >= 2
        assert drv.has("fm_line_0") and drv.has(f"fm_line_{len(lines) - 1}") and not drv.has("opt_a")
        drv.shot("find_mistake_card")
        drv.press(pygame.K_2)
        assert card.mistake.sel == 1 and top(drv) is card and not card.sent
        drv.click("fm_line_0")                                     # click another line: the choice changes
        assert card.mistake.sel == 0
        drv.shot("find_mistake_chosen")
        assert server.sql("select count(*) from quiz_sessions where answered_at is not null")[0][0] == 0

        # ---- a wrong line: the reveal names the real one, then the solution
        key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
        res = _answer(drv, server, q, correct=False)
        assert not res["correct"] and res["reveal"]["answer_text"] == f"Bước {key['line'] + 1}: {lines[key['line']]}"
        assert res["reveal"]["solution_vi"]
        assert card.given_text() == f"Bước {card.given['line'] + 1}"
        assert card.given["line"] != key["line"] and type(card.given["line"]) is int
        drv.shot("find_mistake_wrong")
        drv.click("math_next")

        # ---- the right line: paid, and the next question comes
        q2 = wait_question(drv, q["session_id"])
        assert q2["qtype"] == "find_mistake"
        res = _answer(drv, server, q2, correct=True)
        assert res["correct"] and res["reveal"]["answer_text"].startswith("Bước ")
        drv.shot("find_mistake_right")
        rows = server.sql("select qtype, correct from math_answers where user_id=? order by id", (uid,))
        assert rows == [("find_mistake", 0), ("find_mistake", 1)]
        drv.close()
    finally:
        server.stop()


def _answer(drv: Driver, server: ServerProcess, q: dict, correct: bool) -> dict:
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("DungeonQuizScene") and top(drv).result, 10, "the result")
    return top(drv).result


def test_find_mistake_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_find_mistake_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "find_mistake"
    with tempfile.TemporaryDirectory() as tmp:
        run_find_mistake_flow(Path(tmp), out)
    print("screenshots in", out)
