"""M9 on the client, with no server and no window: the effects of the six chiêu thức and the
two new answer inputs (matching, ordering) of the math card."""
import json
from pathlib import Path
from types import SimpleNamespace

import pygame
import pytest

from client.art import skill_fx as F
from client.engine.display import Display
from client.engine.text import Fonts
from client.ui import mathinputs as MI
from client.ui.kit import UI

ROOT = Path(__file__).resolve().parents[2]
SRC, DST = (30.0, 150.0), (210.0, 150.0)
SIZE = (260, 190)


def paint(fx: str, p: float, ok: bool = True, dst=DST, radius: float = 0.0) -> pygame.Surface:
    surf = pygame.Surface(SIZE, pygame.SRCALPHA)
    F.draw(surf, fx, p, SRC, dst, ok=ok, radius=radius)
    return surf


def pixels(surf: pygame.Surface) -> list[tuple[int, int, int, int]]:
    w, h = surf.get_size()
    return [surf.get_at((x, y)) for y in range(h) for x in range(w) if surf.get_at((x, y)).a > 0]


def centroid_x(surf: pygame.Surface) -> float:
    w, h = surf.get_size()
    xs = [x for y in range(h) for x in range(w) if surf.get_at((x, y)).a > 40]
    return sum(xs) / len(xs)


def colourfulness(surf: pygame.Surface) -> float:
    """How far from grey the picture is: mean of (max - min) over its visible pixels."""
    px = pixels(surf)
    return sum(max(c.r, c.g, c.b) - min(c.r, c.g, c.b) for c in px) / max(1, len(px))


# ------------------------------------------------------------------ effects
def test_the_effect_ids_are_exactly_the_contract():
    """The six of M9 and the eleven of Chiêu Thức II (named after their Blender sheets)."""
    assert F.FX_IDS == ("chem", "kiem_khi", "hoa_cau", "tran_do", "ho_tran", "thien_loi",
                        "ngu_kiem", "van_kiem", "bang_phong", "loi_xich", "hoa_long", "dia_liet", "thanh_dang",
                        "phong_nhan", "kim_chung", "kiem_vuc", "hoi_xuan")


@pytest.mark.parametrize("fx", F.FX_IDS)
@pytest.mark.parametrize("ok", [True, False])
def test_every_effect_draws_something_through_its_whole_life(fx, ok):
    """Alive at every moment of its duration, so nothing is invisible half way."""
    seen = 0
    for i in range(1, 20):
        if pixels(paint(fx, i / 20, ok)):
            seen += 1
    assert seen >= 12, (fx, ok, seen)
    assert F.duration(fx, ok) > 0


@pytest.mark.parametrize("fx", F.FX_IDS)
def test_outside_its_life_nothing_is_drawn_and_nothing_raises(fx):
    surf = pygame.Surface(SIZE, pygame.SRCALPHA)
    assert F.draw(surf, fx, -0.1, SRC, DST) is False
    assert F.draw(surf, fx, 1.1, SRC, DST) is False
    assert not pixels(surf)
    assert F.draw(surf, fx, 0.0, SRC, DST) is True and F.draw(surf, fx, 1.0, SRC, DST) is True


def test_unknown_effect_and_missing_target_never_crash():
    surf = pygame.Surface(SIZE, pygame.SRCALPHA)
    assert F.draw(surf, "khong_co", 0.4, SRC, DST)
    assert F.draw(surf, "hoa_cau", 0.4, SRC, None)            # a chiêu with no target
    assert F.draw(surf, "ho_tran", 0.5, SRC, None, radius=500)  # an absurd radius is clamped, not a crash
    assert F.draw(surf, "tran_do", 0.5, SRC, DST, ok=False, radius=0)


def test_effects_are_pure_functions_of_the_moment():
    for fx in F.FX_IDS:
        a, b = paint(fx, 0.37), paint(fx, 0.37)
        assert pygame.image.tobytes(a, "RGBA") == pygame.image.tobytes(b, "RGBA"), fx


def test_each_effect_looks_different_from_every_other():
    shots = {fx: pygame.image.tobytes(paint(fx, 0.5), "RGBA") for fx in F.FX_IDS}
    assert len(set(shots.values())) == len(F.FX_IDS)
    miss = {fx: pygame.image.tobytes(paint(fx, 0.5, ok=False), "RGBA") for fx in F.FX_IDS}
    assert len(set(miss.values())) == len(F.FX_IDS)
    for fx in F.FX_IDS:
        assert shots[fx] != miss[fx], f"{fx}: a miss must not look like a hit"


