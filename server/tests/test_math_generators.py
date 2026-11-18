"""M3: the question bank of floors 1-3 - generators (valid, repeatable, varied, answers
recomputed with sympy), bank targets per floor, near-duplicates, matrices. Pure tests."""
import copy
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_path as mp
from app.learning.math_gen import Draw, complex_text, linear_text, num, nums, paren, set_text, vec_text

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "dai_so_tuyen_tinh"
WRITTEN_FLOORS = (1, 2, 3)                  # of every subject (M11)
SUBJECTS = [SUBJECT, "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac"]
GENERATORS = sorted(mi.generators())


@pytest.fixture(scope="module")
def math_verify():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


def raw_items() -> dict:
    return json.loads(mi.items_path(SUBJECT).read_text("utf-8"))


def check(mutate) -> list[str]:
    raw = copy.deepcopy(raw_items())
    mutate(raw)
    return mi.validate_items(mp.subject(SUBJECT), raw, mp.cfg())


# ------------------------------------------------------------------ the shipped bank
def test_the_bank_is_valid():
    assert mp.validate_all() == []
    assert mi.validate_all() == []


@pytest.mark.parametrize("subject", SUBJECTS)
@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_a_written_floor_has_enough_templates_and_generators(subject, floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(subject, floor, allow_unreviewed=True)
    assert len(templates) >= want["templates_per_floor"] == 30
    assert sum(1 for t in templates if t.generated) >= want["generators_per_floor"] == 3
    f = mp.subject(subject).floor(floor)
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)
            if subject == SUBJECT:      # Đại Số Tuyến Tính floors 2-3: new numbers everywhere (M3)
                assert any(t.generated for t in own) or floor == 1, (skill.id, tier)


def test_the_written_subjects_are_the_four_of_luyen_khi():
    assert [s.id for s in mp.subjects()] == SUBJECTS                     # M11
    assert {g.subject for g in mi.generators().values()} == set(SUBJECTS)


@pytest.mark.parametrize("subject", SUBJECTS)
def test_floors_not_written_yet_have_no_templates(subject):
    for floor in range(4, 11):
        assert mi.floor_templates(subject, floor, allow_unreviewed=True) == []


def test_every_generator_is_listed_and_every_listed_generator_exists():
    assert set(math_gen.REGISTRY) == set(mi.generators())
    assert not set(mi.generators()) & set(mi.bank())


@pytest.mark.parametrize("subject", SUBJECTS)
def test_unreviewed_generators_are_held_back_like_items(subject):
    assert all(not t.generated or t.reviewed for t in mi.floor_templates(subject, 2, allow_unreviewed=False))


# ------------------------------------------------------------------ what a generator draws
@pytest.mark.parametrize("gid", GENERATORS)
def test_one_seed_always_gives_the_same_question(gid):
    spec = mi.generators()[gid]
    for seed in range(15):
        assert mi.draw(spec, random.Random(seed)) == mi.draw(spec, random.Random(seed))


@pytest.mark.parametrize("gid", GENERATORS)
def test_every_draw_is_a_valid_playable_question(gid):
    spec = mi.generators()[gid]
    prints = set()
    for seed in range(60):
        item = mi.draw(spec, random.Random(seed))
        assert mi.draw_problems(spec, item) == []
        assert item.generated and item.id == gid and (item.skill, item.tier, item.qtype) == (
            spec.skill, spec.tier, spec.qtype)
        assert mp.tier_allowed(item.floor, item.tier) and json.loads(item.numbers)
        prints.add(item.fingerprint)
        q = mi.to_question(item, random.Random(seed))
        assert q.item_id == gid and q.answer_key["fingerprint"] == item.fingerprint
        public = json.dumps(q.public(), ensure_ascii=False)
        assert "solution_vi" not in public and "fingerprint" not in public
        if item.qtype == "true_false":
            right, wrong = {"value": item.answer}, {"value": not item.answer}
        else:
            right, wrong = {"text": item.answer}, {"text": "987654"}
        assert mi.grade(item.qtype, q.answer_key, right) and not mi.grade(item.qtype, q.answer_key, wrong)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


def test_the_shipped_generators_pass_the_generator_check():
    assert mi.generator_problems(draws=40) == []


