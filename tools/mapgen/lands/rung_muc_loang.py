"""Mê Đồ Lâm (zone rung_muc_loang)."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "rung_muc_loang"


def forest() -> dict:
    """Rừng Mực Loang: first zone with Mặc Quái (spec 7.1). West gate -> Trúc Lâm Thôn."""
    m = MapBuilder("rung_muc_loang", "Mê Đồ Lâm", 60, 40, "forest")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "dark_grass0" if r < 0.6 else "dark_grass1" if r < 0.96 else
                   ("ink0" if r > 0.985 else "ink1"))
    west_gap = set(range(18, 22))
    # a winding dirt trail
    y = 19
    for x in range(0, W - 6):
        if x % 6 == 0 and x > 4:
            ny = max(6, min(H - 9, y + m.rng.choice((-2, -1, 0, 1, 2))))
            m.fill(x, min(y, ny), x + 2, max(y, ny) + 2, "dirt0")
            y = ny
        m.fill(x, y, x, y + 2, "dirt0")
    for y in range(8, 30):  # side trail north-south
        m.fill(38, y, 39, y, "dirt0")
    # a clearing where the ink is thickest
    for yy in range(26, 33):
        for xx in range(42, 54):
            m.setg(xx, yy, "ink0" if m.rng.random() < 0.3 else "ink1" if m.rng.random() < 0.3 else "dark_grass0")
            m.blocked_tiles.add((xx, yy))
    m.ring("ink_tree", {("w", y) for y in west_gap})
    m.obj("Cổng Tây", "prop", 0, 18 * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", -8, 18 * T, T + 12, 4 * T, target="truc_lam_thon", target_spawn="from_forest")
    m.obj("Về Trúc Lâm Thôn", "sign", 3 * T, 15 * T, 16, 20, sprite="sign", text="← Trúc Lâm Thôn")
    m.solid(3 * T + 6, 15 * T + 14, 4, 6)
    m.reserve(0, 15 * T, 6 * T, 8 * T, pad=0)
    for i, (tx, ty) in enumerate(((14, 8), (30, 32), (52, 10), (24, 14))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # where the monsters roam (stage 3: they wander; Vấn Đạo combat comes in stage 4)
    m.obj("slimes_entrance", "monster_area", 12 * T, 14 * T, 14 * T, 12 * T, monster="ink_slime", count=6)
    m.obj("wisps_north", "monster_area", 30 * T, 4 * T, 18 * T, 10 * T, monster="tone_wisp", count=4)
    m.obj("clearing", "monster_area", 42 * T, 24 * T, 12 * T, 9 * T, monster="ink_slime", count=5)
    m.obj("clearing_wisps", "monster_area", 42 * T, 24 * T, 12 * T, 9 * T, monster="tone_wisp", count=2)
    m.obj("fox_den", "monster_area", 44 * T, 26 * T, 8 * T, 6 * T, monster="ink_fox", count=1)
    m.scatter_trees(45, "ink_tree")
    m.scatter_trees(15, "tree")
    m.obj("spawn", "spawn", 4 * T, 20 * T, 1, 1)
    m.obj("from_village", "spawn", 4 * T, 20 * T, 1, 1)
    maze_spots(m)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("hoa_yeu_nam", "monster_area", 128, 480, 256, 128, monster="hoa_yeu", count=3)
    m.obj("bach_vien_dong", "monster_area", 800, 208, 144, 160, monster="bach_vien", count=1)
    return m.build({"music": "forest", "safe": "false"})


def maze_spots(m: MapBuilder) -> None:
    """Mê Đồ Lâm (rung_muc_loang): the fork, the dead end, the hollow of the mother tree and
    the lowest hollow of the forest, plus the creatures of Thuật Toán và Tối Ưu."""
    dirt = GID["dirt0"]
    rows = [y for y in range(m.H) if m.ground[y * m.W + 37] == dirt]
    fy = rows[len(rows) // 2]
    m.clear(35, fy - 3, 41, fy + 2)
    m.sign("Ngã ba", "Ngã ba: mỗi lối là một cạnh của đồ thị", 40, fy - 2)
    m.clear(36, 5, 41, 9)                                    # the dead end at the top of the side trail
    m.clear(48, 2, 57, 12)                                   # the mother tree and the ring around its hollow
    m.tree(53, 5, "tree")
    for tx, ty in ((50, 5), (51, 3), (55, 3), (56, 5), (56, 8), (50, 8), (51, 10), (55, 10)):
        m.tree(tx, ty, "ink_tree")
    m.obj("moc_yeu_hoc_cay", "monster_area", 49 * T, 3 * T, 9 * T, 9 * T, monster="moc_yeu", count=1)
    m.obj("tri_chu_bac", "monster_area", 14 * T, 3 * T, 12 * T, 9 * T, monster="tri_chu_tinh", count=4)
    m.obj("tri_chu_nam", "monster_area", 26 * T, 24 * T, 10 * T, 10 * T, monster="tri_chu_tinh", count=3)


build = forest
