"""The math question loop: a player sits down on a floor of a math subject and answers
one question after another.

A sitting is a MathRun. `next_question` picks a template (a hand-written item or a
generator), turns it into a question and opens it through the shared quiz service
(context "math"), so the countdown, the grading and the answer key work like every other
question and the client answers through /quiz/answer. The handler below then logs the
answer (MathAnswer), moves the tier (learning-path rules 2 and 3,
learning/math_adaptive.py) and Tu Vi is paid by tier (balance/math.json).

Anti-repeat (M3): a question whose fingerprint (micro-skill + template + numbers) is among
the player's last `anti_repeat_window` answers is not asked again while anything else is
left, and a template asked within the last `template_cooldown` answers waits its turn.

Rule 6, "tâm ma" (M3): a wrong answer is remembered (MathRetry). Once `after_answers`
other questions have been answered, the same idea comes back: the same generator with
new numbers, or for a hand-written item another template of the same micro-skill and
tier. A right answer to that parallel question clears the mistake; a wrong one keeps it.

Leaving a floor (M5, rules 3 and 6; the rules themselves are in learning/math_mastery.py):

  * floor 1 of a subject is open, and a floor opens when the floor below it is cleared;
  * a floor is cleared by passing its own test, the Thiên kiếp nhỏ - a sitting with
    `mode == "trial"`, one question per micro-skill at the hardest tier of the floor;
  * that test can only be started once every micro-skill of the floor is through the
    mastery gate (half (a) of rule 3), which is read from the answer log;
  * an ordinary sitting mixes in **spiral review**: every fourth question or so comes from
    a micro-skill of a floor below, chosen by the spaced-repetition schedule.

So one question of a sitting is chosen in this order: the parallel question of a mistake
that has waited long enough (rule 6a), then a review question when the sitting is due one
(rule 6b), then the ordinary next question of this floor (rules 2 and 3).
"""
from __future__ import annotations

import datetime as dt
import random

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import settings
from ..learning import (math_adaptive, math_items, math_library, math_mastery, math_path,
                        math_problems, quiz)
from ..learning.math_items import GeneratorSpec, MathItem, Template
from ..models import MathAnswer, MathRetry, MathRun, QuizSession, User

CONTEXT = "math"
PRACTICE, TRIAL = "practice", "trial"
DRAW_TRIES = 30         # draws of one generator before giving up on finding numbers not seen lately
REVIEW_SCAN = 4         # times the gate window: how far back the review schedule reads the log


class MathError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ views
def _templates(subject_id: str, floor: int) -> list[Template]:
    return math_items.floor_templates(subject_id, floor, settings.allow_unreviewed)


def run_view(run: MathRun) -> dict:
    lo, hi = math_path.floor_tiers(run.floor)
    out = {"run_id": run.id, "subject_id": run.subject_id, "floor": run.floor, "mode": run.mode,
           "tier": run.tier, "tier_name_vi": math_path.cfg()["tiers"][str(run.tier)]["name_vi"],
           "tier_min": lo, "tier_max": hi, "combo": run.combo, "best_combo": run.best_combo,
           "asked": run.asked, "correct": run.correct, "review_asked": run.review_asked,
           "xp_gained": run.xp_gained, "passed": run.passed, "ended": run.ended_at is not None}
    if run.mode == TRIAL:
        total = math_mastery.trial_total(math_path.subject(run.subject_id), run.floor)
        out["trial"] = {"total": total, "left": max(0, total - run.asked),
                        "wrong": run.asked - run.correct,
                        "max_wrong": math_mastery.trial_cfg()["max_wrong"]}
    return out


async def open_run(db: AsyncSession, user_id: int) -> MathRun | None:
    return (await db.execute(select(MathRun).where(MathRun.user_id == user_id, MathRun.ended_at.is_(None))
                             .order_by(MathRun.id.desc()))).scalars().first()


