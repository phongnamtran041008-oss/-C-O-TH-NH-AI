"""The bestiary (2026-11-20): thirteen new creatures of the Luyện Khí lands (data/math/monsters.json,
spawned by the land maps) and six new linh thú with six new gifts (world_plan.json `beasts`).

The six beasts shipped with `status` "cho_hinh" (waiting for their art, like a weapon type): such a
beast is validated as data, absent from the live game, and its gift reads 0 (the `waiting` fixture
plays that). Their art arrived on 2026-11-20 and they are "co": the `live` fixture is now a no-op
kept for the tests that were written against the flip.
"""
import copy
import json
import math
import shutil
import sys
from pathlib import Path

import pytest
from app import db as dbm
from app.learning import math_tree
from app.models import Character, Pet
from app.realtime import abilities, combat, lands
from app.realtime.world import World
from app.systems import beasts, catalog, cultivation, loot, pets
from tests.test_beasts import (BESTIARY, at_beast, bplan, gw, pos, tame)  # noqa: F401 - gw is a fixture
from tests.test_combat import FakeMono, fighter, run, settle
from tests.test_combat_on_hit import SLIME_MA, VALLEY, answer, events, provoke, stand_at, take_blow

ROOT = Path(__file__).resolve().parents[2]
NEW = {   # creature -> (land, rank, hovers)
    "thiet_giap_thu": ("kiem_trung_son", "normal", False), "vong_hon_kiem_si": ("kiem_trung_son", "elite", False),
    "van_diep": ("luu_van_coc", "normal", True), "loi_ung": ("luu_van_coc", "elite", True),
    "u_minh_dang": ("van_tuong_trach", "normal", True), "huyet_ngac": ("van_tuong_trach", "elite", False),
    "hoa_yeu": ("me_do_lam", "normal", False), "bach_vien": ("me_do_lam", "elite", False),
    "co_quan_thu": ("thien_cong_phuong", "normal", False), "lo_linh": ("thien_cong_phuong", "elite", False),
    "thao_nhan": ("linh_xa_nguyen", "normal", False), "xich_diem_ma": ("linh_xa_nguyen", "elite", False),
    "loi_linh": ("loi_kiep_dai", "normal", True),
}
GIFTS = {"ngoc_tho": "heal_on_right", "tam_bao_thu": "stone_bonus", "kim_thiem": "drop_luck",
         "bach_ho_con": "atk_bonus", "cuu_vi_ho": "xp_bonus", "kim_si_dieu": "glide_range"}


def flipped_plan() -> dict:
    plan = copy.deepcopy(math_tree.world_plan())
    for b in plan["beasts"]:
        if b["id"] in BESTIARY:
            b["status"] = "co"
    return plan


def waiting_plan() -> dict:
    plan = copy.deepcopy(math_tree.world_plan())
    for b in plan["beasts"]:
        if b["id"] in BESTIARY:
            b["status"] = "cho_hinh"
    return plan


@pytest.fixture
def waiting(monkeypatch):
    """The six beasts back to 'cho_hinh': how a new beast waits for its art."""
    real = beasts._data()
    every = copy.deepcopy(real["all"])
    for bid in BESTIARY:
        every[bid]["status"] = "cho_hinh"
    patched = {**real, "all": every, "built": {k: b for k, b in every.items() if b.get("status") == "co"}}
    monkeypatch.setattr(beasts, "_data", lambda: patched)
    beasts.land_nodes.cache_clear()
    beasts.fight_info.cache_clear()
    yield patched
    beasts.land_nodes.cache_clear()
    beasts.fight_info.cache_clear()


@pytest.fixture
def live(monkeypatch):
    """The six beasts flipped to 'co'."""
    real = beasts._data()
    every = copy.deepcopy(real["all"])
    for bid in BESTIARY:
        every[bid]["status"] = "co"
    patched = {**real, "all": every, "built": {k: b for k, b in every.items() if b.get("status") == "co"}}
    monkeypatch.setattr(beasts, "_data", lambda: patched)
    beasts.land_nodes.cache_clear()
    beasts.fight_info.cache_clear()
    yield patched
    beasts.land_nodes.cache_clear()
    beasts.fight_info.cache_clear()


