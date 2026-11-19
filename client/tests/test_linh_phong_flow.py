"""Stage 5 through the real client UI: open the Linh Phong Sào, hatch the starter egg, feed
the bee, move it, see the two roles (ở tổ / hộ vệ), collect honey, upgrade the hive, roll the
bee-egg gacha, read the Ong Phổ; then take two guard bees into Rừng Mực Loang and watch them
sting a monster whose Mặc Thuẫn the player broke."""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import Driver, ServerProcess
from client.tests.test_combat_flow import CARD, answer_math, beat, engage, world
from client.tests.test_world_flow import make_account

HAN = re.compile("[" + chr(0x3400) + "-" + chr(0x9FFF) + "]")    # CJK ideographs


def give(server: ServerProcess, uid: int, item: str, qty: int) -> None:
    server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, ?, ?, 0)", (uid, item, qty))


def abode(drv: Driver):
    from client.scenes.abode import AbodeScene
    return next((s for s in drv.game.scenes if isinstance(s, AbodeScene)), None)


def run_bee_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "nuoi_ong", "Phong Nữ", {"hair_color": "#A0522D", "hair_style": "dai",
                                                                "body": "nu"})
        h = {"Authorization": f"Bearer {token}"}
        httpx.get(url + "/quests", headers=h).raise_for_status()
        server.sql("update users set flags=?, spirit_stones=2000, immortal_jade=20 where id=?",
                   (json.dumps({"tutorial": 5}), uid))
        give(server, uid, "linh_mat", 6)
        give(server, uid, "trung_ong_linh", 1)
        give(server, uid, "sap_ong", 5)
        give(server, uid, "go_linh_moc", 3)
        server.sql("update characters set zone_id='abode', x=?, y=? where user_id=?", (27 * 16 + 12, 14 * 16, uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "nuoi_ong", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "abode")
        drv.wait_api()

        # the hive: Trúc Lão explains, then the starter egg hatches
        drv.press(pygame.K_h)
        drv.wait(lambda: drv.top_is("DialogScene"), 5, "hive intro")
        drv.shot("hive_intro")
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)
        drv.wait_scene("HiveScene")
        drv.wait(lambda: drv.game.top.hive is not None, 5, "hive data")
        hive = drv.game.top
        assert sorted(e["item_id"] for e in hive.hive["eggs"]) == ["trung_ong_linh", "trung_ong_pham"]
        drv.shot("hive_empty")
        drv.click("hv_hatch_trung_ong_pham")
        drv.wait_scene("HatchScene")
        drv.step(30)
        drv.game.top.t = 1.0
        drv.shot("hatch_cracking")
        drv.game.top.t = 2.4
        drv.shot("hatch_done")
        drv.click("hatch_ok")
        drv.wait_scene("HiveScene")
        drv.click("hv_hatch_trung_ong_linh")
        drv.wait_scene("HatchScene")
        drv.game.top.t = 2.4
        drv.step(3)
        drv.click("hatch_ok")
        drv.wait_scene("HiveScene")
        drv.wait_api()
        drv.wait(lambda: len(hive.hive["bees"]) == 2, 5, "two bees")
        for b in hive.hive["bees"]:                       # Vietnamese names only, no word attached
            assert not {"hanzi", "pinyin", "word", "word_mastery", "pollen_per_hour"} & set(b), b
            assert not HAN.search(b["name_vi"] + b["desc_vi"] + b["skill_vi"]), b
        first = hive.hive["bees"][0]
        hive.sel = first["id"]
        drv.step(3)
        # feed the first one Linh Mật (the only food in the bag)
        assert [f["food"] for f in hive.hive["foods"]] == ["linh_mat"]
        drv.click("hv_feed")
        drv.wait_scene("FoodPicker")
        drv.shot("feed_picker")
        drv.click("food_0")
        drv.wait_api()
        drv.wait(lambda: drv.top_is("HiveScene") or drv.top_is("MessageBox"), 5, "fed")
        if drv.top_is("MessageBox"):           # it was its favourite: Ong Phổ learns it
            drv.shot("favourite_found")
            drv.click("msg_ok")
        drv.wait_scene("HiveScene")
        drv.wait(lambda: hive.bee(first["id"])["xp"] > 0 or hive.bee(first["id"])["level"] > 1, 5, "fed")
        # move it to another open cell (pick, then click an empty cell)
        empty = next(c for c in hive.hive["open_cells"] if hive.bee_at(c) is None)
        drv.click(f"hv_cell_{empty}")
        drv.wait_api()
        drv.wait(lambda: hive.bee(first["id"])["slot"] == empty, 5, "moved")
        # two roles: Ở tổ (both bees, by default) and Hộ vệ, locked for a Phàm Nhân
        drv.step(2)
        assert "hv_role_hive" in drv.game.ui.widgets and "hv_role_guard" in drv.game.ui.widgets
        assert "hv_role_pollinate" not in drv.game.ui.widgets
        assert all(b["role"] == "hive" for b in hive.hive["bees"]) and hive.hive["guard_slots"] == 0
        # honey: the comb fills (here by hand), "Thu mật" puts it in the bag
        server.sql("update hive set honey=5.5, wax=1.2 where user_id=?", (uid,))
        hive.reload()
        drv.wait_api()
        drv.wait(lambda: hive.hive["honey"] >= 5, 5, "honey in the comb")
        drv.click("hv_collect")
        drv.wait_api()
        drv.wait(lambda: hive.hive["honey"] < 1, 5, "honey collected")
        drv.wait(lambda: any(f["food"] == "linh_mat" and f["qty"] >= 10 for f in hive.hive["foods"]), 5,
                 "honey in the bag")
        drv.click("hv_upgrade")                  # Sáp Ong + Gỗ Linh Mộc: level 2 and a lantern
        drv.wait_api()
        drv.wait(lambda: hive.hive["level"] == 2, 5, "hive level 2")
        assert hive.hive["decorations"][0]["id"] == "den_long"
        drv.step(5)
        drv.shot("hive_bees")
        drv.click("hv_book")
        drv.wait_scene("BeeBookScene")
        drv.wait(lambda: drv.game.top.book is not None, 5, "book")
        assert drv.game.top.book["found"] >= 1
        assert all("hanzi" not in e and "word" not in e for e in drv.game.top.book["entries"])
        drv.step(3)
        drv.shot("bee_book")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("HiveScene")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "abode again")
        drv.wait_api()
        # bee eggs at Thiên Cơ Các
        drv.press(pygame.K_g)
        drv.wait_scene("GachaScene")
        drv.click("g_tab_bees")
        drv.wait(lambda: drv.game.top.banner is not None and drv.game.top.banner["id"] == "bees", 5, "bee banner")
        drv.shot("gacha_bees")
        drv.click("g_bee1")
        drv.wait(lambda: drv.game.top.results is not None, 5, "egg roll")
        drv.game.top.anim_t = 2.0
        drv.game.top.opened = True
        drv.step(3)
        drv.shot("gacha_egg")
        drv.click("g_done")
        drv.press(pygame.K_ESCAPE)
        drv.close()

        # ---------------------------------------------------------------- guard bees in the forest
        server.sql("update characters set realm='luyen_khi', realm_stage=1, zone_id='rung_muc_loang', x=?, y=? "
                   "where user_id=?", (16 * 18, 16 * 20, uid))
        server.sql("update bees set role='guard', level=3 where user_id=?", (uid,))
        n_shots = drv.n_shots
        drv = Driver(url, workdir, shots)
        drv.n_shots = n_shots
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "forest")
        drv.wait_api()
        ws = world(drv)
        drv.wait(lambda: len(ws.my_bees) == 2, 5, "guard bees in the snapshot")
        drv.step(60)
        assert len(ws.flock.bees) == 2
        drv.shot("guards_follow")
        m = engage(drv, server)
        res = answer_math(drv, server, correct=True)
        assert res["combat"]["shield_broken"]
        drv.wait(lambda: not drv.top_is(CARD), 5, "card closes")
        drv.wait(lambda: ws.bee_hits > 0, 6, "bees sting the monster")
        drv.shot("guards_sting")
        if m.alive and m.id in ws.entities:
            beat(drv, ws, m, server)
        drv.close()
    finally:
        server.stop()


def test_bee_ui_flow():
    with tempfile.TemporaryDirectory() as tmp:
        run_bee_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots"
    with tempfile.TemporaryDirectory() as tmp:
        run_bee_flow(Path(tmp), out)
    print("screenshots in", out)
