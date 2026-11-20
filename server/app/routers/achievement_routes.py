"""Thành Tựu (systems/achievements.py): the list with progress, claims, the Đạo Tâm milestones and
the unlock toasts missed while offline. Titles are worn through POST /books/wear. docs/API.md has
the shapes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import achievements

router = APIRouter(tags=["achievements"])


class ClaimIn(BaseModel):
    id: str = Field(max_length=40)
    tier: int = Field(ge=1, le=20)


class MilestoneIn(BaseModel):
    points: int = Field(ge=1)


class SeenIn(BaseModel):
    keys: list[str] = Field(max_length=200)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except achievements.AchievementError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/achievements")
async def view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.view(db, user))


@router.get("/achievements/new")
async def new(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.new_unlocks(db, user))


@router.post("/achievements/seen")
async def seen(body: SeenIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.mark_seen(db, user, body.keys))


@router.post("/achievements/claim")
async def claim(body: ClaimIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.claim(db, user, body.id, body.tier))


@router.post("/achievements/claim-all")
async def claim_all(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.claim_all(db, user))


@router.post("/achievements/milestone")
async def milestone(body: MilestoneIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, achievements.claim_milestone(db, user, body.points))
