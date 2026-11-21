"""Thiên Công Phường (zone thien_cong_phuong, land thien_cong_phuong, branch Lập Trình): the
abandoned craftsmen's city, a giant land of Đại Địa Đồ (320 x 240 tiles).

The gate is in the east (Trúc Lâm Thôn's west gate leads here) and the city sinks westward in
three tiers: the old quarters of Ngoại Vi (tầng 1-3) whose street grid still stands, a canal
across them; behind a fallen rampart the forges, gear yards and scrap yards of Trung Vực (tầng
4-6), where the grid starts to break; behind a crack of cold slag the ruins and the great foundry
of Thâm Xứ (tầng 7-9), where only a few streets are left. A rest camp waits after each wall.
Everything the small map had is here: the cold forge (chuy_1 hạ on its anvil, by the gate camp),
the gear workshop behind its mechanism gate (chuy_1 trung), the yard of the leader of the Cơ Quan
Nhân (chuy_1 thượng), the great furnace with three mouths and more (chuy_2 hạ, Tiểu Long), the
walled scrap yard (Tầm Bảo Thử), the well, the abandoned stall, the craftsmen's board.
"""
from __future__ import annotations

import math

from ..builder import T
from ..giant import DaiDiaDo, Theme, PAVED
from . import _xay_dung as X

ZONE = "thien_cong_phuong"
SIZE = (320, 240)

# the places other data points at (world_plan.json weapons_placed / beasts `pos`): tiles
LO_NGUOI = (287, 104)            # the cold forge by the gate camp: its dead furnace
CHUY_1_HA = (285, 108)           # on the anvil of the cold forge
XUONG = (140, 90, 158, 104)      # the gear workshop (fence outline), its gate in the south wall
CHUY_1_TRUNG = (144, 95)         # inside the workshop, behind the mechanism gate
SAN = (160, 146)                 # the yard of the leader of the Cơ Quan Nhân (centre)
CHUY_1_THUONG = SAN              # in the leader's hands
KHO = (121, 205, 139, 219)       # the walled scrap yard (wall outline), its gap in the north wall
TAM_BAO_THU = (127, 213)        # its nest among the heaps of gears
LO_DUC = (32, 186, 60, 208)      # the great foundry (wall outline), its door in the north wall
CHUY_2_HA = (46, 201)            # in front of the great furnace's middle mouth
TIEU_LONG = (51, 199)            # curled up by the furnace
GATE_Y = 118                     # the east gate covers tiles 118..121 of the east edge


# ------------------------------------------------------------------ the grounds
def g_pho_tho(P, D, r):          # old quarter: dirt, worn paving, stone, a few weeds
    if P > 0.66:
        return "stone0"
    if P < 0.2:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    return "dirt0"


def g_cho(P, D, r):              # the market: dirt trodden flat, a few stone patches, weeds
    if P > 0.7:
        return "stone0"
    if P < 0.24:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    return "dirt0"


def g_lo_ren(P, D, r):           # forges: stone and soot-dark dirt
    if P > 0.5:
        return "stone0"
    if P < 0.18:
        return "dark_grass1"
    return "dirt0"


def g_banh_rang(P, D, r):        # gear yards: dirt, stone; the plank floors are laid by hand
    if P > 0.7:
        return "stone0"
    if P < 0.2:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    return "dirt0" if D < 0.7 else "stone0"


def g_phe_lieu(P, D, r):         # scrap: dirt, stone, rank grass
    if P > 0.62:
        return "stone0"
    if P < 0.25:
        return "dark_grass1" if r < 0.7 else "dark_grass0"
    return "dirt0"


def g_do_nat(P, D, r):           # ruins taken back by the grass
    if P > 0.68:
        return "stone0"
    if P < 0.4:
        return "dark_grass0" if r < 0.6 else "dark_grass1"
    return "grass1" if D < 0.55 else "dirt0"


def g_lo_duc(P, D, r):           # the foundry ground: cinders, stone, a little scorched grass
    if P > 0.64:
        return "stone0"
    if P < 0.26:
        return "dark_grass1"
    return "dirt0"


