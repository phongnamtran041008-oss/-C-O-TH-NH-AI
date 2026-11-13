"""Math questions (milestone M2): the items of data/math/items/<subject>.json, how one
becomes a question a player sees, and how an answer is graded.

An item belongs to one micro-skill and one tier. Three question types are playable so
far; the other types of balance/math.json come with later milestones:

  true_false       "answer": true | false                     the player sends {"value": bool}
  multiple_choice  "options_vi": [...], "answer": <index>      the player sends {"option": "a"}
  numeric          "answer": "7" | "3/4" | "1, 3, 5"           the player sends {"text": "..."}
                   ("unordered": true when the listed numbers form a set)

Pure data and rules, like math_path: no database here. `validate_all()` returns one
readable line per problem; the tests and tools/check_all.py fail when it is not empty.
"""
from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from . import math_path
from .math_path import MATH_DIR, text_problem

ITEMS_DIR_NAME = "items"
PLAYABLE_TYPES = ("true_false", "multiple_choice", "numeric")
OPTION_IDS = "abcdef"
MIN_OPTIONS, MAX_OPTIONS = 2, 6
MAX_NUMBERS = 12            # longest list a numeric answer may have
MAX_ANSWER_CHARS = 120      # longer typed answers are wrong without being parsed

TRUE_VI, FALSE_VI = "Đúng", "Sai"
INSTRUCTIONS_VI = {
    "true_false": "Mệnh đề sau đúng hay sai?",
    "multiple_choice": "Chọn một đáp án đúng",
    "numeric": "Điền số (phân số viết a/b, nhiều số cách nhau bằng dấu phẩy)",
}
INPUTS = {"true_false": "truefalse", "multiple_choice": "choice", "numeric": "number"}

_FILE_KEYS = {"subject", "items"}
_ITEM_KEYS = {"id", "skill", "tier", "type", "prompt_vi", "options_vi", "answer", "unordered",
              "solution_vi", "reviewed"}


# ------------------------------------------------------------------ numbers
def parse_number(text: str) -> Fraction | None:
    """One number as typed by a player: 7, -3, 0.25, 3/4, -1/2. None when it is not a number.
    The decimal mark is a point; the comma separates the numbers of a list."""
    s = text.strip().replace(" ", "")
    if not s or len(s) > 40:
        return None
    num, slash, den = s.partition("/")
    try:
        if slash:
            if not _plain_integer(num) or not _plain_integer(den, signed=False):
                return None
            return Fraction(int(num), int(den)) if int(den) else None
        if not _plain_decimal(s):
            return None
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None


def _plain_integer(s: str, signed: bool = True) -> bool:
    body = s[1:] if signed and s[:1] in "+-" else s
    return body.isascii() and body.isdigit()


def _plain_decimal(s: str) -> bool:
    body = s[1:] if s[:1] in "+-" else s
    whole, _, frac = body.partition(".")
    return (body.isascii() and body.count(".") <= 1 and (whole + frac).isdigit()
            and all(part.isdigit() for part in (whole, frac) if part))


def parse_numbers(text) -> list[Fraction] | None:
    """A typed numeric answer: one number, or several separated by commas or semicolons.
    None when any part is not a number."""
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_ANSWER_CHARS:
        return None
    parts = [p for p in text.replace(";", ",").split(",")]
    if len(parts) > MAX_NUMBERS:
        return None
    out = [parse_number(p) for p in parts]
    return None if any(n is None for n in out) else out


def number_text(n: Fraction) -> str:
    return str(n.numerator) if n.denominator == 1 else f"{n.numerator}/{n.denominator}"


