"""Đạo Thụ wired into the game: where a player stands in the curriculum tree
(systems/math_tree_progress.py) and how the question loop, the old entry points and every
mode outside a sitting obey it. One section per rule of the contract, R1-R12, then a player
who walks the whole Luyện Khí main path by passing Thiên kiếp nhỏ node by node.
"""
import datetime as dt
import random
import sqlite3
from types import SimpleNamespace

from app import clock
from app import db as dbm
from app.learning import math_mastery as mm
from app.learning import math_path as mp
from app.learning import math_problems as pr
from app.learning import math_tree
from app.models import MathAnswer, MathRun, User
from app.systems import math_ask, math_combat, math_dungeon, math_practice, math_skills
from app.systems import math_tree_progress as tp
from tests.test_math_loop import log_answers, make, play
from tests.test_math_mastery import play_trial

LA, GT, XS, TR = "dai_so_tuyen_tinh", "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac"


# ------------------------------------------------------------------ helpers
def tree():
    return math_tree.tree()


async def state(uid) -> tp.TreeState:
    async with dbm.SessionLocal() as db:
        return await tp.state(db, uid)


async def pass_part(uid, node_id, floor=None, subject=None):
    """A passed Thiên kiếp nhỏ on one part of a node (the first part by default)."""
    part = next(p for p in tp.parts(node_id) if floor is None or p.floor == floor)
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id=subject or part.subject_id, node_id=node_id, floor=part.floor,
                       mode="trial", tier=mp.floor_tiers(part.floor)[1], asked=1, correct=1, passed=True,
                       started_at=dt.datetime(2026, 1, 1), ended_at=dt.datetime(2026, 1, 1)))
        await db.commit()


async def pass_node(uid, node_id):
    for p in tp.parts(node_id):
        await pass_part(uid, node_id, p.floor)


async def old_trial(uid, subject, floor):
    """A passed trial of an old save: no node, the whole floor."""
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id=subject, floor=floor, mode="trial", tier=mp.floor_tiers(floor)[1],
                       asked=1, correct=1, passed=True, started_at=dt.datetime(2026, 1, 1),
                       ended_at=dt.datetime(2026, 1, 1)))
        await db.commit()


async def meet_part_gate(uid, part):
    """The log the mastery gate wants, for the micro-skills of one part only."""
    lo, hi = mp.floor_tiers(part.floor)
    window = mp.cfg()["mastery_gate"]["window"]
    for skill in part.skills:
        for tier in range(lo, hi + 1):
            await log_answers(uid, skill, tier, [True] * window, floor=part.floor)


async def solve(client, h, problem_id):
    """Hand in a program that gets every hidden test right."""
    r = await client.post(f"/math/problem/{problem_id}/tests", json={}, headers=h)
    assert r.status_code == 200, r.text
    outputs = [t.expected for t in pr.problem(problem_id).tests]
    r = await client.post(f"/math/problem/{problem_id}/judge",
                          json={"outputs": outputs, "attempt_id": r.json()["attempt_id"]}, headers=h)
    assert r.status_code == 200 and r.json()["result"]["verdict"] == "AC", r.text


async def solve_node(client, h, node_id):
    """Hand in every exercise of a programming node."""
    for pid in tree().nodes[node_id].problems:
        await solve(client, h, pid)


async def clear_stage_one(client, h, uid):
    """The whole first stage of Luyện Khí: its four maths nodes and Python nhập môn."""
    for nid in ("ds_ngon_ngu", "gt_ham_so", "xs_dem_su_kien", "tr_logic_dem"):
        await pass_node(uid, nid)
    await solve_node(client, h, "lt_python_co_ban")


def without_floors(*floors):
    """A stand-in for math_practice._templates with no question on these (subject, floor)s."""
    real = math_practice._templates
    return lambda s, f: [] if (s, f) in floors else real(s, f)


async def real_nodes_of_stage(uid, stage):
    """The main-path nodes of a Luyện Khí stage that have anything to learn (a vacant one is no work)."""
    st = await state(uid)
    return sum(1 for n in tree().main_nodes("luyen_khi") if n.stage == stage and st.status[n.id] != "vacant")


def tree_with(**changes) -> math_tree.Tree:
    """The real tree with some raw changes: cut=[...] adds cut micro-skills, requires={node: [...]}."""
    import copy
    raw = copy.deepcopy(tree().raw)
    raw["cut"]["skills"] = raw["cut"]["skills"] + list(changes.get("cut", []))
    for n in raw["nodes"]:
        if n["id"] in changes.get("requires", {}):
            n["requires"] = changes["requires"][n["id"]]
    return math_tree.build(raw)


async def node_start(client, h, node_id, floor=None, trial=False):
    body = {"node_id": node_id} if floor is None else {"node_id": node_id, "floor": floor}
    return await client.post("/math/node/trial" if trial else "/math/node/start", json=body, headers=h)


