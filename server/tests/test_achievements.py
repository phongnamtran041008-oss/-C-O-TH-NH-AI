"""Thành Tựu (systems/achievements.py, data/achievements.json): the data, counting through the
real call sites (answers, kills, Phản Đòn, zones, abilities, linh căn, weapons, beasts), the
unlock message after the commit and never after a rollback, the toasts missed while offline,
claims gated by tu vi, danh hiệu worn through /books/wear, milestones, hidden entries and the
backfill of an old player."""
import json

import pytest
import pytest_asyncio
from sqlalchemy import select, update

from app import db as dbm
from app.models import Achievement, AchievementCounter, Character, CodexEntry, User
from app.realtime import abilities, combat
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import achievements as ach
from app.systems import beasts, catalog, items, weapons
from tests.econ_helpers import give, player, stones
from tests.test_combat import FakeMono, answer, at_monster, fighter, hit, last, run, settle
from tests.test_math_loop import play, start


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


async def counter(uid: int, key: str) -> int:
    async with dbm.SessionLocal() as db:
        row = await db.get(AchievementCounter, (uid, key))
        return int(row.value) if row else 0


async def tier(uid: int, aid: str) -> int:
    async with dbm.SessionLocal() as db:
        row = await db.get(Achievement, (uid, aid))
        return row.tier if row else 0


async def event(uid: int, name: str, n: int = 1, **ctx) -> list[dict]:
    async with dbm.SessionLocal() as db:
        out = await ach.on_event(db, uid, name, n, **ctx)
        await db.commit()
    return out


def unlocked(s, key: str) -> bool:
    return any(u["key"] == key for m in s.sent if m.get("t") == "achievement" for u in m["unlocks"])


def entry(view: dict, aid: str) -> dict:
    return next(e for c in view["categories"] for e in c["achievements"] if e["id"] == aid)


# ------------------------------------------------------------------ the data
def test_the_data_is_sound_and_rich():
    assert ach.validate() == []
    d = ach.data()
    assert len(d["achievements"]) >= 90
    cats = {c["id"] for c in d["categories"]}
    assert cats == {"tu_luyen", "ngo_dao", "chien_dau", "suu_tam", "kham_pha", "tai_phu", "bi_an"}
    assert all(any(a["category"] == c for a in d["achievements"]) for c in cats)
    assert sum(1 for a in d["achievements"] if a.get("hidden")) >= 8
    assert sum(1 for a in d["achievements"] if len(a["tiers"]) >= 3) >= 30, "most climb through tiers"
    assert len(ach.title_names()) >= 30


def test_validate_catches_broken_entries():
    d = json.loads(json.dumps(ach.data()))
    a = d["achievements"][0]
    a["tiers"][0]["reward"]["items"] = [{"item": "dai_thua_dan", "qty": 1}]       # far above luyen_khi:1
    d["achievements"][1]["icon"] = ["misc", "khong_co"]
    d["achievements"][2]["counter"] = "khong_co"
    d["achievements"][3]["tiers"].reverse()
    d["achievements"][4]["name_vi"] = d["achievements"][5]["name_vi"]
    d["achievements"][-1].pop("reveal_vi")
    errs = "\n".join(ach.validate(d))
    for needle in ("dai_thua_dan", "icon", "unknown counter", "strictly rising", "used twice", "reveal_vi"):
        assert needle in errs, needle


def test_every_event_has_a_call_site():
    assert set(ach.RAW) <= ach._emitted()


# ------------------------------------------------------------------ answers
async def test_right_answers_and_a_streak_unlock_with_one_message_after_the_commit(client, gw):
    h, uid, s = await fighter(client, gw, "tt_1", "Thành Tựu Một")
    run_id = await start(client, h)
    for _ in range(5):
        await play(client, h, run_id, True)
    assert await counter(uid, "answer_right") == 5 and await counter(uid, "answer_streak") == 5
    assert await counter(uid, "answer_right|context=math") == 5
    assert await tier(uid, "answer_streak") == 1
    assert unlocked(s, "answer_streak:1")
    msgs = [u["key"] for m in s.sent if m.get("t") == "achievement" for u in m["unlocks"]]
    assert msgs.count("answer_streak:1") == 1
    u = next(u for m in s.sent if m.get("t") == "achievement" for u in m["unlocks"] if u["id"] == "answer_streak")
    assert u["tier_name_vi"] == "Ngũ Liên" and u["icon"] and u["points"] > 0
    # the toast waits for the acknowledgement: /new still has it until /seen
    new = (await client.get("/achievements/new", headers=h)).json()["unlocks"]
    assert "answer_streak:1" in [x["key"] for x in new]
    r = await client.post("/achievements/seen", json={"keys": ["answer_streak:1"]}, headers=h)
    assert r.json()["marked"] == 1
    new = (await client.get("/achievements/new", headers=h)).json()["unlocks"]
    assert "answer_streak:1" not in [x["key"] for x in new]


