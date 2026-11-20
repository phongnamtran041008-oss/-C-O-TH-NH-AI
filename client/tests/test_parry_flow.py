"""The open-world fight rule through the real client UI (world_plan.json "combat": questions
only when a monster hits you), in Loạn Số Cốc against an elite quái lỗi sai (Ảnh Trùng Ma: it
wears a Mặc Thuẫn and lives through a counter hit):

  * hitting it asks nothing; it answers with a telegraphed blow whose zone fills on the ground;
  * Né Đòn (Shift, open from Luyện Khí tầng 1) dashes out of the zone: no blow, no card;
  * standing in it, the blow lands: the fight pauses for us and its card asks about the
    monster's own micro-skill (ParryCard);
  * a right answer is a Phản Đòn: no damage, the monster takes the counter and is stunned;
  * inside the rest window a blow lands for half and asks nothing;
  * after it, a wrong answer lets the blow land in full and the card shows the solution.

    python -m client.tests.test_parry_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_combat_flow import CARD, nearest, walk_to, world
from client.tests.test_math_combat_flow import VALLEY, answer_card
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the map and the plan the server ships

from app.learning import math_tree  # noqa: E402
from app.realtime import maps  # noqa: E402
from app.systems import catalog  # noqa: E402

PLAN = math_tree.world_plan()["combat"]
ELITE = "dstt_anh_trung_ma"      # an elite of floor 1: a Mặc Thuẫn, and cone / circle / line blows


class FxSpy:
    """Every effect the world scene was sent."""

    def __init__(self, ws):
        self.events: list[dict] = []
        on_fx = ws.on_fx

        def spy(ev):
            self.events.append(dict(ev))
            on_fx(ev)
        ws.on_fx = spy

    def of(self, k: str, **match) -> list[dict]:
        return [e for e in self.events if e.get("k") == k and all(e.get(a) == b for a, b in match.items())]


def hp(drv) -> int:
    return int(drv.game.state.character.get("hp") or 0)


def wait_for_tele(drv, spy: FxSpy, mid: str, after: int, timeout: float = 8.0) -> dict:
    drv.wait(lambda: len(spy.of("tele", id=mid)) > after, timeout, "the monster winds up")
    return spy.of("tele", id=mid)[-1]


def run_parry_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_pd", "Phản Đòn")
        vmap = maps.load(VALLEY)
        area = next(a for a in vmap.monster_areas if a.props.get("monster") == ELITE)
        server.sql("update characters set zone_id=?, x=?, y=?, realm='luyen_khi', realm_stage=1 where user_id=?",
                   (VALLEY, area.x + area.w / 2, area.y + area.h / 2, uid))
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_pd",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "Loạn Số Cốc")
        drv.wait_api()
        ws = world(drv)
        assert ws.zone_id == VALLEY
        assert ws.rule and ws.rule["rule"] == "on_hit" and ws.dodge_open(), ws.rule
        spy = FxSpy(ws)
        info = catalog.monsters()[ELITE]

        # ---- the elite (it wears a Mặc Thuẫn) comes at us; hitting it asks nothing, it winds up a blow
        drv.wait(lambda: nearest(ws, ELITE) is not None, 10, f"a {ELITE}")
        m = nearest(ws, ELITE)
        assert m.shield, "an elite keeps its Mặc Thuẫn in the wild"
        walk_to(drv, m.pos[0], m.pos[1], near=20)
        drv.click_at(drv.game.display.to_window(*ws.world_to_screen(m.pos[0], m.pos[1] - 8)))
        tele = wait_for_tele(drv, spy, m.id, 0)
        assert not drv.top_is(CARD), "hitting a monster asks nothing"
        assert tele.get("sh") in PLAN["telegraph"]["by_rank"]["elite"], tele
        drv.step(8)
        drv.shot("telegraph")

        # ---- Né Đòn away from it, out of the zone: nothing lands, no card
        x0, y0 = ws.player.x, ws.player.y
        hp0 = hp(drv)
        away_x, away_y = x0 - m.pos[0], y0 - m.pos[1]
        held = []
        if abs(away_x) > 3:
            held.append(pygame.K_d if away_x > 0 else pygame.K_a)
        if abs(away_y) > 3:
            held.append(pygame.K_s if away_y > 0 else pygame.K_w)
        drv.keys.held = set(held or [pygame.K_s])
        drv.press(pygame.K_LSHIFT)
        drv.keys.held = set()
        assert ws.dodge_ready > drv.game.now, "the dash went out"
        drv.step(4)
        drv.shot("dodge")
        # (the dash length itself is pinned by server/tests/test_combat_on_hit.py; against a wall the
        # dash goes nowhere, and its moment of invulnerability still beats the blow)
        assert math.hypot(ws.player.x - x0, ws.player.y - y0) > 0
        end = time.time() + PLAN["telegraph_min_seconds"] + 0.6
        while time.time() < end:
            drv.step(3)
            assert not drv.top_is(CARD), "a dodged blow asks nothing"
        drv.wait(lambda: spy.of("dodge", id=f"p{drv.game.state.me['id']}"), 3, "the server saw the dash")
        assert hp(drv) >= hp0

        # ---- stand in its zone: the blow lands and the card asks about the monster's own skill
        walk_to(drv, m.pos[0], m.pos[1], near=12)
        drv.wait(lambda: drv.top_is(CARD), 12, "the card of a landed blow")
        card = drv.game.top
        foe = ws.entities.get(card.monster_id) or m      # the one whose blow landed
        assert card.monster_id == m.id and card.hit.get("dmg", 0) > 0, card.hit
        assert card.q["context"] == "math_combat" and card.q["math"]["skill"] == info["skill"], card.q["math"]
        hp_asked = hp(drv)
        drv.step(6)
        drv.shot("question_on_hit")

        # ---- a right answer: Phản Đòn
        res = answer_card(drv, server, correct=True)
        c = res["combat"]
        assert c["parry"] and c["damage"] > 0 and c["stun"] == PLAN["right_answer"]["stun_seconds"], c
        assert c["shield_broken"], "the Phản Đòn breaks the elite's Mặc Thuẫn"
        drv.wait(lambda: spy.of("parry", id=m.id), 4, "the parry effect")
        drv.step(3)
        drv.shot("phan_don_card")
        drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes by itself")
        drv.step(2)
        drv.shot("phan_don")
        assert hp(drv) >= hp_asked, "a Phản Đòn takes no damage"
        rows = server.sql("select skill_id, correct, run_id from math_answers where user_id=?", (uid,))
        assert rows == [(info["skill"], 1, None)], rows

        # ---- the rest window: a blow lands for half and asks nothing
        rest_end = time.time() + c["rest"]
        before = hp(drv)
        while time.time() < rest_end - 0.5 and hp(drv) >= before:
            walk_to(drv, foe.pos[0], foe.pos[1], near=12, timeout=0.5)
            drv.step(5)
            assert not drv.top_is(CARD), "no question inside the rest window"
        assert hp(drv) < before, "a blow inside the rest window still lands (for half)"

        # ---- after it, a wrong answer: the blow lands in full and the solution shows
        while time.time() < rest_end + 0.3:
            drv.step(5)
        drv.wait(lambda: drv.top_is(CARD), 15, "a card again after the rest")
        before = hp(drv)
        res = answer_card(drv, server, correct=False)
        c = res["combat"]
        assert not c["parry"] and c["damage_taken"] > 0 and c["shows_solution"], c
        drv.step(8)
        drv.shot("guard_break_solution")
        drv.wait(lambda: hp(drv) < before, 5, "the blow lands")
        rows = server.sql("select correct from math_answers where user_id=? order by id", (uid,))
        assert [r[0] for r in rows] == [1, 0], rows
        drv.close()
    finally:
        server.stop()


def test_parry_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_parry_") as tmp:
        run_parry_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "parry"
    with tempfile.TemporaryDirectory() as tmp:
        run_parry_flow(Path(tmp), out)
    print("screenshots in", out)
