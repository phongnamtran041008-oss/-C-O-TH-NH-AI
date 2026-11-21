"""M11, second round: Tối Ưu và Toán Rời Rạc floors 7-9 - the question bank (hand-written items
of all six basic types plus Thiên kiếp on every floor, a ladder on every tier-5 item, generators
recomputed by tools/math_verify_tr_t7.py), the library documents, and a player who has cleared
floors 1-6 sitting down on floor 7 through the API."""
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
FLOORS = (7, 8, 9)
BASIC_TYPES = {"true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake"}
PART_FILE = mi.items_path(SUBJECT).with_name(f"{SUBJECT}.t7_9.json")
GENERATORS = sorted(g for g in math_gen.REGISTRY if g[:6] in ("tr_g7_", "tr_g8_", "tr_g9_"))


@pytest.fixture(scope="module")
def recompute():
    """tools/math_verify_tr_t7.py EXPECTED (needs sympy)."""
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_tr_t7 as module
        import math_verify_rasoat
        # the curriculum review's generators (tools/math_verify_rasoat.py) sit on these floors too
        mine = {k: v for k, v in math_verify_rasoat.EXPECTED.items() if k.startswith(('tr_g7_', 'tr_g8_', 'tr_g9_'))}
        yield {**module.EXPECTED, **mine}
    finally:
        sys.path.remove(str(ROOT / "tools"))


def raw_part() -> dict:
    return json.loads(PART_FILE.read_text("utf-8"))


def my_items() -> list:
    return [i for i in mi.bank().values() if i.subject == SUBJECT and i.floor in FLOORS]


def templates_by_id() -> dict:
    """Every template of the subject (hand-written or generator): id -> (floor, tier)."""
    out = {i.id: (i.floor, i.tier) for i in mi.bank().values() if i.subject == SUBJECT}
    out.update({g.id: (g.floor, g.tier) for g in mi.generators().values() if g.subject == SUBJECT})
    return out


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_7_to_9_and_the_subject_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    skills = mp.subject(SUBJECT).skills
    assert {skills[i["skill"]].floor for i in raw["items"]} == set(FLOORS)
    assert {skills[g["skill"]].floor for g in raw["generators"]} == set(FLOORS)
    assert all(i["id"].startswith(("tr_t7_", "tr_t8_", "tr_t9_")) for i in raw["items"])
    mine = {i["id"] for i in raw["items"]} | {g["id"] for g in raw["generators"]}
    assert not [e for e in mi.validate_all() if any(m in e for m in mine) or "t7_9" in e]


@pytest.mark.parametrize("floor", FLOORS)
def test_a_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert sum(1 for t in templates if t.generated) >= max(want["generators_per_floor"], 9)
    f = mp.subject(SUBJECT).floor(floor)
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)
    assert {t.tier for t in templates} == set(f.tiers)


@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_has_the_six_basic_types_and_two_tribulations(floor):
    items = mi.floor_items(SUBJECT, floor, allow_unreviewed=True)
    assert BASIC_TYPES <= {i.qtype for i in items}
    tribulations = [i for i in items if i.qtype == "tribulation"]
    assert len(tribulations) >= 2
    assert all(t.tier in (4, 5) and 2 <= len(t.parts) <= 4 for t in tribulations)
    assert all(i.tier >= 4 for i in items)


def test_every_tier_5_item_has_a_valid_ladder_and_only_those():
    where = templates_by_id()
    tier5 = [i for i in my_items() if i.tier == 5]
    assert len(tier5) >= 30
    for it in my_items():
        if it.tier != 5:
            assert not it.ladder, it.id
            continue
        assert 2 <= len(it.ladder) <= 4, it.id
        assert len(set(it.ladder)) == len(it.ladder) and it.id not in it.ladder, it.id
        rungs = [where[r] for r in it.ladder]             # KeyError: a rung that does not exist
        assert all(tier in (3, 4) and floor <= it.floor for floor, tier in rungs), (it.id, rungs)
        assert any(tier == 4 for _, tier in rungs), it.id
    # floor 9 has only tier 5, so its ladders point down
    assert all(where[r][0] < 9 for i in tier5 if i.floor == 9 for r in i.ladder)


