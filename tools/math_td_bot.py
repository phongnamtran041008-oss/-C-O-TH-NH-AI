#!/usr/bin/env python3
"""A Thủ thành toán player (M10) that plays one whole level through the public API, the way
the client does: it starts a run, simulates the board with td_sim (the same file the game
uses), asks for a question before every tower it places or upgrades, answers it - right, or
wrong with probability `--wrong-rate`, from the answer key the way the test helpers read it
- logs the action with that question, answers the Linh Khí questions between waves and
presses Tụ Khí, saves its log as it goes, waits as long as a player would have needed at
the fastest speed, and finishes the run so the server replays and checks it.

Where to build comes from tools/td_bot.py (`decide`, the careful beginner of the old edition).

    python tools/math_td_bot.py --url http://127.0.0.1:8000 --db server/dev.db --seeds 3 --wrong-rate 0.2

In a test the same `play_round` runs against the app in-process (see
server/tests/test_math_td.py): only the HTTP client, the answer-key reader and the clock
differ.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / "server", ROOT / "tools"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import td_bot  # noqa: E402
from app.systems import td_sim  # noqa: E402


class BotError(Exception):
    def __init__(self, path: str, status: int, body: str):
        super().__init__(f"{path} -> {status}: {body[:300]}")
        self.path, self.status, self.body = path, status, body


class Api:
    """The few calls a player makes. `http` is any httpx.AsyncClient (a live server, or the
    app in-process); `keyfn(session_id)` reads a question's answer key (tests only);
    `waitfn(seconds)` lets real time pass (asyncio.sleep, or a frozen clock in a test)."""

    def __init__(self, http, headers: dict, keyfn, waitfn):
        self.http, self.headers, self.keyfn, self.waitfn = http, headers, keyfn, waitfn

    async def get(self, path: str) -> dict:
        r = await self.http.get(path, headers=self.headers)
        if r.status_code != 200:
            raise BotError(path, r.status_code, r.text)
        return r.json()

    async def post(self, path: str, body: dict) -> dict:
        r = await self.http.post(path, json=body, headers=self.headers)
        if r.status_code != 200:
            raise BotError(path, r.status_code, r.text)
        return r.json()

    async def key(self, session_id: str) -> dict:
        out = self.keyfn(session_id)
        return await out if asyncio.iscoroutine(out) else out

    async def wait(self, seconds: float) -> None:
        out = self.waitfn(seconds)
        if asyncio.iscoroutine(out):
            await out


# ------------------------------------------------------------------ answering
def right_answer(q: dict, key: dict) -> dict:
    t = q["qtype"]
    if t == "true_false":
        return {"value": key["value"]}
    if t == "multiple_choice":
        return {"option": key["option"]}
    if t == "matching":
        return {"pairs": list(key["pairs"])}
    if t == "ordering":
        return {"order": list(key["order"])}
    if t == "find_mistake":
        return {"line": key["line"]}
    return {"text": ", ".join(key["numbers"])}


def wrong_answer(q: dict, key: dict) -> dict:
    t = q["qtype"]
    if t == "true_false":
        return {"value": not key["value"]}
    if t == "multiple_choice":
        return {"option": next(o["id"] for o in q["options"] if o["id"] != key["option"])}
    if t in ("matching", "ordering"):          # rotated: every entry in the wrong place
        name = "pairs" if t == "matching" else "order"
        return {name: key[name][1:] + key[name][:1]}
    if t == "find_mistake":                             # the next line: always another line
        return {"line": (key["line"] + 1) % len(q["prompt"]["lines"])}
    return {"text": "987654"}


# ------------------------------------------------------------------ one round
async def play_round(api: Api, level_id: str | None = None, seed: int = 1, wrong_rate: float = 0.0,
                     save_every: int = 25) -> dict:
    """Play one level to its end and finish it. Returns a report: the bot's claim, the
    server's verdict, whether they agree, and what was asked."""
    rng = random.Random(seed)
    view = await api.get("/math/td")
    if level_id is None:
        level_id = next(lv["id"] for lv in view["levels"] if lv["unlocked"])
    started = time.monotonic()
    run = await api.post("/math/td/start", {"level_id": level_id})
    rid, params = run["run_id"], run["params"]
    answers: dict = {}
    sim = td_sim.Sim(params, answers)
    events: list[dict] = []
    saved = [0]
    asked: list[dict] = []

    async def question(kind: str, tower: str | None) -> str:
        q = await api.post("/math/td/question", {"run_id": rid, "kind": kind, "tower_id": tower})
        key = await api.key(q["session_id"])
        right = rng.random() >= wrong_rate
        res = await api.post("/quiz/answer", {"session_id": q["session_id"],
                                              "answer": right_answer(q, key) if right else wrong_answer(q, key)})
        ok = bool(res["correct"])
        answers[q["session_id"]] = {"kind": kind, "word": tower or "", "ok": ok, "power": q["math_td"]["power"]}
        asked.append({"kind": kind, "tower": tower, "ok": ok, "meant": right, "math": q["math"]})
        return q["session_id"]

    async def save() -> None:
        if len(events) > saved[0]:
            r = await api.post("/math/td/event", {"run_id": rid, "start": saved[0], "events": events[saved[0]:]})
            saved[0] = r["saved"]

    async def do(ev: dict) -> None:
        ev = {"s": sim.step_n, **ev}
        sim.apply(ev)
        events.append(ev)
        if len(events) - saved[0] >= save_every:
            await save()

    async def act(a: dict) -> None:
        if a["k"] == "up":
            await do({"k": "up", "x": a["x"], "y": a["y"], "q": await question("upgrade", a["w"])})
        else:
            await do({**a, "q": await question("place", a["w"])})

    while sim.phase not in (td_sim.WON, td_sim.LOST):
        if sim.phase == td_sim.BUILD:
            for _ in range(params["qi"]["break_questions"] - sim.break_q):
                await do({"k": "qi", "q": await question("break", None)})
            for _ in range(30):
                acts = td_bot.decide(sim)
                if not acts:
                    break
                await act(acts[0])
            await do({"k": "wave"})
            continue
        sim.step()
        if sim.phase != td_sim.WAVE:
            continue
        if sim.step_n - sim.last_tu_khi >= sim.tu_khi_cd() and sim.step_n % 7 == 0 and sim.qi < 90:
            await do({"k": "qi", "q": await question("tu_khi", None)})
        if sim.step_n % 10 == 0:
            acts = td_bot.decide(sim)
            if acts:
                await act(acts[0])
    await save()
    s = sim.summary()
    claim = {k: s[k] for k in ("result", "core_hp", "wave", "steps")}
    # a player needs at least this long, even at the fastest speed the server allows
    need = sim.step_n * td_sim.STEP_MS / 1000 / run["max_speed"] + 1
    await api.wait(max(0.0, need - (time.monotonic() - started)))
    res = await api.post("/math/td/finish", {"run_id": rid, "events": events, "claim": claim})
    return {"seed": seed, "level_id": level_id, "claim": claim,
            "server": {k: res.get(k) for k in ("result", "core_hp", "wave", "steps")},
            "agree": all(res.get(k) == claim[k] for k in claim), "stars": res.get("stars"),
            "rewards": res.get("rewards"), "towers": {sim.plants[c].word for c in sim.order},
            "questions": len(asked), "right": sum(a["ok"] for a in asked), "asked": asked, "events": len(events)}


