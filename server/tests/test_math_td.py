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
  * rewards after the replay; one run at a time; leftovers of the removed word tower defence
    are never shown or continued;
  * the bot (tools/math_td_bot.py) plays 20 seeds through the API and every run ends clean.

And the run plumbing (systems/td.py, td_sim.py), on this mode's levels: the simulation is the
client's file byte for byte and replays a log to the same end; fake logs are refused by the
simulation and by the API (false claims, forged events, unasked or hidden questions, a run
faster than real time, an unfinished run); the saved log lets a closed game continue, cannot
be rewritten, and forgets a question asked after the last save.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app import clock
from app import db as dbm
from app.learning import math_path
from app.models import CodexEntry, InventoryItem, MathAnswer, Pet, TdProgress, TdRun, User
from app.systems import math_combat, math_practice, math_td, quests, td, td_sim
from tests.helpers import answer_key, register
from tests.test_math_ask import open_tier_2
from tests.test_math_skills import clear_floor, right_answer, wrong_answer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import math_td_bot  # noqa: E402

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
    return math_td_bot.best_cell(sim, tower)


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
    # a new player: the towers of floor 1 - of Đại Số Tuyến Tính and, since M11 wrote them, of
    # Xác Suất và Thống Kê and Giải Tích
    assert [k for k, v in t.items() if v["available"]] == ["tap_hop", "xac_suat", "gradient"]
    assert "tầng 2" in t["so_phuc"]["locked_vi"] and "Đạo Thụ" in t["so_phuc"]["locked_vi"]
    assert "tầng 3" in t["vecto"]["locked_vi"]
    for k in ("xac_suat", "gradient"):
        assert t[k]["available"] and t[k]["locked_vi"] is None
    run = await start(client, h)
    assert set(run["params"]["plants"]) == {"tap_hop", "xac_suat", "gradient"}  # the simulation knows only what is open
    assert {x["id"]: x["available"] for x in run["towers"]}["vecto"] is False    # the bar shows the rest, locked
    # Đạo Thụ: floor 1's node opens floor 3's (vectors and matrices). Floor 2 holds only an optional
    # node, whose micro-skills are not asked outside its own sittings (R6): its tower stays shut ...
    await clear_floor(uid, 1)
    t = await towers_of(client, h)
    assert {k for k, v in t.items() if v["available"]} == {"tap_hop", "vecto", "ma_tran", "xac_suat", "gradient"}
    assert not t["so_phuc"]["available"] and "tầng 2" in t["so_phuc"]["locked_vi"]
    # ... until the player has finished that optional node: then its micro-skills may come back
    await clear_floor(uid, 2)
    t = await towers_of(client, h)
    assert ({k for k, v in t.items() if v["available"]}
            == {"tap_hop", "so_phuc", "vecto", "ma_tran", "xac_suat", "gradient"})
    assert t["so_phuc"]["locked_vi"] is None
    # a tower that is not open in this run cannot be asked about, whatever the client sends
    await ask(client, h, run["run_id"], "place", "vecto", status=400)
    await ask(client, h, run["run_id"], "place", "ma_tran", status=400)
    await ask(client, h, run["run_id"], "place", "khong_co", status=400)


