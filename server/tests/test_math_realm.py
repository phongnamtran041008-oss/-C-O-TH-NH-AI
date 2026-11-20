"""M10: bí cảnh toán (kế hoạch 4.3) - "nhiều người cùng vào, mỗi người nhận câu theo tầng của
mình; boss cuối là câu 'Tìm chỗ sai' hoặc bài tổng hợp."

The run is the stage-9 bí cảnh (test_realm.py); what is new is what it asks. These tests hold
it to the learning rules: every question at the answering player's own floor and tier (two
players on different floors fighting one monster get two different floors), every answer in
the learning log with no run, a timeout is a wrong answer and nothing else, the boss asks the
hardest question each player may be asked, and the party realms (scheduled, rift) ask the same way.
Like test_realm, the world runs on a fake clock ticked by hand."""
import os

import pytest
from sqlalchemy import select

from app import balance
from app import db as dbm
from app.learning import math_items, math_path
from app.models import MathAnswer, RealmClaim, User
from app.realtime import combat
from app.systems import math_ask, math_combat, math_realm, secret_realm
from tests.helpers import answer_key
from tests.realm_bot import Bot, Team, right_answer_any
from tests.test_combat import last, settle
from tests.test_math_ask import open_tier_2
from tests.test_math_loop import right_answer, wrong_answer
from tests.test_math_skills import clear_floor, prepare
from tests.test_realm import gw, hero, make_party, msgs, play, tick  # noqa: F401  (gw is a fixture)
from tests.test_realm_ws import dev_server  # noqa: F401  (a fixture: a real server process)

REALM = "toan_tran"
SUBJECT = "dai_so_tuyen_tinh"
SEEDS = int(os.environ.get("MATH_REALM_SEEDS", "30"))


# ------------------------------------------------------------------ helpers
# three different own floors of Đạo Thụ's main path in Đại Số (floor 2 holds only an optional node,
# so it is never a player's own floor: the frontier, R9)
OWN = (1, 3, 4)


async def math_hero(client, gw, username, display, floor=1, realm_id="luyen_khi"):
    """A player whose own floor is `floor` (the floors below it passed), standing at the gate."""
    h, uid, s = await hero(client, gw, username, display, realm_id=realm_id)
    for n in range(1, floor):
        await clear_floor(uid, n)
    p = gw.players[uid]
    p.max_hp = p.hp = 600          # sturdy, so a test is about the rules rather than the fight
    p.stats["atk"] = 45
    return h, uid, s


async def enter(gw, leader, *others, rooms=None, seed=None):
    if others:
        await make_party(gw, leader, *others)
    gw.realms.room_order = rooms
    gw.realms.seed = seed
    await gw.handle(leader, {"t": "realm", "op": "enter", "realm": REALM})
    await settle(gw)
    return gw.realms.instance_of(gw.players[leader.user_id])


async def answer(client, h, q: dict, right: bool = True) -> dict:
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


def stand(p, o) -> None:
    p.x, p.y = o.x + o.w / 2, o.y + o.h / 2


def away(inst, ps) -> None:
    cx, cy = inst.room_center()
    for i, p in enumerate(ps):
        p.x, p.y = cx - 60 + 40 * i, cy + 80


async def own_tier(uid: int, meta: dict) -> int:
    async with dbm.SessionLocal() as db:
        return await math_combat.tier_for(db, uid, meta["skill"], meta["floor"])


# ------------------------------------------------------------------ the data and the gate
def test_the_math_realm_data_is_sound():
    assert math_realm.validate() == []


