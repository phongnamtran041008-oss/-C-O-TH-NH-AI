"""M11 round 2: Đại Số Tuyến Tính floors 4-6 (nhân ma trận; hệ phương trình và khử Gauss;
định thức, hạng, nghịch đảo) - the question bank meets the targets and the contract (every
basic type on every floor, Thiên kiếp from floor 5 up), every generator draw is valid and
recomputed with sympy, the library explains every micro-skill, and a player who has cleared
floors 1-3 plays floor 4 through the API."""
import json
import random
import sys
from pathlib import Path

import pytest

from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from tests.helpers import answer_key
from tests.test_math_loop import ask, clear_below, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "dai_so_tuyen_tinh"
FLOORS = (4, 5, 6)
PART_FILE = ROOT / "server" / "data" / "math" / "items" / f"{SUBJECT}.t4_6.json"
BASIC = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_TYPES = ("true_false", "multiple_choice", "numeric")
DRAWS = 200


def subject():
    return mp.subject(SUBJECT)


def raw_items() -> list[dict]:
    """The hand-written items of floors 4-6 as written (a tribulation keeps its parts here)."""
    return json.loads(PART_FILE.read_text("utf-8"))["items"]


def floor_of(skill: str) -> int:
    return subject().skills[skill].floor


def my_generators() -> list[mi.GeneratorSpec]:
    return [g for g in mi.generators().values() if g.subject == SUBJECT and g.floor in FLOORS]


@pytest.fixture(scope="module")
def expected():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_dstt_t4 as module
        import math_verify_rasoat
        # the curriculum review's generators (tools/math_verify_rasoat.py) sit on these floors too
        mine = {k: v for k, v in math_verify_rasoat.EXPECTED.items() if k.startswith(('dstt_g4_', 'dstt_g5_', 'dstt_g6_'))}
        yield {**module.EXPECTED, **mine}
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the path
def test_the_floors_keep_their_micro_skills_and_never_point_forward():
    s = subject()
    for floor in FLOORS:
        skills = s.floor(floor).skills
        assert 3 <= len(skills) <= 6
        for skill in skills:
            assert skill.id.startswith(f"dstt_t{floor}_")
            assert all(s.skills[r].floor <= floor for r in skill.requires), skill.id
    assert not [e for e in mp.validate_all() if "dstt_t4" in e or "dstt_t5" in e or "dstt_t6" in e]


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_four_to_six_with_unique_ids():
    data = json.loads(PART_FILE.read_text("utf-8"))
    assert data["subject"] == SUBJECT
    ids = [i["id"] for i in data["items"]] + [g["id"] for g in data["generators"]]
    assert len(ids) == len(set(ids))
    for it in data["items"]:
        assert floor_of(it["skill"]) in FLOORS
        assert it["id"].startswith(f"dstt_t{floor_of(it['skill'])}_")
        assert it["reviewed"] is False
    for g in data["generators"]:
        assert floor_of(g["skill"]) in FLOORS and g["id"].startswith(f"dstt_g{floor_of(g['skill'])}_")
    main = json.loads((ROOT / "server" / "data" / "math" / "items" / f"{SUBJECT}.json").read_text("utf-8"))
    assert not set(ids) & {i["id"] for i in main["items"] + main["generators"]}


