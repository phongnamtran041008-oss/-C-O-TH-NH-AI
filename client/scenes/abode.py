"""Động Phủ — the player's own abode (spec 7.1): walk around, talk to Trúc Lão, open the
gacha altar, the hive, the meditation mat, the furnace, fish in the pond, leave by the gate."""
from __future__ import annotations

import math
import random

import pygame

from .. import strings_vi as T
from ..art.palette import rgb
from ..engine import art2, sprites
from ..engine.beeflock import Flock
from ..engine.effects import Effects
from ..engine.tilemap import load_map
from ..ui.dialog import DialogScene
from .base import Scene

SPEED = 74.0
FOOT_W, FOOT_H = 10, 6


class Player:
    def __init__(self, x: float, y: float, facing: str, appearance: dict):
        self.x, self.y = x, y
        self.facing = facing if facing in ("up", "down", "left", "right") else "down"
        self.appearance = appearance
        self.walk_t = 0.0
        self.moving = False

    def foot_rect(self, x=None, y=None) -> pygame.Rect:
        x = self.x if x is None else x
        y = self.y if y is None else y
        return pygame.Rect(int(x - FOOT_W / 2), int(y - FOOT_H), FOOT_W, FOOT_H)

    def frame(self) -> pygame.Surface:
        frames = sprites.character(self.appearance)
        f = (0, 1, 0, 2)[int(self.walk_t * 8) % 4] if self.moving else 0
        return frames[(self.facing, f)]


