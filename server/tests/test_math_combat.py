"""M7: quái = lỗi sai, ghi chú lỗi sai and Lò Toán.

The same machinery as test_combat (a real database, a world on a fake clock whose tick is
called by hand), but in Loạn Số Cốc, where every monster stands for a mistake and asks a
math question about the micro-skill that mistake belongs to - since the open-world rule
(world_plan.json "combat"), when it lands a blow on the player.
"""
import pytest
import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.learning import math_path
from app.models import CodexEntry, EquipmentInstance, InventoryItem, MathAnswer, User
from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import catalog, math_combat
from tests.helpers import answer_key
from tests.test_math_loop import right_answer, wrong_answer
from tests.test_combat import FakeMono, fighter, last, run, settle  # noqa: F401  (fixtures/helpers)

VALLEY = "loan_so_coc"
SLIME_MA = "dstt_phan_tu_ma"          # floor 1, tập hợp: the gentlest of them


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    """The same world fixture test_combat uses: a fake clock, ticked by hand."""
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def at_math_monster(w: World, s, kind: str = SLIME_MA):
    """Stand the player on a mistake-monster of Loạn Số Cốc, with the others out of the way."""
    assert w.join(s, "truc_lam_thon", "abode")
    ch = w._pick_channel(VALLEY)
    m0 = next(m for m in ch.monsters if m.kind == kind)
    w._place(s, VALLEY, m0.x, m0.y, "down")
    for m in ch.monsters:
        if m is not m0:
            m.mode, m.respawn_at = "dead", 1e12
    return s.player, m0


async def hit(w: World, p, m) -> None:
    w.mono.t += 1.0
    assert combat.attack(p, m.eid, w.mono(), w.rng) is None
    await settle(w)


async def blow(w: World, s, p, m) -> dict | None:
    """Hit it so it fights back, then stand still and let its telegraphed blow land: the
    question that decides the blow (Phản Đòn or not)."""
    await hit(w, p, m)
    s.sent.clear()
    m.atk_ready = 0.0
    run(w, combat.windup() + 0.2)
    await settle(w)
    return last(s, "q")


async def answer(client, h, s, right: bool):
    q = last(s, "q")["q"]
    key = await answer_key(q["session_id"])
    a = right_answer(q, key) if right else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": a}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def give(uid: int, item_id: str, qty: int = 1) -> None:
    async with dbm.SessionLocal() as db:
        db.add(InventoryItem(user_id=uid, item_id=item_id, quantity=qty, bound=False))
        await db.commit()


# ------------------------------------------------------------------ the data itself
def test_every_mistake_monster_points_at_a_real_skill_and_section():
    """A monster that names a micro-skill nobody teaches would ask a question that cannot be
    built, and a note that opens nothing."""
    from app.learning import math_library
    docs = math_library.documents()
    for kind, m in catalog.monsters().items():
        if not math_combat.is_mistake_monster(m):
            continue
        subject = math_path.subject(m["subject"])
        floor = next((f for f in subject.floors if f.number == m["floor"]), None)
        assert floor is not None, (kind, m["floor"])
        assert m["skill"] in {s.id for s in floor.skills}, (kind, m["skill"])
        doc = next((d for d in docs.values() if m["skill"] in d.skills), None)
        assert doc is not None, (kind, m["skill"])
        note = catalog.stack_item(m["note"])
        assert note is not None and note["kind"] == "note", (kind, m["note"])
        assert note["skill"] == m["skill"], (kind, note["skill"], m["skill"])
        assert m["mistake_vi"].strip(), kind


def test_the_valley_spawns_only_mistake_monsters():
    from app.realtime import maps
    areas = maps.load(VALLEY).monster_areas
    assert areas, "Loạn Số Cốc has no monster area at all"
    for a in areas:
        info = catalog.monsters()[a.props["monster"]]
        assert math_combat.is_mistake_monster(info), a.props["monster"]


