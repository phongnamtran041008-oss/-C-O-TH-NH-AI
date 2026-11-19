"""Stage 8: luyện đan (spec 12.3). Đan phương, ingredients, the fee, the canh lửa minigame replayed
on the server, quality from the fire alone, a little Tu Vi per brew, the furnace, and the pills it
makes (Tụ Linh, Kháng Mực, Ngộ Tính, Phong Vương)."""
import json
from pathlib import Path

import pytest
from sqlalchemy import select

from app import balance, clock
from app.learning import math_path
from app.models import Bee
from app.systems import alchemy_fire, catalog
from tests.econ_helpers import give, player, qty, set_stones, stones
from tests.helpers import answer_key, old_script
from tests.test_math_loop import right_answer

ROOT = Path(__file__).resolve().parents[2]
C = balance.load("alchemy")


def perfect_timings(fire: dict) -> list[int]:
    """Stop the needle on the centre of each văn hỏa zone."""
    out = []
    for z, period in zip(fire["zones"], fire["periods"]):
        half = period // 2
        out.append(max(C["min_press_ms"], round(z["center"] / fire["bar"] * half)))
    return out


def miss_timings(fire: dict) -> list[int]:
    out = []
    for z, period in zip(fire["zones"], fire["periods"]):
        half = period // 2
        out.append(half if z["center"] < 60 else C["min_press_ms"])   # at the far end, or right at the start
    return out


async def brewer(client, name="dan_su", **kw):
    """A beginner with the Hồi Huyết đan phương and enough for two brews."""
    h, uid = await player(client, name, stones=500, **kw)
    await give(uid, "dp_hoi_huyet", 1)
    await give(uid, "truc_diep_thao", 3)
    await give(uid, "muc_tinh", 6)
    return h, uid


async def finish(client, h, fire, timings, frozen=None):
    if frozen is not None:
        frozen.advance(milliseconds=sum(timings) + 50)
    return await client.post("/alchemy/finish", json={"session_id": fire["session_id"], "timings": timings},
                             headers=h)


def no_word_game(obj) -> None:
    """Nothing of the old Chinese-word game in an alchemy payload."""
    text = json.dumps(obj, ensure_ascii=False)
    for key in ("chars", "fruit"):
        assert f'"{key}' not in text, key
    assert not old_script(obj)


# ------------------------------------------------------------------ data
def test_shared_fire_file_is_identical():
    a = (ROOT / "server" / "app" / "systems" / "alchemy_fire.py").read_bytes()
    b = (ROOT / "client" / "engine" / "alchemy_fire.py").read_bytes()
    assert a == b


def test_needle_and_judging():
    assert alchemy_fire.needle(0, 2000) == 0
    assert alchemy_fire.needle(1000, 2000) == 100
    assert alchemy_fire.needle(1500, 2000) == 50
    assert alchemy_fire.needle(2000, 2000) == 0        # back at the start
    assert alchemy_fire.judge(50, 50, 20, 6) == "perfect"
    assert alchemy_fire.judge(58, 50, 20, 6) == "good"
    assert alchemy_fire.judge(70, 50, 20, 6) == "miss"
    assert alchemy_fire.total(["perfect", "good", "miss"], C["points"]) == (3, 6)


@pytest.mark.parametrize("hits,want", [
    (["perfect"] * 3, "thuong"),
    (["perfect", "perfect", "good"], "thuong"),
    (["perfect", "good", "good"], "trung"),
    (["good"] * 3, "trung"),
    (["perfect", "good", "miss"], "trung"),
    (["good", "good", "miss"], "ha"),
    (["good", "miss", "miss"], "ha"),
    (["miss"] * 3, "phe"),
])
def test_quality_comes_from_the_fire_alone(hits, want):
    """The same hand at the fire gives the quality a player who also typed every reading right
    got before the purge (only three misses, once still Hạ phẩm, are now Phế đan)."""
    assert alchemy_fire.quality(*alchemy_fire.total(hits, C["points"]), C["quality"]) == want