@pytest.mark.parametrize("fx", F.FX_IDS)
def test_a_miss_is_grey_and_a_hit_has_colour(fx):
    """The fizzle reads as one at a glance because it has lost its colour."""
    hit = max(colourfulness(paint(fx, i / 10)) for i in range(1, 10))
    miss = max(colourfulness(paint(fx, i / 10, ok=False)) for i in range(1, 10))
    assert miss < 6, (fx, miss)
    assert hit > miss + 12, (fx, hit, miss)


@pytest.mark.parametrize("fx", ["kiem_khi", "hoa_cau"])
def test_a_flying_effect_travels_from_the_caster_to_the_target(fx):
    xs = [centroid_x(paint(fx, p)) for p in (0.1, 0.25, 0.4, 0.55)]
    assert xs == sorted(xs) and xs[-1] - xs[0] > 60, xs
    assert xs[0] < (SRC[0] + DST[0]) / 2 < xs[-1]


def test_the_fireball_bursts_where_the_target_is():
    after = paint("hoa_cau", 0.75)
    assert abs(centroid_x(after) - DST[0]) < 6
    assert abs(centroid_x(paint("chem", 0.5)) - DST[0]) < 25         # the slash is on the target


def test_the_array_surrounds_the_target_and_the_ward_surrounds_the_caster():
    arr = paint("tran_do", 0.5, radius=60)
    ward = paint("ho_tran", 0.5, radius=40)
    assert abs(centroid_x(arr) - DST[0]) < 8
    assert abs(centroid_x(ward) - SRC[0]) < 8
    w, _h = SIZE
    xs = [x for x in range(w) for y in range(SIZE[1]) if arr.get_at((x, y)).a > 40]
    assert max(xs) - min(xs) >= 100                                    # roughly the radius it was told
    # the array has all five element colours in its marks
    cols = {(c.r, c.g, c.b) for c in pixels(arr) if c.a > 200}
    for five in F.FIVE:
        assert any(abs(c[0] - five[0]) + abs(c[1] - five[1]) + abs(c[2] - five[2]) < 30 for c in cols), five


def test_lightning_comes_from_above_the_target():
    surf = paint("thien_loi", 0.35)
    ys = [y for y in range(SIZE[1]) for x in range(SIZE[0]) if surf.get_at((x, y)).a > 200]
    assert min(ys) < DST[1] - 80 and max(ys) <= DST[1]


def test_every_chieu_in_the_data_names_a_real_effect_and_a_real_icon():
    """A chiêu's slot shows an icon rendered from a 3D model (art/models/), never a Chinese
    character: every chiêu names one that is in the sheet, and no two chiêu share a picture."""
    from client.engine import icons
    skills = json.loads((ROOT / "server" / "data" / "math" / "skills.json").read_text("utf-8"))["skills"]
    index = json.loads((icons.ICON_DIR / "items.json").read_text("utf-8"))["icons"]
    assert len(skills) >= 5
    seen = set()
    for sid, s in skills.items():
        assert s["fx"] in F.FX_IDS, (sid, s["fx"])
        picture = (s["icon"], s.get("icon_variant", 0))
        assert len(index.get(picture[0], [])) > picture[1], (sid, picture)
        assert picture not in seen, f"{sid} shares the icon {picture} with another chiêu"
        seen.add(picture)
        assert icons.icon(*picture) is not None, (sid, picture)


def has_cjk(text: str) -> bool:
    return any("\u2e80" <= ch <= "\u9fff" or "\uf900" <= ch <= "\ufaff" for ch in text)


