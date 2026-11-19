# ART PIPELINE v2 — every picture in the game comes out of Blender

This is the contract between the people (and agents) who build art and the game that reads it.
It replaces the M8 look (32 px flat boxes, `client/assets/chars/`), which stays in place only
until the game is switched over to `client/assets/v2/`.

The target look is the author's own reference sheets in `art/reference/` — open them before
building anything:

| File | What it shows |
|---|---|
| `art/reference/nhan_vat/nhan_vat_8_canh_gioi.webp` | the player at the 8 realms (one row each), 8 poses per row |
| `art/reference/vu_khi/vu_khi_8_loai_10_bac.webp` | 8 weapon types (columns) × 10 grades (rows) |
| `art/reference/cong_phap/cong_phap.webp` | manuals, scrolls, bamboo slips |
| `art/reference/phap_tran/phap_tran.webp` | formation circles, from plain to cosmic |
| `art/reference/trang_bi/trang_bi.webp`, `dan_duoc/*.webp` | gear, pills, herbs |
| `art/reference/luu_y.txt`, `nhan_vat/luu_y.txt` | the author's notes: 8 realms; fine clothes are crafted gear, not a realm reward |

Author's standing rules for art: **built properly in Blender, with the Blender skills, never
drawn by hand in code, never sloppy**; no Chinese characters anywhere (runes on books and
circles are abstract strokes); xianxia naming in Vietnamese.

## 1. The look (what "pixel art from 3D" means here)

1. **Read the silhouette first.** Chibi proportions (head ≈ 1/2.6 of the height), big clear
   shapes, exaggerated weapons. If a sprite does not read as a black silhouette, no shading
   will save it.
2. **Three-tone cel shading.** Shadow / base / light per material, hard steps, key light from
   the upper left (as in the reference). Metals get one small hard highlight. No gradients.
3. **Selective dark outline, 1 px, added after scaling down** — a darker shade of the colour
   it borders, not flat black. Inner lines only where two parts would merge.
4. **One master palette** (`art/palette.json`), every sprite quantised to it. Low grades are
   earthy and dull; high grades add saturated accents and glow. That contrast *is* the
   progression, so do not make grade 1 shiny.
5. **Hard pixels.** No anti-aliasing, alpha is 0 or 255 on solid art. Only FX may carry soft
   alpha, and they are drawn additively.
6. **Glow is a separate thing.** Emissive parts (blade runes, halos, wings, auras) are marked
   in the model with emission; the kit renders them into the sprite as bright palette colours
   plus a 1–2 px halo, the way the reference does it.
7. **Animation has anticipation and follow-through.** A slash is wind-up → strike → recovery,
   not a linear swing; idle breathes; cloth, hair, ribbons lag behind. Feet never slide: the
   pivot is the projected ground point, fixed for every frame.

## 2. Sizes (game is 480×270, tiles are 16×16)

| Kind | Frame | Drawn size | Directions |
|---|---|---|---|
| Player character (v2, after the author rejected the 36 px chibi) | 96×96 | body ≈ 48 px tall, **about 3.4 heads** — a slender young cultivator like the reference, not a chibi; wings/halo may fill the frame | down, left, up, right |
| Monster — normal / elite / boss | 48×48 / 64×64 / 96×96 | fills ~70 % | 4 |
| Spirit beast (linh thú) | 48×48 | | 4 |
| Weapon in hand (layer over the character) | 64×64, same grid as the character sheet | | 4 |
| Weapon / item / manual icon | 32×32 | ≈ 26 px, drawn diagonally like the reference | – |
| Ground pickup (weapon lying in the world) | 32×32, 4-frame bob + glint | | – |
| FX (slash arc, hit, projectile) | 64×64 | | per FX |
| FX big (formation circle, tribulation, aura) | 96×96 | ground circles are ellipses seen from 35° | – |
| Tile | 16×16 | | – |
| Prop (tree, rock, building, altar) | free rect in an atlas, pivot at the base | | – |

