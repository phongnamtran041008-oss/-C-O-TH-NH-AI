"""M11 round 2: Giải Tích floors 7-9 (tích phân; ứng dụng và tích phân suy rộng; hàm nhiều biến
với gradient và lan truyền ngược) - the question bank meets the targets and the contract (every
basic type on every floor, two Thiên kiếp per floor, a valid ladder on every tier-5 item),
every generator draw is valid and recomputed with sympy, the library explains every
micro-skill, and a player who has cleared floors 1-6 plays floor 7, and floor 9 where a missed
tier-5 question is followed by its ladder, through the API."""
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
from tests.test_math_loop import ask, clear_below, item_of, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "giai_tich"
FLOORS = (7, 8, 9)
PART_FILE = ROOT / "server" / "data" / "math" / "items" / f"{SUBJECT}.t7_9.json"
BASIC = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_TYPES = ("true_false", "multiple_choice", "numeric")
DRAWS = 200


def subject():
    return mp.subject(SUBJECT)


def raw_items() -> list[dict]:
    """The hand-written items of floors 7-9 as written (a tribulation keeps its parts here)."""
    return json.loads(PART_FILE.read_text("utf-8"))["items"]


def floor_of(skill: str) -> int:
    return subject().skills[skill].floor


def my_generators() -> list[mi.GeneratorSpec]:
    return [g for g in mi.generators().values() if g.subject == SUBJECT and g.floor in FLOORS]


def whole_subject() -> tuple[list[dict], list[dict]]:
    raw = mi.read_items(SUBJECT)
    return raw["items"], raw["generators"]


@pytest.fixture(scope="module")
def expected():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify_gt_t7 as module
        import math_verify_rasoat
        # the curriculum review's generators (tools/math_verify_rasoat.py) sit on these floors too
        mine = {k: v for k, v in math_verify_rasoat.EXPECTED.items() if k.startswith(('gt_g7_', 'gt_g8_', 'gt_g9_'))}
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
            assert skill.id.startswith(f"gt_t{floor}_")
            assert all(s.skills[r].floor <= floor for r in skill.requires), skill.id
    assert not [e for e in mp.validate_all() if any(f"gt_t{f}" in e for f in FLOORS)]


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_seven_to_nine_with_unique_ids():
    data = json.loads(PART_FILE.read_text("utf-8"))
    assert data["subject"] == SUBJECT
    ids = [i["id"] for i in data["items"]] + [g["id"] for g in data["generators"]]
    assert len(ids) == len(set(ids))
    for it in data["items"]:
        assert floor_of(it["skill"]) in FLOORS
        assert it["id"].startswith(f"gt_t{floor_of(it['skill'])}_")
        assert it["reviewed"] is False
    for g in data["generators"]:
        assert floor_of(g["skill"]) in FLOORS and g["id"].startswith(f"gt_g{floor_of(g['skill'])}_")
        assert g["reviewed"] is False
    items, gens = whole_subject()
    assert len([t for t in items + gens if t["id"] in set(ids)]) == len(ids)     # no clash in the subject


def test_the_bank_has_no_problems_in_these_floors():
    assert not [e for e in mi.validate_all() if "giai_tich" in e or "gt_" in e]


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    gens = [t for t in templates if t.generated]
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert len(gens) >= max(want["generators_per_floor"], 3)
    lo, hi = mp.floor_tiers(floor)
    assert all(lo <= t.tier <= hi for t in templates)
    for skill in subject().floor(floor).skills:
        for tier in mp.allowed_tiers(floor):
            n = sum(1 for t in templates if t.skill == skill.id and t.tier == tier)
            assert n >= want["per_skill_tier"], (skill.id, tier, n)


@pytest.mark.parametrize("floor", FLOORS)
def test_each_floor_has_every_basic_type_and_two_tribulations(floor):
    mine = [i for i in raw_items() if floor_of(i["skill"]) == floor]
    present = {i["type"] for i in mine}
    assert set(BASIC) <= present, set(BASIC) - present
    assert sum(1 for i in mine if i["type"] == "tribulation") >= 2


