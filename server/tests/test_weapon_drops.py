"""Binh khí rơi từ quái (world_plan.json `weapon_drops`, systems/weapons.py roll_drops, called by
realtime/combat._reward): the five qualities, the drop odds by rank, the loot rule (the killer's
cultivation tu vi and the cap of the place of the kill), the kỳ binh that only drop, the types
that wait for their art, and the `loot` message that tells the client where a piece lies.
Every number is read from the plan, never repeated here."""
import copy
import json
import random
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest
from sqlalchemy import select

from app import db as dbm
from app.models import EquipmentInstance
from app.realtime import combat
from app.systems import catalog, loot, weapons
from tests.test_combat import fighter, gw, last, settle  # noqa: F401  (gw is a fixture)
from tests.test_loot import set_tier

ROOT = Path(__file__).resolve().parents[2]
NORMAL, ELITE, BOSS = "kiem_linh", "ma_tran_thu", "loi_long"     # Kiếm Trủng Sơn and Lôi Kiếp Đài
TOP = ("dai_thua", 3)                                              # a player no tu vi cap holds back
FORCED = 1000.0                                                    # a drop_mult that makes every roll drop


def by_rank(rank: str) -> dict:
    return weapons.data()["drops"]["by_rank"][rank]


def rolls(kind: str, n: int, tier=TOP, within=None, mult: float = 1.0, seed: int = 7):
    rng = random.Random(seed)
    grants, locked = [], []
    for _ in range(n):
        g, lk = weapons.roll_drops(rng, kind, *tier, within=within, drop_mult=mult)
        grants.append(g)
        locked += lk
    return grants, locked


# ------------------------------------------------------------------ the five qualities
def test_every_quality_maps_to_its_rarity_and_glows_in_its_colour():
    d = weapons.data()
    assert list(d["qualities"]) == ["ha", "trung", "thuong", "cuc", "tuyet"]
    assert {q: x["rarity"] for q, x in d["qualities"].items()} == weapons.QUALITY_RARITY
    rar = catalog.equipment()["rarities"]
    for q in weapons.qualities_view():
        assert q["color"] == rar[q["rarity"]]["color"], q
    powers = [x["power"] for x in weapons.qualities_view()]
    assert powers == sorted(powers) and len(set(powers)) == 5
    for qid, q in d["qualities"].items():
        assert weapons.quality_of_rarity(q["rarity"])["id"] == qid


# ------------------------------------------------------------------ which types drop
def test_kỳ_binh_only_drop_and_are_never_placed():
    d = weapons.data()
    ky = [k for k, t in d["types"].items() if t.get("drop_only")]
    assert set(ky) == {"kich", "roi", "am_khi", "luan", "phu", "cam"}
    placed_types = {weapons.split(p["weapon"])[0] for p in d["placed"]}
    assert not placed_types & set(ky)
    for k in ky:
        t = d["types"][k]
        main = [x for x, y in d["types"].items() if y.get("land") == t["land"] and not y.get("drop_only")]
        assert main, f"{k}: its land has a main type it is rarer than"
        assert t["why_vi"] and t["clip"] in weapons.CLIPS


def test_the_six_kỳ_binh_are_in_the_game():
    d = weapons.data()
    assert {k for k, t in d["types"].items() if t["status"] == "cho_hinh"} == set(), "their art is in"
    items = catalog.equipment()["items"]
    for k in ("kich", "roi", "am_khi", "luan", "phu", "cam"):
        assert d["types"][k]["status"] == "co"
        assert f"{k}_1" in items and f"{k}_1" in weapons.droppable_weapons()


def test_a_type_waiting_for_its_art_never_drops_and_is_not_equipment(kich_waiting):
    waiting = ["kich"]
    items = catalog.equipment()["items"]
    for k in waiting:
        assert not any(w.startswith(k + "_") for w in weapons.droppable_weapons())
        assert not any(i.startswith(k + "_") for i in items)
        assert weapons.is_weapon(f"{k}_1"), "still a weapon of the plan, as data"
    seen = set()
    for kind in (ELITE, BOSS):
        grants, _ = rolls(kind, 200, mult=FORCED)
        seen |= {weapons.split(g["weapon"])[0] for gs in grants for g in gs}
    assert not seen & set(waiting)