def test_validate_catches_what_breaks_the_rules():
    import copy
    import json
    from app.config import DATA_DIR
    raw = json.loads((DATA_DIR / "realms.json").read_text("utf-8"))
    bad = copy.deepcopy(raw)
    r = bad["realms"][REALM]
    r["min_realm"] = "truc_co"                                        # rule 6
    r["math"]["rooms"][0]["place"] = "nowhere"
    r["math"]["boss_question"]["prefer"] = "riddle"
    c = copy.deepcopy(balance.load("realm"))
    c["chest"][REALM]["table"].append({"item": "muc_tinh", "weight": 1})   # rule 7: not an M7 material
    c["room_loot_by_realm"][REALM]["xp"] = 10
    out = "\n".join(math_realm.validate(bad, c))
    for bit in ("min_realm", "nowhere", "boss_question.prefer", "muc_tinh", "no xp"):
        assert bit in out, (bit, out)
    # since 2026-11-20 Mảnh Bảo Vật and Linh Quả may come from a math bí cảnh (gated by tu vi,
    # app/systems/loot.py); Tu Vi and Tiên Ngọc from loot are still refused
    ok = copy.deepcopy(balance.load("realm"))
    ok["chest"][REALM].update({"fragments": 2, "flawless_fragments": 1})
    ok["chest"][REALM]["table"].append({"item": "linh_qua", "weight": 1})
    assert math_realm.validate(raw, ok) == []
    ok["chest"][REALM]["jade"] = [0, 2]
    assert any("no xp nor jade" in e for e in math_realm.validate(raw, ok))


async def test_the_gate_lists_the_math_realm_open_and_alone(client, gw):
    h, uid, s = await math_hero(client, gw, "cong_toan", "Cổng Toán", floor=3)
    v = (await client.get("/realms", headers=h)).json()
    assert REALM not in {x["id"] for x in v["realms"]}                 # its own list, its own tab
    r = next(x for x in v["math_realms"] if x["id"] == REALM)
    assert r["math"] and r["open"] and r["party_min"] == 1 and r["floor"] == 3 and r["realm_ok"]
    assert "min_realm" not in r and r["entries_left"] == secret_realm.daily_limit(REALM)
    assert v["puzzles"]["seal"]["how_vi"] and v["puzzles"]["boss"]["how_vi"]


async def test_alone_at_the_lowest_realm_and_the_old_realms_still_want_a_party(client, gw):
    """Rule 6: nothing reads the cultivation realm; and a party of one is enough here only."""
    h, uid, s = await math_hero(client, gw, "mot_minh", "Một Mình", realm_id="luyen_khi")
    await gw.handle(s, {"t": "realm", "op": "enter", "realm": "mac_anh_dong"})
    assert last(s, "error")["code"] == "need_party"
    inst = await enter(gw, s)
    assert inst is not None and inst.math and inst.rooms == ["seal", "seal", "boss"]
    assert [r["place"] for r in inst.room_specs] == ["compose", "sentence", "boss"]
    room = msgs(s, "realm", "room")[-1]
    assert room["kind"] == "seal" and room["place"] == "compose" and room["math"]
    assert room["puzzle"]["need"] == balance.load("realm")["seal"]["base"]           # alone: base seals
    start = msgs(s, "realm", "start")[-1]["run"]
    assert start["math"] and start["members"][0]["floor"] == 1


async def test_nobody_enters_without_a_floor_that_has_questions(client, gw, monkeypatch):
    h, uid, s = await math_hero(client, gw, "khong_tang", "Không Tầng")

    async def nothing(db, user_id, subject_id=None):
        return None
    monkeypatch.setattr(math_ask, "own_floor", nothing)
    inst = await enter(gw, s)
    assert inst is None and last(s, "error")["code"] == "no_math_question"
    async with dbm.SessionLocal() as db:   # no entry was used up
        assert (await secret_realm.entries_used(db, uid)).get(REALM, 0) == 0


# ------------------------------------------------------------------ every question at the player's own floor
async def test_two_floors_one_monster_two_floors_of_questions(client, gw):
    """The heart of the mode: whatever asks, the question comes from the answerer's own floor.
    The monster is a quái lỗi sai of floor 1; the player on floor 3 is still asked floor 3."""
    ha, a, sa = await math_hero(client, gw, "tang_mot", "Tầng Một", floor=1)
    hb, b, sb = await math_hero(client, gw, "tang_ba", "Tầng Ba", floor=3)
    inst = await enter(gw, sa, sb)
    m = next(m for m in inst.monsters if m.alive)
    assert m.info["floor"] == 1
    pa, pb = gw.players[a], gw.players[b]
    for p in (pa, pb):
        p.x, p.y = m.x, m.y + 6
        combat.engage(inst, m, p, gw.mono())
    await settle(gw)
    qa, qb = last(sa, "q")["q"], last(sb, "q")["q"]
    assert qa["context"] == qb["context"] == math_realm.CONTEXT
    assert qa["math"]["floor"] == 1 and qb["math"]["floor"] == 3
    for uid, q in ((a, qa), (b, qb)):
        assert q["math"]["tier"] <= await own_tier(uid, q["math"])          # never above their own tier
        assert q["math"]["realm_asker"] == "monster" and q["math"]["mistake_vi"]
    # a right answer breaks the Mặc Thuẫn as anywhere, and is written to the learning log
    res = await answer(client, hb, qb, True)
    assert res["combat"]["shield_broken"] and not m.shield
    async with dbm.SessionLocal() as db:
        row = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == b))).scalars().one()
        assert row.run_id is None and row.floor == 3 and row.correct


