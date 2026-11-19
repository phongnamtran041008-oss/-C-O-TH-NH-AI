"""Render-time toon conversion of ordinary Principled materials (bpy).

Every material gets a small node block appended (nodes named ``KIT_*``) and its own EEVEE
output made active. The block emits one of two flat images, switched by the view-layer
attribute ``kit_pass`` (a uniform, so switching never recompiles a shader):

  pass 0 (albedo): the material's base colour (its emission colour if it glows; for FX the
                   emission colour x strength), unlit
  pass 1 (data):   R = material id/255, G = tone code, B = view depth (0..1 over the
                   camera's depth window), alpha cut at 0.5

Tone code: 0 shadow, 1 base, 2 light (N.L against the kit's fixed key light, hard
thresholds), 3 metal highlight (N.H), 4 glow. All lighting is computed here from the
geometry normal; no lamps exist in the scene, so nothing is soft and nothing is random.

The original node tree is left in place (just not the active output). Do not save a .blend
after rendering through the kit.
"""
from __future__ import annotations

import bpy

PASS_PROP = "kit_pass"

# Tone thresholds on N.L (L = key light from the upper left, see scene.py). A surface
# facing the camera gets N.L ~ 0.62, i.e. base tone; surfaces turned to the upper left go
# light, surfaces turned right/down go into shadow.
T_SHADOW = 0.20
T_LIGHT = 0.72
T_SPEC = 0.955


def _principled(mat):
    nodes = mat.node_tree.nodes
    outs = [n for n in nodes if n.type == "OUTPUT_MATERIAL" and not n.name.startswith("KIT_")]
    active = next((n for n in outs if n.is_active_output), outs[0] if outs else None)
    if active and active.inputs[0].is_linked:
        n = active.inputs[0].links[0].from_node
        seen = 0
        while n is not None and seen < 8:        # walk through mix shaders to a BSDF
            if n.type in ("BSDF_PRINCIPLED", "EMISSION", "BSDF_DIFFUSE"):
                return n
            nxt = None
            for s in n.inputs:
                if s.is_linked and s.type == "SHADER":
                    nxt = s.links[0].from_node
                    break
            n, seen = nxt, seen + 1
    return next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None) or \
        next((n for n in nodes if n.type == "EMISSION"), None)


def _src(node, name):
    """(linked output socket or None, default value) of an input, None if missing."""
    if node is None or name not in node.inputs:
        return None, None
    s = node.inputs[name]
    if s.is_linked:
        return s.links[0].from_socket, getattr(s, "default_value", None)
    return None, getattr(s, "default_value", None)


def describe(mat) -> dict:
    """What the kit needs to know about a material: glow?, metal?, priority, forced ramp."""
    info = {"name": mat.name, "glow": False, "metal": False, "halo": 1,
            "priority": float(mat.get("kit_priority", 1.0)),
            "outline": bool(mat.get("kit_outline", 1))}
    if mat.get("kit_ramp"):
        info["ramp"] = str(mat["kit_ramp"])
    if not mat.use_nodes:
        return info
    p = _principled(mat)
    if p is None:
        return info
    if p.type == "EMISSION":
        _, col = _src(p, "Color")
        _, st = _src(p, "Strength")
        info["glow"] = (st or 0) > 0
        info["strength"] = float(st or 0)
    else:
        lc, col = _src(p, "Emission Color")
        ls, st = _src(p, "Emission Strength")
        lit = (lc is not None) or (col is not None and max(col[:3]) > 0.001)
        info["glow"] = bool(lit and (ls is not None or (st or 0) > 0))
        info["strength"] = float(st or 0)
        lm, met = _src(p, "Metallic")
        info["metal"] = bool((met or 0) >= 0.5)
    if "kit_metal" in mat:
        info["metal"] = bool(mat["kit_metal"])
    if "kit_glow" in mat:
        g = mat["kit_glow"]
        info["glow"] = bool(g)
        if isinstance(g, str) and g:
            info["glow_ramp"] = g
    info["halo"] = int(mat.get("kit_halo", 2 if info.get("strength", 0) >= 4 else 1))
    return info


