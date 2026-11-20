"""Rebuild the fx_kiem batch:  python art/src/fx_kiem/build.py [--only id[,id...]] [--jobs N] [--no-proof]

Runs Blender headless (scene -> .blend -> render -> pixelise -> pack) for every sheet of the batch, then the
four contact sheets (art/preview/fx_kiem_khi.png, fx_kiem_song.png, fx_kiem_no_ngan.png, fx_kiem_families.png)
and the proof on the characters (art/preview/fx_kiem_on_char.png).  Use the venv python.
At most 2 Blender processes at once by default (other work shares this machine).
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe")

ALL = ([f"kiem_khi_{t}" for t in range(1, 11)] + [f"kiem_song_{t}" for t in range(2, 11)]
       + [f"kiem_no_{g}" for g in range(1, 5)] + [f"kiem_ngan_{k}" for k in range(1, 4)]
       + [f"{f}_{g}" for f in ("thuong_dam", "chuy_chan", "cung_ten", "phap_dan") for g in range(1, 5)])


def run(ids, contact):
    cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "kiem_run.py"), "--", "--root", ROOT]
    if ids:
        cmd += ["--ids", ",".join(ids)]
    if contact:
        cmd += ["--contact"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = True
    for line in p.stdout.splitlines():
        if line.startswith(("BUILT", "CONTACT")) or "Traceback" in line or "Error" in line:
            print(line, flush=True)
    if p.returncode or "Traceback" in p.stdout or "Traceback" in p.stderr:
        print(p.stdout[-3000:], p.stderr[-3000:])
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated ids")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-proof", action="store_true")
    a = ap.parse_args()
    ids = a.only.split(",") if a.only else ALL
    unknown = [i for i in ids if i not in ALL]
    if unknown:
        sys.exit("unknown ids: %s" % ", ".join(unknown))
    jobs = max(1, min(a.jobs, 2, len(ids)))
    chunks = [ids[i::jobs] for i in range(jobs)]
    with ThreadPoolExecutor(jobs) as ex:
        oks = list(ex.map(lambda c: run(c, False), chunks))
    oks.append(run([], True))
    if not a.no_proof:
        subprocess.run([sys.executable, os.path.join(HERE, "kiem_proof.py")], check=True)
    if not all(oks):
        sys.exit(1)


if __name__ == "__main__":
    main()
