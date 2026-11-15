#!/usr/bin/env python3
"""Run every automated content check of the math game. A build must not go on when this
fails:

    python tools/check_all.py

Exit code 0 when every check passes, 1 otherwise. The list grows with each milestone
(plan section 6.4). Checks so far:

  * learning path: balance/math.json makes sense (tiers each floor may show, time limits
    per question type and tier, the rule numbers), every floor has 3-6 micro-skills with
    text the game can show, and prerequisites exist, never point to a later floor and
    have no cycle
  * question items (M2): every item of data/math/items/ belongs to a micro-skill, has a
    tier its floor allows and a type with a time limit at that tier; a multiple-choice
    item has exactly one right option and no two options with the same text; a numeric
    answer is a number, a fraction or a list of them; every text can be shown by the game
  * question bank (M3): no two hand-written questions of a micro-skill differ only in
    their numbers; a floor that has questions has enough templates and generators, and
    enough templates for every micro-skill and tier (balance/math.json bank_targets)
  * generators (M3): 200 draws of every generator follow the rules of an item, one seed
    always gives the same question, and the draws are varied enough
  * generated answers (M3): the answer of every one of those draws is recomputed with
    sympy from the numbers that were drawn (tools/math_verify.py; needs
    server/requirements-dev.txt)
  * library (M4): every document of math/library/ parses, covers exactly the micro-skills
    of its floor, and every floor that has questions has its document
  * formula pictures (M4): every $$...$$ has a picture that ships with the game, built
    from that very formula, and small enough to fit the page
  * fonts (M4): every string the game shows, questions and documents included, can really
    be drawn with the two fonts that ship with it
  * programming exercises (M6): every exercise of math/problems/ belongs to a micro-skill
    and a tier its floor allows, has samples and enough hidden tests, and its test data is
    plain ASCII that ends with a newline
  * reference solutions (M6): each exercise's own solution is run on every sample and
    every hidden test, and has to produce exactly the answer that is written down - so a
    sample answer typed by hand and a test answer built by tools/build_problem_tests.py
    can never drift apart from the problem
  * exercise tests have teeth (M6): every exercise is also run with three wrong programs
    (one that prints nothing, one that prints a constant, one that always prints the first
    sample's answer) and none of them may be accepted
"""
from __future__ import annotations

import random
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
sys.path.insert(0, str(ROOT / "tools"))

from app.learning import math_items, math_library, math_path, math_problems  # noqa: E402

FONT_DIR = ROOT / "client" / "assets" / "fonts"
FORMULA_DIR = ROOT / "client" / "assets" / "formulas"
CJK_START = 0x2E80          # the game draws these with Noto, never with the pixel font


def check_learning_path() -> list[str]:
    return math_path.validate_all()


def check_items() -> list[str]:
    if math_path.validate_all():        # items are checked against the path: fix the path first
        return ["skipped: the learning path check above must pass first"]
    return math_items.validate_all()


def check_generators() -> list[str]:
    if math_path.validate_all() or math_items.validate_all():
        return ["skipped: the checks above must pass first"]
    return math_items.generator_problems()


def check_library() -> list[str]:
    if math_path.validate_all():
        return ["skipped: the learning path check above must pass first"]
    return math_library.validate_all()


def check_formulas() -> list[str]:
    if math_library.validate_all():
        return ["skipped: the library check above must pass first"]
    return math_library.manifest_problems(assets_dir=FORMULA_DIR)


