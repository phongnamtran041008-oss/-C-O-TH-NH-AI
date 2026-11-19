"""Tàng Thư Các shelf of phổ (spec 9.3, 8.4): every book counted with its % and milestones,
titles and portrait frames from milestones, the Bảo Vật Phổ, the Thủ Thư's đan phương."""
from app import clock
from app.models import CodexEntry, FishCatch, Hive, User
from app.systems import books, catalog
from tests.helpers import register

LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}


async def player(client, name="thu_thu"):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " ").title(), "appearance": LOOK},
                          headers=h)
    assert r.status_code == 200, r.text
    return h, data["user_id"]


def book(view: dict, bid: str) -> dict:
    return next(b for b in view["books"] if b["id"] == bid)


async def test_overview_counts_every_book(client):
    h, uid = await player(client)
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        db.add(FishCatch(user_id=uid, fish_id="ca_diec", count=2, best_size_cm=12.0, first_caught_at=clock.now()))
        db.add(CodexEntry(user_id=uid, codex="monster", entry_id="ink_slime", discovered_at=clock.now(), progress={}))
        db.add(CodexEntry(user_id=uid, codex="monster", entry_id="td_muc_con", discovered_at=clock.now(), progress={}))
        await db.commit()
    v = (await client.get("/books", headers=h)).json()
    assert [b["id"] for b in v["books"]] == ["monster", "bee", "fish", "treasure", "pet"]
    assert book(v, "fish")["found"] == 1 and book(v, "fish")["total"] == len(catalog.fish())
    assert book(v, "monster")["found"] == 2
    for b in v["books"]:
        assert [m["pct"] for m in b["milestones"]] == [25, 50, 75, 100]
        assert all(not m["ready"] for m in b["milestones"])
    assert (await client.get("/library", headers=h)).status_code == 404        # the word library is gone


