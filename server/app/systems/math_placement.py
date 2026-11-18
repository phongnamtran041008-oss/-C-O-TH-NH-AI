"""Bài kiểm tra đầu vào: learning-path rule 7 (milestone M11).

"10-15 câu rải các bậc để đặt điểm xuất phát; ai đã giỏi thì được nhảy tầng, nhưng vẫn
phải qua cổng thuần thục của tầng đích." The rules this module plays, every number from
`balance/math.json` -> `placement_test`:

**When it is offered.** Per subject, and optional. A subject offers it while the player
  * has no floor of that subject cleared by a Thiên kiếp nhỏ,
  * has no sitting of it going on, and no result for it yet - or a result that placed them
    on the first floor (nothing skipped) at least `retake_after_days` days ago. A result
    that skipped a floor is final: the floors it skipped are already behind the player
    (`retake_after_days: null` = never a second sitting at all);
  * and the subject has at least two written main floors (floors that have questions):
    with one, the only possible outcome is the first floor, and the test says nothing.

**What it asks.** A sitting plans `per_floor` questions for every written main floor,
clamped to [min_questions, max_questions] in all and shared out evenly (a lower floor gets
the odd one). Inside a floor the questions go tier by tier, lowest first (the odd one goes
to the higher tier), and the micro-skills of the floor take turns in path order. So the
whole sitting rises: floor by floor, and tier by tier inside a floor. Each question is a
real question of the shared quiz service (context `math_placement`, answered through
`POST /quiz/answer`) with the normal time limit of its type and tier. The plan is a pure
function of the path and the bank (`plan`), so nothing about it is stored.

**Rule 4's one exception.** Everywhere else a tier-N question of a micro-skill appears only
after right answers at tier N-1 (math_adaptive, math_ask.pick). A placement question is
asked at the tier its slot says, whatever the player's log - that is what lets a strong
player show it. So this module picks its questions itself (`_question`) and is the only
place that does. Its answers are real answers: they go to `math_answers` with the
placement sitting's `run_id`, so they count for the tiers the player opens and for the
mastery gate like any other answer, and an audit of rule 4 can tell them apart (the run's
`mode` is "placement").

**When it stops.** A floor's bar is `pass_pct` of its planned questions right (80% of 5 =
4). The sitting stops as soon as the bar of a floor can no longer be met - the floors above
cannot change the outcome any more - or when every question has been asked. Questions are
not skipped when a floor's bar is already met: the hardest tier of the floor is still
asked. A question whose time runs out is wrong (the client sends `{"timed_out": true}`; a
question nobody answered is settled as a timeout when the sitting next asks for one).

**The outcome.** The start floor is the lowest written floor whose bar was not met; when
every bar was met, the last written floor - never a floor without questions. The main
floors below the start floor count as **cleared by placement** (math_practice.
cleared_floors, the single source everything reads: path_view, math_ask.open_floor and so
bí cảnh, hầm ngục, cơ duyên, thủ thành, chiêu thức). They are told apart from floors cleared
by a Thiên kiếp nhỏ in the path view (`cleared_by`). On the start floor nothing is waived:
its mastery gate and its Thiên kiếp nhỏ work exactly as for anyone.

**Leaving a sitting.** "Nghỉ" only pauses it (the question that was open runs out and
counts as wrong). Abandoning it (`/math/placement/abandon`, or `/math/run/end` on it) ends
it with nothing skipped: the player starts on the first floor, and the retake rule of a
first-floor result applies. A placement sitting lives beside a buổi luyện; starting one
never ends the other.

Stored as a `MathRun` with `mode == "placement"`: while it runs, `floor`/`tier` are those of
the current question; once it has an outcome `passed` is true and `floor` is the start
floor. An abandoned sitting has `passed` false (or null when another path ended it).
"""
from __future__ import annotations

import datetime as dt
import math
import random
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..learning import math_items, math_path, quiz
from ..learning.math_items import Template
from ..models import MathAnswer, MathRun, QuizSession, User
from . import math_practice
from .math_practice import PLACEMENT, MathError

CONTEXT = "math_placement"
OFFERED, IN_PROGRESS, DONE, UNAVAILABLE = "offered", "in_progress", "done", "unavailable"


