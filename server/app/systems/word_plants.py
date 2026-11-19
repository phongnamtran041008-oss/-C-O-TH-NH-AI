"""Leftovers of the removed word tower defence that the old library still reads (wave 2).

The word-plant tower defence is gone (Thủ Thành Toán, systems/math_td.py, is the only tower
defence now). Two older features still show a word's "plant role" and power: the Bách Thảo
Phổ of the old library (systems/library.py) and inscription stats (systems/inscription.py).
They reach these helpers as `td.role_of`, `td.roles_data`, `td.power` and
`td.plant_entries` (systems/td.py forwards those names here). Delete this module together
with the old library and inscription in wave 2, with `roles`, `idiom_skills` and `power` of
balance/td.json and data/plants/plant_roles.json.
"""
from __future__ import annotations

import json
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from ..config import DATA_DIR
from ..learning import srs
from ..learning.wordbank import bank
from ..models import Collection, Plot, User


def _cfg() -> dict:
    return balance.load("td")


@lru_cache(maxsize=1)
def roles_data() -> dict:
    return json.loads((DATA_DIR / "plants" / "plant_roles.json").read_text("utf-8"))


def role_of(word_id: str) -> str:
    """Spec 9.2: special characters by hand, the rest by topic."""
    w = bank().get(word_id)
    rd = roles_data()
    return rd["by_hanzi"].get(w.hanzi) or rd["by_topic"][w.topic]


def power(mastery: float, wither: float) -> float:
    """Spec 9.1: mastery 0 -> 60%, 100 -> 130%; wither in the real garden up to -30%."""
    p = _cfg()["power"]
    m = max(0.0, min(100.0, float(mastery))) / 100
    w = max(0.0, min(100.0, float(wither))) / 100
    return round((p["mastery_min"] + (p["mastery_max"] - p["mastery_min"]) * m) * (1 - p["wither_max_penalty"] * w), 4)


async def plant_entries(db: AsyncSession, user: User) -> dict[str, dict]:
    """Every learned word as a plant: role, power from mastery and the real garden's wither
    (the healthiest plot of that word counts; a word not growing now has no wither)."""
    cols = (await db.execute(select(Collection).where(
        Collection.user_id == user.id, Collection.introduced.is_(True)))).scalars().all()
    now = clock.now()
    wither: dict[str, float] = {}
    from ..garden.garden import wither_rate
    rate = await wither_rate(db, user.id)
    for p in (await db.execute(select(Plot).where(Plot.user_id == user.id, Plot.word_id.is_not(None)))).scalars():
        srs.refresh_wither(p, now, rate)
        wither[p.word_id] = min(wither.get(p.word_id, 100.0), p.wither)
    out = {}
    b = bank()
    skills = _cfg()["idiom_skills"]
    for c in cols:
        if c.word_id not in b.words:
            continue
        w = b.get(c.word_id)
        role = role_of(c.word_id)
        e = {"word_id": w.id, "hanzi": w.hanzi, "pinyin": w.pinyin, "meaning_vi": w.meaning_vi,
             "rarity": w.rarity, "role": role, "mastery": c.mastery, "wither": round(wither.get(w.id, 0.0), 1),
             "power": power(c.mastery, wither.get(w.id, 0.0))}
        if role == "thanh_ngu":
            e["skill"] = skills.get(w.hanzi)
            if e["skill"] is None:
                continue
        out[w.id] = e
    return out
