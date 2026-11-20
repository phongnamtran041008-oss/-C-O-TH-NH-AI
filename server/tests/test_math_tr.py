"""M11: Tối Ưu và Toán Rời Rạc - the path, the question bank of floors 1-3 (hand-written
items of all six types, generators recomputed by tools/math_verify_tr.py), the library
documents, and a player really sitting down on floor 1 through the API."""
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
from tests.test_math_loop import ask, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "toi_uu_roi_rac"
PREFIX = "tr_"
WRITTEN_FLOORS = (1, 2, 3)
ALL_TYPES = {"true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake"}
GENERATORS = sorted(g for g in mi.generators() if g.startswith("tr_g"))


@pytest.fixture(scope="module")
def recompute():
    """The recomputations of every generator of the subject: tools/math_verify.py gathers
    math_verify_tr.py (floors 1-3), _tr_t4.py and _tr_t7.py (needs sympy)."""
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module.EXPECTED
    finally:
        sys.path.remove(str(ROOT / "tools"))


def raw_items() -> dict:
    return json.loads(mi.items_path(SUBJECT).read_text("utf-8"))


# ------------------------------------------------------------------ the path
def test_the_subject_is_written_with_nine_floors_and_a_hidden_tenth():
    entry = next(e for e in mp.load_index()["subjects"] if e["id"] == SUBJECT)
    assert entry["file"] == "toi_uu_roi_rac.json"
    subject = mp.subject(SUBJECT)
    assert subject.name_vi == "Tối Ưu và Toán Rời Rạc"
    assert [f.number for f in subject.floors] == list(range(1, 11))
    assert [f.number for f in subject.floors if f.hidden] == [10]
    for f in subject.floors:
        assert 3 <= len(f.skills) <= 6, f.number
        assert all(s.id.startswith(f"tr_t{f.number}_") for s in f.skills)


def test_the_path_file_is_valid_and_prerequisites_only_look_back():
    raw = json.loads((mp.MATH_DIR / "toi_uu_roi_rac.json").read_text("utf-8"))
    assert mp.validate_subject(raw, mp.cfg()) == []
    subject = mp.subject(SUBJECT)
    for skill in subject.skills.values():
        for r in skill.requires:
            assert subject.skills[r].floor <= skill.floor, (skill.id, r)


# ------------------------------------------------------------------ the bank
def test_the_item_file_is_valid():
    assert mi.validate_items(mp.subject(SUBJECT), raw_items(), mp.cfg()) == []
    assert not [e for e in mi.validate_all() if SUBJECT in e or " tr_" in e]


@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_a_written_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= want["templates_per_floor"]
    assert sum(1 for t in templates if t.generated) >= want["generators_per_floor"]
    f = mp.subject(SUBJECT).floor(floor)
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)


@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_every_written_floor_mixes_all_six_types(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    assert {i.qtype for i in items} == ALL_TYPES
    assert all(i.tier >= 2 for i in items if i.qtype == "find_mistake")


def test_the_optional_floor_ten_is_written_too():
    """Floor 10 (phương pháp tính) has its own bank now: tests/test_math_tr_t10.py."""
    assert mi.floor_templates(SUBJECT, 10, allow_unreviewed=True)


def test_find_mistake_items_point_at_one_line_and_explain_it():
    items = [i for i in mi.bank().values() if i.subject == SUBJECT and i.qtype == "find_mistake"]
    assert len(items) >= 3 * len(WRITTEN_FLOORS)
    for it in items:
        assert 3 <= len(it.lines_vi) <= 6, it.id
        assert 0 <= it.answer < len(it.lines_vi), it.id
        assert "bước đầu tiên bị sai" in it.prompt_vi.casefold(), it.id
        assert len(it.solution_vi) >= 2, it.id


def test_every_hand_written_item_is_passed_by_its_own_answer_and_failed_by_another():
    rng = random.Random(7)
    for it in (i for i in mi.bank().values() if i.subject == SUBJECT):
        q = mi.to_question(it, rng)
        public = q.public()
        assert mi.grade(it.qtype, q.answer_key, right_answer(public, q.answer_key)), it.id
        assert not mi.grade(it.qtype, q.answer_key, wrong_answer(public, q.answer_key)), it.id


def test_everything_is_unreviewed_until_a_person_checks_it():
    raw = raw_items()
    assert all(i["reviewed"] is False for i in raw["items"])
    assert all(g["reviewed"] is False for g in raw["generators"])


# ------------------------------------------------------------------ the generators
def test_every_generator_is_listed_and_registered():
    listed = {g["id"] for part in mi.item_files(SUBJECT)        # floors 1-3, 4-6 and 7-9 are separate files
              for g in json.loads(part.read_text("utf-8")).get("generators", [])}
    registered = {g for g in math_gen.REGISTRY if g.startswith("tr_g")}
    assert listed == registered == set(GENERATORS)
    assert len(GENERATORS) >= 3 * len(WRITTEN_FLOORS)


def _expected_matches(item, want) -> bool:
    if item.qtype == "true_false":
        return bool(want) == item.answer
    got = mi.parse_numbers(item.answer)
    want = [Fraction(v) for v in want]
    return sorted(got) == sorted(want) if item.unordered else got == want


@pytest.mark.parametrize("gid", GENERATORS)
def test_every_draw_is_valid_repeatable_varied_and_recomputed(gid, recompute):
    spec = mi.generators()[gid]
    assert spec.qtype in ("true_false", "numeric")
    prints = set()
    for seed in range(200):
        item = mi.draw(spec, random.Random(seed))
        assert mi.draw_problems(spec, item) == [], (gid, seed)
        assert mi.draw(spec, random.Random(seed)) == item
        assert _expected_matches(item, recompute[gid](json.loads(item.numbers))), (gid, item.numbers, item.answer)
        prints.add(item.fingerprint)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


def test_the_recomputation_module_stands_alone():
    text = (ROOT / "tools" / "math_verify_tr.py").read_text("utf-8")
    assert "import math_verify\n" not in text and "from math_verify " not in text


# ------------------------------------------------------------------ the library
@pytest.mark.parametrize("floor", WRITTEN_FLOORS)
def test_one_document_per_written_floor_explains_every_micro_skill(floor):
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


def test_the_library_of_this_subject_is_valid():
    assert not [e for e in ml.validate_all() if SUBJECT in e]
    assert not [e for e in ml.manifest_problems() if any(b["tex"] in e for d in ml.for_floor(SUBJECT, 1)
                                                          for b in d.formulas)]


# ------------------------------------------------------------------ a player sits down
async def test_a_fresh_player_practises_floor_1_right_and_wrong(client):
    h, _ = await make(client, "roi_rac_1")
    subjects = (await client.get("/math/path", headers=h)).json()["subjects"]
    mine = next(s for s in subjects if s["id"] == SUBJECT)
    assert [f["has_questions"] for f in mine["floors"]] == [True] * 10   # floor 10 too
    assert mine["floors"][0]["playable"]
    assert mine["floors"][0]["questions"] == len(mi.floor_templates(SUBJECT, 1, True))
    run_id = await start(client, h, floor=1, subject=SUBJECT)
    results = []
    for correct in (True, True, False, True, False, False, True, True):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT and q["math"]["floor"] == 1
        assert q["math"]["skill"].startswith("tr_t1_")
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
