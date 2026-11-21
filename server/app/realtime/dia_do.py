"""Đại Địa Đồ: the sub-areas ("khu") of the giant lands.

A land is one zone (zones.json) with one Tiled map. On the giant maps a land is cut into khu,
each made for a band of tu vi (the stages of Đạo Thụ its monsters stand for):

    band 1  Ngoại Vi    Luyện Khí tầng 1-3
    band 2  Trung Vực   Luyện Khí tầng 4-6
    band 3  Thâm Xứ     Luyện Khí tầng 7-9

**The contract of a map** (objects layer of the .tmj; every property is a string):

* an object of type ``khu``: its rectangle is the khu (pixels). Properties: ``khu`` (the id,
  unique in the whole world, e.g. ``kts_ngoai_vi``), ``name_vi``, ``band`` ("1".."3", "0" for
  a safe place with no monsters), ``realm`` (a realm of tree.json), ``stage_min``, ``stage_max``,
  ``anchor_x``, ``anchor_y`` (pixels: a walkable point inside it that can be reached on foot
  from the map's ``spawn`` - where "Chỉ Đường" leads), and optionally ``desc_vi``, ``safe``.
  Where two khu overlap, the one listed first in the map wins.
* a ``monster_area`` of a khu names it: ``khu`` (the id) and ``band``.
* an object of type ``poi`` is a named place the big map lists: ``poi`` (gate, camp, bi_canh,
  npc, beast, boss, landmark), ``name_vi``; its rectangle's centre is where it is.

A map with no khu (the old small maps, the hub, the abode) simply has an empty list here, and
everything that reads this module must cope with that.

The readers below are the frozen part of the contract (the navigation reads them); the band
table, the stat multipliers and the loot caps of a band are added to this module by the world
builder.
"""
from __future__ import annotations

from functools import lru_cache

from . import maps

BAND_NAMES_VI = {0: "An Toàn", 1: "Ngoại Vi", 2: "Trung Vực", 3: "Thâm Xứ"}


def _int(v, default: int = 0) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def _zone_map(zone_id: str):
    from .world import zone_defs
    z = zone_defs().get(zone_id or "")
    if not z or not z.get("map") or z.get("kind") == "instance":
        return None
    try:
        return maps.load(z["map"])
    except FileNotFoundError:
        return None


@lru_cache(maxsize=None)
def khu_list(zone_id: str) -> tuple[dict, ...]:
    """The khu of a zone in map order; () for a zone that has none. Each one:
    {id, zone, land, name_vi, band, band_vi, realm, stage_min, stage_max, rect: [x, y, w, h],
    anchor: [x, y], safe, desc_vi} (pixels)."""
    from . import lands
    zmap = _zone_map(zone_id)
    if zmap is None:
        return ()
    out = []
    for a in zmap.khu:
        p = a.props
        band = _int(p.get("band"))
        out.append({
            "id": a.name, "zone": zone_id, "land": lands.zone_land_id(zone_id),
            "name_vi": p.get("name_vi") or a.name, "band": band,
            "band_vi": BAND_NAMES_VI.get(band, ""), "realm": p.get("realm") or "luyen_khi",
            "stage_min": _int(p.get("stage_min")), "stage_max": _int(p.get("stage_max")),
            "rect": [int(a.x), int(a.y), int(a.w), int(a.h)],
            "anchor": [_int(p.get("anchor_x"), int(a.x + a.w / 2)), _int(p.get("anchor_y"), int(a.y + a.h / 2))],
            "safe": str(p.get("safe", "")).lower() == "true" or band == 0,
            "desc_vi": p.get("desc_vi", ""),
        })
    return tuple(out)


def khu_at(zone_id: str, x: float, y: float) -> dict | None:
    """The khu a point of a zone lies in (the first one in map order), or None."""
    for k in khu_list(zone_id):
        rx, ry, rw, rh = k["rect"]
        if rx <= x <= rx + rw and ry <= y <= ry + rh:
            return k
    return None


def khu(khu_id: str) -> dict | None:
    """A khu by its id, wherever it is."""
    return next((k for k in all_khu() if k["id"] == khu_id), None)


def all_khu() -> list[dict]:
    """Every khu of every zone of the world, zone by zone."""
    from .world import zone_defs
    return [k for zid in zone_defs() for k in khu_list(zid)]


def poi_list(zone_id: str) -> list[dict]:
    """The named places of a zone: {name_vi, poi, x, y} (pixels, the centre)."""
    zmap = _zone_map(zone_id)
    if zmap is None:
        return []
    return [{"name_vi": a.props.get("name_vi") or a.name, "poi": a.props.get("poi", "landmark"),
             "x": int(a.x + a.w / 2), "y": int(a.y + a.h / 2)} for a in zmap.pois]
