#!/usr/bin/env python3
"""Generate the Tiled maps (.tmj, Tiled JSON 1.10) used by the client and the server.

    python tools/gen_maps.py                 every map
    python tools/gen_maps.py loan_so_coc     only the maps named (their ZONE)

Each map is one module of tools/mapgen/lands (ZONE + build()); the toolkit for the giant lands is
tools/mapgen/giant.py and the authoring guide docs/DAI_DIA_DO.md. Every map is written twice,
byte-identical, to client/assets/maps and server/maps; they open in the Tiled editor
(https://www.mapeditor.org) for a look, but the code is the source: regenerate, never hand-edit.
After a run, `git status` shows exactly the maps whose code changed; then check them with
`python tools/check_maps.py`.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import mapgen  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    want = list(sys.argv[1:] if argv is None else argv)
    mods = mapgen.land_modules()
    unknown = [z for z in want if z not in mods]
    if unknown:
        print("unknown map(s):", ", ".join(unknown), "- known:", ", ".join(sorted(mods)))
        return 2
    for zone, mod in mods.items():
        if want and zone not in want:
            continue
        for path in mapgen.write(zone, mod.build())[:1]:
            print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
