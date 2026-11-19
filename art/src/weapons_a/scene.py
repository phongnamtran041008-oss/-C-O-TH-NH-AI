"""Runs INSIDE headless Blender (started by build.py): builds the 32 weapons, saves one .blend
per weapon, then renders the icon atlas through the kit.

args: [--only kiem_3,dao_5]   (blend files only for the ids given; atlas always has all 32,
      unless --only is given, then the atlas holds just those)
"""
import os
import sys

import kit.api as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import models  # noqa: E402

BLEND_DIR = "art/blender/weapons"
ICON_DIR = "client/assets/v2/icons"


def main():
    args = kit.args()
    only = models.ALL_IDS
    if "--only" in args:
        only = args[args.index("--only") + 1].split(",")
    os.makedirs(kit.out_path(BLEND_DIR), exist_ok=True)
    # 1. one .blend per weapon (saved before any render, the kit edits materials in memory)
    for wid in only:
        models.build_one(wid, str(kit.out_path(BLEND_DIR)))
    # 2. everything in one scene for the atlas
    models.clear_all()
    icons = []
    for wid in only:
        root = models.make(wid)
        icons.append({"id": wid, "objects": [root] + list(root.children),
                      "name_vi": root["name_vi"], "grade": int(root["grade"]),
                      "ppm": None})
    for ic in icons:
        ic.pop("ppm")
    kit.render_icons("weapons_a", icons, ICON_DIR, cols=8)


main()
