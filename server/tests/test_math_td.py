"""M10: Thủ thành toán - towers that stand for an area of mathematics (systems/math_td.py).

The rules under test:
  * the data is sound (`validate`) and its checks have teeth;
  * a tower is available only when its area has questions and is on a floor the player has
    reached; a tower of a subject with no questions is locked with a reason and opens by
    itself when the subject gets questions;
  * placing and upgrading a tower each need a right answer to a question of that tower's
    area, at the player's own tier or below; wrong or out of time places nothing (the Linh
    Khí of the attempt is spent, nothing else is lost); every answer is in `math_answers`;
  * the server replays the log: a run whose events claim a tower that no right answer
    earned is refused;
  * rewards after the replay; the editions never touch each other's runs;
  * the bot (tools/math_td_bot.py) plays 20 seeds through the API and every run ends clean.
"""
import copy
import sys
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app import db as dbm
from app.learning import math_path
from app.models import InventoryItem, MathAnswer, TdProgress, TdRun, User
from app.systems import math_combat, math_practice, math_td, td, td_sim
from tests.helpers import answer_key, register
from tests.test_math_ask import open_tier_2
from tests.test_math_skills import clear_floor, right_answer, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import math_td_bot  # noqa: E402
import td_bot  # noqa: E402

SUBJECT = "dai_so_tuyen_tinh"
LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}
LEVEL = "math_td_01"


# ------------------------------------------------------------------ helpers
async def player(client, name: str):
    h, data = await register(client, name)
    r = await client.post("/character/create", json={"display_name": name.replace("_", " ").title(),
                                                      "appearance": LOOK}, headers=h)
    assert r.status_code == 200, r.text
    return h, data["user_id"]


async def ask(client, h, run_id: str, kind: str, tower: str | None = None, status: int = 200) -> dict:
    r = await client.post("/math/td/question", json={"run_id": run_id, "kind": kind, "tower_id": tower}, headers=h)
    assert r.status_code == status, r.text
    return r.json()


async def reply(client, h, q: dict, right: bool) -> dict:
    key = await answer_key(q["session_id"])
    r = await client.post("/quiz/answer", json={"session_id": q["session_id"],
                                                "answer": right_answer(q, key) if right else wrong_answer(q, key)},
                          headers=h)
    assert r.status_code == 200, r.text
    return r.json()


async def start(client, h) -> dict:
    r = await client.post("/math/td/start", json={"level_id": LEVEL}, headers=h)
    assert r.status_code == 200, r.text
    return r.json()


def open_cell(sim: td_sim.Sim, tower: str) -> tuple[int, int]:
    return td_bot.best_cell(sim, tower)


def bot_api(client, h, frozen) -> math_td_bot.Api:
    return math_td_bot.Api(client, h, answer_key, lambda s: frozen.advance(seconds=s))


async def towers_of(client, h) -> dict:
    r = await client.get("/math/td", headers=h)
    assert r.status_code == 200, r.text
    return {t["id"]: t for t in r.json()["towers"]}


# ------------------------------------------------------------------ data
def test_data_is_sound_and_the_checks_have_teeth():
    assert math_td.validate() == []
    d = math_td._read()
    ids = {t["id"] for t in d["towers"]}
    assert {"tap_hop", "so_phuc", "vecto", "ma_tran", "xac_suat", "gradient"} <= ids    # plan 4.3's four + floors 1-2
    floor3 = {k.id for k in math_path.subject(SUBJECT).floor(3).skills}
    t = math_td.towers()
    assert set(t["vecto"]["area"]["skills"]) | set(t["ma_tran"]["area"]["skills"]) == floor3
    assert not set(t["vecto"]["area"]["skills"]) & set(t["ma_tran"]["area"]["skills"])

    def broken(fn) -> list[str]:
        raw = copy.deepcopy(d)
        fn(raw)
        return math_td.validate(raw)
    assert any("role" in e for e in broken(lambda r: r["towers"][0].update(role="laser")))
    assert any("subjects.json" in e for e in broken(lambda r: r["towers"][0]["area"].update(subject="hoa_hoc")))
    assert any("micro-skill" in e for e in broken(lambda r: r["towers"][2]["area"].update(skills=["dstt_t9_khong_co"])))
    assert any("no floor" in e for e in broken(lambda r: r["towers"][0]["area"].update(floor=42)))
    assert any("neighbours" in e for e in broken(lambda r: r["levels"][0]["path"].pop(3)))
    assert any("rocks" in e for e in broken(lambda r: r["levels"][0]["rocks"].append([0, 1])))
    assert any("wave group" in e for e in broken(lambda r: r["levels"][0]["waves"][0][0].update(m="rong")))
    assert any("reward item" in e
               for e in broken(lambda r: r["levels"][0]["first_rewards"][1].update(items={"vang_ao": 1})))
    assert any("tier_power" in e for e in broken(lambda r: r["tier_power"].pop("3")))


