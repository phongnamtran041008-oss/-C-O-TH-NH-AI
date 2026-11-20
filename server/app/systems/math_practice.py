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

Đạo Thụ (the curriculum tree, systems/math_tree_progress.py) decides what is open. A sitting
is on one **part** of a tree node - the node's micro-skills that live on the sitting's floor
(`MathRun.node_id`); every rule below runs on the part's micro-skills, not the whole floor.
A sitting with no node is an old save and keeps the whole floor.

Leaving a part (M5, rules 3 and 6; the rules themselves are in learning/math_mastery.py):

  * a node opens when every node it requires is done (math_tree_progress, R3/R4); the old
    entry points "sit down on floor n" resolve to the open part on that floor (R11);
  * a part is passed by its own test, the Thiên kiếp nhỏ - a sitting with `mode == "trial"`,
    one question per micro-skill of the part at the hardest tier of the floor - or, for a
    whole floor, by an old passed trial or the bài kiểm tra đầu vào (M11,
    systems/math_placement.py);
  * that test can only be started once every micro-skill of the part is through the
    mastery gate (half (a) of rule 3), which is read from the answer log;
  * an ordinary sitting mixes in **spiral review**: every fourth question or so comes from
    a micro-skill of the nodes this node `reinforces` (any subject; if none has questions,
    its done ancestors), chosen by the spaced-repetition schedule. An old sitting with no
    node reviews the floors below, as before.
  * no mode ever asks a micro-skill of the tree's `cut` list (`_templates` drops them), and
    a sitting asks nothing outside its part except review, ladder rungs and the parallel
    question of a missed rung.

Rule 8, the ladder (M11 đợt 2): "Bài khó luôn có bậc thang". Every hand-written tier-5 item
lists 2-4 tier 3-4 questions that lead to it (`ladder`, learning/math_items.py).

  * A tier-5 hand-written question answered wrong in a buổi luyện (or left to time out)
    opens a ladder (MathLadder, kept in the database: closing the game mid-ladder loses
    nothing). The next questions of the sittings of that floor are exactly its rungs, in
    order, before anything else: a hand-written rung as it is (even if seen lately), a
    generator rung as one fresh draw. A rung id that is no longer in the bank is passed by.
    A tier-5 generator has no ladder (only hand-written items have one), so missing one
    opens nothing beyond rule 6.
  * A rung answered wrong is an ordinary wrong answer: rule 6 remembers it - keyed to the
    floor of the sitting, so its parallel question comes back in this sitting even when the
    rung lives on a floor below. The remaining rungs still come: the ladder is the teaching.
  * Rules 6 and 8 together: the tier-5 mistake is remembered by rule 6 as always, but its
    parallel question is *held* while its ladder is being climbed. Climbed with every rung
    right, the hold ends and that parallel question is the very next one (it goes ahead of
    other waiting mistakes): the same generator with new numbers, or another tier-5 template
    of the micro-skill (the same item only when it is the only one). Climbed with a rung
    missed, the tier-5 idea does not come back in this sitting: the missed rungs' own
    parallel questions come first, and the tier-5 one waits for the next sitting.
  * At most one ladder is being climbed per part (per floor for an old sitting with no node:
    a ladder belongs to the part whose micro-skill opened it), and a tier-5 item opens a ladder at most
    once per sitting (a second miss of it in the same sitting is plain rule 6), so ladders
    and parallel questions can never chase each other for ever.
  * Rungs do not move the sitting's adaptive tier (they are below the floor's range when
    they come from a floor below); they are logged and paid like any answer.
  * Only a buổi luyện opens a ladder. A Thiên kiếp nhỏ, the placement test, a chiêu, a
    monster, a dungeon room, the tower, cơ duyên: none, and none is stored for later - like
    rule 6 since M7, those have no sitting to come back into, and a tier-5 question there
    was not part of the player's own climb.

  Rule 4 and the ladder. A rung is tier 3 or 4 on the item's floor or below. A player asked
  tier 5 has opened those tiers in the ordinary course - except a player placed high by the
  bài kiểm tra đầu vào, and anyone on floor 9, whose lowest tier is 5 and so always open.
  For them a rung may be a tier the log has not opened: that is the point (the step they are
  missing), and it is the second stated exception to rule 4 after the placement test. No
  other path here asks above the player's tier: an ordinary question is capped by
  math_adaptive.question_tier, a review question by the open tier of its own floor, and a
  parallel question repeats a tier the player was already asked at.

