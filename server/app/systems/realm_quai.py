"""Quái của bí cảnh: which creatures a run fields (docs/BI_CANH_QUAI.md).

What a run of a bí cảnh fields depends on two things, both read from data (the `quai` block of
each realm of data/realms.json):

* **which bí cảnh it is** (its theme): Mặc Ảnh Động is the ink cave of Nghiên Ma and fields the
  old ink family (data/creatures/monsters.json); Toán Trận Bí Cảnh is a trial array of quái lỗi
  sai, by floor; Khe Nứt Mực is a rift torn open in a wild land and spills the creatures of the
  land and of the khu where it opened (the land's monster areas, realtime/dia_do.py);
* **the tu vi of the party** (its band, 1 Ngoại Vi .. 3 Thâm Xứ, the bands of the giant lands):
  the band of the *weakest* member's place in Đạo Thụ, so nobody is dragged into a run above
  them (`party_band`). A rift answers to the khu it opened in as well: its band is the lower of
  the party's and the khu's.

The band picks the rooms' creatures and counts (a deeper band: more of them, an elite, a
tougher boss through the band multipliers), and the run's monsters carry it like the monsters
of a banded khu (ai.Monster.band): their numbers are scaled by dia_do.scaled_info, their drops
capped by the band (combat.py), they are sent with "kv". The room loot and the chest stay within
the bí cảnh's own cap and the band's (secret_realm.py).

Questions never come from these creatures: every player is asked at their own floor
(math_ask.pick_own, app/systems/math_realm.py).

Everything here is pure: the live run (realtime/realm.py) calls `plan` and `boss` once a room.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path

from ..config import DATA_DIR

BANDS = (1, 2, 3)
THEMES = ("muc", "tran", "land")
LAND = "land"                    # in a rift's rooms: "the creatures of the land", worked out here
# what a boss needs to behave as one (the group shield, its phases) when it borrows another body
BOSS_KEYS = ("hp", "atk", "def", "speed", "aggressive", "aggro_radius", "attack_radius", "idle_seconds",
             "shield_regen", "group_shield", "size", "rank")


# ------------------------------------------------------------------ the data
def realms() -> dict:
    from . import secret_realm
    return secret_realm.realms()


def quai(realm_id: str, raw: dict | None = None) -> dict:
    r = (raw or {}).get("realms", {}).get(realm_id) if raw is not None else realms().get(realm_id)
    return (r or {}).get("quai") or {}


def band_spec(realm_id: str, band: int, raw: dict | None = None) -> dict:
    """The band's row of a realm: {"rooms": [...], "boss": {...}} ({} when missing)."""
    return (quai(realm_id, raw).get("bands") or {}).get(str(int(band))) or {}


@lru_cache(maxsize=1)
def ink_family() -> frozenset:
    """The old Mặc Quái (data/creatures/monsters.json): the ink cave's own creatures."""
    raw = json.loads((DATA_DIR / "creatures" / "monsters.json").read_text("utf-8"))
    return frozenset(k for k in raw if not k.startswith("_"))


def _mons() -> dict:
    from . import catalog
    return catalog.monsters()


# ------------------------------------------------------------------ the band of a party
def band_of_stage(realm: str | None, stage: int) -> int:
    """The band (1..3) of a place in Đạo Thụ: `stage` is the stage reached in `realm`
    (lands.TreePos); the stage being learned is the one above it, and it is that one the bands
    of the giant lands are cut for (navigation.py leads a player to the khu of the stage they
    learn). Beyond Luyện Khí: the deepest band."""
    from ..learning import math_tree
    from ..realtime import dia_do
    t = math_tree.tree()
    realm = realm or dia_do.DEFAULT_REALM
    here, base = t.realm_order.get(realm, 0), t.realm_order.get(dia_do.DEFAULT_REALM, 0)
    if here > base:
        return BANDS[-1]
    if here < base:
        return BANDS[0]
    working = min(int(stage or 0) + 1, t.realm_stages.get(realm, 9))
    for b in BANDS:
        lo, hi = dia_do.band_range(b) or (0, 0)
        if working <= hi:
            return b
    return BANDS[-1]