def themes(m: DaiDiaDo) -> None:
    th = m.themes
    th["pho_tho"] = Theme("pho_tho", g_pho_tho, [("rock", 2), ("log", 2), ("stump", 1), ("tall_grass", 2), ("bush", 1)],
                          [("tree", 3), ("bush", 2), ("tall_grass", 1)], 0.02, 0.10, 16.0, 0.62, PAVED)
    th["cho_tho"] = Theme("cho_tho", g_cho, [("rock", 2), ("log", 1), ("tall_grass", 2), ("bush", 1), ("x_mat", 1)],
                          [("tree", 3), ("peach", 1), ("bush", 2)], 0.02, 0.10, 16.0, 0.62, PAVED)
    th["lo_ren"] = Theme("lo_ren", g_lo_ren, [("rock", 3), ("log", 1), ("x_anvil", 1), ("stump", 1)],
                         [("boulder", 2), ("dead_tree", 2), ("rock", 2)], 0.022, 0.12, 15.0, 0.6, PAVED)
    th["banh_rang"] = Theme("banh_rang", g_banh_rang, [("log", 3), ("stump", 3), ("rock", 1), ("tall_grass", 1)],
                            [("log", 2), ("stump", 2), ("tree", 2), ("bush", 1)], 0.024, 0.12, 15.0, 0.6, PAVED)
    th["phe_lieu"] = Theme("phe_lieu", g_phe_lieu, [("rock", 3), ("log", 2), ("stump", 2), ("boulder", 1),
                                                    ("tall_grass", 1)],
                           [("boulder", 3), ("rock", 2), ("dead_tree", 1), ("log", 1)], 0.028, 0.14, 14.0, 0.58, PAVED)
    th["do_nat"] = Theme("do_nat", g_do_nat, [("rock", 2), ("bush", 2), ("dead_tree", 2), ("tall_grass", 2),
                                              ("boulder", 1)],
                         [("dead_tree", 4), ("tree", 2), ("bush", 1), ("boulder", 1)], 0.04, 0.18, 15.0, 0.56, PAVED)
    th["lo_duc"] = Theme("lo_duc", g_lo_duc, [("rock", 3), ("boulder", 1), ("crystal", 1), ("dead_tree", 2),
                                              ("x_anvil", 1), ("log", 1)],
                         [("boulder", 3), ("dead_tree", 3), ("crystal", 1)], 0.045, 0.18, 14.0, 0.56, PAVED)


