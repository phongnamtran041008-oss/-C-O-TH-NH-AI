#!/usr/bin/env python3
"""A player of cơ duyên (M10) for tests and for a live server, through the public API only.

It sits down on floor 1 of the first subject, answers practice questions right until an offer
appears (`math.fortune_offer` in the answer), accepts it (or declines, `--decline-rate`), wins
or loses it (`--wrong-rate`: the chance a cơ duyên question is answered wrong), and goes on
until the day's limit of offers is used up.

Like the other bots it answers from the answer key, which a real player does not have: a
`key_of(session_id)` function supplies it. In a server test that is a read of the test
database (the default); against a live dev server pass `--db path/to/sqlite`.

    python tools/math_fortune_bot.py --url http://127.0.0.1:8000 --db server/kvtt.db --seed 3
"""
from __future__ import annotations

import argparse
import asyncio
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECT = "dai_so_tuyen_tinh"


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
    if t in ("matching", "ordering"):
        name = "pairs" if t == "matching" else "order"
        return {name: key[name][1:] + key[name][:1]}
    if t == "find_mistake":                             # the next line: always another line
        return {"line": (key["line"] + 1) % len(q["prompt"]["lines"])}
    return {"text": "987654"}


def sqlite_keys(path: str):
    """key_of() for a dev server whose SQLite file we can read."""
    def key_of(session_id: str) -> dict:
        import json
        con = sqlite3.connect(path)
        try:
            return json.loads(con.execute("select answer_key from quiz_sessions where id=?", (session_id,)).fetchone()[0])
        finally:
            con.close()
    return key_of


async def db_keys(session_id: str) -> dict:
    """key_of() inside a server test: the application's own database."""
    from sqlalchemy import select
    from app import db as dbm
    from app.models import QuizSession
    async with dbm.SessionLocal() as s:
        return (await s.execute(select(QuizSession.answer_key).where(QuizSession.id == session_id))).scalar_one()


class FortuneBot:
    """`client` is an httpx.AsyncClient (ASGI in a test, or a real base_url), `headers` its auth."""

    def __init__(self, client, headers: dict, key_of=None, seed: int = 0, wrong_rate: float = 0.0,
                 decline_rate: float = 0.0, max_answers: int = 3000):
        self.client, self.h = client, headers
        self.key_of = key_of or db_keys
        self.rng = random.Random(seed)
        self.wrong_rate, self.decline_rate, self.max_answers = wrong_rate, decline_rate, max_answers
        self.run_id: int | None = None
        self.summary = {"answers": 0, "offers": 0, "won": 0, "lost": 0, "declined": 0, "stones": 0,
                        "items": {}, "events": []}

    async def _call(self, method: str, path: str, **kw):
        r = await getattr(self.client, method)(path, headers=self.h, **kw)
        assert r.status_code == 200, f"{method} {path}: {r.status_code} {r.text}"
        return r.json()

    async def _key(self, session_id: str) -> dict:
        key = self.key_of(session_id)
        return await key if asyncio.iscoroutine(key) else key

    async def _answer(self, q: dict, right: bool) -> dict:
        key = await self._key(q["session_id"])
        a = right_answer(q, key) if right else wrong_answer(q, key)
        return await self._call("post", "/quiz/answer", json={"session_id": q["session_id"], "answer": a})

    async def _practice_once(self) -> dict | None:
        """One right practice answer; returns the fortune offer it earned, if any."""
        if self.run_id is None:
            res = await self._call("post", "/math/run/start", json={"subject_id": SUBJECT, "floor": 1})
            self.run_id = res["run"]["run_id"]
        q = (await self._call("post", "/math/run/next", json={"run_id": self.run_id}))["question"]
        res = await self._answer(q, True)
        self.summary["answers"] += 1
        return (res.get("math") or {}).get("fortune_offer")

    async def _play_event(self) -> None:
        s = self.summary
        s["offers"] += 1
        if self.rng.random() < self.decline_rate:
            await self._call("post", "/math/fortune/decline")
            s["declined"] += 1
            return
        got = await self._call("post", "/math/fortune/accept")
        q, fortune = got["question"], None
        while q is not None:
            res = await self._answer(q, self.rng.random() >= self.wrong_rate)
            s["answers"] += 1
            fortune = res["fortune"]
            q = fortune.get("next")
        if fortune is None:       # the game had no question for this player: nothing was lost
            return
        assert fortune["done"], fortune
        s["events"].append({"event": fortune["event"], "won": fortune["won"], "rewards": fortune["rewards"]})
        if not fortune["won"]:
            s["lost"] += 1
            return
        s["won"] += 1
        r = fortune["rewards"]
        s["stones"] += r["spirit_stones"]
        for i in r["items"]:
            s["items"][i["item"]] = s["items"].get(i["item"], 0) + i["qty"]

    async def play(self) -> dict:
        """Play until the day's offers are used up. Returns the summary."""
        state = await self._call("get", "/math/fortune")
        limit = state["today"]["limit"]
        while True:
            state = await self._call("get", "/math/fortune")
            if state["offer"] is not None:
                await self._play_event()
                continue
            if state["today"]["offers"] >= limit:
                return self.summary
            if self.summary["answers"] >= self.max_answers:
                raise AssertionError("no cơ duyên after %d answers" % self.summary["answers"])
            if await self._practice_once() is not None:
                continue


async def _main(args) -> int:
    import httpx
    sys.path.insert(0, str(ROOT / "server"))
    async with httpx.AsyncClient(base_url=args.url, timeout=30) as c:
        r = await c.post("/auth/register", json={"username": args.user, "password": args.password})
        if r.status_code != 200:
            r = await c.post("/auth/login", json={"username": args.user, "password": args.password})
        r.raise_for_status()
        h = {"Authorization": f"Bearer {r.json()['token']}"}
        bot = FortuneBot(c, h, key_of=sqlite_keys(args.db), seed=args.seed, wrong_rate=args.wrong_rate,
                         decline_rate=args.decline_rate)
        out = await bot.play()
    print({k: v for k, v in out.items() if k != "events"})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--db", required=True, help="the dev server's SQLite file (for the answer key)")
    ap.add_argument("--user", default="co_duyen_bot")
    ap.add_argument("--password", default="secret123")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--wrong-rate", type=float, default=0.3)
    ap.add_argument("--decline-rate", type=float, default=0.0)
    return asyncio.run(_main(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
