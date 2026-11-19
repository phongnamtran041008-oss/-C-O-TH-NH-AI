"""Shared helpers for the WORLD_TILES batch. Runs inside Blender (headless).

Units: tile scenes are modelled in *pixel units* (a tile is 16 x 16 units, +Y = screen up,
+X = screen right, +Z = towards the camera, one render pixel at 6x = 1/6 unit).
Prop scenes are modelled in metres (1 unit = 1 m, pivot on the ground at the origin) and
rendered with the standard camera: orthographic, 35 degrees above the horizon, light from the
upper left; 1 m of height = 36 px, i.e. a 1.0 m player is 36 px tall.
"""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector, Matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RENDER_DIR = ROOT / "art" / "render" / "world_tiles"
BLEND_DIR = ROOT / "art" / "blender" / "world_tiles"

SS = 6                      # supersampling: render at 6x the target size, then scale down
T = 16.0                    # tile size in tile-scene units
PX_PER_M = 36.0             # prop scale: 1 m of height = 36 px on screen
CAM_ELEV = 35.0             # degrees above the horizon (props)

# --------------------------------------------------------------------------- palette
# Four steps per ramp: shadow / base / light / highlight (hard steps, no gradients).
RAMPS = {
    "grass":   ["#3E6B3A", "#5C9A47", "#86BF5A", "#B4DD7E"],
    "foliage": ["#3E6B3A", "#5C9A47", "#86BF5A", "#B4DD7E"],      # trees, bushes (kit ramp leaf)
    "grass_d": ["#1D4237", "#2E6A4B", "#43905A", "#6BB67A"],
    "jade":    ["#2A5F46", "#43916A", "#6FBF8C", "#A8E3B4"],
    "olive":   ["#475F26", "#7A9A36", "#A8C44C", "#D3E67A"],
    "blossom": ["#B5566F", "#E884A0", "#F7B3C6", "#FFE0E8"],
    "wood":    ["#4A2F1D", "#7A4E2C", "#A8733F", "#D19B5E"],
    "bark":    ["#2A1D18", "#4A3424", "#6B4A32", "#8E6A48"],
    "path":    ["#8E7650", "#B89F6E", "#D5C28F", "#EEDFB0"],
    "dirt":    ["#47301C", "#6B4828", "#8F6638", "#B08650"],
    "teal":    ["#1F6F6B", "#2F9A92", "#58C0B0", "#9FE0CF"],
    "steel":   ["#34405A", "#5D6E86", "#94A6BA", "#DBE6EF"],
    "gold":    ["#7A4C0E", "#B9821A", "#E6B83A", "#FFF0A0"],
    "earth":   ["#47392D", "#6C5A47", "#958065", "#BFAB8A"],
    "rock":    ["#4A4038", "#7C6E5E", "#A59886", "#CFC3AE"],
    "stone":   ["#454A54", "#767C86", "#A2A7AC", "#D0D2CE"],
    "slate":   ["#15172A", "#292D45", "#434A68", "#6A7194"],
    "water":   ["#2B5B88", "#4A86B5", "#79B4D8", "#C2E6F4"],
    "sand":    ["#B08F58", "#D6BC84", "#EAD6A0", "#F8EBC6"],
    "snow":    ["#8497BC", "#BCCBE4", "#E4ECF8", "#FFFFFF"],
    "basalt":  ["#171013", "#2B2024", "#483A3E", "#6C5B5E"],
    "lava":    ["#8A1F0F", "#D4401A", "#F28A2A", "#FFD95A"],
    "cloud":   ["#8794CC", "#BDC7EE", "#E7ECFC", "#FFFFFF"],
    "ink":     ["#0A0920", "#161440", "#27235E", "#4C3F9E"],
    "mist":    ["#5B45C8", "#8C6CFF", "#B9A2FF", "#E4D8FF"],
    "crys_c":  ["#256A98", "#3FB0D8", "#8DE6F2", "#E6FDFF"],
    "crys_v":  ["#43268A", "#8350CE", "#BE96F2", "#EEDDFF"],
    "glow_g":  ["#23925A", "#5FE088", "#B2FFB6", "#EFFFEF"],
    "glow_b":  ["#2A74C8", "#62BEFF", "#C0EEFF", "#F2FCFF"],
    "glow_p":  ["#B8409A", "#FF80C6", "#FFCCEA", "#FFF2FA"],
    "glow_y":  ["#C28418", "#FFD04A", "#FFEE9C", "#FFFBE0"],
    "shroom":  ["#80262A", "#C4443F", "#E8776A", "#FFC8B6"],
    "bone":    ["#5A5866", "#9894A2", "#CFCBD3", "#F6F4F7"],
    "paper":   ["#5A4630", "#C4AE84", "#EAD9B0", "#F5EAD0"],
    "cream":   ["#A58C6A", "#D6C39C", "#F0E4C6", "#FFF8E6"],
    "white":   ["#A5B1C8", "#DCE4F0", "#F6F9FD", "#FFFFFF"],
    "violet":  ["#43286F", "#7752B4", "#A586DE", "#D0BAF4"],
    "yellow":  ["#B88A18", "#F0C444", "#FFE47C", "#FFF6BE"],
    "red":     ["#7E2328", "#BC4749", "#E26E6A", "#F8A89C"],
}


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def palette_list() -> list[tuple[int, int, int]]:
    seen, out = set(), []
    for ramp in RAMPS.values():
        for h in ramp:
            c = hex_rgb(h)
            if c not in seen:
                seen.add(c)
                out.append(c)
    return out


