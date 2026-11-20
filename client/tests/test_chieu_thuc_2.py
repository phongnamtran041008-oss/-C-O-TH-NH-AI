"""Chiêu Thức II on the client, with no server and no window: the recipes of the eleven new chiêu
and the hero sheets of the old six (pixel counts, which sheets, how many of them), what a
`mskill` event carries to them, the Công Pháp slot rules and the hotbar that reads the bar."""
from types import SimpleNamespace

import pygame
import pytest

from client.engine import art2
from client.engine import combat_vfx as C
from client.engine import vfx as V
from client.scenes import cong_phap as CP
from client.scenes import world as W
from client.tests.test_vfx import coverage

SRC, DST = (40.0, 60.0), (90.0, 60.0)
HITS = [DST, (115.0, 58.0), (140.0, 63.0)]
NEW = ("ngu_kiem", "van_kiem", "bang_phong", "loi_xich", "hoa_long", "dia_liet", "thanh_dang", "phong_nhan",
       "kim_chung", "kiem_vuc", "hoi_xuan")
SELF = ("kim_chung", "kiem_vuc", "hoi_xuan")

pytestmark = pytest.mark.skipif(not art2.on(), reason="no v2 art in this checkout")


def cast(fx: str, t: int = 5, ex: dict | None = None, r: float = 60.0) -> tuple[V.Vfx, float]:
    v = V.Vfx()
    v.resolve = lambda key: SRC if key == "me" else None
    ex = {"hits": HITS, "end": (160.0, 60.0), "d": 2.0} if ex is None else ex
    land = C.chieu(v, fx, SRC, None if fx in SELF else DST, t, radius=r, follow="me", ex=ex)
    return v, land


def spawned(v: V.Vfx, fid: str) -> int:
    return sum(1 for it in v.live if it.fid == fid)


@pytest.mark.parametrize("fx", C.RECIPES)
def test_every_chieu_lands_and_lights_the_screen(fx):
    v, land = cast(fx)
    assert 0 < land < 2.0, (fx, land)
    assert coverage(v, until=land + 0.3) > 3000, fx


@pytest.mark.parametrize("fx", NEW + ("chem", "kiem_khi", "hoa_cau", "tran_do", "ho_tran", "thien_loi"))
def test_the_charge_gathers_the_qi_of_the_element(fx):
    v, _land = cast(fx)
    assert spawned(v, f"tu_khi_{C.CHIEU_EL[fx]}") == 1, fx
    it = next(i for i in v.live if i.fid == f"tu_khi_{C.CHIEU_EL[fx]}")
    assert it.scale[0] == (1.0 if fx in C.TUYET_KY else 0.75)


def test_the_hero_sheets_replace_the_stand_ins_of_the_old_six():
    v, _ = cast("kiem_khi")
    assert spawned(v, "pha_me_kiem") == 1
    v, _ = cast("hoa_cau")
    assert spawned(v, "hoa_cau_lon") == 1 and spawned(v, "hoa_cau_no") == 1 and spawned(v, "bolt_hoa") == 0
    v, _ = cast("thien_loi")
    assert spawned(v, "thien_loi_giang") == 1


def test_the_flying_sword_pierces_each_monster_on_its_line_in_order():
    v, land = cast("ngu_kiem")
    rings = sorted((it for it in v.live if it.fid == "ngu_kiem_xuyen"), key=lambda it: it.t0)
    assert [(it.x, it.y) for it in rings] == HITS                  # nearest first: the sword meets them in order
    assert spawned(v, "ngu_kiem") == 2                              # out, and back
    assert land == pytest.approx(rings[0].t0)


def test_chain_lightning_draws_one_link_per_hop_and_a_strike_on_each():
    v, _ = cast("loi_xich")
    assert spawned(v, "loi_xich") == len(HITS) and spawned(v, "loi_cham") == len(HITS)
    links = sorted((it for it in v.live if it.fid == "loi_xich"), key=lambda it: it.t0)
    assert all(b.t0 > a.t0 for a, b in zip(links, links[1:]))      # one after the other
    # the second link starts on the first monster and is stretched to the second
    assert (links[1].x, links[1].y) == HITS[0]
    w = links[1].size[0]
    want = ((HITS[1][0] - HITS[0][0]) ** 2 + (HITS[1][1] - HITS[0][1]) ** 2) ** 0.5 * 2 * 96 / 89
    assert w == pytest.approx(want, rel=0.02)


