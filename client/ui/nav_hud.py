"""Chỉ Đường in the world and abode HUD: the arrow round the player, the plate with the goal's
name and distance, the khu banner, the keys (N: the picker, M: Thiên Địa Đồ, H: home) and their
buttons. The world scene calls `draw_world` once after drawing the world and `hud` once in its
HUD; the abode does the same."""
from __future__ import annotations

import pygame

from .. import strings_nav_vi as N
from ..engine import chi_duong
from . import nav_arrow

PLATE_BG = (20, 18, 15, 190)
GOLD = "#F2C14E"
PALE = "#F4EBD9"
GREY = "#B9B09E"
WARN = "#F08A8C"
BANNER_Y = 40
BANNER_SECONDS = 3.2


def _z(scene) -> float:
    v = getattr(scene, "view", None)
    return float(getattr(v, "zoom", 1) or 1)


def body_centre(scene) -> tuple[float, float]:
    """The player's body on the screen: a little above the feet, lifted with a flyer."""
    p = scene.player
    x, y = p.x, p.y
    if hasattr(scene, "glide_pos"):
        x, y = scene.glide_pos(scene.my_eid(), p.x, p.y)[:2]
    sx, sy = scene.world_to_screen(x, y)
    z = _z(scene)
    lift = 0.0
    if hasattr(scene, "drawn_alt") and hasattr(scene, "my_eid"):
        lift = scene.drawn_alt.get(scene.my_eid(), 0.0) * z
    return sx, sy - 11 * z - lift


def draw_world(surf: pygame.Surface, scene) -> None:
    """The arrow, over the world (under the name tags and the HUD)."""
    nav = chi_duong.of(scene.game)
    a = nav.arrow(scene)
    if a is None:
        return
    angle, mode = a
    cx, cy = body_centre(scene)
    nav_arrow.draw(surf, cx, cy, angle, _z(scene), scene.game.now, straight=mode in ("straight", "searching"))


def _fit(ui, text: str, size: float, w: float) -> str:
    if ui.text_size(text, size)[0] <= w:
        return text
    while text and ui.text_size(text + "...", size)[0] > w:
        text = text[:-1]
    return text.rstrip() + "..."


PLATE_MAX_W = 196          # between the player card (x < 140) and the N / M buttons (x > 352)


def plate(ui, nav, y: float) -> float:
    """The goal's name and distance (the distance is never cut: a long name is), and a second
    line wrapped to two lines at most; returns the y under it."""
    lines = nav.plate()
    if lines is None:
        return y
    name, far, sub, warn = lines
    tail = f" · {far}"
    tail_w = ui.text_size(tail, 8)[0]
    name = _fit(ui, name, 8, PLATE_MAX_W - 22 - tail_w)
    top_w = ui.text_size(name, 8)[0] + tail_w
    subs = ui.f.wrap(sub, 7, int((PLATE_MAX_W - 22) * ui.s), ui.s)[:2] if sub else []
    if len(subs) == 2:
        subs[1] = _fit(ui, subs[1], 7, PLATE_MAX_W - 22)
    w = min(PLATE_MAX_W, max([top_w] + [ui.text_size(s, 7)[0] for s in subs]) + 22)
    h = 13 + 9 * len(subs)
    x = 240 - w / 2
    ui.fill(x, y, w, h, PLATE_BG)
    ui.border(x, y, w, h, "#BC4749" if warn and nav.status != "straight" else "#8B5A2B")
    img = nav_arrow.sprite(nav_arrow.step_of(-1.5708), nav.status in ("straight", "searching"))
    ui.image(img, x + 7, y + 6.5, zoom=0.5, anchor="center")
    r = ui.text(name, x + 14, y + 2, 8, GOLD)
    ui.text(tail, r.right, y + 2, 8, PALE)
    for i, s in enumerate(subs):
        ui.text(s, x + 14, y + 12 + 9 * i, 7, WARN if warn else GREY)
    return y + h


def banner(ui, nav, now: float, y: float, busy: bool) -> None:
    """The khu just walked into. It waits while toasts are up (they sit right under it), and
    shows for BANNER_SECONDS from the moment it is first drawn."""
    b = nav.banner
    if b is None:
        return
    title, line, warn, until = b
    if until is None:                        # not shown yet
        if busy:
            return
        until = now + BANNER_SECONDS
        nav.banner = (title, line, warn, until)
    elif busy and until - now > 0.3:         # a toast came up under it: make way
        until = now + 0.3
        nav.banner = (title, line, warn, until)
    if now > until:
        nav.banner = None
        return
    fade = min(1.0, (until - now) / 0.6)
    lines = ui.f.wrap(line, 7, int((PLATE_MAX_W + 8 - 28) * ui.s), ui.s) or [""]   # (clear of the card)
    w = max([ui.text_size(title, 9)[0]] + [ui.text_size(s, 7)[0] for s in lines]) + 28
    h = 26 + 9 * (len(lines) - 1)
    x = 240 - w / 2
    edge = "#BC4749" if warn else "#C99A3A"
    ui.fill(x, y, w, h, (20, 18, 15, int(200 * fade)))
    ui.border(x, y, w, h, edge)
    for sx in (x + 6, x + w - 6):            # a small diamond at each end
        ui.fill(sx - 1, y + 12, 3, 3, edge)
    ui.text(title, 240, y + 2, 9, WARN if warn else GOLD, anchor="midtop")
    for i, s in enumerate(lines):
        ui.text(s, 240, y + 15 + 9 * i, 7, WARN if warn else PALE, anchor="midtop")