# ------------------------------------------------------------------ items
@dataclass(frozen=True)
class MathItem:
    id: str
    subject: str
    skill: str
    floor: int
    tier: int
    qtype: str
    prompt_vi: str
    answer: object                       # bool | option index | numeric text
    solution_vi: tuple[str, ...]
    options_vi: tuple[str, ...] = ()
    unordered: bool = False
    reviewed: bool = False

    @property
    def fingerprint(self) -> str:
        """concept + template + numbers. A hand-written item is its own template with fixed
        numbers; generators (M3) put the numbers they drew in the third part."""
        return fingerprint(self.skill, self.id, "")

    @property
    def answer_text(self) -> str:
        if self.qtype == "true_false":
            return TRUE_VI if self.answer else FALSE_VI
        if self.qtype == "multiple_choice":
            return self.options_vi[self.answer]
        return ", ".join(number_text(n) for n in parse_numbers(self.answer))


def fingerprint(skill: str, template: str, numbers: str) -> str:
    return hashlib.sha1(f"{skill}|{template}|{numbers}".encode()).hexdigest()[:32]


@dataclass
class MathQuestion:
    """What quiz.create_session stores: the same shape as a vocabulary Question."""
    qtype: str
    item_id: str
    prompt: dict
    input: str
    options: list[dict] | None
    answer_key: dict
    time_limit: float
    meta: dict = field(default_factory=dict)

    def public(self) -> dict:
        return {"qtype": self.qtype, "instruction_vi": INSTRUCTIONS_VI[self.qtype],
                "prompt": self.prompt, "input": self.input, "options": self.options,
                "time_limit": self.time_limit, "math": self.meta}


def to_question(item: MathItem, rng: random.Random | None = None, config: dict | None = None) -> MathQuestion:
    """The question a player gets for this item. Options are shuffled; the answer key
    (never sent before answering) carries the solution steps."""
    rng = rng or random.Random()
    config = config or math_path.cfg()
    limit = math_path.time_limit(item.qtype, item.tier, config)
    if item.qtype not in PLAYABLE_TYPES or limit is None:
        raise ValueError(f"{item.id}: a {item.qtype} question cannot be asked at tier {item.tier}")
    subject = math_path.subject(item.subject)
    reveal = {"answer_text": item.answer_text, "solution_vi": list(item.solution_vi)}
    key: dict = {"reveal": reveal, "fingerprint": item.fingerprint}
    options = None
    if item.qtype == "true_false":
        key["value"] = bool(item.answer)
    elif item.qtype == "multiple_choice":
        order = list(range(len(item.options_vi)))
        rng.shuffle(order)
        options = [{"id": OPTION_IDS[i], "text": item.options_vi[src]} for i, src in enumerate(order)]
        key["option"] = OPTION_IDS[order.index(item.answer)]
    else:
        key["numbers"] = [number_text(n) for n in parse_numbers(item.answer)]
        key["unordered"] = item.unordered
        key["tolerance"] = float(config["numeric_tolerance"])
    meta = {"subject": item.subject, "subject_name_vi": subject.name_vi, "skill": item.skill,
            "skill_name_vi": subject.skills[item.skill].name_vi, "floor": item.floor, "tier": item.tier,
            "tier_name_vi": config["tiers"][str(item.tier)]["name_vi"]}
    return MathQuestion(qtype=item.qtype, item_id=item.id, prompt={"text": item.prompt_vi},
                        input=INPUTS[item.qtype], options=options, answer_key=key,
                        time_limit=float(limit), meta=meta)


# ------------------------------------------------------------------ grading
def grade(qtype: str, answer_key: dict, answer: dict | None) -> bool:
    if not isinstance(answer, dict):
        return False
    if qtype == "true_false":
        value = answer.get("value")
        return isinstance(value, bool) and value == answer_key["value"]
    if qtype == "multiple_choice":
        option = answer.get("option")
        return isinstance(option, str) and option == answer_key["option"]
    if qtype == "numeric":
        given = parse_numbers(answer.get("text"))
        want = [Fraction(n) for n in answer_key["numbers"]]
        if given is None or len(given) != len(want):
            return False
        if answer_key.get("unordered"):
            given, want = sorted(given), sorted(want)
        tolerance = Fraction(str(answer_key.get("tolerance", 0)))
        return all(abs(g - w) <= tolerance for g, w in zip(given, want))
    return False


