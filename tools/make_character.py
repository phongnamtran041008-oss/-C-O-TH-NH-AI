#!/usr/bin/env python3
"""The whole character pipeline in one command (M8, kế hoạch 7.1).

    python tools/make_character.py                 # dao_si: build -> render -> pack -> check
    python tools/make_character.py --id dao_si --frame-px 32
    python tools/make_character.py --skip-build    # re-render the .blend you edited by hand

    build_character.py  ->  art/blender/<id>.blend
    render_character.py ->  art/render/<id>/*.png + render.json
    pack_sprites.py     ->  client/assets/chars/<id>.png + .json
    sprite_qc.py        ->  pass or a list of what is wrong

Only the first two steps need Blender. Where it is: `$KVTT_BLENDER`, else `blender` on PATH,
else the usual Windows spots. Blender is **not** needed to play the game or to run the test
suite - only to build a character - so this script says plainly where to point it rather
than failing somewhere deep inside a render.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

CANDIDATES = [
    Path(r"C:/Program Files/Blender Foundation"),
    Path(r"C:/Program Files (x86)/Blender Foundation"),
    Path("C:/"), Path("D:/"), Path("E:/"),
]


def find_blender(explicit: str = "") -> Path | None:
    for cand in (explicit, os.environ.get("KVTT_BLENDER", "")):
        if cand and Path(cand).exists():
            return Path(cand)
    on_path = shutil.which("blender")
    if on_path:
        return Path(on_path)
    for base in CANDIDATES:
        if not base.exists():
            continue
        direct = base / "blender.exe"
        if direct.exists():
            return direct
        try:
            for child in sorted(base.iterdir(), reverse=True):      # newest version first
                exe = child / "blender.exe"
                if exe.exists():
                    return exe
        except OSError:
            continue
    return None


def run_blender(blender: Path, args: list[str], blend: Path | None = None) -> int:
    cmd = [str(blender), "-b"]
    if blend is not None:
        cmd.append(str(blend))
    else:
        cmd.append("--factory-startup")
    cmd += ["--python", *args]
    print("$ " + " ".join(cmd))
    # Blender's own console output is long; let it through so a render failure is visible
    return subprocess.call(cmd, cwd=str(ROOT))


REALMS = ["luyen_khi", "truc_co", "ket_dan", "nguyen_anh",
          "hoa_than", "luyen_hu", "hop_the", "dai_thua"]
REALM_NAMES = {"luyen_khi": "Luyện Khí", "truc_co": "Trúc Cơ", "ket_dan": "Kết Đan",
               "nguyen_anh": "Nguyên Anh", "hoa_than": "Hóa Thần", "luyen_hu": "Luyện Hư",
               "hop_the": "Hợp Thể", "dai_thua": "Đại Thừa"}


def every_realm(argv: list[str]) -> int:
    """One character per cultivation realm (the author's eight looks), built in one run."""
    bad = 0
    for realm in REALMS:
        print(f"==== {REALM_NAMES[realm]} ({realm})")
        rc = main([*argv, "--id", f"dao_si_{realm}", "--outfit", realm,
                   "--name-vi", f"Đạo Sĩ {REALM_NAMES[realm]}"])
        bad += bool(rc)
    import sprite_qc                     # now that every one of them is rebuilt, judge the set
    problems = sprite_qc.check_all()
    for line in problems:
        print(f" - {line}")
    print(f"==== {len(REALMS) - bad}/{len(REALMS)} realms built; "
          f"the set as a whole: {'FAIL' if problems else 'OK'}")
    return 1 if (bad or problems) else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--id", default="dao_si")
    ap.add_argument("--outfit", default="", help="a realm's look (see build_character.OUTFITS)")
    ap.add_argument("--realms", action="store_true",
                    help="build one character per cultivation realm, all eight looks")
    ap.add_argument("--name-vi", default="Đạo Sĩ")
    ap.add_argument("--render-px", type=int, default=256)
    ap.add_argument("--frame-px", type=int, default=32)
    ap.add_argument("--blender", default="", help="path to blender.exe")
    ap.add_argument("--skip-build", action="store_true", help="keep the .blend as it is")
    args = ap.parse_args(argv)
    if args.realms:
        rest = [a for a in (argv or []) if a != "--realms"]
        return every_realm(rest)

    blend = ROOT / "art" / "blender" / f"{args.id}.blend"
    blender = find_blender(args.blender)
    if blender is None:
        print("make_character: cannot find Blender. Install it, or point me at it:\n"
              "  python tools/make_character.py --blender \"C:/Program Files/Blender "
              "Foundation/Blender 4.5/blender.exe\"\n"
              "  (or set KVTT_BLENDER)", file=sys.stderr)
        return 2
    print(f"blender: {blender}")

    if not args.skip_build:
        build_args = [str(ROOT / "tools/blender/build_character.py"), "--", "--id", args.id]
        if args.outfit:
            build_args += ["--outfit", args.outfit]
        rc = run_blender(blender, build_args)
        if rc or not blend.exists():
            print(f"make_character: building the .blend failed (exit {rc})", file=sys.stderr)
            return 1
    elif not blend.exists():
        print(f"make_character: {blend} does not exist, so there is nothing to render",
              file=sys.stderr)
        return 1

    rc = run_blender(blender, [str(ROOT / "tools/blender/render_character.py"), "--",
                               "--id", args.id, "--name-vi", args.name_vi,
                               "--render-px", str(args.render_px),
                               "--frame-px", str(args.frame_px)], blend=blend)
    if rc:
        print(f"make_character: the render failed (exit {rc})", file=sys.stderr)
        return 1

    import pack_sprites
    import sprite_qc
    try:
        doc = pack_sprites.pack(ROOT / "art" / "render" / args.id)
    except pack_sprites.PackError as e:
        print(f"make_character: {e}", file=sys.stderr)
        return 1
    print(f"packed {doc['id']}: {doc['frames']} frames, pivot "
          f"{doc['pivot']['x']},{doc['pivot']['y']}")
    # only this character: checking the whole folder here would report the characters that
    # a batch has not rebuilt yet, which reads as if this one were broken
    problems = sprite_qc.check_character(sprite_qc.CHARS_DIR / f"{doc['id']}.json")
    for line in problems:
        print(f" - {line}")
    print(f"sprite check ({doc['id']}): " + ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
