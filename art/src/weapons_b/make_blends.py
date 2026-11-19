"""Run inside Blender: build the .blend of each weapon.  blender -b --factory-startup --python make_blends.py -- [ids]"""
import sys, os, bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import weapons
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "art", "blender", "weapons")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
todo = argv or weapons.ids()
os.makedirs(OUT, exist_ok=True)
bpy.context.preferences.filepaths.save_version = 0
for wid in todo:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    col = bpy.data.collections.new("COL_weapon_" + wid)
    sc.collection.children.link(col)
    obj = weapons.build(wid)
    col.objects.link(obj)
    obj["weapon_id"] = wid
    obj["name_vi"] = weapons.name_vi(*[wid.rsplit("_", 1)[0], int(wid.rsplit("_", 1)[1])])
    obj["grade"] = int(wid.rsplit("_", 1)[1])
    bpy.context.view_layer.update()
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    print("MODEL %s tris=%d mats=%d dims=%s" % (wid, tris, len(obj.data.materials), tuple(round(v, 3) for v in obj.dimensions)))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, wid + ".blend"), compress=True)
