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

import json
import random
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
sys.path.insert(0, str(ROOT / "tools"))

from app.learning import math_items, math_library, math_path, math_problems  # noqa: E402

DATA_DIR = ROOT / "server" / "data"
MATH_DIR = DATA_DIR / "math"
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


def _json(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def check_mistake_monsters() -> list[str]:
    """M7: every quái lỗi sai has to hang together across four files. A monster names a
    micro-skill (data/math/monsters.json), the floor's document must have a section for it
    (data/math/library/), the ghi chú it drops must be an item pointing at that same skill
    (data/math/drops.json), and the client must be able to draw it (client/art/math_art.py).
    Any one of those missing is a monster that cannot be fought, or a note that opens nothing.
    """
    if math_path.validate_all() or math_library.validate_all():
        return ["skipped: the learning path and library checks above must pass first"]
    sys.path.insert(0, str(ROOT))
    try:
        from client.art import math_art
    except ImportError as e:
        return [f"cannot read the client art: {e}"]
    finally:
        sys.path.remove(str(ROOT))
    out: list[str] = []
    monsters = {k: v for k, v in _json(MATH_DIR / "monsters.json").items() if not k.startswith("_")}
    drops = {k: v for k, v in _json(MATH_DIR / "drops.json").items() if not k.startswith("_")}
    docs = math_library.documents()
    for kind, m in sorted(monsters.items()):
        where = f"monster {kind}"
        try:
            subject = math_path.subject(m["subject"])
        except KeyError:
            out.append(f"{where}: no subject {m.get('subject')!r}")
            continue
        floor = next((f for f in subject.floors if f.number == m.get("floor")), None)
        if floor is None:
            out.append(f"{where}: {m['subject']} has no floor {m.get('floor')!r}")
            continue
        if m.get("skill") not in {s.id for s in floor.skills}:
            out.append(f"{where}: {m.get('skill')!r} is not a micro-skill of floor {m['floor']}")
            continue
        doc = next((d for d in docs.values() if m["skill"] in d.skills), None)
        if doc is None:
            out.append(f"{where}: no document explains {m['skill']}")
        elif not any(b["type"] == "section" and b.get("skill") == m["skill"] for b in doc.blocks):
            out.append(f"{where}: {doc.id} has no section for {m['skill']}, so its note opens page 1")
        note = drops.get(m.get("note"))
        if note is None:
            out.append(f"{where}: drops.json has no note {m.get('note')!r}")
        else:
            if note.get("kind") != "note":
                out.append(f"{where}: {m['note']} is a {note.get('kind')!r}, not a note")
            if note.get("skill") != m["skill"]:
                out.append(f"{where}: {m['note']} points at {note.get('skill')!r}, "
                           f"the monster at {m['skill']!r}")
            if note.get("monster") != kind:
                out.append(f"{where}: {m['note']} says it comes from {note.get('monster')!r}")
        if not str(m.get("mistake_vi", "")).strip():
            out.append(f"{where}: no mistake_vi, so the card cannot say what it gets wrong")
        for key in ("name_vi", "speed", "idle_seconds", "hp"):
            if key not in m:
                out.append(f"{where}: no {key} (the world needs it to spawn one)")
        art = math_art.MONSTERS.get(kind)
        if art is None:
            out.append(f"{where}: client/art/math_art.py cannot draw it")
        else:
            shape, body = art[0], art[1]
            if shape != m.get("shape"):
                out.append(f"{where}: shape {m.get('shape')!r} in the data, {shape!r} in the art")
            if body.lower() != str((m.get("look") or {}).get("body", "")).lower():
                out.append(f"{where}: the body colour differs between the data and the art")
    for item_id, note in sorted(drops.items()):
        if note.get("kind") != "note":
            continue
        if note.get("monster") not in monsters:
            out.append(f"note {item_id}: no monster {note.get('monster')!r} drops it")
    spawned, problem = _spawned_monsters(set(monsters))
    if problem:
        return out + [problem]
    for kind in sorted(set(monsters) - spawned):
        out.append(f"monster {kind}: no zone spawns it, so nobody can ever meet it")
    return out


def _spawned_monsters(known: set[str]) -> tuple[set[str], str]:
    """Which of these monsters a zone really spawns, read from the Tiled maps."""
    spawned: set[str] = set()
    try:
        zones = _json(DATA_DIR / "zones.json")
        for zid, z in zones.items():
            if zid.startswith("_") or not z.get("map"):
                continue
            tiled = _json(ROOT / "server" / "maps" / f"{z['map']}.tmj")
            for layer in tiled.get("layers", []):
                for o in layer.get("objects", []):
                    if o.get("type") != "monster_area":
                        continue
                    props = {p["name"]: p["value"] for p in o.get("properties", [])}
                    if props.get("monster") in known:
                        spawned.add(props["monster"])
    except (OSError, ValueError, KeyError) as e:
        return spawned, f"cannot read the maps: {e}"
    return spawned, ""


def check_math_crafting() -> list[str]:
    """M7: every recipe of Lò Toán makes a real piece of equipment out of things that really
    drop, and asks only for notes that really exist."""
    out: list[str] = []
    recipes = _json(MATH_DIR / "crafting.json")["recipes"]
    drops = _json(MATH_DIR / "drops.json")
    equipment = _json(DATA_DIR / "items" / "equipment.json")
    materials = _json(DATA_DIR / "items" / "materials.json")
    monsters = {k: v for k, v in _json(MATH_DIR / "monsters.json").items() if not k.startswith("_")}
    creatures = {k: v for k, v in _json(DATA_DIR / "creatures" / "monsters.json").items()
                 if not k.startswith("_")}
    dropped = set()
    for m in list(monsters.values()) + list(creatures.values()):
        dropped |= {d["item"] for d in m.get("drops", []) if "item" in d}
        if m.get("note"):
            dropped.add(m["note"])
    for rid, r in sorted(recipes.items()):
        where = f"recipe {rid}"
        if r.get("makes") not in equipment["items"]:
            out.append(f"{where}: makes {r.get('makes')!r}, which is not a piece of equipment")
        if r.get("rarity") not in equipment["rarities"]:
            out.append(f"{where}: rarity {r.get('rarity')!r} does not exist")
        if int(r.get("fee", 0)) < 0:
            out.append(f"{where}: a negative fee")
        if not r.get("ingredients"):
            out.append(f"{where}: no ingredients at all")
        for i in r.get("ingredients", []):
            item = i.get("item")
            if item not in drops and item not in materials:
                out.append(f"{where}: ingredient {item!r} is not an item")
            elif item not in dropped:
                out.append(f"{where}: nothing drops {item!r}, so the recipe cannot be finished")
            if int(i.get("qty", 0)) <= 0:
                out.append(f"{where}: {item!r} with qty {i.get('qty')!r}")
        for n in r.get("needs_notes", []):
            if drops.get(n, {}).get("kind") != "note":
                out.append(f"{where}: needs {n!r}, which is not a ghi chú lỗi sai")
    return out


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
    ("mistake-monsters: skill, library section, ghi chú, sprite, and a zone that spawns them",
     check_mistake_monsters),
    ("Lò Toán: every recipe makes real equipment from things that really drop",
     check_math_crafting),
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
