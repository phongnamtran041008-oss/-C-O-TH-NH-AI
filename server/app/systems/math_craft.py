"""Lò Toán: the basic crafting of M7 (kế hoạch 4.1, bước 3).

What a quái lỗi sai leaves behind is half of a recipe; the other half is having understood
it. A recipe therefore asks for two different things:

  * **ingredients**, which are spent: the materials the monsters drop, plus Linh Thạch for
    the furnace;
  * **ghi chú lỗi sai**, which are *not* spent. Holding the note is the proof the mistake
    was read about, so "only forge what you understand" is a rule of the data, not a
    sermon in the text. A note stays in the bag afterwards, the way a đan phương does.

The rarity of what comes out is written in the recipe, not rolled: a player who gathered
the materials knows exactly what they are getting, and a test can assert it.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..models import User
from . import catalog, inventory, items


class CraftError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


def recipes() -> dict:
    return catalog.math_crafting()["recipes"]


def _recipe(recipe_id: str) -> dict:
    r = recipes().get(recipe_id)
    if r is None:
        raise CraftError(404, "no_recipe", "Không có công thức này.")
    return r


def _line(item_id: str, qty: int, have: int) -> dict:
    info = catalog.stack_item(item_id) or {}
    return {"item_id": item_id, "name_vi": info.get("name_vi", item_id), "qty": qty, "have": have,
            "enough": have >= qty}


async def view(db: AsyncSession, user: User) -> dict:
    """Every recipe, with what the player holds against it."""
    held = await items.stacks(db, user.id)
    out = []
    for rid, r in sorted(recipes().items(), key=lambda kv: (kv[1].get("floor", 0), kv[0])):
        made = catalog.equipment()["items"].get(r["makes"], {})
        ingredients = [_line(i["item"], int(i["qty"]), held.get(i["item"], 0)) for i in r["ingredients"]]
        notes = [_line(n, 1, held.get(n, 0)) for n in r.get("needs_notes", [])]
        out.append({"id": rid, "name_vi": r["name_vi"], "floor": r.get("floor", 0), "fee": int(r.get("fee", 0)),
                    "desc_vi": r.get("desc_vi", ""), "rarity": r["rarity"],
                    "makes": {"item_id": r["makes"], "name_vi": made.get("name_vi", r["makes"]),
                              "slot": made.get("slot"), "stats": made.get("stats", {})},
                    "ingredients": ingredients, "notes": notes,
                    "can": all(x["enough"] for x in ingredients + notes)
                    and user.spirit_stones >= int(r.get("fee", 0))})
    return {"recipes": out, "spirit_stones": user.spirit_stones}


async def craft(db: AsyncSession, user: User, recipe_id: str) -> dict:
    """Spends the materials and the fee and hands over the equipment. The notes are only
    checked, never spent."""
    r = _recipe(recipe_id)
    held = await items.stacks(db, user.id)
    for note in r.get("needs_notes", []):
        if held.get(note, 0) < 1:
            info = catalog.stack_item(note) or {}
            raise CraftError(400, "need_note",
                             f"Chưa có {info.get('name_vi', note)}: đánh con quái giữ lỗi ấy rồi đọc ghi chú đã.")
    for i in r["ingredients"]:
        if held.get(i["item"], 0) < int(i["qty"]):
            info = catalog.stack_item(i["item"]) or {}
            raise CraftError(400, "need_material",
                             f"Thiếu {info.get('name_vi', i['item'])}: cần {i['qty']}, "
                             f"có {held.get(i['item'], 0)}.")
    fee = int(r.get("fee", 0))
    if fee:
        try:
            await inventory.change_currency(db, user.id, "spirit_stones", -fee, "math_craft", recipe_id)
        except inventory.InsufficientFunds as e:
            raise CraftError(400, "no_stones", e.message_vi) from None
    for i in r["ingredients"]:
        try:
            await inventory.consume_item(db, user.id, i["item"], int(i["qty"]), "math_craft", recipe_id)
        except inventory.InsufficientFunds as e:
            raise CraftError(400, "need_material", e.message_vi) from None
    made = await items.grant_equipment(db, user.id, r["makes"], r["rarity"], "math_craft", recipe_id)
    await db.refresh(user, ["spirit_stones"])
    return {"crafted": recipe_id, "equipment": made, "spirit_stones": user.spirit_stones,
            "at": clock.now().isoformat() + "Z"}
