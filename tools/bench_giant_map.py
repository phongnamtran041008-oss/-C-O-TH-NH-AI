"""Benchmark of the engine on a giant map (Đại Địa Đồ: 320 x 240 tiles).

Builds a synthetic land - mixed ground with lakes, paths, dirt and dark grass, ~6,000 props,
~4,000 collision rectangles, ~260 monsters in their areas, khu and poi objects - in a temporary
folder (never in the assets) and measures:

  client  map load time, memory held by the map's surfaces, average / worst frame of the world
          draw while the camera walks across the map, at zoom 1 (old art) and zoom 2 (v2 art),
          next to the same walk on one of today's small maps (SDL dummy driver);
  server  map parse time, channel creation time, average / worst tick (World.tick with its
          snapshots) with 1, 10 and 40 players spread over the map, walking.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" tools/bench_giant_map.py [--frames N] [--ticks N]
    ... tools/bench_giant_map.py --zone ho_nghien_muc     # a real land instead of the synthetic one
    ... tools/bench_giant_map.py --zone all               # every map the server ships, in turn
    ... tools/bench_giant_map.py --zone ho_nghien_muc --map old.tmj   # an older file of that zone
    ... tools/bench_giant_map.py --startup                # the server's start-up: every map preloaded

With `--zone` the map is the shipped one (client/assets/maps and server/maps), the server runs it
as that zone (its real monsters, lands, khu), and the client walks it with the real art.

Each part runs in its own process so the memory numbers do not mix. The minimap of the world
scene (`WorldScene._build_minimap`) is stubbed out: it is being replaced by a 1-px-per-tile
overview and is not part of the engine's budget.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W_TILES, H_TILES, TILE = 320, 240, 16
SMALL_MAP = "loan_so_coc"
ZONE = "rung_muc_loang"        # the zone id the synthetic land runs as on the server (a starter land)

PROPS = [("ink_tree", 32, 40, 30), ("bamboo", 16, 40, 22), ("tree", 32, 40, 14), ("pine", 32, 40, 10),
         ("peach", 32, 40, 8), ("rock", 16, 12, 5), ("tall_grass", 24, 16, 4), ("bush", 24, 16, 3),
         ("lantern", 8, 24, 1), ("boulder", 32, 24, 1), ("crystal", 24, 32, 1), ("house", 48, 48, 1)]
MONSTERS = ["ink_slime", "tone_wisp", "ink_fox", "moc_yeu"]


# ------------------------------------------------------------------ the synthetic map
def make_map(folder: Path, seed: int = 7) -> Path:
    sys.path.insert(0, str(ROOT))
    from client.art import build as B
    names = [n for n, _ in B.TILESET]

    def gid(name, k=0):
        ids = [i + 1 for i, n in enumerate(names) if n == name]
        return ids[k % len(ids)]
    rng = random.Random(seed)
    w, h = W_TILES, H_TILES
    g = [gid("grass", rng.randrange(3)) for _ in range(w * h)]

    def blob(name, cx, cy, rx, ry, k=None):
        for y in range(max(0, cy - ry), min(h, cy + ry + 1)):
            for x in range(max(0, cx - rx), min(w, cx + rx + 1)):
                if ((x - cx) / max(1, rx)) ** 2 + ((y - cy) / max(1, ry)) ** 2 <= 1.0:
                    g[y * w + x] = gid(name, rng.randrange(2) if k is None else k)
    for _ in range(60):
        blob("dark_grass", rng.randrange(w), rng.randrange(h), rng.randint(6, 22), rng.randint(5, 16))
    for _ in range(400):
        blob("flowers", rng.randrange(w), rng.randrange(h), rng.randint(0, 2), rng.randint(0, 2))
    for _ in range(250):
        blob("dirt", rng.randrange(w), rng.randrange(h), rng.randint(0, 3), rng.randint(0, 2), 0)
    for _ in range(80):
        blob("stone", rng.randrange(w), rng.randrange(h), rng.randint(0, 2), rng.randint(0, 2))
    lakes = []
    for _ in range(36):
        cx, cy, rx, ry = rng.randrange(10, w - 10), rng.randrange(10, h - 10), rng.randint(3, 12), rng.randint(3, 9)
        if abs(cx - w // 2) < 20 and abs(cy - h // 2) < 16:
            continue
        blob("water", cx, cy, rx, ry, 0)
        lakes.append((cx, cy, rx, ry))
    for _ in range(24):                        # paths: random walks, one or two tiles wide
        x, y = rng.randrange(w), rng.randrange(h)
        dx, dy = rng.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        for _ in range(rng.randint(40, 160)):
            if 0 <= x < w and 0 <= y < h and names[g[y * w + x] - 1] != "water":
                g[y * w + x] = gid("path", rng.randrange(2))
            if rng.random() < 0.15:
                dx, dy = rng.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            x, y = x + dx, y + dy
    objects, solids = [], []
    oid = [0]

    def obj(name, otype, x, y, ow, oh, props=None):
        oid[0] += 1
        objects.append({"id": oid[0], "name": name, "type": otype, "x": x, "y": y, "width": ow, "height": oh,
                        "rotation": 0, "visible": True,
                        "properties": [{"name": k, "type": "string", "value": str(v)} for k, v in (props or {}).items()]})
    px_w, px_h = w * TILE, h * TILE
    sx, sy = px_w // 2, px_h // 2
    obj("spawn", "spawn", sx, sy, 0, 0)
    weights = [p[3] for p in PROPS]
    placed = 0
    while placed < 6000:
        name, ow, oh, _ = rng.choices(PROPS, weights)[0]
        x, y = rng.randrange(0, px_w - ow), rng.randrange(0, px_h - oh)
        if abs(x - sx) < 160 and abs(y - sy) < 120:
            continue
        tx, ty = (x + ow // 2) // TILE, (y + oh - 1) // TILE
        if names[g[ty * w + tx] - 1] == "water":
            continue
        obj(name, "prop", x, y, ow, oh, {"sprite": name, "variant": rng.randrange(1000)})
        placed += 1
        if len(solids) < 3400 and name not in ("tall_grass", "bush"):
            solids.append((x + ow // 2 - 4, y + oh - 7, 9, 7))
    for cx, cy, rx, ry in lakes:              # the shores are solid
        for k in range(16):
            a = k / 16 * 6.283
            solids.append((int((cx + math.cos(a) * rx) * TILE) - 8, int((cy + math.sin(a) * ry) * TILE) - 8, 16, 16))
        obj(f"ho_{cx}_{cy}", "area", (cx - rx) * TILE, (cy - ry) * TILE, rx * 2 * TILE, ry * 2 * TILE, {"kind": "pond"})
    while len(solids) < 4000:                 # walls and fences
        x, y = rng.randrange(0, px_w - 64), rng.randrange(0, px_h - 64)
        if abs(x - sx) < 200 and abs(y - sy) < 150:
            continue
        solids.append((x, y, rng.choice([16, 32, 48, 64]), rng.choice([8, 16])))
    for i in range(20):
        obj(f"bia_{i}", "sign", rng.randrange(64, px_w - 64), rng.randrange(64, px_h - 64), 16, 20,
            {"sprite": "sign", "text": f"Bia đá số {i}"})
    for i, look in enumerate(("guide", "smith", "merchant", "elder", "guide", "smith")):
        obj(f"npc_{i}", "npc", rng.randrange(64, px_w - 64), rng.randrange(64, px_h - 64), 16, 24, {"npc": look})
    for i, (px, py) in enumerate(((16, 16), (px_w - 80, 16), (16, px_h - 40), (px_w - 80, px_h - 40))):
        obj(f"cong_{i}", "portal", px, py, 64, 26, {"target": "truc_lam_thon", "target_spawn": "from_forest"})
    total = 0
    k = 0
    while total < 260:                         # monster areas over the whole map
        x, y = rng.randrange(64, px_w - 260), rng.randrange(64, px_h - 200)
        if abs(x - sx) < 300 and abs(y - sy) < 220:
            continue
        n = min(5, 260 - total)
        obj(f"a{k}", "monster_area", x, y, 192, 160, {"monster": MONSTERS[k % len(MONSTERS)], "count": n,
                                                     "khu": f"bench_khu_{k % 9}", "band": 1 + k % 3})
        total += n
        k += 1
    for i in range(9):                        # khu: a 3 x 3 cut of the land; rectangles with properties only
        kx, ky = i % 3, i // 3
        obj(f"bench_khu_{i}", "khu", kx * px_w // 3, ky * px_h // 3, px_w // 3, px_h // 3,
            {"khu": f"bench_khu_{i}", "name_vi": f"Khu {i}", "band": 1 + i % 3, "realm": "luyen_khi",
             "stage_min": 1, "stage_max": 3, "anchor_x": kx * px_w // 3 + 200, "anchor_y": ky * px_h // 3 + 200})
    for i in range(30):
        obj(f"poi_{i}", "poi", rng.randrange(0, px_w - 64), rng.randrange(0, px_h - 64), 48, 48,
            {"poi": "landmark", "name_vi": f"Danh thắng {i}"})
    coll = [{"id": 100000 + i, "name": "", "type": "solid", "x": x, "y": y, "width": cw, "height": chh,
             "rotation": 0, "visible": True} for i, (x, y, cw, chh) in enumerate(solids)]
    doc = {"width": w, "height": h, "tilewidth": TILE, "tileheight": TILE, "orientation": "orthogonal",
           "renderorder": "right-down", "type": "map", "infinite": False, "version": "1.10",
           "properties": [{"name": "zone", "type": "string", "value": "bench_giant"}],
           "tilesets": [{"firstgid": 1, "name": "tiles", "tilewidth": 16, "tileheight": 16, "tilecount": len(names)}],
           "layers": [{"type": "tilelayer", "name": "ground", "width": w, "height": h, "data": g},
                      {"type": "objectgroup", "name": "objects", "objects": objects},
                      {"type": "objectgroup", "name": "collision", "objects": coll}]}
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "bench_giant.tmj"
    path.write_text(json.dumps(doc), "utf-8")
    return path


# ------------------------------------------------------------------ memory of this process
def working_set_mb() -> tuple[float, float]:
    """(current, peak) working set of this process in MB (Windows; (0, 0) elsewhere)."""
    if os.name != "nt":
        return 0.0, 0.0
    import ctypes
    from ctypes import wintypes

    class PMC(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
    c = PMC()
    c.cb = ctypes.sizeof(PMC)
    psapi = ctypes.WinDLL("psapi")
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
    k32 = ctypes.WinDLL("kernel32")
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return c.WorkingSetSize / 2 ** 20, c.PeakWorkingSetSize / 2 ** 20


def surface_mb(tm) -> float:
    """MB of pixels the map holds in surfaces (the ground pictures and their chunk caches)."""
    import pygame
    from client.engine import tilemap
    if hasattr(tilemap, "ground_bytes"):
        return tilemap.ground_bytes(tm) / 2 ** 20
    total = 0
    for v in vars(tm).values():
        if isinstance(v, pygame.Surface):
            total += v.get_width() * v.get_height() * v.get_bytesize()
    return total / 2 ** 20


# ------------------------------------------------------------------ client
def client_part(zoom: int, path: Path | None, frames: int, zone_id: str = "") -> dict:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    sys.path.insert(0, str(ROOT))
    import pygame
    from client.engine import art2, tilemap
    if zoom == 1:
        art2.set_root(Path(tempfile.mkdtemp(prefix="bench_noart_")))    # a checkout without the v2 art
    from client.config import Config
    from client.main import Game
    from client.config import Session
    from client.scenes import world as W
    out: dict = {"zoom": zoom, "map": "giant" if path else SMALL_MAP}
    work = Path(tempfile.mkdtemp(prefix="bench_client_"))
    game = Game(Config(server_url="http://127.0.0.1:9"), Session(work / "session.json"), size=(480, 270))
    game.state.character = {"facing": "down", "appearance": {}, "realm": "luyen_khi"}
    game.state.me = {"id": 1}
    game.state.cult = {"stats": {}}
    t0 = time.perf_counter()
    if zone_id:                                # a real zone (its shipped map, or the file given)
        zone = zone_id
        tilemap._MAPS.pop(zone, None)
        tm = tilemap.TileMap(path) if path is not None else tilemap.load_map(zone)
        tilemap._MAPS[zone] = tm
        out["map"] = zone
    elif path is not None:
        tm = tilemap.TileMap(path)
        zone = "bench_giant"
        tilemap._MAPS[zone] = tm
    else:
        zone = SMALL_MAP
        tilemap._MAPS.pop(zone, None)
        tm = tilemap.load_map(zone)
    out["load_s"] = time.perf_counter() - t0
    W.WorldScene._build_minimap = lambda self: (setattr(self, "mm_k", 0.01), pygame.Surface((4, 4)))[1]
    t0 = time.perf_counter()
    scene = W.WorldScene(game, zone)
    out["scene_s"] = time.perf_counter() - t0
    surf = pygame.Surface((480, 270))
    # the walk: corner to corner, then back along the middle; 4 world px a frame (240 px/s at 60 fps)
    pw, ph = tm.px_w, tm.px_h
    pts = [(120, 120), (pw - 120, ph - 120), (pw - 120, ph / 2), (120, ph / 2)]
    if path is None and not zone_id or pw < 2000:       # a small map: back and forth over it
        pts = [(100, 100), (pw - 100, ph - 100), (100, ph - 100), (pw - 100, 100)] * 3
    route = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(bx - ax, by - ay) / 4))
        route += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(n)]
    route = route[:frames]
    times, net = [], []
    t_first = None
    stats = getattr(tilemap, "STATS", None)
    for i, (x, y) in enumerate(route):
        scene.player.x, scene.player.y = x, y
        scene.player.moving = True
        scene.t += 1 / 60
        game.now += 1 / 60
        b0 = stats["build_s"] if stats else 0.0
        t0 = time.perf_counter()
        scene.draw_world(surf)
        scene._check_portals()
        scene.find_target()
        dt = time.perf_counter() - t0
        if t_first is None:
            t_first = dt
        else:
            times.append(dt)
            net.append(dt - ((stats["build_s"] - b0) if stats else 0.0))
    times.sort()
    out["net_avg_ms"] = sum(net) / max(1, len(net)) * 1000 if stats else None
    out["frames"] = len(times) + 1
    out["first_ms"] = (t_first or 0) * 1000
    out["avg_ms"] = sum(times) / max(1, len(times)) * 1000
    out["p99_ms"] = times[int(len(times) * 0.99)] * 1000 if times else 0
    out["worst_ms"] = times[-1] * 1000 if times else 0
    out["surface_mb"] = surface_mb(tm)
    out["ws_mb"], out["peak_ws_mb"] = working_set_mb()
    return out


# ------------------------------------------------------------------ server
def server_part(path: Path, ticks: int, zone_id: str = "") -> dict:
    db = Path(tempfile.mkdtemp(prefix="bench_db_")) / "bench.db"
    os.environ.setdefault("DATABASE_URL", f"sqlite+aiosqlite:///{db}")
    os.environ.setdefault("ENV", "dev")
    os.environ.setdefault("ALLOW_UNREVIEWED", "1")
    os.environ.setdefault("AUTO_MIGRATE", "0")
    sys.path.insert(0, str(ROOT / "server"))
    from app.realtime import maps
    from app.realtime import world as wmod
    from app.realtime.world import Session, World
    from app.realtime.zone import ChannelZone
    out: dict = {}
    ZONE = zone_id or globals()["ZONE"]
    t0 = time.perf_counter()
    zmap = maps.parse(path)
    out["parse_s"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    ChannelZone(ZONE, 1, zmap, random.Random(1))
    out["channel_s"] = time.perf_counter() - t0
    for n in (1, 10, 40):
        class Mono:
            t = 1000.0

            def __call__(self):
                return self.t
        mono = Mono()
        w = World(mono=mono)
        wmod.world = w
        ch = ChannelZone(ZONE, 1, zmap, random.Random(2))
        out["monsters"] = len(ch.monsters)
        w.channels[ZONE] = [ch]
        rng = random.Random(3)
        sessions = []
        for uid in range(1, n + 1):
            s = Session(uid, f"bench{uid}", f"Đạo Hữu {uid}", "luyen_khi", {"hair_color": "#2B2B2B"})
            s.sent = []
            s.hp, s.qi = 1e9, 1e9
            s.stats = {"max_hp": 1e9, "max_qi": 1e9, "atk": 20, "def": 1}
            w.sessions[uid] = s
            for _ in range(200):
                x, y = rng.uniform(64, zmap.width_px - 64), rng.uniform(64, zmap.height_px - 64)
                if not zmap.collider.blocked(x, y):
                    break
            w.put(s, ch, x, y, "down")
            sessions.append(s)
        dt = 0.05
        times = []
        seq = {s.user_id: 0 for s in sessions}
        dirs = {s.user_id: (1, 0) for s in sessions}
        for i in range(ticks + 20):
            for s in sessions:                 # everyone walks, turning now and then
                if rng.random() < 0.05:
                    dirs[s.user_id] = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)])
                dx, dy = dirs[s.user_id]
                ch.queue_input(s.player, seq[s.user_id], [(dx, dy, 50)])
                seq[s.user_id] += 1
            mono.t += dt
            t0 = time.perf_counter()
            w.tick(dt)
            el = time.perf_counter() - t0
            if i >= 20:
                times.append(el)
            for s in sessions:
                s.sent.clear()
        times.sort()
        out[f"tick_{n}"] = {"avg_ms": sum(times) / len(times) * 1000, "p99_ms": times[int(len(times) * 0.99)] * 1000,
                            "worst_ms": times[-1] * 1000}
    return out


def startup_part() -> dict:
    """The server's start-up: every zone map parsed and channel 1 opened (World.preload), timed."""
    db = Path(tempfile.mkdtemp(prefix="bench_db_")) / "bench.db"
    os.environ.setdefault("DATABASE_URL", f"sqlite+aiosqlite:///{db}")
    os.environ.setdefault("ENV", "dev")
    os.environ.setdefault("ALLOW_UNREVIEWED", "1")
    os.environ.setdefault("AUTO_MIGRATE", "0")
    sys.path.insert(0, str(ROOT / "server"))
    t0 = time.perf_counter()
    from app.realtime.world import World, world_zones
    out = {"import_s": time.perf_counter() - t0}
    w = World()
    per = {}
    t0 = time.perf_counter()
    for z in world_zones():
        t = time.perf_counter()
        w._channels(z)
        per[z] = round((time.perf_counter() - t) * 1000)
    out["preload_s"] = time.perf_counter() - t0
    out["per_zone_ms"] = per
    out["maps_mb"] = sum(p.stat().st_size for p in (ROOT / "server" / "maps").glob("*.tmj")) / 2 ** 20
    out["ws_mb"], out["peak_ws_mb"] = working_set_mb()
    return out


