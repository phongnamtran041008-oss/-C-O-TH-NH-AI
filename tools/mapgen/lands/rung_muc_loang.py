"""Mê Đồ Lâm (zone rung_muc_loang, land me_do_lam, branch Thuật Toán và Tối Ưu): the forest maze,
a giant land of Đại Địa Đồ (320 x 240 tiles).

The forest is a graph you walk. Its glades are the vertices, walled from each other by tree
lines; the trails that cut through the walls are the edges, and the signposts at the junctions
work like a routing table: each way out names the nearest place whose shortest way starts there,
or says "ngõ cụt" when the branch leads nowhere else. The three tiers of tu vi lie from the west
gate to the east: Ngoại Vi (tầng 1-3) behind the gate, a line of ink trees, Trung Vực (tầng
4-6), the ink ravine Khe Mực crossed by three bridges of stone, Thâm Xứ (tầng 7-9). Each khu
shows one shape of graph:

* Bìa Rừng Đa Lối - glades with a few loops, the first junction of the forest just inside the
  gate (the old Mực Con, Lân Hỏa Yêu and Mặc Hồ of the quests live here, near the first camp);
* Rừng Rẽ Nhánh - a tree: one root, branches, no loop; every leaf a dead end (Linh Hồ);
* Lũng Tơ Nhện - spiders' glades, a tree with two loops;
* Cổ Lâm Vòng Lặp - a ring of glades round the old banyan (a cycle with two spokes);
* Trung Lâm Ngã Bảy - one glade where seven trails meet, two shortcuts that skip a glade;
* Ngõ Cụt Sương Mù - a tree of long branches, the deepest dead end holds a spear;
* Hốc Cây Mẹ - the mother tree, whose hollow holds the best spear of the forest;
* Mê Cung Ngàn Lá - a true maze of hedges (a spanning tree of its cells, a few walls taken out
  so it has loops), its heart the anchor; Chỉ Đường finds the way through;
* Thung Cực Tiểu - the valley every slope runs down into: its bottom is the minimum.
"""
from __future__ import annotations

import math
import random

from ..builder import T
from ..giant import SOLID_WALL, Theme
from ._do_thi import Builder, Cells, glade_walls, overlaps, route_signs, spread

ZONE = "rung_muc_loang"
SIZE = (320, 240)
SEED = "me_do_lam_dai_dia_do"

GATE_Y = 118                  # the west gate: tiles 118..121 of the west edge
SPAWN = (4, 120)
NGA_BA = (30, 119)            # the first junction of the forest (thuong_1 ha stands by it)
THUONG_HA = (29, 116)
CAMP1 = (56, 119)
CAMP2 = (137, 119)
CAMP3 = (234, 119)
HANG_HO = (24, 149)           # Hang Mặc Hồ, a dead end near the first camp
LINH_HO_LEAF = (14, 12)       # the deepest leaf of Rừng Rẽ Nhánh, where Linh Hồ shows
LINH_HO = (14, 12)
NGA_BAY = (166, 119)          # the junction of seven trails
DA_CO_THU = (162, 40)         # the old banyan in the middle of the ring
NGO_CUT_SAU = (202, 229)      # the deepest dead end (thuong_1 trung)
THUONG_TRUNG = (202, 229)
CAY_ME = (276, 30)            # the mother tree; thuong_1 thuong lies in its hollow
THUONG_THUONG = (276, 32)
DAY_THUNG = (262, 206)        # the bottom of Thung Cực Tiểu (thuong_2 ha)
THUONG_2 = (262, 206)
CUU_VI = (304, 226)           # the old tree of the south-east corner (Cửu Vĩ Hồ)
CUU_VI_HO = (304, 228)

# the maze: cells of 5 tiles (a corridor of 3, a hedge of 2), its heart 4 x 4 cells
MX, MY, MC, MNX, MNY = 244, 84, 5, 14, 14
HEART = (5, 5, 8, 8)
MAZE_W_ROW = 7                # the west door (towards Am Khe Mực)
MAZE_N_COL = 3
MAZE_S_COL = 10


# ------------------------------------------------------------------ themes
def g_light(P, D, r):
    if P < 0.26:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    if P > 0.74 and D > 0.55:
        return "flowers0" if r < 0.5 else "flowers1"
    return "grass0" if r < 0.5 else "grass1" if r < 0.85 else "grass2"


def g_flowers(P, D, r):
    if P > 0.56 and D > 0.42:
        return "flowers1" if r < 0.5 else "flowers0"
    if P < 0.22:
        return "dark_grass0"
    return "grass0" if r < 0.5 else "grass1" if r < 0.85 else "grass2"


def g_old(P, D, r):
    if P < 0.24:
        return "dark_grass0" if r < 0.65 else "dark_grass1"
    if P > 0.72 and D > 0.5:
        return "dirt0"
    return "grass2" if r < 0.45 else "grass1"


def g_mist(P, D, r):
    if P > 0.66:
        return "stone0"
    if P < 0.3:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    return "grass1" if r < 0.6 else "grass2"


def g_ink_wood(P, D, r):
    if P > 0.7 and D > 0.45:
        return "dirt0"
    if P < 0.26:
        return "dark_grass0" if r < 0.55 else "dark_grass1"
    return "grass2" if r < 0.6 else "grass1"


def g_spider(P, D, r):
    if P < 0.24:
        return "dark_grass0" if r < 0.6 else "dark_grass1"
    if P > 0.66:
        return "dirt0"
    return "grass2" if r < 0.7 else "grass1"


def g_valley(P, D, r):
    if P > 0.7:
        return "stone0"
    if P < 0.3:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    return "dirt0" if D > 0.5 else "grass2"


