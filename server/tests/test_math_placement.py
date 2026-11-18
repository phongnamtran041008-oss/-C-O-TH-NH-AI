"""M11: the bài kiểm tra đầu vào, learning-path rule 7 (systems/math_placement.py).

"10-15 câu rải các bậc để đặt điểm xuất phát; ai đã giỏi thì được nhảy tầng, nhưng vẫn phải
qua cổng thuần thục của tầng đích." Offered per subject until a floor is cleared; a rising
sitting of real questions; it stops once a floor's bar is out of reach; the start floor is
the lowest floor whose bar was not met, never above the last written floor; the floors below
it count as cleared by placement for everything that asks "which floor is this player on";
on the start floor the mastery gate and the Thiên kiếp nhỏ apply exactly as for anyone."""
import datetime as dt

import pytest
from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_path as mp
from app.models import MathAnswer, MathRun, QuizSession, User
from app.systems import math_ask, math_placement as mpl, math_practice
from tests.helpers import answer_key
from tests.test_math_loop import SUBJECT, make, right_answer, wrong_answer
from tests.test_math_mastery import meet_gate, play_trial, start_trial

LA = SUBJECT


def other_subject() -> str:
    """A second subject with at least two written floors (M11 writes three more)."""
    return next(s for s in math_placement_subjects() if s != LA)


def math_placement_subjects() -> list[str]:
    return [s.id for s in mp.subjects() if len(mpl.written_floors(s.id)) >= 2]


