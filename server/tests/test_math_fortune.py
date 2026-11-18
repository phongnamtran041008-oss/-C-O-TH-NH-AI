"""M10: cơ duyên - a chance event that follows right math answers (kế hoạch 4.3).

The rules under test are in app/systems/math_fortune.py and the data contract is the
`_comment` of data/math/fortune.json. Most tests shrink the trigger (threshold, chance, daily
limit) by patching `math_fortune.data`, so an offer comes after two or three answers; the data
itself is checked by `validate()`."""
import copy
import datetime as dt
import random
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app import clock
from app import db as dbm
from app.learning import math_path
from app.learning import quiz
from app.models import AuditLog, MathAnswer, QuizSession, User
from app.systems import items, math_ask, math_combat, math_fortune
from tests.helpers import answer_key, register
from tests.test_math_ask import open_tier_2
from tests.test_math_loop import ask, start
from tests.test_math_skills import right_answer, wrong_answer

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from math_fortune_bot import FortuneBot  # noqa: E402

SUBJECT = "dai_so_tuyen_tinh"


# ------------------------------------------------------------------ helpers
def patch(monkeypatch, **trigger) -> dict:
    """fortune.json with a different trigger (and, through the returned dict, other changes)."""
    d = copy.deepcopy(math_fortune.data())
    d["trigger"].update(trigger)
    monkeypatch.setattr(math_fortune, "data", lambda: d)
    return d


