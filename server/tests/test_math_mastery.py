"""M5: leaving a floor and coming back to it.

Learning-path rule 3 - the mastery gate (every micro-skill of the floor answered at the
floor's hardest tier with at least 80% of its last 5 right) and the floor's own test, the
Thiên kiếp nhỏ. Learning-path rule 6 - spiral review: a sitting keeps mixing in questions
from the floors below, on the 1 -> 3 -> 7 -> 14 day schedule, worst-answered first.
"""
import datetime as dt
import sqlite3

import pytest
from sqlalchemy import select

from app import db as dbm
from app.learning import math_items as mi
from app.learning import math_mastery as mm
from app.learning import math_path as mp
from app.models import MathAnswer, MathRetry, MathRun
from tests.helpers import answer_key
from tests.test_math_loop import (SUBJECT, ask, clear_below, fake_items, log_answers, make, play,
                                  right_answer, start, wrong_answer)

FLOOR1_SKILLS = [s.id for s in mp.subject(SUBJECT).floor(1).skills]


# ------------------------------------------------------------------ helpers
def results(*, tier: int, answers: list[bool], below: int = 0) -> dict[int, list[bool]]:
    """One micro-skill's log: `answers` at `tier`, and enough right answers below it for
    that tier to be open at all (rule 4)."""
    out = {t: [True] * 5 for t in range(1, tier)} if below == 0 else {t: [True] * below for t in range(1, tier)}
    out[tier] = answers
    return out


async def meet_gate(uid, floor=1, subject=SUBJECT, skip: set[str] = frozenset(), weak=False):
    """Give every micro-skill of a floor the log the gate wants: the lower tiers open and
    the top tier answered well. `skip` leaves a micro-skill untouched (so the gate is not
    met); `weak` answers the top tier badly instead."""
    lo, hi = mp.floor_tiers(floor)
    window = mp.cfg()["mastery_gate"]["window"]
    for skill in (s.id for s in mp.subject(subject).floor(floor).skills):
        if skill in skip:
            continue
        for tier in range(lo, hi):
            await log_answers(uid, skill, tier, [True] * window, floor=floor)
        top = [False] * window if weak else [True] * window
        await log_answers(uid, skill, hi, top, floor=floor)


async def run_row(run_id) -> MathRun:
    async with dbm.SessionLocal() as db:
        return await db.get(MathRun, run_id)


async def answers_of(uid) -> list[MathAnswer]:
    async with dbm.SessionLocal() as db:
        return list((await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid)
                                      .order_by(MathAnswer.id))).scalars())


async def start_trial(client, h, floor=1, subject=SUBJECT):
    return await client.post("/math/trial/start", json={"subject_id": subject, "floor": floor}, headers=h)


async def play_trial(client, h, run_id, wrong_at: set[int] = frozenset()) -> list[dict]:
    """Answer a whole Thiên kiếp nhỏ, missing the questions whose number is in `wrong_at`."""
    out = []
    for n in range(1, 99):
        q, res = await play(client, h, run_id, correct=n not in wrong_at)
        out.append({"q": q, "res": res})
        trial = res["math"]["trial"]
        if trial["passed"] is not None:
            break
    return out


# ------------------------------------------------------------------ rule 3 (a): the gate, as rules
def test_the_gate_wants_four_of_the_last_five_right_at_the_top_tier():
    gate = mm.skill_gate("s", 1, results(tier=2, answers=[True, False, True, True, True]))
    assert (gate.tier, gate.top_tier, gate.at_top) == (2, 2, True)
    assert (gate.correct, gate.needed, gate.window) == (4, 4, 5) and gate.ok
    assert not mm.skill_gate("s", 1, results(tier=2, answers=[True, False, False, True, True])).ok


def test_only_the_last_five_answers_count():
    old_misses = [False] * 10 + [True] * 5
    assert mm.skill_gate("s", 1, results(tier=2, answers=old_misses)).ok
    assert not mm.skill_gate("s", 1, results(tier=2, answers=[True] * 10 + [False, False])).ok


