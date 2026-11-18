"""Chiêu thức gắn câu hỏi (M9, kế hoạch 4.4): a chiêu is cast by answering one math question.

The chiêu live in data/math/skills.json. Pressing one (`{"t": "mskill"}` on the WebSocket)
does not hit anything yet: it asks the caster one question of the chiêu's type, through the
same quiz service and the same `p.question` slot as Vấn Đạo, so while it is open the caster
has Hộ Thể and cannot open a second one. The qi and the cooldown are spent when the cast is
accepted - before the answer - because the question *is* the chiêu being channelled.

  * Right -> the chiêu lands: damage to the target, damage + slow to everything around it,
    or a ward on the caster's group. A landed chiêu breaks the target's Mặc Thuẫn like any
    right answer (and a bí cảnh boss's group shield counts it as this player's answer, no
    more). Right casts in a row build a combo; a fast answer is a crit like Ngộ Đạo.
  * Wrong or out of time -> "chiêu hụt": nothing happens, the combo is back to 0, and -
    unlike a missed Vấn Đạo - there is no Mặc Kích. Missing a chiêu you chose to cast costs
    the qi and the cooldown, never health. The fight then goes on as before: the monster,
    still shielded, asks its own question a few seconds later.

Which question: a type of the chiêu's `qtypes`, about the target's own micro-skill when the
target is a quái lỗi sai (else another micro-skill of its floor), otherwise about the
player's open floor. The tier is the player's own for that micro-skill (math_combat.tier_for)
and never above it. The answer goes to `math_answers` with no run, like M7, so the learning
path counts it.

Unlocking reads only the learning path (the player's open floor), never the cultivation
realm: the realm list is not decided yet.
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import random
from functools import lru_cache
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance
from .. import db as dbm
from ..config import DATA_DIR
from ..learning import math_items, math_mastery, math_path, quiz
from ..models import MathAnswer, QuizSession, User
from . import math_combat, math_practice

if TYPE_CHECKING:
    from ..realtime.zone import ChannelZone, Player

log = logging.getLogger("khu_vuon.math_skills")

CONTEXT = "math_skill"
SKILLS_FILE = DATA_DIR / "math" / "skills.json"

KINDS = ("Đòn thường", "Kiếm quyết", "Pháp thuật", "Trận pháp", "Tuyệt kỹ")
ELEMENTS = ("kim", "moc", "thuy", "hoa", "tho", "loi")
# the extra numbers each effect needs, each with its range lo < value <= hi
EFFECT_KEYS = {
    "damage": {},
    "area": {"radius": (0, 1000), "slow": (0, 0.95), "duration": (0, 120)},
    "ward": {"radius": (0, 1000), "duration": (0, 120), "reduce": (0, 0.95), "heal_pct": (0, 100)},
}
_REQUIRED = ("name_vi", "kind_vi", "element", "qtypes", "min_tier", "qi", "cooldown", "range", "effect",
             "power", "anim", "fx", "icon", "unlock", "desc_vi")
_OPTIONAL = {"reviewed", "radius", "slow", "duration", "reduce", "heal_pct", "icon_variant"}

REFUSALS_VI = {
    "unknown": "Không có chiêu này.",
    "cannot": "Lúc này không thi triển chiêu được.",
    "answering": "Con đang trả lời một câu khác.",
    "cooldown": "Chiêu này chưa hồi xong.",
    "no_qi": "Không đủ linh khí.",
    "no_target": "Hãy chọn một con quái làm mục tiêu.",
    "too_far": "Mục tiêu ở quá xa.",
    "tier_low": "Bậc câu hỏi con đã mở chưa đủ cho chiêu này. Luyện thêm ở Động Phủ nhé!",
    "no_question": "Chưa có câu hỏi loại này ở tầng của con.",
}


# ------------------------------------------------------------------ the data
def _read() -> dict:
    return json.loads(SKILLS_FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    """skills.json without its comment. It is checked by validate() in the tests and in
    tools/check_all.py, so the game itself trusts it."""
    return {k: v for k, v in _read().items() if not k.startswith("_")}


def skills() -> dict[str, dict]:
    return data()["skills"]


def combo_cfg() -> dict:
    return data()["combo"]


def _number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(raw: dict | None = None, config: dict | None = None) -> list[str]:
    """One readable line per problem in skills.json; empty when it is sound."""
    raw = _read() if raw is None else raw
    qtypes = math_path.question_types(config)
    out: list[str] = []
    combo = raw.get("combo")
    if not isinstance(combo, dict) or not _number(combo.get("per_streak")) or not _number(combo.get("max_mult")):
        out.append("combo must be {per_streak: number, max_mult: number}")
    elif combo["per_streak"] < 0 or combo["max_mult"] < 1:
        out.append("combo: per_streak must be >= 0 and max_mult >= 1")
    table = raw.get("skills")
    if not isinstance(table, dict) or not table:
        return out + ["skills must be a non-empty object"]
    for sid, s in table.items():
        here = f"skill {sid}"
        if not isinstance(s, dict):
            out.append(f"{here}: must be an object")
            continue
        missing = [k for k in _REQUIRED if k not in s]
        if missing:
            out.append(f"{here}: missing {', '.join(missing)}")
            continue
        extra = sorted(set(s) - set(_REQUIRED) - _OPTIONAL)
        if extra:
            out.append(f"{here}: unknown keys {', '.join(extra)}")
        variant = s.get("icon_variant", 0)
        if not isinstance(variant, int) or isinstance(variant, bool) or variant < 0:
            out.append(f"{here}: icon_variant must be a whole number >= 0")
        for key in ("name_vi", "desc_vi", "anim", "fx", "icon"):
            if not isinstance(s[key], str) or not s[key].strip():
                out.append(f"{here}: {key} must be a non-empty string")
        if s["kind_vi"] not in KINDS:
            out.append(f"{here}: kind_vi must be one of {', '.join(KINDS)}")
        if s["element"] not in ELEMENTS:
            out.append(f"{here}: element must be one of {', '.join(ELEMENTS)}")
        tier = s["min_tier"]
        if not isinstance(tier, int) or isinstance(tier, bool) or tier not in math_path.TIERS:
            out.append(f"{here}: min_tier must be a tier 1..{math_path.TOP_TIER}")
            tier = None
        if not isinstance(s["qtypes"], list) or not s["qtypes"]:
            out.append(f"{here}: qtypes must be a non-empty list")
        else:
            for q in s["qtypes"]:
                if q not in qtypes:
                    out.append(f"{here}: {q!r} is not a question type of balance/math.json")
                elif tier is not None and all(lim is None for lim in qtypes[q]["time_limit"][tier - 1:]):
                    out.append(f"{here}: a {q} question exists at no tier from {tier} up")
        for key in ("qi", "cooldown", "range", "power"):
            if not _number(s[key]) or s[key] < 0:
                out.append(f"{here}: {key} must be a number >= 0")
        if _number(s["cooldown"]) and s["cooldown"] <= 0:
            out.append(f"{here}: cooldown must be > 0")
        effect = s["effect"]
        if effect not in EFFECT_KEYS:
            out.append(f"{here}: effect must be one of {', '.join(EFFECT_KEYS)}")
        else:
            if effect != "ward":
                for key in ("power", "range"):
                    if _number(s[key]) and s[key] <= 0:
                        out.append(f"{here}: a {effect} chiêu needs {key} > 0")
            for key, (lo, hi) in EFFECT_KEYS[effect].items():
                v = s.get(key)
                if not _number(v) or not (lo < v <= hi):
                    out.append(f"{here}: a {effect} chiêu needs {key} > {lo} and <= {hi}")
            stray = sorted(k for k in ("radius", "slow", "duration", "reduce", "heal_pct")
                           if k in s and k not in EFFECT_KEYS[effect])
            if stray:
                out.append(f"{here}: {', '.join(stray)} mean nothing for a {effect} chiêu")
        unlock = s["unlock"]
        if (not isinstance(unlock, dict) or set(unlock) != {"floor"} or not isinstance(unlock["floor"], int)
                or isinstance(unlock["floor"], bool) or unlock["floor"] < 1):
            out.append(f"{here}: unlock must be {{\"floor\": n}} with n >= 1")
        if s.get("reviewed", False) not in (True, False):
            out.append(f"{here}: reviewed must be true or false")
    return out


def castable_floors(sk: dict, allow_unreviewed: bool = True) -> list[tuple[str, int]]:
    """(subject, floor) pairs at or above the chiêu's unlock floor where some template of one
    of its question types can really be asked at a tier the chiêu accepts. Empty means the
    chiêu cannot be cast by anyone today (tools/check_all.py reads this)."""
    out = []
    qtypes = set(sk["qtypes"]) & set(math_items.PLAYABLE_TYPES)
    for subject in math_path.subjects():
        for floor in subject.main_floors:
            if floor.number < sk["unlock"]["floor"]:
                continue
            templates = math_items.floor_templates(subject.id, floor.number, allow_unreviewed)
            if any(t.qtype in qtypes and t.tier >= sk["min_tier"] for t in templates):
                out.append((subject.id, floor.number))
    return out


# ------------------------------------------------------------------ unlocking
async def open_floor(db: AsyncSession, user_id: int) -> int:
    """The floor the player is working on: the lowest main floor not cleared yet (the last
    one when every floor is cleared), the best of all subjects."""
    best = 1
    for subject in math_path.subjects():
        if not subject.main_floors:
            continue
        cleared = await math_practice.cleared_floors(db, user_id, subject.id)
        n = math_mastery.next_floor(subject, cleared)
        best = max(best, n if n is not None else subject.main_floors[-1].number)
    return best


def locked_reason(sk: dict, floor: int) -> str | None:
    need = sk["unlock"]["floor"]
    if floor >= need:
        return None
    return f"Mở khi lộ trình học tới tầng {need} (con đang ở tầng {floor})."


async def view(db: AsyncSession, user: User) -> dict:
    """GET /math/skills: every chiêu in data order, and whether this player has it."""
    floor = await open_floor(db, user.id)
    types = math_path.question_types()
    out = []
    for sid, s in skills().items():
        reason = locked_reason(s, floor)
        row = {"id": sid, **{k: s[k] for k in ("name_vi", "kind_vi", "element", "min_tier", "qi", "cooldown",
                                                 "range", "effect", "power", "anim", "fx", "icon",
                                                 "desc_vi")},
               "icon_variant": int(s.get("icon_variant", 0)),
               "qtypes": list(s["qtypes"]),
               "qtype_vi": ", ".join(types[q]["name_vi"] for q in s["qtypes"]),
               "unlock": {"floor": s["unlock"]["floor"]}, "unlocked": reason is None, "locked_vi": reason}
        row.update({k: s[k] for k in EFFECT_KEYS[s["effect"]]})
        out.append(row)
    return {"combo": dict(combo_cfg()), "open_floor": floor, "skills": out}


# ------------------------------------------------------------------ the formula
def combo_mult(streak_before: int, combo: dict | None = None) -> float:
    """x1 for the first right cast, +per_streak for each right cast before it, capped."""
    c = combo or combo_cfg()
    return min(float(c["max_mult"]), 1.0 + float(c["per_streak"]) * max(0, streak_before))


def is_fast(answer_ms: int | None, limit: float) -> bool:
    """The same rule as Ngộ Đạo: answered within fast_answer_fraction of the time limit."""
    c = balance.load("combat")
    return answer_ms is not None and answer_ms <= c["fast_answer_fraction"] * limit * 1000


def damage(base: float, sk: dict, streak_before: int, fast: bool) -> float:
    """base_damage x power x combo x fast-answer crit (skills.json _comment)."""
    crit = float(balance.load("combat")["fast_answer_crit_mult"]) if fast else 1.0
    return base * float(sk["power"]) * combo_mult(streak_before) * crit


# ------------------------------------------------------------------ which question
async def _recent_fingerprints(db: AsyncSession, user_id: int, config: dict) -> dict[str, int]:
    rows = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user_id)
                             .order_by(MathAnswer.id.desc())
                             .limit(config["anti_repeat_window"]))).scalars().all()
    return {f: n for n, f in enumerate(reversed(list(rows)))}


async def _groups(db: AsyncSession, user_id: int, info: dict | None,
                  rng: random.Random) -> list[tuple[str, int, list[str]]]:
    """(subject, floor, micro-skills) to try in order of preference."""
    if math_combat.is_mistake_monster(info):
        subject, floor = info["subject"], int(info["floor"])
        others = [k.id for k in math_path.subject(subject).floor(floor).skills if k.id != info["skill"]]
        rng.shuffle(others)
        return [(subject, floor, [info["skill"]]), (subject, floor, others)]
    for subject in math_path.subjects():   # the first subject that has questions at all
        numbers = [f.number for f in subject.main_floors if math_practice._templates(subject.id, f.number)]
        if not numbers:
            continue
        cleared = await math_practice.cleared_floors(db, user_id, subject.id)
        here = math_mastery.next_floor(subject, cleared) or subject.main_floors[-1].number
        out = []
        for n in sorted((n for n in numbers if n <= here), reverse=True):   # the open floor, then below
            ids = [k.id for k in subject.floor(n).skills]
            rng.shuffle(ids)
            out.append((subject.id, n, ids))
        return out
    return []


async def question_for(db: AsyncSession, user: User, sk: dict, info: dict | None,
                       rng: random.Random | None = None) -> tuple[math_items.MathQuestion | None, str | None]:
    """The question that casts this chiêu, or (None, refusal code). The type is one of the
    chiêu's qtypes; the tier is the player's own for the micro-skill, else the nearest lower
    tier with a template, never below min_tier ("tier_low" when only that is missing)."""
    rng = rng or random.Random()
    config = math_path.cfg()
    qtypes = set(sk["qtypes"]) & set(math_items.PLAYABLE_TYPES)
    min_tier = int(sk["min_tier"])
    too_low = False
    seen_at = None
    for subject_id, floor, skill_ids in await _groups(db, user.id, info, rng):
        templates = [t for t in math_practice._templates(subject_id, floor) if t.qtype in qtypes]
        for skill_id in skill_ids:
            mine = [t for t in templates if t.skill == skill_id]
            if not mine:
                continue
            tier = await math_combat.tier_for(db, user.id, skill_id, floor, config)
            usable = sorted({t.tier for t in mine if min_tier <= t.tier <= tier})
            if not usable:
                too_low = True
                continue
            if seen_at is None:
                seen_at = await _recent_fingerprints(db, user.id, config)
            item = math_practice._pick([t for t in mine if t.tier == usable[-1]], seen_at, rng)
            if item is None:
                continue
            question = math_items.to_question(item, rng, config)
            question.meta["doc"] = math_practice.doc_link(item.skill)
            if math_combat.is_mistake_monster(info):
                question.meta["mistake_vi"] = info.get("mistake_vi", "")
                question.meta["monster_vi"] = info.get("name_vi", "")
            question.meta["cast_vi"] = sk["name_vi"]
            return question, None
    return None, ("tier_low" if too_low else "no_question")


# ------------------------------------------------------------------ casting (in memory + one task)
def _world():
    from ..realtime.world import world
    return world


def _target_code(p: "Player", sk: dict, eid: str | None):
    """(monster or None, refusal code or None) for this chiêu's target."""
    if sk["effect"] == "ward":
        return None, None
    m = p.channel.monster(eid) if eid else None
    if m is None or not m.alive:
        return None, "no_target"
    from ..realtime import combat
    if combat.dist(p.x, p.y, m.x, m.y) > sk["range"]:
        return None, "too_far"
    return m, None


