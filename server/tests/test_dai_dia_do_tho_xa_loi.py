"""Đại Địa Đồ, the second wave (2026-11-21): Thiên Công Phường and Linh Xạ Nguyên are giant lands
cut into khu by band of tu vi; Lôi Kiếp Đài grew into a pilgrimage up to its terrace and keeps no
bands (its boss and its two Lôi Linh behave exactly as before). Places are read from the maps and
world_plan.json, never written here."""
import json
import random

import pytest

from app.learning import math_tree
from app.realtime import ai, dia_do, lands, maps
from app.systems import catalog

GIANT = ("thien_cong_phuong", "linh_xa_nguyen")
BOSS = "loi_kiep_dai"
TILE = 16


def spawned(zone: str) -> list:
    return ai.spawn_all(maps.load(zone), random.Random(4))


@pytest.mark.parametrize("zone", GIANT)
def test_the_land_has_khu_of_every_band_and_camps_first(zone):
    ks = dia_do.khu_list(zone)
    real = [k for k in ks if k["band"]]
    assert 6 <= len(real) <= 9 and {k["band"] for k in real} == {1, 2, 3}
    camps = [k for k in ks if k["band"] == 0]
    assert len(camps) >= 3 and ks[:len(camps)] == tuple(camps), "a camp after each wall, listed first"
    for k in ks:
        assert k["land"] == lands.zone_land_id(zone) and k["name_vi"]
        x, y, w, h = k["rect"]
        assert x <= k["anchor"][0] <= x + w and y <= k["anchor"][1] <= y + h
        if k["band"]:
            assert (k["stage_min"], k["stage_max"]) == dia_do.band_range(k["band"])
    kinds = {p["poi"] for p in dia_do.poi_list(zone)}
    assert {"gate", "camp", "landmark", "beast"} <= kinds


@pytest.mark.parametrize("zone", GIANT)
def test_its_creatures_spawn_by_band_and_band_3_has_only_elites(zone):
    ms = spawned(zone)
    assert 100 <= len(ms) <= dia_do.distribution()["max_monsters_per_land"]
    plan = next(l for l in math_tree.world_plan()["lands"] if l["map"] == zone)
    assert {m.kind for m in ms} == set(plan["monsters"]), "every creature of the land lives somewhere"
    for m in ms:
        band = int(m.area.props["band"])
        assert m.band == band and band in (1, 2, 3)
        info = catalog.monsters()[m.kind]
        assert info["land"] == lands.zone_land_id(zone)
        if band == 3:       # no normal creature of the land reaches tầng 7-9: the elites hold Thâm Xứ
            assert info["rank"] == "elite", m.kind
        if band == 1:
            assert info["rank"] == "normal", m.kind


@pytest.mark.parametrize("zone", GIANT)
def test_every_weapon_and_beast_lies_in_the_khu_of_its_stage(zone):
    land = lands.zone_land_id(zone)
    plan = math_tree.world_plan()
    spots = [(f"{w['weapon']} {w['quality']}", w["pos"], w["requires"]["stage"])
             for w in plan["weapons_placed"] if w.get("land") == land and w.get("pos")]
    spots += [(b["id"], b["pos"], b["requires"]["stage"]) for b in plan["beasts"]
              if b.get("land") == land and b.get("pos") and b.get("status") == "co"]
    assert len(spots) >= 4
    for what, (tx, ty), stage in spots:
        k = dia_do.khu_at(zone, tx * TILE + 8, ty * TILE + 8)
        assert k is not None, what
        if k["band"]:
            assert k["stage_min"] <= stage <= k["stage_max"], (what, k["id"], stage)
        else:
            assert stage <= dia_do.band_range(1)[1], f"{what}: only a first-band reward waits in a camp"


def test_the_boss_terrace_keeps_no_bands_and_its_three_areas():
    assert dia_do.khu_list(BOSS) == ()
    zmap = maps.load(BOSS)
    names = {a.name: a.props["monster"] for a in zmap.monster_areas}
    assert names == {"loi_long": "loi_long", "loi_linh_tay": "loi_linh", "loi_linh_dong": "loi_linh"}
    ms = spawned(BOSS)
    assert sorted(m.kind for m in ms) == ["loi_linh", "loi_linh", "loi_long"]
    assert all(m.band == 0 and m.info is catalog.monsters()[m.kind] for m in ms), "exactly the old monsters"
    pois = {p["poi"] for p in dia_do.poi_list(BOSS)}
    assert {"gate", "camp", "boss"} <= pois
    # the long way up: the boss stands far north of the gate the player arrives at
    sx, sy = zmap.spawns["from_village"]
    boss = next(m for m in ms if m.kind == "loi_long")
    assert sy - boss.y > 40 * TILE


def test_the_village_signs_name_their_direction_in_words():
    """The fonts draw "→" but not the other arrows: the village's signs say where in words."""
    data = json.loads((maps.MAP_DIR / "truc_lam_thon.tmj").read_text("utf-8"))
    texts = [p["value"] for l in data["layers"] if l["type"] == "objectgroup" for o in l["objects"]
             if o.get("type") == "sign" for p in o.get("properties", []) if p["name"] == "text"]
    assert len(texts) >= 6
    for text in texts:
        assert not set(text) & {"↑", "↓", "←"}, text
