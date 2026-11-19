# WORLD_TILES: ground, terrain and nature props

## Production brief (blender-director)

**Type:** environment kit (tiles) + vegetation / rock / prop set
**Target:** 2D game, pygame, 480x270 screen, 16 px tiles, maps in Tiled
**Style:** pixel art from 3D (HD-2D spirit): calm lush base, sparse accents, three-tone cel bands from the kit, hard pixels, key light upper left
**Budget:** tiles 16x16, props 36-100 px, trees 48-72 px tall (1 m = 36 px), everything on the master palette `art/palette.json`
**Export:** `client/assets/v2/tiles/{base,terrain}.png+json`, `client/assets/v2/props/nature.png+json` (written by the kit)
**Pivot:** props on the ground at the base (`pivot`, relative to `rect`); `solid` = walk-blocking footprint, relative to `rect`
**Animation:** only `water_anim` (4 frames, the wave pattern moves 4 px per frame and loops exactly)

Active skills: environment-artist (modular kit, grid, seamless pieces), vegetation-artist (crowns, culms, ground pivot),
prop-artist (readable silhouette, scale), procedural-modeling (seeded scatter, no hand-saved state), materials (Principled,
one ramp per surface), pixel-art-style / hd-2d-style (texel discipline, hard steps), fantasy-worlds + biome-worlds
(xianxia village, snow / sand / lava / sky), qa-review (look, list defects, fix, look again).

### How it is made
* `build.py` (venv python) starts `scene.py` in headless Blender through the kit launcher. `scene.py` builds every model by
  script (numbers and code, nothing hand-saved), saves `art/blender/world_tiles/{base,terrain,props}.blend` (one `COL_<id>`
  collection per asset) and renders through `kit.render_tiles` / `kit.render_props`. Then `build.py` patches the json, runs
  the kit QC and writes the previews (`wt_preview.py`).
* Tiles are 3D patches seen from straight above (grass cones, pebbles, cobbles, planks, flagstones, mist wisps). A tile that
  must repeat with itself is built so that anything crossing an edge is repeated on the opposite side, and the kit's wrap
  check confirms the seam (score <= 2).
* Transitions (grass / path, grass / dirt, shore) are height-fields cut by a signed-distance shape: a raised grass bank, a
  contact shade line, foam on the shore. The 12 tiles of a pair (8 sides + 4 notch corners) come from the same shape, so
  they join. The cliff face is a height-field of stepped ledges with rounded risers and cracks (the face is lit by the kit's
  N.L bands: ledge tops light, risers in shadow); its grass lip, mossy ledges, a cast-shadow tile at the foot and a lighter
  yellower plateau top make the height read at a glance. Stairs are worn steps cut into the same rock.
* Materials are plain Principled. `wt_common.mat()` writes the master-palette colour the material should snap to
  (`kit_color`) and sets `kit_ramp` / `kit_glow` (glow only where the model really glows: herbs, crystals, wisps, lava).
  Small accents get `kit_priority`.
* Props are modelled in metres with the origin on the ground, plus a hard-edged contact shadow disc (one palette colour).

## The 32 px world and the village (added for the 2x game)
The game draws the world at 2x (one map tile = 32 screen px) while characters, monsters and the nature props stay at native size.
* `scene32.py` renders the same scenes as `scene.py` at twice the pixels per metre (`wt_common.DETAIL = 1.6`: smaller, more numerous
  tufts, pebbles, flowers, grain), not an upscale. Output: `client/assets/v2/tiles/base32.png/.json` and `terrain32.png/.json`
  (`"cell": 32`). `base32` has the same indices as `base.png` (0..20 = TILESET, water_anim 21-24, stone/plaza extras) plus the dirt
  variants; `terrain32` has the same names as `terrain` plus the isolated-cell tiles below. The 16 px sheets are untouched.
* **Dirt** (32 px sheet): plain worked earth with fine specks, nothing at the centre, 3 variants (`dirt` lists them) that tile with
  each other; only the third has two tiny off-centre stones.
* **Isolated cells** (`grass_path_*` and `grass_dirt_*`): `island` (all four sides grass: a soft round patch), `h`, `v` (1-cell
  strips, 8 px wide), `cap_n/cap_s/cap_e/cap_w` (strip ends; the name is the open side).
