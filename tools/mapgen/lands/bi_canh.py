"""Bí Cảnh: the rooms of the secret realms."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "bi_canh"

REALM_ROOM_W, REALM_ROOM_H = 22, 16
REALM_LAYOUT = (("compose", 0, 0), ("sentence", 1, 0), ("tone", 2, 0), ("mirror", 0, 1), ("maze", 1, 1), ("boss", 2, 1))


def secret_realm() -> dict:
    """Bí cảnh (spec 14): six walled rooms, one per puzzle kind plus the boss's den. A run
    uses 3-5 of the puzzle rooms in a random order; the server moves the party from room to
    room (they are not joined by corridors). Puzzle props are `realm_obj` objects whose
    `kind` the server and the client both understand; their state is sent at run time."""
    RW, RH = REALM_ROOM_W, REALM_ROOM_H
    m = MapBuilder("bi_canh", "Bí Cảnh", RW * 3, RH * 2, "realm")

    def ro(kind, x, y, w, h, room, **props):
        m.obj(f"{room}_{kind}{props.get('n', props.get('slot', props.get('tone', '')))}", "realm_obj", x, y, w, h,
              kind=kind, room=room, **props)

    for room, col, row in REALM_LAYOUT:
        x0, y0 = col * RW, row * RH
        for y in range(y0, y0 + RH):
            for x in range(x0, x0 + RW):
                edge = x in (x0, x0 + RW - 1) or y in (y0, y0 + RH - 1)
                m.setg(x, y, "realm_wall0" if edge else ("realm_floor0" if (x + y) % 3 else "realm_floor1"))
        m.solid(x0 * T, y0 * T, RW * T, T + 6)
        m.solid(x0 * T, (y0 + RH - 1) * T - 2, RW * T, T + 2)
        m.solid(x0 * T, y0 * T, T, RH * T)
        m.solid((x0 + RW - 1) * T, y0 * T, T, RH * T)
        m.obj(room, "realm_room", (x0 + 1) * T, (y0 + 1) * T, (RW - 2) * T, (RH - 2) * T, kind=room)
        cx, cy = x0 + 11, y0 + 7
        entry = ((x0 + 11) * T, (y0 + RH - 3) * T + 8)
        exit_tile = (x0 + 10, y0 + 1)
        if room == "compose":
            for slot, (tx, ty) in (("top", (cx, cy - 3)), ("bottom", (cx, cy + 3)), ("left", (cx - 4, cy)),
                                   ("right", (cx + 4, cy))):
                ro("pedestal", tx * T - 4, ty * T - 4, 24, 24, room, slot=slot)
        elif room == "sentence":
            for i in range(1, 9):
                tx = cx - 7 + 2 * (i - 1)
                ro("tile", tx * T - 2, cy * T - 2, 20, 20, room, n=i)
        elif room == "tone":
            for tone, (tx, ty) in ((1, (cx - 5, cy - 3)), (2, (cx + 5, cy - 3)), (3, (cx - 5, cy + 3)),
                                   (4, (cx + 5, cy + 3))):
                ro("pillar", tx * T, ty * T - 16, 16, 32, room, tone=tone)
                m.solid(tx * T + 2, ty * T + 6, 12, 10)
            ro("statue", cx * T - 4, (cy - 2) * T, 24, 32, room)
            m.solid(cx * T - 2, (cy - 2) * T + 22, 20, 10)
        elif room == "mirror":
            ro("mirror", (cx - 1) * T, (cy - 4) * T, 3 * T, 2 * T, room)
        elif room == "maze":
            # a perfect maze on the interior: cells on odd sub-tiles, walls between them
            gw, gh = RW - 3, RH - 3                      # 19 x 13 sub-grid
            open_ = {(i, j) for i in range(1, gw, 2) for j in range(1, gh, 2)}
            seen, stack = {(1, gh - 2)}, [(1, gh - 2)]
            while stack:
                ci, cj = stack[-1]
                nxt = [(ci + di, cj + dj, di, dj) for di, dj in ((2, 0), (-2, 0), (0, 2), (0, -2))
                       if (ci + di, cj + dj) in open_ and (ci + di, cj + dj) not in seen]
                if not nxt:
                    stack.pop()
                    continue
                ni, nj, di, dj = m.rng.choice(nxt)
                open_.add((ci + di // 2, cj + dj // 2))
                seen.add((ni, nj))
                stack.append((ni, nj))
            open_ |= {(1, gh - 1), (1, gh), (gw - 2, 0)}  # the way in (bottom left) and out (top right)
            for j in range(RH - 2):
                run = None
                for i in range(RW - 1):
                    wall = i < RW - 2 and (i, j) not in open_
                    tx, ty = x0 + 1 + i, y0 + 1 + j
                    if wall:
                        m.setg(tx, ty, "realm_wall0")
                        if run is None:
                            run = i
                    elif run is not None:
                        m.solid((x0 + 1 + run) * T, ty * T, (i - run) * T, T)
                        run = None
            entry = ((x0 + 2) * T + 8, (y0 + RH - 2) * T + 12)
            exit_tile = (x0 + 1 + gw - 2, y0 + 1)
            ro("maze_exit", exit_tile[0] * T - 4, exit_tile[1] * T, T + 8, T + 4, room)
        elif room == "boss":
            ro("boss_spawn", cx * T, (cy - 3) * T, 16, 16, room)
            ro("chest", cx * T - 4, (cy - 1) * T, 24, 18, room)
        ro("exit", exit_tile[0] * T, exit_tile[1] * T - 8, 2 * T if room != "maze" else T, T + 8, room)
        m.obj(f"{room}_entry", "spawn", *entry, 1, 1)
    m.obj("spawn", "spawn", 11 * T, (RH - 3) * T + 8, 1, 1)
    return m.build({"music": "forest", "safe": "false", "dark": "true"})


build = secret_realm
