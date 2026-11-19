"""ARM_dao_si: the one armature every look of the player shares (runs inside Blender).

Rest pose in metres: the character faces -Y, +X is their own LEFT (bones `.L`), the origin is
the ground point between the feet, the top of the head is at ~0.99 and the bun at ~1.03 (final proportions, see to_rig).

Posing works in the rig's own terms instead of raw bone-local Euler angles, because the
limb bones slant and their local axes are hard to read:

* ``rot``  - a rotation given in the rig's rest axes, applied relative to the parent (so
  "lean forward 20 degrees" is ``rx(-20)`` on the spine whatever the hips are doing);
* ``aim``  - point the bone along a direction given in the parent's frame (as if the parent
  were at rest; for a forearm, the chest's frame): ``(0, -1, 0)`` on an upper arm is
  "straight forward" even when the body leans;
* ``waim`` - the same in world (armature) space - used for hair and cloth, which hang by
  gravity whatever the body does;
* ``loc``  - a translation in armature space (hips, mount);
* legs are solved here (two-bone IK, analytic) from an ankle target and a knee pole and
  baked to plain FK keys, so the saved actions have no constraints and replay identically
  for every batch that loads the rig.

`solve` evaluates a whole pose with our own forward kinematics (same maths Blender uses),
so a clip can read positions of its own bones (for the follow-through pass) without a scene
update per bone.
"""
from __future__ import annotations

import math

import bpy
from mathutils import Matrix, Quaternion, Vector

RIG_NAME = "ARM_dao_si"
FRAME0 = 1            # the first frame of every action (Blender convention)

