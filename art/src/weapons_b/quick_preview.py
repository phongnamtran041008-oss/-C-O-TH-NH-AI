"""Quick Workbench look-check (NOT the final render - the final look comes only from the kit).
blender -b --factory-startup --python quick_preview.py -- out.png [ids] """
import sys, os, math, bpy, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import weapons
argv = sys.argv[sys.argv.index("--") + 1:]
out = os.path.abspath(argv[0]); todo = argv[1:] or weapons.ids()
S = 256
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x = sc.render.resolution_y = S
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "MATERIAL"
sc.display.shading.show_object_outline = True
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("w"); sc.world.color = (0.03, 0.03, 0.05)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam)
cam.data.type = "ORTHO"; cam.data.ortho_scale = float(os.environ.get("QP_SCALE", 1.45))
cam.location = (float(os.environ.get("QP_X", 0.2)), -5, float(os.environ.get("QP_Z", 0.35))); cam.rotation_euler = (math.pi / 2, 0, 0)
sc.camera = cam
tiles = {}
for wid in todo:
    obj = weapons.build(wid); sc.collection.objects.link(obj)
    obj.rotation_euler = (0, math.radians(45), 0)
    sc.render.filepath = os.path.join(os.path.dirname(out), "_q_%s.png" % wid)
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(sc.render.filepath)
    a = np.array(img.pixels[:]).reshape(S, S, 4)
    tiles[wid] = a
    bpy.data.images.remove(img); os.remove(sc.render.filepath)
    bpy.data.objects.remove(obj)
types = ["truong", "cung", "phien", "ho_lo"]
sheet = np.zeros((8 * S, 4 * S, 4)); sheet[..., 3] = 1
for ci, t in enumerate(types):
    for g in range(1, 9):
        w = "%s_%d" % (t, g)
        if w in tiles:
            sheet[(8 - g) * S:(9 - g) * S, ci * S:(ci + 1) * S] = tiles[w]  # y flipped
img = bpy.data.images.new("sheet", 4 * S, 8 * S, alpha=True)
img.pixels = sheet.ravel().tolist()
img.filepath_raw = out; img.file_format = "PNG"; img.save()
print("WROTE", out)
