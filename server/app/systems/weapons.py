"""Binh khí của Thiên Địa Đồ: the weapons lying in the lands, dropping from their creatures and
raised at the forge (world_plan.json, wired sections `weapons` and `weapon_drops`).

The plan names the weapon types (`weapon_types`: one main type per curriculum branch, plus the
kỳ binh - drop-only types of a land), a grade per realm (`grades`), five qualities
(`qualities`: hạ, trung, thượng, cực, tuyệt), the spots where weapons lie (`weapons_placed`)
and what the creatures of a land drop (`weapon_drops`). This module turns that into rules, and
fits them into the equipment the game already has instead of building a second inventory
beside it:

  * a weapon is `<type>_<grade>` (kiem_1 = Mộc Kiếm). Every weapon that is placed somewhere or
    can drop becomes a piece of equipment of slot `weapon` in `catalog.equipment()`
    (equipment_items), whose `kind` is the weapon id itself - so the stats the world reads
    (`stats.weapon`), the fight profile and the layer drawn in the hand all follow the weapon,
    grade included;
  * a type's `status` is "co" (in the game) or "cho_hinh" (waiting for its art): a cho_hinh
    type is plan data only - never placed, never dropped, not equipment. Flipping it to "co"
    is the only change needed once its art is in (tools/check_all.py then demands the art);
  * a quality is stored as the equipment rarity it maps to (QUALITY_RARITY: hạ = Phàm,
    trung = Linh, thượng = Huyền, cực = Địa, tuyệt = Thiên - also the colour a drop glows
    in), so the bag, the shop, Bảo Vật Phổ and the enhance forge treat the piece like any
    other; its power is the plan's own number (`power`), not the rarity multiplier
    (cultivation.instance_stats reads `power_by_rarity`);
  * a spot gives its weapon once per player (`WeaponClaim`), only when the player's place in
    Đạo Thụ - "tu vi" in the plan - reaches its realm and stage and every node it names is
    done, and when its land is open and the ability it needs exists;
  * a creature of a land drops that land's weapons (roll_drops, called by
    realtime/combat._reward): a chance by rank, odds over the qualities by rank, the grade of
    the land's realm. The loot rule holds (systems/loot.py): the quality is capped by the
    killer's cultivation tu vi and by the cap of the place of the kill, and a roll the
    player's tu vi blocks is reported as locked;
  * the fight: the type decides the normal attack (range, cooldown, multiplier) and the
    animation clip; the weapon's Công is the grade's `atk` times the quality's `power`; a
    Phản Đòn on a question of the weapon's own branch hits harder (`weapons` block of the
    plan, parry_mult);
  * Rèn nâng phẩm: at the forge, a weapon goes up one quality per step of the chain of
    crafting.json `upgrades` (hạ -> trung -> thượng -> cực -> tuyệt), each step for materials
    that really drop, a fee, a stage of Đạo Thụ and a cultivation tu vi.
"""
from __future__ import annotations

import random
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..learning import math_tree
from ..models import AuditLog, EquipmentInstance, User, WeaponClaim
from . import catalog, inventory

AVAILABLE, TAKEN, LOCKED = "available", "taken", "locked"
CLIPS = ("slash", "cast", "shoot")
STATUSES = ("co", "cho_hinh")
RANKS = ("normal", "elite", "boss")
# a contract with the artist and the VFX programmer: the quality ids and the equipment rarity
# each is stored as (the colour a dropped piece glows in is that rarity's colour)
QUALITY_RARITY = {"ha": "pham", "trung": "linh", "thuong": "huyen", "cuc": "dia", "tuyet": "thien"}
# where the pieces of one kill lie around the spot the monster died, in pixels
SCATTER = ((0, 0), (10, 4), (-10, 4), (6, -8), (-6, -8))


class WeaponError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the plan, as tables
@lru_cache(maxsize=1)
def data() -> dict:
    plan = math_tree.world_plan()
    placed = []
    for p in plan.get("weapons_placed", []):
        placed.append({**p, "id": placed_id(p)})
    return {"plan": plan,
            "cfg": plan.get("weapons", {}),
            "drops": plan.get("weapon_drops", {}),
            "grades": {g["grade"]: g for g in plan.get("grades", [])},
            "qualities": {q["id"]: q for q in plan.get("qualities", [])},
            "types": {t["id"]: t for t in plan.get("weapon_types", [])},
            "lands": {land["id"]: land for land in plan.get("lands", [])},
            "unlocks": {u["id"]: u for u in plan.get("unlocks", [])},
            "placed": placed,
            "by_id": {p["id"]: p for p in placed}}


def clear_cache() -> None:
    data.cache_clear()
    catalog.equipment.cache_clear()


def placed_id(p: dict) -> str:
    """The id of a spot: its own `id` when the plan gives one, else '<weapon>_<quality>'
    (unique: the tree checker refuses a quality placed twice)."""
    return p.get("id") or f"{p['weapon']}_{p['quality']}"


def split(weapon_id: str | None) -> tuple[str, int] | None:
    """'ho_lo_2' -> ('ho_lo', 2); None for anything that is not a weapon of the plan."""
    kind, _, grade = str(weapon_id or "").rpartition("_")
    if kind in data()["types"] and grade.isdigit() and int(grade) in data()["grades"]:
        return kind, int(grade)
    return None


def is_weapon(weapon_id: str | None) -> bool:
    return split(weapon_id) is not None


def type_live(kind: str) -> bool:
    """A type that is in the game: status 'co'. A 'cho_hinh' type waits for its art."""
    return data()["types"].get(kind, {}).get("status") == "co"


def weapon_name(weapon_id: str) -> str:
    kind, grade = split(weapon_id)
    return f"{data()['grades'][grade]['prefix_vi']} {data()['types'][kind]['name_vi']}"


def quality_of_rarity(rarity: str) -> dict | None:
    return next((q for q in data()["qualities"].values() if q.get("rarity") == rarity), None)


