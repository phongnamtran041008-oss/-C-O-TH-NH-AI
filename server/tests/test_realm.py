"""Stage 9 + M10: tổ đội, matchmaking, the schedule and the rifts, bí cảnh instances, the boss
with many phases, loot per player (never twice) and coming back after a lost connection.

Every realm is a math bí cảnh now (test_math_realm.py holds the learning rules: every question
at the answering player's own floor). These tests hold the machinery around it on the two
party realms: Mặc Ảnh Động (opening hours, three Trận Nhãn rooms) and Khe Nứt Mực (a rift in
the wild, one room). Like test_combat, the world runs on a fake clock and its tick is called by
hand; players talk to it with the real protocol messages and answer through the real REST API."""
import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import select

from app import balance, clock
from app import db as dbm
from app.models import Character, EquipmentInstance, InventoryItem, RealmClaim, RealmMember
from app.realtime import maps, realm
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import cultivation, math_realm, secret_realm
from tests.helpers import answer_key, old_script
from tests.realm_bot import Bot, Team, path, right_answer_any
from tests.test_combat import FakeMono, fighter, last, run, settle

SCHEDULED, RIFT = "mac_anh_dong", "khe_nut_muc"


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    monkeypatch.setitem(balance.load("realm"), "always_open", True)
    yield w
    await settle(w)


def gate() -> tuple[float, float]:
    return maps.load("truc_lam_thon").interacts["realm"]


async def hero(client, w, username, display, realm_id="truc_co"):
    """A player standing at the Cổng Bí Cảnh (own math floor 1: a new player)."""
    h, uid, s = await fighter(client, w, username, display)
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, uid)
        ch.realm, ch.realm_stage = realm_id, cultivation.first_stage(realm_id)
        await db.commit()
    s.realm = realm_id
    assert w.join(s, "truc_lam_thon", "abode")
    gx, gy = gate()
    w._place(s, "truc_lam_thon", gx, gy + 14, "up")
    return h, uid, s


def msgs(s, t, event=None):
    return [m for m in s.sent if m.get("t") == t and (event is None or m.get("event") == event)]


async def make_party(w, leader, *others):
    for o in others:
        await w.handle(leader, {"t": "party", "op": "invite", "name": o.name})
        assert last(o, "party")["event"] == "invite"
        await w.handle(o, {"t": "party", "op": "accept", "uid": leader.user_id})
    return w.parties.party_of(leader.user_id)


async def tick(w, seconds: float = 0.05) -> None:
    run(w, seconds)
    await settle(w)


def answerer(client):
    async def answer(bot, q):
        key = await answer_key(q["session_id"])
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"],
                                                    "answer": right_answer_any(q, key)}, headers=bot.h)
        assert r.status_code == 200, r.text
        return r.json()
    return answer


async def answer_right(client, h, q: dict) -> dict:
    key = await answer_key(q["session_id"])
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": right_answer_any(q, key)},
                          headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def play(w, bots, seconds: float, until) -> bool:
    for _ in range(int(seconds / 0.05)):
        for b in bots:
            await b.think()
        await tick(w)
        if until():
            return True
    return False


# ------------------------------------------------------------------ tổ đội
async def test_party_invite_accept_chat_leave(client, gw):
    _, a, sa = await hero(client, gw, "doi_a", "Đội A")
    _, b, sb = await hero(client, gw, "doi_b", "Đội B")
    _, c, sc = await hero(client, gw, "doi_c", "Đội C")
    await gw.handle(sb, {"t": "party", "op": "accept", "uid": a})
    assert last(sb, "error")["code"] == "no_invite"               # nobody asked
    party = await make_party(gw, sa, sb)
    assert party.leader == a and party.members == [a, b]
    st = last(sa, "party")
    assert st["event"] == "state" and [m["name"] for m in st["party"]["members"]] == ["Đội A", "Đội B"]
    assert st["party"]["members"][1]["hp"] == 100                 # party members see each other's health
    await gw.handle(sb, {"t": "party", "op": "invite", "name": "Đội C"})
    assert last(sb, "error")["code"] == "not_leader"
    # the Tổ Đội chat channel reaches the party only
    sc.sent.clear()
    await gw.handle(sa, {"t": "chat", "ch": "party", "text": "vào bí cảnh không?"})
    assert last(sb, "chat")["ch"] == "party" and not msgs(sc, "chat")
    await gw.handle(sc, {"t": "chat", "ch": "party", "text": "?"})
    assert last(sc, "error")["code"] == "no_party"
    # health changes reach the others within a second
    gw.players[b].hp -= 30
    await tick(gw, 1.1)
    assert last(sa, "party")["party"]["members"][1]["hp"] < 100
    # the leader leaves: a party of one is disbanded
    await gw.handle(sa, {"t": "party", "op": "leave"})
    assert last(sa, "party")["event"] == "left" and last(sb, "party")["reason"] == "disbanded"
    assert gw.parties.party_of(b) is None and not gw.parties.parties


