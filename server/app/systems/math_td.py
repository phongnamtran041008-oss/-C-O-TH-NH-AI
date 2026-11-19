"""Thủ thành toán (M10, kế hoạch 4.3): tower defense where every tower stands for an area of
mathematics, and a tower is placed or upgraded by answering a question of that area.

The parts that keep a run honest live in systems/td.py and td_sim.py:

  * the simulation, td_sim.py, run by the client and replayed by the server: a "place" or
    "up" event must carry a question about that tower that the server recorded as answered
    right;
  * the run table and log handling (td.save_events / td.verify), so a log is checked against
    the saved part, the server's own answers, the claimed result and real time.

The learning rules (contract M10):

  * every question comes from math_ask: `pick` on the tower's area for placing and
    upgrading, `pick_own` (the player's own floor) for the Linh Khí questions between waves
    and the Tụ Khí button; the tier is the player's own and never above it;
  * the answer is written to `math_answers` with no run (math_ask.record) and pays Tu Vi by
    tier (math_ask.xp_rule);
  * a tower is available only when its area has questions and lies on a floor the player
    has reached on Đạo Thụ (math_tree_progress.reached_floors), and it asks only the
    micro-skills of its area the player has open. Towers of subjects without questions are in the data,
    shown locked with the reason, and open by themselves the day the subject gets questions;
  * a wrong answer or a timeout places / upgrades nothing. The Linh Khí of the attempt is
    spent ("Linh Khí bỏ ra không hoàn lại"), as a missed chiêu of M9 is; nothing else is lost (no Linh Mạch point, no tower). A wrong
    Tụ Khí costs nothing here (`tu_khi_wrong_loss` 0 in the data).

A tower's strength never reads mastery: it is the tower's `power` from the data times
`tier_power` of the question that placed it (an upgrade keeps the highest tier reached).
The multiplier is fixed when the question is asked and is part of the server's answer
record, so the replay computes exactly what the client did.
"""
from __future__ import annotations

import datetime as dt
import json
import random
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from .. import clock
from ..config import DATA_DIR
from ..learning import math_items, math_path, quiz
from ..models import QuizSession, TdProgress, TdRun, User
from . import catalog, math_ask, math_practice, math_tree_progress, td, td_sim
from .td import TdError

CONTEXT = "math_td"
DATA_FILE = DATA_DIR / "math" / "td.json"
ROLES = ("hoa", "thuy", "kim", "son", "quang", "ho_tro", "sinh_khi", "moc")   # behaviours td_sim knows


