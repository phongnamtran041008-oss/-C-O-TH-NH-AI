"""Linh căn (systems/linh_can.py, data/linh_can.json): the data, the caps and the odds, the free
first test, tẩy linh pills with pity and the keep-or-take choice, brewing the pills, and every
effect type as a real effect where the server applies it.

The world tests run on the fake clock of test_combat; the quiz service and the database are
real. The effect tests give the player a test root carrying exactly the effect under test
(`with_root`), so they do not depend on which roots the data holds today.
"""
import copy
import random
import types

import pytest
import pytest_asyncio
from sqlalchemy import update

from app import db as dbm
from app.learning import math_path, quiz
from app.models import Character, LinhCan, User
from app.realtime import abilities, combat
from app.realtime import beasts as wild
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import catalog, cultivation, linh_can, loot, math_skills
from tests.econ_helpers import give, player, qty
from tests.test_alchemy import perfect_timings
from tests.test_combat import FakeMono, fighter, last, run, settle
from tests.test_combat_on_hit import SLIME_MA, VALLEY, answer, plan, provoke, rest, stand_at, take_blow

TEST_ROOT = "thu_nghiem_linh_can"


def covers(*types_: str) -> None:
    """Marks the effect types a test exercises (test_every_effect_type_is_exercised_here reads
    these calls from the source, so the check holds however the tests are selected)."""
    assert set(types_) <= set(linh_can.SITES), types_


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def with_root(monkeypatch, **effects) -> str:
    """A test root of Huyền giai carrying exactly these effects."""
    d = copy.deepcopy(linh_can.data())
    d["roots"][TEST_ROOT] = {"name_vi": "Linh Căn Thử", "giai": "huyen", "he": ["kim"], "loai": "don",
                             "effects": [{"type": t, "value": v} for t, v in effects.items()],
                             "desc_vi": "thử", "lore_vi": "thử"}
    monkeypatch.setattr(linh_can, "data", lambda: d)
    return TEST_ROOT


async def set_root(uid: int, rid: str | None, push: bool = True) -> None:
    async with dbm.SessionLocal() as db:
        row = await db.get(LinhCan, uid)
        if row is None:
            row = LinhCan(user_id=uid, pity={}, rolls=0, discovered=[])
            db.add(row)
        row.root_id = rid
        await db.flush()
        if push:
            ch = await db.get(Character, uid)
            await cultivation.push_to_world(db, ch)
        await db.commit()


async def set_realm(uid: int, realm: str, stage: int) -> None:
    async with dbm.SessionLocal() as db:
        await db.execute(update(Character).where(Character.user_id == uid).values(realm=realm, realm_stage=stage))
        await db.commit()


# ------------------------------------------------------------------ the data
def test_the_data_is_sound_and_rich():
    assert linh_can.validate() == []
    d = linh_can.data()
    assert [g["id"] for g in d["giai"]] == ["pham", "hoang", "huyen", "dia", "thien", "thanh", "tien", "than",
                                            "hon_don"]
    assert len(d["roots"]) >= 48
    per = [sum(1 for r in d["roots"].values() if r["giai"] == g) for g in linh_can.giai_ids()]
    assert all(per) and per[0] > per[-1], per
    assert len(d["effect_types"]) >= 18 and set(d["effect_types"]) == set(linh_can.SITES)
    assert len(d["pills"]) >= 4
    hd = d["roots"]["hon_don_linh_can"]
    assert len(hd["effects"]) >= 6, "a Hỗn Độn root touches many systems at once"
    for pid in d["pills"]:
        assert catalog.pills()[pid]["effect"] == "linh_can"
        assert pid in catalog.recipes() and pid in loot.data()["items"]
        for ing in catalog.recipes()[pid]["ingredients"]:
            assert ing["item"] in loot.data()["items"], ing


