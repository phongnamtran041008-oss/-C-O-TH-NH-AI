"""One way to pick a math question for a player outside a buổi luyện (M10).

Bí cảnh, hầm ngục, cơ duyên and thủ thành all need the same thing: "a question for *this*
player, about these micro-skills, of these types". The learning rules that make such a
question legal are the ones of M7 and M9 and must not be re-invented per mode:

  * the tier is the player's own for the micro-skill (math_combat.tier_for, rule 3.3) and
    never above it; when the micro-skill has no template at that tier, the nearest lower
    tier that has one, never below `min_tier`;
  * the anti-repeat window is the player's whole answer log, whatever asked the question;
  * the answer is written to `math_answers` with no run (`record`), so what a player learns
    in a mode counts towards the tier they have opened and towards the mastery gate.

`pick` chooses, `record` writes the log row, `xp_rule` is the Tu Vi of a right answer. A
mode registers its own quiz context with `quiz.register_handler(CONTEXT, handler)` and
`quiz.register_xp_rule(CONTEXT, math_ask.xp_rule)`; its handler calls `record` first.
"""
from __future__ import annotations

import random
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..learning import math_items, math_mastery, math_path
from ..models import MathAnswer, User
from . import math_combat, math_practice

record = math_combat.record        # (db, user, quiz_session, correct, now) -> the "math" block
xp_rule = math_combat.xp_rule      # (quiz_session) -> Tu Vi for a right answer, by tier


async def open_floor(db: AsyncSession, user_id: int, subject_id: str) -> int:
    """The main floor of this subject the player is working on: the lowest one not cleared
    yet, or the last one when every main floor is cleared."""
    subject = math_path.subject(subject_id)
    cleared = await math_practice.cleared_floors(db, user_id, subject_id)
    n = math_mastery.next_floor(subject, cleared)
    return n if n is not None else subject.main_floors[-1].number


def playable_floors(subject_id: str) -> list[int]:
    """The main floors of this subject that have questions today."""
    subject = math_path.subject(subject_id)
    return [f.number for f in subject.main_floors if math_practice._templates(subject_id, f.number)]


def first_subject() -> str | None:
    """The first subject that has questions at all (today: Đại Số Tuyến Tính)."""
    return next((s.id for s in math_path.subjects() if playable_floors(s.id)), None)


async def own_floor(db: AsyncSession, user_id: int, subject_id: str | None = None) -> tuple[str, int] | None:
    """(subject, floor) a question "at the player's own floor" comes from: their open floor
    of the subject, or the highest floor below it that has questions. None when the game
    has no question for them at all."""
    subject_id = subject_id or first_subject()
    if subject_id is None:
        return None
    here = await open_floor(db, user_id, subject_id)
    below = [n for n in playable_floors(subject_id) if n <= here]
    return (subject_id, below[-1]) if below else None


async def _seen_at(db: AsyncSession, user_id: int, config: dict) -> dict[str, int]:
    rows = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user_id)
                             .order_by(MathAnswer.id.desc())
                             .limit(config["anti_repeat_window"]))).scalars().all()
    return {f: n for n, f in enumerate(reversed(list(rows)))}


async def pick(db: AsyncSession, user: User, subject_id: str, floor: int, *,
               skills: Iterable[str] | None = None, qtypes: Iterable[str] | None = None,
               min_tier: int = 1, highest: bool = False,
               rng: random.Random | None = None) -> math_items.MathQuestion | None:
    """One question for this player from floor `floor` of `subject_id`, or None.

    skills   micro-skills to ask about, tried in the given order (default: all of the
             floor, in random order);
    qtypes   allowed question types (default: every playable type);
    min_tier never ask below this tier;
    highest  False: the first micro-skill that has a usable template wins. True: among
             all the micro-skills, the one where the player's usable tier is highest wins
             (a boss, a "bài tổng hợp": the hardest question this player may be asked).

    The tier is the player's own for the chosen micro-skill, never above it."""
    rng = rng or random.Random()
    config = math_path.cfg()
    allowed = set(qtypes) if qtypes is not None else set(math_items.PLAYABLE_TYPES)
    allowed &= set(math_items.PLAYABLE_TYPES)
    templates = [t for t in math_practice._templates(subject_id, floor) if t.qtype in allowed]
    if skills is None:
        order = [k.id for k in math_path.subject(subject_id).floor(floor).skills]
        rng.shuffle(order)
    else:
        order = list(skills)
    best: tuple[int, list] | None = None
    for skill_id in order:
        mine = [t for t in templates if t.skill == skill_id]
        if not mine:
            continue
        tier = await math_combat.tier_for(db, user.id, skill_id, floor, config)
        usable = sorted({t.tier for t in mine if min_tier <= t.tier <= tier})
        if not usable:
            continue
        pool = [t for t in mine if t.tier == usable[-1]]
        if not highest:
            best = (usable[-1], pool)
            break
        if best is None or usable[-1] > best[0]:
            best = (usable[-1], pool)
    if best is None:
        return None
    item = math_practice._pick(best[1], await _seen_at(db, user.id, config), rng)
    if item is None:
        return None
    question = math_items.to_question(item, rng, config)
    question.meta["doc"] = math_practice.doc_link(item.skill)
    return question


async def pick_own(db: AsyncSession, user: User, *, subject_id: str | None = None,
                   qtypes: Iterable[str] | None = None, min_tier: int = 1, highest: bool = False,
                   rng: random.Random | None = None) -> math_items.MathQuestion | None:
    """A question at the player's own floor ("mỗi người nhận câu theo tầng của mình")."""
    where = await own_floor(db, user.id, subject_id)
    if where is None:
        return None
    return await pick(db, user, where[0], where[1], qtypes=qtypes, min_tier=min_tier, highest=highest, rng=rng)