def test_every_recipe_is_complete_and_free_of_the_word_game():
    pills, mats = catalog.pills(), catalog.materials()
    for rid, r in catalog.recipes().items():
        assert rid in pills, rid
        assert "chars" not in r and not old_script(pills[rid]), rid
        assert mats[r["item"]]["kind"] == "recipe" and mats[r["item"]]["recipe"] == rid
        for ing in r["ingredients"]:
            assert ing["kind"] in ("item", "fish"), (rid, ing)
            if ing["kind"] == "item":
                assert catalog.stack_item(ing["item"]) is not None, ing
        assert set(r["yield"]) == {"ha", "trung", "thuong"}
    assert set(C["brew_xp"]) == {"ha", "trung", "thuong"} and set(C["points"]) <= {"perfect", "good", "miss"}
    # spec 12.3 names every one of these pills
    for pid in ("hoi_huyet_dan", "hoi_khi_dan", "tu_linh_dan", "khang_muc_dan", "ngo_tinh_dan", "truc_co_dan",
                "kim_dan_dan", "phong_vuong_dan", "nguyen_anh_dan", "hoa_than_dan", "luyen_hu_dan", "hop_the_dan",
                "dai_thua_dan"):
        assert pid in catalog.recipes()


def _walk_items(rel: str) -> set[str]:
    found: set[str] = set()

    def walk(v):
        if isinstance(v, dict):
            if isinstance(v.get("item"), str):
                found.add(v["item"])
            if isinstance(v.get("items"), dict):
                found.update(v["items"])
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(json.loads((ROOT / "server" / "data" / rel).read_text("utf-8")))
    return found


def _shop_stock() -> set[str]:
    return {s["item"] for s in balance.load("shop")["stock"]}


def _obtainable_items() -> set[str]:
    """Every item some part of today's game hands out: monster drops (old and math), bí cảnh
    rooms and chests, the math dungeon and cơ duyên, quest rewards, the Sạp Tạp Hóa, the đan
    phương shelf of Tàng Thư Các and what the hive makes. Recipes only consume, so they are not read."""
    found: set[str] = set()
    for rel in ("creatures/monsters.json", "math/monsters.json", "balance/realm.json", "math/dungeon.json",
                "math/fortune.json", "quests.json"):
        found |= _walk_items(rel)
    found |= _shop_stock()
    found.update(balance.load("books")["shop"])
    found.update(("linh_mat", "sap_ong"))           # collected from the hive (systems/bees.py)
    return found


def test_every_ingredient_is_handed_out_somewhere_and_the_first_pills_need_nothing_rare():
    got = _obtainable_items()
    mats = catalog.materials()
    for rid, r in catalog.recipes().items():
        for ing in r["ingredients"]:
            if ing["kind"] == "item":
                assert ing["item"] in got, (rid, ing)
                assert ing["item"] not in mats or mats[ing["item"]]["kind"] != "recipe", (rid, ing)
    # a beginner brews Hồi Huyết / Hồi Khí Đan from what the shop sells or the first monsters drop
    first = _shop_stock() | {d["item"] for kind in ("ink_slime", "tone_wisp")
                             for d in catalog.monsters()[kind]["drops"] if "item" in d}
    for rid in ("hoi_huyet_dan", "hoi_khi_dan"):
        r = catalog.recipes()[rid]
        assert r["min_realm"] == "pham_nhan"
        for ing in r["ingredients"]:
            assert ing["kind"] == "item" and ing["item"] in first, (rid, ing)


def test_every_breakthrough_pill_is_craftable_from_what_the_game_hands_out():
    """Each realm's pill has a recipe and the đan phương for it is sold or dropped."""
    from app.systems import cultivation
    order = cultivation.order()
    got = _obtainable_items()
    pills = catalog.pills()
    trib = cultivation.cfg()["tribulation_to"]
    assert set(trib) == set(order[2:]), "every realm after Luyện Khí needs its pill"
    for realm, pid in trib.items():
        assert pills[pid]["effect"] == "breakthrough" and pills[pid]["realm"] == realm, pid
        r = catalog.recipes()[pid]
        assert r["item"] in got, f"{r['item']} (the đan phương of {pid}) is nowhere to be had"
        assert order.index(r["min_realm"]) == order.index(realm) - 1, pid       # brewed at the realm below
        if order.index(realm) >= order.index("nguyen_anh"):
            assert all(ing["kind"] == "item" for ing in r["ingredients"]), pid