def test_floor_nine_is_all_tier_five_and_floors_seven_and_eight_have_both_tiers():
    assert {i["tier"] for i in raw_items() if floor_of(i["skill"]) == 9} == {5}
    assert {g.tier for g in my_generators() if g.floor == 9} == {5}
    for floor in (7, 8):
        assert {i["tier"] for i in raw_items() if floor_of(i["skill"]) == floor} == {4, 5}


def test_tribulation_items_follow_the_contract_format():
    for it in raw_items():
        if it["type"] != "tribulation":
            assert "parts" not in it
            continue
        assert it["tier"] in (4, 5)
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


def test_every_thien_kiep_is_graded_right_only_when_every_part_is_right():
    tribulations = [i for i in mi.bank().values()
                    if i.subject == SUBJECT and i.floor in FLOORS and i.qtype == "tribulation"]
    assert len(tribulations) >= 6
    for item in tribulations:
        q = mi.to_question(item, random.Random(5))
        rights = []
        for k, part in zip(q.answer_key["parts"], item.parts):
            if part.qtype == "true_false":
                rights.append({"value": k["value"]})
            elif part.qtype == "multiple_choice":
                rights.append({"option": k["option"]})
            else:
                rights.append({"text": ", ".join(k["numbers"])})
        assert mi.grade("tribulation", q.answer_key, {"parts": rights}), item.id
        for n in range(len(rights)):
            broken = list(rights)
            broken[n] = ({"value": not rights[n]["value"]} if "value" in rights[n] else
                         {"option": "z"} if "option" in rights[n] else {"text": "987654"})
            assert not mi.grade("tribulation", q.answer_key, {"parts": broken}), (item.id, n)


def test_every_tier_five_item_has_a_valid_ladder_and_no_other_item_has_one():
    items, gens = whole_subject()
    where = {t["id"]: (floor_of(t["skill"]), t["tier"]) for t in items + gens}
    tier5 = [i for i in raw_items() if i["tier"] == 5]
    assert len(tier5) >= 50
    for it in raw_items():
        if it["tier"] != 5:
            assert "ladder" not in it, it["id"]
            continue
        ladder = it["ladder"]
        assert 2 <= len(ladder) <= 4 and len(set(ladder)) == len(ladder), it["id"]
        own = floor_of(it["skill"])
        tiers = []
        for rung in ladder:
            floor, tier = where[rung]
            assert tier in (3, 4) and floor <= own, (it["id"], rung)
            tiers.append(tier)
        assert 4 in tiers, it["id"]
    assert not mi.ladder_problems(subject(), items, gens)


def test_floor_nine_ladders_lead_back_down_to_lower_floors():
    """Floor 9 has no tier-4 question of its own: its ladders step down to floors 3-8."""
    items, gens = whole_subject()
    where = {t["id"]: floor_of(t["skill"]) for t in items + gens}
    for it in raw_items():
        if floor_of(it["skill"]) == 9:
            assert all(3 <= where[r] < 9 for r in it["ladder"]), it["id"]


def test_find_mistake_items_point_at_a_line():
    for it in raw_items():
        if it["type"] == "find_mistake":
            assert 3 <= len(it["lines_vi"]) <= 6
            assert 0 <= it["answer"] < len(it["lines_vi"])


# ------------------------------------------------------------------ the generators
def test_every_floor_has_its_generators_registered_listed_and_recomputed(expected):
    listed = {g.id for g in my_generators()}
    registered = {gid for gid in math_gen.REGISTRY if gid.startswith(("gt_g7_", "gt_g8_", "gt_g9_"))}
    assert listed == registered == set(expected)
    for floor in FLOORS:
        assert sum(1 for g in my_generators() if g.floor == floor) >= 3


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
    for skill in want:
        assert ml.for_skill(skill) is doc