So one question of a sitting is chosen in this order: the next rung of a ladder being
climbed on this floor (rule 8), then the parallel question of a mistake that has waited long
enough (rule 6a; a mistake held by its ladder waits, one released by a clean climb goes
first), then a review question when the sitting is due one (rule 6b), then the ordinary next
question of this floor (rules 2 and 3).
"""
from __future__ import annotations

import datetime as dt
import random

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import settings
from ..learning import (math_adaptive, math_items, math_library, math_mastery, math_path,
                        math_problems, math_tree, quiz)
from ..learning.math_items import GeneratorSpec, MathItem, Template
from ..models import MathAnswer, MathLadder, MathRetry, MathRun, QuizSession, User
from . import math_tree_progress as tp
from .math_tree_progress import Part

CONTEXT = "math"
PRACTICE, TRIAL = "practice", "trial"
PLACEMENT = "placement"     # M11: bài kiểm tra đầu vào (systems/math_placement.py)
DRAW_TRIES = 30         # draws of one generator before giving up on finding numbers not seen lately
REVIEW_SCAN = 4         # times the gate window: how far back the review schedule reads the log


class MathError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ views
def _templates(subject_id: str, floor: int) -> list[Template]:
    """The question templates of a floor this server may ask - never one of a micro-skill
    the tree has cut (R6: in no mode, since every mode reads its templates here)."""
    cut = math_tree.tree().cut_skills()
    return [t for t in math_items.floor_templates(subject_id, floor, settings.allow_unreviewed)
            if t.skill not in cut]


def _part_templates(part: Part) -> list[Template]:
    """The templates of a part's own micro-skills (a whole floor for an old sitting)."""
    skills = set(part.skills)
    return [t for t in _templates(part.subject_id, part.floor) if t.skill in skills]


def run_skills(run: MathRun) -> list[str]:
    """The micro-skills a sitting is about: its part's (the whole floor for an old sitting)."""
    part = tp.run_part(run)
    return list(part.skills) if part is not None else []


def trial_skills(run: MathRun, config: dict | None = None) -> list[str]:
    """The micro-skills a Thiên kiếp nhỏ asks about, in path order, each one
    `questions_per_skill` times (R8: a part's trial asks the part's micro-skills)."""
    per = math_mastery.trial_cfg(config)["questions_per_skill"]
    return [s for s in run_skills(run) for _ in range(per)]


def run_view(run: MathRun) -> dict:
    lo, hi = math_path.floor_tiers(run.floor)
    node_id = getattr(run, "node_id", None)
    node = math_tree.tree().nodes.get(node_id) if node_id else None
    out = {"run_id": run.id, "subject_id": run.subject_id, "floor": run.floor, "mode": run.mode,
           "node_id": node_id, "node_name_vi": node.name_vi if node else None,
           "tier": run.tier, "tier_name_vi": math_path.cfg()["tiers"][str(run.tier)]["name_vi"],
           "tier_min": lo, "tier_max": hi, "combo": run.combo, "best_combo": run.best_combo,
           "asked": run.asked, "correct": run.correct, "review_asked": run.review_asked,
           "xp_gained": run.xp_gained, "passed": run.passed, "ended": run.ended_at is not None,
           "ladders": run.ladders or 0}
    if run.mode == TRIAL:
        total = len(trial_skills(run))
        out["trial"] = {"total": total, "left": max(0, total - run.asked),
                        "wrong": run.asked - run.correct,
                        "max_wrong": math_mastery.trial_allowed(total)}
    return out


async def open_run(db: AsyncSession, user_id: int) -> MathRun | None:
    """The buổi luyện or Thiên kiếp nhỏ the player left open. A placement sitting (M11) is
    not one of them: it has its own routes and lives beside them."""
    return (await db.execute(select(MathRun).where(MathRun.user_id == user_id, MathRun.ended_at.is_(None),
                                                   MathRun.mode != PLACEMENT)
                             .order_by(MathRun.id.desc()))).scalars().first()


async def trial_floors(db: AsyncSession, user_id: int, subject_id: str) -> set[int]:
    """The floors of this subject whose Thiên kiếp nhỏ the player has passed."""
    rows = (await db.execute(select(MathRun.floor).where(
        MathRun.user_id == user_id, MathRun.subject_id == subject_id,
        MathRun.mode == TRIAL, MathRun.passed.is_(True)).distinct())).scalars().all()
    return set(rows)


async def placement_floors(db: AsyncSession, user_id: int, subject_id: str) -> set[int]:
    """The main floors of this subject the player skipped with the bài kiểm tra đầu vào
    (M11): every main floor below the start floor of their latest finished sitting. An
    abandoned sitting (`passed` not true) skipped nothing."""
    run = (await db.execute(select(MathRun).where(
        MathRun.user_id == user_id, MathRun.subject_id == subject_id, MathRun.mode == PLACEMENT,
        MathRun.ended_at.is_not(None)).order_by(MathRun.id.desc()))).scalars().first()
    if run is None or not run.passed:
        return set()
    try:
        subject = math_path.subject(subject_id)
    except KeyError:
        return set()
    return {f.number for f in subject.main_floors if f.number < run.floor}


