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

The readers below are the frozen part of the contract (the navigation reads them).

**The bands in the game** (data/math/dia_do.json, below the readers): a monster takes the band
of the ``monster_area`` that spawns it (its ``band`` property, and ``realm``, Luyện Khí when
absent); a monster of a map without bands has band 0 and behaves exactly as before.

* its fighting numbers (hp, atk, def) and what it gives (xp, stones) are multiplied by the
  band's ``mult`` - gently, since the questions already follow the player's own level
  (realtime/ai.py ``Monster.info`` and the kill's reward in realtime/combat.py);
* its drops stay within the band's ``loot_cap`` (systems/loot.py ``band_within`` and
  ``band_allows``), never above the zone's own cap (``source_caps``);
* ``full()`` sends the band as ``"kv"`` (docs/PROTOCOL.md);
* a land creature prefers to ask, among its own ``nodes``, those whose stage lies in the band
  (realtime/lands.py ``LandAsker``); a quái lỗi sai keeps its own micro-skill.
"""
from __future__ import annotations

import json
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


# ------------------------------------------------------------------ the bands (world builder)
MULT_KEYS = ("hp", "atk", "def", "xp", "stones")
DEFAULT_REALM = "luyen_khi"


@lru_cache(maxsize=1)
def data() -> dict:
    from ..config import DATA_DIR
    return json.loads((DATA_DIR / "math" / "dia_do.json").read_text("utf-8"))


def band_def(band: int, realm: str | None = None) -> dict | None:
    """The row of a band (1..3) in a realm, or None (band 0, an unknown band or realm)."""
    if not band:
        return None
    return (data().get("realms", {}).get(realm or DEFAULT_REALM) or {}).get(str(int(band)))


def band_range(band: int, realm: str | None = None) -> tuple[int, int] | None:
    """(stage_min, stage_max) of a band, or None."""
    b = band_def(band, realm)
    return (int(b["stage_min"]), int(b["stage_max"])) if b else None


def mult(band: int, realm: str | None, key: str) -> float:
    """The band's multiplier for hp, atk, def, xp or stones (1.0 outside any band)."""
    b = band_def(band, realm)
    return float((b or {}).get("mult", {}).get(key, 1.0))


def loot_cap(band: int, realm: str | None = None) -> str | None:
    """The loot cap of a band (a tier of loot_tiers.json, 'luyen_khi:3'), or None."""
    b = band_def(band, realm)
    return b.get("loot_cap") if b else None


def area_band(props: dict) -> tuple[int, str]:
    """(band, realm) of a monster_area from its properties; (0, Luyện Khí) when it has none."""
    return max(0, _int(props.get("band"))), props.get("realm") or DEFAULT_REALM


def scaled_info(info: dict, band: int, realm: str | None = None) -> dict:
    """A monster's numbers in a band: hp, atk and def, xp and the stones range multiplied by the
    band's `mult` (the dict itself when nothing changes)."""
    b = band_def(band, realm)
    if not b:
        return info
    out = dict(info)
    for key in ("hp", "atk", "def"):
        if isinstance(info.get(key), (int, float)):
            out[key] = round(info[key] * mult(band, realm, key), 2)
    if isinstance(info.get("xp"), (int, float)):
        out["xp"] = int(round(info["xp"] * mult(band, realm, "xp")))
    st = info.get("stones")
    if isinstance(st, (list, tuple)) and len(st) == 2:
        k = mult(band, realm, "stones")
        out["stones"] = [int(round(st[0] * k)), int(round(st[1] * k))]
    return out


def distribution() -> dict:
    """The distribution rules the map generator and tools/check_maps.py keep."""
    return dict(data().get("distribution", {}))


def validate(raw: dict | None = None) -> list[str]:
    """Problems of data/math/dia_do.json (empty = sound): every band of a realm has a name, a
    stage range inside the realm that rises with the band, gentle multipliers that never fall
    with the band, and a loot cap of loot_tiers.json that rises with it."""
    from ..systems import loot
    d = raw if raw is not None else data()
    out: list[str] = []
    realms = d.get("realms")
    if not isinstance(realms, dict) or not realms:
        return ["realms: missing"]
    for realm, bands in realms.items():
        prev = None
        for key in sorted(bands, key=lambda k: _int(k)):
            b = bands[key]
            where = f"realms.{realm}.{key}"
            if _int(key) < 1:
                out.append(f"{where}: bands are numbered from 1 (0 is a safe place, it has no row)")
            if not b.get("name_vi"):
                out.append(f"{where}: needs name_vi")
            lo, hi = _int(b.get("stage_min"), -1), _int(b.get("stage_max"), -1)
            if not 0 <= lo <= hi:
                out.append(f"{where}: stage_min..stage_max must be a range of stages")
            m = b.get("mult") or {}
            for k in MULT_KEYS:
                v = m.get(k)
                if not isinstance(v, (int, float)) or not 0.5 <= v <= 2.0:
                    out.append(f"{where}: mult.{k} must be a gentle number in 0.5..2")
            try:
                cap = loot.parse(b.get("loot_cap"))
            except ValueError as e:
                out.append(f"{where}: loot_cap: {e}")
                cap = None
            if prev is not None:
                plo, phi, pm, pcap = prev
                if lo <= phi:
                    out.append(f"{where}: its stages must come after those of the band before it")
                for k in MULT_KEYS:
                    if isinstance(m.get(k), (int, float)) and isinstance(pm.get(k), (int, float)) and m[k] < pm[k]:
                        out.append(f"{where}: mult.{k} is lower than in the band before it")
                if cap is not None and pcap is not None and cap < pcap:
                    out.append(f"{where}: loot_cap is lower than in the band before it")
            prev = (lo, hi, m, cap)
    dist = d.get("distribution") or {}
    for k in ("min_kinds_per_khu", "clearance_tiles", "max_monsters_per_land", "max_elites_per_khu"):
        if not isinstance(dist.get(k), int) or dist[k] <= 0:
            out.append(f"distribution.{k} must be a positive whole number")
    tpm = dist.get("tiles_per_monster")
    if not (isinstance(tpm, list) and len(tpm) == 2 and 0 < tpm[0] <= tpm[1]):
        out.append("distribution.tiles_per_monster must be [low, high]")
    return out
