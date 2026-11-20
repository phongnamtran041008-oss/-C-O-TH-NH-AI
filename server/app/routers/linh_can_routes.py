"""Linh căn and the Trắc Linh Đài (systems/linh_can.py): the free first test, tẩy linh pills,
the keep-or-take choice and the đồ giám. docs/API.md has the shapes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import linh_can

router = APIRouter(tags=["linh_can"])


class RollIn(BaseModel):
    pill: str = Field(max_length=40)


class ChooseIn(BaseModel):
    keep: bool


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except linh_can.LinhCanError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/linh-can")
async def linh_can_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, linh_can.view(db, user))


@router.post("/linh-can/awaken")
async def awaken(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, linh_can.awaken(db, user))


@router.post("/linh-can/roll")
async def roll(body: RollIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, linh_can.roll(db, user, body.pill))


@router.post("/linh-can/choose")
async def choose(body: ChooseIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, linh_can.choose(db, user, body.keep))
