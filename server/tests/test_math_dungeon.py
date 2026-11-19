"""M10: hầm ngục - a seeded chain of rooms, one question type per room.

The layout is a pure function of (seed, subject, floor); the questions inside follow the
learning rules (the player's own tier, the anti-repeat window, every answer logged). A wrong
answer or a timeout costs a tâm lực, zero ends the run, nothing earned is taken back."""
import copy
import random
import sqlite3
import sys
from pathlib import Path

import pytest
from sqlalchemy import select

from app import db as dbm
from app.learning import math_items, math_path
from app.models import MathAnswer, MathDungeonRun, User
from app.systems import items, math_combat, math_dungeon, math_practice
from tests.helpers import answer_key, register
from tests.test_combat import LOOK
from tests.test_math_ask import open_tier_2
from tests.test_math_skills import clear_floor

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import math_dungeon_bot as bot  # noqa: E402

SUBJECT = "dai_so_tuyen_tinh"
FLOORS = (1, 2, 3)


async def make(client, name: str, floor: int = 1):
    """A player with a character (Tu Vi needs one) whose own floor is `floor` (the floors
    below it cleared)."""
    h, me = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " "), "appearance": LOOK},
                          headers=h)
    assert r.status_code == 200, r.text
    for n in range(1, floor):
        await clear_floor(me["user_id"], n)
    return h, me["user_id"]