def test_the_gate_needs_a_full_window_of_answers():
    gate = mm.skill_gate("s", 1, results(tier=2, answers=[True] * 4))
    assert gate.at_top and gate.correct == 4 and not gate.ok    # four right, but only four answers
    assert mm.skill_gate("s", 1, results(tier=2, answers=[True] * 5)).ok


def test_a_micro_skill_still_on_a_lower_tier_is_not_through_the_gate():
    """Floor 1 is tiers 1-2: being good at tier 1 is not finishing the floor."""
    gate = mm.skill_gate("s", 1, {1: [True] * 5})
    assert (gate.tier, gate.top_tier) == (2, 2) and gate.at_top       # five right at tier 1 opened tier 2
    only_two_right = mm.skill_gate("s", 1, {1: [True, True, False, False, False]})
    assert (only_two_right.tier, only_two_right.at_top, only_two_right.ok) == (1, False, False)


def test_the_needed_count_follows_the_config(monkeypatch):
    monkeypatch.setitem(mp.cfg()["mastery_gate"], "min_correct_pct", 100)
    assert mm.needed_correct() == 5
    assert not mm.skill_gate("s", 1, results(tier=2, answers=[True, False, True, True, True])).ok
    monkeypatch.setitem(mp.cfg()["mastery_gate"], "min_correct_pct", 60)
    assert mm.needed_correct() == 3
    assert mm.skill_gate("s", 1, results(tier=2, answers=[True, False, True, False, True])).ok


def test_the_floor_gate_names_the_micro_skills_to_go_and_practise():
    good = results(tier=2, answers=[True] * 5)
    bad = results(tier=2, answers=[False] * 5)
    gate = mm.floor_gate(1, FLOOR1_SKILLS, {s: (bad if i else good) for i, s in enumerate(FLOOR1_SKILLS)})
    assert not gate.ok
    assert [s.skill_id for s in gate.weak] == FLOOR1_SKILLS[1:]
    assert gate.view()["weak"] == FLOOR1_SKILLS[1:]
    every = mm.floor_gate(1, FLOOR1_SKILLS, {s: good for s in FLOOR1_SKILLS})
    assert every.ok and not every.weak and every.view()["ok"]


def test_a_floor_without_micro_skills_is_never_through_the_gate():
    assert not mm.floor_gate(1, [], {}).ok


# ------------------------------------------------------------------ which floors are open
def test_the_first_floor_is_open_and_the_rest_wait_for_the_floor_below():
    s = mp.subject(SUBJECT)
    assert [mm.floor_state(s, n, set()) for n in range(1, 11)] == ["open"] + ["locked"] * 9
    assert [mm.floor_state(s, n, {1, 2}) for n in range(1, 5)] == ["cleared", "cleared", "open", "locked"]
    assert mm.playable(s, 3, {1, 2}) and not mm.playable(s, 4, {1, 2})


def test_the_hidden_floor_waits_for_the_last_main_floor_and_opens_nothing():
    s = mp.subject(SUBJECT)
    mains = {f.number for f in s.main_floors}
    assert mm.floor_state(s, 10, mains - {9}) == "locked"
    assert mm.floor_state(s, 10, mains) == "open"
    assert mm.floor_below(s, 10) == 9 and mm.floor_above(s, 9) == 10 and mm.floor_above(s, 10) is None
    assert mm.floor_below(s, 1) is None


def test_a_floor_opens_the_next_one_and_nothing_else():
    s = mp.subject(SUBJECT)
    assert [mm.floor_above(s, n) for n in range(1, 10)] == list(range(2, 11))
    assert [mm.floor_below(s, n) for n in range(1, 10)] == [None] + list(range(1, 9))


def test_the_floor_to_work_on_is_the_lowest_one_not_cleared():
    s = mp.subject(SUBJECT)
    assert mm.next_floor(s, set()) == 1 and mm.next_floor(s, {1, 2}) == 3
    assert mm.next_floor(s, {f.number for f in s.main_floors}) is None       # the subject is finished


# ------------------------------------------------------------------ rule 3 (b): the trial, as rules
def test_the_trial_asks_every_micro_skill_of_the_floor_at_its_hardest_tier():
    s = mp.subject(SUBJECT)
    assert mm.trial_skills(s, 1) == FLOOR1_SKILLS
    assert mm.trial_total(s, 1) == len(FLOOR1_SKILLS)
    assert [mm.trial_tier(n) for n in (1, 3, 9)] == [2, 3, 5]


