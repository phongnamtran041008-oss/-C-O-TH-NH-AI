"""M9: chiêu thức gắn câu hỏi - a chiêu is cast by answering one math question of its type.

The same machinery as test_combat and test_math_combat (a real database, the real quiz
service, a world on a fake clock ticked by hand), in Loạn Số Cốc where every monster is a
quái lỗi sai. The rules under test are in app/systems/math_skills.py and the contract of
data/math/skills.json is its `_comment`.
"""
import copy
import json
import random

import pytest
import pytest_asyncio
from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_path, math_problems, math_tree
from app.models import MathAnswer, MathRun, MathSubmission, QuizSession, User
from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.party import Party
from app.realtime.world import World
from app.systems import catalog, math_combat, math_skills, math_tree_progress
from tests.helpers import answer_key
from tests.test_combat import FakeMono, fighter, last, run, settle  # noqa: F401
from tests.test_math_combat import at_math_monster
from tests.test_math_loop import right_answer as _right3, wrong_answer as _wrong3

SUBJECT = "dai_so_tuyen_tinh"
SLIME_MA = "dstt_phan_tu_ma"          # floor 1, normal, 40 HP

# contract section 2: these never change, the client and the checks rely on them
FIXED = {
    "thuong_quyen": (["true_false"], 1, "damage", "slash", "chem", 1),
    "kiem_quyet": (["multiple_choice"], 1, "damage", "slash", "kiem_khi", 1),
    "hoa_cau_thuat": (["numeric"], 1, "damage", "cast", "hoa_cau", 1),
    "ngu_hanh_tran": (["ordering"], 1, "area", "cast", "tran_do", 2),
    "ho_than_tran": (["matching"], 1, "ward", "cast", "ho_tran", 2),
    "thien_loi_tuyet_ky": (["tribulation"], 4, "damage", "cast", "thien_loi", 7),
}


@pytest.fixture(autouse=True)
def van_dao(monkeypatch):
    """Casting by answering a question (M9) is the rule of a bí cảnh: these tests pin it on a
    wild zone. Out in the wild a chiêu is cast freely: tests/test_combat_on_hit.py."""
    from app.realtime import combat
    monkeypatch.setattr(combat, "on_hit_rule", lambda ch: False)


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


# ------------------------------------------------------------------ helpers
def right_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "matching":
        return {"pairs": list(key["pairs"])}
    if q["qtype"] == "ordering":
        return {"order": list(key["order"])}
    return _right3(q, key)


def wrong_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "matching":
        pairs = list(key["pairs"])
        return {"pairs": pairs[1:] + pairs[:1]}      # every left gets another right side
    if q["qtype"] == "ordering":
        return {"order": list(reversed(key["order"]))}
    return _wrong3(q, key)


async def clear_floor(uid: int, floor: int) -> None:
    """Pass the Thiên kiếp nhỏ of a floor, the way the learning path records it."""
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id=SUBJECT, floor=floor, mode="trial", tier=1, passed=True,
                       started_at=clock.now(), ended_at=clock.now()))
        await db.commit()


async def clear_first_floors(uid: int) -> None:
    """Đạo Thụ: a chiêu of "floor n" opens at Luyện Khí tầng n (the working stage, one above the
    stage reached). Luyện Khí tầng 1 is reached when every stage-1 main node is done: the first
    node of each of the four branches: one Thiên kiếp per subject on floor 1, and every exercise of
    Python nhập môn (the programming node) handed in with all its tests right."""
    async with dbm.SessionLocal() as db:
        for subject in math_path.subjects():
            db.add(MathRun(user_id=uid, subject_id=subject.id, floor=1, mode="trial", tier=1, passed=True,
                           started_at=clock.now(), ended_at=clock.now()))
        for pid in math_tree.tree().nodes["lt_python_co_ban"].problems:
            p = math_problems.problem(pid)
            db.add(MathSubmission(user_id=uid, problem_id=pid, subject_id=p.subject, floor=p.floor, tier=p.tier,
                                  verdict="AC", passed=len(p.tests), total=len(p.tests), ms=1, xp_gained=0,
                                  created_at=clock.now(), judged_at=clock.now()))
        await db.commit()


