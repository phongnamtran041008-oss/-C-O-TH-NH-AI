"""Trắc Linh Đài through the real client: a new player presses C in Động Phủ, sees no root yet
and the odds of the free first test, awakens one (the reveal burst, then the root card in the
colour of its giai), is given Tẩy Linh Đan, rolls until a different root comes out, sees the
old and the new side by side and takes the new one; the đồ giám then lists both and the Tu Vi
sheet (K) names the root carried.

Every screen is saved as art/preview/linh_can_*.png for review.
    python -m client.tests.test_linh_can_flow
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import httpx
import pygame

from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_world_flow import make_account

PREVIEW = ROOT / "art" / "preview"
PILL = "tay_linh_dan"


def save(drv: Driver, name: str) -> Path:
    drv.step(3)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    p = PREVIEW / f"linh_can_{name}.png"
    pygame.image.save(drv.game.display.window, str(p))
    return p


def give(server: ServerProcess, uid: int, item_id: str, qty: int) -> None:
    server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, ?, ?, 0) "
               "on conflict(user_id, item_id, bound) do update set quantity = quantity + excluded.quantity",
               (uid, item_id, qty))


def run_linh_can_flow(workdir: Path) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_linh", "Trắc Linh")
        auth = {"Authorization": f"Bearer {token}"}
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_linh",
                                                          "server_url": url}))
        drv = Driver(url, workdir)
        drv.click("menu_start")
        drv.wait(lambda: drv.top_is("AbodeScene") and drv.game.state.cult is not None, 15, "Động Phủ")
        drv.wait_api()

        # ---- C opens the Trắc Linh Đài: no root yet, the free test and its odds
        drv.press(pygame.K_c)
        drv.wait_scene("LinhCanScene")
        sc = drv.game.top
        drv.wait(lambda: sc.v is not None, 10, "the view")
        assert not sc.v["awakened"] and drv.has("lc_awaken")
        save(drv, "1_chua_trac")

        # ---- the free first test: the burst, then the root card
        drv.click("lc_awaken")
        drv.wait(lambda: sc.reveal is not None and sc.reveal["t"] > 0.9, 10, "the reveal")
        save(drv, "2_hien_linh")
        first = sc.reveal["root"]
        drv.wait(lambda: sc.reveal is None, 10, "the reveal ends")
        drv.wait(lambda: sc.v["awakened"] and sc.v["root"]["id"] == first["id"], 5, "the root carried")
        assert first["giai_index"] <= 3, "a Phàm Nhân is capped at Huyền giai"
        save(drv, "3_linh_can")

        # ---- a tẩy linh pill: roll until a different root comes out, then take it
        give(server, uid, PILL, 8)
        sc.reload()
        drv.wait(lambda: next(p for p in sc.v["pills"] if p["id"] == PILL)["have"] == 8, 10, "the pills")
        sc.sel_pill = PILL
        save(drv, "4_dan_tay_linh")
        for _ in range(8):
            have = next(p for p in sc.v["pills"] if p["id"] == PILL)["have"]
            drv.click(f"lc_roll_{PILL}")
            drv.wait(lambda: next(p for p in sc.v["pills"] if p["id"] == PILL)["have"] == have - 1, 10, "a roll")
            drv.wait(lambda: sc.reveal is None, 10, "the reveal ends")
            if sc.v.get("pending"):
                break
        new = sc.v["pending"]
        assert new and new["id"] != first["id"], "eight rolls never gave another root"
        assert drv.has("lc_keep") and drv.has("lc_take")
        save(drv, "5_chon")
        drv.click("lc_take")
        drv.wait_api()
        drv.wait(lambda: sc.v["pending"] is None and sc.v["root"]["id"] == new["id"], 10, "the new root")
        drv.wait(lambda: any(new["name_vi"] in t for t in drv.toast_log), 5, "the toast")
        assert httpx.get(url + "/linh-can", headers=auth).json()["root"]["id"] == new["id"]
        save(drv, "6_da_doi")

        # ---- the đồ giám: both roots seen, the rest still ???
        drv.click("lc_tab_book")
        drv.step(3)
        seen = [b["id"] for b in sc.v["book"] if b["discovered"]]
        assert first["id"] in seen and new["id"] in seen and len(seen) < len(sc.v["book"])
        save(drv, "7_do_giam")

        # ---- the Tu Vi sheet names the root carried, in its colour
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "back in Động Phủ")
        drv.game.refresh_cult()
        drv.wait(lambda: ((drv.game.state.cult or {}).get("linh_can") or {}).get("id") == new["id"], 10,
                 "the sheet knows the root")
        drv.press(pygame.K_k)
        drv.wait_scene("CharacterScene")
        drv.wait_api()
        assert drv.has("ch_linh_can")
        save(drv, "8_tu_vi")
        drv.close()
    finally:
        server.stop()


def test_linh_can_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_linh_can_") as tmp:
        run_linh_can_flow(Path(tmp))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        run_linh_can_flow(Path(tmp))
    sys.exit(0)
