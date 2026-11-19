"""Tàng Thư Các shelf of phổ (spec 9.3, 8.4): the books of things a player meets, catches and
owns (Yêu Quái Phổ, Ong Phổ, Ngư Phổ, Bảo Vật Phổ, Linh Thú Phổ), each with its % complete and
milestone rewards; the titles and portrait frames those milestones give; the Bảo Vật Phổ itself;
and the đan phương the Thủ Thư sells.

The other books keep their own data and screens (codex.py, bees.py, fishing.py, pets.py); this
module only counts them. The math scrolls of the library are learning/math_library.py.
"""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance
from ..models import AuditLog, CodexEntry, EquipmentInstance, FishCatch, InventoryItem, User
from . import catalog, inventory, td

BOOKS = ["monster", "bee", "fish", "treasure", "pet"]
BOOK_VI = {"monster": "Yêu Quái Phổ", "bee": "Ong Phổ", "fish": "Ngư Phổ", "treasure": "Bảo Vật Phổ",
           "pet": "Linh Thú Phổ"}


class BooksError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


def cfg() -> dict:
    return balance.load("books")


# ------------------------------------------------------------------ counting every book
async def _count(db: AsyncSession, user_id: int, codex: str) -> int:
    return (await db.execute(select(func.count()).select_from(CodexEntry).where(
        CodexEntry.user_id == user_id, CodexEntry.codex == codex))).scalar_one()


async def counts(db: AsyncSession, user: User) -> dict[str, tuple[int, int]]:
    """book -> (found, total)."""
    fish = (await db.execute(select(func.count()).select_from(FishCatch).where(
        FishCatch.user_id == user.id))).scalar_one()
    monsters_total = len(catalog.monsters()) + len(td.cfg()["monsters"])
    return {"monster": (await _count(db, user.id, "monster"), monsters_total),
            "bee": (await _count(db, user.id, "bee"), len(catalog.bees())),
            "fish": (fish, len(catalog.fish())),
            "treasure": (len(await treasures_owned(db, user.id)), len(treasure_catalog())),
            "pet": (await _count(db, user.id, "pet"), len(catalog.pets()["species"]))}


def _claimed(user: User) -> dict[str, list[int]]:
    # the flag keeps its old name so milestones claimed before the shelf was renamed stay claimed
    return {k: list(v) for k, v in ((user.flags or {}).get("library_claims") or {}).items() if k in BOOKS}


def reward_vi(r: dict) -> str:
    parts = []
    if r.get("spirit_stones"):
        parts.append(f"{r['spirit_stones']} Linh Thạch")
    if r.get("immortal_jade"):
        parts.append(f"{r['immortal_jade']} Tiên Ngọc")
    if r.get("title"):
        parts.append(f"danh hiệu «{r['title']}»")
    if r.get("frame"):
        parts.append(cfg()["frames_vi"].get(r["frame"], r["frame"]))
    if r.get("hive_cell"):
        parts.append("thêm 1 ô tổ ong")
    return ", ".join(parts)


# ------------------------------------------------------------------ titles and avatar frames
def _earnable() -> tuple[set[str], set[str]]:
    titles, frames = set(), set()
    for by_pct in cfg()["rewards"].values():
        for r in by_pct.values():
            if r.get("title"):
                titles.add(r["title"])
            if r.get("frame"):
                frames.add(r["frame"])
    return titles, frames


def owned_badges(user: User) -> tuple[list[str], list[str]]:
    """Titles and frames the player has that a milestone still gives (ones only the removed
    word books gave are no longer shown)."""
    titles, frames = _earnable()
    flags = user.flags or {}
    return ([t for t in flags.get("titles", []) if t in titles], [f for f in flags.get("frames", []) if f in frames])


def worn(user: User) -> dict:
    """The title under the name and the frame around the portrait, as /me and the HUD show them."""
    titles, frames = owned_badges(user)
    flags = user.flags or {}
    return {"title": flags.get("title") if flags.get("title") in titles else None,
            "frame": flags.get("frame") if flags.get("frame") in frames else None}


