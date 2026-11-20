"""The combat VFX layer (client/engine/vfx.py, client/engine/combat_vfx.py), with no server and no
window: kiếm khí tiers, weapon families, chiêu, the fallback chain to today's sheets and to the
sheets still being rendered, the budget, the shake, the hit-stop, and the world scene's use of
them (hits wait for the blade; a hit-stop never holds up input)."""
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

import pygame
import pytest

from client.engine import art2
from client.engine import combat_vfx as C
from client.engine import vfx as V
from client.engine.view import View

SRC, DST = (60.0, 60.0), (86.0, 60.0)


def coverage(v: V.Vfx, until: float = 1.2, step: float = 1 / 30) -> int:
    """Lit pixels summed over the life of what was spawned (both layers)."""
    view = View(2)
    total = 0
    while v.t < until:
        v.update(step)
        s = pygame.Surface((400, 240))
        v.draw(s, view, "ground")
        v.draw(s, view, "over")
        total += lit(s)
    return total


def _dark(s: pygame.Surface) -> int:
    raw = pygame.image.tobytes(s, "RGB")
    return sum(1 for i in range(0, len(raw), 3) if not (raw[i] or raw[i + 1] or raw[i + 2]))


def lit(s: pygame.Surface) -> int:
    return s.get_width() * s.get_height() - _dark(s)


# ------------------------------------------------------------------ who swings how hard
@pytest.mark.parametrize("realm,stage,want", [
    ("pham_nhan", 0, 1), ("luyen_khi", 1, 1), ("luyen_khi", 3, 1), ("luyen_khi", 4, 2), ("luyen_khi", 6, 2),
    ("luyen_khi", 7, 3), ("luyen_khi", 9, 3), ("truc_co", 2, 4), ("kim_dan", 1, 5), ("ket_dan", 1, 5),
    ("nguyen_anh", 1, 6), ("hoa_than", 1, 7), ("luyen_hu", 1, 8), ("hop_the", 1, 9), ("dai_thua", 9, 10),
    (None, None, 1), ("khong_co", 3, 1)])
def test_the_tier_ladder_is_the_contract(realm, stage, want):
    assert C.tier(realm, stage) == want


def test_tier_groups():
    assert [C.group(t) for t in range(1, 11)] == [1, 1, 1, 2, 2, 3, 3, 4, 4, 4]


@pytest.mark.parametrize("weapon,fam", [
    ("kiem_3", "blade"), ("dao_1", "blade"), ("roi_2", "blade"), ("sword", "blade"), (None, "blade"),
    ("thuong_4", "thrust"), ("kich_1", "thrust"), ("chuy_8", "smash"), ("phu_2", "smash"),
    ("cung_2", "shot"), ("am_khi_3", "shot"), ("luan_1", "shot"), ("ho_lo_5", "spell"), ("truong_1", "spell"),
    ("phien_2", "spell"), ("cam_7", "spell"), ("brush", "spell")])
def test_every_weapon_type_has_a_family(weapon, fam):
    assert C.family(weapon) == fam


def test_an_unknown_type_goes_by_the_clip_its_art_plays(monkeypatch):
    monkeypatch.setattr(art2, "weapon_for", lambda w: (None, "shoot"))
    assert C.family("song_tiet_con_3") == "shot"
    monkeypatch.setattr(art2, "weapon_for", lambda w: (None, "cast"))
    assert C.family("bao_kinh_1") == "spell"


def test_the_strike_comes_from_the_sheet_events():
    s = art2.char_for("truc_co")
    want = s.events["slash"]["hit"] / s.clips["slash"].fps
    assert C.strike_delay("truc_co", "kiem_2") == pytest.approx(want)


# ------------------------------------------------------------------ every tier, every family
@pytest.mark.parametrize("weapon", ["kiem_3", "thuong_3", "chuy_3", "cung_3", "truong_3"])
def test_every_tier_draws_and_a_higher_tier_draws_more(weapon):
    seen = []
    for t in range(1, 11):
        v = V.Vfx()
        land = C.swing(v, weapon, t, SRC, DST, strike=0.2, dst_lift=10)
        assert 0.2 <= land < 1.0, (weapon, t, land)
        seen.append(coverage(v))
    assert all(n > 0 for n in seen), seen
    assert all(b > a for a, b in zip(seen, seen[1:])), (weapon, seen)