# ------------------------------------------------------------------ helpers
async def state(client, h, subject=LA) -> dict:
    r = await client.get(f"/math/placement?subject_id={subject}", headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def begin(client, h, subject=LA) -> int:
    r = await client.post("/math/placement/start", json={"subject_id": subject}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["run"]["run_id"]


async def next_q(client, h, run_id) -> dict:
    r = await client.post("/math/placement/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def reply(client, h, q: dict, correct: bool, timed_out: bool = False) -> dict:
    key = await answer_key(q["session_id"])
    given = {"timed_out": True} if timed_out else right_answer(q, key) if correct else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": given}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def sit(client, h, subject=LA, right=lambda n, q: True) -> tuple[int, list[dict], dict]:
    """A whole sitting: `right(n, question)` says whether question n (from 0) is answered
    right. Returns (run id, the questions, the last answer)."""
    run_id = await begin(client, h, subject)
    qs, res = [], {}
    for n in range(40):
        out = await next_q(client, h, run_id)
        if out["question"] is None:
            break
        q = out["question"]
        qs.append(q)
        res = await reply(client, h, q, right(n, q))
        if res["math"]["placement"]["decided"]:
            break
    return run_id, qs, res


def wrong_on_floor(floor: int):
    """Right everywhere except every question of `floor`."""
    return lambda n, q: q["math"]["floor"] != floor


async def path_subject(client, h, subject=LA) -> dict:
    data = (await client.get("/math/path", headers=h)).json()
    return next(s for s in data["subjects"] if s["id"] == subject)


# ------------------------------------------------------------------ the plan, as rules
@pytest.mark.parametrize("n", range(1, 10))
def test_a_sitting_plans_between_min_and_max_questions_and_every_floor_gets_one(n):
    p = mp.cfg()["placement_test"]
    counts = mpl.floor_counts(n)
    assert len(counts) == n and min(counts) >= 1 and max(counts) - min(counts) <= 1
    assert p["min_questions"] <= sum(counts) <= p["max_questions"]
    assert counts == sorted(counts, reverse=True)               # a lower floor gets the odd one


def test_the_bounds_come_from_the_config(monkeypatch):
    monkeypatch.setitem(mp.cfg()["placement_test"], "per_floor", 2)
    assert sum(mpl.floor_counts(3)) == mp.cfg()["placement_test"]["min_questions"]
    monkeypatch.setitem(mp.cfg()["placement_test"], "per_floor", 9)
    assert sum(mpl.floor_counts(3)) == mp.cfg()["placement_test"]["max_questions"]
    plan = mpl.subject_plan(LA)
    assert len(plan) == mp.cfg()["placement_test"]["max_questions"]


@pytest.mark.parametrize("subject", [s.id for s in mp.subjects()])
def test_the_plan_rises_floor_by_floor_and_tier_by_tier(subject):
    plan = mpl.subject_plan(subject)
    written = mpl.written_floors(subject)
    if len(written) < 1:
        assert plan == []
        return
    p = mp.cfg()["placement_test"]
    assert p["min_questions"] <= len(plan) <= p["max_questions"]
    keys = [(s.floor, s.tier) for s in plan]
    assert keys == sorted(keys)
    assert sorted({s.floor for s in plan}) == written            # every written floor, nothing else
    s = mp.subject(subject)
    for slot in plan:
        lo, hi = mp.floor_tiers(slot.floor)
        assert lo <= slot.tier <= hi
        assert slot.skill in {k.id for k in s.floor(slot.floor).skills}
        assert any(t.skill == slot.skill and t.tier == slot.tier
                   for t in math_practice._templates(subject, slot.floor))
    for f in written:                                           # the hardest tier of each floor is reached
        assert max(t for fl, t in keys if fl == f) == mp.floor_tiers(f)[1]
        mine = [x.skill for x in plan if x.floor == f]
        assert len(set(mine)) == min(len(mine), len(s.floor(f).skills))   # micro-skills take turns


def test_the_score_decides_as_soon_as_a_bar_is_out_of_reach():
    plan = mpl.subject_plan(LA)
    first = sum(1 for s in plan if s.floor == 1)
    assert mpl.needed(first) == 4
    _, start = mpl.score(plan, [True, True])
    assert start is None
    _, start = mpl.score(plan, [False, False])                   # 3 left, 4 needed: floor 1 is lost
    assert start == 1
    _, start = mpl.score(plan, [False])
    assert start is None
    scores, start = mpl.score(plan, [True] * first + [False, False])
    assert start == 2 and scores[0].met and scores[1].met is False
    _, start = mpl.score(plan, [True] * len(plan))
    assert start == 3


# ------------------------------------------------------------------ when it is offered
@pytest.mark.asyncio
async def test_a_new_player_is_offered_it_and_a_trial_cleared_floor_takes_it_away(client):
    h, uid = await make(client, "pl_offer")
    st = await state(client, h)
    assert st["status"] == "offered" and st["offered"] and st["planned"] == 15
    assert st["written_floors"] == [1, 2, 3] and st["result"] is None
    assert (await path_subject(client, h))["placement"]["offered"]
    h2, uid2 = await make(client, "pl_offer2")
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid2, subject_id=LA, floor=1, mode="trial", tier=2, asked=1, correct=1,
                       passed=True, started_at=clock.now(), ended_at=clock.now()))
        await db.commit()
    st = await state(client, h2)
    assert not st["offered"] and st["reason"] == "cleared"
    r = await client.post("/math/placement/start", json={"subject_id": LA}, headers=h2)
    assert r.status_code == 409 and r.json()["error"]["code"] == "placement_not_offered"


@pytest.mark.asyncio
async def test_a_subject_with_one_written_floor_does_not_offer_it(client, monkeypatch):
    real = math_practice._templates
    monkeypatch.setattr(math_practice, "_templates", lambda s, f: real(s, f) if f == 1 else [])
    h, _ = await make(client, "pl_few")
    st = await state(client, h)
    assert st["status"] == "unavailable" and st["reason"] == "few_floors" and not st["offered"]


@pytest.mark.asyncio
async def test_one_sitting_at_a_time_and_it_can_be_resumed(client):
    h, _ = await make(client, "pl_resume")
    run_id = await begin(client, h)
    st = await state(client, h)
    assert st["status"] == "in_progress" and st["run"]["run_id"] == run_id and not st["offered"]
    r = await client.post("/math/placement/start", json={"subject_id": LA}, headers=h)
    assert r.status_code == 409
    q1 = (await next_q(client, h, run_id))["question"]
    q2 = (await next_q(client, h, run_id))["question"]
    assert q1["session_id"] == q2["session_id"]                  # the open question comes back
    assert q1["context"] == "math_placement" and q1["math"]["placement"]
    # a buổi luyện beside it ends nothing, and its own route refuses the placement sitting
    practice = await client.post("/math/run/start", json={"subject_id": LA, "floor": 1}, headers=h)
    assert practice.status_code == 200
    assert (await state(client, h))["status"] == "in_progress"
    r = await client.post("/math/run/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "wrong_mode"
    path = (await client.get("/math/path", headers=h)).json()
    assert path["run"]["run_id"] == practice.json()["run"]["run_id"]


# ------------------------------------------------------------------ a sitting
@pytest.mark.asyncio
async def test_all_right_places_on_the_last_written_floor_and_never_above(client, frozen):
    h, uid = await make(client, "pl_all")
    run_id, qs, res = await sit(client, h)
    plan = mpl.subject_plan(LA)
    assert len(qs) == len(plan) == 15
    got = [(q["math"]["floor"], q["math"]["tier"], q["math"]["skill"]) for q in qs]
    assert got == [(s.floor, s.tier, s.skill) for s in plan]     # rising, as planned
    for q in qs:                                                 # each with its normal time limit
        assert q["time_limit"] == mp.time_limit(q["qtype"], q["math"]["tier"])
    result = res["math"]["placement_result"]
    assert result["start_floor"] == 3 == mpl.written_floors(LA)[-1]
    assert result["skipped"] == [1, 2] and not result["abandoned"]
    assert [(f["floor"], f["asked"], f["correct"]) for f in result["floors"]] == [(1, 5, 5), (2, 5, 5), (3, 5, 5)]
    r = await client.post("/math/placement/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 409                                  # the sitting is over
    st = await state(client, h)
    assert st["status"] == "done" and not st["offered"] and st["result"]["start_floor"] == 3
    s = await path_subject(client, h)
    assert [f["state"] for f in s["floors"][:5]] == ["cleared", "cleared", "open", "locked", "locked"]
    assert [f["cleared_by"] for f in s["floors"][:4]] == ["placement", "placement", None, None]
    assert s["cleared"] == [1, 2] and s["next_floor"] == 3
    assert s["placement"]["start_floor"] == 3 and s["placement"]["status"] == "done"
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2}
        assert await math_practice.trial_floors(db, uid, LA) == set()        # told apart
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
    assert len(rows) == 15 and all(a.run_id == run_id for a in rows)       # real answers, in the log
    frozen.advance(days=25)                 # well past retake_after_days (and inside a login's life)
    assert mp.cfg()["placement_test"]["retake_after_days"] < 25
    assert (await state(client, h))["status"] == "done"                     # a result that skipped is final


@pytest.mark.parametrize("fail_floor, start_floor, asked", [(1, 1, 2), (2, 2, 7), (3, 3, 12)])
@pytest.mark.asyncio
async def test_every_outcome_floor_and_the_early_stop(client, fail_floor, start_floor, asked):
    h, uid = await make(client, f"pl_fail{fail_floor}")
    run_id, qs, res = await sit(client, h, right=wrong_on_floor(fail_floor))
    # two misses on a floor of five (four needed) decide it: nothing above it is asked
    assert len(qs) == asked and max(q["math"]["floor"] for q in qs) == fail_floor
    result = res["math"]["placement_result"]
    assert result["start_floor"] == start_floor
    assert result["skipped"] == list(range(1, start_floor))
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == set(range(1, start_floor))
        assert await math_ask.open_floor(db, uid, LA) == start_floor


@pytest.mark.asyncio
async def test_a_floor_missed_once_still_passes_with_four_of_five(client):
    h, _ = await make(client, "pl_one_miss")
    _, qs, res = await sit(client, h, right=lambda n, q: n != 0)
    assert len(qs) == 15 and res["math"]["placement_result"]["start_floor"] == 3


@pytest.mark.asyncio
async def test_timeouts_count_as_wrong(client, frozen):
    h, uid = await make(client, "pl_timeout")
    run_id = await begin(client, h)
    q = (await next_q(client, h, run_id))["question"]
    res = await reply(client, h, q, True, timed_out=True)           # the card's countdown ran out
    assert not res["correct"] and res["math"]["timed_out"] and res["math"]["placement"]["correct"] == 0
    q = (await next_q(client, h, run_id))["question"]
    frozen.advance(seconds=q["time_limit"] + 30)                   # nobody answered at all
    out = await next_q(client, h, run_id)
    assert out["question"] is None                                  # two misses on floor 1: decided
    assert out["result"]["start_floor"] == 1
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer.correct, MathAnswer.timed_out)
                                 .where(MathAnswer.run_id == run_id).order_by(MathAnswer.id))).all()
        s = await db.get(QuizSession, q["session_id"])
    assert rows == [(False, True), (False, True)] and s.answered_at is not None
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": {"value": True}},
                          headers=h)
    assert r.status_code == 409                                     # settled: no late answer


