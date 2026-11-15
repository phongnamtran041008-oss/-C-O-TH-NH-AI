"""Programming exercises: the statements, the hidden tests and the marking (milestone M6,
plan 5.2).

An exercise belongs to one micro-skill and one tier, like every other question, so the
floors keep deciding what a player may be asked. It carries:

  * the statement, the input and output format, the constraints - all Vietnamese;
  * **samples**: input, expected output and a word of explanation. Public: the game shows
    them, and "Chạy thử" runs the player's program on them so they can see what happens;
  * **tests**: the hidden ones. Their input is handed out at "Nộp bài" (the program has to
    run somewhere), but their expected output never leaves the server;
  * a **reference solution**, `problems/<subject>/<id>.py`, which never leaves the server
    either. tools/check_all.py runs it on every test to prove the expected output is right.

Marking is here because only the server has the expected output. The learner's program runs
on the learner's own machine (client/engine/coderun.py) and sends back what it printed;
this module compares and says AC / WA / TLE / RE / CE. The game is for one learner and
their friends, so a doctored client could claim a verdict it did not earn - that is a
cheat against yourself, and the hidden answers still stay hidden either way.

Pure data and rules, like math_path and math_items: no database here.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from . import math_path
from .math_path import ID_RE, MATH_DIR, text_problem

PROBLEMS_DIR_NAME = "problems"
PROBLEMS_DIR = MATH_DIR / PROBLEMS_DIR_NAME
AC, WA, TLE, RE, CE = "AC", "WA", "TLE", "RE", "CE"
NOT_RUN = "-"               # a test the program never reached: it had already crashed or timed out
VERDICTS = (AC, WA, TLE, RE, CE)
RUN_STATUS = {"ok": None, "tle": TLE, "re": RE, "ce": CE}      # coderun status -> verdict
CHECKERS = ("exact", "float")
MAX_LINE = 200              # a statement line the reading panel can still lay out

_FILE_KEYS = {"subject", "problems"}
_PROBLEM_KEYS = {"id", "skill", "tier", "title_vi", "statement_vi", "input_vi", "output_vi",
                 "limits_vi", "checker", "time_limit_ms", "samples", "tests", "reviewed"}
_TEST_KEYS = {"in", "out", "note_vi"}


# ------------------------------------------------------------------ the data
@dataclass(frozen=True)
class Test:
    data: str
    expected: str
    note_vi: str = ""

    def view(self) -> dict:
        """What the game may see of a sample test."""
        return {"in": self.data, "out": self.expected, "note_vi": self.note_vi}


@dataclass(frozen=True)
class Problem:
    id: str
    subject: str
    skill: str
    floor: int
    tier: int
    title_vi: str
    statement_vi: tuple[str, ...]
    input_vi: str
    output_vi: str
    limits_vi: str
    checker: str
    time_limit_ms: int
    samples: tuple[Test, ...]
    tests: tuple[Test, ...]
    reviewed: bool = False

    def view(self, config: dict | None = None) -> dict:
        """The statement as the game gets it: samples yes, hidden tests never."""
        config = config or math_path.cfg()
        subject = math_path.subject(self.subject)
        return {"id": self.id, "subject": self.subject, "subject_name_vi": subject.name_vi,
                "skill": self.skill, "skill_name_vi": subject.skills[self.skill].name_vi,
                "floor": self.floor, "tier": self.tier,
                "tier_name_vi": config["tiers"][str(self.tier)]["name_vi"],
                "title_vi": self.title_vi, "statement_vi": list(self.statement_vi),
                "input_vi": self.input_vi, "output_vi": self.output_vi, "limits_vi": self.limits_vi,
                "checker": self.checker, "time_limit_ms": self.time_limit_ms,
                "samples": [s.view() for s in self.samples], "tests": len(self.tests),
                "think_limit_s": math_path.time_limit("programming", self.tier, config),
                "reviewed": self.reviewed}

    def brief(self) -> dict:
        """One line of the exercise list."""
        return {"id": self.id, "title_vi": self.title_vi, "skill": self.skill, "floor": self.floor,
                "tier": self.tier, "tests": len(self.tests), "reviewed": self.reviewed}


def solution_path(subject_id: str, problem_id: str, math_dir: Path = MATH_DIR) -> Path:
    """The reference solution. Server side only - it is never put in any answer."""
    return math_dir / PROBLEMS_DIR_NAME / subject_id / f"{problem_id}.py"


def _read(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def problems_path(subject_id: str, math_dir: Path = MATH_DIR) -> Path:
    return math_dir / PROBLEMS_DIR_NAME / f"{subject_id}.json"


def build_test(raw: dict) -> Test:
    return Test(data=raw["in"], expected=raw["out"], note_vi=raw.get("note_vi", ""))


def build_problem(subject: math_path.Subject, raw: dict, config: dict) -> Problem:
    skill = subject.skills[raw["skill"]]
    return Problem(id=raw["id"], subject=subject.id, skill=skill.id, floor=skill.floor,
                   tier=raw["tier"], title_vi=raw["title_vi"],
                   statement_vi=tuple(raw["statement_vi"]), input_vi=raw["input_vi"],
                   output_vi=raw["output_vi"], limits_vi=raw.get("limits_vi", ""),
                   checker=raw.get("checker", "exact"),
                   time_limit_ms=int(raw.get("time_limit_ms", config["programming"]["time_limit_ms"])),
                   samples=tuple(build_test(t) for t in raw["samples"]),
                   tests=tuple(build_test(t) for t in raw["tests"]),
                   reviewed=bool(raw.get("reviewed", False)))


@lru_cache(maxsize=1)
def bank() -> dict[str, Problem]:
    """Every exercise that is written, by id, in subject and floor order."""
    config = math_path.cfg()
    out: dict[str, Problem] = {}
    for subject in math_path.subjects():
        path = problems_path(subject.id)
        if not path.is_file():
            continue
        for raw in _read(path).get("problems", []):
            try:
                problem = build_problem(subject, raw, config)
            except (KeyError, TypeError, ValueError):
                continue                        # validate_all reports it properly
            out[problem.id] = problem
    return dict(sorted(out.items(), key=lambda kv: (kv[1].subject, kv[1].floor, kv[1].tier, kv[0])))


def problem(problem_id: str) -> Problem:
    try:
        return bank()[problem_id]
    except KeyError:
        raise KeyError(f"no programming exercise {problem_id!r}")


def floor_problems(subject_id: str, floor: int, allow_unreviewed: bool) -> list[Problem]:
    return [p for p in bank().values() if p.subject == subject_id and p.floor == floor
            and (allow_unreviewed or p.reviewed)]


# ------------------------------------------------------------------ marking
def tokens(text: str) -> list[str]:
    return str(text).split()


def _as_float(token: str) -> float | None:
    try:
        value = float(token)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def same_output(expected: str, given: str, checker: str = "exact",
                tolerance: float | None = None) -> bool:
    """Is this output right? Whitespace never counts: both sides are compared token by
    token, so trailing spaces, blank lines and \\r\\n are all fine. With the "float"
    checker two tokens that are both numbers may differ by `tolerance` (plan 5.2: about
    1e-6), relative to the larger one once the numbers get big."""
    want, got = tokens(expected), tokens(given)
    if len(want) != len(got):
        return False
    if checker == "exact":
        return want == got
    tolerance = math_path.cfg()["programming"]["tolerance"] if tolerance is None else tolerance
    for a, b in zip(want, got):
        if a == b:
            continue
        x, y = _as_float(a), _as_float(b)
        if x is None or y is None:
            return False
        if abs(x - y) > tolerance * max(1.0, abs(x)):
            return False
    return True


@dataclass(frozen=True)
class TestResult:
    index: int                      # 1-based, the way the game numbers them
    verdict: str
    ms: int = 0

    @property
    def passed(self) -> bool:
        return self.verdict == AC

    def view(self) -> dict:
        return {"test": self.index, "verdict": self.verdict, "ms": self.ms}


@dataclass(frozen=True)
class Judgement:
    verdict: str
    passed: int
    total: int
    results: tuple[TestResult, ...]
    error: str = ""                 # the compile error or the crash, as the player's run saw it

    @property
    def accepted(self) -> bool:
        return self.verdict == AC

    @property
    def share(self) -> float:
        """How much of the exercise is done, which is what the reward follows."""
        return (self.passed / self.total) if self.total else 0.0

    @property
    def ms(self) -> int:
        return max((r.ms for r in self.results), default=0)

    def view(self) -> dict:
        return {"verdict": self.verdict, "passed": self.passed, "total": self.total,
                "share": round(self.share, 4), "ms": self.ms, "error": self.error,
                "tests": [r.view() for r in self.results]}


def judge(tests: list[Test], outputs: list[str], status: str = "ok", times_ms: list[int] | None = None,
          checker: str = "exact", error: str = "", tolerance: float | None = None) -> Judgement:
    """The verdict of one submission. `status` is what the run itself reported ("ok", or
    "ce"/"re"/"tle" when it never got through every test); the tests that did run are still
    compared, so a program that solves four tests and then crashes is told exactly that.

    AC only when every test is right and nothing went wrong on the way."""
    if status == "ce":
        return Judgement(CE, 0, len(tests), tuple(TestResult(i + 1, CE) for i in range(len(tests))), error)
    times_ms = times_ms or []
    stop = RUN_STATUS.get(status)               # None when the program got through every test
    broke_at = len(outputs) - 1 if stop else -1     # the last test it tried is the one that broke
    results: list[TestResult] = []
    for i, test in enumerate(tests):
        ms = times_ms[i] if i < len(times_ms) else 0
        if i == broke_at:
            results.append(TestResult(i + 1, stop, ms))
        elif i < len(outputs):
            ok = same_output(test.expected, outputs[i], checker, tolerance)
            results.append(TestResult(i + 1, AC if ok else WA, ms))
        else:                                   # no answer for this test
            results.append(TestResult(i + 1, NOT_RUN if stop else WA, ms))
    passed = sum(1 for r in results if r.passed)
    verdict = AC if passed == len(tests) and len(tests) else next(
        (r.verdict for r in results if not r.passed), WA)
    return Judgement(verdict, passed, len(tests), tuple(results), error)


# ------------------------------------------------------------------ validation
def _unknown_keys(obj: dict, allowed: set[str]) -> list[str]:
    return sorted(k for k in obj if not k.startswith("_") and k not in allowed)


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def io_problem(value, what: str) -> str | None:
    """Test data and expected output are plain ASCII text: they go through stdin and stdout
    of another program, so anything else is asking for trouble on some machine."""
    if not isinstance(value, str) or not value.strip():
        return f"{what} is missing or empty"
    if not value.isascii():
        return f"{what} has characters that are not ASCII"
    if "\r" in value:
        return f"{what} has a carriage return; write the lines with \\n"
    if not value.endswith("\n"):
        return f"{what} must end with a newline"
    return None


def validate_problem(subject: math_path.Subject, raw: dict, config: dict,
                     math_dir: Path = MATH_DIR) -> list[str]:
    errors: list[str] = []
    pid = raw.get("id")
    here = f"{pid}"
    for key in _unknown_keys(raw, _PROBLEM_KEYS):
        errors.append(f"{here}: unknown key {key!r}")
    if not isinstance(pid, str) or not ID_RE.match(pid):
        return errors + [f"{pid!r}: the id must be 3-40 lowercase letters, digits and _"]

    skill_id = raw.get("skill")
    skill = subject.skills.get(skill_id) if isinstance(skill_id, str) else None
    if skill is None:
        errors.append(f"{here}: skill {skill_id!r} is not a micro-skill of {subject.id}")
    tier = raw.get("tier")
    if not _is_int(tier) or tier not in math_path.TIERS:
        errors.append(f"{here}: tier must be a whole number 1-{math_path.TOP_TIER}")
    elif skill is not None and not math_path.tier_allowed(skill.floor, tier, config):
        lo, hi = math_path.floor_tiers(skill.floor, config)
        errors.append(f"{here}: tier {tier} is outside floor {skill.floor} (bậc {lo}-{hi})")
    elif math_path.time_limit("programming", tier, config) is None:
        errors.append(f"{here}: a programming exercise has no time limit at tier {tier}")

    for field in ("title_vi", "input_vi", "output_vi"):
        problem_text = text_problem(raw.get(field))
        if problem_text:
            errors.append(f"{here}: {field} {problem_text}")
    if raw.get("limits_vi") and text_problem(raw["limits_vi"]):
        errors.append(f"{here}: limits_vi {text_problem(raw['limits_vi'])}")
    lines = raw.get("statement_vi")
    if not isinstance(lines, list) or not lines:
        errors.append(f"{here}: statement_vi must be a list of paragraphs")
    else:
        for n, line in enumerate(lines, 1):
            problem_text = text_problem(line)
            if problem_text:
                errors.append(f"{here}: statement_vi line {n} {problem_text}")
            elif len(line) > MAX_LINE * 4:
                errors.append(f"{here}: statement_vi line {n} is very long; split it into paragraphs")

    checker = raw.get("checker", "exact")
    if checker not in CHECKERS:
        errors.append(f"{here}: checker must be one of {', '.join(CHECKERS)}")
    limit = raw.get("time_limit_ms", config["programming"]["time_limit_ms"])
    if not _is_int(limit) or not 100 <= limit <= config["programming"]["max_time_limit_ms"]:
        errors.append(f"{here}: time_limit_ms must be 100..{config['programming']['max_time_limit_ms']}")

    for group, least in (("samples", 1), ("tests", config["programming"]["min_tests"])):
        tests = raw.get(group)
        if not isinstance(tests, list) or len(tests) < least:
            errors.append(f"{here}: {group} needs at least {least} test(s)")
            continue
        for n, test in enumerate(tests, 1):
            where = f"{here}: {group}[{n}]"
            if not isinstance(test, dict):
                errors.append(f"{where} must be an object with \"in\" and \"out\"")
                continue
            for key in _unknown_keys(test, _TEST_KEYS):
                errors.append(f"{where}: unknown key {key!r}")
            if group == "tests" and test.get("note_vi"):
                errors.append(f"{where}: only a sample may explain itself (note_vi)")
            for field in ("in", "out"):
                problem_text = io_problem(test.get(field), field)
                if problem_text:
                    errors.append(f"{where}: {problem_text}")
            if test.get("note_vi") and text_problem(test["note_vi"]):
                errors.append(f"{where}: note_vi {text_problem(test['note_vi'])}")

    path = solution_path(subject.id, pid, math_dir)
    if not path.is_file():
        errors.append(f"{here}: the reference solution {path.parent.name}/{path.name} is missing")
    else:
        try:
            compile(path.read_text("utf-8"), path.name, "exec")
        except (SyntaxError, ValueError) as e:
            errors.append(f"{here}: the reference solution does not compile ({e})")
    return errors


def validate_subject(subject: math_path.Subject, raw: dict, config: dict,
                     math_dir: Path = MATH_DIR) -> list[str]:
    errors: list[str] = []
    for key in _unknown_keys(raw, _FILE_KEYS):
        errors.append(f"unknown key {key!r}")
    if raw.get("subject") != subject.id:
        errors.append(f"its subject is {raw.get('subject')!r} but the file is {subject.id}.json")
    problems = raw.get("problems")
    if not isinstance(problems, list) or not problems:
        return errors + ["problems: is missing or empty"]
    seen: set[str] = set()
    for p in problems:
        if not isinstance(p, dict):
            errors.append("every exercise must be an object")
            continue
        if p.get("id") in seen:
            errors.append(f"{p.get('id')}: this id is used twice")
        seen.add(p.get("id"))
        errors += validate_problem(subject, p, config, math_dir)
    return errors


def validate_all(math_dir: Path = MATH_DIR, config: dict | None = None) -> list[str]:
    """Every problem in the exercises, one readable line each."""
    config = config or math_path.cfg()      # the caller checks the learning path first
    errors: list[str] = []
    ids: set[str] = set()
    for subject in math_path.subjects():
        path = problems_path(subject.id, math_dir)
        if not path.is_file():
            continue
        try:
            raw = _read(path)
        except (OSError, ValueError) as e:
            errors.append(f"problems/{path.name}: cannot be read as JSON ({e})")
            continue
        if not isinstance(raw, dict):
            errors.append(f"problems/{path.name}: must be a JSON object")
            continue
        errors += [f"problems/{path.name}: {e}" for e in validate_subject(subject, raw, config, math_dir)]
        for p in raw.get("problems") or []:
            pid = p.get("id") if isinstance(p, dict) else None
            if pid in ids:
                errors.append(f"problems/{path.name}: {pid} is already an exercise of another subject")
            ids.add(pid)
    stray = {p.stem for p in (math_dir / PROBLEMS_DIR_NAME).glob("*/*.py")} - ids
    for name in sorted(stray):
        errors.append(f"problems/: {name}.py is a solution with no exercise")
    return errors
