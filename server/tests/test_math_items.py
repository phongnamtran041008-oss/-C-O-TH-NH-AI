"""M2: math items - the seed bank is valid, questions are built and graded correctly, and
the validator catches broken items. Pure tests: no database."""
import copy
import json
import random
from fractions import Fraction

import pytest

from app.learning import math_items as mi
from app.learning import math_path as mp

SUBJECT = "dai_so_tuyen_tinh"


def raw_items() -> dict:
    return json.loads(mi.items_path(SUBJECT).read_text("utf-8"))


def item(**over) -> mi.MathItem:
    base = dict(id="x_item_1", subject=SUBJECT, skill="dstt_t1_tap_hop", floor=1, tier=1, qtype="numeric",
                prompt_vi="Tính 1 + 1.", answer="2", solution_vi=("1 + 1 = 2.",))
    base.update(over)
    return mi.MathItem(**base)


# ------------------------------------------------------------------ the shipped bank
def test_shipped_items_are_valid():
    assert mp.validate_all() == []
    assert mi.validate_all() == []


def test_seed_bank_covers_every_skill_and_tier_of_floor_1():
    floor = mp.subject(SUBJECT).floor(1)
    items = mi.floor_items(SUBJECT, 1, allow_unreviewed=True)
    for skill in floor.skills:
        for tier in floor.tiers:
            assert sum(1 for i in items if i.skill == skill.id and i.tier == tier) >= 2, (skill.id, tier)


def test_every_item_tier_is_allowed_on_its_floor():
    for it in mi.bank().values():
        assert mp.tier_allowed(it.floor, it.tier), it.id


def test_unreviewed_items_are_held_back_unless_allowed():
    assert mi.floor_items(SUBJECT, 1, allow_unreviewed=True)
    assert all(i.reviewed for i in mi.floor_items(SUBJECT, 1, allow_unreviewed=False))


def test_fingerprints_are_unique_and_fit_the_column():
    prints = [i.fingerprint for i in mi.bank().values()]
    assert len(set(prints)) == len(prints)
    assert all(len(p) <= 64 for p in prints)


def test_every_shipped_item_becomes_a_question_its_own_answer_passes():
    rng = random.Random(7)
    for it in mi.bank().values():
        q = mi.to_question(it, rng)
        assert q.time_limit == mp.time_limit(it.qtype, it.tier)
        assert q.item_id == it.id and q.meta["tier"] == it.tier and q.meta["skill"] == it.skill
        public = json.dumps(q.public(), ensure_ascii=False)
        assert "solution_vi" not in public and "fingerprint" not in public     # the key stays on the server
        if it.qtype == "true_false":
            right, wrong = {"value": it.answer}, {"value": not it.answer}
        elif it.qtype == "multiple_choice":
            right = {"option": q.answer_key["option"]}
            wrong = {"option": next(o["id"] for o in q.options if o["id"] != q.answer_key["option"])}
        else:
            right, wrong = {"text": it.answer}, {"text": "987654"}
        assert mi.grade(it.qtype, q.answer_key, right), it.id
        assert not mi.grade(it.qtype, q.answer_key, wrong), it.id
        assert not mi.grade(it.qtype, q.answer_key, {}), it.id
        assert not mi.grade(it.qtype, q.answer_key, None), it.id


# ------------------------------------------------------------------ numbers
@pytest.mark.parametrize("text,value", [
    ("7", Fraction(7)), (" -3 ", Fraction(-3)), ("0.25", Fraction(1, 4)), ("3/4", Fraction(3, 4)),
    ("-1/2", Fraction(-1, 2)), ("+5", Fraction(5)), (".5", Fraction(1, 2)), ("6/3", Fraction(2)),
    ("1 / 2", Fraction(1, 2)),
])
def test_parse_number(text, value):
    assert mi.parse_number(text) == value


@pytest.mark.parametrize("text", ["", "abc", "1/0", "1/-2", "1e5", "1,5x", "2/3/4", "--2", "1.2.3", "½", "٣",
                                  "1/2.5", "inf", "nan", "0x10", "1_000"])
