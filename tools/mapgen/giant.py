"""Đại Địa Đồ: the toolkit for the giant lands (docs/DAI_DIA_DO.md is the guide).

A giant land is a ``DaiDiaDo`` (a MapBuilder) built in this order, every step deterministic from
the seed:

1. ``khu(...)`` / ``camp(...)``     declare the sub-areas: their tile rectangles, band, theme, anchor;
2. ``paint()``                      paint the ground of every tile from the theme of its khu (borders
                                    wobble with a domain warp, so no khu looks like a rectangle);
3. ``river`` / ``lake`` / ``chasm`` the large features (water and ink are solid tiles);
4. ``barriers({...})``              natural walls between neighbouring khu (trees, cliff, chasm, water);
5. ``network(nodes, edges)``        the roads from the gate through the camps to every anchor and
                                    landmark; a road crossing water is a bridge, crossing a barrier
                                    a pass, crossing a chasm a land bridge;
6. the module's own places          (``thing``, ``sign``, ``building``, ``landmark``, ``poi``...);
7. ``signposts()``                  a sign at every junction naming where each road leads;
8. ``monsters(...)`` / ``monster_area(...)``   the monster areas of each khu (band, khu, realm);
9. ``scatter()``                    props by a density map per theme, clumped by noise;
10. ``finish(...)``                 the ring, collision of the solid tiles, the khu and poi
                                    objects, the checks of the budget -> the Tiled map dict.

Tiles are (x, y) in tiles; a rectangle (x0, y0, x1, y1) includes both corners.
"""
from __future__ import annotations

import heapq
import json
import math
import zlib
from dataclasses import dataclass, field

from .builder import GID, ROOT, T, MapBuilder

DIA_DO = ROOT / "server" / "data" / "math" / "dia_do.json"
COMBAT = ROOT / "server" / "data" / "balance" / "combat.json"
LEASH_SHARE = 0.8      # a monster area's half diagonal stays within this share of the leash


def max_area_half_diagonal() -> float:
    """Pixels: a monster pulled from anywhere in its area must stay within its leash (a monster
    dragged further than `leash_radius` from the middle of its area gives up the fight)."""
    return LEASH_SHARE * float(json.loads(COMBAT.read_text("utf-8"))["leash_radius"])

# ------------------------------------------------------------------ noise
_M = 0xFFFFFFFF


def _hash(ix: int, iy: int, s: int) -> float:
    h = (ix * 374761393 + iy * 668265263 + s * 2246822519) & _M
    h = ((h ^ (h >> 13)) * 1274126177) & _M
    return ((h ^ (h >> 16)) & _M) / 4294967296.0


class Noise:
    """Smooth value noise in [0, 1], the same for the same seed on every machine."""

    def __init__(self, seed: str):
        self.s = zlib.crc32(seed.encode("utf-8"))

    def value(self, x: float, y: float, scale: float, salt: int = 0) -> float:
        fx, fy = x / scale, y / scale
        ix, iy = math.floor(fx), math.floor(fy)
        tx, ty = fx - ix, fy - iy
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
        s = (self.s + salt * 7919) & _M
        a, b = _hash(ix, iy, s), _hash(ix + 1, iy, s)
        c, d = _hash(ix, iy + 1, s), _hash(ix + 1, iy + 1, s)
        return (a + (b - a) * tx) + ((c + (d - c) * tx) - (a + (b - a) * tx)) * ty

    def fbm(self, x: float, y: float, scale: float, octaves: int = 3, salt: int = 0) -> float:
        tot, amp, norm = 0.0, 1.0, 0.0
        for o in range(octaves):
            tot += amp * self.value(x, y, scale / (2 ** o), salt + o * 101)
            norm += amp
            amp *= 0.5
        return tot / norm


