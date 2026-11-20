"""Thiên Địa Đồ through the real client: the lands of Luyện Khí (world_plan.json "lands").

  * a newcomer walks into the gate of Thiên Công Phường and is refused: a toast names what
    is missing in Đạo Thụ, and the game does not knock again while they stand in the gate;
  * they walk across Trúc Lâm Thôn to the north-east gate and into Lưu Vân Cốc, a new map;
  * a Vân Xà there strikes, and its card asks Giải Tích, the branch of the land; a right
    answer is a Phản Đòn.

and the weapons lying in the lands (the weapon system: GET /weapons, POST /weapons/claim), on the
real server (test_weapon_spot_flow):

  * a player who finished Luyện Khí tầng 1 walks to the Kiếm Gỗ Hạ Phẩm on its stone tablet at
    the gate of Kiếm Trủng Sơn (its `pos`), presses E: it is in the bag and the spot is gone;
  * a newcomer at the same spot presses E and is told, in Vietnamese, what is still missing.

    python -m client.tests.test_lands_flow <dir>     # numbered screenshots of the flow in <dir>,
                                                     # and land_<id>.png of every land of Luyện Khí
"""
from __future__ import annotations

import datetime as dt
import json
import math
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_combat_flow import CARD, engage, nearest, walk_to, world
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the maps and the plan the server ships

from app.learning import math_tree  # noqa: E402
from app.realtime import maps  # noqa: E402

HUB = "truc_lam_thon"
LOCKED = "thien_cong_phuong"
LAND = "luu_van_coc"
CREATURE = "van_xa"


def zones() -> dict:
    return {k: v for k, v in json.loads((ROOT / "server" / "data" / "zones.json").read_text("utf-8")).items()
            if not k.startswith("_")}


def route_to(drv: Driver, server: ServerProcess, zone: str, tx: float, ty: float, near: float = 12.0,
             timeout: float = 60.0) -> None:
    """Walk to a point over a route that exists on the zone's own collider (the BFS the realm
    bots walk with), answering any card a monster's blow opens on the way."""
    from tests.realm_bot import path as route_over
    col = maps.load(zones()[zone]["map"]).collider
    end = time.time() + timeout
    while time.time() < end:
        if drv.top_is(CARD):
            answer_card(drv, server, correct=True)
            drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes")
            continue
        ws = world(drv)
        if ws.zone_id != zone or math.hypot(tx - ws.player.x, ty - ws.player.y) < near:
            return
        route = route_over(col, (ws.player.x, ws.player.y), (tx, ty))
        if not route:
            raise AssertionError(f"no way to ({tx:.0f}, {ty:.0f}) in {zone}")
        step = 6 if len(route) > 60 else 3          # near the goal: small steps, no corner cut
        for wx, wy in route[step - 1::step] + [(tx, ty)]:
            if drv.top_is(CARD) or world(drv).zone_id != zone:
                break
            walk_to(drv, wx, wy, near=6 if step == 3 else 8, timeout=4)
    ws = world(drv)
    raise AssertionError(f"could not reach ({tx:.0f}, {ty:.0f}) in {zone}: standing at ({ws.player.x:.0f}, "
                         f"{ws.player.y:.0f}); scenes={drv.scene_names()}; toasts={drv.toast_log[-5:]}")


def into_gate(drv: Driver, portal, key: int, seconds: float = 1.5) -> None:
    """Stand at the mouth of a gate, then hold the key that walks through it."""
    drv.hold([key], seconds)
    drv.keys.held = set()


def start(server: ServerProcess, workdir: Path, uid: int, token: str, username: str, shots: Path | None,
          zone: str, x: float, y: float) -> Driver:
    server.sql("update characters set zone_id=?, x=?, y=? where user_id=?", (zone, x, y, uid))
    server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": username,
                                                      "server_url": server.url}))
    drv = Driver(server.url, workdir, shots)
    drv.click("menu_start")
    drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, f"the world ({zone})")
    drv.wait_api()
    return drv


