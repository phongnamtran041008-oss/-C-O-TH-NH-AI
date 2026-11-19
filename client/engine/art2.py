"""The one cached access point to the v2 art rendered out of Blender (client/assets/v2/).

docs/ART_PIPELINE.md is the contract. What is here:

* animated sheets - characters, monsters, spirit beasts, weapon layers, realm glow - in the
  charsheet format, with every frame cut once and kept (`Sheet`);
* FX sheets: the frame at a moment, the pivot, and the blend (`add` sheets are drawn with
  BLEND_RGBA_ADD, `alpha` sheets with an ordinary blit);
* the icon atlases, the base tileset (the same 21 tiles in the same order as
  client/art/build.py TILESET, plus the water frames) and the nature props with their pivots;
* `wiring.json`: which picture goes with which realm, monster, prop, weapon, pet, chiêu or
  item. It is data, so the author can change a mapping without touching code.

**The game must run without any of it.** `client/assets/v2/` is produced by tools that need
Blender; a checkout without it gets None from every accessor here and draws its old art,
exactly as before. Nothing in this module raises on a missing or broken file.

Everything is loaded once and cached: nothing here loads or scales in a draw loop after the
first frame that needed it (scaled and rotated copies go through a bounded cache).
"""
from __future__ import annotations

import json
import math
from collections import OrderedDict
from pathlib import Path

import pygame

from . import charsheet

ROOT = Path(__file__).resolve().parents[1] / "assets" / "v2"
DIRS = ("down", "up", "left", "right")

_root: Path = ROOT
_sheets: dict = {}
_fx: dict = {}
_atlas: dict = {}
_icons: dict = {}
_props: dict = {}
_misc: dict = {}
_scaled: OrderedDict = OrderedDict()
SCALED_MAX = 600


def set_root(path: Path | str | None) -> None:
    """Point the loader somewhere else (tests: an empty folder = a checkout without v2)."""
    global _root
    _root = Path(path) if path else ROOT
    clear()


def root() -> Path:
    return _root


def clear() -> None:
    for c in (_sheets, _fx, _atlas, _icons, _props, _misc, _scaled):
        c.clear()


def _json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text("utf-8"))
    except (OSError, ValueError):
        return None


def _image(path: Path) -> pygame.Surface | None:
    try:
        img = pygame.image.load(str(path))
    except (pygame.error, FileNotFoundError, OSError):
        return None
    try:
        return img.convert_alpha()
    except pygame.error:           # no display yet (a tool): keep it unconverted
        return img


# ------------------------------------------------------------------ wiring
def wiring() -> dict:
    if "wiring" not in _misc:
        _misc["wiring"] = _json(_root / "wiring.json") or {}
    return _misc["wiring"]


def on() -> bool:
    """Is there v2 art to draw (a wiring file and the character sheets)?"""
    if "on" not in _misc:
        _misc["on"] = bool(wiring()) and (_root / "chars").is_dir()
    return _misc["on"]


def _w(section: str) -> dict:
    v = wiring().get(section)
    return v if isinstance(v, dict) else {}


# ------------------------------------------------------------------ animated sheets
class Sheet(charsheet.CharSheet):
    """A charsheet with every frame cut once (stable surfaces, so caches keyed on them hold),
    the events of its clips, and FX timing when it is an FX sheet."""

    def __init__(self, doc: dict, sheet: pygame.Surface):
        doc = dict(doc)
        doc.setdefault("clips", {})
        super().__init__(doc, sheet)
        self.events = doc.get("events") or {}
        self.fps = float(doc.get("fps") or 10)
        self.loop = bool(doc.get("loop", True))
        self.additive = doc.get("blend") == "add"
        self.ground = bool(doc.get("ground"))
        self.flags = pygame.BLEND_RGBA_ADD if self.additive else 0
        self._frames: list = [None] * self.total
        self._white: dict = {}

    def frame(self, n: int) -> pygame.Surface:
        n = max(0, min(self.total - 1, int(n)))
        f = self._frames[n]
        if f is None:
            f = self._frames[n] = super().frame(n)
        return f

    def clip(self, name: str):
        return self.clips.get(name)

    def has(self, name: str) -> bool:
        return name in self.clips

    def seconds(self, name: str) -> float:
        c = self.clips.get(name)
        return c.seconds if c else 0.0

    def index(self, clip: str, t: float, facing: str = "down") -> int:
        c = self.clips.get(clip) or self.clips.get("idle") or next(iter(self.clips.values()), None)
        if c is None:
            return 0
        return c.index_at(max(0.0, t), facing if facing in DIRS else "down")

    def white(self, n: int) -> pygame.Surface:
        """The hit flash of frame n: the same shape painted white."""
        w = self._white.get(n)
        if w is None:
            w = self.frame(n).copy()
            w.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
            self._white[n] = w
        return w

    # FX timing (a sheet without clips: the whole sheet is one clip)
    @property
    def duration(self) -> float:
        return self.total / self.fps if self.fps > 0 else 0.0

    def fx_index(self, t: float) -> int:
        n = int(max(0.0, t) * self.fps)
        return n % self.total if self.loop else min(n, self.total - 1)

    def offset(self) -> tuple[int, int]:
        return -int(round(self.pivot[0])), -int(round(self.pivot[1]))