def themes(m) -> None:
    m.themes["rung_mo"] = Theme("rung_mo", g_light, [("tree", 3), ("bush", 3), ("tall_grass", 3), ("stump", 1), ("rock", 1)],
                                [("tree", 6), ("pine", 2), ("bush", 1)], 0.035, 0.14, 15.0, 0.57)
    m.themes["rung_hoa"] = Theme("rung_hoa", g_flowers, [("peach", 2), ("bush", 2), ("tall_grass", 3), ("tree", 1)],
                                 [("peach", 4), ("tree", 3), ("bush", 1)], 0.035, 0.14, 15.0, 0.57)
    m.themes["co_lam"] = Theme("co_lam", g_old, [("tree", 3), ("stump", 2), ("log", 1), ("bush", 2), ("tall_grass", 2)],
                               [("tree", 7), ("pine", 2)], 0.035, 0.15, 16.0, 0.56)
    m.themes["rung_suong"] = Theme("rung_suong", g_mist, [("pine", 3), ("cloud", 2), ("bush", 1), ("tall_grass", 2), ("stump", 1)],
                                   [("pine", 6), ("cloud", 1), ("tree", 1)], 0.035, 0.14, 15.0, 0.57)
    m.themes["muc_lam"] = Theme("muc_lam", g_ink_wood, [("dead_tree", 3), ("rock", 2), ("stump", 2), ("crystal", 1)],
                                [("dead_tree", 6), ("tree", 1)], 0.035, 0.14, 15.0, 0.57)
    m.themes["me_cung"] = Theme("me_cung", g_old, [("bush", 2), ("tall_grass", 2), ("stump", 1)],
                                [("tree", 4), ("bush", 2)], 0.03, 0.12, 15.0, 0.58)
    m.themes["to_nhen"] = Theme("to_nhen", g_spider, [("dead_tree", 3), ("stump", 2), ("rock", 2), ("log", 1), ("bush", 1)],
                                [("dead_tree", 6), ("tree", 1), ("rock", 1)], 0.035, 0.15, 16.0, 0.56)
    m.themes["thung"] = Theme("thung", g_valley, [("rock", 3), ("tall_grass", 2), ("dead_tree", 1), ("bush", 1)],
                              [("dead_tree", 3), ("boulder", 2), ("pine", 2)], 0.035, 0.14, 15.0, 0.57)