async def test_a_wrong_answer_breaks_the_streak_and_a_comeback_is_a_hidden_one(client, gw):
    h, uid, s = await fighter(client, gw, "tt_2", "Thành Tựu Hai")
    run_id = await start(client, h)
    await play(client, h, run_id, True)
    await play(client, h, run_id, True)
    for _ in range(ach.COMEBACK_AFTER):
        await play(client, h, run_id, False)
    assert await counter(uid, ach.STREAK) == 0
    v = (await client.get("/achievements", headers=h)).json()
    hidden = entry(v, "secret_comeback")
    assert hidden["name_vi"] == "???" and not hidden["revealed"] and hidden["tiers"][0]["reward_vi"] == ["???"]
    await play(client, h, run_id, True)
    assert await counter(uid, "answer_streak") == 2, "the best run is kept"
    assert await tier(uid, "secret_comeback") == 1
    v = (await client.get("/achievements", headers=h)).json()
    shown = entry(v, "secret_comeback")
    assert shown["revealed"] and shown["name_vi"] == "Thất Bại Là Mẹ Thành Công" and shown["reveal_vi"]


async def test_a_rollback_drops_the_toast(client, gw):
    h, uid, s = await fighter(client, gw, "tt_3", "Thành Tựu Ba")
    async with dbm.SessionLocal() as db:
        out = await ach.on_event(db, uid, "linh_can", seen=5, rolls=5)
        assert [u["key"] for u in out] == ["lc_book:1", "lc_test:1"]
        await db.rollback()
    assert not unlocked(s, "lc_book:1") and await tier(uid, "lc_book") == 0
    await event(uid, "linh_can", seen=5, rolls=5)
    assert unlocked(s, "lc_book:1") and unlocked(s, "lc_test:1")


# ------------------------------------------------------------------ the world
async def test_a_kill_counts_by_rank_kind_and_without_a_scratch(client, gw, monkeypatch):
    monkeypatch.setattr(combat, "on_hit_rule", lambda ch: False)
    h, uid, s = await fighter(client, gw, "tt_4", "Thành Tựu Bốn")
    p, m = at_monster(gw, s)
    assert "zone" in ach.FIRED
    await hit(gw, p, m)
    await answer(client, h, s, True)
    p.stats["atk"] = 10000
    while m.alive:
        await hit(gw, p, m)
    await settle(gw)
    await ach.flush_all()
    assert await counter(uid, "kill") == 1 and await counter(uid, "kill_kinds") == 1
    assert await counter(uid, "kill_flawless") == 1
    assert await tier(uid, "kill") == 1 and await tier(uid, "kill_flawless") == 1
    assert await counter(uid, "zones") == 2      # Trúc Lâm Thôn, then the forest
    assert await counter(uid, "lands") >= 1


async def test_phan_don_and_the_combo_are_buffered_then_written(client, gw):
    from tests.test_combat_on_hit import SLIME_MA, VALLEY, provoke, stand_at, take_blow
    from tests.test_combat_on_hit import answer as hit_answer
    from tests.test_combat_on_hit import rest
    h, uid, s = await fighter(client, gw, "tt_5", "Thành Tựu Năm")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    for _ in range(3):
        await take_blow(gw, s, p, m)
        await hit_answer(client, h, s, True)
        rest(gw)
    assert ach._pending.get(uid), "nothing written in the fight itself"
    assert await counter(uid, "parry") == 0
    await ach.flush_all()
    assert await counter(uid, "parry") == 3 and await counter(uid, "parry_combo") == 3
    assert await tier(uid, "parry_combo") == 1
    assert unlocked(s, "parry_combo:1")