def srgb_to_lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin_color(h: str, k: float = 1.0):
    r, g, b = (srgb_to_lin(v / 255.0) * k for v in hex_rgb(h))
    return (r, g, b, 1.0)


# --------------------------------------------------------------------------- scene
def reset() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for blk in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for b in list(blk):
            blk.remove(b)


DETAIL = 1.0                 # 1.6 for the 32 px tiles: smaller marks, more of them
KIT = False                  # True when rendering through tools/blender/kit (it reads kit_* material properties)

# my ramps -> the master palette ramps (art/palette.json); solid first, glow ramp second
KIT_SOLID = {"bone": "bone", "teal": "teal", "steel": "steel", "gold": "gold", "earth": "earth", "paper": "paper", "grass": "grass", "foliage": "leaf", "blossom": "pink", "grass_d": "jade", "jade": "jade", "olive": "leaf", "wood": "wood", "bark": "wood",
             "path": "earth", "dirt": "earth", "stone": "stone", "slate": "steel", "water": "blue", "sand": "earth",
             "snow": "bone", "basalt": "hair", "cloud": "bone", "ink": "purple", "mist": "purple", "shroom": "red",
             "cream": "paper", "white": "bone", "violet": "purple", "yellow": "gold", "red": "red", "rock": "earth",
             "crys_c": "blue", "crys_v": "purple", "glow_g": "leaf", "glow_b": "blue", "glow_p": "purple",
             "glow_y": "gold", "lava": "red"}
KIT_GLOW = {"mist": "cosmic", "crys_c": "spirit", "crys_v": "cosmic", "glow_g": "verdant", "glow_b": "ice",
            "glow_p": "cosmic", "glow_y": "holy", "lava": "flame", "white": "ice"}


_KP: dict = {}


def kit_color(ramp: str, step: int):
    """In kit mode a material's base colour is the master-palette entry it should snap to:
    step 0 -> shadow entry, 1 -> base, 2 -> light, 3 -> light (the kit adds the highlight itself)."""
    if not _KP:
        _KP.update(json.loads((ROOT / "art" / "palette.json").read_text("utf-8"))["ramps"])
    kr = KIT_SOLID.get(ramp)
    if kr is None:
        return None
    cols = _KP[kr]["colors"]
    return cols[min(step + 1, 3)]


def kit_or(kit_value, mine):
    return kit_value if KIT else mine


def lit(v: float) -> float:
    """Emission used only to brighten a part under my own lamp: the kit would read it as glow."""
    return 0.0 if KIT else v


_MATS: dict = {}
USED_RAMPS: set = set()      # ramps touched while one asset is being built (its quantiser palette)


