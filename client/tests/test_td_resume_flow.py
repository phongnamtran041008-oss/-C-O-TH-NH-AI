"""Stage 7 through the real client UI, part 2: the Thủ Thư in Trúc Lâm Thôn opens the math
scrolls; under them, on the shelf of phổ, wear a title and an avatar frame, buy an đan phương
from her shelf, read the Bảo Vật Phổ; then start a level of Thủ
Thành Toán, build towers by answering their questions, start a wave, close the game in the
middle, open it again and continue the same run from the saved log to the end."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.engine import td_sim
from client.tests.driver import Driver, ServerProcess
from client.tests.test_combat_flow import world
from client.tests.test_linh_phong_flow import give
from client.tests.test_math_td_flow import answer_card, click_card, on_board, play_scene, top
from client.tests.test_td_flow import play_level
from client.tests.test_world_flow import make_account

import math_td_bot  # noqa: E402  (tools/ is on the path: test_td_flow put it there)


def open_td(drv: Driver):
    from client.scenes.math_td import MathTdScene
    drv.game.push(MathTdScene(drv.game))
    drv.wait(lambda: drv.top_is("MathTdScene") and top(drv).data is not None, 10, "Thủ Thành Toán")
    return top(drv)


def run_resume_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1, env={"BALANCE_PROFILE": "dev"})
    try:
        url = server.url
        token, uid = make_account(url, "thu_thu_khach", "Khách Thư Các")
        import httpx
        h = {"Authorization": f"Bearer {token}"}
        httpx.get(url + "/quests", headers=h).raise_for_status()
        server.sql("update users set spirit_stones=3000, flags=? where id=?",
                   (json.dumps({"tutorial": 5, "titles": ["Kẻ Săn Mực"], "frames": ["khung_muc"]}), uid))
        give(server, uid, "hoi_huyet_dan", 2)    # a treasure for the Bảo Vật Phổ
        # in front of the Thủ Thư (tile 41, 9)
        server.sql("update characters set zone_id='truc_lam_thon', x=664, y=186, facing='up' where user_id=?", (uid,))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "thu_thu_khach",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 20, "the village")
        drv.wait_api()
        drv.wait(lambda: world(drv).target is not None and world(drv).action_of(world(drv).target) == "library", 5,
                 "the Thủ Thư in front")
        drv.press(pygame.K_e)
        drv.wait_scene("DialogScene")
        for _ in range(10):
            if not drv.top_is("DialogScene"):
                break
            drv.press(pygame.K_RETURN)
            drv.step(20)
        drv.wait(lambda: drv.top_is("LibraryListScene") and top(drv).data is not None, 10, "the math scrolls")
        drv.shot("library_scrolls")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("BooksScene") and top(drv).data is not None, 10, "the shelf of phổ")
        lib = top(drv)
        assert lib.data["at_desk"]
        # wear the title and the frame
        drv.click("lib_title_1")
        drv.wait(lambda: lib.data.get("title") == "Kẻ Săn Mực", 5, "title worn")
        drv.click("lib_frame_1")
        drv.wait(lambda: lib.data.get("frame") == "khung_muc", 5, "frame worn")
        assert drv.game.state.me["title"] == "Kẻ Săn Mực" and drv.game.state.me["frame"] == "khung_muc"
        drv.shot("library_badges")
        # buy an đan phương from the shelf
        drv.click("lib_shop")
        drv.wait_scene("BooksShopScene")
        drv.click("lib_buy_dp_hoi_khi")
        drv.wait_api()
        drv.wait(lambda: next(s for s in lib.data["shop"] if s["item_id"] == "dp_hoi_khi")["have"] == 1, 5, "bought")
        drv.shot("library_shop")
        have = server.sql("select sum(quantity) from inventory_items where user_id=? and item_id='dp_hoi_khi'", (uid,))
        assert have[0][0] == 1
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("BooksScene")
        drv.click("lib_open_treasure")
        drv.wait(lambda: drv.top_is("TreasureBookScene") and top(drv).data is not None, 5, "Bảo Vật Phổ")
        tb = top(drv).data
        assert any(e["id"] == "hoi_huyet_dan" and e["found"] for e in tb["entries"]) and tb["found"] >= 1
        drv.shot("bao_vat_pho")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("BooksScene")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("WorldScene"), 5, "back in the village")
        drv.shot("hud_title_frame")

        # ---- a level, closed in the middle of a wave
        open_td(drv)
        drv.click("mtd_start")
        drv.wait(lambda: play_scene(drv) is not None, 10, "the board")
        sc = play_scene(drv)
        stats = {"questions": 0, "right": 0, "floors": set()}
        while sc.speed < sc.speeds[-1] or sc.sim.phase == td_sim.BUILD:
            t = top(drv)
            if type(t).__name__ == "MathTdCard":
                answer_card(drv, server, True, stats)
            elif t is sc and not sc.busy and sc.speed < sc.speeds[-1]:
                on_board(drv, sc, "td_speed")
            elif t is sc and not sc.busy and len(sc.sim.plants) < 2:
                acts = math_td_bot.decide(sc.sim, allow_upgrade=False)
                if acts and click_card(drv, sc, acts[0]["w"]):
                    on_board(drv, sc, f"td_cell_{acts[0]['x']}_{acts[0]['y']}")
            elif t is sc and not sc.busy and click_card(drv, sc, None):
                on_board(drv, sc, "td_wave")
            else:
                drv.step(1)
        drv.wait(lambda: sc.sim.step_n > 40 and sc.saved == len(sc.events) and not sc.saving, 15, "log saved")
        sc.speed = 1                       # (keep the board where it is while the game closes)
        saved_events = list(sc.events)
        towers = sorted((c, pl.word) for c, pl in sc.sim.plants.items())
        assert towers
        drv.shot("td_before_close")
        drv.close()

        # ---- the game is opened again
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 20, "the village again")
        drv.wait_api()
        m = open_td(drv)
        assert m.data["active_run"] and m.data["active_run"]["level_id"] == "math_td_01"
        drv.shot("td_resume_offer")
        drv.click("mtd_resume")
        drv.wait(lambda: play_scene(drv) is not None, 10, "the board again")
        sc = play_scene(drv)
        assert sc.events == saved_events
        assert sorted((c, pl.word) for c, pl in sc.sim.plants.items()) == towers
        assert sc.sim.step_n >= saved_events[-1]["s"] and sc.sim.wave == sum(e["k"] == "wave" for e in saved_events)
        res = play_level(drv, server, stats)
        assert res["result"] == "won", res
        rows = dict(server.sql("select level_id, stars from td_progress where user_id=?", (uid,)))
        assert rows.get("math_td_01", 0) >= 1
        assert server.sql("select count(*) from td_runs where user_id=?", (uid,))[0][0] == 0
        drv.click("td_result_map")
        drv.close()
    finally:
        server.stop()


def test_td_resume_and_library_shop_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_resume_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "td_resume"
    with tempfile.TemporaryDirectory() as tmp:
        run_resume_flow(Path(tmp), out)
    print("screenshots in", out)
