# FX batch - production brief

**Type:** effects (no characters). **Target:** game, 480x270 pygame, FX sheets of `docs/ART_PIPELINE.md` section 4.
**Style:** pixel art from 3D, glowing xianxia magic in the look of `art/reference/phap_tran/phap_tran.webp`
(saturated crisp shapes, 1-2 px halo, posterised glow ramps), stylized + pixel-art skills.
**Budgets:** combat FX 64x64, ground / realm FX 96x96, 4-10 frames; 1 Blender unit = 32 sprite px; every scene is
a handful of flat emissive meshes (< 3k tris).
**Export:** `client/assets/v2/fx/<id>.png + .json`, scenes `art/blender/fx/<id>.blend`, contact sheets
`art/preview/fx_combat.png`, `fx_ground.png`, `fx_realm.png`. **Pivot:** centre, except where the table says otherwise.
**Animation:** keyframed in Blender (location, rotation, scale, material value nodes); shapes that deform
(flames, lightning, helices) are one mesh per frame shown only on its own frame.

## How it is made

`python art/src/fx/build.py [--only id,id]` (venv python) starts Blender headless (`fx_run.py`) which, per FX:

1. `fxlib.py` builds the scene: ortho camera, emissive materials (Emission through an Add shader for `add`,
   Emission over Transparent for `alpha`), 2D shapes made from numbers (ribbons, fans, flames, runes = random
   abstract strokes, never glyphs), animation keys. Views: `front` (combat, auras), `ground` (35 deg above
   the horizon: circles become ellipses), `top` (hit-zone warnings).
2. Saves `art/blender/fx/<id>.blend`, renders every frame with EEVEE at 6x the target size.
3. `fxpost.py` scales down (area average), spills a 1-2 px halo outwards, and **snaps every colour to
   `art/palette.json`** (OKLab nearest; the glow ramps are the four intensity steps), black becomes alpha 0
   on additive sheets; alpha sheets quantise alpha to a few steps. Writes sheet + JSON, then the contact sheets.

Blend semantics: `blend: "add"` sheets store the light the effect ADDS (palette colour, alpha 255 where lit, 0 elsewhere):
draw them with `BLEND_ADD` (alpha ignored). `blend: "alpha"` sheets are ordinary straight-alpha sprites.
Warn sheets are full-bleed on purpose: the artwork is stretched by the game (fan bounding box = R x 1.41 R,
apex at the pivot on the left edge).

**Status of the render path:** the kit (`tools/blender/kit/READY`) did not exist when this batch was
finished, so the renderer/packer here is this batch's own provisional one (`fxlib.py`, `fxpost.py`); colours already
come from the master palette and `python tools/blender/kit/qc.py client/assets/v2/fx` passes (56 files, 0 problems).
When the kit is READY, replace `Fx.render` + `fxpost.pack` with the kit's FX packer; the scene builders do not change.

## Every FX

