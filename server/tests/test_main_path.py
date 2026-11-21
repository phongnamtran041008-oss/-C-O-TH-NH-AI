"""Chính đạo, the main quest: one total order over the main-path nodes of Đạo Thụ
(tree.json `main_path`, learning/math_tree.py) and the ONE next step it gives a player
(systems/math_tree_progress.next_step), in GET /math/tree `main` and GET /guide `main`.
"""
import copy
import json

import pytest

from app import db as dbm
from app.learning import math_tree as mt
from app.models import User
from app.systems import guide
from app.systems import math_tree_progress as tp
from tests.test_math_loop import log_answers, make
from tests.test_math_tree_progress import meet_part_gate, pass_node, pass_part, solve_node, old_trial

LA = "dai_so_tuyen_tinh"
STAGE_1 = ["ds_ngon_ngu", "tr_logic_dem", "lt_python_co_ban", "gt_ham_so", "xs_dem_su_kien"]


def tree():
    return mt.tree()


@pytest.fixture
def raw():
    return copy.deepcopy(json.loads((mt.MATH_DIR / mt.TREE_FILE).read_text("utf-8")))


def check(raw):
    return mt.validate_tree(raw, mt.subject_skills(), mt.problem_ids())


# ------------------------------------------------------------------ the order
def test_every_main_node_is_on_the_path_exactly_once():
    t = tree()
    path = t.main_path()
    assert len(path) == len(set(path)) == len(t.main_nodes())
    assert set(path) == {n.id for n in t.main_nodes()}


def test_no_node_comes_before_one_it_requires():
    t = tree()
    rank = t.path_rank
    for nid in t.main_path():
        for r in t.nodes[nid].requires:
            assert rank[r] < rank[nid], f"{nid} comes before {r}"


def test_the_path_runs_realm_by_realm_and_stage_by_stage():
    t = tree()
    keys = [(t.realm_order[t.nodes[n].realm], t.nodes[n].stage) for n in t.main_path()]
    assert keys == sorted(keys)


def test_the_path_is_the_order_the_data_gives_and_is_stable():
    t = tree()
    listed = [nid for realm in sorted(t.realm_order, key=t.realm_order.get)
              for row in t.raw["main_path"][realm] for nid in row]
    assert t.main_path() == listed
    assert mt.build(copy.deepcopy(t.raw)).main_path() == listed      # same data, same order
    assert t.main_path()[:5] == STAGE_1


def test_code_comes_right_after_the_maths_it_uses():
    path = tree().main_path()
    for code, maths in (("lt_vecto_bang_code", "ds_nhan_ma_tran"), ("ud_knn", "lt_vecto_bang_code"),
                        ("lt_ma_tran_gauss", "ds_he_gauss"), ("lt_mo_phong_xac_suat", "xs_bayes"),
                        ("lt_dao_ham_so", "gt_cuc_tri"), ("ud_binh_phuong_toi_thieu", "ds_truc_giao_chieu"),
                        ("ud_mang_no_ron", "tr_gradient_descent"), ("ud_pca", "ds_pca_svd"),
                        ("ud_ab_test", "xs_kiem_dinh")):
        assert path.index(code) == path.index(maths) + 1, (code, maths)


def test_inside_a_stage_a_subject_keeps_its_own_floor_order():
    """Two nodes of one subject in one stage come in the order of their floors, so the player's own
    floor of a subject (the frontier, R9) is the lower one, as the subject files and the placement
    test read it."""
    t, path = tree(), tree().main_path()
    for i, a in enumerate(path):
        for b in path[i + 1:]:
            pa, pb = tp.parts(a), tp.parts(b)
            if pa and pb and pa[0].subject_id == pb[0].subject_id and t.nodes[a].stage == t.nodes[b].stage \
                    and t.nodes[a].realm == t.nodes[b].realm:
                assert pa[0].floor <= pb[0].floor, (a, b)


def test_the_shipped_path_is_sound_and_required():
    assert mt.validate_all() == []


