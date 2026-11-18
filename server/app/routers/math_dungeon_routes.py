"""Hầm ngục (M10): a seeded run of rooms, one question type per room. A question of a run is
answered through /quiz/answer like every other question (context "math_dungeon"); the
result carries a `dungeon` block with what the answer did to the run."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import math_dungeon

router = APIRouter(tags=["math"])


class StartIn(BaseModel):
    seed: int | None = Field(default=None, ge=0, le=2_000_000_000)
    floor: int | None = Field(default=None, ge=1, le=99)


class RunIn(BaseModel):
    run_id: int = Field(ge=1)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except math_dungeon.DungeonError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/math/dungeon")
async def dungeon_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """The floors a dungeon can be opened on, today's rewarded runs, and the open run."""
    return await _run(db, math_dungeon.view(db, user))


@router.get("/math/dungeon/layout")
async def dungeon_layout(seed: int, floor: int | None = None, user: User = Depends(current_user),
                         db: AsyncSession = Depends(get_db)):
    """The map of a seed on a floor the player has reached, without entering it."""
    return await _run(db, math_dungeon.preview(db, user, seed, floor))


@router.get("/math/dungeon/run/{run_id}")
async def dungeon_run(run_id: int, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """One run of this player, open or ended (the result screen reads the final numbers here)."""
    async def view():
        return {"run": math_dungeon.run_view(await math_dungeon.get_run(db, user, run_id))}
    return await _run(db, view())


@router.post("/math/dungeon/start")
async def dungeon_start(body: StartIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_dungeon.start(db, user, body.seed, body.floor))


@router.post("/math/dungeon/next")
async def dungeon_next(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """Enter the current room, or ask its next question (the open one if it is waiting)."""
    return await _run(db, math_dungeon.next_question(db, user, body.run_id))


@router.post("/math/dungeon/abandon")
async def dungeon_abandon(body: RunIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_dungeon.abandon(db, user, body.run_id))
