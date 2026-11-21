"""A synthetic giant land (320 x 240 tiles) with khu, gates and named places, for Chỉ Đường's
tests and pictures until the real giant maps arrive: `write_giant(path)` writes the .tmj,
`GiantScene` shows it with the world HUD's minimap, plate and arrow (no server needed).

    python -m client.tests.nav_giant <dir>      # giant_*.png: the minimap window, the big map
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pygame

TW, TH = 320, 240
GID = {"grass": 1, "flowers": 4, "path": 6, "water": 8, "stone": 10, "dirt": 14, "dark_grass": 15, "ink": 17}


def write_giant(path: Path, seed: int = 11) -> Path:
    rng = random.Random(seed)
    g = [GID["grass"]] * (TW * TH)

    def put(x, y, name):
        if 0 <= x < TW and 0 <= y < TH:
            g[y * TW + x] = GID[name]

    for _ in range(900):                                  # patches of ground
        cx, cy, r = rng.randrange(TW), rng.randrange(TH), rng.randrange(2, 7)
        kind = "dark_grass" if cy < 80 else ("dirt" if cy < 160 else rng.choice(["flowers", "dark_grass"]))
        for y in range(cy - r, cy + r):
            for x in range(cx - r, cx + r):
                if (x - cx) ** 2 + (y - cy) ** 2 < r * r:
                    put(x, y, kind)
    for y in range(0, 80):                                # the deep north is stone and ink
        for x in range(TW):
            if rng.random() < 0.35:
                put(x, y, "stone" if rng.random() < 0.8 else "ink")
    water = set()
    for x in range(TW):                                   # a river across the middle, two bridges
        y0 = 118 + int(6 * __import__("math").sin(x / 17))
        for y in range(y0, y0 + 5):
            if x in range(70, 74) or x in range(230, 234):
                put(x, y, "path")
            else:
                put(x, y, "water")
                water.add((x, y))
    for y in range(TH):                                   # paths
        put(72, y, "path")
        put(232, y, "path") if y < 200 else None
    for x in range(20, 300):
        put(x, 200, "path")
        put(x, 60, "path")
    solids = []
    for y in range(TH):                                   # water rows as solid runs
        x = 0
        while x < TW:
            if (x, y) in water:
                x0 = x
                while x < TW and (x, y) in water:
                    x += 1
                solids.append((x0 * 16, y * 16, (x - x0) * 16, 16))
            else:
                x += 1
    for _ in range(2500):                                 # rocks and trees, off the paths
        x, y = rng.randrange(TW), rng.randrange(TH)
        if g[y * TW + x] != GID["path"] and (x, y) not in water and not (150 < x < 170 and y > 225):
            solids.append((x * 16 + 2, y * 16 + 6, 12, 8))

    def khu(oid, x, y, w, h, kid, name, band, lo, hi, ax, ay):
        props = {"khu": kid, "name_vi": name, "band": band, "stage_min": lo, "stage_max": hi,
                 "anchor_x": ax, "anchor_y": ay, "realm": "luyen_khi"}
        return {"id": oid, "name": kid, "type": "khu", "x": x, "y": y, "width": w, "height": h,
                "properties": [{"name": k, "type": "string", "value": str(v)} for k, v in props.items()]}

    def poi(oid, x, y, kind, name):
        return {"id": oid, "name": name, "type": "poi", "x": x, "y": y, "width": 16, "height": 16,
                "properties": [{"name": "poi", "type": "string", "value": kind},
                               {"name": "name_vi", "type": "string", "value": name}]}
    objs = [khu(1, 2400, 3500, 480, 340, "thu_trai", "Trại Kiếm Khách", 0, 0, 0, 2560, 3620),
            khu(2, 0, 2560, 5120, 1280, "thu_ngoai", "Ngoại Vi", 1, 1, 3, 1160, 3200),
            khu(3, 0, 1280, 5120, 1280, "thu_trung", "Trung Vực", 2, 4, 6, 3720, 1600),
            khu(4, 0, 0, 5120, 1280, "thu_tham", "Thâm Xứ", 3, 7, 9, 1160, 960),
            {"id": 5, "name": "to_village", "type": "portal", "x": 2528, "y": 3826, "width": 64, "height": 26,
             "properties": [{"name": "target", "type": "string", "value": "truc_lam_thon"},
                            {"name": "target_spawn", "type": "string", "value": "from_loan_so_coc"}]},
            {"id": 6, "name": "spawn", "type": "spawn", "x": 2560, "y": 3780, "width": 1, "height": 1},
            {"id": 7, "name": "from_village", "type": "spawn", "x": 2560, "y": 3780, "width": 1, "height": 1},
            poi(8, 1150, 960, "bi_canh", "Kiếm Mộ Bí Cảnh"), poi(9, 3700, 1580, "camp", "Trại Trung Vực"),
            poi(10, 4600, 400, "boss", "Kiếm Hồn Đài"), poi(11, 600, 3000, "beast", "Hang Linh Hồ")]
    data = {"width": TW, "height": TH, "tilewidth": 16, "tileheight": 16, "properties": [],
            "layers": [{"type": "tilelayer", "name": "ground", "data": g},
                       {"type": "objectgroup", "name": "objects", "objects": objs},
                       {"type": "objectgroup", "name": "collision",
                        "objects": [{"id": 1000 + i, "name": "", "type": "solid", "x": x, "y": y, "width": w,
                                     "height": h} for i, (x, y, w, h) in enumerate(solids)]}]}
    path.write_text(json.dumps(data), "utf-8")
    return path


class GiantScene:
    """Just enough of a world scene for the minimap, the plate, the arrow and Thiên Địa Đồ."""
    draws_world = True
    modal = False
    opaque = False
    toast_y = 70
    realm = None

    def __init__(self, game, tmap, zone: str, x: float, y: float):
        from client.engine.minimap import MiniMap
        from client.engine.view import View
        self.game, self.map, self.zone_id = game, tmap, zone
        self.player = type("P", (), {"x": x, "y": y})()
        self.entities, self.sniffed = {}, []
        self.mm = MiniMap(tmap)
        self.minimap = self.mm.frame
        self.view = View(1)

    def world_to_screen(self, x, y):
        return self.view.to_screen(x, y)

    def on_enter(self): ...
    def on_exit(self): ...
    def on_resume(self): ...
    def update(self, dt, top): ...

    def draw_world(self, surf):
        w, h = surf.get_size()
        cx = int(max(0, min(self.map.px_w - w, self.player.x - w / 2)))
        cy = int(max(0, min(self.map.px_h - h, self.player.y - 12 - h / 2)))
        self.view.ox, self.view.oy = cx, cy
        self.map.draw_ground(surf, (cx, cy), 0)
        for r in self.map.solids:
            if r.colliderect(pygame.Rect(cx, cy, w, h)) and r.w < 16:
                pygame.draw.rect(surf, (60, 52, 44), r.move(-cx, -cy))
        sx, sy = self.view.to_screen(self.player.x, self.player.y)
        pygame.draw.rect(surf, (240, 220, 180), (sx - 4, sy - 16, 8, 16))
        from client.ui import nav_hud
        nav_hud.draw_world(surf, self)

    def draw_ui(self, ui):
        mw, mh = self.minimap.get_size()
        self.mm.draw(ui, 476 - mw, 4, self)
        from client.ui import nav_hud
        nav_hud.hud(ui, self, self.game.top is self)


def run_giant_screens(workdir: Path, shots: Path | None = None) -> dict:
    """Lead to the Thâm Xứ of the giant land across the river: the minimap window, the arrow and
    Thiên Địa Đồ. Returns a few facts for the test."""
    from client.config import Config, Session
    from client.engine import chi_duong
    from client.engine.tilemap import TileMap
    from client.main import Game
    from client.scenes.world_map import WorldMapScene
    game = Game(Config(server_url="http://127.0.0.1:9"), Session(workdir / "s.json"), size=(1440, 810))
    tmap = TileMap(write_giant(workdir / "dai_dia_thu.tmj"))
    sc = GiantScene(game, tmap, "dai_dia_thu", 2560, 3700)
    game.replace_all(sc)
    nav = chi_duong.of(game)
    nav.data = {"stage": {"realm": "luyen_khi", "realm_vi": "Luyện Khí", "stage": 3, "working": 4}}
    rect, props = next(k for k in chi_duong.khu_objects(tmap) if k[1]["khu"] == "thu_tham")
    nav.dest = chi_duong.khu_dest("dai_dia_thu", rect, props, "Đại Địa Thử")
    frames, worst = 0, 0.0
    import time
    while nav.status != "path" and frames < 600:
        t = time.perf_counter()
        game.step(1 / 60, [])
        worst = max(worst, time.perf_counter() - t)
        frames += 1
    for _ in range(40):
        game.step(1 / 60, [])
    out = {"frames": frames, "status": nav.status, "route": len(nav.route), "search_s": nav.leg.job.spent,
           "grid_s": nav.leg.grid_job.spent if nav.leg.grid_job else 0.0}
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
        pygame.image.save(game.display.window, str(shots / "giant_minimap_arrow.png"))
    game.push(WorldMapScene(game, sc))
    for _ in range(6):
        game.step(1 / 60, [])
    if shots:
        pygame.image.save(game.display.window, str(shots / "giant_map_zone.png"))
    sc.player.x, sc.player.y = 3720, 1700                  # in the Trung Vực, past the river
    nav.khu_check_t = -1e9
    game.pop()
    for _ in range(30):
        game.step(1 / 60, [])
    out["banner"] = nav.banner
    if shots:
        pygame.image.save(game.display.window, str(shots / "giant_khu_banner.png"))
    game.running = False
    game.shutdown()
    return out


if __name__ == "__main__":
    import tempfile
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "nav"
    with tempfile.TemporaryDirectory() as tmp:
        print({k: v for k, v in run_giant_screens(Path(tmp), dest).items() if k != "banner"})
