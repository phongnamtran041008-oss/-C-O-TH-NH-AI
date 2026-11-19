"""M11, second round: Tối Ưu và Toán Rời Rạc floors 4-6 - the question bank (hand-written items
of all six basic types plus Thiên kiếp on floors 5 and 6, generators recomputed by
tools/math_verify_tr_t4.py), the library documents, and a player who has cleared floors 1-3
sitting down on floor 4 through the API."""
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from tests.helpers import answer_key
from tests.test_math_loop import ask, clear_below, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "toi_uu_roi_rac"
FLOORS = (4, 5, 6)
BASIC_TYPES = {"true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake"}
PART_FILE = mi.items_path(SUBJECT).with_name(f"{SUBJECT}.t4_6.json")
GENERATORS = sorted(g for g in math_gen.REGISTRY if g[:6] in ("tr_g4_", "tr_g5_", "tr_g6_"))


@pytest.fixture(scope="module")
def recompute():
    """tools/math_verify_tr_t4.py EXPECTED (needs sympy)."""
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_tr_t4 as module
        yield module.EXPECTED
    finally:
        sys.path.remove(str(ROOT / "tools"))


def raw_part() -> dict:
    return json.loads(PART_FILE.read_text("utf-8"))


def my_items() -> list:
    return [i for i in mi.bank().values() if i.subject == SUBJECT and i.floor in FLOORS]


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_4_to_6_and_the_subject_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    skills = mp.subject(SUBJECT).skills
    assert {skills[i["skill"]].floor for i in raw["items"]} == set(FLOORS)
    assert {skills[g["skill"]].floor for g in raw["generators"]} == set(FLOORS)
    assert all(i["id"].startswith(("tr_t4_", "tr_t5_", "tr_t6_")) for i in raw["items"])
    assert not [e for e in mi.validate_all() if SUBJECT in e or " tr_" in e]


@pytest.mark.parametrize("floor", FLOORS)
def test_a_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert sum(1 for t in templates if t.generated) >= max(want["generators_per_floor"], 8)
    f = mp.subject(SUBJECT).floor(floor)
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)


@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_has_the_six_basic_types_and_the_upper_floors_two_tribulations(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    assert BASIC_TYPES <= {i.qtype for i in items}
    tribulations = [i for i in items if i.qtype == "tribulation"]
    if floor >= 5:
        assert len(tribulations) >= 2
    assert all(t.tier == 4 and 2 <= len(t.parts) <= 4 for t in tribulations)
    assert all(i.tier >= 2 for i in items if i.qtype == "find_mistake")
    assert not [i.id for i in items if i.tier == 5]          # no tier 5 below floor 7: no ladders here


def test_find_mistake_items_point_at_one_line_and_explain_it():
    items = [i for i in my_items() if i.qtype == "find_mistake"]
    assert len(items) >= 3 * len(FLOORS)
    for it in items:
        assert 0 <= it.answer < len(it.lines_vi), it.id
        assert "bước đầu tiên bị sai" in it.prompt_vi.casefold(), it.id
        assert len(it.solution_vi) >= 2, it.id


def test_graphs_and_traversals_are_given_unambiguously():
    """A graph is text: an edge list, adjacency lists or a matrix; a traversal fixes its tie-break."""
    asked = 0
    for it in my_items():
        text = " ".join([it.prompt_vi] + [p.prompt_vi for p in it.parts]).casefold()
        if ("bfs" in text or "dfs" in text) and "nhập thứ tự thăm" in text:     # the answer is a visiting order
            assert "thứ tự số tăng dần" in text, it.id
            assert "các cạnh" in text or "ke(" in text, it.id
            asked += 1
    assert asked >= 2


def _answers(q: dict, key: dict) -> tuple[dict, dict]:
    return right_answer(q, key), wrong_answer(q, key)


def test_every_hand_written_item_is_passed_by_its_own_answer_and_failed_by_another():
    rng = random.Random(11)
    for it in my_items():
        q = mi.to_question(it, rng)
        public = q.public()
        right, wrong = _answers(public, q.answer_key)
        assert mi.grade(it.qtype, q.answer_key, right), it.id
        assert not mi.grade(it.qtype, q.answer_key, wrong), it.id


def test_a_tribulation_is_right_only_when_every_part_is_right():
    rng = random.Random(5)
    for it in (i for i in my_items() if i.qtype == "tribulation"):
        q = mi.to_question(it, rng)
        public = q.public()
        right = right_answer(public, q.answer_key)
        assert len(public["prompt"]["parts"]) == len(it.parts)
        for k in range(len(it.parts)):
            broken = [dict(p) for p in right["parts"]]
            broken[k] = {}                                    # a missing part is wrong, never an error
            assert not mi.grade(it.qtype, q.answer_key, {"parts": broken}), (it.id, k)
        assert not mi.grade(it.qtype, q.answer_key, {"parts": right["parts"][:-1]}), it.id


def test_everything_is_unreviewed_until_a_person_checks_it():
    raw = raw_part()
    assert all(i["reviewed"] is False for i in raw["items"])
    assert all(g["reviewed"] is False for g in raw["generators"])


# ------------------------------------------------------------------ the generators
def test_every_generator_is_listed_and_registered():
    listed = {g["id"] for g in raw_part()["generators"]}
    assert listed == set(GENERATORS)
    assert all(mi.generators()[g].qtype in ("true_false", "numeric") for g in GENERATORS)


def _expected_matches(item, want) -> bool:
    if item.qtype == "true_false":
        return bool(want) == item.answer
    got = mi.parse_numbers(item.answer)
    want = [Fraction(v) for v in want]
    return sorted(got) == sorted(want) if item.unordered else got == want


@pytest.mark.parametrize("gid", GENERATORS)
def test_every_draw_is_valid_repeatable_varied_and_recomputed(gid, recompute):
    spec = mi.generators()[gid]
    prints, answers = set(), set()
    for seed in range(200):
        item = mi.draw(spec, random.Random(seed))
        assert mi.draw_problems(spec, item) == [], (gid, seed)
        assert mi.draw(spec, random.Random(seed)) == item
        assert _expected_matches(item, recompute[gid](json.loads(item.numbers))), (gid, item.numbers, item.answer)
        prints.add(item.fingerprint)
        answers.add(str(item.answer))
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]
    if spec.qtype == "true_false":
        assert answers == {"True", "False"}, gid             # both answers really occur