# ------------------------------------------------------------------ build
def build() -> dict:
    W, H = SIZE
    m = Builder(ZONE, "Mê Đồ Lâm", W, H, SEED)
    rng = random.Random(SEED + ":do_thi")
    themes(m)

    # ---- 1. the khu (band 1 by the west gate, band 3 beyond Khe Mực in the east)
    K = {}
    K["re"] = m.khu("mdl_re_nhanh", "Rừng Rẽ Nhánh", 1, (0, 0, 109, 79), "rung_hoa", (0, 0),
                    "Lối rừng tỏa ra như cành cây: không vòng nào, mỗi nhánh tận cùng là một ngõ cụt. Hoa Yêu nở dọc lối.")
    K["bia"] = m.khu("mdl_bia_rung", "Bìa Rừng Đa Lối", 1, (0, 80, 109, 159), "rung_mo", NGA_BA,
                     "Bìa rừng ngay trong cổng tây: các khoảng trống nối nhau bằng nhiều lối, có lối vòng. Mực Con và Lân Hỏa Yêu quanh ngã ba đầu tiên.")
    K["nhen"] = m.khu("mdl_to_nhen", "Lũng Tơ Nhện", 1, (0, 160, 109, 239), "to_nhen", (0, 0),
                      "Lũng rừng tối chằng chịt tơ: Tri Chu Tinh giăng lưới giữa những cây chết.")
    K["vong"] = m.khu("mdl_vong_lap", "Cổ Lâm Vòng Lặp", 2, (110, 0, 214, 79), "co_lam", DA_CO_THU,
                      "Rừng cổ: các khoảng trống xếp thành một vòng quanh cây đa cổ thụ, đi mãi lại về chỗ cũ.")
    K["bay"] = m.khu("mdl_nga_bay", "Trung Lâm Ngã Bảy", 2, (110, 80, 214, 159), "rung_mo", NGA_BAY,
                     "Giữa rừng: bảy lối gặp nhau ở một khoảng trống, và hai lối tắt bỏ qua một chặng.")
    K["cut"] = m.khu("mdl_ngo_cut", "Ngõ Cụt Sương Mù", 2, (110, 160, 214, 239), "rung_suong", (0, 0),
                     "Rừng thông chìm sương, lối nào cũng rẽ nhánh rồi tắc: ngõ cụt sâu nhất giữ một cây thương.")
    K["me"] = m.khu("mdl_cay_me", "Hốc Cây Mẹ", 3, (215, 0, 319, 71), "muc_lam", CAY_ME,
                    "Rừng mực bên kia Khe Mực, quanh cây mẹ của cả khu rừng; Mộc Yêu canh hốc cây.")
    K["mc"] = m.khu("mdl_me_cung", "Mê Cung Ngàn Lá", 3, (215, 72, 319, 167), "me_cung", (280, 120),
                    "Mê cung tường lá thật sự: lối rẽ, ngõ cụt và vài vòng lặp. Chỉ Đường vẫn tìm được lối vào tâm.")
    K["thung"] = m.khu("mdl_cuc_tieu", "Thung Cực Tiểu", 3, (215, 168, 319, 239), "thung", DAY_THUNG,
                       "Thung lũng mọi sườn dốc đều đổ về một đáy: điểm cực tiểu của rừng.")
    ri = {key: m.bands_khu.index(k) for key, k in K.items()}

    # ---- 2. the ground, the camps
    m.paint(warp=7.0, scale=26.0)
    m.camp("mdl_leu_bia_rung", "Lều Bìa Rừng", CAMP1, r=6,
           desc_vi="Lều nghỉ sau ngã ba đầu tiên, ngay trong cổng tây. Không có quái.",
           label_vi="Lều Bìa Rừng (nghỉ chân)")
    m.camp("mdl_tram_nga_bay", "Trạm Ngã Bảy", CAMP2, r=6,
           desc_vi="Trạm nghỉ sau hàng cây mực, cửa vào Trung Vực.", label_vi="Trạm Ngã Bảy · cửa Trung Vực")
    m.camp("mdl_am_khe_muc", "Am Khe Mực", CAMP3, r=6,
           desc_vi="Am nhỏ bên kia Khe Mực, trước cửa mê cung: cửa vào Thâm Xứ.",
           label_vi="Am Khe Mực · cửa Thâm Xứ")
    m.clear_zones.append((0, GATE_Y - 2, 6, GATE_Y + 5))       # the gate and the spawn

    # ---- 3. the large features: the valley, the landmarks' ground
    valley(m)
    disc(m, DA_CO_THU, 6.5, "flowers0", "dirt0")
    disc(m, NGA_BAY, 5.5, "dirt0", "stone0")
    disc(m, CAY_ME, 6.5, "dirt0", "dark_grass1")
    disc(m, (52, 200), 6.5, "dirt0", "stone0")
    disc(m, HANG_HO, 4.5, "dirt0", "stone0")
    disc(m, NGO_CUT_SAU, 3.5, "stone0", "dirt0")
    disc(m, CUU_VI, 4.5, "flowers1", "dirt0")
    lm = landmark_rects()
    no_walls(m, lm)

    # ---- 4. the walls between the khu
    m.barriers({
        ("mdl_re_nhanh", "mdl_bia_rung"): "trees", ("mdl_bia_rung", "mdl_to_nhen"): "trees",
        ("mdl_re_nhanh", "mdl_vong_lap"): "dead_trees", ("mdl_bia_rung", "mdl_nga_bay"): "dead_trees",
        ("mdl_to_nhen", "mdl_ngo_cut"): "dead_trees", ("mdl_re_nhanh", "mdl_nga_bay"): "dead_trees",
        ("mdl_bia_rung", "mdl_vong_lap"): "dead_trees", ("mdl_bia_rung", "mdl_ngo_cut"): "dead_trees",
        ("mdl_to_nhen", "mdl_nga_bay"): "dead_trees",
        ("mdl_vong_lap", "mdl_nga_bay"): "trees", ("mdl_nga_bay", "mdl_ngo_cut"): "trees",
        ("mdl_vong_lap", "mdl_cay_me"): "chasm", ("mdl_nga_bay", "mdl_me_cung"): "chasm",
        ("mdl_ngo_cut", "mdl_cuc_tieu"): "chasm", ("mdl_vong_lap", "mdl_me_cung"): "chasm",
        ("mdl_nga_bay", "mdl_cay_me"): "chasm", ("mdl_nga_bay", "mdl_cuc_tieu"): "chasm",
        ("mdl_ngo_cut", "mdl_me_cung"): "chasm",
        ("mdl_cay_me", "mdl_me_cung"): "dead_trees", ("mdl_me_cung", "mdl_cuc_tieu"): "dead_trees",
    })

    # ---- the glades (vertices) and the walls between them
    seeds, fixed = glade_seeds(m, rng)
    cells = Cells(m, seeds, warp=5.0)
    wall_kind = {ri["re"]: "trees", ri["bia"]: "trees", ri["nhen"]: "dead_trees", ri["vong"]: "trees",
                 ri["bay"]: "trees", ri["cut"]: "pines", ri["me"]: "dead_trees", ri["thung"]: "pines"}
    glade_walls(m, cells, lambda r: wall_kind.get(r, "trees"))
    maze(m, rng)
    release(m, lm)

    # ---- 5. the roads: the edges of the graph
    for sid in cells.ids:
        if sid not in m.nodes:
            m.node(sid, cells.tile[sid], "", sign=False)
    m.node("gate", (3, GATE_Y + 1), "Cổng Tây · về Trúc Lâm Thôn", sign=False)
    mx0, my0 = MX, MY
    m.node("n_cua_me_cung", (mx0 - 3, MY + MC * MAZE_W_ROW + 3), "Cửa Mê Cung", sign=False)
    m.node("n_cua_bac", (MX + MC * MAZE_N_COL + 3, my0 - 4), "Cửa Bắc Mê Cung", sign=False)
    m.node("n_cua_nam", (MX + MC * MAZE_S_COL + 3, MY + MC * MNY + 5), "Cửa Nam Mê Cung", sign=False)
    edges = graph_edges(m, cells, rng, ri)
    spine = spine_edges(edges, {k: v["tile"] for k, v in m.nodes.items()}, ["gate", "mdl_leu_bia_rung", "mdl_tram_nga_bay", "mdl_am_khe_muc"])
    order = [e for e in edges if frozenset(e[:2]) in spine] + [e for e in edges if frozenset(e[:2]) not in spine]
    m.network([(a, b, "main" if frozenset((a, b)) in spine else "trail", chasm)
               for (a, b, chasm) in order])
    m.carve([(x, GATE_Y + 1) for x in range(0, 4)], "main")      # through the gate

    # the anchors of the khu whose hub glade is computed
    K["re"].anchor = cells.tile[fixed["re_root"]]
    K["nhen"].anchor = cells.tile[fixed["nhen_hub"]]
    K["cut"].anchor = cells.tile[fixed["cut_hub"]]

    # ---- 6. the places, 7. the signposts
    places(m, cells, fixed)
    named = {
        "gate": "Cổng Tây · về Trúc Lâm Thôn",
        "n_nga_ba": "Ngã Ba Đầu Tiên",
        "mdl_leu_bia_rung": "Lều Bìa Rừng",
        "mdl_tram_nga_bay": "Trạm Ngã Bảy · Trung Vực",
        "mdl_am_khe_muc": "Am Khe Mực · Thâm Xứ",
        fixed["re_root"]: "Rừng Rẽ Nhánh",
        fixed["nhen_hub"]: "Lũng Tơ Nhện",
        "n_da_co_thu": "Cổ Lâm Vòng Lặp",
        "n_nga_bay": "Ngã Bảy",
        fixed["cut_hub"]: "Ngõ Cụt Sương Mù",
        "n_hang_ho": "Hang Mặc Hồ",
        "n_cay_me": "Hốc Cây Mẹ",
        "n_cua_me_cung": "Cửa Mê Cung",
        "n_day_thung": "Đáy Thung Cực Tiểu",
        "n_cuu_vi": "Gốc Cổ Thụ Đông Nam",
    }
    route_signs(m, named, at={"n_nga_ba", "mdl_leu_bia_rung", "mdl_tram_nga_bay", "mdl_am_khe_muc",
                              "n_nga_bay", "n_da_co_thu"})

    # ---- 8. the monsters
    monsters(m, cells)

    # ---- 9, 10
    bare(m, lm)
    m.dress_barriers()
    dress_maze(m)
    m.scatter()
    m.obj("Cổng Tây", "prop", 0, GATE_Y * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", -8, GATE_Y * T, T + 12, 4 * T, target="truc_lam_thon", target_spawn="from_forest")
    m.sign("Về Trúc Lâm Thôn", "Tây → Trúc Lâm Thôn", 3, GATE_Y - 2)
    m.poi("gate", "Cổng Tây · về Trúc Lâm Thôn", 1, GATE_Y + 1)
    m.obj("spawn", "spawn", SPAWN[0] * T, SPAWN[1] * T, 1, 1)
    m.obj("from_village", "spawn", SPAWN[0] * T, SPAWN[1] * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="ink_tree",
                    gaps={("w", y) for y in range(GATE_Y, GATE_Y + 4)})


# ------------------------------------------------------------------ the glades
def glade_seeds(m, rng) -> tuple[list, dict]:
    """(seeds, the ids of the special glades): (id, tile, khu id) for every glade."""
    seeds: list[tuple] = []
    fixed: dict[str, str] = {}

    def add(sid, tile, kid):
        seeds.append((sid, tuple(tile), kid))
        return sid

    def fill_khu(kid, rect, spacing, have, prefix):
        pts = spread(rng, rect, spacing, fixed=have, margin=6)
        for n, p in enumerate(pts):
            add(f"{prefix}_{n}", p, kid)

    # Bìa Rừng: the first junction, the camp, the fox's den, the wisps' glade
    add("n_nga_ba", NGA_BA, "mdl_bia_rung")
    add("mdl_leu_bia_rung", CAMP1, "mdl_bia_rung")
    add("n_hang_ho", HANG_HO, "mdl_bia_rung")
    add("n_lan_hoa", (24, 100), "mdl_bia_rung")
    fill_khu("mdl_bia_rung", (0, 80, 109, 159), 25, [NGA_BA, CAMP1, HANG_HO, (24, 100)], "bia")
    # Rừng Rẽ Nhánh: a tree; the leaf of Linh Hồ
    add("n_linh_ho", LINH_HO_LEAF, "mdl_re_nhanh")
    fill_khu("mdl_re_nhanh", (0, 0, 109, 79), 24, [LINH_HO_LEAF], "re")
    # Lũng Tơ Nhện
    add("n_mang_to", (52, 200), "mdl_to_nhen")
    fill_khu("mdl_to_nhen", (0, 160, 109, 239), 25, [(52, 200)], "nhen")
    fixed["nhen_hub"] = "n_mang_to"
    # Cổ Lâm Vòng Lặp: a ring of eight glades round the banyan
    add("n_da_co_thu", DA_CO_THU, "mdl_vong_lap")
    cx, cy = DA_CO_THU
    for i in range(8):
        a = -math.pi / 2 + i * 2 * math.pi / 8
        add(f"vong_{i}", (round(cx + 36 * math.cos(a)), round(cy + 26 * math.sin(a))), "mdl_vong_lap")
    # Trung Lâm Ngã Bảy: the hub, seven glades round it (the camp is the western one), the corners
    add("n_nga_bay", NGA_BAY, "mdl_nga_bay")
    add("mdl_tram_nga_bay", CAMP2, "mdl_nga_bay")
    ring = [CAMP2]
    for i in range(1, 7):
        a = math.pi + i * 2 * math.pi / 7
        p = (round(NGA_BAY[0] + 29 * math.cos(a)), round(NGA_BAY[1] + 26 * math.sin(a)))
        add(f"bay_{i}", p, "mdl_nga_bay")
        ring.append(p)
    fill_khu("mdl_nga_bay", (110, 80, 214, 159), 24, [NGA_BAY] + ring, "bayx")
    # Ngõ Cụt Sương Mù: the deepest dead end
    add("n_ngo_cut_sau", NGO_CUT_SAU, "mdl_ngo_cut")
    add("n_suong", (160, 200), "mdl_ngo_cut")
    fill_khu("mdl_ngo_cut", (110, 160, 214, 239), 23, [NGO_CUT_SAU, (160, 200)], "cut")
    fixed["cut_hub"] = "n_suong"
    # Hốc Cây Mẹ
    add("n_cay_me", CAY_ME, "mdl_cay_me")
    fill_khu("mdl_cay_me", (215, 0, 319, 71), 27, [CAY_ME, CAMP3], "me")
    # Thung Cực Tiểu
    add("n_day_thung", DAY_THUNG, "mdl_cuc_tieu")
    add("n_cuu_vi", CUU_VI, "mdl_cuc_tieu")
    fill_khu("mdl_cuc_tieu", (215, 168, 319, 239), 27, [DAY_THUNG, CUU_VI], "thung")
    root = min((s for s in seeds if s[2] == "mdl_re_nhanh"), key=lambda s: abs(s[1][0] - 40) + abs(s[1][1] - 74))
    fixed["re_root"] = root[0]
    return seeds, fixed


def graph_edges(m, cells: Cells, rng, ri: dict) -> list[tuple]:
    """(a, b, crosses Khe Mực) for every edge of the forest's graph."""
    out: list[tuple] = []

    def add(a, b, chasm=False):
        if a != b and not any({a, b} == {x, y} for x, y, _c in out):
            out.append((a, b, chasm))

    def leaf_only(pairs, leaves):
        """Keep one pair per forced leaf (to its nearest neighbour): it stays a dead end."""
        keep = []
        for lf in leaves:
            mine = [p for p in pairs if lf in p]
            if mine:
                keep.append(min(mine, key=lambda p: cells.dist(*p)))
        return [p for p in pairs if not any(lf in p for lf in leaves)] + keep

    # Bìa Rừng: a spanning tree with loops; the fox's den a dead end off the first junction
    p = leaf_only(cells.same_khu_pairs(ri["bia"]), ["n_hang_ho"])
    for a, b in cells.tree(p, rng, extra=4, keep=[("n_nga_ba", "mdl_leu_bia_rung")]):
        add(a, b)
    # Rừng Rẽ Nhánh: a tree and nothing else
    for a, b in cells.tree(leaf_only(cells.same_khu_pairs(ri["re"]), ["n_linh_ho"]), rng):
        add(a, b)
    # Lũng Tơ Nhện: a tree with two loops
    for a, b in cells.tree(cells.same_khu_pairs(ri["nhen"]), rng, extra=2):
        add(a, b)
    # Cổ Lâm Vòng Lặp: the ring, two spokes to the banyan
    for i in range(8):
        add(f"vong_{i}", f"vong_{(i + 1) % 8}")
    add("n_da_co_thu", "vong_2")
    add("n_da_co_thu", "vong_6")
    # Trung Lâm Ngã Bảy: the seven trails of the hub, the rest a tree, two shortcuts
    for sid in ["mdl_tram_nga_bay"] + [f"bay_{i}" for i in range(1, 7)]:
        add("n_nga_bay", sid)
    rest = [q for q in cells.same_khu_pairs(ri["bay"]) if "n_nga_bay" not in q]
    for a, b in cells.tree(rest, rng, keep=[]):
        add(a, b)
    corner = [s for s in cells.ids if s.startswith("bayx_")]
    for i, ring_id in enumerate(("bay_2", "bay_5")):
        far = [c for c in corner if c not in cells.neighbours(ring_id) and 20 < cells.dist(c, ring_id) < 46]
        if far:
            add(ring_id, min(far, key=lambda c: cells.dist(c, ring_id)))
    # Ngõ Cụt Sương Mù: a tree of long branches
    for a, b in cells.tree(leaf_only(cells.same_khu_pairs(ri["cut"]), ["n_ngo_cut_sau"]), rng):
        add(a, b)
    # Hốc Cây Mẹ and Thung Cực Tiểu: trees with loops
    for a, b in cells.tree(cells.same_khu_pairs(ri["me"]), rng, extra=2):
        add(a, b)
    for a, b in cells.tree(cells.same_khu_pairs(ri["thung"]), rng, extra=2):
        add(a, b)
    # between the khu
    add("gate", "n_nga_ba")
    add(*cells.link(ri["bia"], ri["re"], (40, 80)))
    add(*cells.link(ri["bia"], ri["nhen"], (24, 160)))
    add(*cells.link(ri["bia"], ri["nhen"], (88, 160)))
    a, _b = cells.link(ri["bia"], ri["bay"], (110, 120))
    add(a, "mdl_tram_nga_bay")
    add(*cells.link(ri["nhen"], ri["cut"], (110, 206)))
    add(*cells.link(ri["vong"], ri["bay"], (150, 80)))
    add(*cells.link(ri["bay"], ri["cut"], (178, 160)))
    # over Khe Mực: three stone bridges
    add(*cells.link(ri["vong"], ri["me"], (215, 36)), True)
    add("bay_4", "mdl_am_khe_muc", True)
    add(*cells.link(ri["cut"], ri["thung"], (215, 204)), True)
    # Thâm Xứ: the camp, the three doors of the maze
    add("mdl_am_khe_muc", "n_cua_me_cung")
    me = [s for s in cells.ids if cells.region_of[s] == ri["me"]]
    th = [s for s in cells.ids if cells.region_of[s] == ri["thung"]]
    near = lambda pool, p: min(pool, key=lambda s: math.hypot(cells.tile[s][0] - p[0], cells.tile[s][1] - p[1]))  # noqa: E731
    add("mdl_am_khe_muc", near(me, (234, 64)))
    add("mdl_am_khe_muc", near(th, (234, 176)))
    add("n_cua_bac", near(me, m.nodes["n_cua_bac"]["tile"]))
    add("n_cua_nam", near(th, m.nodes["n_cua_nam"]["tile"]))
    return out


def spine_edges(edges, tiles: dict, stops: list[str]) -> set:
    """The edges on the shortest ways from each stop to the next: the main road."""
    import heapq
    adj: dict[str, list] = {}
    for a, b, _c in edges:
        w = math.dist(tiles[a], tiles[b])
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    out = set()
    for s, t in zip(stops, stops[1:]):
        dist, prev, q = {s: 0.0}, {}, [(0.0, s)]
        while q:
            d, u = heapq.heappop(q)
            if u == t:
                break
            if d > dist.get(u, 1e18):
                continue
            for v, w in adj.get(u, ()):
                if d + w < dist.get(v, 1e18):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(q, (d + w, v))
        u = t
        while u in prev:
            out.add(frozenset((u, prev[u])))
            u = prev[u]
    return out


# ------------------------------------------------------------------ the features
def valley(m) -> None:
    """Thung Cực Tiểu: rings of ground round the bottom, darker as they go down."""
    bx, by = DAY_THUNG
    for y in range(by - 13, by + 14):
        for x in range(bx - 16, bx + 17):
            d = math.hypot(x - bx, (y - by) * 1.2)
            if d > 15:
                continue
            key = "stone0" if d < 2.5 else "dirt0" if d < 6.5 else "dark_grass1" if d < 10.5 else "dark_grass0"
            if 6.5 <= d < 7.3 or 10.5 <= d < 11.3:
                key = "stone0"             # the contour lines
            m.setg(x, y, key)


def disc(m, center, r, inner, rim) -> None:
    """The ground of a landmark: a round floor of `inner` with a rim of `rim`."""
    cx, cy = center
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            d = math.hypot(x - cx, (y - cy) * 1.15)
            if d <= r and m.inside(x, y, 2) and not m.hard[m.i(x, y)]:
                m.setg(x, y, inner if d < r - 1.2 else rim)


def landmark_rects() -> list[tuple]:
    """The ground of the landmarks: no glade wall crosses it, no scattered prop grows on it (the
    roads still pass and are painted there)."""
    x, y = NGA_BA
    out = [(1, GATE_Y - 3, 8, GATE_Y + 5), (x - 3, y - 5, x + 3, y + 4)]
    bx, by = DAY_THUNG
    out.append((bx - 11, by - 9, bx + 11, by + 9))
    for (cx, cy), r in ((DA_CO_THU, 7), (NGA_BAY, 6), (CAY_ME, 7), (HANG_HO, 4), (LINH_HO_LEAF, 3),
                        (NGO_CUT_SAU, 3), (CUU_VI, 4), ((52, 200), 6)):
        out.append((cx - r, cy - r, cx + r, cy + r))
    return out


def no_walls(m, rects) -> None:
    for (x0, y0, x1, y1) in rects:
        m.keep_rect(x0, y0, x1, y1)


def release(m, rects) -> None:
    """The landmarks' ground is ordinary ground again (roads paint over it) ..."""
    for (x0, y0, x1, y1) in rects:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if m.inside(x, y):
                    m.keep[m.i(x, y)] = 0


def bare(m, rects) -> None:
    """... but nothing is scattered on it."""
    for (x0, y0, x1, y1) in rects:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m.blocked_tiles.add((x, y))


def maze(m, rng) -> None:
    """Mê Cung Ngàn Lá: a perfect maze of MNX x MNY cells (a random depth-first walk: a spanning
    tree of the grid), a few hedges taken out so it has loops, a heart of 4 x 4 cells in the
    middle, three doors. Hedges are solid tiles roads never cross; corridors are kept clear."""
    W = m.W
    wall_w = 2
    x1, y1 = MX + MC * MNX + wall_w - 1, MY + MC * MNY + wall_w - 1
    solid = {(x, y) for x in range(MX, x1 + 1) for y in range(MY, y1 + 1)}

    def cell_tiles(i, j):
        bx, by = MX + MC * i + wall_w, MY + MC * j + wall_w
        return {(x, y) for x in range(bx, bx + MC - wall_w) for y in range(by, by + MC - wall_w)}

    def opening(i, j, di, dj):
        """The hedge tiles between cell (i, j) and its neighbour (i + di, j + dj)."""
        bx, by = MX + MC * i + wall_w, MY + MC * j + wall_w
        n = MC - wall_w
        if di == 1:
            return {(bx + n + k, y) for k in range(wall_w) for y in range(by, by + n)}
        if di == -1:
            return {(bx - 1 - k, y) for k in range(wall_w) for y in range(by, by + n)}
        if dj == 1:
            return {(x, by + n + k) for k in range(wall_w) for x in range(bx, bx + n)}
        return {(x, by - 1 - k) for k in range(wall_w) for x in range(bx, bx + n)}

    hi0, hj0, hi1, hj1 = HEART
    heart = {(i, j) for i in range(hi0, hi1) for j in range(hj0, hj1)}
    open_ = set()
    for i in range(MNX):
        for j in range(MNY):
            open_ |= cell_tiles(i, j)
    # the heart: one room (the hedges inside it go)
    hx0, hy0 = MX + MC * hi0 + wall_w, MY + MC * hj0 + wall_w
    hx1, hy1 = MX + MC * hi1 - 1, MY + MC * hj1 - 1
    open_ |= {(x, y) for x in range(hx0, hx1 + 1) for y in range(hy0, hy1 + 1)}
    # the walk
    start = (0, MAZE_W_ROW)
    seen = {start} | heart
    stack = [start]
    links = []
    while stack:
        i, j = stack[-1]
        nb = [(di, dj) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= i + di < MNX and 0 <= j + dj < MNY and (i + di, j + dj) not in seen]
        if not nb:
            stack.pop()
            continue
        di, dj = rng.choice(nb)
        links.append((i, j, di, dj))
        seen.add((i + di, j + dj))
        stack.append((i + di, j + dj))
    for (i, j, di, dj) in links:
        open_ |= opening(i, j, di, dj)
    # the heart's doors: one on each side
    for (i, j, di, dj) in ((hi0 - 1, hj0 + 1, 1, 0), (hi1, hj1 - 2, -1, 0), (hi0 + 2, hj0 - 1, 0, 1),
                           (hi0 + 1, hj1, 0, -1)):
        open_ |= opening(i, j, di, dj)
    # loops: a few more hedges go
    cand = [(i, j, di, dj) for i in range(MNX) for j in range(MNY) for di, dj in ((1, 0), (0, 1))
            if i + di < MNX and j + dj < MNY and (i, j) not in heart and (i + di, j + dj) not in heart
            and (i, j, di, dj) not in links]
    rng.shuffle(cand)
    for c in cand[:16]:
        open_ |= opening(*c)
    # the three doors in the outer hedge
    wy = MY + MC * MAZE_W_ROW + wall_w
    open_ |= {(x, y) for x in (MX, MX + 1) for y in range(wy, wy + MC - wall_w)}
    nx = MX + MC * MAZE_N_COL + wall_w
    open_ |= {(x, y) for x in range(nx, nx + MC - wall_w) for y in (MY, MY + 1)}
    sx = MX + MC * MAZE_S_COL + wall_w
    open_ |= {(x, y) for x in range(sx, sx + MC - wall_w) for y in (y1 - 1, y1)}
    hedge = solid - open_
    # the strip east of the maze is hedge too (nobody walks round it)
    hedge |= {(x, y) for x in range(x1 + 1, m.W - 1) for y in range(MY, y1 + 1)}
    for (x, y) in sorted(hedge):
        j = y * W + x
        m.hard[j] = SOLID_WALL
        m.barrier[j] = None
        m.keep[j] = 1
        m.setg(x, y, "dark_grass1" if (x + y) % 3 else "dark_grass0")
    for (x, y) in sorted(open_):
        j = y * W + x
        m.hard[j] = 0
        m.barrier[j] = None
        m.keep[j] = 1
        r = m.rng.random()
        m.setg(x, y, "grass1" if r < 0.55 else "grass0" if r < 0.85 else "grass2")
    m.maze_hedge = hedge
    m.maze_open = open_


def dress_maze(m) -> None:
    """The hedges: a bush on every other tile, a pine at the corners where hedges meet."""
    hedge = m.maze_hedge
    for (x, y) in sorted(hedge):
        if (x + y) % 2:
            continue
        if x >= MX + MC * MNX + 2:
            m._place("pine" if (x + 2 * y) % 4 == 0 else "dead_tree", x, y, solid=False)
            continue
        corner = (x - MX) % MC in (0, 1) and (y - MY) % MC in (0, 1)
        m._place("pine" if corner and (x - MX) % MC == 0 and (y - MY) % MC == 0 else "bush", x, y, solid=False)
        m.blocked_tiles.add((x, y))


# ------------------------------------------------------------------ the places
def _free(m, x, y) -> bool:
    j = m.i(x, y)
    return not (m.road[j] or m.hard[j] or (x, y) in m.blocked_tiles)


def tree_near(m, x, y, sprite="tree", avoid=()) -> None:
    """A solid tree on the free tile nearest (x, y) (never on a road nor on `avoid`)."""
    for r in range(0, 4):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r or (x + dx, y + dy) in avoid:
                    continue
                if _free(m, x + dx, y + dy) and _free(m, x + dx, y + dy + 1):
                    tree_at(m, x + dx, y + dy, sprite)
                    return


def tree_at(m, x, y, sprite="tree") -> None:
    """A solid tree, unless its tile is a road, a wall or taken."""
    if _free(m, x, y):
        m.tree(x, y, sprite)
        m.blocked_tiles.update({(x - 1, y), (x, y), (x + 1, y), (x, y - 1)})


def thing_at(m, name, sprite, x, y, w, h, foot=None, **kw) -> None:
    if _free(m, x, y):
        m.thing(name, sprite, x, y, w, h, foot=foot, **kw)


def ring_of(cx, cy, n, rx, ry, phase=0.0):
    for i in range(n):
        a = phase + i * 2 * math.pi / n
        yield i, round(cx + rx * math.cos(a)), round(cy + ry * math.sin(a))


def places(m, cells: Cells, fixed: dict) -> None:
    # the first junction: the old sign, the spear of the first fork
    x, y = NGA_BA
    m.sign("Ngã ba", "Ngã ba: mỗi lối là một cạnh của đồ thị", x + 2, y - 4)
    thing_at(m, "Đá ngã ba", "rock", x - 2, y - 4, 16, 12, foot=(12, 8))
    m.poi("landmark", "Ngã Ba Đầu Tiên", *NGA_BA)
    # Hang Mặc Hồ: a den of ink trees under a boulder
    hx, hy = HANG_HO
    for i, (dx, dy) in enumerate(((-3, -1), (3, -1), (-3, 3), (3, 3))):
        tree_at(m, hx + dx, hy + dy, "ink_tree")
    thing_at(m, "Đá hang", "boulder", hx, hy - 3, 32, 24, foot=(26, 10))
    m.poi("landmark", "Hang Mặc Hồ", hx, hy)
    # the root of the branching wood
    rx, ry = cells.tile[fixed["re_root"]]
    spot = m.free_near(rx, ry, 4)
    if spot:
        m.sign("Rừng Rẽ Nhánh", "Rừng Rẽ Nhánh: lối tỏa như cành cây, không vòng nào.\n"
               "Mỗi nhánh tận cùng là một ngõ cụt.", *spot)
    tree_at(m, rx - 3, ry - 2, "peach")
    tree_at(m, rx + 3, ry - 2, "peach")
    m.poi("landmark", "Gốc Rừng Rẽ Nhánh", rx, ry)
    lx, ly = LINH_HO_LEAF
    for i, (dx, dy) in enumerate(((-2, -2), (2, -2), (0, -3), (-3, 1), (3, 1))):
        thing_at(m, "Bụi hoa", "bush", lx + dx, ly + dy, 24, 16, variant=i)
    m.poi("beast", "Ngõ Cụt Linh Hồ", lx, ly)
    # Mạng Tơ Lớn: a ring of dead trees in the spiders' glade
    wx, wy = 52, 200
    for i, tx, ty in ring_of(wx, wy, 10, 6, 5):
        tree_at(m, tx, ty, "ink_tree")
    thing_at(m, "Khúc gỗ", "log", wx - 1, wy - 1, 24, 16, foot=(18, 8))
    m.poi("landmark", "Mạng Tơ Lớn", wx, wy)
    # the old banyan and its ring
    bx, by = DA_CO_THU
    tree_near(m, bx + 1, by - 2, "tree", avoid={(bx, by), (bx, by - 1)})
    for i, tx, ty in ring_of(bx, by, 8, 6, 5, math.pi / 8):
        tree_at(m, tx, ty, "tree")
    m.sign("Đa Cổ Thụ", "Cây đa cổ thụ: các khoảng trống quanh nó nối thành một vòng,\nđi mãi lại về chỗ cũ.",
           bx + 2, by + 1)
    m.poi("landmark", "Đa Cổ Thụ", bx, by)
    # Ngã Bảy: seven stones round the hub
    nx, ny = NGA_BAY
    for i, tx, ty in ring_of(nx, ny, 7, 5, 4, math.pi / 7):
        thing_at(m, "Đá", "rock", tx, ty, 16, 12, foot=(12, 8), variant=i)
    m.sign("Ngã Bảy", "Ngã Bảy: bảy lối gặp nhau ở một đỉnh.\nBậc của đỉnh này là bảy.", nx + 2, ny + 2)
    m.poi("landmark", "Ngã Bảy", nx, ny)
    # the deepest dead end
    dx_, dy_ = NGO_CUT_SAU
    thing_at(m, "Mây", "cloud_puff", dx_ - 2, dy_ - 2, 32, 20, variant=3)
    thing_at(m, "Đá", "rock", dx_ + 2, dy_ - 2, 16, 12, foot=(12, 8))
    m.poi("landmark", "Ngõ Cụt Sâu Nhất", dx_, dy_)
    # the mother tree and the ring of ink trees round its hollow
    cx, cy = CAY_ME
    tree_near(m, cx, cy - 2, "tree", avoid={(cx, cy), (cx, cy - 1)})
    for i, tx, ty in ring_of(cx, cy - 1, 9, 6, 5):
        tree_at(m, tx, ty, "ink_tree")
    m.sign("Hốc Cây Mẹ", "Cây mẹ của cả khu rừng. Mộc Yêu canh hốc cây.", cx + 2, cy + 1)
    m.poi("landmark", "Hốc Cây Mẹ", cx, cy - 2)
    # the heart of the maze
    hx0, hy0 = MX + MC * HEART[0] + 2, MY + MC * HEART[1] + 2
    hx1, hy1 = MX + MC * HEART[2] - 1, MY + MC * HEART[3] - 1
    ax, ay = (hx0 + hx1) // 2, (hy0 + hy1) // 2
    m.thing("Bia Cây Khung", "tablet", ax, ay - 2, 16, 24, foot=(12, 8))
    for i, (ddx, ddy) in enumerate(((-5, -5), (5, -5), (-5, 5), (5, 5))):
        m.thing("Đèn", "lantern", ax + ddx, ay + ddy, 8, 24, foot=(4, 4), variant=i)
    m.sign("Tâm Mê Cung", "Tâm mê cung. Lối đã đi qua là một cây khung:\nmỗi ô một đường duy nhất về cửa.",
           ax + 2, ay - 2)
    m.poi("landmark", "Tâm Mê Cung", ax, ay)
    m.sign("Cửa Mê Cung", "Mê Cung Ngàn Lá: lạc lối thì theo Chỉ Đường.", MX - 2, MY + MC * MAZE_W_ROW + 1)
    # the bottom of the valley
    bx, by = DAY_THUNG
    for i, tx, ty in ring_of(bx, by, 10, 9, 7):
        thing_at(m, "Đá", "rock", tx, ty, 16, 12, foot=(12, 8), variant=i + 30)
    m.sign("Đáy Thung", "Đáy thung: mọi sườn dốc đều đổ về đây.\nĐiểm cực tiểu của rừng.", bx + 3, by + 2)
    m.poi("landmark", "Đáy Thung Cực Tiểu", bx, by)
    # Cửu Vĩ Hồ's old tree in the south-east corner
    cx, cy = CUU_VI
    tree_near(m, cx, cy - 2, "tree", avoid={(cx, cy), (cx, cy - 1), CUU_VI_HO})
    thing_at(m, "Đèn", "lantern", cx - 2, cy, 8, 24, foot=(4, 4), variant=9)
    m.poi("beast", "Gốc Cổ Thụ · Cửu Vĩ Hồ", *CUU_VI_HO)


# ------------------------------------------------------------------ the monsters
def monsters(m, cells: Cells) -> None:
    """Band 1: Tri Chu Tinh and Hoa Yêu, and by the gate the old Mực Con, Lân Hỏa Yêu and Mặc Hồ
    the first quests send a newcomer after; band 2: the same with their higher nodes and a few
    elites; band 3: only the elites (the land has no normal creature of tầng 7-9)."""
    hand = []

    def area(kid, kind, rect, want):
        walk, _mine = m._walk_count(rect)
        cnt = max(1, min(want, int(walk // 115)))
        m.monster_area(kid, kind, rect, cnt, name=f"{kid}_{kind}_{len(hand)}")
        hand.append(rect)

    area("mdl_bia_rung", "ink_slime", (15, 111, 33, 125), 2)
    area("mdl_bia_rung", "ink_slime", (15, 131, 33, 142), 2)
    area("mdl_bia_rung", "tone_wisp", (15, 94, 33, 108), 2)
    hx, hy = HANG_HO
    area("mdl_bia_rung", "ink_fox", (hx - 4, hy - 4, hx + 4, hy + 4), 1)
    cx, cy = CAY_ME
    area("mdl_cay_me", "moc_yeu", (cx - 6, cy - 5, cx + 6, cy + 7), 1)
    sk = lambda r: overlaps(r, hand)  # noqa: E731
    m.monsters("mdl_bia_rung", [("tri_chu_tinh", 2), ("hoa_yeu", 2)], tiles_per=200, skip=sk)
    m.monsters("mdl_re_nhanh", [("hoa_yeu", 3), ("tri_chu_tinh", 1)], tiles_per=200, skip=sk)
    m.monsters("mdl_to_nhen", [("tri_chu_tinh", 3), ("hoa_yeu", 1)], tiles_per=200, skip=sk)
    m.monsters("mdl_vong_lap", [("tri_chu_tinh", 2), ("hoa_yeu", 2)], [("bach_vien", 2), ("moc_yeu", 1)],
               tiles_per=200, skip=sk)
    m.monsters("mdl_nga_bay", [("hoa_yeu", 2), ("tri_chu_tinh", 2)], [("bach_vien", 2), ("moc_yeu", 1)],
               tiles_per=200, skip=sk)
    m.monsters("mdl_ngo_cut", [("tri_chu_tinh", 2), ("hoa_yeu", 2)], [("moc_yeu", 2), ("bach_vien", 1)],
               tiles_per=200, skip=sk)
    m.monsters("mdl_cay_me", [("bach_vien", 1), ("moc_yeu", 1)], cell=(16, 14), tiles_per=1e9, max_areas=6, skip=sk)
    m.monsters("mdl_cuc_tieu", [("moc_yeu", 1), ("bach_vien", 1)], cell=(16, 14), tiles_per=1e9, max_areas=7, skip=sk)
    # the maze: elites in its corridors, one in its heart
    picks = [(2, 2), (11, 2), (2, 11), (11, 11), (7, 1), (12, 7)]
    for n, (i, j) in enumerate(picks):
        x, y = MX + MC * i + 3, MY + MC * j + 3
        m.monster_area("mdl_me_cung", ("bach_vien", "moc_yeu")[n % 2], (x - 4, y - 4, x + 4, y + 4), 1,
                       name=f"mdl_me_cung_tinh_anh_{n}")