**Characters are seen almost side-on (camera 15° above the horizon), the world from 35°.**
The reference figures are drawn frontally, like every 2D RPG hero: a 35° camera squashes the
body and shows the top of the head, which is what made the first characters look like dolls.
Tiles and props keep 35°.

Camera for everything that stands on the ground: orthographic, 35° above the horizon (15° for
the player), never moved; the *model* is turned for the four directions so the light stays upper-left.
Render at 6× the target size, then scale down (the kit does this).

## 3. Clips

Player (all 8 realm looks share one rig, so all clips exist for all looks):

| Clip | Frames | fps | Loop | Notes |
|---|---|---|---|---|
| `idle` | 4 | 6 | yes | breathing, robe sways |
| `walk` | 8 | 10 | yes | |
| `slash` | 6 | 14 | no | melee; `events.hit` = the strike frame |
| `cast` | 6 | 12 | no | niệm chú: hand seal, release on `events.hit` |
| `shoot` | 6 | 12 | no | bow / thrown gourd |
| `hit` | 3 | 12 | no | flinch |
| `die` | 6 | 10 | no | ends lying down |
| `meditate` | 4 | 5 | yes | lotus seat |
| `fly` | 4 | 8 | yes | standing on a flying sword (ngự kiếm), robe streaming |
| `dodge` | 4 | 14 | no | short dash |

Monster / beast: `idle` 4, `walk` 6, `windup` 4 (the telegraph pose, held while the hit zone
fills), `attack` 4 (`events.hit`), `hit` 2, `die` 6. Bosses add `special` 8.

## 4. What the game reads (`client/assets/v2/`)

Nothing here is edited by hand; everything is written by the kit's packer.

**Animated sheet** — `v2/chars/<id>`, `v2/monsters/<id>`, `v2/beasts/<id>`, and the weapon
layers `v2/weapons/<weapon_id>` (`.png` + `.json`). Same format `client/engine/charsheet.py`
already loads, plus `events`:

```json
{"id": "dao_si_luyen_khi", "name_vi": "Đạo Sĩ Luyện Khí",
 "frame": {"w": 64, "h": 64}, "pivot": {"x": 32, "y": 54},
 "sheet": "dao_si_luyen_khi.png", "cols": 16, "frames": 204,
 "clips": {"idle": {"fps": 6, "loop": true,
                    "frames": {"down": [0,1,2,3], "left": [...], "up": [...], "right": [...]}}},
 "events": {"slash": {"hit": 3}}}
```

A weapon layer has exactly the clips, frame order and pivot of the character sheets, and is
drawn over the character; where the body hides the weapon the layer is transparent (the kit
renders the body as a holdout), so the game never has to sort them.

**FX sheet** — `v2/fx/<id>.png` + `.json`:
`{"id", "frame": {"w","h"}, "pivot": {"x","y"}, "cols", "frames", "fps", "loop", "blend": "add"|"alpha", "ground": true|false}`.
`ground: true` means it is drawn under the characters (circles, cracks, telegraph marks).

**Icon atlas** — `v2/icons/<set>.png` + `.json`:
`{"sheet", "cell": 32, "cols", "icons": {"<id>": {"index": n, "name_vi": "...", "grade": 1..8}}}`.

**Tileset** — `v2/tiles/<region>.png` (16-px grid) + `.json` `{"tiles": {"<name>": [indices…]}}`
with at least: ground ×4 variants, path ×4, water (4-frame), cliff edges (N,S,E,W + 4 corners),
transition tiles between ground and path.
**Props** — `v2/props/<region>.png` + `.json`
`{"props": {"<name>": {"rect": [x,y,w,h], "pivot": [px,py], "frames": 1, "solid": [x,y,w,h]|null}}}`.

