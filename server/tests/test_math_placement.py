"""M11 (and M11 đợt 2): the bài kiểm tra đầu vào, learning-path rule 7 (systems/math_placement.py).

"10-15 câu rải các bậc để đặt điểm xuất phát; ai đã giỏi thì được nhảy tầng, nhưng vẫn phải
qua cổng thuần thục của tầng đích." Offered per subject until a floor is cleared; a climb in
blocks over the written floors (a passed block jumps up, a failed one stops the climb and
steps back to confirm what was jumped over); at most 15 questions whatever happens, at least
10 for a player who gets everything right; the start floor is the lowest floor whose block
failed, never above the last written floor; the floors below it count as cleared by
placement for everything that asks "which floor is this player on"; on the start floor the
mastery gate and the Thiên kiếp nhỏ apply exactly as for anyone.

The sittings run on fixture banks of 3, 6 and 9 written floors (`written`), so the result does
not depend on how many floors the content agents have written when this runs."""
import datetime as dt
import itertools

import pytest
from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_items as mi
from app.learning import math_path as mp
from app.models import MathAnswer, MathRun, QuizSession, User
from app.systems import math_ask, math_placement as mpl, math_practice, math_tree_progress
from tests.helpers import answer_key
from tests.test_math_loop import SUBJECT, fake_items, make, right_answer, wrong_answer
from tests.test_math_mastery import meet_gate, play_trial, start_trial

LA = SUBJECT


def other_subject() -> str:
    """A second subject with at least two written floors (M11 writes three more)."""
    return next(s for s in math_placement_subjects() if s != LA)


def math_placement_subjects() -> list[str]:
    return [s.id for s in mp.subjects() if len(mpl.written_floors(s.id)) >= 2]


def thien_kiep(floor: int, skill: str) -> mi.MathItem:
    """A tribulation template at the floor's top tier: never a placement question."""
    return mi.MathItem(id=f"fake_tk_{floor}", subject=SUBJECT, skill=skill, floor=floor,
                       tier=mp.floor_tiers(floor)[1], qtype="tribulation", prompt_vi="Một bài tổng hợp.",
                       answer=None, solution_vi=("Lời giải.",), reviewed=True)


def bank_with(n: int) -> dict[str, mi.MathItem]:
    """The real bank of the other subjects, and fake questions on floors 1..n of LA (with a
    Thiên kiếp on every floor whose tiers allow one)."""
    items = {k: v for k, v in mi.bank().items() if v.subject != LA}
    for f in range(1, n + 1):
        items.update(fake_items(f))
        if mp.floor_tiers(f)[1] >= 4:
            tk = thien_kiep(f, mp.subject(LA).floor(f).skills[0].id)
            items[tk.id] = tk
    return items


@pytest.fixture
def written(monkeypatch):
    """`written(n)`: LA has questions on floors 1..n only (and no generators)."""
    real_gens = {k: v for k, v in mi.generators().items() if v.subject != LA}
    real_bank = dict(mi.bank())

    def use(n: int) -> list[int]:
        items = {k: v for k, v in real_bank.items() if v.subject != LA}
        items.update(bank_with(n) if n else {})
        monkeypatch.setattr(mi, "bank", lambda: items)
        monkeypatch.setattr(mi, "generators", lambda: real_gens)
        assert mpl.written_floors(LA) == list(range(1, n + 1))
        return mpl.written_floors(LA)
    return use


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


def below(floor: int):
    """A player who knows every floor below `floor` and nothing from `floor` up."""
    return lambda n, q: q["math"]["floor"] < floor


async def path_subject(client, h, subject=LA) -> dict:
    data = (await client.get("/math/path", headers=h)).json()
    return next(s for s in data["subjects"] if s["id"] == subject)


def fixture_layout(n: int) -> mpl.Layout:
    subject = mp.subject(LA)
    temps: dict[int, list] = {}
    for f in range(1, n + 1):
        temps[f] = list(fake_items(f).values())
        if mp.floor_tiers(f)[1] >= 4:
            temps[f].append(thien_kiep(f, subject.floor(f).skills[0].id))
    return mpl.layout(subject, temps)


