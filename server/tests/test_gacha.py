import random
from collections import Counter

from sqlalchemy import select

from app.models import AuditLog, User
from app.systems.gacha import Banner, expected_rate_with_pity
from tests.econ_helpers import qty
from tests.helpers import register

N = 100_000
LOW = {"pham": 1.0, "linh": 0.0, "huyen": 0.0, "dia": 0.0, "thien": 0.0}   # worst luck on the bee banner
HUYEN_UP = ("huyen", "dia", "thien")


def test_base_rates_100k():
    b = Banner.load("bees")
    rarities, _ = b.roll(N, {}, random.Random(42), use_pity=False)
    c = Counter(rarities)
    for r, p in b.rates.items():
        assert abs(c[r] / N - p) < 0.01, (r, c[r] / N, p)


def test_rates_with_pity_match_expected():
    b = Banner.load("bees")
    state, got = {}, Counter()
    rng = random.Random(7)
    for _ in range(N):
        (r,), state = b.roll(1, state, rng)
        got[r] += 1
    thien = got["thien"] / N
    huyen_up = sum(got[r] for r in HUYEN_UP) / N
    assert abs(thien - expected_rate_with_pity(b, "thien", 90)) < 0.004
    assert abs(huyen_up - expected_rate_with_pity(b, "huyen", 30)) < 0.01
    assert abs(thien - 0.01) < 0.01  # spec: within 1% of the advertised rate


def test_huyen_pity_on_30th():
    b = Banner.load("bees")
    b.rates = dict(LOW)
    out, state = b.roll(30, {}, random.Random(1))
    assert all(r == "pham" for r in out[:29])
    assert out[29] in HUYEN_UP
    assert state["huyen"] == 0


def test_thien_pity_on_90th_and_counter_resets():
    b = Banner.load("bees")
    b.rates = dict(LOW)
    out, state = b.roll(90, {}, random.Random(1))
    assert out[89] == "thien"
    assert state["thien"] == 0 and state["huyen"] == 0
    # the huyen pity kept firing every 30 along the way
    assert out[29] in HUYEN_UP and out[59] in HUYEN_UP


def test_pity_counter_carries_over_between_rolls():
    b = Banner.load("bees")
    b.rates = dict(LOW)
    _, state = b.roll(20, {}, random.Random(1))
    out, _ = b.roll(10, state, random.Random(1))
    assert out[9] in HUYEN_UP


def test_ten_pull_guarantees_linh():
    b = Banner.load("bees")
    b.rates = dict(LOW)
    out, _ = b.roll(10, {}, random.Random(3))
    assert out[9] != "pham"
    b = Banner.load("bees")
    rng = random.Random(5)
    for _ in range(2000):
        out, _ = b.roll(10, {}, rng)
        assert any(r != "pham" for r in out)


def test_the_seed_banner_is_gone():
    from app import balance
    assert set(balance.gacha()["banners"]) == {"bees", "pets"}


# ------------------------------------------------------------------ API
async def _rich(db, n: int) -> User:
    user = (await db.execute(select(User))).scalar_one()
    user.spirit_stones = n
    await db.commit()
    return user


async def test_roll_charges_and_gives_an_egg(client, db):
    h, data = await register(client)
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)
    assert r.status_code == 200, r.text
    assert r.json()["spirit_stones"] == 0          # 300 to start, an egg costs 300
    (egg,) = r.json()["results"]
    assert egg["item"].startswith("trung_ong") and await qty(data["user_id"], egg["item"]) == 1
    logs = (await db.execute(select(AuditLog))).scalars().all()
    assert any(l.delta == -300 and l.reason == "gacha_bees" for l in logs)
    r = await client.post("/gacha/roll", json={"banner": "seeds", "count": 1}, headers=h)
    assert r.status_code == 422                     # no seed banner any more


async def test_cannot_go_negative(client, db):
    h, _ = await register(client)
    assert (await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)).status_code == 200
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "insufficient_funds"
    user = (await db.execute(select(User))).scalar_one()
    assert user.spirit_stones == 0
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 10}, headers=h)
    assert r.status_code == 400
    await db.refresh(user)
    assert user.spirit_stones == 0


async def test_free_roll_once_a_day_on_its_banner(client, db, frozen):
    h, data = await register(client)
    me = (await client.get("/me", headers=h)).json()
    assert me["free_rolls_left"] == 1
    r = await client.post("/gacha/roll", json={"banner": "pets", "count": 1, "free": True}, headers=h)
    assert r.json()["error"]["code"] == "no_free_roll"              # only on free_roll_banner
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1, "free": True}, headers=h)
    assert r.status_code == 200 and r.json()["spirit_stones"] == 300   # free: nothing charged
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1, "free": True}, headers=h)
    assert r.json()["error"]["code"] == "no_free_roll"
    assert (await client.get("/me", headers=h)).json()["free_rolls_left"] == 0
    frozen.advance(hours=17)  # 15:00 UTC+7 -> 08:00 UTC+7 the next day
    assert (await client.post("/gacha/roll", json={"banner": "bees", "count": 1, "free": True},
                              headers=h)).status_code == 200


async def test_daily_limit_on_a_banner_that_counts(client, db, frozen, monkeypatch):
    from app import balance
    cfg = balance.gacha()
    monkeypatch.setitem(cfg, "daily_roll_limit", 3)
    monkeypatch.setitem(cfg["banners"], "bees", {**cfg["banners"]["bees"], "counts_toward_daily_limit": True})
    h, _ = await register(client)
    user = await _rich(db, 10_000)
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 10}, headers=h)
    assert r.json()["error"]["code"] == "daily_limit"
    for _ in range(3):
        assert (await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)).status_code == 200
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)
    assert r.json()["error"]["message_vi"] == "Hôm nay đã quay đủ lượt, mai quay lại nhé."
    assert (await client.post("/gacha/roll", json={"banner": "pets", "count": 1}, headers=h)).status_code == 200
    await db.refresh(user)
    assert user.spirit_stones == 10_000 - 3 * 300 - 500  # failed rolls were not charged
    frozen.advance(hours=17)
    assert (await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)).status_code == 200


async def test_closed_banner(client, monkeypatch):
    h, _ = await register(client)
    from app import balance
    cfg = balance.gacha()
    monkeypatch.setitem(cfg["banners"], "pets", {**cfg["banners"]["pets"], "enabled": False})
    r = await client.post("/gacha/roll", json={"banner": "pets", "count": 1}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "banner_closed"
    monkeypatch.undo()
    # stage 8: the Linh Thú banner is open (300 Linh Thạch is not enough for 500)
    r = await client.post("/gacha/roll", json={"banner": "pets", "count": 1}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "insufficient_funds"
    info = (await client.get("/gacha/banners", headers=h)).json()["banners"]
    assert [b["id"] for b in info] == ["bees", "pets"]
    bees = next(b for b in info if b["id"] == "bees")
    assert bees["rates"]["thien"] == 0.01 and bees["effective_rates_with_pity"]["thien"] > 0.01


async def test_concurrent_spending_never_negative(client, db):
    import asyncio
    h, _ = await register(client, "racer")
    await _rich(db, 900)
    rs = await asyncio.gather(*[client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)
                                for _ in range(6)])
    ok = [r for r in rs if r.status_code == 200]
    assert len(ok) == 3
    user = (await db.execute(select(User))).scalar_one()
    await db.refresh(user)
    assert user.spirit_stones == 0
    spent = (await db.execute(select(AuditLog).where(AuditLog.reason == "gacha_bees",
                                                  AuditLog.currency_or_item == "spirit_stones"))).scalars().all()
    assert sum(l.delta for l in spent) == -900
