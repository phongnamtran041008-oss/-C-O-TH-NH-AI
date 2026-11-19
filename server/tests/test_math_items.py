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
        elif it.qtype == "find_mistake":
            right = {"line": it.answer}
            wrong = {"line": (it.answer + 1) % len(it.lines_vi)}
        elif it.qtype == "tribulation":            # M11 đợt 2: every part right / the last part wrong
            right = {"parts": [part_right(k) for k in q.answer_key["parts"]]}
            wrong = {"parts": right["parts"][:-1] + [part_wrong(q.prompt["parts"][-1], q.answer_key["parts"][-1])]}
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
    assert not mi.grade("chung_minh", {"line": 1}, {"line": 1})
    assert not mi.grade("tribulation", {"line": 1}, {"line": 1})     # (a key without parts: never right)
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
    "type not playable": lambda r: r["items"][0].update(type="chung_minh"),
    "tribulation without parts": lambda r: r["items"][0].update(type="tribulation"),
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


def copy_paths(folder) -> None:
    """subjects.json and the path file of every written subject, and no item file at all."""
    index = (mp.MATH_DIR / "subjects.json").read_text("utf-8")
    names = [e["file"] for e in json.loads(index)["subjects"] if e.get("file")]
    assert "dai_so_tuyen_tinh.json" in names and len(names) >= 4      # M11: four subjects are written
    for name in ("subjects.json", *names):
        (folder / name).write_text((mp.MATH_DIR / name).read_text("utf-8"), "utf-8")


def test_validate_all_reports_a_broken_file_as_one_line(tmp_path):
    copy_paths(tmp_path)
    (tmp_path / "items").mkdir()
    (tmp_path / "items" / "dai_so_tuyen_tinh.json").write_text('{"subject": "dai_so_tuyen_tinh", "items": [,]}', "utf-8")
    (tmp_path / "items" / "mon_la.json").write_text("{}", "utf-8")
    errors = mi.validate_all(tmp_path)
    assert len(errors) == 2
    assert errors[0].startswith("math/items/dai_so_tuyen_tinh.json: cannot be read as JSON")
    assert errors[1] == "math/items/mon_la.json: no written subject has this id"


def test_a_subject_without_an_item_file_is_fine(tmp_path):
    copy_paths(tmp_path)
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


# ------------------------------------------------------------------ find_mistake (M11)
LINES = ("Đặt y = 2x + 1.", "Chuyển vế: 2x = y - 1.", "Chia cho 3: x = (y - 1)/3.", "Vậy g(x) = (x - 1)/3.")


def mistake(n: int = 4, answer: int = 2, **over) -> mi.MathItem:
    base = dict(qtype="find_mistake", tier=2, answer=answer, lines_vi=LINES[:n],
                prompt_vi="Bước đầu tiên bị sai là bước nào?")
    base.update(over)
    return item(**base)


def test_find_mistake_is_playable_named_and_starts_at_tier_2():
    assert "find_mistake" in mi.PLAYABLE_TYPES
    assert mi.INPUTS["find_mistake"] == "find_mistake" and mi.INSTRUCTIONS_VI["find_mistake"]
    assert not mp.text_problem(mi.INSTRUCTIONS_VI["find_mistake"])
    assert mp.time_limit("find_mistake", 1) is None and mp.time_limit("find_mistake", 2) is not None


def test_find_mistake_payload_keeps_the_lines_in_order_and_never_shuffles():
    it = mistake()
    for seed in range(40):
        q = mi.to_question(it, random.Random(seed))
        assert q.input == "find_mistake" and q.options is None and q.qtype == "find_mistake"
        assert q.prompt == {"text": it.prompt_vi, "lines": list(LINES)}
        assert q.answer_key["line"] == 2 and q.answer_key["fingerprint"] == it.fingerprint
        assert q.answer_key["reveal"]["answer_text"] == f"Bước 3: {LINES[2]}"
        assert q.answer_key["reveal"]["solution_vi"] == list(it.solution_vi)
        assert q.time_limit == float(mp.time_limit("find_mistake", 2))
    public = q.public()
    assert public["instruction_vi"] == mi.INSTRUCTIONS_VI["find_mistake"] and "line" not in public["prompt"] and "line" not in public


def test_matrices_still_come_with_a_find_mistake_question():
    it = mistake(matrices=(("A", (("1", "2"), ("3", "4"))),))
    q = mi.to_question(it, random.Random(1))
    assert q.prompt["matrices"] == [{"name": "A", "rows": [["1", "2"], ["3", "4"]]}]
    assert q.prompt["lines"] == list(LINES)


