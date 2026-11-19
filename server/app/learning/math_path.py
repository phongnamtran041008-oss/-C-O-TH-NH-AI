"""Learning path of the math game (plan section 3): subject -> floor -> micro-skill -> tier.

A *subject* is one math bí cảnh (Đại Số Tuyến Tính, Giải Tích, ...). The code says
"subject" because "realm" already means cảnh giới and "secret realm" already means the
party dungeon. A subject has floors 1..9 plus an optional hidden floor 10; a floor has
3-6 micro-skills; a micro-skill lists the micro-skills that must be mastered before it.

Pure data and rules: no database, no pygame, nothing from the vocabulary code. Numbers
come from data/balance/math.json, floors and micro-skills from data/math/*.json.

`validate_all()` returns every problem it finds as one readable line. The tests and
tools/check_all.py fail when that list is not empty, so a broken path never ships.
"""
from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .. import balance
from ..config import DATA_DIR

MATH_DIR = DATA_DIR / "math"
TIERS = (1, 2, 3, 4, 5)
TOP_TIER = TIERS[-1]
ID_RE = re.compile(r"^[a-z][a-z0-9_]{2,39}$")      # fits the String(40) id columns
EXTENSIONS = {"ai"}                                 # additions that are not in the syllabus

_INDEX_KEYS = {"cultivation_realm", "subjects"}
_ENTRY_KEYS = {"id", "order", "name_vi", "courses", "file"}
_SUBJECT_KEYS = {"id", "floors"}
_FLOOR_KEYS = {"floor", "title_vi", "syllabus_ref", "hidden", "skills"}
_SKILL_KEYS = {"id", "name_vi", "desc_vi", "requires", "extension"}


# ------------------------------------------------------------------ config
def _clean(d: dict) -> dict:
    """A JSON object without its "_comment"-style keys."""
    return {k: v for k, v in d.items() if not k.startswith("_")}


def cfg() -> dict:
    return balance.load("math")


def floor_tiers(floor: int, config: dict | None = None) -> tuple[int, int]:
    """(lowest, highest) tier a question on this floor may have."""
    lo, hi = _clean((config or cfg())["floor_tiers"])[str(floor)]
    return lo, hi


def allowed_tiers(floor: int, config: dict | None = None) -> list[int]:
    lo, hi = floor_tiers(floor, config)
    return list(range(lo, hi + 1))


def tier_allowed(floor: int, tier: int, config: dict | None = None) -> bool:
    """False for a tier outside the floor's range, and for a floor that does not exist."""
    try:
        return tier in allowed_tiers(floor, config)
    except KeyError:
        return False


def question_types(config: dict | None = None) -> dict:
    return _clean((config or cfg())["question_types"])


def time_limit(qtype: str, tier: int, config: dict | None = None) -> int | None:
    """Seconds to answer, or None when this question type does not exist at this tier."""
    if tier not in TIERS:
        raise ValueError(f"tier must be 1..{TOP_TIER}, got {tier!r}")
    return question_types(config)[qtype]["time_limit"][tier - 1]


def xp_for_tier(tier: int, config: dict | None = None) -> int:
    """Tu Vi for one right answer at this tier."""
    if tier not in TIERS:
        raise ValueError(f"tier must be 1..{TOP_TIER}, got {tier!r}")
    return int((config or cfg())["xp_per_correct"]["by_tier"][tier - 1])


# ------------------------------------------------------------------ the path
@dataclass(frozen=True)
class MicroSkill:
    id: str
    name_vi: str
    desc_vi: str
    floor: int
    requires: tuple[str, ...] = ()
    extension: str | None = None


@dataclass(frozen=True)
class Floor:
    number: int
    title_vi: str
    hidden: bool
    skills: tuple[MicroSkill, ...]
    syllabus_ref: str = ""

    @property
    def tiers(self) -> list[int]:
        return allowed_tiers(self.number)