def test_different_numbers_give_different_fingerprints_of_one_template():
    spec = mi.generators()["dstt_g1_giao"]
    a, b = mi.draw(spec, random.Random(1)), mi.draw(spec, random.Random(2))
    assert a.id == b.id and a.numbers != b.numbers and a.fingerprint != b.fingerprint
    static = next(iter(mi.bank().values()))
    assert static.numbers == "" and not static.generated


def test_a_matrix_question_sends_its_matrices_to_the_client():
    item = mi.draw(mi.generators()["dstt_g3_doi_xung_dien"], random.Random(4))
    q = mi.to_question(item)
    (m,) = q.prompt["matrices"]
    cells = [v for row in m["rows"] for v in row]
    assert m["name"] == "A" and len(m["rows"]) == 3 and sorted(c for c in cells if c.isalpha()) == ["x", "y"]
    assert all(isinstance(v, str) for v in cells)
    static = mi.bank()["dstt_t3_db_03"]
    assert mi.to_question(static).prompt["matrices"] == [
        {"name": "A", "rows": [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "0"]]}]
    assert "matrices" not in mi.to_question(mi.bank()["dstt_t1_th_01"]).prompt


# ------------------------------------------------------------------ the generator check catches bad generators
def swap(monkeypatch, gid, fn):
    monkeypatch.setitem(math_gen.REGISTRY, gid, fn)


def test_generator_check_catches_too_little_variety(monkeypatch):
    swap(monkeypatch, "dstt_g3_vet", lambda rng: Draw({"n": rng.randint(1, 3)}, "Tính 1 + 1.", "2", ["1 + 1 = 2."]))
    assert mi.generator_problems(draws=40) == ["dstt_g3_vet: 40 draws give only 3 different questions, need 8"]


def test_generator_check_catches_a_generator_that_ignores_its_seed(monkeypatch):
    loose = random.Random()
    swap(monkeypatch, "dstt_g3_vet", lambda rng: Draw({"n": loose.random()}, "Tính 1 + 1.", "2", ["1 + 1 = 2."]))
    (error,) = mi.generator_problems(draws=5)
    assert error == "dstt_g3_vet: seed 0 gives two different questions"


@pytest.mark.parametrize("draw,problem", [
    (Draw({"n": 1}, "Tính A ∩ B.", "2", ["ok"]), "prompt_vi has the character"),
    (Draw({"n": 1}, "Tính 1 + 1.", "hai", ["ok"]), "answer must be a number"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", []), "solution_vi must list at least one step"),
    (Draw({"n": 1}, "Tính 1 + 1.", "1, 1", ["ok"], unordered=True), "lists the same number twice"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", ["ok"], matrices={"A": [[1, 2], [3]]}), "must be a rectangle"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", ["ok"], matrices={"a": [[1]]}), "must be one capital letter"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", ["ok"], matrices={"A": [[1] * 5]}), "must be a rectangle"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", ["ok"], matrices={"A": [["quá dài"]]}), "must be a number, a fraction a/b or one small letter"),
    (Draw({"n": 1}, "Tính 1 + 1.", "2", ["ok"], matrices={"A": [[True]]}), "must be a number, a fraction a/b or one small letter"),
])
def test_generator_check_catches_a_bad_draw(monkeypatch, draw, problem):
    swap(monkeypatch, "dstt_g3_vet", lambda rng: draw)
    errors = mi.generator_problems(draws=3)
    assert errors and problem in errors[0] and errors[0].startswith("dstt_g3_vet with")


def test_a_generator_function_that_is_not_listed_is_reported(monkeypatch):
    swap(monkeypatch, "dstt_g9_quen_khai_bao", lambda rng: Draw({}, "x", "1", ["x"]))
    assert mi.validate_all() == [
        "learning/math_gen: generator dstt_g9_quen_khai_bao is not listed in any math/items file"]


def test_registering_one_id_twice_is_an_error():
    with pytest.raises(ValueError):
        math_gen.generator("dstt_g3_vet")(lambda rng: None)


# ------------------------------------------------------------------ answers recomputed with sympy
def test_every_generator_has_a_recomputation(math_verify):
    assert set(math_verify.EXPECTED) == set(mi.generators())


def test_sympy_confirms_the_answer_of_every_draw(math_verify):
    assert math_verify.verify_all(draws=25) == []


