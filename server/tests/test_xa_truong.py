"""Xạ Trường (docs/THUC_CHIEN_TRONG_GAME.md, tier 1): exercises marked by quality.

A scored exercise trains a small model. Each hidden test is one data set made from a seed:
the player's machine gets the training data and the points to predict, sends back one
prediction per point, and the server - which alone holds the labels - computes accuracy or
error, the mean over the sets, and the grade (hạ / trung / thượng phẩm). These tests play
the player's machine: they send back predictions of a chosen quality and check the grade,
the Tu Vi (tier XP x grade / 3, only for progress), what malformed predictions get, the
nodes of Đạo Thụ that hold the exercises, and that the data really comes from its seeds.
"""
import datetime as dt
import math

import pytest

from app import db as dbm
from app.learning import math_path as mp
from app.learning import math_problems as pr
from app.learning import xa_truong_data as xt
from app.models import MathRun, MathSubmission
from app.systems import math_code
from app.systems import math_tree_progress as tp
from tests.test_math_loop import make
from tests.test_math_problems import rows_of, send, tu_vi

KNN = "xt_knn_phan_loai"               # accuracy, bars 65% / 75% / 82%, node ud_knn
LINE = "xt_hq_khop_duong_thang"        # error (RMSE), bars 2.0 / 1.5 / 1.2, node ud_hoi_quy_1_bien
LUYEN_KHI_UD = ["ud_knn", "ud_naive_bayes", "ud_hoi_quy_1_bien", "ud_binh_phuong_toi_thieu", "ud_mang_no_ron",
                "ud_logistic", "ud_pca", "ud_ab_test", "du_an_luyen_khi"]


# ------------------------------------------------------------------ helpers
def tree():
    return tp.tree()


def labels(problem_id: str) -> list[list[str]]:
    return [t.expected.split() for t in pr.problem(problem_id).tests]


def predictions(problem_id: str, wrong_share: float = 0.0) -> list[str]:
    """The true labels with the first `wrong_share` of each set changed to another class."""
    out = []
    for want in labels(problem_id):
        cut = round(len(want) * wrong_share)
        got = [str((int(v) + 1) % 3) if i < cut else v for i, v in enumerate(want)]
        out.append("\n".join(got) + "\n")
    return out


def shifted(problem_id: str, by: float) -> list[str]:
    """Regression answers off by exactly `by` everywhere: the RMSE is `by`."""
    return ["\n".join(f"{float(v) + by:.6f}" for v in want) + "\n" for want in labels(problem_id)]


async def open_node(uid: int, node_id: str) -> None:
    """Every node `node_id` waits for, done: each part's trial passed, each exercise solved."""
    t = tree()
    seen, todo = set(), list(t.nodes[node_id].requires)
    async with dbm.SessionLocal() as db:
        while todo:
            nid = todo.pop()
            if nid in seen:
                continue
            seen.add(nid)
            todo += t.nodes[nid].requires
            for part in tp.parts(nid):
                db.add(MathRun(user_id=uid, subject_id=part.subject_id, node_id=nid, floor=part.floor,
                               mode="trial", tier=mp.floor_tiers(part.floor)[1], asked=1, correct=1, passed=True,
                               started_at=dt.datetime(2026, 1, 1), ended_at=dt.datetime(2026, 1, 1)))
            for pid in t.nodes[nid].problems:
                db.add(MathSubmission(user_id=uid, problem_id=pid, subject_id="x", floor=1, tier=1, verdict="AC",
                                      passed=3, total=3, ms=1, xp_gained=0, code="",
                                      created_at=dt.datetime(2026, 1, 1), judged_at=dt.datetime(2026, 1, 1)))
        await db.commit()


async def status(uid: int) -> dict:
    async with dbm.SessionLocal() as db:
        return (await tp.state(db, uid)).status


async def hand_in(client, h, problem_id: str, outputs: list[str], **kw) -> dict:
    r = await client.post(f"/math/problem/{problem_id}/tests", json={}, headers=h)
    assert r.status_code == 200, r.text
    r = await send(client, h, problem_id, outputs, r.json()["attempt_id"], **kw)
    assert r.status_code == 200, r.text
    return r.json()


# ------------------------------------------------------------------ the content
def test_every_thuc_chien_node_of_luyen_khi_has_two_to_four_exercises_and_says_so():
    t = tree()
    for nid in LUYEN_KHI_UD:
        node = t.nodes[nid]
        assert node.content == "co", nid
        assert 2 <= len(node.problems) <= 4 or nid == "du_an_luyen_khi", nid
        assert all(pid in pr.bank() for pid in node.problems), nid
        assert pr.bank()[node.problems[-1]].scored, f"{nid} must end with a scored exercise"


