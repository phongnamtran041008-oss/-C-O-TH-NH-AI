"""The tower defence through the real client UI, from the village: walk up to the Cổng Thủ
Thành in Trúc Lâm Thôn and press E. The gate's first words come up, then Thủ Thành Toán (the
math tower defence: there is no other). Play its first level to the end by clicking the
tower cards and the board and answering every question on the math card, all right. The
server replays the log before the result shows; the Mặc Quái met are then in the Yêu Quái
Phổ of the Tàng Thư Các.

The server runs with BALANCE_PROFILE=dev, which only allows the board to run faster (×32);
the levels and numbers are the real ones."""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.engine import td_sim
from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_combat_flow import world
from client.tests.test_math_td_flow import answer_card, click_card, on_board, play_scene, top
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "tools"))
import math_td_bot  # noqa: E402


def play_level(drv: Driver, server: ServerProcess, stats: dict, shot: str | None = None) -> dict:
    """Play the open board to the end like a careful beginner, every answer right; returns
    the server's result."""
    drv.wait(lambda: play_scene(drv) is not None, 10, "the board")
    sc = play_scene(drv)
    end = time.time() + 300
    while time.time() < end:
        t = top(drv)
        name = type(t).__name__
        if name == "MathTdResultScene":
            return t.r
        if name == "MathTdCard":
            answer_card(drv, server, True, stats)
            continue
        if t is not sc or sc.sending or sc.busy:
            drv.step(1)
            continue
        sim = sc.sim
        if sc.speed < sc.speeds[-1]:          # fast forward (the dev profile allows ×32)
            on_board(drv, sc, "td_speed")
            continue
        if sim.phase == td_sim.BUILD:
            acts = math_td_bot.decide(sim, allow_upgrade=False)
            if acts:
                a = acts[0]
                if click_card(drv, sc, a["w"]) and on_board(drv, sc, f"td_cell_{a['x']}_{a['y']}"):
                    drv.wait(lambda: drv.top_is("MathTdCard"), 10, "the place question")
                continue
            if click_card(drv, sc, None):
                on_board(drv, sc, "td_wave")
            continue
        if shot and sim.phase == td_sim.WAVE and sim.wave >= 2 and len(sim.monsters) >= 3:
            drv.shot(shot)
            shot = None
        drv.step(1)
    raise AssertionError(f"level did not end in time: {play_scene(drv).sim.summary()}")


def run_td_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1, env={"BALANCE_PROFILE": "dev"})
    try:
        url = server.url
        token, uid = make_account(url, "thu_thanh_thon", "Thủ Thành Thôn")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        # in Trúc Lâm Thôn, just below the Cổng Thủ Thành
        server.sql("update characters set zone_id='truc_lam_thon', x=724, y=438, facing='up' where user_id=?", (uid,))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "thu_thanh_thon",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 20, "the village")
        drv.wait_api()
        drv.wait(lambda: world(drv).target is not None and world(drv).action_of(world(drv).target) == "td", 5,
                 "the Cổng Thủ Thành in front")
        drv.press(pygame.K_e)
        drv.wait_scene("DialogScene")
        drv.shot("td_gate_intro")
        for _ in range(10):
            if not drv.top_is("DialogScene"):
                break
            drv.press(pygame.K_RETURN)
            drv.step(20)
        drv.wait(lambda: drv.top_is("MathTdScene") and top(drv).data is not None, 10, "Thủ Thành Toán")
        m = top(drv)
        assert [t["id"] for t in m.data["towers"] if t["available"]] == ["tap_hop", "xac_suat", "gradient"]
        assert m.level("math_td_01")["unlocked"]
        drv.shot("td_gate_map")

        stats = {"questions": 0, "right": 0, "floors": set()}
        drv.click("mtd_start")
        res = play_level(drv, server, stats, shot="td_gate_board")
        assert res["result"] == "won" and res["stars"] >= 1, res
        assert stats["questions"] == stats["right"] > 0 and stats["floors"] == {1}, stats
        n = server.sql("select count(*) from quiz_sessions where user_id=? and context='math_td'", (uid,))[0][0]
        assert n == stats["questions"]
        assert server.sql("select count(*) from quiz_sessions where user_id=? and context='td'", (uid,))[0][0] == 0
        drv.shot("td_gate_result")
        drv.click("td_result_map")
        drv.wait(lambda: drv.top_is("MathTdScene") and top(drv).level("math_td_01")["stars"] >= 1, 10,
                 "back on the level screen")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("WorldScene"), 5, "back in the village")

        # ---- the Mặc Quái met are in the Yêu Quái Phổ (Tàng Thư Các, the L key)
        drv.press(pygame.K_l)
        drv.wait(lambda: drv.top_is("LibraryScene") and top(drv).data is not None, 10, "Tàng Thư Các")
        assert {b["id"]: b for b in top(drv).data["books"]}["monster"]["found"] >= 1
        drv.click("lib_open_monster")
        drv.wait(lambda: drv.top_is("MonsterBookScene") and top(drv).data is not None, 5, "Yêu Quái Phổ")
        assert any(e["id"].startswith("td_") and e["found"] for e in top(drv).data["entries"])
        drv.shot("td_monster_book")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("LibraryScene")
        drv.press(pygame.K_ESCAPE)
        drv.close()
    finally:
        server.stop()


def test_the_village_gate_opens_thu_thanh_toan():
    with tempfile.TemporaryDirectory() as tmp:
        run_td_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "td"
    with tempfile.TemporaryDirectory() as tmp:
        run_td_flow(Path(tmp), out)
    print("screenshots in", out)