def test_the_library_of_these_floors_has_no_problems_and_its_pictures_are_built():
    docs = [d for f in FLOORS for d in ml.for_floor(SUBJECT, f)]
    assert len(docs) == 3
    files = {f"t{d.floor}_" for d in docs}
    assert not [e for e in ml.validate_all() if SUBJECT in e and any(f in e for f in files)]
    manifest = ml.load_manifest()
    for doc in docs:
        for block in doc.formulas:
            assert manifest.get(block["key"], {}).get("tex") == block["tex"], block["tex"]
            assert (ROOT / "client" / "assets" / "formulas" / f"{block['key']}.png").is_file()


# ------------------------------------------------------------------ playing it
async def answer(client, h, q: dict, correct: bool) -> dict:
    key = await answer_key(q["session_id"])
    given = right_answer(q, key) if correct else wrong_answer(q, key)
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": given}, headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["correct"] is correct, (q["qtype"], q["prompt"], body)
    if not correct:
        assert body["reveal"]["solution_vi"]
    return body


async def test_a_player_past_floor_six_plays_floor_seven(client):
    h, uid = await make(client, "gt_tich_phan")
    await clear_below(uid, 7, subject=SUBJECT)
    run_id = await start(client, h, floor=7, subject=SUBJECT)
    floor_skills = {s.id for s in subject().floor(7).skills}
    results = []
    for n in range(9):
        q = await ask(client, h, run_id)
        info = q["math"]
        assert info["subject"] == SUBJECT and 1 <= info["floor"] <= 7
        if info.get("ladder"):                          # rule 8: a rung is tier 3-4, floor 7 or below
            assert info["tier"] in (3, 4)
        elif info["review"]:                            # rule 6b may bring back a floor below
            assert info["floor"] < 7
        else:
            assert info["floor"] == 7 and info["skill"] in floor_skills
            assert info["tier"] in (4, 5)
        correct = n % 3 != 2
        await answer(client, h, q, correct)
        results.append((info["floor"], correct))
    assert sum(1 for _, ok in results if ok) >= 6 and sum(1 for _, ok in results if not ok) >= 3
    assert sum(1 for f, _ in results if f == 7) >= 5


async def test_on_floor_nine_a_missed_question_is_followed_by_its_ladder(client):
    h, uid = await make(client, "gt_nhieu_bien")
    await clear_below(uid, 9, subject=SUBJECT)
    # Đạo Thụ: floor 9's first node (gt_nhieu_bien) also requires Đại Số's ds_vecto_ma_tran (its floor 3)
    await clear_below(uid, 4, subject="dai_so_tuyen_tinh")
    run_id = await start(client, h, floor=9, subject=SUBJECT)
    bank = mi.bank()
    for _ in range(14):                                 # answer right until a hand-written tier-5 item
        q = await ask(client, h, run_id)
        # (a review question may come from the Đại Số node it reinforces)
        assert q["math"]["subject"] == SUBJECT or (q["math"]["review"] and q["math"]["subject"] == "dai_so_tuyen_tinh")
        if q["math"]["floor"] == 9 and not q["math"]["review"]:
            assert q["math"]["tier"] == 5
            iid = await item_of(q)
            if iid in bank:
                break
        await answer(client, h, q, True)
    else:
        pytest.fail("no hand-written floor-9 question came up")
    body = await answer(client, h, q, False)
    rungs = list(bank[iid].ladder)
    assert body["math"]["ladder"]["started"] and body["math"]["ladder"]["steps"] == len(rungs)
    asked = []
    for n in range(len(rungs)):
        r = await ask(client, h, run_id)
        assert r["math"]["ladder"] == {"of": iid, "step": n + 1, "steps": len(rungs)}
        assert r["math"]["floor"] < 9 and r["math"]["tier"] in (3, 4)
        asked.append(await item_of(r))
        await answer(client, h, r, True)
    assert asked == rungs                               # exactly its rungs, in order