# ------------------------------------------------------------------ the creatures
def test_the_thirteen_creatures_live_in_their_lands():
    mons = catalog.monsters()
    plan_lands = {l["id"]: l for l in math_tree.world_plan()["lands"]}
    for kind, (land, rank, _) in NEW.items():
        m = mons[kind]
        assert m["land"] == land and m["rank"] == rank and m["name_vi"] and m["taunt_vi"] and m["weakness_vi"], kind
        assert kind in plan_lands[land]["monsters"], kind
        assert m["name_vi"] in plan_lands[land]["desc_vi"] or land == "loi_kiep_dai", kind
        w = World(mono=FakeMono())
        ch = w._channels(lands.zone_of(land))[0]
        assert any(x.kind == kind for x in ch.monsters), kind
    assert math_tree.validate_all() == [] and loot.validate() == []


def test_each_creature_teaches_something_of_its_own():
    """No new creature merely repeats another creature's nodes, and each one asks at least one node
    no creature of its land and rank asked before."""
    mons = catalog.monsters()
    for kind, (land, _, _) in NEW.items():
        others = [k for k, m in mons.items() if m.get("land") == land and k != kind]
        assert all(set(mons[kind]["nodes"]) != set(mons[o]["nodes"]) for o in others), kind
        assert set(mons[kind]["nodes"]) - {n for o in others if mons[o]["rank"] == mons[kind]["rank"]
                                           for n in mons[o]["nodes"]}, f"{kind} adds nothing to its rank"


def test_the_lands_feel_more_alive_not_swamped():
    from app.realtime import dia_do
    budget = dia_do.distribution()["max_monsters_per_land"]
    for land in {v[0] for v in NEW.values()}:
        zmap = World(mono=FakeMono())._channels(lands.zone_of(land))[0].map
        added = sum(int(a.props["count"]) for a in zmap.monster_areas if a.props["monster"] in NEW)
        total = sum(int(a.props["count"]) for a in zmap.monster_areas)
        if zmap.khu:      # a giant land of Đại Địa Đồ: its own distribution rules (tools/check_maps.py)
            assert added >= 2 and total <= budget, land
            continue
        assert 2 <= added <= 5, land
        assert total <= 45, land


def test_the_client_map_copies_match():
    for land in {v[0] for v in NEW.values()}:
        name = lands.land(land)["map"]
        server = json.loads((ROOT / "server" / "maps" / f"{name}.tmj").read_text("utf-8"))
        client = json.loads((ROOT / "client" / "assets" / "maps" / f"{name}.tmj").read_text("utf-8"))
        assert server == client, name


def test_the_elites_strike_in_their_own_rhythm():
    for kind, (land, rank, _) in NEW.items():
        info = catalog.monsters()[kind]
        if rank != "elite":
            assert "attack_shape" not in info, kind
            continue
        rhythm = info["attack_shape"]
        assert isinstance(rhythm, list) and len(set(rhythm)) >= 2, kind
        w = World(mono=FakeMono())
        m = next(x for x in w._channels(lands.zone_of(land))[0].monsters if x.kind == kind)
        assert [combat.next_shape(m) for _ in range(2 * len(rhythm))] == rhythm * 2, kind


