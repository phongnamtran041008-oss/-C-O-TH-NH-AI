"""Rơi đồ theo tu vi (2026-11-20): good loot unlocks only as the player climbs.

The author's rule: "từ quái và các bí cảnh đồ xịn thì càng đi lên cao ms càng mở khóa nhé k p
tống hết con nào cx rơi ra đc". Two sides, both read from data/loot_tiers.json:

  * the player: every item of a loot table has a tier (a cultivation realm and stage) at
    which it starts dropping, and every equipment rarity has one too. Wherever loot from
    fighting or exploring is granted - monsters (realtime/combat.py), bí cảnh rooms and
    chest (secret_realm.py), hầm ngục (math_dungeon.py), cơ duyên (math_fortune.py) - an
    entry the player has not unlocked is not granted; a drop that was rolled but is locked
    is reported to the client (`locked`, see note_locked) instead of being lost silently.
    An item missing from the file is locked below the top tier (fail closed), except the
    ghi chú lỗi sai (kind note of math/drops.json), which are learning aids and never gated;
  * the sources: a wild zone or a bí cảnh may not list anything above its cap, counting the
    monsters that spawn there. validate() checks this (tools/check_all.py).

Not gated on purpose: shop purchases, quest and milestone rewards, gacha, crafting outputs,
fishing catches, alchemy and the thủ thành first-clear rewards.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from ..config import DATA_DIR
from . import catalog

DATA_FILE = DATA_DIR / "loot_tiers.json"
MAX_LOCKED = 3          # at most this many locked drops are reported in one payload

Tier = tuple[int, int]  # (index of the realm in realms_cultivation.json, stage)


@lru_cache(maxsize=1)
def data() -> dict:
    return json.loads(DATA_FILE.read_text("utf-8"))


def _realms() -> list[dict]:
    return catalog.realms()


def _index(realm: str) -> int:
    for i, r in enumerate(_realms()):
        if r["id"] == realm:
            return i
    raise ValueError(f"unknown realm {realm!r}")


def _first_stage(realm_def: dict) -> int:
    return 1 if realm_def.get("stages", 0) > 0 else 0


# ------------------------------------------------------------------ tiers
def parse(tier: str) -> Tier:
    """'luyen_khi:4' -> (1, 4); 'truc_co' -> (2, 1) (a realm alone is its first stage);
    'pham_nhan' -> (0, 0). Raises ValueError on anything else."""
    if not isinstance(tier, str) or not tier:
        raise ValueError(f"bad tier {tier!r}")
    realm, _, stage = tier.partition(":")
    i = _index(realm)
    rd = _realms()[i]
    if not stage:
        return i, _first_stage(rd)
    if not stage.isdigit():
        raise ValueError(f"bad stage in tier {tier!r}")
    s = int(stage)
    lo, hi = _first_stage(rd), rd.get("stages", 0)
    if not lo <= s <= max(lo, hi):
        raise ValueError(f"stage {s} out of range for {realm} in tier {tier!r}")
    return i, s


def top() -> Tier:
    i = len(_realms()) - 1
    rd = _realms()[i]
    return i, max(_first_stage(rd), rd.get("stages", 0))


def rank(realm: str, stage: int) -> Tier:
    """Where a player stands; an unknown realm counts as the very bottom."""
    try:
        return _index(realm), int(stage or 0)
    except ValueError:
        return 0, 0


def compare(a: str, b: str) -> int:
    """-1, 0 or 1 as tier a is below, equal to or above tier b."""
    x, y = parse(a), parse(b)
    return (x > y) - (x < y)


def label(t: Tier) -> str:
    """'Phàm Nhân', 'Luyện Khí tầng 7', 'Trúc Cơ sơ kỳ': the wording of cultivation.stage_label."""
    from . import cultivation
    return cultivation.stage_label(_realms()[t[0]]["id"], t[1])


def _is_note(item_id: str) -> bool:
    return catalog.math_drops().get(item_id, {}).get("kind") == "note"


def item_tier(item_id: str) -> Tier | None:
    """The tier an item starts dropping at; None for an item that is never gated (a ghi chú).
    An item the file does not list is locked below the top tier."""
    if _is_note(item_id):
        return None
    t = data()["items"].get(item_id)
    return parse(t) if t else top()


def unlocked(item_id: str, realm: str, stage: int) -> bool:
    t = item_tier(item_id)
    return t is None or rank(realm, stage) >= t


def need_vi(item_id: str) -> str:
    t = item_tier(item_id)
    return label(t) if t is not None else ""


def rarity_tier(rarity: str) -> Tier:
    t = data()["equipment_rarity"].get(rarity)
    return parse(t) if t else top()


def rarity_cap(realm: str, stage: int) -> str | None:
    """The best equipment rarity this player may get from a drop (None: not even the lowest)."""
    from .items import RARITY_ORDER
    me = rank(realm, stage)
    best = None
    for r in RARITY_ORDER:
        if rarity_tier(r) <= me:
            best = r
    return best


def best_rarity(t: Tier) -> str | None:
    """The best equipment rarity that has unlocked by tier t (None: not even the lowest)."""
    from .items import RARITY_ORDER
    best = None
    for r in RARITY_ORDER:
        if rarity_tier(r) <= t:
            best = r
    return best


def roll_equipment_rarity(rng: random.Random, min_rarity: str | None, realm: str, stage: int,
                          within: Tier | None = None) -> str | None:
    """items.roll_rarity between min_rarity and the lower of two caps: the player's tu vi and,
    when given, the cap `within` of the source (monster_cap / source_cap) - a Trúc Cơ player
    does not pull Địa gear out of a first-forest monster. None when min_rarity is above the
    player's cap (the drop is skipped and reported as locked)."""
    from .items import RARITY_ORDER, roll_rarity
    cap = rarity_cap(realm, stage)
    lo = RARITY_ORDER.index(min_rarity) if min_rarity else 0
    if cap is None or RARITY_ORDER.index(cap) < lo:
        return None
    if within is not None:
        src = best_rarity(within)
        # validate() keeps every entry's minimum inside its source's cap, so `lo` is the floor
        hi = max(lo, RARITY_ORDER.index(src) if src is not None else 0)
        cap = RARITY_ORDER[min(RARITY_ORDER.index(cap), hi)]
    return roll_rarity(rng, min_rarity, cap)


