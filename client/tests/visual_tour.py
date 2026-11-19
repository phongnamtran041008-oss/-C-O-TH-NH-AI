"""Screenshots of screens the main flow does not reach (the 10-pulls of Thiên Cơ Các).
For visual review:

    python -m client.tests.visual_tour OUT_DIR
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import Driver, ServerProcess


def tour(workdir: Path, out: Path) -> None:
    server = ServerProcess(workdir)
    try:
        r = httpx.post(server.url + "/auth/register", json={"username": "tour", "password": "matkhau1"}).json()
        token = r["token"]
        h = {"Authorization": f"Bearer {token}"}
        httpx.post(server.url + "/character/create", headers=h,
                   json={"display_name": "Khách Tham Quan", "appearance": {"hair_color": "#6B3FA0",
                                                                         "hair_style": "dai", "body": "nu"}})
        server.sql("update users set spirit_stones=50000")
        (workdir / "session.json").write_text(f'{{"token": "{token}", "username": "tour", '
                                              f'"server_url": "{server.url}"}}')
        drv = Driver(server.url, workdir, out)
        drv.n_shots = 40
        drv.click("menu_start")
        drv.wait(lambda: "AbodeScene" in drv.scene_names(), 10, "abode")
        drv.wait_api()
        drv.press(pygame.K_g)
        drv.wait_scene("GachaScene")
        drv.wait_api()
        for tab, button in (("bees", "g_bee10"), ("pets", "g_pet10")):
            drv.click(f"g_tab_{tab}")
            drv.step(5)
            drv.shot(f"gacha_{tab}")
            drv.click(button)
            drv.wait(lambda: drv.game.top.results is not None, 5, f"10-pull {tab}")
            drv.wait(lambda: drv.game.top.anim_t > 3.5, 10, "revealed")
            drv.shot(f"gacha_{tab}_10")
            drv.click("g_done")
        drv.press(pygame.K_ESCAPE)
        drv.close()
    finally:
        server.stop()


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots"
    with tempfile.TemporaryDirectory() as tmp:
        tour(Path(tmp), out)
    print("screenshots in", out)
