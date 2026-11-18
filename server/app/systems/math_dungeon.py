"""Hầm ngục (M10, kế hoạch 4.3): "sinh ngẫu nhiên theo hạt giống; mỗi phòng một dạng câu".

A dungeon is a short chain of rooms on one floor of the learning path. Its **layout** - how
many rooms, the kind of each room and their order, the micro-skill a room asks about, the
name of whoever guards it, and the chest at the end - is a pure function of
(seed, subject, floor) and the data (`generate`). The same seed gives the same dungeon, so a
player can replay one or share it. The *questions* are not part of the seed: they are picked
when the room is entered, through math_ask, at the player's own tier and with the player's own
anti-repeat window, like every other question of the game.

  * A room is one question type (data/math/dungeon.json `room_kinds`, one per playable type).
    Its questions come from the room's micro-skill. A room is only generated when it can be
    asked by *anyone* standing on that floor: its (type, micro-skill) has a template at the
    floor's lowest tier, which is always open (math_adaptive.open_tier). A player whose tier
    is higher gets the harder template - the tier is theirs, never above it (math_ask.pick).
  * The last room is the trấn thủ: the hardest question this player may be asked of that
    type on the floor (`highest=True`), from every micro-skill of the floor.
  * The delver starts with a few tâm lực. A wrong answer or a timeout costs one (plan 4.4:
    running out of time is a wrong answer); at zero the run is over. A room is cleared by
    `questions_per_room` right answers; each cleared room pays its small reward at once and
    the trấn thủ opens the chest. Nothing earned is ever taken back ("không mất đồ"): a lost
    or abandoned run keeps what it paid.
  * One open run per player, like a buổi luyện. A question left open when the game was
    closed is waiting on return; one whose time ran out meanwhile is settled as a timeout
    the next time the run is looked at, which costs its tâm lực like any other timeout.
  * Daily limit, cheap and in data: the first `rewards_per_day` runs started in a UTC day pay
    Linh Thạch and materials; later runs still play and still pay Tu Vi (that is the learning,
    not the loot).

Every answer goes to `math_answers` with no run (math_ask.record), so the dungeon counts for
the learning path. Tu Vi is paid by tier through math_ask.xp_rule.
"""
from __future__ import annotations

import datetime as dt
import json
import random
from functools import lru_cache

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import DATA_DIR
from ..learning import math_items, math_path, quiz
from ..models import MathDungeonRun, QuizSession, User
from . import catalog, inventory, math_ask, math_practice

CONTEXT = "math_dungeon"
DATA_FILE = DATA_DIR / "math" / "dungeon.json"
OPEN, CLEARED, FAILED, ABANDONED = "open", "cleared", "failed", "abandoned"
REASON = "math_dungeon"


