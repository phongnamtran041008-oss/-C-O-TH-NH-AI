"""Bài kiểm tra đầu vào: learning-path rule 7 (milestone M11; redesigned for nine written
floors in M11 đợt 2).

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

**What it asks: a climb in blocks.** M11 gave every written floor its own questions; with
nine written floors that leaves one or two questions a floor, so the sitting now climbs:

  * A *block* is `block` questions on one floor, tier by tier, lowest first (the odd one
    goes to the higher tier), the micro-skills of the floor taking turns in path order.
  * The climb starts on the first written floor. A block passed jumps `stride` written
    floors up (never past the last written floor). A block failed stops the climb; if the
    floor just below the failed one was jumped over, the sitting steps back to it to
    confirm, and so on down until it reaches a floor that was passed (or the first floor).
  * `block` and `stride` follow from the number of written floors `n`: the smallest stride,
    then the smallest block from `block_min` to `per_floor`, such that **every** possible
    sitting asks at most `max_questions` and a sitting answered all right asks at least
    `min_questions` (when no block can reach it, the largest that keeps the bound). So 3
    written floors: blocks of 4, every floor (12 questions all right); 6 floors: blocks of
    3, floors 1-3-5-6; 9 floors: blocks of 3, floors 1-4-7-9 - a beginner stops after one
    or two questions, a strong player reaches floor 9 in 12, and no sitting passes 15
    (`layout`, `walk`; the test file checks every pattern of passes and failures).
  * Each question is a real question of the shared quiz service (context `math_placement`,
    answered through `POST /quiz/answer`) with the normal time limit of its type and tier.
    A Thiên kiếp (`tribulation`, 8-12 minutes, a whole problem) is never a placement
    question. What comes next is a pure function of the path, the bank and the answers so
    far, so nothing about the plan is stored.

**Rule 4's exception.** Everywhere else a tier-N question of a micro-skill appears only
after right answers at tier N-1 (math_adaptive, math_ask.pick; the one other exception is a
ladder rung of rule 8, systems/math_practice.py). A placement question is asked at the tier
its slot says, whatever the player's log - that is what lets a strong player show it. So
this module picks its questions itself (`_question`). Its answers are real answers: they go
to `math_answers` with the placement sitting's `run_id`, so they count for the tiers the
player opens and for the mastery gate like any other answer, and an audit of rule 4 can
tell them apart (the run's `mode` is "placement").

**When a block is decided.** Its bar is `pass_pct` of its questions right (80% of 3 = 3, of
4 = 4, of 5 = 4). A block fails as soon as its bar can no longer be met (the rest of it is
not asked); a block whose bar is met is still asked to its end, hardest tier included. A
question whose time runs out is wrong (the client sends `{"timed_out": true}`; a question
nobody answered is settled as a timeout when the sitting next asks for one).

**The outcome.** The start floor is the lowest floor whose block failed; when the climb
passed the last written floor, that floor - never a floor without questions. The main floors
below the start floor count as **cleared by placement**, including floors the climb jumped
over (a passed floor above them vouches for them) and unwritten floors in between: every
part of a Đạo Thụ node on such a floor counts as passed (systems/math_tree_progress.py, the
legacy half of rule R2, which everything reads: the tree, path_view, and through the
frontier bí cảnh, hầm ngục, cơ duyên, thủ thành, chiêu thức). They are told
apart from floors cleared by a Thiên kiếp nhỏ in the path view (`cleared_by`). On the start
floor nothing is waived: its mastery gate and its Thiên kiếp nhỏ work exactly as for anyone.
The test itself still climbs whole floors, every micro-skill of a floor included.
(Should the bank change in the middle of a sitting so that a whole block no longer fits in
`max_questions`, the sitting ends on the lowest floor not yet passed - the cautious answer.)

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
NOT_ASKED = ("tribulation",)        # a Thiên kiếp (8-12 minutes) is never a placement question


def cfg(config: dict | None = None) -> dict:
    return (config or math_path.cfg())["placement_test"]


def askable(templates: list[Template]) -> list[Template]:
    """The templates a placement question may come from."""
    return [t for t in templates if t.qtype not in NOT_ASKED]


# ------------------------------------------------------------------ the climb (pure)
@dataclass(frozen=True)
class Slot:
    """One planned question: which floor, micro-skill and tier."""
    floor: int
    skill: str
    tier: int


def needed(planned: int, config: dict | None = None) -> int:
    """Right answers a block's bar wants out of its `planned` questions (80% of 5 = 4)."""
    return math.ceil(planned * cfg(config)["pass_pct"] / 100 - 1e-9)