@pytest.mark.parametrize("n,answer", [(3, 0), (3, 2), (4, 1), (4, 3)])
def test_find_mistake_grades_only_the_wrong_line(n, answer):
    q = mi.to_question(mistake(n, answer), random.Random(3))
    assert mi.grade("find_mistake", q.answer_key, {"line": answer}) is True
    for other in range(n):
        if other != answer:
            assert mi.grade("find_mistake", q.answer_key, {"line": other}) is False


def test_find_mistake_malformed_answers_are_wrong_never_an_error():
    q = mi.to_question(mistake(4, 1), random.Random(3))
    key = json.loads(json.dumps(q.answer_key))                 # as stored in the database
    assert mi.grade("find_mistake", key, {"line": 1})
    malformed = [None, [], "1", 1, {}, {"line": None}, {"line": True}, {"line": False}, {"line": 1.0},
                 {"line": "1"}, {"line": [1]}, {"line": {"i": 1}}, {"line": -1}, {"line": 4}, {"line": 10 ** 30},
                 {"line": float("nan")}, {"lines": 1}, {"value": True}, {"order": [1]}]
    for answer in malformed:
        assert mi.grade("find_mistake", key, answer) is False, answer
    for broken in ({}, {"line": None}, {"line": "1"}, {"line": 1.0}, {"line": True}):
        assert not mi.grade("find_mistake", broken, {"line": 1}), broken


def test_find_mistake_answer_text_names_the_step():
    assert mistake(4, 0).answer_text == f"Bước 1: {LINES[0]}"
    assert mistake(4, 3).answer_text == f"Bước 4: {LINES[3]}"


def test_find_mistake_items_build_from_data_and_the_bank_has_them_on_every_floor():
    raw = raw_items()
    subject = mp.subject(SUBJECT)
    data = first(raw, "find_mistake")
    built = mi.build_item(subject, data)
    assert built.qtype == "find_mistake" and built.lines_vi == tuple(data["lines_vi"]) and built.answer == data["answer"]
    assert not built.steps_vi and not built.pairs_vi and not built.options_vi
    assert mi.bank()[data["id"]] == built
    for floor in (1, 2, 3):
        own = [i for i in mi.floor_items(SUBJECT, floor, allow_unreviewed=True) if i.qtype == "find_mistake"]
        assert len(own) >= 2, floor
        assert len({i.skill for i in own}) >= 2, floor
        assert all(i.tier >= 2 and 3 <= len(i.lines_vi) <= 6 and 0 <= i.answer < len(i.lines_vi) for i in own)
        assert all(not i.reviewed for i in own)


def test_every_shipped_find_mistake_item_asks_for_the_first_wrong_step_and_explains_it():
    for i in mi.bank().values():
        if i.qtype != "find_mistake":
            continue
        assert "đầu tiên" in i.prompt_vi, i.id
        assert len(i.solution_vi) >= 2, i.id
        q = mi.to_question(i, random.Random(5))
        assert mi.grade("find_mistake", q.answer_key, {"line": i.answer})
        assert q.answer_key["reveal"]["answer_text"].startswith(f"Bước {i.answer + 1}: ")


FM_MESSAGES = {
    "find_mistake without lines": (lambda r: first(r, "find_mistake").pop("lines_vi"), "lines_vi must list 3 to 6 lines"),
    "find_mistake with two lines": (lambda r: first(r, "find_mistake").update(lines_vi=["a", "b"], answer=0),
                                    "lines_vi must list 3 to 6 lines"),
    "find_mistake with seven lines": (lambda r: first(r, "find_mistake").update(lines_vi=list("abcdefg"), answer=0),
                                      "lines_vi must list 3 to 6 lines"),
    "find_mistake lines as text": (lambda r: first(r, "find_mistake").update(lines_vi="a b c"),
                                   "lines_vi must list 3 to 6 lines"),
    "find_mistake with a repeated line": (lambda r: first(r, "find_mistake").update(lines_vi=["x = 1", "y = 2", "x  =  1"]),
                                          "two lines have the same text"),
    "find_mistake with an empty line": (lambda r: first(r, "find_mistake")["lines_vi"].__setitem__(1, " "),
                                        "line 2 is missing or empty"),
    "find_mistake line with a bad symbol": (lambda r: first(r, "find_mistake")["lines_vi"].__setitem__(0, "x ∈ A"),
                                            "line 1 has the character"),
    "find_mistake without an answer": (lambda r: first(r, "find_mistake").pop("answer"),
                                       "answer must be the position (from 0) of the one wrong line"),
    "find_mistake answer out of range": (lambda r: first(r, "find_mistake").update(answer=9),
                                         "answer must be the position (from 0) of the one wrong line"),
    "find_mistake answer is negative": (lambda r: first(r, "find_mistake").update(answer=-1),
                                        "answer must be the position (from 0) of the one wrong line"),
    "find_mistake answer is a boolean": (lambda r: first(r, "find_mistake").update(answer=True),
                                         "answer must be the position (from 0) of the one wrong line"),
    "find_mistake answer is text": (lambda r: first(r, "find_mistake").update(answer="2"),
                                    "answer must be the position (from 0) of the one wrong line"),
    "find_mistake with steps": (lambda r: first(r, "find_mistake").update(steps_vi=["a", "b", "c"]),
                                "only an ordering question has steps_vi"),
    "find_mistake at tier 1": (lambda r: first(r, "find_mistake").update(tier=1),
                               "a find_mistake question does not exist at tier 1"),
    "find_mistake with options": (lambda r: first(r, "find_mistake").update(options_vi=["a", "b"]),
                                  "only a multiple_choice question has options_vi"),
    "numeric with lines": (lambda r: first(r, "numeric").update(lines_vi=["a", "b", "c"]),
                           "only a find_mistake question has lines_vi"),
    "ordering with lines": (lambda r: first(r, "ordering").update(lines_vi=["a", "b", "c"]),
                            "only a find_mistake question has lines_vi"),
    "no solution for the wrong line": (lambda r: first(r, "find_mistake").update(solution_vi=[]),
                                       "solution_vi must list at least one step"),
}


