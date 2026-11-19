"""FX building blocks. Runs INSIDE Blender (headless).

Every effect is a real Blender scene: emissive meshes (flat 2D shapes built from numbers),
animated with keyframes (location / rotation / scale / material value nodes), seen by an
orthographic camera.  Shapes live in a local 2D plane (x right, y up):

  view 'front'  : camera looks along +Y, the shape plane is world XZ      (combat, realm FX)
  view 'ground' : camera 35 deg above the horizon, plane is world XY      (formation circles)
  view 'top'    : camera straight down, plane is world XY                 (hit-zone warnings)

1 Blender unit = 32 sprite pixels (a 64 px frame is 2 units, a 96 px frame is 3 units).
"""
import bpy
import bmesh
import math
import random
import numpy as np

TAU = math.tau
PI = math.pi
RENDER_SCALE = 6          # render at 6x the target size, then scale down (contract section 2)
PXU = 32.0                # sprite pixels per unit


# --------------------------------------------------------------------------- colours
def hexc(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5))


def lin(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return tuple(f(v) for v in c)


def mixc(a, b, t):
    a, b = hexc(a) if isinstance(a, str) else a, hexc(b) if isinstance(b, str) else b
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def tohex(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255 + 0.5) for v in c)


# element colours: (body, core)
ELEM = {
    "tho": ("#b4701e", "#f2b25a"),
    "kim": ("#ffe49a", "#ffffff"),
    "hoa": ("#ff5a18", "#ffe58a"),
    "moc": ("#46dc58", "#e2ffb8"),
    "thuy": ("#2aa6ff", "#d2f6ff"),
    "loi": ("#9858ff", "#f4ecff"),
}


# --------------------------------------------------------------------------- materials
class FxMat:
    def __init__(self, mat, vals):
        self.mat = mat
        self.vals = vals


def make_mat(name, color, mode="add", grad=None, core=None, window=False, opacity=1.0,
             strength=1.0, ufade=0.0):
    """Emissive material.  mode 'add' = pure additive, 'alpha' = ordinary alpha (emission over
    transparent).  grad = dict(src='attr'|'radial'|'rim', pow=2.0) drives the opacity (and the
    colour blend towards `core`).  window=True adds keyed 'head'/'tail' sweep along attribute u."""
    m = bpy.data.materials.new("MAT_" + name)
    m.use_nodes = True
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    nt = m.node_tree
    N = nt.nodes
    L = nt.links
    N.clear()
    out = N.new("ShaderNodeOutputMaterial")
    em = N.new("ShaderNodeEmission")
    tr = N.new("ShaderNodeBsdfTransparent")

    def math_(op, a=None, b=None, clamp=False):
        n = N.new("ShaderNodeMath")
        n.operation = op
        n.use_clamp = clamp
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                L.new(v, n.inputs[i])
        return n.outputs[0]

    vals = {}
    opn = N.new("ShaderNodeValue")
    opn.outputs[0].default_value = opacity
    vals["op"] = opn.outputs[0]
    fac = opn.outputs[0]
    t = None
    if grad:
        src = grad.get("src", "attr")
        if src == "attr":
            a = N.new("ShaderNodeAttribute")
            a.attribute_name = grad.get("name", "g")
            t = a.outputs["Fac"]
        else:
            tc = N.new("ShaderNodeTexCoord")
            vl = N.new("ShaderNodeVectorMath")
            vl.operation = "LENGTH"
            L.new(tc.outputs["Object"], vl.inputs[0])
            ln = vl.outputs["Value"]
            t = math_("SUBTRACT", 1.0, ln, True) if src == "radial" else math_("MULTIPLY", ln, 1.0, True)
        tp = math_("POWER", t, grad.get("pow", 2.0))
        fac = math_("MULTIPLY", fac, tp)
    if window:
        au = N.new("ShaderNodeAttribute")
        au.attribute_name = "u"
        u = au.outputs["Fac"]
        hn = N.new("ShaderNodeValue")
        hn.outputs[0].default_value = 1.0
        tn = N.new("ShaderNodeValue")
        tn.outputs[0].default_value = 0.0
        vals["head"] = hn.outputs[0]
        vals["tail"] = tn.outputs[0]
        d1 = math_("SUBTRACT", u, tn.outputs[0])
        a1 = math_("DIVIDE", d1, 0.35, True)                # soft tail
        d2 = math_("SUBTRACT", hn.outputs[0], u)
        b1 = math_("DIVIDE", d2, 0.04, True)                # crisp head
        fac = math_("MULTIPLY", fac, math_("MULTIPLY", a1, b1))
    if ufade:
        au2 = N.new("ShaderNodeAttribute")
        au2.attribute_name = "u"
        sn = math_("SINE", math_("MULTIPLY", au2.outputs["Fac"], PI))
        fac = math_("MULTIPLY", fac, math_("POWER", sn, ufade))
    col = N.new("ShaderNodeRGB")
    col.outputs[0].default_value = (*lin(hexc(color) if isinstance(color, str) else color), 1)
    colo = col.outputs[0]
    if core is not None and t is not None:
        c2 = N.new("ShaderNodeRGB")
        c2.outputs[0].default_value = (*lin(hexc(core) if isinstance(core, str) else core), 1)
        mx = N.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        cf = math_("POWER", t, grad.get("cpow", 2.5))
        L.new(cf, mx.inputs[0])
        L.new(colo, mx.inputs[6])
        L.new(c2.outputs[0], mx.inputs[7])
        colo = mx.outputs[2]
    L.new(colo, em.inputs["Color"])
    if mode == "add":
        L.new(math_("MULTIPLY", fac, strength), em.inputs["Strength"])
        ad = N.new("ShaderNodeAddShader")
        L.new(em.outputs[0], ad.inputs[0])
        L.new(tr.outputs[0], ad.inputs[1])
        L.new(ad.outputs[0], out.inputs["Surface"])
    else:
        em.inputs["Strength"].default_value = strength
        mix = N.new("ShaderNodeMixShader")
        L.new(fac, mix.inputs[0])
        L.new(tr.outputs[0], mix.inputs[1])
        L.new(em.outputs[0], mix.inputs[2])
        L.new(mix.outputs[0], out.inputs["Surface"])
    return FxMat(m, vals)