# ------------------------------------------------------------------ R1: parts
def test_a_node_is_made_of_its_micro_skills_grouped_by_floor():
    la1 = [k.id for k in mp.subject(LA).floor(1).skills]
    assert tp.parts("ds_ngon_ngu") == [tp.Part("ds_ngon_ngu", LA, 1, tuple(la1))]
    two = tp.parts("gt_gioi_han")                          # a node across two floors: one part each
    assert [(p.subject_id, p.floor) for p in two] == [(GT, 2), (GT, 3)]
    for p in two:                                          # in path order, only the node's own
        floor = [k.id for k in mp.subject(GT).floor(p.floor).skills]
        assert list(p.skills) == [s for s in floor if s in tree().nodes["gt_gioi_han"].skills]
    assert [p.floor for p in tp.parts("gt_gioi_han_nang_cao")] == [2, 3]       # the optional twin too
    assert tp.parts("lt_python_co_ban") == [] and tp.parts("ud_knn") == []     # no micro-skills, no parts
    for node in tree().nodes.values():                     # the parts hold exactly the node's micro-skills
        assert sorted(s for p in tp.parts(node) for s in p.skills) == sorted(node.skills)


def test_several_nodes_can_share_a_floor_and_the_floor_lists_them_by_stage():
    assert [p.node_id for p in tp.floor_parts(LA, 9)] == ["ds_truc_giao_chieu", "ds_tri_rieng", "ds_pca_svd"]
    assert [p.node_id for p in tp.floor_parts(GT, 1)] == ["gt_ham_so", "gt_tinh_chat_ham"]   # main first


# ------------------------------------------------------------------ R2: a part is passed
async def test_a_part_is_passed_by_its_own_trial_and_the_node_by_all_of_its_parts(client):
    h, uid = await make(client)
    await pass_node(uid, "gt_ham_so")
    await pass_part(uid, "gt_gioi_han", 2)
    st = await state(uid)
    first, second = tp.parts("gt_gioi_han")
    assert st.part_passed(first) and not st.part_passed(second)
    assert st.status["gt_gioi_han"] == "open"
    assert not st.part_passed(tp.parts("gt_gioi_han_nang_cao")[0])      # the same floor, another node
    await pass_part(uid, "gt_gioi_han", 3)
    assert (await state(uid)).status["gt_gioi_han"] == "done"


async def test_a_failed_trial_or_a_buoi_luyen_passes_nothing(client):
    h, uid = await make(client)
    async with dbm.SessionLocal() as db:
        for mode, passed in (("trial", False), ("trial", None), ("practice", None)):
            db.add(MathRun(user_id=uid, subject_id=LA, node_id="ds_ngon_ngu", floor=1, mode=mode, tier=2,
                           passed=passed, started_at=dt.datetime(2026, 1, 1)))
        await db.commit()
    assert (await state(uid)).status["ds_ngon_ngu"] == "open"


async def test_an_old_trial_without_a_node_passes_every_part_of_its_floor(client):
    h, uid = await make(client)
    await old_trial(uid, GT, 1)
    await old_trial(uid, GT, 2)
    st = await state(uid)
    assert st.status["gt_ham_so"] == "done" and st.status["gt_tinh_chat_ham"] == "done"   # floor 1, both nodes
    assert st.part_passed(tp.parts("gt_gioi_han")[0]) and st.part_passed(tp.parts("gt_gioi_han_nang_cao")[0])
    assert st.status["gt_gioi_han"] == "open"              # its floor-3 part is still to do
    await old_trial(uid, GT, 3)
    assert (await state(uid)).status["gt_gioi_han"] == "done"


async def test_the_placement_test_passes_the_whole_floors_it_skipped(client):
    h, uid = await make(client)
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id=LA, floor=4, mode="placement", tier=3, passed=True,
                       started_at=dt.datetime(2026, 1, 1), ended_at=dt.datetime(2026, 1, 1)))
        await db.commit()
    st = await state(uid)
    assert [st.status[n] for n in ("ds_ngon_ngu", "ds_so_phuc", "ds_vecto_ma_tran")] == ["done"] * 3
    assert st.status["ds_nhan_ma_tran"] == "open"          # the start floor: nothing waived
    assert tp.cleared_floors_of(st, LA) == {1, 2, 3}


# ------------------------------------------------------------------ R3: done, and vacant
async def test_a_vacant_node_counts_as_done_and_is_shown_as_being_written(client):
    h, uid = await make(client)
    st = await state(uid)
    # every node of Luyện Khí has content now; the Lập Trình node of Trúc Cơ is still empty
    assert st.status["tc_python_nang_cao"] == "vacant" and "tc_python_nang_cao" in st.done
    assert st.status["lt_numpy"] == "locked"                # it has exercises (curriculum review) and waits
    # the realm project got its exercises with Xạ Trường: no longer vacant, it waits for its prerequisites
    assert st.status["du_an_luyen_khi"] == "locked"
    # lt_cau_truc_du_lieu needs lt_python_co_ban (open, it has exercises) and ds_ngon_ngu: both hold it back
    assert st.status["lt_python_co_ban"] == "open" and st.status["lt_python_co_ban"] not in ("vacant", "done")
    assert st.status["lt_cau_truc_du_lieu"] == "locked"
    assert st.missing("lt_cau_truc_du_lieu") == ["lt_python_co_ban", "ds_ngon_ngu"]
    view = (await client.get("/math/tree", headers=h)).json()
    node = next(n for n in view["nodes"] if n["id"] == "tc_python_nang_cao")
    assert node["state"] == "vacant" and node["state_vi"] == "Đang biên soạn"
    assert node["parts"] == [] and node["problems"] == []
    node = next(n for n in view["nodes"] if n["id"] == "lt_python_co_ban")
    assert node["state"] == "open" and node["state_vi"] is None and len(node["problems"]) >= 3