# ------------------------------------------------------------------ which towers
@pytest.mark.asyncio
async def test_towers_open_with_the_learning_path(client):
    h, uid = await player(client, "mtd_floors")
    t = await towers_of(client, h)
    assert [k for k, v in t.items() if v["available"]] == ["tap_hop"]          # a new player: floor 1 only
    assert "tầng 1" in t["so_phuc"]["locked_vi"] and "Thiên kiếp nhỏ" in t["so_phuc"]["locked_vi"]
    assert "tầng 2" in t["vecto"]["locked_vi"]
    for k, subject in (("xac_suat", "Xác Suất và Thống Kê"), ("gradient", "Giải Tích")):
        assert not t[k]["available"] and subject in t[k]["locked_vi"] and "chưa có câu hỏi" in t[k]["locked_vi"]
    run = await start(client, h)
    assert set(run["params"]["plants"]) == {"tap_hop"}                          # the simulation knows only what is open
    assert {x["id"]: x["available"] for x in run["towers"]}["vecto"] is False    # the bar shows the rest, locked
    await clear_floor(uid, 1)
    assert {k for k, v in (await towers_of(client, h)).items() if v["available"]} == {"tap_hop", "so_phuc"}
    await clear_floor(uid, 2)
    t = await towers_of(client, h)
    assert {k for k, v in t.items() if v["available"]} == {"tap_hop", "so_phuc", "vecto", "ma_tran"}
    assert t["xac_suat"]["locked_vi"] and t["gradient"]["locked_vi"]
    # a tower that is not open in this run cannot be asked about, whatever the client sends
    await ask(client, h, run["run_id"], "place", "vecto", status=400)
    await ask(client, h, run["run_id"], "place", "gradient", status=400)
    await ask(client, h, run["run_id"], "place", "khong_co", status=400)


@pytest.mark.asyncio
async def test_a_locked_subject_tower_opens_by_itself_when_the_subject_gets_questions(client, monkeypatch):
    """Fake 'Xác Suất và Thống Kê' as a written subject whose floor 1 has questions (borrowed
    from Đại Số Tuyến Tính): the tower opens with no change to math/td.json."""
    real_subjects, real_templates = math_path.subjects(), math_practice._templates
    entry = next(e for e in math_path.load_index()["subjects"] if e["id"] == "xac_suat_thong_ke")
    raw = math_path._read(math_path.MATH_DIR / "dai_so_tuyen_tinh.json")
    fake = math_path.build_subject(entry, raw)
    monkeypatch.setattr(math_path, "subjects", lambda: real_subjects + (fake,))
    monkeypatch.setattr(math_practice, "_templates",
                        lambda sid, floor: real_templates(SUBJECT if sid == "xac_suat_thong_ke" else sid, floor))
    h, uid = await player(client, "mtd_new_subject")
    t = await towers_of(client, h)
    assert t["xac_suat"]["available"] and t["xac_suat"]["locked_vi"] is None
    assert not t["gradient"]["available"]                                       # Giải Tích is still unwritten
    run = await start(client, h)
    assert "xac_suat" in run["params"]["plants"]
    q = await ask(client, h, run["run_id"], "place", "xac_suat")
    assert q["math"]["floor"] == 1