def test_a_scored_exercise_has_bars_a_generator_and_a_naive_program():
    scored = [p for p in pr.bank().values() if p.scored]
    assert len(scored) == 9
    for p in scored:
        assert len(p.grades) == pr.GRADES and p.data and p.data.gen in xt.GENERATORS
        assert p.test_count == len(p.data.seeds) >= 4
        assert pr.naive_path(p.subject, p.id).is_file() and pr.solution_path(p.subject, p.id).is_file()
        higher = pr.SCORED[p.checker]
        assert list(p.grades) == sorted(p.grades, reverse=not higher)


def test_the_same_seed_gives_the_same_set_and_another_seed_another():
    for name in xt.GENERATORS:
        a, b, c = xt.generate(name, 5), xt.generate(name, 5), xt.generate(name, 6)
        assert a == b and a != c, name
        data, truth = a
        assert data.isascii() and truth.isascii() and data.endswith("\n") and truth.endswith("\n")


def test_the_statement_hands_out_practice_sets_but_never_a_hidden_label():
    p = pr.problem(KNN)
    view = p.view()
    assert view["scored"] and view["grades"] == [0.65, 0.75, 0.82] and view["higher_better"]
    assert view["tests"] == 4 and view["starter"]
    big = [s for s in view["samples"] if s.get("big")]
    assert len(big) == len(p.data.practice_seeds) and big[0]["out"] == xt.generate(p.data.gen, 7)[1]
    shown = repr(view)
    for t in p.tests:
        assert t.data not in shown and t.expected not in shown


def test_the_hidden_input_carries_the_training_labels_but_not_the_labels_of_the_targets():
    for t in pr.problem(KNN).tests:
        lines = t.data.splitlines()
        n, d = map(int, lines[0].split())
        m = int(lines[1 + n])
        assert all(len(row.split()) == d + 1 for row in lines[1:1 + n])
        assert len(lines) == 2 + n + m and all(len(row.split()) == d for row in lines[2 + n:])
        assert len(t.expected.split()) == m


# ------------------------------------------------------------------ the marking
def test_accuracy_counts_right_predictions_and_a_number_matches_its_spelling():
    assert pr.score_output("0\n1\n2\n1\n", "0 1 2 2", pr.ACCURACY) == (0.75, "")
    assert pr.score_output("1\n0\n", "1.0\n0\n", pr.ACCURACY) == (1.0, "")
    assert pr.score_output("A\nB\n0\n", "A B 0", pr.ACCURACY) == (1.0, "")


def test_a_wrong_number_of_predictions_scores_nothing_and_says_why():
    assert pr.score_output("0\n1\n2\n", "0 1", pr.ACCURACY) == (0.0, "count:3:2")
    assert pr.score_output("0\n1\n", "0 1 1", pr.ACCURACY) == (0.0, "count:2:3")
    assert pr.score_output("1.0\n2.0\n", "1.0", pr.ERROR) == (None, "count:2:1")


def test_the_error_is_the_root_mean_square_and_a_word_or_nan_is_no_score():
    score, note = pr.score_output("1\n2\n3\n4\n", "2 3 4 5", pr.ERROR)
    assert math.isclose(score, 1.0) and note == ""
    score, _ = pr.score_output("0\n0\n", "3 4", pr.ERROR)
    assert math.isclose(score, math.sqrt(12.5))
    assert pr.score_output("1\n2\n", "1 hai", pr.ERROR) == (None, "not_number")
    assert pr.score_output("1\n2\n", "1 nan", pr.ERROR) == (None, "not_number")


@pytest.mark.parametrize("scores,grade", [((0.90, 0.85), 3), ((0.80, 0.78), 2), ((0.70, 0.66), 1), ((0.5, 0.6), 0)])
def test_the_mean_over_the_sets_decides_the_grade(scores, grade):
    tests = [pr.Test("", "1\n" * 100) for _ in scores]
    outputs = ["1\n" * round(s * 100) + "0\n" * (100 - round(s * 100)) for s in scores]
    j = pr.judge_scored(tests, outputs, (0.65, 0.75, 0.82), pr.ACCURACY)
    assert j.grade == grade and j.passed == grade and j.total == 3
    assert math.isclose(j.score, sum(scores) / len(scores))
    assert j.verdict == ("AC" if grade == 3 else "WA") and math.isclose(j.share, grade / 3)