async def test_a_vacant_node_does_not_block_and_counts_again_once_it_has_questions(client, monkeypatch):
    h, uid = await make(client)
    monkeypatch.setattr(math_practice, "_templates", without_floors((LA, 3)))
    st = await state(uid)
    assert st.status["ds_vecto_ma_tran"] == "vacant"       # its floor has no question on this server
    assert st.status["ds_nhan_ma_tran"] == "open"          # so it holds nothing back
    monkeypatch.undo()
    st = await state(uid)                                  # the day it gets questions, it counts again
    assert st.status["ds_vecto_ma_tran"] == "locked" and st.status["ds_nhan_ma_tran"] == "locked"


async def test_a_part_without_questions_does_not_count_for_its_node(client, monkeypatch):
    h, uid = await make(client)
    await pass_node(uid, "gt_ham_so")
    await pass_part(uid, "gt_gioi_han", 2)
    monkeypatch.setattr(math_practice, "_templates", without_floors((GT, 3)))
    st = await state(uid)
    assert st.status["gt_gioi_han"] == "done"
    assert [p["floor"] for p in next(n for n in (await client.get("/math/tree", headers=h)).json()["nodes"]
                                     if n["id"] == "gt_gioi_han")["parts"]] == [2]


async def test_a_programming_node_is_done_when_every_exercise_is_solved(client):
    h, uid = await make(client)
    await pass_node(uid, "ds_ngon_ngu")
    assert (await state(uid)).status["lt_cau_truc_du_lieu"] == "locked"      # Python nhập môn comes first
    basics = tree().nodes["lt_python_co_ban"].problems
    for pid in basics[:-1]:
        await solve(client, h, pid)
    assert (await state(uid)).status["lt_python_co_ban"] == "open"          # one exercise is still undone
    await solve(client, h, basics[-1])
    st = await state(uid)
    assert st.status["lt_python_co_ban"] == "done" and set(basics) <= st.solved
    assert st.status["lt_cau_truc_du_lieu"] == "open"
    problems = tree().nodes["lt_cau_truc_du_lieu"].problems
    assert 3 <= len(problems) <= 5
    for pid in problems[:-1]:
        await solve(client, h, pid)
    assert (await state(uid)).status["lt_cau_truc_du_lieu"] == "open"
    await solve(client, h, problems[-1])
    st = await state(uid)
    assert st.status["lt_cau_truc_du_lieu"] == "done" and set(problems) <= st.solved


# ------------------------------------------------------------------ R4: open
async def test_a_node_opens_when_its_requirements_are_done_even_in_another_subject(client):
    h, uid = await make(client)
    assert set(tree().nodes["tr_dem"].requires) == {"tr_logic_dem", "xs_dem_su_kien"}
    await pass_node(uid, "tr_logic_dem")
    assert (await state(uid)).status["tr_dem"] == "locked"
    r = await node_start(client, h, "tr_dem")
    assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked"
    assert tree().nodes["xs_dem_su_kien"].name_vi in r.json()["error"]["message_vi"]
    await pass_node(uid, "xs_dem_su_kien")                 # the probability node opens the algorithms one
    assert (await state(uid)).status["tr_dem"] == "open"
    assert (await node_start(client, h, "tr_dem")).status_code == 200


async def test_optional_nodes_open_by_the_same_rule_and_never_block(client):
    h, uid = await make(client)
    st = await state(uid)
    assert st.status["ds_so_phuc"] == "open" and st.status["gt_tinh_chat_ham"] == "locked"
    for node in tree().nodes.values():                     # no main node requires an optional one
        if node.main:
            assert all(tree().nodes[r].main for r in node.requires)
    await clear_stage_one(client, h, uid)
    st = await state(uid)
    assert st.status["ds_so_phuc"] == "open" and st.status["gt_tinh_chat_ham"] == "open"
    assert st.stage == ("luyen_khi", 1)                    # stage 1 reached with both optional nodes undone