def _ready_code(p: "Player", k: str, eid: str | None, now: float) -> str | None:
    """Everything that can be checked in memory, in the order the player should hear it."""
    sk = skills()[k]
    if now < p.mskill_ready.get(k, 0.0):
        return "cooldown"
    if p.qi < sk["qi"]:
        return "no_qi"
    return _target_code(p, sk, eid)[1]


def refuse(p: "Player", k: str, code: str, message_vi: str | None = None) -> None:
    if p.session is not None:
        p.session.send({"t": "mcast", "k": k, "ok": False, "code": code,
                        "message_vi": message_vi or REFUSALS_VI.get(code, REFUSALS_VI["cannot"])})


def request(p: "Player", k: str, eid: str | None, now: float) -> str | None:
    """The `mskill` message. Returns a refusal code at once, or None when the question is
    being written in the background (which may still refuse: locked, cooldown, no_qi, ...
    tier_low, no_question). Nothing is spent until the question exists."""
    if k not in skills():
        return "unknown"
    if p.channel is None or p.dead or p.ghost or p.session is None:
        return "cannot"
    if p.question is not None or p.q_pending or p.protected(now):
        return "answering"
    p.q_pending = True
    _world().spawn(_create(p, p.channel, k, eid))
    return None


async def _create(p: "Player", ch: "ChannelZone", k: str, eid: str | None) -> None:
    from ..realtime import combat
    w = _world()
    sk = skills()[k]
    rng = random.Random()
    try:
        async with dbm.SessionLocal() as db:
            user = await db.get(User, p.user_id)
            reason = locked_reason(sk, await open_floor(db, p.user_id))
            if reason is not None:
                p.q_pending = False
                refuse(p, k, "locked", reason)
                return
            code = _ready_code(p, k, eid, w.mono()) if p.channel is ch else "cannot"
            if code is not None:
                p.q_pending = False
                refuse(p, k, code)
                return
            m0 = ch.monster(eid) if (eid and sk["effect"] != "ward") else None
            # M10: in a bí cảnh toán every question is at the answering player's own floor,
            # whoever is hit (plan 4.3) - so the target's own floor and micro-skill are not used
            own_floor = getattr(ch, "question_source", None) is not None
            info = m0.info if (m0 is not None and not own_floor) else None
            question, code = await question_for(db, user, sk, info, rng)
            if question is None:
                p.q_pending = False
                refuse(p, k, code)
                return
            mid = m0.eid if m0 is not None else None
            out = await quiz.create_session(db, user, CONTEXT, question, ref=f"{ch.key}|{mid or ''}|{k}")
            await db.commit()
    except Exception:
        log.exception("could not create a cast question")
        p.q_pending = False
        refuse(p, k, "cannot")
        return
    p.q_pending = False
    now = w.mono()
    # the world went on while the question was written: check everything again
    code = None
    if p.dead or p.ghost or p.channel is not ch or p.session is None or w.players.get(p.user_id) is not p:
        code = "cannot"
    elif p.question is not None:
        code = "answering"
    else:
        code = _ready_code(p, k, mid, now)
    if code is not None:
        refuse(p, k, code)
        return   # the question is never shown; it simply expires
    m = ch.monster(mid) if mid else None
    p.qi -= sk["qi"]
    p.mskill_ready[k] = now + float(sk["cooldown"])
    limit = float(question.time_limit)
    deadline = now + limit + balance.quiz()["network_grace"]
    p.question = {"sid": out["session_id"], "mid": mid, "deadline": deadline, "asked": now, "limit": limit,
                  "timeout_sent": False, "cast": k, "ch": ch.key}
    p.protect_until = deadline
    p.inputs.clear()
    p.queued_ms = 0
    if m is not None:
        dx, dy = m.x - p.x, m.y - p.y
        p.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")
        combat.engage(ch, m, p, now)
    p.session.send({"t": "mcast", "k": k, "ok": True, "ready_in": float(sk["cooldown"]),
                    "qi": round(p.qi, 1)})
    p.session.send({"t": "q", "mid": mid, "q": out, "first_meet": False,
                    "cast": {"k": k, "name_vi": sk["name_vi"]}})
    ch.event(k="mcast", by=p.eid, s=k, anim=sk["anim"], x=p.x, y=p.y)


