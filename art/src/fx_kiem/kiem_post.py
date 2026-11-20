"""fx_kiem pixel pass (runs inside Blender's Python).  A copy of the additive branch of art/src/fx/fxpost.py
(the shared library is not edited) with ONE change: the palette snap only considers ramps that make sense for
light - the seven glow ramps plus the cool / neutral / gold solids that their dim fringes fall onto.

Why: snapping to the whole master palette sent the dim fringes of the glow onto skin / earth / wood / pink / leaf /
grass (violet+white -> pink, dim gold -> earth brown, dim green -> grass).  Those are legal colours but they read
as mud on a sword-qi sheet.  Every colour written is still an entry of art/palette.json (qc.py checks it).
"""
import json
import os

import numpy as np

import fxpost

LIGHT_RAMPS = ("spirit", "flame", "ice", "cosmic", "holy", "verdant", "thunder",       # glow ramps
               "steel", "stone", "bone", "hair", "blue", "purple", "teal", "jade", "gold")  # dim fringes


def _palette(names):
    here = os.path.dirname(os.path.abspath(__file__))
    doc = json.load(open(os.path.join(here, "..", "..", "palette.json"), encoding="utf-8"))
    cols = [doc.get("ink", "#0b0a10")]
    for n in names:
        cols += doc["ramps"][n]["colors"]
    return np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in cols], np.float32) / 255.0


PAL = _palette(LIGHT_RAMPS)
PAL_LAB = fxpost._oklab(PAL)
BLACK_LAB = fxpost._oklab(np.zeros((1, 3), np.float32))
R = fxpost.R


def snap(rgb):
    flat = rgb.reshape(-1, 3)
    lab = fxpost._oklab(np.clip(flat, 0, 1))
    d = ((lab[:, None, :] - PAL_LAB[None, :, :]) ** 2).sum(-1)
    idx = d.argmin(1)
    best = d[np.arange(len(idx)), idx]
    db = ((lab - BLACK_LAB) ** 2).sum(-1)
    return PAL[idx].reshape(rgb.shape), (db < best * 0.8).reshape(rgb.shape[:-1])


def process_add(frame6, halo, gamma=1.0):
    h = frame6.shape[0] // R
    rgb = np.clip(frame6[..., :3], 0, 1)
    f = rgb.reshape(h, R, h, R, 3).mean((1, 3))
    if halo > 0:
        f = np.maximum(f, halo * 1.25 * fxpost.blur(f, 1.3))
        f = np.maximum(f, halo * 0.8 * fxpost.blur(f, 2.6))
    f = np.clip(f, 0, 1) ** gamma
    col, nothing = snap(f)
    nothing |= f.max(-1) < 0.09
    out = np.zeros((h, h, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = 1.0
    out[nothing] = 0
    return (out * 255 + 0.5).astype(np.uint8)


def pack(fx, frame_paths, outdir):
    """same sheet layout and JSON as fxpost.pack (ART_PIPELINE section 4)."""
    assert fx.mode == "add"
    frames = [process_add(fxpost.read_png(p), fx.halo, fx.gamma) for p in frame_paths]
    n = len(frames)
    cols = n if n <= 8 else (5 if n % 5 == 0 else 6 if n % 6 == 0 else 8)
    rows = (n + cols - 1) // cols
    sheet = np.zeros((rows * fx.px, cols * fx.px, 4), np.uint8)
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols)
        sheet[r * fx.px:(r + 1) * fx.px, c * fx.px:(c + 1) * fx.px] = fr
    fxpost.write_png(os.path.join(outdir, fx.id + ".png"), sheet)
    meta = {
        "id": fx.id, "name_vi": fx.name_vi,
        "frame": {"w": fx.px, "h": fx.px}, "pivot": {"x": fx.pivot[0], "y": fx.pivot[1]},
        "sheet": fx.id + ".png", "cols": cols, "frames": n, "fps": fx.fps, "loop": bool(fx.loop),
        "blend": fx.mode, "ground": bool(fx.ground),
    }
    if getattr(fx, "extra", None):
        meta.update(fx.extra)
    with open(os.path.join(outdir, fx.id + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return frames