def test_the_hotbar_shows_no_chinese_with_or_without_the_icon_sheet(monkeypatch):
    """With the sheet a slot draws the icon; without it, the initials of the Vietnamese name."""
    from client.engine import icons
    from client.scenes import world
    assert world.MSKILL_KEY_NAMES == "123456" and len(world.MSKILL_KEYS) == 6
    skills = json.loads((ROOT / "server" / "data" / "math" / "skills.json").read_text("utf-8"))["skills"]
    for sid, s in skills.items():
        short = world.mskill_initials(s["name_vi"])
        assert 1 <= len(short) <= 2 and not has_cjk(short), (sid, short)
        assert not has_cjk(s["name_vi"] + s["desc_vi"] + s["kind_vi"]), sid

    drawn = []
    ui = SimpleNamespace(image=lambda *a, **k: drawn.append("image"),
                         text=lambda text, *a, **k: drawn.append(text))
    ws = world.WorldScene.__new__(world.WorldScene)
    sk = {"name_vi": "Hỏa Cầu Thuật", "icon": "quat"}
    ws.draw_mskill_icon(ui, sk, 0, 0, locked=False)
    assert drawn == ["image"]
    monkeypatch.setattr(icons, "icon", lambda name, variant=0: None)       # a checkout with no sheet
    ws.draw_mskill_icon(ui, sk, 0, 0, locked=False)
    assert drawn == ["image", "HC"]


def test_the_interface_no_longer_names_the_old_word_skills():
    import client.strings_vi as T
    for name in ("ATTACK_HINT", "SKILLS_TITLE", "SKILL_LOCKED"):
        assert "Pháp Chữ" not in getattr(T, name), name
    assert all("Pháp Chữ" not in text for text in T.SKILL_FAIL.values())
    assert not hasattr(T, "SKILL_EMPTY")


# ------------------------------------------------------------------ matching and ordering: state
def test_matching_pairs_repairs_and_sends_only_when_complete():
    st = MI.MatchingState(3)
    assert not st.complete
    st.pick_left(0)
    st.pick_right(2)
    assert st.pairs == [2, None, None] and st.sel is None
    st.pick_left(1)
    st.pick_right(2)                          # right 2 moves from left 0 to left 1
    assert st.pairs == [None, 2, None]
    st.pick_left(0)
    st.pick_right(0)
    st.pick_left(2)
    st.pick_right(1)
    assert st.complete and st.answer() == {"pairs": [0, 2, 1]}
    st.pick_left(0)
    st.pick_right(1)                          # re-pairing an already paired left item
    assert st.pairs == [1, 2, None] and not st.complete


def test_matching_undo_clear_and_picking_a_paired_right_item_up_again():
    st = MI.MatchingState(3)
    for k, j in ((0, 1), (1, 0), (2, 2)):
        st.pick_left(k)
        st.pick_right(j)
    st.undo()
    assert st.pairs == [1, 0, None]
    st.pick_right(1)                          # pick the item of left 0 up to move it
    assert st.sel == 0
    st.pick_right(2)
    assert st.pairs == [2, 0, None]
    st.pick_left(1)
    st.pick_left(1)                           # selecting the same left again drops the selection
    assert st.sel is None
    st.clear()
    assert st.pairs == [None] * 3 and not st.complete


def test_ordering_numbers_steps_by_click_and_takes_them_back():
    st = MI.OrderingState(4)
    for i in (2, 0, 3):
        st.click(i)
    assert st.order == [2, 0, 3] and st.number_of(0) == 2 and st.number_of(1) is None and not st.complete
    st.click(0)                               # a numbered step clicked again goes back
    assert st.order == [2, 3]
    st.click(1)
    st.click(0)
    assert st.complete and st.answer() == {"order": [2, 3, 1, 0]}
    st.undo()
    assert st.order == [2, 3, 1]
    st.clear()
    assert st.order == [] and st.answer() == {"order": []}
    st.click(9)                               # out of range is ignored
    assert st.order == []


def test_what_the_reveal_shows_of_the_answer_and_the_players_choice():
    assert MI.answer_lines("matching", "a — x; b — y; c — z") == ["a — x", "b — y", "c — z"]
    assert MI.answer_lines("ordering", "1. Đặt ẩn  2. Giải phương trình  3. Kiểm tra nghiệm") == \
        ["1. Đặt ẩn", "2. Giải phương trình", "3. Kiểm tra nghiệm"]
    assert MI.given_text("matching", {"pairs": [1, 0, 2]}) == "1-B, 2-A, 3-C"
    assert MI.given_text("ordering", {"order": [2, 0, 1]}) == "C, A, B"


# ------------------------------------------------------------------ matching and ordering: drawing
def make_ui() -> UI:
    return UI(Display(0, False, size=(960, 540)), Fonts())


def frame(ui: UI, draw, click: str | None = None, keys=()):
    """One frame of a widget; `click` names a widget (from the previous frame) to click."""
    events = [pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="", scancode=0) for k in keys]
    if click:
        pos = ui.widgets[click].center
        events += [pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos)]
    ui.begin(events, 0.016)
    return draw()


