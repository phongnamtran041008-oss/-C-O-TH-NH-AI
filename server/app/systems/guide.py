"""Lộ Trình Tu Tiên: the newbie guide and roadmap board (data/guide.json).

The board is chapters of steps. Every step says what to do and how (keys, buttons), shows
its progress and pays a small reward once; a chapter may pay a bonus once all of its required
steps are done. The rules:

  * **Everything is derived.** A step's progress is read from what the database already
    records - math answers, sittings, passed Thiên kiếp nhỏ, the player's place on Đạo Thụ,
    dungeon runs, thủ thành stars, the cơ duyên log, exercises solved, the character's
    realm. No other system calls into this one. The only facts the client declares are a
    handful of "seen" keys (the welcome dialog was read, a panel was opened).
  * **Steps are never locked.** An old save may find many steps already done and claim them
    all at once. A step is `active` (check not met), `done` (met, reward waiting) or
    `claimed`. A chapter is `active`, `done` (every required step done or claimed, bonus
    waiting) or `claimed`; a chapter without a bonus goes straight from active to claimed.
  * **Optional steps** never block the chapter bonus or the "next thing to do" (`current`),
    but they can still be claimed.
  * **Generated chapters** (`"generated": "tree_stages"`) hold one step per stage of a realm
    of Đạo Thụ: step k (`<chapter id>_s<k>`) is done when the stage reached on the tree
    (math_tree_progress.TreeState.stage) is at least k. Its progress counts the main-path
    nodes of stages 1..k that have content (vacant ones are left out of both numbers, R3)
    and it lists the main-path nodes of exactly stage k.
  * **Paying once.** Per-player state is `users.flags["guide"] = {"claimed": [...], "seen":
    [...]}`. It is written with a compare-and-swap on the whole flags column (`_swap`): the
    UPDATE only applies when the column still holds the text that was read, so of two
    concurrent claims of one step only the first can mark it, and the second re-reads and
    is refused - on SQLite (writes are serialised) and on PostgreSQL (the second UPDATE
    waits for the first to commit, then re-checks its WHERE) alike. Every claim also leaves a
    marker row in `audit_log` (reason "guide", ref = the id), checked before paying, so even
    a later lost update of the flags column by another system cannot pay a step twice.

`GET /guide` is read by the client HUD often, so a view costs one TreeState plus a few
count queries, each run only when a check of that type is on the board.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from sqlalchemy import Text, cast, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import set_committed_value

from .. import clock
from ..config import DATA_DIR
from ..learning import math_problems, math_tree
from ..models import (AuditLog, Character, MathAnswer, MathDungeonRun, MathRetry, MathRun, MathSubmission,
                      TdProgress, User)
from . import catalog, inventory, items
from . import math_tree_progress as tp

FILE = DATA_DIR / "guide.json"
FLAG = "guide"
REASON = "guide"
ACTIVE, DONE, CLAIMED = "active", "done", "claimed"
GOTO = ("math", "library", "dungeon", "td", "fortune", "char")
SEEN_KEYS = ("welcome", "board", "math_hub", "library_doc", "village")
ALWAYS_SEEN = ("welcome", "board")           # accepted by POST /guide/seen even when no check uses them
GENERATED = ("tree_stages",)
CURRENCIES = ("spirit_stones", "immortal_jade")
REWARD_KEYS = ("spirit_stones", "immortal_jade", "xp", "items")
ID_RE = re.compile(r"^[a-z0-9_]{1,40}$")
CJK_START = 0x2E80
SWAP_TRIES = 5

# the longest text the board can lay out (characters)
LIMITS = {"chapter_title": 24, "chapter_intro": 120, "step_title": 28, "step_desc": 140, "how_line": 90,
          "welcome_line": 150, "handbook_title": 28, "handbook_line": 110}
HOW_LINES = (1, 3)
WELCOME_LINES = (3, 6)
HANDBOOK_LINES = (1, 12)

# check type -> (required params, optional params)
CHECKS: dict[str, tuple[frozenset, frozenset]] = {
    "seen": (frozenset({"key"}), frozenset()),
    "math_answers": (frozenset({"count"}), frozenset({"correct"})),
    "practice_runs": (frozenset({"count"}), frozenset()),
    "trials_passed": (frozenset({"count"}), frozenset()),
    "nodes_done": (frozenset({"count"}), frozenset({"branch"})),
    "node_done": (frozenset({"node"}), frozenset()),
    "tree_stage": (frozenset({"realm", "stage"}), frozenset()),
    "placement_done": (frozenset({"count"}), frozenset()),
    "mistakes_cleared": (frozenset({"count"}), frozenset()),
    "dungeon_cleared": (frozenset({"count"}), frozenset()),
    "td_wins": (frozenset({"count"}), frozenset()),
    "fortune_won": (frozenset({"count"}), frozenset()),
    "code_solved": (frozenset({"count"}), frozenset()),
    "skills_unlocked": (frozenset({"count"}), frozenset()),
    "realm": (frozenset({"target"}), frozenset()),
    "linh_can": (frozenset(), frozenset()),          # the first test at the Trắc Linh Thạch is done
}
STEP_KEYS = {"id", "title_vi", "desc_vi", "how_vi", "check", "goto", "help", "optional", "rewards"}
TEMPLATE_KEYS = {"title_vi", "desc_vi", "how_vi", "goto", "help"}
CHAPTER_KEYS = {"id", "title_vi", "intro_vi", "rewards", "steps"}
GENERATED_KEYS = {"id", "title_vi", "intro_vi", "rewards", "generated", "realm", "step", "stage_rewards"}


class GuideError(Exception):
    def __init__(self, status: int, code: str, message_vi: str):
        super().__init__(message_vi)
        self.status, self.code, self.message_vi = status, code, message_vi


# ------------------------------------------------------------------ the data
def _read() -> dict:
    return json.loads(FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    """guide.json without its comments. validate() checks it in the tests and in
    tools/check_guide.py / tools/check_all.py, so the game itself trusts it."""
    return {k: v for k, v in _read().items() if not k.startswith("_")}


def _int(v, lo: int | None = None) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and (lo is None or v >= lo)


def _text(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _fill(text: str, stage: int) -> str:
    return text.replace("{stage}", str(stage))


def _known(raw: dict) -> set:
    return {k for k in raw if not str(k).startswith("_")}


def _check_text(out: list, where: str, v, limit: int | None) -> None:
    if not _text(v):
        out.append(f"{where} must be a non-empty string")
        return
    if limit is not None and len(v) > limit:
        out.append(f"{where} is {len(v)} characters, at most {limit}: {v!r}")
    if any(ord(ch) >= CJK_START for ch in v):
        out.append(f"{where} has a Hanzi (or other CJK) character: {v!r}")


def _check_lines(out: list, where: str, v, n: tuple[int, int], limit: int) -> None:
    if not isinstance(v, list) or not (n[0] <= len(v) <= n[1]):
        out.append(f"{where} must be a list of {n[0]}-{n[1]} lines")
        return
    for i, line in enumerate(v):
        _check_text(out, f"{where}[{i}]", line, limit)


def _check_rewards(out: list, where: str, r, required: bool = True) -> None:
    if r is None and not required:
        return
    if not isinstance(r, dict) or not r:
        out.append(f"{where} must be a non-empty object")
        return
    for k in r:
        if k not in REWARD_KEYS:
            out.append(f"{where}: unknown reward {k!r} (allowed: {', '.join(REWARD_KEYS)})")
    for k in ("spirit_stones", "immortal_jade", "xp"):
        if k in r and not _int(r[k], 1):
            out.append(f"{where}.{k} must be a whole number >= 1")
    if "items" in r:
        if not isinstance(r["items"], list) or not r["items"]:
            out.append(f"{where}.items must be a non-empty list")
        else:
            for it in r["items"]:
                if (not isinstance(it, dict) or set(it) != {"item", "qty"}
                        or catalog.stack_item(str(it.get("item", ""))) is None or not _int(it.get("qty"), 1)):
                    out.append(f"{where}.items: {it!r} must be {{item: an existing stackable item, qty >= 1}}")


def _check_check(out: list, where: str, c, seen_ok: set, t: math_tree.Tree) -> None:
    if not isinstance(c, dict) or c.get("type") not in CHECKS:
        out.append(f"{where}: check type must be one of {', '.join(CHECKS)}")
        return
    need, may = CHECKS[c["type"]]
    params = set(c) - {"type"}
    for p in sorted(need - params):
        out.append(f"{where}: check {c['type']} needs {p!r}")
    for p in sorted(params - need - may):
        out.append(f"{where}: check {c['type']} does not take {p!r}")
    if "count" in c and not _int(c["count"], 1):
        out.append(f"{where}: count must be a whole number >= 1")
    kind = c["type"]
    if kind == "seen" and c.get("key") not in seen_ok:
        out.append(f"{where}: seen key {c.get('key')!r} is not one the client sends ({', '.join(SEEN_KEYS)})")
    if kind == "math_answers" and "correct" in c and not isinstance(c["correct"], bool):
        out.append(f"{where}: correct must be true or false")
    if kind == "nodes_done" and "branch" in c and c["branch"] not in {b["id"] for b in t.raw.get("branches", [])}:
        out.append(f"{where}: {c['branch']!r} is not a branch of Đạo Thụ")
    if kind == "node_done" and c.get("node") not in t.nodes:
        out.append(f"{where}: {c.get('node')!r} is not a node of Đạo Thụ")
    if kind == "tree_stage":
        if c.get("realm") not in t.realm_stages:
            out.append(f"{where}: {c.get('realm')!r} is not a realm of Đạo Thụ")
        elif not _int(c.get("stage"), 1) or c["stage"] > t.realm_stages[c["realm"]]:
            out.append(f"{where}: stage must be 1..{t.realm_stages[c['realm']]}")
    if kind == "fortune_won" and c.get("count") != 1:
        out.append(f"{where}: fortune_won only knows whether one cơ duyên was won (count must be 1)")
    if kind == "realm" and c.get("target") not in [r["id"] for r in catalog.realms()]:
        out.append(f"{where}: {c.get('target')!r} is not a cultivation realm")


def _check_step_texts(out: list, where: str, s: dict, help_ids: set, stage: int | None = None) -> None:
    fill = (lambda v: _fill(v, stage) if isinstance(v, str) else v) if stage else (lambda v: v)
    _check_text(out, f"{where}.title_vi", fill(s.get("title_vi")), LIMITS["step_title"])
    _check_text(out, f"{where}.desc_vi", fill(s.get("desc_vi")), LIMITS["step_desc"])
    how = s.get("how_vi")
    _check_lines(out, f"{where}.how_vi", [fill(x) for x in how] if isinstance(how, list) else how,
                 HOW_LINES, LIMITS["how_line"])
    if s.get("goto") is not None and s["goto"] not in GOTO:
        out.append(f"{where}: goto {s['goto']!r} is not one of {', '.join(GOTO)}")
    if s.get("help") is not None and s["help"] not in help_ids:
        out.append(f"{where}: help {s['help']!r} is not a handbook page")


def validate(raw: dict | None = None) -> list[str]:
    """One readable line per problem in guide.json; empty when it is sound."""
    raw = _read() if raw is None else raw
    out: list[str] = []
    if not isinstance(raw, dict):
        return ["guide.json must be an object"]
    t = math_tree.tree()
    if raw.get("version") != 1:
        out.append("version must be 1")
    _check_text(out, "title_vi", raw.get("title_vi"), None)
    w = raw.get("welcome")
    if not isinstance(w, dict):
        out.append("welcome must be {speaker_vi, lines_vi}")
    else:
        _check_text(out, "welcome.speaker_vi", w.get("speaker_vi"), None)
        _check_lines(out, "welcome.lines_vi", w.get("lines_vi"), WELCOME_LINES, LIMITS["welcome_line"])

    help_ids: set[str] = set()
    pages = raw.get("handbook")
    if not isinstance(pages, list) or not pages:
        out.append("handbook must be a non-empty list of pages")
        pages = []
    for i, p in enumerate(pages):
        here = f"handbook[{i}]"
        if not isinstance(p, dict):
            out.append(f"{here} must be an object")
            continue
        if not isinstance(p.get("id"), str) or not ID_RE.match(p["id"]):
            out.append(f"{here}: id must be [a-z0-9_], 1-40 characters")
        elif p["id"] in help_ids:
            out.append(f"{here}: duplicate handbook id {p['id']!r}")
        else:
            help_ids.add(p["id"])
        _check_text(out, f"{here}.title_vi", p.get("title_vi"), LIMITS["handbook_title"])
        _check_lines(out, f"{here}.lines_vi", p.get("lines_vi"), HANDBOOK_LINES, LIMITS["handbook_line"])

    chapters = raw.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        return out + ["chapters must be a non-empty list"]
    ids: set[str] = set()

    def take(where: str, i) -> None:
        if not isinstance(i, str) or not ID_RE.match(i):
            out.append(f"{where}: id {i!r} must be [a-z0-9_], 1-40 characters")
        elif i in ids:
            out.append(f"{where}: duplicate id {i!r} (ids are unique among chapters and steps)")
        else:
            ids.add(i)

    seen_ok = set(SEEN_KEYS)
    for ci, ch in enumerate(chapters):
        if not isinstance(ch, dict):
            out.append(f"chapters[{ci}] must be an object")
            continue
        here = f"chapter {ch.get('id', ci)}"
        take(here, ch.get("id"))
        _check_text(out, f"{here}.title_vi", ch.get("title_vi"), LIMITS["chapter_title"])
        _check_text(out, f"{here}.intro_vi", ch.get("intro_vi"), LIMITS["chapter_intro"])
        _check_rewards(out, f"{here}.rewards", ch.get("rewards"), required=False)
        if "generated" in ch:
            for k in sorted(_known(ch) - GENERATED_KEYS):
                out.append(f"{here}: unknown key {k!r} for a generated chapter")
            if ch["generated"] not in GENERATED:
                out.append(f"{here}: generated must be one of {', '.join(GENERATED)}")
                continue
            realm = ch.get("realm")
            if realm not in t.realm_stages:
                out.append(f"{here}: realm {realm!r} is not a realm of Đạo Thụ")
                continue
            stages = t.realm_stages[realm]
            tpl = ch.get("step")
            if not isinstance(tpl, dict):
                out.append(f"{here}: step must be the template {{title_vi, desc_vi, how_vi, goto?, help?}}")
            else:
                for k in sorted(_known(tpl) - TEMPLATE_KEYS):
                    out.append(f"{here}.step: unknown key {k!r}")
                for k in range(1, stages + 1):
                    _check_step_texts(out, f"{here}.step (stage {k})", tpl, help_ids, stage=k)
            rewards = ch.get("stage_rewards")
            if not isinstance(rewards, list) or len(rewards) != stages:
                out.append(f"{here}: stage_rewards must hold one reward per stage of {realm} ({stages})")
            else:
                for k, r in enumerate(rewards, 1):
                    _check_rewards(out, f"{here}.stage_rewards[{k - 1}]", r)
            for k in range(1, stages + 1):
                take(f"{here} (generated step {k})", f"{ch.get('id')}_s{k}")
            continue
        for k in sorted(_known(ch) - CHAPTER_KEYS):
            out.append(f"{here}: unknown key {k!r}")
        steps = ch.get("steps")
        if not isinstance(steps, list) or not steps:
            out.append(f"{here}: steps must be a non-empty list")
            continue
        if ch.get("rewards") and all(isinstance(s, dict) and s.get("optional") for s in steps):
            out.append(f"{here}: a chapter bonus needs at least one required step")
        for si, s in enumerate(steps):
            if not isinstance(s, dict):
                out.append(f"{here}.steps[{si}] must be an object")
                continue
            sh = f"step {s.get('id', f'{here}[{si}]')}"
            take(sh, s.get("id"))
            for k in sorted(_known(s) - STEP_KEYS):
                out.append(f"{sh}: unknown key {k!r}")
            _check_step_texts(out, sh, s, help_ids)
            _check_check(out, sh, s.get("check"), seen_ok, t)
            if "optional" in s and not isinstance(s["optional"], bool):
                out.append(f"{sh}: optional must be true or false")
            _check_rewards(out, f"{sh}.rewards", s.get("rewards"))
    return out


def seen_keys() -> set[str]:
    """The keys POST /guide/seen accepts: welcome, board and every key a seen check uses."""
    keys = set(ALWAYS_SEEN)
    for ch in data()["chapters"]:
        for s in ch.get("steps", []):
            if s["check"]["type"] == "seen":
                keys.add(s["check"]["key"])
    return keys


# ------------------------------------------------------------------ the board, unrolled
def chapters() -> list[dict]:
    """Every chapter with its steps as the board shows them: a generated chapter gets one
    step per stage of its realm (`<chapter id>_s<k>`, a tree_stage check, its stage's
    reward). Pure: no player in it."""
    t = math_tree.tree()
    out = []
    for ch in data()["chapters"]:
        steps = []
        if ch.get("generated") == "tree_stages":
            tpl, realm = ch["step"], ch["realm"]
            for k in range(1, t.realm_stages[realm] + 1):
                steps.append({"id": f"{ch['id']}_s{k}", "title_vi": _fill(tpl["title_vi"], k),
                              "desc_vi": _fill(tpl["desc_vi"], k), "how_vi": [_fill(x, k) for x in tpl["how_vi"]],
                              "goto": tpl.get("goto"), "help": tpl.get("help"), "optional": False,
                              "check": {"type": "tree_stage", "realm": realm, "stage": k},
                              "rewards": ch["stage_rewards"][k - 1], "stage": (realm, k)})
        else:
            for s in ch["steps"]:
                steps.append({**s, "goto": s.get("goto"), "help": s.get("help"),
                              "optional": bool(s.get("optional", False)), "stage": None})
        out.append({"id": ch["id"], "title_vi": ch["title_vi"], "intro_vi": ch["intro_vi"],
                    "rewards": ch.get("rewards") or {}, "steps": steps})
    return out


def rewards_vi(rw: dict) -> list[str]:
    """The same wording as the quest board."""
    out = []
    if rw.get("spirit_stones"):
        out.append(f"{rw['spirit_stones']} Linh Thạch")
    if rw.get("immortal_jade"):
        out.append(f"{rw['immortal_jade']} Tiên Ngọc")
    if rw.get("xp"):
        out.append(f"{rw['xp']} Tu Vi")
    for it in rw.get("items", []):
        out.append(f"{catalog.item_name(it['item'])} ×{it['qty']}")
    return out


def _guide(flags: dict | None) -> dict:
    g = (flags or {}).get(FLAG) or {}
    return {"claimed": list(g.get("claimed") or []), "seen": list(g.get("seen") or [])}


# ------------------------------------------------------------------ what the database says
class Facts:
    """Answers the checks for one player in one request. TreeState is read once; every
    count query runs at most once, and only when a check needs it."""

    def __init__(self, db: AsyncSession, user_id: int, st: tp.TreeState, flags: dict | None):
        self.db, self.user_id, self.st, self.flags = db, user_id, st, flags or {}
        self.seen = set(_guide(flags)["seen"])
        self._memo: dict = {}

    async def _scalar(self, key, query) -> int:
        if key not in self._memo:
            self._memo[key] = int((await self.db.execute(query)).scalar() or 0)
        return self._memo[key]

    async def count(self, c: dict) -> int:
        """The raw number a counting check reads (not capped)."""
        uid, st, kind = self.user_id, self.st, c["type"]
        if kind == "math_answers":
            q = select(func.count()).select_from(MathAnswer).where(MathAnswer.user_id == uid)
            if c.get("correct"):
                q = q.where(MathAnswer.correct.is_(True))
            return await self._scalar((kind, bool(c.get("correct"))), q)
        if kind == "practice_runs":       # a sitting with at least one answered question
            return await self._scalar(kind, select(func.count()).select_from(MathRun).where(
                MathRun.user_id == uid, MathRun.mode == "practice", MathRun.asked > 0))
        if kind == "trials_passed":       # parts passed by their own trial, plus whole floors of old saves
            old = sum(len(floors - st.placement.get(s, set())) for s, floors in st.legacy.items())
            return len(st.passed_parts) + old
        if kind == "nodes_done":
            branch = c.get("branch")
            return sum(1 for n, s in st.status.items()
                       if s == tp.DONE and (branch is None or st.tree.nodes[n].branch == branch))
        if kind == "placement_done":      # finished with an outcome; an abandoned sitting has passed false
            return await self._scalar(kind, select(func.count()).select_from(MathRun).where(
                MathRun.user_id == uid, MathRun.mode == "placement", MathRun.ended_at.is_not(None),
                MathRun.passed.is_(True)))
        if kind == "mistakes_cleared":
            return await self._scalar(kind, select(func.count()).select_from(MathRetry).where(
                MathRetry.user_id == uid, MathRetry.cleared_at.is_not(None)))
        if kind == "dungeon_cleared":
            return await self._scalar(kind, select(func.count()).select_from(MathDungeonRun).where(
                MathDungeonRun.user_id == uid, MathDungeonRun.state == "cleared"))
        if kind == "td_wins":
            from . import math_td
            return await self._scalar(kind, select(func.count()).select_from(TdProgress).where(
                TdProgress.user_id == uid, TdProgress.stars >= 1,
                TdProgress.level_id.in_(list(math_td.levels()))))
        if kind == "fortune_won":
            return await self._fortune_won()
        if kind == "code_solved":
            return await self._scalar(kind, select(func.count(func.distinct(MathSubmission.problem_id))).where(
                MathSubmission.user_id == uid, MathSubmission.judged_at.is_not(None),
                MathSubmission.total > 0, MathSubmission.passed >= MathSubmission.total))
        if kind == "skills_unlocked":
            from . import math_skills
            where = tp.working_position_of(st)
            return sum(1 for s in math_skills.skills().values() if math_skills.locked_reason(s, where, st) is None)
        raise KeyError(kind)

    async def _fortune_won(self) -> int:
        """Best effort: a "won" row in the cơ duyên log (it keeps only the latest few), else a
        payment the cơ duyên wrote to the ledger (a won event always pays something)."""
        log = ((self.flags.get("math_fortune") or {}).get("log")) or []
        if any(isinstance(r, dict) and r.get("outcome") == "won" for r in log):
            return 1
        return min(1, await self._scalar("fortune_won", select(func.count()).select_from(AuditLog).where(
            AuditLog.user_id == self.user_id, AuditLog.reason == "math_fortune", AuditLog.delta > 0)))

    async def progress(self, c: dict) -> tuple[int, int]:
        """(n, count) of a check, n capped at count; met when n == count."""
        st, kind = self.st, c["type"]
        if kind == "seen":
            return int(c["key"] in self.seen), 1
        if kind == "node_done":           # vacant nodes count as done for the tree, not here
            return int(st.status.get(c["node"]) == tp.DONE), 1
        if kind == "realm":
            from .cultivation import order
            if "realm" not in self._memo:
                ch = await self.db.get(Character, self.user_id)
                self._memo["realm"] = ch.realm if ch is not None else None
            have, ids = self._memo["realm"], order()
            return int(have in ids and c["target"] in ids and ids.index(have) >= ids.index(c["target"])), 1
        if kind == "tree_stage":
            return self._tree_stage(c["realm"], c["stage"])
        if kind == "linh_can":
            from ..models import LinhCan
            row = await self.db.get(LinhCan, self.user_id)
            return int(row is not None and row.root_id is not None), 1
        n = await self.count(c)
        return min(n, c["count"]), c["count"]

    def _tree_stage(self, realm: str, stage: int) -> tuple[int, int]:
        st, t = self.st, self.st.tree
        order = t.realm_order
        mains = [n for n in t.main_nodes() if st.status[n.id] != tp.VACANT and (
            order[n.realm] < order[realm] or (n.realm == realm and (n.stage or 0) <= stage))]
        reached = t.reaches(realm, stage, st.stage)
        total = len(mains)
        if total == 0:
            return int(reached), 1
        if reached:
            return total, total
        return min(sum(1 for n in mains if st.status[n.id] == tp.DONE), total - 1), total


# ------------------------------------------------------------------ the view
def _branch_names(t: math_tree.Tree) -> dict[str, str]:
    return {b["id"]: b["name_vi"] for b in t.raw.get("branches", [])}


def _stage_nodes(st: tp.TreeState, realm: str, stage: int) -> list[dict]:
    t = st.tree
    names = _branch_names(t)
    nodes = sorted((n for n in t.main_nodes(realm) if n.stage == stage), key=tp.node_order)
    return [{"id": n.id, "name_vi": n.name_vi, "branch": n.branch, "branch_vi": names.get(n.branch, n.branch),
             "state": st.status[n.id]} for n in nodes]


async def _study(db: AsyncSession, user_id: int, st: tp.TreeState) -> dict | None:
    """What to learn on Đạo Thụ right now: the sitting left open; else the first open
    main-path node, its first part not passed (the trial when the part's mastery gate is
    open); a node whose parts are all passed or that has only exercises: the exercises."""
    from . import math_practice
    t = st.tree
    names = _branch_names(t)
    run = await math_practice.open_run(db, user_id)
    if run is not None:
        node = t.nodes.get(run.node_id) if run.node_id else None
        name = node.name_vi if node else _subject_name(run.subject_id)
        what = "Thiên kiếp nhỏ" if run.mode == math_practice.TRIAL else "Buổi luyện"
        return {"action": "resume", "node_id": run.node_id, "name_vi": name,
                "branch_vi": names.get(node.branch) if node else None, "floor": run.floor,
                "text_vi": f"{what} ở nút «{name}» còn dở: vào Đạo Thụ để làm tiếp"}
    for nid in st.open:
        node = t.nodes[nid]
        if not node.main:
            continue
        base = {"node_id": node.id, "name_vi": node.name_vi, "branch_vi": names.get(node.branch, node.branch)}
        part = next((p for p in tp.parts(node) if st.has_questions(p) and not st.part_passed(p)), None)
        if part is not None:
            gate = await math_practice.part_gate(db, user_id, part)
            if gate.ok:
                return {"action": "trial", **base, "floor": part.floor,
                        "text_vi": f"Nút «{node.name_vi}» đã đủ thuần thục: vượt Thiên kiếp nhỏ"}
            return {"action": "practice", **base, "floor": part.floor,
                    "text_vi": f"Học nút «{node.name_vi}»: luyện cho tới khi mở Thiên kiếp nhỏ"}
        todo = [p for p in node.problems if tp.problem_available(p) and p not in st.solved]
        floor = math_problems.bank()[todo[0]].floor if todo else None
        return {"action": "code", **base, "floor": floor,
                "text_vi": f"Nút «{node.name_vi}»: giải các bài tập lập trình của nút"}
    return None


def _subject_name(subject_id: str) -> str:
    from ..learning import math_path
    try:
        return math_path.subject(subject_id).name_vi
    except KeyError:
        return subject_id


async def _board(db: AsyncSession, user: User, flags: dict | None, st: tp.TreeState | None = None) -> dict:
    """The whole board for this player, with the raw rewards kept beside each entry
    (`_rewards`) for claim(); view() strips those."""
    st = st if st is not None else await tp.state(db, user.id)
    g = _guide(flags)
    claimed = set(g["claimed"])
    facts = Facts(db, user.id, st, flags)
    out_chapters, current, claimable = [], None, 0
    for ch in chapters():
        steps = []
        for s in ch["steps"]:
            n, count = await facts.progress(s["check"])
            state = CLAIMED if s["id"] in claimed else DONE if n >= count else ACTIVE
            claimable += state == DONE
            steps.append({"id": s["id"], "chapter_id": ch["id"], "title_vi": s["title_vi"], "desc_vi": s["desc_vi"],
                          "how_vi": list(s["how_vi"]), "goto": s["goto"], "help": s["help"],
                          "optional": s["optional"], "state": state, "progress": n, "count": count,
                          "rewards_vi": rewards_vi(s["rewards"]),
                          "nodes": _stage_nodes(st, *s["stage"]) if s["stage"] else [],
                          "_rewards": s["rewards"]})
            if current is None and not s["optional"] and state == ACTIVE:
                current = {"chapter_id": ch["id"], "step_id": s["id"], "title_vi": s["title_vi"],
                           "hint_vi": s["how_vi"][0], "progress": n, "count": count, "goto": s["goto"]}
        required = [s for s in steps if not s["optional"]]
        done = sum(1 for s in required if s["state"] != ACTIVE)
        complete = done == len(required)
        if ch["id"] in claimed or (complete and not ch["rewards"]):
            state = CLAIMED
        else:
            state = DONE if complete else ACTIVE
        claimable += state == DONE
        out_chapters.append({"id": ch["id"], "title_vi": ch["title_vi"], "intro_vi": ch["intro_vi"],
                             "done": done, "total": len(required), "state": state,
                             "rewards_vi": rewards_vi(ch["rewards"]), "steps": steps, "_rewards": ch["rewards"]})
    d = data()
    return {"title_vi": d["title_vi"],
            "welcome": {"seen": "welcome" in g["seen"], "speaker_vi": d["welcome"]["speaker_vi"],
                        "lines_vi": list(d["welcome"]["lines_vi"])},
            "chapters": out_chapters, "current": current, "claimable": claimable,
            "study": await _study(db, user.id, st), "stage": tp.stage_view(st),
            "handbook": [{"id": p["id"], "title_vi": p["title_vi"], "lines_vi": list(p["lines_vi"])}
                         for p in d["handbook"]]}


def _public(board: dict) -> dict:
    for ch in board["chapters"]:
        ch.pop("_rewards", None)
        for s in ch["steps"]:
            s.pop("_rewards", None)
    return board


async def view(db: AsyncSession, user: User) -> dict:
    """GET /guide."""
    return _public(await _board(db, user, user.flags))


# ------------------------------------------------------------------ writing the state
async def _read_flags(db: AsyncSession, user_id: int) -> tuple[str | None, dict]:
    """The flags column as stored (the text the swap compares against) and parsed."""
    raw = (await db.execute(select(cast(User.flags, Text)).where(User.id == user_id))).scalar_one()
    flags = json.loads(raw) if raw else {}
    return raw, flags if isinstance(flags, dict) else {}


async def _swap(db: AsyncSession, user: User, change) -> dict:
    """Read users.flags, let `change(guide)` return the new guide state (or None for no
    change; it may raise), and write it only if the column still holds what was read - a
    compare-and-swap, retried when another request changed the flags in between. Returns
    the flags now stored."""
    for _ in range(SWAP_TRIES):
        raw, flags = await _read_flags(db, user.id)
        new_guide = change(_guide(flags))
        if new_guide is None:
            set_committed_value(user, "flags", flags)
            return flags
        new = {**flags, FLAG: new_guide}
        same = User.flags.is_(None) if raw is None else cast(User.flags, Text) == raw
        res = await db.execute(update(User).where(User.id == user.id, same).values(flags=new)
                               .execution_options(synchronize_session=False))
        if res.rowcount == 1:
            set_committed_value(user, "flags", new)
            return new
    raise GuideError(409, "busy", "Lộ Trình đang bận, con thử lại nhé.")


async def seen(db: AsyncSession, user: User, key: str) -> dict:
    """POST /guide/seen: the client declares a fact only it knows. Idempotent."""
    if key not in seen_keys():
        raise GuideError(400, "bad_key", "Không có việc này trong Lộ Trình.")

    def add(g: dict) -> dict | None:
        return None if key in g["seen"] else {**g, "seen": g["seen"] + [key]}
    flags = await _swap(db, user, add)
    return {"guide": _public(await _board(db, user, flags))}


async def claim(db: AsyncSession, user: User, target: str) -> dict:
    """POST /guide/claim: the reward of a done step, or the bonus of a done chapter, once."""
    known = {c["id"] for c in chapters()} | {s["id"] for c in chapters() for s in c["steps"]}
    if target not in known:
        raise GuideError(404, "no_step", "Không có bước này trong Lộ Trình.")
    marker = (await db.execute(select(AuditLog.id).where(
        AuditLog.user_id == user.id, AuditLog.reason == REASON, AuditLog.ref_id == target).limit(1))).first()
    _, flags = await _read_flags(db, user.id)
    st = await tp.state(db, user.id)
    board = await _board(db, user, flags, st)
    entry = next((c for c in board["chapters"] if c["id"] == target), None) or \
        next(s for c in board["chapters"] for s in c["steps"] if s["id"] == target)
    if entry["state"] == CLAIMED or marker is not None:
        raise GuideError(400, "already_claimed", "Con đã nhận phần thưởng này rồi.")
    if entry["state"] != DONE:
        raise GuideError(400, "not_done", "Bước này chưa xong." if "chapter_id" in entry
                         else "Chương này còn bước chưa xong.")

    def mark(g: dict) -> dict:
        if target in g["claimed"]:
            raise GuideError(400, "already_claimed", "Con đã nhận phần thưởng này rồi.")
        return {**g, "claimed": g["claimed"] + [target]}
    flags = await _swap(db, user, mark)

    rw = entry["_rewards"]
    got: dict = {"items": [], "equipment": []}
    for cur in CURRENCIES:
        if rw.get(cur):
            got[cur] = await inventory.change_currency(db, user.id, cur, rw[cur], REASON, target)
    got["items"] = await items.grant_items(db, user.id, rw.get("items", []), REASON, target)
    if rw.get("xp"):
        from . import cultivation
        got["xp"] = await cultivation.add_xp(db, user.id, rw["xp"], REASON)
    db.add(AuditLog(user_id=user.id, currency_or_item="guide", delta=0, balance_after=None, reason=REASON,
                    ref_id=target, created_at=clock.now()))
    await db.flush()
    if any(rw.get(cur) for cur in CURRENCIES):
        await db.refresh(user, list(CURRENCIES))
    return {"claimed": target, "rewards": got, "guide": _public(await _board(db, user, flags, st))}