async def start(client, h, **body) -> dict:
    r = await client.post("/math/dungeon/start", json=body, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["run"]


async def ask(client, h, run_id) -> dict:
    r = await client.post("/math/dungeon/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def answer(client, h, q: dict, correct: bool, given: dict | None = None) -> dict:
    key = await answer_key(q["session_id"])
    given = given if given is not None else (bot.right_answer(q, key) if correct else bot.wrong_answer(q, key))
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": given}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def stones(uid: int) -> int:
    async with dbm.SessionLocal() as db:
        return (await db.get(User, uid)).spirit_stones


async def held(uid: int) -> dict[str, int]:
    async with dbm.SessionLocal() as db:
        return await items.stacks(db, uid)


def lowest_tier_pairs(floor: int) -> set[tuple[str, str]]:
    lo, _ = math_path.floor_tiers(floor)
    return {(t.qtype, t.skill) for t in math_practice._templates(SUBJECT, floor) if t.tier == lo}


# ------------------------------------------------------------------ the data
def test_the_dungeon_data_is_sound():
    assert math_dungeon.validate() == []
    raw = math_dungeon._read()
    assert set(raw["room_kinds"]) == set(math_items.PLAYABLE_TYPES)     # one room kind per playable type


def test_validate_catches_broken_data():
    raw = math_dungeon._read()
    bad = copy.deepcopy(raw)
    del bad["room_kinds"]["ordering"]
    bad["hearts"] = 0
    bad["rooms"] = {"min": 5, "max": 3}
    bad["wardens"] = []
    bad["rewards"]["1"]["room"]["items"] = {"ghi_chu_phan_tu": 1}          # a note: only monsters drop those
    bad["rewards"]["2"]["chests"][0]["items"] = {"no_such_thing": 1}
    del bad["rewards"]["3"]
    problems = "\n".join(math_dungeon.validate(bad))
    for needle in ("no room for the question type ordering", "hearts", "rooms must be", "wardens",
                   "ghi_chu_phan_tu", "no_such_thing", "floor 3 has questions but no rewards"):
        assert needle in problems, needle


# ------------------------------------------------------------------ the layout
@pytest.mark.parametrize("floor", FLOORS)
def test_the_same_seed_gives_the_same_dungeon_and_other_seeds_differ(floor):
    d = math_dungeon.data()
    layouts = [math_dungeon.generate(seed, SUBJECT, floor) for seed in range(60)]
    assert layouts == [math_dungeon.generate(seed, SUBJECT, floor) for seed in range(60)]
    shapes = {tuple((r["kind"], r["skill"], r["guardian_vi"]) for r in lay["rooms"]) for lay in layouts}
    assert len(shapes) > 40                                   # different seeds, different dungeons
    assert {len(lay["rooms"]) for lay in layouts} == set(range(d["rooms"]["min"], d["rooms"]["max"] + 1))
    assert len({lay["chest"]["name_vi"] for lay in layouts}) == len(d["rewards"][str(floor)]["chests"])
    # the floor is part of the seed's meaning: seed 7 on another floor is another dungeon
    assert math_dungeon.generate(7, SUBJECT, floor) != math_dungeon.generate(7, SUBJECT, floor % 3 + 1)


@pytest.mark.parametrize("floor", FLOORS)
def test_every_generated_room_can_be_asked_and_is_one_question_type(floor):
    pairs = lowest_tier_pairs(floor)
    kinds = {q for q, _ in pairs}
    skills = {k.id for k in math_path.subject(SUBJECT).floor(floor).skills}
    seen = set()
    for seed in range(300):
        lay = math_dungeon.generate(seed, SUBJECT, floor)
        *rooms, warden = lay["rooms"]
        assert warden["warden"] and warden["skill"] is None and warden["kind"] in kinds
        for a, b in zip(lay["rooms"], lay["rooms"][1:]):
            assert a["kind"] != b["kind"]                     # never the same kind twice in a row
        for r in rooms:
            assert not r["warden"] and r["skill"] in skills
            assert (r["kind"], r["skill"]) in pairs           # askable by anyone on the floor
            seen.add(r["kind"])
    assert seen == kinds                                       # every kind the floor can ask turns up
    # find_mistake exists from tier 2: floors 1-2 (lowest tier 1) never get a room for it, floor 3 (tiers 2-3) does
    assert ("find_mistake" in kinds) == (math_path.floor_tiers(floor)[0] >= 2)
    if math_path.floor_tiers(floor)[0] == 1:
        assert not any(r["kind"] == "find_mistake" for seed in range(100)
                       for r in math_dungeon.generate(seed, SUBJECT, floor)["rooms"])


def test_a_kind_the_floor_cannot_ask_at_its_lowest_tier_is_never_generated(monkeypatch):
    real = math_practice._templates
    lo, _ = math_path.floor_tiers(1)

    def without_low_ordering(subject_id, floor):
        return [t for t in real(subject_id, floor) if not (t.qtype == "ordering" and t.tier == lo)]
    monkeypatch.setattr(math_practice, "_templates", without_low_ordering)
    assert "ordering" not in math_dungeon.askable(SUBJECT, 1)
    for seed in range(200):
        assert all(r["kind"] != "ordering" for r in math_dungeon.generate(seed, SUBJECT, 1)["rooms"])
    monkeypatch.setattr(math_practice, "_templates", lambda s, f: [])
    assert math_dungeon.generate(1, SUBJECT, 1) is None


@pytest.mark.asyncio
async def test_a_seed_replays_through_the_api_and_without_one_the_server_draws_it(client):
    h, _ = await make(client, "dg_seed")
    a = await start(client, h, seed=4242)
    b = await start(client, h, seed=4242)
    assert a["seed"] == b["seed"] == 4242 and a["rooms"] == b["rooms"] and a["chest"] == b["chest"]
    prev = (await client.get("/math/dungeon/layout", params={"seed": 4242}, headers=h)).json()["layout"]
    assert [r["kind"] for r in prev["rooms"]] == [r["kind"] for r in a["rooms"]]
    drawn = await start(client, h)
    assert 0 <= drawn["seed"] <= math_dungeon.data()["seed_max"]
    again = await start(client, h, seed=drawn["seed"])
    assert again["rooms"] == drawn["rooms"]
    r = await client.post("/math/dungeon/start", json={"seed": math_dungeon.data()["seed_max"] + 1}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_seed"


@pytest.mark.asyncio
async def test_only_floors_the_player_has_reached(client, monkeypatch):
    h, _ = await make(client, "dg_floor")
    view = (await client.get("/math/dungeon", headers=h)).json()
    assert view["own_floor"] == 1 and view["run"] is None and view["hearts"] == math_dungeon.data()["hearts"]
    floors = {f["floor"]: f for f in view["floors"]}
    assert sorted(floors) == list(range(1, 10))                          # main floors only, never the hidden 10
    assert floors[1]["open"] and not floors[2]["open"] and floors[2]["locked_vi"]
    assert floors[4]["locked_vi"] == "Chưa tới tầng này trên lộ trình học."     # written, not reached
    r = await client.post("/math/dungeon/start", json={"floor": 2}, headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "floor_locked"
    r = await client.post("/math/dungeon/start", json={"floor": 10}, headers=h)    # the hidden floor: no questions
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"
    # rule 5 (every main floor is written today, so floor 4 is made to look unwritten)
    real = math_practice._templates
    monkeypatch.setattr(math_practice, "_templates", lambda s, f: [] if f == 4 else real(s, f))
    floors = {f["floor"]: f for f in (await client.get("/math/dungeon", headers=h)).json()["floors"]}
    assert floors[4]["locked_vi"] == "Tầng này chưa có câu hỏi."      # rule 5: shown, locked, with a reason
    r = await client.post("/math/dungeon/start", json={"floor": 4}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"
    monkeypatch.undo()
    r = await client.get("/math/dungeon/layout", params={"seed": 1, "floor": 2}, headers=h)
    assert r.status_code == 403
    h3, _ = await make(client, "dg_floor3", floor=3)
    assert (await start(client, h3))["floor"] == 3                       # default: the player's own floor
    assert (await start(client, h3, floor=1))["floor"] == 1               # a floor below may be replayed


# ------------------------------------------------------------------ the questions
@pytest.mark.asyncio
@pytest.mark.parametrize("floor", FLOORS)
async def test_each_room_asks_its_own_type_at_the_players_tier_and_every_answer_is_logged(client, floor):
    h, uid = await make(client, f"dg_rooms{floor}", floor)
    run = await start(client, h, seed=100 + floor)
    asked = []
    while True:
        out = await ask(client, h, run["run_id"])
        q, run = out["question"], out["run"]
        room = run["rooms"][run["room"]]
        m = q["math"]
        assert q["qtype"] == room["kind"] and m["floor"] == floor and m["dungeon"]["room"] == run["room"]
        if not room["warden"]:
            assert m["skill"] == room["skill"]
        async with dbm.SessionLocal() as db:
            assert m["tier"] <= await math_combat.tier_for(db, uid, m["skill"], floor)
        res = await answer(client, h, q, True)
        asked.append((m["skill"], m["tier"]))
        run = res["dungeon"]["run"]
        if run["ended"]:
            break
    assert run["state"] == "cleared" and run["chest_opened"]
    assert run["asked"] == len(asked) == sum(r["need"] for r in run["rooms"])
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid)
                                 .order_by(MathAnswer.id))).scalars().all()
    assert [(a.skill_id, a.tier) for a in rows] == asked
    assert all(a.run_id is None and a.correct for a in rows)


@pytest.mark.asyncio
async def test_the_warden_asks_the_hardest_question_this_player_may_get(client):
    h, uid = await make(client, "dg_warden")
    seed = next(s for s in range(100) if math_dungeon.generate(s, SUBJECT, 1)["rooms"][-1]["kind"] == "numeric")
    skill = next(t.skill for t in math_practice._templates(SUBJECT, 1) if t.qtype == "numeric" and t.tier == 2)
    await open_tier_2(uid, skill, 1)
    run = await start(client, h, seed=seed)
    async with dbm.SessionLocal() as db:                  # walk straight to the last room
        row = await db.get(MathDungeonRun, run["run_id"])
        row.room = len(run["rooms"]) - 1
        await db.commit()
    for _ in range(3):
        q = (await ask(client, h, run["run_id"]))["question"]
        assert q["math"]["dungeon"]["warden"] and q["qtype"] == "numeric"
        assert (q["math"]["skill"], q["math"]["tier"]) == (skill, 2)     # the one micro-skill at tier 2
        await answer(client, h, q, False)
        if (await client.get(f"/math/dungeon/run/{run['run_id']}", headers=h)).json()["run"]["ended"]:
            break


# ------------------------------------------------------------------ tâm lực, timeouts, resuming
@pytest.mark.asyncio
async def test_wrong_answers_cost_tam_luc_and_zero_ends_the_run_keeping_what_was_paid(client):
    h, uid = await make(client, "dg_hearts")
    before = await stones(uid)
    run = await start(client, h, seed=11)
    need = run["rooms"][0]["need"]
    for _ in range(need):                                  # clear the first room
        res = await answer(client, h, (await ask(client, h, run["run_id"]))["question"], True)
    d = res["dungeon"]
    assert d["room_cleared"] and d["reward"]["stones"] == run["room_reward"]["stones"] and not d["reward"]["withheld"]
    hearts = d["run"]["hearts"]
    assert hearts == math_dungeon.data()["hearts"]
    for n in range(hearts):
        res = await answer(client, h, (await ask(client, h, run["run_id"]))["question"], False)
        d = res["dungeon"]
        assert d["heart_lost"] and d["run"]["hearts"] == hearts - n - 1
    assert d["run"]["state"] == "failed" and d["run"]["ended"] and d["run"]["rooms"][1]["state"] == "lost"
    assert d["run"]["stones_gained"] == run["room_reward"]["stones"]
    assert await stones(uid) - before == run["room_reward"]["stones"]       # không mất đồ
    r = await client.post("/math/dungeon/next", json={"run_id": run["run_id"]}, headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "run_ended"


@pytest.mark.asyncio
async def test_running_out_of_time_is_a_wrong_answer(client, frozen):
    h, uid = await make(client, "dg_time")
    run = await start(client, h, seed=12)
    q = (await ask(client, h, run["run_id"]))["question"]
    frozen.advance(seconds=q["time_limit"] + 30)
    res = await answer(client, h, q, True)                     # the right answer, too late
    assert not res["correct"] and res["timed_out"] and res["math"]["timed_out"]
    assert res["dungeon"]["heart_lost"] and res["dungeon"]["run"]["hearts"] == math_dungeon.data()["hearts"] - 1
    assert "xp" not in res
    # the client's own countdown ran out: it sends {"timed_out": true}
    q = (await ask(client, h, run["run_id"]))["question"]
    res = await answer(client, h, q, False, given={"timed_out": True})
    assert res["math"]["timed_out"] and res["dungeon"]["run"]["hearts"] == math_dungeon.data()["hearts"] - 2
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer.timed_out, MathAnswer.correct)
                                 .where(MathAnswer.user_id == uid))).all()
    assert rows == [(True, False), (True, False)]


