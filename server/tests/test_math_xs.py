"""M11: Xác Suất và Thống Kê - the path (9 floors + hidden 10), the question bank of floors 1-3
(bank targets, all six types, generators valid and recomputed with sympy), Tàng Thư Các for
floors 1-3, and a learner really playing floor 1 through the API."""
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
SUBJECT = "xac_suat_thong_ke"
WRITTEN_FLOORS = (1, 2, 3)
TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")


def subject() -> mp.Subject:
    return mp.subject(SUBJECT)


def raw_items() -> dict:
    return json.loads(mi.items_path(SUBJECT).read_text("utf-8"))


def own_generators() -> dict[str, mi.GeneratorSpec]:
    return {gid: g for gid, g in mi.generators().items() if g.subject == SUBJECT}


@pytest.fixture(scope="module")
def math_verify():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the path
def test_the_subject_is_written_with_nine_floors_and_a_hidden_tenth():
    s = subject()
    assert s.name_vi == "Xác Suất và Thống Kê"
    assert [f.number for f in s.main_floors] == list(range(1, 10))
    assert s.hidden_floor is not None and s.hidden_floor.number == 10
    assert s.floor(1).title_vi == "Phép thử, sự kiện và giải tích kết hợp"
    assert s.floor(4).title_vi == "Công thức xác suất đầy đủ và công thức Bayes"
    for f in s.floors:
        assert 3 <= len(f.skills) <= 6, f.number
        assert all(sk.id.startswith(f"xs_t{f.number}_") for sk in f.skills)
    assert not [e for e in mp.validate_all() if SUBJECT in e]


def test_prerequisites_point_back_and_counting_comes_before_probability():
    s = subject()
    for sk in s.skills.values():
        for r in sk.requires:
            assert s.skills[r].floor <= sk.floor, (sk.id, r)
    assert "xs_t1_to_hop" in s.skills["xs_t2_co_dien_to_hop"].requires
    assert "xs_t3_dieu_kien" in s.skills["xs_t3_cong_thuc_nhan"].requires
    assert "xs_t3_doc_lap" in s.skills["xs_t3_bernoulli"].requires


# ------------------------------------------------------------------ the bank
def test_the_items_file_is_valid():
    assert not [e for e in mi.validate_all() if SUBJECT in e or "xs_" in e]


@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_a_written_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= want["templates_per_floor"]
    assert sum(1 for t in templates if t.generated) >= want["generators_per_floor"]
    f = subject().floor(floor)
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)


@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_every_written_floor_mixes_all_six_types(floor):
    types = {i.qtype for i in mi.floor_items(SUBJECT, floor, allow_unreviewed=True)}
    assert types == set(TYPES)
    assert all(i.tier >= 2 for i in mi.floor_items(SUBJECT, floor, True) if i.qtype == "find_mistake")


def test_every_floor_including_the_hidden_tenth_is_written():
    """Floor 10 (Tài Năng) is written too (tests/test_math_xs_t10.py): no floor of the subject is empty."""
    for floor in range(1, 11):
        assert mi.floor_templates(SUBJECT, floor, allow_unreviewed=True), floor


def test_numeric_probabilities_are_written_in_lowest_terms():
    for it in raw_items()["items"]:
        if it["type"] == "numeric":
            for part in it["answer"].split(","):
                num, _, den = part.strip().partition("/")
                if den:
                    from math import gcd
                    assert gcd(int(num), int(den)) == 1 and int(den) > 1, it["id"]


def test_a_find_mistake_item_is_graded_on_the_first_wrong_line():
    item = mi.bank()["xs_t3_dk_04"]
    q = mi.to_question(item, random.Random(0))
    assert q.input == "find_mistake" and q.prompt["lines"] == list(item.lines_vi)
    assert mi.grade("find_mistake", q.answer_key, {"line": 2})
    assert not mi.grade("find_mistake", q.answer_key, {"line": 3})


# ------------------------------------------------------------------ generators
def test_every_floor_has_its_own_generators_registered():
    gens = own_generators()
    for floor in WRITTEN_FLOORS:
        assert sum(1 for g in gens.values() if g.floor == floor) >= 3
    assert all(gid in math_gen.REGISTRY for gid in gens)
    assert all(gid.startswith(f"xs_g{g.floor}_") for gid, g in gens.items())


@pytest.mark.parametrize("gid", sorted(g for g in mi.generators() if g.startswith("xs_")))
def test_every_draw_is_valid_varied_and_recomputed(gid, math_verify):
    spec = mi.generators()[gid]
    prints = set()
    for seed in range(200):
        item = mi.draw(spec, random.Random(seed))
        assert mi.draw_problems(spec, item) == [], seed
        assert math_verify.mismatch(item) is None, (seed, item.numbers)
        json.loads(item.numbers)                               # plain JSON
        prints.add(item.fingerprint)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


def test_the_recomputation_catches_a_wrong_answer(math_verify):
    import dataclasses
    item = mi.draw(mi.generators()["xs_g3_bernoulli"], random.Random(3))
    wrong = mi.parse_numbers(item.answer)[0] + 1
    assert math_verify.mismatch(dataclasses.replace(item, answer=mi.number_text(wrong)))


# ------------------------------------------------------------------ Tàng Thư Các
@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_the_library_covers_every_micro_skill_of_a_written_floor(floor):
    docs = ml.for_floor(SUBJECT, floor)
    assert len(docs) == 1
    doc = docs[0]
    assert list(doc.skills) == [sk.id for sk in subject().floor(floor).skills]
    sections = [b for b in doc.blocks if b["type"] == "section"]
    assert len(sections) == len(doc.skills)
    notes = [b for b in doc.blocks if b["type"] == "note"]
    assert len(notes) >= len(doc.skills)                         # a "Lỗi thường gặp" per section
    assert doc.formulas
    for sk in doc.skills:
        assert ml.for_skill(sk) is doc
    assert not [e for e in ml.validate_all() if SUBJECT in e]


# ------------------------------------------------------------------ a learner plays floor 1
async def test_a_fresh_player_practises_floor_one(client):
    h, _ = await make(client, "xs_hoc_tro")
    run_id = await start(client, h, floor=1, subject=SUBJECT)
    rights = 0
    for n in range(8):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT and q["math"]["floor"] in (1,)  # (spiral review: nothing below 1)
        assert q["math"]["skill"].startswith("xs_t1_")
        key = await answer_key(q["session_id"])
        correct = n % 3 != 2
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["correct"] is correct, (q["qtype"], res)
        rights += correct
        if not correct:
            assert res["math"]  # the reveal comes back after a mistake
    assert rights == 6
