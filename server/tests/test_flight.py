"""Ngự kiếm: flying on the sword under one's own keys (world_plan.json unlocks dap_kiem_luot, the low
rung with a gauge, and ngu_kiem_phi_hanh, free flight from Trúc Cơ; realtime/abilities.py, the
geometry in realtime/glide.fly_step). The server decides every airborne step, the gauge, the
landing and the fall back to the ground; in the air nobody fights, and a blow on the ground
misses. The world runs on a fake clock ticked by hand (test_combat's machinery).
"""
import math

import pytest
import pytest_asyncio

from app.learning import math_tree
from app.realtime import abilities, beasts, combat, glide, lands, maps, protocol
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import math_skills, weapons
from tests.test_abilities import KIEM_TRUNG_SON, place, tile_feet, unlock
from tests.test_combat import FakeMono, fighter, last, run, settle
from tests.test_combat_on_hit import SLIME_MA, VALLEY, events, luyen_khi, provoke, stand_at


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def low() -> dict:
    return unlock("dap_kiem_luot")["flight"]


def high() -> dict:
    return unlock("ngu_kiem_phi_hanh")["flight"]


def at(stage: int, realm: str = "luyen_khi") -> lands.TreePos:
    return lands.TreePos(realm, stage, frozenset())


# Kiếm Trủng Sơn: the ledge below the nest, a chasm of ink north of it (read from the plan)
from tests.test_abilities import CHASM, LEDGE  # noqa: E402


def _open() -> tuple[float, float]:
    """Open ground in the south of Kiếm Trủng Sơn: the plaza of the gate camp (its khu anchor)."""
    k = next(a for a in maps.load(KIEM_TRUNG_SON).khu if a.name == "kts_trai_cong")
    return float(k.props["anchor_x"]), float(k.props["anchor_y"])


OPEN = _open()


def take_off(gw: World, p, seq: int) -> None:
    assert abilities.request_fly(p, seq, True, gw.mono()) is None
    run(gw, 0.05)
    assert p.fly


def fly_keys(gw: World, p, seq: int, dx: int, dy: int, ms: int) -> int:
    """Hold a direction for `ms` in the air, sent as the client sends it (200 ms per message)."""
    for i in range(ms // 200):
        p.channel.queue_input(p, seq + i, [(dx, dy, 100), (dx, dy, 100)])
    run(gw, ms / 1000 + 0.2)
    return seq + ms // 200


# ------------------------------------------------------------------ the plan
def test_both_rungs_are_built_and_the_high_one_is_higher_and_faster():
    lo, hi = unlock("dap_kiem_luot"), unlock("ngu_kiem_phi_hanh")
    assert (lo["realm"], lo["stage"], lo["status"]) == ("luyen_khi", 6, "co")
    assert (hi["realm"], hi["stage"], hi["status"]) == ("truc_co", 0, "co")
    assert low()["gauge_seconds"] > 0 and high()["gauge_seconds"] == 0
    assert high()["speed_mult"] > low()["speed_mult"] > 1 and high()["lift_px"] > low()["lift_px"]
    assert "fly" in protocol.MESSAGES
    # what hangs on the high rung stays shut: its land (and so its spots and beast) are not built
    sky = next(l for l in math_tree.world_plan()["lands"] if l["id"] == "van_hai_thien_dao")
    assert sky["status"] == "chua_co" and sky["needs"] == "ngu_kiem_phi_hanh"
    kylan = next(b for b in math_tree.world_plan()["beasts"] if b["id"] == "ky_lan_con")
    assert kylan["status"] == "chua_co" and kylan["needs"] == "ngu_kiem_phi_hanh"
    assert math_tree.validate_world(math_tree.world_plan(), math_tree.tree()) == []


def test_the_cloud_spots_stay_shut_until_their_land_is_built():
    every = set(math_tree.tree().nodes)
    for spot in (p for p in weapons.data()["placed"] if p.get("needs") == "ngu_kiem_phi_hanh"):
        why = weapons.missing(spot, ("truc_co", 9), every)
        assert any("Vân Hải Thiên Đảo" in w and "chưa có" in w for w in why), why


def test_the_sword_follows_the_realm():
    assert [abilities.sword_sheet(r) for r in ("pham_nhan", "luyen_khi", "truc_co", "ket_dan", "nguyen_anh",
                                               "hoa_than", "dai_thua")] == \
        ["phi_kiem_1", "phi_kiem_1", "phi_kiem_1", "phi_kiem_2", "phi_kiem_2", "phi_kiem_3", "phi_kiem_3"]


def test_the_checker_bites_on_the_flight_numbers():
    import copy
    plan = copy.deepcopy(math_tree.world_plan())
    u = next(x for x in plan["unlocks"] if x["id"] == "ngu_kiem_phi_hanh")
    u["flight"]["speed_mult"] = 1.2                     # slower than the low rung
    u["flight"]["gauge_seconds"] = 5                    # free flight with a gauge
    lo = next(x for x in plan["unlocks"] if x["id"] == "dap_kiem_luot")
    lo["flight"]["over_tiles"] = ["lava"]
    errs = math_tree.validate_world(plan, math_tree.tree())
    assert any("speed_mult must be above" in e for e in errs)
    assert any("free flight has no gauge" in e for e in errs)
    assert any("over_tiles" in e for e in errs)


# ------------------------------------------------------------------ the unlock gates
async def test_the_rungs_open_with_the_tree(client, gw):
    h, uid, s = await fighter(client, gw, "fl_1", "Phi Một")
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(*LEDGE))
    s.tree = at(5)
    assert abilities.fly_level(p) == 0
    assert abilities.request_fly(p, 1, True, gw.mono()) == "fly_locked"
    run(gw, 0.1)
    assert not p.fly and p.ack == 1, "a refused take-off still uses up its number"
    s.tree = at(6)
    assert abilities.fly_level(p) == 1
    s.tree = at(0, "truc_co")                           # Ngự Kiếm Phi Hành, monkeypatched there
    assert abilities.fly_level(p) == 2
    v = abilities.view(p, gw.mono())
    assert v["ngu_kiem_phi_hanh"]["ok"] and v["dap_kiem_luot"]["flight"]["level"] == 2
    assert v["dap_kiem_luot"]["flight"]["levels"][2]["lift"] == high()["lift_px"]


