"""Tàng Thư Các shelf of phổ (spec 9.3) REST: systems/books.py. The math scrolls of the library
are /math/library (routers/math_routes.py)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import books

router = APIRouter(tags=["books"])


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
    except books.BooksError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/books")
async def books_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, books.overview(db, user))


@router.get("/codex/treasure")
async def codex_treasure(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, books.treasure_book(db, user))


@router.post("/books/wear")
async def books_wear(body: WearIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, books.wear(db, user, body.title, body.frame))


@router.post("/books/buy")
async def books_buy(body: BuyIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, books.buy(db, user, body.item_id))


@router.post("/books/claim")
async def books_claim(body: ClaimIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    user = await db.merge(user)
    return await _run(db, books.claim(db, user, body.book, body.pct))
