"""Đại Địa Đồ (2026-11-21): the bands of tu vi of the giant lands (realtime/dia_do.py,
data/math/dia_do.json) - the khu of Kiếm Trủng Sơn, Lưu Vân Cốc, Mê Đồ Lâm and Vạn Tượng Trạch, a monster's band from its
area, its scaled numbers, its capped drops, `kv` in its record, and the asker that prefers the
nodes of the band. Every number is read from the data, never repeated here."""
import random

import pytest

from app.learning import math_tree
from app.realtime import ai, combat, dia_do, lands, maps
from app.systems import catalog, cultivation, loot
from tests.test_combat import fighter, gw, last, settle  # noqa: F401  (gw is a fixture)
from tests.test_loot import set_tier

GIANT = ("loan_so_coc", "luu_van_coc", "rung_muc_loang", "ho_nghien_muc")
FORCED = 1000.0


def bands() -> dict:
    return dia_do.data()["realms"]["luyen_khi"]


def spawned(zone: str) -> list:
    return ai.spawn_all(maps.load(zone), random.Random(4))


def plain_spawned(tmp_path) -> list:
    """The monsters of a map without bands (a small map with monster areas and no khu)."""
    import json
    area = {"id": 2, "name": "slimes", "type": "monster_area", "x": 32, "y": 32, "width": 160, "height": 160,
            "properties": [{"name": "monster", "type": "string", "value": "ink_slime"},
                           {"name": "count", "type": "string", "value": "3"}]}
    doc = {"width": 20, "height": 20, "tilewidth": 16, "tileheight": 16,
           "layers": [{"type": "tilelayer", "name": "ground", "data": [1] * 400},
                      {"type": "objectgroup", "name": "objects", "objects": [
                          {"id": 1, "name": "spawn", "type": "spawn", "x": 100, "y": 100, "width": 0, "height": 0},
                          area]},
                      {"type": "objectgroup", "name": "collision", "objects": []}]}
    p = tmp_path / "plain.tmj"
    p.write_text(json.dumps(doc), "utf-8")
    return ai.spawn_all(maps.parse(p), random.Random(4))


# ------------------------------------------------------------------ the data
def test_the_band_table_is_sound_and_rises_gently():
    assert dia_do.validate() == []
    assert [dia_do.band_range(b) for b in (1, 2, 3)] == [(1, 3), (4, 6), (7, 9)]
    assert dia_do.band_def(0) is None and dia_do.band_range(0) is None and dia_do.mult(0, None, "hp") == 1.0
    assert dia_do.loot_cap(1) == "luyen_khi:3" and dia_do.loot_cap(2) == "luyen_khi:6"
    assert dia_do.loot_cap(3) == "luyen_khi:9"
    for key in dia_do.MULT_KEYS:
        assert dia_do.mult(1, None, key) == 1.0, "band 1 is the old monster unchanged"
        assert dia_do.mult(1, None, key) <= dia_do.mult(2, None, key) <= dia_do.mult(3, None, key) <= 2.0


def test_validate_names_a_band_that_falls():
    bad = dia_do.data()
    bad = {**bad, "realms": {"luyen_khi": {**bad["realms"]["luyen_khi"],
                                           "3": {**bad["realms"]["luyen_khi"]["3"], "loot_cap": "luyen_khi:2"}}}}
    assert any("loot_cap is lower" in e for e in dia_do.validate(bad))