def displayed_strings() -> list[tuple[str, str]]:
    """(where, text) for every string the game puts on the screen: the learning path, the
    questions (a few draws of each generator included), the documents and the interface."""
    out: list[tuple[str, str]] = []
    cfg = math_path.cfg()
    for tier, info in math_path._clean(cfg["tiers"]).items():
        out.append((f"balance/math.json tier {tier}", info["name_vi"]))
    for name, q in math_path.question_types(cfg).items():
        out.append((f"balance/math.json {name}", q["name_vi"]))
    for subject in math_path.subjects():
        out.append((f"math/{subject.id}", subject.name_vi))
        for floor in subject.floors:
            out.append((f"math/{subject.id} floor {floor.number}", floor.title_vi))
            for skill in floor.skills:
                out += [(f"math/{subject.id} {skill.id}", skill.name_vi),
                        (f"math/{subject.id} {skill.id}", skill.desc_vi)]
    for item in math_items.bank().values():
        out += [(item.id, t) for t in (item.prompt_vi, *item.solution_vi, *item.options_vi)]
    for spec in math_items.generators().values():
        for seed in range(5):
            drawn = math_items.draw(spec, random.Random(seed))
            out += [(spec.id, t) for t in (drawn.prompt_vi, *drawn.solution_vi, *drawn.options_vi)]
            out += [(spec.id, str(v)) for _, rows in drawn.matrices for row in rows for v in row]
    for doc in math_library.documents().values():
        out += [(doc.id, doc.title_vi), (doc.id, doc.summary_vi)]
        for b in doc.blocks:
            out += [(doc.id, b[k]) for k in ("title_vi", "text", "alt") if b.get(k)]
            out += [(doc.id, item) for item in b.get("items", [])]
            out += [(doc.id, str(v)) for m in b.get("matrices", []) for row in m["rows"] for v in row]
    for p in math_problems.bank().values():
        out += [(p.id, t) for t in (p.title_vi, *p.statement_vi, p.input_vi, p.output_vi, p.limits_vi) if t]
        out += [(p.id, s.note_vi) for s in p.samples if s.note_vi]
        out += [(p.id, s.data) for s in p.samples] + [(p.id, s.expected) for s in p.samples]
    out += [(f"strings_vi.{name}", text) for name, text in _interface_strings()]
    return out


def _interface_strings() -> list[tuple[str, str]]:
    """Every string constant of the game's Vietnamese interface file."""
    sys.path.insert(0, str(ROOT))
    try:
        from client import strings_vi
    except ImportError:
        return []
    finally:
        sys.path.remove(str(ROOT))
    out = []

    def walk(name: str, value) -> None:
        if isinstance(value, str):
            out.append((name, value))
        elif isinstance(value, dict):
            for k, v in value.items():
                walk(f"{name}[{k}]", v)
        elif isinstance(value, (list, tuple, set)):
            for i, v in enumerate(value):
                walk(f"{name}[{i}]", v)
    for name in dir(strings_vi):
        if not name.startswith("_"):
            walk(name, getattr(strings_vi, name))
    return out


