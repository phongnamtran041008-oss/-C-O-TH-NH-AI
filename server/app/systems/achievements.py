"""Thành Tựu: achievements, their tiers, the Đạo Tâm points and the danh hiệu they give
(data/achievements.json, docs/THANH_TUU.md).

* **One entry point.** The places where things happen call `on_event(db, uid, event, n, **ctx)`
  (a request or task that already has a database session) or `bump(uid, event, n, **ctx)` (the
  realtime tick: Phản Đòn, a glide, a zone entered; buffered in memory and written by a small
  task about a second later, so a fight costs no query per hit). RAW lists every event a call
  site may send; `_expand` turns one into the counters it moves (COUNTERS). validate() checks
  that every RAW event really is sent somewhere in server/app.
* **Counters, not scans.** A counter is one row of achievement_counters per player and key:
  'kill', 'kill|rank=boss' (a filtered count), 'answer_streak' (a best value), and for a
  distinct count a marker row 'zones#loi_kiep_dai' per value. Only keys some achievement reads
  are written. A threshold crossing is found from the old and new value alone; the
  achievement row is read only then.
* **Telling the player.** A tier reached is stored with `seen` below it. The unlock is queued on
  the database session and sent as a websocket message {"t": "achievement"} only after the
  transaction commits (a rollback drops it). The client shows the toast and acknowledges with
  POST /achievements/seen; at login it asks GET /achievements/new for anything it missed while
  offline. Nothing is lost, and the acknowledgement keeps it from being announced twice.
* **Rewards follow tu vi.** Linh thạch and tiên ngọc, tiered items and danh hiệu. A tier's
  `req` (a cultivation tier) is the lowest a player may be to claim it; validate() keeps every
  item at or below it (loot_tiers.json). The danh hiệu is given on unlock; everything else
  waits for "Nhận". Points (Đạo Tâm) count on unlock and open milestone rewards.
* **Old players.** The first view (GET /achievements or /achievements/new) backfills the
  counters from what the database already knows - realm, the Yêu Quái Phổ kills, weapons,
  beasts, linh căn, trials passed, the furnace - and unlocks what that reaches without toasts.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from sqlalchemy import event as sa_event
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session as _SyncSession

from .. import clock
from ..config import DATA_DIR
from ..models import Achievement, AchievementCounter, User
from . import catalog

log = logging.getLogger("toan_tu_tien.achievements")

FILE = DATA_DIR / "achievements.json"
APP_DIR = Path(__file__).resolve().parents[1]
CLIENT_ICONS = APP_DIR.parents[1] / "client" / "assets" / "v2" / "icons"
MIN_ACHIEVEMENTS = 90
FLUSH_DELAY = 1.0           # seconds a realtime bump waits before it is written
FAST_FRACTION = 1 / 3       # a right answer in the first third of the time limit is "fast"
CLUTCH_LEFT_MS = 1500       # a right answer with this little time left is a clutch
NIGHT_HOURS = (0, 4)        # UTC+7 hours [from, to) of the night owl
COMEBACK_AFTER = 5          # wrong answers in a row before a right one counts as a comeback
BACKFILL_VERSION = 1
TITLE_MAX = 40              # POST /books/wear takes at most this many characters
NAME_MAX = 26               # a name must fit one row of Thành Tựu Lục
CJK = re.compile(r"[㐀-鿿豈-﫿　-〿]")
STREAK, WRONG = "_streak", "_wrong"     # the current runs of right / wrong answers
CURRENCIES = ("spirit_stones", "immortal_jade")


class AchievementError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the registry
@dataclass(frozen=True)
class Counter:
    mode: str                       # sum | max | distinct
    dims: tuple[str, ...] = ()      # ctx fields an achievement may filter on ('where')
    of: str | None = None           # distinct: the ctx field whose values are counted
    doc: str = ""


COUNTERS: dict[str, Counter] = {
    # Ngộ Đạo - every answer goes through learning/quiz.answer
    "answer_right": Counter("sum", ("context",), doc="right answers, by quiz context"),
    "answer_fast": Counter("sum", doc="right answers in the first third of the time limit"),
    "answer_streak": Counter("max", doc="the longest run of right answers"),
    "answer_clutch": Counter("sum", doc="right answers with under 1.5 s left"),
    "answer_night": Counter("sum", doc="right answers between 0:00 and 4:00 (UTC+7)"),
    "answer_comeback": Counter("sum", doc="a right answer after five wrong ones in a row"),
    "trial_pass": Counter("sum", doc="Thiên kiếp nhỏ passed"),
    "tree_nodes": Counter("max", doc="Đạo Thụ nodes done (vacant ones not counted)"),
    "code_solved": Counter("distinct", of="problem", doc="programming exercises fully solved"),
    "xa_truong": Counter("distinct", of="problem", doc="Xạ Trường exercises at hạ phẩm or better"),
    "xa_truong_top": Counter("distinct", of="problem", doc="Xạ Trường exercises at thượng phẩm"),
    # Tu Luyện
    "cult": Counter("max", doc="the cultivation tier reached (realm index * 100 + stage)"),
    "tribulation": Counter("sum", doc="Thiên Kiếp passed"),
    "meditate": Counter("sum", doc="meditations finished"),
    # Chiến Đấu
    "kill": Counter("sum", ("rank", "subject", "land", "monster"), doc="monsters killed"),
    "kill_kinds": Counter("distinct", of="monster", doc="kinds of monster killed (Yêu Quái Phổ)"),
    "kill_flawless": Counter("sum", ("rank",), doc="kills with the health bar full"),
    "parry": Counter("sum", doc="Phản Đòn"),
    "parry_combo": Counter("max", doc="the longest chiêu combo of right answers in a fight"),
    "death": Counter("sum", doc="falls in the open world"),
    # Sưu Tầm
    "weapon_get": Counter("sum", ("type", "quality"), doc="weapons of Thiên Địa Đồ obtained"),
    "weapon_types": Counter("distinct", of="type", doc="weapon types owned"),
    "weapon_forge": Counter("sum", ("quality",), doc="Rèn nâng phẩm, by the quality reached"),
    "beast_tame": Counter("sum", ("beast",), doc="linh thú sealed"),
    "lc_giai": Counter("max", doc="the best linh căn giai ever revealed (1..9)"),
    "lc_carry": Counter("max", doc="the best linh căn giai carried"),
    "lc_book": Counter("max", doc="linh căn in the đồ giám"),
    "lc_test": Counter("max", doc="trắc linh tests in all"),
    "brew": Counter("sum", ("quality",), doc="batches of pills out of the furnace, by quality"),
    "pill_made": Counter("sum", doc="pills brewed"),
    "fish": Counter("sum", doc="fish caught"),
    # Khám Phá
    "zones": Counter("distinct", of="zone", doc="zones of the world entered"),
    "lands": Counter("distinct", ("land",), of="land", doc="lands of Thiên Địa Đồ entered"),
    "glide": Counter("sum", doc="Đạp Kiếm Lướt"),
    "formation": Counter("sum", doc="pháp trận laid"),
    "ride": Counter("sum", doc="times mounted on a linh thú"),
    "weapon_claim": Counter("sum", doc="weapon spots of Thiên Địa Đồ claimed"),
    "realm_clear": Counter("sum", doc="bí cảnh chests opened (a run to the end)"),
    "td_win": Counter("sum", doc="Thủ Thành Toán levels won"),
    # Tài Phú
    "stones_earned": Counter("sum", doc="linh thạch earned"),
    "stones_spent": Counter("sum", doc="linh thạch spent"),
    "jade_earned": Counter("sum", doc="tiên ngọc earned"),
    "furnace": Counter("max", doc="the furnace level"),
}

# what a call site may send -> where it is sent from (docs/THANH_TUU.md repeats this table)
RAW: dict[str, str] = {
    "answer": "learning/quiz.answer",
    "quest": "systems/quests.on_event (kill, meditate, fish, td_win)",
    "cult": "systems/cultivation.add_xp (a stage or realm up)",
    "tribulation": "systems/cultivation.tribulation_handler (Thiên Kiếp passed)",
    "trial": "systems/math_practice._trial_after_answer (a Thiên kiếp nhỏ passed)",
    "code": "systems/math_code.judge (Nộp bài)",
    "gear": "systems/items.grant_equipment (every piece of equipment granted)",
    "weapon_claim": "systems/weapons.claim",
    "weapon_forge": "systems/weapons.upgrade",
    "beast_tame": "systems/beasts.seal",
    "linh_can": "systems/linh_can.awaken / roll / choose",
    "brew": "systems/alchemy.finish",
    "furnace": "systems/alchemy.upgrade_furnace",
    "currency": "systems/inventory.change_currency",
    "realm_clear": "systems/secret_realm.claim_chest",
    "kill_flawless": "realtime/combat.kill (bump)",
    "parry": "realtime/combat._parry (bump)",
    "death": "realtime/combat.die (bump)",
    "zone": "realtime/world.put (bump)",
    "glide": "realtime/abilities.apply_glide (bump)",
    "formation": "realtime/abilities.place_formation (bump)",
    "ride": "realtime/abilities.apply_ride (bump)",
}

QUEST_KINDS = {"kill": "kill", "meditate": "meditate", "fish": "fish", "td_win": "td_win"}
FIRED: set[str] = set()     # RAW events seen in this process (the tests check every one is sent)


# ------------------------------------------------------------------ data
@lru_cache(maxsize=1)
def data() -> dict:
    return json.loads(FILE.read_text("utf-8"))


def entries() -> list[dict]:
    return data()["achievements"]


@lru_cache(maxsize=1)
def by_id() -> dict[str, dict]:
    return {a["id"]: a for a in entries()}


def key_of(a: dict) -> str:
    where = a.get("where") or {}
    if not where:
        return a["counter"]
    (dim, val), = where.items()
    return f"{a['counter']}|{dim}={val}"


@lru_cache(maxsize=1)
def by_key() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for a in entries():
        out.setdefault(key_of(a), []).append(a)
    return out


def threshold(a: dict, at) -> int:
    """A tier's `at` as a counter value: a number, or for 'cult' a tier such as 'truc_co:2'."""
    if a["counter"] == "cult":
        from . import loot
        i, s = loot.parse(at)
        return i * 100 + s
    return int(at)