async def test_the_world_answers_take_off_and_its_refusal(client, gw):
    h, uid, s = await fighter(client, gw, "fl_2", "Phi Hai")
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(*LEDGE))
    s.tree = at(1)
    await gw.handle(s, {"t": "fly", "s": 1, "on": True})
    r = last(s, "fly")
    assert r["ok"] is False and r["code"] == "fly_locked" and "tầng 6" in r["message_vi"]
    s.tree = at(6)
    s.sent.clear()
    await gw.handle(s, {"t": "fly", "s": 2, "on": True})
    run(gw, 0.1)
    r = last(s, "fly")
    assert r["ok"] is True and r["on"] == 1 and r["why"] == "up"
    ev = events(s, "fly")[-1]
    assert (ev["id"], ev["on"], ev["sw"]) == (p.eid, 1, "phi_kiem_1")


# ------------------------------------------------------------------ flying
async def test_a_flyer_crosses_the_chasm_walking_cannot_and_lands_on_the_far_side(client, gw):
    h, uid, s = await fighter(client, gw, "fl_3", "Phi Ba")
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = at(6)
    z = maps.load(KIEM_TRUNG_SON)
    assert z.tile_name(*CHASM) == "ink" and z.collider.blocked(*tile_feet(*CHASM))
    p.channel.queue_input(p, 1, [(0, -1, 100)] * 10)
    run(gw, 1.2)
    assert p.y > tile_feet(*CHASM)[1] - 4, "on foot the chasm stops it"
    take_off(gw, p, 2)
    seq = fly_keys(gw, p, 3, 0, -1, 400)
    tx, ty = int(p.x // 16), int((p.y - 1) // 16)
    assert ty < CHASM[1] - 1, f"over the chasm and beyond it: tile {tx},{ty}"
    assert glide.land_ok(z.collider, z.tile_name, abilities.fly_over(1), p.x, p.y)
    s.sent.clear()
    assert abilities.request_fly(p, seq, False, gw.mono()) is None
    run(gw, 0.1)
    assert not p.fly and last(s, "fly")["why"] == "land" and events(s, "fly")[-1]["on"] == 0
    spot = weapons.data()["by_id"]["kiem_2_ha"]
    assert math.hypot(spot["pos"][0] * 16 + 8 - p.x, spot["pos"][1] * 16 + 12 - p.y) < 40, "up by the spot"


async def test_a_flyer_moves_at_the_swords_speed_and_no_faster(client, gw):
    h, uid, s = await fighter(client, gw, "fl_4", "Phi Bốn")
    x0, y0 = OPEN                                       # the open plaza in the south of Kiếm Trủng Sơn
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    speed = p.channel.speed
    s.tree = at(6)
    take_off(gw, p, 1)
    x = p.x
    fly_keys(gw, p, 2, 1, 0, 400)
    assert p.x - x == pytest.approx(speed * low()["speed_mult"] * 0.4, abs=0.5)
    # a client that sends faster than real time gains nothing: the budget holds like walking
    x = p.x
    for i in range(12):
        p.channel.queue_input(p, 20 + i, [(1, 0, 100), (1, 0, 100)])
    run(gw, 0.5)
    lag = wmod.cfg()["move_budget_max_ms"] / 1000
    assert p.x - x <= speed * low()["speed_mult"] * (0.5 + lag) + 1


async def test_a_flyer_does_not_pass_walls(client, gw):
    h, uid, s = await fighter(client, gw, "fl_5", "Phi Năm")
    z = maps.load(KIEM_TRUNG_SON)
    over = abilities.fly_over(1)
    x0, y0 = tile_feet(*LEDGE)
    wall = next(tx for tx in range(LEDGE[0] + 1, LEDGE[0] + 5) if z.collider.blocked(*tile_feet(tx, LEDGE[1]))
                and z.tile_name(tx, LEDGE[1]) not in over)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = at(6)
    take_off(gw, p, 1)
    fly_keys(gw, p, 2, 1, 0, 1000)
    assert p.x < wall * 16, "the wall stops a flyer like a walker"
    assert glide.over_ok(z.collider, z.tile_name, over, p.x, p.y)


async def test_no_landing_over_the_chasm(client, gw):
    h, uid, s = await fighter(client, gw, "fl_6", "Phi Sáu")
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(*LEDGE))
    s.tree = at(6)
    take_off(gw, p, 1)
    p.x, p.y = tile_feet(*CHASM)                        # hovering over the ink
    s.sent.clear()
    assert abilities.request_fly(p, 2, False, gw.mono()) is None
    run(gw, 0.1)
    r = last(s, "fly")
    assert r["ok"] is False and r["code"] == "no_landing" and r["message_vi"] and p.fly == 1


