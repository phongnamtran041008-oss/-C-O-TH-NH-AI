"""The flying sword (ngự kiếm): phi_kiem_1..3, runs inside Blender (called by scene.py).

A broad flat sword lies under the character's feet at SOCKET_mount, pointing the way the
character faces, with a glowing edge and a short light trail streaming back. It is drawn
UNDER the character (no body holdout) and exists for the `fly` clip only (4 frames x 4 facings),
where the `mount` bone lifts it with the character's bob.

Modelled here in code, one function per grade:  1 spirit cyan (Truc Co and later),
2 gold flame, 3 cosmic violet.
"""
from __future__ import annotations

import json
import math

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

import kit.api as kit
from kit.scene import Cam

GRADES = {
    "phi_kiem_1": dict(name="Phi Kiếm Thanh Quang", body="#b9d4e4", body_ramp="steel", guard="#c9a24a",
                       glow="#5ae0f4", glow_ramp="spirit", strength=4.0, trail=3),
    "phi_kiem_2": dict(name="Phi Kiếm Hỏa Kim", body="#4a3226", body_ramp="earth", guard="#e6b83a",
                       glow="#ff9a2e", glow_ramp="flame", strength=4.0, trail=4),
    "phi_kiem_3": dict(name="Phi Kiếm Tinh Không", body="#4a2c8c", body_ramp="purple", guard="#e6b83a",
                       glow="#b57cff", glow_ramp="cosmic", strength=4.0, trail=5),
}


def srgb(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = h.lstrip("#")
    return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def mat(name, base, metal=0.0, emit=None, strength=0.0, **props):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value = (*base, 1.0)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = 0.4
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1.0)
        p.inputs["Emission Strength"].default_value = strength
    for k, v in props.items():
        m[k] = v
    return m


def new_obj(name, bm, material, parent, smooth=False):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = smooth
    o.parent = parent
    return o


# the 15 degree camera sees a flat blade as a 2 px line: bank it about its length so the
# blade shows (side view: width x sin(bank + 15 deg))
BANK = 48.0
SIZE = 1.45          # the sword is bigger than the hand weapons: the 96 px frame has room

# blade profile along +Z: (z, half width, half thickness)
PROFILE = [(-0.12, 0.050, 0.018), (-0.02, 0.076, 0.022), (0.18, 0.082, 0.022), (0.32, 0.070, 0.018),
           (0.40, 0.040, 0.010)]
TIP = 0.49


def width_at(z):
    pts = [(p[0], p[1]) for p in PROFILE] + [(TIP, 0.0)]
    for (z0, w0), (z1, w1) in zip(pts, pts[1:]):
        if z0 <= z <= z1:
            return w0 + (w1 - w0) * (z - z0) / (z1 - z0)
    return 0.0


def blade_mesh(name, material, parent):
    bm = bmesh.new()
    rings = []
    for z, w, t in PROFILE:
        rings.append([bm.verts.new(v) for v in ((-w, 0, z), (0, -t, z), (w, 0, z), (0, t, z))])
    tip = bm.verts.new((0, 0, TIP))
    for a, b in zip(rings, rings[1:]):
        for k in range(4):
            bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
    for k in range(4):
        bm.faces.new((rings[-1][k], rings[-1][(k + 1) % 4], tip))
    bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, material, parent)


def ribbon(name, material, parent, pts):
    """Flat strip through quads: pts = [(x0, x1, y, z), ...] (x0..x1 across, at height y)."""
    bm = bmesh.new()
    prev = None
    for x0, x1, y, z in pts:
        cur = (bm.verts.new((x0, y, z)), bm.verts.new((x1, y, z)))
        if prev:
            bm.faces.new((prev[0], prev[1], cur[1], cur[0]))
        prev = cur
    return new_obj(name, bm, material, parent)


def box(name, size, loc, material, parent):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(loc), verts=bm.verts)
    return new_obj(name, bm, material, parent)


def cyl(name, r, z0, z1, material, parent, seg=8):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Identity(3), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector((0, 0, (z0 + z1) / 2)), verts=bm.verts)
    return new_obj(name, bm, material, parent)


def build(sid, g):
    root = bpy.data.objects.new(f"SM_{sid}", None)
    bpy.context.scene.collection.objects.link(root)
    gl = srgb(g["glow"])
    m_body = mat(f"MAT_{sid}_body", srgb(g["body"]), metal=1.0, kit_ramp=g["body_ramp"])
    m_guard = mat(f"MAT_{sid}_guard", srgb(g["guard"]), metal=1.0)
    m_grip = mat(f"MAT_{sid}_grip", srgb("#3c5e9c" if sid != "phi_kiem_2" else "#94302a"))
    m_edge = mat(f"MAT_{sid}_edge", gl, emit=gl, strength=3.0, kit_glow=g["glow_ramp"],
                 kit_priority=2.5, kit_halo=1)
    m_trail = mat(f"MAT_{sid}_trail", gl, emit=gl, strength=2.4, kit_glow=g["glow_ramp"], kit_halo=0)
    blade_mesh(f"SM_{sid}_blade", m_body, root)
    # glowing edges (both sides) and a rune line down the middle
    for sx in (-1, 1):
        pts = []
        for z in [-0.10 + 0.04 * k for k in range(0, 14)] + [0.43]:
            w = width_at(z)
            if w > 0.004:
                pts.append((sx * (w - 0.015), sx * (w + 0.002), 0.006, z))
        ribbon(f"SM_{sid}_edge{sx}", m_edge, root, pts)
    ribbon(f"SM_{sid}_rune", m_edge, root, [(-0.008, 0.008, 0.026, z) for z in (0.0, 0.1, 0.2, 0.3)])
    box(f"SM_{sid}_guard", (0.2, 0.04, 0.035), (0, 0, -0.125), m_guard, root)
    cyl(f"SM_{sid}_grip", 0.018, -0.25, -0.13, m_grip, root)
    cyl(f"SM_{sid}_pommel", 0.027, -0.27, -0.24, m_guard, root, 6)
    # the trail: tapered streaks flowing back from the guard
    trails = []
    n = g["trail"]
    for k in range(n):
        x = (k - (n - 1) / 2) * (0.15 / max(1, n - 1))
        length = 0.27 - 0.08 * abs(k - (n - 1) / 2) / max(1.0, (n - 1) / 2) + (0.04 if k % 2 else 0.0)
        bm = bmesh.new()
        a = bm.verts.new((x - 0.016, -0.012, -0.16))
        b = bm.verts.new((x + 0.016, -0.012, -0.16))
        c = bm.verts.new((x, -0.012, -0.16 - length))
        bm.faces.new((a, b, c))
        trails.append(new_obj(f"SM_{sid}_trail{k}", bm, m_trail, root))
    root["name_vi"] = g["name"]
    return root, trails


