"""Quái của bí cảnh (docs/BI_CANH_QUAI.md): what a run fields depends on which bí cảnh it is
(its theme) and on the band of tu vi of the party (the weakest member's place in Đạo Thụ).

The pure part (app/systems/realm_quai.py: bands, plans, a rift's land, the check) first; then the
live runs (app/realtime/realm.py) on the fake clock of test_realm, with the party's places in
Đạo Thụ set by hand (lands.load_pos), and the loot of a band (app/systems/secret_realm.py)."""
import copy
import json
import random

import pytest

from app import db as dbm
from app.config import DATA_DIR
from app.realtime import dia_do, lands
from app.realtime.lands import TreePos
from app.systems import catalog, loot, math_realm, realm_quai, secret_realm
from tests.test_combat import fighter, settle
from tests.test_loot import held, set_tier
from tests.test_realm import gw, hero, make_party, tick  # noqa: F401  (gw is a fixture)

MUC, RIFT, TRAN = "mac_anh_dong", "khe_nut_muc", "toan_tran"
INK = realm_quai.ink_family()


def pos(stage: int, realm: str = "luyen_khi") -> TreePos:
    return TreePos(realm, stage, frozenset())


def mons() -> dict:
    return catalog.monsters()


def rooms_of(realm_id: str) -> int:
    return len(secret_realm.realms()[realm_id]["math"]["rooms"])


def raw() -> dict:
    return json.loads((DATA_DIR / "realms.json").read_text("utf-8"))


# ------------------------------------------------------------------ the band of a party
def test_the_band_is_the_stage_being_learned():
    assert realm_quai.band_of_pos(None) == 1
    assert realm_quai.band_of_pos(TreePos.newcomer()) == 1          # learning tầng 1
    assert [realm_quai.band_of_stage("luyen_khi", s) for s in range(10)] == [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]
    assert realm_quai.band_of_stage("truc_co", 0) == 3               # beyond Luyện Khí: the deepest band
    assert realm_quai.band_vi(2) == "Trung Vực"


def test_a_mixed_party_takes_the_weakest_members_band():
    assert realm_quai.party_band([pos(7), pos(4), pos(8)]) == 2
    assert realm_quai.party_band([pos(8), TreePos.newcomer()]) == 1
    assert realm_quai.party_band([pos(0, "ket_dan"), pos(6)]) == 3
    assert realm_quai.party_band([]) == 1


# ------------------------------------------------------------------ each bí cảnh x each band
@pytest.mark.parametrize("band", [1, 2, 3])
def test_mac_anh_dong_fields_the_ink_family(band):
    p = realm_quai.plan(MUC, band, random.Random(band), rooms_of(MUC))
    assert p["band"] == band and len(p["rooms"]) == 3
    kinds = [k for room in p["rooms"] for k in room]
    assert kinds and set(kinds) <= INK
    elites = [k for k in kinds if mons()[k]["rank"] == "elite"]
    # the elite Mặc Hồ guards the last room before the boss, from Trung Vực on
    assert elites == ([] if band == 1 else ["ink_fox"]) and (band == 1 or p["rooms"][-1][-1] == "ink_fox")
    assert p["boss"]["kind"] == "nghien_ma" and p["boss"]["hp_mult"] == 1.0 and not p["boss"]["overlay"]


@pytest.mark.parametrize("band", [1, 2, 3])
def test_toan_tran_fields_mistake_monsters_of_the_bands_floors(band):
    p = realm_quai.plan(TRAN, band, random.Random(band), rooms_of(TRAN))
    kinds = [k for room in p["rooms"] for k in room]
    floors = {mons()[k]["floor"] for k in kinds}
    assert all(mons()[k].get("skill") for k in kinds)                  # quái lỗi sai only
    assert floors == set(range(1, band + 1))                           # floor 1 / 1-2 / 1-3
    assert any(mons()[k]["floor"] == 1 for k in p["rooms"][0])         # the first room always has floor 1
    last_elites = [k for k in p["rooms"][-1] if mons()[k]["rank"] == "elite"]
    assert len(last_elites) == (0 if band == 1 else 1)                 # the warden of the last room
    boss = p["boss"]
    body = mons()[boss["kind"]]
    assert body["rank"] == "elite" and body["floor"] == band           # the Trận Chủ: the band's deepest floor
    assert boss["overlay"]["group_shield"] and boss["overlay"]["rank"] == "boss"
    assert boss["overlay"]["name_vi"].startswith("Trận Chủ ") and boss["hp_mult"] == 0.6


