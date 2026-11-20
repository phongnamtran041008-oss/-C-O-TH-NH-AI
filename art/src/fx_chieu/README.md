# fx_chieu — FX of the chiêu thức (combat skills)

## Production Brief: fx_chieu (11 new skills, 3 hero upgrades, 6 charge-ups)

**Type:** effects (no characters), 33 sheets. **Target:** the game (pygame, 480x270, world drawn at 2x), FX sheets of
`docs/ART_PIPELINE.md` section 4. **Style:** pixel art from 3D in the xianxia manhua language — each skill one strong
silhouette that reads without its label: a flying jian with a light trail, a ring of swords in the sky and their rain,
a sword compass on the ground and a cage of swords round the body, ice spikes, chain lightning, a fire dragon, a
fissure and erupting slabs, grasping vines, a wind crescent and whirlwind, a golden bell, a healing spiral.
Skills used: blender-director, vfx-fx, pixel-art-style, stylized-style, genre-action-combat, fantasy-worlds, qa-review.
**Poly budget:** flat emissive meshes only, < 6k tris per scene. **Texture budget:** none (emission colours, all from
`art/palette.json`). **Export:** `client/assets/v2/fx/<id>.png + .json`, scenes `art/blender/fx_chieu/<id>.blend`
(git-ignored), frames `art/render/fx_chieu/` (git-ignored). **Pivot:** per sheet (table). **Animation:** keyframed
(location / rotation / scale / material opacity); shapes that deform (flames, lightning, vines, the dragon) are one
mesh per frame.

### Active skills
1. blender-director — this brief, pipeline order, validation before delivery.
2. vfx-fx — game path: mesh cards / ribbons + emissive materials; a timing brief per sheet (start / peak / tail, below);
   pivot at the logical spawn point (hand, feet, ground centre, hit point).
3. pixel-art-style — 1 unit = 32 px, render 6x, area downscale, master palette only, nearest filtering, 1 px outlines
   modelled in the scene on solid things (ice, rock, vines).
4. stylized-style — shape language: triangles for danger (spikes, swords, slabs), circles for protection and healing
   (bell, rings, spiral); white-hot core small, saturated body colour carries the element.
5. genre-action-combat — readable attack silhouettes; the target stays visible inside every area effect.
6. fantasy-worlds — xianxia material honesty: qi = light, ice and rock = solid with outlines, wood = vines and leaves,
   runes are abstract strokes (never glyphs).
7. qa-review — contact sheets and proofs looked at (log below), `qc.py` verdict, clean-rebuild check.

### Pipeline phases
- [x] Reference & planning (fx_kiem quality bar, phap_tran / cong_phap / vu_khi references, ELEM colours, cast clip)
- [x] Blockout & silhouette (one builder per sheet, numbers only)
- [x] Layers (halo / body / lit facet or core / accents) + motion (anticipation, peak, tail)
- [x] Render (EEVEE 6x) -> pixelise -> palette snap -> pack (`chieu_post.py`)
- [x] Contact sheets, proof in context on grass (4x and 1x), look-fix rounds, QC, rebuild check

### Execution plan
`python art/src/fx_chieu/build.py` (venv python) -> `chieu_run.py` inside headless Blender (2 processes) per chunk:
`fx_chieu.make(id)` builds the scene with `chieu_lib.py` (which imports `art/src/fx/fxlib.py` and
`art/src/fx_kiem/kiem_lib.py`, both read only) -> save `.blend` -> `Fx.render` -> `chieu_post.pack` -> then
`chieu_proof.py` (pygame) writes the contact sheets and the proofs.