# name: (head, tail, parent, deform)
BONES: dict[str, tuple] = {
    "root":       ((0, 0, 0), (0, 0.15, 0), None, False),
    "mount":      ((0, 0, 0), (0, -0.12, 0), "root", False),
    "qi":         ((0, 0, 0.45), (0, 0, 0.55), "root", True),
    "hips":       ((0, 0, 0.30), (0, 0, 0.40), "root", True),
    "spine":      ((0, 0, 0.40), (0, 0, 0.48), "hips", True),
    "chest":      ((0, 0, 0.48), (0, 0, 0.58), "spine", True),
    "neck":       ((0, 0, 0.58), (0, 0, 0.635), "chest", True),
    "head":       ((0, 0, 0.635), (0, 0, 0.95), "neck", True),
    "hair_01":    ((0, 0.10, 0.99), (0, 0.18, 0.86), "head", True),
    "hair_02":    ((0, 0.18, 0.86), (0, 0.215, 0.69), "hair_01", True),
    "hair_03":    ((0, 0.215, 0.69), (0, 0.225, 0.50), "hair_02", True),
    "ribbon_01.L": ((0.05, 0.07, 1.01), (0.11, 0.16, 0.89), "head", True),
    "ribbon_02.L": ((0.11, 0.16, 0.89), (0.15, 0.22, 0.68), "ribbon_01.L", True),
    "ribbon_01.R": ((-0.05, 0.07, 1.01), (-0.11, 0.16, 0.89), "head", True),
    "ribbon_02.R": ((-0.11, 0.16, 0.89), (-0.15, 0.22, 0.68), "ribbon_01.R", True),
    "halo":       ((0, 0, 0.80), (0, 0, 0.92), "head", True),
    "upper_arm.L": ((0.125, 0, 0.545), (0.165, 0.0, 0.44), "chest", True),
    "forearm.L":  ((0.165, 0.0, 0.44), (0.18, -0.02, 0.345), "upper_arm.L", True),
    "hand.L":     ((0.18, -0.02, 0.345), (0.185, -0.03, 0.27), "forearm.L", True),
    "sleeve.L":   ((0.175, 0.0, 0.43), (0.205, 0.03, 0.30), "forearm.L", True),
    "upper_arm.R": ((-0.125, 0, 0.545), (-0.165, 0.0, 0.44), "chest", True),
    "forearm.R":  ((-0.165, 0.0, 0.44), (-0.18, -0.02, 0.345), "upper_arm.R", True),
    "hand.R":     ((-0.18, -0.02, 0.345), (-0.185, -0.03, 0.27), "forearm.R", True),
    "sleeve.R":   ((-0.175, 0.0, 0.43), (-0.205, 0.03, 0.30), "forearm.R", True),
    "thigh.L":    ((0.07, 0, 0.30), (0.075, -0.012, 0.178), "hips", True),
    "shin.L":     ((0.075, -0.012, 0.178), (0.075, 0, 0.06), "thigh.L", True),
    "foot.L":     ((0.075, 0, 0.06), (0.075, -0.085, 0.025), "shin.L", True),
    "thigh.R":    ((-0.07, 0, 0.30), (-0.075, -0.012, 0.178), "hips", True),
    "shin.R":     ((-0.075, -0.012, 0.178), (-0.075, 0, 0.06), "thigh.R", True),
    "foot.R":     ((-0.075, 0, 0.06), (-0.075, -0.085, 0.025), "shin.R", True),
    "hem_F":      ((0, -0.085, 0.36), (0, -0.115, 0.10), "hips", True),
    "hem_B":      ((0, 0.075, 0.36), (0, 0.11, 0.10), "hips", True),
    "hem.L":      ((0.095, 0, 0.36), (0.135, 0, 0.10), "hips", True),
    "hem.R":      ((-0.095, 0, 0.36), (-0.135, 0, 0.10), "hips", True),
    "cape_01":    ((0, 0.10, 0.565), (0, 0.135, 0.40), "chest", True),
    "cape_02":    ((0, 0.135, 0.40), (0, 0.155, 0.24), "cape_01", True),
    "cape_03":    ((0, 0.155, 0.24), (0, 0.165, 0.07), "cape_02", True),
    "wing_01.L":  ((0.05, 0.11, 0.50), (0.17, 0.20, 0.62), "chest", True),
    "wing_02.L":  ((0.17, 0.20, 0.62), (0.34, 0.30, 0.82), "wing_01.L", True),
    "wing_01.R":  ((-0.05, 0.11, 0.50), (-0.17, 0.20, 0.62), "chest", True),
    "wing_02.R":  ((-0.17, 0.20, 0.62), (-0.34, 0.30, 0.82), "wing_01.R", True),
}

# ---------------------------------------------------------------- proportions
# Everything (bones and meshes) is DESIGNED in the coordinates above, then fitted to the
# final proportions by two transforms: the head and everything on it is scaled down about
# the neck (HEAD_K), the body below the neck is stretched along Z by a piecewise map (longer
# legs and torso). A vertex shared by both (the neck) blends them by its skin weights. The
# result is ~2.8 heads tall inside ~1.03 m: a young cultivator, not a toddler.
NECK_OLD, NECK_NEW, HEAD_K = 0.635, 0.69, 0.76
ZMAP = [(0.0, 0.0), (0.06, 0.055), (0.178, 0.20), (0.30, 0.36), (0.36, 0.43), (0.48, 0.535),
        (0.58, 0.645), (0.635, 0.69)]
HEAD_REGION = {"head", "hair_01", "hair_02", "hair_03", "ribbon_01.L", "ribbon_02.L",
               "ribbon_01.R", "ribbon_02.R", "halo"}


def fz(z: float) -> float:
    pts = ZMAP
    if z <= pts[0][0]:
        return z
    for (a, fa), (b, fb) in zip(pts, pts[1:]):
        if z <= b:
            return fa + (fb - fa) * (z - a) / (b - a)
    (a, fa), (b, fb) = pts[-2], pts[-1]
    return fb + (z - b) * (fb - fa) / (b - a)


def t_body(v) -> Vector:
    return Vector((v[0], v[1], fz(v[2])))


