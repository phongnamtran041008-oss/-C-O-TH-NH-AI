"""Lộ Trình Tu Tiên (systems/guide.py, routers/guide_routes.py): the data check, every check
type read from the database, step and chapter states, rewards paid once, the generated
Đạo Thụ chapter, `study`, `seen` and the routes.

Every test of the board runs on a small inline guide (BOARD) instead of server/data/guide.json,
whose content is written separately; the real file is only required to validate clean.
"""
import asyncio
import copy
import datetime as dt

import pytest
from sqlalchemy import func, select

from app import db as dbm
from app.learning import math_tree
from app.models import (AuditLog, Character, MathDungeonRun, MathRetry, MathRun, MathSubmission, TdProgress,
                        User)
from app.systems import catalog, guide, math_skills, math_td
from app.systems import math_tree_progress as tp
from tests.test_math_loop import make, play
from tests.test_math_tree_progress import meet_part_gate, pass_node, solve

MATERIAL = next(k for k, v in catalog.math_drops().items() if v.get("kind") == "material")


def step(sid, check, rewards, optional=False, **more):
    return {"id": sid, "title_vi": "Bước thử", "desc_vi": "Làm một việc nhỏ.", "how_vi": ["Bấm phím M.", "Rồi bấm Luyện."],
            "check": check, "goto": "math", "help": "h_cay", "optional": optional, "rewards": rewards, **more}


BOARD = {
    "version": 1,
    "title_vi": "Lộ Trình Thử",
    "welcome": {"speaker_vi": "Trúc Lão", "lines_vi": ["Con tới rồi.", "Đường tu ở đây đi bằng toán.", "Bấm F1."]},
    "chapters": [
        {"id": "c1", "title_vi": "Nhập Môn", "intro_vi": "Những bước đầu tiên.", "rewards": {"spirit_stones": 100},
         "steps": [
             step("s_opt", {"type": "seen", "key": "village"}, {"spirit_stones": 1}, optional=True),
             step("s_hub", {"type": "seen", "key": "math_hub"}, {"spirit_stones": 20, "xp": 10}),
             step("s_right", {"type": "math_answers", "count": 2, "correct": True},
                  {"immortal_jade": 5, "items": [{"item": MATERIAL, "qty": 2}]}),
         ]},
        {"id": "c2", "title_vi": "Không Thưởng", "intro_vi": "Chương không có thưởng riêng.",
         "steps": [
             step("s_runs", {"type": "practice_runs", "count": 1}, {"spirit_stones": 5}),
             step("s_trial", {"type": "trials_passed", "count": 1}, {"spirit_stones": 5}),
             step("s_nodes", {"type": "nodes_done", "count": 1}, {"spirit_stones": 5}),
         ]},
        {"id": "c3", "title_vi": "Đường Luyện Khí", "intro_vi": "Chín tầng.", "generated": "tree_stages",
         "realm": "luyen_khi",
         "step": {"title_vi": "Luyện Khí tầng {stage}", "desc_vi": "Xong tầng {stage}.",
                  "how_vi": ["Học các nút tầng {stage}."], "goto": "math", "help": "h_cay"},
         "stage_rewards": [{"spirit_stones": 10 * k} for k in range(1, 10)]},
    ],
    "handbook": [{"id": "h_cay", "title_vi": "Đạo Thụ là gì", "lines_vi": ["Đạo Thụ là cây giáo trình."]}],
}


@pytest.fixture
def board(monkeypatch):
    monkeypatch.setattr(guide, "data", lambda: BOARD)
    return BOARD


async def get(client, h) -> dict:
    r = await client.get("/guide", headers=h)
    assert r.status_code == 200, r.text
    return r.json()


def find(view, sid) -> dict:
    for ch in view["chapters"]:
        if ch["id"] == sid:
            return ch
        for s in ch["steps"]:
            if s["id"] == sid:
                return s
    raise KeyError(sid)


async def seen(client, h, key):
    return await client.post("/guide/seen", json={"key": key}, headers=h)


