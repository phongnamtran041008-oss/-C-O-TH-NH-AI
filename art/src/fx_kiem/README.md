# fx_kiem — kiếm khí and basic-attack FX that grow with tu vi

## Production Brief: fx_kiem (sword qi + weapon-family basic attacks)

**Type:** effects (no characters), 42 sheets. **Target:** the game (pygame, 480x270, world drawn at 2x), FX sheets of
`docs/ART_PIPELINE.md` section 4. **Style:** pixel art from 3D, xianxia manhua sword qi — a pale glint for a mortal,
then a crescent of light leaving the blade, then a roaring wave with a white-hot cutting edge, a coloured body,
torn edges, streaks, sparks and lightning, and at the top a blade of light that tears space (cracks, stars).
Skills: blender-director, vfx-fx, pixel-art-style, stylized-style, genre-action-combat, qa-review.
**Poly budget:** flat emissive meshes only, < 5k tris per scene. **Texture budget:** none (emission colours from
`art/palette.json`). **Export:** `client/assets/v2/fx/<id>.png + .json`, scenes `art/blender/fx_kiem/<id>.blend`
(git-ignored), frames `art/render/fx_kiem/` (git-ignored). **Pivot:** per family, below. **Animation:** keyframed
in Blender (location / rotation / scale / material sweep window `head`/`tail` along the swing); shapes that
flicker (lightning, flames, cracks, the flying wave) are one mesh per frame.

### Active skills
1. blender-director — this brief, pipeline order, validation before delivery.
2. vfx-fx — game path: mesh cards / ribbons + emissive materials, timing brief (start / peak / end), pivot at the spawn point.
3. pixel-art-style — texel discipline: 1 unit = 32 px, render 6x, area downscale, limited (master) palette, nearest filtering.
4. stylized-style — shape language: crescents and blades (triangles = danger), layered colour (white core / hue / deep hue), exaggeration grows with tier.
5. genre-action-combat — readable attack silhouettes: the arc reads at 1x, high tiers wild but never a blob.
6. qa-review — contact sheets + proof on the characters looked at, defects listed, fixed, re-checked; `qc.py` verdict.

### Pipeline phases
- [x] Reference & planning (aura colours, slash clip timing, weapon reference, existing slash_* / sword_trail)
- [x] Blockout & silhouette (crescent on an ellipse, pivot = sword hand)
- [x] Layers (halo / body / white-hot core / echoes / wisps / torn edge) + tier features
- [x] Render (EEVEE 6x) → pixelise → palette snap → pack
- [x] Contact sheets, proof on characters, look-fix rounds, QC, rebuild check

### Execution plan
`python art/src/fx_kiem/build.py` (venv python) → `kiem_run.py` inside headless Blender per chunk (at most 2
processes): `fx_kiem.make(id)` builds the scene with `art/src/fx/fxlib.py` (imported, never edited) →
save `.blend` → `Fx.render` → `kiem_post.pack` → contact sheets → `kiem_proof.py` (pygame).