async def cleared_floors(db: AsyncSession, user_id: int, subject_id: str) -> set[int]:
    """The floors of this subject whose Thiên kiếp nhỏ the player has passed."""
    rows = (await db.execute(select(MathRun.floor).where(
        MathRun.user_id == user_id, MathRun.subject_id == subject_id,
        MathRun.mode == TRIAL, MathRun.passed.is_(True)).distinct())).scalars().all()
    return set(rows)


async def floor_gate(db: AsyncSession, user_id: int, subject: math_path.Subject, floor: int,
                     config: dict | None = None) -> math_mastery.FloorGate:
    """Half (a) of the mastery gate for one floor, read from the answer log."""
    config = config or math_path.cfg()
    skills = [s.id for s in subject.floor(floor).skills]
    results = await _results_by_skill(db, user_id, skills, floor,
                                      max(config["mastery_gate"]["window"], config["tier_unlock"]["window"]),
                                      include_top=True)
    return math_mastery.floor_gate(floor, skills, results, config)


async def path_view(db: AsyncSession, user: User) -> dict:
    """The subjects and floors, how many question templates each floor has for this server
    (hand-written items + generators), which floors are open or cleared and how far the
    mastery gate of each open floor has come, and the sitting the player left open (if any)."""
    cfg = math_path.cfg()
    subjects = []
    for s in math_path.subjects():
        cleared = await cleared_floors(db, user.id, s.id)
        floors = []
        for f in s.floors:
            lo, hi = math_path.floor_tiers(f.number)
            templates = _templates(s.id, f.number)
            docs = math_library.for_floor(s.id, f.number)
            state = math_mastery.floor_state(s, f.number, cleared)
            gate = None
            if templates and state != math_mastery.LOCKED:
                gate = (await floor_gate(db, user.id, s, f.number, cfg)).view()
            floors.append({"floor": f.number, "title_vi": f.title_vi, "hidden": f.hidden,
                           "tier_min": lo, "tier_max": hi, "questions": len(templates),
                           "generators": sum(1 for t in templates if t.generated),
                           "playable": bool(templates) and state != math_mastery.LOCKED,
                           "has_questions": bool(templates), "state": state, "gate": gate,
                           "trial_total": math_mastery.trial_total(s, f.number, cfg),
                           "doc_id": docs[0].id if docs else None,
                           "skills": [{"id": k.id, "name_vi": k.name_vi} for k in f.skills]})
        playable_floors = {f["floor"] for f in floors if f["playable"]}
        subjects.append({"id": s.id, "name_vi": s.name_vi, "order": s.order, "floors": floors,
                         "cleared": sorted(cleared), "next_floor": math_mastery.next_floor(s, cleared),
                         # how many programming exercises the player may open right now (M6)
                         "problems": sum(len(math_problems.floor_problems(s.id, n, settings.allow_unreviewed))
                                         for n in playable_floors)})
    run = await open_run(db, user.id)
    return {"subjects": subjects, "run": run_view(run) if run else None,
            "tiers": {t: v["name_vi"] for t, v in cfg["tiers"].items() if not t.startswith("_")}}


def doc_link(skill_id: str) -> dict | None:
    """Where the library explains this micro-skill, for the answer card to point at."""
    doc = math_library.for_skill(skill_id)
    if doc is None:
        return None
    return {"id": doc.id, "title_vi": doc.title_vi, "block": doc.section_of(skill_id)}


def library_view() -> dict:
    """Every document the game ships, in reading order."""
    subjects = []
    for s in math_path.subjects():
        docs = [d for d in math_library.documents().values() if d.subject == s.id]
        if docs:
            subjects.append({"id": s.id, "name_vi": s.name_vi, "order": s.order, "documents": [
                {"id": d.id, "title_vi": d.title_vi, "floor": d.floor, "summary_vi": d.summary_vi,
                 "skills": list(d.skills), "sections": [b["title_vi"] for b in d.blocks if b["type"] == "section"]}
                for d in sorted(docs, key=lambda d: d.floor)]})
    return {"subjects": subjects}