def band_of_pos(pos) -> int:
    """The band of a lands.TreePos (a newcomer, or None: band 1)."""
    if pos is None:
        return BANDS[0]
    return band_of_stage(pos.realm, pos.stage)


def party_band(positions) -> int:
    """The band of a party: the weakest member's (an empty party: band 1)."""
    bands = [band_of_pos(p) for p in positions]
    return min(bands) if bands else BANDS[0]


def band_vi(band: int) -> str:
    from ..realtime import dia_do
    return dia_do.BAND_NAMES_VI.get(int(band), "")


# ------------------------------------------------------------------ a rift's land
def _zone_areas(zone_id: str) -> list:
    from ..realtime import maps
    from ..realtime.world import zone_defs
    z = zone_defs().get(zone_id or "")
    if not z or not z.get("map"):
        return []
    try:
        return list(maps.load(z["map"]).monster_areas)
    except FileNotFoundError:
        return []


def _split(kinds) -> tuple[list[str], list[str]]:
    """(normals, elites) of some monster kinds, known ones only, never a boss."""
    mons = _mons()
    kinds = list(kinds)
    normals = sorted({k for k in kinds if k in mons and mons[k].get("rank", "normal") == "normal"})
    elites = sorted({k for k in kinds if k in mons and mons[k].get("rank") == "elite"})
    return normals, elites


def land_pool(realm_id: str, zone_id: str | None, x: float | None, y: float | None, band: int,
              raw: dict | None = None) -> dict:
    """What a rift spills: {"band", "khu", "zone", "normals", "elites", "from"}.

    * opened in a khu of band 1..3: the run's band is the lower of the party's (`band`) and the
      khu's; at the khu's own band it spills that khu's creatures, below it those of the land's
      areas of the run's band;
    * elsewhere on a banded land (a camp, between two khu): the land's areas of the party's band;
    * on a land without bands (an old small map): every creature of the zone's areas;
    * a band with no normal creature (a land whose deepest khu hold elites only) takes the
      normals of the nearest band below it; a zone with no creature at all, the realm's
      `fallback` (the ink family: it is a Khe Nứt Mực).
    """
    from ..realtime import dia_do
    band = int(band)
    areas = _zone_areas(zone_id) if zone_id else []
    k = dia_do.khu_at(zone_id, x, y) if zone_id and x is not None and y is not None else None
    banded = [a for a in areas if dia_do.area_band(a.props)[0] > 0]
    khu_id, src = None, []
    if k is not None and int(k.get("band") or 0) > 0:
        band = min(band, int(k["band"]))
        if band == int(k["band"]):
            khu_id = k["id"]
            src = [a for a in areas if a.props.get("khu") == khu_id]
    if not src and banded:
        src = [a for a in banded if dia_do.area_band(a.props)[0] == band]
    if not src and not banded:
        src = areas
    normals, elites = _split(a.props.get("monster") for a in src)
    where = "khu" if khu_id else ("band" if banded else ("zone" if areas else "fallback"))
    if not normals and banded:      # a deepest band of elites only: the normals of the band below
        for lower in range(band - 1, 0, -1):
            normals, _ = _split(a.props.get("monster") for a in banded if dia_do.area_band(a.props)[0] == lower)
            if normals:
                break
    if not normals and not elites:
        fb = quai(realm_id, raw).get("fallback") or {}
        normals, elites, where = list(fb.get("normals", [])), list(fb.get("elites", [])), "fallback"
    if not normals:                 # elites only, even below: they fill the room themselves
        normals = list(elites)
    return {"band": band, "khu": khu_id, "zone": zone_id, "normals": normals, "elites": elites, "from": where}