@pytest.mark.parametrize("name", sorted(FM_MESSAGES))
def test_validator_explains_find_mistake_problems(name):
    mutate, message = FM_MESSAGES[name]
    errors = check(mutate)
    assert any(message in e for e in errors), errors


def test_a_find_mistake_with_the_same_prompt_but_other_lines_is_another_question():
    def twin(r):
        a = first(r, "find_mistake")
        r["items"].append({**copy.deepcopy(a), "id": "dstt_x_twin",
                           "lines_vi": ["Một dòng khác hẳn.", "Dòng thứ hai mới.", "Kết luận khác."], "answer": 1})
    assert check(twin) == []


def test_find_mistake_items_with_the_same_lines_are_the_same_question():
    def clone(r):
        a = first(r, "find_mistake")
        r["items"].append({**copy.deepcopy(a), "id": "dstt_x_clone"})
    assert any("has the same question text as" in e for e in check(clone))


def test_the_lines_count_towards_near_duplicates_only_when_they_are_alike():
    a = {"id": "a_1", "skill": "s", "type": "find_mistake", "prompt_vi": "Bước nào sai?",
         "lines_vi": ["Tính 1 + 2 = 3.", "Nhân 3 với 4 được 12.", "Vậy kết quả là 12."]}
    b = {**a, "id": "a_2", "lines_vi": ["Tính 5 + 6 = 11.", "Nhân 11 với 7 được 77.", "Vậy kết quả là 77."]}
    c = {**a, "id": "a_3", "lines_vi": ["Đặt ẩn x là số cần tìm.", "Lập phương trình bậc nhất.", "Giải ra nghiệm x."]}
    assert mi.near_duplicates([a, b]) and not mi.near_duplicates([a, c])
    assert mi.question_text(a).endswith("Vậy kết quả là 12.")


# ------------------------------------------------------------------ a subject in several files
def test_a_subject_may_keep_its_floors_in_several_item_files(tmp_path):
    """`<subject>.json` plus parts `<subject>.<part>.json`: one bank, checked as one."""
    copy_paths(tmp_path)
    folder = tmp_path / "items"
    folder.mkdir()
    whole = json.loads((mp.MATH_DIR / "items" / f"{SUBJECT}.json").read_text("utf-8"))
    floor3 = {s.id for s in mp.subject(SUBJECT).floor(3).skills}
    part = {"subject": SUBJECT,
            "items": [i for i in whole["items"] if i["skill"] in floor3],
            "generators": [g for g in whole["generators"] if g["skill"] in floor3]}
    main = {**whole, "items": [i for i in whole["items"] if i["skill"] not in floor3],
            "generators": [g for g in whole["generators"] if g["skill"] not in floor3]}
    (folder / f"{SUBJECT}.json").write_text(json.dumps(main), "utf-8")
    (folder / f"{SUBJECT}.t3.json").write_text(json.dumps(part), "utf-8")
    assert [p.name for p in mi.item_files(SUBJECT, tmp_path)] == [f"{SUBJECT}.json", f"{SUBJECT}.t3.json"]
    merged = mi.read_items(SUBJECT, tmp_path)
    assert sorted(i["id"] for i in merged["items"]) == sorted(i["id"] for i in whole["items"])
    assert sorted(g["id"] for g in merged["generators"]) == sorted(g["id"] for g in whole["generators"])
    assert mi.validate_all(tmp_path) == []
    # the rules hold across the files: an id used in both is caught ...
    twice = {**part, "items": part["items"] + [main["items"][0]]}
    (folder / f"{SUBJECT}.t3.json").write_text(json.dumps(twice), "utf-8")
    assert any("used twice" in e for e in mi.validate_all(tmp_path))
    # ... a part that names another subject is refused, and one of an unknown subject too
    (folder / f"{SUBJECT}.t3.json").write_text(json.dumps({**part, "subject": "giai_tich"}), "utf-8")
    assert any(f"{SUBJECT}.t3.json" in e and '"subject" must be' in e for e in mi.validate_all(tmp_path))
    (folder / f"{SUBJECT}.t3.json").write_text(json.dumps(part), "utf-8")
    (folder / "mon_la.t1.json").write_text("{}", "utf-8")
    assert mi.validate_all(tmp_path) == ["math/items/mon_la.t1.json: no written subject has this id"]