# ------------------------------------------------------------------ brewing
async def test_brew_takes_ingredients_and_fee_and_perfect_fire_gives_thuong_pham(client, frozen):
    h, uid = await brewer(client)
    ov = (await client.get("/alchemy", headers=h)).json()
    no_word_game(ov)
    hh = next(r for r in ov["recipes"] if r["id"] == "hoi_huyet_dan")
    assert hh["known"] and hh["ready"] and ov["where"] == "home"
    assert [(i["name_vi"], i["qty"], i["have"]) for i in hh["ingredients"]] == [("Mực Tinh", 3, 6),
                                                                                ("Trúc Diệp Thảo", 1, 3)]
    unknown = next(r for r in ov["recipes"] if r["id"] == "truc_co_dan")
    assert not unknown["known"] and "ingredients" not in unknown and unknown["sources_vi"]
    r = await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)
    assert r.status_code == 200, r.text
    no_word_game(r.json())
    fire = r.json()["fire"]
    assert len(fire["zones"]) == len(fire["periods"]) == C["presses"]
    assert await stones(uid) == 500 - 10
    assert await qty(uid, "truc_diep_thao") == 2 and await qty(uid, "muc_tinh") == 3
    assert await qty(uid, "dp_hoi_huyet") == 1          # the recipe is kept
    res = (await finish(client, h, fire, perfect_timings(fire), frozen=frozen)).json()
    no_word_game(res)
    assert res["quality"] == "thuong" and res["hits"] == ["perfect"] * 3 and (res["points"], res["best"]) == (6, 6)
    assert res["made"] == 3 and await qty(uid, "hoi_huyet_dan") == 3
    assert res["xp"]["gained"] == C["brew_xp"]["thuong"]      # a little Tu Vi for a good brew
    # the same session cannot pay out twice
    r = await finish(client, h, fire, perfect_timings(fire))
    assert r.status_code == 409


async def test_a_missed_fire_is_phe_dan_and_the_ingredients_are_gone(client, frozen):
    h, uid = await brewer(client)
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    res = (await finish(client, h, fire, miss_timings(fire), frozen=frozen)).json()
    assert res["quality"] == "phe" and res["made"] == 0 and res["xp"] is None
    assert await qty(uid, "hoi_huyet_dan") == 0 and await qty(uid, "muc_tinh") == 3


async def test_without_recipe_ingredients_or_money_nothing_is_taken(client):
    h, uid = await player(client, stones=500)
    r = await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "no_recipe"
    await give(uid, "dp_hoi_huyet", 1)
    await give(uid, "truc_diep_thao", 1)
    await give(uid, "muc_tinh", 2)                       # needs 3
    r = await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "no_ingredient"
    assert await qty(uid, "truc_diep_thao") == 1 and await qty(uid, "muc_tinh") == 2 and await stones(uid) == 500
    await give(uid, "muc_tinh", 1)
    await set_stones(uid, 5)                              # the fee is 10
    r = await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "insufficient_funds"
    assert await qty(uid, "truc_diep_thao") == 1 and await qty(uid, "muc_tinh") == 3 and await stones(uid) == 5