def test_find_mistake_items_point_at_one_line_and_explain_it():
    items = [i for i in my_items() if i.qtype == "find_mistake"]
    assert len(items) >= 3 * len(FLOORS)
    for it in items:
        assert 0 <= it.answer < len(it.lines_vi), it.id
        assert "bước đầu tiên bị sai" in it.prompt_vi.casefold(), it.id
        assert len(it.solution_vi) >= 2, it.id


def test_graphs_and_networks_are_given_as_weighted_edge_lists():
    """No picture of a graph: a weighted graph lists every edge with its weight, a network
    every arc with its capacity, and the matrices field (4 x 4 at most) is not used for them."""
    asked = 0
    for it in my_items():
        if it.floor != 7:
            continue
        text = " ".join([it.prompt_vi] + [p.prompt_vi for p in it.parts])
        if "trọng số trong ngoặc" in text:
            assert "các cạnh" in text or "các cung" in text, it.id
            asked += 1
        if "khả năng thông qua trong ngoặc" in text:
            assert "đỉnh phát" in text and "đỉnh thu" in text and "->" in text, it.id
            asked += 1
        assert not it.matrices, it.id
    assert asked >= 8


def test_every_hand_written_item_is_passed_by_its_own_answer_and_failed_by_another():
    rng = random.Random(17)
    for it in my_items():
        q = mi.to_question(it, rng)
        public = q.public()
        right, wrong = right_answer(public, q.answer_key), wrong_answer(public, q.answer_key)
        assert mi.grade(it.qtype, q.answer_key, right), it.id
        assert not mi.grade(it.qtype, q.answer_key, wrong), it.id


def test_a_tribulation_is_right_only_when_every_part_is_right():
    rng = random.Random(9)
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
    # plus the generators the curriculum review added (items/<subject>.rasoat.json) on these floors
    review = json.loads(PART_FILE.with_name(f"{SUBJECT}.rasoat.json").read_text("utf-8"))["generators"]
    listed |= {g["id"] for g in review if g["id"].startswith(('tr_g7_', 'tr_g8_', 'tr_g9_'))}
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
    text = (ROOT / "tools" / "math_verify_tr_t7.py").read_text("utf-8")
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
        # a worked case in some form: a "Ví dụ", a list of steps, or a self-check with its answer
        assert any(b["type"] in ("steps", "check") or (b["type"] == "text" and "Ví dụ" in b["text"])
                   for b in part), blocks[n]
    assert any(b["type"] in ("formula", "figure", "matrices") for b in doc.blocks)


def test_the_library_of_floors_7_to_9_is_valid_and_its_pictures_are_built():
    names = {f"t{f}_" for f in FLOORS}
    assert not [e for e in ml.validate_all() if SUBJECT in e and any(n in e for n in names)]
    texs = {b["tex"] for f in FLOORS for d in ml.for_floor(SUBJECT, f) for b in d.formulas}
    assert not [e for e in ml.manifest_problems() if any(t in e for t in texs)]


# ------------------------------------------------------------------ a player sits down
async def test_a_player_who_cleared_floors_1_to_6_practises_floor_7_right_and_wrong(client):
    h, uid = await make(client, "roi_rac_7")
    await clear_below(uid, 7, subject=SUBJECT)
    subjects = (await client.get("/math/path", headers=h)).json()["subjects"]
    mine = next(s for s in subjects if s["id"] == SUBJECT)
    floor7 = mine["floors"][6]
    assert floor7["has_questions"] and floor7["playable"]
    assert floor7["questions"] == len(mi.floor_templates(SUBJECT, 7, True))
    run_id = await start(client, h, floor=7, subject=SUBJECT)
    results, qtypes = [], set()
    pattern = (True, False, True, True, False, True, False, True, True, False)
    for correct in pattern:
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT
        if not q["math"].get("review") and not q["math"].get("ladder"):   # (rules 6b and 8 may reach below)
            assert q["math"]["floor"] == 7 and q["math"]["skill"].startswith("tr_t7_")
            assert q["math"]["tier"] in (4, 5)
        qtypes.add(q["qtype"])
        key = await answer_key(q["session_id"])
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["correct"] is correct, (q["qtype"], q["prompt"])
        assert res["reveal"]["solution_vi"]
        results.append(res)
    assert results[-1]["math"]["run"]["asked"] == len(pattern)
    assert results[-1]["math"]["run"]["correct"] == sum(pattern)