@dataclass(frozen=True)
class Subject:
    id: str
    name_vi: str
    order: int
    courses: tuple[str, ...]
    floors: tuple[Floor, ...]

    @property
    def main_floors(self) -> tuple[Floor, ...]:
        """The floors that count for advancing; the hidden floor never blocks anything."""
        return tuple(f for f in self.floors if not f.hidden)

    @property
    def hidden_floor(self) -> Floor | None:
        return next((f for f in self.floors if f.hidden), None)

    def floor(self, number: int) -> Floor:
        for f in self.floors:
            if f.number == number:
                return f
        raise KeyError(f"{self.id} has no floor {number}")

    @property
    def skills(self) -> dict[str, MicroSkill]:
        """Every micro-skill by id, in path order (floor, then the order in the file)."""
        return {s.id: s for f in self.floors for s in f.skills}

    def is_unlocked(self, skill_id: str, mastered: Iterable[str]) -> bool:
        """A micro-skill opens only when all of its prerequisites are mastered."""
        return set(self.skills[skill_id].requires) <= set(mastered)

    def unlocked(self, mastered: Iterable[str]) -> list[str]:
        done = set(mastered)
        return [s.id for s in self.skills.values() if set(s.requires) <= done]

    def learning_order(self) -> list[str]:
        """Every micro-skill, each one after all of its prerequisites."""
        return topological_order({s.id: list(s.requires) for s in self.skills.values()})