# --------------------------------------------------------------------------- mesh builder
class MB:
    """Accumulates 2D shapes into one mesh.  Attributes per vertex: g (0..1 'body' mask used for
    soft edges / gradients) and u (0..1 along a ribbon, used by the sweep window)."""

    def __init__(self):
        self.v = []
        self.f = []
        self.g = []
        self.u = []

    def _add(self, pts, faces, g, u):
        b = len(self.v)
        self.v += [(float(p[0]), float(p[1])) for p in pts]
        self.f += [tuple(b + i for i in f) for f in faces]
        self.g += list(g)
        self.u += list(u)
        return self

    def strip(self, pts, widths, soft=False, g_edge=None):
        """Ribbon along a polyline. soft=True: g = 0 at both edges, 1 on the spine."""
        n = len(pts)
        P = np.array(pts, dtype=float)
        if np.isscalar(widths):
            widths = [widths] * n
        T = np.zeros_like(P)
        T[1:-1] = P[2:] - P[:-2]
        T[0] = P[1] - P[0]
        T[-1] = P[-1] - P[-2]
        T /= np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-9)
        Nn = np.stack([-T[:, 1], T[:, 0]], 1)
        ge = (0.0 if soft else 1.0) if g_edge is None else g_edge
        verts, g, u, faces = [], [], [], []
        for i in range(n):
            w = widths[i] * 0.5
            verts += [P[i] + Nn[i] * w, P[i], P[i] - Nn[i] * w]
            g += [ge, 1.0, ge]
            u += [i / max(n - 1, 1)] * 3
        for i in range(n - 1):
            a = i * 3
            faces += [(a, a + 1, a + 4, a + 3), (a + 1, a + 2, a + 5, a + 4)]
        return self._add(verts, faces, g, u)

    def fan(self, cx, cy, pts, g_c=1.0, g_e=1.0):
        """Convex fan around (cx,cy)."""
        verts = [(cx, cy)] + [tuple(p) for p in pts]
        n = len(pts)
        faces = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)]
        return self._add(verts, faces, [g_c] + [g_e] * n, [0.0] * (n + 1))

    def disc(self, cx, cy, r, seg=28, g_c=1.0, g_e=1.0, ky=1.0):
        pts = [(cx + r * math.cos(TAU * i / seg), cy + ky * r * math.sin(TAU * i / seg)) for i in range(seg)]
        return self.fan(cx, cy, pts, g_c, g_e)

    def poly(self, pts, g=1.0):
        """Any simple polygon (ear-clipped through bmesh)."""
        bm = bmesh.new()
        vs = [bm.verts.new((p[0], p[1], 0)) for p in pts]
        try:
            fc = bm.faces.new(vs)
            bmesh.ops.triangulate(bm, faces=[fc], quad_method="BEAUTY", ngon_method="EAR_CLIP")
        except ValueError:
            bm.free()
            return self
        faces = [tuple(v.index for v in f.verts) for f in bm.faces]
        bm.free()
        return self._add(pts, faces, [g] * len(pts), [0.0] * len(pts))

    def ring(self, cx, cy, r, w, a0=0.0, a1=TAU, seg=None, soft=False, ky=1.0, kx=1.0):
        seg = seg or max(8, int(48 * abs(a1 - a0) / TAU) + 2)
        pts = [(cx + kx * r * math.cos(a0 + (a1 - a0) * i / seg), cy + ky * r * math.sin(a0 + (a1 - a0) * i / seg))
               for i in range(seg + 1)]
        if abs((a1 - a0) - TAU) < 1e-6:
            pts[-1] = pts[0]
        return self.strip(pts, w, soft=soft)

    def line(self, p0, p1, w, soft=False, taper=False):
        n = 4
        pts = [(p0[0] + (p1[0] - p0[0]) * i / n, p0[1] + (p1[1] - p0[1]) * i / n) for i in range(n + 1)]
        ws = [w * (1 - i / n) if taper else w for i in range(n + 1)]
        if taper:
            ws[-1] = w * 0.05
        return self.strip(pts, ws, soft=soft)

    def star(self, cx, cy, n, r_out, r_in, rot=0.0, g_c=1.0, g_e=1.0):
        pts = []
        for i in range(n * 2):
            r = r_out if i % 2 == 0 else r_in
            a = rot + PI * i / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return self.fan(cx, cy, pts, g_c, g_e)

    def diamond(self, cx, cy, length, width, rot=0.0, g_c=1.0, g_e=1.0):
        ca, sa = math.cos(rot), math.sin(rot)
        loc = [(length / 2, 0), (0, width / 2), (-length / 2, 0), (0, -width / 2)]
        pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in loc]
        return self.fan(cx, cy, pts, g_c, g_e)

    def drop(self, cx, cy, length, width, rot=0.0):
        """Teardrop pointing along +x (round head at +x... tail point at -x)."""
        pts = []
        n = 14
        for i in range(n + 1):
            a = -PI / 2 + PI * i / n
            pts.append((width / 2 * math.cos(a) + length / 2 - width / 2, width / 2 * math.sin(a)))
        pts.append((-length / 2, 0))
        # that polyline is the head arc then the tail point: close it
        ca, sa = math.cos(rot), math.sin(rot)
        pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
        return self.poly(pts)

    def flame(self, cx, cy, h, w, sway=0.0, lean=0.0, seg=8):
        """A flame tongue: wide base at (cx,cy), tip at the top, S-bent by sway."""
        left, right = [], []
        for i in range(seg + 1):
            s = i / seg
            width = w * (math.sin(PI * min(1.0, s * 0.85 + 0.15)) ** 0.8) * (1 - s) ** 0.55 + w * 0.02
            cxs = cx + lean * s + sway * math.sin(s * PI * 1.3) * s
            y = cy + h * s
            left.append((cxs - width / 2, y))
            right.append((cxs + width / 2, y))
        pts = left + right[::-1][1:]
        return self.poly(pts)

    def xform(self, rot=0.0, sx=1.0, sy=1.0, dx=0.0, dy=0.0):
        """rotate, then scale (x, y separately), then move - all vertices (used to squash ground circles)."""
        ca, sa = math.cos(rot), math.sin(rot)
        self.v = [((x * ca - y * sa) * sx + dx, (x * sa + y * ca) * sy + dy) for x, y in self.v]
        return self

    def merge(self, other, dx=0.0, dy=0.0, s=1.0, rot=0.0):
        ca, sa = math.cos(rot), math.sin(rot)
        verts = [((x * ca - y * sa) * s + dx, (x * sa + y * ca) * s + dy) for x, y in other.v]
        return self._add(verts, other.f, other.g, other.u)

    def build(self, fx, name, fm, x=0.0, y=0.0, z=0.0):
        me = bpy.data.meshes.new("SM_" + fx.id + "_" + name)
        verts = [(p[0], p[1], 0.0) for p in self.v]
        me.from_pydata(verts, [], self.f)
        me.update()
        for an, arr in (("g", self.g), ("u", self.u)):
            at = me.attributes.new(an, "FLOAT", "POINT")
            at.data.foreach_set("value", np.array(arr, dtype=np.float32))
        me.materials.append(fm.mat)
        ob = bpy.data.objects.new("SM_" + fx.id + "_" + name, me)
        fx.col.objects.link(ob)
        fx.reg(ob, fm, x, y, z)
        return ob