# ------------------------------------------------------------------ the map
def build() -> dict:
    W, H = SIZE
    m = DaiDiaDo(ZONE, "Thiên Công Phường", W, H, "thien_cong_phuong_dai_dia_do")
    themes(m)

    # ---- 1. the khu (band 1 by the east gate, band 3 in the far west)
    m.khu("tcp_pho_tho_cu", "Phố Thợ Cũ", 1, (210, 0, 319, 119), "pho_tho", (262, 60),
          "Khu xưởng cũ phía bắc cổng phường: phố còn nguyên ô bàn cờ, Cơ Quan Nhân vẫn đi tuần.")
    m.khu("tcp_cho_tho", "Chợ Thợ Hoang", 1, (210, 120, 319, 239), "cho_tho", (262, 180),
          "Chợ phiên của thợ phía nam cổng: sạp bỏ trống, Cơ Quan Thú lục lọi giữa các dãy hàng.")
    m.khu("tcp_xom_lo_ren", "Xóm Lò Rèn", 2, (105, 0, 209, 79), "lo_ren", (150, 40),
          "Những lò rèn tắt lửa quanh Hồ Tôi Thép; Lò Linh còn âm ỉ trong vài cửa lò.")
    m.khu("tcp_bai_banh_rang", "Bãi Bánh Răng", 2, (105, 80, 209, 159), "banh_rang", (150, 118),
          "Bãi bánh răng và Xưởng Bánh Răng sau cơ quan cửa; Cơ Quan Nhân Đầu Đàn giữ sân của nó.")
    m.khu("tcp_kho_phe_lieu", "Kho Phế Liệu", 2, (105, 160, 209, 239), "phe_lieu", (157, 200),
          "Băng chuyền gỗ dừng giữa chừng, đống phế liệu có tường vây nơi Tầm Bảo Thử làm ổ.")
    m.khu("tcp_pho_do_nat", "Phố Đổ Nát", 3, (0, 0, 104, 119), "do_nat", (52, 58),
          "Phố xưởng sụp đổ, cỏ mọc kín lối; chỉ tinh anh cơ quan còn canh Đình Tổ Nghề.")
    m.khu("tcp_dai_lo_duc", "Đại Lò Đúc", 3, (0, 120, 104, 239), "lo_duc", (52, 176),
          "Xưởng đúc lớn nhất phường, lò năm miệng nằm sau tường đá: Tiểu Long cuộn mình bên lò.")

    # ---- 2. the ground, the camps
    m.paint(warp=6.0, scale=26.0)
    m.camp("tcp_trai_cong", "Trại Cổng Phường", (300, 120), r=8,
           desc_vi="Trại ngay trong cổng phường, cạnh lò rèn nguội. Không có quái.",
           label_vi="Trại Cổng Phường · lò rèn nguội", to_edge="e")
    m.camp("tcp_tram_giua", "Trạm Thợ Giữa", (196, 120), r=6,
           desc_vi="Trạm nghỉ sau tường thành đổ, cửa vào Trung Vực.", label_vi="Trạm Thợ Giữa · cửa Trung Vực")
    m.camp("tcp_lan_cuoi", "Lán Thợ Cuối", (92, 120), r=6,
           desc_vi="Lán nghỉ cuối cùng bên kia khe xỉ, cửa vào Thâm Xứ.", label_vi="Lán Thợ Cuối · cửa Thâm Xứ")
    m.clear_zones.append((304, GATE_Y - 4, W - 1, GATE_Y + 7))          # the gate and the spawn

    # ---- 3. the large features
    canal(m)
    m.lake(178, 22, 7, 4)                                 # Hồ Tôi Thép, the quench pond
    m.lake(72, 92, 5, 3)                                  # a sunken cellar full of rain
    keep_landmarks(m)
    workshop_walls(m)

    # ---- 4. the walls: a fallen rampart, then a crack of cold slag
    band1, band2, band3 = ("tcp_pho_tho_cu", "tcp_cho_tho"), \
        ("tcp_xom_lo_ren", "tcp_bai_banh_rang", "tcp_kho_phe_lieu"), ("tcp_pho_do_nat", "tcp_dai_lo_duc")
    walls = {}
    for a in band1:
        for b in band2:
            walls[(a, b)] = "cliff"
    for a in band2:
        for b in band3:
            walls[(a, b)] = "chasm"
    for a in band1:
        for b in band3:
            walls[(a, b)] = "chasm"
    m.barriers(walls, default="open")

    # ---- 5. the streets, then the roads (they follow the streets)
    grids = {}
    for kid, pitch, keep_p, off in (("tcp_pho_tho_cu", 14, 0.96, (0, 0)), ("tcp_cho_tho", 14, 0.92, (3, 2)),
                                    ("tcp_xom_lo_ren", 16, 0.8, (2, 0)), ("tcp_bai_banh_rang", 16, 0.72, (0, 3)),
                                    ("tcp_kho_phe_lieu", 18, 0.66, (4, 0)), ("tcp_pho_do_nat", 16, 0.42, (0, 2)),
                                    ("tcp_dai_lo_duc", 20, 0.34, (5, 0))):
        grids[kid] = X.streets(m, kid, pitch, keep_p, off)
    canal_bridges(m, grids["tcp_pho_tho_cu"][1] + grids["tcp_cho_tho"][1])
    conveyors(m)

    m.node("gate", (W - 4, GATE_Y + 2), "Cổng Đông · về Trúc Lâm Thôn")
    m.node("n_pho_tho", (262, 60), "Phố Thợ Cũ · Ngoại Vi, tầng 1-3")
    m.node("n_cho", (262, 180), "Chợ Thợ Hoang · Ngoại Vi, tầng 1-3")
    m.node("n_lo_ren", (150, 40), "Xóm Lò Rèn · Trung Vực, tầng 4-6")
    m.node("n_banh_rang", (150, 118), "Bãi Bánh Răng · Trung Vực, tầng 4-6")
    m.node("n_xuong", (149, XUONG[3] + 3), "Xưởng Bánh Răng", sign=False)
    m.node("n_san", (SAN[0], SAN[1] + 7), "Sân Đầu Đàn", sign=False)
    m.node("n_phe_lieu", (157, 200), "Kho Phế Liệu · Trung Vực, tầng 4-6")
    m.node("n_kho", (130, KHO[1] - 3), "Bãi phế liệu có tường", sign=False)
    m.node("n_do_nat", (52, 58), "Phố Đổ Nát · Thâm Xứ, tầng 7-9")
    m.node("n_dinh_to", (52, 46), "Đình Tổ Nghề", sign=False)
    m.node("n_lo_duc", (52, 176), "Đại Lò Đúc · Thâm Xứ, tầng 7-9")
    m.node("n_cua_lo", (46, LO_DUC[1] - 3), "Cửa Đại Lò Đúc", sign=False)
    m.network([
        ("gate", "tcp_trai_cong", "main"),
        ("tcp_trai_cong", "n_pho_tho", "main"),
        ("tcp_trai_cong", "n_cho", "main"),
        ("tcp_trai_cong", "tcp_tram_giua", "main"),
        ("tcp_tram_giua", "n_lo_ren", "main"),
        ("tcp_tram_giua", "n_banh_rang", "main"),
        ("tcp_tram_giua", "n_phe_lieu", "main"),
        ("n_banh_rang", "n_xuong", "trail"),
        ("n_banh_rang", "n_san", "trail"),
        ("n_phe_lieu", "n_kho", "trail"),
        ("n_pho_tho", "n_lo_ren", "trail"),
        ("n_cho", "n_phe_lieu", "trail"),
        ("n_banh_rang", "tcp_lan_cuoi", "main", True),
        ("tcp_lan_cuoi", "n_do_nat", "main"),
        ("tcp_lan_cuoi", "n_lo_duc", "main"),
        ("n_do_nat", "n_dinh_to", "trail"),
        ("n_lo_duc", "n_cua_lo", "trail"),
        ("n_lo_ren", "n_do_nat", "trail", True),
    ])
    m.carve([(x, GATE_Y + 2) for x in range(300, W - 1)], "main")      # through the gate

    # ---- 6. the places
    gate_camp(m)
    landmarks(m)
    furnish(m, grids)
    m.signposts()

    # ---- 8. the monsters
    monsters(m)

    # ---- 9, 10
    m.dress_barriers()
    m.scatter()
    m.gate("e", GATE_Y, "truc_lam_thon", "from_thien_cong_phuong", "Cổng Đông")
    m.sign("Về Trúc Lâm Thôn", "Đông → Trúc Lâm Thôn", W - 5, GATE_Y - 2)
    m.poi("gate", "Cổng Đông · về Trúc Lâm Thôn", W - 2, GATE_Y + 2)
    m.obj("spawn", "spawn", (W - 4) * T, (GATE_Y + 2) * T, 1, 1)
    m.obj("from_village", "spawn", (W - 4) * T, (GATE_Y + 2) * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="ink_tree",
                    gaps={("e", y) for y in range(GATE_Y, GATE_Y + 4)})