def mat(ramp: str, step: int = 1, emit: float = 0.0, rough: float = 1.0, name: str | None = None,
        alpha: float = 1.0, prio: float = 0.0, extra: dict | None = None):
    """Ordinary Principled material (contract section 5). `emit` > 0 marks a glowing part."""
    USED_RAMPS.add(ramp)
    key = (ramp, step, round(emit, 2), alpha, prio, tuple(sorted((extra or {}).items())))
    if key in _MATS and _MATS[key].name in bpy.data.materials:
        return _MATS[key]
    m = bpy.data.materials.new(name or f"MAT_{ramp}_{step}" + (f"_glow" if emit else ""))
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    kc = kit_color(ramp, step) if KIT else None
    col = lin_color(kc if kc else RAMPS[ramp][step])
    bsdf.inputs["Base Color"].default_value = col
    bsdf.inputs["Roughness"].default_value = rough
    for k in ("Specular IOR Level", "Specular"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.0
    if emit > 0:
        bsdf.inputs["Emission Color"].default_value = col
        bsdf.inputs["Emission Strength"].default_value = emit
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
    m.diffuse_color = col
    if KIT:
        if emit > 0 and ramp in KIT_GLOW:
            m["kit_glow"] = KIT_GLOW[ramp]
        elif ramp in KIT_SOLID:
            m["kit_ramp"] = KIT_SOLID[ramp]
        if emit == 0:
            m["kit_glow"] = 0
        if prio:
            m["kit_priority"] = prio
        for k, v in (extra or {}).items():
            m[k] = v
    _MATS[key] = m
    return m


def collection(name: str):
    c = bpy.data.collections.new(f"COL_{name}")
    bpy.context.scene.collection.children.link(c)
    return c


def _link(obj, col):
    col.objects.link(obj)
    return obj


def mesh_obj(name: str, bm: bmesh.types.BMesh, material, col, smooth=False, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(f"SM_{name}")
    bm.to_mesh(me)
    bm.free()
    mats = material if isinstance(material, (list, tuple)) else [material]
    for m in mats:
        me.materials.append(m)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(f"SM_{name}", me)
    ob.location = loc
    return _link(ob, col)


# --------------------------------------------------------------------------- primitives
def box(col, name, c, size, material, rot_z=0.0, bevel=0.0, taper=1.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]
        v.co.y *= size[1]
        v.co.z *= size[2]
        if v.co.z > 0 and taper != 1.0:
            v.co.x *= taper
            v.co.y *= taper
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1, affect="EDGES")
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(rot_z, 3, "Z"))
    return mesh_obj(name, bm, material, col, loc=c)


def blob(col, name, c, size, material, seed=0, rough=0.18, subdiv=2, smooth=False, rot_z=0.0):
    """Lumpy ellipsoid: pebble, bush lump, crown puff, boulder."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    ph = [rnd.uniform(0, 6.28) for _ in range(6)]
    for v in bm.verts:
        p = v.co.copy()
        n = (math.sin(p.x * 2.1 + ph[0]) * math.sin(p.y * 2.3 + ph[1]) +
             math.sin(p.z * 2.7 + ph[2]) * math.sin(p.x * 1.7 + ph[3])) * 0.5
        k = 1.0 + rough * n
        v.co = Vector((p.x * size[0] * k, p.y * size[1] * k, p.z * size[2] * k))
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(rot_z, 3, "Z"))
    return mesh_obj(name, bm, material, col, smooth=smooth, loc=c)


def cyl(col, name, c, r0, r1, h, material, seg=8, smooth=False, tilt=(0.0, 0.0)):
    """Tapered cylinder standing on z = 0 of its own origin (r0 at the bottom, r1 at the top)."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r0, radius2=r1, depth=h)
    for v in bm.verts:
        v.co.z += h / 2
    if tilt != (0.0, 0.0):
        # shear the top sideways: tilt = (dx, dy) per unit height
        for v in bm.verts:
            v.co.x += tilt[0] * v.co.z
            v.co.y += tilt[1] * v.co.z
    return mesh_obj(name, bm, material, col, smooth=smooth, loc=c)


