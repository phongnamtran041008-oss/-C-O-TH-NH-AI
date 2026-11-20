"""Bí cảnh, the database side (spec 14): daily entries, runs, loot and the forge for Mảnh Bảo Vật.

The live run (rooms, puzzles, the boss) is app/realtime/realm.py and never touches the
database in its tick; it calls the coroutines here as background tasks. Loot is written
together with a RealmClaim row whose primary key is (run, player, stage), so a room or the
final chest can pay each player once and only once, however often it is asked (spec 14.3).
"""
from __future__ import annotations

import json
import random
from functools import lru_cache

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from .. import db as dbm
from ..config import DATA_DIR
from ..models import Character, RealmClaim, RealmMember, RealmRun, User
from . import catalog, cultivation, inventory, items


class RealmError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


def cfg() -> dict:
    return balance.load("realm")


@lru_cache(maxsize=1)
def data() -> dict:
    return json.loads((DATA_DIR / "realms.json").read_text("utf-8"))


def realms() -> dict:
    return data()["realms"]


def puzzle_info(kind: str) -> dict:
    return data()["puzzles"].get(kind, {})


# ------------------------------------------------------------------ entries
async def entries_used(db: AsyncSession, user_id: int, day: str | None = None) -> dict[str, int]:
    day = day or clock.local_date(clock.now())
    rows = (await db.execute(select(RealmMember.realm_id, func.count()).where(
        RealmMember.user_id == user_id, RealmMember.day == day).group_by(RealmMember.realm_id))).all()
    return {r: int(n) for r, n in rows}


def daily_limit(realm_id: str) -> int:
    """Entries a day: the realm's own `daily_entries` (realms.json) or the balance default."""
    return int(realms().get(realm_id, {}).get("daily_entries", cfg()["daily_entries"]))


async def math_floors(db: AsyncSession, user_ids: list[int]) -> dict[int, int | None]:
    """M10: the floor each player's questions in a math bí cảnh come from (math_ask.own_floor),
    None for a player the bank has no question for at all."""
    from . import math_ask
    out: dict[int, int | None] = {}
    for uid in user_ids:
        where = await math_ask.own_floor(db, uid)
        out[uid] = where[1] if where else None
    return out


async def over_limit(db: AsyncSession, user_ids: list[int], realm_id: str) -> list[int]:
    """Spec 14.1: each player may enter each realm at most N times a day."""
    day = clock.local_date(clock.now())
    limit = daily_limit(realm_id)
    out = []
    for uid in user_ids:
        if (await entries_used(db, uid, day)).get(realm_id, 0) >= limit:
            out.append(uid)
    return out


async def create_run(db: AsyncSession, realm_id: str, user_ids: list[int]) -> int:
    now = clock.now()
    run = RealmRun(realm_id=realm_id, started_at=now, members=list(user_ids))
    db.add(run)
    await db.flush()
    day = clock.local_date(now)
    for uid in user_ids:
        db.add(RealmMember(run_id=run.id, user_id=uid, realm_id=realm_id, day=day, joined_at=now))
    await db.flush()
    return run.id


async def abort_run(run_id: int) -> None:
    """The party fell apart before stepping in: the entry is given back."""
    async with dbm.SessionLocal() as db:
        run = await db.get(RealmRun, run_id)
        if run is not None:
            await db.delete(run)
        await db.commit()


async def member_left(run_id: int, user_id: int, result: str = "left") -> None:
    async with dbm.SessionLocal() as db:
        await db.execute(update(RealmMember).where(
            RealmMember.run_id == run_id, RealmMember.user_id == user_id, RealmMember.left_at.is_(None))
            .values(left_at=clock.now(), result=result))
        await db.commit()


async def finish_run(run_id: int, result: str, user_ids: list[int]) -> None:
    async with dbm.SessionLocal() as db:
        run = await db.get(RealmRun, run_id)
        if run is not None:
            run.ended_at, run.result = clock.now(), result
        if user_ids:
            await db.execute(update(RealmMember).where(
                RealmMember.run_id == run_id, RealmMember.user_id.in_(user_ids), RealmMember.left_at.is_(None))
                .values(left_at=clock.now(), result=result))
        await db.commit()


# ------------------------------------------------------------------ loot
async def _claim(user_id: int, run_id: int, stage: str, roll) -> dict | None:
    """Writes the claim and what `roll(db, rng)` grants in one transaction. Returns None when
    this stage was already paid to this player."""
    rng = random.Random()
    async with dbm.SessionLocal() as db:
        claim = RealmClaim(run_id=run_id, user_id=user_id, stage=stage, loot={}, created_at=clock.now())
        db.add(claim)
        try:
            await db.flush()
        except IntegrityError:
            await db.rollback()
            return None
        loot = await roll(db, rng)
        claim.loot = {k: v for k, v in loot.items() if k != "xp"}
        try:
            await db.commit()
        except IntegrityError:   # a twin request won the race
            await db.rollback()
            return None
    return loot