# ------------------------------------------------------------------ R5: the stage
async def test_the_stage_is_reached_when_every_main_node_of_it_is_done(client):
    from app.models import Character
    h, uid = await make(client)

    async def realm():
        async with dbm.SessionLocal() as db:
            char = await db.get(Character, uid)
            return char.realm, char.realm_stage            # exercises pay xp, so xp is not part of this
    before = await realm()
    assert (await state(uid)).stage == ("luyen_khi", 0)
    for nid in ("ds_ngon_ngu", "gt_ham_so", "xs_dem_su_kien"):
        await pass_node(uid, nid)
    assert (await state(uid)).stage == ("luyen_khi", 0)    # tr_logic_dem is still missing
    mid = (await client.get("/math/tree", headers=h)).json()["stage"]["progress"]
    assert mid == {"stage": 1, "done": 3, "total": 5}      # inside the stage: 3 of its 5 real nodes
    await pass_node(uid, "tr_logic_dem")
    assert (await state(uid)).stage == ("luyen_khi", 0)    # Python nhập môn has exercises now: it counts too
    await solve_node(client, h, "lt_python_co_ban")
    assert (await state(uid)).stage == ("luyen_khi", 1)
    view = (await client.get("/math/tree", headers=h)).json()
    assert view["stage"]["progress"] == {"stage": 2, "done": 0, "total": await real_nodes_of_stage(uid, 2)}
    assert {k: v for k, v in view["stage"].items() if k != "progress"} == {
        "realm": "luyen_khi", "realm_name_vi": "Luyện Khí", "stage": 1, "stages": 9}
    assert (await client.get("/math/path", headers=h)).json()["tree"]["stage"]["stage"] == 1
    assert await realm() == before                         # shown only: the cultivation realm is not touched


# ------------------------------------------------------------------ R6: what may be asked
async def test_a_cut_micro_skill_is_never_asked_in_any_mode(client, monkeypatch):
    cut = [k.id for k in mp.subject(LA).floor(1).skills][0]
    monkeypatch.setattr(math_tree, "tree", lambda t=tree_with(cut=[cut]): t)
    h, uid = await make(client)
    assert all(t.skill != cut for t in math_practice._templates(LA, 1))
    run_id = (await client.post("/math/run/start", json={"subject_id": LA, "floor": 1}, headers=h)).json()["run"]["run_id"]
    for _ in range(18):                                    # a buổi luyện
        q, _ = await play(client, h, run_id, correct=True)
        assert q["math"]["skill"] != cut
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        rng = random.Random(3)
        for _ in range(15):                                # bí cảnh, cơ duyên, thủ thành: the player's own part
            q = await math_ask.pick_own(db, user, subject_id=LA, rng=rng)
            assert q is not None and q.meta["skill"] != cut
        monster = {"skill": cut, "subject": LA, "floor": 1, "name_vi": "Quái"}
        assert await math_combat.question_for(db, user, monster, rng) is None       # a quái lỗi sai about it
    for seed in range(15):                                 # hầm ngục
        layout = math_dungeon.generate(seed, LA, 1)
        assert all(r["skill"] != cut for r in layout["rooms"])


async def test_an_optional_nodes_micro_skills_are_asked_only_in_its_own_sittings(client):
    h, uid = await make(client)
    optional = set(tree().nodes["gt_tinh_chat_ham"].skills)          # on floor 1 of Giải Tích, beside gt_ham_so
    run_id = (await client.post("/math/run/start", json={"subject_id": GT, "floor": 1}, headers=h)).json()["run"]
    assert run_id["node_id"] == "gt_ham_so"
    for _ in range(16):
        q, _ = await play(client, h, run_id["run_id"], correct=True)
        assert q["math"]["skill"] not in optional
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        for _ in range(12):
            q = await math_ask.pick_own(db, user, subject_id=GT, rng=random.Random(_))
            assert q.meta["skill"] not in optional
    await pass_node(uid, "gt_ham_so")
    run = (await node_start(client, h, "gt_tinh_chat_ham")).json()["run"]
    asked = set()
    for _ in range(6):
        q, _ = await play(client, h, run["run_id"], correct=True)
        if not q["math"]["review"]:
            asked.add(q["math"]["skill"])
    assert asked == optional                               # its own sitting asks it


# ------------------------------------------------------------------ R7: review
async def test_review_comes_from_the_reinforced_nodes_even_of_another_subject(client):
    h, uid = await make(client)
    await pass_node(uid, "tr_logic_dem")
    await pass_node(uid, "xs_dem_su_kien")
    own = set(tree().nodes["tr_logic_dem"].skills)
    other = set(tree().nodes["xs_dem_su_kien"].skills)
    async with dbm.SessionLocal() as db:                   # tr_logic_dem was practised just now: not due
        for n, skill in enumerate(own):
            db.add(MathAnswer(user_id=uid, subject_id=TR, skill_id=skill, floor=1, tier=1, item_id=f"f{n}",
                              qtype="numeric", fingerprint=f"f{n}", correct=True, timed_out=False, review=False,
                              answer_ms=900, answered_at=clock.now()))
        await db.commit()
    run = (await node_start(client, h, "tr_dem")).json()["run"]
    reviews, labels = [], []
    for _ in range(8):
        q, _ = await play(client, h, run["run_id"], correct=True)
        if q["math"]["review"]:
            reviews.append((q["math"]["subject"], q["math"]["skill"]))
            labels.append(q["math"].get("review_node_vi"))
        else:
            assert q["math"]["skill"] in tree().nodes["tr_dem"].skills
            assert "review_node_vi" not in q["math"]
    assert len(reviews) == 2
    assert all(subj == XS and skill in other for subj, skill in reviews)    # Xác Suất, in an algorithms sitting
    assert all(name == tree().nodes["xs_dem_su_kien"].name_vi for name in labels)   # the card names the node reviewed


