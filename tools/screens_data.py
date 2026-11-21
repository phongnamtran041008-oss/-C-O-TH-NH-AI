"""Real server payloads for tools/audit_screens.py.

Starts the FastAPI app in this process on a throw-away SQLite file (the real Alembic
migration), makes one player rich in everything a screen lists - every stackable item of the
catalog, one piece of every equipment, a few Linh Thú, a linh căn - and GETs what the screens
read. Nothing listens on a port and nothing leaves the machine.

    payloads = harvest()        # {"/inventory": {...}, "/shop": {...}, ...}

The caller must import this module before anything imports `app.db`: importing it points the
server's database at a throw-away file and loads `app.db` at once. The environment variables it
needs are set only while it works and put back afterwards, so a test process that later starts
a real server (client/tests/driver.py) inherits nothing from here."""
from __future__ import annotations

import asyncio
import os
import random
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_DB = Path(tempfile.mkdtemp(prefix="screens_audit_")) / "audit.db"
ENV = {"DATABASE_URL": f"sqlite+aiosqlite:///{_DB}", "ENV": "dev", "ALLOW_UNREVIEWED": "1", "AUTO_MIGRATE": "0",
       "RATE_LIMIT": "0", "TIME_SCALE": "1"}
sys.path.insert(0, str(ROOT / "server"))


class _Env:
    """ENV in os.environ inside the block, the old values after it."""

    def __enter__(self):
        self.saved = {k: os.environ.get(k) for k in ENV}
        os.environ.update(ENV)

    def __exit__(self, *exc):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


# Inside one test process another test may have imported `app.db` first, or re-pointed its engine
# at a database of its own (several client flow tests do): harvest() points the engine at the
# throw-away file for the time it works and puts the old one back afterwards.
if "app.db" not in sys.modules:
    with _Env():
        import app.db  # noqa: E402,F401 - the engine is made now, on the throw-away file

GETS = ["/me", "/character", "/inventory", "/weapons", "/shop", "/pets", "/linh-can", "/achievements", "/guide",
        "/math/skills", "/math/dungeon", "/math/td", "/math/fortune", "/math/path", "/math/tree",
        "/math/placement?subject_id=giai_tich", "/books", "/cultivation", "/quests"]
LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}


async def _harvest() -> dict:
    import httpx
    from sqlalchemy import update

    from app import db as dbm
    from app.main import create_app
    from app.models import User
    from app.systems import catalog, inventory, items, linh_can, pets

    app = create_app(use_lifespan=False)
    out: dict = {}
    transport = httpx.ASGITransport(app=app, client=("10.0.0.1", 1234))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/auth/register", json={"username": "kiem_tra_man_hinh", "password": "secret123"})
        data = r.json()
        h = {"Authorization": f"Bearer {data['token']}"}
        uid = data["user_id"]
        r = await c.post("/character/create", json={"display_name": "Thuong Quan Vo", "appearance": LOOK},
                         headers=h)
        if r.status_code != 200:
            out.setdefault("_failed", {})["/character/create"] = f"{r.status_code} {r.text[:200]}"
        async with dbm.SessionLocal() as db:
            await db.execute(update(User).where(User.id == uid).values(spirit_stones=98765432, immortal_jade=8888))
            ids = (list(catalog.pills()) + list(catalog.materials()) + list(catalog.math_drops())
                   + list(catalog.rods()) + list(catalog.baits()) + [f"fish_{f}" for f in catalog.fish()])
            for k, item_id in enumerate(ids):
                try:
                    await inventory.change_item(db, uid, item_id, 1 + (k * 37) % 999, "audit")
                except Exception:       # noqa: BLE001 - an item the inventory refuses is simply left out
                    pass
            rarities = list(catalog.equipment()["rarities"])[::-1]
            for k, item_id in enumerate(catalog.equipment()["items"]):
                try:
                    await items.grant_equipment(db, uid, item_id, rarities[k % len(rarities)], "audit")
                except Exception:       # noqa: BLE001
                    pass
            user = await db.get(User, uid)
            try:
                await pets.resolve_gacha(db, user, ["legendary", "epic", "rare", "common", "epic", "rare"],
                                         random.Random(7))
            except Exception:           # noqa: BLE001
                pass
            await db.commit()
        for path in ("/linh-can/awaken",):
            await c.post(path, json={}, headers=h)
        for path in GETS:
            r = await c.get(path, headers=h)
            if r.status_code == 200:
                out[path] = r.json()
            else:
                out.setdefault("_failed", {})[path] = f"{r.status_code} {r.text[:160]}"
        del linh_can
    return out


_CACHE: dict | None = None


def harvest() -> dict:
    global _CACHE
    if _CACHE is None:
        with _Env():
            from app import db as dbm
            from app.main import run_migrations
            old = (dbm.engine, dbm.SessionLocal)
            dbm.configure(ENV["DATABASE_URL"])      # (always: a test run earlier may have re-pointed it)
            try:
                run_migrations(ENV["DATABASE_URL"])     # (it runs its own event loop)
                _CACHE = asyncio.run(_harvest())
            finally:
                dbm.engine, dbm.SessionLocal = old
    return _CACHE


if __name__ == "__main__":
    got = harvest()
    for k, v in got.items():
        print(k, type(v).__name__, (list(v)[:12] if isinstance(v, dict) else len(v)))
