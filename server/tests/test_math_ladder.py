"""M11 đợt 2: learning-path rule 8, the ladder of a tier-5 question.

"Bài khó luôn có bậc thang: một câu bậc 5 phải được liên kết với danh sách bậc 3-4 dẫn tới
nó; nếu người chơi sai câu bậc 5, game quay lại đưa đúng các câu bậc thang đó."

The data rule (learning/math_items.py, `ladder_problems`) and the loop (systems/
math_practice.py): a wrong tier-5 answer in a buổi luyện is followed by exactly its rungs,
in order; rungs live in the database; rules 6 and 8 share the tier-5 mistake; nothing else
opens a ladder. There is no tier-5 content yet, so the loop runs on a fixture bank
(`ladder_bank`): floors 3, 7, 8 and 9 of Đại Số Tuyến Tính with fake questions, the tier-5
ones laddered to a floor-3 tier-3 item, a floor-8 tier-4 item and a floor-8 tier-4
generator."""
import dataclasses
import datetime as dt
import random
import sqlite3

import pytest
from sqlalchemy import select

from app import db as dbm
from app.learning import math_adaptive as ma
from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_path as mp
from app.models import MathAnswer, MathLadder, MathRetry, MathRun
from app.systems import math_practice
from tests.helpers import answer_key
from tests.test_math_loop import SUBJECT, clear_below, fake_items, make, right_answer, start, wrong_answer
from tests.test_math_mastery import meet_gate, start_trial

RUNG3 = "fake_3_0_3_0"           # floor 3, tier 3, the first micro-skill
RUNG4 = "fake_8_0_4_0"           # floor 8, tier 4
GEN = "fake_g8_ladder"           # a floor-8 tier-4 generator
LADDER = (RUNG3, RUNG4, GEN)
LADDER7 = (RUNG3, "fake_7_1_4_0", "fake_7_2_4_0")     # floor 7's tier-5 items: nothing above floor 7


def _gen(rng: random.Random) -> math_gen.Draw:
    a = rng.randint(2, 400)
    return math_gen.Draw(params={"a": a}, prompt_vi=f"Tính {a} + 1.", answer=str(a + 1),
                         solution_vi=[f"{a} + 1 = {a + 1}."])


@pytest.fixture
def ladder_bank(monkeypatch):
    """`ladder_bank(per_tier=3)`: the fixture bank (see the module docstring); spiral review
    off, so a test sees only what rules 6 and 8 put in."""
    real = {k: v for k, v in mi.bank().items() if v.subject != SUBJECT}
    real_gens = {k: v for k, v in mi.generators().items() if v.subject != SUBJECT}

    def use(per_tier: int = 3) -> dict:
        items = dict(real)
        for floor in (3, 7, 8, 9):
            for iid, it in fake_items(floor, per_tier=3 if floor in (3, 8) else per_tier).items():
                items[iid] = (dataclasses.replace(it, ladder=LADDER7 if floor == 7 else LADDER)
                              if it.tier == 5 else it)
        spec = mi.GeneratorSpec(id=GEN, subject=SUBJECT, skill=mp.subject(SUBJECT).floor(8).skills[0].id,
                                floor=8, tier=4, qtype="numeric", reviewed=True)
        gens = {**real_gens, GEN: spec}
        monkeypatch.setattr(mi, "bank", lambda: items)
        monkeypatch.setattr(mi, "generators", lambda: gens)
        monkeypatch.setitem(math_gen.REGISTRY, GEN, _gen)
        monkeypatch.setitem(mp.cfg()["spiral_review"], "share_min", 0)
        monkeypatch.setitem(mp.cfg()["spiral_review"], "share_max", 0)
        return items
    return use


async def player(client, name: str, floor: int = 9) -> tuple[dict, int, int]:
    h, uid = await make(client, name)
    await clear_below(uid, floor)
    return h, uid, await start(client, h, floor=floor)


