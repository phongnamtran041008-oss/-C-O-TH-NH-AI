"""M10: math_ask, the one place the game modes pick a math question from.

Whatever asks it - a bí cảnh, a hầm ngục, a cơ duyên, a tower - the question is legal only if
it is at the player's own tier or below, of an allowed type, and from a floor the player has
reached."""
import random

import pytest

from app import clock
from app import db as dbm
from app.learning import math_items, math_path
from app.models import MathAnswer, User
from app.systems import math_ask, math_combat, math_practice
from tests.helpers import register
from tests.test_math_skills import clear_floor

SUBJECT = "dai_so_tuyen_tinh"


async def open_tier_2(uid: int, skill_id: str, floor: int) -> None:
    window = math_path.cfg()["tier_unlock"]["window"]
    async with dbm.SessionLocal() as db:
        for n in range(window):
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=SUBJECT, skill_id=skill_id, floor=floor,
                              tier=1, item_id=f"x{n}", qtype="true_false", fingerprint=f"f{n}", correct=True,
                              timed_out=False, review=False, answer_ms=800, answered_at=clock.now()))
        await db.commit()


@pytest.mark.asyncio
async def test_own_floor_follows_the_learning_path(client, monkeypatch):
    _, me = await register(client, "ask_floor")
    uid = me["user_id"]
    assert math_ask.first_subject() == SUBJECT
    assert math_ask.playable_floors(SUBJECT) == list(range(1, 10))          # never the hidden floor 10
    async with dbm.SessionLocal() as db:
        assert await math_ask.own_floor(db, uid) == (SUBJECT, 1)
    await clear_floor(uid, 1)
    async with dbm.SessionLocal() as db:
        assert await math_ask.open_floor(db, uid, SUBJECT) == 2
        assert await math_ask.own_floor(db, uid) == (SUBJECT, 2)
    for n in (2, 3):
        await clear_floor(uid, n)
    async with dbm.SessionLocal() as db:
        assert await math_ask.open_floor(db, uid, SUBJECT) == 4
        assert await math_ask.own_floor(db, uid) == (SUBJECT, 4)
    # an open floor with no question (none today, so floor 4 is made to look unwritten):
    # "the player's own floor" is the highest one below it that has
    real = math_practice._templates
    monkeypatch.setattr(math_practice, "_templates", lambda s, f: [] if f == 4 else real(s, f))
    assert math_ask.playable_floors(SUBJECT) == [1, 2, 3] + list(range(5, 10))
    async with dbm.SessionLocal() as db:
        assert await math_ask.open_floor(db, uid, SUBJECT) == 4
        assert await math_ask.own_floor(db, uid) == (SUBJECT, 3)
    monkeypatch.undo()
    for n in range(4, 10):
        await clear_floor(uid, n)
    async with dbm.SessionLocal() as db:                                    # every main floor cleared: the last
        assert await math_ask.open_floor(db, uid, SUBJECT) == 9
        assert await math_ask.own_floor(db, uid) == (SUBJECT, 9)


@pytest.mark.asyncio
async def test_a_picked_question_is_of_an_allowed_type_and_never_above_the_players_tier(client):
    _, me = await register(client, "ask_tier")
    uid = me["user_id"]
    skill = math_path.subject(SUBJECT).floor(1).skills[0].id
    await open_tier_2(uid, skill, 1)
    rng = random.Random(3)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for qtype in [t for t in math_items.PLAYABLE_TYPES if t not in ("find_mistake", "tribulation")]:
            for _ in range(8):
                q = await math_ask.pick(db, user, SUBJECT, 1, qtypes=[qtype], rng=rng)
                assert q is not None, qtype
                meta = q.public()["math"]
                assert q.qtype == qtype and meta["floor"] == 1 and meta["subject"] == SUBJECT
                assert meta["tier"] <= await math_combat.tier_for(db, uid, meta["skill"], 1)
                assert meta["doc"]
        # a fresh player elsewhere on the floor is at tier 1: nothing harder is ever picked
        others = [k.id for k in math_path.subject(SUBJECT).floor(1).skills if k.id != skill]
        for _ in range(20):
            q = await math_ask.pick(db, user, SUBJECT, 1, skills=others, rng=rng)
            assert q.public()["math"]["tier"] == 1
        # Tìm chỗ sai (M11) starts at tier 2: nothing for a player who has not opened tier 2 of a
        # micro-skill that has one - never a question above their tier instead
        assert await math_ask.pick(db, user, SUBJECT, 1, qtypes=["find_mistake"], rng=rng) is None
        # a Thiên kiếp (M11 đợt 2) exists only at tiers 4-5: never on floor 1
        assert await math_ask.pick(db, user, SUBJECT, 1, qtypes=["tribulation"], rng=rng) is None
    with_one = "dstt_t1_tich_descartes"
    await open_tier_2(uid, with_one, 1)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for _ in range(6):
            q = await math_ask.pick(db, user, SUBJECT, 1, qtypes=["find_mistake"], rng=rng)
            meta = q.public()["math"]
            assert (q.qtype, meta["skill"], meta["tier"]) == ("find_mistake", with_one, 2)


@pytest.mark.asyncio
async def test_highest_asks_the_hardest_question_this_player_may_get(client):
    _, me = await register(client, "ask_high")
    uid = me["user_id"]
    skill = math_path.subject(SUBJECT).floor(1).skills[0].id
    await open_tier_2(uid, skill, 1)
    rng = random.Random(5)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for _ in range(10):
            q = await math_ask.pick(db, user, SUBJECT, 1, highest=True, rng=rng)
            meta = q.public()["math"]
            assert (meta["skill"], meta["tier"]) == (skill, 2)       # the one skill where tier 2 is open
        # min_tier above everything the player has opened: no question rather than an illegal one
        assert await math_ask.pick(db, user, SUBJECT, 1, min_tier=3, rng=rng) is None
        assert await math_ask.pick(db, user, SUBJECT, 1, qtypes=["tribulation"], rng=rng) is None
        assert await math_ask.pick(db, user, SUBJECT, 1, skills=["no_such_skill"], rng=rng) is None


@pytest.mark.asyncio
async def test_pick_own_asks_from_the_players_own_floor(client):
    _, me = await register(client, "ask_own")
    uid = me["user_id"]
    rng = random.Random(9)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        assert (await math_ask.pick_own(db, user, rng=rng)).public()["math"]["floor"] == 1
    await clear_floor(uid, 1)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for _ in range(6):
            assert (await math_ask.pick_own(db, user, rng=rng)).public()["math"]["floor"] == 2