async def test_a_fish_ingredient_takes_the_least_precious_fish(client, frozen):
    h, uid = await player(client, stones=500)
    await give(uid, "dp_khang_muc", 1)
    await give(uid, "muc_tinh", 2)
    await give(uid, "truc_diep_thao", 1)
    fish = catalog.fish()
    linh = sorted((fid for fid, f in fish.items() if f["rarity"] == "linh"), key=lambda f: (fish[f]["sell_price"], f))
    pham = next(fid for fid, f in fish.items() if f["rarity"] == "pham")
    await give(uid, f"fish_{pham}", 1)                    # too common to count
    await give(uid, f"fish_{linh[-1]}", 1)
    await give(uid, f"fish_{linh[0]}", 1)
    r = await client.post("/alchemy/start", json={"recipe_id": "khang_muc_dan"}, headers=h)
    assert r.status_code == 200, r.text
    assert await qty(uid, f"fish_{pham}") == 1
    if linh[0] != linh[-1]:
        assert await qty(uid, f"fish_{linh[0]}") == 0 and await qty(uid, f"fish_{linh[-1]}") == 1


async def test_a_breakthrough_pill_brews_on_the_fire_alone(client, frozen):
    h, uid = await player(client, "dan_hoa_than", stones=5000)
    from app import db as dbm
    from app.models import Character
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        ch.realm, ch.realm_stage = "nguyen_anh", 3
        await db.commit()
    r = catalog.recipes()["hoa_than_dan"]
    await give(uid, r["item"], 1)
    for ing in r["ingredients"]:
        await give(uid, ing["item"], ing["qty"])
    ov = (await client.get("/alchemy", headers=h)).json()
    e = next(x for x in ov["recipes"] if x["id"] == "hoa_than_dan")
    assert e["known"] and e["ready"]
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoa_than_dan"}, headers=h)).json()["fire"]
    assert await stones(uid) == 5000 - r["fee"]
    res = (await finish(client, h, fire, perfect_timings(fire), frozen=frozen)).json()
    assert res["quality"] == "thuong" and res["made"] >= 1
    assert await qty(uid, "hoa_than_dan") == res["made"]
    for ing in r["ingredients"]:
        assert await qty(uid, ing["item"]) == 0


async def test_realm_gate(client):
    h, uid = await player(client, stones=5000)
    await give(uid, "dp_kim_dan", 1)
    r = await client.post("/alchemy/start", json={"recipe_id": "kim_dan_dan"}, headers=h)
    assert r.json()["error"]["code"] == "realm_low"


async def test_finishing_faster_than_the_needle_can_run_is_refused(client, frozen):
    h, uid = await brewer(client)
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    r = await client.post("/alchemy/finish", json={"session_id": fire["session_id"], "timings": [9000, 9000, 9000]},
                          headers=h)
    assert r.json()["error"]["code"] == "too_fast"
    r = await client.post("/alchemy/finish", json={"session_id": fire["session_id"], "timings": [1, 2]}, headers=h)
    assert r.json()["error"]["code"] == "bad_timings"
    # still open: an honest finish works
    res = (await finish(client, h, fire, perfect_timings(fire), frozen=frozen)).json()
    assert res["quality"] == "thuong"


async def test_starting_again_resumes_the_same_fire(client):
    h, uid = await brewer(client)
    a = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()
    b = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()
    assert b["resumed"] and b["fire"]["session_id"] == a["fire"]["session_id"]
    assert await qty(uid, "truc_diep_thao") == 2            # taken once
    ov = (await client.get("/alchemy", headers=h)).json()
    assert ov["open"]["session_id"] == a["fire"]["session_id"]


async def test_a_fire_left_too_long_goes_out(client, frozen):
    h, uid = await brewer(client)
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    frozen.advance(seconds=C["session_seconds"] + 1)
    res = (await finish(client, h, fire, perfect_timings(fire))).json()
    assert res["expired"] and res["made"] == 0


async def test_brew_tu_vi_follows_quality_and_tu_linh(client, frozen):
    """Trung phẩm pays brew_xp["trung"]; under Tụ Linh Đan the same brew pays x1.5."""
    h, uid = await brewer(client)

    def trung(fire):     # perfect, perfect, then a miss: 4/6
        return perfect_timings(fire)[:2] + miss_timings(fire)[2:]
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    res = (await finish(client, h, fire, trung(fire), frozen=frozen)).json()
    assert res["quality"] == "trung" and res["xp"]["gained"] == C["brew_xp"]["trung"]
    await give(uid, "tu_linh_dan", 1)
    assert (await client.post("/inventory/use", json={"item_id": "tu_linh_dan"}, headers=h)).status_code == 200
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    res = (await finish(client, h, fire, trung(fire), frozen=frozen)).json()
    assert res["xp"]["gained"] == round(C["brew_xp"]["trung"] * C["buffs"]["tu_linh"]["xp_mult"])


