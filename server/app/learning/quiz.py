"""Question sessions (spec 8, 17): the shared question service of every math mode.

A mode asks a question with `create_session(context=...)` and the player answers it through
`POST /quiz/answer` -> `answer()`. Grading is identical everywhere and comes from the grader
registered for the question type; what happens next is decided by the handler registered for
the context (math practice, combat, tower defence, fishing, ...). Answer keys stay in the
database and are revealed only after answering.
"""
from __future__ import annotations

import datetime as dt
import uuid
from collections.abc import Awaitable, Callable
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from ..models import QuizSession, User


class QuizError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


class Question(Protocol):
    """What create_session needs of a question (learning/math_items.MathQuestion is one)."""
    qtype: str
    item_id: str
    time_limit: float
    answer_key: dict

    def public(self) -> dict: ...


Handler = Callable[[AsyncSession, User, QuizSession, bool, dt.datetime], Awaitable[dict]]
_handlers: dict[str, Handler] = {}


def register_handler(context: str, fn: Handler) -> None:
    _handlers[context] = fn


# Every question type registers its grader (math: systems/math_practice.py). A type nobody
# registered cannot be asked: create_session refuses it instead of grading it wrong later.
Grader = Callable[[str, dict, dict | None], bool]
_graders: dict[str, Grader] = {}


def register_grader(qtypes, fn: Grader) -> None:
    for qtype in qtypes:
        _graders[qtype] = fn


def grade(qtype: str, answer_key: dict, given: dict | None) -> bool:
    grader = _graders.get(qtype)
    if grader is None:
        raise LookupError(f"no grader registered for question type {qtype!r}")
    return grader(qtype, answer_key, given)


# Tu Vi for a right answer: cultivation.json xp_per_correct[context] unless the context
# registered its own rule (math: by difficulty tier).
XpRule = Callable[[QuizSession], int]
XpListener = Callable[[AsyncSession, QuizSession, int], Awaitable[None]]
_xp_rules: dict[str, XpRule] = {}
_xp_listeners: dict[str, XpListener] = {}


def register_xp_rule(context: str, fn: XpRule, on_gain: XpListener | None = None) -> None:
    """`fn(session)` = base Tu Vi for a right answer in this context; `on_gain` is told
    what the player really gained (after pills and pets)."""
    _xp_rules[context] = fn
    if on_gain:
        _xp_listeners[context] = on_gain


def base_xp(s: QuizSession) -> int:
    from ..systems import cultivation
    rule = _xp_rules.get(s.context)
    return int(rule(s)) if rule else int(cultivation.cfg()["xp_per_correct"].get(s.context, 0))


async def create_session(db: AsyncSession, user: User, context: str, question: Question,
                         ref: str | None = None, expires_in: float | None = None) -> dict:
    if question.qtype not in _graders:
        raise LookupError(f"no grader registered for question type {question.qtype!r}")
    now = clock.now()
    from ..systems import buffs
    from ..systems import linh_can                # and a linh căn of the calm mind (q_time)
    extra = buffs.extra_seconds(user, now) + await linh_can.value_db(db, user.id, "q_time")
    if extra and question.time_limit:
        question.time_limit = float(question.time_limit) + extra
    grace = balance.quiz()["network_grace"]
    life = expires_in if expires_in is not None else question.time_limit + grace
    s = QuizSession(id=str(uuid.uuid4()), user_id=user.id, context=context, ref=ref,
                    qtype=question.qtype, item_id=question.item_id, payload=question.public(),
                    answer_key=question.answer_key, created_at=now,
                    expires_at=now + dt.timedelta(seconds=life))
    db.add(s)
    await db.flush()
    return public_session(s)


def public_session(s: QuizSession) -> dict:
    return {"session_id": s.id, "context": s.context, **s.payload,
            "server_time": clock.now().isoformat() + "Z", "expires_at": s.expires_at.isoformat() + "Z"}


async def answer(db: AsyncSession, user: User, session_id: str, given: dict | None) -> dict:
    s = (await db.execute(select(QuizSession).where(QuizSession.id == session_id)
                          .with_for_update())).scalar_one_or_none()
    if s is None or s.user_id != user.id:
        raise QuizError(404, "no_session", "Không tìm thấy câu hỏi này.")
    if s.answered_at is not None:
        raise QuizError(409, "already_answered", "Câu này đã được trả lời rồi.")
    now = clock.now()
    timed_out = now > s.expires_at
    correct = (not timed_out) and grade(s.qtype, s.answer_key, given)
    s.answered_at, s.correct = now, correct
    s.answer = given if isinstance(given, dict) and len(str(given)) < 500 else None
    s.answer_ms = int((now - s.created_at).total_seconds() * 1000)
    _watch_for_bots(user, correct, s.answer_ms)

    handler = _handlers.get(s.context)
    extra = await handler(db, user, s, correct, now) if handler else {}
    if correct:  # Tu Vi: right answers anywhere are the main source (spec 7.3)
        from ..systems import buffs, cultivation, quests
        amount = base_xp(s)
        if amount:   # Tụ Linh Đan (stage 8), and the linh căn's xp_pct
            from ..systems import linh_can
            amount = int(round(amount * buffs.xp_mult(user, now) * (1 + await linh_can.value_db(db, user.id, "xp_pct"))))
        info = await cultivation.add_xp(db, user.id, amount, s.context) if amount else None
        if info:
            extra["xp"] = info
            if s.context in _xp_listeners:
                await _xp_listeners[s.context](db, s, info["gained"])
        await quests.on_event(db, user.id, "answer", "*")
    return {"correct": correct, "timed_out": timed_out,
            "correct_option": s.answer_key.get("option"),
            "reveal": s.answer_key.get("reveal"), **extra}


def _watch_for_bots(user: User, correct: bool, answer_ms: int) -> None:
    """Spec 17: a long run of right answers that are all inhumanly fast flags the account
    for an admin (`/admin flagged`). Nothing is banned automatically. The user row is only
    written when the streak actually changes."""
    w = balance.quiz()["bot_watch"]
    flags = user.flags or {}
    streak = int(flags.get("fast_streak", 0))
    new = streak + 1 if correct and answer_ms < w["fast_ms"] else 0
    if new == streak:
        return
    user.flags = {**flags, "fast_streak": new}
    if new >= w["streak"] and not user.suspicious_flag:
        user.suspicious_flag = (f"{new} câu đúng liền, mỗi câu dưới {w['fast_ms']} ms "
                                f"({clock.now():%d/%m/%Y %H:%M} UTC)")