def prepare(p, qi: float = 200.0, atk: float = 10.0) -> None:
    """Known numbers for the formula: plain attack, no weapon, no crit, plenty of qi."""
    p.stats = {"atk": atk, "def": 0, "crit": 0}
    p.max_qi = p.qi = qi


async def cast(w: World, s, k: str, eid: str | None):
    """Press a chiêu through the WebSocket handler and wait for the background task."""
    s.sent.clear()
    w.mono.t += 0.05
    await w.handle(s, {"t": "mskill", "k": k, "id": eid})
    await settle(w)
    return last(s, "mcast")


async def answer(client, h, s, right: bool, after: float = 0.0, frozen=None):
    q = last(s, "q")["q"]
    key = await answer_key(q["session_id"])
    if after and frozen is not None:
        frozen.advance(seconds=after)
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


def fx(w: World, p, k: str) -> list[dict]:
    """Channel events of this kind not yet sent out in a snapshot."""
    return [e for e in p.channel.events if e.get("k") == k]


def expected(p, m, k: str, streak: int, fast: bool) -> float:
    c = combat.cfg()
    mult = min(math_skills.combo_cfg()["max_mult"], 1 + math_skills.combo_cfg()["per_streak"] * streak)
    return (combat.base_damage(p, m) * math_skills.skills()[k]["power"] * mult
            * (c["fast_answer_crit_mult"] if fast else 1.0))


# ------------------------------------------------------------------ the data
def test_the_data_validates():
    assert math_skills.validate() == []
    assert len(math_skills.skills()) >= 5


def test_the_six_chieu_of_the_contract_are_there_unchanged():
    sk = math_skills.skills()
    assert list(sk)[:len(FIXED)] == list(FIXED), "the first six are the default Công Pháp bar (keys 1-6)"
    for sid, (qtypes, min_tier, effect, anim, fx_id, floor) in FIXED.items():
        s = sk[sid]
        assert (s["qtypes"], s["min_tier"], s["effect"], s["anim"], s["fx"], s["unlock"]["floor"]) == \
            (qtypes, min_tier, effect, anim, fx_id, floor), sid
        assert s.get("reviewed") is False, sid


def test_bigger_chieu_hit_harder_and_cost_more():
    """small < medium < large < tuyệt kỹ, and qi and cooldown grow with the power."""
    sk = math_skills.skills()
    ladder = [sk[k] for k in ("thuong_quyen", "kiem_quyet", "hoa_cau_thuat", "thien_loi_tuyet_ky")]
    for a, b in zip(ladder, ladder[1:]):
        assert a["power"] < b["power"] and a["qi"] < b["qi"] and a["cooldown"] < b["cooldown"]
    assert sk["thuong_quyen"]["qi"] == 0
    assert sk["hoa_cau_thuat"]["range"] > sk["kiem_quyet"]["range"] > 0      # Hỏa Cầu is ranged


def test_validate_catches_broken_data():
    raw = json.loads(math_skills.SKILLS_FILE.read_text("utf-8"))

    def broken(edit) -> list[str]:
        r = copy.deepcopy(raw)
        edit(r["skills"])
        return math_skills.validate(r)

    assert any("question type" in e for e in broken(lambda s: s["kiem_quyet"].update(qtypes=["essay"])))
    assert any("radius" in e for e in broken(lambda s: s["ngu_hanh_tran"].pop("radius")))
    assert any("effect" in e for e in broken(lambda s: s["thuong_quyen"].update(effect="explode")))
    assert any("unlock" in e for e in broken(lambda s: s["thuong_quyen"].update(unlock={"realm": "kim_dan"})))
    assert any("cooldown" in e for e in broken(lambda s: s["thuong_quyen"].update(cooldown=0)))
    assert any("min_tier" in e for e in broken(lambda s: s["thuong_quyen"].update(min_tier=9)))
    assert any("element" in e for e in broken(lambda s: s["thuong_quyen"].update(element="gio")))
    assert any("slow" in e for e in broken(lambda s: s["ngu_hanh_tran"].update(slow=1.0)))
    assert any("mean nothing" in e for e in broken(lambda s: s["kiem_quyet"].update(radius=50)))
    assert any("missing" in e for e in broken(lambda s: s["hoa_cau_thuat"].pop("fx")))


