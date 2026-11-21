"""Walk the real lands by following nothing but the Chỉ Đường arrow (no server, no drawing): the
movement code of the client (engine/movement.py) steps toward each reading's aim, as the held
keys of a player would (the eight directions, a tenth of a second a step). docs/CHI_DUONG.md,
"Walking every anchor", and docs/DAI_DIA_DO_KIEM_THU.md.

* `walk_land(zone)`: from the land's gate (its spawn from the village) to the anchor of every khu
  the map declares, in map order;
* `walk_all(zone)`: the same and every named place of the map (`poi`, the gate itself left out)
  and every weapon spot and beast of the land in server/data/math/world_plan.json, except those
  that `needs` a flying skill (they lie past water or ink on purpose); then from the deepest anchor
  back home as the H key leads: through the land's gate, then through the village to the gate of
  the Động Phủ;
* `world_lands()`: the lands walked - every shipped map with khu or named places (derived from
  the maps, never a list kept by hand).

    python -m client.tests.nav_walk                      # every land, a table of the walks
    python -m client.tests.nav_walk rung_muc_loang       # one land

Used by client/tests/test_nav_units.py.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from client.engine import chi_duong, movement as mv, navigator as nv

SPEED = 74.0            # px per second on foot (scenes/world.py SPEED)
STEP_MS = 100
STUCK_STEPS = 40        # four seconds without getting 8 px nearer the goal by the field: stuck
RATIO_MAX = 1.6         # walked / length of the way
ROOT = Path(__file__).resolve().parents[2]
SKIP_POI = {"gate"}     # the gate is where the walks start


def keys_for(dx: float, dy: float, lean: bool = False) -> tuple[int, int]:
    """The keys a player holds for an arrow pointing along (dx, dy): the nearest of the eight
    directions (a key of the minor axis only when the arrow leans more than about 22 degrees
    toward it), nothing within 2 px. `lean`: a player stopped against a corner presses the
    minor axis too, however little the arrow leans."""
    ax, ay = abs(dx), abs(dy)
    k = 0.0 if lean else 0.41
    kx = (dx > 0) - (dx < 0) if ax > (0.5 if lean else 2) and ax >= k * ay else 0
    ky = (dy > 0) - (dy < 0) if ay > (0.5 if lean else 2) and ay >= k * ax else 0
    return kx, ky


def line_free(col: mv.Collider, x: float, y: float, ax: float, ay: float) -> bool:
    """Can the feet go straight from (x, y) to the arrow's aim? (the movement collider, every
    2 px: a wall, water, a tree line between khu all are solids there)"""
    n = max(1, int(math.hypot(ax - x, ay - y) / 2))
    return not any(col.blocked(x + (ax - x) * k / n, y + (ay - y) * k / n) for k in range(1, n + 1))


def path_length(leg: nv.Leg, x: float, y: float) -> float:
    """The length of the way from (x, y): the field's chain of cells, its corners cut by the
    straight lines the arrow takes (each run of cells walked as one segment while it is straight
    in a line the grid allows) - what a player who knows the way walks."""
    f, g = leg.field, leg.grid
    i = f.start_of(x, y)
    if i is None:
        return 0.0
    cells = f.chain(i, 10 ** 7)
    pts = [g.point(c) for c in cells]
    # cut corners greedily: from each anchor point, the farthest point seen in a straight line
    total, k, ax, ay = 0.0, 0, float(x), float(y)
    n = len(pts)
    while k < n - 1:
        best = k + 1
        hi = min(n - 1, k + 60)
        for j in range(hi, k + 1, -1):
            if g.clear_line(ax, ay, *pts[j]):
                best = j
                break
        bx, by = pts[best]
        total += math.hypot(bx - ax, by - ay)
        ax, ay, k = bx, by, best
    return total


def walk(tmap, start: tuple[float, float], goal: tuple[float, float] | None = None, limit_s: float = 900.0,
         budget: float = 0.003, goal_rect: tuple | None = None) -> dict:
    """Follow the arrow from start to a goal point (or a gate's rectangle). Returns the facts of the walk."""
    grid = nv.grid_for(tmap)
    leg = nv.Leg(grid, goal_rect=goal_rect) if goal_rect is not None else nv.Leg(grid, goal_point=goal)
    t0 = time.perf_counter()
    frames = 0
    while not leg.step(budget):
        frames += 1
    search_s = time.perf_counter() - t0
    col = tmap.collider()
    x, y = start
    plen = path_length(leg, x, y)
    walked, ms, best, since = 0.0, 0.0, None, 0.0
    bad_aims = 0
    reads = 0
    read_s = 0.0
    out = {"search_s": search_s, "frames": frames + 1, "path_px": plen}
    water = tmap._water_gid
    while ms / 1000 < limit_s:
        t = time.perf_counter()
        r = leg.read(x, y)
        read_s += time.perf_counter() - t
        reads += 1
        if r.mode == "here" or (goal is not None and math.hypot(goal[0] - x, goal[1] - y) < chi_duong.ARRIVE_PX):
            out.update(ok=True, walked_px=walked, seconds=ms / 1000, x=x, y=y)
            break
        if r.mode != "path":
            out.update(ok=False, why=f"mode {r.mode}", walked_px=walked, seconds=ms / 1000, x=x, y=y)
            break
        ax, ay = r.aim
        if not line_free(col, x, y, ax, ay):
            bad_aims += 1                   # the arrow points through something solid
            out.setdefault("bad_at", []).append((round(x), round(y), round(ax), round(ay)))
        # a tenth of a second, or less when the aim is nearer than that: a player lets go of
        # the keys on the spot the arrow points at (a frame, 16 ms, at the least)
        dt = max(16.0, min(STEP_MS, math.hypot(ax - x, ay - y) / SPEED * 1000))
        dx, dy = keys_for(ax - x, ay - y)
        nx, ny = mv.step(x, y, dx, dy, dt, SPEED, col)
        if (nx, ny) == (x, y):              # held against a corner: the arrow leans a little, so lean too
            dx, dy = keys_for(ax - x, ay - y, lean=True)
            nx, ny = mv.step(x, y, dx, dy, dt, SPEED, col)
        walked += math.hypot(nx - x, ny - y)
        x, y = nx, ny
        if tmap.ground[int(y // tmap.th) * tmap.w + int(x // tmap.tw)] == water:
            out["on_water"] = out.get("on_water", 0) + 1
            out.setdefault("water_at", []).append((round(x), round(y)))
        ms += dt
        d = leg.field.at(leg.field.start_of(x, y) or 0)
        if best is None or d < best - 1:
            best, since = d, 0.0
        else:
            since += dt
            if since > STUCK_STEPS * STEP_MS:
                out.update(ok=False, why="stuck", walked_px=walked, seconds=ms / 1000, x=x, y=y)
                break
    else:
        out.update(ok=False, why="too long", walked_px=walked, seconds=ms / 1000, x=x, y=y)
    out["ratio"] = out["walked_px"] / max(1.0, plen)
    out["bad_aims"] = bad_aims
    out["read_ms"] = read_s / max(1, reads) * 1000
    return out


def good(r: dict) -> bool:
    """The rule every walk keeps (test_nav_units): arrived, never more than RATIO_MAX times the
    way, the arrow never through a solid, the feet never on water."""
    return bool(r.get("ok")) and r["ratio"] < RATIO_MAX and r["bad_aims"] == 0 and not r.get("on_water")


# ------------------------------------------------------------------ what a land offers to walk to
def _map_objects(zone: str) -> tuple[dict, list]:
    data = json.loads((nv._maps_dir() / f"{zone}.tmj").read_text("utf-8"))
    props = {p["name"]: p["value"] for p in data.get("properties", [])}
    objs = []
    for layer in data.get("layers", []):
        if layer.get("type") == "objectgroup" and layer.get("name") != "collision":
            objs += layer.get("objects", [])
    return props, objs


def world_lands() -> list[str]:
    """Every shipped map with khu or named places (poi): the giant lands first, by name, then the
    others (Lôi Kiếp Đài)."""
    out = []
    for p in sorted(nv._maps_dir().glob("*.tmj")):
        props, objs = _map_objects(p.stem)
        if any(o.get("type") in ("khu", "poi") for o in objs):
            out.append((props.get("dai_dia_do") != "true", p.stem))
    return [z for _k, z in sorted(out)]


def _plan() -> dict:
    return json.loads((ROOT / "server" / "data" / "math" / "world_plan.json").read_text("utf-8"))


def land_of(zone: str) -> str | None:
    return next((l["id"] for l in _plan().get("lands", []) if l.get("map") == zone), None)


def spots(zone: str) -> list[dict]:
    """The weapon spots and beasts world_plan places in this land: {name, tile, needs}."""
    plan, land = _plan(), land_of(zone)
    out = []
    for w in plan.get("weapons_placed", []):
        if w.get("land") == land and isinstance(w.get("pos"), list):
            out.append({"name": f"vũ khí {w.get('weapon')}", "tile": tuple(w["pos"]), "needs": w.get("needs")})
    for b in plan.get("beasts", []):
        if b.get("land") == land and isinstance(b.get("pos"), list):
            out.append({"name": f"linh thú {b.get('id')}", "tile": tuple(b["pos"]), "needs": b.get("needs")})
    return out


def flight_tiles(zone: str) -> list[tuple]:
    """The tiles world_plan documents as reached only by a flying skill (`needs`)."""
    return [s["tile"] for s in spots(zone) if s["needs"]]


def goals_of(zone: str, tmap) -> list[dict]:
    """Everything of a land to walk to: {kind (khu, poi, spot), id, name, band, goal (px)}. A poi or
    spot within 3 tiles of a place that needs flight is left out (`skipped` lists them); a goal
    within a tile of one already listed too (a camp's poi stands on its anchor)."""
    out, skipped = [], []
    fly = flight_tiles(zone)

    def near_fly(tx, ty):
        return any(max(abs(tx - fx), abs(ty - fy)) <= 3 for fx, fy in fly)

    def add(g):
        if any(abs(g["goal"][0] - o["goal"][0]) <= 16 and abs(g["goal"][1] - o["goal"][1]) <= 16 for o in out):
            return
        out.append(g)

    for (rx, ry, rw, rh), props in chi_duong.khu_objects(tmap):
        goal = (chi_duong.num(props.get("anchor_x"), int(rx + rw / 2)),
                chi_duong.num(props.get("anchor_y"), int(ry + rh / 2)))
        add({"kind": "khu", "id": props.get("khu"), "name": props.get("name_vi"),
             "band": chi_duong.num(props.get("band")), "goal": goal})
    for o in tmap.find("poi"):
        kind = o.props.get("poi")
        if kind in SKIP_POI:
            continue
        tx, ty = int((o.x + o.w / 2) // 16), int((o.y + o.h / 2) // 16)
        g = {"kind": "poi", "id": kind, "name": o.props.get("name_vi"), "band": None,
             "goal": (tx * 16 + 8, ty * 16 + 12)}
        (skipped.append(g) if near_fly(tx, ty) else add(g))
    for s in spots(zone):
        tx, ty = s["tile"]
        g = {"kind": "spot", "id": s["needs"] or "", "name": s["name"], "band": None,
             "goal": (tx * 16 + 8, ty * 16 + 12)}
        (skipped.append(g) if s["needs"] or near_fly(tx, ty) else add(g))
    goals_of.skipped = skipped
    return out


def _start(tmap, spawn: str = "from_village") -> tuple[float, float]:
    return next((o.x, o.y) for o in tmap.find("spawn") if o.name == spawn)


def walk_land(zone: str, spawn: str = "from_village") -> list[dict]:
    """From the land's gate (its spawn from the village) to the anchor of every khu, in map order."""
    from client.engine.tilemap import load_map
    tmap = load_map(zone)
    start = _start(tmap, spawn)
    rows = []
    for (rx, ry, rw, rh), props in chi_duong.khu_objects(tmap):
        goal = (chi_duong.num(props.get("anchor_x"), int(rx + rw / 2)),
                chi_duong.num(props.get("anchor_y"), int(ry + rh / 2)))
        r = walk(tmap, start, goal)
        r.update(zone=zone, khu=props.get("khu"), name=props.get("name_vi"), band=chi_duong.num(props.get("band")),
                 goal=goal)
        rows.append(r)
    return rows


def walk_home(zone: str, start: tuple[float, float]) -> list[dict]:
    """The H key from `start`: through each gate of the route to the Động Phủ, each leg walked by
    the arrow from where the last gate left the player (the village's spawn for this land)."""
    from client.engine.tilemap import load_map
    zones = nv.world_zones()
    gates = nv.zone_route(zones, zone, chi_duong.HOME) or []
    rows, at, pos = [], zone, start
    for g in gates:
        if g.zone == chi_duong.HOME:
            break
        tmap = load_map(at)
        r = walk(tmap, pos, goal_rect=g.rect)
        r.update(zone=at, khu=f"về nhà: cổng {g.name or g.target}", name=f"H qua {at}", band=None, kind="home")
        rows.append(r)
        info = zones.get(g.target)
        pos = info.spawns.get(g.target_spawn) or info.spawns.get("spawn")
        at = g.target
    if not gates:
        rows.append({"zone": zone, "khu": "về nhà", "ok": False, "why": "no route home", "ratio": 0,
                     "bad_aims": 0, "seconds": 0, "path_px": 0, "walked_px": 0, "kind": "home",
                     "search_s": 0, "read_ms": 0})
    return rows


SHORE_RINGS = 20        # a named place inside water (a lake, a glide islet): walk to its shore, 10 tiles at most


def shore(grid: nv.WalkGrid, reach: nv.Field, goal: tuple) -> tuple | None:
    """None when the cells round a goal (the 6 rings the arrow aims at) can be walked to from the
    gate; else the nearest cell within SHORE_RINGS that can (its point), or () when none can."""
    near = grid.cells_near(*goal, rings=6)
    if any(reach.at(i) >= 0 for i in near):
        return None
    cx, cy = grid.cell_of(*goal)
    for r in range(1, SHORE_RINGS + 1):
        best = None
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r or not (0 <= cx + dx < grid.cw and 0 <= cy + dy < grid.ch):
                    continue
                i = grid.index(cx + dx, cy + dy)
                if reach.at(i) >= 0:
                    d = math.hypot(dx, dy)
                    if best is None or d < best[0]:
                        best = (d, i)
        if best is not None:
            return grid.point(best[1])
    return ()


def walk_all(zone: str, spawn: str = "from_village") -> dict:
    """Every goal of a land from its gate, then home from the deepest anchor. {rows, home, skipped, seconds}
    A named place standing in water (a lake's middle, an islet reached by a glide) is walked to its
    nearest shore that can be walked to (`shore_tiles` in its row)."""
    from client.engine.tilemap import load_map
    t0 = time.perf_counter()
    tmap = load_map(zone)
    start = _start(tmap, spawn)
    grid = nv.grid_for(tmap)
    reach = nv.Leg(grid, goal_point=start)
    while not reach.step(1.0):
        pass
    rows = []
    for g in goals_of(zone, tmap):
        goal, extra = g["goal"], {}
        if g["kind"] != "khu":
            s = shore(grid, reach.field, goal)
            if s == ():
                rows.append({"zone": zone, "khu": g["id"], "name": g["name"], "kind": g["kind"], "ok": False,
                             "why": "no shore", "ratio": 0, "bad_aims": 0, "seconds": 0, "path_px": 0,
                             "walked_px": 0, "search_s": 0, "read_ms": 0, "goal": goal})
                continue
            if s:
                extra["shore_tiles"] = round(math.hypot(s[0] - goal[0], s[1] - goal[1]) / 16, 1)
                goal = s
        r = walk(tmap, start, goal)
        r.update(zone=zone, khu=g["id"], name=g["name"], band=g["band"], goal=goal, kind=g["kind"], **extra)
        rows.append(r)
    skipped = list(goals_of.skipped)
    khu = [r for r in rows if r["kind"] == "khu" and r.get("ok")]
    deep_from = max(khu or [r for r in rows if r.get("ok")] or [{"goal": start, "path_px": 0}],
                    key=lambda r: ((r.get("band") or 0), r["path_px"]))
    home = walk_home(zone, deep_from["goal"])
    for h in home:
        h["from"] = deep_from.get("name")
    return {"zone": zone, "rows": rows, "home": home, "skipped": skipped, "seconds": time.perf_counter() - t0}


def fmt(r: dict) -> str:
    name = str(r.get("name") or "")[:28]
    return (f"{r['zone']:17} {r.get('kind', 'khu'):4} {str(r.get('khu'))[:24]:24} {name:28} ok {good(r)!s:5} "
            f"{r.get('why', ''):12} way {r['path_px'] / 32:5.0f} tr walked {r['walked_px'] / 32:5.0f} tr "
            f"ratio {r['ratio']:.2f} {r['seconds']:6.1f} s search {r['search_s'] * 1000:4.0f} ms "
            f"read {r['read_ms']:.2f} ms bad {r['bad_aims']} water {r.get('on_water', 0)}"
            + (f" (shore {r['shore_tiles']} tiles off)" if r.get("shore_tiles") else ""))


def main() -> None:
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    total_bad = 0
    for zone in sys.argv[1:] or world_lands():
        res = walk_all(zone)
        for r in res["rows"] + res["home"]:
            print(fmt(r))
            if not good(r):
                total_bad += 1
                print("   ", {k: r[k] for k in ("why", "x", "y", "bad_at", "water_at") if k in r})
        for s in res["skipped"]:
            print(f"{zone:17} skip {s['name']} (cần bay)")
        print(f"{zone:17} {len(res['rows'])} goals, home from {res['home'][0].get('from')}: "
              f"{sum(h['seconds'] for h in res['home']):.0f} s walked; test time {res['seconds']:.1f} s")
    print("failures:", total_bad)


if __name__ == "__main__":
    main()