async def test_a_wrong_or_late_answer_is_a_mac_kich_and_counts_as_wrong(client, gw, frozen):
    h, uid, s = await math_hero(client, gw, "sai_muon", "Sai Muộn")
    inst = await enter(gw, s)
    p = gw.players[uid]
    m = next(m for m in inst.monsters if m.alive)
    p.x, p.y = m.x, m.y + 6
    combat.engage(inst, m, p, gw.mono())
    await settle(gw)
    hp = p.hp
    res = await answer(client, h, last(s, "q")["q"], False)
    assert res["combat"]["mac_kich"] > 0 and p.hp < hp and m.shield
    await tick(gw, combat.cfg()["next_question_delay"] + 0.2)      # the monster asks again
    q = last(s, "q")["q"]
    frozen.advance(seconds=q["time_limit"] + 5)                    # the database clock (expires_at)
    await tick(gw, q["time_limit"] + balance.quiz()["network_grace"] + 1.0)
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid)
                                 .order_by(MathAnswer.id))).scalars().all()
    assert [(r.correct, r.timed_out, r.run_id) for r in rows] == [(False, False, None), (False, True, None)]


# ------------------------------------------------------------------ Trận Nhãn
async def test_a_seal_asks_whoever_stands_on_it_and_breaks_on_a_right_answer(client, gw):
    h, uid, s = await math_hero(client, gw, "an_mot", "Ấn Một", floor=3)
    inst = await enter(gw, s)
    inst.monsters[:] = []                       # about the seals alone
    pz, p = inst.puzzle, gw.players[uid]
    seals = inst.objs("pedestal")
    assert pz.kind == "seal" and len(pz.names) == len(seals) == 4 and pz.need() == 2
    stand(p, seals[0])
    await tick(gw, 0.1)
    q = last(s, "q")
    assert q["seal"] == seals[0].name and q["q"]["math"]["floor"] == 3 and q["q"]["math"]["realm_asker"] == "seal"
    assert p.protected(gw.mono())                               # Hộ Thể while answering, like Vấn Đạo
    assert pz.public(gw.mono())["seals"][0]["busy"]
    # wrong: the one who answered pays, the seal holds and asks again a little later
    hp = p.hp
    res = await answer(client, h, q["q"], False)
    assert res["realm"]["broken"] is False and p.hp < hp and pz.mistakes == 1 and not pz.broken
    s.sent.clear()
    await tick(gw, balance.load("realm")["seal"]["retry_seconds"] - 0.5)
    assert not msgs(s, "q")
    await tick(gw, 1.0)
    res = await answer(client, h, last(s, "q")["q"], True)
    assert res["realm"]["broken"] and pz.broken == {seals[0].name: uid} and not pz.solved
    stand(p, seals[1])
    await tick(gw, 0.1)
    await answer(client, h, last(s, "q")["q"], True)
    assert pz.solved
    await tick(gw, 0.1)
    assert inst.phase == "advancing" and any(m.get("event") == "cleared" for m in msgs(s, "realm"))
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
        assert len(rows) == 3 and all(r.run_id is None and r.floor == 3 for r in rows)