async def cleared_floors(db: AsyncSession, user_id: int, subject_id: str) -> set[int]:
    """Compatibility answer (math_tree_progress.cleared_floors): the floors of this subject
    all of whose main-path parts are passed. Nothing that decides what a player may do reads
    it any more: those callers read the tree's frontier, reached floors or working stage."""
    return await tp.cleared_floors(db, user_id, subject_id)


async def floor_gate(db: AsyncSession, user_id: int, subject: math_path.Subject, floor: int,
                     config: dict | None = None) -> math_mastery.FloorGate:
    """Half (a) of the mastery gate for one whole floor, read from the answer log."""
    return await part_gate(db, user_id, tp.part_of(subject.id, floor), config)


async def part_gate(db: AsyncSession, user_id: int, part: Part,
                    config: dict | None = None) -> math_mastery.FloorGate:
    """Half (a) of the mastery gate of a part (R8): math_mastery.floor_gate over the part's
    micro-skills, read from the answer log."""
    config = config or math_path.cfg()
    skills = list(part.skills)
    results = await _results_by_skill(db, user_id, skills, part.floor,
                                      max(config["mastery_gate"]["window"], config["tier_unlock"]["window"]),
                                      include_top=True)
    return math_mastery.floor_gate(part.floor, skills, results, config)


async def path_view(db: AsyncSession, user: User) -> dict:
    """The subjects and floors, how many question templates each floor has for this server
    (hand-written items + generators), which floors are open or cleared and how far the
    mastery gate of each open floor has come, and the sitting the player left open (if any).

    Since Đạo Thụ the floors' states come from the tree: a floor is playable when a part on
    it is open or done, "cleared" when all of its main-path parts are passed; its gate, trial
    and `node_id` are those of the part a sitting on it resolves to (R11). The tree itself is
    GET /math/tree; this view keeps its shape for the screens that read floors."""
    from . import math_placement        # (it imports this module)
    cfg = math_path.cfg()
    st = await tp.state(db, user.id)
    subjects = []
    for s in math_path.subjects():
        by_trial = st.trial_floors.get(s.id, set())
        cleared = tp.cleared_floors_of(st, s.id)
        floors = []
        for f in s.floors:
            lo, hi = math_path.floor_tiers(f.number)
            templates = _templates(s.id, f.number)
            docs = math_library.for_floor(s.id, f.number)
            part = tp.floor_part(st, s.id, f.number) if templates else None
            state = (math_mastery.CLEARED if f.number in cleared else
                     math_mastery.OPEN if part is not None else math_mastery.LOCKED)
            gate = None
            if part is not None:
                gate = (await part_gate(db, user.id, part, cfg)).view()
            floors.append({"floor": f.number, "title_vi": f.title_vi, "hidden": f.hidden,
                           "tier_min": lo, "tier_max": hi, "questions": len(templates),
                           "generators": sum(1 for t in templates if t.generated),
                           "playable": part is not None,
                           "has_questions": bool(templates), "state": state, "gate": gate,
                           # M11: a cleared floor was cleared by its Thiên kiếp nhỏ or skipped by placement
                           "cleared_by": (None if f.number not in cleared else
                                          "trial" if f.number in by_trial else "placement"),
                           "trial_total": (math_mastery.trial_cfg(cfg)["questions_per_skill"] * len(part.skills)
                                           if part is not None else math_mastery.trial_total(s, f.number, cfg)),
                           "node_id": part.node_id if part is not None else None,
                           "doc_id": docs[0].id if docs else None,
                           "skills": [{"id": k.id, "name_vi": k.name_vi} for k in f.skills]})
        front = tp.frontier_of(st, s.id)
        subjects.append({"id": s.id, "name_vi": s.name_vi, "order": s.order, "floors": floors,
                         "cleared": sorted(cleared),
                         # the floor of the first open main-path part of the subject (R9), None when none is open
                         "next_floor": front.floor if front is not None and st.part_open(front) else None,
                         # how many programming exercises the player may open right now (M6, R10)
                         "problems": sum(1 for p in math_problems.bank().values()
                                         if p.subject == s.id and (p.reviewed or settings.allow_unreviewed)
                                         and tp.problem_open(st, p)),
                         # M11: the bài kiểm tra đầu vào of this subject (offered / in progress / done)
                         "placement": _placement_brief(await math_placement.state(db, user, s.id))})
    run = await open_run(db, user.id)
    return {"subjects": subjects, "run": run_view(run) if run else None, "tree": {"stage": tp.stage_view(st)},
            "tiers": {t: v["name_vi"] for t, v in cfg["tiers"].items() if not t.startswith("_")}}