def every_sitting(lay: mpl.Layout):
    """Every possible sitting of this layout, as (answers, walk): each block decided right or
    wrong in each way it can end (a failed block ends at each question it can end on)."""
    need = mpl.needed(lay.block)

    def block_endings():
        yield [True] * lay.block                                     # passed
        for k in range(lay.block):                                   # failed: wrong at k, out of reach
            for pattern in itertools.product((True, False), repeat=k + 1):
                if pattern[-1] is False:
                    s = mpl.FloorScore(0, lay.block, k + 1, sum(pattern), need)
                    prefix = mpl.FloorScore(0, lay.block, k, sum(pattern[:-1]), need)
                    if s.met is False and prefix.met is None:
                        yield list(pattern)

    def go(answers):
        w = mpl.walk(lay, answers)
        if w.start is not None:
            yield answers, w
            return
        for ending in block_endings():
            yield from go(answers + ending)
    yield from go([])


# ------------------------------------------------------------------ the climb, as rules
def test_the_bar_of_a_block():
    assert [mpl.needed(n) for n in (3, 4, 5)] == [3, 4, 4]          # 80%


@pytest.mark.parametrize("n", range(2, 10))
def test_no_sitting_passes_max_questions_and_all_right_asks_at_least_min(n):
    p = mp.cfg()["placement_test"]
    lay = fixture_layout(n)
    assert lay.floors == tuple(range(1, n + 1))
    assert p["block_min"] <= lay.block <= p["per_floor"]
    lengths = [len(answers) for answers, _ in every_sitting(lay)]
    assert lengths and max(lengths) <= p["max_questions"] and max(lengths) <= lay.most
    right = mpl.walk(lay, [True] * 40)
    asked = len([s for s in right.scores for _ in range(s.asked)])
    assert p["min_questions"] <= asked <= p["max_questions"]
    assert right.start == n                                         # never above the last written floor
    # a beginner stops as soon as the first block is out of reach
    assert min(lengths) == lay.block - mpl.needed(lay.block) + 1


def test_the_shape_for_three_six_and_nine_floors():
    assert (fixture_layout(3).block, fixture_layout(3).stride) == (4, 1)     # every floor, 12 questions
    assert (fixture_layout(6).block, fixture_layout(6).stride) == (3, 2)     # floors 1-3-5-6
    assert (fixture_layout(9).block, fixture_layout(9).stride) == (3, 3)     # floors 1-4-7-9
    w = mpl.walk(fixture_layout(9), [True] * 40)
    assert [s.floor for s in w.scores] == [1, 4, 7, 9]


@pytest.mark.parametrize("n", [3, 6, 9])
def test_every_outcome_floor_is_reachable(n):
    lay = fixture_layout(n)
    reached = {w.start for _, w in every_sitting(lay)}
    assert reached == set(range(1, n + 1))
    for target in range(1, n + 1):                                  # and the honest player lands right
        answers, w = [], mpl.walk(lay, [])
        while w.start is None:
            answers.append(w.next.floor < target)
            w = mpl.walk(lay, answers)
        assert w.start == target and len(answers) <= mp.cfg()["placement_test"]["max_questions"]


@pytest.mark.parametrize("n", [3, 6, 9])
def test_the_climb_rises_until_it_fails_and_a_block_rises_tier_by_tier(n):
    lay = fixture_layout(n)
    s = mp.subject(LA)
    for floor, block in zip(lay.floors, lay.blocks):
        assert len(block) == lay.block
        tiers = [x.tier for x in block]
        assert tiers == sorted(tiers) and tiers[-1] == mp.floor_tiers(floor)[1]   # the hardest tier is reached
        assert all(x.floor == floor and x.skill in {k.id for k in s.floor(floor).skills} for x in block)
        for tier in set(tiers):
            mine = [x.skill for x in block if x.tier == tier]
            assert len(set(mine)) == min(len(mine), len(s.floor(floor).skills))  # micro-skills take turns
    for answers, w in every_sitting(lay):
        floors = [sc.floor for sc in w.scores]
        assert len(set(floors)) == len(floors)                      # no floor asked twice
        first_fail = next((i for i, sc in enumerate(w.scores) if sc.met is False), len(w.scores))
        assert floors[:first_fail + 1] == sorted(floors[:first_fail + 1])         # up until the first failure
        assert floors[first_fail:] == sorted(floors[first_fail:], reverse=True)   # then only down, to confirm
        assert w.start == min((sc.floor for sc in w.scores if sc.met is False), default=lay.floors[-1])