def test_the_dragon_leaves_burning_ground_that_lasts_the_servers_strip():
    v, _ = cast("hoa_long", ex={"hits": HITS, "end": (180.0, 60.0), "d": 2.0})
    vet = [it for it in v.live if it.fid == "hoa_long_vet"]
    assert len(vet) == int((180.0 - 40.0) / 35)
    assert all(it.layer == "ground" and it.life == pytest.approx(2.3) for it in vet)
    left, _ = cast("hoa_long", ex={"hits": [(10.0, 60.0)], "end": (-100.0, 60.0), "d": 2.0}), None
    dragon = next(it for it in left[0].live if it.fid == "hoa_long")
    assert dragon.flip and abs(dragon.angle) < 1                    # mirrored, never upside down


def test_freeze_and_vines_hold_every_monster_struck_for_the_duration():
    for fx, hold_fid in (("bang_phong", "bang_ket"), ("thanh_dang", "thanh_dang_troi")):
        v, _ = cast(fx, ex={"hits": HITS, "d": 4.0})
        held = [it for it in v.live if it.fid == hold_fid]
        assert sorted((it.x, it.y) for it in held) == sorted(HITS), fx
        assert all(3.0 < it.life < 4.0 for it in held), fx


def test_the_bell_and_the_domain_follow_the_caster_for_their_duration():
    v, _ = cast("kim_chung", ex={"d": 6.0})
    tru = next(it for it in v.live if it.fid == "kim_chung_tru")
    assert tru.follow == "me" and 5.0 < tru.life <= 6.0
    v, _ = cast("kiem_vuc", ex={"d": 6.0}, r=60.0)
    ground = next(it for it in v.live if it.fid == "kiem_vuc")
    assert ground.layer == "ground" and ground.follow == "me" and ground.life == 6.0
    assert ground.scale[0] == pytest.approx(2.0)                    # its circle is the domain's reach (r 60)
    C.bell_block(v, *SRC, follow="me")
    assert spawned(v, "kim_chung_vang") == 1


def test_area_sigils_are_kept_under_the_size_of_the_screen():
    v, _ = cast("van_kiem", r=400.0)
    vong = next(it for it in v.live if it.fid == "van_kiem_vong")
    assert vong.scale[0] <= 1.4 * 1.1 and vong.layer == "ground" and vong.peak < 0.8


def test_tier_makes_a_chieu_bigger():
    for fx in NEW:
        lo, _ = cast(fx, t=1)
        hi, _ = cast(fx, t=10)
        assert coverage(hi, 1.0) >= coverage(lo, 1.0) * 0.98, fx


def test_a_miss_of_a_new_chieu_falls_on_its_target_or_on_the_caster():
    v = V.Vfx()
    C.fizzle(v, "hoi_xuan", SRC, DST)
    assert next(it for it in v.live if it.fid == "dust_step").x == pytest.approx(SRC[0])
    v = V.Vfx()
    C.fizzle(v, "ngu_kiem", SRC, DST)
    assert next(it for it in v.live if it.fid == "dust_step").x == pytest.approx((SRC[0] + DST[0]) / 2)


# ------------------------------------------------------------------ the event, the bar
def test_what_a_mskill_event_carries_to_the_recipe():
    ev = {"k": "mskill", "hits": [["m1", 10, 20], ["m2", 30.5, 40]], "ex": 99, "ey": 98, "d": 2}
    assert W.chieu_extra(ev) == {"hits": [(10.0, 20.0), (30.5, 40.0)], "end": (99.0, 98.0), "d": 2.0}
    assert W.chieu_extra({"k": "mskill"}) == {"hits": []}


