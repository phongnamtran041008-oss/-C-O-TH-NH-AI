"""Cơ duyên (M10, kế hoạch 4.3): a chance event that comes after right answers - an old
cultivator who poses one hard question, a sealed chest that wants a short chain answered - and
pays a rare reward. All the numbers and texts are in data/math/fortune.json.

When one appears. Every right math answer written to the log in the field or in a buổi luyện
(math_combat.record, math_practice.math_handler: both call `math_combat.notify_answer`) adds one
to a small counter. At the threshold the counter goes back to 0 and a seeded roll decides
whether a cơ duyên is offered, and which one (by weight). Never while an offer is open, and at
most `daily_limit` offers a day (server clock, UTC+7). The answers of a cơ duyên itself do not
feed the counter, or one cơ duyên could breed the next.

What it asks. Questions come only from `math_ask` (the learning rules of M7/M9): the tier is the
player's own and never above it, from the player's own floor, and every answer is written to
`math_answers` with no run. An elder asks the hardest question the player may be asked
(`highest=True`); a chest asks `count` questions of its stated types, all must be right.

Losing. A wrong answer, a timeout, a lapsed offer: no reward and nothing is lost (plan 4.4).

State is small and lives in `users.flags["math_fortune"]`:
  {date, offers, count, open: {event, expires_at, accepted, step, sid}|None, log: [...]}.
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import random
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import DATA_DIR
from ..learning import math_items, math_path, quiz
from ..models import QuizSession, User
from . import catalog, inventory, math_ask, math_combat

CONTEXT = "math_fortune"
FILE = DATA_DIR / "math" / "fortune.json"
FLAG = "math_fortune"
KINDS = ("elder", "chest")

_rng = random.Random()


def seed(n: int | None) -> None:
    """Seed the one random source of this module (tests, the bot)."""
    global _rng
    _rng = random.Random(n)


class FortuneError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the data
def _read() -> dict:
    return json.loads(FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    """fortune.json without its comment. validate() checks it in the tests and in
    tools/check_all.py, so the game itself trusts it."""
    return {k: v for k, v in _read().items() if not k.startswith("_")}


def trigger() -> dict:
    return data()["trigger"]


def events() -> dict[str, dict]:
    return {e["id"]: e for e in data()["events"]}


def _number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _int(v, lo: int | None = None) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and (lo is None or v >= lo)


def _text(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def validate(raw: dict | None = None) -> list[str]:
    """One readable line per problem in fortune.json; empty when it is sound."""
    raw = _read() if raw is None else raw
    out: list[str] = []
    t = raw.get("trigger")
    if not isinstance(t, dict):
        out.append("trigger must be an object")
    else:
        for key in ("right_answers", "daily_limit", "log_size"):
            if not _int(t.get(key), 1):
                out.append(f"trigger.{key} must be an integer >= 1")
        for key in ("expires_seconds", "play_seconds"):
            if not _number(t.get(key)) or t[key] <= 0:
                out.append(f"trigger.{key} must be a number > 0")
        if not _number(t.get("chance")) or not (0 < t["chance"] <= 1):
            out.append("trigger.chance must be a number in (0, 1]")
    if not _text(raw.get("how_vi")):
        out.append("how_vi must be a non-empty string")
    table = raw.get("events")
    if not isinstance(table, list) or len(table) < 4:
        return out + ["events must be a list of at least four events"]
    if not any(isinstance(e, dict) and e.get("kind") == "elder" for e in table) or \
            not any(isinstance(e, dict) and e.get("kind") == "chest" for e in table):
        out.append("events must hold at least one elder and one chest")
    qtypes = math_path.question_types()
    seen: set[str] = set()
    for e in table:
        if not isinstance(e, dict):
            out.append("an event must be an object")
            continue
        here = f"event {e.get('id')}"
        if not _text(e.get("id")) or e["id"] in seen:
            out.append(f"{here}: id must be a unique non-empty string")
        seen.add(str(e.get("id")))
        if e.get("kind") not in KINDS:
            out.append(f"{here}: kind must be one of {', '.join(KINDS)}")
        for key in ("name_vi", "intro_vi", "win_vi", "lose_vi"):
            if not _text(e.get(key)):
                out.append(f"{here}: {key} must be a non-empty string")
        if not _number(e.get("weight")) or e["weight"] <= 0:
            out.append(f"{here}: weight must be a number > 0")
        if e.get("reviewed", False) not in (True, False):
            out.append(f"{here}: reviewed must be true or false")
        out += _validate_question(here, e, qtypes)
        out += _validate_rewards(here, e.get("rewards"))
    return out


def _validate_question(here: str, e: dict, qtypes: dict) -> list[str]:
    q = e.get("question")
    if not isinstance(q, dict) or not isinstance(q.get("qtypes"), list) or not q["qtypes"]:
        return [f"{here}: question must be {{qtypes: [..], count: n}}"]
    out = []
    for qt in q["qtypes"]:
        if qt not in qtypes:
            out.append(f"{here}: {qt!r} is not a question type of balance/math.json")
        elif qt not in math_items.PLAYABLE_TYPES:
            out.append(f"{here}: {qt!r} cannot be played yet")
        elif not _askable_to_a_beginner(qt):
            out.append(f"{here}: no {qt} question at tier 1 of the first playable floor")
    if not _int(q.get("count"), 1) or q["count"] > 5:
        out.append(f"{here}: question.count must be an integer 1..5")
    elif e.get("kind") == "elder" and q["count"] != 1:
        out.append(f"{here}: an elder poses exactly one question")
    return out


def _askable_to_a_beginner(qtype: str) -> bool:
    """A new player (tier 1) must be able to get this type, or the event could never be played."""
    subject = math_ask.first_subject()
    if subject is None:
        return False
    from . import math_practice
    return any(t.qtype == qtype and t.tier == 1 for t in math_practice._templates(subject, 1))


def _validate_rewards(here: str, r) -> list[str]:
    if not isinstance(r, dict):
        return [f"{here}: rewards must be an object"]
    out = []
    st = r.get("stones")
    if not (isinstance(st, list) and len(st) == 2 and all(_int(x, 0) for x in st) and st[0] <= st[1]):
        out.append(f"{here}: rewards.stones must be [lo, hi] with 0 <= lo <= hi")
    items = r.get("items")
    if not isinstance(items, list):
        out.append(f"{here}: rewards.items must be a list")
        items = []
    for i in items:
        if not isinstance(i, dict) or catalog.stack_item(i.get("item", "")) is None or not _int(i.get("qty"), 1):
            out.append(f"{here}: reward item {i!r} must be {{item: an existing item, qty >= 1}}")
    rare = r.get("rare")
    if rare is not None:
        if (not isinstance(rare, dict) or not _number(rare.get("chance")) or not (0 < rare["chance"] <= 1)
                or catalog.stack_item(rare.get("item", "")) is None or not _int(rare.get("qty"), 1)):
            out.append(f"{here}: rewards.rare must be {{chance in (0,1], item: an existing item, qty >= 1}}")
    if not out and st[1] == 0 and not items and rare is None:
        out.append(f"{here}: a cơ duyên that pays nothing")
    return out


# ------------------------------------------------------------------ the small state
def _iso(t: dt.datetime) -> str:
    return t.isoformat()


def _when(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s)


def _state(user: User, now: dt.datetime) -> dict:
    """A copy of this player's state, rolled over to today (the offers of yesterday are forgotten;
    the counter and the open offer are not)."""
    st = copy.deepcopy((user.flags or {}).get(FLAG) or {})
    today = clock.local_date(now)
    if st.get("date") != today:
        st["date"], st["offers"] = today, 0
    st.setdefault("offers", 0)
    st.setdefault("count", 0)
    st.setdefault("open", None)
    st.setdefault("log", [])
    return st


def _save(user: User, st: dict) -> None:
    user.flags = {**(user.flags or {}), FLAG: st}


def _log(st: dict, ev: dict, outcome: str, now: dt.datetime, rewards: dict | None = None) -> None:
    row = {"at": _iso(now), "event": ev["id"], "name_vi": ev["name_vi"], "kind": ev["kind"], "outcome": outcome}
    if rewards:
        row["rewards"] = rewards
    st["log"] = (list(st["log"]) + [row])[-trigger()["log_size"]:]


def _lapse(st: dict, now: dt.datetime) -> bool:
    """An open offer that ran out of time ends here: unaccepted, it just went away; accepted,
    the player did not finish in time. Either way nothing is paid and nothing is lost."""
    op = st["open"]
    if op is None or now <= _when(op["expires_at"]):
        return False
    ev = events().get(op["event"])
    if ev is not None:
        _log(st, ev, "timeout" if op["accepted"] else "expired", now)
    st["open"] = None
    return True


def _offer_view(st: dict, now: dt.datetime) -> dict | None:
    op = st["open"]
    if op is None:
        return None
    ev = events()[op["event"]]
    return {"id": ev["id"], "kind": ev["kind"], "name_vi": ev["name_vi"], "intro_vi": ev["intro_vi"],
            "accepted": op["accepted"], "expires_in": max(0, int((_when(op["expires_at"]) - now).total_seconds())),
            "progress": [op["step"], ev["question"]["count"]]}


def _log_view(st: dict) -> list[dict]:
    return [dict(r) for r in reversed(st["log"])]


# ------------------------------------------------------------------ offering
async def on_answer(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    """Listener of math_combat.record / math_practice.math_handler: count one right answer, and
    maybe open an offer. Returns {"fortune_offer": ...} for the response of that answer."""
    if not correct or s.context == CONTEXT or not events():
        return {}
    t = trigger()
    st = _state(user, now)
    changed = _lapse(st, now)
    if st["open"] is not None or st["offers"] >= t["daily_limit"]:
        if changed:
            _save(user, st)
        return {}
    st["count"] += 1
    offer = None
    if st["count"] >= t["right_answers"]:
        st["count"] = 0
        if _rng.random() < t["chance"]:
            table = list(events().values())
            ev = _rng.choices(table, weights=[e["weight"] for e in table])[0]
            st["offers"] += 1
            st["open"] = {"event": ev["id"], "expires_at": _iso(now + dt.timedelta(seconds=t["expires_seconds"])),
                          "accepted": False, "step": 0, "sid": None}
            offer = _offer_view(st, now)
    _save(user, st)
    return {"fortune_offer": offer} if offer else {}


math_combat.add_answer_listener(on_answer)


async def view(db: AsyncSession, user: User) -> dict:
    """GET /math/fortune."""
    now = clock.now()
    st = _state(user, now)
    if _lapse(st, now):
        _save(user, st)
    t = trigger()
    return {"offer": _offer_view(st, now), "today": {"offers": st["offers"], "limit": t["daily_limit"]},
            "progress": {"right": st["count"], "need": t["right_answers"]},
            "log": _log_view(st), "how_vi": data()["how_vi"]}


# ------------------------------------------------------------------ asking
async def _ask(db: AsyncSession, user: User, ev: dict, step: int) -> math_items.MathQuestion | None:
    """The next question of an event. An elder: the hardest one the player may get, of any of
    its types. A chest: one question of a stated type, at the player's own tier."""
    types = list(ev["question"]["qtypes"])
    if ev["kind"] == "elder":
        return await math_ask.pick_own(db, user, qtypes=types, highest=True, rng=_rng)
    _rng.shuffle(types)
    for qt in types:
        q = await math_ask.pick_own(db, user, qtypes=[qt], rng=_rng)
        if q is not None:
            return q
    return None


