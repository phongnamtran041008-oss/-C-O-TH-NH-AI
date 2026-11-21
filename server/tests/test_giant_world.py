"""The server on a giant map (Đại Địa Đồ): far monsters sleep, wake when a player comes near,
respawn on time, finish what they were doing; a player near them sees exactly what they would
see if nothing slept. No database: channels are built and ticked by hand."""
import json
import random

import pytest

from app.realtime import combat, maps
from app.realtime import world as wmod
from app.realtime.world import World
from app.realtime.zone import ChannelZone, Player

ZONE = "rung_muc_loang"      # a land of today; the map under it is the giant test map
DT = 0.05


class Mono:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


@pytest.fixture(autouse=True)
def quiet_world(monkeypatch):
    monkeypatch.setattr(wmod, "world", World(mono=Mono()))


def area(name, x, y, w, h, kind, count):
    return {"id": abs(hash(name)) % 100000, "name": name, "type": "monster_area", "x": x, "y": y,
            "width": w, "height": h,
            "properties": [{"name": "monster", "type": "string", "value": kind},
                           {"name": "count", "type": "string", "value": str(count)}]}


def giant(tmp_path, areas, w=256, h=256):
    """A w x h tile map of grass with these monster areas and a khu over all of it."""
    objs = [{"id": 1, "name": "spawn", "type": "spawn", "x": 1300, "y": 1300, "width": 0, "height": 0},
            {"id": 2, "name": "kts_ngoai_vi", "type": "khu", "x": 0, "y": 0, "width": w * 16, "height": h * 16,
             "properties": [{"name": "khu", "type": "string", "value": "kts_ngoai_vi"},
                            {"name": "band", "type": "string", "value": "1"}]}] + areas
    doc = {"width": w, "height": h, "tilewidth": 16, "tileheight": 16,
           "layers": [{"type": "tilelayer", "name": "ground", "data": [1] * (w * h)},
                      {"type": "objectgroup", "name": "objects", "objects": objs},
                      {"type": "objectgroup", "name": "collision", "objects": [
                          {"id": 900, "name": "", "type": "solid", "x": 2000, "y": 2000, "width": 32, "height": 32}]}]}
    p = tmp_path / "giant.tmj"
    p.write_text(json.dumps(doc), "utf-8")
    return maps.parse(p)


def channel(zmap, seed=4):
    return ChannelZone(ZONE, 1, zmap, random.Random(seed))


def player(uid, x, y):
    p = Player(uid, f"Đạo Hữu {uid}", {}, "luyen_khi", float(x), float(y))
    p.apply_stats({"max_hp": 1e6, "max_qi": 1e6}, heal=True)
    return p


def run(ch, seconds, t0=1000.0):
    t = t0
    for _ in range(round(seconds / DT)):
        t += DT
        ch.tick(DT, t)
    return t


def far_and_near(ch):
    near = [m for m in ch.monsters if m.area.name == "near"]
    far = [m for m in ch.monsters if m.area.name == "far"]
    return near, far


