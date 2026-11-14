"""Leaving a floor, and coming back to it: learning-path rules 3 and 6 (milestone M5).

Rule 3, the **mastery gate**. A floor is left behind only when both halves are done:

  (a) every micro-skill of the floor is being answered *at the highest tier of the floor*
      and got at least `min_correct_pct` of its last `window` answers at that tier right;
  (b) the floor's own test, the **Thiên kiếp nhỏ**, is passed: one question per micro-skill
      at the highest tier of the floor, with at most `max_wrong` of them missed.

Half (a) is read from the answer log, so it is always the player's recent form, not
something they passed once. "At the highest tier of the floor" is this module's reading of
the plan's "ở bậc hiện tại": the tier a micro-skill is *currently* asked at is the highest
one open for it (learning/math_adaptive.open_tier), and a floor whose hardest questions a
player never reached is not a floor they have finished. A gate that is not met is never a
hard block: the player is told which micro-skills are weak, practises them and tries again
at once.

Rule 6, **spiral review**. A sitting on floor N keeps mixing in questions from the floors
below it, between `share_min` and `share_max` of the questions asked. A micro-skill is due
again after `intervals_days[streak]` days, where the streak is how many times in a row it
was last answered right (1 -> 3 -> 7 -> 14 days; a wrong answer puts it back to 1 day).
Among the micro-skills that are due, the ones answered worst lately come first.

Pure rules: no database and no pygame here. The numbers come from balance/math.json, the
answers from whoever calls. systems/math_practice.py reads the log and plays the sitting.
"""
from __future__ import annotations

import datetime as dt
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from . import math_adaptive, math_path

LOCKED, OPEN, CLEARED = "locked", "open", "cleared"
STATES = (LOCKED, OPEN, CLEARED)


# ------------------------------------------------------------------ config
def gate_cfg(config: dict | None = None) -> dict:
    return (config or math_path.cfg())["mastery_gate"]


def trial_cfg(config: dict | None = None) -> dict:
    return gate_cfg(config)["trial"]


def review_cfg(config: dict | None = None) -> dict:
    return (config or math_path.cfg())["spiral_review"]


def needed_correct(config: dict | None = None) -> int:
    """How many of the last `window` answers must be right: 80% of 5 is 4."""
    g = gate_cfg(config)
    return math.ceil(g["window"] * g["min_correct_pct"] / 100)


# ------------------------------------------------------------------ rule 3 (a): the gate
@dataclass(frozen=True)
class SkillGate:
    """Half (a) of the gate for one micro-skill: its form at the tier it is asked at now."""
    skill_id: str
    tier: int                       # the highest tier open for this micro-skill
    top_tier: int                   # the highest tier of the floor
    answers: tuple[bool, ...]       # its last `window` answers at `tier`, oldest first
    needed: int
    window: int

    @property
    def correct(self) -> int:
        return sum(1 for a in self.answers if a)

    @property
    def at_top(self) -> bool:
        """Is this micro-skill already being asked at the hardest tier of the floor?"""
        return self.tier >= self.top_tier

    @property
    def ok(self) -> bool:
        return self.at_top and len(self.answers) >= self.window and self.correct >= self.needed

    def view(self) -> dict:
        return {"skill": self.skill_id, "tier": self.tier, "top_tier": self.top_tier,
                "at_top": self.at_top, "answered": len(self.answers), "correct": self.correct,
                "needed": self.needed, "window": self.window, "ok": self.ok}


@dataclass(frozen=True)
class FloorGate:
    floor: int
    skills: tuple[SkillGate, ...]

    @property
    def ok(self) -> bool:
        return bool(self.skills) and all(s.ok for s in self.skills)

    @property
    def weak(self) -> tuple[SkillGate, ...]:
        """What to go and practise: the micro-skills that are not through the gate yet."""
        return tuple(s for s in self.skills if not s.ok)

    def view(self) -> dict:
        return {"floor": self.floor, "ok": self.ok, "skills": [s.view() for s in self.skills],
                "weak": [s.skill_id for s in self.weak]}


def skill_gate(skill_id: str, floor: int, results_by_tier: Mapping[int, Sequence[bool]],
               config: dict | None = None) -> SkillGate:
    """results_by_tier[t] = this micro-skill's answers at tier t, oldest first (True = right)."""
    config = config or math_path.cfg()
    window = gate_cfg(config)["window"]
    tier = math_adaptive.open_tier(floor, results_by_tier, config)
    answers = tuple(results_by_tier.get(tier, ()))[-window:]
    return SkillGate(skill_id=skill_id, tier=tier, top_tier=math_path.floor_tiers(floor, config)[1],
                     answers=answers, needed=needed_correct(config), window=window)


def floor_gate(floor: int, skill_ids: Iterable[str],
               results: Mapping[str, Mapping[int, Sequence[bool]]],
               config: dict | None = None) -> FloorGate:
    """Half (a) of the gate for a whole floor, one entry per micro-skill of that floor."""
    config = config or math_path.cfg()
    return FloorGate(floor=floor, skills=tuple(
        skill_gate(sid, floor, results.get(sid, {}), config) for sid in skill_ids))


# ------------------------------------------------------------------ rule 3 (b): the trial
def trial_skills(subject: math_path.Subject, floor: int, config: dict | None = None) -> list[str]:
    """The micro-skills the Thiên kiếp nhỏ of this floor asks about, in path order, each one
    `questions_per_skill` times."""
    per = trial_cfg(config)["questions_per_skill"]
    return [s.id for s in subject.floor(floor).skills for _ in range(per)]