def _placement_brief(st: dict) -> dict:
    """What the hub needs to know about the bài kiểm tra đầu vào of a subject."""
    res = st.get("result") or {}
    return {"status": st["status"], "offered": st["offered"], "planned": st["planned"],
            "run_id": (st.get("run") or {}).get("run_id"),
            "start_floor": res.get("start_floor"), "abandoned": res.get("abandoned")}


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
async def _floor_part(db: AsyncSession, user: User, subject_id: str, floor: int) -> Part:
    """R11: the old "sit down on floor n" - the open part on that floor (the first by stage
    when several nodes share it), or one that may still be practised; refused when no part
    there is open or done."""
    try:
        subject = math_path.subject(subject_id)
        subject.floor(floor)
    except KeyError:
        raise MathError(404, "no_floor", "Không có tầng này.")
    if not _templates(subject_id, floor):
        raise MathError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    st = await tp.state(db, user.id)
    part = tp.floor_part(st, subject_id, floor)
    if part is None:
        here = [p.node_id for p in tp.floor_parts(subject_id, floor) if st.has_questions(p)]
        raise MathError(403, "node_locked", tp.locked_message(st, here[:1]))
    return part


async def _node_part(db: AsyncSession, user: User, node_id: str, floor: int | None) -> Part:
    """The part of a node a sitting is started on: the one on `floor`, by default the first
    part not passed yet (the first part when all are passed)."""
    node = math_tree.tree().nodes.get(node_id)
    if node is None:
        raise MathError(404, "no_node", "Không có nút này trên Đạo Thụ.")
    st = await tp.state(db, user.id)
    asked = [p for p in tp.parts(node) if st.has_questions(p)]
    if not asked:
        raise MathError(400, "no_questions", "Nút này chưa có câu hỏi (đang biên soạn).")
    if floor is not None:
        part = next((p for p in asked if p.floor == floor), None)
        if part is None:
            raise MathError(404, "no_floor", "Nút này không có câu hỏi ở tầng này.")
    else:
        part = next((p for p in asked if not st.part_passed(p)), asked[0])
    if not st.playable(part):
        raise MathError(403, "node_locked", tp.locked_message(st, [node.id]))
    return part


async def _new_run(db: AsyncSession, user: User, part: Part, mode: str, tier: int) -> MathRun:
    now = clock.now()
    for old in (await db.execute(select(MathRun).where(MathRun.user_id == user.id, MathRun.mode != PLACEMENT,
                                                       MathRun.ended_at.is_(None)))).scalars():
        old.ended_at = now          # one sitting at a time (a placement sitting lives beside it, M11)
    run = MathRun(user_id=user.id, subject_id=part.subject_id, node_id=part.node_id, floor=part.floor,
                  mode=mode, tier=tier, correct_streak=0, wrong_streak=0, combo=0, best_combo=0, asked=0,
                  correct=0, review_asked=0, xp_gained=0, passed=None, started_at=now)
    db.add(run)
    await db.flush()
    return run


async def _practice(db: AsyncSession, user: User, part: Part) -> dict:
    run = await _new_run(db, user, part, PRACTICE, math_adaptive.start(part.floor).tier)
    return {"run": run_view(run)}


async def _trial(db: AsyncSession, user: User, part: Part) -> dict:
    """The Thiên kiếp nhỏ of a part (rule 3b, R8). It opens only when every micro-skill of
    the part is through the mastery gate; a failed trial can be taken again straight away."""
    gate = await part_gate(db, user.id, part)
    if not gate.ok:
        skills = math_path.subject(part.subject_id).skills
        names = ", ".join(skills[s.skill_id].name_vi for s in gate.weak)
        raise MathError(409, "gate_not_met", f"Chưa đủ thuần thục để vượt Thiên kiếp nhỏ. Hãy ôn: {names}.")
    run = await _new_run(db, user, part, TRIAL, math_mastery.trial_tier(part.floor))
    return {"run": run_view(run), "gate": gate.view()}


async def start(db: AsyncSession, user: User, subject_id: str, floor: int) -> dict:
    """A buổi luyện on a floor: on the part of it the tree has open (R11)."""
    return await _practice(db, user, await _floor_part(db, user, subject_id, floor))


async def start_trial(db: AsyncSession, user: User, subject_id: str, floor: int) -> dict:
    """The Thiên kiếp nhỏ of a floor: of the part of it the tree has open (R11)."""
    return await _trial(db, user, await _floor_part(db, user, subject_id, floor))


async def start_node(db: AsyncSession, user: User, node_id: str, floor: int | None = None) -> dict:
    """POST /math/node/start: a buổi luyện on a part of a node of Đạo Thụ."""
    return await _practice(db, user, await _node_part(db, user, node_id, floor))