async def claim(client, h, sid):
    return await client.post("/guide/claim", json={"id": sid}, headers=h)


async def wallet(uid) -> tuple[int, int, int]:
    async with dbm.SessionLocal() as db:
        u, ch = await db.get(User, uid), await db.get(Character, uid)
        return u.spirit_stones, u.immortal_jade, ch.cultivation_xp


async def facts(uid) -> guide.Facts:
    db = dbm.SessionLocal()
    u = await db.get(User, uid)
    return guide.Facts(db, uid, await tp.state(db, uid), u.flags)


# ------------------------------------------------------------------ the data
def test_the_real_guide_file_is_sound():
    assert guide.validate() == []


def test_a_sound_inline_guide_has_no_problem():
    assert guide.validate(BOARD) == []


@pytest.mark.parametrize("change, expect", [
    (lambda b: b["chapters"][0]["steps"][1].update(check={"type": "flying", "count": 1}), "check type must be one of"),
    (lambda b: b["chapters"][0]["steps"][1].update(goto="garden"), "goto 'garden'"),
    (lambda b: b["chapters"][0]["steps"][1].update(help="nowhere"), "help 'nowhere'"),
    (lambda b: b["chapters"][0]["steps"][1]["check"].update(key="bees"), "seen key 'bees'"),
    (lambda b: b["chapters"][0]["steps"][1].update(id="c2"), "duplicate id 'c2'"),
    (lambda b: b["chapters"][0]["steps"][1].update(id="c3_s4"), "duplicate id 'c3_s4'"),
    (lambda b: b["chapters"][0]["steps"][1].update(id="Bad-Id"), "must be [a-z0-9_]"),
    (lambda b: b["chapters"][0]["steps"][2]["rewards"]["items"][0].update(item="no_such_thing"), "existing stackable"),
    (lambda b: b["chapters"][0]["steps"][1]["rewards"].update(equipment=[{"item": "x"}]), "unknown reward"),
    (lambda b: b["chapters"][0]["steps"][1].update(rewards={}), "rewards must be a non-empty object"),
    (lambda b: b["chapters"][2]["stage_rewards"].pop(), "one reward per stage of luyen_khi (9)"),
    (lambda b: b["chapters"][2].update(realm="tien_gioi"), "not a realm of Đạo Thụ"),
    (lambda b: b["chapters"][0].update(title_vi="Một tiêu đề dài quá mức cho phép"), "at most 24"),
    (lambda b: b["chapters"][0]["steps"][1].update(how_vi=["a", "b", "c", "d"]), "list of 1-3 lines"),
    (lambda b: b["chapters"][0]["steps"][1].update(how_vi=["x" * 91]), "at most 90"),
    (lambda b: b["chapters"][2]["step"].update(title_vi="Tầng {stage} của con đường rất rất dài"), "at most 28"),
    (lambda b: b["chapters"][0]["steps"][1].update(desc_vi="Học chữ 学 nhé."), "Hanzi"),
    (lambda b: b["welcome"].update(lines_vi=["Một.", "Hai."]), "list of 3-6 lines"),
    (lambda b: b["handbook"][0].update(lines_vi=["dòng"] * 13), "list of 1-12 lines"),
    (lambda b: b["chapters"][0]["steps"][2]["check"].update(count=0), "count must be a whole number >= 1"),
    (lambda b: b["chapters"][0]["steps"][2]["check"].update(colour="red"), "does not take 'colour'"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "node_done"}), "needs 'node'"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "node_done", "node": "x"}), "not a node"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "nodes_done", "count": 1, "branch": "zz"}),
     "not a branch"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "tree_stage", "realm": "luyen_khi", "stage": 10}),
     "stage must be 1..9"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "fortune_won", "count": 2}), "count must be 1"),
    (lambda b: b["chapters"][1]["steps"][0].update(check={"type": "realm", "target": "tien_de"}),
     "not a cultivation realm"),
    (lambda b: b["chapters"][1]["steps"][0].update(colour="red"), "unknown key 'colour'"),
])
def test_bad_data_is_reported(change, expect):
    bad = copy.deepcopy(BOARD)
    change(bad)
    problems = guide.validate(bad)
    assert any(expect in p for p in problems), problems


