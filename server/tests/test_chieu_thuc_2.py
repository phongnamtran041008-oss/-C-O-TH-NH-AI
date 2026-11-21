"""Chiêu Thức II: eleven chiêu earned on Đạo Thụ, the new effect kinds (line, chain, cone, root,
shield, heal, domain, a burning strip), the unlock by nodes and branch shares, and the Công
Pháp loadout of six slots.

The machinery of test_combat / test_math_skills: a real database and quiz service, a world on
a fake clock ticked by hand. The open-world tests cast freely (no question); the bí cảnh test
pins the question rule like test_math_skills does.
"""
import copy
import json
import types

import pytest
import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.models import AchievementCounter
from app.realtime import combat
from app.realtime.maps import Area
from app.realtime import world as wmod
from app.realtime.party import Party
from app.realtime.world import World
from app.systems import math_skills, math_tree_progress
from tests.test_combat import FakeMono, fighter, last, run, settle
from tests.test_combat_on_hit import VALLEY, SLIME_MA, ELITE_MA, stand_at
from tests.test_math_skills import answer, clear_first_floors, clear_floor

NEW = ("ngu_kiem_thuat", "bang_phong_thuat", "chuong_tam_loi", "phong_nhan_thuat", "kim_chung_trao",
       "hoi_xuan_thuat", "dia_liet_tram", "thanh_dang_trien", "hoa_long_thuat", "van_kiem_quy_tong", "kiem_vuc")


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


@pytest.fixture
def learned(monkeypatch):
    """Every chiêu learned and slotted: the effect tests are about the fight, not the tree."""
    async def ok(db, uid, k):
        return None, None
    monkeypatch.setattr(math_skills, "cast_check", ok)


def prepare(p, qi: float = 500.0) -> None:
    p.stats = {"atk": 10, "def": 0, "crit": 0}
    p.max_qi = p.qi = qi


def others(p, n: int) -> list:
    """`n` more monsters of the channel, alive, tough and standing still."""
    ch = p.channel
    out = []
    for o in ch.monsters:
        if len(out) == n:
            break
        if o.alive:
            continue
        o.reset()
        o.respawn_at = 0.0
        o.max_hp = o.hp = 100000.0
        out.append(o)
    assert len(out) == n
    return out


def put(o, x: float, y: float) -> None:
    """Stand a monster at (x, y), its home (the middle of its area) moved there with it: a monster
    put further than `leash_radius` from its own area's middle would give up a fight, run home
    and heal (on the giant maps an area's middle can lie far from where a test stands)."""
    a = o.area
    o.area = Area(a.name, x - a.w / 2, y - a.h / 2, a.w, a.h, a.props)
    o.x, o.y, o.mode, o.target = x, y, "wander", None


async def free_cast(gw, s, k: str, eid):
    s.sent.clear()
    gw.mono.t += 0.05
    assert math_skills.request(s.player, k, eid, gw.mono()) is None
    await settle(gw)
    return last(s, "mcast")


def hit_of(p, k: str, o, power: float | None = None) -> float:
    sk = math_skills.skills()[k]
    if power is not None:
        sk = {**sk, "power": power}
    return math_skills.damage(combat.base_damage(p, o), sk, 0, False, p)


def mskill_events(p) -> list[dict]:
    return [e for e in p.channel.events if e.get("k") == "mskill"]


# ------------------------------------------------------------------ the data
def test_the_eleven_are_there_with_their_effects_and_art_ids():
    sk = math_skills.skills()
    assert list(sk)[6:] == list(NEW)
    want = {"ngu_kiem_thuat": ("line", "ngu_kiem", "kim"), "van_kiem_quy_tong": ("area", "van_kiem", "kim"),
            "bang_phong_thuat": ("area", "bang_phong", "thuy"), "chuong_tam_loi": ("chain", "loi_xich", "loi"),
            "hoa_long_thuat": ("line", "hoa_long", "hoa"), "dia_liet_tram": ("line", "dia_liet", "tho"),
            "thanh_dang_trien": ("root", "thanh_dang", "moc"), "phong_nhan_thuat": ("cone", "phong_nhan", "moc"),
            "kim_chung_trao": ("shield", "kim_chung", "kim"), "kiem_vuc": ("domain", "kiem_vuc", "kim"),
            "hoi_xuan_thuat": ("heal", "hoi_xuan", "moc")}
    for k, (effect, fx, el) in want.items():
        assert (sk[k]["effect"], sk[k]["fx"], sk[k]["element"]) == (effect, fx, el), k
    assert "burn" in sk["hoa_long_thuat"]


