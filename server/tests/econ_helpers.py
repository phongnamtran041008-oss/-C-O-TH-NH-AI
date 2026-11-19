"""Shared helpers of the stage 8 tests (luyện đan, Linh Thú, cửa hàng, kinh tế)."""
from sqlalchemy import select, update

from app import db as dbm
from app.models import InventoryItem, User
from app.systems import inventory
from tests.helpers import register

LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}


async def player(client, name="dan_su", stones: int | None = None):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " ").title(), "appearance": LOOK},
                          headers=h)
    assert r.status_code == 200, r.text
    uid = data["user_id"]
    if stones is not None:
        await set_stones(uid, stones)
    return h, uid


async def set_stones(uid: int, n: int, jade: int | None = None) -> None:
    async with dbm.SessionLocal() as db:
        vals = {"spirit_stones": n}
        if jade is not None:
            vals["immortal_jade"] = jade
        await db.execute(update(User).where(User.id == uid).values(**vals))
        await db.commit()


async def stones(uid: int) -> int:
    async with dbm.SessionLocal() as db:
        return (await db.execute(select(User.spirit_stones).where(User.id == uid))).scalar_one()


async def give(uid: int, item_id: str, n: int, bound: bool = False) -> None:
    async with dbm.SessionLocal() as db:
        await inventory.change_item(db, uid, item_id, n, "test", bound=bound)
        await db.commit()


async def qty(uid: int, item_id: str) -> int:
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(InventoryItem).where(InventoryItem.user_id == uid,
                                                             InventoryItem.item_id == item_id))).scalars().all()
        return sum(r.quantity for r in rows)
