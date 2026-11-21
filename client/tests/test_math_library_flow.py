"""M4 through the real client UI: open Tàng Thư Các from the Bí Cảnh Toán, read a
document from end to end, and open the right section from a question's answer card.

This is also the rendering check the milestone asks for: every page of every document is
laid out and drawn headlessly, and the test fails if a formula picture is missing, if a
line or a picture is wider than the page, or if drawing raises.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pygame

from client.scenes.math_library import DocScene
from client.tests.driver import Driver, ServerProcess
from client.tests.test_linh_phong_flow import abode
from client.tests.test_math_flow import FLOOR_1, answer_math, wait_question
from client.tests.test_world_flow import make_account
from client.ui import mathdraw


def top(drv: Driver):
    return drv.game.top


def read_whole_document(drv: Driver, shots_name: str | None = None) -> dict:
    """Reads a document to the end with Page Down, a page (one micro-skill) at a time,
    checking the layout of every page. Returns what was drawn."""
    scene = top(drv)
    drv.wait(lambda: scene.doc is not None and scene.items, 10, "the document")
    ui = drv.game.ui
    seen = {"formulas": 0, "matrices": 0, "figures": 0, "lines": 0, "screens": 0, "pages": 0}
    checked: set[int] = set()
    while True:
        if scene.page not in checked:
            checked.add(scene.page)
            problems = scene.layout_problems(ui)
            assert problems == [], f"page {scene.page + 1}: {problems[:5]}"
            for it in scene.items:
                kind = {"text": "lines", "formula": "formulas", "matrices": "matrices", "figure": "figures"}
                if it["kind"] in kind:
                    seen[kind[it["kind"]]] += 1
                if it["kind"] == "formula":
                    b = it["block"]
                    img = mathdraw.image(b["key"], max(1, round(b["w"] * ui.s)), max(1, round(b["h"] * ui.s)))
                    assert img is not None, f"no picture shipped for {b['tex']} ({b['key']}.png)"
        seen["screens"] += 1
        if shots_name and seen["screens"] <= 3:
            drv.shot(f"{shots_name}_p{seen['screens']}")
        before = (scene.page, scene.scroll)
        drv.press(pygame.K_PAGEDOWN)
        drv.step(2)
        if (scene.page, scene.scroll) == before or seen["screens"] > 80:
            break
    seen["pages"] = len(checked)
    assert seen["pages"] == len(scene.pages), "Page Down did not reach every page"
    assert (seen["formulas"] or seen["figures"] or seen["matrices"]) and seen["lines"], seen
    return seen


def scroll_to(drv, wid: str, rows: int = 12) -> None:
    """Bring a row of the document list into view with the arrow keys, as a player would."""
    for _ in range(rows):
        if drv.has(wid):
            return
        drv.press(pygame.K_UP)
        drv.step(2)
    for _ in range(rows):
        if drv.has(wid):
            return
        drv.press(pygame.K_DOWN)
        drv.step(2)
    assert drv.has(wid), f"{wid} cannot be scrolled into view"


def run_library_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir, time_scale=1)
    try:
        url = server.url
        token, uid = make_account(url, "thu_sinh", "Thư Sinh")
        server.sql("update users set flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "thu_sinh",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: abode(drv) is not None, 15, "the abode")
        drv.wait_api()
        while drv.top_is("DialogScene"):
            drv.press(pygame.K_RETURN)
            drv.step(3)

        # ---- the list of documents
        drv.click("hud_math")
        drv.wait(lambda: drv.top_is("MathPracticeScene") and top(drv).path is not None, 10, "the math path")
        drv.click("math_library")
        drv.wait(lambda: drv.top_is("LibraryListScene") and top(drv).data is not None, 10, "the library")
        listed = top(drv).data["subjects"]
        # four subjects, each written to floor 9 plus the hidden floor 10, one tab each; the list opens on the hub's subject
        assert [s["id"] for s in listed] == ["dai_so_tuyen_tinh", "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac"]
        assert top(drv).tab == 0
        for s in listed:
            assert [d["floor"] for d in s["documents"]] == list(range(1, 11)), s["id"]
            assert all(len(d["sections"]) == len(d["skills"]) for d in s["documents"])
        assert all(len(d["sections"]) == 6 for d in listed[0]["documents"] if d["floor"] <= 9)
        drv.shot("library_list")

        # ---- read every document of every subject from the first line to the last
        docs = []
        for s in listed:
            drv.click(f"lib_tab_{s['id']}")
            assert top(drv).tab == listed.index(s)
            for d in s["documents"]:            # ten documents do not fit the panel: the list scrolls
                scroll_to(drv, f"lib_open_{d['id']}")
            if s is listed[1]:
                drv.shot("library_list_second_subject")
            docs += [(s["id"], d) for d in s["documents"]]
        for sid, doc in docs:
            drv.click(f"lib_tab_{sid}")
            scroll_to(drv, f"lib_open_{doc['id']}")
            drv.click(f"lib_open_{doc['id']}")
            drv.wait_scene("DocScene")
            seen = read_whole_document(drv, f"library_{sid}_t{doc['floor']}" if doc["floor"] == 3 else None)
            print(f"  {sid} floor {doc['floor']}: {seen}")
            assert top(drv).current_section() == len(doc["sections"]) - 1, "the end is not the last section"
            drv.press(pygame.K_HOME)
            drv.step(2)
            assert top(drv).current_section() == 0
            drv.click("doc_next")                       # jumping by section
            drv.step(2)
            assert top(drv).current_section() == 1
            drv.press(pygame.K_ESCAPE)
            drv.wait_scene("LibraryListScene")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("MathPracticeScene")

        # ---- the answer card opens the document at the right section
        drv.click("math_tab_ds")                        # (a node's rows are on its branch tab)
        drv.click(FLOOR_1)
        q = wait_question(drv)
        answer_math(drv, server, correct=False)
        assert drv.has("math_doc"), "the answer card has no way into the library"
        drv.shot("library_from_answer")
        drv.click("math_doc")
        drv.wait_scene("DocScene")
        scene = top(drv)
        drv.wait(lambda: scene.doc is not None and scene.items, 10, "the document")
        skill = q["math"]["skill"]
        sections = [b for b in scene.doc["blocks"] if b["type"] == "section"]
        assert skill in [b["skill"] for b in sections]
        here = sections[scene.current_section()]
        assert here["skill"] == skill, f"opened at {here['skill']}, the question was about {skill}"
        drv.shot("library_at_section")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("MathQuizScene")
        drv.click("math_stop")
        drv.wait(lambda: drv.top_is("MathPracticeScene"), 10, "back at the floors")
        drv.close()
    finally:
        server.stop()


def test_library_through_the_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_library_flow(Path(tmp))


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "library"
    with tempfile.TemporaryDirectory() as tmp:
        run_library_flow(Path(tmp), out)
    print("screenshots in", out)
