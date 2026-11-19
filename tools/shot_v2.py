"""Screenshots of the running game drawn with the v2 Blender art (client/assets/v2/), 2x world.

Starts a real server, logs test players in through the real client (the test driver) and
saves 3x screenshots (the 1440x810 window) to art/preview/game_*.png:

    game_hub_idle.png         Trúc Lâm Thôn among the stalls and NPCs, standing, a pet beside
    game_hub_walk.png         the same, mid-walk
    game_house_door.png       the player beside a house door
    game_npc_dialog.png       talking to Tiểu Lan (the guide): her dialog open, she plays `talk`
    game_nguyen_anh.png       a Nguyên Anh player (look, flame aura) holding a fan
    game_nguyen_anh_attack.png  the same player mid-attack (a fan attacks with the cast clip)
    game_abode.png            the abode with the garden
    game_wild_monsters.png    Loạn Số Cốc, Trúc Cơ player with a sword, monsters idling
    game_windup.png           a monster winding up, its hit zone on the ground
    game_slash.png            mid-slash with the sword
    game_cast.png             a chiêu (Hỏa Cầu Thuật) being cast
    game_monster_die.png      a monster playing its die clip
    game_player_die.png       the player fallen (die clip held) after a Mặc Kích

The fleeting frames (wind-up, slash, deaths) are caught by a per-frame watch on the game loop.
To keep a wind-up in view, an answered combat card is closed at once instead of after its
2-second display; nothing else is staged.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" tools/shot_v2.py [out_dir]
    SHOT_ONLY=hub|abode|wild|die  ... one scenario
"""
from __future__ import annotations

import json
import math
import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

import pygame  # noqa: E402

from client.tests.driver import Driver, ServerProcess  # noqa: E402
from client.tests.test_combat_flow import nearest, walk_to, world  # noqa: E402
from client.tests.test_math_combat_flow import MA, VALLEY  # noqa: E402
from client.tests.test_math_skill_flow import answer, cast, settle  # noqa: E402
from client.tests.test_world_flow import make_account  # noqa: E402

from app.realtime import maps  # noqa: E402

HUB = "truc_lam_thon"


def calm(drv: Driver) -> None:
    """Mouse off the chat box (hovering it opens the panel) and no chat input focused."""
    pygame.mouse.set_pos((5, 300))
    drv.game.chatbox.close()


def save(drv: Driver, out: Path, name: str, frames: int = 2) -> Path:
    calm(drv)
    drv.step(frames)
    return save_now(drv, out, name)


def save_now(drv: Driver, out: Path, name: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"game_{name}.png"
    pygame.image.save(drv.game.display.window, str(p))
    print("saved", p)
    return p


class Watch:
    """Saves a screenshot on the first frame a condition holds (checked after every game step)."""

    def __init__(self, drv: Driver, out: Path):
        self.drv, self.out, self.items, self.done = drv, out, [], set()
        orig = drv.game.step

        def step(dt, events):
            orig(dt, events)
            for name, pred in self.items:
                if name not in self.done:
                    try:
                        ok = pred()
                    except Exception:                     # noqa: BLE001 - a watch never breaks the run
                        ok = False
                    if ok:
                        save_now(drv, out, name)
                        self.done.add(name)
        drv.game.step = step

    def add(self, name: str, pred) -> None:
        self.items.append((name, pred))


def player(server: ServerProcess, url: str, workdir: Path, name: str, realm: str, zone: str, x: float, y: float,
           weapon: str | None, pet: str | None = None, hp: int | None = None, facing: str = "down") -> Driver:
    workdir.mkdir(parents=True, exist_ok=True)
    token, uid = make_account(url, name, name.replace("_", " ").title())
    server.sql("update characters set zone_id=?, x=?, y=?, realm=?, realm_stage=1, qi=120, facing=? where user_id=?",
               (zone, x, y, realm, facing, uid))
    if hp is not None:
        server.sql("update characters set hp=? where user_id=?", (hp, uid))
    if weapon:
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, inscriptions, "
                   "equipped_slot) values (?, ?, 'linh', 3, '[]', 'weapon')", (uid, weapon))
    if pet:
        server.sql("insert into pets(user_id, pet_type, level, equipped) values (?, ?, 1, 1)", (uid, pet))
    server.sql("update users set spirit_stones=500, flags=? where id=?", (json.dumps({"tutorial": 5}), uid))
    (workdir / "session.json").write_text(json.dumps({"token": token, "username": name, "server_url": url}))
    drv = Driver(url, workdir)
    drv.click("menu_start")
    if zone == "abode":
        drv.wait(lambda: "AbodeScene" in drv.scene_names(), 20, "the abode")
    else:
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 20, zone)
    drv.wait_api()
    drv.wait(lambda: drv.game.state.cult is not None, 10, "cultivation")
    while drv.top_is("DialogScene"):
        drv.press(pygame.K_RETURN)
        drv.step(3)
    calm(drv)
    drv.step(20)
    return drv