async def state(client, h) -> dict:
    r = await client.get("/math/fortune", headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def practice(client, h, run_id: int, right: bool = True) -> dict:
    """One practice question answered; returns the answer response."""
    q = await ask(client, h, run_id)
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def force(uid: int, event_id: str, accepted: bool = False) -> None:
    """Put an offer of this event in the player's state, the way a roll would."""
    now = clock.now()
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        old = (user.flags or {}).get("math_fortune") or {}
        st = {"date": clock.local_date(now), "offers": 1, "count": 0, "log": old.get("log", []),
              "open": {"event": event_id, "expires_at": (now + dt.timedelta(minutes=10)).isoformat(),
                       "accepted": accepted, "step": 0, "sid": None}}
        user.flags = {**(user.flags or {}), "math_fortune": st}
        await db.commit()


async def accept(client, h) -> dict:
    r = await client.post("/math/fortune/accept", headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def answer(client, h, q: dict, right: bool) -> dict:
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def play_event(client, h, right: list[bool]) -> tuple[list[dict], dict]:
    """Accept, then answer the chain with these right/wrong flags. Returns (questions, last response)."""
    q = (await accept(client, h))["question"]
    asked, res = [], None
    for ok in right:
        asked.append(q)
        res = await answer(client, h, q, ok)
        q = res["fortune"].get("next")
        if q is None:
            break
    return asked, res


async def wallet(uid: int) -> tuple[int, dict]:
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        return user.spirit_stones, dict(await items.stacks(db, uid))


async def hear(uid: int, n: int = 1, context: str = "math", correct: bool = True) -> list[dict]:
    out = []
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for _ in range(n):
            out.append(await math_fortune.on_answer(db, user, SimpleNamespace(context=context), correct, clock.now()))
        await db.commit()
    return out


# ------------------------------------------------------------------ the data
def test_the_data_validates_and_has_both_kinds():
    assert math_fortune.validate() == []
    ev = math_fortune.events()
    assert len(ev) >= 4
    assert {e["kind"] for e in ev.values()} == {"elder", "chest"}
    assert all(e.get("reviewed") is False for e in ev.values())


def test_validate_catches_what_would_break_an_event():
    raw = copy.deepcopy(math_fortune._read())
    raw["events"][0]["rewards"]["rare"]["item"] = "no_such_item"
    raw["events"][1]["question"]["qtypes"] = ["tribulation"]
    raw["events"][2]["question"]["count"] = 0
    raw["events"][3]["rewards"]["stones"] = [9, 3]
    raw["events"][4]["id"] = raw["events"][3]["id"]
    raw["trigger"]["chance"] = 0
    problems = "\n".join(math_fortune.validate(raw))
    for needle in ("lao_nhan_ben_suoi: rewards.rare", "tribulation", "count", "stones", "unique", "trigger.chance"):
        assert needle in problems, needle
    assert math_fortune.validate({**raw, "events": raw["events"][:3]})


def test_the_rare_items_are_real_items():
    from app.systems import catalog
    for e in math_fortune.events().values():
        rare = e["rewards"]["rare"]
        assert catalog.stack_item(rare["item"])["kind"] == "material"


# ------------------------------------------------------------------ when one appears
@pytest.mark.asyncio
async def test_a_right_answer_counts_and_the_threshold_rolls(client, monkeypatch):
    patch(monkeypatch, right_answers=3, chance=1.0)
    h, me = await register(client, "fort_count")
    run = await start(client, h)
    one = await practice(client, h, run)
    two = await practice(client, h, run)
    assert "fortune_offer" not in one["math"] and "fortune_offer" not in two["math"]
    assert (await state(client, h))["progress"] == {"right": 2, "need": 3}
    await practice(client, h, run, right=False)               # a wrong answer counts for nothing
    assert (await state(client, h))["progress"]["right"] == 2
    third = await practice(client, h, run)
    offer = third["math"]["fortune_offer"]
    assert offer["id"] in math_fortune.events() and not offer["accepted"] and 0 < offer["expires_in"] <= 600
    s = await state(client, h)
    assert s["offer"]["id"] == offer["id"] and s["progress"]["right"] == 0     # the counter went back to 0
    assert s["today"] == {"offers": 1, "limit": math_fortune.trigger()["daily_limit"]}


@pytest.mark.asyncio
async def test_the_roll_decides_and_the_counter_resets_either_way(client, monkeypatch):
    patch(monkeypatch, right_answers=2, chance=0.5)
    _, me = await register(client, "fort_roll")
    uid = me["user_id"]
    math_fortune.seed(11)
    seen = []
    for _ in range(40):
        seen.append(bool((await hear(uid, 2))[1]))
        async with dbm.SessionLocal() as db:           # close whatever opened, so the next roll can happen
            user = await db.get(User, uid)
            st = dict(user.flags["math_fortune"])
            st["open"], st["offers"] = None, 0
            user.flags = {**user.flags, "math_fortune": st}
            await db.commit()
    assert 8 <= sum(seen) <= 32 and not all(seen)       # about half the thresholds offered something
    # the same seed rolls the same way
    math_fortune.seed(11)
    again = []
    for _ in range(40):
        again.append(bool((await hear(uid, 2))[1]))
        async with dbm.SessionLocal() as db:
            user = await db.get(User, uid)
            st = dict(user.flags["math_fortune"])
            st["open"], st["offers"] = None, 0
            user.flags = {**user.flags, "math_fortune": st}
            await db.commit()
    assert again == seen


@pytest.mark.asyncio
async def test_events_are_chosen_by_weight(client, monkeypatch):
    patch(monkeypatch, right_answers=1, chance=1.0, daily_limit=10 ** 6)
    _, me = await register(client, "fort_weight")
    uid = me["user_id"]
    math_fortune.seed(5)
    counts: dict[str, int] = {}
    for _ in range(400):
        out = (await hear(uid))[0]
        counts[out["fortune_offer"]["id"]] = counts.get(out["fortune_offer"]["id"], 0) + 1
        async with dbm.SessionLocal() as db:
            user = await db.get(User, uid)
            st = dict(user.flags["math_fortune"])
            st["open"] = None
            user.flags = {**user.flags, "math_fortune": st}
            await db.commit()
    ev = math_fortune.events()
    assert set(counts) == set(ev)
    heaviest = max(ev.values(), key=lambda e: e["weight"])["id"]
    lightest = min(ev.values(), key=lambda e: e["weight"])["id"]
    assert counts[heaviest] > counts[lightest] * 2


@pytest.mark.asyncio
async def test_only_one_offer_is_open_and_it_stops_the_counter(client, monkeypatch):
    patch(monkeypatch, right_answers=2, chance=1.0)
    h, me = await register(client, "fort_one")
    uid = me["user_id"]
    outs = await hear(uid, 2)
    assert outs[1]["fortune_offer"]
    first = (await state(client, h))["offer"]["id"]
    assert all(o == {} for o in await hear(uid, 6))     # more right answers: no second offer ...
    s = await state(client, h)
    assert s["offer"]["id"] == first and s["today"]["offers"] == 1
    assert s["progress"]["right"] == 0                  # ... and nothing was saved up for later


@pytest.mark.asyncio
async def test_the_daily_limit_holds_and_the_next_day_starts_again(client, frozen, monkeypatch):
    patch(monkeypatch, right_answers=1, chance=1.0, daily_limit=2)
    h, me = await register(client, "fort_day")
    uid = me["user_id"]

    async def close():
        r = await client.post("/math/fortune/decline", headers=h)
        assert r.status_code == 200
    got = []
    for _ in range(5):
        got.append(bool((await hear(uid))[0]))
        if got[-1]:
            await close()
    assert got == [True, True, False, False, False]
    s = await state(client, h)
    assert s["today"] == {"offers": 2, "limit": 2} and s["offer"] is None
    frozen.advance(hours=1)                              # 16:00 in Việt Nam: still the same day
    assert not (await hear(uid))[0]
    frozen.advance(hours=9)                              # 01:00 the next day
    assert (await state(client, h))["today"]["offers"] == 0
    assert (await hear(uid))[0]["fortune_offer"]


@pytest.mark.asyncio
async def test_an_offer_expires_and_a_taken_one_has_a_play_window(client, frozen, monkeypatch):
    patch(monkeypatch, right_answers=1, chance=1.0, expires_seconds=300, play_seconds=120)
    h, me = await register(client, "fort_expire")
    uid = me["user_id"]
    await hear(uid)
    frozen.advance(seconds=200)
    s = await state(client, h)
    assert s["offer"] and 90 <= s["offer"]["expires_in"] <= 100
    frozen.advance(seconds=200)                          # nobody took it
    s = await state(client, h)
    assert s["offer"] is None and s["log"][0]["outcome"] == "expired"
    r = await client.post("/math/fortune/accept", headers=h)
    assert r.status_code == 404
    # a taken one: too slow for the whole chain -> the right answer comes too late and pays nothing
    await force(uid, "ruong_go_cu")
    stones, _ = await wallet(uid)
    patch(monkeypatch, play_seconds=12)
    q = (await accept(client, h))["question"]
    assert q["time_limit"] > 8
    frozen.advance(seconds=6)
    res = await answer(client, h, q, True)
    assert res["fortune"]["progress"] == [1, 2] and not res["fortune"]["done"]
    frozen.advance(seconds=6.5)                          # 12.5 s after accepting: the 12 s window is over
    res = await answer(client, h, res["fortune"]["next"], True)
    assert res["fortune"]["done"] and not res["fortune"]["won"] and res["fortune"]["rewards"] is None
    assert (await wallet(uid))[0] == stones
    assert (await state(client, h))["log"][0]["outcome"] == "lost"


# ------------------------------------------------------------------ accept / decline
@pytest.mark.asyncio
async def test_decline_takes_the_offer_away_and_costs_nothing(client):
    h, me = await register(client, "fort_decline")
    uid = me["user_id"]
    assert (await client.post("/math/fortune/accept", headers=h)).status_code == 404
    await force(uid, "lao_nhan_ben_suoi")
    before = await wallet(uid)
    r = await client.post("/math/fortune/decline", headers=h)
    assert r.status_code == 200 and r.json()["offer"] is None
    assert r.json()["log"][0]["outcome"] == "declined"
    assert await wallet(uid) == before
    assert (await client.post("/math/fortune/accept", headers=h)).status_code == 404
    await force(uid, "ruong_go_cu", accepted=True)
    assert (await client.post("/math/fortune/decline", headers=h)).status_code == 409   # too late to decline


@pytest.mark.asyncio
async def test_accepting_twice_gives_the_same_question_back(client):
    h, me = await register(client, "fort_twice")
    await force(me["user_id"], "ruong_go_cu")
    a = await accept(client, h)
    b = await accept(client, h)
    assert a["question"]["session_id"] == b["question"]["session_id"]
    assert a["question"]["context"] == "math_fortune" and a["fortune"]["accepted"] is True


# ------------------------------------------------------------------ what is asked
@pytest.mark.asyncio
async def test_an_elder_asks_the_hardest_question_the_player_may_get(client):
    h, me = await register(client, "fort_elder")
    uid = me["user_id"]
    ev = math_fortune.events()["lao_nhan_ben_suoi"]
    from app.systems import math_practice
    skill = next(t.skill for t in math_practice._templates(SUBJECT, 1)
                 if t.qtype in ev["question"]["qtypes"] and t.tier == 2)
    await open_tier_2(uid, skill, 1)
    for n in range(5):
        await force(uid, ev["id"])
        q = (await accept(client, h))["question"]
        meta = q["math"]
        assert (meta["skill"], meta["tier"]) == (skill, 2), n
        assert q["qtype"] in ev["question"]["qtypes"]
        res = await answer(client, h, q, True)
        assert res["fortune"]["done"] and res["fortune"]["won"]
        assert res["fortune"]["progress"] == [1, 1]


@pytest.mark.asyncio
async def test_a_chest_asks_every_stated_question_and_all_must_be_right(client):
    h, me = await register(client, "fort_chest")
    uid = me["user_id"]
    ev = math_fortune.events()["ruong_ngoc_boi"]
    n = ev["question"]["count"]
    assert n >= 2
    # all right: n questions of the stated types, then the reward
    await force(uid, ev["id"])
    asked, res = await play_event(client, h, [True] * n)
    assert len(asked) == n and [a["context"] for a in asked] == ["math_fortune"] * n
    assert all(a["qtype"] in ev["question"]["qtypes"] for a in asked)
    assert res["fortune"]["done"] and res["fortune"]["won"] and res["fortune"]["rewards"]["spirit_stones"] > 0
    assert len({a["session_id"] for a in asked}) == n
    # one wrong in the middle ends it at once
    for wrong_at in range(n):
        await force(uid, ev["id"])
        stones, bag = await wallet(uid)
        asked, res = await play_event(client, h, [i != wrong_at for i in range(n)])
        assert len(asked) == wrong_at + 1
        f = res["fortune"]
        assert f["done"] and not f["won"] and f["rewards"] is None and f["text_vi"] == ev["lose_vi"]
        assert await wallet(uid) == (stones, bag)
        assert (await state(client, h))["offer"] is None


@pytest.mark.asyncio
async def test_a_timeout_is_a_wrong_answer_and_nothing_else_is_lost(client, frozen):
    h, me = await register(client, "fort_timeout")
    uid = me["user_id"]
    await force(uid, "lao_nhan_ben_suoi")
    before = await wallet(uid)
    q = (await accept(client, h))["question"]
    frozen.advance(seconds=q["time_limit"] + 60)
    key = await answer_key(q["session_id"])
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                          headers=h)
    res = r.json()
    assert res["timed_out"] and not res["correct"]
    assert res["fortune"]["done"] and not res["fortune"]["won"]
    assert await wallet(uid) == before


@pytest.mark.asyncio
async def test_the_tier_is_never_above_the_players_and_answers_are_logged(client):
    h, me = await register(client, "fort_log")
    uid = me["user_id"]
    for event_id in ("ruong_sat_tho", "lao_nhan_dai_lo"):
        await force(uid, event_id)
        asked, _ = await play_event(client, h, [True, True, True])
        async with dbm.SessionLocal() as db:
            for q in asked:
                m = q["math"]
                assert m["floor"] == 1                   # the player's own floor
                assert m["tier"] <= await math_combat.tier_for(db, uid, m["skill"], m["floor"])
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
    assert len(rows) >= 4 and all(r.run_id is None and r.floor == 1 for r in rows)
    assert all(r.tier == 1 for r in rows)                # a fresh player never saw tier 2


@pytest.mark.asyncio
async def test_fortune_answers_do_not_feed_the_counter(client, monkeypatch):
    patch(monkeypatch, right_answers=3, chance=1.0)
    h, me = await register(client, "fort_nofeed")
    uid = me["user_id"]
    run = await start(client, h)
    await practice(client, h, run)
    await force(uid, "ruong_sat_tho")                    # (replaces the state: counter 0)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        st = dict(user.flags["math_fortune"])
        st["count"] = 1
        user.flags = {**user.flags, "math_fortune": st}
        await db.commit()
    await play_event(client, h, [True, True, True])
    assert (await state(client, h))["progress"]["right"] == 1
    # the same answers do count when the context is anything else
    assert (await hear(uid, 1, context="math_combat"))[0] == {}
    assert (await state(client, h))["progress"]["right"] == 2
    assert (await hear(uid, 1, context="math_fortune"))[0] == {}
    assert (await hear(uid, 1, correct=False))[0] == {}
    assert (await state(client, h))["progress"]["right"] == 2


@pytest.mark.asyncio
async def test_field_answers_feed_the_counter_too(client, monkeypatch):
    """The monster / chiêu / mode answers go through math_combat.record: the hook is there."""
    patch(monkeypatch, right_answers=2, chance=1.0)
    h, me = await register(client, "fort_field")
    uid = me["user_id"]
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        outs = []
        for _ in range(2):
            q = await math_ask.pick_own(db, user, rng=random.Random(1))
            s = await quiz.create_session(db, user, "math_combat", q)
            row = await db.get(QuizSession, s["session_id"])
            outs.append(await math_combat.record(db, user, row, True, clock.now()))
        await db.commit()
    assert "fortune_offer" not in outs[0] and outs[1]["fortune_offer"]["id"] in math_fortune.events()


# ------------------------------------------------------------------ the rewards
@pytest.mark.asyncio
async def test_rewards_really_land_in_the_inventory(client, monkeypatch):
    d = patch(monkeypatch)
    ev = d["events"][0]
    ev["rewards"]["rare"]["chance"] = 1.0               # the rare one is certain, so it can be checked
    h, me = await register(client, "fort_reward")
    uid = me["user_id"]
    await force(uid, ev["id"])
    stones0, bag0 = await wallet(uid)
    math_fortune.seed(2)
    _, res = await play_event(client, h, [True] * ev["question"]["count"])
    f = res["fortune"]
    assert f["won"] and f["text_vi"] == ev["win_vi"]
    lo, hi = ev["rewards"]["stones"]
    got = f["rewards"]
    assert lo <= got["spirit_stones"] <= hi
    assert [(i["item"], i["qty"], i["rare"]) for i in got["items"]] == \
        [(i["item"], i["qty"], False) for i in ev["rewards"]["items"]] + \
        [(ev["rewards"]["rare"]["item"], ev["rewards"]["rare"]["qty"], True)]
    assert all(i["name_vi"] for i in got["items"])
    stones1, bag1 = await wallet(uid)
    assert stones1 - stones0 >= got["spirit_stones"]      # (the Tu Vi path pays nothing in stones)
    for i in got["items"]:
        assert bag1.get(i["item"], 0) - bag0.get(i["item"], 0) == i["qty"]
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(AuditLog).where(AuditLog.user_id == uid, AuditLog.reason == "math_fortune"))).scalars().all()
    assert len(rows) == 1 + len(got["items"])
    log = (await state(client, h))["log"]
    assert log[0]["outcome"] == "won" and log[0]["rewards"]["spirit_stones"] == got["spirit_stones"]


