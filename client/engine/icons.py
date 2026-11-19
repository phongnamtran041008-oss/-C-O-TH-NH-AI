"""Item icons: the pictures rendered from 3D models (M8).

`client/assets/icons/items.png` is a grid of 32x32 icons and `items.json` says which index
each name holds. This module hands out the surfaces and decides which icon an item of the
game gets.

**The game must run without them.** The sheet is built by a tool that needs Blender, so a
checkout without it simply has no `icons/` folder: `sheet()` returns None, `for_item()`
returns None, and whoever draws falls back to what the game drew before. A missing picture
is never a reason not to start.

Which icon an item gets is decided by rules, not by a list naming every item, because the
item catalogue grows every milestone:

* a piece of equipment goes by its **kind** first (sword, brush, fan...), then by its
  **slot** (áo, mũ, giày, ngọc bội, nhẫn);
* a stackable goes by its **kind** (đan dược, ghi chú lỗi sai, linh thảo);
* anything with no rule gets None and keeps the art it always had.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pygame

ICON_DIR = Path(__file__).resolve().parents[1] / "assets" / "icons"

# equipment `kind` (weapons name themselves) -> icon
BY_WEAPON = {"sword": "kiem", "brush": "truong", "fan": "quat", "staff": "truong",
             "spear": "thuong", "bow": "cung", "hammer": "bua", "mace": "bua"}
# equipment slot -> icon, for everything that is not a weapon
BY_SLOT = {"body": "ao_giap", "hat": "mu", "shoes": "giay", "jade": "day_chuyen",
           "ring": "nhan", "shield": "khien"}
# stackable `kind` -> icon
BY_KIND = {"pill": "dan", "note": "cuon_thu", "herb": "linh_thao",
           "bait": "dan", "rod": "thuong"}
# a few by name, where the rules would miss (checked before the rules)
BY_ID = {"truc_diep_thao": "linh_thao", "linh_qua": "linh_thao", "linh_mat": "dan",
         "manh_tap_hop": "lo_dan", "tinh_so_phuc": "lo_dan", "loi_ma_tran": "lo_dan"}


@lru_cache(maxsize=1)
def _doc() -> dict | None:
    path = ICON_DIR / "items.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text("utf-8"))
    except ValueError:
        return None


@lru_cache(maxsize=1)
def sheet() -> pygame.Surface | None:
    doc = _doc()
    if doc is None:
        return None
    png = ICON_DIR / doc.get("sheet", "items.png")
    if not png.exists():
        return None
    try:
        return pygame.image.load(str(png)).convert_alpha()
    except pygame.error:
        return None


def names() -> list[str]:
    doc = _doc()
    return sorted(doc["icons"]) if doc else []


@lru_cache(maxsize=256)
def icon(name: str, variant: int = 0) -> pygame.Surface | None:
    """One icon by name, or None when this checkout has no sheet."""
    doc, sh = _doc(), sheet()
    if doc is None or sh is None:
        return None
    entries = doc["icons"].get(name)
    if not entries:
        return None
    cell, cols = int(doc["cell"]), int(doc["cols"])
    n = int(entries[variant % len(entries)]["index"])
    return sh.subsurface(((n % cols) * cell, (n // cols) * cell, cell, cell))


def name_for(row: dict) -> str | None:
    """Which icon name an inventory row or a piece of equipment should use."""
    item_id = row.get("item_id") or row.get("id") or ""
    if item_id in BY_ID:
        return BY_ID[item_id]
    kind = row.get("kind")
    if kind in BY_WEAPON:           # equipment names its weapon kind
        return BY_WEAPON[kind]
    if kind in BY_KIND:
        return BY_KIND[kind]
    slot = row.get("slot")
    if slot in BY_SLOT:
        return BY_SLOT[slot]
    return None


def for_item(row: dict, variant: int = 0) -> pygame.Surface | None:
    name = name_for(row)
    return icon(name, variant) if name else None