# ------------------------------------------------------------------ the fight
async def test_a_mistake_monster_asks_about_its_own_micro_skill(client, gw):
    h, uid, s = await fighter(client, gw, "toan_1", "Toán Một")
    p, m = at_math_monster(gw, s)
    q = await blow(gw, s, p, m)
    assert q and q["mid"] == m.eid and q["hit"]["dmg"] > 0
    assert q["q"]["context"] == "math_combat"
    assert "answer_key" not in q["q"]
    meta = q["q"]["math"]
    info = catalog.monsters()[SLIME_MA]
    assert meta["skill"] == info["skill"] and meta["floor"] == info["floor"]
    assert meta["tier"] == 1, meta           # a fresh player starts at the floor's lowest tier
    assert q["q"]["math"]["doc"]["id"], "the card must be able to open Tàng Thư Các"
    assert p.protected(gw.mono())


async def test_a_right_answer_is_a_parry_and_is_written_to_the_learning_log(client, gw):
    h, uid, s = await fighter(client, gw, "toan_2", "Toán Hai")
    p, m = at_math_monster(gw, s)
    m.max_hp = m.hp = 10000.0
    hp = p.hp
    await blow(gw, s, p, m)
    res = await answer(client, h, s, True)
    assert res["correct"] and res["combat"]["parry"] and res["combat"]["damage"] > 0 and p.hp == hp
    info = catalog.monsters()[SLIME_MA]
    assert res["xp"]["gained"] == math_path.xp_for_tier(1)
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().all()
        assert len(rows) == 1
        a = rows[0]
        assert a.run_id is None and a.correct and a.skill_id == info["skill"] and a.tier == 1
        assert a.subject_id == info["subject"] and a.floor == info["floor"]


async def test_a_wrong_answer_hurts_and_is_logged_as_wrong(client, gw):
    h, uid, s = await fighter(client, gw, "toan_3", "Toán Ba")
    p, m = at_math_monster(gw, s)
    m.max_hp = m.hp = 10000.0
    await blow(gw, s, p, m)
    hp_before = p.hp
    res = await answer(client, h, s, False)
    assert not res["correct"] and not res["combat"]["parry"]
    assert p.hp < hp_before                                     # the blow lands in full
    async with dbm.SessionLocal() as db:
        a = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalars().one()
        assert not a.correct and a.run_id is None


async def test_the_question_follows_the_tier_the_player_has_opened(client, gw):
    """Rule 3.3: the monster asks at the tier this player's own answer log has opened, so the
    same monster keeps being worth something later on."""
    h, uid, s = await fighter(client, gw, "toan_4", "Toán Bốn")
    info = catalog.monsters()[SLIME_MA]
    cfg = math_path.cfg()
    window = cfg["tier_unlock"]["window"]
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        assert await math_combat.tier_for(db, uid, info["skill"], info["floor"]) == 1
        for n in range(window):                                 # a full window of right answers at tier 1
            db.add(MathAnswer(user_id=uid, run_id=None, subject_id=info["subject"], skill_id=info["skill"],
                              floor=info["floor"], tier=1, item_id=f"x{n}", qtype="true_false",
                              fingerprint=f"f{n}", correct=True, timed_out=False, review=False,
                              answer_ms=800, answered_at=__import__("app.clock", fromlist=["now"]).now()))
        await db.commit()
        assert await math_combat.tier_for(db, uid, info["skill"], info["floor"]) == 2
        q = await math_combat.question_for(db, user, info)
        assert q is not None and q.public()["math"]["tier"] == 2


async def test_killing_one_drops_its_note_and_its_material(client, gw, monkeypatch):
    """The note is the point of the fight, so the test makes the drop certain rather than
    hoping: every chance in this monster's table is turned up to 1."""
    info = dict(catalog.monsters()[SLIME_MA])
    info["drops"] = [{**d, "chance": 1.0} for d in info["drops"]] + [
        {"item": catalog.monsters()[SLIME_MA]["note"], "chance": 1.0, "qty": [1, 1]}]
    monkeypatch.setitem(catalog.monsters(), SLIME_MA, info)
    h, uid, s = await fighter(client, gw, "toan_5", "Toán Năm")
    p, m = at_math_monster(gw, s)
    assert not m.shield, "out in the wild a normal monster falls to plain hits"
    for _ in range(60):
        if not m.alive:
            break
        await hit(gw, p, m)
    assert not m.alive
    await settle(gw)
    loot = last(s, "loot")
    assert loot and loot["monster"] == info["name_vi"]
    got = {i["item_id"] if isinstance(i, dict) and "item_id" in i else i.get("id", ""): i for i in loot["items"]}
    assert info["note"] in got or any(info["note"] in str(i) for i in loot["items"]), loot["items"]
    async with dbm.SessionLocal() as db:
        rows = {r.item_id: r.quantity for r in (await db.execute(
            select(InventoryItem).where(InventoryItem.user_id == uid))).scalars().all()}
        assert rows.get(info["note"], 0) >= 1 and rows.get("manh_tap_hop", 0) >= 1
        e = await db.get(CodexEntry, (uid, "monster", SLIME_MA))
        assert e is not None and e.progress["kills"] == 1