def test_the_bank_has_no_problems_in_these_floors():
    """Lines about tribulation items stay until the Thiên kiếp type is playable (agent TRIB)."""
    mine = {i["id"] for i in raw_items()} | {g.id for g in my_generators()}
    problems = [e for e in mi.validate_all() if any(f"{iid}:" in e or f"{iid} " in e for iid in mine)
                or any(f"floor {f}:" in e and SUBJECT in e for f in FLOORS)]
    if "tribulation" not in mi.PLAYABLE_TYPES:
        problems = [e for e in problems if not any(f"{i['id']}:" in e for i in raw_items()
                                                   if i["type"] == "tribulation")]
    assert not problems


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    items = [i for i in raw_items() if floor_of(i["skill"]) == floor]
    gens = [g for g in my_generators() if g.floor == floor]
    assert len(items) + len(gens) >= max(want["templates_per_floor"], 34)
    assert len(gens) >= max(want["generators_per_floor"], 3)
    lo, hi = mp.floor_tiers(floor)
    assert all(lo <= t["tier"] <= hi for t in items) and all(lo <= g.tier <= hi for g in gens)
    for skill in subject().floor(floor).skills:
        for tier in mp.allowed_tiers(floor):
            n = sum(1 for i in items if i["skill"] == skill.id and i["tier"] == tier) + \
                sum(1 for g in gens if g.skill == skill.id and g.tier == tier)
            assert n >= want["per_skill_tier"], (skill.id, tier, n)


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_has_every_basic_type(floor):
    present = {i["type"] for i in raw_items() if floor_of(i["skill"]) == floor}
    assert set(BASIC) <= present, set(BASIC) - present
    assert all(i["tier"] >= 2 for i in raw_items() if i["type"] == "find_mistake")


@pytest.mark.parametrize("floor", (5, 6))
def test_floors_five_and_six_have_two_tribulations_at_tier_four(floor):
    tribs = [i for i in raw_items() if floor_of(i["skill"]) == floor and i["type"] == "tribulation"]
    assert len(tribs) >= 2
    assert all(t["tier"] == 4 for t in tribs)


def test_tribulation_items_follow_the_contract_format():
    for it in raw_items():
        if it["type"] != "tribulation":
            assert "parts" not in it
            continue
        assert 2 <= len(it["parts"]) <= 4 and it["solution_vi"] and it["prompt_vi"], it["id"]
        assert "answer" not in it
        for part in it["parts"]:
            assert part["type"] in PART_TYPES and not mp.text_problem(part["prompt_vi"]), it["id"]
            if part["type"] == "true_false":
                assert isinstance(part["answer"], bool)
            elif part["type"] == "multiple_choice":
                assert 0 <= part["answer"] < len(part["options_vi"]) and len(part["options_vi"]) >= 2
            else:
                assert mi.parse_numbers(part["answer"]) is not None
            assert set(part) <= {"type", "prompt_vi", "answer", "options_vi", "unordered", "tolerance"}


def test_no_tier_five_item_so_no_ladder_is_needed():
    assert all(i["tier"] <= 4 and "ladder" not in i for i in raw_items())


def test_find_mistake_items_point_at_a_line():
    for it in raw_items():
        if it["type"] == "find_mistake":
            assert 3 <= len(it["lines_vi"]) <= 6
            assert 0 <= it["answer"] < len(it["lines_vi"])


# ------------------------------------------------------------------ the generators
def test_every_floor_has_its_generators_registered_and_listed():
    listed = {g.id for g in my_generators()}
    registered = {gid for gid in math_gen.REGISTRY if gid.startswith(("dstt_g4_", "dstt_g5_", "dstt_g6_"))}
    assert listed == registered
    assert {g.floor for g in my_generators()} == set(FLOORS)


@pytest.mark.parametrize("gid", sorted(g.id for g in my_generators()))
def test_every_draw_is_valid_repeatable_varied_and_recomputed(gid, expected):
    spec = mi.generators()[gid]
    assert spec.qtype in ("true_false", "numeric")
    prints = set()
    for seed in range(DRAWS):
        item = mi.draw(spec, random.Random(seed))
        assert not mi.draw_problems(spec, item)
        assert mi.draw(spec, random.Random(seed)) == item
        want = expected[gid](json.loads(item.numbers))
        if item.qtype == "true_false":
            assert bool(want) == item.answer, item.numbers
        else:
            got = mi.parse_numbers(item.answer)
            assert (sorted(got) == sorted(want)) if item.unordered else (got == list(want)), item.numbers
        prints.add(item.fingerprint)
    assert len(prints) >= mp.cfg()["bank_targets"]["generator_variety"]


