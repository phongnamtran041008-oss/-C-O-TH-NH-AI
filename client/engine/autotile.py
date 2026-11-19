"""Soft edges for the 2x ground (v2 art): path, dirt and water cells get their transition tiles.

The terrain sheets hold, for each pair (`grass_path`, `grass_dirt`, `shore`), the 12 tiles
`_nw _n _ne _w _e _sw _s _se _in_nw _in_ne _in_sw _in_se`, placed on a cell of the INNER material
(path, dirt, water); the suffix says where the OUTER material (grass) lies, `in_` are notches.

Each cell is built from four quadrants, and each quadrant is decided by its own two orthogonal
neighbours and the diagonal between them (the rule RPG tile engines use):

    both orthogonal neighbours outer  -> that corner of the convex tile   (nw / ne / sw / se)
    only the vertical one outer       -> that quadrant of the edge tile   (n / s)
    only the horizontal one outer     -> that quadrant of the edge tile   (w / e)
    neither, but the diagonal outer   -> that quadrant of the notch tile  (in_nw ...)
    none                              -> the cell's own base tile

So any shape works with the 12 tiles: a single dirt cell becomes a round patch (four convex
corners), a one-tile path has both edges, a pond gets a shore all round. Which neighbours count
as outer comes from wiring.json `autotile`. Out-of-map neighbours never do. The map data and
the collision layer are not touched: this only decides how a cell looks, once, when the ground
surface is built.
"""
from __future__ import annotations

QUADS = ("nw", "ne", "sw", "se")
_DIR = {"nw": ((0, -1), (-1, 0), (-1, -1)), "ne": ((0, -1), (1, 0), (1, -1)),
        "sw": ((0, 1), (-1, 0), (-1, 1)), "se": ((0, 1), (1, 0), (1, 1))}


def piece(v_out: bool, h_out: bool, d_out: bool, quad: str) -> str | None:
    """The transition-tile suffix for one quadrant, or None for the plain base tile."""
    if v_out and h_out:
        return quad
    if v_out:
        return quad[0]                      # n or s
    if h_out:
        return quad[1]                      # w or e
    if d_out:
        return "in_" + quad
    return None


def cell_pieces(cls, x: int, y: int, w: int, h: int, outer: set) -> tuple:
    """The four quadrant suffixes (nw, ne, sw, se) of cell (x, y). `cls(x, y)` gives a cell's
    class name; neighbours whose class is in `outer` are the outer material."""
    def out(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < w and 0 <= ny < h and cls(nx, ny) in outer
    res = []
    for q in QUADS:
        (vx, vy), (hx, hy), (dx, dy) = _DIR[q]
        res.append(piece(out(vx, vy), out(hx, hy), out(dx, dy), q))
    return tuple(res)


def whole(cls, x: int, y: int, w: int, h: int, outer: set) -> str | None:
    """A whole-tile shape for cells the quadrants cannot draw as nicely, when the sheet has one:
    `island` (outer on all four sides), `h` / `v` (a one-tile strip running east-west /
    north-south), `cap_e` ... (the end of a strip: open toward the named side's opposite, closed
    on the named side). None for every other cell."""
    def out(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < w and 0 <= ny < h and cls(nx, ny) in outer
    n, e, s, w_ = out(0, -1), out(1, 0), out(0, 1), out(-1, 0)
    k = (n, e, s, w_)
    return {(True, True, True, True): "island",
            (True, False, True, False): "h", (False, True, False, True): "v",
            (True, True, True, False): "cap_e", (True, False, True, True): "cap_w",
            (True, True, False, True): "cap_n", (False, True, True, True): "cap_s"}.get(k)


def mask(cls, x: int, y: int, w: int, h: int, outer: set) -> int:
    """The 8-neighbour mask of cell (x, y): bit i set when neighbour i (N, NE, E, SE, S, SW, W, NW)
    is outer. Handy for tests and tools; the quadrant rule above only needs part of it."""
    order = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
    m = 0
    for i, (dx, dy) in enumerate(order):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and cls(nx, ny) in outer:
            m |= 1 << i
    return m


_MASKED: dict = {}


def is_outer_pixel(c) -> bool:
    """A grass pixel of a transition tile (the OUTER material is grass in every pair): green
    clearly above red and blue. Paths, dirt, sand, water and the dark edge lines are not."""
    return c.a > 0 and c.g > c.r + 12 and c.g > c.b + 12


def masked(tile):
    """The transition tile with its grass made transparent (cached), so the real neighbouring
    ground - light grass, dark grass, flowers - shows round the path, dirt or water instead of
    the one grass the sheet was painted with."""
    m = _MASKED.get(tile)
    if m is None:
        import pygame
        m = tile.convert_alpha() if pygame.display.get_surface() is not None else tile.copy()
        m = m.copy()
        w, h = m.get_size()
        for yy in range(h):
            for xx in range(w):
                c = m.get_at((xx, yy))
                if is_outer_pixel(c):
                    m.set_at((xx, yy), (c.r, c.g, c.b, 0))
        _MASKED[tile] = m
    return m


def compose(base, pieces: tuple, terrain: dict, pair: str, variant: int = 0, outer=None, whole_tile=None):
    """The tile for one cell. `base` is the cell's own tile (path, dirt, water); each quadrant
    with a piece takes that quadrant of the pair's transition tile. With `outer` (the tile of the
    neighbouring ground), the transition's own grass is replaced by that ground. `whole_tile`:
    one transition tile for the whole cell (island, strip, cap). Returns (surface, complete) -
    complete is False when a needed transition tile is missing (that quadrant keeps the base)."""
    import pygame
    if whole_tile is not None:
        if outer is None:
            return whole_tile, True
        out = outer.copy()
        out.blit(masked(whole_tile), (0, 0))
        return out, True
    if not any(pieces):
        return base, True
    size = base.get_width()
    half = size // 2
    out = outer.copy() if outer is not None else base.copy()
    complete = True
    for q, p in zip(QUADS, pieces):
        qx, qy = (0 if q[1] == "w" else half), (0 if q[0] == "n" else half)
        area = pygame.Rect(qx, qy, half, half)
        tiles = terrain.get(f"{pair}_{p}") if p is not None else None
        if p is not None and not tiles:
            complete = False
        if not tiles:
            out.blit(base, (qx, qy), area)
            continue
        t = tiles[variant % len(tiles)]
        out.blit(masked(t) if outer is not None else t, (qx, qy), area)
    return out, complete