LEFT = ["Hai ma trận cùng cỡ", "Ma trận vuông", "Ma trận chuyển vị", "Ma trận đơn vị", "Ma trận không"]
RIGHT = ["có thể cộng với nhau", "số hàng bằng số cột", "đổi hàng thành cột", "đường chéo toàn số 1", "mọi phần tử bằng 0"]
STEPS = ["Đặt ẩn phụ để đưa về phương trình bậc hai",
         "Giải phương trình bậc hai theo ẩn phụ",
         "Đối chiếu điều kiện của ẩn phụ rồi quay lại ẩn ban đầu",
         "Thử lại các nghiệm vào phương trình đã cho"]
LONG = ["Phân tích đa thức ở tử số và ở mẫu số thành nhân tử rồi rút gọn các nhân tử chung của hai vế " * 2] * 6


def test_matching_widget_is_usable_with_the_mouse():
    ui = make_ui()
    st = MI.MatchingState(5)
    box = (24, 60, 432, 190)

    def draw():
        return MI.draw_matching(ui, st, LEFT, RIGHT, *box[:3], box[1] + box[3], False)

    frame(ui, draw)
    assert frame(ui, draw) is None
    for k in range(5):
        frame(ui, draw, click=f"match_l_{k}")
        frame(ui, draw, click=f"match_r_{(k + 1) % 5}")
    assert st.pairs == [1, 2, 3, 4, 0]
    ans = frame(ui, draw, click="mq_submit")
    assert ans == {"pairs": [1, 2, 3, 4, 0]}


def test_matching_widget_keys_and_submit_needs_every_pair():
    ui = make_ui()
    st = MI.MatchingState(3)

    def draw(sent=False):
        return MI.draw_matching(ui, st, LEFT[:3], RIGHT[:3], 24, 60, 432, 250, sent)

    frame(ui, draw)
    frame(ui, draw, keys=[pygame.K_1])
    frame(ui, draw, keys=[pygame.K_c])
    assert st.pairs == [2, None, None]
    assert frame(ui, draw, keys=[pygame.K_RETURN]) is None            # not complete: Enter does nothing
    frame(ui, draw, keys=[pygame.K_2])
    frame(ui, draw, keys=[pygame.K_a])
    frame(ui, draw, keys=[pygame.K_3])
    frame(ui, draw, keys=[pygame.K_b])
    assert frame(ui, draw, keys=[pygame.K_RETURN]) == {"pairs": [2, 0, 1]}
    frame(ui, draw, keys=[pygame.K_BACKSPACE])
    assert st.pairs == [2, 0, None]
    assert frame(ui, lambda: draw(sent=True), keys=[pygame.K_RETURN]) is None   # nothing after it was sent


def test_ordering_widget_numbers_clicks_and_sends_the_order():
    ui = make_ui()
    st = MI.OrderingState(4)

    def draw(sent=False):
        return MI.draw_ordering(ui, st, STEPS, 24, 60, 432, 250, sent)

    frame(ui, draw)
    assert frame(ui, draw, click="mq_submit") is None                 # disabled until all are numbered
    for i in (1, 0, 3, 2):
        frame(ui, draw, click=f"ord_step_{i}")
    assert st.order == [1, 0, 3, 2]
    frame(ui, draw, click="mq_undo")
    frame(ui, draw, keys=[pygame.K_c])                                # key C = the third step again
    assert st.order == [1, 0, 3, 2]
    assert frame(ui, draw, click="mq_submit") == {"order": [1, 0, 3, 2]}
    frame(ui, draw, click="mq_clear")
    assert st.order == []


