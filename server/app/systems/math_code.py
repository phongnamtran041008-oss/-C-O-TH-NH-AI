"""Bài tập lập trình: handing out an exercise, and marking what the player's machine sends
back (milestone M6, plan 5.2).

The learner's program runs on the learner's own machine (client/engine/coderun.py). The
server only ever sends **input**: the statement with its samples, and, when the player
presses Nộp bài, the input of the hidden tests. The expected output of a hidden test and
the exercise's reference solution never leave this process.

One go at an exercise is a MathSubmission. It is opened by `open_attempt` (which hands out
the hidden inputs) and closed by `judge` (which compares the outputs and pays Tu Vi). An
attempt nobody hands in simply stays open and is reused next time.

Chạy thử is the same marking on the samples: the player already has those answers, but
letting the server mark them means one comparator and one set of verdicts, not two that
can drift apart. It pays nothing and keeps no row.

Tu Vi follows the plan ("phần thưởng tỉ lệ theo số test đạt"): the exercise's tier is worth
`xp_per_correct` and the player gets that times the share of tests passed - but only for
the part they had not already earned, so handing in the same solution twice pays once.

Xạ Trường (scored exercises, docs/THUC_CHIEN_TRONG_GAME.md): Nộp bài hands out each hidden
set's training data and the inputs of its points, never their labels; what comes back is
the program's predictions, and math_problems.judge_scored computes the score here. The
row keeps the grade as passed out of 3, so the same rule pays tier XP x grade / 3, only
for a grade above the best one so far, and the exercise is solved at thượng phẩm.

Exercises listed by a Thực Chiến or project node (branch "ud") also wait for that node to
open: their micro-skill's node opens much earlier (R10), but a training ground is reached
through its own node of Đạo Thụ.
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import settings
from ..learning import math_path, math_problems
from ..learning.math_problems import Problem
from ..models import MathSubmission, User
from . import cultivation, math_tree_progress
from .math_practice import MathError

RUN, SUBMIT = "run", "submit"


def cfg(config: dict | None = None) -> dict:
    return (config or math_path.cfg())["programming"]


# ------------------------------------------------------------------ views
def _visible(problem: Problem) -> bool:
    return settings.allow_unreviewed or problem.reviewed


GATED_BRANCHES = ("ud",)     # Thực Chiến and the realm project: exercises open with their node


def _gate_nodes(st, problem: Problem) -> list[str]:
    """The Thực Chiến / project nodes that list this exercise."""
    return [n.id for n in st.tree.nodes.values() if n.branch in GATED_BRANCHES and problem.id in n.problems]


def problem_open(st, problem: Problem) -> bool:
    """R10 (the micro-skill's node is open or done), and for an exercise of a Thực Chiến or
    project node, that node is open or done too."""
    if not math_tree_progress.problem_open(st, problem):
        return False
    gates = _gate_nodes(st, problem)
    return not gates or any(st.status.get(n) in (math_tree_progress.OPEN, math_tree_progress.DONE)
                            for n in gates)


async def _playable_floor(db: AsyncSession, user: User, problem: Problem) -> None:
    """An exercise belongs to a micro-skill, and it is open when that micro-skill's node of
    Đạo Thụ is open or done (R10); an exercise of a Thực Chiến node also needs that node
    open or done. Otherwise it stays shut."""
    st = await math_tree_progress.state(db, user.id)
    if not problem_open(st, problem):
        owner = st.tree.node_of_skill().get(problem.skill)
        shut = _gate_nodes(st, problem) or ([owner] if owner else [])
        raise MathError(403, "node_locked", math_tree_progress.locked_message(st, shut))


async def _best(db: AsyncSession, user_id: int, problem_id: str) -> MathSubmission | None:
    """The best go so far: most tests passed, then the most recent."""
    rows = (await db.execute(select(MathSubmission).where(
        MathSubmission.user_id == user_id, MathSubmission.problem_id == problem_id,
        MathSubmission.judged_at.is_not(None)))).scalars().all()
    return max(rows, key=lambda s: (s.passed / s.total if s.total else 0, s.id), default=None)


def _best_view(best: MathSubmission | None, problem: Problem | None = None) -> dict | None:
    if best is None:
        return None
    out = {"verdict": best.verdict, "passed": best.passed, "total": best.total,
           "ms": best.ms, "xp_gained": best.xp_gained}
    if problem is not None and problem.scored:            # passed is the grade, 0..3
        grade = max(0, min(math_problems.GRADES, best.passed))
        out.update({"grade": grade, "grade_vi": math_problems.GRADE_NAMES_VI[grade]})
    return out


async def list_view(db: AsyncSession, user: User, subject_id: str, floor: int | None = None) -> dict:
    """The exercises of a subject, floor by floor, with how the player has done on each.
    An exercise whose node is still shut keeps to itself (R10), so only open ones are listed."""
    try:
        subject = math_path.subject(subject_id)
        if floor is not None:
            subject.floor(floor)
    except KeyError:
        raise MathError(404, "no_floor", "Không có tầng này.")
    st = await math_tree_progress.state(db, user.id)
    floors = []
    for f in subject.floors:
        if floor is not None and f.number != floor:
            continue
        problems = [p for p in math_problems.floor_problems(subject_id, f.number, settings.allow_unreviewed)
                    if problem_open(st, p)]
        if not problems:
            continue
        out = []
        for p in problems:
            brief = p.brief()
            brief["best"] = _best_view(await _best(db, user.id, p.id), p)
            out.append(brief)
        floors.append({"floor": f.number, "title_vi": f.title_vi, "problems": out})
    return {"subject_id": subject_id, "name_vi": subject.name_vi, "floors": floors}


async def problem_view(db: AsyncSession, user: User, problem_id: str) -> dict:
    """The statement, its samples, and the player's best go. No hidden test is in here."""
    try:
        problem = math_problems.problem(problem_id)
    except KeyError:
        raise MathError(404, "no_problem", "Không có bài tập này.")
    if not _visible(problem):
        raise MathError(404, "no_problem", "Không có bài tập này.")
    await _playable_floor(db, user, problem)
    view = problem.view()
    view["best"] = _best_view(await _best(db, user.id, problem_id), problem)
    view["max_code_chars"] = cfg()["max_code_chars"]
    return {"problem": view}


# ------------------------------------------------------------------ one go
async def open_attempt(db: AsyncSession, user: User, problem_id: str) -> dict:
    """Nộp bài, step one: hand out the input of the hidden tests and open the row that the
    verdict will be written to. An attempt the player never handed in is reused."""
    try:
        problem = math_problems.problem(problem_id)
    except KeyError:
        raise MathError(404, "no_problem", "Không có bài tập này.")
    if not _visible(problem):
        raise MathError(404, "no_problem", "Không có bài tập này.")
    await _playable_floor(db, user, problem)
    open_row = (await db.execute(select(MathSubmission).where(
        MathSubmission.user_id == user.id, MathSubmission.problem_id == problem_id,
        MathSubmission.judged_at.is_(None)).order_by(MathSubmission.id.desc()))).scalars().first()
    if open_row is None:
        open_row = MathSubmission(user_id=user.id, problem_id=problem.id, subject_id=problem.subject,
                                  floor=problem.floor, tier=problem.tier, passed=0,
                                  total=math_problems.GRADES if problem.scored else problem.test_count,
                                  ms=0, xp_gained=0, code="", created_at=clock.now())
        db.add(open_row)
        await db.flush()
    # a scored exercise's hidden input is training data plus the points to predict; the
    # labels of those points are the test's expected output and stay here
    return {"attempt_id": open_row.id, "total": problem.test_count,
            "time_limit_ms": problem.time_limit_ms,
            "inputs": [t.data for t in problem.tests]}


def _check_outputs(outputs: list[str], total: int, config: dict) -> list[str]:
    if len(outputs) > total:
        raise MathError(400, "too_many_outputs", "Gửi về nhiều kết quả hơn số test.")
    limit = config["max_output_chars"]
    if any(len(o) > limit for o in outputs):
        raise MathError(400, "output_too_long", "Chương trình in ra quá nhiều.")
    return outputs


async def judge(db: AsyncSession, user: User, problem_id: str, outputs: list[str],
                status: str = "ok", times_ms: list[int] | None = None, code: str = "",
                attempt_id: int | None = None, error: str = "") -> dict:
    """Mark what the player's machine printed. Without `attempt_id` this is Chạy thử on the
    samples: a verdict, no Tu Vi and no row."""
    try:
        problem = math_problems.problem(problem_id)
    except KeyError:
        raise MathError(404, "no_problem", "Không có bài tập này.")
    if not _visible(problem):
        raise MathError(404, "no_problem", "Không có bài tập này.")
    if status not in math_problems.RUN_STATUS:
        raise MathError(400, "bad_status", "Kết quả chạy không hợp lệ.")
    config = cfg()
    if len(code) > config["max_code_chars"]:
        raise MathError(400, "code_too_long", "Bài làm dài quá.")
    now = clock.now()

    if attempt_id is None:                      # Chạy thử, on the samples
        tests = list(problem.samples)
        _check_outputs(outputs, len(tests), config)
        result = math_problems.judge_problem(problem, tests, outputs, status, times_ms, error)
        return {"mode": RUN, "result": result.view(), "problem_id": problem.id}

    row = await db.get(MathSubmission, attempt_id)
    if row is None or row.user_id != user.id or row.problem_id != problem.id:
        raise MathError(404, "no_attempt", "Không tìm thấy lần nộp này.")
    if row.judged_at is not None:
        raise MathError(409, "already_judged", "Lần nộp này đã chấm rồi.")
    await _playable_floor(db, user, problem)
    tests = list(problem.tests)
    _check_outputs(outputs, len(tests), config)
    result = math_problems.judge_problem(problem, tests, outputs, status, times_ms, error)

    before = await _best(db, user.id, problem.id)
    had = (before.passed / before.total) if before and before.total else 0.0
    full = math_path.xp_for_tier(problem.tier)
    gain = max(0, int(round(full * result.share)) - int(round(full * had)))
    row.verdict, row.passed, row.total = result.verdict, result.passed, result.total
    row.ms, row.code, row.judged_at = result.ms, code, now
    row.xp_gained = gain
    xp = await cultivation.add_xp(db, user.id, gain, reason="math_code") if gain else None
    return {"mode": SUBMIT, "result": result.view(), "problem_id": problem.id,
            "attempt_id": row.id, "xp": xp, "xp_gained": gain,
            "best": _best_view(await _best(db, user.id, problem.id), problem)}
