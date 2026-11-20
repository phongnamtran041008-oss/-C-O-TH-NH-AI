import os
import sys
import tempfile
from pathlib import Path

# KVTT_TEST_URL runs the whole suite against another database, e.g. a throwaway PostgreSQL:
#   KVTT_TEST_URL=postgresql+asyncpg://user:pass@127.0.0.1:5432/kvtt_test python -m pytest -q
# Without it the suite uses its own SQLite file, as it always has.
if os.environ.get("KVTT_TEST_URL"):
    os.environ["DATABASE_URL"] = os.environ["KVTT_TEST_URL"]
else:
    if "KVTT_TEST_DB" not in os.environ:  # guard: this module must configure the DB only once
        os.environ["KVTT_TEST_DB"] = str(Path(tempfile.mkdtemp(prefix="kvtt_test_")) / "test.db")
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{os.environ['KVTT_TEST_DB']}"
os.environ["TIME_SCALE"] = "1"
os.environ["ENV"] = "dev"
os.environ["ALLOW_UNREVIEWED"] = "1"
os.environ["AUTO_MIGRATE"] = "0"
os.environ["RATE_LIMIT"] = "0"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402
import pytest  # noqa: E402
import pytest_asyncio  # noqa: E402
from sqlalchemy import delete  # noqa: E402

from app import clock, models  # noqa: E402
from app import db as dbm  # noqa: E402
from app.auth import limiter  # noqa: E402
from app.main import create_app, run_migrations  # noqa: E402


@pytest.fixture(scope="session")
def migrated():
    run_migrations(os.environ["DATABASE_URL"])  # the real Alembic migration, not create_all
    return True


@pytest.fixture
def frozen():
    c = clock.FrozenClock()
    clock.set_clock(c)
    yield c
    clock.set_clock(clock.Clock())


@pytest_asyncio.fixture
async def app(migrated, frozen):
    yield create_app(use_lifespan=False)
    from app.systems import achievements   # Thành Tựu bumps of this test die with it
    for t in achievements._tasks.values():
        t.cancel()
    achievements._tasks.clear()
    achievements._pending.clear()
    async with dbm.SessionLocal() as db:  # clean tables between tests
        for t in reversed(models.Base.metadata.sorted_tables):
            await db.execute(delete(t))
        await db.commit()
    limiter.reset()


@pytest_asyncio.fixture
async def client(app):
    transport = httpx.ASGITransport(app=app, client=("10.0.0.1", 1234))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def db():
    async with dbm.SessionLocal() as s:
        yield s




def pytest_sessionfinish(session, exitstatus):
    """Thành Tựu: when the whole suite ran, every event a call site may send must have been sent
    by some test (achievements.FIRED), so no event of data/achievements.json is dead."""
    if session.testscollected < 1500 or exitstatus != 0:
        return
    from app.systems import achievements
    missing = sorted(set(achievements.RAW) - achievements.FIRED)
    if missing:
        print(f"Thành Tựu: no test sent the events {missing}")
        session.exitstatus = 1