# ------------------------------------------------------------------ a sitting
async def _open_floor(db: AsyncSession, user: User, subject_id: str, floor: int) -> math_path.Subject:
    """The subject, once this floor is known, has questions and is not locked (M5)."""
    try:
        subject = math_path.subject(subject_id)
        subject.floor(floor)
    except KeyError:
        raise MathError(404, "no_floor", "Không có tầng này.")
    if not _templates(subject_id, floor):
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    cleared = await cleared_floors(db, user.id, subject_id)
    if not math_mastery.playable(subject, floor, cleared):
        below = math_mastery.floor_below(subject, floor)
        raise MathError(403, "floor_locked",
                        f"Tầng này chưa mở. Hãy qua Thiên kiếp nhỏ của tầng {below} trước.")
    return subject


async def _new_run(db: AsyncSession, user: User, subject_id: str, floor: int, mode: str, tier: int) -> MathRun:
    now = clock.now()
    for old in (await db.execute(select(MathRun).where(MathRun.user_id == user.id,
                                                       MathRun.ended_at.is_(None)))).scalars():
        old.ended_at = now          # one sitting at a time
    run = MathRun(user_id=user.id, subject_id=subject_id, floor=floor, mode=mode, tier=tier,
                  correct_streak=0, wrong_streak=0, combo=0, best_combo=0, asked=0, correct=0,
                  review_asked=0, xp_gained=0, passed=None, started_at=now)
    db.add(run)
    await db.flush()
    return run


async def start(db: AsyncSession, user: User, subject_id: str, floor: int) -> dict:
    await _open_floor(db, user, subject_id, floor)
    run = await _new_run(db, user, subject_id, floor, PRACTICE, math_adaptive.start(floor).tier)
    return {"run": run_view(run)}


async def start_trial(db: AsyncSession, user: User, subject_id: str, floor: int) -> dict:
    """The Thiên kiếp nhỏ of a floor (rule 3b). It opens only when every micro-skill of the
    floor is through the mastery gate; a failed trial can be taken again straight away."""
    subject = await _open_floor(db, user, subject_id, floor)
    gate = await floor_gate(db, user.id, subject, floor)
    if not gate.ok:
        names = ", ".join(subject.skills[s.skill_id].name_vi for s in gate.weak)
        raise MathError(409, "gate_not_met", f"Chưa đủ thuần thục để vượt Thiên kiếp nhỏ. Hãy ôn: {names}.")
    run = await _new_run(db, user, subject_id, floor, TRIAL, math_mastery.trial_tier(floor))
    return {"run": run_view(run), "gate": gate.view()}


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
                            window: int, include_top: bool = False) -> dict[str, dict[int, list[bool]]]:
    """skill -> tier -> the player's last `window` answers at that tier, oldest first. Only
    the tiers that can open a higher tier of this floor are read, plus the highest tier of
    the floor when the mastery gate is being read (`include_top`)."""
    out: dict[str, dict[int, list[bool]]] = {s: {} for s in skill_ids}
    lo, hi = math_path.floor_tiers(floor)
    for skill in skill_ids:
        for tier in range(lo, hi + 1 if include_top else hi):
            rows = (await db.execute(
                select(MathAnswer.correct).where(MathAnswer.user_id == user_id, MathAnswer.skill_id == skill,
                                                 MathAnswer.tier == tier)
                .order_by(MathAnswer.id.desc()).limit(window))).scalars().all()
            if rows:
                out[skill][tier] = list(reversed(rows))
    return out


