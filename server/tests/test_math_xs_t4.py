"""M11 round 2: Xác Suất và Thống Kê floors 4-6 - total probability and Bayes, random variables
and F(x) = P(X < x), expectation, variance and the usual laws. The bank of each floor (targets,
all six basic types, Thiên kiếp on floors 5-6), the generators (valid, varied, recomputed with
sympy), Tàng Thư Các for the three floors, and a learner who has cleared floors 1-3 playing
floor 4 through the API."""
import dataclasses
import json
import random
import sys
from math import gcd
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from tests.helpers import answer_key
from tests.test_math_loop import ask, clear_below, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "xac_suat_thong_ke"
FLOORS = (4, 5, 6)
BASIC_TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_FILE = "xac_suat_thong_ke.t4_6.json"


def subject() -> mp.Subject:
    return mp.subject(SUBJECT)


def raw_part() -> dict:
    return json.loads((mi.items_path(SUBJECT).parent / PART_FILE).read_text("utf-8"))


def own_generators(floor: int) -> dict[str, mi.GeneratorSpec]:
    return {gid: g for gid, g in mi.generators().items() if g.subject == SUBJECT and g.floor == floor}


@pytest.fixture(scope="module")
def math_verify():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_four_to_six_and_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    floors = {subject().skills[it["skill"]].floor for it in raw["items"] + raw["generators"]}
    assert floors == set(FLOORS)
    assert all(it["id"].startswith(f"xs_t{subject().skills[it['skill']].floor}_") for it in raw["items"])
    assert all(not it["reviewed"] for it in raw["items"] + raw["generators"])
    assert not [e for e in mi.validate_all() if "xs_t4_" in e or "xs_t5_" in e or "xs_t6_" in e
                or "xs_g4_" in e or "xs_g5_" in e or "xs_g6_" in e or PART_FILE in e]


@pytest.mark.parametrize("floor", FLOORS)
def test_a_written_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert sum(1 for t in templates if t.generated) >= want["generators_per_floor"]
    f = subject().floor(floor)
    assert list(f.tiers) == ([2, 3] if floor == 4 else [3, 4])
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)
    assert all(f.tiers[0] <= t.tier <= f.tiers[1] for t in templates)