# ------------------------------------------------------------------ placing and upgrading
@pytest.mark.asyncio
async def test_place_and_upgrade_each_need_a_right_answer(client, frozen):
    h, uid = await player(client, "mtd_place")
    run = await start(client, h)
    rid, params = run["run_id"], run["params"]
    answers: dict = {}
    sim = td_sim.Sim(params, answers)
    events: list = []

    def do(ev):
        ev = {"s": sim.step_n, **ev}
        sim.apply(ev)
        events.append(ev)

    cell = open_cell(sim, "tap_hop")
    cost = sim.cost_to_place("tap_hop")
    qi0 = sim.qi
    # wrong: nothing is built, the Linh Khí of the attempt is spent
    q = await ask(client, h, rid, "place", "tap_hop")
    res = await reply(client, h, q, right=False)
    assert res["correct"] is False and res["math_td"] == {"kind": "place", "tower": "tap_hop", "ok": False,
                                                          "power": q["math_td"]["power"], "qi": 0}
    answers[q["session_id"]] = {"kind": "place", "word": "tap_hop", "ok": False, "power": q["math_td"]["power"]}
    do({"k": "place", "x": cell[0], "y": cell[1], "w": "tap_hop", "q": q["session_id"]})
    assert cell not in sim.plants and sim.qi == qi0 - cost and sim.hp == params["core_hp"]
    # right: the tower stands, with the power of its question's tier
    q = await ask(client, h, rid, "place", "tap_hop")
    assert q["math_td"]["power"] == math_td.tier_power(q["math"]["tier"])
    res = await reply(client, h, q, right=True)
    assert res["correct"] and res["math_td"]["ok"] and res["xp"]["gained"] > 0          # Tu Vi by tier
    answers[q["session_id"]] = {"kind": "place", "word": "tap_hop", "ok": True, "power": q["math_td"]["power"]}
    do({"k": "place", "x": cell[0], "y": cell[1], "w": "tap_hop", "q": q["session_id"]})
    assert sim.plants[cell].level == 1 and sim.plants[cell].mult == q["math_td"]["power"]
    # upgrade: wrong keeps the level, right raises it (waves first, for the Linh Khí)
    for right, level in ((False, 1), (True, 2)):
        need = sim.cost_to_upgrade(sim.plants[cell])
        while sim.qi < need:
            if sim.phase == td_sim.BUILD:
                do({"k": "wave"})
            sim.step()
        assert sim.phase in (td_sim.BUILD, td_sim.WAVE)
        q = await ask(client, h, rid, "upgrade", "tap_hop")
        res = await reply(client, h, q, right=right)
        answers[q["session_id"]] = {"kind": "upgrade", "word": "tap_hop", "ok": res["correct"],
                                    "power": q["math_td"]["power"]}
        do({"k": "up", "x": cell[0], "y": cell[1], "q": q["session_id"]})
        assert sim.plants[cell].level == level
    r = await client.post("/math/td/event", json={"run_id": rid, "start": 0, "events": events}, headers=h)
    assert r.status_code == 200 and r.json()["saved"] == len(events)
    # the server's own record of the answers replays to the same board
    async with dbm.SessionLocal() as db:
        row = await db.get(TdRun, rid)
        again = td_sim.replay(row.params, td._answers(row), row.events, finish=False)
    assert again.plants[cell].level == 2 and again.qi == sim.qi
    # resuming hands back the same log and answers
    r = await client.post("/math/td/resume", headers=h)
    assert r.status_code == 200 and r.json()["events"] == events and set(r.json()["answers"]) == set(answers)