async def test_far_from_any_furnace(client, monkeypatch):
    h, uid = await brewer(client)
    from app.realtime.world import world
    monkeypatch.setattr(world, "in_world", lambda u: True)
    monkeypatch.setattr(world, "near_npc", lambda u, npc, radius=56: False)
    r = await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "too_far"
    monkeypatch.setattr(world, "near_npc", lambda u, npc, radius=56: npc == "alchemist")
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    assert fire["furnace_level"] == C["public_furnace_level"]
    r = await client.post("/alchemy/furnace/upgrade", headers=h)
    assert r.json()["error"]["code"] == "not_home"


async def test_upgrading_the_furnace_widens_the_zones(client):
    h, uid = await brewer(client)
    lv2 = C["furnace"][1]
    r = await client.post("/alchemy/furnace/upgrade", headers=h)
    assert r.json()["error"]["code"] == "no_material"
    for m in lv2["materials"]:
        await give(uid, m["item"], m["qty"])
    await set_stones(uid, lv2["cost"]["spirit_stones"] + 10)
    r = await client.post("/alchemy/furnace/upgrade", headers=h)
    assert r.status_code == 200 and r.json()["furnace"]["level"] == 2
    assert await stones(uid) == 10 and await qty(uid, "muc_tinh") == 6     # the brewer's own 6 are left
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    assert fire["zones"][0]["width"] == C["zone_width"]["1"] + lv2["zone_bonus"] and fire["furnace_level"] == 2


async def test_brewing_counts_for_quests(client, frozen):
    """Đan Đạo: Mẻ đan đầu tiên takes any pill, the next step a Hồi Khí Đan only."""
    h, uid = await brewer(client)
    await give(uid, "dp_hoi_khi", 1)
    await give(uid, "go_linh_moc", 1)
    from app.models import Quest
    from app import db as dbm
    async with dbm.SessionLocal() as s:
        s.add(Quest(user_id=uid, quest_id="dd2_me_dan_dau", state="active", progress={"n": 0}))
        s.add(Quest(user_id=uid, quest_id="dd3_khac_van", state="active", progress={"n": 0}))
        await s.commit()
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    await finish(client, h, fire, perfect_timings(fire), frozen=frozen)
    qs = {x["id"]: x for x in (await client.get("/quests", headers=h)).json()["quests"]}
    assert qs["dd2_me_dan_dau"]["state"] == "done" and qs["dd3_khac_van"]["state"] == "active"
    assert qs["dd3_khac_van"]["objective"]["type"] == "brew"
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_khi_dan"}, headers=h)).json()["fire"]
    await finish(client, h, fire, perfect_timings(fire), frozen=frozen)
    qs = {x["id"]: x for x in (await client.get("/quests", headers=h)).json()["quests"]}
    assert qs["dd3_khac_van"]["state"] == "done"


def test_no_quest_asks_for_the_old_inscription():
    for chain in catalog.quests()["chains"].values():
        for st in chain["steps"]:
            assert st["objective"]["type"] != "inscribe", st["id"]
            for it in st["rewards"].get("items", []):
                assert catalog.stack_item(it["item"]) is not None, (st["id"], it)


# ------------------------------------------------------------------ the pills
async def _meditate_right(client, h) -> tuple[dict, dict]:
    q = (await client.post("/cultivation/meditate", headers=h)).json()
    assert "session_id" in q, q
    key = await answer_key(q["session_id"])
    res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                             headers=h)).json()
    return q, res