def smooth(lo: float, hi: float, v: float) -> float:
    t = min(1.0, max(0.0, (v - lo) / (hi - lo)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ props and themes
@dataclass(frozen=True)
class Prop:
    """What scatter() may put down: a tree (``tree`` with its collision at the trunk) or a
    ``thing`` (rect w x h standing on its tile, solid ``foot`` or walk-through)."""
    kind: str                 # "tree" or "thing"
    sprite: str
    name: str = ""
    w: int = 16
    h: int = 16
    foot: tuple | None = None
    big: bool = False         # takes 3 x 2 tiles of room instead of one


PROPS = {
    "tree": Prop("tree", "tree", big=True),
    "pine": Prop("tree", "pine", big=True),
    "peach": Prop("tree", "peach", big=True),
    "dead_tree": Prop("tree", "ink_tree", big=True),
    "rock": Prop("thing", "rock", "Đá", 16, 12, (12, 8)),
    "boulder": Prop("thing", "boulder", "Tảng đá", 32, 24, (26, 10), big=True),
    "bush": Prop("thing", "bush", "Bụi cây", 24, 16),
    "tall_grass": Prop("thing", "tall_grass", "Cỏ", 24, 16),
    "stump": Prop("thing", "stump", "Gốc cây", 24, 16, (18, 8)),
    "log": Prop("thing", "log", "Khúc gỗ", 24, 16, (18, 8)),
    "crystal": Prop("thing", "crystal", "Tinh thạch", 24, 32, (14, 8)),
    "cloud": Prop("thing", "cloud_puff", "Mây", 32, 20, big=True),
    "grave": Prop("thing", "tablet", "Mộ kiếm", 16, 24, (12, 8)),
    "bamboo": Prop("thing", "bamboo", "Trúc", 16, 40, (12, 6)),
    "lantern": Prop("thing", "lantern", "Đèn", 8, 24, (4, 4)),
}
# every sprite above has a picture: client/engine/sprites.py (old) or client/assets/v2/wiring.json


def _pick(table, r: float) -> str:
    tot = sum(w for _, w in table)
    acc = 0.0
    for name, w in table:
        acc += w / tot
        if r < acc:
            return name
    return table[-1][0]


@dataclass
class Theme:
    """How a khu looks: ``ground(P, D, r)`` -> a TILESET key, from a large-patch noise P, a
    detail noise D (both 0..1) and a per-tile random r; props in the open and in the clumps (a
    noise of scale ``clump`` above ``clump_cut`` is a clump); densities are props per tile."""
    name: str
    ground: object
    open_props: list
    dense_props: list
    open_density: float = 0.02
    dense_density: float = 0.10
    clump: float = 18.0
    clump_cut: float = 0.58
    road: tuple = ()          # the road tiles here ((): path); a dirt land paves its roads


def _g(fn):
    return fn


def g_meadow(P, D, r):
    if P > 0.68 and D > 0.42:
        return "flowers1" if r < 0.5 else "flowers0"
    if P < 0.24:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    return "grass0" if r < 0.55 else "grass1" if r < 0.86 else "grass2"


def g_flower_meadow(P, D, r):
    if P > 0.52 and D > 0.38:
        return "flowers1" if r < 0.5 else "flowers0"
    return "grass0" if r < 0.5 else "grass1" if r < 0.85 else "grass2"


def g_foothill(P, D, r):
    if P < 0.32:
        return "dark_grass0" if r < 0.75 else "dark_grass1"
    if P > 0.74 and D > 0.5:
        return "dirt0"
    return "grass1" if r < 0.5 else "grass0" if r < 0.88 else "grass2"


def g_pine(P, D, r):
    if P > 0.54:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    if P < 0.22 and D > 0.55:
        return "dirt0"
    return "grass1" if r < 0.6 else "grass0" if r < 0.9 else "grass2"


def g_dark_wood(P, D, r):
    if P < 0.22:
        return "grass1" if r < 0.7 else "grass2"
    if P > 0.80 and D > 0.55:
        return "dirt0"
    return "dark_grass0" if r < 0.6 else "dark_grass1"


def g_stone(P, D, r):
    if P < 0.28:
        return "dirt0"
    if P < 0.46:
        return "grass1" if r < 0.7 else "grass2"
    if P > 0.74:
        return "dark_grass0" if r < 0.75 else "dark_grass1"
    return "stone0"


def g_sword_field(P, D, r):
    if P > 0.60:
        return "stone0"
    if P < 0.18:
        return "dark_grass1"
    return "dirt0"


def g_peak(P, D, r):
    if P < 0.30:
        return "dirt0"
    if P > 0.72:
        return "dark_grass1" if r < 0.7 else "dark_grass0"
    return "stone0"


def g_waste(P, D, r):
    if P > 0.62:
        return "stone0"
    if P < 0.22:
        return "dark_grass0" if r < 0.75 else "dark_grass1"
    return "dirt0"


def g_cloud_plateau(P, D, r):
    if P < 0.38:
        return "grass1" if r < 0.7 else "grass2"
    if P > 0.78:
        return "dirt0"
    return "stone0"


def g_bank(P, D, r):
    if P > 0.72:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    if P < 0.18 and D > 0.5:
        return "flowers0" if r < 0.6 else "flowers1"
    return "grass0" if r < 0.5 else "grass1" if r < 0.85 else "grass2"


PAVED = ("plaza0", "plaza1")
THEMES: dict[str, Theme] = {
    "dong_co": Theme("dong_co", g_meadow,
                     [("bush", 3), ("tall_grass", 4), ("rock", 1), ("tree", 2), ("stump", 1)],
                     [("tree", 5), ("bush", 2), ("peach", 1), ("tall_grass", 1)], 0.045, 0.16),
    "dong_hoa": Theme("dong_hoa", g_flower_meadow,
                      [("tall_grass", 3), ("bush", 2), ("rock", 1), ("peach", 2)],
                      [("peach", 5), ("bush", 2), ("tree", 1)], 0.045, 0.15),
    "chan_nui": Theme("chan_nui", g_foothill,
                      [("rock", 3), ("tall_grass", 3), ("bush", 2), ("grave", 1), ("stump", 1), ("pine", 2)],
                      [("pine", 4), ("tree", 2), ("dead_tree", 1), ("boulder", 1)], 0.045, 0.16),
    "rung_thong": Theme("rung_thong", g_pine,
                        [("pine", 4), ("bush", 2), ("stump", 1), ("rock", 1), ("tall_grass", 2), ("log", 1)],
                        [("pine", 7), ("tree", 2), ("log", 1)], 0.05, 0.24, 16.0, 0.5),
    "rung_toi": Theme("rung_toi", g_dark_wood,
                      [("stump", 2), ("rock", 2), ("log", 1), ("bush", 1), ("dead_tree", 3)],
                      [("dead_tree", 6), ("tree", 1), ("rock", 1)], 0.05, 0.22, 16.0, 0.52),
    "thach_lam": Theme("thach_lam", g_stone,
                       [("rock", 4), ("boulder", 2), ("tall_grass", 2), ("crystal", 1), ("bush", 1), ("pine", 1)],
                       [("boulder", 4), ("pine", 3), ("rock", 2)], 0.045, 0.16, 14.0, 0.56),
    "bai_kiem": Theme("bai_kiem", g_sword_field,
                      [("grave", 5), ("rock", 2), ("dead_tree", 1), ("tall_grass", 1)],
                      [("grave", 6), ("rock", 2), ("dead_tree", 2), ("boulder", 1)], 0.045, 0.15, 12.0, 0.55,
                      PAVED),
    "dinh_nui": Theme("dinh_nui", g_peak,
                      [("rock", 3), ("crystal", 2), ("cloud", 2), ("grave", 1), ("tall_grass", 1)],
                      [("boulder", 4), ("crystal", 2), ("dead_tree", 1), ("pine", 1)], 0.045, 0.14),
    "dat_hoang": Theme("dat_hoang", g_waste,
                       [("rock", 3), ("tall_grass", 3), ("stump", 1), ("dead_tree", 2), ("bush", 1), ("log", 1)],
                       [("dead_tree", 4), ("rock", 2), ("boulder", 2), ("tall_grass", 1)], 0.045, 0.16, 16.0, 0.55,
                       PAVED),
    "cao_nguyen": Theme("cao_nguyen", g_cloud_plateau,
                        [("cloud", 3), ("rock", 3), ("crystal", 1), ("tall_grass", 1), ("pine", 1)],
                        [("boulder", 4), ("pine", 2), ("cloud", 2)], 0.045, 0.14),
    "bai_suoi": Theme("bai_suoi", g_bank,
                      [("tall_grass", 4), ("bush", 3), ("rock", 1), ("log", 1), ("tree", 2)],
                      [("tree", 4), ("pine", 1), ("bush", 2)], 0.045, 0.16),
}

BARRIER_LOOK = {   # kind -> (ground keys, decoration prop names, radius in tiles)
    "trees": (("dark_grass0", "dark_grass1"), ("tree", "pine"), 1),
    "pines": (("dark_grass0", "dark_grass1"), ("pine",), 1),
    "dead_trees": (("dark_grass1",), ("dead_tree",), 1),
    "cliff": (("stone0",), ("boulder", "rock"), 2),
    "chasm": (("ink0", "ink1"), (), 2),
    "water": (("water0",), (), 1),
}
SOLID_WATER, SOLID_PIT, SOLID_WALL = 1, 2, 3
ROAD_STYLE = {"main": (("path0", "path1"), 1), "trail": (("path1", "path0"), 0)}
# the game's fonts draw "→" but not the other arrows: a signpost names the direction in words
ARROWS = {(0, -1): "Bắc", (0, 1): "Nam", (-1, 0): "Tây", (1, 0): "Đông"}


def band_table(realm: str = "luyen_khi") -> dict:
    return json.loads(DIA_DO.read_text("utf-8"))["realms"][realm]


def rules() -> dict:
    return json.loads(DIA_DO.read_text("utf-8"))["distribution"]


@dataclass
class Khu:
    id: str
    name_vi: str
    band: int
    rect: tuple            # tiles, inclusive
    theme: str
    anchor: tuple          # a walkable tile
    desc_vi: str = ""
    camp: bool = False
    realm: str = "luyen_khi"
    stage_min: int = 0
    stage_max: int = 0
    areas: list = field(default_factory=list)


class DaiDiaDo(MapBuilder):
    """A giant land. See the module docstring for the order of the steps."""

    def __init__(self, zone: str, name_vi: str, w: int, h: int, seed: str, realm: str = "luyen_khi"):
        super().__init__(zone, name_vi, w, h, seed)
        self.realm = realm
        self.noise = Noise(seed)
        self.themes = dict(THEMES)
        self.khus: list[Khu] = []           # camps first (they win where they overlap)
        n = w * h
        self.region = [-1] * n              # index into self.bands_khu
        self.hard = bytearray(n)           # SOLID_* of a tile, 0 = free
        self.road = bytearray(n)            # 1 road, 2 bridge, 3 pass, 4 land bridge
        self.barrier = [None] * n           # the barrier kind of a tile
        self.keep = bytearray(n)            # no barrier, no scatter (camps, landmarks)
        self.soft = bytearray(n)            # scatter puts only walk-through props here (soft_rect)
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []
        self.pois: list[tuple] = []
        self.clear_zones: list[tuple] = []  # rects nothing may spawn near (gates, spawns, camps)
        self.sign_tiles: list[tuple] = []

    # ---------------------------------------------------------------- grid helpers
    def i(self, x: int, y: int) -> int:
        return y * self.W + x

    def inside(self, x: int, y: int, margin: int = 0) -> bool:
        return margin <= x < self.W - margin and margin <= y < self.H - margin

    def key_at(self, x: int, y: int) -> str:
        gid = self.ground[self.i(x, y)]
        return next(k for k, v in GID.items() if v == gid)

    # ---------------------------------------------------------------- 1. the khu
    @property
    def bands_khu(self) -> list[Khu]:
        return [k for k in self.khus if not k.camp]

    def khu(self, kid: str, name_vi: str, band: int, rect: tuple, theme: str, anchor: tuple,
            desc_vi: str = "") -> Khu:
        """A khu of band 1..3: its tile rectangle, the theme of its ground, the walkable tile
        Chỉ Đường leads to (keep it on a road: network() nodes are the natural anchors)."""
        if theme not in self.themes:
            raise ValueError(f"khu {kid}: unknown theme {theme!r}")
        b = band_table(self.realm)[str(band)]
        k = Khu(kid, name_vi, band, tuple(rect), theme, tuple(anchor), desc_vi, False, self.realm,
                int(b["stage_min"]), int(b["stage_max"]))
        self.khus.append(k)
        return k

    def camp(self, kid: str, name_vi: str, center: tuple, r: int = 6, desc_vi: str = "",
             label_vi: str | None = None, to_edge: str | None = None) -> Khu:
        """A rest camp: a band 0 khu (no monster within the clearance), a plaza with lanterns, a
        well and mats, a road node of the same id and a poi. Call after paint(). `to_edge` ("n",
        "s", "w", "e") stretches the camp's khu to that edge of the map: the gate camp, so the
        gate and the arrival spawns lie inside it (a spawn always lies in a band 0 khu)."""
        cx, cy = center
        x0, y0, x1, y1 = (cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2)
        if to_edge == "s":
            y1 = self.H - 1
        elif to_edge == "n":
            y0 = 0
        elif to_edge == "w":
            x0 = 0
        elif to_edge == "e":
            x1 = self.W - 1
        rect = (x0, y0, x1, y1)
        k = Khu(kid, name_vi, 0, rect, "camp", (cx, cy + 1), desc_vi, True, self.realm, 0, 0)
        self.khus.insert(sum(1 for q in self.khus if q.camp), k)
        for y in range(cy - r - 2, cy + r + 3):
            for x in range(cx - r - 2, cx + r + 3):
                if not self.inside(x, y, 1):
                    continue
                d = math.hypot(x - cx, (y - cy) * 1.15)
                j = self.i(x, y)
                if d <= r + 2:
                    self.hard[j] = 0
                    self.barrier[j] = None
                if d <= r - 1:
                    self.setg(x, y, "plaza0" if (x + y) % 3 else "plaza1")
                elif d <= r:
                    self.setg(x, y, "dirt0")
                if d <= r + 1:
                    self.keep[j] = 1
        for i, (dx, dy) in enumerate(((-r + 1, -2), (r - 1, -2), (-r + 1, 3), (r - 1, 3))):
            self.thing("Đèn trại", "lantern", cx + dx, cy + dy, 8, 24, foot=(4, 4), variant=i)
        self.thing("Giếng", "well", cx + 2, cy - 2, 24, 24, foot=(20, 12))
        self.thing("Chiếu nghỉ", "mat", cx - 3, cy + 2, 24, 16)
        self.thing("Chiếu nghỉ", "mat", cx - 3, cy - 2, 24, 16)
        self.node(kid, (cx, cy), label_vi or f"{name_vi} (nghỉ chân)")
        self.poi("camp", name_vi, cx, cy)
        self.clear_zones.append(rect)
        return k

    # ---------------------------------------------------------------- 2. the ground
    def paint(self, warp: float = 7.0, scale: float = 24.0, default: int = 0) -> None:
        """The ground of every tile from the theme of its khu; khu borders wobble by `warp` tiles."""
        bk = self.bands_khu
        W, H = self.W, self.H
        nz = self.noise
        for y in range(H):
            for x in range(W):
                wx = x + max(-1.0, min(1.0, (nz.fbm(x, y, scale, 2, 1) - 0.5) * 4)) * warp
                wy = y + max(-1.0, min(1.0, (nz.fbm(x, y, scale, 2, 2) - 0.5) * 4)) * warp
                ri = default
                best = None
                for n, k in enumerate(bk):
                    x0, y0, x1, y1 = k.rect
                    if x0 <= wx <= x1 + 1 and y0 <= wy <= y1 + 1:
                        ri = n
                        break
                    d = max(x0 - wx, wx - x1 - 1, 0) + max(y0 - wy, wy - y1 - 1, 0)
                    if best is None or d < best[0]:
                        best = (d, n)
                else:
                    ri = best[1] if best else default
                j = y * W + x
                self.region[j] = ri
                P = nz.fbm(x, y, 14.0, 2, 3)
                D = nz.fbm(x, y, 5.0, 2, 4)
                th = self.themes[bk[ri].theme]
                self.ground[j] = GID[th.ground(P, D, self.rng.random())]

    def region_khu(self, x: int, y: int) -> Khu | None:
        r = self.region[self.i(x, y)]
        return self.bands_khu[r] if r >= 0 else None

    # ---------------------------------------------------------------- 3. features
    def _wet(self, tiles, key: str, code: int, bank: str | None) -> set:
        tiles = {(x, y) for x, y in tiles if self.inside(x, y, 1)}
        for (x, y) in tiles:
            j = self.i(x, y)
            self.setg(x, y, key if key != "ink" else ("ink0" if (x * 3 + y) % 4 else "ink1"))
            self.hard[j] = code
            self.barrier[j] = None
        if bank:
            for (x, y) in tiles:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        n = (x + dx, y + dy)
                        if n not in tiles and self.inside(*n, 1) and not self.hard[self.i(*n)] \
                                and not self.keep[self.i(*n)]:
                            self.setg(n[0], n[1], bank)
        return tiles

    def river(self, points, width: int = 3, bank: str | None = "stone0") -> set:
        """Water along a line of tile points (consecutive points are joined), `width` tiles wide."""
        tiles: set = set()
        pts = [(float(a), float(b)) for a, b in points]
        half = (width - 1) / 2
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            steps = max(1, int(max(abs(bx - ax), abs(by - ay)) * 2))
            for s in range(steps + 1):
                cx, cy = ax + (bx - ax) * s / steps, ay + (by - ay) * s / steps
                for x in range(int(cx - half - 1), int(cx + half + 2)):
                    for y in range(int(cy - half - 1), int(cy + half + 2)):
                        if abs(x - cx) <= half + 0.01 and abs(y - cy) <= half + 0.01:
                            tiles.add((x, y))
        return self._wet(tiles, "water0", SOLID_WATER, bank)

    def blob(self, cx: float, cy: float, rx: float, ry: float, jitter: float = 0.25, salt: int = 21) -> set:
        """The tiles of a noisy ellipse."""
        out = set()
        for y in range(int(cy - ry * 1.4) - 1, int(cy + ry * 1.4) + 2):
            for x in range(int(cx - rx * 1.4) - 1, int(cx + rx * 1.4) + 2):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1 + (self.noise.fbm(x, y, 6.0, 2, salt) - 0.5) * 2 * jitter * 2:
                    out.add((x, y))
        return out

    def lake(self, cx, cy, rx, ry, bank: str | None = "stone0", fishing: bool = False) -> set:
        tiles = self._wet(self.blob(cx, cy, rx, ry), "water0", SOLID_WATER, bank)
        if fishing and tiles:
            xs, ys = [x for x, _ in tiles], [y for _, y in tiles]
            self.obj("lake", "area", min(xs) * T, min(ys) * T, (max(xs) - min(xs) + 1) * T,
                     (max(ys) - min(ys) + 1) * T, kind="fishing", pool="ho")
        return tiles

    def chasm(self, tiles) -> set:
        """Ink nobody walks on (a chasm, the deep): solid."""
        return self._wet(tiles, "ink", SOLID_PIT, None)

    def wall(self, tiles, key: str = "stone0") -> None:
        """Solid ground of another kind (a cliff face, a wall): solid tiles drawn as `key`."""
        for (x, y) in tiles:
            if self.inside(x, y):
                self.setg(x, y, key)
                self.hard[self.i(x, y)] = SOLID_WALL

    def open_tiles(self, tiles, key: str | None = None) -> None:
        """Make tiles walkable again (and optionally repaint them)."""
        for (x, y) in tiles:
            if self.inside(x, y):
                j = self.i(x, y)
                self.hard[j] = 0
                self.barrier[j] = None
                if key:
                    self.setg(x, y, key)

    def soft_rect(self, x0, y0, x1, y1) -> None:
        """Ground to fight on: scatter() puts no solid prop in these tiles (grass and bushes only),
        so a dodge or a chase is never stopped by a rock that happens to stand there."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.inside(x, y):
                    self.soft[self.i(x, y)] = 1

    def keep_rect(self, x0, y0, x1, y1) -> None:
        """No barrier, no road detour and no scatter in these tiles (a landmark's ground)."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.inside(x, y):
                    self.keep[self.i(x, y)] = 1

    # ---------------------------------------------------------------- 4. barriers
    def barriers(self, kinds: dict, default: str = "trees") -> None:
        """Walls between neighbouring khu (on the warped borders): `kinds` maps a pair of khu ids
        (a frozenset or a tuple) to "trees", "pines", "dead_trees", "cliff", "chasm", "water" or
        "open" (no wall). Roads cut passes through them later."""
        lookup = {frozenset(k): v for k, v in kinds.items()}
        bk = self.bands_khu
        W, H = self.W, self.H
        for y in range(2, H - 2):
            for x in range(2, W - 2):
                j = y * W + x
                if self.keep[j] or self.hard[j]:
                    continue
                me = self.region[j]
                kind = None
                for rad in (1, 2):
                    for dy in range(-rad, rad + 1):
                        for dx in range(-rad, rad + 1):
                            o = self.region[(y + dy) * W + x + dx] if self.inside(x + dx, y + dy) else me
                            if o != me:
                                k = lookup.get(frozenset((bk[me].id, bk[o].id)), default)
                                if BARRIER_LOOK.get(k, (0, 0, 0))[2] >= rad and k != "open":
                                    kind = k
                        if kind:
                            break
                    if kind:
                        break
                if not kind:
                    continue
                look = BARRIER_LOOK[kind]
                self.barrier[j] = kind
                grounds = look[0]
                self.ground[j] = GID[grounds[(x * 7 + y * 3) % len(grounds)]]
                self.hard[j] = SOLID_WATER if kind == "water" else SOLID_PIT if kind == "chasm" else SOLID_WALL

    # ---------------------------------------------------------------- 5. roads
    def node(self, nid: str, tile: tuple, label_vi: str = "", sign: bool = True) -> None:
        """A place the roads join: a camp, a fork, a khu anchor, a landmark. `label_vi` is what a
        signpost elsewhere says when its road leads here; `sign`: put a signpost here."""
        self.nodes[nid] = {"tile": tuple(tile), "label": label_vi, "sign": sign, "edges": []}

    def _cost(self, x: int, y: int, chasm_ok: bool) -> float:
        if not self.inside(x, y, 2):
            return math.inf
        j = self.i(x, y)
        if self.road[j]:
            return 0.55
        s = self.hard[j]
        if s == SOLID_WATER:
            return 9.0
        if s == SOLID_PIT:
            return 16.0 if chasm_ok else math.inf
        if s == SOLID_WALL:
            return 28.0 if self.barrier[j] else math.inf
        if (x, y) in self.blocked_tiles:
            return 40.0
        return 1.0 + 1.6 * self.noise.fbm(x, y, 11.0, 2, 9)

    def path(self, a: tuple, b: tuple, chasm_ok: bool = False) -> list[tuple]:
        """The cheapest 4-way way from tile a to tile b (A*): roads attract, water and walls
        repel, a chasm is crossed only when `chasm_ok`."""
        W = self.W
        start, goal = a, b
        openq = [(0.0, 0.0, start)]
        came = {start: None}
        g = {start: 0.0}
        while openq:
            _, gc, cur = heapq.heappop(openq)
            if cur == goal:
                break
            if gc > g.get(cur, math.inf):
                continue
            x, y = cur
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                c = 0.0 if (nx, ny) == goal else self._cost(nx, ny, chasm_ok)
                if c == math.inf:
                    continue
                ng = gc + c
                if ng < g.get((nx, ny), math.inf):
                    g[(nx, ny)] = ng
                    came[(nx, ny)] = cur
                    h = 0.55 * (abs(nx - goal[0]) + abs(ny - goal[1]))
                    heapq.heappush(openq, (ng + h, ng, (nx, ny)))
        if goal not in came:
            raise ValueError(f"{self.zone}: no way from {a} to {b}")
        out, cur = [], goal
        while cur is not None:
            out.append(cur)
            cur = came[cur]
        return out[::-1]

    def carve(self, tiles, style: str = "main") -> None:
        keys, rad = ROAD_STYLE[style]
        for (cx, cy) in tiles:
            for dy in range(-rad, rad + 1) if rad else (0, 1):
                for dx in range(-rad, rad + 1) if rad else (0, 1):
                    x, y = cx + dx, cy + dy
                    if not self.inside(x, y, 1):
                        continue
                    j = self.i(x, y)
                    if self.keep[j] and not self.road[j] and (dx or dy):
                        continue
                    s = self.hard[j]
                    if s == SOLID_WATER:
                        self.setg(x, y, "wood0")
                        self.road[j] = 2
                    elif s == SOLID_PIT:
                        self.setg(x, y, "stone0")
                        self.road[j] = 4
                    else:
                        if s == SOLID_WALL and self.barrier[j]:
                            self.road[j] = 3
                        elif not self.road[j]:
                            self.road[j] = 1
                        if self.road[j] in (1, 3) and not self.keep[j]:
                            th = self.themes[self.bands_khu[self.region[j]].theme] if self.region[j] >= 0 else None
                            ks = th.road if th is not None and th.road else keys
                            self.setg(x, y, ks[(x + y) % 2] if (x * 5 + y) % 3 else ks[0])
                    self.hard[j] = 0
                    self.barrier[j] = None
        # a pass is wider than its road: the wall steps back one more tile on each side
        for (cx, cy) in tiles:
            for dy in (-rad - 1, rad + 1):
                for dx in (-rad - 1, rad + 1):
                    x, y = cx + dx, cy + dy
                    if self.inside(x, y, 1) and self.barrier[self.i(x, y)] in ("trees", "pines", "dead_trees", "cliff"):
                        j = self.i(x, y)
                        self.hard[j] = 0
                        self.barrier[j] = None

    def network(self, edges) -> None:
        """Roads between nodes: edges are (a, b, style) with style "main" (3 tiles) or "trail"
        (2 tiles), optionally a 4th item True when the road may bridge a chasm."""
        for e in edges:
            a, b, style = e[0], e[1], e[2]
            chasm_ok = len(e) > 3 and bool(e[3])
            p = self.path(self.nodes[a]["tile"], self.nodes[b]["tile"], chasm_ok)
            self.carve(p, style)
            rec = {"a": a, "b": b, "style": style, "path": p}
            self.edges.append(rec)
            self.nodes[a]["edges"].append((b, p))
            self.nodes[b]["edges"].append((a, p[::-1]))

    # ---------------------------------------------------------------- 6. places
    def poi(self, kind: str, name_vi: str, tx: int, ty: int, w: int = 1, h: int = 1) -> None:
        """A named place the big map lists (gate, camp, bi_canh, npc, beast, boss, landmark)."""
        self.pois.append((kind, name_vi, tx, ty, w, h))

    def landmark(self, name_vi: str, tx: int, ty: int, poi: str = "landmark") -> None:
        self.poi(poi, name_vi, tx, ty)

    def free_near(self, tx: int, ty: int, radius: int = 4, off_road: bool = True) -> tuple | None:
        """The nearest tile to (tx, ty) where a sign or a small prop can stand."""
        best = None
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x, y = tx + dx, ty + dy
                if not self.inside(x, y, 2):
                    continue
                j = self.i(x, y)
                if self.hard[j] or (off_road and self.road[j]) or (x, y) in self.blocked_tiles:
                    continue
                if off_road and not any(self.road[self.i(x + a, y + b)] for a in (-1, 0, 1) for b in (-1, 0, 1)
                                        if self.inside(x + a, y + b)):
                    continue
                d = dx * dx + dy * dy
                if best is None or d < best[0]:
                    best = (d, (x, y))
        return best[1] if best else None

    # ---------------------------------------------------------------- 7. signposts
    def signposts(self) -> int:
        """A signpost by every node marked `sign` with two roads or more: one line per way out,
        its direction (where the road heads over the next dozen tiles: Bắc, Nam, Đông, Tây) and
        where it leads, "Bắc → Trại Luyện Kiếm · cửa Trung Vực"."""
        n = 0
        for nid, nd in self.nodes.items():
            if not nd["sign"] or len(nd["edges"]) < 2:
                continue
            lines = []
            seen = set()
            for other, p in nd["edges"]:
                tip = p[min(len(p) - 1, 12)]
                dx, dy = tip[0] - nd["tile"][0], tip[1] - nd["tile"][1]
                d = (1 if dx > 0 else -1, 0) if abs(dx) > abs(dy) else (0, 1 if dy > 0 else -1)
                label = self.nodes[other]["label"]
                if not label or (d, label) in seen:
                    continue
                seen.add((d, label))
                lines.append((list(ARROWS).index(d), f"{ARROWS[d]} → {label}"))
            if len(lines) < 2:
                continue
            spot = self.free_near(*nd["tile"], radius=4)
            if spot is None:
                continue
            text = "\n".join(t for _, t in sorted(lines))
            self.sign("Biển chỉ đường", text, *spot)
            self.sign_tiles.append(spot)
            n += 1
        return n

    # ---------------------------------------------------------------- 8. monsters
    def _clear_ok(self, rect: tuple, clearance: int) -> bool:
        x0, y0, x1, y1 = rect
        for (a0, b0, a1, b1) in self.clear_zones:
            dx = max(a0 - x1 - 1, x0 - a1 - 1, 0)       # whole tiles between the two
            dy = max(b0 - y1 - 1, y0 - b1 - 1, 0)
            if max(dx, dy) < clearance:
                return False
        return True

    def reach(self) -> bytearray:
        """The tiles that can be walked to from the first road node (the gate), on the ground
        alone (props aside): monster areas are cut from these."""
        if getattr(self, "_reach", None) is None:
            W = self.W
            seen = bytearray(W * self.H)
            start = next(iter(self.nodes.values()))["tile"]
            q = [start]
            seen[self.i(*start)] = 1
            while q:
                x, y = q.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if self.inside(nx, ny, 1):
                        j = ny * W + nx
                        if not seen[j] and not self.hard[j]:
                            seen[j] = 1
                            q.append((nx, ny))
            self._reach = seen
        return self._reach

    def _walk_count(self, rect: tuple, ri: int | None = None) -> tuple[int, int]:
        """(walkable tiles that can be walked to, of them in region ri) of a rectangle."""
        x0, y0, x1, y1 = rect
        walk = mine = 0
        reach = self.reach()
        for y in range(max(0, y0), min(self.H, y1 + 1)):
            for x in range(max(0, x0), min(self.W, x1 + 1)):
                j = self.i(x, y)
                if not self.hard[j] and reach[j]:
                    walk += 1
                    if ri is None or self.region[j] == ri:
                        mine += 1
        return walk, mine

    def monster_area(self, kid: str, monster: str, rect: tuple, count: int, name: str | None = None) -> dict:
        """One monster_area (tile rect) of khu `kid`: band, khu and realm come from the khu."""
        k = next(q for q in self.khus if q.id == kid)
        x0, y0, x1, y1 = rect
        if math.hypot((x1 - x0 + 1) * T / 2, (y1 - y0 + 1) * T / 2) > max_area_half_diagonal():
            raise ValueError(f"{self.zone}: monster area {rect} of {kid} is larger than a monster's leash "
                             f"(at most about 20 x 15 tiles)")
        a = {"name": name or f"{kid}_{monster}_{len(k.areas)}", "monster": monster, "rect": tuple(rect),
             "count": int(count)}
        k.areas.append(a)
        self.obj(a["name"], "monster_area", x0 * T, y0 * T, (x1 - x0 + 1) * T, (y1 - y0 + 1) * T,
                 monster=monster, count=int(count), band=k.band, khu=k.id, realm=k.realm)
        return a

    def monsters(self, kid: str, kinds: list, elites: list = (), cell: tuple = (18, 14),
                 tiles_per: float = 190.0, inset: int = 2, skip=None, max_areas: int | None = None) -> int:
        """Fill khu `kid` with monster areas: its rectangle cut into cells, a cell kept when it is
        clear of gates, spawns and camps (the clearance of dia_do.json), mostly walkable and mostly
        on this khu's own side of the border; `kinds` (kind, weight) take the cells in turn by
        weight, one monster per `tiles_per` walkable tiles; `elites` (kind, n) add n areas of one
        elite each inside n of the kept cells. `skip(rect)` may veto a cell. Returns the count."""
        k = next(q for q in self.khus if q.id == kid)
        ri = self.bands_khu.index(k)
        clearance = int(rules()["clearance_tiles"])
        x0, y0, x1, y1 = k.rect
        cw, ch = cell
        nx = max(1, (x1 - x0 + 1 - 2 * inset) // cw)
        ny = max(1, (y1 - y0 + 1 - 2 * inset) // ch)
        ox = x0 + inset + ((x1 - x0 + 1 - 2 * inset) - nx * cw) // 2
        oy = y0 + inset + ((y1 - y0 + 1 - 2 * inset) - ny * ch) // 2
        cells = []
        for j in range(ny):
            for i in range(nx):
                r = (ox + i * cw, oy + j * ch, ox + (i + 1) * cw - 2, oy + (j + 1) * ch - 2)
                if not self._clear_ok(r, clearance) or (skip and skip(r)):
                    continue
                walk, mine = self._walk_count(r, ri)
                area = (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
                if walk < 0.55 * area or mine < 0.8 * walk:
                    continue
                cells.append((r, walk))
        self.rng.shuffle(cells)
        if max_areas is not None:
            cells = cells[:max_areas]
        bag = [kind for kind, w in kinds for _ in range(int(w))]
        total = 0
        for n, (r, walk) in enumerate(cells):
            kind = bag[n % len(bag)]
            cnt = max(1, int(round(walk / tiles_per)))
            self.monster_area(kid, kind, r, cnt)
            total += cnt
        picks = sorted(cells, key=lambda c: self.rng.random())
        e = 0
        for kind, n in elites:
            for _ in range(int(n)):
                if not picks:
                    break
                r, _w = picks[e % len(picks)]
                e += 1
                cx, cy = (r[0] + r[2]) // 2, (r[1] + r[3]) // 2
                inner = (cx - 4, cy - 4, cx + 4, cy + 4)
                self.monster_area(kid, kind, inner, 1, name=f"{kid}_{kind}_tinh_anh_{e}")
                total += 1
        return total

    # ---------------------------------------------------------------- 9. props
    def _place(self, name: str, tx: int, ty: int, solid: bool = True) -> None:
        pr = PROPS[name]
        if pr.kind == "tree":
            if solid:
                self.tree(tx, ty, pr.sprite)
            else:
                x, y = tx * T - 8, ty * T - 24
                self.obj("tree", "prop", x, y, 32, 40, sprite=pr.sprite, variant=self.rng.randrange(1000))
        else:
            self.thing(pr.name, pr.sprite, tx, ty, pr.w, pr.h, foot=pr.foot if solid else None,
                       variant=self.rng.randrange(1000))

    def _room(self, name: str, tx: int, ty: int) -> list[tuple] | None:
        big = PROPS[name].big
        foot = [(tx + dx, ty + dy) for dx in ((-1, 0, 1) if big else (0,)) for dy in ((-1, 0) if big else (0,))]
        for (x, y) in foot:
            if not self.inside(x, y, 2):
                return None
            j = self.i(x, y)
            if (x, y) in self.blocked_tiles or self.hard[j] or self.road[j] or self.keep[j]:
                return None
        return foot

    def dress_barriers(self) -> None:
        """The pictures on the walls: trees along a tree line, boulders along a cliff."""
        W = self.W
        for y in range(2, self.H - 2):
            for x in range(2, W - 2):
                j = y * W + x
                kind = self.barrier[j]
                if not kind or not self.hard[j]:
                    continue
                props = BARRIER_LOOK[kind][1]
                if not props or (x + 2 * y) % 2 or self.rng.random() > 0.9:
                    continue
                name = props[int(self.noise.value(x, y, 3.0, 31) * len(props)) % len(props)]
                if PROPS[name].big and (x // 2 + y) % 2:
                    name = props[-1]
                self._place(name, x, y, solid=False)
                self.blocked_tiles.add((x, y))

    def scatter(self) -> int:
        """Props over every walkable tile by the density map of its theme: sparse in the open, dense
        in the clumps; solid props keep a tile off the roads, nothing grows on a road or a keep."""
        W, H = self.W, self.H
        near_road = bytearray(W * H)
        for y in range(H):
            for x in range(W):
                if self.road[y * W + x]:
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if self.inside(x + dx, y + dy):
                                near_road[(y + dy) * W + x + dx] = 1
        order = [(x, y) for y in range(3, H - 3) for x in range(2, W - 2)]
        self.rng.shuffle(order)
        bk = self.bands_khu
        n = 0
        for (x, y) in order:
            j = y * W + x
            if self.hard[j] or self.road[j] or self.keep[j] or (x, y) in self.blocked_tiles:
                continue
            th = self.themes[bk[self.region[j]].theme]
            c = smooth(th.clump_cut - 0.12, th.clump_cut + 0.12, self.noise.fbm(x, y, th.clump, 2, 11))
            dens = th.open_density + (th.dense_density - th.open_density) * c
            if self.rng.random() >= dens:
                continue
            table = th.dense_props if self.rng.random() < c else th.open_props
            name = _pick(table, self.rng.random())
            solid = PROPS[name].foot is not None or PROPS[name].kind == "tree"
            if solid and (near_road[j] or self.soft[j]):
                continue
            room = self._room(name, x, y)
            if room is None:
                continue
            self._place(name, x, y)
            self.blocked_tiles.update(room)
            n += 1
        return n

    # ---------------------------------------------------------------- 10. finish
    def _solid_rects(self) -> list[tuple]:
        """The solid tiles as few rectangles: runs per row, merged down while they line up."""
        W, H = self.W, self.H
        out, open_ = [], {}
        for y in range(H + 1):
            runs = set()
            if y < H:
                x = 0
                while x < W:
                    if self.hard[y * W + x]:
                        s = x
                        while x < W and self.hard[y * W + x]:
                            x += 1
                        runs.add((s, x - 1))
                    else:
                        x += 1
            for run in list(open_):
                if run not in runs:
                    out.append((run[0], open_.pop(run), run[1], y - 1))
            for run in runs:
                open_.setdefault(run, y)
        return out

    def finish(self, extra_props: dict | None = None, ring: str = "tree", gaps=()) -> dict:
        """The ring of `ring` trees around the map (open at `gaps`, (side, tile) pairs), the
        collision of every solid tile, the khu and poi objects, the budget checks -> the map."""
        self.ring(ring, set(gaps))
        for (x0, y0, x1, y1) in self._solid_rects():
            self.solid_tile_rect(x0, y0, x1, y1)
        total = sum(a["count"] for k in self.khus for a in k.areas)
        cap = int(rules()["max_monsters_per_land"])
        if total > cap:
            raise ValueError(f"{self.zone}: {total} monsters, the budget is {cap}")
        for k in self.khus:
            x0, y0, x1, y1 = k.rect
            ax, ay = k.anchor
            self.obj(k.id, "khu", x0 * T, y0 * T, (x1 - x0 + 1) * T, (y1 - y0 + 1) * T,
                     khu=k.id, name_vi=k.name_vi, band=k.band, realm=k.realm, stage_min=k.stage_min,
                     stage_max=k.stage_max, anchor_x=ax * T + T // 2, anchor_y=ay * T + 12,
                     desc_vi=k.desc_vi, safe="true" if k.band == 0 else "false")
        for (kind, name_vi, tx, ty, w, h) in self.pois:
            self.obj(name_vi, "poi", tx * T, ty * T, w * T, h * T, poi=kind, name_vi=name_vi)
        props = {"music": "forest", "safe": "false", "dai_dia_do": "true"}
        props.update(extra_props or {})
        return self.build(props)

    def solid_tile_rect(self, x0: int, y0: int, x1: int, y1: int) -> None:
        self.solid(x0 * T, y0 * T, (x1 - x0 + 1) * T, (y1 - y0 + 1) * T)

    # ---------------------------------------------------------------- report
    def summary(self) -> list[str]:
        out = []
        for k in self.khus:
            kinds: dict[str, int] = {}
            for a in k.areas:
                kinds[a["monster"]] = kinds.get(a["monster"], 0) + a["count"]
            x0, y0, x1, y1 = k.rect
            out.append(f"{k.id} | {k.name_vi} | band {k.band} | {x1 - x0 + 1}x{y1 - y0 + 1} | "
                       + ", ".join(f"{m} {c}" for m, c in sorted(kinds.items())))
        return out