@lru_cache(maxsize=None)
def thresholds(ach_id: str) -> tuple[int, ...]:
    a = by_id()[ach_id]
    return tuple(threshold(a, t["at"]) for t in a["tiers"])


def reached(ach_id: str, value: int) -> int:
    return sum(1 for t in thresholds(ach_id) if t <= value)


def req_of(a: dict, n: int) -> str:
    """The cultivation tier a player needs to claim tier n (1-based)."""
    t = a["tiers"][n - 1]
    if t.get("req"):
        return t["req"]
    return t["at"] if a["counter"] == "cult" else "pham_nhan"


def title_names() -> set[str]:
    """Every danh hiệu an achievement or a milestone gives (books.wear accepts them)."""
    out = {t["reward"]["title"] for a in entries() for t in a["tiers"] if (t.get("reward") or {}).get("title")}
    out |= {m["reward"]["title"] for m in data().get("milestones", []) if m["reward"].get("title")}
    return out


def reward_vi(r: dict | None) -> list[str]:
    r = r or {}
    out = []
    if r.get("spirit_stones"):
        out.append(f"{r['spirit_stones']} Linh Thạch")
    if r.get("immortal_jade"):
        out.append(f"{r['immortal_jade']} Tiên Ngọc")
    for it in r.get("items", []):
        out.append(f"{catalog.item_name(it['item'])} x{it['qty']}")
    if r.get("title"):
        out.append(f"Danh hiệu «{r['title']}»")
    return out


def tier_name(a: dict, n: int) -> str:
    return a["tiers"][n - 1].get("name_vi") or a["name_vi"]


def unlock_view(a: dict, n: int) -> dict:
    """What the toast needs about one tier reached (the websocket message and /achievements/new)."""
    t = a["tiers"][n - 1]
    return {"key": f"{a['id']}:{n}", "id": a["id"], "tier": n, "tiers": len(a["tiers"]),
            "name_vi": a["name_vi"], "tier_name_vi": tier_name(a, n), "category": a["category"],
            "icon": a["icon"], "points": int(t.get("points", 0)), "title": (t.get("reward") or {}).get("title"),
            "hidden": bool(a.get("hidden")), "reveal_vi": a.get("reveal_vi", "")}


# ------------------------------------------------------------------ after commit: the websocket
def _queue(db: AsyncSession, uid: int, unlocks: list[dict]) -> None:
    if unlocks:
        db.sync_session.info.setdefault("ach_out", []).append((uid, list(unlocks)))