async def start_node_trial(db: AsyncSession, user: User, node_id: str, floor: int | None = None) -> dict:
    """POST /math/node/trial: the Thiên kiếp nhỏ of a part of a node."""
    return await _trial(db, user, await _node_part(db, user, node_id, floor))


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


def _with_questions(skills: list[str]) -> dict[str, int]:
    """skill -> its floor, for the micro-skills that have a template on their own floor."""
    home = tp.skill_home()
    out: dict[str, int] = {}
    asked: dict[tuple[str, int], set[str]] = {}
    for s in skills:
        if s not in home or s in out:
            continue
        key = home[s]
        if key not in asked:
            asked[key] = {t.skill for t in _templates(*key)}
        if s in asked[key]:
            out[s] = key[1]
    return out


async def _review_candidates(db: AsyncSession, user_id: int, run: MathRun) -> dict[str, int]:
    """The micro-skills review questions of this sitting come from (rule 6b, R7), with their
    floors: those of the nodes the sitting's node reinforces (any subject); when none of them
    has questions, those of the node's done ancestors; an old sitting with no node: every
    micro-skill of a floor below, as before Đạo Thụ."""
    node_id = getattr(run, "node_id", None)
    if node_id is None:
        subject = math_path.subject(run.subject_id)
        return {s.id: f.number for f in subject.floors
                if not f.hidden and f.number < run.floor and _templates(run.subject_id, f.number)
                for s in f.skills}
    t = math_tree.tree()
    if node_id not in t.nodes:
        return {}
    where = _with_questions(t.review_skills(node_id))
    if where:
        return where
    st = await tp.state(db, user_id)
    done = st.done
    ancestors = sorted(a for a in t.ancestors(node_id) if a in done)
    return _with_questions([s for a in ancestors for s in t.nodes[a].skills])


async def _review_stats(db: AsyncSession, user_id: int, run: MathRun,
                        config: dict) -> list[math_mastery.ReviewStat]:
    """Every micro-skill this sitting may review (`_review_candidates`), as the spaced
    repetition schedule sees it. One pass over the end of the answer log: a micro-skill that
    is not in it at all was answered so long ago that it is due anyway."""
    where = await _review_candidates(db, user_id, run)
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
    """A review question (rule 6b, R7): the micro-skill that is due and has been answered
    worst lately, at the highest tier open for it on its own floor (of its own subject)."""
    seen_at = {fp: i for i, fp in reversed(list(enumerate(recent)))}
    home = tp.skill_home()
    for stat in math_mastery.review_queue(stats, clock.now(), config):
        templates = _templates(home.get(stat.skill_id, (run.subject_id,))[0], stat.floor)
        results = await _results_by_skill(db, user_id, [stat.skill_id], stat.floor,
                                          config["tier_unlock"]["window"])
        top = math_adaptive.open_tier(stat.floor, results.get(stat.skill_id, {}), config)
        item = _pick(_at_tier(templates, stat.skill_id, top), seen_at, rng)
        if item is not None:
            return item
    return None


async def _trial_item(db: AsyncSession, run: MathRun, recent: list[str], rng: random.Random,
                      config: dict) -> MathItem:
    """The next question of a Thiên kiếp nhỏ: the next micro-skill of the part this trial
    has not asked about yet, at the hardest tier of the floor."""
    left = trial_skills(run, config)
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
    """The oldest open mistake of this part that has waited long enough. A tier-5 mistake
    whose ladder is being climbed (or was climbed in this sitting with a rung missed) is held;
    one whose ladder was just climbed cleanly goes first (rule 8, see the module docstring).
    A mistake about a micro-skill of another part of this floor waits for a sitting on that
    part; a missed rung from a floor below (kept on this floor by rule 8) comes back here."""
    wait = math_path.cfg()["parallel_question"]["after_answers"]
    held, first = await _ladder_holds(db, user_id, run)
    retries = (await db.execute(select(MathRetry).where(
        MathRetry.user_id == user_id, MathRetry.subject_id == run.subject_id, MathRetry.floor == run.floor,
        MathRetry.cleared_at.is_(None)).order_by(MathRetry.id))).scalars().all()
    mine, home = set(run_skills(run)), tp.skill_home()
    retries = [r for r in retries if r.skill_id in mine
               or home.get(r.skill_id) != (run.subject_id, run.floor)]
    retries = sorted((r for r in retries if r.id not in held), key=lambda r: (r.id not in first, r.id))
    for retry in retries:
        since = (await db.execute(select(func.count()).select_from(MathAnswer).where(
            MathAnswer.user_id == user_id, MathAnswer.id > retry.after_answer_id))).scalar_one()
        if since >= wait:
            return retry
    return None