* **Autotile rule** (also in `terrain32.json` and `wt_preview32.autotile32`): n, s, e, w = the 4 neighbours are the same material.
  0 neighbours: island. 1: N present -> cap_s, S -> cap_n, E -> cap_w, W -> cap_e. 2 opposite: N+S -> v, E+W -> h. 2 adjacent (a
  corner): the missing sides in the order n s w e (nw ne sw se). 3: the missing side (n s w e). 4: the first missing diagonal in the
  order nw ne sw se gives in_<it>, none missing -> the centre tile. Strips are 8 px wide and blob edges 11 px: at turns and
  branches paint paths at least 2 cells wide.
* `scene_village.py` + `wt_village.py` build the buildings and structures (`client/assets/v2/props/buildings.png/.json`):
  hut, house_0..2, pavilion (4 frames), library, stall_0..1, shrine (4), furnace (4), anvil, board, well, lantern (4), portal (4),
  td_gate (4), realm_gate (4), sign, tablet, table, gate, mat, hive (4). Each rect is exactly 2x the old code-drawn sprite
  (hut 128x112, house 96x96, pavilion 128x128, library 128x112, stall 80x64, shrine 64x88, furnace 48x56, anvil 48x40, board 48x56,
  well 48x48, lantern 16x48, portal 64x80, td_gate and realm_gate 80x80, sign 32x40, tablet 32x48, table 48x32, gate 64x64,
  mat 48x32, hive 48x64). `pivot` = bottom-centre of the rect (W/2, H); the door of every building is at the bottom centre; the
  building base sits 5 px above the bottom edge (the contact shadow, drawn with the `kit_outline=0` recipe, fills the rest).
  **Animation layout:** the frames of an animated prop sit side by side in the atlas, frame 0 first; `rect` covers frame 0 and frame
  i is at `rect.x + i * rect.w`; `frames` is the count (4 for every animated prop: pavilion lanterns sway and pulse, shrine
  smoke rises 2 px per frame and loops, furnace flame flickers, lantern glow pulses, portal and realm gate swirl, td_gate curtain
  shimmers, hive bees circle). `solid` = [x, y, w, h] relative to the rect (null = walkable). Scale: the doors are about 56 px
  tall, the player (`dao_si_luyen_khi`, frame 96x96, pivot 48,82) about 52 px.
* Proofs: `art/preview/world_village.png` (480x270 at 3x, real player sprite), `art/preview/world_dirt_test.png` (islands, strips,
  patches and a 6x6 block of dirt).
* `build.py --parts 16,32,village` (default all) chooses what to render; `--no-render` repacks previews and patches json.

## Files
* `build.py`, `scene.py` / `scene32.py` / `scene_village.py` (Blender side), `build_lists.py` (names, order, collision footprints, Vietnamese names),
  `wt_common.py` (primitives, palette mapping), `wt_base.py`, `wt_terrain.py`, `wt_props.py`, `wt_preview.py` (16 px sheets, mock-ups), `wt_preview32.py` (32 px proofs, autotile rule), `wt_village.py` (buildings).
* `build.py --only a,b` renders only those tiles / props (use tile and prop names; it skips the patching and QC),
  `build.py --no-render` only repacks previews.
* A full build takes about 6 minutes.

## Tile names
**base.png** (index = TILESET position of `client/art/build.py`, gid = index + 1): grass x3, flowers x2, path x2, water,
bamboo_floor, stone, wood, plaza x2, dirt, dark_grass x2, ink x2 (dark spirit-mist ground), realm_floor x2, realm_wall;
then `water_anim` (4 frames, indices 21-24) and the extra variants `stone` +1 and `plaza` +1 (they are listed in the
json under the same name, after the original index).

**terrain.png**: for each pair `grass_path`, `grass_dirt`, `shore` the 12 tiles `_nw _n _ne _w _e _sw _s _se _in_nw _in_ne
_in_sw _in_se` (suffix = where the *outer* material lies); plateau: `cliff_nw cliff_n cliff_ne cliff_w cliff_e`,
`plateau_top` x3 (lighter grass for the top), `cliff_face_a` / `cliff_face_b` (+ `_l _r` ends, `a2 / b2` variants),
`cliff_shadow` (+ `_l _r`), `stairs_a / b`; `bridge_h`, `bridge_v`, shore ends `bridge_h_w / _e`, `bridge_v_n / _s`;
`snow` x2, `sand` x2, `lava_rock` x2, `cloud` x2.

