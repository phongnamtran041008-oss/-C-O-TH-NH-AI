"""M11 round 2: Xác Suất và Thống Kê floors 7-9 - population and sample, point estimation and
maximum likelihood, confidence intervals, the law of large numbers and the central limit
theorem, hypothesis tests. The bank of each floor (targets, all six basic types, Thiên kiếp, a
valid ladder on every tier-5 item), the generators (valid, varied, recomputed with sympy), Tàng
Thư Các for the three floors, and a learner who has cleared floors 1-6 playing floor 7 through
the API."""
import dataclasses
import datetime as dt
import json
import random
import sys
from math import gcd
from pathlib import Path

import pytest

from app import db as dbm
from app.learning import math_gen
from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from app.models import MathRun
from tests.helpers import answer_key
from tests.test_math_loop import ask, clear_below, make, right_answer, start, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
SUBJECT = "xac_suat_thong_ke"
FLOORS = (7, 8, 9)
BASIC_TYPES = ("true_false", "multiple_choice", "numeric", "matching", "ordering", "find_mistake")
PART_FILE = "xac_suat_thong_ke.t7_9.json"
OWN_PREFIXES = ("xs_t7_", "xs_t8_", "xs_t9_", "xs_g7_", "xs_g8_", "xs_g9_")


def subject() -> mp.Subject:
    return mp.subject(SUBJECT)


def raw_part() -> dict:
    return json.loads((mi.items_path(SUBJECT).parent / PART_FILE).read_text("utf-8"))


def own_generators(floor: int) -> dict[str, mi.GeneratorSpec]:
    return {gid: g for gid, g in mi.generators().items() if g.subject == SUBJECT and g.floor == floor}


def own_items(floor: int) -> list[mi.MathItem]:
    return mi.floor_items(SUBJECT, floor, allow_unreviewed=True)


@pytest.fixture(scope="module")
def math_verify():
    pytest.importorskip("sympy", reason="pip install -r server/requirements-dev.txt")
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import math_verify as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


# ------------------------------------------------------------------ the bank
def test_the_part_file_holds_only_floors_seven_to_nine_and_is_valid():
    raw = raw_part()
    assert raw["subject"] == SUBJECT
    floors = {subject().skills[it["skill"]].floor for it in raw["items"] + raw["generators"]}
    assert floors == set(FLOORS)
    assert all(it["id"].startswith(f"xs_t{subject().skills[it['skill']].floor}_") for it in raw["items"])
    assert all(it["id"].startswith(f"xs_g{subject().skills[it['skill']].floor}_") for it in raw["generators"])
    assert all(not it["reviewed"] for it in raw["items"] + raw["generators"])
    assert not [e for e in mi.validate_all() if any(p in e for p in OWN_PREFIXES) or PART_FILE in e]


@pytest.mark.parametrize("floor", FLOORS)
def test_a_written_floor_meets_the_bank_targets(floor):
    want = mp.cfg()["bank_targets"]
    templates = mi.floor_templates(SUBJECT, floor, allow_unreviewed=True)
    assert len(templates) >= max(want["templates_per_floor"], 34)
    assert sum(1 for t in templates if t.generated) >= max(want["generators_per_floor"], 3)
    f = subject().floor(floor)
    assert list(f.tiers) == ([5] if floor == 9 else [4, 5])
    for skill in f.skills:
        for tier in f.tiers:
            own = [t for t in templates if t.skill == skill.id and t.tier == tier]
            assert len(own) >= want["per_skill_tier"], (skill.id, tier)
    assert all(t.tier in f.tiers for t in templates)


@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_mixes_all_six_basic_types_and_has_tribulations(floor):
    items = own_items(floor)
    assert {i.qtype for i in items} >= set(BASIC_TYPES)
    tribs = [i for i in items if i.qtype == "tribulation"]
    assert len(tribs) >= 2
    for it in tribs:
        assert it.tier in (4, 5) and 2 <= len(it.parts) <= 4
        assert len(it.solution_vi) >= len(it.parts)


@pytest.mark.parametrize("floor", FLOORS)
def test_a_tribulation_is_right_only_with_every_part_right(floor):
    for it in [i for i in own_items(floor) if i.qtype == "tribulation"]:
        q = mi.to_question(it, random.Random(1))
        shown = q.public()
        assert shown["input"] == "tribulation" and len(shown["prompt"]["parts"]) == len(it.parts)
        assert mi.grade("tribulation", q.answer_key, right_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, wrong_answer(shown, q.answer_key)), it.id
        assert not mi.grade("tribulation", q.answer_key, {"parts": []}), it.id