async def test_review_falls_back_to_done_ancestors_and_else_there_is_none(client, monkeypatch):
    h, uid = await make(client)
    for n in range(1, 8):
        await old_trial(uid, GT, n)
    node = tree().nodes["gt_tich_phan_ung_dung"]
    run = SimpleNamespace(node_id=node.id, subject_id=GT, floor=8)
    async with dbm.SessionLocal() as db:
        where = await math_practice._review_candidates(db, uid, run)
    assert set(where) == set(tree().review_skills(node.id))           # what it reinforces
    # its reinforced nodes lose their questions: the done ancestors with questions take over
    monkeypatch.setattr(math_practice, "_templates", without_floors((GT, 2), (GT, 3), (GT, 7)))
    async with dbm.SessionLocal() as db:
        where = await math_practice._review_candidates(db, uid, run)
    want = {s for a in tree().ancestors(node.id) for s in tree().nodes[a].skills
            if tp.skill_home()[s][1] not in (2, 3, 7) and tp.skill_home()[s][0] == GT}
    assert where and set(where) == want and set(where.values()) <= {1, 4, 5, 6}
    async with dbm.SessionLocal() as db:                   # the first node of a branch reviews nothing
        assert await math_practice._review_candidates(db, uid, SimpleNamespace(
            node_id="gt_ham_so", subject_id=GT, floor=1)) == {}


# ------------------------------------------------------------------ R8: gate and trial per part
async def test_the_gate_and_the_trial_of_a_part_are_its_own_micro_skills(client):
    h, uid = await make(client)
    await pass_node(uid, "gt_ham_so")
    first, second = tp.parts("gt_gioi_han")
    r = await node_start(client, h, "gt_gioi_han", floor=3, trial=True)
    assert r.status_code == 409 and r.json()["error"]["code"] == "gate_not_met"
    await meet_part_gate(uid, second)                     # only the floor-3 part: the optional twin is not needed
    r = await node_start(client, h, "gt_gioi_han", floor=3, trial=True)
    assert r.status_code == 200, r.text
    run = r.json()["run"]
    assert (run["node_id"], run["floor"], run["trial"]["total"]) == ("gt_gioi_han", 3, len(second.skills))
    assert [s["skill"] for s in r.json()["gate"]["skills"]] == list(second.skills)
    played = await play_trial(client, h, run["run_id"])
    assert [p["q"]["math"]["skill"] for p in played] == list(second.skills)
    assert {p["q"]["math"]["tier"] for p in played} == {mp.floor_tiers(3)[1]}
    st = await state(uid)
    assert st.part_passed(second) and not st.part_passed(first) and st.status["gt_gioi_han"] == "open"
    r = await node_start(client, h, "gt_gioi_han")        # the default part: the first one not passed
    assert r.json()["run"]["floor"] == 2


# ------------------------------------------------------------------ R9: the frontier
async def test_the_frontier_is_the_first_open_main_part_in_tree_order(client):
    h, uid = await make(client)
    async with dbm.SessionLocal() as db:
        assert (await tp.frontier(db, uid, LA)).node_id == "ds_ngon_ngu"
        assert await math_ask.own_floor(db, uid, LA) == (LA, 1)
    await pass_node(uid, "ds_ngon_ngu")
    async with dbm.SessionLocal() as db:
        part = await tp.frontier(db, uid, LA)              # floor 2 is an optional node: never the frontier
        assert (part.node_id, part.floor) == ("ds_vecto_ma_tran", 3)
        user = await db.get(User, uid)
        for n in range(10):                                # questions outside a sitting: that part only
            q = await math_ask.pick_own(db, user, subject_id=LA, rng=random.Random(n))
            assert q.meta["skill"] in part.skills


async def test_with_nothing_open_the_frontier_is_the_last_passed_main_part(client):
    h, uid = await make(client)
    for n in range(1, 10):
        await old_trial(uid, LA, n)
    async with dbm.SessionLocal() as db:
        part = await tp.frontier(db, uid, LA)
    assert (part.node_id, part.floor) == ("ds_pca_svd", 9)


async def test_with_nothing_open_or_passed_the_frontier_is_the_first_main_part(client, monkeypatch):
    monkeypatch.setattr(math_tree, "tree", lambda t=tree_with(requires={"ds_ngon_ngu": ["gt_ham_so"]}): t)
    h, uid = await make(client)
    st = await state(uid)
    assert st.status["ds_ngon_ngu"] == "locked" and not [p for p in tp.all_parts(True)
                                                         if p.subject_id == LA and st.part_open(p)]
    async with dbm.SessionLocal() as db:
        part = await tp.frontier(db, uid, LA)
    assert (part.node_id, part.floor) == ("ds_ngon_ngu", 1)


