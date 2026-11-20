"""Runs inside Blender:  blender -b --factory-startup --python chieu_run.py -- --root <repo> --ids a,b
Builds each fx_chieu scene, saves art/blender/fx_chieu/<id>.blend, renders (EEVEE, 6x) to art/render/fx_chieu/<id>/,
pixelises + palette-snaps (chieu_post) and packs client/assets/v2/fx/<id>.png/.json."""
import os
import sys
import time

sys.dont_write_bytecode = True      # no __pycache__ in art/src/fx or art/src/fx_kiem (other batches own them)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "fx"))
sys.path.insert(2, os.path.join(HERE, "..", "fx_kiem"))
import bpy  # noqa: E402
import fx_chieu  # noqa: E402
import chieu_post  # noqa: E402


def arg(name, default=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if name in a:
        i = a.index(name)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else True
    return default


ROOT = arg("--root")
OUT = os.path.join(ROOT, "client", "assets", "v2", "fx")
BLEND = os.path.join(ROOT, "art", "blender", "fx_chieu")
RENDER = os.path.join(ROOT, "art", "render", "fx_chieu")


def build_one(id):
    t0 = time.time()
    fx = fx_chieu.make(id)
    os.makedirs(BLEND, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BLEND, id + ".blend"), compress=True)
    paths = fx.render(os.path.join(RENDER, id))
    bad = chieu_post.pack(fx, paths, OUT)
    print("BUILT %s %d frames in %.1fs%s" % (id, fx.N, time.time() - t0, ("  WARN " + ",".join(bad)) if bad else ""),
          flush=True)


if __name__ == "__main__":
    ids = arg("--ids")
    if ids and ids is not True:
        for id in ids.split(","):
            build_one(id)