# ------------------------------------------------------------------ the routes
async def test_the_guide_needs_a_login(client, board):
    assert (await client.get("/guide")).status_code == 401
    assert (await client.post("/guide/claim", json={"id": "s_hub"})).status_code == 401
    assert (await client.post("/guide/seen", json={"key": "welcome"})).status_code == 401


async def test_a_fresh_account_sees_the_whole_road(client, board):
    h, uid = await make(client, "guide_new")
    v = await get(client, h)
    assert v["title_vi"] == "Lộ Trình Thử"
    assert v["welcome"] == {"seen": False, "speaker_vi": "Trúc Lão", "lines_vi": BOARD["welcome"]["lines_vi"]}
    assert [c["id"] for c in v["chapters"]] == ["c1", "c2", "c3"]
    c1 = v["chapters"][0]
    assert (c1["done"], c1["total"], c1["state"], c1["rewards_vi"]) == (0, 2, "active", ["100 Linh Thạch"])
    hub = find(v, "s_hub")
    assert hub == {"id": "s_hub", "chapter_id": "c1", "title_vi": "Bước thử", "desc_vi": "Làm một việc nhỏ.",
                   "how_vi": ["Bấm phím M.", "Rồi bấm Luyện."], "goto": "math", "help": "h_cay", "optional": False,
                   "state": "active", "progress": 0, "count": 1, "rewards_vi": ["20 Linh Thạch", "10 Tu Vi"],
                   "nodes": []}
    assert find(v, "s_right")["rewards_vi"] == ["5 Tiên Ngọc", f"{catalog.item_name(MATERIAL)} ×2"]
    # the optional first step does not hold the tracker
    assert v["current"] == {"chapter_id": "c1", "step_id": "s_hub", "title_vi": "Bước thử", "hint_vi": "Bấm phím M.",
                            "progress": 0, "count": 1, "goto": "math"}
    assert v["claimable"] == 0
    assert v["stage"] == {"realm": "luyen_khi", "realm_name_vi": "Luyện Khí", "stage": 0, "stages": 9}
    assert v["handbook"] == BOARD["handbook"]
    st = v["study"]
    first = next(n for n in math_tree.tree().nodes.values() if n.id == st["node_id"])
    assert st["action"] == "practice" and first.main and first.stage == 1
    assert st["name_vi"] == first.name_vi and st["floor"] == tp.parts(first)[0].floor
    assert st["text_vi"] == f"Học nút «{first.name_vi}»: luyện cho tới khi mở Thiên kiếp nhỏ"
    assert st["branch_vi"]


async def test_seen_marks_a_step_done_and_refuses_unknown_keys(client, board):
    h, uid = await make(client, "guide_seen")
    r = await seen(client, h, "math_hub")
    assert r.status_code == 200, r.text
    v = r.json()["guide"]
    assert find(v, "s_hub")["state"] == "done" and find(v, "s_hub")["progress"] == 1
    assert v["claimable"] == 1
    assert v["current"]["step_id"] == "s_right"
    assert (await seen(client, h, "math_hub")).status_code == 200          # idempotent
    async with dbm.SessionLocal() as db:
        assert (await db.get(User, uid)).flags["guide"] == {"claimed": [], "seen": ["math_hub"]}
    for key in ("welcome", "board"):                                        # always accepted
        assert (await seen(client, h, key)).status_code == 200
    assert (await get(client, h))["welcome"]["seen"] is True
    for key in ("nonsense", "library_doc"):                                 # library_doc: no seen check uses it here
        r = await seen(client, h, key)
        assert r.status_code == 400 and r.json()["error"]["code"] == "bad_key", r.text


