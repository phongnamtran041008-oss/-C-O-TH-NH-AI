"""The MONSTERS_C table: id -> (name_vi, frame size, builder, extra render options).

`ground` lists clips the kit QC treats as lying on the ground (render.ground_clips): a long,
low creature seen from 35 degrees draws its snout below the pivot when it faces the camera,
which is the true projection of its footprint, not a sink (see README, "My choices").
"""
from __future__ import annotations


def _table():
    from pangolin import build_thiet_giap_thu
    table = {
        "thiet_giap_thu": ("Thiết Giáp Thú", 48, build_thiet_giap_thu, {}),
    }
    for mod, fn, mid, name, size, opts in (
        ("ghost_swordsman", "build_vong_hon_kiem_si", "vong_hon_kiem_si", "Vong Hồn Kiếm Sĩ", 64, {}),
        ("butterfly", "build_van_diep", "van_diep", "Vân Điệp", 48, {}),
        ("hawk", "build_loi_ung", "loi_ung", "Lôi Ưng", 64, {}),
        ("lantern", "build_u_minh_dang", "u_minh_dang", "U Minh Đăng", 48, {}),
        ("crocodile", "build_huyet_ngac", "huyet_ngac", "Huyết Ngạc", 64,
         {"ground": ["idle", "walk", "windup", "attack", "hit", "die"]}),
        ("ball_lightning", "build_loi_linh", "loi_linh", "Lôi Linh", 48, {}),
    ):
        try:
            m = __import__(mod)
        except ModuleNotFoundError:
            continue
        table[mid] = (name, size, getattr(m, fn), opts)
    return table


IDS = ["thiet_giap_thu", "vong_hon_kiem_si", "van_diep", "loi_ung", "u_minh_dang",
       "huyet_ngac", "loi_linh"]