def run_lands_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        token, uid = make_account(server.url, "detu_ld", "Lữ Khách")
        hub = maps.load(HUB)
        sx, sy = hub.spawn("from_thien_cong_phuong")
        drv = start(server, workdir, uid, token, "detu_ld", shots, HUB, sx, sy)
        ws = world(drv)
        assert ws.zone_id == HUB and ws.land_id == HUB, (ws.zone_id, ws.land_id)

        # ---- the door of Thiên Công Phường: refused, with what is missing
        gate = next(a for a in hub.portals if a.props.get("target") == LOCKED)
        walk_to(drv, gate.x + gate.w + 6, gate.y + gate.h / 2, near=6, timeout=6)
        into_gate(drv, gate, pygame.K_a)
        drv.wait(lambda: any(t.startswith("Chưa vào được Thiên Công Phường") for t in drv.toast_log), 8,
                 "the door's refusal")
        why = next(t for t in drv.toast_log if t.startswith("Chưa vào được Thiên Công Phường"))
        assert "tầng 1" in why and "Python nhập môn" in why, why
        drv.step(4)
        drv.shot("land_locked")
        assert world(drv).zone_id == HUB and ws.portal_refused == LOCKED
        n = sum(t.startswith("Chưa vào được") for t in drv.toast_log)
        drv.step(150)                                  # standing in the gate: no knocking again
        assert sum(t.startswith("Chưa vào được") for t in drv.toast_log) == n

        # ---- across the village to the north-east gate, into Lưu Vân Cốc
        gate = next(a for a in hub.portals if a.props.get("target") == LAND)
        route_to(drv, server, HUB, gate.x + gate.w / 2, gate.y + gate.h + 14)
        into_gate(drv, gate, pygame.K_w)
        drv.wait(lambda: world(drv) is not None and world(drv).zone_id == LAND and world(drv).joined, 10,
                 "Lưu Vân Cốc")
        drv.wait_api()
        ws = world(drv)
        assert ws.land_id == LAND and ws.zone_name == "Lưu Vân Cốc", (ws.land_id, ws.zone_name)
        drv.step(10)
        drv.shot("luu_van_coc")

        # ---- a Vân Xà strikes: its card asks Giải Tích, a right answer is a Phản Đòn
        drv.wait(lambda: nearest(ws, CREATURE) is not None, 10, "a Vân Xà")
        m = nearest(ws, CREATURE)                     # the stream winds between: go round by the bridge
        route_to(drv, server, LAND, m.pos[0], m.pos[1], near=30)
        engage(drv, server, CREATURE)
        card = drv.game.top
        assert card.q["context"] == "math_combat" and card.q["math"]["subject"] == "giai_tich", card.q["math"]
        assert card.q["math"].get("land_vi") == "Lưu Vân Cốc", card.q["math"]
        drv.step(4)
        drv.shot("van_xa_question")
        res = answer_card(drv, server, correct=True)
        assert res["combat"]["parry"], res["combat"]
        drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes by itself")
        rows = server.sql("select subject_id, correct from math_answers where user_id=?", (uid,))
        assert rows == [("giai_tich", 1)], rows
        drv.step(3)
        drv.shot("phan_don")
        drv.close()
    finally:
        server.stop()


# ------------------------------------------------------------------ a weapon lying in a land
SPOT = "kiem_1_ha"


def spot_of(ws, sid: str):
    return next((sp for sp in ws.weapon_spots if sp.id == sid), None)


def to_spot(drv: Driver, server: ServerProcess, zone: str, spot) -> None:
    """Walk to just below the spot, then turn to face it (the E target is in front of the feet)."""
    route_to(drv, server, zone, spot.x, spot.y + 14, near=8)
    drv.hold([pygame.K_w], 0.08)
    drv.keys.held = set()
    drv.step(3)


