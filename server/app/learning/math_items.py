"""Math questions: the templates of data/math/items/<subject>.json, how one becomes a
question a player sees, and how an answer is graded.

A *template* belongs to one micro-skill and one tier. There are two kinds:

  * a hand-written item (the "items" list): one fixed question;
  * a generator (the "generators" list + a function in learning/math_gen): a question
    with new numbers every time it is drawn.

Six question types are playable so far; the other types of balance/math.json come with
later milestones:

  true_false       "answer": true | false                     the player sends {"value": bool}
  multiple_choice  "options_vi": [...], "answer": <index>      the player sends {"option": "a"}
  numeric          "answer": "7" | "3/4" | "1, 3, 5"           the player sends {"text": "..."}
                   ("unordered": true when the listed numbers form a set)
  matching         "pairs_vi": [[left, right], ...]  (3-5)     the player sends {"pairs": [r0, r1, ...]}
  ordering         "steps_vi": [step, ...]  (3-6, right order) the player sends {"order": [i0, i1, ...]}
  find_mistake     "lines_vi": [line, ...] (3-6), "answer": <index of the first wrong line>
                                                              the player sends {"line": i}
  tribulation      "parts": [part, ...] (2-4), tiers 4-5 only  the player sends {"parts": [a0, a1, ...]}
                   (Thiên kiếp, M11 đợt 2: one situation in prompt_vi, then parts that build on
                   each other; a part is a true_false, multiple_choice or numeric question with
                   exactly the fields that type has as an item, and ai is that part's own
                   answer. Right only when every part is right.)

A numeric item or numeric part may carry "tolerance": an absolute tolerance (0 < t <= 1) for an
answer that is a rounded decimal; it replaces balance/math.json numeric_tolerance for that
question only.

Every hand-written tier-5 item has a "ladder" (learning-path rule 8, M11 đợt 2): 2 to 4 ids,
in the order they are asked, of hand-written items or generators of the same subject at tier
3 or 4 (at least one at tier 4), on a floor not above the item's own, neither the item itself
nor any id twice. When the player gets the tier-5 question wrong in a buổi luyện, these come
next (systems/math_practice.py). No other item has a ladder.

A matching or ordering item has no "answer": the data is written right (each left side next
to its right side, the steps in the order of the derivation) and the server shuffles what it
shows, so the answer key is the inverse of that shuffle (see to_question).

A question may show small matrices next to its text ("matrices": {"A": [[1, 2], [3, 4]]});
the game draws them, so the text only names them.

Pure data and rules, like math_path: no database here. `validate_all()` returns one
readable line per problem; the tests and tools/check_all.py fail when it is not empty.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import random
import re
from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from . import math_path
from .math_path import MATH_DIR, text_problem

ITEMS_DIR_NAME = "items"
PLAYABLE_TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake",
                  "tribulation")
PART_TYPES = ("true_false", "multiple_choice", "numeric")     # what a part of a tribulation may be
MIN_PARTS, MAX_PARTS = 2, 4     # a tribulation question
MAX_TOLERANCE = 1               # a numeric "tolerance" is above 0 and at most this
OPTION_IDS = "abcdef"
MIN_OPTIONS, MAX_OPTIONS = 2, 6
MIN_PAIRS, MAX_PAIRS = 3, 5     # a matching question (fewer is a guess, more does not fit the card)
MIN_STEPS, MAX_STEPS = 3, 6     # an ordering question
MIN_LINES, MAX_LINES = 3, 6     # a find_mistake question: the lines of the worked solution
MAX_NUMBERS = 12            # longest list a numeric answer may have
MAX_ANSWER_CHARS = 120      # longer typed answers are wrong without being parsed
MAX_MATRICES, MAX_MATRIX_SIDE = 3, 4
MATRIX_NAME_RE = re.compile(r"^[A-Z]$")
MATRIX_ENTRY_RE = re.compile(r"^(-?\d{1,4}(/\d{1,3})?|[a-z])$")    # a number, a fraction, or an unknown like x
NEAR_DUPLICATE = 0.95       # two hand-written prompts this alike (digits ignored) are one question twice

TRUE_VI, FALSE_VI = "Đúng", "Sai"
INSTRUCTIONS_VI = {
    "true_false": "Mệnh đề sau đúng hay sai?",
    "multiple_choice": "Chọn một đáp án đúng",
    "numeric": "Điền số (phân số viết a/b, nhiều số cách nhau bằng dấu phẩy)",
    "matching": "Ghép mỗi vế trái với một vế phải cho đúng",
    "ordering": "Sắp xếp các bước giải theo đúng thứ tự",
    "find_mistake": "Tìm bước đầu tiên bị sai trong lời giải",
    "tribulation": "Thiên kiếp: trả lời đúng mọi phần của bài tổng hợp",
}
INPUTS = {"true_false": "truefalse", "multiple_choice": "choice", "numeric": "number",
          "matching": "matching", "ordering": "ordering", "find_mistake": "find_mistake",
          "tribulation": "tribulation"}
MATCH_SEP_VI = " — "        # between the two sides of a pair in the revealed answer
PART_LETTERS = "abcd"       # the parts of a tribulation: a), b), ...

_FILE_KEYS = {"subject", "items", "generators"}
_ITEM_KEYS = {"id", "skill", "tier", "type", "prompt_vi", "options_vi", "answer", "unordered",
              "pairs_vi", "steps_vi", "lines_vi", "solution_vi", "matrices", "reviewed", "parts", "tolerance",
              "ladder"}
_PART_KEYS = {"true_false": {"type", "prompt_vi", "answer"},          # a part has exactly the fields
              "multiple_choice": {"type", "prompt_vi", "options_vi", "answer"},     # its type has as an item
              "numeric": {"type", "prompt_vi", "answer", "unordered", "tolerance"}}
_KEYED_TYPES = ("matching", "ordering")      # the data order is the answer: no "answer" key
_GENERATOR_KEYS = {"id", "skill", "tier", "type", "reviewed"}


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


def _numbers_text(answer, tolerance) -> str:
    """A numeric answer as the reveal shows it: exact numbers in lowest terms, a rounded
    decimal (one with a tolerance) as it was written - "12.35", not "247/20"."""
    if tolerance is not None:
        return ", ".join(p.strip() for p in str(answer).replace(";", ",").split(","))
    return ", ".join(number_text(n) for n in parse_numbers(answer))


# ------------------------------------------------------------------ templates
@dataclass(frozen=True)
class MathPart:
    """One part of a tribulation question: a true_false, multiple_choice or numeric question
    without a solution of its own (the solution of the whole problem covers every part)."""
    qtype: str
    prompt_vi: str
    answer: object                       # bool | option index | numeric text
    options_vi: tuple[str, ...] = ()
    unordered: bool = False
    tolerance: float | None = None

    @property
    def answer_text(self) -> str:
        if self.qtype == "true_false":
            return TRUE_VI if self.answer else FALSE_VI
        if self.qtype == "multiple_choice":
            return self.options_vi[self.answer]
        return _numbers_text(self.answer, self.tolerance)


def build_part(raw: dict) -> MathPart:
    return MathPart(qtype=raw["type"], prompt_vi=raw["prompt_vi"], answer=raw.get("answer"),
                    options_vi=tuple(raw.get("options_vi", ())), unordered=bool(raw.get("unordered", False)),
                    tolerance=raw.get("tolerance"))


@dataclass(frozen=True)
class MathItem:
    """One concrete question: a hand-written item, or one draw of a generator (then
    `numbers` says which numbers were drawn and `id` is the id of the generator)."""
    id: str
    subject: str
    skill: str
    floor: int
    tier: int
    qtype: str
    prompt_vi: str
    answer: object                       # bool | option index | numeric text | wrong line index | None (matching, ordering)
    solution_vi: tuple[str, ...]
    options_vi: tuple[str, ...] = ()
    unordered: bool = False
    pairs_vi: tuple[tuple[str, str], ...] = ()     # matching: (left, right), each left next to its right
    steps_vi: tuple[str, ...] = ()                 # ordering: the steps in the right order
    lines_vi: tuple[str, ...] = ()                 # find_mistake: the lines of the solution, as written
    reviewed: bool = False
    matrices: tuple[tuple[str, tuple[tuple[str, ...], ...]], ...] = ()    # ((name, rows), ...)
    numbers: str = ""
    generated: bool = False
    parts: tuple[MathPart, ...] = ()               # tribulation: the parts, in order
    tolerance: float | None = None                 # numeric: replaces numeric_tolerance when set
    ladder: tuple[str, ...] = ()                   # rule 8: a hand-written tier-5 item's rungs, in order

    @property
    def fingerprint(self) -> str:
        """concept + template + numbers: what the anti-repeat window remembers."""
        return fingerprint(self.skill, self.id, self.numbers)

    @property
    def answer_text(self) -> str:
        if self.qtype == "true_false":
            return TRUE_VI if self.answer else FALSE_VI
        if self.qtype == "multiple_choice":
            return self.options_vi[self.answer]
        if self.qtype == "matching":
            return "; ".join(f"{left}{MATCH_SEP_VI}{right}" for left, right in self.pairs_vi)
        if self.qtype == "ordering":
            return "  ".join(f"{k}. {step}" for k, step in enumerate(self.steps_vi, 1))
        if self.qtype == "find_mistake":
            return f"Bước {self.answer + 1}: {self.lines_vi[self.answer]}"
        if self.qtype == "tribulation":
            return "; ".join(f"{PART_LETTERS[k]}) {p.answer_text}" for k, p in enumerate(self.parts))
        return _numbers_text(self.answer, self.tolerance)


@dataclass(frozen=True)
class GeneratorSpec:
    """A generator as the data file lists it; the function that draws lives in math_gen."""
    id: str
    subject: str
    skill: str
    floor: int
    tier: int
    qtype: str
    reviewed: bool = False
    generated: bool = True


Template = MathItem | GeneratorSpec


def fingerprint(skill: str, template: str, numbers: str) -> str:
    return hashlib.sha1(f"{skill}|{template}|{numbers}".encode()).hexdigest()[:32]


def _matrices(raw) -> tuple:
    return tuple((name, tuple(tuple(str(v) for v in row) for row in rows)) for name, rows in (raw or {}).items())


def draw(spec: GeneratorSpec, rng: random.Random) -> MathItem:
    """One question of this generator, with the numbers this rng gives."""
    from . import math_gen
    d = math_gen.REGISTRY[spec.id](rng)
    return MathItem(id=spec.id, subject=spec.subject, skill=spec.skill, floor=spec.floor, tier=spec.tier,
                    qtype=spec.qtype, prompt_vi=d.prompt_vi, answer=d.answer, solution_vi=tuple(d.solution_vi),
                    options_vi=tuple(d.options_vi), unordered=d.unordered, reviewed=spec.reviewed,
                    matrices=_matrices(d.matrices), numbers=json.dumps(d.params, sort_keys=True, ensure_ascii=True),
                    generated=True, tolerance=getattr(d, "tolerance", None))     # (a Draw may give one)


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


def shown_order(n: int, rng: random.Random) -> list[int]:
    """A shuffle of range(n) for a matching or ordering question that never shows the
    answer: shown position j holds data position order[j], and the shuffle is drawn again
    until at least one entry has moved (the right order shown as-is would be a free point)."""
    order = list(range(n))
    if n < 2:                   # (validation keeps these types at 3 or more; nothing to move)
        return order
    while order == sorted(order):
        rng.shuffle(order)
    return order


def _simple_key(qtype: str, answer, options_vi, unordered: bool, tolerance, rng: random.Random,
                config: dict) -> tuple[dict, list[dict] | None]:
    """The answer key and the shown options of a true_false, multiple_choice or numeric
    question - a whole item, or one part of a tribulation. Options are shuffled; a numeric key
    carries the item's own tolerance, else the global numeric_tolerance."""
    if qtype == "true_false":
        return {"value": bool(answer)}, None
    if qtype == "multiple_choice":
        order = list(range(len(options_vi)))
        rng.shuffle(order)
        options = [{"id": OPTION_IDS[i], "text": options_vi[src]} for i, src in enumerate(order)]
        return {"option": OPTION_IDS[order.index(answer)]}, options
    return {"numbers": [number_text(n) for n in parse_numbers(answer)], "unordered": bool(unordered),
            "tolerance": float(config["numeric_tolerance"] if tolerance is None else tolerance)}, None


