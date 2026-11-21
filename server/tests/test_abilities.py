"""Thần thông of Luyện Khí (world_plan.json `unlocks`, wired section 'abilities', realtime/abilities.py):
Bày pháp trận slows the windup of the monsters standing in it, Đạp Kiếm Lướt glides over chasms
and water (and nothing else) to a walkable landing and opens the weapon spots that need it,
Cưỡi linh thú moves the rider faster at a speed only the server decides. Each is refused before
its stage of Đạo Thụ. The world runs on a fake clock ticked by hand (test_combat's machinery).
"""
import math

import pytest
import pytest_asyncio

from app.learning import math_tree
from app.realtime import abilities, combat, glide, lands, maps, protocol
from app.realtime import world as wmod
from app.realtime.world import World
from app.systems import weapons
from tests.test_combat import FakeMono, fighter, last, run, settle
from tests.test_combat_on_hit import SLIME_MA, VALLEY, events, provoke, stand_at

KIEM_TRUNG_SON = "loan_so_coc"      # Kiếm Trủng Sơn: kiem_2_ha sits behind a chasm of ink
LUU_VAN_COC = "luu_van_coc"         # Lưu Vân Cốc: dao_2_ha sits in the waterfall


def spot_pos(pid: str) -> tuple[int, int]:
    """The tile of a weapon spot (world_plan.json weapons_placed), e.g. "kiem_2_ha"."""
    return tuple(next(p for p in math_tree.world_plan()["weapons_placed"]
                      if f"{p['weapon']}_{p['quality']}" == pid)["pos"])


# Đại Địa Đồ (2026-11-21): the places are read from the plan, not written here. Around both spots
# the giant maps keep the small maps' shape: Kiếm Trủng Sơn's peak (3 x 2 tiles) in a ring of ink,
# the ledge 4 tiles south of the spot; Lưu Vân Cốc's ledge in the pool, the shore 3 tiles south.
PEAK = spot_pos("kiem_2_ha")
LEDGE = (PEAK[0], PEAK[1] + 4)       # the ledge below the nest of Hỏa Tước
CHASM = (PEAK[0], PEAK[1] + 3)       # the ink between them
POOL = spot_pos("dao_2_ha")          # the ledge in the clouds above the falls
SHORE = (POOL[0], POOL[1] + 3)       # the rock at the foot of the waterfall


@pytest_asyncio.fixture
async def gw(app, monkeypatch):
    w = World(mono=FakeMono())
    monkeypatch.setattr(wmod, "world", w)
    yield w
    await settle(w)


def unlock(uid: str) -> dict:
    return next(u for u in math_tree.world_plan()["unlocks"] if u["id"] == uid)


def pos(stage: int) -> lands.TreePos:
    return lands.TreePos("luyen_khi", stage, frozenset())


def tile_feet(tx: int, ty: int) -> tuple[float, float]:
    return tx * 16 + 8.0, ty * 16 + 12.0


def place(w: World, s, zone: str, x: float, y: float):
    """The player at (x, y) of a zone, every monster of the channel out of the way."""
    assert w.join(s, "truc_lam_thon", "abode")
    ch = w._pick_channel(zone)
    for m in ch.monsters:
        m.mode, m.respawn_at = "dead", 1e12
    w._place(s, zone, x, y, "up")
    return s.player


def test_the_four_luyen_khi_unlocks_are_built_and_later_ones_wait():
    for uid, stage in (("thu_phuc_linh_thu", 3), ("phap_tran", 5), ("dap_kiem_luot", 6), ("cuoi_linh_thu", 8)):
        u = unlock(uid)
        assert (u["realm"], u["stage"], u["status"]) == ("luyen_khi", stage, "co"), uid
    later = [u for u in math_tree.world_plan()["unlocks"] if u["realm"] != "luyen_khi"]
    # (Ngự Kiếm Phi Hành is built ahead of its land: test_flight)
    assert later and all(u["status"] == "chua_co" for u in later if u["id"] != "ngu_kiem_phi_hanh")
    assert {"glide", "ride", "tran", "fly"} <= set(protocol.MESSAGES)