async def test_the_gauge_runs_dry_over_the_chasm_and_the_flyer_falls_back(client, gw):
    h, uid, s = await fighter(client, gw, "fl_7", "Phi Bảy")
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = at(6)
    assert abilities.gauge(p) == low()["gauge_seconds"], "a fresh gauge is full"
    take_off(gw, p, 1)
    fly_keys(gw, p, 2, 0, -1, 200)                       # out over the ink
    z = maps.load(KIEM_TRUNG_SON)
    if glide.land_ok(z.collider, z.tile_name, abilities.fly_over(1), p.x, p.y):
        p.x, p.y = tile_feet(*CHASM)
    hang = p.x, p.y
    s.sent.clear()
    run(gw, low()["gauge_seconds"] + 0.2)
    r = last(s, "fly")
    assert r["ok"] and r["on"] == 0 and r["why"] == "fall"
    fall = events(s, "fly")[-1]
    assert (fall["x0"], fall["y0"]) == (round(hang[0], 1), round(hang[1], 1)), "the fall starts where it hung"
    assert not p.fly and glide.land_ok(z.collider, z.tile_name, abilities.fly_over(1), p.x, p.y)
    assert math.hypot(p.x - x0, p.y - y0) < 20, "back on the ledge it came from"
    # an empty gauge does not take off again; on the ground it refills in refill_seconds
    assert abilities.request_fly(p, 9, True, gw.mono()) == "gauge_low"
    run(gw, low()["refill_seconds"] + 0.1)
    assert abilities.gauge(p) == pytest.approx(abilities.gauge_max(p))
    assert abilities.request_fly(p, 10, True, gw.mono()) is None


async def test_the_gauge_runs_dry_over_ground_and_lands_there(client, gw):
    h, uid, s = await fighter(client, gw, "fl_8", "Phi Tám")
    p = place(gw, s, KIEM_TRUNG_SON, *OPEN)
    s.tree = at(6)
    take_off(gw, p, 1)
    x, y = p.x, p.y
    s.sent.clear()
    run(gw, low()["gauge_seconds"] + 0.2)
    assert not p.fly and last(s, "fly")["why"] == "gauge" and (p.x, p.y) == (x, y)