# ------------------------------------------------------------------ the plan of a run
def _draw(kinds: list[str], count: int, rng: random.Random) -> list[str]:
    """`count` creatures out of `kinds`: every kind once before any twice (shuffled), so a room
    of n >= len(kinds) creatures shows every kind of its row."""
    if not kinds or count <= 0:
        return []
    order = list(kinds)
    rng.shuffle(order)
    return [order[i % len(order)] for i in range(count)]


def plan(realm_id: str, band: int, rng: random.Random, n_rooms: int, origin: dict | None = None,
         raw: dict | None = None) -> dict:
    """The creatures of a whole run: {"band", "rooms": [[kind, ...] per room before the boss],
    "boss": {...}, "khu", "from"}. `origin` = {"zone", "x", "y"} of a rift. A realm with fewer
    rows than rooms repeats its last row; with no row at all (data under construction) a room
    is empty."""
    band = max(BANDS[0], min(BANDS[-1], int(band or 1)))
    q = quai(realm_id, raw)
    land = None
    if q.get("theme") == LAND:
        o = origin or {}
        land = land_pool(realm_id, o.get("zone"), o.get("x"), o.get("y"), band, raw)
        band = land["band"]
    spec = band_spec(realm_id, band, raw)
    rows = spec.get("rooms") or []
    rooms = []
    for i in range(n_rooms):
        row = rows[min(i, len(rows) - 1)] if rows else {}
        kinds = row.get("kinds") or []
        if kinds == LAND:
            kinds = land["normals"] if land else []
        out = _draw(list(kinds), int(row.get("count", 0)), rng)
        elite = row.get("elite")
        if elite == LAND:
            elite = rng.choice(land["elites"]) if land and land["elites"] else None
        if elite:
            out.append(elite)
        rooms.append(out)
    return {"band": band, "rooms": rooms, "boss": boss_spec(realm_id, band, raw),
            "khu": land["khu"] if land else None, "from": land["from"] if land else "theme"}


def boss_spec(realm_id: str, band: int, raw: dict | None = None) -> dict:
    """The den's boss in this band: {"kind" (its body and picture), "hp_mult", "overlay"}.
    `overlay` = what its info gets on top of its kind's own numbers: the stats of the boss it
    stands in for (`stats_from`: the group shield and its phases) and its name; {} when it is
    simply its own kind."""
    r = (raw or {}).get("realms", {}).get(realm_id) if raw is not None else realms().get(realm_id)
    r = r or {}
    b = band_spec(realm_id, band, raw).get("boss") or {}
    kind = b.get("kind") or r.get("boss")
    overlay: dict = {}
    src = b.get("stats_from")
    if src and src != kind:
        base = _mons().get(src, {})
        overlay = {k: base[k] for k in BOSS_KEYS if k in base}
    if b.get("name_vi"):
        overlay["name_vi"] = b["name_vi"]
    return {"kind": kind, "hp_mult": float(b.get("hp_mult", r.get("boss_hp_mult", 1.0))), "overlay": overlay}


def fielded(realm_id: str, raw: dict | None = None) -> set[str]:
    """Every creature a realm may field, whatever the band and wherever a rift opens (loot.py
    counts their drops in the realm's cap)."""
    from .. import balance
    out: set[str] = set()
    q = quai(realm_id, raw)
    for b in BANDS:
        spec = band_spec(realm_id, b, raw)
        for row in spec.get("rooms") or []:
            if isinstance(row.get("kinds"), list):
                out |= set(row["kinds"])
            if row.get("elite") and row["elite"] != LAND:
                out.add(row["elite"])
        bs = boss_spec(realm_id, b, raw)
        if bs["kind"]:
            out.add(bs["kind"])
    if q.get("theme") == LAND:
        fb = q.get("fallback") or {}
        out |= set(fb.get("normals", [])) | set(fb.get("elites", []))
        rc = balance.load("realm").get("rift", {})
        if rc.get("realm") == realm_id:
            for zid in rc.get("zones", []):
                normals, elites = _split(a.props.get("monster") for a in _zone_areas(zid))
                out |= set(normals) | set(elites)
    return out


# ------------------------------------------------------------------ pictures
def _client_dir() -> Path:
    return DATA_DIR.parent.parent / "client"


