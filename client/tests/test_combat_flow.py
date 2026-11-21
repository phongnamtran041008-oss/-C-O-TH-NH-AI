"""Stage 4 through the real client UI: fight a Mực Con (attack freely, its blow lands, the
question card, Hộ Thể, Phản Đòn, kill, loot), take a blow in full from a wrong answer, look at
the cultivation, bag, quest and Yêu Quái Phổ screens, then pass Thiên Kiếp from Luyện Khí 9 to
Trúc Cơ. Every question on the way is a math question at the player's own floor, on the math
card. Out in the wild a question comes only when a monster lands a blow (world_plan.json
"combat"); test_parry_flow drives that rule in detail."""
from __future__ import annotations

import json
import math
import tempfile
import time
from pathlib import Path

import pygame

from client.tests.driver import Driver, ServerProcess, fill_math_answer
from client.tests.test_world_flow import make_account


CARD = "ParryCard"       # the card a monster's blow opens in the wild (rpg.ParryCard)


def world(drv):
    return drv.game.world_scene()


def slime_spot() -> tuple[int, int]:
    """Feet in the middle of the first Mực Con area of Mê Đồ Lâm, by the west gate (read from
    the map: it is generated)."""
    data = json.loads((Path(__file__).resolve().parents[2] / "server" / "maps" / "rung_muc_loang.tmj")
                      .read_text("utf-8"))
    a = next(o for layer in data["layers"] if layer["type"] == "objectgroup" for o in layer["objects"]
             if o.get("type") == "monster_area"
             and {"name": "monster", "type": "string", "value": "ink_slime"} in o.get("properties", []))
    return int(a["x"] + a["width"] // 2) // 16 * 16 + 8, int(a["y"] + a["height"] // 2) // 16 * 16 + 12


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
    """Walk up to the nearest monster of that kind, hit it once so it fights back, then stand
    still in its hit zone until its blow lands and the question card opens.

    Attacking asks nothing in the wild: the card comes with the monster's blow. One click may
    not start the fight - a weapon has a cooldown and the server ignores an attack sent inside
    it, and a click can miss a monster that moved since the frame it was aimed at - so after a
    while without a card this clicks again, as a player would. Not more often than that: a
    flurry of hits could kill a Mực Con before it ever swings. The monster that comes back is
    the one whose blow landed, which is not always the nearest one."""
    import time
    ws = world(drv)
    drv.wait(lambda: nearest(ws, kind) is not None, 10, f"a {kind}")
    end = time.time() + 20
    while time.time() < end:
        if drv.top_is(CARD):                # a blow already landed (a bystander's, maybe)
            return ws.entities.get(getattr(drv.game.top, "monster_id", "")) or nearest(ws, kind)
        m = nearest(ws, kind)
        if m is None:
            break
        if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) >= 34:
            walk_to(drv, m.pos[0], m.pos[1])
            drv.step(5)
            continue
        drv.click_at(drv.game.display.to_window(*ws.world_to_screen(m.pos[0], m.pos[1] - 8)))   # left click = attack
        for _ in range(100):                # its windup and its blow, then attack again
            drv.step(3)
            if drv.top_is(CARD):
                asked = getattr(drv.game.top, "monster_id", "")
                return ws.entities.get(asked) or m
    open_q = server.sql("select ref, created_at from quiz_sessions where answered_at is null")
    raise AssertionError(f"no card from the blow of a {kind}; questions the server still "
                         f"has open: {open_q}; scenes={drv.scene_names()}; toasts={drv.toast_log[-5:]}")


def beat(drv: Driver, ws, m, server: ServerProcess | None = None) -> None:
    """Swing (Space) at a monster until it falls.

    It hits back meanwhile, and so may a bystander: a blow that lands outside the rest window
    opens a card. That is the game working: answer it right (a Phản Đòn) the way a player
    would and go back to swinging."""
    for _ in range(60):
        if not m.alive or m.id not in ws.entities:
            return
        if drv.top_is(CARD):
            asked = getattr(drv.game.top, "monster_id", "")
            assert server is not None, f"{asked} asked a question and this test cannot answer it"
            answer_math(drv, server, correct=True)
            drv.wait(lambda: not drv.top_is(CARD), 6, f"the card of {asked} closes")
            continue
        drv.press(pygame.K_SPACE)
        drv.step(20)
    raise AssertionError("monster did not fall")