def quality_order() -> list[str]:
    return list(data()["qualities"])


def qualities_view() -> list[dict]:
    """Every quality with the name, colour and power the client shows."""
    rar = catalog.equipment()["rarities"]
    return [{"id": q["id"], "name_vi": q["name_vi"], "rarity": q["rarity"], "power": float(q["power"]),
             "color": rar.get(q["rarity"], {}).get("color")} for q in data()["qualities"].values()]


def branch_name(branch: str) -> str:
    b = next((x for x in math_tree.tree().raw.get("branches", []) if x["id"] == branch), None)
    return b["name_vi"] if b else branch


def branch_subject(branch: str) -> str | None:
    b = next((x for x in math_tree.tree().raw.get("branches", []) if x["id"] == branch), None)
    return b.get("subject") if b else None


def effect_vi(weapon_id: str) -> str:
    """What the weapon does in a fight, in one line."""
    kind, _ = split(weapon_id)
    t = data()["types"][kind]
    cfg = data()["cfg"]
    subject = branch_subject(t["branch"])
    if subject:
        bonus = int(round(float(cfg.get("own_branch_parry_bonus", 0)) * 100))
        parry = f"Phản Đòn câu {branch_name(t['branch'])} mạnh thêm {bonus}%."
    else:
        bonus = int(round(float(cfg.get("any_branch_parry_bonus", 0)) * 100))
        parry = f"Phản Đòn mọi câu mạnh thêm {bonus}%."
    cooldown = f"{float(t['cooldown']):g}".replace(".", ",")
    return f"Tầm đánh {t['range']}, mỗi đòn {cooldown} giây. {parry}"


def equipment_items() -> dict[str, dict]:
    """Every weapon of a live type that lies somewhere or can drop, as a piece of equipment
    (merged into catalog.equipment()). Its `atk` is the grade's; `power_by_rarity` holds the
    quality powers by the rarity each quality is stored as."""
    d = data()
    power = {q["rarity"]: float(q["power"]) for q in d["qualities"].values() if q.get("rarity")}
    out = {}
    for wid in [p["weapon"] for p in d["placed"]] + sorted(droppable_weapons()):
        if wid in out or not is_weapon(wid):
            continue
        kind, grade = split(wid)
        if not type_live(kind):
            continue
        t = d["types"][kind]
        out[wid] = {"name_vi": weapon_name(wid), "slot": "weapon", "kind": wid, "weapon_type": kind,
                    "grade": grade, "stats": {"atk": int(d["grades"][grade]["atk"])},
                    "power_by_rarity": power, "desc_vi": t.get("why_vi", "")}
    return out


# ------------------------------------------------------------------ the fight
def fight_profile(weapon_id: str | None) -> dict | None:
    """The normal attack of a plan weapon, shaped like combat.json's weapon_kinds."""
    s = split(weapon_id)
    if s is None:
        return None
    t = data()["types"][s[0]]
    return {"name_vi": t["name_vi"], "range": float(t["range"]), "cooldown": float(t["cooldown"]),
            "mult": float(t.get("mult", 1.0)), "clip": t["clip"]}


def parry_mult(weapon_id: str | None, subject_id: str | None) -> float:
    """How much harder a Phản Đòn hits with this weapon on a question of this subject: the
    weapon's own branch gets `own_branch_parry_bonus`; a weapon whose branch has no math subject
    of its own (Lập Trình, Thực Chiến, Học Máy, Học Sâu) gets `any_branch_parry_bonus` on every
    question. 1.0 without a plan weapon."""
    s = split(weapon_id)
    if s is None:
        return 1.0
    cfg = data()["cfg"]
    own = branch_subject(data()["types"][s[0]]["branch"])
    if own is None:
        return 1.0 + float(cfg.get("any_branch_parry_bonus", 0))
    if subject_id and subject_id == own:
        return 1.0 + float(cfg.get("own_branch_parry_bonus", 0))
    return 1.0


# ------------------------------------------------------------------ drops from monsters
def drops_wired() -> bool:
    return math_tree.section_wired("weapon_drops", data()["plan"])


def realm_grade(realm: str | None) -> int | None:
    return next((g for g, x in data()["grades"].items() if x.get("realm") == realm), None)


def land_table(land_id: str | None) -> dict | None:
    """What the creatures of a land drop: {"main": [types], "ky_binh": [types], "grades":
    [{"grade", "weight", "tu_vi"?}]}, live types only. A land's main types are the types whose
    `land` it is and that are not drop_only; its kỳ binh the drop_only ones. `weapon_drops.lands`
    may override the types and the grades (the boss arena has no type of its own). None for an
    unknown land."""
    d = data()
    land = d["lands"].get(land_id or "")
    if land is None:
        return None
    over = d["drops"].get("lands", {}).get(land_id, {})
    own = [k for k, t in d["types"].items() if t.get("land") == land_id]
    main = over.get("types") if "types" in over else [k for k in own if not d["types"][k].get("drop_only")]
    ky = over.get("ky_binh") if "ky_binh" in over else [k for k in own if d["types"][k].get("drop_only")]
    g = realm_grade(land.get("realm"))
    grades = over.get("grades") or ([{"grade": g, "weight": 1}] if g is not None else [])
    return {"main": [k for k in main if type_live(k)], "ky_binh": [k for k in ky if type_live(k)],
            "grades": grades}


def droppable_weapons() -> set[str]:
    """Every weapon id some creature can drop today."""
    d = data()
    out: set[str] = set()
    for land_id, land in d["lands"].items():
        if land.get("status") != "co":
            continue
        tb = land_table(land_id)
        for kind in tb["main"] + tb["ky_binh"]:
            out |= {f"{kind}_{g['grade']}" for g in tb["grades"]}
    return out


def _weighted(rng: random.Random, pairs: list[tuple[object, float]]):
    total = sum(w for _, w in pairs if w > 0)
    if total <= 0:
        return pairs[0][0] if pairs else None
    x = rng.uniform(0, total)
    for v, w in pairs:
        if w <= 0:
            continue
        x -= w
        if x <= 0:
            return v
    return next(v for v, w in reversed(pairs) if w > 0)