def _run_part(args: list) -> dict:
    cmd = [sys.executable, str(Path(__file__).resolve()), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith("RESULT ")), None)
    if line is None:
        tail = (r.stderr or r.stdout).strip().splitlines()[-6:]
        return {"error": " | ".join(tail)}
    return json.loads(line[7:])


def bench_zone(zone: str, path: Path | None, a) -> dict:
    """One real zone: the client's walk at zoom 2 (the v2 art) and the server's channel and ticks."""
    spath = path or ROOT / "server" / "maps" / f"{zone}.tmj"
    args = ["--part", "client", "--zoom", "2", "--frames", str(a.frames), "--zone", zone]
    if path is not None:
        args += ["--map", str(path)]
    c = _run_part(args)
    s = _run_part(["--part", "server", "--map", str(spath), "--ticks", str(a.ticks), "--zone", zone])
    size = spath.stat().st_size / 1024
    if "error" in c:
        print(f"{zone:18} client FAILED {c['error']}")
    else:
        print(f"{zone:18} file {size:7.0f} KB  client: load {c['load_s'] * 1000:5.0f} ms, scene {c['scene_s'] * 1000:5.0f} ms, "
              f"surfaces {c['surface_mb']:5.1f} MB, frame avg {c['avg_ms']:.2f} / p99 {c['p99_ms']:.2f} / worst "
              f"{c['worst_ms']:.2f} ms, working set {c['ws_mb']:.0f} MB")
    if "error" in s:
        print(f"{zone:18} server FAILED {s['error']}")
    else:
        print(f"{zone:18} server: parse {s['parse_s'] * 1000:5.0f} ms, channel {s['channel_s'] * 1000:5.0f} ms, "
              f"{s['monsters']} monsters, ticks " + ", ".join(
                  f"{n}p {s[f'tick_{n}']['avg_ms']:.2f}/{s[f'tick_{n}']['worst_ms']:.2f} ms" for n in (1, 10, 40)))
    return {"client": c, "server": s, "file_kb": size}


