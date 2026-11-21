"""Kiếm Trủng Sơn (zone loan_so_coc, land kiem_trung_son, branch Đại Số Tuyến Tính): the
sword-grave mountain, a giant land of Đại Địa Đồ (320 x 240 tiles).

The mountain rises from the gate in the south to the peak in the north-east, in three tiers
cut by natural walls: a ridge of boulders between the foothills (Ngoại Vi, tầng 1-3) and the
slopes (Trung Vực, tầng 4-6), a chasm of ink between the slopes and the summit (Thâm Xứ, tầng
7-9). A rest camp waits after each wall. The old valley where the mistakes walk, Loạn Số Cốc,
is the eastern foothill: its three stretches are the three floors of Đại Số Tuyến Tính, floor 1
nearest the gate camp. Everything the small map had is here: Lò Toán, the Đạo Sĩ, the stone
tablet at the gate, the cave behind the falls, the field of broken swords and the peak beyond
the chasm (Đạp Kiếm Lướt), where Hỏa Tước nests.
"""
from __future__ import annotations

from ..builder import T
from ..giant import DaiDiaDo, Theme

ZONE = "loan_so_coc"
SIZE = (320, 240)

# the places other data points at (world_plan.json weapons_placed / beasts `pos`): tiles
BIA_KIEM = (156, 230)          # the tablet just inside the gate; kiem_1_ha lies in front of it
KIEM_1_HA = (156, 231)
CAVE = (30, 98)                # kiem_1_trung: in the cave behind Thác Bạc
FIELD = (58, 26)               # kiem_1_thuong: amid the broken swords
PEAK = (268, 2)                # kiem_2_ha: on the peak beyond the chasm of ink
HOA_TUOC = (PEAK[0] + 1, PEAK[1] + 1)
BACH_HO_CON = (291, 104)       # on the eastern slope


def g_suon_kim(P, D, r):
    if P > 0.62:
        return "stone0"
    if P < 0.24:
        return "dark_grass0" if r < 0.7 else "grass1"
    return "dirt0" if D > 0.48 else "grass1"