def to_question(item: MathItem, rng: random.Random | None = None, config: dict | None = None,
                parallel: bool = False, review: bool = False) -> MathQuestion:
    """The question a player gets for this item. Options are shuffled; the answer key
    (never sent before answering) carries the solution steps. `parallel` marks the
    question that comes back after a mistake (rule 6a), `review` one that comes from a
    floor below the one being played (rule 6b, spiral review)."""
    rng = rng or random.Random()
    config = config or math_path.cfg()
    limit = math_path.time_limit(item.qtype, item.tier, config)
    if item.qtype not in PLAYABLE_TYPES or limit is None:
        raise ValueError(f"{item.id}: a {item.qtype} question cannot be asked at tier {item.tier}")
    subject = math_path.subject(item.subject)
    reveal = {"answer_text": item.answer_text, "solution_vi": list(item.solution_vi)}
    key: dict = {"reveal": reveal, "fingerprint": item.fingerprint}
    options = None
    shown_parts: list[dict] = []
    if item.qtype in PART_TYPES:
        part_key, options = _simple_key(item.qtype, item.answer, item.options_vi, item.unordered,
                                        item.tolerance, rng, config)
        key.update(part_key)
    elif item.qtype == "tribulation":
        # each part is asked like a question of its own type (a multiple-choice part's options
        # shuffled, in part order, with the same rng); its key has that type's shape
        key["parts"] = []
        for part in item.parts:
            part_key, part_options = _simple_key(part.qtype, part.answer, part.options_vi, part.unordered,
                                                 part.tolerance, rng, config)
            key["parts"].append(part_key)
            shown_parts.append({"text": part.prompt_vi, "input": INPUTS[part.qtype], "options": part_options})
        # (sent only after answering: what each part was, so the card can say which part was wrong)
        reveal["parts"] = [{"answer_text": p.answer_text, "key": k} for p, k in zip(item.parts, key["parts"])]
    elif item.qtype == "matching":
        # left stays in the data order; right is shuffled, so the right side of left k is
        # shown at the position where the shuffle put data entry k
        order = shown_order(len(item.pairs_vi), rng)
        shown_right = [item.pairs_vi[src][1] for src in order]
        key["pairs"] = [order.index(k) for k in range(len(order))]
    elif item.qtype == "ordering":
        order = shown_order(len(item.steps_vi), rng)
        shown_steps = [item.steps_vi[src] for src in order]
        key["order"] = [order.index(k) for k in range(len(order))]
    elif item.qtype == "find_mistake":
        key["line"] = item.answer       # the lines are shown as written: nothing to shuffle
    meta ={"subject": item.subject, "subject_name_vi": subject.name_vi, "skill": item.skill,
            "skill_name_vi": subject.skills[item.skill].name_vi, "floor": item.floor, "tier": item.tier,
            "tier_name_vi": config["tiers"][str(item.tier)]["name_vi"], "parallel": bool(parallel),
            "review": bool(review)}
    prompt: dict = {"text": item.prompt_vi}
    if item.qtype == "matching":
        prompt["left"] = [left for left, _ in item.pairs_vi]
        prompt["right"] = shown_right
    elif item.qtype == "ordering":
        prompt["steps"] = shown_steps
    elif item.qtype == "find_mistake":
        prompt["lines"] = list(item.lines_vi)
    elif item.qtype == "tribulation":
        prompt["parts"] = shown_parts
    if item.matrices:
        prompt["matrices"] = [{"name": name, "rows": [list(r) for r in rows]} for name, rows in item.matrices]
    return MathQuestion(qtype=item.qtype, item_id=item.id, prompt=prompt,
                        input=INPUTS[item.qtype], options=options, answer_key=key,
                        time_limit=float(limit), meta=meta)