def _where() -> dict[str, tuple[int, int]]:
    """id -> (floor, tier) of every hand-written item and generator of the subject."""
    out = {i.id: (i.floor, i.tier) for i in mi.bank().values() if i.subject == SUBJECT}
    out.update({g.id: (g.floor, g.tier) for g in mi.generators().values() if g.subject == SUBJECT})
    return out


@pytest.mark.parametrize("floor", FLOORS)
def test_every_tier_five_item_has_a_valid_ladder(floor):
    where = _where()
    tier5 = [i for i in own_items(floor) if i.tier == 5]
    assert tier5 and (floor != 9 or len(tier5) == len(own_items(floor)))
    for it in tier5:
        assert 2 <= len(it.ladder) <= 4, it.id
        assert len(set(it.ladder)) == len(it.ladder) and it.id not in it.ladder
        rungs = [where[r] for r in it.ladder]              # (KeyError: a rung that does not exist)
        assert all(t in (3, 4) and f <= it.floor for f, t in rungs), (it.id, rungs)
        assert any(t == 4 for _, t in rungs), it.id
    assert not [i.id for i in own_items(floor) if i.tier != 5 and i.ladder]


def test_numeric_answers_are_exact_and_decimals_come_from_the_given_tables():
    answers = []
    for it in raw_part()["items"]:
        if it["type"] == "numeric":
            answers.append((it["id"], it["answer"], it["prompt_vi"]))
        for part in it.get("parts", []):
            if part["type"] == "numeric":
                answers.append((it["id"], part["answer"], it["prompt_vi"] + " " + part["prompt_vi"]))
    for iid, answer, prompt in answers:
        for value in answer.split(","):
            num, _, den = value.strip().partition("/")
            if den:
                assert gcd(int(num), int(den)) == 1 and int(den) > 1, iid
    assert not any("tolerance" in it for it in raw_part()["items"])
    assert not any("tolerance" in p for it in raw_part()["items"] for p in it.get("parts", []))


def test_the_find_mistake_items_target_the_classic_errors():
    fm = [i for f in FLOORS for i in own_items(f) if i.qtype == "find_mistake"]
    assert len(fm) >= 15
    text = " ".join(" ".join(i.lines_vi) for i in fm)
    for idea in ("s^2 = 14/4",                    # dividing by n where n - 1 is meant
                 "(492 - 500)/16",                # sigma used where sigma/sqrt(n) is meant
                 "t(15; 0.05)",                   # a one-sided critical value in a two-sided interval
                 "miền bác bỏ là z > 1.645",      # ... and in a two-sided test
                 "đã chứng minh được",            # accepting H0 taken as proof that it is true
                 "3 + 4 = 7",                     # adding standard deviations
                 "64 . 0.8 = 51.2",               # the sd of a sum taken as n sigma
                 "(0.5 + 0.35)/2",                # the pooled proportion as a plain average
                 "epsilon <= 4",                  # the length of an interval taken for epsilon
                 "n nhỏ nhất là 61"):             # a sample size rounded down
        assert idea in text, idea
    tf = " ".join(i.prompt_vi for f in FLOORS for i in own_items(f) if i.qtype == "true_false")
    assert "xác suất để giả thuyết H0 đúng" in tf             # the p-value read as P(H0)
    assert "95% số liệu" in tf                                # a 95% interval read as 95% of the data


# ------------------------------------------------------------------ generators
@pytest.mark.parametrize("floor", FLOORS)
def test_every_floor_has_its_own_generators(floor):
    gens = own_generators(floor)
    assert len(gens) >= 3
    assert all(gid in math_gen.REGISTRY and gid.startswith(f"xs_g{floor}_") for gid in gens)
    assert {g.qtype for g in gens.values()} <= {"true_false", "numeric"}
    assert all(g.tier == 5 for g in gens.values()) if floor == 9 else True


@pytest.mark.parametrize("gid", sorted(g for g in mi.generators() if g[:5] in ("xs_g7", "xs_g8", "xs_g9")))
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


@pytest.mark.parametrize("gid", ["xs_g7_phuong_sai_mau", "xs_g7_hop_ly", "xs_g8_khoang_biet_sigma", "xs_g8_co_mau",
                                 "xs_g9_t_trung_binh", "xs_g9_hai_trung_binh"])
