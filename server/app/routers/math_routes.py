"""Math question loop REST (milestone M2). A question of a sitting is answered through
/quiz/answer like every other question."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import math_practice

router = APIRouter(tags=["math"])


class StartIn(BaseModel):
    subject_id: str = Field(max_length=40)
    floor: int = Field(ge=1, le=99)


class RunIn(BaseModel):
    run_id: int = Field(ge=1)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except math_practice.MathError as e:
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


@router.post("/math/run/next")
async def math_run_next(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.next_question(db, user, body.run_id))


@router.post("/math/run/end")
async def math_run_end(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_practice.end(db, user, body.run_id))