@pytest.mark.asyncio
async def test_an_abandoned_sitting_skips_nothing_and_may_be_retaken_after_the_wait(client, frozen):
    h, uid = await make(client, "pl_abandon")
    run_id = await begin(client, h)
    for _ in range(5):                                              # floor 1 all right ...
        await reply(client, h, (await next_q(client, h, run_id))["question"], True)
    r = await client.post("/math/placement/abandon", json={"run_id": run_id}, headers=h)
    assert r.status_code == 200, r.text
    st = r.json()                                                   # ... but given up: nothing skipped
    assert st["status"] == "done" and not st["offered"]
    assert st["result"]["abandoned"] and st["result"]["start_floor"] == 1 and st["result"]["skipped"] == []
    assert st["result"]["retake_at"] is not None
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == set()
    r = await client.post("/math/placement/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 409
    frozen.advance(days=mp.cfg()["placement_test"]["retake_after_days"] - 1)
    assert not (await state(client, h))["offered"]
    frozen.advance(days=1)
    st = await state(client, h)
    assert st["offered"] and st["reason"] == "retake"
    _, _, res = await sit(client, h)
    assert res["math"]["placement_result"]["start_floor"] == 3
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2}


@pytest.mark.asyncio
async def test_placed_on_floor_one_may_retake_after_the_wait(client, frozen):
    h, _ = await make(client, "pl_retake")
    _, _, res = await sit(client, h, right=lambda n, q: False)
    assert res["math"]["placement_result"]["start_floor"] == 1
    assert not (await state(client, h))["offered"]
    frozen.advance(days=mp.cfg()["placement_test"]["retake_after_days"])
    assert (await state(client, h))["offered"]


