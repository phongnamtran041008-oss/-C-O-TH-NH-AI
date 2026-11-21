"""A world tour in pictures (docs/DAI_DIA_DO_KIEM_THU.md): a character at Luyện Khí tầng 9 with
every land open walks every land by the Chỉ Đường arrow, through the real client and a real
server, and the screen is saved at each place a player would judge:

* the picker with everything open, "Thiên hạ" (once);
* per land: the gate camp on arrival, the minimap window (a crop at full size), the big map
  "Vùng này", the khu banner at every khu entered (the passes between bands), the anchor of the
  nearest khu of each band (one typical screenful there), a monster of that band with its pips
  under the mouse (when one is on the screen);
* Lôi Kiếp Đài (no khu): its camp, the climb to the boss terrace.

    python -m client.tests.tour_world [dir] [zone ...]   # default tools/reports/tour, every land

Pictures are the game window at 1440 x 810 (three times the 480 x 270 screen) scaled to half
(720 x 405: two window pixels a game pixel at most lost) to keep the folder small; the minimap
crop is at full window size.
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
from client.engine.tilemap import load_map
from client.tests import nav_walk
from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_combat_flow import CARD
from client.tests.test_lands_flow import grant_luyen_khi
from client.tests.test_math_combat_flow import answer_card
from client.tests.test_nav_flow import KEYS, follow_arrow, here, nav, open_big_map
from client.tests.test_world_flow import make_account
from client.tests.nav_walk import keys_for

OUT = ROOT / "tools" / "reports" / "tour"


class Shots:
    def __init__(self, drv: Driver, out: Path, land: str, first: int):
        self.drv, self.out, self.land, self.n = drv, out, land, first
        self.saved: list[Path] = []
        self.banners: list[tuple] = []
        self.facts: dict = {}

    def shot(self, what: str, crop: pygame.Rect | None = None) -> Path:
        self.drv.step(2)
        win = self.drv.game.display.window
        self.n += 1
        p = self.out / f"{self.n:03d}_{self.land}_{what}.png"
        if crop is not None:
            surf = win.subsurface(crop.clip(win.get_rect())).copy()
        else:
            surf = pygame.transform.smoothscale(win, (win.get_width() // 2, win.get_height() // 2))
        pygame.image.save(surf, str(p))
        self.saved.append(p)
        return p


class Banners:
    """follow_arrow's walk hook: a picture when a new khu banner shows (the pass into it)."""

    def __init__(self, shots: Shots, facts: dict | None = None):
        self.s = shots
        self.facts = facts if facts is not None else {}
        self.pos, self.since, self.stalled = None, time.time(), False

    def look(self, sc) -> None:
        p = (round(sc.player.x), round(sc.player.y))
        if p != self.pos:
            self.pos, self.since, self.stalled = p, time.time(), False
        elif not self.stalled and time.time() - self.since > 4.0:    # held keys, not moving: a picture of why
            self.stalled = True
            r = nav(self.s.drv).reading
            self.facts.setdefault("stalls", []).append(
                {"zone": sc.zone_id, "at": p, "aim": r and tuple(round(v) for v in r.aim),
                 "server": (round(getattr(sc.player, "sx", 0)), round(getattr(sc.player, "sy", 0)))})
            self.s.shot("stall")
        b = nav(self.s.drv).banner
        if b is not None and (not self.s.banners or self.s.banners[-1][:3] != b[:3]):
            self.s.banners.append(b[:3])
            self.s.drv.step(4)
            self.s.shot(f"khu_{len(self.s.banners):02d}")


def minimap_rect(drv: Driver) -> pygame.Rect:
    """The minimap window in window px (top right, at most 100 x 64 game px)."""
    d = drv.game.display
    a, b = d.to_window(370, 0), d.to_window(480, 80)
    return pygame.Rect(a[0], a[1], b[0] - a[0], b[1] - a[1])


def monster_of_band(drv: Driver, band: int, s: Shots) -> bool:
    """A monster of this band on the screen under the mouse: its pips and tooltip."""
    ws = here(drv)
    mons = sorted((e for e in ws.entities.values() if e.kind == "m" and e.alive and getattr(e, "kv", 0) == band),
                  key=lambda e: abs(e.pos[0] - ws.player.x) + abs(e.pos[1] - ws.player.y))
    mons = [e for e in mons if abs(e.pos[0] - ws.player.x) < 220 and abs(e.pos[1] - ws.player.y) < 120]
    if not mons:
        return False
    e = mons[0]
    real = pygame.mouse.get_pos

    def over():
        sx, sy = ws.view.to_screen(e.pos[0], e.pos[1] - 4)
        return drv.game.display.to_window(sx, sy)
    pygame.mouse.get_pos = over
    try:
        drv.step(4)
        s.shot(f"band{band}_monster")
    finally:
        pygame.mouse.get_pos = real
    drv.step(2)
    return True


def lead(drv: Driver, server: ServerProcess, dest: dict, s: Shots, timeout: float = 400.0) -> float:
    zone = here(drv).zone_id
    nav(drv).set_dest(dest, zone)
    drv.wait(lambda: nav(drv).status in ("path", "here") or nav(drv).dest is None, 15, "the way")
    t0 = time.time()
    follow_arrow(drv, server, lambda: nav(drv).dest is None, dest.get("name_vi", ""), timeout=timeout,
                 walk=Banners(s, s.facts))
    return time.time() - t0