# ------------------------------------------------------------------ driver
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="")
    ap.add_argument("--map", default="")
    ap.add_argument("--zoom", type=int, default=2)
    ap.add_argument("--frames", type=int, default=1500)
    ap.add_argument("--ticks", type=int, default=200)
    ap.add_argument("--zone", default="", help="a real zone (or 'all') instead of the synthetic land")
    ap.add_argument("--startup", action="store_true", help="the server's start-up with every map preloaded")
    a = ap.parse_args()
    if a.part == "client":
        res = client_part(a.zoom, Path(a.map) if a.map else None, a.frames, a.zone)
        print("RESULT " + json.dumps(res))
        return
    if a.part == "server":
        print("RESULT " + json.dumps(server_part(Path(a.map), a.ticks, a.zone)))
        return
    if a.part == "startup":
        print("RESULT " + json.dumps(startup_part()))
        return
    if a.startup:
        print(json.dumps(_run_part(["--part", "startup"]), ensure_ascii=False))
        return
    if a.zone:
        zones = ([p.stem for p in sorted((ROOT / "server" / "maps").glob("*.tmj")) if p.stem != "bi_canh"]
                 if a.zone == "all" else [a.zone])
        for z in zones:
            print("RESULT " + json.dumps({z: bench_zone(z, Path(a.map) if a.map else None, a)}))
        return
    folder = Path(tempfile.mkdtemp(prefix="bench_giant_"))
    t0 = time.perf_counter()
    path = make_map(folder)
    print(f"synthetic map: {path} ({path.stat().st_size / 2 ** 20:.1f} MB, built in {time.perf_counter() - t0:.1f} s)")

    def run(args):
        cmd = [sys.executable, str(Path(__file__).resolve()), *args]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        line = next((ln for ln in r.stdout.splitlines() if ln.startswith("RESULT ")), None)
        if line is None:
            tail = (r.stderr or r.stdout).strip().splitlines()[-6:]
            return {"error": " | ".join(tail)}
        return json.loads(line[7:])
    for zoom in (1, 2):
        for which in ("small", "giant"):
            args = ["--part", "client", "--zoom", str(zoom), "--frames", str(a.frames)]
            if which == "giant":
                args += ["--map", str(path)]
            r = run(args)
            if "error" in r:
                print(f"client zoom {zoom} {which:5}: FAILED {r['error']}")
                continue
            print(f"client zoom {zoom} {which:5}: load {r['load_s']:.2f} s, scene {r['scene_s']:.2f} s, "
                  f"surfaces {r['surface_mb']:.1f} MB, frame avg {r['avg_ms']:.2f} ms, p99 {r['p99_ms']:.2f} ms, "
                  f"worst {r['worst_ms']:.2f} ms, first {r['first_ms']:.0f} ms ({r['frames']} frames), "
                  + (f"without ground building {r['net_avg_ms']:.2f} ms, " if r.get("net_avg_ms") is not None else "")
                  + f"working set {r['ws_mb']:.0f} MB (peak {r['peak_ws_mb']:.0f} MB)")
    r = run(["--part", "server", "--map", str(path), "--ticks", str(a.ticks)])
    if "error" in r:
        print(f"server: FAILED {r['error']}")
    else:
        print(f"server: parse {r['parse_s']:.2f} s, channel {r['channel_s'] * 1000:.0f} ms, {r['monsters']} monsters")
        for n in (1, 10, 40):
            t = r[f"tick_{n}"]
            print(f"server tick, {n:2} players: avg {t['avg_ms']:.2f} ms, p99 {t['p99_ms']:.2f} ms, worst {t['worst_ms']:.2f} ms")


if __name__ == "__main__":
    main()
