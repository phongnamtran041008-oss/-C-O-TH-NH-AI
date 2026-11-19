# Art kit (`tools/blender/kit/`)

One renderer and packer for every v2 sprite, so that all batches share one look. You build a
model in Blender with ordinary Principled materials; the kit renders it, turns it into
3-tone pixel art on the master palette (`art/palette.json`), packs the files the game reads
(docs/ART_PIPELINE.md section 4), checks them and draws the contact sheet.

Reference result: `art/preview/kit_samples.png` (built by `art/src/kit_samples/`, which is
also the longest worked example).

## 1. How a batch runs

Two scripts:

* `art/src/<batch>/build.py`: run with the venv python. Starts Blender and then QC + preview.
* `art/src/<batch>/scene.py`: runs **inside** headless Blender. Builds the models, saves the
  .blend, renders through the kit.

```python
# art/src/my_batch/build.py
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
from kit import launcher

code = launcher.run_blender(Path(__file__).with_name("scene.py"), "my_batch", sys.argv[1:])
# optional: blend="art/blender/my_batch/x.blend" opens that file first
if code == 0:
    code = 1 if launcher.finish("my_batch", ["client/assets/v2/monsters"]) else 0
sys.exit(code)
```

```python
# art/src/my_batch/scene.py   (inside Blender; `import kit` works here)
import kit.api as kit
args = kit.args()                    # whatever build.py passed after the script
... build models ...
kit.save_blend("art/blender/my_batch/my_batch.blend")   # save BEFORE rendering
kit.render_animated(...)            # see below
```

`launcher.finish` runs `qc.py` on each folder and writes `art/preview/<batch>.png`.
Several batches may run at once: each Blender writes its temp files to
`art/render/<batch>/_tmp_<pid>/` and its log to `art/render/<batch>/blender_*.log`.

Stand-alone tools (venv python):
`python tools/blender/kit/qc.py <folder or .json>...` and
`python tools/blender/kit/contact.py <out.png> <folder or json>...`.

## 2. What your model must look like

* 1 unit = 1 m. Origin on the ground between the feet (props: at the base). Characters face
  **-Y**. The player is about 1.0 m tall.
* Weapons and hand items: modelled along **+Z**, grip centred on the origin, blade up, flat
  side facing -Y. The same object is used for the icon and, parented to the hand bone, for
  the layer.
* Materials: Principled BSDF. The kit reads **Base Color** (value or any linked node, e.g.
  a colour attribute), **Metallic** (>= 0.5 gets a hard highlight), **Emission Color +
  Strength** (> 0 = glow), **Alpha** (cut at 0.5; FX keep soft alpha). Plain Emission
  shaders work too. Everything else is ignored.
* Clips are actions named after the clip (`idle`, `slash`, ...) on the armature. The kit
  samples N evenly spaced frames over the action's frame range (a loop does not repeat its
  last key, so key the loop's first pose again at the end).
* Small features (eyes, gems, flowers) must be at least ~1 px = 0.027 m across at the
  standard scale, and should get `kit_priority` (below) so the downscale keeps them.
* Do not save the .blend after rendering: the kit edits materials in memory.

Optional custom properties on a material (Object Properties are not used):

| property | effect |
|---|---|
| `kit_ramp` = `"gold"` | force the palette ramp (`skin hair earth wood stone steel gold jade leaf blue red purple bone grass pink paper teal`) |
| `kit_glow` = `"spirit"` | force glow (and its ramp: `spirit flame ice cosmic holy verdant thunder`), or `0` to turn glow off |
| `kit_priority` = `3.0` | wins pixel blocks it covers ≥ 20 % of (eyes, gems, runes) and is never cleaned away |
| `kit_metal` = `1` / `0` | force the metal highlight on/off |
| `kit_halo` = `0..2` | glow halo width in px (default 1, 2 when emission strength ≥ 4) |
| `kit_shadow`, `kit_light` | N·L thresholds of the 3 tones (default 0.20 and 0.72); `kit_shadow=2, kit_light=3` = always the shadow tone |
| `kit_outline` = `0` | no 1 px outline around this material and no inner line against its neighbours (contact shadows, ground decals) |

## 3. The API (`import kit.api as kit`)

Every `out_dir` is relative to the repository. All render functions return the JSON dict they
wrote. Any function also takes `palette=` (path) and `restrict=[ramp names]` (snap base
colours only to these ramps) and pixel options (`coverage=0.34`, `outline=True`,
`inner_lines=True`, `inner_depth=0.12`, `orphans=True`).

### Animated character / monster / beast
```python
kit.render_animated(rig, "dao_si_luyen_khi", kit.PLAYER_CLIPS, "client/assets/v2/chars",
                    name_vi="Đạo Sĩ Luyện Khí", kind="player", exclude=held_weapon)
kit.render_animated(rig, "soi_xam", kit.MONSTER_CLIPS, "client/assets/v2/monsters",
                    name_vi="Sói Xám", kind="monster")              # 48x48
```
* `rig`: armature, root object, collection or list; all descendants are drawn.
* `clips`: `{"slash": {"frames": 6, "fps": 14, "loop": False, "events": {"hit": 3},
  "action": "slash"}}`. Ready-made: `PLAYER_CLIPS`, `MONSTER_CLIPS`, `BOSS_EXTRA_CLIPS`
  (contract section 3). Take a subset with a dict comprehension while you work.