async def test_abilities_and_a_fall_are_counted(client, gw, monkeypatch):
    monkeypatch.setattr(combat, "on_hit_rule", lambda ch: False)
    h, uid, s = await fighter(client, gw, "tt_6", "Thành Tựu Sáu")
    p, m = at_monster(gw, s)
    monkeypatch.setattr(abilities, "is_open", lambda p, u: True)
    monkeypatch.setattr(abilities, "check_glide", lambda *a: None)
    assert abilities.place_formation(p, gw.mono()) is None
    assert abilities.apply_glide(p.channel, p, p.x + 20, p.y) is None
    abilities.apply_ride(p.channel, p, True)
    combat.die(p.channel, p, gw.mono())
    await settle(gw)
    await ach.flush_all()
    for key in ("formation", "glide", "ride", "death"):
        assert await counter(uid, key) == 1, key
    assert await tier(uid, "secret_death") == 1 and await tier(uid, "ride") == 1


# ------------------------------------------------------------------ collecting
async def test_weapons_beasts_and_linh_can(client, gw):
    h, uid, s = await fighter(client, gw, "tt_7", "Thành Tựu Bảy")
    wid = next(w for w in weapons.equipment_items() if w.startswith("kiem_"))
    async with dbm.SessionLocal() as db:
        await items.grant_equipment(db, uid, wid, "huyen", "test")       # thượng phẩm
        await db.commit()
    assert await counter(uid, "weapon_get") == 1 and await counter(uid, "weapon_get|type=kiem") == 1
    assert await counter(uid, "weapon_get|quality=thuong") == 1
    assert await tier(uid, "weapon_q_thuong") == 1 and await tier(uid, "weapon_t_kiem") == 1
    await give(uid, "phong_an_phu", 1)
    bid = next(iter(beasts._data()["all"]))
    async with dbm.SessionLocal() as db:
        await beasts.seal(db, await db.get(User, uid), bid)
        await db.commit()
    assert await tier(uid, "beast_tame") == 1 and await tier(uid, f"beast_{bid}") == 1
    r = await client.post("/linh-can/awaken", headers=h)
    assert r.status_code == 200
    assert await counter(uid, "lc_giai") >= 1 and await counter(uid, "lc_test") == 1
    assert await tier(uid, "lc_giai") >= 1


