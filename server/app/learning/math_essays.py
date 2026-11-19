"""Luận Đạo Đài: the essay and proof problems, their rubrics and the marking rule
(docs/LUAN_DAO_DAI.md).

These are the written-exam questions the main path leaves out on purpose: prove it, or
compute it and show the reasoning. They are optional and gate nothing. An essay carries:

  * the statement, a word on why it matters for AI, and hints - shown before the learner
    writes anything (`Essay.public_view`);
  * a **model solution**, a **rubric** that always adds up to 10 and the **fatal mistakes**
    - handed out only once the learner has submitted an answer (`Essay.marking_view`),
    like the expected output of a programming exercise.

Three kinds of marker use the same rubric: the learner (tu_cham), a language model called
with the learner's own key from the learner's machine (ai), or a friend (dong_dao). A marker
only says, for each rubric item, whether the answer has it in full, in part or not at all,
and whether a fatal mistake was made. **The points are added up here**, never by the
marker: a model that is asked for a total gives a generous one.

Not wired into the game yet: no route and no table uses this module. Pure data and rules,
like math_path and math_problems: no database here.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .math_path import ID_RE, MATH_DIR, text_problem

ESSAYS_DIR_NAME = "essays"
SUBJECT_PREFIX = {"dai_so_tuyen_tinh": "ds", "giai_tich": "gt", "xac_suat_thong_ke": "xs",
                  "toi_uu_roi_rac": "tr"}
KINDS = ("chung_minh", "tinh_co_lap_luan", "phat_bieu_chung_minh", "phan_bien")
LEVELS = (1, 2, 3)
RUBRIC_TOTAL = 10
FULL, PART, NONE = "du", "mot_phan", "khong"
SHARE = {FULL: 1.0, PART: 0.5, NONE: 0.0}
MARKS = tuple(SHARE)
FATAL_CAP = 4.0             # a fatal mistake: the essay is worth at most this, whatever else it has
MARKERS = ("tu_cham", "ai", "dong_dao")
MAX_LINE = 260              # a line the reading panel can still lay out
MIN_RUBRIC_ITEMS = 3
MAX_ANSWER_CHARS = 8000     # about four handwritten pages; longer is not an exam answer
# Đạo tâm for a full-mark essay of each level. My values, for the author to change.
DAO_TAM = {1: 10, 2: 20, 3: 30}

_FILE_KEYS = {"subject", "wired", "essays"}
_ESSAY_KEYS = {"id", "node", "kind", "level", "minutes", "title_vi", "statement_vi", "why_vi",
               "hints_vi", "solution_vi", "rubric", "fatal_vi", "reviewed"}
_RUBRIC_KEYS = {"id", "points", "need_vi"}


# ------------------------------------------------------------------ the data
@dataclass(frozen=True)
class RubricItem:
    id: str
    points: int
    need_vi: str

    def view(self) -> dict:
        return {"id": self.id, "points": self.points, "need_vi": self.need_vi}


@dataclass(frozen=True)
class Essay:
    id: str
    subject: str
    node: str                       # the node of the curriculum tree it belongs to
    kind: str
    level: int
    minutes: int
    title_vi: str
    statement_vi: str
    why_vi: str
    hints_vi: tuple[str, ...]
    solution_vi: tuple[str, ...]
    rubric: tuple[RubricItem, ...]
    fatal_vi: tuple[str, ...]
    reviewed: bool = False

    def brief(self) -> dict:
        """One line of the essay list."""
        return {"id": self.id, "node": self.node, "kind": self.kind, "level": self.level,
                "minutes": self.minutes, "title_vi": self.title_vi, "reviewed": self.reviewed}

    def public_view(self) -> dict:
        """What the learner sees before answering. No solution, no rubric: the rubric says
        what the proof needs, so showing it first would give the proof away."""
        return {**self.brief(), "subject": self.subject, "statement_vi": self.statement_vi,
                "why_vi": self.why_vi, "hints_vi": list(self.hints_vi),
                "max_points": RUBRIC_TOTAL}

    def marking_view(self) -> dict:
        """What a marker needs. Only for a learner who has already submitted an answer."""
        return {**self.public_view(), "solution_vi": list(self.solution_vi),
                "rubric": [item.view() for item in self.rubric],
                "fatal_vi": list(self.fatal_vi), "fatal_cap": FATAL_CAP}


def essays_path(subject_id: str, math_dir: Path = MATH_DIR) -> Path:
    return math_dir / ESSAYS_DIR_NAME / f"{subject_id}.json"


def _read(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def build_essay(subject_id: str, raw: dict) -> Essay:
    return Essay(id=raw["id"], subject=subject_id, node=raw["node"], kind=raw["kind"],
                 level=raw["level"], minutes=raw["minutes"], title_vi=raw["title_vi"],
                 statement_vi=raw["statement_vi"], why_vi=raw["why_vi"],
                 hints_vi=tuple(raw["hints_vi"]), solution_vi=tuple(raw["solution_vi"]),
                 rubric=tuple(RubricItem(id=item["id"], points=item["points"], need_vi=item["need_vi"])
                              for item in raw["rubric"]),
                 fatal_vi=tuple(raw["fatal_vi"]), reviewed=bool(raw.get("reviewed", False)))


def load_bank(math_dir: Path = MATH_DIR) -> dict[str, Essay]:
    out: dict[str, Essay] = {}
    for subject_id in SUBJECT_PREFIX:
        path = essays_path(subject_id, math_dir)
        if not path.is_file():
            continue
        for raw in _read(path).get("essays", []):
            try:
                essay = build_essay(subject_id, raw)
            except (KeyError, TypeError, ValueError):
                continue                        # validate_all reports it properly
            out[essay.id] = essay
    return dict(sorted(out.items(), key=lambda kv: (kv[1].subject, kv[1].level, kv[0])))


@lru_cache(maxsize=1)
def bank() -> dict[str, Essay]:
    """Every essay that is written, by id, in subject and level order."""
    return load_bank()


def essay(essay_id: str) -> Essay:
    try:
        return bank()[essay_id]
    except KeyError:
        raise KeyError(f"no essay {essay_id!r}")


def open_essays(done_nodes: set[str], allow_unreviewed: bool) -> list[Essay]:
    """The essays a learner may take: those of the tree nodes they have finished. One
    discusses a notion only after having learnt it."""
    return [e for e in bank().values() if e.node in done_nodes and (allow_unreviewed or e.reviewed)]


# ------------------------------------------------------------------ marking
def clean_marks(essay: Essay, marks: dict) -> dict[str, str]:
    """A marker's word on every rubric item. An item the marker left out, or answered with
    anything but du / mot_phan / khong, counts as khong: no evidence, no points."""
    marks = marks if isinstance(marks, dict) else {}
    return {item.id: (marks.get(item.id) if marks.get(item.id) in SHARE else NONE)
            for item in essay.rubric}


def score(essay: Essay, marks: dict, fatal: bool = False) -> float:
    """The mark out of 10. Full points for du, half for mot_phan; a fatal mistake caps the
    essay at FATAL_CAP."""
    clean = clean_marks(essay, marks)
    total = sum(item.points * SHARE[clean[item.id]] for item in essay.rubric)
    return min(total, FATAL_CAP) if fatal else total


def dao_tam(essay: Essay, points: float, best_before: float = 0.0) -> int:
    """Đạo tâm earned by this marking: the level's worth times the share of the 10 points,
    and only for the improvement over the learner's best so far (as M6 pays for programming
    exercises), so marking the same answer again earns nothing."""
    worth = DAO_TAM[essay.level]
    now = round(worth * max(0.0, min(points, RUBRIC_TOTAL)) / RUBRIC_TOTAL)
    before = round(worth * max(0.0, min(best_before, RUBRIC_TOTAL)) / RUBRIC_TOTAL)
    return max(0, now - before)


def answer_problem(answer) -> str | None:
    """Why an answer cannot be marked, or None."""
    if not isinstance(answer, str) or not answer.strip():
        return "empty"
    if len(answer) > MAX_ANSWER_CHARS:
        return "too_long"
    return None


@dataclass(frozen=True)
class Marking:
    """One marked essay, as the game shows it and as it would be stored."""
    essay: str
    marker: str
    marks: dict[str, str]
    fatal: bool
    points: float
    dao_tam: int

    def view(self) -> dict:
        return {"essay": self.essay, "marker": self.marker, "marks": dict(self.marks),
                "fatal": self.fatal, "points": self.points, "max_points": RUBRIC_TOTAL,
                "dao_tam": self.dao_tam}


def mark(essay: Essay, marker: str, marks: dict, fatal: bool = False,
         best_before: float = 0.0) -> Marking:
    if marker not in MARKERS:
        raise ValueError(f"marker must be one of {', '.join(MARKERS)}")
    points = score(essay, marks, bool(fatal))
    return Marking(essay=essay.id, marker=marker, marks=clean_marks(essay, marks),
                   fatal=bool(fatal), points=points, dao_tam=dao_tam(essay, points, best_before))


# ------------------------------------------------------------------ checking the data
def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _lines(raw: dict, key: str, here: str, errors: list[str], needed: bool = True) -> None:
    lines = raw.get(key)
    if not isinstance(lines, list) or (needed and not lines):
        errors.append(f"{here}: {key} must be a list of sentences")
        return
    for n, line in enumerate(lines, 1):
        problem = text_problem(line)
        if problem:
            errors.append(f"{here}: {key} line {n} {problem}")
        elif len(line) > MAX_LINE:
            errors.append(f"{here}: {key} line {n} has {len(line)} characters, at most {MAX_LINE}")


def validate_essay(subject_id: str, raw: dict, nodes: set[str] | None = None) -> list[str]:
    """Problems in one essay. `nodes` is the set of node ids of the curriculum tree, when the
    tree is at hand: the tree is not part of this module's data."""
    errors: list[str] = []
    essay_id = raw.get("id")
    here = f"{essay_id}"
    prefix = SUBJECT_PREFIX[subject_id]
    if not isinstance(essay_id, str) or not ID_RE.match(essay_id):
        return [f"{essay_id!r}: the id must be 3-40 lowercase letters, digits and _"]
    if not essay_id.startswith(f"{prefix}_tl_"):
        errors.append(f"{here}: an essay of {subject_id} is named {prefix}_tl_<name>")
    for key in sorted(_ESSAY_KEYS - raw.keys()):
        errors.append(f"{here}: missing {key}")
    for key in sorted(k for k in raw if not k.startswith("_") and k not in _ESSAY_KEYS):
        errors.append(f"{here}: unknown key {key}")

    node = raw.get("node")
    if not isinstance(node, str) or not node.startswith(f"{prefix}_"):
        errors.append(f"{here}: node {node!r} is not a node of {subject_id}")
    elif nodes is not None and node not in nodes:
        errors.append(f"{here}: node {node!r} is not in the curriculum tree")
    if raw.get("kind") not in KINDS:
        errors.append(f"{here}: kind must be one of {', '.join(KINDS)}")
    if not _is_int(raw.get("level")) or raw.get("level") not in LEVELS:
        errors.append(f"{here}: level must be 1, 2 or 3")
    if not _is_int(raw.get("minutes")) or not 3 <= raw["minutes"] <= 60:
        errors.append(f"{here}: minutes must be a whole number from 3 to 60")
    if not isinstance(raw.get("reviewed", False), bool):
        errors.append(f"{here}: reviewed must be true or false")
    for key in ("title_vi", "statement_vi", "why_vi"):
        problem = text_problem(raw.get(key))
        if problem:
            errors.append(f"{here}: {key} {problem}")
    for key in ("hints_vi", "solution_vi", "fatal_vi"):
        _lines(raw, key, here, errors)

    rubric = raw.get("rubric")
    if not isinstance(rubric, list) or len(rubric) < MIN_RUBRIC_ITEMS:
        errors.append(f"{here}: the rubric needs at least {MIN_RUBRIC_ITEMS} items")
        return errors
    ids: list[str] = []
    total = 0
    for item in rubric:
        if not isinstance(item, dict) or set(item) != _RUBRIC_KEYS:
            errors.append(f"{here}: a rubric item has exactly id, points, need_vi")
            continue
        ids.append(item["id"])
        if not _is_int(item["points"]) or item["points"] < 1:
            errors.append(f"{here}: rubric {item['id']} must be worth a whole number of points")
        else:
            total += item["points"]
        problem = text_problem(item["need_vi"])
        if problem:
            errors.append(f"{here}: rubric {item['id']} need_vi {problem}")
    if len(set(ids)) != len(ids):
        errors.append(f"{here}: rubric ids repeat")
    if total != RUBRIC_TOTAL:
        errors.append(f"{here}: the rubric adds up to {total}, not {RUBRIC_TOTAL}")
    return errors


def validate_all(math_dir: Path = MATH_DIR, nodes: set[str] | None = None) -> list[str]:
    """Problems in the whole essay bank."""
    errors: list[str] = []
    seen: set[str] = set()
    for subject_id in SUBJECT_PREFIX:
        path = essays_path(subject_id, math_dir)
        if not path.is_file():
            continue
        try:
            data = _read(path)
        except ValueError as exc:
            errors.append(f"{path.name}: not valid JSON ({exc})")
            continue
        for key in sorted(k for k in data if not k.startswith("_") and k not in _FILE_KEYS):
            errors.append(f"{path.name}: unknown key {key}")
        if data.get("subject") != subject_id:
            errors.append(f"{path.name}: subject is {data.get('subject')!r}")
        for raw in data.get("essays", []):
            if not isinstance(raw, dict):
                errors.append(f"{path.name}: an essay must be an object")
                continue
            errors += [f"{path.name}: {line}" for line in validate_essay(subject_id, raw, nodes)]
            if raw.get("id") in seen:
                errors.append(f"{path.name}: {raw.get('id')} is used twice")
            seen.add(raw.get("id"))
    return errors
