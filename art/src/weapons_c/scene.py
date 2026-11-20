"""Runs INSIDE headless Blender (started by build.py): builds the 48 weapons, saves one .blend
per weapon, then renders the icon atlas through the kit.

args: [--only kich_3,roi_5]   (.blends only for those ids, and an atlas holding only those)
"""
import os
import sys

import kit.api as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom    # noqa: E402
import models  # noqa: E402

BLEND_DIR = "art/blender/weapons"
ICON_DIR = "client/assets/v2/icons"

# icon pose per type: angle = lean of +Z toward the upper right, spin = turn about its own axis
POSE = {
    "kich": dict(angle=45, spin=12),
    "roi": dict(angle=40, spin=0),
    "am_khi": dict(angle=30, spin=0),
    "luan": dict(angle=20, spin=0),
    "phu": dict(angle=40, spin=10),
    "cam": dict(angle=90, spin=0, tilt=-25),
}


def main():
    args = kit.args()
    only = models.ALL_IDS
    if "--only" in args:
        only = [x for x in args[args.index("--only") + 1].split(",") if x]
    os.makedirs(kit.out_path(BLEND_DIR), exist_ok=True)
    # 1. one .blend per weapon (saved before any render: the kit edits materials in memory)
    for wid in only:
        models.build_one(wid, str(kit.out_path(BLEND_DIR)))
    # 2. everything in one scene for the atlas
    models.clear_all()
    icons = []
    for wid in only:
        root = models.make(wid)
        t = root["type"]
        icons.append({"id": wid, "objects": [root] + geom.visible_children(root),
                      "name_vi": root["name_vi"], "grade": int(root["grade"]), **POSE[t]})
    kit.render_icons("weapons_c", icons, ICON_DIR, cols=8)


main()
