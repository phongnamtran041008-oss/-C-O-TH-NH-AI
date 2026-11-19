"""The base of every question card: the question, its countdown and the round trip to
`POST /quiz/answer`. The client never knows the answer: it sends what the player chose and
shows what the server reveals afterwards. What a card looks like is up to the subclass
(math_practice.MathQuizScene and the cards built on it)."""
from __future__ import annotations

import pygame

from .base import Scene

KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]


class CombatCard:
    """Marker for a question card that belongs to a fight (math_practice.MathCombatQuizScene).
    The world scene never stacks two of them and closes them all when the fight ends."""


class QuizScene(Scene):
    def __init__(self, game, question: dict):
        super().__init__(game)
        self.q = question
        self.result: dict | None = None
        self.sent = False
        self.t = 0.0
        self.limit = float(question.get("time_limit") or 10)
        self.result_t = 0.0
        game.ui.set_value("quiz_text", "")

    def submit(self, answer: dict):
        if self.sent:
            return
        self.sent = True

        def ok(res):
            self.result = res
            self.result_t = 0.0
            self.game.on_xp(res.get("xp"))
            self.game.audio.play("correct" if res.get("correct") else "wrong")

        def err(e):
            self.sent = False
            self.game.api_error(e)
            if e.status in (404, 409):
                self.close()
        self.api.post("/quiz/answer", {"session_id": self.q["session_id"], "answer": answer}, ok, err)
