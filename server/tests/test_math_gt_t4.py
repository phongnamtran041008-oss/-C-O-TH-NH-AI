"""M11 round 2: Giải Tích floors 4-6 (đạo hàm; Taylor và L'Hospital; khảo sát hàm số) - the
bank meets its targets with every question type on every floor and the Thiên kiếp items the
contract asks for, every generator draw is valid and its answer recomputed with sympy, the
library explains every micro-skill, and a player who has cleared floors 1-3 plays floor 4
through the API."""
import json
import random
import sys
from pathlib import Path

import pytest

from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from tests.helpers import answer_key
from tests.test_math_loop import ask, clear_below, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "giai_tich"
FLOORS = (4, 5, 6)
TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_FILE = "giai_tich.t4_6.json"
DRAWS = 200


def subject():
    return mp.subject(SUBJECT)


def my_generators() -> list[mi.GeneratorSpec]:
    return [g for g in mi.generators().values() if g.subject == SUBJECT and g.floor in FLOORS]


@pytest.fixture(scope="module")
def expected():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_gt_t4 as module
        yield module.EXPECTED
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the bank
def test_the_part_file_is_valid_and_holds_exactly_floors_four_to_six():
    assert not [e for e in mi.validate_all() if "giai_tich" in e or "gt_" in e]
    raw = json.loads((mi.MATH_DIR / mi.ITEMS_DIR_NAME / PART_FILE).read_text("utf-8"))
    s = subject()
    for it in raw["items"] + raw["generators"]:
        assert s.skills[it["skill"]].floor in FLOORS, it["id"]
        assert it["reviewed"] is False
    assert all(it["id"].startswith(f"gt_t{s.skills[it['skill']].floor}_") for it in raw["items"])
    assert all(g["id"].startswith(f"gt_g{s.skills[g['skill']].floor}_") for g in raw["generators"])


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    gens = [t for t in templates if t.generated]
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert len(gens) >= max(want["generators_per_floor"], 3)
    for skill in subject().floor(floor).skills:
        for tier in mp.allowed_tiers(floor):
            n = sum(1 for t in templates if t.skill == skill.id and t.tier == tier)
            assert n >= want["per_skill_tier"], (skill.id, tier, n)


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_has_every_basic_type_and_its_thien_kiep(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    present = {i.qtype for i in items}
    assert set(TYPES) <= present, (floor, set(TYPES) - present)
    lo, hi = mp.floor_tiers(floor)
    assert all(lo <= i.tier <= hi for i in items)
    tribulations = [i for i in items if i.qtype == "tribulation"]
    if floor >= 5:
        assert len(tribulations) >= 2
        assert all(i.tier == 4 for i in tribulations)
    else:
        assert not tribulations


def test_every_thien_kiep_is_graded_right_only_when_every_part_is_right():
    tribulations = [i for i in mi.bank().values()
                    if i.subject == SUBJECT and i.floor in FLOORS and i.qtype == "tribulation"]
    assert len(tribulations) >= 4
    for item in tribulations:
        assert 2 <= len(item.parts) <= 4
        q = mi.to_question(item, random.Random(7))
        public = q.public()
        assert public["input"] == "tribulation" and len(public["prompt"]["parts"]) == len(item.parts)
        rights = []
        for k, part in zip(q.answer_key["parts"], item.parts):
            if part.qtype == "true_false":
                rights.append({"value": k["value"]})
            elif part.qtype == "multiple_choice":
                rights.append({"option": k["option"]})
            else:
                rights.append({"text": ", ".join(k["numbers"])})
        assert mi.grade("tribulation", q.answer_key, {"parts": rights}), item.id
        for n in range(len(rights)):                    # one wrong part makes the whole answer wrong
            broken = list(rights)
            broken[n] = ({"value": not rights[n]["value"]} if "value" in rights[n] else
                         {"option": "z"} if "option" in rights[n] else {"text": "987654"})
            assert not mi.grade("tribulation", q.answer_key, {"parts": broken}), (item.id, n)
        assert not mi.grade("tribulation", q.answer_key, {"parts": rights[:-1]})


def test_find_mistake_items_point_at_a_line_and_are_tier_two_or_more():
    for item in mi.bank().values():
        if item.subject == SUBJECT and item.floor in FLOORS and item.qtype == "find_mistake":
            assert 3 <= len(item.lines_vi) <= 6
            assert 0 <= item.answer < len(item.lines_vi)
            assert item.tier >= 2


# ------------------------------------------------------------------ the generators
def test_every_floor_has_its_generators_registered_and_recomputed(expected):
    ids = {g.id for g in my_generators()}
    for floor in FLOORS:
        assert sum(1 for g in my_generators() if g.floor == floor) >= 3
    assert ids == set(expected)
    assert all(g.qtype in ("true_false", "numeric") for g in my_generators())


@pytest.mark.parametrize("gid", sorted(g.id for g in my_generators()))
def test_every_draw_is_valid_repeatable_varied_and_recomputed(gid, expected):
    spec = mi.generators()[gid]
    prints, answers = set(), set()
    for seed in range(DRAWS):
        item = mi.draw(spec, random.Random(seed))
        assert not mi.draw_problems(spec, item)
        assert mi.draw(spec, random.Random(seed)) == item
        want = expected[gid](json.loads(item.numbers))
        if item.qtype == "true_false":
            assert bool(want) == item.answer, item.numbers
        else:
            got = mi.parse_numbers(item.answer)
            assert (sorted(got) == sorted(want)) if item.unordered else (got == list(want)), item.numbers
        prints.add(item.fingerprint)
        answers.add(item.answer)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]
    if spec.qtype == "true_false":
        assert answers == {True, False}                 # both answers really occur


