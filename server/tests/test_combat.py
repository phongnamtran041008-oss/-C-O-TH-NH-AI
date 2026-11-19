"""Stage 4: Vấn Đạo combat (spec 8.1). A real database and the real quiz service; the
world runs with a fake clock and its tick is called by hand."""
import asyncio

import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.learning import math_path
from app.models import Character, CodexEntry, InventoryItem, MathAnswer, Quest
from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.world import Session, World
from app.systems import catalog
from tests.helpers import answer_key, register

FOREST = "rung_muc_loang"
LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}


class FakeMono:
    def __init__(self):
        self.t = 5000.0

    def __call__(self):
        return self.t


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


async def settle(w: World) -> None:
    for _ in range(30):
        if not w._bg:
            return
        await asyncio.gather(*list(w._bg), return_exceptions=True)


def run(w: World, seconds: float, dt_: float = 0.05) -> None:
    for _ in range(round(seconds / dt_)):
        w.mono.t += dt_
        w.tick(dt_)


async def fighter(client, w: World, username: str, display: str, learned=None):
    """A character in the world. `learned` is still accepted for old callers and ignored:
    nothing about words is needed to fight since the purge."""
    h, data = await register(client, username)
    r = await client.post("/character/create", json={"display_name": display, "appearance": LOOK}, headers=h)
    assert r.status_code == 200, r.text
    uid = data["user_id"]
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        s = Session(uid, username, display, ch.realm, LOOK)
        s.sent = []
        s.hp, s.qi = float(ch.hp), float(ch.qi)
        await w._load_combat(s, ch)
    w.sessions[uid] = s
    return h, uid, s


def last(s: Session, t: str):
    return next((m for m in reversed(s.sent) if m.get("t") == t), None)


def at_monster(w: World, s: Session, kind: str = "ink_slime"):
    assert w.join(s, "truc_lam_thon", "abode")
    m0 = None
    ch = w._pick_channel(FOREST)
    m0 = next(m for m in ch.monsters if m.kind == kind)
    w._place(s, FOREST, m0.x, m0.y, "down")
    for m in ch.monsters:  # keep the others away from the test
        if m is not m0:
            m.mode, m.respawn_at = "dead", 1e12
    return s.player, m0


async def hit(w: World, p, m) -> None:
    w.mono.t += 1.0
    assert combat.attack(p, m.eid, w.mono(), w.rng) is None
    await settle(w)


async def answer(client, h, s, right: bool):
    """Answer the last question a monster asked (a math question since the purge)."""
    from tests.test_math_loop import right_answer, wrong_answer   # (that module imports this one)
    q = last(s, "q")["q"]
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


