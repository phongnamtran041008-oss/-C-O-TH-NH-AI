"""Rebuild the fx_tien_ich batch (38 FX):
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_tien_ich/build.py [--only id[,id...]] [--jobs 2] [--no-proof]

Blender headless (fxt_run.py) builds scene -> .blend -> render -> pixelise -> pack for every id, then the four
contact sheets (art/preview/fx_tien_ich_{phi,roi,linh_can,khac}.png) and the three proofs (proof.py, pygame).
Output: client/assets/v2/fx/<id>.png + .json, art/blender/fx_tien_ich/<id>.blend (git-ignored)."""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe")
RAR = ("pham", "linh", "huyen", "dia", "thien")

ALL = (["phi_bong", "phi_vet", "phi_gio", "phi_may", "phi_cat_canh", "phi_ha_canh"]
       + ["roi_cot_" + r for r in RAR] + ["roi_vong_" + r for r in RAR] + ["roi_nhat"]
       + ["linh_can_%d" % i for i in range(1, 10)] + ["linh_can_tru_%d" % i for i in range(1, 10)]
       + ["trac_linh_thach", "thanh_tuu", "uy_ap"])


def run(ids, contact):
    cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "fxt_run.py"), "--", "--root", ROOT]
    if ids:
        cmd += ["--ids", ",".join(ids)]
    if contact:
        cmd += ["--contact"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in p.stdout.splitlines():
        if line.startswith(("BUILT", "CONTACT", "UNKNOWN")) or "Traceback" in line or "Error" in line:
            print(line, flush=True)
    if p.returncode:
        print(p.stdout[-2500:], p.stderr[-2500:])
        sys.exit(p.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated ids")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-proof", action="store_true")
    a = ap.parse_args()
    ids = a.only.split(",") if a.only else ALL
    jobs = max(1, min(a.jobs, 2))
    chunks = [ids[i::jobs] for i in range(jobs)] if len(ids) > 2 else [ids]
    with ThreadPoolExecutor(len(chunks)) as ex:
        list(ex.map(lambda c: run(c, False), [c for c in chunks if c]))
    run([], True)
    if not a.no_proof:
        subprocess.run([sys.executable, os.path.join(HERE, "proof.py")], check=False)


if __name__ == "__main__":
    main()