def build() -> dict:
    W, H = SIZE
    m = DaiDiaDo(ZONE, "Kiếm Trủng Sơn", W, H, "kiem_trung_son_dai_dia_do")
    m.themes["suon_kim"] = Theme("suon_kim", g_suon_kim,
                                 [("rock", 3), ("crystal", 2), ("tall_grass", 2), ("bush", 1)],
                                 [("pine", 4), ("boulder", 3), ("crystal", 1)], 0.038, 0.15, 15.0, 0.56)

    # ---- 1. the khu (band 1 in the south, band 3 at the summit)
    m.khu("kts_chan_nui", "Chân Núi Kiếm Gãy", 1, (0, 160, 159, 239), "chan_nui", (72, 196),
          "Sườn thấp phía tây cổng núi: cỏ, thông và những thanh kiếm gãy cắm lẻ loi. Kiếm Linh lang thang.")
    m.khu("kts_loan_so_coc", "Loạn Số Cốc", 1, (160, 160, 319, 239), "dat_hoang", (214, 198),
          "Thung lũng nơi chính các lỗi sai đi lại: lỗi tầng 1 gần trại cổng, tầng 3 ở cuối cốc.")
    m.khu("kts_thach_lam", "Thạch Lâm Thác Bạc", 2, (0, 80, 109, 159), "thach_lam", (54, 122),
          "Rừng đá phía tây, thác bạc đổ xuống trước một hang đá. Thạch Khôi canh hang.")
    m.khu("kts_co_kiem_dao", "Cổ Kiếm Đạo", 2, (110, 80, 209, 159), "rung_thong", (160, 112),
          "Đường thông cổ dẫn lên Miếu Kiếm Cổ, nơi kiếm khách xưa dừng chân trước khi lên đỉnh.")
    m.khu("kts_suon_dong", "Sườn Đông Gió Kim", 2, (210, 80, 319, 159), "suon_kim", (264, 122),
          "Sườn đông lộng gió kim khí, đá và tinh thạch lởm chởm; Bạch Hổ Con lang thang trên mỏm cao.")
    m.khu("kts_bai_kiem", "Bãi Kiếm Gãy", 3, (0, 0, 109, 79), "bai_kiem", (56, 42),
          "Cả một bãi mộ kiếm: nơi Ma Trận Thú canh thanh kiếm còn nguyên giữa ngàn thanh gãy.")
    m.khu("kts_kiem_trung", "Kiếm Trủng", 3, (110, 0, 209, 79), "rung_toi", (160, 38),
          "Rừng mực quanh mộ kiếm lớn nhất núi; Vong Hồn Kiếm Sĩ không chịu rời chủ cũ.")
    m.khu("kts_dinh", "Đỉnh Vạn Kiếm", 3, (210, 0, 319, 79), "dinh_nui", (254, 40),
          "Đỉnh núi trơ đá, vực mực vây quanh chóp cao nhất: phải Đạp Kiếm Lướt mới tới tổ Hỏa Tước.")

    # ---- 2. the ground, then the camps on it
    m.paint(warp=7.0, scale=26.0)
    m.camp("kts_trai_cong", "Trại Cổng Núi", (159, 222), r=8,
           desc_vi="Trại ngay trong cổng núi: Lò Toán, Đạo Sĩ luyện kiếm và bia kiếm. Không có quái.",
           label_vi="Trại Cổng Núi · Lò Toán")
    m.camp("kts_trai_luyen_kiem", "Trại Luyện Kiếm", (160, 148), r=6,
           desc_vi="Trại nghỉ sau đèo đá, cửa vào Trung Vực.", label_vi="Trại Luyện Kiếm · cửa Trung Vực")
    m.camp("kts_tram_may", "Trạm Mây Đỉnh", (160, 70), r=6,
           desc_vi="Trạm nghỉ cuối cùng bên kia vực mực, cửa vào Thâm Xứ.", label_vi="Trạm Mây Đỉnh · cửa Thâm Xứ")
    m.clear_zones.append((154, 226, 165, 239))          # the gate and the spawn

    # ---- 3. the large features
    falls_and_cave(m)
    peak_and_chasm(m)
    m.lake(36, 212, 9, 6)                                # Đầm Kiếm Rỉ, in the foothills
    m.lake(290, 136, 6, 4)                               # a tarn on the eastern slope
    m.chasm(m.blob(150, 52, 5, 3, salt=41))              # an ink sink in Kiếm Trủng
    keep_landmarks(m)

    # ---- 4. the walls between the tiers
    chasm = "chasm"
    cliff = "cliff"
    m.barriers({
        ("kts_chan_nui", "kts_thach_lam"): cliff, ("kts_chan_nui", "kts_co_kiem_dao"): cliff,
        ("kts_loan_so_coc", "kts_co_kiem_dao"): cliff, ("kts_loan_so_coc", "kts_suon_dong"): cliff,
        ("kts_chan_nui", "kts_loan_so_coc"): "trees",
        ("kts_thach_lam", "kts_co_kiem_dao"): "water", ("kts_co_kiem_dao", "kts_suon_dong"): "pines",
        ("kts_thach_lam", "kts_bai_kiem"): chasm, ("kts_co_kiem_dao", "kts_kiem_trung"): chasm,
        ("kts_suon_dong", "kts_dinh"): chasm, ("kts_thach_lam", "kts_kiem_trung"): chasm,
        ("kts_co_kiem_dao", "kts_bai_kiem"): chasm, ("kts_co_kiem_dao", "kts_dinh"): chasm,
        ("kts_suon_dong", "kts_kiem_trung"): chasm,
        ("kts_bai_kiem", "kts_kiem_trung"): cliff, ("kts_kiem_trung", "kts_dinh"): chasm,
    })

    # ---- 5. the roads
    m.node("gate", (159, 234), "Cổng Núi · về Trúc Lâm Thôn")
    m.node("n_chan_nui", (72, 196), "Chân Núi Kiếm Gãy · Ngoại Vi, tầng 1-3")
    m.node("n_loan", (214, 198), "Loạn Số Cốc · lỗi sai tầng 1")
    m.node("n_loan_t2", (252, 200), "Loạn Số Cốc · lỗi sai tầng 2")
    m.node("n_loan_t3", (290, 198), "Cuối Cốc · lỗi sai tầng 3")
    m.node("n_thach_lam", (54, 122), "Thạch Lâm Thác Bạc · Trung Vực, tầng 4-6")
    m.node("n_thac", (38, 99), "Thác Bạc", sign=False)
    m.node("n_co_kiem", (160, 112), "Miếu Kiếm Cổ · Trung Vực, tầng 4-6")
    m.node("n_suon_dong", (264, 122), "Sườn Đông Gió Kim · Trung Vực, tầng 4-6")
    m.node("n_ho_gam", (288, 106), "Mỏm Hổ Gầm", sign=False)
    m.node("n_bai_kiem", (56, 42), "Bãi Kiếm Gãy · Thâm Xứ, tầng 7-9")
    m.node("n_field", (FIELD[0], FIELD[1] + 4), "Kiếm còn nguyên", sign=False)
    m.node("n_kiem_trung", (160, 38), "Kiếm Trủng · Thâm Xứ, tầng 7-9")
    m.node("n_dinh", (254, 40), "Đỉnh Vạn Kiếm · Thâm Xứ, tầng 7-9")
    m.node("n_ledge", (PEAK[0], PEAK[1] + 5), "Bờ Vực Mực", sign=False)
    m.network([
        ("gate", "kts_trai_cong", "main"),
        ("kts_trai_cong", "n_chan_nui", "main"),
        ("kts_trai_cong", "n_loan", "main"),
        ("n_loan", "n_loan_t2", "trail"), ("n_loan_t2", "n_loan_t3", "trail"),
        ("kts_trai_cong", "kts_trai_luyen_kiem", "main"),
        ("n_chan_nui", "n_thach_lam", "trail"),
        ("n_loan_t3", "n_suon_dong", "trail"),
        ("kts_trai_luyen_kiem", "n_co_kiem", "main"),
        ("kts_trai_luyen_kiem", "n_thach_lam", "main"),
        ("kts_trai_luyen_kiem", "n_suon_dong", "main"),
        ("n_thach_lam", "n_thac", "trail"),
        ("n_suon_dong", "n_ho_gam", "trail"),
        ("n_co_kiem", "kts_tram_may", "main", True),
        ("n_thach_lam", "n_bai_kiem", "trail", True),
        ("kts_tram_may", "n_kiem_trung", "main"),
        ("kts_tram_may", "n_bai_kiem", "main"),
        ("n_bai_kiem", "n_field", "trail"),
        ("kts_tram_may", "n_dinh", "main", True),
        ("n_dinh", "n_ledge", "trail"),
    ])
    m.carve([(159, y) for y in range(226, H - 1)], "main")      # through the gate

    # ---- 6. the places
    gate_camp(m)
    landmarks(m)
    m.signposts()

    # ---- 8. the monsters
    monsters(m)

    # ---- 9. the props, 10. the rest
    m.dress_barriers()
    m.scatter()
    m.obj("Cổng Nam", "prop", 158 * T, (H - 2) * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", 158 * T, (H - 1) * T - 2, 4 * T, T + 10, target="truc_lam_thon",
          target_spawn="from_loan_so_coc")
    m.poi("gate", "Cổng Núi · về Trúc Lâm Thôn", 159, H - 2)
    m.obj("spawn", "spawn", 159 * T + 8, (H - 5) * T, 1, 1)
    m.obj("from_village", "spawn", 159 * T + 8, (H - 5) * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="ink_tree",
                    gaps={("s", x) for x in range(158, 162)})


