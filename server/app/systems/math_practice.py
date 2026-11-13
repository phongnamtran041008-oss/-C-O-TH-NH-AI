"""The math question loop (milestone M2): a player sits down on a floor of a math subject
and answers one question after another.

A sitting is a MathRun. `next_question` picks an item and opens it through the shared
quiz service (context "math"), so the countdown, the grading and the answer key work
like every other question and the client answers through /quiz/answer. The handler below
then logs the answer (MathAnswer), moves the tier (learning-path rules 2 and 3,
learning/math_adaptive.py) and Tu Vi is paid by tier (balance/math.json).

Not here yet: prerequisites and mastery gates between floors, spaced review, the
parallel question after a mistake (later milestones).
"""
from __future__ import annotations

import datetime as dt
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import settings
from ..learning import math_adaptive, math_items, math_path, quiz
from ..models import MathAnswer, MathRun, QuizSession, User

CONTEXT = "math"


class MathError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ views
def _items(subject_id: str, floor: int) -> list[math_items.MathItem]:
    return math_items.floor_items(subject_id, floor, settings.allow_unreviewed)


def run_view(run: MathRun) -> dict:
    lo, hi = math_path.floor_tiers(run.floor)
    return {"run_id": run.id, "subject_id": run.subject_id, "floor": run.floor, "tier": run.tier,
            "tier_name_vi": math_path.cfg()["tiers"][str(run.tier)]["name_vi"], "tier_min": lo, "tier_max": hi,
            "combo": run.combo, "best_combo": run.best_combo, "asked": run.asked, "correct": run.correct,
            "xp_gained": run.xp_gained, "ended": run.ended_at is not None}


async def open_run(db: AsyncSession, user_id: int) -> MathRun | None:
    return (await db.execute(select(MathRun).where(MathRun.user_id == user_id, MathRun.ended_at.is_(None))
                             .order_by(MathRun.id.desc()))).scalars().first()


async def path_view(db: AsyncSession, user: User) -> dict:
    """The subjects and floors, how many questions each floor has for this server, and the
    sitting the player left open (if any)."""
    cfg = math_path.cfg()
    subjects = []
    for s in math_path.subjects():
        floors = []
        for f in s.floors:
            lo, hi = math_path.floor_tiers(f.number)
            n = len(_items(s.id, f.number))
            floors.append({"floor": f.number, "title_vi": f.title_vi, "hidden": f.hidden,
                           "tier_min": lo, "tier_max": hi, "questions": n, "playable": n > 0,
                           "skills": [{"id": k.id, "name_vi": k.name_vi} for k in f.skills]})
        subjects.append({"id": s.id, "name_vi": s.name_vi, "order": s.order, "floors": floors})
    run = await open_run(db, user.id)
    return {"subjects": subjects, "run": run_view(run) if run else None,
            "tiers": {t: v["name_vi"] for t, v in cfg["tiers"].items() if not t.startswith("_")}}


# ------------------------------------------------------------------ a sitting
async def start(db: AsyncSession, user: User, subject_id: str, floor: int) -> dict:
    try:
        subject = math_path.subject(subject_id)
        subject.floor(floor)
    except KeyError:
        raise MathError(404, "no_floor", "Không có tầng này.")
    if not _items(subject_id, floor):
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    now = clock.now()
    for old in (await db.execute(select(MathRun).where(MathRun.user_id == user.id,
                                                       MathRun.ended_at.is_(None)))).scalars():
        old.ended_at = now          # one sitting at a time
    state = math_adaptive.start(floor)
    run = MathRun(user_id=user.id, subject_id=subject_id, floor=floor, tier=state.tier,
                  correct_streak=0, wrong_streak=0, combo=0, best_combo=0, asked=0, correct=0,
                  xp_gained=0, started_at=now)
    db.add(run)
    await db.flush()
    return {"run": run_view(run)}


async def _own_run(db: AsyncSession, user: User, run_id: int, lock: bool = False) -> MathRun:
    q = select(MathRun).where(MathRun.id == run_id)
    run = (await db.execute(q.with_for_update() if lock else q)).scalar_one_or_none()
    if run is None or run.user_id != user.id:
        raise MathError(404, "no_run", "Không tìm thấy buổi luyện này.")
    return run


async def end(db: AsyncSession, user: User, run_id: int) -> dict:
    run = await _own_run(db, user, run_id, lock=True)
    if run.ended_at is None:
        run.ended_at = clock.now()
    return {"run": run_view(run)}


async def _results_by_skill(db: AsyncSession, user_id: int, skill_ids: list[str], floor: int,
                            window: int) -> dict[str, dict[int, list[bool]]]:
    """skill -> tier -> the player's last `window` answers at that tier, oldest first. Only
    the tiers that can open a higher tier of this floor are read."""
    out: dict[str, dict[int, list[bool]]] = {s: {} for s in skill_ids}
    lo, hi = math_path.floor_tiers(floor)
    for skill in skill_ids:
        for tier in range(lo, hi):
            rows = (await db.execute(
                select(MathAnswer.correct).where(MathAnswer.user_id == user_id, MathAnswer.skill_id == skill,
                                                 MathAnswer.tier == tier)
                .order_by(MathAnswer.id.desc()).limit(window))).scalars().all()
            if rows:
                out[skill][tier] = list(reversed(rows))
    return out


