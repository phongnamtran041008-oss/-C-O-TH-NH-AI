"""Lộ Trình Tu Tiên (the newbie guide and roadmap board): the board, claiming a step's reward
or a chapter's bonus, and the few facts only the client knows ("seen" keys). Every step's
progress is derived from the database (systems/guide.py)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import guide

router = APIRouter(tags=["guide"])


class ClaimIn(BaseModel):
    id: str = Field(max_length=64)


class SeenIn(BaseModel):
    key: str = Field(max_length=40)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except guide.GuideError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/guide")
async def guide_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """The whole board: chapters, steps with progress, the next thing to do, what to learn
    on Đạo Thụ now, the stage reached and the handbook. Read-only."""
    return await _run(db, guide.view(db, user))


@router.post("/guide/claim")
async def guide_claim(body: ClaimIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """The reward of a done step or the bonus of a done chapter, paid once."""
    return await _run(db, guide.claim(db, user, body.id))


@router.post("/guide/seen")
async def guide_seen(body: SeenIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """The client declares a fact only it knows (the welcome was read, a panel was opened)."""
    return await _run(db, guide.seen(db, user, body.key))