@sa_event.listens_for(_SyncSession, "after_commit")
def _after_commit(session) -> None:
    out = session.info.pop("ach_out", None)
    if not out:
        return
    try:
        from ..realtime.world import world
        merged: dict[int, list[dict]] = {}
        for uid, unlocks in out:
            merged.setdefault(uid, []).extend(unlocks)
        for uid, unlocks in merged.items():
            world.notify(uid, {"t": "achievement", "unlocks": unlocks})
    except Exception:      # never let a toast break a commit
        log.exception("achievement notify failed")


@sa_event.listens_for(_SyncSession, "after_soft_rollback")
def _after_rollback(session, previous_transaction) -> None:
    if not previous_transaction.nested:
        session.info.pop("ach_out", None)


# ------------------------------------------------------------------ counting
def _expand_static(event: str, n: int, ctx: dict) -> list[tuple[str, int, dict]]:
    """The counters a raw event moves, for every event that needs no database read."""
    if event == "quest":
        c = QUEST_KINDS.get(ctx.get("kind") or "")
        if c is None:
            return []
        if c != "kill":
            return [(c, n, {})]
        kind = ctx.get("target") or ""
        m = catalog.monsters().get(kind, {})
        mc = {"monster": kind, "rank": m.get("rank", "normal"), "subject": m.get("subject"), "land": m.get("land")}
        return [("kill", n, mc), ("kill_kinds", 1, mc)]
    if event in ("cult", "tribulation"):
        from . import loot
        i, s = loot.rank(ctx.get("realm") or "pham_nhan", int(ctx.get("stage") or 0))
        out = [("cult", i * 100 + s, {})]
        return out + ([("tribulation", 1, {})] if event == "tribulation" else [])
    if event == "trial":
        return [("trial_pass", 1, {}), ("tree_nodes", int(ctx.get("nodes") or 0), {})]
    if event == "code":
        pid = ctx.get("problem")
        if ctx.get("scored"):
            grade = int(ctx.get("grade") or 0)
            return ([("xa_truong", 1, {"problem": pid})] if grade >= 1 else []) + \
                   ([("xa_truong_top", 1, {"problem": pid})] if grade >= 3 else [])
        return [("code_solved", 1, {"problem": pid})] if ctx.get("full") else []
    if event == "gear":
        from . import weapons
        item = ctx.get("item") or ""
        if not weapons.is_weapon(item):
            return []
        kind = (catalog.equipment()["items"].get(item) or {}).get("weapon_type") or weapons.split(item)[0]
        q = weapons.quality_of_rarity(ctx.get("rarity") or "")
        wc = {"type": kind, "quality": q["id"] if q else None}
        return [("weapon_get", 1, wc), ("weapon_types", 1, wc)]
    if event == "weapon_claim":
        return [("weapon_claim", 1, {})]
    if event == "weapon_forge":
        return [("weapon_forge", 1, {"quality": ctx.get("quality")})]
    if event == "beast_tame":
        return [("beast_tame", 1, {"beast": ctx.get("beast")})]
    if event == "linh_can":
        from . import linh_can
        out = [("lc_book", int(ctx.get("seen") or 0), {}), ("lc_test", int(ctx.get("rolls") or 0), {})]
        for counter, rid in (("lc_giai", ctx.get("rolled")), ("lc_giai", ctx.get("root")), ("lc_carry", ctx.get("root"))):
            r = linh_can.roots().get(rid) if rid else None
            if r:
                out.append((counter, linh_can.giai_index(r["giai"]), {}))
        return out
    if event == "brew":
        made = int(ctx.get("made") or 0)
        return [("brew", 1, {"quality": ctx.get("quality")})] + ([("pill_made", made, {})] if made > 0 else [])
    if event == "furnace":
        return [("furnace", int(ctx.get("level") or 0), {})]
    if event == "currency":
        if ctx.get("reason") == "achievement":
            return []       # the rewards of Thành Tựu do not feed Thành Tựu
        cur, delta = ctx.get("currency"), int(ctx.get("delta") or 0)
        if cur == "spirit_stones" and delta > 0:
            return [("stones_earned", delta, {})]
        if cur == "spirit_stones" and delta < 0:
            return [("stones_spent", -delta, {})]
        if cur == "immortal_jade" and delta > 0:
            return [("jade_earned", delta, {})]
        return []
    if event == "realm_clear":
        return [("realm_clear", 1, {})]
    if event == "kill_flawless":
        return [("kill_flawless", n, {"rank": ctx.get("rank")})]
    if event == "parry":
        return [("parry", n, {}), ("parry_combo", int(ctx.get("combo") or 0), {})]
    if event == "death":
        return [("death", n, {})]
    if event == "zone":
        zone = ctx.get("zone")
        from ..realtime import lands
        land = lands.zone_land_id(zone)
        return [("zones", 1, {"zone": zone})] + ([("lands", 1, {"land": land})] if land else [])
    if event in ("glide", "formation", "ride"):
        return [(event, n, {})]
    return []


def _keys(counter: str, ctx: dict) -> list[str]:
    spec = COUNTERS[counter]
    keys = [counter] + [f"{counter}|{d}={ctx[d]}" for d in spec.dims if ctx.get(d) not in (None, "")]
    wanted = by_key()
    return [k for k in keys if k in wanted]


async def _insert_ignore(db: AsyncSession, model, **values) -> bool:
    """INSERT ... ON CONFLICT DO NOTHING (SQLite and PostgreSQL): True when the row is new.
    No savepoint: with pysqlite a SAVEPOINT that opens a transaction commits on release, which
    would make a counter outlive a request that rolled back."""
    if db.get_bind().dialect.name == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    else:
        from sqlalchemy.dialects.sqlite import insert
    res = await db.execute(insert(model).values(**values).on_conflict_do_nothing())
    return res.rowcount == 1


async def _row(db: AsyncSession, uid: int, key: str) -> AchievementCounter:
    row = await db.get(AchievementCounter, (uid, key))
    if row is None:
        await _insert_ignore(db, AchievementCounter, user_id=uid, key=key, value=0)
        row = await db.get(AchievementCounter, (uid, key))
    return row


async def _move(db: AsyncSession, uid: int, key: str, n: int, best: bool) -> tuple[int, int]:
    row = await _row(db, uid, key)
    old = int(row.value or 0)
    new = max(old, n) if best else old + n
    if new != old:
        row.value = new
    return old, new