# ------------------------------------------------------------------ grading
def _permutation(value, n: int) -> list[int] | None:
    """`value` as a permutation of range(n), or None: a list of n distinct ints (not bools,
    not floats like 1.0) each in 0..n-1. Anything else a client sends is a wrong answer."""
    if not isinstance(value, (list, tuple)) or len(value) != n:
        return None
    if not all(type(v) is int for v in value) or sorted(value) != list(range(n)):
        return None
    return list(value)


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
    if qtype in _KEYED_TYPES:
        name = "pairs" if qtype == "matching" else "order"
        want = answer_key.get(name)
        if not isinstance(want, list):
            return False
        given = _permutation(answer.get(name), len(want))
        return given is not None and given == want
    if qtype == "find_mistake":
        line = answer.get("line")
        return type(line) is int and type(answer_key.get("line")) is int and line == answer_key["line"]
    if qtype == "tribulation":
        # right only when every part is right, each graded by the rule of its own type; a
        # missing, extra or malformed part is a wrong answer, never an error
        keys, given = answer_key.get("parts"), answer.get("parts")
        if not isinstance(keys, list) or not keys or not isinstance(given, list) or len(given) != len(keys):
            return False
        return all(grade(part_type(k), k, g) for k, g in zip(keys, given))
    return False


