"""Runs INSIDE headless Blender through the kit: builds the 32 weapons and renders the icon atlas.
Started by build.py (kit.launcher.run_blender).  The per-weapon .blend files are written by
make_blends.py (a separate, plain Blender run) so that rendering never touches saved files."""
import os
import sys

import bpy  # noqa: F401
import kit.api as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import weapons  # noqa: E402

# per-type pose in the icon: angle = tilt of +Z from vertical, spin = turn about the weapon's own axis
POSE = {
    "truong": dict(angle=45, spin=20),
    "cung": dict(angle=45, spin=10),
    "phien": dict(angle=30, spin=0),
    "ho_lo": dict(angle=0, spin=20),
}

kit.clear_scene()
icons = []
for t in weapons.TYPES:
    for g in range(1, 9):
        wid = "%s_%d" % (t, g)
        obj = weapons.build(wid)
        bpy.context.scene.collection.objects.link(obj)
        icons.append(dict(id=wid, objects=obj, name_vi=weapons.name_vi(t, g), grade=g, **POSE[t]))

doc = kit.render_icons("weapons_b", icons, "client/assets/v2/icons")
kit.log("icons done: %d" % len(doc["icons"]))
