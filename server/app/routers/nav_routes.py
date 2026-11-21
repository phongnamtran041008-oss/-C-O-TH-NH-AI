"""Chỉ Đường (systems/navigation.py): where this player should go. docs/API.md has the shape."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import current_user
from ..db import get_db
from ..models import User
from ..systems import navigation

router = APIRouter(tags=["nav"])


@router.get("/nav/destinations")
async def destinations(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await navigation.destinations(db, user)