async def test_a_seal_room_needs_more_seals_and_everyone_for_a_party(client, gw):
    hs = [await math_hero(client, gw, f"doi_an_{i}", f"Đội Ấn {i}", floor=OWN[i]) for i in range(3)]
    inst = await enter(gw, hs[0][2], hs[1][2], hs[2][2])
    inst.monsters[:] = []
    pz = inst.puzzle
    ps = [gw.players[u] for _, u, _ in hs]
    seals = inst.objs("pedestal")
    c = balance.load("realm")["seal"]
    assert pz.need() == min(len(seals), c["base"] + 2 * c["per_member"]) == 4
    away(inst, ps)
    first = ps[0]

    async def take(i_player, seal, right=True):
        h, _u, s = hs[i_player]
        stand(ps[i_player], seal)
        await tick(gw, 0.1)
        q = last(s, "q")
        assert q["seal"] == seal.name, q
        assert q["q"]["math"]["floor"] == OWN[i_player]                   # each on their own floor
        await answer(client, h, q["q"], right)
        ps[i_player].y += 60
        await tick(gw, 0.1)
    await take(0, seals[0])
    await take(0, seals[1])                    # 4 seals, 2 left unbroken for the other two: allowed
    # now taking a third would leave one seal for two players who have broken none: refused
    hb, ub, sb = hs[0]
    stand(first, seals[2])
    sb.sent.clear()
    await tick(gw, 0.1)
    assert not msgs(sb, "q") and msgs(sb, "realm", "hint")[-1]["code"] == "seal_share"
    away(inst, ps)
    await tick(gw, 0.1)
    await take(1, seals[2])
    assert not pz.solved and pz.missing() == [ps[2].user_id]
    await take(2, seals[3])
    assert pz.solved


async def test_two_players_cannot_answer_the_same_seal_at_once(client, gw):
    hs = [await math_hero(client, gw, f"tranh_{i}", f"Tranh {i}") for i in range(2)]
    inst = await enter(gw, hs[0][2], hs[1][2])
    inst.monsters[:] = []
    seal = inst.objs("pedestal")[0]
    pa, pb = gw.players[hs[0][1]], gw.players[hs[1][1]]
    stand(pa, seal)
    await tick(gw, 0.1)
    stand(pb, seal)
    await tick(gw, 0.5)
    assert last(hs[0][2], "q") and not msgs(hs[1][2], "q")


async def test_falling_or_leaving_mid_question_frees_the_seal(client, gw):
    hs = [await math_hero(client, gw, f"nga_{i}", f"Ngã {i}") for i in range(3)]
    inst = await enter(gw, *[s for _, _, s in hs])
    inst.monsters[:] = []
    pz = inst.puzzle
    seals = inst.objs("pedestal")
    ps = [gw.players[u] for _, u, _ in hs]
    away(inst, ps)
    stand(ps[1], seals[0])
    stand(ps[2], seals[1])
    await tick(gw, 0.1)
    assert set(pz.asking) == {ps[1].user_id, ps[2].user_id}
    q1, q2 = last(hs[1][2], "q")["q"], last(hs[2][2], "q")["q"]
    # one falls while answering: the question closes, the seal is free again
    combat.hurt_player(inst, ps[1], 10_000, gw.mono(), ignore_protect=True)
    await tick(gw, 0.1)
    assert ps[1].ghost and ps[1].question is None and ps[1].user_id not in pz.asking
    assert last(hs[1][2], "q_end")["sid"] == q1["session_id"]
    # an answer that comes in after all is only logged
    res = await answer(client, hs[1][0], q1, True)
    assert "math" in res and seals[0].name not in pz.broken
    # one walks out while answering: the same, and the room no longer waits for them
    await gw.handle(hs[2][2], {"t": "realm", "op": "leave"})
    await tick(gw, 0.1)
    assert ps[2].user_id not in pz.asking and ps[2].question is None
    res = await answer(client, hs[2][0], q2, True)
    assert seals[1].name not in pz.broken
    assert pz.need() == balance.load("realm")["seal"]["base"]          # only the one left can be asked
    for seal in seals[:2]:
        stand(ps[0], seal)
        await tick(gw, 0.1)
        await answer(client, hs[0][0], last(hs[0][2], "q")["q"], True)
        ps[0].y += 60
        await tick(gw, 0.1)
    assert pz.solved