def cfg(config: dict | None = None) -> dict:
    return (config or math_path.cfg())["placement_test"]


# ------------------------------------------------------------------ the plan (pure)
@dataclass(frozen=True)
class Slot:
    """One planned question: which floor, micro-skill and tier."""
    floor: int
    skill: str
    tier: int


def floor_counts(n_floors: int, config: dict | None = None) -> list[int]:
    """How many questions each of `n_floors` written floors gets, lowest floor first."""
    if n_floors <= 0:
        return []
    p = cfg(config)
    total = min(max(n_floors * p["per_floor"], p["min_questions"]), p["max_questions"])
    base, extra = divmod(total, n_floors)
    return [base + (1 if i < extra else 0) for i in range(n_floors)]


def plan(subject: math_path.Subject, templates_by_floor: dict[int, list[Template]],
         config: dict | None = None) -> list[Slot]:
    """The questions of a sitting, in the order they are asked. `templates_by_floor` = the
    question templates this server can ask, by floor (a floor without any is not written)."""
    config = config or math_path.cfg()
    floors = [f for f in subject.main_floors if templates_by_floor.get(f.number)]
    out: list[Slot] = []
    for f, count in zip(floors, floor_counts(len(floors), config)):
        temps = templates_by_floor[f.number]
        lo, hi = math_path.floor_tiers(f.number, config)
        tiers = [t for t in range(lo, hi + 1) if any(x.tier == t for x in temps)]
        if not tiers:
            continue
        base, extra = divmod(count, len(tiers))
        n = 0
        for i, tier in enumerate(tiers):
            k = base + (1 if i >= len(tiers) - extra else 0)       # the odd one: the harder tier
            skills = [s.id for s in f.skills if any(x.skill == s.id and x.tier == tier for x in temps)]
            for _ in range(k):
                out.append(Slot(f.number, skills[n % len(skills)], tier))
                n += 1
    return out


def needed(planned: int, config: dict | None = None) -> int:
    """Right answers a floor's bar wants out of its `planned` questions (80% of 5 = 4)."""
    return math.ceil(planned * cfg(config)["pass_pct"] / 100 - 1e-9)


@dataclass(frozen=True)
class FloorScore:
    floor: int
    planned: int
    asked: int
    correct: int
    needed: int

    @property
    def met(self) -> bool | None:
        """True = bar met, False = it can no longer be met, None = still open."""
        if self.correct >= self.needed and self.asked >= self.planned:
            return True
        if self.correct + (self.planned - self.asked) < self.needed:
            return False
        return None

    def view(self) -> dict:
        return {"floor": self.floor, "planned": self.planned, "asked": self.asked,
                "correct": self.correct, "needed": self.needed, "met": self.met}


def score(slots: list[Slot], results: list[bool], config: dict | None = None
          ) -> tuple[list[FloorScore], int | None]:
    """The floors' scores after these answers (in slot order), and the start floor once the
    outcome is decided (None while it is not)."""
    floors: dict[int, list[bool | None]] = {}
    for i, slot in enumerate(slots):
        floors.setdefault(slot.floor, []).append(results[i] if i < len(results) else None)
    scores = [FloorScore(n, len(r), sum(1 for x in r if x is not None), sum(1 for x in r if x),
                         needed(len(r), config)) for n, r in floors.items()]
    for s in scores:
        if s.met is False:
            return scores, s.floor
        if s.met is None:
            return scores, None
    return scores, (scores[-1].floor if scores else None)


# ------------------------------------------------------------------ reading the database
def _templates_by_floor(subject: math_path.Subject) -> dict[int, list[Template]]:
    return {f.number: math_practice._templates(subject.id, f.number) for f in subject.main_floors}


def written_floors(subject_id: str) -> list[int]:
    subject = math_path.subject(subject_id)
    return [f.number for f in subject.main_floors if math_practice._templates(subject_id, f.number)]


def subject_plan(subject_id: str) -> list[Slot]:
    subject = math_path.subject(subject_id)
    return plan(subject, _templates_by_floor(subject))


async def _sittings(db: AsyncSession, user_id: int, subject_id: str) -> list[MathRun]:
    """This player's placement sittings of the subject, newest first."""
    return list((await db.execute(select(MathRun).where(
        MathRun.user_id == user_id, MathRun.subject_id == subject_id, MathRun.mode == PLACEMENT)
        .order_by(MathRun.id.desc()))).scalars())