def trial_total(subject: math_path.Subject, floor: int, config: dict | None = None) -> int:
    return len(trial_skills(subject, floor, config))


def trial_tier(floor: int, config: dict | None = None) -> int:
    """The trial is all questions at the hardest tier of the floor."""
    return math_path.floor_tiers(floor, config)[1]


def trial_verdict(asked: int, correct: int, total: int, config: dict | None = None) -> bool | None:
    """True = passed, False = failed, None = still going. A trial is lost as soon as too many
    questions are missed, so nobody has to finish a trial they cannot pass any more."""
    allowed = trial_cfg(config)["max_wrong"]
    if asked - correct > allowed:
        return False
    if asked >= total:
        return True
    return None


# ------------------------------------------------------------------ which floors are open
def floor_below(subject: math_path.Subject, floor: int) -> int | None:
    """The floor whose trial opens this one, or None for the first floor of the subject.
    The hidden floor waits for the last main floor; it opens nothing itself."""
    mains = [f.number for f in subject.main_floors]
    if not mains or floor == mains[0]:
        return None
    hidden = subject.hidden_floor
    if hidden is not None and floor == hidden.number:
        return mains[-1]
    below = [n for n in mains if n < floor]
    return below[-1] if below else None


def floor_above(subject: math_path.Subject, floor: int) -> int | None:
    """The floor that clearing this one opens: the next main floor, the hidden floor after
    the last main one, and nothing beyond that."""
    mains = [f.number for f in subject.main_floors]
    above = [n for n in mains if n > floor]
    if above:
        return above[0]
    hidden = subject.hidden_floor
    if hidden is not None and mains and floor == mains[-1]:
        return hidden.number
    return None


def floor_state(subject: math_path.Subject, floor: int, cleared: Iterable[int]) -> str:
    """"cleared" (its trial is passed), "open" (playable) or "locked"."""
    done = set(cleared)
    if floor in done:
        return CLEARED
    need = floor_below(subject, floor)
    return OPEN if need is None or need in done else LOCKED


def playable(subject: math_path.Subject, floor: int, cleared: Iterable[int]) -> bool:
    return floor_state(subject, floor, cleared) in (OPEN, CLEARED)


def next_floor(subject: math_path.Subject, cleared: Iterable[int]) -> int | None:
    """The main floor the player is working on: the lowest one not cleared yet, or None when
    every main floor is done (then the subject is finished and only the hidden floor is left)."""
    done = set(cleared)
    return next((f.number for f in subject.main_floors if f.number not in done), None)


# ------------------------------------------------------------------ rule 6: spiral review
@dataclass(frozen=True)
class ReviewStat:
    """One micro-skill of an earlier floor, as the spaced-repetition schedule sees it."""
    skill_id: str
    floor: int
    last_answered: dt.datetime | None       # None = never answered, or answered long ago
    streak: int                             # right answers in a row, latest first
    recent: tuple[bool, ...]                # its last few answers, oldest first

    @property
    def accuracy(self) -> float:
        """How well it has been going lately; a micro-skill with no answers counts as 0."""
        return (sum(1 for r in self.recent if r) / len(self.recent)) if self.recent else 0.0

    @property
    def lapsed(self) -> bool:
        """Was the last answer wrong? Then the micro-skill is due again at once, not in a
        day: this is rule 5's "tâm ma" for the floors below, and it is what spaced
        repetition does with a lapse."""
        return bool(self.recent) and not self.recent[-1]

    def wait_days(self, config: dict | None = None) -> int:
        """The wait after this many right answers in a row: the first one buys the first
        interval (1 day), the second the next (3 days), and the last interval repeats."""
        days = review_cfg(config)["intervals_days"]
        return days[min(max(self.streak, 1), len(days)) - 1]

    def due_at(self, config: dict | None = None) -> dt.datetime | None:
        """When it comes back, or None for "now" (never answered, or answered wrong)."""
        if self.last_answered is None or self.lapsed:
            return None
        return self.last_answered + dt.timedelta(days=self.wait_days(config))

    def is_due(self, now: dt.datetime, config: dict | None = None) -> bool:
        due = self.due_at(config)
        return due is None or due <= now

    def overdue_days(self, now: dt.datetime, config: dict | None = None) -> float:
        due = self.due_at(config)
        return float("inf") if due is None else (now - due).total_seconds() / 86400

    def view(self, now: dt.datetime, config: dict | None = None) -> dict:
        due = self.due_at(config)
        return {"skill": self.skill_id, "floor": self.floor, "streak": self.streak,
                "wait_days": self.wait_days(config), "due": self.is_due(now, config),
                "due_at": due.isoformat(timespec="seconds") if due else None}


def review_queue(stats: Iterable[ReviewStat], now: dt.datetime,
                 config: dict | None = None) -> list[ReviewStat]:
    """The micro-skills due for review, the ones answered worst lately first, and among
    equals the one waiting longest. Same order on every run."""
    config = config or math_path.cfg()
    due = [s for s in stats if s.is_due(now, config)]
    return sorted(due, key=lambda s: (s.accuracy, -s.overdue_days(now, config), s.floor, s.skill_id))


def wants_review(asked: int, review_asked: int, config: dict | None = None) -> bool:
    """Is the next question of a sitting a review question? `share_max` of the questions
    asked are review questions, so with 0.25 every fourth one is - which keeps the share
    above `share_min` as well."""
    share = review_cfg(config)["share_max"]
    return review_asked < int(share * (asked + 1))
