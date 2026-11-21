"""Chỉ Đường through the real client and a real server, on the real giant lands
(docs/CHI_DUONG.md):

  * a newcomer in Trúc Lâm Thôn presses N: the picker asks the server where to go and offers
    "Khu hợp tu vi: <a khu of band 1> · Kiếm Trủng Sơn" first, the khu read from the land's own
    map; choosing it puts the arrow round the player;
  * M: Thiên Địa Đồ of the village, then "Thiên hạ" (the toast keeps off the lands' boxes);
  * following nothing but the arrow (the test turns its direction into held keys, as a player
    would), they cross the village, go through the north gate, walk the camp at the gate (its
    banner: "nơi an toàn") into the khu of band 1 (its banner: "hợp Luyện Khí tầng 1-3") and on to
    the khu's anchor: "Đã tới <khu> (Kiếm Trủng Sơn).";
  * M on the giant land: "Vùng này" with every khu of the map; a khu of band 2 is picked there and
    the arrow followed into it: the banner warns "cao hơn tu vi của con";
  * H from deep inside the land: the arrow leads back to the gate, across the village to the gate
    of the Động Phủ; one step and they are home; in the abode N, "Về Trúc Lâm Thôn": E at the
    abode's gate and on to the middle of the village;
  * a second newcomer is led from the gate of Lưu Vân Cốc to a khu picked on its big map.

    python -m client.tests.test_nav_flow <dir>     # numbered screenshots of the flow in <dir>
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.engine import chi_duong
from client.engine.tilemap import load_map
from client.tests.driver import Driver, ServerProcess
from client.tests.nav_walk import keys_for
from client.tests.test_combat_flow import CARD
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_world_flow import make_account

HUB = "truc_lam_thon"
LAND = "loan_so_coc"
LAND2 = "luu_van_coc"
KEYS = {(1, 0): [pygame.K_d], (-1, 0): [pygame.K_a], (0, 1): [pygame.K_s], (0, -1): [pygame.K_w]}


def here(drv: Driver):
    """The world or abode scene at the bottom of the stack."""
    return next((s for s in drv.game.scenes if type(s).__name__ in ("WorldScene", "AbodeScene")), None)


def nav(drv: Driver) -> chi_duong.ChiDuong:
    return chi_duong.of(drv.game)


def khu_list(zone: str) -> list[tuple]:
    """(rect, props) of every khu of a land, read from the client's copy of its map."""
    return chi_duong.khu_objects(load_map(zone))