def test_from_t2_a_wave_flies_on_past_the_target():
    for t in (1, 2, 5, 10):
        v = V.Vfx()
        C.swing(v, "kiem_3", t, SRC, DST, strike=0.2)
        moving = [it for it in v.live if it.to is not None]
        if t == 1:
            assert not moving
            continue
        assert moving, t
        assert max(it.to[0] for it in moving) > DST[0] + 5, t      # past the monster
    v = V.Vfx()
    C.swing(v, "kiem_3", 7, SRC, DST, strike=0.2)
    assert len({round(it.angle) for it in v.live if it.to is not None and it.fid != "sword_trail"}) == 3


def test_from_t4_a_scar_on_the_ground_and_only_your_own_blows_shake_your_camera():
    v = V.Vfx()
    C.swing(v, "kiem_3", 3, SRC, DST)
    assert not [it for it in v.live if it.layer == "ground"]
    v = V.Vfx()
    C.swing(v, "kiem_3", 4, SRC, DST, mine=True)
    assert [it for it in v.live if it.layer == "ground"]
    while v.t < 1.0:
        v.update(1 / 60)
        if v.trauma > 0:
            break
    assert v.trauma > 0
    v = V.Vfx()
    C.swing(v, "kiem_3", 10, SRC, DST, mine=False)
    for _ in range(80):
        v.update(1 / 60)
    assert v.trauma == 0 and not v.frozen


# ------------------------------------------------------------------ the fallback chain
def make_root(tmp: Path, extra: dict | None = None) -> Path:
    """An art root with today's FX sheets, plus fake new sheets ({new id: copied from id})."""
    src = art2.ROOT
    (tmp / "fx").mkdir(parents=True)
    for p in (src / "fx").iterdir():
        shutil.copy(p, tmp / "fx" / p.name)
    for new, old in (extra or {}).items():
        doc = json.loads((src / "fx" / f"{old}.json").read_text("utf-8"))
        doc["id"], doc["sheet"] = new, f"{new}.png"
        (tmp / "fx" / f"{new}.json").write_text(json.dumps(doc), "utf-8")
        shutil.copy(src / "fx" / f"{old}.png", tmp / "fx" / f"{new}.png")
    return tmp


@pytest.fixture
def art_root():
    yield
    art2.set_root(None)
    V.clear_cache()


def test_without_the_new_sheets_todays_sheets_stand_in(tmp_path, art_root):
    art2.set_root(make_root(tmp_path))
    assert V.pick([("kiem_khi_5", 1.0), ("slash_tho", 1.24)]) == ("slash_tho", 1.24)
    assert V.pick([("khong_co", 1.0)]) == (None, 0.0)
    v = V.Vfx()
    C.swing(v, "kiem_3", 6, SRC, DST)
    ids = {it.fid for it in v.live}
    assert not any(i.startswith(("kiem_khi_", "kiem_song_", "kiem_no_", "kiem_ngan_")) for i in ids)
    assert {"slash_thuy", "crack_ground"} <= ids


def test_the_new_sheets_light_up_when_they_arrive(tmp_path, art_root):
    new = {"kiem_khi_6": "slash_kim", "kiem_song_6": "sword_trail", "kiem_no_3": "hit_crit", "kiem_ngan_2": "crack_ground",
           "thuong_dam_2": "sword_trail", "chuy_chan_2": "crack_ground", "cung_ten_3": "bolt_kim",
           "phap_dan_4": "bolt_hoa", "uy_ap": "burst_tho"}
    art2.set_root(make_root(tmp_path, new))
    v = V.Vfx()
    C.swing(v, "kiem_3", 6, SRC, DST)
    ids = [it.fid for it in v.live]
    assert {"kiem_khi_6", "kiem_song_6", "kiem_no_3", "kiem_ngan_2"} <= set(ids)
    assert "slash_thuy" not in ids                       # the stand-in arc is gone
    arc = next(it for it in v.live if it.fid == "kiem_khi_6")
    assert arc.scale[1] == 1.0                           # drawn at the size the artist rendered
    for weapon, t, fid in (("thuong_1", 4, "thuong_dam_2"), ("chuy_1", 5, "chuy_chan_2"), ("cung_1", 7, "cung_ten_3"),
                           ("ho_lo_1", 9, "phap_dan_4"), ("chuy_1", 7, "uy_ap")):
        v = V.Vfx()
        C.swing(v, weapon, t, SRC, DST)
        assert fid in {it.fid for it in v.live}, (weapon, fid)
    assert coverage(v) > 0