## How to rebuild

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_kiem/build.py                 # everything (~1 min)
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_kiem/build.py --only kiem_khi_7,kiem_song_7
"/e/TU TIÊN AI/.venv/Scripts/python.exe" tools/blender/kit/qc.py client/assets/v2/fx
```

Files: `fx_kiem.py` (one builder per family, tier tables), `kiem_lib.py` (crescent, torn edge, wisps, lightning,
cracks, flame tongues, runes = abstract strokes), `kiem_post.py` (copy of fxpost's additive pass, see "palette"),
`kiem_run.py` (inside Blender), `kiem_proof.py` (proof on characters), `build.py` (driver).

## Tier → realm → ramp (the swing belongs to the character)

Colours come from each realm's aura family (`art/preview/fx_aura.png`). Ramps are `art/palette.json` glow ramps
`[halo far, halo near, glow edge, glow core]`; layers: halo = near, body = edge → deep (fading inward), core = glow core.

| Tier | Cultivation | Aura look | kiếm khí ramp | Accent | What is added at this tier |
|---|---|---|---|---|---|
| T1 | Phàm Nhân, Luyện Khí 1–3 | faint grey wisps | steel (solid, no glow) | – | a thin dull steel arc, one pale tip glint, 2 motes |
| T2 | Luyện Khí 4–6 | faint grey wisps | bone (pale white) | bone white | soft halo, crescent body fading inward, white edge, 1 speed line, 4 sparks |
| T3 | Luyện Khí 7–9 | (growing into hue) | ice | ice white | wider, 2 speed lines, inner wisps, 6 sparks |
| T4 | Trúc Cơ | blue-white ribbons | thunder | white | torn outer edge, lightning crawling on the wave, 8 sparks |
| T5 | Kết Đan | green spirals + gold core | verdant | holy gold | gold lightning, gold star motes, longer tears |
| T6 | Nguyên Anh | teal-gold flame outline | spirit | holy gold | a second outer crescent (double wave), torn inner edge |
| T7 | Hóa Thần | violet column, runes | cosmic | holy gold | rune strokes riding the body, 3 bolts, double wave |
| T8 | Luyện Hư | ring of fire, flame wings | flame | holy white | flame tongues on the outer edge (3 tones), rising embers |
| T9 | Hợp Thể | frost sphere, ice wings | ice | thunder blue | double wave, sharp frost spikes, frost shards, snow |
| T10 | Đại Thừa | galaxy + golden circle | cosmic | holy gold | void cracks splitting space along the cut, star glints, 4 bolts |

Weapon families and impacts use the tier group g (1 = T1–3, 2 = T4–5, 3 = T6–7, 4 = T8–10):
g1 ice (pale), g2 spirit (teal, between Trúc Cơ blue and Kết Đan green), g3 cosmic (violet), g4 holy gold
(+ flame fins, cosmic cracks and stars). `kiem_ngan_1/2/3` (scar): ice / holy / flame.

## Every sheet (all `blend: "add"`: draw with BLEND_ADD, black = nothing)

| id | frame | frames | fps | loop | ground | pivot | notes |
|---|---|---|---|---|---|---|---|
| kiem_khi_1..3 | 64 | 7 | 20 | no | no | (16,35) | swing arc; pivot = the sword hand |
| kiem_khi_4..7 | 96 | 7 | 20 | no | no | (22,50) | |
| kiem_khi_8..10 | 128 | 7 | 20 | no | no | (30,66) | |
| kiem_song_2,3 | 64 | 6 | 14 | yes | no | centre | qi wave flying right; front of the wave at +0.30·frame from the pivot |
| kiem_song_4..7 | 96 | 6 | 14 | yes | no | centre | |
| kiem_song_8..10 | 128 | 6 | 14 | yes | no | centre | |
| kiem_no_1,2 / 3 / 4 | 64 / 96 / 128 | 6 | 18 | no | no | centre | impact of the wave: X cut, shock ring(s), shards; 2+ lightning; 4 cracks + stars |
| kiem_ngan_1,2 / 3 | 96 / 128 | 8 | 12 | no | **yes** | centre | ground scar (35° view), glows then thins; embers; 2+ side cracks |
| thuong_dam_g | 64,64,96,128 | 6 | 20 | no | no | (0.12·w, h/2) = hand | lance of light stabbing right, pierce rings, tip flare |
| chuy_chan_g | 64,64,96,128 | 7 | 16 | no | **yes** | centre | smash: shock ring(s), radial cracks, debris |
| cung_ten_g | 64,64,96,128 | 4 | 14 | yes | no | centre | arrow of light, head at +0.30·w |
| phap_dan_g | 64,64,96,128 | 6 | 12 | yes | no | (0.62·w, h/2) = orb | spell orb + tail; g2+ orbit ring, g3+ runes + bolts, g4 stars |

## Notes for the programmer

- **Spawn and timing.** The player's `slash` is 6 frames at 14 fps with `events.slash.hit = 3` (214 ms in). Spawn
  `kiem_khi_T` ON the hit frame: its frame 0 (anticipation glint + the arc already trailing behind the blade) lines up
  with the hit pose, frame 1 (full arc) lands 50 ms later while the hit pose is still held, frames 3–6 dissipate during
  the recovery frames 4–5. The whole swing lasts 350 ms. Spawn `kiem_song_T` (T ≥ 2) from the same point on FX frame 2
  (100 ms after the hit), moving right at ~ 300–500 world px/s; at the landing point play `kiem_no_g` and, for a
  ground hit, `kiem_ngan_k` under the characters.
- **Placement.** `kiem_khi` pivot = the sword hand. In `fx_kiem_on_char.png` the hand is measured from the weapon
  layer on the hit frame (the weapon pixel nearest the chest): for the 96x96 character frames facing right it is
  (60–61, 58–59) in the character frame, i.e. character pivot + (12..13, −24..−23). Draw the FX with its pivot on that point, same 2x zoom
  as the character.
- **Facing.** Everything points right. Facing left: **mirror horizontally** around the pivot (do not rotate 180°, the
  swing would come from below). Facing up / down: rotate ±90° around the pivot (for down also mirror vertically if the
  swing should still come from the attacker's weapon side). Projectiles (`kiem_song`, `cung_ten`, `phap_dan`) rotate
  freely to their flight angle.
- **Scale.** Designed for the character's 96 px frame, both at the same world zoom: T1 reaches just past the blade tip,
  T10 is about 2.3x the character's height (≈ 240 screen px at 2x).
- **Ground sheets** (`kiem_ngan_*`, `chuy_chan_*`) are additive too: draw them before the characters.

## Palette

`kiem_post.py` is fxpost's additive pass with one change: the snap only considers the seven glow ramps plus the
`steel stone bone hair blue purple teal jade gold` solids. Snapping to the whole palette put the dim fringes on
`pink` (violet + white), `earth` / `wood` (dim gold), `leaf` / `grass` (dim green): legal colours, but mud on light.
All colours are still master-palette entries; no colour was added.

## Look-and-fix log

Round 1 (kiem_khi T1 / T5 / T10, first render):
- T10 clips the frame on every frame: the second wave sat at R + 1.25 W and the body was 25 px wide.
- Violet + white layers ADDED inside the render went over 1.0 and snapped to the `pink` skin ramp: mud.
- High tiers were a filled blob, no crescent-moon read, no clean cutting edge.
- Fix: layers alpha-blended inside the scene (z order, black world; the sheet stays additive), body = one-sided
  gradient (bright cutting edge fading inward), widths and offsets cut, pivots moved.

Round 2 (all ten kiem_khi):
- The swing read as a narrow ")" bracket, not a sweeping arc; torn edges too timid; T8–T10 looked like parallel stripes.
- T8 had no visible flames (the tongues were small and the same orange as the body edge); T10's cracks hid under the
  second wave; T7's runes were invisible at 1x.
- Fix: the swing runs on an ellipse (x 1.08, y 0.82) from +70° to −60°; streaks (wisps) peel off the inner edge and trail
  the swing; spikes 25–40 % longer; T8 drops the second wave and gets 3-tone flame tongues twice as tall; T10 drops the
  second wave for longer void cracks; rune strokes bigger.

Round 3 (all families):
- kiem_song tails were huge zigzags: the stream's wave used the integer loop index as phase and amplitude (bug); the
  wave body was a filled "D" shield.
- thuong_dam touched the right edge; its tip star sat at the far right on frame 0 while the lance was still short; the
  pierce rings floated on after the lance was gone. kiem_ngan scars too thin to read through the 35° squash.
  cung_ten halo made the arrow a capsule.
- Dim fringes still on skin / earth / wood / pink / leaf / grass ramps (measured: up to 37 % earth on chuy_chan_4).
- Fix: stream bug fixed, streams of varied length, wave body thinner with a steeper inward fade; lance 0.68 w, star rides
  the head, rings only on frames 1–3; scars 60 % wider; arrow halo slimmer; `kiem_post.py` light-ramp snap
  (after it: no pixel on those ramps).

Round 4 (proof on the characters, 3x and 1x):
- Arc lines up with the blade (T1 lies just beyond the tip of the wooden sword); progression clear at 1x.
- T1 still too bright for a mortal (white core): body now dull steel, core steel light, only the tip glint pale.
- T10 cropped by the proof cell: cell made taller.
- Song lightning branches touched the frame edge on 3 sheets: no branches on the flying wave.