async def test_a_seal_question_left_to_time_out_is_wrong_and_nothing_more(client, gw, frozen):
    h, uid, s = await math_hero(client, gw, "het_gio", "Hết Giờ")
    inst = await enter(gw, s)
    inst.monsters[:] = []
    pz, p = inst.puzzle, gw.players[uid]
    stand(p, inst.objs("pedestal")[0])
    await tick(gw, 0.1)
    q = last(s, "q")["q"]
    hp = p.hp
    frozen.advance(seconds=q["time_limit"] + 5)
    await tick(gw, q["time_limit"] + balance.quiz()["network_grace"] + 0.5)
    assert p.question is None and not pz.broken and pz.mistakes == 1
    assert hp - p.hp == pytest.approx(p.max_hp * balance.load("realm")["seal"]["fail_pct"] / 100, abs=1)
    async with dbm.SessionLocal() as db:
        row = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert row.timed_out and not row.correct and row.run_id is None


async def test_a_player_with_no_question_is_told_and_not_waited_for(client, gw, monkeypatch):
    ha, a, sa = await math_hero(client, gw, "co_cau", "Có Câu")
    hb, b, sb = await math_hero(client, gw, "het_cau", "Hết Câu")
    inst = await enter(gw, sa, sb)
    inst.monsters[:] = []
    real = math_ask.pick_own

    async def none_for_b(db, user, **kw):
        return None if user.id == b else await real(db, user, **kw)
    monkeypatch.setattr(math_ask, "pick_own", none_for_b)
    pz = inst.puzzle
    seals = inst.objs("pedestal")
    pa, pb = gw.players[a], gw.players[b]
    away(inst, [pa, pb])
    stand(pb, seals[0])
    await tick(gw, 0.1)
    assert last(sb, "error")["code"] == "no_math_question" and not msgs(sb, "q")
    assert b in inst.no_question and not pz.asking and pb.question is None
    assert pz.need() == balance.load("realm")["seal"]["base"] and pz.missing() == [a]
    pb.y += 60
    for seal in seals[1:3]:
        stand(pa, seal)
        await tick(gw, 0.1)
        await answer(client, ha, last(sa, "q")["q"], True)
        pa.y += 60
        await tick(gw, 0.1)
    assert pz.solved                                                   # the room did not wait for b
    # the boss's big shield does not wait for them either
    assert inst.group_need(None) == 1


# ------------------------------------------------------------------ the boss
async def test_the_boss_asks_each_player_their_bai_tong_hop(client, gw):
    """A player with no 'Tìm chỗ sai' question at their tier gets the bài tổng hợp, the hardest
    question the player may be asked - here tier 2 on the one micro-skill where this player has
    opened tier 2 (find_mistake starts at tier 2 and lives on other micro-skills of the floor)."""
    assert "find_mistake" in math_items.PLAYABLE_TYPES
    assert math_realm.boss_type(secret_realm.realms()[REALM]) == "find_mistake"
    ha, a, sa = await math_hero(client, gw, "boss_mot", "Boss Một")
    hb, b, sb = await math_hero(client, gw, "boss_hai", "Boss Hai", floor=3)
    skill = math_path.subject(SUBJECT).floor(1).skills[0].id
    await open_tier_2(a, skill, 1)
    inst = await enter(gw, sa, sb, rooms=["boss"])
    await tick(gw, 3.5)
    boss = inst.boss
    assert boss is not None and boss.shield and inst.group_need(boss) == 2
    qa, qb = last(sa, "q")["q"], last(sb, "q")["q"]
    assert qa["math"]["realm_asker"] == qb["math"]["realm_asker"] == "boss"
    assert qa["math"]["floor"] == 1 and qa["math"]["skill"] == skill and qa["math"]["tier"] == 2
    assert qa["qtype"] != "find_mistake"                                     # a has none at their tier
    # b's own floor is 3 (Đạo Thụ: floor 2 is never an own floor), whose lowest tier is 2, where
    # Tìm chỗ sai lives: b gets the boss's own type
    assert qb["math"]["floor"] == 3 and qb["qtype"] == "find_mistake"
    r = await answer(client, ha, qa, True)
    assert r["combat"]["shield_progress"] == [1, 2] and boss.shield
    r = await answer(client, hb, qb, True)
    assert r["combat"]["shield_broken"] and not boss.shield


