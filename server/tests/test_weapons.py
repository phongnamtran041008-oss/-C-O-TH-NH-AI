"""Binh khí của Thiên Địa Đồ (systems/weapons.py, the `weapons` sections of world_plan.json).

The player's place in Đạo Thụ is what the plan calls tu vi; most tests set it directly
(`at`), so they do not depend on which tree nodes have questions today. One test reads the
real tree state of a new player. Every number is read from the plan, never repeated here.
"""
import pytest
import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.learning import math_tree
from app.models import EquipmentInstance, WeaponClaim
from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import catalog, cultivation, inventory, weapons
from tests.helpers import register
from tests.test_combat import LOOK, FakeMono, fighter, settle
from tests.test_combat_on_hit import (SLIME_MA, VALLEY, answer, plan, provoke, stand_at,
                                      take_blow)

STARTER = "kiem_1_ha"       # Kiếm Trủng Sơn, Luyện Khí tầng 1, ds_ngon_ngu
LATER = "kiem_1_trung"      # Luyện Khí tầng 4, ds_he_gauss


def spot(pid: str) -> dict:
    return weapons.data()["by_id"][pid]


def at(monkeypatch, stage: int, done=(), realm: str = "luyen_khi"):
    """Put every player at this place in Đạo Thụ with these nodes done."""
    async def standing(db, user_id):
        return (realm, stage), set(done)
    monkeypatch.setattr(weapons, "standing", standing)


async def player(client, name: str):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " ").title(), "appearance": LOOK}, headers=h)
    assert r.status_code == 200, r.text
    return h, data["user_id"]


async def placed(client, h, pid: str) -> dict:
    r = await client.get("/weapons", headers=h)
    assert r.status_code == 200, r.text
    return next(p for p in r.json()["placed"] if p["id"] == pid)


async def claim(client, h, pid: str, land: str | None = None):
    body = {"id": pid} if land is None else {"id": pid, "land": land}
    return await client.post("/weapons/claim", json=body, headers=h)


def err(r) -> str:
    return r.json()["error"]["code"]


# ------------------------------------------------------------------ the plan as equipment
def test_every_placed_weapon_is_a_piece_of_equipment_with_the_plans_numbers():
    assert weapons.validate() == []
    items = catalog.equipment()["items"]
    d = weapons.data()
    for p in d["placed"]:
        it = items[p["weapon"]]
        kind, grade = weapons.split(p["weapon"])
        assert it["slot"] == "weapon" and it["kind"] == p["weapon"] and it["weapon_type"] == kind
        assert it["stats"]["atk"] == d["grades"][grade]["atk"]
        assert it["name_vi"] == f"{d['grades'][grade]['prefix_vi']} {d['types'][kind]['name_vi']}"
    assert "kiem_go_dao" in items, "the old equipment is still there, one model for both"


def test_the_quality_sets_the_power_and_the_rarity_it_is_stored_as():
    d = weapons.data()
    base = d["grades"][1]["atk"]
    for q in d["qualities"].values():
        e = EquipmentInstance(user_id=1, item_id="kiem_1", rarity=q["rarity"], enhance_level=0)
        assert cultivation.instance_stats(e)["atk"] == int(round(base * q["power"]))
    plus = EquipmentInstance(user_id=1, item_id="kiem_1", rarity=d["qualities"]["ha"]["rarity"], enhance_level=2)
    bonus = catalog.equipment()["enhance"]["stat_bonus_per_level"]
    assert cultivation.instance_stats(plus)["atk"] == int(round(base * (1 + 2 * bonus))), "enhancing still works"


# ------------------------------------------------------------------ GET /weapons
async def test_a_new_player_sees_every_spot_locked_by_the_tree_with_the_reason(client):
    h, _ = await player(client, "binh_moi")
    r = await client.get("/weapons", headers=h)
    body = r.json()
    assert body["weapons"] == [] and body["equipped"] is None
    assert [p["id"] for p in body["placed"]] == [p["id"] for p in weapons.data()["placed"]]
    first = next(p for p in body["placed"] if p["id"] == STARTER)
    assert set(first) >= {"id", "weapon", "quality", "land", "pos", "state", "reason_vi"}
    assert first["state"] == "locked" and first["land"] == "kiem_trung_son"
    assert "Luyện Khí tầng 1" in first["reason_vi"], first["reason_vi"]
    assert first["pos"] == spot(STARTER).get("pos")


