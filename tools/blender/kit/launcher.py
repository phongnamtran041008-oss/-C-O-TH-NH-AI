"""Start headless Blender with the kit importable (runs in the game's venv, or anywhere).

    from kit import launcher
    launcher.run_blender("art/src/my_batch/scene.py", batch="my_batch", args=["--only", "x"])

Each call gets KIT_BATCH in its environment, so its temporary files go to
art/render/<batch>/_tmp_<pid>/: several batches (and several Blenders of one batch) can run
at the same time.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

from . import paths

BOOT = paths.KIT_DIR / "_boot.py"


def run_blender(script, batch: str, args: list[str] | None = None, blend=None,
                timeout: float | None = None, quiet: bool = False) -> int:
    """Run `script` inside `blender -b --factory-startup [blend]`. Returns the exit code
    (non-zero if the script raised). The script sees its own args in sys.argv[1:]."""
    script = Path(script)
    if not script.is_absolute():
        script = paths.ROOT / script
    cmd = [paths.BLENDER_EXE, "-b", "--factory-startup"]
    if blend:
        b = Path(blend)
        cmd.append(str(b if b.is_absolute() else paths.ROOT / b))
    cmd += ["--python-exit-code", "1", "--python", str(BOOT), "--", str(script)] + list(args or [])
    env = dict(os.environ, KIT_BATCH=batch, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    paths.render_dir(batch)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
                            cwd=str(paths.ROOT))
    log = paths.render_dir(batch) / f"blender_{os.getpid()}_{int(time.time() * 1000)}.log"
    with open(log, "wb") as fh:
        for line in proc.stdout:
            fh.write(line)
            text = line.decode("utf-8", "replace").rstrip()
            if not quiet and _interesting(text):
                print(text, flush=True)
    code = proc.wait(timeout=timeout)
    if code:
        print(f"blender exited with {code}; full log: {log}", file=sys.stderr)
    return code


def _interesting(text: str) -> bool:
    """Hide Blender's per-render chatter ("Saved: ...", "Fra:..."), keep everything else."""
    if not text:
        return False
    noise = ("Saved:", "Fra:", " render  ", "Time:", "Blender quit", "Read prefs",
             "| render", "EEVEE", "Read blend:", "Info: Saved")
    return not any(n in text for n in noise)


def finish(batch: str, out_dirs: list, preview_name: str | None = None) -> int:
    """After rendering: QC every output folder and write art/preview/<batch>.png.
    Returns the number of QC problems (0 = pass). Runs in the venv (needs pygame)."""
    from . import contact, qc
    problems = 0
    for d in out_dirs:
        problems += qc.report(Path(d) if Path(d).is_absolute() else paths.ROOT / d)
    out = paths.PREVIEW_DIR / f"{preview_name or batch}.png"
    contact.write([Path(d) if Path(d).is_absolute() else paths.ROOT / d for d in out_dirs], out,
                  title=batch)
    print(f"contact sheet: {out}")
    return problems