# ------------------------------------------------------------------ the features
def falls_and_cave(m: DaiDiaDo) -> None:
    """Thác Bạc: a cliff face, a waterfall down it into a pool, and behind the pool the cave
    (open to the east) where kiem_1_trung lies."""
    cx, cy = CAVE
    m.wall({(x, y) for x in range(cx - 5, cx + 6) for y in range(cy - 4, cy - 1)})     # the rock face
    m.wall({(x, y) for x in (cx - 4, cx - 3) for y in range(cy - 1, cy + 2)})           # its west side
    m.open_tiles({(x, y) for x in range(cx - 2, cx + 4) for y in range(cy - 1, cy + 2)}, "stone0")  # the cave
    m._wet({(x, y) for x in (cx, cx + 1) for y in range(cy - 4, cy - 1)}, "water0", 1, None)      # the falls
    m._wet({(x, y) for x in range(cx - 3, cx + 5) for y in range(cy + 2, cy + 5)}, "water0", 1, "stone0")  # pool
    for x in range(cx - 5, cx + 6, 2):                  # boulders along the top of the face
        if x not in (cx, cx + 1):
            m.thing("Vách đá", "boulder", x, cy - 4, 32, 24, foot=(26, 10), variant=x)
    m.open_tiles({(x, y) for x in range(cx - 7, cx + 8) for y in (cy - 6, cy - 5)} - m_solid(m), "dark_grass0")
    m.keep_rect(cx - 6, cy - 5, cx + 6, cy + 5)