# ------------------------------------------------------------------ the shield
async def test_shielded_monster_cannot_be_killed(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_1", "Kiếm Một")
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    q = last(s, "q")
    assert q and q["mid"] == m.eid and q["q"]["context"] == "math_combat"
    assert "answer_key" not in q["q"] and "hanzi" not in q["q"].get("prompt", {})
    assert p.protected(gw.mono())            # Hộ Thể while answering
    # even a thousand hits cannot kill it while the Mặc Thuẫn is up
    p.question, p.protect_until = None, 0     # (pretend the player ignores the question)
    for _ in range(1000):
        gw.mono.t += 1
        combat.attack(p, m.eid, gw.mono(), gw.rng)
    assert m.alive and m.hp >= 1 and m.shield


async def test_right_answer_breaks_shield_and_kills(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_2", "Kiếm Hai")
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    hp_before = m.hp
    res = await answer(client, h, s, True)
    c = res["combat"]
    assert res["correct"] and c["shield_broken"] and not m.shield
    expected = combat.base_damage(p, m) * 2 * (1.5 if c["crit"] else 1)
    assert abs((hp_before - m.hp) - expected) < 0.01 or c["killed"]
    assert res["xp"]["gained"] == math_path.xp_for_tier(res["math"]["tier"])   # Tu Vi of a right answer, by tier
    for _ in range(40):
        if not m.alive:
            break
        await hit(gw, p, m)
    assert not m.alive
    await settle(gw)
    loot = last(s, "loot")
    assert loot and loot["monster"] == "Mực Con" and loot["xp"]["gained"] == catalog.monsters()["ink_slime"]["xp"]
    async with dbm.SessionLocal() as db:
        e = await db.get(CodexEntry, (uid, "monster", "ink_slime"))
        assert e is not None and e.progress["kills"] == 1


async def test_wrong_answer_mac_kich_formula(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_3", "Kiếm Ba")
    p, m = at_monster(gw, s)
    p.stats["ink_res"] = 20
    await hit(gw, p, m)
    before = p.hp
    res = await answer(client, h, s, False)
    expected = p.max_hp * 10 / 100 * (1 - 20 / 100)        # normal monster: 10% of max HP, minus Kháng Mực
    assert not res["correct"] and abs((before - p.hp) - expected) < 0.01
    assert res["combat"]["mac_kich"] == round(expected)
    assert m.shield
    s.sent.clear()
    run(gw, combat.cfg()["next_question_delay"] - 0.2)
    await settle(gw)
    assert last(s, "q") is None                            # not before 3 s
    run(gw, 0.5)
    await settle(gw)
    assert last(s, "q") is not None


async def test_elite_hits_harder_and_regrows_shield(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_4", "Kiếm Bốn")
    p, m = at_monster(gw, s, "ink_fox")
    p.max_hp = p.hp = 500
    await hit(gw, p, m)
    res = await answer(client, h, s, False)
    assert abs(res["combat"]["mac_kich"] - round(500 * 0.15)) <= 1     # tinh anh: 15%
    run(gw, 3.5)
    await settle(gw)
    await answer(client, h, s, True)
    assert not m.shield
    p.stats["atk"] = 1000                                  # hit straight down to under 50%
    p.stats["crit"] = 0
    gw.mono.t += 1
    m.hp = m.max_hp * 0.55
    combat.attack(p, m.eid, gw.mono(), gw.rng)
    assert m.alive and m.shield                            # back up at 50%: a new question comes
    await settle(gw)
    run(gw, 0.5)
    await settle(gw)
    assert last(s, "q")["mid"] == m.eid


async def test_timeout_counts_as_wrong(client, gw, frozen):
    h, uid, s = await fighter(client, gw, "kiem_5", "Kiếm Năm")
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    before = p.hp
    limit = last(s, "q")["q"]["time_limit"]
    frozen.advance(seconds=limit + 5)          # the database clock (expires_at)
    run(gw, limit + 2)                         # the world clock (deadline)
    await settle(gw)
    assert p.question is None and p.hp < before
    sid = last(s, "q")["q"]["session_id"]
    async with dbm.SessionLocal() as db:
        from app.models import QuizSession
        qs = await db.get(QuizSession, sid)
        assert qs.answered_at is not None and qs.correct is False


async def test_protection_while_answering(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_6", "Kiếm Sáu")
    p, m = at_monster(gw, s, "tone_wisp")
    await hit(gw, p, m)
    assert p.question is not None
    hp = p.hp
    x, y = p.x, p.y
    p.channel.queue_input(p, 0, [(1, 0, 50)])
    run(gw, 3.0)                               # it chases and swings, but Hộ Thể holds
    assert p.hp == hp and (p.x, p.y) == (x, y)


async def test_first_right_answer_breaks_for_everyone(client, gw):
    ha, a, sa = await fighter(client, gw, "kiem_7a", "Kiếm Bảy")
    hb, b, sb = await fighter(client, gw, "kiem_7b", "Kiếm Tám")
    pa, m = at_monster(gw, sa)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, FOREST, m.x, m.y, "down")
    pb = sb.player
    await hit(gw, pa, m)
    await hit(gw, pb, m)
    assert pa.question and pb.question
    await answer(client, ha, sa, True)
    assert not m.shield and pb.question is None
    assert last(sb, "q_end")["reason"] == "broken"


async def test_a_forest_monster_asks_math_at_the_players_own_floor_and_logs_it_once(client, gw):
    """A Mặc Quái of the forest is no quái lỗi sai: it asks a quick question at the player's
    own floor (math_ask.pick_own), and the answer is written to the learning log once."""
    from app.systems import math_ask, math_combat
    h, uid, s = await fighter(client, gw, "kiem_8", "Kiếm Chín")
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    q = last(s, "q")["q"]
    async with dbm.SessionLocal() as db:
        own = await math_ask.own_floor(db, uid)
    assert (q["math"]["subject"], q["math"]["floor"]) == own
    assert q["qtype"] in math_combat.QUICK_TYPES and q["math"]["monster_vi"] == "Mực Con"
    assert q["math"]["tier"] <= await math_combat_tier(uid, q["math"])
    res = await answer(client, h, s, False)
    assert not res["correct"] and res["combat"]["mac_kich"] > 0 and res["math"]["tier"] == q["math"]["tier"]
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
        assert len(rows) == 1 and not rows[0].correct and rows[0].run_id is None
        assert rows[0].skill_id == q["math"]["skill"]


async def math_combat_tier(uid: int, meta: dict) -> int:
    from app.systems import math_combat
    async with dbm.SessionLocal() as db:
        return await math_combat.tier_for(db, uid, meta["skill"], meta["floor"])


async def test_no_question_when_the_bank_has_none_for_the_player(client, gw, monkeypatch):
    from app.systems import math_practice
    h, uid, s = await fighter(client, gw, "kiem_8b", "Kiếm Chín Bis")
    monkeypatch.setattr(math_practice, "_templates", lambda subject, floor: [])
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    err = last(s, "error")
    assert err["code"] == "no_math_question" and p.question is None and not p.q_pending
    assert "chữ" not in err["message_vi"] and "vườn" not in err["message_vi"]
    assert p.no_question_until > gw.mono()                  # not asked again at once
    s.sent.clear()
    run(gw, 3.0)
    await hit(gw, p, m)
    assert last(s, "q") is None and last(s, "error") is None


# ------------------------------------------------------------------ death
async def test_death_loses_tu_vi_and_respawns_in_village(client, gw):
    h, uid, s = await fighter(client, gw, "kiem_9", "Kiếm Mười")
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        ch.realm, ch.realm_stage, ch.cultivation_xp = "luyen_khi", 1, 100
        await db.commit()
    p, m = at_monster(gw, s)
    combat.hurt_player(p.channel, p, p.hp + 5, gw.mono())
    assert p.dead and last(s, "dead")
    await settle(gw)
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        assert ch.cultivation_xp == 100 - round(120 * 0.05)   # 5% of this stage's Tu Vi, never a stage
        assert ch.realm_stage == 1
    run(gw, combat.cfg()["death_overlay_seconds"] + 0.1)
    assert not p.dead and p.channel.zone_id == "truc_lam_thon" and p.hp == p.max_hp


# ------------------------------------------------------------------ pills
async def test_pill_heals_in_world_with_cooldown(client, gw):
    h, uid, s = await fighter(client, gw, "dan_1", "Đan Một")
    async with dbm.SessionLocal() as db:
        from app.systems import inventory
        await inventory.change_item(db, uid, "hoi_huyet_dan", 2, "test")
        await db.commit()
    r = await client.post("/inventory/use", json={"item_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "not_in_world"
    p, m = at_monster(gw, s)
    p.hp = 10
    r = await client.post("/inventory/use", json={"item_id": "hoi_huyet_dan"}, headers=h)
    assert r.status_code == 200 and p.hp == 10 + p.max_hp * 0.35
    r = await client.post("/inventory/use", json={"item_id": "hoi_huyet_dan"}, headers=h)
    assert r.json()["error"]["code"] == "pill_cooldown"
    async with dbm.SessionLocal() as db:
        q = (await db.execute(select(InventoryItem.quantity).where(
            InventoryItem.user_id == uid, InventoryItem.item_id == "hoi_huyet_dan"))).scalar_one()
        assert q == 1


async def test_kill_counts_for_quest(client, gw):
    h, uid, s = await fighter(client, gw, "nv_1", "Nhiệm Vụ")
    await client.get("/quests", headers=h)
    async with dbm.SessionLocal() as db:
        q = await db.get(Quest, (uid, "nm1_xuong_lang"))
        q.state = "claimed"
        db.add(Quest(user_id=uid, quest_id="nm2_muc_con", state="active", progress={"n": 2}))
        await db.commit()
    p, m = at_monster(gw, s)
    await hit(gw, p, m)
    await answer(client, h, s, True)
    p.stats["atk"] = 10000
    while m.alive:
        await hit(gw, p, m)
    await settle(gw)
    assert last(s, "quest")["quest"]["id"] == "nm2_muc_con"
    r = (await client.post("/quests/claim", json={"quest_id": "nm2_muc_con"}, headers=h)).json()
    assert r["next"]["id"] == "nm3_thanh_dieu"
    assert {i["item"] for i in r["rewards"]["items"]} == {"hoi_huyet_dan", "hoi_khi_dan"}


def test_monster_data_is_complete():
    """Two kinds of monster: a Mặc Quái asks a math question at the player's own floor, while
    a quái lỗi sai (M7) asks a math question about one micro-skill and drops the ghi chú that
    explains the mistake. Neither carries anything of the old word game."""
    for kind, m in catalog.monsters().items():
        for key in ("qtypes", "hanzi", "pinyin") + (() if m.get("skill") else ("tier",)):   # (the word tier)
            assert key not in m, (kind, key)
        for key in ("hp", "atk", "def", "xp", "rank", "drops", "name_vi"):
            assert key in m, (kind, key)
        if m.get("skill"):
            for key in ("subject", "floor", "note", "mistake_vi", "shape", "look"):
                assert m.get(key), (kind, key)
            assert catalog.stack_item(m["note"]), (kind, m["note"])
        for d in m["drops"]:
            if "item" in d:
                assert catalog.stack_item(d["item"]), d
            else:
                assert all(e in catalog.equipment()["items"] for e in d["equipment"])


async def test_the_old_word_skills_are_gone(client, gw):
    """Pháp Chữ (skills bound to a word) and their manuals are deleted: the world no longer
    takes a word-skill cast, and nothing in the bag teaches one. The chiêu thức (M9, mskill)
    are the only skills."""
    from app.realtime import protocol
    assert "skill" not in protocol.MESSAGES and "mskill" in protocol.MESSAGES
    assert not hasattr(combat, "cast")
    assert not any(m.get("kind") == "manual" for m in catalog.materials().values() if isinstance(m, dict))
    for kind, m in catalog.monsters().items():
        assert not any(str(d.get("item", "")).startswith("bi_kip") for d in m["drops"]), kind
    h, uid, s = await fighter(client, gw, "phap_0", "Pháp Không")
    p, m = at_monster(gw, s)
    await gw.handle(s, {"t": "skill", "k": "hoa", "id": m.eid})
    assert last(s, "error")["code"] == "bad_message" and m.hp == m.max_hp
    cult = (await client.get("/cultivation", headers=h)).json()
    assert "skills" not in cult

