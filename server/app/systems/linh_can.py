"""Linh căn (spirit roots): what a cultivator is born with, tested at the Trắc Linh Thạch and
re-rolled with tẩy linh pills (data/linh_can.json, docs/LINH_CAN.md).

* **Nine giai**, Phàm to Hỗn Độn. Every root has a giai, elements (hệ), a kind (loại) and a
  list of effects; the first effect is its primary one. Every effect type is applied by the
  server at the place SITES names, and validate() refuses a type that is not there.
* **The first test is free** (POST /linh-can/awaken): every player gets a root early. Later
  tests eat one tẩy linh pill (brewed at the furnace from its đan phương and materials). The
  roll lands in `pending`; the player keeps the old root or takes the new one before the
  next roll (POST /linh-can/choose).
* **Odds and caps.** Each pill has its own odds over the giai; the player's cultivation realm
  caps the giai (a roll above it is drawn again inside the cap). Each pill keeps a pity
  counter: after `every - 1` rolls in a row below its floor, the next is at least the floor.
* **Effects reach the live world through the stats.** cultivation.current_stats() calls
  apply_stats(): the flat stat effects (công, thủ, sinh lực, linh lực, bạo kích) change the
  numbers, and the rest ride along as stats["lc_fx"] = {type: value}, with stats["lc"] = the
  giai index (0 = none). The realtime Player keeps its stats, so fx(p, type) reads them in
  the tick; the database side (quiz, alchemy, death) reads value_db().
"""
from __future__ import annotations

import json
import random
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import DATA_DIR
from ..models import Character, LinhCan, User
from . import catalog, inventory, items

FILE = DATA_DIR / "linh_can.json"
PILL_EFFECT = "linh_can"
MIN_ROOTS = 48
STAT_PCT = {"atk_pct": "atk", "def_pct": "def", "hp_pct": "max_hp", "qi_pct": "max_qi"}
STAT_FLAT = {"crit": "crit"}
CHIEU = ("kim", "moc", "thuy", "hoa", "tho", "loi")

# every effect type -> where the server applies it (validate() keeps data and code in step;
# docs/LINH_CAN.md repeats this table)
SITES: dict[str, str] = {
    "atk_pct": "systems/linh_can.apply_stats (cultivation.current_stats)",
    "def_pct": "systems/linh_can.apply_stats (cultivation.current_stats)",
    "hp_pct": "systems/linh_can.apply_stats (cultivation.current_stats)",
    "qi_pct": "systems/linh_can.apply_stats (cultivation.current_stats)",
    "crit": "systems/linh_can.apply_stats (cultivation.current_stats)",
    "xp_pct": "learning/quiz.answer (Tu Vi of a right answer)",
    "q_time": "learning/quiz.create_session (question time limit)",
    "basic_dmg": "realtime/combat.attack (a normal hit)",
    "parry_dmg": "realtime/combat._parry (the counter hit)",
    "stun_pct": "realtime/combat._parry (the stun)",
    "qi_gain": "realtime/combat._parry (linh lực gained)",
    "heal_right": "realtime/combat._parry (healed on a Phản Đòn)",
    "wrong_guard": "realtime/combat._parry (the blow of a wrong answer)",
    "dodge_cd": "realtime/combat.dodge_cooldown",
    "qi_regen": "realtime/combat.tick (linh lực regeneration)",
    "death_guard": "realtime/combat._death_penalty",
    "drop_luck": "realtime/combat._loot_bonus (drop_mult)",
    "stones_pct": "realtime/combat._loot_bonus (stones_pct)",
    "chieu_kim": "systems/math_skills._land (chiêu damage by element)",
    "chieu_moc": "systems/math_skills._land (chiêu damage by element)",
    "chieu_thuy": "systems/math_skills._land (chiêu damage by element)",
    "chieu_hoa": "systems/math_skills._land (chiêu damage by element)",
    "chieu_tho": "systems/math_skills._land (chiêu damage by element)",
    "chieu_loi": "systems/math_skills._land (chiêu damage by element)",
    "chieu_cd": "systems/math_skills (cooldown of a cast)",
    "qi_cost": "systems/math_skills (linh lực of a cast)",
    "glide_cd": "realtime/abilities.request_glide (Đạp Kiếm Lướt cooldown)",
    "tran_time": "realtime/abilities.place_formation (how long the formation stands)",
    "tame": "realtime/beasts.on_parry (Phản Đòn needed to tame)",
    "alchemy_zone": "systems/alchemy.start (văn hỏa zone width)",
    "alchemy_extra": "systems/alchemy.finish (chance of one more pill)",
}
UNITS = ("pct", "point", "sec", "count")