def test_deeper_bands_field_more():
    for rid, n in ((MUC, 3), (TRAN, 2)):
        totals = [sum(len(r) for r in realm_quai.plan(rid, b, random.Random(0), n)["rooms"]) for b in (1, 2, 3)]
        assert totals[0] <= totals[1] <= totals[2] and totals[0] < totals[2], (rid, totals)


def test_every_kind_of_a_row_appears_before_any_twice():
    for seed in range(20):
        room = realm_quai.plan(MUC, 1, random.Random(seed), 3)["rooms"][1]
        assert set(room) == {"ink_slime", "tone_wisp", "muc_anh"}


# ------------------------------------------------------------------ the rift and its land
def khu_of(zone: str, band: int) -> dict:
    return next(k for k in dia_do.khu_list(zone) if k["band"] == band)


def rift(zone: str, k: dict | None, band: int) -> dict:
    o = {"zone": zone, "x": k["anchor"][0] if k else None, "y": k["anchor"][1] if k else None}
    return realm_quai.plan(RIFT, band, random.Random(3), 1, o)


def areas_of_khu(zone: str, khu_id: str) -> set[str]:
    return {a.props["monster"] for a in realm_quai._zone_areas(zone) if a.props.get("khu") == khu_id}


def test_a_rift_in_kiem_trung_son_thâm_xu_spills_that_khus_creatures():
    k = khu_of("loan_so_coc", 3)
    p = rift("loan_so_coc", k, 3)
    kinds = p["rooms"][0]
    assert p["band"] == 3 and p["khu"] == k["id"] and p["from"] == "khu"
    assert set(kinds) <= areas_of_khu("loan_so_coc", k["id"])
    assert all(mons()[x].get("land") == "kiem_trung_son" for x in kinds)
    assert len(kinds) == 4 and mons()[kinds[-1]]["rank"] == "elite"    # 3 normals + one of its elites
    assert p["boss"]["kind"] == "nghien_ma" and p["boss"]["hp_mult"] == 0.5
    assert p["boss"]["overlay"] == {"name_vi": "Nghiên Ma Non"}


def test_a_rift_in_luu_van_coc_ngoai_vi_spills_its_valley_creatures():
    k = khu_of("luu_van_coc", 1)
    p = rift("luu_van_coc", k, 1)
    assert p["band"] == 1 and p["khu"] == k["id"]
    assert set(p["rooms"][0]) <= areas_of_khu("luu_van_coc", k["id"]) and len(p["rooms"][0]) == 2
    assert all(mons()[x]["rank"] == "normal" and mons()[x]["land"] == "luu_van_coc" for x in p["rooms"][0])


def test_a_rift_never_drags_a_weak_party_up_nor_a_strong_one_past_its_khu():
    deep, shallow = khu_of("luu_van_coc", 3), khu_of("luu_van_coc", 1)
    weak = rift("luu_van_coc", deep, 1)                 # a Ngoại Vi party at a rift in Thâm Xứ
    assert weak["band"] == 1 and weak["khu"] is None and weak["from"] == "band"
    band1 = {a.props["monster"] for a in realm_quai._zone_areas("luu_van_coc") if a.props.get("band") == "1"}
    assert set(weak["rooms"][0]) <= band1
    strong = rift("luu_van_coc", shallow, 3)            # a Thâm Xứ party at a rift in Ngoại Vi
    assert strong["band"] == 1 and strong["khu"] == shallow["id"]


