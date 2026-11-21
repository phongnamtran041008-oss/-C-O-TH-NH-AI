"""Helpers shared by Mê Đồ Lâm (rung_muc_loang) and Vạn Tượng Trạch (ho_nghien_muc): giant lands
whose ways are a graph of cells - glades walled by trees in the forest, reed islands in the marsh.

* ``spread``      seed points of the cells, at least `spacing` tiles apart (dart throwing);
* ``Cells``       every tile to its nearest seed of the same khu (a warped Voronoi), the pairs of
                  cells that touch, a spanning tree of them plus a few extra edges;
* ``glade_walls`` a wall of trees on every border between two cells (the forest);
* ``islands``     land around each seed, water everywhere else (the marsh);
* ``route_signs`` a signpost at every junction: for each way out, the nearest named place whose
                  shortest way starts there (a routing table), "ngõ cụt" for a branch that leads
                  nowhere else;
* ``fill``        monster areas over a khu like DaiDiaDo.monsters, for khu that are partly water;
* ``Builder``     DaiDiaDo with a tighter cover of the solid tiles by rectangles (fewer
                  collision objects on maps with many small walls).

The module's name starts with an underscore: tools/mapgen does not take it for a land.
"""
from __future__ import annotations

import heapq
import math
import random

from ..builder import T
from ..giant import ARROWS, SOLID_WALL, SOLID_WATER, DaiDiaDo, rules


# ------------------------------------------------------------------ the builder
class Builder(DaiDiaDo):
    """DaiDiaDo whose solid tiles are covered by greedy maximal rectangles (a run of a row grows
    down while the rows below are solid over the same span), not only by identical row runs."""

    def _solid_rects(self) -> list[tuple]:
        W, H = self.W, self.H
        hard = self.hard
        used = bytearray(W * H)
        out = []
        for y in range(H):
            x = 0
            row = y * W
            while x < W:
                if not hard[row + x] or used[row + x]:
                    x += 1
                    continue
                s = x
                while x < W and hard[row + x] and not used[row + x]:
                    x += 1
                e = x - 1
                y1 = y
                while y1 + 1 < H:
                    r2 = (y1 + 1) * W
                    if all(hard[r2 + i] and not used[r2 + i] for i in range(s, e + 1)):
                        y1 += 1
                    else:
                        break
                for yy in range(y, y1 + 1):
                    for i in range(s, e + 1):
                        used[yy * W + i] = 1
                out.append((s, y, e, y1))
        return out


# ------------------------------------------------------------------ seeds
def spread(rng: random.Random, rect: tuple, spacing: float, fixed=(), tries: int = 900,
           margin: int = 3, avoid=None) -> list[tuple]:
    """Points of rect (x0, y0, x1, y1), each at least `spacing` from the others and from `fixed`
    (which are not returned); `avoid(x, y)` may veto a point."""
    x0, y0, x1, y1 = rect
    pts: list[tuple] = []
    allp = list(fixed)
    for _ in range(tries):
        x = rng.randint(x0 + margin, x1 - margin)
        y = rng.randint(y0 + margin, y1 - margin)
        if avoid and avoid(x, y):
            continue
        if all((x - a) ** 2 + (y - b) ** 2 >= spacing * spacing for a, b in allp):
            pts.append((x, y))
            allp.append((x, y))
    return pts