def test_a_trial_asks_each_micro_skill_more_than_once_if_the_config_says_so(monkeypatch):
    monkeypatch.setitem(mp.cfg()["mastery_gate"]["trial"], "questions_per_skill", 2)
    s = mp.subject(SUBJECT)
    assert mm.trial_total(s, 1) == 2 * len(FLOOR1_SKILLS)
    assert mm.trial_skills(s, 1)[:2] == [FLOOR1_SKILLS[0]] * 2        # one micro-skill at a time


def test_a_trial_is_lost_as_soon_as_two_are_missed_and_won_at_the_end():
    assert mm.trial_verdict(asked=3, correct=3, total=6) is None
    assert mm.trial_verdict(asked=3, correct=2, total=6) is None      # one miss is allowed
    assert mm.trial_verdict(asked=3, correct=1, total=6) is False     # two is not
    assert mm.trial_verdict(asked=6, correct=6, total=6) is True
    assert mm.trial_verdict(asked=6, correct=5, total=6) is True
    assert mm.trial_verdict(asked=6, correct=4, total=6) is False


def test_how_many_misses_a_trial_allows_comes_from_the_config(monkeypatch):
    monkeypatch.setitem(mp.cfg()["mastery_gate"]["trial"], "max_wrong", 0)
    assert mm.trial_verdict(asked=1, correct=0, total=6) is False
    assert mm.trial_verdict(asked=6, correct=6, total=6) is True


# ------------------------------------------------------------------ rule 6: spiral review, as rules
def stat(skill="s", floor=1, days_ago=None, streak=0, recent=()):
    now = dt.datetime(2026, 1, 10, 12)
    last = None if days_ago is None else now - dt.timedelta(days=days_ago)
    return mm.ReviewStat(skill_id=skill, floor=floor, last_answered=last, streak=streak, recent=tuple(recent))


NOW = dt.datetime(2026, 1, 10, 12)


def test_the_wait_grows_one_three_seven_fourteen_days_and_stops_there():
    assert [stat(streak=n, recent=[True] * n).wait_days() for n in range(6)] == [1, 1, 3, 7, 14, 14]


def test_a_micro_skill_comes_back_when_its_wait_is_over():
    fresh = stat(days_ago=0.5, streak=1, recent=[True])
    assert not fresh.is_due(NOW) and fresh.due_at().day == 11
    assert stat(days_ago=1.5, streak=1, recent=[True]).is_due(NOW)
    assert not stat(days_ago=1.5, streak=3, recent=[True] * 3).is_due(NOW)       # a 7 day wait
    assert stat(days_ago=8, streak=3, recent=[True] * 3).is_due(NOW)


def test_a_micro_skill_never_answered_is_due_at_once():
    never = stat()
    assert never.is_due(NOW) and never.due_at() is None and never.accuracy == 0.0


def test_a_micro_skill_answered_wrong_is_due_at_once_however_recent():
    missed = stat(days_ago=0, streak=0, recent=[True, True, False])
    assert missed.lapsed and missed.is_due(NOW) and missed.due_at() is None
    assert not stat(days_ago=0, streak=1, recent=[False, True]).lapsed


def test_the_review_queue_takes_the_worst_answered_first_then_the_longest_waiting():
    good_but_old = stat("good", days_ago=40, streak=4, recent=[True] * 5)
    shaky = stat("shaky", days_ago=20, streak=1, recent=[True, False, True, True, True])
    bad = stat("bad", days_ago=3, streak=0, recent=[False] * 5)
    not_due = stat("not_due", days_ago=0.1, streak=2, recent=[True] * 3)
    queue = mm.review_queue([good_but_old, not_due, shaky, bad], NOW)
    assert [s.skill_id for s in queue] == ["bad", "shaky", "good"]


def test_every_fourth_question_of_a_sitting_is_review(monkeypatch):
    asked = review = 0
    picked = []
    for _ in range(12):
        if mm.wants_review(asked, review):
            review += 1
            picked.append(asked + 1)
        asked += 1
    assert picked == [4, 8, 12] and review / asked == 0.25
    cfg = mp.cfg()["spiral_review"]
    assert cfg["share_min"] <= review / asked <= cfg["share_max"]