@pytest.mark.asyncio
async def test_running_out_of_time_is_a_wrong_answer_and_nothing_else(client, frozen):
    h, uid = await player(client, "mtd_timeout")
    run = await start(client, h)
    q = await ask(client, h, run["run_id"], "place", "tap_hop")
    frozen.advance(seconds=q["time_limit"] + 60)
    res = await reply(client, h, q, right=True)
    assert res["correct"] is False and res["timed_out"] and res["math_td"]["ok"] is False
    assert "xp" not in res
    async with dbm.SessionLocal() as db:
        row = (await db.execute(select(MathAnswer).where(MathAnswer.user_id == uid))).scalar_one()
        assert row.timed_out and not row.correct and row.run_id is None
        assert (await db.get(TdRun, run["run_id"])).questions[q["session_id"]]["ok"] is False
    # a timed-out Tụ Khí loses no Linh Khí in the math edition (rule 4.4)
    sim = td_sim.Sim(run["params"], {})
    assert run["params"]["qi"]["tu_khi_wrong_loss"] == 0 and sim.p["qi"]["tu_khi_wrong_loss"] == 0


@pytest.mark.asyncio
async def test_questions_come_from_the_towers_area_never_above_the_players_tier(client, frozen):
    h, uid = await player(client, "mtd_tier")
    for n in (1, 2):
        await clear_floor(uid, n)
    floor1 = [k.id for k in math_path.subject(SUBJECT).floor(1).skills]
    await open_tier_2(uid, floor1[0], 1)                 # one floor-1 skill at tier 2, the rest at tier 1
    run = await start(client, h)
    rid = run["run_id"]
    asked = 0
    async with dbm.SessionLocal() as db:
        for tower in ("tap_hop", "so_phuc", "vecto", "ma_tran"):
            t = math_td.towers()[tower]
            for kind in ("place", "upgrade"):
                for _ in range(4):
                    q = await ask(client, h, rid, kind, tower)
                    m = q["math"]
                    assert m["subject"] == t["area"]["subject"] and m["floor"] == t["area"]["floor"]
                    assert m["skill"] in math_td.area_skills(t)
                    assert m["tier"] <= await math_combat.tier_for(db, uid, m["skill"], m["floor"])
                    await reply(client, h, q, right=bool(asked % 2))
                    asked += 1
        for kind in ("break", "tu_khi"):                  # Linh Khí questions: the player's own floor (3)
            q = await ask(client, h, rid, kind)
            assert q["math"]["floor"] == 3
            assert q["math"]["tier"] <= await math_combat.tier_for(db, uid, q["math"]["skill"], 3)
            await reply(client, h, q, right=True)
            asked += 1
        n = (await db.execute(select(func.count()).select_from(MathAnswer).where(
            MathAnswer.user_id == uid, MathAnswer.run_id.is_(None)))).scalar_one()
        seeded = math_path.cfg()["tier_unlock"]["window"]
        assert n == asked + seeded                       # every answer is in the learning log
    await ask(client, h, rid, "laser", "tap_hop", status=422)