# ------------------------------------------------------------------ Thiên kiếp (M11 đợt 2) and tolerance
PART_TYPES = {"truefalse": "true_false", "choice": "multiple_choice", "number": "numeric"}
TRIB_PARTS = (
    mi.MathPart(qtype="numeric", prompt_vi="a) Tìm k.", answer="2"),
    mi.MathPart(qtype="multiple_choice", prompt_vi="b) Với m = 2, hệ có bao nhiêu nghiệm?",
                options_vi=("Vô số nghiệm", "Đúng một nghiệm", "Vô nghiệm"), answer=0),
    mi.MathPart(qtype="numeric", prompt_vi="c) Nhập x, y, z.", answer="-3, 2, 0"),
    mi.MathPart(qtype="true_false", prompt_vi="d) Có m làm hệ vô nghiệm.", answer=False),
)


def trib(parts=TRIB_PARTS, **over) -> mi.MathItem:
    base = dict(qtype="tribulation", tier=4, floor=5, skill="dstt_t5_so_nghiem", answer=None, parts=tuple(parts),
                prompt_vi="Cho hệ có tham số m.", solution_vi=("a) ...", "b) ...", "c) ...", "d) ..."))
    base.update(over)
    return item(**base)


def part_right(key: dict) -> dict:
    if "value" in key:
        return {"value": key["value"]}
    if "option" in key:
        return {"option": key["option"]}
    return {"text": ", ".join(key["numbers"])}


def part_wrong(shown: dict, key: dict) -> dict:
    if "value" in key:
        return {"value": not key["value"]}
    if "option" in key:
        return {"option": next(o["id"] for o in shown["options"] if o["id"] != key["option"])}
    return {"text": "987654"}


def test_tribulation_is_playable_named_and_only_at_tiers_4_and_5():
    assert "tribulation" in mi.PLAYABLE_TYPES
    assert mi.INPUTS["tribulation"] == "tribulation" and mi.INSTRUCTIONS_VI["tribulation"]
    assert not mp.text_problem(mi.INSTRUCTIONS_VI["tribulation"])
    assert [mp.time_limit("tribulation", t) for t in (1, 2, 3)] == [None, None, None]
    assert mp.time_limit("tribulation", 4) and mp.time_limit("tribulation", 5) > mp.time_limit("tribulation", 4)
    for tier in (1, 2, 3):
        with pytest.raises(ValueError):
            mi.to_question(trib(tier=tier))


def test_tribulation_payload_has_the_parts_in_order_and_keeps_the_keys_on_the_server():
    q = mi.to_question(trib(matrices=(("A", (("1", "2"), ("3", "4"))),)), random.Random(3))
    public = q.public()
    assert public["input"] == "tribulation" and public["options"] is None and public["qtype"] == "tribulation"
    assert public["prompt"]["text"] == "Cho hệ có tham số m."
    assert public["prompt"]["matrices"] == [{"name": "A", "rows": [["1", "2"], ["3", "4"]]}]
    parts = public["prompt"]["parts"]
    assert [p["text"] for p in parts] == [p.prompt_vi for p in TRIB_PARTS]
    assert [p["input"] for p in parts] == ["number", "choice", "number", "truefalse"]
    assert [set(p) for p in parts] == [{"text", "input", "options"}] * 4
    assert parts[0]["options"] is None and parts[3]["options"] is None
    assert sorted(o["text"] for o in parts[1]["options"]) == sorted(TRIB_PARTS[1].options_vi)
    text = json.dumps(public, ensure_ascii=False)
    assert "solution_vi" not in text and "fingerprint" not in text and "numbers" not in text
    key = q.answer_key
    assert set(key) == {"parts", "reveal", "fingerprint"} and key["fingerprint"] == trib().fingerprint
    assert key["parts"][0] == {"numbers": ["2"], "unordered": False, "tolerance": mp.cfg()["numeric_tolerance"]}
    assert set(key["parts"][1]) == {"option"} and key["parts"][3] == {"value": False}
    assert key["parts"][2]["numbers"] == ["-3", "2", "0"]
    right_text = next(o["text"] for o in parts[1]["options"] if o["id"] == key["parts"][1]["option"])
    assert right_text == "Vô số nghiệm"
    assert key["reveal"]["answer_text"] == "a) 2; b) Vô số nghiệm; c) -3, 2, 0; d) Sai"
    assert [p["answer_text"] for p in key["reveal"]["parts"]] == ["2", "Vô số nghiệm", "-3, 2, 0", "Sai"]
    assert [p["key"] for p in key["reveal"]["parts"]] == key["parts"]
    assert json.loads(json.dumps(key)) == key                    # the key survives the database


