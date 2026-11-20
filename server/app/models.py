"""Database schema (spec section 4). Every table of the full game is defined here so the
first migration already has the final shape; later stages only add behaviour."""
from __future__ import annotations

import datetime as dt

from sqlalchemy import (JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String,
                        Text, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

UserFK = lambda: ForeignKey("users.id", ondelete="CASCADE")  # noqa: E731


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    recovery_code_hash: Mapped[str] = mapped_column(String(100))
    spirit_stones: Mapped[int] = mapped_column(Integer, default=300)   # Linh Thạch
    immortal_jade: Mapped[int] = mapped_column(Integer, default=0)     # Tiên Ngọc
    pity: Mapped[dict] = mapped_column(JSON, default=dict)             # {banner: {min_rarity: count}}
    daily_rolls_count: Mapped[int] = mapped_column(Integer, default=0)   # gacha rolls today
    daily_free_rolls_used: Mapped[int] = mapped_column(Integer, default=0)
    daily_reset_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    token_version: Mapped[int] = mapped_column(Integer, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    register_ip: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    last_login_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    banned_until: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    chat_banned_until: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    suspicious_flag: Mapped[str | None] = mapped_column(String(200), nullable=True)
    flags: Mapped[dict] = mapped_column(JSON, default=dict)  # tutorial step, decorations, ...
    # LAN worlds: the Firebase account this local user belongs to (None = username/password account)
    firebase_uid: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    __table_args__ = (Index("ix_quiz_user_created", "user_id", "created_at"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    # the mode that asked: math, math_combat, math_td, math_fishing, math_realm, math_skill,
    # math_dungeon, math_fortune, math_placement, math_meditate, math_tribulation
    context: Mapped[str] = mapped_column(String(16))
    ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    qtype: Mapped[str] = mapped_column(String(20))    # a math question type (balance/math.json)
    item_id: Mapped[str] = mapped_column(String(40))  # the math item or generator the question came from
    payload: Mapped[dict] = mapped_column(JSON)
    answer_key: Mapped[dict] = mapped_column(JSON)  # never sent to the client before answering
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    expires_at: Mapped[dt.datetime] = mapped_column(DateTime)
    answered_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    answer: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    answer_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Friendship(Base):
    __tablename__ = "friendships"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    friend_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    status: Mapped[str] = mapped_column(String(12), default="pending")  # pending|accepted
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class Character(Base):
    __tablename__ = "characters"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(20), unique=True)
    realm: Mapped[str] = mapped_column(String(16), default="pham_nhan")
    realm_stage: Mapped[int] = mapped_column(Integer, default=0)
    cultivation_xp: Mapped[int] = mapped_column(Integer, default=0)
    hp: Mapped[int] = mapped_column(Integer, default=100)
    max_hp: Mapped[int] = mapped_column(Integer, default=100)
    qi: Mapped[int] = mapped_column(Integer, default=50)
    stats: Mapped[dict] = mapped_column(JSON, default=dict)
    zone_id: Mapped[str] = mapped_column(String(32), default="abode")
    x: Mapped[float] = mapped_column(Float, default=0)
    y: Mapped[float] = mapped_column(Float, default=0)
    appearance: Mapped[dict] = mapped_column(JSON, default=dict)
    hotbar: Mapped[dict] = mapped_column(JSON, default=dict)
    tribulation_retry_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    facing: Mapped[str] = mapped_column(String(5), default="down")


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (UniqueConstraint("user_id", "item_id", "bound"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    item_id: Mapped[str] = mapped_column(String(40))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    bound: Mapped[bool] = mapped_column(Boolean, default=False)


class EquipmentInstance(Base):
    __tablename__ = "equipment_instances"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    item_id: Mapped[str] = mapped_column(String(40))
    rarity: Mapped[str] = mapped_column(String(12))
    enhance_level: Mapped[int] = mapped_column(Integer, default=0)
    equipped_slot: Mapped[str | None] = mapped_column(String(16), nullable=True)


class WeaponClaim(Base):
    """A weapon of Thiên Địa Đồ picked up from its spot (systems/weapons.py). One row per
    player and spot (`placed_id` = '<weapon>_<quality>'), so a spot gives its weapon once,
    whatever later happens to the piece (`instance_id` is the piece it gave, kept for the
    record only: a sold piece leaves it pointing at nothing)."""
    __tablename__ = "weapon_claims"
    __table_args__ = (UniqueConstraint("user_id", "placed_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    placed_id: Mapped[str] = mapped_column(String(48))
    instance_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    claimed_at: Mapped[dt.datetime] = mapped_column(DateTime)


class LinhCan(Base):
    """A player's linh căn (systems/linh_can.py, data/linh_can.json): the root they carry, the
    one a tẩy linh pill just revealed and that waits for the keep-or-take choice, the rolls
    since the last one at or above each pill's pity floor ({pill: n}), how many tests in all,
    and the đồ giám (every root id ever revealed to them). No row = chưa trắc linh."""
    __tablename__ = "linh_can"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    root_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    pending_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    pending_pill: Mapped[str | None] = mapped_column(String(40), nullable=True)
    pity: Mapped[dict] = mapped_column(JSON, default=dict)
    rolls: Mapped[int] = mapped_column(Integer, default=0)
    discovered: Mapped[list] = mapped_column(JSON, default=list)
    awakened_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class AchievementCounter(Base):
    """Thành Tựu (systems/achievements.py): one number per player and counter key - a running
    total ('kill', 'kill|rank=boss'), a best value ('answer_streak', 'cult') or, for a key with
    a '#', the marker that one value of a distinct count was already seen ('zones#loi_kiep_dai')."""
    __tablename__ = "achievement_counters"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    key: Mapped[str] = mapped_column(String(80), primary_key=True)
    value: Mapped[int] = mapped_column(Integer, default=0)


class Achievement(Base):
    """One achievement a player has reached at least its first tier of: the highest tier
    reached, the tiers claimed (bit i = tier i+1) and the highest tier the player was told of
    (the unlock toast; below `tier` = still to announce, even after a logout)."""
    __tablename__ = "achievements"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    ach_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    tier: Mapped[int] = mapped_column(Integer, default=0)
    claimed: Mapped[int] = mapped_column(Integer, default=0)
    seen: Mapped[int] = mapped_column(Integer, default=0)
    unlocked_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class Bee(Base):
    __tablename__ = "bees"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    bee_type: Mapped[str] = mapped_column(String(32))
    level: Mapped[int] = mapped_column(Integer, default=1)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    hive_slot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    role: Mapped[str] = mapped_column(String(12), default="hive")  # hive|guard
    bond: Mapped[int] = mapped_column(Integer, default=0)
    obtained_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class Hive(Base):
    __tablename__ = "hive"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    layout: Mapped[dict] = mapped_column(JSON, default=dict)
    level: Mapped[int] = mapped_column(Integer, default=1)
    decorations: Mapped[list] = mapped_column(JSON, default=list)
    honey_checked_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    honey: Mapped[float] = mapped_column(Float, default=0.0)        # Linh Mật waiting to be collected
    wax: Mapped[float] = mapped_column(Float, default=0.0)
    cells: Mapped[int] = mapped_column(Integer, default=5)          # open hexagon cells


class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    pet_type: Mapped[str] = mapped_column(String(32))
    level: Mapped[int] = mapped_column(Integer, default=1)
    equipped: Mapped[bool] = mapped_column(Boolean, default=False)


class FishCatch(Base):
    __tablename__ = "fish_catches"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    fish_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)
    best_size_cm: Mapped[float] = mapped_column(Float, default=0)
    first_caught_at: Mapped[dt.datetime] = mapped_column(DateTime)


class CodexEntry(Base):
    __tablename__ = "codex_entries"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    codex: Mapped[str] = mapped_column(String(12), primary_key=True)  # bee|monster|pet
    entry_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    discovered_at: Mapped[dt.datetime] = mapped_column(DateTime)
    progress: Mapped[dict] = mapped_column(JSON, default=dict)


class TdProgress(Base):
    __tablename__ = "td_progress"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    level_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    stars: Mapped[int] = mapped_column(Integer, default=0)
    best_wave: Mapped[int] = mapped_column(Integer, default=0)
    cleared_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class Quest(Base):
    __tablename__ = "quests"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    quest_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    state: Mapped[str] = mapped_column(String(12), default="active")
    progress: Mapped[dict] = mapped_column(JSON, default=dict)


class RealmRun(Base):
    __tablename__ = "realm_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    realm_id: Mapped[str] = mapped_column(String(32))
    started_at: Mapped[dt.datetime] = mapped_column(DateTime)
    ended_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[str | None] = mapped_column(String(12), nullable=True)
    members: Mapped[list] = mapped_column(JSON, default=list)


class RealmMember(Base):
    """Who went into which bí cảnh run (stage 9): the daily entry limit counts these rows."""
    __tablename__ = "realm_members"
    __table_args__ = (Index("ix_realm_members_user_day", "user_id", "day"),)
    run_id: Mapped[int] = mapped_column(ForeignKey("realm_runs.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    realm_id: Mapped[str] = mapped_column(String(32))
    day: Mapped[str] = mapped_column(String(10))                 # UTC+7 date of entry
    joined_at: Mapped[dt.datetime] = mapped_column(DateTime)
    left_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[str | None] = mapped_column(String(12), nullable=True)


class RealmClaim(Base):
    """One reward of a run for one player: a cleared room ('room0'...) or the final chest.
    The primary key makes it impossible to be paid twice for the same thing (spec 14.3)."""
    __tablename__ = "realm_claims"
    run_id: Mapped[int] = mapped_column(ForeignKey("realm_runs.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    stage: Mapped[str] = mapped_column(String(16), primary_key=True)
    loot: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class RealmLoot(Base):
    __tablename__ = "realm_loot"
    __table_args__ = (UniqueConstraint("run_id", "user_id", "item_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("realm_runs.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(UserFK())
    item_id: Mapped[str] = mapped_column(String(40))
    quantity: Mapped[int] = mapped_column(Integer, default=1)


class ChatReport(Base):
    __tablename__ = "chat_reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(UserFK())
    reported_id: Mapped[int] = mapped_column(UserFK())
    message: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(String(200), default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class Block(Base):
    __tablename__ = "blocks"
    user_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(UserFK(), primary_key=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    currency_or_item: Mapped[str] = mapped_column(String(40))
    delta: Mapped[int] = mapped_column(Integer)
    balance_after: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str] = mapped_column(String(40))
    ref_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class TribulationRun(Base):
    """Thiên Kiếp (spec 7.3): one 20-question exam to enter a new realm."""
    __tablename__ = "tribulation_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    from_realm: Mapped[str] = mapped_column(String(16))
    to_realm: Mapped[str] = mapped_column(String(16))
    total: Mapped[int] = mapped_column(Integer, default=0)       # questions in the exam
    index: Mapped[int] = mapped_column(Integer, default=0)       # questions answered so far
    correct: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[dt.datetime] = mapped_column(DateTime)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[str | None] = mapped_column(String(8), nullable=True)   # passed | failed


class TdRun(Base):
    """Thủ Thành Toán (stage 7, M10): a run being played. The log is saved as it grows (/td/event), so
    a game closed in the middle of a level can continue it, and what is saved can never be
    taken back (/td/finish must start with it)."""
    __tablename__ = "td_runs"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    level_id: Mapped[str] = mapped_column(String(32))
    params: Mapped[dict] = mapped_column(JSON)
    questions: Mapped[dict] = mapped_column(JSON, default=dict)   # session id -> {kind, word (the tower), ok, power, tier}
    events: Mapped[list] = mapped_column(JSON, default=list)
    started_at: Mapped[dt.datetime] = mapped_column(DateTime)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime)


class AlchemySession(Base):
    """Luyện đan (stage 8): one fire being tended. Ingredients and the fee are taken when it
    is lit; the zones of the fire stay here until /alchemy/finish."""
    __tablename__ = "alchemy_sessions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK(), index=True)
    recipe_id: Mapped[str] = mapped_column(String(32))
    params: Mapped[dict] = mapped_column(JSON)          # zones, periods, bar, furnace level, ingredients used
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    expires_at: Mapped[dt.datetime] = mapped_column(DateTime)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AdminAction(Base):
    """Stage 10: every admin command that changes something (spec 17), from chat or from
    `python -m app.admin_cli`. Names are copied so the log still reads after an account
    is deleted."""
    __tablename__ = "admin_actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    admin_name: Mapped[str] = mapped_column(String(40))          # username, or "cli"
    action: Mapped[str] = mapped_column(String(20), index=True)
    target_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    target_name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    detail: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)


class MathRun(Base):
    """One sitting on a floor of a math subject (milestone M2). Holds what the adaptive rule
    needs between two questions: the tier now and the two streaks. A sitting is either
    ordinary practice or the floor's own test, the Thiên kiếp nhỏ (`mode`, M5). Since the
    curriculum tree (Đạo Thụ) is wired, a sitting is on one *part* of a tree node - the
    node's micro-skills that live on this floor - named by `node_id`; a passed trial passes
    that part. A run with no `node_id` is an old save (or the placement test): a passed trial
    of that kind still covers the whole floor (systems/math_tree_progress.py)."""
    __tablename__ = "math_runs"
    __table_args__ = (Index("ix_math_runs_user_open", "user_id", "ended_at"),
                      Index("ix_math_runs_cleared", "user_id", "subject_id", "mode", "passed"),
                      Index("ix_math_runs_node", "user_id", "node_id"))
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    subject_id: Mapped[str] = mapped_column(String(40))
    node_id: Mapped[str | None] = mapped_column(String(40), nullable=True)   # Đạo Thụ node (None = whole floor)
    floor: Mapped[int] = mapped_column(Integer)
    mode: Mapped[str] = mapped_column(String(10), default="practice")   # practice|trial
    tier: Mapped[int] = mapped_column(Integer)                    # tier of the next question
    correct_streak: Mapped[int] = mapped_column(Integer, default=0)
    wrong_streak: Mapped[int] = mapped_column(Integer, default=0)
    combo: Mapped[int] = mapped_column(Integer, default=0)        # right answers in a row; a timeout ends it
    best_combo: Mapped[int] = mapped_column(Integer, default=0)
    asked: Mapped[int] = mapped_column(Integer, default=0)        # questions answered (timeouts included)
    correct: Mapped[int] = mapped_column(Integer, default=0)
    review_asked: Mapped[int] = mapped_column(Integer, default=0)  # of those, spiral review (rule 6)
    xp_gained: Mapped[int] = mapped_column(Integer, default=0)
    ladders: Mapped[int] = mapped_column(Integer, default=0, server_default="0")  # rule 8 ladders climbed (M11 đợt 2)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)   # a trial: passed, failed, still going
    started_at: Mapped[dt.datetime] = mapped_column(DateTime)
    ended_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class MathAnswer(Base):
    """Every answered math question. The learning rules read this log: which tier of a
    micro-skill is open (rule 3) now, mastery gates and spaced review in later milestones."""
    __tablename__ = "math_answers"
    __table_args__ = (Index("ix_math_answers_skill", "user_id", "skill_id", "tier", "id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    run_id: Mapped[int | None] = mapped_column(ForeignKey("math_runs.id", ondelete="SET NULL"), nullable=True)
    subject_id: Mapped[str] = mapped_column(String(40))
    skill_id: Mapped[str] = mapped_column(String(40))
    floor: Mapped[int] = mapped_column(Integer)
    tier: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[str] = mapped_column(String(40))
    qtype: Mapped[str] = mapped_column(String(20))
    fingerprint: Mapped[str] = mapped_column(String(64))          # concept + template + numbers (anti-repeat)
    correct: Mapped[bool] = mapped_column(Boolean)
    timed_out: Mapped[bool] = mapped_column(Boolean, default=False)
    review: Mapped[bool] = mapped_column(Boolean, default=False)   # a spiral-review question (M5, rule 6)
    answer_ms: Mapped[int] = mapped_column(Integer, default=0)
    answered_at: Mapped[dt.datetime] = mapped_column(DateTime)


class MathSubmission(Base):
    """One go at a programming exercise (M6). The row is opened when the player asks for
    the hidden tests and closed when their machine sends back what the program printed, so
    an unfinished row is simply an attempt nobody handed in. `code` is kept so the player
    can read back what they wrote; it never leaves their own account."""
    __tablename__ = "math_submissions"
    __table_args__ = (Index("ix_math_submissions_user", "user_id", "problem_id", "id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    problem_id: Mapped[str] = mapped_column(String(40))
    subject_id: Mapped[str] = mapped_column(String(40))
    floor: Mapped[int] = mapped_column(Integer)
    tier: Mapped[int] = mapped_column(Integer)
    verdict: Mapped[str | None] = mapped_column(String(4), nullable=True)   # AC|WA|TLE|RE|CE
    passed: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    ms: Mapped[int] = mapped_column(Integer, default=0)                    # the slowest test
    xp_gained: Mapped[int] = mapped_column(Integer, default=0)
    code: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    judged_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class MathRetry(Base):
    """A mistake that has to come back (learning-path rule 6, "tâm ma"): the template the
    player got wrong returns as a parallel question, the same idea with new numbers, once
    a few other questions have been answered. Cleared by a right answer to it."""
    __tablename__ = "math_retries"
    __table_args__ = (Index("ix_math_retries_open", "user_id", "subject_id", "floor", "cleared_at"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    subject_id: Mapped[str] = mapped_column(String(40))
    floor: Mapped[int] = mapped_column(Integer)
    skill_id: Mapped[str] = mapped_column(String(40))
    tier: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[str] = mapped_column(String(40))              # the template: an item id or a generator id
    fingerprint: Mapped[str] = mapped_column(String(64))          # the question that was missed last
    after_answer_id: Mapped[int] = mapped_column(Integer)         # math_answers.id of the latest miss
    misses: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    cleared_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)

class MathDungeonRun(Base):
    """One trip into a hầm ngục (M10). `layout` is what math_dungeon.generate made of
    (seed, subject, floor) when the run started - rooms, their kinds, guardians, the chest -
    kept so a run is not changed by a data edit while it is being played. `room` is the room
    being played (== number of rooms cleared), `progress` the right answers in it so far.
    `rewarded` is false for a run started after the day's rewarded runs were used up."""
    __tablename__ = "math_dungeon_runs"
    __table_args__ = (Index("ix_math_dungeon_runs_user", "user_id", "ended_at"),
                      Index("ix_math_dungeon_runs_day", "user_id", "started_at"))
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    seed: Mapped[int] = mapped_column(Integer)
    subject_id: Mapped[str] = mapped_column(String(40))
    floor: Mapped[int] = mapped_column(Integer)
    layout: Mapped[dict] = mapped_column(JSON)
    room: Mapped[int] = mapped_column(Integer, default=0)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    hearts: Mapped[int] = mapped_column(Integer)
    max_hearts: Mapped[int] = mapped_column(Integer)
    state: Mapped[str] = mapped_column(String(10), default="open")      # open|cleared|failed|abandoned
    asked: Mapped[int] = mapped_column(Integer, default=0)
    correct: Mapped[int] = mapped_column(Integer, default=0)
    xp_gained: Mapped[int] = mapped_column(Integer, default=0)
    stones_gained: Mapped[int] = mapped_column(Integer, default=0)
    items_gained: Mapped[dict] = mapped_column(JSON, default=dict)      # {item_id: qty}
    rewarded: Mapped[bool] = mapped_column(Boolean, default=True)
    started_at: Mapped[dt.datetime] = mapped_column(DateTime)
    ended_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)


class MathLadder(Base):
    """The ladder of a tier-5 question the player got wrong in a buổi luyện (learning-path
    rule 8, M11 đợt 2; systems/math_practice.py). `steps` are the ids of the tier 3-4
    questions to ask, in order; `step` how many have been answered. Kept in the database so
    the ladder goes on after the game is closed. `retry_id` is the rule-6 mistake (MathRetry)
    through which the tier-5 idea comes back once the ladder is climbed."""
    __tablename__ = "math_ladders"
    __table_args__ = (Index("ix_math_ladders_open", "user_id", "subject_id", "floor", "finished_at"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(UserFK())
    subject_id: Mapped[str] = mapped_column(String(40))
    floor: Mapped[int] = mapped_column(Integer)                   # the floor of the sittings that climb it
    item_id: Mapped[str] = mapped_column(String(40))              # the tier-5 question that was missed
    skill_id: Mapped[str] = mapped_column(String(40))
    steps: Mapped[list] = mapped_column(JSON)                     # rung ids, in order
    step: Mapped[int] = mapped_column(Integer, default=0)         # rungs answered so far
    missed: Mapped[int] = mapped_column(Integer, default=0)       # of those, answered wrong (or timed out)
    retry_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_run_id: Mapped[int | None] = mapped_column(Integer, nullable=True)   # the sitting of the miss
    run_id: Mapped[int | None] = mapped_column(Integer, nullable=True)           # the sitting of the latest rung
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