# ------------------------------------------------------------------ a live server
def sqlite_keys(db: Path):
    def key(sid: str) -> dict:
        con = sqlite3.connect(db)
        try:
            return json.loads(con.execute("select answer_key from quiz_sessions where id=?", (sid,)).fetchone()[0])
        finally:
            con.close()
    return key


async def main_async(args) -> int:
    import httpx
    async with httpx.AsyncClient(base_url=args.url, timeout=30) as http:
        name = f"{args.prefix}_{int(time.time())}"
        r = await http.post("/auth/register", json={"username": name, "password": "matkhau1"})
        r.raise_for_status()
        api = Api(http, {"Authorization": f"Bearer {r.json()['token']}"}, sqlite_keys(Path(args.db)), asyncio.sleep)
        bad = 0
        for seed in range(1, args.seeds + 1):
            rep = await play_round(api, args.level, seed, args.wrong_rate)
            bad += not rep["agree"]
            print(f"seed {seed}: {rep['claim']['result']} core {rep['claim']['core_hp']} wave {rep['claim']['wave']} "
                  f"steps {rep['claim']['steps']} questions {rep['right']}/{rep['questions']} "
                  f"server agrees: {rep['agree']} rewards {rep['rewards']}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--db", default=str(ROOT / "server" / "dev.db"), help="the server's SQLite file (answer keys)")
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--wrong-rate", type=float, default=0.0)
    ap.add_argument("--level", default=None)
    ap.add_argument("--prefix", default="mtdbot")
    return asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
