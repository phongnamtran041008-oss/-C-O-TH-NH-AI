"""Rebuild the fx_chieu batch:  python art/src/fx_chieu/build.py [--only id[,id...]] [--jobs N] [--no-proof]

Runs Blender headless (scene -> .blend -> render -> pixelise -> pack) for every sheet of the batch, then the
contact sheets and the proofs in context (chieu_proof.py, pygame):
art/preview/fx_chieu_<group>.png, fx_chieu_proof.png, fx_chieu_proof_1x.png.  Use the venv python.
At most 2 Blender processes at once (other work shares this machine).
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe")
sys.path.insert(0, HERE)
from ids import ALL  # noqa: E402


def run(ids):
    cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "chieu_run.py"), "--", "--root", ROOT,
           "--ids", ",".join(ids)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = True
    for line in p.stdout.splitlines():
        if line.startswith("BUILT") or "Traceback" in line or "Error" in line:
            print(line, flush=True)
    if p.returncode or "Traceback" in p.stdout or "Traceback" in p.stderr:
        print(p.stdout[-4000:], p.stderr[-3000:])
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated ids")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-proof", action="store_true")
    a = ap.parse_args()
    ids = a.only.split(",") if a.only else list(ALL)
    unknown = [i for i in ids if i not in ALL]
    if unknown:
        sys.exit("unknown ids: %s" % ", ".join(unknown))
    jobs = max(1, min(a.jobs, 2, len(ids)))
    chunks = [ids[i::jobs] for i in range(jobs)]
    with ThreadPoolExecutor(jobs) as ex:
        oks = list(ex.map(run, chunks))
    if not a.no_proof:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        subprocess.run([sys.executable, os.path.join(HERE, "chieu_proof.py")], check=True, env=env)
    if not all(oks):
        sys.exit(1)


if __name__ == "__main__":
    main()