@pytest.mark.asyncio
async def test_a_locked_subject_tower_opens_by_itself_when_the_subject_gets_questions(client, monkeypatch):
    """A tower whose subject has no question is locked, with the reason; it opens with no change
    to math/td.json once the subject has some. Until M11 the test had to fake a written subject;
    now Xác Suất và Thống Kê is written, so it hides its questions to see the locked state."""
    real_templates = math_practice._templates
    h, uid = await player(client, "mtd_new_subject")
    with monkeypatch.context() as unwritten:
        unwritten.setattr(math_practice, "_templates",
                          lambda sid, floor: [] if sid == "xac_suat_thong_ke" else real_templates(sid, floor))
        t = await towers_of(client, h)
        assert not t["xac_suat"]["available"]
        assert "Xác Suất và Thống Kê" in t["xac_suat"]["locked_vi"] and "chưa có câu hỏi" in t["xac_suat"]["locked_vi"]
        assert t["gradient"]["available"]                                       # Giải Tích is not affected
        run = await start(client, h)
        assert "xac_suat" not in run["params"]["plants"]
        await ask(client, h, run["run_id"], "place", "xac_suat", status=400)
    t = await towers_of(client, h)
    assert t["xac_suat"]["available"] and t["xac_suat"]["locked_vi"] is None
    run = await start(client, h)
    assert "xac_suat" in run["params"]["plants"]
    q = await ask(client, h, run["run_id"], "place", "xac_suat")
    assert q["math"]["subject"] == "xac_suat_thong_ke" and q["math"]["floor"] == 1


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
        again = td_sim.replay(row.params, td.answers(row), row.events, finish=False)
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
        for tower in ("tap_hop", "vecto", "ma_tran"):     # (so_phuc: an optional node's area, never open)
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
        x, y = open_cell(sim, "vecto")
        q = await ask(client, h, run["run_id"], "place", "tap_hop")
        await reply(client, h, q, right=True)
        return [{"s": 0, "k": "place", "x": x, "y": y, "w": "vecto", "q": q["session_id"]}]

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
async def test_one_run_at_a_time_and_word_leftovers_are_ignored(client, frozen):
    """A run of the removed word tower defence left in td_runs is never shown, asked about or
    continued; starting a run deletes it. A new run replaces an unfinished one; a run left
    too long is gone."""
    h, uid = await player(client, "mtd_runs")
    async with dbm.SessionLocal() as db:
        db.add(TdRun(id="old_word_run", user_id=uid, level_id="c1_01", params={}, questions={}, events=[],
                     started_at=clock.now(), updated_at=clock.now()))
        await db.commit()
    assert (await client.get("/math/td", headers=h)).json()["active_run"] is None
    assert (await client.post("/math/td/resume", headers=h)).status_code == 404
    await ask(client, h, "old_word_run", "break", status=404)
    r = await client.post("/math/td/event", json={"run_id": "old_word_run", "start": 0, "events": []}, headers=h)
    assert r.status_code == 404
    run = await start(client, h)
    assert (await client.get("/math/td", headers=h)).json()["active_run"]["run_id"] == run["run_id"]
    async with dbm.SessionLocal() as db:
        assert await db.get(TdRun, "old_word_run") is None                  # gone with the new run
    # a new run replaces an unfinished one
    a = await start(client, h)
    b = await start(client, h)
    await ask(client, h, a["run_id"], "break", status=404)
    await ask(client, h, b["run_id"], "break")
    assert (await client.post("/math/td/cancel", headers=h)).json() == {"cancelled": True}
    await ask(client, h, b["run_id"], "break", status=404)
    # a run left too long is gone
    c = await start(client, h)
    frozen.advance(hours=td.cfg()["anti_cheat"]["run_hours"] + 1)
    await ask(client, h, c["run_id"], "break", status=404)
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


# ------------------------------------------------------------------ Thiên kiếp (M11 đợt 2)
def test_the_thu_thanh_never_asks_a_thien_kiep():
    """A tower, an upgrade, a break question, Tụ Khí: short questions only (td.json qtypes)."""
    kinds = math_td.qtypes()
    assert "tribulation" not in kinds and set(kinds) == set(math_td.math_items.PLAYABLE_TYPES) - {"tribulation"}
    raw = copy.deepcopy(math_td._read())
    raw["qtypes"] = kinds + ["tribulation"]
    assert any("too long for a tower" in e for e in math_td.validate(raw))
    raw["qtypes"] = ["riddle"]
    assert any(e.startswith("qtypes must be a non-empty list of playable question types") for e in math_td.validate(raw))
    raw.pop("qtypes")
    assert "missing qtypes" in math_td.validate(raw)


async def test_every_question_of_the_mode_is_asked_with_its_qtypes(monkeypatch):
    seen = []

    async def fake_pick(*a, **k):
        seen.append(k.get("qtypes"))
        return None
    monkeypatch.setattr(math_td.math_ask, "pick", fake_pick)
    monkeypatch.setattr(math_td.math_ask, "pick_own", fake_pick)

    async def open_area(db, user_id, t, st=None):           # (no database here: the tower's whole area)
        return math_td.area_skills(t)
    monkeypatch.setattr(math_td, "tower_skills", open_area)
    run = type("Run", (), {"questions": {}, "params": {"plants": ["tap_hop"]}, "id": "r"})()

    async def get_run(*a, **k):
        return run
    monkeypatch.setattr(math_td.td, "get_run", get_run)
    user = type("U", (), {"id": 1})()
    for kind, tower in (("place", "tap_hop"), ("break", None), ("tu_khi", None)):
        with pytest.raises(Exception):                       # (no question: refused after asking)
            await math_td.ask(None, user, "r", kind, tower)
    assert seen == [math_td.qtypes()] * 3