class AbodeScene(Scene):
    draws_world = True
    modal = False
    toast_y = 70

    def __init__(self, game):
        super().__init__(game)
        self.map = load_map("abode")
        ch = game.state.character
        spawn = self.map.find("spawn")[0]
        x, y = ch.get("x", spawn.x), ch.get("y", spawn.y)
        if ch.get("zone_id") != "abode":
            x, y = spawn.x, spawn.y
        self.player = Player(float(x), float(y), ch.get("facing", "down"), ch.get("appearance", {}))
        if self.map.blocked(self.player.foot_rect()):
            self.player.x, self.player.y = spawn.x, spawn.y
        self.cam = [0, 0]
        from ..engine.view import View
        self.view = View(2 if art2.on() else 1)     # world <-> screen (2x with the v2 art)
        self.t = 0.0
        self.fx = Effects()
        self.target = None
        self.last_saved = (self.player.x, self.player.y, self.player.facing)
        self.save_timer = 0.0
        self.refresh_timer = 0.0
        self.flock = Flock()          # spirit bees flying around (stage 5)
        self.pet_follow = None        # the worn Linh Thú trotting after the player (stage 8)
        hv = [o for o in self.map.objects if o.props.get("action") == "hive"]
        self.hive_obj = hv[0] if hv else None
        self.egg_hint_shown = False
        self.fishing = None           # the FishingScene casting from here (stage 6)
        from .fishing import WeatherWatch
        self.weather = WeatherWatch("abode")

    # ------------------------------------------------------------ lifecycle
    def on_enter(self):
        self.refresh_home()
        self.refresh_me()

    def on_exit(self):
        self.save_position()

    def save_position(self):
        p = self.player
        cur = (round(p.x, 1), round(p.y, 1), p.facing)
        if cur == self.last_saved or not self.api.token:
            return
        self.last_saved = cur
        self.api.post("/character/position", {"zone_id": "abode", "x": cur[0], "y": cur[1], "facing": cur[2]},
                      lambda r: None, lambda e: None)

    # ------------------------------------------------------------ data
    def refresh_me(self):
        def ok(me):
            self.game.state.me.update(me)
        self.api.get("/me", ok, lambda e: None)

    def refresh_home(self, then=None):
        """The hive and its bees (they fly around it, or after me as guards)."""
        def ok(h):
            self.game.state.home = h
            if (not h.get("bees") and not self.egg_hint_shown
                    and any(q["id"] == "lp1_trung_ong" and q["state"] == "active"
                            for q in (self.game.state.quests or {}).get("quests", []))):
                self.egg_hint_shown = True
                self.game.toast(T.STARTER_EGG_HINT, "#C99A3A")
            if then:
                then()
        self.api.get("/hive", ok, self.game.api_error)

    # ------------------------------------------------------------ update
    def update(self, dt, top):
        self.t += dt
        self.fx.update(dt)
        self.update_bees(dt)
        self.update_pet(dt)
        self.weather.update(dt, self.api)
        self.save_timer += dt
        self.refresh_timer += dt
        if self.save_timer > 60:
            self.save_timer = 0
            self.save_position()
        if self.refresh_timer > 45 and top:
            self.refresh_timer = 0
            self.refresh_home()
        if not top or self.game.chatbox.typing:
            self.player.moving = False
            if not top:
                return
            self.target = self.find_target()
            return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        p = self.player
        p.moving = bool(dx or dy)
        if p.moving:
            if dx and dy:
                dx, dy = dx * 0.7071, dy * 0.7071
            if abs(dx) > abs(dy):
                p.facing = "right" if dx > 0 else "left"
            elif dy:
                p.facing = "down" if dy > 0 else "up"
            nx = p.x + dx * SPEED * dt
            if not self.map.blocked(p.foot_rect(nx, p.y)):
                p.x = nx
            ny = p.y + dy * SPEED * dt
            if not self.map.blocked(p.foot_rect(p.x, ny)):
                p.y = ny
            p.walk_t += dt
        self.target = self.find_target()

    # ------------------------------------------------------------ spirit bees (stage 5)
    def bee_list(self) -> list[dict]:
        return self.game.state.home.get("bees", [])

    def hive_decorations(self) -> list[str]:
        return [d["id"] for d in self.game.state.home.get("decorations", []) if d.get("on")]

    def hive_center(self) -> tuple[float, float]:
        o = self.hive_obj
        if o is None:
            return self.player.x, self.player.y - 20
        return o.x + o.w / 2, o.y + 12

    def update_bees(self, dt: float) -> None:
        """Guards follow me; every other bee idles around the hive."""
        now = self.game.now
        hx, hy = self.hive_center()
        guards = 0
        for b in self.bee_list():
            fb = self.flock.get(str(b["id"]), b["species"], hx, hy + 14, now)
            if b["role"] == "guard":
                side = -1 if guards % 2 == 0 else 1
                guards += 1
                fb.update(dt, self.player.x + side * (10 + guards * 3), self.player.y - 2, 7, 90, 18)
            else:
                fb.update(dt, hx, hy + 14, 14, 45, 10)
        self.flock.prune(now)

    def update_pet(self, dt: float) -> None:
        kind = self.game.worn_pet()
        if not kind:
            self.pet_follow = None
            return
        if self.pet_follow is None or self.pet_follow.kind != kind:
            from ..engine.petfollow import PetFollower
            self.pet_follow = PetFollower(self.player.x, self.player.y)
            self.pet_follow.kind = kind
        self.pet_follow.update(dt, self.player.x, self.player.y, self.player.facing)

    def bee_drawables(self, cx: int, cy: int, only: set | None = None) -> list:
        out = []
        species = self.game.state.bee_species
        for fb in self.flock.bees.values():
            if only is not None and id(fb) not in only:
                continue
            look = (species.get(fb.sp) or {}).get("look")
            img = sprites.bee(look, fb.frame(), fb.left)
            out.append((fb.y + 6, img, (int(fb.x - 4) - cx, int(fb.y - fb.z - 4) - cy), (fb.x, fb.y)))
        return out

    def find_target(self):
        p = self.player
        off = {"up": (0, -10), "down": (0, 6), "left": (-10, -3), "right": (10, -3)}[p.facing]
        fx, fy = p.x + off[0], p.y + off[1]
        best, best_d = None, 22.0
        for o in self.map.objects:
            if o.type in ("npc", "interact"):
                cx, cy = o.x + o.w / 2, o.y + o.h
                d = math.hypot(cx - fx, cy - fy)
                if d < best_d:
                    best, best_d = ("object", o), d
        return best

    # ------------------------------------------------------------ interaction
    def interact(self, target) -> None:
        _, obj = target
        self.talking_to = obj     # v2: that NPC talks while its dialog is up
        action = obj.props.get("action") or ("talk" if obj.type == "npc" else None)
        if action == "talk":
            self.game.push(DialogScene(self.game, [random.choice(T.MASTER_IDLE)]))
        elif action == "gacha":
            from .gacha import GachaScene
            self.game.push(GachaScene(self.game, on_close=self.after_gacha))
        elif action == "hive":
            self.open_hive()
        elif action == "alchemy":        # stage 8: the Đan Lô of the abode
            self.save_position()
            self.game.open_alchemy()
        elif action == "meditate":
            from .rpg import MeditateScene
            self.save_position()   # the server checks that we are at home
            self.game.push(MeditateScene(self.game))
        elif action == "exit":
            self.leave_to_village()

    def start_fishing(self, bob) -> None:
        from .fishing import FishingScene
        self.player.moving = False
        self.game.push(FishingScene(self.game, self, "abode", bob))

    def leave_to_village(self) -> None:
        """Through the bamboo gate into the shared world (stage 3)."""
        self.save_position()
        self.game.go_village()

    def after_gacha(self):
        self.refresh_me()

    # ------------------------------------------------------------ drawing
    def npc_talking(self, o) -> bool:
        if o.type != "npc" or getattr(self, "talking_to", None) is not o:
            return False
        return any(type(sc).__name__ == "DialogScene" for sc in self.game.scenes)

    def _cam(self, surf) -> tuple[int, int]:
        w, h = surf.get_size()
        v = self.view
        if art2.on():             # the 2x world (v2 art): the same camera rule as the shared world
            v.zoom = 2
            v.follow(self.player.x, self.player.y - 12, self.map.px_w, self.map.px_h, w, h)
            if self.fx.shake:
                v.shake(random.randint(-3, 3), random.randint(-3, 3))
            self.cam = v.cam
            return v.ox, v.oy
        v.zoom = 1
        cx = int(self.player.x - w / 2)
        cy = int(self.player.y - 12 - h / 2)
        cx = max(0, min(self.map.px_w - w, cx))
        cy = max(0, min(self.map.px_h - h, cy))
        if self.fx.shake:
            cx += random.randint(-2, 2)
            cy += random.randint(-2, 2)
        self.cam = [cx, cy]
        v.ox, v.oy = cx, cy
        return cx, cy

    def _small_text(self, text: str, color: str) -> pygame.Surface:
        return self.game.fonts.render(text, 7, color, 1)

    def world_to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        """Where a world point is on the 480x270 screen (2x world with the v2 art)."""
        return self.view.to_screen(wx, wy)

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        return self.view.to_world(sx, sy)

    def draw_world(self, surf):
        cx, cy = self._cam(surf)
        v = self.view
        if v.zoom == 1:
            self.map.draw_ground(surf, (cx, cy), self.t)
        else:
            self.map.draw_ground_view(surf, v, self.t)
        # y-sorted props, NPC and player
        drawables = []
        for o in self.map.objects:
            name = o.props.get("sprite")
            d2 = art2.object_drawable(o, v, self.t, talking=self.npc_talking(o)) if v.zoom != 1 else None
            if d2 is not None:          # a prop, building or NPC rendered out of Blender
                drawables.append(d2)
            elif name:
                img = sprites.prop(name, int(o.props.get("variant", 0) or 0),
                                   int(self.t * 3) % 4 if name in sprites.ANIMATED_PROPS else 0)
                drawables.append((o.foot_y, v.img(img), v.to_screen(o.x, o.y)))
            elif o.type == "npc":
                img = sprites.truc_lao()[1 if int(self.t * 10) % 37 == 0 else 0]
                drawables.append((o.foot_y, v.img(img), v.to_screen(o.x, o.y)))
        pl = self.player
        me = art2.walker_drawables(self.game.state.character.get("realm"), pl.x, pl.y, pl.facing, pl.moving,
                                   pl.walk_t, self.t, (self.game.state.cult or {}).get("stats", {}).get("weapon"),
                                   v) if v.zoom != 1 else None
        if me is not None:             # the v2 Đạo Sĩ of my realm: aura, glow, body, weapon
            drawables += me
        else:
            img = self.player.frame()
            drawables.append((self.player.y, v.img(img), v.to_screen(self.player.x - 8, self.player.y - 24)))
        pf = self.pet_follow
        bd = art2.beast_drawable(pf.kind, pf.x, pf.y, pf.moving, pf.walk_t, self.t, pf.left, v) \
            if pf is not None and v.zoom != 1 else None
        if bd is not None:
            drawables.append(bd)
        elif pf is not None:             # the worn Linh Thú (stage 8)
            ex, ey = v.to_screen(pf.x - 5, pf.y - 1)
            pygame.draw.ellipse(surf, (40, 50, 30), (ex, ey, int(v.len(10)), int(v.len(3))))
            drawables.append((pf.y, v.img(sprites.pet(pf.kind, pf.frame, pf.left)), v.to_screen(pf.x - 8, pf.y - 13)))
        if self.hive_obj is not None:
            for i, d in enumerate(self.hive_decorations()):   # spec 10.1: trang trí tổ ong
                dimg = sprites.decoration(d, int(self.t * 3) % 4)
                ox = self.hive_obj.x + (-14 - i * 10 if i % 2 == 0 else 28 + (i // 2) * 10)
                oy = self.hive_obj.y + self.hive_obj.h - dimg.get_height()
                dp = art2.decoration(d) if v.zoom != 1 else None
                if dp is not None:     # v2 decoration: its pivot on the old sprite's bottom-centre
                    sx, sy = v.to_screen(ox + dimg.get_width() / 2, oy + dimg.get_height())
                    drawables.append((oy + dimg.get_height(), dp.at(self.t), (sx - dp.pivot[0], sy - dp.pivot[1])))
                    continue
                drawables.append((oy + dimg.get_height(), v.img(dimg), v.to_screen(ox, oy)))
        bcx, bcy = (0, 0) if v.zoom != 1 else (cx, cy)     # at 2x: world positions, converted below
        old_bees = []
        for fb in self.flock.bees.values():
            img = art2.bee_frame(fb.sp, fb.t, fb.left) if v.zoom != 1 else None
            if img is None:
                old_bees.append(fb)
                continue
            ex, ey = v.to_screen(fb.x - 2, fb.y)
            pygame.draw.ellipse(surf, (40, 50, 30), (ex, ey, int(v.len(4)), int(v.len(2))))
            bx, by = v.to_screen(fb.x, fb.y - fb.z)
            drawables.append((fb.y + 6, img, (bx - 16, by - 16)))       # the bee's pivot is its body centre
        keep = {id(fb) for fb in old_bees}
        for fy, bimg, pos, ground in self.bee_drawables(bcx, bcy, keep):
            ex, ey = v.to_screen(ground[0] - 2, ground[1])
            pygame.draw.ellipse(surf, (40, 50, 30), (ex, ey, int(v.len(4)), int(v.len(2))))
            drawables.append((fy, v.img(bimg), v.to_screen(*pos) if v.zoom != 1 else pos))
        for d in sorted(drawables, key=lambda d: d[0]):
            surf.blit(d[1], d[2], None, d[3] if len(d) > 3 else 0)
        if self.fishing is not None:
            from .fishing import draw_rod
            draw_rod(surf, self.fishing, cx, cy, self.t, view=v)
        # interaction marker
        if self.target and self.game.top is self:
            _, obj = self.target
            bob = int(math.sin(self.t * 6) * 2)
            tx, ty = v.to_screen(obj.x + obj.w / 2, obj.y)
            if v.zoom != 1:
                tx, ty = v.to_screen(obj.x + obj.w / 2, obj.y + obj.h)
                ty -= art2.object_height(obj, v)
            pygame.draw.polygon(surf, rgb("o"), [(tx - 3, ty - 8 + bob), (tx + 3, ty - 8 + bob),
                                                 (tx, ty - 4 + bob)])
        self.fx.draw(surf, (cx, cy), self._small_text, self.t, view=v if v.zoom != 1 else None)
        from .world import darkness
        d = darkness(self.game.day_phase())
        if d > 0:  # same day/night as the shared world (spec 7.1)
            night = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            night.fill((18, 22, 58, int(90 * d)))
            surf.blit(night, (0, 0))
        if self.weather.rain:
            from .fishing import draw_rain
            draw_rain(surf, self.t)

    # ------------------------------------------------------------ HUD
    def draw_ui(self, ui):
        top = self.game.top is self
        me = self.game.state.me
        ch = self.game.state.character
        # player card
        ui.fill(4, 4, 128, 34, (244, 235, 217, 235))
        ui.border(4, 4, 128, 34, "#8B5A2B")
        ui.fill(7, 7, 28, 28, "#E3D5BA")
        head = art2.portrait(ch.get("realm")) if art2.on() else None
        if head is not None:              # cropped from the v2 idle-down frame of my realm's look
            ui.image(head, 21, 21, zoom=1, anchor="center")
        else:
            head = self.player.frame().subsurface(pygame.Rect(2, 1, 12, 11)) if self.player.facing != "up" else \
                sprites.character(self.player.appearance)[("down", 0)].subsurface(pygame.Rect(2, 1, 12, 11))
            ui.image(head, 21, 21, zoom=2, anchor="center")
        from .books import portrait_frame
        portrait_frame(ui, me.get("frame"), 7, 7, 28, 28)
        ui.text(ch.get("display_name", ""), 39, 7, 9)
        if me.get("title"):
            ui.text(f"«{me['title']}»", 39, 28, 6, "#B8862E")
        ui.text(T.REALMS.get(ch.get("realm", "pham_nhan"), ""), 39, 19, 8, "#6A994E")
        ui.image((art2.stone_small() or sprites.icon("stone")), 7, 41, zoom=1)
        ui.text(f"{me.get('spirit_stones', 0):,}".replace(",", "."), 22 if art2.stone_small() else 18, 44, 9, "#FFFFFF",
                anchor="midleft")
        ui.text(f"{me.get('spirit_stones', 0):,}".replace(",", "."), 21.5 if art2.stone_small() else 17.5, 43.5, 9,
                "#2B2B2B", anchor="midleft")
        # chat first: while typing, letters must not trigger the hotkeys below
        self.game.chatbox.draw(ui, in_zone=False, enabled=top)
        typing = self.game.chatbox.typing
        # menu buttons
        bx = 480 - 4
        for wid, label, key, action in [("hud_menu", T.HUD_MENU, pygame.K_ESCAPE, self.open_settings),
                                        ("hud_friends", T.HUD_FRIENDS, pygame.K_p, self.game.open_friends),
                                        ("hud_quests", T.HUD_QUESTS, pygame.K_j, self.game.open_quests),
                                        ("hud_char", T.HUD_CHAR, pygame.K_k, self.game.open_char),
                                        ("hud_gacha", T.HUD_GACHA, pygame.K_g, self.open_gacha),
                                        ("hud_hive", T.HUD_HIVE, pygame.K_h, self.open_hive),
                                        ("hud_book", T.HUD_BOOK, pygame.K_b, self.game.open_book),
                                        ("hud_bag", T.HUD_BAG, pygame.K_TAB, self.open_bag),
                                        ("hud_math", T.HUD_MATH, pygame.K_m, self.game.open_math)]:
            w = ui.text_size(label, 8)[0] + 10
            bx -= w + 3
            if ui.button(wid, bx, 252, w, 14, label, key=key if (top and not typing) else None, enabled=top):
                action()
        if top and not typing and ui.key(pygame.K_l):
            self.game.open_library()
        if top and not typing and ui.key(pygame.K_o):
            self.game.open_pets()
        if not top or typing:
            return
        mx, my = ui.inp.mouse
        wx, wy = self.screen_to_world(mx, my)
        # interaction hint
        if self.target:
            _, obj = self.target
            label = T.ACTIONS.get(obj.props.get("action") or ("talk" if obj.type == "npc" else ""), obj.name)
            ui.text(T.PRESS_E.format(action=label), 240, 230, 9, "#FFFFFF", anchor="center")
            if ui.key(pygame.K_e):
                self.interact(self.target)
                return
        # the pond (stage 6, spec 11.1: F at the water)
        from .fishing import water_near
        spot = water_near(self.map, self.player.x, self.player.y, self.player.facing)
        if spot:
            if not self.target:
                ui.text(T.PRESS_F, 240, 230, 9, "#FFFFFF", anchor="center")
            if ui.key(pygame.K_f):
                self.start_fishing(spot[1])
                return
        # clicks in the world
        if ui.inp.clicked and my < 248 and not ui.hover(0, 150, 214, 100):
            for o in self.map.objects:
                if o.type in ("npc", "interact") and o.rect.collidepoint(wx, wy):
                    ui.consume_click()
                    self.interact(("object", o))
                    return

    def open_settings(self):
        from .settings import SettingsScene
        self.game.push(SettingsScene(self.game, in_game=True))

    def open_gacha(self):
        from .gacha import GachaScene
        self.game.push(GachaScene(self.game, on_close=self.after_gacha))

    def open_hive(self):
        self.game.open_hive(on_close=self.refresh_me)

    def open_bag(self):
        from .bag import BagScene
        self.game.push(BagScene(self.game, self))