@pytest.mark.asyncio
async def test_a_run_left_open_is_resumed_and_a_question_that_ran_out_meanwhile_counts_as_a_timeout(client, frozen):
    h, uid = await make(client, "dg_resume")
    run = await start(client, h, seed=13)
    first = await ask(client, h, run["run_id"])
    again = await ask(client, h, run["run_id"])                # the game was closed and opened again
    assert again["question"]["session_id"] == first["question"]["session_id"]
    view = (await client.get("/math/dungeon", headers=h)).json()
    assert view["run"]["run_id"] == run["run_id"] and view["run"]["hearts"] == run["hearts"]

    frozen.advance(seconds=first["question"]["time_limit"] + 60)       # ... and stayed closed too long
    view = (await client.get("/math/dungeon", headers=h)).json()
    assert view["run"]["hearts"] == run["hearts"] - 1                   # the question was a timeout
    out = await ask(client, h, run["run_id"])
    assert out["question"]["session_id"] != first["question"]["session_id"]
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer.timed_out).where(MathAnswer.user_id == uid))).scalars().all()
    assert rows == [True]

    # starting another dungeon leaves this one (one run at a time)
    other = await start(client, h, seed=14)
    assert (await client.get(f"/math/dungeon/run/{run['run_id']}", headers=h)).json()["run"]["state"] == "abandoned"
    assert (await client.get("/math/dungeon", headers=h)).json()["run"]["run_id"] == other["run_id"]


