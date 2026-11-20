"""Runs inside Blender:  blender -b --factory-startup --python kiem_run.py -- --root <repo> [--ids a,b] [--contact]
Builds each fx_kiem scene, saves art/blender/fx_kiem/<id>.blend, renders (EEVEE, 6x) to art/render/fx_kiem/<id>/,
pixelises + palette-snaps with art/src/fx/fxpost.py and packs client/assets/v2/fx/<id>.png/.json.
`--contact` writes the four contact sheets art/preview/fx_kiem_*.png."""
import os
import sys
import time

sys.dont_write_bytecode = True      # do not leave __pycache__ in art/src/fx (another batch owns it)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "fx"))
import bpy  # noqa: E402
import numpy as np  # noqa: E402
import fxpost  # noqa: E402  (shared, read only)
import fx_kiem  # noqa: E402
import kiem_post  # noqa: E402  (fxpost's additive pass, snapped to the light ramps only)


def arg(name, default=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if name in a:
        i = a.index(name)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else True
    return default


ROOT = arg("--root")
OUT = os.path.join(ROOT, "client", "assets", "v2", "fx")
BLEND = os.path.join(ROOT, "art", "blender", "fx_kiem")
RENDER = os.path.join(ROOT, "art", "render", "fx_kiem")
PREVIEW = os.path.join(ROOT, "art", "preview")


def edge_report(fx):
    """after packing: say if any drawn pixel touches the frame border (the design must keep a margin)."""
    meta, arr = fxpost.load_sheet(OUT, fx.id)
    px, cols = meta["frame"]["w"], meta["cols"]
    bad = []
    for i in range(meta["frames"]):
        r, c = divmod(i, cols)
        a = arr[r * px:(r + 1) * px, c * px:(c + 1) * px, 3]
        if a.max() == 0:
            bad.append("%d:empty" % i)
        elif a[0].any() or a[-1].any() or a[:, 0].any() or a[:, -1].any():
            bad.append("%d:edge" % i)
    return bad


def build_one(id):
    t0 = time.time()
    fx = fx_kiem.make(id)
    os.makedirs(BLEND, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BLEND, id + ".blend"), compress=True)
    paths = fx.render(os.path.join(RENDER, id))
    kiem_post.pack(fx, paths, OUT)
    bad = edge_report(fx)
    print("BUILT %s %d frames in %.1fs%s" % (id, fx.N, time.time() - t0, ("  WARN " + ",".join(bad)) if bad else ""), flush=True)


def contacts():
    ids = fx_kiem.all_ids()
    sheets = [
        ("fx_kiem_khi", [i for i in ids if i.startswith("kiem_khi_")]),
        ("fx_kiem_song", [i for i in ids if i.startswith("kiem_song_")]),
        ("fx_kiem_no_ngan", [i for i in ids if i.startswith(("kiem_no_", "kiem_ngan_"))]),
        ("fx_kiem_families", [i for i in ids if i.startswith(("thuong_dam_", "chuy_chan_", "cung_ten_", "phap_dan_"))]),
    ]
    for name, sel in sheets:
        # width=1: every sheet on its own row (tiers as rows, frames as columns)
        fxpost.contact(OUT, sel, os.path.join(PREVIEW, name + ".png"), width=1, zoom=3)
        print("CONTACT", name, flush=True)


if __name__ == "__main__":
    ids = arg("--ids")
    if ids and ids is not True:
        for id in ids.split(","):
            build_one(id)
    if arg("--contact"):
        contacts()