async def _answer(db: AsyncSession, uid: int, ctx: dict) -> list[tuple[str, int, dict]]:
    """A graded answer: the runs of right and wrong answers live in two hidden counters."""
    streak = await _row(db, uid, STREAK)
    wrong = await _row(db, uid, WRONG)
    if not ctx.get("correct"):
        streak.value, wrong.value = 0, int(wrong.value or 0) + 1
        return []
    out: list[tuple[str, int, dict]] = [("answer_right", 1, {"context": ctx.get("context")})]
    if int(wrong.value or 0) >= COMEBACK_AFTER:
        out.append(("answer_comeback", 1, {}))
    streak.value, wrong.value = int(streak.value or 0) + 1, 0
    out.append(("answer_streak", streak.value, {}))
    ms, limit = ctx.get("ms"), ctx.get("limit")
    if ms is not None and limit:
        if ms <= FAST_FRACTION * float(limit) * 1000:
            out.append(("answer_fast", 1, {}))
        if float(limit) * 1000 - ms <= CLUTCH_LEFT_MS:
            out.append(("answer_clutch", 1, {}))
    hour = (clock.now() + clock.VN_OFFSET).hour
    if NIGHT_HOURS[0] <= hour < NIGHT_HOURS[1]:
        out.append(("answer_night", 1, {}))
    return out


async def _apply(db: AsyncSession, uid: int, counter: str, n: int, ctx: dict, out: list[dict],
                 quiet: bool = False) -> None:
    spec = COUNTERS[counter]
    keys = _keys(counter, ctx)
    if not keys or (n <= 0 and spec.mode != "max"):
        return
    if spec.mode == "distinct":
        v = ctx.get(spec.of)
        if v in (None, ""):
            return
        if not await _insert_ignore(db, AchievementCounter, user_id=uid, key=f"{counter}#{v}", value=1):
            return
        n = 1
    for k in keys:
        old, new = await _move(db, uid, k, n, spec.mode == "max")
        if new > old:
            for a in by_key()[k]:
                r = reached(a["id"], new)
                if r > reached(a["id"], old):
                    await _reach(db, uid, a, r, out, quiet)


async def _reach(db: AsyncSession, uid: int, a: dict, tier: int, out: list[dict], quiet: bool = False) -> None:
    row = await db.get(Achievement, (uid, a["id"]))
    if row is None:
        await _insert_ignore(db, Achievement, user_id=uid, ach_id=a["id"], tier=0, claimed=0, seen=0)
        row = await db.get(Achievement, (uid, a["id"]))
    if row.tier >= tier:
        return
    titles = [t for n in range(row.tier + 1, tier + 1) if (t := (a["tiers"][n - 1].get("reward") or {}).get("title"))]
    if titles:
        await _give_titles(db, uid, titles)
    for n in range(row.tier + 1, tier + 1):
        out.append(unlock_view(a, n))
    row.tier, row.unlocked_at = tier, clock.now()
    if quiet:
        row.seen = tier


async def _give_titles(db: AsyncSession, uid: int, titles: list[str]) -> None:
    user = await db.get(User, uid)
    if user is None:
        return
    flags = dict(user.flags or {})
    flags["titles"] = sorted(set(flags.get("titles", [])) | set(titles))
    user.flags = flags


async def on_event(db: AsyncSession, user_id: int, event: str, n: int = 1, **ctx) -> list[dict]:
    """Count one thing that happened. Returns the tiers reached now (also sent to the player
    over the websocket once the transaction commits). Never raises: a fault in the
    bookkeeping must not undo the kill or the answer it counts."""
    if event not in RAW:
        log.warning("unknown achievement event %r", event)
        return []
    FIRED.add(event)
    out: list[dict] = []
    try:
        if event == "answer":
            steps = await _answer(db, user_id, ctx)
        else:
            steps = [s for s in _expand_static(event, n, ctx) if _keys(s[0], s[2])]
        for counter, k, c in steps:
            await _apply(db, user_id, counter, k, c, out)
    except Exception:
        log.exception("achievement event %s failed", event)
        return []
    _queue(db, user_id, out)
    return out


# ------------------------------------------------------------------ the realtime buffer
_pending: dict[int, list[tuple[str, int, dict]]] = {}
_tasks: dict[int, asyncio.Task] = {}


def bump(user_id: int, event: str, n: int = 1, **ctx) -> None:
    """on_event for the realtime tick: no database here; written about FLUSH_DELAY later."""
    if event not in RAW:
        return
    FIRED.add(event)
    _pending.setdefault(user_id, []).append((event, n, ctx))
    if user_id in _tasks:
        return
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:        # no loop (a sync unit test): flush() writes it later
        return
    _tasks[user_id] = loop.create_task(_flush_later(user_id))


async def _flush_later(uid: int) -> None:
    await asyncio.sleep(FLUSH_DELAY)
    await flush(uid)


def _merged(items: list[tuple[str, int, dict]]) -> list[tuple[str, int, dict]]:
    """Several bumps of the same event and context become one (a burst of glides = one write)."""
    acc: dict[tuple, list] = {}
    for ev, n, ctx in items:
        if ev == "parry":       # the combo is a best value: keep the highest, add the counts
            k = (ev, ())
            cur = acc.setdefault(k, [ev, 0, {"combo": 0}])
            cur[1] += n
            cur[2]["combo"] = max(cur[2]["combo"], int(ctx.get("combo") or 0))
            continue
        k = (ev, tuple(sorted(ctx.items())))
        acc.setdefault(k, [ev, 0, dict(ctx)])[1] += n
    return [tuple(v) for v in acc.values()]


async def flush(uid: int) -> None:
    _tasks.pop(uid, None)
    items = _pending.pop(uid, [])
    if not items:
        return
    from .. import db as dbm
    try:
        async with dbm.SessionLocal() as db:
            for ev, n, ctx in _merged(items):
                await on_event(db, uid, ev, n, **ctx)
            await db.commit()
    except Exception:
        log.exception("achievement flush failed")


async def flush_all() -> None:
    """Write every bump still waiting (tests; the server stopping)."""
    for uid in list(_pending):
        t = _tasks.pop(uid, None)
        if t is not None and t is not asyncio.current_task():
            t.cancel()
        await flush(uid)


# ------------------------------------------------------------------ backfill and reconcile
async def _counters(db: AsyncSession, uid: int) -> dict[str, int]:
    rows = (await db.execute(select(AchievementCounter.key, AchievementCounter.value).where(
        AchievementCounter.user_id == uid))).all()
    return {k: int(v or 0) for k, v in rows}


async def _rows(db: AsyncSession, uid: int) -> dict[str, Achievement]:
    return {r.ach_id: r for r in (await db.execute(select(Achievement).where(Achievement.user_id == uid))).scalars()}


async def _raise_to(db: AsyncSession, uid: int, counter: str, value: int, ctx: dict) -> None:
    for k in _keys(counter, ctx):
        await _move(db, uid, k, value, True)


