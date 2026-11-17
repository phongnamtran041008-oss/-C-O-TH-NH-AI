"""M8: the half of the Blender pipeline that does not need Blender.

Rendering needs Blender, but packing the frames into a sheet and judging their quality does
not - and those are the parts that decide whether a character walks properly in the game. So
these tests draw their own "renders" (a stick figure standing on a known ground point, the
way the camera would leave it), pack them, and then break them on purpose to prove the
quality checks of plan 7.3 actually catch each fault.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pygame
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import pack_sprites  # noqa: E402
import sprite_qc  # noqa: E402

RENDER_PX, FRAME_PX = 256, 64
PIVOT = (128, 232)          # where the camera puts the feet, in rendered pixels
CLIPS = {"idle": {"fps": 6, "loop": True, "count": 2},
         "walk": {"fps": 10, "loop": True, "count": 4},
         "slash": {"fps": 12, "loop": False, "count": 3}}


def draw_figure(bob: int = 0, lean: int = 0) -> pygame.Surface:
    """A figure standing on PIVOT: the feet never move, the rest may."""
    s = pygame.Surface((RENDER_PX, RENDER_PX), pygame.SRCALPHA)
    px, py = PIVOT
    body = (60, 50, 40, 255)
    pygame.draw.rect(s, body, (px - 10, py - 8, 20, 8))                 # feet, on the ground
    pygame.draw.rect(s, body, (px - 14, py - 80 + bob, 28, 72 - bob))   # body
    pygame.draw.circle(s, body, (px + lean, py - 96 + bob), 18)         # head
    pygame.draw.rect(s, body, (px + 12 + lean, py - 70 + bob, 30, 8))   # an arm that moves
    return s


def write_render(folder: Path, char_id: str = "thi_nhan", clips: dict | None = None) -> Path:
    """Write what tools/blender/render_character.py would write."""
    clips = clips or CLIPS
    folder.mkdir(parents=True, exist_ok=True)
    for clip, c in clips.items():
        for d in pack_sprites.DIRS:
            for n in range(int(c["count"])):
                bob = n % 2 if clip != "slash" else 0
                lean = (n - 1) * 2 if clip == "slash" else 0
                pygame.image.save(draw_figure(bob, lean), str(folder / f"{clip}_{d}_{n:04d}.png"))
    (folder / "render.json").write_text(json.dumps({
        "id": char_id, "name_vi": "Thi Nhân", "source": "test", "render_px": RENDER_PX,
        "frame_px": FRAME_PX, "pivot_px": list(PIVOT), "dirs": list(pack_sprites.DIRS),
        "clips": clips}, ensure_ascii=False), "utf-8")
    return folder


@pytest.fixture
def packed(tmp_path):
    """One character rendered, packed, and ready to be judged."""
    out = tmp_path / "chars"
    doc = pack_sprites.pack(write_render(tmp_path / "render" / "thi_nhan"), out)
    return out, doc


# ------------------------------------------------------------------ packing
def test_packing_lays_out_every_frame_and_scales_the_pivot(packed):
    out, doc = packed
    frames = sum(int(c["count"]) for c in CLIPS.values()) * len(pack_sprites.DIRS)
    assert doc["frames"] == frames == 36
    assert doc["frame"] == {"w": FRAME_PX, "h": FRAME_PX}
    # the pivot came from the camera and is scaled by the same factor as the pixels
    assert doc["pivot"] == {"x": PIVOT[0] / 4, "y": PIVOT[1] / 4} == {"x": 32.0, "y": 58.0}
    sheet = pygame.image.load(str(out / doc["sheet"])).convert_alpha()
    rows = -(-doc["frames"] // doc["cols"])
    assert sheet.get_size() == (doc["cols"] * FRAME_PX, rows * FRAME_PX)
    for clip, c in doc["clips"].items():
        assert c["fps"] == CLIPS[clip]["fps"] and c["loop"] == CLIPS[clip]["loop"]
        assert sorted(c["frames"]) == sorted(pack_sprites.DIRS)
        for ids in c["frames"].values():
            assert len(ids) == CLIPS[clip]["count"]
    everything = [i for c in doc["clips"].values() for ids in c["frames"].values() for i in ids]
    assert sorted(everything) == list(range(frames)), "a frame is packed twice or not at all"


def test_packing_refuses_a_render_it_cannot_scale_cleanly(tmp_path):
    folder = write_render(tmp_path / "render" / "x")
    meta = json.loads((folder / "render.json").read_text("utf-8"))
    meta["frame_px"] = 48                      # 256 / 48 is not a whole number
    (folder / "render.json").write_text(json.dumps(meta), "utf-8")
    with pytest.raises(pack_sprites.PackError, match="whole multiple"):
        pack_sprites.pack(folder, tmp_path / "chars")


def test_packing_says_which_frame_is_missing(tmp_path):
    folder = write_render(tmp_path / "render" / "x")
    (folder / "walk_left_0002.png").unlink()
    with pytest.raises(pack_sprites.PackError, match="walk_left_0002.png is missing"):
        pack_sprites.pack(folder, tmp_path / "chars")


# ------------------------------------------------------------------ the quality checks (7.3)
def test_a_good_character_passes_every_check(packed):
    out, doc = packed
    assert sprite_qc.check_character(out / f"{doc['id']}.json") == []
    assert sprite_qc.check_all(out) == []


def _repack(out: Path, doc: dict, edit) -> list[str]:
    """Edit the packed sheet in place, then judge it again."""
    png = out / doc["sheet"]
    sheet = pygame.image.load(str(png)).convert_alpha()
    edit(sheet, doc)
    pygame.image.save(sheet, str(png))
    return sprite_qc.check_character(out / f"{doc['id']}.json")


def test_a_cut_off_frame_is_caught(packed):
    out, doc = packed

    def cut(sheet, doc):                       # paint over the frame's left edge
        pygame.draw.rect(sheet, (0, 0, 0, 255), (0, 20, 2, 20))
    problems = _repack(out, doc, cut)
    assert any("cut off" in p for p in problems), problems


def test_an_opaque_background_is_caught(packed):
    out, doc = packed

    def fill(sheet, doc):                      # the render forgot a transparent film
        bg = pygame.Surface((FRAME_PX, FRAME_PX))
        bg.fill((120, 140, 160))
        bg.blit(sheet.subsurface((0, 0, FRAME_PX, FRAME_PX)), (0, 0))
        sheet.blit(bg, (0, 0))
    problems = _repack(out, doc, fill)
    assert any("not transparent" in p for p in problems), problems


def test_a_frame_that_slides_is_caught(packed):
    out, doc = packed

    def shift(sheet, doc):                     # move one frame sideways: the walk would skate
        f = sheet.subsurface((0, 0, FRAME_PX, FRAME_PX)).copy()
        sheet.fill((0, 0, 0, 0), (0, 0, FRAME_PX, FRAME_PX))
        sheet.blit(f, (12, 0), (0, 0, FRAME_PX - 12, FRAME_PX))
    problems = _repack(out, doc, shift)
    assert any("will slide" in p for p in problems), problems


def test_a_floating_frame_is_caught(packed):
    out, doc = packed

    def lift(sheet, doc):                      # lift one frame off the ground
        f = sheet.subsurface((0, 0, FRAME_PX, FRAME_PX)).copy()
        sheet.fill((0, 0, 0, 0), (0, 0, FRAME_PX, FRAME_PX))
        sheet.blit(f, (0, -10))
    problems = _repack(out, doc, lift)
    assert any("will float" in p for p in problems), problems


def test_an_empty_frame_is_caught(packed):
    out, doc = packed
    problems = _repack(out, doc, lambda sheet, d: sheet.fill((0, 0, 0, 0),
                                                             (0, 0, FRAME_PX, FRAME_PX)))
    assert any("nothing is drawn" in p for p in problems), problems


def test_a_frame_index_outside_the_sheet_is_caught(packed):
    out, doc = packed
    path = out / f"{doc['id']}.json"
    d = json.loads(path.read_text("utf-8"))
    d["clips"]["idle"]["frames"]["down"] = [999]
    path.write_text(json.dumps(d, ensure_ascii=False), "utf-8")
    problems = sprite_qc.check_character(path)
    assert any("outside the" in p for p in problems), problems


def test_a_clip_without_fps_is_caught(packed):
    out, doc = packed
    path = out / f"{doc['id']}.json"
    d = json.loads(path.read_text("utf-8"))
    d["clips"]["walk"]["fps"] = 0
    path.write_text(json.dumps(d, ensure_ascii=False), "utf-8")
    assert any("fps is" in p for p in sprite_qc.check_character(path)), path


def test_two_characters_must_share_one_frame_size(tmp_path):
    out = tmp_path / "chars"
    pack_sprites.pack(write_render(tmp_path / "r1" / "a", "a"), out)
    big = {k: dict(v) for k, v in CLIPS.items()}
    folder = write_render(tmp_path / "r2" / "b", "b", big)
    meta = json.loads((folder / "render.json").read_text("utf-8"))
    meta["frame_px"] = 32                      # half the height of the first character
    (folder / "render.json").write_text(json.dumps(meta), "utf-8")
    pack_sprites.pack(folder, out)
    problems = sprite_qc.check_all(out)
    assert any("do not share one frame size" in p for p in problems), problems
