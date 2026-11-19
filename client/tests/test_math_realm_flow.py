"""M10 through the real client: alone at the Cổng Bí Cảnh in Trúc Lâm Thôn, the player opens the
"Bí cảnh toán" tab, enters Toán Trận Bí Cảnh without a party, and plays the whole run on the
keyboard and mouse: in each Trận Nhãn room they stand on seals and answer the math question
each one asks (on the math card, at their own floor), fight the room's Mặc Quái, and at the end
break Nghiên Ma's big shield with their bài tổng hợp until it falls.

    python -m client.tests.test_math_realm_flow OUT_DIR      # with screenshots
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
from client.tests.test_combat_flow import walk_to, world
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the map the server ships

from app.realtime import maps  # noqa: E402

REALM = "toan_tran"
FLOOR = 3                         # the player's own floor: the frontier of Đại Số once its first node (floor 1)
                                  # is done is the node it opens, on floor 3 (floor 2 holds only an optional node)


def card_open(drv: Driver) -> bool:
    return drv.top_is("MathCombatQuizScene")


def answer_open_card(drv: Driver, server: ServerProcess, asked: list) -> None:
    card = drv.game.top
    if card.result:              # only showing the result of the last answer: it closes itself
        drv.wait(lambda: drv.game.top is not card, 8, "the card closes")
        return
    asked.append(card.q["math"])
    res = answer_card(drv, server, correct=True)
    assert res["correct"], res
    # (the boss may ask its next phase at once: another card, not this one)
    drv.wait(lambda: drv.game.top is not card, 8, "the card closes")


def go(drv: Driver, server: ServerProcess, tx: float, ty: float, asked: list, near: float = 6.0) -> None:
    """Walk to a point over the room's real floor (the realm bots' breadth-first route),
    answering any card that opens on the way."""
    from tests.realm_bot import path as route_over
    col = maps.load("bi_canh").collider
    end = time.time() + 30
    while time.time() < end:
        if card_open(drv):
            if not drv.game.top.result:
                drv.shot(f"question_{len(asked)}")
            answer_open_card(drv, server, asked)
            continue
        ws = world(drv)
        if math.hypot(tx - ws.player.x, ty - ws.player.y) < near:
            return
        route = route_over(col, (ws.player.x, ws.player.y), (tx, ty)) or [(tx, ty)]
        for wx, wy in route[5::6] + [(tx, ty)]:
            if card_open(drv):
                break
            walk_to(drv, wx, wy, near=near, timeout=3)
    raise AssertionError(f"could not reach ({tx:.0f}, {ty:.0f})")


def seal_step(drv: Driver, server: ServerProcess, asked: list) -> bool:
    """Stand on an unbroken seal until it asks. False when no seal is left to break."""
    rv = world(drv).realm
    pz = rv.puzzle or {}
    if pz.get("solved"):
        return False
    open_ = {s["name"] for s in pz.get("seals", []) if not s["broken"]}
    objs = [o for o in rv.room_objs() if o.name in open_]
    if not objs:
        return False
    p = world(drv).player
    o = min(objs, key=lambda o: math.hypot(o.x + o.w / 2 - p.x, o.y + o.h / 2 - p.y))
    before = len(asked)
    go(drv, server, o.x + o.w / 2, o.y + o.h / 2, asked)
    if len(asked) > before:          # it asked the moment we stepped on it, and was answered on the way
        return True

    def broken() -> bool:
        return any(s["name"] == o.name and s["broken"] for s in (world(drv).realm.puzzle or {}).get("seals", []))
    drv.wait(lambda: card_open(drv) or broken(), 6, "the seal asks")
    if card_open(drv):
        drv.shot(f"seal_question_{len(asked)}")
        answer_open_card(drv, server, asked)
    return True


def fight_step(drv: Driver, server: ServerProcess, asked: list) -> bool:
    """One swing at the nearest monster (or the answer to its card). False when none is left."""
    if card_open(drv):
        answer_open_card(drv, server, asked)
        return True
    ws = world(drv)
    alive = [e for e in ws.entities.values() if e.kind == "m" and e.alive]
    if not alive:
        return False
    m = min(alive, key=lambda e: math.hypot(e.pos[0] - ws.player.x, e.pos[1] - ws.player.y))
    if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) >= 30:
        walk_to(drv, m.pos[0], m.pos[1] + 6, near=18, timeout=3)
        return True
    drv.click_at(drv.game.display.to_window(*ws.world_to_screen(m.pos[0], m.pos[1] - 8)))
    drv.step(6)
    drv.press(pygame.K_SPACE)
    drv.step(6)
    return True


def run_math_realm_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "khach_toan", "Khách Toán Trận")
        gx, gy = maps.load("truc_lam_thon").interacts["realm"]
        server.sql("update characters set zone_id='truc_lam_thon', x=?, y=?, facing='up', hp=400 where user_id=?",
                   (gx, gy + 14, uid))
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        for item, slot in (("gay_truc", "weapon"), ("mac_anh_bao", "body")):   # about the rules, not the fight
            server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, inscriptions, "
                       "equipped_slot) values (?, ?, 'thien', 5, '[]', ?)", (uid, item, slot))
        for n in range(1, FLOOR):     # the player has passed the floors below their own
            server.sql("insert into math_runs(user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
                       "combo, best_combo, asked, correct, review_asked, xp_gained, passed, started_at, ended_at) "
                       "values (?, 'dai_so_tuyen_tinh', ?, 'trial', 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, datetime('now'), "
                       "datetime('now'))", (uid, n))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "khach_toan",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).zone_id == "truc_lam_thon" and world(drv).joined,
                 20, "Trúc Lâm Thôn")
        drv.wait_api()
        # ---- the gate: the math tab, alone
        drv.wait(lambda: world(drv).target is not None and world(drv).action_of(world(drv).target) == "realm", 5,
                 "standing at the Cổng Bí Cảnh")
        drv.press(pygame.K_e)
        drv.wait(lambda: drv.top_is("RealmGateScene") and drv.game.top.data is not None, 10, "the gate")
        drv.click("rg_tab_math")
        r = next(r for r in drv.game.top.data["math_realms"] if r["id"] == REALM)
        assert r["math"] and r["floor"] == FLOOR and r["open"], r
        drv.shot("math_gate")
        drv.click(f"rg_enter_{REALM}")
        drv.wait(lambda: world(drv) is not None and world(drv).zone_id == "bi_canh" and world(drv).realm.room
                 is not None, 20, "the first room")
        rv = world(drv).realm
        assert rv.run["math"] and rv.room["kind"] == "seal" and rv.place == "compose"
        drv.step(20)
        drv.shot("seal_room")
        asked: list[dict] = []
        rooms_cleared = 0
        shot_once: set[str] = set()
        end = time.time() + 420
        while time.time() < end:
            rv = world(drv).realm
            if rv.ended:
                break
            if rv.cleared_at is not None:   # the doors open: on to the next room
                i = rv.room["i"]
                rooms_cleared = max(rooms_cleared, i + 1)
                if i == 0:
                    drv.shot("room_cleared")
                drv.wait(lambda: world(drv).realm.ended or world(drv).realm.room["i"] > i, 15, "the next room")
                if not world(drv).realm.ended:
                    drv.step(20)
                    drv.shot(f"room{world(drv).realm.room['i'] + 1}_{world(drv).realm.room['kind']}")
                continue
            if card_open(drv):
                answer_open_card(drv, server, asked)
            elif rv.kind == "seal" and seal_step(drv, server, asked):
                pass
            elif not fight_step(drv, server, asked):
                drv.step(5)
            if rv.kind == "boss" and "boss" not in shot_once:
                shot_once.add("boss")
                drv.step(10)
                drv.shot("boss")
        rv = world(drv).realm
        assert rooms_cleared >= 1, "the first room was never cleared"
        assert rv.ended and rv.ended["result"] == "won", (rv.ended, rv.room and rv.room["kind"], rv.puzzle)
        for _ in range(20):
            drv.step(1)
        drv.shot("result")
        # every question came from the player's own floor, whoever asked it
        assert asked and {a["floor"] for a in asked} == {FLOOR}, asked
        assert {a["realm_asker"] for a in asked} >= {"seal", "boss"}, {a["realm_asker"] for a in asked}
        rows = server.sql("select floor, run_id from math_answers where user_id=?", (uid,))
        assert rows and all(f == FLOOR and run is None for f, run in rows), rows
        stages = sorted(x[0] for x in server.sql("select stage from realm_claims where user_id=?", (uid,)))
        assert stages == ["chest", "room0", "room1", "room2"], stages
        drv.close()
    finally:
        server.stop()


def test_math_realm_flow(tmp_path):
    run_math_realm_flow(tmp_path)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("screenshots_math_realm")
    run_math_realm_flow(Path(tempfile.mkdtemp(prefix="kvtt_mrealm_")), out)
    print("screenshots in", out)
