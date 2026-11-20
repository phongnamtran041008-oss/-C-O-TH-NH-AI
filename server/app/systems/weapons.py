"""Binh khí của Thiên Địa Đồ: the weapons lying in the lands (world_plan.json, wired section
`weapons`).

The plan names eight weapon types (one per curriculum branch, `weapon_types`), a grade per
realm (`grades`), three qualities (`qualities`) and the spots where weapons lie
(`weapons_placed`). This module turns that into rules, and fits them into the equipment the
game already has instead of building a second inventory beside it:

  * a weapon is `<type>_<grade>` (kiem_1 = Mộc Kiếm). Every weapon that is placed somewhere
    becomes a piece of equipment of slot `weapon` in `catalog.equipment()` (equipment_items),
    whose `kind` is the weapon id itself - so the stats the world reads (`stats.weapon`), the
    fight profile and the layer drawn in the hand all follow the weapon, grade included;
  * a quality is stored as the equipment rarity it maps to (`qualities[].rarity`: hạ = Phàm,
    trung = Linh, thượng = Huyền), so the bag, the shop, Bảo Vật Phổ and the enhance forge
    treat the piece like any other; its power is the plan's own number (`power`), not the
    rarity multiplier (cultivation.instance_stats reads `power_by_rarity`);
  * a spot gives its weapon once per player (`WeaponClaim`), only when the player's place in
    Đạo Thụ - "tu vi" in the plan - reaches its realm and stage and every node it names is
    done, and when its land is open and the ability it needs exists;
  * the fight: the type decides the normal attack (range, cooldown, multiplier) and the
    animation clip; the weapon's Công is the grade's `atk` times the quality's `power`; a
    Phản Đòn on a question of the weapon's own branch hits harder (`weapons` block of the
    plan, parry_mult);
  * Rèn nâng phẩm (unlock nang_pham): at the forge, a hạ phẩm weapon becomes trung phẩm for
    materials that really drop (crafting.json, `upgrades`).
"""
from __future__ import annotations

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


def weapon_name(weapon_id: str) -> str:
    kind, grade = split(weapon_id)
    return f"{data()['grades'][grade]['prefix_vi']} {data()['types'][kind]['name_vi']}"


def quality_of_rarity(rarity: str) -> dict | None:
    return next((q for q in data()["qualities"].values() if q.get("rarity") == rarity), None)


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
    """Every weapon that lies somewhere, as a piece of equipment (merged into
    catalog.equipment()). Its `atk` is the grade's; `power_by_rarity` holds the quality powers
    by the rarity each quality is stored as."""
    d = data()
    power = {q["rarity"]: float(q["power"]) for q in d["qualities"].values() if q.get("rarity")}
    out = {}
    for p in d["placed"]:
        wid = p["weapon"]
        if wid in out or not is_weapon(wid):
            continue
        kind, grade = split(wid)
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
           "why_vi": t.get("why_vi", "")}
    if quality in d["qualities"]:
        q = d["qualities"][quality]
        out.update(quality=quality, quality_vi=q["name_vi"],
                   atk=int(round(int(d["grades"][grade]["atk"]) * float(q["power"]))))
    return out


def instance_extra(e: EquipmentInstance) -> dict | None:
    """The weapon part of items.equipment_view for a plan weapon (None for other gear)."""
    if not is_weapon(e.item_id):
        return None
    q = quality_of_rarity(e.rarity)
    out = weapon_view(e.item_id, q["id"] if q else None)
    up = upgrade_recipe()
    out["upgradable"] = bool(q and up and q["id"] == up["from"])
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
    """GET /weapons: the player's weapons, the one equipped, and every placed weapon."""
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
def upgrade_recipe() -> dict | None:
    return catalog.math_crafting().get("upgrades", {}).get(data()["cfg"].get("upgrade_unlock", ""))


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


async def upgrade_view(db: AsyncSession, user: User) -> dict:
    """What the forge shows for Rèn nâng phẩm: whether it is open, the cost against what the
    player holds, and the weapons it can raise."""
    from . import items
    r = upgrade_recipe()
    uid = data()["cfg"].get("upgrade_unlock", "")
    at, _ = await standing(db, user.id)
    if r is None:
        return {"open": False, "reason_vi": "Lò rèn chưa có công thức nâng phẩm.", "candidates": []}
    held = await items.stacks(db, user.id)
    frm, to = data()["qualities"][r["from"]], data()["qualities"][r["to"]]
    rows = (await db.execute(select(EquipmentInstance).where(
        EquipmentInstance.user_id == user.id, EquipmentInstance.rarity == frm["rarity"])
        .order_by(EquipmentInstance.id))).scalars().all()
    lines = _lines(r, held)
    is_open = unlock_open(uid, at)
    return {"open": is_open, "reason_vi": "" if is_open else _unlock_reason(uid),
            "name_vi": r["name_vi"], "desc_vi": r.get("desc_vi", ""), "fee": int(r.get("fee", 0)),
            "from": r["from"], "from_vi": frm["name_vi"], "to": r["to"], "to_vi": to["name_vi"],
            "ingredients": lines,
            "can": is_open and all(x["enough"] for x in lines) and user.spirit_stones >= int(r.get("fee", 0)),
            "candidates": [{**items.equipment_view(e), "after": weapon_view(e.item_id, r["to"]),
                            "after_atk": _atk_as(e, to["rarity"])}
                           for e in rows if is_weapon(e.item_id)],
            "spirit_stones": user.spirit_stones}


