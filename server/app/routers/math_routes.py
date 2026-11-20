"""Math question loop REST (milestone M2; the Thiên kiếp nhỏ of a floor in M5; the nodes of
Đạo Thụ, the curriculum tree, since it was wired). A question of a sitting is answered
through /quiz/answer like every other question."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..learning import math_library
from ..models import User
from ..systems import math_code, math_craft, math_placement, math_practice, math_tree_progress
from ..systems import math_combat  # noqa: F401  (registers the quái lỗi sai grader)
from ..systems import math_skills  # (registers the grader of cast questions, M9)

router = APIRouter(tags=["math"])


class StartIn(BaseModel):
    subject_id: str = Field(max_length=40)
    floor: int = Field(ge=1, le=99)


class RunIn(BaseModel):
    run_id: int = Field(ge=1)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except (math_practice.MathError, math_craft.CraftError) as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/math/path")
async def math_path_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.path_view(db, user))


@router.post("/math/run/start")
async def math_run_start(body: StartIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.start(db, user, body.subject_id, body.floor))


@router.post("/math/trial/start")
async def math_trial_start(body: StartIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """Thiên kiếp nhỏ: the test that clears a floor (M5, learning-path rule 3b)."""
    return await _run(db, math_practice.start_trial(db, user, body.subject_id, body.floor))


class NodeIn(BaseModel):
    node_id: str = Field(max_length=40)
    floor: int | None = Field(default=None, ge=1, le=99)    # the part of a node that spans two floors


@router.get("/math/tree")
async def math_tree_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Đạo Thụ: every node of the curriculum tree with this player's state, the stage reached,
    what to do next and the sitting left open."""
    return await _run(db, math_tree_progress.tree_view(db, user))


@router.post("/math/node/start")
async def math_node_start(body: NodeIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """A buổi luyện on a node (its first part not passed yet, or the part on `floor`)."""
    return await _run(db, math_practice.start_node(db, user, body.node_id, body.floor))


@router.post("/math/node/trial")
async def math_node_trial(body: NodeIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """The Thiên kiếp nhỏ of a part of a node (R8)."""
    return await _run(db, math_practice.start_node_trial(db, user, body.node_id, body.floor))


@router.post("/math/run/next")
async def math_run_next(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.next_question(db, user, body.run_id))


@router.post("/math/run/end")
async def math_run_end(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.end(db, user, body.run_id))


class SubjectIn(BaseModel):
    subject_id: str = Field(max_length=40)


@router.get("/math/placement")
async def math_placement_state(subject_id: str, user: User = Depends(current_user),
                               db: AsyncSession = Depends(get_db)):
    """Bài kiểm tra đầu vào of a subject (M11, rule 7): offered, in progress or done, and
    the result floor by floor."""
    return await _run(db, math_placement.state(db, user, subject_id))


@router.post("/math/placement/start")
async def math_placement_start(body: SubjectIn, user: User = Depends(write_user),
                               db: AsyncSession = Depends(get_db)):
    return await _run(db, math_placement.start(db, user, body.subject_id))


@router.post("/math/placement/next")
async def math_placement_next(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """The open question, or the next one; `question` is null once the outcome is decided."""
    return await _run(db, math_placement.next_question(db, user, body.run_id))


@router.post("/math/placement/abandon")
async def math_placement_abandon(body: RunIn, user: User = Depends(write_user),
                                 db: AsyncSession = Depends(get_db)):
    """Give the sitting up: nothing is skipped (the player starts on the first floor)."""
    return await _run(db, math_placement.abandon(db, user, body.run_id))


class ProblemsIn(BaseModel):
    subject_id: str = Field(max_length=40)
    floor: int = Field(ge=1, le=99)


class JudgeIn(BaseModel):
    """What the player's machine printed. The code never leaves their own account; it is
    kept so they can read back what they handed in."""
    outputs: list[str] = Field(default_factory=list, max_length=200)
    status: str = Field(default="ok", max_length=4)
    times_ms: list[int] = Field(default_factory=list, max_length=200)
    code: str = Field(default="", max_length=40000)
    error: str = Field(default="", max_length=2000)
    attempt_id: int | None = Field(default=None, ge=1)


@router.get("/math/problems")
async def math_problems_list(subject_id: str, floor: int | None = None, ids: str = "",
                             user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Bài tập lập trình of a subject, floor by floor; `floor` narrows it to one (M6). `ids`
    (comma separated, the exercises of one node) lists only those, from every subject."""
    wanted = [i for i in ids.split(",") if i][:50]
    return await _run(db, math_code.list_view(db, user, subject_id, floor, wanted or None))


@router.get("/math/problem/{problem_id}")
async def math_problem_get(problem_id: str, user: User = Depends(current_user),
                           db: AsyncSession = Depends(get_db)):
    """The statement and its samples. Hidden tests are not in this answer."""
    return await _run(db, math_code.problem_view(db, user, problem_id))


@router.post("/math/problem/{problem_id}/tests")
async def math_problem_tests(problem_id: str, user: User = Depends(write_user),
                             db: AsyncSession = Depends(get_db)):
    """Nộp bài, step one: the input of the hidden tests, to run on the player's machine."""
    return await _run(db, math_code.open_attempt(db, user, problem_id))


@router.post("/math/problem/{problem_id}/judge")
async def math_problem_judge(problem_id: str, body: JudgeIn, user: User = Depends(write_user),
                             db: AsyncSession = Depends(get_db)):
    """Mark a run: with `attempt_id` it is Nộp bài (hidden tests, Tu Vi), without it Chạy
    thử on the samples."""
    return await _run(db, math_code.judge(db, user, problem_id, body.outputs, body.status,
                                          body.times_ms, body.code, body.attempt_id, body.error))


@router.get("/math/library")
async def math_library_list(user: User = Depends(current_user)):
    """Tàng Thư Các: every document, by subject and floor."""
    return math_practice.library_view()


class CraftIn(BaseModel):
    recipe_id: str = Field(max_length=40)


@router.get("/math/craft")
async def math_craft_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Lò Toán (M7): the recipes, and what the player holds against each one."""
    return await _run(db, math_craft.view(db, user))


@router.post("/math/craft")
async def math_craft_make(body: CraftIn, user: User = Depends(write_user),
                          db: AsyncSession = Depends(get_db)):
    """Forge one recipe: materials and the fee are spent, the ghi chú are only checked."""
    return await _run(db, math_craft.craft(db, user, body.recipe_id))


@router.get("/math/skills")
async def math_skills_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Chiêu thức gắn câu hỏi (M9): every chiêu in data order, and which this player has
    unlocked on the learning path."""
    return await _run(db, math_skills.view(db, user))


@router.get("/math/library/{doc_id}")
async def math_library_doc(doc_id: str, user: User = Depends(current_user)):
    doc = math_library.documents().get(doc_id)
    if doc is None:
        raise api_error(404, "no_doc", "Không tìm thấy trang sách này.")
    return doc.view()