def part_type(part_key) -> str:
    """The type of a tribulation part, read from the shape of its key."""
    if isinstance(part_key, dict):
        for name, qtype in (("value", "true_false"), ("option", "multiple_choice"), ("numbers", "numeric")):
            if name in part_key:
                return qtype
    return ""


# ------------------------------------------------------------------ the bank
def items_path(subject_id: str, math_dir: Path = MATH_DIR) -> Path:
    return math_dir / ITEMS_DIR_NAME / f"{subject_id}.json"


def build_item(subject: math_path.Subject, raw: dict) -> MathItem:
    return MathItem(id=raw["id"], subject=subject.id, skill=raw["skill"],
                    floor=subject.skills[raw["skill"]].floor, tier=raw["tier"], qtype=raw["type"],
                    prompt_vi=raw["prompt_vi"], answer=raw.get("answer"),
                    solution_vi=tuple(raw["solution_vi"]), options_vi=tuple(raw.get("options_vi", ())),
                    unordered=bool(raw.get("unordered", False)), reviewed=bool(raw.get("reviewed", False)),
                    pairs_vi=tuple((left, right) for left, right in raw.get("pairs_vi", ())),
                    steps_vi=tuple(raw.get("steps_vi", ())),
                    lines_vi=tuple(raw.get("lines_vi", ())),
                    matrices=_matrices(raw.get("matrices")),
                    parts=tuple(build_part(p) for p in raw.get("parts", ())), tolerance=raw.get("tolerance"),
                    ladder=tuple(raw.get("ladder") or ()))


def build_generator(subject: math_path.Subject, raw: dict) -> GeneratorSpec:
    return GeneratorSpec(id=raw["id"], subject=subject.id, skill=raw["skill"],
                         floor=subject.skills[raw["skill"]].floor, tier=raw["tier"], qtype=raw["type"],
                         reviewed=bool(raw.get("reviewed", False)))


def item_files(subject_id: str, math_dir: Path = MATH_DIR) -> list[Path]:
    """The item files of a subject: `<subject>.json`, then its parts `<subject>.<part>.json` in
    name order. A part is a group of floors written on its own (`giai_tich.t4_6.json`), so that
    floors can be added to a subject without rewriting - or sharing - one growing file."""
    folder = math_dir / ITEMS_DIR_NAME
    main = items_path(subject_id, math_dir)
    parts = sorted(folder.glob(f"{subject_id}.*.json")) if folder.is_dir() else []
    return ([main] if main.is_file() else []) + parts


def merge_items(subject_id: str, raws: list[dict]) -> dict:
    """The files of one subject as one: their items and generators, in file order."""
    out: dict = {"subject": subject_id, "items": [], "generators": []}
    for raw in raws:
        for key in ("items", "generators"):
            value = raw.get(key, [])
            out[key] = out[key] + value if isinstance(value, list) and isinstance(out[key], list) else value
    return out


def read_items(subject_id: str, math_dir: Path = MATH_DIR) -> dict | None:
    """Every item and generator entry of a subject, from all its files, or None when it has none."""
    files = item_files(subject_id, math_dir)
    if not files:
        return None
    return merge_items(subject_id, [json.loads(p.read_text("utf-8")) for p in files])


def _files() -> list[tuple[math_path.Subject, dict]]:
    out = []
    for subject in math_path.subjects():
        raw = read_items(subject.id)
        if raw is not None:
            out.append((subject, raw))
    return out


@lru_cache(maxsize=1)
def bank() -> dict[str, MathItem]:
    """Every hand-written item of every written subject, by id."""
    return {raw["id"]: build_item(subject, raw) for subject, data in _files() for raw in data.get("items", [])}


@lru_cache(maxsize=1)
def generators() -> dict[str, GeneratorSpec]:
    """Every generator of every written subject, by id."""
    return {raw["id"]: build_generator(subject, raw)
            for subject, data in _files() for raw in data.get("generators", [])}


def floor_items(subject_id: str, floor: int, allow_unreviewed: bool) -> list[MathItem]:
    """The hand-written items a player may get on this floor: unreviewed ones only where
    the server allows them (ALLOW_UNREVIEWED, on by default in the dev environment only)."""
    return [i for i in bank().values()
            if i.subject == subject_id and i.floor == floor and (i.reviewed or allow_unreviewed)]


def floor_templates(subject_id: str, floor: int, allow_unreviewed: bool) -> list[Template]:
    """Hand-written items and generators of this floor, under the same review rule."""
    return floor_items(subject_id, floor, allow_unreviewed) + [
        g for g in generators().values()
        if g.subject == subject_id and g.floor == floor and (g.reviewed or allow_unreviewed)]


