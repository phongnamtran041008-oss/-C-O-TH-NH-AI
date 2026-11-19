"""Stage 5: Linh Phong (spec 10). Hive, eggs, honey, feeding, Ong Phổ and the guard-slot rule.
Since the purge of the old word game bees have two roles (hive, guard), eat honey, fish, herbs
and bee pills, and owe nothing to words. Guard bees in combat are tested in test_bee_guard.py."""
import random
import re

import pytest
from sqlalchemy import select

from app import balance, clock
from app.models import Bee, Character, CodexEntry, Hive, InventoryItem, Quest, User
from app.systems import bees as beesys
from app.systems import catalog
from tests.helpers import register

LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}
HAN = re.compile("[" + chr(0x3400) + "-" + chr(0x9FFF) + "]")    # CJK ideographs


async def player(client, db, name="ongchu", character=True):
    h, data = await register(client, name)
    if character:
        r = await client.post("/character/create", json={"display_name": name.replace("_", " ").title(), "appearance": LOOK},
                              headers=h)
        assert r.status_code == 200, r.text
    return h, data["user_id"]


async def item_qty(db, uid, item_id) -> int:
    db.expire_all()
    rows = (await db.execute(select(InventoryItem).where(InventoryItem.user_id == uid,
                                                         InventoryItem.item_id == item_id))).scalars().all()
    return sum(r.quantity for r in rows)


async def give_bee(db, uid, kind="muc", role="hive", slot=None, level=1):
    hive = await db.get(Hive, uid)
    if slot is None:
        used = set((await db.execute(select(Bee.hive_slot).where(Bee.user_id == uid))).scalars().all())
        slot = next(i for i in beesys.open_cells(hive) if i not in used)
    b = Bee(user_id=uid, bee_type=kind, level=level, xp=0, hive_slot=slot, role=role, bond=0,
            obtained_at=clock.now())
    db.add(b)
    await db.commit()
    return Ref(b.id)


class Ref:
    """Just the id: ORM objects expire on every commit of the test session."""

    def __init__(self, id_: int):
        self.id = id_


# ------------------------------------------------------------------ species data (spec 10.1)
def test_species_data_has_no_words_and_edible_favourites():
    sp = catalog.bees()
    assert len(sp) >= 15
    assert {s["rarity"] for s in sp.values()} == {"pham", "linh", "huyen", "dia", "thien"}
    for kind, s in sp.items():
        assert s["element"] in beesys.cfg()["element_names_vi"]
        assert not {"hanzi", "pinyin", "word_id", "word_hanzi", "word_pinyin", "word_vi", "real_word",
                    "pollen"} & set(s), kind
        assert not HAN.search(str(s)), kind
        assert "thụ phấn" not in str(s).lower(), kind
        assert beesys.food_xp(s["favorite"]), (kind, s["favorite"])      # every favourite can be fed
        assert catalog.stack_item(s["favorite"]) is not None, kind
    assert "pollination" not in beesys.cfg() and "word_mastery_bonus_at_100" not in beesys.cfg()
    assert set(beesys.cfg()["role_names_vi"]) == set(beesys.ROLES) == {"hive", "guard"}


def test_food_table():
    assert beesys.food_xp("linh_mat") == 25
    assert beesys.food_xp("truc_diep_thao") == 20
    assert beesys.food_xp("fish_ca_diec") == 12            # a Phàm fish
    assert beesys.food_xp("fish_con") == 100               # a Thiên fish
    assert beesys.food_xp("phong_vuong_dan") == 400        # the bee pill
    for no in ("muc_tinh", "sap_ong", "trung_ong_pham", "fish", "fish_khong_co", "fruit:abc"):
        assert beesys.food_xp(no) is None, no


def test_hex_grid():
    order = beesys.cell_order()
    assert sorted(order) == list(range(30))
    first = order[0]
    assert len(beesys.neighbours(first)) == 6           # the comb opens from its middle
    for i in range(30):
        for n in beesys.neighbours(i):
            assert i in beesys.neighbours(n)            # symmetric