# ------------------------------------------------------------------ the simulation (td_sim.py)
def sim_params(seed: int = 1, level: str = LEVEL, towers: list[str] | None = None) -> dict:
    """A level's params with every tower of the data open (as math_td.start builds them)."""
    views = [math_td.tower_view(t, None) for t in math_td.data()["towers"] if towers is None or t["id"] in towers]
    return math_td.build_params(math_td.levels()[level], math_td.sim_towers(views), seed)


def test_client_simulation_is_the_same_file():
    server = (ROOT / "server" / "app" / "systems" / "td_sim.py").read_bytes()
    client = (ROOT / "client" / "engine" / "td_sim.py").read_bytes()
    assert server == client


def test_the_tower_cards_carry_a_label_and_a_name():
    defs = sim_params()["plants"]
    t = math_td.towers()["tap_hop"]
    assert defs["tap_hop"] == {"role": t["role"], "label": t["label"], "name_vi": t["name_vi"],
                               "power": float(t["power"])}


@pytest.mark.parametrize("seed", [1, 7, 12345])
def test_replaying_a_valid_log_gives_the_same_result(seed):
    params = sim_params(seed)
    sim, answers, events = math_td_bot.play(td_sim, params, accuracy=0.8, seed=seed)
    assert sim.phase in (td_sim.WON, td_sim.LOST) and sim.plants
    again = td_sim.replay(json.loads(json.dumps(params)), json.loads(json.dumps(answers)),
                          json.loads(json.dumps(events)))
    assert again.summary() == sim.summary()
    assert (again.kills, again.leaked, again.qi) == (sim.kills, sim.leaked, sim.qi)


def test_fake_logs_are_refused_by_the_simulation():
    params = sim_params()
    fire = "tap_hop"
    path = [tuple(c) for c in params["path"]]
    free = next((x, y) for y in range(7) for x in range(12)
                if (x, y) not in path and [x, y] not in params["rocks"])
    good = {"p1": {"kind": "place", "word": fire, "ok": True}, "p2": {"kind": "place", "word": fire, "ok": True},
            "q1": {"kind": "break", "word": "", "ok": True}, "q2": {"kind": "upgrade", "word": fire, "ok": True}}

    def refused(events, answers=None):
        with pytest.raises(td_sim.LogError):
            td_sim.replay(params, answers if answers is not None else good, events)

    refused([{"s": 0, "k": "place", "x": free[0], "y": free[1], "w": "khong_co", "q": "p1"}])  # no such tower
    refused([{"s": 0, "k": "place", "x": path[3][0], "y": path[3][1], "w": fire, "q": "p1"}])  # on the path
    refused([{"s": 0, "k": "place", "x": free[0], "y": free[1], "w": fire, "q": "p1"},       # same cell twice
             {"s": 0, "k": "place", "x": free[0], "y": free[1], "w": fire, "q": "p2"}])
    refused([{"s": 0, "k": "place", "x": x, "y": y, "w": fire, "q": f"m{i}"}                 # more than the Linh Khí
             for i, (x, y) in enumerate([(x, y) for y in range(7) for x in range(12) if (x, y) not in path][:6])],
            {f"m{i}": {"kind": "place", "word": fire, "ok": True} for i in range(6)})
    refused([{"s": 0, "k": "qi", "q": "made_up"}])                                       # never asked
    refused([{"s": 0, "k": "sell", "x": [1], "y": 2}])                                   # wrong types
    refused([{"s": 0, "k": "place", "x": 1, "y": 1, "w": {"a": 1}}])
    refused([{"s": 0, "k": "skill", "w": fire}])                                         # no such action
    refused(["wave"])
    refused([{"s": 0, "k": "qi", "q": "q1"}, {"s": 0, "k": "qi", "q": "q1"}])            # used twice
    refused([{"s": 0, "k": "qi", "q": "q2"}])                                            # an upgrade question
    refused([{"s": 0, "k": "place", "x": free[0], "y": free[1], "w": fire, "q": "p1"},  # upgrade about another tower
             {"s": 0, "k": "up", "x": free[0], "y": free[1], "q": "q3"}],
            {**good, "q3": {"kind": "upgrade", "word": "gradient", "ok": True}})
    refused([{"s": 5, "k": "wave"}])                                                     # time passes only in waves
    refused([{"s": 0, "k": "wave"}, {"s": 40, "k": "qi", "q": "q1"}])                    # a break question mid-wave
    refused([{"s": 0, "k": "wave"}, {"s": 3, "k": "wave"}])
    refused([{"s": 0, "k": "place", "x": free[0], "y": free[1], "w": fire, "q": "p1"}, {"s": 0, "k": "wave"},
             {"s": 9, "k": "sell", "x": free[0], "y": free[1]}, {"s": 4, "k": "wave"}])  # going back in time
    tk = {"t1": {"kind": "tu_khi", "word": "", "ok": True}, "t2": {"kind": "tu_khi", "word": "", "ok": True}}
    refused([{"s": 0, "k": "wave"}, {"s": 10, "k": "qi", "q": "t1"}, {"s": 50, "k": "qi", "q": "t2"}], tk)  # cooldown
    # the honest version of the same actions is fine
    ok = td_sim.replay(params, tk, [{"s": 0, "k": "wave"}, {"s": 10, "k": "qi", "q": "t1"},
                                    {"s": 10 + td_sim.Sim(params).tu_khi_cd(), "k": "qi", "q": "t2"}])
    assert ok.phase in (td_sim.WON, td_sim.LOST, td_sim.BUILD)