class Cells:
    """The cells of a land: seeds (id, tile, khu id), every tile's cell, the touching pairs."""

    def __init__(self, m: DaiDiaDo, seeds: list[tuple], warp: float = 5.0, salt: int = 61):
        self.m = m
        self.ids = [s[0] for s in seeds]
        self.tile = {s[0]: tuple(s[1]) for s in seeds}
        bk = m.bands_khu
        rid = {k.id: n for n, k in enumerate(bk)}
        self.region_of = {s[0]: rid[s[2]] for s in seeds}
        by_region: dict[int, list[int]] = {}
        for n, s in enumerate(seeds):
            by_region.setdefault(rid[s[2]], []).append(n)
        W, H = m.W, m.H
        self.owner = [-1] * (W * H)
        nz = m.noise
        for y in range(H):
            for x in range(W):
                j = y * W + x
                cand = by_region.get(m.region[j])
                if not cand:
                    continue
                wx = x + (nz.fbm(x, y, 9.0, 2, salt) - 0.5) * 2 * warp
                wy = y + (nz.fbm(x, y, 9.0, 2, salt + 1) - 0.5) * 2 * warp
                best, bd = -1, 1e18
                for n in cand:
                    sx, sy = seeds[n][1]
                    d = (wx - sx) ** 2 + (wy - sy) ** 2
                    if d < bd:
                        bd, best = d, n
                self.owner[j] = best
        # touching pairs (same khu or not), with the length of the shared border
        self.touch: dict[tuple, int] = {}
        for y in range(H - 1):
            for x in range(W - 1):
                a = self.owner[y * W + x]
                for b in (self.owner[y * W + x + 1], self.owner[(y + 1) * W + x]):
                    if a >= 0 and b >= 0 and a != b:
                        key = (min(a, b), max(a, b))
                        self.touch[key] = self.touch.get(key, 0) + 1

    def idx(self, sid: str) -> int:
        return self.ids.index(sid)

    def neighbours(self, sid: str, min_border: int = 6) -> list[str]:
        n = self.idx(sid)
        out = []
        for (a, b), c in self.touch.items():
            if c >= min_border and n in (a, b):
                out.append(self.ids[b if a == n else a])
        return out

    def same_khu_pairs(self, khu_index: int, min_border: int = 6) -> list[tuple]:
        out = []
        for (a, b), c in sorted(self.touch.items()):
            if c >= min_border and self.region_of[self.ids[a]] == khu_index == self.region_of[self.ids[b]]:
                out.append((self.ids[a], self.ids[b]))
        return out

    def dist(self, a: str, b: str) -> float:
        (ax, ay), (bx, by) = self.tile[a], self.tile[b]
        return math.hypot(ax - bx, ay - by)

    def link(self, khu_a: int, khu_b: int, near: tuple, min_border: int = 4) -> tuple[str, str]:
        """The touching pair of cells across the border of two khu whose middle is nearest `near`."""
        best = None
        for (a, b), c in self.touch.items():
            if c < min_border:
                continue
            ia, ib = self.ids[a], self.ids[b]
            ra, rb = self.region_of[ia], self.region_of[ib]
            if {ra, rb} != {khu_a, khu_b}:
                continue
            (ax, ay), (bx, by) = self.tile[ia], self.tile[ib]
            d = math.hypot((ax + bx) / 2 - near[0], (ay + by) / 2 - near[1])
            if best is None or d < best[0]:
                best = (d, ia if ra == khu_a else ib, ib if ra == khu_a else ia)
        if best is None:
            raise ValueError(f"no cells touch between khu {khu_a} and {khu_b}")
        return best[1], best[2]

    def tree(self, pairs: list[tuple], rng: random.Random, extra: int = 0, keep=()) -> list[tuple]:
        """A spanning tree of `pairs` (Kruskal on the distance, a little jittered), the pairs of
        `keep` always in it, plus `extra` more pairs (each one closes a loop)."""
        parent: dict[str, str] = {}

        def find(a):
            while parent.setdefault(a, a) != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        chosen = []
        for a, b in keep:
            parent[find(a)] = find(b)
            chosen.append((a, b))
        order = sorted(pairs, key=lambda p: self.dist(*p) * (0.75 + 0.5 * rng.random()))
        rest = []
        for a, b in order:
            if (a, b) in chosen or (b, a) in chosen:
                continue
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                chosen.append((a, b))
            else:
                rest.append((a, b))
        rng.shuffle(rest)
        return chosen + rest[:extra]


