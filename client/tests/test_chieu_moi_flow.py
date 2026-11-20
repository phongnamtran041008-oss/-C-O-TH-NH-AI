"""Chiêu Thức II through the real client: a disciple who has finished Luyện Khí on Đạo Thụ
(every trial passed, every exercise handed in) opens Công Pháp with U, puts six of the new
chiêu on keys 1-6, saves, and casts them on the quái lỗi sai of Loạn Số Cốc. Each lands (the
server's event names every monster struck) and its effect is on screen.

    python -m client.tests.test_chieu_moi_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess
from client.tests.test_combat_flow import world
from client.tests.test_math_combat_flow import MA, VALLEY
from client.tests.test_math_skill_flow import Spy, approach, me_eid, settle
from client.tests.test_world_flow import make_account

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "server"))

from app.realtime import maps  # noqa: E402

BAR = ["ngu_kiem_thuat", "chuong_tam_loi", "hoa_long_thuat", "van_kiem_quy_tong", "bang_phong_thuat", "kiem_vuc"]
KEY = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
SUBJECTS = ("dai_so_tuyen_tinh", "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac")
# how long after the landing event each picture is taken (the effect is at its most telling)
# (just as it lands: a Nguyên Anh kills these monsters in one blow, and their death light follows)
SHOT_AFTER = {"ngu_kiem_thuat": 0.36, "chuong_tam_loi": 0.3, "hoa_long_thuat": 0.42, "van_kiem_quy_tong": 1.1,
              "bang_phong_thuat": 0.42, "kiem_vuc": 1.0}


def finish_luyen_khi(server: ServerProcess, uid: int) -> None:
    """Every node of Luyện Khí done: a trial of every floor of every subject, every exercise right."""
    for subject in SUBJECTS:
        for floor in range(1, 13):
            server.sql("insert into math_runs(user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
                       "combo, best_combo, asked, correct, review_asked, xp_gained, passed, started_at, ended_at) "
                       "values (?, ?, ?, 'trial', 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, datetime('now'), datetime('now'))",
                       (uid, subject, floor))
    tree = json.loads((ROOT / "server" / "data" / "math" / "tree.json").read_text("utf-8"))
    for node in tree["nodes"]:
        for pid in node.get("problems", []):
            server.sql("insert into math_submissions(user_id, problem_id, subject_id, floor, tier, verdict, passed, "
                       "total, ms, xp_gained, code, created_at, judged_at) "
                       "values (?, ?, 'x', 1, 1, 'AC', 5, 5, 1, 0, '', datetime('now'), datetime('now'))", (uid, pid))


def hold(drv: Driver, seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        drv.step(1)


def cast_slot(drv: Driver, server: ServerProcess, spy: Spy, slot: int, sid: str, near: bool = True) -> dict:
    ws = world(drv)
    drv.wait(lambda: ws.mskill_ready.get(sid, 0) < drv.game.now, 30, f"the cooldown of {sid}")
    before = len(spy.landed(sid))
    for _ in range(6):
        settle(drv, server)
        if near:
            approach(drv, server, near=58.0)   # far enough that it travels
        drv.press(KEY[slot])
        try:
            drv.wait(lambda: len(spy.landed(sid)) > before, 4, f"{sid} lands")
        except AssertionError:
            continue
        break
    assert len(spy.landed(sid)) > before, f"{sid} never landed; toasts={drv.toast_log[-3:]}"
    return spy.landed(sid)[-1]


def run_chieu_moi_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_c2", "Kiếm Tu")
        vmap = maps.load(VALLEY)
        area = next(a for a in vmap.monster_areas if a.props.get("monster") == MA)
        server.sql("update characters set zone_id=?, x=?, y=?, realm='nguyen_anh', realm_stage=1, qi=999 "
                   "where user_id=?", (VALLEY, area.x + area.w / 2, area.y + area.h / 2, uid))
        server.sql("update users set spirit_stones=500, flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        finish_luyen_khi(server, uid)
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_c2",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "Loạn Số Cốc")
        drv.wait_api()
        ws = world(drv)
        spy = Spy(ws)
        drv.wait(lambda: ws.mskills and len(ws.mskills) == 17, 10, "GET /math/skills")
        assert all(s["unlocked"] for s in ws.mskills), [(s["id"], s["locked_vi"]) for s in ws.mskills if not s["unlocked"]]

        # ---- Công Pháp: U opens it; put six new chiêu on the bar and save
        settle(drv, server)
        drv.press(pygame.K_u)
        drv.wait_scene("CongPhapScene")
        drv.shot("cong_phap_mo")
        for i, sid in enumerate(BAR):
            drv.click(f"cp_skill_{sid}")
            drv.click(f"cp_slot_{i}")
        assert drv.game.top.slots == BAR, drv.game.top.slots
        drv.shot("cong_phap_xep")
        drv.click("cp_save")
        drv.wait(lambda: not drv.top_is("CongPhapScene"), 10, "the bar is saved")
        pygame.mouse.set_pos((5, 5))             # (off the bar: its tooltip would cover the fight)
        assert ws.mskill_loadout == BAR
        assert json.loads(server.sql("select hotbar from characters where user_id=?", (uid,))[0][0])["chieu"] == BAR

        # ---- cast them in a real fight
        for slot, sid in enumerate(BAR):
            ev = cast_slot(drv, server, spy, slot, sid, near=sid != "kiem_vuc")
            assert ev["ok"] == 1 and ev["by"] == me_eid(drv), ev
            if sid in ("ngu_kiem_thuat", "chuong_tam_loi", "hoa_long_thuat", "van_kiem_quy_tong", "bang_phong_thuat"):
                assert ev.get("hits"), ev
            if sid in ("ngu_kiem_thuat", "hoa_long_thuat"):
                assert ev.get("ex") is not None, ev
            hold(drv, SHOT_AFTER[sid])
            drv.shot(f"chieu_moi_{sid}")
            hold(drv, 0.8)
        drv.close()
    finally:
        server.stop()


def test_chieu_moi_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_c2_") as tmp:
        run_chieu_moi_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "chieu_moi"
    with tempfile.TemporaryDirectory() as tmp:
        run_chieu_moi_flow(Path(tmp), out)
    print("screenshots in", out)