def test_a_wrong_answer_is_a_wrong_answer_in_the_replay():
    """The replay uses the server's record of each answer, never the client's."""
    params = sim_params()
    path = [tuple(c) for c in params["path"]]
    free = next((x, y) for y in range(7) for x in range(12) if (x, y) not in path and [x, y] not in params["rocks"])
    evs = [{"s": 0, "k": "place", "x": free[0], "y": free[1], "w": "tap_hop", "q": "p"},
           {"s": 0, "k": "up", "x": free[0], "y": free[1], "q": "u"}]
    placed = {"kind": "place", "word": "tap_hop", "ok": True}
    right = td_sim.replay(params, {"p": placed, "u": {"kind": "upgrade", "word": "tap_hop", "ok": True}}, evs)
    wrong = td_sim.replay(params, {"p": placed, "u": {"kind": "upgrade", "word": "tap_hop", "ok": False}}, evs)
    assert right.plants[free].level == 2 and wrong.plants[free].level == 1
    assert right.qi == wrong.qi          # the Linh Khí is spent either way


def test_hidden_monsters_need_light():
    """Mực Ẩn walks past every tower unless a Quang tower (xac_suat) lights the path."""
    lv = {"id": "t", "path": [[x, 3] for x in range(12)], "rocks": [],
          "waves": [[{"m": "muc_an", "n": 1, "gap": 1000, "at": 0}]]}
    defs = math_td.sim_towers([math_td.tower_view(t, None) for t in math_td.data()["towers"]])
    assert defs["xac_suat"]["role"] == "quang" and defs["vecto"]["role"] == "kim"

    def play(towers):
        answers = {f"q{i}": {"kind": "place", "word": w, "ok": True} for i, (_, w) in enumerate(towers)}
        sim = td_sim.Sim(math_td.build_params(lv, defs, 1), answers)
        sim.qi = 1000
        for i, ((x, y), w) in enumerate(towers):
            sim.apply({"k": "place", "x": x, "y": y, "w": w, "q": f"q{i}"})
        sim.apply({"k": "wave"})
        while sim.phase == td_sim.WAVE:
            sim.step()
        return sim
    kim = [((4, 2), "vecto"), ((5, 2), "vecto"), ((6, 2), "vecto")]
    dark = play(kim)
    assert dark.leaked == 1 and dark.kills == 0
    lit = play(kim + [((5, 4), "xac_suat")])
    assert lit.kills == 1 and lit.leaked == 0


# ------------------------------------------------------------------ the run plumbing through the API
class StopBeforeFinish(Exception):
    pass