# ------------------------------------------------------------------ the forest: walls of trees
def glade_walls(m: DaiDiaDo, cells: Cells, kind_of_region=None, skip=None) -> int:
    """A wall two tiles thick on every border between two cells of the same khu: solid, drawn as
    a tree line (`kind_of_region(region) -> barrier kind`, default "trees"); the roads cut
    passes through them later. `skip(x, y)` keeps a tile open."""
    W, H = m.W, m.H
    own = cells.owner
    n = 0
    marks = set()
    for y in range(2, H - 3):
        for x in range(2, W - 3):
            j = y * W + x
            a = own[j]
            if a < 0:
                continue
            for k in (j + 1, j + W):
                b = own[k]
                if b >= 0 and b != a and m.region[k] == m.region[j]:
                    marks.add(j)
                    marks.add(k)
    for j in sorted(marks):
        x, y = j % W, j // W
        if m.keep[j] or m.hard[j] or (skip and skip(x, y)):
            continue
        kind = kind_of_region(m.region[j]) if kind_of_region else "trees"
        m.barrier[j] = kind
        m.hard[j] = SOLID_WALL
        m.setg(x, y, "dark_grass1" if (x * 7 + y * 3) % 3 else "dark_grass0")
        n += 1
    return n


# ------------------------------------------------------------------ the marsh: islands in water
def islands(m: DaiDiaDo, cells: Cells, radius: dict, jitter: float = 0.28, salt: int = 71,
            keep_land=None) -> set:
    """Land within `radius[seed]` (tiles, noisy) of each seed, water everywhere else (solid, no
    bank). `keep_land(x, y)` keeps a tile dry. Returns the water tiles."""
    W, H = m.W, m.H
    nz = m.noise
    wet = set()
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            j = y * W + x
            if m.keep[j]:
                continue
            o = cells.owner[j]
            if o >= 0:
                sid = cells.ids[o]
                sx, sy = cells.tile[sid]
                r = radius.get(sid, 0)
                d = math.hypot(x - sx, (y - sy) * 1.12)
                if r and d <= r * (1 + (nz.fbm(x, y, 7.0, 2, salt) - 0.5) * 2 * jitter):
                    continue
            if keep_land and keep_land(x, y):
                continue
            wet.add((x, y))
    m._wet(wet, "water0", SOLID_WATER, None)
    return wet


# ------------------------------------------------------------------ signposts
def _direction(path: list) -> str:
    a = path[0]
    tip = path[min(len(path) - 1, 12)]
    dx, dy = tip[0] - a[0], tip[1] - a[1]
    d = (1 if dx > 0 else -1, 0) if abs(dx) > abs(dy) else (0, 1 if dy > 0 else -1)
    return ARROWS[d]


def route_signs(m: DaiDiaDo, named: dict, at=None, min_degree: int = 3, dead_end_vi: str = "ngõ cụt",
                loop_vi: str = "vòng lại", max_lines: int = 4) -> int:
    """A signpost by every node with `min_degree` roads or more (and by the nodes of `at`): one
    line per way out, "Bắc → <the nearest place of `named` whose shortest way leaves by it>";
    a way out that leads only to places with no name says `dead_end_vi` when it is a branch
    with no other way back, else `loop_vi`. `named`: node id -> label."""
    adj: dict[str, list] = {}
    for e in m.edges:
        w = len(e["path"])
        adj.setdefault(e["a"], []).append((e["b"], w, e["path"]))
        adj.setdefault(e["b"], []).append((e["a"], w, e["path"][::-1]))
    at = set(at or ())
    n_signs = 0
    for nid in sorted(adj):
        ways = adj[nid]
        if len(ways) < min_degree and nid not in at:
            continue
        # Dijkstra from nid, remembering the first way taken
        dist = {nid: 0}
        first: dict[str, int] = {}
        q = []
        for i, (b, w, _p) in enumerate(ways):
            if w < dist.get(b, 1e18):
                dist[b] = w
                first[b] = i
                heapq.heappush(q, (w, b))
        while q:
            d, u = heapq.heappop(q)
            if d > dist.get(u, 1e18):
                continue
            for v, w, _p in adj.get(u, ()):
                if v == nid:
                    continue
                if d + w < dist.get(v, 1e18):
                    dist[v] = d + w
                    first[v] = first[u]
                    heapq.heappush(q, (d + w, v))
        lines = []
        for i, (b, w, p) in enumerate(ways):
            best = None
            for v, lab in named.items():
                if v != nid and first.get(v) == i and (best is None or dist[v] < best[0]):
                    best = (dist[v], lab)
            if best is None:
                # a branch: removing nid cuts b off from the rest
                seen = {nid, b}
                stack = [b]
                back = False
                while stack and not back:
                    u = stack.pop()
                    for v, _w, _p in adj.get(u, ()):
                        if v == nid and u != b:
                            back = True
                            break
                        if v not in seen:
                            seen.add(v)
                            stack.append(v)
                label = loop_vi if back else dead_end_vi
            else:
                label = best[1]
            d = _direction(p)
            text = f"{d} → {label}"
            if text not in [t for _o, t in lines]:
                lines.append((list(ARROWS.values()).index(d), text))
        if len(lines) < 2:
            continue
        spot = m.free_near(*m.nodes[nid]["tile"], radius=4)
        if spot is None:
            continue
        m.sign("Biển chỉ đường", "\n".join(t for _o, t in sorted(lines)[:max_lines]), *spot)
        m.sign_tiles.append(spot)
        n_signs += 1
    return n_signs


