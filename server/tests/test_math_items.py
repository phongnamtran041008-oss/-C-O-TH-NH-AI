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
        if it.qtype == "matching":
            right = {"pairs": list(q.answer_key["pairs"])}
            wrong = {"pairs": right["pairs"][1:] + right["pairs"][:1]}
        elif it.qtype == "ordering":
            right = {"order": list(q.answer_key["order"])}
            wrong = {"order": right["order"][::-1]}
        elif it.qtype == "true_false":
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
    assert not mi.grade("find_mistake", {}, {"pairs": []})
    assert not mi.grade("matching", {}, {"pairs": []})        # (a key without pairs: never right)
    assert not mi.grade("ordering", {"order": "012"}, {"order": "012"})


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
    "type not playable yet": lambda r: r["items"][0].update(type="tribulation"),
    "true_false turned matching without pairs": lambda r: first(r, "true_false").update(type="matching"),
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
    "matching without pairs": lambda r: first(r, "matching").pop("pairs_vi"),
    "matching with two pairs": lambda r: first(r, "matching").update(pairs_vi=[["a", "1"], ["b", "2"]]),
    "matching with six pairs": lambda r: first(r, "matching").update(
        pairs_vi=[[f"trái {k}", f"phải {k}"] for k in range(6)]),
    "matching pair of three sides": lambda r: first(r, "matching")["pairs_vi"].__setitem__(0, ["a", "b", "c"]),
    "matching pair as text": lambda r: first(r, "matching")["pairs_vi"].__setitem__(0, "a - b"),
    "matching with a repeated left side": lambda r: first(r, "matching")["pairs_vi"].__setitem__(
        1, [first(r, "matching")["pairs_vi"][0][0].upper(), "khác hẳn"]),
    "matching with a repeated right side": lambda r: first(r, "matching")["pairs_vi"].__setitem__(
        1, ["khác hẳn", first(r, "matching")["pairs_vi"][0][1].replace(" ", "  ")]),
    "matching side with a bad symbol": lambda r: first(r, "matching")["pairs_vi"].__setitem__(0, ["A ∪ B", "x"]),
    "matching side not text": lambda r: first(r, "matching")["pairs_vi"].__setitem__(0, ["a", 5]),
    "matching with an answer": lambda r: first(r, "matching").update(answer=[0, 1, 2, 3]),
    "matching with steps": lambda r: first(r, "matching").update(steps_vi=["a", "b", "c"]),
    "matching with options": lambda r: first(r, "matching").update(options_vi=["a", "b"]),
    "ordering without steps": lambda r: first(r, "ordering").pop("steps_vi"),
    "ordering with two steps": lambda r: first(r, "ordering").update(steps_vi=["một", "hai"]),
    "ordering with seven steps": lambda r: first(r, "ordering").update(steps_vi=[f"bước {k}" for k in range(7)]),
    "ordering with a repeated step": lambda r: first(r, "ordering")["steps_vi"].append(
        first(r, "ordering")["steps_vi"][0].casefold()),
    "ordering with an empty step": lambda r: first(r, "ordering")["steps_vi"].__setitem__(1, " "),
    "ordering steps as text": lambda r: first(r, "ordering").update(steps_vi="bước 1, bước 2, bước 3"),
    "ordering with an answer": lambda r: first(r, "ordering").update(answer=0),
    "ordering with pairs": lambda r: first(r, "ordering").update(pairs_vi=[["a", "1"], ["b", "2"], ["c", "3"]]),
    "numeric with steps": lambda r: first(r, "numeric").update(steps_vi=["a", "b", "c"]),
    "true_false with pairs": lambda r: first(r, "true_false").update(pairs_vi=[["a", "1"], ["b", "2"], ["c", "3"]]),
    "same ordering question twice": lambda r: r["items"].append(
        {**copy.deepcopy(first(r, "ordering")), "id": "dstt_x_twin"}),
    "same matching question with other numbers": lambda r: r["items"].append(
        {**copy.deepcopy(first(r, "matching")), "id": "dstt_x_twin",
         "pairs_vi": [[a, b.replace("2", "7")] for a, b in first(r, "matching")["pairs_vi"]]}),
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


# ------------------------------------------------------------------ matching and ordering (M9)
PAIRS = (("A hợp B", "{1, 2, 3}"), ("A giao B", "{2}"), ("A \\ B", "{1}"), ("B \\ A", "{3}"))
STEPS = ("Đặt y = 2x + 1.", "Chuyển vế: 2x = y - 1.", "Chia cho 2: x = (y - 1)/2.", "Vậy g(x) = (x - 1)/2.")


def matching(n: int = 4, **over) -> mi.MathItem:
    return item(qtype="matching", answer=None, pairs_vi=PAIRS[:n], prompt_vi="Ghép phép toán với kết quả.", **over)


def ordering(n: int = 4, **over) -> mi.MathItem:
    return item(qtype="ordering", answer=None, steps_vi=STEPS[:n], prompt_vi="Sắp xếp các bước.", **over)


