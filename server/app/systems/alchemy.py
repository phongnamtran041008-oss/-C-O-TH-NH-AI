"""Luyện đan (spec 12.3): đan phương, ingredients, the furnace and the canh lửa minigame.

/alchemy/start takes the ingredients and the fee (a Linh Thạch sink) and lights the fire:
the server picks where each văn hỏa zone sits. /alchemy/finish gets how long the needle ran
before each press; the server replays the needle with alchemy_fire.py (the same file as the
client) and decides the quality from the presses alone: phế đan / hạ / trung / thượng phẩm.
A brew that makes pills gives a little Tu Vi by quality (balance/alchemy.json brew_xp).

The furnace in the abode can be upgraded (wider zones, a chance of an extra pill); the
public one at Trúc Lâm Thôn, next to the Đan Sư, is always level 1.
"""
from __future__ import annotations

import datetime as dt
import random
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from ..models import AlchemySession, User
from . import alchemy_fire, buffs, catalog, inventory, items

FISH_RARITY = ["pham", "linh", "huyen", "dia", "thien"]
FISH_RARITY_VI = {"pham": "Phàm", "linh": "Linh", "huyen": "Huyền", "dia": "Địa", "thien": "Thiên"}


class AlchemyError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


def cfg() -> dict:
    return balance.load("alchemy")


def recipes() -> dict:
    return catalog.recipes()


# ------------------------------------------------------------------ the furnace
def furnace_level(user: User) -> int:
    return int((user.flags or {}).get("furnace", 1))


def furnace_info(level: int) -> dict:
    return next(f for f in cfg()["furnace"] if f["level"] == level)


def location(user: User) -> tuple[str, int]:
    """("home", own furnace level) in the abode, ("public", 1) next to the Đan Sư, else
    ("far", 0). Not being in the shared world means the player is at home."""
    from ..realtime.world import world
    if not world.in_world(user.id):
        return "home", furnace_level(user)
    if world.near_npc(user.id, "alchemist", cfg()["public_furnace_reach"]):
        return "public", int(cfg()["public_furnace_level"])
    return "far", 0


# ------------------------------------------------------------------ ingredients
def _ingredient_vi(ing: dict) -> str:
    if ing["kind"] == "item":
        return catalog.item_name(ing["item"])
    return f"Cá {FISH_RARITY_VI[ing['rarity']]}+"


def _fish_rarity(item_id: str) -> str | None:
    if item_id.startswith("fish_") and item_id[5:] in catalog.fish():
        return catalog.fish()[item_id[5:]]["rarity"]
    return None


def _have(ing: dict, stacks: dict[str, int]) -> int:
    if ing["kind"] == "item":
        return stacks.get(ing["item"], 0)
    lo = FISH_RARITY.index(ing["rarity"])
    return sum(q for iid, q in stacks.items() if (_fish_rarity(iid) or "") in FISH_RARITY[lo:])


async def _take(db: AsyncSession, user_id: int, ing: dict, ref: str) -> list[dict]:
    """Spends one ingredient line, the least precious things first. All or nothing (the
    caller's transaction rolls back on InsufficientFunds)."""
    need = int(ing["qty"])
    used = []
    if ing["kind"] == "item":
        await inventory.consume_item(db, user_id, ing["item"], need, "alchemy", ref)
        return [{"what": ing["item"], "name_vi": catalog.item_name(ing["item"]), "qty": need}]
    lo = FISH_RARITY.index(ing["rarity"])
    st = await items.stacks(db, user_id)
    fish = [(iid, q) for iid, q in st.items() if (_fish_rarity(iid) or "") in FISH_RARITY[lo:]]
    fish.sort(key=lambda x: (FISH_RARITY.index(_fish_rarity(x[0])), catalog.fish()[x[0][5:]]["sell_price"], x[0]))
    for iid, q in fish:
        take = min(need, q)
        await inventory.consume_item(db, user_id, iid, take, "alchemy", ref)
        used.append({"what": iid, "name_vi": catalog.item_name(iid), "qty": take})
        need -= take
        if not need:
            break
    if need:
        raise inventory.InsufficientFunds(_ingredient_vi(ing), int(ing["qty"]), int(ing["qty"]) - need)
    return used