def test_parse_number_rejects(text):
    assert mi.parse_number(text) is None


def test_parse_numbers_lists():
    assert mi.parse_numbers("1, 3, 5") == [1, 3, 5]
    assert mi.parse_numbers("1;3") == [1, 3]
    assert mi.parse_numbers("1, , 3") is None
    assert mi.parse_numbers("1,") is None
    assert mi.parse_numbers(12) is None
    assert mi.parse_numbers(",".join(["1"] * (mi.MAX_NUMBERS + 1))) is None
    assert mi.parse_numbers("1" * (mi.MAX_ANSWER_CHARS + 1)) is None


# ------------------------------------------------------------------ grading
def test_numeric_grading_accepts_equal_forms_and_a_tiny_error():
    key = mi.to_question(item(answer="3/4")).answer_key
    for text in ("3/4", "0.75", "6/8", " 0.750 ", "0.7500004"):
        assert mi.grade("numeric", key, {"text": text}), text
    for text in ("0.76", "0.7501", "4/3", "3/4, 1", "", "ba phần tư"):
        assert not mi.grade("numeric", key, {"text": text}), text
    assert not mi.grade("numeric", key, {"text": 0.75})          # must be typed text
    assert not mi.grade("numeric", key, {"value": True})


def test_numeric_list_order_matters_unless_unordered():
    ordered = mi.to_question(item(answer="1, 2, 3")).answer_key
    assert mi.grade("numeric", ordered, {"text": "1,2,3"})
    assert not mi.grade("numeric", ordered, {"text": "3,2,1"})
    assert not mi.grade("numeric", ordered, {"text": "1,2"})
    a_set = mi.to_question(item(answer="1, 2, 3", unordered=True)).answer_key
    assert mi.grade("numeric", a_set, {"text": "3; 1; 2"})
    assert not mi.grade("numeric", a_set, {"text": "1, 2, 2"})
    assert not mi.grade("numeric", a_set, {"text": "1, 2, 3, 3"})


def test_true_false_grading_needs_a_real_boolean():
    key = mi.to_question(item(qtype="true_false", answer=False)).answer_key
    assert mi.grade("true_false", key, {"value": False})
    assert not mi.grade("true_false", key, {"value": True})
    for junk in (0, "false", None, "Sai"):
        assert not mi.grade("true_false", key, {"value": junk})


def test_multiple_choice_is_shuffled_but_keeps_exactly_one_right_option():
    it = item(qtype="multiple_choice", options_vi=("một", "hai", "ba", "bốn"), answer=2)
    orders = set()
    for seed in range(40):
        q = mi.to_question(it, random.Random(seed))
        assert sorted(o["text"] for o in q.options) == sorted(it.options_vi)
        assert [o["id"] for o in q.options] == list("abcd")
        right = [o for o in q.options if mi.grade("multiple_choice", q.answer_key, {"option": o["id"]})]
        assert [o["text"] for o in right] == ["ba"]
        orders.add(tuple(o["text"] for o in q.options))
    assert len(orders) > 5
    assert not mi.grade("multiple_choice", q.answer_key, {"option": "z"})
    assert not mi.grade("multiple_choice", q.answer_key, {"option": 2})


def test_unknown_question_type_is_never_right():
    assert not mi.grade("matching", {}, {"pairs": []})


def test_a_type_without_a_time_at_that_tier_cannot_be_asked():
    with pytest.raises(ValueError):
        mi.to_question(item(qtype="find_mistake", tier=1))


# ------------------------------------------------------------------ the validator
def check(mutate) -> list[str]:
    raw = copy.deepcopy(raw_items())
    mutate(raw)
    return mi.validate_items(mp.subject(SUBJECT), raw, mp.cfg())


def first(raw: dict, qtype: str) -> dict:
    return next(i for i in raw["items"] if i["type"] == qtype)