# ------------------------------------------------------------------ data
def _read() -> dict:
    return json.loads(DATA_FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    return _read()


def towers() -> dict[str, dict]:
    return {t["id"]: t for t in data()["towers"]}


def levels() -> dict[str, dict]:
    return {lv["id"]: lv for lv in data()["levels"]}


def subject_names() -> dict[str, str]:
    """Every subject of math/subjects.json, written or not (a locked tower names its subject)."""
    return {s["id"]: s["name_vi"] for s in math_path.load_index()["subjects"]}


def tier_power(tier: int) -> float:
    return float(data()["tier_power"][str(tier)])


def qtypes() -> list[str]:
    """The question types this mode asks (td.json `qtypes`): short ones only - no Thiên kiếp
    in the middle of a wave."""
    return list(data()["qtypes"])


def area_skills(t: dict) -> list[str]:
    """The micro-skills a tower asks about: the listed ones, or every one of its floor."""
    a = t["area"]
    if a.get("skills"):
        return list(a["skills"])
    try:
        return [k.id for k in math_path.subject(a["subject"]).floor(int(a["floor"])).skills]
    except KeyError:
        return []


# ------------------------------------------------------------------ which towers a player has
def content_lock(t: dict) -> str | None:
    """Why nobody can build this tower today (its area has no question), or None. It reads
    the bank, so a tower of a subject that gets questions later opens with no data change."""
    a = t["area"]
    sid, floor = a["subject"], int(a["floor"])
    name = subject_names().get(sid, sid)
    if sid not in {s.id for s in math_path.subjects()}:
        return f"Bí cảnh {name} chưa có câu hỏi: tháp này mở khi môn ấy có câu."
    if floor not in math_ask.playable_floors(sid):
        return f"Tầng {floor} của {name} chưa có câu hỏi: tháp này mở khi tầng ấy có câu."
    skills = set(area_skills(t))
    kinds = set(qtypes())
    if not any(tp.skill in skills and tp.qtype in kinds for tp in math_practice._templates(sid, floor)):
        return f"Mảng này ở tầng {floor} của {name} chưa có câu hỏi."
    return None


async def tower_skills(db: AsyncSession, user_id: int, t: dict,
                       st: math_tree_progress.TreeState | None = None) -> list[str]:
    """The micro-skills of the tower's area this player may be asked: those of main-path
    nodes of Đạo Thụ they have open or done, and those of optional nodes they have finished
    (R6: an optional node is asked in its own sittings, and again once it is done)."""
    st = st or await math_tree_progress.state(db, user_id)
    allowed = math_tree_progress.allowed_skills_of(st) | math_tree_progress.finished_optional_skills_of(st)
    return [k for k in area_skills(t) if k in allowed]


async def tower_lock(db: AsyncSession, user_id: int, t: dict,
                     st: math_tree_progress.TreeState | None = None) -> str | None:
    """Why this player cannot build this tower yet, or None (rule: the learning path - the
    tower's floor must hold an open or passed main-path part of Đạo Thụ, and some micro-skill
    of its area must be open)."""
    why = content_lock(t)
    if why:
        return why
    a = t["area"]
    floor = int(a["floor"])
    st = st or await math_tree_progress.state(db, user_id)
    # a floor that holds only optional nodes is never "reached" on the main path: its tower
    # opens when the player has finished the optional node its area belongs to
    nodes = math_tree_progress.tree().nodes
    main_floor = any(nodes[p.node_id].main for p in math_tree_progress.floor_parts(a["subject"], floor))
    reached = floor in math_tree_progress.reached_floors_of(st, a["subject"]) if main_floor else True
    if not reached or not await tower_skills(db, user_id, t, st):
        name = subject_names().get(a["subject"], a["subject"])
        return f"Học tới tầng {floor} của {name} trên Đạo Thụ để mở tháp này."
    return None


def tower_view(t: dict, locked_vi: str | None) -> dict:
    r = data()["roles"][t["role"]]
    a = t["area"]
    return {"id": t["id"], "name_vi": t["name_vi"], "label": t["label"], "role": t["role"], "desc_vi": t["desc_vi"],
            "power": t["power"], "cost": r.get("cost", 0), "subject": a["subject"],
            "subject_name_vi": subject_names().get(a["subject"], a["subject"]), "floor": int(a["floor"]),
            "available": locked_vi is None, "locked_vi": locked_vi}


async def tower_views(db: AsyncSession, user_id: int) -> list[dict]:
    st = await math_tree_progress.state(db, user_id)
    return [tower_view(t, await tower_lock(db, user_id, t, st)) for t in data()["towers"]]


def sim_towers(views: list[dict]) -> dict[str, dict]:
    """What td_sim needs of the towers this player may build (its `plants`), with the label
    and name the board shows."""
    return {v["id"]: {"role": v["role"], "label": v["label"], "name_vi": v["name_vi"], "power": float(v["power"])}
            for v in views if v["available"]}


def build_params(level: dict, defs: dict[str, dict], seed: int) -> dict:
    """Everything td_sim needs, sent to the client as is. Monsters and the two safety numbers
    of the simulation are in balance/td.json; the rest is math/td.json."""
    d, c = data(), td.cfg()
    return {"level": level["id"], "cols": d["grid"]["cols"], "rows": d["grid"]["rows"], "path": level["path"],
            "rocks": level.get("rocks", []), "core_hp": d["core_hp"], "qi": d["qi"], "upgrade": d["upgrade"],
            "sell_refund": d["sell_refund"], "roles": d["roles"], "monsters": c["monsters"],
            "boss_stun_mult": c["boss_stun_mult"], "wave_max_seconds": c["wave_max_seconds"], "plants": defs,
            "seed": seed, "waves": level["waves"], "hp_mult": 1.0}


# ------------------------------------------------------------------ levels
def unlocked(level_id: str, prog: dict[str, TdProgress]) -> tuple[bool, str | None]:
    ids = [lv["id"] for lv in data()["levels"]]
    i = ids.index(level_id)
    if i == 0:
        return True, None
    prev = prog.get(ids[i - 1])
    if prev is None or prev.stars <= 0:
        return False, f"Giữ được {levels()[ids[i - 1]]['name_vi']} trước đã."
    return True, None


def _daily(user: User) -> dict:
    d = dict((user.flags or {}).get("math_td_daily") or {})
    today = clock.local_date(clock.now())
    return d if d.get("date") == today else {"date": today, "n": 0}


def daily_left(user: User) -> int:
    return max(0, data()["rewards"]["daily_rewarded_plays"] - _daily(user)["n"])


def _use_daily(user: User) -> None:
    d = _daily(user)
    d["n"] += 1
    user.flags = {**(user.flags or {}), "math_td_daily": d}


def stars_for(core_hp: int) -> int:
    need = data()["stars"]
    return next((s for s in (3, 2, 1) if core_hp >= need[str(s)]), 0)


def reward_view(r: dict) -> dict:
    """A reward as the client shows it: items with their names."""
    out = {k: v for k, v in r.items() if k != "items"}
    if r.get("items"):
        out["items"] = [{"item": k, "qty": n, "name_vi": catalog.item_name(k)} for k, n in r["items"].items()]
    return out


async def view(db: AsyncSession, user: User) -> dict:
    """The level screen: levels with stars and first rewards, every tower (locked ones with
    the reason), and a run left unfinished."""
    prog = await td.progress(db, user.id)
    out = []
    for lv in data()["levels"]:
        ok, why = unlocked(lv["id"], prog)
        pr = prog.get(lv["id"])
        out.append({"id": lv["id"], "name_vi": lv["name_vi"], "desc_vi": lv["desc_vi"], "waves": len(lv["waves"]),
                    "unlocked": ok, "locked_vi": why, "stars": pr.stars if pr else 0,
                    "best_wave": pr.best_wave if pr else 0,
                    "monsters": [td.monster_card(k) for k in td.monster_kinds(lv)],
                    "first_rewards": [reward_view(r) for r in lv["first_rewards"]]})
    run = await td.current_run(db, user.id)
    active = None
    if run is not None:
        active = {"run_id": run.id, "level_id": run.level_id, "name_vi": levels()[run.level_id]["name_vi"],
                  "waves": sum(1 for e in run.events or [] if isinstance(e, dict) and e.get("k") == "wave")}
    return {"levels": out, "towers": await tower_views(db, user.id), "roles": data()["roles"],
            "active_run": active, "stars_need": data()["stars"], "daily_left": daily_left(user),
            "daily_max": data()["rewards"]["daily_rewarded_plays"]}


async def run_view(db: AsyncSession, user: User, row: TdRun) -> dict:
    lv = levels()[row.level_id]
    return {"run_id": row.id, "level_id": row.level_id, "params": row.params, "step_ms": td_sim.STEP_MS,
            "max_speed": td.cfg()["anti_cheat"]["max_speed"], "name_vi": lv["name_vi"],
            "monsters": [td.monster_card(k) for k in td.monster_kinds(lv)],
            "towers": await tower_views(db, user.id)}


# ------------------------------------------------------------------ a run
async def start(db: AsyncSession, user: User, level_id: str, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    if level_id not in levels():
        raise TdError(404, "no_level", "Không có ải này.")
    ok, why = unlocked(level_id, await td.progress(db, user.id))
    if not ok:
        raise TdError(400, "locked", why or "Ải này chưa mở.")
    defs = sim_towers(await tower_views(db, user.id))
    if not defs:
        raise TdError(400, "no_tower", "Chưa có tháp nào dựng được: mảng toán của con chưa có câu hỏi.")
    params = build_params(levels()[level_id], defs, rng.randrange(1, 2 ** 31))
    from . import pets
    bonus = await pets.skill_value(db, user.id, "td_qi")   # Khỉ (stage 8): more Linh Khí to start with
    if bonus:
        params["qi"] = {**params["qi"], "start": params["qi"]["start"] + int(bonus)}
    row = await td.new_run(db, user, level_id, params)       # one run at a time
    return await run_view(db, user, row)


async def ask(db: AsyncSession, user: User, run_id: str, kind: str, tower_id: str | None,
              rng: random.Random | None = None) -> dict:
    """A question for the run. 'place' / 'upgrade': about the tower's own area of mathematics;
    'break' (between waves) / 'tu_khi' (the button during a wave): at the player's own floor.
    The answer comes back through /quiz/answer; the run remembers it for the replay."""
    rng = rng or random.Random()
    run = await td.get_run(db, user.id, run_id)
    if len(run.questions or {}) >= td.cfg()["anti_cheat"]["max_questions"]:
        raise TdError(400, "too_many", "Đã hỏi quá nhiều câu trong lượt này.")
    if kind in ("place", "upgrade"):
        if not isinstance(tower_id, str) or tower_id not in run.params["plants"] or tower_id not in towers():
            raise TdError(400, "no_tower", "Tháp này không dựng được trong lượt này.")
        t = towers()[tower_id]
        skills = await tower_skills(db, user.id, t)
        rng.shuffle(skills)
        question = await math_ask.pick(db, user, t["area"]["subject"], int(t["area"]["floor"]), skills=skills,
                                       qtypes=qtypes(), rng=rng)
    elif kind in ("break", "tu_khi"):
        tower_id = ""
        question = await math_ask.pick_own(db, user, qtypes=qtypes(), rng=rng)
    else:
        raise TdError(400, "bad_kind", "Loại câu hỏi không hợp lệ.")
    if question is None:
        raise TdError(400, "no_question", "Mảng toán này chưa có câu nào hợp với con lúc này.")
    tier = int(question.public()["math"]["tier"])
    power = tier_power(tier)
    out = await quiz.create_session(db, user, CONTEXT, question, ref=run.id)
    run.questions = {**(run.questions or {}),
                     out["session_id"]: {"kind": kind, "word": tower_id, "ok": None, "power": power, "tier": tier}}
    return {**out, "math_td": {"kind": kind, "tower": tower_id, "power": power}}


async def math_td_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool, now: dt.datetime) -> dict:
    """Grading a question of a run: the learning log first (rule 3), then the run remembers
    the result, which is what the replay uses (the client's word is never trusted)."""
    out: dict = {"math": await math_ask.record(db, user, s, correct, now)}
    run = await db.get(TdRun, s.ref) if s.ref else None
    if run is not None and run.user_id == user.id and s.id in (run.questions or {}):
        q = {**run.questions[s.id], "ok": bool(correct)}
        run.questions = {**run.questions, s.id: q}
        c = data()["qi"]
        gain = {"break": c["break_qi"] if correct else 0,
                "tu_khi": c["tu_khi_qi"] if correct else -c["tu_khi_wrong_loss"]}.get(q["kind"], 0)
        out["math_td"] = {"kind": q["kind"], "tower": q["word"], "ok": bool(correct), "power": q["power"], "qi": gain}
    return out


quiz.register_handler(CONTEXT, math_td_handler)
quiz.register_xp_rule(CONTEXT, math_ask.xp_rule)


async def save_events(db: AsyncSession, user: User, run_id: str, start_at: int, events: list) -> dict:
    return await td.save_events(db, user, run_id, start_at, events)


async def resume(db: AsyncSession, user: User) -> dict:
    """Continue the run left unfinished: its parameters, the saved log and the answers the log
    uses (a question asked after the last save was never applied, so it is dropped)."""
    row = await td.current_run(db, user.id)
    if row is None:
        raise TdError(404, "no_run", "Không có lượt thủ thành nào đang dở.")
    td.drop_unlogged_questions(row)
    return {**(await run_view(db, user, row)), "events": row.events, "answers": td.answers(row)}


async def cancel(db: AsyncSession, user: User) -> dict:
    return await td.cancel(db, user)


async def finish(db: AsyncSession, user: User, run_id: str, events: list, claim: dict) -> dict:
    """The server replays the log (td.verify) and only then pays: first-time stars give the
    level's `first_rewards`; a level won again pays `replay_stones` a few times a day. A lost
    run pays nothing here (its right answers already paid Tu Vi). A win counts for the
    "td_win" quests."""
    sim, got, level_id = await td.verify(db, user, run_id, events, claim)
    await td.record_monsters(db, user.id, sim)
    lv = levels()[level_id]
    row = await db.get(TdProgress, (user.id, level_id))
    if row is None:
        row = TdProgress(user_id=user.id, level_id=level_id, stars=0, best_wave=0)
        db.add(row)
    prev = row.stars
    won = sim.phase == td_sim.WON
    stars = stars_for(sim.hp) if won else 0
    row.best_wave = max(row.best_wave, sim.wave if won else sim.wave - 1)
    rewards: dict = {}
    new_stars = []
    if stars > prev:
        for s in range(prev + 1, stars + 1):
            rewards = td.merge(rewards, await td.grant(db, user, lv["first_rewards"][s - 1], level_id))
            new_stars.append(s)
        row.stars = stars
        if row.cleared_at is None:
            row.cleared_at = clock.now()
    elif won and daily_left(user) > 0:
        _use_daily(user)
        rewards = await td.grant(db, user, {"spirit_stones": data()["rewards"]["replay_stones"]}, level_id)
        rewards["replay"] = True
    if won:
        from . import quests
        await quests.on_event(db, user.id, "td_win", "*")
    await db.flush()
    ids = [x["id"] for x in data()["levels"]]
    i = ids.index(level_id)
    nxt = ids[i + 1] if won and i + 1 < len(ids) else None
    return {**got, "stars": stars, "prev_stars": prev, "new_stars": new_stars, "rewards": rewards,
            "daily_left": daily_left(user), "next_level": nxt}


# ------------------------------------------------------------------ checks (tools/check_all.py)
def _cell(c, cols: int, rows: int) -> bool:
    return (isinstance(c, list) and len(c) == 2 and all(isinstance(v, int) and not isinstance(v, bool) for v in c)
            and 0 <= c[0] < cols and 0 <= c[1] < rows)


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(raw: dict | None = None) -> list[str]:
    """Problems with math/td.json (empty = sound): towers with a known behaviour and a real
    area (a subject of subjects.json; for a written subject, a real floor and real
    micro-skills), levels whose path is a walk of neighbouring cells, waves of real monsters,
    rewards of real items, and at least one tower a brand-new player can build."""
    d = raw if raw is not None else _read()
    errs: list[str] = []
    for key in ("grid", "core_hp", "qtypes", "qi", "upgrade", "sell_refund", "tier_power", "roles", "towers",
                "stars", "rewards", "levels"):
        if key not in d:
            errs.append(f"missing {key}")
    if errs:
        return errs
    kinds = d["qtypes"]
    if not isinstance(kinds, list) or not kinds or not all(k in math_items.PLAYABLE_TYPES for k in kinds):
        errs.append(f"qtypes must be a non-empty list of playable question types ({', '.join(math_items.PLAYABLE_TYPES)})")
    elif "tribulation" in kinds:
        errs.append("qtypes: a Thiên kiếp (tribulation) takes 8-12 minutes, too long for a tower or a break")
    cols, rows = d["grid"].get("cols"), d["grid"].get("rows")
    if (cols, rows) != (12, 7):
        errs.append("grid must be 12 x 7 (the client draws that board)")
        return errs
    for k in ("start", "regen_per_s", "wave_bonus", "break_questions", "break_qi", "tu_khi_qi", "tu_khi_wrong_loss",
              "tu_khi_cooldown_s"):
        if not _num(d["qi"].get(k)) or d["qi"][k] < 0:
            errs.append(f"qi.{k} must be a number >= 0")
    if not all(str(t) in d["tier_power"] and _num(d["tier_power"][str(t)]) and d["tier_power"][str(t)] > 0
               for t in range(1, 6)):
        errs.append("tier_power needs a positive number for tiers 1-5")
    ups = d["upgrade"]
    if len(ups.get("level_mult", [])) != len(ups.get("cost", [])) + 1:
        errs.append("upgrade.level_mult must have one more entry than upgrade.cost")
    for role, st in d["roles"].items():
        if role not in ROLES:
            errs.append(f"role {role}: td_sim has no such behaviour")
        elif not _num(st.get("cost")) or st["cost"] <= 0:
            errs.append(f"role {role}: cost must be > 0")
        elif role not in ("ho_tro", "sinh_khi", "moc") and not all(_num(st.get(k)) for k in ("range", "cd", "dmg")):
            errs.append(f"role {role}: needs range, cd and dmg")
    names = {s["id"]: s for s in math_path.load_index()["subjects"]}
    written = {s.id: s for s in math_path.subjects()}
    seen: set[str] = set()
    for t in d["towers"]:
        tid = t.get("id")
        if not tid or tid in seen:
            errs.append(f"tower {tid!r}: missing or repeated id")
            continue
        seen.add(tid)
        for k in ("name_vi", "label", "desc_vi"):
            if not isinstance(t.get(k), str) or not t[k]:
                errs.append(f"tower {tid}: {k} missing")
        if t.get("role") not in d["roles"]:
            errs.append(f"tower {tid}: role {t.get('role')!r} is not in roles")
        if not _num(t.get("power")) or t["power"] <= 0:
            errs.append(f"tower {tid}: power must be > 0")
        a = t.get("area") or {}
        if a.get("subject") not in names:
            errs.append(f"tower {tid}: subject {a.get('subject')!r} is not in math/subjects.json")
            continue
        if not isinstance(a.get("floor"), int) or a["floor"] < 1:
            errs.append(f"tower {tid}: floor must be an integer >= 1")
            continue
        if a.get("skills") is not None and (not isinstance(a["skills"], list) or not a["skills"]):
            errs.append(f"tower {tid}: skills must be null or a non-empty list")
            continue
        subj = written.get(a["subject"])
        if subj is None:
            continue                     # a subject still to be written: the tower stays locked
        try:
            floor = subj.floor(a["floor"])
        except KeyError:
            errs.append(f"tower {tid}: {a['subject']} has no floor {a['floor']}")
            continue
        real = {k.id for k in floor.skills}
        for k in a.get("skills") or []:
            if k not in real:
                errs.append(f"tower {tid}: {k} is not a micro-skill of floor {a['floor']}")
    monsters = td.cfg()["monsters"]
    for lid, lv in enumerate(d["levels"]):
        name = lv.get("id", f"#{lid}")
        if not isinstance(lv.get("id"), str) or not td.is_math(lv["id"]) or len(lv["id"]) > 32:
            errs.append(f"level {name}: id must start with {td.MATH_PREFIX!r} (at most 32 characters)")
        for k in ("name_vi", "desc_vi"):
            if not isinstance(lv.get(k), str) or not lv[k]:
                errs.append(f"level {name}: {k} missing")
        path = lv.get("path") or []
        if len(path) < 4 or not all(_cell(c, cols, rows) for c in path):
            errs.append(f"level {name}: path must be at least 4 cells inside the grid")
        else:
            if any(abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1 for a, b in zip(path, path[1:])):
                errs.append(f"level {name}: path cells must be neighbours")
            if len({tuple(c) for c in path}) != len(path):
                errs.append(f"level {name}: path crosses itself")
        rocks = lv.get("rocks") or []
        if not all(_cell(c, cols, rows) for c in rocks) or any(c in path for c in rocks):
            errs.append(f"level {name}: rocks must be inside the grid and off the path")
        waves = lv.get("waves") or []
        if not waves:
            errs.append(f"level {name}: no waves")
        for w in waves:
            for g in w:
                if g.get("m") not in monsters or not isinstance(g.get("n"), int) or g["n"] < 1 \
                        or not isinstance(g.get("gap"), int) or not isinstance(g.get("at"), int):
                    errs.append(f"level {name}: bad wave group {g}")
        fr = lv.get("first_rewards")
        if not isinstance(fr, list) or len(fr) != 3:
            errs.append(f"level {name}: first_rewards needs one reward per star (3)")
        else:
            for r in fr:
                for item in (r.get("items") or {}):
                    if catalog.stack_item(item) is None:
                        errs.append(f"level {name}: reward item {item} does not exist")
    if raw is None and not any(content_lock(t) is None and int(t["area"]["floor"]) == 1 for t in d["towers"]):
        errs.append("no tower of a floor-1 area has questions: a new player could not build anything")
    return errs