def test_the_lightning_sprites_leave_the_boss_fight_fair():
    w = World(mono=FakeMono())
    ch = w._channels(lands.zone_of("loi_kiep_dai"))[0]
    sprites = [a for a in ch.map.monster_areas if a.props["monster"] == "loi_linh"]
    boss = next(a for a in ch.map.monster_areas if a.props["monster"] == "loi_long")
    info, boss_info = catalog.monsters()["loi_linh"], catalog.monsters()["loi_long"]
    assert len(sprites) == 2 and sum(int(a.props["count"]) for a in sprites) == 2
    assert not info["aggressive"] and info["atk"] < boss_info["atk"] / 2 and info["rank"] == "normal"
    for a in sprites:   # out of the boss's reach even when it stands at the edge of its own area
        gap = max(boss.x - (a.x + a.w), a.x - (boss.x + boss.w))
        assert gap > boss_info["aggro_radius"], a.name


def test_every_new_creature_has_a_picture_today():
    wiring = json.loads((ROOT / "client" / "assets" / "v2" / "wiring.json").read_text("utf-8"))
    for kind, (_, rank, hovers) in NEW.items():
        sheet = wiring["monsters"][kind]
        assert (ROOT / "client" / "assets" / "v2" / "monsters" / f"{sheet}.png").exists(), kind
        if hovers:
            assert sheet in wiring["monster_float"], kind


# ------------------------------------------------------------------ the six beasts, as data
def test_the_six_beasts_are_in_the_game():
    for bid, gtype in GIFTS.items():
        b = bplan(bid)
        assert b["status"] == "co" and b["gift"]["type"] == gtype and gtype in math_tree.GIFT_TYPES
        assert bid in beasts.built() and bid in pets.species()


def test_a_beast_waiting_for_its_art_is_nowhere(waiting):
    for bid, gtype in GIFTS.items():
        b = waiting["all"][bid]
        assert b["status"] == "cho_hinh" and b["gift"]["type"] == gtype and gtype in math_tree.GIFT_TYPES
        assert bid not in beasts.built() and bid not in pets.species()
        assert beasts.gift_value(bid, gtype) == 0, "a beast waiting for its art gives nothing"
        w = World(mono=FakeMono())
        ch = w._channels(lands.zone_of(b["land"]))[0]
        assert not [m for m in ch.monsters if m.kind == bid]


def test_the_six_beasts_are_spread_over_luyen_khi():
    stages = {bid: bplan(bid)["requires"]["stage"] for bid in GIFTS}
    assert min(stages.values()) == 3 and max(stages.values()) == 9
    assert stages["cuu_vi_ho"] >= 8 and stages["kim_si_dieu"] >= 8
    assert any(bplan(b)["needs"] == "dap_kiem_luot" for b in GIFTS)
    assert len({bplan(b)["land"] for b in GIFTS}) == 6, "one new beast for each land of Luyện Khí"
    for bid in GIFTS:
        assert 0 < bplan(bid)["gift"]["value"] <= math_tree.SMALL_GIFT_MAX


def test_flipped_they_pass_every_rule_of_the_plan():
    plan = flipped_plan()
    assert math_tree.validate_world(plan, math_tree.tree()) == []
    # a spot two beasts share, or a weapon's, is refused; so is an immodest gift
    bad = copy.deepcopy(plan)
    nb = next(b for b in bad["beasts"] if b["id"] == "ngoc_tho")
    nb["pos"] = next(b for b in bad["beasts"] if b["id"] == "kim_si_dieu")["pos"]
    nb["land"] = "luu_van_coc"
    assert any("already the spot" in e for e in math_tree.validate_world(bad, math_tree.tree()))
    bad = copy.deepcopy(plan)
    next(b for b in bad["beasts"] if b["id"] == "bach_ho_con")["gift"]["value"] = 0.9
    assert any("bach_ho_con" in e and "modest" in e for e in math_tree.validate_world(bad, math_tree.tree()))
    bad = copy.deepcopy(plan)
    next(b for b in bad["beasts"] if b["id"] == "cuu_vi_ho")["status"] = "maybe"
    assert any("cuu_vi_ho" in e for e in math_tree.validate_world(bad, math_tree.tree()))


@pytest.fixture
def check_all():
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import check_all as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


