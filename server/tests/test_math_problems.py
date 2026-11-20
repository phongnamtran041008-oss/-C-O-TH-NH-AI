"""M6: bài tập lập trình - the exercises, the checker, the verdicts and one go from the
statement to Tu Vi.

The learner's program runs on the learner's machine, so these tests play the part of that
machine: they send back what a program would have printed (and what a broken one would
have done) and check the server marks it the way plan 5.2 says.
"""
import sqlite3

import pytest
from sqlalchemy import select

from app import db as dbm
from app.config import settings
from app.learning import math_path as mp
from app.learning import math_problems as pr
from app.models import Character, MathSubmission
from tests.test_math_loop import SUBJECT, clear_below, make

PROBLEM = "dstt_bt_tich_vo_huong"          # floor 3, tier 2
FLOOR1_PROBLEM = "dstt_bt_dem_phan_tu"     # floor 1, tier 1


# ------------------------------------------------------------------ helpers
def right(problem_id: str = PROBLEM) -> list[str]:
    return [t.expected for t in pr.problem(problem_id).tests]


async def open_attempt(client, h, problem_id: str = PROBLEM):
    r = await client.post(f"/math/problem/{problem_id}/tests", json={}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def send(client, h, problem_id: str, outputs, attempt_id=None, status="ok", **kw):
    body = {"outputs": outputs, "status": status, **kw}
    if attempt_id is not None:
        body["attempt_id"] = attempt_id
    r = await client.post(f"/math/problem/{problem_id}/judge", json=body, headers=h)
    return r


async def submit(client, h, outputs, problem_id: str = PROBLEM, status="ok", **kw):
    attempt = await open_attempt(client, h, problem_id)
    r = await send(client, h, problem_id, outputs, attempt["attempt_id"], status, **kw)
    assert r.status_code == 200, r.text
    return r.json()


async def rows_of(uid) -> list[MathSubmission]:
    async with dbm.SessionLocal() as db:
        return list((await db.execute(select(MathSubmission).where(MathSubmission.user_id == uid)
                                      .order_by(MathSubmission.id))).scalars())


async def tu_vi(uid) -> int:
    async with dbm.SessionLocal() as db:
        return (await db.get(Character, uid)).cultivation_xp


# ------------------------------------------------------------------ the exercises as data
def test_every_exercise_belongs_to_a_micro_skill_and_a_tier_of_its_floor():
    assert pr.validate_all() == []
    assert pr.bank(), "no programming exercise is written"
    for p in pr.bank().values():
        subject = mp.subject(p.subject)
        assert p.skill in subject.skills and subject.skills[p.skill].floor == p.floor
        assert mp.tier_allowed(p.floor, p.tier)
        assert mp.time_limit("programming", p.tier) is not None


def test_an_exercise_has_samples_hidden_tests_and_a_reference_solution():
    least = mp.cfg()["programming"]["min_tests"]
    for p in pr.bank().values():
        assert p.samples and len(p.tests) >= least
        assert pr.solution_path(p.subject, p.id).is_file()
        for t in (*p.samples, *p.tests):
            assert t.data.endswith("\n") and t.expected.endswith("\n")


PUBLIC_KEYS = {"id", "subject", "subject_name_vi", "skill", "skill_name_vi", "floor", "tier",
               "tier_name_vi", "title_vi", "statement_vi", "input_vi", "output_vi", "limits_vi",
               "checker", "time_limit_ms", "samples", "tests", "think_limit_s", "reviewed", "starter"}
SCORED_KEYS = {"scored", "grades", "higher_better", "grade_names_vi"}     # Xạ Trường only


def test_the_statement_the_game_gets_never_carries_a_hidden_test():
    """The view is the whole contract: these keys and no others, and `tests` is a count."""
    for p in pr.bank().values():
        view = p.view()
        assert set(view) == PUBLIC_KEYS | (SCORED_KEYS if p.scored else set()), p.id
        assert view["tests"] == len(p.tests) and isinstance(view["tests"], int)
        assert view["samples"] == [s.view() for s in p.samples]
        # The view is a fixed set of fields, so nothing hidden can ride along in a new one.
        # Short answers like "4" are bound to appear inside some sample by chance, so what is
        # checked here is the shape; the API test below looks for whole hidden inputs.
        assert all(t.data not in repr(view["samples"]) or t in p.samples for t in p.tests)


def test_floor_problems_hides_what_is_not_reviewed_yet():
    p = pr.problem(PROBLEM)
    assert p in pr.floor_problems(SUBJECT, p.floor, True)
    assert pr.floor_problems(SUBJECT, p.floor, False) == [x for x in pr.bank().values()
                                                          if x.floor == p.floor and x.reviewed]


# ------------------------------------------------------------------ the checker
def test_whitespace_never_decides_right_or_wrong():
    assert pr.same_output("1 2 3\n", "1 2 3\n")
    assert pr.same_output("1 2 3\n", " 1\t2  3 \r\n\n")
    assert pr.same_output("1\n2\n", "1 2\n")             # tokens, not lines
    assert not pr.same_output("1 2\n", "1 2 3\n")
    assert not pr.same_output("1 2 3\n", "1 2\n")


def test_the_float_checker_allows_a_small_error_and_the_exact_one_does_not():
    assert pr.same_output("5.000000\n", "4.9999996\n", "float")
    assert pr.same_output("5.000000\n", "5\n", "float")
    assert not pr.same_output("5.000000\n", "5.001\n", "float")
    assert not pr.same_output("5.000000\n", "5\n", "exact")
    assert pr.same_output("2236.067977\n", "2236.0679775\n", "float")   # big numbers: relative


def test_the_float_checker_still_compares_words_word_by_word():
    assert pr.same_output("yes 1.0\n", "yes 1.0000001\n", "float")
    assert not pr.same_output("yes 1.0\n", "no 1.0\n", "float")
    assert not pr.same_output("1.0\n", "nan\n", "float")


# ------------------------------------------------------------------ the verdicts
def test_every_test_right_is_ac_and_one_wrong_is_wa():
    tests = list(pr.problem(PROBLEM).tests)
    good = [t.expected for t in tests]
    assert pr.judge(tests, good).verdict == pr.AC
    assert pr.judge(tests, good).share == 1.0
    bad = pr.judge(tests, ["0\n"] + good[1:])
    assert (bad.verdict, bad.passed, bad.total) == (pr.WA, len(tests) - 1, len(tests))


def test_a_crash_names_the_test_it_crashed_on_and_the_rest_did_not_run():
    tests = list(pr.problem(PROBLEM).tests)
    good = [t.expected for t in tests]
    j = pr.judge(tests, good[:2] + [""], status="re", error="ZeroDivisionError")
    assert (j.verdict, j.passed) == (pr.RE, 2)
    assert [r.verdict for r in j.results] == [pr.AC, pr.AC, pr.RE] + [pr.NOT_RUN] * (len(tests) - 3)
    assert j.error == "ZeroDivisionError"


def test_running_out_of_time_is_tle_on_that_test():
    tests = list(pr.problem(PROBLEM).tests)
    j = pr.judge(tests, [tests[0].expected, ""], status="tle")
    assert (j.verdict, j.passed) == (pr.TLE, 1)
    assert [r.verdict for r in j.results][:2] == [pr.AC, pr.TLE]


def test_code_that_does_not_compile_is_ce_and_no_test_counts():
    tests = list(pr.problem(PROBLEM).tests)
    j = pr.judge(tests, [], status="ce", error="SyntaxError (dòng 2)")
    assert (j.verdict, j.passed, j.share) == (pr.CE, 0, 0.0)
    assert {r.verdict for r in j.results} == {pr.CE} and "SyntaxError" in j.error


def test_a_program_that_answers_fewer_tests_than_it_claims_is_wrong_not_accepted():
    tests = list(pr.problem(PROBLEM).tests)
    j = pr.judge(tests, [t.expected for t in tests[:3]], status="ok")
    assert (j.verdict, j.passed) == (pr.WA, 3)


def test_the_five_verdicts_of_the_plan_all_exist():
    assert set(pr.VERDICTS) == {"AC", "WA", "TLE", "RE", "CE"}


# ------------------------------------------------------------------ the tests must have teeth
def test_the_hidden_tests_of_an_exercise_never_all_want_the_same_answer():
    """Otherwise a program that prints that one answer would be accepted."""
    for p in pr.bank().values():
        answers = {t.expected.strip() for t in p.tests}
        assert len(answers) > 1, f"{p.id}: every hidden test wants {answers}"


def test_a_program_that_prints_nothing_is_never_accepted():
    for p in pr.bank().values():
        j = pr.judge(list(p.tests), [""] * len(p.tests), checker=p.checker)
        assert j.verdict != pr.AC and j.passed == 0, p.id


def test_a_program_that_prints_one_constant_is_never_accepted():
    """Whatever constant it picks - including the answer of its own first sample or test."""
    for p in pr.bank().values():
        for constant in {t.expected for t in p.tests} | {s.expected for s in p.samples}:
            j = pr.judge(list(p.tests), [constant] * len(p.tests), checker=p.checker)
            assert j.verdict != pr.AC, f"{p.id}: printing {constant.strip()!r} every time is accepted"


def test_only_the_right_answers_are_accepted():
    """The other half of the same coin: the real answers do pass."""
    for p in pr.bank().values():
        j = pr.judge(list(p.tests), [t.expected for t in p.tests], checker=p.checker)
        assert j.verdict == pr.AC and j.share == 1.0, p.id


# ------------------------------------------------------------------ through the API
async def test_the_list_only_shows_floors_that_are_open(client):
    h, uid = await make(client)
    r = await client.get(f"/math/problems?subject_id={SUBJECT}", headers=h)
    assert r.status_code == 200, r.text
    floors = r.json()["floors"]
    # Đạo Thụ (R10): an exercise is open when its micro-skill's node is - floor 1's node and floor 2's
    # optional node require nothing; floor 3's node waits for floor 1's, so it is locked for a new player
    assert [f["floor"] for f in floors] == [1, 2]
    assert any(p["id"] == FLOOR1_PROBLEM for p in floors[0]["problems"])
    assert all(p["best"] is None for p in floors[0]["problems"])
    assert PROBLEM not in {p["id"] for f in floors for p in f["problems"]}
    await clear_below(uid, 3)
    floors = (await client.get(f"/math/problems?subject_id={SUBJECT}", headers=h)).json()["floors"]
    assert [f["floor"] for f in floors] == [1, 2, 3]


async def test_the_statement_comes_without_the_hidden_tests(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    r = await client.get(f"/math/problem/{PROBLEM}", headers=h)
    assert r.status_code == 200, r.text
    p = r.json()["problem"]
    assert p["title_vi"] and p["statement_vi"] and p["samples"]
    assert p["tests"] == len(pr.problem(PROBLEM).tests)
    body = r.text
    hidden = [t for t in pr.problem(PROBLEM).tests if len(t.data) >= 12]
    assert hidden, "this test needs a hidden input long enough to recognise"
    for t in hidden:
        assert t.data.strip() not in body                # not one hidden input went out
        assert t.data.replace("\n", "\\n") not in body   # nor as JSON writes it


async def test_a_locked_floor_keeps_its_exercises_shut(client):
    h, uid = await make(client)
    for path in (f"/math/problem/{PROBLEM}", ):
        r = await client.get(path, headers=h)
        assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked", r.text
    r = await client.post(f"/math/problem/{PROBLEM}/tests", json={}, headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked"


async def test_an_unknown_exercise_is_a_404(client):
    h, uid = await make(client)
    assert (await client.get("/math/problem/khong_co_bai_nay", headers=h)).status_code == 404


async def test_chay_thu_marks_the_samples_and_pays_nothing(client):
    h, uid = await make(client)
    samples = pr.problem(FLOOR1_PROBLEM).samples
    r = await send(client, h, FLOOR1_PROBLEM, [s.expected for s in samples])
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["mode"] == "run" and data["result"]["verdict"] == "AC"
    assert data["result"]["total"] == len(samples) and "xp" not in data
    assert await rows_of(uid) == []                         # a try is not a submission


async def test_chay_thu_on_a_wrong_program_shows_which_sample_failed(client):
    h, uid = await make(client)
    samples = pr.problem(FLOOR1_PROBLEM).samples
    data = (await send(client, h, FLOOR1_PROBLEM, ["999\n"] + [s.expected for s in samples[1:]])).json()
    assert data["result"]["verdict"] == "WA"
    assert [t["verdict"] for t in data["result"]["tests"]][0] == "WA"


async def test_nop_bai_hands_out_the_hidden_input_only(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    attempt = await open_attempt(client, h)
    problem = pr.problem(PROBLEM)
    assert attempt["inputs"] == [t.data for t in problem.tests]
    assert attempt["total"] == len(problem.tests)
    assert attempt["time_limit_ms"] == problem.time_limit_ms
    assert "out" not in str(attempt)
    rows = await rows_of(uid)
    assert len(rows) == 1 and rows[0].judged_at is None and rows[0].verdict is None


async def test_asking_twice_without_handing_in_reuses_the_same_attempt(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    first, second = await open_attempt(client, h), await open_attempt(client, h)
    assert first["attempt_id"] == second["attempt_id"]
    assert len(await rows_of(uid)) == 1


async def test_a_right_solution_is_accepted_and_pays_tu_vi_by_tier(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    before = await tu_vi(uid)
    data = await submit(client, h, right(), times_ms=[12, 9, 14, 11, 10])
    assert data["mode"] == "submit"
    assert data["result"]["verdict"] == "AC" and data["result"]["share"] == 1.0
    assert data["xp_gained"] == mp.xp_for_tier(pr.problem(PROBLEM).tier)
    after = await tu_vi(uid)
    assert after - before == data["xp_gained"]
    row = (await rows_of(uid))[0]
    assert (row.verdict, row.passed, row.total) == ("AC", 5, 5) and row.judged_at is not None
    assert row.ms == 14 and row.code == ""


async def test_the_reward_follows_the_share_of_tests_passed(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    good = right()
    data = await submit(client, h, ["0\n"] + good[1:])      # 4 of 5
    full = mp.xp_for_tier(pr.problem(PROBLEM).tier)
    assert data["result"]["verdict"] == "WA" and data["result"]["passed"] == 4
    assert data["xp_gained"] == round(full * 0.8)


async def test_only_the_progress_beyond_the_best_so_far_pays_again(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    good = right()
    full = mp.xp_for_tier(pr.problem(PROBLEM).tier)
    first = await submit(client, h, ["0\n"] + good[1:])     # 4/5
    second = await submit(client, h, good)                  # 5/5: only the last fifth pays
    third = await submit(client, h, good)                   # the same again: nothing
    assert first["xp_gained"] + second["xp_gained"] == full
    assert third["xp_gained"] == 0
    assert second["best"]["verdict"] == "AC"
    assert [r.verdict for r in await rows_of(uid)] == ["WA", "AC", "AC"]


async def test_a_worse_solution_after_a_good_one_pays_nothing_and_keeps_the_best(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    await submit(client, h, right())
    data = await submit(client, h, ["0\n"] * 5)
    assert data["result"]["verdict"] == "WA" and data["xp_gained"] == 0
    assert data["best"]["verdict"] == "AC"
    listing = (await client.get(f"/math/problems?subject_id={SUBJECT}&floor=3", headers=h)).json()
    best = next(p["best"] for p in listing["floors"][0]["problems"] if p["id"] == PROBLEM)
    assert best["verdict"] == "AC" and best["passed"] == 5


async def test_a_crash_is_reported_test_by_test_and_pays_for_what_passed(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    good = right()
    data = await submit(client, h, good[:2] + [""], status="re", error="IndexError")
    res = data["result"]
    assert res["verdict"] == "RE" and res["passed"] == 2
    assert [t["verdict"] for t in res["tests"]] == ["AC", "AC", "RE", "-", "-"]
    assert res["error"] == "IndexError"
    assert data["xp_gained"] == round(mp.xp_for_tier(pr.problem(PROBLEM).tier) * 0.4)


async def test_code_that_does_not_compile_is_ce_through_the_api(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    data = await submit(client, h, [], status="ce", error="SyntaxError (dòng 1)", code="def f(:\n")
    assert data["result"]["verdict"] == "CE" and data["xp_gained"] == 0
    row = (await rows_of(uid))[0]
    assert row.verdict == "CE" and row.code == "def f(:\n"      # kept so the player can read it back


async def test_the_same_attempt_cannot_be_handed_in_twice(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    attempt = await open_attempt(client, h)
    assert (await send(client, h, PROBLEM, right(), attempt["attempt_id"])).status_code == 200
    again = await send(client, h, PROBLEM, right(), attempt["attempt_id"])
    assert again.status_code == 409 and again.json()["error"]["code"] == "already_judged"


async def test_nobody_else_can_hand_in_your_attempt(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    attempt = await open_attempt(client, h)
    other, _ = await make(client, "toan_2")
    r = await send(client, h=other, problem_id=PROBLEM, outputs=right(), attempt_id=attempt["attempt_id"])
    assert r.status_code == 404 and r.json()["error"]["code"] == "no_attempt"


async def test_a_flood_of_output_is_refused(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    attempt = await open_attempt(client, h)
    huge = "x" * (mp.cfg()["programming"]["max_output_chars"] + 1)
    r = await send(client, h, PROBLEM, [huge], attempt["attempt_id"])
    assert r.status_code == 400 and r.json()["error"]["code"] == "output_too_long"


async def test_more_answers_than_tests_is_refused(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    attempt = await open_attempt(client, h)
    r = await send(client, h, PROBLEM, right() + ["1\n"], attempt["attempt_id"])
    assert r.status_code == 400 and r.json()["error"]["code"] == "too_many_outputs"


async def test_a_nonsense_run_status_is_refused(client):
    h, uid = await make(client)
    r = await send(client, h, FLOOR1_PROBLEM, ["1\n"], status="lol")
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_status"


async def test_the_float_exercise_accepts_a_slightly_different_number(client):
    h, uid = await make(client)
    await clear_below(uid, 3)
    problem = pr.problem("dstt_bt_do_dai_vecto")
    nudged = [f"{float(t.expected) + 1e-9:.9f}\n" for t in problem.tests]
    data = await submit(client, h, nudged, problem_id=problem.id)
    assert data["result"]["verdict"] == "AC"


async def test_an_exercise_that_is_not_reviewed_is_hidden_when_the_server_forbids_it(client, monkeypatch):
    h, uid = await make(client)
    monkeypatch.setattr(settings, "allow_unreviewed", False)
    r = await client.get(f"/math/problem/{FLOOR1_PROBLEM}", headers=h)
    assert r.status_code == 404
    floors = (await client.get(f"/math/problems?subject_id={SUBJECT}", headers=h)).json()["floors"]
    assert floors == []


async def test_the_floor_list_says_how_many_exercises_can_be_opened(client):
    h, uid = await make(client)
    subject = (await client.get("/math/path", headers=h)).json()["subjects"][0]
    # floor 1's node and floor 2's optional node are open from the start (Đạo Thụ, R10)
    assert subject["problems"] == sum(len(pr.floor_problems(SUBJECT, n, True)) for n in (1, 2))
    await clear_below(uid, 3)
    subject = (await client.get("/math/path", headers=h)).json()["subjects"][0]
    assert subject["problems"] == sum(len(pr.floor_problems(SUBJECT, n, True)) for n in (1, 2, 3))


# ------------------------------------------------------------------ the migration
def test_migration_0013_adds_the_submissions_table(tmp_path):
    from alembic import command

    from tests.test_math_loop import _alembic
    path = tmp_path / "m13.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0012")
    con = sqlite3.connect(path)
    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    assert "math_submissions" not in tables
    con.close()

    command.upgrade(cfg, "0013")
    con = sqlite3.connect(path)
    cols = {r[1] for r in con.execute("pragma table_info(math_submissions)")}
    assert {"user_id", "problem_id", "verdict", "passed", "total", "code", "xp_gained"} <= cols
    assert "ix_math_submissions_user" in [r[1] for r in con.execute("pragma index_list(math_submissions)")]
    con.close()

    command.downgrade(cfg, "0012")
    con = sqlite3.connect(path)
    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    assert "math_submissions" not in tables and "math_runs" in tables
    con.close()
