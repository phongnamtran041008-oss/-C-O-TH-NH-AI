"""Rơi đồ theo tu vi (2026-11-20): good loot from monsters and bí cảnh unlocks only as the player
climbs; not every monster drops everything. Rules in app/systems/loot.py, data in
data/loot_tiers.json."""
import copy
import random
from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app import db as dbm
from app.models import Character, InventoryItem, User
from app.realtime import combat
from app.systems import catalog, items, loot, math_dungeon, math_fortune, secret_realm
from tests.test_combat import FakeMono, fighter, gw, last, settle  # noqa: F401  (gw is a fixture)


async def set_tier(uid: int, realm: str, stage: int) -> None:
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        ch.realm, ch.realm_stage = realm, stage
        await db.commit()


async def held(uid: int) -> dict[str, int]:
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(InventoryItem).where(InventoryItem.user_id == uid))).scalars().all()
    out: dict[str, int] = {}
    for r in rows:
        out[r.item_id] = out.get(r.item_id, 0) + r.quantity
    return out


# ------------------------------------------------------------------ tiers
def test_tiers_parse_and_compare():
    assert loot.parse("pham_nhan") == (0, 0) and loot.parse("pham_nhan:0") == (0, 0)
    assert loot.parse("luyen_khi") == (1, 1) and loot.parse("luyen_khi:4") == (1, 4)
    assert loot.parse("truc_co") == loot.parse("truc_co:1") == (2, 1)
    assert loot.parse("luyen_khi:9") < loot.parse("truc_co:1") < loot.parse("truc_co:3") < loot.parse("kim_dan")
    assert loot.compare("luyen_khi:7", "luyen_khi:3") == 1 and loot.compare("truc_co", "truc_co:1") == 0
    assert loot.compare("pham_nhan", "luyen_khi:1") == -1
    for bad in ("", "tien_nhan", "luyen_khi:10", "luyen_khi:0", "luyen_khi:x", "pham_nhan:1", None):
        with pytest.raises(ValueError):
            loot.parse(bad)
    assert loot.top() == loot.parse("dai_thua:3")


def test_unlocked_need_and_fail_closed():
    assert loot.unlocked("muc_tinh", "pham_nhan", 0)
    assert not loot.unlocked("truc_co_dan", "luyen_khi", 6) and loot.unlocked("truc_co_dan", "luyen_khi", 7)
    assert not loot.unlocked("manh_bao_vat", "truc_co", 3) and loot.unlocked("manh_bao_vat", "kim_dan", 1)
    assert loot.need_vi("truc_co_dan") == "Luyện Khí tầng 7"
    assert loot.need_vi("linh_qua") == "Trúc Cơ sơ kỳ"
    assert loot.need_vi("manh_bao_vat") == "Kết Đan sơ kỳ"
    assert loot.need_vi("muc_tinh") == "Phàm Nhân"
    # an item the file forgot is locked for everyone below the top tier...
    assert "trung_ong_thien" not in loot.data()["items"]
    assert not loot.unlocked("trung_ong_thien", "hop_the", 3) and loot.unlocked("trung_ong_thien", "dai_thua", 3)
    # ...but a ghi chú lỗi sai (a learning aid) is never gated
    note = next(k for k, v in catalog.math_drops().items() if v.get("kind") == "note")
    assert loot.unlocked(note, "pham_nhan", 0) and note not in loot.data()["items"]


def test_rarity_cap():
    assert loot.rarity_cap("pham_nhan", 0) == "pham"
    assert loot.rarity_cap("luyen_khi", 5) == "linh" and loot.rarity_cap("luyen_khi", 6) == "huyen"
    assert loot.rarity_cap("truc_co", 1) == "dia" and loot.rarity_cap("kim_dan", 1) == "thien"
    rng = random.Random(3)
    assert {loot.roll_equipment_rarity(rng, None, "pham_nhan", 0) for _ in range(300)} == {"pham"}
    assert loot.roll_equipment_rarity(rng, "linh", "pham_nhan", 0) is None         # min above the cap: skipped
    assert {loot.roll_equipment_rarity(rng, None, "luyen_khi", 1) for _ in range(500)} == {"pham", "linh"}
    seen = {loot.roll_equipment_rarity(rng, None, "truc_co", 1) for _ in range(3000)}
    assert "dia" in seen and "thien" not in seen
    assert items.roll_rarity(rng, "huyen", "huyen") == "huyen"


