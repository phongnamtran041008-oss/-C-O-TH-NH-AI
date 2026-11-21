"""Chỉ Đường, the client parts without a server (docs/CHI_DUONG.md):

* the walk grid agrees with the movement collider (every walkable cell is a foot position the
  collider allows, the step to a walkable neighbour too);
* the way round walls and through a maze, a stray player read again without a new search, an
  island with no way on foot (a straight arrow), and a 320 x 240 tile map searched within the
  frame budget;
* the route from zone to zone through the gates of the shipped maps, the abode's gate included;
* a synthetic .tmj with khu: the khu read from the map, the banner, the big map's khu target,
  the minimap's overview and its window on a giant map;
* every string can be drawn by the shipped pixel font.
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import pygame
import pytest

from client.engine import chi_duong, minimap, navigator as nv
from client.engine import movement as mv

ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------ helpers
def maze(tw: int, th: int, corridor: int = 2, seed: int = 1):
    """A perfect maze of rooms `corridor` tiles wide and 1-tile walls, as solid rectangles (px);
    the start and goal are opposite corners."""
    rng = random.Random(seed)
    step = corridor + 1
    nx, ny = (tw - 1) // step, (th - 1) // step
    wall = [[True] * tw for _ in range(th)]
    for j in range(ny):
        for i in range(nx):
            for y in range(j * step + 1, j * step + 1 + corridor):
                for x in range(i * step + 1, i * step + 1 + corridor):
                    wall[y][x] = False
    seen, stack = {(0, 0)}, [(0, 0)]
    while stack:
        i, j = stack[-1]
        nb = [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= i + a < nx and 0 <= j + b < ny and (i + a, j + b) not in seen]
        if not nb:
            stack.pop()
            continue
        a, b = rng.choice(nb)
        seen.add((a, b))
        stack.append((a, b))
        if a != i:
            for y in range(j * step + 1, j * step + 1 + corridor):
                wall[y][max(a, i) * step] = False
        else:
            for x in range(i * step + 1, i * step + 1 + corridor):
                wall[max(b, j) * step][x] = False
    solids = []
    for y in range(th):
        x = 0
        while x < tw:
            if wall[y][x]:
                x0 = x
                while x < tw and wall[y][x]:
                    x += 1
                solids.append((x0 * 16, y * 16, (x - x0) * 16, 16))
            else:
                x += 1
    start = (16 + 8, 16 + 11)
    goal = ((nx - 1) * step * 16 + 16 + 8, (ny - 1) * step * 16 + 16 + 11)
    return solids, start, goal


def walk_reading(leg: nv.Leg, col: mv.Collider, x: float, y: float, limit: int = 4000) -> tuple[float, float]:
    """Walk with the movement code toward each reading's aim, as the arrow says; returns where it stopped."""
    for _ in range(limit):
        r = leg.read(x, y)
        if r.mode == "here":
            break
        assert r.mode == "path", r.mode
        ax, ay = r.aim
        dx = (ax > x + 1) - (ax < x - 1)
        dy = (ay > y + 1) - (ay < y - 1)
        if not dx and not dy:
            break
        x, y = mv.step(x, y, dx, dy, 50, 74.0, col)
    return x, y


def run(leg: nv.Leg, budget: float = 0.003, frames: int = 100000) -> tuple[int, float]:
    worst, n = 0.0, 0
    for n in range(1, frames + 1):
        t = time.perf_counter()
        done = leg.step(budget)
        worst = max(worst, time.perf_counter() - t)
        if done:
            break
    return n, worst


# ------------------------------------------------------------------ the grid
def test_every_walkable_cell_is_a_foot_position_the_collider_allows():
    rng = random.Random(7)
    solids = [(rng.randrange(0, 600), rng.randrange(0, 400), rng.randrange(1, 40), rng.randrange(1, 40))
              for _ in range(120)]
    col = mv.Collider(640, 448, solids)
    g = nv.WalkGrid(640, 448, solids).build_now()
    free = 0
    for cy in range(g.ch):
        for cx in range(g.cw):
            i = g.index(cx, cy)
            x, y = g.point(i)
            if not g.walk[i]:
                continue
            free += 1
            assert not col.blocked(x, y), (cx, cy)
            for j in (i + 1, i + g.W):                  # the way to a walkable neighbour is free too
                if g.walk[j]:
                    x2, y2 = g.point(j)
                    for k in range(1, 8):
                        assert not col.blocked(x + (x2 - x) * k / 8, y + (y2 - y) * k / 8), (cx, cy, j)
    assert free > 1000


