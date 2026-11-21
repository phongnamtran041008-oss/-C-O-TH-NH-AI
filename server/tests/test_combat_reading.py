"""A wrong answer leaves time to read (realtime/combat.hold_reading).

After a wrong answer or a timeout on a fight card the card shows the solution, and the fight
stays paused for that player - Hộ Thể, no blow, no new question - until the client sends
`q_read` for that question, at most READ_CAP_SECONDS. A client that does not say it can
(`hello.caps` without "q_read") keeps the old timing. Nobody else is held.

The machinery of test_combat / test_combat_on_hit: a real database and quiz service, a world
on a fake clock ticked by hand.
"""
import pytest
import pytest_asyncio

from app.realtime import combat
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import math_skills
from tests.test_combat import FakeMono, at_monster, fighter, last, run, settle
from tests.test_combat_on_hit import SLIME_MA, VALLEY, answer, plan, provoke, stand_at, take_blow
from tests.test_realm import make_party

CAP = combat.READ_CAP_SECONDS


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


async def reader(client, w, username, display):
    """A fighter whose client reports when the card closes (hello.caps = ["q_read"])."""
    h, uid, s = await fighter(client, w, username, display)
    s.reads_solution = True
    return h, uid, s


async def wrong_blow(client, gw, h, s, p, m) -> dict:
    """A blow lands and is answered wrong: the result of that answer."""
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    assert q is not None
    res = await answer(client, h, s, False)
    assert not res["correct"]
    return res


def sid_of(s) -> str:
    return last(s, "q")["q"]["session_id"]


# ------------------------------------------------------------------ the open world (a blow)
async def test_a_wrong_parry_holds_the_fight_while_the_card_is_read(client, gw):
    h, uid, s = await reader(client, gw, "doc_1", "Đọc Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    res = await wrong_blow(client, gw, h, s, p, m)
    assert res["combat"]["read_cap"] == CAP and res["combat"]["shows_solution"]
    assert p.reading is not None and p.protected(gw.mono())
    hp, struck = p.hp, p.struck_at
    s.sent.clear()
    run(gw, 20.0)                                 # far past the rest window: still reading
    await settle(gw)
    assert p.hp >= hp and p.struck_at == struck, "nothing landed (it only healed out of combat)"
    assert last(s, "q") is None and m.tele is None
    assert p.protected(gw.mono()) and combat.reading(p, gw.mono())
    assert combat.dodge(p, 0, 1, 0, gw.mono()) in ("answering", "locked")
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) == "answering"


