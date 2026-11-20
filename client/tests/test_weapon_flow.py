"""Binh khí của Thiên Địa Đồ through the real client: a player at Luyện Khí tầng 4 of Đạo Thụ
picks up Mộc Kiếm hạ phẩm through the API (the lands session's spot calls the same route),
finds it in the bag's Binh Khí tab with its type, grade, quality and effect next to the
locked spots and why they are locked, equips it there - and the character then holds it: the
stats the world draws from name it, and the v2 layer drawn in the hand is its own sheet. Then
Lò Toán raises it from hạ phẩm to trung phẩm (Rèn nâng phẩm) and lists the rest of the chain, up
to tuyệt phẩm, with the sword waiting at the next step until Đạo Thụ climbs.

Run as a script with a folder to keep the screenshots:
    python -m client.tests.test_weapon_flow art/preview/weapon_flow
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the tree the server ships

from app.learning import math_path, math_tree  # noqa: E402
from app.systems import math_tree_progress as tp  # noqa: E402

SPOT = "kiem_1_ha"
WEAPON = "kiem_1"
STAGE = 4


def reach_stage(server: ServerProcess, uid: int, realm: str = "luyen_khi", stage: int = STAGE) -> None:
    """Every node of the realm up to `stage` done, the way the game records it: a passed Thiên
    kiếp nhỏ on each part of a node, every programming exercise solved."""
    t = math_tree.tree()
    day = "2026-01-01 00:00:00"
    for n in t.nodes.values():
        if n.realm != realm or (n.stage or 99) > stage:
            continue
        for part in tp.parts(n):
            server.sql("insert into math_runs(user_id, subject_id, node_id, floor, mode, tier, correct_streak, "
                       "wrong_streak, combo, best_combo, asked, correct, review_asked, xp_gained, ladders, passed, "
                       "started_at, ended_at) values (?, ?, ?, ?, 'trial', ?, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, ?, ?)",
                       (uid, part.subject_id, n.id, part.floor, math_path.floor_tiers(part.floor)[1], day, day))
        for pid in n.problems:
            server.sql("insert into math_submissions(user_id, problem_id, subject_id, floor, tier, verdict, passed, "
                       "total, ms, xp_gained, code, created_at, judged_at) "
                       "values (?, ?, 'lap_trinh', 1, 1, 'AC', 1, 1, 1, 0, '', ?, ?)", (uid, pid, day, day))


def give(server: ServerProcess, uid: int, item_id: str, qty: int) -> None:
    server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, ?, ?, 0) "
               "on conflict(user_id, item_id, bound) do update set quantity = quantity + excluded.quantity",
               (uid, item_id, qty))


def run_weapon_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_binh", "Kiếm Khách")
        auth = {"Authorization": f"Bearer {token}"}
        server.sql("update users set spirit_stones=500, flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        reach_stage(server, uid)

        # ---- the API the land spots call: a spot shows why it is shut, then gives its weapon once
        view = httpx.get(url + "/weapons", headers=auth).json()
        assert view["tu_vi"]["stage"] >= STAGE, view["tu_vi"]
        spot = next(p for p in view["placed"] if p["id"] == SPOT)
        assert spot["state"] == "available", spot
        assert any(p["state"] == "locked" and p["reason_vi"] for p in view["placed"]), "later spots say why"
        r = httpx.post(url + "/weapons/claim", json={"id": SPOT, "land": spot["land"]}, headers=auth)
        assert r.status_code == 200, r.text
        piece = r.json()["equipment"]
        assert httpx.post(url + "/weapons/claim", json={"id": SPOT}, headers=auth).status_code == 400

        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_binh",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: drv.top_is("AbodeScene") and drv.game.state.cult is not None, 15, "Động Phủ")
        drv.wait_api()
        assert not drv.game.state.cult.get("stats", {}).get("weapon"), "bare hands first"

        # ---- the bag: Binh Khí tab, then equip
        from client.scenes.bag import BagScene
        drv.game.push(BagScene(drv.game))
        drv.wait_scene("BagScene")
        drv.click("bag_tab_weapons")
        bag = drv.game.top
        drv.wait(lambda: bag.wpn is not None, 5, "the weapons")
        mine = [w for w in bag.wpn["weapons"] if w.get("weapon")]
        assert [w["id"] for w in mine] == [piece["id"]]
        wv = mine[0]["weapon"]
        assert (wv["type"], wv["grade"], wv["quality"]) == ("kiem", 1, "ha") and wv["effect_vi"], wv
        assert [q["id"] for q in bag.wpn["qualities"]] == ["ha", "trung", "thuong", "cuc", "tuyet"]
        from client import strings_vi as T
        assert T.gear_grade(mine[0]) == ("Hạ phẩm", bag.wpn["qualities"][0]["color"])
        drv.shot("weapon_bag_before_equip")
        drv.click(f"weq_{piece['id']}")
        drv.wait_api()
        drv.wait(lambda: bag.wpn.get("equipped") == piece["id"], 5, "the sword equipped")
        drv.wait(lambda: (drv.game.state.cult or {}).get("stats", {}).get("weapon") == WEAPON, 5,
                 "the stats name the sword")
        from client.engine import art2
        if art2.on():          # the v2 layer drawn in the hand is the weapon's own sheet
            sheet, clip = art2.weapon_for(WEAPON)
            assert sheet is not None and sheet is art2.weapon(WEAPON) and clip == "slash"
            realm = drv.game.state.character.get("realm")
            bare = art2.char_layers(realm, "idle", 0.0, "right", None, aura=False)
            held = art2.char_layers(realm, "idle", 0.0, "right", WEAPON, aura=False)
            assert len(held) == len(bare) + 1, "the sword is a layer of the character"
            assert art2.weapon_for("kiem_3")[0] is art2.weapon("kiem_3"), "each grade has its own sheet"
        drv.shot("weapon_bag_equipped")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "back in Động Phủ")
        drv.step(10)
        drv.shot("weapon_in_hand_abode")

        # ---- Lò Toán: Rèn nâng phẩm
        from client.scenes.math_craft import MathCraftScene
        up = httpx.get(url + "/weapons/upgrade", headers=auth).json()
        for i in up["ingredients"]:
            give(server, uid, i["item_id"], i["qty"])
        drv.game.push(MathCraftScene(drv.game))
        drv.wait(lambda: drv.top_is("MathCraftScene") and drv.game.top.up is not None, 10, "Lò Toán")
        drv.click("craft_tab_upgrade")
        forge = drv.game.top
        drv.wait(lambda: forge.up["can"], 5, "the upgrade is possible")
        drv.shot("weapon_forge_upgrade")
        drv.click(f"upgrade_{piece['id']}")
        drv.wait_api()
        drv.wait(lambda: any("Trung phẩm" in t for t in drv.toast_log), 10, "the upgrade toast")
        rarity = server.sql("select rarity from equipment_instances where id=?", (piece["id"],))[0][0]
        assert rarity == "linh", rarity
        drv.wait(lambda: forge.up is not None and not forge.up["candidates"], 5, "nothing left to raise")
        # the whole chain is listed: the sword now waits at the next step, shut until Đạo Thụ climbs
        steps = forge.up["steps"]
        assert [(s["from"], s["to"]) for s in steps] == [("ha", "trung"), ("trung", "thuong"),
                                                         ("thuong", "cuc"), ("cuc", "tuyet")]
        assert [c["id"] for c in steps[1]["candidates"]] == [piece["id"]] and not steps[1]["open"]
        assert steps[1]["reason_vi"] and steps[-1]["to_color"] == "#C99A3A"
        assert [k for k, _, _ in forge.upgrade_rows()].count("step") == 4
        drv.shot("weapon_forge_done")
        drv.close()
    finally:
        server.stop()


def test_weapon_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_weapon_") as tmp:
        run_weapon_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "weapons"
    with tempfile.TemporaryDirectory() as tmp:
        run_weapon_flow(Path(tmp), out)
    print("screenshots in", out)