# ------------------------------------------------------------------ the khu of the two lands
@pytest.mark.parametrize("zone", GIANT)
def test_a_giant_land_has_khu_of_every_band_and_camps_first(zone):
    ks = dia_do.khu_list(zone)
    real = [k for k in ks if k["band"]]
    assert 6 <= len(real) <= 9 and {k["band"] for k in real} == {1, 2, 3}
    camps = [k for k in ks if k["band"] == 0]
    assert camps and ks[:len(camps)] == tuple(camps), "the camps come first (they win where khu overlap)"
    assert all(k["safe"] for k in camps) and not any(k["safe"] for k in real)
    for k in ks:
        assert k["land"] == lands.zone_land_id(zone) and k["name_vi"]
        x, y, w, h = k["rect"]
        assert x <= k["anchor"][0] <= x + w and y <= k["anchor"][1] <= y + h
        assert dia_do.khu_at(zone, *k["anchor"]) is not None
        if k["band"]:
            assert (k["stage_min"], k["stage_max"]) == dia_do.band_range(k["band"])
    pois = dia_do.poi_list(zone)
    assert {"gate", "camp", "landmark"} <= {p["poi"] for p in pois}


def test_khu_ids_are_unique_in_the_world_and_found_by_id():
    ids = [k["id"] for k in dia_do.all_khu()]
    assert len(ids) == len(set(ids)) and len(ids) >= 2 * 9
    assert dia_do.khu("kts_dinh")["zone"] == "loan_so_coc" and dia_do.khu("lvc_cao_nguyen")["band"] == 3
    assert dia_do.khu("mdl_me_cung")["zone"] == "rung_muc_loang" and dia_do.khu("vtt_mieu_chim")["band"] == 3
    assert dia_do.khu_list("truc_lam_thon") == () and dia_do.poi_list("truc_lam_thon") == []


# ------------------------------------------------------------------ a monster's band
@pytest.mark.parametrize("zone", GIANT)
def test_every_monster_of_a_giant_land_takes_the_band_of_its_area(zone):
    budget = dia_do.distribution()["max_monsters_per_land"]
    ms = spawned(zone)
    assert 100 <= len(ms) <= budget
    for m in ms:
        band = int(m.area.props["band"])
        assert m.band == band and band in (1, 2, 3)
        assert m.full()["kv"] == band
        k = dia_do.khu(m.area.props["khu"])
        assert k["band"] == band and k["zone"] == zone


def test_a_monster_without_bands_is_the_old_monster(tmp_path):
    ms = plain_spawned(tmp_path)
    assert ms and all(m.band == 0 and "kv" not in m.full() for m in ms)
    assert all(m.info is catalog.monsters()[m.kind] for m in ms)


def test_the_numbers_of_a_band_are_scaled_where_they_are_read():
    base = catalog.monsters()["thiet_giap_thu"]
    by_band = {}
    for m in spawned("loan_so_coc"):
        if m.kind == "thiet_giap_thu":
            by_band.setdefault(m.band, m)
    assert set(by_band) >= {1, 2, 3}, "Thiết Giáp Thú lives in the three bands"
    for band, m in by_band.items():
        k = bands()[str(band)]["mult"]
        assert m.info["hp"] == pytest.approx(base["hp"] * k["hp"], abs=0.01)
        assert m.max_hp == pytest.approx(base["hp"] * k["hp"], abs=0.01)
        assert m.info["atk"] == pytest.approx(base["atk"] * k["atk"], abs=0.01)
        assert m.info["def"] == pytest.approx(base["def"] * k["def"], abs=0.01)
        assert m.info["xp"] == int(round(base["xp"] * k["xp"]))
        assert m.info["speed"] == base["speed"] and m.info["name_vi"] == base["name_vi"]
        assert m.info is m.info, "worked out once"
    assert by_band[1].info == base


# ------------------------------------------------------------------ drops of a band
def test_the_cap_of_a_band_never_lifts_the_zone_cap():
    lk = loot.parse
    assert loot.band_within(lk("luyen_khi:9"), 1) == lk("luyen_khi:3")
    assert loot.band_within(None, 2) == lk("luyen_khi:6")
    assert loot.band_within(lk("luyen_khi:5"), 3) == lk("luyen_khi:5"), "never above the zone's own cap"
    assert loot.band_within(lk("luyen_khi:9"), 0) == lk("luyen_khi:9"), "no band: as before"
    assert not loot.band_allows("truc_co_dan", 1) and loot.band_allows("truc_co_dan", 3)
    assert loot.band_allows("truc_co_dan", 0)
    note = next(i for i, d in catalog.math_drops().items() if d.get("kind") == "note")
    assert loot.band_allows(note, 1), "a ghi chú lỗi sai is never gated"
    assert loot.best_rarity(loot.band_within(lk("luyen_khi:9"), 1)) == "linh"