# ------------------------------------------------------------------ validation
def _matrix_problems(matrices) -> list[str]:
    if not isinstance(matrices, dict) or not 1 <= len(matrices) <= MAX_MATRICES:
        return [f"matrices must name 1 to {MAX_MATRICES} matrices"]
    errors = []
    for name, rows in matrices.items():
        if not isinstance(name, str) or not MATRIX_NAME_RE.match(name):
            errors.append(f"matrix name {name!r} must be one capital letter A-Z")
            continue
        ok = (isinstance(rows, (list, tuple)) and 1 <= len(rows) <= MAX_MATRIX_SIDE
              and all(isinstance(r, (list, tuple)) and 1 <= len(r) <= MAX_MATRIX_SIDE for r in rows)
              and len({len(r) for r in rows}) == 1)
        if not ok:
            errors.append(f"matrix {name} must be a rectangle of 1 to {MAX_MATRIX_SIDE} rows and columns")
            continue
        for row in rows:
            for v in row:
                if isinstance(v, bool) or not isinstance(v, (int, str)) or not MATRIX_ENTRY_RE.match(str(v)):
                    errors.append(f"matrix {name}: entry {v!r} must be a number, a fraction a/b or one small letter")
    return errors


def _slot_problems(subject: math_path.Subject, it: dict, config: dict, here: str) -> list[str]:
    """Problems in what a hand-written item and a generator share: skill, tier, type."""
    errors = []
    qtypes = math_path.question_types(config)
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
    if not isinstance(it.get("reviewed", False), bool):
        errors.append(f"{here}: reviewed must be true or false")
    return errors


def _same_text(text: str) -> str:
    """How two display texts are compared for "the same": spacing and case ignored."""
    return " ".join(text.split()).casefold()


def _pairs_problems(pairs, here: str) -> list[str]:
    """A matching question: 3-5 pairs [left, right] of showable text, no two lefts and no two
    rights alike - otherwise more than one pairing would be right."""
    if not (isinstance(pairs, (list, tuple)) and MIN_PAIRS <= len(pairs) <= MAX_PAIRS):
        return [f"{here}: pairs_vi must list {MIN_PAIRS} to {MAX_PAIRS} pairs"]
    errors = []
    for k, pair in enumerate(pairs, 1):
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            errors.append(f"{here}: pair {k} must be [left side, right side]")
            continue
        for side, text in zip(("left", "right"), pair):
            problem = text_problem(text)
            if problem:
                errors.append(f"{here}: pair {k} {side} side {problem}")
    if errors:
        return errors
    for n, side in ((0, "left"), (1, "right")):
        texts = [_same_text(p[n]) for p in pairs]
        if len(set(texts)) != len(texts):
            errors.append(f"{here}: two {side} sides have the same text, so more than one pairing would be right")
    return errors


def _steps_problems(steps, here: str) -> list[str]:
    """An ordering question: 3-6 distinct steps of showable text, in the right order."""
    if not (isinstance(steps, (list, tuple)) and MIN_STEPS <= len(steps) <= MAX_STEPS):
        return [f"{here}: steps_vi must list {MIN_STEPS} to {MAX_STEPS} steps"]
    errors = []
    for k, step in enumerate(steps, 1):
        problem = text_problem(step)
        if problem:
            errors.append(f"{here}: step {k} {problem}")
    if not errors:
        texts = [_same_text(s) for s in steps]
        if len(set(texts)) != len(texts):
            errors.append(f"{here}: two steps have the same text, so more than one order would be right")
    return errors


def _lines_problems(lines, here: str) -> list[str]:
    """A find_mistake question: 3-6 distinct lines of showable text, the solution as written."""
    if not (isinstance(lines, (list, tuple)) and MIN_LINES <= len(lines) <= MAX_LINES):
        return [f"{here}: lines_vi must list {MIN_LINES} to {MAX_LINES} lines"]
    errors = []
    for k, line in enumerate(lines, 1):
        problem = text_problem(line)
        if problem:
            errors.append(f"{here}: line {k} {problem}")
    if not errors:
        texts = [_same_text(s) for s in lines]
        if len(set(texts)) != len(texts):
            errors.append(f"{here}: two lines have the same text, so more than one line could be the wrong one")
    return errors


def content_problems(it: dict, here: str) -> list[str]:
    """Problems in the question itself: the text, the options, the answer, the matrices.
    Used for hand-written items and for every draw of a generator."""
    errors = []
    qtype, answer = it.get("type"), it.get("answer")
    problem = text_problem(it.get("prompt_vi"))
    if problem:
        errors.append(f"{here}: prompt_vi {problem}")
    steps = it.get("solution_vi")
    if not isinstance(steps, (list, tuple)) or not steps:
        errors.append(f"{here}: solution_vi must list at least one step")
    else:
        for k, step in enumerate(steps, 1):
            problem = text_problem(step)
            if problem:
                errors.append(f"{here}: solution_vi step {k} {problem}")
    if it.get("matrices"):
        errors += [f"{here}: {e}" for e in _matrix_problems(it["matrices"])]
    return errors + _answer_problems(it, here)


def _tolerance_problems(it: dict, here: str) -> list[str]:
    """`tolerance`: only on a numeric question (or numeric part), a number in (0, MAX_TOLERANCE]."""
    if it.get("tolerance") is None:
        return []
    if it.get("type") != "numeric":
        return [f"{here}: only a numeric question has tolerance"]
    t = it["tolerance"]
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not 0 < t <= MAX_TOLERANCE:
        return [f"{here}: tolerance must be a number above 0 and at most {MAX_TOLERANCE}"]
    return []