def t_head(v) -> Vector:
    return Vector((0, 0, NECK_NEW)) + (Vector(v) - Vector((0, 0, NECK_OLD))) * HEAD_K


def to_rig(v, weights: dict | None = None, bone: str | None = None) -> Vector:
    """Design space -> final rig space for a point skinned with `weights` (or on `bone`)."""
    if bone is not None:
        return t_head(v) if bone in HEAD_REGION else t_body(v)
    wh = sum(w for b, w in (weights or {}).items() if b in HEAD_REGION)
    tot = sum((weights or {}).values()) or 1.0
    k = wh / tot
    if k <= 0:
        return t_body(v)
    if k >= 1:
        return t_head(v)
    return t_body(v).lerp(t_head(v), k)


# direction of a held weapon (its socket's +Z) in the rest pose, per hand
BLADE_REST = {"hand.R": Vector((0, -1, -0.55)).normalized(), "hand.L": Vector((0, -1, 0))}

# an arm is posed in the chest's frame: both its upper arm and its forearm `aim` are
# directions as if the chest were at rest (forward -Y, out +-X, up +Z), so a pose reads
# like a drawing ("forearm straight forward") whatever the upper arm does
AIM_REF = {"forearm.L": "chest", "forearm.R": "chest"}

CHAINS = {   # secondary chains, root first: these get the follow-through pass
    "hair": ["hair_01", "hair_02", "hair_03"],
    "ribbon.L": ["ribbon_01.L", "ribbon_02.L"],
    "ribbon.R": ["ribbon_01.R", "ribbon_02.R"],
    "cape": ["cape_01", "cape_02", "cape_03"],
    "sleeve.L": ["sleeve.L"],
    "sleeve.R": ["sleeve.R"],
}
HEMS = ["hem_F", "hem_B", "hem.L", "hem.R"]


def bone_order() -> list[str]:
    out, left = [], dict(BONES)
    while left:
        for name, (_, _, parent, _) in list(left.items()):
            if parent is None or parent in out:
                out.append(name)
                del left[name]
    return out


ORDER = bone_order()
# the bones as built (final proportions); BONES stays the design space the meshes and the
# skin-weight functions are written in
RIG_BONES = {n: (tuple(to_rig(h, bone=n)), tuple(to_rig(t, bone=n)), p, d)
             for n, (h, t, p, d) in BONES.items()}


# ---------------------------------------------------------------- building
def build_armature(collection) -> bpy.types.Object:
    arm = bpy.data.armatures.new(RIG_NAME)
    rig = bpy.data.objects.new(RIG_NAME, arm)
    collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    made = {}
    for name in ORDER:
        head, tail, parent, deform = RIG_BONES[name]
        b = arm.edit_bones.new(name)
        b.head, b.tail = Vector(head), Vector(tail)
        # a fixed roll rule so the rest frames never depend on Blender's guess
        along = (Vector(tail) - Vector(head)).normalized()
        b.align_roll(Vector((0, 0, 1)) if abs(along.y) > 0.7 else Vector((0, -1, 0)))
        b.use_deform = deform
        if parent:
            b.parent = made[parent]
            b.use_connect = False
        made[name] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    arm.display_type = "STICK"
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
    halo_billboard(rig)
    return rig


def halo_billboard(rig):
    """The halo ring is a disc behind the head *as seen by the camera*: it turns against
    whatever turns the rig in the world (the kit's turntable for the four facings), so the
    left/right sprites show a ring, not a gold stick. A driver on the halo bone's twist
    (its own Y axis is world up) reads the rig's world Z rotation; nothing else keys it."""
    pb = rig.pose.bones["halo"]
    pb.rotation_mode = "XYZ"
    fc = pb.driver_add("rotation_euler", 1)
    drv = fc.driver
    drv.type = "SCRIPTED"
    var = drv.variables.new()
    var.name = "turn"
    var.type = "TRANSFORMS"
    t = var.targets[0]
    t.id = rig
    t.transform_type = "ROT_Z"
    t.transform_space = "WORLD_SPACE"
    drv.expression = "-turn"


