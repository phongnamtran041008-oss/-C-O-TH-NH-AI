"""Read-only game data: items, equipment, pills, skills, quests, monsters, bees, fish, rods,
baits, recipes, pets (server/data)."""
from __future__ import annotations

import json
from functools import lru_cache

from ..config import DATA_DIR


def _load(rel: str) -> dict:
    data = json.loads((DATA_DIR / rel).read_text("utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


@lru_cache(maxsize=1)
def equipment() -> dict:
    """equipment.json, plus every weapon of Thiên Địa Đồ that lies somewhere or drops from a
    creature (systems/weapons.py): one equipment model for both."""
    from . import weapons
    eq = _load("items/equipment.json")
    return {**eq, "items": {**eq["items"], **weapons.equipment_items()}}


@lru_cache(maxsize=1)
def pills() -> dict:
    return _load("items/pills.json")


@lru_cache(maxsize=1)
def materials() -> dict:
    return _load("items/materials.json")


@lru_cache(maxsize=1)
def quests() -> dict:
    return _load("quests.json")


@lru_cache(maxsize=1)
def monsters() -> dict:
    """Every kind of monster: the Mặc Quái of the old game and, since M7, the quái lỗi sai
    of the math edition, which keep their own file because they carry a micro-skill and a
    ghi chú instead of a word list. One registry, so loot, codex and quests see them all."""
    return {**_load("creatures/monsters.json"), **_load("math/monsters.json")}


@lru_cache(maxsize=1)
def bees() -> dict:
    """Linh Phong species (built and verified by tools/build_bees.py)."""
    return _load("creatures/bees.json")


@lru_cache(maxsize=1)
def fish() -> dict:
    """Fish species (built and verified by tools/build_fish.py)."""
    return _load("creatures/fish.json")


@lru_cache(maxsize=1)
def rods() -> dict:
    return _load("items/rods.json")


@lru_cache(maxsize=1)
def baits() -> dict:
    return _load("items/baits.json")


@lru_cache(maxsize=1)
def recipes() -> dict:
    """Đan phương (stage 8): recipe id (= the pill it makes) -> ingredients, yield, name chars."""
    return _load("recipes.json")["recipes"]


@lru_cache(maxsize=1)
def pets() -> dict:
    """Linh Thú: the 12 zodiac pets (stage 8)."""
    return _load("creatures/pets.json")


@lru_cache(maxsize=1)
def realms() -> list[dict]:
    return _load("realms_cultivation.json")["realms"]


@lru_cache(maxsize=1)
def math_crafting() -> dict:
    """Lò Toán (M7): recipes that turn those drops, plus the notes the player kept, into
    equipment."""
    import json
    return json.loads((DATA_DIR / "math" / "crafting.json").read_text("utf-8"))


@lru_cache(maxsize=1)
def math_drops() -> dict:
    """What the "quái = lỗi sai" of the math edition leave behind (M7): materials to
    craft with, and the ghi chú lỗi sai, which open a section of Tàng Thư Các."""
    return _load("math/drops.json")


def stack_item(item_id: str) -> dict | None:
    """Stackable things in inventory_items: pills, materials, the math
    edition's materials and ghi chú lỗi sai, fishing rods, baits and caught fish
    (`fish_<species>`)."""
    if item_id in pills():
        return {"kind": "pill", **pills()[item_id]}
    if item_id in materials():
        return materials()[item_id]
    if item_id in math_drops():
        return math_drops()[item_id]
    if item_id in rods():
        r = rods()[item_id]
        return {"kind": "rod", "name_vi": r["name_vi"], "desc_vi": r["desc_vi"], "rarity": r["rarity"]}
    if item_id in baits():
        b = baits()[item_id]
        return {"kind": "bait", "name_vi": b["name_vi"], "desc_vi": b["desc_vi"], "sell_price": b["sell_price"]}
    if item_id.startswith("fish_") and item_id[5:] in fish():
        f = fish()[item_id[5:]]
        return {"kind": "fish", "name_vi": f["name_vi"], "rarity": f["rarity"], "sell_price": f["sell_price"],
                "desc_vi": f["desc_vi"]}
    return None


def item_name(item_id: str) -> str:
    info = stack_item(item_id) or equipment()["items"].get(item_id)
    return info["name_vi"] if info else item_id