def test_the_recomputation_catches_a_wrong_answer(math_verify, monkeypatch):
    real = math_gen.REGISTRY["dstt_g3_vet"]

    def off_by_one(rng):
        d = real(rng)
        d.answer = str(int(d.answer) + 1)
        return d
    swap(monkeypatch, "dstt_g3_vet", off_by_one)
    (error,) = math_verify.verify_all(draws=3)
    assert error.startswith("dstt_g3_vet with ") and "but sympy gets" in error


def test_the_recomputation_catches_a_wrong_truth_value_and_a_wrong_order(math_verify, monkeypatch):
    real_tf, real_list = math_gen.REGISTRY["dstt_g1_thuoc"], math_gen.REGISTRY["dstt_g2_cong_tru"]

    def flipped(rng):
        d = real_tf(rng)
        d.answer = not d.answer
        return d

    def swapped(rng):
        d = real_list(rng)
        re, im = mi.parse_numbers(d.answer)
        d.answer = nums([im, re])
        return d
    swap(monkeypatch, "dstt_g1_thuoc", flipped)
    swap(monkeypatch, "dstt_g2_cong_tru", swapped)
    errors = math_verify.verify_all(draws=10)
    assert sorted(e.split()[0] for e in errors) == ["dstt_g1_thuoc", "dstt_g2_cong_tru"]


def test_a_draw_without_a_recomputation_is_reported(math_verify, monkeypatch):
    monkeypatch.delitem(math_verify.EXPECTED, "dstt_g3_vet")
    item = mi.draw(mi.generators()["dstt_g3_vet"], random.Random(1))
    assert math_verify.mismatch(item) == "has no recomputation in tools/math_verify.py"


# ------------------------------------------------------------------ the validator: generators, targets, near-duplicates
def drop_generators_of_floor(raw: dict, floor: int) -> None:
    skills = {s.id for s in mp.subject(SUBJECT).floor(floor).skills}
    raw["generators"] = [g for g in raw["generators"] if g["skill"] not in skills]


def too_few_templates_on_floor_2(raw: dict) -> None:
    """Floor 2 without its generators and without its three Tìm chỗ sai items (M11): the 27
    hand-written questions it had before, three short of the target."""
    drop_generators_of_floor(raw, 2)
    skills = {s.id for s in mp.subject(SUBJECT).floor(2).skills}
    gone = [i for i in raw["items"] if i["skill"] in skills and i["type"] == "find_mistake"]
    assert len(gone) == 3
    raw["items"] = [i for i in raw["items"] if i not in gone]


def clone_with_other_numbers(raw: dict) -> None:
    twin = copy.deepcopy(next(i for i in raw["items"] if i["id"] == "dstt_t1_td_04"))
    twin.update(id="dstt_t1_td_99", prompt_vi="Tập A x B có 20 phần tử và A có 5 phần tử. B có bao nhiêu phần tử?",
                answer="4")
    raw["items"].append(twin)


BREAKAGE = {
    "generators not a list": (lambda r: r.update(generators={}), "generators: must be a list"),
    "generator without a function": (lambda r: r["generators"].append(
        {"id": "dstt_g9_khong_co", "skill": "dstt_t1_tap_hop", "tier": 1, "type": "numeric"}),
        "no generator function with this id"),
    "generator on a tier its floor does not have": (lambda r: r["generators"][0].update(tier=3),
                                                    "tier 3 is not allowed on floor 1"),
    "generator of an unknown skill": (lambda r: r["generators"][0].update(skill="dstt_t1_khong_co"),
                                      "is not a micro-skill"),
    "generator of a type that is not playable": (lambda r: r["generators"][0].update(type="tribulation"),
                                                 "type must be one of"),
    "generator of a find_mistake question": (lambda r: r["generators"][0].update(type="find_mistake"),
                                             "a find_mistake question can only be hand-written for now"),
    "generator of a matching question": (lambda r: r["generators"][0].update(type="matching"),
                                         "a matching question can only be hand-written for now"),
    "generator of an ordering question": (lambda r: r["generators"][0].update(type="ordering"),
                                          "an ordering question can only be hand-written for now"),
    "generator with an unknown key": (lambda r: r["generators"][0].update(prompt_vi="x"), "unknown key 'prompt_vi'"),
    "generator reviewed is not a boolean": (lambda r: r["generators"][0].update(reviewed=1),
                                            "reviewed must be true or false"),
    "generator id already used by an item": (lambda r: r["generators"][0].update(id=r["items"][0]["id"]),
                                             "this id is used twice"),
    "the same question with other numbers": (clone_with_other_numbers,
                                             "dstt_t1_td_99: is almost the same question as dstt_t1_td_04"),
    "a floor without its generators": (lambda r: drop_generators_of_floor(r, 2), "floor 2: has 0 generators, need 3"),
    "a floor with too few templates": (too_few_templates_on_floor_2, "floor 2: has 27 templates, need 30"),
    "a micro-skill and tier with one template": (
        lambda r: r["items"].remove(next(i for i in r["items"] if i["id"] == "dstt_t3_vt_03")),
        "floor 3: dstt_t3_vecto_rn has 1 templates at tier 3, need 2"),
    "matrix name": (lambda r: r["items"][0].update(matrices={"ab": [[1]]}), "must be one capital letter"),
    "ragged matrix": (lambda r: r["items"][0].update(matrices={"A": [[1, 2], [3]]}), "must be a rectangle"),
    "too many matrices": (lambda r: r["items"][0].update(matrices={k: [[1]] for k in "ABCD"}),
                          "matrices must name 1 to 3 matrices"),
}