def test_the_formula():
    assert math_skills.combo_mult(0) == 1.0
    assert math_skills.combo_mult(1) == pytest.approx(1.1)
    assert math_skills.combo_mult(5) == pytest.approx(1.5)
    assert math_skills.combo_mult(50) == pytest.approx(1.5)                  # capped
    sk = math_skills.skills()["kiem_quyet"]
    crit = combat.cfg()["fast_answer_crit_mult"]
    assert math_skills.damage(10, sk, 2, True) == pytest.approx(10 * sk["power"] * 1.2 * crit)
    assert math_skills.damage(10, sk, 0, False) == pytest.approx(10 * sk["power"])


def test_only_the_documented_chieu_cannot_be_cast_today():
    # floors 7-9 now hold Thiên kiếp questions, so even the documented exception is castable
    uncastable = [k for k, s in math_skills.skills().items() if not math_skills.castable_floors(s)]
    assert uncastable == []
    tl = math_skills.skills()["thien_loi_tuyet_ky"]
    want = [(s.id, n) for s in math_path.subjects() for n in (7, 8, 9)]
    assert sorted(math_skills.castable_floors(tl)) == sorted(want)


# ------------------------------------------------------------------ the view
async def test_the_view_follows_the_learning_path(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_v", "Chiêu Xem")
    r = await client.get("/math/skills", headers=h)
    assert r.status_code == 200, r.text
    v = r.json()
    assert v["combo"] == math_skills.combo_cfg()
    assert [x["id"] for x in v["skills"]] == list(math_skills.skills())
    assert v["loadout"] == list(FIXED) and v["new"] == []
    by = {x["id"]: x for x in v["skills"]}
    for sid in ("thuong_quyen", "kiem_quyet", "hoa_cau_thuat"):
        assert by[sid]["unlocked"] and by[sid]["locked_vi"] is None
    for sid in ("ngu_hanh_tran", "ho_than_tran", "thien_loi_tuyet_ky"):
        assert not by[sid]["unlocked"] and "tầng" in by[sid]["locked_vi"], by[sid]
    assert by["kiem_quyet"]["qtype_vi"] == math_path.question_types()["multiple_choice"]["name_vi"]
    for key in ("name_vi", "kind_vi", "element", "qtypes", "min_tier", "qi", "cooldown", "range", "effect",
                "power", "anim", "fx", "desc_vi", "unlock"):
        assert key in by["hoa_cau_thuat"], key
    await clear_floor(uid, 1)                       # one subject's first node: Luyện Khí tầng 1 is not reached yet
    v = (await client.get("/math/skills", headers=h)).json()
    assert v["open_floor"] == 1 and not {x["id"]: x for x in v["skills"]}["ngu_hanh_tran"]["unlocked"]
    await clear_first_floors(uid)
    by = {x["id"]: x for x in (await client.get("/math/skills", headers=h)).json()["skills"]}
    assert by["ngu_hanh_tran"]["unlocked"] and by["ho_than_tran"]["unlocked"]
    tl = by["thien_loi_tuyet_ky"]
    assert not tl["unlocked"] and "tầng 7" in tl["locked_vi"]                 # honest: still locked


# ------------------------------------------------------------------ refusals (nothing spent)
def assert_nothing_spent(p, qi: float) -> None:
    assert p.qi == qi and not p.mskill_ready and p.question is None and not p.q_pending
    assert not p.protected(wmod.world.mono())


async def test_every_refusal_spends_nothing(client, gw, monkeypatch):
    h, uid, s = await fighter(client, gw, "chieu_r", "Chiêu Từ")
    p, m = at_math_monster(gw, s)
    prepare(p)
    qi = p.qi

    async def code(k, eid):
        msg = await cast(gw, s, k, eid)
        assert msg and msg["ok"] is False and msg["message_vi"], msg
        return msg["code"]

    assert await code("khong_co", m.eid) == "unknown"
    assert await code("ngu_hanh_tran", m.eid) == "locked"            # floor 2 not open yet
    assert await code("thien_loi_tuyet_ky", m.eid) == "locked"
    assert await code("kiem_quyet", None) == "no_target"
    assert await code("kiem_quyet", "m9_nobody") == "no_target"
    p.x += 500
    assert await code("kiem_quyet", m.eid) == "too_far"
    p.x -= 500
    p.qi = 1
    assert await code("kiem_quyet", m.eid) == "no_qi"
    p.qi = qi
    p.mskill_ready["kiem_quyet"] = gw.mono() + 100
    assert await code("kiem_quyet", m.eid) == "cooldown"
    p.mskill_ready.clear()
    p.question = {"sid": "x", "mid": m.eid, "deadline": 1e12, "asked": 0, "limit": 10, "timeout_sent": False}
    assert await code("kiem_quyet", m.eid) == "answering"
    p.question = None
    sk = math_skills.skills()
    monkeypatch.setitem(sk, "thuong_quyen", {**sk["thuong_quyen"], "min_tier": 2})
    assert await code("thuong_quyen", m.eid) == "tier_low"           # a fresh player is at tier 1
    monkeypatch.setitem(sk, "thuong_quyen", {**sk["thuong_quyen"], "qtypes": ["tribulation"]})     # (a type nothing can ask yet)
    assert await code("thuong_quyen", m.eid) == "no_question"
    p.dead = True
    assert await code("kiem_quyet", m.eid) == "cannot"
    p.dead = False
    assert_nothing_spent(p, qi)
    assert m.shield and m.hp == m.max_hp
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(QuizSession).where(QuizSession.user_id == uid))).first() is None