# ------------------------------------------------------------------ the answer
def _block(k: str, **kw) -> dict:
    out = {"cast": k, "correct": False, "missed": False, "timed_out": False, "damage": 0, "crit": False,
           "combo": 0, "combo_mult": 1.0, "shield_broken": False, "monster_hp": 0, "killed": False}
    out.update(kw)
    return out


def resolve(p: "Player", sid: str, correct: bool, answer_ms: int | None, timed_out: bool) -> dict:
    """The cast question was graded (in memory): the chiêu lands or misses."""
    from ..realtime import combat
    q = p.question
    if q is None or q["sid"] != sid or not q.get("cast"):
        return {"stale": True}
    k = q["cast"]
    ch = p.channel
    p.question = None
    p.protect_until = 0.0
    if ch is None or ch.key != q["ch"] or p.dead or k not in skills():
        return {"cast": k, "stale": True}
    sk = skills()[k]
    now = _world().mono()
    m = ch.monster(q["mid"]) if q["mid"] else None
    ev = {"k": "mskill", "by": p.eid, "s": k, "fx": sk["fx"], "anim": sk["anim"], "x": p.x, "y": p.y}
    if sk["effect"] != "ward":
        if m is None or not m.alive:   # the target went away while the question was open
            return {"cast": k, "stale": True, "gone": True, "correct": correct}
        ev.update(tx=m.x, ty=m.y)
    if sk["effect"] in ("area", "ward"):
        ev["r"] = sk["radius"]
    if not correct:   # chiêu hụt: no damage, the combo is gone, and no Mặc Kích
        p.mcombo = 0
        ch.event(**ev, ok=0, combo=0)
        if m is not None and m.alive and m.shield and p.user_id in m.engaged:
            p.next_q = (m.eid, now + combat.cfg()["next_question_delay"])   # the fight goes on
        return _block(k, missed=True, timed_out=bool(timed_out),
                      monster_hp=max(0, m.hp_pct()) if m is not None else 0)
    streak = p.mcombo
    mult = combo_mult(streak)
    p.mcombo = streak + 1
    fast = is_fast(answer_ms, q["limit"])
    ev.update(ok=1, combo=p.mcombo)
    if sk["effect"] == "ward":
        healed = _ward(ch, p, sk, now)
        ch.event(**ev)
        return _block(k, correct=True, crit=fast, combo=p.mcombo, combo_mult=mult, ward=healed)
    if m.shield and m.info.get("group_shield"):
        progress = combat.group_hit(ch, m, p)
        if progress is not None:   # the others still have to answer: the boss's shield holds
            ch.event(**ev)
            return _block(k, correct=True, crit=fast, combo=p.mcombo, combo_mult=mult,
                          shield_progress=list(progress), monster_hp=max(0, m.hp_pct()))
    broke = m.shield
    if broke:
        combat.break_shield(ch, m, p, now)
    if sk["effect"] == "area":
        m.slow_until, m.slow_mult = now + sk["duration"], sk["slow"]
    dealt = combat.hurt_monster(ch, m, p, damage(combat.base_damage(p, m), sk, streak, fast), fast, now)
    if sk["effect"] == "area":
        cx, cy = ev["tx"], ev["ty"]
        for o in list(ch.monsters):
            if o is m or not o.alive or combat.dist(cx, cy, o.x, o.y) > sk["radius"]:
                continue
            o.slow_until, o.slow_mult = now + sk["duration"], sk["slow"]
            combat.engage(ch, o, p, now)
            combat.hurt_monster(ch, o, p, damage(combat.base_damage(p, o), sk, streak, fast), fast, now)
    ch.event(**ev)
    return _block(k, correct=True, damage=int(round(dealt)), crit=fast, combo=p.mcombo, combo_mult=mult,
                  shield_broken=broke, monster_hp=max(0, m.hp_pct()), killed=not m.alive)