def test_gear_also_stays_within_the_cap_of_its_source():
    """A high player does not pull high gear out of a low source: the first forest is capped at
    Luyện Khí tầng 5, where only Phàm and Linh gear has unlocked."""
    rng = random.Random(11)
    forest = loot.source_cap("rung_muc_loang")
    assert forest == loot.parse("luyen_khi:5") and loot.best_rarity(forest) == "linh"
    assert loot.monster_cap("ink_fox") == forest                        # it lives only in that forest
    assert loot.monster_cap("ink_slime") == loot.parse("luyen_khi:9")   # also by the lake: the kinder cap
    seen = {loot.roll_equipment_rarity(rng, None, "dai_thua", 3, within=forest) for _ in range(3000)}
    assert seen == {"pham", "linh"}
    assert loot.source_cap("mac_anh_dong") is None                      # the big bí cảnh has no cap
    free = {loot.roll_equipment_rarity(rng, None, "dai_thua", 3, within=None) for _ in range(6000)}
    assert "huyen" in free and "dia" in free
    # the player's own tu vi still comes first
    assert {loot.roll_equipment_rarity(rng, None, "pham_nhan", 0, within=forest) for _ in range(300)} == {"pham"}
    # an entry's own minimum is never undercut (validate() keeps it inside the source's cap anyway)
    assert loot.roll_equipment_rarity(rng, "huyen", "truc_co", 1, within=forest) == "huyen"


def test_locked_payload_is_deduplicated_and_short():
    out: dict = {}
    for item_id in ("truc_co_dan", "truc_co_dan", "linh_qua", "manh_bao_vat", "loi_ma_tran"):
        loot.note_locked(out, item_id)
    assert out["locked"] == [{"name_vi": "Trúc Cơ Đan", "need_vi": "Luyện Khí tầng 7"},
                             {"name_vi": "Linh Quả", "need_vi": "Trúc Cơ sơ kỳ"},
                             {"name_vi": "Mảnh Bảo Vật", "need_vi": "Kết Đan sơ kỳ"}]


# ------------------------------------------------------------------ the sources
def test_the_loot_data_is_sound():
    assert loot.validate() == []


def test_validate_catches_an_unlisted_item_and_a_source_over_its_cap():
    raw = copy.deepcopy(loot.data())
    del raw["items"]["loi_ma_tran"]
    assert any("loi_ma_tran" in e and "no tier" in e for e in loot.validate(raw))
    raw = copy.deepcopy(loot.data())
    raw["source_caps"]["rung_muc_loang"] = "pham_nhan"          # the forest's wisps drop Mặc Linh Chi
    out = loot.validate(raw)
    assert any("mac_linh_chi" in e and "cap of rung_muc_loang" in e for e in out), out
    raw = copy.deepcopy(loot.data())
    raw["source_caps"]["khe_nut_muc"] = "luyen_khi:3"           # the rift's chest holds Lõi Ma Trận
    assert any("loi_ma_tran" in e and "khe_nut_muc" in e for e in loot.validate(raw))
    raw = copy.deepcopy(loot.data())
    raw["items"]["truc_co_dan"] = "truc_co:1"                   # a breakthrough pill out of reach
    assert any("truc_co_dan" in e and "last stage" in e for e in loot.validate(raw))
    raw = copy.deepcopy(loot.data())
    del raw["source_caps"]["toan_tran"]
    assert any("source_caps.toan_tran missing" in e for e in loot.validate(raw))


def test_the_breakthrough_pill_left_the_first_forest():
    """The first forest is capped at Luyện Khí tầng 5: Trúc Cơ Đan drops from the hardest
    Luyện Khí source, the valley's Đối Xứng Ma, and never in the forest."""
    mons = catalog.monsters()
    forest = loot._zone_monsters()["rung_muc_loang"]
    assert not any(d.get("item") in ("truc_co_dan", "dp_truc_co") for k in forest for d in mons[k]["drops"])
    assert "dstt_doi_xung_ma" in loot._zone_monsters()["loan_so_coc"]
    assert {"truc_co_dan", "dp_truc_co"} <= {d.get("item") for d in mons["dstt_doi_xung_ma"]["drops"]}


def test_the_thien_fish_can_be_caught_again():
    """Linh Quả - the only ingredient of the bait for Cá Chép Hóa Long - has a source again: a
    bí cảnh that may hold it."""
    assert "linh_qua_vun" in catalog.fish()["chep_hoa_long"]["bait"]
    assert catalog.baits()["linh_qua_vun"]["craft"]["from"] == "linh_qua"
    caps = loot.data()["source_caps"]
    holders = [sid for sid, src in loot.sources().items() if "linh_qua" in {i for i, _ in src["items"]}]
    assert "mac_anh_dong" in holders and "toan_tran" in holders
    for sid in holders:
        assert caps[sid] is None or loot.parse(caps[sid]) >= loot.item_tier("linh_qua")


