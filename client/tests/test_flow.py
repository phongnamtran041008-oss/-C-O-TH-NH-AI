"""Acceptance test of a new player's first minutes (spec 20): register, create a character,
land in the Động Phủ (no garden: hive, mat, furnace, pond, Thiên Cơ Đài, gate), walk around,
open the bag, take the daily free roll (a bee egg), look at the shelf of phổ, quit and come
back to the same place, then walk out through the bamboo gate into Trúc Lâm Thôn."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess


def advance_dialogs(drv: Driver) -> None:
    while drv.top_is("DialogScene"):
        drv.press(pygame.K_RETURN)
        drv.step(3)


def run_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        drv = Driver(server.url, workdir, shots)
        drv.step(10)
        drv.shot("menu")
        drv.click("menu_start")
        drv.wait_scene("LoginScene")
        drv.click("tab_register")
        drv.click("rg_user")
        drv.type("detu_01")
        drv.click("rg_pass")
        drv.type("matkhau1")
        drv.click("rg_pass2")
        drv.type("matkhau1")
        drv.shot("register")
        drv.click("btn_register")
        drv.wait_scene("RecoveryCodeScene")
        code = drv.game.top.code
        assert len(code) == 14
        drv.shot("recovery_code")
        drv.click("btn_saved")
        drv.wait_scene("CreateCharScene")
        drv.click("cc_name")
        drv.type("Tiểu Trúc")
        drv.step(30)
        drv.shot("create_character")
        drv.click("cc_go")
        drv.wait(lambda: "AbodeScene" in drv.scene_names(), 10, "abode")
        drv.wait_api()
        advance_dialogs(drv)
        abode = drv.game.scenes[0]
        assert type(abode).__name__ == "AbodeScene" and drv.game.top is abode
        assert not hasattr(abode, "plots"), "the word garden is gone"
        drv.shot("abode")

        # walk around the abode
        x0, y0 = abode.player.x, abode.player.y
        drv.hold([pygame.K_w], 0.8)
        drv.hold([pygame.K_a], 0.4)
        assert abode.player.y < y0 - 20 and abode.player.x < x0 - 10, "player should have moved"
        drv.shot("walking")

        # the bag: items and gear only
        drv.press(pygame.K_TAB)
        drv.wait_scene("BagScene")
        drv.wait(lambda: drv.game.top.inv is not None, 5, "the inventory")
        assert drv.has("bag_tab_items") and drv.has("bag_tab_gear") and not drv.has("bag_tab_seeds")
        drv.shot("bag")
        drv.press(pygame.K_ESCAPE)

        # Thiên Cơ Các: the daily free roll is a bee egg, it costs nothing and goes to the bag
        stones = drv.game.state.me["spirit_stones"]
        eggs = "select coalesce(sum(quantity), 0) from inventory_items where user_id=1 and item_id like 'trung_ong%'"
        eggs_before = server.sql(eggs)[0][0]
        drv.press(pygame.K_g)
        drv.wait_scene("GachaScene")
        drv.wait_api()
        assert drv.game.top.tab == "bees" and not drv.has("g_tab_seeds")
        drv.shot("gacha")
        drv.click("g_free")
        drv.wait(lambda: drv.game.top.results is not None, 5, "gacha results")
        drv.wait(lambda: drv.game.top.anim_t > 0.5, 5, "shaking")
        drv.shot("gacha_opening")
        drv.wait(lambda: drv.game.top.anim_t > 2.4, 8, "revealed")
        drv.shot("gacha_revealed")
        drv.click("g_done")
        drv.press(pygame.K_ESCAPE)
        drv.wait_api()
        assert drv.game.state.me["spirit_stones"] == stones
        assert server.sql(eggs)[0][0] == eggs_before + 1

        # B: the shelf of phổ (monsters, bees, fish, treasures, Linh Thú)
        drv.press(pygame.K_b)
        drv.wait_scene("BooksScene")
        drv.wait(lambda: drv.game.top.data is not None, 5, "the shelf of phổ")
        drv.shot("books")
        drv.press(pygame.K_ESCAPE)

        pos = (round(abode.player.x, 1), round(abode.player.y, 1), abode.player.facing)
        stones = drv.game.state.me["spirit_stones"]
        drv.close()

        # come back: auto-login from session.json, same place
        drv2 = Driver(server.url, workdir, shots)
        drv2.n_shots = drv.n_shots
        drv2.click("menu_start")
        drv2.wait(lambda: "AbodeScene" in drv2.scene_names(), 10, "abode again")
        drv2.wait_api()
        ab2 = drv2.game.scenes[0]
        assert (round(ab2.player.x, 1), round(ab2.player.y, 1), ab2.player.facing) == pos
        assert drv2.game.state.me["spirit_stones"] == stones
        assert not drv2.top_is("DialogScene")
        drv2.shot("back_again")

        # out through the bamboo gate into the village
        drv2.wait(lambda: drv2.game.net is not None and drv2.game.net.online, 10, "world connection")
        spawn = ab2.map.find("spawn")[0]
        ab2.player.x, ab2.player.y, ab2.player.facing = float(spawn.x), float(spawn.y), "down"
        drv2.hold([pygame.K_s], 0.9)
        assert ab2.target and ab2.target[1].props.get("action") == "exit", ab2.target
        drv2.press(pygame.K_e)
        drv2.wait(lambda: drv2.game.world_scene() is not None and drv2.game.world_scene().joined, 10, "village")
        assert drv2.game.world_scene().zone_id == "truc_lam_thon"
        drv2.step(10)
        drv2.shot("village")
        drv2.close()
        saved = json.loads((workdir / "session.json").read_text())
        assert saved["username"] == "detu_01"
    finally:
        server.stop()


def test_new_player_flow():
    with tempfile.TemporaryDirectory() as tmp:
        run_flow(Path(tmp))


def test_tests_leave_no_settings_in_game_folder():
    """Regression: a test run once saved its random server port into client/config.json,
    which then shipped and pointed players at a server that did not exist."""
    root = Path(__file__).resolve().parents[1]

    def snapshot():   # the player's own files may exist: they must just stay exactly as they were
        return {n: (root / n).read_bytes() if (root / n).exists() else None for n in ("config.json", "session.json")}
    before = snapshot()
    with tempfile.TemporaryDirectory() as tmp:
        run_flow(Path(tmp))
    assert snapshot() == before