def roll_quality(rng: random.Random, odds: dict[str, float]) -> str:
    return _weighted(rng, [(q, float(odds.get(q, 0))) for q in quality_order()])


def cap_quality(quality: str, realm: str, stage: int, within=None) -> tuple[str | None, str | None]:
    """(the quality granted, the quality to report as locked or None) for a rolled quality.
    The granted one is the best at or below the roll that both the player's cultivation tu vi
    (loot.rarity_cap) and the cap of the place of the kill (`within`, a loot tier) allow. The
    roll is reported as locked only when it is the player's tu vi that held it back: then the
    report names the best quality this place could have given (the roll, or lower), which the
    player will get here by climbing."""
    from . import loot
    from .items import RARITY_ORDER
    order = quality_order()
    q = data()["qualities"]

    def idx(qid: str) -> int:
        return RARITY_ORDER.index(q[qid]["rarity"])

    mine = loot.rarity_cap(realm, stage)
    me = RARITY_ORDER.index(mine) if mine is not None else -1
    src = RARITY_ORDER.index(loot.best_rarity(within) or RARITY_ORDER[0]) if within is not None \
        else len(RARITY_ORDER) - 1
    allowed = min(me, src)
    granted = next((x for x in reversed(order[:order.index(quality) + 1]) if idx(x) <= allowed), None)
    shown = next((x for x in reversed(order[:order.index(quality) + 1]) if idx(x) <= src), None)
    locked = shown if shown is not None and idx(shown) > me else None
    return granted, locked


def roll_drops(rng: random.Random, kind: str, realm: str, stage: int, within=None,
               drop_mult: float = 1.0) -> tuple[list[dict], list[dict]]:
    """The weapons one kill of this monster drops for one player: (grants, locked).
    grants: [{"weapon", "quality", "rarity"}]; locked: [{"name_vi", "need_vi"}] for
    loot.note_locked. Nothing (and no dice thrown) for a monster without a land, a land that
    drops nothing, or when the section is not wired."""
    from . import loot
    if not drops_wired():
        return [], []
    info = catalog.monsters().get(kind, {})
    rank = info.get("rank", "normal")
    tb = land_table(info.get("land"))
    rk = data()["drops"].get("by_rank", {}).get(rank)
    if tb is None or rk is None or not tb["grades"]:
        return [], []
    picks = []
    if tb["main"] and rng.random() < min(1.0, float(rk.get("chance", 0)) * drop_mult):
        picks.append(rng.choice(tb["main"]))
    if tb["ky_binh"] and rank != "normal" \
            and rng.random() < min(1.0, float(rk.get("ky_binh_chance", 0)) * drop_mult):
        picks.append(rng.choice(tb["ky_binh"]))
    grants, locked = [], []
    me = loot.rank(realm, stage)
    open_grades = [g for g in tb["grades"] if not g.get("tu_vi")]
    for wtype in picks:
        g = _weighted(rng, [(x, float(x.get("weight", 1))) for x in tb["grades"]])
        if g.get("tu_vi") and me < loot.parse(g["tu_vi"]):
            locked.append({"name_vi": weapon_name(f"{wtype}_{g['grade']}"), "need_vi": loot.label(loot.parse(g["tu_vi"]))})
            g = min(open_grades, key=lambda x: x["grade"]) if open_grades else None
            if g is None:
                continue
        wid = f"{wtype}_{g['grade']}"
        rolled = roll_quality(rng, rk.get("qualities", {}))
        got, held = cap_quality(rolled, realm, stage, within)
        if held is not None:
            qq = data()["qualities"][held]
            locked.append({"name_vi": f"{weapon_name(wid)} ({qq['name_vi']})",
                           "need_vi": loot.label(loot.rarity_tier(qq["rarity"]))})
        if got is None:
            continue
        grants.append({"weapon": wid, "quality": got, "rarity": data()["qualities"][got]["rarity"]})
    return grants, locked


def ground_entry(view: dict, x: float | None, y: float | None, index: int = 0) -> dict:
    """An `equipment` entry of the `loot` message: the piece as items.equipment_view shows it,
    plus where it lies (the spot the monster died, scattered a little when one kill drops
    several pieces) and what the client needs to draw it glowing in its rarity colour. For a
    weapon of the plan `weapon_info` is the weapon part of the view (type, grade, quality...)."""
    w = view.get("weapon") if isinstance(view.get("weapon"), dict) else None
    dx, dy = SCATTER[index % len(SCATTER)]
    out = {**view, "item": view.get("item_id"), "weapon": view.get("slot") == "weapon",
           "quality": w.get("quality") if w else None, "quality_vi": w.get("quality_vi") if w else None,
           "x": None if x is None else round(float(x) + dx, 1),
           "y": None if y is None else round(float(y) + dy, 1)}
    if w:
        out["weapon_info"] = w
    return out


async def grant_drops(db: AsyncSession, uid: int, kind: str, realm: str, stage: int, within,
                      rng: random.Random, drop_mult: float, out: dict,
                      x: float | None = None, y: float | None = None) -> None:
    """Roll this kill's weapons for one player, grant them like any equipment drop (nothing is
    lost if the player walks away) and add them to the `loot` payload `out`."""
    from . import items
    from . import loot
    grants, locked = roll_drops(rng, kind, realm, stage, within, drop_mult)
    for note in locked:
        loot.note_locked(out, name_vi=note["name_vi"], need=note["need_vi"])
    for g in grants:
        view = await items.grant_equipment(db, uid, g["weapon"], g["rarity"], "weapon_drop", kind)
        eq = out.setdefault("equipment", [])
        eq.append(ground_entry(view, x, y, len(eq)))


