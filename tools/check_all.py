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
  * the four modes of M10 - bí cảnh toán, hầm ngục, cơ duyên, thủ thành toán: each mode's
    own validate() (app/systems/math_realm.py, math_dungeon.py, math_fortune.py, math_td.py):
    its data is sound, names things that exist, and can really be played with the questions
    the bank has today
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
  * Xạ Trường (scored exercises): the reference solution reaches thượng phẩm on the hidden
    sets and the top bar on every sample, in at most half its time limit; the exercise's
    naive program (problems/<subject>/ngay_tho/<id>.py: predict the majority, the mean...)
    does not even reach hạ phẩm, and a naive program of an exact exercise is not accepted
  * chiêu thức (M9): data/math/skills.json has at least five chiêu with sound fields, every
    question type exists, every effect is drawn by client/art/skill_fx.py and every
    animation is a clip of every Đạo Sĩ sheet; each chiêu unlocked on floors 1-3 has a
    question that casts it there, and only the documented one may have none anywhere
  * rơi đồ theo tu vi (2026-11-20): app/systems/loot.py validate() - every item of a loot
    table has a tu vi tier in data/loot_tiers.json, no wild zone or bí cảnh lists anything
    above its cap (its monsters included), and no breakthrough pill unlocks too late
  * Đạo Thụ: tree.json and world_plan.json pass math_tree.validate_all(), every part of a
    node names real micro-skills of its floor, and every main-path node with content can be
    reached from an empty save by finishing open nodes (vacant nodes count as done)
  * Lộ Trình Tu Tiên: guide.json passes app/systems/guide.py validate() - known check types,
    GOTO ids, seen keys and handbook pages, unique ids, real items, one reward per stage of
    the generated Đạo Thụ chapter, the text-length limits (also tools/check_guide.py)
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
    for qtype, text in math_items.INSTRUCTIONS_VI.items():
        out.append((f"math_items.INSTRUCTIONS_VI {qtype}", text))
    for item in math_items.bank().values():
        out += [(item.id, t) for t in (item.prompt_vi, *item.solution_vi, *item.options_vi,
                                       *(side for pair in item.pairs_vi for side in pair), *item.steps_vi, *item.lines_vi,
                                       item.answer_text)]   # answer_text: what the reveal shows
        out += [(item.id, t) for part in item.parts for t in (part.prompt_vi, *part.options_vi)]   # Thiên kiếp
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
    for sid, sk in _json(MATH_DIR / "skills.json").get("skills", {}).items():   # chiêu thức (M9)
        out += [(f"math/skills.json {sid}", str(sk.get(k, ""))) for k in ("name_vi", "kind_vi", "desc_vi")]
    for name in M10_TEXT_FILES:   # M10: what the four modes show comes from their data
        out += [(f"{name} {where}", text) for where, text in _vi_strings(_json(DATA_DIR / name))]
    out += [(f"strings_vi.{name}", text) for name, text in _interface_strings()]
    return out


M10_TEXT_FILES = ("math/dungeon.json", "math/fortune.json", "math/td.json", "math/drops.json", "realms.json",
                  "guide.json", "linh_can.json", "achievements.json")


def _vi_strings(node, where: str = "") -> list[tuple[str, str]]:
    """(path, text) of every string kept under a key ending in `_vi`, anywhere in a data
    file: a plain string, or strings inside lists and objects below such a key."""
    out: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{where}.{key}" if where else str(key)
            if str(key).endswith("_vi"):
                out += [(here, t) for t in _all_strings(value)]
            else:
                out += _vi_strings(value, here)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out += _vi_strings(value, f"{where}[{i}]")
    return out


def _all_strings(node) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, dict):
        return [t for v in node.values() for t in _all_strings(v)]
    if isinstance(node, list):
        return [t for v in node for t in _all_strings(v)]
    return []


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
        if problem.scored:
            errors += _check_scored_solution(coderun, problem, path)
            continue
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