def test_the_review_share_follows_the_config(monkeypatch):
    monkeypatch.setitem(mp.cfg()["spiral_review"], "share_max", 0.5)
    picked = [n for n, (a, r) in enumerate(((0, 0), (1, 0), (2, 1), (3, 1)), 1) if mm.wants_review(a, r)]
    assert picked == [2, 4]


# ------------------------------------------------------------------ the gate through the API
async def test_the_path_shows_which_floors_are_open_and_how_far_the_gate_has_come(client):
    h, uid = await make(client)
    await meet_gate(uid, 1, skip={FLOOR1_SKILLS[0]})
    floors = (await client.get("/math/path", headers=h)).json()["subjects"][0]
    assert floors["cleared"] == [] and floors["next_floor"] == 1
    first, second = floors["floors"][0], floors["floors"][1]
    assert (first["state"], first["playable"], first["trial_total"]) == ("open", True, len(FLOOR1_SKILLS))
    assert (second["state"], second["playable"], second["gate"]) == ("locked", False, None)
    gate = first["gate"]
    assert not gate["ok"] and gate["weak"] == [FLOOR1_SKILLS[0]]
    done = next(s for s in gate["skills"] if s["skill"] == FLOOR1_SKILLS[1])
    assert (done["tier"], done["top_tier"], done["correct"], done["needed"], done["ok"]) == (2, 2, 5, 4, True)
    missing = next(s for s in gate["skills"] if s["skill"] == FLOOR1_SKILLS[0])
    assert (missing["tier"], missing["at_top"], missing["answered"], missing["ok"]) == (1, False, 0, False)


async def test_a_locked_floor_cannot_be_played(client):
    h, uid = await make(client)
    for path in ("/math/run/start", "/math/trial/start"):
        r = await client.post(path, json={"subject_id": SUBJECT, "floor": 2}, headers=h)
        assert r.status_code == 403 and r.json()["error"]["code"] == "floor_locked", r.text
        assert "tầng 1" in r.json()["error"]["message_vi"]
    await clear_below(uid, 2)
    assert (await client.post("/math/run/start", json={"subject_id": SUBJECT, "floor": 2},
                              headers=h)).status_code == 200


async def test_the_trial_is_refused_until_every_micro_skill_is_through_the_gate(client):
    h, uid = await make(client)
    r = await start_trial(client, h, 1)
    assert r.status_code == 409 and r.json()["error"]["code"] == "gate_not_met", r.text
    await meet_gate(uid, 1, skip={FLOOR1_SKILLS[-1]})
    r = await start_trial(client, h, 1)
    assert r.status_code == 409
    name = mp.subject(SUBJECT).skills[FLOOR1_SKILLS[-1]].name_vi
    assert name in r.json()["error"]["message_vi"]           # which one to go and practise
    await meet_gate(uid, 1)
    r = await start_trial(client, h, 1)
    assert r.status_code == 200 and r.json()["gate"]["ok"], r.text


async def test_a_weak_micro_skill_keeps_the_gate_shut(client):
    h, uid = await make(client)
    await meet_gate(uid, 1, skip={FLOOR1_SKILLS[0]})
    await meet_gate(uid, 1, skip=set(FLOOR1_SKILLS[1:]), weak=True)      # the first one, badly
    r = await start_trial(client, h, 1)
    assert r.status_code == 409 and r.json()["error"]["code"] == "gate_not_met"