# ------------------------------------------------------------------ where the player stands
async def standing(db: AsyncSession, user_id: int) -> tuple[tuple[str, int], set[str]]:
    """(the stage reached in Đạo Thụ, the nodes that count as done). Tu vi in the plan."""
    from . import math_tree_progress
    st = await math_tree_progress.state(db, user_id)
    return st.stage, st.done


def _realm_vi(realm: str) -> str:
    r = next((x for x in math_tree.tree().raw["realms"] if x["id"] == realm), None)
    return r["name_vi"] if r else realm


def reaches(at: tuple[str, int], realm: str, stage: int) -> bool:
    t = math_tree.tree()
    return t.reaches(realm, int(stage), at)


def unlock_open(unlock_id: str, at: tuple[str, int]) -> bool:
    u = data()["unlocks"].get(unlock_id)
    return bool(u) and u.get("status") == "co" and reaches(at, u["realm"], u["stage"])


def _unlock_reason(unlock_id: str) -> str:
    u = data()["unlocks"][unlock_id]
    if u.get("status") != "co":
        return f"Cần {u['name_vi']}: chưa có trong game."
    return f"Cần {u['name_vi']}, mở ở {_realm_vi(u['realm'])} tầng {u['stage']} trên Đạo Thụ."


def missing(p: dict, at: tuple[str, int], done: set[str]) -> list[str]:
    """What the player still lacks for this spot, one Vietnamese sentence each; empty = ready.
    The spot asks its own `requires`, plus its land's `opens`, its `needs` and the claim
    unlock (nhat_vu_khi)."""
    d = data()
    t = math_tree.tree()
    out: list[str] = []
    req = p.get("requires", {})
    land = d["lands"].get(p.get("land"), {})
    opens = land.get("opens", {})
    need_realm, need_stage = req.get("realm", land.get("realm")), int(req.get("stage", 0))
    if land.get("realm") and t.realm_order.get(land["realm"], 0) > t.realm_order.get(need_realm, 0):
        need_realm, need_stage = land["realm"], int(opens.get("stage", 0))
    elif land.get("realm") == need_realm:
        need_stage = max(need_stage, int(opens.get("stage", 0)))
    if need_realm and not reaches(at, need_realm, need_stage):
        out.append(f"Cần {_realm_vi(need_realm)} tầng {need_stage} trên Đạo Thụ "
                   f"(đang ở {_realm_vi(at[0])} tầng {at[1]}).")
    nodes = list(dict.fromkeys(list(req.get("nodes", [])) + list(opens.get("nodes", []))))
    lacking = [n for n in nodes if n not in done]
    if lacking:
        names = ", ".join(t.nodes[n].name_vi if n in t.nodes else n for n in lacking)
        out.append(f"Cần học xong: {names}.")
    claim = d["cfg"].get("claim_unlock")
    if claim and not unlock_open(claim, at) and not out:
        out.append(_unlock_reason(claim))
    for need in filter(None, (land.get("needs"), p.get("needs"))):
        if not unlock_open(need, at):
            out.append(_unlock_reason(need))
    return out


# ------------------------------------------------------------------ views
def _requires_view(p: dict) -> dict:
    t = math_tree.tree()
    req = p.get("requires", {})
    return {"realm": req.get("realm"), "realm_vi": _realm_vi(req.get("realm", "")), "stage": req.get("stage", 0),
            "nodes": [{"id": n, "name_vi": t.nodes[n].name_vi if n in t.nodes else n} for n in req.get("nodes", [])],
            "needs": p.get("needs")}


def weapon_view(weapon_id: str, quality: str | None = None) -> dict:
    """What a weapon is: name, type, grade, quality, Công and what it does."""
    d = data()
    kind, grade = split(weapon_id)
    t = d["types"][kind]
    out = {"weapon": weapon_id, "name_vi": weapon_name(weapon_id), "type": kind, "type_vi": t["name_vi"],
           "grade": grade, "grade_vi": d["grades"][grade]["prefix_vi"], "branch": t["branch"],
           "branch_vi": branch_name(t["branch"]), "clip": t["clip"], "effect_vi": effect_vi(weapon_id),
           "why_vi": t.get("why_vi", ""), "ky_binh": bool(t.get("drop_only"))}
    if quality in d["qualities"]:
        q = d["qualities"][quality]
        out.update(quality=quality, quality_vi=q["name_vi"],
                   quality_color=catalog.equipment()["rarities"].get(q["rarity"], {}).get("color"),
                   atk=int(round(int(d["grades"][grade]["atk"]) * float(q["power"]))))
    return out


def instance_extra(e: EquipmentInstance) -> dict | None:
    """The weapon part of items.equipment_view for a plan weapon (None for other gear)."""
    if not is_weapon(e.item_id):
        return None
    q = quality_of_rarity(e.rarity)
    out = weapon_view(e.item_id, q["id"] if q else None)
    out["upgradable"] = bool(q and step_for(q["id"]))
    return out


def placed_view(p: dict, at: tuple[str, int], done: set[str], taken: set[str]) -> dict:
    land = data()["lands"].get(p["land"], {})
    lacking = [] if p["id"] in taken else missing(p, at, done)
    state = TAKEN if p["id"] in taken else (LOCKED if lacking else AVAILABLE)
    pos = p.get("pos")
    return {"id": p["id"], "weapon": p["weapon"], "quality": p["quality"], "land": p["land"],
            "pos": list(pos) if isinstance(pos, (list, tuple)) and len(pos) == 2 else None,
            "state": state, "reason_vi": " ".join(lacking),
            "land_vi": land.get("name_vi", p["land"]), "spot_vi": p.get("spot_vi", ""),
            "requires": _requires_view(p), **{k: v for k, v in weapon_view(p["weapon"], p["quality"]).items()
                                              if k not in ("weapon", "quality")}}


async def _taken(db: AsyncSession, user_id: int) -> set[str]:
    return set((await db.execute(select(WeaponClaim.placed_id).where(WeaponClaim.user_id == user_id))).scalars())