@pytest.mark.asyncio
async def test_a_run_can_be_abandoned_and_a_question_answered_after_that_only_counts_for_learning(client):
    h, uid = await make(client, "dg_leave")
    run = await start(client, h, seed=15)
    q = (await ask(client, h, run["run_id"]))["question"]
    r = await client.post("/math/dungeon/abandon", json={"run_id": run["run_id"]}, headers=h)
    assert r.status_code == 200 and r.json()["run"]["state"] == "abandoned" and r.json()["run"]["ended"]
    res = await answer(client, h, q, False)
    assert res["dungeon"]["stale"] and res["dungeon"]["run"]["hearts"] == run["hearts"]
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(MathAnswer.id).where(MathAnswer.user_id == uid))).scalars().all()
    assert (await client.get("/math/dungeon", headers=h)).json()["run"] is None
    r = await client.post("/math/dungeon/next", json={"run_id": run["run_id"]}, headers=h)
    assert r.status_code == 409
    h2, _ = await make(client, "dg_other")
    r = await client.post("/math/dungeon/abandon", json={"run_id": run["run_id"]}, headers=h2)
    assert r.status_code == 404                                        # someone else's run


# ------------------------------------------------------------------ rewards
@pytest.mark.asyncio
async def test_a_cleared_dungeon_pays_every_room_and_the_chest_and_tu_vi_by_tier(client):
    h, uid = await make(client, "dg_chest", floor=2)
    before_stones, before_items = await stones(uid), await held(uid)
    out = await bot.play_dungeon(client, h, answer_key, seed=777)
    run = out["run"]
    assert run["state"] == "cleared" and run["chest_opened"] and run["rewarded"]
    lay = math_dungeon.generate(777, SUBJECT, 2)
    want_stones = lay["room_reward"]["stones"] * (len(lay["rooms"]) - 1) + lay["chest"]["stones"]
    assert run["stones_gained"] == want_stones == await stones(uid) - before_stones
    after = await held(uid)
    for item, qty in lay["chest"]["items"].items():
        assert after.get(item, 0) - before_items.get(item, 0) == qty
    assert {i["item_id"]: i["qty"] for i in run["items_gained"]} == lay["chest"]["items"]
    assert run["xp_gained"] == out["xp"] == sum(math_path.xp_for_tier(s["tier"]) for s in out["steps"])
    assert out["steps"][-1]["dungeon"]["chest"]["stones"] == lay["chest"]["stones"]