async def test_q_read_releases_and_the_rest_window_starts_then(client, gw):
    h, uid, s = await reader(client, gw, "doc_2", "Đọc Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await wrong_blow(client, gw, h, s, p, m)
    sid = sid_of(s)
    run(gw, 12.0)
    await gw.handle(s, {"t": "q_read", "sid": "not-this-one"})
    assert p.reading is not None and p.protected(gw.mono()), "another question's sid releases nothing"
    await gw.handle(s, {"t": "q_read", "sid": sid})
    now = gw.mono()
    assert p.reading is None and not p.protected(now)
    assert p.rest_until == pytest.approx(now + plan()["question_cooldown_seconds"])
    hp = p.hp
    assert await take_blow(gw, s, p, m) is None, "inside the rest window a blow asks nothing"
    assert p.hp < hp, "and it lands (at half damage) again"
    run(gw, plan()["question_cooldown_seconds"] + 0.1)
    assert await take_blow(gw, s, p, m) is not None, "after the rest a blow asks again"


async def test_the_cap_releases_a_card_left_open(client, gw):
    h, uid, s = await reader(client, gw, "doc_3", "Đọc Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await wrong_blow(client, gw, h, s, p, m)
    run(gw, CAP - 1.0)
    assert p.protected(gw.mono()) and p.reading is not None
    run(gw, 1.2)
    now = gw.mono()
    assert p.reading is None and not p.protected(now)
    assert p.rest_until > now, "the rest window follows the cap too"
    run(gw, plan()["question_cooldown_seconds"] + 0.1)
    assert await take_blow(gw, s, p, m) is not None


async def test_a_timeout_holds_like_a_wrong_answer(client, gw, frozen):
    h, uid, s = await reader(client, gw, "doc_4", "Đọc Bốn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    q = await take_blow(gw, s, p, m)
    limit = q["q"]["time_limit"]
    frozen.advance(seconds=limit + 5)
    run(gw, limit + 2)
    await settle(gw)
    assert p.question is None and p.reading is not None and p.reading["sid"] == q["q"]["session_id"]
    assert p.protected(gw.mono())
    await gw.handle(s, {"t": "q_read", "sid": q["q"]["session_id"]})
    assert not p.protected(gw.mono())


async def test_a_right_parry_keeps_todays_timing(client, gw):
    h, uid, s = await reader(client, gw, "doc_5", "Đọc Năm")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await provoke(gw, p, m)
    await take_blow(gw, s, p, m)
    res = await answer(client, h, s, True)
    now = gw.mono()
    assert res["combat"]["parry"] and "read_cap" not in res["combat"]
    assert p.reading is None and not p.protected(now)
    assert p.rest_until == pytest.approx(now + plan()["question_cooldown_seconds"])


async def test_an_old_client_keeps_the_old_timing(client, gw):
    """No "q_read" in hello.caps: nothing would ever release the hold but the cap, which would
    freeze an old client for 45 s after every mistake - so it is not held at all."""
    h, uid, s = await fighter(client, gw, "doc_6", "Đọc Sáu")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    res = await wrong_blow(client, gw, h, s, p, m)
    now = gw.mono()
    assert "read_cap" not in res["combat"] and p.reading is None and not p.protected(now)
    assert p.rest_until == pytest.approx(now + plan()["question_cooldown_seconds"])


async def test_death_drops_the_hold(client, gw):
    h, uid, s = await reader(client, gw, "doc_7", "Đọc Bảy")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    await wrong_blow(client, gw, h, s, p, m)
    assert p.reading is not None
    combat.die(p.channel, p, gw.mono())
    assert p.reading is None and not p.protected(gw.mono())


# ------------------------------------------------------------------ other players
async def test_one_reader_holds_nobody_else_not_even_the_party(client, gw):
    ha, a, sa = await reader(client, gw, "doc_8a", "Đọc Tám")
    hb, b, sb = await reader(client, gw, "doc_8b", "Đọc Chín")
    pa, m = stand_at(gw, sa, VALLEY, SLIME_MA)
    gw.join(sb, "truc_lam_thon", "abode")
    gw._place(sb, VALLEY, m.x + 8, m.y, "down")
    pb = sb.player
    party = await make_party(gw, sa, sb)
    assert party is not None and set(party.members) == {a, b}
    await provoke(gw, pa, m)
    await provoke(gw, pb, m)
    pb.x = m.x + 60                                   # b out of reach: a is hit first
    await take_blow(gw, sa, pa, m)
    await answer(client, ha, sa, False)
    assert pa.reading is not None and pb.reading is None and not pb.protected(gw.mono())
    pb.x, pb.y = m.x + 10, m.y
    sb.sent.clear()
    m.atk_ready = 0.0
    run(gw, combat.windup() + 0.2)
    await settle(gw)
    assert last(sb, "q") is not None, "the monster turned on the mate still fighting"
    assert pa.reading is not None and pb.question is not None
    await gw.handle(sb, {"t": "q_read", "sid": sid_of(sa)})
    assert pa.reading is not None, "a mate cannot release someone else's card"


# ------------------------------------------------------------------ Vấn Đạo (a bí cảnh's rule)
async def test_van_dao_asks_nothing_new_until_the_card_closes(client, gw, monkeypatch):
    monkeypatch.setattr(combat, "on_hit_rule", lambda ch: False)
    h, uid, s = await reader(client, gw, "doc_9", "Đọc Mười")
    p, m = at_monster(gw, s)
    gw.mono.t += 1.0
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) is None
    await settle(gw)
    sid = sid_of(s)
    res = await answer(client, h, s, False)
    assert res["combat"]["mac_kich"] > 0 and res["combat"]["read_cap"] == CAP
    s.sent.clear()
    run(gw, combat.cfg()["next_question_delay"] + 5.0)      # well past the old 3 s
    await settle(gw)
    assert last(s, "q") is None and p.protected(gw.mono())
    gw.mono.t += 1.0
    combat.engage(p.channel, m, p, gw.mono())               # (a monster coming at them asks nothing either)
    await settle(gw)
    assert last(s, "q") is None
    await gw.handle(s, {"t": "q_read", "sid": sid})
    run(gw, combat.READ_GAP_SECONDS - 0.2)
    await settle(gw)
    assert last(s, "q") is None, "a moment to breathe after the card"
    run(gw, 0.5)
    await settle(gw)
    assert last(s, "q") is not None and last(s, "q")["mid"] == m.eid


# ------------------------------------------------------------------ a chiêu that missed
async def test_a_missed_chieu_holds_too(client, gw):
    h, uid, s = await reader(client, gw, "doc_10", "Đọc Mười Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    now = gw.mono()
    p.question = {"sid": "c1", "mid": m.eid, "deadline": now + 10, "asked": now, "limit": 10.0,
                  "timeout_sent": False, "cast": "kiem_quyet", "ch": p.channel.key}
    out = math_skills.resolve(p, "c1", False, None, False)
    assert out["missed"] and out["read_cap"] == CAP and p.reading["kind"] == "cast"
    assert p.protected(gw.mono())
    await gw.handle(s, {"t": "q_read", "sid": "c1"})
    assert p.reading is None and not p.protected(gw.mono())


# ------------------------------------------------------------------ the protocol
def test_hello_caps_and_q_read_parse():
    from app.realtime import protocol
    h = protocol.Hello.model_validate({"t": "hello", "v": 5, "token": "x"})
    assert h.caps == []                                       # an old client
    h = protocol.Hello.model_validate({"t": "hello", "v": 5, "token": "x", "caps": ["q_read"]})
    assert h.caps == ["q_read"]
    msg = protocol.parse({"t": "q_read", "sid": "abc"})
    assert isinstance(msg, protocol.QRead) and msg.sid == "abc"
    with pytest.raises(protocol.BadMessage):
        protocol.parse({"t": "q_read"})
    assert "q_read" in protocol.SERVER_CAPS
