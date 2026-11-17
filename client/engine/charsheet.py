"""Reading the character sheets that come out of the Blender pipeline (M8).

A character is `client/assets/chars/<id>.png` plus `<id>.json`, written by
tools/pack_sprites.py: frames in a grid, and clips that name frame indices per direction.
This module turns that into pygame surfaces and plays a clip against the clock.

**The game must run without them.** The sheets are built from a .blend by a tool that needs
Blender; a fresh clone, or a milestone before the render has been done, simply has no
`chars/` folder. So `load()` returns None instead of raising, and whoever draws a character
checks for that - a missing animation must never be the reason the game will not start.

The pivot is the character's feet: draw a frame so that its pivot lands on the world
position, which is what `blit_pos` works out.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pygame

CHARS_DIR = Path(__file__).resolve().parents[1] / "assets" / "chars"
DIRS = ("down", "up", "left", "right")


class Clip:
    __slots__ = ("name", "fps", "loop", "frames")

    def __init__(self, name: str, fps: float, loop: bool, frames: dict[str, list[int]]):
        self.name, self.fps, self.loop, self.frames = name, float(fps), bool(loop), frames

    def count(self, direction: str = "down") -> int:
        return len(self.frames.get(direction) or self.frames.get("down") or ())

    @property
    def seconds(self) -> float:
        return self.count() / self.fps if self.fps > 0 else 0.0

    def index_at(self, t: float, direction: str = "down") -> int:
        """Which frame of the sheet this clip shows `t` seconds in."""
        ids = self.frames.get(direction) or self.frames.get("down") or [0]
        n = int(t * self.fps)
        n = n % len(ids) if self.loop else min(n, len(ids) - 1)
        return ids[n]


class CharSheet:
    def __init__(self, doc: dict, sheet: pygame.Surface):
        self.id = doc["id"]
        self.name_vi = doc.get("name_vi", doc["id"])
        self.fw, self.fh = int(doc["frame"]["w"]), int(doc["frame"]["h"])
        self.pivot = (float(doc["pivot"]["x"]), float(doc["pivot"]["y"]))
        self.cols = int(doc["cols"])
        self.total = int(doc["frames"])
        self.sheet = sheet
        self.clips = {name: Clip(name, c["fps"], c.get("loop", True), c["frames"])
                      for name, c in doc["clips"].items()}

    def frame(self, n: int) -> pygame.Surface:
        if not 0 <= n < self.total:
            raise IndexError(f"{self.id}: frame {n} of {self.total}")
        return self.sheet.subsurface(((n % self.cols) * self.fw, (n // self.cols) * self.fh,
                                      self.fw, self.fh))

    def at(self, clip: str, t: float, direction: str = "down") -> pygame.Surface:
        """The frame to draw for this clip at this moment, falling back to anything that
        exists rather than blowing up mid-draw."""
        c = self.clips.get(clip) or next(iter(self.clips.values()))
        return self.frame(c.index_at(t, direction))

    def blit_pos(self, x: float, y: float) -> tuple[int, int]:
        """Where to blit so the character's feet land on (x, y)."""
        return int(round(x - self.pivot[0])), int(round(y - self.pivot[1]))


@lru_cache(maxsize=16)
def load(char_id: str, chars_dir: Path | None = None) -> CharSheet | None:
    """The character, or None when it has not been rendered in this checkout."""
    folder = chars_dir or CHARS_DIR
    doc_path = folder / f"{char_id}.json"
    if not doc_path.exists():
        return None
    try:
        doc = json.loads(doc_path.read_text("utf-8"))
        png = folder / doc.get("sheet", f"{char_id}.png")
        if not png.exists():
            return None
        return CharSheet(doc, pygame.image.load(str(png)).convert_alpha())
    except (ValueError, KeyError, pygame.error):
        return None                      # a half-written sheet is not worth a crash


def available(chars_dir: Path | None = None) -> list[str]:
    folder = chars_dir or CHARS_DIR
    return sorted(p.stem for p in folder.glob("*.json")) if folder.exists() else []