async def played_not_finished(client, h, frozen, seed: int = 2, wrong_rate: float = 0.0) -> dict:
    """The bot plays a whole level through the API (every question asked and answered, the log
    saved as it goes) and stops right before /math/td/finish: returns the finish body."""
    api = bot_api(client, h, frozen)
    real_post, body = api.post, {}

    async def post(path, b):
        if path == "/math/td/finish":
            body.update(b)
            raise StopBeforeFinish
        return await real_post(path, b)
    api.post = post
    with pytest.raises(StopBeforeFinish):
        await math_td_bot.play_round(api, seed=seed, wrong_rate=wrong_rate)
    return body


async def finish(client, h, body: dict):
    return await client.post("/math/td/finish", json=body, headers=h)


@pytest.mark.asyncio
async def test_saved_log_lets_a_closed_game_continue(client, frozen):
    """/math/td/event saves the log as it grows; /math/td/resume gives it back after the game
    was closed, and the run finishes normally from there; the monsters met go into the Yêu
    Quái Phổ."""
    h, uid = await player(client, "mtd_resume")
    body = await played_not_finished(client, h, frozen)
    rid, events = body["run_id"], body["events"]
    v = (await client.get("/math/td", headers=h)).json()
    assert v["active_run"]["level_id"] == LEVEL and v["active_run"]["run_id"] == rid
    assert v["active_run"]["waves"] == sum(e["k"] == "wave" for e in events)
    async with dbm.SessionLocal() as db:            # saved in the database, not in memory
        assert (await db.get(TdRun, rid)).events == events
    # saving the end again from an earlier index is fine (the overlap is the same)
    r = await client.post("/math/td/event", json={"run_id": rid, "start": len(events) - 2, "events": events[-2:]},
                          headers=h)
    assert r.status_code == 200 and r.json()["saved"] == len(events)
    res = (await client.post("/math/td/resume", headers=h)).json()          # the game was closed and opened again
    assert res["run_id"] == rid and res["events"] == events
    used = {e["q"] for e in events if "q" in e}
    assert set(res["answers"]) == used and all("power" in a for a in res["answers"].values())
    # the client rebuilds the board from the saved log, stopping where the log stops
    half = len(events) // 2
    mid = td_sim.replay(res["params"], res["answers"], res["events"][:half], finish=False)
    assert mid.step_n == events[half - 1]["s"] and len(mid.plants) > 0
    out = await finish(client, h, body)
    assert out.status_code == 200 and out.json()["stars"] >= 1, out.text
    assert (await client.get("/math/td", headers=h)).json()["active_run"] is None
    async with dbm.SessionLocal() as db:
        met = (await db.execute(select(CodexEntry).where(CodexEntry.user_id == uid, CodexEntry.codex == "monster",
                                                         CodexEntry.entry_id.startswith("td_")))).scalars().all()
        assert met and all(e.progress["kills"] >= 0 for e in met)
        assert sum(e.progress["kills"] for e in met) > 0