def start_floor_of(run: MathRun) -> int:
    """Where a finished sitting placed the player: its floor, or the first floor when the
    sitting was abandoned."""
    first = math_path.subject(run.subject_id).main_floors[0].number
    return run.floor if run.passed else first


async def _results(db: AsyncSession, run: MathRun) -> list[MathAnswer]:
    return list((await db.execute(select(MathAnswer).where(MathAnswer.run_id == run.id)
                                  .order_by(MathAnswer.id))).scalars())


def _retake_at(run: MathRun, config: dict | None = None) -> dt.datetime | None:
    """When a finished sitting may be taken again, or None for never."""
    days = cfg(config).get("retake_after_days")
    first = math_path.subject(run.subject_id).main_floors[0].number
    if days is None or start_floor_of(run) != first or run.ended_at is None:
        return None
    return run.ended_at + dt.timedelta(days=days)


async def result_view(db: AsyncSession, run: MathRun) -> dict:
    """What a sitting found, floor by floor (the answers it really got), and where it put
    the player."""
    answers = await _results(db, run)
    by_floor: dict[int, list[bool]] = {}
    for a in answers:
        by_floor.setdefault(a.floor, []).append(bool(a.correct))
    start = start_floor_of(run)
    subject = math_path.subject(run.subject_id)
    slots = subject_plan(run.subject_id)
    planned = {}
    for s in slots:
        planned[s.floor] = planned.get(s.floor, 0) + 1
    floors = []
    for n in sorted(set(planned) | set(by_floor)):
        got = by_floor.get(n, [])
        p = planned.get(n, len(got))
        floors.append({"floor": n, "planned": p, "asked": len(got), "correct": sum(got), "needed": needed(p),
                       "met": len(got) >= p and sum(got) >= needed(p)})     # the bar, as answered
    retake = _retake_at(run)
    return {"start_floor": start, "abandoned": not run.passed,
            "skipped": [f.number for f in subject.main_floors if f.number < start],
            "asked": len(answers), "correct": sum(1 for a in answers if a.correct), "floors": floors,
            "finished_at": run.ended_at.isoformat(timespec="seconds") if run.ended_at else None,
            "retake_at": retake.isoformat(timespec="seconds") if retake else None}


async def progress(db: AsyncSession, run: MathRun) -> dict:
    """Where a sitting stands: questions asked of the plan and each floor's score."""
    slots = subject_plan(run.subject_id)
    results = [bool(a.correct) for a in await _results(db, run)]
    scores, start = score(slots, results)
    return {"total": len(slots), "asked": len(results), "correct": sum(results),
            "left": max(0, len(slots) - len(results)) if start is None else 0,
            "decided": start is not None, "start_floor": start,
            "floors": [s.view() for s in scores]}


def run_view(run: MathRun, prog: dict | None = None) -> dict:
    out = math_practice.run_view(run)
    if prog is not None:
        out["placement"] = {k: prog[k] for k in ("total", "asked", "correct", "left", "decided", "start_floor")}
    return out


async def state(db: AsyncSession, user: User, subject_id: str) -> dict:
    """GET /math/placement: is the test offered for this subject, going on, or done."""
    try:
        subject = math_path.subject(subject_id)
    except KeyError:
        raise MathError(404, "no_subject", "Không có bí cảnh này.")
    await _settle_all(db, user, subject_id)
    sittings = await _sittings(db, user.id, subject_id)
    going = next((r for r in sittings if r.ended_at is None), None)
    last = next((r for r in sittings if r.ended_at is not None), None)
    written = written_floors(subject_id)
    trials = await math_practice.trial_floors(db, user.id, subject_id)
    slots = subject_plan(subject_id)
    out = {"subject_id": subject_id, "subject_name_vi": subject.name_vi, "status": UNAVAILABLE,
           "offered": False, "reason": None, "planned": len(slots), "written_floors": written,
           "pass_pct": cfg()["pass_pct"], "run": None, "progress": None, "result": None}
    if last is not None:
        out["result"] = await result_view(db, last)
    if going is not None:
        prog = await progress(db, going)
        out.update(status=IN_PROGRESS, run=run_view(going, prog), progress=prog)
        return out
    if len(written) < 2:
        out["reason"] = "few_floors"
    elif trials:
        out["reason"] = "cleared"
    elif last is not None:
        retake = _retake_at(last)
        if retake is None or clock.now() < retake:
            out.update(status=DONE, reason="done")
            return out
        out.update(status=OFFERED, offered=True, reason="retake")
    else:
        out.update(status=OFFERED, offered=True)
    if out["result"] is not None and not out["offered"]:
        out["status"] = DONE
    return out


