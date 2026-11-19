"""Stage 8 through the real client UI: brew Hồi Khí Đan at the abode's Đan Lô (canh lửa: three
presses, the fire alone decides the quality), wear a Linh Thú that then follows the player, roll
the Linh Thú banner, look at the Lò Rèn (no more Khắc Văn there), the daily tasks and the Linh
Thú Phổ; then, next time the game opens in Trúc Lâm Thôn, buy a herb from Bà Chủ Sạp at the
Sạp Tạp Hóa."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, answer_current_quiz
from client.tests.test_combat_flow import world
from client.tests.test_world_flow import make_account


def top(drv: Driver):
    return drv.game.top


def give(server: ServerProcess, uid: int, item: str, qty: int) -> None:
    server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, ?, ?, 0)", (uid, item, qty))


def abode(drv: Driver):
    from client.scenes.abode import AbodeScene
    return next((s for s in drv.game.scenes if isinstance(s, AbodeScene)), None)


def middle_of_zone(zone: dict, period_ms: int, bar: int) -> float:
    """The first needle time that lands exactly in the middle of the văn hỏa zone, late
    enough that the game counts the press (FireScene ignores anything under 120 ms)."""
    half = max(2, int(period_ms)) // 2
    t = zone["center"] * half / bar                 # the needle climbs 0 -> bar over half a sweep
    while t < 130:
        t += 2 * half                               # the same spot one whole sweep later
    return t


def run_alchemy_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "dan_khach", "Đan Khách")
        import httpx
        h = {"Authorization": f"Bearer {token}"}
        give(server, uid, "dp_hoi_khi", 1)
        give(server, uid, "go_linh_moc", 1)
        give(server, uid, "truc_diep_thao", 1)          # spent by the brew; one more is bought at the shop
        give(server, uid, "muc_tinh", 6)
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, inscriptions) "
                   "values (?, 'kiem_go_dao', 'linh', 0, '[]')", (uid,))
        eid = server.sql("select id from equipment_instances where user_id=?", (uid,))[0][0]
        server.sql("insert into pets(user_id, pet_type, level, equipped) values (?, 'trau', 2, 0)", (uid,))
        pid = server.sql("select id from pets where user_id=?", (uid,))[0][0]
        server.sql("update users set spirit_stones=3000, flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        # ---- the Đan Lô at home
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "dan_khach", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        ab = abode(drv)
        ab.player.x, ab.player.y, ab.player.facing = 34 * 16 + 12, 16 * 16 + 36, "up"
        drv.wait(lambda: ab.target is not None and ab.target[1].props.get("action") == "alchemy", 5, "the furnace")
        drv.press(pygame.K_e)
        drv.wait(lambda: drv.top_is("AlchemyScene") and top(drv).data is not None, 10, "the recipes")
        assert top(drv).data["where"] == "home"
        drv.shot("alchemy_list")
        drv.click("alc_brew_hoi_khi_dan")
        drv.wait(lambda: drv.top_is("FireScene"), 10, "the fire")
        fire = top(drv)
        assert "chars" not in fire.fire and "hanzi" not in fire.fire and len(fire.fire["zones"]) == 3
        from client.engine import alchemy_fire
        drv.fixed_dt = 1 / 60           # the needle is judged to the millisecond: pin the clock
        for rnd in range(3):
            z = fire.fire["zones"][rnd]
            per = fire.fire["periods"][rnd]
            drv.wait(lambda: fire.state == "run" and fire.round == rnd, 10, f"round {rnd} burning")
            # Put the needle one frame short of the middle of the văn hỏa zone: the frame that
            # handles the press adds exactly that frame, so it is judged dead centre. Waiting
            # for the needle instead would race three frames of wall clock against a band
            # about 27 ms wide, which is what used to make this test flaky.
            want = middle_of_zone(z, per, fire.fire["bar"])
            fire.round_ms = want - drv.fixed_dt * 1000
            drv.press(pygame.K_SPACE)
            drv.wait(lambda: fire.state != "run", 3, "the press")
            assert fire.hits[-1] == "perfect", (rnd, fire.hits, fire.timings[-1], want, z)
            if rnd == 0:
                drv.shot("fire_hit")
            drv.click("fire_next")
        drv.fixed_dt = None         # back to real time for the rest of the walk-about
        drv.wait(lambda: fire.state == "result", 10, "the pills")
        res = fire.result
        assert res["hits"] == fire.hits, (res["hits"], fire.hits)       # the server replayed the same fire
        assert fire.hits == ["perfect"] * 3                             # every press was dead centre
        assert res["made"] >= 1 and res["quality"] == "thuong" and res["xp"]["gained"] > 0
        assert all(h != "miss" for h in res["hits"])
        drv.shot("fire_result")
        n = server.sql("select coalesce(sum(quantity), 0) from inventory_items where user_id=? and item_id='hoi_khi_dan'",
                       (uid,))[0][0]
        assert n == res["made"]
        left = server.sql("select coalesce(sum(quantity), 0) from inventory_items where user_id=? and item_id='muc_tinh'",
                          (uid,))[0][0]
        assert left == 4                                # two Mực Tinh went into the fire
        drv.click("fire_done")
        drv.wait_scene("AlchemyScene")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "home")

        # ---- a Linh Thú
        drv.press(pygame.K_o)
        drv.wait(lambda: drv.top_is("PetScene") and (drv.game.state.pets or {}).get("pets"), 10, "the pets")
        drv.click(f"pets_wear_{pid}")
        drv.wait(lambda: drv.game.worn_pet() == "trau", 10, "the buffalo worn")
        drv.shot("pets")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "home again")
        drv.hold([pygame.K_LEFT], 0.6)
        drv.step(20)
        assert ab.pet_follow is not None and ab.pet_follow.kind == "trau"
        drv.shot("pet_follows")
        cult = httpx.get(url + "/cultivation", headers=h).json()
        assert cult["pet"]["pet_type"] == "trau"
        from client.scenes.gacha import GachaScene
        drv.game.push(GachaScene(drv.game, tab="pets"))
        drv.wait(lambda: drv.top_is("GachaScene") and top(drv).banner is not None, 10, "the Linh Thú banner")
        drv.shot("gacha_pets")
        drv.click("g_pet1")
        drv.wait(lambda: top(drv).results is not None, 10, "a pet")
        drv.wait(lambda: top(drv).opened and top(drv).anim_t > 2.0, 10, "the pet appears")
        assert top(drv).results[0]["pet_type"] in drv.game.state.pets.get("looks", {})
        drv.shot("gacha_pet_open")
        drv.click("g_done")
        drv.press(pygame.K_ESCAPE)

        # ---- the Lò Rèn: enhancing only, nothing is carved any more
        from client.scenes.rpg import ForgeScene
        drv.game.push(ForgeScene(drv.game))
        drv.wait(lambda: drv.top_is("ForgeScene") and (top(drv).inv or {}).get("equipment"), 10, "the forge")
        drv.step(3)
        assert drv.has(f"forge_{eid}") and not drv.has(f"forge_ins_{eid}")
        assert "inscriptions" not in top(drv).inv["equipment"][0]
        drv.shot("forge")
        drv.press(pygame.K_ESCAPE)

        # ---- daily tasks and the Linh Thú Phổ
        drv.press(pygame.K_j)
        drv.wait_scene("QuestScene")
        drv.click("quest_tab_daily")
        drv.wait(lambda: len((drv.game.state.quests or {}).get("daily", [])) == 3, 5, "daily tasks")
        drv.shot("quests_daily")
        drv.press(pygame.K_ESCAPE)
        drv.press(pygame.K_l)
        drv.wait_scene("LibraryListScene")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("BooksScene") and top(drv).data is not None, 10, "the shelf of phổ")
        drv.click("lib_open_pet")
        drv.wait_scene("PetBookScene")
        drv.shot("pet_book")
        drv.close()

        # ---- next time the game opens in the village, in front of Bà Chủ Sạp (tile 13, 11)
        server.sql("update characters set zone_id='truc_lam_thon', x=216, y=218, facing='up' where user_id=?", (uid,))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 20, "the village")
        drv.wait_api()

        # ---- the shop
        drv.wait(lambda: world(drv).target is not None and world(drv).action_of(world(drv).target) == "shop", 5,
                 "Bà Chủ Sạp in front")
        drv.press(pygame.K_e)
        drv.wait_scene("DialogScene")
        for _ in range(10):
            if not drv.top_is("DialogScene"):
                break
            drv.press(pygame.K_RETURN)
            drv.step(20)
        drv.wait(lambda: drv.top_is("ShopScene") and top(drv).data is not None, 10, "the shop")
        assert top(drv).data["at_shop"]
        drv.shot("shop_buy")
        drv.click("shop_buy_truc_diep_thao")
        drv.wait_api()
        drv.wait(lambda: server.sql("select coalesce(sum(quantity), 0) from inventory_items where user_id=? and "
                                    "item_id='truc_diep_thao'", (uid,))[0][0] == 1, 5, "bought a herb")
        drv.click("shop_tab_gear")
        drv.shot("shop_gear")
        drv.click("shop_tab_sell")
        drv.shot("shop_sell")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("WorldScene"), 5, "back in the village")
        drv.close()
    finally:
        server.stop()


def test_stage8_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_alchemy_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "stage8"
    with tempfile.TemporaryDirectory() as tmp:
        run_alchemy_flow(Path(tmp), out)
    print("screenshots in", out)