async def view(db: AsyncSession, user: User) -> dict:
    """GET /weapons: the player's weapons, the one equipped, every placed weapon, and the
    qualities with their colours."""
    from . import items
    at, done = await standing(db, user.id)
    taken = await _taken(db, user.id)
    eq = catalog.equipment()["items"]
    mine = (await db.execute(select(EquipmentInstance).where(EquipmentInstance.user_id == user.id)
                             .order_by(EquipmentInstance.id))).scalars().all()
    weapons = [items.equipment_view(e) for e in mine if eq.get(e.item_id, {}).get("slot") == "weapon"]
    equipped = next((w for w in weapons if w.get("equipped") == "weapon"), None)
    return {"weapons": weapons, "equipped": equipped["id"] if equipped else None,
            "placed": [placed_view(p, at, done, taken) for p in data()["placed"]],
            "qualities": qualities_view(),
            "tu_vi": {"realm": at[0], "realm_vi": _realm_vi(at[0]), "stage": at[1]},
            "can_claim": unlock_open(data()["cfg"].get("claim_unlock", ""), at),
            "can_upgrade": unlock_open(data()["cfg"].get("upgrade_unlock", ""), at)}


# ------------------------------------------------------------------ claim
async def claim(db: AsyncSession, user: User, pid: str, land: str | None = None) -> dict:
    """POST /weapons/claim: the weapon of a spot, once, when its requirements are met and (when
    the caller says which land the player is in) the player is in its land."""
    from . import items
    p = data()["by_id"].get(pid)
    if p is None:
        raise WeaponError(404, "no_weapon", "Không có binh khí nào ở chỗ này.")
    if pid in await _taken(db, user.id):
        raise WeaponError(400, "taken", "Đã nhặt binh khí này rồi.")
    if land is not None and land != p["land"]:
        name = data()["lands"].get(p["land"], {}).get("name_vi", p["land"])
        raise WeaponError(400, "wrong_land", f"Binh khí này nằm ở {name}, không phải ở đây.")
    at, done = await standing(db, user.id)
    lacking = missing(p, at, done)
    if lacking:
        raise WeaponError(400, "locked", " ".join(lacking))
    q = data()["qualities"][p["quality"]]
    piece = await items.grant_equipment(db, user.id, p["weapon"], q["rarity"], "weapon_claim", pid)
    db.add(WeaponClaim(user_id=user.id, placed_id=pid, instance_id=piece["id"], claimed_at=clock.now()))
    try:
        await db.flush()
    except IntegrityError:          # the same spot claimed twice at once: the second one loses
        await db.rollback()
        raise WeaponError(400, "taken", "Đã nhặt binh khí này rồi.") from None
    return {"claimed": pid, "equipment": piece,
            "placed": placed_view(p, at, done, {pid})}


# ------------------------------------------------------------------ equip
async def _mine(db: AsyncSession, user: User, instance_id: int) -> EquipmentInstance:
    e = await db.get(EquipmentInstance, instance_id)
    if e is None or e.user_id != user.id:
        raise WeaponError(404, "no_item", "Không tìm thấy binh khí này.")
    if catalog.equipment()["items"].get(e.item_id, {}).get("slot") != "weapon":
        raise WeaponError(400, "not_weapon", "Món này không phải binh khí.")
    return e


async def equip(db: AsyncSession, user: User, instance_id: int) -> dict:
    """Through the one equipment path (items.equip): stats, max HP and the live world follow."""
    from . import items
    await _mine(db, user, instance_id)
    return await items.equip(db, user, instance_id)


async def unequip(db: AsyncSession, user: User) -> dict:
    from . import items
    return await items.unequip(db, user, "weapon")


# ------------------------------------------------------------------ Rèn nâng phẩm
def upgrade_steps() -> list[dict]:
    """The chain of forge steps of crafting.json `upgrades` (each with its `id`), from the
    lowest quality up."""
    ups = catalog.math_crafting().get("upgrades", {})
    order = quality_order()
    steps = [{**v, "id": k} for k, v in ups.items() if not k.startswith("_") and isinstance(v, dict)]
    return sorted(steps, key=lambda s: order.index(s["from"]) if s.get("from") in order else len(order))


def upgrade_recipe() -> dict | None:
    """The first step of the chain (hạ -> trung), the one opened by the unlock nang_pham."""
    uid = data()["cfg"].get("upgrade_unlock", "")
    return next((s for s in upgrade_steps() if s["id"] == uid), None)


def step_for(quality: str | None) -> dict | None:
    """The forge step that raises a weapon of this quality (None at the top)."""
    return next((s for s in upgrade_steps() if s.get("from") == quality), None)


def _lines(recipe: dict, held: dict[str, int]) -> list[dict]:
    out = []
    for i in recipe["ingredients"]:
        info = catalog.stack_item(i["item"]) or {}
        have = held.get(i["item"], 0)
        out.append({"item_id": i["item"], "name_vi": info.get("name_vi", i["item"]), "qty": int(i["qty"]),
                    "have": have, "enough": have >= int(i["qty"])})
    return out


def _atk_as(e: EquipmentInstance, rarity: str) -> int:
    """The Công this piece would have at another quality, its enhance level kept."""
    from . import cultivation
    probe = EquipmentInstance(user_id=e.user_id, item_id=e.item_id, rarity=rarity, enhance_level=e.enhance_level)
    return int(cultivation.instance_stats(probe).get("atk", 0))


def step_missing(step: dict, at: tuple[str, int], tier: tuple[str, int]) -> list[str]:
    """Why a forge step is shut, one sentence each (empty = open): the first step opens with
    the unlock nang_pham, a later one at its stage of Đạo Thụ (`requires`); every step also
    asks the character's cultivation tu vi (`tu_vi`, a loot tier)."""
    from . import loot
    out: list[str] = []
    uid = data()["cfg"].get("upgrade_unlock", "")
    if step["id"] == uid:
        if not unlock_open(uid, at):
            out.append(_unlock_reason(uid))
    else:
        req = step.get("requires", {})
        if not reaches(at, req.get("realm", "luyen_khi"), int(req.get("stage", 0))):
            out.append(f"Mở ở {_realm_vi(req.get('realm', ''))} tầng {req.get('stage', 0)} trên Đạo Thụ.")
    if step.get("tu_vi") and loot.rank(*tier) < loot.parse(step["tu_vi"]):
        out.append(f"Cần tu vi {loot.label(loot.parse(step['tu_vi']))}.")
    return out