@pytest.mark.asyncio
async def test_a_saved_move_cannot_be_taken_back(client, frozen):
    h, uid = await player(client, "mtd_no_undo")
    body = await played_not_finished(client, h, frozen)
    rid, events = body["run_id"], body["events"]
    n = len(events) // 2
    changed = [dict(e, x=e.get("x", 0) + 1) if e.get("k") == "place" else e for e in events[:n]]
    r = await client.post("/math/td/event", json={"run_id": rid, "start": 0, "events": changed}, headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "log_conflict"
    r = await client.post("/math/td/event", json={"run_id": rid, "start": len(events) + 5, "events": events[n:]},
                          headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "log_gap"
    # finishing with a different past than the one saved is refused (and the run is gone)
    r = await finish(client, h, {**body, "events": changed + events[n:]})
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_log"
    assert (await finish(client, h, body)).status_code == 404


@pytest.mark.asyncio
async def test_the_api_refuses_fake_logs(client, frozen):
    h, uid = await player(client, "mtd_fake")
    # a question the server never asked
    body = await played_not_finished(client, h, frozen)
    forged = [dict(e, q="khong-co-cau-nay") if e.get("k") == "qi" else e for e in body["events"]]
    async with dbm.SessionLocal() as db:            # (the saved part must match, so the forgery is unsaved)
        (await db.get(TdRun, body["run_id"])).events = []
        await db.commit()
    r = await finish(client, h, {**body, "events": forged})
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_log"
    # a log that leaves out an answered question (a wrong one it wanted to hide)
    body = await played_not_finished(client, h, frozen, seed=3, wrong_rate=0.3)
    first_q = next(e for e in body["events"] if e.get("k") == "qi")
    async with dbm.SessionLocal() as db:
        (await db.get(TdRun, body["run_id"])).events = []
        await db.commit()
    r = await finish(client, h, {**body, "events": [e for e in body["events"] if e is not first_q]})
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_log"
    # the whole level in no time at all
    run = await start(client, h)
    events = [{"s": 0, "k": "wave"}]      # no towers: the wave walks in
    local = td_sim.replay(run["params"], {}, events)
    claim = {k: local.summary()[k] for k in ("result", "core_hp", "wave", "steps")}
    r = await finish(client, h, {"run_id": run["run_id"], "events": events, "claim": claim})
    assert r.status_code == 400 and r.json()["error"]["code"] == "too_fast"
    # an unfinished log
    run = await start(client, h)
    frozen.advance(seconds=10)
    r = await finish(client, h, {"run_id": run["run_id"], "events": [],
                                 "claim": {"result": "build", "core_hp": 20, "wave": 0, "steps": 0}})
    assert r.status_code == 400 and r.json()["error"]["code"] == "unfinished"
    async with dbm.SessionLocal() as db:            # nothing was ever rewarded
        assert (await db.execute(select(TdProgress).where(TdProgress.user_id == uid))).first() is None


@pytest.mark.asyncio
async def test_resume_drops_questions_asked_after_the_last_save(client, frozen):
    h, uid = await player(client, "mtd_drop_q")
    run = await start(client, h)
    q = await ask(client, h, run["run_id"], "break")
    await reply(client, h, q, right=True)
    res = (await client.post("/math/td/resume", headers=h)).json()      # closed before the answer was logged
    assert res["events"] == [] and res["answers"] == {}
    local, events = td_sim.Sim(run["params"], {}), []                  # no towers at all: lost, but a valid log
    while local.phase not in (td_sim.WON, td_sim.LOST):
        events.append({"s": local.step_n, "k": "wave"})
        local.apply(events[-1])
        while local.phase == td_sim.WAVE:
            local.step()
    frozen.advance(seconds=local.step_n * td_sim.STEP_MS / 1000)
    claim = {k: local.summary()[k] for k in ("result", "core_hp", "wave", "steps")}
    r = await finish(client, h, {"run_id": run["run_id"], "events": events, "claim": claim})
    assert r.status_code == 200 and r.json()["result"] == "lost", r.text
    assert r.json()["rewards"] == {}
    assert (await client.post("/math/td/resume", headers=h)).status_code == 404


# ------------------------------------------------------------------ what other loops get from a run
@pytest.mark.asyncio
async def test_khi_gives_more_linh_khi_to_start_with(client, frozen):
    """The Khỉ pet's skill (td_qi) adds Linh Khí at the start of a run."""
    h, uid = await player(client, "mtd_khi")
    a = await start(client, h)
    async with dbm.SessionLocal() as db:
        db.add(Pet(user_id=uid, pet_type="khi", level=1, equipped=True))
        await db.commit()
    b = await start(client, h)
    assert b["params"]["qi"]["start"] == a["params"]["qi"]["start"] + 20
    assert a["params"]["qi"]["start"] == math_td.data()["qi"]["start"]


@pytest.mark.asyncio
async def test_a_won_run_counts_for_the_td_win_quests(client, frozen, monkeypatch):
    seen = []
    real = quests.on_event

    async def on_event(db, user_id, kind, target, n=1):
        seen.append((user_id, kind, target))
        return await real(db, user_id, kind, target, n)
    monkeypatch.setattr(quests, "on_event", on_event)
    h, uid = await player(client, "mtd_quest")
    api = bot_api(client, h, frozen)
    rep = await math_td_bot.play_round(api, seed=2, wrong_rate=0.0)
    assert rep["server"]["result"] == "won"
    assert seen.count((uid, "td_win", "*")) == 1
    rep = await math_td_bot.play_round(api, seed=3, wrong_rate=1.0)
    assert rep["server"]["result"] == "lost" and seen.count((uid, "td_win", "*")) == 1