def test_lower_is_better_for_an_error():
    tests = [pr.Test("", "0\n0\n") for _ in range(2)]
    grade = lambda e: pr.judge_scored(tests, [f"{e}\n{-e}\n"] * 2, (2.0, 1.5, 1.2), pr.ERROR).grade  # noqa: E731
    assert (grade(1.0), grade(1.3), grade(1.9), grade(2.5)) == (3, 2, 1, 0)


def test_a_crash_on_a_set_scores_that_set_zero_and_names_it():
    tests = [pr.Test("", "1\n1\n") for _ in range(4)]
    j = pr.judge_scored(tests, ["1\n1\n", "1\n1\n", ""], (0.65, 0.75, 0.82), pr.ACCURACY, status="re",
                        error="ZeroDivisionError")
    assert [r.verdict for r in j.results] == ["AC", "AC", "RE", "-"]
    assert math.isclose(j.score, 0.5) and j.grade == 0 and j.verdict == "RE" and j.error == "ZeroDivisionError"
    j = pr.judge_scored(tests, [], (2.0, 1.5, 1.2), pr.ERROR, status="ce")
    assert j.verdict == "CE" and j.score is None and j.grade == 0


def test_an_error_with_an_unscorable_set_has_no_score_at_all():
    tests = [pr.Test("", "1\n") for _ in range(3)]
    j = pr.judge_scored(tests, ["1\n", "x\n", "1\n"], (2.0, 1.5, 1.2), pr.ERROR)
    assert j.score is None and j.grade == 0 and j.results[1].note == "not_number"