# ------------------------------------------------------------------ monsters
def fill(m: DaiDiaDo, kid: str, kinds: list, elites: list = (), cell: tuple = (18, 14),
         tiles_per: float = 200.0, min_walk: float = 0.4, skip=None, max_areas: int | None = None,
         rng: random.Random | None = None) -> int:
    """DaiDiaDo.monsters for a khu that is partly water: a cell is kept when at least `min_walk`
    of it is walkable and reached (and 80 % of that on this khu's side), clear of gates, spawns
    and camps. Kinds take the cells by weight; `elites` (kind, n) one-elite areas in kept cells."""
    rng = rng or m.rng
    k = next(q for q in m.khus if q.id == kid)
    ri = m.bands_khu.index(k)
    clearance = int(rules()["clearance_tiles"])
    x0, y0, x1, y1 = k.rect
    cw, ch = cell
    nx = max(1, (x1 - x0 + 1 - 4) // cw)
    ny = max(1, (y1 - y0 + 1 - 4) // ch)
    ox = x0 + 2 + ((x1 - x0 + 1 - 4) - nx * cw) // 2
    oy = y0 + 2 + ((y1 - y0 + 1 - 4) - ny * ch) // 2
    cells = []
    for j in range(ny):
        for i in range(nx):
            r = (ox + i * cw, oy + j * ch, ox + (i + 1) * cw - 2, oy + (j + 1) * ch - 2)
            if not m._clear_ok(r, clearance) or (skip and skip(r)):
                continue
            walk, mine = m._walk_count(r, ri)
            area = (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
            if walk < min_walk * area or mine < 0.8 * walk:
                continue
            cells.append((r, walk))
    rng.shuffle(cells)
    if max_areas is not None:
        cells = cells[:max_areas]
    bag = [kind for kind, w in kinds for _ in range(int(w))]
    total = 0
    for n, (r, walk) in enumerate(cells):
        if not bag:
            break
        cnt = max(1, int(round(walk / tiles_per)))
        m.monster_area(kid, bag[n % len(bag)], r, cnt)
        total += cnt
    picks = sorted(cells, key=lambda c: rng.random())
    e = 0
    for kind, n in elites:
        for _ in range(int(n)):
            if not picks:
                break
            r, _w = picks[e % len(picks)]
            e += 1
            cx, cy = (r[0] + r[2]) // 2, (r[1] + r[3]) // 2
            inner = (cx - 4, cy - 4, cx + 4, cy + 4)
            m.monster_area(kid, kind, inner, 1, name=f"{kid}_{kind}_tinh_anh_{e}")
            total += 1
    return total


def overlaps(r: tuple, rects) -> bool:
    return any(not (r[2] < a[0] or a[2] < r[0] or r[3] < a[1] or a[3] < r[1]) for a in rects)


def tiles_of(rect: tuple) -> set:
    x0, y0, x1, y1 = rect
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


__all__ = ["Builder", "Cells", "fill", "glade_walls", "islands", "overlaps", "route_signs", "spread", "tiles_of",
           "T"]
