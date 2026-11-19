"""Turn two flat full-size renders into one finished pixel-art frame (numpy only, no bpy).

Input per frame (both H x W x 4 float, rendered at `scale` x the target size):
  * albedo: linear base colour of every pixel (emission colour for glowing materials)
  * data:   R = material id / 255, G = tone code (shadow/base/light/spec/glow), B = depth 0..1,
            A = coverage (0 or 1)

Steps: toon colour per pixel (palette ramp shift by tone) -> block downscale choosing the
dominant colour (weighted mode, never an average) -> orphan clean-up -> inner lines ->
glow (edge/core + halo) -> 1 px selective outline. Output RGBA uint8, every colour from
the palette.
"""
from __future__ import annotations

import numpy as np

from . import palette as P

SHADOW, BASE, LIGHT, SPEC, GLOW = 0, 1, 2, 3, 4

DEFAULTS = dict(
    coverage=0.34,        # share of a block that must be drawn for the pixel to be drawn
    glow_weight=1.6,      # glow pixels win blocks more easily (thin runes survive)
    outline=True,         # 1 px outer outline
    outline_mode=4,       # 4- or 8-neighbourhood for the outer outline
    inner_lines=True,     # dark line where two parts would merge
    inner_de=0.10,        # OKLab distance under which two materials "merge"
    inner_depth=0.12,     # metres of depth jump that always gets an inner line
    orphans=True,
    wrap=False,           # tiles: neighbourhoods wrap around the edges
    halo=None,            # force halo width (0/1/2); default per material
)


# ------------------------------------------------------------------ colour helpers
def lin_to_srgb8(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    s = np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)
    return np.rint(s * 255).astype(np.int32)


