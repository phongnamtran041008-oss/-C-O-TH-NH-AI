"""Packers: finished frames (numpy RGBA) -> the files the game reads (docs/ART_PIPELINE.md 4)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from . import png

DIR_ORDER = ("down", "left", "up", "right")


def _write_json(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", "utf-8", newline="\n")


def grid(frames: list[np.ndarray], cols: int) -> np.ndarray:
    h, w = frames[0].shape[:2]
    rows = max(1, -(-len(frames) // cols))
    sheet = np.zeros((rows * h, cols * w, 4), np.uint8)
    for i, f in enumerate(frames):
        r, c = divmod(i, cols)
        sheet[r * h:(r + 1) * h, c * w:(c + 1) * w] = f
    return sheet


def save_png(path: Path, img: np.ndarray) -> None:
    png.write(path, img.shape[1], img.shape[0], np.ascontiguousarray(img))


def pack_animated(out_dir, asset_id: str, frames: list[np.ndarray], clips: dict, frame_wh,
                  pivot, name_vi: str | None = None, events: dict | None = None,
                  cols: int = 16, extra: dict | None = None) -> dict:
    """clips: {clip: {"fps", "loop", "frames": {dir: [indices]}}} in sheet order."""
    out_dir = Path(out_dir)
    cols = min(cols, max(1, len(frames)))
    save_png(out_dir / f"{asset_id}.png", grid(frames, cols))
    doc = {"id": asset_id, "name_vi": name_vi or asset_id,
           "frame": {"w": int(frame_wh[0]), "h": int(frame_wh[1])},
           "pivot": {"x": int(pivot[0]), "y": int(pivot[1])},
           "sheet": f"{asset_id}.png", "cols": cols, "frames": len(frames),
           "clips": clips, "events": events or {}}
    if extra:
        doc.update(extra)
    _write_json(out_dir / f"{asset_id}.json", doc)
    return doc


def pack_fx(out_dir, fx_id: str, frames: list[np.ndarray], size, pivot, fps: float, loop: bool,
            blend: str, ground: bool, cols: int = 8, extra: dict | None = None) -> dict:
    out_dir = Path(out_dir)
    cols = min(cols, len(frames))
    save_png(out_dir / f"{fx_id}.png", grid(frames, cols))
    doc = {"id": fx_id, "frame": {"w": int(size[0]), "h": int(size[1])},
           "pivot": {"x": int(pivot[0]), "y": int(pivot[1])}, "sheet": f"{fx_id}.png",
           "cols": cols, "frames": len(frames), "fps": fps, "loop": bool(loop),
           "blend": blend, "ground": bool(ground)}
    if extra:
        doc.update(extra)
    _write_json(out_dir / f"{fx_id}.json", doc)
    return doc


def pack_icons(out_dir, set_name: str, cells: list[np.ndarray], icons: dict, cell: int = 32,
               cols: int = 8) -> dict:
    """icons: {id: {"index", "name_vi", "grade"}} (index = position in `cells`)."""
    out_dir = Path(out_dir)
    cols = min(cols, max(1, len(cells)))
    save_png(out_dir / f"{set_name}.png", grid(cells, cols))
    doc = {"sheet": f"{set_name}.png", "cell": cell, "cols": cols, "icons": icons}
    _write_json(out_dir / f"{set_name}.json", doc)
    return doc


def pack_tiles(out_dir, region: str, tiles: list[np.ndarray], names: dict, cols: int = 8,
               extra: dict | None = None) -> dict:
    out_dir = Path(out_dir)
    cols = min(cols, max(1, len(tiles)))
    save_png(out_dir / f"{region}.png", grid(tiles, cols))
    doc = {"sheet": f"{region}.png", "tile": 16, "cols": cols, "tiles": names}
    if extra:
        doc.update(extra)
    _write_json(out_dir / f"{region}.json", doc)
    return doc


def shelf_pack(sizes: list[tuple[int, int]], width: int = 256, pad: int = 1):
    """Simple shelf packing, tallest first. Returns ([(x, y)], atlas_w, atlas_h)."""
    width = max(width, max(w for w, _ in sizes) + 2 * pad)
    order = sorted(range(len(sizes)), key=lambda i: (-sizes[i][1], -sizes[i][0], i))
    pos = [None] * len(sizes)
    x = y = pad
    shelf = 0
    for i in order:
        w, h = sizes[i]
        if x + w + pad > width:
            x, y, shelf = pad, y + shelf + pad, 0
        pos[i] = (x, y)
        x += w + pad
        shelf = max(shelf, h)
    return pos, width, y + shelf + pad


def pack_props(out_dir, region: str, props: list[dict]) -> dict:
    """props: [{"name", "frames": [rgba...] (same size), "pivot": (px, py), "solid"}].
    Frames of one prop sit side by side; rect covers frame 0, the others follow at +w."""
    out_dir = Path(out_dir)
    sizes = [(p["frames"][0].shape[1] * len(p["frames"]), p["frames"][0].shape[0]) for p in props]
    pos, W, H = shelf_pack(sizes)
    atlas = np.zeros((H, W, 4), np.uint8)
    doc_props = {}
    for p, (x, y) in zip(props, pos):
        fh, fw = p["frames"][0].shape[:2]
        for k, f in enumerate(p["frames"]):
            atlas[y:y + fh, x + k * fw:x + (k + 1) * fw] = f
        doc_props[p["name"]] = {"rect": [x, y, fw, fh], "pivot": [int(p["pivot"][0]), int(p["pivot"][1])],
                                "frames": len(p["frames"]), "solid": p.get("solid")}
    save_png(out_dir / f"{region}.png", atlas)
    doc = {"sheet": f"{region}.png", "props": doc_props}
    _write_json(out_dir / f"{region}.json", doc)
    return doc