def test_the_code_names_no_missing_sheet_in_wiring():
    """wiring.json may only name sheets on disk (test_art2); the new ids live in combat_vfx."""
    text = json.dumps(art2.wiring())
    for prefix in ("kiem_khi_", "kiem_song_", "kiem_no_", "kiem_ngan_", "thuong_dam_", "chuy_chan_", "cung_ten_",
                   "phap_dan_"):
        assert prefix not in text


def test_nothing_breaks_with_no_v2_art_at_all(tmp_path, art_root):
    art2.set_root(tmp_path)
    v = V.Vfx()
    assert C.swing(v, "kiem_3", 10, SRC, DST) > 0
    assert C.chieu(v, "thien_loi", SRC, DST, 10) > 0
    C.parry(v, *DST, *SRC, 5, "kiem_3", True)
    C.death(v, *DST, 10)
    assert not v.live
    coverage(v)


# ------------------------------------------------------------------ chiêu thức
FX = ("chem", "kiem_khi", "hoa_cau", "tran_do", "ho_tran", "thien_loi")


@pytest.mark.parametrize("fx", FX)
def test_every_chieu_has_a_whole_arc(fx):
    v = V.Vfx()
    land = C.chieu(v, fx, SRC, None if fx == "ho_tran" else (130.0, 60.0), 5, radius=60)
    assert 0.0 < land < 1.2
    view = View(2)
    frames = 0
    while v.t < land + 0.5:
        v.update(1 / 30)
        s = pygame.Surface((480, 270))
        v.draw(s, view, "ground")
        v.draw(s, view, "over")
        frames += lit(s) > 50
    assert frames >= int((land + 0.5) * 30 * 0.7), (fx, frames)


def test_each_chieu_looks_different_at_its_impact():
    shots = {}
    for fx in FX:
        v = V.Vfx()
        land = C.chieu(v, fx, SRC, None if fx == "ho_tran" else (130.0, 60.0), 5, radius=60)
        while v.t < land + 0.06:
            v.update(1 / 60)
        s = pygame.Surface((480, 270))
        v.draw(s, View(2), "ground")
        v.draw(s, View(2), "over")
        shots[fx] = pygame.image.tobytes(s, "RGB")
    assert len(set(shots.values())) == len(FX)


def test_a_chieu_grows_with_the_caster():
    for fx in ("kiem_khi", "thien_loi"):
        a, b = V.Vfx(), V.Vfx()
        C.chieu(a, fx, SRC, (130.0, 60.0), 1)
        C.chieu(b, fx, SRC, (130.0, 60.0), 9)
        assert coverage(b) > coverage(a), fx


def test_a_channel_loops_until_it_is_ended():
    v = V.Vfx()
    C.channel(v, "hoa_cau", "p1", *SRC, t=3)
    for _ in range(120):
        v.update(1 / 30)
    assert [it for it in v.live if it.tag == ("chan", "p1")]
    C.chieu(v, "hoa_cau", SRC, (130.0, 60.0), 3, charged=True, follow="p1")
    assert not [it for it in v.live if it.tag == ("chan", "p1")] and ("chan", "p1") not in v.emitters
    C.channel(v, "hoa_cau", "p1", *SRC)
    C.fizzle(v, "hoa_cau", SRC, (130.0, 60.0), follow="p1")
    assert ("chan", "p1") not in v.emitters