def test_the_new_types_are_playable_and_named():
    for qtype in ("matching", "ordering"):
        assert qtype in mi.PLAYABLE_TYPES
        assert mi.INPUTS[qtype] == qtype and mi.INSTRUCTIONS_VI[qtype]
        assert not mp.text_problem(mi.INSTRUCTIONS_VI[qtype])
        assert mp.time_limit(qtype, 1) is not None


def test_the_seed_bank_has_matching_and_ordering_on_every_written_floor():
    """At least two of each per floor, on at least two micro-skills, and at the floor's
    lowest tier too (a chiêu cast by a new player needs a question at tier 1 / tier 2)."""
    for floor in (1, 2, 3):
        lowest = mp.floor_tiers(floor)[0]
        items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
        for qtype in ("matching", "ordering"):
            own = [i for i in items if i.qtype == qtype]
            assert len(own) >= 2, (floor, qtype)
            assert len({i.skill for i in own}) >= 2, (floor, qtype)
            assert any(i.tier == lowest for i in own), (floor, qtype)
            assert all(i.answer is None and not i.options_vi for i in own)


def test_matching_payload_keeps_left_and_shuffles_right():
    it = matching()
    q = mi.to_question(it, random.Random(3))
    public = q.public()
    assert public["input"] == "matching" and public["options"] is None and public["qtype"] == "matching"
    assert public["instruction_vi"] == mi.INSTRUCTIONS_VI["matching"]
    assert set(public["prompt"]) == {"text", "left", "right"}
    assert public["prompt"]["text"] == it.prompt_vi
    assert public["prompt"]["left"] == [left for left, _ in PAIRS]
    assert sorted(public["prompt"]["right"]) == sorted(right for _, right in PAIRS)
    assert "pairs" not in json.dumps(public) and "order" not in json.dumps(public)
    key = q.answer_key["pairs"]
    for k, left in enumerate(public["prompt"]["left"]):          # the key points at left k's own right side
        assert dict(PAIRS)[left] == public["prompt"]["right"][key[k]]
    assert set(q.answer_key) == {"pairs", "reveal", "fingerprint"}
    assert q.answer_key["reveal"]["answer_text"] == "A hợp B — {1, 2, 3}; A giao B — {2}; A \\ B — {1}; B \\ A — {3}"
    assert q.answer_key["reveal"]["solution_vi"] == list(it.solution_vi)


def test_ordering_payload_shuffles_the_steps():
    it = ordering()
    q = mi.to_question(it, random.Random(3))
    public = q.public()
    assert public["input"] == "ordering" and public["options"] is None
    assert set(public["prompt"]) == {"text", "steps"}
    shown = public["prompt"]["steps"]
    assert sorted(shown) == sorted(STEPS)
    assert [shown[i] for i in q.answer_key["order"]] == list(STEPS)
    assert set(q.answer_key) == {"order", "reveal", "fingerprint"}
    assert q.answer_key["reveal"]["answer_text"] == "  ".join(f"{k}. {s}" for k, s in enumerate(STEPS, 1))


def test_matrices_still_come_with_a_matching_question():
    q = mi.to_question(matching(matrices=(("A", (("1", "2"),)),)), random.Random(1))
    assert q.prompt["matrices"] == [{"name": "A", "rows": [["1", "2"]]}]
    assert set(q.prompt) == {"text", "left", "right", "matrices"}


@pytest.mark.parametrize("n", [3, 4])
def test_the_shuffle_never_shows_the_answer(n):
    """An ordering question is never shown already solved, a matching one never with every
    right side next to its own left; and the shuffle really varies."""
    seen_steps, seen_right = set(), set()
    for seed in range(300):
        q = mi.to_question(ordering(n), random.Random(seed))
        assert q.prompt["steps"] != list(STEPS[:n]), seed
        assert q.answer_key["order"] != list(range(n)), seed
        seen_steps.add(tuple(q.prompt["steps"]))
        m = mi.to_question(matching(n), random.Random(seed))
        assert m.prompt["right"] != [right for _, right in PAIRS[:n]], seed
        assert m.answer_key["pairs"] != list(range(n)), seed
        seen_right.add(tuple(m.prompt["right"]))
    import math
    assert len(seen_steps) == len(seen_right) == math.factorial(n) - 1     # every other order shows up


def test_shown_order_is_a_permutation_that_moves_something():
    for n in range(2, 8):
        for seed in range(50):
            order = mi.shown_order(n, random.Random(seed))
            assert sorted(order) == list(range(n)) and order != list(range(n))
    assert mi.shown_order(1, random.Random(0)) == [0]