# ------------------------------------------------------------------ the trial through the API
async def test_a_trial_asks_each_micro_skill_once_at_the_hardest_tier_and_never_moves_the_tier(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    assert (await run_row(run_id)).mode == "trial"
    played = await play_trial(client, h, run_id)
    assert len(played) == len(FLOOR1_SKILLS)
    assert [p["q"]["math"]["skill"] for p in played] == FLOOR1_SKILLS    # path order, one each
    assert {p["q"]["math"]["tier"] for p in played} == {2}               # the hardest tier of floor 1
    assert {p["res"]["math"]["tier_change"] for p in played} == {0}
    assert not any(p["q"]["math"]["parallel"] or p["q"]["math"]["review"] for p in played)
    first, last = played[0]["res"]["math"]["trial"], played[-1]["res"]["math"]["trial"]
    assert (first["asked"], first["left"], first["passed"]) == (1, len(FLOOR1_SKILLS) - 1, None)
    assert (last["passed"], last["left"], last["unlocked"]) == (True, 0, 2)


async def test_passing_the_trial_clears_the_floor_and_opens_the_next(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    await play_trial(client, h, run_id)
    run = await run_row(run_id)
    assert run.passed is True and run.ended_at is not None and run.asked == len(FLOOR1_SKILLS)
    subject = (await client.get("/math/path", headers=h)).json()["subjects"][0]
    assert subject["cleared"] == [1] and subject["next_floor"] == 2
    assert [f["state"] for f in subject["floors"][:3]] == ["cleared", "open", "locked"]
    assert (await client.post("/math/run/start", json={"subject_id": SUBJECT, "floor": 2},
                              headers=h)).status_code == 200
    assert await math_cleared(uid) == {1}


async def math_cleared(uid, subject=SUBJECT):
    from app.systems import math_practice
    async with dbm.SessionLocal() as db:
        return await math_practice.cleared_floors(db, uid, subject)


async def test_one_miss_still_passes_a_trial(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    played = await play_trial(client, h, run_id, wrong_at={2})
    assert len(played) == len(FLOOR1_SKILLS)
    assert played[-1]["res"]["math"]["trial"]["passed"] is True
    assert (await run_row(run_id)).correct == len(FLOOR1_SKILLS) - 1
    assert await math_cleared(uid) == {1}


async def test_a_failed_trial_ends_at_once_and_can_be_taken_again(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    played = await play_trial(client, h, run_id, wrong_at={1, 2})
    assert len(played) == 2                                   # lost on the second miss, no third question
    trial = played[-1]["res"]["math"]["trial"]
    assert (trial["passed"], trial["unlocked"]) == (False, None)
    run = await run_row(run_id)
    assert run.passed is False and run.ended_at is not None
    assert await math_cleared(uid) == set()
    assert (await client.post("/math/run/next", json={"run_id": run_id}, headers=h)).status_code == 409
    again = await start_trial(client, h, 1)                   # no waiting: straight back in
    assert again.status_code == 200
    assert (await play_trial(client, h, again.json()["run"]["run_id"]))[-1]["res"]["math"]["trial"]["passed"]


async def test_a_trial_queues_no_parallel_questions(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    played = await play_trial(client, h, run_id, wrong_at={1})
    assert not any(p["res"]["math"]["parallel_waiting"] for p in played)
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(MathRetry).where(MathRetry.user_id == uid))).scalars().all() == []


async def test_a_trial_pays_tu_vi_like_any_question(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    run_id = (await start_trial(client, h, 1)).json()["run"]["run_id"]
    played = await play_trial(client, h, run_id)
    assert [p["res"]["xp"]["gained"] for p in played] == [mp.xp_for_tier(2)] * len(FLOOR1_SKILLS)
    assert (await run_row(run_id)).xp_gained == mp.xp_for_tier(2) * len(FLOOR1_SKILLS)


async def test_a_trial_cannot_be_started_on_a_floor_without_questions(client):
    h, uid = await make(client)
    await clear_below(uid, 4)
    r = await start_trial(client, h, 4)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"


async def test_the_trial_of_a_cleared_floor_can_be_taken_again(client):
    h, uid = await make(client)
    await meet_gate(uid, 1)
    await play_trial(client, h, (await start_trial(client, h, 1)).json()["run"]["run_id"])
    assert (await start_trial(client, h, 1)).status_code == 200
    assert await math_cleared(uid) == {1}


# ------------------------------------------------------------------ rule 6 through the API
async def test_a_sitting_on_the_first_floor_never_reviews_anything(client):
    h, uid = await make(client)
    run_id = await start(client, h, 1)
    for _ in range(8):
        q, _ = await play(client, h, run_id, correct=True)
        assert not q["math"]["review"] and q["math"]["floor"] == 1
    assert (await run_row(run_id)).review_asked == 0


async def test_a_sitting_mixes_in_questions_from_the_floor_below(client):
    h, uid = await make(client)
    await clear_below(uid, 2)
    run_id = await start(client, h, 2)
    marks = []
    for _ in range(8):
        q, res = await play(client, h, run_id, correct=True)
        marks.append(q["math"]["review"])
        assert q["math"]["floor"] == (1 if q["math"]["review"] else 2)
        assert res["math"]["review"] == q["math"]["review"]
    assert marks == [False, False, False, True, False, False, False, True]      # every fourth
    run = await run_row(run_id)
    assert (run.review_asked, run.asked) == (2, 8)
    share = run.review_asked / run.asked
    assert mp.cfg()["spiral_review"]["share_min"] <= share <= mp.cfg()["spiral_review"]["share_max"]
    logged = [(a.review, a.floor) for a in await answers_of(uid)]
    assert logged == [(False, 2)] * 3 + [(True, 1)] + [(False, 2)] * 3 + [(True, 1)]


async def test_the_review_question_is_the_micro_skill_that_was_answered_worst(client):
    h, uid = await make(client)
    await clear_below(uid, 2)
    weakest = FLOOR1_SKILLS[2]
    for skill in FLOOR1_SKILLS:
        await log_answers(uid, skill, 1, [True] * 5, floor=1)
    await log_answers(uid, weakest, 1, [False] * 3, floor=1)   # this one has just been missed
    run_id = await start(client, h, 2)
    seen = []
    for _ in range(8):
        q, _ = await play(client, h, run_id, correct=True)
        if q["math"]["review"]:
            seen.append(q["math"]["skill"])
    assert len(seen) == 2 and seen[0] == weakest               # a lapse comes back before anything else
    assert seen[1] != weakest                                  # once it is right again, it waits its turn


async def test_a_review_question_that_is_missed_waits_for_a_sitting_on_its_own_floor(client):
    """A mistake belongs to the floor of the question, not to the sitting (M3's rule)."""
    h, uid = await make(client)
    await clear_below(uid, 2)
    for skill in FLOOR1_SKILLS:
        await log_answers(uid, skill, 1, [True] * 5, floor=1)
    run_id = await start(client, h, 2)
    for _ in range(3):
        q, _ = await play(client, h, run_id, correct=True)     # no mistakes of its own in the way
        assert not q["math"]["review"]
    missed, res = await play(client, h, run_id, correct=False)  # the fourth question: review, missed
    assert missed["math"]["review"] and missed["math"]["floor"] == 1 and res["math"]["parallel_waiting"]
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathRetry.floor, MathRetry.skill_id)
                                 .where(MathRetry.user_id == uid, MathRetry.cleared_at.is_(None))
                                 .order_by(MathRetry.id))).all()
    assert rows == [(1, missed["math"]["skill"])]              # waits on floor 1, where it belongs
    q, _ = await play(client, h, run_id, correct=True)         # the floor-2 sitting goes on as before
    assert not q["math"]["parallel"] and q["math"]["floor"] == 2
    back = await start(client, h, 1)
    q = await ask(client, h, back)
    assert q["math"]["parallel"] and q["math"]["floor"] == 1
    assert q["math"]["skill"] == missed["math"]["skill"]


async def test_a_question_that_is_not_due_yet_is_not_reviewed(client, frozen):
    h, uid = await make(client)
    await clear_below(uid, 2)
    now = frozen.now()
    async with dbm.SessionLocal() as db:                       # every floor-1 micro-skill answered just now
        for n, skill in enumerate(FLOOR1_SKILLS):
            db.add(MathAnswer(user_id=uid, subject_id=SUBJECT, skill_id=skill, floor=1, tier=1,
                              item_id=f"fresh_{n}", qtype="numeric", fingerprint=f"fresh_{n}", correct=True,
                              timed_out=False, review=False, answer_ms=900, answered_at=now))
        await db.commit()
    run_id = await start(client, h, 2)
    for _ in range(8):
        q, _ = await play(client, h, run_id, correct=True)
        assert not q["math"]["review"]                         # all of them wait a day
    assert (await run_row(run_id)).review_asked == 0
    frozen.advance(days=2)
    q = await ask(client, h, run_id)
    assert q["math"]["review"] and q["math"]["floor"] == 1     # the day is over


async def test_a_trial_never_mixes_in_review_questions(client):
    h, uid = await make(client)
    await clear_below(uid, 2)
    await meet_gate(uid, 2)
    run_id = (await start_trial(client, h, 2)).json()["run"]["run_id"]
    played = await play_trial(client, h, run_id)
    assert not any(p["q"]["math"]["review"] for p in played)
    assert {p["q"]["math"]["floor"] for p in played} == {2}
    assert (await run_row(run_id)).review_asked == 0


# ------------------------------------------------------------------ the migration
def test_migration_0012_keeps_the_sittings_and_the_answers(tmp_path):
    """0011 -> 0012 on a database that already has a sitting: it becomes ordinary practice."""
    from alembic import command

    from tests.test_math_loop import _alembic
    path = tmp_path / "m12.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0011")
    con = sqlite3.connect(path)
    cols = {r[1]: r for r in con.execute("pragma table_info(users)")}
    values = {name: ("old" if "CHAR" in col[2].upper() or "TEXT" in col[2].upper() else 0)
              for name, col in cols.items() if col[3] and col[4] is None and not col[5]}
    values.update(id=1, created_at="2026-01-01 00:00:00")
    con.execute(f"insert into users ({', '.join(values)}) values ({', '.join('?' * len(values))})",
                list(values.values()))
    con.execute("insert into math_runs (id, user_id, subject_id, floor, tier, correct_streak, wrong_streak, "
                "combo, best_combo, asked, correct, xp_gained, started_at) "
                "values (1, 1, ?, 1, 1, 0, 0, 2, 2, 3, 2, 11, '2026-01-01')", (SUBJECT,))
    con.execute("insert into math_answers (id, user_id, run_id, subject_id, skill_id, floor, tier, item_id, "
                "qtype, fingerprint, correct, timed_out, answer_ms, answered_at) "
                "values (1, 1, 1, ?, 'tap_hop', 1, 1, 'i1', 'numeric', 'fp', 1, 0, 900, '2026-01-01')",
                (SUBJECT,))
    con.commit()
    con.close()

    command.upgrade(cfg, "0012")
    con = sqlite3.connect(path)
    assert con.execute("select mode, review_asked, passed, asked, correct, xp_gained from math_runs").fetchall() \
        == [("practice", 0, None, 3, 2, 11)]
    assert con.execute("select review, correct, skill_id from math_answers").fetchall() == [(0, 1, "tap_hop")]
    con.close()

    command.downgrade(cfg, "0011")
    con = sqlite3.connect(path)
    assert [r[1] for r in con.execute("pragma table_info(math_runs)")].count("mode") == 0
    assert con.execute("select count(*) from math_answers").fetchone() == (1,)
    con.close()


