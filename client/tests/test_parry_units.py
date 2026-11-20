"""The open-world rule on the client, without a server: hit-zone shapes (the polygon fallback
drawn when the v2 sheets are missing) and the wiring of the effects it uses."""
from __future__ import annotations

import math

import pygame

from client.engine import art2
from client.scenes import world as W


def test_an_old_tele_entry_is_a_circle():
    assert W.tele_shape([1, 2, 20, 0.5, 0.8, "m1"])["sh"] == "circle"
    shape = {"sh": "cone", "a": 90.0, "deg": 90.0, "w": 12.0}
    assert W.tele_shape([1, 2, 20, 0.5, 0.8, "m1", shape]) is shape


def test_cone_and_line_outlines_point_the_way_of_the_blow():
    cone = W.tele_points(100, 100, 30, {"sh": "cone", "a": 0.0, "deg": 90.0, "w": 0})
    assert cone[0] == (100, 100) and len(cone) == 10
    assert all(x >= 100 for x, _ in cone)                       # pointing right
    tip = max(math.hypot(x - 100, y - 100) for x, y in cone)
    assert abs(tip - 30) < 1e-6
    half = W.tele_points(100, 100, 30, {"sh": "cone", "a": 0.0, "deg": 90.0, "w": 0}, k=0.5)
    assert max(math.hypot(x - 100, y - 100) for x, y in half) < 16
    line = W.tele_points(100, 100, 40, {"sh": "line", "a": 90.0, "deg": 0, "w": 10.0})   # pointing down
    xs, ys = [p[0] for p in line], [p[1] for p in line]
    assert abs(max(xs) - min(xs) - 10) < 1e-6 and abs(max(ys) - 140) < 1e-6 and min(ys) > 99


def test_the_polygon_fallback_fills_the_zone_and_nothing_behind_it():
    surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    W.draw_tele_poly(surf, 100, 100, 50, {"sh": "cone", "a": 0.0, "deg": 60.0, "w": 0}, 1.0)
    assert surf.get_at((140, 100)).a > 0                        # in front, inside the fan
    assert surf.get_at((60, 100)).a == 0                        # behind the monster
    surf.fill((0, 0, 0, 0))
    W.draw_tele_poly(surf, 100, 100, 50, {"sh": "line", "a": 0.0, "deg": 0, "w": 8.0}, 0.5, outline_only=True)
    assert surf.get_bounding_rect().w > 40


def test_the_effects_of_the_rule_are_wired_or_fall_back():
    """Parry, guard break, the dash trail and the cone / line zones use v2 sheets that exist;
    a checkout without them draws plain shapes instead (combat_fx returns None)."""
    for name in ("parry", "guard_break", "dodge_trail", "telegraph_cone", "telegraph_cone_land",
                 "telegraph_line", "telegraph_line_land"):
        fid = art2.combat_fx(name)
        if art2.on():
            assert fid and art2.fx(fid) is not None, name
        else:
            assert fid is None
