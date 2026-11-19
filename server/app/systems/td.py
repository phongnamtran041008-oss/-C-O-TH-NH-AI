"""The run plumbing of the tower defence (Thủ Thành Toán, systems/math_td.py): a run from
start to finish, its saved log, the anti-cheat replay, the Yêu Quái Phổ entries and the
payout helpers.

The game runs on the client (td_sim.py, the same file on both sides). The server picks the
seed, sends every number the simulation needs, asks and grades every question, and at the
end replays the client's event log (`td_sim.replay`): only a log that reaches exactly the
result the client claims, within a believable real time, earns anything. A run in progress
is saved in `td_runs` with its log, so a game closed mid-level can continue it.

Level ids start with MATH_PREFIX (they are the keys of `td_progress` and `td_runs`, so they
never change). Rows left in those tables by the word tower defence that was removed have
other ids: they are never shown or continued, and a new run deletes the player's old ones.

Numbers shared by every level (monsters, anti-cheat, the simulation's safety limits) are in
balance/td.json; everything else of the mode is in math/td.json.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from ..models import CodexEntry, TdProgress, TdRun, User
from . import inventory, items, td_sim

MATH_PREFIX = "math_"      # every level id of the tower defence starts with this

# Wave 2: the old library (systems/library.py) and inscription (systems/inscription.py) still
# read a word's plant role as td.role_of / td.roles_data / td.power / td.plant_entries. Those
# helpers live in word_plants.py; this forwards the names until those features are deleted.
_WORD_LEFTOVERS = ("role_of", "roles_data", "power", "plant_entries")


def __getattr__(name: str):
    if name in _WORD_LEFTOVERS:
        from . import word_plants
        return getattr(word_plants, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def is_math(level_id: str) -> bool:
    return level_id.startswith(MATH_PREFIX)


def _ours():
    """SQL filter: runs of this mode (not leftovers of the removed word tower defence)."""
    return TdRun.level_id.startswith(MATH_PREFIX, autoescape=True)


class TdError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


def cfg() -> dict:
    return balance.load("td")


# ------------------------------------------------------------------ monsters and progress
def monster_kinds(level: dict) -> list[str]:
    seen: list[str] = []
    for wave in level["waves"]:
        for g in wave:
            if g["m"] not in seen:
                seen.append(g["m"])
    return seen


def monster_card(kind: str) -> dict:
    m = cfg()["monsters"][kind]
    return {"id": kind, "name_vi": m["name_vi"], "hp": m["hp"], "speed": m["speed"], "leak": m["leak"],
            "resist": m["resist"], "weakness_vi": m["weakness_vi"], "hidden": bool(m.get("hidden")),
            "boss": bool(m.get("boss"))}


async def progress(db: AsyncSession, user_id: int) -> dict[str, TdProgress]:
    return {r.level_id: r for r in (await db.execute(select(TdProgress).where(TdProgress.user_id == user_id))).scalars()}


# ------------------------------------------------------------------ runs
_finishing: set[str] = set()     # runs whose log is being replayed right now


def _expired(row: TdRun) -> bool:
    return clock.now() - row.started_at > dt.timedelta(hours=cfg()["anti_cheat"]["run_hours"])


async def _drop(db: AsyncSession, row: TdRun) -> None:
    """Delete a run for good (committed now: the error that follows rolls back the rest)."""
    await db.delete(row)
    await db.commit()


async def current_run(db: AsyncSession, user_id: int) -> TdRun | None:
    row = (await db.execute(select(TdRun).where(TdRun.user_id == user_id, _ours())
                            .order_by(TdRun.started_at.desc()))).scalars().first()
    if row is not None and _expired(row):
        await db.delete(row)
        await db.flush()
        return None
    return row


async def get_run(db: AsyncSession, user_id: int, run_id: str) -> TdRun:
    row = await db.get(TdRun, run_id) if isinstance(run_id, str) else None
    if row is None or row.user_id != user_id or not is_math(row.level_id):
        raise TdError(404, "no_run", "Lượt thủ thành này không còn nữa, vào ải lại nhé.")
    if _expired(row):
        await _drop(db, row)
        raise TdError(404, "no_run", "Lượt thủ thành này đã quá lâu, vào ải lại nhé.")
    return row


async def new_run(db: AsyncSession, user: User, level_id: str, params: dict) -> TdRun:
    """A new run replaces any run the player left unfinished."""
    await db.execute(delete(TdRun).where(TdRun.user_id == user.id))
    now = clock.now()
    row = TdRun(id=uuid.uuid4().hex, user_id=user.id, level_id=level_id, params=params, questions={}, events=[],
                started_at=now, updated_at=now)
    db.add(row)
    await db.flush()
    return row


def _check_events(events, last_step: int) -> None:
    if not isinstance(events, list):
        raise TdError(400, "bad_log", "Nhật ký ải không hợp lệ.")
    for ev in events:
        s = ev.get("s") if isinstance(ev, dict) else None
        if not isinstance(s, int) or isinstance(s, bool) or s < last_step or not isinstance(ev.get("k"), str):
            raise TdError(400, "bad_log", "Nhật ký ải không hợp lệ.")
        last_step = s


async def save_events(db: AsyncSession, user: User, run_id: str, start_at: int, events: list) -> dict:
    """The client saves its log as it plays (from index `start_at`). A part already saved may
    be sent again (it must be the same); nothing saved can be changed or removed, so closing
    the game never lets a player take a move back."""
    row = await get_run(db, user.id, run_id)
    have = list(row.events or [])
    if not isinstance(start_at, int) or start_at < 0 or start_at > len(have):
        raise TdError(409, "log_gap", "Nhật ký ải bị hụt một đoạn.")
    overlap = have[start_at:start_at + len(events)]
    if events[:len(overlap)] != overlap:
        raise TdError(409, "log_conflict", "Nhật ký ải khác với đoạn đã lưu.")
    new = events[len(overlap):]
    _check_events(new, have[-1]["s"] if have else 0)
    if len(have) + len(new) > cfg()["anti_cheat"]["max_events"]:
        raise TdError(400, "too_many", "Nhật ký ải quá dài.")
    if new:
        row.events = have + new
        row.updated_at = clock.now()
    return {"saved": len(row.events)}


def drop_unlogged_questions(row: TdRun) -> None:
    """Before a run continues: a question asked after the last save was never applied, so it
    is forgotten."""
    used = {ev.get("q") for ev in row.events or [] if isinstance(ev, dict)}
    row.questions = {sid: q for sid, q in (row.questions or {}).items() if sid in used}


async def cancel(db: AsyncSession, user: User) -> dict:
    res = await db.execute(delete(TdRun).where(TdRun.user_id == user.id, _ours()))
    return {"cancelled": bool(res.rowcount)}


def answers(run: TdRun) -> dict:
    """Results the replay may use. A question never answered counts as wrong. An answer
    carries the `power` its tier gives the tower it placed or upgraded."""
    return {sid: {"kind": q["kind"], "word": q["word"], "ok": bool(q["ok"]),
                  **({"power": q["power"]} if "power" in q else {})}
            for sid, q in (run.questions or {}).items()}


async def verify(db: AsyncSession, user: User, run_id: str, events: list, claim: dict) -> tuple[td_sim.Sim, dict, str]:
    """Replay a finished run's log with the server's own answers and check it against the
    claim, the saved log and real time. A run that fails any check is deleted and nothing is
    earned; a run that passes is deleted too (it is over) and (sim, summary, level id) comes
    back for the caller to pay out."""
    run = await get_run(db, user.id, run_id)
    if run.id in _finishing:
        raise TdError(409, "busy", "Đang kiểm tra lượt này.")
    c = cfg()["anti_cheat"]
    saved = list(run.events or [])
    if not isinstance(events, list) or events[:len(saved)] != saved:
        await _drop(db, run)
        raise TdError(400, "bad_log", "Nhật ký ải khác với đoạn đã lưu, máy chủ không chấp nhận.")
    _finishing.add(run.id)
    try:
        sim = await asyncio.to_thread(td_sim.replay, run.params, answers(run), events, c["max_events"])
    except td_sim.LogError as e:
        await _drop(db, run)
        raise TdError(400, "bad_log", f"Nhật ký ải không hợp lệ ({e}), máy chủ không chấp nhận.")
    finally:
        _finishing.discard(run.id)
    questions, level_id, started = dict(run.questions or {}), run.level_id, run.started_at
    if set(questions) - sim.used_q:
        await _drop(db, run)
        raise TdError(400, "bad_log", "Nhật ký ải bỏ sót câu hỏi đã trả lời, máy chủ không chấp nhận.")
    got = sim.summary()
    if not isinstance(claim, dict) or any(claim.get(k) != got[k] for k in ("result", "core_hp", "wave", "steps")):
        await _drop(db, run)
        raise TdError(400, "log_mismatch", "Kết quả gửi lên không khớp khi máy chủ chơi lại nhật ký ải.")
    played = (clock.now() - started).total_seconds()
    needed = sim.step_n * td_sim.STEP_MS / 1000 / c["max_speed"]
    if played < needed * c["time_slack"] - c["time_grace_s"]:
        await _drop(db, run)
        raise TdError(400, "too_fast", "Ải kết thúc nhanh hơn thời gian thật, máy chủ không chấp nhận.")
    if got["result"] not in (td_sim.WON, td_sim.LOST):
        await _drop(db, run)
        raise TdError(400, "unfinished", "Ải chưa kết thúc.")
    await db.delete(run)
    return sim, got, level_id


async def record_monsters(db: AsyncSession, user_id: int, sim: td_sim.Sim) -> None:
    """Mặc Quái met on the board go into the Yêu Quái Phổ (entries "td_<kind>")."""
    now = clock.now()
    for kind in sim.met:
        eid = "td_" + kind
        e = await db.get(CodexEntry, (user_id, "monster", eid))
        if e is None:
            e = CodexEntry(user_id=user_id, codex="monster", entry_id=eid, discovered_at=now, progress={"kills": 0})
            db.add(e)
        e.progress = {**(e.progress or {}), "kills": int((e.progress or {}).get("kills", 0)) + sim.killed.get(kind, 0)}
    await db.flush()


# ------------------------------------------------------------------ payouts
async def grant(db: AsyncSession, user: User, reward: dict, ref: str) -> dict:
    got: dict = {}
    for cur in ("spirit_stones", "immortal_jade"):
        if reward.get(cur):
            await inventory.change_currency(db, user.id, cur, reward[cur], "td_reward", ref)
            got[cur] = got.get(cur, 0) + reward[cur]
    if reward.get("items"):
        got["items"] = await items.grant_items(db, user.id, [{"item": k, "qty": v} for k, v in reward["items"].items()],
                                               "td_reward", ref)
    return got


def merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if k in ("spirit_stones", "immortal_jade"):
            out[k] = out.get(k, 0) + v
        elif k == "items":
            out["items"] = out.get("items", []) + v
        else:
            out[k] = v
    return out