async def player_tier(db: AsyncSession, user_id: int) -> tuple[str, int]:
    """(realm, stage) of a player; Phàm Nhân when they have no character yet."""
    from ..models import Character
    ch = await db.get(Character, user_id)
    if ch is None:
        return "pham_nhan", 0
    return ch.realm or "pham_nhan", int(ch.realm_stage or 0)


# ------------------------------------------------------------------ the locked report
def note_locked(out: dict, item_id: str | None = None, *, name_vi: str | None = None,
                need: str | None = None) -> None:
    """Add one locked drop to a loot payload: out["locked"] = [{"name_vi", "need_vi"}],
    deduplicated, at most MAX_LOCKED."""
    entry = {"name_vi": name_vi or catalog.item_name(item_id or ""),
             "need_vi": need if need is not None else need_vi(item_id or "")}
    locked = out.setdefault("locked", [])
    if entry not in locked and len(locked) < MAX_LOCKED:
        locked.append(entry)


def note_locked_gear(out: dict, item_id: str, min_rarity: str | None) -> None:
    """A piece of equipment whose lowest rarity the player may not get yet."""
    eq = catalog.equipment()
    rarity = min_rarity or "pham"
    name = eq["items"].get(item_id, {}).get("name_vi", item_id)
    note_locked(out, name_vi=f"{name} ({eq['rarities'][rarity]['name_vi']})", need=label(rarity_tier(rarity)))


# ------------------------------------------------------------------ the sources
def _zone_monsters() -> dict[str, set[str]]:
    """Wild zone id -> the monster kinds its map spawns."""
    from ..realtime import maps
    zones = json.loads((DATA_DIR / "zones.json").read_text("utf-8"))
    out: dict[str, set[str]] = {}
    for zid, z in zones.items():
        if zid.startswith("_") or z.get("kind") != "wild":
            continue
        zmap = maps.load(z["map"])
        out[zid] = {a.props.get("monster") for a in zmap.monster_areas if a.props.get("monster")}
    return out