async def test_milestones_are_claimed_once_when_reached(client):
    h, uid = await player(client)
    r = await client.post("/books/claim", json={"book": "fish", "pct": 25}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_yet"
    fish = list(catalog.fish())
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        for f in fish[:(len(fish) + 3) // 4]:
            db.add(FishCatch(user_id=uid, fish_id=f, count=1, best_size_cm=10.0, first_caught_at=clock.now()))
        await db.commit()
    stones = (await client.get("/me", headers=h)).json()["spirit_stones"]
    r = await client.post("/books/claim", json={"book": "fish", "pct": 25}, headers=h)
    assert r.status_code == 200, r.text
    assert (await client.get("/me", headers=h)).json()["spirit_stones"] == stones + 100
    assert (await client.post("/books/claim", json={"book": "fish", "pct": 25}, headers=h)).status_code == 409
    v = (await client.get("/books", headers=h)).json()
    ms = {m["pct"]: m for m in book(v, "fish")["milestones"]}
    assert ms[25]["claimed"] and not ms[50]["ready"]
    for bad in ("nope", "plant", "discovery"):           # the word books are gone
        assert (await client.post("/books/claim", json={"book": bad, "pct": 25}, headers=h)).status_code == 400


async def test_titles_and_hive_cells_from_milestones(client):
    h, uid = await player(client)
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        for bid in list(catalog.bees())[:(len(catalog.bees()) + 1) // 2]:
            db.add(CodexEntry(user_id=uid, codex="bee", entry_id=bid, discovered_at=clock.now(), progress={}))
        await db.commit()
    await client.get("/hive", headers=h)
    async with dbm.SessionLocal() as db:
        cells = (await db.get(Hive, uid)).cells
    assert (await client.post("/books/claim", json={"book": "bee", "pct": 50}, headers=h)).status_code == 200
    async with dbm.SessionLocal() as db:
        assert (await db.get(Hive, uid)).cells == cells + 1
    async with dbm.SessionLocal() as db:
        for f in list(catalog.fish())[:(len(catalog.fish()) + 1) // 2]:
            db.add(FishCatch(user_id=uid, fish_id=f, count=1, best_size_cm=10.0, first_caught_at=clock.now()))
        await db.commit()
    v = (await client.post("/books/claim", json={"book": "fish", "pct": 50}, headers=h)).json()
    assert v["titles"] == ["Lão Câu Thủ"]


async def test_treasure_book_lists_everything_ever_owned(client):
    h, uid = await player(client)
    tb = (await client.get("/codex/treasure", headers=h)).json()
    start = tb["found"]
    pill = next(e for e in tb["entries"] if e["id"] == "hoi_huyet_dan")
    assert tb["total"] == len(books.treasure_catalog()) and not pill["found"] and "name_vi" not in pill
    from app import db as dbm
    from app.systems import inventory
    async with dbm.SessionLocal() as db:
        await inventory.change_item(db, uid, "hoi_huyet_dan", 2, "test")
        await inventory.change_item(db, uid, "hoi_huyet_dan", -2, "test")     # used up: still in the book
        await db.commit()
    tb = (await client.get("/codex/treasure", headers=h)).json()
    pill = next(e for e in tb["entries"] if e["id"] == "hoi_huyet_dan")
    assert tb["found"] == start + 1 and pill["found"] and pill["name_vi"] == "Hồi Huyết Đan" and pill["first_at"]
    v = (await client.get("/books", headers=h)).json()
    assert book(v, "treasure")["found"] == start + 1


async def test_wear_a_title_and_a_frame(client):
    h, uid = await player(client)
    r = await client.post("/books/wear", json={"title": "Kẻ Săn Mực"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_title"     # not earned yet
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.flags = {**(u.flags or {}), "titles": ["Kẻ Săn Mực"], "frames": ["khung_muc"]}
        await db.commit()
    v = (await client.post("/books/wear", json={"title": "Kẻ Săn Mực", "frame": "khung_muc"}, headers=h)).json()
    assert v["title"] == "Kẻ Săn Mực" and v["frame"] == "khung_muc"
    me = (await client.get("/me", headers=h)).json()
    assert me["title"] == "Kẻ Săn Mực" and me["frame"] == "khung_muc"
    v = (await client.post("/books/wear", json={"title": ""}, headers=h)).json()
    assert v["title"] is None and v["frame"] == "khung_muc"


async def test_badges_only_the_word_books_gave_are_dropped(client):
    """A title or frame earned from the removed word books (Bách Thảo Phổ, Sổ Phát Hiện) is no
    longer listed, worn or shown on /me."""
    h, uid = await player(client)
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.flags = {**(u.flags or {}), "titles": ["Bách Thảo Tiên", "Kẻ Săn Mực"], "frames": ["khung_truc"],
                   "title": "Bách Thảo Tiên", "frame": "khung_truc"}
        await db.commit()
    me = (await client.get("/me", headers=h)).json()
    assert me["title"] is None and me["frame"] is None
    v = (await client.get("/books", headers=h)).json()
    assert v["titles"] == ["Kẻ Săn Mực"] and v["frames"] == [] and v["title"] is None
    r = await client.post("/books/wear", json={"title": "Bách Thảo Tiên"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_title"


async def test_buy_a_recipe_once_at_the_librarians_desk(client, monkeypatch):
    h, uid = await player(client)
    v = (await client.get("/books", headers=h)).json()
    assert v["shop"] and {s["kind"] for s in v["shop"]} == {"recipe"}       # đan phương only, no bí kíp
    assert not v["at_desk"]
    r = await client.post("/books/buy", json={"item_id": "dp_hoi_khi"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "too_far"      # must stand by the Thủ Thư
    monkeypatch.setattr(books, "at_desk", lambda uid: True)
    r = await client.post("/books/buy", json={"item_id": "dp_truc_co"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_enough"   # 300 Linh Thạch at the start
    from app import db as dbm
    async with dbm.SessionLocal() as db:
        (await db.get(User, uid)).spirit_stones = 1000
        await db.commit()
    r = await client.post("/books/buy", json={"item_id": "dp_hoi_khi"}, headers=h)
    assert r.status_code == 200, r.text
    dp = next(s for s in r.json()["shop"] if s["item_id"] == "dp_hoi_khi")
    assert dp["have"] == 1 and dp["learned"]
    assert (await client.get("/me", headers=h)).json()["spirit_stones"] == 1000 - dp["price"]
    r = await client.post("/books/buy", json={"item_id": "dp_hoi_khi"}, headers=h)
    assert r.json()["error"]["code"] == "already_have"
    assert (await client.post("/books/buy", json={"item_id": "hoi_huyet_dan"}, headers=h)).json()["error"]["code"] \
        == "not_sold"