def run_weapon_spot_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        plan_lands = {l["id"]: l for l in math_tree.world_plan()["lands"]}
        zone = next(k for k, v in zones().items() if v.get("land") == "kiem_trung_son")
        placed = next(p for p in math_tree.world_plan()["weapons_placed"]
                      if (p["weapon"], p["quality"]) == ("kiem_1", "ha"))
        assert placed["land"] == "kiem_trung_son" and plan_lands[placed["land"]]["map"] == zones()[zone]["map"]
        spawn = maps.load(zones()[zone]["map"]).spawn("from_village")

        # ---- a player done with Luyện Khí tầng 1: E picks it up
        token, uid = make_account(server.url, "detu_vk1", "Nhặt Kiếm")
        grant_luyen_khi(server, uid, up_to=1)
        drv = start(server, workdir, uid, token, "detu_vk1", shots, zone, *spawn)
        ws = world(drv)
        drv.wait(lambda: spot_of(ws, SPOT) is not None, 10, "the weapon spots of the land")
        sp = spot_of(ws, SPOT)
        assert sp.state == "available" and sp.icon == ("weapons_a", "kiem_1"), sp
        assert ws.land_id == "kiem_trung_son"
        route_to(drv, server, zone, sp.x + 30, sp.y + 10, near=8)     # beside it: the sword in view
        drv.step(10)
        drv.shot("weapon_spot")
        if shots is not None:
            pygame.image.save(drv.game.display.window, str(shots / "land_weapon_spot.png"))
        to_spot(drv, server, zone, sp)
        drv.wait(lambda: ws.target is not None and ws.target[0] == "weapon" and ws.target[1].id == SPOT, 5,
                 "the weapon as the target")
        n = len(drv.toast_log)
        drv.press(pygame.K_e)
        drv.wait(lambda: any(t.startswith("Đã nhặt") for t in drv.toast_log[n:]), 6, "the weapon picked up")
        drv.wait_api()
        rows = server.sql("select item_id, rarity from equipment_instances where user_id=?", (uid,))
        assert rows and rows[0][0] == "kiem_1", rows
        assert server.sql("select placed_id from weapon_claims where user_id=?", (uid,)) == [(SPOT,)]
        drv.wait(lambda: spot_of(ws, SPOT) is not None and spot_of(ws, SPOT).state == "taken", 6,
                 "the spot taken after the reload")
        drv.step(3)
        assert ws.target is None or ws.target[0] != "weapon", "a taken weapon is no target"
        assert not any(d[1] is not None and d[0] == sp.y for d in ws.weapon_drawables(ws.view)), "and is not drawn"
        drv.shot("weapon_picked_up")
        # the bag: the sword is there
        got = {}
        drv.game.api.get("/inventory", lambda r: got.update(r), lambda e: got.update(err=e))
        drv.wait(lambda: got, 5, "the bag")
        items = [e.get("item_id") for e in got.get("equipment", [])]
        assert "kiem_1" in items, got.keys()
        drv.close()

        # ---- a newcomer: the spot is there for them, locked, and E says what is missing
        token, uid = make_account(server.url, "detu_vk0", "Tân Thủ")
        drv = start(server, workdir, uid, token, "detu_vk0", shots, zone, *spawn)
        ws = world(drv)
        assert ws.land_id == "kiem_trung_son"
        drv.wait(lambda: spot_of(ws, SPOT) is not None, 10, "the weapon spots of the land")
        sp = spot_of(ws, SPOT)
        assert (sp.tx, sp.ty) == tuple(placed["pos"]) and sp.state == "locked" and sp.reason_vi, sp
        to_spot(drv, server, zone, sp)
        drv.wait(lambda: ws.target is not None and ws.target[0] == "weapon" and ws.target[1].id == SPOT, 5,
                 "the weapon as the target")
        n = len(drv.toast_log)
        drv.press(pygame.K_e)
        drv.wait(lambda: len(drv.toast_log) > n, 5, "the reason")
        why = drv.toast_log[-1]
        assert why == sp.reason_vi and "Luyện Khí tầng 1" in why and "Tập hợp và ánh xạ" in why, why
        assert not server.sql("select 1 from equipment_instances where user_id=?", (uid,))
        drv.step(4)
        drv.shot("weapon_locked")
        drv.close()
    finally:
        server.stop()


# ------------------------------------------------------------------ the tour (screenshots only)
SCENIC = {   # land -> a tile to stand on for its picture
    "kiem_trung_son": (44, 13), "luu_van_coc": (27, 21), "van_tuong_trach": (30, 16),
    "me_do_lam": (50, 12), "thien_cong_phuong": (12, 7), "linh_xa_nguyen": (40, 18),
    "loi_kiep_dai": (20, 22),
}