def test_the_climb_steps_back_to_confirm_a_floor_it_jumped_over():
    lay = fixture_layout(9)                                        # blocks of 3 (all 3 needed), floors 1-4-7-9
    w = mpl.walk(lay, [True] * 3 + [False])                        # floor 1 passed, floor 4 failed
    assert w.start is None and w.next.floor == 3
    w = mpl.walk(lay, [True] * 3 + [False] + [True] * 3)           # floor 3 passed: start on 4
    assert w.start == 4
    w = mpl.walk(lay, [True] * 3 + [False, False, True, True, True])   # 3 failed, 2 passed: start on 3
    assert w.start == 3 and [s.floor for s in w.scores] == [1, 4, 3, 2]
    w = mpl.walk(lay, [True] * 6 + [False, True, True, True])      # 1, 4 passed; 7 failed; 6 passed
    assert w.start == 7


def test_the_numbers_come_from_the_config(monkeypatch):
    monkeypatch.setitem(mp.cfg()["placement_test"], "max_questions", 30)
    lay = fixture_layout(9)
    assert (lay.block, lay.stride) == (3, 1) and lay.most == 27     # room for every floor
    monkeypatch.setitem(mp.cfg()["placement_test"], "max_questions", 15)
    monkeypatch.setitem(mp.cfg()["placement_test"], "pass_pct", 60)
    assert mpl.needed(3) == 2
    monkeypatch.setitem(mp.cfg()["placement_test"], "block_min", 5)
    lay = fixture_layout(3)
    assert lay.block == 5 and lay.most == 15


def test_a_thien_kiep_is_never_a_placement_question_and_alone_writes_no_floor():
    subject = mp.subject(LA)
    lay = fixture_layout(9)
    assert all(slot.skill and slot.tier <= 5 for block in lay.blocks for slot in block)
    tk = thien_kiep(5, subject.floor(5).skills[0].id)
    assert mpl.askable([tk]) == []
    temps = {1: list(fake_items(1).values()), 2: list(fake_items(2).values()), 5: [tk]}
    assert mpl.layout(subject, temps).floors == (1, 2)


# ------------------------------------------------------------------ when it is offered
@pytest.mark.asyncio
async def test_a_new_player_is_offered_it_and_a_trial_cleared_floor_takes_it_away(client, written):
    written(3)
    h, uid = await make(client, "pl_offer")
    st = await state(client, h)
    assert st["status"] == "offered" and st["offered"] and st["planned"] == 12 and st["block"] == 4
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
async def test_a_subject_with_one_written_floor_does_not_offer_it(client, written):
    written(1)
    h, _ = await make(client, "pl_few")
    st = await state(client, h)
    assert st["status"] == "unavailable" and st["reason"] == "few_floors" and not st["offered"]


