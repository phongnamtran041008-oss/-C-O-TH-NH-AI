"""WebSocket message formats (spec 15.1). Every message is a JSON object with a short
type field `t`; the first client message (`hello`) carries the protocol version `v`.
Documented for humans in docs/PROTOCOL.md. Client -> server messages are validated here;
anything malformed is answered with an `error` and otherwise ignored."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

from ..config import PROTOCOL_VERSION

FACING = ("down", "up", "left", "right")
FACING_CODE = {f: i for i, f in enumerate(FACING)}


class Hello(BaseModel):
    t: Literal["hello"]
    v: int
    token: str = Field(max_length=1000)
    # what this client can do beyond the protocol version: "q_read" = it reports when the card
    # of a wrong answer closes (QRead). An old client sends none and keeps the old timing.
    caps: list[str] = Field(default_factory=list, max_length=16)


class Ping(BaseModel):
    t: Literal["ping"]
    c: float | None = None  # client clock, echoed back


class Input(BaseModel):
    """Movement intent: the keys held for each client frame since the last message."""
    t: Literal["in"]
    s: int = Field(ge=0)
    k: list[tuple[int, int, int]] = Field(max_length=64)

    @field_validator("k")
    @classmethod
    def _steps(cls, v):
        for dx, dy, ms in v:
            if dx not in (-1, 0, 1) or dy not in (-1, 0, 1) or not (0 < ms <= 100):
                raise ValueError("bad step")
        return v


class Join(BaseModel):
    t: Literal["join"]
    zone: str = Field(max_length=32)
    via: Literal["portal", "abode", "resume"] = "portal"


class Channel(BaseModel):
    t: Literal["channel"]
    n: int = Field(ge=1, le=99)


class Chat(BaseModel):
    t: Literal["chat"]
    ch: Literal["world", "zone", "friend", "party"]
    text: str = Field(max_length=1000)
    to: str | None = Field(default=None, max_length=40)   # friend's display name


class Face(BaseModel):
    """Turn without moving (e.g. to face an NPC)."""
    t: Literal["face"]
    f: Literal["down", "up", "left", "right"]


class Attack(BaseModel):
    """Normal attack on a monster (left click), stage 4."""
    t: Literal["atk"]
    id: str = Field(max_length=24)


class Dodge(BaseModel):
    """Né Đòn (the open-world rule, world_plan.json "combat"): a short dash in a direction,
    queued among the movement messages under the next sequence number `s`."""
    t: Literal["dodge"]
    s: int = Field(ge=0)
    dx: int = Field(ge=-1, le=1)
    dy: int = Field(ge=-1, le=1)


class Glide(BaseModel):
    """Đạp Kiếm Lướt (world_plan.json unlock dap_kiem_luot): glide on the sword to the landing
    point (x, y) the client picked, queued among the movement messages under the number `s`."""
    t: Literal["glide"]
    s: int = Field(ge=0)
    x: float = Field(ge=0, le=10000)
    y: float = Field(ge=0, le=10000)


class Ride(BaseModel):
    """Cưỡi linh thú (unlock cuoi_linh_thu): mount the worn beast (on) or get down, queued among
    the movement messages under the number `s` (the speed changes from that step on)."""
    t: Literal["ride"]
    s: int = Field(ge=0)
    on: bool


class Fly(BaseModel):
    """Ngự kiếm (unlocks dap_kiem_luot, ngu_kiem_phi_hanh): take off on the sword (on) or come
    down, queued among the movement messages under the number `s`; the steps after it are
    flown (realtime/glide.fly_step) until the landing."""
    t: Literal["fly"]
    s: int = Field(ge=0)
    on: bool


class Formation(BaseModel):
    """Bày pháp trận (unlock phap_tran): lay a formation on the ground at the feet."""
    t: Literal["tran"]


class MathCast(BaseModel):
    """Cast a chiêu thức gắn câu hỏi (M9, data/math/skills.json): the server answers with a
    question of the chiêu's type; id = target monster, null for a ward."""
    t: Literal["mskill"]
    k: str = Field(max_length=40)
    id: str | None = Field(default=None, max_length=24)


class QRead(BaseModel):
    """The card of a wrong (or timed-out) fight question was closed: the player has read the
    solution, the fight may go on (realtime/combat.end_reading). `sid` = its quiz session."""
    t: Literal["q_read"]
    sid: str = Field(max_length=64)


class PartyCmd(BaseModel):
    """Tổ đội (stage 9): invite by display name, answer an invite (uid = who invited), leave,
    kick or promote a member (uid)."""
    t: Literal["party"]
    op: Literal["invite", "accept", "decline", "leave", "kick", "promote"]
    name: str | None = Field(default=None, max_length=40)
    uid: int | None = None


class RealmCmd(BaseModel):
    """Bí cảnh (stage 9): enter with the party (leader), join/leave the matchmaking queue, or
    leave the run. `rift` instead of `realm` for a Khe Nứt Mực seen in the world."""
    t: Literal["realm"]
    op: Literal["enter", "queue", "unqueue", "leave"]
    realm: str | None = Field(default=None, max_length=32)
    rift: str | None = Field(default=None, max_length=24)


class Mark(BaseModel):
    """A ping icon on the ground for the party (spec 14.2: 'ping biểu tượng')."""
    t: Literal["mark"]
    x: float = Field(ge=0, le=10000)
    y: float = Field(ge=0, le=10000)
    i: int = Field(ge=0, le=3)


MESSAGES: dict[str, type[BaseModel]] = {"ping": Ping, "in": Input, "join": Join, "channel": Channel,
                                        "chat": Chat, "face": Face, "atk": Attack, "dodge": Dodge,
                                        "mskill": MathCast, "party": PartyCmd, "realm": RealmCmd, "mark": Mark,
                                        "glide": Glide, "ride": Ride, "tran": Formation, "fly": Fly,
                                        "q_read": QRead}
SERVER_CAPS = ["q_read"]   # sent in `welcome`: what this server understands beyond the version


class BadMessage(Exception):
    pass


def parse(data: Any) -> BaseModel:
    if not isinstance(data, dict) or not isinstance(data.get("t"), str):
        raise BadMessage("no type")
    model = MESSAGES.get(data["t"])
    if model is None:
        raise BadMessage(f"unknown type {data['t']!r}")
    try:
        return model.model_validate(data)
    except ValidationError as e:
        raise BadMessage(str(e.errors()[0].get("msg", "invalid"))) from None


def error(code: str, message_vi: str, **extra) -> dict:
    return {"t": "error", "code": code, "message_vi": message_vi, **extra}


__all__ = ["PROTOCOL_VERSION", "Hello", "Ping", "Input", "Join", "Channel", "Chat", "Face", "parse",
           "BadMessage", "error", "FACING", "FACING_CODE", "Attack", "MathCast", "PartyCmd", "RealmCmd",
           "Mark", "Dodge", "Glide", "Ride", "Formation", "QRead", "SERVER_CAPS"]