def test_the_two_tuyet_ky_are_costly_and_rare():
    sk = math_skills.skills()
    tl = sk["thien_loi_tuyet_ky"]
    for k in ("van_kiem_quy_tong", "kiem_vuc"):
        s = sk[k]
        assert s["kind_vi"] == "Tuyệt kỹ"
        assert s["qi"] >= tl["qi"] and s["cooldown"] >= tl["cooldown"], k
        assert all(s["qi"] > o["qi"] and s["cooldown"] > o["cooldown"]
                   for o in sk.values() if o["kind_vi"] != "Tuyệt kỹ"), k
        assert s["unlock"]["floor"] >= 7


def test_every_new_chieu_is_earned_on_dao_thu_spread_over_luyen_khi_2_to_9():
    t = math_skills.math_tree.tree()
    floors = set()
    for k in NEW:
        u = math_skills.skills()[k]["unlock"]
        assert u.get("nodes"), k
        assert 2 <= u["floor"] <= 9
        floors.add(u["floor"])
        for n in u["nodes"]:
            node = t.nodes[n]
            assert node.content == "co" and node.branch not in ("ml", "dl") and node.realm == "luyen_khi"
            assert node.stage <= u["floor"]
    assert floors >= {2, 3, 4, 5, 6, 7, 9}
    # the old six keep their floors only
    for k in list(math_skills.skills())[:6]:
        assert set(math_skills.skills()[k]["unlock"]) == {"floor"}


def test_validate_catches_broken_new_effects_and_unreachable_requirements():
    raw = json.loads(math_skills.SKILLS_FILE.read_text("utf-8"))

    def broken(edit) -> list[str]:
        r = copy.deepcopy(raw)
        edit(r["skills"])
        return math_skills.validate(r)

    assert math_skills.validate(raw) == []
    assert any("width" in e for e in broken(lambda s: s["ngu_kiem_thuat"].pop("width")))
    assert any("whole number" in e for e in broken(lambda s: s["chuong_tam_loi"].update(hops=2.5)))
    assert any("falloff" in e for e in broken(lambda s: s["chuong_tam_loi"].update(falloff=1.5)))
    assert any("angle" in e for e in broken(lambda s: s["phong_nhan_thuat"].update(angle=0)))
    assert any("duration" in e for e in broken(lambda s: s["thanh_dang_trien"].pop("duration")))
    assert any("power must be 0" in e for e in broken(lambda s: s["kim_chung_trao"].update(power=1)))
    assert any("every" in e for e in broken(lambda s: s["kiem_vuc"].update(every=0.01)))
    assert any("burn means nothing" in e for e in broken(lambda s: s["bang_phong_thuat"].update(
        burn={"power": 0.3, "every": 0.5, "duration": 2})))
    assert any("burn.power" in e for e in broken(lambda s: s["hoa_long_thuat"]["burn"].update(power=0)))
    assert any("mean nothing" in e for e in broken(lambda s: s["ngu_kiem_thuat"].update(hops=2)))
    assert any("not in Đạo Thụ" in e for e in broken(lambda s: s["ngu_kiem_thuat"]["unlock"].update(nodes=["khong_co"])))
    assert any("no content" in e for e in broken(lambda s: s["ngu_kiem_thuat"]["unlock"].update(
        nodes=["tc_du_lieu"], floor=3)))
    assert any("below the stage" in e for e in broken(lambda s: s["kiem_vuc"]["unlock"].update(floor=2)))
    assert any("does not have" in e for e in broken(lambda s: s["van_kiem_quy_tong"]["unlock"].update(
        share={"branch": "dl", "at_least": 0.5})))
    assert any("at_least" in e for e in broken(lambda s: s["van_kiem_quy_tong"]["unlock"]["share"].update(at_least=0)))
    assert any("unlock" in e for e in broken(lambda s: s["ngu_kiem_thuat"]["unlock"].update(realm="truc_co")))


# ------------------------------------------------------------------ earned by learning
def fake_state(done: set[str]):
    t = math_skills.math_tree.tree()
    status = {n: (math_tree_progress.DONE if n in done else math_tree_progress.OPEN) for n in t.nodes}
    return types.SimpleNamespace(tree=t, status=status, done=set(done))


