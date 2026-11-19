"""Stage 4: Tu Vi, realms, Thiên Kiếp, đả tọa, equipment, quests, Yêu Quái Phổ (spec 7.3, 7.4, 12)."""
import random

from sqlalchemy import select

from app import db as dbm
from app.models import Character, EquipmentInstance, InventoryItem, Quest, TribulationRun
from app.systems import cultivation, inventory, items
from tests.helpers import answer_key, correct_answer, register, wrong_answer
from tests.test_combat import LOOK, learn


async def make(client, name="tu_1", display="Tu Sĩ"):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": display, "appearance": LOOK}, headers=h)
    assert r.status_code == 200
    return h, data["user_id"]


async def setchar(uid, **kw):
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        for k, v in kw.items():
            setattr(ch, k, v)
        await db.commit()


async def getchar(uid):
    async with dbm.SessionLocal() as db:
        return await db.get(Character, uid)


async def give(uid, item, qty=1, bound=False):
    async with dbm.SessionLocal() as db:
        await inventory.change_item(db, uid, item, qty, "test", bound=bound)
        await db.commit()


# ------------------------------------------------------------------ Tu Vi
async def test_stages_advance_by_themselves_until_a_new_realm(client):
    h, uid = await make(client)
    async with dbm.SessionLocal() as db:
        r = await cultivation.add_xp(db, uid, 100)
        assert (r["realm"], r["stage"], r["xp"]) == ("luyen_khi", 1, 0) and r["stage_up"]
        r = await cultivation.add_xp(db, uid, 120 + 150 + 10)
        assert (r["realm"], r["stage"], r["xp"]) == ("luyen_khi", 3, 10)
        r = await cultivation.add_xp(db, uid, 100000)
        assert (r["realm"], r["stage"]) == ("luyen_khi", 9)
        assert r["bottleneck"] and r["xp"] == 500            # full Tu Vi, waiting for Thiên Kiếp
        await db.commit()
    ch = await getchar(uid)
    st = cultivation.stats_for("luyen_khi", 9, [])
    assert ch.max_hp == st["max_hp"] == 100 + 12 * 9 + 20


async def test_right_answers_anywhere_give_tu_vi(client):
    h, uid = await make(client, "tu_2", "Tu Hai")
    await learn(uid, ("水",))
    q = (await client.post("/quiz/practice", json={}, headers=h)).json()
    key = await answer_key(q["session_id"])
    r = (await client.post("/quiz/answer", json={"session_id": q["session_id"],
                                                "answer": correct_answer(q["qtype"], key)}, headers=h)).json()
    assert r["xp"]["gained"] == cultivation.cfg()["xp_per_correct"]["practice"]


# ------------------------------------------------------------------ Thiên Kiếp
async def bottleneck(uid):
    await setchar(uid, realm="luyen_khi", realm_stage=9, cultivation_xp=500)


async def run_tribulation(client, h, right: int):
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.status_code == 200, r.text
    q = r.json()["question"]
    assert q["time_limit"] == 30 and q["total"] == 20
    res = None
    for i in range(20):
        key = await answer_key(q["session_id"])
        ans = correct_answer(q["qtype"], key) if i < right else wrong_answer(q["qtype"], key)
        res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": ans},
                                 headers=h)).json()
        q = res.get("next")
    assert q is None
    return res["tribulation"]


async def test_tribulation_needs_full_tu_vi_and_pill(client):
    h, uid = await make(client, "tu_3", "Tu Ba")
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.json()["error"]["code"] == "no_tribulation"
    await setchar(uid, realm="luyen_khi", realm_stage=9, cultivation_xp=499)
    assert (await client.post("/cultivation/breakthrough/start", headers=h)).json()["error"]["code"] == "xp_not_full"
    await bottleneck(uid)
    assert (await client.post("/cultivation/breakthrough/start", headers=h)).json()["error"]["code"] == "no_pill"
    v = (await client.get("/cultivation", headers=h)).json()
    assert v["pill"] == "truc_co_dan" and not v["can_tribulation"]


async def test_tribulation_pass_at_80_percent(client):
    h, uid = await make(client, "tu_4", "Tu Bốn")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    assert (await client.get("/cultivation", headers=h)).json()["can_tribulation"]
    res = await run_tribulation(client, h, right=16)            # 16/20 = 80%
    assert res["passed"] and res["realm"] == "truc_co"
    ch = await getchar(uid)
    assert (ch.realm, ch.realm_stage, ch.cultivation_xp) == ("truc_co", 1, 0)
    async with dbm.SessionLocal() as db:
        qty = (await db.execute(select(InventoryItem.quantity).where(
            InventoryItem.user_id == uid, InventoryItem.item_id == "truc_co_dan"))).scalar_one()
        assert qty == 0                                          # the pill is used up
        from app.models import User
        assert (await db.get(User, uid)).immortal_jade == cultivation.cfg()["tribulation"]["reward_jade"]