# ------------------------------------------------------------------ claiming
async def test_a_step_goes_active_done_claimed_and_pays_once(client, board):
    h, uid = await make(client, "guide_pay")
    assert (await claim(client, h, "s_hub")).json()["error"]["code"] == "not_done"
    assert (await claim(client, h, "nope")).status_code == 404
    assert (await claim(client, h, "nope")).json()["error"]["code"] == "no_step"
    await seen(client, h, "math_hub")
    stones, jade, xp = await wallet(uid)
    r = await claim(client, h, "s_hub")
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["claimed"] == "s_hub"
    assert out["rewards"]["spirit_stones"] == stones + 20 and out["rewards"]["xp"]["gained"] == 10
    assert find(out["guide"], "s_hub")["state"] == "claimed" and out["guide"]["claimable"] == 0
    after = await wallet(uid)
    assert after[0] == stones + 20 and after[1] == jade
    r = await claim(client, h, "s_hub")
    assert r.status_code == 400 and r.json()["error"]["code"] == "already_claimed"
    assert (await wallet(uid)) == after
    async with dbm.SessionLocal() as db:
        rows = (await db.execute(select(AuditLog).where(AuditLog.user_id == uid, AuditLog.reason == "guide"))
                ).scalars().all()
        assert sorted((r.currency_or_item, r.delta, r.ref_id) for r in rows) == [
            ("guide", 0, "s_hub"), ("spirit_stones", 20, "s_hub")]


async def test_two_claims_at_once_pay_once(client, board):
    h, uid = await make(client, "guide_race")
    await seen(client, h, "math_hub")
    stones = (await wallet(uid))[0]
    a, b = await asyncio.gather(claim(client, h, "s_hub"), claim(client, h, "s_hub"))
    assert sorted([a.status_code, b.status_code]) == [200, 400], (a.text, b.text)
    assert (await wallet(uid))[0] == stones + 20


async def test_a_lost_flag_cannot_pay_a_step_twice(client, board):
    """Another system writing a stale copy of users.flags could drop the guide's record; the
    ledger marker still refuses the second payment."""
    h, uid = await make(client, "guide_lost")
    await seen(client, h, "math_hub")
    assert (await claim(client, h, "s_hub")).status_code == 200
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.flags = {**u.flags, "guide": {"claimed": [], "seen": ["math_hub"]}}
        await db.commit()
    stones = (await wallet(uid))[0]
    r = await claim(client, h, "s_hub")
    assert r.status_code == 400 and r.json()["error"]["code"] == "already_claimed"
    assert (await wallet(uid))[0] == stones


async def test_math_answers_and_sittings_and_the_chapter_bonus(client, board):
    h, uid = await make(client, "guide_math")
    v = await get(client, h)
    node = v["study"]["node_id"]
    r = await client.post("/math/node/start", json={"node_id": node}, headers=h)
    assert r.status_code == 200, r.text
    run_id = r.json()["run"]["run_id"]
    v = await get(client, h)
    assert v["study"]["action"] == "resume" and v["study"]["node_id"] == node
    assert v["study"]["text_vi"].startswith("Buổi luyện ở nút «")
    assert find(v, "s_runs")["state"] == "active"                       # no answer yet
    await play(client, h, run_id, correct=False)
    v = await get(client, h)
    assert find(v, "s_right")["progress"] == 0 and find(v, "s_runs")["state"] == "done"
    await play(client, h, run_id)
    await play(client, h, run_id)
    v = await get(client, h)
    assert find(v, "s_right")["state"] == "done" and find(v, "s_right")["progress"] == 2
    assert find(v, "c1")["state"] == "active" and find(v, "c1")["done"] == 1       # s_hub still missing
    assert (await claim(client, h, "c1")).json()["error"]["code"] == "not_done"
    await seen(client, h, "math_hub")
    v = await get(client, h)
    c1 = find(v, "c1")
    assert (c1["state"], c1["done"], c1["total"]) == ("done", 2, 2)       # s_opt (optional) is not needed
    assert find(v, "s_opt")["state"] == "active"
    assert v["claimable"] == 4                                            # s_hub, s_right, s_runs, c1
    stones, jade, _ = await wallet(uid)
    out = (await claim(client, h, "c1")).json()
    assert out["rewards"]["spirit_stones"] == stones + 100 and find(out["guide"], "c1")["state"] == "claimed"
    out = (await claim(client, h, "s_right")).json()
    assert out["rewards"]["immortal_jade"] == jade + 5
    assert out["rewards"]["items"][0]["item"] == MATERIAL and out["rewards"]["items"][0]["qty"] == 2
    assert (await claim(client, h, "c1")).json()["error"]["code"] == "already_claimed"