# ------------------------------------------------------------------ the bank
def items_path(subject_id: str, math_dir: Path = MATH_DIR) -> Path:
    return math_dir / ITEMS_DIR_NAME / f"{subject_id}.json"


def build_item(subject: math_path.Subject, raw: dict) -> MathItem:
    return MathItem(id=raw["id"], subject=subject.id, skill=raw["skill"],
                    floor=subject.skills[raw["skill"]].floor, tier=raw["tier"], qtype=raw["type"],
                    prompt_vi=raw["prompt_vi"], answer=raw["answer"],
                    solution_vi=tuple(raw["solution_vi"]), options_vi=tuple(raw.get("options_vi", ())),
                    unordered=bool(raw.get("unordered", False)), reviewed=bool(raw.get("reviewed", False)))


@lru_cache(maxsize=1)
def bank() -> dict[str, MathItem]:
    """Every item of every written subject, by id."""
    out: dict[str, MathItem] = {}
    for subject in math_path.subjects():
        path = items_path(subject.id)
        if path.is_file():
            for raw in json.loads(path.read_text("utf-8"))["items"]:
                out[raw["id"]] = build_item(subject, raw)
    return out


def floor_items(subject_id: str, floor: int, allow_unreviewed: bool) -> list[MathItem]:
    """The items a player may get on this floor: unreviewed ones only where the server
    allows them (ALLOW_UNREVIEWED, on by default in the dev environment only)."""
    return [i for i in bank().values()
            if i.subject == subject_id and i.floor == floor and (i.reviewed or allow_unreviewed)]