def test_a_choice_part_is_shuffled_like_a_choice_question_and_keeps_one_right_option():
    orders = set()
    for seed in range(40):
        q = mi.to_question(trib(), random.Random(seed))
        shown = q.prompt["parts"][1]["options"]
        assert [o["id"] for o in shown] == list("abc")
        right = [o["text"] for o in shown if mi.grade("multiple_choice", q.answer_key["parts"][1], {"option": o["id"]})]
        assert right == ["Vô số nghiệm"]
        orders.add(tuple(o["text"] for o in shown))
        # the same rng discipline as a choice question: the options of a lone choice question
        # drawn with the same seed come out in the same order
        alone = mi.to_question(item(qtype="multiple_choice", options_vi=TRIB_PARTS[1].options_vi, answer=0),
                               random.Random(seed))
        first_choice = mi.to_question(trib(parts=TRIB_PARTS[1:]), random.Random(seed)).prompt["parts"][0]["options"]
        assert [o["text"] for o in first_choice] == [o["text"] for o in alone.options]
    assert len(orders) == 6                                      # every order of three options shows up


def test_tribulation_is_right_only_when_every_part_is_right():
    for seed in range(10):
        q = mi.to_question(trib(), random.Random(seed))
        keys, shown = q.answer_key["parts"], q.prompt["parts"]
        right = [part_right(k) for k in keys]
        assert mi.grade("tribulation", q.answer_key, {"parts": right})
        for k in range(len(keys)):                               # each single part wrong
            one_wrong = right[:k] + [part_wrong(shown[k], keys[k])] + right[k + 1:]
            assert not mi.grade("tribulation", q.answer_key, {"parts": one_wrong}), k
        assert mi.grade("tribulation", q.answer_key,                 # each part by its own rule: equal forms count
                        {"parts": [{"text": "4/2"}, right[1], {"text": "-3; 2.0; 0"}, right[3]]})


MALFORMED = {
    "nothing": None, "not a dict": [1, 2], "empty": {}, "timed out": {"timed_out": True},
    "parts not a list": {"parts": {"0": {"text": "2"}}}, "parts as text": {"parts": "2, a, -3 2 0, sai"},
    "parts empty": {"parts": []}, "a part short": "short", "a part extra": "long", "part not a dict": "list",
    "part None": "none", "true/false as text": "tf_text", "true/false as 0": "tf_int",
    "option as an index": "opt_int", "number as a number": "num_int", "number not a number": "num_text",
    "another type's shape": "shape", "parts as tuple of the right answers": "nested",
}


def malformed(name: str, right: list[dict]):
    v = MALFORMED[name]
    if not isinstance(v, str) or name == "parts as text":
        return v
    p = [dict(a) for a in right]
    if v == "short":
        return {"parts": p[:-1]}
    if v == "long":
        return {"parts": p + [{"value": True}]}
    if v == "list":
        return {"parts": [list(p[0].values())] + p[1:]}
    if v == "none":
        return {"parts": [None] + p[1:]}
    if v == "tf_text":
        return {"parts": p[:3] + [{"value": "false"}]}
    if v == "tf_int":
        return {"parts": p[:3] + [{"value": 0}]}
    if v == "opt_int":
        return {"parts": [p[0], {"option": 0}] + p[2:]}
    if v == "num_int":
        return {"parts": [{"text": 2}] + p[1:]}
    if v == "num_text":
        return {"parts": [{"text": "hai"}] + p[1:]}
    if v == "shape":
        return {"parts": [{"value": True}] + p[1:]}
    return {"parts": [p]}


