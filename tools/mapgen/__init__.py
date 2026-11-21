"""The map generator of Toán Tu Tiên, one module per map so several people can author lands at
the same time (docs/DAI_DIA_DO.md).

* ``builder.py``: ``MapBuilder`` (ground grid, objects, collision rectangles -> Tiled JSON);
* ``giant.py``: ``DaiDiaDo``, the toolkit for the giant lands (terrain painted in regions,
  roads, barriers with passes, camps, signposts, khu, poi, monster areas by band);
* ``lands/<zone>.py``: one map each. A module there defines ``ZONE`` (the map's file name,
  server/maps/<ZONE>.tmj) and ``build() -> dict`` (the Tiled map). It is found on its own: a new
  land is a new file and nothing else.

``tools/gen_maps.py`` is the entry point; it writes every map twice, byte-identical, to
client/assets/maps and server/maps.
"""
from __future__ import annotations

import importlib
import json
import pkgutil
from pathlib import Path

from .builder import ROOT

OUT_DIRS = (ROOT / "client" / "assets" / "maps", ROOT / "server" / "maps")
COMPACT_TILES = 20000   # a map with more tiles than this is written without indentation (size)


def land_modules() -> dict[str, object]:
    """ZONE -> module, for every module of tools/mapgen/lands (a name starting with _ is skipped)."""
    from . import lands
    out: dict[str, object] = {}
    for info in sorted(pkgutil.iter_modules(lands.__path__), key=lambda i: i.name):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{lands.__name__}.{info.name}")
        zone = getattr(mod, "ZONE", None)
        if not zone or not callable(getattr(mod, "build", None)):
            raise SystemExit(f"tools/mapgen/lands/{info.name}.py: needs ZONE and build()")
        if zone in out:
            raise SystemExit(f"two modules build map {zone}")
        out[zone] = mod
    return out


def encode(data: dict) -> bytes:
    """The bytes of a map file: LF on every OS; the giant maps compact."""
    if data["width"] * data["height"] > COMPACT_TILES:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")


def write(zone: str, data: dict) -> list[Path]:
    raw = encode(data)
    out = []
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{zone}.tmj").write_bytes(raw)
        out.append(d / f"{zone}.tmj")
    return out
