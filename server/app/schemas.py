from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class RegisterIn(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=256)


class LoginIn(RegisterIn):
    pass


class FirebaseIn(BaseModel):
    id_token: str = Field(max_length=4096)


class ResetPasswordIn(BaseModel):
    username: str = Field(max_length=64)
    recovery_code: str = Field(max_length=32)
    new_password: str = Field(max_length=256)


class ChangePasswordIn(BaseModel):
    old_password: str = Field(max_length=256)
    new_password: str = Field(max_length=256)


class GachaRollIn(BaseModel):
    banner: Literal["bees", "pets"] = "bees"
    count: int = 1
    free: bool = False
    currency: Literal["spirit_stones", "immortal_jade"] = "spirit_stones"


class AnswerIn(BaseModel):
    session_id: str = Field(max_length=36)
    answer: dict[str, Any] | None = None


class CharacterCreateIn(BaseModel):
    display_name: str = Field(max_length=64)
    appearance: dict[str, str] = Field(default_factory=dict)


class PositionIn(BaseModel):
    zone_id: str = Field(default="abode", max_length=32)
    x: float
    y: float
    facing: str = Field(default="down", max_length=5)


class TutorialIn(BaseModel):
    step: int = Field(ge=0, le=100)