# ------------------------------------------------------------------ Bày pháp trận
async def test_a_formation_slows_the_windup_of_a_monster_inside_it(client, gw):
    h, uid, s = await fighter(client, gw, "ab_1", "Trận Một")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    f = unlock("phap_tran")["formation"]
    s.tree = pos(4)
    assert abilities.place_formation(p, gw.mono()) == "formation_locked"
    s.tree = pos(5)
    # without a formation: the plain windup
    await provoke(gw, p, m)
    m.atk_ready = 0.0
    run(gw, 0.1)
    assert m.tele is not None and m.tele["land"] - gw.mono() == pytest.approx(combat.windup() - 0.05, abs=0.06)
    m.tele, m.atk_ready = None, 1e12
    # laid at the feet: the monster beside the player stands in it and winds up slower
    assert abilities.place_formation(p, gw.mono()) is None
    tran = events(s, "tran")[-1]
    assert (tran["r"], tran["d"], tran["by"]) == (f["radius_px"], f["seconds"], p.eid)
    assert abilities.windup_mult(p.channel, m, gw.mono()) == f["windup_mult"]
    m.atk_ready = 0.0
    run(gw, 0.1)
    assert m.tele is not None
    assert m.tele["land"] - gw.mono() == pytest.approx(combat.windup() * f["windup_mult"] - 0.05, abs=0.06)
    assert events(s, "tele")[-1]["d"] == pytest.approx(combat.windup() * f["windup_mult"])
    # a monster outside it is not slowed, and the formation fades after its seconds
    m.x += f["radius_px"] + 10
    assert abilities.windup_mult(p.channel, m, gw.mono()) == 1.0
    m.x -= f["radius_px"] + 10
    assert abilities.place_formation(p, gw.mono()) == "cooldown"
    run(gw, f["seconds"] + 0.1)
    assert abilities.windup_mult(p.channel, m, gw.mono()) == 1.0
    assert abilities.formations_view(p.channel, gw.mono()) == []


async def test_the_world_answers_a_formation_and_its_refusal(client, gw):
    h, uid, s = await fighter(client, gw, "ab_2", "Trận Hai")
    p, m = stand_at(gw, s, VALLEY, SLIME_MA)
    s.tree = pos(1)
    await gw.handle(s, {"t": "tran"})
    r = last(s, "tran")
    assert r["ok"] is False and r["code"] == "formation_locked" and r["message_vi"]
    s.tree = pos(5)
    await gw.handle(s, {"t": "tran"})
    assert last(s, "tran")["ok"] is True
    assert last(s, "tran")["ready_in"] == unlock("phap_tran")["formation"]["cooldown_seconds"]


# ------------------------------------------------------------------ Đạp Kiếm Lướt
def over() -> set:
    return set(unlock("dap_kiem_luot")["glide"]["over_tiles"])


def landing(zone: str, x: float, y: float, dx: int, dy: int):
    z = maps.load(zone)
    g = unlock("dap_kiem_luot")["glide"]
    return glide.pick(z.collider, z.tile_name, over(), x, y, dx, dy, g["max_px"], g["min_px"])