def after_block(n: int, stride: int, i: int, ok: bool, passed: int, failed: int | None
                ) -> tuple[int | None, int | None, int, int | None]:
    """One step of the climb over `n` written floors (indices 0..n-1): block `i` was passed
    (`ok`) or failed; `passed` = highest index passed so far (-1: none), `failed` = lowest
    index failed (None: none). Returns (next index to ask, the start index once decided,
    passed, failed)."""
    if ok:
        passed = max(passed, i)
    else:
        failed = i if failed is None else min(failed, i)
    if failed is None:
        if i >= n - 1:
            return None, n - 1, passed, failed
        return min(i + stride, n - 1), None, passed, failed
    if failed - 1 <= passed:
        return None, failed, passed, failed
    return failed - 1, None, passed, failed           # step back to confirm a floor jumped over


def block_counts(n: int, stride: int) -> tuple[int, int]:
    """(the most blocks any sitting asks, the blocks of a sitting answered all right)."""
    def most(i: int, passed: int, failed: int | None) -> int:
        best = 0
        for ok in (True, False):
            nxt, _, p, f = after_block(n, stride, i, ok, passed, failed)
            best = max(best, 1 + (0 if nxt is None else most(nxt, p, f)))
        return best

    right, i, p, f = 0, 0, -1, None
    while i is not None:
        right += 1
        i, _, p, f = after_block(n, stride, i, True, p, f)
    return (most(0, -1, None), right) if n > 0 else (0, 0)


def shape(n: int, config: dict | None = None) -> tuple[int, int]:
    """(block, stride) for `n` written floors: see the module docstring."""
    p = cfg(config)
    least = p["block_min"]
    sizes = range(least, max(least, p["per_floor"]) + 1)
    fallback: tuple[int, int] | None = None
    for stride in range(1, max(1, n - 1) + 1):
        most, right = block_counts(n, stride)
        fits = [b for b in sizes if most * b <= p["max_questions"]]
        if fits:
            return next((b for b in fits if right * b >= p["min_questions"]), fits[-1]), stride
        if fallback is None or most < fallback[0]:
            fallback = (most, stride)
    return least, fallback[1] if fallback else 1


def block_slots(floor: math_path.Floor, temps: list[Template], size: int, config: dict | None = None
                ) -> tuple[Slot, ...]:
    """The `size` questions of one floor's block: tier by tier, lowest first (the odd one
    to the harder tier), the micro-skills taking turns in path order."""
    lo, hi = math_path.floor_tiers(floor.number, config)
    tiers = [t for t in range(lo, hi + 1) if any(x.tier == t for x in temps)]
    if not tiers:
        return ()
    base, extra = divmod(size, len(tiers))
    out, n = [], 0
    for i, tier in enumerate(tiers):
        k = base + (1 if i >= len(tiers) - extra else 0)
        skills = [s.id for s in floor.skills if any(x.skill == s.id and x.tier == tier for x in temps)]
        for _ in range(k):
            out.append(Slot(floor.number, skills[n % len(skills)], tier))
            n += 1
    return tuple(out)


@dataclass(frozen=True)
class Layout:
    """How a sitting of one subject climbs: the written floors, the block size, the stride,
    each floor's block (same order as `floors`) and the most questions any sitting asks."""
    floors: tuple[int, ...]
    block: int
    stride: int
    blocks: tuple[tuple[Slot, ...], ...]
    most: int


def layout(subject: math_path.Subject, templates_by_floor: dict[int, list[Template]],
           config: dict | None = None) -> Layout:
    """`templates_by_floor` = the question templates this server can ask, by floor (a floor
    without any placement-askable template is not written)."""
    config = config or math_path.cfg()
    floors = [f for f in subject.main_floors if askable(templates_by_floor.get(f.number) or [])]
    block, stride = shape(len(floors), config)
    blocks = tuple(block_slots(f, askable(templates_by_floor[f.number]), block, config) for f in floors)
    most = min(block_counts(len(floors), stride)[0] * block, cfg(config)["max_questions"])
    return Layout(tuple(f.number for f in floors), block, stride, blocks, most)


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


@dataclass(frozen=True)
class Walk:
    """Where a sitting stands: the blocks asked so far (in the order asked), the next
    question's slot (None once decided) and the start floor once decided."""
    scores: tuple[FloorScore, ...]
    next: Slot | None
    start: int | None


def walk(lay: Layout, results: list[bool], config: dict | None = None) -> Walk:
    """The climb after these answers (in the order they were given)."""
    n = len(lay.floors)
    if n == 0:
        return Walk((), None, None)
    need, limit = needed(lay.block, config), cfg(config)["max_questions"]
    i: int | None = 0
    passed, failed, pos, scores = -1, None, 0, []
    while True:
        asked = correct = 0
        for ok in results[pos:pos + lay.block]:
            asked, correct = asked + 1, correct + int(bool(ok))
            if FloorScore(lay.floors[i], lay.block, asked, correct, need).met is not None:
                break
        score = FloorScore(lay.floors[i], lay.block, asked, correct, need)
        scores.append(score)
        if score.met is None:
            return Walk(tuple(scores), lay.blocks[i][asked], None)
        pos += asked
        i, start, passed, failed = after_block(n, lay.stride, i, score.met, passed, failed)
        if start is not None:
            return Walk(tuple(scores), None, lay.floors[start])
        if pos + lay.block > limit:                     # (only when the bank changed mid-sitting)
            return Walk(tuple(scores), None, lay.floors[passed + 1])


