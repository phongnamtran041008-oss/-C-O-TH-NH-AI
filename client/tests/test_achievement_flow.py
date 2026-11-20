"""Thành Tựu through the real client: a new player at Động Phủ tests their linh căn at the Trắc
Linh Đài (a real deed), the server pushes the unlock over the websocket and the banner with the
thanh_tuu FX plays at the top of the screen; V opens Thành Tựu Lục on the category with something
to claim, "Nhận" pays the linh thạch; reaching Trúc Cơ unlocks an achievement with a danh hiệu,
which the Danh Hiệu tab wears and the HUD shows under the name. The hidden ones read "???".

Every screen is saved as art/preview/thanh_tuu_*.png for review.
    python -m client.tests.test_achievement_flow
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


def save(drv: Driver, name: str, frames: int = 3) -> Path:
    drv.step(frames)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    p = PREVIEW / f"thanh_tuu_{name}.png"
    pygame.image.save(drv.game.display.window, str(p))
    return p


def run_achievement_flow(workdir: Path) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_thanh", "Thành Tựu")
        auth = {"Authorization": f"Bearer {token}"}
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_thanh",
                                                          "server_url": url}))
        drv = Driver(url, workdir)
        g = drv.game
        drv.click("menu_start")
        drv.wait(lambda: drv.top_is("AbodeScene") and g.state.cult is not None, 15, "Động Phủ")
        drv.wait_api()
        drv.wait(lambda: g.net is not None and g.net.online, 10, "the websocket")
        assert drv.has("hud_achievements")
        save(drv, "0_dong_phu")

        # ---- a real deed: the first test at the Trắc Linh Đài unlocks "Linh Căn Phẩm Giai"
        drv.press(pygame.K_c)
        drv.wait_scene("LinhCanScene")
        lc = g.top
        drv.wait(lambda: lc.v is not None, 10, "the linh căn view")
        drv.click("lc_awaken")
        drv.wait(lambda: "lc_giai:1" in g.achievements.shown, 15, "the unlock banner")
        drv.step(20)                              # the banner slides in, the FX burns
        save(drv, "1_bang_vang", frames=1)
        assert g.achievements.current and g.achievements.current["id"] == "lc_giai"
        drv.wait(lambda: lc.reveal is None, 10, "the reveal ends")
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "back in Động Phủ")
        drv.wait(lambda: g.achievements.current is None and not g.achievements.queue, 10, "the banner ends")
        # the banner was acknowledged: nothing waits any more
        drv.wait(lambda: httpx.get(url + "/achievements/new", headers=auth).json()["unlocks"] == [], 5, "seen")

        # ---- V opens Thành Tựu Lục on the category to claim
        drv.press(pygame.K_v)
        drv.wait_scene("AchievementsScene")
        sc = g.top
        drv.wait(lambda: sc.v is not None, 10, "the view")
        assert sc.tab == "suu_tam", sc.tab
        assert drv.has("ach_claim_lc_giai") and drv.has("ach_claim_all")
        save(drv, "2_thanh_tuu_luc")
        before = httpx.get(url + "/me", headers=auth).json()["spirit_stones"]
        drv.click("ach_claim_lc_giai")
        drv.wait_api()
        drv.wait(lambda: any("Linh Thạch" in t for t in drv.toast_log), 5, "the reward toast")
        assert httpx.get(url + "/me", headers=auth).json()["spirit_stones"] == before + 100
        e = next(e for c in sc.v["categories"] for e in c["achievements"] if e["id"] == "lc_giai")
        assert e["tiers"][0]["claimed"] and not e["claimable"]
        save(drv, "3_da_nhan")

        # ---- the other tabs: Tu Luyện, and the hidden ones
        drv.click("ach_tab_tu_luyen")
        save(drv, "4_tu_luyen")
        drv.click("ach_tab_bi_an")
        drv.step(2)
        assert all(not e["revealed"] for e in sc.rows(sc.v))
        save(drv, "5_bi_an")
        for _ in range(12):                       # scroll to the end of a long category
            drv.click("ach_tab_suu_tam")
            break
        sc.first = 99
        save(drv, "6_cuon")

        # ---- Trúc Cơ: an achievement with a danh hiệu, worn from the Danh Hiệu tab
        server.sql("update characters set realm='truc_co', realm_stage=1 where user_id=?", (uid,))
        server.sql("insert into achievement_counters(user_id, key, value) values (?, 'cult', 201) "
                   "on conflict(user_id, key) do update set value = 201", (uid,))
        sc.reload()                                # the view reconciles: the tier unlocks with a toast
        drv.wait(lambda: "cult_truc_co:1" in g.achievements.shown, 15, "the Trúc Cơ banner")
        drv.step(20)
        save(drv, "7_danh_hieu_moi", frames=1)
        drv.wait(lambda: any(t["title"] == "Trúc Cơ Tu Sĩ" for t in (sc.v or {}).get("titles", [])), 10,
                 "the title owned")
        drv.click("ach_tab_danh_hieu")
        drv.step(3)
        save(drv, "8_danh_hieu")
        i = [t["title"] for t in sc.v["titles"]].index("Trúc Cơ Tu Sĩ")
        drv.click(f"ach_wear_{i}")
        drv.wait_api()
        drv.wait(lambda: g.state.me.get("title") == "Trúc Cơ Tu Sĩ", 10, "the title worn")
        assert httpx.get(url + "/me", headers=auth).json()["title"] == "Trúc Cơ Tu Sĩ"
        save(drv, "9_mang_danh_hieu")
        drv.press(pygame.K_v)
        drv.wait(lambda: drv.top_is("AbodeScene"), 5, "closed")
        drv.wait(lambda: g.achievements.current is None, 10, "the banner ends")
        save(drv, "10_hud")
        drv.close()
    finally:
        server.stop()


def test_achievement_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_thanh_tuu_") as tmp:
        run_achievement_flow(Path(tmp))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        run_achievement_flow(Path(tmp))
    sys.exit(0)