def _check_scored_solution(coderun, problem, path: Path) -> list[str]:
    """Xạ Trường: the reference reaches thượng phẩm on the hidden sets, the top bar on each
    sample, and needs at most half of the time limit (the limit is about five times what it
    takes on the machine the bars were measured on)."""
    errors = []
    top = problem.grades[-1:]
    for group, tests in (("ví dụ", problem.samples), ("bia ẩn", problem.tests)):
        attempt = coderun.run_tests(path, [t.data for t in tests], problem.time_limit_ms)
        if attempt.status != coderun.OK:
            errors.append(f"{problem.id} {group}: the reference solution gave {attempt.status.upper()} "
                          f"{attempt.error.strip()[:120]}")
            continue
        verdict = math_problems.judge_problem(problem, list(tests), attempt.outputs, attempt.status,
                                              attempt.times_ms, attempt.error)
        slow = max(attempt.times_ms, default=0)
        if slow * 2 > problem.time_limit_ms:
            errors.append(f"{problem.id} {group}: the reference solution took {slow} ms, more than half "
                          f"of the {problem.time_limit_ms} ms limit")
        if group == "bia ẩn" and verdict.grade != math_problems.GRADES:
            errors.append(f"{problem.id}: the reference solution scores {verdict.score} on the hidden sets, "
                          f"only {math_problems.GRADE_NAMES_VI[verdict.grade]} (bars {list(problem.grades)})")
        for r in verdict.results if group == "ví dụ" else ():
            if math_problems.grade_of(r.score, top, problem.checker) != 1:
                errors.append(f"{problem.id} ví dụ {r.index}: the reference solution scores {r.score}, "
                              f"short of the top bar {top[0]}")
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
            tests = list(problem.tests)
            for name, build in MUTANTS:
                coderun.write_solution(path, build(problem))
                attempt = coderun.run_tests(path, [t.data for t in tests], problem.time_limit_ms)
                verdict = math_problems.judge_problem(problem, tests, attempt.outputs, attempt.status,
                                                      attempt.times_ms, attempt.error)
                if verdict.accepted or (problem.scored and verdict.grade):
                    errors.append(f"{problem.id}: a program that only {name} is accepted; "
                                  f"the hidden tests do not test anything")
            naive = math_problems.naive_path(problem.subject, problem.id)
            if naive.is_file():         # Xạ Trường: the naive model fails, not even hạ phẩm
                attempt = coderun.run_tests(naive, [t.data for t in tests], problem.time_limit_ms)
                verdict = math_problems.judge_problem(problem, tests, attempt.outputs, attempt.status,
                                                      attempt.times_ms, attempt.error)
                if attempt.status != coderun.OK:
                    errors.append(f"{problem.id}: the naive program does not even run ({attempt.status.upper()} "
                                  f"{attempt.error.strip()[:80]}), so it proves nothing")
                elif problem.scored and verdict.grade:
                    errors.append(f"{problem.id}: the naive program reaches {math_problems.GRADE_NAMES_VI[verdict.grade]} "
                                  f"(score {verdict.score}); the bars {list(problem.grades)} are too easy")
                elif not problem.scored and verdict.accepted:
                    errors.append(f"{problem.id}: the naive program is accepted; the hidden tests miss its mistake")
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
        if m.get("land") and not m.get("skill"):   # a creature of a land (Thiên Địa Đồ): learning/math_tree.py
            continue
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


def check_weapons(v2: Path | None = None) -> list[str]:
    """Binh khí của Thiên Địa Đồ: the rules' own check (app/systems/weapons.py validate():
    numbers, the five qualities and their rarities, real nodes, a drop table that keeps the loot
    rule, a forge chain made of things that drop by the time each step opens), plus the client
    art of every type in the game (status "co"; a "cho_hinh" type waits for its art and is
    skipped): every placed or droppable weapon has its icon in the atlas wired for its type and
    its own in-hand layer, and each type's clip in wiring.json is the plan's. `v2` is the art
    folder (client/assets/v2; a test passes a fake one)."""
    try:
        from app.systems import weapons
        out = list(weapons.validate())
    except Exception as e:      # noqa: BLE001 - a broken file or module must fail the check, not crash the run
        return [f"app/systems/weapons.py: validate() raised {type(e).__name__}: {e}"]
    v2 = v2 or ROOT / "client" / "assets" / "v2"
    wiring = _json(v2 / "wiring.json")
    atlases = (wiring.get("item_icons") or {}).get("by_weapon_type") or {}
    layers = wiring.get("weapons") or {}
    icons: dict[str, set] = {}
    for kind, t in weapons.data()["types"].items():
        if not weapons.type_live(kind):
            continue
        entry = layers.get(kind)
        if not isinstance(entry, dict):
            out.append(f"wiring.json weapons: no entry for weapon type {kind!r}")
        elif entry.get("clip") != t["clip"]:
            out.append(f"wiring.json weapons.{kind}: clip {entry.get('clip')!r}, the plan says {t['clip']!r}")
    shown = {p["weapon"]: f"weapon {p['id']}" for p in weapons.data()["placed"]}
    for wid in sorted(weapons.droppable_weapons()):
        shown.setdefault(wid, f"dropped weapon {wid}")
    for wid, where in shown.items():
        kind = wid.rpartition("_")[0]
        if not weapons.type_live(kind):
            continue
        atlas = atlases.get(kind)
        if atlas is None:
            out.append(f"{where}: no icon atlas wired for type {kind!r}")
        else:
            if atlas not in icons:
                doc = _json(v2 / "icons" / f"{atlas}.json") if (v2 / "icons" / f"{atlas}.json").exists() else {}
                icons[atlas] = set((doc or {}).get("icons") or {})
            if wid not in icons[atlas]:
                out.append(f"{where}: no icon {wid!r} in the {atlas} atlas")
        if not (v2 / "weapons" / f"{wid}.json").exists() or not (v2 / "weapons" / f"{wid}.png").exists():
            out.append(f"{where}: no in-hand layer weapons/{wid}")
    return out