def _parts_problems(parts, here: str) -> list[str]:
    """A tribulation question: 2-4 parts, each a true_false, multiple_choice or numeric question
    with exactly the fields that type has as an item, checked by the rules of that type."""
    if not (isinstance(parts, (list, tuple)) and MIN_PARTS <= len(parts) <= MAX_PARTS):
        return [f"{here}: parts must list {MIN_PARTS} to {MAX_PARTS} parts"]
    errors = []
    covered = set().union(*_PART_KEYS.values())      # (a field of another part type has its own message)
    for k, part in enumerate(parts, 1):
        at = f"{here} part {k}"
        if not isinstance(part, dict):
            errors.append(f"{at}: must be a question {{type, prompt_vi, answer, ...}}")
            continue
        if part.get("type") not in PART_TYPES:
            errors.append(f"{at}: type must be one of {', '.join(PART_TYPES)}")
            continue
        for key in sorted(k for k in part if not k.startswith("_") and k not in covered):
            errors.append(f"{at}: unknown key {key!r} (a part has only the fields of its type)")
        problem = text_problem(part.get("prompt_vi"))
        if problem:
            errors.append(f"{at}: prompt_vi {problem}")
        errors += _answer_problems(part, at)
    if not errors:
        texts = [_same_text(p["prompt_vi"]) for p in parts]
        if len(set(texts)) != len(texts):
            errors.append(f"{here}: two parts have the same text")
    return errors


def _answer_problems(it: dict, here: str) -> list[str]:
    """Problems in the answer of a question - a whole item or a part of a tribulation: the
    fields its type has (options, pairs, steps, lines, parts) and the answer key."""
    errors = []
    qtype, answer = it.get("type"), it.get("answer")
    if qtype != "multiple_choice" and it.get("options_vi"):
        errors.append(f"{here}: only a multiple_choice question has options_vi")
    if qtype != "numeric" and it.get("unordered"):
        errors.append(f"{here}: only a numeric question has unordered")
    if qtype != "matching" and it.get("pairs_vi"):
        errors.append(f"{here}: only a matching question has pairs_vi")
    if qtype != "ordering" and it.get("steps_vi"):
        errors.append(f"{here}: only an ordering question has steps_vi")
    if qtype != "find_mistake" and it.get("lines_vi"):
        errors.append(f"{here}: only a find_mistake question has lines_vi")
    if qtype != "tribulation" and it.get("parts") is not None:
        errors.append(f"{here}: only a tribulation question has parts")
    errors += _tolerance_problems(it, here)
    if qtype in _KEYED_TYPES and answer is not None:
        errors.append(f"{here}: {qtype} questions have no answer key: the order of the data is the answer")
    if qtype == "tribulation":
        if answer is not None:
            errors.append(f"{here}: a tribulation question has no answer of its own: each part has its answer")
        errors += _parts_problems(it.get("parts"), here)
    elif qtype == "matching":
        errors += _pairs_problems(it.get("pairs_vi"), here)
    elif qtype == "ordering":
        errors += _steps_problems(it.get("steps_vi"), here)
    elif qtype == "find_mistake":
        errors += _lines_problems(it.get("lines_vi"), here)
        lines = it.get("lines_vi")
        n = len(lines) if isinstance(lines, (list, tuple)) else 0
        if isinstance(answer, bool) or not isinstance(answer, int) or not 0 <= answer < n:
            errors.append(f"{here}: answer must be the position (from 0) of the one wrong line")
    elif qtype == "true_false":
        if not isinstance(answer, bool):
            errors.append(f"{here}: the answer of a true_false question must be true or false")
    elif qtype == "multiple_choice":
        options = it.get("options_vi")
        if not (isinstance(options, (list, tuple)) and MIN_OPTIONS <= len(options) <= MAX_OPTIONS):
            return errors + [f"{here}: options_vi must list {MIN_OPTIONS} to {MAX_OPTIONS} options"]
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


def draw_problems(spec: GeneratorSpec, item: MathItem) -> list[str]:
    """Problems in one draw of a generator (the same rules as a hand-written item)."""
    raw = {"type": item.qtype, "prompt_vi": item.prompt_vi, "answer": item.answer,
           "solution_vi": list(item.solution_vi), "options_vi": list(item.options_vi),
           "unordered": item.unordered, "matrices": {name: rows for name, rows in item.matrices},
           "pairs_vi": [list(p) for p in item.pairs_vi], "steps_vi": list(item.steps_vi),
           "lines_vi": list(item.lines_vi), "tolerance": item.tolerance}
    return content_problems(raw, f"{spec.id} with {item.numbers}")


