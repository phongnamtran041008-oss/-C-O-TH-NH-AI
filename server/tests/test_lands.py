"""Thiên Địa Đồ: the lands of Luyện Khí (the `lands` section of data/math/world_plan.json,
wired through `wired_sections`, realtime/lands.py).

* the doors: a land opens at a stage of Đạo Thụ with some nodes done; the world refuses
  anyone short of it, through a portal and on a reconnect, with a Vietnamese reason that
  names what is missing;
* the creatures: every land spawns its own, and a fight there asks the math of its branch -
  for the lands of exercises (Lập Trình, Thực Chiến) the math those exercises reinforce;
* the boss: Thiên Kiếp Lôi Long asks the four math branches in turn, its shield breaks only on
  a Phản Đòn, and winning is recorded (the codex) and rewarded within the loot rules.
"""
from collections import deque

import pytest
import pytest_asyncio
from sqlalchemy import select

from app import db as dbm
from app.learning import math_tree
from app.models import CodexEntry
from app.realtime import combat, lands, maps
from app.realtime import world as wmod
from app.realtime.world import Session, World, zone_defs
from app.systems import catalog, math_tree_progress
from tests.test_combat import FakeMono, fighter, last, settle
from tests.test_combat_on_hit import answer, provoke, rest, take_blow

HUB = "truc_lam_thon"
TILE = 16
SUBJECT = {"ds": "dai_so_tuyen_tinh", "gt": "giai_tich", "xs": "xac_suat_thong_ke", "tr": "toi_uu_roi_rac"}


def plan_lands() -> dict:
    return {l["id"]: l for l in math_tree.world_plan()["lands"]}


def built() -> list[dict]:
    return [l for l in plan_lands().values() if l["status"] == "co" and l["kind"] != "hub"]


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def bare_session(w: World, uid: int, tree: lands.TreePos | None) -> Session:
    s = Session(uid, f"user{uid}", f"Đạo Hữu {uid}", "luyen_khi", {"hair_color": "#2B2B2B"})
    s.sent = []
    s.tree = tree
    w.sessions[uid] = s
    return s


def at_gate(w: World, s: Session, zone: str):
    """The player standing inside the hub's gate to `zone`."""
    hub = maps.load(zone_defs()[HUB]["map"])
    portal = next(a for a in hub.portals if a.props.get("target") == zone)
    x, y = portal.x + portal.w / 2, min(portal.y + portal.h / 2, hub.height_px - 1)
    assert w._place(s, HUB, x, y, "down")
    return s.player


def pos(stage: int, *nodes: str, realm: str = "luyen_khi") -> lands.TreePos:
    return lands.TreePos(realm, stage, frozenset(nodes))


# ------------------------------------------------------------------ the data
def test_every_built_land_is_a_zone_with_a_map_and_a_gate_from_the_hub():
    hub = maps.load(zone_defs()[HUB]["map"])
    targets = {a.props.get("target") for a in hub.portals}
    for l in built():
        zid = lands.zone_of(l["id"])
        assert zid is not None and zone_defs()[zid]["map"] == l["map"], l["id"]
        assert lands.zone_land_id(zid) == l["id"]
        assert zid in targets, f"no gate from the hub to {l['id']}"
        zmap = maps.load(l["map"])
        back = [a for a in zmap.portals if a.props.get("target") == HUB]
        assert back and back[0].props.get("target_spawn") in hub.spawns, l["id"]
        assert "from_village" in zmap.spawns
    assert plan_lands()["van_hai_thien_dao"]["status"] == "chua_co" and lands.zone_of("van_hai_thien_dao") is None