def test_the_recomputation_catches_a_wrong_answer(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(7))
    numbers = mi.parse_numbers(item.answer)
    numbers[-1] += mi.parse_numbers("1/100")[0]
    assert math_verify.mismatch(dataclasses.replace(item, answer=", ".join(mi.number_text(v) for v in numbers)))


@pytest.mark.parametrize("gid", ["xs_g7_khong_chech_tf", "xs_g9_quyet_dinh"])
def test_the_recomputation_catches_a_wrong_verdict(gid, math_verify):
    item = mi.draw(mi.generators()[gid], random.Random(3))
    assert math_verify.mismatch(dataclasses.replace(item, answer=not item.answer))


def test_a_sample_size_is_always_rounded_up():
    """The smallest n: never the rounded value of (z sigma/epsilon)^2 when that is not whole."""
    from fractions import Fraction
    for seed in range(200):
        d = math_gen.REGISTRY["xs_g8_co_mau"](random.Random(seed))
        p = d.params
        z, eps = Fraction(p["z"]), Fraction(p["eps"])
        bound = (z * Fraction(p["sigma"]) / eps) ** 2 if p["kind"] == "trung_binh" else \
            z * z * Fraction(p["f"]) * (1 - Fraction(p["f"])) / eps ** 2
        n = int(d.answer)
        assert n >= bound > n - 1


# ------------------------------------------------------------------ Tàng Thư Các
@pytest.mark.parametrize("floor", FLOORS)
def test_the_library_covers_every_micro_skill_of_the_floor(floor):
    docs = ml.for_floor(SUBJECT, floor)
    assert len(docs) == 1
    doc = docs[0]
    assert list(doc.skills) == [sk.id for sk in subject().floor(floor).skills]
    sections = [b for b in doc.blocks if b["type"] == "section"]
    assert len(sections) == len(doc.skills)
    notes = [b for b in doc.blocks if b["type"] == "note"]
    assert len(notes) >= len(doc.skills) and all(n["text"].startswith("Lỗi thường gặp") for n in notes)
    assert sum(1 for b in doc.blocks if b["type"] in ("formula", "figure", "matrices")) >= len(doc.skills)   # something to look at per micro-skill
    assert any(b["type"] == "steps" for b in doc.blocks)              # worked examples
    for sk in doc.skills:
        assert ml.for_skill(sk) is doc
    assert not [e for e in ml.validate_all() if f"{SUBJECT}/t{floor}_" in e]
    assert not [e for e in ml.manifest_problems() if any(f["tex"] in e for f in doc.formulas)]
    assert not any(r"\bar" in f["tex"] or r"\hat" in f["tex"] or r"\overline" in f["tex"] for f in doc.formulas)


# ------------------------------------------------------------------ a learner plays floor 7
async def test_a_player_who_cleared_floors_one_to_six_practises_floor_seven(client):
    h, uid = await make(client, "xs_t7_hoc_tro")
    await clear_below(uid, 7, subject=SUBJECT)
    # Đạo Thụ: floor 7's node (xs_mau_uoc_luong) also requires Giải Tích's gt_cuc_tri, on its floor 6
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id="giai_tich", floor=6, mode="trial", tier=5, asked=1, correct=1,
                       passed=True, started_at=dt.datetime(2026, 1, 1), ended_at=dt.datetime(2026, 1, 1)))
        await db.commit()
    run_id = await start(client, h, floor=7, subject=SUBJECT)
    rights, on_floor_seven, kinds = 0, 0, set()
    for n in range(12):
        q = await ask(client, h, run_id)
        # (spiral review and the ladder of a missed tier-5 question may go below; review also comes
        # from the Giải Tích node it reinforces)
        assert 1 <= q["math"]["floor"] <= 7
        assert q["math"]["subject"] == SUBJECT or (q["math"]["review"] and q["math"]["subject"] == "giai_tich")
        on_floor_seven += q["math"]["floor"] == 7
        if q["math"]["floor"] == 7:
            assert q["math"]["skill"].startswith("xs_t7_") and q["math"]["tier"] in (4, 5)
            kinds.add(q["qtype"])
        key = await answer_key(q["session_id"])
        correct = n % 3 != 2
        answer = right_answer(q, key) if correct else wrong_answer(q, key)
        r = await client.post("/quiz/answer", json={"session_id": q["session_id"], "answer": answer}, headers=h)
        assert r.status_code == 200, r.text
        res = r.json()
        assert res["correct"] is correct, (q["qtype"], res)
        rights += correct
        if not correct:
            assert res["math"]
    assert rights == 8 and on_floor_seven >= 5
