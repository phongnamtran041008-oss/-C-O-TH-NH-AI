"""M9 through the real client UI: in Loạn Số Cốc, cast the chiêu thức by their keys on a quái
lỗi sai. A right answer makes the chiêu land (its effect flies, damage, a combo), a wrong one
makes it miss (a fizzle, no damage, no Mặc Kích), and a chiêu the player has not unlocked is
refused by the server with the reason. Then the first floor is cleared, which opens the
Trận pháp: the ward is cast with a matching question and the area chiêu with an ordering
question, both answered through the new inputs.

    python -m client.tests.test_math_skill_flow <dir>     # leaves numbered screenshots in <dir>
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import time
from pathlib import Path

import pygame

from client import strings_vi as T
from client.tests.driver import ROOT, Driver, ServerProcess
from client.tests.test_combat_flow import nearest, walk_to, world
from client.tests.test_math_combat_flow import MA, VALLEY, answer_card
from client.tests.test_world_flow import make_account

sys.path.insert(0, str(ROOT / "server"))        # the test reads the map the server ships

from app.realtime import maps  # noqa: E402

KEYS = {"thuong_quyen": pygame.K_1, "kiem_quyet": pygame.K_2, "hoa_cau_thuat": pygame.K_3,
        "ngu_hanh_tran": pygame.K_4, "ho_than_tran": pygame.K_5, "thien_loi_tuyet_ky": pygame.K_6}
SUBJECT = "dai_so_tuyen_tinh"


class Spy:
    """What the world scene was told: the chiêu events of the channel and the floating texts."""

    def __init__(self, ws):
        self.events: list[dict] = []
        self.texts: list[str] = []
        on_fx, float_text = ws.on_fx, ws.fx.float_text

        def spy_fx(ev):
            if ev.get("k") in ("mcast", "mskill"):
                self.events.append(dict(ev))
            on_fx(ev)

        def spy_text(text, *a, **kw):
            self.texts.append(text)
            return float_text(text, *a, **kw)
        ws.on_fx, ws.fx.float_text = spy_fx, spy_text

    def landed(self, skill: str) -> list[dict]:
        return [e for e in self.events if e["k"] == "mskill" and e.get("s") == skill]


def me_eid(drv) -> str:
    return f"p{drv.game.state.me['id']}"


def settle(drv: Driver, server: ServerProcess) -> None:
    """Close whatever card is open: a neighbouring quái lỗi sai may ask its own question."""
    for _ in range(40):
        if not drv.top_is("MathCombatQuizScene"):
            return
        card = drv.game.top
        if not card.result:
            answer(drv, server, True)
        drv.wait(lambda: card not in drv.game.scenes, 6, "the card closes")


def approach(drv: Driver, server: ServerProcess, near: float = 24.0):
    """Stand next to the nearest quái lỗi sai (chiêu have a range of a few tens of pixels)."""
    ws = world(drv)
    end = time.time() + 40
    while time.time() < end:
        settle(drv, server)
        m = nearest(ws, MA)
        if m is None:
            drv.step(10)
            continue
        if math.hypot(m.pos[0] - ws.player.x, m.pos[1] - ws.player.y) < near:
            return m
        walk_to(drv, m.pos[0], m.pos[1], near=near - 6, timeout=3)
        drv.step(3)
    raise AssertionError(f"no {MA} to stand next to; scenes={drv.scene_names()}")


def cast(drv: Driver, server: ServerProcess, skill: str, near: bool = True):
    """Press the chiêu's key (next to a monster, unless it is a ward) and wait for its card."""
    ws = world(drv)
    sid = skill
    if near:
        approach(drv, server)
    drv.wait(lambda: ws.mskill_ready.get(sid, 0) < drv.game.now, 10, "the cooldown")
    for attempt in range(6):
        # a monster next to us may ask its own question at any moment (and the client now always
        # shows it): answer that one first, then press again
        settle(drv, server)
        drv.press(KEYS[sid])
        try:
            drv.wait(lambda: drv.top_is("MathCombatQuizScene"), 5, f"a card after pressing {sid}")
        except AssertionError:
            continue
        if getattr(drv.game.top, "cast", None):
            break
    assert drv.top_is("MathCombatQuizScene") and getattr(drv.game.top, "cast", None), \
        f"no card of {sid}; scenes={drv.scene_names()}; toasts={drv.toast_log[-3:]}"
    card = drv.game.top
    assert card.cast["k"] == sid and card.cast["name_vi"]
    return card


def key_of(server: ServerProcess, q: dict) -> dict:
    return json.loads(server.sql("select answer_key from quiz_sessions where id=?", (q["session_id"],))[0][0])