def test_the_recomputation_module_stands_alone():
    text = (ROOT / "tools" / "math_verify_tr_t4.py").read_text("utf-8")
    assert "import math_verify\n" not in text and "from math_verify " not in text


# ------------------------------------------------------------------ the library
@pytest.mark.parametrize("floor", FLOORS)
def test_one_document_per_floor_explains_every_micro_skill(floor):
    (doc,) = ml.for_floor(SUBJECT, floor)
    skills = [s.id for s in mp.subject(SUBJECT).floor(floor).skills]
    assert list(doc.skills) == skills
    blocks = list(doc.blocks)
    starts = [n for n, b in enumerate(blocks) if b["type"] == "section"]
    assert [blocks[n]["skill"] for n in starts] == skills
    for n, end in zip(starts, starts[1:] + [len(blocks)]):
        part = blocks[n:end]
        assert any(b["type"] == "note" and b["text"].startswith("Lỗi thường gặp") for b in part), blocks[n]
    assert doc.formulas


def test_the_library_of_floors_4_to_6_is_valid_and_its_pictures_are_built():
    names = {f"t{f}_" for f in FLOORS}
    assert not [e for e in ml.validate_all() if SUBJECT in e and any(n in e for n in names)]
    texs = {b["tex"] for f in FLOORS for d in ml.for_floor(SUBJECT, f) for b in d.formulas}
    assert not [e for e in ml.manifest_problems() if any(t in e for t in texs)]


# ------------------------------------------------------------------ a player sits down
async def test_a_player_who_cleared_floors_1_to_3_practises_floor_4_right_and_wrong(client):
    h, uid = await make(client, "roi_rac_4")
    await clear_below(uid, 4, subject=SUBJECT)
    subjects = (await client.get("/math/path", headers=h)).json()["subjects"]
    mine = next(s for s in subjects if s["id"] == SUBJECT)
    floor4 = mine["floors"][3]
    assert floor4["has_questions"] and floor4["playable"]
    assert floor4["questions"] == len(mi.floor_templates(SUBJECT, 4, True))
    run_id = await start(client, h, floor=4, subject=SUBJECT)
    results = []
    for correct in (True, False, True, True, False, True, False, True):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT
        if not q["math"].get("review"):                       # (rule 6b may bring a question from below)
            assert q["math"]["floor"] == 4 and q["math"]["skill"].startswith("tr_t4_")
            assert q["math"]["tier"] in (2, 3)
        key = await answer_key(q["session_id"])
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["correct"] is correct, (q["qtype"], q["prompt"])
        assert res["reveal"]["solution_vi"]
        results.append(res)
    assert results[-1]["math"]["run"]["asked"] == 8
    assert results[-1]["math"]["run"]["correct"] == 5
