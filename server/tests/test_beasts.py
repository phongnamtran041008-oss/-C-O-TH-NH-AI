"""Linh thú of Thiên Địa Đồ (world_plan.json `beasts` and `beast_taming`, wired section 'beasts'):
who a beast shows itself to, taming it by Phản Đòn, sealing it with a Phong Ấn Phù, the one
companion model it joins, and each beast's gift as a real effect.

The world runs on a fake clock whose tick is called by hand (the machinery of test_combat); the
quiz service and the database are real. Every number is read from the plan.
"""
import pytest
import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.learning import math_tree
from app.models import InventoryItem, Pet
from app.realtime import beasts as wild
from app.realtime import combat, lands
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import beasts, pets, weapons
from tests.test_combat import FakeMono, fighter, last, run, settle
from tests.test_combat_on_hit import (SLIME_MA, VALLEY, answer, events, luyen_khi, plan, provoke, rest, stand_at,
                                      take_blow)

TALISMAN = "phong_an_phu"


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def bplan(bid: str) -> dict:
    return next(b for b in math_tree.world_plan()["beasts"] if b["id"] == bid)


def pos(stage: int, realm: str = "luyen_khi") -> lands.TreePos:
    return lands.TreePos(realm, stage, frozenset())


def at_beast(w: World, s, bid: str, near: float = 0.0):
    """The player beside a beast in its land, every monster of the channel out of the way."""
    b = bplan(bid)
    zone = lands.zone_of(b["land"])
    assert w.join(s, "truc_lam_thon", "abode")
    ch = w._pick_channel(zone)
    m = next(x for x in ch.monsters if getattr(x, "beast", False) and x.kind == bid)
    for o in ch.monsters:
        if o is not m:
            o.mode, o.respawn_at = "dead", 1e12
    w._place(s, zone, m.x, m.y + near, "up")
    return s.player, m


def seen_ids(s) -> set:
    out = set()
    for msg in s.sent:
        if msg.get("t") == "snap":
            out |= {e["id"] for e in msg.get("add", [])}
    return out


async def give(uid: int, item: str, qty: int = 1) -> None:
    async with dbm.SessionLocal() as db:
        db.add(InventoryItem(user_id=uid, item_id=item, quantity=qty, bound=False))
        await db.commit()


async def own(uid: int) -> list[str]:
    async with dbm.SessionLocal() as db:
        return list((await db.execute(select(Pet.pet_type).where(Pet.user_id == uid))).scalars())


# ------------------------------------------------------------------ the plan
BESTIARY = {"ngoc_tho", "tam_bao_thu", "kim_thiem", "bach_ho_con", "cuu_vi_ho", "kim_si_dieu"}


def test_the_eleven_beasts_of_luyen_khi_are_built_and_the_sky_one_waits():
    built = beasts.built()
    assert set(built) == {"linh_ho", "huyen_quy", "bach_hac", "hoa_tuoc", "tieu_long"} | BESTIARY
    assert bplan("ky_lan_con")["status"] == "chua_co" and "ky_lan_con" not in built
    # the six of the bestiary have their art since 2026-11-20 (test_bestiary.py also plays them waiting)
    assert all(bplan(b)["status"] == "co" for b in BESTIARY)
    assert math_tree.section_wired("beasts") and math_tree.section_wired("abilities")
    for bid, b in built.items():
        assert lands.zone_of(b["land"]) is not None, bid
        assert b["gift"]["type"] in math_tree.GIFT_TYPES and b["parries_to_tame"] >= 1, bid


def test_each_land_spawns_its_own_beast_in_every_channel_and_a_bi_canh_none(gw):
    for bid, b in beasts.built().items():
        ch = gw._pick_channel(lands.zone_of(b["land"]))
        mine = [m for m in ch.monsters if getattr(m, "beast", False)]
        assert sorted(m.kind for m in mine) == sorted(k for k, o in beasts.built().items() if o["land"] == b["land"])
        m = next(x for x in mine if x.kind == bid)
        tx, ty = b["pos"]
        assert (m.x, m.y) == (tx * 16 + 8, ty * 16 + 12) and m.on_hit and not m.shield
    assert not [m for m in gw._pick_channel("truc_lam_thon").monsters if getattr(m, "beast", False)]


