"""Rebuild the FX batch:  python art/src/fx/build.py [--only id[,id...]] [--jobs N]

Runs Blender headless (scene -> .blend -> render -> pixelise -> pack) for every FX, then the three
contact sheets.  Use the venv python.  Output: client/assets/v2/fx/<id>.png+.json,
art/blender/fx/<id>.blend, art/preview/fx_{combat,ground,realm}.png.
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe")
ELEMS = ["tho", "kim", "hoa", "moc", "thuy", "loi"]

ALL = ([f"{k}_{e}" for e in ELEMS for k in ("slash", "bolt", "burst")]
       + ["hit_spark", "hit_crit", "parry", "guard_break", "dust_step", "dash_trail", "heal", "linh_thuan",
          "pickup_glow", "chest_open", "capture_seal", "sword_trail"]
       + [f"tran_{i}" for i in range(1, 9)]
       + [f"warn_{s}_{p}" for s in ("circle", "cone", "line") for p in ("charge", "release")] + ["crack_ground"]
       + [f"aura_{r}_{l}" for r in ("luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua") for l in ("back", "front")]
       + ["dot_pha", "loi_kiep", "thang_cap"])


def run(ids, contact):
    cmd = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "fx_run.py"), "--", "--root", ROOT]
    if ids:
        cmd += ["--ids", ",".join(ids)]
    if contact:
        cmd += ["--contact"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith(("BUILT", "CONTACT", "UNKNOWN")) or "Traceback" in line or "Error" in line:
            print(line)
    if p.returncode:
        print(p.stdout[-2000:], p.stderr[-2000:])
        sys.exit(p.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated ids")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    ids = a.only.split(",") if a.only else ALL
    chunks = [ids[i::a.jobs] for i in range(a.jobs)] if len(ids) > 3 else [ids]
    with ThreadPoolExecutor(len(chunks)) as ex:
        list(ex.map(lambda c: run(c, False), [c for c in chunks if c]))
    run([], True)
    subprocess.run([sys.executable, os.path.join(HERE, "glow_sheets.py")], check=True)      # glow_<realm> from the character sheets


if __name__ == "__main__":
    main()