class Walk:
    """What a walk saw: the khu banners shown (title, line, warn), and the screenshots taken on
    the way (`shoot`: a picture when a new khu begins, by water, and every `every` seconds)."""

    def __init__(self, drv: Driver, tag: str = "", every: float = 0.0):
        self.drv, self.tag, self.every = drv, tag, every
        self.banners: list[tuple] = []
        self.last_shot = time.time()
        self.wet = False
        self.n = 0

    def look(self, sc) -> None:
        b = nav(self.drv).banner
        if b is not None and (not self.banners or self.banners[-1][:3] != b[:3]):
            self.banners.append(b[:3])
            if self.drv.shots:
                self.drv.step(3)
                self.drv.shot(f"{self.tag}khu_{len(self.banners)}")
        if not self.drv.shots or not hasattr(sc, "zone_id") or sc.zone_id == HUB:
            return
        tm = sc.map
        tx, ty = int(sc.player.x // tm.tw), int(sc.player.y // tm.th)
        near_water = any(tm.ground[y * tm.w + x] == tm._water_gid
                         for y in range(max(0, ty - 2), min(tm.h, ty + 3))
                         for x in range(max(0, tx - 2), min(tm.w, tx + 3)))
        if near_water and not self.wet:
            self.drv.shot(f"{self.tag}by_water")
        self.wet = near_water
        if self.every and time.time() - self.last_shot > self.every:
            self.last_shot = time.time()
            self.n += 1
            self.drv.shot(f"{self.tag}walk_{self.n}")


def follow_arrow(drv: Driver, server: ServerProcess, done, what: str, timeout: float = 120.0,
                 on_exit=None, walk: Walk | None = None) -> None:
    """Walk where the arrow points until `done()`: its direction (the aim of the last reading)
    becomes held keys - the nearest of the eight directions, as a player reads an arrow - a
    tenth of a second at a time."""
    end = time.time() + timeout
    lean, last = False, None
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
                or not getattr(sc, "joined", True) or drv.game.top is not sc:
            drv.keys.held = set()
            drv.step(2)
            continue
        if walk is not None:
            walk.look(sc)
        if n.status == "exit" and on_exit is not None:
            drv.keys.held = set()
            on_exit(sc)
            continue
        ax, ay = n.reading.aim
        kx, ky = keys_for(ax - sc.player.x, ay - sc.player.y, lean=lean)
        keys = KEYS.get((kx, 0), []) + KEYS.get((0, ky), [])
        if not keys:
            drv.step(2)
            continue
        last = (sc, sc.player.x, sc.player.y)
        drv.hold(keys, 0.1)
        lean = last == (here(drv), sc.player.x, sc.player.y)    # held against a corner: lean as the arrow does
    sc = here(drv)
    raise AssertionError(f"the arrow did not lead to {what}: in {getattr(sc, 'zone_id', type(sc).__name__)} at "
                         f"({sc.player.x:.0f}, {sc.player.y:.0f}), status {nav(drv).status}, "
                         f"toasts {drv.toast_log[-6:]}")


def start(server: ServerProcess, workdir: Path, shots: Path | None, name: str, zone: str = HUB,
          spawn: str = "spawn") -> tuple[Driver, int]:
    token, uid = make_account(server.url, name, "Lữ Khách")
    x, y = next((o.x, o.y) for o in load_map(zone).find("spawn") if o.name == spawn)
    server.sql("update characters set zone_id=?, x=?, y=? where user_id=?", (zone, x, y, uid))
    server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": name, "server_url": server.url}))
    drv = Driver(server.url, workdir, shots)
    drv.click("menu_start")
    drv.wait(lambda: here(drv) is not None and getattr(here(drv), "joined", False), 15, "the world")
    drv.wait_api()
    return drv, uid


def open_big_map(drv: Driver):
    drv.press(pygame.K_m)
    drv.wait_scene("WorldMapScene")
    drv.step(4)
    return drv.game.top


def click_khu(drv: Driver, kid: str, zone: str) -> None:
    """Click a khu on the big map ("Vùng này"), at a point of its own (no camp drawn over it)."""
    khus = khu_list(zone)
    rect, props = next(k for k in khus if k[1]["khu"] == kid)
    rx, ry, rw, rh = rect
    pic, mx, my, k = drv.game.top.zone_layout()
    for fx, fy in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7)):
        x, y = rx + rw * fx, ry + rh * fy
        if chi_duong.khu_at(load_map(zone), x, y)[1]["khu"] == kid:
            break
    drv.click_at(drv.game.display.to_window(mx + x * k, my + y * k))


def toast_rects(drv: Driver) -> list[pygame.Rect]:
    """Where the toasts up now are drawn, in window px (main.py `_draw_overlays`: from the top
    scene's `toast_y`, 17 px apart, drifting up at most a few px)."""
    g = drv.game
    y = max(getattr(g.top, "toast_y", 4), g.achievements.clear_y())
    out = []
    for t in g.toasts:
        w = g.ui.text_size(t.text, 9)[0] + 16
        ty = y - min((g.now - t.born) * 4, max(0.0, y - 2))
        a = g.display.to_window(240 - w / 2, ty)
        b = g.display.to_window(240 + w / 2, ty + 14)
        out.append(pygame.Rect(a[0], a[1], b[0] - a[0], b[1] - a[1]))
        y += 17
    return out