async def ask(client, h, run_id) -> dict:
    r = await client.post("/math/run/next", json={"run_id": run_id}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["question"]


async def reply(client, h, q, correct=True, timed_out=False) -> dict:
    key = await answer_key(q["session_id"])
    given = {"timed_out": True} if timed_out else right_answer(q, key) if correct else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": given}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()["math"]


async def ladders(uid) -> list[MathLadder]:
    async with dbm.SessionLocal() as db:
        return list((await db.execute(select(MathLadder).where(MathLadder.user_id == uid)
                                      .order_by(MathLadder.id))).scalars())


async def miss_tier5(client, h, run_id, timed_out=False) -> tuple[dict, dict]:
    q = await ask(client, h, run_id)
    assert q["math"]["tier"] == 5 and not q["math"].get("ladder")
    res = await reply(client, h, q, correct=False, timed_out=timed_out)
    return q, res


# ------------------------------------------------------------------ the data rule
SUBJ = mp.subject(SUBJECT)
S3, S8, S9 = (SUBJ.floor(n).skills[0].id for n in (3, 8, 9))


def raw_items(**ladders) -> tuple[list[dict], list[dict]]:
    items = [{"id": "x_t3", "skill": S3, "tier": 3}, {"id": "x_t2", "skill": S3, "tier": 2},
             {"id": "x_t8a", "skill": S8, "tier": 4}, {"id": "x_t8b", "skill": S8, "tier": 4},
             {"id": "x_t8_5", "skill": S8, "tier": 5, "ladder": ["x_t3", "x_t8a"]}]
    for iid, ladder in ladders.items():
        it = {"id": iid, "skill": S9, "tier": 5}
        if ladder is not ...:
            it["ladder"] = ladder
        items.append(it)
    return items, [{"id": "x_g8", "skill": S8, "tier": 4}, {"id": "x_g3", "skill": S3, "tier": 3}]


def problems(**ladders) -> list[str]:
    return mi.ladder_problems(SUBJ, *raw_items(**ladders))


def test_a_good_ladder_passes():
    assert problems(q9=["x_t3", "x_t8a"]) == []
    assert problems(q9=["x_g3", "x_t8a", "x_g8", "x_t8b"]) == []          # generators count, up to four


@pytest.mark.parametrize("ladder, message", [
    (..., "q9: a tier-5 question must have a ladder (rule 8): 2 to 4 ids of tier 3-4 questions that lead to it"),
    (["x_t8a"], "q9: ladder must list 2 to 4 ids"),
    (["x_t3", "x_t8a", "x_t8b", "x_g8", "x_g3"], "q9: ladder must list 2 to 4 ids"),
    ("x_t8a", "q9: ladder must list 2 to 4 ids"),
    (["x_t3", "nope"], "q9: ladder id 'nope' is not a question or generator of dai_so_tuyen_tinh"),
    (["x_t8a", 7], "q9: ladder id 7 is not a question or generator of dai_so_tuyen_tinh"),
    (["x_t8a", "q9"], "q9: ladder lists the question itself"),
    (["x_t8a", "x_t8a"], "q9: ladder lists x_t8a twice"),
    (["x_t8a", "x_t2"], "q9: ladder step x_t2 is tier 2, a step must be tier 3 or 4"),
    (["x_t8a", "x_t8_5"], "q9: ladder step x_t8_5 is tier 5, a step must be tier 3 or 4"),
    (["x_t3", "x_g3"], "q9: ladder needs at least one tier-4 step"),
])
def test_ladder_problems_have_exact_messages(ladder, message):
    assert message in problems(q9=ladder)


def test_a_step_above_the_question_s_floor_and_a_ladder_below_tier_5_are_errors():
    items, gens = raw_items()
    items.append({"id": "x_t8c", "skill": S8, "tier": 5, "ladder": ["x_t3", "x_t9"]})
    items.append({"id": "x_t9", "skill": S9, "tier": 4})       # (tier 4 is not on floor 9, but the ladder rule sees floor 9)
    items.append({"id": "x_t3b", "skill": S3, "tier": 3, "ladder": ["x_t3", "x_t8a"]})
    got = mi.ladder_problems(SUBJ, items, gens)
    assert "x_t8c: ladder step x_t9 is on floor 9, above the question's floor 8" in got
    assert "x_t3b: only a tier-5 question has a ladder" in got


def test_a_rung_from_another_file_of_the_subject_counts(tmp_path):
    """The ids are checked against the whole subject: `<subject>.json` and its parts."""
    import json
    from app.learning import math_items
    folder = tmp_path / "items"
    folder.mkdir()
    (folder / f"{SUBJECT}.json").write_text(json.dumps({"subject": SUBJECT, "items": [{"id": "a"}]}), "utf-8")
    (folder / f"{SUBJECT}.t7_9.json").write_text(json.dumps({"subject": SUBJECT, "items": [{"id": "b"}]}),
                                                 "utf-8")
    merged = math_items.read_items(SUBJECT, tmp_path)
    assert [i["id"] for i in merged["items"]] == ["a", "b"]           # one bank: what ladder_problems is given
    items, gens = raw_items(q9=["x_t3", "x_t8a"])
    assert mi.ladder_problems(SUBJ, items[:2], []) == []              # the rungs alone: nothing to check
    assert mi.ladder_problems(SUBJ, items[2:], gens) != []            # the item without its rungs' file: unknown
    assert mi.ladder_problems(SUBJ, items, gens) == []


def test_the_ladder_key_is_known_and_carried_by_the_item():
    raw = {"id": "q9", "skill": S9, "tier": 5, "type": "true_false", "prompt_vi": "Mệnh đề.", "answer": True,
           "solution_vi": ["Vì."], "ladder": ["x_t3", "x_t8a"]}
    assert "ladder" in mi._ITEM_KEYS
    assert mi.build_item(SUBJ, raw).ladder == ("x_t3", "x_t8a")


def test_every_shipped_tier5_item_has_a_valid_ladder():
    """Over the real bank. Passes vacuously while no tier-5 item is written; becomes real
    when floors 7-9 land."""
    tier5 = [it for it in mi.bank().values() if it.tier == 5]
    for it in tier5:
        assert 2 <= len(it.ladder) <= 4, it.id
    for subject in mp.subjects():
        raw = mi.read_items(subject.id)
        if raw is None:
            continue
        assert mi.ladder_problems(subject, raw.get("items", []), raw.get("generators", [])) == []


# ------------------------------------------------------------------ a wrong tier-5 answer
@pytest.mark.asyncio
async def test_a_wrong_tier5_answer_is_followed_by_exactly_its_rungs_in_order(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_rungs")
    q5, res = await miss_tier5(client, h, run_id)
    async with dbm.SessionLocal() as db:
        missed = (await db.execute(select(MathAnswer.item_id).where(MathAnswer.user_id == uid))).scalar_one()
    assert res["ladder"] == {"of": missed, "step": 0, "steps": 3, "started": True, "rung": False, "done": False}
    assert res["parallel_waiting"]                                    # rule 6 remembers it too
    asked = []
    for n in range(3):
        q = await ask(client, h, run_id)
        assert q["math"]["ladder"] == {"of": res["ladder"]["of"], "step": n + 1, "steps": 3}
        asked.append(q)
        out = await reply(client, h, q, correct=True)
        assert out["ladder"]["step"] == n + 1 and out["ladder"]["done"] == (n == 2)
        assert out["tier_change"] == 0                                # a rung does not move the tier
    async with dbm.SessionLocal() as db:
        ids = (await db.execute(select(MathAnswer.item_id).where(MathAnswer.user_id == uid)
                                .order_by(MathAnswer.id))).scalars().all()
    assert ids[1:] == list(LADDER)                                     # exactly the rungs, in order
    assert [(q["math"]["floor"], q["math"]["tier"]) for q in asked] == [(3, 3), (8, 4), (8, 4)]
    assert out["ladder"]["returns"] and out["run"]["ladders"] == 1
    back = await ask(client, h, run_id)                               # the tier-5 idea comes back now
    assert back["math"]["tier"] == 5 and back["math"]["parallel"] and back["math"]["skill"] == q5["math"]["skill"]
    assert not back["math"].get("ladder")
    done = await reply(client, h, back, correct=True)
    assert "ladder" not in done
    async with dbm.SessionLocal() as db:
        retries = (await db.execute(select(MathRetry).where(MathRetry.user_id == uid))).scalars().all()
    assert len(retries) == 1 and retries[0].cleared_at is not None    # rule 6: cleared by the right answer
    (ladder,) = await ladders(uid)
    assert ladder.finished_at is not None and ladder.step == 3 and ladder.missed == 0


@pytest.mark.asyncio
async def test_a_generator_rung_is_a_fresh_draw_each_time(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_fresh")
    prints = []
    for sitting in range(3):
        await miss_tier5(client, h, run_id)
        for _ in range(3):
            q = await ask(client, h, run_id)
            if q["math"]["ladder"]["step"] == 3:
                prints.append((await answer_key(q["session_id"]))["fingerprint"])
            await reply(client, h, q)
        await client.post("/math/run/end", json={"run_id": run_id}, headers=h)
        run_id = await start(client, h, floor=9)
        q = await ask(client, h, run_id)                              # the tier-5 parallel question
        await reply(client, h, q)
    assert len(prints) == 3 and len(set(prints)) == 3


@pytest.mark.asyncio
async def test_a_right_tier5_answer_starts_nothing(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_right")
    for _ in range(4):
        q = await ask(client, h, run_id)
        assert q["math"]["tier"] == 5 and not q["math"].get("ladder")
        res = await reply(client, h, q, correct=True)
        assert "ladder" not in res
    assert await ladders(uid) == []


@pytest.mark.asyncio
async def test_a_timeout_on_a_tier5_question_opens_the_ladder(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_timeout")
    _, res = await miss_tier5(client, h, run_id, timed_out=True)
    assert res["timed_out"] and res["ladder"]["started"]
    q = await ask(client, h, run_id)
    assert q["math"]["ladder"]["step"] == 1
    out = await reply(client, h, q, timed_out=True)                  # a rung timed out is a missed rung
    assert out["ladder"]["missed"] == 1


@pytest.mark.asyncio
async def test_a_missed_rung_keeps_the_ladder_going_and_holds_the_tier5_idea_to_the_next_sitting(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_missed")
    q5, _ = await miss_tier5(client, h, run_id)
    steps = []
    for n in range(3):
        q = await ask(client, h, run_id)
        steps.append(q["math"]["ladder"]["step"])
        out = await reply(client, h, q, correct=(n != 0))           # the first rung (floor 3) is missed
        if n == 0:
            assert out["parallel_waiting"] and out["ladder"]["missed"] == 1
    assert steps == [1, 2, 3] and out["ladder"]["done"] and not out["ladder"]["returns"]
    # this sitting: the missed rung comes back (rule 6, its own floor's templates), the tier-5 idea does not
    later = []
    for _ in range(6):
        q = await ask(client, h, run_id)
        later.append(q["math"])
        await reply(client, h, q, correct=True)
    assert later[0]["parallel"] and (later[0]["floor"], later[0]["tier"]) == (3, 3)
    assert later[0]["skill"] == mp.subject(SUBJECT).floor(3).skills[0].id
    assert not any(m["parallel"] and m["tier"] == 5 for m in later)
    # the next sitting: the tier-5 idea comes back first
    await client.post("/math/run/end", json={"run_id": run_id}, headers=h)
    run_id = await start(client, h, floor=9)
    q = await ask(client, h, run_id)
    assert q["math"]["parallel"] and q["math"]["tier"] == 5 and q["math"]["skill"] == q5["math"]["skill"]


@pytest.mark.asyncio
async def test_the_ladder_survives_closing_the_game(client, ladder_bank):
    ladder_bank()
    h, uid, run_id = await player(client, "ld_survive")
    await miss_tier5(client, h, run_id)
    q = await ask(client, h, run_id)
    await reply(client, h, q)                                         # rung 1 of 3
    q2 = await ask(client, h, run_id)                                 # rung 2 open ... and the game is closed
    assert q2["math"]["ladder"]["step"] == 2
    assert (await ask(client, h, run_id))["session_id"] == q2["session_id"]      # back: the same question
    await client.post("/math/run/end", json={"run_id": run_id}, headers=h)
    run_id = await start(client, h, floor=9)                          # a new sitting of the floor
    q = await ask(client, h, run_id)
    assert q["math"]["ladder"]["step"] == 2 and q["math"]["floor"] == 8
    await reply(client, h, q)
    q = await ask(client, h, run_id)
    assert q["math"]["ladder"]["step"] == 3
    out = await reply(client, h, q)
    assert out["ladder"]["done"] and out["run"]["ladders"] == 1      # counted in the sitting it ends in
    async with dbm.SessionLocal() as db:
        assert (await db.get(MathRun, run_id)).ladders == 1


@pytest.mark.asyncio
async def test_rules_6_and_8_never_chase_each_other(client, ladder_bank):
    """One tier-5 template per micro-skill: the parallel question of the miss is the item
    itself, and a second miss of it in the same sitting is plain rule 6 (no second ladder)."""
    ladder_bank(per_tier=1)
    h, uid, run_id = await player(client, "ld_chase")
    q5, _ = await miss_tier5(client, h, run_id)
    for _ in range(3):
        await reply(client, h, await ask(client, h, run_id))
    back = await ask(client, h, run_id)
    assert back["math"]["parallel"] and back["math"]["tier"] == 5
    res = await reply(client, h, back, correct=False)
    assert "ladder" not in res and res["parallel_waiting"]
    assert len(await ladders(uid)) == 1
    q = await ask(client, h, run_id)
    assert not q["math"].get("ladder")                                # rule 6 goes on, no rungs
    # a new sitting: the same item may open its ladder again
    await reply(client, h, q, correct=True)
    await client.post("/math/run/end", json={"run_id": run_id}, headers=h)
    run_id = await start(client, h, floor=9)
    while True:
        q = await ask(client, h, run_id)
        if q["math"]["tier"] == 5:
            break
        await reply(client, h, q)
    res = await reply(client, h, q, correct=False)
    assert res["ladder"]["started"] and len(await ladders(uid)) == 2


@pytest.mark.asyncio
async def test_a_rung_that_left_the_bank_is_passed_by(client, ladder_bank, monkeypatch):
    items = ladder_bank()
    h, uid, run_id = await player(client, "ld_gone")
    await miss_tier5(client, h, run_id)
    del items[RUNG4]
    steps = []
    for _ in range(2):
        q = await ask(client, h, run_id)
        steps.append((q["math"]["ladder"]["step"], q["math"]["floor"]))
        await reply(client, h, q)
    assert steps == [(1, 3), (3, 8)]


# ------------------------------------------------------------------ nothing else opens a ladder
@pytest.mark.asyncio
async def test_the_thien_kiep_nho_starts_no_ladder(client, ladder_bank):
    ladder_bank()
    h, uid, _ = await player(client, "ld_trial")
    await meet_gate(uid, floor=9)
    r = await start_trial(client, h, floor=9)
    assert r.status_code == 200, r.text
    run_id = r.json()["run"]["run_id"]
    q = await ask(client, h, run_id)
    assert q["math"]["tier"] == 5
    res = await reply(client, h, q, correct=False)
    assert "ladder" not in res and await ladders(uid) == []
    # floor 9 resolves to a two-skill part of Đạo Thụ, where no miss is allowed: the trial is over
    assert res["trial"]["passed"] is False
    r = await start_trial(client, h, floor=9)             # taken again straight away: still no rung waiting
    assert r.status_code == 200, r.text
    q = await ask(client, h, r.json()["run"]["run_id"])
    assert not q["math"].get("ladder") and await ladders(uid) == []


@pytest.mark.asyncio
async def test_the_placement_test_starts_no_ladder_and_leaves_none_for_later(client, ladder_bank):
    ladder_bank()                                                     # written floors: 3, 7, 8, 9
    h, uid = await make(client, "ld_place")
    r = await client.post("/math/placement/start", json={"subject_id": SUBJECT}, headers=h)
    assert r.status_code == 200, r.text
    run_id = r.json()["run"]["run_id"]
    tier5 = 0
    for _ in range(20):
        out = (await client.post("/math/placement/next", json={"run_id": run_id}, headers=h)).json()
        if out["question"] is None:
            break
        q = out["question"]
        tier5 += q["math"]["tier"] == 5
        res = await reply(client, h, q, correct=q["math"]["floor"] < 9)
        assert "ladder" not in res
        if res["placement"]["decided"]:
            break
    assert tier5 >= 1 and res["placement"]["start_floor"] == 9
    assert await ladders(uid) == []
    run_id = await start(client, h, floor=9)
    q = await ask(client, h, run_id)
    assert not q["math"].get("ladder") and not q["math"]["parallel"]


def test_only_a_buoi_luyen_calls_the_ladder():
    """The other modes (chiêu, quái, hầm ngục, tháp, cơ duyên, bí cảnh) answer through their
    own handlers, none of which knows the ladder: only math_practice.math_handler calls it,
    and only for a sitting whose mode is practice."""
    import inspect
    from pathlib import Path

    import app.systems as systems
    for path in Path(systems.__file__).parent.glob("*.py"):
        if path.name != "math_practice.py":
            assert "_ladder_after_answer" not in path.read_text("utf-8"), path.name
    src = inspect.getsource(math_practice.math_handler)
    assert "run.mode == PRACTICE" in src and "_ladder_after_answer" in src


# ------------------------------------------------------------------ rule 4 still holds
@pytest.mark.asyncio
async def test_nothing_asks_above_the_player_s_tier_except_a_rung(client, ladder_bank):
    """Floor 7 (tiers 4-5) from a fresh log: every question is at most the open tier of its
    micro-skill, a parallel question repeats a tier already asked; only a rung (marked as
    one) may be above what the log opened - here a floor-3 tier-3 question to a player who
    never answered floor 3 (cleared by a passed trial row only)."""
    ladder_bank()
    h, uid, run_id = await player(client, "ld_rule4", floor=7)
    log: dict[str, dict[int, list[bool]]] = {}
    asked_tiers: dict[str, set[int]] = {}
    rungs, missed5 = [], False
    for n in range(80):
        q = await ask(client, h, run_id)
        m = q["math"]
        mine = log.setdefault(m["skill"], {})
        if m.get("ladder"):
            rungs.append((m["floor"], m["tier"], ma.open_tier(m["floor"], mine)))
        elif m["parallel"]:
            assert m["tier"] in asked_tiers.get(m["skill"], set())
        else:
            assert m["tier"] <= ma.open_tier(m["floor"], mine), (n, m)
        asked_tiers.setdefault(m["skill"], set()).add(m["tier"])
        wrong = m["tier"] == 5 and not missed5 and not m.get("ladder")
        missed5 = missed5 or wrong
        await reply(client, h, q, correct=not wrong)
        mine.setdefault(m["tier"], []).append(not wrong)
        if missed5 and len(rungs) == 3:
            break
    assert missed5 and len(rungs) == 3
    assert rungs[0] == (3, 3, 2)                                      # the stated exception: above the log


# ------------------------------------------------------------------ the migration
def test_migration_0015_adds_the_ladder_table_and_the_count(tmp_path):
    from alembic import command

    from tests.test_math_loop import _alembic
    path = tmp_path / "m15.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0014_math_dungeon")
    con = sqlite3.connect(path)
    con.execute("insert into math_runs (user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
                "combo, best_combo, asked, correct, review_asked, xp_gained, started_at) "
                "values (1, 's', 1, 'practice', 1, 0, 0, 0, 0, 0, 0, 0, 0, '2026-01-01 00:00:00')")
    con.commit()
    con.close()
    command.upgrade(cfg, "0015_math_ladder")
    con = sqlite3.connect(path)
    cols = {r[1] for r in con.execute("pragma table_info(math_ladders)")}
    assert {"user_id", "subject_id", "floor", "item_id", "steps", "step", "missed", "retry_id",
            "started_run_id", "run_id", "finished_at"} <= cols
    assert con.execute("select ladders from math_runs").fetchall() == [(0,)]
    con.close()
    command.downgrade(cfg, "0014_math_dungeon")
    con = sqlite3.connect(path)
    assert "ladders" not in {r[1] for r in con.execute("pragma table_info(math_runs)")}
    con.close()
