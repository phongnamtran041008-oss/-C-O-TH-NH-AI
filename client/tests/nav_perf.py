"""The cost of Chỉ Đường on the real giant lands, in the real game loop under the dummy driver
(a real server, the real world scene): docs/CHI_DUONG.md "Measured".

    python -m client.tests.nav_perf            # every land (nav_walk.world_lands); prints the numbers
    python -m client.tests.nav_perf ho_nghien_muc

* loading the map (`load_map`, a cold cache) and the bytes of its file;

* the frame time of the world scene (average, 95th percentile, worst) while following the arrow
  across the land (the time of `game.step`, the driver's sleep left out);
* the time from choosing a khu to the first arrow that follows the way (and in frames);
* one reading of the way (`Leg.read`), with and without the route for the maps;
* building the overview, a minimap window frame, opening the big map and drawing it;
* the memory held by the map's surfaces (ground chunks, overview, minimap) and by the walk grid
  and field;
* the world HUD's icon rows (`draw_ability_row`, `draw_hotbar`) timed inside every walking
  frame: their share of the slow frames (the rare frames over 25 ms).
"""
from __future__ import annotations

import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.engine import chi_duong, minimap, navigator as nv
from client.engine.tilemap import load_map
from client.tests.driver import Driver, ServerProcess
from client.tests.nav_walk import keys_for
from client.tests.test_combat_flow import CARD
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_world_flow import make_account

KEYS = {(1, 0): [pygame.K_d], (-1, 0): [pygame.K_a], (0, 1): [pygame.K_s], (0, -1): [pygame.K_w]}


def timed_steps(drv: Driver, n: int, out: list) -> None:
    """n frames of the game, each timed (the driver's own sleep is not part of a frame)."""
    for _ in range(n):
        now = time.perf_counter()
        dt = min(0.1, max(1 / 240, now - getattr(drv, "_last", now - 1 / 60)))
        drv._last = now
        t = time.perf_counter()
        drv.game.step(dt, [])
        out.append(time.perf_counter() - t)
        time.sleep(0.004)


def surface_bytes(s) -> int:
    return s.get_width() * s.get_height() * s.get_bytesize() if s is not None else 0