def _load_sheet(folder: str, sid: str) -> Sheet | None:
    key = (folder, sid)
    if key in _sheets:
        return _sheets[key]
    s = None
    doc = _json(_root / folder / f"{sid}.json")
    if doc and "frame" in doc:
        img = _image(_root / folder / doc.get("sheet", f"{sid}.png"))
        if img is not None:
            try:
                s = Sheet(doc, img)
            except (KeyError, ValueError, TypeError):
                s = None
    _sheets[key] = s
    return s


def char(look: str | None) -> Sheet | None:
    return _load_sheet("chars", f"dao_si_{look}") if look else None


def char_sheet(sheet_id: str | None) -> Sheet | None:
    """A character sheet by its full id ("dao_si_truc_co"), as map objects name them."""
    return _load_sheet("chars", sheet_id) if sheet_id else None


def monster(sid: str | None) -> Sheet | None:
    return _load_sheet("monsters", sid) if sid else None


def beast(sid: str | None) -> Sheet | None:
    return _load_sheet("beasts", sid) if sid else None


def weapon(layer: str | None) -> Sheet | None:
    return _load_sheet("weapons", layer) if layer else None


def fx(fid: str | None) -> Sheet | None:
    return _load_sheet("fx", fid) if fid else None


# ------------------------------------------------------------------ scaled / rotated copies
def scaled(img: pygame.Surface, w: int, h: int) -> pygame.Surface:
    """A nearest-neighbour copy at (w, h), cached (bounded)."""
    w, h = max(1, int(w)), max(1, int(h))
    if img.get_size() == (w, h):
        return img
    key = ("s", img, w, h)
    s = _scaled.get(key)
    if s is None:
        s = pygame.transform.scale(img, (w, h))
        _scaled[key] = s
        if len(_scaled) > SCALED_MAX:
            _scaled.popitem(last=False)
    else:
        _scaled.move_to_end(key)
    return s


def rotated(img: pygame.Surface, degrees: float, step: int = 15) -> pygame.Surface:
    """Rotated copy, angle snapped to `step` degrees so the cache stays small."""
    a = int(round(degrees / step) * step) % 360
    if a == 0:
        return img
    key = ("r", img, a)
    s = _scaled.get(key)
    if s is None:
        s = pygame.transform.rotate(img, a)
        _scaled[key] = s
        if len(_scaled) > SCALED_MAX:
            _scaled.popitem(last=False)
    else:
        _scaled.move_to_end(key)
    return s


