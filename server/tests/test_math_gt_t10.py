"""Giải Tích, floor 10 (the hidden Tài Năng floor): the real numbers (sup and inf), limsup and liminf, Riemann
integrability, convex functions, metric spaces. The bank (targets, all six basic types, Thiên kiếp, a valid ladder on every item), the generators
(valid, varied, recomputed with sympy), every hand-written answer recomputed with sympy (tools/math_verify_gt_t10.py),
Tàng Thư Các for the floor, and the fact that every micro-skill of the floor is on the tree's cut list, so none is asked."""
import dataclasses
import json
import random
import sys
from math import gcd
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning.math_gen import gt_floor10 as _gt_floor10  # noqa: F401  (registers the floor-10 generators)
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from app.learning import math_tree as mt
from tests.test_math_loop import right_answer, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "giai_tich"
FLOOR = 10
BASIC_TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_FILE = "giai_tich.t10.json"
SKILLS = ("gt_t10_tien_de_so_thuc", "gt_t10_gioi_han_tren_duoi", "gt_t10_kha_tich_riemann", "gt_t10_ham_loi",
          "gt_t10_khong_gian_metric")


def subject() -> mp.Subject:
    return mp.subject(SUBJECT)


def raw_part() -> dict:
    return json.loads((mi.items_path(SUBJECT).parent / PART_FILE).read_text("utf-8"))


def own_generators() -> dict[str, mi.GeneratorSpec]:
    return {gid: g for gid, g in mi.generators().items() if g.subject == SUBJECT and g.floor == FLOOR}


def own_items() -> list[mi.MathItem]:
    return mi.floor_items(SUBJECT, FLOOR, allow_unreviewed=True)


@pytest.fixture(scope="module")
def math_verify():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


@pytest.fixture(scope="module")
def verify_t10():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_gt_t10 as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floor_ten_and_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    assert {subject().skills[it["skill"]].floor for it in raw["items"] + raw["generators"]} == {FLOOR}
    assert all(it["id"].startswith("gt_t10_") for it in raw["items"])
    assert all(it["id"].startswith("gt_g10_") for it in raw["generators"])
    assert all(not it["reviewed"] for it in raw["items"] + raw["generators"])
    assert not [e for e in mi.validate_all() if "gt_t10_" in e or "gt_g10_" in e or PART_FILE in e]


def test_floor_ten_meets_the_bank_targets_and_every_micro_skill_has_enough():
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, FLOOR, allow_unreviewed=True)
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert sum(1 for t in templates if t.generated) >= max(want["generators_per_floor"], 3)
    f = subject().floor(FLOOR)
    assert f.hidden and list(f.tiers) == [5]
    assert [s.id for s in f.skills] == list(SKILLS)
    for skill in f.skills:
        own = [t for t in templates if t.skill == skill.id]
        assert len([t for t in own if not t.generated]) >= 6, skill.id        # as many as the micro-skills of floors 7-9
        assert len(own) >= want["per_skill_tier"], skill.id
    assert all(t.tier == 5 for t in templates)


def test_the_floor_mixes_all_six_basic_types_and_has_tribulations():
    items = own_items()
    assert {i.qtype for i in items} >= set(BASIC_TYPES)
    tribs = [i for i in items if i.qtype == "tribulation"]
    assert len(tribs) >= 8                                  # two for each micro-skill
    for it in tribs:
        assert 2 <= len(it.parts) <= 4 and len(it.solution_vi) >= len(it.parts)
    for skill in SKILLS:
        types = {i.qtype for i in items if i.skill == skill}
        assert len(types) >= 5, skill                       # (a skill is never only one kind of question)


def test_a_tribulation_is_right_only_with_every_part_right():
    for it in [i for i in own_items() if i.qtype == "tribulation"]:
        q = mi.to_question(it, random.Random(1))
        shown = q.public()
        assert shown["input"] == "tribulation" and len(shown["prompt"]["parts"]) == len(it.parts)
        assert mi.grade("tribulation", q.answer_key, right_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, wrong_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, {"parts": []}), it.id


