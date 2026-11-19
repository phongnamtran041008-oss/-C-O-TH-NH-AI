"""M11 đợt 2, Thiên kiếp through the real client UI against a real server.

No mode hands a brand-new player a Thiên kiếp (tiers 4-5 only, and the dungeon, the thủ thành and
the bí cảnh never ask one), so the question itself is made by the server's own code - the seed
item dstt_t5_so_nghiem_91 through math_items.to_question and quiz.create_session, in a
subprocess on the server's database, as a hầm ngục question with no run - and everything after
that is the real thing: the card shows the situation and the parts, the player answers part by
part with the card's widgets (number box, options, Đúng / Sai, Phần sau, Trả lời), POST
/quiz/answer grades {"parts": [...]}, the answer is logged in math_answers, and the reveal says
part by part what was right.

    python -m client.tests.test_tribulation_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import ROOT, Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account

ITEM = "dstt_t5_so_nghiem_91"

MAKE = """
import asyncio, json, random, sys
from app import db as dbm
from app.learning import math_items, quiz
from app.models import User
from app.systems import math_dungeon  # noqa: F401  (registers the context's handler)

async def main():
    async with dbm.SessionLocal() as db:
        user = await db.get(User, int(sys.argv[1]))
        q = math_items.to_question(math_items.bank()[sys.argv[2]], random.Random(int(sys.argv[3])))
        out = await quiz.create_session(db, user, "math_dungeon", q, ref="")
        await db.commit()
    print(json.dumps(out))

asyncio.run(main())
"""


def make_question(server: ServerProcess, uid: int, seed: int) -> dict:
    """A Thiên kiếp quiz session made by the server's own code (see the module docstring)."""
    env = dict(os.environ, DATABASE_URL=f"sqlite+aiosqlite:///{server.db}", ENV="dev", ALLOW_UNREVIEWED="1")
    out = subprocess.run([sys.executable, "-c", MAKE, str(uid), ITEM, str(seed)], cwd=ROOT / "server", env=env,
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def open_card(drv: Driver, q: dict):
    from client.scenes.math_practice import MathQuizScene
    card = MathQuizScene(drv.game, q)
    drv.game.push(card)
    drv.step(3)
    return card


def answer(drv: Driver, server: ServerProcess, card, correct: bool) -> dict:
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (card.q["session_id"],))[0][0])
    fill_math_answer(drv, card.q, key, correct)
    drv.wait(lambda: card.result is not None, 10, "the result")
    drv.step(2)
    return card.result


def run_tribulation_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        token, uid = make_account(server.url, "thien_kiep", "Thiên Kiếp")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "thien_kiep",
                                                          "server_url": server.url}))
        drv = Driver(server.url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the card: the situation on top, part a of 4 with its own input
        q = make_question(server, uid, 1)
        assert q["qtype"] == "tribulation" and q["input"] == "tribulation" and q["time_limit"] == 480
        parts = q["prompt"]["parts"]
        assert [p["input"] for p in parts] == ["number", "choice", "number", "truefalse"]
        card = open_card(drv, q)
        assert card.trib is not None and card.trib.cur == 0
        assert drv.has("trib_text_0") and drv.has("trib_part_3") and not drv.has("trib_true")
        drv.shot("tribulation_part_a")
        drv.click("trib_text_0")
        drv.type("2")
        drv.click("trib_next")
        drv.step(2)
        assert drv.has("trib_opt_a") and not drv.has("trib_text_0")
        drv.press(pygame.K_1)                                       # a number key picks an option
        assert card.trib.answers[1] == {"option": "a"} and not card.sent
        drv.shot("tribulation_part_b")
        drv.press(pygame.K_LEFT)                                    # back to part a: its answer is kept
        assert card.trib.cur == 0 and card.trib.answers[0] == {"text": "2"}
        drv.shot("tribulation_back_to_a")
        assert server.sql("select count(*) from quiz_sessions where answered_at is not null")[0][0] == 0

        # ---- a wrong answer (part a wrong, the rest right): one wrong part makes it all wrong
        drv.game.ui.set_value("trib_text_0", "")
        card.trib.answers = [None] * 4
        res = answer(drv, server, card, correct=False)
        assert not res["correct"] and card.given["parts"][0] == {"text": "987654"}
        assert len(card.given["parts"]) == 4 and all(p is not None for p in card.given["parts"])
        assert [p["answer_text"] for p in res["reveal"]["parts"]] == ["2", "Vô số nghiệm", "-3, 2, 0", "Sai"]
        assert res["reveal"]["solution_vi"]
        drv.shot("tribulation_wrong_reveal")
        drv.press(pygame.K_DOWN)
        drv.press(pygame.K_DOWN)
        drv.shot("tribulation_wrong_reveal_scrolled")
        drv.click("math_next")
        drv.wait(lambda: card not in drv.game.scenes, 5, "the card closes")

        # ---- the right answer, every part
        card = open_card(drv, make_question(server, uid, 2))
        res = answer(drv, server, card, correct=True)
        assert res["correct"]
        drv.shot("tribulation_right")
        rows = server.sql("select item_id, qtype, tier, correct from math_answers where user_id=? order by id", (uid,))
        assert rows == [(ITEM, "tribulation", 4, 0), (ITEM, "tribulation", 4, 1)]
        given = json.loads(server.sql("select answer from quiz_sessions where id=?", (card.q["session_id"],))[0][0])
        assert set(given) == {"parts"} and len(given["parts"]) == 4
        drv.click("math_next")
        drv.close()
    finally:
        server.stop()


def test_tribulation_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_tribulation_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "tribulation"
    with tempfile.TemporaryDirectory() as tmp:
        run_tribulation_flow(Path(tmp), out)
    print("screenshots in", out)