def answer(drv: Driver, server: ServerProcess, correct: bool) -> dict:
    """Answer the open card through its widgets, whatever its type; the key comes from the database."""
    card = drv.game.top
    q = card.q
    if q["input"] == "matching":
        pairs = key_of(server, q)["pairs"]
        if not correct:
            pairs = pairs[1:] + pairs[:1]
        for k, j in enumerate(pairs):
            drv.click(f"match_l_{k}")
            drv.click(f"match_r_{j}")
        drv.click("mq_submit")
    elif q["input"] == "ordering":
        order = key_of(server, q)["order"]
        for i in (order if correct else order[::-1]):
            drv.click(f"ord_step_{i}")
        drv.click("mq_submit")
    else:
        return answer_card(drv, server, correct)
    drv.wait(lambda: drv.top_is("MathCombatQuizScene") and drv.game.top.result, 10, "the result")
    return drv.game.top.result


def finish(drv: Driver) -> None:
    """Wait for the card that is up to close. Another one may open right behind it - the
    question of a monster standing next to us - which is not this card's business."""
    card = drv.game.top if drv.top_is("MathCombatQuizScene") else None
    drv.wait(lambda: card is None or card not in drv.game.scenes, 8, "the card closes")


def see_effect(drv: Driver, name: str, ok: bool = True) -> None:
    """The effect of a chiêu plays once the card has closed: wait for it to be on screen and photograph it."""
    ws = world(drv)
    drv.wait(lambda: any(f["t0"] is not None and f["ok"] == ok for f in ws.skill_fx), 6, f"the effect of {name}; skill_fx={ws.skill_fx} casting={ws.casting}")
    drv.shot(name)


def hover_slot(drv: Driver, slot: int) -> None:
    pygame.mouse.set_pos(drv.game.display.to_window(252 + slot * 24 + 11, 226 + 11))
    drv.step(3)