async def _mark(db: AsyncSession, uid: int, counter: str, values: set[str], dims_of=None) -> None:
    """Distinct values already owned: their markers, then each key raised to the count."""
    if not values:
        return
    for v in values:
        await _insert_ignore(db, AchievementCounter, user_id=uid, key=f"{counter}#{v}", value=1)
    seen = [k[len(counter) + 1:] for k in (await _counters(db, uid)) if k.startswith(counter + "#")]
    await _raise_to(db, uid, counter, len(seen), {})
    for v in seen:      # a distinct count filtered by its own value ('lands|land=x')
        if COUNTERS[counter].of in COUNTERS[counter].dims:
            await _raise_to(db, uid, counter, 1, {COUNTERS[counter].of: v})


async def backfill(db: AsyncSession, uid: int) -> None:
    """What the database already knows about a player from before Thành Tựu (once)."""
    from ..models import Character, CodexEntry, EquipmentInstance, LinhCan, MathRun, WeaponClaim
    from . import beasts, loot, weapons
    ch = await db.get(Character, uid)
    if ch is not None:
        i, s = loot.rank(ch.realm or "pham_nhan", int(ch.realm_stage or 0))
        await _raise_to(db, uid, "cult", i * 100 + s, {})
    kills: dict[str, int] = {}
    for e in (await db.execute(select(CodexEntry).where(CodexEntry.user_id == uid,
                                                        CodexEntry.codex == "monster"))).scalars():
        k = int((e.progress or {}).get("kills", 0))
        if k > 0 and e.entry_id in catalog.monsters():
            kills[e.entry_id] = k
    totals: dict[str, int] = {}
    for kind, k in kills.items():
        m = catalog.monsters()[kind]
        totals["kill"] = totals.get("kill", 0) + k
        for dim, val in (("rank", m.get("rank", "normal")), ("subject", m.get("subject")),
                         ("land", m.get("land")), ("monster", kind)):
            if val:
                key = f"kill|{dim}={val}"
                totals[key] = totals.get(key, 0) + k
    for key, v in totals.items():
        if key in by_key():
            await _move(db, uid, key, v, True)
    await _mark(db, uid, "kill_kinds", set(kills))
    wtot: dict[str, int] = {}
    types: set[str] = set()
    for e in (await db.execute(select(EquipmentInstance).where(EquipmentInstance.user_id == uid))).scalars():
        if not weapons.is_weapon(e.item_id):
            continue
        kind = weapons.split(e.item_id)[0]
        q = weapons.quality_of_rarity(e.rarity)
        types.add(kind)
        for key in ("weapon_get", f"weapon_get|type={kind}") + ((f"weapon_get|quality={q['id']}",) if q else ()):
            wtot[key] = wtot.get(key, 0) + 1
    for key, v in wtot.items():
        if key in by_key():
            await _move(db, uid, key, v, True)
    await _mark(db, uid, "weapon_types", types)
    claims = (await db.execute(select(func.count()).select_from(WeaponClaim).where(WeaponClaim.user_id == uid))).scalar()
    await _raise_to(db, uid, "weapon_claim", int(claims or 0), {})
    tamed = await beasts.tamed(db, uid)
    await _raise_to(db, uid, "beast_tame", len(tamed), {})
    for b in tamed:
        await _raise_to(db, uid, "beast_tame", 1, {"beast": b})
    lc = await db.get(LinhCan, uid)
    if lc is not None and lc.root_id:
        for counter, k, c in _expand_static("linh_can", 1, {"root": lc.root_id, "seen": len(lc.discovered or []),
                                                            "rolls": lc.rolls or 0}):
            await _raise_to(db, uid, counter, k, c)
        from . import linh_can
        best = max((linh_can.giai_index(linh_can.roots()[r]["giai"]) for r in (lc.discovered or []) if r in linh_can.roots()),
                   default=0)
        await _raise_to(db, uid, "lc_giai", best, {})
    trials = (await db.execute(select(func.count()).select_from(MathRun).where(
        MathRun.user_id == uid, MathRun.mode == "trial", MathRun.passed.is_(True)))).scalar()
    if trials:
        await _raise_to(db, uid, "trial_pass", int(trials), {})
        from . import math_tree_progress as tp
        st = await tp.state(db, uid)
        await _raise_to(db, uid, "tree_nodes", sum(1 for v in st.status.values() if v == tp.DONE), {})
    user = await db.get(User, uid)
    if user is not None:
        await _raise_to(db, uid, "furnace", int((user.flags or {}).get("furnace", 1)), {})


async def sync(db: AsyncSession, user: User) -> list[dict]:
    """Backfill once, then unlock whatever the counters already reach (an achievement added in
    a later version starts where the player is). Returns the tiers unlocked with a toast."""
    out: list[dict] = []
    quiet = (user.flags or {}).get("ach_backfill") != BACKFILL_VERSION
    if quiet:
        await backfill(db, user.id)
        flags = dict(user.flags or {})
        flags["ach_backfill"] = BACKFILL_VERSION
        user.flags = flags
        await db.flush()
    counters = await _counters(db, user.id)
    rows = await _rows(db, user.id)
    for a in entries():
        r = reached(a["id"], counters.get(key_of(a), 0))
        row = rows.get(a["id"])
        if r > (row.tier if row else 0):
            await _reach(db, user.id, a, r, out, quiet)
    _queue(db, user.id, out)
    return out


# ------------------------------------------------------------------ the view
def _claimed(row: Achievement | None, n: int) -> bool:
    return bool(row and (int(row.claimed or 0) >> (n - 1)) & 1)


def points_of(rows: dict[str, Achievement]) -> int:
    total = 0
    for aid, row in rows.items():
        a = by_id().get(aid)
        if a:
            total += sum(int(t.get("points", 0)) for t in a["tiers"][:row.tier])
    return total


def _at_vi(a: dict, n: int) -> str:
    at = a["tiers"][n - 1]["at"]
    if a["counter"] == "cult":
        from . import loot
        return loot.label(loot.parse(at))
    return f"{int(at):,}".replace(",", ".")