# --------------------------------------------------------------------------- scene / fx object
class Fx:
    def __init__(self, id, view="front", frames=6, fps=12, loop=False, mode="add", px=64,
                 ground=False, pivot=None, halo=0.0, levels=5, name_vi="", where="", alpha_levels=3,
                 gamma=1.0, zoom=1.12, ppu=PXU):
        self.id, self.view, self.N, self.fps, self.loop, self.mode = id, view, frames, fps, loop, mode
        self.px, self.ground, self.halo, self.levels = px, ground, halo, levels
        self.alpha_levels = alpha_levels
        self.gamma = gamma
        self.pivot = pivot or (px // 2, px // 2)
        self.name_vi, self.where = name_vi, where
        self.units = px / ppu
        self.state = {}
        self.mats = {}
        self.rng = random.Random(hash(id) & 0xFFFF)
        self.rng = random.Random(sum(ord(c) * (i + 3) for i, c in enumerate(id)))
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.sc = sc = bpy.context.scene
        sc.name = "SC_FX_" + id
        self.col = bpy.data.collections.new("COL_FX_" + id)
        sc.collection.children.link(self.col)
        r = sc.render
        r.engine = "BLENDER_EEVEE"
        r.resolution_x = r.resolution_y = px * RENDER_SCALE
        r.resolution_percentage = 100
        r.film_transparent = (mode == "alpha")
        r.fps = fps
        sc.frame_start, sc.frame_end = 1, frames
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.display_settings.display_device = "sRGB"
        r.image_settings.file_format = "PNG"
        r.image_settings.color_mode = "RGBA"
        r.image_settings.color_depth = "8"
        try:
            sc.eevee.taa_render_samples = 6
        except Exception:
            pass
        w = bpy.data.worlds.new("W")
        w.use_nodes = True
        for n in w.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Color"].default_value = (0, 0, 0, 1)
                n.inputs["Strength"].default_value = 0.0
        sc.world = w
        cam = bpy.data.cameras.new("CAM_" + id)
        cam.type = "ORTHO"
        cam.ortho_scale = self.units * zoom
        cam.clip_end = 200
        co = bpy.data.objects.new("CAM_" + id, cam)
        sc.collection.objects.link(co)
        if view == "front":
            co.location, co.rotation_euler = (0, -30, 0), (PI / 2, 0, 0)
        elif view == "top":
            co.location, co.rotation_euler = (0, 0, 30), (0, 0, 0)
        else:
            e = math.radians(35)
            co.location = (0, -30 * math.cos(e), 30 * math.sin(e))
            co.rotation_euler = (PI / 2 - e, 0, 0)
        sc.camera = co

    # ---- bookkeeping
    def T(self, i):
        return i / self.N if self.loop else i / max(self.N - 1, 1)

    def mat(self, name, color, **kw):
        kw.setdefault("mode", self.mode)
        key = name
        fm = make_mat(self.id + "_" + name, color, **kw)
        self.mats[key] = fm
        return fm

    def reg(self, ob, fm, x, y, z):
        ob.rotation_mode = "ZXY" if self.view == "front" else "XYZ"
        self.state[ob.name] = dict(x=x, y=y, rot=0.0, sx=1.0, sy=1.0, z=z, fm=fm)
        self._place(ob)

    def _place(self, ob):
        s = self.state[ob.name]
        if self.view == "front":
            ob.location = (s["x"], s["z"], s["y"])
            ob.rotation_euler = (PI / 2, 0, s["rot"])
        else:
            ob.location = (s["x"], s["y"], s["z"])
            ob.rotation_euler = (0, 0, s["rot"])
        ob.scale = (s["sx"], s["sy"], 1.0)

    def pose(self, ob, f=None, **d):
        """Set (and, with f, keyframe) x, y, z, rot, s, sx, sy, op, head, tail, show."""
        s = self.state[ob.name]
        fm = s["fm"]
        if "s" in d:
            d["sx"] = d["sy"] = d.pop("s")
        show = d.pop("show", True)
        for k in ("x", "y", "z", "rot", "sx", "sy"):
            if k in d:
                s[k] = d[k]
        saved = (s["sx"], s["sy"])
        if not show:
            s["sx"] = s["sy"] = 0.0
        self._place(ob)
        s["sx"], s["sy"] = saved
        if f is not None:
            ob.keyframe_insert("location", frame=f)
            ob.keyframe_insert("rotation_euler", frame=f)
            ob.keyframe_insert("scale", frame=f)
        for k in ("op", "head", "tail"):
            if k in d and k in fm.vals:
                v = fm.vals[k]
                v.default_value = d[k]
                if f is not None:
                    v.keyframe_insert("default_value", frame=f)
        return ob

    def track(self, ob, fn):
        """fn(t, i) -> dict for pose(); keyed on every frame."""
        for i in range(self.N):
            d = fn(self.T(i), i)
            if d is None:
                d = dict(show=False)
            self.pose(ob, i + 1, **d)
        self.pose(ob, None, **(fn(self.T(0), 0) or dict(show=False)))
        return ob

    def only_on(self, ob, frames):
        """Visible only in the listed 0-based frames."""
        fr = set(frames)
        return self.track(ob, lambda t, i: dict(show=(i in fr)))

    def per_frame(self, name, fm, builder, x=0.0, y=0.0, z=0.0, post=None):
        """One mesh per frame (builder(t, i) -> MB), each visible only on its own frame - used for
        shapes that deform (flames, lightning, helices).  post(ob, t, i) may add extra pose."""
        obs = []
        for i in range(self.N):
            mb = builder(self.T(i), i)
            ob = mb.build(self, "%s_%02d" % (name, i), fm, x, y, z)
            self.track(ob, (lambda ii: (lambda t, i2: dict(show=(i2 == ii), **(post(ob, t, i2) if post else {}))))(i))
            obs.append(ob)
        return obs

    # ---- render
    def render(self, outdir):
        import os
        os.makedirs(outdir, exist_ok=True)
        paths = []
        for f in range(1, self.N + 1):
            self.sc.frame_set(f)
            p = os.path.join(outdir, "%s_%02d.png" % (self.id, f))
            self.sc.render.filepath = p
            bpy.ops.render.render(write_still=True)
            paths.append(p)
        return paths


# --------------------------------------------------------------------------- shape helpers
def arc_pts(cx, cy, r, a0, a1, n=24, ky=1.0):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + ky * r * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def runes(mb, cx, cy, r, n, size, rng, w=0.03, tangent=True, rot0=0.0, strokes=(2, 4), ky=1.0):
    """n abstract rune marks (random strokes on a 3x3 grid) placed around a circle. No glyphs."""
    grid = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for k in range(n):
        a = rot0 + TAU * k / n
        px, py = cx + r * math.cos(a), cy + ky * r * math.sin(a)
        rot = a - PI / 2 if tangent else 0.0
        ca, sa = math.cos(rot), math.sin(rot)
        used = set()
        for _ in range(rng.randint(*strokes)):
            p, q = rng.sample(grid, 2)
            if (p, q) in used or (q, p) in used:
                continue
            used.add((p, q))
            pts = []
            for (gx, gy) in (p, q):
                lx, ly = gx * size * 0.5, gy * size * 0.5
                pts.append((px + lx * ca - ly * sa, py + lx * sa + ly * ca))
            mb.line(pts[0], pts[1], w)
    return mb


def jag(p0, p1, rng, n=7, amp=0.12):
    """Jagged lightning polyline from p0 to p1."""
    pts = [p0]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for i in range(1, n):
        s = i / n
        o = rng.uniform(-amp, amp) * (1 - abs(s - 0.5) * 0.6)
        pts.append((p0[0] + dx * s + nx * o, p0[1] + dy * s + ny * o))
    pts.append(p1)
    return pts


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in(t):
    return t ** 3


def sat(x):
    return max(0.0, min(1.0, x))