# ------------------------------------------------------------------ the note
async def test_reading_a_note_opens_the_right_part_of_tang_thu_cac(client, gw):
    h, uid, s = await fighter(client, gw, "toan_6", "Toán Sáu")
    note = catalog.monsters()[SLIME_MA]["note"]
    await give(uid, note)
    r = await client.get("/inventory", headers=h)
    assert r.status_code == 200, r.text
    row = next(i for i in r.json()["items"] if i["item_id"] == note)
    assert row["usable"] and row["kind"] == "note"
    r = await client.post("/inventory/use", json={"item_id": note}, headers=h)
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["skill"] == catalog.stack_item(note)["skill"]
    assert out["doc"]["id"] and isinstance(out["doc"]["block"], int)
    r = await client.get("/inventory", headers=h)                 # reading never spends it
    assert any(i["item_id"] == note for i in r.json()["items"])


# ------------------------------------------------------------------ Lò Toán
async def test_crafting_needs_the_note_as_well_as_the_materials(client, gw):
    h, uid, s = await fighter(client, gw, "toan_7", "Toán Bảy")
    recipe = "but_tap_hop"
    r = catalog.math_crafting()["recipes"][recipe]
    for i in r["ingredients"]:
        await give(uid, i["item"], i["qty"])
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.spirit_stones = 500
        await db.commit()
    res = await client.post("/math/craft", json={"recipe_id": recipe}, headers=h)
    assert res.status_code == 400 and res.json()["error"]["code"] == "need_note"
    for n in r["needs_notes"]:
        await give(uid, n)
    view = (await client.get("/math/craft", headers=h)).json()
    assert next(x for x in view["recipes"] if x["id"] == recipe)["can"]
    res = await client.post("/math/craft", json={"recipe_id": recipe}, headers=h)
    assert res.status_code == 200, res.text
    out = res.json()
    assert out["equipment"]["item_id"] == r["makes"] and out["equipment"]["rarity"] == r["rarity"]
    assert out["spirit_stones"] == 500 - r["fee"]
    async with dbm.SessionLocal() as db:
        rows = {x.item_id: x.quantity for x in (await db.execute(
            select(InventoryItem).where(InventoryItem.user_id == uid))).scalars().all()}
        for i in r["ingredients"]:                      # materials are spent
            assert rows.get(i["item"], 0) == 0, (i["item"], rows)
        for n in r["needs_notes"]:                      # the understanding is not
            assert rows.get(n, 0) == 1, (n, rows)
        eq = (await db.execute(select(EquipmentInstance).where(
            EquipmentInstance.user_id == uid))).scalars().all()
        assert [e.item_id for e in eq] == [r["makes"]]


async def test_crafting_refuses_without_the_materials(client, gw):
    h, uid, s = await fighter(client, gw, "toan_8", "Toán Tám")
    r = catalog.math_crafting()["recipes"]["but_tap_hop"]
    for n in r["needs_notes"]:
        await give(uid, n)
    res = await client.post("/math/craft", json={"recipe_id": "but_tap_hop"}, headers=h)
    assert res.status_code == 400 and res.json()["error"]["code"] == "need_material"


@pytest.mark.parametrize("recipe_id", sorted(catalog.math_crafting()["recipes"]))
def test_every_recipe_makes_a_real_piece_of_equipment(recipe_id):
    r = catalog.math_crafting()["recipes"][recipe_id]
    assert r["makes"] in catalog.equipment()["items"], r["makes"]
    assert r["rarity"] in catalog.equipment()["rarities"], r["rarity"]
    for n in r.get("needs_notes", []):
        info = catalog.stack_item(n)
        assert info is not None and info["kind"] == "note", n
    for i in r["ingredients"]:
        assert catalog.stack_item(i["item"]) is not None, i["item"]
        assert int(i["qty"]) > 0