@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_mixes_all_six_basic_types(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    assert {i.qtype for i in items} >= set(BASIC_TYPES)
    assert all(i.tier >= 2 for i in items if i.qtype == "find_mistake")
    assert not [i.id for i in items if i.tier == 5]            # (no tier 5 below floor 7: no ladder needed)


@pytest.mark.parametrize("floor", (5, 6))
def test_floors_five_and_six_each_have_tier_four_tribulations(floor):
    tribs = [i for i in mi.floor_items(SUBJECT, floor, allow_unreviewed=True) if i.qtype == "tribulation"]
    assert len(tribs) >= 2
    for it in tribs:
        assert it.tier == 4 and 2 <= len(it.parts) <= 4
        assert len(it.solution_vi) >= len(it.parts)


@pytest.mark.parametrize("floor", (5, 6))
def test_a_tribulation_is_right_only_with_every_part_right(floor):
    for it in [i for i in mi.floor_items(SUBJECT, floor, True) if i.qtype == "tribulation"]:
        q = mi.to_question(it, random.Random(1))
        shown = q.public()
        assert shown["input"] == "tribulation" and len(shown["prompt"]["parts"]) == len(it.parts)
        assert mi.grade("tribulation", q.answer_key, right_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, wrong_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, {"parts": []}), it.id


def test_probabilities_are_written_in_lowest_terms_and_decimals_only_for_table_values():
    answers = []
    for it in raw_part()["items"]:
        if it["type"] == "numeric":
            answers.append((it["id"], it["answer"]))
        for part in it.get("parts", []):
            if part["type"] == "numeric":
                answers.append((it["id"], part["answer"]))
    for iid, answer in answers:
        for value in answer.split(","):
            num, _, den = value.strip().partition("/")
            if den:
                assert gcd(int(num), int(den)) == 1 and int(den) > 1, iid
            elif "." in num:                                     # an exact sum of table values given in the prompt
                assert "Phi(" in mi.bank()[iid].prompt_vi or "e^(" in mi.bank()[iid].prompt_vi, iid
    assert not any("tolerance" in it for it in raw_part()["items"])


def test_the_find_mistake_items_target_the_classic_errors():
    items = {i.id: i for i in mi.bank().values() if i.subject == SUBJECT and i.floor in FLOORS}
    fm = [i for i in items.values() if i.qtype == "find_mistake"]
    assert len(fm) >= 15
    text = " ".join(" ".join(i.lines_vi) for i in fm)
    for idea in ("P(A|H_2)",              # P(A|B) taken for P(B|A)
                 "1 - 1/50",              # the base rate ignored
                 "trung bình cộng",       # total probability without the weights
                 "E(X^2) = (E(X))^2",     # E(X^2) = E(X)^2
                 "tổng các phương sai",   # the variance of a sum of dependent variables
                 "phương sai bằng kỳ vọng",  # binomial taken for Poisson
                 "(X - 20)/9"):           # standardising with the variance
        assert idea in text, idea


# ------------------------------------------------------------------ generators
@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_has_its_own_generators(floor):
    gens = own_generators(floor)
    assert len(gens) >= 3
    assert all(gid in math_gen.REGISTRY and gid.startswith(f"xs_g{floor}_") for gid in gens)
    assert {g.qtype for g in gens.values()} <= {"true_false", "numeric"}


@pytest.mark.parametrize("gid", sorted(g for g in mi.generators() if g[:5] in ("xs_g4", "xs_g5", "xs_g6")))
def test_every_draw_is_valid_varied_and_recomputed(gid, math_verify):
    spec = mi.generators()[gid]
    prints = set()
    for seed in range(200):
        item = mi.draw(spec, random.Random(seed))
        assert mi.draw_problems(spec, item) == [], seed
        assert math_verify.mismatch(item) is None, (seed, item.numbers)
        json.loads(item.numbers)
        prints.add(item.fingerprint)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


@pytest.mark.parametrize("gid", ["xs_g4_bayes", "xs_g5_ham_phan_phoi", "xs_g6_chuan"])
def test_the_recomputation_catches_a_wrong_answer(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(7))
    wrong = mi.parse_numbers(item.answer)[0] + mi.parse_numbers("1/100")[0]
    assert math_verify.mismatch(dataclasses.replace(item, answer=mi.number_text(wrong)))


def test_the_distribution_function_uses_a_strict_inequality():
    """F(x) = P(X < x): a value equal to x is never counted (HUST's convention)."""
    from app.learning.math_gen import xs_floor5
    for seed in range(200):
        d = xs_floor5.ham_phan_phoi(random.Random(seed))
        values, probs, c = d.params["values"], d.params["probs"], d.params["c"]
        want = sum((mi.parse_numbers(p)[0] for v, p in zip(values, probs) if v < c), mi.parse_numbers("0")[0])
        assert mi.parse_numbers(d.answer)[0] == want


# ------------------------------------------------------------------ Tàng Thư Các
@pytest.mark.parametrize("floor", FLOORS)
def test_the_library_covers_every_micro_skill_of_the_floor(floor):
    docs = ml.for_floor(SUBJECT, floor)
    assert len(docs) == 1
    doc = docs[0]
    assert list(doc.skills) == [sk.id for sk in subject().floor(floor).skills]
    sections = [b for b in doc.blocks if b["type"] == "section"]
    assert len(sections) == len(doc.skills)
    notes = [b for b in doc.blocks if b["type"] == "note"]
    assert len(notes) >= len(doc.skills) and all(n["text"].startswith("Lỗi thường gặp") for n in notes)
    assert len(doc.formulas) >= len(doc.skills)
    assert any(b["type"] == "steps" for b in doc.blocks)              # worked examples
    for sk in doc.skills:
        assert ml.for_skill(sk) is doc
    assert not [e for e in ml.validate_all() if SUBJECT in e]
    assert not [e for e in ml.manifest_problems() if any(f["tex"] in e for f in doc.formulas)]


# ------------------------------------------------------------------ a learner plays floor 4
async def test_a_player_who_cleared_floors_one_to_three_practises_floor_four(client):
    h, uid = await make(client, "xs_t4_hoc_tro")
    await clear_below(uid, 4, subject=SUBJECT)
    run_id = await start(client, h, floor=4, subject=SUBJECT)
    rights, on_floor_four = 0, 0
    for n in range(10):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT and 1 <= q["math"]["floor"] <= 4   # (spiral review may go below)
        on_floor_four += q["math"]["floor"] == 4
        if q["math"]["floor"] == 4:
            assert q["math"]["skill"].startswith("xs_t4_") and q["math"]["tier"] in (2, 3)
        key = await answer_key(q["session_id"])
        correct = n % 3 != 2
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["correct"] is correct, (q["qtype"], res)
        rights += correct
        if not correct:
            assert res["math"]
    assert rights == 7 and on_floor_four >= 5
