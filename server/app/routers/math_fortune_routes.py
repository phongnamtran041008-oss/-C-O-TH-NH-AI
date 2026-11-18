"""Cơ duyên (M10): chance events - an elder with a problem, a sealed chest - with rare rewards.

The state is read with GET /math/fortune; an offer is accepted or declined with the two POSTs;
the questions of an accepted offer are answered through POST /quiz/answer like every other
question (context "math_fortune"), and that answer's response carries a `fortune` block. The
offer itself arrives in the answer of the right math answer that earned it, as
`math.fortune_offer`."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import math_fortune

router = APIRouter(tags=["math"])


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except math_fortune.FortuneError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/math/fortune")
async def fortune_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Read-only to the player, but it lets an offer that ran out of time go (so it commits)."""
    return await _run(db, math_fortune.view(db, user))


@router.post("/math/fortune/accept")
async def fortune_accept(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_fortune.accept(db, user))


@router.post("/math/fortune/decline")
async def fortune_decline(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, math_fortune.decline(db, user))