# ------------------------------------------------------------------ hive, eggs, Ong Phổ
async def test_starter_egg_hatch_and_book(client, db):
    h, uid = await player(client, db)
    hv = (await client.get("/hive", headers=h)).json()
    assert hv["cells"] == 5 and len(hv["open_cells"]) == 5 and hv["bees"] == []
    assert [e["item_id"] for e in hv["eggs"]] == ["trung_ong_pham"]
    assert "pollinate_max" not in hv and "pollinate_used" not in hv
    hv2 = (await client.get("/hive", headers=h)).json()
    assert hv2["eggs"][0]["qty"] == 1                   # given once only
    r = (await client.post("/hive/hatch", json={"item_id": "trung_ong_pham"}, headers=h)).json()
    bee = r["bee"]
    assert r["new_species"] and bee["rarity"] == "pham" and bee["slot"] in hv["open_cells"]
    assert bee["role"] == "hive" and bee["level"] == 1 and bee["favorite"] is None
    assert not {"hanzi", "pinyin", "word", "word_mastery", "pollen_per_hour", "real_word"} & set(bee)
    assert await item_qty(db, uid, "trung_ong_pham") == 0
    book = (await client.get("/codex/bee", headers=h)).json()
    assert book["found"] == 1 and book["total"] >= 15
    found = next(e for e in book["entries"] if e["found"])
    assert found["id"] == bee["species"] and found["name_vi"].startswith("Ong ") and found["favorite"] is None
    assert not {"hanzi", "pinyin", "word", "pollen"} & set(found)
    hidden = next(e for e in book["entries"] if not e["found"])
    assert "name_vi" not in hidden and hidden["look"] is None
    q = await db.get(Quest, (uid, "lp1_trung_ong"))
    assert q.state == "done"
    r = await client.post("/hive/hatch", json={"item_id": "trung_ong_pham"}, headers=h)
    assert r.json()["error"]["code"] == "no_egg"


async def test_species_catalog_is_vietnamese_only(client):
    sp = (await client.get("/bees/species")).json()["species"]
    assert sp and all("hanzi" not in s and not HAN.search(str(s)) for s in sp.values())


async def test_hive_full_and_cells(client, db):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    for _ in range(5):
        await give_bee(db, uid)
    r = await client.post("/hive/hatch", json={"item_id": "trung_ong_pham"}, headers=h)
    assert r.json()["error"]["code"] == "hive_full"
    r = (await client.post("/hive/unlock_cell", headers=h)).json()
    assert r["cells"] == 6
    assert (await client.get("/me", headers=h)).json()["spirit_stones"] == 300 - 150
    r = await client.post("/hive/hatch", json={"item_id": "trung_ong_pham"}, headers=h)
    assert r.status_code == 200
    hive = await db.get(Hive, uid)
    await db.refresh(hive)
    hive.cells = 10
    await db.commit()
    u = await db.get(User, uid)
    await db.refresh(u)
    u.spirit_stones = 5000
    await db.commit()
    r = (await client.post("/hive/unlock_cell", headers=h)).json()   # 11th cell needs 3 species
    assert r["error"]["code"] == "need_species"


async def test_move_and_swap(client, db):
    h, uid = await player(client, db)
    hv = (await client.get("/hive", headers=h)).json()
    cells = hv["open_cells"]
    a = await give_bee(db, uid, "muc", slot=cells[0])
    b = await give_bee(db, uid, "hoa", slot=cells[1])
    r = (await client.post("/bees/move", json={"bee_id": a.id, "slot": cells[1]}, headers=h)).json()
    slots = {x["id"]: x["slot"] for x in r["bees"]}
    assert slots[a.id] == cells[1] and slots[b.id] == cells[0]
    locked = next(i for i in range(30) if i not in cells)
    r = await client.post("/bees/move", json={"bee_id": a.id, "slot": locked}, headers=h)
    assert r.json()["error"]["code"] == "cell_locked"


async def test_resonance_same_element_neighbours(client, db):
    h, uid = await player(client, db)
    hv = (await client.get("/hive", headers=h)).json()
    cells = hv["open_cells"]
    centre = cells[0]
    nbs = [c for c in beesys.neighbours(centre) if c in cells]
    assert len(nbs) >= 2
    a = await give_bee(db, uid, "thao", slot=centre)        # Mộc
    await give_bee(db, uid, "hoa", slot=nbs[0])             # Mộc
    await give_bee(db, uid, "vu", slot=nbs[1])              # Thủy: no resonance
    hv = (await client.get("/hive", headers=h)).json()
    bee = next(x for x in hv["bees"] if x["id"] == a.id)
    assert bee["resonance_pct"] == 5