# ------------------------------------------------------------------ where a recipe comes from
def _library_shelf() -> dict:
    """The đan phương Thủ Thư sells at Tàng Thư Các (balance/books.json shop)."""
    try:
        return balance.load("books").get("shop", {})
    except FileNotFoundError:
        return {}


def _sources_vi(recipe_item: str) -> list[str]:
    out = []
    if recipe_item in _library_shelf():
        out.append("Mua ở Tàng Thư Các")
    for chain in catalog.quests()["chains"].values():
        if any(it["item"] == recipe_item for st in chain["steps"] for it in st["rewards"].get("items", [])):
            out.append(f"Nhiệm vụ «{chain['title_vi']}»")
    for m in catalog.monsters().values():
        if any(d.get("item") == recipe_item for d in m.get("drops", [])):
            out.append(f"{m['name_vi']} làm rơi")
    return out


def _realm_ok(realm: str, need: str) -> bool:
    from .cultivation import order
    return order().index(realm) >= order().index(need)


async def overview(db: AsyncSession, user: User) -> dict:
    from ..models import Character
    from .cultivation import realm_name
    st = await items.stacks(db, user.id)
    ch = await db.get(Character, user.id)
    realm = ch.realm if ch else "pham_nhan"
    out = []
    for rid, r in recipes().items():
        pill = catalog.pills()[rid]
        known = st.get(r["item"], 0) > 0
        e = {"id": rid, "name_vi": pill["name_vi"], "desc_vi": pill["desc_vi"], "known": known,
             "difficulty": r["difficulty"], "fee": r["fee"], "yield": r["yield"], "have_pills": st.get(rid, 0),
             "min_realm": r["min_realm"], "min_realm_vi": realm_name(r["min_realm"]),
             "realm_ok": _realm_ok(realm, r["min_realm"])}
        if known:
            e["ingredients"] = [{"name_vi": _ingredient_vi(i), "qty": i["qty"], "have": _have(i, st)}
                                for i in r["ingredients"]]
            e["ready"] = all(i["have"] >= i["qty"] for i in e["ingredients"]) and e["realm_ok"]
        else:
            e["sources_vi"] = _sources_vi(r["item"])
        out.append(e)
    where, level = location(user)
    lvl = furnace_level(user)
    nxt = next((f for f in cfg()["furnace"] if f["level"] == lvl + 1), None)
    furnace = {"level": lvl, "name_vi": furnace_info(lvl)["name_vi"], "max": len(cfg()["furnace"]),
               "next": None}
    if nxt:
        furnace["next"] = {"level": nxt["level"], "name_vi": nxt["name_vi"], "cost": nxt["cost"],
                           "materials": [{"item": m["item"], "name_vi": catalog.item_name(m["item"]), "qty": m["qty"],
                                          "have": st.get(m["item"], 0)} for m in nxt["materials"]],
                           "zone_bonus": nxt["zone_bonus"], "extra_chance": nxt["extra_chance"]}
    open_s = await _open_session(db, user.id, clock.now())
    return {"recipes": out, "furnace": furnace, "where": where, "level_here": level,
            "open": public(open_s) if open_s else None, "buffs": buffs.view(user, clock.now()),
            "quality": cfg()["quality"], "brew_xp": cfg()["brew_xp"]}


async def _open_session(db: AsyncSession, user_id: int, now: dt.datetime) -> AlchemySession | None:
    return (await db.execute(select(AlchemySession).where(
        AlchemySession.user_id == user_id, AlchemySession.finished_at.is_(None),
        AlchemySession.expires_at > now))).scalars().first()


def public(s: AlchemySession) -> dict:
    """What the client needs to run the fire."""
    p = s.params
    return {"session_id": s.id, "recipe_id": s.recipe_id, "name_vi": p["name_vi"],
            "bar": p["bar"], "periods": p["periods"], "zones": p["zones"],
            "furnace_level": p["furnace_level"], "expires_at": s.expires_at.isoformat() + "Z",
            "server_time": clock.now().isoformat() + "Z"}