def test_a_node_before_its_requirement_is_caught(raw):
    row = raw["main_path"]["luyen_khi"][2]
    row.remove("ud_knn")
    row.insert(0, "ud_knn")                  # before lt_vecto_bang_code, which it requires
    assert any("ud_knn comes before lt_vecto_bang_code" in e for e in check(raw))
    t = mt.build(raw)                        # the game still never leads there first
    assert t.path_rank["lt_vecto_bang_code"] < t.path_rank["ud_knn"]


def test_a_missing_doubled_or_misplaced_node_is_caught(raw):
    raw["main_path"]["luyen_khi"][0].remove("gt_ham_so")
    errs = check(raw)
    assert any("gt_ham_so has no place" in e for e in errs)
    raw["main_path"]["luyen_khi"][1].append("gt_ham_so")
    raw["main_path"]["luyen_khi"][1].append("ds_vecto_ma_tran")
    errs = check(raw)
    assert any("gt_ham_so belongs to luyen_khi stage 1" in e for e in errs)
    assert any("ds_vecto_ma_tran is listed more than once" in e for e in errs)


def test_unknown_or_optional_nodes_and_bad_shapes_are_caught(raw):
    opt = next(n["id"] for n in raw["nodes"] if n["status"] == "phu")
    raw["main_path"]["luyen_khi"][0] += ["khong_co", opt]
    raw["main_path"]["xa_xoi"] = [[]]
    raw["main_path"]["truc_co"] = [["tc_du_lieu"]]
    errs = check(raw)
    assert any("unknown node 'khong_co'" in e for e in errs)
    assert any(f"{opt} is optional" in e for e in errs)
    assert any("unknown realm 'xa_xoi'" in e for e in errs)
    assert any("main_path.truc_co: needs one list of node ids per stage (3)" in e for e in errs)


def test_without_a_list_the_order_still_respects_requires(raw):
    del raw["main_path"]
    assert check(raw) == []                  # a test tree may leave it out ...
    t = mt.build(raw)
    for nid in t.main_path():
        for r in t.nodes[nid].requires:
            assert t.path_rank[r] < t.path_rank[nid]


def test_the_shipped_tree_must_carry_the_path(monkeypatch, raw):
    del raw["main_path"]                     # ... the shipped one may not
    real = mt._read
    monkeypatch.setattr(mt, "_read", lambda name, d: copy.deepcopy(raw) if name == mt.TREE_FILE else real(name, d))
    assert any("main_path is missing" in e for e in mt.validate_all())


def test_open_nodes_and_tree_order_follow_the_path():
    t = tree()
    assert t.open_nodes([])[:5] == STAGE_1
    assert sorted(t.nodes.values(), key=tp.node_order)[0].id == "ds_ngon_ngu"


# ------------------------------------------------------------------ the next step
async def main(client, h) -> dict:
    r = await client.get("/math/tree", headers=h)
    assert r.status_code == 200, r.text
    return r.json()["main"]


async def read(client, h, node_id, floor):
    return await client.post("/guide/read", json={"node_id": node_id, "floor": floor}, headers=h)


async def test_a_newcomer_is_told_to_read_the_first_lesson(client):
    h, uid = await make(client, "cd_new")
    m = await main(client, h)
    assert (m["node_id"], m["step"], m["stage"], m["index"], m["total"]) == ("ds_ngon_ngu", "hoc", 1, 1, 5)
    assert m["name_vi"] == tree().nodes["ds_ngon_ngu"].name_vi and m["why_vi"]
    assert m["done"] == {"hieu": False, "luyen": False, "kiep": False}
    assert m["doc_id"] and isinstance(m["block"], int)
    assert (m["subject_id"], m["floor"]) == (LA, 1) and m["part"]["index"] == 1
    assert m["gate"]["done"] == 0 and m["gate"]["total"] == len(tp.parts("ds_ngon_ngu")[0].skills)
    assert [s["id"] for s in m["stage_nodes"]] == STAGE_1
    assert [s["state"] for s in m["stage_nodes"]] == ["now", "later", "later", "later", "later"]
    assert m["path_done"] == 0 and m["path_total"] == len(tp.path_nodes(await tp_state(uid), "luyen_khi"))
    assert m["resume"] is None


async def tp_state(uid):
    async with dbm.SessionLocal() as db:
        return await tp.state(db, uid)