def test_the_requirement_names_what_is_missing():
    sk = math_skills.skills()
    where = ("luyen_khi", 9)
    st = fake_state(set())
    miss = math_skills.missing_parts(sk["ngu_kiem_thuat"], where, st)
    assert miss == {"floor": None, "nodes": ["ds_vecto_ma_tran"], "share": None}
    text = math_skills.locked_reason(sk["ngu_kiem_thuat"], where, st)
    assert text.startswith("Còn thiếu nút: Vectơ và ma trận")
    assert math_skills.locked_reason(sk["ngu_kiem_thuat"], where, fake_state({"ds_vecto_ma_tran"})) is None
    # the floor still counts: the node alone does not open it below its stage
    low = math_skills.locked_reason(sk["ngu_kiem_thuat"], ("luyen_khi", 1), fake_state({"ds_vecto_ma_tran"}))
    assert low is not None and "tầng 2" in low
    # a branch share: the nodes alone are not enough
    vk = sk["van_kiem_quy_tong"]
    nodes = set(vk["unlock"]["nodes"])
    st = fake_state(nodes)
    miss = math_skills.missing_parts(vk, where, st)
    assert miss["nodes"] == [] and miss["share"]["branch"] == "ds"
    assert "nhánh Đại Số Tuyến Tính" in math_skills.locked_reason(vk, where, st)
    ds = {n.id for n in st.tree.main_nodes("luyen_khi") if n.branch == "ds"}
    assert math_skills.locked_reason(vk, where, fake_state(nodes | ds)) is None


async def test_the_view_says_what_is_missing_and_announces_a_new_chieu_once(client, gw):
    h, uid, s = await fighter(client, gw, "c2_view", "Chiêu Hai Xem")
    v = (await client.get("/math/skills", headers=h)).json()
    by = {x["id"]: x for x in v["skills"]}
    nk = by["ngu_kiem_thuat"]
    assert not nk["unlocked"] and "Còn thiếu nút: Vectơ và ma trận" in nk["locked_vi"]
    assert nk["unlock"]["nodes"] == [{"id": "ds_vecto_ma_tran", "name_vi": "Vectơ và ma trận", "branch": "ds",
                                      "stage": 2, "done": False}]
    assert v["new"] == [] and v["loadout"] == list(math_skills.skills())[:6]
    await clear_first_floors(uid)
    await clear_floor(uid, 3)                       # Đại Số Tuyến Tính floor 3 holds the node Vectơ và ma trận
    v = (await client.get("/math/skills", headers=h)).json()
    by = {x["id"]: x for x in v["skills"]}
    assert by["ngu_kiem_thuat"]["unlocked"] and by["ngu_kiem_thuat"]["locked_vi"] is None
    assert not by["bang_phong_thuat"]["unlocked"] and "Giới hạn và liên tục" in by["bang_phong_thuat"]["locked_vi"]
    # announced once: the two old chiêu of tầng 2 and the new one its node opened
    assert [n["id"] for n in v["new"]] == ["ngu_hanh_tran", "ho_than_tran", "ngu_kiem_thuat"]
    # it went to the slot of a chiêu not learned yet (Thiên Lôi, floor 7)
    assert "ngu_kiem_thuat" in v["loadout"] and "thien_loi_tuyet_ky" not in v["loadout"]
    again = (await client.get("/math/skills", headers=h)).json()
    assert again["new"] == [] and again["loadout"] == v["loadout"]
    async with dbm.SessionLocal() as db:
        row = (await db.execute(select(AchievementCounter).where(
            AchievementCounter.user_id == uid, AchievementCounter.key == "chieu_learned"))).scalars().first()
    assert row is not None and row.value == sum(1 for x in v["skills"] if x["unlocked"])


async def test_the_tree_card_names_the_chieu_a_node_opens(client, gw):
    h, uid, s = await fighter(client, gw, "c2_tree", "Chiêu Hai Cây")
    v = (await client.get("/math/tree", headers=h)).json()
    by = {n["id"]: n for n in v["nodes"]}
    assert [c["id"] for c in by["ds_vecto_ma_tran"]["chieu"]] == ["ngu_kiem_thuat"]
    assert {c["id"] for c in by["lt_do_thi"]["chieu"]} == {"thanh_dang_trien", "kiem_vuc"}
    assert by["ds_ngon_ngu"]["chieu"] == []