def cone(col, name, c, r, h, material, seg=7, smooth=False):
    return cyl(col, name, c, r, 0.0, h, material, seg=seg, smooth=smooth)


def tube(col, name, pts, radii, material, seg=6, smooth=True):
    """Tapered tube along a polyline (branches, vines, roots). pts: list of (x,y,z)."""
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(pts):
        p = Vector(p)
        if i < len(pts) - 1:
            d = (Vector(pts[i + 1]) - p).normalized()
        else:
            d = (p - Vector(pts[i - 1])).normalized()
        a = d.cross(Vector((0, 0, 1)))
        if a.length < 1e-4:
            a = Vector((1, 0, 0))
        a.normalize()
        b = d.cross(a).normalized()
        r = radii[i] if i < len(radii) else radii[-1]
        ring = [bm.verts.new(p + (a * math.cos(2 * math.pi * k / seg) + b * math.sin(2 * math.pi * k / seg)) * r)
                for k in range(seg)]
        rings.append(ring)
    for i in range(len(rings) - 1):
        for k in range(seg):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % seg], rings[i + 1][(k + 1) % seg], rings[i + 1][k]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_obj(name, bm, material, col, smooth=smooth)


def blade(col, name, base, tip, width, material, bend=0.0):
    """Two-sided tapered blade: base (x,y,z) -> tip (x,y,z), `width` at the base."""
    bx, by, bz = base
    tx, ty, tz = tip
    d = Vector((tx - bx, ty - by, 0.0))
    side = Vector((-d.y, d.x, 0.0))
    if side.length < 1e-6:
        side = Vector((1, 0, 0))
    side.normalize()
    bm = bmesh.new()
    a = bm.verts.new(Vector(base) + side * width / 2)
    b = bm.verts.new(Vector(base) - side * width / 2)
    mid = Vector(base).lerp(Vector(tip), 0.5) + Vector((0, 0, bend))
    ma = bm.verts.new(mid + side * width * 0.32)
    mb = bm.verts.new(mid - side * width * 0.32)
    t = bm.verts.new(tip)
    bm.faces.new((a, ma, mb, b))
    bm.faces.new((ma, t, mb))
    return mesh_obj(name, bm, material, col)


def grass_blade(col, base, tip, width, material):
    """A blade of grass for ground tiles. Through the kit it is a thin solid cone (a single quad can face away from
    the camera and vanish); in my own render a flat blade."""
    if not KIT:
        return blade(col, "blade", base, tip, width, material, bend=0.2)
    bx, by, bz = base
    h = max(tip[2] - bz, 0.5)
    return cyl(col, "blade", (bx, by, bz), width * 0.62, width * 0.12, h, material, seg=3,
               tilt=((tip[0] - bx) / h, (tip[1] - by) / h))


def plane(col, name, x0, y0, x1, y1, z, material):
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in ((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z))]
    bm.faces.new(vs)
    return mesh_obj(name, bm, material, col)


def poly_flat(col, name, pts, z, material, thick=0.0):
    """Flat polygon (ordered 2D points) at height z; optionally extruded upward by `thick`."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, y in pts]
    f = bm.faces.new(vs)
    if thick:
        r = bmesh.ops.extrude_face_region(bm, geom=[f])
        for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]:
            v.co.z += thick
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if not thick:
        bm.faces.ensure_lookup_table()
        if bm.faces[0].normal.z < 0:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
    return mesh_obj(name, bm, material, col)


def heightfield(col, name, x0, y0, x1, y1, n, z_fn, mat_fn, materials, smooth=False):
    """Grid surface. z_fn(x, y) -> height; mat_fn(x, y) -> material index of the face centred there."""
    bm = bmesh.new()
    nx = ny = n
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    grid = [[bm.verts.new((x0 + i * dx, y0 + j * dy, z_fn(x0 + i * dx, y0 + j * dy))) for i in range(nx + 1)]
            for j in range(ny + 1)]
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            f.material_index = mat_fn(x0 + (i + 0.5) * dx, y0 + (j + 0.5) * dy)
            f.smooth = smooth
    return mesh_obj(name, bm, materials, col, smooth=smooth)


def wraps(x: float, y: float, r: float, period: float = T):
    """Offsets at which a feature of radius r at (x, y) must also be drawn so the tile is seamless."""
    out = []
    for dx in (-period, 0.0, period):
        for dy in (-period, 0.0, period):
            if -r < x + dx < T + r and -r < y + dy < T + r:
                out.append((dx, dy))
    return out


def wraps_x(x: float, r: float, period: float = T):
    return [dx for dx in (-period, 0.0, period) if -r < x + dx < period + r]


def shear_z_into_y(objs, k=1.0):
    """Oblique game projection: raise = move up the screen. y' = y + k*z (applied to mesh data)."""
    for ob in objs:
        me = ob.data
        m = ob.matrix_basis.copy()
        for v in me.vertices:
            co = m @ v.co
            v.co = Vector((co.x, co.y + k * co.z, co.z))
        ob.matrix_basis = Matrix.Identity(4)
        me.update()