BREAKAGE = {
    "wrong subject": lambda r: r.update(subject="giai_tich"),
    "unknown file key": lambda r: r.update(extra=1),
    "items not a list": lambda r: r.update(items={}),
    "duplicate id": lambda r: r["items"].append(copy.deepcopy(r["items"][0])),
    "bad id": lambda r: r["items"][0].update(id="Câu 1"),
    "unknown item key": lambda r: r["items"][0].update(hint="x"),
    "unknown skill": lambda r: r["items"][0].update(skill="dstt_t1_khong_co"),
    "tier not on this floor": lambda r: r["items"][0].update(tier=3),
    "tier out of range": lambda r: r["items"][0].update(tier=6),
    "tier is a boolean": lambda r: r["items"][0].update(tier=True),
    "type not playable yet": lambda r: r["items"][0].update(type="matching"),
    "empty prompt": lambda r: r["items"][0].update(prompt_vi=" "),
    "symbol the font may lack": lambda r: r["items"][0].update(prompt_vi="Cho x ∈ A."),
    "no solution": lambda r: r["items"][0].update(solution_vi=[]),
    "bad solution step": lambda r: r["items"][0].update(solution_vi=["ok", "A ≠ B"]),
    "reviewed not a boolean": lambda r: r["items"][0].update(reviewed="yes"),
    "true_false answer not a boolean": lambda r: first(r, "true_false").update(answer="Đúng"),
    "true_false with options": lambda r: first(r, "true_false").update(options_vi=["Đúng", "Sai"]),
    "choice with one option": lambda r: first(r, "multiple_choice").update(options_vi=["a"], answer=0),
    "choice with two equal options": lambda r: first(r, "multiple_choice").update(
        options_vi=["{1, 2}", "{1,  2}", "{3}"], answer=0),
    "choice answer out of range": lambda r: first(r, "multiple_choice").update(answer=9),
    "choice answer as text": lambda r: first(r, "multiple_choice").update(answer="a"),
    "choice answer as boolean": lambda r: first(r, "multiple_choice").update(answer=True),
    "choice option with a bad symbol": lambda r: first(r, "multiple_choice")["options_vi"].__setitem__(1, "A ∪ B"),
    "numeric answer not a number": lambda r: first(r, "numeric").update(answer="tám"),
    "numeric answer not text": lambda r: first(r, "numeric").update(answer=8),
    "numeric unordered not a boolean": lambda r: first(r, "numeric").update(unordered="yes"),
    "numeric set with a repeat": lambda r: first(r, "numeric").update(answer="1, 1, 2", unordered=True),
    "unordered on a non-numeric": lambda r: first(r, "true_false").update(unordered=True),
    "same question twice": lambda r: r["items"][1].update(skill=r["items"][0]["skill"],
                                                         prompt_vi=r["items"][0]["prompt_vi"]),
}


@pytest.mark.parametrize("name", sorted(BREAKAGE))
def test_validator_catches(name):
    errors = check(BREAKAGE[name])
    assert errors, name
    assert all(isinstance(e, str) and "\n" not in e for e in errors)


def test_validator_passes_the_untouched_file():
    assert check(lambda r: None) == []


def test_validate_all_reports_a_broken_file_as_one_line(tmp_path):
    for name in ("subjects.json", "dai_so_tuyen_tinh.json"):
        (tmp_path / name).write_text((mp.MATH_DIR / name).read_text("utf-8"), "utf-8")
    (tmp_path / "items").mkdir()
    (tmp_path / "items" / "dai_so_tuyen_tinh.json").write_text('{"subject": "dai_so_tuyen_tinh", "items": [,]}', "utf-8")
    (tmp_path / "items" / "mon_la.json").write_text("{}", "utf-8")
    errors = mi.validate_all(tmp_path)
    assert len(errors) == 2
    assert errors[0].startswith("math/items/dai_so_tuyen_tinh.json: cannot be read as JSON")
    assert errors[1] == "math/items/mon_la.json: no written subject has this id"


def test_a_subject_without_an_item_file_is_fine(tmp_path):
    for name in ("subjects.json", "dai_so_tuyen_tinh.json"):
        (tmp_path / name).write_text((mp.MATH_DIR / name).read_text("utf-8"), "utf-8")
    assert mi.validate_all(tmp_path) == []
