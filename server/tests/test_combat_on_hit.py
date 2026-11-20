"""The open-world fight rule: questions only when a monster hits you (the `combat` section of
data/math/world_plan.json, wired through `wired_sections`).

A real database and the real quiz service; the world runs on a fake clock whose tick is
called by hand (the machinery of test_combat). Every number is read from the plan, so these
tests read it too instead of repeating it.

The learning-path rules hold on this path as on every other one: the question of a blow is
the monster's own micro-skill at the player's own tier, bounded by its floor; the answer is
written to the learning log, where it opens tiers, feeds the spiral review and counts for
mastery like an answer in Động Phủ.
"""
import math
import types

import pytest
import pytest_asyncio
from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_path, math_tree
from app.models import MathAnswer, QuizSession, User
from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import catalog, math_ask, math_combat, math_practice, math_skills
from tests.helpers import answer_key
from tests.test_combat import FOREST, FakeMono, fighter, last, run, settle
from tests.test_math_loop import right_answer, wrong_answer

VALLEY = "loan_so_coc"
SLIME_MA = "dstt_phan_tu_ma"          # Loạn Số Cốc, floor 1, normal
ELITE_MA = "dstt_anh_trung_ma"        # Loạn Số Cốc, floor 1, elite (Mặc Thuẫn)


def plan() -> dict:
    return math_tree.world_plan()["combat"]


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def stand_at(w: World, s, zone: str, kind: str):
    """The player on a monster of `zone`, every other monster out of the way, and this one
    too tough to fall to the counter hits a test lands."""
    assert w.join(s, "truc_lam_thon", "abode")
    ch = w._pick_channel(zone)
    m0 = next(m for m in ch.monsters if m.kind == kind)
    w._place(s, zone, m0.x, m0.y, "down")
    for m in ch.monsters:
        if m is not m0:
            m.mode, m.respawn_at = "dead", 1e12
    m0.max_hp = m0.hp = 100000.0
    return s.player, m0


async def provoke(w: World, p, m) -> None:
    """Hit it once so it fights back (the mistake monsters are not aggressive)."""
    w.mono.t += 1.0
    assert combat.attack(p, m.eid, w.mono(), w.rng) is None
    await settle(w)


async def take_blow(w: World, s, p, m) -> dict | None:
    """Let the monster wind up and land its blow on a player standing still; the `q` message
    it brings, or None."""
    s.sent.clear()
    m.atk_ready = 0.0
    run(w, combat.windup() + 0.2)
    await settle(w)
    return last(s, "q")


async def answer(client, h, s, right: bool):
    q = last(s, "q")["q"]
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


def rest(w: World) -> None:
    """Sit out the rest window that follows every question."""
    run(w, float(plan()["question_cooldown_seconds"]) + 0.1)


def events(s, k: str) -> list[dict]:
    """Effects of kind `k` this player was sent (the snapshots carry them) or that are still
    waiting for the next snapshot."""
    seen = [e for msg in s.sent if msg.get("t") == "snap" for e in msg.get("fx", [])]
    if s.player is not None and s.player.channel is not None:
        seen += s.player.channel.events
    return [e for e in seen if e.get("k") == k]


def luyen_khi(p, stage: int = 1) -> None:
    p.realm, p.stage = "luyen_khi", stage