def test_a_land_drops_its_own_type_at_its_realms_grade():
    for kind in (NORMAL, ELITE, "van_xa", "dau_tu_oa", "tri_chu_tinh", "co_quan_nhan", "tam_ma"):
        land = catalog.monsters()[kind]["land"]
        types = weapons.data()["types"]
        own = {k for k, t in types.items() if t.get("land") == land and not t.get("drop_only")}
        rare = {k for k, t in types.items() if t.get("land") == land and t.get("drop_only")}
        if catalog.monsters()[kind]["rank"] == "normal":
            rare = set()          # the kỳ binh of a land only from its elites and bosses
        grants, _ = rolls(kind, 50, mult=FORCED)
        got = {g["weapon"] for gs in grants for g in gs}
        assert got == {f"{k}_1" for k in own | rare}, (kind, got)
    assert weapons.roll_drops(random.Random(1), "ink_slime", *TOP, drop_mult=FORCED) == ([], []), "no land"


# ------------------------------------------------------------------ the odds
@pytest.mark.parametrize("kind,rank", [(NORMAL, "normal"), (ELITE, "elite"), (BOSS, "boss")])
def test_the_drop_chance_follows_the_rank(kind, rank):
    n = 4000
    grants, _ = rolls(kind, n)
    types = weapons.data()["types"]       # the main type's chance: a kỳ binh rolls on its own
    rate = sum(1 for gs in grants
               if any(not types[weapons.split(g["weapon"])[0]].get("drop_only") for g in gs)) / n
    want = by_rank(rank)["chance"]
    assert abs(rate - want) < max(0.02, want * 0.25), (rank, rate, want)


def test_normal_rare_elite_sometimes_boss_surely():
    c = [by_rank(r)["chance"] for r in ("normal", "elite", "boss")]
    assert c[0] < c[1] < c[2] == 1.0
    assert by_rank("normal")["ky_binh_chance"] == 0
    assert 0 < by_rank("elite")["ky_binh_chance"] < by_rank("elite")["chance"]


def test_the_quality_odds_follow_the_rank():
    """With no cap at all, the qualities of a boss's drops come out at the plan's odds."""
    n = 6000
    grants, _ = rolls(BOSS, n, tier=TOP)
    got = Counter(g["quality"] for gs in grants for g in gs if weapons.split(g["weapon"])[1] == 1)
    total = sum(got.values())
    for q, p in by_rank("boss")["qualities"].items():
        assert abs(got[q] / total - p) < 0.025, (q, got[q] / total, p)


def test_a_normal_drops_mostly_ha_pham():
    grants, _ = rolls(NORMAL, 600, mult=FORCED)
    got = Counter(g["quality"] for gs in grants for g in gs)
    assert got["ha"] > got["trung"] > got["thuong"] and not got["cuc"] and not got["tuyet"]


# ------------------------------------------------------------------ the loot rule
def test_the_killers_tu_vi_caps_the_quality_and_the_roll_is_reported_locked():
    """A Phàm Nhân may only get Phàm gear: every boss drop is hạ phẩm, and the better rolls show
    as locked with the stage they open at."""
    grants, locked = rolls(BOSS, 300, tier=("pham_nhan", 0))
    assert {g["quality"] for gs in grants for g in gs} == {"ha"}
    needs = {x["need_vi"] for x in locked}
    assert loot.label(loot.rarity_tier("linh")) in needs and loot.label(loot.rarity_tier("huyen")) in needs
    assert any("(Trung phẩm)" in x["name_vi"] for x in locked)
    # at Luyện Khí 6 up to thượng phẩm
    grants, locked = rolls(BOSS, 300, tier=("luyen_khi", 6))
    assert {g["quality"] for gs in grants for g in gs} == {"ha", "trung", "thuong"}


def test_the_place_of_the_kill_caps_the_quality_without_a_locked_report():
    """The first forest (cap Luyện Khí 5) gives nothing above trung phẩm even to an Đại Thừa -
    that is the place, not the player, so nothing is reported as locked."""
    cap = loot.source_cap("rung_muc_loang")
    best = loot.best_rarity(cap)
    grants, locked = rolls(BOSS, 400, tier=TOP, within=cap)
    rarities = {g["rarity"] for gs in grants for g in gs}
    from app.systems.items import RARITY_ORDER
    assert max(RARITY_ORDER.index(r) for r in rarities) == RARITY_ORDER.index(best)
    assert not [x for x in locked if "phẩm)" in x["name_vi"]]


def test_both_caps_the_lower_one_wins():
    granted, held = weapons.cap_quality("tuyet", "luyen_khi", 1, within=loot.parse("luyen_khi:9"))
    assert granted == "trung" and held == "thuong"          # the place allows thượng, the player not yet
    assert weapons.cap_quality("ha", "pham_nhan", 0) == ("ha", None)
    assert weapons.cap_quality("cuc", *TOP) == ("cuc", None)