def test_every_item_has_a_valid_ladder_that_stays_on_or_below_floor_ten():
    where = {i.id: (i.floor, i.tier) for i in mi.bank().values() if i.subject == SUBJECT}
    where.update({g.id: (g.floor, g.tier) for g in mi.generators().values() if g.subject == SUBJECT})
    items = own_items()
    assert items and all(it.tier == 5 for it in items)
    for it in items:
        assert 2 <= len(it.ladder) <= 4, it.id
        assert len(set(it.ladder)) == len(it.ladder) and it.id not in it.ladder
        rungs = [where[r] for r in it.ladder]
        assert all(t in (3, 4) and f <= FLOOR for f, t in rungs), (it.id, rungs)
        assert any(t == 4 for _, t in rungs), it.id


def test_numeric_answers_are_lowest_terms_fractions_without_tolerance():
    raw = raw_part()
    answers = []
    for it in raw["items"]:
        if it["type"] == "numeric":
            answers.append(it["answer"])
        answers += [p["answer"] for p in it.get("parts", []) if p["type"] == "numeric"]
    assert len(answers) >= 25
    for answer in answers:
        for value in answer.split(","):
            top, _, bottom = value.strip().partition("/")
            if bottom:
                assert gcd(int(top), int(bottom)) == 1 and int(bottom) > 1, answer
    assert not any("tolerance" in it for it in raw["items"])
    assert not any("tolerance" in p for it in raw["items"] for p in it.get("parts", []))


def test_every_wrong_option_of_a_multiple_choice_gets_its_own_line_in_the_solution():
    """The solution tells why the right option is right and, in its own line, what mistake leads to each wrong one."""
    for it in [i for i in own_items() if i.qtype == "multiple_choice"]:
        assert len(it.solution_vi) >= len(it.options_vi), it.id


def test_the_find_mistake_items_target_the_classic_errors():
    fm = [i for i in own_items() if i.qtype == "find_mistake"]
    assert len(fm) >= 5
    text = " ".join(" ".join(i.lines_vi) for i in fm)
    for idea in ("Do đó 1 thuộc A và là giá trị lớn nhất",   # sup taken for max
                 "nên dãy không có limsup và liminf",       # two subsequence limits taken to mean "no limsup"
                 "n^2/2 = 1/2",                              # 1 + 2 + ... + n taken as n^2/2
                 "f''(x) = 6x >= 0 với mọi x nên f lồi trên R",   # the sign of f'' read on half the line
                 "tức d(x, z) = d(x, y) + d(y, z)"):         # the cross term of a square forgotten
        assert idea in text, idea
    tf = " ".join(i.prompt_vi for i in own_items() if i.qtype == "true_false")
    assert "tập các số hữu tỉ Q" in tf and "Hàm Dirichlet" in tf and "Tích của hai hàm lồi" in tf


# ------------------------------------------------------------------ the answers, recomputed
def test_every_hand_written_numeric_answer_is_confirmed_by_sympy(verify_t10):
    assert verify_t10.hand_problems() == []


def test_the_hand_check_covers_every_numeric_answer_of_the_floor(verify_t10):
    covered = set(verify_t10.HAND)
    for it in raw_part()["items"]:
        has_number = it["type"] == "numeric" or any(p["type"] == "numeric" for p in it.get("parts", []))
        if has_number:
            assert it["id"] in covered, it["id"]


def test_the_hand_check_has_teeth(verify_t10, tmp_path):
    for iid, change in (("gt_t10_ts_01", lambda it: it.update(answer="2")),
                        ("gt_t10_kt_09", lambda it: it["parts"][0].update(answer="12")),
                        ("gt_t10_hl_08", lambda it: it["parts"][1].update(answer="3")),
                        ("gt_t10_mt_10", lambda it: it["parts"][3].update(answer=False)),
                        ("gt_t10_ts_06", lambda it: it.update(answer=1)),
                        ("gt_t10_mt_04", lambda it: it.update(answer=True))):
        raw = raw_part()
        change(next(it for it in raw["items"] if it["id"] == iid))
        path = tmp_path / f"{iid}.json"
        path.write_text(json.dumps(raw), "utf-8")
        assert verify_t10.hand_problems(path), iid


