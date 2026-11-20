"""Weapon layers: one command.

    python art/src/weapon_layers/build.py                       # all 64 + 3 flying swords, QC, previews
    python art/src/weapon_layers/build.py --only kiem_1,cung_3  # just those
    python art/src/weapon_layers/build.py --jobs 4              # several Blenders in parallel
    python art/src/weapon_layers/build.py --only kiem_1 --dev --clips idle,slash --dirs right
        # --dev: write to art/render/weapon_layers/dev (not the game folder), no QC / previews
    python art/src/weapon_layers/build.py --flying              # only phi_kiem_1..3

Run with the game's venv python. Needs the character sheets (client/assets/v2/chars).
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
from kit import launcher  # noqa: E402

BATCH = "weapon_layers"
SCENE = Path(__file__).with_name("scene.py")
TYPES = ("kiem", "dao", "thuong", "chuy", "truong", "cung", "phien", "ho_lo",
         "kich", "roi", "am_khi", "luan", "phu", "cam")     # the last six: WEAPONS_C (kỳ binh)
ALL = [f"{t}_{g}" for t in TYPES for g in range(1, 9)]
FLY = ["phi_kiem_1", "phi_kiem_2", "phi_kiem_3"]


def take(args, name, default=None, flag=False):
    if name in args:
        i = args.index(name)
        if flag:
            del args[i]
            return True
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return False if flag else default


def main(argv):
    only = take(argv, "--only")
    jobs = int(take(argv, "--jobs", 1))
    dev = take(argv, "--dev", flag=True)
    flying_only = take(argv, "--flying", flag=True)
    passthrough = []
    for k in ("--clips", "--dirs", "--char"):
        v = take(argv, k)
        if v:
            passthrough += [k, v]
    out = "art/render/weapon_layers/dev" if dev else "client/assets/v2/weapons"
    ids = [x for x in only.split(",") if x] if only else (FLY if flying_only else ALL + FLY)
    hand = [i for i in ids if not i.startswith("phi_kiem")]
    fly = [i for i in ids if i.startswith("phi_kiem")]
    t0 = time.time()
    code = 0
    runs = []
    if hand:
        groups = [hand[i::jobs] for i in range(min(jobs, len(hand)))]
        for g in groups:
            runs.append(["--only", ",".join(g), "--out", out] + passthrough)
    if fly:
        runs.append(["--flying", "--only", ",".join(fly), "--out", out])
    procs = []
    for r in runs:
        cmd = [sys.executable, str(Path(__file__)), "--_worker"] + r
        procs.append(subprocess.Popen(cmd))
        if jobs <= 1:
            code |= procs[-1].wait()
    for p in procs:
        code |= p.wait()
    print(f"blender work done in {time.time() - t0:.0f}s (exit {code})")
    if code == 0 and not dev:
        if not only:
            import preview
            preview.write_all_previews()
        from kit import qc
        code = 1 if qc.report(ROOT / "client" / "assets" / "v2" / "weapons") else 0
    return code


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--_worker":
        code = launcher.run_blender(SCENE, BATCH, sys.argv[2:], blend="art/blender/chars/rig_base.blend")
        sys.exit(code)
    sys.exit(main(sys.argv[1:]))
