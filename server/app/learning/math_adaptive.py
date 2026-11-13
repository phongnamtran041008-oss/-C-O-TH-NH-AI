"""Which tier the next math question has (learning-path rules 2 and 3). Pure rules: the
numbers come from balance/math.json, the answers from whoever calls.

Rule 2, inside one sitting: `up_after_correct_streak` right answers in a row raise the
tier by one, `down_after_wrong_streak` wrong ones lower it by one, and the tier never
leaves the range of the floor.

Rule 3, per micro-skill: tier N is open only when at least `correct_at_previous_tier` of
the player's last `window` answers at tier N-1 of that micro-skill were right. The lowest
tier of the floor is always open.

A question's tier is the lower of the two: the sitting's tier, capped by what is open
for the micro-skill it asks about.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from . import math_path


@dataclass(frozen=True)
class TierState:
    tier: int
    correct_streak: int = 0
    wrong_streak: int = 0


def start(floor: int, config: dict | None = None) -> TierState:
    """A sitting starts at the lowest tier of its floor."""
    return TierState(tier=math_path.floor_tiers(floor, config)[0])


def after_answer(state: TierState, correct: bool, floor: int, config: dict | None = None) -> TierState:
    """The state after one answer (a timeout is a wrong answer). A streak that moves the
    tier is used up: the next move needs a new streak. At the edge of the floor's range
    the tier stays and the streak keeps counting."""
    config = config or math_path.cfg()
    lo, hi = math_path.floor_tiers(floor, config)
    rule = config["adaptive"]
    tier = min(max(state.tier, lo), hi)
    if correct:
        streak = state.correct_streak + 1
        if streak >= rule["up_after_correct_streak"] and tier < hi:
            return TierState(tier + 1)
        return TierState(tier, correct_streak=streak)
    streak = state.wrong_streak + 1
    if streak >= rule["down_after_wrong_streak"] and tier > lo:
        return TierState(tier - 1)
    return TierState(tier, wrong_streak=streak)


def open_tier(floor: int, results_by_tier: Mapping[int, Sequence[bool]], config: dict | None = None) -> int:
    """The highest tier of this floor that is open for one micro-skill.
    results_by_tier[t] = the player's answers at tier t of that micro-skill, oldest first
    (True = right); only the last `window` of them count."""
    config = config or math_path.cfg()
    lo, hi = math_path.floor_tiers(floor, config)
    rule = config["tier_unlock"]
    tier = lo
    while tier < hi:
        recent = list(results_by_tier.get(tier, ()))[-rule["window"]:]
        if sum(1 for r in recent if r) < rule["correct_at_previous_tier"]:
            break
        tier += 1
    return tier


def question_tier(state_tier: int, floor: int, results_by_tier: Mapping[int, Sequence[bool]],
                  config: dict | None = None) -> int:
    """The tier of the next question about one micro-skill."""
    lo, _ = math_path.floor_tiers(floor, config)
    return max(lo, min(state_tier, open_tier(floor, results_by_tier, config)))