def test_flipping_the_status_is_the_only_change_needed_for_the_art_check(check_all, monkeypatch, tmp_path):
    assert check_all.check_beasts() == [], "with the artists' sheets in, the check passes"
    # without their art (the tree as it was before the artists delivered) the check names the six...
    real = ROOT / "client" / "assets" / "v2"
    bare = tmp_path / "bare"
    shutil.copytree(real / "beasts", bare / "beasts")
    wiring = json.loads((real / "wiring.json").read_text("utf-8"))
    for bid in BESTIARY:
        wiring["spirit_beasts"].pop(bid, None)
        for f in (bare / "beasts").glob(f"{bid}.*"):
            f.unlink()
    (bare / "wiring.json").write_text(json.dumps(wiring), "utf-8")
    missing = [e for e in check_all.check_beasts(bare) if e.startswith("beast ")]
    assert {e.split()[1].rstrip(":") for e in missing} == BESTIARY
    # ...and is quiet about them while they wait
    plan = waiting_plan()
    monkeypatch.setattr(math_tree, "world_plan", lambda *a, **k: plan)
    assert [e for e in check_all.check_beasts(bare) if e.startswith("beast ")] == []
    plan = flipped_plan()
    monkeypatch.setattr(math_tree, "world_plan", lambda *a, **k: plan)
    # the artists' files: a sheet with every clip and the spirit_beasts line
    v2 = tmp_path / "v2"
    shutil.copytree(real / "beasts", v2 / "beasts")
    wiring = json.loads((real / "wiring.json").read_text("utf-8"))
    for bid in BESTIARY:
        wiring["spirit_beasts"][bid] = bid
        clips = {c: {} for c in check_all.BEAST_CLIPS}
        (v2 / "beasts" / f"{bid}.json").write_text(json.dumps({"clips": clips}), "utf-8")
        (v2 / "beasts" / f"{bid}.png").write_bytes(b"")
    (v2 / "wiring.json").write_text(json.dumps(wiring), "utf-8")
    assert [e for e in check_all.check_beasts(v2) if e.startswith("beast ")] == []


# ------------------------------------------------------------------ flipped: in the game
def test_flipped_each_lands_its_new_beast(live, gw):
    for bid in GIFTS:
        b = bplan(bid)
        ch = gw._pick_channel(lands.zone_of(b["land"]))
        m = next(x for x in ch.monsters if getattr(x, "beast", False) and x.kind == bid)
        assert (m.x, m.y) == (b["pos"][0] * 16 + 8, b["pos"][1] * 16 + 12)
    assert set(GIFTS) <= set(pets.species())