def run_combat_flow(workdir: Path, shots: Path | None = None) -> None:
    # every drop roll succeeds (a dev server only): the kill below surely leaves gear on the ground
    server = ServerProcess(workdir, env={"DEV_DROP_MULT": "1000"})
    try:
        url = server.url
        token, uid = make_account(url, "detu_c", "Chiến Sĩ")     # no word learned: none is needed
        # stand at the edge of the Mực Con area in Rừng Mực Loang, with the quest-1 brush
        server.sql("update characters set zone_id='rung_muc_loang', x=?, y=? where user_id=?", (*slime_spot(), uid))
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

        # fight: hitting asks nothing; its blow lands and brings the card, Hộ Thể meanwhile
        m = engage(drv, server)
        drv.shot("combat_question")
        q = drv.game.top.q
        assert q["context"] == "math_combat" and q["math"]["floor"] == 1, q
        assert q["math"]["monster_vi"] == "Mực Con"
        res = answer_math(drv, server, correct=True)
        assert res["combat"]["parry"] and res["combat"]["damage"] > 0, res["combat"]
        rows = server.sql("select skill_id, correct, run_id from math_answers where user_id=?", (uid,))
        assert rows == [(q["math"]["skill"], 1, None)], rows        # the learning log, once
        drv.step(8)
        drv.shot("parry")
        drv.wait(lambda: not drv.top_is(CARD), 6, "card closes by itself")
        beat(drv, ws, m, server)
        drv.wait(lambda: any("Linh Thạch" in t or "Nhận" in t for t in drv.toast_log) or
                 any(f.text.startswith("+") for f in ws.fx.texts), 6, "loot")
        drv.shot("loot")

        # the gear of that kill lies where the monster fell, glowing in its rarity colour; it is
        # already in the bag, but its toast waits until the player walks to it - and shows once
        from client.engine import art2
        if art2.on():
            drv.wait(lambda: any(d.state == "lie" for d in ws.ground_loot.drops), 6, "gear on the ground")
            d = next(x for x in ws.ground_loot.drops if x.state == "lie")
            said = d.toast[0]
            assert said not in drv.toast_log, "the toast waits for the pickup"
            drv.step(6)
            drv.shot("loot_on_the_ground")
            for _ in range(4):                      # a bystander's blow may open a card on the way
                while drv.top_is(CARD):
                    answer_math(drv, server, correct=True)
                    drv.wait(lambda: not drv.top_is(CARD), 6, "the card closes")
                walk_to(drv, d.x, d.y, near=4)
                drv.step(int(1 + 0.4 * 60))
                if said in drv.toast_log:
                    break
            drv.wait(lambda: said in drv.toast_log, 6, "the pickup toast")
            drv.step(20)
            assert drv.toast_log.count(said) == 1 and d not in ws.ground_loot.drops

        # a wrong answer: the blow lands in full, red flash, and the solution on the card
        rest_until = time.time() + res["combat"]["rest"] + 0.5     # past the rest window of the last answer
        while time.time() < rest_until and not drv.top_is(CARD):
            drv.step(5)
        hp0 = drv.game.state.character.get("hp")
        m2 = engage(drv, server)
        res = answer_math(drv, server, correct=False)
        assert res["combat"]["damage_taken"] > 0 and not res["combat"]["parry"]
        drv.step(6)
        drv.shot("guard_break")
        drv.press(pygame.K_RETURN)         # read enough: close it
        drv.wait(lambda: not drv.top_is(CARD), 6, "wrong card closes")
        drv.wait(lambda: drv.game.state.character.get("hp", 0) < hp0, 5, "hp drops")
        drv.press(pygame.K_q)              # Hồi Huyết Đan
        drv.wait_api()
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