# ------------------------------------------------------------------ rule 4's one exception
@pytest.mark.asyncio
async def test_placement_questions_skip_the_tier_unlock_and_are_marked_as_placement(client):
    h, uid = await make(client, "pl_rule4")
    run_id, qs, _ = await sit(client, h, right=wrong_on_floor(2))
    first_tier2 = next(q for q in qs if q["math"]["floor"] == 1 and q["math"]["tier"] == 2)
    async with dbm.SessionLocal() as db:
        before = (await db.execute(select(MathAnswer).where(
            MathAnswer.user_id == uid, MathAnswer.skill_id == first_tier2["math"]["skill"],
            MathAnswer.tier == 1))).scalars().all()
        runs = {a.run_id for a in (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars()}
        modes = {r.mode for r in (await db.execute(select(MathRun).where(MathRun.id.in_(runs)))).scalars()}
    assert before == []                     # a tier-2 question with no tier-1 answer: the stated exception
    assert runs == {run_id} and modes == {"placement"}


# ------------------------------------------------------------------ the start floor's gate still applies
@pytest.mark.asyncio
async def test_the_gate_and_the_trial_of_the_start_floor_apply_as_for_anyone(client):
    h, uid = await make(client, "pl_gate")
    await sit(client, h)
    s = await path_subject(client, h)
    floor3 = s["floors"][2]
    assert floor3["playable"] and floor3["state"] == "open" and not floor3["gate"]["ok"]
    r = await start_trial(client, h, floor=3)
    assert r.status_code == 409 and r.json()["error"]["code"] == "gate_not_met"
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 4}, headers=h)
    assert r.status_code == 400                                      # floor 4 has no question
    await meet_gate(uid, floor=3)
    r = await start_trial(client, h, floor=3)
    assert r.status_code == 200, r.text
    played = await play_trial(client, h, r.json()["run"]["run_id"])
    assert played[-1]["res"]["math"]["trial"]["passed"] is True
    s = await path_subject(client, h)
    assert [f["cleared_by"] for f in s["floors"][:4]] == ["placement", "placement", "trial", None]