| id | frames | fps | loop | blend | ground | where it is used |
|---|---|---|---|---|---|---|
| bolt_hoa | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| bolt_kim | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| bolt_loi | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| bolt_moc | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| bolt_tho | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| bolt_thuy | 4 | 14 | yes | add | no | projectile of that element (points right, game rotates it) |
| burst_hoa | 6 | 16 | no | add | no | impact burst of that element |
| burst_kim | 6 | 16 | no | add | no | impact burst of that element |
| burst_loi | 6 | 16 | no | add | no | impact burst of that element |
| burst_moc | 6 | 16 | no | add | no | impact burst of that element |
| burst_tho | 6 | 16 | no | add | no | impact burst of that element |
| burst_thuy | 6 | 16 | no | add | no | impact burst of that element |
| capture_seal | 8 | 12 | no | add | no | talisman ring closes around a spirit beast, then flashes |
| chest_open | 6 | 10 | no | add | no | treasure chest opens: a fan of golden light |
| crack_ground | 5 | 12 | no | alpha | yes |mark left by a heavy slam (alpha, under characters) |
| dash_trail | 4 | 16 | no | add | no | behind a dodging / dashing player (streaks point left) |
| dot_pha | 10 | 10 | no | add | no |realm breakthrough cut-scene |
| dust_step | 4 | 10 | no | alpha | no | footstep puff under the feet |
| guard_break | 5 | 14 | no | add | no | wrong answer: the guard shatters |
| heal | 6 | 10 | yes | add | no | HP restored: rising green-gold motes |
| hit_crit | 5 | 16 | no | add | no | critical hit (bigger, star-shaped) |
| hit_spark | 4 | 18 | no | add | no | any normal hit on a target |
| linh_thuan | 6 | 8 | yes | add | no | spirit shield bubble around the player (correct streak) |
| loi_kiep | 8 | 12 | no | add | no |tribulation lightning strike on the cultivator |
| parry | 5 | 16 | no | add | no | player answered right: the blow is deflected |
| pickup_glow | 6 | 8 | yes | add | no | soft light pillar over a weapon lying on the ground |
| slash_hoa | 5 | 18 | no | add | no | melee sword-light arc of that element |
| slash_kim | 5 | 18 | no | add | no | melee sword-light arc of that element |
| slash_loi | 5 | 18 | no | add | no | melee sword-light arc of that element |
| slash_moc | 5 | 18 | no | add | no | melee sword-light arc of that element |
| slash_tho | 5 | 18 | no | add | no | melee sword-light arc of that element |
| slash_thuy | 5 | 18 | no | add | no | melee sword-light arc of that element |
| sword_trail | 4 | 14 | yes | add | no | light streak behind a flying sword (streak trails to the left) |
| thang_cap | 6 | 10 | no | add | no |level-up sparkle ring |
| tran_1 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_2 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_3 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_4 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_5 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_6 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_7 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| tran_8 | 8 | 6 | yes | add | yes |ground formation circle, one per realm grade 1-8 (drawn under characters) |
| warn_circle_charge | 4 | 8 | yes | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| warn_circle_release | 3 | 14 | no | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| warn_cone_charge | 4 | 8 | yes | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| warn_cone_release | 3 | 14 | no | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| warn_line_charge | 4 | 8 | yes | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| warn_line_release | 3 | 14 | no | alpha | yes |hit-zone telegraph, stretched by the game to the zone (charge loops while the monster winds up, release flashes on the hit) |
| aura_luyen_khi_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: a few faint breath wisps |
| aura_luyen_khi_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: a few faint breath wisps |
| aura_truc_co_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: two thin blue-white qi ribbons + mist ring at the feet |
| aura_truc_co_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: two thin blue-white qi ribbons + mist ring at the feet |
| aura_ket_dan_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: green spiral ribbons, golden motes, golden core glow at the belly |
| aura_ket_dan_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: green spiral ribbons, golden motes, golden core glow at the belly |
| aura_nguyen_anh_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: teal-gold flame outline, gold sparks |
| aura_nguyen_anh_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: teal-gold flame outline, gold sparks |
| aura_hoa_than_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: violet light column, drifting runes, faint large halo |
| aura_hoa_than_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: violet light column, drifting runes, faint large halo |
| aura_luyen_hu_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: ring of fire on the ground, shoulder flames, warm glow behind the wings, embers |
| aura_luyen_hu_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: ring of fire on the ground, shoulder flames, warm glow behind the wings, embers |
| aura_hop_the_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: frost sphere (rim), orbiting ice shards, snow, cold glow behind the wings |
| aura_hop_the_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: frost sphere (rim), orbiting ice shards, snow, cold glow behind the wings |
| aura_dai_thua_back | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn behind the character: galaxy swirl, golden magic circle, star motes, gold-violet glow behind the wings |
| aura_dai_thua_front | 8 | 10 | yes | alpha | no | 128x128, pivot (64,104)=feet of the v2 character, drawn in front of the character: galaxy swirl, golden magic circle, star motes, gold-violet glow behind the wings |
| glow_luyen_hu | 204 | 10 | no | alpha | no | per-frame silhouette glow cut from dao_si_luyen_hu.png, same grid / index / pivot, drawn directly behind the character (layer back) |
| glow_hop_the | 204 | 10 | no | alpha | no | per-frame silhouette glow cut from dao_si_hop_the.png, same grid / index / pivot, drawn directly behind the character (layer back) |
| glow_dai_thua | 204 | 10 | no | alpha | no | per-frame silhouette glow cut from dao_si_dai_thua.png, same grid / index / pivot, drawn directly behind the character (layer back) |
| glow_hoa_than | 204 | 10 | no | alpha | no | per-frame silhouette glow cut from dao_si_hoa_than.png, same grid / index / pivot, drawn directly behind the character (layer back) |