def _step_view(step: dict, at, tier, held: dict[str, int], rows: list[EquipmentInstance], stones: int) -> dict:
    from . import items
    d = data()
    rar = catalog.equipment()["rarities"]
    frm, to = d["qualities"][step["from"]], d["qualities"][step["to"]]
    lines = _lines(step, held)
    why = step_missing(step, at, tier)
    fee = int(step.get("fee", 0))
    return {"id": step["id"], "name_vi": step["name_vi"], "desc_vi": step.get("desc_vi", ""), "fee": fee,
            "from": step["from"], "from_vi": frm["name_vi"], "from_color": rar[frm["rarity"]]["color"],
            "to": step["to"], "to_vi": to["name_vi"], "to_color": rar[to["rarity"]]["color"],
            "ingredients": lines, "open": not why, "reason_vi": " ".join(why),
            "can": not why and all(x["enough"] for x in lines) and stones >= fee,
            "candidates": [{**items.equipment_view(e), "after": weapon_view(e.item_id, step["to"]),
                            "after_atk": _atk_as(e, to["rarity"])}
                           for e in rows if e.rarity == frm["rarity"] and is_weapon(e.item_id)]}


async def upgrade_view(db: AsyncSession, user: User) -> dict:
    """What the forge shows for Rèn nâng phẩm: every step of the chain (`steps`) - whether it is
    open and why not, its cost against what the player holds, and the weapons it can raise. The
    first step's fields are also at the top level (the shape of the one-step forge)."""
    from . import items, loot
    steps = upgrade_steps()
    first = upgrade_recipe()
    if first is None:
        return {"open": False, "reason_vi": "Lò rèn chưa có công thức nâng phẩm.", "candidates": [], "steps": []}
    at, _ = await standing(db, user.id)
    tier = await loot.player_tier(db, user.id)
    held = await items.stacks(db, user.id)
    rows = (await db.execute(select(EquipmentInstance).where(EquipmentInstance.user_id == user.id)
                             .order_by(EquipmentInstance.id))).scalars().all()
    views = [_step_view(s, at, tier, held, rows, user.spirit_stones) for s in steps]
    top = next(v for v in views if v["id"] == first["id"])
    return {**top, "steps": views, "qualities": qualities_view(), "spirit_stones": user.spirit_stones}


async def upgrade(db: AsyncSession, user: User, instance_id: int) -> dict:
    """One quality up, by the step of the chain that starts at the piece's quality, for its
    materials and fee; grade and enhance stay."""
    from . import items, loot
    if upgrade_recipe() is None:
        raise WeaponError(400, "no_recipe", "Lò rèn chưa có công thức nâng phẩm.")
    e = await _mine(db, user, instance_id)
    if not is_weapon(e.item_id):
        raise WeaponError(400, "not_plan_weapon", "Chỉ binh khí của các vùng đất mới nâng phẩm được.")
    q = quality_of_rarity(e.rarity)
    r = step_for(q["id"] if q else None)
    if r is None:
        if q is not None and q["id"] == quality_order()[-1]:
            raise WeaponError(400, "wrong_quality", f"Binh khí này đã là {q['name_vi'].lower()}, không nâng được nữa.")
        raise WeaponError(400, "wrong_quality", "Lò rèn không có cách nâng phẩm binh khí này.")
    at, _ = await standing(db, user.id)
    why = step_missing(r, at, await loot.player_tier(db, user.id))
    if why:
        raise WeaponError(400, "locked", " ".join(why))
    held = await items.stacks(db, user.id)
    for line in _lines(r, held):
        if not line["enough"]:
            raise WeaponError(400, "need_material",
                              f"Thiếu {line['name_vi']}: cần {line['qty']}, có {line['have']}.")
    fee = int(r.get("fee", 0))
    if fee:
        try:
            await inventory.change_currency(db, user.id, "spirit_stones", -fee, r["id"], str(e.id))
        except inventory.InsufficientFunds as err:
            raise WeaponError(400, "no_stones", err.message_vi) from None
    for i in r["ingredients"]:
        try:
            await inventory.consume_item(db, user.id, i["item"], int(i["qty"]), r["id"], str(e.id))
        except inventory.InsufficientFunds as err:
            raise WeaponError(400, "need_material", err.message_vi) from None
    to = data()["qualities"][r["to"]]
    e.rarity = to["rarity"]
    db.add(AuditLog(user_id=user.id, currency_or_item=f"equip:{e.item_id}:{e.rarity}", delta=0, balance_after=None,
                    reason=r["id"], ref_id=str(e.id), created_at=clock.now()))
    await db.flush()
    stats = await items._after_gear_change(db, user.id) if e.equipped_slot else None
    await db.refresh(user, ["spirit_stones"])
    return {"upgraded": e.id, "step": r["id"], "item": items.equipment_view(e), "stats": stats,
            "spirit_stones": user.spirit_stones}