# ------------------------------------------------------------------ the library
@pytest.mark.parametrize("floor", FLOORS)
def test_the_library_explains_every_micro_skill_of_the_floor(floor):
    docs = ml.for_floor(SUBJECT, floor)
    assert len(docs) == 1
    doc = docs[0]
    want = [s.id for s in subject().floor(floor).skills]
    assert list(doc.skills) == want
    sections = [b.get("skill") for b in doc.blocks if b["type"] == "section"]
    assert sections == want
    notes = [b for b in doc.blocks if b["type"] == "note" and b["text"].startswith("Lỗi thường gặp")]
    assert len(notes) >= len(want)
    assert len(doc.formulas) >= len(want)
    for skill in want:
        assert ml.for_skill(skill) is doc


def test_the_library_of_floors_four_to_six_has_no_problems():
    assert not [e for e in ml.validate_all() if "giai_tich" in e]
    names = {f"t{f}_" for f in FLOORS}
    assert not [e for e in ml.manifest_problems() if "giai_tich" in e and any(n in e for n in names)]


# ------------------------------------------------------------------ playing it
async def test_a_player_past_floor_three_plays_floor_four(client):
    h, uid = await make(client, "gt_dao_ham")
    await clear_below(uid, 4, subject=SUBJECT)
    run_id = await start(client, h, floor=4, subject=SUBJECT)
    skills = {s.id for s in subject().floor(4).skills}
    results = []
    for n in range(9):
        q = await ask(client, h, run_id)
        info = q["math"]
        assert info["subject"] == SUBJECT
        if info.get("review"):                         # rule 6b may bring back a floor below
            assert info["floor"] < 4
        else:
            assert info["floor"] == 4 and info["skill"] in skills
            assert info["tier"] in (2, 3)
        key = await answer_key(q["session_id"])
        correct = n % 3 != 2
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["correct"] is correct, (q["qtype"], q["prompt"], body)
        if not correct:
            assert body["reveal"]["solution_vi"]
        results.append(body["correct"])
    assert results.count(True) >= 6 and results.count(False) >= 3