@lru_cache(maxsize=1)
def _wiring() -> dict | None:
    p = _client_dir() / "assets" / "v2" / "wiring.json"
    try:
        return json.loads(p.read_text("utf-8"))
    except FileNotFoundError:
        return None


def has_picture(kind: str) -> bool | None:
    """Has this creature its own picture in the client's v2 art (wiring.json -> a sheet that
    exists)? None when there is no client next to the server (nothing to check)."""
    w = _wiring()
    if w is None:
        return None
    sheet = (w.get("monsters") or {}).get(kind)
    return bool(sheet) and (_client_dir() / "assets" / "v2" / "monsters" / f"{sheet}.png").exists()


# ------------------------------------------------------------------ the check
def _land_of(zone_id: str) -> str | None:
    from ..realtime import lands
    return lands.zone_land_id(zone_id)


def _sample_points(zone_id: str) -> list[tuple[float | None, float | None, str]]:
    """Where a rift may open, for the check: the anchor of every khu, and nowhere in particular."""
    from ..realtime import dia_do
    pts = [(float(k["anchor"][0]), float(k["anchor"][1]), k["id"]) for k in dia_do.khu_list(zone_id)]
    return pts + [(None, None, "no khu")]


def validate(raw: dict | None = None, realm_cfg: dict | None = None) -> list[str]:
    """One line per problem with what the bí cảnh field (empty = sound): every realm has a theme
    and a row for every band, one per room of its math.rooms; every creature exists, has a
    picture and belongs to the theme (ink family / quái lỗi sai of the band's floors / the
    rift's own land); room creatures are normals, an `elite` an elite, never in band 1, the
    boss has a body with a picture and a group shield; a deeper band never fields fewer; the
    rift fields something in every band wherever it opens."""
    from .. import balance
    raw = raw if raw is not None else json.loads((DATA_DIR / "realms.json").read_text("utf-8"))
    c = realm_cfg if realm_cfg is not None else balance.load("realm")
    mons = _mons()
    ink = ink_family()
    out: list[str] = []

    def creature(kind, where: str, rank: str | None = None, theme: str | None = None, band: int = 0) -> None:
        if kind not in mons:
            out.append(f"{where}: unknown creature {kind!r}")
            return
        if has_picture(kind) is False:
            out.append(f"{where}: {kind} has no picture (client/assets/v2/wiring.json monsters)")
        m = mons[kind]
        if rank and m.get("rank", "normal") != rank:
            out.append(f"{where}: {kind} is {m.get('rank', 'normal')}, not {rank}")
        if theme == "muc" and kind not in ink:
            out.append(f"{where}: {kind} is not of the ink family (data/creatures/monsters.json)")
        if theme == "tran":
            if not m.get("skill") or not isinstance(m.get("floor"), int):
                out.append(f"{where}: {kind} is not a quái lỗi sai")
            elif m["floor"] > band:
                out.append(f"{where}: {kind} is a quái lỗi sai of floor {m['floor']}, above the band's floors 1-{band}")

    for rid, r in raw.get("realms", {}).items():
        here = f"realm {rid}"
        q = r.get("quai")
        if not isinstance(q, dict):
            out.append(f"{here}: quai (the creatures it fields) missing")
            continue
        theme = q.get("theme")
        if theme not in THEMES:
            out.append(f"{here}: quai.theme must be one of {', '.join(THEMES)}")
        if theme == LAND and r.get("kind") != "rift":
            out.append(f"{here}: only a rift spills the creatures of a land")
        n_rooms = len((r.get("math") or {}).get("rooms") or [])
        totals = []
        for b in BANDS:
            spec = (q.get("bands") or {}).get(str(b))
            where = f"{here} band {b}"
            if not isinstance(spec, dict):
                out.append(f"{where}: missing (every bí cảnh needs a row for every band)")
                totals.append(None)
                continue
            rows = spec.get("rooms")
            if not isinstance(rows, list) or len(rows) != n_rooms:
                out.append(f"{where}: rooms must have one row per room of math.rooms ({n_rooms})")
                rows = rows if isinstance(rows, list) else []
            total = 0
            for i, row in enumerate(rows):
                w = f"{where} room {i}"
                kinds, count = row.get("kinds"), row.get("count")
                if not isinstance(count, int) or count < 1:
                    out.append(f"{w}: count must be a whole number >= 1")
                    count = 0
                if kinds == LAND:
                    if theme != LAND:
                        out.append(f"{w}: kinds 'land' is for a rift only")
                elif not isinstance(kinds, list) or not kinds:
                    out.append(f"{w}: kinds must be a list of creatures (or 'land' in a rift)")
                else:
                    for kind in kinds:
                        creature(kind, w, "normal", theme, b)
                elite = row.get("elite")
                if elite:
                    if b == BANDS[0]:
                        out.append(f"{w}: no elite in band 1 (an elite appears from Trung Vực on)")
                    if elite == LAND:
                        if theme != LAND:
                            out.append(f"{w}: elite 'land' is for a rift only")
                    else:
                        creature(elite, w, "elite", theme, b)
                total += count + (1 if elite else 0)
            totals.append(total)
            bs = spec.get("boss") or {}
            body = bs.get("kind") or r.get("boss")
            w = f"{where} boss"
            if body not in mons:
                out.append(f"{w}: unknown creature {body!r}")
            else:
                if has_picture(body) is False:
                    out.append(f"{w}: {body} has no picture")
                if theme == "muc" and body not in ink:
                    out.append(f"{w}: {body} is not of the ink family")
                if theme == "tran":
                    creature(body, w, None, "tran", b)
                stats = mons.get(bs.get("stats_from") or body, {})
                if not stats.get("group_shield"):
                    out.append(f"{w}: its stats ({bs.get('stats_from') or body}) have no group shield: "
                               f"not a boss")
                if stats.get("land") == "loi_kiep_dai" or mons[body].get("land") == "loi_kiep_dai":
                    out.append(f"{w}: Lôi Kiếp Đài's creatures stay in their arena")
            hp = bs.get("hp_mult", r.get("boss_hp_mult", 1.0))
            if not isinstance(hp, (int, float)) or not 0.2 <= hp <= 3:
                out.append(f"{w}: hp_mult must be a number in 0.2..3")
            if bs.get("name_vi") is not None and not str(bs["name_vi"]).strip():
                out.append(f"{w}: name_vi is empty")
        known = [t for t in totals if t is not None]
        if any(b < a for a, b in zip(known, known[1:])):
            out.append(f"{here}: a deeper band fields fewer creatures than the band before it ({totals})")
        if theme == LAND:
            fb = q.get("fallback") or {}
            if not fb.get("normals"):
                out.append(f"{here}: quai.fallback.normals missing (a rift where no creature lives)")
            for kind in fb.get("normals", []):
                creature(kind, f"{here} fallback", "normal", "muc")
            for kind in fb.get("elites", []):
                creature(kind, f"{here} fallback", "elite", "muc")
            rc = c.get("rift", {})
            if rc.get("realm") == rid:
                for zid in rc.get("zones", []):
                    land_id = _land_of(zid)
                    for x, y, label in _sample_points(zid):
                        for b in BANDS:
                            pool = land_pool(rid, zid, x, y, b, raw)
                            w = f"{here}: a rift in {zid} ({label}) band {b}"
                            if not pool["normals"]:
                                out.append(f"{w}: fields nothing")
                            for kind in pool["normals"] + pool["elites"]:
                                if has_picture(kind) is False:
                                    out.append(f"{w}: {kind} has no picture")
                                own = mons.get(kind, {}).get("land")
                                if pool["from"] != "fallback" and own and land_id and own != land_id:
                                    out.append(f"{w}: {kind} belongs to the land {own}, not {land_id}")
                                if mons.get(kind, {}).get("rank") == "boss":
                                    out.append(f"{w}: {kind} is a boss")
    return out
