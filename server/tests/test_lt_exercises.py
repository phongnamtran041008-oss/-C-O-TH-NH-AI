"""The programming exercises of the Lập Trình nodes of Luyện Khí in Đạo Thụ: every node but NumPy
has 3-5 of them, they sit on micro-skills the player has already reached when the node opens,
the node is done when all of them are solved, and the hidden tests reject the typical wrong
programs (data/lt_mutants.json, one list of deliberately wrong programs per exercise).

The reference solutions reproducing every answer is tools/check_all.py's job; here is the
shape of the content and how it plugs into the tree.
"""
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

import pytest

from app import db as dbm
from app.learning import math_path, math_problems as pr, math_tree
from app.models import MathSubmission
from app.systems import math_tree_progress as tp
from tests.test_math_loop import make
from tests.test_math_tree_progress import state, tree

ROOT = Path(__file__).resolve().parents[2]
MUTANTS = json.loads((Path(__file__).parent / "data" / "lt_mutants.json").read_text("utf-8"))

#: the Lập Trình nodes of Luyện Khí; each has exercises. lt_numpy's teach the ideas of NumPy on plain lists
#: (NumPy is not installed with the game, curriculum review 2026-11-20).
CODE_NODES = ["lt_python_co_ban", "lt_cau_truc_du_lieu", "lt_vecto_bang_code", "lt_ham_de_quy",
              "lt_ma_tran_gauss", "lt_numpy", "lt_mo_phong_xac_suat", "lt_do_phuc_tap", "lt_dao_ham_so", "lt_do_thi"]
NEW_PROBLEMS = sorted(pid for pid in pr.bank() if pid in MUTANTS)


def ancestors(node_id: str) -> set[str]:
    out: set[str] = set()
    todo = list(tree().nodes[node_id].requires)
    while todo:
        n = todo.pop()
        if n not in out:
            out.add(n)
            todo += tree().nodes[n].requires
    return out


# ------------------------------------------------------------------ what is written
def test_every_lap_trinh_node_of_luyen_khi_has_three_to_five_exercises_but_numpy():
    t = tree()
    lt = [n.id for n in t.nodes.values() if n.branch == "lt" and n.realm == "luyen_khi"]
    assert sorted(lt) == sorted(CODE_NODES)
    for nid in CODE_NODES:
        node = t.nodes[nid]
        assert 3 <= len(node.problems) <= 5, nid
        assert node.content == "co", nid
        assert len(set(node.problems)) == len(node.problems)
    # NumPy is not installed with the game: its exercises teach the ideas (shapes, broadcasting, axis sums,
    # X @ w + b, X.T @ X) on plain lists, and the node says so
    numpy = t.nodes["lt_numpy"]
    assert len(numpy.problems) == 5 and all(p.startswith("dstt_bt_np_") for p in numpy.problems)
    assert "Python thuần" in numpy.why_vi and "không cài NumPy" in numpy.why_vi


def test_the_exercise_files_are_well_formed():
    assert math_path.validate_all() == []
    assert pr.validate_all() == []
    assert math_tree.validate_all() == []


def test_a_node_lists_one_subjects_exercises_in_the_order_the_list_shows_them():
    """The "Làm bài" button of a node opens the exercise list of the subject of its first exercise and keeps
    the node's own exercises, so a node must not mix subjects; and that list is ordered by floor, tier, id."""
    for nid in CODE_NODES:
        problems = [pr.problem(p) for p in tree().nodes[nid].problems]
        assert len({p.subject for p in problems}) == 1, nid
        assert [(p.floor, p.tier, p.id) for p in problems] == sorted((p.floor, p.tier, p.id) for p in problems), nid
        assert len({p.skill for p in problems}) >= 1


def test_an_exercise_belongs_to_one_node_and_every_exercise_of_a_node_is_used_by_it():
    seen: dict[str, str] = {}
    for nid in CODE_NODES:
        for pid in tree().nodes[nid].problems:
            assert pid not in seen, f"{pid} is listed by {seen[pid]} and {nid}"
            seen[pid] = nid
    assert set(seen) >= set(NEW_PROBLEMS)                            # none of the new ones is orphaned


def test_each_exercise_has_a_sample_hidden_tests_and_answers_that_tell_programs_apart():
    config = math_path.cfg()["programming"]
    for pid in NEW_PROBLEMS:
        p = pr.problem(pid)
        assert not p.reviewed                                         # new content waits for a human read
        assert len(p.tests) >= config["min_tests"] and len(p.samples) >= 1
        assert len({t.expected.strip() for t in p.tests}) > 1, pid
        assert all(len(t.expected) <= config["max_output_chars"] for t in p.tests), pid
        assert all(len(t.data) <= 400_000 for t in p.tests), pid         # inputs are kept in the JSON
        assert p.time_limit_ms <= 4000, pid


def test_a_simulation_spells_out_its_random_numbers_so_every_machine_gets_the_same_answer():
    sims = [p for p in tree().nodes["lt_mo_phong_xac_suat"].problems if "tong_n_xuc_xac" not in p]
    assert len(sims) == 4
    for pid in sims:
        text = " ".join(pr.problem(pid).statement_vi)
        assert "1103515245" in text and "hạt giống" in text, pid        # the generator is in the statement
        assert "random" not in text.lower(), pid