def test_validate_catches_broken_data():
    d = copy.deepcopy(linh_can.data())
    d["pills"]["tay_linh_dan"]["odds"]["pham"] += 0.1
    d["roots"]["phe_linh_can"]["effects"] = [{"type": "bay_len_troi", "value": 0.1}]
    d["roots"]["tu_linh_can"]["effects"][0]["type"] = "hp_pct"          # a second Phàm root with primary hp_pct
    d["roots"] = {k: v for k, v in d["roots"].items() if v["giai"] not in ("tien", "than")}
    d["effect_types"]["bay_cao"] = {"unit": "pct", "cap": 0.1, "text_vi": "{v}"}
    probs = "\n".join(linh_can.validate(d))
    for want in ("sum to", "bay_len_troi", "primary effect hp_pct", "giai tien: no root",
                 "bay_cao: the server does not apply it", "at least 48"):
        assert want in probs, want


def test_caps_follow_the_cultivation_realm():
    cap = linh_can.cap_index
    assert cap("pham_nhan", 0) == cap("luyen_khi", 3) == 3          # Huyền
    assert cap("luyen_khi", 4) == cap("luyen_khi", 6) == 4          # Địa
    assert cap("luyen_khi", 7) == cap("luyen_khi", 9) == 5          # Thiên
    assert cap("truc_co", 1) == 6 and cap("kim_dan", 2) == 7 and cap("nguyen_anh", 3) == 8
    assert cap("hoa_than", 1) == cap("dai_thua", 3) == 9
    assert linh_can.opens_at("dia") == loot.label(loot.parse("luyen_khi:4"))
    assert linh_can.opens_at("pham") is None


def test_capped_odds_redraw_inside_the_cap_and_better_pills_aim_higher():
    p = linh_can.pills()
    w = linh_can.capped(p["tay_linh_dan"]["odds"], 3)
    assert sum(w) == pytest.approx(1) and all(x == 0 for x in w[3:])
    assert w[0] / w[1] == pytest.approx(p["tay_linh_dan"]["odds"]["pham"] / p["tay_linh_dan"]["odds"]["hoang"])
    # a pill that never rolls that low: everything on the cap
    assert linh_can.capped(p["khai_thien_dan"]["odds"], 3) == [0, 0, 1, 0, 0, 0, 0, 0, 0]
    rng = random.Random(7)
    for _ in range(300):
        assert linh_can.draw_giai(rng, p["tao_hoa_dan"]["odds"], 5) <= 5
    means = [sum((i + 1) * x for i, x in enumerate(linh_can.odds_list(v["odds"]))) for v in p.values()]
    assert means == sorted(means)