def alpha_copy(img: pygame.Surface, alpha: int, step: int = 16) -> pygame.Surface:
    """`img` with its per-pixel alpha multiplied by alpha/255 (snapped), cached."""
    a = max(0, min(255, int(alpha) // step * step))
    if a >= 255 - step + 1:
        return img
    key = ("a", img, a)
    s = _scaled.get(key)
    if s is None:
        s = img.copy()
        s.fill((255, 255, 255, a), special_flags=pygame.BLEND_RGBA_MULT)
        _scaled[key] = s
        if len(_scaled) > SCALED_MAX:
            _scaled.popitem(last=False)
    else:
        _scaled.move_to_end(key)
    return s


def trim(img: pygame.Surface) -> pygame.Surface:
    """`img` cut to its opaque pixels (for UI pictures), cached."""
    key = ("t", img)
    s = _scaled.get(key)
    if s is None:
        r = img.get_bounding_rect()
        s = img.subsurface(r) if r.w and r.h else img
        _scaled[key] = s
        if len(_scaled) > SCALED_MAX:
            _scaled.popitem(last=False)
    return s


def extent(sheet: "Sheet | None") -> tuple[int, int]:
    """(width, height above the feet) of the sheet's standing pose, for bars and name tags."""
    if sheet is None:
        return 16, 24
    key = ("extent", sheet.id)
    if key not in _misc:
        f = sheet.frame(sheet.index("idle", 0, "down")) if sheet.clips else sheet.frame(0)
        r = f.get_bounding_rect()
        _misc[key] = (max(8, r.w), max(8, int(sheet.pivot[1] - r.top))) if r.h else (sheet.fw, sheet.fh)
    return _misc[key]


def draw_fx(surf: pygame.Surface, fid: str, t: float, x: float, y: float, scale: float = 1.0,
            angle: float = 0.0, size: tuple[int, int] | None = None) -> bool:
    """Draw FX `fid` at `t` seconds with its pivot on (x, y). Returns False when there is no
    such sheet or a one-shot is over."""
    s = fx(fid)
    if s is None or (not s.loop and t > s.duration):
        return False
    img = s.frame(s.fx_index(t))
    px, py = s.pivot
    if size is not None or scale != 1.0:
        w, h = size if size is not None else (s.fw * scale, s.fh * scale)
        kx, ky = w / s.fw, h / s.fh
        img = scaled(img, w, h)
        px, py = px * kx, py * ky
    if angle:
        cx, cy = img.get_width() / 2, img.get_height() / 2
        rimg = rotated(img, angle)
        # rotate the pivot about the centre (pygame turns counter-clockwise)
        r = math.radians(-int(round(angle / 15) * 15))
        dx, dy = px - cx, py - cy
        px = rimg.get_width() / 2 + dx * math.cos(r) - dy * math.sin(r)
        py = rimg.get_height() / 2 + dx * math.sin(r) + dy * math.cos(r)
        img = rimg
    surf.blit(img, (int(x - px), int(y - py)), special_flags=s.flags)
    return True


# ------------------------------------------------------------------ icons
def _atlas_doc(set_id: str):
    if set_id not in _atlas:
        doc = _json(_root / "icons" / f"{set_id}.json")
        img = _image(_root / "icons" / doc.get("sheet", f"{set_id}.png")) if doc else None
        _atlas[set_id] = (doc, img) if (doc and img is not None) else None
    return _atlas[set_id]


def icon(set_id: str | None, icon_id: str | None) -> pygame.Surface | None:
    """A 32 px icon, or None."""
    if not set_id or not icon_id:
        return None
    key = (set_id, icon_id)
    if key in _icons:
        return _icons[key]
    out = None
    a = _atlas_doc(set_id)
    if a is not None:
        doc, img = a
        e = (doc.get("icons") or {}).get(icon_id)
        if e is not None:
            cell, cols, n = int(doc["cell"]), int(doc["cols"]), int(e["index"])
            r = pygame.Rect((n % cols) * cell, (n // cols) * cell, cell, cell)
            if img.get_rect().contains(r):
                out = img.subsurface(r)
    _icons[key] = out
    return out


def icon_ids(set_id: str) -> list[str]:
    a = _atlas_doc(set_id)
    return sorted((a[0].get("icons") or {})) if a else []


def _icon_ref(ref) -> pygame.Surface | None:
    if isinstance(ref, (list, tuple)) and len(ref) == 2:
        return icon(ref[0], ref[1])
    return None


def item_icon(row: dict) -> pygame.Surface | None:
    """The icon of an inventory row or piece of equipment, by the rules of wiring.item_icons."""
    rules = _w("item_icons")
    if not rules:
        return None
    item_id = row.get("item_id") or row.get("id") or ""
    kind, slot = row.get("kind"), row.get("slot")
    for table, key in (("by_id", item_id), ("by_weapon", kind), ("by_kind", kind), ("by_slot", slot)):
        ref = (rules.get(table) or {}).get(key) if key else None
        if ref:
            return _icon_ref(ref)
    return None


def skill_icon(skill_id: str | None) -> pygame.Surface | None:
    return _icon_ref(_w("skill_icons").get(skill_id or ""))


def stone_icon() -> pygame.Surface | None:
    return _icon_ref(_w("item_icons").get("spirit_stone"))


# ------------------------------------------------------------------ tiles and props
class TileSet:
    def __init__(self, tiles: list[pygame.Surface], water: list[pygame.Surface], water_fps: float,
                 alternates: dict | None = None, size: int = 16, native: bool = True):
        self.tiles, self.water, self.water_fps = tiles, water, water_fps
        self.alternates = alternates or {}      # tile index -> [the tile, its extra variants]
        self.size = size                        # pixels per tile
        self.native = native                    # False: scaled up from a smaller sheet (a fallback)

    def pick(self, index: int, x: int, y: int) -> pygame.Surface:
        """The tile at a map cell: the same every time, but varied where the tile has extra variants."""
        alts = self.alternates.get(index)
        if not alts:
            return self.tiles[index]
        return alts[(x * 7 + y * 13 + (x * y) % 5) % len(alts)]


def _cut_grid(img: pygame.Surface, size: int, cols: int):
    def cut(n):
        r = pygame.Rect((n % cols) * size, (n // cols) * size, size, size)
        return img.subsurface(r) if img.get_rect().contains(r) else None
    return cut


def _tile_doc(name: str):
    """(doc, image, cell size, cut) of a tile sheet, or None."""
    doc = _json(_root / "tiles" / f"{name}.json")
    img = _image(_root / "tiles" / doc.get("sheet", f"{name}.png")) if doc else None
    if not doc or img is None:
        return None
    size, cols = int(doc.get("cell") or doc.get("tile") or 16), int(doc.get("cols", 8))
    return doc, img, size, _cut_grid(img, size, cols)


def _tileset_entries():
    from ..art import build as B
    return list(B.TILESET)


def _load_tileset(name: str, count: int) -> TileSet | None:
    """The base tiles of a sheet, looked up BY NAME (`tiles: {name: [indices]}`): entry i of
    build.TILESET (name, variant) is tiles[name][variant]. Extra indices after a name's TILESET
    variants, and the indices of `<name>_alt`, are its alternates. Missing tiles are None."""
    t = _tile_doc(name)
    if t is None:
        return None
    doc, img, size, cut = t
    names = (doc.get("tiles") or {})
    entries = _tileset_entries()[:count]
    variants: dict = {}
    for n, v in entries:
        variants[n] = max(variants.get(n, 0), v + 1)
    tiles = []
    alternates = {}
    wa = doc.get("water_anim") or {}
    anim = set(wa.get("frames", []))
    for i, (n, v) in enumerate(entries):
        idx = names.get(n) or []
        tiles.append(cut(idx[v]) if v < len(idx) else None)
        if tiles[-1] is None:
            continue
        extra = [j for j in idx[variants[n]:] if j not in anim] if v == 0 else []
        extra += names.get(f"{n}_alt") or [] if v == 0 else []
        alts = [tiles[-1]] + [s_ for s_ in (cut(j) for j in extra) if s_ is not None]
        if len(alts) > 1:
            alternates[i] = alts
    water = [cut(j) for j in wa.get("frames", [])]
    water = [w_ for w_ in water if w_ is not None]
    return TileSet(tiles, water, float(wa.get("fps", 2)), alternates, size)


def tileset(count: int = 21) -> TileSet | None:
    """The 16 px base tiles 0..count-1 (gid = index + 1, same order as build.TILESET) and the
    water frames, or None (also when a tile is missing)."""
    if "tiles" not in _misc:
        ts = _load_tileset("base", count)
        _misc["tiles"] = ts if ts is not None and all(t is not None for t in ts.tiles) else None
    return _misc["tiles"]


def _x2(img: pygame.Surface) -> pygame.Surface:
    return pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))


def tileset32(count: int = 21) -> TileSet | None:
    """The base tiles for the 2x world: each tile from `base32` where that sheet has it, else the
    16 px tile scaled 2x nearest. `native` is True only when every tile came from base32."""
    if "tiles32" not in _misc:
        small = tileset(count)
        big = _load_tileset("base32", count)
        if big is not None and big.size != 32:
            big = None
        if small is None and big is None:
            _misc["tiles32"] = None
            return None
        tiles, alternates, native = [], {}, True
        for i in range(count):
            t = big.tiles[i] if big is not None and i < len(big.tiles) else None
            if t is not None:
                tiles.append(t)
                if i in big.alternates:
                    alternates[i] = big.alternates[i]
            elif small is not None:
                native = False
                tiles.append(_x2(small.tiles[i]))
                if i in small.alternates:
                    alternates[i] = [_x2(a) for a in small.alternates[i]]
            else:
                _misc["tiles32"] = None
                return None
        water = big.water if big is not None and big.water else [_x2(w) for w in (small.water if small else [])]
        fps = big.water_fps if big is not None and big.water else (small.water_fps if small else 2.0)
        _misc["tiles32"] = TileSet(tiles, water, fps, alternates, 32, native=native and bool(big and big.water))
    return _misc["tiles32"]


def terrain32() -> tuple[dict, bool]:
    """The transition tiles at 32 px by name ({name: [surfaces]}): the 16 px `terrain` scaled 2x,
    with every name `terrain32` has replaced by its native tile (and its new names added).
    The flag says whether terrain32 was there at all."""
    if "terrain32" not in _misc:
        out, native = {}, False
        for name in ("terrain", "terrain32"):
            t = _tile_doc(name)
            if t is None:
                continue
            doc, img, size, cut = t
            for tname, idx in (doc.get("tiles") or {}).items():
                surfs = [cut(i) for i in (idx if isinstance(idx, list) else [idx])]
                surfs = [s_ if size == 32 else _x2(s_) for s_ in surfs if s_ is not None]
                if surfs:
                    out[tname] = surfs
            native = native or (name == "terrain32" and size == 32)
        _misc["terrain32"] = (out, native)
    return _misc["terrain32"]


class Prop:
    def __init__(self, img: pygame.Surface, pivot: tuple[int, int], solid, frames: list | None = None,
                 fps: float = 3.0):
        self.img, self.pivot, self.solid = img, pivot, solid
        self.frames = frames or [img]
        self.fps = fps

    def at(self, t: float) -> pygame.Surface:
        return self.frames[int(t * self.fps) % len(self.frames)] if len(self.frames) > 1 else self.img


def _prop_atlas(atlas: str):
    key = ("atlas", atlas)
    if key not in _props:
        doc = _json(_root / "props" / f"{atlas}.json")
        img = _image(_root / "props" / doc.get("sheet", f"{atlas}.png")) if doc else None
        _props[key] = (doc, img) if (doc and img is not None) else None
    return _props[key]


def prop(name: str | None, atlas: str = "nature") -> Prop | None:
    """A prop of an atlas (`nature`, `buildings`): image, pivot (relative to its rect), solid
    footprint, and its frames when it is animated (laid side by side, each `rect` wide, unless
    the entry lists `frame_rects`)."""
    if not name:
        return None
    key = (atlas, name)
    if key not in _props:
        out = None
        a = _prop_atlas(atlas)
        if a is not None:
            e = (a[0].get("props") or {}).get(name)
            if e is not None:
                r = pygame.Rect(*e["rect"])
                n = int(e.get("frames", 1) or 1)
                rects = [pygame.Rect(*fr) for fr in e["frame_rects"]] if e.get("frame_rects") else                     [r.move(i * r.w, 0) for i in range(n)]
                if all(a[1].get_rect().contains(fr) for fr in rects):
                    frames = [a[1].subsurface(fr) for fr in rects]
                    out = Prop(frames[0], (int(e["pivot"][0]), int(e["pivot"][1])), e.get("solid"), frames,
                               float(e.get("fps", 3) or 3))
        _props[key] = out
    return _props[key]


def prop_for(old_name: str, variant: int = 0) -> Prop | None:
    """The v2 prop that replaces the old map sprite `old_name` (picked by variant), or None:
    nature props first, then buildings (wiring.buildings)."""
    for section, atlas in (("props", "nature"), ("buildings", "buildings")):
        choices = _w(section).get(old_name)
        if isinstance(choices, list) and choices:
            return prop(choices[int(variant) % len(choices)], atlas)
    return None


def npc(kind: str | None) -> Sheet | None:
    """An NPC on the v2 body (npcs/<id>: idle, walk, talk), or None."""
    sid = _w("npcs").get(kind or "") if (kind and on()) else None
    return _load_sheet("npcs", sid) if sid else None


# ------------------------------------------------------------------ mappings
def realm_entry(realm: str | None) -> dict:
    e = _w("realms").get(realm or "pham_nhan")
    return e if isinstance(e, dict) else {}


def look_for(realm: str | None) -> str | None:
    if not on():
        return None
    return realm_entry(realm).get("look") or wiring().get("default_look")


def char_for(realm: str | None) -> Sheet | None:
    return char(look_for(realm))


def aura_for(realm: str | None) -> tuple[Sheet | None, Sheet | None]:
    a = realm_entry(realm).get("aura")
    if not a:
        return None, None
    return fx(f"aura_{a}_back"), fx(f"aura_{a}_front")


def glow_for(look: str | None) -> Sheet | None:
    return fx(_w("glow").get(look or "")) if look else None


def portrait(realm: str | None) -> pygame.Surface | None:
    """The HUD head: a crop of the idle-down frame of the realm's look."""
    look = look_for(realm)
    s = char(look)
    if s is None:
        return None
    key = ("portrait", look)
    if key not in _misc:
        rect = (wiring().get("portrait") or {}).get("rect") or [37, 30, 22, 22]
        f = s.frame(s.index("idle", 0, "down"))
        r = pygame.Rect(*rect).clip(f.get_rect())
        _misc[key] = f.subsurface(r)
    return _misc[key]


def npc_portrait(kind: str | None) -> pygame.Surface | None:
    """An NPC's head for the dialog box: a 20x20 crop of its v2 idle-down frame, or None."""
    s = npc(kind)
    if s is None:
        return None
    key = ("npc_portrait", kind)
    if key not in _misc:
        f = s.frame(s.index("idle", 0, "down"))
        _misc[key] = f.subsurface(pygame.Rect(38, 31, 20, 20).clip(f.get_rect()))
    return _misc[key]


def monster_id(mtype: str | None, rank: str = "normal", subject: str | None = None) -> str | None:
    if not on():
        return None
    sid = _w("monsters").get(mtype or "")
    if not sid and subject:
        sid = (_w("monster_subjects").get(subject) or {}).get(rank or "normal")
    if not sid:
        sid = _w("monster_default").get(rank or "normal")
    return sid or None


def monster_for(mtype: str | None, rank: str = "normal", subject: str | None = None) -> Sheet | None:
    return monster(monster_id(mtype, rank, subject))


def floats(sheet_id: str | None) -> bool:
    return sheet_id in (wiring().get("monster_float") or [])


def td_monster(kind: str) -> tuple[Sheet | None, float]:
    e = _w("td_monsters").get(kind) if on() else None
    if not isinstance(e, dict):
        return None, 1.0
    return monster(e.get("sheet")), float(e.get("scale", 1.0))


def weapon_for(kind: str | None) -> tuple[Sheet | None, str]:
    """(layer sheet, attack clip) for an equipped weapon kind."""
    e = _w("weapons").get(kind or "") if (kind and on()) else None
    if not isinstance(e, dict):
        return None, "slash"
    return weapon(e.get("layer")), e.get("clip") or "slash"


def beast_for(pet_kind: str | None) -> Sheet | None:
    return beast(_w("pets").get(pet_kind or "")) if (pet_kind and on()) else None


def skill_fx(fx_id: str | None) -> dict | None:
    e = _w("skill_fx").get(fx_id or "") if on() else None
    return e if isinstance(e, dict) else None


def combat_fx(name: str) -> str | None:
    return _w("combat_fx").get(name) if on() else None


# ------------------------------------------------------------------ drawing a character
def char_layers(realm: str | None, clip: str, t: float, facing: str, weapon_kind: str | None = None,
                aura_t: float = 0.0, flash: bool = False, sheet: Sheet | None = None,
                aura: bool = True) -> list | None:
    """The layers of one character as [(surface, (dx, dy) from the feet, blend flags)], in draw
    order: aura back, glow, body, weapon layer, aura front. None when there is no sheet."""
    look = look_for(realm)
    body = sheet or char(look)
    if body is None:
        return None
    n = body.index(clip, t, facing)
    off = body.offset()
    out = []
    back, front = aura_for(realm) if aura else (None, None)
    if back is not None:
        out.append((back.frame(back.fx_index(aura_t)), back.offset(), back.flags))
    glow = glow_for(look)
    if glow is not None and n < glow.total:
        out.append((glow.frame(n), glow.offset(), glow.flags))
    out.append((body.white(n) if flash else body.frame(n), off, 0))
    wsheet, _clip = weapon_for(weapon_kind)
    if wsheet is not None and n < wsheet.total:
        out.append((wsheet.frame(n), wsheet.offset(), 0))
    if front is not None:
        out.append((front.frame(front.fx_index(aura_t)), front.offset(), front.flags))
    return out


def _screen(view, wx: float, wy: float) -> tuple[int, int]:
    return view.to_screen(wx, wy)


def prop_drawable(o, view, t: float = 0.0):
    """(foot y, image, screen position) of a map object whose old sprite has a v2 prop (nature or
    building): the bottom-centre of the object's rect lands on the prop's pivot, the prop drawn
    at its native size. None: keep the old sprite."""
    name = o.props.get("sprite")
    pr = prop_for(name, int(o.props.get("variant", 0) or 0)) if (name and on()) else None
    if pr is None:
        return None
    sx, sy = _screen(view, o.x + o.w / 2, o.y + o.h)
    return (o.foot_y, pr.at(t), (int(sx - pr.pivot[0]), int(sy - pr.pivot[1])))


def npc_drawable(o, view, t: float = 0.0, talking: bool = False):
    """A map NPC on the v2 body (idle, `talk` while its dialog is open), feet on the bottom-centre
    of its map rect, facing down. None when that NPC has no v2 sheet yet."""
    s = npc(o.props.get("npc", "guide"))
    if s is None:
        return None
    clip = "talk" if talking and s.has("talk") else "idle"
    sx, sy = _screen(view, o.x + o.w / 2, o.y + o.h)
    n = s.index(clip, t + (int(o.x) % 7) * 0.11, o.props.get("facing", "down"))
    return (o.foot_y, s.frame(n), (int(sx - s.pivot[0]), int(sy - s.pivot[1])))


def object_drawable(o, view, t: float = 0.0, talking: bool = False):
    """A map object drawn from v2 art (prop, building or NPC), or None."""
    if o.type == "npc":
        return npc_drawable(o, view, t, talking)
    if o.props.get("sprite"):
        return prop_drawable(o, view, t)
    return None


def object_height(o, view) -> int:
    """How far above its feet (screen pixels) a map object's picture reaches, for markers."""
    if o.type == "npc":
        s = npc(o.props.get("npc", "guide"))
        if s is not None:
            return extent(s)[1]
    name = o.props.get("sprite")
    pr = prop_for(name, int(o.props.get("variant", 0) or 0)) if (name and on()) else None
    if pr is not None:
        return pr.pivot[1]
    return int(o.h * view.zoom)


def walker_drawables(realm: str | None, x: float, y: float, facing: str, moving: bool, walk_t: float, t: float,
                     weapon_kind: str | None, view) -> list | None:
    """A character that only walks and idles (the abode, menus) as y-sorted drawables
    [(y, image, position, blend flags)], or None without v2 art."""
    layers = char_layers(realm, "walk" if moving else "idle", walk_t if moving else t, facing, weapon_kind,
                         aura_t=t) if on() else None
    if layers is None:
        return None
    ix, iy = _screen(view, x, y)
    return [(y, img, (ix + ox, iy + oy), flags) for img, (ox, oy), flags in layers]


def beast_drawable(kind: str | None, x: float, y: float, moving: bool, walk_t: float, t: float, left: bool, view):
    """A Linh Thú following its owner, or None when its kind has no v2 beast."""
    b = beast_for(kind)
    if b is None:
        return None
    n = b.index("walk" if moving else "idle", walk_t if moving else t, "left" if left else "right")
    sx, sy = _screen(view, x, y)
    return (y, b.frame(n), (int(sx - b.pivot[0]), int(sy - b.pivot[1])))


def beast_picture(kind: str | None, t: float = 0.0, clip: str = "idle", facing: str = "down") -> pygame.Surface | None:
    """A Linh Thú for a menu: the frame cut to its pixels, or None when the kind has no v2 beast."""
    b = beast_for(kind)
    return trim(b.frame(b.index(clip, t, facing))) if b is not None else None


def monster_picture(sheet: Sheet | None, t: float = 0.0, clip: str = "idle", facing: str = "down"):
    """A monster for a menu (bestiary, level cards): the frame cut to its pixels, or None."""
    return trim(sheet.frame(sheet.index(clip, t, facing))) if sheet is not None else None
