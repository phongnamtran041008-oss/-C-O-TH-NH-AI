"""Linh Xạ Nguyên."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "linh_xa_nguyen"


def archery_plain() -> dict:
    """Linh Xạ Nguyên (Thực Chiến): a bright grassland of shooting lanes, two rows of stone
    targets, a bow rack at the start and the far field where one's own Tâm Ma waits. West
    gate -> Trúc Lâm Thôn."""
    m = MapBuilder("linh_xa_nguyen", "Linh Xạ Nguyên", 64, 36, "linh_xa_nguyen")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.5 else "flowers0" if r < 0.62 else "flowers1" if r < 0.72
                   else "grass1" if r < 0.94 else "grass2")
    west_gap = set(range(16, 20))
    m.fill(0, 16, 8, 19, ["path0", "path1"])
    for ly in (8, 17, 26):                                   # three shooting lanes
        m.fill(6, ly, 56, ly + 1, "dirt0")
    m.fill(50, 11, 60, 24, ["dirt0", "dark_grass0"])        # the far field
    m.ring("peach", {("w", y) for y in west_gap})
    m.thing("Giá Cung", "board", 8, 12, 24, 28, foot=(20, 8))
    for row_x in (30, 44):                                   # the two rows of targets
        for ty in (6, 11, 15, 20, 24, 29):
            m.thing("Bia bắn", "tablet", row_x, ty, 16, 24, foot=(12, 8))
    for i, (tx, ty) in enumerate(((9, 5), (9, 29), (52, 11), (58, 11), (52, 24), (58, 24))):
        m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i)
    m.sign("Trường bắn", "Nhắm, bắn, xem lệch bao nhiêu rồi chỉnh lại: đó là huấn luyện", 11, 14)
    m.obj("tam_ma_bac", "monster_area", 12 * T, 3 * T, 16 * T, 11 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_nam", "monster_area", 12 * T, 21 * T, 16 * T, 11 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_giua", "monster_area", 33 * T, 4 * T, 9 * T, 27 * T, monster="tam_ma", count=3)
    m.obj("tam_ma_chap_niem", "monster_area", 51 * T, 12 * T, 9 * T, 12 * T, monster="tam_ma_chap_niem",
          count=1)
    rng = m.rng
    for i in range(40):                                     # tall grass and bushes, to walk through
        tx, ty = rng.randrange(3, W - 3), rng.randrange(3, H - 3)
        if (tx, ty) in m.blocked_tiles:
            continue
        m.thing("Cỏ", "tall_grass" if i % 3 else "bush", tx, ty, 24, 16, variant=i)
    m.scatter_trees(10, "peach")
    m.gate("w", 16, "truc_lam_thon", "from_linh_xa_nguyen", "Cổng Tây")
    m.sign("Về Trúc Lâm Thôn", "← Trúc Lâm Thôn", 3, 14)
    m.obj("spawn", "spawn", 4 * T, 18 * T, 1, 1)
    m.obj("from_village", "spawn", 4 * T, 18 * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("thao_nhan_bai_tap", "monster_area", 704, 400, 288, 128, monster="thao_nhan", count=3)
    m.obj("xich_diem_ma_dong_bac", "monster_area", 704, 32, 288, 128, monster="xich_diem_ma", count=1)
    return m.build({"music": "forest", "safe": "false"})


build = archery_plain