# ------------------------------------------------------------------ content check
def validate() -> list[str]:
    """The weapon sections can be played: every number the rules read is there and sane, every
    placed or droppable weapon is a piece of equipment, the drop table keeps the loot rule, and
    every forge step costs things that really drop no later than it opens (tools/check_all.py
    adds the client art of the live types: icons and in-hand layers)."""
    errs: list[str] = []
    d = data()
    t = math_tree.tree()
    if "weapons" not in d["plan"].get("wired_sections", []) and d["plan"].get("wired") is not True:
        errs.append("world_plan: 'weapons' is not in wired_sections, yet the game runs on it")
    for g, grade in d["grades"].items():
        if not isinstance(grade.get("atk"), int) or grade["atk"] <= 0:
            errs.append(f"grade {g}: 'atk' must be a positive whole number")
    atks = [d["grades"][g].get("atk", 0) for g in sorted(d["grades"])]
    if atks != sorted(atks):
        errs.append("grades: 'atk' must grow with the grade")
    powers = []
    for qid, q in d["qualities"].items():
        if q.get("rarity") not in catalog.equipment()["rarities"]:
            errs.append(f"quality {qid}: rarity {q.get('rarity')!r} is not an equipment rarity")
        powers.append(float(q.get("power", 0)))
    if powers != sorted(powers) or len(set(powers)) != len(powers) or (powers and powers[0] <= 0):
        errs.append("qualities: 'power' must be positive and grow from hạ to tuyệt")
    if len({q.get("rarity") for q in d["qualities"].values()}) != len(d["qualities"]):
        errs.append("qualities: two qualities share a rarity")
    got = {qid: q.get("rarity") for qid, q in d["qualities"].items()}
    if list(got) != list(QUALITY_RARITY) or got != QUALITY_RARITY:
        errs.append(f"qualities: the ids and rarities are a contract with the art: {QUALITY_RARITY}")
    for kid, k in d["types"].items():
        if k.get("clip") not in CLIPS:
            errs.append(f"weapon type {kid}: clip {k.get('clip')!r} is not one of {CLIPS}")
        for key in ("range", "cooldown", "mult"):
            v = k.get(key)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                errs.append(f"weapon type {kid}: '{key}' must be a positive number")
        if k.get("status") not in STATUSES:
            errs.append(f"weapon type {kid}: status {k.get('status')!r} is not one of {STATUSES}")
        if not k.get("why_vi"):
            errs.append(f"weapon type {kid}: no why_vi")
        if k.get("drop_only"):
            land = d["lands"].get(k.get("land") or "")
            if land is None or land.get("kind") not in ("wild", "boss"):
                errs.append(f"weapon type {kid}: a kỳ binh (drop_only) needs a land whose creatures drop it")
    cfg = d["cfg"]
    for key in ("own_branch_parry_bonus", "any_branch_parry_bonus"):
        v = cfg.get(key)
        if not isinstance(v, (int, float)) or not 0 <= v <= 2:
            errs.append(f"weapons.{key} must be a number from 0 to 2")
    for key in ("claim_unlock", "upgrade_unlock"):
        if cfg.get(key) not in d["unlocks"]:
            errs.append(f"weapons.{key}: unknown unlock {cfg.get(key)!r}")
        elif d["unlocks"][cfg[key]].get("status") != "co":
            errs.append(f"weapons.{key}: {cfg[key]} is wired, so its status must be 'co'")
    items = catalog.equipment()["items"]
    for p in d["placed"]:
        where = f"weapons_placed {p['id']}"
        if not is_weapon(p["weapon"]):
            errs.append(f"{where}: {p['weapon']!r} is not <weapon type>_<grade>")
            continue
        kind = split(p["weapon"])[0]
        if d["types"][kind].get("drop_only"):
            errs.append(f"{where}: {kind} is a kỳ binh, it only drops and is never placed")
        if not type_live(kind):
            errs.append(f"{where}: type {kind} is not in the game (status {d['types'][kind].get('status')!r})")
        if items.get(p["weapon"], {}).get("slot") != "weapon":
            errs.append(f"{where}: {p['weapon']} is not a piece of equipment")
        for n in p.get("requires", {}).get("nodes", []):
            if n not in t.nodes:
                errs.append(f"{where}: requires unknown node {n!r}")
        pos = p.get("pos")
        if pos is not None and not (isinstance(pos, list) and len(pos) == 2
                                    and all(isinstance(v, (int, float)) for v in pos)):
            errs.append(f"{where}: 'pos' must be [x, y]")
    if len(d["by_id"]) != len(d["placed"]):
        errs.append("weapons_placed: two spots share an id")
    for wid in sorted(droppable_weapons()):
        if items.get(wid, {}).get("slot") != "weapon":
            errs.append(f"weapon_drops: {wid} can drop but is not a piece of equipment")
    errs += _validate_drops()
    errs += _validate_upgrade()
    return errs


