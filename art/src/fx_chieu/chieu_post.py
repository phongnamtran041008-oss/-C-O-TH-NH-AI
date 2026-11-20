"""fx_chieu pixel pass (inside Blender's Python, numpy).  Generalises art/src/fx_kiem/kiem_post.py (read only):

- frames may be non-square (w x h),
- additive sheets: area-average 6x -> 1x, 1-2 px halo, snap to the light ramps only (no mud), black -> alpha 0;
- alpha sheets (ice, vines, earth, wind, the standing bell): straight colour snapped to the ramps the sheet names
  (`fx.ramps`), alpha quantised to `alpha_levels` steps; the dark outline is modelled in the scene, not added here.

Every colour written is an entry of art/palette.json.  Nothing may touch the frame border: the pass reports it
(`edge` warnings) so the scene is fixed; it does not silently crop.
"""
import json
import os

import numpy as np

import fxpost

R = fxpost.R
LIGHT = ("spirit", "flame", "ice", "cosmic", "holy", "verdant", "thunder",
         "steel", "stone", "bone", "hair", "blue", "purple", "teal", "jade", "gold")
_DOC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "palette.json"),
                      encoding="utf-8"))
_CACHE = {}


def palette(names):
    key = tuple(names)
    if key not in _CACHE:
        cols = [_DOC.get("ink", "#0b0a10")]
        for n in names:
            cols += _DOC["ramps"][n]["colors"]
        pal = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in cols], np.float32) / 255.0
        _CACHE[key] = (pal, fxpost._oklab(pal))
    return _CACHE[key]


BLACK_LAB = fxpost._oklab(np.zeros((1, 3), np.float32))


def snap(rgb, names):
    pal, lab_p = palette(names)
    flat = rgb.reshape(-1, 3)
    lab = fxpost._oklab(np.clip(flat, 0, 1))
    d = ((lab[:, None, :] - lab_p[None, :, :]) ** 2).sum(-1)
    idx = d.argmin(1)
    best = d[np.arange(len(idx)), idx]
    db = ((lab - BLACK_LAB) ** 2).sum(-1)
    return pal[idx].reshape(rgb.shape), (db < best * 0.8).reshape(rgb.shape[:-1])


def down(a, h, w):
    return a.reshape(h, R, w, R, a.shape[-1]).mean((1, 3))


def process(frame6, fx):
    h, w = fx.h, fx.w
    names = fx.ramps or LIGHT
    if fx.mode == "add":
        f = down(np.clip(frame6[..., :3], 0, 1), h, w)
        if fx.halo > 0:
            f = np.maximum(f, fx.halo * 1.25 * fxpost.blur(f, 1.3))
            f = np.maximum(f, fx.halo * 0.8 * fxpost.blur(f, 2.6))
        f = np.clip(f, 0, 1) ** fx.gamma
        col, nothing = snap(f, names)
        nothing |= f.max(-1) < 0.09
        out = np.zeros((h, w, 4), np.float32)
        out[..., :3] = col
        out[..., 3] = 1.0
        out[nothing] = 0
        return (out * 255 + 0.5).astype(np.uint8)
    a6 = frame6[..., 3:4]
    A = down(a6, h, w)
    C = down(frame6[..., :3] * a6, h, w) / np.maximum(A, 1e-6)
    C, _ = snap(np.clip(C, 0, 1), names)
    A = np.clip(A[..., 0], 0, 1)
    lv = fx.alpha_levels
    Aq = np.round(A * lv) / lv
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = C
    out[..., 3] = Aq
    out[Aq == 0] = 0
    return (out * 255 + 0.5).astype(np.uint8)


def pack(fx, frame_paths, outdir):
    frames = [process(fxpost.read_png(p), fx) for p in frame_paths]
    n = len(frames)
    cols = n if n <= 8 else (5 if n % 5 == 0 else 6 if n % 6 == 0 else 8)
    rows = (n + cols - 1) // cols
    sheet = np.zeros((rows * fx.h, cols * fx.w, 4), np.uint8)
    bad = []
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols)
        sheet[r * fx.h:(r + 1) * fx.h, c * fx.w:(c + 1) * fx.w] = fr
        a = fr[..., 3]
        if a.max() == 0:
            bad.append("%d:empty" % i)
        elif a[0].any() or a[-1].any() or a[:, 0].any() or a[:, -1].any():
            bad.append("%d:edge" % i)
    fxpost.write_png(os.path.join(outdir, fx.id + ".png"), sheet)
    meta = {
        "id": fx.id, "name_vi": fx.name_vi,
        "frame": {"w": fx.w, "h": fx.h}, "pivot": {"x": fx.pivot[0], "y": fx.pivot[1]},
        "sheet": fx.id + ".png", "cols": cols, "frames": n, "fps": fx.fps, "loop": bool(fx.loop),
        "blend": fx.mode, "ground": bool(fx.ground),
    }
    with open(os.path.join(outdir, fx.id + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return bad
