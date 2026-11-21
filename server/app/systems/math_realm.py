"""Bí cảnh toán (M10, kế hoạch 4.3): "nhiều người cùng vào, mỗi người nhận câu theo tầng của
mình; boss cuối là câu 'Tìm chỗ sai' hoặc bài tổng hợp."

The run itself is the bí cảnh of stage 9 (app/realtime/realm.py: matchmaking, instances,
rooms, ghosts, the boss's group shield, loot). Every realm of data/realms.json is a math
bí cảnh (its `kind` only says how it is entered), and this module is what it asks:

  * every question - a Mặc Quái's, a Trận Nhãn seal's, the boss's - comes from
    math_ask.pick_own, i.e. the answering player's own floor and their own tier for the
    micro-skill, never the monster's floor nor the room's. Two players on different floors
    fighting one monster get questions of two different floors;
  * the boss asks each player their "bài tổng hợp": pick_own(highest=True), the hardest
    question that player may be asked. The data names the type the boss would rather ask
    ("find_mistake", Tìm chỗ sai, playable since M11); a player who has no question of that
    type at their tier gets the bài tổng hợp instead - never a faked Tìm chỗ sai;
  * nobody here is asked a Thiên kiếp (tribulation, M11 đợt 2): one takes 8-12 minutes and a
    math bí cảnh lasts 15-20 minutes with a group waiting on every shield, so every asker -
    the boss's bài tổng hợp included - draws from QUICK_TYPES;
  * the answer is written to math_answers with no run (math_ask.record) before the fight
    or the seal hears about it, so it counts for the learning path; running out of time is
    graded as a wrong answer by the quiz service and costs nothing else.
"""
from __future__ import annotations

import datetime as dt
import random
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance
from .. import db as dbm
from ..learning import math_items, math_path, quiz
from ..models import QuizSession, User
from . import math_ask

if TYPE_CHECKING:
    from ..realtime.realm import RealmInstance
    from ..realtime.zone import Player

CONTEXT = "math_realm"
ASKERS = ("monster", "seal", "boss")
QUICK_TYPES = tuple(t for t in math_items.PLAYABLE_TYPES if t != "tribulation")    # what a bí cảnh asks
REALM_EXTRA_LOOT = ("linh_qua",)    # besides the M7 materials: Linh Quả, whose only source is a bí cảnh


# ------------------------------------------------------------------ which question
def rules(rdef: dict) -> dict:
    return rdef.get("math") or {}


def boss_type(rdef: dict) -> str | None:
    """The question type the boss asks, or None for the bài tổng hợp (any playable type).
    The preferred type only counts once the game can ask it."""
    prefer = rules(rdef).get("boss_question", {}).get("prefer")
    return prefer if prefer in QUICK_TYPES else None


async def question_for(db: AsyncSession, user: User, rdef: dict, asker: str, rng: random.Random | None = None,
                       who_vi: str = "") -> math_items.MathQuestion | None:
    """One question for this player in a math bí cảnh, at their own floor; None when the bank
    has none for them. `asker` is one of ASKERS."""
    rng = rng or random.Random()
    if asker == "boss":
        q = None
        prefer = boss_type(rdef)
        if prefer is not None:
            q = await math_ask.pick_own(db, user, qtypes=[prefer], highest=True, rng=rng)
        if q is None:
            q = await math_ask.pick_own(db, user, qtypes=QUICK_TYPES, highest=True, rng=rng)
    else:
        q = await math_ask.pick_own(db, user, qtypes=QUICK_TYPES, rng=rng)
    if q is not None:   # the card names who asks (math_practice.MathCombatQuizScene draws it)
        q.meta["monster_vi"] = who_vi or rdef.get("name_vi", "")
        q.meta["mistake_vi"] = rules(rdef).get("lines_vi", {}).get(asker, "")
        q.meta["realm_asker"] = asker
    return q


async def seal_session(inst: "RealmInstance", p: "Player", name: str) -> tuple[dict, float] | None:
    """Writes the question a seal asks this player: (the public quiz session, its time limit),
    or None when the bank has no question for them (they are told so)."""
    async with dbm.SessionLocal() as db:
        user = await db.get(User, p.user_id)
        q = await question_for(db, user, inst.rdef, "seal", random.Random(), who_vi="Trận Nhãn")
        if not inst.got_question(p, q):
            return None
        out = await quiz.create_session(db, user, CONTEXT, q, ref=f"{inst.key}|seal:{name}")
        await db.commit()
    return out, float(q.time_limit)


# ------------------------------------------------------------------ the answer
async def math_realm_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool,
                             now: dt.datetime) -> dict:
    """Grading a question asked in a math bí cảnh: the learning log first, then the seal or the
    fight that asked it (both in memory)."""
    from ..realtime import combat
    out: dict = {"math": await math_ask.record(db, user, s, correct, now)}
    p = combat._world().players.get(user.id)
    if p is None:
        return out
    q = p.question
    if q is not None and q["sid"] == s.id and q.get("seal"):
        ch = p.channel
        puzzle = getattr(ch, "puzzle", None)
        if ch is not None and ch.key == q.get("ch") and hasattr(puzzle, "answer"):
            out["realm"] = puzzle.answer(p, s.id, correct)
        else:   # the room is gone: the question just closes
            combat.end_question(p, "gone")
            out["realm"] = {"seal": q["seal"], "stale": True}
    else:
        out["combat"] = combat.on_answer(p, s.id, correct, s.answer_ms)
    return out


quiz.register_handler(CONTEXT, math_realm_handler)
quiz.register_xp_rule(CONTEXT, math_ask.xp_rule)


