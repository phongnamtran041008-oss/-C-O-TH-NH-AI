"""M2: one math question loop - open a question, the countdown, grading, the adaptive tier
(learning-path rules 2 and 3), Tu Vi by tier, and what is written to the database."""
import datetime as dt
import random
import sqlite3

import pytest
from sqlalchemy import func, select

from app import db as dbm
from app.config import settings
from app.learning import math_adaptive as ma
from app.learning import math_items as mi
from app.learning import math_path as mp
from app.learning import selection
from app.models import Character, MathAnswer, MathRun, QuizSession
from app.systems import math_practice
from tests.helpers import answer_key, register
from tests.test_combat import LOOK

SUBJECT = "dai_so_tuyen_tinh"


# ------------------------------------------------------------------ helpers
async def make(client, name="toan_1"):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " "), "appearance": LOOK},
                          headers=h)
    assert r.status_code == 200, r.text
    return h, data["user_id"]


async def start(client, h, floor=1, subject=SUBJECT) -> int:
    r = await client.post("/math/run/start", json={"subject_id": subject, "floor": floor}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["run"]["run_id"]


async def ask(client, h, run_id) -> dict:
    r = await client.post("/math/run/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["question"]


def right_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "true_false":
        return {"value": key["value"]}
    if q["qtype"] == "multiple_choice":
        return {"option": key["option"]}
    return {"text": ", ".join(key["numbers"])}


def wrong_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "true_false":
        return {"value": not key["value"]}
    if q["qtype"] == "multiple_choice":
        return {"option": next(o["id"] for o in q["options"] if o["id"] != key["option"])}
    return {"text": "987654"}


async def play(client, h, run_id, correct=True) -> tuple[dict, dict]:
    """Ask the next question of the run and answer it. Returns (question, result)."""
    q = await ask(client, h, run_id)
    key = await answer_key(q["session_id"])
    answer = right_answer(q, key) if correct else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
    assert r.status_code == 200, r.text
    return q, r.json()


def fake_items(floor: int, per_tier: int = 3) -> dict[str, mi.MathItem]:
    """Numeric items for every micro-skill and tier of a floor that has no questions yet."""
    out = {}
    f = mp.subject(SUBJECT).floor(floor)
    for k, skill in enumerate(f.skills):
        for tier in f.tiers:
            for n in range(per_tier):
                iid = f"fake_{floor}_{k}_{tier}_{n}"
                out[iid] = mi.MathItem(id=iid, subject=SUBJECT, skill=skill.id, floor=floor, tier=tier,
                                       qtype="numeric", prompt_vi=f"Tính {n} + {tier}.", answer=str(n + tier),
                                       solution_vi=(f"{n} + {tier} = {n + tier}.",), reviewed=True)
    return out


@pytest.fixture
def floor3(monkeypatch):
    """Floor 3 (tiers 2-3) with questions, so the tier has room to move both ways."""
    items = fake_items(3)
    monkeypatch.setattr(mi, "bank", lambda: items)
    return items


async def log_answers(uid, skill, tier, results, floor=3):
    async with dbm.SessionLocal() as db:
        for n, ok in enumerate(results):
            db.add(MathAnswer(user_id=uid, subject_id=SUBJECT, skill_id=skill, floor=floor, tier=tier,
                              item_id=f"old_{n}", qtype="numeric", fingerprint=f"old_{skill}_{tier}_{n}",
                              correct=ok, timed_out=False, answer_ms=1000,
                              answered_at=dt.datetime(2025, 12, 1) + dt.timedelta(minutes=n)))
        await db.commit()


# ------------------------------------------------------------------ rule 2: the tier inside a sitting
def test_two_right_in_a_row_raise_the_tier_and_two_wrong_lower_it():
    s = ma.start(3)
    assert s == ma.TierState(2)
    s = ma.after_answer(s, True, 3)
    assert (s.tier, s.correct_streak) == (2, 1)
    s = ma.after_answer(s, True, 3)
    assert s == ma.TierState(3)                       # up, and the streak is used up
    s = ma.after_answer(s, False, 3)
    assert (s.tier, s.wrong_streak) == (3, 1)
    s = ma.after_answer(s, False, 3)
    assert s == ma.TierState(2)


def test_a_wrong_answer_breaks_the_right_streak_and_the_other_way_round():
    s = ma.after_answer(ma.start(3), True, 3)
    s = ma.after_answer(s, False, 3)
    assert (s.tier, s.correct_streak, s.wrong_streak) == (2, 0, 1)
    s = ma.after_answer(s, True, 3)
    assert (s.tier, s.correct_streak, s.wrong_streak) == (2, 1, 0)
    s = ma.after_answer(s, True, 3)
    assert s.tier == 3


@pytest.mark.parametrize("floor", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_the_tier_never_leaves_the_range_of_the_floor(floor):
    lo, hi = mp.floor_tiers(floor)
    rng = random.Random(floor)
    s = ma.start(floor)
    assert s.tier == lo
    for _ in range(300):
        s = ma.after_answer(s, rng.random() < 0.5, floor)
        assert lo <= s.tier <= hi
    for _ in range(10):
        s = ma.after_answer(s, False, floor)
    assert s.tier == lo                               # never below the floor's minimum
    for _ in range(10):
        s = ma.after_answer(s, True, floor)
    assert s.tier == hi


def test_no_tier_1_question_from_floor_3_on():
    for floor in range(3, 11):
        s = ma.start(floor)
        for _ in range(20):
            s = ma.after_answer(s, False, floor)
            assert s.tier >= 2
            assert ma.question_tier(s.tier, floor, {}) >= 2


def test_the_streak_lengths_come_from_the_config():
    cfg = {**mp.cfg(), "adaptive": {"up_after_correct_streak": 3, "down_after_wrong_streak": 1}}
    s = ma.start(3, cfg)
    for _ in range(2):
        s = ma.after_answer(s, True, 3, cfg)
    assert s.tier == 2
    s = ma.after_answer(s, True, 3, cfg)
    assert s.tier == 3
    assert ma.after_answer(s, False, 3, cfg).tier == 2


# ------------------------------------------------------------------ rule 3: a tier opens per micro-skill
def test_a_tier_opens_after_three_recent_right_answers_one_tier_below():
    assert ma.open_tier(3, {}) == 2                                   # the floor's lowest tier is always open
    assert ma.open_tier(3, {2: [True, True]}) == 2
    assert ma.open_tier(3, {2: [True, True, True]}) == 3
    assert ma.open_tier(3, {2: [True, False, True, False, True]}) == 3
    assert ma.open_tier(3, {2: [True, True, True, False, False, False]}) == 2     # only the last 5 count
    assert ma.open_tier(3, {2: [False, False, False, True, True, True]}) == 3
    assert ma.open_tier(3, {3: [True] * 5}) == 2                      # tier 3 answers do not open tier 3
    assert ma.open_tier(9, {}) == 5 and ma.open_tier(10, {}) == 5     # one-tier floors


def test_the_question_tier_is_the_lower_of_the_sitting_and_what_is_open():
    opened = {2: [True, True, True]}
    assert ma.question_tier(3, 3, {}) == 2            # the sitting is at 3 but the skill has not opened it
    assert ma.question_tier(3, 3, opened) == 3
    assert ma.question_tier(2, 3, opened) == 2        # open, but the sitting is lower
    assert ma.question_tier(1, 3, opened) == 2        # never below the floor


# ------------------------------------------------------------------ choosing the item
def test_choose_item_respects_the_tier_and_skips_what_was_just_asked():
    items = list(fake_items(3).values())
    rng = random.Random(1)
    for _ in range(50):
        assert math_practice.choose_item(items, 3, 3, {}, [], rng).tier == 2
    skill = mp.subject(SUBJECT).floor(3).skills[0].id
    opened = {skill: {2: [True, True, True]}}
    picks = [math_practice.choose_item(items, 3, 3, opened, [], rng) for _ in range(200)]
    assert {p.tier for p in picks if p.skill == skill} == {3}
    assert {p.tier for p in picks if p.skill != skill} == {2}

    tier2 = [i for i in items if i.tier == 2]
    recent = [i.fingerprint for i in tier2[1:]]
    for _ in range(30):                               # one fresh item left: it is always the one
        assert math_practice.choose_item(items, 2, 3, {}, recent, rng) is tier2[0]
    recent = [i.fingerprint for i in tier2]           # everything seen: the one seen longest ago
    assert math_practice.choose_item(items, 2, 3, {}, recent, rng) is tier2[-1]


def test_choose_item_falls_back_when_a_skill_has_no_item_at_the_wanted_tier():
    items = [i for i in fake_items(3).values() if i.tier == 3]            # tier 3 only
    with pytest.raises(math_practice.MathError):                          # ...and tier 3 is not open yet
        math_practice.choose_item(items, 2, 3, {}, [], random.Random(1))
    skill = items[0].skill
    pick = math_practice.choose_item(items, 2, 3, {skill: {2: [True] * 3}}, [], random.Random(1))
    assert pick.skill == skill and pick.tier == 3


# ------------------------------------------------------------------ the loop through the API
async def test_path_lists_the_floors_and_which_have_questions(client):
    h, _ = await make(client)
    r = await client.get("/math/path", headers=h)
    assert r.status_code == 200
    data = r.json()
    assert [s["id"] for s in data["subjects"]] == [SUBJECT]
    floors = data["subjects"][0]["floors"]
    assert [f["floor"] for f in floors] == list(range(1, 11))
    assert floors[0]["playable"] and floors[0]["questions"] == len(mi.floor_items(SUBJECT, 1, True))
    assert (floors[0]["tier_min"], floors[0]["tier_max"]) == (1, 2)
    assert not floors[1]["playable"] and floors[9]["hidden"]
    assert data["run"] is None and data["tiers"]["1"] == "Nhập môn"


async def test_start_refuses_a_floor_without_questions_or_that_does_not_exist(client):
    h, _ = await make(client)
    for body, status, code in (({"subject_id": SUBJECT, "floor": 2}, 400, "no_questions"),
                               ({"subject_id": SUBJECT, "floor": 11}, 404, "no_floor"),
                               ({"subject_id": "giai_tich", "floor": 1}, 404, "no_floor")):
        r = await client.post("/math/run/start", json=body, headers=h)
        assert r.status_code == status and r.json()["error"]["code"] == code, r.text
    assert (await client.post("/math/run/start", json={"subject_id": SUBJECT, "floor": 1})).status_code == 401


async def test_a_question_opens_with_its_countdown_and_without_its_answer(client, frozen):
    h, _ = await make(client)
    run_id = await start(client, h)
    q = await ask(client, h, run_id)
    assert q["context"] == "math" and q["qtype"] in mi.PLAYABLE_TYPES
    assert q["math"]["floor"] == 1 and q["math"]["tier"] == 1 and q["math"]["tier_name_vi"] == "Nhập môn"
    assert q["prompt"]["text"] and q["instruction_vi"]
    assert q["time_limit"] == mp.time_limit(q["qtype"], 1)
    assert "answer_key" not in q and "reveal" not in q and "solution_vi" not in str(q)
    opened = dt.datetime.fromisoformat(q["server_time"].rstrip("Z"))
    expires = dt.datetime.fromisoformat(q["expires_at"].rstrip("Z"))
    assert (expires - opened).total_seconds() == pytest.approx(q["time_limit"] + 1.5)      # + network grace
    again = await ask(client, h, run_id)
    assert again["session_id"] == q["session_id"]         # the open question, not a second one


async def test_a_right_answer_pays_tu_vi_by_tier_and_is_written_down(client):
    h, uid = await make(client)
    run_id = await start(client, h)
    q, res = await play(client, h, run_id, correct=True)
    assert res["correct"] and not res["timed_out"]
    assert res["xp"]["gained"] == mp.xp_for_tier(1) == 3
    assert res["reveal"]["solution_vi"] and res["reveal"]["answer_text"]
    m = res["math"]
    assert m["tier"] == 1 and m["xp_base"] == 3 and m["tier_change"] == 0
    assert (m["run"]["asked"], m["run"]["correct"], m["run"]["combo"], m["run"]["xp_gained"]) == (1, 1, 1, 0)
    async with dbm.SessionLocal() as db:
        row = (await db.execute(select(MathAnswer))).scalar_one()
        assert (row.user_id, row.run_id, row.subject_id, row.floor, row.tier) == (uid, run_id, SUBJECT, 1, 1)
        assert row.skill_id == q["math"]["skill"] and row.correct and not row.timed_out
        assert row.fingerprint == mi.bank()[row.item_id].fingerprint and row.qtype == q["qtype"]
        s = await db.get(QuizSession, q["session_id"])
        assert s.item_id == row.item_id and s.context == "math" and s.qtype == q["qtype"] and s.correct
        run = await db.get(MathRun, run_id)
        assert (run.asked, run.correct, run.combo, run.xp_gained) == (1, 1, 1, 3)
        assert (await db.get(Character, uid)).cultivation_xp == 3
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": {}}, headers=h)
    assert r.status_code == 409                           # one answer per question


async def test_a_wrong_answer_shows_the_solution_and_pays_nothing(client):
    h, uid = await make(client)
    run_id = await start(client, h)
    q, res = await play(client, h, run_id, correct=False)
    assert not res["correct"] and not res["timed_out"] and "xp" not in res
    assert res["reveal"]["solution_vi"] == list(mi.bank()[(await item_of(q))].solution_vi)
    assert res["math"]["xp_base"] == 0 and res["math"]["run"]["combo"] == 0
    async with dbm.SessionLocal() as db:
        assert (await db.get(Character, uid)).cultivation_xp == 0
        assert not (await db.execute(select(MathAnswer))).scalar_one().correct


async def item_of(q: dict) -> str:
    async with dbm.SessionLocal() as db:
        return (await db.get(QuizSession, q["session_id"])).item_id


async def test_running_out_of_time_is_a_wrong_answer_and_ends_the_combo(client, frozen):
    h, uid = await make(client)
    run_id = await start(client, h)
    for _ in range(2):
        await play(client, h, run_id, correct=True)
    q = await ask(client, h, run_id)
    key = await answer_key(q["session_id"])
    frozen.advance(seconds=q["time_limit"] + 2)           # past the limit and the network grace
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                          headers=h)
    res = r.json()
    assert r.status_code == 200 and not res["correct"] and res["timed_out"] and "xp" not in res
    run = res["math"]["run"]
    assert (run["combo"], run["best_combo"], run["asked"], run["correct"]) == (0, 2, 3, 2)
    async with dbm.SessionLocal() as db:
        last = (await db.execute(select(MathAnswer).order_by(MathAnswer.id.desc()))).scalars().first()
        assert last.timed_out and not last.correct
        assert (await db.get(Character, uid)).cultivation_xp == 2 * mp.xp_for_tier(1)     # nothing else is lost
    nxt = await ask(client, h, run_id)
    assert nxt["session_id"] != q["session_id"]


async def test_a_countdown_that_ran_out_on_the_client_is_logged_as_a_timeout(client):
    h, _ = await make(client)
    run_id = await start(client, h)
    await play(client, h, run_id, correct=True)
    q = await ask(client, h, run_id)              # the server's own clock still has its network grace
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": {"timed_out": True}},
                          headers=h)
    res = r.json()
    assert r.status_code == 200 and not res["correct"] and res["math"]["timed_out"] and "xp" not in res
    assert res["math"]["run"]["combo"] == 0
    async with dbm.SessionLocal() as db:
        last = (await db.execute(select(MathAnswer).order_by(MathAnswer.id.desc()))).scalars().first()
        assert last.timed_out and not last.correct


async def test_an_expired_question_is_replaced_by_a_new_one(client, frozen):
    h, _ = await make(client)
    run_id = await start(client, h)
    q = await ask(client, h, run_id)
    frozen.advance(seconds=q["time_limit"] + 5)
    assert (await ask(client, h, run_id))["session_id"] != q["session_id"]


async def test_the_sitting_tier_moves_with_streaks_through_the_api(client, floor3):
    h, _ = await make(client)
    run_id = await start(client, h, floor=3)
    changes = []
    for ok in (True, True, False, False, False, False, True, True, True, True):
        q, res = await play(client, h, run_id, correct=ok)
        assert q["math"]["tier"] in (2, 3)
        changes.append((res["math"]["tier_change"], res["math"]["run"]["tier"]))
    assert changes == [(0, 2), (1, 3), (0, 3), (-1, 2), (0, 2), (0, 2),      # floor 3 never goes below tier 2
                       (0, 2), (1, 3), (0, 3), (0, 3)]                       # ...nor above tier 3


async def test_a_higher_tier_question_needs_three_right_answers_one_tier_below(client, floor3):
    h, uid = await make(client)
    skills = [s.id for s in mp.subject(SUBJECT).floor(3).skills]
    await log_answers(uid, skills[0], 2, [True, True, True])
    await log_answers(uid, skills[1], 2, [True, True, False, False, False])
    run_id = await start(client, h, floor=3)
    async with dbm.SessionLocal() as db:                  # a sitting that has reached tier 3
        (await db.get(MathRun, run_id)).tier = 3
        await db.commit()
    seen = {}
    for _ in range(40):
        q, _ = await play(client, h, run_id, correct=False)
        async with dbm.SessionLocal() as db:
            (await db.get(MathRun, run_id)).tier = 3
            await db.commit()
        seen.setdefault(q["math"]["skill"], set()).add(q["math"]["tier"])
    assert seen[skills[0]] == {3}                         # opened by its three right answers
    assert all(tiers == {2} for skill, tiers in seen.items() if skill != skills[0])
    assert len(seen) == len(skills)


async def test_tu_vi_grows_with_the_tier(client, floor3):
    h, uid = await make(client)
    skills = [s.id for s in mp.subject(SUBJECT).floor(3).skills]
    for skill in skills:
        await log_answers(uid, skill, 2, [True, True, True])
    run_id = await start(client, h, floor=3)
    gains = {}
    for _ in range(4):
        q, res = await play(client, h, run_id, correct=True)
        gains[q["math"]["tier"]] = res["xp"]["gained"]
    assert gains == {2: 5, 3: 8} == {t: mp.xp_for_tier(t) for t in (2, 3)}
    async with dbm.SessionLocal() as db:
        assert (await db.get(MathRun, run_id)).xp_gained == 5 + 5 + 8 + 8


async def test_no_question_repeats_while_a_fresh_one_is_left(client):
    h, _ = await make(client)
    run_id = await start(client, h)
    tier1 = {i.id for i in mi.floor_items(SUBJECT, 1, True) if i.tier == 1}
    asked = []
    for _ in range(len(tier1)):                           # all wrong: tier 2 never opens
        q, _ = await play(client, h, run_id, correct=False)
        asked.append(await item_of(q))
    assert set(asked) == tier1 and len(asked) == len(tier1)
    q, _ = await play(client, h, run_id, correct=False)
    assert await item_of(q) == asked[0]                   # all seen: the oldest comes back first


async def test_ending_a_sitting_and_starting_another(client):
    h, uid = await make(client)
    first = await start(client, h)
    await play(client, h, first)
    second = await start(client, h)                       # one sitting at a time
    assert second != first
    r = await client.post("/math/run/next", json={"run_id": first}, headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "run_ended"
    assert (await client.get("/math/path", headers=h)).json()["run"]["run_id"] == second
    r = await client.post("/math/run/end", json={"run_id": second}, headers=h)
    assert r.status_code == 200 and r.json()["run"]["ended"]
    assert (await client.get("/math/path", headers=h)).json()["run"] is None
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(func.count()).select_from(MathRun).where(
            MathRun.user_id == uid, MathRun.ended_at.is_(None)))).scalar_one() == 0