async def _open_question(db: AsyncSession, user: User, ev: dict, st: dict) -> dict | None:
    q = await _ask(db, user, ev, st["open"]["step"])
    if q is None:
        return None
    out = await quiz.create_session(db, user, CONTEXT, q, ref=ev["id"])
    st["open"]["sid"] = out["session_id"]
    out["fortune"] = {"event": ev["id"], "kind": ev["kind"], "name_vi": ev["name_vi"],
                      "progress": [st["open"]["step"], ev["question"]["count"]]}
    return out


def _ended(message_vi: str, st: dict, now: dt.datetime) -> dict:
    """accept() when there is nothing to ask any more: a normal answer (no error, so the state
    change is kept) saying the event is over."""
    return {"question": None, "ended": True, "message_vi": message_vi, "fortune": _offer_view(st, now)}


async def accept(db: AsyncSession, user: User) -> dict:
    """POST /math/fortune/accept: the first question of the open offer, or - when it was
    accepted already - the question still waiting."""
    now = clock.now()
    st = _state(user, now)
    if _lapse(st, now):
        _save(user, st)
        return _ended("Cơ duyên này đã tan mất rồi.", st, now)
    op = st["open"]
    if op is None:
        raise FortuneError(404, "no_offer", "Chưa có cơ duyên nào đang chờ con.")
    ev = events()[op["event"]]
    if op["accepted"]:
        s = await db.get(QuizSession, op["sid"]) if op["sid"] else None
        if s is not None and s.answered_at is None and now <= s.expires_at:
            return {"question": quiz.public_session(s), "fortune": _offer_view(st, now)}
        _log(st, ev, "lost", now)           # the question lapsed unanswered
        st["open"] = None
        _save(user, st)
        return _ended("Câu hỏi của cơ duyên đã hết giờ, cơ duyên tan mất.", st, now)
    op["accepted"], op["step"] = True, 0
    op["expires_at"] = _iso(now + dt.timedelta(seconds=trigger()["play_seconds"]))
    question = await _open_question(db, user, ev, st)
    if question is None:                    # the game has no question for them: give the offer back
        st["open"], st["offers"] = None, max(0, st["offers"] - 1)
        _save(user, st)
        return _ended("Chưa có câu đố nào hợp với con lúc này. Cơ duyên chưa mất.", st, now)
    _save(user, st)
    return {"question": question, "fortune": _offer_view(st, now)}