async def test_the_boss_asks_find_mistake_of_a_player_who_has_one(client, gw):
    """M11: the boss's preferred type is playable now. A player who has opened tier 2 on a
    micro-skill that has a 'Tìm chỗ sai' gets that question; a player at tier 1 everywhere
    still gets the bài tổng hợp. The right answer is {"line": i}; a wrong line is wrong."""
    ha, a, sa = await math_hero(client, gw, "boss_soi", "Boss Soi Lỗi")
    hb, b, sb = await math_hero(client, gw, "boss_moi", "Boss Mới")
    mistakes = {i.skill for i in math_items.floor_items(SUBJECT, 1, True) if i.qtype == "find_mistake"}
    assert mistakes
    skill = sorted(mistakes)[0]
    await open_tier_2(a, skill, 1)
    inst = await enter(gw, sa, sb, rooms=["boss"])
    await tick(gw, 3.5)
    boss = inst.boss
    assert boss is not None and boss.shield
    qa, qb = last(sa, "q")["q"], last(sb, "q")["q"]
    assert qa["qtype"] == "find_mistake" and qa["input"] == "find_mistake"
    assert qa["math"]["skill"] == skill and qa["math"]["tier"] == 2 and qa["math"]["realm_asker"] == "boss"
    assert 3 <= len(qa["prompt"]["lines"]) <= 6
    assert qb["qtype"] != "find_mistake" and qb["math"]["tier"] == 1                # b has none: the bài tổng hợp
    key = await answer_key(qa["session_id"])
    wrong = (key["line"] + 1) % len(qa["prompt"]["lines"])
    r = await client.post("/quiz/answer", json={"session_id": qa["session_id"], "answer": {"line": wrong}}, headers=ha)
    assert r.status_code == 200 and not r.json()["correct"]
    assert r.json()["reveal"]["answer_text"].startswith(f"Bước {key['line'] + 1}: ")


async def test_a_chieu_still_works_on_the_math_boss(client, gw):
    """M9 inside the bí cảnh: a landed chiêu is one player's right answer to the big shield."""
    ha, a, sa = await math_hero(client, gw, "chieu_mot", "Chiêu Một")
    hb, b, sb = await math_hero(client, gw, "chieu_hai", "Chiêu Hai")
    inst = await enter(gw, sa, sb, rooms=["boss"])
    boss = inst.boss
    pa = gw.players[a]
    prepare(pa, atk=45)
    pa.x, pa.y = boss.x, boss.y + 20
    sa.sent.clear()
    await gw.handle(sa, {"t": "mskill", "k": "kiem_quyet", "id": boss.eid})
    await settle(gw)
    assert last(sa, "mcast")["ok"], last(sa, "mcast")
    q = last(sa, "q")
    assert q["cast"]["k"] == "kiem_quyet"
    res = await answer(client, ha, q["q"], True)
    assert res["combat"]["correct"] and res["combat"]["shield_progress"] == [1, 2] and boss.shield


async def test_a_chieu_in_the_math_realm_asks_at_the_casters_own_floor(client, gw):
    """Plan 4.3 holds for chiêu too: the room monsters are floor-1 quái lỗi sai, and outside the
    realm a chiêu asks about its target's floor. Inside, a floor-3 player casting at one gets a
    floor-3 question, like every other question of the bí cảnh."""
    h, uid, s = await math_hero(client, gw, "chieu_tang_ba", "Chiêu Tầng Ba", floor=3)
    inst = await enter(gw, s)
    m = next(m for m in inst.monsters if m.alive and m.info.get("floor") == 1)
    p = gw.players[uid]
    prepare(p, atk=10)
    for _ in range(4):
        p.x, p.y = m.x, m.y + 10
        gw.mono.t += 30
        p.question, p.q_pending, p.next_q, p.protect_until = None, False, None, 0.0
        s.sent.clear()
        await gw.handle(s, {"t": "mskill", "k": "thuong_quyen", "id": m.eid})
        await settle(gw)
        assert last(s, "mcast")["ok"], last(s, "mcast")
        q = last(s, "q")["q"]
        assert q["math"]["floor"] == 3, q["math"]
        assert q["math"]["tier"] <= await own_tier(uid, q["math"])
        await answer(client, h, q, False)       # a miss: the monster keeps its shield for the next cast


