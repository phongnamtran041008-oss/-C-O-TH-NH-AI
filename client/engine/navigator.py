"""Chỉ Đường on the client: the way through a zone and from zone to zone (docs/CHI_DUONG.md).

**In a zone** the way is read from a distance field over a grid of foot positions:

* `WalkGrid`: one cell every CELL = 8 px; cell (cx, cy) stands for the feet at (cx * 8, cy * 8 + 3)
  (so the middle of a one-tile corridor, x = tile + 8, y = tile + 11, is a cell). A cell is
  walkable when the 10 x 6 foot box of engine/movement.py, made 2 px taller (one pixel above and
  below), touches no solid and stays on the map. The taller box makes the step between two
  neighbouring cells safe: the boxes of every point on the way lie inside the two cells' boxes.
  The grid is rasterised from the solid rectangles, row slice by row slice.
* `Field`: a breadth-first distance field (4 neighbours) from the goal cells - the walkable cells
  inside a gate, or the cells round a point - over the whole map. Because it covers every cell
  the goal can be walked to from, a player who strays needs no new search: the way is read
  again from wherever they stand. Building the grid and the field are generators run a few
  milliseconds per frame (`Job.run(budget)`), so a 320 x 240 tile map never hitches a frame.
* `Leg.read`: from the player's cell, down the field; the arrow points at the farthest cell of
  the next few that can be seen in a straight line (so a staircase of grid steps reads as one
  diagonal). A player standing where the field never reached (an island) gets a straight arrow.

**From zone to zone** (`gates`, `zone_route`): the portals of every map (`portal` objects with
`target`, `target_spawn`), plus the abode's gate (its `interact` object with action `exit`, which
leads to the village). The route is a breadth-first search over zones.
"""
from __future__ import annotations

import json
from array import array
import math
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

CELL = 8
OFF_Y = 3                 # cell (cx, cy) is the feet at (cx * CELL, cy * CELL + OFF_Y)
FOOT_W, FOOT_H = 10, 6    # engine/movement.py
LOOK = 14                 # how many cells ahead the arrow may look for a straight line
NEAR = 3                  # rings searched round a cell the field did not reach
TRUONG_PX = 32            # 1 trượng = 2 tiles
ROAD, OFF = 2, 3          # the cost of a step onto a road cell, onto any other: the way keeps to the
                          # roads (and their bridges and passes) unless leaving them saves a third
ROAD_TILES = ("path", "plaza", "wood", "bamboo_floor")       # TILESET names a road is made of


def _ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