* `kind` sets frame / pivot / scale (defaults below are the 35° ones; the 15° player passes
  its own `frame`, `pivot`, `ppm`): player 64×64 pivot (32,54); monster and beast 48×48
  (24,42); elite 64×64 (32,56); boss 96×96 (48,86); all at `ppm=38` px per metre. Override
  with `frame=(w,h)`, `pivot=(x,y)`, `ppm=`. A bigger monster: raise `ppm`, not the model.
* Four facings by turning the model (light stays upper-left): `down left up right`.
* `exclude=`: objects left out (the held weapon). `on_frame(clip, dir, i)`: hook after posing.
* `elevation=15.0` (v1.3): camera angle above the horizon (default 35, today's look). The
  player (contract §2) uses 15 in a 96x96 frame:
  `kind="player", frame=(96, 96), pivot=(48, 84), ppm=..., elevation=15.0`. The pivot is
  still the projected ground origin and the key light stays upper-left on screen. Written
  to the JSON as `render.elevation`; `render_layer` reuses it. QC's lowest-row band scales
  with sin(elevation) (and with the frame size), so 15° feet must sit closer to the pivot.
* `snap=True, snap_to="head"` (v1.3): per frame, the camera is moved sideways/up by the
  sub-pixel amount that puts that bone (of the rig) or object exactly on the centre of a
  final pixel before the 6x downscale, so eyes and other small features keep the same
  pixel shape from frame to frame. Cost: the rest of the body can shift by up to half a
  pixel against the nominal pivot (after rounding, feet may move 1 px between frames).
  Written as `render.snap_to`; `render_layer` applies the same shift, so the weapon stays
  on the hand.
* `ground_clips=["die", "hit"]`: clips that lie down or collapse. QC lets their lowest row
  reach a quarter of the frame below the pivot (still not above it). Default `die`, `sleep`
  (those are never held to the standing rule anyway). Weapon layers inherit the list.
* `qc_ignore=held_sword` (v1.4): objects baked into the sheet (a held weapon) that QC leaves
  out of the lowest-row, feet and bottom-edge checks, so a sword tip resting low does not
  fail the character. The kit measures each frame without those objects' pixels (and
  their outline) and writes `render.qc_ignore` + `render.qc_frames`. Their materials must
  not be shared with the body (the kit warns and keeps shared ones in).
* QC requires all contract clips for kinds player/monster/elite/beast/boss, and holds
  idle/walk/slash/cast/shoot/hit/windup/attack to the standing rule: the lowest row within
  max(4, frame/12 × sin(elevation)/sin 35°) px of the pivot. In idle/walk the feet must
  not jitter or drift: up to 64 px frames, the lowest row may move 2 px and the middle of
  the lowest 3 rows may drift 4 px from the pivot x (unchanged since v1.0); above 64 px
  both limits scale with frame/64 (96 px: 3 and 6) and the **planted foot** is judged:
  only pixels within a quarter frame of the pivot x count, and the drift is measured on
  the run of the lowest row nearest the pivot, so the swinging foot may stride freely.

### Weapon layer (drawn over the character, same grid)
```python
kit.render_layer(sword, rig, "client/assets/v2/chars/dao_si_luyen_khi.json",
                 "client/assets/v2/weapons", "kiem_thep", name_vi="Kiếm Thép")
```
The weapon (parented to the hand bone) is rendered through the character's clips, frame
counts, pivot and scale, read from the character's JSON; the body is a holdout, so where the
body hides the weapon the layer is transparent. Render the character first.

### Icons (32×32 atlas)
```python
kit.render_icons("vu_khi_kiem", [
    {"id": "kiem_go", "objects": sword1, "name_vi": "Kiếm Gỗ", "grade": 1},
    {"id": "kiem_linh", "objects": sword5, "name_vi": "Linh Kiếm", "grade": 5},
], "client/assets/v2/icons")
```
Each object is posed diagonally (+Z to the upper right, `angle=45`, turned `spin=25`
degrees about its own axis, optional `tilt`) and fitted to `size=26` px. Upright things
(gourds, pills, books): `"angle": 0`. One shared scale for a set: give each icon the same
`"ppm"`. Per-icon `"frame"` picks a scene frame.

### FX (soft alpha, additive)
```python
kit.render_fx("chem_kiem", fx_objects, "client/assets/v2/fx", frames=[1, 2, 3, 4, 5],
              size=64, fps=14, loop=False, blend="add", ground=False)
kit.render_fx("tran_1", circle, "client/assets/v2/fx", frames=list(range(1, 9)),
              size=96, fps=8, loop=True, ground=True)      # ground circle -> ellipse at 35°
```
Model FX as emissive surfaces (Emission Color × Strength; Principled Alpha, may be linked to
a colour attribute or texture for soft edges). Colour chooses the glow ramp, brightness ×
coverage chooses halo / edge / core on it, so 1.5-3 strength reads as a hot core. `halo=0..2`
soft rings, `ramps=["flame"]` to restrict, `mode="top"` for a straight-down decal. Animate
with keyframes (`hide_render` per stage is fine).

