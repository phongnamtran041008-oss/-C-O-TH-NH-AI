"""Runs inside Blender:  blender -b --factory-startup --python fxt_run.py -- --ids a,b --root <repo>
Builds each FX scene of the fx_tien_ich batch, saves the .blend, renders, pixelises and packs the sheet
(art/src/fx/fxlib.py + fxpost.py, imported, not edited).  `--contact` (no ids) rebuilds the four contact sheets."""
import sys
import os
import importlib
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy                      # noqa: E402
import tilib                    # noqa: E402,F401  (puts art/src/fx on sys.path)
import fxpost                   # noqa: E402


def arg(name, default=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if name in a:
        i = a.index(name)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else True
    return default


ROOT = arg("--root")
OUT = os.path.join(ROOT, "client", "assets", "v2", "fx")
BLEND = os.path.join(ROOT, "art", "blender", "fx_tien_ich")
RENDER = os.path.join(ROOT, "art", "render", "fx_tien_ich")
PREVIEW = os.path.join(ROOT, "art", "preview")
MODS = ["ti_phi", "ti_roi", "ti_linh", "ti_khac"]


def groups():
    out = {}
    for m in MODS:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        out[m] = (mod, mod.all_ids())
    return out


def build_one(id, g):
    for m, (mod, ids) in g.items():
        if id in ids:
            t = time.time()
            fx = mod.make(id)
            os.makedirs(BLEND, exist_ok=True)
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BLEND, id + ".blend"), compress=True)
            paths = fx.render(os.path.join(RENDER, id))
            fxpost.pack(fx, paths, OUT)
            print("BUILT %s %d frames in %.1fs" % (id, fx.N, time.time() - t), flush=True)
            return
    print("UNKNOWN id", id)


SHEETS = {
    "fx_tien_ich_phi": ["phi_bong", "phi_vet", "phi_gio", "phi_may", "phi_cat_canh", "phi_ha_canh"],
    "fx_tien_ich_roi": ["roi_cot_%s" % r for r in ("pham", "linh", "huyen", "dia", "thien")]
    + ["roi_vong_%s" % r for r in ("pham", "linh", "huyen", "dia", "thien")] + ["roi_nhat"],
    "fx_tien_ich_linh_can": ["linh_can_%d" % i for i in range(1, 10)] + ["linh_can_tru_%d" % i for i in range(1, 10)],
    "fx_tien_ich_khac": ["trac_linh_thach", "thanh_tuu", "uy_ap"],
}


def contacts():
    for name, ids in SHEETS.items():
        fxpost.contact(OUT, ids, os.path.join(PREVIEW, name + ".png"), width=2400)
        print("CONTACT", name)


if __name__ == "__main__":
    g = groups()
    ids = arg("--ids")
    if ids and ids is not True:
        for id in ids.split(","):
            build_one(id, g)
    if arg("--contact"):
        contacts()
