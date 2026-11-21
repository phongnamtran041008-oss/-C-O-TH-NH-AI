"""Linh thú and thần thông of Thiên Địa Đồ through the real client and a real server.

Taming (Vạn Tượng Trạch, Huyền Quy on the misty island, Luyện Khí tầng 4 of Đạo Thụ): the beast
shows itself, fights by the open-world rule, the count of Phản Đòn shows over it and at the top
while it is tamed, it yields after the planned number, a click with a Phong Ấn Phù in the bag
seals it, and it becomes a Linh Thú worn and following like a con giáp.

Gliding (Lưu Vân Cốc, Luyện Khí tầng 9 with Tiểu Long worn): Bày pháp trận (T), Cưỡi linh thú
(R), then Đạp Kiếm Lướt (G) over the waterfall to the weapon spot that walking cannot reach,
and E picks up the weapon lying there.

    python -m client.tests.test_beast_flow <dir>     # leaves numbered screenshots in <dir>
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
from client.tests.test_combat_flow import CARD, walk_to, world
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_weapon_flow import give, reach_stage
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_tree  # noqa: E402

PLAN = math_tree.world_plan()
TAME = "huyen_quy"
TAME_ZONE = "ho_nghien_muc"          # Vạn Tượng Trạch
GLIDE_ZONE = "luu_van_coc"           # Lưu Vân Cốc
GLIDE_SPOT = "dao_2_ha"              # in the clouds above the waterfall
# the shore 3 tiles below it, where the glide starts (read from the plan: the map is generated)
GLIDE_FROM = next((p["pos"][0], p["pos"][1] + 3) for p in PLAN["weapons_placed"]
                  if f"{p['weapon']}_{p['quality']}" == GLIDE_SPOT)


def beast_plan(bid: str) -> dict:
    return next(b for b in PLAN["beasts"] if b["id"] == bid)


def feet(tx: int, ty: int) -> tuple[float, float]:
    return tx * 16 + 8.0, ty * 16 + 12.0


def start(server: ServerProcess, workdir: Path, shots, username: str, name: str, zone: str, tile, stage: int):
    token, uid = make_account(server.url, username, name)
    reach_stage(server, uid, stage=stage)
    x, y = feet(*tile)
    server.sql("update characters set zone_id=?, x=?, y=?, realm='luyen_khi', realm_stage=?, hp=400 where user_id=?",
               (zone, x, y, stage, uid))
    server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": username,
                                                      "server_url": server.url}))
    return uid


def enter(drv: Driver, zone: str):
    drv.click("menu_start")
    drv.wait(lambda: world(drv) is not None and world(drv).joined and world(drv).zone_id == zone, 15, zone)
    drv.wait_api()
    return world(drv)


def beast_ent(ws, bid: str):
    return next((e for e in ws.entities.values() if e.beast and e.mtype == bid and e.alive), None)


# ------------------------------------------------------------------ taming
def run_tame_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        b = beast_plan(TAME)
        stage = b["requires"]["stage"]
        near = (b["pos"][0] + 1, b["pos"][1] + 3)          # on Đảo Sương, just south of it
        uid = start(server, workdir, shots, "detu_thu", "Thu Phục", TAME_ZONE, near, stage)
        give(server, uid, "phong_an_phu", 1)
        drv = Driver(server.url, workdir, shots)
        ws = enter(drv, TAME_ZONE)
        assert ws.abilities and ws.abilities["thu_phuc_linh_thu"]["ok"], ws.abilities
        drv.wait(lambda: beast_ent(ws, TAME) is not None, 10, "Huyền Quy shows itself")
        e = beast_ent(ws, TAME)
        assert e.need == b["parries_to_tame"] and ws.beast_label(e).startswith(b["name_vi"])
        drv.wait(lambda: math.hypot(e.pos[0] - ws.player.x, e.pos[1] - ws.player.y) < 40 or drv.top_is(CARD), 10,
                 "it comes out to fight")
        if not drv.top_is(CARD):
            drv.shot("beast_in_land")

        # ---- it fights by the open-world rule: each right answer to its blow is a Phản Đòn that counts
        need, counted, shot_taming = b["parries_to_tame"], 0, False
        end = time.time() + 150
        while not (ws.taming.get(e.id) or {}).get("yielded"):
            assert time.time() < end, f"taming stalled at {ws.taming}"
            if drv.top_is(CARD):
                card = drv.game.top
                res = answer_card(drv, server, correct=True)
                c = res.get("combat") or {}
                assert c.get("parry"), c
                if card.monster_id == e.id:
                    counted += 1
                    assert c["tame"]["n"] == counted and c["tame"]["need"] == need, c["tame"]
                drv.wait(lambda: not drv.top_is(CARD), 8, "the card closes")
                if counted == 1 and not shot_taming:
                    drv.wait(lambda: e.id in ws.taming, 4, "the count over the beast")
                    drv.step(4)
                    drv.shot("beast_taming")
                    shot_taming = True
                continue
            if math.hypot(e.pos[0] - ws.player.x, e.pos[1] - ws.player.y) > 30:
                walk_to(drv, e.pos[0], e.pos[1], near=14, timeout=1.0)
            drv.step(3)
        assert counted == need and ws.taming[e.id]["n"] == need
        drv.step(6)
        drv.shot("beast_yielded")

        # ---- E beside it, with the talisman in the bag: Phong Ấn Phù
        assert ws.action_of(("ent", e)) == "seal"
        end = time.time() + 15
        while not (ws.target is not None and ws.target[0] == "ent" and ws.target[1] is e):
            assert time.time() < end, "never stood facing the beast"
            walk_to(drv, e.pos[0], e.pos[1] + 9, near=3, timeout=1.0)
            ws.player.facing = "up"
            drv.step(3)
        drv.press(pygame.K_e)
        drv.wait(lambda: any("thu phục" in t for t in drv.toast_log), 10, "the seal")
        rows = server.sql("select pet_type, equipped from pets where user_id=?", (uid,))
        assert rows == [(TAME, 0)], rows
        left = server.sql("select coalesce(sum(quantity), 0) from inventory_items where user_id=? and item_id=?",
                          (uid, "phong_an_phu"))[0][0]
        assert left == 0, "the talisman was spent"
        drv.wait(lambda: beast_ent(ws, TAME) is None, 5, "it leaves the wild for its owner")
        drv.step(4)
        drv.shot("beast_sealed")

        # ---- one companion model: it is a Linh Thú, worn from the same panel, following like a con giáp
        drv.wait_api()
        drv.game.open_pets()
        drv.wait(lambda: drv.top_is("PetScene") and (drv.game.state.pets or {}).get("pets"), 10, "the pets")
        pet = next(p for p in drv.game.state.pets["pets"] if p["pet_type"] == TAME)
        assert pet["tamed"] and pet["skill_vi"] == b["gift_vi"]
        drv.click(f"pets_wear_{pet['id']}")
        drv.wait(lambda: drv.game.worn_pet() == TAME, 10, "Huyền Quy worn")
        drv.shot("beast_in_pets")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("WorldScene"), 5, "back in the world")
        me = f"p{drv.game.state.me['id']}"
        drv.wait(lambda: me in ws.pet_follow and ws.pet_follow[me].kind == TAME, 5, "it follows")
        drv.step(20)
        drv.shot("beast_following")
        drv.close()
    finally:
        server.stop()


# ------------------------------------------------------------------ thần thông and the glide
def run_glide_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        uid = start(server, workdir, shots, "detu_luot", "Đạp Kiếm", GLIDE_ZONE, GLIDE_FROM, 9)
        server.sql("insert into pets(user_id, pet_type, level, equipped) values (?, 'tieu_long', 1, 1)", (uid,))
        drv = Driver(server.url, workdir, shots)
        ws = enter(drv, GLIDE_ZONE)
        a = ws.abilities
        assert a["dap_kiem_luot"]["ok"] and a["phap_tran"]["ok"] and a["cuoi_linh_thu"]["ok"], a
        drv.wait(lambda: any(sp.id == GLIDE_SPOT for sp in ws.weapon_spots), 10, "the spots of the land")
        spot = next(sp for sp in ws.weapon_spots if sp.id == GLIDE_SPOT)
        assert spot.state == "available", spot.reason_vi
        x0, y0 = feet(*GLIDE_FROM)

        # ---- on foot the spot is out of reach: the water stops the steps
        walk_to(drv, spot.x, spot.y, near=4, timeout=1.5)
        assert math.hypot(spot.x - ws.player.x, spot.y - ws.player.y) > 20, "walking cannot reach it"
        walk_to(drv, x0, y0, near=2, timeout=3)

        # ---- Bày pháp trận (T)
        drv.press(pygame.K_t)
        drv.wait(lambda: ws.formations, 5, "the formation is laid")
        drv.step(10)
        drv.shot("ability_formation")

        # ---- Cưỡi linh thú (R): Tiểu Long carries us, and the server moves us at its speed
        drv.wait(lambda: drv.game.worn_pet() == "tieu_long", 5, "Tiểu Long worn")
        drv.press(pygame.K_r)
        drv.wait(lambda: ws.riding and not ws.pending, 5, "on the mount")
        assert ws.move_speed() == ws.ride_mult * 74.0 and ws.ride_mult > 1
        start_x = ws.player.x
        drv.hold([pygame.K_d], 0.25)
        drv.wait(lambda: not ws.pending, 5, "the server caught up")
        assert ws.player.x > start_x and ws.corrections <= 2, ws.corrections
        drv.step(6)
        drv.shot("ability_ride")
        drv.press(pygame.K_r)
        drv.wait(lambda: not ws.riding and not ws.pending, 5, "on foot again")
        walk_to(drv, x0, y0, near=2, timeout=3)
        ws.player.facing = "up"

        # ---- Đạp Kiếm Lướt (G) up over the waterfall
        before = ws.corrections
        drv.keys.held = {pygame.K_w}
        drv.press(pygame.K_g)
        drv.keys.held = set()
        drv.step(3)
        drv.shot("ability_glide")
        drv.wait(lambda: not ws.pending, 5, "the server applied the glide")
        me = f"p{drv.game.state.me['id']}"
        drv.wait(lambda: not ws.glide_pos(me, 0.0, 0.0)[2], 5, "the sword lands")
        drv.step(6)
        assert ws.corrections == before, "the server put us where we glided"
        assert (int(ws.player.x // 16), int((ws.player.y - 1) // 16)) == (spot.tx, spot.ty)
        assert not any("Chỗ ấy" in t or "vật cản" in t for t in drv.toast_log)

        # ---- the weapon spot behind the waterfall: E picks it up
        drv.wait(lambda: ws.target is not None and ws.target[0] == "weapon" and ws.target[1].id == GLIDE_SPOT, 5,
                 "the spot under our feet")
        drv.shot("ability_glide_spot")
        drv.press(pygame.K_e)
        drv.wait(lambda: server.sql("select placed_id from weapon_claims where user_id=?", (uid,)) == [(GLIDE_SPOT,)],
                 10, "the weapon is ours")
        drv.wait_api()
        drv.step(6)
        drv.shot("ability_glide_claimed")
        drv.close()
    finally:
        server.stop()


def test_tame_a_beast_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_beast_") as tmp:
        run_tame_flow(Path(tmp))


def test_glide_to_a_weapon_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_glide_") as tmp:
        run_glide_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "beasts"
    for run, sub in ((run_tame_flow, "tame"), (run_glide_flow, "glide")):
        with tempfile.TemporaryDirectory() as tmp:
            run(Path(tmp), out / sub)
    print("screenshots in", out)