# ------------------------------------------------------------------ the replay refuses what was not earned
@pytest.mark.asyncio
async def test_the_server_refuses_a_tower_no_right_answer_earned(client, frozen):
    h, uid = await player(client, "mtd_cheat")
    await clear_floor(uid, 1)

    async def attempt(build) -> dict:
        run = await start(client, h)
        sim = td_sim.Sim(run["params"], {})
        events = await build(run, sim)
        claim = {"result": "won", "core_hp": 20, "wave": 5, "steps": 3000}
        frozen.advance(hours=1)
        r = await client.post("/math/td/finish", json={"run_id": run["run_id"], "events": events, "claim": claim},
                              headers=h)
        assert r.status_code == 400, r.text
        async with dbm.SessionLocal() as db:
            assert await db.get(TdRun, run["run_id"]) is None           # a refused run is gone
        return r.json()

    async def no_question(run, sim):
        x, y = open_cell(sim, "tap_hop")
        return [{"s": 0, "k": "place", "x": x, "y": y, "w": "tap_hop"}]

    async def wrong_answer_then_upgrade(run, sim):
        x, y = open_cell(sim, "tap_hop")
        q = await ask(client, h, run["run_id"], "place", "tap_hop")
        await reply(client, h, q, right=False)
        q2 = await ask(client, h, run["run_id"], "upgrade", "tap_hop")
        await reply(client, h, q2, right=True)
        return [{"s": 0, "k": "place", "x": x, "y": y, "w": "tap_hop", "q": q["session_id"]},
                {"s": 0, "k": "up", "x": x, "y": y, "q": q2["session_id"]}]

    async def answer_of_another_tower(run, sim):
        x, y = open_cell(sim, "so_phuc")
        q = await ask(client, h, run["run_id"], "place", "tap_hop")
        await reply(client, h, q, right=True)
        return [{"s": 0, "k": "place", "x": x, "y": y, "w": "so_phuc", "q": q["session_id"]}]

    async def one_answer_two_towers(run, sim):
        q = await ask(client, h, run["run_id"], "place", "tap_hop")
        await reply(client, h, q, right=True)
        a = open_cell(sim, "tap_hop")
        first = {"s": 0, "k": "place", "x": a[0], "y": a[1], "w": "tap_hop", "q": q["session_id"]}
        sim.answers[q["session_id"]] = {"kind": "place", "word": "tap_hop", "ok": True}
        sim.apply(first)
        b = open_cell(sim, "tap_hop")                   # a second cell that is free and legal
        return [first, {"s": 0, "k": "place", "x": b[0], "y": b[1], "w": "tap_hop", "q": q["session_id"]}]

    async def upgrade_answer_used_to_place(run, sim):
        x, y = open_cell(sim, "tap_hop")
        q = await ask(client, h, run["run_id"], "upgrade", "tap_hop")
        await reply(client, h, q, right=True)
        return [{"s": 0, "k": "place", "x": x, "y": y, "w": "tap_hop", "q": q["session_id"]}]

    for build in (no_question, wrong_answer_then_upgrade, answer_of_another_tower, one_answer_two_towers,
                  upgrade_answer_used_to_place):
        err = await attempt(build)
        assert err["error"]["code"] == "bad_log", (build.__name__, err)
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(TdProgress).where(TdProgress.user_id == uid))).first() is None


@pytest.mark.asyncio
async def test_a_true_log_with_a_false_claim_is_refused(client, frozen):
    h, uid = await player(client, "mtd_claim")
    rep = await math_td_bot.play_round(bot_api(client, h, frozen), seed=4)
    assert rep["agree"]
    # the same game again, then claim one more point of Linh Mạch than the log gives
    api = bot_api(client, h, frozen)
    real_post = api.post

    async def lying_post(path, body):
        if path == "/math/td/finish":
            body = {**body, "claim": {**body["claim"], "core_hp": body["claim"]["core_hp"] + 1}}
        return await real_post(path, body)
    api.post = lying_post
    with pytest.raises(math_td_bot.BotError) as e:
        await math_td_bot.play_round(api, seed=4)
    assert e.value.status == 400 and "log_mismatch" in e.value.body


# ------------------------------------------------------------------ runs and rewards
@pytest.mark.asyncio
async def test_rewards_after_the_replay(client, frozen):
    h, uid = await player(client, "mtd_reward")
    api = bot_api(client, h, frozen)
    async with dbm.SessionLocal() as db:
        stones0 = (await db.get(User, uid)).spirit_stones
    rep = await math_td_bot.play_round(api, seed=2, wrong_rate=0.0)
    assert rep["agree"] and rep["claim"]["result"] == "won" and rep["stars"] == 3      # every answer right
    lv = math_td.levels()[LEVEL]
    paid = sum(lv["first_rewards"][s - 1]["spirit_stones"] for s in range(1, rep["stars"] + 1))
    assert rep["rewards"]["spirit_stones"] == paid
    async with dbm.SessionLocal() as db:
        assert (await db.get(User, uid)).spirit_stones == stones0 + paid
        assert (await db.get(TdProgress, (uid, LEVEL))).stars == rep["stars"]
        for item, qty in (("manh_tap_hop", 2), ("tinh_so_phuc", 1), ("loi_ma_tran", 1)):    # M7 materials
            inv = (await db.execute(select(InventoryItem).where(InventoryItem.user_id == uid,
                                                                InventoryItem.item_id == item))).scalar_one()
            assert inv.quantity == qty
    # the same stars again: the daily replay stones, counted
    rep2 = await math_td_bot.play_round(api, seed=2, wrong_rate=0.0)
    assert rep2["claim"]["result"] == "won" and rep2["stars"] == 3
    assert rep2["rewards"] == {"spirit_stones": math_td.data()["rewards"]["replay_stones"], "replay": True}
    r = await client.get("/math/td", headers=h)
    assert r.json()["daily_left"] == math_td.data()["rewards"]["daily_rewarded_plays"] - 1
    assert r.json()["levels"][0]["stars"] == rep["stars"]
    # a lost run pays nothing
    rep3 = await math_td_bot.play_round(api, seed=3, wrong_rate=1.0)
    assert rep3["claim"]["result"] == "lost" and rep3["agree"] and rep3["rewards"] == {}
    assert rep3["right"] == 0 and not rep3["towers"]


