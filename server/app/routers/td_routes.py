"""Tàng Thư Các (spec 9.3) REST. This module once also served the word tower defence (/td/*),
which was removed; the tower defence is Thủ Thành Toán now (routers/math_td_routes.py). The
module keeps its name because app/main.py registers it."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import library

router = APIRouter(tags=["library"])


class WearIn(BaseModel):
    title: str | None = Field(default=None, max_length=40)
    frame: str | None = Field(default=None, max_length=40)


class BuyIn(BaseModel):
    item_id: str = Field(max_length=40)


class ClaimIn(BaseModel):
    book: str = Field(max_length=16)
    pct: int = Field(ge=0, le=100)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except library.LibraryError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


# ------------------------------------------------------------------ Tàng Thư Các
@router.get("/library")
async def library_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.overview(db, user))


@router.get("/codex/plant")
async def codex_plant(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.herb_book(db, user))


@router.get("/codex/treasure")
async def codex_treasure(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.treasure_book(db, user))


@router.get("/library/search")
async def library_search(q: str = "", user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.search(db, user, q[:40]))


@router.get("/library/mistakes")
async def library_mistakes(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await library.mistakes(db, user)


@router.post("/library/wear")
async def library_wear(body: WearIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.wear(db, user, body.title, body.frame))


@router.post("/library/buy")
async def library_buy(body: BuyIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.buy(db, user, body.item_id))


@router.post("/library/claim")
async def library_claim(body: ClaimIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, library.claim(db, user, body.book, body.pct))