async def _review_stats(db: AsyncSession, user_id: int, subject_id: str, floor: int,
                        config: dict) -> list[math_mastery.ReviewStat]:
    """Every micro-skill of a floor *below* this one that has questions, as the spaced
    repetition schedule sees it. One pass over the end of the answer log: a micro-skill that
    is not in it at all was answered so long ago that it is due anyway."""
    subject = math_path.subject(subject_id)
    where: dict[str, int] = {}
    for f in subject.floors:
        if f.hidden or f.number >= floor or not _templates(subject_id, f.number):
            continue
        for s in f.skills:
            where[s.id] = f.number
    if not where:
        return []
    window = config["mastery_gate"]["window"]
    rows = (await db.execute(
        select(MathAnswer.skill_id, MathAnswer.correct, MathAnswer.answered_at)
        .where(MathAnswer.user_id == user_id, MathAnswer.skill_id.in_(list(where)))
        .order_by(MathAnswer.id.desc()).limit(len(where) * window * REVIEW_SCAN))).all()
    latest: dict[str, list[tuple[bool, dt.datetime]]] = {}
    for skill_id, correct, at in rows:                      # newest first
        latest.setdefault(skill_id, []).append((bool(correct), at))
    stats = []
    for skill_id, floor_no in where.items():
        mine = latest.get(skill_id, [])
        streak = 0
        for ok, _ in mine:
            if not ok:
                break
            streak += 1
        stats.append(math_mastery.ReviewStat(
            skill_id=skill_id, floor=floor_no, last_answered=mine[0][1] if mine else None,
            streak=streak, recent=tuple(ok for ok, _ in reversed(mine[:window]))))
    return stats


# ------------------------------------------------------------------ choosing the question
def _fresh(template: Template, seen: dict[str, int] | set[str], rng: random.Random) -> MathItem | None:
    """This template as a question the player has not seen lately, or None: a hand-written
    item that is inside the window, or a generator that keeps drawing numbers seen lately."""
    if isinstance(template, MathItem):
        return None if template.fingerprint in seen else template
    for _ in range(DRAW_TRIES):
        item = math_items.draw(template, rng)
        if item.fingerprint not in seen:
            return item
    return None


def choose_item(templates: list[Template], run_tier: int, floor: int,
                results: dict[str, dict[int, list[bool]]], recent: list[str],
                rng: random.Random, recent_templates: list[str] | tuple = (),
                cooldown: int | None = None) -> MathItem:
    """The next question of a sitting. `recent` = fingerprints of the player's latest
    answers and `recent_templates` = the template ids of those answers, both newest first.

    A micro-skill is drawn first, then one of its templates at the tier that skill may be
    asked at (math_adaptive.question_tier); when it has none at that tier, the nearest
    lower tier that has one, else the nearest higher tier that is open. In order of
    preference: a question not seen inside the anti-repeat window from a template not asked
    in the last `cooldown` answers; any question not seen inside the window; a generator
    (its numbers repeat, nothing else is left); the hand-written item seen longest ago."""
    cooldown = math_path.cfg()["template_cooldown"] if cooldown is None else cooldown
    by_skill: dict[str, list[Template]] = {}
    for t in templates:
        by_skill.setdefault(t.skill, []).append(t)
    lo, _ = math_path.floor_tiers(floor)
    pools: list[list[Template]] = []
    for skill, own in sorted(by_skill.items()):
        by_tier = results.get(skill, {})
        want = math_adaptive.question_tier(run_tier, floor, by_tier)
        top = math_adaptive.open_tier(floor, by_tier)
        tiers = sorted({t.tier for t in own})
        usable = ([t for t in reversed(tiers) if lo <= t <= want]
                  or [t for t in tiers if want < t <= top])
        if usable:
            pools.append(sorted((t for t in own if t.tier == usable[0]), key=lambda t: t.id))
    if not pools:
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi phù hợp.")
    seen_at = {fp: i for i, fp in reversed(list(enumerate(recent)))}      # fingerprint -> how recent (0 = newest)
    resting = set(list(recent_templates)[:cooldown])
    fresh = [[(t, item) for t in pool if (item := _fresh(t, seen_at, rng)) is not None] for pool in pools]
    rested = [[c for c in pool if c[0].id not in resting] for pool in fresh]
    for candidates in (rested, fresh):
        candidates = [pool for pool in candidates if pool]
        if candidates:
            return rng.choice(rng.choice(candidates))[1]
    generators = [t for pool in pools for t in pool if isinstance(t, GeneratorSpec)]
    if generators:
        return math_items.draw(rng.choice(generators), rng)
    return max((t for pool in pools for t in pool), key=lambda t: (seen_at[t.fingerprint], t.id))