# ------------------------------------------------------------------ where the rule runs
async def test_every_wild_zone_runs_on_hit_and_a_bi_canh_keeps_van_dao(client, gw):
    h, uid, s = await fighter(client, gw, "nd_1", "Né Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    assert combat.on_hit_rule(p.channel) and m.on_hit
    assert not combat.on_hit_rule(types.SimpleNamespace(instance=True))     # realm.RealmInstance
    # out here a normal monster has no Mặc Thuẫn; an elite still wears one
    ch = p.channel
    for mon in ch.monsters:
        assert mon.shield == (mon.info.get("rank", "normal") in plan()["shielded_ranks"]), mon.kind
    assert "combat" in math_tree.wired_sections() and math_tree.world_plan()["wired"] is False


async def test_the_zone_message_tells_the_client_the_rule(client, gw):
    h, uid, s = await fighter(client, gw, "nd_2", "Né Hai")
    stand_at(gw, s, VALLEY, SLIME_MA)
    z = last(s, "zone")["combat"]
    assert z["rule"] == "on_hit" and z["rest"] == plan()["question_cooldown_seconds"]
    assert z["dodge"]["dash_px"] == plan()["dodge"]["dash_px"] and z["dodge"]["ok"] is False   # Phàm Nhân


# ------------------------------------------------------------------ attacking is free
async def test_attacking_asks_nothing_and_a_normal_monster_falls_to_plain_hits(client, gw):
    h, uid, s = await fighter(client, gw, "nd_3", "Né Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    m.max_hp = m.hp = 12.0
    for _ in range(10):
        if not m.alive:
            break
        await provoke(gw, p, m)
    assert not m.alive and last(s, "q") is None and p.question is None


# ------------------------------------------------------------------ a blow lands
async def test_a_landed_blow_pauses_the_player_and_asks_the_monsters_own_micro_skill(client, gw):
    h, uid, s = await fighter(client, gw, "nd_4", "Né Bốn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    hp = p.hp
    q = await take_blow(gw, s, p, m)
    assert q is not None and q["mid"] == m.eid and q["hit"]["dmg"] > 0
    assert q["q"]["context"] == math_combat.CONTEXT
    info = catalog.monsters()[SLIME_MA]
    meta = q["q"]["math"]
    assert (meta["skill"], meta["floor"], meta["tier"]) == (info["skill"], info["floor"], 1)
    assert p.hp == hp, "the blow is decided by the answer, nothing lands yet"
    assert p.protected(gw.mono()) and p.question["hit"] > 0
    assert events(s, "tele")[-1]["id"] == m.eid and events(s, "struck")[-1]["id"] == p.eid
    # paused: while the card is open nobody swings at them and they cannot move
    x, y = p.x, p.y
    p.channel.queue_input(p, 50, [(1, 0, 50)])
    run(gw, 3.0)
    assert p.hp == hp and (p.x, p.y) == (x, y) and m.tele is None


async def test_a_right_answer_is_a_parry(client, gw):
    h, uid, s = await fighter(client, gw, "nd_5", "Né Năm")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    p.qi = 0.0
    q = await take_blow(gw, s, p, m)
    hp, mhp = p.hp, m.hp
    expected = combat.base_damage(p, m) * plan()["right_answer"]["counter_multiplier"]
    res = await answer(client, h, s, True)
    c = res["combat"]
    assert res["correct"] and c["parry"] and c["damage"] == int(round(expected))
    assert p.hp == hp and m.hp == pytest.approx(mhp - expected)
    now = gw.mono()
    assert m.stun_until == pytest.approx(now + plan()["right_answer"]["stun_seconds"])
    assert p.qi == pytest.approx(plan()["right_answer"]["linh_luc_gain"])
    assert res["xp"]["gained"] == math_path.xp_for_tier(q["q"]["math"]["tier"])        # tu vi
    assert p.rest_until == pytest.approx(now + plan()["question_cooldown_seconds"])
    assert p.question is None and not p.protected(now) and p.mcombo == 1
    assert events(s, "parry")[-1]["by"] == p.eid
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
        assert len(rows) == 1 and rows[0].correct and rows[0].run_id is None
        assert rows[0].skill_id == catalog.monsters()[SLIME_MA]["skill"]
    run(gw, plan()["right_answer"]["stun_seconds"] - 0.2)
    assert m.tele is None, "a stunned monster does not wind up"


async def test_a_wrong_answer_takes_the_full_blow_and_shows_the_solution(client, gw):
    h, uid, s = await fighter(client, gw, "nd_6", "Né Sáu")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    hp = p.hp
    res = await answer(client, h, s, False)
    blow = p.question is None and q["hit"]["dmg"]
    assert not res["correct"] and not res["combat"]["parry"] and res["combat"]["shows_solution"]
    assert res["combat"]["damage_taken"] == round(blow * plan()["wrong_answer"]["damage_taken"])
    assert p.hp == pytest.approx(hp - blow * plan()["wrong_answer"]["damage_taken"], abs=0.6)
    assert res.get("reveal") is not None or res.get("correct_option") is not None   # the solution
    assert events(s, "gb")[-1]["id"] == p.eid and p.mcombo == 0
    async with dbm.SessionLocal() as db:
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert not a.correct and a.run_id is None


async def test_running_out_of_time_is_a_wrong_answer(client, gw, frozen):
    h, uid, s = await fighter(client, gw, "nd_7", "Né Bảy")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    hp = p.hp
    limit = q["q"]["time_limit"]
    frozen.advance(seconds=limit + 5)            # the database clock (expires_at)
    run(gw, limit + 2)                           # the world clock (deadline)
    await settle(gw)
    assert p.question is None and p.hp < hp
    assert p.rest_until > gw.mono() - 2
    async with dbm.SessionLocal() as db:
        qs = await db.get(QuizSession, q["q"]["session_id"])
        assert qs.answered_at is not None and qs.correct is False


async def test_the_rest_window_halves_a_blow_and_asks_nothing(client, gw):
    h, uid, s = await fighter(client, gw, "nd_8", "Né Tám")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    await answer(client, h, s, True)
    blow = q["hit"]["dmg"]
    run(gw, plan()["right_answer"]["stun_seconds"] + 0.1)
    hp = p.hp
    assert await take_blow(gw, s, p, m) is None, "no question inside the rest window"
    assert p.rest_until > gw.mono()
    assert hp - p.hp == pytest.approx(blow * plan()["hit_during_cooldown"]["damage_taken"], abs=0.6)
    rest(gw)
    assert await take_blow(gw, s, p, m) is not None, "after the rest a blow asks again"


async def test_no_question_to_ask_lands_a_rest_blow(client, gw, monkeypatch):
    h, uid, s = await fighter(client, gw, "nd_9", "Né Chín")
    monkeypatch.setattr(math_practice, "_templates", lambda subject, floor: [])
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    hp = p.hp
    assert await take_blow(gw, s, p, m) is None
    assert last(s, "error")["code"] == "no_math_question"
    assert p.hp < hp and not p.protected(gw.mono()) and p.rest_until > gw.mono()


# ------------------------------------------------------------------ getting out of the way
async def test_stepping_out_of_the_zone_avoids_the_blow(client, gw):
    h, uid, s = await fighter(client, gw, "nd_10", "Né Mười")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, 0.1)
    assert m.tele is not None
    p.x, p.y = m.tele["x"], m.tele["y"] + m.tele["r"] + 40      # well out of it
    hp = p.hp
    run(gw, combat.windup())
    await settle(gw)
    assert last(s, "q") is None and p.hp == hp


async def test_dodge_is_locked_before_luyen_khi_one(client, gw):
    h, uid, s = await fighter(client, gw, "nd_11", "Né Mười Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    x = p.x
    assert combat.dodge(p, 0, 1, 0, gw.mono()) == "locked"
    run(gw, 0.3)
    assert p.x == x and p.ack == 0, "a refused dash still takes its sequence number"


async def test_dodge_dashes_out_of_the_zone_and_has_a_cooldown(client, gw):
    h, uid, s = await fighter(client, gw, "nd_12", "Né Mười Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    luyen_khi(p)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, combat.windup() - 0.1)                       # the zone is nearly full
    assert m.tele is not None
    hp, x = p.hp, p.x
    assert combat.dodge(p, 0, 0, 0, gw.mono()) == "cannot"  # a direction is needed
    s.sent.clear()
    assert combat.dodge(p, 1, -1, 0, gw.mono()) is None
    assert last(s, "zone") is None and events(s, "dodge")[-1]["id"] == p.eid
    run(gw, 0.2)
    await settle(gw)
    assert last(s, "q") is None and p.hp == hp
    assert 0 < x - p.x <= plan()["dodge"]["dash_px"] + 0.5, "the dash moved it, never further than the plan"
    assert not combat.in_tele(combat.make_tele(m, x, p.y, catalog.monsters()[SLIME_MA]["attack_radius"], 0), p.x, p.y)
    assert combat.dodge(p, 2, 1, 0, gw.mono()) == "cooldown"
    run(gw, plan()["dodge"]["cooldown_seconds"])
    assert combat.dodge(p, 3, 1, 0, gw.mono()) is None


async def test_the_dodge_iframes_beat_a_blow_that_still_reaches(client, gw):
    """Dashing along the edge of a long line can leave you inside it: the iframes save you."""
    h, uid, s = await fighter(client, gw, "nd_12b", "Né Mười Hai Bis")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    luyen_khi(p)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, combat.windup() - 0.1)
    tele = m.tele
    hp = p.hp
    assert combat.dodge(p, 0, 1, 0, gw.mono()) is None
    run(gw, 0.05)
    p.x, p.y = tele["x"], tele["y"]                      # still standing in it when it lands
    s.sent.clear()
    run(gw, 0.15)
    await settle(gw)
    assert gw.mono() < p.dodge_until or events(s, "dodged")
    assert events(s, "dodged")[-1]["id"] == p.eid and last(s, "q") is None and p.hp == hp


async def test_no_dodge_while_answering_or_in_a_bi_canh(client, gw):
    h, uid, s = await fighter(client, gw, "nd_13", "Né Mười Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    luyen_khi(p)
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    assert combat.dodge(p, 0, 1, 0, gw.mono()) == "answering"
    p.channel.instance = True                                # what realm.RealmInstance says
    try:
        assert combat.dodge(p, 1, 1, 0, gw.mono()) == "cannot"
    finally:
        p.channel.instance = False


def test_the_cone_and_the_line_hit_what_they_cover():
    m = types.SimpleNamespace(x=100.0, y=100.0, info={"rank": "elite"}, shape_i=0)
    cone = combat.make_tele(m, 120.0, 100.0, 20, 0.0, "cone")   # pointing right
    t = plan()["telegraph"]
    assert cone["r"] == pytest.approx(20 * t["cone_reach_mult"])
    assert combat.in_tele(cone, 125.0, 100.0)
    half = math.radians(t["cone_degrees"] / 2)
    inside = (100 + 20 * math.cos(half * 0.8), 100 + 20 * math.sin(half * 0.8))
    outside = (100 + 25 * math.cos(half + 0.6), 100 + 25 * math.sin(half + 0.6))
    assert combat.in_tele(cone, *inside) and not combat.in_tele(cone, *outside)
    assert not combat.in_tele(cone, 80.0, 100.0)                # behind it
    line = combat.make_tele(m, 100.0, 130.0, 20, 0.0, "line")   # pointing down
    assert combat.in_tele(line, 100.0, 100.0 + line["r"] - 1)
    assert not combat.in_tele(line, 100.0 + line["w"] / 2 + combat.HIT_SLACK + 3, 120.0)
    assert not combat.in_tele(line, 100.0, 60.0)
    circle = combat.make_tele(m, 50.0, 50.0, 20, 0.0)
    assert combat.in_tele(circle, 50.0, 74.0) and not combat.in_tele(circle, 50.0, 80.0)


async def test_an_elite_takes_turns_through_its_ranks_shapes(client, gw):
    h, uid, s = await fighter(client, gw, "nd_14", "Né Mười Bốn")
    p, m = stand_at(gw, s, VALLEY, ELITE_MA)
    luyen_khi(p)
    await provoke(gw, p, m)
    seen = []
    for _ in range(len(plan()["telegraph"]["by_rank"]["elite"])):
        m.atk_ready, m.tele = 0.0, None
        s.sent.clear()
        run(gw, 0.06)
        seen.append(events(s, "tele")[-1]["sh"])
        m.tele = None
    assert seen == plan()["telegraph"]["by_rank"]["elite"]


# ------------------------------------------------------------------ shields and other players
async def test_an_elites_shield_breaks_only_on_a_parry(client, gw):
    h, uid, s = await fighter(client, gw, "nd_15", "Né Mười Lăm")
    p, m = stand_at(gw, s, VALLEY, ELITE_MA)
    p.qi = 200.0
    assert m.shield
    await provoke(gw, p, m)
    assert m.shield and m.hp == m.max_hp - combat.cfg()["shielded_damage"]
    gw.mono.t += 5
    assert math_skills.request(p, "kiem_quyet", m.eid, gw.mono()) is None
    await settle(gw)
    assert last(s, "mcast")["ok"] and m.shield, "a chiêu does not break it out here"
    await take_blow(gw, s, p, m)
    res = await answer(client, h, s, True)
    assert res["combat"]["shield_broken"] and not m.shield


async def test_other_players_keep_fighting_while_one_answers(client, gw):
    ha, a, sa = await fighter(client, gw, "nd_16a", "Né Mười Sáu")
    hb, b, sb = await fighter(client, gw, "nd_16b", "Né Mười Bảy")
    pa, m = stand_at(gw, sa, VALLEY, SLIME_MA)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, VALLEY, m.x + 8, m.y, "down")
    pb = sb.player
    await provoke(gw, pa, m)
    await provoke(gw, pb, m)
    pb.x = m.x + 60                                        # b out of reach: a is hit first
    assert await take_blow(gw, sa, pa, m) is not None
    assert pa.protected(gw.mono()) and not pb.protected(gw.mono()) and pb.question is None
    pb.x, pb.y = m.x + 10, m.y
    sb.sent.clear()
    m.atk_ready = 0.0
    run(gw, combat.windup() + 0.2)
    await settle(gw)
    assert last(sb, "q") is not None, "the monster turned on the one still fighting"
    assert pa.question is not None, "and the first one's card is still open"


# ------------------------------------------------------------------ the learning path holds
async def test_a_forest_monster_asks_at_the_players_own_floor(client, gw):
    h, uid, s = await fighter(client, gw, "nd_17", "Né Mười Tám")
    p, m = stand_at(gw, s, FOREST, "ink_slime")
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    async with dbm.SessionLocal() as db:
        own = await math_ask.own_floor(db, uid)
    assert (q["q"]["math"]["subject"], q["q"]["math"]["floor"]) == own
    assert q["q"]["qtype"] in math_combat.QUICK_TYPES


async def test_right_parries_open_the_next_tier_and_the_floor_bounds_it(client, gw):
    """Rule 3.3 (adaptive tier) on this path: parries count like answers in Động Phủ. Enough
    right answers at tier 1 - the last one a Phản Đòn - open tier 2, and the next
    blow asks at tier 2; never above what the floor allows."""
    h, uid, s = await fighter(client, gw, "nd_18", "Né Mười Chín")
    info = catalog.monsters()[SLIME_MA]
    need = math_path.cfg()["tier_unlock"]["correct_at_previous_tier"]
    async with dbm.SessionLocal() as db:
        for n in range(need - 1):
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=info["subject"], skill_id=info["skill"],
                              floor=info["floor"], tier=1, item_id=f"x{n}", qtype="true_false",
                              fingerprint=f"f{n}", correct=True, timed_out=False, review=False,
                              answer_ms=800, answered_at=clock.now()))
        await db.commit()
        assert await math_combat.tier_for(db, uid, info["skill"], info["floor"]) == 1
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q["q"]["math"]["tier"] == 1
    await answer(client, h, s, True)
    async with dbm.SessionLocal() as db:
        assert await math_combat.tier_for(db, uid, info["skill"], info["floor"]) == 2
    rest(gw)
    q = await take_blow(gw, s, p, m)
    lo, hi = math_path.floor_tiers(info["floor"])
    assert q["q"]["math"]["tier"] == 2 and lo <= 2 <= hi
    # the floor caps it: right answers at its top tier open nothing above
    async with dbm.SessionLocal() as db:
        for n in range(need):
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=info["subject"], skill_id=info["skill"],
                              floor=info["floor"], tier=hi, item_id=f"y{n}", qtype="true_false",
                              fingerprint=f"g{n}", correct=True, timed_out=False, review=False,
                              answer_ms=800, answered_at=clock.now()))
        await db.commit()
    await answer(client, h, s, True)
    rest(gw)
    q = await take_blow(gw, s, p, m)
    assert q["q"]["math"]["tier"] == hi