def _entries(drops: list[dict]) -> tuple[list[str], list[str | None]]:
    """(item ids, min rarities of equipment entries) of a drop list."""
    items_, rarities = [], []
    for d in drops:
        if "item" in d:
            items_.append(d["item"])
        elif "equipment" in d:
            rarities.append(d.get("min_rarity"))
    return items_, rarities


def source_cap(source_id: str) -> Tier | None:
    """The cap of a wild zone or a bí cảnh (None: no cap, or not a capped source)."""
    t = data().get("source_caps", {}).get(source_id)
    return parse(t) if t else None


@lru_cache(maxsize=1)
def _monster_caps() -> dict[str, Tier | None]:
    """Monster kind -> the most generous cap among the sources it lives in (None: one of them
    has no cap)."""
    homes: dict[str, set[str]] = {}
    for zid, kinds in _zone_monsters().items():
        for kind in kinds:
            homes.setdefault(kind, set()).add(zid)
    realms = json.loads((DATA_DIR / "realms.json").read_text("utf-8"))["realms"]
    for rid, r in realms.items():
        for kind in set(r.get("room_monsters", {})) | ({r["boss"]} if r.get("boss") else set()):
            homes.setdefault(kind, set()).add(rid)
    out: dict[str, Tier | None] = {}
    for kind, ids in homes.items():
        caps = [source_cap(i) for i in ids]
        out[kind] = None if any(c is None for c in caps) else max(caps)
    return out


def monster_cap(kind: str) -> Tier | None:
    """The cap on what this monster may hand out (None: uncapped, or it lives nowhere)."""
    return _monster_caps().get(kind)


def sources() -> dict[str, dict]:
    """Every capped source: id -> {"what": label, "items": [...], "rarities": [...]}, the
    monsters that spawn there included."""
    from .. import balance
    mons = catalog.monsters()
    rc = balance.load("realm")
    out: dict[str, dict] = {}

    def add(src: str, what: str, items_: list[str], rarities: list[str | None]) -> None:
        s = out.setdefault(src, {"what": what, "items": [], "rarities": []})
        s["items"] += [(i, what) for i in items_]
        s["rarities"] += [(r, what) for r in rarities]

    for zid, kinds in _zone_monsters().items():
        out.setdefault(zid, {"what": f"zone {zid}", "items": [], "rarities": []})
        for kind in sorted(kinds):
            add(zid, f"monster {kind} (zone {zid})", *_entries(mons.get(kind, {}).get("drops", [])))
    realms = json.loads((DATA_DIR / "realms.json").read_text("utf-8"))["realms"]
    for rid, r in realms.items():
        out.setdefault(rid, {"what": f"bí cảnh {rid}", "items": [], "rarities": []})
        for kind in sorted(set(r.get("room_monsters", {})) | ({r["boss"]} if r.get("boss") else set())):
            add(rid, f"monster {kind} (bí cảnh {rid})", *_entries(mons.get(kind, {}).get("drops", [])))
        room = rc.get("room_loot_by_realm", {}).get(rid, {})
        add(rid, f"room loot of {rid}", *_entries(room.get("items", [])))
        chest = rc.get("chest", {}).get(rid, {})
        add(rid, f"chest of {rid}", *_entries(chest.get("table", [])))
        if chest.get("fragments") or chest.get("flawless_fragments", rc.get("flawless_fragments", 0)):
            add(rid, f"chest of {rid} (Mảnh Bảo Vật)", ["manh_bao_vat"], [])
    return out


def table_items() -> dict[str, str]:
    """Every item id of every gated loot table -> where it was seen first."""
    from . import math_dungeon, math_fortune
    seen: dict[str, str] = {}

    def see(item_id: str, where: str) -> None:
        seen.setdefault(item_id, where)

    for kind, m in catalog.monsters().items():
        for i in _entries(m.get("drops", []))[0]:
            see(i, f"monster {kind}")
    for src in sources().values():
        for i, where in src["items"]:
            see(i, where)
    for floor, r in math_dungeon.data().get("rewards", {}).items():
        for i in r.get("room", {}).get("items", {}):
            see(i, f"hầm ngục floor {floor} room")
        for c in r.get("chests", []):
            for i in c.get("items", {}):
                see(i, f"hầm ngục floor {floor} chest")
    for eid, ev in math_fortune.events().items():
        rw = ev.get("rewards", {})
        for i in rw.get("items", []):
            see(i["item"], f"cơ duyên {eid}")
        if rw.get("rare"):
            see(rw["rare"]["item"], f"cơ duyên {eid} (rare)")
    return seen


