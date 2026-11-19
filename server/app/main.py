"""FastAPI entry point: `uvicorn app.main:app` from the server/ folder."""
from __future__ import annotations

import asyncio
import gc
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import admin
from . import db as dbm
from .config import GAME_VERSION, SERVER_DIR, settings
from .realtime import ws as ws_routes
from .realtime.world import world
from .routers import (auth_routes, bee_routes, economy_routes, fishing_routes, game_routes,
                      math_dungeon_routes, math_fortune_routes, math_routes, math_td_routes,
                      realm_routes, rpg_routes, server_routes, social_routes, books_routes)
from .systems import cultivation as _cultivation  # noqa: F401  (registers meditate/tribulation handlers)

log = logging.getLogger("toan_tu_tien")


def run_migrations(url: str | None = None) -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(str(SERVER_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(SERVER_DIR / "alembic"))
    if url:
        cfg.set_main_option("sqlalchemy.url", url)
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_migrate:
        await asyncio.to_thread(run_migrations, None)
    if await admin.sync_admin_usernames():
        log.info("ADMIN_USERNAMES: admin rights granted")
    world.preload()
    # everything loaded so far lives for the whole process: keep it out of the garbage
    # collector's full passes, which would otherwise pause the 20 Hz world tick
    gc.collect()
    gc.freeze()
    await world.start()
    idle_closer = asyncio.create_task(dbm.close_idle_connections(), name="db-idle-closer")
    lan_task = None
    if settings.lan_beacon:
        from . import lan
        lan_task = asyncio.create_task(lan.run(), name="lan-beacon")
    log.info("Toán Tu Tiên server ready")
    yield
    idle_closer.cancel()
    if lan_task:
        lan_task.cancel()
    await world.stop()  # saves every character still standing in the world
    await dbm.engine.dispose()


def create_app(use_lifespan: bool = True) -> FastAPI:
    app = FastAPI(title="Toán Tu Tiên", version=GAME_VERSION, lifespan=lifespan if use_lifespan else None)
    app.include_router(server_routes.router)
    app.include_router(auth_routes.router)
    app.include_router(game_routes.router)
    app.include_router(social_routes.router)
    app.include_router(rpg_routes.router)
    app.include_router(bee_routes.router)
    app.include_router(fishing_routes.router)
    app.include_router(books_routes.router)           # Tàng Thư Các: the shelf of phổ
    app.include_router(economy_routes.router)
    app.include_router(realm_routes.router)
    app.include_router(math_routes.router)
    app.include_router(math_dungeon_routes.router)    # M10: hầm ngục
    app.include_router(math_fortune_routes.router)    # M10: cơ duyên
    app.include_router(math_td_routes.router)         # M10: thủ thành toán
    app.include_router(ws_routes.router)

    @app.exception_handler(HTTPException)
    async def http_exc(_: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, dict) else {"code": "error", "message_vi": str(exc.detail)}
        return JSONResponse(status_code=exc.status_code, content={"error": detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exc(_: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"error": {
            "code": "bad_request", "message_vi": "Dữ liệu gửi lên không hợp lệ.",
            "details": [e.get("msg") for e in exc.errors()][:5]}})

    return app


app = create_app()