def _read(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def load_index(math_dir: Path = MATH_DIR) -> dict:
    return _clean(_read(math_dir / "subjects.json"))


def build_subject(entry: dict, raw: dict) -> Subject:
    floors = tuple(
        Floor(number=f["floor"], title_vi=f["title_vi"], hidden=bool(f.get("hidden", False)),
              syllabus_ref=f.get("syllabus_ref", ""),
              skills=tuple(MicroSkill(id=s["id"], name_vi=s["name_vi"], desc_vi=s["desc_vi"],
                                      floor=f["floor"], requires=tuple(s.get("requires", ())),
                                      extension=s.get("extension"))
                           for s in f["skills"]))
        for f in raw["floors"])
    return Subject(id=entry["id"], name_vi=entry["name_vi"], order=entry["order"],
                   courses=tuple(entry.get("courses", ())), floors=floors)


@lru_cache(maxsize=1)
def subjects() -> tuple[Subject, ...]:
    """The subjects that are written (have a floor file), in play order."""
    entries = [e for e in load_index()["subjects"] if e.get("file")]
    return tuple(build_subject(e, _read(MATH_DIR / e["file"]))
                 for e in sorted(entries, key=lambda e: e["order"]))


def subject(subject_id: str) -> Subject:
    for s in subjects():
        if s.id == subject_id:
            return s
    raise KeyError(f"no subject {subject_id!r}")


# ------------------------------------------------------------------ the prerequisite graph
def find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """A cycle as [a, b, ..., a] where each one requires the next, or None. Prerequisites
    that are not nodes of the graph are ignored (they are reported as unknown elsewhere)."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(graph, WHITE)
    for start in graph:
        if colour[start] != WHITE:
            continue
        colour[start] = GREY
        path = [start]
        stack = [iter(graph[start])]
        while stack:
            for nxt in stack[-1]:
                if nxt not in colour or colour[nxt] == BLACK:
                    continue
                if colour[nxt] == GREY:
                    return path[path.index(nxt):] + [nxt]
                colour[nxt] = GREY
                path.append(nxt)
                stack.append(iter(graph[nxt]))
                break
            else:
                colour[path.pop()] = BLACK
                stack.pop()
    return None


def topological_order(graph: dict[str, list[str]]) -> list[str]:
    """Nodes with every prerequisite before the node that needs it. Among the nodes that
    are ready, the one listed first goes first, so the result is the same on every run."""
    cycle = find_cycle(graph)
    if cycle:
        raise ValueError("prerequisite cycle: " + " -> ".join(cycle))
    done: set[str] = set()
    order: list[str] = []
    waiting = list(graph)
    while waiting:
        ready = next(n for n in waiting if all(r in done or r not in graph for r in graph[n]))
        waiting.remove(ready)
        done.add(ready)
        order.append(ready)
    return order


# ------------------------------------------------------------------ validation
def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _get(d, *path):
    for key in path:
        if not isinstance(d, dict) or key not in d:
            return None
        d = d[key]
    return d


def text_problem(value) -> str | None:
    """Why this cannot be shown in the game, or None. Display text is plain Latin and
    precomposed Vietnamese letters; math is written ASCII-safe (A^T, a_ij, !=), so the
    game font always has every character."""
    if not isinstance(value, str) or not value.strip():
        return "is missing or empty"
    if value != value.strip():
        return "has spaces at the start or the end"
    for ch in value:
        o = ord(ch)
        ascii_ok = 0x20 <= o <= 0x7E
        letter_ok = (0xC0 <= o <= 0x24F and o not in (0xD7, 0xF7)) or 0x1E00 <= o <= 0x1EFF
        if not (ascii_ok or letter_ok):     # no combining marks either: letters must be precomposed
            return f"has the character {ch!r} (U+{o:04X}); write math ASCII-safe, e.g. A^T, x, !="
    return None


def _unknown_keys(obj: dict, allowed: set[str]) -> list[str]:
    return sorted(k for k in obj if not k.startswith("_") and k not in allowed)


def validate_config(config: dict) -> list[str]:
    """Problems in balance/math.json."""
    errors: list[str] = []

    tiers = _get(config, "tiers")
    tiers = _clean(tiers) if isinstance(tiers, dict) else {}
    if sorted(tiers) != [str(t) for t in TIERS]:
        errors.append(f"tiers: must be exactly {', '.join(str(t) for t in TIERS)}")
    for t, info in tiers.items():
        problem = text_problem(_get(info, "name_vi"))
        if problem:
            errors.append(f"tiers[{t}].name_vi {problem}")

    main, hidden = _get(config, "main_floors"), _get(config, "hidden_floor")
    if not (_is_int(main) and main >= 1):
        errors.append("main_floors: must be a whole number >= 1")
    if not (_is_int(hidden) and _is_int(main) and hidden > main):
        errors.append("hidden_floor: must be a whole number above main_floors")
    ft = _get(config, "floor_tiers")
    ft = _clean(ft) if isinstance(ft, dict) else {}
    if _is_int(main) and _is_int(hidden):
        expected = [str(n) for n in range(1, main + 1)] + [str(hidden)]
        if sorted(ft) != sorted(expected):
            errors.append(f"floor_tiers: must have exactly the floors {', '.join(expected)}")
    below: tuple[int, int] | None = None
    for n in sorted(ft, key=lambda k: (not k.isdigit(), int(k) if k.isdigit() else 0, k)):
        rng = ft[n]
        if not (isinstance(rng, list) and len(rng) == 2 and all(_is_int(x) for x in rng)
                and TIERS[0] <= rng[0] <= rng[1] <= TOP_TIER):
            errors.append(f"floor_tiers[{n}]: must be [low, high] with 1 <= low <= high <= {TOP_TIER}")
            continue
        if below and (rng[0] < below[0] or rng[1] < below[1]):
            errors.append(f"floor_tiers[{n}]: is easier than the floor below it")
        below = (rng[0], rng[1])
        if _is_int(hidden) and n == str(hidden) and rng != [TOP_TIER, TOP_TIER]:
            errors.append(f"floor_tiers[{n}]: the hidden floor is tier {TOP_TIER} only")

    def need_int(lowest: int, *path: str) -> int | None:
        v = _get(config, *path)
        if not (_is_int(v) and v >= lowest):
            errors.append(f"{'.'.join(path)}: must be a whole number >= {lowest}")
            return None
        return v

    lo, hi = need_int(1, "skills_per_floor", "min"), need_int(1, "skills_per_floor", "max")
    if lo and hi and lo > hi:
        errors.append("skills_per_floor: min is above max")
    need_int(1, "adaptive", "up_after_correct_streak")
    need_int(1, "adaptive", "down_after_wrong_streak")
    need, window = need_int(1, "tier_unlock", "correct_at_previous_tier"), need_int(1, "tier_unlock", "window")
    if need and window and need > window:
        errors.append("tier_unlock: correct_at_previous_tier is above window, so no tier could ever open")
    xp = _get(config, "xp_per_correct", "by_tier")
    if not (isinstance(xp, list) and len(xp) == len(TIERS) and all(_is_int(v) and v >= 1 for v in xp)
            and all(a <= b for a, b in zip(xp, xp[1:]))):
        errors.append(f"xp_per_correct.by_tier: must list {len(TIERS)} whole numbers >= 1 that never go down")
    tol = _get(config, "numeric_tolerance")
    if not (isinstance(tol, (int, float)) and not isinstance(tol, bool) and 0 <= tol < 0.01):
        errors.append("numeric_tolerance: must be a number from 0 to below 0.01")
    need_int(1, "mastery_gate", "window")
    pct = _get(config, "mastery_gate", "min_correct_pct")
    if not (isinstance(pct, (int, float)) and not isinstance(pct, bool) and 0 < pct <= 100):
        errors.append("mastery_gate.min_correct_pct: must be above 0 and at most 100")
    per_skill = need_int(1, "mastery_gate", "trial", "questions_per_skill")
    wrong = need_int(0, "mastery_gate", "trial", "max_wrong")
    few = _get(config, "skills_per_floor", "min")
    if per_skill and wrong is not None and _is_int(few) and wrong >= per_skill * few:
        errors.append("mastery_gate.trial.max_wrong: a trial on the smallest floor could then be "
                      "passed with every question wrong")
    need_int(1, "anti_repeat_window")
    need_int(0, "template_cooldown")
    need_int(0, "parallel_question", "after_answers")
    need_int(1, "parallel_question", "max_open")
    for key in ("templates_per_floor", "generators_per_floor", "per_skill_tier", "generator_variety"):
        need_int(1, "bank_targets", key)
    lo, hi = need_int(1, "placement_test", "min_questions"), need_int(1, "placement_test", "max_questions")
    if lo and hi and lo > hi:
        errors.append("placement_test: min_questions is above max_questions")
    if hi and _is_int(main) and hi < main:
        errors.append("placement_test: max_questions must allow one question for every main floor")
    most, least = need_int(1, "placement_test", "per_floor"), need_int(1, "placement_test", "block_min")
    if most and least and least > most:
        errors.append("placement_test: block_min is above per_floor")
    pp =_get(config, "placement_test", "pass_pct")
    if not (isinstance(pp, (int, float)) and not isinstance(pp, bool) and 0 < pp <= 100):
        errors.append("placement_test.pass_pct: must be above 0 and at most 100")
    if _get(config, "placement_test", "retake_after_days") is not None:
        need_int(0, "placement_test", "retake_after_days")

    share = [_get(config, "spiral_review", k) for k in ("share_min", "share_max")]
    if not (all(isinstance(s, (int, float)) and not isinstance(s, bool) for s in share)
            and 0 <= share[0] <= share[1] < 1):
        errors.append("spiral_review: need 0 <= share_min <= share_max < 1")
    elif share[1] > 0 and 1 / math.ceil(1 / share[1]) < share[0] - 1e-9:
        # one review question every ceil(1 / share_max) questions is what the loop can do
        errors.append(f"spiral_review: a share of at most {share[1]} means one review question every "
                      f"{math.ceil(1 / share[1])}, which is below share_min {share[0]}")
    days = _get(config, "spiral_review", "intervals_days")
    if not (isinstance(days, list) and days and all(_is_int(d) and d >= 1 for d in days)
            and all(a < b for a, b in zip(days, days[1:]))):
        errors.append("spiral_review.intervals_days: must be whole days that keep growing")

    for key in ("counts_as_wrong", "resets_combo"):
        if not isinstance(_get(config, "timeout", key), bool):
            errors.append(f"timeout.{key}: must be true or false")

    qts = _get(config, "question_types")
    qts = _clean(qts) if isinstance(qts, dict) else {}
    if not qts:
        errors.append("question_types: is missing or empty")
    for name, q in qts.items():
        if not ID_RE.match(name):
            errors.append(f"question_types.{name}: the id must be lowercase letters, digits and _")
        problem = text_problem(_get(q, "name_vi"))
        if problem:
            errors.append(f"question_types.{name}.name_vi {problem}")
        limits = _get(q, "time_limit")
        if not (isinstance(limits, list) and len(limits) == len(TIERS)):
            errors.append(f"question_types.{name}.time_limit: must list {len(TIERS)} values, one per tier")
            continue
        last = 0
        for tier, seconds in zip(TIERS, limits):
            if seconds is None:
                if last:
                    errors.append(f"question_types.{name}.time_limit: tier {tier} is null above a tier that has a time")
                continue
            if not (_is_int(seconds) and seconds > 0):
                errors.append(f"question_types.{name}.time_limit: tier {tier} must be whole seconds above 0, or null")
                continue
            if seconds < last:
                errors.append(f"question_types.{name}.time_limit: tier {tier} has less time than the tier below")
            last = seconds
        if not last:
            errors.append(f"question_types.{name}.time_limit: no tier has a time")
    for tier in TIERS:
        if qts and not any(isinstance(_get(q, "time_limit"), list) and len(q["time_limit"]) == len(TIERS)
                           and q["time_limit"][tier - 1] is not None for q in qts.values()):
            errors.append(f"question_types: no question type can be asked at tier {tier}")
    return errors


def validate_subject(raw: dict, config: dict) -> list[str]:
    """Problems in one data/math/<subject>.json, given a config that is itself valid."""
    errors: list[str] = []
    for key in _unknown_keys(raw, _SUBJECT_KEYS):
        errors.append(f"unknown key {key!r}")
    floors = raw.get("floors")
    if not isinstance(floors, list) or not floors or not all(isinstance(f, dict) for f in floors):
        return errors + ["floors: is missing or empty"]

    main, hidden = config["main_floors"], config["hidden_floor"]
    numbers = [f.get("floor") for f in floors]
    if numbers[:main] != list(range(1, main + 1)) or numbers[main:] not in ([], [hidden]):
        errors.append(f"floors: must be numbered 1..{main} in order, then optionally the hidden floor {hidden}; "
                      f"got {numbers}")
    few, many = config["skills_per_floor"]["min"], config["skills_per_floor"]["max"]

    floor_of: dict[str, int] = {}
    graph: dict[str, list[str]] = {}
    for f in floors:
        n = f.get("floor")
        here = f"floor {n}"
        for key in _unknown_keys(f, _FLOOR_KEYS):
            errors.append(f"{here}: unknown key {key!r}")
        if not _is_int(n):
            errors.append(f"{here}: the floor number must be a whole number")
            continue
        if f.get("hidden", False) is not (n == hidden):
            errors.append(f"{here}: \"hidden\" must be true for floor {hidden} and absent for the others")
        problem = text_problem(f.get("title_vi"))
        if problem:
            errors.append(f"{here}: title_vi {problem}")
        if "syllabus_ref" in f and text_problem(f["syllabus_ref"]):
            errors.append(f"{here}: syllabus_ref {text_problem(f['syllabus_ref'])}")
        skills = f.get("skills")
        if not isinstance(skills, list) or not all(isinstance(s, dict) for s in skills):
            errors.append(f"{here}: skills is missing")
            continue
        if not few <= len(skills) <= many:
            errors.append(f"{here}: has {len(skills)} micro-skills, need {few} to {many}")
        for s in skills:
            sid = s.get("id")
            where = f"{here}, {sid}"
            for key in _unknown_keys(s, _SKILL_KEYS):
                errors.append(f"{where}: unknown key {key!r}")
            if not isinstance(sid, str) or not ID_RE.match(sid):
                errors.append(f"{where}: the id must be 3-40 lowercase letters, digits and _")
                continue
            if sid in floor_of:
                errors.append(f"{where}: this id is used twice")
                continue
            for field in ("name_vi", "desc_vi"):
                problem = text_problem(s.get(field))
                if problem:
                    errors.append(f"{where}: {field} {problem}")
            if "extension" in s and s["extension"] not in EXTENSIONS:
                errors.append(f"{where}: extension must be one of {sorted(EXTENSIONS)}")
            reqs = s.get("requires")
            if not isinstance(reqs, list) or not all(isinstance(r, str) for r in reqs):
                errors.append(f"{where}: requires must be a list of micro-skill ids (may be empty)")
                reqs = []
            if len(set(reqs)) != len(reqs):
                errors.append(f"{where}: requires lists the same micro-skill twice")
            floor_of[sid] = n
            graph[sid] = list(reqs)

    for sid, reqs in graph.items():
        for r in reqs:
            if r == sid:
                errors.append(f"{sid}: requires itself")
            elif r not in floor_of:
                errors.append(f"{sid}: requires {r}, which does not exist")
            elif floor_of[r] > floor_of[sid]:
                hint = " (the hidden floor may never block a main floor)" if floor_of[r] == hidden else ""
                errors.append(f"{sid} (floor {floor_of[sid]}): requires {r} from the later floor {floor_of[r]}{hint}")
    cycle = find_cycle({sid: [r for r in reqs if r != sid] for sid, reqs in graph.items()})
    if cycle:
        errors.append("prerequisite cycle: " + " -> ".join(cycle))
    return errors


def validate_index(index: dict, math_dir: Path = MATH_DIR) -> list[str]:
    """Problems in data/math/subjects.json."""
    from ..systems import catalog
    errors: list[str] = []
    for key in _unknown_keys(index, _INDEX_KEYS):
        errors.append(f"unknown key {key!r}")
    realm = index.get("cultivation_realm")
    if realm not in {r["id"] for r in catalog.realms()}:
        errors.append(f"cultivation_realm: {realm!r} is not a realm in realms_cultivation.json")
    entries = index.get("subjects")
    if not isinstance(entries, list) or not entries or not all(isinstance(e, dict) for e in entries):
        return errors + ["subjects: is missing or empty"]
    ids, orders = set(), set()
    for e in entries:
        sid = e.get("id")
        for key in _unknown_keys(e, _ENTRY_KEYS):
            errors.append(f"{sid}: unknown key {key!r}")
        if not isinstance(sid, str) or not ID_RE.match(sid):
            errors.append(f"{sid}: the id must be 3-40 lowercase letters, digits and _")
        elif sid in ids:
            errors.append(f"{sid}: this id is used twice")
        ids.add(sid)
        order = e.get("order")
        if not (_is_int(order) and order >= 1) or order in orders:
            errors.append(f"{sid}: order must be a whole number >= 1 that no other subject uses")
        orders.add(order)
        problem = text_problem(e.get("name_vi"))
        if problem:
            errors.append(f"{sid}: name_vi {problem}")
        courses = e.get("courses")
        if not isinstance(courses, list) or not courses or not all(isinstance(c, str) and c.strip() for c in courses):
            errors.append(f"{sid}: courses must list at least one course code")
        file = e.get("file", "")
        if file is not None and not (isinstance(file, str) and (math_dir / file).is_file()):
            errors.append(f"{sid}: file {file!r} is not in {math_dir.name}/ (use null for a subject not written yet)")
    return errors


def _read_checked(path: Path) -> tuple[dict, str | None]:
    """(data, None), or ({}, why the file cannot be used). A stray comma in a hand-edited
    file becomes one line of the report instead of a traceback."""
    try:
        data = _read(path)
    except (OSError, ValueError) as e:      # JSONDecodeError and UnicodeDecodeError are ValueErrors
        return {}, f"cannot be read as JSON ({e})"
    if not isinstance(data, dict):
        return {}, "must be a JSON object"
    return data, None


def validate_all(math_dir: Path = MATH_DIR, config: dict | None = None) -> list[str]:
    """Every problem in the path data, each line starting with the file it is in."""
    config = cfg() if config is None else config
    errors = [f"balance/math.json: {e}" for e in validate_config(config)]
    if errors:
        return errors                      # the floor checks need a config that makes sense
    index, problem = _read_checked(math_dir / "subjects.json")
    if problem:
        return [f"math/subjects.json: {problem}"]
    index = _clean(index)
    errors += [f"math/subjects.json: {e}" for e in validate_index(index, math_dir)]
    seen: dict[str, str] = {}
    for e in index.get("subjects") or []:
        file = e.get("file") if isinstance(e, dict) else None
        if not isinstance(file, str) or not (math_dir / file).is_file():
            continue
        raw, problem = _read_checked(math_dir / file)
        if problem:
            errors.append(f"math/{file}: {problem}")
            continue
        if raw.get("id") != e.get("id"):
            errors.append(f"math/{file}: its id is {raw.get('id')!r} but subjects.json calls it {e.get('id')!r}")
        errors += [f"math/{file}: {x}" for x in validate_subject(raw, config)]
        for f in raw.get("floors") or []:
            for s in (f.get("skills") or []) if isinstance(f, dict) else []:
                sid = s.get("id") if isinstance(s, dict) else None
                if sid in seen and seen[sid] != file:
                    errors.append(f"math/{file}: micro-skill {sid} is already used in math/{seen[sid]}")
                seen.setdefault(sid, file)
    return errors