def band_mark(drv: Driver, facts: dict, shot: str) -> None:
    """A monster of band 2 on the screen under the mouse: pips after its name, its band (above
    the newcomer's stage) in the tooltip. (Where the monsters stand is the map's: when none is on
    the screen, the facts say so.)"""
    from client.ui import nav_hud
    ws = here(drv)
    mons = sorted((e for e in ws.entities.values() if e.kind == "m" and e.alive and e.kv >= 2),
                  key=lambda e: abs(e.pos[0] - ws.player.x) + abs(e.pos[1] - ws.player.y))
    facts.setdefault("band_monsters_seen", []).append(len(mons))
    mons = [e for e in mons if abs(e.pos[0] - ws.player.x) < 200 and abs(e.pos[1] - ws.player.y) < 100]
    if not mons:
        return
    e = mons[0]
    real = pygame.mouse.get_pos

    def over():                                      # the mouse on its body, wherever it wanders
        sx, sy = ws.view.to_screen(e.pos[0], e.pos[1] - 4)
        return drv.game.display.to_window(sx, sy)
    pygame.mouse.get_pos = over                      # (the dummy video driver cannot move the mouse)
    try:
        drv.step(4)
        marks = nav_hud.band_marks(drv.game.ui, ws)
        facts.setdefault("band_marks", []).append(marks.get(e.id))
        assert marks.get(e.id) == (2, True), (marks, e.id, e.pos, (ws.player.x, ws.player.y))
        assert "Trung Vực · hợp Luyện Khí tầng 4-6 · cao hơn tu vi" in nav_hud.band_tip(ws, e)
        drv.shot(shot)
    finally:
        pygame.mouse.get_pos = real
    drv.step(2)