class LinhCanError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the data
@lru_cache(maxsize=1)
def data() -> dict:
    return json.loads(FILE.read_text("utf-8"))


def giai_list() -> list[dict]:
    return data()["giai"]


def giai_ids() -> list[str]:
    return [g["id"] for g in giai_list()]


def giai_index(gid: str | None) -> int:
    """1..9 for a giai id, 0 for none."""
    ids = giai_ids()
    return ids.index(gid) + 1 if gid in ids else 0


def giai_info(gid: str) -> dict:
    return next(g for g in giai_list() if g["id"] == gid)


def roots() -> dict[str, dict]:
    return data()["roots"]


def pills() -> dict[str, dict]:
    return data()["pills"]


def effect_types() -> dict[str, dict]:
    return data()["effect_types"]


def effects_of(root_id: str | None) -> dict[str, float]:
    """{type: value} of a root (values of one type add up); {} for none."""
    r = roots().get(root_id or "")
    out: dict[str, float] = {}
    for e in (r or {}).get("effects", []):
        out[e["type"]] = out.get(e["type"], 0.0) + float(e["value"])
    return out


def effect_text(etype: str, value: float) -> str:
    et = effect_types()[etype]
    unit = et["unit"]
    if unit == "pct":
        v = f"{round(value * 100, 1):g}%"
    elif unit == "sec":
        v = f"{value:g} giây"
    elif unit == "point":
        v = f"{value:g} điểm"
    else:
        v = f"{int(value)}"
    return et["text_vi"].replace("{v}", v)


def root_view(root_id: str | None) -> dict | None:
    r = roots().get(root_id or "")
    if r is None:
        return None
    g = giai_info(r["giai"])
    d = data()
    return {"id": root_id, "name_vi": r["name_vi"], "giai": r["giai"], "giai_index": giai_index(r["giai"]),
            "giai_vi": g["name_vi"], "color": g["color"], "he": list(r["he"]),
            "he_vi": [d["he_vi"][h] for h in r["he"]], "loai": r["loai"], "loai_vi": d["loai_vi"][r["loai"]],
            "effects": [{"type": e["type"], "value": e["value"], "text_vi": effect_text(e["type"], e["value"])}
                        for e in r["effects"]],
            "effects_vi": [effect_text(e["type"], e["value"]) for e in r["effects"]],
            "desc_vi": r["desc_vi"], "lore_vi": r["lore_vi"]}


def brief(root_id: str | None) -> dict | None:
    """What /cultivation carries: {id, name_vi, giai, giai_vi, color, effects_vi} or None."""
    v = root_view(root_id)
    if v is None:
        return None
    return {k: v[k] for k in ("id", "name_vi", "giai", "giai_index", "giai_vi", "color", "effects_vi")}


# ------------------------------------------------------------------ effects in the world
def fx(p, etype: str) -> float:
    """The value of one effect for a realtime Player (or a stats dict); 0 without a root."""
    stats = p if isinstance(p, dict) else (getattr(p, "stats", None) or {})
    return float((stats.get("lc_fx") or {}).get(etype, 0.0))


def chieu_mult(p, element: str | None) -> float:
    """1 + the bonus of a chiêu of this element (chieu_<element>)."""
    return 1.0 + fx(p, f"chieu_{element}") if element in CHIEU else 1.0