# ------------------------------------------------------------------ the features
def canal(m: DaiDiaDo) -> None:
    """Kênh Thợ: a straight canal with stone banks down the old quarters, a little bent where the
    old water wheels stood; the roads bridge it."""
    pts = [(239 + round(2.5 * math.sin(y / 23.0)), y) for y in range(2, 238)]
    m.river(pts, width=3)


def canal_bridges(m: DaiDiaDo, rows: list) -> None:
    """A plank bridge wherever a street of the old quarters meets the canal from both banks."""
    for y in rows:
        left = next((x for x in range(236, 224, -1) if m.road[m.i(x, y)]), None)
        right = next((x for x in range(242, 254) if m.road[m.i(x, y)]), None)
        if left is not None and right is not None and m.rng.random() < 0.7:
            m.carve([(x, y) for x in range(left, right + 1)], "trail")


def keep_landmarks(m: DaiDiaDo) -> None:
    x, y = LO_NGUOI
    m.keep_rect(x - 5, y - 3, x + 5, y + 5)                    # the cold forge
    m.keep_rect(256, 54, 268, 64)                              # Giếng Thợ Cả
    m.keep_rect(252, 172, 274, 188)                            # Chợ Phiên
    m.keep_rect(140, 26, 162, 38)                              # Lò Rèn Ba Miệng
    m.keep_rect(XUONG[0] - 1, XUONG[1] - 1, XUONG[2] + 1, XUONG[3] + 1)
    m.keep_rect(SAN[0] - 7, SAN[1] - 5, SAN[0] + 7, SAN[1] + 5)
    m.keep_rect(KHO[0] - 1, KHO[1] - 1, KHO[2] + 1, KHO[3] + 1)
    m.keep_rect(44, 34, 60, 46)                                # Đình Tổ Nghề
    m.keep_rect(LO_DUC[0] - 2, LO_DUC[1] - 4, LO_DUC[2] + 2, LO_DUC[3] + 1)