def run_nav_flow(workdir: Path, shots: Path | None = None) -> dict:
    server = ServerProcess(workdir)
    facts: dict = {}
    try:
        drv, uid = start(server, workdir, shots, "detu_cd")
        ws = here(drv)
        assert ws.zone_id == HUB
        drv.step(10)
        drv.shot("village_minimap")

        # ---- N: the picker, the server's recommendation first: a khu of band 1 of Kiếm Trủng Sơn
        drv.press(pygame.K_n)
        drv.wait_scene("NavPicker")
        drv.wait(lambda: nav(drv).data is not None and drv.has("nav_pick_rec"), 10, "the destinations")
        rec = nav(drv).data["recommended"]
        khus = {p["khu"]: (r, p) for r, p in khu_list(LAND)}
        assert rec["zone"] == LAND and rec["land_vi"] == "Kiếm Trủng Sơn", rec
        assert rec["khu"] in khus and khus[rec["khu"]][1]["band"] == "1", rec
        assert (rec["x"], rec["y"]) == (int(khus[rec["khu"]][1]["anchor_x"]), int(khus[rec["khu"]][1]["anchor_y"]))
        assert drv.has("nav_pick_home") and drv.has("nav_pick_village") and drv.has("nav_lock_thien_cong_phuong")
        picker = drv.game.top
        drv.step(3)
        assert not picker.cut, picker.cut              # every reason is read in full, none cut with "..."
        drv.shot("picker")
        label = f"{rec['name_vi']} (Kiếm Trủng Sơn)"
        drv.click("nav_pick_rec")
        drv.wait(lambda: not drv.top_is("NavPicker") and nav(drv).dest is not None, 5, "the arrow set")
        assert f"Chỉ Đường: tới {label}" in drv.toast_log, drv.toast_log[-3:]
        drv.wait(lambda: nav(drv).status == "path", 10, "the way through the village")
        assert nav(drv).gates and nav(drv).gates[0].target == LAND
        drv.step(20)
        drv.shot("arrow_village")

        # ---- M: Thiên Địa Đồ of the village, then the world; the toast keeps off the boxes
        big = open_big_map(drv)
        drv.shot("map_zone_village")
        drv.press(pygame.K_TAB)
        drv.step(4)
        assert big.view == "world" and drv.has("map_land_loan_so_coc")
        drv.game.toast("Chỉ Đường: tới một nơi rất xa có cái tên dài (Kiếm Trủng Sơn)", "#C99A3A")
        drv.step(3)
        boxes = [drv.game.ui.widgets[w] for w in drv.game.ui.widgets if w.startswith("map_land_")]
        tr = toast_rects(drv)
        assert tr
        facts["toast_over_box"] = [b for b in boxes for t in tr if b.colliderect(t)]
        drv.shot("map_world")
        drv.click("map_land_luu_van_coc")           # a land chosen on the map sets the arrow
        drv.wait(lambda: drv.top_is("WorldScene") and (nav(drv).dest or {}).get("zone") == LAND2, 5,
                 "the arrow to Lưu Vân Cốc")
        drv.press(pygame.K_n)                       # and back to the recommendation
        drv.wait(lambda: drv.has("nav_pick_rec"), 10, "the picker")
        drv.click("nav_pick_rec")
        drv.wait(lambda: (nav(drv).dest or {}).get("khu") == rec["khu"], 5, "the arrow to the khu again")

        # ---- follow the arrow through the gate, the camp and into the khu, to its anchor
        walk = Walk(drv, "kts_", every=9.0)
        t0 = time.time()
        follow_arrow(drv, server, lambda: here(drv).zone_id == LAND and nav(drv).dest is None, rec["name_vi"],
                     timeout=150, walk=walk)
        facts["walk_to_rec_s"] = time.time() - t0
        assert f"Đã tới {label}." in drv.toast_log, drv.toast_log[-5:]
        ws = here(drv)
        ax, ay = rec["x"], rec["y"]
        assert abs(ws.player.x - ax) < 60 and abs(ws.player.y - ay) < 60, (ws.player.x, ws.player.y, rec)
        titles = [b[0] for b in walk.banners]
        camp = next(p for r, p in khu_list(LAND) if p["band"] == "0")     # the camp at the gate comes first
        assert any(b[0].startswith(camp["name_vi"]) and b[1] == "nơi an toàn" and not b[2] for b in walk.banners), \
            walk.banners
        assert any(b[0].startswith(rec["name_vi"]) and "tầng 1-3" in b[1] and not b[2] for b in walk.banners), \
            walk.banners
        facts["banners_kts"] = titles
        drv.step(6)
        drv.shot("kts_at_anchor")

        # ---- M on the giant land: every khu; a khu of band 2 picked there
        big = open_big_map(drv)
        assert big.view == "zone"
        drv.step(6)
        facts["map_labels"] = list(big.labels)
        assert len(big.labels) == len(khu_list(LAND)), big.labels    # every khu named on the map
        drv.shot("kts_map_zone")
        band2 = [p for r, p in khu_list(LAND) if p["band"] == "2"]
        target = min(band2, key=lambda p: abs(int(p["anchor_x"]) - ws.player.x) + abs(int(p["anchor_y"]) - ws.player.y))
        click_khu(drv, target["khu"], LAND)
        drv.wait(lambda: drv.top_is("WorldScene") and (nav(drv).dest or {}).get("khu") == target["khu"], 5,
                 "the arrow to the khu of band 2")
        drv.wait(lambda: nav(drv).status == "path", 10, "the way to the khu")
        drv.step(30)
        drv.shot("kts_arrow_band2")
        big = open_big_map(drv)                     # the way on the big map
        drv.step(4)
        drv.shot("kts_map_zone_route")
        drv.press(pygame.K_TAB)
        drv.step(4)
        drv.shot("kts_map_world")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("WorldScene")
        walk = Walk(drv, "kts2_", every=9.0)
        follow_arrow(drv, server, lambda: any(b[2] for b in walk.banners), "the khu of band 2", timeout=120,
                     walk=walk)
        warn = next(b for b in walk.banners if b[2])
        assert warn[0].startswith(target["name_vi"]) and "tầng 4-6" in warn[1] and "cao hơn tu vi" in warn[1], warn
        facts["banners_kts2"] = [b[0] for b in walk.banners]
        drv.step(30)
        drv.shot("kts_band2_banner_plate")
        band_mark(drv, facts, "kts_band2_monster_mark")
        follow_arrow(drv, server, lambda: nav(drv).dest is None, target["name_vi"], timeout=120, walk=walk)
        drv.step(10)
        drv.shot("kts_band2_anchor")
        band_mark(drv, facts, "kts_band2_monster_mark_anchor")

        # ---- H: home from deep inside the land, through the gate, across the village
        drv.press(pygame.K_h)
        drv.wait(lambda: nav(drv).dest is not None and nav(drv).status == "path", 10, "the way home")
        drv.step(10)
        drv.shot("kts_arrow_home")
        t0 = time.time()
        follow_arrow(drv, server, lambda: nav(drv).dest is None and here(drv).zone_id == HUB, "the abode gate",
                     timeout=200, walk=Walk(drv, "home_", every=12.0))
        facts["walk_home_s"] = time.time() - t0
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

        def press_e(sc):
            if sc.target is not None and sc.target[1].props.get("action") == "exit":
                drv.press(pygame.K_e)
                drv.wait(lambda: here(drv) is not None and type(here(drv)).__name__ == "WorldScene", 10, "the village")
            else:                                   # face the gate
                drv.hold([pygame.K_s], 0.1)

        follow_arrow(drv, server, lambda: nav(drv).dest is None and getattr(here(drv), "zone_id", None) == HUB,
                     "the village centre", on_exit=press_e)
        assert "Đã tới Trúc Lâm Thôn." in drv.toast_log, drv.toast_log[-5:]
        drv.close()
    finally:
        server.stop()
    return facts