async def test_an_answer_after_the_sitting_ended_is_still_logged(client):
    h, uid = await make(client)
    run_id = await start(client, h)
    q = await ask(client, h, run_id)
    key = await answer_key(q["session_id"])
    await client.post("/math/run/end", json={"run_id": run_id}, headers=h)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer(q, key)},
                          headers=h)
    assert r.status_code == 200 and r.json()["correct"] and "run" not in r.json()["math"]
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(func.count()).select_from(MathAnswer))).scalar_one() == 1
        assert (await db.get(MathRun, run_id)).asked == 0


async def test_nobody_else_can_use_a_sitting(client):
    h1, _ = await make(client, "toan_a")
    h2, _ = await make(client, "toan_b")
    run_id = await start(client, h1)
    q = await ask(client, h1, run_id)
    for path in ("/math/run/next", "/math/run/end"):
        r = await client.post(path, json={"run_id": run_id}, headers=h2)
        assert r.status_code == 404 and r.json()["error"]["code"] == "no_run"
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": {}}, headers=h2)
    assert r.status_code == 404


async def test_unreviewed_questions_are_not_served_when_the_server_forbids_them(client, monkeypatch):
    h, _ = await make(client)
    monkeypatch.setattr(settings, "allow_unreviewed", False)
    floors = (await client.get("/math/path", headers=h)).json()["subjects"][0]["floors"]
    assert not any(f["playable"] for f in floors)
    r = await client.post("/math/run/start", json={"subject_id": SUBJECT, "floor": 1}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"


async def test_math_questions_stay_out_of_the_vocabulary_no_repeat_window(client):
    h, uid = await make(client)
    run_id = await start(client, h)
    for _ in range(3):
        await play(client, h, run_id)
    async with dbm.SessionLocal() as db:
        assert await selection.recent_word_ids(db, uid, 5) == set()


# ------------------------------------------------------------------ migration 0010
def _alembic(url: str):
    from alembic.config import Config

    from app.config import SERVER_DIR
    cfg = Config(str(SERVER_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(SERVER_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def test_migration_0010_keeps_the_question_log_and_drops_the_word_key(tmp_path):
    from alembic import command
    path = tmp_path / "old.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0009")
    con = sqlite3.connect(path)
    con.execute("insert into words (id, hanzi, tier, rarity) values ('w_ma', '妈', 1, 'common')")
    user_cols = {r[1]: r for r in con.execute("pragma table_info(users)")}
    values = {name: ("old" if "CHAR" in col[2].upper() or "TEXT" in col[2].upper() else 0)
              for name, col in user_cols.items() if col[3] and col[4] is None and not col[5]}
    values.update(id=1, created_at="2026-01-01 00:00:00")
    values = {k: v for k, v in values.items() if k in user_cols}
    con.execute(f"insert into users ({', '.join(values)}) values ({', '.join('?' * len(values))})",
                list(values.values()))
    con.execute("insert into quiz_sessions (id, user_id, context, qtype, word_id, payload, answer_key, created_at, "
                "expires_at) values ('s1', 1, 'practice', 'Q1', 'w_ma', '{}', '{}', '2026-01-01', '2026-01-01')")
    con.commit()
    con.close()

    command.upgrade(cfg, "head")
    con = sqlite3.connect(path)
    assert con.execute("select id, item_id, qtype from quiz_sessions").fetchall() == [("s1", "w_ma", "Q1")]
    assert [fk[2] for fk in con.execute("pragma foreign_key_list(quiz_sessions)")] == ["users"]
    assert "ix_quiz_user_created" in [r[1] for r in con.execute("pragma index_list(quiz_sessions)")]
    con.execute("pragma foreign_keys=ON")
    con.execute("insert into quiz_sessions (id, user_id, context, qtype, item_id, payload, answer_key, created_at, "
                "expires_at) values ('s2', 1, 'math', 'multiple_choice', 'dstt_t1_th_02', '{}', '{}', "
                "'2026-01-01', '2026-01-01')")              # not a word: allowed now
    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    assert {"math_runs", "math_answers"} <= tables
    con.commit()
    con.close()

    command.downgrade(cfg, "0009")
    con = sqlite3.connect(path)
    assert con.execute("select id, word_id from quiz_sessions").fetchall() == [("s1", "w_ma")]     # math rows go
    assert sorted(fk[2] for fk in con.execute("pragma foreign_key_list(quiz_sessions)")) == ["users", "words"]
    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    assert not {"math_runs", "math_answers"} & tables
    con.close()
    command.upgrade(cfg, "head")                           # and forward again
