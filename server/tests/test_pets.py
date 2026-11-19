"""Stage 8: Linh Thú (spec 13, 6.8). The banner, the 12 con giáp, duplicates, wearing one pet, its
combat bonus, and each skill where it acts. No skill answers or skips a question.

Six skills used to act in the old word garden; since the purge they act on loops that live on:
Chuột (Linh Thú banner), Trâu (Hầm Ngục stones), Hổ (failed Thiên Kiếp), Rồng (a streak of right
math answers), Gà (meditation), Lợn (selling to the village)."""
import math
import random
from collections import Counter
from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app import balance
from app import db as dbm
from app.models import Character, CodexEntry, Pet, QuizSession, User
from app.systems import catalog, cultivation, inventory, math_dungeon, pets
from app.systems.gacha import Banner
from tests.econ_helpers import player, stones
from tests.helpers import answer_key, old_script
from tests.test_math_loop import right_answer, wrong_answer

SP = catalog.pets()["species"]


async def make(client, name, display=None):
    return await player(client, name)


async def getchar(uid):
    async with dbm.SessionLocal() as db:
        return await db.get(Character, uid)


async def bottleneck(uid):
    """Luyện Khí 9 with full Tu Vi (500): waiting for Thiên Kiếp."""
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        ch.realm, ch.realm_stage, ch.cultivation_xp = "luyen_khi", 9, 500
        await db.commit()


async def give(uid, item, qty=1):
    async with dbm.SessionLocal() as db:
        await inventory.change_item(db, uid, item, qty, "test")
        await db.commit()


async def run_tribulation(client, h, right: int) -> dict:
    """A whole Thiên Kiếp: the first `right` questions right, the others wrong."""
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.status_code == 200, r.text
    q, res, i = r.json()["question"], None, 0
    while q is not None:
        key = await answer_key(q["session_id"])
        ans = right_answer(q, key) if i < right else wrong_answer(q, key)
        res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": ans},
                                 headers=h)).json()
        q, i = res.get("next"), i + 1
    assert i == 20
    return res["tribulation"]


async def give_pet(db, uid, kind, level=1, equipped=True) -> int:
    p = Pet(user_id=uid, pet_type=kind, level=level, equipped=equipped)
    db.add(p)
    await db.commit()
    return p.id


async def wear(uid, kind):
    async with dbm.SessionLocal() as db:
        await give_pet(db, uid, kind)


def test_twelve_zodiac_pets_with_the_banner_rarities():
    assert len(SP) == 12
    b = balance.gacha()["banners"]["pets"]
    assert b["enabled"] and b["price"] == {"spirit_stones": 500} and b["alt_price"] == {"immortal_jade": 10}
    assert {s["rarity"] for s in SP.values()} == set(b["rarities"])
    assert [s["zodiac_vi"] for s in SP.values()] == ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân",
                                                    "Dậu", "Tuất", "Hợi"]
    assert SP["rong"]["rarity"] == "legendary"
    assert SP["chuot"]["skill"] == {"type": "pet_rare", "value": 0.05}
    assert SP["trau"]["skill"] == {"type": "dungeon_stones", "value": 0.2}
    assert SP["ho"]["skill"] == {"type": "tribulation_guard", "value": 0.5}
    assert SP["rong"]["skill"] == {"type": "streak_double", "every": 5}
    assert SP["ga"]["skill"] == {"type": "xp_meditate", "value": 0.1}
    assert SP["lon"]["skill"] == {"type": "sell_stones", "value": 0.1}
    assert len({s["skill"]["type"] for s in SP.values()}) == 12


def test_no_words_in_the_pet_data():
    for pid, s in SP.items():
        assert not old_script(s), pid
        low = s["skill_vi"].lower()
        assert not any(w in low for w in ("vườn", "hạt", "quả", "chữ")), (pid, s["skill_vi"])
    assert not old_script(catalog.pets())