async def test_a_kill_in_a_band_pays_that_band_and_drops_within_its_cap(client, gw, monkeypatch):
    _, uid, s = await fighter(client, gw, "dai_dia_do_1", "Thâm Xứ Một")
    await set_tier(uid, "dai_thua", 3)                     # a player no tu vi of their own holds back
    xp = []
    real = cultivation.add_xp

    async def add_xp(db, user_id, amount, why):
        xp.append(amount)
        return await real(db, user_id, amount, why)
    monkeypatch.setattr(cultivation, "add_xp", add_xp)
    kind = "ma_tran_thu"                                    # drops Lôi Kiếp Tinh Hạch (luyen_khi:8)
    info = catalog.monsters()[kind]
    item = "loi_kiep_tinh_hach"
    assert any(d.get("item") == item for d in info["drops"])
    forced = {"stones_pct": 0.0, "drop_mult": FORCED}
    got = {}
    for band in (1, 3):
        await combat._reward(uid, kind, forced, rng=random.Random(8), source="loan_so_coc", x=1.0, y=2.0,
                             band=band, band_realm="luyen_khi")
        await settle(gw)
        msg = last(s, "loot")
        got[band] = {i["item"] for i in msg["items"]}
        k = bands()[str(band)]["mult"]
        lo, hi = info["stones"]
        assert int(round(lo * k["stones"])) <= msg["stones"] <= int(round(hi * k["stones"]))
        assert xp[-1] == int(round(info["xp"] * k["xp"]))
        assert all(l["name_vi"] != catalog.item_name(item) for l in msg.get("locked", [])), \
            "above the band's cap it is not part of the place: never reported as locked"
    assert item not in got[1] and item in got[3]


# ------------------------------------------------------------------ the asker of a band
class _St:
    def __init__(self):
        self.tree = math_tree.tree()


def test_a_creature_prefers_the_nodes_of_its_band(tmp_path):
    nodes = catalog.monsters()["thiet_giap_thu"]["nodes"]
    t = math_tree.tree()
    for m in spawned("loan_so_coc"):
        if m.kind != "thiet_giap_thu":
            continue
        lo, hi = dia_do.band_range(m.band)
        pref = lands.LandAsker.band_nodes(_St(), nodes, m)
        assert pref and all(lo <= t.nodes[n].stage <= hi for n in pref)
    assert lands.LandAsker.band_nodes(_St(), nodes, None) == []
    plain = plain_spawned(tmp_path)[0]
    assert lands.LandAsker.band_nodes(_St(), nodes, plain) == []


async def test_the_asker_tries_the_band_first_then_the_rest(monkeypatch):
    asker = lands.LandAsker(lands.land("kiem_trung_son"))
    nodes = ["a", "b", "c", "d"]
    monkeypatch.setattr(asker, "_playable", lambda st, ns: [f"part {n}" for n in ns])
    tried = []

    async def pick(db, user, part, rng, highest=False):
        tried.append(part)
        return None
    monkeypatch.setattr(lands.LandAsker, "_pick", staticmethod(pick))
    assert await asker._of_nodes(None, None, None, nodes, random.Random(1), prefer=["c"]) is None
    assert tried[0] == "part c" and sorted(tried) == ["part a", "part b", "part c", "part d"]
    tried.clear()
    assert await asker._of_nodes(None, None, None, nodes, random.Random(1)) is None
    assert sorted(tried) == ["part a", "part b", "part c", "part d"], "no band: every node, as before"
