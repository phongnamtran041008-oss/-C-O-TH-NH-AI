"""Lộ Trình through the real client UI: a new player enters the abode, Trúc Lão welcomes them and
the board opens; the first two steps are done and can be claimed (the Linh Thạch go up once);
the handbook opens; the HUD box names the next step; opening Đạo Thụ completes a step; the board's
"Đi tới" button opens the hub; a sitting completes the next one and the "Xong" toast comes; the
trip down to the village completes the last of the easy ones and the HUD box is there too.

Run as `python -m client.tests.test_guide_flow <folder>` to leave numbered screenshots."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.scenes import guide
from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_flow import advance_dialogs
from client.tests.test_linh_phong_flow import abode
from client.tests.test_math_flow import answer_math, top, wait_question
from client.tests.test_math_tree_flow import drawn_text
from client.tests.test_world_flow import make_account

DATA = json.loads((ROOT / "server" / "data" / "guide.json").read_text("utf-8"))
STEPS = {s["id"]: s for c in DATA["chapters"] for s in c.get("steps", [])}


def state_of(drv: Driver, step_id: str) -> str:
    view = drv.game.state.guide
    return next(s["state"] for c in view["chapters"] for s in c["steps"] if s["id"] == step_id)


def wait_state(drv: Driver, step_id: str, state: str) -> None:
    drv.wait(lambda: drv.game.state.guide is not None and state_of(drv, step_id) == state, 10,
             f"{step_id} {state}")


def select_step(drv: Driver, step_id: str) -> None:
    """Walks the selection to a step with Up / Down (the list scrolls to keep it in sight)."""
    board = drv.game.top
    items = guide.list_items(guide.find_chapter(drv.game.state.guide, board.ch_id))
    want = items.index(step_id)
    for _ in range(len(items)):
        have = items.index(board.sel)
        if have == want:
            break
        drv.press(pygame.K_DOWN if want > have else pygame.K_UP)
    assert board.sel == step_id and drv.has(f"guide_step_{step_id}")


def check_fit(drv: Driver) -> int:
    """Draws every row of every chapter and checks that the detail text stays above the buttons
    and inside the panel. Returns how many rows were looked at."""
    board = drv.game.top
    ui = drv.game.ui
    x, y, w, h = board.PANEL
    seen: list[tuple[str, pygame.Rect]] = []
    real = ui.text

    def spy(txt, *args, **kwargs):
        r = real(txt, *args, **kwargs)
        seen.append((txt, r))
        return r
    n = 0
    for ch in drv.game.state.guide["chapters"]:
        for key in guide.list_items(ch):
            board.ch_id, board.sel, board.show_sel = ch["id"], key, True
            seen.clear()
            ui.text, ui.set_tooltip = spy, lambda txt: None      # (a tooltip is not the detail)
            try:
                drv.step(2)
                seen.clear()
                drv.step(1)
            finally:
                del ui.text, ui.set_tooltip
            for txt, r in seen:
                if y + 25 + board.ROW * board.ROWS < r.y < y + h - 22:      # the detail: under the list, above the buttons
                    assert r.bottom <= y + h - 22, (key, txt, r)
                    assert r.right <= x + w - 8, (key, txt, r)
            n += 1
    return n


def stones(server: ServerProcess, uid: int) -> int:
    return server.sql("select spirit_stones from users where id=?", (uid,))[0][0]


def run_guide_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "lo_trinh", "Lộ Trình Sinh")
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "lo_trinh",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        old = guide.WELCOME
        guide.WELCOME = True                # (the Driver turns it off for the old flows)
        try:
            drv.click("menu_start")
            drv.wait(lambda: abode(drv) is not None, 15, "the abode")

            # ---- the welcome: Trúc Lão's lines, then the board opens
            drv.wait(lambda: drv.top_is("DialogScene"), 15, "the welcome dialog")
            dlg = drv.game.top
            assert dlg.speaker == DATA["welcome"]["speaker_vi"] and dlg.lines == DATA["welcome"]["lines_vi"]
            drv.step(30)
            drv.shot("welcome_dialog")
            advance_dialogs(drv)
            drv.wait(lambda: drv.top_is("GuideScene"), 10, "the board")
            drv.wait_api()
            assert drv.game.state.me["tutorial_step"] == 5      # (the abode keeps no tutorial state any more)
            flags = json.loads(server.sql("select flags from users where id=?", (uid,))[0][0])
            assert flags["tutorial"] == 5 and "welcome" in flags["guide"]["seen"]      # the old tutorial is over
            assert state_of(drv, "g_welcome") == "done" and state_of(drv, "g_board") == "done"
            assert drv.game.state.guide["welcome"]["seen"]
            # Chính đạo leads once the welcome steps are done: the board opens on its one step
            assert drv.game.state.guide["lead"] == "main" and drv.game.top.ch_id == guide.MAIN
            assert drv.has("guide_ch_main") and drv.has("guide_goto") and drv.has("guide_ch_c4_luyen_khi")
            assert drv.game.state.guide["main"]["name_vi"] in drawn_text(drv)
            drv.shot("board_first_open")
            drv.click("guide_ch_c1_nhap_mon")
            assert drv.has("guide_step_g_welcome") and drv.has("guide_close")

            # ---- claim a step: the Linh Thạch go up by its reward, once
            drv.click("guide_step_g_welcome")
            assert drv.has("guide_claim")
            drv.shot("step_with_claim_button")
            before = stones(server, uid)
            drv.click("guide_claim")
            wait_state(drv, "g_welcome", "claimed")
            drv.wait_api()
            gain = STEPS["g_welcome"]["rewards"]["spirit_stones"]
            assert stones(server, uid) - before == gain, (before, stones(server, uid))
            assert not drv.has("guide_claim")
            drv.step(10)
            drv.shot("after_claim")

            # ---- the chapters: optional steps, and the generated Luyện Khí chapter
            drv.click("guide_ch_c3_thuc_chien")
            drv.click("guide_step_g_fortune")
            assert "(tuỳ chọn)" in drawn_text(drv)
            drv.shot("chapter_with_optional_steps")
            drv.click("guide_ch_c1_nhap_mon")
            select_step(drv, "g_first_trial")
            drv.shot("long_step_first_trial")
            drv.click("guide_ch_c4_luyen_khi")
            drv.click("guide_step_c4_luyen_khi_s1")
            assert any(t.startswith("Còn:") for t in drawn_text(drv))
            drv.shot("generated_chapter_step")
            assert check_fit(drv) >= 20, "every step and bonus row fits its box"
            drv.click("guide_ch_c1_nhap_mon")

            # ---- the handbook
            drv.click("guide_tab_book")
            drv.click("guide_topic_buoi_luyen")
            assert drv.has("guide_topic_dao_thu")
            drv.shot("handbook_buoi_luyen")
            drv.click("guide_topic_phim_tat")
            drv.shot("handbook_phim_tat")
            drv.click("guide_tab_road")
            drv.click("guide_close")
            drv.wait(lambda: not drv.top_is("GuideScene"), 5, "the abode")

            # ---- the HUD box names the next step
            drv.wait(lambda: drv.has("hud_guide"), 5, "the HUD box")
            cur = drv.game.state.guide["current"]
            assert cur["step_id"] == "g_open_tree" and cur["title_vi"] == "Mở Đạo Thụ"
            main = drv.game.state.guide["main"]         # the box leads with Chính đạo, not with the step
            text = drawn_text(drv)
            assert main["node_id"] == "ds_ngon_ngu" and any(main["name_vi"] in t for t in text), text
            assert "Học bài" in text and "Chính đạo 1/5 · F1" in text
            drv.shot("abode_hud_tracker")

            # ---- M opens Đạo Thụ; closing it and pressing F1 shows the step done
            drv.press(pygame.K_m)
            drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the hub")
            wait_state(drv, "g_open_tree", "done")
            drv.click("math_close")
            drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode")
            drv.press(pygame.K_F1)
            drv.wait(lambda: drv.top_is("GuideScene"), 5, "the board by F1")
            assert state_of(drv, "g_open_tree") == "done"

            # ---- "Đi tới" of a step: the button closes the board and opens the hub
            drv.click("guide_ch_c1_nhap_mon")
            select_step(drv, "g_first_run")
            assert STEPS["g_first_run"]["goto"] == "math" and drv.has("guide_goto") and drv.has("guide_help")
            drv.click("guide_goto")
            drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the hub")
            assert "GuideScene" not in drv.scene_names()
            assert top(drv).tab == "next" and drv.has("math_main_go")
            drv.click("math_close")
            drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode")

            # ---- "Đi tới" of Chính đạo does what the hub card's button does: the lesson first
            drv.press(pygame.K_F1)
            drv.wait(lambda: drv.top_is("GuideScene"), 5, "the board by F1")
            assert drv.game.top.ch_id == guide.MAIN
            drv.shot("board_main_entry")
            drv.click("guide_goto")
            drv.wait(lambda: drv.top_is("DocScene"), 10, "the lesson of the first node")
            assert "GuideScene" not in drv.scene_names()
            drv.wait(lambda: "ds_ngon_ngu:1" in json.loads(server.sql("select flags from users where id=?",
                                                                       (uid,))[0][0]).get("path", {}).get("read", []),
                     10, "the lesson recorded as read")
            drv.press(pygame.K_ESCAPE)
            drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).tree is not None
                     and top(drv).tree["main"]["step"] == "luyen", 10, "the card at Luyện")
            drv.shot("hub_main_luyen")

            # ---- a sitting from the card finishes g_first_run: the "Xong" toast comes by itself
            drv.click("math_main_go")
            wait_question(drv)
            answer_math(drv, server, correct=True)
            drv.click("math_stop")
            drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).summary is not None, 10, "the summary")
            wait_state(drv, "g_first_run", "done")
            assert any("Xong: Buổi luyện đầu tiên" in t for t in drv.toast_log), drv.toast_log
            drv.click("math_back")
            drv.wait(lambda: top(drv).summary is None, 10, "the floors again")
            drv.click("math_close")
            drv.wait(lambda: not drv.top_is("MathPracticeScene"), 5, "the abode")

            # ---- down to the village: the HUD box is there, and g_village is done
            drv.hold([pygame.K_s], 0.9)
            drv.press(pygame.K_e)
            drv.wait(lambda: drv.game.world_scene() is not None and drv.game.world_scene().joined, 10, "village")
            wait_state(drv, "g_village", "done")
            drv.wait(lambda: drv.has("hud_guide"), 5, "the box in the village")
            assert drv.game.state.guide["claimable"] >= 3
            drv.shot("world_hud_tracker")
            drv.press(pygame.K_F1)
            drv.wait(lambda: drv.top_is("GuideScene"), 5, "the board in the village")
            drv.click("guide_ch_c3_thuc_chien")
            drv.shot("board_in_village")
            drv.press(pygame.K_F1)                       # F1 again closes it
            drv.wait(lambda: not drv.top_is("GuideScene"), 5, "back in the village")
        finally:
            guide.WELCOME = old
        drv.close()
    finally:
        server.stop()


def test_guide_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_guide_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "guide"
    with tempfile.TemporaryDirectory() as tmp:
        run_guide_flow(Path(tmp), out)
    print("screenshots in", out)