def apply_stats(out: dict, root_id: str | None) -> dict:
    """Fold a root into the stats of cultivation.stats_for(): the flat stat effects change the
    numbers, the others ride along in out["lc_fx"]; out["lc"] is the giai index (0 = none)."""
    eff = effects_of(root_id)
    for etype, key in STAT_PCT.items():
        if eff.get(etype) and key in out:
            out[key] = int(round(out[key] * (1 + eff[etype])))
    for etype, key in STAT_FLAT.items():
        if eff.get(etype):
            out[key] = round(out.get(key, 0) + eff[etype], 1)
    r = roots().get(root_id or "")
    out["lc"] = giai_index(r["giai"]) if r else 0
    out["lc_fx"] = {k: v for k, v in eff.items() if k not in STAT_PCT and k not in STAT_FLAT}
    return out


async def root_of(db: AsyncSession, user_id: int) -> str | None:
    row = await db.get(LinhCan, user_id)
    return row.root_id if row is not None else None


async def value_db(db: AsyncSession, user_id: int, etype: str) -> float:
    """One effect of a player's root, read from the database (quiz, alchemy, death)."""
    return float(effects_of(await root_of(db, user_id)).get(etype, 0.0))


# ------------------------------------------------------------------ caps and odds
def _tier(t: str):
    from . import loot
    return loot.parse(t)


def cap_index(realm: str, stage: int) -> int:
    """The highest giai (1..9) a player at this cultivation tier may roll."""
    from . import loot
    me = loot.rank(realm, stage)
    best = 1
    for c in data()["caps"]:
        if me >= _tier(c["from"]):
            best = max(best, giai_index(c["giai"]))
    return best


def opens_at(gid: str) -> str | None:
    """'Luyện Khí tầng 4'...: the tu vi at which a giai opens (None: open from the start)."""
    from . import loot
    i = giai_index(gid)
    for c in data()["caps"]:
        if giai_index(c["giai"]) >= i:
            t = _tier(c["from"])
            return None if t == _tier("pham_nhan") else loot.label(t)
    return None


def odds_list(odds: dict) -> list[float]:
    return [float(odds.get(g, 0.0)) for g in giai_ids()]


def capped(odds: dict, cap: int, floor: int = 1) -> list[float]:
    """The odds over giai 1..9 restricted to floor..cap and renormalised. No mass left inside
    the window: everything on the nearest edge (the cap when the pill aims above it, the floor
    when it aims below)."""
    p = odds_list(odds)
    floor = min(floor, cap)
    w = [x if floor <= i + 1 <= cap else 0.0 for i, x in enumerate(p)]
    s = sum(w)
    if s <= 0:
        above = sum(x for i, x in enumerate(p) if i + 1 > cap)
        edge = cap if above > 0 else floor
        return [1.0 if i + 1 == edge else 0.0 for i in range(len(p))]
    return [x / s for x in w]


def draw_giai(rng: random.Random, odds: dict, cap: int, floor: int = 1) -> int:
    w = capped(odds, cap, floor)
    r = rng.random()
    acc = 0.0
    last = 1
    for i, x in enumerate(w):
        if x <= 0:
            continue
        last = i + 1
        acc += x
        if r < acc:
            return i + 1
    return last


def draw_root(rng: random.Random, giai: int) -> str:
    gid = giai_ids()[giai - 1]
    pool = [(rid, float(r.get("weight", 1))) for rid, r in roots().items() if r["giai"] == gid]
    total = sum(w for _, w in pool)
    x = rng.random() * total
    for rid, w in pool:
        x -= w
        if x < 0:
            return rid
    return pool[-1][0]


# ------------------------------------------------------------------ the player
async def _row(db: AsyncSession, user_id: int, create: bool = False) -> LinhCan | None:
    row = await db.get(LinhCan, user_id)
    if row is None and create:
        row = LinhCan(user_id=user_id, root_id=None, pending_id=None, pending_pill=None, pity={}, rolls=0,
                      discovered=[], awakened_at=None, updated_at=clock.now())
        db.add(row)
        await db.flush()
    return row


