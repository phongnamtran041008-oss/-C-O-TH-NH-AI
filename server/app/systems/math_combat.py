"""Quái = lỗi sai: what the math edition's monsters ask, and what answering them does (M7,
kế hoạch 4.2).

A monster of `data/math/monsters.json` stands for one common mistake and carries the
micro-skill that mistake belongs to. Its Mặc Thuẫn comes down the same way every other
monster's does - by answering a question - except the question is a math one about that
micro-skill, and the tier is **the player's own**: the highest tier of the floor their
answer log has opened for that skill (rule 3.3). So the same monster keeps being worth
fighting as the player gets better, and nobody meets a question the path has not opened.

The answer is written to `math_answers` with no run, exactly like a question asked in a
buổi luyện: the learning rules read that log, so what a player learns in the field counts
towards the tier they have opened and towards the mastery gate. What is deliberately *not*
done here is rule 6 ("tâm ma"): a parallel question has nowhere to come back to outside a
run, so a mistake in the field is recorded and left at that.
"""
from __future__ import annotations

import datetime as dt
import random
from collections.abc import Awaitable, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..learning import math_adaptive, math_items, math_path, quiz
from ..models import MathAnswer, QuizSession, User
from . import math_practice

CONTEXT = "math_combat"
# What is asked in the middle of a fight or on a timer (a field monster, đả tọa, Thiên Kiếp):
# every playable type except the Thiên kiếp question type, which takes 8-12 minutes.
QUICK_TYPES = tuple(t for t in math_items.PLAYABLE_TYPES if t != "tribulation")


def skill_of(info: dict) -> str | None:
    """The micro-skill a monster is a mistake about, or None for the Mặc Quái of the forest,
    which ask a question at the player's own floor instead (realtime/combat.py)."""
    return info.get("skill")


def is_mistake_monster(info: dict | None) -> bool:
    return bool(info) and bool(info.get("skill")) and bool(info.get("subject"))


async def tier_for(db: AsyncSession, user_id: int, skill_id: str, floor: int,
                   config: dict | None = None) -> int:
    """Which tier this player is at for this micro-skill, read from their own answer log."""
    config = config or math_path.cfg()
    window = config["tier_unlock"]["window"]
    lo, hi = math_path.floor_tiers(floor, config)
    results: dict[int, list[bool]] = {}
    for tier in range(lo, hi):
        rows = (await db.execute(
            select(MathAnswer.correct).where(MathAnswer.user_id == user_id, MathAnswer.skill_id == skill_id,
                                             MathAnswer.tier == tier)
            .order_by(MathAnswer.id.desc()).limit(window))).scalars().all()
        if rows:
            results[tier] = list(reversed(rows))
    return math_adaptive.open_tier(floor, results, config)


async def question_for(db: AsyncSession, user: User, info: dict,
                       rng: random.Random | None = None) -> math_items.MathQuestion | None:
    """One question for this monster, or None when its micro-skill has no template that can
    be asked (then the monster simply keeps its shield and the player is told)."""
    rng = rng or random.Random()
    config = math_path.cfg()
    skill_id, floor, subject_id = info["skill"], int(info["floor"]), info["subject"]
    tier = await tier_for(db, user.id, skill_id, floor, config)
    # a monster asks a quick question in the middle of a fight, never a Thiên kiếp (8-12 minutes)
    templates = [t for t in math_practice._templates(subject_id, floor) if t.qtype != "tribulation"]
    pool = math_practice._at_tier(templates, skill_id, tier)
    if not pool:
        return None
    rows = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user.id)
                             .order_by(MathAnswer.id.desc())
                             .limit(config["anti_repeat_window"]))).scalars().all()
    seen_at = {f: n for n, f in enumerate(reversed(list(rows)))}
    item = math_practice._pick(pool, seen_at, rng)
    if item is None:
        return None
    question = math_items.to_question(item, rng, config)
    question.meta["doc"] = math_practice.doc_link(item.skill)
    question.meta["mistake_vi"] = info.get("mistake_vi", "")
    question.meta["monster_vi"] = info.get("name_vi", "")
    return question


# M10 (cơ duyên): modes that want to hear "a math answer was just written to the log" register
# here. A listener gets (db, user, quiz session, correct, now) and returns a dict that is merged
# into the "math" block of the answer response (or {}); it must filter by `s.context` itself.
AnswerListener = Callable[[AsyncSession, User, QuizSession, bool, dt.datetime], Awaitable[dict]]
_answer_listeners: list[AnswerListener] = []


def add_answer_listener(fn: AnswerListener) -> None:
    if fn not in _answer_listeners:
        _answer_listeners.append(fn)


async def notify_answer(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    out: dict = {}
    for fn in _answer_listeners:
        out.update(await fn(db, user, s, correct, now) or {})
    return out


async def record(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    """Write a question asked in the field (a monster's, or a chiêu's since M9) to the answer
    log with no run, so the learning path counts it."""
    meta = s.payload["math"]
    timed_out = now > s.expires_at or bool(isinstance(s.answer, dict) and s.answer.get("timed_out"))
    db.add(MathAnswer(user_id=user.id, run_id=None, subject_id=meta["subject"], skill_id=meta["skill"],
                      floor=meta["floor"], tier=meta["tier"], item_id=s.item_id, qtype=s.qtype,
                      fingerprint=s.answer_key.get("fingerprint", ""), correct=correct, timed_out=timed_out,
                      review=False, answer_ms=s.answer_ms or 0, answered_at=now))
    await db.flush()
    block = {"tier": meta["tier"], "timed_out": timed_out, "parallel": False, "parallel_waiting": False,
             "review": False, "xp_base": math_path.xp_for_tier(meta["tier"]) if correct else 0}
    block.update(await notify_answer(db, user, s, correct, now))
    from . import pets   # Rồng and Gà (stage 8): Tu Vi on top of the answer's own
    block.update(await pets.on_math_answer(db, user, s, correct))
    return block


async def math_combat_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool,
                              now: dt.datetime) -> dict:
    """Grading a question a monster asked: write it to the learning log, then tell the fight."""
    from ..realtime import combat
    out: dict = {"math": await record(db, user, s, correct, now)}
    p = combat._world().players.get(user.id)
    if p is not None:
        out["combat"] = combat.on_answer(p, s.id, correct, s.answer_ms)
    return out


def xp_rule(s: QuizSession) -> int:
    return math_path.xp_for_tier(s.payload["math"]["tier"])


quiz.register_handler(CONTEXT, math_combat_handler)
quiz.register_xp_rule(CONTEXT, xp_rule)
