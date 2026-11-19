"""Kit samples: build, render, pack, QC and contact sheet in one go.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/kit_samples/build.py [--only sword|figure|fx|tiles|prop]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher  # noqa: E402

BATCH = "kit_samples"
OUT = "client/assets/v2/_samples"


def main(argv):
    code = launcher.run_blender(Path(__file__).with_name("scene.py"), BATCH, argv)
    if code:
        return code
    problems = launcher.finish(BATCH, [OUT])
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