# ------------------------------------------------------------------ a sitting
async def start(db: AsyncSession, user: User, subject_id: str) -> dict:
    st = await state(db, user, subject_id)
    if not st["offered"]:
        why = {"few_floors": "Bí cảnh này chưa đủ tầng có câu hỏi để kiểm tra đầu vào.",
               "cleared": "Con đã qua Thiên kiếp nhỏ của một tầng ở bí cảnh này, không cần kiểm tra đầu vào nữa.",
               "done": "Con đã làm bài kiểm tra đầu vào của bí cảnh này rồi."}.get(
            st["reason"], "Bài kiểm tra đầu vào đang dở, hãy làm tiếp.")
        raise MathError(409, "placement_not_offered", why)
    first = subject_plan(subject_id)[0]
    # not math_practice._new_run: a placement sitting lives beside a buổi luyện and ends none
    run = MathRun(user_id=user.id, subject_id=subject_id, floor=first.floor, mode=PLACEMENT, tier=first.tier,
                  correct_streak=0, wrong_streak=0, combo=0, best_combo=0, asked=0, correct=0,
                  review_asked=0, xp_gained=0, passed=None, started_at=clock.now())
    db.add(run)
    await db.flush()
    prog = await progress(db, run)
    return {"run": run_view(run, prog), "progress": prog}


async def _own(db: AsyncSession, user: User, run_id: int) -> MathRun:
    run = (await db.execute(select(MathRun).where(MathRun.id == run_id).with_for_update())).scalar_one_or_none()
    if run is None or run.user_id != user.id or run.mode != PLACEMENT:
        raise MathError(404, "no_run", "Không tìm thấy bài kiểm tra này.")
    return run


async def _settle_expired(db: AsyncSession, user: User, run: MathRun) -> None:
    """A question of this sitting nobody answered in time is a wrong answer (a timeout)."""
    now = clock.now()
    for s in (await db.execute(select(QuizSession).where(
            QuizSession.user_id == user.id, QuizSession.context == CONTEXT, QuizSession.ref == str(run.id),
            QuizSession.answered_at.is_(None), QuizSession.expires_at <= now)
            .order_by(QuizSession.created_at))).scalars().all():
        s.answered_at, s.correct, s.answer, s.answer_ms = now, False, {"timed_out": True}, 0
        await _on_answer(db, user, s, False, now)


async def _settle_all(db: AsyncSession, user: User, subject_id: str) -> None:
    for run in (await db.execute(select(MathRun).where(
            MathRun.user_id == user.id, MathRun.subject_id == subject_id, MathRun.mode == PLACEMENT,
            MathRun.ended_at.is_(None)))).scalars().all():
        await _settle_expired(db, user, run)


def _question(subject_id: str, slot: Slot, seen_at: dict[str, int], rng: random.Random
              ) -> math_items.MathQuestion:
    """The question of one slot, at the slot's tier whatever the player's log says (rule 4's
    one exception, see the module docstring). Anti-repeat as everywhere else."""
    pool = [t for t in math_practice._templates(subject_id, slot.floor)
            if t.skill == slot.skill and t.tier == slot.tier]
    item = math_practice._pick(pool, seen_at, rng)
    if item is None:
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi phù hợp.")
    question = math_items.to_question(item, rng, math_path.cfg())
    question.meta["doc"] = math_practice.doc_link(item.skill)
    question.meta["placement"] = True
    return question