async def _character(db: AsyncSession, user_id: int) -> Character:
    ch = await db.get(Character, user_id)
    if ch is None:
        raise LinhCanError(404, "no_character", "Bạn chưa tạo nhân vật.")
    return ch


def _discover(row: LinhCan, root_id: str) -> None:
    seen = list(row.discovered or [])
    if root_id not in seen:
        seen.append(root_id)
        row.discovered = seen


async def _after_change(db: AsyncSession, ch: Character) -> dict:
    """The root changed: the body follows (max hp), the live world gets the new stats, and
    whoever sees this player gets their entity again (its `lc` mark)."""
    from . import cultivation
    st = await cultivation.current_stats(db, ch)
    ch.max_hp = st["max_hp"]
    ch.hp = min(ch.hp, st["max_hp"])
    ch.qi = min(ch.qi, st["max_qi"])
    await cultivation.push_to_world(db, ch)
    _reshow(ch.user_id)
    return st


def _reshow(user_id: int) -> None:
    from ..realtime.world import world
    p = world.players.get(user_id)
    if p is None or p.channel is None:
        return
    for other in p.channel.players.values():
        other.known.pop(p.eid, None)


def pill_odds_view(pid: str, cap: int, count: int = 0) -> dict:
    pdef = pills()[pid]
    pity = pdef.get("pity") or {}
    floor = giai_index(pity.get("floor")) if pity else 0
    eff_floor = min(floor, cap) if floor else 0
    w = capped(pdef["odds"], cap)
    every = int(pity.get("every", 0)) if pity else 0
    return {"id": pid, "name_vi": catalog.item_name(pid), "desc_vi": (catalog.stack_item(pid) or {}).get("desc_vi", ""),
            "odds": [{"giai": g, "p": round(x, 6)} for g, x in zip(giai_ids(), w) if x > 0],
            "base_odds": [{"giai": g, "p": float(pdef["odds"].get(g, 0))} for g in giai_ids()
                          if pdef["odds"].get(g, 0) > 0],
            "pity": ({"every": every, "floor": giai_ids()[eff_floor - 1], "floor_vi": giai_info(giai_ids()[eff_floor - 1])["name_vi"],
                      "count": count, "left": max(1, every - count)} if every else None)}


async def view(db: AsyncSession, user: User) -> dict:
    ch = await _character(db, user.id)
    row = await _row(db, user.id)
    cap = cap_index(ch.realm, ch.realm_stage)
    stacks = await items.stacks(db, user.id)
    seen = set(row.discovered or []) if row else set()
    pill_rows = []
    for pid in pills():
        v = pill_odds_view(pid, cap, int(((row.pity if row else None) or {}).get(pid, 0)))
        v["have"] = stacks.get(pid, 0)
        r = catalog.recipes().get(pid) or {}
        v["recipe_item"] = r.get("item")
        v["recipe_vi"] = catalog.item_name(r["item"]) if r.get("item") else ""
        v["know_recipe"] = stacks.get(r.get("item") or "", 0) > 0
        pill_rows.append(v)
    giai = []
    for g in giai_list():
        i = giai_index(g["id"])
        giai.append({"id": g["id"], "index": i, "name_vi": g["name_vi"], "color": g["color"],
                     "open": i <= cap, "need_vi": opens_at(g["id"]) if i > cap else None,
                     "count": sum(1 for r in roots().values() if r["giai"] == g["id"])})
    book = []
    for rid, r in roots().items():
        e = {"id": rid, "giai": r["giai"], "giai_index": giai_index(r["giai"]), "discovered": rid in seen}
        if rid in seen:
            e.update(root_view(rid))
        book.append(e)
    book.sort(key=lambda e: e["giai_index"])
    return {"awakened": bool(row and row.root_id),
            "root": root_view(row.root_id if row else None),
            "pending": root_view(row.pending_id if row else None),
            "pending_pill": row.pending_pill if row else None,
            "rolls": row.rolls if row else 0,
            "cap": {"giai": giai_ids()[cap - 1], "index": cap, "name_vi": giai_list()[cap - 1]["name_vi"]},
            "giai": giai, "pills": pill_rows,
            "awaken_odds": [{"giai": g, "p": round(x, 6)} for g, x in
                            zip(giai_ids(), capped(data()["awaken"]["odds"], cap)) if x > 0],
            "book": book, "discovered": len(seen), "total": len(roots())}


