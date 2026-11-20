"""Combat, all decided by the server. Two rules live here.

**The open world: questions only when a monster hits you** (the `combat` section of
data/math/world_plan.json, wired through `wired_sections`; every number is read from there).
The player attacks and casts chiêu freely. A monster's blow is telegraphed: a circle, cone or
line fills on the ground during the windup. Out of it in time (or inside the invulnerability
of a Né Đòn dash) - nothing happens. Caught by it - the fight pauses *for that player*: Hộ Thể
(no damage, no moving, no acting, no monster picks them as a target) while one math question
is written and answered, on the micro-skill that monster stands for, through the same
question pipeline as before (math_combat.question_for / math_ask.pick_own). Right = Phản Đòn:
no damage, the monster takes a counter hit (x counter_multiplier) and is stunned, the player
gains tu vi (the quiz service's xp rule) and linh lực. Wrong or out of time = the blow lands in
full and the card shows the solution. After either, a rest window: a blow landing then does
half damage and asks nothing. Normal monsters have no Mặc Thuẫn out here (plain hits kill
them); an elite's or a boss's shield breaks only on a Phản Đòn. Other players in the zone are
not paused: they keep fighting, the same monster included.

**Vấn Đạo (spec 8.1), still the rule of a bí cảnh** (an instance, realtime/realm.py): every
monster wears a Mặc Thuẫn. While it is up, hits do 1 damage and can never kill it.
Engaging a monster (hitting it, or an aggressive one coming at you) brings a question;
while answering you have Hộ Thể (no damage, no moving, no attacking). Right: the shield
breaks and a "Ngộ Đạo" strike lands (x2, more when fast). Wrong or too late: Mặc Kích, a
hit of 10/15/20% of your max HP (less with Kháng Mực), and the next question in 3 s.

The tick (sync, no database) moves monsters, lands telegraphed attacks, checks question
deadlines and regenerates. Everything needing the database (creating questions, grading
timeouts, rewards, death penalty) runs as background tasks and comes back into memory.
"""
from __future__ import annotations

import logging
import math
import random
from typing import TYPE_CHECKING

from .. import balance
from .. import db as dbm

if TYPE_CHECKING:
    from .ai import Monster
    from .world import World
    from .zone import ChannelZone, Player

log = logging.getLogger("toan_tu_tien.combat")
FACING_NAMES = ("down", "up", "left", "right")


def cfg() -> dict:
    return balance.load("combat")


def _world() -> "World":
    from .world import world
    return world