### Ground tiles (16×16, seamless)
```python
kit.render_tiles("rung_truc", {
    "grass": [grass_a, grass_b, grass_c, grass_d],          # 4 variants
    "path":  [path_a, path_b, path_c, path_d],
    "water": [{"objects": water, "frame": f} for f in (1, 2, 3, 4)],
    "cliff_n": [{"objects": cliff_n, "wrap": False}],
}, "client/assets/v2/tiles")
```
Each entry is one tile, modelled in a `kit.TILE_M` (0.421 m) square centred on the origin,
seen straight down. With `wrap=True` (default) the kit renders the 8 neighbouring copies too,
so anything over an edge comes back on the other side: tiles are seamless by construction,
and every tile gets a wrap score in the JSON (`render.wrap_check`, > 2 = visible seam; QC
fails it). Use `"wrap": False` for edges and transitions. Tiles have no outline and no
inner lines by default. Keep ground calm: a flat base plus a few accents ≥ 1 px with
`kit_priority`.

### Props (free rect atlas)
```python
kit.render_props("rung_truc", [
    {"name": "tang_da", "objects": rock, "solid": [4, 10, 16, 6]},
    {"name": "den_long", "objects": lantern, "frames": [1, 3, 5, 7]},
], "client/assets/v2/props")
```
Seen by the 35° camera at `ppm=38`; each prop gets its own rect sized to fit, and its pivot
is the projected origin (put the origin at the base). `solid` is the collision rect in prop
pixels, passed through. Several frames sit side by side in the atlas.

A hard contact shadow: a flat dark disc under the prop with a material
`kit_outline=0, kit_shadow=2.0, kit_light=3.0, kit_ramp="grass"` (or the ground's ramp). It
is drawn as one flat shadow tone with no outline ring; the prop's own outline stops where it
meets the shadow. The same `kit_outline=0` works for ground decals on tiles.

Tiles and props need no armature or clips; a WORLD batch only calls `render_tiles` and
`render_props`. Objects can be given by object, collection, or name, so a .blend built
earlier works: `launcher.run_blender(script, batch, blend="art/blender/x/world.blend")` and
in the script `kit.render_tiles(..., {"grass": ["COL_grass_a", ...]}, ...)`.

### Helpers
* `kit.swap_sheet(src_json, new_id, {"earth": "ice"}, name_vi=...)`: palette-swapped copy of
  any packed sheet (monster colour variants; ramp position is kept).
* `kit.palette` (`from kit import palette`): `load()`, `swap_png(src, dst, mapping)`
  (pure Python, works in the venv).
* `kit.clear_scene()`, `kit.save_blend(rel_path)`, `kit.out_path(rel)`, `kit.log(...)`,
  `kit.TILE_M`, `kit.PPM`, `kit.DIRS`.

## 4. What the kit does to the pixels

1. Two flat EEVEE renders at 6× (1 sample, no filter, Raw colour): the base colour, and a
   data pass (material id, tone from N·L / N·H against a fixed upper-left key light, depth).
   No lamps, no randomness: the same model gives the same pixels. About 0.2 s per frame
   on an idle machine (first frame of each render call ~1 s: EEVEE compiles shaders).
2. Base colours snap to entry 1..3 of the nearest palette ramp (OKLab); shadow / light take
   the ramp neighbours, metal highlight the ramp top, glow the glow ramp.
3. 6×6 blocks are reduced to their dominant colour (weighted mode, never an average); a
   block needs ≥ 34 % cover to be drawn.
4. Speckle removed (lone pixels, one-pixel holes, colours no neighbour shares).
5. Inner lines: the farther pixel darkens where two materials of near colour meet or where
   depth jumps > 0.12 m (an arm in front of the body).
6. Glow: core / edge colours of its ramp, 1-2 px halo into empty space.
7. Outline: 1 px around the silhouette in the darkest entry of the colour it borders (ink
   next to dark colours).

## 5. Palette

`art/palette.json`: 17 solid ramps × 5 `[outline, shadow, base, light, highlight]` and 7
glow ramps × 4 `[halo far, halo near, edge, core]`, plus ink; 114 colours.

* solid: `skin hair earth wood stone steel gold jade leaf blue red purple bone` and (v1.1)
  `grass` (bright meadow green for ground, lighter and yellower than `leaf`, which is for
  trees and foliage), `pink` (peach blossom), `paper` (cream parchment, scrolls, books);
  (v1.2) `teal` (saturated blue-green: Nguyên Anh robes, pale teal beasts).
* glow: `spirit flame ice cosmic holy verdant thunder`.

Low grades should use `earth wood stone hair steel`; saturated ramps and glow are the grade
progression. Base colours snap to the nearest ramp, so a colour close to the new ramps
(cream, light pink, meadow green) may snap there on a rebuild: pin it with `kit_ramp` if you
want the old ramp. Ask the KIT owner before adding colours; never edit the PNGs by hand.