# ------------------------------------------------------------------ the gate where loot is paid
async def test_a_low_player_never_gets_the_high_drop_a_high_player_does(client, gw):
    """Đối Xứng Ma drops Lõi Ma Trận (Luyện Khí 4) and Trúc Cơ Đan (Luyện Khí 7). With every drop
    forced (drop_mult), a Phàm Nhân gets neither over many kills - they show as locked - while a
    Luyện Khí 7 player gets both."""
    _, low, s_low = await fighter(client, gw, "thap_tu", "Thấp Tu")
    _, high, s_high = await fighter(client, gw, "cao_tu", "Cao Tu")
    await set_tier(high, "luyen_khi", 7)
    forced = {"stones_pct": 0.0, "drop_mult": 100.0}
    for seed in range(15):
        await combat._reward(low, "dstt_doi_xung_ma", forced, rng=random.Random(seed))
        await combat._reward(high, "dstt_doi_xung_ma", forced, rng=random.Random(seed))
    await settle(gw)
    lo, hi = await held(low), await held(high)
    assert "truc_co_dan" not in lo and "loi_ma_tran" not in lo and "dp_truc_co" not in lo
    assert lo.get("muc_tinh", 0) > 0
    assert hi.get("truc_co_dan", 0) >= 15 and hi.get("loi_ma_tran", 0) >= 30
    msg = last(s_low, "loot")
    assert {"name_vi": "Trúc Cơ Đan", "need_vi": "Luyện Khí tầng 7"} in msg["locked"]
    assert {"name_vi": "Lõi Ma Trận", "need_vi": "Luyện Khí tầng 4"} in msg["locked"]
    assert len(msg["locked"]) <= loot.MAX_LOCKED
    assert "locked" not in last(s_high, "loot")


async def test_gear_above_the_cap_is_skipped(client, gw, monkeypatch):
    _, uid, s = await fighter(client, gw, "giap_tu", "Giáp Tu")
    mons = dict(catalog.monsters())
    mons["ink_fox"] = {**mons["ink_fox"], "drops": [{"equipment": ["gay_truc"], "chance": 1.0, "min_rarity": "huyen"}]}
    monkeypatch.setattr(catalog, "monsters", lambda: mons)
    await combat._reward(uid, "ink_fox", rng=random.Random(1))
    await settle(gw)
    msg = last(s, "loot")
    assert not msg["equipment"] and msg["locked"][0]["need_vi"] == "Luyện Khí tầng 6"
    await set_tier(uid, "luyen_khi", 6)
    await combat._reward(uid, "ink_fox", rng=random.Random(1))
    await settle(gw)
    assert [e["rarity"] for e in last(s, "loot")["equipment"]] == ["huyen"]


async def test_a_high_player_gets_no_high_gear_from_the_first_forest(client, gw, monkeypatch):
    """The same monster, the same Đại Thừa player, the same dice: killed in the first forest
    (cap Luyện Khí tầng 5) its gear is Phàm or Linh only; killed by the lake (cap tầng 9) it can
    be Huyền too."""
    _, uid, s = await fighter(client, gw, "dai_nang", "Đại Năng")
    await set_tier(uid, "dai_thua", 3)
    mons = dict(catalog.monsters())
    mons["ink_slime"] = {**mons["ink_slime"], "drops": [{"equipment": ["gay_truc"], "chance": 1.0}]}
    monkeypatch.setattr(catalog, "monsters", lambda: mons)
    seen = {"rung_muc_loang": set(), "ho_nghien_muc": set()}
    for place, got in seen.items():
        for seed in range(400):
            await combat._reward(uid, "ink_slime", rng=random.Random(seed), source=place)
            await settle(gw)
            got.update(e["rarity"] for e in last(s, "loot")["equipment"])
    assert seen["rung_muc_loang"] == {"pham", "linh"}
    assert "huyen" in seen["ho_nghien_muc"] and "dia" not in seen["ho_nghien_muc"]