# ------------------------------------------------------------------ the nodes of Đạo Thụ
async def test_an_exercise_of_a_thuc_chien_node_waits_for_that_node(client):
    h, uid = await make(client, "xa_1")
    t = tree()
    owner = t.node_of_skill()[pr.problem(KNN).skill]
    await open_node(uid, owner)                               # R10 alone would open it now...
    async with dbm.SessionLocal() as db:
        st = await tp.state(db, uid)
    assert tp.problem_open(st, pr.problem(KNN)) and st.status["ud_knn"] == "locked"
    assert not math_code.problem_open(st, pr.problem(KNN))     # ...but the node is still shut
    r = await client.get(f"/math/problem/{KNN}", headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked"
    listed = (await client.get("/math/problems", params={"subject_id": "dai_so_tuyen_tinh"}, headers=h)).json()
    assert KNN not in [p["id"] for f in listed["floors"] for p in f["problems"]]
    await open_node(uid, "ud_knn")
    assert (await status(uid))["ud_knn"] == "open"
    assert (await client.get(f"/math/problem/{KNN}", headers=h)).status_code == 200


async def test_the_node_is_done_when_every_exercise_reaches_thuong_pham(client):
    h, uid = await make(client, "xa_2")
    await open_node(uid, "ud_knn")
    first, second, last = tree().nodes["ud_knn"].problems
    for pid in (first, second):
        res = await hand_in(client, h, pid, [t.expected for t in pr.problem(pid).tests])
        assert res["result"]["verdict"] == "AC"
    res = await hand_in(client, h, last, predictions(last, 0.2))       # trung phẩm: not enough
    assert res["result"]["grade"] == 2
    assert (await status(uid))["ud_knn"] == "open"
    res = await hand_in(client, h, last, predictions(last))
    assert res["result"]["grade"] == 3
    assert (await status(uid))["ud_knn"] == "done"
    assert (await client.get(f"/math/problem/{last}", headers=h)).status_code == 200     # done: still open


async def test_the_project_lists_its_exercises_from_three_subjects(client):
    h, uid = await make(client, "xa_3")
    await open_node(uid, "du_an_luyen_khi")
    ids = tree().nodes["du_an_luyen_khi"].problems
    assert len({pr.problem(p).subject for p in ids}) == 3
    r = await client.get("/math/problems", params={"subject_id": pr.problem(ids[0]).subject, "ids": ",".join(ids)},
                         headers=h)
    listed = [p["id"] for f in r.json()["floors"] for p in f["problems"]]
    assert sorted(listed) == sorted(ids)


# ------------------------------------------------------------------ one go, through the API
async def test_thuong_pham_pays_the_full_tier_xp(client):
    h, uid = await make(client, "xa_4")
    await open_node(uid, "ud_knn")
    before = await tu_vi(uid)
    res = await hand_in(client, h, KNN, predictions(KNN), times_ms=[30] * 4)
    r = res["result"]
    full = mp.xp_for_tier(pr.problem(KNN).tier)
    assert r["scored"] and r["metric"] == "do_chinh_xac" and r["score"] == 1.0
    assert (r["grade"], r["grade_vi"], r["verdict"], r["passed"], r["total"]) == (3, "Thượng phẩm", "AC", 3, 3)
    assert [t["verdict"] for t in r["tests"]] == ["AC"] * 4 and all(t["score"] == 1.0 for t in r["tests"])
    assert res["xp_gained"] == full and await tu_vi(uid) - before == full
    assert res["best"]["grade"] == 3 and res["best"]["grade_vi"] == "Thượng phẩm"
    assert [(s.verdict, s.passed, s.total) for s in await rows_of(uid) if s.problem_id == KNN] == [("AC", 3, 3)]


async def test_a_middle_grade_pays_its_share_and_only_progress_pays_again(client):
    h, uid = await make(client, "xa_5")
    await open_node(uid, "ud_knn")
    full = mp.xp_for_tier(pr.problem(KNN).tier)
    res = await hand_in(client, h, KNN, predictions(KNN, 0.22))          # 78%: trung phẩm
    assert res["result"]["grade"] == 2 and math.isclose(res["result"]["score"], 0.78, abs_tol=0.01)
    assert res["result"]["verdict"] == "WA" and res["xp_gained"] == round(full * 2 / 3)
    res = await hand_in(client, h, KNN, predictions(KNN, 0.30))          # 70%: hạ phẩm, worse: nothing
    assert res["result"]["grade"] == 1 and res["xp_gained"] == 0 and res["best"]["grade"] == 2
    res = await hand_in(client, h, KNN, predictions(KNN))                # thượng: only the rest
    assert res["result"]["grade"] == 3 and res["xp_gained"] == full - round(full * 2 / 3)
    res = await hand_in(client, h, KNN, predictions(KNN))                # the same again: nothing
    assert res["xp_gained"] == 0


async def test_an_error_exercise_is_graded_by_how_far_off_the_predictions_are(client):
    h, uid = await make(client, "xa_6")
    await open_node(uid, "ud_hoi_quy_1_bien")
    for by, grade in ((1.4, 2), (1.9, 1), (2.5, 0), (0.5, 3)):
        res = await hand_in(client, h, LINE, shifted(LINE, by))
        r = res["result"]
        assert r["metric"] == "sai_so" and not r["higher_better"] and math.isclose(r["score"], by, abs_tol=1e-3)
        assert r["grade"] == grade, (by, r)


async def test_a_naive_model_gets_nothing(client):
    h, uid = await make(client, "xa_7")
    await open_node(uid, "ud_knn")
    majority = []
    for want in labels(KNN):
        top = max(set(want), key=want.count)
        majority.append(f"{top}\n" * len(want))
    res = await hand_in(client, h, KNN, majority)
    assert res["result"]["grade"] == 0 and res["result"]["grade_vi"] == "Chưa đạt" and res["xp_gained"] == 0


async def test_malformed_predictions_score_nothing_and_say_what_was_wrong(client):
    h, uid = await make(client, "xa_8")
    await open_node(uid, "ud_hoi_quy_1_bien")
    await open_node(uid, "ud_knn")
    good = predictions(KNN)
    res = await hand_in(client, h, KNN, [good[0], good[1] + "2\n", "", "0 1 2"])
    tests = res["result"]["tests"]
    assert tests[0]["score"] == 1.0 and tests[1]["score"] == 0.0 and tests[1]["note"].startswith("count:")
    assert res["result"]["grade"] == 0 and res["xp_gained"] == 0
    words = shifted(LINE, 0.0)
    words[2] = words[2].replace("\n", " xa\n", 1)
    res = await hand_in(client, h, LINE, words)
    assert res["result"]["score"] is None and res["result"]["grade"] == 0
    assert res["result"]["tests"][2]["note"] in ("not_number", f"count:{len(labels(LINE)[2])}:{len(labels(LINE)[2]) + 1}")
    r = await client.post(f"/math/problem/{KNN}/tests", json={}, headers=h)
    r = await send(client, h, KNN, good + [good[0]], r.json()["attempt_id"])     # more outputs than sets
    assert r.status_code == 400 and r.json()["error"]["code"] == "too_many_outputs"


async def test_chay_thu_scores_the_samples_and_the_practice_set_and_pays_nothing(client):
    h, uid = await make(client, "xa_9")
    await open_node(uid, "ud_knn")
    samples = pr.problem(KNN).samples
    r = await send(client, h, KNN, [s.expected for s in samples])
    assert r.status_code == 200
    res = r.json()
    assert res["mode"] == "run" and res["result"]["grade"] == 3 and "xp" not in res
    assert len(res["result"]["tests"]) == len(samples) >= 2
    assert await rows_of(uid) == [] or all(s.problem_id != KNN for s in await rows_of(uid))