# ------------------------------------------------------------------ the data
def validate(realms_data: dict | None = None, realm_cfg: dict | None = None) -> list[str]:
    """One readable line per problem with the math bí cảnh in data/realms.json and
    balance/realm.json; empty when they are sound."""
    import json

    from ..config import DATA_DIR
    from ..realtime import maps
    from ..realtime.realm import MAP, PUZZLES
    from . import catalog
    raw = realms_data if realms_data is not None else json.loads((DATA_DIR / "realms.json").read_text("utf-8"))
    c = realm_cfg if realm_cfg is not None else balance.load("realm")
    drops = json.loads((DATA_DIR / "math" / "drops.json").read_text("utf-8"))
    materials = {k for k, v in drops.items() if not k.startswith("_") and v.get("kind") == "material"}
    qtypes = math_path.question_types()
    out: list[str] = []
    m = maps.load(MAP)
    puzzles = raw.get("puzzles", {})
    seal = c.get("seal")
    if not isinstance(seal, dict) or any(not isinstance(seal.get(k), (int, float)) or seal[k] < 0
                                         for k in ("base", "per_member", "fail_pct", "retry_seconds")):
        out.append("balance/realm.json: seal needs base, per_member, fail_pct, retry_seconds >= 0")
        seal = {"base": 1}
    for rid, r in raw.get("realms", {}).items():
        here = f"realm {rid}"
        if r.get("kind") not in ("math", "scheduled", "rift"):
            out.append(f"{here}: kind must be math, scheduled or rift")
        if r.get("kind") == "rift" and c.get("rift", {}).get("realm") != rid:
            out.append(f"{here}: a rift realm must be balance/realm.json rift.realm, or nothing opens it")
        if "min_realm" in r:
            out.append(f"{here}: a math bí cảnh must not depend on the cultivation realms (min_realm)")
        for key in ("name_vi", "desc_vi"):
            if not str(r.get(key, "")).strip():
                out.append(f"{here}: {key} missing")
        if not isinstance(r.get("party_min"), int) or not 1 <= r["party_min"] <= c["party_max"]:
            out.append(f"{here}: party_min must be 1..party_max")
        rooms = rules(r).get("rooms")
        if not isinstance(rooms, list) or not rooms:
            out.append(f"{here}: math.rooms must be a non-empty list")
            rooms = []
        for i, room in enumerate(rooms):
            kind, place = room.get("kind"), room.get("place", room.get("kind"))
            if kind not in PUZZLES:
                out.append(f"{here}: room {i}: unknown puzzle kind {kind!r}")
            if not puzzles.get(kind):
                out.append(f"{here}: room {i}: puzzles.{kind} (name and how-to) missing")
            if place not in m.rooms:
                out.append(f"{here}: room {i}: the bi_canh map has no room {place!r}")
                continue
            if kind == "seal":
                stones = [o for o in m.realm_objs if o.props.get("room") == place
                          and o.props.get("kind") == room.get("seal")]
                if len(stones) < seal.get("base", 1):
                    out.append(f"{here}: room {i}: {len(stones)} {room.get('seal')!r} in {place}, "
                               f"fewer than seal.base")
        bq = rules(r).get("boss_question", {})
        if bq.get("prefer") not in qtypes:
            out.append(f"{here}: boss_question.prefer must be a question type of balance/math.json")
        elif bq["prefer"] in math_items.PLAYABLE_TYPES and bq["prefer"] not in QUICK_TYPES:
            out.append(f"{here}: boss_question.prefer {bq['prefer']!r} takes too long for a bí cảnh "
                       f"(one of {', '.join(QUICK_TYPES)})")
        if bq.get("fallback") != "highest":
            out.append(f"{here}: boss_question.fallback must be 'highest' (the bài tổng hợp)")
        lines = rules(r).get("lines_vi", {})
        for asker in ASKERS:
            if not str(lines.get(asker, "")).strip():
                out.append(f"{here}: math.lines_vi.{asker} missing")
        mons = catalog.monsters()
        boss = mons.get(r.get("boss", ""))
        if boss is None or not boss.get("group_shield"):
            out.append(f"{here}: boss must be a monster with a group shield")
        if not puzzles.get("boss"):
            out.append(f"{here}: puzzles.boss missing")
        # rule 7: Linh Thạch, Tu Vi through the answers, the M7 materials and Linh Quả only; Mảnh
        # Bảo Vật are allowed again since 2026-11-20, gated by tu vi like all loot (loot.py)
        chest = c.get("chest", {}).get(rid)
        loot = c.get("room_loot_by_realm", {}).get(rid)
        if chest is None or loot is None:
            out.append(f"{here}: balance/realm.json needs chest.{rid} and room_loot_by_realm.{rid}")
            continue
        if chest.get("xp") or loot.get("xp") or any(chest.get("jade", [0, 0])):
            out.append(f"{here}: its loot pays no xp nor jade (Tu Vi comes from the answers)")
        for e in list(chest.get("table", [])) + list(loot.get("items", [])):
            if e.get("item") not in materials and e.get("item") not in REALM_EXTRA_LOOT:
                out.append(f"{here}: loot {e} is not a material of data/math/drops.json nor Linh Quả")
        table = {e.get("item") for e in chest.get("table", [])}
        for t in chest.get("treasures", []):
            if t not in table:
                out.append(f"{here}: chest treasure {t!r} is not in its table")
    # the creatures each realm fields, by theme and band (app/systems/realm_quai.py)
    from . import realm_quai
    out += realm_quai.validate(raw, c)
    return out