# ------------------------------------------------------------------ the party realms
@pytest.mark.parametrize("realm_id", ["mac_anh_dong", "khe_nut_muc"])
async def test_the_party_realms_ask_at_each_players_own_floor_too(client, gw, realm_id):
    """The scheduled realm and the rift realm (which used to ask Chinese words) are math bí cảnh
    like this one: a seal asks each player at their own floor."""
    hs = [await math_hero(client, gw, f"tiec_{realm_id[:3]}_{i}", f"Tiệc {i}", floor=OWN[i], realm_id="truc_co")
          for i in range(2)]
    await make_party(gw, hs[0][2], hs[1][2])
    gw.realms.room_order = None
    if realm_id == "khe_nut_muc":
        ch = gw._pick_channel("rung_muc_loang")
        for _, _, s in hs:
            gw._place(s, "rung_muc_loang", 300, 330, "down")
        r = gw.realms.spawn_rift(ch, gw.mono(), 310, 330)
        await gw.handle(hs[0][2], {"t": "realm", "op": "enter", "rift": r.id})
    else:
        await gw.handle(hs[0][2], {"t": "realm", "op": "enter", "realm": realm_id})
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[hs[0][1]])
    assert inst is not None and inst.realm_id == realm_id and inst.math and inst.question_source is not None
    assert inst.rooms[0] == "seal" and inst.rooms[-1] == "boss"
    inst.monsters[:] = []
    seals = inst.objs(inst.room_spec()["seal"])
    ps = [gw.players[u] for _, u, _ in hs]
    away(inst, ps)
    for i, (h, u, s) in enumerate(hs):
        stand(ps[i], seals[i])
        await tick(gw, 0.1)
        q = last(s, "q")
        assert q["seal"] == seals[i].name and q["q"]["context"] == math_realm.CONTEXT
        assert q["q"]["math"]["floor"] == OWN[i]
        ps[i].y += 60


# ------------------------------------------------------------------ bots, over many seeds
def math_answerer(client, seen: dict):
    async def answer_fn(bot, q):
        seen.setdefault(bot.uid, []).append(q["math"]["floor"] if "math" in q else None)
        key = await answer_key(q["session_id"])
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"],
                                                    "answer": right_answer_any(q, key)}, headers=bot.h)
        assert r.status_code == 200, r.text
        return r.json()
    return answer_fn


async def bot_run(client, gw, prefix: str, floors: list[int], seed: int):
    heroes = [await math_hero(client, gw, f"{prefix}_{i}", f"{prefix.title()} {i}", floor=f)
              for i, f in enumerate(floors)]
    inst = await enter(gw, *[s for _, _, s in heroes], seed=seed)
    assert inst is not None, [last(s, "error") for _, _, s in heroes]
    team, seen = Team(), {}
    bots = [Bot(gw, client, h, uid, s, team, math_answerer(client, seen)) for h, uid, s in heroes]
    done = await play(gw, bots, 600, lambda: inst.phase == "ended")
    return heroes, inst, bots, seen, done


@pytest.mark.parametrize("floors", [[1], list(OWN)], ids=["solo", "party_of_3"])
async def test_bots_clear_the_math_realm(client, gw, floors):
    """A bot team plays one whole run - two Trận Nhãn rooms and the boss - and every question each
    bot was asked came from its own floor; each gets its own loot once, of rule 7's kinds only."""
    heroes, inst, bots, seen, done = await bot_run(client, gw, "bot", floors, seed=7)
    assert done and inst.result == "won", (inst.kind, inst.puzzle and inst.puzzle.public(gw.mono()))
    for (h, uid, s), f in zip(heroes, floors):
        assert seen.get(uid) and set(seen[uid]) == {f}, (uid, f, seen.get(uid))
    await tick(gw, 0.2)
    materials = {e["item"] for e in balance.load("realm")["chest"][REALM]["table"]} | {
        e["item"] for e in balance.load("realm")["room_loot_by_realm"][REALM]["items"]}
    async with dbm.SessionLocal() as db:
        for _, uid, _ in heroes:
            rows = (await db.execute(select(RealmClaim).where(RealmClaim.run_id == inst.run_id,
                                                              RealmClaim.user_id == uid))).scalars().all()
            assert sorted(r.stage for r in rows) == ["chest", "room0", "room1", "room2"]
            for r in rows:
                assert {i["item"] for i in r.loot.get("items", [])} <= materials and not r.loot.get("equipment")
                assert not r.loot.get("jade")
            user = await db.get(User, uid)
            assert user is not None
    for b in bots:
        b.read()
        assert b.ended and b.ended["result"] == "won" and b.ended["fragments"] == 0
        assert b.loot and all("xp" not in lt for lt in b.loot)          # Tu Vi comes from the answers only