def hub_objects():
    from client.engine.tilemap import load_map
    m = load_map(HUB)
    return m


def hub(server, url, workdir, out) -> None:
    m = hub_objects()
    stall = next(o for o in m.objects if o.props.get("sprite") == "stall")
    drv = player(server, url, workdir / "hub", "v2_luyen_khi", "luyen_khi", HUB, stall.x + stall.w / 2,
                 stall.y + stall.h + 30, None, pet="rong")
    save(drv, out, "hub_idle", 30)
    drv.keys.held = {pygame.K_d}
    end = time.perf_counter() + 0.6
    while time.perf_counter() < end:
        drv.step(1)
    save(drv, out, "hub_walk", 1)
    drv.keys.held = set()
    drv.close()

    house = next(o for o in m.objects if o.props.get("sprite") == "house")
    drv = player(server, url, workdir / "door", "v2_cua_nha", "truc_co", HUB, house.x + house.w / 2 + 14,
                 house.y + house.h + 6, "kiem_go_dao", facing="up")
    save(drv, out, "house_door", 30)
    guide = next(o for o in m.objects if o.type == "npc" and o.props.get("npc") == "guide")
    drv.close()

    drv = player(server, url, workdir / "npc", "v2_hoi_chuyen", "luyen_khi", HUB, guide.x + guide.w / 2 + 16,
                 guide.y + guide.h - 1, None, facing="left")
    ws = world(drv)
    drv.wait(lambda: ws.target is not None, 5, "the guide in reach")
    drv.press(pygame.K_e)
    drv.wait(lambda: drv.top_is("DialogScene"), 5, "the guide's dialog")
    save(drv, out, "npc_dialog", 20)
    drv.close()

    drv = player(server, url, workdir / "na", "v2_nguyen_anh", "nguyen_anh", HUB, stall.x + stall.w / 2 + 60,
                 stall.y + stall.h + 30, "quat_giay")
    save(drv, out, "nguyen_anh", 30)
    ws = world(drv)
    ws.my_atk_t0 = drv.game.now           # the attack clip of a fan (no monster in the village to hit)
    while drv.game.now - ws.my_atk_t0 < 0.25:
        drv.step(1)
    save(drv, out, "nguyen_anh_attack", 1)
    drv.close()


def abode(server, url, workdir, out) -> None:
    from client.engine.tilemap import load_map
    am = load_map("abode")
    g = am.find("area", "garden")[0]
    drv = player(server, url, workdir / "abode", "v2_dong_phu", "truc_co", "abode", g.x + g.w / 2,
                 g.y + g.h + 10, None, pet="ngua", facing="up")
    save(drv, out, "abode", 40)
    drv.close()


def wild(server, url, workdir, out) -> None:
    vmap = maps.load(VALLEY)
    area = next(a for a in vmap.monster_areas if a.props.get("monster") == MA)
    drv = player(server, url, workdir / "wild", "v2_truc_co", "truc_co", VALLEY, area.x + area.w / 2,
                 area.y + area.h / 2 + 30, "kiem_go_dao")
    ws = world(drv)
    drv.wait(lambda: nearest(ws, MA) is not None, 10, "monsters")
    drv.step(30)
    save(drv, out, "wild_monsters", 2)

    watch = Watch(drv, out)
    watch.add("windup", lambda: drv.game.top is ws and ws.hurt_flash <= 0 and not drv.game.chatbox.typing and
              any(len(tl) > 5 and 0.1 < tl[3] < tl[4] - 0.3 for tl in ws.teles))
    watch.add("monster_die", lambda: drv.game.top is ws and any(
        e.kind == "m" and e.die_t0 is not None and 0.25 < drv.game.now - e.die_t0 < 0.45
        for e in ws.entities.values()))

    # pick a fight: the monster's card opens (answered wrong, so it stays shielded and engaged)
    m = nearest(ws, MA)
    walk_to(drv, m.pos[0] - 18, m.pos[1], near=8, timeout=4)
    drv.keys.held = set()
    end = time.time() + 15
    while time.time() < end and not drv.top_is("MathCombatQuizScene"):
        m = nearest(ws, MA)
        if m is not None and drv.game.now >= ws.attack_ready:
            ws.attack(m)
        drv.step(3)
    target = getattr(drv.game.top, "monster_id", None)

    # then wait, next to it, for it to wind up with its zone on the ground
    end = time.time() + 40
    while time.time() < end and "windup" not in watch.done:
        if drv.top_is("MathCombatQuizScene"):
            card = drv.game.top
            if not card.result:
                answer(drv, server, False)        # wrong: the shield holds and the fight goes on
            card.finish()      # it would close itself after showing the solution; close it at once
            calm(drv)
            drv.step(2)
            continue
        m = ws.entities.get(target) if target else None
        if m is None or not m.alive:
            m = nearest(ws, MA)
        if m is not None and math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) > 26:
            dx, dy = m.pos[0] - ws.player.x, m.pos[1] - ws.player.y     # short steps: never miss a 0.8 s wind-up
            keys = ([pygame.K_d if dx > 0 else pygame.K_a] if abs(dx) > 4 else []) + \
                   ([pygame.K_s if dy > 0 else pygame.K_w] if abs(dy) > 4 else [])
            drv.hold(keys, 0.05)
        drv.step(1)
    if "windup" not in watch.done:
        print("no telegraph shot in 40 s")

    # mid-slash, between the cards of the fight; the monster dies of it sooner or later
    watch.add("slash", lambda: ws.my_atk_t0 is not None and 0.16 < drv.game.now - ws.my_atk_t0 < 0.3
              and drv.game.top is ws and ws.hurt_flash <= 0)
    end = time.time() + 60
    while time.time() < end and not {"slash", "monster_die"} <= watch.done:
        if drv.top_is("MathCombatQuizScene"):
            card = drv.game.top
            if not card.result:
                answer(drv, server, True)
            card.finish()
            calm(drv)
            drv.step(2)
            continue
        m = nearest(ws, MA)
        if m is None:
            drv.step(5)
            continue
        if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) > 24:
            walk_to(drv, m.pos[0] - 14, m.pos[1], near=8, timeout=1)
            drv.keys.held = set()
        elif drv.game.now >= ws.attack_ready and drv.game.top is ws:
            calm(drv)
            ws.attack(m)
        drv.step(1)
    for name in ("slash", "monster_die"):
        if name not in watch.done:
            print(f"no {name} frame in 60 s")

    # a chiêu: Hỏa Cầu Thuật lands after its card closes
    settle(drv, server)
    card = cast(drv, server, "hoa_cau_thuat")
    answer(drv, server, True)
    drv.wait(lambda: card not in drv.game.scenes, 10, "the card closes")
    drv.wait(lambda: any(f["t0"] is not None for f in ws.skill_fx), 6, "the effect")
    t0 = next(f["t0"] for f in ws.skill_fx if f["t0"] is not None)
    while drv.game.now - t0 < 0.42:
        drv.step(1)
    save(drv, out, "cast", 1)
    perf(drv, ws)
    drv.close()


