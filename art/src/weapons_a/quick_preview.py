"""Quick EEVEE/Workbench look at the models (dev aid only; final art goes through the kit).

  blender -b --factory-startup --python quick_preview.py -- --blend-dir <dir> --out <dir> [--only ids] [--size 256]
"""
import bpy, sys, os, math
from mathutils import Vector


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    a = dict(zip(argv[0::2], argv[1::2]))
    bdir, out = a["--blend-dir"], a["--out"]
    size = int(a.get("--size", 256))
    ids = a["--only"].split(",") if "--only" in a else sorted(f[:-6] for f in os.listdir(bdir) if f.endswith(".blend"))
    os.makedirs(out, exist_ok=True)
    for wid in ids:
        bpy.ops.wm.open_mainfile(filepath=os.path.join(bdir, wid + ".blend"))
        sc = bpy.context.scene
        root = bpy.data.objects["SM_" + wid]
        root.rotation_euler = (0, math.radians(45), 0)
        bpy.context.view_layer.update()
        # bounds
        pts = []
        for o in root.children:
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        ctr = (mn + mx) / 2
        cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
        sc.collection.objects.link(cam)
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = max(mx.x - mn.x, mx.z - mn.z) * 1.15
        cam.location = (ctr.x, ctr.y - 5, ctr.z)
        cam.rotation_euler = (math.radians(90), 0, 0)
        sc.camera = cam
        w = bpy.data.worlds.new("w")
        w.use_nodes = True
        w.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.55, 1)
        w.node_tree.nodes["Background"].inputs[1].default_value = 0.9
        sc.world = w
        sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", 'SUN'))
        sc.collection.objects.link(sun)
        sun.data.energy = 3.0
        sun.rotation_euler = (math.radians(55), math.radians(-25), math.radians(-35))
        sc.render.resolution_x = sc.render.resolution_y = size
        sc.render.film_transparent = False
        w.node_tree.nodes["Background"].inputs[0].default_value = (0.04, 0.04, 0.06, 1)
        for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH'):
            try:
                sc.render.engine = eng
                break
            except TypeError:
                continue
        sc.view_settings.view_transform = 'Standard'
        sc.render.filepath = os.path.join(out, wid + ".png")
        bpy.ops.render.render(write_still=True)
        print("PREVIEW", wid, sc.render.engine)


main()