async def test_bound_pill_is_used_too(client):
    h, uid = await make(client, "tu_11", "Tu Mười Một")
    await bottleneck(uid)
    await give(uid, "truc_co_dan", bound=True)                  # e.g. a quest reward
    res = await run_tribulation(client, h, right=20)
    assert res["passed"]
    async with dbm.SessionLocal() as db:
        left = (await db.execute(select(InventoryItem.quantity).where(
            InventoryItem.user_id == uid, InventoryItem.item_id == "truc_co_dan"))).scalars().all()
        assert sum(left) == 0


async def test_tribulation_fail_below_80_percent(client, frozen):
    h, uid = await make(client, "tu_5", "Tu Năm")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    res = await run_tribulation(client, h, right=15)            # 75%
    assert not res["passed"] and res["xp_lost"] == 50           # 10% of the stage's Tu Vi
    ch = await getchar(uid)
    assert (ch.realm, ch.realm_stage, ch.cultivation_xp) == ("luyen_khi", 9, 450)
    async with dbm.SessionLocal() as db:
        qty = (await db.execute(select(InventoryItem.quantity).where(
            InventoryItem.user_id == uid, InventoryItem.item_id == "truc_co_dan"))).scalar_one()
        assert qty == 1                                          # kept on failure
    await bottleneck(uid)
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.json()["error"]["code"] == "tribulation_wait"     # 30 minutes (TIME_SCALE)
    frozen.advance(minutes=31)
    assert (await client.post("/cultivation/breakthrough/start", headers=h)).status_code == 200


async def test_tribulation_timeout_counts_wrong_and_resumes(client, frozen):
    h, uid = await make(client, "tu_6", "Tu Sáu")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    q = (await client.post("/cultivation/breakthrough/start", headers=h)).json()["question"]
    frozen.advance(seconds=40)                                   # walked away: the question expired
    r = (await client.post("/cultivation/breakthrough/start", headers=h)).json()
    assert r["resumed"] and r["question"]["number"] == 2 and r["question"]["session_id"] != q["session_id"]
    async with dbm.SessionLocal() as db:
        run = (await db.execute(select(TribulationRun).where(TribulationRun.user_id == uid))).scalar_one()
        assert (run.index, run.correct) == (1, 0)



# ------------------------------------------------------------------ the eight realms
EIGHT = ["luyen_khi", "truc_co", "kim_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua"]


def test_the_realm_ladder_is_phàm_nhân_then_eight_realms():
    assert cultivation.order() == ["pham_nhan"] + EIGHT
    names = {r: cultivation.realm_name(r) for r in cultivation.order()}
    assert names == {"pham_nhan": "Phàm Nhân", "luyen_khi": "Luyện Khí", "truc_co": "Trúc Cơ", "kim_dan": "Kết Đan",
                     "nguyen_anh": "Nguyên Anh", "hoa_than": "Hóa Thần", "luyen_hu": "Luyện Hư",
                     "hop_the": "Hợp Thể", "dai_thua": "Đại Thừa"}
    assert cultivation.stage_label("kim_dan", 1) == "Kết Đan sơ kỳ"
    assert cultivation.stage_label("dai_thua", 3) == "Đại Thừa hậu kỳ"


def test_every_realm_has_every_per_realm_entry():
    """Adding a realm to realms_cultivation.json must never again silently give 0 of something
    (guard bees, stats) or a KeyError (last_stage) somewhere else."""
    import json
    from app import balance
    from app.config import DATA_DIR
    from app.realtime import world as wmod
    from app.systems import bees, gacha_service
    realms = catalog_realms()
    ids = [r["id"] for r in realms]
    assert wmod.realm_order() == ids
    c = cultivation.cfg()
    dev = balance._merge(json.loads((DATA_DIR / "balance" / "cultivation.json").read_text("utf-8")),
                         json.loads((DATA_DIR / "balance" / "dev" / "cultivation.json").read_text("utf-8")))
    slots = bees.cfg()["guard"]["slots_by_realm"]
    for i, r in enumerate(realms):
        rid = r["id"]
        assert r["name_vi"] and isinstance(r.get("hsk"), int), rid
        n = 1 if rid == "pham_nhan" else r["stages"]
        for prof, cc in (("default", c), ("dev", dev)):
            xs = cc["xp_to_next"].get(rid)
            assert xs is not None and len(xs) == n and all(x > 0 for x in xs), (prof, rid)
        assert rid in slots, rid
        assert rid in cultivation.REALM_TIER and rid in gacha_service.REALM_TIER, rid
        if rid != "pham_nhan":
            assert rid in c["stats"]["realm_bonus"], rid
        if i >= 2:                                   # Trúc Cơ and up: a pill and a Thiên Kiếp
            pill = c["tribulation_to"].get(rid)
            assert pill and catalog_pill(pill)["realm"] == rid and pill in catalog_recipes(), rid
    # every curve keeps climbing realm after realm
    for a, b in zip(ids[1:], ids[2:]):
        assert c["xp_to_next"][b][0] > c["xp_to_next"][a][-1], (a, b)
        assert slots[b] > slots[a], (a, b)
        for k, v in c["stats"]["realm_bonus"][a].items():
            assert c["stats"]["realm_bonus"][b].get(k, 0) >= v, (a, b, k)
        assert cultivation.stats_for(b, 1, [])["max_hp"] > cultivation.stats_for(a, 1, [])["max_hp"], (a, b)