async def test_a_parry_answer_feeds_the_spiral_review(client, gw):
    """Rule 6b: the review schedule of a sitting on a later floor reads this answer."""
    h, uid, s = await fighter(client, gw, "nd_19", "Né Hai Mươi")
    info = catalog.monsters()[SLIME_MA]
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    await answer(client, h, s, False)
    run_ = types.SimpleNamespace(subject_id=info["subject"], floor=info["floor"] + 1, node_id=None)
    async with dbm.SessionLocal() as db:
        stats = await math_practice._review_stats(db, uid, run_, math_path.cfg())
    mine = next(st for st in stats if st.skill_id == info["skill"])
    assert mine.last_answered is not None and mine.recent == (False,) and mine.streak == 0


# ------------------------------------------------------------------ chiêu thức
async def test_a_chieu_is_cast_freely_and_the_parry_streak_is_its_combo(client, gw):
    h, uid, s = await fighter(client, gw, "nd_20", "Né Hai Mốt")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.qi = 200.0
    sk = math_skills.skills()["kiem_quyet"]
    hp0 = m.hp
    assert math_skills.request(p, "kiem_quyet", m.eid, gw.mono()) is None
    await settle(gw)
    msg = last(s, "mcast")
    assert msg["ok"] and msg["free"] and last(s, "q") is None and p.question is None
    assert p.qi == pytest.approx(200.0 - sk["qi"])
    first = hp0 - m.hp
    assert first == pytest.approx(math_skills.damage(combat.base_damage(p, m), sk, 0, False))
    qi = p.qi
    assert math_skills.request(p, "kiem_quyet", m.eid, gw.mono()) is None
    await settle(gw)
    assert last(s, "mcast")["code"] == "cooldown" and p.qi == qi
    # two Phản Đòn in a row, then the same chiêu hits harder by the combo
    for _ in range(2):
        await take_blow(gw, s, p, m)
        await answer(client, h, s, True)
        rest(gw)
    assert p.mcombo == 2
    hp1 = m.hp
    gw.mono.t += sk["cooldown"]
    assert math_skills.request(p, "kiem_quyet", m.eid, gw.mono()) is None
    await settle(gw)
    assert hp1 - m.hp == pytest.approx(math_skills.damage(combat.base_damage(p, m), sk, 2, False))
    assert last(s, "mcast")["result"]["combo"] == 2


async def test_a_locked_chieu_is_refused_and_costs_nothing(client, gw):
    h, uid, s = await fighter(client, gw, "nd_21", "Né Hai Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.qi = 200.0
    assert math_skills.request(p, "ngu_hanh_tran", m.eid, gw.mono()) is None    # opens at floor 2
    await settle(gw)
    msg = last(s, "mcast")
    assert not msg["ok"] and msg["code"] == "locked" and p.qi == 200.0
    assert "ngu_hanh_tran" not in p.mskill_ready
    # the client sends a locked chiêu with no target: "locked" is still what the player hears
    assert math_skills.request(p, "ngu_hanh_tran", None, gw.mono()) is None
    await settle(gw)
    assert last(s, "mcast")["code"] == "locked"


async def test_a_bi_canh_question_is_untouched_by_the_rule(client, gw):
    """The answer handler only takes the Phản Đòn path for the question of a blow."""
    h, uid, s = await fighter(client, gw, "nd_22", "Né Hai Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.question = {"sid": "x", "mid": m.eid, "deadline": 1e12, "asked": 0, "limit": 10, "timeout_sent": False}
    res = combat.on_answer(p, "x", True, 1000)
    assert "parry" not in res and res["correct"]