async def test_party_full_and_kick(client, gw, monkeypatch):
    monkeypatch.setitem(balance.load("realm"), "party_max", 2)
    _, a, sa = await hero(client, gw, "kick_a", "Kick A")
    _, b, sb = await hero(client, gw, "kick_b", "Kick B")
    _, c, sc = await hero(client, gw, "kick_c", "Kick C")
    await make_party(gw, sa, sb)
    await gw.handle(sa, {"t": "party", "op": "invite", "name": "Kick C"})
    assert last(sa, "error")["code"] == "party_full"
    await gw.handle(sa, {"t": "party", "op": "kick", "uid": b})
    assert last(sb, "party")["reason"] == "kicked" and gw.parties.party_of(a) is None


async def test_party_members_share_xp(client, gw):
    from app.realtime import combat
    _, a, sa = await hero(client, gw, "chia_a", "Chia A")
    _, b, sb = await hero(client, gw, "chia_b", "Chia B")
    await make_party(gw, sa, sb)
    ch = gw._pick_channel("rung_muc_loang")
    m = next(m for m in ch.monsters if m.kind == "ink_slime")
    gw._place(sa, "rung_muc_loang", m.x, m.y, "down")
    gw._place(sb, "rung_muc_loang", m.x + 30, m.y, "down")
    m.engaged = {a}
    combat.kill(ch, m, gw.mono())
    await settle(gw)
    got = last(sb, "party_xp")
    assert got and got["xp"]["gained"] == int(m.info["xp"] * balance.load("realm")["party_xp_share"])


# ------------------------------------------------------------------ the data
def test_every_realm_is_a_sound_math_realm_with_no_word_left():
    """All three realms pass the math bí cảnh's checks (rule 6: no min_realm, rule 7: loot), and
    the old word fields and rooms are gone."""
    assert math_realm.validate() == []
    rs = secret_realm.realms()
    assert {r["kind"] for r in rs.values()} == {"math", "scheduled", "rift"}
    assert set(secret_realm.data()["puzzles"]) == {"seal", "boss"} == set(realm.PUZZLES) | {"boss"}
    for r in rs.values():
        assert not old_script(r) and "tier" not in r and all(x["kind"] == "seal" for x in r["math"]["rooms"])
    assert len(rs[RIFT]["math"]["rooms"]) < len(rs["toan_tran"]["math"]["rooms"]) < len(rs[SCHEDULED]["math"]["rooms"])
    for key in ("compose", "sentence", "tone", "mirror", "maze", "room_loot"):
        assert key not in balance.load("realm")


# ------------------------------------------------------------------ the whole run with three bots
def test_a_bot_can_walk_off_a_stone_it_must_avoid():
    """`path()` has to let a bot leave a place it was told to avoid. A bot that has just stepped on
    a seal stone of the row in the sentence room is standing inside one, and the stones sit
    shoulder to shoulder: if its own cell counts as forbidden the search has no legal first step,
    so the bot stays on that stone for ever and the room never finishes (6 of 200 seeded runs of
    the three-bot realm test once wedged exactly like that)."""
    m = maps.load("bi_canh")
    tiles = [o for o in m.realm_objs
             if o.props.get("room") == "sentence" and o.props.get("kind") == "tile"]
    assert len(tiles) >= 3, len(tiles)
    goal = tiles[0]
    for standing_on in tiles[1:]:
        feet = (standing_on.x + standing_on.w / 2, standing_on.y + standing_on.h / 2 + 7)
        route = path(m.collider, feet, (goal.x + goal.w / 2, goal.y + goal.h / 2),
                     avoid=[t for t in tiles if t is not goal])
        assert route, f"no way off the stone at {feet}"
        # it got out of the stone it stood on, and it did not route through any other
        assert not any(t.x - 2 <= x <= t.x + t.w + 2 and t.y - 2 <= y <= t.y + t.h + 2
                       for x, y in route[2:] for t in tiles if t is not goal and t is not standing_on), route