def catalog_realms():
    from app.systems import catalog
    return catalog.realms()


def catalog_pill(pid):
    from app.systems import catalog
    return catalog.pills()[pid]


def catalog_recipes():
    from app.systems import catalog
    return catalog.recipes()


async def test_a_character_climbs_from_luyện_khí_to_the_last_stage_of_đại_thừa(client, frozen):
    """The real rule all the way up: Tu Vi fills each stage by itself; each new realm waits at
    full Tu Vi for its pill and a passed Thiên Kiếp."""
    h, uid = await make(client, "tu_thang", "Tu Thăng")
    async with dbm.SessionLocal() as db:
        await cultivation.add_xp(db, uid, cultivation.xp_needed("pham_nhan", 0))
        await db.commit()
    hp = 0
    for realm in EIGHT:
        ch = await getchar(uid)
        assert (ch.realm, ch.realm_stage, ch.cultivation_xp) == (realm, 1, 0)
        assert ch.max_hp > hp, realm                              # a new realm makes the body stronger
        hp = ch.max_hp
        for stage in range(1, cultivation.last_stage(realm) + 1):
            need = cultivation.xp_needed(realm, stage)
            async with dbm.SessionLocal() as db:
                r = await cultivation.add_xp(db, uid, need)
                await db.commit()
            if stage < cultivation.last_stage(realm):
                assert (r["realm"], r["stage"], r["xp"]) == (realm, stage + 1, 0) and r["stage_up"], r
                ch = await getchar(uid)
                assert ch.max_hp > hp, (realm, stage)
                hp = ch.max_hp
        if realm == "dai_thua":
            break
        assert r["bottleneck"] and (r["realm"], r["xp"]) == (realm, need), r
        v = (await client.get("/cultivation", headers=h)).json()
        nxt = EIGHT[EIGHT.index(realm) + 1]
        assert v["next_realm"] == nxt and not v["can_tribulation"] and v["pill"] == cultivation.cfg()["tribulation_to"][nxt]
        await give(uid, v["pill"])
        assert (await client.get("/cultivation", headers=h)).json()["can_tribulation"]
        res = await run_tribulation(client, h, right=20)
        assert res["passed"] and res["realm"] == nxt and res["label"] == cultivation.stage_label(nxt, 1), res
        frozen.advance(seconds=5)
    ch = await getchar(uid)
    assert (ch.realm, ch.realm_stage) == ("dai_thua", 3)
    assert ch.max_hp == cultivation.stats_for("dai_thua", 3, [])["max_hp"]
    v = (await client.get("/cultivation", headers=h)).json()
    assert v["label"] == "Đại Thừa hậu kỳ" and v["realm_name"] == "Đại Thừa" and v["pill"] is None
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.json()["error"]["code"] == "no_tribulation"          # the top of the ladder


# ------------------------------------------------------------------ đả tọa
async def test_meditation(client, frozen):
    h, uid = await make(client, "tu_7", "Tu Bảy")
    await learn(uid, ("水",))
    r = (await client.post("/cultivation/meditate", headers=h)).json()
    assert r["context"] == "meditate"
    key = await answer_key(r["session_id"])
    res = (await client.post("/quiz/answer", json={"session_id": r["session_id"],
                                                  "answer": correct_answer(r["qtype"], key)}, headers=h)).json()
    assert res["xp"]["gained"] == 15 and res["next_in"] > 0
    again = await client.post("/cultivation/meditate", headers=h)
    assert again.json()["error"]["code"] == "meditate_wait"      # one question every 2 minutes, no AFK Tu Vi
    frozen.advance(seconds=121)
    assert (await client.post("/cultivation/meditate", headers=h)).status_code == 200
    await setchar(uid, zone_id="truc_lam_thon")
    frozen.advance(seconds=121)
    assert (await client.post("/cultivation/meditate", headers=h)).json()["error"]["code"] == "not_home"


