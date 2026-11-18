"""M11: Giải Tích (bí cảnh 2) - its path, the question bank of floors 1-3, its generators
(valid, repeatable, varied, answers recomputed with sympy), its library, and a fresh player
really playing floor 1 through the API."""
import json
import random
import sys
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from tests.helpers import answer_key
from tests.test_math_loop import ask, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "giai_tich"
WRITTEN = (1, 2, 3)
TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
DRAWS = 200


def subject():
    return mp.subject(SUBJECT)


def gt_generators() -> list[mi.GeneratorSpec]:
    return [g for g in mi.generators().values() if g.subject == SUBJECT]


@pytest.fixture(scope="module")
def expected():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_gt as module
        yield module.EXPECTED
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the path
def test_the_subject_is_written_with_nine_floors_and_the_hidden_one():
    s = subject()
    assert s.name_vi == "Giải Tích"
    assert [f.number for f in s.floors] == list(range(1, 11))
    assert s.hidden_floor is not None and s.hidden_floor.number == 10
    assert all(3 <= len(f.skills) <= 6 for f in s.floors)
    assert all(sid.startswith("gt_t") for sid in s.skills)
    assert not [e for e in mp.validate_all() if SUBJECT in e or "gt_" in e]


def test_prerequisites_never_point_forward():
    s = subject()
    for sid, skill in s.skills.items():
        for r in skill.requires:
            assert s.skills[r].floor <= skill.floor, (sid, r)


# ------------------------------------------------------------------ the bank
def test_the_bank_file_is_valid():
    assert not [e for e in mi.validate_all() if "giai_tich" in e or "gt_" in e]


@pytest.mark.parametrize("floor", WRITTEN)
def test_each_written_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    gens = [t for t in templates if t.generated]
    assert len(templates) >= want["templates_per_floor"]
    assert len(gens) >= want["generators_per_floor"]
    for skill in subject().floor(floor).skills:
        for tier in mp.allowed_tiers(floor):
            n = sum(1 for t in templates if t.skill == skill.id and t.tier == tier)
            assert n >= want["per_skill_tier"], (skill.id, tier, n)


@pytest.mark.parametrize("floor", WRITTEN)
def test_each_written_floor_mixes_every_question_type(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    present = {i.qtype for i in items}
    for qtype in TYPES:
        if any(mp.time_limit(qtype, t) is not None for t in mp.allowed_tiers(floor)):
            assert qtype in present, (floor, qtype)
    assert all(i.tier >= 2 for i in items if i.qtype == "find_mistake")


def test_floors_four_to_ten_have_no_questions_yet():
    for floor in subject().floors:
        if floor.number not in WRITTEN:
            assert not mi.floor_templates(SUBJECT, floor.number, allow_unreviewed=True)


def test_find_mistake_items_point_at_a_line():
    for item in mi.bank().values():
        if item.subject == SUBJECT and item.qtype == "find_mistake":
            assert 3 <= len(item.lines_vi) <= 6
            assert 0 <= item.answer < len(item.lines_vi)


# ------------------------------------------------------------------ the generators
def test_every_floor_has_its_generators_registered_and_listed():
    listed = {g.id for g in gt_generators()}
    registered = {gid for gid in math_gen.REGISTRY if gid.startswith("gt_")}
    assert listed == registered
    assert {g.floor for g in gt_generators()} == set(WRITTEN)


@pytest.mark.parametrize("gid", sorted(g.id for g in gt_generators()))
def test_every_draw_is_valid_repeatable_varied_and_recomputed(gid, expected):
    spec = mi.generators()[gid]
    assert spec.qtype in ("true_false", "numeric")
    prints = set()
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
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


# ------------------------------------------------------------------ the library
@pytest.mark.parametrize("floor", WRITTEN)
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
    for skill in want:
        assert ml.for_skill(skill) is doc


def test_the_library_has_no_problems():
    assert not [e for e in ml.validate_all() if SUBJECT in e]
    assert not ml.manifest_problems()


# ------------------------------------------------------------------ playing it
async def test_a_fresh_player_plays_giai_tich_floor_one(client):
    h, _ = await make(client, "gt_hoc")
    run_id = await start(client, h, floor=1, subject=SUBJECT)
    results = []
    for n in range(8):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT and q["math"]["floor"] == 1
        assert q["math"]["tier"] in (1, 2)
        assert q["math"]["skill"] in {s.id for s in subject().floor(1).skills}
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
    assert results.count(True) >= 5 and results.count(False) >= 2