# ------------------------------------------------------------------ honey
async def test_honey_is_made_lazily_and_capped(client, db, frozen):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    b = await give_bee(db, uid, "tra", role="hive")
    hv = (await client.get("/hive", headers=h)).json()
    rate = next(x for x in hv["bees"] if x["id"] == b.id)["honey_per_hour"]
    assert rate == pytest.approx(1.6, abs=0.01) and hv["honey_per_hour"] == pytest.approx(rate)
    frozen.advance(hours=5)
    hv = (await client.get("/hive", headers=h)).json()
    assert hv["honey"] == pytest.approx(rate * 5, abs=0.02)
    assert hv["wax"] == pytest.approx(rate * 5 * 0.1, abs=0.01)
    r = (await client.post("/hive/collect", headers=h)).json()
    assert r["honey"] == 8 and await item_qty(db, uid, "linh_mat") == 8
    frozen.advance(days=10)
    hv = (await client.get("/hive", headers=h)).json()
    assert hv["honey"] == pytest.approx(hv["capacity"], abs=0.5)   # the comb is full, nothing more
    # guard bees make no honey
    await client.post("/hive/collect", headers=h)
    ch = await db.get(Character, uid)
    ch.realm, ch.realm_stage = "luyen_khi", 1
    await db.commit()
    r = await client.post("/bees/role", json={"bee_id": b.id, "role": "guard"}, headers=h)
    assert r.status_code == 200, r.text
    frozen.advance(hours=5)
    hv = (await client.get("/hive", headers=h)).json()
    assert hv["honey"] < 1


async def test_old_pollinate_role_is_a_honey_bee(client, db, frozen):
    """A bee saved with the deleted garden role works as a hive bee, and the role is gone
    from the API."""
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    b = await give_bee(db, uid, "tra", role="pollinate")
    hv = (await client.get("/hive", headers=h)).json()
    bee = next(x for x in hv["bees"] if x["id"] == b.id)
    assert bee["role"] == "hive" and bee["role_vi"] == "Ở tổ" and hv["honey_per_hour"] > 0
    db.expire_all()
    assert (await db.get(Bee, b.id)).role == "hive"                    # fixed in the save
    frozen.advance(hours=5)
    assert (await client.get("/hive", headers=h)).json()["honey"] == pytest.approx(1.6 * 5, abs=0.05)
    r = await client.post("/bees/role", json={"bee_id": b.id, "role": "pollinate"}, headers=h)
    assert r.status_code == 422
    with pytest.raises(beesys.BeeError) as e:
        await beesys.set_role(db, await db.get(User, uid), b.id, "pollinate")
    assert e.value.code == "bad_role"


async def test_collect_honey_finishes_the_quest_step(client, db, frozen):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    await client.get("/quests", headers=h)
    q = await db.get(Quest, (uid, "lp1_trung_ong"))
    q.state = "claimed"
    db.add(Quest(user_id=uid, quest_id="lp3_thu_phan", state="active", progress={"n": 0}))
    await give_bee(db, uid, "tra")
    await db.commit()
    frozen.advance(hours=3)
    r = await client.post("/hive/collect", headers=h)
    assert r.status_code == 200, r.text
    db.expire_all()
    assert (await db.get(Quest, (uid, "lp3_thu_phan"))).state == "done"
    step = next(s for s in catalog.quests()["chains"]["linh_phong"]["steps"] if s["id"] == "lp3_thu_phan")
    assert step["objective"]["type"] == "collect_honey"
    text = str(catalog.quests()["chains"]["linh_phong"]).lower()
    assert "thụ phấn" not in text and "quả chữ" not in text and "vườn" not in text


async def test_sell_honey(client, db):
    h, uid = await player(client, db)
    from app.systems import inventory
    await inventory.change_item(db, uid, "linh_mat", 10, "test")
    await db.commit()
    r = (await client.post("/inventory/sell", json={"item_id": "linh_mat", "qty": 4}, headers=h)).json()
    assert r["earned"] == 8 and r["left"] == 6 and r["spirit_stones"] == 308
    r = await client.post("/inventory/sell", json={"item_id": "trung_ong_pham", "qty": 1}, headers=h)
    assert r.json()["error"]["code"] == "not_sellable"