def run(rig, socks, only, out, argv):
    ids = only or list(GRADES)
    scene = bpy.context.scene
    mount = socks["mount"]
    clips = {"fly": kit.PLAYER_CLIPS["fly"]}
    doc = json.loads(kit.out_path("client/assets/v2/chars/dao_si_luyen_khi.json").read_text("utf-8"))
    cam = Cam("ground", doc["frame"]["w"], doc["frame"]["h"], doc["render"]["ppm"],
              (doc["pivot"]["x"], doc["pivot"]["y"]), elevation=doc["render"].get("elevation", 35.0))
    fw, fh = doc["frame"]["w"], doc["frame"]["h"]
    import numpy as np
    for sid in ids:
        g = GRADES[sid]
        root, trails = build(sid, g)
        objs = [root] + list(root.children_recursive)

        def pose(i, scale=1.0):
            bpy.context.view_layer.update()
            pitch = (6.0 + 2.0 * math.sin(i * math.pi / 2)) * 1.0
            local = (Matrix.Translation((0, -0.035, 0.03)) @ Euler((math.radians(-pitch), 0, 0)).to_matrix().to_4x4()
                     @ Matrix.Rotation(math.radians(BANK), 4, "Z")
                     @ Matrix.Diagonal((scale * SIZE, scale * SIZE, scale * SIZE, 1.0)))
            turn = bpy.data.objects.get("KIT_TURN")
            inv = turn.matrix_world.inverted() if turn is not None else Matrix.Identity(4)
            return inv @ mount.matrix_world @ local

        def hook(clip, d, i):
            root.matrix_basis = pose(i, hook.scale)
            for k, t in enumerate(trails):          # the trail flickers from frame to frame
                f = (1.0, 0.8, 1.12, 0.92)[(i + k) % 4]
                t.scale = (1, 1, f)
                t.location = (0, 0, -0.16 * (1 - f))

        # shrink until it fits in all four facings and all four frames
        hook.scale = 1.0
        act = kit._assign_action(rig, "fly")
        times = kit._times(act, dict(frames=4, loop=True))
        pts = []
        for o in objs:
            if o.type == "MESH":
                v = np.empty(len(o.data.vertices) * 3, np.float32)
                o.data.vertices.foreach_get("co", v)
                m = np.array(o.matrix_local)
                pts.append(v.reshape(-1, 3) @ m[:3, :3].T + m[:3, 3])
        pts = np.concatenate(pts)
        best = 1.0
        for sc in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6):
            bad = 0.0
            for i, t in enumerate(times):
                kit._set_time(scene, t)
                m = np.array(pose(i, sc))
                w = pts @ m[:3, :3].T + m[:3, 3]
                for deg in kit.DIRS.values():
                    r = math.radians(deg)
                    c, s = math.cos(r), math.sin(r)
                    ww = np.stack([w[:, 0] * c - w[:, 1] * s, w[:, 0] * s + w[:, 1] * c, w[:, 2]], 1)
                    loc = np.array(cam.matrix.to_translation())
                    d = ww - loc
                    x = fw / 2 + d @ np.array(cam.right) * cam.ppm
                    y = fh / 2 - d @ np.array(cam.up) * cam.ppm
                    bad += (max(0, 2.5 - x.min()) + max(0, x.max() - (fw - 2.5))
                            + max(0, 2.5 - y.min()) + max(0, y.max() - (fh - 2.5)))
            if bad == 0:
                best = sc
                break
        else:
            best = 0.7
        hook.scale = best
        kit.log(f"{sid}: scale {best}")
        bpy.context.view_layer.update()
        kit.save_blend(f"art/blender/weapon_layers/{sid}.blend") if "--dev" not in argv and out.endswith("weapons") else None
        r = doc["render"]
        kit.render_animated(objs, sid, clips, out, name_vi=g["name"], kind="flying_sword", layer=True,
                            frame=(fw, fh), pivot=(doc["pivot"]["x"], doc["pivot"]["y"]), ppm=r["ppm"],
                            elevation=r.get("elevation", 35.0), snap=bool(r.get("snap_to")),
                            snap_to=r.get("snap_to", "head"), action_target=rig, holdout=[rig], on_frame=hook)
        for o in objs:
            bpy.data.objects.remove(o)