class DungeonError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the data
def _read() -> dict:
    return json.loads(DATA_FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    """dungeon.json without its comment. It is checked by validate() in the tests and in
    tools/check_all.py, so the game itself trusts it."""
    return {k: v for k, v in _read().items() if not k.startswith("_")}


def _whole(v, lo: int = 0) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v >= lo


def _text(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _reward_problems(where: str, r, drops: dict) -> list[str]:
    out = []
    if not isinstance(r, dict) or set(r) - {"name_vi", "stones", "items"} or "stones" not in r or "items" not in r:
        return [f"{where}: must be {{stones, items}} (a chest also has name_vi)"]
    if not _whole(r["stones"]):
        out.append(f"{where}: stones must be a whole number >= 0")
    if not isinstance(r["items"], dict):
        return out + [f"{where}: items must be an object {{item: qty}}"]
    for item, qty in r["items"].items():
        info = drops.get(item)
        if info is None:
            out.append(f"{where}: {item!r} is not in data/math/drops.json")
        elif info.get("kind") != "material":
            out.append(f"{where}: {item!r} is a {info.get('kind')}, only materials may be given here")
        if not _whole(qty, 1):
            out.append(f"{where}: {item} needs a qty >= 1")
    return out


def validate(raw: dict | None = None, drops: dict | None = None) -> list[str]:
    """One readable line per problem in dungeon.json; empty when it is sound. Also checks
    that every floor with questions can generate a dungeon (some room kind is askable there
    at the floor's lowest tier) and has its rewards."""
    raw = _read() if raw is None else raw
    drops = catalog.math_drops() if drops is None else drops
    out: list[str] = []
    for key in ("hearts", "questions_per_room", "warden_questions", "rewards_per_day"):
        if not _whole(raw.get(key), 1 if key != "rewards_per_day" else 0):
            out.append(f"{key} must be a whole number >= {1 if key != 'rewards_per_day' else 0}")
    if not _whole(raw.get("seed_max"), 1):
        out.append("seed_max must be a whole number >= 1")
    rooms = raw.get("rooms")
    if (not isinstance(rooms, dict) or set(rooms) != {"min", "max"} or not _whole(rooms["min"], 2)
            or not _whole(rooms["max"], 2) or rooms["min"] > rooms["max"]):
        out.append("rooms must be {min, max} with 2 <= min <= max (the last room is the trấn thủ)")
    kinds = raw.get("room_kinds")
    if not isinstance(kinds, dict):
        out.append("room_kinds must be an object")
        kinds = {}
    for q in math_items.PLAYABLE_TYPES:
        if q not in kinds:
            out.append(f"room_kinds: no room for the question type {q}")
    for q, k in kinds.items():
        if q not in math_items.PLAYABLE_TYPES:
            out.append(f"room_kinds: {q!r} is not a playable question type")
        if not isinstance(k, dict) or set(k) != {"name_vi", "short_vi", "desc_vi"} or not all(map(_text, k.values())):
            out.append(f"room_kinds.{q}: must be {{name_vi, short_vi, desc_vi}}, all non-empty text")
    for key in ("guardians", "wardens"):
        table = raw.get(key)
        if not isinstance(table, list) or not table:
            out.append(f"{key} must be a non-empty list")
            continue
        for i, g in enumerate(table):
            if not isinstance(g, dict) or set(g) != {"name_vi", "flavour_vi"} or not all(map(_text, g.values())):
                out.append(f"{key}[{i}]: must be {{name_vi, flavour_vi}}, both non-empty text")
    rewards = raw.get("rewards")
    if not isinstance(rewards, dict):
        return out + ["rewards must be an object by floor"]
    for floor, r in rewards.items():
        here = f"rewards.{floor}"
        if not isinstance(r, dict) or set(r) != {"room", "chests"}:
            out.append(f"{here}: must be {{room, chests}}")
            continue
        out += _reward_problems(f"{here}.room", r["room"], drops)
        if not isinstance(r["chests"], list) or not r["chests"]:
            out.append(f"{here}.chests: must be a non-empty list")
            continue
        for i, c in enumerate(r["chests"]):
            out += _reward_problems(f"{here}.chests[{i}]", c, drops)
            if isinstance(c, dict) and not _text(c.get("name_vi")):
                out.append(f"{here}.chests[{i}]: needs a name_vi")
    for subject in math_path.subjects():
        for f in subject.main_floors:
            if not math_practice._templates(subject.id, f.number):
                continue
            if not askable(subject.id, f.number):
                out.append(f"{subject.id} floor {f.number}: has questions but no room kind can be asked there")
            if str(f.number) not in rewards:
                out.append(f"rewards: floor {f.number} has questions but no rewards")
    return out


# ------------------------------------------------------------------ the layout (pure)
def askable(subject_id: str, floor: int) -> dict[str, list[str]]:
    """question type -> the micro-skills of this floor (path order) that have a template of
    that type at the floor's lowest tier: the rooms anyone standing on the floor can be
    asked. Types with none are left out."""
    lo, _ = math_path.floor_tiers(floor)
    templates = math_practice._templates(subject_id, floor)
    order = [k.id for k in math_path.subject(subject_id).floor(floor).skills]
    out = {}
    for qtype in math_items.PLAYABLE_TYPES:
        have = {t.skill for t in templates if t.qtype == qtype and t.tier == lo}
        if have:
            out[qtype] = [s for s in order if s in have]
    return out


def _deal(rng: random.Random, pool: list, n: int, avoid_first=None) -> list:
    """n entries from `pool`, every entry once before any repeats, never the same entry
    twice in a row when the pool has more than one (`avoid_first` is the one before)."""
    out: list = []
    bag: list = []
    while len(out) < n:
        if not bag:
            bag = list(pool)
            rng.shuffle(bag)
        last = out[-1] if out else avoid_first
        if len(bag) > 1 and bag[0] == last:
            bag.append(bag.pop(0))
        out.append(bag.pop(0))
    return out


def generate(seed: int, subject_id: str, floor: int, raw: dict | None = None) -> dict | None:
    """The dungeon of this seed on this floor, or None when the floor has nothing to ask.

    A pure function of (seed, subject, floor) and the data: no clock, no player. Everything
    a client needs to draw the map is in it, names included, so a run keeps the dungeon it
    was started with even if the data changes under it."""
    d = data() if raw is None else raw
    kinds = askable(subject_id, floor)
    if not kinds:
        return None
    rng = random.Random(f"ham_nguc|{int(seed)}|{subject_id}|{int(floor)}")
    n = rng.randint(d["rooms"]["min"], d["rooms"]["max"])
    subject = math_path.subject(subject_id)
    names = d["room_kinds"]
    order = _deal(rng, sorted(kinds), n - 1)
    guardians = _deal(rng, list(range(len(d["guardians"]))), n - 1)
    used: set[str] = set()
    rooms = []
    for kind, g in zip(order, guardians):
        fresh = [s for s in kinds[kind] if s not in used] or kinds[kind]
        skill = rng.choice(fresh)
        used.add(skill)
        rooms.append(_room(kind, names[kind], skill, subject.skills[skill].name_vi, d["guardians"][g],
                           False, d["questions_per_room"]))
    kind = _deal(rng, sorted(kinds), 1, avoid_first=order[-1] if order else None)[0]
    warden = d["wardens"][rng.randrange(len(d["wardens"]))]
    rooms.append(_room(kind, names[kind], None, None, warden, True, d["warden_questions"]))
    rewards = d["rewards"].get(str(floor), {"room": {"stones": 0, "items": {}}, "chests": []})
    chest = (dict(rewards["chests"][rng.randrange(len(rewards["chests"]))]) if rewards["chests"]
             else {"name_vi": "", "stones": 0, "items": {}})
    return {"seed": int(seed), "subject_id": subject_id, "floor": int(floor),
            "floor_title_vi": subject.floor(floor).title_vi, "rooms": rooms,
            "room_reward": {"stones": rewards["room"]["stones"], "items": dict(rewards["room"]["items"])},
            "chest": {"name_vi": chest.get("name_vi", ""), "stones": chest["stones"], "items": dict(chest["items"])}}


def _room(kind: str, names: dict, skill: str | None, skill_vi: str | None, keeper: dict, warden: bool,
          need: int) -> dict:
    return {"kind": kind, "name_vi": names["name_vi"], "short_vi": names["short_vi"], "desc_vi": names["desc_vi"],
            "skill": skill, "skill_name_vi": skill_vi, "guardian_vi": keeper["name_vi"],
            "flavour_vi": keeper["flavour_vi"], "warden": warden, "need": need}


# ------------------------------------------------------------------ views
def _items_view(items: dict) -> list[dict]:
    return [{"item_id": k, "name_vi": (catalog.stack_item(k) or {}).get("name_vi", k), "qty": int(v)}
            for k, v in items.items()]


def _reward_view(r: dict) -> dict:
    return {"stones": int(r["stones"]), "items": _items_view(r["items"])}


def run_view(run: MathDungeonRun) -> dict:
    lay = run.layout
    types = math_path.question_types()
    ended = run.ended_at is not None
    rooms = []
    for i, r in enumerate(lay["rooms"]):
        if i < run.room:
            state = "cleared"
        elif i == run.room:
            state = "lost" if run.state == FAILED else ("left" if run.state == ABANDONED else "current")
        else:
            state = "ahead"
        rooms.append({**r, "index": i, "qtype_vi": types[r["kind"]]["name_vi"], "state": state,
                      "progress": run.progress if i == run.room and not ended else (r["need"] if i < run.room else 0)})
    return {"run_id": run.id, "seed": run.seed, "subject_id": run.subject_id,
            "subject_name_vi": math_path.subject(run.subject_id).name_vi, "floor": run.floor,
            "floor_title_vi": lay.get("floor_title_vi", ""), "rooms": rooms, "room": run.room,
            "rooms_cleared": min(run.room, len(lay["rooms"])), "total_rooms": len(lay["rooms"]),
            "hearts": run.hearts, "max_hearts": run.max_hearts, "state": run.state, "ended": ended,
            "asked": run.asked, "correct": run.correct, "xp_gained": run.xp_gained,
            "stones_gained": run.stones_gained, "items_gained": _items_view(run.items_gained or {}),
            "rewarded": run.rewarded, "room_reward": _reward_view(lay["room_reward"]),
            "chest": {"name_vi": lay["chest"]["name_vi"], **_reward_view(lay["chest"])},
            "chest_opened": run.state == CLEARED}


def layout_view(layout: dict) -> dict:
    types = math_path.question_types()
    return {**layout, "rooms": [{**r, "index": i, "qtype_vi": types[r["kind"]]["name_vi"]}
                                for i, r in enumerate(layout["rooms"])],
            "room_reward": _reward_view(layout["room_reward"]),
            "chest": {"name_vi": layout["chest"]["name_vi"], **_reward_view(layout["chest"])}}


def _day_start(now: dt.datetime) -> dt.datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


async def rewarded_today(db: AsyncSession, user_id: int) -> int:
    """Runs started today (UTC) that pay rewards."""
    return (await db.execute(select(func.count()).select_from(MathDungeonRun).where(
        MathDungeonRun.user_id == user_id, MathDungeonRun.rewarded.is_(True),
        MathDungeonRun.started_at >= _day_start(clock.now())))).scalar_one()


async def floors_open(db: AsyncSession, user_id: int, subject_id: str) -> list[int]:
    """The floors this player may delve on: the ones with questions, up to their open floor
    (rule 2: never a floor the player has not reached)."""
    here = await math_ask.open_floor(db, user_id, subject_id)
    return [n for n in math_ask.playable_floors(subject_id) if n <= here]


async def open_run(db: AsyncSession, user_id: int) -> MathDungeonRun | None:
    return (await db.execute(select(MathDungeonRun).where(MathDungeonRun.user_id == user_id,
                                                          MathDungeonRun.ended_at.is_(None))
                             .order_by(MathDungeonRun.id.desc()))).scalars().first()


async def view(db: AsyncSession, user: User) -> dict:
    """GET /math/dungeon: the floors (and why a floor is shut), today's rewarded runs, and the
    run the player left open, after settling a question whose time ran out meanwhile."""
    d = data()
    subject_id = math_ask.first_subject()
    run = await open_run(db, user.id)
    if run is not None:
        await _settle_expired(db, user, run)
    out = {"subject_id": subject_id, "subject_name_vi": None, "floors": [], "own_floor": None,
           "run": run_view(run) if run is not None else None, "hearts": d["hearts"],
           "rewards_per_day": d["rewards_per_day"], "seed_max": d["seed_max"],
           "rewards_left": max(0, d["rewards_per_day"] - await rewarded_today(db, user.id))}
    if subject_id is None:
        return out
    subject = math_path.subject(subject_id)
    reachable = await floors_open(db, user.id, subject_id)
    playable = set(math_ask.playable_floors(subject_id))
    for f in subject.main_floors:
        locked = (None if f.number in reachable else
                  "Tầng này chưa có câu hỏi." if f.number not in playable else
                  "Chưa tới tầng này trên lộ trình học.")
        out["floors"].append({"floor": f.number, "title_vi": f.title_vi, "open": locked is None, "locked_vi": locked})
    out.update(subject_name_vi=subject.name_vi, own_floor=reachable[-1] if reachable else None)
    return out


async def _where(db: AsyncSession, user: User, floor: int | None) -> tuple[str, int]:
    subject_id = math_ask.first_subject()
    if subject_id is None:
        raise DungeonError(400, "no_questions", "Chưa có câu hỏi nào để mở hầm ngục.")
    reachable = await floors_open(db, user.id, subject_id)
    if not reachable:
        raise DungeonError(400, "no_questions", "Chưa có câu hỏi nào để mở hầm ngục.")
    if floor is None:
        return subject_id, reachable[-1]
    if floor not in reachable:
        if floor in math_ask.playable_floors(subject_id):
            raise DungeonError(403, "floor_locked", "Chưa tới tầng này trên lộ trình học.")
        raise DungeonError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    return subject_id, floor


def _seed(seed: int | None, rng: random.Random | None) -> int:
    top = data()["seed_max"]
    if seed is None:
        return (rng or random.SystemRandom()).randint(0, top)
    if not 0 <= seed <= top:
        raise DungeonError(400, "bad_seed", f"Số khắc trên linh thạch là một số từ 0 đến {top}.")
    return int(seed)


async def preview(db: AsyncSession, user: User, seed: int, floor: int | None = None) -> dict:
    """The map of a seed on a floor the player has reached, without entering it."""
    subject_id, floor = await _where(db, user, floor)
    layout = generate(_seed(seed, None), subject_id, floor)
    if layout is None:
        raise DungeonError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    return {"layout": layout_view(layout)}


# ------------------------------------------------------------------ a run
async def start(db: AsyncSession, user: User, seed: int | None = None, floor: int | None = None,
                rng: random.Random | None = None) -> dict:
    """Open a dungeon. Without a seed the server draws one and returns it. A run the player
    left open is abandoned (one run at a time) and keeps what it paid."""
    subject_id, floor = await _where(db, user, floor)
    seed = _seed(seed, rng)
    layout = generate(seed, subject_id, floor)
    if layout is None:
        raise DungeonError(400, "no_questions", "Tầng này chưa có câu hỏi.")
    now = clock.now()
    for old in (await db.execute(select(MathDungeonRun).where(MathDungeonRun.user_id == user.id,
                                                              MathDungeonRun.ended_at.is_(None)))).scalars():
        old.state, old.ended_at = ABANDONED, now
    d = data()
    rewarded = await rewarded_today(db, user.id) < d["rewards_per_day"]
    run = MathDungeonRun(user_id=user.id, seed=seed, subject_id=subject_id, floor=floor, layout=layout,
                         room=0, progress=0, hearts=d["hearts"], max_hearts=d["hearts"], state=OPEN,
                         asked=0, correct=0, xp_gained=0, stones_gained=0, items_gained={},
                         rewarded=rewarded, started_at=now)
    db.add(run)
    await db.flush()
    return {"run": run_view(run)}


async def _own_run(db: AsyncSession, user: User, run_id: int) -> MathDungeonRun:
    run = (await db.execute(select(MathDungeonRun).where(MathDungeonRun.id == run_id)
                            .with_for_update())).scalar_one_or_none()
    if run is None or run.user_id != user.id:
        raise DungeonError(404, "no_run", "Không tìm thấy hầm ngục này.")
    return run


async def get_run(db: AsyncSession, user: User, run_id: int) -> MathDungeonRun:
    """One run of this player, open or ended."""
    run = await db.get(MathDungeonRun, run_id)
    if run is None or run.user_id != user.id:
        raise DungeonError(404, "no_run", "Không tìm thấy hầm ngục này.")
    return run


def _ref(run: MathDungeonRun) -> str:
    return f"{run.id}|{run.room}"


async def _settle_expired(db: AsyncSession, user: User, run: MathDungeonRun) -> None:
    """A question of this run whose time ran out while nobody answered it (the game was
    closed) is a timeout, and a timeout is a wrong answer (rule 4): it is graded as one now,
    so it is logged and costs its tâm lực. Otherwise closing the game would dodge a question."""
    now = clock.now()
    stale = (await db.execute(select(QuizSession.id).where(
        QuizSession.user_id == user.id, QuizSession.context == CONTEXT, QuizSession.ref == _ref(run),
        QuizSession.answered_at.is_(None), QuizSession.expires_at <= now))).scalars().all()
    for sid in stale:
        if run.ended_at is not None:
            break
        await quiz.answer(db, user, sid, {"timed_out": True})


async def next_question(db: AsyncSession, user: User, run_id: int, rng: random.Random | None = None) -> dict:
    """Enter the current room, or its next question; the open question if one is waiting.
    `question` is None when a timeout settled just now has ended the run."""
    run = await _own_run(db, user, run_id)
    if run.ended_at is not None:
        raise DungeonError(409, "run_ended", "Hầm ngục này đã kết thúc.")
    await _settle_expired(db, user, run)
    if run.ended_at is not None:
        return {"run": run_view(run), "question": None}
    pending = (await db.execute(select(QuizSession).where(
        QuizSession.user_id == user.id, QuizSession.context == CONTEXT, QuizSession.ref == _ref(run),
        QuizSession.answered_at.is_(None), QuizSession.expires_at > clock.now())
        .order_by(QuizSession.created_at.desc()))).scalars().first()
    if pending is not None:
        return {"run": run_view(run), "question": quiz.public_session(pending)}
    room = run.layout["rooms"][run.room]
    question = await math_ask.pick(db, user, run.subject_id, run.floor,
                                   skills=[room["skill"]] if room["skill"] else None,
                                   qtypes=[room["kind"]], highest=room["warden"], rng=rng)
    if question is None:          # generate() makes only rooms that can be asked: data changed under the run
        raise DungeonError(409, "no_question", "Phòng này không còn câu hỏi nào. Hãy rời hầm và vào lại.")
    question.meta["dungeon"] = {"room": run.room, "rooms": len(run.layout["rooms"]), "name_vi": room["name_vi"],
                                "guardian_vi": room["guardian_vi"], "warden": room["warden"]}
    out = await quiz.create_session(db, user, CONTEXT, question, ref=_ref(run))
    return {"run": run_view(run), "question": out}


async def abandon(db: AsyncSession, user: User, run_id: int) -> dict:
    """Leave the dungeon. What was paid stays paid; an open question simply expires."""
    run = await _own_run(db, user, run_id)
    if run.ended_at is None:
        run.state, run.ended_at = ABANDONED, clock.now()
    return {"run": run_view(run)}


# ------------------------------------------------------------------ after an answer
async def _grant(db: AsyncSession, user_id: int, run: MathDungeonRun, reward: dict, what: str) -> dict:
    """Pay one room's reward or the chest - unless today's rewarded runs are used up."""
    if not run.rewarded:
        return {"stones": 0, "items": [], "withheld": True}
    ref = f"{run.id}|{what}"
    if reward["stones"]:
        await inventory.change_currency(db, user_id, "spirit_stones", int(reward["stones"]), REASON, ref)
        run.stones_gained += int(reward["stones"])
    items = dict(run.items_gained or {})
    for item, qty in reward["items"].items():
        await inventory.change_item(db, user_id, item, int(qty), REASON, ref)
        items[item] = items.get(item, 0) + int(qty)
    run.items_gained = items          # (a new dict, so the JSON column sees the change)
    return {"stones": int(reward["stones"]), "items": _items_view(reward["items"]), "withheld": False}


async def _after_answer(db: AsyncSession, user_id: int, run: MathDungeonRun, correct: bool,
                        now: dt.datetime) -> dict:
    lay = run.layout
    rooms = lay["rooms"]
    out = {"correct": correct, "room": run.room, "room_cleared": False, "reward": None, "chest": None,
           "heart_lost": False}
    run.asked += 1
    if correct:
        run.correct += 1
        run.progress += 1
        if run.progress >= rooms[run.room]["need"]:
            last = run.room == len(rooms) - 1
            out["room_cleared"] = True
            granted = await _grant(db, user_id, run, lay["chest"] if last else lay["room_reward"],
                                   "chest" if last else f"room{run.room}")
            out["chest" if last else "reward"] = granted
            run.room += 1
            run.progress = 0
            if last:
                run.state, run.ended_at = CLEARED, now
    else:
        run.hearts = max(0, run.hearts - 1)
        out["heart_lost"] = True
        if run.hearts == 0:
            run.state, run.ended_at = FAILED, now
    out["run"] = run_view(run)
    return out


async def dungeon_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    """Grading a dungeon question (answered or timed out): the learning log first, then the run."""
    out: dict = {"math": await math_ask.record(db, user, s, correct, now)}
    run_id, _, room = (s.ref or "").partition("|")
    run = (await db.execute(select(MathDungeonRun).where(MathDungeonRun.id == int(run_id))
                            .with_for_update())).scalar_one_or_none() if run_id.isdigit() else None
    if run is None or run.user_id != user.id:
        return out
    if run.ended_at is not None or str(run.room) != room:     # left, or already settled: only the log
        out["dungeon"] = {"stale": True, "run": run_view(run)}
        return out
    out["dungeon"] = await _after_answer(db, user.id, run, correct, now)
    return out


async def _on_xp(db: AsyncSession, s: QuizSession, gained: int) -> None:
    run_id = (s.ref or "").partition("|")[0]
    run = await db.get(MathDungeonRun, int(run_id)) if run_id.isdigit() else None
    if run is not None:
        run.xp_gained += int(gained)


quiz.register_handler(CONTEXT, dungeon_handler)
quiz.register_xp_rule(CONTEXT, math_ask.xp_rule, _on_xp)
