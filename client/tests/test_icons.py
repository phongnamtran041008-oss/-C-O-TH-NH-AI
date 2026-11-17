"""M8: packing the item icons, and choosing which icon an item gets.

The icons are rendered from 3D models by a tool that needs Blender, so these tests draw
their own "renders" and pack those - the packing, the blank-icon guard and the rules that
map a game item to an icon are what the game depends on, and none of them need Blender.
The shipped sheet is checked too when this checkout has one.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pygame
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import pack_icons  # noqa: E402

from client.engine import icons  # noqa: E402


def write_render(folder: Path, names: list[tuple[str, str]], blank: str = "") -> Path:
    """What tools/blender/render_item.py leaves behind."""
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    for n, (kind, slug) in enumerate(names):
        surf = pygame.Surface((256, 256), pygame.SRCALPHA)
        if slug != blank:
            pygame.draw.rect(surf, (90 + n * 10, 70, 50, 255), (60, 40, 130, 180))
        pygame.image.save(surf, str(folder / f"{slug}.png"))
        out.append({"file": f"{slug}.png", "span_m": 1.0, "kind": kind, "slug": slug,
                    "title": slug.title(), "creator": "test", "licence": "CC0"})
    (folder / "items.json").write_text(json.dumps({"icons": out}, ensure_ascii=False), "utf-8")
    return folder


ITEMS = [("vu_khi", "kiem"), ("vu_khi", "dao"), ("trang_bi", "mu"), ("dan_duoc", "dan")]


def test_packing_lays_the_icons_out_and_indexes_them(tmp_path):
    src = write_render(tmp_path / "render", ITEMS)
    doc = pack_icons.pack(src, tmp_path / "icons", cell=32)
    assert doc["count"] == len(ITEMS) and doc["cell"] == 32
    assert sorted(doc["icons"]) == sorted({slug for _, slug in ITEMS})
    sheet = pygame.image.load(str(tmp_path / "icons" / doc["sheet"])).convert_alpha()
    rows = -(-doc["count"] // doc["cols"])
    assert sheet.get_size() == (doc["cols"] * 32, rows * 32)
    seen = [e["index"] for v in doc["icons"].values() for e in v]
    assert sorted(seen) == list(range(doc["count"])), "an icon is packed twice or not at all"


def test_several_models_can_share_one_name(tmp_path):
    src = write_render(tmp_path / "render", ITEMS + [("vu_khi", "kiem2")])
    # two files, one name: rename the second so both land under "kiem"
    index = json.loads((src / "items.json").read_text("utf-8"))
    index["icons"][-1]["slug"] = "kiem"
    (src / "items.json").write_text(json.dumps(index, ensure_ascii=False), "utf-8")
    doc = pack_icons.pack(src, tmp_path / "icons", cell=32)
    assert len(doc["icons"]["kiem"]) == 2, doc["icons"]["kiem"]


def test_a_blank_icon_is_refused(tmp_path):
    """A model that renders to nothing must not reach the game as an empty square."""
    src = write_render(tmp_path / "render", ITEMS, blank="mu")
    with pytest.raises(pack_icons.IconError, match="blank"):
        pack_icons.pack(src, tmp_path / "icons", cell=32)


def test_packing_says_which_file_is_missing(tmp_path):
    src = write_render(tmp_path / "render", ITEMS)
    (src / "dao.png").unlink()
    with pytest.raises(pack_icons.IconError, match="dao.png is missing"):
        pack_icons.pack(src, tmp_path / "icons", cell=32)


# ------------------------------------------------------------------ choosing an icon
@pytest.mark.parametrize("row, want", [
    ({"item_id": "kiem_go_dao", "kind": "sword", "slot": "weapon"}, "kiem"),
    ({"item_id": "quat_giay", "kind": "fan", "slot": "weapon"}, "quat"),
    ({"item_id": "but_long_go", "kind": "brush", "slot": "weapon"}, "truong"),
    ({"item_id": "ao_truc_van", "slot": "body"}, "ao_giap"),
    ({"item_id": "non_la", "slot": "hat"}, "mu"),
    ({"item_id": "giay_co", "slot": "shoes"}, "giay"),
    ({"item_id": "nhan_ma_tran", "slot": "ring"}, "nhan"),
    ({"item_id": "ngoc_so_phuc", "slot": "jade"}, "day_chuyen"),
    ({"item_id": "hoi_huyet_dan", "kind": "pill"}, "dan"),
    ({"item_id": "bi_kip_thuy", "kind": "manual"}, "sach"),
    ({"item_id": "ghi_chu_phan_tu", "kind": "note"}, "cuon_thu"),
    ({"item_id": "manh_tap_hop", "kind": "material"}, "lo_dan"),
    ({"item_id": "muc_tinh", "kind": "material"}, None),       # no rule: keeps its old art
])
def test_an_item_gets_the_right_icon_name(row, want):
    assert icons.name_for(row) == want


def test_the_game_runs_without_any_icons(tmp_path, monkeypatch):
    """A checkout with no sheet must not raise anywhere: it just draws what it used to."""
    monkeypatch.setattr(icons, "ICON_DIR", tmp_path / "nothing_here")
    icons._doc.cache_clear(); icons.sheet.cache_clear(); icons.icon.cache_clear()
    try:
        assert icons.sheet() is None
        assert icons.names() == []
        assert icons.icon("kiem") is None
        assert icons.for_item({"item_id": "kiem_go_dao", "kind": "sword"}) is None
    finally:
        icons._doc.cache_clear(); icons.sheet.cache_clear(); icons.icon.cache_clear()


# ------------------------------------------------------------------ the sheet that ships
SHIPPED = (ROOT / "client" / "assets" / "icons" / "items.json").exists()


@pytest.mark.skipif(not SHIPPED, reason="this checkout has no rendered icons yet")
def test_every_shipped_icon_has_something_drawn_in_it():
    doc = json.loads((icons.ICON_DIR / "items.json").read_text("utf-8"))
    assert icons.sheet() is not None
    for name, entries in doc["icons"].items():
        for n, _entry in enumerate(entries):
            img = icons.icon(name, n)
            assert img is not None, name
            drawn = sum(1 for y in range(img.get_height()) for x in range(img.get_width())
                        if img.get_at((x, y))[3] > 8)
            assert drawn >= 12, f"{name}[{n}] is blank"


@pytest.mark.skipif(not SHIPPED, reason="this checkout has no rendered icons yet")
def test_every_cc_by_model_is_credited():
    """CC-BY is a legal duty, not a nicety: the credit must be in CREDITS.md."""
    doc = json.loads((icons.ICON_DIR / "items.json").read_text("utf-8"))
    credits = (ROOT / "CREDITS.md").read_text("utf-8")
    for name, entries in doc["icons"].items():
        for e in entries:
            if e["licence"] == "CC-BY":
                assert e["creator"] in credits, f"{name}: {e['title']} by {e['creator']}"