async def test_the_realm_chest_pays_fragments_only_above_the_gate(client, gw):
    _, low, _s = await fighter(client, gw, "manh_thap", "Mảnh Thấp")
    _, high, _s2 = await fighter(client, gw, "manh_cao", "Mảnh Cao")
    await set_tier(low, "truc_co", 3)
    await set_tier(high, "kim_dan", 1)
    async with dbm.SessionLocal() as db:
        run_id = await secret_realm.create_run(db, "mac_anh_dong", [low, high])
        await db.commit()
    a = await secret_realm.claim_chest(run_id, low, "mac_anh_dong", 5, False)
    b = await secret_realm.claim_chest(run_id, high, "mac_anh_dong", 5, False)
    assert "manh_bao_vat" not in {i["item"] for i in a["items"]}
    assert {"name_vi": "Mảnh Bảo Vật", "need_vi": "Kết Đan sơ kỳ"} in a["locked"]
    assert {"item": "manh_bao_vat", "qty": 5} in [{"item": i["item"], "qty": i["qty"]} for i in b["items"]]
    assert (await held(high)).get("manh_bao_vat") == 5 and "manh_bao_vat" not in await held(low)


async def test_a_weighted_table_is_filtered_before_it_is_weighed(client, gw):
    _, uid, _s = await fighter(client, gw, "ruong_tu", "Rương Tu")
    heavy = [{"item": "linh_qua", "weight": 1000}, {"item": "muc_tinh", "weight": 1}]
    async with dbm.SessionLocal() as db:
        for seed in range(20):
            out = {"items": [], "equipment": []}
            await secret_realm._grant_table(db, uid, random.Random(seed), heavy, "t", out, ("pham_nhan", 0))
            assert [i["item"] for i in out["items"]] == ["muc_tinh"]
        out = {"items": [], "equipment": []}
        await secret_realm._grant_table(db, uid, random.Random(0), heavy[:1], "t", out, ("pham_nhan", 0))
        assert out == {"items": [], "equipment": []}                 # nothing left: nothing extra
        out = {"items": [], "equipment": []}
        await secret_realm._grant_table(db, uid, random.Random(0), heavy, "t", out, ("truc_co", 1))
        assert [i["item"] for i in out["items"]] == ["linh_qua"]
        await db.commit()


async def test_room_loot_is_gated(client, gw, monkeypatch):
    _, uid, _s = await fighter(client, gw, "phong_tu", "Phòng Tu")
    from app import balance
    c = copy.deepcopy(balance.load("realm"))
    c["room_loot_by_realm"]["toan_tran"]["items"] = [{"item": "loi_ma_tran", "chance": 1.0, "qty": [1, 1]},
                                                     {"item": "manh_tap_hop", "chance": 1.0, "qty": [1, 1]}]
    monkeypatch.setattr(secret_realm, "cfg", lambda: c)
    async with dbm.SessionLocal() as db:
        run_id = await secret_realm.create_run(db, "toan_tran", [uid])
        await db.commit()
    got = await secret_realm.claim_room(run_id, uid, 0, "seal", "toan_tran")
    assert [i["item"] for i in got["items"]] == ["manh_tap_hop"]
    assert got["locked"] == [{"name_vi": "Lõi Ma Trận", "need_vi": "Luyện Khí tầng 4"}]


async def test_dungeon_and_fortune_rewards_are_gated(client, gw):
    _, uid, _s = await fighter(client, gw, "ham_tu", "Hầm Tu")
    run = SimpleNamespace(rewarded=True, id=1, stones_gained=0, items_gained={})
    async with dbm.SessionLocal() as db:
        r = await math_dungeon._grant(db, uid, run, {"stones": 5, "items": {"manh_tap_hop": 2, "loi_ma_tran": 3}},
                                      "chest")
        assert [i["item_id"] for i in r["items"]] == ["manh_tap_hop"] and run.items_gained == {"manh_tap_hop": 2}
        assert r["locked"] == [{"name_vi": "Lõi Ma Trận", "need_vi": "Luyện Khí tầng 4"}]
        user = await db.get(User, uid)
        ev = {"id": "thu_nghiem", "rewards": {"stones": [0, 0], "items": [{"item": "manh_tap_hop", "qty": 1},
                                                                          {"item": "an_ruong_de", "qty": 1}]}}
        f = await math_fortune.grant(db, user, ev)
        assert [i["item"] for i in f["items"]] == ["manh_tap_hop"]
        assert f["locked"] == [{"name_vi": "Ấn Rương Đề", "need_vi": "Luyện Khí tầng 6"}]
        await db.commit()
    assert "an_ruong_de" not in await held(uid) and "loi_ma_tran" not in await held(uid)
