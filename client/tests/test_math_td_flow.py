"""M10 through the real client UI: Thủ Thành Toán. Open the math hub from the abode, go
through its "Thủ Thành" door, read the towers (the floor-1 tower open, the rest locked with
their reasons), start the level, place towers by answering a question of each tower's area
on the math card (one answer given wrong on purpose: nothing is built), upgrade a tower the
same way, and play the level to its end. The server replays the log before the result
card shows; every answer is in the learning log.

The server runs with BALANCE_PROFILE=dev, which only lets the board run faster (×32).

    python -m client.tests.test_math_td_flow <dir>     # leaves screenshots in <dir>
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.engine import td_sim
from client.tests.driver import ROOT, Driver, ServerProcess, fill_math_answer
from client.tests.test_linh_phong_flow import abode
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "tools"))
import td_bot  # noqa: E402


def top(drv: Driver):
    return drv.game.top


def play_scene(drv: Driver):
    from client.scenes.math_td import MathTdPlayScene
    return next((s for s in drv.game.scenes if isinstance(s, MathTdPlayScene)), None)


def on_board(drv: Driver, sc, wid: str) -> bool:
    """Click a widget of the board, unless a card is up over it (the caller answers it first)."""
    if drv.game.top is not sc or sc.busy or not drv.has(wid):
        return False
    drv.click_at(drv.game.ui.widgets[wid].center)
    return True


def click_card(drv: Driver, sc, word: str | None) -> bool:
    if sc.card == word:
        return True
    if sc.card is not None and not on_board(drv, sc, f"td_card_{sc.words.index(sc.card)}"):
        return False
    return word is None or on_board(drv, sc, f"td_card_{sc.words.index(word)}")


def answer_card(drv: Driver, server: ServerProcess, right: bool, stats: dict, shot: str | None = None) -> dict:
    card = top(drv)
    drv.wait(lambda: card.t >= card.GUARD_SECONDS, 3, "the card is ready for clicks")
    q = card.q
    if shot:
        drv.shot(shot)
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, right)
    drv.wait(lambda: card.result is not None, 10, "the answer is graded")
    res = card.result
    assert bool(res["correct"]) == right, (q["qtype"], res)
    stats["questions"] += 1
    stats["right"] += int(right)
    stats["floors"].add(q["math"]["floor"])
    if shot:
        drv.shot(shot + "_result")
    drv.press(pygame.K_RETURN)                    # "Tiếp": back to the board at once
    drv.wait(lambda: top(drv) is not card, 5, "the card closes")
    return res


def run_math_td_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1, env={"BALANCE_PROFILE": "dev"})
    try:
        url = server.url
        token, uid = make_account(url, "thu_thanh", "Thủ Thành")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "thu_thanh", "server_url": url}))
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
        drv.click("math_hub_td")
        drv.wait(lambda: drv.top_is("MathTdScene") and top(drv).data is not None, 10, "Thủ Thành Toán")
        m = top(drv)
        towers = {t["id"]: t for t in m.data["towers"]}
        # a new player has the towers of floor 1: Đại Số Tuyến Tính's and, since M11 wrote those
        # subjects, Xác Suất và Thống Kê's and Giải Tích's; the rest are locked, each with its reason
        open_now = ["tap_hop", "xac_suat", "gradient"]
        assert [k for k, t in towers.items() if t["available"]] == open_now
        assert all(t["locked_vi"] for k, t in towers.items() if k not in open_now)
        assert not any(towers[k]["locked_vi"] for k in open_now)
        assert drv.has("mtd_tower_vecto") and drv.has("mtd_tower_gradient")
        drv.shot("math_td_map")

        # ---- the level
        drv.click("mtd_start")
        drv.wait(lambda: play_scene(drv) is not None, 10, "the board")
        sc = play_scene(drv)
        drv.wait(lambda: drv.has("mtd_locked_vecto") and drv.has("mtd_locked_ma_tran"), 5, "the locked towers")
        assert not drv.has("mtd_locked_gradient") and not drv.has("mtd_locked_xac_suat")    # open since M11
        stats = {"questions": 0, "right": 0, "floors": set(), "placed_wrong": 0, "placed": 0, "upgraded": 0}
        wrong_once = True
        pending = None                   # what the card being answered is for
        end = time.time() + 300
        result = None
        while time.time() < end:
            t = top(drv)
            name = type(t).__name__
            if name == "TdResultScene":
                result = t.r
                break
            if name == "MathTdCard":
                kind = t.hint
                right = not (wrong_once and pending == "place")
                shot = None
                if pending == "place" and stats["placed"] == 0 and not right:
                    shot = "math_td_place_card"
                before = len(sc.sim.plants)
                answer_card(drv, server, right, stats, shot)
                if pending == "place":
                    if right:
                        assert len(sc.sim.plants) == before + 1, kind
                        stats["placed"] += 1
                    else:
                        assert len(sc.sim.plants) == before        # a wrong answer builds nothing
                        stats["placed_wrong"] += 1
                        wrong_once = False
                pending = None
                continue
            if t is not sc or sc.sending or sc.busy:
                drv.step(1)
                continue
            sim = sc.sim
            if sc.speed < sc.speeds[-1]:
                on_board(drv, sc, "td_speed")
                continue
            if sim.phase == td_sim.BUILD:
                # one upgrade through the card as soon as a tower and the Linh Khí for it are there
                if not stats["upgraded"] and sim.plants:
                    pl = sim.plants[sim.order[0]]
                    cost = sim.cost_to_upgrade(pl)
                    if cost is not None and sim.qi >= cost:
                        if click_card(drv, sc, None) and on_board(drv, sc, f"td_cell_{pl.x}_{pl.y}") \
                                and sc.picked == (pl.x, pl.y):
                            drv.shot("math_td_tower_picked")
                            if on_board(drv, sc, "td_upgrade"):
                                pending = "upgrade"
                                drv.wait(lambda: drv.top_is("MathTdCard"), 10, "the upgrade question")
                                answer_card(drv, server, True, stats, "math_td_upgrade_card")
                                pending = None
                                assert pl.level == 2 and sc.events[-1]["k"] == "up"
                                stats["upgraded"] += 1
                        continue
                acts = td_bot.decide(sim, allow_upgrade=False)
                if acts and acts[0]["k"] == "place":
                    a = acts[0]
                    if click_card(drv, sc, a["w"]) and on_board(drv, sc, f"td_cell_{a['x']}_{a['y']}"):
                        pending = "place"
                        drv.wait(lambda: drv.top_is("MathTdCard"), 10, "the place question")
                        if stats["placed"] == 1 and not stats["upgraded"]:
                            drv.shot("math_td_board_build")
                    continue
                if click_card(drv, sc, None):
                    on_board(drv, sc, "td_wave")
                continue
            if sim.phase == td_sim.WAVE and sim.wave >= 3 and len(sim.monsters) >= 3 and not stats.get("shot"):
                stats["shot"] = True
                drv.shot("math_td_wave")
            drv.step(1)
        assert result is not None, f"the level did not end in time: {sc.sim.summary()}"
        drv.shot("math_td_result")
        assert result["result"] in ("won", "lost") and result["result"] == "won", result
        assert result["stars"] >= 1 and result["rewards"].get("spirit_stones")
        assert stats["placed"] >= 1 and stats["placed_wrong"] == 1 and stats["upgraded"] == 1, stats
        assert stats["floors"] == {1}                      # a floor-1 player only meets floor-1 questions
        rows = server.sql("select count(*), sum(correct) from math_answers where user_id=? and run_id is null", (uid,))
        assert rows[0][0] == stats["questions"] and rows[0][1] == stats["right"], (rows, stats)
        n = server.sql("select count(*) from quiz_sessions where user_id=? and context='math_td'", (uid,))[0][0]
        assert n == stats["questions"]
        assert server.sql("select stars from td_progress where user_id=? and level_id='math_td_01'", (uid,))[0][0] >= 1
        drv.click("td_result_map")
        drv.wait(lambda: drv.top_is("MathTdScene") and top(drv).level("math_td_01")["stars"] >= 1, 10,
                 "back on the level screen")
        drv.shot("math_td_map_after")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 5, "back in the hub")
        drv.close()
    finally:
        server.stop()


def test_math_td_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_math_td_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "math_td"
    with tempfile.TemporaryDirectory() as tmp:
        run_math_td_flow(Path(tmp), out)
    print("screenshots in", out)
