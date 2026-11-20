"""Đại Số Tuyến Tính, floor 10 (the hidden Tài Năng floor): binary relations, binary operations, groups, rings and
fields, bilinear forms. The bank (targets, all six basic types, Thiên kiếp, a valid ladder on every item), the generators
(valid, varied, recomputed with sympy), every hand-written answer recomputed with sympy (tools/math_verify_dstt_t10.py),
Tàng Thư Các for the floor, and the fact that every micro-skill of the floor is on the tree's cut list, so none is asked."""
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
from app.learning import math_tree as mt
from tests.test_math_loop import right_answer, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "dai_so_tuyen_tinh"
FLOOR = 10
BASIC_TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_FILE = "dai_so_tuyen_tinh.t10.json"
SKILLS = ("dstt_t10_quan_he", "dstt_t10_phep_toan_hai_ngoi", "dstt_t10_nhom", "dstt_t10_vanh_truong",
          "dstt_t10_dang_song_tuyen_tinh")


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
        import math_verify_dstt_t10 as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floor_ten_and_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    assert {subject().skills[it["skill"]].floor for it in raw["items"] + raw["generators"]} == {FLOOR}
    assert all(it["id"].startswith("dstt_t10_") for it in raw["items"])
    assert all(it["id"].startswith("dstt_g10_") for it in raw["generators"])
    assert all(not it["reviewed"] for it in raw["items"] + raw["generators"])
    assert not [e for e in mi.validate_all() if "dstt_t10_" in e or "dstt_g10_" in e or PART_FILE in e]


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
    for idea in ("cộng lại được |x - z| < 1",             # two strict inequalities added as if the sum stayed under 1
                 "cùng có a, b, c nhân với các hệ số",   # associativity "checked" by comparing the wrong things
                 "phần tử ngược của 2a là 1/(2a)",       # the multiplicative inverse in an additive group
                 "Vậy mọi phần tử khác 0 đều khả nghịch",  # a few units tried, then all of them assumed
                 "b12 = b21 = 6"):                       # the cross coefficient not halved
        assert idea in text, idea
    tf = " ".join(i.prompt_vi for i in own_items() if i.qtype == "true_false")
    assert "Hợp của hai nhóm con" in tf and "không có ước của 0 đều là một trường" in tf    # the two classic false claims


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
    for iid, change in (("dstt_t10_pt_01", lambda it: it.update(answer="-3")),
                        ("dstt_t10_nh_01", lambda it: it.update(answer="4")),
                        ("dstt_t10_qh_08", lambda it: it["parts"][2].update(answer="6")),
                        ("dstt_t10_ds_09", lambda it: it["parts"][2].update(answer=False)),
                        ("dstt_t10_nh_04", lambda it: it.update(answer=1)),
                        ("dstt_t10_qh_02", lambda it: it.update(answer=True))):
        raw = raw_part()
        change(next(it for it in raw["items"] if it["id"] == iid))
        path = tmp_path / f"{iid}.json"
        path.write_text(json.dumps(raw), "utf-8")
        assert verify_t10.hand_problems(path), iid


# ------------------------------------------------------------------ generators
def test_the_floor_has_its_own_generators():
    gens = own_generators()
    assert len(gens) >= 8 and {g.skill for g in gens.values()} == set(SKILLS)
    assert all(gid in math_gen.REGISTRY and gid.startswith("dstt_g10_") for gid in gens)
    assert {g.qtype for g in gens.values()} <= {"true_false", "numeric"}
    assert all(g.tier == 5 for g in gens.values())


@pytest.mark.parametrize("gid", sorted(g for g in mi.generators() if g.startswith("dstt_g10_")))
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


@pytest.mark.parametrize("gid", ["dstt_g10_so_lop", "dstt_g10_trung_hoa", "dstt_g10_cap_cong", "dstt_g10_cap_nhan",
                                 "dstt_g10_dem_don_vi", "dstt_g10_nghich_dao_mod", "dstt_g10_ma_tran_song_tuyen",
                                 "dstt_g10_he_so_cheo"])
def test_the_recomputation_catches_a_wrong_answer(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(7))
    numbers = mi.parse_numbers(item.answer)
    numbers[-1] += mi.parse_numbers("1/100")[0]
    assert math_verify.mismatch(dataclasses.replace(item, answer=", ".join(mi.number_text(v) for v in numbers)))


@pytest.mark.parametrize("gid", ["dstt_g10_quan_he_tf", "dstt_g10_ket_hop_tf"])
def test_the_recomputation_catches_a_wrong_verdict(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(3))
    assert math_verify.mismatch(dataclasses.replace(item, answer=not item.answer))


@pytest.mark.parametrize("gid", ["dstt_g10_quan_he_tf", "dstt_g10_ket_hop_tf"])
def test_the_verdict_generators_give_both_verdicts(gid):
    assert {math_gen.REGISTRY[gid](random.Random(seed)).answer for seed in range(80)} == {True, False}


def test_a_relation_generator_explains_the_counterexample_it_found():
    for seed in range(80):
        d = math_gen.REGISTRY["dstt_g10_quan_he_tf"](random.Random(seed))
        if d.answer is False:
            assert any(w in " ".join(d.solution_vi) for w in ("Thiếu cặp", "thiếu cặp đảo", "không bắc cầu", "không phải")), seed


# ------------------------------------------------------------------ Tàng Thư Các
def test_the_library_covers_every_micro_skill_of_floor_ten():
    docs = ml.for_floor(SUBJECT, FLOOR)
    assert len(docs) == 1
    doc = docs[0]
    assert doc.id == "dstt_lib_t10" and list(doc.skills) == list(SKILLS)
    sections = [b for b in doc.blocks if b["type"] == "section"]
    assert len(sections) == len(doc.skills)
    notes = [b for b in doc.blocks if b["type"] == "note"]
    assert len(notes) >= len(doc.skills) and all(n["text"].startswith("Lỗi thường gặp") for n in notes)
    assert len(doc.formulas) >= len(doc.skills)
    assert any(b["type"] == "steps" for b in doc.blocks) and any(b["type"] == "matrices" for b in doc.blocks)
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
