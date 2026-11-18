"""Thủ thành toán (M10): towers that stand for an area of mathematics. A tower is placed or
upgraded by answering a question of its area; questions are answered through /quiz/answer
like every other question (docs/API.md, "Thủ thành toán")."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import math_td, td

router = APIRouter(tags=["math"])


class StartIn(BaseModel):
    level_id: str = Field(max_length=32)


class QuestionIn(BaseModel):
    run_id: str = Field(max_length=40)
    kind: Literal["place", "upgrade", "break", "tu_khi"]
    tower_id: str | None = Field(default=None, max_length=40)


class EventIn(BaseModel):
    run_id: str = Field(max_length=40)
    start: int = Field(ge=0, le=6000)
    events: list[dict] = Field(default_factory=list, max_length=6000)


class FinishIn(BaseModel):
    run_id: str = Field(max_length=40)
    events: list[dict] = Field(default_factory=list, max_length=6000)
    claim: dict = Field(default_factory=dict)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except td.TdError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/math/td")
async def math_td_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.view(db, user))


@router.post("/math/td/start")
async def math_td_start(body: StartIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.start(db, user, body.level_id))


@router.post("/math/td/question")
async def math_td_question(body: QuestionIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.ask(db, user, body.run_id, body.kind, body.tower_id))


@router.post("/math/td/event")
async def math_td_event(body: EventIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.save_events(db, user, body.run_id, body.start, body.events))


@router.post("/math/td/resume")
async def math_td_resume(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.resume(db, user))


@router.post("/math/td/finish")
async def math_td_finish(body: FinishIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.finish(db, user, body.run_id, body.events, body.claim))


@router.post("/math/td/cancel")
async def math_td_cancel(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, math_td.cancel(db, user))