# ------------------------------------------------------------------ the routes
async def test_first_test_is_free_and_only_once(client, app):
    h, uid = await player(client, "lc_mot")
    v = (await client.get("/linh-can", headers=h)).json()
    assert not v["awakened"] and v["root"] is None and v["cap"]["giai"] == "huyen"
    assert [g["open"] for g in v["giai"]] == [True] * 3 + [False] * 6
    assert v["giai"][3]["need_vi"] == loot.label(loot.parse("luyen_khi:4"))
    assert all(not b["discovered"] and "name_vi" not in b for b in v["book"]), "the đồ giám hides what was not seen"
    assert sum(o["p"] for o in v["awaken_odds"]) == pytest.approx(1)
    guide0 = (await client.get("/guide", headers=h)).json()
    r = await client.post("/linh-can/awaken", headers=h)
    assert r.status_code == 200, r.text
    root = r.json()["root"]
    assert root["giai_index"] <= 3 and root["effects_vi"] and root["color"].startswith("#")
    v = r.json()["view"]
    assert v["awakened"] and v["discovered"] == 1
    assert next(b for b in v["book"] if b["id"] == root["id"])["name_vi"] == root["name_vi"]
    r = await client.post("/linh-can/awaken", headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "already_awakened"
    c = (await client.get("/cultivation", headers=h)).json()
    assert c["linh_can"]["id"] == root["id"] and c["linh_can"]["giai_vi"] and c["linh_can"]["effects_vi"]
    assert c["stats"]["lc"] == root["giai_index"]
    # Lộ Trình: the step of the first test is done
    def step(g):
        return next(s for ch in g["chapters"] for s in ch["steps"] if s["id"] == "g_linh_can")
    assert step(guide0)["state"] == "active"
    assert step((await client.get("/guide", headers=h)).json())["state"] == "done"


async def test_a_pill_roll_waits_for_the_choice(client, app, monkeypatch):
    h, uid = await player(client, "lc_hai")
    await set_root(uid, "phe_linh_can", push=False)
    r = await client.post("/linh-can/roll", json={"pill": "tay_linh_dan"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_pill"
    await give(uid, "tay_linh_dan", 3)
    seq = iter(["vi_hoa_linh_can", "tu_linh_can", "phe_linh_can"])
    monkeypatch.setattr(linh_can, "draw_root", lambda rng, g: next(seq))
    r = await client.post("/linh-can/roll", json={"pill": "tay_linh_dan"}, headers=h)
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["rolled"]["id"] == "vi_hoa_linh_can" and not out["same"] and out["old"]["id"] == "phe_linh_can"
    assert out["view"]["pending"]["id"] == "vi_hoa_linh_can" and out["view"]["root"]["id"] == "phe_linh_can"
    assert await qty(uid, "tay_linh_dan") == 2
    r = await client.post("/linh-can/roll", json={"pill": "tay_linh_dan"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "pending_choice"
    assert await qty(uid, "tay_linh_dan") == 2, "a refused roll eats nothing"
    r = await client.post("/linh-can/choose", json={"keep": True}, headers=h)
    assert r.json()["root"]["id"] == "phe_linh_can" and r.json()["view"]["pending"] is None
    assert (await client.post("/linh-can/choose", json={"keep": True}, headers=h)).json()["error"]["code"] == \
        "no_pending"
    await client.post("/linh-can/roll", json={"pill": "tay_linh_dan"}, headers=h)
    r = await client.post("/linh-can/choose", json={"keep": False}, headers=h)
    assert r.json()["root"]["id"] == "tu_linh_can" and r.json()["took"]
    # the same root as the one carried is simply kept
    await set_root(uid, "phe_linh_can", push=False)
    out = (await client.post("/linh-can/roll", json={"pill": "tay_linh_dan"}, headers=h)).json()
    assert out["same"] and out["view"]["pending"] is None
    v = out["view"]
    assert v["rolls"] == 3 and {"vi_hoa_linh_can", "tu_linh_can", "phe_linh_can"} <= \
        {b["id"] for b in v["book"] if b["discovered"]}
    # pills are spent at the Trắc Linh Đài, never from the bag
    await give(uid, "tay_linh_dan", 1)
    inv = (await client.get("/inventory", headers=h)).json()
    assert not next(i for i in inv["items"] if i["item_id"] == "tay_linh_dan")["usable"]
    r = await client.post("/inventory/use", json={"item_id": "tay_linh_dan"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "linh_can_pill"


async def test_rolls_never_pass_the_realm_cap_and_pity_lifts_the_floor(client, app, monkeypatch):
    h, uid = await player(client, "lc_ba")
    await set_root(uid, "phe_linh_can", push=False)
    await give(uid, "khai_thien_dan", 2)
    out = (await client.post("/linh-can/roll", json={"pill": "khai_thien_dan"}, headers=h)).json()
    assert out["rolled"]["giai"] == "huyen", "a Phàm Nhân gets the cap, not the pill's Địa giai"
    await client.post("/linh-can/choose", json={"keep": True}, headers=h)
    # pity: a hand that always draws the lowest giai still reaches the floor on the every-th roll
    every = linh_can.pills()["tay_tuy_dan"]["pity"]["every"]
    await set_realm(uid, "luyen_khi", 5)           # cap Địa = the floor of Tẩy Tủy Đan
    await give(uid, "tay_tuy_dan", every)
    low = types.SimpleNamespace(random=lambda: 0.0)          # always the lowest giai the window allows
    draw = linh_can.draw_giai
    monkeypatch.setattr(linh_can, "draw_giai", lambda rng, odds, cap, floor=1: draw(low, odds, cap, floor))
    got = []
    for i in range(every):
        out = (await client.post("/linh-can/roll", json={"pill": "tay_tuy_dan"}, headers=h)).json()
        got.append(out["rolled"]["giai"])
        pity = next(p for p in out["view"]["pills"] if p["id"] == "tay_tuy_dan")["pity"]
        if not out["same"]:
            await client.post("/linh-can/choose", json={"keep": True}, headers=h)
        if i < every - 1:
            assert pity["count"] == i + 1 and pity["left"] == every - i - 1
    assert got[:-1] == ["pham"] * (every - 1) and got[-1] == "dia" and out["pity_hit"]
    assert pity["count"] == 0
    v = (await client.get("/linh-can", headers=h)).json()
    tt = next(p for p in v["pills"] if p["id"] == "tay_tuy_dan")
    assert v["cap"]["giai"] == "dia" and all(linh_can.giai_index(o["giai"]) <= 4 for o in tt["odds"])
    assert sum(o["p"] for o in tt["odds"]) == pytest.approx(1)


async def test_the_pill_is_brewed_at_the_furnace_from_its_materials(client, app, frozen):
    h, uid = await player(client, "lc_bon", stones=500)
    await set_realm(uid, "luyen_khi", 1)
    r = catalog.recipes()["tay_linh_dan"]
    await give(uid, r["item"], 1)
    for ing in r["ingredients"]:
        await give(uid, ing["item"], ing["qty"])
    ov = (await client.get("/alchemy", headers=h)).json()
    e = next(x for x in ov["recipes"] if x["id"] == "tay_linh_dan")
    assert e["known"] and e["ready"]
    fire = (await client.post("/alchemy/start", json={"recipe_id": "tay_linh_dan"}, headers=h)).json()["fire"]
    frozen.advance(milliseconds=sum(perfect_timings(fire)) + 50)
    res = (await client.post("/alchemy/finish", json={"session_id": fire["session_id"],
                                                      "timings": perfect_timings(fire)}, headers=h)).json()
    assert res["made"] >= r["yield"]["thuong"] and await qty(uid, "tay_linh_dan") == res["made"]
    for ing in r["ingredients"]:
        assert await qty(uid, ing["item"]) == 0
    # every material really drops from a land monster, and only once the tu vi allows it
    drops = {d["item"] for m in catalog.monsters().values() for d in m.get("drops", []) if "item" in d}
    for pid in linh_can.pills():
        for ing in catalog.recipes()[pid]["ingredients"]:
            assert ing["item"] in drops, ing


# ------------------------------------------------------------------ effects: the stats
async def test_stat_effects_raise_the_stats(client, app, monkeypatch):
    covers("atk_pct", "def_pct", "hp_pct", "qi_pct", "crit")
    h, uid = await player(client, "lc_nam")
    base = (await client.get("/cultivation", headers=h)).json()["stats"]
    assert base["lc"] == 0 and base["lc_fx"] == {}
    rid = with_root(monkeypatch, atk_pct=0.5, def_pct=0.4, hp_pct=0.3, qi_pct=0.2, crit=3.0, xp_pct=0.1)
    await set_root(uid, rid, push=False)
    st = (await client.get("/cultivation", headers=h)).json()["stats"]
    assert st["atk"] == round(base["atk"] * 1.5) and st["def"] == round(base["def"] * 1.4)
    assert st["max_hp"] == round(base["max_hp"] * 1.3) and st["max_qi"] == round(base["max_qi"] * 1.2)
    assert st["crit"] == base["crit"] + 3.0
    assert st["lc"] == 3 and st["lc_fx"] == {"xp_pct": 0.1}


async def test_a_new_root_reaches_the_live_world_and_the_marks_of_others(client, gw, monkeypatch):
    h, uid, s = await fighter(client, gw, "lc_sau", "Linh Sáu")
    h2, uid2, s2 = await fighter(client, gw, "lc_bay", "Linh Bảy")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    assert gw.join(s2, "truc_lam_thon", "abode")
    gw._place(s2, VALLEY, p.x + 10, p.y, "down")
    assert p.full()["lc"] == 0
    hp0 = p.max_hp
    rid = with_root(monkeypatch, hp_pct=0.5)
    s2.player.known[p.eid] = p.full()
    async with dbm.SessionLocal() as db:
        row = LinhCan(user_id=uid, root_id=None, pity={}, rolls=0, discovered=[])
        db.add(row)
        await db.flush()
        row.root_id = rid
        await linh_can._after_change(db, await db.get(Character, uid))
        await db.commit()
    assert p.max_hp == round(hp0 * 1.5) and p.full()["lc"] == 3
    assert p.eid not in s2.player.known, "whoever sees the player gets them again, mark and all"
    assert last(s, "stats")["stats"]["lc"] == 3


# ------------------------------------------------------------------ effects: the fight
async def test_basic_damage(client, gw, monkeypatch):
    covers("basic_dmg")
    h, uid, s = await fighter(client, gw, "lc_tam", "Linh Tám")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.stats["crit"] = -1000
    gw.mono.t += 5
    hp = m.hp
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) is None
    plain = hp - m.hp
    await set_root(uid, with_root(monkeypatch, basic_dmg=0.5))
    p.stats["crit"] = -1000
    gw.mono.t += 5
    hp = m.hp
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) is None
    assert hp - m.hp == pytest.approx(plain * 1.5)


async def test_a_parry_with_the_root(client, gw, monkeypatch):
    covers("parry_dmg", "stun_pct", "qi_gain", "heal_right", "xp_pct")
    h, uid, s = await fighter(client, gw, "lc_chin", "Linh Chín")
    await set_root(uid, with_root(monkeypatch, parry_dmg=0.5, stun_pct=0.4, qi_gain=1.0, heal_right=0.1,
                                  xp_pct=0.5))
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    p.qi = 0.0
    q = await take_blow(gw, s, p, m)
    p.hp = p.max_hp / 2
    hp, mhp = p.hp, m.hp
    right = plan()["right_answer"]
    expected = combat.base_damage(p, m) * right["counter_multiplier"] * 1.5
    res = await answer(client, h, s, True)
    c = res["combat"]
    assert c["parry"] and c["damage"] == int(round(expected)) and m.hp == pytest.approx(mhp - expected)
    assert m.stun_until == pytest.approx(gw.mono() + right["stun_seconds"] * 1.4)
    assert p.qi == pytest.approx(right["linh_luc_gain"] * 2)
    assert p.hp == pytest.approx(hp + p.max_hp * 0.1)
    assert res["xp"]["gained"] == round(math_path.xp_for_tier(q["q"]["math"]["tier"]) * 1.5)


async def test_a_wrong_answer_with_the_root(client, gw, monkeypatch):
    covers("wrong_guard")
    h, uid, s = await fighter(client, gw, "lc_muoi", "Linh Mười")
    await set_root(uid, with_root(monkeypatch, wrong_guard=0.5))
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    hp = p.hp
    res = await answer(client, h, s, False)
    blow = q["hit"]["dmg"] * plan()["wrong_answer"]["damage_taken"] * 0.5
    assert hp - p.hp == pytest.approx(blow, abs=0.6) and res["combat"]["damage_taken"] == round(blow)


async def test_dodge_glide_and_formation(client, gw, monkeypatch):
    covers("dodge_cd", "glide_cd", "tran_time")
    h, uid, s = await fighter(client, gw, "lc_mmot", "Linh Mười Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    dodge0, glide0 = combat.dodge_cooldown(p), abilities.glide_cooldown(p)
    await set_root(uid, with_root(monkeypatch, dodge_cd=0.25, glide_cd=0.5, tran_time=0.5))
    assert combat.dodge_cooldown(p) == pytest.approx(dodge0 * 0.75)
    assert abilities.glide_cooldown(p) == pytest.approx(glide0 * 0.5)
    v = abilities.view(p, gw.mono())
    if v is not None:
        assert v[abilities.GLIDE]["cooldown"] == pytest.approx(glide0 * 0.5)
    monkeypatch.setattr(abilities, "is_open", lambda p_, uid_: True)
    now = gw.mono()
    assert abilities.place_formation(p, now) is None
    f = p.channel.formations[-1]
    assert f["until"] == pytest.approx(now + float(abilities.formation_cfg().get("seconds", 20)) * 1.5)


async def test_linh_luc_comes_back_faster(client, gw, monkeypatch):
    covers("qi_regen")
    h, uid, s = await fighter(client, gw, "lc_mhai", "Linh Mười Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.qi, p.last_combat = 0.0, -1e9
    run(gw, 1.0)
    plain = p.qi
    await set_root(uid, with_root(monkeypatch, qi_regen=0.5))
    p.qi, p.last_combat = 0.0, -1e9
    run(gw, 1.0)
    assert plain > 0 and p.qi == pytest.approx(plain * 1.5)


async def test_death_costs_less_tu_vi(client, gw, monkeypatch):
    covers("death_guard")
    h, uid, s = await fighter(client, gw, "lc_mba", "Linh Mười Ba")
    await set_realm(uid, "luyen_khi", 2)
    async def xp_now(v):
        async with dbm.SessionLocal() as db:
            await db.execute(update(Character).where(Character.user_id == uid).values(cultivation_xp=v))
            await db.commit()
    need = cultivation.xp_needed("luyen_khi", 2)
    await xp_now(need - 1)
    await combat._death_penalty(uid)
    async with dbm.SessionLocal() as db:
        plain = need - 1 - (await db.get(Character, uid)).cultivation_xp
    await set_root(uid, with_root(monkeypatch, death_guard=0.5), push=False)
    await xp_now(need - 1)
    await combat._death_penalty(uid)
    async with dbm.SessionLocal() as db:
        guarded = need - 1 - (await db.get(Character, uid)).cultivation_xp
    assert plain > 0 and guarded == pytest.approx(plain * 0.5, abs=1)


async def test_drops_and_stones_from_kills(client, gw, monkeypatch):
    covers("drop_luck", "stones_pct")
    h, uid, s = await fighter(client, gw, "lc_mbon", "Linh Mười Bốn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    plain = combat._loot_bonus(p, m)
    await set_root(uid, with_root(monkeypatch, drop_luck=0.3, stones_pct=0.2))
    got = combat._loot_bonus(p, m)
    assert got["drop_mult"] == pytest.approx(plain["drop_mult"] * 1.3)
    assert got["stones_pct"] == pytest.approx(plain["stones_pct"] + 20)


async def test_taming_needs_one_parry_less(client, gw, monkeypatch):
    covers("tame")
    from tests.test_beasts import at_beast, pos
    h, uid, s = await fighter(client, gw, "lc_mnam", "Linh Mười Lăm")
    s.tree = pos(3)
    await set_root(uid, with_root(monkeypatch, tame=1))
    p, m = at_beast(gw, s, "linh_ho", near=6)
    need = m.need
    out = wild.on_parry(p.channel, m, p, gw.mono())
    assert out["need"] == need - 1 and out["n"] == 1


# ------------------------------------------------------------------ effects: chiêu
@pytest.mark.parametrize("elem", linh_can.CHIEU)
def test_chieu_damage_by_element(elem):
    covers(f"chieu_{elem}")
    sk = {"power": 2.0, "element": elem}
    p = types.SimpleNamespace(stats={"lc_fx": {f"chieu_{elem}": 0.25}})
    assert math_skills.damage(10, sk, 0, False, p) == pytest.approx(math_skills.damage(10, sk, 0, False) * 1.25)
    other = next(e for e in linh_can.CHIEU if e != elem)
    assert math_skills.damage(10, {"power": 2.0, "element": other}, 0, False, p) == pytest.approx(20)


async def test_a_cast_costs_less_qi_and_comes_back_sooner(client, gw, monkeypatch):
    covers("chieu_cd", "qi_cost")
    h, uid, s = await fighter(client, gw, "lc_msau", "Linh Mười Sáu")
    sk = math_skills.skills()["kiem_quyet"]
    elem = f"chieu_{sk['element']}"
    await set_root(uid, with_root(monkeypatch, chieu_cd=0.2, qi_cost=0.5, **{elem: 0.3}))
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.qi = 200.0
    hp0 = m.hp
    now = gw.mono()
    assert math_skills.request(p, "kiem_quyet", m.eid, now) is None
    await settle(gw)
    msg = last(s, "mcast")
    assert msg["ok"] and p.qi == pytest.approx(200.0 - sk["qi"] * 0.5)
    assert p.mskill_ready["kiem_quyet"] == pytest.approx(gw.mono() + sk["cooldown"] * 0.8)
    assert msg["ready_in"] == pytest.approx(sk["cooldown"] * 0.8)
    assert hp0 - m.hp == pytest.approx(math_skills.damage(combat.base_damage(p, m), sk, 0, False) * 1.3)


# ------------------------------------------------------------------ effects: the database side
async def test_more_time_for_each_question(client, app, monkeypatch):
    covers("q_time")
    h, uid = await player(client, "lc_q")
    rid = with_root(monkeypatch, q_time=3.0)
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        qtype = next(iter(quiz._graders))

        def question():
            q = types.SimpleNamespace(qtype=qtype, time_limit=10.0, item_id="x", answer_key={})
            q.public = lambda: {"time_limit": q.time_limit}
            return q
        plain = await quiz.create_session(db, u, "math_meditate", question())
        db.add(LinhCan(user_id=uid, root_id=rid, pity={}, rolls=0, discovered=[]))
        await db.flush()
        more = await quiz.create_session(db, u, "math_meditate", question())
        assert plain["time_limit"] == 10.0 and more["time_limit"] == 13.0
        await db.rollback()


async def test_alchemy_zone_and_extra_pill(client, app, frozen, monkeypatch):
    covers("alchemy_zone", "alchemy_extra")
    h, uid = await player(client, "lc_dan", stones=500)
    r = catalog.recipes()["hoi_huyet_dan"]
    await give(uid, r["item"], 1)
    for ing in r["ingredients"]:
        await give(uid, ing["item"], ing["qty"] * 2)
    fire0 = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    frozen.advance(milliseconds=sum(perfect_timings(fire0)) + 50)
    plain = (await client.post("/alchemy/finish", json={"session_id": fire0["session_id"],
                                                        "timings": perfect_timings(fire0)}, headers=h)).json()
    await set_root(uid, with_root(monkeypatch, alchemy_zone=4, alchemy_extra=1.0), push=False)
    fire = (await client.post("/alchemy/start", json={"recipe_id": "hoi_huyet_dan"}, headers=h)).json()["fire"]
    assert all(z["width"] == z0["width"] + 4 for z, z0 in zip(fire["zones"], fire0["zones"]))
    frozen.advance(milliseconds=sum(perfect_timings(fire)) + 50)
    res = (await client.post("/alchemy/finish", json={"session_id": fire["session_id"],
                                                      "timings": perfect_timings(fire)}, headers=h)).json()
    assert res["extra"] and res["made"] == plain["made"] + (0 if plain["extra"] else 1)


def test_every_effect_type_is_exercised_here():
    """Every effect type of the data has a test in this file that applies it for real."""
    import re
    from pathlib import Path
    src = Path(__file__).read_text("utf-8")
    seen = {t for call in re.findall(r"covers\(([^)]*)\)", src) for t in re.findall(r'"([a-z_]+)"', call)}
    if 'covers(f"chieu_{elem}")' in src:
        seen |= {f"chieu_{e}" for e in linh_can.CHIEU}
    assert set(linh_can.effect_types()) <= seen, sorted(set(linh_can.effect_types()) - seen)