# ------------------------------------------------------------------ R12: reached floors, working stage
async def test_the_reached_floors_are_those_with_an_open_or_passed_main_part(client):
    h, uid = await make(client)
    assert (await state(uid)) and tp.reached_floors_of(await state(uid), LA) == {1}     # not 2: optional only
    await pass_node(uid, "ds_ngon_ngu")
    assert tp.reached_floors_of(await state(uid), LA) == {1, 3}
    for n in range(1, 9):
        await old_trial(uid, LA, n)
    st = await state(uid)
    assert tp.reached_floors_of(st, LA) == {1, 3, 4, 5, 6, 7, 8, 9}     # 9: two of its three nodes are open
    assert [st.status[n] for n in ("ds_truc_giao_chieu", "ds_tri_rieng", "ds_pca_svd")] == ["open", "open", "locked"]


async def test_the_working_stage_is_one_above_the_stage_reached(client):
    h, uid = await make(client)
    async with dbm.SessionLocal() as db:
        assert await tp.working_stage(db, uid) == 1
    await clear_stage_one(client, h, uid)
    async with dbm.SessionLocal() as db:
        assert await tp.working_stage(db, uid) == 2
        assert await tp.working_position(db, uid) == ("luyen_khi", 2)
    view = (await client.get("/math/skills", headers=h)).json()
    assert view["open_floor"] == 2
    by = {s["id"]: s for s in view["skills"]}
    for sid, sk in math_skills.skills().items():           # a chiêu of "floor n" opens at Luyện Khí tầng n
        u = sk["unlock"]
        if u.get("nodes") or u.get("share"):                # ...and one earned on Đạo Thụ needs its nodes too
            assert not by[sid]["unlocked"], sid             # (none of them is a stage-1 node)
            assert by[sid]["locked_vi"]
        else:
            assert by[sid]["unlocked"] == (u["floor"] <= 2), sid


async def test_the_dungeon_and_the_towers_read_the_reached_floors(client):
    h, uid = await make(client)
    view = (await client.get("/math/dungeon", headers=h)).json()
    assert [f["floor"] for f in view["floors"] if f["open"]] == [1] and view["own_floor"] == 1
    r = await client.post("/math/dungeon/start", json={"floor": 2}, headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "floor_locked"        # an optional floor
    await pass_node(uid, "ds_ngon_ngu")
    view = (await client.get("/math/dungeon", headers=h)).json()
    assert [f["floor"] for f in view["floors"] if f["open"]] == [1, 3] and view["own_floor"] == 3


# ------------------------------------------------------------------ R10: programming exercises
async def test_an_exercise_is_open_when_its_micro_skills_node_is_open_or_done(client):
    h, uid = await make(client)
    by_node = {p.id: tree().node_of_skill()[p.skill] for p in pr.bank().values()}
    assert by_node["dstt_bt_tich_vo_huong"] == "ds_vecto_ma_tran" and by_node["dstt_bt_nhan_so_phuc"] == "ds_so_phuc"
    assert (await client.get("/math/problem/dstt_bt_dem_phan_tu", headers=h)).status_code == 200      # open node
    assert (await client.get("/math/problem/dstt_bt_nhan_so_phuc", headers=h)).status_code == 200     # optional, open
    r = await client.get("/math/problem/dstt_bt_tich_vo_huong", headers=h)
    assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked"
    listed = (await client.get("/math/problems", params={"subject_id": LA}, headers=h)).json()
    assert [f["floor"] for f in listed["floors"]] == [1, 2]
    await pass_node(uid, "ds_ngon_ngu")
    assert (await client.get("/math/problem/dstt_bt_tich_vo_huong", headers=h)).status_code == 200
    await pass_node(uid, "ds_vecto_ma_tran")              # done: still open
    assert (await client.get("/math/problem/dstt_bt_tich_vo_huong", headers=h)).status_code == 200
    listed = (await client.get("/math/problems", params={"subject_id": LA}, headers=h)).json()
    assert [f["floor"] for f in listed["floors"]] == [1, 2, 3, 4]       # ds_nhan_ma_tran opened with it


# ------------------------------------------------------------------ R11: the old entry points
async def test_the_old_entry_points_refuse_a_floor_whose_nodes_are_shut(client):
    h, uid = await make(client)
    for path in ("/math/run/start", "/math/trial/start"):
        r = await client.post(path, json={"subject_id": GT, "floor": 3}, headers=h)
        assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked", r.text
        assert tree().nodes["gt_ham_so"].name_vi in r.json()["error"]["message_vi"]
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 2}, headers=h)
    assert r.status_code == 200 and r.json()["run"]["node_id"] == "ds_so_phuc"     # an optional node, open
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 10}, headers=h)
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"


async def test_the_old_entry_points_resolve_to_the_open_part_first_by_stage(client):
    h, uid = await make(client)
    for n in range(1, 9):
        await old_trial(uid, LA, n)
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 9}, headers=h)
    assert r.status_code == 200 and r.json()["run"]["node_id"] == "ds_truc_giao_chieu"
    await pass_node(uid, "ds_truc_giao_chieu")
    await pass_node(uid, "ds_anh_xa_tuyen_tinh")
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 9}, headers=h)
    assert r.json()["run"]["node_id"] == "ds_tri_rieng"
    r = await client.post("/math/run/start", json={"subject_id": LA, "floor": 1}, headers=h)
    assert r.status_code == 200 and r.json()["run"]["node_id"] == "ds_ngon_ngu"     # a done part may be practised