async def test_flipped_ngoc_tho_is_tamed_by_parries(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_1", "Bách Thú Một")
    s.tree = pos(bplan("ngoc_tho")["requires"]["stage"])
    p, m = at_beast(gw, s, "ngoc_tho", near=6)
    assert m.shows_to(p)
    await provoke(gw, p, m)
    t = await tame(client, gw, h, s, p, m)
    assert t["yielded"] and t["need"] == bplan("ngoc_tho")["parries_to_tame"]


async def test_ngoc_tho_heals_on_every_parry(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_2", "Bách Thú Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    p.pet = "ngoc_tho"
    p.hp = p.max_hp / 2
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    hp = p.hp
    res = await answer(client, h, s, True)
    want = p.max_hp * bplan("ngoc_tho")["gift"]["value"]
    assert res["combat"]["healed"] == int(round(want)) and p.hp == pytest.approx(hp + want)
    assert events(s, "heal")[-1]["id"] == p.eid
    # never past the full bar, and nothing without the rabbit
    p.hp = p.max_hp
    assert combat.parry_heal(p.channel, p) == 0
    p.hp, p.pet = p.max_hp / 2, None
    assert combat.parry_heal(p.channel, p) == 0


async def test_tam_bao_thu_and_kim_thiem_better_the_loot(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_3", "Bách Thú Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    base = combat._loot_bonus(p, m)
    p.pet = "tam_bao_thu"
    stones = combat._loot_bonus(p, m)
    assert stones["stones_pct"] == pytest.approx(base["stones_pct"] + 100 * bplan("tam_bao_thu")["gift"]["value"])
    assert stones["drop_mult"] == base["drop_mult"]
    p.pet = "kim_thiem"
    luck = combat._loot_bonus(p, m)
    assert luck["drop_mult"] == pytest.approx(base["drop_mult"] * (1 + bplan("kim_thiem")["gift"]["value"]))
    assert luck["stones_pct"] == base["stones_pct"]


async def test_kim_thiem_luck_never_opens_a_locked_drop(live, client, gw):
    """Drop luck only raises chances: an item above the killer's tu vi still comes as locked."""
    h, uid, s = await fighter(client, gw, "bt_7", "Bách Thú Bảy")
    want = loot.need_vi("an_ruong_de")          # Vong Hồn Kiếm Sĩ's an_ruong_de: Luyện Khí tầng 6
    luck = beasts.loot_gift("kim_thiem", {"stones_pct": 0.0, "drop_mult": 1.0})
    assert luck["drop_mult"] > 1
    luck["drop_mult"] = 1e6                       # every roll succeeds: only the gate is left
    import random
    s.sent.clear()
    await combat._reward(uid, "vong_hon_kiem_si", luck, rng=random.Random(1))
    out = next(m for m in reversed(s.sent) if m.get("t") == "loot")
    assert "an_ruong_de" not in {x.get("item_id") for x in out.get("items", [])}
    assert any(e["need_vi"] == want for e in out.get("locked", []))



async def test_bach_ho_con_raises_cong(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_4", "Bách Thú Bốn")
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        before = await cultivation.current_stats(db, ch)
        db.add(Pet(user_id=uid, pet_type="bach_ho_con", level=1, equipped=True))
        await db.flush()
        after = await cultivation.current_stats(db, ch)
    assert after["atk"] == int(round(before["atk"] * (1 + bplan("bach_ho_con")["gift"]["value"])))
    assert after["atk"] > before["atk"] and after["def"] == before["def"]


async def test_cuu_vi_ho_adds_tu_vi_to_right_answers(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_5", "Bách Thú Năm")
    async with dbm.SessionLocal() as db:
        db.add(Pet(user_id=uid, pet_type="cuu_vi_ho", level=1, equipped=True))
        await db.commit()
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    res = await answer(client, h, s, True)
    xp = res["xp"]["gained"]
    assert res["math"]["pet_skill"] == "xp_bonus"
    assert res["math"]["pet_xp"] == math.ceil(xp * bplan("cuu_vi_ho")["gift"]["value"]) > 0
    run(gw, float(math_tree.world_plan()["combat"]["question_cooldown_seconds"]) + 0.1)
    await take_blow(gw, s, p, m)                 # a wrong answer pays nothing extra
    wrong = await answer(client, h, s, False)
    assert "pet_xp" not in wrong["math"]


async def test_kim_si_dieu_lengthens_the_glide(live, client, gw):
    h, uid, s = await fighter(client, gw, "bt_6", "Bách Thú Sáu")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    base = float(abilities.glide_cfg()["max_px"])
    assert abilities.glide_max_px(p) == base
    p.pet = "kim_si_dieu"
    far = base * (1 + bplan("kim_si_dieu")["gift"]["value"])
    assert abilities.glide_max_px(p) == pytest.approx(far)
    ch = p.channel
    x0, y0 = p.x, p.y
    # somewhere a plain glide cannot reach but the roc's can (straight along open ground, if any)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d = (base + far) / 2
        x1, y1 = x0 + dx * d, y0 + dy * d
        if abilities.check_glide(ch, x0, y0, x1, y1, far) is None:
            assert abilities.check_glide(ch, x0, y0, x1, y1) == "too_far"
            break
    else:
        pytest.skip("no open ground around the test spot")
    await settle(gw)