async def test_kim_si_dieu_lengthens_the_gauge_and_a_linh_can_refills_it_faster(client, gw, monkeypatch):
    from app.systems import beasts as sysbeasts
    h, uid, s = await fighter(client, gw, "fl_9", "Phi Chín")
    p = place(gw, s, KIEM_TRUNG_SON, *OPEN)
    s.tree = at(6)
    base, refill = abilities.gauge_max(p), abilities.refill_seconds(p)
    assert (base, refill) == (low()["gauge_seconds"], low()["refill_seconds"])
    kim = next(b for b in math_tree.world_plan()["beasts"] if b["id"] == "kim_si_dieu")
    gift = kim["gift"]["value"]
    real = sysbeasts.gift          # (Kim Sí Điểu waits for its art: worn as if it were built)
    monkeypatch.setattr(sysbeasts, "gift", lambda pet: kim["gift"] if pet == "kim_si_dieu" else real(pet))
    p.pet = "kim_si_dieu"
    assert abilities.gauge_max(p) == pytest.approx(base * (1 + gift))
    assert abilities.flight_view(p)["gauge_max"] == pytest.approx(base * (1 + gift))
    p.stats = {**p.stats, "lc_fx": {"glide_cd": 0.25}}
    assert abilities.refill_seconds(p) == pytest.approx(refill * 0.75)
    assert abilities.glide_cooldown(p) == pytest.approx(unlock("dap_kiem_luot")["glide"]["cooldown_seconds"] * 0.75)


async def test_free_flight_at_truc_co_has_no_gauge_and_is_faster(client, gw):
    h, uid, s = await fighter(client, gw, "fl_10", "Phi Mười")
    p = place(gw, s, KIEM_TRUNG_SON, *OPEN)
    speed = p.channel.speed
    s.tree = at(0, "truc_co")
    p.fly_gauge = 0.0                                  # (an empty low-rung gauge does not matter up there)
    take_off(gw, p, 1)
    assert p.fly == 2
    x = p.x
    fly_keys(gw, p, 2, 1, 0, 400)
    assert p.x - x == pytest.approx(speed * high()["speed_mult"] * 0.4, abs=0.5)
    run(gw, 30)
    assert p.fly == 2, "no gauge: it flies as long as it likes"
    assert abilities.request_fly(p, 50, False, gw.mono()) is None
    run(gw, 0.1)
    assert not p.fly


# ------------------------------------------------------------------ fighting and flying
async def test_no_take_off_with_a_question_open_nor_right_after_a_blow(client, gw):
    h, uid, s = await fighter(client, gw, "fl_11", "Phi Mười Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    s.tree = at(6)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, combat.windup() + 0.2)
    await settle(gw)
    assert p.question is not None or p.q_pending or p.protected(gw.mono())
    assert abilities.request_fly(p, 1, True, gw.mono()) == "answering"
    p.question, p.q_pending, p.protect_until = None, False, 0.0      # answered
    m.mode, m.respawn_at = "dead", 1e12
    assert abilities.request_fly(p, 2, True, gw.mono()) == "struck"
    run(gw, low()["hit_lock_seconds"] + 0.05)
    assert abilities.request_fly(p, 3, True, gw.mono()) is None


async def test_a_blow_on_the_ground_misses_a_flyer(client, gw):
    h, uid, s = await fighter(client, gw, "fl_12", "Phi Mười Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    s.tree = at(6)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, 0.1)
    assert m.tele is not None, "the monster winds up"
    hp = p.hp
    take_off(gw, p, 1)                                  # seen in time: up on the sword
    run(gw, combat.windup())
    await settle(gw)
    assert last(s, "q") is None and p.hp == hp and p.fly == 1
    assert events(s, "soar")[-1]["id"] == p.eid
    m.atk_ready = 0.0
    run(gw, 1.0)
    assert m.tele is None, "it does not wind up at a flyer overhead"


async def test_a_blow_that_lands_during_the_rise_knocks_the_flyer_off(client, gw):
    h, uid, s = await fighter(client, gw, "fl_13", "Phi Mười Ba")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    s.tree = at(6)
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, combat.windup() - 0.1)                      # too late: the blow is about to land
    assert m.tele is not None
    take_off(gw, p, 1)
    s.sent.clear()
    run(gw, 0.2)
    await settle(gw)
    assert not p.fly and last(s, "fly")["why"] == "knocked"
    assert last(s, "q") is not None or p.q_pending or p.question is not None


async def test_in_the_air_nobody_attacks_casts_dodges_rides_seals_or_glides(client, gw):
    h, uid, s = await fighter(client, gw, "fl_14", "Phi Mười Bốn")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    luyen_khi(p, 9)
    s.tree = at(9)
    take_off(gw, p, 1)
    gw.mono.t += 2
    assert combat.attack(p, m.eid, gw.mono(), gw.rng) == "flying"
    assert combat.dodge(p, 2, 1, 0, gw.mono()) == "flying"
    sk = next(iter(math_skills.skills()))
    assert math_skills.request(p, sk, m.eid, gw.mono()) == "flying"
    p.pet = "tieu_long"
    assert abilities.request_ride(p, 3, True, gw.mono()) == "flying"
    assert abilities.request_glide(p, 4, p.x + 20, p.y, gw.mono()) == "flying"
    assert beasts.seal_target(p, m.eid, gw.mono()) == "not_here"     # (no beast) - and a flyer:
    assert beasts.SEAL_REFUSALS_VI["flying"]
    s.sent.clear()
    await gw.handle(s, {"t": "atk", "id": m.eid})
    assert last(s, "act_fail")["code"] == "flying"
    # and a rider does not take off
    run(gw, 0.2)
    assert abilities.request_fly(p, 9, False, gw.mono()) is None
    run(gw, 0.1)
    p.riding = True
    assert abilities.request_fly(p, 10, True, gw.mono()) == "riding"


async def test_no_flight_in_a_bi_canh(client, gw):
    h, uid, s = await fighter(client, gw, "fl_15", "Phi Mười Lăm")
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(*LEDGE))
    s.tree = at(6)
    p.channel.instance = True
    try:
        assert abilities.request_fly(p, 1, True, gw.mono()) == "cannot"
    finally:
        p.channel.instance = False