def parallel_item(templates: list[Template], retry: MathRetry, recent: list[str],
                  rng: random.Random) -> MathItem | None:
    """The question that comes back after a mistake: the same idea with new numbers.
    A generator is drawn again (never the question that was missed); a hand-written item is
    replaced by another template of the same micro-skill and tier, and comes back itself
    only when it is the only one. None when the floor no longer has that micro-skill."""
    seen = set(recent) | {retry.fingerprint}
    same = next((t for t in templates if t.id == retry.item_id), None)
    if isinstance(same, GeneratorSpec):
        return _fresh(same, seen, rng) or _fresh(same, {retry.fingerprint}, rng) or math_items.draw(same, rng)
    others = [t for t in templates if t.skill == retry.skill_id and t.tier == retry.tier and t.id != retry.item_id]
    rng.shuffle(others)
    others.sort(key=lambda t: not isinstance(t, GeneratorSpec))       # new numbers first
    for wanted in (seen, {retry.fingerprint}):
        for t in others:
            item = _fresh(t, wanted, rng)
            if item is not None:
                return item
    return same


def _pick(pool: list[Template], seen_at: dict[str, int], rng: random.Random) -> MathItem | None:
    """One question from this pool, in the same order of preference as choose_item: a
    question not seen inside the anti-repeat window, else a new draw of a generator, else
    the hand-written item seen longest ago."""
    fresh = [item for t in pool if (item := _fresh(t, seen_at, rng)) is not None]
    if fresh:
        return rng.choice(fresh)
    generators = [t for t in pool if isinstance(t, GeneratorSpec)]
    if generators:
        return math_items.draw(rng.choice(generators), rng)
    items = [t for t in pool if isinstance(t, MathItem)]
    return max(items, key=lambda t: (seen_at.get(t.fingerprint, -1), t.id)) if items else None


def _at_tier(templates: list[Template], skill_id: str, tier: int) -> list[Template]:
    """The templates of this micro-skill at `tier`, or at the nearest tier below it that has
    any; empty when the micro-skill has no template at all."""
    mine = [t for t in templates if t.skill == skill_id]
    below = [t for t in sorted({x.tier for x in mine}) if t <= tier]
    return [t for t in mine if t.tier == below[-1]] if below else []


async def _review_item(db: AsyncSession, user_id: int, run: MathRun,
                       stats: list[math_mastery.ReviewStat], recent: list[str],
                       rng: random.Random, config: dict) -> MathItem | None:
    """A question from a floor below this one (rule 6b): the micro-skill that is due and has
    been answered worst lately, at the highest tier open for it on its own floor."""
    seen_at = {fp: i for i, fp in reversed(list(enumerate(recent)))}
    for stat in math_mastery.review_queue(stats, clock.now(), config):
        templates = _templates(run.subject_id, stat.floor)
        results = await _results_by_skill(db, user_id, [stat.skill_id], stat.floor,
                                          config["tier_unlock"]["window"])
        top = math_adaptive.open_tier(stat.floor, results.get(stat.skill_id, {}), config)
        item = _pick(_at_tier(templates, stat.skill_id, top), seen_at, rng)
        if item is not None:
            return item
    return None


async def _trial_item(db: AsyncSession, run: MathRun, recent: list[str], rng: random.Random,
                      config: dict) -> MathItem:
    """The next question of a Thiên kiếp nhỏ: the next micro-skill of the floor this trial
    has not asked about yet, at the hardest tier of the floor."""
    subject = math_path.subject(run.subject_id)
    left = math_mastery.trial_skills(subject, run.floor, config)
    for skill_id in (await db.execute(select(MathAnswer.skill_id).where(MathAnswer.run_id == run.id)
                                      .order_by(MathAnswer.id))).scalars().all():
        if skill_id in left:
            left.remove(skill_id)
    if not left:
        raise MathError(409, "trial_done", "Thiên kiếp nhỏ này đã xong.")
    pool = _at_tier(_templates(run.subject_id, run.floor), left[0],
                    math_mastery.trial_tier(run.floor, config))
    item = _pick(pool, {fp: i for i, fp in reversed(list(enumerate(recent)))}, rng)
    if item is None:
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi phù hợp.")
    return item


