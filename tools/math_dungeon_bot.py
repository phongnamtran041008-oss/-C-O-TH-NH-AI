#!/usr/bin/env python3
"""A bot that plays whole hầm ngục (M10) through the public API, the way the game does:
POST /math/dungeon/start, then /math/dungeon/next and POST /quiz/answer until the run ends,
then GET /math/dungeon/run/<id> for the final numbers. `--wrong-rate` makes it miss that
share of its questions, so it also loses runs.

    # next to a local server (the bot reads the answer keys from its database file):
    #   cd server && ALLOW_UNREVIEWED=1 python -m uvicorn app.main:app --port 8000
    python tools/math_dungeon_bot.py --url http://127.0.0.1:8000 --db server/dev.db --runs 5 --wrong-rate 0.3

Like tools/realm_bots.py it knows the answers by reading them from the server's database (a
stand-in for a player who knows the maths), so against a live server it only works next to
it. In-process, a test hands it an httpx client on the ASGI app and its own key reader
(server/tests/test_math_dungeon.py).
"""
from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import random
import sqlite3
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOOK = {"hair_color": "#2B2B2B", "hair_style": "ngan", "body": "nam"}
MAX_STEPS = 200          # far above the longest run the data allows; a run that goes on longer is a bug


class BotError(RuntimeError):
    pass


def right_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "true_false":
        return {"value": key["value"]}
    if q["qtype"] == "multiple_choice":
        return {"option": key["option"]}
    if q["qtype"] == "matching":
        return {"pairs": list(key["pairs"])}
    if q["qtype"] == "ordering":
        return {"order": list(key["order"])}
    return {"text": ", ".join(key["numbers"])}


def wrong_answer(q: dict, key: dict) -> dict:
    if q["qtype"] == "true_false":
        return {"value": not key["value"]}
    if q["qtype"] == "multiple_choice":
        return {"option": next(o["id"] for o in q["options"] if o["id"] != key["option"])}
    if q["qtype"] in ("matching", "ordering"):          # rotated: every entry in the wrong place
        name = "pairs" if q["qtype"] == "matching" else "order"
        return {name: key[name][1:] + key[name][:1]}
    return {"text": "987654"}


async def _call(client, method: str, path: str, headers: dict, body: dict | None = None) -> dict:
    r = await (client.get(path, headers=headers) if method == "GET"
               else client.post(path, json=body or {}, headers=headers))
    if r.status_code != 200:
        raise BotError(f"{method} {path} -> {r.status_code}: {r.text}")
    return r.json()


async def play_dungeon(client, headers: dict, keyfn, *, seed: int | None = None, floor: int | None = None,
                       wrong_rate: float = 0.0, rng: random.Random | None = None) -> dict:
    """Play one dungeon to its end. `keyfn(session_id)` returns the answer key (sync or async).

    Returns {"start": the run as started, "run": the final run, "steps": one entry per answer
    with the question's type/tier/room and the `dungeon` block of the result, "xp": Tu Vi the
    answers reported}. Raises BotError if the server refuses anything or the run never ends."""
    rng = rng or random.Random()
    body = {k: v for k, v in (("seed", seed), ("floor", floor)) if v is not None}
    start = (await _call(client, "POST", "/math/dungeon/start", headers, body))["run"]
    run_id = start["run_id"]
    steps, xp = [], 0
    for _ in range(MAX_STEPS):
        nxt = await _call(client, "POST", "/math/dungeon/next", headers, {"run_id": run_id})
        q = nxt["question"]
        if q is None:
            break
        key = keyfn(q["session_id"])
        if inspect.isawaitable(key):
            key = await key
        good = rng.random() >= wrong_rate
        res = await _call(client, "POST", "/quiz/answer", headers,
                          {"session_id": q["session_id"], "answer": right_answer(q, key) if good else wrong_answer(q, key)})
        if res["correct"] != good:
            raise BotError(f"meant to answer {'right' if good else 'wrong'}, graded {res['correct']}: {q['qtype']}")
        xp += (res.get("xp") or {}).get("gained", 0)
        steps.append({"qtype": q["qtype"], "tier": q["math"]["tier"], "skill": q["math"]["skill"],
                      "floor": q["math"]["floor"], "room": q["math"]["dungeon"]["room"], "correct": good,
                      "dungeon": res["dungeon"]})
        if res["dungeon"]["run"]["ended"]:
            break
    else:
        raise BotError(f"run {run_id} did not end in {MAX_STEPS} answers")
    final = (await _call(client, "GET", f"/math/dungeon/run/{run_id}", headers))["run"]
    if not final["ended"] or final["state"] not in ("cleared", "failed"):
        raise BotError(f"run {run_id} ended as {final['state']}")
    return {"start": start, "run": final, "steps": steps, "xp": xp}


# ------------------------------------------------------------------ against a live server
def sqlite_keys(db: Path):
    def key(session_id: str) -> dict:
        con = sqlite3.connect(db)
        try:
            row = con.execute("select answer_key from quiz_sessions where id=?", (session_id,)).fetchone()
        finally:
            con.close()
        if row is None:
            raise BotError(f"no quiz session {session_id} in {db}")
        return json.loads(row[0])
    return key


async def main_async(args) -> int:
    import httpx
    rng = random.Random(args.rng_seed)
    async with httpx.AsyncClient(base_url=args.url, timeout=30) as client:
        name = args.username or f"hamnguc_{uuid.uuid4().hex[:8]}"
        r = await client.post("/auth/register", json={"username": name, "password": args.password})
        if r.status_code != 200:
            r = await client.post("/auth/login", json={"username": name, "password": args.password})
        if r.status_code != 200:
            print(f"cannot sign in as {name}: {r.text}", file=sys.stderr)
            return 2
        headers = {"Authorization": f"Bearer {r.json()['token']}"}
        # Tu Vi needs a character; an account that already has one just says so
        await client.post("/character/create", json={"display_name": name.replace("_", " "), "appearance": LOOK},
                          headers=headers)
        keyfn = sqlite_keys(Path(args.db))
        bad = 0
        for n in range(args.runs):
            seed = args.seed + n if args.seed is not None else None
            try:
                out = await play_dungeon(client, headers, keyfn, seed=seed, floor=args.floor,
                                         wrong_rate=args.wrong_rate, rng=rng)
            except BotError as e:
                bad += 1
                print(f"run {n + 1}: FAILED {e}")
                continue
            run = out["run"]
            items = ", ".join(f"{i['name_vi']} x{i['qty']}" for i in run["items_gained"]) or "-"
            print(f"run {n + 1}: seed {run['seed']} floor {run['floor']} -> {run['state']}, "
                  f"rooms {run['rooms_cleared']}/{run['total_rooms']}, {run['correct']}/{run['asked']} right, "
                  f"hearts {run['hearts']}/{run['max_hearts']}, Tu Vi {run['xp_gained']}, "
                  f"Linh Thạch {run['stones_gained']}, {items}")
        return 1 if bad else 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--db", default=str(ROOT / "server" / "dev.db"), help="the server's SQLite file (answer keys)")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--seed", type=int, default=None, help="first seed (then +1 per run); default: the server draws")
    ap.add_argument("--floor", type=int, default=None, help="default: the player's own floor")
    ap.add_argument("--wrong-rate", type=float, default=0.0)
    ap.add_argument("--username", default=None)
    ap.add_argument("--password", default="bot-secret-123")
    ap.add_argument("--rng-seed", type=int, default=None)
    return asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