BEAST_CLIPS = ("idle", "walk", "windup", "attack", "hit", "die", "happy")


def check_beasts() -> list[str]:
    """Linh thú and thần thông of Thiên Địa Đồ: the rules are checked with the world plan
    (app/learning/math_tree.py); here the client art they are drawn with - every built beast has
    its own v2 sheet wired in spirit_beasts with the clips its fight and its following play, the
    flying sword of Đạp Kiếm Lướt has its fly clip, the formation and the seal their effects, and
    the Phong Ấn Phù its icon."""
    from app.learning import math_tree
    plan = math_tree.world_plan()
    v2 = ROOT / "client" / "assets" / "v2"
    wiring = _json(v2 / "wiring.json")
    out: list[str] = []
    wired = wiring.get("spirit_beasts") or {}
    for b in plan.get("beasts", []):
        if b.get("status") != "co":
            continue
        sid = wired.get(b["id"])
        path = v2 / "beasts" / f"{sid}.json"
        if not isinstance(sid, str) or not path.exists() or not (v2 / "beasts" / f"{sid}.png").exists():
            out.append(f"beast {b['id']}: no v2 sheet wired in wiring.json spirit_beasts")
            continue
        clips = set((_json(path).get("clips") or {}))
        for clip in BEAST_CLIPS:
            if clip not in clips:
                out.append(f"beast {b['id']}: its sheet {sid} has no {clip!r} clip")
    unlocks = {u["id"]: u for u in plan.get("unlocks", [])}
    sword = ((unlocks.get("dap_kiem_luot") or {}).get("glide") or {}).get("sheet")
    if not sword or "fly" not in ((_json(v2 / "weapons" / f"{sword}.json").get("clips") or {})
                                  if (v2 / "weapons" / f"{sword}.json").exists() else {}):
        out.append(f"dap_kiem_luot: the flying sword {sword!r} has no v2 sheet with a fly clip")
    tran = ((unlocks.get("phap_tran") or {}).get("formation") or {}).get("fx")
    for fid in (tran, "capture_seal", "burst_hoa"):
        if not fid or not (v2 / "fx" / f"{fid}.json").exists():
            out.append(f"thần thông: no v2 effect fx/{fid}")
    talisman = (plan.get("beast_taming") or {}).get("talisman")
    if talisman not in ((wiring.get("item_icons") or {}).get("by_id") or {}):
        out.append(f"beast_taming: the talisman {talisman!r} has no icon in wiring.json item_icons.by_id")
    return out


MIN_CHIEU = 5                      # the M9 milestone: at least five chiêu from data
# chiêu that may not be castable yet, and why (the only one allowed: contract M9 section 2). The
# exception lasts only while NO question anywhere casts the chiêu: the day a Thiên kiếp of tier 4+
# lands on floor 7 or above, Thiên Lôi is checked on every floor like any other chiêu.
UNCASTABLE_OK = {"thien_loi_tuyet_ky": "no Thiên kiếp (tribulation) of tier 4+ on floor 7 or above yet "
                                       "(floors 7-9 are written in M11 đợt 2)"}


def chieu_floors() -> dict[int, list[str]]:
    """floor number -> the subjects that have questions on that floor today: where a chiêu is
    checked. A player reaching floor n can cast from any subject's floor n (the unlock floor is
    the best over all subjects), so a floor passes when one of its subjects has the question."""
    out: dict[int, list[str]] = {}
    for s in math_path.subjects():
        for f in s.main_floors:
            if math_items.floor_templates(s.id, f.number, True):
                out.setdefault(f.number, []).append(s.id)
    return dict(sorted(out.items()))


