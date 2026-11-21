"""The shared world (spec 7.1, 15.1, 18): Trúc Lâm Thôn, Rừng Mực Loang...

The own character is predicted: every frame's held keys become a movement step that is
applied at once and sent to the server in small batches. Snapshots bring the
authoritative position plus the last batch the server applied; unapplied batches are
replayed on top, so normally nothing visible happens. Everyone else is interpolated 100 ms
in the past between snapshots.
"""
from __future__ import annotations

import math
import random
from collections import deque
from dataclasses import dataclass, field

import pygame

from .. import strings_vi as T
from ..art import skill_fx
from ..art.palette import rgb
from ..art import build as B
from ..engine import art2
from ..engine import combat_vfx as CV
from ..engine import flight as fl
from ..engine import glide as gl
from ..engine import movement as mv
from ..engine import petfollow
from ..engine import sprites
from ..engine.beeflock import Flock
from ..engine.effects import Effects
from ..engine.ground_loot import GroundLoot
from ..engine.tilemap import load_map
from ..engine.vfx import Vfx
from ..net.interpolation import Interpolator
from ..ui.dialog import DialogScene
from ..ui import nav_hud
from . import guide
from .abode import Player
from .base import Scene

FACING = ("down", "up", "left", "right")
SPEED = 74.0
SEND_EVERY = 0.05          # 20 input messages a second at most
BUBBLE_SECONDS = 5.0

# The hotbar: the six chiêu thức (M9), keys 1-6.
MSKILL_KEYS = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6)
MSKILL_KEY_NAMES = "123456"
MSKILL_ROW = (252, 226)            # top-left of the first slot; a slot is 22 px, 24 px apart
MSKILL_NEAR = 140                  # a chiêu aimed at "the nearest monster" looks this far (px)
def mskill_initials(name_vi: str) -> str:
    """"Hỏa Cầu Thuật" -> "HC": what a slot shows when there is no icon to draw."""
    return "".join(w[0] for w in name_vi.split()[:2]).upper()


MSKILL_TARGETLESS = ("ward", "shield", "heal", "domain")     # chiêu cast with no monster aimed at


def chieu_extra(ev: dict) -> dict:
    """What a `mskill` event says beyond its one target (Chiêu Thức II): every monster struck,
    in order (hits), where a line ends (end) and how long what it leaves lasts (d)."""
    out: dict = {"hits": [(float(h[1]), float(h[2])) for h in ev.get("hits") or [] if len(h) >= 3]}
    if ev.get("ex") is not None and ev.get("ey") is not None:
        out["end"] = (float(ev["ex"]), float(ev["ey"]))
    if ev.get("d") is not None:
        out["d"] = float(ev["d"])
    return out


CAST_SHEET = "dao_si_luyen_khi"    # the Đạo Sĩ sheet a caster is drawn from (no realm mapping yet)
CAST_CHANNEL_MAX = 40.0            # a channel the server never finished stops looking like one after this
WAITING_Q_MAX = 2.5                # a question waits this long at most behind the result of the last one


@dataclass
class Ent:
    id: str
    kind: str                      # "p" player, "m" monster
    name: str
    uid: int | None = None
    appearance: dict = field(default_factory=dict)
    mtype: str = ""
    realm: str = "pham_nhan"
    walk_t: float = 0.0
    pos: tuple = (0.0, 0.0, 0, 0)  # last drawn (x, y, facing, moving)
    hp: int = 100                  # percent
    shield: int = 0
    alive: int = 1
    rank: str = "normal"
    weapon: str | None = None
    hurt_t: float = 0.0            # flashes white when hit
    swing_t: float = 0.0           # attack animation
    bees: list = field(default_factory=list)   # guard bees: [species, hp %, target id, down]
    pet: str | None = None                     # worn Linh Thú (stage 8)
    ghost: bool = False                        # out of health in a bí cảnh (stage 9)
    realm_id: str = ""                         # a Khe Nứt Mực rift ("r"): where it leads
    left: float = 0.0                          # rift: seconds until it closes, when first seen
    seen: float = 0.0
    # v2 animation state (game clock times; None = not playing)
    die_t0: float | None = None                # the die clip started
    atk_t0: float | None = None                # a monster's blow landed / a player's attack swing
    aim: tuple | None = None                   # where a winding-up monster is aiming
    # Thiên Địa Đồ: a linh thú in the wild ("m" with beast), a player riding their mount
    beast: bool = False
    need: int = 0                              # Phản Đòn it takes to tame this beast
    ride: bool = False
    fly: int = 0                               # ngự kiếm: 1 low flight, 2 free flight (0 on the ground)
    fsword: str = ""                           # the flying sword under it
    stage: int = 0                             # a player's realm stage (its kiếm khí tier)
    lc: int = 0                                # a player's linh căn giai (1-9; 0 = none)
    kv: int = 0                                # a monster's band of tu vi on a giant land (0: none)
    kick: tuple | None = None                 # a struck body's recoil (combat_vfx.recoil)
    dissolve: bool = False                     # its death turns to light (the VFX layer took it over)


_GHOST: dict = {}


def tele_shape(tl: list) -> dict:
    """The shape of a hit zone: [x, y, r, left, total, monster, shape]; an old entry is a circle."""
    return tl[6] if len(tl) > 6 and isinstance(tl[6], dict) else {"sh": "circle", "a": 0.0, "deg": 90.0, "w": 12.0}


def tele_points(sx: float, sy: float, r: float, shape: dict, k: float = 1.0) -> list[tuple[float, float]]:
    """The outline of a cone or line from its origin (screen px), filled to `k` of its reach."""
    a = math.radians(shape["a"])
    reach = max(1.0, r * k)
    if shape["sh"] == "cone":
        half = math.radians(min(shape["deg"], 179) / 2)
        pts = [(sx, sy)]
        for i in range(9):
            b = a - half + 2 * half * i / 8
            pts.append((sx + math.cos(b) * reach, sy + math.sin(b) * reach))
        return pts
    w = shape["w"] / 2
    ca, sa = math.cos(a), math.sin(a)
    return [(sx - sa * w, sy + ca * w), (sx + ca * reach - sa * w, sy + sa * reach + ca * w),
            (sx + ca * reach + sa * w, sy + sa * reach - ca * w), (sx + sa * w, sy - ca * w)]


def draw_tele_poly(surf: pygame.Surface, sx: float, sy: float, r: float, shape: dict, k: float,
                   outline_only: bool = False) -> None:
    """A cone or line drawn with plain polygons (no v2 sheet): the whole zone faint, the part
    already filled stronger, and its rim."""
    full = tele_points(sx, sy, r, shape)
    if outline_only:
        pygame.draw.polygon(surf, (255, 214, 120), full, 1)
        return
    xs, ys = [q[0] for q in full], [q[1] for q in full]
    left, top = int(min(xs)) - 2, int(min(ys)) - 2
    zone = pygame.Surface((int(max(xs)) - left + 4, int(max(ys)) - top + 4), pygame.SRCALPHA)
    shift = [(qx - left, qy - top) for qx, qy in full]
    pygame.draw.polygon(zone, (188, 71, 73, 50), shift)
    if k > 0.05:
        part = [(qx - left, qy - top) for qx, qy in tele_points(sx, sy, r, shape, k)]
        pygame.draw.polygon(zone, (188, 71, 73, 110), part)
    pygame.draw.polygon(zone, (142, 53, 55, 200), shift, 1)
    surf.blit(zone, (left, top))


def ghostly(img: pygame.Surface) -> pygame.Surface:
    """A bí cảnh ghost: the same sprite, pale and see-through."""
    key = id(img)
    if key not in _GHOST:
        g = img.copy()
        g.fill((170, 190, 220, 0), special_flags=pygame.BLEND_RGBA_MAX)
        g.set_alpha(120)
        _GHOST[key] = g
    return _GHOST[key]


@dataclass
class WeaponSpot:
    """A weapon lying in a land (Thiên Địa Đồ), as GET /weapons of the weapon system lists it:
    `pos` is a tile of this map; state available / taken / locked (with `reason_vi`)."""
    id: str
    land: str
    tx: int
    ty: int
    state: str = "available"
    reason_vi: str = ""
    name_vi: str = ""
    icon: tuple | None = None          # (icon set, icon id) of client/assets/v2/icons

    @property
    def x(self) -> float:
        return self.tx * 16 + 8

    @property
    def y(self) -> float:
        return self.ty * 16 + 12

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y


def weapon_icon_ref(row: dict) -> tuple | None:
    """The weapon icon of a GET /weapons row: its `weapon`/`icon` id, else its id without the
    quality (kiem_1_ha -> kiem_1), looked up in the two weapon icon sets."""
    rid = str(row.get("id", ""))
    for cand in (row.get("weapon"), row.get("icon"), rid, rid.rsplit("_", 1)[0]):
        if not cand:
            continue
        for set_id in ("weapons_a", "weapons_b"):
            try:
                if cand in art2.icon_ids(set_id):
                    return set_id, cand
            except Exception:
                return None
    return None


def weapon_spots_from(data, land: str | None) -> list[WeaponSpot]:
    """The spots of this land in a GET /weapons answer: its "placed" list (the weapons lying in the
    lands; "weapons" is the player's own), or a bare list; anything malformed is skipped, so a
    weapon system still being written cannot break the world."""
    rows = (data.get("placed") or []) if isinstance(data, dict) else data
    out = []
    for w in rows if isinstance(rows, list) else []:
        pos = w.get("pos") if isinstance(w, dict) else None
        if not land or w.get("land") != land or not isinstance(pos, (list, tuple)) or len(pos) != 2:
            continue
        try:
            tx, ty = int(pos[0]), int(pos[1])
        except (TypeError, ValueError):
            continue
        out.append(WeaponSpot(str(w.get("id", "")), land, tx, ty, str(w.get("state", "available")),
                              str(w.get("reason_vi") or ""), str(w.get("name_vi") or ""), weapon_icon_ref(w)))
    return out


def old_prop(name: str, variant: int, frame: int):
    """The code-drawn sprite of a map prop, or None for the props that only exist in the v2 art
    (boulder, crystal, cloud_puff... used by the lands of Thiên Địa Đồ)."""
    try:
        return sprites.prop(name, variant, frame)
    except KeyError:
        return None


SPOT_MARGIN = 160          # screen px: a weapon spot's icon, ring and light column (96 px) never reach further


def off_screen(v, wx: float, wy: float, size: tuple[int, int], margin: int = SPOT_MARGIN) -> bool:
    """Is world point (wx, wy) so far off a screen of `size` that nothing drawn round it shows?"""
    sx, sy = v.to_screen(wx, wy)
    return sx < -margin or sy < -margin or sx > size[0] + margin or sy > size[1] + margin


def map_collider(tmap) -> mv.Collider:
    if hasattr(tmap, "collider"):       # a TileMap builds its grid once, not at every zone change
        return tmap.collider()
    solids = [(r.x, r.y, r.w, r.h) for r in tmap.solids]
    return mv.Collider(tmap.px_w, tmap.px_h, solids)


def darkness(phase: float) -> float:
    """0 by day, 1 at night (spec 7.1: one game day = two real hours)."""
    h = (phase % 1.0) * 24
    if 6 <= h < 18:
        return 0.0
    if 18 <= h < 20:
        return (h - 18) / 2
    if 4 <= h < 6:
        return 1 - (h - 4) / 2
    return 1.0


_WHITE: dict = {}
_FLIP: dict = {}


def white(img: pygame.Surface) -> pygame.Surface:
    """The hit flash: the same sprite painted white."""
    key = id(img)
    if key not in _WHITE:
        w = img.copy()
        w.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
        _WHITE[key] = w
    return _WHITE[key]


def flipped(img: pygame.Surface) -> pygame.Surface:
    key = id(img)
    if key not in _FLIP:
        _FLIP[key] = pygame.transform.flip(img, True, False)
    return _FLIP[key]


_RINGS: dict = {}


