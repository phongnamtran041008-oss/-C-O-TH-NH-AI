"""Linh thú of Thiên Địa Đồ: the `beasts` section of data/math/world_plan.json and its taming rule
(`beast_taming`), wired through `wired_sections` ('beasts'). This is the data and database side;
the beast out in a land - fighting, counting Phản Đòn, yielding - is realtime/beasts.py.

**One companion model.** The game already has Linh Thú: the twelve con giáp of the gacha banner
(data/creatures/pets.json, systems/pets.py), one worn at a time, following the player. A tamed
beast is not a second kind of companion beside them: it becomes a row of the same `pets` table
(`pet_type` = the beast id) and a species of the same `pets.species()` table, so it is worn,
taken off, drawn following its owner and shown in the Linh Thú panel exactly like a con giáp.
What differs is only where it comes from (taming, never the banner: `source` 'thu_phuc', which
the gacha pool leaves out) and its skill: the plan's `gift`, a small effect read where it acts:

  sniff (Linh Hồ)            - GET /beasts/sniff: the weapons lying hidden near the player;
  wrong_guard (Huyền Quy)    - realtime/combat.py _parry: a wrong answer's blow is lighter;
  dodge_cooldown (Bạch Hạc)  - realtime/combat.py dodge: Né Đòn comes back sooner;
  parry_fire (Hỏa Tước)      - realtime/combat.py _parry: the counter hits harder, with fire;
  mount (Tiểu Long)          - realtime/abilities.py: Cưỡi linh thú, faster on the ground.

"Tu vi" in the plan is the player's place in Đạo Thụ (lands.TreePos), never the cultivation realm.
"""
from __future__ import annotations

from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..learning import math_tree
from ..models import CodexEntry, Pet, User
from . import catalog, inventory

SOURCE = "thu_phuc"
LOCKED, OPEN, TAMED = "locked", "open", "tamed"


class BeastError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the plan, as tables
def wired() -> bool:
    return math_tree.section_wired("beasts")


@lru_cache(maxsize=1)
def _data() -> dict:
    plan = math_tree.world_plan()
    every = {b["id"]: b for b in plan.get("beasts", [])}
    return {"all": every, "built": {k: b for k, b in every.items() if b.get("status") == "co"},
            "taming": plan.get("beast_taming", {}), "lands": {l["id"]: l for l in plan.get("lands", [])}}


def clear_cache() -> None:
    _data.cache_clear()
    land_nodes.cache_clear()
    fight_info.cache_clear()


def taming() -> dict:
    return _data()["taming"]


def built() -> dict[str, dict]:
    """The beasts that exist in the game (status 'co'), by id; none while the section is not wired."""
    return _data()["built"] if wired() else {}


def beast(bid: str | None) -> dict | None:
    return built().get(bid or "")


def is_beast(kind: str | None) -> bool:
    return beast(kind) is not None


def gift(pet_type: str | None) -> dict | None:
    b = beast(pet_type)
    return b.get("gift") if b else None


def gift_value(pet_type: str | None, gtype: str, key: str = "value") -> float:
    """The worn beast's gift number if its gift is of this type, else 0."""
    g = gift(pet_type)
    if not g or g.get("type") != gtype:
        return 0.0
    return float(g.get(key, 0) or 0)


def species() -> dict[str, dict]:
    """Every built beast shaped like a species of pets.json, for the one companion table."""
    out = {}
    for bid, b in built().items():
        out[bid] = {"name_vi": b["name_vi"], "zodiac_vi": "Linh thú", "rarity": "epic", "source": SOURCE,
                    "skill": dict(b.get("gift") or {}), "skill_vi": b.get("gift_vi", ""), "stats": {},
                    "look": {}}
    return out


@lru_cache(maxsize=None)
def land_nodes(land_id: str) -> tuple[str, ...]:
    """The Đạo Thụ nodes the creatures of a land stand for: what a beast of that land asks about
    when its blow lands (realtime/lands.py LandAsker picks from them like for any creature)."""
    land = _data()["lands"].get(land_id) or {}
    mons = catalog.monsters()
    nodes: list[str] = []
    for kind in land.get("monsters", []):
        for n in mons.get(kind, {}).get("nodes", []):
            if n not in nodes:
                nodes.append(n)
    return tuple(nodes)


@lru_cache(maxsize=None)
def fight_info(bid: str) -> dict:
    """How a beast fights, shaped like a monster of monsters.json (realtime/ai.py reads it)."""
    b = _data()["all"][bid]
    f = b.get("fight", {})
    land = _data()["lands"].get(b["land"]) or {}
    return {"name_vi": b["name_vi"], "rank": "normal", "beast": True, "land": b["land"], "branch": land.get("branch"),
            "ask": "nodes", "nodes": list(land_nodes(b["land"])),
            "hp": float(f.get("hp", 100)), "atk": float(f.get("atk", 8)), "def": float(f.get("def", 0)),
            "speed": float(f.get("speed", 30)), "attack_radius": float(f.get("attack_radius", 22)),
            "aggro_radius": float(f.get("aggro_radius", 64)), "aggressive": True, "idle_seconds": [1.5, 4.0],
            "xp": 0, "stones": [0, 0], "drops": [], "respawn_seconds": 30, "shield_regen": []}