def die(server, url, workdir, out) -> None:
    """One Sinh Lực left: the first Mặc Kích of a wrong answer brings the player down."""
    vmap = maps.load(VALLEY)
    area = next(a for a in vmap.monster_areas if a.props.get("monster") == MA)
    drv = player(server, url, workdir / "die", "v2_nga_xuong", "truc_co", VALLEY, area.x + area.w / 2,
                 area.y + area.h / 2 + 30, "kiem_go_dao", hp=1)
    ws = world(drv)
    watch = Watch(drv, out)
    watch.add("player_die", lambda: ws.dead and ws.my_die_t0 is not None and drv.game.now - ws.my_die_t0 > 0.8)
    drv.wait(lambda: nearest(ws, MA) is not None, 10, "monsters")
    end = time.time() + 40
    while time.time() < end and "player_die" not in watch.done:
        if drv.top_is("MathCombatQuizScene"):
            card = drv.game.top
            try:
                if not card.result:
                    answer(drv, server, False)
            except AssertionError:                      # fell while answering: the card went with us
                pass
            if card in drv.game.scenes:
                card.finish()
            drv.step(2)
            continue
        m = nearest(ws, MA)
        if m is not None and not ws.dead:
            if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) > 24:
                walk_to(drv, m.pos[0] - 14, m.pos[1], near=8, timeout=1)
                drv.keys.held = set()
            elif drv.game.now >= ws.attack_ready and drv.game.top is ws:
                ws.attack(m)
        drv.step(1)
    if "player_die" not in watch.done:
        print("the player did not fall in 40 s")
    drv.close()


def perf(drv: Driver, ws) -> None:
    """Time the world's draw (the 480x270 game surface) with the v2 art and with the old path."""
    from client.engine import art2
    surf = pygame.Surface((480, 270))
    for label, on in (("v2", True), ("old", False)):
        real = art2.on
        if not on:
            art2.on = lambda: False
        try:
            ws.draw_world(surf)                       # warm the caches
            t0 = time.perf_counter()
            for _ in range(200):
                ws.draw_world(surf)
            ms = (time.perf_counter() - t0) / 200 * 1000
        finally:
            art2.on = real
        print(f"draw_world {label}: {ms:.2f} ms/frame ({len(ws.entities)} entities)")


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "art" / "preview"
    only = os.environ.get("SHOT_ONLY")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        server = ServerProcess(tmp, env={"ACCOUNTS_PER_IP": "50"})     # one account per scenario
        try:
            for name, fn in (("hub", hub), ("abode", abode), ("wild", wild), ("die", die)):
                if only in (None, name):
                    try:
                        fn(server, server.url, tmp, out)
                    except AssertionError as e:          # one scenario failing does not lose the others
                        print(f"{name} failed: {e}")
        finally:
            server.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