async def test_pos_is_copied_from_the_plan_when_present(client, monkeypatch):
    h, _ = await player(client, "binh_pos")
    at(monkeypatch, 0)
    d = weapons.data()
    monkeypatch.setitem(d["by_id"][STARTER], "pos", [120, 64])
    assert (await placed(client, h, STARTER))["pos"] == [120, 64]
    assert (await placed(client, h, LATER))["pos"] is None


async def test_the_reason_names_the_missing_stage_and_nodes_by_name(client, monkeypatch):
    h, _ = await player(client, "binh_ly_do")
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    p = await placed(client, h, LATER)
    t = math_tree.tree()
    assert p["state"] == "locked"
    assert "Luyện Khí tầng 4" in p["reason_vi"] and t.nodes["ds_he_gauss"].name_vi in p["reason_vi"]
    assert (await placed(client, h, STARTER))["state"] == "available"


# ------------------------------------------------------------------ POST /weapons/claim
async def test_claim_gives_the_weapon_once(client, monkeypatch):
    h, uid = await player(client, "binh_nhat")
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    r = await claim(client, h, STARTER, land="kiem_trung_son")
    assert r.status_code == 200, r.text
    piece = r.json()["equipment"]
    q = weapons.data()["qualities"]["ha"]
    assert piece["item_id"] == "kiem_1" and piece["rarity"] == q["rarity"] and piece["slot"] == "weapon"
    assert piece["weapon"]["quality"] == "ha" and piece["weapon"]["type"] == "kiem"
    assert r.json()["placed"]["state"] == "taken"
    assert (await placed(client, h, STARTER))["state"] == "taken"
    view = (await client.get("/weapons", headers=h)).json()
    assert [w["id"] for w in view["weapons"]] == [piece["id"]]
    # already taken
    r = await claim(client, h, STARTER)
    assert r.status_code == 400 and err(r) == "taken"
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(WeaponClaim).where(WeaponClaim.user_id == uid))).scalars().all()
        assert [(c.placed_id, c.instance_id) for c in rows] == [(STARTER, piece["id"])]
        n = len((await db.execute(select(EquipmentInstance).where(EquipmentInstance.user_id == uid))).scalars().all())
        assert n == 1


async def test_claim_is_refused_below_the_stage(client, monkeypatch):
    h, _ = await player(client, "binh_tang")
    at(monkeypatch, 3, done={"ds_ngon_ngu", "ds_he_gauss"})
    r = await claim(client, h, LATER)
    assert r.status_code == 400 and err(r) == "locked"
    assert "Luyện Khí tầng 4" in r.json()["error"]["message_vi"]


async def test_claim_is_refused_without_the_nodes(client, monkeypatch):
    h, _ = await player(client, "binh_nut")
    at(monkeypatch, 4, done={"ds_ngon_ngu"})
    r = await claim(client, h, LATER)
    assert r.status_code == 400 and err(r) == "locked"
    assert math_tree.tree().nodes["ds_he_gauss"].name_vi in r.json()["error"]["message_vi"]
    at(monkeypatch, 4, done={"ds_ngon_ngu", "ds_he_gauss"})
    assert (await claim(client, h, LATER)).status_code == 200


async def test_claim_is_refused_in_another_land(client, monkeypatch):
    h, _ = await player(client, "binh_lac")
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    r = await claim(client, h, STARTER, land="luu_van_coc")
    assert r.status_code == 400 and err(r) == "wrong_land"
    assert "Kiếm Trủng Sơn" in r.json()["error"]["message_vi"]
    assert (await placed(client, h, STARTER))["state"] == "available"


async def test_a_spot_needing_an_ability_not_in_the_game_stays_locked(client, monkeypatch):
    h, _ = await player(client, "binh_dap")
    pid = next(p["id"] for p in weapons.data()["placed"] if p.get("needs") == "dap_kiem_luot")
    at(monkeypatch, 9, done=set(math_tree.tree().nodes))
    r = await claim(client, h, pid)
    assert r.status_code == 400 and err(r) == "locked" and "Đạp Kiếm Lướt" in r.json()["error"]["message_vi"]


async def test_an_unknown_spot(client, monkeypatch):
    h, _ = await player(client, "binh_khong")
    r = await claim(client, h, "kiem_9_ha")
    assert r.status_code == 404 and err(r) == "no_weapon"