BAND_NEAR_PX = 80          # a monster this close to the player shows its band (5 tiles)
BAND_PIP = {2: "#F2C14E", 3: "#F08A8C"}
BAND_FIRST = {1: 1, 2: 4, 3: 7}      # the first stage of a band (when no khu says it)


def band_marks(ui, scene) -> dict:
    """eid -> (band, above the player's working stage) for the monsters of band 2 or 3 standing
    near the player or under the mouse; empty on a map without bands and for band 1 (they look
    as they always did)."""
    ents = getattr(scene, "entities", None) or {}
    if not any(getattr(e, "kv", 0) >= 2 for e in ents.values()):
        return {}
    nav = chi_duong.of(scene.game)
    p = scene.player
    hov = None
    if scene.game.top is scene and hasattr(scene, "entity_at"):
        try:
            from ..engine import art2
            mx, my = ui.inp.mouse
            cx, cy = scene.cam
            wx, wy = scene.view.to_world(mx, my) if art2.on() else (mx + cx, my + cy)
            hov = scene.entity_at(wx, wy)
        except Exception:               # (a scene without a camera yet)
            hov = None
    out = {}
    for e in ents.values():
        kv = getattr(e, "kv", 0)
        if kv < 2 or e.kind != "m" or not e.alive:
            continue
        x, y = e.pos[0], e.pos[1]
        if e is not hov and abs(x - p.x) + abs(y - p.y) > BAND_NEAR_PX * 1.4:
            continue
        if e is not hov and (x - p.x) ** 2 + (y - p.y) ** 2 > BAND_NEAR_PX ** 2:
            continue
        k = chi_duong.khu_at(scene.map, x, y)
        lo = chi_duong.num(k[1].get("stage_min")) if k and chi_duong.num(k[1].get("band")) == kv else BAND_FIRST[kv]
        out[e.id] = (kv, nav.above_stage(lo))
    return out


def draw_band_mark(ui, x: float, y: float, band: int, warn: bool) -> None:
    """`band` small diamonds after a name tag (gold for Trung Vực, red for Thâm Xứ), on a dark
    outline; a red underline under them when the band lies above the player's stage."""
    col = BAND_PIP.get(band, GOLD)
    for i in range(band):
        cx = x + 2 + i * 4
        ui.fill(cx - 1.5, y - 1.5, 3, 3, "#1A1A1A")
        ui.fill(cx - 1, y - 1, 2, 2, col)
    if warn:
        ui.fill(x, y + 2.5, band * 4 + 1, 1, "#BC4749")


def band_tip(scene, e) -> str:
    """The line a hovered monster's tooltip gets on a giant land: "Trung Vực · hợp Luyện Khí
    tầng 4-6" (and "cao hơn tu vi của con" when it is); "" for band 0-1."""
    kv = getattr(e, "kv", 0)
    if kv < 2:
        return ""
    nav = chi_duong.of(scene.game)
    k = chi_duong.khu_at(scene.map, e.pos[0], e.pos[1])
    if k and chi_duong.num(k[1].get("band")) == kv:
        lo, hi = chi_duong.num(k[1].get("stage_min")), chi_duong.num(k[1].get("stage_max"))
    else:
        lo, hi = BAND_FIRST[kv], BAND_FIRST[kv] + 2
    fit = (N.BAND_FIT_ONE if lo == hi else N.BAND_FIT).format(realm=nav.realm_vi, lo=lo, hi=hi)
    line = f"{N.BAND_NAMES.get(kv, '')} · {fit}"
    return f"{line} · {N.TOO_HIGH}" if nav.above_stage(lo) else line


def open_picker(scene) -> None:
    from ..scenes.world_map import NavPicker
    g = scene.game
    if not any(isinstance(s, NavPicker) for s in g.scenes):
        g.push(NavPicker(g, scene))


def open_map(scene) -> None:
    from ..scenes.world_map import WorldMapScene
    g = scene.game
    if not any(isinstance(s, WorldMapScene) for s in g.scenes):
        g.push(WorldMapScene(g, scene))


def go_home(scene) -> None:
    nav = chi_duong.of(scene.game)
    nav.set_dest(nav.pick("home"), chi_duong.scene_zone(scene))


def hud(ui, scene, top: bool) -> None:
    """Called once a frame from the HUD of the world or the abode."""
    g = scene.game
    nav = chi_duong.of(g)
    if nav.data is None and not nav.failed:
        nav.refresh()
    nav.update(scene)
    if chi_duong.scene_zone(scene) is None:
        return
    in_world = hasattr(scene, "zone_id")
    ach = g.achievements.clear_y() if getattr(g, "achievements", None) is not None else 0
    y = plate(ui, nav, max(19 if in_world else 4, ach))
    banner(ui, nav, g.now, max(BANNER_Y, y + 3), busy=bool(g.toasts) or bool(ach))
    typing = g.chatbox.typing
    keys = top and not typing
    if in_world:
        mw = scene.minimap.get_size()[0] if getattr(scene, "minimap", None) is not None else 100
        bx = 476 - mw - 4 - 16
        if ui.button("nav_open", bx, 4, 14, 13, "N", key=pygame.K_n if keys else None, enabled=top,
                     tooltip=N.TIP_NAV):
            open_picker(scene)
        if ui.button("nav_map", bx, 19, 14, 13, "M", key=pygame.K_m if keys else None, enabled=top,
                     tooltip=N.TIP_MAP):
            open_map(scene)
        if keys and ui.key(pygame.K_h):
            go_home(scene)
    else:                                   # the abode: H is the hive and M the math hall there
        if ui.button("nav_open", 4, 52, 62, 12, N.BTN_NAV, key=pygame.K_n if keys else None, enabled=top,
                     size=7, tooltip=N.TIP_NAV):
            open_picker(scene)
