"""Thủ Thành Toán client pieces without a server: the board runs the server's own simulation,
a log played on the client replays to the same end, the board draws and places a tower only
after its question, and the Cổng Thủ Thành in the village opens the math tower defence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from client.engine import td_sim

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def params(seed: int = 4) -> dict:
    """Like the server's math_td.build_params, from the data files (the client tests never
    import the server package), with every tower of the data open."""
    data = ROOT / "server" / "data"
    c = json.loads((data / "balance" / "td.json").read_text("utf-8"))
    d = json.loads((data / "math" / "td.json").read_text("utf-8"))
    lv = d["levels"][0]
    towers = {t["id"]: {"role": t["role"], "label": t["label"], "name_vi": t["name_vi"], "power": float(t["power"])}
              for t in d["towers"]}
    return {"level": lv["id"], "cols": d["grid"]["cols"], "rows": d["grid"]["rows"], "path": lv["path"],
            "rocks": lv.get("rocks", []), "core_hp": d["core_hp"], "qi": d["qi"], "upgrade": d["upgrade"],
            "sell_refund": d["sell_refund"], "roles": d["roles"], "monsters": c["monsters"],
            "boss_stun_mult": c["boss_stun_mult"], "wave_max_seconds": c["wave_max_seconds"], "plants": towers,
            "seed": seed, "waves": lv["waves"], "hp_mult": 1.0}


def test_board_runs_the_servers_simulation():
    assert (ROOT / "client" / "engine" / "td_sim.py").read_bytes() == \
        (ROOT / "server" / "app" / "systems" / "td_sim.py").read_bytes()


def test_a_log_played_on_the_client_replays_to_the_same_end():
    import math_td_bot
    p = params()
    sim, answers, events = math_td_bot.play(td_sim, p, accuracy=0.9, seed=2)
    again = td_sim.replay(json.loads(json.dumps(p)), answers, json.loads(json.dumps(events)))
    assert again.summary() == sim.summary() and sim.phase in (td_sim.WON, td_sim.LOST) and sim.plants


def game_without_server(tmp_path):
    from client.config import Config, Session
    from client.main import Game
    game = Game(Config(server_url="http://127.0.0.1:9"), Session(tmp_path / "s.json"), size=(960, 540))
    asked = []
    game.api.post = lambda path, body, *a, **k: asked.append((path, body))     # no server
    game.api.get = lambda *a, **k: None
    return game, asked


def test_board_draws_and_a_tower_needs_its_answer(tmp_path):
    from client.scenes.math_td import MathTdPlayScene
    from client.scenes.td import monster_frames
    game, asked = game_without_server(tmp_path)
    run = {"run_id": "r", "params": params(), "max_speed": 2, "name_vi": "Thử", "monsters": [], "towers": []}
    sc = game.push(MathTdPlayScene(game, run, None))
    assert asked[-1] == ("/math/td/question", {"run_id": "r", "kind": "break"})   # the break questions first
    sc.busy = False
    tower = next(w for w, d in run["params"]["plants"].items() if d["role"] == "hoa")
    path = {tuple(c) for c in run["params"]["path"]}
    cell = next((x, y) for y in range(7) for x in range(12) if (x, y) not in path and [x, y] not in run["params"]["rocks"])
    sc.card = tower
    sc.place(*cell)
    assert asked[-1] == ("/math/td/question", {"run_id": "r", "kind": "place", "tower_id": tower})
    assert cell not in sc.sim.plants and sc.busy                     # nothing stands before the answer
    q = {"session_id": "s1", "math_td": {"power": 1.25}}
    sc.answered(q, "place", tower, cell, {"correct": False})
    assert cell not in sc.sim.plants and sc.events[-1]["k"] == "place"   # wrong: the Linh Khí is spent, no tower
    sc.answered({**q, "session_id": "s2"}, "place", tower, cell, {"correct": True})
    assert sc.sim.plants[cell].mult == 1.25 and sc.events[-1] == {"s": 0, "k": "place", "x": cell[0], "y": cell[1],
                                                                  "w": tower, "q": "s2"}
    sc.start_wave()
    for _ in range(80):
        game.step(0.05, [])
    assert sc.sim.step_n > 0 and sc.sim.monsters
    for kind in run["params"]["monsters"]:
        assert monster_frames(kind)
    game.api.close()      # (not shutdown(): it quits pygame for the tests that follow)


def test_the_village_gate_opens_the_math_tower_defence(tmp_path):
    from client.scenes.math_td import MathTdScene
    from client.scenes.world import WorldScene
    game, asked = game_without_server(tmp_path)
    game.state.me = {"met_td": True}
    gate = type("Obj", (), {"type": "interact", "props": {"action": "td"}})()
    stub = type("W", (), {"game": game, "talking_to": None, "action_of": lambda self, t: "td"})()
    WorldScene.interact(stub, ("object", gate))
    assert isinstance(game.top, MathTdScene)
    game.api.close()