def workshop_walls(m: DaiDiaDo) -> None:
    """The fences and walls of the gear workshop, the scrap yard and the great foundry, with their
    floors; built before the barriers and roads (the roads come in through the gaps)."""
    # the gear workshop: plank floor inside a bamboo fence, the mechanism gate in the south wall
    x0, y0, x1, y1 = XUONG
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            m.setg(x, y, "wood0")
    gate_x = (148, 149, 150)
    X.fence(m, {t for t in X.outline(*XUONG) if not (t[1] == y1 and t[0] in gate_x)}, "dirt0")
    # the scrap yard: a stone wall, a gap in the north
    x0, y0, x1, y1 = KHO
    X.solid_ring(m, {t for t in X.outline(*KHO) if not (t[1] == y0 and t[0] in (129, 130, 131))}, "realm_wall0")
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            m.setg(x, y, "dirt0")
    # the great foundry: a wall of dark stone, the door in the north, a paved floor
    x0, y0, x1, y1 = LO_DUC
    door = (45, 46, 47)
    X.solid_ring(m, {t for t in X.outline(*LO_DUC) if not (t[1] == y0 and t[0] in door)}, "realm_wall0")
    X.solid_ring(m, {t for t in X.outline(x0 + 1, y0 + 1, x1 - 1, y1 - 1)
                     if not (t[1] == y0 + 1 and t[0] in door)}, "realm_wall0")
    for y in range(y0 + 2, y1 - 1):
        for x in range(x0 + 2, x1 - 1):
            m.setg(x, y, "plaza0" if (x + y) % 3 else "plaza1")
    # the casting channels, still glowing: from the door to the furnaces and across the hall
    for y in range(y0 + 2, y1 - 4):
        for x in (45, 46, 47):
            m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
    for x in range(x0 + 4, x1 - 3):
        for y in (196, 197):
            m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
    for y in range(y0 - 4, y0):                                # the forecourt
        for x in range(x0 + 6, x1 - 5):
            m.setg(x, y, "stone0")


def conveyors(m: DaiDiaDo) -> None:
    """Băng Chuyền: long plank lanes of Kho Phế Liệu, stopped halfway; rollers along them."""
    ri = X.region_index(m, "tcp_kho_phe_lieu")
    for y, xa, xb in ((172, 146, 204), (188, 112, 150), (228, 140, 200)):
        tiles = [(x, yy) for x in range(xa, xb + 1) for yy in (y, y + 1)
                 if m.region[m.i(x, yy)] == ri and not m.hard[m.i(x, yy)] and not m.keep[m.i(x, yy)]]
        X.lane(m, tiles, "wood0")
        for x in range(xa + 1, xb, 4):
            for yy in (y - 1, y + 2):
                X.try_thing(m, "log", x, yy, ri, "Con lăn băng chuyền")
    m.poi("landmark", "Băng Chuyền Gỗ", 175, 172)


def gate_camp(m: DaiDiaDo) -> None:
    """The cold forge (where chuy_1 hạ lies on the anvil), the well, the board of the craftsmen."""
    x, y = LO_NGUOI
    m.thing("Lò nguội", "furnace", x, y, 24, 28, foot=(18, 12))
    m.thing("Đe nguội", "anvil", CHUY_1_HA[0], CHUY_1_HA[1] - 1, 24, 20, foot=(20, 8))
    m.thing("Đe nguội", "anvil", x + 3, y + 3, 24, 20, foot=(20, 8))
    for i, (dx, dy) in enumerate(((-4, 1), (4, 1))):
        m.thing("Đèn", "lantern", x + dx, y + dy, 8, 24, foot=(4, 4), variant=i)
    m.sign("Lò Rèn Nguội", "Lò rèn nguội: trên đe còn một cây chùy chưa nguội hẳn ý chí người thợ.", x - 3, y + 4)
    m.poi("landmark", "Lò Rèn Nguội", x, y)
    m.thing("Bảng thợ", "board", 306, 114, 24, 28, foot=(20, 8))
    m.sign("Bảng chỉ dẫn", "Phường Thiên Công: đi về tây là vào sâu.\n"
           "Qua tường thành đổ là Trung Vực, qua khe xỉ nguội là Thâm Xứ.", 304, 114)


