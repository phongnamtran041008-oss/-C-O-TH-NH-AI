"""Stage 4: Tu Vi, realms, Thiên Kiếp, đả tọa, equipment, quests, Yêu Quái Phổ (spec 7.3, 7.4, 12)."""
import random

from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_path
from app.models import Character, EquipmentInstance, InventoryItem, MathAnswer, Quest, TribulationRun
from app.systems import cultivation, inventory, items, math_ask, math_combat, math_practice
from tests.helpers import answer_key, old_script, register
from tests.test_combat import LOOK
from tests.test_math_loop import right_answer, wrong_answer


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


# ------------------------------------------------------------------ Thiên Kiếp
async def bottleneck(uid):
    await setchar(uid, realm="luyen_khi", realm_stage=9, cultivation_xp=500)


async def run_tribulation(client, h, right: int):
    """Answer a whole Thiên Kiếp: the first `right` questions right, the others wrong. Every
    question is a quick math question with its own time limit, and no answer pays Tu Vi."""
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.status_code == 200, r.text
    q = r.json()["question"]
    assert q["total"] == 20 and q["number"] == 1
    res = None
    for i in range(20):
        assert q["context"] == cultivation.TRIBULATION_CONTEXT and q["number"] == i + 1, q
        assert q["qtype"] in math_combat.QUICK_TYPES and not old_script(q)
        assert q["time_limit"] == math_path.time_limit(q["qtype"], q["math"]["tier"])
        key = await answer_key(q["session_id"])
        ans = right_answer(q, key) if i < right else wrong_answer(q, key)
        res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": ans},
                                 headers=h)).json()
        assert res["correct"] == (i < right) and "xp" not in res          # the realm is the prize
        assert res["math"]["tier"] == q["math"]["tier"]                   # written to the learning log
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
    r = (await client.post("/cultivation/breakthrough/start", headers=h)).json()
    assert r["resumed"] and r["question"]["session_id"] == q["session_id"]      # still open: the same one
    frozen.advance(seconds=q["time_limit"] + 10)                 # walked away: the question expired
    r = (await client.post("/cultivation/breakthrough/start", headers=h)).json()
    assert r["resumed"] and r["question"]["number"] == 2 and r["question"]["session_id"] != q["session_id"]
    async with dbm.SessionLocal() as db:
        run = (await db.execute(select(TribulationRun).where(TribulationRun.user_id == uid))).scalar_one()
        assert (run.index, run.correct) == (1, 0) and run.total == 20
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalar_one()
        assert a.timed_out and not a.correct                      # the timeout is in the learning log


async def test_a_tribulation_asks_the_hardest_question_this_player_may_get(client):
    """highest=True: one micro-skill of the player's own part has tier 2 open, so every
    question of the run is from that skill at tier 2, never above what the player opened."""
    h, uid = await make(client, "tu_12", "Tu Mười Hai")
    async with dbm.SessionLocal() as db:
        part = await math_ask.own_part(db, uid)
    quick = [t for t in math_practice._templates(part.subject_id, part.floor) if t.qtype in math_combat.QUICK_TYPES]
    skill = next(k for k in part.skills if any(t.skill == k and t.tier == 2 for t in quick))
    window = math_path.cfg()["tier_unlock"]["window"]
    async with dbm.SessionLocal() as db:
        for n in range(window):                      # a full window of right answers at tier 1
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=part.subject_id, skill_id=skill,
                              floor=part.floor, tier=1, item_id=f"x{n}", qtype="true_false", fingerprint=f"f{n}",
                              correct=True, timed_out=False, review=False, answer_ms=800,
                              answered_at=clock.now()))
        await db.commit()
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    q = (await client.post("/cultivation/breakthrough/start", headers=h)).json()["question"]
    for _ in range(3):
        assert (q["math"]["skill"], q["math"]["tier"], q["math"]["floor"]) == (skill, 2, part.floor), q["math"]
        key = await answer_key(q["session_id"])
        q = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                               headers=h)).json()["next"]