async def next_question(db: AsyncSession, user: User, run_id: int, rng: random.Random | None = None) -> dict:
    """The run's open question if it still has one, else a new one."""
    run = await _own_run(db, user, run_id, lock=True)
    if run.mode == PLACEMENT:
        raise MathError(409, "wrong_mode", "Bài kiểm tra đầu vào có đường riêng: /math/placement/next.")
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
    part = tp.run_part(run)
    templates = _part_templates(part) if part is not None else []
    rows = (await db.execute(select(MathAnswer.fingerprint, MathAnswer.item_id).where(MathAnswer.user_id == user.id)
                             .order_by(MathAnswer.id.desc()).limit(cfg["anti_repeat_window"]))).all()
    recent = [r[0] for r in rows]
    rng = rng or random.Random()
    item, retry, review, ladder = None, None, False, None
    if run.mode == TRIAL:
        item = await _trial_item(db, run, recent, rng, cfg)
    else:
        ladder = await _open_ladder(db, user.id, run)
        if ladder is not None:
            item = _next_rung(ladder, run, recent, rng, now)
            if item is None:                # no rung of it is in the bank any more: climbed
                ladder = None
        if item is None:
            retry = await _due_retry(db, user.id, run)
        if retry is not None:
            item = parallel_item(_retry_templates(run, retry, templates), retry, recent, rng)
            if item is None:                # its micro-skill has no question any more
                retry.cleared_at, retry = now, None
        if item is None and math_mastery.wants_review(run.asked, run.review_asked, cfg):
            stats = await _review_stats(db, user.id, run, cfg)
            item = await _review_item(db, user.id, run, stats, recent, rng, cfg)
            review = item is not None       # nothing to review, or nothing due: an ordinary question
        if item is None:
            skills = sorted({t.skill for t in templates})
            results = await _results_by_skill(db, user.id, skills, run.floor, cfg["tier_unlock"]["window"])
            item = choose_item(templates, run.tier, run.floor, results, recent, rng, [r[1] for r in rows])
    question = math_items.to_question(item, rng, cfg, parallel=retry is not None, review=review)
    question.meta["doc"] = doc_link(item.skill)          # "Đọc Tàng Thư" on the answer card
    if review:                                           # "Ôn: <the node reviewed>" on the card
        owner = math_tree.tree().node_of_skill().get(item.skill)
        if owner is not None:
            question.meta["review_node_vi"] = math_tree.tree().nodes[owner].name_vi
    if retry is not None:
        question.answer_key["retry_id"] = retry.id
    if ladder is not None:
        question.meta["ladder"] = _ladder_view(ladder, ladder.step + 1)     # "Bậc thang 2/3" on the card
        question.answer_key["ladder_id"], question.answer_key["ladder_step"] = ladder.id, ladder.step
    out = await quiz.create_session(db, user, CONTEXT, question, ref=str(run.id))
    return {"run": run_view(run), "question": out}


# ------------------------------------------------------------------ rule 8: the ladder
def _ladder_view(ladder: MathLadder, step: int) -> dict:
    return {"of": ladder.item_id, "step": step, "steps": len(ladder.steps or [])}


def _template(subject_id: str, template_id: str) -> Template | None:
    """A hand-written item or a generator of this subject that this server may ask."""
    t = math_items.bank().get(template_id) or math_items.generators().get(template_id)
    if t is None or t.subject != subject_id or not (t.reviewed or settings.allow_unreviewed):
        return None
    return t


def _retry_templates(run: MathRun, retry: MathRetry, templates: list[Template]) -> list[Template]:
    """The templates a parallel question is found among: this part's, or - for a missed rung
    that lives elsewhere (rule 8 keys it to the sitting's floor) - those of the rung's floor."""
    skill = math_path.subject(run.subject_id).skills.get(retry.skill_id)
    if skill is None or retry.skill_id in {t.skill for t in templates}:
        return templates
    return _templates(run.subject_id, skill.floor)


async def _open_ladder(db: AsyncSession, user_id: int, run: MathRun) -> MathLadder | None:
    """The ladder being climbed on this sitting's part (there is at most one): a ladder
    belongs to the part whose micro-skill opened it (one opened by a review question, whose
    micro-skill lives elsewhere, to the sittings of the floor it was opened on, as before)."""
    mine, home = set(run_skills(run)), tp.skill_home()
    rows = (await db.execute(select(MathLadder).where(
        MathLadder.user_id == user_id, MathLadder.subject_id == run.subject_id, MathLadder.floor == run.floor,
        MathLadder.finished_at.is_(None)).order_by(MathLadder.id))).scalars().all()
    return next((ladder for ladder in rows if ladder.skill_id in mine
                 or home.get(ladder.skill_id) != (run.subject_id, run.floor)), None)