def test_a_band_of_elites_only_borrows_the_normals_below():
    p = rift("luu_van_coc", khu_of("luu_van_coc", 3), 3)   # Lưu Vân Cốc's Thâm Xứ: elites only
    normals, elite = p["rooms"][0][:-1], p["rooms"][0][-1]
    assert normals and all(mons()[x]["rank"] == "normal" for x in normals)
    assert mons()[elite]["rank"] == "elite"


def test_a_rift_on_a_land_without_khu_and_nowhere_at_all():
    p = rift("ho_nghien_muc", None, 2)
    zone_kinds = {a.props["monster"] for a in realm_quai._zone_areas("ho_nghien_muc")}
    assert p["band"] == 2 and p["from"] in ("zone", "band", "khu") and set(p["rooms"][0]) <= zone_kinds
    p = realm_quai.plan(RIFT, 3, random.Random(0), 1, {"zone": "no_such_zone", "x": 1, "y": 1})
    assert p["from"] == "fallback" and set(p["rooms"][0]) <= INK and p["rooms"][0][-1] == "ink_fox"
    p = realm_quai.plan(RIFT, 1, random.Random(0), 1, None)     # no origin at all (tests, old callers)
    assert p["rooms"][0] and set(p["rooms"][0]) <= INK


# ------------------------------------------------------------------ the check
def test_the_data_is_sound_and_wired_into_the_realm_check():
    assert realm_quai.validate() == [] and math_realm.validate() == [] and loot.validate() == []


def test_validate_catches_what_breaks_the_distribution(monkeypatch):
    bad = copy.deepcopy(raw())
    del bad["realms"][MUC]["quai"]["bands"]["3"]                                   # a band without a pool
    bad["realms"][MUC]["quai"]["bands"]["1"]["rooms"][0]["kinds"].append("kiem_linh")   # another theme
    bad["realms"][TRAN]["quai"]["bands"]["1"]["rooms"][0]["kinds"].append("dstt_chi_so_ma")  # floor 3 in band 1
    bad["realms"][TRAN]["quai"]["bands"]["1"]["rooms"][1]["elite"] = "dstt_anh_trung_ma"     # elite in band 1
    bad["realms"][TRAN]["quai"]["bands"]["2"]["rooms"][0]["kinds"].append("khong_co")         # unknown
    bad["realms"][TRAN]["quai"]["bands"]["3"]["boss"] = {"kind": "dstt_doi_xung_ma"}          # no group shield
    bad["realms"][RIFT]["quai"]["bands"]["2"]["rooms"].append({"kinds": "land", "count": 1})  # a room too many
    out = "\n".join(realm_quai.validate(bad))
    for bit in (f"realm {MUC} band 3: missing", "kiem_linh is not of the ink family", "floor 3, above",
                "no elite in band 1", "unknown creature 'khong_co'", "no group shield", "one row per room"):
        assert bit in out, (bit, out)
    monkeypatch.setattr(realm_quai, "has_picture", lambda kind: kind != "but_yeu")
    assert any("but_yeu has no picture" in e for e in realm_quai.validate())
    assert any("but_yeu has no picture" in e for e in math_realm.validate())       # reached by check_all


def test_every_fielded_creature_has_its_picture():
    for rid in (MUC, RIFT, TRAN):
        for kind in realm_quai.fielded(rid):
            assert realm_quai.has_picture(kind), (rid, kind)


def test_loot_counts_every_fielded_creature_in_the_realms_cap():
    src = loot.sources()
    seen = {w for _, w in src[RIFT]["items"]}
    assert any("van_xa" in w for w in seen) and any("thiet_giap_thu" in w for w in seen)   # a rift's lands
    assert any("dstt_doi_xung_ma" in w for w in {w for _, w in src[TRAN]["items"]})        # the Trận Chủ


# ------------------------------------------------------------------ the live run
def set_tree(monkeypatch, stages: dict[int, int]) -> None:
    async def load_pos(db, uid):
        return pos(stages[uid]) if uid in stages else TreePos.newcomer()
    monkeypatch.setattr(lands, "load_pos", load_pos)