@pytest.mark.parametrize("gid", sorted(g.id for g in my_generators() if g.qtype == "true_false"))
def test_true_false_generators_say_both_true_and_false(gid):
    answers = {mi.draw(mi.generators()[gid], random.Random(seed)).answer for seed in range(60)}
    assert answers == {True, False}


# ------------------------------------------------------------------ the library
@pytest.mark.parametrize("floor", FLOORS)
def test_the_library_explains_every_micro_skill_of_the_floor(floor):
    docs = ml.for_floor(SUBJECT, floor)
    assert len(docs) == 1
    doc = docs[0]
    want = [s.id for s in subject().floor(floor).skills]
    assert list(doc.skills) == want
    sections = [b.get("skill") for b in doc.blocks if b["type"] == "section"]
    assert sections == want
    notes = [b for b in doc.blocks if b["type"] == "note" and b["text"].startswith("Lỗi thường gặp")]
    assert len(notes) >= len(want)
    assert sum(1 for b in doc.blocks if b["type"] in ("formula", "figure", "matrices")) >= len(want)   # something to look at per micro-skill
    assert any(b["type"] in ("matrices", "figure") for b in doc.blocks)
    for skill in want:
        assert ml.for_skill(skill) is doc


def test_the_library_of_these_floors_has_no_problems_and_its_pictures_are_built():
    names = [d for f in FLOORS for d in ml.for_floor(SUBJECT, f)]
    assert len(names) == 3
    files = {f"t{d.floor}_" for d in names}
    assert not [e for e in ml.validate_all() if SUBJECT in e and any(f in e for f in files)]
    manifest = ml.load_manifest()
    for doc in names:
        for block in doc.formulas:
            assert manifest.get(block["key"], {}).get("tex") == block["tex"], block["tex"]
            assert (ROOT / "client" / "assets" / "formulas" / f"{block['key']}.png").is_file()


# ------------------------------------------------------------------ playing it
def answer_for(q: dict, key: dict, correct: bool) -> dict:
    """right_answer / wrong_answer of test_math_loop, plus Thiên kiếp in case one comes up
    before those helpers know it (the contract's shape: one answer per part)."""
    if q["qtype"] != "tribulation":
        return right_answer(q, key) if correct else wrong_answer(q, key)
    parts = []
    for part_q, part_key in zip(q["prompt"]["parts"], key["parts"]):
        one = {"qtype": {"truefalse": "true_false", "choice": "multiple_choice"}.get(part_q["input"], "numeric"),
               "options": part_q.get("options")}
        parts.append(right_answer(one, part_key))
    if not correct:
        parts[0] = wrong_answer({"qtype": {"truefalse": "true_false", "choice": "multiple_choice"}.get(
            q["prompt"]["parts"][0]["input"], "numeric"), "options": q["prompt"]["parts"][0].get("options")},
            key["parts"][0])
    return {"parts": parts}


async def test_a_player_past_floor_three_plays_floor_four(client):
    h, uid = await make(client, "dstt_tang_bon")
    await clear_below(uid, 4, subject=SUBJECT)
    run_id = await start(client, h, floor=4, subject=SUBJECT)
    floor_skills = {s.id for s in subject().floor(4).skills}
    results = []
    for n in range(9):
        q = await ask(client, h, run_id)
        assert q["math"]["subject"] == SUBJECT and q["math"]["floor"] in (1, 2, 3, 4)
        if q["math"]["floor"] == 4 and not q["math"]["review"]:
            assert q["math"]["skill"] in floor_skills
            assert q["math"]["tier"] in (2, 3)
        key = await answer_key(q["session_id"])
        correct = n % 3 != 2
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"],
                                                    "answer": answer_for(q, key, correct)}, headers=h)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["correct"] is correct, (q["qtype"], q["prompt"], body)
        if not correct:
            assert body["reveal"]["solution_vi"]
        results.append((q["math"]["floor"], body["correct"]))
    assert sum(1 for _, ok in results if ok) >= 6 and sum(1 for _, ok in results if not ok) >= 3
    assert sum(1 for f, _ in results if f == 4) >= 5