async def upgrade(db: AsyncSession, user: User, instance_id: int) -> dict:
    """Hạ phẩm -> trung phẩm for the recipe's materials and fee; grade and enhance stay."""
    from . import items
    r = upgrade_recipe()
    uid = data()["cfg"].get("upgrade_unlock", "")
    if r is None:
        raise WeaponError(400, "no_recipe", "Lò rèn chưa có công thức nâng phẩm.")
    e = await _mine(db, user, instance_id)
    if not is_weapon(e.item_id):
        raise WeaponError(400, "not_plan_weapon", "Chỉ binh khí nhặt ở các vùng đất mới nâng phẩm được.")
    q = quality_of_rarity(e.rarity)
    if q is None or q["id"] != r["from"]:
        frm = data()["qualities"][r["from"]]["name_vi"]
        raise WeaponError(400, "wrong_quality", f"Chỉ nâng được binh khí {frm.lower()}.")
    at, _ = await standing(db, user.id)
    if not unlock_open(uid, at):
        raise WeaponError(400, "locked", _unlock_reason(uid))
    held = await items.stacks(db, user.id)
    for line in _lines(r, held):
        if not line["enough"]:
            raise WeaponError(400, "need_material",
                              f"Thiếu {line['name_vi']}: cần {line['qty']}, có {line['have']}.")
    fee = int(r.get("fee", 0))
    if fee:
        try:
            await inventory.change_currency(db, user.id, "spirit_stones", -fee, "nang_pham", str(e.id))
        except inventory.InsufficientFunds as err:
            raise WeaponError(400, "no_stones", err.message_vi) from None
    for i in r["ingredients"]:
        try:
            await inventory.consume_item(db, user.id, i["item"], int(i["qty"]), "nang_pham", str(e.id))
        except inventory.InsufficientFunds as err:
            raise WeaponError(400, "need_material", err.message_vi) from None
    to = data()["qualities"][r["to"]]
    e.rarity = to["rarity"]
    db.add(AuditLog(user_id=user.id, currency_or_item=f"equip:{e.item_id}:{e.rarity}", delta=0, balance_after=None,
                    reason="nang_pham", ref_id=str(e.id), created_at=clock.now()))
    await db.flush()
    stats = await items._after_gear_change(db, user.id) if e.equipped_slot else None
    await db.refresh(user, ["spirit_stones"])
    return {"upgraded": e.id, "item": items.equipment_view(e), "stats": stats, "spirit_stones": user.spirit_stones}


# ------------------------------------------------------------------ content check
def validate() -> list[str]:
    """The weapon sections can be played: every number the rules read is there and sane, every
    placed weapon is a piece of equipment, and the forge upgrade costs things that really drop
    no later than it opens (tools/check_all.py adds the client art: icon and in-hand layer)."""
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
    if powers != sorted(powers) or (powers and powers[0] <= 0):
        errs.append("qualities: 'power' must be positive and grow from hạ to thượng")
    if len({q.get("rarity") for q in d["qualities"].values()}) != len(d["qualities"]):
        errs.append("qualities: two qualities share a rarity")
    for kid, k in d["types"].items():
        if k.get("clip") not in CLIPS:
            errs.append(f"weapon type {kid}: clip {k.get('clip')!r} is not one of {CLIPS}")
        for key in ("range", "cooldown", "mult"):
            v = k.get(key)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                errs.append(f"weapon type {kid}: '{key}' must be a positive number")
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
    errs += _validate_upgrade()
    return errs


def _validate_upgrade() -> list[str]:
    from . import loot
    errs: list[str] = []
    d = data()
    r = upgrade_recipe()
    if r is None:
        return [f"crafting.json: no upgrades.{d['cfg'].get('upgrade_unlock')} recipe"]
    if r.get("from") not in d["qualities"] or r.get("to") not in d["qualities"]:
        return ["crafting.json upgrades: 'from' and 'to' must be qualities of world_plan.json"]
    order = list(d["qualities"])
    if order.index(r["to"]) != order.index(r["from"]) + 1:
        errs.append("crafting.json upgrades: an upgrade raises a weapon by exactly one quality")
    if int(r.get("fee", 0)) < 0:
        errs.append("crafting.json upgrades: a negative fee")
    if not r.get("ingredients"):
        errs.append("crafting.json upgrades: no ingredients")
    dropped: set[str] = set()
    for m in catalog.monsters().values():
        dropped |= {x["item"] for x in m.get("drops", []) if "item" in x}
    u = d["unlocks"].get(d["cfg"].get("upgrade_unlock"), {})
    opens = loot.parse(f"{u.get('realm')}:{u.get('stage')}") if u else None
    for i in r.get("ingredients", []):
        item = i.get("item")
        if catalog.stack_item(item) is None:
            errs.append(f"crafting.json upgrades: {item!r} is not an item")
            continue
        if item not in dropped:
            errs.append(f"crafting.json upgrades: nothing drops {item!r}")
        tier = loot.item_tier(item)
        if opens is not None and tier is not None and tier > opens:
            errs.append(f"crafting.json upgrades: {item!r} drops only from {loot.label(tier)}, after the upgrade opens")
        if int(i.get("qty", 0)) <= 0:
            errs.append(f"crafting.json upgrades: {item!r} with qty {i.get('qty')!r}")
    return errs