## How to rebuild

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_chieu/build.py                     # all 33 (~1.5 min)
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_chieu/build.py --only hoa_long,loi_xich
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_chieu/chieu_proof.py                # previews only
"/e/TU TIÊN AI/.venv/Scripts/python.exe" tools/blender/kit/qc.py client/assets/v2/fx
```

Files: `ids.py` (the 33 ids and the contact-sheet groups), `chieu_lib.py` (CFx: px-space scene builder, explicit z
order, per-object depth, non-square frames; shapes: sword, spikes, leaves, bell, bolts), `fx_chieu.py` (one builder per
sheet), `chieu_post.py` (pixel pass), `chieu_run.py` (inside Blender), `chieu_proof.py` (contact sheets + proofs; also
`--look id,id out.png` for review crops), `build.py` (driver).

Previews: `art/preview/fx_chieu_kiem.png`, `fx_chieu_nguyen_to.png`, `fx_chieu_dat_moc_phong.png`, `fx_chieu_tu_khi.png`
(one row per sheet, 3x; left half on dark, right half on grass), `fx_chieu_proof.png` (14 skill scenes on grass at the
2x world zoom, then 2x again), `fx_chieu_proof_1x.png` (the same at 1x).

## Blend: every sheet is `alpha`

First render (all additive, like the older FX): on grass every colour washed out — gold became yellow-green, violet and
blue became white, so Kim, Lôi and Thủy could not be told apart. All sheets are therefore `blend: "alpha"` (ordinary
straight-alpha blit, like the realm auras): palette colours with soft alpha steps (0, 25, 50, 75, 100 %), halos are soft
low-opacity layers in the scene. The element hue survives on any ground; white-hot cores are kept small. Inside a
scene the layers are alpha-stacked in a fixed z order (halo < body < lit facet / core < sparks).

`chieu_post.py` snaps every pixel to the master palette in OKLab but only to the ramps the sheet names: light ramps by
default (glow ramps + cool/neutral solids, like fx_kiem), plus `earth wood` for Thổ, `leaf jade earth` for Mộc, `teal
bone` for wind, `ice blue steel` for ice. No colour was added to the palette.

## Every sheet

| id | frame | frames | fps | loop | blend | ground | pivot | what the pivot is |
|---|---|---|---|---|---|---|---|---|
| ngu_kiem | 96x96 | 4 | 14 | yes | alpha | no | (48,48) | the flying sword (guard at -4 px); tip at +26, trail to -44 |
| ngu_kiem_xuyen | 64x64 | 6 | 18 | no | alpha | no | (32,32) | the hit point on a pierced target |
| van_kiem_troi | 128x128 | 8 | 14 | no | alpha | no | (64,120) | the area centre ON THE GROUND (sword ring 78 px above it) |
| van_kiem_roi | 128x128 | 10 | 16 | no | alpha | no | (64,104) | the area centre on the ground (impacts on an ellipse 44x12) |
| van_kiem_vong | 128x128 | 8 | 8 | yes | alpha | yes | (64,64) | the area centre (sigil radius 58 px, 35° ellipse) |
| kiem_vuc | 128x128 | 8 | 8 | yes | alpha | yes | (64,64) | the caster's feet (domain radius 60 px) |
| kiem_vuc_xoay | 128x128 | 8 | 12 | yes | alpha | no | (64,104) | the caster's feet (orbit 44x12 px at 22 px height) |
| pha_me_kiem | 128x128 | 7 | 20 | no | alpha | no | (10,64) | the sword hand; the cut reaches +112 px |
| bang_phong | 96x96 | 8 | 14 | no | alpha | no | (48,76) | the patch centre on the ground |
| bang_ket | 64x64 | 4 | 6 | yes | alpha | no | (32,56) | the monster's feet (48 px monster) |
| loi_xich | 96x32 | 4 | 16 | yes | alpha | no | (3,16) | left end of the segment; the right end is (92,16) |
| loi_cham | 64x64 | 6 | 18 | no | alpha | no | (32,32) | the hit point |
| thien_loi_giang | 128x128 | 8 | 16 | no | alpha | no | (64,108) | the strike point on the ground; the bolt starts at the frame top |
| hoa_long | 128x128 | 6 | 12 | yes | alpha | no | (64,64) | the dragon's chest; head front at +52, tail at -60 |
| hoa_long_vet | 96x96 | 6 | 10 | yes | alpha | yes | (48,60) | the centre of a 80 px burning streak, long axis horizontal |
| hoa_cau_lon | 96x96 | 4 | 14 | yes | alpha | no | (48,48) | ball centre at +16 px; tail to -42 |
| hoa_cau_no | 128x128 | 8 | 16 | no | alpha | no | (64,64) | the impact point (fireball r 32, ring r 48) |
| dia_liet | 128x128 | 8 | 16 | no | alpha | yes | (8,64) | where the fissure starts; it reaches +112 px right |
| dia_liet_no | 96x96 | 8 | 14 | no | alpha | no | (48,80) | the eruption point on the ground |
| thanh_dang | 96x96 | 8 | 12 | no | alpha | no | (48,78) | the patch centre on the ground |
| thanh_dang_troi | 64x64 | 4 | 8 | yes | alpha | no | (32,56) | the monster's feet (48 px monster) |
| hoi_xuan | 96x96 | 10 | 12 | no | alpha | no | (48,84) | the healed one's feet |
| phong_nhan | 64x64 | 4 | 16 | yes | alpha | no | (32,32) | blade centre (crescent front at +10) |
| phong_xoay | 64x64 | 7 | 16 | no | alpha | no | (32,58) | the ground point where the blade lands |
| kim_chung | 96x96 | 8 | 14 | no | alpha | no | (48,86) | the caster's feet (bell lip) |
| kim_chung_tru | 96x96 | 6 | 8 | yes | alpha | no | (48,86) | the caster's feet |
| kim_chung_vang | 96x96 | 6 | 18 | no | alpha | no | (48,86) | the caster's feet |
| tu_khi_kim/moc/thuy/hoa/tho/loi | 96x96 | 6 | 12 | yes | alpha | no | (48,48) | the point qi gathers to (the cast hand / chest) |

The brief says 34 sheets; its own list adds up to 33 (23 new + 4 hero + 6 tu_khi), which is what is delivered.

## Notes for the programmer (sequencing, draw order, scale, rotation)

General: all sheets are drawn with an ordinary alpha blit (not additive). `ground: true` sheets are drawn before the
characters; the others after the characters unless noted. All sizes are world px at the same zoom as the 96 px
character frames (do not scale up); "mirror" = flip horizontally about the pivot.

- **Charge-up** `tu_khi_<el>`: loop while the skill is channelled, pivot on the cast hand / chest (character pivot
  + (6, -28) facing right); draw at 0.75 scale for a short cast, 1.0 for a tuyệt kỹ. Stop it on the cast `hit` event.
  Wind (Phong Nhận) uses `tu_khi_moc`.
- **Ngự Kiếm Thuật**: on cast hit spawn `ngu_kiem` at the hand, rotate to the flight angle (it points right), move at
  ~250-350 world px/s through the line; on every enemy it passes play `ngu_kiem_xuyen` at the enemy centre (rotated to
  the flight angle, it is directional: rings stand across the line). On the return trip rotate by 180°.
- **Vạn Kiếm Quy Tông**: `van_kiem_vong` (ground, loop) appears on the area as the telegraph; at the same time
  `van_kiem_troi` (8 fr, 0.57 s) plays with its pivot on the area centre; then `van_kiem_roi` (10 fr, 0.63 s) on the
  same point — damage on its frames 2-6 (swords land on frames 1-6). Keep the vong until roi ends. Never rotate; mirror
  is not needed (symmetric). Sized for an area of ~90x25 world px on screen; scale uniformly for bigger areas.
- **Băng Phong Thuật**: `bang_phong` at the target's feet (frames 0-2 burst, 3-5 hold = damage + freeze, 6-7 shatter);
  from frame 5 loop `bang_ket` on each frozen monster for the freeze duration (scale = monster frame / 48).
  The ring of spikes leaves the middle clear: the monster stays visible.
- **Chưởng Tâm Lôi**: for each link A->B draw `loi_xich` with its pivot at A, rotated to the angle of B-A, scaled in x
  by |B-A| / 89 (y scale 1, or up to 1.3 for a fat chain); cycle its 4 frames at 16 fps; hops can appear one after
  another every ~60 ms. At each B play `loi_cham` once.
- **Hỏa Long Thuật**: `hoa_long` flies from the caster (rotate to the flight angle; for leftward flight mirror instead of
  rotating 180° so the dragon is not upside down); drop a `hoa_long_vet` under its path every ~70 px (rotate each to
  the path angle; ground layer) and let them burn 1.5-2 s, then remove (or fade alpha).
- **Địa Liệt Trảm**: `dia_liet` (ground) with its pivot at the caster's front foot, rotated to the aim angle (mirror
  for left); the crack reaches its end on frame 4 (0.25 s); play `dia_liet_no` at each target the crack passes, timed
  when the head passes it (frame ≈ 4 × distance / 112).
- **Thanh Đằng Triền**: `thanh_dang` at the target's feet (grows on frames 0-4); from frame 5 loop
  `thanh_dang_troi` on the held monster (scale = monster frame / 48) for the root duration.
- **Phong Nhận Thuật**: 3-5 `phong_nhan` in a fan (±10-15° apart), rotated to their flight angle; at the landing point
  `phong_xoay` once.
- **Kim Chung Tráo**: `kim_chung` once at the caster's feet, then loop `kim_chung_tru` (draw after the character; it is
  translucent) for the shield duration, follow the caster. On each blocked hit play `kim_chung_vang` over it.
- **Kiếm Vực**: `kiem_vuc` (ground, loop) under the caster, `kiem_vuc_xoay` (loop) over the caster; both follow the
  caster. The ground circle is 120 px wide: it marks the domain's reach.
- **Hồi Xuân Thuật**: `hoi_xuan` once at the healed one's feet; the HP number on frame 4 (the bloom).
- **Hero upgrades**: `hoa_cau_lon` replaces the fireball projectile (rotate to flight angle; mirror for left), then
  `hoa_cau_no` at the impact (damage on frame 1-2). `thien_loi_giang` at the struck ground point (damage on frame 1,
  the main bolt). `pha_me_kiem` at the sword hand on the slash/cast hit frame (mirror for left, rotate ±90° for up/down
  as fx_kiem's `kiem_khi`), damage on frame 1 (the cross glint flashes at +74 px).

## Look-and-fix log

Round 0 (first 7 sheets, additive):
- Additive light on grass: gold -> yellow-green, violet -> white; Kim / Lôi / Thủy indistinguishable. -> every sheet
  re-rendered as `alpha` with soft halo layers.
- Edge clipping: ngu_kiem trail (-54 px), ngu_kiem_xuyen line, thien_loi_giang ground ring and sparks below the frame.
  -> trail 32 px, line 46 px, pivot raised to y 108, ring 46 px, sparks fall less. Empty last frames (loi_cham,
  thien_loi_giang) -> a faint ember / scorch kept.

Round 1 (contact sheets of every family, dark + grass):
- van_kiem_troi frame 0 nearly empty -> the ring starts drawn, first glints on frame 0.
- van_kiem_roi touched the bottom edge and looked sparse -> pivot 104, ellipse 44x12, 14 thin background swords of light
  per frame (the rain itself).
- kiem_vuc: the inner gradient fill snapped to a stepped teal plate on grass -> a narrow soft band only; swords 21x5.
- kiem_vuc_xoay read as a polygon of sticks -> upright swords tip up, leaning into the motion (a sword cage).
- hoa_long: a dark brown disc (halo blob) behind the head, tail clipped -> halo removed (body halo only, 50 %), body
  56 px. hoa_cau_lon / hoa_cau_no: FLAME[0] halos snapped to brown plates (mud), smoke = hard grey rocks -> halos in the
  orange at 50 % with soft edges, dark layer removed, smoke soft.
- Spike outlines missing: `offset_poly` shrank instead of grew (orientation test inverted) -> fixed; ice, rock and the
  dragon head now have their 1 px dark outline.
- bang_ket shell read mint-green on grass -> bluer (ice body) at 30 %; side crystals moved in from the frame edge.
- dia_liet a hairline at 1x -> 1.6x wider, more jagged; tu_khi streams too heavy (pinwheel) -> thinner, shorter.
- pha_me_kiem: a flat yellow disc behind the cross glint -> smaller, soft.

Round 2 (proof in context, 4x and 1x on grass):
- bang_phong, thanh_dang and dia_liet_no hid the monster completely -> rings of spikes / vines / slabs around the target,
  the middle clear, front ones short.
- hoa_cau_no dwarfed the monster (120 px blast for a 30 px monster) -> fireball r 32, ring r 48.
- The dragon head read as a box -> domed brow, tapering snout with a raised nose, shaded jaw, eye socket, nostril, the
  head's back rounded into the neck, mane drawn over the back of the head.
- tu_khi_tho and tu_khi_hoa were the same orange -> hỏa red-orange (flame ramp low end), thổ sandy ochre (wood ramp)
  with rock-chip motes; kim stays pale gold-white with star motes.
- kiem_vuc_xoay merged with the ice-blue domain -> orbiting swords in gold-white over the ice circle.
- Proof: kiem_vuc cell shifted so the whole domain shows; Phong Nhận uses tu_khi_moc.

Round 3 (final contact sheets):
- hoa_cau_no tail: smoke was a ring of grey dots with dark rims; the last fire frame had a dark hole -> one soft cloud
  of light-grey puffs rising, a small hot core kept on frame 5.
- `qc.py client/assets/v2/fx`: OK (181 files = 148 before + 33, 0 problems). Clean rebuild (art/blender/fx_chieu and
  art/render/fx_chieu deleted, full build, 1 min 17 s): every sheet and preview byte-identical to the previous build.

## Still weak (honest)
- hoa_long: reads as a fire dragon (horns, whiskers, teeth, fins, scales) but the head is still a little heavy and
  eel-like at 1x; a more sculpted head (separate brow ridge, open upper lip curl) would help.
- The sword sheets (van_kiem, kiem_vuc_xoay) use small swords (12-22 px); at 1x they read as golden "+" marks rather
  than jian; the ring / rain reads, the individual sword barely.
- hoi_xuan's ground disc and ribbons are thin at 1x; the bloom carries it.
- dia_liet_no and thanh_dang dust / dirt specks are small and a little noisy.
- tu_khi_tho on bright grass is the weakest of the six (sandy ochre on green has little contrast).
