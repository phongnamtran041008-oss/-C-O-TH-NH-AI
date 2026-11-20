"""Ngự kiếm on the client without a server (engine/flight.py): the altitude curves, the shadow, the
wake, a Flyer through take-off, cruise, landing and the fall, the drawing it composes, and the
flown step of the shared geometry (engine/glide.py, the server's copy: test_beast_units checks
the two files agree line for line)."""
from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402
import pytest  # noqa: E402

from client.engine import art2  # noqa: E402
from client.engine import flight as fl  # noqa: E402
from client.engine import glide as gl  # noqa: E402
from client.engine import movement as mv  # noqa: E402
from client.engine.view import View  # noqa: E402


def test_take_off_crouches_then_rises_to_the_height_with_a_small_overshoot():
    lift, crouch = 18.0, 0.25
    curve = [fl.takeoff_alt(i / 100, lift, crouch) for i in range(101)]
    assert min(curve[:25]) == pytest.approx(-fl.CROUCH_PX, abs=0.1), "the crouch sinks first"
    assert curve[0] == 0.0 and curve[-1] == pytest.approx(lift)
    assert max(curve) <= lift * 1.12 and max(curve) > lift, "a touch of overshoot, no more"
    rise = curve[30:70]
    assert all(b >= a - 1e-9 for a, b in zip(rise, rise[1:])), "then it climbs without a jerk"


def test_landing_and_fall_end_on_the_ground_and_the_hop_is_one_arc():
    assert fl.landing_alt(0, 30) == 30 and fl.landing_alt(1, 30) == 0
    land = [fl.landing_alt(i / 50, 30) for i in range(51)]
    assert all(b <= a + 1e-9 for a, b in zip(land, land[1:]))
    assert fl.fall_alt(1, 18) == 0 and all(fl.fall_alt(i / 50, 18) >= 0 for i in range(51))
    assert fl.hop_alt(0) == 0 and fl.hop_alt(1) == pytest.approx(0, abs=1e-9)
    assert fl.hop_alt(0.5) == pytest.approx(fl.HOP_LIFT)


def test_the_shadow_shrinks_and_fades_with_height_and_the_wake_needs_speed():
    s0, a0 = fl.shadow(0)
    s1, a1 = fl.shadow(18)
    s2, a2 = fl.shadow(30)
    assert s0 > s1 > s2 > 0.5 and a0 > a1 > a2 >= 0.7
    assert fl.wake(0, 111) == 0 and fl.wake(fl.WAKE_MIN - 1, 111) == 0
    assert 0 < fl.wake(40, 111) < fl.wake(111, 111) <= 1


def test_a_flyer_takes_off_cruises_lands_and_touches_down_once():
    f = fl.Flyer()
    assert f.alt(0) == 0 and not f.shown(0)
    f.take_off(10.0, 1, 18, 0.3)
    assert f.flying and f.shown(10.0)
    assert f.alt(10.05) < 0, "the crouch"
    assert f.alt(11.0) == pytest.approx(18, abs=fl.BOB_PX + 0.01) and f.kind == "cruise"
    f.land(12.0)
    assert not f.flying and f.shown(12.1) and 0 < f.alt(12.1) < 19.5
    assert not f.touched_down(12.2)
    assert f.touched_down(12.0 + fl.LAND_S + 0.01) and not f.touched_down(12.5), "the dust once"
    assert not f.shown(13) and f.alt(13) == 0
    f.hover(20.0, 2, 30)
    assert f.alt(20.0) == pytest.approx(30, abs=fl.BOB_PX + 0.01)
    f.land(21.0, fall=True)
    assert f.kind == "fall" and f.touched_down(21.0 + fl.FALL_S + 0.01)


def test_a_flyer_tracks_its_velocity_for_the_wake():
    f = fl.Flyer()
    for i in range(30):
        f.track(10 + i * 2.0, 50, i / 60)       # 120 px/s to the right
    assert f.vx == pytest.approx(120, rel=0.05) and abs(f.vy) < 1
    f.track(500, 50, 5.0)                       # a jump (a new zone): no streak of speed
    assert f.speed == 0


@pytest.fixture(scope="module")
def screen():
    pygame.init()
    pygame.display.set_mode((64, 64))
    yield


def test_compose_lifts_the_body_and_leaves_the_shadow_on_the_ground(screen):
    if not art2.on():
        pytest.skip("no v2 art in this checkout")
    v = View(2)
    shadows, body = fl.compose(v, "truc_co", 60, 60, "right", 0.2, None, "phi_kiem_1", 18.0)
    assert len(shadows) == 2 and body
    still = len(body)
    sh_y = shadows[0][1][1] + shadows[0][0].get_height() / 2
    assert sh_y > v.to_screen(60, 60)[1] - 8, "the shadow lies at the feet's ground point"
    assert body[-1][1][1] < shadows[0][1][1] - 18, "the body is drawn well above it"
    _, moving = fl.compose(v, "truc_co", 60, 60, "right", 0.2, None, "phi_kiem_1", 18.0, vx=111, top=111)
    assert len(moving) > still, "moving adds the wake and the wind"
    shadows_dark, _ = fl.compose(v, "truc_co", 60, 60, "right", 0.2, None, "phi_kiem_1", 18.0, dark=True)
    assert len(shadows_dark) == 3, "over ink and stone the sword's light marks the spot"


class Col:
    """A 64x64 map: the tile row 2 (y 32..48) is water, solid to walking; a wall at x 40..48 above it."""
    w, h = 64, 64

    def blocked_box(self, left, top, w, h):
        if left < 0 or top < 0 or left + w > 64 or top + h > 64:
            return True
        water = top < 48 and top + h > 32
        wall = left < 48 and left + w > 40 and top < 32
        return water or wall

    def blocked(self, x, y):
        return self.blocked_box(*mv.foot_box(x, y))


def tile(tx, ty):
    return "water" if ty == 2 else "grass"


def test_a_flown_step_crosses_water_a_walk_cannot_and_stops_at_a_wall():
    col, over = Col(), {"water"}
    x, y = 20.0, 60.0
    wx, wy = x, y
    for _ in range(30):
        wx, wy = mv.step(wx, wy, 0, -1, 10, 100, col)
    assert wy > 48, "walking stops at the water"
    fx_, fy_ = x, y
    for _ in range(60):
        fx_, fy_ = gl.fly_step(col, tile, over, fx_, fy_, 0, -1, 10, 100)
    assert fy_ < 30, "flying passes over it"
    assert gl.land_ok(col, tile, over, fx_, fy_) and not gl.land_ok(col, tile, over, 20, 40)
    sx, sy = 30.0, 20.0
    for _ in range(50):
        sx, sy = gl.fly_step(col, tile, over, sx, sy, 1, 0, 10, 100)
    assert sx <= 40 - 4, "the wall stops a flyer"