def measure_land(zone: str, workdir: Path, seconds: float = 40.0) -> dict:
    import os
    if os.environ.get("NAV_PERF_OLD_ICONS"):         # the hotbar as it was: every icon scaled each frame
        from client.scenes import world as W
        from client.ui.kit import UI
        W.hud_icon = lambda ui, img, x, y, zoom, key=None: UI.image(ui, img, x, y, zoom=zoom, anchor="center")
    server = ServerProcess(workdir)
    facts: dict = {"zone": zone}
    try:
        token, uid = make_account(server.url, "detu_do", "Lữ Khách")
        from client.tests.test_lands_flow import grant_luyen_khi       # every land open, the hotbar full
        grant_luyen_khi(server, uid)
        server.sql("update characters set realm='luyen_khi', realm_stage=9 where user_id=?", (uid,))
        from client.engine import tilemap
        tilemap._MAPS.pop(zone, None)
        t = time.perf_counter()
        tm = load_map(zone)                                # the file read and parsed, the collider, no drawing
        facts["map_load_ms"] = (time.perf_counter() - t) * 1000
        from client.config import assets_dir
        facts["map_file_kb"] = (assets_dir() / "maps" / f"{zone}.tmj").stat().st_size / 1024
        x, y = next((o.x, o.y) for o in tm.find("spawn") if o.name == "from_village")
        server.sql("update characters set zone_id=?, x=?, y=? where user_id=?", (zone, x, y, uid))
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_do",
                                                          "server_url": server.url}))
        drv = Driver(server.url, workdir)
        drv.click("menu_start")
        ws = None

        def world():
            return next((s for s in drv.game.scenes if type(s).__name__ == "WorldScene"), None)
        drv.wait(lambda: world() is not None and world().joined, 20, "the land")
        drv.wait_api()
        ws = world()
        nav = chi_duong.of(drv.game)
        drv.wait(lambda: nav.data is not None, 10, "the destinations")
        idle: list = []
        timed_steps(drv, 120, idle)
        facts["idle_frame_ms"] = (statistics.mean(idle) * 1000, max(idle) * 1000)
        # ---- the nearest khu of band 1 (a newcomer's), the grid not built yet: the first arrow
        khus = chi_duong.khu_objects(ws.map)
        if not khus:                                       # Lôi Kiếp Đài: its named places stand in for khu
            khus = [((o.x, o.y, o.w, o.h), {"khu": "", "name_vi": o.props.get("name_vi", ""), "band": b,
                                             "anchor_x": int(o.x + 8), "anchor_y": int(o.y + 28)})
                    for o in ws.map.find("poi") for b in ("1", "3") if o.props.get("poi") in ("landmark", "boss")]
        rect, props = min((k for k in khus if k[1].get("band") == "1"),
                          key=lambda k: abs(int(k[1]["anchor_x"]) - x) + abs(int(k[1]["anchor_y"]) - y))
        nv._GRIDS.clear()
        t0 = time.perf_counter()
        nav.set_dest(chi_duong.khu_dest(zone, rect, props, ""), zone)
        frames = []
        while nav.status != "path" and len(frames) < 2000:
            timed_steps(drv, 1, frames)
        facts["first_arrow_band1_s"] = time.perf_counter() - t0
        facts["first_arrow_band1_frames"] = len(frames)
        while not nav.leg.ready:
            timed_steps(drv, 1, frames)
        facts["band1_search_frame_worst_ms"] = max(frames) * 1000
        # ---- the farthest khu of band 3: chosen as on the big map
        rect, props = max((k for k in khus if k[1].get("band") == "3"),
                          key=lambda k: abs(int(k[1]["anchor_x"]) - x) + abs(int(k[1]["anchor_y"]) - y))
        nv._GRIDS.clear()                                  # as on the first choice after entering the land
        t0 = time.perf_counter()
        nav.set_dest(chi_duong.khu_dest(zone, rect, props, ""), zone)
        frames: list = []
        while nav.status != "path" and len(frames) < 2000:
            timed_steps(drv, 1, frames)
        facts["first_arrow_s"] = time.perf_counter() - t0
        facts["first_arrow_frames"] = len(frames)
        facts["search_frame_worst_ms"] = max(frames) * 1000
        facts["grid_ms"] = nav.leg.grid_job.spent * 1000 if nav.leg.grid_job else 0.0
        facts["field_ms"] = nav.leg.job.spent * 1000
        facts["field_longest_slice_ms"] = nav.leg.job.longest * 1000
        # ---- one reading
        n = 200
        t = time.perf_counter()
        for _ in range(n):
            nav.leg.read(ws.player.x, ws.player.y)
        facts["read_ms"] = (time.perf_counter() - t) / n * 1000
        t = time.perf_counter()
        for _ in range(20):
            nav.leg.read(ws.player.x, ws.player.y, route_cells=chi_duong.ROUTE_CELLS)
        facts["read_route_ms"] = (time.perf_counter() - t) / 20 * 1000
        # ---- walk by the arrow, every frame timed
        walk: list = []
        hud: list = []                                     # (frame index, ms in the two icon rows)
        cls = type(ws)
        orig = {n: getattr(cls, n) for n in ("draw_ability_row", "draw_hotbar")}
        spent = [0.0]

        def timed(fn):
            def wrap(self, *a, **k):
                t = time.perf_counter()
                try:
                    return fn(self, *a, **k)
                finally:
                    spent[0] += time.perf_counter() - t
            return wrap
        for n, fn in orig.items():
            setattr(cls, n, timed(fn))
        end = time.time() + seconds
        x0, y0 = ws.player.x, ws.player.y
        while time.time() < end and nav.dest is not None:
            if drv.top_is(CARD):
                answer_card(drv, server, correct=True)
                drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes")
                continue
            if nav.reading is None or drv.game.top is not ws:
                timed_steps(drv, 2, walk)
                continue
            ax, ay = nav.reading.aim
            kx, ky = keys_for(ax - ws.player.x, ay - ws.player.y)
            drv.keys.held = set(KEYS.get((kx, 0), []) + KEYS.get((0, ky), []))
            for _ in range(6):
                spent[0] = 0.0
                timed_steps(drv, 1, walk)
                hud.append(spent[0])
        drv.keys.held = set()
        for n, fn in orig.items():
            setattr(cls, n, fn)
        pairs = list(zip(walk[-len(hud):], hud)) if hud else []
        slow = [(f, h) for f, h in pairs if f > 0.025]
        facts["hud_rows_ms"] = (statistics.mean(h for _f, h in pairs) * 1000 if pairs else 0.0,
                                max((h for _f, h in pairs), default=0.0) * 1000)
        facts["slow_frames"] = len(slow)
        facts["slow_frames_hud_share"] = (sum(h for _f, h in slow) / max(1e-9, sum(f for f, _h in slow))) if slow else 0.0
        facts["walked_px"] = abs(ws.player.x - x0) + abs(ws.player.y - y0)
        walk.sort()
        facts["walk_frames"] = len(walk)
        facts["walk_frame_ms"] = (statistics.mean(walk) * 1000, walk[int(len(walk) * 0.95)] * 1000,
                                  walk[-1] * 1000)
        # ---- the minimap and the big map
        minimap._OVERVIEWS.clear()
        t = time.perf_counter()
        ov = minimap.overview(ws.map)
        facts["overview_ms"] = (time.perf_counter() - t) * 1000
        ui = drv.game.ui
        m2 = minimap.MiniMap(ws.map)
        ui.begin([], 1 / 60)
        t = time.perf_counter()
        for _ in range(50):
            m2.draw(ui, 376, 4, ws)
        facts["minimap_frame_ms"] = (time.perf_counter() - t) / 50 * 1000
        ui.end()
        from client.scenes.world_map import WorldMapScene
        t = time.perf_counter()
        big = WorldMapScene(drv.game, ws)
        drv.game.push(big)
        opening: list = []
        timed_steps(drv, 1, opening)
        facts["big_map_open_ms"] = (time.perf_counter() - t) * 1000
        frames = []
        timed_steps(drv, 60, frames)
        facts["big_map_frame_ms"] = (statistics.mean(frames) * 1000, max(frames) * 1000)
        drv.game.pop()
        timed_steps(drv, 2, [])
        # ---- memory
        from client.engine import tilemap
        facts["ground_chunks_mb"] = tilemap.ground_bytes(ws.map) / 2 ** 20
        facts["chunk_cache_mb"] = tilemap.cache_bytes() / 2 ** 20
        facts["overview_kb"] = surface_bytes(ov) / 1024
        facts["big_map_picture_kb"] = surface_bytes(big.zone_layout()[0]) / 1024
        g = nv.grid_for(ws.map)
        facts["walk_grid_kb"] = len(g.walk) / 1024
        facts["field_kb"] = len(nav.leg.field.dist) * nav.leg.field.dist.itemsize / 1024 if nav.leg and nav.leg.field else 0
        drv.close()
    finally:
        server.stop()
    return facts


def main() -> None:
    from client.tests.nav_walk import world_lands
    for zone in sys.argv[1:] or world_lands():
        with tempfile.TemporaryDirectory(prefix="kvtt_navperf_") as tmp:
            try:
                f = measure_land(zone, Path(tmp))
            except AssertionError as e:
                print(f"{zone:12} FAILED {str(e)[:300]}")
                continue
        for k, v in f.items():
            if isinstance(v, tuple):
                v = " / ".join(f"{a:.2f}" for a in v)
            elif isinstance(v, float):
                v = f"{v:.2f}"
            print(f"{zone:12} {k:24} {v}")


if __name__ == "__main__":
    main()