def add_sockets(rig, collection) -> dict:
    """Empties a weapon / mount layer attaches to. A weapon model has its grip at its
    origin, length along +Z, flat side facing -Y (see README)."""
    def frame(z_axis, x_axis):
        z = Vector(z_axis).normalized()
        x = Vector(x_axis)
        x = (x - z * x.dot(z)).normalized()
        y = z.cross(x)
        m = Matrix((x, y, z)).transposed()
        return m

    # right fist: blade leaves the fist forward and a little down; edge up, flat to the side
    grip_r = to_rig(Vector(BONES["hand.R"][0]) + Vector((-0.004, -0.018, -0.04)), bone="hand.R")
    grip_l = to_rig(Vector(BONES["hand.L"][0]) + Vector((0.004, -0.018, -0.04)), bone="hand.L")
    specs = {
        "SOCKET_weapon_r": ("hand.R", grip_r, frame(BLADE_REST["hand.R"], (0, 0, 1))),
        "SOCKET_weapon_l": ("hand.L", grip_l, frame(BLADE_REST["hand.L"], (0, 0, -1))),
        "SOCKET_back": ("chest", t_body((0, 0.13, 0.47)), frame((-0.55, 0.0, 0.85), (0, -1, 0))),
        "SOCKET_mount": ("mount", Vector((0, 0, 0)), frame((0, -1, 0), (1, 0, 0))),
    }
    rig.data.pose_position = "REST"
    bpy.context.view_layer.update()
    out = {}
    for name, (bone, pos, rot) in specs.items():
        e = bpy.data.objects.new(name, None)
        e.empty_display_type = "ARROWS"
        e.empty_display_size = 0.08
        collection.objects.link(e)
        e.parent = rig
        e.parent_type = "BONE"
        e.parent_bone = bone
        bpy.context.view_layer.update()
        e.matrix_world = rig.matrix_world @ (Matrix.Translation(pos) @ rot.to_4x4())
        out[name] = e
    bpy.context.view_layer.update()
    rig.data.pose_position = "POSE"
    return out


def bind(ob, rig, weights):
    """Give `ob` vertex groups from per-vertex {bone: weight} (a list, or a function of the
    design-space position) and an armature modifier (first in the stack, so solidify /
    subdivision act on the deformed shape), then move its vertices from design space to
    the final proportions."""
    me = ob.data
    if callable(weights):
        weights = [weights(Vector(v.co)) for v in me.vertices]
    assert len(weights) == len(me.vertices), ob.name
    for v, wd in zip(me.vertices, weights):
        v.co = to_rig(v.co, wd)
    groups = {}
    for i, wd in enumerate(weights):
        total = sum(wd.values()) or 1.0
        for bone, w in wd.items():
            if w <= 1e-4:
                continue
            if bone not in groups:
                groups[bone] = ob.vertex_groups.new(name=bone)
            groups[bone].add([i], w / total, "REPLACE")
    md = ob.modifiers.new("armature", "ARMATURE")
    md.object = rig
    if ob.modifiers[0] != md:
        ob.modifiers.move(len(ob.modifiers) - 1, 0)
    ob.parent = rig
    return ob


# ---------------------------------------------------------------- weights
def _seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (a + ab * t - p).length


def w_rigid(bone):
    return lambda p: {bone: 1.0}