# ------------------------------------------------------------------ equipment
async def test_equip_and_enhance(client):
    h, uid = await make(client, "tu_8", "Tu Tám")
    async with dbm.SessionLocal() as db:
        e = await items.grant_equipment(db, uid, "but_long_go", "linh", "test")
        await db.commit()
    inv = (await client.get("/inventory", headers=h)).json()
    assert inv["equipment"][0]["stats"] == {"atk": round(6 * 1.3)}
    base_atk = (await client.get("/cultivation", headers=h)).json()["stats"]["atk"]
    r = (await client.post("/equipment/equip", json={"instance_id": e["id"]}, headers=h)).json()
    assert r["stats"]["atk"] == base_atk + 8 and r["stats"]["weapon"] == "brush"
    # enhancing: costs Mực Tinh + Linh Thạch; failing keeps the item and its level
    assert (await client.post("/forge/enhance", json={"instance_id": e["id"]}, headers=h)).json()["error"]["code"] \
        == "no_material"
    await give(uid, "muc_tinh", 50)
    async with dbm.SessionLocal() as db:
        from app.models import User
        user = await db.get(User, uid)
        user.spirit_stones = 10000
        inst = await db.get(EquipmentInstance, e["id"])
        inst.enhance_level = 9                                    # last level: 20% chance
        await db.commit()
        rng = random.Random(2)  # first roll 0.96: a failure
        results = []
        for _ in range(12):
            user = await db.get(User, uid)
            res = await items.enhance(db, user, e["id"], rng)
            results.append(res["success"])
            if res["success"]:
                break
            assert res["item"]["enhance"] == 9
        await db.commit()
    assert results[-1] and results.count(False) >= 1
    r = (await client.post("/equipment/unequip", json={"slot": "weapon"}, headers=h)).json()
    assert r["stats"]["atk"] == base_atk and r["stats"]["weapon"] is None


# ------------------------------------------------------------------ quests & codex
async def test_quest_talk_needs_to_be_near(client):
    h, uid = await make(client, "tu_9", "Tu Chín")
    qs = (await client.get("/quests", headers=h)).json()["quests"]
    assert qs[0]["id"] == "nm1_xuong_lang" and qs[0]["state"] == "active"
    r = await client.post("/quests/talk", json={"npc": "truc_lao"}, headers=h)
    assert r.json()["error"]["code"] == "too_far"
    from app.realtime.zone import Player
    from app.realtime.world import world
    from app.realtime import maps

    class Ch:
        map = maps.load("truc_lam_thon")
    x, y = Ch.map.npcs["truc_lao"]
    world.players[uid] = Player(uid, "Tu Chín", {}, "pham_nhan", x, y + 10)
    world.players[uid].channel = Ch()
    try:
        r = (await client.post("/quests/talk", json={"npc": "truc_lao"}, headers=h)).json()
        assert r["finished"][0]["id"] == "nm1_xuong_lang"
    finally:
        world.players.pop(uid, None)
    r = (await client.post("/quests/claim", json={"quest_id": "nm1_xuong_lang"}, headers=h)).json()
    assert r["rewards"]["equipment"][0]["item_id"] == "but_long_go" and r["next"]["id"] == "nm2_muc_con"
    assert (await client.post("/quests/claim", json={"quest_id": "nm1_xuong_lang"}, headers=h)).status_code == 400
    async with dbm.SessionLocal() as db:
        assert (await db.get(Quest, (uid, "nm2_muc_con"))).state == "active"


async def test_monster_book_hides_unmet(client):
    h, uid = await make(client, "tu_10", "Tu Mười")
    b = (await client.get("/codex/monster", headers=h)).json()
    from app.systems import td   # the book also lists the Mặc Quái of the Thủ Vườn levels (stage 7)
    # every monster the game has: 3 of the forest, 3 of a bí cảnh (stage 9), the 9 quái lỗi
    # sai of Loạn Số Cốc (M7), plus the Mặc Quái of the Thủ Vườn levels (stage 7)
    from app.systems import catalog as cat
    assert b["total"] == len(cat.monsters()) + len(td.cfg()["monsters"])
    assert b["found"] == 0 and "name_vi" not in b["entries"][0]
    async with dbm.SessionLocal() as db:
        from app.systems import codex
        await codex.meet_monster(db, uid, "tone_wisp")
        await db.commit()
    b = (await client.get("/codex/monster", headers=h)).json()
    e = next(x for x in b["entries"] if x["id"] == "tone_wisp")
    assert e["found"] and e["name_vi"] == "Thanh Điệu Yêu" and "Chọn thanh điệu" in e["qtypes_vi"]