def run_math_skill_flow(workdir: Path, shots: Path | None = None) -> None:
    server = ServerProcess(workdir)
    try:
        url = server.url
        token, uid = make_account(url, "detu_m9", "Chiêu Sĩ")
        vmap = maps.load(VALLEY)
        area = next(a for a in vmap.monster_areas if a.props.get("monster") == MA)
        server.sql("update characters set zone_id=?, x=?, y=? where user_id=?",
                   (VALLEY, area.x + area.w / 2, area.y + area.h / 2, uid))
        # Trúc Cơ has the Linh Lực for all four chiêu that cost some (8 + 18 + 15 + 20 > the 50 of a newcomer)
        server.sql("update characters set realm='truc_co', realm_stage=1, qi=120 where user_id=?", (uid,))
        server.sql("insert into equipment_instances(user_id, item_id, rarity, enhance_level, inscriptions, "
                   "equipped_slot) values (?, 'kiem_go_dao', 'linh', 3, '[]', 'weapon')", (uid,))
        server.sql("update users set spirit_stones=500, flags=? where id=?",
                   (json.dumps({"tutorial": 5}), uid))
        (workdir / "session.json").write_text(json.dumps({"token": token, "username": "detu_m9",
                                                          "server_url": url}))
        drv = Driver(url, workdir, shots)
        drv.click("menu_start")
        drv.wait(lambda: world(drv) is not None and world(drv).joined, 15, "Loạn Số Cốc")
        drv.wait_api()
        ws = world(drv)
        assert ws.zone_id == VALLEY
        spy = Spy(ws)

        # ---- the second hotbar row: six chiêu from the data, three open and three locked
        drv.wait(lambda: ws.mskills is not None and len(ws.mskills) == 6, 10, "GET /math/skills")
        assert [s["id"] for s in ws.mskills] == list(KEYS), [s["id"] for s in ws.mskills]
        assert [s["unlocked"] for s in ws.mskills] == [True, True, True, False, False, False], ws.mskills
        for s in ws.mskills:
            assert s["locked_vi"] if not s["unlocked"] else s["locked_vi"] is None
        hover_slot(drv, 0)
        drv.shot("hotbar_open_chieu_tooltip")
        hover_slot(drv, 3)
        drv.shot("hotbar_locked_chieu_tooltip")
        pygame.mouse.set_pos((5, 5))

        # ---- Thường Quyền (đúng/sai): a right answer lands
        approach(drv, server)
        card = cast(drv, server, "thuong_quyen")
        assert card.q["input"] == "truefalse"
        drv.shot("card_of_the_chieu")
        res = answer(drv, server, True)
        c = res["combat"]
        assert c["cast"] == "thuong_quyen" and c["correct"] and not c["missed"] and c["damage"] > 0, c
        drv.wait(lambda: spy.landed("thuong_quyen"), 6, "the chiêu lands")
        ev = spy.landed("thuong_quyen")[-1]
        assert ev["ok"] == 1 and ev["fx"] == "chem" and ev["by"] == me_eid(drv), ev
        assert any(e["k"] == "mcast" and e["s"] == "thuong_quyen" for e in spy.events), "no channel event"
        assert ws.mskill_ready["thuong_quyen"] > drv.game.now - 5
        finish(drv)
        see_effect(drv, "chieu_lands_slash")
        rows = server.sql("select qtype, correct, run_id from math_answers where user_id=? order by id", (uid,))
        assert rows[-1] == ("true_false", 1, None), rows

        # ---- Phá Mê Kiếm Quyết (trắc nghiệm): a wrong answer misses - no damage, no Mặc Kích
        card = cast(drv, server, "kiem_quyet")
        assert card.q["input"] == "choice"
        res = answer(drv, server, False)
        c = res["combat"]
        assert c["cast"] == "kiem_quyet" and c["missed"] and c["damage"] == 0 and not c.get("mac_kich"), c
        assert c["combo"] == 0
        drv.wait(lambda: spy.landed("kiem_quyet"), 6, "the chiêu misses")
        ev = spy.landed("kiem_quyet")[-1]
        assert ev["ok"] == 0, ev
        drv.wait(lambda: T.MSKILL_MISS in spy.texts, 3, "the 'Chiêu hụt!' text")
        finish(drv)
        see_effect(drv, "chieu_misses_fizzle", ok=False)
        rows = server.sql("select qtype, correct from math_answers where user_id=? order by id", (uid,))
        assert rows[-1] == ("multiple_choice", 0), rows

        # ---- Hỏa Cầu Thuật (điền số, costs Linh Lực): right, and the qi is spent
        qi_before = drv.game.state.character["qi"]
        card = cast(drv, server, "hoa_cau_thuat")
        assert card.q["input"] == "number"
        drv.wait(lambda: drv.game.state.character["qi"] < qi_before, 5, "the qi is spent")
        res = answer(drv, server, True)
        c = res["combat"]
        assert c["cast"] == "hoa_cau_thuat" and c["correct"] and c["damage"] > 0, c
        drv.wait(lambda: spy.landed("hoa_cau_thuat"), 6, "the fireball lands")
        assert spy.landed("hoa_cau_thuat")[-1]["fx"] == "hoa_cau"
        finish(drv)
        see_effect(drv, "chieu_lands_fireball")

        # ---- locked chiêu are refused by the server, with the reason, and spend nothing
        for sid in ("ngu_hanh_tran", "thien_loi_tuyet_ky"):
            want = next(s["locked_vi"] for s in ws.mskills if s["id"] == sid)
            assert want
            for _ in range(6):         # a monster that is mid-question makes the server say "answering" first
                approach(drv, server)
                drv.press(KEYS[sid])
                try:
                    drv.wait(lambda: want in drv.toast_log, 3, f"the refusal of {sid}")
                    break
                except AssertionError:
                    continue
            assert want in drv.toast_log, (sid, want, drv.toast_log[-4:])
            # a locked chiêu opens no card (a neighbour's own question may be up, that is not a chiêu's)
            assert not (drv.top_is("MathCombatQuizScene") and drv.game.top.cast)
        drv.shot("locked_chieu_refused")

        # ---- clear floor 1: the Trận pháp open
        server.sql("insert into math_runs(user_id, subject_id, floor, mode, tier, correct_streak, wrong_streak, "
                   "combo, best_combo, asked, correct, review_asked, xp_gained, passed, started_at, ended_at) "
                   "values (?, ?, 1, 'trial', 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, datetime('now'), datetime('now'))",
                   (uid, SUBJECT))
        ws.load_mskills()
        drv.wait(lambda: all(s["unlocked"] for s in ws.mskills[3:5]), 10, "the Trận pháp unlock")

        # ---- Hộ Thân Trận (ghép cặp, a ward: no target)
        card = cast(drv, server, "ho_than_tran", near=False)
        assert card.q["input"] == "matching" and len(card.q["prompt"]["left"]) >= 3
        drv.shot("matching_card")
        res = answer(drv, server, True)
        assert res["combat"]["cast"] == "ho_than_tran" and res["combat"]["correct"], res["combat"]
        drv.wait(lambda: spy.landed("ho_than_tran"), 6, "the ward")
        ev = spy.landed("ho_than_tran")[-1]
        assert ev["ok"] == 1 and ev["fx"] == "ho_tran" and ev.get("r"), ev
        finish(drv)
        see_effect(drv, "ward_dome")

        # ---- Ngũ Hành Trận (sắp xếp bước, an area around the target)
        card = cast(drv, server, "ngu_hanh_tran")
        assert card.q["input"] == "ordering" and len(card.q["prompt"]["steps"]) >= 3
        drv.shot("ordering_card")
        res = answer(drv, server, True)
        assert res["combat"]["cast"] == "ngu_hanh_tran" and res["combat"]["correct"], res["combat"]
        drv.wait(lambda: spy.landed("ngu_hanh_tran"), 6, "the array")
        assert spy.landed("ngu_hanh_tran")[-1]["fx"] == "tran_do"
        finish(drv)
        see_effect(drv, "array_on_the_ground")
        drv.close()
    finally:
        server.stop()


def test_math_skill_flow():
    with tempfile.TemporaryDirectory(prefix="kvtt_m9_") as tmp:
        run_math_skill_flow(Path(tmp))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "screenshots" / "math_skill"
    with tempfile.TemporaryDirectory() as tmp:
        run_math_skill_flow(Path(tmp), out)
    print("screenshots in", out)