@pytest.mark.asyncio
async def test_one_sitting_at_a_time_and_it_can_be_resumed(client, written):
    written(6)
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
@pytest.mark.parametrize("n, path", [(3, [1, 2, 3]), (6, [1, 3, 5, 6]), (9, [1, 4, 7, 9])])
@pytest.mark.asyncio
async def test_all_right_climbs_to_the_last_written_floor_and_never_above(client, frozen, written, n, path):
    written(n)
    h, uid = await make(client, f"pl_all{n}")
    run_id, qs, res = await sit(client, h)
    lay = mpl.subject_layout(LA)
    assert len(qs) == lay.block * len(path) and 10 <= len(qs) <= 15
    got = [(q["math"]["floor"], q["math"]["tier"], q["math"]["skill"]) for q in qs]
    assert got == [(s.floor, s.tier, s.skill) for f in path for s in lay.blocks[f - 1]]   # rising, as planned
    for q in qs:                                                 # each with its normal time limit, never a Thiên kiếp
        assert q["time_limit"] == mp.time_limit(q["qtype"], q["math"]["tier"]) and q["qtype"] != "tribulation"
    result = res["math"]["placement_result"]
    assert result["start_floor"] == n == mpl.written_floors(LA)[-1]
    assert result["skipped"] == list(range(1, n)) and not result["abandoned"]
    assert [(f["floor"], f["asked"], f["correct"], f["met"]) for f in result["floors"]] == \
        [(f, lay.block, lay.block, True) for f in path]
    r = await client.post("/math/placement/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 409                                  # the sitting is over
    st = await state(client, h)
    assert st["status"] == "done" and not st["offered"] and st["result"]["start_floor"] == n
    s = await path_subject(client, h)
    states = [f["state"] for f in s["floors"]]
    assert states[:n - 1] == ["cleared"] * (n - 1) and states[n - 1] == "open"
    assert [f["cleared_by"] for f in s["floors"][:n]] == ["placement"] * (n - 1) + [None]
    assert s["cleared"] == list(range(1, n)) and s["next_floor"] == n
    assert s["placement"]["start_floor"] == n and s["placement"]["status"] == "done"
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == set(range(1, n))
        assert await math_practice.trial_floors(db, uid, LA) == set()        # told apart
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
    assert len(rows) == len(qs) and all(a.run_id == run_id for a in rows)  # real answers, in the log
    frozen.advance(days=25)                 # well past retake_after_days (and inside a login's life)
    assert mp.cfg()["placement_test"]["retake_after_days"] < 25
    assert (await state(client, h))["status"] == "done"                     # a result that skipped is final


@pytest.mark.parametrize("n, target", [(3, 1), (3, 2), (3, 3), (6, 2), (6, 4), (6, 5), (9, 1), (9, 3),
                                       (9, 6), (9, 8)])
@pytest.mark.asyncio
async def test_every_outcome_floor_and_the_early_stop(client, written, n, target):
    written(n)
    h, uid = await make(client, f"pl_out{n}_{target}")
    run_id, qs, res = await sit(client, h, right=below(target))
    assert len(qs) <= mp.cfg()["placement_test"]["max_questions"]
    # a block of the start floor ends at its first miss (its bar wants every answer): no more is asked
    assert sum(1 for q in qs if q["math"]["floor"] == target) == 1
    assert max(q["math"]["floor"] for q in qs) <= max(target, 1) + mpl.subject_layout(LA).stride
    result = res["math"]["placement_result"]
    assert result["start_floor"] == target
    assert result["skipped"] == list(range(1, target))
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == set(range(1, target))
        # Đạo Thụ: the player's own floor is their frontier - the start floor, except floor 2, which
        # holds only an optional node: then the next main node, on floor 3
        assert await math_ask.own_floor(db, uid, LA) == (LA, 3 if target == 2 else target)


@pytest.mark.asyncio
async def test_a_beginner_stops_after_one_question(client, written):
    written(9)
    h, _ = await make(client, "pl_beginner")
    _, qs, res = await sit(client, h, right=lambda n, q: False)
    assert len(qs) == 1 and res["math"]["placement_result"]["start_floor"] == 1


@pytest.mark.asyncio
async def test_timeouts_count_as_wrong(client, frozen, written):
    written(9)
    h, uid = await make(client, "pl_timeout")
    run_id = await begin(client, h)
    q = (await next_q(client, h, run_id))["question"]
    res = await reply(client, h, q, True)
    q = (await next_q(client, h, run_id))["question"]
    res = await reply(client, h, q, True, timed_out=True)           # the card's countdown ran out
    assert not res["correct"] and res["math"]["timed_out"] and res["math"]["placement"]["correct"] == 1
    assert res["math"]["placement"]["decided"] and res["math"]["placement_result"]["start_floor"] == 1
    h2, uid2 = await make(client, "pl_timeout2")
    run_id = await begin(client, h2)
    q = (await next_q(client, h2, run_id))["question"]
    frozen.advance(seconds=q["time_limit"] + 30)                   # nobody answered at all
    out = await next_q(client, h2, run_id)
    assert out["question"] is None and out["result"]["start_floor"] == 1
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer.correct, MathAnswer.timed_out)
                                 .where(MathAnswer.run_id == run_id).order_by(MathAnswer.id))).all()
        s = await db.get(QuizSession, q["session_id"])
    assert rows == [(False, True)] and s.answered_at is not None
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": {"value": True}},
                          headers=h2)
    assert r.status_code == 409                                     # settled: no late answer