@pytest.mark.asyncio
async def test_after_the_days_rewarded_runs_a_dungeon_still_teaches_but_pays_no_loot(client, frozen, monkeypatch):
    monkeypatch.setitem(math_dungeon.data(), "rewards_per_day", 1)
    h, uid = await make(client, "dg_daily")
    first = await bot.play_dungeon(client, h, answer_key, seed=21)
    assert first["run"]["rewarded"] and first["run"]["stones_gained"] > 0
    assert (await client.get("/math/dungeon", headers=h)).json()["rewards_left"] == 0
    before = await stones(uid)
    second = await bot.play_dungeon(client, h, answer_key, seed=22)
    assert not second["run"]["rewarded"] and second["run"]["stones_gained"] == 0 and not second["run"]["items_gained"]
    assert await stones(uid) == before and second["run"]["xp_gained"] > 0
    assert second["steps"][-1]["dungeon"]["chest"]["withheld"]
    frozen.advance(days=1)                                             # a new day
    assert (await client.get("/math/dungeon", headers=h)).json()["rewards_left"] == 1
    assert (await bot.play_dungeon(client, h, answer_key, seed=23))["run"]["rewarded"]


# ------------------------------------------------------------------ the bot
@pytest.mark.asyncio
async def test_the_bot_plays_many_seeds_on_every_floor_and_every_run_ends_cleanly(client):
    """60 dungeons, floors 1-3, from always right to mostly wrong: every run ends as cleared
    or failed, nothing raises, and what it paid is exactly what the data says."""
    rng = random.Random(2026)
    rates = (0.0, 0.2, 0.45, 0.8)
    states = set()
    for floor in FLOORS:
        h, uid = await make(client, f"dg_bot{floor}", floor)
        start_stones, start_items = await stones(uid), await held(uid)
        paid_stones, paid_items, rewarded_runs = 0, {}, 0
        for n in range(20):
            seed = rng.randint(0, math_dungeon.data()["seed_max"])
            out = await bot.play_dungeon(client, h, answer_key, seed=seed, floor=floor,
                                         wrong_rate=rates[n % len(rates)], rng=rng)
            run, lay = out["run"], math_dungeon.generate(seed, SUBJECT, floor)
            states.add(run["state"])
            assert run["ended"] and run["state"] in ("cleared", "failed") and run["seed"] == seed
            assert [r["kind"] for r in run["rooms"]] == [r["kind"] for r in lay["rooms"]]
            assert all(s["floor"] == floor and s["qtype"] == lay["rooms"][s["room"]]["kind"] for s in out["steps"])
            wrong = sum(1 for s in out["steps"] if not s["correct"])
            assert run["hearts"] == run["max_hearts"] - wrong
            assert (run["state"] == "failed") == (run["hearts"] == 0)
            normal_cleared = min(run["rooms_cleared"], len(lay["rooms"]) - 1)
            want = lay["room_reward"]["stones"] * normal_cleared
            if run["state"] == "cleared":
                want += lay["chest"]["stones"]
                for item, qty in lay["chest"]["items"].items():
                    paid_items[item] = paid_items.get(item, 0) + (qty if run["rewarded"] else 0)
            assert run["stones_gained"] == (want if run["rewarded"] else 0)
            paid_stones += run["stones_gained"]
            rewarded_runs += run["rewarded"]
        assert rewarded_runs == math_dungeon.data()["rewards_per_day"]      # the daily limit held
        assert await stones(uid) - start_stones == paid_stones
        after = await held(uid)
        assert {k: after.get(k, 0) - start_items.get(k, 0) for k in paid_items} == paid_items
    assert states == {"cleared", "failed"}