def test_the_boss_drops_grade_two_only_from_truc_co():
    grants, locked = rolls(BOSS, 300, tier=("luyen_khi", 9))
    assert {weapons.split(g["weapon"])[1] for gs in grants for g in gs} == {1}
    assert any(x["name_vi"].startswith(weapons.data()["grades"][2]["prefix_vi"]) for x in locked)
    assert all(len(gs) >= 1 for gs in grants), "a boss surely drops, grade 1 in place of a locked grade 2"
    grants, _ = rolls(BOSS, 300, tier=("truc_co", 1))
    assert {weapons.split(g["weapon"])[1] for gs in grants for g in gs} == {1, 2}


def test_nothing_drops_while_the_section_is_not_wired(monkeypatch):
    monkeypatch.setattr(weapons, "drops_wired", lambda: False)
    assert weapons.roll_drops(random.Random(1), BOSS, *TOP, drop_mult=FORCED) == ([], [])


# ------------------------------------------------------------------ through a kill
async def test_a_kill_grants_the_weapon_and_says_where_it_lies(client, gw):
    _, uid, s = await fighter(client, gw, "nhat_kiem", "Nhặt Kiếm")
    await set_tier(uid, "luyen_khi", 6)
    forced = {"stones_pct": 0.0, "drop_mult": FORCED}
    await combat._reward(uid, NORMAL, forced, rng=random.Random(3), source="loan_so_coc", x=200.0, y=330.0)
    await settle(gw)
    msg = last(s, "loot")
    drops = [e for e in msg["equipment"] if e.get("weapon_info")]
    assert len(drops) == 1
    e = drops[0]
    assert {"item", "name_vi", "rarity", "color", "quality", "quality_vi", "weapon", "x", "y"} <= set(e)
    assert e["item"] == "kiem_1" and e["weapon"] is True and e["name_vi"] == weapons.weapon_name("kiem_1")
    q = weapons.data()["qualities"][e["quality"]]
    assert e["rarity"] == q["rarity"] and e["quality_vi"] == q["name_vi"]
    assert e["color"] == catalog.equipment()["rarities"][e["rarity"]]["color"]
    assert (e["x"], e["y"]) == (200.0, 330.0)
    assert e["rarity_vi"] and e["id"], "the old fields stay: today's client toasts with them"
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(EquipmentInstance).where(EquipmentInstance.user_id == uid))).scalars().all()
    assert [(r.item_id, r.rarity) for r in rows] == [("kiem_1", e["rarity"])], "granted at once: nothing is lost"


async def test_old_gear_drops_carry_their_place_too(client, gw):
    _, uid, s = await fighter(client, gw, "do_cu", "Đồ Cũ")
    forced = {"stones_pct": 0.0, "drop_mult": FORCED}
    await combat._reward(uid, ELITE, forced, rng=random.Random(5), source="loan_so_coc", x=50.0, y=60.0)
    await settle(gw)
    msg = last(s, "loot")
    old = [e for e in msg["equipment"] if not e.get("weapon_info")]
    assert old and all(e["item"] in ("kiem_go_dao", "nhan_ma_tran") for e in old)
    for e in old:
        assert e["quality"] is None and e["weapon"] == (e["slot"] == "weapon")
        assert abs(e["x"] - 50) <= 10 and abs(e["y"] - 60) <= 8
    places = [(e["x"], e["y"]) for e in msg["equipment"]]
    assert len(set(places)) == len(places), "two pieces of one kill do not lie on each other"


async def test_a_locked_roll_reaches_the_player(client, gw, monkeypatch):
    _, uid, s = await fighter(client, gw, "pham_tu", "Phàm Tu")
    odds = copy.deepcopy(weapons.data()["drops"])
    odds["by_rank"]["normal"]["qualities"] = {"ha": 0, "trung": 1.0, "thuong": 0, "cuc": 0, "tuyet": 0}
    patched = {**weapons.data(), "drops": odds}
    monkeypatch.setattr(weapons, "data", lambda: patched)
    forced = {"stones_pct": 0.0, "drop_mult": FORCED}
    await combat._reward(uid, NORMAL, forced, rng=random.Random(2), source="loan_so_coc", x=1.0, y=2.0)
    await settle(gw)
    msg = last(s, "loot")
    got = [e for e in msg["equipment"] if e.get("weapon_info")]
    assert [e["quality"] for e in got] == ["ha"], "a Phàm Nhân gets the hạ phẩm"
    assert {"name_vi": f"{weapons.weapon_name('kiem_1')} (Trung phẩm)",
            "need_vi": loot.label(loot.rarity_tier("linh"))} in msg["locked"]


# ------------------------------------------------------------------ the status flip
@pytest.fixture
def check_all():
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import check_all as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


