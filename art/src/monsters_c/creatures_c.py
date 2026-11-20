"""The MONSTERS_C table: id -> (name_vi, frame size, builder, extra render options).

`ground` lists clips the kit QC treats as lying on the ground (render.ground_clips). Only
Huyết Ngạc uses it: a long, low crocodile seen from 35 degrees draws its snout below the
pivot when it faces the camera (or its tail when it faces away), which is the true
projection of a footprint centred on the monster's position, not a sink. See README,
"My choices".
"""
from __future__ import annotations

IDS = ["thiet_giap_thu", "vong_hon_kiem_si", "van_diep", "loi_ung", "u_minh_dang",
       "huyet_ngac", "loi_linh"]


def _table():
    from ball_lightning import build_loi_linh
    from butterfly import build_van_diep
    from crocodile import build_huyet_ngac
    from ghost_swordsman import build_vong_hon_kiem_si
    from hawk import build_loi_ung
    from lantern import build_u_minh_dang
    from pangolin import build_thiet_giap_thu
    return {
        "thiet_giap_thu": ("Thiết Giáp Thú", 48, build_thiet_giap_thu, {}),
        "vong_hon_kiem_si": ("Vong Hồn Kiếm Sĩ", 64, build_vong_hon_kiem_si, {}),
        "van_diep": ("Vân Điệp", 48, build_van_diep, {}),
        "loi_ung": ("Lôi Ưng", 64, build_loi_ung, {}),
        "u_minh_dang": ("U Minh Đăng", 48, build_u_minh_dang, {}),
        "huyet_ngac": ("Huyết Ngạc", 64, build_huyet_ngac,
                       {"ground": ["idle", "walk", "windup", "attack", "hit", "die"]}),
        "loi_linh": ("Lôi Linh", 48, build_loi_linh, {}),
    }