def check_fonts() -> list[str]:
    """Every character of every displayed string must be in one of the two fonts that ship
    with the game, the way client/engine/text.py picks between them."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError as e:
        return [f"cannot read the fonts: {e} (pip install -r server/requirements-dev.txt)"]
    fonts = {"VT323-Regular.ttf": set(), "NotoSansSC-Game.otf": set()}
    for name in fonts:
        path = FONT_DIR / name
        if not path.is_file():
            return [f"client/assets/fonts/{name} is missing (run python tools/fetch_assets.py)"]
        fonts[name] = set(TTFont(path, fontNumber=0, lazy=True).getBestCmap())
    pixel, han = fonts["VT323-Regular.ttf"], fonts["NotoSansSC-Game.otf"]
    seen: set[str] = set()
    errors = []
    for where, text in displayed_strings():
        for ch in text:
            if ch in seen or ch.isspace():
                continue
            seen.add(ch)
            code = ord(ch)
            if (code < CJK_START and code in pixel) or code in han:
                continue
            errors.append(f"{where}: no font draws {ch!r} (U+{code:04X}), the game would show a box")
    return errors


def check_problems() -> list[str]:
    if math_path.validate_all():
        return ["skipped: the learning path check above must pass first"]
    return math_problems.validate_all()


def check_problem_solutions() -> list[str]:
    """Run every exercise's reference solution on every test it has. The sample answers are
    written by hand, so this is a real check of the solution; the hidden answers come from
    the solution, so this catches a test or a solution that changed without the other."""
    if math_problems.validate_all():
        return ["skipped: the exercise check above must pass first"]
    sys.path.insert(0, str(ROOT))
    try:
        from client.engine import coderun
    except ImportError as e:
        return [f"cannot run the solutions: {e}"]
    finally:
        sys.path.remove(str(ROOT))
    errors = []
    for problem in math_problems.bank().values():
        path = math_problems.solution_path(problem.subject, problem.id)
        for group, tests in (("ví dụ", problem.samples), ("test ẩn", problem.tests)):
            for n, test in enumerate(tests, 1):
                result = coderun.run_one(path, test.data, problem.time_limit_ms)
                where = f"{problem.id} {group} {n}"
                if not result.ok:
                    errors.append(f"{where}: the reference solution gave {result.status.upper()} "
                                  f"{result.error.strip()[:120]}")
                    continue
                if not math_problems.same_output(test.expected, result.output, problem.checker):
                    errors.append(f"{where}: the reference solution printed "
                                  f"{result.output.strip()[:60]!r}, the answer says "
                                  f"{test.expected.strip()[:60]!r}")
    return errors


#: programs that must never be accepted. (name, how to build the source from a problem)
MUTANTS = [
    ("chương trình rỗng", lambda p: "pass\n"),
    ("in ra một hằng số", lambda p: "print(0)\n"),
    # the sharpest one: print the first sample's answer whatever the input is. It passes only
    # if every hidden test happens to have that same answer, i.e. if the tests test nothing.
    ("in đáp án của ví dụ 1", lambda p: f"import sys\nsys.stdout.write({p.samples[0].expected!r})\n"),
]


def check_problem_tests_have_teeth() -> list[str]:
    """A test set that any old program passes is not a test set. Every exercise is run with
    three deliberately wrong programs, and none of them may come out AC."""
    if math_problems.validate_all():
        return ["skipped: the exercise check above must pass first"]
    sys.path.insert(0, str(ROOT))
    try:
        from client.engine import coderun
    except ImportError as e:
        return [f"cannot run the solutions: {e}"]
    finally:
        sys.path.remove(str(ROOT))
    errors = []
    with tempfile.TemporaryDirectory(prefix="kvtt_mutants_") as tmp:
        path = Path(tmp) / "bai_lam.py"
        for problem in math_problems.bank().values():
            answers = {t.expected.strip() for t in problem.tests}
            if len(answers) == 1:
                errors.append(f"{problem.id}: every hidden test wants the same answer "
                              f"({answers.pop()[:40]!r}), so they cannot tell solutions apart")
            for name, build in MUTANTS:
                coderun.write_solution(path, build(problem))
                attempt = coderun.run_tests(path, [t.data for t in problem.tests],
                                            problem.time_limit_ms)
                verdict = math_problems.judge(list(problem.tests), attempt.outputs, attempt.status,
                                              attempt.times_ms, problem.checker, attempt.error)
                if verdict.accepted:
                    errors.append(f"{problem.id}: a program that only {name} is accepted; "
                                  f"the hidden tests do not test anything")
    return errors


def check_generated_answers() -> list[str]:
    if math_path.validate_all() or math_items.validate_all():
        return ["skipped: the checks above must pass first"]
    try:
        import math_verify
    except ImportError as e:
        return [f"cannot recompute the answers: {e} (pip install -r server/requirements-dev.txt)"]
    return math_verify.verify_all()


# (name, function returning one line per problem; an empty list means the check passed)
CHECKS = [
    ("learning path: tiers per floor, time limits, micro-skill prerequisites", check_learning_path),
    ("question bank: items valid, no near-duplicates, enough templates per floor, skill and tier", check_items),
    ("generators: every draw is a valid question, same seed same question, enough variety", check_generators),
    ("generated answers: recomputed with sympy", check_generated_answers),
    ("library: documents parse and cover the micro-skills of their floor", check_library),
    ("formula pictures: one per formula, built from it, small enough for the page", check_formulas),
    ("programming exercises: statements, samples and hidden tests are well formed", check_problems),
    ("reference solutions: every exercise's own solution reproduces every answer", check_problem_solutions),
    ("exercise tests have teeth: no wrong program is accepted", check_problem_tests_have_teeth),
    ("fonts: every string the game shows can be drawn", check_fonts),
]


def main(argv: list[str] | None = None) -> int:
    failed = 0
    for name, check in CHECKS:
        errors = check()
        print(f"[{'FAIL' if errors else ' OK '}] {name}")
        for e in errors:
            print(f"         - {e}")
        failed += bool(errors)
    print(f"{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):   # problem lines may quote Vietnamese text
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
