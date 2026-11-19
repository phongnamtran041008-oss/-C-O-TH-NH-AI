import json
import re

from sqlalchemy import select

from app import db as dbm
from app import models


async def register(client, name="tester", password="secret123"):
    r = await client.post("/auth/register", json={"username": name, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()
    return {"Authorization": f"Bearer {data['token']}"}, data


async def answer_key(session_id: str) -> dict:
    async with dbm.SessionLocal() as s:
        q = (await s.execute(select(models.QuizSession).where(models.QuizSession.id == session_id))).scalar_one()
        return q.answer_key


# CJK ideographs, and the tone-marked vowels only Chinese romanisation uses (a macron or a
# caron: Vietnamese has neither), so a payload that matches still carries the old word game.
_OLD_SCRIPT = re.compile("[\\u3400-\\u9fff\\uf900-\\ufaff\\u0101\\u01ce\\u0113\\u011b\\u012b\\u01d0"
                         "\\u014d\\u01d2\\u016b\\u01d4\\u01d6\\u01d8\\u01da\\u01dc]")


def old_script(obj) -> bool:
    """True when anything in `obj` (any JSON-able value) is written in the old game's script."""
    return bool(_OLD_SCRIPT.search(json.dumps(obj, ensure_ascii=False)))