def generator_problems(draws: int = 200, config: dict | None = None) -> list[str]:
    """Problems that only show when the generators run: a draw that breaks the rules of an
    item, a seed that does not always give the same question, too few different questions."""
    config = math_path.cfg() if config is None else config
    variety = config["bank_targets"]["generator_variety"]
    errors = []
    for spec in generators().values():
        prints = set()
        for seed in range(draws):
            item = draw(spec, random.Random(seed))
            problems = draw_problems(spec, item)
            if draw(spec, random.Random(seed)) != item:
                problems.append(f"{spec.id}: seed {seed} gives two different questions")
            if problems:
                errors += problems[:3]
                break
            prints.add(item.fingerprint)
        else:
            if len(prints) < min(variety, draws // 2):     # (a short run cannot show the full variety)
                errors.append(f"{spec.id}: {draws} draws give only {len(prints)} different questions, "
                              f"need {variety}")
    return errors


def _shape(text: str) -> str:
    """A prompt with its numbers blanked: two prompts of the same shape differ only in numbers."""
    return re.sub(r"\d+", "#", " ".join(text.casefold().split()))


def question_text(it: dict) -> str | None:
    """Everything that makes a hand-written question what it is: the prompt, and for a
    matching or ordering question its pairs or steps too (two ordering questions may share a
    prompt like "Sắp xếp các bước..." and still be different questions). None when the
    prompt is not text."""
    if not isinstance(it.get("prompt_vi"), str):
        return None
    parts = [it["prompt_vi"]]
    if it.get("type") == "matching" and isinstance(it.get("pairs_vi"), list):
        parts += [str(side) for pair in it["pairs_vi"] if isinstance(pair, list) for side in pair]
    elif it.get("type") == "ordering" and isinstance(it.get("steps_vi"), list):
        parts += [str(step) for step in it["steps_vi"]]
    elif it.get("type") == "find_mistake" and isinstance(it.get("lines_vi"), list):
        parts += [str(line) for line in it["lines_vi"]]
    elif it.get("type") == "tribulation" and isinstance(it.get("parts"), list):
        # one situation may well carry two different tribulations: the parts count as the question
        for part in it["parts"]:
            if isinstance(part, dict):
                parts.append(str(part.get("prompt_vi")))
                options = part.get("options_vi")
                parts += [str(o) for o in options] if isinstance(options, list) else []
    return " | ".join(parts)


def near_duplicates(items: list[dict]) -> list[str]:
    """Pairs of hand-written questions of one micro-skill that are almost the same text once
    digits are ignored: the same question with other numbers is a generator's job."""
    errors = []
    by_skill: dict[str, list[tuple[str, str]]] = {}
    for it in items:
        text = question_text(it)
        if text is not None and isinstance(it.get("id"), str):
            by_skill.setdefault(str(it.get("skill")), []).append((it["id"], _shape(text)))
    for group in by_skill.values():
        for i, (a_id, a) in enumerate(group):
            for b_id, b in group[i + 1:]:
                if difflib.SequenceMatcher(None, a, b).ratio() >= NEAR_DUPLICATE:
                    errors.append(f"{b_id}: is almost the same question as {a_id} (only the numbers differ)")
    return errors


def target_problems(subject: math_path.Subject, raw: dict, config: dict) -> list[str]:
    """A floor that has questions must have enough of them (balance/math.json bank_targets):
    templates and generators per floor, and templates per micro-skill and tier."""
    want = config["bank_targets"]
    errors = []
    slots: dict[tuple[int, str, int], int] = {}
    per_floor: dict[int, list[int]] = {}
    for kind, n_gen in (("items", 0), ("generators", 1)):
        for it in raw.get(kind) or []:
            skill = subject.skills.get(it.get("skill")) if isinstance(it, dict) else None
            if skill is None or it.get("tier") not in math_path.TIERS:
                continue
            slots[(skill.floor, skill.id, it["tier"])] = slots.get((skill.floor, skill.id, it["tier"]), 0) + 1
            count = per_floor.setdefault(skill.floor, [0, 0])
            count[0] += 1
            count[1] += n_gen
    for floor in sorted(per_floor):
        templates, gens = per_floor[floor]
        if templates < want["templates_per_floor"]:
            errors.append(f"floor {floor}: has {templates} templates, need {want['templates_per_floor']}")
        if gens < want["generators_per_floor"]:
            errors.append(f"floor {floor}: has {gens} generators, need {want['generators_per_floor']}")
        for skill in subject.floor(floor).skills:
            for tier in math_path.allowed_tiers(floor, config):
                n = slots.get((floor, skill.id, tier), 0)
                if n < want["per_skill_tier"]:
                    errors.append(f"floor {floor}: {skill.id} has {n} templates at tier {tier}, "
                                  f"need {want['per_skill_tier']}")
    return errors


LADDER_TIERS = (3, 4)               # rule 8: the tiers a rung may have
MIN_RUNGS, MAX_RUNGS = 2, 4


def ladder_problems(subject: math_path.Subject, items: list[dict], gens: list[dict]) -> list[str]:
    """Rule 8: every hand-written tier-5 item has a ladder, and only those (see the module
    docstring). `items` and `gens` are the whole subject (all its files), since a rung may be
    written in another file of the subject than the item it leads to."""
    where: dict[str, tuple[int | None, object]] = {}        # id -> (floor, tier) of every template
    for it in list(items) + list(gens):
        if isinstance(it.get("id"), str):
            skill = subject.skills.get(it.get("skill")) if isinstance(it.get("skill"), str) else None
            where.setdefault(it["id"], (skill.floor if skill else None, it.get("tier")))
    errors = []
    for n, it in enumerate(items, 1):
        here = it["id"] if isinstance(it.get("id"), str) else f"item {n}"
        ladder, tier = it.get("ladder"), it.get("tier")
        if ladder is None:
            if tier == 5 and not isinstance(tier, bool):
                errors.append(f"{here}: a tier-5 question must have a ladder (rule 8): "
                              f"{MIN_RUNGS} to {MAX_RUNGS} ids of tier 3-4 questions that lead to it")
            continue
        if tier != 5 or isinstance(tier, bool):
            errors.append(f"{here}: only a tier-5 question has a ladder")
            continue
        if not (isinstance(ladder, list) and MIN_RUNGS <= len(ladder) <= MAX_RUNGS):
            errors.append(f"{here}: ladder must list {MIN_RUNGS} to {MAX_RUNGS} ids")
            continue
        own_floor = where.get(it.get("id"), (None, None))[0]
        listed: set[str] = set()
        tiers = []
        for rung in ladder:
            if not isinstance(rung, str) or rung not in where:
                errors.append(f"{here}: ladder id {rung!r} is not a question or generator of {subject.id}")
                continue
            if rung == it.get("id"):
                errors.append(f"{here}: ladder lists the question itself")
                continue
            if rung in listed:
                errors.append(f"{here}: ladder lists {rung} twice")
                continue
            listed.add(rung)
            floor, rung_tier = where[rung]
            tiers.append(rung_tier)
            if rung_tier not in LADDER_TIERS or isinstance(rung_tier, bool):
                errors.append(f"{here}: ladder step {rung} is tier {rung_tier}, a step must be tier 3 or 4")
            if floor is not None and own_floor is not None and floor > own_floor:
                errors.append(f"{here}: ladder step {rung} is on floor {floor}, above the question's floor {own_floor}")
        if tiers and 4 not in tiers:
            errors.append(f"{here}: ladder needs at least one tier-4 step")
    return errors


def validate_items(subject: math_path.Subject, raw: dict, config: dict) -> list[str]:
    """Problems in one data/math/items/<subject>.json."""
    from . import math_gen
    errors = [f"unknown key {k!r}" for k in sorted(raw) if not k.startswith("_") and k not in _FILE_KEYS]
    if raw.get("subject") != subject.id:
        errors.append(f"its subject is {raw.get('subject')!r} but the file belongs to {subject.id!r}")
    items = raw.get("items")
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        return errors + ["items: must be a list of questions"]
    gens = raw.get("generators", [])
    if not isinstance(gens, list) or not all(isinstance(g, dict) for g in gens):
        return errors + ["generators: must be a list"]
    seen: set[str] = set()
    prompts: dict[tuple[str, str], str] = {}

    def check_id(it: dict, here: str) -> None:
        iid = it.get("id")
        if not isinstance(iid, str) or not math_path.ID_RE.match(iid):
            errors.append(f"{here}: the id must be 3-40 lowercase letters, digits and _")
        elif iid in seen:
            errors.append(f"{here}: this id is used twice")
        seen.add(iid)

    for n, it in enumerate(items, 1):
        here = it["id"] if isinstance(it.get("id"), str) else f"item {n}"
        for key in sorted(k for k in it if not k.startswith("_") and k not in _ITEM_KEYS):
            errors.append(f"{here}: unknown key {key!r}")
        check_id(it, here)
        errors += _slot_problems(subject, it, config, here)
        errors += content_problems(it, here)
        if isinstance(it.get("prompt_vi"), str) and not text_problem(it["prompt_vi"]):
            key = (it.get("skill"), question_text(it))
            if key in prompts:
                errors.append(f"{here}: has the same question text as {prompts[key]}")
            else:
                prompts[key] = here
    for n, g in enumerate(gens, 1):
        here = g["id"] if isinstance(g.get("id"), str) else f"generator {n}"
        for key in sorted(k for k in g if not k.startswith("_") and k not in _GENERATOR_KEYS):
            errors.append(f"{here}: unknown key {key!r}")
        check_id(g, here)
        errors += _slot_problems(subject, g, config, here)
        if g.get("type") in _KEYED_TYPES or g.get("type") in ("find_mistake", "tribulation"):    # (a Draw has no pairs, steps, lines or parts)
            article = "an" if g["type"] == "ordering" else "a"
            errors.append(f"{here}: {article} {g['type']} question can only be hand-written for now")
        if isinstance(g.get("id"), str) and g["id"] not in math_gen.REGISTRY:
            errors.append(f"{here}: no generator function with this id in learning/math_gen")
    errors += ladder_problems(subject, items, gens)
    errors += near_duplicates(items)
    if not errors:
        errors += target_problems(subject, raw, config)
    return errors


def validate_all(math_dir: Path = MATH_DIR, config: dict | None = None) -> list[str]:
    """Every problem in the item files, each line starting with the file it is in. Run
    after math_path.validate_all() passes: the items are checked against that path."""
    from . import math_gen
    config = math_path.cfg() if config is None else config
    errors: list[str] = []
    index = math_path.load_index(math_dir)
    known = set()
    listed: set[str] = set()
    for entry in sorted((e for e in index["subjects"] if e.get("file")), key=lambda e: e["order"]):
        subject = math_path.build_subject(entry, json.loads((math_dir / entry["file"]).read_text("utf-8")))
        known.add(subject.id)
        files = item_files(subject.id, math_dir)
        if not files:
            continue
        raws, broken = [], False
        for path in files:
            name = f"math/{ITEMS_DIR_NAME}/{path.name}"
            try:
                one = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError) as e:
                errors.append(f"{name}: cannot be read as JSON ({e})")
                broken = True
                continue
            if not isinstance(one, dict):
                errors.append(f"{name}: must be a JSON object")
                broken = True
                continue
            if one.get("subject") != subject.id:
                errors.append(f"{name}: \"subject\" must be {subject.id!r}, the subject the file name says")
                broken = True
                continue
            raws.append(one)
        if broken:
            continue
        # the rules (ids used once, near-duplicates, the targets of a floor) hold for the subject
        # as a whole, so its files are checked as one; a line names the subject's main file
        name = f"math/{ITEMS_DIR_NAME}/{subject.id}.json"
        raw = merge_items(subject.id, raws)
        errors += [f"{name}: {e}" for e in validate_items(subject, raw, config)]
        gens = raw.get("generators")
        listed |= {g.get("id") for g in gens if isinstance(g, dict)} if isinstance(gens, list) else set()
    folder = math_dir / ITEMS_DIR_NAME
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if path.name.split(".")[0] not in known:
            errors.append(f"math/{ITEMS_DIR_NAME}/{path.name}: no written subject has this id")
    if math_dir == MATH_DIR:        # (a test folder lists only the generators it wants to try)
        for gid in sorted(set(math_gen.REGISTRY) - listed):
            errors.append(f"learning/math_gen: generator {gid} is not listed in any math/{ITEMS_DIR_NAME} file")
    return errors