def test_the_slot_rules_of_cong_phap():
    six = ["a", "b", None, "c", None, None]
    assert CP.assign(six, 2, "d") == ["a", "b", "d", "c", None, None]
    assert CP.assign(six, 4, "a") == [None, "b", None, "c", "a", None]      # a chiêu sits on one slot only
    assert CP.clear(six, 0) == [None, "b", None, "c", None, None]
    assert six == ["a", "b", None, "c", None, None]                          # pure


def fake_world(loadout):
    ws = W.WorldScene.__new__(W.WorldScene)
    ws.mskills = [{"id": k, "name_vi": k, "unlocked": True, "effect": e}
                  for k, e in (("a", "damage"), ("b", "heal"), ("c", "line"), ("d", "domain"))]
    ws.mskill_loadout = loadout
    return ws


def test_the_hotbar_reads_the_bar_and_targetless_chieu_need_no_monster():
    ws = fake_world(["c", None, "b", None, None, "d"])
    assert ws.slot_skill(0)["id"] == "c" and ws.slot_skill(1) is None and ws.slot_skill(5)["id"] == "d"
    sent, pushed = [], []
    ws.game = SimpleNamespace(now=1.0, state=SimpleNamespace(me={"id": 1}, character={}),
                              net=SimpleNamespace(send=sent.append), push=pushed.append)
    ws.mskill_ready, ws.dead = {}, False
    ws.player = SimpleNamespace(x=0.0, y=0.0, facing="down")
    ws.nearest_monster = lambda d: None
    ws.flush_inputs = lambda: None
    ws.fx = SimpleNamespace(float_text=lambda *a, **k: None)
    ws.cast_mskill(2, None)                      # Hồi Xuân style: no monster needed
    assert sent == [{"t": "mskill", "k": "b", "id": None}]
    ws.cast_mskill(0, None)                      # a line needs a monster: none near, nothing sent
    assert len(sent) == 1
    ws.cast_mskill(1, None)                      # an empty slot opens Công Pháp
    assert pushed and type(pushed[0]).__name__ == "CongPhapScene"


def test_a_saved_bar_is_applied_and_a_new_chieu_announced_once():
    ws = fake_world([])
    toasts = []
    ws.game = SimpleNamespace(toast=lambda text, *a, **k: toasts.append(text), state=SimpleNamespace(me={"id": 1}))
    ws.apply_mskills({"skills": ws.mskills, "loadout": ["d", "a", None, None, None, None],
                      "new": [{"id": "d", "name_vi": "Kiếm Vực"}]})
    assert ws.mskill_loadout == ["d", "a", None, None, None, None]
    assert toasts == ["Lĩnh ngộ chiêu mới: Kiếm Vực!"]


def test_the_cong_phap_card_places_a_learned_chieu_and_keeps_it_unique():
    ws = fake_world(["a", "b", None, None, None, None])
    ws.mskills.append({"id": "z", "name_vi": "z", "unlocked": False, "effect": "damage"})
    sc = CP.CongPhapScene(SimpleNamespace(), ws)
    assert sc.slots == ["a", "b", None, None, None, None]
    sc.pick = "c"
    sc.place(3)
    assert sc.slots == ["a", "b", None, "c", None, None] and sc.pick is None and sc.look == "c"
    sc.pick = "a"
    sc.place(5)
    assert sc.slots == [None, "b", None, "c", None, "a"]


def test_the_cong_phap_card_draws_without_a_window():
    """It draws with the real UI kit on a dummy display (the flow test clicks it for real)."""
    from client.engine.display import Display
    from client.engine.text import Fonts
    from client.ui.kit import UI
    pygame.init()
    d = Display(0, False, size=(960, 540))
    ui = UI(d, Fonts())
    ui.begin([], 1 / 60)
    ws = fake_world(["a", "b", None, None, None, None])
    sc = CP.CongPhapScene(SimpleNamespace(), ws)
    sc.draw_ui(ui)
    ui.end()
    for i in range(6):
        assert f"cp_slot_{i}" in ui.widgets
    assert all(f"cp_skill_{s['id']}" in ui.widgets for s in ws.mskills)