# ------------------------------------------------------------------ feeding
async def test_feeding_levels_and_favourite(client, db):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    b = await give_bee(db, uid, "hoa_diem")     # likes Mặc Linh Chi
    assert catalog.bees()["hoa_diem"]["favorite"] == "mac_linh_chi"
    db.add(CodexEntry(user_id=uid, codex="bee", entry_id="hoa_diem", discovered_at=clock.now(),
                      progress={"hatched": 1, "favorite_known": False, "best_level": 1}))
    from app.systems import inventory
    await inventory.change_item(db, uid, "linh_mat", 5, "test")
    await inventory.change_item(db, uid, "mac_linh_chi", 2, "test")
    await inventory.change_item(db, uid, "fish_ca_diec", 1, "test")
    await db.commit()
    hv = (await client.get("/hive", headers=h)).json()
    assert {f["food"] for f in hv["foods"]} == {"linh_mat", "mac_linh_chi", "fish_ca_diec"}
    r = (await client.post("/bees/feed", json={"bee_id": b.id, "food": "linh_mat"}, headers=h)).json()
    assert r["xp_gained"] == 25 and not r["favorite"] and r["bond"] == 2
    r = (await client.post("/bees/feed", json={"bee_id": b.id, "food": "fish_ca_diec"}, headers=h)).json()
    assert r["xp_gained"] == 12 and not r["favorite"]
    r = (await client.post("/bees/feed", json={"bee_id": b.id, "food": "mac_linh_chi"}, headers=h)).json()
    assert r["favorite"] and r["favorite_discovered"] and r["xp_gained"] == 90 and r["bond"] == 12
    assert r["favorite_vi"] == "Mặc Linh Chi"
    assert r["level"] == 3   # 25 + 12 + 90 = 127: level 2 at 50, level 3 at 50 + 70
    book = (await client.get("/codex/bee", headers=h)).json()
    e = next(x for x in book["entries"] if x["id"] == "hoa_diem")
    assert e["favorite_known"] and e["favorite"] == "Mặc Linh Chi" and e["best_level"] == 3
    r = await client.post("/bees/feed", json={"bee_id": b.id, "food": "fish_ca_diec"}, headers=h)
    assert r.json()["error"]["code"] == "no_food"
    for bad in ("muc_tinh", "fruit:abc"):
        r = await client.post("/bees/feed", json={"bee_id": b.id, "food": bad}, headers=h)
        assert r.json()["error"]["code"] == "bad_food", bad


async def test_level_and_bond_make_bees_stronger(client, db):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    weak = await give_bee(db, uid, "muc", level=1)
    strong = await give_bee(db, uid, "muc", level=10)
    (await db.get(Bee, strong.id)).bond = 100
    await db.commit()
    hv = (await client.get("/hive", headers=h)).json()
    w = next(x for x in hv["bees"] if x["id"] == weak.id)
    s = next(x for x in hv["bees"] if x["id"] == strong.id)
    assert s["guard"]["atk"] > w["guard"]["atk"] and s["honey_per_hour"] > w["honey_per_hour"]
    # a level-1 Phàm bee with no bond is its species' base numbers (times its resonance)
    k = 1 + w["resonance_pct"] / 100
    assert w["guard"] == {"hp": int(round(30 * k)), "atk": round(3 * k, 1), "cd": 1.5}


async def test_release_gives_wax(client, db):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    b = await give_bee(db, uid, "bang_tam")
    r = (await client.post("/bees/release", json={"bee_id": b.id}, headers=h)).json()
    assert r["wax"] == 4 and await item_qty(db, uid, "sap_ong") == 4
    assert await db.get(Bee, b.id) is None


async def test_upgrade_hive_needs_materials(client, db):
    h, uid = await player(client, db)
    await client.get("/hive", headers=h)
    r = await client.post("/hive/upgrade", headers=h)
    assert r.json()["error"]["code"] == "no_material"
    from app.systems import inventory
    await inventory.change_item(db, uid, "sap_ong", 5, "test")
    await inventory.change_item(db, uid, "go_linh_moc", 3, "test")
    await db.commit()
    r = (await client.post("/hive/upgrade", headers=h)).json()
    assert r["level"] == 2 and r["capacity"] == 80 and r["decorations"][0]["id"] == "den_long"
    assert await item_qty(db, uid, "sap_ong") == 0
    r = (await client.post("/hive/decoration", json={"decoration": "den_long", "on": False}, headers=h)).json()
    assert not r["decorations"][0]["on"]
    r = await client.post("/hive/decoration", json={"decoration": "hoa_sen", "on": True}, headers=h)
    assert r.json()["error"]["code"] == "decoration_locked"