# ------------------------------------------------------------------ brewing
async def start(db: AsyncSession, user: User, recipe_id: str, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    r = recipes().get(recipe_id)
    if r is None:
        raise AlchemyError(404, "no_recipe", "Không có đan phương này.")
    now = clock.now()
    open_s = await _open_session(db, user.id, now)
    if open_s is not None:
        if open_s.recipe_id != recipe_id:
            raise AlchemyError(400, "fire_busy", "Lò đang luyện một mẻ khác, luyện xong đã nhé.")
        return {"fire": public(open_s), "resumed": True}
    if (await items.stacks(db, user.id)).get(r["item"], 0) <= 0:
        raise AlchemyError(400, "no_recipe", f"Con chưa có {catalog.item_name(r['item'])}.")
    from ..models import Character
    ch = await db.get(Character, user.id)
    if ch is None:
        raise AlchemyError(404, "no_character", "Bạn chưa tạo nhân vật.")
    if not _realm_ok(ch.realm, r["min_realm"]):
        from .cultivation import realm_name
        raise AlchemyError(400, "realm_low", f"Đan này cần tu tới {realm_name(r['min_realm'])} mới luyện nổi.")
    where, level = location(user)
    if where == "far":
        raise AlchemyError(400, "too_far", "Hãy đứng cạnh lò luyện đan (ở động phủ, hoặc lò của Đan Sư trong làng).")
    sid = str(uuid.uuid4())
    used = []
    try:
        for ing in r["ingredients"]:
            used += await _take(db, user.id, ing, sid)
    except inventory.InsufficientFunds as e:
        raise AlchemyError(400, "no_ingredient",
                           f"Thiếu nguyên liệu: {catalog.item_name(e.what)} (cần {e.need}, có {e.have}).")
    try:
        await inventory.change_currency(db, user.id, "spirit_stones", -int(r["fee"]), "alchemy_fee", sid)
    except inventory.InsufficientFunds as e:
        raise AlchemyError(400, "insufficient_funds", e.message_vi)
    c = cfg()
    d = str(r["difficulty"])
    from . import linh_can     # a linh căn of the đan path widens the zones (alchemy_zone)
    bonus = furnace_info(level)["zone_bonus"] + int(await linh_can.value_db(db, user.id, "alchemy_zone"))
    lo, hi = c["zone_center_range"]
    zones = [{"center": rng.randint(lo, hi), "width": c["zone_width"][d] + bonus,
              "perfect": c["perfect_width"] + bonus // 2} for _ in range(c["presses"])]
    pill = catalog.pills()[recipe_id]
    params = {"name_vi": pill["name_vi"], "bar": c["bar"], "periods": list(c["period_ms"][d]), "zones": zones,
              "furnace_level": level, "where": where, "used": used}
    s = AlchemySession(id=sid, user_id=user.id, recipe_id=recipe_id, params=params, created_at=now,
                       expires_at=now + dt.timedelta(seconds=c["session_seconds"]))
    db.add(s)
    await db.flush()
    return {"fire": public(s), "resumed": False, "used": used}


def _bad(code: str, msg: str) -> AlchemyError:
    return AlchemyError(400, code, msg)


async def finish(db: AsyncSession, user: User, session_id: str, timings: list,
                 rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    s = await db.get(AlchemySession, session_id)
    if s is None or s.user_id != user.id:
        raise AlchemyError(404, "no_session", "Không tìm thấy mẻ đan này.")
    if s.finished_at is not None:
        raise AlchemyError(409, "finished", "Mẻ đan này đã ra lò rồi.")
    c = cfg()
    now = clock.now()
    p = s.params
    if now > s.expires_at:   # left too long: the fire went out, the ingredients are gone
        s.finished_at = now
        s.result = {"quality": "phe", "expired": True}
        return {"quality": "phe", "quality_vi": _quality_vi("phe"), "expired": True, "made": 0}
    n = c["presses"]
    if not isinstance(timings, list) or len(timings) != n or not all(isinstance(t, int) for t in timings):
        raise _bad("bad_timings", "Dữ liệu canh lửa không hợp lệ.")
    if any(t < c["min_press_ms"] or t > c["max_needle_ms"] for t in timings):
        raise _bad("bad_timings", "Dữ liệu canh lửa không hợp lệ.")
    elapsed_ms = (now - s.created_at).total_seconds() * 1000
    if sum(timings) > elapsed_ms + c["time_grace_ms"]:
        raise _bad("too_fast", "Lửa chưa kịp cháy tới đó, canh lại nhé.")
    hits, positions = [], []
    for i in range(n):
        z = p["zones"][i]
        pos = alchemy_fire.needle(timings[i], p["periods"][i], p["bar"])
        positions.append(round(pos, 2))
        hits.append(alchemy_fire.judge(pos, z["center"], z["width"], z["perfect"]))
    got, best = alchemy_fire.total(hits, c["points"])
    q = alchemy_fire.quality(got, best, c["quality"])
    r = recipes()[s.recipe_id]
    made = int(r["yield"].get(q, 0))
    extra = False
    from . import linh_can     # and gives a chance of one more pill (alchemy_extra)
    chance = furnace_info(p["furnace_level"])["extra_chance"] + await linh_can.value_db(db, user.id, "alchemy_extra")
    if made and chance and rng.random() < chance:
        made += 1
        extra = True
    total_now = None
    if made:
        total_now = await inventory.change_item(db, user.id, s.recipe_id, made, "alchemy", s.id)
    xp = None
    gain = int(round(int(c["brew_xp"].get(q, 0)) * buffs.xp_mult(user, now))) if made else 0
    if gain:
        from . import cultivation
        xp = await cultivation.add_xp(db, user.id, gain, "alchemy")
    if made:
        from . import quests
        await quests.on_event(db, user.id, "brew", s.recipe_id)
    from . import achievements   # Thành Tựu: the batch's quality and the pills made
    await achievements.on_event(db, user.id, "brew", quality=q, made=made)
    result = {"quality": q, "quality_vi": _quality_vi(q), "points": got, "best": best, "hits": hits,
              "positions": positions, "made": made, "extra": extra, "pill": s.recipe_id,
              "pill_name_vi": p["name_vi"], "total": total_now, "xp": xp}
    s.finished_at = now
    s.result = {k: v for k, v in result.items() if k != "xp"}
    return result


def _quality_vi(q: str) -> str:
    return next(x["name_vi"] for x in cfg()["quality"] if x["id"] == q)


async def upgrade_furnace(db: AsyncSession, user: User) -> dict:
    where, _ = location(user)
    if where != "home":
        raise AlchemyError(400, "not_home", "Chỉ nâng cấp được lò luyện đan trong động phủ của con.")
    lvl = furnace_level(user)
    nxt = next((f for f in cfg()["furnace"] if f["level"] == lvl + 1), None)
    if nxt is None:
        raise AlchemyError(400, "max_level", "Lò đã là loại tốt nhất rồi.")
    ref = f"furnace:{nxt['level']}"
    try:
        for m in nxt["materials"]:
            await inventory.consume_item(db, user.id, m["item"], m["qty"], "furnace_upgrade", ref)
    except inventory.InsufficientFunds as e:
        raise AlchemyError(400, "no_material", f"Cần {e.need} {catalog.item_name(e.what)} (đang có {e.have}).")
    try:
        await inventory.charge(db, user.id, nxt["cost"], "furnace_upgrade", ref)
    except inventory.InsufficientFunds as e:
        raise AlchemyError(400, "insufficient_funds", e.message_vi)
    flags = dict(user.flags or {})
    flags["furnace"] = nxt["level"]
    user.flags = flags
    await db.flush()
    from . import achievements   # Thành Tựu: the furnace level
    await achievements.on_event(db, user.id, "furnace", level=nxt["level"])
    return {"furnace": nxt["level"], **(await overview(db, user))}
