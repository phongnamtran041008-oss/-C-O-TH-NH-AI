# fx_tien_ich - production brief (blender-director)

**Type:** effects (no characters), 38 FX sheets. **Target:** game, 480x270 pygame, FX sheets of `docs/ART_PIPELINE.md` section 4.
**Style:** pixel art from 3D (pixel-art-style) + stylized xianxia manhua glow (stylized-style); RPG loot-rarity language (genre-rpg);
FX built as real Blender scenes (vfx-fx): flat emissive meshes, keyframed, orthographic camera, EEVEE 6x, post by `art/src/fx/fxpost.py`
(area downscale, 1-2 px halo, OKLab snap to `art/palette.json`).
**Budgets:** 64 / 96 / 128 px frames, 4-11 frames, every scene < 3k tris. 1 unit = 28.6 px (camera margin 12 %).
**Export:** `client/assets/v2/fx/<id>.png + .json`; scenes `art/blender/fx_tien_ich/<id>.blend` (git-ignored); contact sheets
`art/preview/fx_tien_ich_{phi,roi,linh_can,khac}.png`; proofs `fx_tien_ich_{roi,phi,linh_can}_proof.png` (+ `fx_tien_ich_phi_ground_proof.png`).
**Pivot:** see the table. **Skills used:** blender-director, vfx-fx, pixel-art-style, stylized-style, genre-rpg, qa-review.

Rebuild: `"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_tien_ich/build.py [--only id,id] [--jobs 2] [--no-proof]`
(imports `fxlib.py` / `fxpost.py` of `art/src/fx/`, edits nothing there; `tilib.py` = FxP subclass with pivot-relative coordinates and
billboards, column mesh, motes).

## The sheets
| id | frame | frames | fps | loop | blend | ground | pivot |
|---|---|---|---|---|---|---|---|
| phi_bong | 64 | 4 | 6 | yes | alpha | yes | 32,32 |
| phi_vet | 96 | 6 | 12 | yes | add | no | 80,48 (sword tail; trails LEFT) |
| phi_gio | 64 | 6 | 12 | yes | add | no | 32,32 |
| phi_may | 96 | 6 | 8 | yes | alpha | no | 48,56 (feet) |
| phi_cat_canh | 96 | 7 | 14 | no | alpha | yes | 48,48 |
| phi_ha_canh | 96 | 6 | 14 | no | alpha | yes | 48,48 |
| roi_cot_{pham,linh,huyen,dia,thien} | 96 | 8 | 8 | yes | add | no | 48,84 (base of the column) |
| roi_vong_{...} | 64 | 6 | 8 | yes | add | yes | 32,32 |
| roi_nhat | 64 | 6 | 14 | no | add | no | 32,32 |
| linh_can_1..9 | 128 | 11 | 12 | no | add | no | 64,108 |
| linh_can_tru_1..9 | 128 | 8 | 10 | yes | add | no | 64,108 |
| trac_linh_thach | 96 | 6 | 6 | yes | alpha | no | 48,84 |
| thanh_tuu | 96 | 10 | 12 | no | add | no | 48,48 |
| uy_ap | 128 | 8 | 10 | no | alpha | yes | 64,64 |

Rarity ladder (hue AND shape AND strength): pham grey = glints + haze, dashed ring | linh green = short column, plain ring |
huyen blue = taller column + bright core, ring + 4 ticks | dia purple = tall + crossing blades, double ring + 6 nodes |
thien gold = tallest, orbiting halo, crown star, ground star, double ring + 8-ray star.
Linh can ladder: 1 grey flicker | 2 ochre low glow | 3 blue column | 4 purple + blades + rune ring | 5 gold + halo + whiteout |
6 white-gold fan of beams + big halo | 7 jade helix + lotus | 8 flame column + flame ring | 9 cosmic vortex, stars, cracks, big whiteout.
The last `linh_can_<n>` frame equals the `linh_can_tru_<n>` steady state (hand over there).

## Look-and-fix log (what was wrong, then what changed)
1. First contact sheet: `phi_vet` clipped at the left edge and shifted (pivot offset had the wrong sign; also 1 unit is 28.6 px not
   32 because of the camera margin) -> FxP uses the real px/unit. Dust of `phi_cat_canh`/`phi_ha_canh` was a heap of huge coins with
   highlights -> puffs are now small three-bump clouds (shade + lit layer), fewer, flying outward; stray drops at the start/end of
   the `phi_may` clouds -> steeper scale window and hidden below 25 %.
2. Loot sheets: pham read as a grey gravestone -> only a very faint short haze + two twinkling glints; the white core line ran
   through the 32 px weapon icon -> core starts above the icon (0.85 u), column base is dimmer; blades start beside the icon;
   ring discs of thien hid the ground -> lower opacities; thick grey-brown rim of snapped low-intensity halo -> halo 0.8 -> 0.5;
   `roi_vong_thien` touched the frame edge -> smaller radii. Linh can: pillars faded out at half height and the whiteout was a hard
   white disc (frame-filling grey blob for giai 9) -> columns keep brightness to the top (p 0.45), whiteout = soft glow in the giai
   colour + small solid core, limited to 1.6 u; crown star and downward rays cut at the frame edge -> moved / shortened.
3. Proofs in context: flat hard top on the columns -> tip fade; wind streaks crossed the character's face -> draw wind behind the
   character; `phi_bong` was a hard black hole (the keyframed `op` replaced the material opacity) -> real 0.3-0.45 alpha, soft;
   `thanh_tuu` seal turned into a white blob with white spikes -> star in gold, white only for the cross and jewel, rays gold and
   shorter (rays also touched the frame edge). `uy_ap`, `trac_linh_thach`: stele got a band and a finial so it is less a gravestone.
QC: `qc.py client/assets/v2/fx` -> OK (0 problems).

## Known weak points
- The stele is flat-shaded stone with a glowing face; it still reads a little like a tombstone. `hon_don` has no true black (additive
  sheets cannot subtract): it is dark violet, rings and stars instead.
- On bright grass the additive wake/loot columns shift hue (cyan -> mint, purple -> pale). That is the nature of `add`.