def test_a_one_tile_corridor_is_walkable():
    # walls above and below a corridor one tile high, left of and right of one a tile wide
    solids = [(0, 0, 320, 16), (0, 32, 160, 16), (176, 32, 144, 200)]
    g = nv.WalkGrid(320, 240, solids).build_now()
    assert g.walk[g.index_of(100, 27)]                      # in the horizontal corridor (y = tile + 11)
    assert g.walk[g.index_of(168, 40)]                      # in the vertical slot (x = tile + 8)


# ------------------------------------------------------------------ the way in a zone
def test_the_way_goes_round_a_wall_not_through_it():
    solids = [(150, 0, 20, 300)]                            # a wall with a gap at the bottom
    col = mv.Collider(320, 400, solids)
    leg = nv.Leg(nv.WalkGrid(320, 400, solids), goal_point=(260, 100))
    run(leg)
    r = leg.read(40, 100, route_cells=400)
    assert r.mode == "path" and r.aim[1] > 100              # it points down, toward the gap
    assert max(y for _, y in r.route) > 300                 # the way passes under the wall
    assert r.dist_px > 2 * (300 - 100)
    x, y = walk_reading(leg, col, 40, 100)
    assert abs(x - 260) < 20 and abs(y - 100) < 20, (x, y)


def test_a_maze_is_walked_by_following_the_arrow():
    solids, start, goal = maze(41, 31)
    col = mv.Collider(41 * 16, 31 * 16, solids)
    leg = nv.Leg(nv.WalkGrid(41 * 16, 31 * 16, solids), goal_point=goal)
    run(leg)
    x, y = walk_reading(leg, col, *start, limit=20000)
    assert abs(x - goal[0]) < 16 and abs(y - goal[1]) < 16, (x, y, goal)


def test_a_player_who_strays_is_read_again_without_a_new_search():
    solids, start, goal = maze(41, 31, seed=3)
    leg = nv.Leg(nv.WalkGrid(41 * 16, 31 * 16, solids), goal_point=goal)
    run(leg)
    field = leg.field
    elsewhere = next(leg.grid.point(i) for i in range(len(field.dist)) if field.dist[i] > 40)
    assert leg.read(*elsewhere).mode == "path" and leg.field is field


def test_an_island_has_no_way_on_foot_and_gets_a_straight_arrow():
    solids = [(100, 0, 16, 400), (0, 100, 300, 16), (300, 0, 16, 400), (0, 300, 400, 16)]   # a closed box
    leg = nv.Leg(nv.WalkGrid(400, 400, solids), goal_point=(200, 200))
    run(leg)
    r = leg.read(50, 50)
    assert r.mode == "straight" and r.aim == (200, 200) and r.dist_px == pytest.approx(212.1, abs=1)


def test_a_gate_on_the_edge_of_the_map_is_a_goal():
    leg = nv.Leg(nv.WalkGrid(320, 320, []), goal_rect=(-8, 128, 28, 64))
    run(leg)
    assert leg.field.goals
    r = leg.read(200, 160)
    assert r.mode == "path" and r.aim[0] < 200


def test_a_giant_map_is_searched_a_few_milliseconds_a_frame():
    """320 x 240 tiles (5120 x 3840 px): building the grid and the field is spread over frames;
    no frame spends much more than the 3 ms budget (one slice of 1024 cells may overrun it)."""
    solids, start, goal = maze(320, 240, corridor=3, seed=5)
    g = nv.WalkGrid(320 * 16, 240 * 16, solids)
    leg = nv.Leg(g, goal_point=goal)
    t = time.perf_counter()
    frames, worst = run(leg)
    total = time.perf_counter() - t
    assert leg.ready and leg.field.reached > 100000
    assert frames > 3 and worst < 0.012, (frames, worst)    # (generous: other tests run at the same time)
    assert total < 2.0, total
    t = time.perf_counter()
    r = leg.read(*start, route_cells=900)
    assert time.perf_counter() - t < 0.01
    assert r.mode == "path" and len(r.route) > 50
    print(f"giant maze: {len(solids)} solids, {frames} frames, worst {worst * 1000:.1f} ms, total {total * 1000:.0f} ms")


# ------------------------------------------------------------------ from zone to zone
def test_the_route_between_zones_goes_through_the_village():
    zones = nv.world_zones()
    assert {"truc_lam_thon", "abode", "loan_so_coc", "luu_van_coc"} <= set(zones) and "bi_canh" not in zones
    r = nv.zone_route(zones, "loan_so_coc", "luu_van_coc")
    assert [(g.zone, g.target) for g in r] == [("loan_so_coc", "truc_lam_thon"), ("truc_lam_thon", "luu_van_coc")]
    assert nv.zone_route(zones, "truc_lam_thon", "truc_lam_thon") == []
    out = nv.zone_route(zones, "abode", "ho_nghien_muc")
    assert out[0].kind == "exit" and out[0].target == "truc_lam_thon" and out[1].target == "ho_nghien_muc"
    assert nv.zone_route(zones, "truc_lam_thon", "nowhere") is None
    assert nv.estimate_after(zones, r, (100, 100)) > 0