def test_banner_rates_hold_over_many_rolls():
    banner = Banner.load("pets")
    rng = random.Random(8)
    got, _ = banner.roll(100_000, {}, rng, use_pity=False)
    n = Counter(got)
    for r, p in banner.rates.items():
        assert abs(n[r] / 100_000 - p) < 0.01, r


async def test_rolling_gives_pets_levels_duplicates_and_codex(client, db):
    h, uid = await player(client, "thu_nuoi", stones=60_000)
    seen = Counter()
    for _ in range(12):
        r = await client.post("/gacha/roll", json={"banner": "pets", "count": 10}, headers=h)
        assert r.status_code == 200, r.text
        for res in r.json()["results"]:
            seen[res["pet_type"]] += 1
            assert res["rarity"] == SP[res["pet_type"]]["rarity"]
            assert not old_script(res)
    rows = (await db.execute(select(Pet).where(Pet.user_id == uid))).scalars().all()
    assert len(rows) == len(seen)                         # one row per species
    for p in rows:
        assert p.level == min(catalog.pets()["max_level"], seen[p.pet_type])
    codex = (await db.execute(select(CodexEntry).where(CodexEntry.user_id == uid, CodexEntry.codex == "pet"))
             ).scalars().all()
    assert {c.entry_id for c in codex} == set(seen)
    ov = (await client.get("/pets", headers=h)).json()
    assert ov["found"] == len(seen) and ov["total"] == 12
    hidden = [b for b in ov["book"] if not b["found"]]
    assert all("name_vi" not in b and "skill_vi" not in b for b in hidden)
    assert not old_script(ov["book"] + ov["pets"])


async def test_a_copy_past_the_top_level_becomes_stones(client, db):
    h, uid = await player(client, "thu_day", stones=0)
    await give_pet(db, uid, "chuot", level=catalog.pets()["max_level"], equipped=False)
    user = await db.get(User, uid)
    out = await pets.resolve_gacha(db, user, ["common"], type("R", (), {"choice": staticmethod(lambda xs: "chuot")})())
    await db.commit()
    assert out[0]["stones"] == catalog.pets()["dupe_stones"]["common"]
    assert await stones(uid) == catalog.pets()["dupe_stones"]["common"]


async def test_wearing_one_pet_adds_its_stats(client, db):
    h, uid = await player(client, "thu_deo")
    a = await give_pet(db, uid, "ho", level=1, equipped=False)
    b = await give_pet(db, uid, "trau", level=3, equipped=False)
    base = (await client.get("/cultivation", headers=h)).json()["stats"]
    r = await client.post("/pets/equip", json={"pet_id": a}, headers=h)
    assert r.status_code == 200 and r.json()["equipped"] == a
    st = (await client.get("/cultivation", headers=h)).json()
    assert st["stats"]["atk"] == base["atk"] + SP["ho"]["stats"]["atk"] and st["pet"]["pet_type"] == "ho"
    r = await client.post("/pets/equip", json={"pet_id": b}, headers=h)
    assert r.json()["equipped"] == b
    worn = (await db.execute(select(Pet).where(Pet.user_id == uid, Pet.equipped.is_(True)))).scalars().all()
    assert [p.id for p in worn] == [b]                    # only one at a time
    st = (await client.get("/cultivation", headers=h)).json()["stats"]
    mult = 1 + catalog.pets()["stat_per_level"] * 2
    assert st["def"] == base["def"] + round(SP["trau"]["stats"]["def"] * mult) and st["atk"] == base["atk"]
    r = await client.post("/pets/equip", json={"pet_id": None}, headers=h)
    assert r.json()["equipped"] is None
    h2, _ = await player(client, "ke_khac")
    r = await client.post("/pets/equip", json={"pet_id": a}, headers=h2)
    assert r.json()["error"]["code"] == "no_pet"


# ------------------------------------------------------------------ the six replaced skills
class _Lucky:
    """An rng whose random() is always `r` and whose choice() takes the first species."""

    def __init__(self, r: float):
        self.r = r

    def random(self):
        return self.r

    def choice(self, xs):
        return xs[0]