# ------------------------------------------------------------------ how it plugs into the tree
def test_an_exercise_never_opens_before_the_node_that_lists_it_could_be_reached():
    """An exercise is open when the node of its micro-skill is open or done (R10), and the player does the
    exercises of a Lập Trình node when that node is open. So the micro-skill's node must be one the Lập Trình
    node needs (a prerequisite, however far back), or one that opens at the same time as the Lập Trình node
    does (every prerequisite of it is one of the Lập Trình node's), and never a node of a later stage."""
    t = tree()
    for nid in CODE_NODES:
        before = ancestors(nid)
        for pid in t.nodes[nid].problems:
            owner = t.nodes[t.node_of_skill()[pr.problem(pid).skill]]
            assert owner.id in before or set(owner.requires) <= before, (pid, owner.id)
            if owner.main:
                assert owner.stage <= t.nodes[nid].stage, (pid, owner.id, owner.stage)


@pytest.mark.parametrize("node_id", CODE_NODES)
async def test_the_exercises_of_a_node_are_open_once_the_node_is_open_and_not_before(client, node_id):
    h, uid = await make(client)
    st = await state(uid)
    node = tree().nodes[node_id]
    problems = [pr.problem(p) for p in node.problems]
    # the node is open: everything it needs is done
    st.status.clear()
    before = ancestors(node_id)
    st.status.update({n.id: "done" if n.id in before else "open" if set(n.requires) <= before else "locked"
                      for n in st.tree.nodes.values()})
    assert st.status[node_id] == "open"
    assert all(tp.problem_open(st, p) for p in problems), node_id
    # nothing is done: an exercise on a micro-skill whose node is shut stays shut
    st.status.clear()
    st.status.update({n: "locked" for n in st.tree.nodes})
    for p in problems:
        owner = tree().node_of_skill()[p.skill]
        st.status[owner] = "locked"
        assert not tp.problem_open(st, p), (p.id, owner)
        st.status[owner] = "open"
        assert tp.problem_open(st, p)


async def test_a_new_player_can_open_python_nhap_mon_but_not_the_dijkstra_exercise(client):
    h, uid = await make(client)
    for pid in tree().nodes["lt_python_co_ban"].problems:
        assert (await client.get(f"/math/problem/{pid}", headers=h)).status_code == 200, pid
    for pid in ("tr_bt_dijkstra", "xs_bt_bernoulli_mo_phong", "gt_bt_toc_do_hoc", "dstt_bt_so_nghiem_he"):
        r = await client.get(f"/math/problem/{pid}", headers=h)
        assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked", pid


async def _submit(uid: int, problem_id: str) -> None:
    p = pr.problem(problem_id)
    async with dbm.SessionLocal() as db:
        db.add(MathSubmission(user_id=uid, problem_id=problem_id, subject_id=p.subject, floor=p.floor, tier=p.tier,
                              verdict="AC", passed=len(p.tests), total=len(p.tests), ms=1, xp_gained=0,
                              created_at=dt.datetime(2026, 1, 1), judged_at=dt.datetime(2026, 1, 1)))
        await db.commit()


@pytest.mark.parametrize("node_id", CODE_NODES)
async def test_a_node_is_done_when_every_one_of_its_exercises_is_solved(client, node_id):
    h, uid = await make(client)
    problems = list(tree().nodes[node_id].problems)
    for pid in problems[:-1]:
        await _submit(uid, pid)
    st = await state(uid)
    assert st.status[node_id] != "done" and st.status[node_id] != "vacant", node_id
    await _submit(uid, problems[-1])
    st = await state(uid)
    assert st.status[node_id] == "done" and set(problems) <= st.solved


async def test_the_tree_view_lists_the_exercises_of_every_lap_trinh_node_of_luyen_khi(client):
    h, uid = await make(client)
    view = (await client.get("/math/tree", headers=h)).json()
    by = {n["id"]: n for n in view["nodes"]}
    for nid in CODE_NODES:
        listed = by[nid]["problems"]
        assert [p["id"] for p in listed] == list(tree().nodes[nid].problems), nid
        assert all(p["title_vi"] and p["subject_id"] and p["solved"] is False for p in listed)
        assert by[nid]["state"] != "vacant" and by[nid]["state_vi"] is None
    # every Lập Trình node of Luyện Khí has exercises now; the ones of the later realms still wait for their content
    assert not [n["id"] for n in view["nodes"] if n["branch"] == "lt" and n["state"] == "vacant"
                and tree().nodes[n["id"]].realm == "luyen_khi"]
    assert {n["id"] for n in view["nodes"] if n["branch"] == "lt" and n["state"] == "vacant"} >= {"tc_python_nang_cao"}


# ------------------------------------------------------------------ the hidden tests have teeth
@pytest.mark.parametrize("problem_id", NEW_PROBLEMS)
def test_the_hidden_tests_reject_every_listed_wrong_program(problem_id):
    sys.path.insert(0, str(ROOT))
    try:
        from client.engine import coderun
    finally:
        sys.path.remove(str(ROOT))
    problem = pr.problem(problem_id)
    wrong = MUTANTS[problem_id]
    assert len(wrong) >= 2
    with tempfile.TemporaryDirectory(prefix="kvtt_lt_") as tmp:
        path = Path(tmp) / "bai_lam.py"
        for m in wrong:
            coderun.write_solution(path, m["code"])
            attempt = coderun.run_tests(path, [t.data for t in problem.tests], problem.time_limit_ms)
            verdict = pr.judge(list(problem.tests), attempt.outputs, attempt.status, attempt.times_ms,
                               problem.checker, attempt.error)
            assert not verdict.accepted, f"{problem_id}: the wrong program {m['name']!r} is accepted"