def test_matching_and_ordering_grade_only_the_exact_key():
    for qtype, name, it in (("matching", "pairs", matching()), ("ordering", "order", ordering())):
        q = mi.to_question(it, random.Random(5))
        key = q.answer_key[name]
        assert mi.grade(qtype, q.answer_key, {name: list(key)})
        assert mi.grade(qtype, q.answer_key, {name: tuple(key)})       # (same values, any sequence)
        # every other permutation is wrong
        import itertools
        others = [list(p) for p in itertools.permutations(range(len(key))) if list(p) != key]
        assert others and not any(mi.grade(qtype, q.answer_key, {name: p}) for p in others)
        other_name = "order" if name == "pairs" else "pairs"
        malformed = [
            None, [], "0123", {name: None}, {name: ""}, {name: "0,1,2,3"}, {name: []}, {name: key[:-1]},
            {name: key + [len(key)]}, {name: [key[0]] * len(key)},                  # wrong length, repeats
            {name: [key[0], key[0]] + key[2:]},                                       # a repeated index
            {name: [k + 1 for k in key]}, {name: [-1] + key[1:]},                    # out of range
            {name: [float(k) for k in key]}, {name: [str(k) for k in key]},          # not ints
            {name: [bool(k) if k in (0, 1) else k for k in key]},                    # bools are not indices
            {name: {str(k): v for k, v in enumerate(key)}},                          # a dict, not a list
            {name: [[k] for k in key]}, {name: [None] * len(key)},
            {other_name: list(key)}, {},                                             # the wrong field / none
        ]
        for answer in malformed:
            assert mi.grade(qtype, q.answer_key, answer) is False, (qtype, answer)


def test_a_broken_answer_key_is_never_right():
    for qtype, name in (("matching", "pairs"), ("ordering", "order")):
        for key in ({}, {name: None}, {name: "012"}, {name: 3}):
            assert not mi.grade(qtype, key, {name: [0, 1, 2]})


def test_matching_and_ordering_keys_survive_json():
    """The key is stored in the database as JSON and graded after a round trip."""
    for qtype, name, it in (("matching", "pairs", matching(5)), ("ordering", "order", ordering(4))):
        q = mi.to_question(it, random.Random(11))
        stored = json.loads(json.dumps(q.answer_key))
        sent = json.loads(json.dumps({name: q.answer_key[name]}))
        assert mi.grade(qtype, stored, sent)


def test_matching_and_ordering_items_build_from_data():
    raw = raw_items()
    subject = mp.subject(SUBJECT)
    for qtype in ("matching", "ordering"):
        data = first(raw, qtype)
        built = mi.build_item(subject, data)
        assert built.qtype == qtype and built.answer is None
        if qtype == "matching":
            assert built.pairs_vi == tuple(tuple(p) for p in data["pairs_vi"]) and not built.steps_vi
        else:
            assert built.steps_vi == tuple(data["steps_vi"]) and not built.pairs_vi
        assert mi.bank()[data["id"]] == built


NEW_TYPE_MESSAGES = {
    "matching without pairs": "pairs_vi must list 3 to 5 pairs",
    "matching with two pairs": "pairs_vi must list 3 to 5 pairs",
    "matching with six pairs": "pairs_vi must list 3 to 5 pairs",
    "matching pair of three sides": "pair 1 must be [left side, right side]",
    "matching pair as text": "pair 1 must be [left side, right side]",
    "matching with a repeated left side": "two left sides have the same text",
    "matching with a repeated right side": "two right sides have the same text",
    "matching side with a bad symbol": "pair 1 left side has the character",
    "matching side not text": "pair 1 right side is missing or empty",
    "matching with an answer": "matching questions have no answer key",
    "matching with steps": "only an ordering question has steps_vi",
    "matching with options": "only a multiple_choice question has options_vi",
    "ordering without steps": "steps_vi must list 3 to 6 steps",
    "ordering with two steps": "steps_vi must list 3 to 6 steps",
    "ordering with seven steps": "steps_vi must list 3 to 6 steps",
    "ordering with a repeated step": "two steps have the same text",
    "ordering with an empty step": "step 2 is missing or empty",
    "ordering steps as text": "steps_vi must list 3 to 6 steps",
    "ordering with an answer": "ordering questions have no answer key",
    "ordering with pairs": "only a matching question has pairs_vi",
    "numeric with steps": "only an ordering question has steps_vi",
    "true_false with pairs": "only a matching question has pairs_vi",
    "true_false turned matching without pairs": "pairs_vi must list 3 to 5 pairs",
    "same ordering question twice": "has the same question text as",
    "same matching question with other numbers": "is almost the same question as",
}


@pytest.mark.parametrize("name", sorted(NEW_TYPE_MESSAGES))
def test_validator_explains_matching_and_ordering_problems(name):
    errors = check(BREAKAGE[name])
    assert any(NEW_TYPE_MESSAGES[name] in e for e in errors), errors


def test_ordering_questions_with_one_prompt_but_other_steps_are_different_questions():
    """Two ordering items may share a prompt like "Sắp xếp các bước..." when their steps differ."""
    def twin(r):
        a = first(r, "ordering")
        r["items"].append({**copy.deepcopy(a), "id": "dstt_x_twin",
                           "steps_vi": ["Một bước khác hẳn.", "Bước thứ hai mới.", "Kết luận khác."]})
    assert check(twin) == []