def grant_luyen_khi(server: ServerProcess, uid: int, up_to: int | None = None) -> None:
    """Every part of Đạo Thụ passed and every exercise solved: the whole of Luyện Khí done, or
    (`up_to`) only its main-path nodes of that stage and below."""
    from app.learning import math_problems
    from app.systems import math_tree_progress
    t = math_tree.tree()

    def wanted(node_id) -> bool:
        n = t.nodes.get(node_id)
        return up_to is None or (n is not None and n.main and n.realm == "luyen_khi" and (n.stage or 99) <= up_to)
    now = dt.datetime(2026, 11, 20, 8).isoformat(sep=" ")
    for part in math_tree_progress.all_parts():
        if not wanted(part.node_id):
            continue
        server.sql("insert into math_runs(user_id, subject_id, node_id, floor, mode, tier, correct_streak, "
                   "wrong_streak, combo, best_combo, asked, correct, review_asked, xp_gained, ladders, passed, "
                   "started_at, ended_at) values (?, ?, ?, ?, 'trial', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ?, ?)",
                   (uid, part.subject_id, part.node_id, part.floor, now, now))
    bank = math_problems.bank()
    for node in t.nodes.values():
        if not wanted(node.id):
            continue
        for pid in node.problems:
            p = bank.get(pid)
            server.sql("insert into math_submissions(user_id, problem_id, subject_id, floor, tier, verdict, "
                       "passed, total, ms, xp_gained, code, created_at, judged_at) "
                       "values (?, ?, ?, ?, 1, 'AC', 1, 1, 1, 0, '', ?, ?)",
                       (uid, pid, p.subject if p else "", p.floor if p else 1, now, now))


def tour_lands(workdir: Path, out: Path) -> list[Path]:
    """A player who finished Luyện Khí stands in every land in turn: art/preview/land_<id>.png.
    One player per land (a character that just left lingers where it was for a while), and a
    fresh server every four lands (a server lets five accounts a day come from one address)."""
    built = [l for l in math_tree.world_plan()["lands"] if l["status"] == "co" and l["kind"] != "hub"]
    saved = []
    for n in range(0, len(built), 4):
        sub = workdir / f"server_{n}"
        sub.mkdir(parents=True, exist_ok=True)
        saved += _tour(sub, out, built[n:n + 4], n)
    return saved


def _tour(workdir: Path, out: Path, built: list[dict], first: int) -> list[Path]:
    server = ServerProcess(workdir)
    saved = []
    try:
        z = zones()
        for i, land in enumerate(built, start=first):
            user = f"du_lam_{i}"
            token, uid = make_account(server.url, user, f"Du Lãm {i}")
            grant_luyen_khi(server, uid)
            server.sql("update characters set realm='luyen_khi', realm_stage=9 where user_id=?", (uid,))
            zid = next(k for k, v in z.items() if v.get("land") == land["id"])
            tx, ty = SCENIC[land["id"]]
            drv = start(server, workdir, uid, token, user, None, zid, tx * 16 + 8, ty * 16 + 12)
            ws = world(drv)
            assert ws.zone_id == zid, (zid, drv.toast_log[-3:])
            if drv.top_is(CARD):
                answer_card(drv, server, correct=True)
            drv.step(40)
            out.mkdir(parents=True, exist_ok=True)
            p = out / f"land_{land['id']}.png"
            pygame.image.save(drv.game.display.window, str(p))
            saved.append(p)
            drv.close()
    finally:
        server.stop()
    return saved


def test_lands_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_lands_") as tmp:
        run_lands_flow(Path(tmp))


def test_weapon_spot_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_weapon_spot_") as tmp:
        run_weapon_spot_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "lands"
    with tempfile.TemporaryDirectory() as tmp:
        run_lands_flow(Path(tmp), out)
    with tempfile.TemporaryDirectory() as tmp:
        run_weapon_spot_flow(Path(tmp), out)
    with tempfile.TemporaryDirectory() as tmp:
        for p in tour_lands(Path(tmp), out):
            print("saved", p)
    print("screenshots in", out)