def run_second_land(workdir: Path, shots: Path | None = None) -> dict:
    """Lưu Vân Cốc: a newcomer at its gate opens the big map, picks the khu of band 1 farthest
    from the gate and follows the arrow there (the river and its bridges on the way)."""
    server = ServerProcess(workdir)
    facts: dict = {}
    try:
        drv, uid = start(server, workdir, shots, "detu_lvc", LAND2, "from_village")
        drv.step(20)
        drv.shot("lvc_gate")
        big = open_big_map(drv)
        drv.step(6)
        assert len(big.labels) == len(khu_list(LAND2)), big.labels
        drv.shot("lvc_map_zone")
        sc = here(drv)
        band1 = [p for r, p in khu_list(LAND2) if p["band"] == "1"]
        target = max(band1, key=lambda p: abs(int(p["anchor_x"]) - sc.player.x) + abs(int(p["anchor_y"]) - sc.player.y))
        click_khu(drv, target["khu"], LAND2)
        drv.wait(lambda: drv.top_is("WorldScene") and (nav(drv).dest or {}).get("khu") == target["khu"], 5,
                 "the arrow to the khu")
        drv.wait(lambda: nav(drv).status == "path", 10, "the way")
        drv.step(20)
        drv.shot("lvc_arrow")
        walk = Walk(drv, "lvc_", every=7.0)
        t0 = time.time()
        follow_arrow(drv, server, lambda: nav(drv).dest is None, target["name_vi"], timeout=150, walk=walk)
        facts["walk_s"] = time.time() - t0
        assert f"Đã tới {target['name_vi']} (Lưu Vân Cốc)." in drv.toast_log, drv.toast_log[-4:]
        assert any(b[0].startswith(target["name_vi"]) and "tầng 1-3" in b[1] for b in walk.banners), walk.banners
        facts["banners"] = [b[0] for b in walk.banners]
        drv.step(6)
        drv.shot("lvc_at_anchor")
        big = open_big_map(drv)
        drv.press(pygame.K_TAB)
        drv.step(4)
        drv.shot("lvc_map_world")
        drv.close()
    finally:
        server.stop()
    return facts


def test_nav_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_nav_") as tmp:
        facts = run_nav_flow(Path(tmp))
    assert not facts["toast_over_box"], facts


def test_nav_flow_second_land():
    with tempfile.TemporaryDirectory(prefix="kvtt_nav2_") as tmp:
        run_second_land(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "nav"
    with tempfile.TemporaryDirectory() as tmp:
        print("Kiếm Trủng Sơn:", run_nav_flow(Path(tmp), out))
    with tempfile.TemporaryDirectory() as tmp:
        print("Lưu Vân Cốc:", run_second_land(Path(tmp), out))
    print("screenshots in", out)