async def awaken(db: AsyncSession, user: User, rng: random.Random | None = None) -> dict:
    """The free first test at the Trắc Linh Thạch."""
    rng = rng or random.Random()
    ch = await _character(db, user.id)
    row = await _row(db, user.id, create=True)
    if row.root_id:
        raise LinhCanError(400, "already_awakened", "Con đã trắc linh rồi. Muốn đổi linh căn thì cần đan tẩy linh.")
    cap = cap_index(ch.realm, ch.realm_stage)
    rid = draw_root(rng, draw_giai(rng, data()["awaken"]["odds"], cap))
    now = clock.now()
    row.root_id, row.awakened_at, row.updated_at = rid, now, now
    row.rolls = int(row.rolls or 0) + 1
    _discover(row, rid)
    await _after_change(db, ch)
    return {"root": root_view(rid), "first": True, "view": await view(db, user)}


async def roll(db: AsyncSession, user: User, pill: str, rng: random.Random | None = None) -> dict:
    """One tẩy linh pill: draw a root (odds of the pill, inside the realm's cap, pity), keep it
    pending until the player chooses. The same root as the one carried is kept at once."""
    rng = rng or random.Random()
    if pill not in pills():
        raise LinhCanError(404, "no_pill", "Không có đan tẩy linh này.")
    ch = await _character(db, user.id)
    row = await _row(db, user.id)
    if row is None or not row.root_id:
        raise LinhCanError(400, "not_awakened", "Con chưa trắc linh lần nào. Lần đầu đặt tay lên Trắc Linh Thạch là miễn phí.")
    if row.pending_id:
        raise LinhCanError(400, "pending_choice", "Linh căn vừa trắc còn chờ con chọn giữ hay đổi.")
    try:
        await inventory.consume_item(db, user.id, pill, 1, "linh_can", None)
    except inventory.InsufficientFunds:
        raise LinhCanError(400, "no_pill", f"Con không có {catalog.item_name(pill)}. Luyện ở lò đan từ đan phương của nó.")
    pdef = pills()[pill]
    cap = cap_index(ch.realm, ch.realm_stage)
    pity = dict(row.pity or {})
    count = int(pity.get(pill, 0))
    pity_def = pdef.get("pity") or {}
    floor = min(giai_index(pity_def.get("floor")), cap) if pity_def else 0
    forced = bool(pity_def) and count + 1 >= int(pity_def["every"])
    giai = draw_giai(rng, pdef["odds"], cap, floor if forced else 1)
    pity[pill] = 0 if (floor and giai >= floor) else count + 1
    row.pity = pity
    row.rolls = int(row.rolls or 0) + 1
    rid = draw_root(rng, giai)
    _discover(row, rid)
    row.updated_at = clock.now()
    same = rid == row.root_id
    if not same:
        row.pending_id, row.pending_pill = rid, pill
    return {"rolled": root_view(rid), "same": same, "pity_hit": forced and giai >= floor,
            "old": root_view(row.root_id), "view": await view(db, user)}


async def choose(db: AsyncSession, user: User, keep: bool) -> dict:
    """Resolve the pending root: keep the old one, or take the new one."""
    ch = await _character(db, user.id)
    row = await _row(db, user.id)
    if row is None or not row.pending_id:
        raise LinhCanError(400, "no_pending", "Không có linh căn nào đang chờ chọn.")
    took = not keep
    if took:
        row.root_id = row.pending_id
    row.pending_id, row.pending_pill = None, None
    row.updated_at = clock.now()
    if took:
        await _after_change(db, ch)
    return {"root": root_view(row.root_id), "took": took, "view": await view(db, user)}