# ------------------------------------------------------------------ gacha (spec 13)
async def test_bee_gacha_gives_eggs(client, db):
    h, uid = await player(client, db)
    r = (await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)).json()
    assert r["spirit_stones"] == 0 and r["results"][0]["item"].startswith("trung_ong_")
    assert await item_qty(db, uid, r["results"][0]["item"]) >= 1
    r = await client.post("/gacha/roll", json={"banner": "bees", "count": 1}, headers=h)
    assert r.json()["error"]["code"] == "insufficient_funds"
    u = await db.get(User, uid)
    await db.refresh(u)
    u.immortal_jade = 50
    await db.commit()
    r = (await client.post("/gacha/roll", json={"banner": "bees", "count": 10, "currency": "immortal_jade"},
                           headers=h)).json()
    assert r["immortal_jade"] == 5 and len(r["results"]) == 10
    assert any(x["rarity"] != "pham" for x in r["results"])     # ten-pull: at least one Linh
    if balance.gacha().get("free_roll_banner") == "bees":    # the daily free roll: once a day
        r = await client.post("/gacha/roll", json={"banner": "bees", "free": True}, headers=h)
        assert r.status_code == 200, r.text
    r = await client.post("/gacha/roll", json={"banner": "bees", "free": True}, headers=h)
    assert r.json()["error"]["code"] == "no_free_roll"
    info = (await client.get("/gacha/banners", headers=h)).json()["banners"]
    bees = next(b for b in info if b["id"] == "bees")
    assert bees["enabled"] and bees["alt_price"] == {"immortal_jade": 5}


def test_bee_banner_rates_and_pity():
    from app.systems.gacha import Banner
    b = Banner.load("bees")
    rng = random.Random(7)
    counts = {r: 0 for r in b.rarities}
    state = {}
    for _ in range(20000):
        out, state = b.roll(1, state, rng, use_pity=False)
        counts[out[0]] += 1
    assert abs(counts["pham"] / 20000 - 0.60) < 0.015
    out, _ = b.roll(1, {"thien": 89, "huyen": 0}, rng)
    assert out == ["thien"]
    out, _ = b.roll(1, {"thien": 0, "huyen": 29}, rng)
    assert out[0] in ("huyen", "dia", "thien")


# ------------------------------------------------------------------ guard slots (spec 7.3, 10.2.3)
@pytest.mark.parametrize("realm,slots", [("pham_nhan", 0), ("luyen_khi", 2), ("truc_co", 3), ("kim_dan", 4),
                                         ("nguyen_anh", 5), ("hoa_than", 6), ("luyen_hu", 7), ("hop_the", 8),
                                         ("dai_thua", 9)])
async def test_guard_slots_follow_realm(client, db, realm, slots):
    h, uid = await player(client, db, f"ho_ve_{realm[:4]}{slots}")
    await client.get("/hive", headers=h)
    hive = await db.get(Hive, uid)
    await db.refresh(hive)
    hive.cells = 12
    ch = await db.get(Character, uid)
    ch.realm, ch.realm_stage = realm, 0 if realm == "pham_nhan" else 1
    await db.commit()
    ids = [(await give_bee(db, uid, "muc")).id for _ in range(max(6, slots + 1))]
    ok = 0
    for bid in ids:
        r = await client.post("/bees/role", json={"bee_id": bid, "role": "guard"}, headers=h)
        if r.status_code == 200:
            ok += 1
        else:
            assert r.json()["error"]["code"] == ("no_guard_slot" if slots == 0 else "guard_full")
    assert ok == slots
    hv = (await client.get("/hive", headers=h)).json()
    assert hv["guard_slots"] == slots and hv["guard_used"] == slots
    assert len(await beesys.guard_loadout(db, uid)) == slots


def test_guard_slot_table_matches_spec():
    assert beesys.cfg()["guard"]["slots_by_realm"] == {"pham_nhan": 0, "luyen_khi": 2, "truc_co": 3,
                                                        "kim_dan": 4, "nguyen_anh": 5, "hoa_than": 6,
                                                        "luyen_hu": 7, "hop_the": 8, "dai_thua": 9}