# ------------------------------------------------------------------ the grid
class WalkGrid:
    """Walkable foot cells of a map (see the module docstring). Index i = (cy + 1) * W + cx + 1:
    the grid has a frame of blocked cells, so neighbours never need a bounds check."""

    def __init__(self, px_w: int, px_h: int, solids, ground=None, tiles_w: int = 0, tile: int = 16,
                 roads=()):
        self.px_w, self.px_h = int(px_w), int(px_h)
        self.cw = self.px_w // CELL + 1
        self.ch = self.px_h // CELL + 1
        self.W = self.cw + 2
        self.H = self.ch + 2
        self.solids = [(int(r[0]), int(r[1]), int(r[2]), int(r[3])) for r in solids]
        self.walk: bytearray | None = None
        self.ready = False
        # the cost of stepping onto a cell: ROAD on a road tile (the tile under the feet), OFF
        # elsewhere; None (no ground given) is 1 everywhere: plain breadth-first distances
        self.ground, self.tiles_w, self.tile, self.roads = ground, int(tiles_w), int(tile), frozenset(roads)
        self.cost: bytearray | None = None

    def build(self):
        """A generator: yields every few hundred solids (Job runs it within a time budget)."""
        W, cw, ch = self.W, self.cw, self.ch
        walk = bytearray(W * self.H)
        # on the map: left = x - 5 >= 0, x + 5 <= w; the taller box: y - 7 >= 0, y + 1 <= h
        x0, x1 = 1, (self.px_w - FOOT_W // 2) // CELL
        y0 = _ceil_div(FOOT_H + 1 - OFF_Y, CELL)
        y1 = (self.px_h - 1 - OFF_Y) // CELL
        x0, x1 = max(0, x0), min(cw - 1, x1)
        y0, y1 = max(0, y0), min(ch - 1, y1)
        if x1 >= x0:
            row = b"\x01" * (x1 - x0 + 1)
            for cy in range(y0, y1 + 1):
                base = (cy + 1) * W + 1
                walk[base + x0: base + x1 + 1] = row
        yield
        for n, (sx, sy, sw, sh) in enumerate(self.solids):
            # feet (fx, fy) are blocked when fx in (sx - 5, sx + sw + 5) and fy in (sy - 1, sy + sh + 7)
            a = max(0, (sx - FOOT_W // 2) // CELL + 1)
            b = min(cw - 1, _ceil_div(sx + sw + FOOT_W // 2, CELL) - 1)
            c = max(0, (sy - 1 - OFF_Y) // CELL + 1)
            d = min(ch - 1, _ceil_div(sy + sh + FOOT_H + 1 - OFF_Y, CELL) - 1)
            if a <= b and c <= d:
                zeros = bytes(b - a + 1)
                for cy in range(c, d + 1):
                    base = (cy + 1) * W + 1
                    walk[base + a: base + b + 1] = zeros
            if n % 256 == 255:
                yield
        if self.ground and self.roads and self.tile == 2 * CELL and self.tiles_w > 0:
            yield from self._build_cost()
        self.walk = walk
        self.ready = True

    def _build_cost(self):
        """Every cell's cost from the tile under its feet (x = 8 cx, y = 8 cy + 3: tile column
        cx // 2, row (8 cy + 3) // 16): a row of tiles turned into costs by a byte table, each
        tile doubled into its two columns of cells."""
        lut = bytes(ROAD if i in self.roads else OFF for i in range(256))
        W, cw, tw = self.W, self.cw, self.tiles_w
        g = self.ground
        rows = len(g) // tw
        cost = bytearray([OFF]) * (W * self.H)
        pair = bytearray(2 * tw)
        for cy in range(self.ch):
            ty = (cy * CELL + OFF_Y) // self.tile
            if ty >= rows:
                break
            part = g[ty * tw:(ty + 1) * tw]
            try:
                row = bytes(part).translate(lut)
            except ValueError:                 # a tile id past 255: clamp it (never a road)
                row = bytes(min(255, max(0, v)) for v in part).translate(lut)
            pair[0::2] = row
            pair[1::2] = row
            n = min(cw, len(pair))
            base = (cy + 1) * W + 1
            cost[base: base + n] = pair[:n]
            if cy % 64 == 63:
                yield
        self.cost = cost

    def build_now(self) -> "WalkGrid":
        for _ in self.build():
            pass
        return self

    # ---- cells and points
    def index(self, cx: int, cy: int) -> int:
        return (cy + 1) * self.W + cx + 1

    def cell_of(self, x: float, y: float) -> tuple[int, int]:
        return int(round(x / CELL)), int(round((y - OFF_Y) / CELL))

    def index_of(self, x: float, y: float) -> int:
        cx, cy = self.cell_of(x, y)
        cx = min(max(cx, -1), self.cw)
        cy = min(max(cy, -1), self.ch)
        return self.index(cx, cy)

    def point(self, i: int) -> tuple[int, int]:
        cy, cx = divmod(i, self.W)
        return (cx - 1) * CELL, (cy - 1) * CELL + OFF_Y

    def walkable(self, i: int) -> bool:
        return bool(self.walk[i]) if 0 <= i < len(self.walk) else False

    def cells_in(self, x: float, y: float, w: float, h: float) -> list[int]:
        """The walkable cells whose feet lie inside a rectangle (a gate)."""
        out = []
        for cy in range(max(0, _ceil_div(int(y) - OFF_Y, CELL)), min(self.ch - 1, int((y + h - OFF_Y) // CELL)) + 1):
            for cx in range(max(0, _ceil_div(int(x), CELL)), min(self.cw - 1, int((x + w) // CELL)) + 1):
                i = self.index(cx, cy)
                if self.walk[i]:
                    out.append(i)
        return out

    def cells_near(self, x: float, y: float, rings: int = 4) -> list[int]:
        """The walkable cells nearest a point (the point's own cell when it is walkable)."""
        cx, cy = self.cell_of(x, y)
        for r in range(rings + 1):
            found = []
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.cw and 0 <= ny < self.ch and self.walk[self.index(nx, ny)]:
                        found.append(self.index(nx, ny))
            if found:
                return found
        return []

    def free_at(self, x: float, y: float) -> bool:
        """Is the foot position (x, y) free? True when the cells round it (the 2 x 2 block, or
        fewer when it lies on a cell's row or column) are walkable: their boxes tile a rectangle
        that holds the foot box."""
        fx, fy = x / CELL, (y - OFF_Y) / CELL
        x0, y0 = math.floor(fx), math.floor(fy)
        xs = (x0,) if fx == x0 else (x0, x0 + 1)
        ys = (y0,) if fy == y0 else (y0, y0 + 1)
        walk, W = self.walk, self.W
        for cy in ys:
            for cx in xs:
                if not (0 <= cx < self.cw and 0 <= cy < self.ch) or not walk[(cy + 1) * W + cx + 1]:
                    return False
        return True

    def clear_line(self, ax: float, ay: float, bx: float, by: float) -> bool:
        """Can the feet go straight from a to b? (every 2 px on the way is a free foot position;
        a, where the player stands, is not checked)"""
        d = math.hypot(bx - ax, by - ay)
        n = max(1, int(d / 2))
        for k in range(1, n + 1):
            t = k / n
            if not self.free_at(ax + (bx - ax) * t, ay + (by - ay) * t):
                return False
        return True


# ------------------------------------------------------------------ the distance field
class Field:
    """Breadth-first distances (in cells) from the goal cells to every cell that can walk there."""

    def __init__(self, grid: WalkGrid, goals: list[int]):
        self.grid = grid
        self.goals = list(dict.fromkeys(goals))
        self.dist: array | None = None
        self.done = False
        self.reached = 0
        self.level = 0            # while building: every distance below it is final already
        self.weighted = grid.cost is not None

    @property
    def unit(self) -> float:
        """Cost units per cell walked (to turn a distance of the field into pixels)."""
        return (ROAD + OFF) / 2 if self.grid.cost is not None else 1.0

    def build(self):
        if self.grid.cost is not None:
            yield from self._build_weighted()
            return
        g = self.grid
        walk, W = g.walk, g.W
        dist = array("i", [-1]) * len(walk)     # (4 bytes a cell: a list of ints is 9 times that)
        q = []
        for s in self.goals:
            if walk[s] and dist[s] < 0:
                dist[s] = 0
                q.append(s)
        self.dist = dist
        head = 0
        append = q.append
        while head < len(q):
            i = q[head]
            head += 1
            d = dist[i] + 1
            j = i - 1
            if walk[j] and dist[j] < 0:
                dist[j] = d
                append(j)
            j = i + 1
            if walk[j] and dist[j] < 0:
                dist[j] = d
                append(j)
            j = i - W
            if walk[j] and dist[j] < 0:
                dist[j] = d
                append(j)
            j = i + W
            if walk[j] and dist[j] < 0:
                dist[j] = d
                append(j)
            if not head & 1023:
                yield
        self.reached = len(q)
        self.done = True

    def _build_weighted(self):
        """Dial's shortest paths (costs ROAD / OFF per step onto a cell): buckets by distance,
        a bucket per distance modulo OFF + 1; a cell may be queued twice, the later copy is
        skipped when it comes out."""
        g = self.grid
        walk, W, cost = g.walk, g.W, g.cost
        dist = array("i", [-1]) * len(walk)     # (4 bytes a cell: a list of ints is 9 times that)
        nb = OFF + 1
        buckets = [[] for _ in range(nb)]
        pending = 0
        for s in self.goals:
            if walk[s] and dist[s] < 0:
                dist[s] = 0
                buckets[0].append(s)
                pending += 1
        self.dist = dist
        d = 0
        n = 0
        reached = 0
        while pending:
            b = buckets[d % nb]
            self.level = d
            if not b:
                d += 1
                continue
            pending -= len(b)
            cur = b[:]
            b.clear()
            for i in cur:
                n += 1
                if not n & 511:
                    yield
                if dist[i] != d:
                    continue
                reached += 1
                for j in (i - 1, i + 1, i - W, i + W):
                    if walk[j]:
                        nd = d + cost[j]
                        dj = dist[j]
                        if dj < 0 or nd < dj:
                            dist[j] = nd
                            buckets[nd % nb].append(j)
                            pending += 1
            d += 1
        self.reached = reached
        self.done = True

    def at(self, i: int) -> int:
        return self.dist[i] if self.dist is not None and 0 <= i < len(self.dist) else -1

    def final(self, d: int) -> bool:
        """Is a distance of the field final? (always once it is built; while it is being built,
        a breadth-first distance is final when set, a weighted one below the level reached -
        the way down the field from such a cell passes only through smaller, final ones)"""
        return d >= 0 and (self.done or not self.weighted or d < self.level)

    def start_of(self, x: float, y: float) -> int | None:
        """The cell the way is read from: the player's own cell, else the nearest one the field
        reached within NEAR rings (the feet may stand a pixel off a cell); None: no way on foot
        (or, while the field is still being built, not known yet). The way from a cell is known
        as soon as its distance is final: on a giant land the arrow shows long before the field
        has covered the whole map."""
        if self.dist is None:
            return None
        g = self.grid
        i = g.index_of(x, y)
        if self.final(self.at(i)):
            return i
        partial = not self.done and self.weighted
        if partial and g.walkable(i):
            return None                     # its own cell may still be reached: wait for it
        cx, cy = g.cell_of(x, y)
        best, best_d = None, None
        for r in range(1, NEAR + 1):
            unsure = False
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < g.cw and 0 <= ny < g.ch):
                        continue
                    j = g.index(nx, ny)
                    d = self.at(j)
                    if self.final(d):
                        if best_d is None or d + r * OFF < best_d:
                            best, best_d = j, d + r * OFF
                    elif partial and g.walk[j]:
                        unsure = True       # not final yet: it might be the better start
            if unsure:
                return None
            if best is not None:
                return best
        return None

    def next_cell(self, i: int, prev: int = 0) -> int | None:
        """One step down the field (keeping the last direction on a tie, so the way is straight)."""
        d = self.dist[i]
        if d <= 0:
            return None
        W = self.grid.W
        cost = self.grid.cost
        want = d - (cost[i] if cost is not None else 1)       # the cell this one was reached from
        steps = (prev, 1, -1, W, -W) if prev else (1, -1, W, -W)
        for s in steps:
            if s and self.dist[i + s] == want:
                return i + s
        return None

    def chain(self, i: int, n: int) -> list[int]:
        """Up to n cells down the field from cell i (i included)."""
        out = [i]
        prev = 0
        while len(out) < n:
            j = self.next_cell(out[-1], prev)
            if j is None:
                break
            prev = j - out[-1]
            out.append(j)
        return out


class Job:
    """Runs a generator a little at a time."""

    def __init__(self, gen):
        self.gen = gen
        self.done = False
        self.spent = 0.0          # seconds of work so far
        self.slices = 0
        self.longest = 0.0        # the longest single slice

    def run(self, budget: float) -> bool:
        if self.done:
            return True
        t0 = time.perf_counter()
        end = t0 + budget
        try:
            while time.perf_counter() < end:
                next(self.gen)
        except StopIteration:
            self.done = True
        dt = time.perf_counter() - t0
        self.spent += dt
        self.slices += 1
        self.longest = max(self.longest, dt)
        return self.done


# ------------------------------------------------------------------ a zone's way to one goal
@dataclass
class Reading:
    mode: str                       # "path" | "straight" | "searching" | "here"
    aim: tuple[float, float]        # the point the arrow points at (world px)
    dist_px: float                  # what is left to walk in this zone
    route: list = field(default_factory=list)     # world points down the way (for the maps)


class Leg:
    """The way to one goal (a gate, a point) in one map: its grid, its field, its readings."""

    def __init__(self, grid: WalkGrid, goal_rect: tuple | None = None, goal_point: tuple | None = None):
        self.grid = grid
        self.goal_rect = goal_rect
        self.goal_point = goal_point
        if goal_rect is not None:
            x, y, w, h = goal_rect
            self.aim = (x + w / 2, y + h / 2)
        else:
            self.aim = goal_point
        self.field: Field | None = None
        self.job: Job | None = None
        self.grid_job = Job(grid.build()) if not grid.ready else None

    def step(self, budget: float) -> bool:
        """Work on the grid and the field for at most `budget` seconds; True once the way is known."""
        end = time.perf_counter() + budget
        if self.grid_job is not None and not self.grid_job.done:
            self.grid_job.run(budget)
            if not self.grid_job.done:
                return False
        if self.field is None:
            g = self.grid
            if self.goal_rect is not None:
                goals = g.cells_in(*self.goal_rect)
                if not goals:                       # a gate drawn past the walkable edge: its mouth
                    x, y, w, h = self.goal_rect
                    goals = g.cells_near(min(max(x + w / 2, 0), g.px_w), min(max(y + h / 2, 0), g.px_h), 6)
            else:
                goals = g.cells_near(*self.goal_point, rings=6)
            self.field = Field(g, goals)
            self.job = Job(self.field.build())
        left = end - time.perf_counter()
        if left > 0 and not self.job.done:
            self.job.run(left)
        return self.job.done

    @property
    def ready(self) -> bool:
        return self.job is not None and self.job.done

    def read(self, x: float, y: float, route_cells: int = 0) -> Reading:
        """Where the arrow points from (x, y), how far it still is, and (route_cells > 0) the way
        itself as world points, one every 4 cells."""
        ax, ay = self.aim
        straight = math.hypot(ax - x, ay - y)
        f, g = self.field, self.grid
        i = f.start_of(x, y) if f is not None else None
        if i is None:                       # not reached yet (searching) or never (an island)
            return Reading("searching" if not self.ready else "straight", self.aim, straight)
        ahead = f.chain(i, LOOK + 1)
        aim = g.point(ahead[1]) if len(ahead) > 1 else self.aim     # no straight line: the next cell
        for j in reversed(ahead[2:]):
            px, py = g.point(j)
            if g.clear_line(x, y, px, py):
                aim = (px, py)
                break
        if f.at(i) == 0:
            return Reading("here", self.aim, 0.0)
        route = []
        dist = None
        if route_cells:
            cells = f.chain(i, route_cells)
            pts = [g.point(c) for c in cells[::4]] + [g.point(cells[-1])]
            length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
            left = f.at(cells[-1])
            dist = math.hypot(pts[0][0] - x, pts[0][1] - y) + length + max(0, left) / f.unit * CELL * 0.85
            route = [(x, y)] + pts
        if dist is None:
            dist = f.at(i) / f.unit * CELL * 0.85
        return Reading("path", aim, dist, route)


# ------------------------------------------------------------------ zones and gates
@dataclass(frozen=True)
class Gate:
    zone: str                       # the zone it is in
    target: str                     # the zone it leads to
    target_spawn: str
    rect: tuple                     # (x, y, w, h) world px
    kind: str = "portal"            # "portal" (walk in) | "exit" (the abode's gate: press E)
    name: str = ""


@dataclass
class ZoneInfo:
    zone: str
    px_w: int
    px_h: int
    gates: list
    spawns: dict


def _maps_dir() -> Path:
    from ..config import assets_dir
    return assets_dir() / "maps"


def read_zone(path: Path) -> ZoneInfo:
    """The gates and spawns of one map, read from its file (the ground is not drawn)."""
    data = json.loads(Path(path).read_text("utf-8"))
    zone = Path(path).stem
    gates, spawns = [], {}
    for layer in data.get("layers", []):
        if layer.get("type") != "objectgroup" or layer.get("name") == "collision":
            continue
        for o in layer.get("objects", []):
            props = {p["name"]: p["value"] for p in o.get("properties", [])}
            rect = (float(o["x"]), float(o["y"]), float(o["width"]), float(o["height"]))
            if o.get("type") == "portal" and props.get("target"):
                gates.append(Gate(zone, props["target"], props.get("target_spawn", "spawn"), rect, "portal",
                                  o.get("name", "")))
            elif o.get("type") == "interact" and props.get("action") == "exit":
                gates.append(Gate(zone, "truc_lam_thon", "from_abode", rect, "exit", o.get("name", "")))
            elif o.get("type") == "spawn":
                spawns[o.get("name") or "spawn"] = (float(o["x"]), float(o["y"]))
    return ZoneInfo(zone, data["width"] * data["tilewidth"], data["height"] * data["tileheight"], gates, spawns)


@lru_cache(maxsize=None)
def world_zones(maps_dir: str | None = None) -> dict:
    """zone id -> ZoneInfo for every map the client ships (the bí cảnh, an instance, is left out)."""
    d = Path(maps_dir) if maps_dir else _maps_dir()
    out = {}
    for p in sorted(d.glob("*.tmj")):
        if p.stem == "bi_canh":
            continue
        out[p.stem] = read_zone(p)
    return out


def zone_route(zones: dict, src: str, dst: str) -> list[Gate] | None:
    """The gates to walk through from zone src to zone dst ([] when already there; None: no way)."""
    if src == dst:
        return []
    prev: dict[str, Gate] = {}
    seen = {src}
    q = [src]
    for z in q:
        info = zones.get(z)
        for g in info.gates if info else ():
            if g.target in seen or g.target not in zones:
                continue
            seen.add(g.target)
            prev[g.target] = g
            if g.target == dst:
                out = []
                at = dst
                while at != src:
                    out.append(prev[at])
                    at = prev[at].zone
                return out[::-1]
            q.append(g.target)
    return None


def estimate_after(zones: dict, gates: list[Gate], final: tuple | None) -> float:
    """A straight-line guess of the walk after the first gate: spawn to next gate, ... to the goal."""
    total = 0.0
    for k, g in enumerate(gates):
        info = zones.get(g.target)
        if info is None:
            break
        sx, sy = info.spawns.get(g.target_spawn) or info.spawns.get("spawn") or (info.px_w / 2, info.px_h / 2)
        if k + 1 < len(gates):
            nx, ny, nw, nh = gates[k + 1].rect
            total += math.hypot(nx + nw / 2 - sx, ny + nh / 2 - sy)
        elif final is not None:
            total += math.hypot(final[0] - sx, final[1] - sy)
    return total


# ------------------------------------------------------------------ grids kept per map
_GRIDS: "OrderedDict[tuple, WalkGrid]" = OrderedDict()


def grid_for(tmap) -> WalkGrid:
    """One walk grid per map (built lazily by the first Leg that needs it)."""
    key = (id(tmap), tmap.px_w, tmap.px_h, len(tmap.solids))
    g = _GRIDS.get(key)
    if g is None:
        g = WalkGrid(tmap.px_w, tmap.px_h, [(r[0], r[1], r[2], r[3]) for r in tmap.solids],
                     getattr(tmap, "ground", None), getattr(tmap, "w", 0), getattr(tmap, "tw", 16), road_gids())
        _GRIDS[key] = g
        while len(_GRIDS) > 4:
            _GRIDS.popitem(last=False)
    return g


@lru_cache(maxsize=1)
def road_gids() -> frozenset:
    """The Tiled ids of the road tiles (gid = TILESET index + 1)."""
    from ..art import build as B
    return frozenset(i + 1 for i, (name, _v) in enumerate(B.TILESET) if name in ROAD_TILES)


def truong(px: float) -> int:
    """World pixels as trượng, never 0 for a way still to walk."""
    return max(1, int(round(px / TRUONG_PX))) if px > 0 else 0