def _progress_vi(a: dict, value: int) -> str:
    if a["counter"] == "cult":
        from . import loot
        return loot.label((value // 100, value % 100)) if value else "Phàm Nhân"
    return f"{value:,}".replace(",", ".")


def entry_view(a: dict, value: int, row: Achievement | None, tier_now) -> dict:
    tier = row.tier if row else 0
    revealed = not a.get("hidden") or tier > 0
    ths = thresholds(a["id"])
    tiers = []
    from . import loot
    for n, t in enumerate(a["tiers"], 1):
        got = n <= tier
        claimed = _claimed(row, n)
        req = req_of(a, n)
        ok = tier_now >= loot.parse(req)
        has = bool(reward_vi(t.get("reward")) and any(k != "title" for k in (t.get("reward") or {})))
        tiers.append({"n": n, "at": ths[n - 1], "at_vi": _at_vi(a, n) if revealed else "???",
                      "name_vi": tier_name(a, n) if revealed else "???", "points": int(t.get("points", 0)),
                      "reward_vi": reward_vi(t.get("reward")) if revealed else ["???"],
                      "reached": got, "claimed": claimed or (got and not has),
                      "claimable": got and has and not claimed and ok,
                      "req_vi": "" if ok else f"Cần đạt {loot.label(loot.parse(req))} để nhận."})
    nxt = ths[tier] if tier < len(ths) else ths[-1]
    prev = ths[tier - 1] if tier else 0
    if a["counter"] == "cult":    # progress of a realm is not a number: show where the player stands
        frac = 1.0 if tier >= len(ths) else 0.0
    else:
        frac = 1.0 if tier >= len(ths) else max(0.0, min(1.0, (value - prev) / max(1, nxt - prev)))
    return {"id": a["id"], "category": a["category"], "icon": a["icon"], "hidden": bool(a.get("hidden")),
            "revealed": revealed, "name_vi": a["name_vi"] if revealed else "???",
            "desc_vi": a["desc_vi"] if revealed else (a.get("hint_vi") or "Thiên cơ bất khả lộ."),
            "reveal_vi": a.get("reveal_vi", "") if revealed and a.get("hidden") else "",
            "tier": tier, "tiers": tiers, "max": len(ths), "done": tier >= len(ths),
            "value": value if revealed else 0, "next": nxt if revealed else 0,
            "progress_vi": (f"{_progress_vi(a, value)} / {_at_vi(a, min(tier + 1, len(ths)))}"
                            if revealed else "???"),
            "frac": round(frac, 4) if revealed else 0.0,
            "claimable": any(t["claimable"] for t in tiers),
            "points": sum(t["points"] for t in tiers if t["reached"]),
            "points_max": sum(t["points"] for t in tiers)}


def _milestones_view(points: int, user: User) -> list[dict]:
    got = set((user.flags or {}).get("ach_ms", []))
    return [{"points": m["points"], "reward_vi": reward_vi(m["reward"]), "reached": points >= m["points"],
             "claimed": m["points"] in got, "claimable": points >= m["points"] and m["points"] not in got}
            for m in data().get("milestones", [])]


async def view(db: AsyncSession, user: User) -> dict:
    """GET /achievements: every category with its achievements, the points, the milestones and
    the danh hiệu (Thành Tựu's and the library's) with the one worn."""
    from . import books, loot
    await sync(db, user)
    counters = await _counters(db, user.id)
    rows = await _rows(db, user.id)
    tier_now = loot.rank(*(await loot.player_tier(db, user.id)))
    items = [entry_view(a, counters.get(key_of(a), 0), rows.get(a["id"]), tier_now) for a in entries()]
    points = points_of(rows)
    cats = []
    for c in data()["categories"]:
        mine = [e for e in items if e["category"] == c["id"]]
        cats.append({"id": c["id"], "name_vi": c["name_vi"], "icon": c["icon"],
                     "done": sum(1 for e in mine if e["tier"] > 0), "total": len(mine),
                     "claimable": sum(1 for e in mine if e["claimable"]), "achievements": mine})
    ms = _milestones_view(points, user)
    nxt = next((m for m in ms if not m["reached"]), None)
    titles, _ = books.owned_badges(user)
    ach_titles = title_names()
    return {"points_name_vi": data()["points_name_vi"], "points": points,
            "points_max": sum(e["points_max"] for e in items), "categories": cats, "milestones": ms,
            "next_milestone": nxt, "claimable": sum(c["claimable"] for c in cats) + sum(m["claimable"] for m in ms),
            "done": sum(1 for e in items if e["tier"] > 0), "total": len(items),
            "titles": [{"title": t, "source": "thanh_tuu" if t in ach_titles else "tang_thu"} for t in titles],
            "title": books.worn(user)["title"]}


async def new_unlocks(db: AsyncSession, user: User) -> dict:
    """GET /achievements/new: every tier reached that the player has not been told of yet."""
    await sync(db, user)
    db.sync_session.info.pop("ach_out", None)       # returned here: no second copy over the socket
    out = []
    for aid, row in (await _rows(db, user.id)).items():
        a = by_id().get(aid)
        if a:
            out += [unlock_view(a, n) for n in range(int(row.seen or 0) + 1, row.tier + 1)]
    return {"unlocks": out}


async def mark_seen(db: AsyncSession, user: User, keys: list[str]) -> dict:
    """POST /achievements/seen: the toasts of these 'id:tier' were shown."""
    rows = await _rows(db, user.id)
    n_marked = 0
    for k in keys[:200]:
        aid, _, t = str(k).partition(":")
        row = rows.get(aid)
        if row is None or not t.isdigit():
            continue
        t = min(int(t), row.tier)
        if t > int(row.seen or 0):
            row.seen = t
            n_marked += 1
    return {"marked": n_marked}


# ------------------------------------------------------------------ claims
async def _grant(db: AsyncSession, uid: int, r: dict, ref: str) -> dict:
    from . import inventory, items
    got: dict = {}
    for cur in CURRENCIES:
        if r.get(cur):
            got[cur] = await inventory.change_currency(db, uid, cur, int(r[cur]), "achievement", ref)
    if r.get("items"):
        got["items"] = await items.grant_items(db, uid, r["items"], "achievement", ref)
    return got


async def _claim_one(db: AsyncSession, user: User, a: dict, n: int, row: Achievement | None, tier_now) -> dict:
    from . import loot
    if row is None or n > row.tier:
        raise AchievementError(400, "not_reached", "Con chưa đạt bậc thành tựu này.")
    if _claimed(row, n):
        raise AchievementError(409, "claimed", "Con đã nhận phần thưởng này rồi.")
    req = req_of(a, n)
    if tier_now < loot.parse(req):
        raise AchievementError(403, "locked", f"Phần thưởng này cần đạt {loot.label(loot.parse(req))} mới nhận được.")
    r = a["tiers"][n - 1].get("reward") or {}
    got = await _grant(db, user.id, r, f"{a['id']}:{n}")
    row.claimed = int(row.claimed or 0) | (1 << (n - 1))
    return {"id": a["id"], "tier": n, "rewards_vi": [x for x in reward_vi(r) if not x.startswith("Danh hiệu")], **got}


async def claim(db: AsyncSession, user: User, ach_id: str, tier: int) -> dict:
    from . import loot
    a = by_id().get(ach_id)
    if a is None or not 1 <= tier <= len(a["tiers"]):
        raise AchievementError(404, "no_achievement", "Không có thành tựu này.")
    row = await db.get(Achievement, (user.id, ach_id))
    tier_now = loot.rank(*(await loot.player_tier(db, user.id)))
    got = await _claim_one(db, user, a, tier, row, tier_now)
    await db.flush()
    return {"claimed": [got], "view": await view(db, user)}


async def claim_all(db: AsyncSession, user: User) -> dict:
    """Every tier and milestone that can be claimed now; the ones still locked by tu vi stay."""
    from . import loot
    await sync(db, user)
    tier_now = loot.rank(*(await loot.player_tier(db, user.id)))
    out = []
    for aid, row in (await _rows(db, user.id)).items():
        a = by_id().get(aid)
        if a is None:
            continue
        for n in range(1, row.tier + 1):
            if _claimed(row, n) or tier_now < loot.parse(req_of(a, n)):
                continue
            if not any(k != "title" for k in (a["tiers"][n - 1].get("reward") or {})):
                continue
            out.append(await _claim_one(db, user, a, n, row, tier_now))
    ms = []
    points = points_of(await _rows(db, user.id))
    for m in data().get("milestones", []):
        if points >= m["points"] and m["points"] not in (user.flags or {}).get("ach_ms", []):
            ms.append(await _claim_milestone(db, user, m))
    if not out and not ms:
        raise AchievementError(400, "nothing", "Chưa có phần thưởng nào để nhận.")
    await db.flush()
    return {"claimed": out, "milestones": ms, "view": await view(db, user)}


async def _claim_milestone(db: AsyncSession, user: User, m: dict) -> dict:
    got = await _grant(db, user.id, m["reward"], f"ms:{m['points']}")
    if m["reward"].get("title"):
        await _give_titles(db, user.id, [m["reward"]["title"]])
    flags = dict(user.flags or {})
    flags["ach_ms"] = sorted(set(flags.get("ach_ms", [])) | {m["points"]})
    user.flags = flags
    return {"points": m["points"], "rewards_vi": reward_vi(m["reward"]), **got}


async def claim_milestone(db: AsyncSession, user: User, points: int) -> dict:
    m = next((x for x in data().get("milestones", []) if x["points"] == points), None)
    if m is None:
        raise AchievementError(404, "no_milestone", "Không có mốc Đạo Tâm này.")
    if points in (user.flags or {}).get("ach_ms", []):
        raise AchievementError(409, "claimed", "Con đã nhận mốc này rồi.")
    if points_of(await _rows(db, user.id)) < points:
        raise AchievementError(400, "not_reached", f"Cần {points} {data()['points_name_vi']} để nhận mốc này.")
    got = await _claim_milestone(db, user, m)
    await db.flush()
    return {"milestone": got, "view": await view(db, user)}


# ------------------------------------------------------------------ the checks
def _icon_ok(icon) -> bool:
    if not (isinstance(icon, list) and len(icon) == 2):
        return False
    try:
        doc = json.loads((CLIENT_ICONS / f"{icon[0]}.json").read_text("utf-8"))
    except (OSError, ValueError):
        return False
    return icon[1] in (doc.get("icons") or {})


def _contexts() -> set[str]:
    out = set()
    for p in APP_DIR.rglob("*.py"):
        out |= set(re.findall(r'^(?:[A-Z_]*CONTEXT)\s*=\s*"([a-z_]+)"', p.read_text("utf-8"), re.M))
    return out


def dim_values(counter: str, dim: str) -> set[str] | None:
    """The values a 'where' may name, read from the catalogs (None: anything goes)."""
    from . import alchemy, beasts, weapons
    from ..realtime import lands
    mons = catalog.monsters().values()
    table = {
        ("answer_right", "context"): _contexts,
        ("kill", "rank"): lambda: {m.get("rank", "normal") for m in mons},
        ("kill_flawless", "rank"): lambda: {m.get("rank", "normal") for m in mons},
        ("kill", "subject"): lambda: {m["subject"] for m in mons if m.get("subject")},
        ("kill", "land"): lambda: {m["land"] for m in mons if m.get("land")},
        ("kill", "monster"): lambda: set(catalog.monsters()),
        ("weapon_get", "type"): lambda: set(weapons.data()["types"]),
        ("weapon_get", "quality"): lambda: set(weapons.quality_order()),
        ("weapon_forge", "quality"): lambda: set(weapons.quality_order()),
        ("beast_tame", "beast"): lambda: set(beasts._data()["all"]),
        ("brew", "quality"): lambda: {q["id"] for q in alchemy.cfg()["quality"]},
        ("lands", "land"): lambda: set(lands._lands()),
    }
    f = table.get((counter, dim))
    return f() if f else None


def domain(counter: str) -> int | None:
    """How high a count can go at all, for counters with a ceiling."""
    from . import alchemy, beasts, linh_can, weapons
    from ..learning import math_problems, math_tree
    from ..realtime import lands
    from ..realtime.world import zone_defs
    f = {"kill_kinds": lambda: len(catalog.monsters()), "weapon_types": lambda: len(weapons.data()["types"]),
         "lands": lambda: len(lands._lands()), "zones": lambda: len(zone_defs()),
         "code_solved": lambda: len(math_problems.bank()), "xa_truong": lambda: len(math_problems.bank()),
         "xa_truong_top": lambda: len(math_problems.bank()), "lc_book": lambda: len(linh_can.roots()),
         "lc_giai": lambda: 9, "lc_carry": lambda: 9, "beast_tame": lambda: len(beasts._data()["all"]),
         "weapon_claim": lambda: len(weapons.data()["placed"]), "tree_nodes": lambda: len(math_tree.tree().nodes),
         "furnace": lambda: max(f["level"] for f in alchemy.cfg()["furnace"])}.get(counter)
    return f() if f else None


def _emitted() -> set[str]:
    """RAW events some module of server/app really sends (a literal in an on_event/bump call)."""
    out = set()
    pat = re.compile(r'achievements\.(?:on_event|bump)\([^"\n]*"([a-z_]+)"')
    for p in APP_DIR.rglob("*.py"):
        if p.name == "achievements.py":
            continue
        out |= set(pat.findall(p.read_text("utf-8")))
    return out


def _check_reward(r: dict, req: str, where: str, errs: list[str]) -> None:
    from . import loot
    for k in r:
        if k not in ("spirit_stones", "immortal_jade", "items", "title"):
            errs.append(f"{where}: unknown reward {k!r}")
    for cur in CURRENCIES:
        if cur in r and (not isinstance(r[cur], int) or r[cur] <= 0):
            errs.append(f"{where}: {cur} must be a positive whole number")
    try:
        cap = loot.parse(req)
    except ValueError as e:
        errs.append(f"{where}: {e}")
        return
    for it in r.get("items", []):
        if catalog.stack_item(it.get("item", "")) is None:
            errs.append(f"{where}: item {it.get('item')!r} does not exist")
            continue
        if not isinstance(it.get("qty"), int) or it["qty"] <= 0:
            errs.append(f"{where}: item {it['item']} needs a positive qty")
        t = loot.item_tier(it["item"])
        if t is not None and t > cap:
            errs.append(f"{where}: {it['item']} unlocks at {loot.label(t)}, above the tier it is given at ({req})")
    if r.get("title") is not None:
        if not isinstance(r["title"], str) or not r["title"] or len(r["title"]) > TITLE_MAX:
            errs.append(f"{where}: a title is 1..{TITLE_MAX} characters")


def validate(raw: dict | None = None) -> list[str]:
    """Problems of data/achievements.json (empty = sound)."""
    d = raw if raw is not None else data()
    errs: list[str] = []
    achs = d.get("achievements", [])
    cats = {c["id"] for c in d.get("categories", [])}
    if len(achs) < MIN_ACHIEVEMENTS:
        errs.append(f"only {len(achs)} achievements, need at least {MIN_ACHIEVEMENTS}")
    for c in d.get("categories", []):
        if not c.get("name_vi") or not _icon_ok(c.get("icon")):
            errs.append(f"category {c.get('id')}: name_vi and an icon that exists are needed")
    ids = [a.get("id") for a in achs]
    names = [a.get("name_vi") for a in achs]
    for x in {i for i in ids if ids.count(i) > 1}:
        errs.append(f"achievement id {x!r} used twice")
    for x in {n for n in names if names.count(n) > 1}:
        errs.append(f"achievement name {x!r} used twice")
    titles: list[str] = []
    emitted = _emitted()
    for name in RAW:
        if name not in emitted:
            errs.append(f"event {name!r} ({RAW[name]}) is not sent by any call site in server/app")
    used = set()
    for a in achs:
        w = f"achievement {a.get('id')}"
        if not a.get("id") or len(a["id"]) > 40 or not re.fullmatch(r"[a-z0-9_]+", a["id"]):
            errs.append(f"{w}: id must be 1..40 of a-z 0-9 _")
        if a.get("category") not in cats:
            errs.append(f"{w}: unknown category {a.get('category')!r}")
        if not a.get("name_vi") or len(a["name_vi"]) > NAME_MAX:
            errs.append(f"{w}: name_vi must be 1..{NAME_MAX} characters")
        if not a.get("desc_vi"):
            errs.append(f"{w}: desc_vi is missing")
        if a.get("hidden") and not a.get("reveal_vi"):
            errs.append(f"{w}: a hidden achievement needs reveal_vi")
        if not _icon_ok(a.get("icon")):
            errs.append(f"{w}: icon {a.get('icon')!r} is not in client/assets/v2/icons")
        counter = a.get("counter")
        if counter not in COUNTERS:
            errs.append(f"{w}: unknown counter {counter!r}")
            continue
        used.add(counter)
        where = a.get("where") or {}
        if len(where) > 1:
            errs.append(f"{w}: 'where' takes one field")
        for dim, val in where.items():
            if dim not in COUNTERS[counter].dims:
                errs.append(f"{w}: {counter} cannot be filtered by {dim!r}")
                continue
            allowed = dim_values(counter, dim)
            if allowed is not None and val not in allowed:
                errs.append(f"{w}: {dim}={val!r} is not a known value")
        tiers = a.get("tiers") or []
        if not tiers:
            errs.append(f"{w}: no tiers")
            continue
        try:
            ths = [threshold(a, t["at"]) for t in tiers]
        except (KeyError, ValueError, TypeError) as e:
            errs.append(f"{w}: bad threshold ({e})")
            continue
        if any(x <= 0 for x in ths) or any(b <= a_ for a_, b in zip(ths, ths[1:])):
            errs.append(f"{w}: thresholds must be positive and strictly rising")
        top = domain(counter)
        if top is not None and ths[-1] > top:
            errs.append(f"{w}: the last threshold {ths[-1]} is above what can be reached ({top})")
        for n, t in enumerate(tiers, 1):
            if not isinstance(t.get("points"), int) or t["points"] <= 0:
                errs.append(f"{w} tier {n}: points must be a positive whole number")
            r = t.get("reward") or {}
            if not r:
                errs.append(f"{w} tier {n}: no reward")
            _check_reward(r, req_of(a, n), f"{w} tier {n}", errs)
            if r.get("title"):
                titles.append(r["title"])
        for s in _strings(a):
            if CJK.search(s):
                errs.append(f"{w}: no Chinese characters ({s!r})")
    for c in COUNTERS:
        if c not in used:
            errs.append(f"counter {c!r} is read by no achievement (remove it or use it)")
    pts = [m.get("points") for m in d.get("milestones", [])]
    if not pts or any(not isinstance(p, int) or p <= 0 for p in pts) or pts != sorted(set(pts)):
        errs.append("milestones: points must be positive, distinct and rising")
    total = sum(int(t.get("points", 0)) for a in achs for t in a.get("tiers", []))
    if pts and pts[-1] > total:
        errs.append(f"milestones: the last one ({pts[-1]}) is above every point there is ({total})")
    for m in d.get("milestones", []):
        _check_reward(m.get("reward") or {}, m.get("req", "pham_nhan"), f"milestone {m.get('points')}", errs)
        if (m.get("reward") or {}).get("title"):
            titles.append(m["reward"]["title"])
    for t in {t for t in titles if titles.count(t) > 1}:
        errs.append(f"title {t!r} is given twice")
    if not d.get("points_name_vi"):
        errs.append("points_name_vi is missing")
    return errs


def _strings(node) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, dict):
        return [s for v in node.values() for s in _strings(v)]
    if isinstance(node, list):
        return [s for v in node for s in _strings(v)]
    return []