**Preview** — every batch also writes a contact sheet `art/preview/<batch>.png` (frames laid
out, 3× nearest-neighbour, dark background like the reference) — that is what gets reviewed.

## 5. Where things live

| Path | What | Owner |
|---|---|---|
| `tools/blender/kit/` | the shared library: scene/camera/light setup, toon conversion, render, pixelise, outline, palette, pack, QC, contact sheets | KIT |
| `art/palette.json` | master palette | KIT |
| `art/src/<batch>/…py` | build scripts: one function per asset, **numbers and code, no hand-saved state** | the batch |
| `art/blender/<batch>/*.blend` | built scenes (git-ignored: rebuilt by the batch's `build.py`) | the batch |
| `art/render/…` | intermediate frames (git-ignored) | – |
| `client/assets/v2/<kind>/` | packed output | the batch |
| `art/preview/` | contact sheets | the batch |

Models use ordinary Principled materials (base colour, emission colour + strength, alpha).
The kit turns them into toon shading at render time, so a model never depends on the kit's
internals. Names: collections `COL_`, meshes `SM_`, materials `MAT_`, armatures `ARM_`,
actions = the clip name. 1 unit = 1 m; the player is ≈ 1.0 m tall; characters face −Y;
origin on the ground between the feet.

Blender is run headless, so several batches can render at once:
`"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b --factory-startup --python <script> -- <args>`
(Blender 5.3; its Python has numpy. The game's venv has pygame but **no Pillow and no numpy**.)

## 6. Quality gate (a batch is not done until all of these hold)

- `python tools/blender/kit/qc.py <output folder>` passes: pivot steady, nothing cut at the
  frame edge, real transparency, JSON and sheet agree, required clips present, every colour in
  the palette.
- The contact sheet has been **looked at** next to the reference and the gaps fixed (at least
  two look-fix rounds): silhouette, readable face/eyes, weapon reads at a glance, grade
  progression visible, no mud, no stray pixels, no jitter between frames.
- Rebuilding from scratch (`art/src/...` → `.blend` → render → pack) gives the same files.

## 7. How a batch works (read this if you were handed one)

1. **Skills first.** Before any Blender work, load the skills named in your brief with the
   Skill tool and follow them (they were given by the author for exactly this). Write the short
   production brief the `blender-director` skill asks for at the top of your batch's
   `art/src/<batch>/README.md`.
2. **Stay in your folders.** You own `art/src/<batch>/`, `art/blender/<batch>/`,
   `art/preview/<batch>*`, and the output folder(s) your brief names under
   `client/assets/v2/`. Do not edit anything else (other agents are working in this checkout
   at the same time), do not commit, do not run the game's test suites.
3. **Headless and reproducible.** Everything is built by scripts:
   `python art/src/<batch>/build.py [--only <id>]` (run with the venv python
   `"/e/TU TIÊN AI/.venv/Scripts/python.exe"`) rebuilds the .blend files, renders, packs and
   writes the contact sheets. Do not use the live Blender MCP tools (one shared window; other
   agents would collide) — look at your own renders with the Read tool instead.
4. **Model first, then the final look.** The kit (`tools/blender/kit/`) is being written at
   the same time as your batch. Start modelling and animating right away and preview with a
   quick Workbench render. The kit is ready when `tools/blender/kit/READY` exists (its
   `README.md` documents the API); from then on render and pack **only** through the kit, so
   every batch has the same look. If the kit is not ready when your models are, wait for it
   (`until [ -f tools/blender/kit/READY ]; do sleep 20; done` in a background shell), do not
   write a second renderer.
5. **Look, then fix, at least twice.** After each render, open the contact sheet next to the
   reference sheet and write down what is wrong before changing anything. Stop when section 6
   holds, not when the script first runs.
6. **Report** (your final message): what you built (ids, counts), the files, the commands you
   ran and their results, what you looked at and fixed, what is still weak, and anything you
   needed from the kit that it does not do.