def point_dest(zone: str, name: str, x: float, y: float) -> dict:
    return {"kind": "khu", "zone": zone, "khu": "", "name_vi": name, "land_vi": "", "band": 0,
            "stage_min": 0, "stage_max": 0, "x": int(x), "y": int(y)}


def tour_land(drv: Driver, server: ServerProcess, zone: str, s: Shots, facts: dict) -> None:
    ws = here(drv)
    drv.step(30)
    s.shot("gate_camp")
    s.shot("minimap", minimap_rect(drv))
    big = open_big_map(drv)
    drv.step(6)
    s.shot("map_vung_nay")
    drv.press(pygame.K_ESCAPE)
    drv.wait_scene("WorldScene")
    tm = load_map(zone)
    khus = chi_duong.khu_objects(tm)
    walked = {}
    if khus:
        for band in (1, 2, 3):
            cand = [k for k in khus if chi_duong.num(k[1].get("band")) == band]
            if not cand:
                continue
            px, py = ws.player.x, ws.player.y
            rect, props = min(cand, key=lambda k: math.hypot(int(k[1]["anchor_x"]) - px, int(k[1]["anchor_y"]) - py))
            secs = lead(drv, server, chi_duong.khu_dest(zone, rect, props, ""), s)
            walked[props["khu"]] = round(secs)
            drv.step(10)
            s.shot(f"band{band}_{props['khu']}")
            if band == 3:
                s.shot("band3_minimap", minimap_rect(drv))
            facts.setdefault("monsters_seen", {})[f"{zone}:{band}"] = monster_of_band(drv, band, s)
        big = open_big_map(drv)
        drv.step(6)
        s.shot("map_vung_nay_deep")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("WorldScene")
    else:
        for o in sorted(tm.find("poi"), key=lambda o: -o.y):
            if o.props.get("poi") in ("landmark", "boss"):
                name = o.props.get("name_vi", "")
                secs = lead(drv, server, point_dest(zone, name, o.x + 8, o.y + 28), s)
                walked[name] = round(secs)
                drv.step(10)
                s.shot(f"poi_{len(walked):02d}")
    facts.setdefault("walked_s", {})[zone] = walked
    facts.setdefault("banners", {})[zone] = [b[0] for b in s.banners]
    facts.setdefault("stalls", []).extend(s.facts.get("stalls", []))


def start_at(server: ServerProcess, workdir: Path, name: str, zone: str) -> Driver:
    token, uid = make_account(server.url, name, "Du Lãm")
    grant_luyen_khi(server, uid)
    server.sql("update characters set realm='luyen_khi', realm_stage=9 where user_id=?", (uid,))
    x, y = next((o.x, o.y) for o in load_map(zone).find("spawn") if o.name == "from_village")
    server.sql("update characters set zone_id=?, x=?, y=? where user_id=?", (zone, x, y, uid))
    server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": name, "server_url": server.url}))
    drv = Driver(server.url, workdir, None)
    drv.click("menu_start")
    drv.wait(lambda: here(drv) is not None and getattr(here(drv), "joined", False), 20, "the world")
    drv.wait_api()
    drv.wait(lambda: nav(drv).data is not None, 15, "the destinations")
    if drv.top_is(CARD):
        answer_card(drv, server, correct=True)
    return drv


def run_tour(out: Path, zones: list[str]) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    facts: dict = {}
    n = 0
    for k in range(0, len(zones), 4):                 # a server lets five accounts a day from one address
        with tempfile.TemporaryDirectory(prefix="kvtt_tour_") as tmp:
            server = ServerProcess(Path(tmp))
            try:
                for i, zone in enumerate(zones[k:k + 4]):
                    sub = Path(tmp) / f"c{i}"
                    sub.mkdir()
                    drv = start_at(server, sub, f"du_lam_{k + i}", zone)
                    s = Shots(drv, out, zone, n)
                    if k == 0 and i == 0:
                        drv.press(pygame.K_n)
                        drv.wait_scene("NavPicker")
                        drv.wait(lambda: drv.has("nav_pick_rec"), 10, "the picker")
                        drv.step(4)
                        s.land = "the_gioi"
                        s.shot("picker_moi_vung_mo")
                        facts["picker_cut"] = list(drv.game.top.cut)
                        drv.press(pygame.K_ESCAPE)
                        drv.step(4)
                        open_big_map(drv)
                        drv.press(pygame.K_TAB)
                        drv.step(6)
                        s.shot("thien_ha")
                        drv.press(pygame.K_ESCAPE)
                        drv.wait_scene("WorldScene")
                        s.land = zone
                    t0 = time.time()
                    try:
                        tour_land(drv, server, zone, s, facts)
                    except AssertionError as e:
                        facts.setdefault("errors", {})[zone] = str(e)[:400]
                        facts.setdefault("stalls", []).extend(s.facts.get("stalls", []))
                        s.shot("FAILED")
                    facts.setdefault("tour_s", {})[zone] = round(time.time() - t0)
                    n = s.n
                    drv.close()
            finally:
                server.stop()
    return facts


def main() -> None:
    args = sys.argv[1:]
    out = Path(args.pop(0)) if args and ("/" in args[0] or "\\" in args[0]) else OUT
    zones = args or nav_walk.world_lands()
    facts = run_tour(out, zones)
    print(json.dumps(facts, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
