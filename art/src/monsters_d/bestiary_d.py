"""MONSTERS_D: id -> (name_vi, frame size, builder). Builders live one per file."""
from __future__ import annotations


def _hoa_yeu():
    from hoa_yeu import build
    return build()


def _bach_vien():
    from bach_vien import build
    return build()


def _co_quan_thu():
    from co_quan_thu import build
    return build()


def _lo_linh():
    from lo_linh import build
    return build()


def _thao_nhan():
    from thao_nhan import build
    return build()


def _xich_diem_ma():
    from xich_diem_ma import build
    return build()


BUILD = {
    "hoa_yeu": ("Hoa Yêu", 48, _hoa_yeu),
    "bach_vien": ("Bạch Viên", 64, _bach_vien),
    "co_quan_thu": ("Cơ Quan Thú", 48, _co_quan_thu),
    "lo_linh": ("Lò Linh", 64, _lo_linh),
    "thao_nhan": ("Thảo Nhân", 48, _thao_nhan),
    "xich_diem_ma": ("Xích Diễm Mã", 64, _xich_diem_ma),
}