def _kich(monkeypatch, status: str):
    patched = copy.deepcopy(weapons.data())
    patched["types"]["kich"]["status"] = status
    monkeypatch.setattr(weapons, "data", lambda: patched)
    catalog.equipment.cache_clear()
    return patched


@pytest.fixture
def kich_live(monkeypatch):
    """Kích as 'co' - the one change the plan needed once its art was in (it is, since 2026-11-20)."""
    yield _kich(monkeypatch, "co")
    catalog.equipment.cache_clear()


@pytest.fixture
def kich_waiting(monkeypatch):
    """Kích back to 'cho_hinh': how a new type waits for its art."""
    yield _kich(monkeypatch, "cho_hinh")
    catalog.equipment.cache_clear()


def without_art(tmp: Path, kind: str) -> Path:
    """A copy of the v2 weapon art with one type's art taken out again."""
    real = ROOT / "client" / "assets" / "v2"
    v2 = tmp / "v2_without"
    (v2 / "icons").mkdir(parents=True)
    shutil.copytree(real / "weapons", v2 / "weapons")
    wiring = json.loads((real / "wiring.json").read_text("utf-8"))
    for atlas in {v for k, v in wiring["item_icons"]["by_weapon_type"].items() if not k.startswith("_")}:
        shutil.copy(real / "icons" / f"{atlas}.json", v2 / "icons" / f"{atlas}.json")
    wiring["weapons"].pop(kind, None)
    wiring["item_icons"]["by_weapon_type"].pop(kind, None)
    for f in (v2 / "weapons").glob(f"{kind}_*"):
        f.unlink()
    (v2 / "wiring.json").write_text(json.dumps(wiring), "utf-8")
    return v2


def fake_art(tmp: Path, extra_types: dict[str, str]) -> Path:
    """A copy of the v2 weapon art, plus the art an artist would add for `extra_types`
    ({type: clip}): a wiring entry, an atlas with an icon per grade and an in-hand layer per
    grade (empty files: the check only asks that they exist)."""
    real = ROOT / "client" / "assets" / "v2"
    v2 = tmp / "v2"
    (v2 / "icons").mkdir(parents=True)
    shutil.copytree(real / "weapons", v2 / "weapons")
    wiring = json.loads((real / "wiring.json").read_text("utf-8"))
    for atlas in {v for k, v in wiring["item_icons"]["by_weapon_type"].items() if not k.startswith("_")}:
        shutil.copy(real / "icons" / f"{atlas}.json", v2 / "icons" / f"{atlas}.json")
    icons = {}
    for kind, clip in extra_types.items():
        wiring["weapons"][kind] = {"layer": f"{kind}_1", "clip": clip}
        wiring["item_icons"]["by_weapon_type"][kind] = "ky_binh_a"
        for g in weapons.data()["grades"]:
            icons[f"{kind}_{g}"] = [0, 0]
            (v2 / "weapons" / f"{kind}_{g}.json").write_text("{}", "utf-8")
            (v2 / "weapons" / f"{kind}_{g}.png").write_bytes(b"")
    (v2 / "icons" / "ky_binh_a.json").write_text(json.dumps({"icons": icons}), "utf-8")
    (v2 / "wiring.json").write_text(json.dumps(wiring), "utf-8")
    return v2


def test_today_the_art_check_passes(check_all):
    assert check_all.check_weapons() == []


def test_flipping_the_status_is_the_only_change_needed(kich_live, check_all, tmp_path):
    # the rules take Kích in: it is equipment, the elites and the boss of Kiếm Trủng Sơn drop it...
    assert weapons.validate() == []
    assert "kich_1" in catalog.equipment()["items"] and "kich_1" in weapons.droppable_weapons()
    assert weapons.fight_profile("kich_1")["clip"] == "slash"
    grants, _ = rolls(ELITE, 300, mult=FORCED)
    got = Counter(weapons.split(g["weapon"])[0] for gs in grants for g in gs)
    assert got["kich"] > 0 and set(got) == {"kiem", "kich"}
    grants, _ = rolls(NORMAL, 300, mult=FORCED)
    assert all(not g["weapon"].startswith("kich_") for gs in grants for g in gs), "never from a normal"
    # ...and with natural odds it is rarer than the land's main type
    grants, _ = rolls(ELITE, 6000)
    got = Counter(weapons.split(g["weapon"])[0] for gs in grants for g in gs)
    assert 0 < got["kich"] < got["kiem"]
    # the art check demands its art: it passes with the artist's files, and names Kích without them
    assert check_all.check_weapons() == []
    missing = check_all.check_weapons(without_art(tmp_path, "kich"))
    assert missing and all("kich" in m for m in missing)
    assert check_all.check_weapons(fake_art(tmp_path, {"kich": "slash"})) == []