def _open_entries(entries: list[dict], realm: str, stage: int) -> list[dict]:
    """The entries of a weighted table this player may get (loot.py): items they have
    unlocked, equipment whose lowest rarity is within their cap."""
    from . import loot
    cap = loot.rarity_cap(realm, stage)
    order = items.RARITY_ORDER
    out = []
    for e in entries:
        if "item" in e:
            if loot.unlocked(e["item"], realm, stage):
                out.append(e)
        elif cap is not None and order.index(e.get("min_rarity") or order[0]) <= order.index(cap):
            out.append(e)
    return out


async def _grant_table(db: AsyncSession, uid: int, rng: random.Random, entries: list[dict], ref: str,
                       out: dict, tier: tuple[str, int] = ("pham_nhan", 0), realm_id: str | None = None) -> None:
    """One roll of a weighted table: what the player has not unlocked is taken out first, then
    the rest is weighed; nothing left, nothing paid. Equipment also stays within the cap of
    the bí cảnh `realm_id`."""
    from . import loot
    entries = _open_entries(entries, *tier)
    if not entries:
        return
    total = sum(e["weight"] for e in entries)
    x = rng.uniform(0, total)
    for e in entries:
        x -= e["weight"]
        if x <= 0:
            break
    if "item" in e:
        qty = rng.randint(*e.get("qty", [1, 1]))
        out["items"] += await items.grant_items(db, uid, [{"item": e["item"], "qty": qty}], "realm", ref)
    else:
        rar = loot.roll_equipment_rarity(rng, e.get("min_rarity"), *tier,
                                         within=loot.source_cap(realm_id) if realm_id else None)
        out["equipment"].append(await items.grant_equipment(db, uid, rng.choice(e["equipment"]), rar, "realm", ref))


async def claim_room(run_id: int, user_id: int, room_index: int, room_kind: str, realm_id: str) -> dict | None:
    """A cleared room's loot, from the realm's own table (`room_loot_by_realm`: Linh Thạch and
    the materials of data/math/drops.json; Tu Vi comes from the answers alone, so its `xp` is 0)."""
    c = cfg()["room_loot_by_realm"][realm_id]
    ref = f"run{run_id}:room{room_index}"

    async def roll(db, rng):
        from . import loot
        out = {"stage": f"room{room_index}", "room": room_kind, "items": [], "equipment": []}
        stones = rng.randint(*c["stones"])
        out["spirit_stones"] = await inventory.change_currency(db, user_id, "spirit_stones", stones, "realm", ref)
        out["stones"] = stones
        realm, stage = await loot.player_tier(db, user_id)
        for d in c["items"]:
            if rng.random() < d["chance"]:
                qty = rng.randint(*d.get("qty", [1, 1]))
                if not loot.unlocked(d["item"], realm, stage):   # rolled but above this player's tu vi
                    loot.note_locked(out, d["item"])
                    continue
                out["items"] += await items.grant_items(db, user_id, [{"item": d["item"], "qty": qty}], "realm", ref)
        if c["xp"]:
            out["xp"] = await cultivation.add_xp(db, user_id, c["xp"], "realm")
        return out
    return await _claim(user_id, run_id, f"room{room_index}", roll)


async def claim_chest(run_id: int, user_id: int, realm_id: str, fragments: int, fast: bool) -> dict | None:
    """The final chest (spec 14.3): every player rolls on their own; the Mảnh Bảo Vật count is
    the same for the whole team, but only a player whose tu vi has unlocked them gets them
    (loot.py; the others see them under `locked`). Finishing fast adds stones and a roll."""
    c = cfg()
    chest = c["chest"][realm_id]
    ref = f"run{run_id}:chest"

    async def roll(db, rng):
        from . import loot
        out = {"stage": "chest", "items": [], "equipment": [], "fast": fast}
        tier = await loot.player_tier(db, user_id)
        stones = rng.randint(*chest["stones"])
        if fast:
            stones = int(round(stones * c["fast_bonus"]["stones_mult"]))
        out["spirit_stones"] = await inventory.change_currency(db, user_id, "spirit_stones", stones, "realm", ref)
        out["stones"] = stones
        jade = rng.randint(*chest["jade"])
        if jade:
            out["immortal_jade"] = await inventory.change_currency(db, user_id, "immortal_jade", jade, "realm", ref)
            out["jade"] = jade
        if fragments and not loot.unlocked("manh_bao_vat", *tier):
            loot.note_locked(out, "manh_bao_vat")      # the team's count, but not for this tu vi yet
        elif fragments:
            out["items"] += await items.grant_items(db, user_id, [{"item": "manh_bao_vat", "qty": fragments}],
                                                    "realm", ref)
        for _ in range(chest["rolls"] + (c["fast_bonus"]["extra_rolls"] if fast else 0)):
            await _grant_table(db, user_id, rng, chest["table"], ref, out, tier, realm_id)
        if chest["xp"]:
            out["xp"] = await cultivation.add_xp(db, user_id, chest["xp"], "realm")
        from . import quests
        out["quests"] = await quests.on_event(db, user_id, "realm", realm_id)
        return out
    return await _claim(user_id, run_id, "chest", roll)