# ------------------------------------------------------------------ the checks
def validate(raw: dict | None = None) -> list[str]:
    """Problems of data/linh_can.json and of the pills it names (empty = sound)."""
    from . import loot
    d = raw if raw is not None else data()
    out: list[str] = []
    gids = [g.get("id") for g in d.get("giai", [])]
    if len(gids) != 9 or len(set(gids)) != 9:
        out.append("giai: need nine distinct giai")
    for g in d.get("giai", []):
        if not g.get("name_vi") or not str(g.get("color", "")).startswith("#"):
            out.append(f"giai.{g.get('id')}: name_vi and a #colour are needed")
    et = d.get("effect_types", {})
    for t, e in et.items():
        if t not in SITES:
            out.append(f"effect_types.{t}: the server does not apply it (not in linh_can.SITES)")
        if e.get("unit") not in UNITS:
            out.append(f"effect_types.{t}: unit must be one of {', '.join(UNITS)}")
        if "{v}" not in str(e.get("text_vi", "")):
            out.append(f"effect_types.{t}: text_vi must show the value {{v}}")
    for t in SITES:
        if t not in et:
            out.append(f"linh_can.SITES.{t}: no effect_types entry")
    rs = d.get("roots", {})
    if len(rs) < MIN_ROOTS:
        out.append(f"roots: {len(rs)} roots, at least {MIN_ROOTS}")
    names: dict[str, str] = {}
    used: set[str] = set()
    primary: dict[tuple[str, str], str] = {}
    for rid, r in rs.items():
        where = f"roots.{rid}"
        if r.get("giai") not in gids:
            out.append(f"{where}: giai {r.get('giai')!r} unknown")
            continue
        if r.get("name_vi") in names:
            out.append(f"{where}: name {r.get('name_vi')!r} also used by {names[r['name_vi']]}")
        names[r.get("name_vi")] = rid
        for h in r.get("he", []):
            if h not in d.get("he_vi", {}):
                out.append(f"{where}: hệ {h!r} unknown")
        if r.get("loai") not in d.get("loai_vi", {}):
            out.append(f"{where}: loại {r.get('loai')!r} unknown")
        if not r.get("desc_vi") or not r.get("lore_vi"):
            out.append(f"{where}: desc_vi and lore_vi are needed")
        effs = r.get("effects") or []
        if not effs:
            out.append(f"{where}: no effect")
            continue
        for e in effs:
            t = e.get("type")
            if t not in et:
                out.append(f"{where}: effect {t!r} unknown")
                continue
            used.add(t)
            v = e.get("value")
            if not isinstance(v, (int, float)) or v <= 0 or v > et[t]["cap"]:
                out.append(f"{where}: {t} = {v!r} must be > 0 and <= {et[t]['cap']}")
        key = (r["giai"], effs[0].get("type"))
        if key in primary:
            out.append(f"{where}: primary effect {key[1]} already the primary of {primary[key]} in {key[0]}")
        primary[key] = rid
    for g in gids:
        n = sum(1 for r in rs.values() if r.get("giai") == g)
        if n == 0:
            out.append(f"giai {g}: no root")
    counts = [sum(1 for r in rs.values() if r.get("giai") == g) for g in gids]
    if counts and counts[-1] > counts[0]:
        out.append("roots: the top giai must hold fewer roots than the bottom one")
    for t in et:
        if t not in used:
            out.append(f"effect_types.{t}: no root carries it")
    # higher giai, bigger numbers: as a primary effect, a type is never weaker at a higher giai
    best: dict[str, list[tuple[int, float]]] = {}
    for r in rs.values():
        e = (r.get("effects") or [{}])[0]
        if e.get("type") in et and r.get("giai") in gids:
            best.setdefault(e["type"], []).append((gids.index(r["giai"]), float(e["value"])))
    for t, vals in best.items():
        top_by_giai: dict[int, float] = {}
        for gi, v in vals:
            top_by_giai[gi] = max(top_by_giai.get(gi, 0.0), v)
        seq = [top_by_giai[k] for k in sorted(top_by_giai)]
        if any(b < a for a, b in zip(seq, seq[1:])):
            out.append(f"effect {t}: as a primary effect it gets weaker as the giai rises {seq}")
    # caps: data-driven, every realm is covered and the giai only rise
    caps = d.get("caps", [])
    if not caps or caps[0].get("from") != "pham_nhan":
        out.append("caps: the first entry must start at pham_nhan")
    prev_t, prev_g = None, 0
    for c in caps:
        try:
            t = loot.parse(c.get("from"))
        except ValueError as e:
            out.append(f"caps: {e}")
            continue
        gi = gids.index(c["giai"]) + 1 if c.get("giai") in gids else 0
        if not gi:
            out.append(f"caps: giai {c.get('giai')!r} unknown")
        if prev_t is not None and (t <= prev_t or gi <= prev_g):
            out.append(f"caps: {c} must come after a lower tier and open a higher giai")
        prev_t, prev_g = t, gi
    if caps and caps[-1].get("giai") != gids[-1]:
        out.append("caps: the last entry must open the top giai")
    # odds, pity, the pills and how to get them
    def odds_ok(where: str, odds: dict) -> None:
        if any(g not in gids for g in odds):
            out.append(f"{where}: a giai of the odds is unknown")
        if any(not isinstance(x, (int, float)) or x < 0 for x in odds.values()):
            out.append(f"{where}: odds must be >= 0")
        if abs(sum(odds.values()) - 1.0) > 1e-6:
            out.append(f"{where}: odds sum to {sum(odds.values())}, not 1")
    odds_ok("awaken", d.get("awaken", {}).get("odds", {}))
    ps = d.get("pills", {})
    if len(ps) < 4:
        out.append("pills: at least four tẩy linh pills")
    tiers = loot.data().get("items", {})
    got = _obtainable()
    prev_mean = -1.0
    for pid, p in ps.items():
        where = f"pills.{pid}"
        odds_ok(where, p.get("odds", {}))
        mean = sum((gids.index(g) + 1) * x for g, x in p.get("odds", {}).items() if g in gids)
        if mean <= prev_mean:
            out.append(f"{where}: a better pill must shift the odds upward (mean giai {mean:.2f})")
        prev_mean = mean
        pity = p.get("pity")
        if pity is not None and (pity.get("floor") not in gids or not isinstance(pity.get("every"), int)
                                 or pity["every"] < 2):
            out.append(f"{where}: pity needs a giai floor and every >= 2")
        info = catalog.pills().get(pid)
        if info is None or info.get("effect") != PILL_EFFECT:
            out.append(f"{where}: not a pill of items/pills.json with effect {PILL_EFFECT}")
        if pid not in tiers:
            out.append(f"{where}: no tier in loot_tiers.json")
        rec = catalog.recipes().get(pid)
        if rec is None:
            out.append(f"{where}: no recipe in recipes.json")
            continue
        if rec["item"] not in got:
            out.append(f"{where}: its đan phương {rec['item']} is sold or dropped nowhere")
        if rec["item"] not in tiers:
            out.append(f"{where}: its đan phương {rec['item']} has no tier in loot_tiers.json")
        if not rec.get("min_realm") or not rec.get("fee"):
            out.append(f"{where}: the recipe needs a min_realm and a fee")
        for ing in rec["ingredients"]:
            if ing["kind"] != "item":
                continue
            if ing["item"] not in got:
                out.append(f"{where}: ingredient {ing['item']} is handed out nowhere")
            if ing["item"] not in tiers:
                out.append(f"{where}: ingredient {ing['item']} has no tier in loot_tiers.json")
    for pid, info in catalog.pills().items():
        if info.get("effect") == PILL_EFFECT and pid not in ps:
            out.append(f"items/pills.json {pid}: a linh căn pill without odds in linh_can.json")
    return out


def _obtainable() -> set[str]:
    """Every item monsters drop, the shop sells or the library shelf sells."""
    from .. import balance
    got: set[str] = set()
    for m in catalog.monsters().values():
        got |= {d["item"] for d in m.get("drops", []) if "item" in d}
    got |= {s["item"] for s in balance.load("shop")["stock"]}
    got |= set(balance.load("books").get("shop", {}))
    return got