# ------------------------------------------------------------------ sleeping
def test_far_monsters_sleep_and_near_ones_wander(tmp_path):
    zmap = giant(tmp_path, [area("near", 1450, 1100, 150, 150, "ink_slime", 4),
                            area("far", 3300, 3300, 200, 200, "ink_slime", 4)])
    ch = channel(zmap)
    assert ch.sleepy and ch.wake_radius >= ch.radius + 1
    ch.add(player(1, 1300, 1300))
    near, far = far_and_near(ch)
    was_near, was_far = [(m.x, m.y) for m in near], [(m.x, m.y) for m in far]
    run(ch, 12.0)
    assert [(m.x, m.y) for m in near] != was_near
    assert [(m.x, m.y) for m in far] == was_far                        # asleep
    assert (int(far[0].x // ch.cell_px), int(far[0].y // ch.cell_px)) not in ch.wake_cells()


def test_a_sleeping_monster_wakes_when_a_player_comes(tmp_path):
    zmap = giant(tmp_path, [area("far", 3300, 3300, 200, 200, "tone_wisp", 3)])
    ch = channel(zmap)
    p = player(1, 300, 300)
    ch.add(p)
    t = run(ch, 2.0)
    m = next(m for m in ch.monsters if m.area.name == "far")
    still = (m.x, m.y)
    run(ch, 2.0, t)
    assert (m.x, m.y) == still
    p.x, p.y = m.x + 30, m.y                                          # right beside it: within its aggro radius
    t = run(ch, 0.3, t + 2.0)
    assert p.user_id in m.engaged and m.mode == "chase"


def test_respawn_timers_run_far_from_everyone(tmp_path):
    zmap = giant(tmp_path, [area("far", 3300, 3300, 200, 200, "ink_slime", 2)])
    ch = channel(zmap)
    ch.add(player(1, 300, 300))
    m = next(m for m in ch.monsters if m.area.name == "far")
    m.mode, m.respawn_at, m.hp = "dead", 1001.0, 0
    run(ch, 2.0)
    assert m.alive and m.mode == "wander" and m.hp == m.max_hp
    assert m.area.contains(m.x, m.y)


def test_a_monster_going_home_is_awake_until_it_is_there(tmp_path):
    zmap = giant(tmp_path, [area("far", 3300, 3300, 200, 200, "ink_slime", 1)])
    ch = channel(zmap)
    ch.add(player(1, 300, 300))
    m = next(m for m in ch.monsters if m.area.name == "far")
    m.x, m.y, m.mode, m.hp = 3200.0, 3250.0, "return", 1.0           # dragged off, far from every player
    run(ch, 15.0)
    hx, hy = m.home
    assert m.mode == "wander" and abs(m.x - hx) < 6 and abs(m.y - hy) < 6
    assert m.hp == m.max_hp                                            # home: healed, as before


def test_an_engaged_monster_keeps_fighting_even_out_of_the_wake_cells(tmp_path):
    zmap = giant(tmp_path, [area("far", 3300, 3300, 200, 200, "tone_wisp", 1)])
    ch = channel(zmap)
    p = player(1, 300, 300)
    ch.add(p)
    m = next(m for m in ch.monsters if m.area.name == "far")
    m.engaged = {p.user_id}
    x0, y0 = m.x, m.y
    t = run(ch, 1.0)
    assert m.mode == "chase" and m.x < x0 and m.y < y0          # it runs after its foe, far from everyone
    for _ in range(60):                                          # dragged past its leash it gives up, goes home
        t = run(ch, 1.0, t)
        if m.mode == "wander":
            break
    hx, hy = m.home
    assert m.mode == "wander" and not m.engaged and abs(m.x - hx) < 6 and abs(m.y - hy) < 6


def test_a_player_near_them_sees_what_they_would_see_if_nothing_slept(tmp_path):
    zmap = giant(tmp_path, [area("near", 1450, 1100, 150, 150, "ink_slime", 5),
                            area("near", 1050, 1450, 150, 120, "tone_wisp", 3),
                            area("far", 3300, 3300, 200, 200, "ink_slime", 6),
                            area("far", 300, 3400, 200, 200, "tone_wisp", 6)])
    a, b = channel(zmap, seed=9), channel(zmap, seed=9)
    b.sleepy = False                       # the same channel where nothing ever sleeps
    pa, pb = player(1, 1300, 1300), player(1, 1300, 1300)
    a.add(pa)
    b.add(pb)
    t = 1000.0
    slept = 0
    for i in range(400):
        t += DT
        a.tick(DT, t)
        b.tick(DT, t)
        slept += sum(1 for m in a.monsters if (int(m.x // a.cell_px), int(m.y // a.cell_px)) not in a.wake_cells())
        if i % 2:
            sa, sb = a.snapshot_for(pa, t), b.snapshot_for(pb, t)
            assert sa == sb, i
    assert slept > 0
    seen = {e[0] for e in pa.known.values()}
    assert any(m.eid in seen for m in a.monsters if m.area.name == "near")
    near_a = [(m.x, m.y, m.mode) for m in a.monsters if m.area.name == "near"]
    near_b = [(m.x, m.y, m.mode) for m in b.monsters if m.area.name == "near"]
    assert near_a == near_b


def test_aggro_through_the_player_grid_finds_who_a_full_scan_finds(tmp_path):
    zmap = giant(tmp_path, [area("far", 3300, 3300, 200, 200, "ink_slime", 1)])
    ch = channel(zmap)
    rng = random.Random(3)
    for uid in range(1, 41):
        ch.add(player(uid, rng.uniform(0, 4000), rng.uniform(0, 4000)))
    combat._player_grid(ch, ch.cell_px)
    m = ch.monsters[0]
    for _ in range(500):
        m.x, m.y = rng.uniform(0, 4096), rng.uniform(0, 4096)
        r = rng.uniform(0, ch.cell_px)
        full = [p for p in ch.players.values() if combat.dist(p.x, p.y, m.x, m.y) <= r]
        got = [p for p in combat._near_players(ch, m, r) if combat.dist(p.x, p.y, m.x, m.y) <= r]
        assert got == full
    q = next(iter(ch.players.values()))                 # a player moved by a knock-down (an event): seen at once
    q.x, q.y = m.x + 3, m.y
    ch.event(k="fly", id=q.eid)
    assert q in combat._near_players(ch, m, 10)
    ch._pgrid = None
    assert list(combat._near_players(ch, m, 10)) == list(ch.players.values())   # no grid: everyone


# ------------------------------------------------------------------ today's maps are untouched
def test_small_maps_and_bi_canh_never_sleep():
    ch = ChannelZone("truc_lam_thon", 1, maps.load("truc_lam_thon"))    # (Mê Đồ Lâm is giant since B2)
    assert not ch.sleepy and ch.wake_cells() is None
    assert all(getattr(m, "rng", None) is None for m in ch.monsters)    # they share the channel's stream, as before


def test_monster_lookup_by_id_follows_the_list(tmp_path):
    zmap = giant(tmp_path, [area("near", 1450, 1100, 150, 150, "ink_slime", 3)])
    ch = channel(zmap)
    m = ch.monsters[1]
    assert ch.monster(m.eid) is m and ch.monster("nope") is None
    ch.monsters = ch.monsters[:1]                         # replaced (a bí cảnh does this): looked up again
    assert ch.monster(m.eid) is None and ch.monster(ch.monsters[0].eid) is ch.monsters[0]