def stuck_report(gw, inst, bots) -> str:
    """Everything needed to tell apart the ways a room can wedge: the puzzle's state, who holds
    which question and where everyone stands."""
    pz = inst.puzzle
    out = [f"stuck in room {inst.room_i} ({inst.kind} at {inst.place}): {pz.public(gw.mono()) if pz else None}"]
    if pz is not None and hasattr(pz, "asking"):
        out.append(f"  asking = {pz.asking!r} broken = {pz.broken!r}")
    alive = [m for m in inst.monsters if m.alive]
    out.append("  monsters alive = " + repr([(m.eid, round(m.x, 1), round(m.y, 1)) for m in alive]))
    out.append(f"  phase = {inst.phase} mono = {gw.mono():.1f}")
    for b in bots:
        p = b.p
        if p is None:
            out.append(f"  bot {b.uid}: no player")
            continue
        out.append(f"  bot {b.uid}: pos=({p.x:.1f},{p.y:.1f}) dead={p.dead} question={bool(p.question)} "
                   f"goal={b.goal} route_left={len(b.route)}")
    return "\n".join(out)


async def test_three_bots_clear_the_scheduled_realm_together(client, gw):
    """Spec 20, stage 9: three players clear one bí cảnh - Mặc Ảnh Động's three Trận Nhãn rooms
    (pedestals, the row of stones, the pillars) and the boss; each gets their own loot, once."""
    heroes = [await hero(client, gw, f"bot_{i}", f"Đạo Hữu {i}") for i in range(3)]
    (h0, u0, s0), (h1, u1, s1), (h2, u2, s2) = heroes
    for _, uid, _s in heroes:   # sturdy bots, so the test is about the rules, not the luck
        p = gw.players[uid]
        p.max_hp = p.hp = 600
        p.stats["atk"] = 45
    party = await make_party(gw, s0, s1, s2)
    assert len(party.members) == 3
    gw.realms.room_order = None
    await gw.handle(s1, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    assert last(s1, "error")["code"] == "not_leader"
    await gw.handle(s0, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[u0])
    assert inst is not None and inst.rooms == ["seal", "seal", "seal", "boss"]
    assert [r["place"] for r in inst.room_specs] == ["compose", "sentence", "tone", "boss"]
    assert [r.get("seal") for r in inst.room_specs[:3]] == ["pedestal", "tile", "pillar"]
    assert all(gw.realms.instance_of(gw.players[u]) is inst for u in (u1, u2))
    assert last(s0, "zone")["zone"] == "bi_canh"
    team = Team()
    bots = [Bot(gw, client, h, uid, s, team, answerer(client)) for h, uid, s in heroes]
    room = msgs(s0, "realm", "room")[-1]
    assert room["kind"] == "seal" and room["math"] and not old_script(room) and "mine" not in room
    done = await play(gw, bots, 900, lambda: inst.phase == "ended")
    assert done, stuck_report(gw, inst, bots)
    assert inst.result == "won", inst.result
    end = msgs(s0, "realm", "end")[-1]
    assert end["puzzles"] == 3 and end["fragments"] == 0
    # after each move to a new room the others are sent again in full (the client forgets them on `zone`)
    zones = [i for i, m in enumerate(s0.sent) if m.get("t") == "zone" and m.get("zone") == "bi_canh"]
    assert len(zones) == 4
    for i in zones[1:]:
        snap = next(m for m in s0.sent[i:] if m.get("t") == "snap")
        assert {f"p{u1}", f"p{u2}"} <= {e["id"] for e in snap.get("add", [])}
    # the boss's big shield took three different players each phase (spec 14.2)
    gs = [e for m in msgs(s0, "snap") for e in m.get("fx", []) if e.get("k") == "gshield"]
    phases = [gs[i:i + 3] for i in range(0, len(gs), 3)]
    assert len(phases) == 4 and all([e["n"] for e in ph] == [1, 2, 3] and len({e["by"] for e in ph}) == 3
                                    and all(e["need"] == 3 for e in ph) for ph in phases)
    for b in bots:
        b.read()
        assert b.ended and b.ended["result"] == "won"
    await tick(gw, 0.2)
    # loot: every player has their own claims, one per room and one chest, of the realm's materials
    c = balance.load("realm")
    materials = {e["item"] for e in c["chest"][SCHEDULED]["table"]} | {
        e["item"] for e in c["room_loot_by_realm"][SCHEDULED]["items"]}
    async with dbm.SessionLocal() as db:
        for uid in (u0, u1, u2):
            rows = (await db.execute(select(RealmClaim).where(RealmClaim.run_id == inst.run_id,
                                                              RealmClaim.user_id == uid))).scalars().all()
            assert sorted(r.stage for r in rows) == sorted([f"room{i}" for i in range(4)] + ["chest"])
            for r in rows:
                assert {i["item"] for i in r.loot.get("items", [])} <= materials and not r.loot.get("equipment")
            m = await db.get(RealmMember, (inst.run_id, uid))
            assert m.result == "won" and m.left_at is not None
    # asking again pays nothing (spec 14.3: no loot twice)
    for uid in (u0, u1, u2):
        assert await secret_realm.claim_chest(inst.run_id, uid, inst.realm_id, 0, False) is None
        assert await secret_realm.claim_room(inst.run_id, uid, 0, "seal", inst.realm_id) is None
    # each bot was told about its own loot only, and none of it is Tu Vi (that comes from the answers)
    for b in bots:
        b.read()
        assert {lt["stage"] for lt in b.loot} == {f"room{i}" for i in range(4)} | {"chest"}
        assert all("xp" not in lt for lt in b.loot)
    # after the result screen everyone is back at the gate in Trúc Lâm Thôn
    await tick(gw, balance.load("realm")["exit_seconds"] + 0.5)
    assert all(gw.players[u].channel.zone_id == "truc_lam_thon" for u in (u0, u1, u2))
    assert not gw.realms.instances


# ------------------------------------------------------------------ entering
async def enter(gw, leader, *others, realm_id=SCHEDULED, rooms=None):
    await make_party(gw, leader, *others)
    gw.realms.room_order = rooms
    await gw.handle(leader, {"t": "realm", "op": "enter", "realm": realm_id})
    await settle(gw)
    return gw.realms.instance_of(gw.players[leader.user_id])


async def test_entry_rules_party_hours_and_daily_limit(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "luat_a", "Luật A")
    _, b, sb = await hero(client, gw, "luat_b", "Luật B", realm_id="luyen_khi")
    await gw.handle(sa, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    assert last(sa, "error")["code"] == "need_party"                 # 2-5 players
    await make_party(gw, sa, sb)
    await gw.handle(sa, {"t": "realm", "op": "enter", "realm": RIFT})
    assert last(sa, "error")["code"] == "no_realm"                   # rifts are entered at a rift
    # the scheduled realm keeps its hours (spec 14.1)
    monkeypatch.setitem(balance.load("realm"), "always_open", False)
    sa.sent.clear()
    await gw.handle(sa, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    assert last(sa, "error")["code"] == "realm_closed"
    monkeypatch.setitem(balance.load("realm"), "always_open", True)
    # rule 6: nothing reads the cultivation realm - a Luyện Khí member goes in like anyone; two
    # entries a day, the third is refused for everyone in the party
    for _ in range(2):
        gw.realms.room_order = ["boss"]
        await gw.handle(sa, {"t": "realm", "op": "enter", "realm": SCHEDULED})
        await settle(gw)
        assert gw.realms.instance_of(gw.players[a]) is not None, last(sa, "error")
        assert gw.realms.instance_of(gw.players[b]) is not None
        await gw.handle(sa, {"t": "realm", "op": "leave"})
        await gw.handle(sb, {"t": "realm", "op": "leave"})
        await tick(gw)
        assert gw.realms.instance_of(gw.players[a]) is None and gw.players[a].channel.zone_id == "truc_lam_thon"
        gw._place(sa, "truc_lam_thon", *gate(), "up")
        gw._place(sb, "truc_lam_thon", *gate(), "up")
    await gw.handle(sa, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    await settle(gw)
    assert last(sb, "error")["code"] == "daily_limit" and gw.realms.instance_of(gw.players[a]) is None
    async with dbm.SessionLocal() as db:
        assert (await secret_realm.entries_used(db, a))[SCHEDULED] == 2
    clock._clock.advance(days=1)                                     # a new day (UTC+7): entries again
    async with dbm.SessionLocal() as db:
        assert (await secret_realm.entries_used(db, a)).get(SCHEDULED, 0) == 0


async def test_must_stand_at_the_gate(client, gw):
    _, a, sa = await hero(client, gw, "xa_a", "Xa A")
    _, b, sb = await hero(client, gw, "xa_b", "Xa B")
    gw._place(sa, "truc_lam_thon", 100, 300, "up")
    await make_party(gw, sa, sb)
    await gw.handle(sa, {"t": "realm", "op": "enter", "realm": SCHEDULED})
    assert last(sa, "error")["code"] == "too_far"


async def test_matchmaking_queue_forms_a_party(client, gw):
    """Spec 14.1: solo players queue at the gate; a party is made when enough wait (whatever
    their cultivation realms: each is asked at their own floor)."""
    fill = balance.load("realm")["queue"]["fill_seconds"]
    _, a, sa = await hero(client, gw, "cho_a", "Chờ A")
    _, b, sb = await hero(client, gw, "cho_b", "Chờ B", realm_id="luyen_khi")
    gw.realms.room_order = ["boss"]
    await gw.handle(sa, {"t": "realm", "op": "queue", "realm": SCHEDULED})
    assert last(sa, "realm")["event"] == "queued" and last(sa, "realm")["waiting"] == 1
    await tick(gw, 2.0)
    assert gw.realms.queued.get(a) == SCHEDULED                      # alone: still waiting
    await gw.handle(sb, {"t": "realm", "op": "queue", "realm": SCHEDULED})
    assert last(sa, "realm")["waiting"] == 2
    await tick(gw, fill - 3.0)
    assert gw.realms.instance_of(gw.players[a]) is None              # waiting a little for more people
    await tick(gw, 1.5)
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[a])
    assert inst is not None and gw.realms.instance_of(gw.players[b]) is inst
    assert set(gw.parties.party_of(a).members) == {a, b} and not gw.realms.queued


async def test_rift_appears_near_players_and_closes(client, gw):
    """A Khe Nứt Mực leads to the short math realm: one Trận Nhãn room, then the boss."""
    _, a, sa = await hero(client, gw, "nut_a", "Nứt A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "nut_b", "Nứt B", realm_id="luyen_khi")
    ch = gw._pick_channel("rung_muc_loang")
    gw._place(sa, "rung_muc_loang", 300, 330, "down")
    gw._place(sb, "rung_muc_loang", 300, 340, "down")
    r = gw.realms.spawn_rift(ch, gw.mono(), 330, 330)
    assert last(sa, "notice")
    await tick(gw, 0.2)
    snap = [m for m in msgs(sa, "snap") if any(e.get("k") == "r" for e in m.get("add", []))]
    assert snap and next(e for e in snap[-1]["add"] if e["k"] == "r")["realm"] == RIFT
    await make_party(gw, sa, sb)
    gw.players[a].x = 600                                            # far away: cannot step in
    await gw.handle(sa, {"t": "realm", "op": "enter", "rift": r.id})
    assert last(sa, "error")["code"] == "too_far"
    gw.players[a].x = 320
    gw.realms.room_order = None
    await gw.handle(sa, {"t": "realm", "op": "enter", "rift": r.id})
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[a])
    assert inst is not None and inst.realm_id == RIFT and inst.rooms == ["seal", "boss"]
    assert inst.question_source == inst.math_question                 # every question is a math one
    await tick(gw, balance.load("realm")["rift"]["life_seconds"] + 1)   # five minutes later it is gone
    assert r.id not in gw.realms.rifts and r not in ch.extras


async def test_rift_queue_pairs_strangers(client, gw):
    _, a, sa = await hero(client, gw, "la_a", "Lạ A", realm_id="luyen_khi")
    _, b, sb = await hero(client, gw, "la_b", "Lạ B", realm_id="luyen_khi")
    ch = gw._pick_channel("ho_nghien_muc")
    gw._place(sa, "ho_nghien_muc", 820, 300, "down")
    gw._place(sb, "ho_nghien_muc", 830, 300, "down")
    r = gw.realms.spawn_rift(ch, gw.mono(), 825, 310)
    gw.realms.room_order = ["boss"]
    await gw.handle(sa, {"t": "realm", "op": "queue", "rift": r.id})
    await gw.handle(sb, {"t": "realm", "op": "queue", "rift": r.id})
    await tick(gw, balance.load("realm")["queue"]["fill_seconds"] + 1.5)
    await settle(gw)
    inst = gw.realms.instance_of(gw.players[a])
    assert inst is not None and inst.realm_id == RIFT and gw.realms.instance_of(gw.players[b]) is inst


async def test_a_realm_monster_asks_math_not_words(client, gw):
    """The Mặc Quái of a party realm ask through the math bí cảnh's question source."""
    hs = [await hero(client, gw, f"quai_{i}", f"Quái {i}") for i in range(2)]
    inst = await enter(gw, hs[0][2], hs[1][2])
    m = next(m for m in inst.monsters if m.alive)
    p = gw.players[hs[0][1]]
    p.x, p.y = m.x, m.y + 6
    from app.realtime import combat
    combat.engage(inst, m, p, gw.mono())
    await settle(gw)
    q = last(hs[0][2], "q")["q"]
    assert q["context"] == math_realm.CONTEXT and q["math"]["floor"] == 1 and q["math"]["realm_asker"] == "monster"


# ------------------------------------------------------------------ the rooms of a party realm
async def three(client, gw, prefix, rooms, **kw):
    hs = [await hero(client, gw, f"{prefix}_{i}", f"{prefix.title()} {i}", **kw) for i in range(3)]
    inst = await enter(gw, hs[0][2], hs[1][2], hs[2][2], rooms=rooms)
    assert inst is not None
    inst.monsters[:] = [m for m in inst.monsters if m is inst.boss]   # about the room alone (the boss stays)
    return hs, inst


def stand(p, a, dx=0.0, dy=0.0):
    p.x, p.y = a.x + a.w / 2 + dx, a.y + a.h / 2 + dy


def away(inst, ps):
    cx, cy = inst.room_center()
    for i, p in enumerate(ps):
        p.x, p.y = cx - 40 + 40 * i, cy + 80


async def break_seal(client, gw, h, s, p, seal) -> dict:
    """The player steps on a seal, answers its question right and steps off again."""
    stand(p, seal)
    await tick(gw, 0.1)
    q = last(s, "q")
    assert q and q.get("seal") == seal.name, q
    res = await answer_right(client, h, q["q"])
    p.y += 60
    await tick(gw, 0.1)
    return res


async def test_the_pillars_of_the_scheduled_realm_are_seals(client, gw):
    """Mặc Ảnh Động's third room plays Trận Nhãn on the four pillars of the old map."""
    hs, inst = await three(client, gw, "tru", ["seal", "seal", "seal", "boss"])
    inst._start_room(2, gw.mono())
    inst.monsters[:] = []
    pz = inst.puzzle
    pillars = inst.objs("pillar")
    assert inst.place == "tone" and pz.obj_kind == "pillar" and sorted(pz.names) == sorted(o.name for o in pillars)
    ps = [gw.players[u] for _, u, _ in hs]
    away(inst, ps)
    await tick(gw, 0.1)
    assert pz.need() == 4
    for (h, u, s), p, pil in zip(hs, ps, pillars):
        await break_seal(client, gw, h, s, p, pil)
    assert not pz.solved and pz.missing() == []
    res = await break_seal(client, gw, hs[0][0], hs[0][2], ps[0], pillars[3])
    assert res["realm"]["broken"] and pz.solved


# ------------------------------------------------------------------ ghosts, the boss, coming back
async def test_down_in_a_realm_is_a_ghost_until_the_next_room(client, gw):
    from app.realtime import combat
    hs, inst = await three(client, gw, "hon", ["seal", "boss"])
    p = gw.players[hs[1][1]]
    async with dbm.SessionLocal() as db:
        xp_before = (await db.get(Character, p.user_id)).cultivation_xp
    combat.hurt_player(inst, p, p.max_hp * 2, gw.mono())
    await settle(gw)
    assert p.dead and p.ghost and last(hs[1][2], "dead")["ghost"] == 1
    x0 = p.x
    await gw.handle(hs[1][2], {"t": "in", "s": 900, "k": [[0, -1, 50]]})
    await tick(gw, 0.1)
    assert p.y != x0 or p.x != x0                                    # a ghost still follows the party
    await tick(gw, 5)
    assert p.ghost and p.channel is inst                             # no respawn in the village
    async with dbm.SessionLocal() as db:
        assert (await db.get(Character, p.user_id)).cultivation_xp == xp_before   # no Tu Vi lost
    # the room waits only for the living two: base + per_member seals, one each at least
    pz = inst.puzzle
    living = [hs[0], hs[2]]
    assert pz.need() == balance.load("realm")["seal"]["base"] + balance.load("realm")["seal"]["per_member"]
    seals = inst.objs("pedestal")
    away(inst, [gw.players[u] for _, u, _ in living])
    for (h, u, s), seal in zip(living + [living[0]], seals):
        await break_seal(client, gw, h, s, gw.players[u], seal)
    assert pz.solved and inst.phase == "advancing"                   # the living were enough
    await tick(gw, balance.load("realm")["advance_seconds"] + 0.1)
    assert inst.kind == "boss" and not p.ghost and not p.dead and p.hp > 0
    assert any(m.get("event") == "revived" for m in msgs(hs[1][2], "realm"))


async def test_everyone_down_fails_the_run(client, gw):
    from app.realtime import combat
    hs, inst = await three(client, gw, "bai", ["seal", "boss"])
    for _, u, _ in hs:
        p = gw.players[u]
        combat.hurt_player(inst, p, p.max_hp * 2, gw.mono())
    await tick(gw, 0.1)
    assert inst.phase == "ended" and inst.result == "failed"
    await tick(gw, balance.load("realm")["exit_seconds"] + 0.5)
    assert all(gw.players[u].channel.zone_id == "truc_lam_thon" and not gw.players[u].dead for _, u, _ in hs)


async def test_boss_needs_one_right_answer_per_living_member(client, gw):
    from app.realtime import combat
    hs, inst = await three(client, gw, "ma", ["boss"])
    await tick(gw, 3.5)
    b = inst.boss
    assert b is not None and b.shield and b.info["rank"] == "boss"
    extra = balance.load("realm")["boss"]["hp_per_extra_member"] * 2
    mult = secret_realm.realms()[SCHEDULED]["boss_hp_mult"]
    assert round(b.max_hp) == round(b.info["hp"] * mult * (1 + extra))   # grows with the party
    ps = [gw.players[u] for _, u, _ in hs]
    assert all(p.question is not None for p in ps)                   # everyone gets their own question
    for h, u, s in hs[:2]:
        q = last(s, "q")["q"]
        assert q["math"]["realm_asker"] == "boss"
        res = (await answer_right(client, h, q))["combat"]
        assert res["correct"] and not res["shield_broken"]
    assert b.shield and len(b.group_hits) == 2                       # two of three: still up
    combat.hurt_player(inst, ps[2], 10_000, gw.mono(), ignore_protect=True)   # the third falls
    await tick(gw, 0.1)
    assert not b.shield                                              # the two living ones were enough


async def test_reconnect_within_a_minute_keeps_the_place(client, gw):
    hs, inst = await three(client, gw, "rot", ["seal", "seal", "boss"])
    h, u, s = hs[2]
    p = gw.players[u]
    gw.disconnect(s)
    assert p.session is None
    assert p.linger_until - gw.mono() == pytest.approx(balance.load("realm")["reconnect_seconds"])
    await tick(gw, 40)
    assert p.channel is inst and inst.members[u].state == "in"
    s2 = type(s)(u, s.username, s.name, s.realm, s.appearance)
    s2.sent = []
    gw.sessions[u] = s2
    assert gw.join(s2, "bi_canh", "resume")
    kinds = [(m["t"], m.get("event")) for m in s2.sent]
    assert ("zone", None) in kinds and ("realm", "start") in kinds and ("realm", "room") in kinds
    room = msgs(s2, "realm", "room")[-1]
    assert room["kind"] == inst.kind and room["puzzle"]["seals"] and p.session is s2


async def test_gone_too_long_leaves_but_keeps_the_loot(client, gw):
    hs, inst = await three(client, gw, "mat", ["seal", "seal", "boss"])
    ps = [gw.players[u] for _, u, _ in hs]
    seals = inst.objs("pedestal")
    away(inst, ps)
    for (h, u, s), seal in zip(hs + [hs[0]], seals):   # four seals, each of the three breaks one at least
        await break_seal(client, gw, h, s, gw.players[u], seal)
    await settle(gw)
    assert inst.puzzle.solved
    h, u, s = hs[2]
    gw.disconnect(s)
    for _ in range(2 * (balance.load("realm")["reconnect_seconds"] + 1)):
        await tick(gw, 0.5)
        inst.monsters[:] = []      # the two left idle must not die meanwhile (that would end the run)
    assert inst.room_i == 1 and inst.kind == "seal" and inst.phase != "ended"
    await settle(gw)
    await gw.flush_saves()
    assert u not in gw.players and inst.members[u].state == "left"
    async with dbm.SessionLocal() as db:
        assert (await db.get(Character, u)).zone_id == "truc_lam_thon"   # a bí cảnh is never saved as a place
        claims = (await db.execute(select(RealmClaim).where(RealmClaim.user_id == u))).scalars().all()
        assert [c.stage for c in claims] == ["room0"]                # the first room's loot stays theirs
        assert (await db.get(RealmMember, (inst.run_id, u))).result == "disconnected"
    assert any(m.get("event") == "member_left" for m in msgs(hs[0][2], "realm"))


async def test_run_ending_while_someone_is_away_gives_them_the_run_result(client, gw):
    """Someone drops, 40 s later the run fails (finish_run writes "failed" for them too), and their
    60 s reconnect window runs out before the 30 s exit: the first result written stays (left_at IS NULL)."""
    hs, inst = await three(client, gw, "vang", ["seal", "boss"])
    h, u, s = hs[2]
    gw.disconnect(s)
    for _ in range(80):
        await tick(gw, 0.5)
        inst.monsters[:] = []
    inst._finish("failed", gw.mono.t)          # the two still here fell to the boss
    await settle(gw)
    await tick(gw, 25)                          # past the reconnect window, before everyone is sent out
    await gw.flush_saves()
    assert inst.members[u].state == "left"
    async with dbm.SessionLocal() as db:
        assert (await db.get(RealmMember, (inst.run_id, u))).result == "failed"


# ------------------------------------------------------------------ loot
async def test_loot_is_claimed_once_even_when_asked_twice_at_once(client, gw):
    _, a, sa = await hero(client, gw, "kho_a", "Kho A")
    _, b, sb = await hero(client, gw, "kho_b", "Kho B")
    async with dbm.SessionLocal() as db:
        run_id = await secret_realm.create_run(db, RIFT, [a, b])
        await db.commit()
    got = await asyncio.gather(*[secret_realm.claim_chest(run_id, a, RIFT, 0, False) for _ in range(4)])
    assert sum(1 for x in got if x is not None) == 1
    assert await secret_realm.claim_chest(run_id, b, RIFT, 0, False) is not None   # b rolls on their own
    table = {e["item"] for e in balance.load("realm")["chest"][RIFT]["table"]}
    async with dbm.SessionLocal() as db:
        for uid in (a, b):
            held = (await db.execute(select(InventoryItem.item_id).where(InventoryItem.user_id == uid))).scalars().all()
            assert set(held) & table and "manh_bao_vat" not in held
        assert len((await db.execute(select(RealmClaim).where(RealmClaim.run_id == run_id))).scalars().all()) == 2


async def test_fast_clear_pays_more(client, gw, monkeypatch):
    _, a, sa = await hero(client, gw, "nhanh_a", "Nhanh A")
    async with dbm.SessionLocal() as db:
        run_id = await secret_realm.create_run(db, RIFT, [a])
        await db.commit()
    monkeypatch.setitem(balance.load("realm")["chest"][RIFT], "stones", [100, 100])
    fast = await secret_realm.claim_chest(run_id, a, RIFT, 0, True)
    assert fast["stones"] == 100 * balance.load("realm")["fast_bonus"]["stones_mult"] and fast["fast"]


async def test_forge_fragments_into_a_set_piece_with_bonus(client, gw):
    h, a, sa = await hero(client, gw, "ren_a", "Rèn A")
    fc = balance.load("realm")["forge"]
    r = await client.post("/realm/forge", json={"piece": "mac_anh_bao"}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "not_enough"
    async with dbm.SessionLocal() as db:
        from app.systems import inventory
        await inventory.change_item(db, a, "manh_bao_vat", fc["fragments"] * 2, "test")
        await inventory.change_currency(db, a, "spirit_stones", fc["stones"] * 2, "test")
        await db.commit()
    ids = []
    for piece in ("mac_anh_bao", "mac_anh_quan"):
        r = await client.post("/realm/forge", json={"piece": piece}, headers=h)
        assert r.status_code == 200, r.text
        assert r.json()["equipment"]["rarity"] == "thien"
        ids.append(r.json()["equipment"]["id"])
    async with dbm.SessionLocal() as db:
        ch = await db.get(Character, a)
        before = await cultivation.current_stats(db, ch)
        own = 0
        for e in (await db.execute(select(EquipmentInstance).where(EquipmentInstance.id.in_(ids)))).scalars():
            e.equipped_slot = {"mac_anh_bao": "body", "mac_anh_quan": "hat"}[e.item_id]
            own += cultivation.instance_stats(e).get("ink_res", 0)
        await db.commit()
        after = await cultivation.current_stats(db, ch)
    set_bonus = cultivation.catalog.equipment()["sets"]["mac_anh"]["bonus"]["2"]["ink_res"]
    assert after["ink_res"] - before["ink_res"] == own + set_bonus    # Bộ Mặc Ảnh, 2 pieces


async def test_gate_view(client, gw):
    h, a, sa = await hero(client, gw, "cong_a", "Cổng A")
    v = (await client.get("/realms", headers=h)).json()
    ids = {r["id"]: r for r in v["realms"]}
    assert set(ids) == {SCHEDULED, RIFT} and {r["id"] for r in v["math_realms"]} == {"toan_tran"}
    sch, rift = ids[SCHEDULED], ids[RIFT]
    assert sch["entries_left"] == 2 and sch["open"] is True and sch["puzzles"] == 3 and sch["party_min"] == 2
    assert rift["kind"] == "rift" and rift["open"] is None and rift["puzzles"] == 1
    for r in v["realms"] + v["math_realms"]:
        assert r["math"] and r["floor"] == 1 and r["realm_ok"] and not old_script(r) and "min_realm" not in r
        assert r["rooms"] and all(name == "Trận Nhãn" for name in r["rooms"])
    assert v["party"] is None and v["forge"]["fragments"] > 0
    assert set(v["puzzles"]) == {"seal", "boss"} and not old_script(v["puzzles"])


def test_schedule_window(monkeypatch):
    import datetime as dt
    c = balance.load("realm")
    monkeypatch.setitem(c, "always_open", False)
    h = c["schedule"]["hours_local"][0]
    at = dt.datetime(2026, 3, 1, h, 5) - clock.VN_OFFSET            # five minutes after it opened
    st = realm.window_status(at)
    assert st["open"] and st["closes_in"] == (c["schedule"]["open_minutes"] - 5) * 60
    st = realm.window_status(at - dt.timedelta(minutes=15))
    assert not st["open"] and st["opens_in"] == 10 * 60