# ------------------------------------------------------------------ a whole floor, start to finish
async def test_a_floor_from_the_first_question_to_the_trial(client, monkeypatch):
    """The milestone's own promise: a player answers their way up a floor, the gate opens,
    the Thiên kiếp nhỏ is passed, and the next floor is there."""
    items = fake_items(1)
    monkeypatch.setattr(mi, "bank", lambda: items)
    monkeypatch.setattr(mi, "generators", lambda: {})
    h, uid = await make(client)
    run_id = await start(client, h, 1)
    for _ in range(80):                       # answer everything right: tier 1, then tier 2
        await play(client, h, run_id, correct=True)
        gate = (await client.get("/math/path", headers=h)).json()["subjects"][0]["floors"][0]["gate"]
        if gate["ok"]:
            break
    assert gate["ok"], "the gate never opened"
    assert all(s["tier"] == 2 and s["correct"] >= 4 for s in gate["skills"])
    trial = await start_trial(client, h, 1)
    assert trial.status_code == 200, trial.text
    played = await play_trial(client, h, trial.json()["run"]["run_id"])
    assert played[-1]["res"]["math"]["trial"]["passed"] is True
    subject = (await client.get("/math/path", headers=h)).json()["subjects"][0]
    assert subject["cleared"] == [1] and [f["state"] for f in subject["floors"][:2]] == ["cleared", "open"]