async def test_chuot_moves_five_percent_of_the_pet_banner_from_common_to_rare(client, db):
    common = balance.gacha()["banners"]["pets"]["rates"]["common"]
    assert pets.rare_upgrade_chance(0.05) == pytest.approx(0.05 / common)
    assert pets.rare_upgrade_chance(0.0) == 0.0
    h, uid = await player(client, "chu_chuot", stones=0)
    user = await db.get(User, uid)
    just_under = 0.05 / common - 1e-6
    out = await pets.resolve_gacha(db, user, ["common"], _Lucky(just_under))
    assert out[0]["rarity"] == "common"                   # no Chuột: nothing changes
    await give_pet(db, uid, "chuot", equipped=True)
    out = await pets.resolve_gacha(db, user, ["common", "epic"], _Lucky(just_under))
    assert out[0]["rarity"] == "rare" and SP[out[0]["pet_type"]]["rarity"] == "rare"
    assert out[1]["rarity"] == "epic"                     # only Common is touched
    out = await pets.resolve_gacha(db, user, ["common"], _Lucky(0.05 / common + 1e-6))
    assert out[0]["rarity"] == "common"
    # over many rolls: P(Rare) grows by 5 points, P(Common) shrinks by the same
    rng = random.Random(5)
    lucky = pets.rare_upgrade_chance(0.05)
    n = 200_000
    up = sum(1 for _ in range(n) if rng.random() < common and rng.random() < lucky)
    assert up / n == pytest.approx(0.05, abs=0.003)
    assert balance.gacha()["banners"]["pets"]["rates"]["common"] == common   # the config is untouched


async def test_trau_adds_20_percent_to_ham_nguc_stones(client, db):
    h, uid = await player(client, "chu_trau", stones=0)

    def run():
        return SimpleNamespace(id=1, rewarded=True, stones_gained=0, items_gained={})

    r1 = run()
    plain = await math_dungeon._grant(db, uid, r1, {"stones": 50, "items": {}}, "room")
    assert plain["stones"] == 50 and r1.stones_gained == 50
    await give_pet(db, uid, "trau")
    r2 = run()
    more = await math_dungeon._grant(db, uid, r2, {"stones": 50, "items": {}}, "chest")
    assert more["stones"] == 60 and r2.stones_gained == 60
    await db.commit()
    assert await stones(uid) == 110
    withheld = SimpleNamespace(id=2, rewarded=False, stones_gained=0, items_gained={})
    assert (await math_dungeon._grant(db, uid, withheld, {"stones": 50, "items": {}}, "room"))["stones"] == 0


async def test_ho_halves_the_tu_vi_lost_on_a_failed_tribulation(client, frozen):
    h, uid = await make(client, "chu_ho", "Chủ Hổ")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    await wear(uid, "ho")
    res = await run_tribulation(client, h, right=15)            # 75%: failed
    assert not res["passed"] and res["xp_lost"] == 25           # half of the usual 10% (50)
    assert (await getchar(uid)).cultivation_xp == 475


async def _meditate(client, h, frozen, right=True) -> dict:
    frozen.advance(seconds=121)
    r = await client.post("/cultivation/meditate", headers=h)
    assert r.status_code == 200, r.text
    q = r.json()
    key = await answer_key(q["session_id"])
    ans = right_answer(q, key) if right else wrong_answer(q, key)
    res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": ans}, headers=h)).json()
    assert res["correct"] == right
    return res


async def test_ga_adds_ten_percent_tu_vi_to_meditation(client, frozen):
    h, uid = await make(client, "chu_ga", "Chủ Gà")
    plain = await _meditate(client, h, frozen)
    assert "pet_xp" not in plain["math"]
    await wear(uid, "ga")
    before = (await getchar(uid)).cultivation_xp
    res = await _meditate(client, h, frozen)
    base = res["xp"]["gained"]
    assert res["math"]["pet_skill"] == "xp_meditate" and res["math"]["pet_xp"] == math.ceil(base * 0.1)
    if not res["xp"]["stage_up"]:                   # both parts reached the Tu Vi bar
        assert (await getchar(uid)).cultivation_xp == before + base + res["math"]["pet_xp"]
    wrong = await _meditate(client, h, frozen, right=False)
    assert "pet_xp" not in wrong["math"]


