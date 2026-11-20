"""The client side of the weapons of Thiên Địa Đồ, without a server: the spots read from
GET /weapons, the reach the auto-target uses for each weapon type, and the code-drawn
picture of each type when the v2 art is off (the real pickup: test_lands_flow.test_weapon_spot_flow)."""
from __future__ import annotations

import json

import pygame

from client.scenes import world as W
from client.tests.driver import ROOT


def plan() -> dict:
    return json.loads((ROOT / "server" / "data" / "math" / "world_plan.json").read_text("utf-8"))


def test_the_reach_of_every_weapon_type_agrees_with_the_server():
    types = {t["id"]: t for t in plan()["weapon_types"]}
    assert W.PLAN_WEAPON_RANGE == {k: t["range"] for k, t in types.items()}
    assert set(W.PLAN_WEAPON_LOOK) == set(types)
    assert W.plan_weapon_type("kiem_3") == "kiem" and W.plan_weapon_type("ho_lo_1") == "ho_lo"
    assert W.plan_weapon_type("sword") is None and W.plan_weapon_type(None) is None
    assert W.plan_weapon_type("nothing_2") is None


def test_the_auto_target_uses_the_weapon_in_hand():
    class G:
        class state:
            cult = {"stats": {"weapon": "cung_1"}}
    scene = W.WorldScene.__new__(W.WorldScene)
    scene.game = G
    assert scene.weapon_range() == 60.0
    G.state.cult = {"stats": {"weapon": "chuy_2"}}
    assert scene.weapon_range() == 24.0
    G.state.cult = {"stats": {"weapon": "brush"}}
    assert scene.weapon_range() == 40
    G.state.cult = {"stats": {}}
    assert scene.weapon_range() == 22


def test_without_the_v2_art_a_plan_weapon_is_not_drawn_as_a_brush():
    pygame.init()
    brush = pygame.image.tobytes(W.weapon_img("brush", "down", 0.0), "RGBA")
    pics = {}
    for t in W.PLAN_WEAPON_RANGE:
        img = W.weapon_img(f"{t}_1", "down", 0.0)
        assert img.get_width() > 0
        pics[t] = pygame.image.tobytes(img, "RGBA")
        assert pics[t] != brush, t
    assert pics["kiem"] == pygame.image.tobytes(W.weapon_img("sword", "down", 0.0), "RGBA")
    assert len({pics[t] for t in ("cung", "ho_lo", "chuy", "thuong", "dao")}) == 5


def test_the_spots_come_from_the_placed_list_of_get_weapons():
    answer = {"weapons": [{"id": 9, "item_id": "kiem_1"}], "equipped": None, "placed": [
        {"id": "kiem_1_ha", "weapon": "kiem_1", "quality": "ha", "land": "kiem_trung_son", "pos": [25, 41],
         "state": "locked", "reason_vi": "Cần Luyện Khí tầng 1 trên Đạo Thụ.", "name_vi": "Kiếm Gỗ"},
        {"id": "kiem_1_trung", "land": "kiem_trung_son", "pos": [4, 18], "state": "taken"},
        {"id": "dao_1_ha", "land": "luu_van_coc", "pos": [25, 7], "state": "available"},
        {"id": "hong", "land": "kiem_trung_son", "pos": "a"},
    ]}
    spots = W.weapon_spots_from(answer, "kiem_trung_son")
    assert [s.id for s in spots] == ["kiem_1_ha", "kiem_1_trung"]
    s = spots[0]
    assert (s.tx, s.ty, s.state, s.name_vi) == (25, 41, "locked", "Kiếm Gỗ")
    assert (s.x, s.y) == (25 * 16 + 8, 41 * 16 + 12)
    assert W.weapon_spots_from({"weapons": []}, "kiem_trung_son") == []        # an older answer: nothing
    assert W.weapon_spots_from(None, "kiem_trung_son") == [] and W.weapon_spots_from(answer, None) == []
