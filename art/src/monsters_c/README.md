# MONSTERS_C: seven new monsters, modelled, rigged, animated and rendered in Blender

## Production brief (blender-director)

**Type:** creatures: 4 normal (48×48, pivot 24,42) and 3 elite (64×64, pivot 32,56), each with a
dị chủng colour variant (`<id>_di`, same model, a second material colour/ramp set).
**Target:** pixel sprites for the game client (`client/assets/v2/monsters/`), rendered only
through the shared kit (`tools/blender/kit/`): 35° orthographic camera, 38 px per metre, 3-tone
cel shading on the master palette, 1 px outline, glow only where the creature has it.
**Style:** xianxia monsters at the MONSTERS_A bar. Readable black silhouettes, believable
anatomy (real pangolin, crocodile, raptor and butterfly reference), big simple shapes, glowing
eyes or face where there is one. No text, digits or Chinese characters anywhere.
**Lands:** Kiếm Trủng Sơn (steel, rust red, sword shards), Lưu Vân Cốc (cloud white, sky blue,
thunder), Vạn Tượng Trạch (blood red, marsh green, pale ghost fire), Lôi Kiếp Đài (thunder).
**Poly budget:** under 4k triangles per creature (low-poly solids at sprite scale); no textures.
Colour comes from Principled base colours given as **palette hex codes** (`common.hx`), so every
material lands on the palette entry that was meant (see "My choices").
**Pivot:** the ground point under the middle of the footprint; hovering creatures carry a flat
contact shadow there (like Kiếm Linh).
**Animation:** one armature per creature, the six contract clips: `idle` 4, `walk` 6, `windup` 4
(held telegraph), `attack` 4 (`events.attack.hit` = 1, the impact frame), `hit` 2, `die` 6;
four facings.
**Export:** kit `render_animated` sheets `<id>` and `<id>_di`; `.blend` files in
`art/blender/monsters_c/`.

### Active skills
1. blender-director: this brief, pipeline order, the validation gate.
2. creature-artist: anatomy grounding per body type (pangolin, crocodile, raptor, butterfly,
   hollow armour, lantern, ball lightning), silhouette tested from the 35° gameplay camera, rig
   joints planned during blockout.
3. blender-modeler: everything built from numbers in scripts (`plate`, `tube`, `ball`, `aim`),
   `COL_` / `SM_` / `MAT_` / `ARM_` naming, nothing saved by hand.
4. rigging: bone-parented hard parts, distance-weighted skins for soft parts (tails, cape, wisps),
   two-bone leg IK (MONSTERS_A `quadrupeds.Legs`), quaternion poses for the tilted lightning rings.
5. animation: pose tables with anticipation, follow-through and lag (hind wings, hands of the
   hawk's wings, tassels, capes and tails trail by a frame); loops close on themselves.
6. pixel-art-style: texel discipline - features at least 1 px (0.027 m), thin glowing lines
   without halo, compact silhouettes for 48 px.
7. stylized-style / fantasy-worlds / genre-rpg: shape language (round friendly butterfly,
   triangular hawk and crocodile, blocky armour), land colour identity, `_di` as the rarer look.
8. qa-review: fit checks before rendering, kit QC, contact sheets, 5× zoom crops, look rounds.

### Pipeline (all scripted)
- [x] Reference and planning (contract, kit API, MONSTERS_A worked example and previews)
- [x] Blockout and silhouette (kit renders from the first pass: about 20 s per creature)
- [x] Modelling from numbers, rig and clips (one file per creature)
- [x] Fit checks (`--fit`, `fitdir.py`), kit QC, contact sheets, zoom crops
- [x] Look-fix rounds (logged below)

## Files

| File | What |
|---|---|
| `build.py` | venv entry point: one headless Blender per creature (at most 2 at once), then QC, contact sheets, overview |
| `scene.py` | inside Blender: build one creature, save `art/blender/monsters_c/<id>.blend`, optional fit check, render `<id>` and `<id>_di` |
| `creatures_c.py` | the table id → (name_vi, frame size, builder, render options) |
| `common.py` | imports the MONSTERS_A helpers read-only; adds `hx` (palette hex → linear colour), `plate` (flat outlined plates: wings, feathers, scales, blades), `zigzag`/`bolt` (lightning), `hover_shadow`, `about` (turn the whole creature about a point), `write_clips` |
| `pangolin.py` | Thiết Giáp Thú |
| `ghost_swordsman.py` | Vong Hồn Kiếm Sĩ |
| `butterfly.py` | Vân Điệp |
| `hawk.py` | Lôi Ưng |
| `lantern.py` | U Minh Đăng |
| `crocodile.py` | Huyết Ngạc |
| `ball_lightning.py` | Lôi Linh |
| `zoom.py` | 5× crops of key frames (or `--all` frames) with optional existing monsters beside them, into `art/render/monsters_c/zoom_<id>.png` |
| `fitdir.py` | Blender-side: per frame and facing, the lowest projected row and side extents of one clip, with the part that is lowest (for balancing lying poses) |

```
python art/src/monsters_c/build.py                       # everything (about 6 min, 2 Blenders)
python art/src/monsters_c/build.py --only loi_ung         # one creature (comma list allowed)
python art/src/monsters_c/build.py --no-render --fit      # .blend files + fit check only
python art/src/monsters_c/zoom.py huyet_ngac --vs ma_tran_thu
blender -b art/blender/monsters_c/<id>.blend --python art/src/monsters_c/fitdir.py -- die
```

Outputs: `client/assets/v2/monsters/<id>.png/.json` and `<id>_di.png/.json`,
`art/preview/monsters_c_<id>.png` (every clip × every facing, both looks, 3×),
`art/preview/monsters_c.png` (all seven, every frame of every clip facing right, both looks,
with the Luyện Khí player at the same scale on the ground line).