@pytest.mark.parametrize("name", sorted(BREAKAGE))
def test_validator_catches(name):
    mutate, expected = BREAKAGE[name]
    errors = check(mutate)
    assert any(expected in e for e in errors), errors[:5]


def test_similar_questions_about_different_things_are_not_near_duplicates():
    items = [{"id": "a", "skill": "s", "prompt_vi": "Cho A = {1, 2} và B = {2, 3}. Liệt kê các phần tử của A giao B."},
             {"id": "b", "skill": "s", "prompt_vi": "Cho A = {1, 2} và B = {2, 3}. Liệt kê các phần tử của hiệu A \\ B."},
             {"id": "c", "skill": "t", "prompt_vi": "Cho A = {4, 5} và B = {5, 6}. Liệt kê các phần tử của A giao B."}]
    assert mi.near_duplicates(items) == []                # (c is another micro-skill)
    items[2]["skill"] = "s"
    assert mi.near_duplicates(items) == ["c: is almost the same question as a (only the numbers differ)"]


def test_targets_apply_only_to_floors_that_have_questions():
    raw = raw_items()
    floor1 = {s.id for s in mp.subject(SUBJECT).floor(1).skills}
    raw["items"] = [i for i in raw["items"] if i["skill"] in floor1]
    raw["generators"] = [g for g in raw["generators"] if g["skill"] in floor1]
    assert mi.target_problems(mp.subject(SUBJECT), raw, mp.cfg()) == []


# ------------------------------------------------------------------ writing math as text
def test_numbers_and_sets_as_text():
    assert [num(v) for v in (3, -2, Fraction(6, 4), Fraction(-1, 2), 0)] == ["3", "-2", "3/2", "-1/2", "0"]
    assert nums([1, Fraction(1, 2), -3]) == "1, 1/2, -3"
    assert [paren(v) for v in (3, -3, Fraction(1, 2), 0)] == ["3", "(-3)", "(1/2)", "0"]
    assert set_text([1, 2, 3]) == "{1, 2, 3}" and vec_text([1, -2, 0]) == "(1, -2, 0)"


@pytest.mark.parametrize("a,b,text", [(2, 1, "2x + 1"), (1, 0, "x"), (-1, -3, "-x - 3"), (0, 4, "4"), (-4, 0, "-4x"),
                                      (1, -7, "x - 7"), (3, 0, "3x"), (0, 0, "0")])
def test_linear_text(a, b, text):
    assert linear_text(a, b) == text


@pytest.mark.parametrize("re,im,text", [(3, -2, "3 - 2i"), (0, 1, "i"), (0, -1, "-i"), (5, 0, "5"), (0, 0, "0"),
                                        (-1, 1, "-1 + i"), (0, 4, "4i"), (2, -1, "2 - i"),
                                        (Fraction(1, 2), Fraction(-1, 2), "1/2 - (1/2)i")])
def test_complex_text(re, im, text):
    assert complex_text(re, im) == text


def test_all_generated_text_is_showable():
    """Every character of every draw passes the same test as hand-written text."""
    for spec in mi.generators().values():
        item = mi.draw(spec, random.Random(11))
        for text in (item.prompt_vi, *item.solution_vi, *item.options_vi):
            assert mp.text_problem(text) is None, (spec.id, text)