async def test_tu_linh_dan_gives_more_tu_vi_for_right_answers(client, frozen):
    h, uid = await player(client, "tu_linh", stones=0)
    await give(uid, "tu_linh_dan", 1)
    q, res = await _meditate_right(client, h)
    assert res["xp"]["gained"] == math_path.xp_for_tier(q["math"]["tier"])
    r = await client.post("/inventory/use", json={"item_id": "tu_linh_dan"}, headers=h)
    assert r.status_code == 200 and r.json()["buff"] == "tu_linh" and r.json()["seconds"] == C["buff_seconds"]
    frozen.advance(seconds=121)                              # one meditation question every 2 minutes
    q, res = await _meditate_right(client, h)
    assert res["xp"]["gained"] == round(math_path.xp_for_tier(q["math"]["tier"]) * C["buffs"]["tu_linh"]["xp_mult"])
    cult = (await client.get("/cultivation", headers=h)).json()
    assert cult["buffs"][0]["id"] == "tu_linh" and "skills" not in cult


async def test_ngo_tinh_dan_adds_seconds_to_every_question(client, frozen):
    h, uid = await player(client, "ngo_tinh")
    await give(uid, "ngo_tinh_dan", 1)

    def plain(q):
        return math_path.time_limit(q["qtype"], q["math"]["tier"])
    q1 = (await client.post("/cultivation/meditate", headers=h)).json()
    assert q1["time_limit"] == plain(q1)
    await client.post("/inventory/use", json={"item_id": "ngo_tinh_dan"}, headers=h)
    frozen.advance(seconds=121)
    q2 = (await client.post("/cultivation/meditate", headers=h)).json()
    assert q2["time_limit"] == plain(q2) + C["buffs"]["ngo_tinh"]["extra_seconds"]
    frozen.advance(seconds=C["buff_seconds"] + 1)            # it wears off
    q3 = (await client.post("/cultivation/meditate", headers=h)).json()
    assert q3["time_limit"] == plain(q3)


async def test_taking_the_same_buff_twice_stacks_up_to_two_doses(client):
    h, uid = await player(client)
    await give(uid, "khang_muc_dan", 3)
    secs = [(await client.post("/inventory/use", json={"item_id": "khang_muc_dan"}, headers=h)).json()["seconds"]
            for _ in range(3)]
    assert secs == [C["buff_seconds"], 2 * C["buff_seconds"], 2 * C["buff_seconds"]]


async def test_khang_muc_dan_softens_mac_kich():
    from app.realtime import combat
    from app.realtime.world import world
    from app.realtime.zone import Player
    p = Player(1, "a", {}, "luyen_khi", 0, 0)
    p.max_hp = 200
    m = type("M", (), {"info": {"rank": "normal"}})()
    plain = combat.mac_kich(p, m)
    p.buffs = {"khang_muc": world.mono() + 100}
    assert combat.mac_kich(p, m) == pytest.approx(plain * (1 - C["buffs"]["khang_muc"]["ink_res"] / 100))


async def test_phong_vuong_dan_feeds_a_bee(client, db):
    h, uid = await player(client)
    await client.get("/hive", headers=h)
    db.add(Bee(user_id=uid, bee_type="muc", level=1, xp=0, hive_slot=0, role="hive", bond=0, obtained_at=clock.now()))
    await db.commit()
    bee = (await db.execute(select(Bee).where(Bee.user_id == uid))).scalar_one()
    await give(uid, "phong_vuong_dan", 1)
    r = await client.post("/inventory/use", json={"item_id": "phong_vuong_dan"}, headers=h)
    assert r.json()["error"]["code"] == "bee_food"
    r = await client.post("/bees/feed", json={"bee_id": bee.id, "food": "phong_vuong_dan"}, headers=h)
    assert r.status_code == 200, r.text
    assert r.json()["xp_gained"] >= C["bee_food"]["phong_vuong_dan"]["xp"] and r.json()["levels_gained"] >= 1
    assert r.json()["bond"] >= C["bee_food"]["phong_vuong_dan"]["bond"]
