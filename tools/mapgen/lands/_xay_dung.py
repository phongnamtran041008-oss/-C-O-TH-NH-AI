"""Helpers of three lands (Thiên Công Phường, Linh Xạ Nguyên, Lôi Kiếp Đài) on top of the Đại Địa
Đồ toolkit, kept here so tools/mapgen/giant.py does not change: street grids that break down with
depth, buildings and small things set into the blocks between streets, rows of things, hand-painted
lanes that count as roads, and a finish for a map that has no khu.

A module whose name starts with "_" is not a map (tools/mapgen/__init__.py skips it).
"""
from __future__ import annotations

from ..builder import T
from ..giant import PROPS, SOLID_WALL, DaiDiaDo, Khu, Prop

# props the city lands scatter (a key added once; the exemplar lands never name them)
PROPS.setdefault("x_anvil", Prop("thing", "anvil", "Đe rèn", 24, 20, (20, 8)))
PROPS.setdefault("x_board", Prop("thing", "board", "Bảng thợ", 24, 28, (20, 8)))
PROPS.setdefault("x_mat", Prop("thing", "mat", "Chiếu", 24, 16))


def khu_of(m: DaiDiaDo, kid: str) -> Khu:
    return next(k for k in m.khus if k.id == kid)


def region_index(m: DaiDiaDo, kid: str) -> int:
    return m.bands_khu.index(khu_of(m, kid))