async def claims(db: AsyncSession, run_id: int, user_id: int) -> list[dict]:
    rows = (await db.execute(select(RealmClaim).where(RealmClaim.run_id == run_id, RealmClaim.user_id == user_id)
                             .order_by(RealmClaim.created_at))).scalars().all()
    return [{"stage": r.stage, **(r.loot or {})} for r in rows]


# ------------------------------------------------------------------ the gate
async def view(db: AsyncSession, user: User) -> dict:
    from ..realtime.realm import window_status
    from ..realtime.world import world
    ch = await db.get(Character, user.id)
    used = await entries_used(db, user.id)
    out, math_out = [], []
    floor = (await math_floors(db, [user.id]))[user.id] or 0
    for rid, r in realms().items():
        limit = daily_limit(rid)
        if r["kind"] == "scheduled":
            st = window_status(clock.now())
        elif r["kind"] == "math":   # open whenever the gate is; entered alone or with the party
            st = {"open": True, "opens_in": 0, "closes_in": None}
        else:                       # a rift: open while one is there
            st = {"open": None}
        rooms = r["math"]["rooms"]
        row = {"id": rid, "name_vi": r["name_vi"], "kind": r["kind"], "math": True, "floor": floor,
               "realm_ok": ch is not None and floor > 0, "puzzles": len(rooms),
               "rooms": [puzzle_info(x["kind"]).get("name_vi", x["kind"]) for x in rooms],
               "time_limit_minutes": r["time_limit_minutes"], "desc_vi": r.get("desc_vi", ""),
               "entries_left": max(0, limit - used.get(rid, 0)), "daily": limit,
               "party_min": int(r.get("party_min", cfg()["party_min"])), **st}
        # the always-open one on its own tab; the party ones (rift, scheduled) on the first
        (math_out if r["kind"] == "math" else out).append(row)
    fc = cfg()["forge"]
    eq = catalog.equipment()
    s = eq["sets"]["mac_anh"]
    have = (await items.stacks(db, user.id)).get("manh_bao_vat", 0)
    return {"realms": out, "math_realms": math_out,
            "party": world.parties.view_for(user.id), "queue": world.realms.queue_of(user.id),
            "puzzles": data()["puzzles"],
            "forge": {"fragments": fc["fragments"], "stones": fc["stones"], "have": have,
                      "rarity": fc["rarity"], "rarity_vi": eq["rarities"][fc["rarity"]]["name_vi"],
                      "set_vi": s["name_vi"], "bonus_vi": s["bonus_vi"],
                      "pieces": [{"id": pid, "name_vi": eq["items"][pid]["name_vi"],
                                  "slot_vi": eq["slots"][eq["items"][pid]["slot"]]} for pid in s["pieces"]]}}


async def forge(db: AsyncSession, user: User, piece: str) -> dict:
    """Mảnh Bảo Vật -> one piece of the Mặc Ảnh set at Thiên rarity (spec 14.3)."""
    fc = cfg()["forge"]
    if piece not in catalog.equipment()["sets"]["mac_anh"]["pieces"]:
        raise RealmError(400, "bad_piece", "Không có món đồ này trong bộ.")
    try:
        await inventory.consume_item(db, user.id, "manh_bao_vat", fc["fragments"], "realm_forge", piece)
        await inventory.charge(db, user.id, {"spirit_stones": fc["stones"]}, "realm_forge", piece)
    except inventory.InsufficientFunds:
        raise RealmError(400, "not_enough", f"Cần {fc['fragments']} Mảnh Bảo Vật và {fc['stones']} Linh Thạch.")
    gear = await items.grant_equipment(db, user.id, piece, fc["rarity"], "realm_forge")
    stones = (await db.execute(select(User.spirit_stones).where(User.id == user.id))).scalar_one()
    return {"equipment": gear, "spirit_stones": stones}