def _finish_ladder(ladder: MathLadder, run: MathRun, now: dt.datetime) -> None:
    ladder.finished_at, ladder.run_id = now, run.id
    run.ladders = (run.ladders or 0) + 1


def _next_rung(ladder: MathLadder, run: MathRun, recent: list[str], rng: random.Random,
               now: dt.datetime) -> MathItem | None:
    """The next rung as a question: a hand-written rung as it is, a generator rung as one
    fresh draw. Rungs that are no longer in the bank are passed by; None (and the ladder is
    finished) when none is left."""
    steps = list(ladder.steps or [])
    while ladder.step < len(steps):
        t = _template(run.subject_id, steps[ladder.step])
        if isinstance(t, MathItem):
            return t
        if isinstance(t, GeneratorSpec):
            seen = {fp: i for i, fp in enumerate(recent)}
            return _fresh(t, seen, rng) or math_items.draw(t, rng)
        ladder.step += 1
    _finish_ladder(ladder, run, now)
    return None


async def _ladder_holds(db: AsyncSession, user_id: int, run: MathRun) -> tuple[set[int], set[int]]:
    """Rule 6 meets rule 8: (the mistakes held back, the mistakes to ask first). A tier-5
    mistake is held while its ladder is climbed, and for the rest of the sitting when a rung
    was missed; a clean climb in this sitting puts it first."""
    rows = (await db.execute(select(MathLadder).where(
        MathLadder.user_id == user_id, MathLadder.subject_id == run.subject_id,
        MathLadder.retry_id.is_not(None),
        (MathLadder.finished_at.is_(None)) | (MathLadder.run_id == run.id)))).scalars().all()
    held, first = set(), set()
    for ladder in rows:
        if ladder.finished_at is None or ladder.missed:
            held.add(ladder.retry_id)
        else:
            first.add(ladder.retry_id)
    return held, first - held


async def _ladder_after_answer(db: AsyncSession, user: User, s: QuizSession, meta: dict, run: MathRun,
                               correct: bool, retry: MathRetry | None, now: dt.datetime) -> dict | None:
    """Rule 8 after one answer of a buổi luyện: a rung moves its ladder on; a tier-5
    hand-written question answered wrong opens its ladder. Returns `math.ladder` for the
    client, or None when this answer had nothing to do with a ladder."""
    if s.answer_key.get("ladder_id") is not None:
        ladder = await db.get(MathLadder, s.answer_key["ladder_id"])
        if (ladder is None or ladder.user_id != user.id or ladder.finished_at is not None
                or ladder.step != s.answer_key.get("ladder_step")):
            return None
        ladder.step += 1
        ladder.missed += int(not correct)
        ladder.run_id = run.id
        done = ladder.step >= len(ladder.steps or [])
        out = {**_ladder_view(ladder, ladder.step), "rung": True, "done": done, "missed": ladder.missed,
               "returns": False}
        if done:
            _finish_ladder(ladder, run, now)
            back = await db.get(MathRetry, ladder.retry_id) if ladder.retry_id is not None else None
            out["returns"] = not ladder.missed and back is not None and back.cleared_at is None
        return out
    if correct or meta["tier"] != math_path.TOP_TIER:
        return None
    item = math_items.bank().get(s.item_id)
    if item is None or not item.ladder or item.subject != meta["subject"]:
        return None                     # a generator (no ladder), or a stale id
    if await _open_ladder(db, user.id, run) is not None:
        return None
    again = (await db.execute(select(MathLadder.id).where(
        MathLadder.user_id == user.id, MathLadder.item_id == item.id,
        MathLadder.started_run_id == run.id))).scalars().first()
    if again is not None:               # once per item and sitting: a second miss is plain rule 6
        return None
    ladder = MathLadder(user_id=user.id, subject_id=run.subject_id, floor=run.floor, item_id=item.id,
                        skill_id=item.skill, steps=list(item.ladder), step=0, missed=0,
                        retry_id=retry.id if retry is not None else None, started_run_id=run.id,
                        run_id=run.id, created_at=now)
    db.add(ladder)
    return {**_ladder_view(ladder, 0), "started": True, "rung": False, "done": False}