def inject(mat, mid: int, light, half, depth_lo: float, depth_hi: float, fx: bool = False) -> dict:
    """Add (or update) the KIT block on this material. Returns describe(mat) + id."""
    if not mat.use_nodes:
        col = tuple(mat.diffuse_color)
        mat.use_nodes = True
        p = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if p is not None:
            p.inputs["Base Color"].default_value = col
    info = describe(mat)
    info["id"] = mid
    nt = mat.node_tree
    N = nt.nodes
    for n in [n for n in N if n.name.startswith("KIT_")]:
        N.remove(n)
    p = _principled(mat)

    def node(kind, name, **props):
        n = N.new(kind)
        n.name = n.label = "KIT_" + name
        n.location = (2000, -200 * len([x for x in N if x.name.startswith("KIT_")]))
        for k, v in props.items():
            setattr(n, k, v)
        return n

    def link(a, b):
        nt.links.new(a, b)

    def value_or_link(sock_in, src_name, fallback):
        ls, dv = _src(p, src_name)
        if ls is not None:
            link(ls, sock_in)
        else:
            v = dv if dv is not None else fallback
            try:
                sock_in.default_value = v
            except (TypeError, ValueError):
                sock_in.default_value = tuple(v)[:len(sock_in.default_value)]

    def math(op, a, b=None, name=""):
        m = node("ShaderNodeMath", f"m_{op}_{name}", operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, bpy.types.NodeSocket):
                link(v, m.inputs[i])
            else:
                m.inputs[i].default_value = float(v)
        return m.outputs[0]

    # ---- albedo
    if p is not None and p.type == "EMISSION":
        alb = node("ShaderNodeMix", "alb", data_type="RGBA")
        value_or_link(alb.inputs[6], "Color", (1, 1, 1, 1))
        alb.inputs[0].default_value = 0.0
        albedo = alb.outputs[2]
        alpha_sock = None
    else:
        alb = node("ShaderNodeMix", "alb", data_type="RGBA")
        if p is None:
            alb.inputs[6].default_value = tuple(mat.diffuse_color)
        else:
            value_or_link(alb.inputs[6], "Base Color", (0.8, 0.8, 0.8, 1))
            value_or_link(alb.inputs[7], "Emission Color", (0, 0, 0, 1))
        alb.inputs[0].default_value = 1.0 if info["glow"] else 0.0
        albedo = alb.outputs[2]
        alpha_sock = None
        if p is not None and "Alpha" in p.inputs:
            a = node("ShaderNodeMath", "alpha", operation="ADD")
            value_or_link(a.inputs[0], "Alpha", 1.0)
            a.inputs[1].default_value = 0.0
            alpha_sock = a.outputs[0]
    if fx and info["glow"]:
        # FX colour = emission colour x strength
        sc = node("ShaderNodeVectorMath", "fxscale", operation="SCALE")
        link(albedo, sc.inputs[0])
        ls, st = _src(p, "Strength" if p.type == "EMISSION" else "Emission Strength")
        if ls is not None:
            link(ls, sc.inputs["Scale"])
        else:
            sc.inputs["Scale"].default_value = float(st or 1.0)
        albedo = sc.outputs[0]

    # ---- data: tone code from N.L / N.H
    geo = node("ShaderNodeNewGeometry", "geo")
    flip = math("MULTIPLY_ADD", geo.outputs["Backfacing"], -2.0, "flip")
    flip.node.inputs[2].default_value = 1.0          # 1 - 2*backfacing
    nrm = node("ShaderNodeVectorMath", "nrm", operation="SCALE")
    link(geo.outputs["Normal"], nrm.inputs[0])
    link(flip, nrm.inputs["Scale"])
    ndl = node("ShaderNodeVectorMath", "ndl", operation="DOT_PRODUCT")
    link(nrm.outputs[0], ndl.inputs[0])
    ndl.inputs[1].default_value = tuple(light)
    ndh = node("ShaderNodeVectorMath", "ndh", operation="DOT_PRODUCT")
    link(nrm.outputs[0], ndh.inputs[0])
    ndh.inputs[1].default_value = tuple(half)
    ts = float(mat.get("kit_shadow", T_SHADOW))
    tl = float(mat.get("kit_light", T_LIGHT))
    b1 = math("GREATER_THAN", ndl.outputs["Value"], ts, "b1")
    b2 = math("GREATER_THAN", ndl.outputs["Value"], tl, "b2")
    band = math("ADD", b1, b2, "band")
    if info["glow"]:
        code = math("ADD", 4.0, 0.0, "code")
    elif info["metal"]:
        spec = math("GREATER_THAN", ndh.outputs["Value"], float(mat.get("kit_spec", T_SPEC)), "spec")
        rest = math("SUBTRACT", 3.0, band, "rest")
        code = math("MULTIPLY_ADD", spec, rest, "code")
        link(band, code.node.inputs[2])
    else:
        code = band
    g = math("MULTIPLY_ADD", code, 40.0 / 255.0, "g")
    g.node.inputs[2].default_value = 20.0 / 255.0
    cam = node("ShaderNodeCameraData", "cam")
    dz = math("SUBTRACT", cam.outputs["View Z Depth"], float(depth_lo), "dz")
    dn = math("DIVIDE", dz, float(depth_hi - depth_lo), "dn")
    dn.node.use_clamp = True
    comb = node("ShaderNodeCombineColor", "data")
    comb.inputs[0].default_value = mid / 255.0
    link(g, comb.inputs[1])
    link(dn, comb.inputs[2])

    # ---- switch, alpha, output
    attr = node("ShaderNodeAttribute", "pass", attribute_type="VIEW_LAYER", attribute_name=PASS_PROP)
    sw = node("ShaderNodeMix", "switch", data_type="RGBA")
    link(attr.outputs["Fac"], sw.inputs[0])
    link(albedo, sw.inputs[6])
    link(comb.outputs[0], sw.inputs[7])
    em = node("ShaderNodeEmission", "emit")
    link(sw.outputs[2], em.inputs[0])
    em.inputs[1].default_value = 1.0
    tr = node("ShaderNodeBsdfTransparent", "transp")
    mix = node("ShaderNodeMixShader", "mix")
    if alpha_sock is not None:
        if fx:
            link(alpha_sock, mix.inputs[0])
        else:
            link(math("GREATER_THAN", alpha_sock, 0.5, "cut"), mix.inputs[0])
    else:
        mix.inputs[0].default_value = 1.0
    link(tr.outputs[0], mix.inputs[1])
    link(em.outputs[0], mix.inputs[2])
    out = node("ShaderNodeOutputMaterial", "out")
    link(mix.outputs[0], out.inputs[0])
    for n in N:
        if n.type == "OUTPUT_MATERIAL" and n is not out:
            n.target = "CYCLES"                 # EEVEE must use the kit output
            n.is_active_output = False
    out.target = "EEVEE"
    out.is_active_output = True
    try:
        mat.surface_render_method = "BLENDED" if fx else "DITHERED"
    except (AttributeError, TypeError):
        pass
    mat.use_backface_culling = False
    mat["kit_toon"] = 1
    return info


def set_pass(scene, value: int) -> None:
    scene[PASS_PROP] = float(value)
    for vl in scene.view_layers:
        vl[PASS_PROP] = float(value)