async def wear(db: AsyncSession, user: User, title: str | None, frame: str | None) -> dict:
    """Choose the title shown under the name and the frame around the portrait ("" = none)."""
    titles, frames = owned_badges(user)
    flags = dict(user.flags or {})
    if title is not None:
        if title and title not in titles:
            raise BooksError(400, "no_title", "Con chưa có danh hiệu này.")
        flags["title"] = title or None
    if frame is not None:
        if frame and frame not in frames:
            raise BooksError(400, "no_frame", "Con chưa có khung này.")
        flags["frame"] = frame or None
    user.flags = flags
    await db.flush()
    return await overview(db, user)


# ------------------------------------------------------------------ the shelf
async def overview(db: AsyncSession, user: User) -> dict:
    c = cfg()
    claimed = _claimed(user)
    books = []
    for book, (found, total) in (await counts(db, user)).items():
        pct = int(found * 100 // total) if total else 0
        ms = []
        for m in c["milestones"]:
            r = c["rewards"][book][str(m)]
            ms.append({"pct": m, "reward": r, "reward_vi": reward_vi(r), "ready": pct >= m,
                       "claimed": m in claimed.get(book, [])})
        books.append({"id": book, "name_vi": BOOK_VI[book], "found": found, "total": total, "pct": pct,
                      "milestones": ms})
    titles, frames = owned_badges(user)
    return {"books": books, "titles": titles,
            "frames": [{"id": f, "name_vi": c["frames_vi"].get(f, f)} for f in frames],
            **worn(user), "shop": await shop_view(db, user), "at_desk": at_desk(user.id)}


async def claim(db: AsyncSession, user: User, book: str, pct: int) -> dict:
    c = cfg()
    if book not in BOOKS or pct not in c["milestones"]:
        raise BooksError(400, "bad_milestone", "Không có mốc thưởng này.")
    found, total = (await counts(db, user))[book]
    if not total or found * 100 // total < pct:
        raise BooksError(400, "not_yet", f"{BOOK_VI[book]} chưa đạt {pct}%.")
    claimed = _claimed(user)
    if pct in claimed.get(book, []):
        raise BooksError(409, "claimed", "Con đã nhận mốc này rồi.")
    r = c["rewards"][book][str(pct)]
    flags = dict(user.flags or {})
    ref = f"{book}:{pct}"
    for cur in ("spirit_stones", "immortal_jade"):
        if r.get(cur):
            await inventory.change_currency(db, user.id, cur, r[cur], "library_milestone", ref)
    if r.get("title"):
        flags["titles"] = sorted(set(flags.get("titles", [])) | {r["title"]})
    if r.get("frame"):
        flags["frames"] = sorted(set(flags.get("frames", [])) | {r["frame"]})
    if r.get("hive_cell"):
        from . import bees
        hive = await bees.ensure_hive(db, user)
        if hive.cells < bees.cfg()["hive"]["cells_max"]:
            hive.cells += r["hive_cell"]
    claimed[book] = sorted(set(claimed.get(book, [])) | {pct})
    flags["library_claims"] = claimed
    user.flags = flags
    await db.flush()
    return {"claimed": {"book": book, "pct": pct, "reward_vi": reward_vi(r)}, **(await overview(db, user))}


# ------------------------------------------------------------------ the Thủ Thư's đan phương
def at_desk(user_id: int) -> bool:
    """Đan phương are sold by the Thủ Thư herself (spec 8.4): stand next to her in Trúc Lâm Thôn."""
    from ..realtime.world import world
    return world.near_npc(user_id, "librarian", cfg()["shop_reach"])


async def inventory_count(db: AsyncSession, user_id: int, item_id: str) -> int:
    return int((await db.execute(select(func.coalesce(func.sum(InventoryItem.quantity), 0)).where(
        InventoryItem.user_id == user_id, InventoryItem.item_id == item_id))).scalar_one())


async def shop_view(db: AsyncSession, user: User) -> list[dict]:
    held = dict((await db.execute(select(InventoryItem.item_id, func.sum(InventoryItem.quantity)).where(
        InventoryItem.user_id == user.id).group_by(InventoryItem.item_id))).all())
    out = []
    for iid, price in cfg()["shop"].items():
        m = catalog.materials().get(iid)
        if m is None:
            continue
        have = int(held.get(iid) or 0)
        # an đan phương is "learned" as soon as it is in the bag: it is never used up
        out.append({"item_id": iid, "name_vi": m["name_vi"], "desc_vi": m.get("desc_vi", ""), "price": price,
                    "kind": m.get("kind"), "have": have, "learned": have > 0})
    return out


async def buy(db: AsyncSession, user: User, item_id: str) -> dict:
    price = cfg()["shop"].get(item_id)
    if price is None:
        raise BooksError(400, "not_sold", "Tàng Thư Các không bán thứ này.")
    if not at_desk(user.id):
        raise BooksError(400, "too_far", "Muốn mua đan phương thì tới gặp Thủ Thư ở Tàng Thư Các.")
    if (await inventory_count(db, user.id, item_id)) > 0:
        raise BooksError(400, "already_have", "Con đã có đan phương này rồi, giữ trong túi là luyện được mãi.")
    try:
        await inventory.charge(db, user.id, {"spirit_stones": price}, "library_shop", item_id)
    except inventory.InsufficientFunds:
        raise BooksError(400, "not_enough", "Chưa đủ Linh Thạch.")
    await inventory.change_item(db, user.id, item_id, 1, "library_shop")
    return {"bought": item_id, "name_vi": catalog.item_name(item_id), **(await overview(db, user))}


# ------------------------------------------------------------------ Bảo Vật Phổ
def treasure_catalog() -> dict[str, dict]:
    """Spec 9.3: equipment, pills and fishing rods a player has ever had."""
    out: dict[str, dict] = {}
    eq = catalog.equipment()
    for iid, it in eq["items"].items():
        out[iid] = {"id": iid, "kind": "equip", "kind_vi": eq["slots"].get(it["slot"], it["slot"]),
                    "name_vi": it["name_vi"], "desc_vi": it.get("desc_vi", ""), "stats": it.get("stats", {})}
    for iid, it in catalog.pills().items():
        out[iid] = {"id": iid, "kind": "pill", "kind_vi": "Đan dược", "name_vi": it["name_vi"],
                    "desc_vi": it.get("desc_vi", "")}
    for iid, it in catalog.rods().items():
        out[iid] = {"id": iid, "kind": "rod", "kind_vi": "Cần câu", "name_vi": it["name_vi"],
                    "desc_vi": it.get("desc_vi", ""), "rarity": it.get("rarity")}
    return out


async def treasures_owned(db: AsyncSession, user_id: int) -> dict[str, object]:
    """Every treasure ever received (from the audit log of every item change, plus what is
    held now), with the first time it came."""
    known = treasure_catalog()
    got: dict[str, object] = {}
    rows = (await db.execute(select(AuditLog.currency_or_item, func.min(AuditLog.created_at)).where(
        AuditLog.user_id == user_id, AuditLog.delta > 0,
        (AuditLog.currency_or_item.like("item:%")) | (AuditLog.currency_or_item.like("equip:%")))
        .group_by(AuditLog.currency_or_item))).all()
    for key, first in rows:
        iid = key.split(":")[1]
        if iid in known and (iid not in got or first < got[iid]):
            got[iid] = first
    held = list((await db.execute(select(InventoryItem.item_id).where(
        InventoryItem.user_id == user_id, InventoryItem.quantity > 0))).scalars())
    held += list((await db.execute(select(EquipmentInstance.item_id).where(
        EquipmentInstance.user_id == user_id))).scalars())
    for iid in held:
        if iid in known:
            got.setdefault(iid, None)
    return got


async def treasure_book(db: AsyncSession, user: User) -> dict:
    owned = await treasures_owned(db, user.id)
    out = []
    for iid, t in treasure_catalog().items():
        if iid in owned:
            first = owned[iid]
            out.append({**t, "found": True, "first_at": first.isoformat() + "Z" if first else None})
        else:
            out.append({"id": iid, "kind": t["kind"], "kind_vi": t["kind_vi"], "found": False})
    return {"entries": out, "found": len(owned), "total": len(out)}