def w_near(bones, power=4.0, keep=2):
    """Inverse-distance weights to bone segments (like envelope skinning, deterministic)."""
    segs = [(b, Vector(BONES[b][0]), Vector(BONES[b][1])) for b in bones]

    def fn(p):
        p = Vector(p)
        ws = sorted(((1.0 / max(_seg_dist(p, a, b), 0.004) ** power, n) for n, a, b in segs),
                    reverse=True)[:keep]
        return {n: w for w, n in ws}
    return fn


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def w_chain(bones, z_top, z_bottom, top_bone=None, blend=0.6):
    """Weights along a hanging chain by height: z_top..z_bottom spread over `bones`,
    with an optional fixed `top_bone` holding the very top."""
    def fn(p):
        t = (z_top - p[2]) / max(z_top - z_bottom, 1e-6)
        seq = ([top_bone] if top_bone else []) + list(bones)
        x = max(0.0, min(1.0, t)) * (len(seq) - 1)
        i = min(int(x), len(seq) - 2) if len(seq) > 1 else 0
        f = x - i
        if len(seq) == 1:
            return {seq[0]: 1.0}
        f = smooth((f - (1 - blend) / 2) / blend) if blend < 1 else f
        return {seq[i]: 1 - f, seq[i + 1]: f}
    return fn


def w_skirt(z_waist, z_hem, top=("hips",), top_fn=None):
    """A robe skirt: the top follows the body, the lower part is shared between the four
    hem bones by the angle round the body."""
    hem_dirs = {"hem_F": Vector((0, -1, 0)), "hem_B": Vector((0, 1, 0)),
                "hem.L": Vector((1, 0, 0)), "hem.R": Vector((-1, 0, 0))}

    def fn(p):
        p = Vector(p)
        t = smooth((z_waist - p.z) / max(z_waist - z_hem, 1e-6) * 1.6)
        flat = Vector((p.x, p.y, 0))
        if flat.length < 1e-6:
            flat = Vector((0, -1, 0))
        flat.normalize()
        out = {}
        tops = top_fn(p) if top_fn else {top[0]: 1.0}
        for b, w in tops.items():
            out[b] = out.get(b, 0) + w * (1 - t)
        lobes = {b: max(0.0, flat.dot(d)) ** 2 for b, d in hem_dirs.items()}
        s = sum(lobes.values()) or 1
        for b, w in lobes.items():
            if w > 0:
                out[b] = out.get(b, 0) + t * w / s
        return out
    return fn


def weights_for(verts, fn):
    return [fn(Vector(v)) for v in verts]


# ---------------------------------------------------------------- posing
REST = {}       # bone -> rest matrix (armature space)
LEN = {}


def load_rest(rig):
    REST.clear()
    LEN.clear()
    for b in rig.data.bones:
        REST[b.name] = b.matrix_local.copy()
        LEN[b.name] = b.length


def rx(d):
    return Quaternion((1, 0, 0), math.radians(d))


def ry(d):
    return Quaternion((0, 1, 0), math.radians(d))


def rz(d):
    return Quaternion((0, 0, 1), math.radians(d))


def euler(x=0.0, y=0.0, z=0.0):
    """Rest-axis rotation: X first (pitch, + tips the top FORWARD and swings a hanging limb
    back), then Y (roll, + tips the top to the character's left), then Z (yaw, + turns the
    character to its left: the left shoulder goes back)."""
    return rz(z) @ ry(y) @ rx(x)


def two_bone(a: Vector, c: Vector, l1: float, l2: float, pole: Vector) -> Vector:
    """Knee/elbow position for a two-bone chain from a to c bending toward pole."""
    d_vec = c - a
    d = max(min(d_vec.length, (l1 + l2) * 0.9995), abs(l1 - l2) + 1e-4)
    dirn = d_vec.normalized() if d_vec.length > 1e-6 else Vector((0, 0, -1))
    aa = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - aa * aa, 0.0))
    perp = pole - dirn * pole.dot(dirn)
    if perp.length < 1e-6:
        perp = Vector((0, -1, 0)) - dirn * (-dirn.y)
    perp.normalize()
    return a + dirn * aa + perp * h