@pytest.mark.parametrize("texts,kind", [(LONG[:5], "match"), (LONG[:6], "order"), (STEPS, "order"), (LEFT, "match")])
def test_long_vietnamese_text_stays_inside_the_card_and_clear_of_the_buttons(texts, kind):
    ui = make_ui()
    x, y, w, bottom = 24, 62, 432, 186                       # the compact combat card leaves this much
    if kind == "match":
        st = MI.MatchingState(len(texts))
        draw = lambda: MI.draw_matching(ui, st, texts, texts[::-1], x, y, w, bottom, False)
    else:
        st = MI.OrderingState(len(texts))
        draw = lambda: MI.draw_ordering(ui, st, texts, x, y, w, bottom, False)
    frame(ui, draw)
    area = ui.rect(x, y, w, bottom - y)
    items = [r for wid, r in ui.widgets.items() if wid.startswith(("match_", "ord_step_"))]
    assert len(items) == len(texts) * (2 if kind == "match" else 1)
    for r in items:
        assert area.contains(r), (r, area)
    buttons_top = min(r.top for wid, r in ui.widgets.items() if wid.startswith("mq_"))
    assert max(r.bottom for r in items) <= buttons_top, "the items run into the buttons"
    for a in items:                                          # and the rows never overlap
        for b in items:
            if a is not b and (a.x == b.x):
                assert not a.colliderect(b), (a, b)


# ------------------------------------------------------------------ the card around them
class FakeApi:
    def __init__(self):
        self.posts = []

    def post(self, path, body, ok, err):
        self.posts.append((path, body))


def make_game(ui):
    return SimpleNamespace(ui=ui, api=FakeApi(), audio=SimpleNamespace(play=lambda *a: None), toast=lambda *a: None)


def question(kind: str) -> dict:
    base = {"session_id": "s1", "context": "math_combat", "time_limit": 30, "instruction_vi": "Hãy ghép cặp",
            "math": {"subject_name_vi": "Đại số", "floor": 1, "skill_name_vi": "Ma trận", "tier": 1,
                     "tier_name_vi": "Nhập môn"}}
    if kind == "matching":
        return {**base, "input": "matching", "options": None,
                "prompt": {"text": "Ghép mỗi khái niệm với mô tả của nó.", "left": LEFT, "right": RIGHT[::-1]}}
    return {**base, "input": "ordering", "options": None,
            "prompt": {"text": "Sắp xếp các bước giải phương trình trùng phương.", "steps": STEPS[::-1]}}


@pytest.mark.parametrize("kind", ["matching", "ordering"])
@pytest.mark.parametrize("combat", [False, True])
def test_the_card_sends_the_answer_and_the_reveal_fits(kind, combat):
    from client.scenes.math_practice import MathCombatQuizScene, MathQuizScene
    ui = make_ui()
    game = make_game(ui)
    q = question(kind)
    card = MathCombatQuizScene(game, q, "m1", cast={"k": "x", "name_vi": "Ngũ Hành Trận"}) if combat \
        else MathQuizScene(game, q)
    ui.begin([], 0.016)
    card.draw_ui(ui)
    pre = [w for w in ui.widgets if w.startswith(("match_", "ord_step_"))]
    assert pre, "the card drew no input"
    n = 5 if kind == "matching" else 4
    if kind == "matching":
        for k in range(n):
            frame(ui, lambda: card.draw_ui(ui), click=f"match_l_{k}")
            frame(ui, lambda: card.draw_ui(ui), click=f"match_r_{k}")
        want = {"pairs": [0, 1, 2, 3, 4]}
    else:
        for i in range(n):
            frame(ui, lambda: card.draw_ui(ui), click=f"ord_step_{i}")
        want = {"order": [0, 1, 2, 3]}
    frame(ui, lambda: card.draw_ui(ui), click="mq_submit")
    assert game.api.posts == [("/quiz/answer", {"session_id": "s1", "answer": want})]
    assert card.given == want
    # the reveal after a wrong answer: the right answer and the steps, drawn without raising
    answer_text = "; ".join(f"{a} — {b}" for a, b in zip(LEFT, RIGHT)) if kind == "matching" else \
        "  ".join(f"{i}. {s}" for i, s in enumerate(STEPS, 1))
    card.result = {"correct": False, "reveal": {"answer_text": answer_text,
                                                "solution_vi": ["Một bước giải khá dài " * 4] * 4},
                   "combat": {"cast": "x", "missed": True, "correct": False}}
    ui.begin([], 0.016)
    card.draw_ui(ui)
    assert MI.given_text(kind, want) in card.given_text()


# ------------------------------------------------------------------ the world scene's side of a chiêu
def bare_world(sheet):
    """A WorldScene with only what the chiêu code touches; `sheet` replaces the Đạo Sĩ sheet."""
    from client.scenes.world import WorldScene
    ws = WorldScene.__new__(WorldScene)
    ws.game = SimpleNamespace(now=10.0, state=SimpleNamespace(me={"id": 7}), scenes=[])
    ws.casting, ws.skill_fx, ws.entities, ws.swing_t = {}, [], {}, 0.0
    ws.fx = SimpleNamespace(float_text=lambda *a, **k: texts.append(a[0]))
    ws.cast_sheet = lambda: sheet
    texts.clear()
    return ws