def test_distances_are_trượng():
    assert nv.truong(0) == 0 and nv.truong(3) == 1 and nv.truong(32 * 40) == 40


# ------------------------------------------------------------------ a synthetic map with khu
def khu_obj(oid, x, y, w, h, kid, name, band, lo, hi):
    props = [{"name": k, "type": "string", "value": str(v)} for k, v in
             (("khu", kid), ("name_vi", name), ("band", band), ("stage_min", lo), ("stage_max", hi),
              ("anchor_x", x + w // 2), ("anchor_y", y + h // 2), ("realm", "luyen_khi"))]
    return {"id": oid, "name": kid, "type": "khu", "x": x, "y": y, "width": w, "height": h, "properties": props}


def write_tmj(path: Path, tw: int, th: int, objects: list, solids: list) -> Path:
    data = {"width": tw, "height": th, "tilewidth": 16, "tileheight": 16, "properties": [],
            "layers": [{"type": "tilelayer", "name": "ground", "data": [1 + (i % 7 == 0) * 7 for i in range(tw * th)]},
                       {"type": "objectgroup", "name": "objects", "objects": objects},
                       {"type": "objectgroup", "name": "collision",
                        "objects": [{"id": 900 + i, "name": "", "type": "solid", "x": x, "y": y, "width": w,
                                     "height": h} for i, (x, y, w, h) in enumerate(solids)]}]}
    path.write_text(json.dumps(data), "utf-8")
    return path


@pytest.fixture
def khu_map(tmp_path):
    from client.engine.tilemap import TileMap
    objs = [khu_obj(1, 0, 0, 640, 320, "t_an", "Trại An Toàn", 0, 0, 0),
            khu_obj(2, 0, 0, 1280, 960, "t_ngoai", "Ngoại Vi Thử", 1, 1, 3),
            khu_obj(3, 1280, 0, 1280, 960, "t_trung", "Trung Vực Thử", 2, 4, 6),
            {"id": 4, "name": "camp", "type": "poi", "x": 100, "y": 100, "width": 16, "height": 16,
             "properties": [{"name": "poi", "type": "string", "value": "camp"},
                            {"name": "name_vi", "type": "string", "value": "Trại"}]}]
    return TileMap(write_tmj(tmp_path / "thu.tmj", 160, 60, objs, [(600, 0, 16, 700)]))


class FakeGame:
    def __init__(self):
        self.now = 0.0
        self.toasts: list = []

    def toast(self, text, *rest):
        self.toasts.append(text)


class FakeScene:
    def __init__(self, tmap, x, y, zone="thu"):
        self.map, self.zone_id = tmap, zone
        self.player = type("P", (), {"x": x, "y": y})()
        self.realm = None


def test_the_khu_of_a_map_are_read_first_one_wins(khu_map):
    assert [p["khu"] for _, p in chi_duong.khu_objects(khu_map)] == ["t_an", "t_ngoai", "t_trung"]
    assert chi_duong.khu_at(khu_map, 100, 100)[1]["khu"] == "t_an"          # listed first: the safe camp
    assert chi_duong.khu_at(khu_map, 900, 500)[1]["khu"] == "t_ngoai"
    assert chi_duong.khu_at(khu_map, 2000, 100)[1]["khu"] == "t_trung"
    rect, props = chi_duong.khu_at(khu_map, 2000, 100)
    d = chi_duong.khu_dest("thu", rect, props, "Vùng Thử")
    assert (d["khu"], d["x"], d["y"], d["band"], d["stage_min"], d["stage_max"]) == ("t_trung", 1920, 480, 2, 4, 6)


def test_walking_into_a_khu_shows_its_banner_and_warns_above_the_tu_vi(khu_map):
    g = FakeGame()
    nav = chi_duong.ChiDuong(g)
    nav.data = {"stage": {"realm": "luyen_khi", "realm_vi": "Luyện Khí", "stage": 1, "working": 2}}
    sc = FakeScene(khu_map, 900, 500)
    nav.update(sc)
    title, line, warn, _ = nav.banner
    assert title == "Ngoại Vi Thử" and line == "hợp Luyện Khí tầng 1-3" and not warn
    g.now += 1
    sc.player.x = 2000
    nav.update(sc)
    title, line, warn, _ = nav.banner
    assert title == "Trung Vực Thử" and warn and "cao hơn tu vi" in line
    g.now += 1
    sc.player.x, sc.player.y = 100, 100
    nav.update(sc)
    assert nav.banner[1] == "nơi an toàn" and not nav.banner[2]


def test_the_arrow_leads_to_a_khu_and_says_when_it_is_reached(khu_map):
    g = FakeGame()
    nav = chi_duong.ChiDuong(g)
    rect, props = chi_duong.khu_at(khu_map, 2000, 100)
    nav.dest = chi_duong.khu_dest("thu", rect, props, "Vùng Thử")
    sc = FakeScene(khu_map, 300, 500)
    for _ in range(200):
        g.now += 0.2
        nav.update(sc)
        if nav.status == "path":
            break
    assert nav.status == "path" and nav.arrow(sc) is not None
    assert nav.plate()[0].startswith("Trung Vực Thử (Vùng Thử) · ")
    sc.player.x = 1300                                          # walked into the khu
    g.now += 0.2
    nav.update(sc)
    assert nav.dest is None and g.toasts[-1] == "Đã tới Trung Vực Thử (Vùng Thử)."


def test_the_overview_has_one_pixel_per_tile_and_solids_darkened(khu_map):
    ov = minimap.overview(khu_map)
    assert ov.get_size() == (160, 60)
    assert sum(ov.get_at((37, 5))[:3]) < sum(ov.get_at((30, 5))[:3])     # tile 37 lies under the solid


def test_the_minimap_is_the_whole_small_map_or_a_window_on_a_giant_one(tmp_path):
    from client.engine.tilemap import TileMap
    small = TileMap(write_tmj(tmp_path / "small.tmj", 56, 36, [], []))
    mm = minimap.MiniMap(small)
    assert mm.whole and mm.size == (99, 64)                     # as large as the footprint allows, as before
    giant = TileMap(write_tmj(tmp_path / "giant.tmj", 320, 240, [], []))
    t = time.perf_counter()
    mm = minimap.MiniMap(giant)
    assert time.perf_counter() - t < 0.5
    assert not mm.whole and mm.size == (100, 64) and mm.k == 1 / 16
    mm.follow(2560, 1920)                                       # centred on the player
    assert mm.to_mm(2560, 1920) == (50.0, 32.0)
    mm.follow(10, 10)                                           # kept inside the map
    assert (mm.ox, mm.oy) == (0, 0)
    mm.follow(5120, 3840)
    assert (mm.ox, mm.oy) == (5120 - 1600, 3840 - 1024)
    assert mm.picture().get_size() == (100, 64)


# ------------------------------------------------------------------ the arrow and the strings
def test_the_arrow_has_an_outline_in_every_direction():
    from client.ui import nav_arrow
    for step in range(nav_arrow.STEPS):
        s = nav_arrow.sprite(step)
        colours = {tuple(s.get_at((x, y)))[:3] for x in range(s.get_width()) for y in range(s.get_height())
                   if s.get_at((x, y))[3] == 255}
        assert nav_arrow.EDGE in colours and nav_arrow.FILL in colours, step


def test_every_string_is_drawn_by_the_shipped_fonts():
    fonttools = pytest.importorskip("fontTools.ttLib")
    cmap = set(fonttools.TTFont(ROOT / "client" / "assets" / "fonts" / "VT323-Regular.ttf", fontNumber=0,
                                lazy=True).getBestCmap())
    from client import strings_nav_vi as N
    texts = [v for v in vars(N).values() if isinstance(v, str)] + list(N.BAND_NAMES.values())
    sys.path.insert(0, str(ROOT / "server"))
    from app.systems import navigation as sn
    learn = sn.Learning("luyen_khi", 3, "Luyện Khí", 9, {"ds": sn.BranchPos("luyen_khi", 4, "Ma trận")})
    lands = [{"id": "kiem_trung_son", "name_vi": "Kiếm Trủng Sơn", "branch": "ds", "kind": "wild",
              "realm": "luyen_khi", "zone": "z", "built": True, "open": True, "reason_vi": None}]
    khu = ({"id": "k", "name_vi": "Trung Vực", "band": 2, "stage_min": 4, "stage_max": 6, "anchor": [1, 2]},)
    out = sn.recommend(learn, lands, lambda z: khu, lambda z, n: (0, 0), {"luyen_khi": 1}, {"ds": "Đại Số"})
    texts += [out["recommended"]["reason_vi"], out["recommended"]["fit_vi"], out["home"]["reason_vi"],
              out["village"]["reason_vi"]]
    missing = {ch for t in texts for ch in t if not ch.isspace() and ord(ch) not in cmap}
    assert not missing, missing
