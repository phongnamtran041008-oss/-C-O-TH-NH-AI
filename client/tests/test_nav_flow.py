"""Chỉ Đường through the real client and a real server (docs/CHI_DUONG.md):

  * a newcomer in Trúc Lâm Thôn presses N: the picker asks the server where to go and offers
    "Khu hợp tu vi: Kiếm Trủng Sơn" first; choosing it puts the arrow round the player;
  * following nothing but the arrow (the test turns its direction into held keys, as a player
    would), they walk across the village, through the north gate, into Kiếm Trủng Sơn, and are
    told "Đã tới Kiếm Trủng Sơn.";
  * H there: the arrow leads back through the gate to the village and on to the gate of the
    Động Phủ ("Đã tới cổng Động Phủ..."); one step and they are home;
  * in the abode N, "Về Trúc Lâm Thôn": the arrow leads to the abode's gate, E, and on to the
    middle of the village;
  * M opens Thiên Địa Đồ (this zone, then the world); a khu walked into shows its banner (the
    khu are added to the client's map by the test: no map has khu yet).

    python -m client.tests.test_nav_flow <dir>     # numbered screenshots of the flow in <dir>
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.engine import chi_duong
from client.engine.tilemap import MapObject
from client.tests.driver import Driver, ServerProcess
from client.tests.test_combat_flow import CARD
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_world_flow import make_account

HUB = "truc_lam_thon"
LAND = "loan_so_coc"


def here(drv: Driver):
    """The world or abode scene at the bottom of the stack."""
    return next((s for s in drv.game.scenes if type(s).__name__ in ("WorldScene", "AbodeScene")), None)


def nav(drv: Driver) -> chi_duong.ChiDuong:
    return chi_duong.of(drv.game)


def follow_arrow(drv: Driver, server: ServerProcess, done, what: str, timeout: float = 90.0,
                 on_exit=None) -> None:
    """Walk where the arrow points until `done()`: its direction (the aim of the last reading)
    becomes held keys, a tenth of a second at a time."""
    end = time.time() + timeout
    while time.time() < end:
        if done():
            drv.keys.held = set()
            drv.step(3)
            return
        if drv.top_is(CARD):
            answer_card(drv, server, correct=True)
            drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes")
            continue
        sc = here(drv)
        n = nav(drv)
        if sc is None or n.reading is None or getattr(sc, "waiting_zone", None) is not None \
                or not getattr(sc, "joined", True):
            drv.keys.held = set()
            drv.step(2)
            continue
        if n.status == "exit" and on_exit is not None:
            drv.keys.held = set()
            on_exit(sc)
            continue
        ax, ay = n.reading.aim
        dx, dy = ax - sc.player.x, ay - sc.player.y
        keys = set()
        if abs(dx) > 2:
            keys.add(pygame.K_d if dx > 0 else pygame.K_a)
        if abs(dy) > 2:
            keys.add(pygame.K_s if dy > 0 else pygame.K_w)
        if not keys:
            drv.step(2)
            continue
        drv.hold(list(keys), 0.1)
    sc = here(drv)
    raise AssertionError(f"the arrow did not lead to {what}: in {getattr(sc, 'zone_id', type(sc).__name__)} at "
                         f"({sc.player.x:.0f}, {sc.player.y:.0f}), status {nav(drv).status}, "
                         f"toasts {drv.toast_log[-6:]}")


def start(server: ServerProcess, workdir: Path, shots: Path | None, name: str) -> tuple[Driver, int]:
    token, uid = make_account(server.url, name, "Lữ Khách")
    server.sql("update characters set zone_id=?, x=?, y=? where user_id=?", (HUB, 448.0, 336.0, uid))
    server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": name, "server_url": server.url}))
    drv = Driver(server.url, workdir, shots)
    drv.click("menu_start")
    drv.wait(lambda: here(drv) is not None and getattr(here(drv), "joined", False), 15, "the village")
    drv.wait_api()
    return drv, uid


def fake_khu(tmap, x, y, w, h, kid, name, band, lo, hi):
    """A khu object as the giant maps will declare it (realtime/dia_do.py)."""
    props = {"khu": kid, "name_vi": name, "band": str(band), "stage_min": str(lo), "stage_max": str(hi),
             "anchor_x": str(int(x + w / 2)), "anchor_y": str(int(y + h / 2)), "realm": "luyen_khi"}
    tmap.objects.append(MapObject(90000 + len(tmap.objects), name, "khu", x, y, w, h, props))
    tmap.__dict__.pop("_nav_khu", None)
    tmap._index()                     # the map looks its objects up by type: index the new one


def run_nav_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        drv, uid = start(server, workdir, shots, "detu_cd")
        ws = here(drv)
        assert ws.zone_id == HUB
        drv.step(10)
        drv.shot("village_minimap")

        # ---- N: the picker, the server's recommendation first
        drv.press(pygame.K_n)
        drv.wait_scene("NavPicker")
        drv.wait(lambda: nav(drv).data is not None and drv.has("nav_pick_rec"), 10, "the destinations")
        rec = nav(drv).data["recommended"]
        assert rec["zone"] == LAND and rec["land_vi"] == "Kiếm Trủng Sơn", rec
        assert drv.has("nav_pick_home") and drv.has("nav_pick_village") and drv.has("nav_lock_thien_cong_phuong")
        drv.shot("picker")
        drv.click("nav_pick_rec")
        drv.wait(lambda: not drv.top_is("NavPicker") and nav(drv).dest is not None, 5, "the arrow set")
        assert any(t.startswith("Chỉ Đường: tới Kiếm Trủng Sơn") for t in drv.toast_log), drv.toast_log[-3:]
        drv.wait(lambda: nav(drv).status == "path", 10, "the way through the village")
        assert nav(drv).gates and nav(drv).gates[0].target == LAND
        drv.step(20)
        drv.shot("arrow_village")

        # ---- M: Thiên Địa Đồ of the village, then the world
        drv.press(pygame.K_m)
        drv.wait_scene("WorldMapScene")
        drv.step(4)
        drv.shot("map_zone")
        drv.press(pygame.K_TAB)
        drv.step(4)
        assert drv.game.top.view == "world" and drv.has("map_land_loan_so_coc")
        drv.shot("map_world")
        drv.click("map_land_luu_van_coc")           # a land chosen on the map sets the arrow
        drv.wait(lambda: drv.top_is("WorldScene") and (nav(drv).dest or {}).get("zone") == "luu_van_coc", 5,
                 "the arrow to Lưu Vân Cốc")
        drv.press(pygame.K_n)                       # and back to the recommendation
        drv.wait(lambda: drv.has("nav_pick_rec"), 10, "the picker")
        drv.click("nav_pick_rec")
        drv.wait(lambda: (nav(drv).dest or {}).get("zone") == LAND, 5, "the arrow to Kiếm Trủng Sơn again")

        # ---- follow the arrow into Kiếm Trủng Sơn
        follow_arrow(drv, server, lambda: here(drv).zone_id == LAND and nav(drv).dest is None, "Kiếm Trủng Sơn")
        assert "Đã tới Kiếm Trủng Sơn." in drv.toast_log, drv.toast_log[-5:]
        drv.wait(lambda: here(drv).joined, 10, "the land joined")
        drv.step(6)
        drv.shot("arrived_land")

        # ---- a khu (added to the client's map) shows its banner, warning above the tu vi
        ws = here(drv)
        px, py = ws.player.x, ws.player.y
        fake_khu(ws.map, px - 200, py - 400, 400, 330, "kts_test_trung", "Trung Vực Kiếm Mộ", 2, 4, 6)
        fake_khu(ws.map, px - 200, py - 70, 400, 140, "kts_test_ngoai", "Ngoại Vi Kiếm Trủng", 1, 1, 3)
        drv.wait(lambda: nav(drv).banner is not None and nav(drv).banner[3] is not None, 8, "the khu banner")
        b = nav(drv).banner
        assert b[0].startswith("Ngoại Vi Kiếm Trủng") and "tầng 1-3" in b[1] and not b[2], b
        drv.shot("khu_banner")
        drv.press(pygame.K_m)                       # the khu on the big map, tinted by band
        drv.wait_scene("WorldMapScene")
        drv.step(4)
        drv.shot("map_zone_khu")
        pic, mx, my, k = drv.game.top.zone_layout()             # a khu chosen on the map sets the arrow
        drv.click_at(drv.game.display.to_window(mx + (px + 100) * k, my + (py - 300) * k))
        drv.wait(lambda: drv.top_is("WorldScene") and (nav(drv).dest or {}).get("khu") == "kts_test_trung", 5,
                 "the arrow to the khu")
        drv.wait(lambda: nav(drv).status == "path", 10, "the way to the khu")
        drv.press(pygame.K_n)
        drv.wait(lambda: drv.has("nav_off"), 10, "the picker")
        drv.click("nav_off")                                    # Tắt chỉ đường
        drv.wait(lambda: nav(drv).dest is None and "Đã tắt chỉ đường." in drv.toast_log, 5, "the arrow off")
        ws.map.objects[:] = [o for o in ws.map.objects if o.type != "khu"]
        fake_khu(ws.map, px - 150, py - 60, 300, 120, "kts_test_tham", "Thâm Xứ Kiếm Mộ", 3, 7, 9)
        # a khu above the player's tu vi: a warning
        drv.wait(lambda: nav(drv).banner is not None and nav(drv).banner[3] is not None
                 and "Thâm Xứ" in nav(drv).banner[0], 8, "the warning banner")
        b = nav(drv).banner
        assert b[2] and "cao hơn tu vi" in b[1], b
        drv.shot("khu_banner_warn")
        ws.map.objects[:] = [o for o in ws.map.objects if o.type != "khu"]
        ws.map.__dict__.pop("_nav_khu", None)
        ws.map._index()
        drv.step(4)

        # ---- H: home, through the gate and across the village to the gate of the abode
        drv.press(pygame.K_h)
        drv.wait(lambda: nav(drv).dest is not None and nav(drv).status == "path", 10, "the way home")
        drv.step(10)
        drv.shot("arrow_home")
        follow_arrow(drv, server, lambda: nav(drv).dest is None and here(drv).zone_id == HUB, "the abode gate")
        assert any(t.startswith("Đã tới cổng Động Phủ") for t in drv.toast_log), drv.toast_log[-5:]
        drv.step(4)
        drv.shot("at_abode_gate")
        drv.hold([pygame.K_s], 1.2)                 # the step home is the player's own
        drv.wait(lambda: drv.top_is("AbodeScene"), 10, "the abode")
        drv.wait_api()

        # ---- out again: N, "Về Trúc Lâm Thôn", E at the gate, on to the village centre
        drv.step(10)
        drv.press(pygame.K_n)
        drv.wait_scene("NavPicker")
        drv.wait(lambda: drv.has("nav_pick_village"), 10, "the picker in the abode")
        drv.shot("picker_abode")
        drv.click("nav_pick_village")
        drv.wait(lambda: nav(drv).status in ("path", "exit"), 10, "the way to the abode's gate")
        drv.step(6)
        drv.shot("arrow_abode")

        def press_e(sc):
            if sc.target is not None and sc.target[1].props.get("action") == "exit":
                drv.press(pygame.K_e)
                drv.wait(lambda: here(drv) is not None and type(here(drv)).__name__ == "WorldScene", 10, "the village")
            else:                                   # face the gate
                drv.hold([pygame.K_s], 0.1)

        follow_arrow(drv, server, lambda: nav(drv).dest is None and getattr(here(drv), "zone_id", None) == HUB,
                     "the village centre", on_exit=press_e)
        assert "Đã tới Trúc Lâm Thôn." in drv.toast_log, drv.toast_log[-5:]
        drv.shot("arrived_village")
        drv.close()
    finally:
        server.stop()


def test_nav_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_nav_") as tmp:
        run_nav_flow(Path(tmp))


def test_a_giant_land_is_led_through_in_the_real_ui():
    """A synthetic 320 x 240 tile land with khu (client/tests/nav_giant.py), drawn by the real
    game loop: the way is found within a few frames of 3 ms, the minimap is a window, the khu
    walked into shows its banner."""
    from client.tests.nav_giant import run_giant_screens
    with tempfile.TemporaryDirectory(prefix="kvtt_nav_giant_") as tmp:
        out = run_giant_screens(Path(tmp))
    assert out["status"] == "path" and out["route"] > 20, out
    assert out["frames"] < 200, out
    assert out["banner"] is not None and out["banner"][0] == "Trung Vực" and "tầng 4-6" in out["banner"][1]


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "nav"
    with tempfile.TemporaryDirectory() as tmp:
        run_nav_flow(Path(tmp), out)
    from client.tests.nav_giant import run_giant_screens
    with tempfile.TemporaryDirectory() as tmp:
        facts = run_giant_screens(Path(tmp), out)
    print("giant land:", {k: v for k, v in facts.items() if k != "banner"})
    print("screenshots in", out)