async def test_a_locked_new_chieu_is_refused_in_the_wild(client, gw):
    h, uid, s = await fighter(client, gw, "c2_lock", "Chiêu Hai Khóa")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    msg = await free_cast(gw, s, "ngu_kiem_thuat", m.eid)
    assert msg["code"] == "locked" and "Vectơ và ma trận" in msg["message_vi"] and p.qi == 500.0


# ------------------------------------------------------------------ the loadout
async def test_the_loadout_is_validated_saved_and_casting_needs_a_slot(client, gw):
    h, uid, s = await fighter(client, gw, "c2_bar", "Chiêu Hai Thanh")
    await clear_first_floors(uid)
    await clear_floor(uid, 3)
    base = (await client.get("/math/skills", headers=h)).json()["loadout"]

    async def save(slots):
        return await client.post("/math/skills/loadout", json={"slots": slots}, headers=h)

    r = await save(["thuong_quyen", None, None, None, None])
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_slots", r.text
    r = await save(["thuong_quyen", "thuong_quyen", None, None, None, None])
    assert r.status_code == 400 and r.json()["error"]["code"] == "twice"
    r = await save(["kiem_vuc", None, None, None, None, None])
    assert r.status_code == 400 and r.json()["error"]["code"] == "locked"
    r = await save(["khong_co", None, None, None, None, None])
    assert r.status_code == 400 and r.json()["error"]["code"] == "unknown"
    want = ["ngu_kiem_thuat", "hoa_cau_thuat", None, "kiem_quyet", None, "ho_than_tran"]
    r = await save(want)
    assert r.status_code == 200, r.text
    assert r.json()["loadout"] == want and want != base
    assert (await client.get("/math/skills", headers=h)).json()["loadout"] == want      # stored
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    msg = await free_cast(gw, s, "thuong_quyen", m.eid)                  # learned, but not on the bar
    assert msg["code"] == "not_slotted" and msg["message_vi"] and p.qi == 500.0
    msg = await free_cast(gw, s, "ngu_kiem_thuat", m.eid)
    assert msg["ok"], msg


def test_an_old_or_broken_hotbar_gets_the_old_six():
    six = list(math_skills.skills())[:6]
    assert math_skills.loadout_of({}) == six
    assert math_skills.loadout_of(None) == six
    assert math_skills.loadout_of({"chieu": ["kiem_quyet"]}) == six
    assert math_skills.loadout_of({"chieu": ["gone", "kiem_quyet", None, None, None, None]}) == \
        [None, "kiem_quyet", None, None, None, None]


