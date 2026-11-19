"""Started by kit.launcher inside headless Blender: makes `import kit` work, then runs the
batch's script with sys.argv = [script, *its args]. Not for direct use."""
import os
import runpy
import sys
import traceback
from pathlib import Path

KIT_PARENT = str(Path(__file__).resolve().parents[1])     # tools/blender
if KIT_PARENT not in sys.path:
    sys.path.insert(0, KIT_PARENT)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    print("kit/_boot.py: no script given", file=sys.stderr)
    sys.exit(2)
script, rest = argv[0], argv[1:]
script_dir = str(Path(script).resolve().parent)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
sys.argv = [script] + rest
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    sys.stdout.flush()
    os._exit(code)
except BaseException:
    traceback.print_exc()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(1)
sys.stdout.flush()
os._exit(0)