@pytest.mark.asyncio
async def test_no_rare_item_when_the_chance_does_not_fall(client, monkeypatch):
    d = patch(monkeypatch)
    ev = d["events"][0]
    ev["rewards"]["rare"]["chance"] = 1e-9
    h, me = await register(client, "fort_norare")
    await force(me["user_id"], ev["id"])
    _, res = await play_event(client, h, [True])
    assert not any(i["rare"] for i in res["fortune"]["rewards"]["items"])


@pytest.mark.asyncio
async def test_the_log_stays_small(client, monkeypatch):
    patch(monkeypatch, log_size=3)
    h, me = await register(client, "fort_logsize")
    for _ in range(6):
        await force(me["user_id"], "ruong_go_cu")
        await client.post("/math/fortune/decline", headers=h)
    assert len((await state(client, h))["log"]) == 3


# ------------------------------------------------------------------ the bot
@pytest.mark.asyncio
@pytest.mark.parametrize("seed", range(20))
async def test_the_bot_plays_cleanly_and_keeps_the_daily_limit(client, frozen, monkeypatch, seed):
    patch(monkeypatch, right_answers=3, chance=0.8, daily_limit=2)
    math_fortune.seed(seed)
    h, me = await register(client, f"fort_bot{seed}")
    uid = me["user_id"]
    stones0, bag0 = await wallet(uid)
    events = math_fortune.events()
    total = {"stones": 0, "items": {}}
    for day in range(2):
        bot = FortuneBot(client, h, seed=seed * 10 + day, wrong_rate=0.3, decline_rate=0.2)
        out = await bot.play()
        assert out["offers"] == 2, out                          # the limit, exactly
        assert out["won"] + out["lost"] + out["declined"] == out["offers"]
        s = await state(client, h)
        assert s["today"] == {"offers": 2, "limit": 2} and s["offer"] is None
        for e in out["events"]:                                  # what was paid matches the data
            data = events[e["event"]]
            if e["won"]:
                lo, hi = data["rewards"]["stones"]
                assert lo <= e["rewards"]["spirit_stones"] <= hi
                paid = {i["item"]: i["qty"] for i in e["rewards"]["items"] if not i["rare"]}
                assert paid == {i["item"]: i["qty"] for i in data["rewards"]["items"]}
                assert all(i["item"] == data["rewards"]["rare"]["item"] for i in e["rewards"]["items"] if i["rare"])
            else:
                assert e["rewards"] is None
        total["stones"] += out["stones"]
        for k, v in out["items"].items():
            total["items"][k] = total["items"].get(k, 0) + v
        # the limit holds: more right answers today bring no offer
        run = await start(client, h)
        for _ in range(4):
            assert "fortune_offer" not in (await practice(client, h, run))["math"]
        frozen.advance(hours=24)
    stones1, bag1 = await wallet(uid)
    assert stones1 - stones0 == total["stones"]
    for k, v in total["items"].items():
        assert bag1.get(k, 0) - bag0.get(k, 0) == v