def check_chieu() -> list[str]:
    """M9: every chiêu thức of data/math/skills.json hangs together with the rest of the
    game. Its fields are sound (math_skills.validate), its question types exist, its effect
    is one client/art/skill_fx.py can draw, its picture is an icon of the item sheet (never a
    Chinese character), its animation is a clip of every Đạo Sĩ sheet,
    and - the point of a chiêu gắn câu hỏi - there really is a question that casts it: on
    every floor that has questions where it is unlocked, at least one template (of some subject
    written on that floor) of one of its types at a tier it accepts and that a player who has just
    reached the floor is asked (the floor's lowest tier). Only the documented exception may have no question
    anywhere, and only for as long as it has none."""
    if math_path.validate_all() or math_items.validate_all():
        return ["skipped: the learning path and question bank checks above must pass first"]
    try:
        from app.systems import math_skills
    except Exception as e:   # noqa: BLE001 - any import problem is a finding, not a crash
        return [f"cannot load server/app/systems/math_skills.py: {e}"]
    out = math_skills.validate()
    if out:
        return out
    skills = math_skills._read()["skills"]
    if len(skills) < MIN_CHIEU:
        out.append(f"only {len(skills)} chiêu in data/math/skills.json, the milestone needs {MIN_CHIEU}")
    sys.path.insert(0, str(ROOT))
    try:
        from client.art import skill_fx
        fx_ids = set(skill_fx.FX_IDS)
    except Exception as e:   # noqa: BLE001
        fx_ids = None
        out.append(f"cannot read client/art/skill_fx.py FX_IDS: {e}")
    finally:
        sys.path.remove(str(ROOT))
    sheets = sorted((ROOT / "client" / "assets" / "chars").glob("dao_si_*.json"))
    clips = {p.stem: set(_json(p).get("clips", {})) for p in sheets}
    icon_file = ROOT / "client" / "assets" / "icons" / "items.json"
    icons = _json(icon_file).get("icons", {}) if icon_file.exists() else None
    if icons is None:
        out.append("no client/assets/icons/items.json, so no chiêu has a picture")
    if not clips:
        out.append("no Đạo Sĩ sheet in client/assets/chars/, so no chiêu can be animated")
    playable = set(math_items.PLAYABLE_TYPES)
    floors = chieu_floors()
    for sid, sk in skills.items():
        where = f"chiêu {sid}"
        if fx_ids is not None and sk["fx"] not in fx_ids:
            out.append(f"{where}: fx {sk['fx']!r} is not in client/art/skill_fx.py FX_IDS")
        if icons is not None and len(icons.get(sk["icon"], [])) <= int(sk.get("icon_variant", 0)):
            out.append(f"{where}: icon {sk['icon']!r} variant {sk.get('icon_variant', 0)} is not in "
                       f"client/assets/icons/items.json")
        lacking = [name for name, have in clips.items() if sk["anim"] not in have]
        if lacking:
            out.append(f"{where}: anim {sk['anim']!r} is not a clip of {', '.join(lacking)}")
        types = set(sk["qtypes"]) & playable
        if sid in UNCASTABLE_OK and not math_skills.castable_floors(sk):     # (excused only while nothing casts it)
            continue
        for n, subject_ids in floors.items():
            if n < sk["unlock"]["floor"]:
                continue
            lo, _ = math_path.floor_tiers(n)
            templates = [t for sid_ in subject_ids for t in math_items.floor_templates(sid_, n, True)]
            if not any(t.qtype in types and sk["min_tier"] <= t.tier <= lo for t in templates):
                out.append(f"{where}: unlocked on floor {n} but no {'/'.join(sk['qtypes'])} question of "
                           f"tier {sk['min_tier']}..{lo} on floor {n} of any subject, so a player there "
                           f"cannot cast it")
        if not math_skills.castable_floors(sk):
            out.append(f"{where}: no question anywhere can cast it")
    return out