async def next_question(db: AsyncSession, user: User, run_id: int, rng: random.Random | None = None) -> dict:
    """The sitting's open question if it still has one, else the next one of the plan.
    `question` is None once the outcome is decided (the sitting is then over)."""
    run = await _own(db, user, run_id)
    if run.ended_at is not None:
        raise MathError(409, "run_ended", "Bài kiểm tra này đã kết thúc.")
    now = clock.now()
    pending = (await db.execute(select(QuizSession).where(
        QuizSession.user_id == user.id, QuizSession.context == CONTEXT, QuizSession.ref == str(run.id),
        QuizSession.answered_at.is_(None), QuizSession.expires_at > now)
        .order_by(QuizSession.created_at.desc()))).scalars().first()
    if pending is not None:
        prog = await progress(db, run)
        return {"run": run_view(run, prog), "question": quiz.public_session(pending), "progress": prog}
    await _settle_expired(db, user, run)
    prog = await progress(db, run)
    if run.ended_at is not None or prog["decided"]:
        await _finish(run, prog, now)
        return {"run": run_view(run, prog), "question": None, "progress": prog,
                "result": await result_view(db, run)}
    slot = subject_plan(run.subject_id)[prog["asked"]]
    rows = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user.id)
                             .order_by(MathAnswer.id.desc())
                             .limit(math_path.cfg()["anti_repeat_window"]))).scalars().all()
    seen_at = {fp: i for i, fp in reversed(list(enumerate(rows)))}
    question = _question(run.subject_id, slot, seen_at, rng or random.Random())
    run.floor, run.tier = slot.floor, slot.tier
    out = await quiz.create_session(db, user, CONTEXT, question, ref=str(run.id))
    return {"run": run_view(run, prog), "question": out, "progress": prog}


async def _finish(run: MathRun, prog: dict, now: dt.datetime) -> None:
    if run.ended_at is None and prog["decided"]:
        run.passed, run.floor, run.ended_at = True, prog["start_floor"], now


async def abandon(db: AsyncSession, user: User, run_id: int) -> dict:
    """Give a sitting up: the player starts on the first floor (see the module docstring)."""
    run = await _own(db, user, run_id)
    if run.ended_at is None:
        run.ended_at, run.passed = clock.now(), False
    return await state(db, user, run.subject_id)


# ------------------------------------------------------------------ after an answer
async def _on_answer(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    meta = s.payload["math"]
    timed_out = now > s.expires_at or bool(isinstance(s.answer, dict) and s.answer.get("timed_out"))
    run = None
    if s.ref:
        run = (await db.execute(select(MathRun).where(MathRun.id == int(s.ref))
                                .with_for_update())).scalar_one_or_none()
    db.add(MathAnswer(user_id=user.id, run_id=run.id if run else None, subject_id=meta["subject"],
                      skill_id=meta["skill"], floor=meta["floor"], tier=meta["tier"], item_id=s.item_id,
                      qtype=s.qtype, fingerprint=s.answer_key.get("fingerprint", ""), correct=correct,
                      timed_out=timed_out, review=False, answer_ms=s.answer_ms or 0, answered_at=now))
    await db.flush()
    out: dict = {"tier": meta["tier"], "timed_out": timed_out, "parallel": False, "parallel_waiting": False,
                 "review": False, "tier_change": 0,
                 "xp_base": math_path.xp_for_tier(meta["tier"]) if correct else 0}
    if run is not None and run.ended_at is None and run.user_id == user.id:
        run.asked += 1
        run.correct += int(correct)
        run.combo = run.combo + 1 if correct else 0
        run.best_combo = max(run.best_combo, run.combo)
        prog = await progress(db, run)
        await _finish(run, prog, now)
        out["placement"] = prog
        out["run"] = run_view(run, prog)
        if prog["decided"]:
            out["placement_result"] = await result_view(db, run)
    return out


async def placement_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool,
                            now: dt.datetime) -> dict:
    """Grading a placement question. No tâm ma, no adaptive tier, no cơ duyên: a test only
    measures (its Tu Vi is the usual Tu Vi of the tier)."""
    return {"math": await _on_answer(db, user, s, correct, now)}


def _xp_rule(s: QuizSession) -> int:
    return math_path.xp_for_tier(s.payload["math"]["tier"])


async def _on_xp(db: AsyncSession, s: QuizSession, gained: int) -> None:
    run = await db.get(MathRun, int(s.ref)) if s.ref else None
    if run is not None:
        run.xp_gained += int(gained)


quiz.register_handler(CONTEXT, placement_handler)
quiz.register_xp_rule(CONTEXT, _xp_rule, _on_xp)