async def test_no_math_question_means_no_tribulation(client, monkeypatch):
    h, uid = await make(client, "tu_13", "Tu Mười Ba")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    monkeypatch.setattr(math_practice, "_templates", lambda subject, floor: [])
    r = await client.post("/cultivation/breakthrough/start", headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_math_question"
    assert "chữ" not in r.json()["error"]["message_vi"]
    async with dbm.SessionLocal() as db:            # refused before a run or a cooldown exists
        assert (await db.execute(select(TribulationRun).where(TribulationRun.user_id == uid))).first() is None
        assert (await db.get(Character, uid)).tribulation_retry_at is None
    monkeypatch.undo()
    assert (await client.post("/cultivation/breakthrough/start", headers=h)).status_code == 200


async def test_a_run_whose_bank_runs_dry_ends_without_a_verdict(client, monkeypatch):
    h, uid = await make(client, "tu_14", "Tu Mười Bốn")
    await bottleneck(uid)
    await give(uid, "truc_co_dan")
    q = (await client.post("/cultivation/breakthrough/start", headers=h)).json()["question"]
    key = await answer_key(q["session_id"])
    monkeypatch.setattr(math_practice, "_templates", lambda subject, floor: [])
    res = (await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                             headers=h)).json()
    assert "next" not in res and res["tribulation"]["aborted"] and res["tribulation"]["xp_lost"] == 0
    ch = await getchar(uid)
    assert ch.realm == "luyen_khi" and ch.cultivation_xp == 500 and ch.tribulation_retry_at is None
    async with dbm.SessionLocal() as db:
        run = (await db.execute(select(TribulationRun).where(TribulationRun.user_id == uid))).scalar_one()
        assert run.result == "aborted" and run.finished_at is not None
        assert (await db.execute(select(InventoryItem.quantity).where(
            InventoryItem.user_id == uid, InventoryItem.item_id == "truc_co_dan"))).scalar_one() == 1



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
    from app.systems import bees
    realms = catalog_realms()
    ids = [r["id"] for r in realms]
    assert wmod.realm_order() == ids
    c = cultivation.cfg()
    dev = balance._merge(json.loads((DATA_DIR / "balance" / "cultivation.json").read_text("utf-8")),
                         json.loads((DATA_DIR / "balance" / "dev" / "cultivation.json").read_text("utf-8")))
    slots = bees.cfg()["guard"]["slots_by_realm"]
    for i, r in enumerate(realms):
        rid = r["id"]
        assert r["name_vi"] and isinstance(r.get("stages"), int), rid
        n = 1 if rid == "pham_nhan" else r["stages"]
        for prof, cc in (("default", c), ("dev", dev)):
            xs = cc["xp_to_next"].get(rid)
            assert xs is not None and len(xs) == n and all(x > 0 for x in xs), (prof, rid)
        assert rid in slots, rid
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
    """One quick math question at the player's own floor (nothing else needed); a right
    answer pays Tu Vi by tier, counts for the quest and is written to the learning log."""
    h, uid = await make(client, "tu_7", "Tu Bảy")
    r = (await client.post("/cultivation/meditate", headers=h)).json()
    assert r["context"] == cultivation.MEDITATE_CONTEXT and r["qtype"] in math_combat.QUICK_TYPES
    async with dbm.SessionLocal() as db:
        assert (r["math"]["subject"], r["math"]["floor"]) == await math_ask.own_floor(db, uid)
    key = await answer_key(r["session_id"])
    res = (await client.post("/quiz/answer", json={"session_id": r["session_id"],
                                                  "answer": right_answer(r, key)}, headers=h)).json()
    assert res["xp"]["gained"] == math_path.xp_for_tier(r["math"]["tier"]) and res["next_in"] > 0
    async with dbm.SessionLocal() as db:
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalar_one()
        assert a.correct and a.run_id is None and a.skill_id == r["math"]["skill"]
    again = await client.post("/cultivation/meditate", headers=h)
    assert again.json()["error"]["code"] == "meditate_wait"      # one question every 2 minutes, no AFK Tu Vi
    frozen.advance(seconds=121)
    assert (await client.post("/cultivation/meditate", headers=h)).status_code == 200
    await setchar(uid, zone_id="truc_lam_thon")
    frozen.advance(seconds=121)
    assert (await client.post("/cultivation/meditate", headers=h)).json()["error"]["code"] == "not_home"


async def test_meditation_counts_for_the_quest_and_says_when_there_is_no_question(client, frozen, monkeypatch):
    h, uid = await make(client, "tu_7b", "Tu Bảy Bis")
    async with dbm.SessionLocal() as db:
        db.add(Quest(user_id=uid, quest_id="nm4_da_toa", state="active", progress={"n": 1}))   # one right answer to go
        await db.commit()
    r = (await client.post("/cultivation/meditate", headers=h)).json()
    key = await answer_key(r["session_id"])
    await client.post("/quiz/answer", json={"session_id": r["session_id"], "answer": right_answer(r, key)}, headers=h)
    async with dbm.SessionLocal() as db:
        assert (await db.get(Quest, (uid, "nm4_da_toa"))).state == "done"
    frozen.advance(seconds=121)
    monkeypatch.setattr(math_practice, "_templates", lambda subject, floor: [])
    r = await client.post("/cultivation/meditate", headers=h)
    err = r.json()["error"]
    assert r.status_code == 400 and err["code"] == "no_math_question"
    assert "chữ" not in err["message_vi"] and "vườn" not in err["message_vi"]
    monkeypatch.undo()
    assert (await client.post("/cultivation/meditate", headers=h)).status_code == 200   # no cooldown was spent


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
    from app.systems import td   # the book also lists the Mặc Quái of the Thủ Thành Toán levels (stage 7)
    # every monster the game has: 3 of the forest, 3 of a bí cảnh (stage 9), the 9 quái lỗi
    # sai of Loạn Số Cốc (M7), plus the Mặc Quái of the Thủ Thành Toán levels (stage 7)
    from app.systems import catalog as cat
    assert b["total"] == len(cat.monsters()) + len(td.cfg()["monsters"])
    assert b["found"] == 0 and "name_vi" not in b["entries"][0]
    async with dbm.SessionLocal() as db:
        from app.systems import codex
        await codex.meet_monster(db, uid, "tone_wisp")
        await db.commit()
    b = (await client.get("/codex/monster", headers=h)).json()
    e = next(x for x in b["entries"] if x["id"] == "tone_wisp")
    assert e["found"] and e["name_vi"] == "Lân Hỏa Yêu" and "qtypes_vi" not in e and e["weakness_vi"]
    assert not any("qtypes_vi" in x for x in b["entries"]) and not old_script(b["entries"])
