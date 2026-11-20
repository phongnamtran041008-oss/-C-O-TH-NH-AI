"""Contact sheets of the combat VFX (client/engine/combat_vfx.py), rendered headless with no
server: the real Blender sheets, the real character and monster sheets, the real engine.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" tools/shot_vfx.py [out_dir]

writes into art/preview/ (3x nearest-neighbour, dark ground, labels):

    vfx_kiem_khi.png   a sword-wielder of each of the 10 tiers mid-swing, several moments per row
    vfx_weapons.png    the five weapon families at the four tier groups, at the moment of the blow
    vfx_chieu.png      each chiêu thức at charge / release / travel / impact, and its miss
    vfx_hits.png       crit, kill and dissolve, Phản Đòn, Né Đòn, stage-up, breakthrough
    vfx_roi_do.png     gear dropped by a monster: the hop out, lying in the five rarity colours on
                       grass, the name when near, the pickup; the weapon spots, open and locked
    vfx_kiem_khi_co.png  the kiếm khí sheet again on grass (bright ground washes additive light out)

Every cell is the world at the game's 2x zoom, cropped to the action; a monster's wind-up ring
is drawn under the player (with its bright rim over everything, as the game does) so you can
judge whether the effects ever hide a telegraph.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402

pygame.init()
pygame.display.set_mode((480, 270))

from client.art import skill_fx  # noqa: E402
from client.engine import art2  # noqa: E402
from client.engine import combat_vfx as C  # noqa: E402
from client.engine.text import Fonts  # noqa: E402
from client.engine.vfx import Vfx  # noqa: E402
from client.engine.view import View  # noqa: E402

SCALE = 3
BG = (24, 28, 27)
GRID = (30, 35, 33)
FONTS = Fonts()
TIERS = [("pham_nhan", 1, "Phàm Nhân"), ("luyen_khi", 5, "Luyện Khí 5"), ("luyen_khi", 8, "Luyện Khí 8"),
         ("truc_co", 1, "Trúc Cơ"), ("kim_dan", 1, "Kết Đan"), ("nguyen_anh", 1, "Nguyên Anh"),
         ("hoa_than", 1, "Hóa Thần"), ("luyen_hu", 1, "Luyện Hư"), ("hop_the", 1, "Hợp Thể"),
         ("dai_thua", 1, "Đại Thừa")]
MONSTER = "dau_tu_oa"
GRASS = os.environ.get("SHOT_GROUND") == "grass"


def text(s: str, size: int = 8, color="#E9E4D8") -> pygame.Surface:
    return FONTS.render(s, size, color, SCALE)


class Cell:
    """One 2x-world picture: an attacker at `src`, a monster at `dst` (world px), a VFX engine."""

    def __init__(self, w: int, h: int, src=(40.0, 40.0), dst=(64.0, 40.0)):
        self.w, self.h = w, h
        self.src, self.dst = src, dst
        self.view = View(2)
        self.view.ox, self.view.oy = 0, 0
        self.vfx = Vfx()
        self.vfx.resolve = lambda key: self.src if key == "me" else None
        self.tele = None
        self.loot = None          # a ground_loot.GroundLoot to draw, at loot_t
        self.loot_t = 0.0
        self.spots: list = []     # [draw(surf, view, ground)] weapon spots

    def run_to(self, t: float) -> None:
        while self.vfx.t + 1e-6 < t and self.vfx.wall < t + 0.5:
            self.vfx.update(1 / 120)

    def picture(self, realm: str, weapon: str | None, clip: str, clip_t: float, facing: str = "right",
                monster: bool = True, mon_clip: str = "idle", mon_t: float = 0.0, extra=None) -> pygame.Surface:
        surf = pygame.Surface((self.w, self.h))
        surf.fill(BG)
        ts = art2.tileset32() if GRASS else None
        if ts is not None:                    # the real grass of the world, as bright as the game's
            for ty in range(0, self.h, 32):
                for tx in range(0, self.w, 32):
                    surf.blit(ts.pick(0, tx // 32, ty // 32), (tx, ty))
        else:
            for x in range(0, self.w, 32):
                pygame.draw.line(surf, GRID, (x, 0), (x, self.h))
            for y in range(0, self.h, 32):
                pygame.draw.line(surf, GRID, (0, y), (self.w, y))
        v = self.view
        if self.loot is not None:
            self.loot.draw_ground(surf, v, self.loot_t, self.loot_t)
        for sp in self.spots:
            sp(surf, v, True)
        if self.tele is not None:
            self.draw_tele(surf, False)
        self.vfx.draw(surf, v, "ground")
        bodies = []
        layers = art2.char_layers(realm, clip, clip_t, facing, weapon, aura_t=clip_t)
        sx, sy = v.to_screen(*self.src)
        for img, (ox, oy), flags in layers or ():
            bodies.append((self.src[1], img, (sx + ox, sy + oy), flags))
        if self.loot is not None:
            for d in self.loot.drawables(v, self.loot_t, *self.src):
                bodies.append((d[0], d[1], d[2], 0))
        if monster:
            m = art2.monster(MONSTER)
            if m is not None:
                n = m.index(mon_clip, mon_t, "left")
                mx, my = v.to_screen(*self.dst)
                bodies.append((self.dst[1], m.frame(n), (int(mx - m.pivot[0]), int(my - m.pivot[1])), 0))
        for _y, img, pos, flags in sorted(bodies, key=lambda b: b[0]):
            surf.blit(img, pos, special_flags=flags)
        if self.loot is not None:
            self.loot.draw_over(surf, v, self.loot_t, self.loot_t)
        for sp in self.spots:
            sp(surf, v, False)
        if extra is not None:
            extra(surf, v)
        if self.tele is not None:
            self.draw_tele(surf, True)
        self.vfx.draw(surf, v, "over")
        self.vfx.draw_tint(surf)
        return surf

    def draw_tele(self, surf, over: bool) -> None:
        """The monster's wind-up ring under the player, as world.draw_teles_v2 draws it."""
        x, y, r, k = self.tele
        cx, cy = self.view.to_screen(x, y)
        rad = self.view.len(r + 5)
        if over:
            pygame.draw.circle(surf, (255, 214, 120), (cx, cy), int(rad), 1)
            return
        charge = art2.fx("warn_circle_charge")
        if charge is None:
            return
        d = max(8, int(2 * rad * charge.fw / 92))
        ring = art2.scaled(charge.frame(charge.fx_index(0.3)), d, d)
        surf.blit(art2.alpha_copy(ring, 150 + 105 * k), (int(cx - d / 2), int(cy - d / 2)))
        inner = int(d * k) // 4 * 4
        if inner >= 8:
            fill = art2.scaled(charge.frame(charge.fx_index(0.3)), inner, inner)
            surf.blit(art2.alpha_copy(fill, 190), (int(cx - inner / 2), int(cy - inner / 2)))