## Prop names (nature.png)
bamboo_1..3, pine_1..2, tree_1..2, peach_tree, dead_tree, bush_1..2, rock_1..3, boulder, linh_thao_1..4 (Lam Tinh Thao,
Thanh Lo Thao, Da Quang Nam, Kim Tue Thao; glowing, with 1 px sparkles in the herb's colour), tall_grass, lotus, stump, log,
crystal_1..2 (emissive), cloud_puff_1..2, mushroom_ring.

## Notes for the kit owner
* `render_tiles` is fixed at 16 px: `scene32.py` repeats its loop with a 32 px camera using the kit's own functions (a `tile_px`
  argument would remove that copy).
* Single-quad blades of grass can vanish (face away from the camera); ground tiles use thin solid cones instead.

## Ground fixes, garden, bi canh and the TD kit (third batch for the 2x game)

### Ground (terrain32 / base32)
* New transition sets, each with the 8 sides, 4 inner corners and `island h v cap_n cap_s cap_e cap_w`, same naming and the same
  autotile rule as dirt: `grass_stone_*` (cobbles, centre `stone`), `grass_plaza_*` (flagstones, centre `plaza`), `grass_dark_*`
  (`dark_grass` inside grass, centre `dark_grass`), `dark_ink_*` (`ink` ground inside dark_grass, centre `ink`).
* `realm_edge_*` (12 tiles): slate floor outside, a raised wall block inside (the wall interior is `realm_wall`). `realm_floor` x2 and
  `realm_wall` already exist at 32 px.
* `dark_grass` now uses the cooler, brighter `jade` ramp of the master palette (clearly darker and cooler than `grass`, no longer
  gloomy) with the same calm texture as grass. Proof: `art/preview/world_stone_test.png`.

### Garden: `client/assets/v2/props/garden.png/.json` (frames side by side: frame i at `rect.x + i * rect.w`)
Old call -> v2 name(s). `old` is also written into each json entry.

| old call | v2 name(s) | size |
|---|---|---|
| `plot_bed(True)` | `plot_locked` (overgrown, rocks) | 64x64, drawn straight down |
| `plot_bed(False)` | `plot_open` | 64x64 |
| withered bed (`plot_bed` + wither) | `plot_dry` (pale cracked soil) | 64x64 |
| `plant(stage 0, ...)` | `<family>_0` (seed mound with a gold glint, 2 frames) | 48x48 |
| `plant(1..2, ...)` | `<family>_1`, `<family>_2` (sprout, growing), 2 frames of sway | 48x48 |
| `plant(3, rarity, ...)` | `<family>_3_<rarity>` (mature: bud / buds / first fruit in the rarity colour) | 48x48 |
| `plant(4, rarity, ...)` | `<family>_4_<rarity>` (budding: open blooms, sparkles for rare and above) | 48x48 |
| `plant(5, rarity, ...)` | `<family>_5_<rarity>` (ready to harvest: full bloom or ripe fruit, glow for rare / epic / legendary) | 48x48 |
| `withered(surf, wither)` | the game keeps applying its own greying filter to the v2 sprite (it works on any surface); `plot_dry` for the bed | |
| `seed_frames(rarity)` | `seed_common/rare/epic/legendary` (3 frames: bob, bob, glint) | 32x32 |
| `tag()` | `tag` (blank paper tag on a stake; the game writes the character) | 26x26 |
| `egg_frames(color)` | `egg_common/rare/epic/legendary` (3 frames: whole, cracked, lid tipping off with glow) | 24x32 |
| `decoration('den_long', f)` | `lantern` of `buildings.png` (4 frames) | 16x48 |
| `decoration('hoa_sen', f)` | `hoa_sen` (4 frames) | 28x24 |
| `decoration('chuong_gio', f)` | `chuong_gio` (4 frames) | 20x36 |
| `decoration('co_phuong', f)` | `co_phuong` (4 frames) | 20x52 |