def _reachable(zmap, start) -> set:
    W, H = zmap.width_px // TILE, zmap.height_px // TILE

    def ok(x, y):
        return not zmap.collider.blocked(x * TILE + 8, y * TILE + 12)
    first = (int(start[0] // TILE), int(start[1] // TILE))
    seen, q = {first}, deque([first])
    while q:
        x, y = q.popleft()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and ok(*n):
                seen.add(n)
                q.append(n)
    return seen


def test_every_gate_and_every_weapon_spot_can_be_walked_to():
    """From where a player arrives: the gate home, and every weapon spot that needs no ability
    (the ones behind a chasm or in the clouds wait for Đạp Kiếm Lướt and must NOT be)."""
    hub = maps.load(zone_defs()[HUB]["map"])
    seen = _reachable(hub, hub.spawn("from_abode"))
    for a in hub.portals:
        cx, cy = int((a.x + a.w / 2) // TILE), int(min(a.y + a.h / 2, hub.height_px - 1) // TILE)
        assert any((cx + dx, cy + dy) in seen for dx in (-1, 0, 1) for dy in (-1, 0, 1)), a.name
    spots = math_tree.world_plan()["weapons_placed"]
    for l in built():
        zmap = maps.load(l["map"])
        seen = _reachable(zmap, zmap.spawn("from_village"))
        for p in (p for p in spots if p["land"] == l["id"]):
            assert tuple(p["pos"]) in seen or p.get("needs"), (p["weapon"], p["quality"])
            if p.get("needs"):
                assert tuple(p["pos"]) not in seen, f"{p['weapon']} {p['quality']} needs {p['needs']}"


# ------------------------------------------------------------------ the doors
def test_a_newcomer_walks_into_the_open_lands_and_is_refused_from_the_others(gw):
    s = bare_session(gw, 1, lands.TreePos.newcomer())
    for l in built():
        zid = lands.zone_of(l["id"])
        s.sent.clear()
        at_gate(gw, s, zid)
        opens = l["opens"]
        ok = gw.join(s, zid, "portal")
        if not opens["stage"] and not opens["nodes"]:
            assert ok and s.player.channel.zone_id == zid, l["id"]
            assert last(s, "zone")["land"] == l["id"]
        else:
            assert not ok and s.player.channel.zone_id == HUB, l["id"]
            err = last(s, "error")
            assert err["code"] == "land_locked" and err["land"] == l["id"]
            assert err["message_vi"].startswith(f"Chưa vào được {l['name_vi']}")


def test_the_reason_names_the_stage_and_the_nodes_still_missing():
    t = math_tree.tree()
    lx = plan_lands()["linh_xa_nguyen"]
    why = lands.refusal_vi(lx, pos(1, "lt_cau_truc_du_lieu"))
    assert "tầng 2" in why and "đang ở tầng 1" in why
    assert t.nodes["ds_vecto_ma_tran"].name_vi in why and t.nodes["lt_cau_truc_du_lieu"].name_vi not in why
    why = lands.refusal_vi(lx, pos(2))                                         # the stage, not the nodes
    assert "cần tu vi" not in why and t.nodes["lt_cau_truc_du_lieu"].name_vi in why
    assert lands.refusal_vi(lx, pos(2, "lt_cau_truc_du_lieu", "ds_vecto_ma_tran")) is None
    boss = plan_lands()["loi_kiep_dai"]
    why = lands.refusal_vi(boss, pos(8, "du_an_luyen_khi"))
    assert "Lôi Kiếp Đài" in why and "tầng 9" in why
    assert lands.refusal_vi(boss, pos(9, "du_an_luyen_khi")) is None
    assert lands.refusal_vi(boss, pos(0, realm="truc_co")) is not None     # a later realm, node not done
    assert lands.refusal_vi(boss, pos(0, "du_an_luyen_khi", realm="truc_co")) is None
    for text in (lands.refusal_vi(l, None) for l in built()):
        assert text is None or text.endswith(".")


@pytest.mark.parametrize("land_id, tree", [
    ("thien_cong_phuong", pos(1, "lt_python_co_ban")),
    ("linh_xa_nguyen", pos(2, "lt_cau_truc_du_lieu", "ds_vecto_ma_tran")),
    ("loi_kiep_dai", pos(9, "du_an_luyen_khi")),
])
def test_a_player_far_enough_in_the_tree_walks_in(gw, land_id, tree):
    s = bare_session(gw, 2, tree)
    zid = lands.zone_of(land_id)
    at_gate(gw, s, zid)
    assert gw.join(s, zid, "portal") and s.player.channel.zone_id == zid
    assert last(s, "error") is None


def test_the_door_holds_on_a_reconnect_too(gw):
    s = bare_session(gw, 3, pos(9, "du_an_luyen_khi"))
    zid = lands.zone_of("loi_kiep_dai")
    at_gate(gw, s, zid)
    assert gw.join(s, zid, "portal")
    gw._leave_world(s.player)
    s2 = bare_session(gw, 3, lands.TreePos.newcomer())            # a stale save, say, or a reset tree
    s2.saved_zone, s2.saved_pos = zid, (300.0, 400.0, "down")
    assert not gw.join(s2, zid, "resume")
    err = last(s2, "error")
    assert err["code"] == "land_locked" and err["zone"] == "abode"


def test_the_hub_and_open_lands_ignore_the_tree(gw):
    s = bare_session(gw, 4, None)                                  # no tree read at all
    assert gw.join(s, HUB, "abode")
    for l in built():
        if not l["opens"]["stage"] and not l["opens"]["nodes"]:
            assert lands.refusal(lands.zone_of(l["id"]), None) is None
    assert lands.refusal(HUB, None) is None and not lands.gated("bi_canh")


async def test_a_portal_join_reads_the_tree_from_the_database(client, gw):
    """The door is decided on the player's real place in Đạo Thụ, read again before the walk."""
    h, uid, s = await fighter(client, gw, "cua_1", "Cửa Một")
    assert s.tree is not None and (s.tree.realm, s.tree.stage) == ("luyen_khi", 0)
    s.tree = pos(9, "du_an_luyen_khi")                            # a stale, too generous copy
    zid = lands.zone_of("loi_kiep_dai")
    at_gate(gw, s, zid)
    await gw.handle(s, {"t": "join", "zone": zid, "via": "portal"})
    err = last(s, "error")
    assert err is not None and err["code"] == "land_locked", s.sent[-3:]
    assert s.player.channel.zone_id == HUB and s.tree.stage == 0
    async with dbm.SessionLocal() as db:
        st = await math_tree_progress.state(db, uid)
    assert lands.view(lands.pos_of(st))[0]["open"]                    # the hub


def test_the_lands_view_tells_what_is_open():
    rows = {r["id"]: r for r in lands.view(lands.TreePos.newcomer())}
    assert rows["luu_van_coc"]["open"] and rows["luu_van_coc"]["zone"] == "luu_van_coc"
    assert rows["kiem_trung_son"]["zone"] == "loan_so_coc" and rows["kiem_trung_son"]["open"]
    assert not rows["thien_cong_phuong"]["open"] and rows["thien_cong_phuong"]["reason_vi"]
    assert not rows["van_hai_thien_dao"]["built"] and rows["van_hai_thien_dao"]["reason_vi"] is None


# ------------------------------------------------------------------ the creatures
def test_every_land_spawns_its_own_creatures():
    mons = catalog.monsters()
    for l in built():
        zid = lands.zone_of(l["id"])
        w = World(mono=FakeMono())
        ch = w._channels(zid)[0]
        kinds = {m.kind for m in ch.monsters}
        assert set(l["monsters"]) <= kinds, l["id"]
        for k in kinds:
            if mons[k].get("land"):
                assert mons[k]["land"] == l["id"], (l["id"], k)
        assert isinstance(ch.question_source, lands.LandAsker) and ch.question_source.land["id"] == l["id"]
    assert not hasattr(World(mono=FakeMono())._channels(HUB)[0], "question_source")


def stand_on(w: World, s, zone: str, kind: str):
    assert w.join(s, HUB, "abode")
    ch = w._pick_channel(zone)
    m0 = next(m for m in ch.monsters if m.kind == kind)
    w._place(s, zone, m0.x, m0.y, "down")
    for m in ch.monsters:
        if m is not m0:
            m.mode, m.respawn_at = "dead", 1e12
    m0.max_hp = m0.hp = 100000.0
    s.player.max_hp = s.player.hp = 100000.0
    return s.player, m0


@pytest.mark.parametrize("zone, kind", [
    ("luu_van_coc", "van_xa"), ("loan_so_coc", "kiem_linh"), ("ho_nghien_muc", "dau_tu_oa"),
    ("rung_muc_loang", "tri_chu_tinh"),
])
async def test_a_fight_in_a_land_asks_the_math_of_its_branch(client, gw, zone, kind):
    h, uid, s = await fighter(client, gw, f"nhanh_{kind}", "Nhánh " + kind.split("_")[0])
    p, m = stand_on(gw, s, zone, kind)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q is not None, last(s, "error")
    info = catalog.monsters()[kind]
    meta = q["q"]["math"]
    assert meta["subject"] == SUBJECT[info["branch"]]
    t = math_tree.tree()
    assert t.node_of_skill()[meta["skill"]] in info["nodes"]      # a newcomer: a part of its own nodes
    assert meta["land_vi"] == lands.zone_land(zone)["name_vi"]
    res = await answer(client, h, s, True)
    assert res["correct"] and res["combat"]["parry"]


async def test_the_creatures_of_the_exercise_lands_ask_the_math_their_nodes_reinforce(client, gw):
    """Thiên Công Phường and Linh Xạ Nguyên: their nodes are programming exercises, so their
    creatures ask the math nodes those exercises reinforce."""
    t = math_tree.tree()
    # a newcomer has Tập hợp và ánh xạ and Logic open, both reinforced by Lập Trình: asked from its nodes
    h, uid, s = await fighter(client, gw, "bt_co_quan", "Bài Tập Một")
    p, m = stand_on(gw, s, "thien_cong_phuong", "co_quan_nhan")
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q is not None, last(s, "error")
    node = t.node_of_skill()[q["q"]["math"]["skill"]]
    fed = {r for n in t.nodes.values() if n.branch == "lt" for r in n.reinforces}
    assert node in fed and node in m.info["nodes"] and t.nodes[node].branch in SUBJECT
    await answer(client, h, s, False)
    gw._leave_world(p)
    # none of Tâm Ma's nodes is open for a newcomer yet: it asks where they learn in those branches
    h, uid, s = await fighter(client, gw, "bt_tam_ma", "Bài Tập Hai")
    p, m = stand_on(gw, s, "linh_xa_nguyen", "tam_ma")
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q is not None, last(s, "error")
    branches = {t.nodes[n].branch for n in m.info["nodes"]}
    assert q["q"]["math"]["subject"] in {SUBJECT[b] for b in branches}
    async with dbm.SessionLocal() as db:
        st = await math_tree_progress.state(db, uid)
    front = math_tree_progress.frontier_of(st, q["q"]["math"]["subject"])
    assert q["q"]["math"]["skill"] in front.skills


# ------------------------------------------------------------------ the boss
async def test_loi_long_asks_the_four_branches_in_turn(client, gw):
    h, uid, s = await fighter(client, gw, "loi_1", "Lôi Một")
    p, m = stand_on(gw, s, "loi_kiep_dai", "loi_long")
    assert m.info["rank"] == "boss" and m.shield, "a boss wears its shield in the wild"
    subjects = []
    for _ in range(4):
        q = await take_blow(gw, s, p, m)
        assert q is not None, last(s, "error")
        subjects.append(q["q"]["math"]["subject"])
        await answer(client, h, s, False)
        rest(gw)
    assert subjects == [SUBJECT[b] for b in lands.MATH_BRANCHES]


async def test_the_tribulation_is_won_by_parries_and_recorded(client, gw):
    """Its shield breaks only on a Phản Đòn and comes back twice; plain hits do the rest. The win
    is written to the codex and paid out within the loot rules (a newcomer sees the Trúc Cơ Đan
    as locked, never gets it)."""
    h, uid, s = await fighter(client, gw, "loi_2", "Lôi Hai")
    p, m = stand_on(gw, s, "loi_kiep_dai", "loi_long")
    m.max_hp = m.hp = 60.0
    m.regen = sorted(m.info["shield_regen"], reverse=True)
    parries = 0
    for _ in range(40):
        if not m.alive:
            break
        if m.shield:
            hp = m.hp
            await provoke(gw, p, m)
            assert m.hp >= hp - combat.cfg()["shielded_damage"] and m.shield, "a plain hit only scratches it"
            q = await take_blow(gw, s, p, m)
            assert q is not None, last(s, "error")
            res = await answer(client, h, s, True)
            assert res["combat"]["parry"] and res["combat"]["shield_broken"]
            parries += 1
            rest(gw)
        else:
            await provoke(gw, p, m)
    assert not m.alive and parries == 1 + len(m.info["shield_regen"])
    await settle(gw)
    loot = last(s, "loot")
    assert loot is not None and loot["monster"] == "Thiên Kiếp Lôi Long" and loot["stones"] > 0
    assert loot["xp"]["gained"] == m.info["xp"]
    assert any(e["name_vi"] == catalog.item_name("truc_co_dan") for e in loot.get("locked", []))
    assert all(i.get("item_id") != "truc_co_dan" for i in loot["items"])
    async with dbm.SessionLocal() as db:
        e = (await db.execute(select(CodexEntry).where(CodexEntry.user_id == uid, CodexEntry.entry_id == "loi_long"))
             ).scalar_one()
        assert e.progress["kills"] == 1