def choose_item(items: list[math_items.MathItem], run_tier: int, floor: int,
                results: dict[str, dict[int, list[bool]]], recent: list[str],
                rng: random.Random) -> math_items.MathItem:
    """The next item of a sitting. `recent` = fingerprints of the player's latest answers,
    newest first (the anti-repeat window).

    A micro-skill is drawn first, then one of its items at the tier that skill may be asked
    at (math_adaptive.question_tier); when it has no item at that tier, the nearest lower
    tier that has one, else the nearest higher tier that is open. Items answered inside the
    window are passed over while anything else is left; when all were seen, the one seen
    longest ago comes back."""
    by_skill: dict[str, list[math_items.MathItem]] = {}
    for it in items:
        by_skill.setdefault(it.skill, []).append(it)
    lo, _ = math_path.floor_tiers(floor)
    pools: list[list[math_items.MathItem]] = []
    for skill, own in sorted(by_skill.items()):
        by_tier = results.get(skill, {})
        want = math_adaptive.question_tier(run_tier, floor, by_tier)
        top = math_adaptive.open_tier(floor, by_tier)
        tiers = sorted({it.tier for it in own})
        usable = ([t for t in reversed(tiers) if lo <= t <= want]
                  or [t for t in tiers if want < t <= top])
        if usable:
            pools.append([it for it in own if it.tier == usable[0]])
    if not pools:
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi phù hợp.")
    seen_at = {fp: i for i, fp in reversed(list(enumerate(recent)))}      # fingerprint -> how recent (0 = newest)
    fresh = [[it for it in pool if it.fingerprint not in seen_at] for pool in pools]
    fresh = [pool for pool in fresh if pool]
    if fresh:
        return rng.choice(rng.choice(fresh))
    return max((it for pool in pools for it in pool), key=lambda it: (seen_at[it.fingerprint], it.id))


async def next_question(db: AsyncSession, user: User, run_id: int, rng: random.Random | None = None) -> dict:
    """The run's open question if it still has one, else a new one."""
    run = await _own_run(db, user, run_id, lock=True)
    if run.ended_at is not None:
        raise MathError(409, "run_ended", "Buổi luyện này đã kết thúc.")
    now = clock.now()
    pending = (await db.execute(select(QuizSession).where(
        QuizSession.user_id == user.id, QuizSession.context == CONTEXT, QuizSession.ref == str(run.id),
        QuizSession.answered_at.is_(None), QuizSession.expires_at > now)
        .order_by(QuizSession.created_at.desc()))).scalars().first()
    if pending is not None:
        return {"run": run_view(run), "question": quiz.public_session(pending)}

    cfg = math_path.cfg()
    items = _items(run.subject_id, run.floor)
    skills = sorted({it.skill for it in items})
    results = await _results_by_skill(db, user.id, skills, run.floor, cfg["tier_unlock"]["window"])
    recent = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user.id)
                               .order_by(MathAnswer.id.desc()).limit(cfg["anti_repeat_window"]))).scalars().all()
    rng = rng or random.Random()
    item = choose_item(items, run.tier, run.floor, results, list(recent), rng)
    question = math_items.to_question(item, rng)
    out = await quiz.create_session(db, user, CONTEXT, question, ref=str(run.id))
    return {"run": run_view(run), "question": out}


# ------------------------------------------------------------------ after an answer
async def math_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    meta = s.payload["math"]
    # the server's clock ran out, or the client's countdown did (it then sends {"timed_out": true})
    timed_out = now > s.expires_at or bool(isinstance(s.answer, dict) and s.answer.get("timed_out"))
    run = None
    if s.ref:
        run = (await db.execute(select(MathRun).where(MathRun.id == int(s.ref))
                                .with_for_update())).scalar_one_or_none()
    db.add(MathAnswer(user_id=user.id, run_id=run.id if run else None, subject_id=meta["subject"],
                      skill_id=meta["skill"], floor=meta["floor"], tier=meta["tier"], item_id=s.item_id,
                      qtype=s.qtype, fingerprint=s.answer_key.get("fingerprint", ""), correct=correct,
                      timed_out=timed_out, answer_ms=s.answer_ms or 0, answered_at=now))
    out: dict = {"tier": meta["tier"], "timed_out": timed_out, "xp_base": math_path.xp_for_tier(meta["tier"]) if correct else 0}
    if run is not None and run.ended_at is None and run.user_id == user.id:
        before = run.tier
        state = math_adaptive.after_answer(
            math_adaptive.TierState(run.tier, run.correct_streak, run.wrong_streak), correct, run.floor)
        run.tier, run.correct_streak, run.wrong_streak = state.tier, state.correct_streak, state.wrong_streak
        run.asked += 1
        run.correct += int(correct)
        run.combo = run.combo + 1 if correct else 0      # a wrong answer or a timeout ends the combo
        run.best_combo = max(run.best_combo, run.combo)
        out.update(run=run_view(run), tier_change=run.tier - before)
    return {"math": out}


def _xp_rule(s: QuizSession) -> int:
    return math_path.xp_for_tier(s.payload["math"]["tier"])


async def _on_xp(db: AsyncSession, s: QuizSession, gained: int) -> None:
    run = await db.get(MathRun, int(s.ref)) if s.ref else None
    if run is not None:
        run.xp_gained += int(gained)


quiz.register_handler(CONTEXT, math_handler)
quiz.register_grader(math_items.PLAYABLE_TYPES, math_items.grade)
quiz.register_xp_rule(CONTEXT, _xp_rule, _on_xp)