@pytest.mark.asyncio
async def test_an_abandoned_sitting_skips_nothing_and_may_be_retaken_after_the_wait(client, frozen, written):
    written(6)
    h, uid = await make(client, "pl_abandon")
    run_id = await begin(client, h)
    for _ in range(4):                                              # floor 1 all right, floor 3 begun ...
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
    assert res["math"]["placement_result"]["start_floor"] == 6
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2, 3, 4, 5}


@pytest.mark.asyncio
async def test_placed_on_floor_one_may_retake_after_the_wait(client, frozen, written):
    written(3)
    h, _ = await make(client, "pl_retake")
    _, _, res = await sit(client, h, right=lambda n, q: False)
    assert res["math"]["placement_result"]["start_floor"] == 1
    assert not (await state(client, h))["offered"]
    frozen.advance(days=mp.cfg()["placement_test"]["retake_after_days"])
    assert (await state(client, h))["offered"]


# ------------------------------------------------------------------ rule 4's exception
@pytest.mark.asyncio
async def test_placement_questions_skip_the_tier_unlock_and_are_marked_as_placement(client, written):
    written(9)
    h, uid = await make(client, "pl_rule4")
    run_id, qs, _ = await sit(client, h, right=below(5))
    # floor 4 (tiers 2-3) was jumped to from floor 1: a tier-3 question of a micro-skill the
    # player had never answered at tier 2 - the stated exception
    k = next(i for i, q in enumerate(qs) if q["math"]["floor"] == 4 and q["math"]["tier"] == 3)
    skill = qs[k]["math"]["skill"]
    assert not any(q["math"]["skill"] == skill and q["math"]["tier"] == 2 for q in qs[:k])
    async with dbm.SessionLocal() as db:
        runs = {a.run_id for a in (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars()}
        modes = {r.mode for r in (await db.execute(select(MathRun).where(MathRun.id.in_(runs)))).scalars()}
    assert modes == {"placement"} and runs == {run_id}


# ------------------------------------------------------------------ the start floor's gate still applies
@pytest.mark.asyncio
async def test_the_gate_and_the_trial_of_the_start_floor_apply_as_for_anyone(client, written):
    written(3)
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
async def test_spiral_review_treats_the_skipped_floors_as_floors_below(client, written):
    written(3)
    h, uid = await make(client, "pl_review")
    await sit(client, h, right=below(3))
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
async def test_open_floor_and_the_dungeon_agree_with_the_placement(client, written):
    written(6)
    h, uid = await make(client, "pl_agree")
    await sit(client, h, right=below(3))
    async with dbm.SessionLocal() as db:
        assert await math_tree_progress.reached_floors(db, uid, LA) == {1, 3}     # 2: an optional node only
        assert await math_ask.own_floor(db, uid, LA) == (LA, 3)
        user = await db.get(User, uid)
        q = await math_ask.pick_own(db, user, subject_id=LA)
        assert q.public()["math"]["floor"] == 3                      # own-floor questions from the start floor
    view = (await client.get("/math/dungeon", headers=h)).json()   # M10: hầm ngục
    if view["subject_id"] == LA:
        assert view["own_floor"] == 3
        assert [f["floor"] for f in view["floors"] if f["open"]] == [1, 3]


@pytest.mark.asyncio
async def test_a_second_subject_is_independent_of_the_first(client, written):
    written(3)
    other = other_subject()
    h, uid = await make(client, "pl_two")
    await sit(client, h)
    st = await state(client, h, other)
    assert st["offered"] and st["result"] is None
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, other) == set()
        assert await math_ask.own_floor(db, uid, other) == (other, 1)
    _, qs, res = await sit(client, h, other, right=below(2))
    assert {q["math"]["subject"] for q in qs} == {other}
    assert res["math"]["placement_result"]["start_floor"] == 2
    async with dbm.SessionLocal() as db:
        assert await math_practice.cleared_floors(db, uid, other) == {1}
        assert await math_practice.cleared_floors(db, uid, LA) == {1, 2}
    s = await path_subject(client, h, other)
    assert s["placement"]["start_floor"] == 2 and s["floors"][0]["cleared_by"] == "placement"