# ------------------------------------------------------------------ claims, titles, milestones
async def test_claim_pays_once_and_waits_for_tu_vi(client, gw):
    h, uid, s = await fighter(client, gw, "tt_8", "Thành Tựu Tám")
    await event(uid, "linh_can", seen=1, rolls=5)          # lc_test tier 1: Tẩy Linh Thảo, Luyện Khí 1
    v = (await client.get("/achievements", headers=h)).json()
    t1 = entry(v, "lc_test")["tiers"][0]
    assert t1["reached"] and not t1["claimable"] and t1["req_vi"]
    r = await client.post("/achievements/claim", json={"id": "lc_test", "tier": 1}, headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "locked"
    async with dbm.SessionLocal() as db:
        await db.execute(update(Character).where(Character.user_id == uid).values(realm="luyen_khi", realm_stage=1))
        await db.commit()
    before = await stones(uid)
    r = await client.post("/achievements/claim", json={"id": "lc_test", "tier": 1}, headers=h)
    assert r.status_code == 200, r.text
    assert await stones(uid) == before + 300
    assert any("Tẩy Linh Thảo" in x for x in r.json()["claimed"][0]["rewards_vi"])
    r = await client.post("/achievements/claim", json={"id": "lc_test", "tier": 1}, headers=h)
    assert r.status_code == 409
    r = await client.post("/achievements/claim", json={"id": "lc_test", "tier": 2}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_reached"
    assert await counter(uid, "stones_earned") == 0, "Thành Tựu's own rewards do not feed it"


async def test_a_title_is_given_on_unlock_and_worn_like_the_librarys(client, gw):
    h, uid, s = await fighter(client, gw, "tt_9", "Thành Tựu Chín")
    async with dbm.SessionLocal() as db:
        await db.execute(update(Character).where(Character.user_id == uid).values(realm="truc_co", realm_stage=1))
        await db.commit()
    await event(uid, "cult", realm="truc_co", stage=1)
    assert await tier(uid, "cult_truc_co") == 1 and await tier(uid, "cult_luyen_khi") == 3
    v = (await client.get("/achievements", headers=h)).json()
    assert {"title": "Trúc Cơ Tu Sĩ", "source": "thanh_tuu"} in v["titles"]
    r = await client.post("/books/wear", json={"title": "Trúc Cơ Tu Sĩ"}, headers=h)
    assert r.status_code == 200, r.text
    assert (await client.get("/me", headers=h)).json()["title"] == "Trúc Cơ Tu Sĩ"
    assert (await client.get("/achievements", headers=h)).json()["title"] == "Trúc Cơ Tu Sĩ"
    r = await client.post("/books/wear", json={"title": "Vô Thượng Chí Tôn"}, headers=h)
    assert r.status_code == 400, "a title not yet earned cannot be worn"


async def test_claim_all_and_the_milestones(client, gw):
    h, uid, s = await fighter(client, gw, "tt_10", "Đạo Hữu Mười")
    r = await client.post("/achievements/claim-all", headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "nothing"
    await event(uid, "quest", 50, kind="kill", target="ink_slime")
    v = (await client.get("/achievements", headers=h)).json()
    assert v["points"] >= 20 and entry(v, "kill")["tier"] == 2
    r = await client.post("/achievements/milestone", json={"points": 50}, headers=h)
    assert r.status_code == 400
    async with dbm.SessionLocal() as db:   # enough Đạo Tâm for the first milestone
        db.add(Achievement(user_id=uid, ach_id="cult_dai_thua", tier=1, claimed=0, seen=1))
        await db.commit()
    before = await stones(uid)
    r = await client.post("/achievements/claim-all", headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    got = {c["id"] for c in body["claimed"]}
    assert "kill" in got and "cult_dai_thua" not in got, "a reward above the player's tu vi waits"
    assert [m["points"] for m in body["milestones"]] == [50, 150]     # 160 Đạo Tâm from Đại Thừa
    assert {"title": "Đạo Tâm Sơ Thành", "source": "thanh_tuu"} in body["view"]["titles"]
    assert await stones(uid) > before
    r = await client.post("/achievements/milestone", json={"points": 50}, headers=h)
    assert r.status_code == 409
    assert body["view"]["milestones"][0]["claimed"]


# ------------------------------------------------------------------ old players
async def test_backfill_unlocks_quietly_what_an_old_player_already_did(client, gw):
    h, uid, s = await fighter(client, gw, "tt_11", "Đạo Hữu Mười Một")
    async with dbm.SessionLocal() as db:
        await db.execute(update(Character).where(Character.user_id == uid).values(realm="luyen_khi", realm_stage=5))
        db.add(CodexEntry(user_id=uid, codex="monster", entry_id="ink_slime", discovered_at=dbm_now(),
                          progress={"kills": 40}))
        db.add(CodexEntry(user_id=uid, codex="monster", entry_id="nghien_ma", discovered_at=dbm_now(),
                          progress={"kills": 12}))
        await db.commit()
    new = (await client.get("/achievements/new", headers=h)).json()["unlocks"]
    assert new == [], "a backfill makes no toasts"
    assert await counter(uid, "kill") == 52 and await counter(uid, "kill|rank=boss") == 12
    assert await counter(uid, "kill_kinds") == 2
    assert await tier(uid, "kill") == 2 and await tier(uid, "kill_boss") == 2
    assert await tier(uid, "cult_luyen_khi") == 2
    v = (await client.get("/achievements", headers=h)).json()
    assert entry(v, "kill")["claimable"]
    async with dbm.SessionLocal() as db:
        assert (await db.get(User, uid)).flags.get("ach_backfill") == ach.BACKFILL_VERSION


async def test_the_view_masks_hidden_ones_and_counts_everything(client, gw):
    h, uid, s = await fighter(client, gw, "tt_12", "Đạo Hữu Mười Hai")
    v = (await client.get("/achievements", headers=h)).json()
    assert v["total"] == len(ach.entries()) and v["points_name_vi"] == "Đạo Tâm"
    assert len(v["categories"]) == 7 and v["next_milestone"]["points"] == 50
    for c in v["categories"]:
        for e in c["achievements"]:
            if e["hidden"] and not e["revealed"]:
                assert e["name_vi"] == "???" and e["progress_vi"] == "???"
    e = entry(v, "cult_truc_co")
    assert e["tiers"][0]["at_vi"] == "Trúc Cơ sơ kỳ" or e["tiers"][0]["at_vi"].startswith("Trúc Cơ")


def dbm_now():
    from app import clock
    return clock.now()
