"""Ngự kiếm through the real client and a real server (Lưu Vân Cốc, the waterfall between the rock
at its foot and the clouds above it).

Low rung (Luyện Khí tầng 9 of Đạo Thụ): G held takes off - the crouch, the rise, the shadow left on
the ground; the arrow keys fly us over the water walking cannot cross; G again lands on the far
side; out over the water again the gauge runs dry and the server carries us back to the bank.
A quick tap of G is still the hop. (The high rung, Trúc Cơ, is proved by server/tests/test_flight.py
with the tree position monkeypatched, and drawn in art/preview/vfx_phi_hanh.png.)

    python -m client.tests.test_flight_flow [dir]     # screenshots in <dir> (and art/preview/ability_phi_hanh_*.png)
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_beast_flow import GLIDE_FROM, GLIDE_ZONE, enter, feet, start

# Đại Địa Đồ: the places come from the plan (the giant map is generated): the rock at the foot
# of the fall is GLIDE_FROM, the water one tile north of it, the clouds (the ledge) 3 tiles north
WATER = (GLIDE_FROM[0], GLIDE_FROM[1] - 1)
LEDGE_ROW = GLIDE_FROM[1] - 3

PREVIEW = ROOT / "art" / "preview"


def keep(drv: Driver, name: str) -> None:
    """A screenshot of the game window, kept as art/preview/ability_phi_hanh_<name>.png."""
    p = drv.shot(name)
    if p is None:
        drv.shots = Path(tempfile.mkdtemp(prefix="kvtt_fly_shots_"))
        p = drv.shot(name)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, PREVIEW / f"ability_phi_hanh_{name}.png")


def hold_fly(drv: Driver, ws, keys: set, seconds: float, shot: str | None = None, at: float = 0.5) -> None:
    """Fly with `keys` held for `seconds` (G is not among them), a screenshot `at` of the way."""
    import time
    drv.keys.held = set(keys)
    t0 = time.perf_counter()
    took = shot is None
    while time.perf_counter() - t0 < seconds:
        drv.step(1)
        if not took and time.perf_counter() - t0 >= seconds * at:
            keep(drv, shot)
            took = True
    drv.keys.held = set()
    drv.step(1)


def take_off(drv: Driver, ws, level: int) -> None:
    drv.keys.held = {pygame.K_g}
    drv.press(pygame.K_g)
    drv.wait(lambda: ws.fly == level, 3, "up on the sword")
    drv.keys.held = set()
    drv.step(1)


def run_flight_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        # stage 8, not 9: at 9 Kim Sí Điểu shows on the cloud pocket where the hop lands, and fights
        uid = start(server, workdir, shots, "detu_bay", "Ngự Kiếm", GLIDE_ZONE, GLIDE_FROM, 8)
        drv = Driver(server.url, workdir, shots)
        ws = enter(drv, GLIDE_ZONE)
        fv = ws.flight
        assert fv and fv["level"] == 1 and fv["gauge_max"] > 0, fv
        me = ws.my_eid()
        x0, y0 = feet(*GLIDE_FROM)
        assert ws.tile_at(*WATER) == "water" and ws.col.blocked(*feet(*WATER))
        drv.step(10)

        # ---- a quick tap is still the hop (Đạp Kiếm Lướt), now a real leap with a shadow
        drv.keys.held = {pygame.K_w}
        drv.press(pygame.K_g)
        drv.keys.held = set()
        drv.wait(lambda: ws.glide_pos(me, 0, 0)[2], 2, "the hop")
        drv.step(4)
        keep(drv, "luot")
        drv.wait(lambda: not ws.glide_pos(me, 0, 0)[2] and not ws.pending, 5, "the hop lands")
        drv.wait(lambda: ws.flight and ws.fly_gauge >= ws.flight["gauge_max"] - 0.05, 3, "a full gauge")
        drv.step(30)
        assert int((ws.player.y - 1) // 16) <= LEDGE_ROW, "over the waterfall by the hop"
        # back down by the hop again
        rest = drv.game.now + 0.3
        drv.wait(lambda: drv.game.now > max(ws.glide_ready, rest), 5, "the hop rests (the server's cooldown too)")
        drv.keys.held = {pygame.K_s}
        drv.step(1)
        ws.player.facing = "down"
        drv.press(pygame.K_g)
        drv.keys.held = set()
        drv.wait(lambda: not ws.glide_pos(me, 0, 0)[2] and not ws.pending, 5, "back on the rock")
        drv.step(20)
        assert abs(ws.player.y - y0) < 12, (ws.player.x, ws.player.y)

        # ---- G held: take off - the crouch, the rise, the ring on the ground
        before = ws.corrections
        drv.keys.held = {pygame.K_g}
        drv.press(pygame.K_g)
        drv.wait(lambda: ws.fly == 1, 3, "up on the sword")
        drv.step(3)
        keep(drv, "cat_canh")
        drv.keys.held = set()
        drv.step(20)
        keep(drv, "tren_khong")
        f = ws.flyers[me]
        assert f.flying and f.alt(drv.game.now) > ws.fly_lift(1) * 0.7
        # ---- out over the water and on to the clouds above the fall
        hold_fly(drv, ws, {pygame.K_w}, 0.2, "tren_nuoc", at=0.7)
        assert not ws.may_land(ws.player.x, ws.player.y), "over the water"
        hold_fly(drv, ws, {pygame.K_w}, 0.12)
        drv.wait(lambda: not ws.pending, 5, "the server flew us too")
        x, y = ws.player.x, ws.player.y
        tile = (int(x // 16), int((y - 1) // 16))
        if not ws.may_land(x, y):              # (a frame short of the far bank: a little further)
            hold_fly(drv, ws, {pygame.K_w}, 0.08)
        assert ws.may_land(ws.player.x, ws.player.y), tile
        drv.press(pygame.K_g)
        drv.wait(lambda: ws.fly == 0 and not ws.pending, 5, "down on the far side")
        drv.step(6)
        keep(drv, "ha_canh")
        drv.wait(lambda: not ws.flyers[me].shown(drv.game.now), 3, "the touch-down")
        assert int((ws.player.y - 1) // 16) <= LEDGE_ROW, "over the water and landed above the fall"
        assert ws.corrections - before <= 2, ws.corrections - before

        # ---- out over the water and hover: the gauge runs dry and the server carries us back
        drv.wait(lambda: ws.fly_gauge >= ws.flight["min_gauge"] + 0.5, 8, "the gauge refills")
        drv.step(int(60 * 3))
        take_off(drv, ws, 1)
        hold_fly(drv, ws, {pygame.K_s}, 0.16)
        hold_fly(drv, ws, set(), 0.8, "can_kiem_khi", at=0.9)
        assert not ws.may_land(ws.player.x, ws.player.y), "hovering over the water"
        drv.wait(lambda: ws.fly == 0, ws.flight["gauge_max"] + 3, "the gauge runs dry")
        drv.step(8)
        keep(drv, "roi_ve_bo")
        drv.wait(lambda: not ws.pending, 5, "settled")
        drv.step(30)
        assert ws.may_land(ws.player.x, ws.player.y), "back on the ground"
        drv.close()
    finally:
        server.stop()


def test_flight_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_fly_") as tmp:
        run_flight_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    with tempfile.TemporaryDirectory(prefix="kvtt_fly_") as tmp:
        run_flight_flow(Path(tmp), out)
    print("ok")
