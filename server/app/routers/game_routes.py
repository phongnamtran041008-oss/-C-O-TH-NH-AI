from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance, clock
from ..auth import api_error, current_user, write_user
from ..db import get_db
from ..learning import quiz
from ..models import QuizSession, User
from ..models import Character
from ..schemas import AnswerIn, CharacterCreateIn, GachaRollIn, PositionIn, TutorialIn
from ..systems import character as charsys
from ..systems import gacha_service
from ..systems.gacha import GachaError

router = APIRouter()


@router.get("/me")
async def me(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    gacha_service.reset_daily(user, clock.local_date(clock.now()))
    from ..systems import books, quests
    await quests.ensure(db, user.id)    # today's daily tasks exist before anything counts toward them
    await db.commit()
    cfg = balance.gacha()
    has_char = await db.get(Character, user.id) is not None
    return {"id": user.id, "username": user.username, "spirit_stones": user.spirit_stones,
            "immortal_jade": user.immortal_jade, "is_admin": user.is_admin,
            "has_character": has_char, "tutorial_step": (user.flags or {}).get("tutorial", 0),
            "daily_rolls_left": cfg["daily_roll_limit"] - user.daily_new_seeds_count,
            "free_rolls_left": cfg["daily_free_rolls"] - user.daily_free_rolls_used,
            **books.worn(user)}


@router.post("/tutorial")
async def tutorial(body: TutorialIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    flags = dict(user.flags or {})
    flags["tutorial"] = max(int(flags.get("tutorial", 0)), body.step)  # never goes backwards
    user.flags = flags
    await db.commit()
    return {"tutorial_step": flags["tutorial"]}


# ---------------------------------------------------------------- character
def _char_err(e: charsys.CharacterError):
    return api_error(e.status, e.code, e.message_vi)


@router.post("/character/create")
async def character_create(body: CharacterCreateIn, user: User = Depends(write_user),
                           db: AsyncSession = Depends(get_db)):
    try:
        out = await charsys.create(db, user, body.display_name, body.appearance)
    except charsys.CharacterError as e:
        await db.rollback()
        raise _char_err(e)
    await db.commit()
    return out


@router.get("/character")
async def character_get(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    ch = await db.get(Character, user.id)
    if ch is None:
        raise api_error(404, "no_character", "Bạn chưa tạo nhân vật.")
    return charsys.view(ch)


@router.get("/character/options")
async def character_options():
    c = charsys.cfg()
    return {k: c[k] for k in ("hair_colors", "hair_styles", "bodies", "display_name_min", "display_name_max")}


@router.post("/character/position")
async def character_position(body: PositionIn, user: User = Depends(write_user),
                             db: AsyncSession = Depends(get_db)):
    try:
        out = await charsys.save_position(db, user, body.zone_id, body.x, body.y, body.facing)
    except charsys.CharacterError as e:
        raise _char_err(e)
    await db.commit()
    return out


# ---------------------------------------------------------------- gacha
@router.get("/gacha/banners")
async def gacha_banners(user: User = Depends(current_user)):
    return {"banners": gacha_service.banner_info(user)}


@router.post("/gacha/roll")
async def gacha_roll(body: GachaRollIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    try:
        out = await gacha_service.roll(db, user, body.banner, body.count, body.free, currency=body.currency)
    except GachaError as e:
        await db.rollback()
        raise api_error(400, e.code, e.message_vi)
    await db.commit()
    return out


# ---------------------------------------------------------------- quiz
@router.post("/quiz/answer")
async def quiz_answer(body: AnswerIn, user: User = Depends(write_user), db: AsyncSession = Depends(get_db)):
    try:
        out = await quiz.answer(db, user, body.session_id, body.answer)
    except quiz.QuizError as e:
        await db.rollback()
        raise api_error(e.status, e.code, e.message_vi)
    await db.commit()
    return out


@router.get("/quiz/{session_id}/audio")
async def quiz_audio(session_id: str, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    """Listening questions stream audio through the session so the client never learns
    which word (= the answer) is being played."""
    s = await db.get(QuizSession, session_id)
    if s is None or s.user_id != user.id or s.qtype != "Q4":
        raise api_error(404, "no_audio", "Không có âm thanh.")
    path = quiz.AUDIO_DIR / f"{s.item_id}.mp3"
    if not path.exists():
        raise api_error(404, "no_audio", "Không có âm thanh.")
    return FileResponse(path, media_type="audio/mpeg", filename="q.mp3")