async def _due_retry(db: AsyncSession, user_id: int, run: MathRun) -> MathRetry | None:
    """The oldest open mistake of this floor that has waited long enough."""
    wait = math_path.cfg()["parallel_question"]["after_answers"]
    retries = (await db.execute(select(MathRetry).where(
        MathRetry.user_id == user_id, MathRetry.subject_id == run.subject_id, MathRetry.floor == run.floor,
        MathRetry.cleared_at.is_(None)).order_by(MathRetry.id))).scalars().all()
    for retry in retries:
        since = (await db.execute(select(func.count()).select_from(MathAnswer).where(
            MathAnswer.user_id == user_id, MathAnswer.id > retry.after_answer_id))).scalar_one()
        if since >= wait:
            return retry
    return None


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
    templates = _templates(run.subject_id, run.floor)
    rows = (await db.execute(select(MathAnswer.fingerprint, MathAnswer.item_id).where(MathAnswer.user_id == user.id)
                             .order_by(MathAnswer.id.desc()).limit(cfg["anti_repeat_window"]))).all()
    recent = [r[0] for r in rows]
    rng = rng or random.Random()
    item, retry, review = None, None, False
    if run.mode == TRIAL:
        item = await _trial_item(db, run, recent, rng, cfg)
    else:
        retry = await _due_retry(db, user.id, run)
        if retry is not None:
            item = parallel_item(templates, retry, recent, rng)
            if item is None:                # its micro-skill has no question any more
                retry.cleared_at, retry = now, None
        if item is None and math_mastery.wants_review(run.asked, run.review_asked, cfg):
            stats = await _review_stats(db, user.id, run.subject_id, run.floor, cfg)
            item = await _review_item(db, user.id, run, stats, recent, rng, cfg)
            review = item is not None       # no floor below, or nothing due: an ordinary question
        if item is None:
            skills = sorted({t.skill for t in templates})
            results = await _results_by_skill(db, user.id, skills, run.floor, cfg["tier_unlock"]["window"])
            item = choose_item(templates, run.tier, run.floor, results, recent, rng, [r[1] for r in rows])
    question = math_items.to_question(item, rng, cfg, parallel=retry is not None, review=review)
    question.meta["doc"] = doc_link(item.skill)          # "Đọc Tàng Thư" on the answer card
    if retry is not None:
        question.answer_key["retry_id"] = retry.id
    out = await quiz.create_session(db, user, CONTEXT, question, ref=str(run.id))
    return {"run": run_view(run), "question": out}


# ------------------------------------------------------------------ after an answer
async def _remember_mistake(db: AsyncSession, user_id: int, s: QuizSession, meta: dict,
                            answer: MathAnswer, correct: bool, now: dt.datetime) -> bool:
    """Rule 6 bookkeeping. Returns True when a parallel question is now waiting."""
    retry_id = s.answer_key.get("retry_id")
    fingerprint = s.answer_key.get("fingerprint", "")
    if retry_id is not None:
        retry = await db.get(MathRetry, retry_id)
        if retry is None or retry.cleared_at is not None or retry.user_id != user_id:
            return False
        if correct:
            retry.cleared_at = now
            return False
        retry.after_answer_id, retry.fingerprint, retry.misses = answer.id, fingerprint, retry.misses + 1
        return True
    if correct:
        return False
    open_ = (await db.execute(select(MathRetry).where(
        MathRetry.user_id == user_id, MathRetry.subject_id == meta["subject"], MathRetry.floor == meta["floor"],
        MathRetry.cleared_at.is_(None)).order_by(MathRetry.id))).scalars().all()
    same = next((r for r in open_ if r.item_id == s.item_id), None)
    if same is not None:
        same.after_answer_id, same.fingerprint, same.misses = answer.id, fingerprint, same.misses + 1
        return True
    db.add(MathRetry(user_id=user_id, subject_id=meta["subject"], floor=meta["floor"], skill_id=meta["skill"],
                     tier=meta["tier"], item_id=s.item_id, fingerprint=fingerprint,
                     after_answer_id=answer.id, misses=1, created_at=now))
    keep = math_path.cfg()["parallel_question"]["max_open"] - 1
    for old in open_[:max(0, len(open_) - keep)]:       # the queue is short: the oldest mistakes are let go
        old.cleared_at = now
    return True