# ------------------------------------------------------------------ who it shows itself to
async def test_a_beast_shows_itself_only_from_its_stage(client, gw):
    h, uid, s = await fighter(client, gw, "lt_1", "Linh Một")
    need = bplan("linh_ho")["requires"]["stage"]
    s.tree = pos(need - 1)
    p, m = at_beast(gw, s, "linh_ho", near=30)
    run(gw, 0.3)
    assert m.eid not in seen_ids(s) and not m.fights(p)
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) == "no_target"
    m.atk_ready = 0.0
    run(gw, 3.0)
    assert last(s, "q") is None and p.user_id not in m.engaged, "it never aims at whom it does not show itself to"
    s.tree = pos(need)
    run(gw, 0.3)
    added = [e for msg in s.sent if msg.get("t") == "snap" for e in msg.get("add", []) if e["id"] == m.eid]
    assert added and added[-1]["beast"] == 1 and added[-1]["need"] == bplan("linh_ho")["parries_to_tame"]
    assert m.fights(p)


async def test_a_beast_that_needs_an_ability_waits_for_it(client, gw, monkeypatch):
    """Hỏa Tước nests behind a chasm: it shows itself from its stage only while Đạp Kiếm Lướt exists."""
    h, uid, s = await fighter(client, gw, "lt_2", "Linh Hai")
    b = bplan("hoa_tuoc")
    assert b["needs"] == "dap_kiem_luot"
    s.tree = pos(b["requires"]["stage"])
    p, m = at_beast(gw, s, "hoa_tuoc", near=8)
    assert m.shows_to(p)
    real = weapons.unlock_open
    monkeypatch.setattr(weapons, "unlock_open", lambda uid_, at: False if uid_ == "dap_kiem_luot" else real(uid_, at))
    assert not m.shows_to(p)
    assert beasts.missing_vi(b, s.tree) == ["Cần Đạp Kiếm Lướt."]


async def test_a_tamed_beast_no_longer_shows_itself_to_its_owner(client, gw):
    h, uid, s = await fighter(client, gw, "lt_3", "Linh Ba")
    s.tree = pos(4)
    p, m = at_beast(gw, s, "huyen_quy", near=30)
    assert m.shows_to(p)
    s.tamed = {"huyen_quy"}
    assert not m.shows_to(p)


# ------------------------------------------------------------------ taming
async def tame(client, gw, h, s, p, m) -> dict:
    """Parry the beast's blows until it yields; the last result."""
    res = None
    for i in range(m.need):
        q = await take_blow(gw, s, p, m)
        assert q is not None and q["mid"] == m.eid, f"the beast's blow {i + 1} lands and asks"
        res = await answer(client, h, s, True)
        assert res["combat"]["parry"] and res["combat"]["tame"]["n"] == i + 1
        rest(gw)
        m.stun_until = 0.0
    return res["combat"]["tame"]


async def test_the_beast_yields_after_the_planned_number_of_parries(client, gw):
    h, uid, s = await fighter(client, gw, "lt_4", "Linh Bốn")
    s.tree = pos(3)
    p, m = at_beast(gw, s, "linh_ho", near=6)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q["q"]["context"] == "math_combat"
    land_nodes = beasts.land_nodes("me_do_lam")
    assert land_nodes and m.info["nodes"] == list(land_nodes), "it asks what the creatures of its land stand for"
    # a wrong answer counts nothing; the result still shows how far the taming is
    wrong = await answer(client, h, s, False)
    assert wrong["combat"]["tame"] == {"beast": "linh_ho", "name_vi": "Linh Hồ", "n": 0,
                                       "need": bplan("linh_ho")["parries_to_tame"], "yielded": False}
    rest(gw)
    m.hp = m.max_hp
    t = await tame(client, gw, h, s, p, m)
    assert t["yielded"] and t["n"] == t["need"] == bplan("linh_ho")["parries_to_tame"]
    assert m.alive and m.hp >= 1, "a beast is never killed"
    assert m.yielded_to(p.user_id, gw.mono()) and not m.fights(p) and p.user_id not in m.engaged
    tames = events(s, "tame")
    assert (tames[-1]["n"], tames[-1]["need"], tames[-1]["ok"], tames[-1]["by"]) == (t["need"], t["need"], 1, p.eid)
    m.atk_ready = 0.0
    s.sent.clear()
    run(gw, 3.0)
    assert last(s, "q") is None, "a beast that yielded no longer strikes its tamer"


