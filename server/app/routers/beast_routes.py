"""Linh thú of Thiên Địa Đồ (systems/beasts.py, realtime/beasts.py): the beasts of the lands, sealing
one that yielded with a Phong Ấn Phù, and the Linh Hồ's nose. docs/API.md has the shapes."""
from __future__ import annotations

import math

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..models import User
from ..systems import beasts

router = APIRouter(tags=["beasts"])

SNIFF_VI = {
    "not_in_world": "Con chưa ở ngoài thế giới.",
    "no_nose": "Cần đeo Linh Hồ thì mới đánh hơi được.",
}
DIRS_VI = ("phía Đông", "phía Đông Nam", "phía Nam", "phía Tây Nam", "phía Tây", "phía Tây Bắc", "phía Bắc",
           "phía Đông Bắc")


class SealIn(BaseModel):
    id: str = Field(max_length=32)      # the beast's entity id in the world (b1_linh_ho)


def _world():
    from ..realtime import world as wmod
    return wmod.world


@router.get("/beasts")
async def beasts_view(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    return await beasts.view(db, user)


@router.post("/beasts/seal")
async def seal(body: SealIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    """Phong Ấn Phù on a beast standing near the player that yielded to them."""
    from ..realtime import beasts as wild
    w = _world()
    p = w.players.get(user.id)
    m = wild.seal_target(p, body.id, w.mono())
    if isinstance(m, str):
        raise api_error(400, m, wild.SEAL_REFUSALS_VI[m])
    try:
        pet = await beasts.seal(db, user, m.kind)
    except beasts.BeastError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    if p.channel is not None:
        wild.sealed(p.channel, m, p)
    return {"sealed": m.kind, "name_vi": m.plan["name_vi"], "pet": pet,
            "message_vi": f"Đã thu phục {m.plan['name_vi']}! Mở bảng Linh Thú (phím O) để đeo."}


def direction_vi(dx: float, dy: float) -> str:
    """Which way (dx, dy) points on the map, in words (y grows southwards)."""
    a = math.degrees(math.atan2(dy, dx)) % 360
    return DIRS_VI[int((a + 22.5) // 45) % 8]


@router.get("/beasts/sniff")
async def sniff(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Linh Hồ's gift (gift `sniff`): the weapons still lying in this land within its radius, the
    nearest first, with the way and the distance. (The open lands hold no chests; a bí cảnh's
    chests are its own.)"""
    from ..realtime import lands
    from ..systems import weapons
    w = _world()
    p = w.players.get(user.id)
    if p is None or p.channel is None or p.channel.instance:
        raise api_error(400, "not_in_world", SNIFF_VI["not_in_world"])
    radius = beasts.gift_value(p.pet, "sniff", "radius_tiles") * 16
    if radius <= 0:
        raise api_error(400, "no_nose", SNIFF_VI["no_nose"])
    land = lands.zone_land_id(p.channel.zone_id)
    taken = await weapons._taken(db, user.id)
    found = []
    for spot in weapons.data()["placed"]:
        pos = spot.get("pos")
        if spot["land"] != land or not pos or spot["id"] in taken:
            continue
        x, y = pos[0] * 16 + 8, pos[1] * 16 + 12
        d = math.hypot(x - p.x, y - p.y)
        if d <= radius:
            found.append({"id": spot["id"], "kind": "weapon", "name_vi": weapons.weapon_name(spot["weapon"]),
                          "pos": list(pos), "distance_tiles": round(d / 16, 1),
                          "way_vi": direction_vi(x - p.x, y - p.y)})
    found.sort(key=lambda f: f["distance_tiles"])
    return {"radius_tiles": radius / 16, "found": found}