texts: list[str] = []


def fake_sheet(*clips):
    from client.engine import charsheet
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    doc = {"id": "t", "frame": {"w": 32, "h": 32}, "pivot": {"x": 16, "y": 24}, "cols": 2, "frames": 4,
           "clips": {c: {"fps": 10, "loop": False, "frames": {"down": [0, 1], "up": [0, 1], "left": [0, 1],
                                                              "right": [0, 1]}} for c in clips}}
    return charsheet.CharSheet(doc, surf)


@pytest.mark.parametrize("clips,want", [(("idle", "slash", "cast"), "cast"), (("idle", "slash"), "slash"),
                                        (("idle",), None)])
def test_the_caster_plays_the_chieu_clip_else_the_slash_else_the_old_swing(clips, want):
    ws = bare_world(fake_sheet(*clips))
    assert ws.cast_clip("cast") == want


def test_no_sheet_at_all_never_crashes_and_falls_back_to_the_swing():
    ws = bare_world(None)
    ws.on_mskill_fx("mcast", {"by": "p7", "s": "hoa_cau_thuat", "anim": "cast", "x": 5, "y": 5})
    ws.on_mskill_fx("mskill", {"by": "p7", "fx": "hoa_cau", "anim": "cast", "ok": 1, "x": 5, "y": 5, "tx": 40,
                               "ty": 5, "combo": 3})
    assert ws.swing_t > 0 and not ws.casting
    assert ws.skill_fx and ws.skill_fx[0]["fx"] == "hoa_cau"
    assert any("x3" in t for t in texts)                    # the combo is shown when it is more than one
    surf = pygame.Surface((480, 270))
    ws.game.now = 10.3
    ws.player = SimpleNamespace(x=5, y=5)
    ws.dead = False
    ws.draw_skill_fx(surf, 0, 0)
    assert ws.cast_image("p7", 5, 5, "down", 0, 0) is None


def test_a_miss_says_so_and_an_unknown_fx_id_is_drawn_as_the_slash():
    ws = bare_world(fake_sheet("slash"))
    ws.on_mskill_fx("mskill", {"by": "p9", "fx": "khong_co", "anim": "khong_co", "ok": 0, "x": 5, "y": 5})
    assert "Chiêu hụt!" in texts
    assert ws.skill_fx[0]["fx"] == "chem" and ws.skill_fx[0]["ok"] is False
    assert ws.casting["p9"]["anim"] == "khong_co" and ws.cast_clip("khong_co") == "slash"
    img = ws.cast_image("p9", 50, 80, "left", 0, 0)
    assert img is not None and img[0].get_size() == (32, 32)


def test_the_effect_of_my_own_chieu_waits_for_its_card_to_close():
    from client.scenes.math_practice import MathCombatQuizScene
    ws = bare_world(fake_sheet("slash"))
    card = MathCombatQuizScene.__new__(MathCombatQuizScene)
    card.cast = {"k": "thuong_quyen", "name_vi": "x"}
    ws.game.scenes = [ws, card]
    ws.on_mskill_fx("mcast", {"by": "p7", "anim": "slash"})
    ws.on_mskill_fx("mskill", {"by": "p7", "fx": "chem", "anim": "slash", "ok": 1, "x": 1, "y": 1})
    assert ws.skill_fx[0]["t0"] is None
    ws.game.now = 12.0
    ws.release_landings()
    assert ws.skill_fx[0]["t0"] is None                     # the card is still up
    ws.game.scenes = [ws]
    ws.release_landings()
    assert ws.skill_fx[0]["t0"] == 12.0 and ws.casting["p7"]["t0"] == 12.0
    # somebody else's chiêu is never held back
    ws.on_mskill_fx("mskill", {"by": "p9", "fx": "chem", "anim": "slash", "ok": 1, "x": 1, "y": 1})
    assert ws.skill_fx[1]["t0"] == 12.0