* Families (6): `herb` (leafy), `flower`, `root`, `vine`, `shroom`, `shrub` (fruit). The old art varied only by stage, rarity colour and a
  per-key random leaf length; the game should pick the family with a stable hash of the key (`family = FAMILIES[hash(key) % 6]`, mirror
  horizontally when the next bit is set) so every word keeps its plant.
* Stages 0-2 do not depend on rarity (names without suffix); stages 3-5 exist per rarity (4 variants), which is the rarity treatment:
  accent colour (common pink, rare blue, epic purple, legendary gold), sparkles from stage 4 and an emissive glow at stage 5 for
  rare and above. Pivot = ground point (bottom centre of the rect, 4 px up); draw it at the bed centre.
* Egg tint: the four `egg_<rarity>` sheets carry the rarity colours; the old `egg_frames(color)` took a hex colour, so use the sheet of the
  rarity the colour belongs to (common grey, rare blue, epic purple, legendary gold).

### Bi canh: `client/assets/v2/props/realm.png/.json` (2x the old sprites, frames side by side)
| old call | v2 name(s) | size / frames |
|---|---|---|
| `rift(frame)` | `rift` | 48x64, 8 frames |
| `pedestal(active, lit)` | `pedestal_off` (inactive), `pedestal_on` (active), `pedestal_lit` (active and stood on) | 48x48 |
| `rune_tile(state)` | `rune_off`, `rune_idle`, `rune_next` (glowing edge), `rune_done` (gold); a sunken blank plaque, the game writes the number | 40x40, straight down |
| `pillar(tone, glow)` | `pillar_<1..4>_off` (red stroke) / `pillar_<1..4>_on` (glowing gold stroke) | 32x64 |
| `statue(frame)` | `statue` (frame 0 plain, frame 1 glowing eyes and motes) | 48x64, 2 frames |
| `mirror(frame)` | `mirror` | 96x80, 4 frames |
| `realm_exit(False, frame)` / `realm_exit(True, frame)` | `exit_closed` / `exit_open` | 64x48, 2 frames each |
| `chest(False)` / `chest(True)` | `chest_closed` / `chest_open` | 48x36 |
Tone strokes are abstract: level, rising, dip-and-rise, falling. No letters or digits anywhere.

### Tower defence: `client/assets/v2/props/td.png/.json` and `client/assets/v2/tiles/td24.png/.json` (the board's NATIVE 24 px cell)
* Tiles (`td24`, `cell: 24`): `grass` x2, `path` x2 and `td_path_<sides>`: a path cell whose letters (n, e, s, w in that order) are the sides
  where grass lies, e.g. `td_path_ns` is a horizontal strip, `td_path_none` an interior cell, `td_path_nesw` an island. Pick the letters from the
  4 neighbours that are not path (cells outside the board count as not grass: leave them out).
* Towers `tower_<role>_<level>` (24x30, ground point at the bottom centre, 3 px up; level 1-3 grows): the board has 7 roles. The math areas
  (`server/data/math/td.json`) map to roles as follows.

| role | math tower | silhouette |
|---|---|---|
| hoa | `tap_hop` Tháp Tập Hợp | bronze cauldron on a tripod, orbiting embers |
| thuy | `so_phuc` Tháp Số Phức | spiral coil of blue light around a rod |
| kim | `vecto` Tháp Vectơ | arrow ballista on a swivel (second bolt at level 2, gold at 3) |
| son | `ma_tran` Tháp Ma Trận | cube-lattice pylon, one to three wire cubes with glowing nodes |
| quang | `xac_suat` Tháp Xác Suất | urn mortar with one to three dice rising |
| ho_tro | `gradient` Tháp Gradient | slope ramp with a lens throwing a beam |
| moc | (wall tower of the word board) | palisade of stakes |
* `td_core` (4 frames, replaces the blue circle), `td_spawn` (4 frames, replaces the dark circle), `td_rock_0/1` (replace `B.rock`),
  projectiles `shot_hoa/thuy/son/quang` (3 frames) and `shot_kim` (2 frames), pointing right, pivot = centre; hit puffs
  `hit_hoa/thuy/kim/son/quang/puff` (4 frames, expanding, pivot = centre). The old `plant()` towers of `td.py` are replaced by the tower of the
  word's role; the word-plant itself stays a garden sprite.
* Proofs: `world_garden.png`, `world_realm.png`, `world_td.png`.