# --------------------------------------------------------------------------- render
def setup_render(px_w: int, px_h: int, transparent: bool, samples: int = 24):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = px_w, px_h
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.filter_size = 0.5
    try:
        sc.eevee.taa_render_samples = samples
    except Exception:
        pass
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.display_settings.display_device = "sRGB"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    w = sc.world
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = AMBIENT_COLOR
    bg.inputs["Strength"].default_value = AMBIENT
    return sc


AMBIENT = 0.70
AMBIENT_COLOR = (0.80, 0.86, 1.0, 1.0)
SUN = 1.15


def add_sun(direction, energy=None, color=(1.0, 0.97, 0.9), angle=0.06):
    d = bpy.data.lights.new("LGT_key", "SUN")
    d.energy = SUN if energy is None else energy
    d.color = color
    d.angle = angle
    o = bpy.data.objects.new("LGT_key", d)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = Vector(direction).to_track_quat("-Z", "Y").to_euler()
    return o


# light travels east, south and down: it comes from the upper left of the screen
TOP_DIR = (0.55, -0.55, -1.0)
# props: from the left, a little from the front, high up
PROP_DIR = (0.62, 0.30, -0.85)


def topdown_camera(cx, cy, size):
    cd = bpy.data.cameras.new("CAM_top")
    cd.type = "ORTHO"
    cd.ortho_scale = size
    cam = bpy.data.objects.new("CAM_top", cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = (cx, cy, 40)
    cam.rotation_euler = (0, 0, 0)
    cd.clip_start, cd.clip_end = 1.0, 100.0
    bpy.context.scene.camera = cam
    return cam


def prop_camera(canvas_px: int, base_px: int):
    """Standard camera. The world origin lands `base_px` above the canvas bottom, centred."""
    cd = bpy.data.cameras.new("CAM_prop")
    cd.type = "ORTHO"
    # image-plane scale: vertical metres are foreshortened by cos(35); the player is 1 m = 36 px
    # tall, so image-plane px/m = 36 / cos(35)
    ppm = PX_PER_M / math.cos(math.radians(CAM_ELEV))
    cd.ortho_scale = canvas_px / ppm
    cam = bpy.data.objects.new("CAM_prop", cd)
    bpy.context.scene.collection.objects.link(cam)
    th = math.radians(90 - CAM_ELEV)
    d = Vector((0, math.sin(th), -math.cos(th)))
    cam.location = -d * 30
    cam.rotation_euler = (th, 0, 0)
    cd.clip_start, cd.clip_end = 1.0, 80.0
    cd.shift_y = ((canvas_px / 2 - base_px) / canvas_px)
    bpy.context.scene.camera = cam
    return cam


def only_collection_visible(name: str):
    for c in bpy.context.scene.collection.children:
        c.hide_render = (c.name != f"COL_{name}")
        c.hide_viewport = c.hide_render


def render_png(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


# --------------------------------------------------------------------------- pixelise (numpy)
def load_rgba(path: Path):
    import numpy as np
    img = bpy.data.images.load(str(path))
    img.colorspace_settings.name = "Non-Color"      # read the stored sRGB bytes as they are
    img.alpha_mode = "STRAIGHT"
    w, h = img.size
    a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1]   # top row first
    bpy.data.images.remove(img)
    return a


def _srgb(a):
    import numpy as np
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.maximum(a, 1e-9), 1 / 2.4) - 0.055)