# ------------------------------------------------------------------ the engine: budget, shake, hit-stop
def test_the_instance_cap_holds_and_heavy_layers_go_first():
    v = V.Vfx()
    for i in range(600):
        v.spawn("hit_spark", i, 0, heavy=i % 2 == 0)
    assert len(v.live) == v.cap
    assert sum(1 for it in v.live if not it.heavy) == v.cap      # the light ones pushed the heavy out
    assert v.spawn("hit_spark", 0, 0, heavy=True) is None
    web = V.Vfx(web=True)
    for _ in range(300):
        web.spawn("hit_spark", 0, 0)
    assert len(web.live) == V.MAX_LIVE_WEB < V.MAX_LIVE


def test_the_transform_cache_is_bounded():
    v = V.Vfx()
    view = View(2)
    s = pygame.Surface((200, 200))
    for i in range(400):
        v.spawn("slash_kim", 50, 50, scale=0.5 + i * 0.01, angle=i * 7)
    v.update(0.05)
    v.draw(s, view)
    assert V.cache_size() <= V.CACHE_MAX


def test_reduce_effects_drops_shake_hitstop_and_the_heavy_layers():
    v = V.Vfx(reduced=True)
    v.shake(1.0)
    v.hitstop(0.1)
    assert v.offset() == (0, 0) and not v.frozen
    assert v.spawn("hit_spark", 0, 0, heavy=True) is None
    assert v.spawn("hit_spark", 0, 0, trail=(3, 0.02)).trail is None
    full, light = V.Vfx(), V.Vfx(reduced=True)
    C.swing(full, "kiem_3", 9, SRC, DST)
    C.swing(light, "kiem_3", 9, SRC, DST)
    assert 0 < len(light.live) < len(full.live)


def test_the_shake_kicks_and_dies_away():
    v = V.Vfx()
    v.shake(0.8)
    offs = []
    for _ in range(10):
        v.update(1 / 60)
        offs.append(v.offset())
    assert any(o != (0, 0) for o in offs)
    assert max(max(abs(a), abs(b)) for a, b in offs) <= V.SHAKE_PX
    for _ in range(120):
        v.update(1 / 60)
    assert v.offset() == (0, 0)


def test_a_hitstop_holds_the_picture_briefly_and_never_the_clock_of_the_game():
    v = V.Vfx()
    v.spawn("hit_spark", 0, 0)
    v.hitstop(5.0)                                  # asked for far too long: capped
    assert v.frozen and v.freeze_pending
    t0, wall0 = v.t, v.wall
    n = 0
    while v.frozen:
        v.update(1 / 60)
        n += 1
    assert v.t == t0                                # the effects held still...
    assert v.wall - wall0 <= V.HITSTOP_MAX + 1 / 60  # ...for a few frames of real time only
    v.hitstop(0.1)
    assert not v.frozen                             # not again straight away
    for _ in range(30):
        v.update(1 / 60)
    v.hitstop(0.1)
    assert v.frozen


def test_draw_layers_and_tags():
    v = V.Vfx()
    v.spawn("crack_ground", 50, 50, layer="ground", tag="a")
    v.spawn("hit_spark", 50, 50, tag="b")
    v.update(0.01)
    s = pygame.Surface((200, 200))
    assert v.draw(s, View(2), "ground") == 1 and v.draw(s, View(2), "over") == 1
    v.kill("a")
    assert v.draw(s, View(2), "ground") == 0
    v.clear()
    assert not v.live


# ------------------------------------------------------------------ the world scene
class FakeNet:
    def __init__(self):
        self.sent = []

    def send(self, m):
        self.sent.append(m)
        return True


