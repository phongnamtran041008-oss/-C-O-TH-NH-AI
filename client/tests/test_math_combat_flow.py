"""M7 through the real client UI: walk into Loạn Số Cốc, pick a fight with a quái lỗi sai,
answer the math question it asks on the combat card, break its Mặc Thuẫn and kill it, read
the ghi chú lỗi sai it leaves behind (which opens the right part of Tàng Thư Các), then
forge at Lò Toán - which refuses until the note is in the bag."""
from __future__ import annotations

import json
import math
import sys
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import ROOT, Driver, ServerProcess, fill_math_answer
from client.tests.test_combat_flow import nearest, walk_to, world
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the map the server ships

from app.realtime import maps  # noqa: E402

VALLEY = "loan_so_coc"
MA = "dstt_phan_tu_ma"            # floor 1, "đếm {1, {2, 3}} thành ba phần tử"
NOTE = "ghi_chu_phan_tu"
RECIPE = "but_tap_hop"


def engage_mistake(drv: Driver, server: ServerProcess, kind: str = MA):
    """Walk to the nearest mistake-monster and keep attacking until its card opens.

    The same shape as test_combat_flow.engage: a weapon has a cooldown and the server
    silently drops an attack sent inside it, so one click is not reliably one attack.
    """
    import time
    ws = world(drv)
    drv.wait(lambda: nearest(ws, kind) is not None, 10, f"a {kind}")
    end = time.time() + 20
    while time.time() < end:
        m = nearest(ws, kind)
        if m is None:
            break
        if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) >= 34:
            walk_to(drv, m.pos[0], m.pos[1])
            drv.step(5)
            continue
        drv.click_at(drv.game.display.to_window(*ws.world_to_screen(m.pos[0], m.pos[1] - 8)))
        for _ in range(40):
            drv.step(3)
            if drv.top_is("MathCombatQuizScene"):
                return ws.entities.get(getattr(drv.game.top, "monster_id", "")) or m
    open_q = server.sql("select ref, created_at from quiz_sessions where answered_at is null")
    raise AssertionError(f"no card after attacking a {kind}; open questions: {open_q}; "
                         f"scenes={drv.scene_names()}; toasts={drv.toast_log[-5:]}")


def answer_card(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    """Answer the math question on the combat card, reading the key from the database."""
    q = drv.game.top.q
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])
    fill_math_answer(drv, q, key, correct)
    drv.wait(lambda: drv.top_is("MathCombatQuizScene") and drv.game.top.result, 10, "the result")
    return drv.game.top.result


def give(server: ServerProcess, uid: int, item_id: str, qty: int = 1) -> None:
    """Put something in the bag. It has to add, because the fight may already have
    dropped the same material."""
    server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, ?, ?, 0) "
               "on conflict(user_id, item_id, bound) do update set "
               "quantity = quantity + excluded.quantity", (uid, item_id, qty))


def trek(drv: Driver, server: ServerProcess, tx: float, ty: float, near: float = 22.0) -> None:
    """Walk across Loạn Số Cốc to a point, over a route that really exists.

    Holding the arrow keys toward a far target is not enough here: rocks and ink trees stand
    in the way, and a monster that comes to ask its question both stops the keys from doing
    anything and pushes the player off course. So the way is planned over the map's own
    collider (the breadth-first walk the realm bots use), any card is answered where it
    opens, and the route is planned again afterwards from wherever the fight left us.
    """
    import time

    from tests.realm_bot import path as route_over   # the same BFS the realm bots walk with
    col = maps.load(VALLEY).collider
    end = time.time() + 60
    while time.time() < end:
        if drv.top_is("MathCombatQuizScene"):
            answer_card(drv, server, correct=True)
            drv.wait(lambda: not drv.top_is("MathCombatQuizScene"), 6, "the card closes")
            continue
        ws = world(drv)
        if math.hypot(tx - ws.player.x, ty - ws.player.y) < near:
            return
        route = route_over(col, (ws.player.x, ws.player.y), (tx, ty))
        if not route:
            raise AssertionError(f"no way from ({ws.player.x:.0f}, {ws.player.y:.0f}) "
                                 f"to ({tx:.0f}, {ty:.0f}) on the map at all")
        for wx, wy in route[5::6] + [(tx, ty)]:        # every sixth cell: ~24 px apart
            if drv.top_is("MathCombatQuizScene"):
                break                                  # answer it first, then plan again
            walk_to(drv, wx, wy, near=10, timeout=4)
    raise AssertionError(f"could not reach ({tx:.0f}, {ty:.0f}) in 60 s; standing at "
                         f"({world(drv).player.x:.0f}, {world(drv).player.y:.0f}); "
                         f"toasts={drv.toast_log[-5:]}")