# ------------------------------------------------------------------ a question never gets lost behind a result
def waiting_world():
    """bare_world plus what the `q` message touches; open_question only records what it was given."""
    from client.scenes.quiz import CombatCard

    class Card(CombatCard):
        def __init__(self, result=None, sid="old"):
            self.result, self.q, self.finished = result, {"session_id": sid}, False

        def finish(self):
            self.finished = True
            ws.game.scenes.remove(self)

    ws = bare_world(fake_sheet("slash"))
    ws.flush_inputs = lambda: None
    ws.player = SimpleNamespace(moving=True)
    ws.dead, ws.waiting_q, ws.opened = False, None, []
    ws.open_question = lambda m, waited=0.0: ws.opened.append((m["q"]["session_id"], round(waited, 2)))
    ws.game.scenes = [ws]
    return ws, Card


def q_msg(sid="new"):
    return {"t": "q", "mid": "m1_0", "q": {"session_id": sid, "time_limit": 20}}


def test_a_question_opens_at_once_when_no_card_is_up():
    ws, _ = waiting_world()
    ws.on_net(q_msg())
    assert ws.opened == [("new", 0.0)] and ws.waiting_q is None


def test_a_question_behind_a_result_card_waits_and_opens_when_that_card_closes():
    """It used to be dropped: the server then held the player in Hộ Thể for a card nobody saw."""
    ws, Card = waiting_world()
    card = Card(result={"correct": True})
    ws.game.scenes.append(card)
    ws.on_net(q_msg())
    assert ws.opened == [] and ws.waiting_q is not None
    ws.game.now += 0.5
    ws.show_waiting_question()
    assert ws.opened == [] and not card.finished          # the result is still being shown
    ws.game.scenes.remove(card)                           # ... it closes by itself
    ws.game.now += 0.4
    ws.show_waiting_question()
    assert ws.opened == [("new", 0.9)] and ws.waiting_q is None    # and the card is told how long it waited


def test_a_waiting_question_closes_a_result_card_that_stays_too_long():
    from client.scenes import world
    ws, Card = waiting_world()
    card = Card(result={"correct": False})
    ws.game.scenes.append(card)
    ws.on_net(q_msg())
    ws.game.now += world.WAITING_Q_MAX + 0.1
    ws.show_waiting_question()
    assert card.finished and ws.opened == [("new", round(world.WAITING_Q_MAX + 0.1, 2))]


def test_a_card_still_being_answered_is_never_closed_for_a_new_question():
    from client.scenes import world
    ws, Card = waiting_world()
    card = Card(result=None)
    ws.game.scenes.append(card)
    ws.on_net(q_msg())
    assert ws.waiting_q is None and ws.opened == []       # as before: one open question at a time
    ws.waiting_q = (q_msg(), ws.game.now)                 # and even a held one never closes it
    ws.game.now += world.WAITING_Q_MAX + 1
    ws.show_waiting_question()
    assert not card.finished and ws.opened == [] and ws.waiting_q is None


def test_a_waiting_question_goes_away_when_the_server_ends_it_or_the_player_dies():
    ws, Card = waiting_world()
    ws.end_channel = lambda eid: None
    ws.game.scenes.append(Card(result={"correct": True}))
    ws.on_net(q_msg("s1"))
    ws.on_net({"t": "q_end", "sid": "other"})
    assert ws.waiting_q is not None                       # somebody else's session: not ours
    ws.on_net({"t": "q_end", "sid": "s1"})
    assert ws.waiting_q is None
    ws.on_net(q_msg("s2"))
    ws.dead = True
    ws.game.scenes = [ws]
    ws.show_waiting_question()
    assert ws.opened == [] and ws.waiting_q is None


def test_a_held_question_gets_only_the_time_the_server_still_allows():
    from client.scenes import world as world_mod
    ws, _ = waiting_world()
    del ws.open_question                                  # the real one this time
    pushed = []
    ws.game.top = ws
    ws.game.push = pushed.append
    ws.game.toast = lambda *a, **k: None
    ws.mskills, ws.mskill_ready = [], {}
    made = []
    import client.scenes.math_practice as mp
    real = mp.MathCombatQuizScene
    mp.MathCombatQuizScene = lambda game, q, mid, on_result=None, cast=None: made.append(q) or "card"
    try:
        ws.open_question({"mid": "m", "q": {"session_id": "s", "context": "math_combat", "time_limit": 20}},
                         waited=1.5)
    finally:
        mp.MathCombatQuizScene = real
    assert made[0]["time_limit"] == 18.5 and pushed == ["card"]
    assert world_mod.WAITING_Q_MAX < 3