def m_solid(m: DaiDiaDo) -> set:
    return {(x, y) for y in range(m.H) for x in range(m.W) if m.hard[m.i(x, y)]}


def peak_and_chasm(m: DaiDiaDo) -> None:
    """Đỉnh Vạn Kiếm: the peak (3 x 2 tiles of stone) in a ring of ink against the north edge; the
    ledge south of it is where a glide starts. Nobody walks onto the peak."""
    px, py = PEAK
    peak = {(x, y) for x in range(px - 1, px + 2) for y in range(py, py + 2)}
    pit = {(x, y) for x in range(px - 3, px + 4) for y in range(py - 1, py + 4)} - peak
    wider = m.blob(px, py + 1, 9, 4, salt=43) - pit - peak
    wider = {(x, y) for (x, y) in wider if y <= py + 3 and abs(x - px) > 3}
    m.chasm(pit | wider)
    m.open_tiles(peak, "stone0")
    m.open_tiles({(x, py + 4) for x in range(px - 2, px + 3)}, "stone0")    # the ledge
    m.keep_rect(px - 10, py - 1, px + 10, py + 6)


def keep_landmarks(m: DaiDiaDo) -> None:
    fx, fy = FIELD
    m.keep_rect(fx - 6, fy - 4, fx + 6, fy + 3)                # the field of broken swords
    m.keep_rect(152, 22, 168, 34)                              # Kiếm Trủng, the tomb
    m.keep_rect(155, 100, 165, 108)                            # Miếu Kiếm Cổ
    bx, by = BACH_HO_CON
    m.keep_rect(bx - 3, by - 2, bx + 3, by + 2)                # Mỏm Hổ Gầm
    m.keep_rect(30, 184, 46, 196)                              # Nghĩa Trủng Kiếm Gãy


def gate_camp(m: DaiDiaDo) -> None:
    """Lò Toán, the Đạo Sĩ and the tablet of the gate (what stood by the gate of the small map)."""
    # Lò Toán: the furnace that turns what the mistakes drop into equipment (data/math/crafting.json)
    m.building("Lò Toán", "furnace", 154, 216, 24, 28, 14, otype="interact", action="math_craft")
    m.sign("Lò Toán", "Lò Toán", 152, 217)
    # the Đạo Sĩ practising by the furnace is a character rendered out of Blender (client/assets/chars)
    m.obj("Đạo Sĩ Luyện Kiếm", "char", 164 * T, 216 * T, 16, 24, sheet="dao_si_truc_co", facing="down")
    m.sign("Bảng chỉ dẫn", "Loạn Số Cốc ở phía đông: lỗi sai tầng 1 gần trại, tầng 3 cuối cốc.\n"
           "Lên núi: qua đèo đá là Trung Vực, qua vực mực là Thâm Xứ.", 162, 217)
    m.thing("Bia Kiếm", "tablet", *BIA_KIEM, 16, 24, foot=(12, 8))
    m.poi("npc", "Lò Toán", 155, 217)
    m.poi("landmark", "Bia Kiếm", *BIA_KIEM)