async def test_the_node_routes_refuse_what_cannot_be_played(client):
    h, uid = await make(client)
    r = await node_start(client, h, "khong_co_nut")
    assert r.status_code == 404 and r.json()["error"]["code"] == "no_node"
    r = await node_start(client, h, "lt_python_co_ban")
    assert r.status_code == 400 and r.json()["error"]["code"] == "no_questions"
    r = await node_start(client, h, "ds_pca_svd", trial=True)
    assert r.status_code == 403 and r.json()["error"]["code"] == "node_locked"
    r = await node_start(client, h, "ds_ngon_ngu", trial=True)
    assert r.status_code == 409 and r.json()["error"]["code"] == "gate_not_met"
    r = await node_start(client, h, "ds_ngon_ngu", floor=4)
    assert r.status_code == 404
    r = await node_start(client, h, "ds_ngon_ngu")
    assert r.status_code == 200 and r.json()["run"]["node_id"] == "ds_ngon_ngu"


# ------------------------------------------------------------------ the views
async def test_the_tree_view_has_every_node_with_its_state_parts_and_reading(client):
    h, uid = await make(client)
    run = (await node_start(client, h, "gt_ham_so")).json()["run"]
    assert run["node_name_vi"] == tree().nodes["gt_ham_so"].name_vi
    view = (await client.get("/math/tree", headers=h)).json()
    assert view["wired"] is True and set(view) == {"wired", "stage", "branches", "nodes", "next", "run"}
    assert {b["id"]: b["subject"] for b in view["branches"]}["ds"] == LA
    assert len(view["nodes"]) == len(tree().nodes)
    by = {n["id"]: n for n in view["nodes"]}
    assert {n["state"] for n in view["nodes"]} == {"open", "locked", "vacant"}
    node = by["ds_vecto_ma_tran"]
    for key in ("id", "branch", "realm", "stage", "status", "kind", "name_vi", "why_vi", "state", "requires",
                "reinforces", "parts", "problems", "source"):
        assert key in node
    assert node["state"] == "locked" and node["requires"] == [
        {"id": "ds_ngon_ngu", "name_vi": tree().nodes["ds_ngon_ngu"].name_vi, "done": False}]
    part = node["parts"][0]
    assert (part["subject_id"], part["floor"], part["tier_min"], part["tier_max"]) == (LA, 3, 2, 3)
    assert part["questions"] > 0 and part["passed"] is False and part["gate"] is None     # locked: no gate
    assert part["trial_total"] == len(part["skills"]) and part["doc_id"]
    open_part = by["ds_ngon_ngu"]["parts"][0]
    assert open_part["gate"]["ok"] is False and len(open_part["gate"]["skills"]) == len(open_part["skills"])
    assert set(by["ds_ngon_ngu"]["source"]) == {"title", "author", "url", "where", "lang", "kind"}
    assert by["ds_ngon_ngu"]["source"]["url"].startswith("http")
    assert [p["id"] for p in by["lt_cau_truc_du_lieu"]["problems"]] == list(tree().nodes["lt_cau_truc_du_lieu"].problems)
    assert by["lt_cau_truc_du_lieu"]["problems"][0]["solved"] is False
    assert by["lt_cau_truc_du_lieu"]["problems"][0]["subject_id"] == LA
    assert view["next"][:5] == ["ds_ngon_ngu", "gt_ham_so", "lt_python_co_ban", "tr_logic_dem", "xs_dem_su_kien"]
    assert all(tree().nodes[n].main for n in view["next"])
    assert view["run"]["run_id"] == run["run_id"] and view["run"]["node_id"] == "gt_ham_so"


def test_a_node_without_a_reading_has_no_source(monkeypatch):
    tp._sources.cache_clear()
    monkeypatch.setattr(tp, "SOURCES_DIR", tp.SOURCES_DIR / "khong_co")
    try:
        assert tp.source(tree().nodes["ds_ngon_ngu"]) is None
    finally:
        tp._sources.cache_clear()


# ------------------------------------------------------------------ the migration
def test_migration_0016_adds_the_node_of_a_sitting(tmp_path):
    from alembic import command

    from tests.test_math_loop import _alembic
    path = tmp_path / "m16.db"
    cfg = _alembic(f"sqlite+aiosqlite:///{path}")
    command.upgrade(cfg, "0015_math_ladder")
    con = sqlite3.connect(path)
    con.execute("insert into math_runs (user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
                "combo, best_combo, asked, correct, review_asked, xp_gained, started_at) "
                "values (1, 's', 1, 'trial', 1, 0, 0, 0, 0, 0, 0, 0, 0, '2026-01-01 00:00:00')")
    con.commit()
    con.close()
    command.upgrade(cfg, "0016_math_tree")
    con = sqlite3.connect(path)
    assert con.execute("select node_id from math_runs").fetchall() == [(None,)]     # an old save: the whole floor
    assert "ix_math_runs_node" in {r[1] for r in con.execute("pragma index_list(math_runs)")}
    con.close()
    command.downgrade(cfg, "0015_math_ladder")
    con = sqlite3.connect(path)
    assert "node_id" not in {r[1] for r in con.execute("pragma table_info(math_runs)")}
    con.close()