# ------------------------------------------------------------------ reading the database
def _templates_by_floor(subject: math_path.Subject) -> dict[int, list[Template]]:
    return {f.number: askable(math_practice._templates(subject.id, f.number)) for f in subject.main_floors}


def written_floors(subject_id: str) -> list[int]:
    subject = math_path.subject(subject_id)
    return [f.number for f in subject.main_floors if askable(math_practice._templates(subject_id, f.number))]


def subject_layout(subject_id: str) -> Layout:
    subject = math_path.subject(subject_id)
    return layout(subject, _templates_by_floor(subject))


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
    """What a sitting found, floor by floor (the floors it really asked about, lowest
    first), and where it put the player."""
    answers = await _results(db, run)
    by_floor: dict[int, list[bool]] = {}
    for a in answers:
        by_floor.setdefault(a.floor, []).append(bool(a.correct))
    start = start_floor_of(run)
    subject = math_path.subject(run.subject_id)
    block = subject_layout(run.subject_id).block
    floors = []
    for n in sorted(by_floor):
        got = by_floor[n]
        p = max(block, len(got))
        floors.append({"floor": n, "planned": p, "asked": len(got), "correct": sum(got), "needed": needed(p),
                       "met": len(got) >= p and sum(got) >= needed(p)})     # the bar, as answered
    retake = _retake_at(run)
    return {"start_floor": start, "abandoned": not run.passed,
            "skipped": [f.number for f in subject.main_floors if f.number < start],
            "asked": len(answers), "correct": sum(1 for a in answers if a.correct), "floors": floors,
            "finished_at": run.ended_at.isoformat(timespec="seconds") if run.ended_at else None,
            "retake_at": retake.isoformat(timespec="seconds") if retake else None}


async def _walk(db: AsyncSession, run: MathRun) -> tuple[Layout, list[bool], Walk]:
    lay = subject_layout(run.subject_id)
    results = [bool(a.correct) for a in await _results(db, run)]
    return lay, results, walk(lay, results)


async def progress(db: AsyncSession, run: MathRun) -> dict:
    """Where a sitting stands: questions asked, the most it can still ask, each block's
    score."""
    lay, results, w = await _walk(db, run)
    return {"total": lay.most, "asked": len(results), "correct": sum(results),
            "left": max(0, lay.most - len(results)) if w.start is None else 0,
            "decided": w.start is not None, "start_floor": w.start,
            "block": lay.block, "stride": lay.stride,
            "floors": [s.view() for s in w.scores]}


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
    lay = subject_layout(subject_id)
    out = {"subject_id": subject_id, "subject_name_vi": subject.name_vi, "status": UNAVAILABLE,
           "offered": False, "reason": None, "planned": lay.most, "written_floors": written,
           "block": lay.block, "stride": lay.stride,
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
    first = walk(subject_layout(subject_id), []).next
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
    exception, see the module docstring). Anti-repeat as everywhere else; never a Thiên kiếp."""
    pool = [t for t in askable(math_practice._templates(subject_id, slot.floor))
            if t.skill == slot.skill and t.tier == slot.tier]
    item = math_practice._pick(pool, seen_at, rng)
    if item is None:
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi phù hợp.")
    question = math_items.to_question(item, rng, math_path.cfg())
    question.meta["doc"] = math_practice.doc_link(item.skill)
    question.meta["placement"] = True
    return question


async def next_question(db: AsyncSession, user: User, run_id: int, rng: random.Random | None = None) -> dict:
    """The sitting's open question if it still has one, else the next one of the climb.
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
    slot = (await _walk(db, run))[2].next
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
    """Grading a placement question. No tâm ma, no ladder, no adaptive tier, no cơ duyên: a
    test only measures (its Tu Vi is the usual Tu Vi of the tier)."""
    return {"math": await _on_answer(db, user, s, correct, now)}


def _xp_rule(s: QuizSession) -> int:
    return math_path.xp_for_tier(s.payload["math"]["tier"])


async def _on_xp(db: AsyncSession, s: QuizSession, gained: int) -> None:
    run = await db.get(MathRun, int(s.ref)) if s.ref else None
    if run is not None:
        run.xp_gained += int(gained)


quiz.register_handler(CONTEXT, placement_handler)
quiz.register_xp_rule(CONTEXT, _xp_rule, _on_xp)