@pytest.mark.asyncio
async def test_the_two_editions_never_touch_each_others_runs(client, frozen):
    from tests.test_td import BEGINNER, wid
    from tests.test_td import player as word_player
    h, uid = await word_player(client, "mtd_editions")
    old = await client.post("/td/start", json={"level_id": "c1_01", "loadout": [wid(hz) for hz in BEGINNER]},
                            headers=h)
    assert old.status_code == 200, old.text
    run = await start(client, h)
    # each edition sees only its own run
    assert (await client.get("/td/levels", headers=h)).json()["active_run"]["run_id"] == old.json()["run_id"]
    assert (await client.get("/math/td", headers=h)).json()["active_run"]["run_id"] == run["run_id"]
    r = await client.post("/td/question", json={"run_id": run["run_id"], "kind": "break"}, headers=h)
    assert r.status_code == 404
    r = await client.post("/math/td/question", json={"run_id": old.json()["run_id"], "kind": "break"}, headers=h)
    assert r.status_code == 404
    await client.post("/math/td/cancel", headers=h)
    async with dbm.SessionLocal() as db:
        assert await db.get(TdRun, old.json()["run_id"]) is not None and await db.get(TdRun, run["run_id"]) is None
    # a new math run replaces an unfinished math run; an old one stays
    a = await start(client, h)
    b = await start(client, h)
    await ask(client, h, a["run_id"], "break", status=404)
    await ask(client, h, b["run_id"], "break")
    # a run left too long is gone
    frozen.advance(hours=td.cfg()["anti_cheat"]["run_hours"] + 1)
    await ask(client, h, b["run_id"], "break", status=404)
    assert (await client.post("/math/td/resume", headers=h)).status_code == 404


# ------------------------------------------------------------------ the bot
@pytest.mark.asyncio
async def test_the_bot_plays_twenty_seeds_and_every_run_ends_clean(client, frozen):
    """tools/math_td_bot.py through the public API, 20 seeds and four wrong-answer rates:
    every run ends won or lost, the server's replay agrees with the bot, nothing raises."""
    h, uid = await player(client, "mtd_bot")
    api = bot_api(client, h, frozen)
    results = []
    for seed in range(1, 21):
        rate = (0.0, 0.2, 0.5, 0.9)[seed % 4]
        rep = await math_td_bot.play_round(api, seed=seed, wrong_rate=rate)
        assert rep["agree"], rep["claim"]
        assert rep["server"]["result"] in (td_sim.WON, td_sim.LOST)
        assert all(a["ok"] == a["meant"] for a in rep["asked"])
        assert all(a["math"]["floor"] == 1 for a in rep["asked"])         # a floor-1 player: floor-1 questions
        results.append(rep["server"]["result"])
    assert td_sim.WON in results and td_sim.LOST in results
    async with dbm.SessionLocal() as db:
        assert (await db.execute(select(func.count()).select_from(TdRun).where(TdRun.user_id == uid))).scalar_one() == 0
