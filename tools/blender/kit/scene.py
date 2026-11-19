"""Scene, camera, key light and frame capture for sprite rendering (bpy).

Three camera modes, all orthographic, all built here and never by hand:
  * "ground": 35 degrees above the horizon, looking along +Y (characters, monsters, props, FX)
  * "top":    straight down (ground tiles)
  * "icon":   level, looking along +Y; the object is posed diagonally (icons)

The camera is placed so that the world origin lands exactly on the requested pivot pixel:
the pivot is computed, never guessed. The key light is fixed in *camera* space (upper left,
a little toward the viewer), so turning the model for the four directions keeps the light
on the upper left of the picture.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

from . import paths, toon

SCALE = 6                       # render at 6x the target size
ELEVATION = 35.0
CAM_DIST = 30.0
# Key light in camera space: x right, y up, z toward the viewer.
LIGHT_CAM = Vector((-0.55, 0.55, 0.63)).normalized()


class Cam:
    """The kit camera for one render job."""

    def __init__(self, mode: str, w: int, h: int, ppm: float, pivot: tuple[float, float],
                 center: Vector | None = None, elevation: float = ELEVATION):
        self.mode, self.w, self.h, self.ppm, self.pivot = mode, w, h, ppm, pivot
        self.elevation = float(elevation)
        if mode == "ground":
            el = math.radians(self.elevation)
            rot = Matrix.Rotation(math.pi / 2 - el, 4, "X")
        elif mode == "top":
            rot = Matrix.Identity(4)
        elif mode == "icon":
            rot = Matrix.Rotation(math.pi / 2, 4, "X")
        else:
            raise ValueError(f"camera mode {mode!r}: use ground, top or icon")
        r3 = rot.to_3x3()
        self.right = (r3 @ Vector((1, 0, 0))).normalized()
        self.up = (r3 @ Vector((0, 1, 0))).normalized()
        self.back = (r3 @ Vector((0, 0, 1))).normalized()     # toward the viewer
        origin = center if center is not None else Vector((0, 0, 0))
        # world point `origin` lands on pixel `pivot` (final px, y down)
        a = (w / 2 - pivot[0]) / ppm
        b = (pivot[1] - h / 2) / ppm
        loc = origin + self.back * CAM_DIST + self.right * a + self.up * b
        self.matrix = Matrix.Translation(loc) @ rot
        self.light = (LIGHT_CAM.x * self.right + LIGHT_CAM.y * self.up + LIGHT_CAM.z * self.back).normalized()
        self.half = (self.light + self.back).normalized()
        self.ortho_scale = max(w, h) / ppm
        reach = max(3.0, self.ortho_scale * 1.5)
        self.depth_lo, self.depth_hi = CAM_DIST - reach, CAM_DIST + reach

    def project(self, p: Vector) -> tuple[float, float]:
        """World point -> final-pixel coordinates (x right, y down)."""
        loc = self.matrix.to_translation()
        d = p - loc
        return (self.w / 2 + d.dot(self.right) * self.ppm,
                self.h / 2 - d.dot(self.up) * self.ppm)

    def snap_offset(self, p: Vector) -> Matrix:
        """Camera matrix moved by the sub-pixel amount that puts world point p exactly on
        the centre of a final pixel (the camera's axes and the light do not change)."""
        x, y = self.project(p)
        ox = (math.floor(x) + 0.5) - x
        oy = (math.floor(y) + 0.5) - y
        move = -self.right * (ox / self.ppm) + self.up * (oy / self.ppm)
        return Matrix.Translation(move) @ self.matrix

    def apply(self, scene) -> bpy.types.Object:
        cam = bpy.data.objects.get("KIT_CAM")
        if cam is None:
            data = bpy.data.cameras.new("KIT_CAM")
            cam = bpy.data.objects.new("KIT_CAM", data)
            scene.collection.objects.link(cam)
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = self.ortho_scale
        cam.data.clip_start = 0.01
        cam.data.clip_end = CAM_DIST * 4
        cam.data.shift_x = cam.data.shift_y = 0.0
        cam.data.sensor_fit = "AUTO"
        cam.matrix_world = self.matrix
        cam.hide_render = False
        scene.camera = cam
        scene.render.resolution_x = self.w * SCALE
        scene.render.resolution_y = self.h * SCALE
        scene.render.resolution_percentage = 100
        scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1
        return cam


def setup_render(scene=None):
    """EEVEE, 1 sample, no filter, no dither, Raw view, transparent film, 16-bit PNG."""
    scene = scene or bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    ee = scene.eevee
    for k, v in (("taa_render_samples", 1), ("use_shadows", False), ("use_raytracing", False),
                 ("use_taa_reprojection", False)):
        try:
            setattr(ee, k, v)
        except (AttributeError, TypeError):
            pass
    r = scene.render
    r.filter_size = 0.0
    r.film_transparent = True
    r.dither_intensity = 0.0
    r.use_motion_blur = False
    try:
        r.use_compositing = False
        r.use_sequencer = False
    except AttributeError:
        pass
    scene.view_settings.view_transform = "Raw"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    try:
        scene.display_settings.display_device = "sRGB"
    except TypeError:
        pass
    im = r.image_settings
    im.file_format = "PNG"
    im.color_mode = "RGBA"
    im.color_depth = "16"
    im.compression = 0
    if scene.world is None:
        scene.world = bpy.data.worlds.new("KIT_world")
    return scene


# ---------------------------------------------------------------- asset objects
def expand(things) -> list:
    """Objects, collections, names or lists of them -> objects with all descendants."""
    if things is None:
        return []
    if not isinstance(things, (list, tuple, set)):
        things = [things]
    out = []
    for t in things:
        if isinstance(t, str):
            t = bpy.data.objects.get(t) or bpy.data.collections.get(t)
            if t is None:
                continue
        if isinstance(t, bpy.types.Collection):
            objs = list(t.all_objects)
        else:
            objs = [t] + list(t.children_recursive)
        for o in objs:
            if o not in out:
                out.append(o)
    return out


class Staging:
    """Show only the asset (plus holdouts), parent its roots to a turntable empty, and put
    everything back afterwards."""

    def __init__(self, scene, show: list, holdout: list = ()):
        self.scene, self.show, self.holdout = scene, list(show), list(holdout)
        self.saved = {}

    def __enter__(self):
        # Bring matrix_world up to date first: a script that just set location /
        # matrix_basis has not been evaluated yet, and the stale world matrix read below
        # would be written back, undoing the move (this broke the first tile of a call).
        bpy.context.view_layer.update()
        keep = set(self.show) | set(self.holdout)
        ancestors = set()
        for o in keep:
            p = o.parent
            while p is not None:
                ancestors.add(p)
                p = p.parent
        # Objects that are not part of this render go into an excluded collection, so that
        # even animated visibility (hide_render keyed by an FX) cannot bring them back.
        hidden = bpy.data.collections.get("KIT_hidden") or bpy.data.collections.new("KIT_hidden")
        if hidden.name not in self.scene.collection.children:
            self.scene.collection.children.link(hidden)
        self.scene.view_layers[0].layer_collection.children[hidden.name].exclude = True
        self.hidden, self.moved = hidden, []
        for o in list(self.scene.objects):
            if o.name in ("KIT_CAM", "KIT_TURN"):
                continue
            self.saved[o.name] = (o.hide_render, getattr(o, "is_holdout", False))
            if o in keep:
                o.hide_render = False
                if o in self.holdout:
                    o.is_holdout = True
            elif o in ancestors:
                o.hide_render = True
            else:
                cols = list(o.users_collection)
                self.moved.append((o, cols))
                for c in cols:
                    c.objects.unlink(o)
                hidden.objects.link(o)
        turn = bpy.data.objects.get("KIT_TURN")
        if turn is None:
            turn = bpy.data.objects.new("KIT_TURN", None)
            self.scene.collection.objects.link(turn)
        turn.matrix_world = Matrix.Identity(4)
        self.turn = turn
        everything = set(self.show) | set(self.holdout)
        self.roots = []
        for o in everything:
            if o.parent is None or o.parent not in everything:
                self.roots.append((o, o.parent, o.matrix_world.copy(), o.matrix_parent_inverse.copy()))
                mw = o.matrix_world.copy()
                o.parent = turn
                o.matrix_parent_inverse = Matrix.Identity(4)
                o.matrix_world = mw
        bpy.context.view_layer.update()
        return self

    def turn_to(self, degrees: float, extra: Matrix | None = None):
        m = Matrix.Rotation(math.radians(degrees), 4, "Z")
        self.turn.matrix_world = (extra @ m) if extra is not None else m

    def __exit__(self, *exc):
        self.turn.matrix_world = Matrix.Identity(4)
        bpy.context.view_layer.update()
        for o, parent, mw, mpi in self.roots:
            o.parent = parent
            o.matrix_parent_inverse = mpi
            o.matrix_world = mw
        for o, cols in self.moved:
            self.hidden.objects.unlink(o)
            for c in cols:
                c.objects.link(o)
        for o in self.scene.objects:
            if o.name in self.saved:
                o.hide_render, hold = self.saved[o.name]
                try:
                    o.is_holdout = hold
                except AttributeError:
                    pass
        bpy.context.view_layer.update()
        return False


def mesh_objects(objs) -> list:
    return [o for o in objs if o.type in ("MESH", "CURVE", "SURFACE", "META", "FONT", "CURVES")]


def prepare_materials(objs, cam: Cam, fx: bool = False) -> dict:
    """Inject the toon block into every material of these objects. Returns {id: info}."""
    mats, table = {}, {}
    fallback = None
    for o in mesh_objects(objs):
        if not getattr(o.data, "materials", None) or not any(o.data.materials):
            if fallback is None:
                fallback = bpy.data.materials.get("KIT_default") or bpy.data.materials.new("KIT_default")
                fallback.use_nodes = True
            if hasattr(o.data, "materials"):
                o.data.materials.append(fallback)
        for m in o.data.materials:
            if m is not None and m.name not in mats:
                mats[m.name] = m
    for i, (name, m) in enumerate(sorted(mats.items()), start=1):
        if i > 250:
            raise RuntimeError("more than 250 materials in one render")
        table[i] = toon.inject(m, i, cam.light, cam.half, cam.depth_lo, cam.depth_hi, fx=fx)
    return table


# ---------------------------------------------------------------- capture
class Capture:
    """Renders the two passes of the current frame and returns them as float arrays."""

    def __init__(self, scene, fx: bool = False):
        self.scene, self.fx = scene, fx
        self.dir = paths.tmp_dir()

    def _shot(self, name: str) -> np.ndarray:
        path = str(self.dir / f"{name}.png")
        self.scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(path, check_existing=False)
        img.colorspace_settings.name = "Non-Color"
        w, h = img.size
        buf = np.empty(w * h * 4, np.float32)
        img.pixels.foreach_get(buf)
        bpy.data.images.remove(img)
        return buf.reshape(h, w, 4)[::-1]           # Blender rows go bottom-up

    def frame(self):
        toon.set_pass(self.scene, 0)
        albedo = self._shot("albedo")
        if self.fx:
            return albedo, None
        toon.set_pass(self.scene, 1)
        data = self._shot("data")
        return albedo, data

    def cleanup(self):
        for p in Path(self.dir).glob("*.png"):
            try:
                p.unlink()
            except OSError:
                pass
        try:
            os.rmdir(self.dir)
        except OSError:
            pass


def world_bounds(objs, depsgraph=None) -> list[Vector]:
    """The 8 bounding-box corners of every renderable object, in world space."""
    pts = []
    for o in mesh_objects(objs):
        if o.hide_render:
            continue
        for c in o.bound_box:
            pts.append(o.matrix_world @ Vector(c))
    return pts