@pytest.mark.parametrize("name", sorted(MALFORMED))
def test_a_malformed_tribulation_answer_is_wrong_never_an_error(name):
    q = mi.to_question(trib(), random.Random(1))
    right = [part_right(k) for k in q.answer_key["parts"]]
    assert not mi.grade("tribulation", q.answer_key, malformed(name, right))


def test_a_broken_tribulation_key_is_never_right():
    for key in ({}, {"parts": []}, {"parts": "x"}, {"parts": [{"line": 1}]}, {"parts": [None, None]}):
        for given in ({"parts": [{"line": 1}]}, {"parts": [None, None]}, {"parts": []}):
            assert not mi.grade("tribulation", key, given)


def test_tribulation_items_build_from_data_and_the_seed_items_are_right():
    seed = json.loads((mp.MATH_DIR / "items" / f"{SUBJECT}.trib_seed.json").read_text("utf-8"))
    assert seed["subject"] == SUBJECT and len(seed["items"]) == 2 and seed["generators"] == []
    for raw in seed["items"]:
        it = mi.bank()[raw["id"]]
        assert it.qtype == "tribulation" and it.tier == 4 and it.floor == 5 and not it.reviewed
        assert [p.qtype for p in it.parts] == [p["type"] for p in raw["parts"]]
        assert mi.content_problems(raw, raw["id"]) == []
        assert mi._slot_problems(mp.subject(SUBJECT), raw, mp.cfg(), raw["id"]) == []
        q = mi.to_question(it, random.Random(0))
        assert mi.grade("tribulation", q.answer_key, {"parts": [part_right(k) for k in q.answer_key["parts"]]})
    assert mi.bank()["dstt_t5_so_nghiem_91"].answer_text == "a) 2; b) Vô số nghiệm; c) -3, 2, 0; d) Sai"


def raw_trib(**over) -> dict:
    base = {"id": "dstt_t5_so_nghiem_99", "skill": "dstt_t5_so_nghiem", "tier": 4, "type": "tribulation",
            "prompt_vi": "Cho hệ có tham số m.",
            "parts": [{"type": "numeric", "prompt_vi": "a) Tìm k.", "answer": "2"},
                      {"type": "multiple_choice", "prompt_vi": "b) Bao nhiêu nghiệm?",
                       "options_vi": ["Vô số", "Một", "Không"], "answer": 0},
                      {"type": "true_false", "prompt_vi": "c) Có m làm hệ vô nghiệm.", "answer": False}],
            "solution_vi": ["a) k = 2.", "b) Vô số.", "c) Sai."], "reviewed": False}
    base.update(over)
    return base


def trib_problems(raw: dict) -> list[str]:
    """Every rule of the validator that does not need a whole floor around the item."""
    return (mi._slot_problems(mp.subject(SUBJECT), raw, mp.cfg(), raw["id"])
            + mi.content_problems(raw, raw["id"]))


def with_part(k: int, **over) -> dict:
    raw = raw_trib()
    raw["parts"][k] = {**raw["parts"][k], **over}
    return raw


def without(k: int, field: str) -> dict:
    raw = raw_trib()
    raw["parts"][k].pop(field)
    return raw