async def test_the_life_of_a_node_hoc_luyen_kiep_then_the_next_node(client):
    h, uid = await make(client, "cd_life")
    part = tp.parts("ds_ngon_ngu")[0]
    r = await read(client, h, "ds_ngon_ngu", part.floor)
    assert r.status_code == 200 and r.json()["read"] == "ds_ngon_ngu:1"
    assert r.json()["main"]["step"] == "luyen" and r.json()["guide"]["main"]["step"] == "luyen"
    assert (await read(client, h, "ds_ngon_ngu", part.floor)).status_code == 200      # idempotent
    async with dbm.SessionLocal() as db:
        flags = (await db.get(User, uid)).flags
    assert flags["path"]["read"] == ["ds_ngon_ngu:1"]
    m = await main(client, h)
    assert m["step"] == "luyen" and m["done"] == {"hieu": True, "luyen": False, "kiep": False}

    half = tp.Part(part.node_id, part.subject_id, part.floor, part.skills[: len(part.skills) // 2])
    await meet_part_gate(uid, half)                                         # the gate half open
    m = await main(client, h)
    assert m["step"] == "luyen" and m["gate"]["done"] == len(half.skills) and not m["gate"]["ok"]

    await meet_part_gate(uid, part)                                         # the gate open
    m = await main(client, h)
    assert m["step"] == "kiep" and m["gate"]["ok"] and m["done"] == {"hieu": True, "luyen": True, "kiep": False}

    await pass_part(uid, "ds_ngon_ngu")                                     # the trial passed
    m = await main(client, h)
    assert (m["node_id"], m["step"], m["index"]) == ("tr_logic_dem", "hoc", 2)
    assert [s["state"] for s in m["stage_nodes"]][:2] == ["done", "now"]
    assert m["path_done"] == 1


async def test_a_code_node_asks_for_its_exercises(client):
    h, uid = await make(client, "cd_code")
    await pass_node(uid, "ds_ngon_ngu")
    await pass_node(uid, "tr_logic_dem")
    m = await main(client, h)
    node = tree().nodes["lt_python_co_ban"]
    assert (m["node_id"], m["step"], m["index"]) == ("lt_python_co_ban", "code", 3)
    assert [p["id"] for p in m["problems"]] == list(node.problems)
    assert m["problems_done"] == 0 and m["problems_total"] == len(node.problems)
    assert m["part"] is None and m["floor"] is not None and m["subject_id"]
    await solve_node(client, h, "lt_python_co_ban")
    m = await main(client, h)
    assert (m["node_id"], m["step"]) == ("gt_ham_so", "hoc")


async def test_finishing_a_stage_moves_to_the_first_node_of_the_next(client):
    h, uid = await make(client, "cd_stage")
    for nid in STAGE_1:
        if tree().nodes[nid].problems:
            await solve_node(client, h, nid)
        else:
            await pass_node(uid, nid)
    m = await main(client, h)
    assert (m["node_id"], m["stage"], m["index"], m["total"]) == ("ds_vecto_ma_tran", 2, 1, 5)
    assert all(s["state"] != "done" for s in m["stage_nodes"])


async def test_a_node_done_ahead_of_the_path_shows_as_done_and_is_skipped(client):
    h, uid = await make(client, "cd_ahead")
    await pass_node(uid, "gt_ham_so")                       # learned out of order
    m = await main(client, h)
    assert m["node_id"] == "ds_ngon_ngu"
    assert {s["id"]: s["state"] for s in m["stage_nodes"]}["gt_ham_so"] == "done"


async def test_everything_finished_says_done(client):
    h, uid = await make(client, "cd_done")
    st = await tp_state(uid)
    st.status = {n: tp.DONE for n in st.status}
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        m = await tp.next_step(db, user, st)
    assert m["step"] == "done" and m["node_id"] is None and m["stage_nodes"] == []
    assert m["path_done"] == m["path_total"] > 0


async def test_an_old_save_with_answers_is_never_sent_back_to_read(client):
    h, uid = await make(client, "cd_old")
    part = tp.parts("ds_ngon_ngu")[0]
    await log_answers(uid, part.skills[0], 1, [True, False], floor=part.floor)
    m = await main(client, h)
    assert (m["node_id"], m["step"]) == ("ds_ngon_ngu", "luyen") and m["done"]["hieu"] is True


async def test_an_old_save_with_whole_floor_trials_lands_further_on(client):
    h, uid = await make(client, "cd_legacy")
    await old_trial(uid, LA, 1)                            # an old trial with no node: ds floor 1 passed
    m = await main(client, h)
    assert m["node_id"] == "tr_logic_dem"
    assert {s["id"]: s["state"] for s in m["stage_nodes"]}["ds_ngon_ngu"] == "done"


async def test_a_sitting_left_open_on_the_step_is_resumed(client):
    h, uid = await make(client, "cd_resume")
    r = await client.post("/math/node/start", json={"node_id": "ds_ngon_ngu"}, headers=h)
    assert r.status_code == 200
    m = await main(client, h)
    assert m["resume"] == "practice"
    r = await client.post("/math/node/start", json={"node_id": "gt_ham_so"}, headers=h)
    m = await main(client, h)
    assert m["resume"] is None                             # the open sitting is elsewhere


async def test_reading_a_part_that_does_not_exist_is_refused(client):
    h, uid = await make(client, "cd_bad")
    assert (await read(client, h, "khong_co", 1)).status_code == 404
    assert (await read(client, h, "ds_ngon_ngu", 9)).status_code == 404
    assert (await client.post("/guide/read", json={"node_id": "ds_ngon_ngu", "floor": 1})).status_code == 401


async def test_read_keeps_the_other_flags(client):
    h, uid = await make(client, "cd_flags")
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.flags = {**(u.flags or {}), "guide": {"claimed": ["g_welcome"], "seen": ["welcome"]}, "x": 1}
        await db.commit()
    assert (await read(client, h, "ds_ngon_ngu", 1)).status_code == 200
    async with dbm.SessionLocal() as db:
        flags = (await db.get(User, uid)).flags
    assert flags["x"] == 1 and flags["guide"]["claimed"] == ["g_welcome"] and flags["path"]["read"] == ["ds_ngon_ngu:1"]


# ------------------------------------------------------------------ the guide leads with it
async def test_the_guide_leads_with_the_main_step_once_the_welcome_is_done(client):
    h, uid = await make(client, "cd_guide")
    v = (await client.get("/guide", headers=h)).json()
    assert v["lead"] == "steps" and v["main"]["node_id"] == "ds_ngon_ngu"
    for key in ("welcome", "board"):
        assert (await client.post("/guide/seen", json={"key": key}, headers=h)).status_code == 200
    v = (await client.get("/guide", headers=h)).json()
    assert v["lead"] == "main" and v["main"]["step"] == "hoc"


OLD_STEP_IDS = {"c1_nhap_mon", "g_welcome", "g_board", "g_open_tree", "g_read_doc", "g_placement", "g_first_run",
                "g_right_5", "g_first_trial", "g_first_node", "c2_bon_nhanh", "g_node_ds", "g_node_gt", "g_node_xs",
                "g_node_tr", "g_tam_ma", "g_answers_50", "g_trials_4", "c3_thuc_chien", "g_village", "g_dungeon",
                "g_td", "g_skill", "g_fortune", "g_code", "g_linh_can", "c4_luyen_khi"}


def test_every_old_step_id_is_kept():
    ids = {c["id"] for c in guide.chapters()} | {s["id"] for c in guide.chapters() for s in c["steps"]}
    assert OLD_STEP_IDS <= ids


def test_required_steps_follow_the_path():
    """A required step that names a node names them in path order, and no required step sends the
    player to a side mode (Hầm Ngục, Thủ Thành, Cơ Duyên)."""
    rank = tree().path_rank
    named = [s["check"]["node"] for c in guide.chapters() for s in c["steps"]
             if not s["optional"] and s["check"]["type"] == "node_done"]
    assert named and named == sorted(named, key=rank.get)
    side = ("dungeon_cleared", "td_wins", "fortune_won")
    for c in guide.chapters():
        for s in c["steps"]:
            if s["check"]["type"] in side or s.get("goto") in ("dungeon", "td", "fortune"):
                assert s["optional"], s["id"]
            if s["check"]["type"] == "nodes_done" and s["check"].get("branch"):
                assert s["optional"], s["id"]