# ------------------------------------------------------------------ equip
async def test_equip_and_unequip_go_through_the_equipment_path(client, monkeypatch):
    h, uid = await player(client, "binh_deo")
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    piece = (await claim(client, h, STARTER)).json()["equipment"]
    before = (await client.get("/cultivation", headers=h)).json()["stats"]
    r = await client.post("/weapons/equip", json={"instance_id": piece["id"]}, headers=h)
    assert r.status_code == 200, r.text
    stats = r.json()["stats"]
    assert stats["weapon"] == "kiem_1" and stats["atk"] == before["atk"] + piece["stats"]["atk"]
    view = (await client.get("/weapons", headers=h)).json()
    assert view["equipped"] == piece["id"]
    r = await client.post("/weapons/unequip", headers=h)
    assert r.status_code == 200 and r.json()["stats"]["weapon"] is None
    assert (await client.get("/weapons", headers=h)).json()["equipped"] is None
    # a piece that is not a weapon is refused
    async with dbm.SessionLocal() as db:
        hat = EquipmentInstance(user_id=uid, item_id="non_la", rarity="pham", enhance_level=0)
        db.add(hat)
        await db.commit()
        hid = hat.id
    r = await client.post("/weapons/equip", json={"instance_id": hid}, headers=h)
    assert r.status_code == 400 and err(r) == "not_weapon"


# ------------------------------------------------------------------ the fight
def test_the_type_decides_the_attack_and_the_clip():
    for kind, t in weapons.data()["types"].items():
        prof = weapons.fight_profile(f"{kind}_1")
        assert (prof["range"], prof["cooldown"], prof["mult"], prof["clip"]) == (
            t["range"], t["cooldown"], t["mult"], t["clip"])
    assert weapons.fight_profile("kiem_go_dao") is None and weapons.fight_profile(None) is None


def test_the_branch_bonus_of_a_parry():
    cfg = weapons.data()["cfg"]
    own = 1 + cfg["own_branch_parry_bonus"]
    anyb = 1 + cfg["any_branch_parry_bonus"]
    assert weapons.parry_mult("kiem_1", "dai_so_tuyen_tinh") == pytest.approx(own)
    assert weapons.parry_mult("dao_1", "giai_tich") == pytest.approx(own)
    assert weapons.parry_mult("ho_lo_1", "xac_suat_thong_ke") == pytest.approx(own)
    assert weapons.parry_mult("thuong_1", "toi_uu_roi_rac") == pytest.approx(own)
    assert weapons.parry_mult("kiem_1", "giai_tich") == 1.0
    assert weapons.parry_mult("chuy_1", "giai_tich") == pytest.approx(anyb)     # Lập Trình: every branch
    assert weapons.parry_mult("cung_1", None) == pytest.approx(anyb)            # Thực Chiến
    assert weapons.parry_mult("kiem_go_dao", "dai_so_tuyen_tinh") == 1.0


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def wield(p, weapon_id: str) -> None:
    p.stats = {**p.stats, "weapon": weapon_id}


async def test_the_weapon_type_sets_the_normal_attack_in_the_world(client, gw):
    h, uid, s = await fighter(client, gw, "binh_danh", "Binh Đánh")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    wield(p, "cung_1")
    prof = combat.weapon_profile(p)
    assert prof["range"] == weapons.data()["types"]["cung"]["range"]
    assert combat.base_damage(p, m) == pytest.approx(
        max(1.0, p.stats["atk"] * prof["mult"] - m.info.get("def", 0) * combat.cfg()["defense_factor"]))


@pytest.mark.parametrize("weapon_id", ["kiem_1", "dao_1", "chuy_1"])
async def test_a_parry_of_the_weapons_own_branch_hits_harder(client, gw, weapon_id):
    h, uid, s = await fighter(client, gw, f"binh_{weapon_id}", "Binh Phản")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)          # an Đại Số monster
    wield(p, weapon_id)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q is not None and p.question["subject"] == "dai_so_tuyen_tinh"
    mult = weapons.parry_mult(weapon_id, "dai_so_tuyen_tinh")
    expected = combat.base_damage(p, m) * plan()["right_answer"]["counter_multiplier"] * mult
    mhp = m.hp
    c = (await answer(client, h, s, True))["combat"]
    assert c["parry"] and c["damage"] == int(round(expected)) and c["weapon_bonus"] == (mult > 1.0)
    assert m.hp == pytest.approx(mhp - expected)