def landmarks(m: DaiDiaDo) -> None:
    # Giếng Thợ Cả, the heart of the old quarter
    m.thing("Giếng", "well", 264, 57, 24, 24, foot=(20, 12))
    for i, (tx, ty) in enumerate(((257, 55), (267, 55), (257, 63), (267, 63))):
        m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i + 4)
    m.thing("Bảng thợ", "board", 259, 57, 24, 28, foot=(20, 8))
    m.sign("Giếng Thợ Cả", "Giếng Thợ Cả: thợ cả múc nước tôi thép, rồi dạy học trò viết ra từng bước.", 266, 61)
    m.poi("landmark", "Giếng Thợ Cả", 264, 58)
    # Chợ Phiên Bỏ Hoang: rows of stalls
    for i, (tx, ty) in enumerate(((255, 175), (260, 175), (266, 175), (271, 175),
                                  (255, 184), (266, 184), (271, 184))):
        m.thing("Sạp bỏ hoang", "stall", tx, ty, 40, 32, foot=(36, 12), variant=i)
    m.sign("Chợ Phiên", "Chợ phiên của thợ: món nào cũng có giá, chỉ là không còn ai bán.", 258, 186)
    m.poi("landmark", "Chợ Phiên Bỏ Hoang", 262, 180)
    # Lò Rèn Ba Miệng beside Hồ Tôi Thép
    for i, tx in enumerate((145, 150, 155)):
        m.thing("Lò rèn", "furnace", tx, 29, 24, 28, foot=(20, 12), variant=i)
        m.thing("Đe rèn", "anvil", tx, 33, 24, 20, foot=(20, 8), variant=i)
    m.sign("Lò Rèn Ba Miệng", "Ba miệng lò, ba công đoạn: nung, rèn, tôi. Thiếu một bước là hỏng cả mẻ.", 142, 34)
    m.poi("landmark", "Lò Rèn Ba Miệng", 150, 30)
    m.poi("landmark", "Hồ Tôi Thép", 178, 22)
    # Xưởng Bánh Răng: gears inside, the mechanism gate in the south wall
    x0, y0, x1, y1 = XUONG
    m.thing("Cơ Quan Cửa", "gate", 149, y1, 32, 32)
    for i, (tx, ty) in enumerate(((x0 + 3, y0 + 3), (x1 - 3, y0 + 3), (x0 + 3, y1 - 3), (x1 - 3, y1 - 3),
                                  (x0 + 8, y0 + 7), (x1 - 7, y0 + 7))):
        m.thing("Bánh xe gỗ", "log" if i % 2 else "stump", tx, ty, 24, 16, foot=(18, 8), variant=i)
    m.thing("Đe rèn", "anvil", x1 - 4, y0 + 10, 24, 20, foot=(20, 8))
    m.sign("Xưởng Bánh Răng", "Xưởng Bánh Răng: cơ quan cửa chỉ mở cho người hiểu từng bánh răng ăn khớp ra sao.",
           146, y1 + 2)
    m.poi("landmark", "Xưởng Bánh Răng", 149, 97)
    # Sân Đầu Đàn: the leader's paved yard
    sx, sy = SAN
    for y in range(sy - 4, sy + 5):
        for x in range(sx - 6, sx + 7):
            m.setg(x, y, "plaza0" if (x + y) % 3 else "plaza1")
    for i, (dx, dy) in enumerate(((-6, -4), (6, -4), (-6, 4), (6, 4))):
        m.thing("Đèn", "lantern", sx + dx, sy + dy, 8, 24, foot=(4, 4), variant=i + 8)
    m.poi("landmark", "Sân Đầu Đàn", sx, sy)
    # Kho Phế Liệu: heaps of gears inside the wall
    x0, y0, x1, y1 = KHO
    for i, (tx, ty) in enumerate(((x0 + 2, y0 + 3), (x0 + 6, y0 + 4), (x1 - 3, y0 + 3), (x1 - 6, y1 - 3),
                                  (x0 + 9, y1 - 2), (x1 - 2, y1 - 5))):
        m.thing("Đống bánh răng", "boulder" if i % 3 == 0 else "log", tx, ty, *((32, 24, (26, 10)) if i % 3 == 0
                                                                              else (24, 16, (18, 8))), variant=i)
    for i, (tx, ty) in enumerate(((x0 + 4, y1 - 4), (x0 + 12, y0 + 6), (x1 - 8, y0 + 8))):
        m.thing("Bánh xe gỗ", "stump", tx, ty, 24, 16, foot=(18, 8), variant=i + 20)
    m.sign("Kho Phế Liệu", "Kho phế liệu: giữa đống bánh răng có thứ gì đó lấp lánh.", 128, y0 - 2)
    m.poi("landmark", "Kho Phế Liệu", 130, 212)
    # Đình Tổ Nghề among the ruins
    m.building("Đình Tổ Nghề", "pavilion", 50, 37, 64, 64, 22)
    for i, (tx, ty) in enumerate(((46, 36), (58, 36), (46, 44), (58, 44), (52, 35))):
        m.thing("Đá đổ", "boulder" if i % 2 else "rock", tx, ty, *((32, 24, (26, 10)) if i % 2 else (16, 12, (12, 8))),
                variant=i)
    m.sign("Đình Tổ Nghề", "Đình thờ tổ nghề đã đổ: chữ khắc trên bia chỉ còn câu 'chia nhỏ việc lớn'.", 49, 45)
    m.poi("landmark", "Đình Tổ Nghề", 52, 40)
    # the great foundry: the five-mouthed furnace against the south wall
    x0, y0, x1, y1 = LO_DUC
    for i, tx in enumerate((38, 42, 46, 50, 54)):
        m.thing("Lò Lớn", "furnace", tx, y1 - 3, 24, 28, foot=(20, 12), variant=i)
    for i, (tx, ty) in enumerate(((x0 + 3, y0 + 4), (x1 - 3, y0 + 4), (x0 + 3, y1 - 4), (x1 - 3, y1 - 4))):
        m.thing("Lôi tinh nung", "crystal", tx, ty, 24, 32, foot=(14, 8), variant=i)
    for i, tx in enumerate((38, 54)):
        m.thing("Đe rèn", "anvil", tx, y0 + 7, 24, 20, foot=(20, 8), variant=i + 3)
    for i, (tx, ty) in enumerate(((37, 192), (41, 192), (51, 192), (55, 192), (37, 201), (41, 201), (55, 201))):
        m.thing("Khuôn đúc", "boulder" if i % 2 else "rock", tx, ty,
                *((32, 24, (26, 10)) if i % 2 else (16, 12, (12, 8))), variant=i + 30)
    for i, (tx, ty) in enumerate(((43, 190), (49, 190), (43, 194), (49, 194))):
        m.thing("Đèn lò", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i + 20)
    m.sign("Rãnh đúc", "Rãnh đúc còn ấm: kim loại chảy theo đúng đường đã vạch sẵn, như từng dòng lệnh.", 44, 198)
    for i, tx in enumerate((43, 49)):
        m.thing("Đèn", "lantern", tx, y0 - 2, 8, 24, foot=(4, 4), variant=i + 12)
    m.sign("Lò Lớn", "Lò Lớn: chỉ cháy lại khi đủ công lực", 42, y0 - 3)
    m.poi("landmark", "Đại Lò Đúc", 46, 196)
    m.poi("beast", "Lò Lớn · Tiểu Long", *TIEU_LONG)