async def decline(db: AsyncSession, user: User) -> dict:
    """POST /math/fortune/decline: the offer is gone, nothing lost."""
    now = clock.now()
    st = _state(user, now)
    _lapse(st, now)
    op = st["open"]
    if op is None:
        _save(user, st)
        return await view(db, user)
    if op["accepted"]:
        raise FortuneError(409, "accepted", "Cơ duyên này đã nhận rồi, hãy trả lời câu đố.")
    _log(st, events()[op["event"]], "declined", now)
    st["open"] = None
    _save(user, st)
    return await view(db, user)


# ------------------------------------------------------------------ the answer
async def grant(db: AsyncSession, user: User, ev: dict) -> dict:
    """Pay a won event: Linh Thạch in its range, the guaranteed items, and the rare one by
    chance. Returns what was really granted."""
    r = ev["rewards"]
    stones = _rng.randint(*r["stones"])
    if stones:
        await inventory.change_currency(db, user.id, "spirit_stones", stones, "math_fortune", ev["id"])
    got = []
    for i in r["items"]:
        got.append({"item": i["item"], "qty": int(i["qty"]), "rare": False})
    rare = r.get("rare")
    if rare and _rng.random() < rare["chance"]:
        got.append({"item": rare["item"], "qty": int(rare["qty"]), "rare": True})
    for g in got:
        await inventory.change_item(db, user.id, g["item"], g["qty"], "math_fortune", ev["id"])
        g["name_vi"] = (catalog.stack_item(g["item"]) or {}).get("name_vi", g["item"])
    if stones:
        await db.flush()
        await db.refresh(user, ["spirit_stones"])
    return {"spirit_stones": stones, "items": got}