async def test_plain_hits_never_kill_a_beast(client, gw):
    h, uid, s = await fighter(client, gw, "lt_5", "Linh Năm")
    s.tree = pos(3)
    p, m = at_beast(gw, s, "linh_ho", near=6)
    m.hp = 2.0
    combat.hurt_monster(p.channel, m, p, 500.0, False, gw.mono())
    assert m.alive and m.hp == 1.0


async def test_the_count_starts_over_when_the_fight_breaks_off(client, gw):
    h, uid, s = await fighter(client, gw, "lt_6", "Linh Sáu")
    s.tree = pos(3)
    p, m = at_beast(gw, s, "linh_ho", near=6)
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    res = await answer(client, h, s, True)
    assert m.parries == {p.user_id: 1} and res["combat"]["tame"]["n"] == 1
    m.reset()                    # it went home (leashed, or its foe left)
    assert m.parries == {}


# ------------------------------------------------------------------ sealing
async def test_sealing_takes_a_talisman_and_the_beast_becomes_a_linh_thu(client, gw):
    h, uid, s = await fighter(client, gw, "lt_7", "Linh Bảy")
    s.tree = pos(3)
    p, m = at_beast(gw, s, "linh_ho", near=6)
    r = await client.post("/beasts/seal", json={"id": m.eid}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_yielded"
    await provoke(gw, p, m)
    await tame(client, gw, h, s, p, m)
    m.x, m.y = p.x, p.y + 4
    r = await client.post("/beasts/seal", json={"id": m.eid}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_talisman", r.text
    assert await own(uid) == []
    await give(uid, TALISMAN, 2)
    p.x += 200
    r = await client.post("/beasts/seal", json={"id": m.eid}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "too_far"
    p.x -= 200
    r = await client.post("/beasts/seal", json={"id": m.eid}, headers=h)
    assert r.status_code == 200, r.text
    assert r.json()["sealed"] == "linh_ho" and r.json()["pet"]["tamed"] is True
    assert await own(uid) == ["linh_ho"]
    async with dbm.SessionLocal() as db:
        left = (await db.execute(select(InventoryItem.quantity).where(InventoryItem.user_id == uid,
                                                                     InventoryItem.item_id == TALISMAN))).scalar()
    assert left == 1, "one talisman spent"
    assert "linh_ho" in s.tamed and not m.shows_to(p) and events(s, "seal")
    run(gw, 0.3)
    assert any(m.eid in msg.get("rm", []) for msg in s.sent if msg.get("t") == "snap"), "it leaves their world"
    r = await client.post("/beasts/seal", json={"id": m.eid}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_here"
    # one companion model: it is a Linh Thú like the con giáp, worn the same way
    view = (await client.get("/pets", headers=h)).json()
    mine = [x for x in view["pets"] if x["pet_type"] == "linh_ho"]
    assert mine and mine[0]["tamed"] and mine[0]["skill_vi"] == bplan("linh_ho")["gift_vi"]
    assert view["total"] == 12 and "linh_ho" not in {b["id"] for b in view["book"]}
    r = await client.post("/pets/equip", json={"pet_id": mine[0]["id"]}, headers=h)
    assert r.status_code == 200 and p.pet == "linh_ho"
    bv = (await client.get("/beasts", headers=h)).json()
    assert next(b for b in bv["beasts"] if b["id"] == "linh_ho")["state"] == "tamed"


def test_the_banner_never_rolls_a_beast():
    assert set(pets.zodiac()) == set(pets.cfg()["species"])
    assert set(beasts.built()) <= set(pets.species()) and not set(beasts.built()) & set(pets.zodiac())
    assert all(sp["source"] == beasts.SOURCE for k, sp in pets.species().items() if k in beasts.built())


async def test_the_talisman_is_sold_in_the_village(client, gw):
    h, uid, s = await fighter(client, gw, "lt_8", "Linh Tám")
    view = (await client.get("/shop", headers=h)).json()
    assert any(x["item_id"] == TALISMAN for x in view["stock"])
    bv = (await client.get("/beasts", headers=h)).json()
    assert bv["talisman"]["item"] == TALISMAN and bv["can_seal"] is False       # a newcomer: tầng 0
    assert all(b["state"] == "locked" and b["reason_vi"] for b in bv["beasts"])


# ------------------------------------------------------------------ the gifts
def wear(p, bid: str) -> None:
    p.pet = bid


async def test_huyen_quy_softens_a_wrong_answers_blow(client, gw):
    h, uid, s = await fighter(client, gw, "lt_9", "Linh Chín")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    wear(p, "huyen_quy")
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    hp, hit = p.hp, p.question["hit"]
    res = await answer(client, h, s, False)
    value = bplan("huyen_quy")["gift"]["value"]
    full = hit * plan()["wrong_answer"]["damage_taken"]
    taken = max(1.0, full * (1 - value))
    assert res["combat"]["guarded"] and taken < full
    assert p.hp == pytest.approx(hp - taken) and res["combat"]["damage_taken"] == int(round(taken))


async def test_hoa_tuoc_adds_fire_to_the_counter(client, gw):
    h, uid, s = await fighter(client, gw, "lt_10", "Linh Mười")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    wear(p, "hoa_tuoc")
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    expected = combat.base_damage(p, m) * plan()["right_answer"]["counter_multiplier"] \
        * (1 + bplan("hoa_tuoc")["gift"]["value"])
    res = await answer(client, h, s, True)
    assert res["combat"]["fire"] and res["combat"]["damage"] == int(round(expected))
    assert events(s, "fire")[-1]["id"] == m.eid


async def test_bach_hac_brings_the_dodge_back_sooner(client, gw):
    h, uid, s = await fighter(client, gw, "lt_11", "Linh Mười Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    luyen_khi(p, 1)
    cd = plan()["dodge"]["cooldown_seconds"]
    assert combat.dodge(p, 10, 1, 0, gw.mono()) is None
    assert p.dodge_ready - gw.mono() == pytest.approx(cd)
    run(gw, cd + 0.1)
    wear(p, "bach_hac")
    assert combat.dodge(p, 11, -1, 0, gw.mono()) is None
    assert p.dodge_ready - gw.mono() == pytest.approx(cd * (1 - bplan("bach_hac")["gift"]["value"]))
    assert combat.rule_view(p)["dodge"]["cooldown"] == pytest.approx(cd * (1 - bplan("bach_hac")["gift"]["value"]))


async def test_linh_ho_sniffs_the_weapons_lying_near(client, gw):
    h, uid, s = await fighter(client, gw, "lt_12", "Linh Mười Hai")
    s.tree = pos(3)
    p, m = at_beast(gw, s, "linh_ho", near=6)
    r = await client.get("/beasts/sniff", headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_nose"
    wear(p, "linh_ho")
    r = await client.get("/beasts/sniff", headers=h)
    assert r.status_code == 200, r.text
    d = r.json()
    radius = bplan("linh_ho")["gift"]["radius_tiles"]
    assert d["radius_tiles"] == radius
    spots = [x for x in weapons.data()["placed"] if x["land"] == "me_do_lam"]
    near = {x["id"] for x in spots
            if ((x["pos"][0] * 16 + 8 - p.x) ** 2 + (x["pos"][1] * 16 + 12 - p.y) ** 2) ** 0.5 <= radius * 16}
    assert near and {f["id"] for f in d["found"]} == near and len(near) < len(spots)
    assert all(f["way_vi"].startswith("phía") for f in d["found"])
    assert d["found"] == sorted(d["found"], key=lambda f: f["distance_tiles"])


def test_the_mount_gift_is_the_ride():
    assert beasts.gift_value("tieu_long", "mount", "speed_mult") == bplan("tieu_long")["gift"]["speed_mult"] > 1
    assert beasts.gift_value("linh_ho", "mount", "speed_mult") == 0
    assert beasts.gift_value("cho", "sniff") == 0          # a con giáp has no beast gift
    assert wild.SEAL_REFUSALS_VI and all(v for v in wild.SEAL_REFUSALS_VI.values())