def furnish(m: DaiDiaDo, grids: dict) -> None:
    """Every block between the streets gets its houses and things, fewer and more broken the
    deeper the khu."""
    plans = {
        "tcp_pho_tho_cu": [(0.9, "house", "Xưởng"), (0.4, "house", "Xưởng"), (0.5, "lantern", "Đèn"),
                           (0.4, "x_board", "Bảng thợ"), (0.3, "log", "Khúc gỗ"), (0.25, "x_anvil", "Đe nguội")],
        "tcp_cho_tho": [(0.7, "stall", "Sạp bỏ hoang"), (0.6, "stall", "Sạp bỏ hoang"), (0.5, "house", "Nhà buôn"),
                        (0.5, "lantern", "Đèn"), (0.3, "x_mat", "Chiếu")],
        "tcp_xom_lo_ren": [(0.6, "house", "Lò rèn"), (0.7, "x_anvil", "Đe rèn"), (0.5, "x_anvil", "Đe rèn"),
                           (0.4, "rock", "Xỉ sắt"), (0.4, "lantern", "Đèn")],
        "tcp_bai_banh_rang": [(0.5, "house", "Xưởng"), (0.7, "stump", "Bánh xe gỗ"), (0.6, "log", "Trục gỗ"),
                              (0.5, "stump", "Bánh xe gỗ"), (0.3, "x_board", "Bảng thợ")],
        "tcp_kho_phe_lieu": [(0.35, "house", "Kho"), (0.6, "boulder", "Đống phế liệu"), (0.6, "log", "Trục gỗ"),
                             (0.5, "rock", "Sắt vụn"), (0.3, "stump", "Bánh xe gỗ")],
        "tcp_pho_do_nat": [(0.22, "house", "Xưởng đổ"), (0.6, "boulder", "Tường đổ"), (0.5, "rock", "Gạch vỡ"),
                           (0.4, "dead_tree", "Cây khô"), (0.3, "log", "Xà gãy")],
        "tcp_dai_lo_duc": [(0.15, "house", "Xưởng đúc"), (0.6, "boulder", "Khuôn đúc vỡ"), (0.5, "rock", "Xỉ"),
                           (0.3, "crystal", "Tinh thạch nung"), (0.3, "dead_tree", "Cây cháy")],
    }
    for kid, (xs, ys) in grids.items():
        k = X.khu_of(m, kid)
        ri = m.bands_khu.index(k)
        for r in X.blocks(k, xs, ys):
            if kid == "tcp_bai_banh_rang" and m.rng.random() < 0.4:
                plank_yard(m, r, ri)
            X.fill_block(m, r, ri, plans[kid])