async def test_a_bad_mskill_message_is_answered_with_an_error(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_b", "Chiêu Hỏng")
    at_math_monster(gw, s)
    s.sent.clear()
    await gw.handle(s, {"t": "mskill", "k": 5})
    assert last(s, "error")["code"] == "bad_message"


# ------------------------------------------------------------------ accepted, then right
async def test_a_cast_is_accepted_with_a_question_of_its_type(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_a", "Chiêu Nhận")
    p, m = at_math_monster(gw, s)
    prepare(p)
    sk = math_skills.skills()["kiem_quyet"]
    ok = await cast(gw, s, "kiem_quyet", m.eid)
    assert ok == {"t": "mcast", "k": "kiem_quyet", "ok": True, "ready_in": sk["cooldown"], "qi": 200 - sk["qi"]}
    assert p.qi == 200 - sk["qi"] and p.mskill_ready["kiem_quyet"] == pytest.approx(gw.mono() + sk["cooldown"])
    q = last(s, "q")
    assert q["mid"] == m.eid and q["first_meet"] is False
    assert q["cast"] == {"k": "kiem_quyet", "name_vi": sk["name_vi"]}
    assert q["q"]["context"] == math_skills.CONTEXT and q["q"]["qtype"] == "multiple_choice"
    assert "answer_key" not in q["q"]
    assert q["q"]["math"]["floor"] == catalog.monsters()[SLIME_MA]["floor"]
    assert p.protected(gw.mono()) and p.question["cast"] == "kiem_quyet"     # Hộ Thể, one question
    assert p.user_id in m.engaged
    ev = fx(gw, p, "mcast")
    assert ev and ev[-1]["by"] == p.eid and ev[-1]["s"] == "kiem_quyet" and ev[-1]["anim"] == "slash"
    assert (await cast(gw, s, "thuong_quyen", m.eid))["code"] == "answering"


async def test_a_right_answer_lands_breaks_the_shield_and_matches_the_formula(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_d", "Chiêu Trúng")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    hp = m.hp
    res = await answer(client, h, s, True)
    c = res["combat"]
    want = expected(p, m, "kiem_quyet", 0, True)       # the frozen test clock answers in 0 ms: fast
    assert c["cast"] == "kiem_quyet" and c["correct"] and not c["missed"] and c["crit"]
    assert c["shield_broken"] and not m.shield
    assert c["combo"] == 1 and c["combo_mult"] == 1.0
    assert hp - m.hp == pytest.approx(want) and c["damage"] == round(want) and not c["killed"]
    assert not p.protected(gw.mono()) and p.question is None
    ev = fx(gw, p, "mskill")[-1]
    assert ev["ok"] == 1 and ev["fx"] == "kiem_khi" and ev["anim"] == "slash" and ev["combo"] == 1
    assert (ev["tx"], ev["ty"]) == (m.x, m.y) and ev["by"] == p.eid


async def test_a_slow_answer_is_no_crit(client, gw, frozen):
    h, uid, s = await fighter(client, gw, "chieu_s", "Chiêu Chậm")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "hoa_cau_thuat", m.eid)
    limit = last(s, "q")["q"]["time_limit"]
    m.hp = m.max_hp = 10000.0
    res = await answer(client, h, s, True, after=limit * (combat.cfg()["fast_answer_fraction"] + 0.1),
                       frozen=frozen)
    c = res["combat"]
    assert c["correct"] and not c["crit"]
    assert 10000 - m.hp == pytest.approx(expected(p, m, "hoa_cau_thuat", 0, False))


async def test_the_answer_is_written_to_the_learning_log_and_pays_by_tier(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_l", "Chiêu Ghi")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "thuong_quyen", m.eid)
    q = last(s, "q")["q"]
    res = await answer(client, h, s, True)
    assert res["math"]["tier"] == q["math"]["tier"]
    assert res["xp"]["gained"] == math_path.xp_for_tier(q["math"]["tier"])
    async with dbm.SessionLocal() as db:
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert a.run_id is None and a.correct and a.qtype == "true_false" and a.tier == q["math"]["tier"]
        assert a.subject_id == SUBJECT and a.skill_id == q["math"]["skill"]


async def test_area_hits_and_slows_everything_around_the_target(client, gw):
    """Ngũ Hành Trận is cast by an *ordering* question (contract section 1)."""
    h, uid, s = await fighter(client, gw, "chieu_t", "Chiêu Trận")
    await clear_first_floors(uid)
    p, m = at_math_monster(gw, s)
    prepare(p)
    ch = p.channel
    sk = math_skills.skills()["ngu_hanh_tran"]
    near = next(o for o in ch.monsters if o is not m)
    near.reset()
    near.mode, near.x, near.y = "wander", m.x + sk["radius"] / 2, m.y
    far = next(o for o in ch.monsters if o is not m and o is not near)
    far.reset()
    far.mode, far.x, far.y = "wander", m.x + sk["radius"] * 3, m.y
    ok = await cast(gw, s, "ngu_hanh_tran", m.eid)
    assert ok["ok"], ok
    assert last(s, "q")["q"]["qtype"] == "ordering"
    hp = m.hp
    res = await answer(client, h, s, True)
    c = res["combat"]
    now = gw.mono()
    assert c["correct"] and c["shield_broken"] and not m.shield
    assert hp - m.hp == pytest.approx(expected(p, m, "ngu_hanh_tran", 0, True))
    assert m.slow_until > now and m.slow_mult == sk["slow"]
    assert near.slow_until > now and near.slow_mult == sk["slow"]
    assert near.hp == near.max_hp - combat.cfg()["shielded_damage"]      # still shielded: a scratch
    assert p.user_id in near.engaged
    assert far.slow_until <= now and far.hp == far.max_hp and p.user_id not in far.engaged
    assert fx(gw, p, "mskill")[-1]["r"] == sk["radius"]


async def test_ward_protects_the_caster_and_the_party_near_and_heals_a_little(client, gw):
    """Hộ Thân Trận is cast by a *matching* question and has no target."""
    ha, a, sa = await fighter(client, gw, "chieu_h1", "Chiêu Hộ")
    hb, b, sb = await fighter(client, gw, "chieu_h2", "Chiêu Bạn")
    hc, c_, sc = await fighter(client, gw, "chieu_h3", "Chiêu Lạ")
    await clear_first_floors(a)
    pa, m = at_math_monster(gw, sa)
    for s_ in (sb, sc):
        gw.join(s_, "truc_lam_thon", "abode")
        gw._place(s_, "loan_so_coc", pa.x + 10, pa.y, "down")
    pb, pc = sb.player, sc.player
    gw.parties.parties[77] = Party(77, a, [a, b])
    gw.parties.of[a] = gw.parties.of[b] = 77
    prepare(pa)
    for pl in (pa, pb, pc):
        pl.hp = pl.max_hp / 2
    sk = math_skills.skills()["ho_than_tran"]
    ok = await cast(gw, sa, "ho_than_tran", None)
    assert ok["ok"], ok
    q = last(sa, "q")
    assert q["mid"] is None and q["q"]["qtype"] == "matching"
    res = await answer(client, ha, sa, True)
    cb = res["combat"]
    assert cb["correct"] and cb["damage"] == 0 and cb["ward"]["players"] == 2
    now = gw.mono()
    for pl in (pa, pb):
        assert pl.guard_until == pytest.approx(now + sk["duration"]) and pl.guard_reduce == sk["reduce"]
        assert pl.hp == pytest.approx(pl.max_hp / 2 + pl.max_hp * sk["heal_pct"] / 100)
    assert pc.guard_until <= now and pc.hp == pc.max_hp / 2               # not in the party
    before = pa.hp
    combat.hurt_player(pa.channel, pa, 100, now)
    assert before - pa.hp == pytest.approx(100 * (1 - sk["reduce"]))
    ev = fx(gw, pa, "mskill")[-1]
    assert ev["ok"] == 1 and ev["fx"] == "ho_tran" and ev["r"] == sk["radius"] and "tx" not in ev


# ------------------------------------------------------------------ chiêu hụt
async def test_a_wrong_answer_misses_without_mac_kich(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_w", "Chiêu Hụt")
    p, m = at_math_monster(gw, s)
    prepare(p)
    p.mcombo = 3
    await cast(gw, s, "kiem_quyet", m.eid)
    hp, mhp = p.hp, m.hp
    res = await answer(client, h, s, False)
    c = res["combat"]
    assert not res["correct"] and c["missed"] and not c["correct"] and c["damage"] == 0
    assert "mac_kich" not in c and p.hp == hp                             # no Mặc Kích
    assert m.hp == mhp and m.shield and p.mcombo == 0 and c["combo"] == 0
    assert p.qi == 200 - math_skills.skills()["kiem_quyet"]["qi"]           # qi stays spent
    ev = fx(gw, p, "mskill")[-1]
    assert ev["ok"] == 0 and ev["combo"] == 0
    async with dbm.SessionLocal() as db:
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert not a.correct and a.run_id is None
    # the fight goes on: the shielded monster asks its own question after the usual pause
    s.sent.clear()
    run(gw, combat.cfg()["next_question_delay"] + 0.3)
    await settle(gw)
    q = last(s, "q")
    assert q and q["mid"] == m.eid and q["q"]["context"] == math_combat.CONTEXT and "cast" not in q


async def test_a_timeout_misses_through_the_tick_without_mac_kich(client, gw, frozen):
    h, uid, s = await fighter(client, gw, "chieu_o", "Chiêu Trễ")
    p, m = at_math_monster(gw, s)
    prepare(p)
    p.mcombo = 2
    await cast(gw, s, "hoa_cau_thuat", m.eid)
    hp, mhp = p.hp, m.hp
    q = last(s, "q")["q"]
    frozen.advance(seconds=q["time_limit"] + 5)      # the database clock (expires_at)
    run(gw, q["time_limit"] + 2)                     # the world clock (deadline)
    await settle(gw)
    assert p.question is None and p.mcombo == 0
    assert p.hp == hp and m.hp == mhp and m.shield
    async with dbm.SessionLocal() as db:
        qs = await db.get(QuizSession, q["session_id"])
        assert qs.answered_at is not None and qs.correct is False
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert not a.correct and a.timed_out


# ------------------------------------------------------------------ combo
async def test_combo_grows_caps_and_resets(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_c", "Chiêu Liên")
    p, m = at_math_monster(gw, s)
    prepare(p, qi=10000)
    m.hp = m.max_hp = 1e7
    sk = math_skills.skills()["thuong_quyen"]
    seen = []
    for n in range(7):
        gw.mono.t += sk["cooldown"] + 0.1
        ok = await cast(gw, s, "thuong_quyen", m.eid)
        assert ok["ok"], ok
        hp = m.hp
        c = (await answer(client, h, s, True))["combat"]
        assert c["combo"] == n + 1
        assert c["combo_mult"] == pytest.approx(min(1.5, 1 + 0.1 * n))
        assert hp - m.hp == pytest.approx(expected(p, m, "thuong_quyen", n, True))
        seen.append(c["combo_mult"])
    assert seen[-1] == seen[-2] == pytest.approx(math_skills.combo_cfg()["max_mult"])
    gw.mono.t += sk["cooldown"] + 0.1
    await cast(gw, s, "thuong_quyen", m.eid)
    c = (await answer(client, h, s, False))["combat"]
    assert c["missed"] and p.mcombo == 0
    gw.mono.t += sk["cooldown"] + 0.1
    await cast(gw, s, "thuong_quyen", m.eid)
    c = (await answer(client, h, s, True))["combat"]
    assert c["combo"] == 1 and c["combo_mult"] == 1.0
    p.mcombo = 4
    combat.die(p.channel, p, gw.mono())                                 # death resets it
    assert p.mcombo == 0


async def test_leaving_the_world_resets_the_combo(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_lw", "Chiêu Đi")
    p, m = at_math_monster(gw, s)
    p.mcombo = 5
    gw._leave_world(p, to_abode=True)
    assert p.mcombo == 0
    assert gw.join(s, "truc_lam_thon", "abode")
    assert s.player.mcombo == 0


# ------------------------------------------------------------------ which question
async def test_question_type_is_the_chieus_and_tier_never_above_the_players(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_q", "Chiêu Hỏi")
    await clear_first_floors(uid)
    info = catalog.monsters()[SLIME_MA]
    window = math_path.cfg()["tier_unlock"]["window"]
    async with dbm.SessionLocal() as db:   # open tier 2 of the monster's own micro-skill only
        for n in range(window):
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=SUBJECT, skill_id=info["skill"],
                              floor=info["floor"], tier=1, item_id=f"x{n}", qtype="true_false",
                              fingerprint=f"f{n}", correct=True, timed_out=False, review=False,
                              answer_ms=800, answered_at=clock.now()))
        await db.commit()
    rng = random.Random(7)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        open_floor = await math_tree_progress.working_stage(db, uid)      # Luyện Khí tầng 2 (Đạo Thụ)
        assert open_floor == 2
        for k, sk in math_skills.skills().items():
            if not math_skills.castable_floors(sk):
                continue
            if sk["unlock"]["floor"] > open_floor:          # Thiên Lôi (floor 7): locked for this player,
                if k != "thien_loi_tuyet_ky":               # (the unlock is checked by the cast, not here)
                    continue
                for target in (info, None):                  # and nothing of floors 1-3 may cast it
                    q, code = await math_skills.question_for(db, user, sk, target, rng)
                    assert q is None and code == "no_question", (k, code)
                continue
            for target in (info, catalog.monsters()["dstt_chi_so_ma"], catalog.monsters()["ink_slime"], None):
                for _ in range(6):
                    q, code = await math_skills.question_for(db, user, sk, target, rng)
                    assert q is not None, (k, target and target.get("name_vi"), code)
                    meta = q.public()["math"]
                    assert q.qtype in sk["qtypes"], (k, q.qtype)
                    assert meta["tier"] >= sk["min_tier"]
                    mine = await math_combat.tier_for(db, uid, meta["skill"], meta["floor"])
                    assert meta["tier"] <= mine, (k, meta)
                    if math_combat.is_mistake_monster(target):
                        assert meta["floor"] == target["floor"]
                    else:                                        # the player's own part of Đạo Thụ (R9):
                        assert (meta["subject"], meta["floor"]) == (SUBJECT, 3)      # floor 3's node


async def test_a_mistake_monster_asks_about_its_own_skill_when_it_can(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_own", "Chiêu Riêng")
    info = catalog.monsters()[SLIME_MA]
    sk = math_skills.skills()["hoa_cau_thuat"]                         # numeric: tập hợp has plenty
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for seed in range(5):
            q, _ = await math_skills.question_for(db, user, sk, info, random.Random(seed))
            assert q.public()["math"]["skill"] == info["skill"]


# ------------------------------------------------------------------ the world moved on
async def test_target_killed_while_answering_deals_nothing(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_k", "Chiêu Muộn")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    combat.kill(p.channel, m, gw.mono())
    assert p.question is None and last(s, "q_end")["reason"] == "killed"
    hits = len(fx(gw, p, "hit"))
    res = await answer(client, h, s, True)
    assert res["combat"] == {"stale": True, "cast": "kiem_quyet"} and len(fx(gw, p, "hit")) == hits
    assert not fx(gw, p, "mskill")


async def test_target_gone_before_the_question_exists_is_refused(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_g", "Chiêu Mất")
    p, m = at_math_monster(gw, s)
    prepare(p)
    qi = p.qi
    s.sent.clear()
    assert math_skills.request(p, "kiem_quyet", m.eid, gw.mono()) is None
    combat.kill(p.channel, m, gw.mono())          # dies while the question is being written
    await settle(gw)
    assert last(s, "mcast")["code"] == "no_target" and last(s, "q") is None
    assert_nothing_spent(p, qi)


async def test_target_left_while_answering(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_e", "Chiêu Xa")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    combat.disengage(p.channel, m, p.user_id, gw.mono())   # leashed home
    assert p.question is None and last(s, "q_end")["reason"] == "gone"
    hp = m.hp
    res = await answer(client, h, s, True)
    assert res["combat"].get("stale") and m.hp == hp


async def test_caster_dies_while_answering(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_x", "Chiêu Ngã")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    combat.hurt_player(p.channel, p, p.hp + 5, gw.mono(), ignore_protect=True)
    assert p.dead and p.question is None
    hp = m.hp
    res = await answer(client, h, s, True)
    assert res["combat"].get("stale") and m.hp == hp and m.shield


async def test_caster_leaves_the_world_while_answering(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_lv", "Chiêu Về")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    gw._leave_world(p, to_abode=True)
    hp = m.hp
    res = await answer(client, h, s, True)
    assert "combat" not in res and m.hp == hp and m.shield                 # nobody left to land it


async def test_caster_changes_zone_while_answering(client, gw):
    h, uid, s = await fighter(client, gw, "chieu_z", "Chiêu Đổi")
    p, m = at_math_monster(gw, s)
    prepare(p)
    await cast(gw, s, "kiem_quyet", m.eid)
    gw._place(s, "rung_muc_loang", 100, 100, "down")
    assert p.channel.zone_id == "rung_muc_loang"
    hp = m.hp
    res = await answer(client, h, s, True)
    assert res["combat"].get("stale") and m.hp == hp and m.shield
    assert not [e for e in p.channel.events if e.get("k") in ("hit", "mskill")]


# ------------------------------------------------------------------ shields shared with others
async def test_someone_elses_right_answer_does_not_cancel_a_chieu(client, gw):
    ha, a, sa = await fighter(client, gw, "chieu_p1", "Chiêu Một")
    hb, b, sb = await fighter(client, gw, "chieu_p2", "Chiêu Hai")
    pa, m = at_math_monster(gw, sa)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, "loan_so_coc", m.x, m.y, "down")
    pb = sb.player
    prepare(pa)
    await cast(gw, sa, "kiem_quyet", m.eid)
    gw.mono.t += 1
    assert combat.attack(pb, m.eid, gw.mono(), gw.rng) is None
    await settle(gw)
    await answer(client, hb, sb, True)                                     # B's Vấn Đạo breaks it
    assert not m.shield and pa.question is not None and pa.question["cast"] == "kiem_quyet"
    hp = m.hp
    c = (await answer(client, ha, sa, True))["combat"]
    assert c["correct"] and not c["shield_broken"]
    assert hp - m.hp == pytest.approx(expected(pa, m, "kiem_quyet", 0, True)) or c["killed"]


async def test_group_shield_needs_every_player_even_with_a_chieu(client, gw, monkeypatch):
    """A bí cảnh boss's big shield needs N right answers from N players (spec 14.2): a landed
    chiêu is one player's right answer, never the whole shield."""
    ha, a, sa = await fighter(client, gw, "chieu_g1", "Chiêu Nhóm")
    hb, b, sb = await fighter(client, gw, "chieu_g2", "Chiêu Đội")
    pa, m = at_math_monster(gw, sa)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, "loan_so_coc", m.x, m.y, "down")
    pb = sb.player
    ch = pa.channel
    from app.realtime import ai
    monkeypatch.setitem(ai.monster_types(), m.kind, {**m.info, "group_shield": True})
    monkeypatch.setattr(ch, "group_need", lambda mon: 2, raising=False)
    prepare(pa)
    await cast(gw, sa, "kiem_quyet", m.eid)
    hp = m.hp
    c = (await answer(client, ha, sa, True))["combat"]
    assert c["correct"] and not c["shield_broken"] and c["shield_progress"] == [1, 2]
    assert m.shield and m.hp == hp and c["damage"] == 0 and pa.mcombo == 1
    assert fx(gw, pa, "gshield")[-1]["n"] == 1
    gw.mono.t += 1
    assert combat.attack(pb, m.eid, gw.mono(), gw.rng) is None
    await settle(gw)
    assert last(sb, "q") and last(sb, "q")["mid"] == m.eid
    res = await answer(client, hb, sb, True)
    assert res["combat"]["shield_broken"] and not m.shield                 # the second player finishes it