I = "dstt_t5_so_nghiem_99"
TRIB_MESSAGES = {
    "one part": (raw_trib(parts=raw_trib()["parts"][:1]), f"{I}: parts must list 2 to 4 parts"),
    "five parts": (raw_trib(parts=raw_trib()["parts"] * 2), f"{I}: parts must list 2 to 4 parts"),
    "no parts": (raw_trib(parts=None), f"{I}: parts must list 2 to 4 parts"),
    "parts as text": (raw_trib(parts="a, b"), f"{I}: parts must list 2 to 4 parts"),
    "a part not a question": (raw_trib(parts=raw_trib()["parts"][:2] + ["c) ..."]),
                              f"{I} part 3: must be a question {{type, prompt_vi, answer, ...}}"),
    "a matching part": (with_part(0, type="matching"),
                        f"{I} part 1: type must be one of true_false, multiple_choice, numeric"),
    "a tribulation part": (with_part(0, type="tribulation"),
                           f"{I} part 1: type must be one of true_false, multiple_choice, numeric"),
    "a part with a solution": (with_part(2, solution_vi=["x"]),
                               f"{I} part 3: unknown key 'solution_vi' (a part has only the fields of its type)"),
    "a part with an id": (with_part(2, id="p3"), f"{I} part 3: unknown key 'id'"),
    "a part with matrices": (with_part(0, matrices={"A": [[1]]}), f"{I} part 1: unknown key 'matrices'"),
    "options on a true/false part": (with_part(2, options_vi=["Đúng", "Sai"]),
                                     f"{I} part 3: only a multiple_choice question has options_vi"),
    "unordered on a choice part": (with_part(1, unordered=True),
                                   f"{I} part 2: only a numeric question has unordered"),
    "tolerance on a true/false part": (with_part(2, tolerance=0.5),
                                       f"{I} part 3: only a numeric question has tolerance"),
    "a part without a prompt": (without(0, "prompt_vi"), f"{I} part 1: prompt_vi "),
    "a part with a bad symbol": (with_part(0, prompt_vi="a) Tìm k ∈ R."), f"{I} part 1: prompt_vi has the character"),
    "a numeric part without an answer": (without(0, "answer"),
                                         f"{I} part 1: answer must be a number, a fraction a/b or numbers separated by commas"),
    "a choice part with one option": (with_part(1, options_vi=["x"]), f"{I} part 2: options_vi must list 2 to 6 options"),
    "a choice answer out of range": (with_part(1, answer=5),
                                     f"{I} part 2: answer must be the position (from 0) of the one right option"),
    "a true/false part answered in words": (with_part(2, answer="Sai"),
                                            f"{I} part 3: the answer of a true_false question must be true or false"),
    "a numeric set with a repeat": (with_part(0, answer="1, 1", unordered=True),
                                    f"{I} part 1: an unordered answer lists the same number twice"),
    "two parts alike": (with_part(1, type="numeric", prompt_vi="A) TÌM  K.", answer="2", options_vi=None),
                        f"{I}: two parts have the same text"),
    "an answer of its own": (raw_trib(answer=0),
                             f"{I}: a tribulation question has no answer of its own: each part has its answer"),
    "options of its own": (raw_trib(options_vi=["a", "b"]), f"{I}: only a multiple_choice question has options_vi"),
    "a tolerance of its own": (raw_trib(tolerance=0.01), f"{I}: only a numeric question has tolerance"),
    "no solution": (raw_trib(solution_vi=[]), f"{I}: solution_vi must list at least one step"),
    "at tier 3": (raw_trib(tier=3), f"{I}: a tribulation question does not exist at tier 3"),
    "at tier 5 on floor 5": (raw_trib(tier=5), f"{I}: tier 5 is not allowed on floor 5 (tiers 3-4)"),
    "parts on a numeric item": (raw_trib(type="numeric", answer="2"), f"{I}: only a tribulation question has parts"),
}


@pytest.mark.parametrize("name", sorted(TRIB_MESSAGES))
def test_validator_explains_tribulation_problems(name):
    raw, message = TRIB_MESSAGES[name]
    errors = trib_problems(copy.deepcopy(raw))
    assert any(e.startswith(message) for e in errors), errors


def test_a_well_formed_tribulation_passes_and_tier_5_is_fine_where_the_floor_has_it():
    assert trib_problems(raw_trib()) == []
    assert trib_problems(raw_trib(parts=raw_trib()["parts"][:2])) == []
    four = raw_trib()["parts"] + [{"type": "numeric", "prompt_vi": "d) Nhập x, y, z.", "answer": "-3, 2, 0",
                                   "unordered": False, "tolerance": 0.001}]
    assert trib_problems(raw_trib(parts=four)) == []
    assert trib_problems(raw_trib(skill=mp.subject(SUBJECT).floor(7).skills[0].id, tier=5)) == []


def test_tribulation_and_its_keys_in_a_whole_file():
    """Through validate_items: the new keys are allowed, a generator of the type is refused, and
    a part-level problem is reported once with the item's id."""
    def add(r):
        r["items"].append(raw_trib())
    assert not [e for e in check(add) if "dstt_t5_so_nghiem_99" in e]
    def gen(r):
        r["generators"].append({"id": "dstt_g5_kiep", "skill": "dstt_t5_so_nghiem", "tier": 4, "type": "tribulation"})
    assert any("dstt_g5_kiep: a tribulation question can only be hand-written for now" in e for e in check(gen))
    def parts_on_tf(r):
        first(r, "true_false")["parts"] = raw_trib()["parts"]
    assert any("only a tribulation question has parts" in e for e in check(parts_on_tf))


def test_two_tribulations_on_one_situation_are_different_questions_unless_their_parts_are_alike():
    a = raw_trib()
    other = raw_trib(id="dstt_t5_so_nghiem_98", parts=[
        {"type": "numeric", "prompt_vi": "a) Với m = 7, tìm z.", "answer": "0"},
        {"type": "true_false", "prompt_vi": "b) Hệ có nghiệm duy nhất với mọi m khác 2.", "answer": True}])
    assert mi.near_duplicates([a, other]) == []
    a3 = raw_trib(prompt_vi="Cho hệ 3 phương trình có tham số m.")
    a4 = raw_trib(id="dstt_t5_so_nghiem_97", prompt_vi="Cho hệ 4 phương trình có tham số m.")
    assert mi.near_duplicates([a3, a4])                            # the same parts, other numbers: one question twice
    assert " | a) Tìm k. | " in mi.question_text(a) and "Vô số" in mi.question_text(a)