@pytest.mark.asyncio
async def test_spiral_review_treats_the_skipped_floors_as_floors_below(client):
    h, uid = await make(client, "pl_review")
    await sit(client, h, right=lambda n, q: q["math"]["floor"] != 3 or n % 2 == 0)
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2}
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 3}, headers=h)
    run_id = r.json()["run"]["run_id"]
    floors = []
    for _ in range(8):
        q = (await client.post("/math/run/next", json={"run_id": run_id}, headers=h)).json()["question"]
        floors.append((q["math"]["floor"], q["math"]["review"]))
        key = await answer_key(q["session_id"])
        await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                          headers=h)
    reviews = [f for f, review in floors if review]
    assert reviews and set(reviews) <= {1, 2}                        # micro-skills never answered are due
    assert all(f == 3 for f, review in floors if not review)


# ------------------------------------------------------------------ everything agrees on the floor
@pytest.mark.asyncio
async def test_open_floor_and_the_dungeon_agree_with_the_placement(client):
    h, uid = await make(client, "pl_agree")
    await sit(client, h, right=wrong_on_floor(3))
    async with dbm.SessionLocal() as db:
        assert await math_ask.open_floor(db, uid, LA) == 3
        assert await math_ask.own_floor(db, uid, LA) == (LA, 3)
        user = await db.get(User, uid)
        q = await math_ask.pick_own(db, user, subject_id=LA)
        assert q.public()["math"]["floor"] == 3                      # own-floor questions from the start floor
    view = (await client.get("/math/dungeon", headers=h)).json()   # M10: hầm ngục
    if view["subject_id"] == LA:
        assert view["own_floor"] == 3
        assert [f["floor"] for f in view["floors"] if f["open"]] == [1, 2, 3]


@pytest.mark.asyncio
async def test_a_second_subject_is_independent_of_the_first(client):
    other = other_subject()
    h, uid = await make(client, "pl_two")
    await sit(client, h)
    st = await state(client, h, other)
    assert st["offered"] and st["result"] is None
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, other) == set()
        assert await math_ask.open_floor(db, uid, other) == 1
    _, qs, res = await sit(client, h, other, right=wrong_on_floor(2))
    assert {q["math"]["subject"] for q in qs} == {other}
    assert res["math"]["placement_result"]["start_floor"] == 2
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, other) == {1}
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2}
    s = await path_subject(client, h, other)
    assert s["placement"]["start_floor"] == 2 and s["floors"][0]["cleared_by"] == "placement"