def bare_world():
    from client.engine.effects import Effects
    from client.scenes.world import Ent, WorldScene
    ws = WorldScene.__new__(WorldScene)
    ws.game = SimpleNamespace(now=10.0, state=SimpleNamespace(me={"id": 7}, character={"realm": "hoa_than",
                                                                                      "realm_stage": 1},
                                                                cult={"stats": {"weapon": "kiem_3"}}),
                              scenes=[], cfg=SimpleNamespace(reduce_effects=False), net=FakeNet())
    ws.vfx = V.Vfx()
    ws.vfx_hold, ws.vfx_held, ws.vfx_late, ws.vfx_bodies = {}, {}, [], {}
    ws.vfx.resolve = ws.vfx_where
    ws.fx = Effects()
    ws.player = SimpleNamespace(x=60.0, y=60.0, facing="down")
    ws.entities = {"m1": Ent("m1", "m", "", mtype="x")}
    ws.entities["m1"].pos = (86.0, 60.0, 2, 0)
    ws.dead, ws.attack_ready, ws.taming = False, 0.0, {}
    ws.batch, ws.swing_t, ws.my_atk_t0 = [], 0.0, None
    ws.view = View(2)
    ws.seen = []
    ws.fx_event = lambda ev: ws.seen.append((ws.game.now, ev["k"]))
    return ws


def test_my_hits_wait_for_my_blade_and_then_show():
    ws = bare_world()
    ws.attack(ws.entities["m1"])
    assert ws.net.sent[-1] == {"t": "atk", "id": "m1"}
    land = ws.vfx_hold["p7"]
    assert land > ws.game.now
    ws.on_fx({"k": "hit", "id": "m1", "by": "p7", "v": 12, "x": 86.0, "y": 60.0})
    ws.on_fx({"k": "die", "id": "m1", "x": 86.0, "y": 60.0})
    ws.on_fx({"k": "hit", "id": "m1", "by": "m9", "v": 3})     # anyone else's: at once
    assert ws.seen == [(10.0, "hit")]
    ws.game.now = land + 0.02
    ws.vfx_release()
    assert [k for _, k in ws.seen] == ["hit", "hit", "die"]


def test_a_hit_never_waits_long():
    ws = bare_world()
    ws.vfx_hold["p7"] = ws.game.now + 30.0
    ws.on_fx({"k": "hit", "id": "m1", "by": "p7", "v": 1})
    ws.game.now += 0.61
    ws.vfx_release()
    assert ws.seen


def test_a_hitstop_never_holds_up_input_or_the_question():
    ws = bare_world()
    ws.vfx.hitstop(0.1)
    assert ws.vfx.frozen
    ws.attack(ws.entities["m1"])                        # the key still acts at once
    assert ws.net.sent == [{"t": "atk", "id": "m1"}]
    # the world's picture holds (draw_world blits the kept frame) but nothing else is gated on it
    drawn = []
    ws.draw_world_now = lambda surf: drawn.append("world")
    surf = pygame.Surface((48, 27))
    ws.frozen = None
    ws.draw_world(surf)                                 # the first frame is drawn and kept
    assert drawn == ["world"] and ws.frozen is not None
    ws.draw_world(surf)
    assert drawn == ["world"]                           # held
    ws.vfx.update(0.2)
    ws.draw_world(surf)
    assert drawn == ["world", "world"]                  # and it lets go


def test_reduce_effects_in_the_settings_reaches_the_world():
    ws = bare_world()
    ws._shake_seen = 0.0
    ws.game.cfg.reduce_effects = True
    ws.update_vfx(0.016)
    assert ws.vfx.reduced
    ws.vfx.shake(1.0)
    assert ws.vfx.offset() == (0, 0)


def test_a_kill_number_is_restyled_and_numbers_scale():
    from client.engine.effects import STYLES, Effects
    fx = Effects()
    fx.float_text("12", 50, 40, "#FFFFFF", style="hit")
    assert fx.restyle(50, "kill") and fx.texts[-1].style == "kill"
    sizes = {}
    for style in ("hit", "crit", "kill", "parry"):
        surf = pygame.Surface((200, 100), pygame.SRCALPHA)
        e = Effects()
        e.float_text("88", 100, 60, "#FFFFFF", style=style)
        e.texts[0].age = 0.02
        e.draw(surf, (0, 0), lambda t, c, size=7: pygame.font.Font(None, size * 3).render(t, False, c), 0)
        sizes[style] = surf.get_bounding_rect().w
    assert sizes["hit"] < sizes["crit"] < sizes["kill"] < sizes["parry"], sizes
    assert set(STYLES) >= {"hit", "crit", "kill", "parry", "dodge", "miss"}