# ------------------------------------------------------------------ a whole realm
async def test_a_player_walks_the_whole_luyen_khi_main_path_node_by_node(client):
    """From an empty save to the end of Luyện Khí: every time, the first open main-path node
    is learned - each part through its mastery gate and its Thiên kiếp nhỏ, played through the
    API; each programming exercise handed in - until no main node of the realm is left open."""
    h, uid = await make(client, "dao_thu_walk")
    t = tree()
    mains = {n.id for n in t.main_nodes("luyen_khi")}
    r = await node_start(client, h, "ds_pca_svd")
    assert r.status_code == 403                             # the end is shut at the start
    learned: list[str] = []
    stages = [(await state(uid)).stage]
    for _ in range(len(mains) + 1):
        st = await state(uid)
        todo = [n for n in st.open if n in mains]
        if not todo:
            break
        nid = todo[0]
        assert set(t.nodes[nid].requires) <= st.done
        for part in tp.parts(nid):
            if not st.has_questions(part) or st.part_passed(part):
                continue
            await meet_part_gate(uid, part)
            r = await node_start(client, h, nid, floor=part.floor, trial=True)
            assert r.status_code == 200, r.text
            played = await play_trial(client, h, r.json()["run"]["run_id"])
            assert played[-1]["res"]["math"]["trial"]["passed"] is True
            assert {p["q"]["math"]["skill"] for p in played} == set(part.skills)
        for pid in t.nodes[nid].problems:
            await solve(client, h, pid)
        st = await state(uid)
        assert st.status[nid] == "done", nid
        learned.append(nid)
        stages.append(st.stage)
    final = await state(uid)
    assert all(final.status[n] in ("done", "vacant") for n in mains)
    assert {n for n in mains if final.status[n] == "done"} == set(learned)
    assert t.reaches("luyen_khi", 9, final.stage)           # the whole realm is behind the player
    assert final.stage == ("luyen_khi", 9)                   # and not a realm that is not written yet
    assert tp.working_position_of(final) == ("luyen_khi", 9)
    assert stages == sorted(stages, key=lambda s: (t.realm_order[s[0]], s[1]))      # never backwards
    assert len(learned) >= 35


# ------------------------------------------------------------------ small trials, unwritten realms
def test_a_small_trial_allows_no_miss():
    """A part can be one or two micro-skills. The miss allowance is at most a quarter of the
    trial, so such a trial is passed only with every answer right."""
    assert [mm.trial_allowed(n) for n in (1, 2, 3, 4, 5, 6)] == [0, 0, 0, 1, 1, 1]
    assert mm.trial_verdict(asked=1, correct=0, total=1) is False
    assert mm.trial_verdict(asked=1, correct=1, total=1) is True
    assert mm.trial_verdict(asked=1, correct=0, total=2) is False
    assert mm.trial_verdict(asked=2, correct=2, total=2) is True
    assert mm.trial_verdict(asked=4, correct=3, total=4) is True        # from four questions on: one miss, as before
    assert mm.trial_verdict(asked=4, correct=2, total=4) is False


async def test_a_two_skill_part_is_failed_by_one_wrong_answer(client):
    h, uid = await make(client)
    await pass_node(uid, "gt_ham_so")
    second = tp.parts("gt_gioi_han")[1]
    assert len(second.skills) == 2
    await meet_part_gate(uid, second)
    run = (await node_start(client, h, "gt_gioi_han", floor=3, trial=True)).json()["run"]
    assert run["trial"]["total"] == 2 and run["trial"]["max_wrong"] == 0
    played = await play_trial(client, h, run["run_id"], wrong_at={1})
    assert len(played) == 1 and played[-1]["res"]["math"]["trial"]["passed"] is False
    assert not (await state(uid)).part_passed(second)
    run = (await node_start(client, h, "gt_gioi_han", floor=3, trial=True)).json()["run"]     # again, straight away
    played = await play_trial(client, h, run["run_id"])
    assert played[-1]["res"]["math"]["trial"]["passed"] is True
    assert (await state(uid)).part_passed(second)


async def test_the_stage_stops_at_the_last_realm_that_is_written(client, monkeypatch):
    """Vacant nodes count as done (R3), and today every realm after Luyện Khí is vacant: the
    position must end at Luyện Khí tầng 9, not run on to the last realm of the tree."""
    h, uid = await make(client)
    st = await state(uid)
    for node in st.tree.nodes.values():                # as if everything that can be learned were learned
        if st.status[node.id] != "vacant":
            st.status[node.id] = "done"
    assert st.stage == ("luyen_khi", 9)
    assert tp.stage_view(st) == {"realm": "luyen_khi", "realm_name_vi": "Luyện Khí", "stage": 9, "stages": 9,
                                 "progress": None}      # no next stage to work on
    assert tp.working_position_of(st) == ("luyen_khi", 9)
    fresh = await state(uid)
    assert fresh.stage == ("luyen_khi", 0)             # a newcomer is still a newcomer