def ramps_palette(ramps):
    import numpy as np
    seen, out = set(), []
    for r in ramps:
        for h in RAMPS[r]:
            c = hex_rgb(h)
            if c not in seen:
                seen.add(c)
                out.append(c)
    return np.array(out, dtype=np.float32)


def pixelise(rgba, out_w: int, out_h: int, outline: bool, alpha_cut: float = 0.5, ramps=None):
    """Box-filter down, drop soft alpha, snap to the world palette, add a selective outline."""
    import numpy as np
    h, w, _ = rgba.shape
    fy, fx = h // out_h, w // out_w
    a = rgba[: out_h * fy, : out_w * fx]
    al = a[..., 3]
    rgb = np.clip(a[..., :3], 0, 1) * 255.0
    wgt = al[..., None]
    num = (rgb * wgt).reshape(out_h, fy, out_w, fx, 3).sum((1, 3))
    den = wgt.reshape(out_h, fy, out_w, fx, 1).sum((1, 3))
    col = num / np.maximum(den, 1e-6)
    alpha = al.reshape(out_h, fy, out_w, fx).mean((1, 3))
    opaque = alpha >= alpha_cut
    pal = ramps_palette(ramps) if ramps else np.array(palette_list(), dtype=np.float32)
    col = snap(col, pal)
    out = np.zeros((out_h, out_w, 4), dtype=np.uint8)
    out[..., :3] = col
    out[..., 3] = np.where(opaque, 255, 0)
    if outline:
        out = add_outline(out, pal)
    return out


_WEIGHTS = np_weights = None


def snap(col, pal):
    import numpy as np
    flat = col.reshape(-1, 3)
    wv = np.array([0.30, 0.55, 0.15], dtype=np.float32) * 1.0
    res = np.empty((flat.shape[0], 3), dtype=np.float32)
    for i in range(0, flat.shape[0], 4096):
        chunk = flat[i:i + 4096]
        d = (((chunk[:, None, :] - pal[None, :, :]) ** 2) * wv).sum(-1)
        res[i:i + 4096] = pal[d.argmin(1)]
    return res.reshape(col.shape)


def add_outline(img, pal, factor=0.42):
    """1 px outline outside the silhouette, a darker shade of the colour it borders."""
    import numpy as np
    h, w, _ = img.shape
    pad = np.zeros((h + 2, w + 2, 4), dtype=np.uint8)
    pad[1:-1, 1:-1] = img
    op = pad[..., 3] > 0
    out = pad.copy()
    sumcol = np.zeros((h + 2, w + 2, 3), dtype=np.float32)
    cnt = np.zeros((h + 2, w + 2), dtype=np.float32)
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        sh = np.roll(np.roll(pad, dy, 0), dx, 1)
        m = sh[..., 3] > 0
        sumcol += sh[..., :3] * m[..., None]
        cnt += m
    edge = (~op) & (cnt > 0)
    avg = sumcol / np.maximum(cnt, 1)[..., None]
    dark = snap(avg * factor + np.array([8, 6, 22], dtype=np.float32) * (1 - factor) * 0.5, pal)
    out[edge, :3] = dark[edge]
    out[edge, 3] = 255
    return out


def save_png(arr, path: Path):
    """Write an RGBA uint8 array as PNG through Blender's image API."""
    import numpy as np
    h, w, _ = arr.shape
    img = bpy.data.images.new("tmp_save", w, h, alpha=True)
    f = np.flipud(arr.astype(np.float32) / 255.0)
    # stored values are sRGB already: make the image non-colour so nothing is converted
    img.colorspace_settings.name = "Non-Color"
    img.pixels.foreach_set(f.ravel())
    img.filepath_raw = str(path)
    img.file_format = "PNG"
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save()
    bpy.data.images.remove(img)


def args_after_dashes():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