def landmarks(m: DaiDiaDo) -> None:
    # the cave behind the falls
    cx, cy = CAVE
    for i, tx in enumerate((cx - 2, cx + 3)):
        m.thing("Đá", "rock", tx, cy - 2, 16, 12, foot=(12, 8), variant=i)
    m.thing("Mây nước", "cloud_puff", cx + 1, cy + 5, 32, 20, variant=2)
    m.sign("Thác Bạc", "Thác Bạc: sau màn nước là một hang đá.", cx + 7, cy + 2)
    m.poi("landmark", "Thác Bạc", cx + 1, cy - 3)
    # the field of broken swords, around the one sword still whole
    fx, fy = FIELD
    for i, (dx, dy) in enumerate(((-5, -1), (-3, 2), (3, 2), (5, -1))):
        m.thing("Đá", "rock", fx + dx, fy + dy, 16, 12, foot=(12, 8), variant=i + 7)
    for dx, dy in ((-2, -1), (2, -1), (0, 2), (-4, -3), (4, -3), (-6, 1), (6, 1)):
        m.thing("Mộ kiếm", "tablet", fx + dx, fy + dy, 16, 24, foot=(12, 8))
    m.poi("landmark", "Bãi Kiếm Gãy", fx, fy)
    # Kiếm Trủng: a ring of sword graves around an old shrine
    import math as _m
    for i in range(14):
        a = i * 2 * _m.pi / 14
        m.thing("Mộ kiếm", "tablet", round(160 + 7 * _m.cos(a)), round(28 + 5 * _m.sin(a)), 16, 24, foot=(12, 8))
    m.thing("Miếu Kiếm Trủng", "shrine", 160, 28, 32, 44, foot=(28, 12))
    for i, (tx, ty) in enumerate(((156, 31), (164, 31))):
        m.thing("Tinh thạch", "crystal", tx, ty, 24, 32, foot=(14, 8), variant=i)
    m.poi("landmark", "Kiếm Trủng", 160, 28)
    # Miếu Kiếm Cổ on the old sword road
    m.thing("Miếu Kiếm Cổ", "shrine", 160, 104, 32, 44, foot=(28, 12))
    for i, tx in enumerate((157, 163)):
        m.thing("Đèn miếu", "lantern", tx, 106, 8, 24, foot=(4, 4), variant=i)
    m.sign("Miếu Kiếm Cổ", "Miếu Kiếm Cổ: kiếm khách xưa thắp hương ở đây trước khi vượt vực mực.", 165, 108)
    m.poi("landmark", "Miếu Kiếm Cổ", 160, 104)
    # the peak, the nest and the ledge; a boulder east of the ledge stands in a glider's way
    px, py = PEAK
    m.thing("Mỏm đá", "boulder", px + 3, py + 4, 32, 24, foot=(26, 10))
    for i, (dx, dy) in enumerate(((-6, 6), (5, 7), (-9, 7))):
        m.thing("Mộ kiếm", "tablet", px + dx, py + dy, 16, 24, foot=(12, 8))
    m.sign("Bờ Vực Mực", "Bên kia vực là Đỉnh Vạn Kiếm. Không có đường bộ: chỉ Đạp Kiếm Lướt mới qua.",
           px - 3, py + 6)
    m.poi("landmark", "Đỉnh Vạn Kiếm", px, py)
    m.poi("beast", "Tổ Hỏa Tước", *HOA_TUOC)
    # Mỏm Hổ Gầm, where Bạch Hổ Con roams
    bx, by = BACH_HO_CON
    for i, (dx, dy) in enumerate(((-3, -1), (3, -1), (0, -2))):
        m.thing("Mỏm đá", "boulder", bx + dx, by + dy, 32, 24, foot=(26, 10), variant=i)
    m.poi("beast", "Mỏm Hổ Gầm · Bạch Hổ Con", bx, by)
    # Nghĩa Trủng Kiếm Gãy, the graves of the foothills
    for i, (tx, ty) in enumerate(((33, 187), (36, 186), (39, 187), (42, 186), (34, 191), (38, 192), (42, 191))):
        m.thing("Mộ kiếm", "tablet", tx, ty, 16, 24, foot=(12, 8))
    m.thing("Đèn mộ", "lantern", 38, 189, 8, 24, foot=(4, 4), variant=5)
    m.poi("landmark", "Nghĩa Trủng Kiếm Gãy", 38, 189)
    m.poi("landmark", "Đầm Kiếm Rỉ", 36, 212)


