"""Stage 4 through the real client UI: fight a Mực Con (attack, Vấn Đạo card, Hộ Thể,
shield break, kill, loot), take a Mặc Kích from a wrong answer, look at the cultivation,
bag, quest and Yêu Quái Phổ screens, then pass Thiên Kiếp from Luyện Khí 9 to Trúc Cơ.
Every question on the way is a math question at the player's own floor, on the math card."""
from __future__ import annotations

import json
import math
import tempfile
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_world_flow import make_account


CARD = "MathCombatQuizScene"       # the card every monster's question opens


def world(drv):
    return drv.game.world_scene()


def answer_math(drv: Driver, server: ServerProcess, correct: bool = True) -> dict:
    """Answer the math question of the card on top through its widgets, reading the key from
    the database (test only), and wait for the verdict."""
    card = drv.game.top
    key = json.loads(server.sql("select answer_key from quiz_sessions where id=?", (card.q["session_id"],))[0][0])
    fill_math_answer(drv, card.q, key, correct)
    drv.wait(lambda: drv.game.top is card and card.result, 10, "the verdict")
    return card.result


def walk_to(drv: Driver, tx: float, ty: float, near: float = 26, timeout: float = 8.0) -> None:
    """Hold the arrow keys toward a point (good enough in the open forest)."""
    import time
    end = time.time() + timeout
    while time.time() < end:
        ws = world(drv)
        dx, dy = tx - ws.player.x, ty - ws.player.y
        if math.hypot(dx, dy) < near:
            break
        keys = []
        if abs(dx) > 4:
            keys.append(pygame.K_d if dx > 0 else pygame.K_a)
        if abs(dy) > 4:
            keys.append(pygame.K_s if dy > 0 else pygame.K_w)
        drv.hold(keys, 0.15)
    drv.keys.held = set()


def nearest(ws, kind: str):
    alive = [e for e in ws.entities.values() if e.kind == "m" and e.mtype == kind and e.alive]
    return min(alive, key=lambda e: math.hypot(e.pos[0] - ws.player.x, e.pos[1] - ws.player.y)) if alive else None


def engage(drv: Driver, server: ServerProcess, kind: str = "ink_slime"):
    """Walk up to the nearest monster of that kind and attack it until its Vấn Đạo card opens.

    One click is not enough. A weapon has a cooldown (0.7 s for a brush, combat.json) and the
    server simply ignores an attack sent inside it - no error, no event - so an attack that
    follows a flurry of swings can land in the dead time and nothing at all happens. A click
    can also miss a monster that moved since the frame it was aimed at. A player clicks again;
    so does this. The monster that comes back is the one that really asked, which is not always
    the nearest one: a bystander can get the swing."""
    import time
    ws = world(drv)
    drv.wait(lambda: nearest(ws, kind) is not None, 10, f"a {kind}")
    end = time.time() + 15
    while time.time() < end:
        m = nearest(ws, kind)
        if m is None:
            break
        if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) >= 34:
            walk_to(drv, m.pos[0], m.pos[1])
            drv.step(5)
            continue
        drv.click_at(drv.game.display.to_window(*ws.world_to_screen(m.pos[0], m.pos[1] - 8)))   # left click = attack
        for _ in range(40):                 # longer than any weapon cooldown, then attack again
            drv.step(3)
            if drv.top_is(CARD):
                asked = getattr(drv.game.top, "monster_id", "")
                return ws.entities.get(asked) or m
    open_q = server.sql("select ref, created_at from quiz_sessions where answered_at is null")
    raise AssertionError(f"no Vấn Đạo card after attacking a {kind}; questions the server still "
                         f"has open: {open_q}; scenes={drv.scene_names()}; toasts={drv.toast_log[-5:]}")