async def test_equipping_a_claimed_weapon_reaches_the_world(client, gw, monkeypatch):
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    h, uid, s = await fighter(client, gw, "binh_the_gioi", "Binh Thế Giới")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    piece = (await claim(client, h, STARTER, land="kiem_trung_son")).json()["equipment"]
    assert (await client.post("/weapons/equip", json={"instance_id": piece["id"]}, headers=h)).status_code == 200
    assert p.weapon == "kiem_1" and combat.weapon_profile(p)["clip"] == "slash"


# ------------------------------------------------------------------ Rèn nâng phẩm
async def stock(uid: int, recipe: dict, extra_stones: int = 0) -> None:
    async with dbm.SessionLocal() as db:
        for i in recipe["ingredients"]:
            await inventory.change_item(db, uid, i["item"], int(i["qty"]), "test")
        await inventory.change_currency(db, uid, "spirit_stones", int(recipe["fee"]) + extra_stones, "test")
        await db.commit()


async def test_the_forge_raises_ha_to_trung_from_stage_four(client, monkeypatch):
    h, uid = await player(client, "binh_ren")
    r = weapons.upgrade_recipe()
    d = weapons.data()
    at(monkeypatch, 1, done={"ds_ngon_ngu"})
    piece = (await claim(client, h, STARTER)).json()["equipment"]
    await client.post("/weapons/equip", json={"instance_id": piece["id"]}, headers=h)
    await stock(uid, r)
    # below stage 4: refused, nothing spent
    res = await client.post("/weapons/upgrade", json={"instance_id": piece["id"]}, headers=h)
    assert res.status_code == 400 and err(res) == "locked" and "Luyện Khí tầng 4" in res.json()["error"]["message_vi"]
    view = (await client.get("/weapons/upgrade", headers=h)).json()
    assert not view["open"] and [c["id"] for c in view["candidates"]] == [piece["id"]]
    assert all(x["enough"] for x in view["ingredients"])
    # stage 4: done
    at(monkeypatch, 4, done={"ds_ngon_ngu"})
    view = (await client.get("/weapons/upgrade", headers=h)).json()
    assert view["open"] and view["can"]
    assert view["candidates"][0]["after_atk"] == int(round(d["grades"][1]["atk"] * d["qualities"][r["to"]]["power"]))
    stones = (await client.get("/inventory", headers=h)).json()["spirit_stones"]
    res = await client.post("/weapons/upgrade", json={"instance_id": piece["id"]}, headers=h)
    assert res.status_code == 200, res.text
    out = res.json()
    assert out["item"]["rarity"] == d["qualities"][r["to"]]["rarity"] and out["item"]["weapon"]["quality"] == r["to"]
    assert out["item"]["stats"]["atk"] == int(round(d["grades"][1]["atk"] * d["qualities"][r["to"]]["power"]))
    assert out["stats"]["atk"] > 0 and out["spirit_stones"] == stones - r["fee"]
    inv = {i["item_id"]: i["qty"] for i in (await client.get("/inventory", headers=h)).json()["items"]}
    assert all(inv.get(i["item"], 0) == 0 for i in r["ingredients"]), "the materials are spent"
    # once trung phẩm it cannot be raised again by this recipe
    await stock(uid, r)
    res = await client.post("/weapons/upgrade", json={"instance_id": piece["id"]}, headers=h)
    assert res.status_code == 400 and err(res) == "wrong_quality"


async def test_the_forge_needs_the_materials(client, monkeypatch):
    h, uid = await player(client, "binh_thieu")
    at(monkeypatch, 4, done={"ds_ngon_ngu"})
    piece = (await claim(client, h, STARTER)).json()["equipment"]
    res = await client.post("/weapons/upgrade", json={"instance_id": piece["id"]}, headers=h)
    assert res.status_code == 400 and err(res) == "need_material"
    # an old weapon is not a weapon of the plan
    async with dbm.SessionLocal() as db:
        old = EquipmentInstance(user_id=uid, item_id="kiem_go_dao", rarity="pham", enhance_level=0)
        db.add(old)
        await db.commit()
        oid = old.id
    res = await client.post("/weapons/upgrade", json={"instance_id": oid}, headers=h)
    assert res.status_code == 400 and err(res) == "not_plan_weapon"


def test_the_upgrade_materials_really_drop_by_the_time_it_opens():
    assert weapons._validate_upgrade() == []