async def enter(gw, realm_id, leader, *others, rooms=None):
    if others:
        await make_party(gw, leader, *others)
    gw.realms.room_order = rooms
    await gw.handle(leader, {"t": "realm", "op": "enter", "realm": realm_id})
    await settle(gw)
    return gw.realms.instance_of(gw.players[leader.user_id])


async def test_a_mixed_party_runs_at_its_weakest_members_band(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "tron_a", "Trộn A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "tron_b", "Trộn B", realm_id="luyen_khi")
    set_tree(monkeypatch, {a: 7, b: 4})                                  # Thâm Xứ and Trung Vực
    inst = await enter(gw, TRAN, sa, sb)
    assert inst is not None and inst.band == 2
    assert inst.monsters and all(m.band == 2 and m.full()["kv"] == 2 for m in inst.monsters)
    assert {mons()[m.kind]["floor"] for m in inst.monsters} <= {1, 2}
    start = next(m for m in reversed(sa.sent) if m.get("event") == "start")
    assert start["run"]["band"] == 2 and start["run"]["band_vi"] == "Trung Vực"
    m = inst.monsters[0]
    base = mons()[m.kind]
    assert m.info["hp"] == round(base["hp"] * dia_do.mult(2, None, "hp"), 2) and m.max_hp == m.info["hp"]


async def test_a_deep_solo_run_meets_the_tran_chu_of_its_band(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "tran_chu", "Trận Chủ", realm_id="luyen_khi")
    set_tree(monkeypatch, {a: 8})
    inst = await enter(gw, TRAN, sa, rooms=["boss"])
    await tick(gw, 3.5)
    boss = inst.boss
    assert inst.band == 3 and boss is not None and boss.kind == "dstt_doi_xung_ma"
    info = boss.info
    assert info["group_shield"] and info["rank"] == "boss" and info["name_vi"] == "Trận Chủ Đối Xứng Ma"
    assert info["skill"] == mons()["dstt_doi_xung_ma"]["skill"]          # still itself under the boss's numbers
    nghien = mons()["nghien_ma"]
    assert info["hp"] == round(nghien["hp"] * dia_do.mult(3, None, "hp"), 2)
    assert round(boss.max_hp) == round(info["hp"] * 0.6)                 # alone: no extra member
    assert boss.full()["kv"] == 3 and boss.full()["n"] == "Trận Chủ Đối Xứng Ma"
    room = next(m for m in reversed(sa.sent) if m.get("event") == "room")
    assert room["name_vi"] == "Trận Tâm"                                 # Toán Trận's own den
    q = next(m for m in reversed(sa.sent) if m.get("t") == "q")["q"]
    assert q["math"]["realm_asker"] == "boss"                            # the overlay's group shield asks the bài tổng hợp


async def test_the_ink_cave_fields_its_own_and_mac_ho_guards_the_last_room(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "hang_a", "Hang A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "hang_b", "Hang B", realm_id="luyen_khi")
    set_tree(monkeypatch, {a: 5, b: 5})
    inst = await enter(gw, MUC, sa, sb)
    assert inst.band == 2 and {m.kind for m in inst.monsters} <= INK
    assert inst.quai["rooms"][-1][-1] == "ink_fox"


async def test_a_rift_run_spills_the_creatures_of_its_khu(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "khe_a", "Khe A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "khe_b", "Khe B", realm_id="luyen_khi")
    set_tree(monkeypatch, {a: 8, b: 6})
    k = khu_of("loan_so_coc", 3)
    x, y = k["anchor"]
    for s, dx in ((sa, 0), (sb, 8)):
        gw._place(s, "loan_so_coc", x + dx, y, "down")
    ch = gw.players[a].channel
    r = gw.realms.spawn_rift(ch, gw.mono(), x + 4, y)
    await make_party(gw, sa, sb)
    gw.realms.room_order = None
    await gw.handle(sa, {"t": "realm", "op": "enter", "rift": r.id})
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[a])
    assert inst is not None and inst.realm_id == RIFT and inst.band == 3 and inst.quai["khu"] == k["id"]
    assert inst.origin == {"zone": "loan_so_coc", "x": x + 4, "y": y}
    kinds = [m.kind for m in inst.monsters]
    assert set(kinds) <= areas_of_khu("loan_so_coc", k["id"]) and len(kinds) == 4
    assert all(m.band == 3 for m in inst.monsters)


async def test_the_gate_shows_the_band_of_the_party(client, gw, monkeypatch):
    h, a, sa = await hero(client, gw, "cong_a", "Cổng A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "cong_b", "Cổng B", realm_id="luyen_khi")
    set_tree(monkeypatch, {a: 7, b: 1})
    v = (await client.get("/realms", headers=h)).json()
    row = next(r for r in v["math_realms"] if r["id"] == TRAN)
    assert row["band"] == 3 and row["band_vi"] == "Thâm Xứ" and row["band_party"] is False
    await make_party(gw, sa, sb)
    sb_sess = gw.sessions[b]
    sb_sess.tree = pos(1)                                               # a mate's place, kept on the session
    v = (await client.get("/realms", headers=h)).json()
    assert all(r["band"] == 1 and r["band_vi"] == "Ngoại Vi" and r["band_party"] for r in v["realms"] + v["math_realms"])


# ------------------------------------------------------------------ the loot of a band
def test_a_band_takes_out_what_lies_above_its_cap_but_the_treasures():
    table = [{"item": "manh_tap_hop", "weight": 1}, {"item": "loi_ma_tran", "weight": 1},
             {"item": "linh_qua", "weight": 1}]
    assert [e["item"] for e in secret_realm._in_band(table, 1, ["linh_qua"])] == ["manh_tap_hop", "linh_qua"]
    assert [e["item"] for e in secret_realm._in_band(table, 2, ["linh_qua"])] == ["manh_tap_hop", "loi_ma_tran",
                                                                                   "linh_qua"]
    assert secret_realm._in_band(table, 0) == table                      # no band: the old rule
    assert secret_realm._band_stones([10, 20], 1) == [10, 20]
    assert secret_realm._band_stones([10, 20], 3) == [round(10 * 1.45), round(20 * 1.45)]


async def test_room_and_chest_loot_stay_within_the_band(client, gw, monkeypatch):
    from app import balance
    _, uid, _s = await fighter(client, gw, "dai_tu", "Đại Tu")
    await set_tier(uid, "kim_dan", 1)                                    # every item unlocked for the player
    c = copy.deepcopy(balance.load("realm"))
    c["room_loot_by_realm"][MUC]["items"] = [{"item": "loi_ma_tran", "chance": 1.0, "qty": [1, 1]},
                                             {"item": "manh_tap_hop", "chance": 1.0, "qty": [1, 1]}]
    c["chest"][MUC]["table"] = [{"item": "loi_ma_tran", "weight": 1000, "qty": [1, 1]},
                                {"item": "linh_qua", "weight": 1, "qty": [1, 1]}]
    monkeypatch.setattr(secret_realm, "cfg", lambda: c)
    async with dbm.SessionLocal() as db:
        run_id = await secret_realm.create_run(db, MUC, [uid])
        await db.commit()
    room = await secret_realm.claim_room(run_id, uid, 0, "seal", MUC, band=1)
    assert [i["item"] for i in room["items"]] == ["manh_tap_hop"] and not room.get("locked")   # skipped, not locked
    lo, hi = c["room_loot_by_realm"][MUC]["stones"]
    assert lo <= room["stones"] <= hi
    chest = await secret_realm.claim_chest(run_id, uid, MUC, 4, False, band=1)
    got = {i["item"] for i in chest["items"]}
    assert "loi_ma_tran" not in got and "linh_qua" in got               # the treasure is not the band's
    assert "manh_bao_vat" in got                                         # nor the Mảnh Bảo Vật
    assert (await held(uid)).get("manh_bao_vat") == 4