def solve(pose: dict) -> tuple[dict, dict]:
    """Evaluate a pose. Returns (basis, posed): per-bone (location, quaternion) basis to key,
    and per-bone posed armature-space matrices.

    pose[bone] = {"rot": Quaternion, "aim": Vector, "waim": Vector, "twist": deg,
                  "loc": Vector}
    pose["legs"] = {"L": {"ankle": Vector, "pole": Vector, "foot": Vector}, "R": {...}}
    """
    posed, basis = {}, {}
    legs = pose.get("legs", {})
    knees = {}
    for name in ORDER:
        parent = BONES[name][2]
        rest = REST[name]
        if parent:
            q = posed[parent] @ REST[parent].inverted() @ rest
        else:
            q = rest.copy()
        qr = q.to_quaternion()
        rest_r = rest.to_quaternion()
        spec = dict(pose.get(name, {}))
        side = name[-1] if name[-2:] in (".L", ".R") else None
        if side and name.startswith("thigh") and side in legs:
            leg = legs[side]
            a = q.translation.copy()
            l1, l2 = LEN[name], LEN["shin." + side]
            knee = two_bone(a, Vector(leg["ankle"]), l1, l2, Vector(leg.get("pole", (0, -1, 0))))
            knees[side] = knee
            spec = {"waim": knee - a}
        elif side and name.startswith("shin") and side in legs:
            spec = {"waim": Vector(legs[side]["ankle"]) - q.translation}
        elif side and name.startswith("foot") and side in legs and "foot" in legs[side]:
            spec = {"waim": Vector(legs[side]["foot"])}
        if "blade" in spec:
            # turn the hand so the held weapon's length (+Z of its socket) points this way
            blade_rest = BLADE_REST[name]
            hr = rest.to_quaternion()
            cur = qr @ (hr.inverted() @ blade_rest)
            turn = cur.rotation_difference(Vector(spec["blade"]).normalized())
            spec = {"rot_world": turn}
        rot_basis = Quaternion()
        if "rot" in spec:
            rot_basis = rest_r.inverted() @ spec["rot"] @ rest_r
        if "aim" in spec or "waim" in spec:
            if "aim" in spec:
                # parent's accumulated turn from rest, applied to a parent-frame direction
                ref = AIM_REF.get(name, parent)
                if ref:
                    delta = posed[ref].to_quaternion() @ REST[ref].to_quaternion().inverted()
                else:
                    delta = Quaternion()
                target = delta @ Vector(spec["aim"]).normalized()
            else:
                target = Vector(spec["waim"]).normalized()
            y_now = qr @ Vector((0, 1, 0))
            turn = y_now.rotation_difference(target)
            rot_basis = qr.inverted() @ turn @ qr
        if "rot_world" in spec:
            rot_basis = qr.inverted() @ spec["rot_world"] @ qr
        if spec.get("twist"):
            rot_basis = rot_basis @ Quaternion((0, 1, 0), math.radians(spec["twist"]))
        loc_basis = Vector()
        if "loc" in spec:
            loc_basis = qr.inverted() @ Vector(spec["loc"])
        sc = float(spec.get("scale", 1.0))
        m = Matrix.Translation(loc_basis) @ rot_basis.to_matrix().to_4x4() @ Matrix.Scale(sc, 4)
        posed[name] = q @ m
        basis[name] = (loc_basis, rot_basis, sc)
    return basis, posed


def head_pos(posed, name):
    return posed[name].translation.copy()


def tail_pos(posed, name):
    return posed[name] @ Vector((0, LEN[name], 0))


def key_pose(rig, basis: dict, frame: int, prev: dict):
    for name, (loc, rot, sc) in basis.items():
        pb = rig.pose.bones[name]
        pb.scale = (sc, sc, sc)
        pb.keyframe_insert("scale", frame=frame, group=name)
        q = rot.copy()
        if name in prev and prev[name].dot(q) < 0:
            q.negate()
        prev[name] = q
        pb.rotation_quaternion = q
        pb.location = loc
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=name)
        pb.keyframe_insert("location", frame=frame, group=name)