def _validate_drops() -> list[str]:
    """weapon_drops: wired, a rate for every rank (rising with the rank; kỳ binh only from
    elites and bosses and rarer than the main type), odds over known qualities that sum to 1,
    sound land overrides, and every built land with creatures drops something."""
    from . import loot
    errs: list[str] = []
    d = data()
    dr = d["drops"]
    if not dr:
        return ["world_plan: no weapon_drops section"]
    if not drops_wired():
        errs.append("world_plan: 'weapon_drops' is not in wired_sections, yet the game runs on it")
    by_rank = dr.get("by_rank", {})
    chances = []
    for rank in RANKS:
        r = by_rank.get(rank)
        where = f"weapon_drops.by_rank.{rank}"
        if not isinstance(r, dict):
            errs.append(f"{where} missing")
            continue
        c, k = r.get("chance"), r.get("ky_binh_chance", 0)
        for key, v in (("chance", c), ("ky_binh_chance", k)):
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 1:
                errs.append(f"{where}.{key} must be a number from 0 to 1")
        if not isinstance(c, (int, float)) or not isinstance(k, (int, float)):
            continue
        chances.append(c)
        if rank == "normal" and k:
            errs.append(f"{where}: a kỳ binh drops only from elites and bosses")
        if rank != "normal" and not 0 < k < c:
            errs.append(f"{where}: a kỳ binh must drop, and more rarely than the land's main type")
        odds = r.get("qualities", {})
        for q, v in odds.items():
            if q not in d["qualities"]:
                errs.append(f"{where}.qualities: unknown quality {q!r}")
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0:
                errs.append(f"{where}.qualities.{q} must be a number from 0")
        total = sum(v for v in odds.values() if isinstance(v, (int, float)))
        if abs(total - 1.0) > 1e-6:
            errs.append(f"{where}.qualities add up to {total:g}, not 1")
    if len(chances) == len(RANKS) and chances != sorted(chances):
        errs.append("weapon_drops.by_rank: the chance must rise from normal to elite to boss")
    for land_id, over in dr.get("lands", {}).items():
        where = f"weapon_drops.lands.{land_id}"
        if land_id not in d["lands"]:
            errs.append(f"{where}: unknown land")
            continue
        for key in ("types", "ky_binh"):
            for k in over.get(key, []):
                if k not in d["types"]:
                    errs.append(f"{where}.{key}: unknown weapon type {k!r}")
                elif bool(d["types"][k].get("drop_only")) != (key == "ky_binh"):
                    errs.append(f"{where}.{key}: {k} is {'not ' if key == 'ky_binh' else ''}a kỳ binh")
        grades = over.get("grades", [])
        for g in grades:
            if g.get("grade") not in d["grades"]:
                errs.append(f"{where}.grades: unknown grade {g.get('grade')!r}")
            w = g.get("weight", 1)
            if not isinstance(w, (int, float)) or w <= 0:
                errs.append(f"{where}.grades: weight of grade {g.get('grade')} must be positive")
            if g.get("tu_vi"):
                try:
                    loot.parse(g["tu_vi"])
                except ValueError as e:
                    errs.append(f"{where}.grades: {e}")
        if grades and all(g.get("tu_vi") for g in grades):
            errs.append(f"{where}.grades: at least one grade must drop without a tu vi gate")
    mons = catalog.monsters()
    lands_with_creatures = {m.get("land") for m in mons.values() if m.get("land")}
    for land_id in sorted(lands_with_creatures):
        land = d["lands"].get(land_id)
        if land is None or land.get("status") != "co":
            continue
        tb = land_table(land_id)
        if not tb["main"] or not tb["grades"]:
            errs.append(f"weapon_drops: the creatures of {land_id} drop no weapon")
    return errs


def _validate_upgrade() -> list[str]:
    """The forge chain: one step per quality but the last, each from the quality the previous
    one reaches to the next one up, a rising fee, gates that never go down, and ingredients
    that really drop no later than the step opens."""
    from . import loot
    errs: list[str] = []
    d = data()
    steps = upgrade_steps()
    if upgrade_recipe() is None:
        return [f"crafting.json: no upgrades.{d['cfg'].get('upgrade_unlock')} recipe"]
    order = quality_order()
    for s in steps:
        if s.get("from") not in d["qualities"] or s.get("to") not in d["qualities"]:
            return [f"crafting.json upgrades.{s['id']}: 'from' and 'to' must be qualities of world_plan.json"]
    if [s["from"] for s in steps] != order[:-1]:
        errs.append(f"crafting.json upgrades: the chain must have one step from each quality but the last "
                    f"({' -> '.join(order)})")
    if upgrade_recipe()["from"] != order[0]:
        errs.append("crafting.json upgrades: the step of the unlock nang_pham must be the first")
    dropped: set[str] = set()
    for m in catalog.monsters().values():
        dropped |= {x["item"] for x in m.get("drops", []) if "item" in x}
    realms = {r["id"] for r in catalog.realms()}
    u = d["unlocks"].get(d["cfg"].get("upgrade_unlock"), {})
    prev_fee, prev_tu_vi, prev_at = -1, None, None
    for s in steps:
        where = f"crafting.json upgrades.{s['id']}"
        if order.index(s["to"]) != order.index(s["from"]) + 1:
            errs.append(f"{where}: an upgrade raises a weapon by exactly one quality")
        fee = int(s.get("fee", 0))
        if fee < 0:
            errs.append(f"{where}: a negative fee")
        if fee <= prev_fee:
            errs.append(f"{where}: the fee must rise along the chain")
        prev_fee = fee
        if not s.get("ingredients"):
            errs.append(f"{where}: no ingredients")
        # Đạo Thụ: the first step by its unlock, the others by `requires`
        if s["id"] == d["cfg"].get("upgrade_unlock"):
            at = (u.get("realm"), int(u.get("stage", 0))) if u else None
        else:
            req = s.get("requires", {})
            if req.get("realm") not in t_realms():
                errs.append(f"{where}: 'requires' must name a realm of Đạo Thụ and a stage")
                continue
            at = (req["realm"], int(req.get("stage", 0)))
        if at and prev_at and not math_tree.tree().reaches(prev_at[0], prev_at[1], at):
            errs.append(f"{where}: opens on Đạo Thụ before the step below it")
        prev_at = at or prev_at
        try:
            tu_vi = loot.parse(s.get("tu_vi", "pham_nhan"))
        except ValueError as e:
            errs.append(f"{where}: tu_vi: {e}")
            continue
        if prev_tu_vi is not None and tu_vi < prev_tu_vi:
            errs.append(f"{where}: its tu vi is below the step under it")
        prev_tu_vi = tu_vi
        # the loot tier by which it opens: its tu vi, or the Đạo Thụ stage read as a tier when
        # the realm has the same id in both ladders (Luyện Khí, Trúc Cơ)
        opens = tu_vi
        if at and at[0] in realms:
            opens = max(opens, loot.parse(f"{at[0]}:{max(at[1], 1) if at[0] != 'pham_nhan' else 0}"))
        for i in s.get("ingredients", []):
            item = i.get("item")
            if catalog.stack_item(item) is None:
                errs.append(f"{where}: {item!r} is not an item")
                continue
            if item not in dropped:
                errs.append(f"{where}: nothing drops {item!r}")
            tier = loot.item_tier(item)
            if tier is not None and tier > opens:
                errs.append(f"{where}: {item!r} drops only from {loot.label(tier)}, after the step opens")
            if int(i.get("qty", 0)) <= 0:
                errs.append(f"{where}: {item!r} with qty {i.get('qty')!r}")
    return errs


def t_realms() -> set[str]:
    return set(math_tree.tree().realm_order)