def beat(drv: Driver, ws, m, server: ServerProcess | None = None) -> None:
    """Swing (Space) at a monster whose shield is down until it falls.

    A swing hits whatever is in range and a Mực Con that decides to attack engages by
    itself, so a *bystander* that still has its Mặc Thuẫn up can ask its own question in
    the middle of this (spec 8.1). That is the game working: answer it the way a player
    would and go back to the monster we came for. A question about that monster is a
    different matter - its shield would have to come back, which only elites do."""
    for _ in range(60):
        if not m.alive or m.id not in ws.entities:
            return
        if drv.top_is(CARD):
            asked = getattr(drv.game.top, "monster_id", "")
            assert asked != m.id, f"the Mặc Thuẫn of {m.id} came back"
            assert server is not None, f"{asked} asked a question and this test cannot answer it"
            answer_math(drv, server, correct=True)
            drv.wait(lambda: not drv.top_is(CARD), 6, f"the card of {asked} closes")
            continue
        drv.press(pygame.K_SPACE)
        drv.step(20)
    raise AssertionError("monster did not fall")


def run_combat_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_c", "Chiến Sĩ")     # no word learned: none is needed
        # stand at the edge of the Mực Con area in Rừng Mực Loang, with the quest-1 brush
        server.sql("update characters set zone_id='rung_muc_loang', x=?, y=? where user_id=?", (16 * 18, 16 * 20, uid))
        h = {"Authorization": f"Bearer {token}"}
        import httpx
        inst = server.sql("select count(*) from equipment_instances")[0][0]
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, "
                   "equipped_slot) values (?, 'but_long_go', 'pham', 0, 'weapon')", (uid,))
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, "
                   "equipped_slot) values (?, 'non_la', 'linh', 2, NULL)", (uid,))
        assert inst == 0
        server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, 'hoi_huyet_dan', 3, 0)",
                   (uid,))
        server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, 'muc_tinh', 6, 0)",
                   (uid,))
        httpx.get(url + "/quests", headers=h)
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_c", "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "forest")
        drv.wait_api()
        ws = world(drv)
        assert ws.zone_id == "rung_muc_loang"

        # fight: the first hit brings the Vấn Đạo card, the character is protected meanwhile
        m = engage(drv, server)
        drv.shot("combat_question")
        q = drv.game.top.q
        assert q["context"] == "math_combat" and q["math"]["floor"] == 1, q
        assert q["math"]["monster_vi"] == "Mực Con"
        res = answer_math(drv, server, correct=True)
        assert res["combat"]["shield_broken"]
        rows = server.sql("select skill_id, correct, run_id from math_answers where user_id=?", (uid,))
        assert rows == [(q["math"]["skill"], 1, None)], rows        # the learning log, once
        drv.step(8)
        drv.shot("shield_broken")
        drv.wait(lambda: not drv.top_is(CARD), 6, "card closes by itself")
        beat(drv, ws, m, server)
        drv.wait(lambda: any("Linh Thạch" in t or "Nhận" in t for t in drv.toast_log) or
                 any(f.text.startswith("+") for f in ws.fx.texts), 6, "loot")
        drv.shot("loot")

        # a wrong answer: Mặc Kích (10% of max HP, minus Kháng Mực), red flash
        hp0 = drv.game.state.character.get("hp")
        m2 = engage(drv, server)
        res = answer_math(drv, server, correct=False)
        assert res["combat"]["mac_kich"] > 0
        drv.step(6)
        drv.shot("mac_kich")
        drv.wait(lambda: not drv.top_is(CARD), 6, "wrong card closes")
        drv.wait(lambda: drv.game.state.character.get("hp", 0) < hp0, 5, "hp drops")
        drv.press(pygame.K_q)              # Hồi Huyết Đan
        drv.wait_api()
        # the next question comes after a short pause; answer it and finish the fight
        drv.wait_scene(CARD, 8)
        answer_math(drv, server, correct=True)
        drv.wait(lambda: not drv.top_is(CARD), 6, "card closes")
        beat(drv, ws, m2, server)

        # the screens
        drv.press(pygame.K_k)
        drv.wait_scene("CharacterScene")
        drv.wait(lambda: drv.game.top.inv is not None and drv.game.state.cult, 5, "character data")
        drv.shot("cultivation")
        drv.press(pygame.K_ESCAPE)
        drv.press(pygame.K_TAB)
        drv.wait_scene("BagScene")
        drv.click("bag_tab_gear")
        drv.wait(lambda: drv.game.top.inv is not None, 5, "inventory")
        drv.shot("bag_gear")
        drv.click("bag_tab_items")
        drv.shot("bag_items")
        drv.press(pygame.K_ESCAPE)
        drv.press(pygame.K_j)
        drv.wait_scene("QuestScene")
        drv.wait(lambda: drv.game.state.quests, 5, "quests")
        drv.shot("quests")
        drv.press(pygame.K_ESCAPE)
        drv.press(pygame.K_b)
        drv.wait_scene("BooksScene")
        drv.wait(lambda: drv.game.top.data is not None, 5, "the shelf of phổ")
        drv.click("lib_open_monster")
        drv.wait(lambda: drv.top_is("MonsterBookScene") and drv.game.top.data, 5, "monster book")
        drv.step(3)
        drv.shot("monster_book")
        assert not any("qtypes_vi" in e for e in drv.game.top.data["entries"])
        drv.press(pygame.K_ESCAPE)
        drv.wait_scene("BooksScene")
        drv.press(pygame.K_ESCAPE)                   # and the shelf of phổ under it
        from client.scenes.rpg import ForgeScene
        drv.game.push(ForgeScene(drv.game))
        drv.wait(lambda: drv.game.top.inv is not None, 5, "forge")
        drv.shot("forge")
        nonla = next(e for e in drv.game.top.inv["equipment"] if e["item_id"] == "non_la")
        drv.click(f"forge_{nonla['id']}")
        drv.wait_api()
        drv.press(pygame.K_ESCAPE)

        # Thiên Kiếp from Luyện Khí 9 with full Tu Vi and a Trúc Cơ Đan
        server.sql("update characters set realm='luyen_khi', realm_stage=9, cultivation_xp=500 where user_id=?", (uid,))
        server.sql("insert into inventory_items(user_id, item_id, quantity, bound) values (?, 'truc_co_dan', 1, 1)",
                   (uid,))
        drv.press(pygame.K_k)
        drv.wait_scene("CharacterScene")
        drv.wait(lambda: drv.game.state.cult.get("can_tribulation"), 5, "can break through")
        drv.click("ch_trib")
        drv.wait_scene("TribulationScene")
        drv.shot("tribulation_intro")
        drv.click("trib_go")
        for i in range(20):
            drv.wait_scene("TribulationQuizScene", 8)
            card = drv.game.top
            assert card.q["context"] == "math_tribulation" and card.storm.progress[0] == i + 1, card.q
            assert "math_stop" not in drv.game.ui.widgets               # no pausing a Thiên Kiếp
            if i == 3:
                drv.shot("tribulation_question")
            res = answer_math(drv, server, correct=(i != 5))            # 19/20
            if i == 5:                                                  # a wrong answer: the lightning
                drv.wait(lambda: card.storm.bolts, 3, "lightning")
                drv.shot("tribulation_lightning")
            assert res["correct_so_far"] == (i + 1 if i < 5 else i)
            drv.click("math_next")
        drv.wait(lambda: drv.top_is("TribulationScene") and drv.game.top.state == "done", 8, "result")
        drv.step(10)
        drv.shot("tribulation_passed")
        assert drv.game.top.result["passed"]
        assert server.sql("select realm, realm_stage from characters where user_id=?", (uid,))[0] == ("truc_co", 1)
        drv.close()
    finally:
        server.stop()


def test_combat_and_tribulation_ui():
    with tempfile.TemporaryDirectory() as tmp:
        run_combat_flow(Path(tmp))