# ------------------------------------------------------------------ generators
def test_the_floor_has_its_own_generators():
    gens = own_generators()
    assert len(gens) >= 6 and {g.skill for g in gens.values()} == set(SKILLS)
    assert all(gid in math_gen.REGISTRY and gid.startswith("gt_g10_") for gid in gens)
    assert {g.qtype for g in gens.values()} <= {"true_false", "numeric"}
    assert all(g.tier == 5 for g in gens.values())


@pytest.mark.parametrize("gid", sorted(g for g in mi.generators() if g.startswith("gt_g10_")))
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


@pytest.mark.parametrize("gid", ["gt_g10_sup_inf", "gt_g10_gioi_han_tren", "gt_g10_tong_darboux", "gt_g10_diem_uon_so",
                                 "gt_g10_jensen_hieu", "gt_g10_chuan_vecto"])
def test_the_recomputation_catches_a_wrong_answer(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(7))
    numbers = mi.parse_numbers(item.answer)
    numbers[-1] += mi.parse_numbers("1/100")[0]
    assert math_verify.mismatch(dataclasses.replace(item, answer=", ".join(mi.number_text(v) for v in numbers)))


def test_the_recomputation_catches_a_wrong_verdict(math_verify):
    for seed in (3, 4, 5):
        item = mi.draw(mi.generators()["gt_g10_metric_tf"], random.Random(seed))
        assert math_verify.mismatch(dataclasses.replace(item, answer=not item.answer))


def test_the_metric_generator_gives_both_verdicts_and_every_candidate_is_decided_by_the_search(verify_t10):
    verdicts = set()
    for seed in range(60):
        d = math_gen.REGISTRY["gt_g10_metric_tf"](random.Random(seed))
        verdicts.add(d.answer)
    assert verdicts == {True, False}
    for text in verify_t10._CANDIDATES:                    # (a non-metric always has a counterexample on the grid)
        assert any(text == t for t, _, _ in _gt_floor10.METRICS), text


# ------------------------------------------------------------------ Tàng Thư Các
def test_the_library_covers_every_micro_skill_of_floor_ten():
    docs = ml.for_floor(SUBJECT, FLOOR)
    assert len(docs) == 1
    doc = docs[0]
    assert doc.id == "gt_lib_t10" and list(doc.skills) == list(SKILLS)
    sections = [b for b in doc.blocks if b["type"] == "section"]
    assert len(sections) == len(doc.skills)
    notes = [b for b in doc.blocks if b["type"] == "note"]
    assert len(notes) >= len(doc.skills) and all(n["text"].startswith("Lỗi thường gặp") for n in notes)
    assert len(doc.formulas) >= len(doc.skills)
    assert any(b["type"] == "steps" for b in doc.blocks)
    for sk in doc.skills:
        assert ml.for_skill(sk) is doc
    assert not [e for e in ml.validate_all() if f"{SUBJECT}/t{FLOOR}_" in e]
    assert not [e for e in ml.manifest_problems() if any(f["tex"] in e for f in doc.formulas)]
    assert not any(r"\bar" in f["tex"] or r"\hat" in f["tex"] or r"\overline" in f["tex"] for f in doc.formulas)


# ------------------------------------------------------------------ the tree
def test_every_micro_skill_of_floor_ten_is_on_the_cut_list_so_none_is_asked():
    """The five micro-skills of this floor are the proof-heavy talent material the Đạo Thụ throws away: their
    questions are in the bank, but no mode asks them (math_practice._templates drops a cut micro-skill)."""
    from app.systems import math_practice
    assert set(SKILLS) <= mt.tree().cut_skills()
    assert mi.floor_templates(SUBJECT, FLOOR, True)
    assert math_practice._templates(SUBJECT, FLOOR) == []