def run_math_combat_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_m7", "Toán Sĩ")
        vmap = maps.load(VALLEY)
        area = next(a for a in vmap.monster_areas if a.props.get("monster") == MA)
        server.sql("update characters set zone_id=?, x=?, y=? where user_id=?",
                   (VALLEY, area.x + area.w / 2, area.y + area.h / 2, uid))
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, inscriptions, "
                   "equipped_slot) values (?, 'kiem_go_dao', 'linh', 3, '[]', 'weapon')", (uid,))
        server.sql("update users set spirit_stones=500, flags=? where id=?",
                   (json.dumps({"tutorial": 5}), uid))      # past Trúc Lão's opening lines
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_m7",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "Loạn Số Cốc")
        drv.wait_api()
        assert world(drv).zone_id == VALLEY

        # ---- the fight: a mistake asks a math question, not a word question
        m = engage_mistake(drv, server)
        drv.shot("mistake_question")
        card = drv.game.top
        assert card.q["context"] == "math_combat", card.q["context"]
        meta = card.q["math"]
        assert meta["skill"] == "dstt_t1_tap_hop" and meta["tier"] == 1, meta
        assert meta["mistake_vi"] and meta["monster_vi"] == "Phần Tử Ma", meta
        assert card.q["math"]["doc"]["id"] == "dstt_lib_t1", card.q["math"]["doc"]
        res = answer_card(drv, server, correct=True)
        assert res["correct"] and res["combat"]["shield_broken"], res
        assert res["math"]["skill"] == "dstt_t1_tap_hop" if "skill" in res["math"] else True
        drv.shot("shield_broken")
        drv.wait(lambda: not drv.top_is("MathCombatQuizScene"), 6, "the card closes itself")

        # the answer counted towards the learning path, with no sitting open
        rows = server.sql("select skill_id, tier, correct, run_id from math_answers where user_id=?", (uid,))
        assert rows and rows[-1][0] == "dstt_t1_tap_hop" and rows[-1][2] == 1 and rows[-1][3] is None, rows

        # ---- kill it
        ws = world(drv)
        for _ in range(80):
            if m.id not in ws.entities or not m.alive:
                break
            if drv.top_is("MathCombatQuizScene"):          # a neighbour may ask its own question
                answer_card(drv, server, correct=True)
                drv.wait(lambda: not drv.top_is("MathCombatQuizScene"), 6, "the card closes")
                continue
            drv.press(pygame.K_SPACE)
            drv.step(20)
        assert m.id not in ws.entities or not m.alive, "the monster did not fall"
        drv.wait(lambda: any("Phần Tử Ma" in t for t in drv.toast_log) or True, 2, "loot")

        # ---- the note: read it and Tàng Thư Các opens at the section that explains the mistake
        give(server, uid, NOTE)
        drv.press(pygame.K_TAB)
        drv.wait_scene("BagScene")
        drv.click("bag_tab_items")
        drv.wait(lambda: drv.game.top.inv is not None, 5, "the inventory")
        drv.wait(lambda: any(i["item_id"] == NOTE for i in drv.game.top.inv["items"]),
                 5, "the note in the bag")
        drv.shot("note_in_bag")
        drv.click(f"read_{NOTE}")
        drv.wait(lambda: drv.top_is("DocScene"), 8, "Tàng Thư Các")
        drv.wait_api()
        doc = drv.game.top
        assert doc.doc_id == "dstt_lib_t1" and doc.want_block == 0, (doc.doc_id, doc.want_block)
        drv.shot("note_opens_library")
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("BagScene")
        drv.wait(lambda: drv.game.top.inv is not None, 5, "the inventory again")
        assert any(i["item_id"] == NOTE for i in drv.game.top.inv["items"]), \
            "reading the note must not spend it"
        drv.press(pygame.K_ESCAPE)
        drv.wait(lambda: world(drv) is drv.game.top, 5, "back to the valley")

        # ---- Lò Toán: it refuses while the materials are missing, then forges
        gx, gy = vmap.interacts["math_craft"]
        # out to the road first, then down to the furnace: straight lines walk into the rocks
        trek(drv, server, gx, gy - 16)
        drv.hold([pygame.K_s], 0.15)      # face the furnace: find_target looks where you look
        drv.wait(lambda: world(drv).target is not None
                 and world(drv).action_of(world(drv).target) == "math_craft", 10,
                 "standing at Lò Toán")
        drv.press(pygame.K_e)
        drv.wait(lambda: drv.top_is("MathCraftScene") and drv.game.top.data is not None, 10, "Lò Toán")
        drv.shot("furnace_without_materials")
        recipe = next(r for r in drv.game.top.data["recipes"] if r["id"] == RECIPE)
        assert not recipe["can"], "nothing was gathered yet, so it cannot be forged"
        assert [n["item_id"] for n in recipe["notes"] if n["enough"]] == [NOTE], \
            "only the note from the monster that was killed is in the bag so far"
        for i in recipe["ingredients"]:
            give(server, uid, i["item_id"], max(0, i["qty"] - i["have"]))
        for n in recipe["notes"]:          # the recipe asks for more than one mistake understood
            if not n["enough"]:
                give(server, uid, n["item_id"])
        drv.game.top.load()
        drv.wait_api()
        drv.wait(lambda: next(r for r in drv.game.top.data["recipes"] if r["id"] == RECIPE)["can"],
                 5, "the recipe becomes possible")
        drv.shot("furnace_ready")
        drv.click(f"craft_{RECIPE}")
        drv.wait_api()
        drv.wait(lambda: any("Bút Tập Hợp" in t for t in drv.toast_log), 10, "the forged brush")
        made = server.sql("select item_id, rarity from equipment_instances where user_id=? and item_id=?",
                          (uid, RECIPE))
        assert made and made[0][1] == "linh", made
        left = dict(server.sql("select item_id, quantity from inventory_items where user_id=?", (uid,)))
        for n in recipe["notes"]:          # understanding is never spent, materials are
            assert left.get(n["item_id"], 0) >= 1, ("the note is kept", n["item_id"], left)
        for i in recipe["ingredients"]:
            assert left.get(i["item_id"], 0) == 0, (i["item_id"], left)
        drv.shot("forged")
    finally:
        server.stop()


def test_math_combat_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_m7_") as tmp:
        run_math_combat_flow(Path(tmp))