def clear_box(m: DaiDiaDo, x0: int, y0: int, x1: int, y1: int, ri: int | None = None,
              road_ok: bool = False, keep_ok: bool = False) -> bool:
    """Every tile of the box free: inside the map, not solid, not blocked by a prop, not a road
    (unless `road_ok`), not kept (unless `keep_ok`), and in region `ri` when given."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inside(x, y, 3):
                return False
            j = m.i(x, y)
            if m.hard[j] or (x, y) in m.blocked_tiles:
                return False
            if (m.road[j] and not road_ok) or (m.keep[j] and not keep_ok):
                return False
            if ri is not None and m.region[j] != ri:
                return False
    return True


# ------------------------------------------------------------------ streets
def streets(m: DaiDiaDo, kid: str, pitch: int, keep_p: float, offset: tuple = (0, 0),
            min_run: int = 3) -> tuple[list, list]:
    """A grid of paved streets (2 tiles wide, the theme's road tiles) over khu `kid`, one every
    `pitch` tiles; each stretch between two crossings survives with chance `keep_p` (an old
    quarter keeps them all, a ruin loses most). Streets stay inside the khu's own ground, two
    tiles away from any wall, water or ink, so they never open a wall. Returns the street lines
    (xs, ys)."""
    k = khu_of(m, kid)
    ri = m.bands_khu.index(k)
    x0, y0, x1, y1 = k.rect
    xs = list(range(x0 + pitch // 2 + offset[0], x1 - 2, pitch))
    ys = list(range(y0 + pitch // 2 + offset[1], y1 - 2, pitch))

    def ok(x: int, y: int) -> bool:
        if not m.inside(x, y, 4) or m.region[m.i(x, y)] != ri:
            return False
        for dy in range(-2, 4):
            for dx in range(-2, 4):
                j = m.i(x + dx, y + dy)
                if m.hard[j] or (m.keep[j] and not m.road[j]):
                    return False
        return True

    def lay(seg: list) -> None:
        run: list = []
        for t in seg + [None]:
            if t is not None and ok(*t):
                run.append(t)
                continue
            if len(run) >= min_run:
                m.carve(run, "trail")
            run = []

    cuts_x = [x0] + xs + [x1]
    cuts_y = [y0] + ys + [y1]
    for y in ys:
        for a, b in zip(cuts_x, cuts_x[1:]):
            if m.rng.random() < keep_p:
                lay([(x, y) for x in range(a, b + 2)])
    for x in xs:
        for a, b in zip(cuts_y, cuts_y[1:]):
            if m.rng.random() < keep_p:
                lay([(x, y) for y in range(a, b + 2)])
    return xs, ys


def blocks(k: Khu, xs: list, ys: list, inset: int = 1) -> list[tuple]:
    """The blocks between the street lines of a khu (tile rects, inclusive), streets excluded."""
    x0, y0, x1, y1 = k.rect
    bx = [x0 - 2] + xs + [x1 + 1]
    by = [y0 - 2] + ys + [y1 + 1]
    out = []
    for a, b in zip(by, by[1:]):
        for c, d in zip(bx, bx[1:]):
            r = (c + 2 + inset, a + 2 + inset, d - 1 - inset, b - 1 - inset)
            if r[2] - r[0] >= 3 and r[3] - r[1] >= 3:
                out.append(r)
    return out


# ------------------------------------------------------------------ buildings and things
BUILDINGS = {    # sprite -> (w px, h px, foot px, tiles wide, tiles tall)
    "house": (48, 48, 20, 3, 3),
    "hut": (64, 56, 30, 4, 4),
    "stall": (40, 32, 12, 3, 2),
    "pavilion": (64, 64, 22, 4, 4),
}


def try_building(m: DaiDiaDo, name: str, sprite: str, tx: int, ty: int, ri: int | None = None,
                 **props) -> bool:
    """A building with its top-left tile at (tx, ty) when its tiles and a ring of one around
    them are free (never on a road)."""
    w, h, foot, tw, th = BUILDINGS[sprite]
    if not clear_box(m, tx - 1, ty - 1, tx + tw, ty + th, ri):
        return False
    m.building(name, sprite, tx, ty, w, h, foot, **props)
    return True


def try_thing(m: DaiDiaDo, prop: str, tx: int, ty: int, ri: int | None = None, name: str | None = None,
              solid: bool = True) -> bool:
    """A prop of PROPS on tile (tx, ty) when the tile is free (never on a road)."""
    pr = PROPS[prop]
    room = [(tx + dx, ty + dy) for dx in ((-1, 0, 1) if pr.big else (0,)) for dy in ((-1, 0) if pr.big else (0,))]
    for (x, y) in room:
        if not clear_box(m, x, y, x, y, ri):
            return False
    if pr.kind == "tree":
        m.tree(tx, ty, pr.sprite)
    else:
        m.thing(name or pr.name, pr.sprite, tx, ty, pr.w, pr.h, foot=pr.foot if solid else None,
                variant=m.rng.randrange(1000))
    m.blocked_tiles.update(room)
    return True


def fill_block(m: DaiDiaDo, r: tuple, ri: int, plan: list, tries: int = 6) -> None:
    """Furnish one block: `plan` is a list of (chance, kind, name) tried in turn; kind is a
    building sprite of BUILDINGS or a prop of PROPS; each lands at a random free spot of the block."""
    x0, y0, x1, y1 = r
    for chance, kind, name in plan:
        if m.rng.random() >= chance:
            continue
        for _ in range(tries):
            if kind in BUILDINGS:
                tw, th = BUILDINGS[kind][3], BUILDINGS[kind][4]
                if x1 - x0 + 1 < tw + 2 or y1 - y0 + 1 < th + 2:
                    break
                tx = m.rng.randint(x0 + 1, x1 - tw)
                ty = m.rng.randint(y0 + 1, y1 - th)
                if try_building(m, name, kind, tx, ty, ri, variant=m.rng.randrange(1000)):
                    break
            else:
                tx, ty = m.rng.randint(x0, x1), m.rng.randint(y0, y1)
                if try_thing(m, kind, tx, ty, ri, name):
                    break


def lane(m: DaiDiaDo, tiles, key: str = "wood0") -> None:
    """Hand-painted walkway tiles (a conveyor of planks, a stair): walkable, a road for the A* and
    for scatter (nothing grows on it)."""
    for (x, y) in tiles:
        if m.inside(x, y, 1):
            j = m.i(x, y)
            m.setg(x, y, key)
            m.hard[j] = 0
            m.barrier[j] = None
            m.road[j] = 1


def fence(m: DaiDiaDo, tiles, ground: str = "dirt0", sprite: str = "bamboo", every: int = 1) -> None:
    """A fence: solid tiles drawn as `ground` with a picket (`sprite`, walk-through picture; the
    tile itself is the collision) on every `every`-th tile."""
    m.wall(tiles, ground)
    for n, (x, y) in enumerate(sorted(tiles)):
        if n % every == 0:
            m.obj(sprite, "prop", x * T, y * T - 24, 16, 40, sprite=sprite, variant=(x * 31 + y * 7) % 1000)
        m.blocked_tiles.add((x, y))


def outline(x0: int, y0: int, x1: int, y1: int) -> set:
    return {(x, y) for x in range(x0, x1 + 1) for y in (y0, y1)} | \
        {(x, y) for y in range(y0, y1 + 1) for x in (x0, x1)}


def solid_ring(m: DaiDiaDo, tiles, key: str = "stone0") -> None:
    """Solid wall tiles of another ground (SOLID_WALL, no barrier: roads go around)."""
    for (x, y) in tiles:
        if m.inside(x, y):
            m.setg(x, y, key)
            m.hard[m.i(x, y)] = SOLID_WALL
            m.barrier[m.i(x, y)] = None


# ------------------------------------------------------------------ a map without khu
def finish_unbanded(m: DaiDiaDo, extra_props: dict | None = None, ring: str = "tree", gaps=()) -> dict:
    """finish() for a giant-toolkit map that must have no khu (Lôi Kiếp Đài, the boss arena: no
    bands, its monsters behave exactly as before): the ring, the collision of every solid tile,
    the poi objects; no khu object is written, the monster areas are the module's own objects."""
    m.ring(ring, set(gaps))
    for (x0, y0, x1, y1) in m._solid_rects():
        m.solid_tile_rect(x0, y0, x1, y1)
    for (kind, name_vi, tx, ty, w, h) in m.pois:
        m.obj(name_vi, "poi", tx * T, ty * T, w * T, h * T, poi=kind, name_vi=name_vi)
    props = {"music": "forest", "safe": "false"}
    props.update(extra_props or {})
    return m.build(props)
