"""Trúc Lâm Thôn: the safe hub, one gate to each land."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "truc_lam_thon"


def village() -> dict:
    """Trúc Lâm Thôn: the safe hub (spec 7.1). Gate south -> abode, east -> Rừng Mực Loang."""
    m = MapBuilder("truc_lam_thon", "Trúc Lâm Thôn", 56, 36, "village")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.6 else "grass1" if r < 0.85 else
                   ("flowers0" if r > 0.98 else "flowers1" if r > 0.96 else "grass2"))
    south_gap = set(range(26, 30))
    east_gap = set(range(16, 20))
    west_gap = set(range(16, 20))
    north_gap = set(range(16, 20))        # M7: north to Loạn Số Cốc
    # roads and the square
    m.fill(26, 24, 29, H - 1, ["path0", "path1", "path0"])            # south road to the abode
    m.fill(36, 16, W - 1, 19, ["path0", "path1", "path0"])            # east road to the forest
    m.fill(26, 8, 29, 11, ["path0", "path1"])                         # north to Thiên Cơ Các
    m.fill(10, 16, 19, 19, ["path0", "path1"])                        # west to the market
    m.fill(16, 0, 19, 15, ["path0", "path1"])                         # M7: north to Loạn Số Cốc
    m.fill(0, 16, 9, 19, ["path0", "path1", "path0"])                 # stage 6: west road to Hồ Nghiên Mực
    m.fill(20, 12, 35, 23, ["plaza0", "plaza1"])                      # the square
    m.fill(30, 24, 31, 27, ["path0", "path1"])
    m.fill(32, 27, 45, 28, ["path0", "path1"])                        # to the Thủ Thành gate
    m.fill(8, 9, 11, 15, ["path0", "path1"])                          # to Trúc Lão's house
    m.fill(36, 10, 39, 15, ["path0", "path1"])                        # to the library
    # pond in the south-west corner
    for y in range(26, 31):
        for x in range(4, 11):
            m.setg(x, y, "water0")
    m.solid(4 * T, 26 * T, 7 * T, 5 * T)
    m.reserve(4 * T, 26 * T, 7 * T, 5 * T)
    # Thiên Địa Đồ (2026-11-20): four more gates, one per new land of Luyện Khí (roads after the scatter)
    land_gaps = ({("n", x) for x in range(45, 49)} | {("n", x) for x in range(2, 6)}
                 | {("w", y) for y in range(9, 13)} | {("e", y) for y in range(26, 30)})
    m.ring("bamboo", {("s", x) for x in south_gap} | {("e", y) for y in east_gap}
           | {("w", y) for y in west_gap} | {("n", x) for x in north_gap} | land_gaps)
    # buildings and service points (actions are handled by the client; spec 7.1)
    m.building("Thiên Cơ Các", "pavilion", 25, 3, 64, 64, 22, otype="interact", action="gacha")
    m.building("Tàng Thư Các", "library", 36, 4, 64, 56, 24, otype="interact", action="library")
    m.building("Nhà Trúc Lão", "hut", 6, 4, 64, 56, 30)
    m.npc("Trúc Lão", "truc_lao", 10, 8, action="talk_master")
    m.building("Sạp Tạp Hóa", "stall", 11, 13, 40, 32, 12, otype="interact", action="shop", variant=0)
    m.npc("Bà Chủ Sạp", "shopkeeper", 13, 11, action="shop")
    m.building("Sạp Vải", "stall", 11, 20, 40, 32, 12, otype="interact", action="cloth", variant=1)
    m.building("Lò Luyện Đan", "furnace", 16, 25, 24, 28, 14, otype="interact", action="alchemy")
    m.npc("Đan Sư", "alchemist", 14, 25, action="alchemy")
    m.building("Lò Rèn", "anvil", 21, 27, 24, 20, 10, otype="interact", action="forge")
    m.npc("Thợ Rèn", "smith", 23, 26, action="forge")
    m.building("Bảng Nhiệm Vụ", "board", 32, 10, 24, 28, 8, otype="interact", action="quests")
    m.building("Cổng Thủ Thành", "td_gate", 44, 24, 40, 40, 6, otype="interact", action="td")
    m.obj("Giếng", "prop", 27 * T + 4, 16 * T, 24, 24, sprite="well")
    m.solid(27 * T + 6, 16 * T + 12, 20, 12)
    m.npc("Tiểu Lan", "guide", 30, 29, action="talk_guide")
    m.npc("Thủ Thư", "librarian", 41, 9, action="library")
    for i, (tx, ty) in enumerate(((20, 12), (35, 12), (20, 23), (35, 23), (25, 24), (30, 24))):
        m.obj("lantern", "prop", tx * T + 4, ty * T - 16, 8, 24, sprite="lantern", variant=i)
        m.solid(tx * T + 6, ty * T + 4, 4, 4)
    for i, (tx, ty) in enumerate(((44, 6), (49, 10), (42, 31), (49, 31), (3, 19), (36, 30))):
        m.building("Nhà dân", "house", tx, ty, 48, 48, 20, variant=i)
    m.obj("sign", "prop", 33 * T, 18 * T - 4, 16, 20, sprite="sign")
    m.obj("Đi Mê Đồ Lâm", "sign", 52 * T, 14 * T, 16, 20, sprite="sign",
          text="Mê Đồ Lâm →")
    m.solid(52 * T + 6, 14 * T + 14, 4, 6)
    m.scatter_trees(26)
    # zone exits (server checks the player stands inside before moving them)
    m.obj("to_abode", "portal", 26 * T, (H - 1) * T - 2, 4 * T, T + 10, target="abode", target_spawn="spawn")
    m.obj("Cổng Đông", "prop", (W - 2) * T, 16 * T - 8, 32, 40, sprite="portal")
    m.obj("to_forest", "portal", (W - 1) * T - 4, 16 * T, T + 12, 4 * T, target="rung_muc_loang",
          target_spawn="from_village")
    m.obj("spawn", "spawn", 28 * T, 21 * T, 1, 1)
    m.obj("from_abode", "spawn", 28 * T, (H - 3) * T, 1, 1)
    m.obj("from_forest", "spawn", (W - 4) * T, 18 * T, 1, 1)
    # M7: the gate north to Loạn Số Cốc, where the mistakes themselves walk around
    m.obj("Cổng Bắc", "prop", 16 * T, 0, 32, 40, sprite="portal")
    m.obj("to_loan_so_coc", "portal", 16 * T, -8, 4 * T, T + 10, target="loan_so_coc",
          target_spawn="from_village")
    m.obj("Đi Kiếm Trủng Sơn", "sign", 20 * T, 3 * T, 16, 20, sprite="sign",
          text="↑ Kiếm Trủng Sơn")
    m.solid(20 * T + 6, 3 * T + 14, 4, 6)
    m.obj("from_loan_so_coc", "spawn", 17 * T, 3 * T, 1, 1)
    # stage 6: the pond can be fished (spec 11.1), the west gate leads to Hồ Nghiên Mực
    m.obj("pond", "area", 4 * T, 26 * T, 7 * T, 5 * T, kind="pond", pool="ao")
    m.obj("Cổng Tây", "prop", 0, 16 * T - 8, 32, 40, sprite="portal")
    m.obj("to_lake", "portal", -8, 16 * T, T + 12, 4 * T, target="ho_nghien_muc", target_spawn="from_village")
    m.obj("Đi Vạn Tượng Trạch", "sign", 3 * T, 14 * T, 16, 20, sprite="sign", text="← Vạn Tượng Trạch")
    m.solid(3 * T + 6, 14 * T + 14, 4, 6)
    m.obj("from_lake", "spawn", 3 * T, 18 * T, 1, 1)
    # stage 9: Cổng Bí Cảnh on the square (secret realms, spec 14)
    m.building("Cổng Bí Cảnh", "realm_gate", 21, 12, 40, 40, 6, otype="interact", action="realm")
    m.obj("from_realm", "spawn", 22 * T + 4, 16 * T + 4, 1, 1)
    village_lands(m)
    return m.build({"music": "village", "safe": "true"})


def village_lands(m: MapBuilder) -> None:
    """Thiên Địa Đồ (2026-11-20): the gates of the four new lands of Luyện Khí. Laid after the
    scatter, so every tree of the village keeps its place except the few on the new roads."""
    W = m.W
    # north-east: Lưu Vân Cốc
    m.clear(44, 0, 49, 15)
    m.fill(45, 0, 48, 4, ["path0", "path1"], reserve=False)
    m.fill(47, 5, 48, 15, ["path0", "path1"], reserve=False)
    m.gate("n", 45, "luu_van_coc", "from_village", "Cổng Mây")
    m.sign("Đi Lưu Vân Cốc", "↑ Lưu Vân Cốc", 44, 3)
    m.obj("from_luu_van_coc", "spawn", 47 * T, 3 * T, 1, 1)
    # north-west: Lôi Kiếp Đài, the trial at the end of the realm
    m.clear(0, 0, 6, 12)
    m.fill(2, 0, 5, 3, ["path0", "path1"], reserve=False)
    m.fill(2, 4, 4, 8, ["path0", "path1"], reserve=False)
    m.gate("n", 2, "loi_kiep_dai", "from_village", "Cổng Lôi")
    m.sign("Đi Lôi Kiếp Đài", "↑ Lôi Kiếp Đài", 6, 2)
    m.obj("from_loi_kiep_dai", "spawn", 3 * T + 8, 3 * T, 1, 1)
    # west, above the lake road: Thiên Công Phường
    m.fill(0, 9, 8, 11, ["path0", "path1", "path0"], reserve=False)
    m.gate("w", 9, "thien_cong_phuong", "from_village", "Cổng Thợ")
    m.sign("Đi Thiên Công Phường", "← Thiên Công Phường", 5, 12)
    m.obj("from_thien_cong_phuong", "spawn", 3 * T, 10 * T + 8, 1, 1)
    # east, past the Thủ Thành gate: Linh Xạ Nguyên
    m.clear(46, 25, W - 1, 30)
    m.fill(46, 27, W - 1, 28, ["path0", "path1"], reserve=False)
    m.gate("e", 26, "linh_xa_nguyen", "from_village", "Cổng Xạ")
    m.sign("Đi Linh Xạ Nguyên", "Linh Xạ Nguyên →", 52, 25)
    m.obj("from_linh_xa_nguyen", "spawn", (W - 4) * T, 28 * T, 1, 1)


build = village