def dist(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(ax - bx, ay - by)


# ------------------------------------------------------------------ the open-world rule
HIT_SLACK = 5          # px: a blow reaches a little past its drawn edge (the feet are a box)
DASH_STEP_MS = 10      # a dash is applied in small steps so it never jumps through a wall

DODGE_REFUSALS_VI = {
    "cannot": "Lúc này không né được.",
    "answering": "Con đang trả lời câu hỏi.",
    "locked": "Né Đòn mở ở Luyện Khí tầng 1.",
    "cooldown": "Né Đòn chưa hồi xong.",
}


def plan() -> dict:
    """The `combat` section of world_plan.json: every number of the open-world rule."""
    from ..learning import math_tree
    return math_tree.world_plan()["combat"]


def on_hit_rule(ch) -> bool:
    """Is this channel fought by "questions only when a monster hits you"? Every wild zone once
    world_plan.json wires its combat section; a bí cảnh (an instance) keeps Vấn Đạo."""
    if ch is None or getattr(ch, "instance", False):
        return False
    from ..learning import math_tree
    return math_tree.section_wired("combat")


def shielded_rank(info: dict) -> bool:
    """Out in the wild only these ranks wear a Mặc Thuẫn (it breaks only on a Phản Đòn)."""
    return info.get("rank", "normal") in plan()["shielded_ranks"]


def windup() -> float:
    """How long a blow is telegraphed: never shorter than the plan's minimum."""
    return max(float(plan()["telegraph_min_seconds"]), float(cfg()["telegraph_seconds"]))


def next_shape(m: "Monster") -> str:
    """The shape of this monster's next blow: its own `attack_shape` if the data gives one (one
    shape, or a list: its own rhythm, in turn), else its rank's list in turn."""
    own = m.info.get("attack_shape")
    if isinstance(own, str) and own in plan()["telegraph_shapes"]:
        return own
    shapes = own if isinstance(own, list) and own else \
        plan()["telegraph"]["by_rank"].get(m.info.get("rank", "normal")) or ["circle"]
    shape = shapes[m.shape_i % len(shapes)]
    m.shape_i += 1
    return shape


def make_tele(m: "Monster", tx: float, ty: float, reach: float, land: float, shape: str = "circle") -> dict:
    """A telegraphed blow. circle: around the target point; cone and line: from the monster
    towards it (`a` = direction in radians, `r` = reach, `w` = width of a line)."""
    tele = {"shape": shape, "x": tx, "y": ty, "r": float(reach), "land": land, "a": 0.0, "w": 0.0, "half": 0.0}
    if shape == "circle":
        return tele
    t = plan()["telegraph"]
    a = math.atan2(ty - m.y, tx - m.x)
    tele.update(x=m.x, y=m.y, a=a)
    if shape == "cone":
        tele.update(r=reach * float(t["cone_reach_mult"]), half=math.radians(float(t["cone_degrees"]) / 2))
    else:
        tele.update(r=reach * float(t["line_reach_mult"]), w=float(t["line_width"]))
    return tele


def in_tele(tele: dict, x: float, y: float) -> bool:
    """Does this blow reach a player standing (feet) at (x, y)?"""
    dx, dy = x - tele["x"], y - tele["y"]
    d = math.hypot(dx, dy)
    if tele["shape"] == "circle":
        return d <= tele["r"] + HIT_SLACK
    if tele["shape"] == "cone":
        if d > tele["r"] + HIT_SLACK:
            return False
        if d <= HIT_SLACK * 2:
            return True
        off = abs((math.atan2(dy, dx) - tele["a"] + math.pi) % (2 * math.pi) - math.pi)
        return off <= tele["half"] + math.asin(min(1.0, HIT_SLACK / d))
    ca, sa = math.cos(tele["a"]), math.sin(tele["a"])
    along, across = dx * ca + dy * sa, -dx * sa + dy * ca
    return -HIT_SLACK <= along <= tele["r"] + HIT_SLACK and abs(across) <= tele["w"] / 2 + HIT_SLACK


def tele_event(m: "Monster", tele: dict, dur: float) -> dict:
    """The `tele` effect: x, y, r and d as ever (an old client draws a circle), plus the shape."""
    ev = {"k": "tele", "id": m.eid, "x": round(tele["x"], 1), "y": round(tele["y"], 1), "r": round(tele["r"], 1),
          "d": round(dur, 2), "sh": tele["shape"]}
    if tele["shape"] != "circle":
        ev["a"] = round(math.degrees(tele["a"]), 1)
    if tele["shape"] == "cone":
        ev["deg"] = round(math.degrees(tele["half"]) * 2, 1)
    if tele["shape"] == "line":
        ev["w"] = round(tele["w"], 1)
    return ev


def dodge_unlocked(p: "Player") -> bool:
    """Né Đòn opens at the realm and stage its world_plan unlock names (Luyện Khí tầng 1)."""
    from ..learning import math_tree
    from .world import realm_index
    uid = plan()["dodge"]["unlock"]
    u = next(x for x in math_tree.world_plan()["unlocks"] if x["id"] == uid)
    have, need = realm_index(p.realm), realm_index(u["realm"])
    return have > need or (have == need and p.stage >= int(u["stage"]))


def dodge_cooldown(p: "Player") -> float:
    """Né Đòn's cooldown; the worn Bạch Hạc (gift dodge_cooldown) shortens it."""
    from ..systems import beasts, linh_can   # and a light-footed linh căn (dodge_cd)
    return float(plan()["dodge"]["cooldown_seconds"]) * (1 - beasts.gift_value(getattr(p, "pet", None),
                                                                                  "dodge_cooldown"))         * (1 - linh_can.fx(p, "dodge_cd"))


def dodge(p: "Player", seq: int, dx: int, dy: int, now: float) -> str | None:
    """Né Đòn: a short dash with a moment of invulnerability. Returns a refusal code or None.

    The dash rides in the movement queue at its own sequence number, so the server moves the
    player exactly where the client predicted, after the steps sent before it. A refused dash
    still takes its place in the queue as an empty step, so the client's later steps line up."""
    ch = p.channel
    code = None
    if ch is None or p.dead or p.ghost or not on_hit_rule(ch) or not (dx or dy):
        code = "cannot"
    elif p.protected(now) or p.q_pending or p.question is not None:
        code = "answering"
    elif not dodge_unlocked(p):
        code = "locked"
    elif now < p.dodge_ready:
        code = "cooldown"
    if ch is None:
        return code
    d = plan()["dodge"]
    if code is not None:
        ch.queue_dash(p, seq, [], 0.0)
        return code
    total = float(d["dash_ms"])
    speed = float(d["dash_px"]) / (total / 1000.0)
    steps, left = [], int(round(total))
    while left > 0:
        part = min(DASH_STEP_MS, left)
        steps.append((dx, dy, part))
        left -= part
    if not ch.queue_dash(p, seq, steps, speed):
        return "cannot"
    p.dodge_ready = now + dodge_cooldown(p)
    p.dodge_until = now + float(d["invulnerable_seconds"])
    p.last_combat = now
    ch.event(k="dodge", id=p.eid, x=round(p.x, 1), y=round(p.y, 1), dx=dx, dy=dy)
    return None


def rule_view(p: "Player") -> dict | None:
    """What the client needs to play the open-world rule (sent with the zone), or None when
    this channel keeps Vấn Đạo."""
    if not on_hit_rule(p.channel):
        return None
    from ..learning import math_tree
    c = plan()
    u = next(x for x in math_tree.world_plan()["unlocks"] if x["id"] == c["dodge"]["unlock"])
    return {"rule": c["question_rule"], "rest": float(c["question_cooldown_seconds"]),
            "dodge": {"ok": dodge_unlocked(p), "unlock": {"realm": u["realm"], "stage": int(u["stage"])},
                      "dash_px": float(c["dodge"]["dash_px"]),
                      "dash_ms": float(c["dodge"]["dash_ms"]), "cooldown": dodge_cooldown(p),
                      "iframes": float(c["dodge"]["invulnerable_seconds"]), "step_ms": DASH_STEP_MS}}


def land_blow(ch: "ChannelZone", m: "Monster", p: "Player", dmg: float, now: float) -> str:
    """A telegraphed blow of `m` reached `p` (open-world rule). Returns what happened:
    dodged | paused | rest | asked."""
    c = plan()
    if now < p.dodge_until:
        ch.event(k="dodged", id=p.eid, by=m.eid, x=round(p.x, 1), y=round(p.y, 1))
        return "dodged"
    if p.protected(now) or p.q_pending or p.question is not None:
        return "paused"          # already answering one: the fight is paused for them
    engage(ch, m, p, now)        # a blow from a monster you never touched still makes it your fight
    if now < p.rest_until:
        amount = dmg * float(c["hit_during_cooldown"]["damage_taken"])
        if amount > 0:
            hurt_player(ch, p, amount, now, by=m.eid)
        return "rest"
    p.q_pending = True
    p.protect_until = now + float(c["question_wait_seconds"])   # held still while it is written
    p.last_combat = now
    ch.event(k="struck", id=p.eid, by=m.eid, x=round(p.x, 1), y=round(p.y, 1))
    _world().spawn(_create_question(ch, p, m.eid, m.kind, hit=dmg))
    return "asked"


def _unasked_blow(ch: "ChannelZone", p: "Player", mid: str, dmg: float) -> None:
    """No question could be written for a blow that landed (nothing open for this player, or
    an error): it counts as a blow during the rest window, and the rest window starts."""
    now = _world().mono()
    p.protect_until = 0.0
    c = plan()
    p.rest_until = now + float(c["question_cooldown_seconds"])
    amount = dmg * float(c["hit_during_cooldown"]["damage_taken"])
    if amount > 0 and p.channel is ch and not p.dead:
        hurt_player(ch, p, amount, now, by=mid)


def parry_heal(ch: "ChannelZone", p: "Player") -> int:
    """The worn Ngọc Thố (gift heal_on_right): a Phản Đòn heals a share of max HP. Returns the HP healed."""
    from ..systems import beasts
    share = beasts.gift_value(getattr(p, "pet", None), "heal_on_right")
    amount = min(p.max_hp - p.hp, p.max_hp * share) if share > 0 and not p.dead else 0.0
    if amount <= 0:
        return 0
    p.hp += amount
    ch.event(k="heal", id=p.eid, v=max(1, int(round(amount))), x=p.x, y=p.y)
    return int(round(amount))


def _parry(ch: "ChannelZone", p: "Player", q: dict, m: "Monster | None", correct: bool, now: float) -> dict:
    """The question of a blow was answered (or ran out): Phản Đòn, or the blow lands."""
    c = plan()
    rest = float(c["question_cooldown_seconds"])
    p.rest_until = now + rest
    if correct:
        right = c["right_answer"]
        p.mcombo += 1          # right answers in a row: the chiêu combo of the open world
        from ..systems import linh_can as lc      # the linh căn: more qi, a heal, a longer stun, a harder counter
        gain = float(right["linh_luc_gain"]) * (1 + lc.fx(p, "qi_gain"))
        p.qi = min(p.max_qi, p.qi + gain)
        if lc.fx(p, "heal_right") > 0:
            p.hp = min(p.max_hp, p.hp + p.max_hp * lc.fx(p, "heal_right"))
        out = {"parry": True, "correct": True, "rest": rest, "combo": p.mcombo, "qi_gain": gain,
               "damage": 0, "shield_broken": False, "stun": 0.0, "monster_hp": 0, "killed": False}
        if m is None or not m.alive:
            return {**out, "gone": True}
        broke = m.shield
        if broke:                                     # elite_shield_breaks_on: parry
            break_shield(ch, m, p, now)
        stun = float(right["stun_seconds"]) * (1 + lc.fx(p, "stun_pct"))
        m.tele = None
        m.moving = False
        m.stun_until = max(m.stun_until, now + stun)
        ch.event(k="parry", id=m.eid, by=p.eid, x=round(m.x, 1), y=round(m.y, 1), px=round(p.x, 1),
                 py=round(p.y, 1), st=stun)
        from ..systems import beasts, weapons   # a Phản Đòn on a question of the weapon's own branch hits harder
        wmult = weapons.parry_mult(p.weapon, q.get("subject"))
        fire = beasts.gift_value(getattr(p, "pet", None), "parry_fire")      # the worn Hỏa Tước
        if fire > 0:
            ch.event(k="fire", id=m.eid, by=p.eid, x=round(m.x, 1), y=round(m.y, 1))
        dealt = hurt_monster(ch, m, p, base_damage(p, m) * float(right["counter_multiplier"]) * wmult * (1 + fire)
                           * (1 + lc.fx(p, "parry_dmg")),
                             False, now)
        from . import beasts as wild     # a linh thú counts the Phản Đòn: enough of them and it yields
        tame = wild.on_parry(ch, m, p, now)
        res = {**out, "damage": int(round(dealt)), "weapon_bonus": wmult > 1.0, "shield_broken": broke, "stun": stun,
               "monster_hp": max(0, m.hp_pct()), "killed": not m.alive, "fire": fire > 0,
               "healed": parry_heal(ch, p)}                                   # the worn Ngọc Thố
        if tame is not None:
            res["tame"] = tame
        return res
    p.mcombo = 0
    from ..systems import beasts         # the worn Huyền Quy: a wrong answer's blow is lighter
    guard = beasts.gift_value(getattr(p, "pet", None), "wrong_guard")
    from ..systems import linh_can as lc     # and the linh căn's own guard
    amount = float(q["hit"]) * float(c["wrong_answer"]["damage_taken"]) * (1 - guard) * (1 - lc.fx(p, "wrong_guard"))
    taken = hurt_player(ch, p, amount, now, kind="gb", by=q["mid"], ignore_protect=True) if amount > 0 else 0.0
    out = {"parry": False, "correct": False, "rest": rest, "damage_taken": int(round(taken)),
           "hp": max(0, int(round(p.hp))), "dead": p.dead, "shows_solution": True, "guarded": guard > 0}
    if m is not None and getattr(m, "beast", False):      # the taming count so far, shown with the result
        out["tame"] = {"beast": m.kind, "name_vi": m.plan["name_vi"], "n": m.parries.get(p.user_id, 0),
                       "need": m.need, "yielded": False}
    return out


# ------------------------------------------------------------------ damage
def weapon_profile(p: "Player") -> dict:
    c = cfg()
    w = p.weapon
    if not w:
        return c["unarmed"]
    from ..systems import weapons   # a weapon of Thiên Địa Đồ: its type's own attack (world_plan.json)
    return c["weapon_kinds"].get(w) or weapons.fight_profile(w) or c["unarmed"]


def base_damage(p: "Player", m: "Monster") -> float:
    """A normal hit: attack x weapon multiplier, minus half the monster's defence."""
    atk = p.stats.get("atk", 10) * weapon_profile(p).get("mult", 1.0)
    return max(1.0, atk - m.info.get("def", 0) * cfg()["defense_factor"])


def roll_crit(p: "Player", rng: random.Random) -> bool:
    chance = p.stats.get("crit", 0) + weapon_profile(p).get("crit_bonus", 0)
    return rng.random() * 100 < chance


def hurt_monster(ch: "ChannelZone", m: "Monster", p: "Player | None", dmg: float, crit: bool, now: float,
                 bee: str | None = None) -> float:
    if not m.alive:
        return 0.0
    regrow = False
    if m.shield:  # spec 8.1: a shielded monster cannot be killed, a hit only scratches it
        dmg = float(cfg()["shielded_damage"])
        m.hp = max(1.0, m.hp - dmg)
    elif getattr(m, "beast", False):   # a linh thú is never killed: it is tamed (realtime/beasts.py)
        m.hp = max(1.0, m.hp - dmg)
    elif m.regen and m.hp - dmg <= m.max_hp * m.regen[0] / 100:
        # elites: the Mặc Thuẫn comes back at its threshold, even a huge hit stops there
        m.hp = min(m.hp, m.max_hp * m.regen[0] / 100)
        regrow = True
    else:
        m.hp -= dmg
    ev = {"k": "hit", "id": m.eid, "v": int(round(dmg)), "c": int(crit), "by": p.eid if p else None,
          "x": m.x, "y": m.y, "sh": int(m.shield)}
    if bee:
        ev["b"] = bee   # stung by a guard bee of this species
    ch.event(**ev)
    if p is not None:
        p.last_combat = now
    if m.hp <= 0:
        kill(ch, m, now)
        return dmg
    if regrow:
        m.regen.pop(0)
        m.shield = True
        m.group_hits = set()
        ch.event(k="shield", id=m.eid, on=1, x=m.x, y=m.y)
        for uid in m.engaged if not m.on_hit else ():   # open world: only a Phản Đòn breaks it again
            pl = ch.players.get(uid)
            if pl is not None and pl.question is None and not pl.dead:
                pl.next_q = (m.eid, now + 0.3)
    return dmg


def hurt_player(ch: "ChannelZone", p: "Player", dmg: float, now: float, kind: str = "hit", by: str | None = None,
                ignore_protect: bool = False) -> float:
    if p.dead or (p.protected(now) and not ignore_protect):
        return 0.0
    if now < p.guard_until:
        dmg *= 1 - p.guard_reduce
    dmg = max(1.0, dmg)
    p.hp -= dmg
    p.last_combat = now
    ch.event(k=kind, id=p.eid, v=int(round(dmg)), by=by, x=p.x, y=p.y)
    if p.hp <= 0:
        die(ch, p, now)
    return dmg


def mac_kich(p: "Player", m: "Monster") -> float:
    c = cfg()
    pct = c["mac_kich_pct"].get(m.info.get("rank", "normal"), 10)
    from ..systems import buffs
    res = min(p.stats.get("ink_res", 0) + buffs.ink_res(_world().buffs_left(p)), c["ink_res_cap"])
    dmg = p.max_hp * pct / 100 * (1 - res / 100)
    pet = getattr(p, "pet", None)
    if pet:   # Rắn (stage 8): Mặc Kích is lighter
        from ..systems import catalog
        sk = catalog.pets()["species"].get(pet, {}).get("skill", {})
        if sk.get("type") == "mac_kich":
            dmg *= 1 - float(sk["value"])
    return dmg


# ------------------------------------------------------------------ engagement
def engage(ch: "ChannelZone", m: "Monster", p: "Player", now: float) -> None:
    if not m.alive or p.dead:
        return
    if p.user_id not in m.engaged:
        m.engaged.add(p.user_id)
        if m.mode == "wander":
            m.mode = "chase"
            m.target = None
            m.idle = 0
    p.last_combat = now
    if m.on_hit:   # open world: nothing is asked until the monster lands a blow (land_blow)
        return
    if m.shield and p.question is None and not p.q_pending and p.next_q is None:
        request_question(ch, p, m, now)


def disengage(ch: "ChannelZone", m: "Monster", uid: int, now: float) -> None:
    m.engaged.discard(uid)
    p = ch.players.get(uid)
    if p is None:
        return
    if p.question and p.question["mid"] == m.eid and p.question.get("hit") is None:
        end_question(p, "gone")   # (the question of a blow that landed is still answered)
    if p.next_q and p.next_q[0] == m.eid:
        p.next_q = None


def end_question(p: "Player", reason: str) -> None:
    q = p.question
    p.question = None
    p.protect_until = 0.0
    if q and p.session is not None:
        p.session.send({"t": "q_end", "sid": q["sid"], "reason": reason})


def request_question(ch: "ChannelZone", p: "Player", m: "Monster", now: float) -> None:
    if p.question is not None or p.q_pending or now < p.no_question_until:
        return
    if p.user_id in m.group_hits:   # a bí cảnh boss: this player already did their part of the shield
        return
    p.q_pending = True
    p.next_q = None
    _world().spawn(_create_question(ch, p, m.eid, m.kind))


async def _own_floor_question(db, user, p: "Player", info: dict | None, rng: random.Random):
    """The Vấn Đạo question a Mặc Quái of the forest asks (spec 8.1): a quick math question at
    this player's own floor. It is graded like a quái lỗi sai's (math_combat: the learning log,
    then `on_answer`)."""
    from ..systems import math_ask, math_combat
    question = await math_ask.pick_own(db, user, qtypes=math_combat.QUICK_TYPES, rng=rng)
    if question is None:
        p.no_question_until = _world().mono() + 10
        if p.session:
            p.session.send({"t": "error", "code": "no_math_question",
                            "message_vi": "Con chưa mở được câu toán nào nên chưa phá được Mặc Thuẫn. "
                                          "Vào Đạo Thụ ở Động Phủ luyện một buổi rồi quay lại!"})
        return None
    question.meta["monster_vi"] = (info or {}).get("name_vi", "")
    return math_combat.CONTEXT, question


async def _math_question(db, user, p: "Player", info: dict, rng: random.Random):
    """The question a quái lỗi sai asks (M7): its own micro-skill, at this player's tier."""
    from ..systems import math_combat
    question = await math_combat.question_for(db, user, info, rng)
    if question is None:
        p.no_question_until = _world().mono() + 10
        if p.session:
            p.session.send({"t": "error", "code": "no_math_question",
                            "message_vi": "Chưa có câu toán nào cho lỗi này ở bậc của con. "
                                          "Luyện ở Động Phủ một lúc rồi quay lại!"})
        return None
    return math_combat.CONTEXT, question


async def _create_question(ch: "ChannelZone", p: "Player", mid: str, kind: str, hit: float | None = None) -> None:
    """Write the question this monster asks and open it. `hit`: the open-world rule - a blow of
    that much damage landed and this question decides it (Phản Đòn or not). The question
    itself is chosen the same way under both rules: a mistake monster's own micro-skill at the
    player's tier (math_combat.question_for), else the player's own floor (math_ask.pick_own)."""
    from ..learning import quiz
    from ..models import User
    from ..systems import codex, math_combat
    w = _world()
    rng = random.Random()
    try:
        async with dbm.SessionLocal() as db:
            user = await db.get(User, p.user_id)
            m0 = ch.monster(mid)
            info = m0.info if m0 is not None else None
            source = getattr(ch, "question_source", None)
            if source is not None:   # M10 realm: a math bí cảnh asks at the player's own floor, whoever asks
                built = await source(db, user, p, m0, rng)
            elif math_combat.is_mistake_monster(info):
                built = await _math_question(db, user, p, info, rng)
            else:
                built = await _own_floor_question(db, user, p, info, rng)
            if built is None:
                p.q_pending = False
                if hit is not None:
                    _unasked_blow(ch, p, mid, hit)
                return
            context, question = built
            out = await quiz.create_session(db, user, context, question, ref=f"{ch.key}|{mid}")
            first = False if getattr(m0, "beast", False) else await codex.meet_monster(db, p.user_id, kind)
            await db.commit()
    except Exception:
        log.exception("could not create a combat question")
        p.q_pending = False
        if hit is not None:
            _unasked_blow(ch, p, mid, hit)
        return
    p.q_pending = False
    now = w.mono()
    m = ch.monster(mid)
    if hit is not None:
        if (m is None or not m.alive or p.dead or p.channel is not ch or p.session is None
                or p.question is not None):
            if p.question is None:      # the monster fell (or we left) while it was written: no blow
                p.protect_until = 0.0
            return
    elif (m is None or not m.alive or not m.shield or p.dead or p.channel is not ch or p.session is None
            or p.user_id not in m.engaged or p.question is not None):
        return  # the fight moved on while the question was being written; it simply expires
    limit = float(question.time_limit)
    deadline = now + limit + balance.quiz()["network_grace"]
    p.question = {"sid": out["session_id"], "mid": mid, "deadline": deadline, "asked": now, "limit": limit,
                  "timeout_sent": False, "subject": (getattr(question, "meta", None) or {}).get("subject")}
    msg = {"t": "q", "mid": mid, "q": out, "first_meet": first}
    if hit is not None:
        p.question["hit"] = round(float(hit), 2)
        msg["hit"] = {"dmg": int(round(hit)), "monster_vi": m.info.get("name_vi", ""),
                      "rest": float(plan()["question_cooldown_seconds"])}
    p.protect_until = deadline
    p.inputs.clear()
    p.queued_ms = 0
    p.session.send(msg)


def on_answer(p: "Player", sid: str, correct: bool, answer_ms: int | None) -> dict:
    """Called (in memory) by a combat quiz handler (math_combat, a bí cảnh's) after the answer
    was graded and written to the learning log."""
    w = _world()
    q = p.question
    if q is None or q["sid"] != sid or p.channel is None:
        return {"stale": True}
    ch = p.channel
    now = w.mono()
    p.question = None
    p.protect_until = 0.0
    m = ch.monster(q["mid"])
    if q.get("hit") is not None:     # the open-world rule: a blow that landed
        return _parry(ch, p, q, m, correct, now)
    if m is None or not m.alive:
        return {"gone": True}
    c = cfg()
    if correct:
        if m.shield and m.info.get("group_shield"):
            progress = group_hit(ch, m, p)
            p.qi = min(p.max_qi, p.qi + c["correct_qi_gain"])
            if progress is not None:
                return {"correct": True, "shield_broken": False, "shield_progress": list(progress),
                        "damage": 0, "crit": False, "monster_hp": max(0, m.hp_pct()), "killed": False}
        broke = m.shield
        if m.shield:
            break_shield(ch, m, p, now)
        fast = answer_ms is not None and answer_ms <= c["fast_answer_fraction"] * q["limit"] * 1000
        dmg = base_damage(p, m) * c["ngo_dao_mult"] * (c["fast_answer_crit_mult"] if fast else 1.0)
        p.qi = min(p.max_qi, p.qi + c["correct_qi_gain"])
        dealt = hurt_monster(ch, m, p, dmg, fast, now)
        return {"correct": True, "shield_broken": broke, "damage": int(round(dealt)), "crit": fast,
                "monster_hp": max(0, m.hp_pct()), "killed": not m.alive}
    dmg = hurt_player(ch, p, mac_kich(p, m), now, kind="mk", by=m.eid, ignore_protect=True)
    if m.alive and m.shield and not p.dead:
        p.next_q = (m.eid, now + c["next_question_delay"])
    return {"correct": False, "mac_kich": int(round(dmg)), "hp": max(0, int(round(p.hp))), "dead": p.dead}


def group_hit(ch: "ChannelZone", m: "Monster", p: "Player") -> tuple[int, int] | None:
    """A right answer against a group shield (spec 14.2: the boss's big shield needs N right
    answers from N different players), from Vấn Đạo or a landed chiêu (M9) alike.
    Returns (have, need) while the shield still holds, None once this answer is enough."""
    m.group_hits.add(p.user_id)
    need = ch.group_need(m) if hasattr(ch, "group_need") else 1
    ch.event(k="gshield", id=m.eid, n=len(m.group_hits), need=need, by=p.eid, x=m.x, y=m.y)
    return (len(m.group_hits), need) if len(m.group_hits) < need else None


def break_shield(ch: "ChannelZone", m: "Monster", p: "Player | None", now: float) -> None:
    m.shield = False
    m.group_hits = set()
    ch.event(k="shield", id=m.eid, on=0, x=m.x, y=m.y, by=p.eid if p else None)
    for uid in list(m.engaged):  # whoever is right first breaks it for everyone (spec 8.1)
        other = ch.players.get(uid)
        if (other is not None and other is not p and other.question and other.question["mid"] == m.eid
                and not other.question.get("cast")      # a chiêu being channelled (M9) still lands
                and other.question.get("hit") is None):  # and a blow that landed is still decided
            end_question(other, "broken")


async def _grade_timeout(uid: int, sid: str) -> None:
    from ..learning import quiz
    from ..models import User
    try:
        async with dbm.SessionLocal() as db:
            user = await db.get(User, uid)
            await quiz.answer(db, user, sid, None)   # past expires_at: graded as timed out
            await db.commit()
    except quiz.QuizError:
        pass  # answered just in time
    except Exception:
        log.exception("timeout grading failed")


# ------------------------------------------------------------------ actions
def attack(p: "Player", eid: str, now: float, rng: random.Random) -> str | None:
    """Normal attack (left click). Returns an error code or None."""
    ch = p.channel
    if ch is None or p.dead:
        return "cannot"
    if p.protected(now):
        return "answering"
    if now < p.next_attack_at:
        return "cooldown"
    m = ch.monster(eid)
    if m is None or not m.alive or not m.fights(p):
        return "no_target"
    prof = weapon_profile(p)
    if dist(p.x, p.y - 6, m.x, m.y - 6) > prof["range"] + 10:
        return "too_far"
    p.next_attack_at = now + prof["cooldown"]
    dx, dy = m.x - p.x, m.y - p.y
    p.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")
    crit = roll_crit(p, rng)
    ch.event(k="atk", by=p.eid, id=m.eid, x=p.x, y=p.y, wp=p.weapon or "")
    engage(ch, m, p, now)
    from ..systems import linh_can   # a normal hit: the linh căn's basic_dmg
    hurt_monster(ch, m, p, base_damage(p, m) * (cfg_mult("crit_mult") if crit else 1.0)
                 * (1 + linh_can.fx(p, "basic_dmg")), crit, now)
    return None


def cfg_mult(key: str) -> float:
    return float(cfg()[key])


# ------------------------------------------------------------------ death & rewards
def kill(ch: "ChannelZone", m: "Monster", now: float) -> None:
    m.mode = "dead"
    m.hp = 0
    m.moving = False
    m.tele = None
    m.respawn_at = now + m.info.get("respawn_seconds", 30)
    ch.event(k="die", id=m.eid, x=m.x, y=m.y)
    for uid in list(m.engaged):
        p = ch.players.get(uid)
        if p is not None:
            if p.question and p.question["mid"] == m.eid and p.question.get("hit") is None:
                end_question(p, "killed")
            if p.next_q and p.next_q[0] == m.eid:
                p.next_q = None
            if not p.dead:
                _world().spawn(_reward(p.user_id, m.kind, _loot_bonus(p, m),
                                       source=getattr(ch, "realm_id", None) or ch.zone_id, x=m.x, y=m.y))
    _party_share(ch, m)
    for uid, ids in m.bee_assist.items():  # guard bees that helped grow a little
        if ids:
            _world().spawn(_bee_xp(uid, sorted(ids)))
    m.engaged = set()
    m.bee_assist = {}
    m.burn = None


def _party_share(ch: "ChannelZone", m: "Monster") -> None:
    """Spec 15.3: party members fighting nearby get part of the Tu Vi even if they did not
    touch this monster."""
    from ..systems import catalog
    rc = balance.load("realm")
    xp = int(catalog.monsters()[m.kind].get("xp", 0) * rc["party_xp_share"])
    if xp <= 0:
        return
    parties = _world().parties
    paid = set(m.engaged)
    for uid in list(m.engaged):
        for mate in parties.mates(uid):
            q = ch.players.get(mate)
            if mate in paid or q is None or q.dead or dist(q.x, q.y, m.x, m.y) > rc["party_share_radius"]:
                continue
            paid.add(mate)
            _world().spawn(_share_xp(mate, xp))


async def _share_xp(uid: int, xp: int) -> None:
    from ..systems import cultivation
    try:
        async with dbm.SessionLocal() as db:
            info = await cultivation.add_xp(db, uid, xp, "party")
            await db.commit()
    except Exception:
        log.exception("party xp failed")
        return
    _world().notify(uid, {"t": "party_xp", "xp": info})


def _loot_bonus(p: "Player", m: "Monster") -> dict:
    """Ong Ngọc Bích & co (skill 'loot'): more stones and drops from monsters they stung;
    the worn pet may add to it."""
    stung = m.bee_assist.get(p.user_id, set())
    best = {"stones_pct": 0.0, "drop_mult": 1.0}
    for b in p.bees:
        sk = b.skill or {}
        if b.id in stung and sk.get("type") == "loot":
            best["stones_pct"] = max(best["stones_pct"], float(sk.get("stones_pct", 0)))
            best["drop_mult"] = max(best["drop_mult"], float(sk.get("drop_mult", 1.0)))
    pet = getattr(p, "pet", None)
    if pet:   # Chó: more drops, Ngựa: more stones (stage 8)
        from ..systems import catalog
        sk = catalog.pets()["species"].get(pet, {}).get("skill", {})
        if sk.get("type") == "drop":
            best["drop_mult"] *= 1 + float(sk["value"])
        elif sk.get("type") == "kill_stones":
            best["stones_pct"] += float(sk["value"]) * 100
    from ..systems import linh_can   # the linh căn: drop_luck, stones_pct
    best["drop_mult"] *= 1 + linh_can.fx(p, "drop_luck")
    best["stones_pct"] += linh_can.fx(p, "stones_pct") * 100
    from ..systems import beasts     # the worn Tầm Bảo Thử (stones) and Kim Thiềm (drop luck)
    return beasts.loot_gift(pet, best)


async def _bee_xp(uid: int, bee_ids: list[int]) -> None:
    from ..systems import bees
    try:
        await bees.combat_xp(uid, bee_ids)
    except Exception:
        log.exception("bee xp failed")


async def _reward(uid: int, kind: str, loot: dict | None = None, rng: random.Random | None = None,
                  source: str | None = None, x: float | None = None, y: float | None = None) -> None:
    """The kill's loot for one player (party members each come through here): stones, then the
    monster's drop table gated by this player's tu vi (systems/loot.py) - a drop rolled but
    not yet unlocked is listed under `locked`, never granted - then the weapons of its land
    (systems/weapons.py roll_drops, same gate). Every piece of gear carries where it lies
    (x, y: the spot the monster died) for the client to draw on the ground."""
    from ..systems import catalog, codex, cultivation, inventory, items, quests, weapons
    from ..systems import loot as gate
    info = catalog.monsters()[kind]
    rng = rng or random.Random()
    loot = loot or {"stones_pct": 0.0, "drop_mult": 1.0}
    out = {"t": "loot", "monster": info["name_vi"], "items": [], "equipment": []}
    try:
        async with dbm.SessionLocal() as db:
            lo, hi = info.get("stones", [0, 0])
            stones = int(round(rng.randint(lo, hi) * (1 + loot["stones_pct"] / 100)))
            if stones:
                out["spirit_stones"] = await inventory.change_currency(db, uid, "spirit_stones", stones, "kill", kind)
                out["stones"] = stones
            realm, stage = await gate.player_tier(db, uid)
            # gear stays within the cap of the place of the kill (the wild zone or the bí cảnh);
            # with no place given, within the most generous cap of where this monster lives
            within = gate.source_cap(source) if source in gate.data().get("source_caps", {}) \
                else gate.monster_cap(kind)
            for d in info.get("drops", []):
                if rng.random() >= min(1.0, d["chance"] * loot["drop_mult"]):
                    continue
                if "item" in d:
                    qty = rng.randint(*d.get("qty", [1, 1]))
                    if not gate.unlocked(d["item"], realm, stage):
                        gate.note_locked(out, d["item"])
                        continue
                    out["items"] += await items.grant_items(db, uid, [{"item": d["item"], "qty": qty}], "drop", kind)
                else:
                    item_id = rng.choice(d["equipment"])
                    rar = gate.roll_equipment_rarity(rng, d.get("min_rarity"), realm, stage,
                                                     within=within)
                    if rar is None:
                        gate.note_locked_gear(out, item_id, d.get("min_rarity"))
                        continue
                    piece = await items.grant_equipment(db, uid, item_id, rar, "drop", kind)
                    out["equipment"].append(weapons.ground_entry(piece, x, y, len(out["equipment"])))
            await weapons.grant_drops(db, uid, kind, realm, stage, within, rng, loot["drop_mult"], out, x, y)
            out["kills"] = await codex.monster_killed(db, uid, kind)
            out["quests"] = await quests.on_event(db, uid, "kill", kind)
            out["xp"] = await cultivation.add_xp(db, uid, info.get("xp", 0), "kill")
            await db.commit()
    except Exception:
        log.exception("reward failed")
        return
    _world().notify(uid, out)


def die(ch: "ChannelZone", p: "Player", now: float) -> None:
    p.mcombo = 0   # the chiêu combo (M9) does not survive a fall
    if ch.instance:   # a bí cảnh: no Tu Vi lost, the player becomes a ghost (spec 14.2)
        ch.on_down(p, now)
        return
    p.dead = True
    p.hp = 0
    p.respawn_at = now + cfg()["death_overlay_seconds"]
    p.inputs.clear()
    p.queued_ms = 0
    ch.event(k="die", id=p.eid, x=p.x, y=p.y)
    for m in ch.monsters:
        if p.user_id in m.engaged:
            m.engaged.discard(p.user_id)
    if p.question:
        end_question(p, "dead")
    p.next_q = None
    if p.session is not None:
        p.session.send({"t": "dead", "respawn_in": cfg()["death_overlay_seconds"]})
    _world().spawn(_death_penalty(p.user_id))


async def _death_penalty(uid: int) -> None:
    from ..systems import cultivation
    try:
        async with dbm.SessionLocal() as db:
            from ..systems import linh_can   # a linh căn may keep part of it (death_guard)
            keep = 1 - await linh_can.value_db(db, uid, "death_guard")
            lost = await cultivation.lose_xp_pct(db, uid, cultivation.cfg()["death_xp_loss_pct"] * keep)
            await db.commit()
        _world().notify(uid, {"t": "xp_lost", "lost": lost})
    except Exception:
        log.exception("death penalty failed")


# ------------------------------------------------------------------ the tick
def _move_monster(m: "Monster", tx: float, ty: float, speed: float, dt: float, col) -> None:
    dx, dy = tx - m.x, ty - m.y
    d = math.hypot(dx, dy)
    if d < 0.5:
        m.moving = False
        return
    stepd = min(d, speed * dt)
    nx, ny = m.x + dx / d * stepd, m.y + dy / d * stepd
    if not col.blocked(nx, ny):
        m.x, m.y = nx, ny
    elif not col.blocked(nx, m.y):
        m.x = nx
    elif not col.blocked(m.x, ny):
        m.y = ny
    m.moving = True
    m.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")


def _respawn_monster(ch: "ChannelZone", m: "Monster") -> None:
    a = m.area
    for _ in range(20):
        x, y = ch.rng.uniform(a.x + 8, a.x + a.w - 8), ch.rng.uniform(a.y + 8, a.y + a.h - 8)
        if not ch.map.collider.blocked(x, y):
            m.x, m.y = x, y
            break
    m.reset()
    m.idle = 1.0


def _monster_tick(ch: "ChannelZone", m: "Monster", dt: float, now: float) -> None:
    c = cfg()
    info = m.info
    col = ch.map.collider
    if m.mode == "dead":
        if now >= m.respawn_at:
            _respawn_monster(ch, m)
        return
    if now < m.stun_until:  # stunned by a guard bee: no moving, no attacking
        m.moving = False
        m.tele = None
        return
    slow = m.slow_mult if now < m.slow_until else 1.0
    if m.mode == "return":
        hx, hy = m.home
        _move_monster(m, hx, hy, info["speed"] * c["return_speed_mult"], dt, col)
        if dist(m.x, m.y, hx, hy) < 6 or not m.moving:
            hp_keep = m.max_hp
            m.reset()
            m.hp = hp_keep
        return
    # who is it fighting?
    for uid in list(m.engaged):
        p = ch.players.get(uid)
        if p is None or p.dead:
            m.engaged.discard(uid)
    if not m.engaged and info.get("aggressive"):
        r = info.get("aggro_radius", 0)
        near = [p for p in ch.players.values() if not p.dead and dist(p.x, p.y, m.x, m.y) <= r
                and not (m.on_hit and (p.protected(now) or p.q_pending)) and m.fights(p)]
        if near:
            engage(ch, m, min(near, key=lambda p: dist(p.x, p.y, m.x, m.y)), now)
    if not m.engaged:
        if m.mode == "chase":
            m.mode = "return"
        else:
            m.update(dt, col, ch.rng)
        return
    hx, hy = m.home
    if dist(m.x, m.y, hx, hy) > c["leash_radius"]:  # dragged too far from home: give up and heal
        for uid in list(m.engaged):
            disengage(ch, m, uid, now)
        m.mode, m.tele = "return", None
        return
    m.mode = "chase"
    targets = [ch.players[u] for u in m.engaged if u in ch.players and m.fights(ch.players[u])]
    if m.on_hit:   # the fight is paused for whoever is answering: nobody swings at them
        targets = [p for p in targets if not p.protected(now) and not p.q_pending]
    if m.tele is not None:
        tele = m.tele
        if now >= tele["land"]:
            m.tele = None
            m.atk_ready = now + c["monster_attack_cooldown"]
            if m.on_hit:
                for p in list(ch.players.values()):
                    if not p.dead and not p.ghost and m.fights(p) and in_tele(tele, p.x, p.y):
                        dmg = max(1.0, info.get("atk", 5) - p.stats.get("def", 0) * c["defense_factor"])
                        land_blow(ch, m, p, dmg, now)
            elif targets:
                tgt = min(targets, key=lambda p: dist(p.x, p.y, m.x, m.y))
                dmg = max(1.0, info.get("atk", 5) - tgt.stats.get("def", 0) * c["defense_factor"])
                for p in list(ch.players.values()):
                    if not p.dead and in_tele(tele, p.x, p.y):
                        hurt_player(ch, p, dmg, now, by=m.eid)
            from . import guard
            guard.hit_bees(ch, m, now)
        m.moving = False
        return
    if not targets:      # its only foes are answering a question: it waits
        m.moving = False
        return
    tgt = min(targets, key=lambda p: dist(p.x, p.y, m.x, m.y))
    d = dist(tgt.x, tgt.y, m.x, m.y)
    reach = info.get("attack_radius", 20)
    if d <= reach + 6:
        m.moving = False
        if now >= m.atk_ready and not tgt.protected(now):
            if m.on_hit:
                from . import abilities      # Bày pháp trận: a monster standing in one winds up slower
                dur = windup() * abilities.windup_mult(ch, m, now)
                m.tele = make_tele(m, tgt.x, tgt.y, reach, now + dur, next_shape(m))
                ch.event(**tele_event(m, m.tele, dur))
            else:
                dur = c["telegraph_seconds"]
                m.tele = make_tele(m, tgt.x, tgt.y, reach, now + dur)
                ch.event(k="tele", id=m.eid, x=round(tgt.x, 1), y=round(tgt.y, 1), r=reach, d=dur)
        return
    _move_monster(m, tgt.x, tgt.y, info["speed"] * c["chase_speed_mult"] * slow, dt, col)


def tick(ch: "ChannelZone", dt: float, now: float) -> None:
    from ..systems.linh_can import fx as lc_fx
    c = cfg()
    w = _world()
    for m in ch.monsters:
        _monster_tick(ch, m, dt, now)
    for p in list(ch.players.values()):
        if p.dead:
            if now >= p.respawn_at:
                w.respawn(p)
            continue
        q = p.question
        if q is not None and now >= q["deadline"] + 0.25 and not q["timeout_sent"]:
            q["timeout_sent"] = True  # nobody answered in time: grade it as a timeout (= wrong)
            w.spawn(_grade_timeout(p.user_id, q["sid"]))
        if p.next_q is not None and now >= p.next_q[1] and p.question is None and not p.q_pending:
            mid = p.next_q[0]
            p.next_q = None
            m = ch.monster(mid)
            if m is not None and m.alive and m.shield and p.user_id in m.engaged:
                request_question(ch, p, m, now)
        if now - p.last_combat > c["out_of_combat_seconds"]:
            mult = c["safe_zone_regen_mult"] if ch.safe else 1.0
            p.hp = min(p.max_hp, p.hp + p.max_hp * c["hp_regen_pct_per_second"] / 100 * dt * mult)
            p.qi = min(p.max_qi, p.qi + c["qi_regen_per_second"] * dt * mult * (1 + lc_fx(p, "qi_regen")))
