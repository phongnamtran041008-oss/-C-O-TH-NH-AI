"""Stage 3: friends, blocks and reports (spec 15.3)."""
from sqlalchemy import select

from app.models import ChatReport, User
from tests.helpers import register

LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}


async def player(client, db, username, display):
    h, _ = await register(client, username)
    r = await client.post("/character/create", json={"display_name": display, "appearance": LOOK}, headers=h)
    assert r.status_code == 200, r.text
    uid = (await db.execute(select(User.id).where(User.username == username))).scalar_one()
    return h, uid


async def befriend(client, ha, hb, name_b, uid_a):
    r = await client.post("/friends/request", json={"display_name": name_b}, headers=ha)
    assert r.json()["status"] == "pending"
    r = await client.post("/friends/accept", json={"user_id": uid_a}, headers=hb)
    assert r.json()["status"] == "accepted", r.text


async def test_friend_request_flow(client, db):
    ha, a = await player(client, db, "an_01", "An")
    hb, b = await player(client, db, "binh_01", "Bình")
    r = await client.post("/friends/request", json={"display_name": "bình"}, headers=ha)
    assert r.status_code == 200 and r.json()["status"] == "pending"
    inc = (await client.get("/friends", headers=hb)).json()
    assert [p["display_name"] for p in inc["incoming"]] == ["An"] and inc["friends"] == []
    assert (await client.get("/friends", headers=ha)).json()["outgoing"][0]["user_id"] == b
    await client.post("/friends/accept", json={"user_id": a}, headers=hb)
    fa = (await client.get("/friends", headers=ha)).json()
    fb = (await client.get("/friends", headers=hb)).json()
    assert [f["display_name"] for f in fa["friends"]] == ["Bình"]
    assert [f["display_name"] for f in fb["friends"]] == ["An"]
    assert fa["friends"][0]["online"] is False and fb["incoming"] == []
    r = await client.post("/friends/request", json={"display_name": "Bình"}, headers=ha)
    assert r.status_code == 409
    await client.post("/friends/remove", json={"user_id": b}, headers=ha)
    assert (await client.get("/friends", headers=hb)).json()["friends"] == []


async def test_mutual_requests_become_friends(client, db):
    ha, a = await player(client, db, "an_02", "An Hai")
    hb, b = await player(client, db, "binh_02", "Bình Hai")
    await client.post("/friends/request", json={"display_name": "Bình Hai"}, headers=ha)
    r = await client.post("/friends/request", json={"display_name": "An Hai"}, headers=hb)
    assert r.json()["status"] == "accepted"


async def test_request_errors(client, db):
    ha, a = await player(client, db, "an_03", "An Ba")
    assert (await client.post("/friends/request", json={"display_name": "An Ba"}, headers=ha)).status_code == 400
    assert (await client.post("/friends/request", json={"display_name": "Không Có"}, headers=ha)).status_code == 404
    assert (await client.post("/friends/accept", json={"user_id": 999}, headers=ha)).status_code == 404


async def test_block_ends_friendship_and_stops_requests(client, db):
    ha, a = await player(client, db, "an_04", "An Bốn")
    hb, b = await player(client, db, "binh_04", "Bình Bốn")
    await befriend(client, ha, hb, "Bình Bốn", a)
    assert (await client.post("/blocks", json={"user_id": b}, headers=ha)).status_code == 200
    assert (await client.get("/friends", headers=hb)).json()["friends"] == []
    assert [x["display_name"] for x in (await client.get("/blocks", headers=ha)).json()["blocked"]] == ["Bình Bốn"]
    r = await client.post("/friends/request", json={"display_name": "An Bốn"}, headers=hb)
    assert r.status_code == 403
    await client.post("/blocks/remove", json={"user_id": b}, headers=ha)
    assert (await client.get("/blocks", headers=ha)).json()["blocked"] == []


async def test_report(client, db):
    ha, a = await player(client, db, "an_05", "An Năm")
    hb, b = await player(client, db, "binh_05", "Bình Năm")
    r = await client.post("/reports", json={"user_id": b, "message": "nói bậy", "reason": "chat"}, headers=ha)
    assert r.status_code == 200
    rows = (await db.execute(select(ChatReport))).scalars().all()
    assert [(x.reporter_id, x.reported_id, x.message) for x in rows] == [(a, b, "nói bậy")]


async def test_abode_position_ignored_while_in_world(client, db):
    from app.realtime.world import world
    from app.realtime.zone import Player
    ha, a = await player(client, db, "an_10", "An Mười")
    world.players[a] = Player(a, "An Mười", {}, "pham_nhan", 1, 1)
    world.players[a].channel = object()  # standing in some zone
    try:
        r = (await client.post("/character/position", json={"zone_id": "abode", "x": 10, "y": 10},
                               headers=ha)).json()
        assert r == {"ok": False, "ignored": "in_world"}
    finally:
        world.players.pop(a, None)