# ------------------------------------------------------------------ the monsters
def monsters(m: DaiDiaDo) -> None:
    """Band 1: the low stages (normal rank); band 2: the middle creatures with a few elites;
    band 3: the high stages and the elites. The nine quái lỗi sai stay in Loạn Số Cốc, in three
    groups by their floor, floor 1 nearest the gate camp."""
    # Loạn Số Cốc: the mistakes, floor by floor (each group two normal kinds and one elite), in
    # areas of 20 x 15 tiles: a monster chased to the edge of its area stays within its leash
    for floor, x0, a, b, elite in (
            (1, 182, "dstt_phan_tu_ma", "dstt_nghich_hieu_ma", "dstt_anh_trung_ma"),
            (2, 226, "dstt_binh_phuong_ma", "dstt_phan_ao_ma", "dstt_modun_ma"),
            (3, 270, "dstt_chi_so_ma", "dstt_chuyen_vi_ma", "dstt_doi_xung_ma")):
        for n, (kind, col, row, count) in enumerate(((a, 0, 0, 2), (b, 1, 0, 2), (a, 0, 1, 2), (b, 1, 1, 2),
                                                    (a, 0, 2, 1))):
            x, y = x0 + 21 * col, 174 + 16 * row
            m.monster_area("kts_loan_so_coc", kind, (x, y, x + 19, y + 14), count, name=f"t{floor}_{kind[5:-3]}_{n}")
            m.keep_rect(x + 8, y + 6, x + 11, y + 8)          # a clearing in the middle of the area
        m.monster_area("kts_loan_so_coc", elite, (x0 + 25, 208, x0 + 33, 216), 1, name=f"t{floor}_{elite[5:-3]}")
    m.monsters("kts_chan_nui", [("kiem_linh", 3), ("thiet_giap_thu", 1)], tiles_per=210)
    fx, fy = CAVE
    m.monster_area("kts_thach_lam", "thach_khoi", (fx - 8, fy + 6, fx + 12, fy + 16), 2, name="thach_khoi_thac")
    m.monsters("kts_thach_lam", [("thach_khoi", 3), ("thiet_giap_thu", 1)], [("vong_hon_kiem_si", 2)],
               tiles_per=210, skip=lambda r: r[1] <= fy + 17 and r[0] <= fx + 12)
    m.monsters("kts_co_kiem_dao", [("thach_khoi", 2), ("thiet_giap_thu", 2)], [("vong_hon_kiem_si", 2)], tiles_per=210)
    m.monsters("kts_suon_dong", [("thiet_giap_thu", 2), ("thach_khoi", 2)], [("vong_hon_kiem_si", 2)], tiles_per=210)
    gx, gy = FIELD
    m.monster_area("kts_bai_kiem", "ma_tran_thu", (gx - 6, gy - 3, gx + 6, gy + 3), 1, name="ma_tran_bai_kiem")
    m.monsters("kts_bai_kiem", [("thiet_giap_thu", 1)], [("ma_tran_thu", 3), ("vong_hon_kiem_si", 2)],
               tiles_per=220, skip=lambda r: abs((r[0] + r[2]) / 2 - gx) < 14 and abs((r[1] + r[3]) / 2 - gy) < 12)
    m.monsters("kts_kiem_trung", [("thiet_giap_thu", 1)], [("vong_hon_kiem_si", 4), ("ma_tran_thu", 2)], tiles_per=220)
    m.monsters("kts_dinh", [("thiet_giap_thu", 1)], [("ma_tran_thu", 3), ("vong_hon_kiem_si", 3)], tiles_per=220)