# ------------------------------------------------------------------ the effects, in the wild
async def test_line_pierces_what_it_covers_up_to_its_count(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_line", "Chiêu Hai Tuyến")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["ngu_kiem_thuat"]
    on1, off, on2, far = others(p, 4)
    x, y = p.x, p.y
    put(m, x + 60, y)
    put(on1, x + 100, y + sk["width"] / 2 - 2)
    put(off, x + 100, y + 40)
    put(on2, x + 140, y)
    put(far, x + sk["range"] + 40, y)
    hp = {o.eid: o.hp for o in (m, on1, off, on2, far)}
    msg = await free_cast(gw, s, "ngu_kiem_thuat", m.eid)
    assert msg["ok"] and msg["result"]["hits"] == 3
    for o in (m, on1, on2):
        assert hp[o.eid] - o.hp == pytest.approx(hit_of(p, "ngu_kiem_thuat", o)), o.eid
    assert off.hp == hp[off.eid] and far.hp == hp[far.eid]
    ev = mskill_events(p)[-1]
    assert [h_[0] for h_ in ev["hits"]] == [m.eid, on1.eid, on2.eid]          # in the order the sword meets them
    assert ev["ex"] == pytest.approx(x + sk["range"], abs=0.1) and ev["w"] == sk["width"]
    # more on the line than it pierces: the nearest `pierce` only
    gw.mono.t += sk["cooldown"]
    extra = others(p, 3)
    for i, o in enumerate(extra):
        put(o, x + 20 + i * 10, y)
    msg = await free_cast(gw, s, "ngu_kiem_thuat", m.eid)
    assert msg["result"]["hits"] == sk["pierce"]
    assert m.eid in [h_[0] for h_ in mskill_events(p)[-1]["hits"]]       # the target always


async def test_chain_hops_at_random_among_the_near_and_falls_off(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_chain", "Chiêu Hai Xích")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["chuong_tam_loi"]
    a, b, lone = others(p, 3)
    x, y = p.x, p.y
    put(m, x + 40, y)
    put(a, x + 40 + sk["hop_range"] - 10, y)
    put(b, x + 40 + 2 * (sk["hop_range"] - 10), y)
    put(lone, x + 40, y + 400)
    hp = {o.eid: o.hp for o in (m, a, b, lone)}
    msg = await free_cast(gw, s, "chuong_tam_loi", m.eid)
    assert msg["ok"] and msg["result"]["hits"] == 3
    f = sk["falloff"]
    for i, o in enumerate((m, a, b)):
        assert hp[o.eid] - o.hp == pytest.approx(hit_of(p, "chuong_tam_loi", o) * f ** i), o.eid
    assert lone.hp == hp[lone.eid]
    assert [h_[0] for h_ in mskill_events(p)[-1]["hits"]] == [m.eid, a.eid, b.eid]
    # never more than `hops` jumps (a and b go far first: the lightning chooses at random, and a
    # hop onto b, out of the crowd's reach, would end the chain early by chance alone)
    gw.mono.t += sk["cooldown"]
    put(a, m.x - 300, m.y)
    put(b, m.x - 300, m.y + 300)
    crowd = others(p, 6)
    for i, o in enumerate(crowd):
        put(o, m.x + 10 + (i % 3) * 8, m.y + (i // 3) * 8)
    msg = await free_cast(gw, s, "chuong_tam_loi", m.eid)
    assert msg["result"]["hits"] == 1 + sk["hops"]


async def test_cone_hits_the_fan_in_front_only(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_cone", "Chiêu Hai Quạt")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["phong_nhan_thuat"]
    side, behind, inside = others(p, 3)
    x, y = p.x, p.y
    put(m, x + 50, y)
    put(inside, x + 70, y + 20)                   # ~16 degrees off the aim: inside a 60 degree fan
    put(side, x + 20, y + 60)                     # ~72 degrees off
    put(behind, x - 50, y)
    hp = {o.eid: o.hp for o in (m, side, behind, inside)}
    msg = await free_cast(gw, s, "phong_nhan_thuat", m.eid)
    assert msg["result"]["hits"] == 2
    assert inside.hp < hp[inside.eid] and m.hp < hp[m.eid]
    assert side.hp == hp[side.eid] and behind.hp == hp[behind.eid]


async def test_root_holds_in_place_but_a_held_monster_still_strikes_within_reach(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_root", "Chiêu Hai Trói")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["thanh_dang_trien"]
    near = others(p, 1)[0]
    x, y = p.x, p.y
    put(m, x + 120, y)
    put(near, x + 120 + sk["radius"] - 5, y)
    msg = await free_cast(gw, s, "thanh_dang_trien", m.eid)
    assert msg["ok"] and msg["result"]["hits"] == 2
    now = gw.mono()
    for o in (m, near):
        assert o.slow_mult == 0.0 and o.slow_until == pytest.approx(now + sk["duration"])
    assert mskill_events(p)[-1]["d"] == sk["duration"]
    mx = m.x
    run(gw, 1.0)                                  # engaged, it would chase the caster: it cannot move
    assert m.x == pytest.approx(mx) and m.mode == "chase"
    # stand inside its reach: it still winds up and lands the blow (and the question comes)
    p.x, p.y = m.x - 10, m.y
    s.sent.clear()
    m.atk_ready = 0.0
    run(gw, combat.windup() + 0.3)
    await settle(gw)
    assert last(s, "q") is not None
    assert m.x == pytest.approx(mx)


async def test_root_holds_an_elite_for_less(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_root_e", "Chiêu Hai Tinh")
    p, m = stand_at(gw, s, VALLEY, ELITE_MA)
    prepare(p)
    sk = math_skills.skills()["thanh_dang_trien"]
    put(m, p.x + 60, p.y)
    await free_cast(gw, s, "thanh_dang_trien", m.eid)
    assert m.slow_until == pytest.approx(gw.mono() + sk["duration"] * math_skills.data()["root_rank_mult"]["elite"])
    assert m.shield                               # a chiêu in the wild never breaks Mặc Thuẫn


async def test_ice_freezes_an_area_long(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_ice", "Chiêu Hai Băng")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["bang_phong_thuat"]
    near = others(p, 1)[0]
    put(m, p.x + 60, p.y)
    put(near, p.x + 60, p.y + sk["radius"] - 5)
    await free_cast(gw, s, "bang_phong_thuat", m.eid)
    for o in (m, near):
        assert o.slow_mult == sk["slow"] and o.slow_until == pytest.approx(gw.mono() + sk["duration"])
    assert sk["slow"] < math_skills.skills()["ngu_hanh_tran"]["slow"]       # a freeze, not a slow


async def test_the_golden_bell_guards_the_caster_alone(client, gw, learned):
    ha, a, sa = await fighter(client, gw, "c2_bell1", "Chiêu Hai Chuông")
    hb, b, sb = await fighter(client, gw, "c2_bell2", "Chiêu Hai Bạn")
    pa, m = stand_at(gw, sa, VALLEY, SLIME_MA)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, VALLEY, pa.x + 10, pa.y, "down")
    gw.parties.parties[78] = Party(78, a, [a, b])
    gw.parties.of[a] = gw.parties.of[b] = 78
    prepare(pa)
    sk = math_skills.skills()["kim_chung_trao"]
    msg = await free_cast(gw, sa, "kim_chung_trao", None)
    assert msg["ok"] and msg["result"]["shield"]["reduce"] == sk["reduce"]
    now = gw.mono()
    assert pa.guard_until == pytest.approx(now + sk["duration"]) and pa.guard_reduce == sk["reduce"]
    assert sb.player.guard_until <= now                     # the bell is for the caster only
    before = pa.hp
    combat.hurt_player(pa.channel, pa, 100, now)
    assert before - pa.hp == pytest.approx(100 * (1 - sk["reduce"]))
    ev = mskill_events(pa)[-1]
    assert ev["fx"] == "kim_chung" and ev["d"] == sk["duration"] and "tx" not in ev


async def test_spring_heals_the_caster_and_the_party_near(client, gw, learned):
    ha, a, sa = await fighter(client, gw, "c2_heal1", "Chiêu Hai Xuân")
    hb, b, sb = await fighter(client, gw, "c2_heal2", "Chiêu Hai Hữu")
    hc, c_, sc = await fighter(client, gw, "c2_heal3", "Chiêu Hai Khách")
    pa, m = stand_at(gw, sa, VALLEY, SLIME_MA)
    for s_ in (sb, sc):
        gw.join(s_, "truc_lam_thon", "abode")
        gw._place(s_, VALLEY, pa.x + 10, pa.y, "down")
    gw.parties.parties[79] = Party(79, a, [a, b])
    gw.parties.of[a] = gw.parties.of[b] = 79
    prepare(pa)
    sk = math_skills.skills()["hoi_xuan_thuat"]
    for pl in (pa, sb.player, sc.player):
        pl.hp = pl.max_hp / 2
    msg = await free_cast(gw, sa, "hoi_xuan_thuat", None)
    assert msg["result"]["heal"]["players"] == 2
    for pl in (pa, sb.player):
        assert pl.hp == pytest.approx(pl.max_hp / 2 + pl.max_hp * sk["heal_pct"] / 100)
    assert sc.player.hp == sc.player.max_hp / 2


async def test_the_dragon_leaves_burning_ground(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_fire", "Chiêu Hai Hỏa")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["hoa_long_thuat"]
    b = sk["burn"]
    put(m, p.x + 80, p.y)
    hp0 = m.hp
    await free_cast(gw, s, "hoa_long_thuat", m.eid)
    first = hp0 - m.hp
    assert first == pytest.approx(hit_of(p, "hoa_long_thuat", m))
    assert mskill_events(p)[-1]["d"] == b["duration"]
    ticks = int(round(b["duration"] / b["every"]))
    run(gw, b["duration"] + 1.0)
    burned = hp0 - m.hp - first
    assert burned == pytest.approx(ticks * hit_of(p, "hoa_long_thuat", m, b["power"]))
    assert not getattr(p.channel, "chieu_zones", [])          # it went out


async def test_the_sword_domain_follows_the_caster_and_ends(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_domain", "Chiêu Hai Vực")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["kiem_vuc"]
    away = others(p, 1)[0]
    put(m, p.x + sk["radius"] - 10, p.y)
    put(away, p.x + 300, p.y)
    hp_m, hp_a = m.hp, away.hp
    msg = await free_cast(gw, s, "kiem_vuc", None)
    assert msg["ok"] and p.qi == pytest.approx(500 - sk["qi"])
    run(gw, 1.1)                                  # ticks at 0, 0.5, 1.0
    per = hit_of(p, "kiem_vuc", m)
    assert hp_m - m.hp == pytest.approx(3 * per)
    assert away.hp == hp_a
    # it follows: step next to the far one, the near one is left behind
    p.x, p.y = away.x - 20, away.y
    hm = m.hp
    run(gw, 1.0)
    assert m.hp == hm and away.hp < hp_a
    ticks = int(round(sk["duration"] / sk["every"]))
    (z,) = p.channel.chieu_zones
    assert ticks - z["left"] == 5                 # 0, 0.5, 1.0, 1.5, 2.0
    run(gw, sk["duration"])
    assert not getattr(p.channel, "chieu_zones", [])
    ha = away.hp
    run(gw, 1.0)
    assert away.hp == ha                          # over


async def test_myriad_swords_rain_on_an_area(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_vk", "Chiêu Hai Vạn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    sk = math_skills.skills()["van_kiem_quy_tong"]
    near, far = others(p, 2)
    put(m, p.x + 120, p.y)
    put(near, p.x + 120, p.y + sk["radius"] - 5)
    put(far, p.x + 120, p.y + sk["radius"] + 30)
    hp = {o.eid: o.hp for o in (m, near, far)}
    msg = await free_cast(gw, s, "van_kiem_quy_tong", m.eid)
    assert msg["ok"] and msg["ready_in"] == sk["cooldown"]
    for o in (m, near):
        assert hp[o.eid] - o.hp == pytest.approx(hit_of(p, "van_kiem_quy_tong", o))
    assert far.hp == hp[far.eid]
    assert p.qi == pytest.approx(500 - sk["qi"])
    gw.mono.t += 10
    assert (await free_cast(gw, s, "van_kiem_quy_tong", m.eid))["code"] == "cooldown"


async def test_the_linh_can_element_bonus_applies_to_a_new_chieu(client, gw, learned):
    h, uid, s = await fighter(client, gw, "c2_lc", "Chiêu Hai Căn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    prepare(p)
    p.stats["lc_fx"] = {"chieu_loi": 0.3, "chieu_kim": 0.0}
    put(m, p.x + 40, p.y)
    hp0 = m.hp
    await free_cast(gw, s, "chuong_tam_loi", m.eid)
    sk = math_skills.skills()["chuong_tam_loi"]
    plain = combat.base_damage(p, m) * sk["power"]
    assert hp0 - m.hp == pytest.approx(plain * 1.3)


# ------------------------------------------------------------------ in a bí cảnh: a question casts it
async def test_a_new_chieu_in_a_bi_canh_is_cast_by_its_question_and_breaks_the_targets_shield(
        client, gw, monkeypatch, learned):
    monkeypatch.setattr(combat, "on_hit_rule", lambda ch: False)
    from tests.test_math_combat import at_math_monster
    h, uid, s = await fighter(client, gw, "c2_bc", "Chiêu Hai Bí")
    p, m = at_math_monster(gw, s)
    prepare(p)
    sk = math_skills.skills()["ngu_kiem_thuat"]
    behind = others(p, 1)[0]
    put(m, p.x + 40, p.y)
    put(behind, p.x + 90, p.y)
    assert m.shield and behind.shield
    s.sent.clear()
    gw.mono.t += 0.05
    await gw.handle(s, {"t": "mskill", "k": "ngu_kiem_thuat", "id": m.eid})
    await settle(gw)
    ok = last(s, "mcast")
    assert ok["ok"] and "free" not in ok
    q = last(s, "q")
    assert q["q"]["qtype"] in sk["qtypes"] and q["cast"]["k"] == "ngu_kiem_thuat"
    hb = behind.hp
    res = await answer(client, h, s, True)
    c = res["combat"]
    assert c["correct"] and c["shield_broken"] and not m.shield and c["hits"] == 2
    assert behind.shield and hb - behind.hp == combat.cfg()["shielded_damage"]     # a scratch only
