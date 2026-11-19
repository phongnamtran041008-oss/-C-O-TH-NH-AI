"""Runs INSIDE headless Blender (started by build.py): builds every icon of the chosen
atlases, saves one .blend per atlas, then renders the 32x32 atlas through the kit.

args: [--only cong_phap,dan_duoc,linh_thao,trang_bi,misc]   atlases to (re)build, default all
      [--dev <ids>] [--outdir <rel dir>]   dev run: just those ids, written to another folder,
                                            no .blend (used while looking and fixing)
Other atlases in client/assets/v2/icons are never touched.
"""
import importlib
import os
import sys

import kit.api as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib  # noqa: E402

BLEND_DIR = "art/blender/icons"
ICON_DIR = "client/assets/v2/icons"
# atlas -> module (each has IDS and make(id) -> lib.W)
ATLASES = {"cong_phap": "books", "dan_duoc": "medicine", "linh_thao": "herbs",
           "trang_bi": "gear", "misc": "misc"}


def build_atlas(name, ids, out_dir, save_blend):
    mod = importlib.import_module(ATLASES[name])
    ids = ids or mod.IDS
    lib.clear_all()
    icons = []
    for i in ids:
        w = mod.make(i)
        root = w.build()
        ic = {"id": i, "objects": [root] + list(root.children), "name_vi": w.name_vi, "grade": w.grade}
        ic.update(w.pose)
        icons.append(ic)
    if save_blend:
        os.makedirs(kit.out_path(BLEND_DIR), exist_ok=True)
        kit.save_blend("%s/%s.blend" % (BLEND_DIR, name))
        print("BLEND", name, len(icons), "icons ->", BLEND_DIR)
    kit.render_icons(name, icons, out_dir, cols=8)


def main():
    args = kit.args()
    only = list(ATLASES)
    if "--only" in args:
        only = args[args.index("--only") + 1].split(",")
    dev = args[args.index("--dev") + 1].split(",") if "--dev" in args else None
    out_dir = args[args.index("--outdir") + 1] if "--outdir" in args else ICON_DIR
    for name in only:
        ids = [i for i in dev if i in importlib.import_module(ATLASES[name]).IDS] if dev else None
        if dev and not ids:
            continue
        build_atlas(name, ids, out_dir, save_blend=not dev)


main()