# ------------------------------------------------------------------ after an answer
async def _remember_mistake(db: AsyncSession, user_id: int, s: QuizSession, meta: dict,
                            answer: MathAnswer, correct: bool, now: dt.datetime,
                            floor: int | None = None) -> MathRetry | None:
    """Rule 6 bookkeeping. Returns the mistake whose parallel question is now waiting, if
    any. `floor` = the floor whose sittings bring it back (a missed rung of a ladder: the
    sitting's floor, rule 8); by default the floor of the question."""
    retry_id = s.answer_key.get("retry_id")
    fingerprint = s.answer_key.get("fingerprint", "")
    if retry_id is not None:
        retry = await db.get(MathRetry, retry_id)
        if retry is None or retry.cleared_at is not None or retry.user_id != user_id:
            return None
        if correct:
            retry.cleared_at = now
            return None
        retry.after_answer_id, retry.fingerprint, retry.misses = answer.id, fingerprint, retry.misses + 1
        return retry
    if correct:
        return None
    floor = meta["floor"] if floor is None else floor
    open_ = (await db.execute(select(MathRetry).where(
        MathRetry.user_id == user_id, MathRetry.subject_id == meta["subject"], MathRetry.floor == floor,
        MathRetry.cleared_at.is_(None)).order_by(MathRetry.id))).scalars().all()
    same = next((r for r in open_ if r.item_id == s.item_id), None)
    if same is not None:
        same.after_answer_id, same.fingerprint, same.misses = answer.id, fingerprint, same.misses + 1
        return same
    retry = MathRetry(user_id=user_id, subject_id=meta["subject"], floor=floor, skill_id=meta["skill"],
                      tier=meta["tier"], item_id=s.item_id, fingerprint=fingerprint,
                      after_answer_id=answer.id, misses=1, created_at=now)
    db.add(retry)
    keep = math_path.cfg()["parallel_question"]["max_open"] - 1
    for old in open_[:max(0, len(open_) - keep)]:       # the queue is short: the oldest mistakes are let go
        old.cleared_at = now
    await db.flush()                                    # (a ladder keeps its id)
    return retry


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
    live = run is not None and run.ended_at is None and run.user_id == user.id
    rung = live and s.answer_key.get("ladder_id") is not None
    retry = None if trial else await _remember_mistake(db, user.id, s, meta, answer, correct, now,
                                                       floor=run.floor if rung else None)
    out: dict = {"tier": meta["tier"], "timed_out": timed_out, "parallel": bool(meta.get("parallel")),
                 "parallel_waiting": retry is not None, "review": review,
                 "xp_base": math_path.xp_for_tier(meta["tier"]) if correct else 0}
    if live and run.mode == PRACTICE:       # rule 8: only a buổi luyện climbs ladders
        ladder = await _ladder_after_answer(db, user, s, meta, run, correct, retry, now)
        if ladder is not None:
            out["ladder"] = ladder
    from . import math_combat      # M10: cơ duyên listens to every right answer (math_combat.add_answer_listener)
    out.update(await math_combat.notify_answer(db, user, s, correct, now))
    if live:
        before = run.tier
        if not trial and not rung:          # the tier of a trial is the floor's hardest, all the way;
            # a rung (rule 8) is below the floor's range when it comes from a floor below
            state = math_adaptive.after_answer(
                math_adaptive.TierState(run.tier, run.correct_streak, run.wrong_streak), correct, run.floor)
            run.tier, run.correct_streak, run.wrong_streak = state.tier, state.correct_streak, state.wrong_streak
        run.asked += 1
        run.correct += int(correct)
        run.review_asked += int(review)
        run.combo = run.combo + 1 if correct else 0      # a wrong answer or a timeout ends the combo
        run.best_combo = max(run.best_combo, run.combo)
        if trial:
            out["trial"] = await _trial_after_answer(db, user, run, now)
        out.update(run=run_view(run), tier_change=run.tier - before)
    return {"math": out}


async def _trial_after_answer(db: AsyncSession, user: User, run: MathRun, now: dt.datetime) -> dict:
    """Where a Thiên kiếp nhỏ stands after one answer, and what passing it opened.
    **Ends the run** as soon as the trial is won or lost, so nobody has to finish a trial
    they cannot pass any more. `opened` = the tree nodes that opened because of it,
    `node_done` = its node is now done, `unlocked` = the lowest floor of this subject that
    holds a part of a node it opened (None when it opened nothing on this subject)."""
    total = len(trial_skills(run))
    verdict = math_mastery.trial_verdict(run.asked, run.correct, total)
    out = {"total": total, "asked": run.asked, "correct": run.correct,
           "left": max(0, total - run.asked), "passed": verdict, "unlocked": None,
           "opened": [], "node_done": False}
    if verdict is None:
        return out
    before = set((await tp.state(db, user.id)).open) if verdict else set()
    run.passed, run.ended_at = verdict, now
    if verdict:
        await db.flush()
        st = await tp.state(db, user.id)
        out["opened"] = [n for n in st.open if n not in before]
        out["node_done"] = run.node_id is not None and run.node_id in st.done
        floors = [p.floor for n in out["opened"] for p in tp.parts(n)
                  if p.subject_id == run.subject_id and st.has_questions(p)]
        out["unlocked"] = min(floors) if floors else None
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