async def test_a_chapter_without_a_bonus_goes_straight_to_claimed(client, board):
    h, uid = await make(client, "guide_c2")
    first = (await get(client, h))["study"]["node_id"]
    async with dbm.SessionLocal() as db:
        db.add(MathRun(user_id=uid, subject_id=tp.parts(first)[0].subject_id, node_id=first,
                       floor=tp.parts(first)[0].floor, mode="practice", tier=1, asked=3, correct=2,
                       started_at=dt.datetime(2026, 1, 1), ended_at=dt.datetime(2026, 1, 1)))
        await db.commit()
    await pass_node(uid, first)
    v = await get(client, h)
    for sid in ("s_runs", "s_trial", "s_nodes"):
        assert find(v, sid)["state"] == "done", sid
    c2 = find(v, "c2")
    assert (c2["state"], c2["done"], c2["total"], c2["rewards_vi"]) == ("claimed", 3, 3, [])
    assert (await claim(client, h, "c2")).json()["error"]["code"] == "already_claimed"


# ------------------------------------------------------------------ the generated Đạo Thụ chapter
async def test_the_tree_chapter_has_one_step_per_stage_with_cumulative_progress(client, board):
    h, uid = await make(client, "guide_tree")
    t = math_tree.tree()
    v = await get(client, h)
    c3 = find(v, "c3")
    assert [s["id"] for s in c3["steps"]] == [f"c3_s{k}" for k in range(1, 10)]
    s1, s2 = c3["steps"][0], c3["steps"][1]
    assert (s1["title_vi"], s1["desc_vi"], s1["how_vi"]) == ("Luyện Khí tầng 1", "Xong tầng 1.", ["Học các nút tầng 1."])
    assert s1["rewards_vi"] == ["10 Linh Thạch"] and c3["steps"][8]["rewards_vi"] == ["90 Linh Thạch"]
    stage1 = sorted((n for n in t.main_nodes("luyen_khi") if n.stage == 1), key=tp.node_order)
    assert [n["id"] for n in s1["nodes"]] == [n.id for n in stage1]
    assert set(s1["nodes"][0]) == {"id", "name_vi", "branch", "branch_vi", "state"}
    async with dbm.SessionLocal() as db:
        st = await tp.state(db, uid)
    vacant = st.vacant
    want1 = [n for n in stage1 if n.id not in vacant]
    want2 = [n for n in t.main_nodes("luyen_khi") if (n.stage or 0) <= 2 and n.id not in vacant]
    assert (s1["progress"], s1["count"], s1["state"]) == (0, len(want1), "active")
    assert s2["count"] == len(want2)
    assert {n["state"] for n in s1["nodes"] if n["id"] in vacant} <= {"vacant"}
    await pass_node(uid, want1[0].id)
    s1 = find(await get(client, h), "c3_s1")
    assert s1["progress"] == 1 and s1["state"] == "active"
    for n in want1[1:]:
        if tp.parts(n):
            await pass_node(uid, n.id)
        for pid in n.problems:
            if tp.problem_available(pid):
                await solve(client, h, pid)
    v = await get(client, h)
    s1, s2 = find(v, "c3_s1"), find(v, "c3_s2")
    assert v["stage"]["stage"] == 1
    assert (s1["progress"], s1["count"], s1["state"]) == (len(want1), len(want1), "done")
    assert s2["state"] == "active" and s2["progress"] == len(want1)          # cumulative: stage 1 counts toward 2
    assert all(n["state"] == "done" for n in s1["nodes"] if n["id"] not in vacant)
    stones = (await wallet(uid))[0]
    out = (await claim(client, h, "c3_s1")).json()
    assert out["rewards"]["spirit_stones"] == stones + 10
    assert (await claim(client, h, "c3_s2")).json()["error"]["code"] == "not_done"