def plank_yard(m: DaiDiaDo, r: tuple, ri: int) -> None:
    """A gear yard: a plank floor filling most of a block, gears and axles lying on it."""
    x0, y0, x1, y1 = r
    tiles = [(x, y) for y in range(y0 + 1, y1) for x in range(x0 + 1, x1)
             if X.clear_box(m, x, y, x, y, ri)]
    for (x, y) in tiles:
        m.setg(x, y, "wood0")
    for i in range(3):
        tx, ty = m.rng.randint(x0 + 2, x1 - 2), m.rng.randint(y0 + 2, y1 - 2)
        X.try_thing(m, "stump" if i % 2 == 0 else "log", tx, ty, ri, "Bánh xe gỗ" if i % 2 == 0 else "Trục gỗ")


# ------------------------------------------------------------------ the monsters
def monsters(m: DaiDiaDo) -> None:
    """Band 1: Cơ Quan Nhân and Cơ Quan Thú (their low nodes); band 2: the same with their middle
    nodes and a few elites; band 3: only the elites (the land has no normal creature of tầng 7-9),
    one per area, a handful per khu. Lò Linh keeps to the forges, the leader to its yard."""
    m.monsters("tcp_pho_tho_cu", [("co_quan_nhan", 3), ("co_quan_thu", 1)], tiles_per=200)
    m.monsters("tcp_cho_tho", [("co_quan_nhan", 2), ("co_quan_thu", 2)], tiles_per=200)
    sx, sy = SAN
    m.monster_area("tcp_bai_banh_rang", "co_quan_nhan_dau_dan", (sx - 5, sy - 3, sx + 5, sy + 3), 1,
                   name="co_quan_dau_dan")
    m.monsters("tcp_xom_lo_ren", [("co_quan_nhan", 2), ("co_quan_thu", 2)], [("lo_linh", 2), ("co_quan_nhan_dau_dan", 1)],
               tiles_per=200)
    m.monsters("tcp_bai_banh_rang", [("co_quan_thu", 2), ("co_quan_nhan", 2)], [("co_quan_nhan_dau_dan", 1), ("lo_linh", 1)],
               tiles_per=200, skip=lambda r: abs((r[0] + r[2]) / 2 - sx) < 14 and abs((r[1] + r[3]) / 2 - sy) < 11)
    m.monsters("tcp_kho_phe_lieu", [("co_quan_thu", 3), ("co_quan_nhan", 1)], [("lo_linh", 1), ("co_quan_nhan_dau_dan", 1)],
               tiles_per=200)
    x0, y0, x1, y1 = LO_DUC
    m.monster_area("tcp_dai_lo_duc", "lo_linh", (x0 + 4, y0 + 3, x1 - 4, y1 - 6), 1, name="lo_linh_dai_lo")
    m.monsters("tcp_pho_do_nat", [("co_quan_nhan_dau_dan", 1), ("lo_linh", 1)], cell=(16, 14), tiles_per=1e9,
               max_areas=7)
    m.monsters("tcp_dai_lo_duc", [("lo_linh", 1), ("co_quan_nhan_dau_dan", 1)], cell=(16, 14), tiles_per=1e9,
               max_areas=6, skip=lambda r: r[2] >= x0 - 2 and r[0] <= x1 + 2 and r[3] >= y0 - 5 and r[1] <= y1 + 2)