# ------------------------------------------------------------------ validation
def validate_items(subject: math_path.Subject, raw: dict, config: dict) -> list[str]:
    """Problems in one data/math/items/<subject>.json."""
    errors = [f"unknown key {k!r}" for k in sorted(raw) if not k.startswith("_") and k not in _FILE_KEYS]
    if raw.get("subject") != subject.id:
        errors.append(f"its subject is {raw.get('subject')!r} but the file belongs to {subject.id!r}")
    items = raw.get("items")
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        return errors + ["items: must be a list of questions"]
    qtypes = math_path.question_types(config)
    seen: set[str] = set()
    prompts: dict[tuple[str, str], str] = {}
    for n, it in enumerate(items, 1):
        iid = it.get("id")
        here = iid if isinstance(iid, str) else f"item {n}"
        for key in sorted(k for k in it if not k.startswith("_") and k not in _ITEM_KEYS):
            errors.append(f"{here}: unknown key {key!r}")
        if not isinstance(iid, str) or not math_path.ID_RE.match(iid):
            errors.append(f"{here}: the id must be 3-40 lowercase letters, digits and _")
        elif iid in seen:
            errors.append(f"{here}: this id is used twice")
        seen.add(iid)

        skill = subject.skills.get(it.get("skill")) if isinstance(it.get("skill"), str) else None
        if skill is None:
            errors.append(f"{here}: skill {it.get('skill')!r} is not a micro-skill of {subject.id}")
        tier, qtype = it.get("tier"), it.get("type")
        if tier not in math_path.TIERS or isinstance(tier, bool):
            errors.append(f"{here}: tier must be 1..{math_path.TOP_TIER}")
        elif skill is not None and not math_path.tier_allowed(skill.floor, tier, config):
            lo, hi = math_path.floor_tiers(skill.floor, config)
            errors.append(f"{here}: tier {tier} is not allowed on floor {skill.floor} (tiers {lo}-{hi})")
        if qtype not in PLAYABLE_TYPES:
            errors.append(f"{here}: type must be one of {', '.join(PLAYABLE_TYPES)}")
        elif qtype not in qtypes:
            errors.append(f"{here}: type {qtype} has no time limits in balance/math.json")
        elif tier in math_path.TIERS and qtypes[qtype]["time_limit"][tier - 1] is None:
            errors.append(f"{here}: a {qtype} question does not exist at tier {tier}")

        problem = text_problem(it.get("prompt_vi"))
        if problem:
            errors.append(f"{here}: prompt_vi {problem}")
        elif (it.get("skill"), it["prompt_vi"]) in prompts:
            errors.append(f"{here}: has the same question text as {prompts[(it.get('skill'), it['prompt_vi'])]}")
        else:
            prompts[(it.get("skill"), it["prompt_vi"])] = here
        steps = it.get("solution_vi")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{here}: solution_vi must list at least one step")
        else:
            for k, step in enumerate(steps, 1):
                problem = text_problem(step)
                if problem:
                    errors.append(f"{here}: solution_vi step {k} {problem}")
        if not isinstance(it.get("reviewed", False), bool):
            errors.append(f"{here}: reviewed must be true or false")

        answer = it.get("answer")
        if qtype != "multiple_choice" and "options_vi" in it:
            errors.append(f"{here}: only a multiple_choice question has options_vi")
        if qtype != "numeric" and "unordered" in it:
            errors.append(f"{here}: only a numeric question has unordered")
        if qtype == "true_false":
            if not isinstance(answer, bool):
                errors.append(f"{here}: the answer of a true_false question must be true or false")
        elif qtype == "multiple_choice":
            options = it.get("options_vi")
            if not (isinstance(options, list) and MIN_OPTIONS <= len(options) <= MAX_OPTIONS):
                errors.append(f"{here}: options_vi must list {MIN_OPTIONS} to {MAX_OPTIONS} options")
                continue
            for k, option in enumerate(options, 1):
                problem = text_problem(option)
                if problem:
                    errors.append(f"{here}: option {k} {problem}")
            texts = [" ".join(o.split()).casefold() for o in options if isinstance(o, str)]
            if len(set(texts)) != len(texts):
                errors.append(f"{here}: two options have the same text, so more than one would be right")
            if isinstance(answer, bool) or not isinstance(answer, int) or not 0 <= answer < len(options):
                errors.append(f"{here}: answer must be the position (from 0) of the one right option")
        elif qtype == "numeric":
            numbers = parse_numbers(answer)
            if numbers is None:
                errors.append(f"{here}: answer must be a number, a fraction a/b or numbers separated by commas")
            elif not isinstance(it.get("unordered", False), bool):
                errors.append(f"{here}: unordered must be true or false")
            elif it.get("unordered") and len(set(numbers)) != len(numbers):
                errors.append(f"{here}: an unordered answer lists the same number twice")
    return errors


def validate_all(math_dir: Path = MATH_DIR, config: dict | None = None) -> list[str]:
    """Every problem in the item files, each line starting with the file it is in. Run
    after math_path.validate_all() passes: the items are checked against that path."""
    config = math_path.cfg() if config is None else config
    errors: list[str] = []
    index = math_path.load_index(math_dir)
    known = set()
    for entry in sorted((e for e in index["subjects"] if e.get("file")), key=lambda e: e["order"]):
        subject = math_path.build_subject(entry, json.loads((math_dir / entry["file"]).read_text("utf-8")))
        known.add(subject.id)
        path = items_path(subject.id, math_dir)
        if not path.is_file():
            continue
        name = f"math/{ITEMS_DIR_NAME}/{path.name}"
        try:
            raw = json.loads(path.read_text("utf-8"))
        except (OSError, ValueError) as e:
            errors.append(f"{name}: cannot be read as JSON ({e})")
            continue
        if not isinstance(raw, dict):
            errors.append(f"{name}: must be a JSON object")
            continue
        errors += [f"{name}: {e}" for e in validate_items(subject, raw, config)]
    folder = math_dir / ITEMS_DIR_NAME
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if path.stem not in known:
            errors.append(f"math/{ITEMS_DIR_NAME}/{path.name}: no written subject has this id")
    return errors
