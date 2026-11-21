"""A wrong answer leaves time to read: the fish's question card and the fight cards wait for
the player after a wrong answer or a timeout ("Đã hiểu", Enter or Space), close quickly after a
right one, never hang forever (a hard cap), and a fight card tells the server when it closes
(`q_read`, only to a server that says it understands it)."""
from __future__ import annotations

from types import SimpleNamespace

import pygame

from client.scenes.fishing import FishQuizScene
from client.scenes.math_practice import MathCombatQuizScene
from client.tests.test_skill_fx import frame, make_game, make_ui, question

WRONG = {"correct": False, "reveal": {"answer_text": "1. a  2. b", "solution_vi": ["Một bước giải khá dài " * 4] * 3}}


def fish_card(ui, done):
    card = FishQuizScene(make_game(ui), {**question("ordering"), "context": "math_fishing"}, "Cá hiếm cắn câu",
                         on_result=done.append)
    card.close = lambda: done.append("closed")
    card.tell_fortune = lambda: None
    return card


def test_a_wrong_fish_answer_waits_for_the_player():
    ui = make_ui()
    done = []
    card = fish_card(ui, done)
    card.result = dict(WRONG)
    for _ in range(10):                                   # far past the old 3.5 s
        card.update(1.0, True)
    assert not done
    frame(ui, lambda: card.draw_ui(ui))
    assert "math_got_it" in ui.widgets
    frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_SPACE])
    assert done[0] == "closed" and done[1] is card.result


def test_the_enter_that_sent_the_answer_does_not_close_its_solution():
    ui = make_ui()
    done = []
    card = fish_card(ui, done)
    card.result = dict(WRONG)
    frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_RETURN])
    assert not done
    frame(ui, lambda: card.draw_ui(ui), click="math_got_it")
    assert done and done[0] == "closed"


def test_a_right_fish_answer_closes_by_itself():
    ui = make_ui()
    done = []
    card = fish_card(ui, done)
    card.result = {"correct": True, "reveal": {"answer_text": "x"}}
    card.update(FishQuizScene.CLOSE_RIGHT - 0.1, True)
    assert not done
    card.update(0.2, True)
    assert done == ["closed", card.result]


def test_a_fish_card_left_open_closes_at_its_cap():
    """(The reel that follows must still start inside the time the server allows it.)"""
    ui = make_ui()
    done = []
    card = fish_card(ui, done)
    card.result = dict(WRONG)
    card.update(FishQuizScene.READ_CAP - 0.5, True)
    assert not done
    card.update(1.0, True)
    assert done and done[0] == "closed"
    import json
    from client.tests.test_fishing_units import ROOT
    late = json.loads((ROOT / "server" / "data" / "balance" / "fishing.json").read_text(encoding="utf-8"))
    assert FishQuizScene.READ_CAP < late["reel_late_seconds"]


# ------------------------------------------------------------------ the fight card
class Net:
    def __init__(self, caps=("q_read",)):
        self.sent, self.caps = [], set(caps)

    def can(self, cap):
        return cap in self.caps

    def send(self, msg):
        self.sent.append(msg)
        return True


def combat_card(ui, net, result):
    game = make_game(ui)
    game.net = net
    scenes = []
    game.pop = lambda sc=None: (scenes.remove(sc or scenes[-1]), (sc or card).on_exit())
    card = MathCombatQuizScene(game, question("ordering"), "m1")
    card.close = lambda: game.pop(card)
    card.tell_fortune = lambda: None
    scenes.append(card)
    card.sent = True
    card.result = result
    return card, scenes


def test_a_wrong_fight_card_tells_the_server_when_it_closes():
    ui = make_ui()
    net = Net()
    card, scenes = combat_card(ui, net, {**WRONG, "combat": {"parry": False, "read_cap": 45.0}})
    card.update(30.0, True)
    assert scenes and not net.sent                        # still reading
    frame(ui, lambda: card.draw_ui(ui))
    frame(ui, lambda: card.draw_ui(ui), keys=[pygame.K_RETURN])
    assert not scenes and net.sent == [{"t": "q_read", "sid": "s1"}]


def test_a_fight_card_closes_at_the_servers_cap_and_still_tells_it():
    ui = make_ui()
    net = Net()
    card, scenes = combat_card(ui, net, {**WRONG, "combat": {"parry": False, "read_cap": 20.0}})
    card.update(19.5, True)
    assert scenes
    card.update(1.0, True)
    assert not scenes and net.sent == [{"t": "q_read", "sid": "s1"}]


def test_with_no_cap_from_the_server_the_card_still_closes_in_the_end():
    ui = make_ui()
    card, scenes = combat_card(ui, Net(), {**WRONG, "combat": {"mac_kich": 5}})
    card.update(MathCombatQuizScene.READ_CAP - 1, True)
    assert scenes
    card.update(2.0, True)
    assert not scenes


def test_a_right_answer_or_an_old_server_hears_no_q_read():
    ui = make_ui()
    net = Net()
    card, scenes = combat_card(ui, net, {"correct": True, "reveal": {"answer_text": "x"},
                                         "combat": {"parry": True}})
    card.update(5.0, True)
    assert not scenes and net.sent == []
    old = Net(caps=())                                    # a server without welcome.caps
    card, scenes = combat_card(ui, old, {**WRONG, "combat": {"parry": False}})
    frame(ui, lambda: card.draw_ui(ui))
    card.result_t = 1.0
    frame(ui, lambda: card.draw_ui(ui), click="math_got_it")
    assert not scenes and old.sent == []


def test_a_card_popped_by_the_world_tells_the_server_once():
    ui = make_ui()
    net = Net()
    card, scenes = combat_card(ui, net, {**WRONG, "combat": {"parry": False, "read_cap": 45.0}})
    card.on_exit()
    card.on_exit()
    assert net.sent == [{"t": "q_read", "sid": "s1"}]
    nothing = SimpleNamespace()
    assert MathCombatQuizScene.tell_read(SimpleNamespace(game=nothing, q={}, result=None, sent=False)) is None