@pytest.mark.parametrize("seed", range(SEEDS))
async def test_bot_runs_finish_for_every_seed(client, gw, seed):
    """The old bots found real hangs by sweeping seeds: a solo bot and a party of three on
    floors 1, 3 and 4 must finish a run whatever the rooms' random monsters and the questions are."""
    for prefix, floors in ((f"s{seed}", [OWN[seed % 3]]), (f"p{seed}", list(OWN))):
        heroes, inst, bots, seen, done = await bot_run(client, gw, prefix, floors, seed)
        assert done and inst.result == "won", (seed, floors, inst.kind,
                                                inst.puzzle and inst.puzzle.public(gw.mono()))
        await tick(gw, balance.load("realm")["exit_seconds"] + 0.5)
        assert inst.run_id not in gw.realms.instances


async def test_bots_clear_the_math_realm_over_websockets(dev_server):  # noqa: F811
    """tools/realm_bots.py over real WebSockets, at once: one bot alone, and a party of three on
    floors 1, 3 and 4. Every bot wins and gets its own loot, once."""
    import asyncio
    import sqlite3

    import realm_bots
    lines: list[str] = []
    try:
        teams = await asyncio.gather(
            realm_bots.run_math(dev_server["url"], dev_server["db"], prefix="ms", floors=[3], timeout=420,
                                log=lines.append),
            realm_bots.run_math(dev_server["url"], dev_server["db"], prefix="mp", floors=list(OWN), timeout=420,
                                log=lines.append))
    except RuntimeError as e:
        raise AssertionError(f"{e} / {dev_server['log'].read_text()[-4000:]}") from None
    bots = [b for team in teams for b in team]
    floor_of = {b.uid: f for team, fl in zip(teams, ([3], list(OWN))) for b, f in zip(team, fl)}
    try:
        assert not [b.kicked for b in bots if b.kicked]
        assert all(b.ended and b.ended["result"] == "won" for b in bots), (lines, dev_server["log"].read_text()[-3000:])
        con = sqlite3.connect(dev_server["db"])
        try:
            for b in bots:
                stages = sorted(r[0] for r in con.execute(
                    "select stage from realm_claims where user_id=?", (b.uid,)).fetchall())
                assert stages == ["chest", "room0", "room1", "room2"], (b.name, stages)
                floors = {r[0] for r in con.execute("select floor from math_answers where user_id=?", (b.uid,))}
                assert floors == {floor_of[b.uid]}, (b.name, floors)   # every question at the bot's own floor
        finally:
            con.close()
    finally:
        for b in bots:
            await b.close()


# ------------------------------------------------------------------ Thiên kiếp (M11 đợt 2)
def test_a_math_realm_never_asks_a_thien_kiep_and_the_data_cannot_ask_for_one():
    assert "tribulation" not in math_realm.QUICK_TYPES
    assert set(math_realm.QUICK_TYPES) == set(math_items.PLAYABLE_TYPES) - {"tribulation"}
    import copy
    import json
    from app.config import DATA_DIR
    bad = copy.deepcopy(json.loads((DATA_DIR / "realms.json").read_text("utf-8")))
    bad["realms"][REALM]["math"]["boss_question"]["prefer"] = "tribulation"
    assert any("takes too long for a bí cảnh" in e for e in math_realm.validate(bad))
    assert math_realm.boss_type(bad["realms"][REALM]) is None


@pytest.mark.parametrize("asker", ["monster", "seal", "boss"])
async def test_every_asker_of_a_math_realm_asks_only_quick_types(asker, monkeypatch):
    seen = []

    async def fake_pick_own(db, user, **k):
        seen.append(k.get("qtypes"))
        return None
    monkeypatch.setattr(math_realm.math_ask, "pick_own", fake_pick_own)
    from app.config import DATA_DIR
    import json
    rdef = json.loads((DATA_DIR / "realms.json").read_text("utf-8"))["realms"][REALM]
    assert await math_realm.question_for(None, None, rdef, asker) is None
    assert seen and all(q is not None and "tribulation" not in q for q in seen), seen