# ------------------------------------------------------------------ the migration
def test_migration_0014_adds_the_dungeon_table(tmp_path):
    from alembic import command

    from tests.test_math_loop import _alembic
    path = tmp_path / "m14.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0013")
    command.upgrade(cfg, "0014_math_dungeon")
    con = sqlite3.connect(path)
    cols = {r[1] for r in con.execute("pragma table_info(math_dungeon_runs)")}
    assert {"user_id", "seed", "floor", "layout", "room", "progress", "hearts", "state", "rewarded"} <= cols
    con.close()
    command.downgrade(cfg, "0013")
    con = sqlite3.connect(path)
    assert "math_dungeon_runs" not in {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    con.close()


def test_a_room_view_never_says_more_than_the_layout():
    """The map a client draws comes from the layout alone: no answer, no template id."""
    lay = math_dungeon.layout_view(math_dungeon.generate(5, SUBJECT, 1))
    assert set(lay["rooms"][0]) == {"kind", "name_vi", "short_vi", "desc_vi", "skill", "skill_name_vi",
                                    "guardian_vi", "flavour_vi", "warden", "need", "index", "qtype_vi"}


# ------------------------------------------------------------------ Thiên kiếp (M11 đợt 2)
def test_a_thien_kiep_room_asks_one_question_and_so_does_its_warden(monkeypatch):
    """A Thiên kiếp takes 8-12 minutes: its room kind (`questions` 1) is cleared by one right
    answer, a trấn thủ of that kind too; the other kinds keep questions_per_room."""
    d = math_dungeon.data()
    assert d["room_kinds"]["tribulation"]["questions"] == 1 and d["questions_per_room"] > 1
    skills = [k.id for k in math_path.subject(SUBJECT).floor(7).skills]
    monkeypatch.setattr(math_dungeon, "askable", lambda s, f: {"tribulation": skills[:2], "numeric": skills})
    seen = set()
    for seed in range(60):
        lay = math_dungeon.generate(seed, SUBJECT, 7)
        for r in lay["rooms"]:
            want = 1 if r["kind"] == "tribulation" else (d["warden_questions"] if r["warden"] else d["questions_per_room"])
            assert r["need"] == want, r
            seen.add((r["kind"], r["warden"]))
            if r["kind"] == "tribulation":
                assert r["name_vi"] == "Phòng Lôi Kiếp"
    assert ("tribulation", True) in seen and ("tribulation", False) in seen


def test_a_thien_kiep_room_is_only_generated_where_the_floor_has_one_at_its_lowest_tier():
    for f in (1, 2, 3, 4, 5, 6):                              # (the lowest tier of these floors is 1-3)
        assert "tribulation" not in math_dungeon.askable(SUBJECT, f)


def test_validate_checks_the_questions_of_a_room_kind():
    raw = copy.deepcopy(math_dungeon._read())
    raw["room_kinds"]["tribulation"]["questions"] = 0
    raw["room_kinds"]["numeric"]["mo_ta"] = "x"
    problems = math_dungeon.validate(raw)
    assert "room_kinds.tribulation.questions: must be a whole number >= 1" in problems
    assert any(p.startswith("room_kinds.numeric: must be {name_vi, short_vi, desc_vi}") for p in problems)