def sheet(rows: list[tuple[str, list[tuple[str, pygame.Surface]]]], title: str) -> pygame.Surface:
    """Rows of (label, [(caption, cell picture)]) laid out 3x with labels."""
    lw = 150
    cw = max(c.get_width() for _, cells in rows for _, c in cells) * SCALE
    ch = max(c.get_height() for _, cells in rows for _, c in cells) * SCALE
    cols = max(len(cells) for _, cells in rows)
    head = 34
    out = pygame.Surface((lw + cols * (cw + 4), head + len(rows) * (ch + 18)))
    out.fill((12, 13, 15))
    out.blit(text(title, 9), (8, 6))
    for r, (label, cells) in enumerate(rows):
        y = head + r * (ch + 18)
        out.blit(text(label, 8), (8, y + ch // 2 - 10))
        for c, (cap, pic) in enumerate(cells):
            x = lw + c * (cw + 4)
            out.blit(pygame.transform.scale(pic, (pic.get_width() * SCALE, pic.get_height() * SCALE)), (x, y))
            out.blit(text(cap, 6, "#A9A39A"), (x + 4, y + ch + 1))
    return out


def sword_of(t: int) -> str:
    return f"kiem_{max(1, min(8, (t * 8 + 9) // 10))}"


def kiem_khi_rows() -> list:
    rows = []
    for t_i, (realm, stage, name) in enumerate(TIERS, start=1):
        t = C.tier(realm, stage)
        assert t == t_i, (realm, stage, t)
        weapon = sword_of(t)
        strike = C.strike_delay(realm, weapon)
        moments = [strike - 0.03, strike + 0.03, strike + 0.08, strike + 0.14, strike + 0.22, strike + 0.36]
        cells = []
        for m in moments:
            cell = Cell(250, 110, src=(36.0, 40.0), dst=(62.0, 40.0))
            cell.tele = (36.0, 40.0, 16.0, 0.6)
            land = C.swing(cell.vfx, weapon, t, cell.src, cell.dst, strike=strike, dst_lift=11, follow="me")
            cell.run_to(m)
            pic = cell.picture(realm, weapon, "slash", m, mon_clip="hit" if m > land else "idle",
                               mon_t=max(0.0, m - land))
            cells.append((f"{m:.2f}s{' *' if abs(m - land) < 0.04 else ''}", pic))
        rows.append((f"T{t} {name}", cells))
    return rows


FAMILY_WEAPON = {"blade": "kiem", "thrust": "thuong", "smash": "chuy", "shot": "cung", "spell": "truong"}
FAMILY_NAME = {"blade": "Kiếm / Đao", "thrust": "Thương / Kích", "smash": "Chùy / Phủ", "shot": "Cung / Ám khí",
               "spell": "Trượng / Hồ lô"}
GROUP_TIER = {1: ("luyen_khi", 8), 2: ("kim_dan", 1), 3: ("hoa_than", 1), 4: ("dai_thua", 1)}


def weapon_rows() -> list:
    rows = []
    for fam, wtype in FAMILY_WEAPON.items():
        cells = []
        for g, (realm, stage) in GROUP_TIER.items():
            t = C.tier(realm, stage)
            weapon = f"{wtype}_{max(1, min(8, g * 2))}"
            clip = art2.weapon_for(weapon)[1]
            strike = C.strike_delay(realm, weapon)
            for label, when in (("blow", 0.06), ("land", None), ("after", 0.15)):
                cell = Cell(220, 100, src=(30.0, 36.0), dst=(70.0, 36.0) if fam in ("shot", "spell") else (56.0, 36.0))
                land = C.swing(cell.vfx, weapon, t, cell.src, cell.dst, strike=strike, dst_lift=11, follow="me")
                m = (strike + when if label == "blow" else land + when) if when is not None else land + 0.03
                cell.run_to(m)
                cells.append((f"g{g} T{t} {label}", cell.picture(realm, weapon, clip, m)))
        rows.append((FAMILY_NAME[fam], cells))
    return rows


CHIEU = [("chem", "Thường Quyền", "slash", 0.0), ("kiem_khi", "Phá Mê Kiếm Quyết", "slash", 0.0),
         ("hoa_cau", "Hỏa Cầu Thuật", "cast", 0.0), ("tran_do", "Ngũ Hành Trận", "cast", 80.0),
         ("ho_tran", "Hộ Thân Trận", "cast", 120.0), ("thien_loi", "Thiên Lôi Tuyệt Kỹ", "cast", 0.0)]


def chieu_rows(t: int = 5, realm: str = "kim_dan") -> list:
    rows = []
    for fx, name, clip, r in CHIEU:
        far = fx in ("hoa_cau", "tran_do", "thien_loi")
        src, dst = (34.0, 52.0), ((96.0, 52.0) if far else (66.0, 52.0))
        probe = Cell(300, 150, src, dst)
        land = C.chieu(probe.vfx, fx, src, None if fx == "ho_tran" else dst, t, radius=r, follow="me")
        charge = 0.1 if fx == "chem" else C.CHARGE[fx]
        moments = [("tụ lực", charge * 0.6), ("xuất chiêu", charge + 0.04), ("bay", (charge + land) / 2 + 0.02),
                   ("trúng", land + 0.05), ("dư âm", land + 0.4)]
        cells = []
        for cap, m in moments:
            cell = Cell(300, 150, src, dst)
            C.chieu(cell.vfx, fx, src, None if fx == "ho_tran" else dst, t, radius=r, follow="me")
            cell.run_to(m)
            cells.append((f"{cap} {m:.2f}s", cell.picture(realm, "kiem_4", clip, m, monster=fx != "ho_tran")))
        # the miss: the grey code-drawn fizzle, drawn at 1x and scaled up as the world does
        cell = Cell(300, 150, src, dst)
        C.fizzle(cell.vfx, fx, src, dst, follow="me")
        p = 0.35
        cell.run_to(p * skill_fx.duration(fx, False))

        def fizzle(surf, v, fx=fx, p=p, src=src, dst=dst, r=r):
            z = 2
            layer = pygame.Surface((surf.get_width() // z + 1, surf.get_height() // z + 1), pygame.SRCALPHA)
            skill_fx.draw(layer, fx, p, src, dst, ok=False, radius=r)
            surf.blit(pygame.transform.scale(layer, (layer.get_width() * z, layer.get_height() * z)), (0, 0))
        cells.append(("hụt", cell.picture(realm, "kiem_4", clip, 0.3, monster=fx != "ho_tran", extra=fizzle)))
        rows.append((name, cells))
    return rows


def hit_rows() -> list:
    rows = []
    realm, weapon = "kim_dan", "kiem_4"
    m = art2.monster(MONSTER)

    def body():
        n = m.index("die", 9.0, "left")
        return m.frame(n), m.white(n), m.pivot

    cells = []
    for when in (0.02, 0.08, 0.16):
        cell = Cell(200, 100)
        C.crit(cell.vfx, cell.dst[0], cell.dst[1], 11, True)
        cell.run_to(when)
        cells.append((f"bạo kích {when:.2f}s", cell.picture(realm, weapon, "slash", 0.3, mon_clip="hit", mon_t=when)))
    rows.append(("Bạo kích", cells))
    cells = []
    die_s = m.seconds("die") if m else 0.5
    for when in (0.05, 0.2, die_s + 0.05, die_s + 0.25, die_s + 0.45):
        cell = Cell(200, 100)
        C.death(cell.vfx, cell.dst[0], cell.dst[1], 11, body(), after=die_s, mine=True)
        cell.run_to(when)
        cells.append((f"hạ {when:.2f}s", cell.picture(realm, weapon, "idle", 0.3,
                                                       monster=when < die_s, mon_clip="die", mon_t=when)))
    rows.append(("Quái tan biến", cells))
    for t in (2, 6, 10):
        cells = []
        r_realm = {2: "luyen_khi", 6: "nguyen_anh", 10: "dai_thua"}[t]
        for when in (0.02, 0.1, 0.2, 0.32, 0.5):
            cell = Cell(220, 110, src=(40.0, 44.0), dst=(60.0, 44.0))
            cell.tele = (40.0, 44.0, 16.0, 1.0)
            C.parry(cell.vfx, cell.dst[0], cell.dst[1], cell.src[0], cell.src[1], t, sword_of(t), True)
            cell.run_to(when)
            cells.append((f"{when:.2f}s", cell.picture(r_realm, sword_of(t), "slash", 0.08 + when, mon_clip="hit",
                                                       mon_t=when)))
        rows.append((f"Phản Đòn T{t}", cells))
    cells = []
    for when in (0.02, 0.1, 0.2):
        cell = Cell(200, 100)
        C.dodge(cell.vfx, cell.src[0], cell.src[1], -1, 0)
        C.dodged(cell.vfx, cell.src[0] + 6, cell.src[1], True)
        cell.run_to(when)
        cells.append((f"né {when:.2f}s", cell.picture(realm, weapon, "dodge", when, facing="left")))
    rows.append(("Né Đòn", cells))
    cells = []
    for when in (0.1, 0.3, 0.5):
        cell = Cell(200, 110, src=(50.0, 46.0))
        C.stage_up(cell.vfx, cell.src[0], cell.src[1], follow="me")
        cell.run_to(when)
        cells.append((f"lên tầng {when:.2f}s", cell.picture(realm, weapon, "idle", when, monster=False)))
    for when in (0.2, 0.6, 0.85, 1.1):
        cell = Cell(200, 110, src=(50.0, 46.0))
        C.breakthrough(cell.vfx, cell.src[0], cell.src[1], follow="me")
        cell.run_to(when)
        cells.append((f"đột phá {when:.2f}s", cell.picture(realm, weapon, "meditate", when, monster=False)))
    rows.append(("Lên tầng / Đột phá", cells))
    return rows


def loot_rows() -> list:
    """Gear dropped where a monster died: the hop, the five rarities lying on the ground, the name
    tag when the player is near, the pickup; then the weapon spots of Thiên Địa Đồ."""
    from client.engine import ground_loot as G
    from client.engine.text import Fonts as _F  # noqa: F401
    rows = []
    items = [("pham", "kiem_1", "#7D7468"), ("linh", "dao_2", "#6A994E"), ("huyen", "thuong_3", "#4A7CC8"),
             ("dia", "cung_4", "#8E5AC8"), ("thien", "truong_6", "#C99A3A")]
    cells = []
    for r, item, col in items:
        cell = Cell(110, 100, src=(14.0, 44.0), dst=(30.0, 40.0))
        g = G.GroundLoot()
        g.add({"item": item, "name_vi": item, "rarity": r, "color": col, "x": 30.0, "y": 40.0}, 0.0, None)
        g.update(2.0, 900.0, 900.0, None)
        cell.loot, cell.loot_t = g, 2.0

        def tag(surf, v, r=r, col=col, item=item):
            sx, sy = v.to_screen(30.0, 40.0)
            img = FONTS.render(item, 7, col, 1)
            surf.blit(img, (int(sx - img.get_width() / 2), int(sy - 70)))
        cells.append((r, cell.picture("kim_dan", "kiem_4", "idle", 0.0, monster=False, extra=tag)))
    rows.append(("Năm phẩm trên cỏ", cells))
    cells = []
    for label, t, px in (("rơi ra", 0.35, 900.0), ("nằm", 1.2, 900.0), ("lại gần", 1.6, 44.0),
                         ("nhặt", 1.6 + 0.12, 34.0), ("vào túi", 1.6 + 0.26, 34.0)):
        cell = Cell(150, 100, src=(min(px, 120.0), 44.0), dst=(60.0, 40.0))
        g = G.GroundLoot()
        g.add({"item": "kiem_3", "name_vi": "Thanh Phong Kiếm", "rarity": "dia", "color": "#8E5AC8",
               "x": 60.0, "y": 44.0}, 0.0, None)
        if label != "rơi ra":
            g.update(1.0, 900.0, 900.0, None)
        if label in ("nhặt", "vào túi"):
            g.update(1.6, 62.0, 44.0, None)
        cell.loot, cell.loot_t = g, t
        cells.append((label, cell.picture("kim_dan", "kiem_4", "idle", 0.0, monster=label == "rơi ra",
                                          mon_clip="die", mon_t=0.5)))
    rows.append(("Rơi, nằm, nhặt", cells))
    from client.scenes import world as W
    cells = []
    for q, state in (("ha", "available"), ("trung", "available"), ("thuong", "available"), ("cuc", "available"),
                     ("tuyet", "available"), ("cuc", "locked")):
        cell = Cell(110, 100, src=(14.0, 44.0))
        sp = W.WeaponSpot(f"kiem_2_{q}", "x", 2, 2, state, icon=None)
        ws = W.WorldScene.__new__(W.WorldScene)
        ws.weapon_spots, ws.t = [sp], 1.0
        cell.spots = [ws.draw_spot_glow]
        icon = art2.weapon_icon("kiem_2")

        def ic(surf, v, sp=sp, icon=icon):
            if icon is not None:
                sx, sy = v.to_screen(sp.x, sp.y)
                img = icon if sp.state == "available" else art2.alpha_copy(icon, 120)
                surf.blit(img, (int(sx - img.get_width() / 2), int(sy - img.get_height() - 2)))
        cells.append((f"{q} {state}", cell.picture("kim_dan", "kiem_4", "idle", 0.0, monster=False, extra=ic)))
    rows.append(("Chỗ đặt binh khí", cells))
    return rows


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "art" / "preview"
    out.mkdir(parents=True, exist_ok=True)
    if not art2.on():
        print("no v2 art in this checkout: nothing to render")
        return 1
    only = os.environ.get("SHOT_ONLY")
    for name, rows, title in (("vfx_kiem_khi", kiem_khi_rows, "Kiếm khí theo tu vi (T1-T10), * = đòn chạm"),
                              ("vfx_weapons", weapon_rows, "Các loại binh khí theo nhóm cảnh giới"),
                              ("vfx_chieu", chieu_rows, "Chiêu thức (Kết Đan): tụ lực, xuất chiêu, bay, trúng, dư âm, hụt"),
                              ("vfx_hits", hit_rows, "Đòn trúng, hạ quái, Phản Đòn, Né Đòn, lên tầng, đột phá"),
                              ("vfx_roi_do", loot_rows, "Đồ rơi phát sáng theo phẩm (trên cỏ)"),
                              ("vfx_kiem_khi_co", kiem_khi_rows, "Kiếm khí trên cỏ (T1-T10)")):
        if only and only != name:
            continue
        global GRASS
        GRASS = name in ("vfx_roi_do", "vfx_kiem_khi_co") or os.environ.get("SHOT_GROUND") == "grass"
        img = sheet(rows(), title)
        p = out / f"{name}.png"
        pygame.image.save(img, str(p))
        print("saved", p, img.get_size())
    return 0


if __name__ == "__main__":
    sys.exit(main())