async def math_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    meta = s.payload["math"]
    # the server's clock ran out, or the client's countdown did (it then sends {"timed_out": true})
    timed_out = now > s.expires_at or bool(isinstance(s.answer, dict) and s.answer.get("timed_out"))
    run = None
    if s.ref:
        run = (await db.execute(select(MathRun).where(MathRun.id == int(s.ref))
                                .with_for_update())).scalar_one_or_none()
    review = bool(meta.get("review"))
    answer = MathAnswer(user_id=user.id, run_id=run.id if run else None, subject_id=meta["subject"],
                        skill_id=meta["skill"], floor=meta["floor"], tier=meta["tier"], item_id=s.item_id,
                        qtype=s.qtype, fingerprint=s.answer_key.get("fingerprint", ""), correct=correct,
                        timed_out=timed_out, review=review, answer_ms=s.answer_ms or 0, answered_at=now)
    db.add(answer)
    await db.flush()                      # the mistake queue counts answers by their id
    trial = run is not None and run.mode == TRIAL
    waiting = False if trial else await _remember_mistake(db, user.id, s, meta, answer, correct, now)
    out: dict = {"tier": meta["tier"], "timed_out": timed_out, "parallel": bool(meta.get("parallel")),
                 "parallel_waiting": waiting, "review": review,
                 "xp_base": math_path.xp_for_tier(meta["tier"]) if correct else 0}
    if run is not None and run.ended_at is None and run.user_id == user.id:
        before = run.tier
        if not trial:                       # the tier of a trial is the floor's hardest, all the way
            state = math_adaptive.after_answer(
                math_adaptive.TierState(run.tier, run.correct_streak, run.wrong_streak), correct, run.floor)
            run.tier, run.correct_streak, run.wrong_streak = state.tier, state.correct_streak, state.wrong_streak
        run.asked += 1
        run.correct += int(correct)
        run.review_asked += int(review)
        run.combo = run.combo + 1 if correct else 0      # a wrong answer or a timeout ends the combo
        run.best_combo = max(run.best_combo, run.combo)
        if trial:
            out["trial"] = _trial_after_answer(run, now)
        out.update(run=run_view(run), tier_change=run.tier - before)
    return {"math": out}


def _trial_after_answer(run: MathRun, now: dt.datetime) -> dict:
    """Where a Thiên kiếp nhỏ stands after one answer, and the floor it opens when passed.
    **Ends the run** as soon as the trial is won or lost, so nobody has to finish a trial
    they cannot pass any more."""
    subject = math_path.subject(run.subject_id)
    total = math_mastery.trial_total(subject, run.floor)
    verdict = math_mastery.trial_verdict(run.asked, run.correct, total)
    out = {"total": total, "asked": run.asked, "correct": run.correct,
           "left": max(0, total - run.asked), "passed": verdict, "unlocked": None}
    if verdict is None:
        return out
    run.passed, run.ended_at = verdict, now
    if verdict:
        out["unlocked"] = math_mastery.floor_above(subject, run.floor)
    return out


def _xp_rule(s: QuizSession) -> int:
    return math_path.xp_for_tier(s.payload["math"]["tier"])


async def _on_xp(db: AsyncSession, s: QuizSession, gained: int) -> None:
    run = await db.get(MathRun, int(s.ref)) if s.ref else None
    if run is not None:
        run.xp_gained += int(gained)


quiz.register_handler(CONTEXT, math_handler)
quiz.register_grader(math_items.PLAYABLE_TYPES, math_items.grade)
quiz.register_xp_rule(CONTEXT, _xp_rule, _on_xp)