def _ward(ch: "ChannelZone", p: "Player", sk: dict, now: float) -> dict:
    """Hộ Thân Trận: the caster and the party members standing near take less damage for a
    while (the stronger ward wins when two overlap) and are healed a little."""
    from ..realtime import combat
    near = [p] + [o for uid in _world().parties.mates(p.user_id)
                  if (o := ch.players.get(uid)) is not None and not o.dead
                  and combat.dist(p.x, p.y, o.x, o.y) <= sk["radius"]]
    healed = 0
    for o in near:
        reduce = float(sk["reduce"])
        if now < o.guard_until:
            reduce = max(reduce, o.guard_reduce)
        o.guard_until = max(o.guard_until, now + float(sk["duration"]))
        o.guard_reduce = reduce
        amount = min(o.max_hp - o.hp, o.max_hp * float(sk["heal_pct"]) / 100)
        if amount > 0:
            o.hp += amount
            healed += amount
            ch.event(k="heal", id=o.eid, v=int(round(amount)), x=o.x, y=o.y)
    return {"players": len(near), "heal": int(round(healed)), "duration": sk["duration"], "reduce": sk["reduce"]}


async def math_skill_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool,
                             now: dt.datetime) -> dict:
    """Grading a cast question (answered or timed out): the learning log first, then the fight."""
    out: dict = {"math": await math_combat.record(db, user, s, correct, now)}
    p = _world().players.get(user.id)
    if p is not None:
        out["combat"] = resolve(p, s.id, correct, s.answer_ms, out["math"]["timed_out"])
        out["combat"].setdefault("cast", (s.ref or "").rsplit("|", 1)[-1])   # ref = "<channel>|<mid>|<chiêu>"
    return out


quiz.register_handler(CONTEXT, math_skill_handler)
quiz.register_xp_rule(CONTEXT, math_combat.xp_rule)