async def test_study_turns_to_the_trial_once_the_gate_is_open(client, board):
    h, uid = await make(client, "guide_gate")
    study = (await get(client, h))["study"]
    part = next(p for p in tp.parts(study["node_id"]) if p.floor == study["floor"])
    await meet_part_gate(uid, part)
    study = (await get(client, h))["study"]
    assert study["action"] == "trial" and study["floor"] == part.floor
    assert "Thiên kiếp nhỏ" in study["text_vi"]


# ------------------------------------------------------------------ every check type, read from the database
async def test_each_counting_check_reads_its_own_rows(client, board):
    h, uid = await make(client, "guide_rows")
    now = dt.datetime(2026, 1, 1)
    level = next(iter(math_td.levels()))
    async with dbm.SessionLocal() as db:
        db.add_all([
            MathRun(user_id=uid, subject_id="dai_so_tuyen_tinh", floor=1, mode="placement", tier=1, passed=True,
                    started_at=now, ended_at=now),
            MathRun(user_id=uid, subject_id="giai_tich", floor=1, mode="placement", tier=1, passed=False,
                    started_at=now, ended_at=now),                              # abandoned: not counted
            MathRetry(user_id=uid, subject_id="dai_so_tuyen_tinh", floor=1, skill_id="x", tier=1, item_id="i",
                      fingerprint="f", after_answer_id=1, created_at=now, cleared_at=now),
            MathRetry(user_id=uid, subject_id="dai_so_tuyen_tinh", floor=1, skill_id="y", tier=1, item_id="i",
                      fingerprint="g", after_answer_id=1, created_at=now),     # not beaten yet
            MathDungeonRun(user_id=uid, seed=1, subject_id="dai_so_tuyen_tinh", floor=1, layout={}, hearts=3,
                           max_hearts=3, state="cleared", started_at=now, ended_at=now),
            MathDungeonRun(user_id=uid, seed=2, subject_id="dai_so_tuyen_tinh", floor=1, layout={}, hearts=0,
                           max_hearts=3, state="failed", started_at=now, ended_at=now),
            TdProgress(user_id=uid, level_id=level, stars=2, best_wave=5, cleared_at=now),
            TdProgress(user_id=uid, level_id="old_word_game_level", stars=3, best_wave=5, cleared_at=now),
            MathSubmission(user_id=uid, problem_id="p1", subject_id="dai_so_tuyen_tinh", floor=1, tier=1,
                           passed=5, total=5, created_at=now, judged_at=now),
            MathSubmission(user_id=uid, problem_id="p1", subject_id="dai_so_tuyen_tinh", floor=1, tier=1,
                           passed=5, total=5, created_at=now, judged_at=now),   # the same exercise again
            MathSubmission(user_id=uid, problem_id="p2", subject_id="dai_so_tuyen_tinh", floor=1, tier=1,
                           passed=3, total=5, created_at=now, judged_at=now),   # not every test
        ])
        await db.commit()
    f = await facts(uid)
    try:
        assert await f.progress({"type": "placement_done", "count": 3}) == (1, 3)
        assert await f.progress({"type": "mistakes_cleared", "count": 1}) == (1, 1)
        assert await f.progress({"type": "dungeon_cleared", "count": 2}) == (1, 2)
        assert await f.progress({"type": "td_wins", "count": 1}) == (1, 1)
        assert await f.progress({"type": "code_solved", "count": 4}) == (1, 4)
        assert await f.progress({"type": "fortune_won", "count": 1}) == (0, 1)
        assert await f.progress({"type": "realm", "target": "pham_nhan"}) == (1, 1)
        assert await f.progress({"type": "realm", "target": "kim_dan"}) == (0, 1)
        where = tp.working_position_of(f.st)
        unlocked = sum(1 for s in math_skills.skills().values() if math_skills.locked_reason(s, where) is None)
        assert await f.progress({"type": "skills_unlocked", "count": 99}) == (unlocked, 99)
        node = f.st.open[0]
        assert await f.progress({"type": "node_done", "node": node}) == (0, 1)
        vacant = next(iter(f.st.vacant))
        assert await f.progress({"type": "node_done", "node": vacant}) == (0, 1)   # vacant is not "done" here
        branch = math_tree.tree().nodes[node].branch
        assert await f.progress({"type": "nodes_done", "count": 1, "branch": branch}) == (0, 1)
    finally:
        await f.db.close()
    await pass_node(uid, node)
    f = await facts(uid)
    try:
        assert await f.progress({"type": "node_done", "node": node}) == (1, 1)
        assert await f.progress({"type": "nodes_done", "count": 2, "branch": branch}) == (1, 2)
        assert await f.progress({"type": "trials_passed", "count": 9}) == (len(tp.parts(node)), 9)
    finally:
        await f.db.close()


