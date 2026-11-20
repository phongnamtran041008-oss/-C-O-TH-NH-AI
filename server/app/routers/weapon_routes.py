"""Binh khí của Thiên Địa Đồ (systems/weapons.py): the weapons lying in the lands, picking
them up, wearing them, and Rèn nâng phẩm at the forge. docs/API.md has the shapes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import items, weapons

router = APIRouter(tags=["weapons"])


class ClaimIn(BaseModel):
    id: str = Field(max_length=48)
    land: str | None = Field(default=None, max_length=40)   # where the player is, when the caller knows


class InstanceIn(BaseModel):
    instance_id: int


ERRORS = (weapons.WeaponError, items.ItemError)


async def _run(db: AsyncSession, coro):
    try:
        out = await coro
    except ERRORS as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/weapons")
async def weapons_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await weapons.view(db, user)


@router.post("/weapons/claim")
async def claim(body: ClaimIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, weapons.claim(db, user, body.id, body.land))


@router.post("/weapons/equip")
async def equip(body: InstanceIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, weapons.equip(db, user, body.instance_id))


@router.post("/weapons/unequip")
async def unequip(user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, weapons.unequip(db, user))


@router.get("/weapons/upgrade")
async def upgrade_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await weapons.upgrade_view(db, user)


@router.post("/weapons/upgrade")
async def upgrade(body: InstanceIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    return await _run(db, weapons.upgrade(db, user, body.instance_id))