# ------------------------------------------------------------------ who may meet a beast
def _realm_vi(realm: str) -> str:
    r = next((x for x in math_tree.tree().raw.get("realms", []) if x["id"] == realm), None)
    return r["name_vi"] if r else realm


def missing_vi(b: dict, pos) -> list[str]:
    """What a player standing at `pos` (a lands.TreePos, or None) lacks to meet this beast."""
    from . import weapons
    out = []
    req = b.get("requires", {})
    at = (pos.realm, pos.stage) if pos is not None else None
    if at is None or not weapons.reaches(at, req.get("realm", "luyen_khi"), int(req.get("stage", 0))):
        out.append(f"Cần {_realm_vi(req.get('realm', 'luyen_khi'))} tầng {req.get('stage', 0)} trên Đạo Thụ.")
    need = b.get("needs")
    if need and (at is None or not weapons.unlock_open(need, at)):
        u = weapons.data()["unlocks"].get(need, {})
        out.append(f"Cần {u.get('name_vi', need)}.")
    return out


def can_meet(b: dict, pos, tamed=()) -> bool:
    """Does this beast show itself to a player at this place in Đạo Thụ who tamed these?"""
    return b.get("status") == "co" and b["id"] not in tamed and not missing_vi(b, pos)


# ------------------------------------------------------------------ the database side
async def tamed(db: AsyncSession, user_id: int) -> set[str]:
    rows = (await db.execute(select(Pet.pet_type).where(Pet.user_id == user_id))).scalars().all()
    return {r for r in rows if r in _data()["all"]}


async def seal(db: AsyncSession, user: User, bid: str) -> dict:
    """Phong Ấn Phù on a beast that yielded (the world checked that): one talisman spent, the
    beast joins the player's Linh Thú. Returns the new pet's view."""
    from . import pets
    b = beast(bid)
    if b is None:
        raise BeastError(404, "no_beast", "Không có linh thú này.")
    if bid in await tamed(db, user.id):
        raise BeastError(400, "tamed", f"Con đã thu {b['name_vi']} rồi.")
    item = taming().get("talisman", "phong_an_phu")
    try:
        await inventory.consume_item(db, user.id, item, 1, "thu_phuc", bid)
    except inventory.InsufficientFunds:
        raise BeastError(400, "no_talisman",
                         f"Cần một {catalog.item_name(item)} (bán ở Sạp Tạp Hóa) để thu {b['name_vi']}.") from None
    row = Pet(user_id=user.id, pet_type=bid, level=1, equipped=False)
    db.add(row)
    await db.flush()
    if await db.get(CodexEntry, (user.id, "pet", bid)) is None:
        db.add(CodexEntry(user_id=user.id, codex="pet", entry_id=bid, discovered_at=clock.now(), progress={}))
        await db.flush()
    return pets.view(row)


def beast_view(b: dict, pos, tamed_ids: set[str]) -> dict:
    from ..realtime import lands
    lacking = missing_vi(b, pos)
    state = TAMED if b["id"] in tamed_ids else (LOCKED if lacking else OPEN)
    land = _data()["lands"].get(b["land"], {})
    return {"id": b["id"], "name_vi": b["name_vi"], "land": b["land"], "land_vi": land.get("name_vi", b["land"]),
            "zone": lands.zone_of(b["land"]), "where_vi": b.get("where_vi", ""), "pos": b.get("pos"),
            "requires": b.get("requires", {}), "needs": b.get("needs"), "parries_to_tame": b["parries_to_tame"],
            "gift": b.get("gift"), "gift_vi": b.get("gift_vi", ""), "state": state, "reason_vi": " ".join(lacking)}


async def view(db: AsyncSession, user: User) -> dict:
    """GET /beasts: every built beast with whether this player can meet it, and the taming rule."""
    from ..realtime import lands
    from . import weapons
    pos = await lands.load_pos(db, user.id)
    mine = await tamed(db, user.id)
    t = taming()
    item = t.get("talisman", "phong_an_phu")
    held = (await _held(db, user.id, item))
    return {"beasts": [beast_view(b, pos, mine) for b in built().values()],
            "rule_vi": math_tree.world_plan().get("beast_taming_vi", ""),
            "talisman": {"item": item, "name_vi": catalog.item_name(item), "have": held},
            "can_seal": weapons.unlock_open(t.get("seal_unlock", ""), (pos.realm, pos.stage)),
            "tu_vi": {"realm": pos.realm, "stage": pos.stage}}


async def _held(db: AsyncSession, user_id: int, item: str) -> int:
    from . import items
    return (await items.stacks(db, user_id)).get(item, 0)