def validate(raw: dict | None = None) -> list[str]:
    """Problems of data/loot_tiers.json and of the loot tables it gates (empty = sound)."""
    from . import cultivation
    from .items import RARITY_ORDER
    d = raw if raw is not None else data()
    out: list[str] = []

    def tier(t, where: str) -> Tier | None:
        try:
            return parse(t)
        except ValueError as e:
            out.append(f"{where}: {e}")
            return None

    items_ = d.get("items", {})
    for item_id, t in items_.items():
        if item_id.startswith("_"):
            continue
        if not catalog.stack_item(item_id):
            out.append(f"items.{item_id}: not an item of the game")
        tier(t, f"items.{item_id}")
    for item_id, where in sorted(table_items().items()):
        if _is_note(item_id):
            continue
        if item_id not in items_:
            out.append(f"{item_id} ({where}) has no tier in loot_tiers.json items: it would never drop "
                       f"below the top tier")
    rar = d.get("equipment_rarity", {})
    prev: Tier | None = None
    for r in RARITY_ORDER:
        if r not in rar:
            out.append(f"equipment_rarity.{r} missing")
            continue
        t = tier(rar[r], f"equipment_rarity.{r}")
        if t is not None and prev is not None and t < prev:
            out.append(f"equipment_rarity.{r} unlocks before a lower rarity")
        prev = t or prev
    for r in rar:
        if r not in RARITY_ORDER:
            out.append(f"equipment_rarity.{r}: not a rarity")

    def item_t(item_id: str) -> Tier | None:
        if _is_note(item_id):
            return None
        if item_id not in items_:
            return top()
        try:
            return parse(items_[item_id])
        except ValueError:
            return None

    def rar_t(r: str) -> Tier | None:
        try:
            return parse(rar[r]) if r in rar else top()
        except ValueError:
            return None

    caps = d.get("source_caps", {})
    srcs = sources()
    for sid in srcs:
        if sid not in caps:
            out.append(f"source_caps.{sid} missing (use null for no cap)")
    for sid in caps:
        if sid not in srcs:
            out.append(f"source_caps.{sid}: not a wild zone of zones.json nor a bí cảnh of realms.json")
    for sid, src in srcs.items():
        if caps.get(sid) is None:
            continue
        cap = tier(caps[sid], f"source_caps.{sid}")
        if cap is None:
            continue
        for item_id, where in src["items"]:
            t = item_t(item_id)
            if t is not None and t > cap:
                out.append(f"{where}: {item_id} ({label(t)}) is above the cap of {sid} ({label(cap)})")
        for r, where in src["rarities"]:
            t = rar_t(r or "pham")
            if t is not None and t > cap:
                out.append(f"{where}: equipment of rarity {r} ({label(t)}) is above the cap of {sid} ({label(cap)})")
    # a breakthrough pill and what it is brewed from unlock by the last stage of the realm it leaves
    order = [r["id"] for r in _realms()]
    recipes = catalog.recipes()
    for pill_id, p in catalog.pills().items():
        if p.get("effect") != "breakthrough" or p.get("realm") not in order:
            continue
        i = order.index(p["realm"])
        if i == 0:
            continue
        leaves = order[i - 1]
        last = (i - 1, cultivation.last_stage(leaves))
        for item_id in [pill_id] + [g["item"] for g in recipes.get(pill_id, {}).get("ingredients", [])
                                    if g.get("kind") == "item"]:
            if item_id in items_:
                t = item_t(item_id)
                if t is not None and t > last:
                    out.append(f"{item_id} (for {pill_id}) unlocks at {label(t)}, after the last stage of "
                               f"{cultivation.realm_name(leaves)} ({label(last)})")
    return out