async def test_a_glide_crosses_the_chasm_to_the_spot_behind_it(client, gw):
    h, uid, s = await fighter(client, gw, "ab_3", "Lướt Ba")
    x0, y0 = tile_feet(*LEDGE)                               # the ledge below the nest of Hỏa Tước
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = pos(6)
    spot = weapons.data()["by_id"]["kiem_2_ha"]
    z = maps.load(KIEM_TRUNG_SON)
    assert z.tile_name(*CHASM) == "ink" and z.collider.blocked(*tile_feet(*CHASM)), "a chasm of ink"
    to = landing(KIEM_TRUNG_SON, x0, y0, 0, -1)
    assert to is not None and (int(to[0] // 16), int((to[1] - 1) // 16)) in {(PEAK[0], PEAK[1] + 1), PEAK}
    # walking there is impossible: the steps stop at the chasm
    p.channel.queue_input(p, 1, [(0, -1, 100)] * 10)
    run(gw, 1.2)
    assert p.y > tile_feet(*CHASM)[1] - 16, "on foot the chasm stops it"
    p.x, p.y = x0, y0
    s.sent.clear()
    assert abilities.request_glide(p, 2, to[0], to[1], gw.mono()) is None
    run(gw, 0.1)
    assert (p.x, p.y) == to and last(s, "glide")["ok"] is True
    g = events(s, "glide")[-1]
    assert (g["x0"], g["y0"], g["ms"]) == (round(x0, 1), round(y0, 1), unlock("dap_kiem_luot")["glide"]["ms"])
    assert math.hypot(spot["pos"][0] * 16 + 8 - p.x, spot["pos"][1] * 16 + 12 - p.y) < 24, "beside the spot now"
    assert abilities.request_glide(p, 3, x0, y0, gw.mono()) == "cooldown"


async def test_a_glide_crosses_water_too(client, gw):
    h, uid, s = await fighter(client, gw, "ab_4", "Lướt Bốn")
    x0, y0 = tile_feet(*SHORE)                               # the rock at the foot of the waterfall
    p = place(gw, s, LUU_VAN_COC, x0, y0)
    s.tree = pos(6)
    assert maps.load(LUU_VAN_COC).tile_name(SHORE[0], SHORE[1] - 1) == "water"
    to = landing(LUU_VAN_COC, x0, y0, 0, -1)
    assert to is not None and int(to[0] // 16) == POOL[0] and int((to[1] - 1) // 16) == POOL[1]
    assert abilities.request_glide(p, 1, to[0], to[1], gw.mono()) is None
    run(gw, 0.1)
    assert (p.x, p.y) == to


async def test_a_glide_is_refused_before_its_stage(client, gw):
    h, uid, s = await fighter(client, gw, "ab_5", "Lướt Năm")
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = pos(5)
    to = landing(KIEM_TRUNG_SON, x0, y0, 0, -1)
    await gw.handle(s, {"t": "glide", "s": 1, "x": to[0], "y": to[1]})
    r = last(s, "glide")
    assert r["ok"] is False and r["code"] == "glide_locked" and "tầng 6" in r["message_vi"]
    run(gw, 0.2)
    assert (p.x, p.y) == (x0, y0) and p.ack == 1, "nothing moved; the number was used up"


async def test_a_glide_is_refused_onto_a_tile_that_is_not_walkable(client, gw):
    h, uid, s = await fighter(client, gw, "ab_6", "Lướt Sáu")
    x0, y0 = tile_feet(*SHORE)
    p = place(gw, s, LUU_VAN_COC, x0, y0)
    s.tree = pos(6)
    wet = tile_feet(POOL[0], POOL[1] + 1)                    # into the waterfall itself
    assert abilities.request_glide(p, 1, *wet, gw.mono()) is None
    s.sent.clear()
    run(gw, 0.1)
    r = last(s, "glide")
    assert r["ok"] is False and r["code"] == "bad_landing" and (p.x, p.y) == (x0, y0)
    assert not events(s, "glide")


async def test_a_glide_does_not_pass_walls_nor_go_too_far(client, gw):
    h, uid, s = await fighter(client, gw, "ab_7", "Lướt Bảy")
    z = maps.load(KIEM_TRUNG_SON)
    x0, y0 = tile_feet(*LEDGE)
    p = place(gw, s, KIEM_TRUNG_SON, x0, y0)
    s.tree = pos(6)
    g = unlock("dap_kiem_luot")["glide"]
    far = (x0, y0 - g["max_px"] - 20)
    assert glide.check(z.collider, z.tile_name, over(), x0, y0, *far, g["max_px"]) == "too_far"
    # east of the ledge stands a stone wall (solid, and no chasm): a glide through it is refused
    lx, ly = LEDGE
    wall = next(tx for tx in range(lx + 1, lx + 5) if z.collider.blocked(*tile_feet(tx, ly))
                and z.tile_name(tx, ly) not in over())
    beyond = next((tile_feet(tx, ly) for tx in range(wall + 1, lx + 5) if not z.collider.blocked(*tile_feet(tx, ly))),
                  None)
    if beyond is not None and math.hypot(beyond[0] - x0, 0) <= g["max_px"]:
        assert glide.check(z.collider, z.tile_name, over(), x0, y0, *beyond, g["max_px"]) == "blocked"
    else:     # nothing walkable behind it: the landing itself is refused
        assert glide.check(z.collider, z.tile_name, over(), x0, y0, *tile_feet(wall, ly), g["max_px"]) == "bad_landing"
    assert abilities.request_glide(p, 1, *tile_feet(wall, ly), gw.mono()) is None
    run(gw, 0.1)
    assert (p.x, p.y) == (x0, y0)


async def test_no_glide_while_answering_or_in_a_bi_canh(client, gw):
    h, uid, s = await fighter(client, gw, "ab_8", "Lướt Tám")
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(*LEDGE))
    s.tree = pos(6)
    p.protect_until = gw.mono() + 5
    assert abilities.request_glide(p, 1, *tile_feet(PEAK[0], PEAK[1] + 1), gw.mono()) == "answering"
    p.protect_until = 0.0
    p.channel.instance = True
    try:
        assert abilities.request_glide(p, 2, *tile_feet(PEAK[0], PEAK[1] + 1), gw.mono()) == "cannot"
        assert abilities.view(p, gw.mono()) is None
    finally:
        p.channel.instance = False


def test_the_spots_behind_the_chasm_and_the_waterfall_open_with_the_glide(monkeypatch):
    every = set(math_tree.tree().nodes)
    for pid in ("kiem_2_ha", "dao_2_ha"):
        spot = weapons.data()["by_id"][pid]
        assert spot["needs"] == "dap_kiem_luot"
        assert weapons.missing(spot, ("luyen_khi", 9), every) == [], pid
    real = weapons.data()

    def unbuilt():
        d = dict(real)
        d["unlocks"] = {**real["unlocks"], "dap_kiem_luot": {**real["unlocks"]["dap_kiem_luot"], "status": "chua_co"}}
        return d
    monkeypatch.setattr(weapons, "data", unbuilt)
    assert any("Đạp Kiếm Lướt" in x for x in weapons.missing(real["by_id"]["kiem_2_ha"], ("luyen_khi", 9), every))


# ------------------------------------------------------------------ Cưỡi linh thú
def open_ground(w: World, s):
    """A stretch of free ground in Kiếm Trủng Sơn for timing a walk: the first row near the gate
    (searched, not written here: the giant map is generated) with 200 px free to the east."""
    z = maps.load(KIEM_TRUNG_SON)
    sx, sy = z.spawn("from_village")
    for ty in range(int(sy // 16), int(sy // 16) - 40, -1):
        for tx in range(int(sx // 16) - 20, int(sx // 16) + 20):
            x0, y0 = tile_feet(tx, ty)
            if all(not z.collider.blocked(x0 + d, y0) for d in range(0, 200, 4)):
                return place(w, s, KIEM_TRUNG_SON, x0, y0)
    raise AssertionError("no free stretch near the gate of Kiếm Trủng Sơn")


async def walk_right(w: World, p, seq: int, ms: int) -> float:
    """Hold the right key for `ms`, sent as the client sends it (200 ms per message, from `seq`)."""
    x0 = p.x
    for i in range(ms // 200):
        p.channel.queue_input(p, seq + i, [(1, 0, 100), (1, 0, 100)])
    run(w, ms / 1000 + 0.3)
    return p.x - x0


async def test_riding_the_mount_moves_faster_at_the_servers_speed(client, gw):
    h, uid, s = await fighter(client, gw, "ab_9", "Cưỡi Chín")
    p = open_ground(gw, s)
    speed = p.channel.speed
    s.tree = pos(8)
    assert abilities.request_ride(p, 1, True, gw.mono()) == "no_mount"
    run(gw, 0.1)
    assert not p.riding
    p.pet = "tieu_long"
    s.tree = pos(7)
    assert abilities.request_ride(p, 2, True, gw.mono()) == "ride_locked"
    s.tree = pos(8)
    walked = await walk_right(gw, p, 3, 400)
    assert walked == pytest.approx(speed * 0.4, abs=0.5)
    s.sent.clear()
    assert abilities.request_ride(p, 10, True, gw.mono()) is None
    run(gw, 0.1)
    assert p.riding and last(s, "ride")["on"] is True and events(s, "ride")[-1]["on"] == 1
    mult = next(b for b in math_tree.world_plan()["beasts"] if b["id"] == "tieu_long")["gift"]["speed_mult"]
    assert last(s, "ride")["mult"] == mult
    ridden = await walk_right(gw, p, 11, 400)
    assert ridden == pytest.approx(speed * mult * 0.4, abs=0.5)
    # a client cannot ask for more: it only sends keys and time, the server applies the speed
    x0 = p.x
    for i in range(12):
        p.channel.queue_input(p, 20 + i, [(1, 0, 100), (1, 0, 100)])
    run(gw, 0.5)
    lag = wmod.cfg()["move_budget_max_ms"] / 1000     # (the time budget lets a late client catch up this much)
    assert p.x - x0 <= speed * mult * (0.5 + lag) + 1
    assert p.full()["rd"] == 1
    # getting down, and taking the mount off, end the ride
    assert abilities.request_ride(p, 50, False, gw.mono()) is None
    assert p.riding, "it happens in the movement stream, after the steps sent before it"
    run(gw, 3.0)
    assert not p.riding
    assert abilities.request_ride(p, 51, True, gw.mono()) is None
    run(gw, 0.1)
    gw.set_pet(uid, None)
    assert not p.riding and last(s, "ride")["on"] is False


async def test_the_zone_message_tells_the_client_its_thanthong(client, gw):
    h, uid, s = await fighter(client, gw, "ab_10", "Thần Mười")
    s.tree = pos(6)
    p = place(gw, s, KIEM_TRUNG_SON, *tile_feet(51, 6))
    a = last(s, "zone")["abilities"]
    assert a["dap_kiem_luot"]["ok"] and a["phap_tran"]["ok"] and not a["cuoi_linh_thu"]["ok"]
    assert a["dap_kiem_luot"]["max_px"] == unlock("dap_kiem_luot")["glide"]["max_px"]
    assert a["dap_kiem_luot"]["over"] == unlock("dap_kiem_luot")["glide"]["over_tiles"]
    assert a["phap_tran"]["radius"] == unlock("phap_tran")["formation"]["radius_px"]
    assert a["thu_phuc_linh_thu"]["unlock"] == {"realm": "luyen_khi", "stage": 3}
    assert last(s, "zone")["formations"] == [] and p.channel is not None
