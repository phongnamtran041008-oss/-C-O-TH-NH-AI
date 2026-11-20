"""Every sheet of the fx_chieu batch, grouped by contact sheet (art/preview/fx_chieu_<group>.png).  Plain Python
(no bpy): used by build.py, chieu_proof.py and, inside Blender, by fx_chieu.py."""
GROUPS = {
    "kiem": ["ngu_kiem", "ngu_kiem_xuyen", "van_kiem_troi", "van_kiem_roi", "van_kiem_vong",
             "kiem_vuc", "kiem_vuc_xoay", "pha_me_kiem"],
    "nguyen_to": ["bang_phong", "bang_ket", "loi_xich", "loi_cham", "thien_loi_giang",
                  "hoa_long", "hoa_long_vet", "hoa_cau_lon", "hoa_cau_no"],
    "dat_moc_phong": ["dia_liet", "dia_liet_no", "thanh_dang", "thanh_dang_troi", "hoi_xuan",
                      "phong_nhan", "phong_xoay", "kim_chung", "kim_chung_tru", "kim_chung_vang"],
    "tu_khi": ["tu_khi_kim", "tu_khi_moc", "tu_khi_thuy", "tu_khi_hoa", "tu_khi_tho", "tu_khi_loi"],
}
ALL = [i for g in GROUPS.values() for i in g]
assert len(ALL) == len(set(ALL)) == 33     # the brief says 34; its own list adds up to 33 (23 new + 4 hero + 6 tu_khi)