async def test_rong_doubles_the_tu_vi_of_every_fifth_right_math_answer_in_a_row(client, frozen):
    h, uid = await make(client, "chu_rong", "Chủ Rồng")
    await wear(uid, "rong")
    got = [await _meditate(client, h, frozen) for _ in range(5)]
    assert all("pet_xp" not in r["math"] for r in got[:4])
    assert got[4]["math"]["pet_skill"] == "streak_double" and got[4]["math"]["pet_xp"] == got[4]["xp"]["gained"]
    # a wrong answer breaks the streak: four right after it are not enough
    await _meditate(client, h, frozen, right=False)
    got = [await _meditate(client, h, frozen) for _ in range(4)]
    assert all("pet_xp" not in r["math"] for r in got)
    assert "pet_xp" in (await _meditate(client, h, frozen))["math"]


async def test_rong_streak_counts_any_math_context_and_keeps_through_answers_without_tu_vi(client, db):
    """on_math_answer, the hook of every math mode's learning log: an answer that pays no Tu Vi
    (a Thiên Kiếp question) keeps the streak for the next one that does."""
    h, uid = await player(client, "rong_2")
    await give_pet(db, uid, "rong")
    user = await db.get(User, uid)

    def sess(context):
        return QuizSession(id="x", user_id=uid, context=context, qtype="MC", item_id="i",
                           payload={"math": {"tier": 1}}, answer_key={})
    for _ in range(4):
        assert await pets.on_math_answer(db, user, sess("math_combat"), True) == {}
    assert await pets.on_math_answer(db, user, sess(cultivation.TRIBULATION_CONTEXT), True) == {}   # 0 Tu Vi
    out = await pets.on_math_answer(db, user, sess("math_combat"), True)
    assert out == {"pet_xp": 3, "pet_skill": "streak_double"}           # tier 1 pays 3
    assert user.flags["pet_streak"] == 0


async def test_lon_sells_to_the_village_for_more(client, db):
    h, uid = await player(client, "chu_lon", stones=0)
    await inventory.change_item(db, uid, "fish_ca_chep", 6, "test")
    await db.commit()
    price = catalog.stack_item("fish_ca_chep")["sell_price"]
    r = (await client.post("/inventory/sell", json={"item_id": "fish_ca_chep", "qty": 3}, headers=h)).json()
    assert r["earned"] == 3 * price
    await give_pet(db, uid, "lon")
    r = (await client.post("/inventory/sell", json={"item_id": "fish_ca_chep", "qty": 3}, headers=h)).json()
    assert r["earned"] == round(3 * price * 1.1)


# ------------------------------------------------------------------ the other six
async def test_combat_pets_ran_cho_ngua():
    from app.realtime import combat
    from app.realtime.zone import Player
    p = Player(1, "a", {}, "luyen_khi", 0, 0)
    p.max_hp = 200
    m = type("M", (), {"info": {"rank": "normal"}, "bee_assist": {}})()
    plain = combat.mac_kich(p, m)
    p.pet = "ran"
    assert combat.mac_kich(p, m) == pytest.approx(plain * 0.8)
    p.pet = "cho"
    assert combat._loot_bonus(p, m)["drop_mult"] == pytest.approx(1.15)
    p.pet = "ngua"
    assert combat._loot_bonus(p, m)["stones_pct"] == pytest.approx(15)


async def test_de_and_meo_skills_are_wired(client, db):
    assert await pets.skill_value(db, 999999, "honey") == 0.0
    h, uid = await player(client, "chu_de")
    await give_pet(db, uid, "de")
    assert await pets.skill_value(db, uid, "honey") == pytest.approx(0.15)
    assert await pets.skill_value(db, uid, "fish_luck") == 0.0