def check_tree() -> list[str]:
    """Đạo Thụ: the tree and the world plan pass math_tree.validate_all(); every part of a node
    (its micro-skills on one floor) names micro-skills that exist on that floor and together
    they are all of the node's; and every main-path node that has content (questions on this
    server's bank, unreviewed included, or programming exercises) can be reached from an empty
    save by the rules R3/R4: repeatedly finish every open node, starting with the vacant ones
    done - every such node must end up done."""
    if math_path.validate_all() or math_items.validate_all():
        return ["skipped: the learning path and question bank checks above must pass first"]
    try:
        from app.learning import math_tree
        from app.systems import math_tree_progress as tp
    except Exception as e:   # noqa: BLE001 - any import problem is a finding, not a crash
        return [f"cannot load the tree modules: {e}"]
    out = math_tree.validate_all()
    if out:
        return out
    t = math_tree.tree()
    cut = t.cut_skills()
    floors = {(s.id, f.number): {k.id for k in f.skills} for s in math_path.subjects() for f in s.floors}
    have: dict[tuple[str, int], set[str]] = {}

    def asked(part) -> bool:
        key = (part.subject_id, part.floor)
        if key not in have:
            have[key] = {x.skill for x in math_items.floor_templates(*key, True) if x.skill not in cut}
        return bool(have[key] & set(part.skills))

    vacant = set()
    for node in t.nodes.values():
        parts = tp.parts(node)
        for p in parts:
            for s in p.skills:
                if s not in floors.get((p.subject_id, p.floor), set()):
                    out.append(f"{node.id}: part on {p.subject_id} floor {p.floor} names {s}, which is not there")
        if sorted(s for p in parts for s in p.skills) != sorted(node.skills):
            out.append(f"{node.id}: its parts do not hold exactly its micro-skills")
        if not any(asked(p) for p in parts) and not any(pid in math_problems.bank() for pid in node.problems):
            vacant.add(node.id)
    done = set(vacant)
    while True:
        opened = {n.id for n in t.nodes.values() if n.id not in done and set(n.requires) <= done}
        if not opened:
            break
        done |= opened
    for node in t.main_nodes():
        if node.id not in done:
            missing = [r for r in node.requires if r not in done]
            out.append(f"{node.id}: can never be opened from an empty save (waits for {', '.join(missing)})")
    return out


def check_guide() -> list[str]:
    """Lộ Trình Tu Tiên: guide.json passes app/systems/guide.py validate() (tools/check_guide.py;
    its strings go through the font check below with the other data files)."""
    try:
        from app.systems import guide
        return list(guide.validate())
    except Exception as e:      # noqa: BLE001 - a broken file or module must fail the check, not crash the run
        return [f"app/systems/guide.py: validate() raised {type(e).__name__}: {e}"]


def check_generated_answers() -> list[str]:
    if math_path.validate_all() or math_items.validate_all():
        return ["skipped: the checks above must pass first"]
    try:
        import math_verify
    except ImportError as e:
        return [f"cannot recompute the answers: {e} (pip install -r server/requirements-dev.txt)"]
    return math_verify.verify_all()


# (name, function returning one line per problem; an empty list means the check passed)
def _mode_check(module: str):
    """A check that is the `validate()` of one M10 mode (empty list = sound)."""
    def check() -> list[str]:
        import importlib
        try:
            return list(importlib.import_module(f"app.systems.{module}").validate())
        except Exception as e:      # a broken module must fail the check, not crash the run
            return [f"app/systems/{module}.py: validate() raised {type(e).__name__}: {e}"]
    return check


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
    ("binh khí: every placed or dropped weapon has requirements, an icon, an in-hand layer, gated drops and a forge chain",
     check_weapons),
    ("linh thú và thần thông: every built beast, the flying sword, the formation and the talisman have their art",
     check_beasts),
    ("chiêu thức: fields, question types, FX, animation, and a question that casts each one",
     check_chieu),
    ("bí cảnh toán: the math realm, its Trận Nhãn rooms and its boss can be played",
     _mode_check("math_realm")),
    ("hầm ngục: room kinds, guardians and chests are sound and every floor can be generated",
     _mode_check("math_dungeon")),
    ("cơ duyên: events, their questions and their rewards are sound",
     _mode_check("math_fortune")),
    ("thủ thành toán: towers, their areas of mathematics and the level are sound",
     _mode_check("math_td")),
    ("rơi đồ: mỗi món có mốc tu vi, không nguồn nào vượt trần", _mode_check("loot")),
    ("linh căn: odds, caps, pity, every effect wired, every pill brewable from tiered drops",
     _mode_check("linh_can")),
    ("thành tựu: at least 90, every event sent by the code, rising tiers, rewards within their tu vi, icons, titles",
     _mode_check("achievements")),
    ("Đạo Thụ: the tree is sound, every part names real micro-skills, every main node can be reached",
     check_tree),
    ("Lộ Trình: guide.json chapters, steps, checks, rewards and text lengths are sound", check_guide),
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