# ------------------------------------------------------------------ tolerance
def test_tolerance_replaces_the_global_one_only_for_its_question():
    exact = mi.to_question(item(answer="12.35")).answer_key
    assert exact["tolerance"] == mp.cfg()["numeric_tolerance"] and exact["numbers"] == ["247/20"]
    assert mi.grade("numeric", exact, {"text": "12.35"}) and not mi.grade("numeric", exact, {"text": "12.354"})
    rounded = item(answer="12.35", tolerance=0.005)
    key = mi.to_question(rounded).answer_key
    assert key["tolerance"] == 0.005 and key["numbers"] == ["247/20"]
    for text in ("12.35", "12.354", "12.346", "12.355", "247/20", "12.3500"):
        assert mi.grade("numeric", key, {"text": text}), text
    for text in ("12.356", "12.344", "12.4", "12,35", "12.35, 1", "mười hai"):
        assert not mi.grade("numeric", key, {"text": text}), text
    assert rounded.answer_text == "12.35"                            # shown as written, not 247/20
    assert item(answer="0.5").answer_text == "1/2"                   # (an exact answer: unchanged)


def test_tolerance_on_a_numeric_part_and_a_list():
    parts = (mi.MathPart(qtype="numeric", prompt_vi="a) Làm tròn đến 2 chữ số thập phân.", answer="0.68, 1.96",
                         tolerance=0.005),
             mi.MathPart(qtype="numeric", prompt_vi="b) Tìm n.", answer="3"))
    q = mi.to_question(trib(parts=parts), random.Random(0))
    a, b = q.answer_key["parts"]
    assert a["tolerance"] == 0.005 and b["tolerance"] == mp.cfg()["numeric_tolerance"]
    assert mi.grade("tribulation", q.answer_key, {"parts": [{"text": "0.684, 1.958"}, {"text": "3"}]})
    assert not mi.grade("tribulation", q.answer_key, {"parts": [{"text": "0.69, 1.96"}, {"text": "3"}]})
    assert not mi.grade("tribulation", q.answer_key, {"parts": [{"text": "0.68, 1.96"}, {"text": "3.001"}]})
    assert q.answer_key["reveal"]["answer_text"] == "a) 0.68, 1.96; b) 3"


@pytest.mark.parametrize("value", [0, -0.1, 1.5, "0.01", True, None, [0.1]])
def test_a_bad_tolerance_is_refused(value):
    raw = {"type": "numeric", "prompt_vi": "Tính.", "answer": "1.41", "solution_vi": ["x"], "tolerance": value}
    errors = mi.content_problems(raw, "it")
    if value is None:                                                # (null: no tolerance at all)
        assert errors == []
    else:
        assert errors == ["it: tolerance must be a number above 0 and at most 1"]


@pytest.mark.parametrize("value", [0.005, 1, 0.5, 1e-9])
def test_a_good_tolerance_is_accepted_and_only_on_numeric(value):
    raw = {"type": "numeric", "prompt_vi": "Tính.", "answer": "1.41", "solution_vi": ["x"], "tolerance": value}
    assert mi.content_problems(raw, "it") == []
    assert mi.content_problems({**raw, "type": "true_false", "answer": True}, "it") == \
        ["it: only a numeric question has tolerance"]


def test_tolerance_is_an_item_key_and_builds_from_data():
    def add(r):
        it = copy.deepcopy(first(r, "numeric"))
        r["items"].append({**it, "id": "dstt_x_round", "prompt_vi": "Làm tròn căn 2 đến 2 chữ số thập phân.",
                           "answer": "1.41", "tolerance": 0.005})
    assert not [e for e in check(add) if "dstt_x_round" in e]
    raw = {**first(raw_items(), "numeric"), "answer": "1.41", "tolerance": 0.005}
    assert mi.build_item(mp.subject(SUBJECT), raw).tolerance == 0.005
    assert mi.build_item(mp.subject(SUBJECT), first(raw_items(), "numeric")).tolerance is None


def test_parse_number_reads_a_rounded_decimal_the_way_the_prompt_asks_for_it():
    assert mi.parse_number("12.35") == Fraction(1235, 100)
    assert mi.parse_number("-0.05") == Fraction(-1, 20) and mi.parse_number("3.") == 3
    assert mi.parse_number("12,35") is None                          # the comma separates numbers
    assert mi.parse_numbers("12,35") == [12, 35]
