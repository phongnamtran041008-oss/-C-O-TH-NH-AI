"""Runs inside Blender:  blender -b --factory-startup --python fx_run.py -- --ids a,b --root <repo>
Builds each FX scene, saves the .blend, renders the frames, pixelises and packs the sheet.
`--contact` (no ids) only rebuilds the three contact sheets from the packed output."""
import sys
import os
import importlib
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import fxlib
import fxpost


def arg(name, default=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if name in a:
        i = a.index(name)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else True
    return default


ROOT = arg("--root")
OUT = os.path.join(ROOT, "client", "assets", "v2", "fx")
BLEND = os.path.join(ROOT, "art", "blender", "fx")
RENDER = os.path.join(ROOT, "art", "render", "fx")
PREVIEW = os.path.join(ROOT, "art", "preview")

MODS = ["fx_combat", "fx_ground", "fx_realm", "fx_aura"]


def group_ids():
    out = {}
    for m in MODS:
        try:
            mod = importlib.import_module(m)
            out[m] = (mod, mod.all_ids())
        except ModuleNotFoundError:
            pass
    return out


def build_one(id, groups):
    for m, (mod, ids) in groups.items():
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


def contacts(groups):
    for key, name in (("fx_combat", "fx_combat"), ("fx_ground", "fx_ground"), ("fx_realm", "fx_realm"), ("fx_aura", "fx_aura")):
        if key in groups:
            fxpost.contact(OUT, groups[key][1], os.path.join(PREVIEW, name + ".png"),
                           width=2300 if key != "fx_ground" else 2400)
            print("CONTACT", name)
    if "fx_ground" in groups:
        fxpost.warn_on_ground(ROOT, OUT, os.path.join(PREVIEW, "fx_warn_on_ground.png"))
        print("CONTACT fx_warn_on_ground")


if __name__ == "__main__":
    groups = group_ids()
    ids = arg("--ids")
    if ids and ids is not True:
        for id in ids.split(","):
            build_one(id, groups)
    if arg("--contact"):
        contacts(groups)