def _block(ev: dict, step: int, *, done: bool, won: bool = False, rewards: dict | None = None,
           question: dict | None = None, stale: bool = False) -> dict:
    out = {"event": ev["id"], "kind": ev["kind"], "name_vi": ev["name_vi"], "progress": [step, ev["question"]["count"]],
           "done": done, "won": won, "rewards": rewards, "next": question, "stale": stale}
    if done:
        out["text_vi"] = ev["win_vi"] if won else ev["lose_vi"]
    return out


async def fortune_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    """Grading a cơ duyên question: the learning log first (the answer counts for the learning
    path like any other), then the event moves on or ends."""
    out: dict = {"math": await math_combat.record(db, user, s, correct, now)}
    st = _state(user, now)
    op = st["open"]
    ev = events().get(s.ref or "")
    if ev is None or op is None or op["sid"] != s.id or op["event"] != ev["id"]:
        out["fortune"] = {"stale": True, "done": True, "won": False}      # an old question: nothing happens
        return out
    ok = correct and now <= _when(op["expires_at"])       # the whole event has a time limit too
    if not ok:
        _log(st, ev, "lost", now)
        st["open"] = None
        _save(user, st)
        out["fortune"] = _block(ev, op["step"], done=True)
        return out
    op["step"] += 1
    if op["step"] >= ev["question"]["count"]:
        rewards = await grant(db, user, ev)
        _log(st, ev, "won", now, rewards)
        st["open"] = None
        _save(user, st)
        out["fortune"] = _block(ev, op["step"], done=True, won=True, rewards=rewards)
        return out
    nxt = await _open_question(db, user, ev, st)
    if nxt is None:                         # cannot go on: end it without a penalty
        _log(st, ev, "lost", now)
        st["open"] = None
        _save(user, st)
        out["fortune"] = _block(ev, op["step"], done=True)
        return out
    _save(user, st)
    out["fortune"] = _block(ev, op["step"], done=False, question=nxt)
    return out


quiz.register_handler(CONTEXT, fortune_handler)
quiz.register_xp_rule(CONTEXT, math_ask.xp_rule)
