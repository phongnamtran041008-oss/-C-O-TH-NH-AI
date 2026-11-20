"""Đạp Kiếm Lướt (world_plan.json, unlock dap_kiem_luot): the geometry of a glide on the sword.

Shared by the server, which decides, and the client, which predicts and picks where to land:
client/engine/glide.py is a copy of this file, line for line (client/tests check they agree).

A glide flies in a straight line from the feet to a landing point at most `max_px` away. On the
way it may pass over free ground and over the tiles the plan names (`over_tiles`: water and
ink, the chasms of the lands) even where those are solid; anything else that is solid - a wall
of stone, a tree, a house - stops it. It must land on free ground that is not such a tile.

`col` is a movement Collider (w, h, blocked, blocked_box); `tile_at(tx, ty)` names the ground of
a tile ('water', 'ink', 'grass'...) or None off the map; `over` is the set of names glided over.
"""
from __future__ import annotations

import math

TILE = 16
STEP = 2.0               # px between two points looked at along a glide
FOOT_W, FOOT_H = 10, 6   # the collision box above the feet (realtime/movement.py)


def _foot(x: float, y: float) -> tuple[int, int, int, int]:
    return int(x - FOOT_W / 2), int(y - FOOT_H), FOOT_W, FOOT_H


def over_ok(col, tile_at, over, x: float, y: float) -> bool:
    """May a glide pass over this point? Free ground, or every solid part under the feet lies on
    a tile it may glide over."""
    left, top, w, h = _foot(x, y)
    if left < 0 or top < 0 or left + w > col.w or top + h > col.h:
        return False
    if not col.blocked_box(left, top, w, h):
        return True
    for ty in range(top // TILE, (top + h - 1) // TILE + 1):
        for tx in range(left // TILE, (left + w - 1) // TILE + 1):
            if tile_at(tx, ty) in over:
                continue
            x0, y0 = max(left, tx * TILE), max(top, ty * TILE)
            x1, y1 = min(left + w, (tx + 1) * TILE), min(top + h, (ty + 1) * TILE)
            if x1 > x0 and y1 > y0 and col.blocked_box(x0, y0, x1 - x0, y1 - y0):
                return False
    return True


def land_ok(col, tile_at, over, x: float, y: float) -> bool:
    """May a glide end here? Free ground, not over water or a chasm."""
    if col.blocked(x, y):
        return False
    return tile_at(int(x // TILE), int((y - 1) // TILE)) not in over


def check(col, tile_at, over, x0: float, y0: float, x1: float, y1: float, max_px: float,
          min_px: float = 0.0) -> str | None:
    """Why this glide may not happen (a refusal code), or None. too_far: past max_px;
    too_short: under min_px; bad_landing: it would end on a tile that is not walkable; blocked:
    something solid that is no water or chasm stands in the way."""
    d = math.hypot(x1 - x0, y1 - y0)
    if d > max_px + 0.5:
        return "too_far"
    if d < min_px:
        return "too_short"
    if not land_ok(col, tile_at, over, x1, y1):
        return "bad_landing"
    n = max(1, int(math.ceil(d / STEP)))
    for i in range(1, n):
        k = i / n
        if not over_ok(col, tile_at, over, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k):
            return "blocked"
    return None


def pick(col, tile_at, over, x: float, y: float, dx: int, dy: int, max_px: float,
         min_px: float = 0.0) -> tuple[float, float] | None:
    """Where a glide from (x, y) the way (dx, dy) points lands: past a gap, on the first free
    ground after it; with no gap on the way, as far as it goes over free ground. None when it
    cannot land (the far side is out of reach, or there is nothing to glide over or to)."""
    if not (dx or dy):
        return None
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm
    best, crossed = None, False
    s = STEP
    while s <= max_px + 1e-9:
        px, py = round(x + ux * s, 2), round(y + uy * s, 2)
        if not over_ok(col, tile_at, over, px, py):
            break
        if land_ok(col, tile_at, over, px, py):
            if crossed:
                return (px, py) if check(col, tile_at, over, x, y, px, py, max_px, min_px) is None else None
            best = (px, py)
        else:
            crossed = True
        s += STEP
    if crossed or best is None:
        return None
    return best if check(col, tile_at, over, x, y, best[0], best[1], max_px, min_px) is None else None