def shield_ring(w: int, frame: int) -> pygame.Surface:
    """Mặc Thuẫn: a dark, slowly turning ring of ink around the monster."""
    key = (w, frame)
    if key not in _RINGS:
        s = pygame.Surface((w, w), pygame.SRCALPHA)
        r = w // 2 - 1
        for i in range(16):
            if (i + frame) % 4 == 0:
                continue
            a0 = i / 16 * 6.283
            pygame.draw.arc(s, (26, 26, 26, 200), s.get_rect().inflate(-2, -2), a0, a0 + 0.35, 2)
        pygame.draw.circle(s, (90, 90, 90, 40), (w // 2, w // 2), r)
        _RINGS[key] = s
    return _RINGS[key]


_WEAPONS: dict = {}


# Thiên Địa Đồ: the weapons of the plan come as "<type>_<grade>" (kiem_3). Their reach is the "range"
# of world_plan.json weapon_types (the server decides every hit; this only aims the auto-target - a
# client test checks the two agree), and with the v2 art off each type is drawn as the nearest
# code-drawn weapon.
PLAN_WEAPON_RANGE = {"kiem": 26, "dao": 28, "ho_lo": 40, "thuong": 38, "chuy": 24, "cung": 60,
                     "truong": 46, "phien": 32, "kich": 34, "roi": 44, "am_khi": 52, "luan": 48, "phu": 22,
                     "cam": 50}
PLAN_WEAPON_LOOK = {"kiem": "sword", "dao": "sabre", "ho_lo": "gourd", "thuong": "spear", "chuy": "hammer",
                    "cung": "bow", "truong": "staff", "phien": "fan", "kich": "spear", "roi": "sabre",
                    "am_khi": "sword", "luan": "fan", "phu": "hammer", "cam": "staff"}


def plan_weapon_type(kind: str | None) -> str | None:
    """'kiem' for 'kiem_3'; None for an old weapon kind (brush, sword...) or nothing."""
    if not kind:
        return None
    t, _, grade = kind.rpartition("_")
    return t if grade.isdigit() and t in PLAN_WEAPON_RANGE else None


def weapon_img(kind: str, facing: str, swing: float) -> pygame.Surface:
    """A small weapon drawn over the hand (spec 7.2: gear changes the look)."""
    kind = PLAN_WEAPON_LOOK.get(plan_weapon_type(kind) or "", kind)
    key = (kind, facing, swing > 0.12)
    if key not in _WEAPONS:
        s = pygame.Surface((12, 12), pygame.SRCALPHA)
        shaft = {"brush": "b", "sword": "t", "fan": "w", "staff": "V", "sabre": "t", "spear": "b",
                 "hammer": "b"}.get(kind, "b")
        tip = {"brush": "K", "sword": "W", "fan": "r", "staff": "n", "sabre": "W", "spear": "W",
               "hammer": "k"}.get(kind, "K")
        length = {"brush": 8, "sword": 9, "fan": 5, "staff": 11, "sabre": 8, "spear": 11, "hammer": 7}.get(kind, 8)
        if kind == "bow":
            pygame.draw.arc(s, rgb("b"), (2, 0, 8, 12), -1.4, 1.4, 2)
            pygame.draw.line(s, rgb("w"), (6, 1), (6, 11))
        elif kind == "gourd":
            pygame.draw.circle(s, rgb("o"), (6, 8), 3)
            pygame.draw.circle(s, rgb("o"), (6, 3), 2)
            pygame.draw.circle(s, rgb("k"), (6, 8), 3, 1)
        elif kind == "hammer":
            pygame.draw.line(s, rgb(shaft), (6, 11), (6, 11 - length), 2)
            pygame.draw.rect(s, rgb(tip), (3, 11 - length - 2, 7, 4))
        elif kind == "fan":
            pygame.draw.polygon(s, rgb("w"), [(6, 10), (1, 3), (11, 3)])
            pygame.draw.polygon(s, rgb("k"), [(6, 10), (1, 3), (11, 3)], 1)
            pygame.draw.line(s, rgb("r"), (2, 4), (10, 4))
        else:
            pygame.draw.line(s, rgb(shaft), (6, 11), (6, 11 - length), 2 if kind != "sword" else 1)
            pygame.draw.rect(s, rgb(tip), (5, 11 - length - 1, 3, 3 if kind == "brush" else 2))
            if kind == "sword":
                pygame.draw.line(s, rgb("o"), (4, 9), (8, 9))
        angle = {"down": 160, "up": -20, "left": 70, "right": -70}[facing] + (-60 if swing > 0.12 else 0)
        _WEAPONS[key] = pygame.transform.rotate(s, angle)
    return _WEAPONS[key]


def weapon_pos(x: float, y: float, facing: str, cx: int, cy: int) -> tuple[int, int]:
    ox, oy = {"down": (2, -16), "up": (-10, -18), "left": (-14, -16), "right": (2, -16)}[facing]
    return int(x + ox) - cx, int(y + oy) - cy


def npc_head(kind: str) -> pygame.Surface:
    """The dialog portrait of an NPC: its v2 head when there is one, else the old 16x24 sprite."""
    return art2.npc_portrait(kind) or sprites.npc(kind)[("down", 0)]


def face_to(dx: float, dy: float, default: str = "down") -> str:
    if abs(dx) < 0.5 and abs(dy) < 0.5:
        return default
    return ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")


# the colours of the nine linh căn giai (server/data/linh_can.json `giai[].color`; a test keeps them equal)
LC_COLORS = ("#C9C4B8", "#C9A44A", "#4F8FD8", "#9B5FD0", "#F2C230", "#FFE9A8", "#5CE1E6", "#FF6A3D", "#A77BFF")
# a weapon spot's id ends in its phẩm; the phẩm glows in its rarity (world_plan.json `qualities`)
QUALITY_RARITY = {"ha": "pham", "trung": "linh", "thuong": "huyen", "cuc": "dia", "tuyet": "thien"}


def spot_rarity(spot_id: str) -> str:
    return QUALITY_RARITY.get(str(spot_id).rpartition("_")[2], "pham")


V2_HEAD = 55                       # a v2 character's name tag sits this far above the feet
V2_TELE_RELEASE = 0.25             # how long the hit zone flashes after the blow lands


class WorldScene(Scene):
    draws_world = True
    modal = False
    # ngự kiếm defaults, read by helpers a scene built piecemeal (tests) may call before __init__ ran
    fly = 0
    flight: dict | None = None
    g_down: float | None = None
    drawn_alt: dict = {}           # (only ever replaced, never changed in place)

    @property
    def toast_y(self) -> int:
        """Toasts sit under the HUD card; over the bí cảnh result panel they move to the very top."""
        return 4 if (self.realm is not None and self.realm.ended) else 70

    def __init__(self, game, zone_id: str, via: str = "resume", zone_msg: dict | None = None):
        super().__init__(game)
        self.zone_id = zone_id
        self.via = via
        self.map = load_map(zone_id)
        self.col = map_collider(self.map)
        ch = game.state.character
        sx, sy = self.map.find("spawn")[0].x, self.map.find("spawn")[0].y
        self.player = Player(float(sx), float(sy), ch.get("facing", "down"), ch.get("appearance", {}))
        self.joined = False
        self.join_sent_at: float | None = None
        self.waiting_zone: float | None = None
        self.portal_cool = 0.0
        self.seq = 0
        self.batch: list[list[int]] = []
        self.batch_t = 0.0
        self.ms_rem = 0.0
        self.pending: deque = deque()
        self.corrections = 0
        self.entities: dict[str, Ent] = {}
        self.interp = Interpolator()
        self.bubbles: dict[str, tuple[str, float]] = {}
        self.channel = 1
        self.channels: list[dict] = []
        self.zone_name = T.ZONE_NAMES.get(zone_id, zone_id)
        self.cam = [0, 0]
        from ..engine.view import View
        self.view = View(2 if art2.on() else 1)   # world <-> screen (2x with the v2 art)
        self.t = 0.0
        self.fx = Effects()
        self.fx.stack_texts = art2.on()
        from ..config import IN_BROWSER
        self.vfx = Vfx(reduced=bool(getattr(game.cfg, "reduce_effects", False)), web=IN_BROWSER)
        self.vfx.resolve = self.vfx_where
        self.vfx_hold: dict[str, float] = {}      # attacker eid -> until when its hits wait for the blade
        self.vfx_held: dict[str, float] = {}      # monster eid -> until when (its death waits too)
        self.vfx_late: list[tuple[float, dict]] = []   # events waiting for the blow to land on screen
        self.vfx_bodies: dict[str, tuple] = {}    # eid -> its last drawn layers (for afterimages)
        self.ground_loot = GroundLoot()            # gear lying where monsters died, glowing by phẩm
        self.parried: dict[str, tuple] = {}       # monster eid -> (who parried it, when): a Phản Đòn kill
        self.frozen: pygame.Surface | None = None  # the world's picture held through a hit-stop
        self.target = None
        self.land_id: str | None = None           # Thiên Địa Đồ: the land this zone is (from the zone message)
        self.weapon_spots: list[WeaponSpot] = []  # the weapons lying here (GET /weapons; none without it)
        self.portal_refused: str | None = None    # a land's door said no: not again until we step out
        self.portal_target: str | None = None
        self.minimap = self._build_minimap()
        self.teles: list[list] = []          # [x, y, r, time_left, total]
        self.hurt_flash = 0.0
        self.swing_t = 0.0
        self.dead = False
        self.my_die_t0: float | None = None       # v2: my die clip started
        self.my_atk_t0: float | None = None       # v2: my attack swing started
        self.my_hurt_t0: float | None = None      # v2: my hit clip started
        self.sparks: list[list] = []              # v2 one-shot FX: [fx id, x, y, t0]
        self.mskills: list[dict] | None = None    # M9: GET /math/skills (None: not loaded, or an old server)
        self.mskill_ready: dict[str, float] = {}
        self.mskill_loadout: list = []            # Công Pháp: the chiêu id (or None) of each slot, keys 1-6
        self.bells: dict[str, float] = {}         # Kim Chung Tráo: caster eid -> when its bell lifts
        self.casting: dict[str, dict] = {}        # eid -> the chiêu animation it is playing
        self.skill_fx: list[dict] = []            # chiêu effects in flight
        self.waiting_q: tuple[dict, float] | None = None   # a "q" message held back, and when it came
        # the open-world rule (world_plan.json "combat", sent with the zone): None = Vấn Đạo (a bí cảnh)
        self.rule: dict | None = None
        self.dodge_ready = 0.0
        self.dodging: dict[str, float] = {}       # eid -> when its Né Đòn clip started
        self.stunned: dict[str, float] = {}       # monster eid -> until when a Phản Đòn stuns it
        self.attack_ready = 0.0
        # Thiên Địa Đồ: thần thông of Luyện Khí and the linh thú (sent with the zone; None in a bí cảnh)
        self.abilities: dict | None = None
        self.riding = False
        self.ride_mult = 1.0
        self.glide_ready = 0.0
        self.tran_ready = 0.0
        self.glides: dict[str, tuple] = {}         # eid -> (t0, x0, y0, x1, y1, seconds) of a glide in flight
        # ngự kiếm (G held): my rung in the air as predicted (0 on the ground), the gauge, the
        # altitude of every flyer drawn (engine/flight.py), G's press time, the camera's lead
        self.flight: dict | None = None            # the numbers sent with the zone (abilities.flight_view)
        self.fly = 0
        self.fly_gauge = 0.0
        self.flyers: dict[str, fl.Flyer] = {}
        self.g_down: float | None = None
        self.cam_lead = [0.0, 0.0]
        self.cam_dip = 0.0
        self.fly_fx_t: dict[str, float] = {}       # eid -> when its last spray / mote was spawned
        self.fly_shadows: list = []                # blits of the shadows under the flyers this frame
        self.drawn_alt: dict[str, float] = {}      # eid -> world px it was drawn above its feet
        self.formations: list[list] = []           # [x, y, r, until, fx id] laid on the ground here
        self.taming: dict[str, dict] = {}          # beast eid -> {"n", "need", "yielded", "name"} (my taming)
        self.sniffed: list | None = None           # Linh Hồ: the weapons it smells nearby
        self.sniff_t = 0.0
        self.no_nose: str | None = None            # the worn pet that turned out to have no nose
        self.flock = Flock()                 # guard bees (stage 5), drawn flying around their owner
        self.pet_follow: dict = {}           # Linh Thú trotting after their owners (stage 8): eid -> PetFollower
        self.my_bees: list = []              # [id, species, hp, max hp, seconds resting, target]
        self.bee_hits = 0
        self.fishing = None                  # the FishingScene casting from here (stage 6)
        from .fishing import WeatherWatch
        self.weather = WeatherWatch(zone_id)
        self.ghost = False                   # stage 9: a ghost following the party in a bí cảnh
        from .realm import RealmView
        self.realm = RealmView(self) if zone_id == "bi_canh" else None
        if zone_msg:
            self.apply_zone(zone_msg)
        self.load_mskills()

    def load_mskills(self) -> None:
        """The six chiêu thức with what this player may cast now (the open floor decides). A server
        without them answers 404: the row is then simply not drawn."""
        def ok(d):
            self.apply_mskills(d)
        self.game.api.get("/math/skills", ok, lambda e: None)

    def apply_mskills(self, d: dict) -> None:
        """GET /math/skills (or the answer of a saved Công Pháp): every chiêu, the six slots of
        keys 1-6, and the chiêu learned since the last look - announced once, here."""
        self.mskills = d.get("skills") or []
        self.mskill_loadout = list(d.get("loadout") or [s["id"] for s in self.mskills[:len(MSKILL_KEYS)]])
        for n in d.get("new") or []:
            self.announce_chieu(n)

    def announce_chieu(self, n: dict) -> None:
        """A chiêu just earned on Đạo Thụ: a gold toast and the stage-up light round the player."""
        self.game.toast(T.CHIEU_NEW.format(name=n.get("name_vi", "")), "#B8860B", 4.0)
        vf = getattr(self, "vfx", None)
        if vf is not None and art2.on() and getattr(self, "player", None) is not None:
            CV.stage_up(vf, self.player.x, self.player.y, follow=f"p{self.game.state.me.get('id')}")

    def slot_skill(self, i: int) -> dict | None:
        """The chiêu on slot i (keys 1-6) of the Công Pháp bar, or None for an empty slot."""
        ids = getattr(self, "mskill_loadout", None) or [s["id"] for s in (self.mskills or [])[:len(MSKILL_KEYS)]]
        sid = ids[i] if i < len(ids) else None
        return next((s for s in self.mskills or [] if s["id"] == sid), None) if sid else None

    def open_cong_phap(self) -> None:
        from .cong_phap import CongPhapScene
        if self.mskills:
            self.game.push(CongPhapScene(self.game, self))

    # ------------------------------------------------------------ network
    @property
    def net(self):
        return self.game.net

    def request_join(self) -> None:
        if self.net is not None and self.net.online:
            self.net.send({"t": "join", "zone": self.zone_id, "via": self.via})
            self.join_sent_at = self.game.now

    def on_net(self, m: dict) -> None:
        t = m.get("t")
        if t == "welcome":  # (re)connected: ask for our place back
            self.joined = False
            if not (m.get("zone") == "abode" and self.via == "abode"):
                self.via = "resume"   # the server still has us here (or saved us here)
            self.join_sent_at = None
            self.pending.clear()
            self.batch = []
        elif t == "zone":
            z = m.get("zone")
            self.collect_loot()                    # leaving (or re-entering): what lies here goes to the bag
            if z == "abode":
                self.game.enter_abode(m.get("x"), m.get("y"), m.get("f", "up"))
            elif z != self.zone_id:
                self.game.replace_all(WorldScene(self.game, z, zone_msg=m))
            else:
                self.apply_zone(m)
        elif t == "snap" and self.joined:
            self.apply_snapshot(m)
        elif t == "error":
            code = m.get("code")
            if code in ("not_at_portal", "realm_too_low", "zone_full", "not_in_zone", "land_locked"):
                self.waiting_zone = None
                self.portal_cool = 2.0
            if code == "land_locked":         # Thiên Địa Đồ: the reason names what is missing
                self.portal_refused = self.portal_target
            if not self.joined and m.get("zone") == "abode":  # cannot return to where we were
                self.game.enter_abode(None, None, "down")
                return
            self.game.toast(m.get("message_vi", ""), "#BC4749")
        elif t == "chat":
            eid = (m.get("from") or {}).get("id")
            if m.get("ch") in ("zone", "world") and eid:
                self.bubbles[eid] = (m.get("text", ""), self.game.now + BUBBLE_SECONDS)
        elif t == "q":  # a Vấn Đạo question: Hộ Thể until answered (spec 8.1)
            from .quiz import CombatCard
            self.flush_inputs()
            self.player.moving = False
            for sc in self.game.scenes:
                if isinstance(sc, CombatCard):
                    if sc.result:    # only showing the result of the last question: the new one waits for it
                        self.waiting_q = (m, self.game.now)
                    return
            self.open_question(m)
        elif t == "q_end":
            from .quiz import CombatCard
            self.end_channel(f"p{self.game.state.me.get('id')}")
            if self.waiting_q is not None and self.waiting_q[0]["q"].get("session_id") == m.get("sid"):
                self.waiting_q = None
            for sc in list(self.game.scenes):
                if isinstance(sc, CombatCard) and sc.q.get("session_id") == m.get("sid") and not sc.result:
                    self.game.pop(sc)
        elif t == "dead":
            from .quiz import CombatCard
            from .rpg import DeathOverlay
            self.end_channel(f"p{self.game.state.me.get('id')}")
            self.waiting_q = None
            for sc in list(self.game.scenes):
                if isinstance(sc, CombatCard):
                    self.game.pop(sc)
            if m.get("ghost"):   # stage 9: in a bí cảnh you follow the party as a ghost
                self.ghost = True
                self.game.toast(T.REALM_GHOST, "#8C8C8C")
                return
            self.dead = True
            if self.my_die_t0 is None:
                self.my_die_t0 = self.game.now
            self.game.push(DeathOverlay(self.game, m.get("respawn_in", 3)))
        elif t == "realm":
            if self.realm is not None:
                self.realm.on_net(m)
        elif t == "loot":
            p = self.player
            y = p.y - 30
            if m.get("stones"):
                self.fx.float_text(T.LOOT_STONES.format(n=m["stones"]), p.x, y, "#E9C46A")
                y -= 9
            xp = (m.get("xp") or {}).get("gained")
            if xp:
                self.fx.float_text(T.LOOT_XP.format(n=xp), p.x, y, "#B5D67A")
        elif t == "act_fail":
            if m.get("code") == "too_far":
                self.fx.float_text(T.SKILL_FAIL["too_far"], self.player.x, self.player.y - 30, "#F4EBD9")
        elif t == "mcast":      # M9: the answer to a chiêu thức key
            if m.get("ok"):
                self.mskill_ready[m["k"]] = self.game.now + float(m.get("ready_in", 0))
                if m.get("qi") is not None:
                    self.game.state.character["qi"] = int(m["qi"])
            else:
                self.game.toast(m.get("message_vi") or T.SKILL_FAIL.get(m.get("code"), ""), "#BC4749")
        elif t in ("glide", "ride", "tran", "fly"):       # thần thông of Luyện Khí, ngự kiếm
            self.on_ability(t, m)

    def open_question(self, m: dict, waited: float = 0.0) -> None:
        """Put the card of a `q` message on the screen. `waited`: seconds the question was held
        back behind the previous card - the server's clock ran meanwhile, so the card gets less."""
        from .math_practice import MathCombatQuizScene
        while self.game.top is not None and self.game.top is not self and self in self.game.scenes:
            self.game.pop()      # the fight comes first: close bag/menus so the card sits over the world
        if m.get("first_meet"):
            self.game.toast(T.PARRY_INTRO if m.get("hit") else T.COMBAT_INTRO, "#4A7CC8")
        q = m["q"]
        if waited > 0:
            q = {**q, "time_limit": max(1.0, float(q.get("time_limit") or 10) - waited)}
        if m.get("hit"):     # the open-world rule: a blow landed and this question decides it
            from .rpg import ParryCard
            self.game.push(ParryCard(self.game, q, m.get("mid") or "", m["hit"], on_result=self.on_combat_result))
            return
        self.start_cooldown((m.get("cast") or {}).get("k"))
        # every monster, chiêu (M9) and bí cảnh (M10) asks a math question: the math card
        self.game.push(MathCombatQuizScene(self.game, q, m.get("mid") or "",
                                           on_result=self.on_combat_result, cast=m.get("cast")))

    def show_waiting_question(self) -> None:
        """A question can arrive while the card of the previous one still shows its result: a
        chiêu lands and the monster beside it asks at once. Such a question used to be thrown
        away, and the server - which had already opened it - kept the player in Hộ Thể for a
        card nobody could see, refused every chiêu with "answering" and ended it with a Mặc
        Kích. Now it waits: it opens the moment that card closes, and closes the card itself
        after WAITING_Q_MAX seconds."""
        if self.waiting_q is None:
            return
        from .quiz import CombatCard
        m, since = self.waiting_q
        waited = self.game.now - since
        cards = [sc for sc in self.game.scenes if isinstance(sc, CombatCard)]
        if cards and waited < WAITING_Q_MAX:
            return
        self.waiting_q = None
        if self.dead or any(not sc.result for sc in cards):
            return               # dead, or a card that is still being answered: never close that one
        for sc in cards:
            sc.finish()
        self.open_question(m, waited)

    def on_combat_result(self, res: dict) -> None:
        # effects arrive with the next snapshot; Tu Vi is shown by the quiz card
        if (res.get("combat") or {}).get("cast"):
            self.load_mskills()          # the answer may have opened a floor, so a chiêu

    def apply_zone(self, m: dict) -> None:
        p = self.player
        p.x, p.y = float(m["x"]), float(m["y"])
        p.facing = m.get("f", p.facing) if m.get("f") in FACING else p.facing
        self.pending.clear()
        self.batch = []
        self.seq = max(self.seq, int(m.get("ack", -1)) + 1)
        self.casting.clear()
        self.skill_fx.clear()
        if getattr(self, "vfx", None) is not None:
            self.vfx.clear()
            self.vfx_late.clear()
        self.entities.clear()
        self.interp.clear()
        self.channel = m.get("channel", 1)
        self.channels = m.get("channels", [])
        self.rule = m.get("combat")
        self.apply_abilities(m)
        self.zone_name = m.get("name_vi") or self.zone_name
        if m.get("land") != self.land_id or not self.weapon_spots:
            self.land_id = m.get("land")
            self.load_weapon_spots()
        self.joined = True
        self.waiting_zone = None
        ch = self.game.state.character
        ch.update({"zone_id": self.zone_id, "x": p.x, "y": p.y, "facing": p.facing})
        if m.get("day") is not None:
            self.game.set_day(m["day"])

    def load_weapon_spots(self) -> None:
        """The weapons lying in this land, from the weapon system (GET /weapons). A server
        without it answers 404 or nothing: then no spot is drawn and nothing else changes."""
        land = self.land_id
        if not land:
            self.weapon_spots = []
            return

        def ok(d):
            if self.land_id == land:
                self.weapon_spots = weapon_spots_from(d, land)
        try:
            self.game.api.get("/weapons", ok, lambda e: None)
        except Exception:
            self.weapon_spots = []

    def claim_weapon(self, spot: WeaponSpot) -> None:
        g = self.game
        if spot.state == "taken":
            g.toast(T.WEAPON_SPOT_TAKEN, "#BC4749")
            return
        if spot.state != "available":
            g.toast(spot.reason_vi or T.WEAPON_SPOT_LOCKED, "#BC4749")
            return

        def ok(r):
            r = r if isinstance(r, dict) else {}
            g.toast(r.get("message_vi") or T.WEAPON_SPOT_CLAIMED.format(name=spot.name_vi or T.WEAPON_SPOT),
                    "#6A994E")
            for name in ("refresh_inv", "refresh_me"):
                fn = getattr(g, name, None)
                if callable(fn):
                    fn()
            self.load_weapon_spots()

        def err(e):
            msg = getattr(e, "message_vi", "") if getattr(e, "status", 0) not in (404, 405) else ""
            if msg:
                g.toast(msg, "#BC4749")
        g.api.post("/weapons/claim", {"id": spot.id, "land": spot.land}, ok, err)

    def weapon_drawables(self, v, size: tuple[int, int] | None = None) -> list:
        """(foot y, image, screen position) of the weapon spots in the v2 world: the weapon's
        icon standing on its tile, bobbing; a locked one is dimmed, a taken one is gone. With the
        screen's `size`, the spots far off it are skipped (a giant land has many)."""
        out = []
        for sp in self.weapon_spots:
            if sp.state == "taken" or (size is not None and off_screen(v, sp.x, sp.y, size)):
                continue
            img = art2.icon(*sp.icon) if sp.icon else None
            if img is None:
                continue
            if sp.state != "available":
                img = art2.alpha_copy(img, 120)
            sx, sy = v.to_screen(sp.x, sp.y)
            bob = int(math.sin(self.t * 3 + sp.tx) * 2)
            out.append((sp.y, img, (int(sx - img.get_width() / 2), int(sy - img.get_height() - 2 + bob))))
        return out

    def apply_snapshot(self, m: dict) -> None:
        st = m["st"]
        now = self.game.now
        self.interp.clock_sample(st, now)
        ack = m.get("ack", -1)
        while self.pending and self.pending[0][0] <= ack:
            self.pending.popleft()
        x, y = float(m["me"][0]), float(m["me"][1])
        # ngự kiếm: the server's rung now, then my unconfirmed take-offs and landings replayed
        fly = int(m["me"][9]) if len(m["me"]) >= 11 else self.fly
        fly_speeds = {self.fly_speed(i) for i in (1, 2)}
        for entry in self.pending:
            if len(entry) > 3 and entry[3]:                  # a glide (or mounting): no steps of its own
                if entry[3][0] == "glide":
                    x, y = entry[3][1], entry[3][2]
                elif entry[3][0] == "fly":
                    fly = self.fly_level() if entry[3][1] else (0 if self.may_land(x, y, fly) else fly)
                continue
            speed = entry[2] if len(entry) > 2 else SPEED     # a Né Đòn dash has its own speed, a rider its mount's
            if fly:
                speed = self.fly_speed(fly)
            elif speed in fly_speeds:                         # sent in the air, but the server had us down
                speed = SPEED
            for dx, dy, ms in entry[1]:
                x, y = self.step_as(fly, x, y, dx, dy, ms, speed)
        for dx, dy, ms in self.batch:
            x, y = self.step_as(fly, x, y, dx, dy, ms, self.fly_speed(fly) if fly else self.move_speed())
        if fly != self.fly:                  # the server disagreed (a landing refused, knocked off the sword)
            self.set_fly(fly, x, y)
        if len(m["me"]) >= 11:
            self.fly_gauge = float(m["me"][10])
        p = self.player
        if abs(x - p.x) > 0.01 or abs(y - p.y) > 0.01:
            self.corrections += 1   # the server disagreed (blocked or too fast): follow it
            p.x, p.y = x, y
        me = m["me"]
        if len(me) >= 7:
            ch = self.game.state.character
            ch["hp"], ch["max_hp"], ch["qi"], ch["max_qi"] = int(round(me[3])), int(me[4]), int(round(me[5])), int(me[6])
            if me[3] > 0:
                self.dead = False
                self.my_die_t0 = None
        if len(me) >= 8:
            self.my_bees = me[7]
        if len(me) >= 9:
            self.ghost = bool(me[8])
        seen = set()
        for e in m.get("add", []):
            ent = Ent(e["id"], e["k"], e.get("n", ""), e.get("uid"), e.get("ap") or {}, e.get("type", ""),
                      e.get("realm", "pham_nhan"))
            ent.hp, ent.shield, ent.alive = e.get("hp", 100), e.get("sh", 0), e.get("alive", 1)
            ent.rank, ent.weapon = e.get("rank", "normal"), e.get("wp")
            ent.kv = int(e.get("kv") or 0)          # Đại Địa Đồ: the band of tu vi a monster stands in
            ent.bees = e.get("bees") or []
            ent.pet = e.get("pet")
            ent.ghost = bool(e.get("gh"))
            ent.beast, ent.need, ent.ride = bool(e.get("beast")), int(e.get("need") or 0), bool(e.get("rd"))
            ent.fly, ent.fsword = int(e.get("fl") or 0), e.get("fs") or ""
            if e["k"] == "p":
                self.sync_flyer(e["id"], ent.fly, now)
            ent.stage = int(e.get("stage") or 0)
            ent.lc = int(e.get("lc") or 0)
            if e["k"] == "r":
                ent.realm_id, ent.left, ent.seen = e.get("realm", ""), float(e.get("left", 0)), self.game.now
            self.entities[e["id"]] = ent
            self.interp.push(e["id"], st, e["x"], e["y"], e.get("f", 0), e.get("m", 0))
            seen.add(e["id"])
        for row in m.get("e", []):
            eid, ex, ey, f, mvng = row[:5]
            ent = self.entities.get(eid)
            if ent is not None:
                if len(row) >= 6:
                    ent.hp = row[5]
                if len(row) >= 8:
                    ent.shield, ent.alive = row[6], row[7]
                    if ent.alive and ent.die_t0 is not None and now - ent.die_t0 > 1.0:
                        ent.die_t0 = None          # respawned
                elif len(row) == 7 and ent.kind == "p":
                    ent.bees = row[6] or []
                self.interp.push(eid, st, ex, ey, f, mvng)
                seen.add(eid)
        # the swings, chiêu and parries before the hits they cause (their hits wait for the blade)
        for ev in sorted(m.get("fx", []), key=lambda e: 0 if e.get("k") in ("atk", "mskill", "parry") else 1):
            self.on_fx(ev)
        for eid in m.get("rm", []):
            self.entities.pop(eid, None)
            self.interp.forget(eid)
        for eid in self.entities:  # unchanged ones keep a sample so interpolation stays continuous
            if eid not in seen:
                last = self.interp.last(eid)
                if last:
                    self.interp.push(eid, st, last[1], last[2], last[3], 0)

    def on_fx(self, ev: dict) -> None:
        """Combat effects from the server (spec 18: sparks, shake, red flash, ink to light). A
        blow's hit (and the death it causes) waits, at most a fraction of a second, for the
        blade or the chiêu to reach the target on screen (presentation only: the server has
        already applied it)."""
        if self.vfx_defer(ev):
            return
        self.fx_event(ev)

    def vfx_defer(self, ev: dict) -> bool:
        hold = getattr(self, "vfx_hold", None)
        if not hold or ev.get("b"):
            return False
        now, k = self.game.now, ev.get("k")
        if k == "hit":
            until = hold.get(ev.get("by"))
            if until is None or until <= now:
                return False
            self.vfx_held[ev.get("id")] = until
        elif k in ("die", "shield"):
            until = self.vfx_held.get(ev.get("id"))
            if until is None or until <= now:
                return False
            until += 0.01
        else:
            return False
        self.vfx_late.append((min(until, now + 0.6), ev))
        return True

    def vfx_release(self) -> None:
        """The held events whose blow has now landed on screen."""
        if not self.vfx_late:
            return
        now = self.game.now
        due = [e for e in self.vfx_late if e[0] <= now]
        if due:
            self.vfx_late = [e for e in self.vfx_late if e[0] > now]
            for _, ev in due:
                self.fx_event(ev)

    def vfx_where(self, key):
        """Where a followed thing is now (the VFX layer's resolver): a player or a monster."""
        if key == f"p{self.game.state.me.get('id')}":
            return self.player.x, self.player.y
        e = self.entities.get(key) if isinstance(key, str) else None
        return (e.pos[0], e.pos[1]) if e is not None else None

    def vfx_tier(self, eid: str | None) -> int:
        """The kiếm khí tier of a player (me: my realm and stage; others: what the server sent)."""
        if eid == f"p{self.game.state.me.get('id')}":
            ch = self.game.state.character or {}
            return CV.tier(ch.get("realm"), ch.get("realm_stage"))
        e = self.entities.get(eid or "")
        return CV.tier(e.realm, e.stage) if e is not None else 1

    def garnish(self, x: float, y: float, el: str, n: int, speed: float) -> None:
        """Code sparks over the sheets (a few pixels of debris; the look itself is the sheets)."""
        if not getattr(self, "vfx", None) or self.vfx.reduced:
            return
        self.fx.burst(x, y, "#%02X%02X%02X" % CV.RGB.get(el, (255, 255, 255)), n, speed)

    def fx_event(self, ev: dict) -> None:
        k = ev.get("k")
        x, y = ev.get("x", 0.0), ev.get("y", 0.0)
        me = f"p{self.game.state.me.get('id')}"
        if k in ("mark", "pz", "gshield"):    # stage 9: pings and puzzle effects
            if self.realm is not None:
                self.realm.on_fx(ev)
            return
        if k in ("mcast", "mskill"):                    # M9: a chiêu thức is channelled / lands
            self.on_mskill_fx(k, ev)
            return
        if k == "hit" and getattr(self, "bells", {}).get(ev.get("id"), 0.0) > self.game.now:   # the golden bell
            vf = getattr(self, "vfx", None)
            pos = self.vfx_where(ev.get("id")) if vf is not None else None
            if pos is not None:
                CV.bell_block(vf, pos[0], pos[1], follow=ev.get("id"))
        if k == "hit" and ev.get("b"):                  # a guard bee stung a monster (spec 10.2.3)
            self.bee_hits += 1
            for fb in self.flock.bees.values():         # that bee plays its sting clip
                if fb.sp == ev.get("b") and getattr(fb, "target", None) == ev.get("id"):
                    fb.sting_t0 = self.game.now
                    break
            ent = self.entities.get(ev.get("id"))
            if ent is not None:
                ent.hurt_t = 0.08
            self.fx.float_text(str(ev.get("v", "")), x + random.uniform(-6, 6), y - 18, "#F2D58A")
            return
        if k == "ink":                                   # Ong Thư Pháp: a brush stroke
            self.fx.burst(x, y - 8, "K", 12, 30)
            return
        if k == "bee_down":
            if ev.get("id") == me:
                name = (self.game.state.bee_species.get(ev.get("s")) or {}).get("name_vi", "Ong")
                self.game.toast(T.BEE_DOWN.format(name=name), "#BC4749")
            self.fx.burst(x, y - 12, "o", 6, 20)
            return
        if k == "stun":
            self.fx.float_text(T.BEE_STUN, x, y - 30, "#B5A0E0")
            return
        if k in ("parry", "dodge", "dodged", "struck"):   # the open-world rule
            self.on_rule_fx(k, ev, me)
            return
        if k in ("tame", "seal", "fire", "glide", "tran", "ride", "fly", "soar"):   # linh thú and thần thông
            self.on_beast_fx(k, ev, me)
            return
        v2 = art2.on()
        now = self.game.now
        z = self.z                       # screen pixels per world pixel: a lift in screen px / z = world px
        if k == "gb" and v2:             # a wrong answer: the blow breaks through the guard
            ent = self.entities.get(ev.get("id"))
            top = (V2_HEAD - 6) / z if ev.get("id") == me else (self.ent_extent(ent)[1] / z if ent else 20)
            self.spark(art2.combat_fx("guard_break"), x, y - top * 0.6)
        if k in ("hit", "mk", "gb") and ev.get("id") == me:   # we were hit
            self.fx.shake = 0.6 if k == "mk" else 0.3
            self.hurt_flash = 0.45 if k == "mk" else 0.2
            self.fx.float_text(f"-{ev.get('v', '')}", x, y - ((V2_HEAD - 6) / z if v2 else 30), "#F08A8C")
            if k == "mk":
                self.fx.float_text(T.MAC_KICH, x, y - ((V2_HEAD + 4) / z if v2 else 40), "#BC4749")
            elif k == "gb":
                self.fx.float_text(T.GUARD_BREAK, x, y - ((V2_HEAD + 4) / z if v2 else 40), "#BC4749")
            if v2:
                self.my_hurt_t0 = now
                self.spark(art2.combat_fx("hit"), x, y - 26 / z)
        elif k in ("hit", "mk", "gb"):
            ent = self.entities.get(ev.get("id"))
            crit = bool(ev.get("c")) and not ev.get("sh")
            if ent is not None:
                ent.hurt_t = 0.22 if crit else 0.15
            col = "#9A9A9A" if ev.get("sh") else ("#E9C46A" if ev.get("c") else "#FFFFFF")
            if k in ("mk", "gb") or (ent is not None and ent.kind == "p"):
                col = "#F08A8C"
            lift = self.ent_extent(ent)[1] / z if (v2 and ent is not None) else 22
            self.fx.float_text(str(ev.get("v", "")), x + random.uniform(-4, 4), y - lift, col,
                               style="crit" if crit else ("dim" if ev.get("sh") else "hit"))
            vf = getattr(self, "vfx", None)
            if v2 and vf is not None and ent is not None:
                by = ev.get("by")
                ent.hit_by = by
                src = self.vfx_where(by) if by else None
                if src is not None:
                    ent.kick = CV.recoil((x, y), src, now, 3.5 if crit else 2.0)
                if crit:
                    CV.crit(vf, x, y, lift * 0.5, mine=by == me)
                elif by not in self.vfx_hold:   # a swing drawn by the VFX layer brought its own impact
                    self.spark(art2.combat_fx("hit"), x, y - lift * 0.5)
            elif v2:
                self.spark(art2.combat_fx("crit" if ev.get("c") else "hit"), x, y - lift * 0.5)
        elif k == "tele":
            # [x, y, r, time left, total, monster, shape]; shape = {"sh", "a" (degrees), "deg", "w"}
            self.teles.append([x, y, ev.get("r", 20), ev.get("d", 0.8), ev.get("d", 0.8), ev.get("id"),
                               {"sh": ev.get("sh", "circle"), "a": float(ev.get("a") or 0.0),
                                "deg": float(ev.get("deg") or 90.0), "w": float(ev.get("w") or 12.0)}])
            ent = self.entities.get(ev.get("id"))
            if ent is not None:
                ent.aim = (x, y)
        elif k == "shield":
            if ev.get("on"):
                if not v2:
                    self.fx.burst(x, y - 8, "K", 16, 25)
                self.fx.float_text(T.SHIELD_BACK, x, y - 34, "#5A5A5A")
            else:  # "mực tan thành hạt sáng khi phá khiên"
                if v2:   # over the head, a beat after the blow, so it does not pile onto the hit spark
                    ent = self.entities.get(ev.get("id"))
                    top = self.ent_extent(ent)[1] / z if ent is not None else 14
                    self.spark(art2.combat_fx("shield_broken"), x, y - top, delay=0.18, scale=0.75)
                else:
                    self.fx.ink_to_light(x, y - 8)
                self.fx.float_text(T.SHIELD_BROKEN, x, y - 34, "#E9C46A")
        elif k == "die":
            ent = self.entities.get(ev.get("id"))
            if v2 and ev.get("id") == me:
                if self.my_die_t0 is None:
                    self.my_die_t0 = now
            elif v2 and ent is not None:
                ent.die_t0 = now                    # the die clip plays once, then it is gone
                self.vfx_death(ent, x, y, me)
            else:
                self.fx.burst(x, y - 8, "K", 22, 40)
                self.fx.burst(x, y - 8, "W", 10, 30)
        elif k == "atk":
            ent = self.entities.get(ev.get("by"))
            if ent is not None:
                ent.swing_t = 0.25
                ent.atk_t0 = now
                self.play_swing(ent.id, ev.get("wp") or ent.weapon, ent.realm,
                                (ent.pos[0], ent.pos[1]) if any(ent.pos[:2]) else (x, y), ev.get("id"))
        elif k == "heal":
            self.fx.float_text(f"+{ev.get('v', '')}", x, y - 30, "#4A7CC8" if ev.get("q") else "#B5D67A")
            if v2 and art2.fx(art2.combat_fx("heal")) is not None:
                self.spark(art2.combat_fx("heal"), x, y - 24 / z, once=True)
            else:
                self.fx.burst(x, y - 10, "l", 8, 15)

    def on_rule_fx(self, k: str, ev: dict, me: str) -> None:
        """Effects of the open-world rule: `struck` (a blow landed: the card is on its way),
        `parry` (a right answer: the monster takes the counter and is stunned), `dodge` (a Né Đòn
        dash starts) and `dodged` (its moment of invulnerability beat a blow)."""
        x, y = float(ev.get("x", 0.0)), float(ev.get("y", 0.0))
        now, z, v2 = self.game.now, self.z, art2.on()
        if k == "struck":
            if ev.get("id") == me:
                self.fx.shake = 0.35
                self.hurt_flash = 0.25
                self.flush_inputs()
                self.player.moving = False
            return
        vf = getattr(self, "vfx", None) if v2 else None
        if k == "parry":
            self.stunned[ev.get("id")] = now + float(ev.get("st") or 0.0)
            ent = self.entities.get(ev.get("id"))
            px, py = float(ev.get("px", x)), float(ev.get("py", y))
            if ent is not None:
                ent.hurt_t = 0.25
                ent.kick = CV.recoil((x, y), (px, py), now, 6.0)
            by = ev.get("by")
            self.parried[ev.get("id")] = (by, now)
            if vf is not None:
                weapon = (self.game.state.cult or {}).get("stats", {}).get("weapon") if by == me else \
                    getattr(self.entities.get(by or ""), "weapon", None)
                m_lift = self.ent_extent(ent)[1] / z * 0.5 if ent is not None else 12.0
                land = CV.parry(vf, x, y, px, py, self.vfx_tier(by), weapon, mine=by == me, m_lift=m_lift,
                                garnish=self.garnish)
                self.vfx_hold[by] = now + land
            elif v2 and art2.fx(art2.combat_fx("parry")) is not None:
                self.spark(art2.combat_fx("parry"), (x + px) / 2, (y + py) / 2 - 18 / z)
            else:
                self.fx.burst((x + px) / 2, (y + py) / 2 - 12, "W", 14, 30)
            self.fx.float_text(T.PARRY, px, py - ((V2_HEAD + 4) / z if v2 else 40), "#E9C46A", style="parry")
            return
        if k == "dodge":
            eid = ev.get("id")
            self.dodging[eid] = now
            if vf is not None:
                CV.dodge(vf, x, y, float(ev.get("dx") or 0), float(ev.get("dy") or 0))
                vf.emit(("ghost", eid), 0.045, lambda: self.afterimage(eid), 0.2)
                return
            fid = art2.combat_fx("dodge_trail") if v2 else None
            if fid and art2.fx(fid) is not None:
                self.spark(fid, x, y - 12 / z)
            return
        if k == "dodged":
            if vf is not None:
                CV.dodged(vf, x, y, mine=ev.get("id") == me)
            self.fx.float_text(T.DODGE_OK, x, y - ((V2_HEAD - 6) / z if v2 else 30), "#B5D67A", style="dodge")

    def dodge_open(self) -> bool:
        """Is Né Đòn open for me? The server's word at the last zone message, or - after a
        breakthrough since - the realm and stage it named, read against my own."""
        d = (self.rule or {}).get("dodge") or {}
        if d.get("ok"):
            return True
        need = d.get("unlock") or {}
        order = list(T.REALMS)
        ch = self.game.state.character or {}
        mine, want = ch.get("realm", "pham_nhan"), need.get("realm")
        if want not in order or mine not in order:
            return False
        a, b = order.index(mine), order.index(want)
        return a > b or (a == b and int(ch.get("realm_stage") or 0) >= int(need.get("stage", 0)))

    def dodge(self) -> None:
        """Né Đòn (Shift): a dash the way the keys point (or the way we face). It rides in the
        movement stream under its own sequence number, so the server repeats exactly the steps
        predicted here; the numbers come from the server with the zone."""
        d = (self.rule or {}).get("dodge")
        if d is None or self.net is None or self.dead or self.ghost or not self.joined or self.grounded_only():
            return
        if not self.dodge_open():
            self.fx.float_text(T.DODGE_LOCKED, self.player.x, self.player.y - 30, "#F4EBD9")
            return
        if self.game.now < self.dodge_ready:
            return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if not (dx or dy):
            dx, dy = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}[self.player.facing]
        self.flush_inputs()
        total, step_ms = int(round(float(d["dash_ms"]))), int(d.get("step_ms") or 10)
        speed = float(d["dash_px"]) / (total / 1000.0)
        steps, left = [], total
        while left > 0:
            part = min(step_ms, left)
            steps.append([dx, dy, part])
            left -= part
        if not self.net.send({"t": "dodge", "s": self.seq, "dx": dx, "dy": dy}):
            return
        self.pending.append((self.seq, steps, speed))
        self.seq += 1
        p = self.player
        for sdx, sdy, ms in steps:
            p.x, p.y = mv.step(p.x, p.y, sdx, sdy, ms, speed, self.col)
        self.dodge_ready = self.game.now + float(d["cooldown"])
        self.dodging[f"p{self.game.state.me.get('id')}"] = self.game.now

    # ------------------------------------------------------------ linh thú and thần thông (Thiên Địa Đồ)
    def apply_abilities(self, m: dict) -> None:
        """The thần thông sent with the zone (server realtime/abilities.py), the formations already
        laid here, and whether the server still has us on our mount."""
        self.abilities = m.get("abilities")
        now = self.game.now
        self.formations = [[float(f["x"]), float(f["y"]), float(f["r"]), now + float(f.get("left", 0)),
                            ((self.abilities or {}).get("phap_tran") or {}).get("fx", "")]
                           for f in (m.get("formations") or [])]
        ride = (self.abilities or {}).get("cuoi_linh_thu") or {}
        self.riding = bool(ride.get("riding"))
        self.ride_mult = float(ride.get("mult") or 1.0) if self.riding else 1.0
        self.flight = ((self.abilities or {}).get("dap_kiem_luot") or {}).get("flight")
        fv = self.flight or {}
        self.fly = int(fv.get("flying") or 0)          # (a new zone puts us on the ground)
        self.fly_gauge = float(fv.get("gauge_now") or 0.0)
        self.flyers.clear()
        self.g_down = None
        self.taming.clear()
        self.glides.clear()
        self.sniffed, self.sniff_t = None, 0.0

    def move_speed(self) -> float:
        """My walking speed: the sword's in the air, the mount's when I ride (the server moves me
        at the same speed)."""
        if self.fly:
            return self.fly_speed(self.fly)
        return SPEED * self.ride_mult if self.riding else SPEED

    # ------------------------------------------------------------ ngự kiếm (G held)
    def fly_rung(self, level: int) -> dict:
        levels = (self.flight or {}).get("levels") or []
        return levels[level] if 0 < level < len(levels) and isinstance(levels[level], dict) else {}

    def fly_level(self) -> int:
        """The rung open to me: 2 free flight (Trúc Cơ), 1 low flight, 0 none."""
        return int((self.flight or {}).get("level") or 0)

    def fly_speed(self, level: int) -> float:
        return SPEED * float(self.fly_rung(level).get("speed_mult") or 1.0)

    def fly_lift(self, level: int) -> float:
        """World px a flyer of this rung cruises above its ground point."""
        return float(self.fly_rung(level).get("lift") or (30.0 if level >= 2 else 18.0))

    def fly_rise(self, level: int) -> float:
        return float(self.fly_rung(level).get("rise") or 0.3)

    def fly_over(self, level: int | None = None) -> set:
        return set(self.fly_rung(level or self.fly or 1).get("over") or ())

    def may_land(self, x: float, y: float, level: int | None = None) -> bool:
        """The server's own landing rule (engine/glide.py, a copy of the server's)."""
        return gl.land_ok(self.col, self.tile_at, self.fly_over(level), x, y)

    def step_as(self, fly: int, x: float, y: float, dx: int, dy: int, ms: int, speed: float):
        """One step as the server takes it: flown over water and chasms, or walked."""
        if fly:
            return gl.fly_step(self.col, self.tile_at, self.fly_over(fly), x, y, dx, dy, ms, speed)
        return mv.step(x, y, dx, dy, ms, speed, self.col)

    def flyer(self, eid: str) -> fl.Flyer:
        f = self.flyers.get(eid)
        if f is None:
            f = self.flyers[eid] = fl.Flyer()
        return f

    def sync_flyer(self, eid: str, level: int, now: float) -> None:
        """A player record arrived: one first seen in the air is drawn up there at once; one that
        came down without an event in reach eases down."""
        f = self.flyers.get(eid)
        if level and (f is None or not f.flying):
            if f is None or f.kind is None:
                self.flyer(eid).hover(now, level, self.fly_lift(level))
        elif not level and f is not None and f.flying and f.kind == "cruise" and now - f.t0 > 0.6:
            f.land(now)

    def my_eid(self) -> str:
        return f"p{self.game.state.me.get('id')}"

    def set_fly(self, level: int, x: float | None = None, y: float | None = None, fall_from=None) -> None:
        """My rung changed (predicted, or said by the server): the altitude follows."""
        now = self.game.now
        f = self.flyer(self.my_eid())
        if level:
            f.take_off(now, level, self.fly_lift(level), self.fly_rise(level))
        elif fall_from is not None and x is not None:
            self.glides[self.my_eid()] = (now, fall_from[0], fall_from[1], x, y, fl.FALL_S)
            f.land(now, fall=True)
        else:
            f.land(now)
        self.fly = level

    def fly_takeoff_fx(self, x: float, y: float, mine: bool = True) -> None:
        """The ring and the dust where a flyer leaves the ground."""
        vf = self.vfx
        vf.spawn("phi_cat_canh", x, y, layer="ground", scale=0.8)
        for side in (-1, 1):
            vf.spawn("dust_step", x + side * 6, y + 1, layer="ground", scale=0.7, flip=side < 0, heavy=True)
        if mine:
            self.game.audio.play("whoosh")

    def fly_landing_fx(self, x: float, y: float, mine: bool) -> None:
        """Touch-down: the landing ring, a puff of dust, and (mine) the camera settles."""
        vf = self.vfx
        vf.spawn("phi_ha_canh", x, y, layer="ground", scale=0.8)
        vf.spawn("dust_step", x, y + 1, layer="ground", scale=0.9, heavy=True)
        if mine:
            self.cam_dip = 3.0
            self.game.audio.play("land")

    def g_pressed(self) -> None:
        """G: in the air it brings me down; on the ground a tap hops over the gap (Đạp Kiếm Lướt)
        and holding it takes off (update() tells the two apart)."""
        if self.fly:
            self.land()
            return
        if self.fly_level() == 0:
            self.glide()            # (says why it is locked)
            return
        self.g_down = self.game.now

    def watch_g(self, top: bool) -> None:
        """G held long enough takes off; let go sooner, it was a tap: the hop."""
        if self.g_down is None:
            return
        if not top:                 # a card came up meanwhile: neither
            self.g_down = None
            return
        held = pygame.key.get_pressed()[pygame.K_g]
        if held and self.game.now - self.g_down >= fl.HOLD_S:
            self.g_down = None
            self.take_off()
        elif not held:
            self.g_down = None
            self.glide()

    def take_off(self) -> None:
        """Ngự kiếm: up on the sword. Predicted here, decided by the server in the movement stream."""
        level = self.fly_level()
        fv = self.flight or {}
        if level == 0 or self.net is None or self.dead or self.ghost or not self.joined or self.fly:
            return
        p = self.player
        why = None
        if self.riding:
            why = T.FLY_RIDING
        elif level == 1 and self.fly_gauge < float(fv.get("min_gauge") or 0):
            why = T.FLY_GAUGE_LOW
        if why:
            self.fx.float_text(why, p.x, p.y - 30, "#F4EBD9")
            return
        self.flush_inputs()
        if not self.net.send({"t": "fly", "s": self.seq, "on": True}):
            return
        self.pending.append((self.seq, [], SPEED, ("fly", True)))
        self.seq += 1
        self.set_fly(level)
        self.fly_takeoff_fx(p.x, p.y)

    def land(self) -> None:
        """Come down where I hover - only over walkable ground (the server's rule)."""
        if not self.fly or self.net is None:
            return
        p = self.player
        if not self.may_land(p.x, p.y):
            self.fx.float_text(T.FLY_NO_LANDING, p.x, p.y - 30 - self.fly_lift(self.fly), "#F4EBD9")
            return
        self.flush_inputs()
        if not self.net.send({"t": "fly", "s": self.seq, "on": False}):
            return
        self.pending.append((self.seq, [], SPEED, ("fly", False)))
        self.seq += 1
        self.set_fly(0)

    def grounded_only(self) -> bool:
        """In the air: say so and refuse (attacks, chiêu, Né Đòn, talking, picking up, fishing)."""
        if self.fly:
            p = self.player
            self.fx.float_text(T.FLY_LAND_FIRST, p.x, p.y - 30 - self.fly_lift(self.fly), "#F4EBD9")
            return True
        return False

    def update_flight(self, dt: float) -> None:
        """The gauge as predicted (the snapshots correct it), touch-downs, spray over water and
        the spirit motes behind a moving sword."""
        fv = self.flight
        if fv:
            top = float(fv.get("gauge_max") or 0)
            if self.fly == 1:
                self.fly_gauge = max(0.0, self.fly_gauge - dt)
            elif not self.fly and top > 0:
                self.fly_gauge = min(top, self.fly_gauge + dt * top / max(0.1, float(fv.get("refill") or 1)))
        now = self.game.now
        me = self.my_eid()
        for eid, f in list(self.flyers.items()):
            if eid == me:
                x, y = self.glide_pos(me, self.player.x, self.player.y)[:2]
            else:
                ent = self.entities.get(eid)
                if ent is None:
                    if not f.shown(now):
                        del self.flyers[eid]
                    continue
                x, y = self.glide_pos(eid, ent.pos[0], ent.pos[1])[:2]
            f.track(x, y, now)
            if f.touched_down(now):
                self.fly_landing_fx(x, y, eid == me)
                continue
            if not f.flying or f.speed < fl.WAKE_MIN:
                continue
            last = self.fly_fx_t.get(eid, 0.0)
            if now - last < 0.16:
                continue
            self.fly_fx_t[eid] = now
            ux, uy = f.vx / f.speed, f.vy / f.speed
            if self.tile_at(int(x // 16), int((y - 1) // 16)) == "water":     # spray on the water below
                self.vfx.spawn("burst_thuy", x - ux * 4, y, layer="ground", hold=5, life=0.3, scale=0.42,
                               fade_out=0.25, peak=0.7, heavy=True)
            a = self.flyer(eid).alt(now)                                      # spirit motes off the tail
            self.vfx.spawn("hit_spark", x - ux * 10, y + 1, lift=a + 2, to=(x - ux * 22, y - uy * 8),
                           lift1=a + 6, hold=0, life=0.35, scale=0.28, fade_out=0.3, peak=0.8, heavy=True,
                           layer="over")
        self.cam_dip = max(0.0, self.cam_dip - dt * 14.0)
        # the camera leads a little the way I fly (eased in and out, never a jump)
        f = self.flyers.get(me)
        tx = ty = 0.0
        if f is not None and f.flying and self.fly:
            tx, ty = f.vx * 0.18, f.vy * 0.18
            d = math.hypot(tx, ty)
            if d > 16.0:
                tx, ty = tx * 16.0 / d, ty * 16.0 / d
        a = min(1.0, dt * 3.0)
        self.cam_lead[0] += (tx - self.cam_lead[0]) * a
        self.cam_lead[1] += (ty - self.cam_lead[1]) * a

    def tile_at(self, tx: int, ty: int) -> str | None:
        """The ground of a tile ('water', 'ink'...), as the server's maps.tile_name names it."""
        m = self.map
        if not (0 <= tx < m.w and 0 <= ty < m.h) or not m.ground:
            return None
        gid = m.ground[ty * m.w + tx]
        return B.TILESET[gid - 1][0] if 0 < gid <= len(B.TILESET) else None

    def ability(self, uid: str) -> dict | None:
        return (self.abilities or {}).get(uid)

    def _ability_locked(self, uid: str) -> None:
        a = self.ability(uid) or {}
        self.fx.float_text(T.ABILITY_LOCKED.format(name=a.get("name_vi", ""), stage=(a.get("unlock") or {}).get("stage", "")),
                           self.player.x, self.player.y - 30, "#F4EBD9")

    def _keys_dir(self) -> tuple[int, int]:
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if not (dx or dy):
            dx, dy = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}[self.player.facing]
        return dx, dy

    def glide(self) -> None:
        """Đạp Kiếm Lướt (G): the landing is picked here with the server's own geometry
        (engine/glide.py, a copy of the server's); the glide rides in the movement stream and the
        server checks it again from where it really has us."""
        a = self.ability("dap_kiem_luot")
        if a is None or self.net is None or self.dead or self.ghost or not self.joined:
            return
        if not a.get("ok"):
            self._ability_locked("dap_kiem_luot")
            return
        now = self.game.now
        if now < self.glide_ready:
            return
        dx, dy = self._keys_dir()
        p = self.player
        to = gl.pick(self.col, self.tile_at, set(a.get("over") or []), p.x, p.y, dx, dy,
                     float(a.get("max_px", 80)), float(a.get("min_px", 0)))
        if to is None:
            self.fx.float_text(T.GLIDE_NO_LANDING, p.x, p.y - 30, "#F4EBD9")
            if self.fly_level():
                self.fx.float_text(T.GLIDE_HOLD_HINT, p.x, p.y - 40, "#9FE8F0")
            return
        self.flush_inputs()
        if not self.net.send({"t": "glide", "s": self.seq, "x": to[0], "y": to[1]}):
            return
        self.pending.append((self.seq, [], SPEED, ("glide", to[0], to[1])))
        self.seq += 1
        me = f"p{self.game.state.me.get('id')}"
        self.glides[me] = (now, p.x, p.y, to[0], to[1], float(a.get("ms", 450)) / 1000)
        self.hop_fx(p.x, p.y, to[0], to[1], float(a.get("ms", 450)) / 1000, True)
        p.facing = face_to(to[0] - p.x, to[1] - p.y, p.facing)
        p.x, p.y = to
        self.glide_ready = now + float(a.get("cooldown", 2.5))

    def hop_fx(self, x0: float, y0: float, x1: float, y1: float, secs: float, mine: bool) -> None:
        """The hop is a real leap: the ring as the sword leaves the ground, dust where it lands."""
        self.fly_takeoff_fx(x0, y0, mine)
        self.vfx.at(secs, lambda: self.fly_landing_fx(x1, y1, mine))

    def toggle_ride(self) -> None:
        """Cưỡi linh thú (R): mount the worn beast or get down; it rides in the movement stream so
        the speed changes at the same step here and on the server."""
        a = self.ability("cuoi_linh_thu")
        if a is None or self.net is None or self.dead or self.ghost or not self.joined:
            return
        on = not self.riding
        if on and not a.get("ok"):
            self._ability_locked("cuoi_linh_thu")
            return
        if on and self.grounded_only():
            return
        mult = float(a.get("mult") or 0)
        if on and (mult <= 0 or not self.game.worn_pet()):
            self.game.toast(T.RIDE_NO_MOUNT, "#BC4749")
            return
        self.flush_inputs()
        if not self.net.send({"t": "ride", "s": self.seq, "on": on}):
            return
        self.pending.append((self.seq, [], SPEED, ("ride", on)))
        self.seq += 1
        self.riding, self.ride_mult = on, (mult if on else 1.0)

    def place_formation(self) -> None:
        """Bày pháp trận (T): the server lays it at our feet and answers."""
        a = self.ability("phap_tran")
        if a is None or self.net is None or self.dead or self.ghost or not self.joined:
            return
        if not a.get("ok"):
            self._ability_locked("phap_tran")
            return
        if self.grounded_only():
            return
        if self.game.now < self.tran_ready:
            return
        self.flush_inputs()
        self.net.send({"t": "tran"})
        self.tran_ready = self.game.now + 0.5        # until the server's answer says how long

    def on_ability(self, t: str, m: dict) -> None:
        """The server's answer to a thần thông."""
        if t == "fly":
            self.on_fly(m)
            return
        if not m.get("ok"):
            if t == "ride":
                self.riding, self.ride_mult = False, 1.0
            if t == "glide":
                self.glides.pop(f"p{self.game.state.me.get('id')}", None)
            if t == "tran":
                self.tran_ready = 0.0
            self.game.toast(m.get("message_vi") or "", "#BC4749")
            return
        if t == "ride":
            self.riding = bool(m.get("on"))
            self.ride_mult = float(m.get("mult") or 1.0) if self.riding else 1.0
        elif t == "tran":
            self.tran_ready = self.game.now + float(m.get("ready_in") or 0)

    def on_fly(self, m: dict) -> None:
        """The server on my flight: a refusal (said as a short float text; the next snapshot puts
        my rung right), a confirmation, or a landing it decided - the gauge ran dry (a fall back to
        the ground when that was over water), knocked off while rising, or gone."""
        p = self.player
        if not m.get("ok"):
            msg = m.get("message_vi") or ""
            if msg:
                self.fx.float_text(msg, p.x, p.y - 30 - (self.fly_lift(self.fly) if self.fly else 0), "#F4EBD9")
            # the take-off (or the landing) I predicted did not happen: it is no change in the replay
            for i in range(len(self.pending) - 1, -1, -1):
                e = self.pending[i]
                if len(e) > 3 and e[3] and e[3][0] == "fly":
                    self.pending[i] = (e[0], [], SPEED, None)
                    break
            on = int(m.get("on") or 0)
            if on != self.fly:
                self.set_fly(on)
            return
        why = m.get("why")
        if "gauge" in m:
            self.fly_gauge = float(m["gauge"])
        if why in ("gauge", "fall", "knocked", "gone") and self.fly:
            x, y = float(m.get("x", p.x)), float(m.get("y", p.y))
            if why == "fall":
                self.set_fly(0, x, y, fall_from=(p.x, p.y))
                p.x, p.y = x, y
                self.fx.float_text(T.FLY_FALL, x, y - 30, "#F4A261")
            else:
                self.set_fly(0)
                if why == "knocked":
                    self.fx.float_text(T.FLY_KNOCKED, p.x, p.y - 30, "#F4A261")
                elif why == "gauge":
                    self.fx.float_text(T.FLY_FALL, p.x, p.y - 30, "#F4A261")

    def on_beast_fx(self, k: str, ev: dict, me: str) -> None:
        """Effects of the linh thú and the thần thông: `tame` (a Phản Đòn counted against a beast),
        `seal` (a Phong Ấn Phù took it), `fire` (Hỏa Tước's counter), `glide`, `tran`, `ride`."""
        x, y = float(ev.get("x", 0.0)), float(ev.get("y", 0.0))
        now, z = self.game.now, self.z
        if k == "tame":
            if ev.get("by") != me:
                return
            ent = self.entities.get(ev.get("id"))
            name = ent.name if ent is not None else ""
            done = bool(ev.get("ok"))
            self.taming[ev.get("id")] = {"n": int(ev.get("n", 0)), "need": int(ev.get("need", 0)), "yielded": done,
                                         "name": name}
            self.fx.float_text(T.BEAST_TAME_COUNT.format(n=ev.get("n"), need=ev.get("need")), x, y - 40 / z, "#B5D67A")
            if done:
                self.game.toast(T.BEAST_YIELDED_TOAST.format(name=name), "#6A994E", 4.0)
                if ent is not None:
                    ent.aim = None
        elif k == "seal":
            self.spark("capture_seal", x, y - 14 / z, once=True)
            if ev.get("by") == me:
                self.taming.pop(ev.get("id"), None)
        elif k == "fire":
            self.spark("burst_hoa", x, y - 12 / z, once=True)
            self.fx.float_text(T.PARRY_FIRE, x, y - 34 / z, "#E76F51")
        elif k == "glide":
            if ev.get("id") != me:
                secs = float(ev.get("ms") or 450) / 1000
                self.glides[ev.get("id")] = (now, float(ev.get("x0", x)), float(ev.get("y0", y)), x, y, secs)
                ent = self.entities.get(ev.get("id"))
                if ent is not None and ev.get("sw"):
                    ent.fsword = ev["sw"]
                self.hop_fx(float(ev.get("x0", x)), float(ev.get("y0", y)), x, y, secs, False)
        elif k == "tran":
            fx = ((self.abilities or {}).get("phap_tran") or {}).get("fx") or ev.get("fx") or ""
            self.formations.append([x, y, float(ev.get("r") or 40), now + float(ev.get("d") or 10), fx])
        elif k == "ride":
            ent = self.entities.get(ev.get("id"))
            if ent is not None:
                ent.ride = bool(ev.get("on"))
        elif k == "fly":                     # ngự kiếm: someone took off or came down (mine: on_ability)
            eid = ev.get("id")
            if eid == me:
                return
            ent = self.entities.get(eid)
            on = int(ev.get("on") or 0)
            if ent is not None:
                ent.fly, ent.fsword = on, ev.get("sw") or ent.fsword
            f = self.flyer(eid)
            if on:
                f.take_off(now, on, self.fly_lift(on), self.fly_rise(on))
                self.fly_takeoff_fx(x, y, False)
            elif ev.get("why") == "fall" and "x0" in ev:
                self.glides[eid] = (now, float(ev["x0"]), float(ev["y0"]), x, y, fl.FALL_S)
                f.land(now, fall=True)
            else:
                f.land(now)
        elif k == "soar":                    # a blow on the ground passed under a flyer
            f = self.flyers.get(ev.get("id"))
            self.fx.float_text(T.FLY_SOAR, x, y - 30 - (f.lift if f is not None else 0), "#9FE8F0")

    def yielded_beast(self, e: "Ent | None") -> bool:
        """A beast that yielded to me: E seals it, it is no longer a foe."""
        return e is not None and e.beast and bool((self.taming.get(e.id) or {}).get("yielded"))

    def seal_beast(self, ent: Ent) -> None:
        """Phong Ấn Phù on a beast that yielded (POST /beasts/seal); the server checks it all."""
        g = self.game

        def ok(r):
            r = r if isinstance(r, dict) else {}
            g.toast(r.get("message_vi") or "", "#6A994E", 4.0)
            self.taming.pop(ent.id, None)
            g.audio.play("coin")
            g.refresh_pets()
            g.refresh_inv()

        g.api.post("/beasts/seal", {"id": ent.id}, ok, g.api_error)

    def beast_label(self, e: Ent) -> str:
        """The name over a beast: what it is, and how far my taming of it has come."""
        tm = self.taming.get(e.id)
        if tm and tm.get("yielded"):
            return f"{e.name} · {T.BEAST_YIELDED}"
        if tm:
            return f"{e.name} · {T.BEAST_TAME_COUNT.format(n=tm['n'], need=tm['need'])}"
        return f"{e.name} · {T.BEAST_RANK}"

    def update_beasts(self, dt: float) -> None:
        """Glides and formations that are over go; the Linh Hồ sniffs now and then."""
        now = self.game.now
        self.glides = {k: v for k, v in self.glides.items() if now - v[0] <= v[5]}
        self.formations = [f for f in self.formations if f[3] > now]
        pet = self.game.worn_pet()
        if not self.joined or self.abilities is None or not pet or pet == self.no_nose:
            if not pet or pet == self.no_nose or self.abilities is None:
                self.sniffed = None
            return
        self.sniff_t -= dt
        if self.sniff_t > 0:
            return
        self.sniff_t = 4.0

        def ok(d):
            self.sniffed = (d or {}).get("found") or []

        def err(e):
            if getattr(e, "code", "") == "no_nose" or getattr(e, "status", 0) in (404, 405):
                self.no_nose = pet            # this companion has no nose (or the server has no sniffing)
            self.sniffed = None
        try:
            self.game.api.get("/beasts/sniff", ok, err)
        except Exception:
            self.sniffed = None

    def glide_pos(self, eid: str, x: float, y: float) -> tuple[float, float, bool]:
        """Where a gliding character is drawn (on the way, not yet at the landing), and whether it glides."""
        g = self.glides.get(eid)
        if g is None:
            return x, y, False
        k = min(1.0, (self.game.now - g[0]) / max(0.05, g[5]))
        return g[1] + (g[3] - g[1]) * k, g[2] + (g[4] - g[2]) * k, k < 1.0

    def air_of(self, eid: str, x: float, y: float) -> tuple[float, float, float, bool]:
        """(x, y, altitude, on the sword) of a character: flying (or coming down, or falling back),
        in the leap of a hop, or on its feet."""
        now = self.game.now
        gx, gy, gliding = self.glide_pos(eid, x, y)
        f = self.flyers.get(eid)
        if f is not None and f.shown(now):
            return gx, gy, f.alt(now), True
        if gliding:
            g = self.glides[eid]
            return gx, gy, fl.hop_alt((now - g[0]) / max(0.05, g[5])), True
        return x, y, 0.0, False

    def flyer_v2(self, drawables: list, eid: str, realm: str, x: float, y: float, facing: str,
                 weapon: str | None, sword: str, alt: float) -> bool:
        """A character on its flying sword, lifted `alt` world px: the shadow on the ground (drawn
        under every body), wind, mist, wake, sword and body sorted together at the ground row
        plus the height, so a flyer passes over what stands below it."""
        sheet = art2.char_for(realm)
        if sheet is None or not sheet.has("fly"):
            return False
        f = self.flyers.get(eid)
        vx, vy = (f.vx, f.vy) if f is not None else (0.0, 0.0)
        level = f.level if (f is not None and f.level) else 1
        shadows, body = fl.compose(self.view, realm, x, y, facing, self.t, weapon, sword, alt, vx, vy,
                                   self.fly_speed(level), aura_t=self.t, sheet=sheet)
        self.fly_shadows += shadows
        key = y + max(0.0, alt) + 0.5
        for img, pos, flags in body:
            drawables.append((key, img, pos, flags))
        self.drawn_alt[eid] = alt
        return True

    def sword_of(self, realm: str | None) -> str:
        """The flying sword of a realm (the plan's rule, sent with the zone) for a flyer whose own
        record did not name one."""
        fv = self.flight or {}
        return fv.get("sword") or ((self.ability("dap_kiem_luot") or {}).get("sheet")) or "phi_kiem_1"

    def posed_v2(self, drawables: list, realm: str, x: float, y: float, clip: str, t: float, facing: str,
                 weapon: str | None, lift: int = 0, sword: bool = False) -> bool:
        """A character in a pose of its own (on the flying sword, sitting on a mount): the v2
        layers lifted `lift` screen px, sorted at its feet; `sword` adds the flying sword under it."""
        sheet = art2.char_for(realm)
        if sheet is None or not sheet.has(clip):
            return False
        ix, iy = self.view.to_screen(x, y)
        iy -= lift
        if sword:
            sid = (self.ability("dap_kiem_luot") or {}).get("sheet") or "phi_kiem_1"
            ss = art2.weapon(sid)
            if ss is not None and ss.has("fly"):
                ox, oy = ss.offset()
                drawables.append((y, ss.frame(ss.index("fly", t, facing)), (ix + ox, iy + oy)))
        for img, (ox, oy), flags in art2.char_layers(realm, clip, t, facing, weapon, aura_t=self.t, sheet=sheet) or ():
            drawables.append((y, img, (ix + ox, iy + oy), flags))
        return True

    def rider_v2(self, drawables: list, realm: str, x: float, y: float, facing: str, moving: bool, walk_t: float,
                 pet: str | None, weapon: str | None) -> bool:
        """A rider: the mount (its own v2 sheet, larger) and the rider sitting cross-legged on it."""
        mount = petfollow.mount_drawable(pet, x, y, facing, moving, walk_t, self.t, self.view)
        if mount is None:
            return False
        drawables.append(mount)
        return self.posed_v2(drawables, realm, x, y, petfollow.RIDER_CLIP, self.t, facing, weapon,
                             lift=petfollow.MOUNT_LIFT)

    def draw_formations(self, surf) -> None:
        """Bày pháp trận: the formation sheet on the ground, stretched to the radius it slows."""
        now = self.game.now
        for fx_, fy, r, until, fid in self.formations:
            if until <= now or not fid:
                continue
            sh = art2.fx(fid)
            if sh is None:
                continue
            sx, sy = self.view.to_screen(fx_, fy)
            d = int(2 * self.view.len(r) * sh.fw / 90)          # the circle fills ~90 of 96 px
            art2.draw_fx(surf, fid, self.t, sx, sy, size=(d, d))

    def draw_ability_row(self, ui, active: bool) -> None:
        """The thần thông of Luyện Khí over the hotbar: T pháp trận, G lướt, R cưỡi - each drawn
        from its own v2 art, grey with a padlock until its stage of Đạo Thụ, shaded while it rests."""
        if self.abilities is None:
            return
        now = self.game.now
        x0, y0 = 404, 200
        for i, uid in enumerate(("phap_tran", "dap_kiem_luot", "cuoi_linh_thu")):
            a = self.ability(uid)
            if a is None:
                continue
            x = x0 + i * 24
            ui.fill(x, y0, 22, 22, (20, 18, 15, 180))
            ui.border(x, y0, 22, 22, "#3E8E5E" if (uid == "cuoi_linh_thu" and self.riding) else "#8B5A2B")
            img = None
            if uid == "phap_tran":
                s = art2.fx(a.get("fx") or "")
                img = art2.trim(s.frame(s.fx_index(ui.time))) if s is not None else None
            elif uid == "dap_kiem_luot":
                s = art2.weapon(a.get("sheet") or "")
                img = art2.trim(s.frame(s.index("fly", ui.time, "right"))) if s is not None and s.has("fly") else None
            else:
                img = petfollow.picture(self.game.worn_pet() or "tieu_long", ui.time)
            if img is not None:
                k = min(1.0, 18 / max(img.get_width(), img.get_height()))
                ui.image(img, x + 11, y0 + 11, zoom=k, anchor="center")
            ui.text(T.ABILITY_KEYS[uid], x + 2, y0 + 1, 6, "#E9C46A")
            if not a.get("ok"):
                ui.fill(x, y0, 22, 22, (0, 0, 0, 120))
                ui.border(x + 14, y0 + 2, 6, 5, "#B8B1A3")
                ui.fill(x + 13, y0 + 5, 8, 6, "#B8B1A3")
            else:
                ready = {"phap_tran": self.tran_ready, "dap_kiem_luot": self.glide_ready}.get(uid, 0.0)
                total = float(a.get("cooldown") or 1)
                left = ready - now
                if left > 0:
                    frac = min(1.0, left / max(0.1, total))
                    ui.fill(x, y0 + 22 * (1 - frac), 22, 22 * frac, (0, 0, 0, 150))
            if uid == "dap_kiem_luot" and a.get("ok"):
                if self.g_down is not None:        # G held: the take-off charging up the icon
                    k = min(1.0, (now - self.g_down) / fl.HOLD_S)
                    ui.fill(x + 1, y0 + 21 - 20 * k, 20, 20 * k, (110, 220, 235, 90))
                if self.fly:
                    ui.border(x, y0, 22, 22, "#7FDDEB")
            if active and ui.hover(x, y0, 22, 22):
                desc = T.ABILITY_DESC[uid]
                if uid == "dap_kiem_luot" and self.fly_level() >= 2:
                    desc += " " + T.FLY_DESC_HIGH
                ui.set_tooltip(T.ABILITY_TIP.format(name=a.get("name_vi", ""), key=T.ABILITY_KEYS[uid],
                                                    desc=desc) if a.get("ok") else
                               T.ABILITY_LOCKED.format(name=a.get("name_vi", ""),
                                                       stage=(a.get("unlock") or {}).get("stage", "")))
        self.draw_fly_gauge(ui, x0, y0)

    def draw_fly_gauge(self, ui, x0: float, y0: float) -> None:
        """Ngự kiếm's gauge just over the ability row, with its key: it shows in the air and while
        it refills (the low rung); free flight shows a full bar named Phi hành."""
        fv = self.flight or {}
        level = int(fv.get("level") or 0)
        top = float(fv.get("gauge_max") or 0)
        if not level or not self.joined:
            return
        free = self.fly >= 2 or (level >= 2 and not self.fly)
        if free and not self.fly:
            return
        if not free and not self.fly and (top <= 0 or self.fly_gauge >= top - 0.01):
            return
        k = 1.0 if free else max(0.0, min(1.0, self.fly_gauge / max(0.1, top)))
        x, y, w, h = x0, y0 - 9, 70, 6
        ui.fill(x, y, w, h, (20, 18, 15, 200))
        low = not free and k < 0.3
        col = "#7FDDEB" if not low else ("#F4A261" if int(self.game.now * 6) % 2 else "#BC4749")
        if not free and self.fly_gauge < float(fv.get("min_gauge") or 0) and not self.fly:
            col = "#6B7F86"                        # refilling, not yet enough to take off
        ui.fill(x + 1, y + 1, (w - 2) * k, h - 2, col)
        ui.border(x, y, w, h, "#8B5A2B")
        label = f"G · {T.FLY_FREE if free else T.FLY_GAUGE}"
        ui.text(label, x + w / 2, y - 1, 6, "#F4EBD9", anchor="midbottom")

    def draw_taming_panel(self, ui) -> None:
        """While I am taming a beast: its name and the Phản Đòn counted so far, at the top."""
        live = [(eid, tm) for eid, tm in self.taming.items() if eid in self.entities]
        y = 20
        for eid, tm in live[:2]:
            line = (T.BEAST_YIELDED_TOAST.format(name=tm["name"]) if tm["yielded"] else
                    T.BEAST_TAME_PANEL.format(name=tm["name"], n=tm["n"], need=tm["need"]))
            w = ui.text_size(line, 7)[0] + 12
            ui.fill(240 - w / 2, y, w, 11, (20, 18, 15, 190))
            ui.border(240 - w / 2, y, w, 11, "#6A994E" if tm["yielded"] else "#E9C46A")
            ui.text(line, 240, y + 5.5, 7, "#B5D67A" if tm["yielded"] else "#F4EBD9", anchor="center")
            if not tm["yielded"]:
                k = tm["n"] / max(1, tm["need"])
                ui.fill(240 - w / 2 + 1, y + 9, (w - 2) * k, 1.5, "#E9C46A")
            y += 13
        if self.sniffed is not None:             # the worn beast has a nose (the server said so)
            f = self.sniffed[0] if self.sniffed else None
            line = T.BEAST_SNIFF.format(name=f["name_vi"], way=f["way_vi"], d=f["distance_tiles"]) if f \
                else T.BEAST_SNIFF_NONE
            ui.text(line, 240, y + 5, 7, "#E9C46A", anchor="center")

    # ------------------------------------------------------------ v2 helpers
    @property
    def z(self) -> int:
        """Screen pixels per world pixel (2 with the v2 art)."""
        v = getattr(self, "view", None)
        return v.zoom if v is not None else 1

    def spark(self, fid: str | None, x: float, y: float, once: bool = False, delay: float = 0.0,
              scale: float = 1.0) -> None:
        """A one-shot v2 effect at a world point (a looping sheet is played through once)."""
        s = art2.fx(fid)
        if s is not None:
            self.sparks.append([fid, x, y, self.game.now + delay, s.duration if (once or s.loop) else None, scale])
            if len(self.sparks) > 40:
                del self.sparks[0]

    # ------------------------------------------------------------ combat VFX (engine/combat_vfx.py)
    def play_swing(self, eid: str, weapon: str | None, realm: str | None, src, target_id: str | None) -> None:
        """A basic attack's kiếm khí (or arrow, orb, thrust, shock) at the strike frame of the
        clip, sized by the attacker's tier. Presentation only: the server decides the hit."""
        vf = getattr(self, "vfx", None)
        tgt = self.entities.get(target_id or "")
        if vf is None or tgt is None or not art2.on():
            return
        dst = (tgt.pos[0], tgt.pos[1]) if any(tgt.pos[:2]) else src
        lift = self.ent_extent(tgt)[1] / self.z * 0.5
        me = eid == f"p{self.game.state.me.get('id')}"
        land = CV.swing(vf, weapon, self.vfx_tier(eid), src, dst, CV.strike_delay(realm, weapon), lift,
                        follow=eid, mine=me, z=self.z, garnish=self.garnish)
        self.vfx_hold[eid] = self.game.now + land

    def vfx_death(self, ent: Ent, x: float, y: float, me: str) -> None:
        """A monster's death: a burst now, and when its die clip ends it turns to light."""
        vf = getattr(self, "vfx", None)
        sheet = self.ent_sheet(ent) if vf is not None else None
        if sheet is None or not sheet.has("die"):
            return
        n = sheet.index("die", 99.0, FACING[int(ent.pos[2]) % 4])
        lift = self.ent_extent(ent)[1] / self.z * 0.5
        ent.dissolve = True
        CV.death(vf, x, y, lift, (sheet.frame(n), sheet.white(n), sheet.pivot), after=sheet.seconds("die"),
                 mine=getattr(ent, "hit_by", None) == me)
        by, when = getattr(self, "parried", {}).get(ent.id, (None, -9.0))
        pos = self.vfx_where(by) if by and self.game.now - when < 1.5 else None
        if pos is not None:                        # a Phản Đòn kill: the pressure of the realm spreads out
            CV.uy_ap(vf, pos[0], pos[1])
        self.fx.restyle(x, "kill")

    def afterimage(self, eid: str) -> None:
        """Né Đòn: a fading copy of the body where it just was."""
        vf = getattr(self, "vfx", None)
        layers = self.vfx_bodies.get(eid)
        pos = self.vfx_where(eid)
        if vf is None or not layers or pos is None:
            return
        for img, (ox, oy) in layers:
            vf.sprite(img, (-ox, -oy), pos[0], pos[1], life=0.26, peak=0.45, fade_out=0.26, heavy=True)

    def play_chieu(self, f: dict) -> None:
        """A landed chiêu thức drawn by the VFX layer (charge, release, travel, impact, linger)."""
        vf = getattr(self, "vfx", None)
        if vf is None:
            return
        by = f["by"]
        src = self.vfx_where(by) or (f["x"], f["y"])
        dst = None if f["tx"] is None else (float(f["tx"]), float(f["ty"]))
        land = CV.chieu(vf, f["fx"], src, dst, self.vfx_tier(by), f["r"], charged=bool(f.get("charged")),
                        follow=by, mine=by == f"p{self.game.state.me.get('id')}", z=self.z, garnish=self.garnish,
                        ex=f.get("ex"))
        f["vfx"] = True
        self.vfx_hold[by] = self.game.now + land

    def celebrate(self, kind: str) -> None:
        """A stage climbed (`stage_up`) or a realm broken through (`breakthrough`)."""
        vf = getattr(self, "vfx", None)
        if vf is None or not art2.on():
            return
        p, me = self.player, f"p{self.game.state.me.get('id')}"
        if kind == "breakthrough":
            CV.breakthrough(vf, p.x, p.y, follow=me, garnish=self.garnish)
        else:
            CV.stage_up(vf, p.x, p.y, follow=me)

    # ------------------------------------------------------------ loot on the ground, weapon spots, linh căn
    def drop_loot(self, entry: dict, toast) -> bool:
        """A piece of gear of a `loot` message lands where its monster died (False: no place, or
        no v2 art - the caller toasts it at once as before)."""
        if not art2.on() or getattr(self, "ground_loot", None) is None:
            return False
        return self.ground_loot.add(entry, self.game.now, toast)

    def collect_loot(self) -> None:
        if getattr(self, "ground_loot", None) is not None:
            self.ground_loot.collect_all(self.game.toast)

    def draw_spot_glow(self, surf, v, ground: bool) -> None:
        """The weapon spots of Thiên Địa Đồ glow in the colour of their phẩm's rarity: the ring on
        the ground, the column over it; a locked spot only a dim ring, a taken one nothing."""
        size = surf.get_size()
        for sp in self.weapon_spots:
            if sp.state == "taken" or off_screen(v, sp.x, sp.y, size):
                continue
            rarity = spot_rarity(sp.id)
            sx, sy = v.to_screen(sp.x, sp.y)
            if ground:
                if sp.state == "available":
                    art2.draw_fx(surf, f"roi_vong_{rarity}", self.t, sx, sy, scale=0.75)
                else:
                    s = art2.fx(f"roi_vong_{rarity}")
                    if s is not None:
                        img = art2.alpha_copy(art2.scaled(s.frame(0), int(s.fw * 0.75), int(s.fh * 0.75)), 70)
                        if s.additive:
                            img = img.copy()
                            img.fill((90, 90, 90, 255), special_flags=pygame.BLEND_RGBA_MULT)
                        surf.blit(img, (int(sx - img.get_width() / 2), int(sy - img.get_height() / 2)),
                                  special_flags=s.flags)
            elif sp.state == "available":
                art2.draw_fx(surf, f"roi_cot_{rarity}", self.t + sp.tx * 0.1, sx, sy, scale=0.8)

    def linh_can_of(self, eid: str | None) -> int:
        if not eid:
            return 0
        if eid == f"p{self.game.state.me.get('id')}":
            return int(((self.game.state.cult or {}).get("stats") or {}).get("lc") or 0)
        e = self.entities.get(eid)
        return int(getattr(e, "lc", 0) or 0) if e is not None and e.kind == "p" else 0

    @staticmethod
    def draw_lc_mark(ui, x: float, y: float, giai: int) -> None:
        """A 5 px diamond in the giai's colour (from 6 up, a bright heart): nothing that clutters a crowd."""
        col = LC_COLORS[max(1, min(9, giai)) - 1]
        ui.fill(x - 1, y - 3, 3, 7, "#1A1A1A")
        ui.fill(x - 3, y - 1, 7, 3, "#1A1A1A")
        for dy, w in ((-2, 1), (-1, 3), (0, 5), (1, 3), (2, 1)):
            ui.fill(x - w // 2, y + dy, w, 1, col)
        if giai >= 6:
            ui.fill(x, y, 1, 1, "#FFFFFF")

    def ent_sheet(self, e: Ent):
        """The v2 sheet an entity is drawn from (cached on first use), or None."""
        key = (e.kind, e.mtype, e.rank, e.realm, e.beast)
        if getattr(e, "_sheet_key", None) != key:
            e._sheet_key = key
            if e.kind == "m" and e.beast:            # a linh thú: its own beast sheet
                e._sheet = petfollow.sheet(e.mtype)
            elif e.kind == "m":
                e._sheet = art2.monster_for(e.mtype, e.rank)
            elif e.kind == "p":
                e._sheet = art2.char_for(e.realm)
            else:
                e._sheet = None
        return e._sheet

    def ent_extent(self, e: Ent | None) -> tuple[int, int]:
        """(width, height above the feet) of what an entity looks like now."""
        if e is None or not art2.on():
            return 16, 24
        if e.kind == "p":
            return 30, V2_HEAD - 2
        if e.kind == "m":
            s = self.ent_sheet(e)
            if s is not None:
                return art2.extent(s)
        return 16, 24

    def tele_of(self, eid: str) -> list | None:
        for tl in self.teles:
            if len(tl) > 5 and tl[5] == eid and tl[3] > 0:
                return tl
        return None

    # ------------------------------------------------------------ chiêu thức (M9)
    def cast_sheet(self):
        """The Đạo Sĩ sheet that times a chiêu (all looks share the clips): my realm's v2 look,
        else the M8 sheet, else None when this checkout has neither."""
        v2 = art2.char_for((self.game.state.character or {}).get("realm")) if art2.on() else None
        if v2 is not None:
            return v2
        from ..engine import charsheet
        return charsheet.load(CAST_SHEET)

    def cast_clip(self, anim: str) -> str | None:
        """The clip to play for a chiêu: its own, else the slash, else none (then the old swing)."""
        cs = self.cast_sheet()
        if cs is None:
            return None
        if anim in cs.clips:
            return anim
        return "slash" if "slash" in cs.clips else None

    def on_mskill_fx(self, k: str, ev: dict) -> None:
        """`mcast`: the caster starts channelling (the question is open). `mskill`: it landed
        or fizzled - the caster plays the clip again and the effect flies."""
        by, now = ev.get("by"), self.game.now
        anim = ev.get("anim") or "slash"
        clip = self.cast_clip(anim)
        vf = getattr(self, "vfx", None) if art2.on() else None
        if k == "mcast":
            if clip is not None and by:
                self.casting[by] = {"anim": anim, "t0": now, "until": now + CAST_CHANNEL_MAX}
            else:
                self.swing(by)
            pos = self.vfx_where(by) if vf is not None else None
            if pos is not None:
                CV.channel(vf, self.chieu_fx_of(ev.get("s"), anim), by, pos[0], pos[1], self.vfx_tier(by))
            return
        ok = bool(ev.get("ok", 1))
        c = self.casting.get(by)
        charged = c is not None and c["until"] - c["t0"] >= CAST_CHANNEL_MAX
        mine = by == f"p{self.game.state.me.get('id')}"
        x, y = float(ev.get("x", 0.0)), float(ev.get("y", 0.0))
        fx = ev.get("fx") if ev.get("fx") in skill_fx.FX_IDS else "chem"
        dur = skill_fx.duration(fx, ok)
        # the card of the caster's own chiêu covers most of the screen while it shows the result:
        # the animation and the effect then wait for it to go, or nobody would see them
        wait = mine and self.cast_card_open()
        if clip is not None and by:
            secs = max(self.cast_sheet().clips[clip].seconds, 0.45) + 0.15
            if wait and by in self.casting:
                self.casting[by]["land"] = secs
            else:
                self.casting[by] = {"anim": anim, "t0": now, "until": now + secs}
        elif not wait:
            self.swing(by)
        f = {"fx": fx, "ok": ok, "t0": None if wait else now, "dur": dur, "by": by, "x": x, "y": y,
             "tx": ev.get("tx"), "ty": ev.get("ty"), "r": float(ev.get("r") or 0), "charged": charged,
             "ex": chieu_extra(ev)}
        if ok and fx == "kim_chung" and by:          # the bell rings on the hits it takes meanwhile
            self.__dict__.setdefault("bells", {})[by] = now + float(ev.get("d") or 6.0) + 0.6
        self.skill_fx.append(f)
        if vf is not None and ok:
            if wait:
                f["vfx_pending"] = True          # played when the card closes (release_landings)
            else:
                self.play_chieu(f)
        elif vf is not None:
            dst = None if f["tx"] is None else (float(f["tx"]), float(f["ty"]))
            CV.fizzle(vf, fx, self.vfx_where(by) or (x, y), dst, follow=by)
        if not ok:
            self.fx.float_text(T.MSKILL_MISS, x, y - 36, "#D8D8D8", style="miss")
        elif int(ev.get("combo") or 0) > 1:
            self.fx.float_text(T.MSKILL_COMBO.format(n=int(ev["combo"])), x, y - 36, "#E9C46A", style="combo")

    def cast_card_open(self) -> bool:
        """Is the question card of a chiêu on screen? (Not `getattr(sc, "cast")`: this scene has a method of that name.)"""
        from .math_practice import MathCombatQuizScene
        return any(isinstance(sc, MathCombatQuizScene) and sc.cast for sc in self.game.scenes)

    def release_landings(self) -> None:
        """Start the effects and animations that were waiting for the card to close."""
        if self.cast_card_open():
            return
        now = self.game.now
        for f in self.skill_fx:
            if f["t0"] is None:
                f["t0"] = now
                if f.pop("vfx_pending", False):
                    self.play_chieu(f)
        for c in self.casting.values():
            if c.get("land") is not None:
                c["t0"], c["until"] = now, now + c.pop("land")

    def start_cooldown(self, skill_id: str | None) -> None:
        """The chiêu's cooldown runs from the moment its question opens, which is when the server
        starts it too. The `mcast` message says exactly how long; this is the same number from
        the data, so the hotbar is right even if that message is late."""
        sk = next((s for s in self.mskills or [] if s["id"] == skill_id), None)
        if sk is not None:
            self.mskill_ready.setdefault(skill_id, 0.0)
            self.mskill_ready[skill_id] = max(self.mskill_ready[skill_id],
                                              self.game.now + float(sk.get("cooldown", 0)))

    def swing(self, eid: str | None) -> None:
        """The old attack swing, for a chiêu whose caster has no sheet to play."""
        if eid == f"p{self.game.state.me.get('id')}":
            self.swing_t = 0.25
        elif eid in self.entities:
            self.entities[eid].swing_t = 0.25

    def end_channel(self, eid: str) -> None:
        c = self.casting.get(eid)
        if c is not None and c["until"] - c["t0"] >= CAST_CHANNEL_MAX:
            del self.casting[eid]
            if getattr(self, "vfx", None) is not None:
                self.vfx.kill(("chan", eid))

    def chieu_fx_of(self, skill_id: str | None, anim: str) -> str:
        """The effect id of a chiêu (from GET /math/skills), else a guess from its clip."""
        sk = next((s for s in self.mskills or [] if s.get("id") == skill_id), None)
        fx = (sk or {}).get("fx")
        return fx if fx in skill_fx.FX_IDS else ("kiem_khi" if anim == "slash" else "hoa_cau")

    def cast_image(self, eid: str, x: float, y: float, facing: str, cx: int, cy: int):
        """(image, position) of the caster playing its chiêu clip, or None when it is not casting
        or there is nothing to play it from."""
        c = self.casting.get(eid)
        if c is None:
            return None
        now = self.game.now
        cs = self.cast_sheet()
        clip = self.cast_clip(c["anim"])
        if now >= c["until"] or cs is None or clip is None:
            if now >= c["until"]:
                del self.casting[eid]
            return None
        img = cs.at(clip, now - c["t0"], facing if facing in ("down", "up", "left", "right") else "down")
        bx, by = cs.blit_pos(x, y)
        return img, (bx - cx, by - cy)

    def draw_skill_fx(self, surf, cx: int = 0, cy: int = 0, ground: bool = False) -> None:
        """The chiêu effects in flight. With the 2x v2 world the camera's View places them and the
        ground part (formation circles) is drawn in a first pass under the bodies (`ground`)."""
        from ..engine.view import View
        v = getattr(self, "view", None)
        if v is None or v.zoom == 1:
            if ground:
                return
            v = View(1)
            v.ox, v.oy = cx, cy
        now = self.game.now
        me = f"p{self.game.state.me.get('id')}"
        keep = []
        for f in self.skill_fx:
            if f["t0"] is None:                  # waiting for the card to close
                keep.append(f)
                continue
            p = (now - f["t0"]) / max(0.01, f["dur"])
            if p > 1.0:
                continue
            keep.append(f)
            if f.get("vfx"):                     # the VFX layer draws this one (combat_vfx.chieu)
                continue
            sx, sy = f["x"], f["y"]
            if f["by"] == me and not self.dead:
                sx, sy = self.player.x, self.player.y         # the ward follows the caster
            elif f["by"] in self.entities:
                sx, sy = self.entities[f["by"]].pos[0], self.entities[f["by"]].pos[1]
            dst = None if f["tx"] is None else v.to_screen(f["tx"], f["ty"])
            src = v.to_screen(sx, sy)
            if f["ok"] and self.draw_skill_v2(surf, f, max(0.0, p), src, dst, "ground" if ground else "over"):
                continue
            if not ground and v.zoom == 1:
                skill_fx.draw(surf, f["fx"], max(0.0, p), src, dst, ok=f["ok"], radius=f["r"])
            elif not ground:     # the code-drawn effect (a fizzle) at the world's zoom: drawn at 1x, scaled up
                z = v.zoom
                sw, sh = surf.get_size()
                layer = pygame.Surface((sw // z + 1, sh // z + 1), pygame.SRCALPHA)
                half = lambda pt: None if pt is None else (pt[0] / z, pt[1] / z)  # noqa: E731
                if skill_fx.draw(layer, f["fx"], max(0.0, p), half(src), half(dst), ok=f["ok"], radius=f["r"]):
                    surf.blit(pygame.transform.scale(layer, (layer.get_width() * z, layer.get_height() * z)), (0, 0))
        if not ground:
            self.skill_fx = keep

    def draw_skill_v2(self, surf, f: dict, p: float, src, dst, layer: str = "over") -> bool:
        """A chiêu drawn from the v2 FX sheets named in wiring.skill_fx (positions already on screen).
        False: no mapping (or no sheets), and the code-drawn effect is used. A fizzle always keeps
        the code effect. `layer` "ground" draws only the formation circle, "over" the rest."""
        spec = art2.skill_fx(f["fx"])
        if spec is None or art2.fx(spec.get("fx")) is None:
            return False
        kind, main, imp = spec.get("kind"), spec.get("fx"), spec.get("impact")
        z = getattr(getattr(self, "view", None), "zoom", 1)
        t = p * f["dur"]
        if dst is None:
            dst = (src[0] + 28 * z, src[1])
        sx, sy = src
        dx, dy = dst
        chest = 26 if z == 1 else V2_HEAD // 2         # where hands and chests are above the feet (screen px)
        if kind in ("circle", "ward"):            # a ground circle stretched to the radius
            if layer == "ground":
                r = (f["r"] or skill_fx.DEFAULT_RADIUS.get(f["fx"], 40.0)) * z
                cx_, cy_ = (sx, sy) if kind == "ward" else (dx, dy)
                sh = art2.fx(main)
                size = (int(2 * r * sh.fw / 90), int(2 * r * sh.fh / 90))     # the circle fills ~90 of 96 px
                art2.draw_fx(surf, main, t, cx_, cy_, size=size)
            elif kind == "ward":
                art2.draw_fx(surf, imp, t, sx, sy - chest)
            elif t > f["dur"] * 0.3:
                art2.draw_fx(surf, imp, t - f["dur"] * 0.3, dx, dy - 12)
            return True
        if layer == "ground":
            return True
        if kind == "bolt":                          # flies from the caster's hands to the target
            fly = f["dur"] * 0.55
            if t < fly:
                k = t / fly
                bx, by = sx + (dx - sx) * k, (sy - chest) + ((dy - 12) - (sy - chest)) * k
                ang = -math.degrees(math.atan2((dy - 12) - (sy - chest), dx - sx))
                art2.draw_fx(surf, main, t, bx, by, angle=ang)
            else:
                art2.draw_fx(surf, imp, t - fly, dx, dy - 12)
        else:                                       # strike: lands on the target
            ms = art2.fx(main)
            art2.draw_fx(surf, main, t, dx, dy - (0 if ms.pivot[1] > ms.fh * 0.6 else 12))
            land = ms.duration * 0.5
            if t > land:
                art2.draw_fx(surf, imp, t - land, dx, dy - 12)
        return True

    def draw_sparks(self, surf, cx: int = 0, cy: int = 0, ground: bool = False) -> None:
        """One-shot v2 effects at world points; `ground` sheets (cracks) go in the first pass."""
        now = self.game.now
        v = getattr(self, "view", None)
        keep = []
        for s in self.sparks:
            fid, x, y, t0, dur, scale = s
            sheet = art2.fx(fid)
            if sheet is None:
                continue
            if sheet.ground != ground:
                keep.append(s)
                continue
            t = now - t0
            if t < 0:                            # delayed
                keep.append(s)
                continue
            if dur is not None and t > dur:
                continue
            px, py = v.to_screen(x, y) if v is not None else (x - cx, y - cy)
            if art2.draw_fx(surf, fid, t, px, py, scale=scale):
                keep.append(s)
        self.sparks = keep

    def cast_mskill(self, slot: int, hovered: Ent | None) -> None:
        """A chiêu thức key. The server decides everything (floor, qi, cooldown, range): a locked
        chiêu is sent too, so it is the server that says why it is locked."""
        s = self.slot_skill(slot)
        if s is None or self.net is None or self.dead:
            if s is None and self.mskills and not self.dead:
                self.open_cong_phap()                # an empty slot: set it up
            return
        if self.grounded_only():                     # in the air: land first
            return
        target = None
        if s.get("unlocked", True):
            if self.game.now < self.mskill_ready.get(s["id"], 0):
                self.fx.float_text(T.SKILL_FAIL["cooldown"], self.player.x, self.player.y - 30, "#F4EBD9")
                return
            if s.get("effect") not in MSKILL_TARGETLESS:
                target = hovered if (hovered is not None and hovered.kind == "m" and hovered.alive) else \
                    self.nearest_monster(MSKILL_NEAR)
                if target is None:
                    self.fx.float_text(T.MSKILL_NEEDS_TARGET, self.player.x, self.player.y - 30, "#F4EBD9")
                    return
        self.flush_inputs()
        self.net.send({"t": "mskill", "k": s["id"], "id": target.id if target else None})
        if target is not None:
            dx, dy = target.pos[0] - self.player.x, target.pos[1] - self.player.y
            self.player.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")

    def draw_mskill_icon(self, ui, sk: dict, x: float, y: float, locked: bool) -> None:
        """The picture of a chiêu on its slot: the icon named in skills.json. A checkout
        without the icon sheet (it is built by a tool that needs Blender) shows the initials
        of the chiêu's Vietnamese name instead - never a Chinese character."""
        from ..engine import icons
        img = art2.skill_icon(sk.get("id")) if art2.on() else None
        if img is None:
            img = icons.icon(sk.get("icon") or "", int(sk.get("icon_variant") or 0))
        if img is not None:
            ui.image(img, x + 11, y + 11, zoom=0.625, anchor="center")       # a 32 px icon, drawn at 20
        else:
            ui.text(mskill_initials(sk.get("name_vi", "")), x + 11, y + 12, 8,
                    "#6B665C" if locked else "#E9C46A", anchor="center")

    def draw_mskill_row(self, ui, active: bool) -> None:
        """The hotbar: the six chiêu thức, keys 1-6, each with the picture its data names (an
        icon rendered from a 3D model). Locked ones are grey and the tooltip says what opens
        them; a chiêu on cooldown or too dear in Linh Lực is shaded."""
        if not self.mskills:
            return
        x0, y0 = MSKILL_ROW
        now = self.game.now
        qi = (self.game.state.character or {}).get("qi", 0)
        for i in range(len(MSKILL_KEYS)):
            x = x0 + i * 24
            ui.fill(x, y0, 22, 22, (20, 18, 15, 180))
            ui.border(x, y0, 22, 22, "#8B5A2B")
            ui.text(MSKILL_KEY_NAMES[i], x + 2, y0 + 1, 6, "#8E877A")
            sk = self.slot_skill(i)
            if active and ui.click_in(x, y0, 22, 22):          # a click on the bar opens Công Pháp
                ui.consume_click()
                self.open_cong_phap()
            if sk is None:
                if active and ui.hover(x, y0, 22, 22):
                    ui.set_tooltip(T.MSKILL_EMPTY)
                continue
            locked = not sk.get("unlocked", True)
            self.draw_mskill_icon(ui, sk, x, y0, locked)
            if sk.get("qi"):
                ui.text(str(sk["qi"]), x + 20, y0 + 20, 6, "#8CB8DA" if not locked else "#6B665C", anchor="bottomright")
            if locked:
                ui.fill(x, y0, 22, 22, (0, 0, 0, 120))
                ui.border(x + 14, y0 + 2, 6, 5, "#B8B1A3")          # the shackle and body of a padlock
                ui.fill(x + 13, y0 + 5, 8, 6, "#B8B1A3")
            else:
                left = self.mskill_ready.get(sk["id"], 0) - now
                if left > 0:
                    frac = min(1.0, left / max(0.1, sk.get("cooldown", 1)))
                    ui.fill(x, y0 + 22 * (1 - frac), 22, 22 * frac, (0, 0, 0, 150))
                    ui.text(f"{left:.0f}", x + 11, y0 + 11, 8, "#FFFFFF", anchor="center")
                if qi < sk.get("qi", 0):
                    ui.fill(x, y0, 22, 22, (40, 60, 120, 90))
            if active and ui.hover(x, y0, 22, 22):
                ui.set_tooltip((T.MSKILL_TIP_LOCKED.format(name=sk["name_vi"], why=sk.get("locked_vi") or "")
                                if locked else
                                T.MSKILL_TIP.format(name=sk["name_vi"], key=MSKILL_KEY_NAMES[i],
                                                    kind=sk.get("kind_vi", ""), qtype=sk.get("qtype_vi", ""),
                                                    qi=sk.get("qi", 0), cd=sk.get("cooldown", 0),
                                                    desc=sk.get("desc_vi", ""))) + "\n" + T.MSKILL_TIP_BAR)

    # ------------------------------------------------------------ guard bees (stage 5)
    def update_bees(self, dt: float) -> None:
        now = self.game.now
        me = f"p{self.game.state.me.get('id')}"
        owners = [(me, self.player.x, self.player.y, [[b[1], 100, b[5], int(b[4] > 0)] for b in self.my_bees])]
        for e in self.entities.values():
            if e.kind == "p" and e.bees and e.alive:
                owners.append((e.id, e.pos[0], e.pos[1], e.bees))
        for eid, ox, oy, bees in owners:
            for i, b in enumerate(bees):
                sp, _hp, tgt, down = b[0], b[1], b[2], b[3]
                if down:
                    continue                      # resting in the hive
                fb = self.flock.get(f"{eid}:{i}", sp, ox, oy, now)
                fb.target = tgt
                target = self.entities.get(tgt) if tgt else None
                if target is not None and target.alive:
                    fb.update(dt, target.pos[0], target.pos[1] - 4, 6, 120, 12)    # stinging
                else:
                    side = -1 if i % 2 == 0 else 1
                    fb.update(dt, ox + side * (9 + i * 3), oy - 2, 6, 95, 18)      # following the owner
        self.flock.prune(now)

    def update_pets(self, dt: float) -> None:
        from ..engine.petfollow import PetFollower
        me = f"p{self.game.state.me.get('id')}"
        owners = []
        mine = self.game.worn_pet()
        if mine and not self.dead and not self.riding:          # (a ridden beast is under its rider)
            owners.append((me, mine, self.player.x, self.player.y, self.player.facing))
        for e in self.entities.values():
            if e.kind == "p" and e.pet and e.alive and not e.ride:
                owners.append((e.id, e.pet, e.pos[0], e.pos[1], FACING[e.pos[2] % 4] if len(e.pos) > 2 else "down"))
        alive = set()
        for eid, kind, ox, oy, facing in owners:
            f = self.pet_follow.get(eid)
            if f is None or f.kind != kind:
                f = self.pet_follow[eid] = PetFollower(ox, oy)
                f.kind = kind
            f.update(dt, ox, oy, facing)
            alive.add(eid)
        for eid in list(self.pet_follow):
            if eid not in alive:
                del self.pet_follow[eid]

    # ------------------------------------------------------------ movement
    def _typing(self) -> bool:
        return self.game.chatbox.typing

    def on_resume(self):
        if self.realm is None:
            guide.resume_refresh(self.game)
        self.load_mskills()          # back from Đạo Thụ or a trial: a chiêu may have been earned

    def update(self, dt, top):
        self.t += dt
        guide.hud_update(self.game, self)
        self.update_vfx(dt)
        if getattr(self, "ground_loot", None) is not None:
            self.ground_loot.update(self.game.now, self.player.x, self.player.y, self.game.toast,
                                    getattr(self, "vfx", None))
        self.fx.update(dt)
        self.update_bees(dt)
        self.update_pets(dt)
        self.update_beasts(dt)
        self.update_flight(dt)
        self.release_landings()
        self.show_waiting_question()
        self.weather.update(dt, self.game.api)
        self.portal_cool = max(0.0, self.portal_cool - dt)
        self.hurt_flash = max(0.0, self.hurt_flash - dt)
        for tl in self.teles:
            was = tl[3]
            tl[3] -= dt
            if was > 0 >= tl[3] and len(tl) > 5:        # the blow lands: the monster plays its attack
                ent = self.entities.get(tl[5])
                if ent is not None:
                    ent.atk_t0 = self.game.now
        keep_for = -V2_TELE_RELEASE if art2.on() else -0.15
        self.teles = [tl for tl in self.teles if tl[3] > keep_for]
        self.swing_t = max(0.0, self.swing_t - dt)
        for e in self.entities.values():
            e.hurt_t = max(0.0, e.hurt_t - dt)
            e.swing_t = max(0.0, e.swing_t - dt)
        net = self.net
        if not self.joined:
            if net is not None and net.online and (self.join_sent_at is None or self.game.now - self.join_sent_at > 6):
                self.request_join()
            return
        if self.waiting_zone is not None and self.game.now - self.waiting_zone > 4:
            self.waiting_zone = None
        p = self.player
        dx = dy = 0
        if top and not self._typing() and self.waiting_zone is None and net is not None and net.online \
                and not self.dead:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
            dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        p.moving = bool(dx or dy)
        if p.moving:
            total = dt * 1000.0 + self.ms_rem
            ms = int(total)
            self.ms_rem = total - ms
            p.facing = mv.facing_for(dx, dy, p.facing)
            while ms > 0:
                part = min(ms, 100)
                ms -= part
                p.x, p.y = self.step_as(self.fly, p.x, p.y, dx, dy, part, self.move_speed())
                # sent exactly as applied (never merged): the server must repeat the same steps
                self.batch.append([dx, dy, part])
            p.walk_t += dt
        else:
            self.ms_rem = 0.0
        self.batch_t += dt
        if self.batch and (self.batch_t >= SEND_EVERY or len(self.batch) >= 12):
            self.flush_inputs()
        if self.batch_t >= SEND_EVERY:
            self.batch_t = 0.0
        self.watch_g(top and not self._typing())
        self._check_portals()
        for e in self.entities.values():
            if e.pos[3]:
                e.walk_t += dt
        self.target = self.find_target() if top and not self.fly else None   # (nothing to pick up in the air)

    def update_vfx(self, dt: float) -> None:
        """The VFX clock, "reduce effects" from the settings, held hits whose blow has landed, and
        the old `fx.shake` (set by many places) turned into camera trauma."""
        vf = getattr(self, "vfx", None)
        if vf is None:
            return
        vf.reduced = bool(getattr(self.game.cfg, "reduce_effects", False))
        if self.fx.shake > getattr(self, "_shake_seen", 0.0) + 0.01:
            vf.shake(math.sqrt(self.fx.shake) * 0.85)
        self._shake_seen = self.fx.shake
        vf.update(dt)
        self.vfx_release()
        if len(self.vfx_hold) > 40:
            now = self.game.now
            self.vfx_hold = {k: v for k, v in self.vfx_hold.items() if v > now}
            self.vfx_held = {k: v for k, v in self.vfx_held.items() if v > now}

    def flush_inputs(self) -> None:
        if not self.batch or self.net is None:
            return
        steps = [list(s) for s in self.batch]
        if self.net.send({"t": "in", "s": self.seq, "k": steps}):
            self.pending.append((self.seq, steps, self.move_speed()))
            self.seq += 1
        self.batch = []
        self.batch_t = 0.0
        if len(self.pending) > 80:  # the server stopped answering: stop predicting that far ahead
            self.pending.popleft()

    def _check_portals(self) -> None:
        if self.waiting_zone is not None or self.portal_cool > 0:
            return
        p = self.player
        inside = [o for o in self.map.find("portal")
                  if o.x <= p.x <= o.x + o.w and o.y <= p.y <= o.y + o.h]
        if self.portal_refused and not any(o.props.get("target") == self.portal_refused for o in inside):
            self.portal_refused = None        # stepped out of the gate whose land said no
        for o in inside:
            target = o.props.get("target")
            if not target or target == self.portal_refused:
                continue
            self.portal_target = target
            self.flush_inputs()
            self.net.send({"t": "join", "zone": target, "via": "portal"})
            self.waiting_zone = self.game.now
            self.game.toast(T.ENTERING.format(zone=T.ZONE_NAMES.get(target, target)))
            return

    # ------------------------------------------------------------ interaction
    def find_target(self):
        p = self.player
        off = {"up": (0, -10), "down": (0, 6), "left": (-10, -3), "right": (10, -3)}[p.facing]
        fx, fy = p.x + off[0], p.y + off[1]
        best, best_d = None, 22.0
        for o in self.map.interactables_near(fx, fy, best_d):     # (buckets: never every object of a giant map)
            if o.type in ("npc", "interact", "sign"):
                cx, cy = o.x + o.w / 2, o.y + o.h
                d = math.hypot(cx - fx, cy - fy)
                if d < best_d:
                    best, best_d = ("object", o), d
        for sp in self.weapon_spots:                 # Thiên Địa Đồ: a weapon lying here
            if sp.state == "taken":
                continue
            d = math.hypot(sp.x - fx, sp.y - fy)
            if d < best_d:
                best, best_d = ("weapon", sp), d
        for e in self.entities.values():
            if not e.alive:
                continue
            x, y = e.pos[0], e.pos[1]
            d = math.hypot(x - fx, y - fy)
            if d < min(best_d, 26 if e.kind == "r" else 18):
                best, best_d = ("ent", e), d
        return best

    # ------------------------------------------------------------ fighting (stage 4)
    def weapon_range(self) -> float:
        """How far the auto-target looks: the reach of the weapon in hand (bare hands: 22)."""
        kinds = {"brush": 40, "sword": 26, "fan": 32, "staff": 46}
        w = (self.game.state.cult or {}).get("stats", {}).get("weapon")
        t = plan_weapon_type(w)
        return float(PLAN_WEAPON_RANGE[t]) if t else kinds.get(w, 22)

    def nearest_monster(self, max_d: float) -> Ent | None:
        p = self.player
        best, bd = None, max_d
        for e in self.entities.values():
            if e.kind == "m" and e.alive:
                d = math.hypot(e.pos[0] - p.x, e.pos[1] - p.y)
                if d < bd:
                    best, bd = e, d
        return best

    def attack(self, ent: Ent | None) -> None:
        if ent is None or self.net is None or self.dead or self.game.now < self.attack_ready:
            return
        if self.yielded_beast(ent) or self.grounded_only():   # (a yielded beast is sealed; no blow from the air)
            return
        self.flush_inputs()
        self.net.send({"t": "atk", "id": ent.id})
        self.attack_ready = self.game.now + 0.45
        self.swing_t = 0.25
        self.my_atk_t0 = self.game.now
        self.play_swing(f"p{self.game.state.me.get('id')}", (self.game.state.cult or {}).get("stats", {}).get("weapon"),
                        (self.game.state.character or {}).get("realm"), (self.player.x, self.player.y), ent.id)
        dx, dy = ent.pos[0] - self.player.x, ent.pos[1] - self.player.y
        self.player.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")

    def use_pill(self) -> None:
        g = self.game

        def ok(r):
            g.refresh_inv()
        g.api.post("/inventory/use", {"item_id": "hoi_huyet_dan"}, ok, g.api_error)

    def start_fishing(self, bob) -> None:
        if self.grounded_only():
            return
        from .fishing import FishingScene
        self.flush_inputs()
        self.player.moving = False
        self.game.push(FishingScene(self.game, self, "world", bob))

    def action_of(self, target) -> str:
        kind, obj = target
        if kind == "weapon":
            return "weapon"
        if kind == "ent":
            if self.yielded_beast(obj):
                return "seal"
            return "player" if obj.kind == "p" else ("rift" if obj.kind == "r" else "monster")
        if obj.type == "sign":
            return "sign"
        return obj.props.get("action") or ("talk_master" if obj.props.get("npc") == "truc_lao" else "talk_guide")

    def interact(self, target) -> None:
        if self.grounded_only():            # talking, picking up, sealing: on the ground
            return
        kind, obj = target
        if kind == "weapon":
            self.claim_weapon(obj)
            return
        if kind == "object":
            self.talking_to = obj          # v2: that NPC plays its talk clip while the dialog is up
        action = self.action_of(target)
        g = self.game
        if kind == "ent":
            if action == "seal":           # Phong Ấn Phù on a beast that yielded
                self.seal_beast(obj)
            elif obj.kind == "p":
                g.open_player_menu(obj.uid, obj.name, obj.realm)
            elif obj.kind == "r":   # stage 9: a Khe Nứt Mực
                from .realm import RealmGateScene
                g.push(RealmGateScene(g, rift={"id": obj.id, "realm": obj.realm_id, "n": obj.name,
                                               "left": obj.left, "seen": obj.seen}))
            else:
                self.attack(obj)
            return
        if action == "realm":
            from .realm import RealmGateScene
            g.push(RealmGateScene(g))
            return
        if action == "talk_master":
            npc = obj.props.get("npc", "truc_lao")

            def talked(r):
                if r.get("finished"):
                    g.push(DialogScene(g, T.MASTER_QUEST_LINES))
                    g.refresh_quests()
                else:
                    g.push(DialogScene(g, [random.choice(T.MASTER_VILLAGE)]))
            g.api.post("/quests/talk", {"npc": npc}, talked,
                       lambda e: g.push(DialogScene(g, [random.choice(T.MASTER_VILLAGE)])))
        elif action == "forge":
            from .rpg import ForgeScene
            g.push(ForgeScene(g))
        elif action == "quests":
            g.open_quests()
        elif action == "talk_guide":
            g.push(DialogScene(g, T.GUIDE_LINES, speaker=T.GUIDE_NAME, portrait=npc_head("guide")))
        elif action == "library":
            first = not g.state.me.get("met_librarian")
            g.state.me["met_librarian"] = True
            g.push(DialogScene(g, T.LIBRARIAN_LINES if first else [random.choice(T.LIBRARIAN_IDLE)],
                               speaker=T.LIBRARIAN_NAME, portrait=npc_head("librarian"),
                               on_done=g.open_library))
        elif action == "td":     # the Cổng Thủ Thành: the tower defence (Thủ Thành Toán)
            from .math_td import MathTdScene
            first = not g.state.me.get("met_td")
            g.state.me["met_td"] = True
            g.push(MathTdScene(g))
            if first:
                g.push(DialogScene(g, T.TD_GATE_LINES))
        elif action == "gacha":
            from .gacha import GachaScene
            g.push(GachaScene(g, on_close=g.refresh_me))
        elif action == "fisher":
            from .fishing import FishShopScene

            def talked(r):
                first = r.get("finished") or not g.state.me.get("met_fisher")
                g.state.me["met_fisher"] = True
                if r.get("finished"):
                    g.refresh_quests()
                g.push(DialogScene(g, T.FISHER_LINES if first else [random.choice(T.FISHER_IDLE)],
                                   speaker=T.FISHER_NAME, portrait=npc_head("fisher"),
                                   on_done=lambda: g.push(FishShopScene(g))))
            g.api.post("/quests/talk", {"npc": "fisher"}, talked, lambda e: g.push(FishShopScene(g)))
        elif action == "fish_book":
            from .fishing import FishBookScene
            g.push(FishBookScene(g))
        elif action == "alchemy":       # stage 8: the Đan Sư and his public furnace
            def talked(r):
                first = r.get("finished") or not g.state.me.get("met_alchemist")
                g.state.me["met_alchemist"] = True
                if r.get("finished"):
                    g.refresh_quests()
                g.push(DialogScene(g, T.ALCHEMIST_LINES if first else [random.choice(T.ALCHEMIST_IDLE)],
                                   speaker=T.ALCHEMIST_NAME, portrait=npc_head("alchemist"),
                                   on_done=g.open_alchemy))
            g.api.post("/quests/talk", {"npc": "alchemist"}, talked, lambda e: g.open_alchemy())
        elif action == "shop":
            from .shop import ShopScene
            first = not g.state.me.get("met_shopkeeper")
            g.state.me["met_shopkeeper"] = True
            if first:
                g.push(DialogScene(g, T.SHOP_LINES, speaker=T.SHOP_NAME, portrait=npc_head("shopkeeper"),
                                   on_done=lambda: g.push(ShopScene(g))))
            else:
                g.push(ShopScene(g))
        elif action == "math_craft":    # M7: Lò Toán in Loạn Số Cốc
            from .math_craft import MathCraftScene
            g.push(MathCraftScene(g))
        elif action == "sign":
            g.message(obj.props.get("text", ""), T.SIGN_READ)
        elif action in T.COMING:
            g.message(T.COMING[action], T.WORLD_ACTIONS.get(action, obj.name))

    # ------------------------------------------------------------ drawing
    def _char_frame(self, o, cx: float, cy: float):
        """A Blender-rendered character (M8): it idles, and every few seconds runs
        through its slash, which is the whole pipeline on show in the world.

        Returns (None, None) when this checkout has no sheet for it - the sheets are
        built from a .blend by a tool that needs Blender, so a clone without them must
        still play."""
        from ..engine import charsheet
        sheet_id = o.props.get("sheet", "")
        cs = (art2.char_sheet(sheet_id) if art2.on() else None) or charsheet.load(sheet_id)
        if cs is None:
            return None, None
        idle_for = 3.0
        slash = cs.clips.get("slash")
        cycle = idle_for + (slash.seconds if slash else 0.0)
        u = self.t % cycle if cycle > 0 else 0.0
        clip, at = ("slash", u - idle_for) if slash and u >= idle_for else ("idle", u)
        img = cs.at(clip, at, o.props.get("facing", "down"))
        bx, by = cs.blit_pos(o.x + o.w / 2, o.y + o.h)
        return img, (int(bx - cx), int(by - cy))

    def _build_minimap(self) -> pygame.Surface:
        """engine/minimap.py: built from the tile colours (one pixel per tile), never by drawing
        the map; the whole map when it is small, a window round the player on a big one."""
        from ..engine.minimap import MiniMap
        self.mm = MiniMap(self.map)
        self.mm_k = self.mm.k
        return self.mm.frame

    def _cam(self, surf) -> tuple[int, int]:
        """Place the camera (self.view) and return its top-left in screen pixels of the zoomed
        world (= world pixels at zoom 1, exactly as before the v2 art)."""
        w, h = surf.get_size()
        v = self.view
        if art2.on():             # the 2x world: follow the player, kept inside the map or the room
            v.zoom = 2
            room = self.realm.room_rect() if self.realm is not None else None
            v.follow(self.player.x + self.cam_lead[0], self.player.y - 12 + self.cam_lead[1] + self.cam_dip / 2,
                     self.map.px_w, self.map.px_h, w, h, bounds=room)   # (ngự kiếm: a lead, a settle)
            vf = getattr(self, "vfx", None)
            if vf is not None:               # the world shakes, never the HUD or the cards
                v.shake(*vf.offset())
            elif self.fx.shake:
                v.shake(random.randint(-3, 3), random.randint(-3, 3))
            self.cam = v.cam
            return v.ox, v.oy
        v.zoom = 1
        cx = int(self.player.x - w / 2)
        cy = int(self.player.y - 12 - h / 2)
        cx = max(0, min(self.map.px_w - w, cx))
        cy = max(0, min(self.map.px_h - h, cy))
        room = self.realm.room_rect() if self.realm is not None else None
        if room is not None:   # a bí cảnh room fits the screen: keep it still and centred
            cx, cy = int(room.centerx - w / 2), int(room.centery - h / 2)
        vf = getattr(self, "vfx", None)
        if vf is not None:
            dx, dy = vf.offset()
            cx, cy = cx + dx // 2, cy + dy // 2
        elif self.fx.shake:
            cx += random.randint(-2, 2)
            cy += random.randint(-2, 2)
        self.cam = [cx, cy]
        v.ox, v.oy = cx, cy
        return cx, cy

    def _ent_frame(self, e: Ent, facing: int, moving: int) -> pygame.Surface:
        if e.kind == "r":
            return sprites.realm("rift", int(self.t * 6) % 8)
        if e.kind == "m":
            kind = e.mtype if e.mtype in ("ink_slime", "tone_wisp", "ink_fox", "muc_anh", "but_yeu", "nghien_ma") else "ink_slime"
            frames = sprites.monster(kind)
            img = frames[int(self.t * (5 if moving else 2) + hash(e.id) % 7) % len(frames)]
            if kind == "ink_fox" and FACING[facing % 4] == "right":
                img = flipped(img)
            return white(img) if e.hurt_t > 0 else img
        frames = sprites.character(e.appearance)
        f = (0, 1, 0, 2)[int(e.walk_t * 8) % 4] if moving else 0
        img = frames[(FACING[facing % 4], f)]
        return white(img) if e.hurt_t > 0 else img

    def draw_world_v1(self, surf, cx: int, cy: int) -> None:
        """The world as drawn before the v2 art (a checkout without client/assets/v2/)."""
        frame = int(self.t * 3) % 4
        drawables = []
        if self.realm is not None:   # stage 9: puzzle stones, tiles, pillars
            self.realm.floor(surf, cx, cy, frame)
            drawables += self.realm.drawables(cx, cy, frame)
        sw, sh = surf.get_size()
        # telegraphed monster attacks: a red zone that fills up before it lands (spec 8.1)
        for tl in self.teles:
            tx, ty, r, left, total = tl[:5]
            k = 1 - max(0.0, left) / max(0.01, total)
            shape = tele_shape(tl)
            if shape["sh"] != "circle":
                draw_tele_poly(surf, tx - cx, ty - cy, r, shape, k)
                continue
            zone = pygame.Surface((int(r * 2 + 4), int(r * 1.3 + 4)), pygame.SRCALPHA)
            rect = zone.get_rect()
            pygame.draw.ellipse(zone, (188, 71, 73, 50), rect)
            inner = rect.inflate(-rect.w * (1 - k), -rect.h * (1 - k))
            pygame.draw.ellipse(zone, (188, 71, 73, 110), inner)
            pygame.draw.ellipse(zone, (142, 53, 55, 200), rect, 1)
            surf.blit(zone, (int(tx - r - 2) - cx, int(ty - r * 0.65 - 2) - cy))
        for o in self.map.drawables_in(cx - 8, cy - 8, cx + sw + 8, cy + sh + 40):
            if o.x + o.w < cx - 8 or o.x > cx + sw + 8 or o.y + o.h < cy - 8 or o.y > cy + sh + 40:
                continue
            name = o.props.get("sprite")
            if name:
                img = old_prop(name, int(o.props.get("variant", 0) or 0),
                               frame if name in sprites.ANIMATED_PROPS else 0)
                if img is not None:
                    drawables.append((o.foot_y, img, (int(o.x) - cx, int(o.y) - cy)))
            elif o.type == "char":      # M8: a character rendered out of Blender
                img, pos = self._char_frame(o, cx, cy)
                if img is not None:
                    drawables.append((o.foot_y, img, pos))
            elif o.type == "npc":
                look = o.props.get("npc", "guide")
                if look == "truc_lao":
                    img = sprites.truc_lao()[1 if int(self.t * 10) % 37 == 0 else 0]
                else:
                    img = sprites.npc(look)[("down", 0)]
                drawables.append((o.foot_y, img, (int(o.x) - cx, int(o.y) - cy)))
        now = self.game.now
        bars = []
        for e in self.entities.values():
            s = self.interp.sample(e.id, now)
            if s is None:
                continue
            e.pos = s
            x, y, f, m = s
            if not e.alive:
                continue
            img = self._ent_frame(e, f, m)
            cast = self.cast_image(e.id, x, y, FACING[f % 4], cx, cy) if e.kind == "p" and not e.ghost else None
            if cast is not None:                  # M9: playing its chiêu clip from the Đạo Sĩ sheet
                drawables.append((y, cast[0], cast[1]))
                if e.hp < 100:
                    bars.append((x, y - 27, 14, e.hp, "#6A994E"))
                continue
            if e.kind == "r":
                drawables.append((y, img, (int(x - 12) - cx, int(y - 32) - cy)))
            elif e.kind == "m":
                bob = int(abs(math.sin(self.t * 3 + hash(e.id) % 5)) * 2) if e.mtype == "tone_wisp" else 0
                w, ih = img.get_width(), img.get_height()
                drawables.append((y, img, (int(x - w / 2) - cx, int(y - ih - bob) - cy)))
                if e.shield:
                    ring = w + 8
                    drawables.append((y - 0.1, shield_ring(ring, int(self.t * 6) % 4),
                                      (int(x - ring / 2) - cx, int(y - ih / 2 - ring / 2 - bob) - cy)))
                if e.hp < 100:
                    bars.append((x, y - ih - 4 - bob, w, e.hp, "#BC4749"))
            else:
                if e.ghost:
                    img = ghostly(img)
                drawables.append((y, img, (int(x - 8) - cx, int(y - 24) - cy)))
                if e.weapon:
                    drawables.append((y + 0.1, weapon_img(e.weapon, FACING[f % 4], e.swing_t),
                                      weapon_pos(x, y, FACING[f % 4], cx, cy)))
                if e.hp < 100:
                    bars.append((x, y - 27, 14, e.hp, "#6A994E"))
        p = self.player
        mine = self.cast_image(f"p{self.game.state.me.get('id')}", p.x, p.y, p.facing, cx, cy) \
            if not self.dead and not self.ghost else None
        if mine is not None:                       # M9: the chiêu clip, instead of the walking sprite
            drawables.append((p.y, mine[0], mine[1]))
        elif not self.dead:
            drawables.append((p.y, ghostly(p.frame()) if self.ghost else p.frame(), (int(p.x - 8) - cx, int(p.y - 24) - cy)))
            wp = (self.game.state.cult or {}).get("stats", {}).get("weapon")
            if wp:
                drawables.append((p.y + 0.1, weapon_img(wp, p.facing, self.swing_t),
                                  weapon_pos(p.x, p.y, p.facing, cx, cy)))
        for pf in self.pet_follow.values():
            pygame.draw.ellipse(surf, (30, 36, 26), (int(pf.x - 5) - cx, int(pf.y - 1) - cy, 10, 3))
            drawables.append((pf.y, sprites.pet(pf.kind, pf.frame, pf.left), (int(pf.x - 8) - cx, int(pf.y - 13) - cy)))
        species = self.game.state.bee_species
        for fb in self.flock.bees.values():
            look = (species.get(fb.sp) or {}).get("look")
            pygame.draw.ellipse(surf, (30, 36, 26), (int(fb.x - 2) - cx, int(fb.y) - cy, 4, 2))
            drawables.append((fb.y + 6, sprites.bee(look, fb.frame(), fb.left),
                              (int(fb.x - 4) - cx, int(fb.y - fb.z - 4) - cy)))
        for _, img, pos in sorted(drawables, key=lambda d: d[0]):
            surf.blit(img, pos)
        self.draw_skill_fx(surf, cx, cy)           # M9: the effect of a chiêu thức, over the bodies
        if self.fishing is not None:
            from .fishing import draw_rod
            draw_rod(surf, self.fishing, cx, cy, self.t)
        for x, y, w, hp, col in bars:  # small health bars over the hurt ones
            bx, by = int(x - w / 2) - cx, int(y - 4) - cy
            pygame.draw.rect(surf, rgb("K"), (bx - 1, by - 1, w + 2, 4))
            pygame.draw.rect(surf, pygame.Color(col), (bx, by, max(1, int(w * hp / 100)), 2))
        if self.target and self.game.top is self:
            kind, obj = self.target
            if kind == "object":
                tx, ty = obj.x + obj.w / 2, obj.y
            elif kind == "weapon":
                tx, ty = obj.x, obj.y - 20
            else:
                tx, ty = obj.pos[0], obj.pos[1] - 26
            bob = int(math.sin(self.t * 6) * 2)
            pygame.draw.polygon(surf, rgb("o"), [(int(tx) - cx - 3, int(ty) - cy - 8 + bob),
                                                 (int(tx) - cx + 3, int(ty) - cy - 8 + bob),
                                                 (int(tx) - cx, int(ty) - cy - 4 + bob)])

    # ------------------------------------------------------------ drawing with the v2 art (the 2x world)
    def world_to_screen(self, wx: float, wy: float) -> tuple[int, int]:
        """Where a world point is on the 480x270 screen (the one conversion; tests click through it)."""
        return self.view.to_screen(wx, wy)

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        return self.view.to_world(sx, sy)

    def char_pose(self, eid: str, sheet, moving: bool, walk_t: float, weapon: str | None,
                  die_t0: float | None, atk_t0: float | None, hurt_t0: float | None) -> tuple[str, float]:
        """Which clip a v2 character plays now and how far into it: die (held on its last frame)
        > a chiêu > the weapon's attack > the hit flinch > walk / idle."""
        now = self.game.now
        if die_t0 is not None:
            return "die", now - die_t0
        c = self.casting.get(eid)
        if c is not None:
            if now < c["until"]:
                clip = c["anim"] if sheet.has(c["anim"]) else "slash"
                return clip, now - c["t0"]
            del self.casting[eid]
        t0 = self.dodging.get(eid)
        if t0 is not None:
            if sheet.has("dodge") and now - t0 < sheet.seconds("dodge"):
                return "dodge", now - t0
            if now - t0 > 2.0:
                del self.dodging[eid]
        _, attack = art2.weapon_for(weapon)
        if atk_t0 is not None and now - atk_t0 < sheet.seconds(attack):
            return attack, now - atk_t0
        if hurt_t0 is not None and now - hurt_t0 < sheet.seconds("hit"):
            return "hit", now - hurt_t0
        return ("walk", walk_t) if moving else ("idle", self.t)

    def char_v2(self, drawables: list, eid: str, realm: str, x: float, y: float, facing: str, moving: bool,
                walk_t: float, weapon: str | None, die_t0, atk_t0, hurt_t0, ghost: bool, flash: bool) -> bool:
        """Append the layers of one character (aura back, glow, body, weapon, aura front)."""
        sheet = art2.char_for(realm)
        if sheet is None:
            return False
        clip, t = self.char_pose(eid, sheet, moving, walk_t, weapon, die_t0, atk_t0, hurt_t0)
        layers = art2.char_layers(realm, clip, t, facing, weapon, aura_t=self.t, flash=flash, sheet=sheet,
                                  aura=not ghost and die_t0 is None)
        ix, iy = self.view.to_screen(x, y)
        for img, (ox, oy), flags in layers or ():
            drawables.append((y, ghostly(img) if ghost else img, (ix + ox, iy + oy), flags))
        bodies = getattr(self, "vfx_bodies", None)
        if bodies is not None and layers:
            bodies[eid] = [(img, off) for img, off, flags in layers if not flags]
        return True

    def monster_v2(self, e: Ent, x: float, y: float, f: int, moving: int, drawables: list, bars: list) -> None:
        sheet = self.ent_sheet(e)
        now = self.game.now
        v = self.view
        if sheet is None:                         # no v2 sheet for it: the old sprite, at the zoom
            if e.alive:
                img = self._ent_frame(e, f, moving)
                drawables.append((y, v.img(img), v.to_screen(x - img.get_width() / 2, y - img.get_height())))
            return
        w, h = art2.extent(sheet)
        facing = FACING[f % 4]
        tl = self.tele_of(e.id)
        if e.die_t0 is not None:
            clip, t = "die", now - e.die_t0
            if t > sheet.seconds("die") + (0.0 if e.dissolve else 0.4):
                return                            # played once: gone until it respawns (or turned to light)
        elif not e.alive:
            return
        elif e.hurt_t > 0 and sheet.has("hit"):
            clip, t = "hit", 0.15 - e.hurt_t
        elif e.atk_t0 is not None and now - e.atk_t0 < sheet.seconds("attack"):
            clip, t = "attack", now - e.atk_t0
        elif tl is not None and self.stunned.get(e.id, 0.0) <= now:
            clip, t = "windup", tl[4] - tl[3]     # held on its last frame while the zone fills
        elif moving:
            clip, t = "walk", e.walk_t
        else:
            clip, t = "idle", self.t + (sum(map(ord, e.id)) % 7) * 0.13
        if clip in ("windup", "attack") and e.aim is not None:
            facing = face_to(e.aim[0] - x, e.aim[1] - y, facing)
        n = sheet.index(clip, t, facing)
        img = sheet.white(n) if e.hurt_t > 0.1 else sheet.frame(n)
        kx, ky = CV.recoil_offset(e.kick, now)     # shoved back by the blow for a moment
        sx, sy = v.to_screen(x + kx, y + ky)
        drawables.append((y, img, (int(sx - sheet.pivot[0]), int(sy - sheet.pivot[1]))))
        if not e.alive or e.die_t0 is not None:
            return
        if e.shield:
            ring = w + 10
            drawables.append((y + 0.1, shield_ring(ring, int(self.t * 6) % 4),
                              (int(sx - ring / 2), int(sy - h / 2 - ring / 2))))
        if e.hp < 100:
            bars.append((sx, sy - h - 5, max(16, min(30, w)), e.hp, "#BC4749"))

    def draw_teles_v2(self, surf, over: bool = False) -> None:
        """Hit zones: the warn_circle sheet stretched to the real hit radius (the server hits
        everyone within r + 5 of the point), drawn on the ground under the bodies. While the
        monster winds up the ring loops and grows more opaque and a second copy fills it from the
        centre; when the blow lands it flashes. `over`: the second pass after the bodies - only a
        thin bright rim, so the edge of the zone stays visible when someone stands in it."""
        charge = art2.fx(art2.combat_fx("telegraph"))
        release = art2.fx(art2.combat_fx("telegraph_land")) or charge
        if charge is None:
            return
        v = self.view
        for tl in self.teles:
            tx, ty, r, left, total = tl[:5]
            cx_, cy_ = v.to_screen(tx, ty)
            rad = v.len(r + 5)
            shape = tele_shape(tl)
            if shape["sh"] != "circle":
                self.draw_tele_shaped(surf, cx_, cy_, v.len(r), shape, left, total, over)
                continue
            if over:
                if left > 0:
                    pygame.draw.circle(surf, (255, 214, 120), (cx_, cy_), int(rad), 1)
                continue
            d = max(8, int(2 * rad * charge.fw / 92))      # the artwork's circle is 92 of 96 px
            if left > 0:
                k = 1 - left / max(0.01, total)
                ring = art2.scaled(charge.frame(charge.fx_index(self.t)), d, d)
                surf.blit(art2.alpha_copy(ring, 150 + 105 * k), (int(cx_ - d / 2), int(cy_ - d / 2)))
                inner = int(d * k) // 4 * 4
                if inner >= 8:
                    fill = art2.scaled(charge.frame(charge.fx_index(self.t)), inner, inner)
                    surf.blit(art2.alpha_copy(fill, 190), (int(cx_ - inner / 2), int(cy_ - inner / 2)))
            else:
                img = art2.scaled(release.frame(release.fx_index(-left)), d, d)
                surf.blit(img, (int(cx_ - d / 2), int(cy_ - d / 2)))

    def draw_tele_shaped(self, surf, sx: float, sy: float, r: float, shape: dict, left: float, total: float,
                         over: bool) -> None:
        """A cone or a line on the ground: the warn_cone / warn_line sheets (they point right from
        their pivot), stretched to the reach and turned to the direction of the blow. Without the
        sheets, a plain polygon."""
        k = 1 - max(0.0, left) / max(0.01, total)
        # a line's width in screen px; the direction snapped like art2.rotated snaps the artwork
        shape = {**shape, "w": self.view.len(shape["w"]), "a": round(shape["a"] / 15) * 15}
        if over:
            if left > 0:
                draw_tele_poly(surf, sx, sy, r, shape, 1.0, outline_only=True)
            return
        name = "telegraph_" + shape["sh"]
        charge = art2.fx(art2.combat_fx(name))
        if charge is None:
            draw_tele_poly(surf, sx, sy, r, shape, k if left > 0 else 1.0)
            return
        fid = art2.combat_fx(name)
        # the artwork reaches from its pivot (left edge) to 4 px short of the right edge, and a
        # quarter-circle fan (or the line) fills its height
        length = max(8, int(r * charge.fw / max(1, charge.fw - charge.pivot[0] - 4)))
        if shape["sh"] == "cone":
            spread = math.sin(math.radians(min(shape["deg"], 179) / 2)) / math.sin(math.radians(45))
            width = max(8, int(length * spread))
        else:
            width = max(4, int(shape["w"] * charge.fh / max(1, charge.fh - 6)))
        angle = -shape["a"]          # pygame turns counter-clockwise; screen y points down
        if left > 0:
            art2.draw_fx(surf, fid, self.t, sx, sy, size=(length, width), angle=angle)
            inner = int(length * k)
            if inner >= 8:
                art2.draw_fx(surf, fid, self.t, sx, sy, size=(inner, width), angle=angle)
        else:
            land = art2.combat_fx(name + "_land")
            if not (land and art2.draw_fx(surf, land, -left, sx, sy, size=(length, width), angle=angle)):
                art2.draw_fx(surf, fid, self.t, sx, sy, size=(length, width), angle=angle)

    def npc_talking(self, o) -> bool:
        """Is this NPC's dialog on screen (it plays `talk` then)?"""
        if getattr(self, "talking_to", None) is not o:
            return False
        return any(type(sc).__name__ == "DialogScene" for sc in self.game.scenes)

    def draw_world_v2(self, surf) -> None:
        """The world at 2x from the v2 Blender art: autotiled ground (drawn by draw_world), props
        and buildings anchored by their pivots, characters with realm aura, glow and weapon layer,
        monsters that wind up, strike, flinch and die, hit zones and ground FX under the bodies.
        Anything with no v2 picture keeps its old sprite, scaled 2x so its size is right."""
        now = self.game.now
        v = self.view
        frame = int(self.t * 3) % 4
        drawables = []
        self.fly_shadows = []
        self.drawn_alt = {}                        # eid -> world px it is drawn above its feet (name tags)
        if self.realm is not None:   # stage 9: puzzle stones, tiles, pillars
            self.realm.floor(surf, v.ox, v.oy, frame)
            drawables += self.realm.drawables(v.ox, v.oy, frame)
        sw, sh = surf.get_size()
        vf = getattr(self, "vfx", None)
        if vf is not None:                         # scars and rings on the ground, under the hit zones
            vf.draw(surf, v, "ground")
        self.ground_loot.draw_ground(surf, v, self.t, now)
        self.draw_spot_glow(surf, v, ground=True)
        self.draw_teles_v2(surf)
        self.draw_skill_fx(surf, ground=True)      # formation circles lie on the ground
        self.draw_sparks(surf, ground=True)
        self.draw_formations(surf)                 # Bày pháp trận
        vw, vh = v.span(sw, sh)
        for o in self.map.drawables_in(v.x - 40, v.y - 8, v.x + vw + 40, v.y + vh + 80):
            if o.x + o.w < v.x - 40 or o.x > v.x + vw + 40 or o.y + o.h < v.y - 8 or o.y > v.y + vh + 80:
                continue
            d = art2.object_drawable(o, v, self.t, talking=self.npc_talking(o) if o.type == "npc" else False)
            if d is not None:
                drawables.append(d)
            elif o.props.get("sprite"):
                name = o.props["sprite"]
                img = old_prop(name, int(o.props.get("variant", 0) or 0),
                               frame if name in sprites.ANIMATED_PROPS else 0)
                if img is not None:
                    drawables.append((o.foot_y, v.img(img), v.to_screen(o.x, o.y)))
            elif o.type == "char":      # M8: a character rendered out of Blender
                img, _pos = self._char_frame(o, 0, 0)
                if img is not None:
                    cs = art2.char_sheet(o.props.get("sheet", ""))
                    sx, sy = v.to_screen(o.x + o.w / 2, o.y + o.h)
                    piv = cs.pivot if cs is not None else (img.get_width() / 2, img.get_height())
                    drawables.append((o.foot_y, img if cs is not None else v.img(img),
                                      (int(sx - piv[0]), int(sy - piv[1]))))
            elif o.type == "npc":
                look = o.props.get("npc", "guide")
                img = sprites.truc_lao()[1 if int(self.t * 10) % 37 == 0 else 0] if look == "truc_lao" \
                    else sprites.npc(look)[("down", 0)]
                drawables.append((o.foot_y, v.img(img), v.to_screen(o.x, o.y)))
        drawables += self.weapon_drawables(v, (sw, sh))
        drawables += self.ground_loot.drawables(v, now, self.player.x, self.player.y)
        bars = []
        for e in self.entities.values():
            s = self.interp.sample(e.id, now)
            if s is None:
                continue
            e.pos = s
            x, y, f, m = s
            if e.kind == "r":
                if e.alive:
                    from .realm import realm_img
                    drawables.append((y, realm_img(v, "rift", int(self.t * 6) % 8), v.to_screen(x - 12, y - 32)))
                continue
            if e.kind == "m":
                self.monster_v2(e, x, y, f, m, drawables, bars)
                continue
            if not e.alive:
                continue
            if e.die_t0 is not None and e.hp > 0 and now - e.die_t0 > 1.0:
                e.die_t0 = None                    # back on their feet
            ax, ay, alt, on_sword = self.air_of(e.id, x, y)
            if on_sword and e.die_t0 is None:      # ngự kiếm, or the hop of Đạp Kiếm Lướt: on the flying sword
                drawn = self.flyer_v2(drawables, e.id, e.realm, ax, ay, FACING[f % 4], e.weapon,
                                      e.fsword or self.sword_of(e.realm), alt)
            elif e.ride and e.pet and e.die_t0 is None:      # Cưỡi linh thú
                drawn = self.rider_v2(drawables, e.realm, x, y, FACING[f % 4], bool(m), e.walk_t, e.pet, e.weapon)
            else:
                drawn = False
            drawn = drawn or self.char_v2(drawables, e.id, e.realm, x, y, FACING[f % 4], bool(m), e.walk_t, e.weapon,
                                          e.die_t0, e.atk_t0, now - (0.15 - e.hurt_t) if e.hurt_t > 0 else None,
                                          e.ghost, e.hurt_t > 0.1)
            if not drawn:
                img = self._ent_frame(e, f, m)
                drawables.append((y, v.img(ghostly(img) if e.ghost else img), v.to_screen(x - 8, y - 24)))
            if e.hp < 100 and e.die_t0 is None:
                sx, sy = v.to_screen(x, y)
                bars.append((sx, sy - V2_HEAD + 6 - int(alt * v.zoom if on_sword else 0), 16, e.hp, "#6A994E"))
        p = self.player
        me = f"p{self.game.state.me.get('id')}"
        ch = self.game.state.character or {}
        if self.dead and not self.ghost and self.my_die_t0 is None:
            self.my_die_t0 = now                   # dead: the fallen body stays until the respawn
        die_t0 = self.my_die_t0 if self.dead and not self.ghost else None
        wp = (self.game.state.cult or {}).get("stats", {}).get("weapon")
        realm = ch.get("realm", "pham_nhan")
        ax, ay, alt, on_sword = self.air_of(me, p.x, p.y)
        posed = False
        if on_sword and not self.dead:             # ngự kiếm, or the hop: on the flying sword
            posed = self.flyer_v2(drawables, me, realm, ax, ay, p.facing, wp, self.sword_of(realm), alt)
        elif self.riding and not self.dead:        # Cưỡi linh thú: sitting on the worn mount
            posed = self.rider_v2(drawables, realm, p.x, p.y, p.facing, p.moving, p.walk_t, self.game.worn_pet(), wp)
        if not posed and not self.char_v2(drawables, me, realm, p.x, p.y, p.facing, p.moving, p.walk_t,
                                          wp, die_t0, self.my_atk_t0, self.my_hurt_t0, self.ghost, False) \
                and not self.dead:
            drawables.append((p.y, v.img(ghostly(p.frame()) if self.ghost else p.frame()),
                              v.to_screen(p.x - 8, p.y - 24)))
        for pf in self.pet_follow.values():
            bd = petfollow.drawable(pf.kind, pf.x, pf.y, pf.moving, pf.walk_t, self.t, pf.left, v)
            if bd is not None:
                drawables.append(bd)
            elif not petfollow.is_spirit_beast(pf.kind):       # the old sprite (a linh thú has only its v2 sheet)
                sx, sy = v.to_screen(pf.x - 5, pf.y - 1)
                pygame.draw.ellipse(surf, (30, 36, 26), (sx, sy, int(v.len(10)), int(v.len(3))))
                drawables.append((pf.y, v.img(sprites.pet(pf.kind, pf.frame, pf.left)),
                                  v.to_screen(pf.x - 8, pf.y - 13)))
        species = self.game.state.bee_species
        for fb in self.flock.bees.values():
            look = (species.get(fb.sp) or {}).get("look")
            sx, sy = v.to_screen(fb.x - 2, fb.y)
            pygame.draw.ellipse(surf, (30, 36, 26), (sx, sy, int(v.len(4)), int(v.len(2))))
            st = getattr(fb, "sting_t0", None)
            img = art2.bee_frame(fb.sp, fb.t, fb.left, now - st if st is not None else None)
            if img is not None:          # the v2 bee: fly, or sting just after it struck
                bx, by = v.to_screen(fb.x, fb.y - fb.z)
                drawables.append((fb.y + 6, img, (bx - 16, by - 16)))
                continue
            drawables.append((fb.y + 6, v.img(sprites.bee(look, fb.frame(), fb.left)),
                              v.to_screen(fb.x - 4, fb.y - fb.z - 4)))
        for img, pos, flags in self.fly_shadows:  # ngự kiếm: shadows on the ground, under every body
            surf.blit(img, pos, None, flags)
        for d in sorted(drawables, key=lambda d: d[0]):
            surf.blit(d[1], d[2], None, d[3] if len(d) > 3 else 0)
        self.ground_loot.draw_over(surf, v, self.t, now)     # the columns of light over the pieces
        self.draw_spot_glow(surf, v, ground=False)
        if vf is not None:                         # kiếm khí, chiêu and hits over the bodies...
            vf.draw(surf, v, "over")
        self.draw_teles_v2(surf, over=True)        # ...and the zone's rim over them: gameplay first
        self.draw_skill_fx(surf)                   # M9: the effect of a chiêu thức, over the bodies
        self.draw_sparks(surf)
        if self.fishing is not None:
            from .fishing import draw_rod
            draw_rod(surf, self.fishing, v.ox, v.oy, self.t, view=v)
        for x, y, w, hp, col in bars:  # small health bars over the hurt ones (already on screen)
            bx, by = int(x - w / 2), int(y)
            pygame.draw.rect(surf, rgb("K"), (bx - 1, by - 1, w + 2, 4))
            pygame.draw.rect(surf, pygame.Color(col), (bx, by, max(1, int(w * hp / 100)), 2))
        if self.target and self.game.top is self:
            kind, obj = self.target
            if kind == "object":
                tx, ty = v.to_screen(obj.x + obj.w / 2, obj.y + obj.h)
                ty -= art2.object_height(obj, v)
            elif kind == "weapon":
                tx, ty = v.to_screen(obj.x, obj.y)
                ty -= 36
            else:
                tx, ty = v.to_screen(obj.pos[0], obj.pos[1])
                ty -= self.ent_extent(obj)[1] + (8 if obj.kind == "m" else 2)
            bob = int(math.sin(self.t * 6) * 2)
            pygame.draw.polygon(surf, rgb("o"), [(tx - 3, ty - 8 + bob), (tx + 3, ty - 8 + bob), (tx, ty - 4 + bob)])

    def draw_world(self, surf):
        vf = getattr(self, "vfx", None)
        if vf is not None and vf.frozen and not vf.freeze_pending and self.frozen is not None                 and self.frozen.get_size() == surf.get_size():
            surf.blit(self.frozen, (0, 0))         # hit-stop: the picture holds; input does not
            return
        self.draw_world_now(surf)
        nav_hud.draw_world(surf, self)             # Chỉ Đường: the arrow round the player
        if vf is not None and vf.freeze_pending:
            self.frozen = surf.copy()
            vf.freeze_pending = False

    def draw_world_now(self, surf):
        cx, cy = self._cam(surf)
        v2 = art2.on()
        if v2:
            self.map.draw_ground_view(surf, self.view, self.t)
            self.draw_world_v2(surf)
        else:
            self.map.draw_ground(surf, (cx, cy), self.t)
            self.draw_world_v1(surf, cx, cy)
        self.fx.draw(surf, (cx, cy), lambda t, c, size=7: self.game.fonts.render(t, size, c, 1), self.t,
                     view=self.view if v2 else None)
        if self.realm is not None:   # underground: no sky, and the other rooms unseen
            self.realm.outside(surf, cx, cy)
        d = darkness(self.game.day_phase()) if self.realm is None else 0.0
        if d > 0:
            night = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            night.fill((18, 22, 58, int(110 * d)))
            surf.blit(night, (0, 0))
        if self.weather.rain:
            from .fishing import draw_rain
            draw_rain(surf, self.t)
        if getattr(self, "vfx", None) is not None:
            self.vfx.draw_tint(surf)
        if self.hurt_flash > 0:  # "chớp đỏ khi trúng Mặc Kích" (spec 18)
            red = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            red.fill((188, 40, 40, int(160 * min(1.0, self.hurt_flash * 2))))
            surf.blit(red, (0, 0))

    # ------------------------------------------------------------ HUD
    def draw_ui(self, ui):
        top = self.game.top is self
        g = self.game
        cx, cy = self.cam
        now = g.now
        # names and chat bubbles over heads (window resolution, so text stays sharp)
        v2 = art2.on()
        mx, my = self.glide_pos(self.my_eid(), self.player.x, self.player.y)[:2]   # (with the body mid-hop)
        heads = [(mx, my, g.state.character.get("display_name", ""), "#FFFFFF",
                  f"p{g.state.me.get('id')}", V2_HEAD if v2 else 25)]
        for e in self.entities.values():
            if not e.alive:
                continue
            col = "#F4EBD9" if e.kind == "p" else ("#E9C46A" if e.rank == "elite" else "#F08A8C")
            name = e.name if e.rank == "normal" or e.kind == "p" else f"{e.name} · {T.MONSTER_RANK.get(e.rank, '')}"
            if e.beast:                            # a linh thú: what it is, and my taming of it
                name, col = self.beast_label(e), "#B5D67A"
            if v2 and e.kind in ("p", "m"):
                lift = V2_HEAD if e.kind == "p" else self.ent_extent(e)[1] + 7
            else:
                lift = 25 if e.kind == "p" else 22
            heads.append((e.pos[0], e.pos[1], name, col, e.id, lift))
        for d in self.ground_loot.near(self.player.x, self.player.y) if v2 else ():
            heads.append((d.x, d.y, d.name, d.color, None, 34))
        for o in self.map.find("npc"):
            if o.type == "npc":
                lift = 25
                if v2:
                    ns = art2.npc(o.props.get("npc", "guide"))
                    lift = art2.extent(ns)[1] + 4 if ns is not None else 25 * self.z
                heads.append((o.x + o.w / 2, o.y + o.h, o.name, "#E9C46A", None, lift))
        placed: list = []            # name tags already drawn: a tag that would cover one moves up
        bands = nav_hud.band_marks(ui, self)       # Chỉ Đường: band 2-3 monsters near me or under the mouse
        for x, y, name, col, eid, lift in (sorted(heads, key=lambda h: -h[1]) if v2 else heads):
            sx, sy = self.view.to_screen(x, y) if v2 else (x - cx, y - cy)
            lift += int(self.drawn_alt.get(eid, 0.0) * self.z) if eid else 0     # a flyer's tag rides with it
            bx, by = sx, sy - lift
            if not (-40 < bx < 520 and -20 < by < 290):
                continue
            if v2:
                tw = ui.text_size(name, 7)[0]
                for _ in range(3):
                    if not any(abs(bx - px) < (tw + pw) / 2 and abs(by - py) < 8 for px, py, pw in placed):
                        break
                    by -= 8
                placed.append((bx, by, tw))
            ui.text(name, bx + 0.5, by + 0.5, 7, "#1A1A1A", anchor="midbottom")
            ui.text(name, bx, by, 7, col, anchor="midbottom")
            if eid in bands:                       # its band: pips after the name
                nav_hud.draw_band_mark(ui, bx + (tw if v2 else ui.text_size(name, 7)[0]) / 2 + 2, by - 4, *bands[eid])
            giai = self.linh_can_of(eid)
            if giai and v2:                        # a small diamond in the colour of the root's giai
                self.draw_lc_mark(ui, bx - (tw if v2 else 0) / 2 - 5, by - 4, giai)
            b = self.bubbles.get(eid) if eid else None
            if b and b[1] > now:
                self._bubble(ui, b[0], bx, by - 9)
        # player card: portrait, realm, Sinh Lực / Linh Lực / Tu Vi
        ch, me = g.state.character, g.state.me
        cult = g.state.cult or {}
        ui.fill(4, 4, 136, 50, (244, 235, 217, 235))
        ui.border(4, 4, 136, 50, "#8B5A2B")
        ui.fill(7, 7, 28, 28, "#E3D5BA")
        head = art2.portrait(ch.get("realm")) if art2.on() else None
        if head is not None:            # cropped from the v2 idle-down frame of my realm's look
            ui.image(head, 21, 21, zoom=1, anchor="center")
        else:
            head = sprites.character(self.player.appearance)[("down", 0)].subsurface(pygame.Rect(2, 1, 12, 11))
            ui.image(head, 21, 21, zoom=2, anchor="center")
        from .books import portrait_frame, title_after
        portrait_frame(ui, me.get("frame"), 7, 7, 28, 28)
        title_after(ui, me.get("title"), ui.text(ch.get("display_name", ""), 39, 6, 8), 7.5)
        ui.text(cult.get("label") or T.REALMS.get(ch.get("realm", "pham_nhan"), ""), 39, 15, 7, "#6A994E")
        hp, mhp = ch.get("hp", 100), ch.get("max_hp", 100) or 100
        qi, mqi = ch.get("qi", 50), ch.get("max_qi", 50) or 50
        ui.progress(39, 25, 96, 5, hp / mhp, "#BC4749")
        ui.progress(39, 33, 96, 5, qi / mqi, "#4A7CC8")
        ui.text(f"{T.HP} {hp}/{mhp}", 41, 27.5, 6, "#FFFFFF", anchor="midleft")
        ui.text(f"{T.QI} {qi}/{mqi}", 41, 35.5, 6, "#FFFFFF", anchor="midleft")
        need = cult.get("need") or 0
        ui.progress(39, 41, 96, 5, (cult.get("xp", 0) / need) if need else 1.0, "#B8862E")
        ui.text(f"{T.TU_VI} {cult.get('xp', 0)}/{need or '—'}", 41, 43.5, 6, "#FFFFFF", anchor="midleft")
        ui.image((art2.stone_small() or sprites.icon("stone")), 7, 57, zoom=1)
        stones = f"{me.get('spirit_stones', 0):,}".replace(",", ".")
        ui.text(stones, 22 if art2.stone_small() else 18, 60.5, 8, "#FFFFFF", anchor="midleft")
        self.draw_bee_hud(ui, 64, 56)
        from .realm import draw_party_frames
        draw_party_frames(ui, g, 4, 72)
        if self.realm is not None:   # stage 9: the room banner and the puzzle card instead of channel/minimap
            ended = self.realm.ended is not None
            self.draw_hotbar(ui, top and not g.chatbox.typing and not ended)
            g.chatbox.draw(ui, in_zone=self.joined, enabled=top)
            self._hud_buttons(ui, top)
            self.realm.draw_ui(ui, top)
            if not ended:
                self._hud_input(ui, top)
            return
        # zone and channel
        label = f"{self.zone_name} · {T.CHANNEL.format(n=self.channel)}"
        w = ui.text_size(label, 8)[0] + 14
        if ui.button("w_channel", 240 - w / 2, 4, w, 13, label, style="dark", enabled=top and self.joined,
                     tooltip=T.CHANNEL_HINT):
            g.push(ChannelPicker(g, self))
        # minimap (top right)
        mw, mh = self.minimap.get_size()
        mx, my = 476 - mw, 4
        self.mm.draw(ui, mx, my, self)             # gates, players, the Linh Hồ's finds, Chỉ Đường, me
        # quest tracker under the minimap
        quests = [q for q in (g.state.quests or {}).get("quests", []) if q["state"] in ("active", "done")]
        if quests:
            q = quests[0]
            o = q["objective"]
            line = f"{q['title_vi']}  {q['progress']}/{o['count']}"
            col = "#B5D67A" if q["state"] == "done" else "#F4EBD9"
            tw = ui.text_size(line, 7)[0] + 8
            ui.fill(476 - tw, my + mh + 4, tw, 11, (20, 18, 15, 150))
            ui.text(line, 472, my + mh + 9.5, 7, col, anchor="midright")
        guide.draw_tracker(ui, g, 476 - guide.TRACKER_W, my + mh + (18 if quests else 5), top)
        self.draw_taming_panel(ui)                 # Thiên Địa Đồ: taming a linh thú, the Linh Hồ's nose
        # hotbar: the chiêu thức 1-6 and the healing pill (spec 18)
        self.draw_hotbar(ui, top and not g.chatbox.typing)
        self.draw_ability_row(ui, top and not g.chatbox.typing)   # thần thông: T, G, R
        # chat (before hotkeys, so typing never triggers them)
        g.chatbox.draw(ui, in_zone=self.joined, enabled=top)
        self._hud_buttons(ui, top)
        self._hud_input(ui, top)
        nav_hud.hud(ui, self, top)                 # Chỉ Đường: plate, khu banner, N / M / H

    def _hud_buttons(self, ui, top: bool) -> None:
        g = self.game
        typing = g.chatbox.typing
        # buttons, bottom right
        bx = 480 - 4
        for wid, lbl, key, action in [("hud_menu", T.HUD_MENU, pygame.K_ESCAPE, g.open_settings),
                                      ("hud_friends", T.HUD_FRIENDS, pygame.K_p, g.open_friends),
                                      ("hud_quests", T.HUD_QUESTS, pygame.K_j, g.open_quests),
                                      ("hud_char", T.HUD_CHAR, pygame.K_k, g.open_char),
                                      ("hud_book", T.HUD_BOOK, pygame.K_b, g.open_book),
                                      ("hud_pets", T.HUD_PETS, pygame.K_o, g.open_pets),
                                      ("hud_linh_can", T.HUD_LINH_CAN, pygame.K_c, g.open_linh_can),
                                      ("hud_bag", T.HUD_BAG, pygame.K_TAB, g.open_bag),
                                      ("hud_party", T.HUD_PARTY, pygame.K_y, g.open_party),
                                      ("hud_achievements", T.HUD_ACHIEVEMENTS, pygame.K_v, g.open_achievements)]:
            w = ui.text_size(lbl, 8)[0] + 10
            bx -= w + 3
            if ui.button(wid, bx, 252, w, 14, lbl, key=key if (top and not typing) else None, enabled=top):
                action()
        if top and not typing and ui.key(pygame.K_l):
            g.open_library()
        if top and not typing and self.realm is None and ui.key(pygame.K_F1):
            g.open_guide()

    def entity_at(self, wx: float, wy: float) -> Ent | None:
        """The entity whose picture covers a world point (mouse picking). Its box is the picture on
        screen turned back into world pixels, so it follows the zoom (16 x 24 with the old sprites)."""
        hovered = None
        z = self.z
        for e in self.entities.values():
            w_, tall = self.ent_extent(e)
            tall /= z
            reach = (12 if e.kind == "m" else 8) if z == 1 else max(5.0, w_ / 2 / z)
            fy = e.pos[1] - self.drawn_alt.get(e.id, 0.0)       # a flyer's box is its lifted body
            if e.alive and abs(e.pos[0] - wx) < reach and fy - tall < wy < fy + 2:
                hovered = e
        return hovered

    def _clickables(self) -> list:
        """The NPCs, interact objects and signs of the map in map order: the objects a click can
        open. Found by type once per map (a giant land has thousands of props, not one of
        which is clickable), not by a walk over every object at each click."""
        tm = self.map
        key = (id(tm), id(getattr(tm, "_by_type", None)))
        cached = getattr(self, "_click_cache", None)
        if cached is None or cached[0] != key:
            objs = [o for t in ("npc", "interact", "sign") for o in tm.find(t)]
            if len(objs) > 1:
                order = {id(o): i for i, o in enumerate(tm.objects)}
                objs.sort(key=lambda o: order.get(id(o), 0))
            cached = self._click_cache = (key, objs)
        return cached[1]

    def _hud_input(self, ui, top: bool) -> None:
        g = self.game
        typing = g.chatbox.typing
        cx, cy = self.cam
        if not self.joined:
            msg = T.ENTERING.format(zone=self.zone_name) if (self.net and self.net.online) else T.CONNECTING_WORLD
            ui.fill(160, 120, 160, 24, (20, 18, 15, 200))
            ui.text(msg, 240, 132, 9, "#FFFFFF", anchor="center")
        if not top or typing:
            return
        # hover tooltips on entities
        mxw, myw = ui.inp.mouse
        wx, wy = self.view.to_world(mxw, myw) if art2.on() else (mxw + cx, myw + cy)
        hovered = self.entity_at(wx, wy)
        z = self.z
        if hovered is not None and ui.hover(0, 60, 480, 180):
            tip = hovered.name
            if hovered.kind == "p":
                tip += "\n" + T.PLAYER_REALM.format(realm=T.REALMS.get(hovered.realm, hovered.realm))
            elif hovered.kind == "r":
                tip += "\n" + T.REALM_RIFT_LEFT.format(t=int(max(0, hovered.left - (g.now - hovered.seen))))
            elif hovered.kind == "m" and hovered.kv >= 2:          # Chỉ Đường: its band, and if above me
                tip += "\n" + nav_hud.band_tip(self, hovered)
            ui.set_tooltip(tip)
        if self.realm is not None and ui.inp.right_clicked and 20 < myw < 222:   # a ping for the party
            self.realm.mark(wx, wy, 1 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 0)
        # fighting keys: Space attacks the nearest monster, 1-6 cast a chiêu thức, Q drinks a pill
        if ui.key(pygame.K_SPACE):
            self.attack(hovered if hovered is not None and hovered.kind == "m" else
                        self.nearest_monster(self.weapon_range() + 14))
        for i, key in enumerate(MSKILL_KEYS):        # M9: a chiêu thức
            if ui.key(key):
                self.cast_mskill(i, hovered)
        if ui.key(pygame.K_u):                       # Công Pháp: which chiêu sit on keys 1-6
            self.open_cong_phap()
        if ui.key(pygame.K_q):
            self.use_pill()
        if self.rule is not None and (ui.key(pygame.K_LSHIFT) or ui.key(pygame.K_RSHIFT)):
            self.dodge()                             # Né Đòn (the open-world rule)
        if self.abilities is not None:               # thần thông of Luyện Khí (Thiên Địa Đồ)
            if ui.key(pygame.K_t):
                self.place_formation()
            if ui.key(pygame.K_g):
                self.g_pressed()         # tap: Đạp Kiếm Lướt; hold: ngự kiếm; in the air: land
            if ui.key(pygame.K_r):
                self.toggle_ride()
        if self.target:
            act = self.action_of(self.target)
            label = T.WEAPON_SPOT if act == "weapon" else T.WORLD_ACTIONS.get(act, T.SIGN_READ)
            ui.text(T.PRESS_E.format(action=label), 240, 216, 9, "#FFFFFF", anchor="center")
            if ui.key(pygame.K_e):
                self.interact(self.target)
                return
        from .fishing import water_near   # stage 6: F at the water (spec 11.1)
        spot = water_near(self.map, self.player.x, self.player.y, self.player.facing) \
            if not (self.dead or self.fly) else None
        if spot:
            ui.text(T.PRESS_F, 240, 206 if self.target else 216, 9, "#FFFFFF", anchor="center")
            if ui.key(pygame.K_f):
                self.start_fishing(spot[1])
                return
        if ui.inp.clicked and 20 < myw < 222 and not ui.hover(0, 150, 214, 100):
            if hovered is not None:
                ui.consume_click()
                self.interact(("ent", hovered))   # a monster: attack (spec 7.2: left click)
                return
            for o in self._clickables():
                r = o.rect
                if o.type == "npc" and z > 1:     # a v2 NPC stands taller than its map rect
                    up = art2.object_height(o, self.view) / z
                    r = pygame.Rect(r.x, int(r.bottom - max(r.h, up)), r.w, int(max(r.h, up)))
                if o.type in ("npc", "interact", "sign") and r.collidepoint(wx, wy):
                    ui.consume_click()
                    self.interact(("object", o))
                    return

    def draw_bee_hud(self, ui, x: float, y: float) -> None:
        """Own guard bees: portrait, health, resting countdown (spec 10.2.3)."""
        species = self.game.state.bee_species
        for i, b in enumerate(self.my_bees):
            bid, sp, hp, mhp, rest, _tgt = b[:6]
            bx = x + i * 16
            ui.fill(bx, y, 14, 14, (20, 18, 15, 170))
            info = species.get(sp) or {}
            vb = art2.bee_frame(sp, ui.time + i * 0.1, False)
            if vb is not None:     # the v2 bee, cut to its pixels and fitted to the 14 px slot
                vb = art2.trim(vb)
                k = min(1.0, 12 / max(vb.get_width(), vb.get_height()))
                ui.image(vb, bx + 7, y + 6, zoom=k, anchor="center")
            else:
                ui.image(sprites.bee(info.get("look"), int(ui.time * 10 + i) % 2), bx + 7, y + 6, zoom=1, anchor="center")
            if rest > 0:
                ui.fill(bx, y, 14, 14, (0, 0, 0, 150))
                ui.text(f"{int(rest)}", bx + 7, y + 7, 6, "#FFFFFF", anchor="center")
            ui.fill(bx + 1, y + 12, 12, 2, "#3A342C")
            ui.fill(bx + 1, y + 12, 12 * hp / max(1, mhp), 2, "#E9C46A")
            if ui.hover(bx, y, 14, 14) and self.game.top is self:
                name = info.get("name_vi", sp)
                ui.set_tooltip(T.BEE_HUD_DOWN.format(name=name, t=int(rest)) if rest > 0 else
                               T.BEE_HUD_TIP.format(name=name, hp=hp, mx=mhp))

    def draw_hotbar(self, ui, active: bool) -> None:
        x0, y0 = MSKILL_ROW
        self.draw_mskill_row(ui, active)
        # pill slot, after the six chiêu
        x = x0 + len(MSKILL_KEYS) * 24 + 4
        ui.fill(x, y0, 22, 22, (20, 18, 15, 180))
        ui.border(x, y0, 22, 22, "#BC4749")
        ui.text("Q", x + 2, y0 + 1, 6, "#8E877A")
        n = sum(i["qty"] for i in (self.game.state.inv or {}).get("items", []) if i["item_id"] == "hoi_huyet_dan")
        pygame.draw.circle(ui.win, pygame.Color("#BC4749"), ui.d.to_window(x + 11, y0 + 12), int(4 * ui.s))
        ui.text(f"{n}", x + 20, y0 + 20, 7, "#FFFFFF", anchor="bottomright")
        if active and ui.hover(x, y0, 22, 22):
            ui.set_tooltip("Hồi Huyết Đan (Q): hồi 35% Sinh Lực, hồi chung 15 giây")
        if active and ui.click_in(x, y0, 22, 22):
            self.use_pill()

    def _bubble(self, ui, text: str, x: float, y: float) -> None:
        lines = ui.f.wrap(text, 7, int(110 * ui.s), ui.s)[:3]
        w = max(ui.text_size(line, 7)[0] for line in lines) + 6
        h = len(lines) * 8 + 4
        ui.fill(x - w / 2, y - h, w, h, "#FFFFFF")
        ui.border(x - w / 2, y - h, w, h, "#2B2B2B")
        for i, line in enumerate(lines):
            ui.text(line, x, y - h + 2 + i * 8, 7, "#2B2B2B", anchor="midtop")


class ChannelPicker(Scene):
    def __init__(self, game, world: WorldScene):
        super().__init__(game)
        self.world = world

    def draw_ui(self, ui):
        ui.dim(110)
        chans = self.world.channels or [{"n": self.world.channel, "players": 1, "cap": 40}]
        h = 50 + 15 * (len(chans) + 1)
        x, y, w = 160, 40, 160
        ui.panel(x, y, w, h, T.CHANNELS_TITLE)
        ui.text(T.CHANNEL_HINT, x + 10, y + 10, 7, "#5A5A5A", max_w=w - 20)
        cy = y + 30
        for c in chans:
            label = T.CHANNEL_ROW.format(n=c["n"], p=c["players"], cap=c["cap"])
            full = c["players"] >= c["cap"] and c["n"] != self.world.channel
            if ui.button(f"chan_{c['n']}", x + 12, cy, w - 24, 13, label, selected=c["n"] == self.world.channel,
                         enabled=not full):
                self.pick(c["n"])
                return
            cy += 15
        nxt = max(c["n"] for c in chans) + 1
        if ui.button("chan_new", x + 12, cy, w - 24, 13, T.CHANNEL_NEW, style="gold"):
            self.pick(nxt)
            return
        if ui.key(pygame.K_ESCAPE) or (ui.inp.clicked and not ui.hover(x, y, w, h)):
            self.close()

    def pick(self, n: int) -> None:
        self.close()
        if self.game.net is not None and n != self.world.channel:
            self.world.flush_inputs()
            self.game.net.send({"t": "channel", "n": n})
