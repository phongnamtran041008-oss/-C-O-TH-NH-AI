"""Walk a real land by following nothing but the Chỉ Đường arrow (no server, no drawing): the
movement code of the client (engine/movement.py) steps toward each reading's aim, as the held
keys of a player would (the eight directions, a tenth of a second a step), from the land's gate
to the anchor of every khu the map declares. docs/CHI_DUONG.md, "The walk of every anchor".

    python -m client.tests.nav_walk                      # both giant lands, a table of the walks

Used by client/tests/test_nav_units.py.
"""
from __future__ import annotations

import math
import sys
import time

from client.engine import chi_duong, movement as mv, navigator as nv

SPEED = 74.0            # px per second on foot (scenes/world.py SPEED)
STEP_MS = 100
STUCK_STEPS = 40        # four seconds without getting 8 px nearer the goal by the field: stuck


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


def walk(tmap, start: tuple[float, float], goal: tuple[float, float], limit_s: float = 900.0,
         budget: float = 0.003) -> dict:
    """Follow the arrow from start to goal. Returns the facts of the walk."""
    grid = nv.grid_for(tmap)
    leg = nv.Leg(grid, goal_point=goal)
    t0 = time.perf_counter()
    frames = 0
    while not leg.step(budget):
        frames += 1
    search_s = time.perf_counter() - t0
    col = tmap.collider()
    x, y = start
    plen = path_length(leg, x, y)
    walked, steps, best, since = 0.0, 0, None, 0
    bad_aims = 0
    reads = 0
    read_s = 0.0
    out = {"search_s": search_s, "frames": frames + 1, "path_px": plen}
    while steps * STEP_MS / 1000 < limit_s:
        t = time.perf_counter()
        r = leg.read(x, y)
        read_s += time.perf_counter() - t
        reads += 1
        if r.mode == "here" or math.hypot(goal[0] - x, goal[1] - y) < chi_duong.ARRIVE_PX:
            out.update(ok=True, walked_px=walked, seconds=steps * STEP_MS / 1000, x=x, y=y)
            break
        if r.mode != "path":
            out.update(ok=False, why=f"mode {r.mode}", walked_px=walked, seconds=steps * STEP_MS / 1000, x=x, y=y)
            break
        ax, ay = r.aim
        if not line_free(col, x, y, ax, ay):
            bad_aims += 1                   # the arrow points through something solid
            out.setdefault("bad_at", []).append((round(x), round(y), round(ax), round(ay)))
        dx, dy = keys_for(ax - x, ay - y)
        nx, ny = mv.step(x, y, dx, dy, STEP_MS, SPEED, col)
        if (nx, ny) == (x, y):              # held against a corner: the arrow leans a little, so lean too
            dx, dy = keys_for(ax - x, ay - y, lean=True)
            nx, ny = mv.step(x, y, dx, dy, STEP_MS, SPEED, col)
        walked += math.hypot(nx - x, ny - y)
        x, y = nx, ny
        if tmap.ground[int(y // tmap.th) * tmap.w + int(x // tmap.tw)] == tmap._water_gid:
            out["on_water"] = out.get("on_water", 0) + 1
        steps += 1
        d = leg.field.at(leg.field.start_of(x, y) or 0)
        if best is None or d < best - 1:
            best, since = d, 0
        else:
            since += 1
            if since > STUCK_STEPS:
                out.update(ok=False, why="stuck", walked_px=walked, seconds=steps * STEP_MS / 1000, x=x, y=y)
                break
    else:
        out.update(ok=False, why="too long", walked_px=walked, seconds=steps * STEP_MS / 1000, x=x, y=y)
    out["ratio"] = out["walked_px"] / max(1.0, plen)
    out["bad_aims"] = bad_aims
    out["read_ms"] = read_s / max(1, reads) * 1000
    return out


def walk_land(zone: str, spawn: str = "from_village") -> list[dict]:
    """From the land's gate (its spawn from the village) to the anchor of every khu, in map order."""
    from client.engine.tilemap import load_map
    tmap = load_map(zone)
    start = next((o.x, o.y) for o in tmap.find("spawn") if o.name == spawn)
    rows = []
    for (rx, ry, rw, rh), props in chi_duong.khu_objects(tmap):
        goal = (chi_duong.num(props.get("anchor_x"), int(rx + rw / 2)),
                chi_duong.num(props.get("anchor_y"), int(ry + rh / 2)))
        r = walk(tmap, start, goal)
        r.update(zone=zone, khu=props.get("khu"), name=props.get("name_vi"), band=chi_duong.num(props.get("band")),
                 goal=goal)
        rows.append(r)
    return rows


def main() -> None:
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    for zone in sys.argv[1:] or ("loan_so_coc", "luu_van_coc"):
        for r in walk_land(zone):
            print(f"{zone:12} {r['khu']:22} band {r['band']} ok {r['ok']!s:5} {r.get('why', ''):8} "
                  f"path {r['path_px'] / 32:6.0f} tr walked {r['walked_px'] / 32:6.0f} tr ratio {r['ratio']:.2f} "
                  f"{r['seconds']:6.1f} s  search {r['search_s'] * 1000:5.0f} ms read {r['read_ms']:.2f} ms "
                  f"bad aims {r['bad_aims']} on water {r.get('on_water', 0)}")


if __name__ == "__main__":
    main()