# ------------------------------------------------------------------ others, saves, zones
async def test_others_and_late_joiners_see_the_flyer(client, gw):
    h, uid, s = await fighter(client, gw, "fl_16", "Phi Mười Sáu")
    p = place(gw, s, KIEM_TRUNG_SON, *OPEN)
    s.tree = at(6)
    take_off(gw, p, 1)
    assert p.full()["fl"] == 1 and p.full()["fs"] == "phi_kiem_1"
    run(gw, 0.2)
    snap = last(s, "snap")
    assert snap["me"][9] == 1 and 0 < snap["me"][10] <= low()["gauge_seconds"]
    h2, uid2, s2 = await fighter(client, gw, "fl_17", "Phi Mười Bảy")
    assert gw.join(s2, "truc_lam_thon", "abode")
    gw._place(s2, KIEM_TRUNG_SON, p.x + 20, p.y, "left")
    assert s2.player.channel is p.channel
    run(gw, 0.2)
    seen = [e for m in s2.sent if m.get("t") == "snap" for e in m.get("add", []) if e["id"] == p.eid]
    assert seen and seen[-1]["fl"] == 1 and seen[-1]["fs"] == "phi_kiem_1"
    assert abilities.request_fly(p, 9, False, gw.mono()) is None
    run(gw, 0.2)
    again = [e for m in s2.sent if m.get("t") == "snap" for e in m.get("add", []) if e["id"] == p.eid]
    assert "fl" not in again[-1], "down again: the record is sent again without the flag"
    assert any(e.get("k") == "fly" and e["id"] == p.eid and e["on"] == 0
               for m in s2.sent if m.get("t") == "snap" for e in m.get("fx", []))


async def test_leaving_over_the_chasm_lands_on_the_ground(client, gw):
    h, uid, s = await fighter(client, gw, "fl_18", "Phi Mười Tám")
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = at(6)
    take_off(gw, p, 1)
    p.x, p.y = tile_feet(*CHASM)
    gw._queue_save(p)
    row = gw._save_now[uid]
    assert (row["x"], row["y"]) == (x0, y0), "saved on the ground under the flyer"
    gw.disconnect(s)
    assert not p.fly and (p.x, p.y) == (x0, y0)


async def test_a_new_channel_puts_the_flyer_on_the_ground(client, gw):
    h, uid, s = await fighter(client, gw, "fl_19", "Phi Mười Chín")
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = at(6)
    take_off(gw, p, 1)
    p.x, p.y = tile_feet(*CHASM)
    gw.channels[KIEM_TRUNG_SON].append(type(p.channel)(KIEM_TRUNG_SON, 2, p.channel.map))
    gw.switch_channel(s, 2)
    p = s.player
    assert p.channel.number == 2 and not p.fly and (p.x, p.y) == (x0, y0)