def oklab_np(rgb8: np.ndarray) -> np.ndarray:
    c = rgb8.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                   [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    m2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    lms = np.cbrt(c @ m1.T)
    return lms @ m2.T


class PalArrays:
    """numpy views of a Palette, cached per palette object."""

    def __init__(self, pal: P.Palette):
        self.pal = pal
        self.rgb = np.array(pal.colors, dtype=np.uint8)
        self.lab = np.array(pal.lab)
        n = len(pal.colors)
        self.ramp_id = np.zeros(n, np.int32)       # which ramp (index into names)
        self.pos = np.zeros(n, np.int32)
        self.names = list(pal.ramps) + ["ink"]
        self.ramp_len = np.zeros(len(self.names), np.int32)
        self.ramp_start = np.zeros(len(self.names), np.int32)
        for gi, (r, p) in enumerate(pal.where):
            self.ramp_id[gi] = self.names.index(r)
            self.pos[gi] = p
        for k, name in enumerate(self.names):
            ids = pal.ramps.get(name, [pal.ink_index])
            self.ramp_start[k], self.ramp_len[k] = ids[0], len(ids)
        self.is_glow = np.array([pal.kind.get(pal.where[i][0]) == "glow" for i in range(n)])
        self.L = self.lab[:, 0]

    def shift(self, gi: np.ndarray, d) -> np.ndarray:
        """Move along the ramp of each colour by d (clamped)."""
        r = self.ramp_id[gi]
        p = np.clip(self.pos[gi] + d, 0, self.ramp_len[r] - 1)
        return self.ramp_start[r] + p

    def at_pos(self, gi: np.ndarray, p) -> np.ndarray:
        r = self.ramp_id[gi]
        p = np.clip(p, 0, self.ramp_len[r] - 1)
        return self.ramp_start[r] + p

    def nearest(self, rgb8: np.ndarray, cand: np.ndarray) -> np.ndarray:
        lab = oklab_np(rgb8)
        d = ((lab[:, None, :] - self.lab[None, cand, :]) ** 2).sum(-1)
        return cand[np.argmin(d, axis=1)]


_PA: dict[int, PalArrays] = {}


def pal_arrays(pal: P.Palette) -> PalArrays:
    k = id(pal)
    if k not in _PA:
        _PA[k] = PalArrays(pal)
    return _PA[k]


# ------------------------------------------------------------------ neighbourhoods
N4 = ((-1, 0), (1, 0), (0, -1), (0, 1))
N8 = N4 + ((-1, -1), (-1, 1), (1, -1), (1, 1))


def nb(a: np.ndarray, dy: int, dx: int, wrap: bool, fill):
    """a shifted so that out[y, x] = a[y+dy, x+dx] (fill outside, or wrap)."""
    if wrap:
        return np.roll(a, (-dy, -dx), axis=(0, 1))
    out = np.full_like(a, fill)
    h, w = a.shape[:2]
    ys, yd = (slice(dy, h), slice(0, h - dy)) if dy >= 0 else (slice(0, h + dy), slice(-dy, h))
    xs, xd = (slice(dx, w), slice(0, w - dx)) if dx >= 0 else (slice(0, w + dx), slice(-dx, w))
    out[yd, xd] = a[ys, xs]
    return out


# ------------------------------------------------------------------ main entry
def toon_labels(albedo: np.ndarray, data: np.ndarray, mats: dict, pal: P.Palette,
                restrict: list[str] | None):
    """Full-res palette label per pixel (-1 = empty), plus mat id, code, depth."""
    pa = pal_arrays(pal)
    alpha = data[..., 3] > 0.5
    mid = np.rint(data[..., 0] * 255).astype(np.int32)
    code = np.clip(np.rint((data[..., 1] * 255 - 20) / 40), 0, 4).astype(np.int32)
    depth = data[..., 2].astype(np.float32)
    rgb = lin_to_srgb8(albedo[..., :3])
    label = np.full(alpha.shape, -1, np.int32)
    if not alpha.any():
        return label, mid, code, depth
    key = (mid.astype(np.int64) << 24) | (rgb[..., 0] << 16) | (rgb[..., 1] << 8) | rgb[..., 2]
    ys, xs = np.nonzero(alpha)
    k = key[ys, xs]
    uniq, inv = np.unique(k, return_inverse=True)
    u_mid = (uniq >> 24).astype(np.int32)
    u_rgb = np.stack([(uniq >> 16) & 255, (uniq >> 8) & 255, uniq & 255], -1)
    base = np.zeros(len(uniq), np.int32)
    glow_core = np.zeros(len(uniq), np.int32)
    default_cand = np.array(pal.base_candidates(restrict), np.int32)
    for m in np.unique(u_mid):
        sel = u_mid == m
        info = mats.get(int(m), {})
        if info.get("glow"):
            gname = info.get("glow_ramp") or pal.glow_ramp_for(tuple(u_rgb[sel][0]))
            glow_core[sel] = pal.at(gname, 99)
        ramp = info.get("ramp")
        cand = np.array(pal.base_candidates([ramp]), np.int32) if ramp else default_cand
        base[sel] = pa.nearest(u_rgb[sel], cand)
    c = code[ys, xs]
    b = base[inv]
    lab = b.copy()
    lab = np.where(c == SHADOW, pa.shift(b, -1), lab)
    lab = np.where(c == LIGHT, pa.shift(b, 1), lab)
    lab = np.where(c == SPEC, pa.at_pos(b, 99), lab)
    lab = np.where(c == GLOW, glow_core[inv], lab)
    label[ys, xs] = lab
    return label, mid, code, depth


def downscale(label, mid, code, depth, scale: int, mats: dict, opt: dict):
    """Dominant label of each scale x scale block (weighted mode), with its material,
    code and mean depth. Blocks below the coverage threshold are empty (-1)."""
    H, W = label.shape
    h, w = H // scale, W // scale
    s = scale

    def blocks(a):
        return a[:h * s, :w * s].reshape(h, s, w, s).swapaxes(1, 2).reshape(h, w, s * s)

    L, M, C, D = blocks(label), blocks(mid), blocks(code), blocks(depth)
    filled = (L >= 0).sum(-1)
    weight = np.ones(L.shape, np.float32)
    prio = {m: float(i.get("priority", 1.0)) for m, i in mats.items()}
    if prio:
        pw = np.ones(256, np.float32)
        for m, p in prio.items():
            if 0 <= m < 256:
                pw[m] = p
        weight = pw[np.clip(M, 0, 255)]
    weight = np.where(C == GLOW, weight * opt["glow_weight"], weight)
    weight = np.where(L >= 0, weight, 0)
    key = np.where(L >= 0, L.astype(np.int64) * 256 + M, -1)
    uniq = np.unique(key)
    uniq = uniq[uniq >= 0]
    best = np.full((h, w), -1, np.int64)
    bestw = np.zeros((h, w), np.float32)
    for u in uniq:
        wsum = (weight * (key == u)).sum(-1)
        better = wsum > bestw
        best[better] = u
        bestw[better] = wsum[better]
    # a block is drawn when enough of it is covered, or a priority part owns it outright
    prio_px = np.zeros((h, w), bool)
    if prio:
        pblock = (np.where(L >= 0, weight, 0) > 1.01).sum(-1)
        prio_px = pblock >= max(2, int(0.2 * s * s))
    drawn = (filled >= opt["coverage"] * s * s) | prio_px
    best = np.where(drawn, best, -1)
    out_l = np.where(best >= 0, best // 256, -1).astype(np.int32)
    out_m = np.where(best >= 0, best % 256, 0).astype(np.int32)
    sel = (key == best[..., None]) & (best[..., None] >= 0)
    cnt = np.maximum(sel.sum(-1), 1)
    out_d = np.where(sel, D, 0).sum(-1) / cnt
    out_c = np.where(sel, C, 0).max(-1)
    return out_l, out_m, out_c, out_d.astype(np.float32)


def clean_orphans(L, M, C, mats, wrap):
    """Remove one-pixel speckle: a pixel whose colour no 8-neighbour shares (inside the
    sprite), lone drawn pixels, and one-pixel holes."""
    h, w = L.shape
    op = L >= 0
    same = np.zeros(L.shape, np.int32)
    opn = np.zeros(L.shape, np.int32)
    for dy, dx in N8:
        n = nb(L, dy, dx, wrap, -1)
        same += (n == L) & op
        opn += n >= 0
    keep = np.isin(C, (SPEC, GLOW))
    prio = np.array([float(mats.get(int(m), {}).get("priority", 1)) > 1 for m in range(256)])
    keep |= prio[np.clip(M, 0, 255)]
    L2 = L.copy()
    ys, xs = np.nonzero(op & (same == 0) & (opn >= 5) & ~keep)
    for y, x in zip(ys, xs):
        votes = {}
        for dy, dx in N8:
            yy, xx = y + dy, x + dx
            if wrap:
                yy, xx = yy % h, xx % w
            elif not (0 <= yy < h and 0 <= xx < w):
                continue
            v = L[yy, xx]
            if v >= 0:
                votes[v] = votes.get(v, 0) + (2 if M[yy, xx] == M[y, x] else 1)
        if votes:
            L2[y, x] = max(sorted(votes), key=lambda k: votes[k])
    L2[op & (opn == 0)] = -1                               # lone pixels in the air
    # one-pixel holes
    n4 = [nb(L2, dy, dx, wrap, -1) for dy, dx in N4]
    hole = (L2 < 0) & np.all([n >= 0 for n in n4], axis=0)
    for y, x in zip(*np.nonzero(hole)):
        L2[y, x] = n4[0][y, x]
    return L2


def no_outline(mats) -> np.ndarray:
    """bool per material id: True for materials with kit_outline = 0 (contact shadows,
    decals): no outline around them, no inner line against them."""
    a = np.zeros(256, bool)
    for m, i in mats.items():
        if 0 <= m < 256 and not i.get("outline", True):
            a[m] = True
    return a


def inner_lines(L, M, C, D, pa: PalArrays, mats, opt):
    """Darken the farther pixel where two parts meet and would merge: different materials
    with near colours, or any big depth jump (an arm in front of the body)."""
    op = L >= 0
    lab = pa.lab[np.clip(L, 0, None)]
    mark = np.zeros(L.shape, bool)
    prio = np.array([float(mats.get(int(m), {}).get("priority", 1)) > 1 for m in range(256)])
    noline = no_outline(mats)
    protect = np.isin(C, (GLOW,)) | prio[np.clip(M, 0, 255)] | noline[np.clip(M, 0, 255)]
    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nL = nb(L, dy, dx, opt["wrap"], -1)
        nM = nb(M, dy, dx, opt["wrap"], 0)
        nD = nb(D, dy, dx, opt["wrap"], 0.0)
        nlab = nb(lab, dy, dx, opt["wrap"], 0.0)
        both = op & (nL >= 0)
        de = np.sqrt(((lab - nlab) ** 2).sum(-1))
        merge = (M != nM) & (de < opt["inner_de"])
        jump = (D - nD) * opt["depth_range"] > opt["inner_depth"]
        farther = D > nD
        mark |= both & farther & (merge | jump) & ~protect & ~noline[np.clip(nM, 0, 255)]
    L2 = L.copy()
    L2[mark] = pa.shift(L[mark], -2)
    return L2


def glow_and_outline(L, M, C, pa: PalArrays, pal: P.Palette, mats, opt):
    """Glow edge/core colours, halo rings into empty space, then the outer outline."""
    wrap = opt["wrap"]
    h, w = L.shape
    op = L >= 0
    glow = op & pa.is_glow[np.clip(L, 0, None)]
    out = L.copy()
    if glow.any():
        n4 = [nb(glow, dy, dx, wrap, False) for dy, dx in N4]
        edge = glow & ~np.all(n4, axis=0)
        out[glow & ~edge] = pa.at_pos(L[glow & ~edge], 3)
        out[edge] = pa.at_pos(L[edge], 2)
        # halo: ring 1 = halo near, ring 2 = halo far on a checker
        halo_w = np.zeros(256, np.int32)
        for m, i in mats.items():
            if 0 <= m < 256:
                halo_w[m] = int(opt["halo"] if opt["halo"] is not None else i.get("halo", 1))
        gw = np.where(glow, halo_w[np.clip(M, 0, 255)], 0)
        ring_src = np.where(glow, L, -1)
        ring1 = np.full(L.shape, -1, np.int32)
        for dy, dx in N8:
            s = nb(ring_src, dy, dx, wrap, -1)
            sw = nb(gw, dy, dx, wrap, 0)
            take = (~op) & (s >= 0) & (sw >= 1) & (ring1 < 0)
            ring1[take] = pa.at_pos(s[take], 1)
        out[ring1 >= 0] = ring1[ring1 >= 0]
        far_src = np.where(glow & (gw >= 2), L, -1)
        grown = far_src.copy()
        for _ in range(2):
            g2 = grown.copy()
            for dy, dx in N8:
                s = nb(grown, dy, dx, wrap, -1)
                g2 = np.where((g2 < 0) & (s >= 0), s, g2)
            grown = g2
        yy, xx = np.mgrid[0:h, 0:w]
        far = (out < 0) & (grown >= 0) & ((yy + xx) % 2 == 0)
        out[far] = pa.at_pos(grown[far], 0)
    if opt["outline"]:
        solid = (out >= 0) & op & ~glow & ~no_outline(mats)[np.clip(M, 0, 255)]
        hood = N4 if opt["outline_mode"] == 4 else N8
        best = np.full(L.shape, -1, np.int32)
        bestL = np.full(L.shape, 9.0)
        for dy, dx in hood:
            s = nb(np.where(solid, out, -1), dy, dx, wrap, -1)
            sL = np.where(s >= 0, pa.L[np.clip(s, 0, None)], 9.0)
            take = (out < 0) & (s >= 0) & (sL < bestL)
            best[take] = s[take]
            bestL[take] = sL[take]
        ol = best >= 0
        if ol.any():
            src = best[ol]
            col = pa.at_pos(src, 0)
            dark = pa.pos[src] <= 1                 # bordering a dark tone: use ink
            col = np.where(dark | pa.is_glow[src], pal.ink_index, col)
            out[ol] = col
    return out


def pixelise(albedo, data, scale: int, mats: dict, pal: P.Palette | None = None,
             restrict: list[str] | None = None, depth_range: float = 1.0, ids_out=None,
             **kw) -> np.ndarray:
    """Full pipeline -> H/scale x W/scale x 4 uint8 RGBA. If `ids_out` is a list, the
    final material id per pixel (0 = empty or outline) is appended to it."""
    pal = pal or P.load()
    pa = pal_arrays(pal)
    opt = dict(DEFAULTS, **kw)
    opt["depth_range"] = depth_range
    label, mid, code, depth = toon_labels(albedo, data, mats, pal, restrict)
    L, M, C, D = downscale(label, mid, code, depth, scale, mats, opt)
    if opt["orphans"]:
        L = clean_orphans(L, M, C, mats, opt["wrap"])
    if opt["inner_lines"]:
        L = inner_lines(L, M, C, D, pa, mats, opt)
    L = glow_and_outline(L, M, C, pa, pal, mats, opt)
    if ids_out is not None:
        ids_out.append(np.where((L >= 0) & (M > 0), M, 0).astype(np.int32))
    return to_rgba(L, pa)


def to_rgba(L, pa: PalArrays) -> np.ndarray:
    h, w = L.shape
    out = np.zeros((h, w, 4), np.uint8)
    op = L >= 0
    out[op, :3] = pa.rgb[L[op]]
    out[op, 3] = 255
    return out


def pixelise_fx(color, scale: int, pal: P.Palette | None = None, ramps: list[str] | None = None,
                alpha_levels: int = 16, halo: int = 2, levels=(0.08, 0.28, 0.50, 0.74)) -> np.ndarray:
    """FX frames: soft alpha allowed, drawn additively in game.

    Each block's colour picks a glow ramp (nearest hue among `ramps`, default all glow
    ramps); its *intensity* (brightness x coverage) picks the position on that ramp
    (far halo / near halo / edge / core at the `levels` thresholds), so FX come out
    saturated with a white-hot core instead of averaged grey. Alpha follows intensity.
    Then a soft halo of `halo` rings (near halo colour at ~45 %, far halo at ~22 %)."""
    pal = pal or P.load()
    pa = pal_arrays(pal)
    H, W = color.shape[:2]
    h, w = H // scale, W // scale
    c = color[:h * scale, :w * scale].astype(np.float64)
    a = np.clip(c[..., 3], 0, 1)
    pre = np.clip(c[..., :3], 0, 1) * a[..., None]
    pre = pre.reshape(h, scale, w, scale, 3).mean((1, 3))
    am = a.reshape(h, scale, w, scale).mean((1, 3))
    rgb = np.where(am[..., None] > 1e-4, pre / np.maximum(am[..., None], 1e-4), 0)
    inten = rgb.max(-1) * np.sqrt(am)          # thin strokes stay bright
    names = ramps or pal.glow_ramps()
    out = np.zeros((h, w, 4), np.uint8)
    on = inten >= levels[0]
    if not on.any():
        return out
    # ramp per pixel: compare the normalised colour with each ramp's edge colour
    norm = rgb / np.maximum(rgb.max(-1, keepdims=True), 1e-4)
    edges = np.array([pal.at(n, 2) for n in names], np.int32)
    ramp_of = np.zeros((h, w), np.int32)
    ramp_of[on] = pa.nearest(lin_to_srgb8(norm[on]), edges)
    pos = np.zeros((h, w), np.int32)
    for k, t in enumerate(levels[1:], start=1):
        pos[inten >= t] = k
    L = np.full((h, w), -1, np.int32)
    L[on] = pa.at_pos(ramp_of[on], pos[on])
    A = np.zeros((h, w), np.float64)
    A[on] = np.clip(0.45 + inten[on], 0, 1)
    # soft halo rings around the bright parts
    src = np.where(on & (pos >= 1), ramp_of, -1)
    for ring, (p_ring, a_ring) in enumerate(((1, 0.45), (0, 0.22))[:halo]):
        grown = np.full((h, w), -1, np.int32)
        for dy, dx in N8:
            s = nb(src, dy, dx, False, -1)
            grown = np.where((grown < 0) & (s >= 0), s, grown)
        new = (L < 0) & (grown >= 0)
        L[new] = pa.at_pos(grown[new], p_ring)
        A[new] = a_ring
        src = np.where(new, grown, src)
    drawn = L >= 0
    out[drawn, :3] = pa.rgb[L[drawn]]
    q = np.clip(np.rint(A[drawn] * alpha_levels) / alpha_levels, 1 / alpha_levels, 1)
    out[drawn, 3] = np.rint(q * 255).astype(np.uint8)
    return out