async def test_a_won_fortune_is_found_in_the_log_or_in_the_ledger(client, board):
    h, uid = await make(client, "guide_luck")
    async with dbm.SessionLocal() as db:
        u = await db.get(User, uid)
        u.flags = {**(u.flags or {}), "math_fortune": {"log": [{"event": "x", "outcome": "lost"},
                                                                {"event": "y", "outcome": "won"}]}}
        await db.commit()
    f = await facts(uid)
    try:
        assert await f.progress({"type": "fortune_won", "count": 1}) == (1, 1)
    finally:
        await f.db.close()
    async with dbm.SessionLocal() as db:                    # the log rolled over; the ledger remembers
        u = await db.get(User, uid)
        u.flags = {**u.flags, "math_fortune": {"log": []}}
        db.add(AuditLog(user_id=uid, currency_or_item="spirit_stones", delta=40, balance_after=340,
                        reason="math_fortune", ref_id="elder", created_at=dt.datetime(2026, 1, 1)))
        await db.commit()
    f = await facts(uid)
    try:
        assert await f.progress({"type": "fortune_won", "count": 1}) == (1, 1)
    finally:
        await f.db.close()


async def test_a_view_costs_one_tree_state(client, board, monkeypatch):
    h, uid = await make(client, "guide_cheap")
    calls = []
    real = tp.state

    async def counted(db, user_id):
        calls.append(user_id)
        return await real(db, user_id)
    monkeypatch.setattr(tp, "state", counted)
    await get(client, h)
    assert calls == [uid]
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(func.count()).select_from(AuditLog))).scalar() == 0   # GET writes nothing


async def test_the_flags_are_written_only_if_nobody_changed_them_since_they_were_read(client, board, monkeypatch):
    """The compare-and-swap itself: a claim that read the flags before another request
    marked the step does not write over it; it reads again and is refused."""
    h, uid = await make(client, "guide_swap")
    await seen(client, h, "math_hub")
    async with dbm.SessionLocal() as db:
        stale = await guide._read_flags(db, uid)               # read before the other claim lands
    assert (await claim(client, h, "s_hub")).status_code == 200
    real, reads = guide._read_flags, []

    async def first_stale(db, user_id):
        reads.append(user_id)
        return stale if len(reads) == 1 else await real(db, user_id)
    monkeypatch.setattr(guide, "_read_flags", first_stale)
    async with dbm.SessionLocal() as db:
        user = await db.get(User, uid)
        with pytest.raises(guide.GuideError) as e:
            await guide._swap(db, user, lambda g: (_ for _ in ()).throw(guide.GuideError(400, "already_claimed", ""))
                              if "s_hub" in g["claimed"] else {**g, "claimed": g["claimed"] + ["s_hub"]})
        assert e.value.code == "already_claimed" and len(reads) == 2      # the stale write matched no row