## Notes added after review

- Renderer decision: FX keep this batch's own render + pack step (`fxlib.py` / `fxpost.py`); colours are snapped to `art/palette.json` and `qc.py` passes. The kit is not waited for.
- `warn_*` sheets are `blend: "alpha"` (normal alpha, NOT additive) so they stay readable on bright grass. Every edge has a dark red outline under an orange-red stroke, the fill is 50 % alpha so the ground shows through. `art/preview/fx_warn_on_ground.png` draws charge and release frames at 1x/2x/3x stretch over the grass, path, stone and water tiles of `client/assets/v2/tiles/base.png`.
- `blend: "add"` sheets must be drawn with BLEND_ADD (alpha ignored); their colours are the light added to the screen.
- Pillars, beams and fades never fade by dimming (dim gold/violet snaps to brown palette steps): they get thinner or sparser and end in sparks (`dot_pha`, `thang_cap` last frames).


## Realm auras for the v2 characters (`fx_aura.py`, `glow_sheets.py`)

Replaces the old 96x96 `aura_<realm>` sheets. Two sheets per realm, `_back` and `_front`, 128x128, pivot (64,104) = the
character's feet (character frame 96x96 pivot (48,82): draw it at aura - (16,22)), 8 frames, 10 fps, loop.

**DRAW RULE (also in every JSON as `blend`, `layer`, `draw`):** the auras are `blend: "alpha"` sheets - palette colours
with soft alpha, drawn with an ordinary alpha blit, NEVER additive - so they keep their hue on bright ground (blue stays
blue, violet violet, fire orange on grass). Order per frame: `aura_<realm>_back`, then `glow_<realm>` (winged realms and
Hoa Than) with the character's own frame index, then the character, then `aura_<realm>_front`.

`glow_<realm>.png/.json` (luyen_hu, hop_the, dai_thua, hoa_than) are made by `glow_sheets.py` from the packed character
sheets: per frame the opaque silhouette is cut to the wings (upper body outside the torso column, behind the body when seen
from the side; for hoa_than the head / halo / hair), blurred, and tinted with the realm's palette glow colours
(flame / ice / cosmic / purple+holy). Same grid, cols, frames and pivot as `dao_si_<realm>`, `layer: "back"`: frame i
is drawn directly behind frame i of the character, so the glow follows the flap, the slash spread and the fly sweep.

Orbiting parts (ribbons, shards, ground flames) are split by depth so they wrap the body; front ribbons fade out before the
torso so the face and chest are never covered. Ladder: luyen_khi tiny wisps -> truc_co ribbons + low ground fog ->
ket_dan spirals + dan glow -> nguyen_anh flame outline -> hoa_than soft light beam + ground rings -> luyen_hu ring of fire +
glowing flame wings -> hop_the see-through frost sphere + glowing ice wings -> dai_thua galaxy + magic circle + glowing cosmic wings.

Proof: `art/src/fx/aura_proof.py` writes `art/preview/aura_on_chars.png` (pygame, 4x, dark + grass; winged realms also
right / up / slash hit / fly). `art/preview/fx_aura.png` is the contact sheet of the 16 aura sheets (shown additively on dark).

Look-and-fix log:
1. Additive auras washed out on grass (blue -> mint, violet -> white, orange -> pale yellow): all auras re-rendered as alpha
   sheets with palette colours; wing glow balloons removed and replaced by the silhouette glow sheets.
2. hoa_than: one soft beam brightest on the centre line, no edge lines, even double ground ring; truc_co: thin low fog
   wisps + the two ribbons (widened); luyen_khi: tiny short wisps; hop_the: sphere is rim + highlights only.
3. QC found the glow touching the frame edge on the widest slash frames: 2 px border cleared.
