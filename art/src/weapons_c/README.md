# WEAPONS_C — the six "kỳ binh" (kich, roi, am_khi, luan, phu, cam) × 8 grades = 48 weapons

## Production brief (blender-director)

**Type:** hero props (hand weapons), 6 types × 8 grades = 48 models, plus their 48 in-hand layers
**Target:** game: 32×32 icon atlas (≈26 px drawn) and 96×96 weapon layers over the player (pivot 48,82, 15° camera, head snap)
**Style:** `stylized-style` / `pixel-art-style` / `fantasy-worlds` (xianxia), chibi-exaggerated heads, 3-tone kit toon on the master palette
**Poly budget:** 300–3000 tris per visible pose (flat, chunky; silhouette matters, not density); 3–12 Principled materials
**Texture budget:** none — plain Principled (base colour, metallic, emission); kit custom props for ramp / glow / priority / halo
**Export:** `art/blender/weapons/<id>.blend`, root empty `SM_<id>` (props `name_vi`, `grade`, `type`, `poses`, `pose_default`), one mesh per material `SM_<id>_<mat>` (or `SM_<id>_<pose>_<mat>`), materials `MAT_<key>`
**Pivot:** grip at the origin, length +Z, flat side −Y, 1 unit = 1 m (halberd ≈1.6, axe ≈1.15, whip handle 0.2 + 0.62 lash, darts 0.3, chakram Ø0.3–0.36, zither 0.84 × 0.26 with its origin at the middle — where it is held)
**Animation:** no armature on the weapons; flexible / thrown weapons carry **pose meshes** (whip: `coil` / `arc` / `lash`; darts: `hand` / `fly`) switched per frame by the weapon-layer hook; the layers follow the player rig's own clips

**Active skills:** blender-director (brief, pipeline), blender-modeler (numbers-and-code bmesh, naming, cleanup),
prop-artist (scale, pivots, grounded props: zither, whip), hard-surface (blades, crescents, bevels, fittings),
pixel-art-style (texel discipline: ≥1 px features, halo-free glows where parts sit close), stylized-style (exaggerated heads,
shape language: crescents and flames = danger, rings = wheel), genre-rpg (loot-rarity read: dull grade 1 → glowing grade 8),
fantasy-worlds (xianxia material honesty), asset-optimization (budgets, one mesh per material), qa-review (look rounds below).

**Pipeline phases:** reference → blockout (numbers) → grade shape passes → kit icon render → in-hand layers through
`art/src/weapon_layers` → QC → contact sheets → look rounds (log below).

### Grade themes (shared with weapons_a / weapons_b)

1 Mộc crude wood / stone / hemp, no shine · 2 Thiết iron + red cord · 3 Bích Ngọc jade + bronze · 4 Kim Lam steel + gold + teal gem ·
5 Linh Quang spirit cyan-violet, emissive · 6 Hỏa Diệm flame, blackened gold · 7 Băng Dực ice + small wings · 8 Tinh Không cosmic purple + gold core + stars.

### Shape progression (every grade changes the silhouette)

* **kich** (halberd): 1 stone point + one stone crescent lashed with hemp → 2 iron point, one iron crescent with a bright edge, red tassel →
  3 jade point and crescent, bronze bars → 4 *phương thiên kích*: two steel crescents, gold, teal gem → 5 glowing crescents, gold feather
  wings → 6 wavy flame point, toothed burning crescents, black-gold spurs → 7 ice crescents with small wings under them → 8 purple
  crescents with gold edges, violet halo, stars.
* **roi** (whip): 1 braided leather rope, knots, hemp tuft → 2 iron nine-section chain (6 links), dart tip, red tassel → 3 jade links,
  bronze joints → 4 steel links, gold joints, gold handle with a teal pommel gem → 5 glowing cyan links → 6 burning links (flame licks
  when lashed) → 7 ice links, winged dart → 8 purple links, gold joints, stars. Three poses each: `coil` (one loop beside the handle),
  `arc` (swung back over the head), `lash` (thrown out straight with a travelling wave).
* **am_khi** (hidden darts): 1 three sharpened bamboo darts, hemp fletching → 2 three iron willow-leaf knives with red streamers →
  3 four jade knives, bronze rings → 4 four steel knives, gold inlay, teal hub → 5 four glowing needles → 6 four flame blades →
  7 four ice shards with tiny wings → 8 five star blades. Poses `hand` (a fan between the fingers) and `fly` (side by side, streaks from grade 5).
* **luan** (chakram): 1 bent-wood hoop lashed with hemp → 2 iron ring, six teeth → 3 jade ring, three bronze leaf blades →
  4 sun-and-moon wheel: gold ring, steel crescents, teal gem → 5 glowing double ring, gold crescent → 6 wind-fire wheel: flames all round →
  7 ice ring, crystal points, wings → 8 purple ring, gold rim, eight star points, gold core spokes.
* **phu** (axe): 1 stone wedge lashed to a branch → 2 bearded iron axe, hammer poll → 3 round jade crescent, bronze back spike →
  4 double-bit (labrys) with gold, teal gem → 5 glowing crescent with gold back wings → 6 jagged burning edge on blackened gold, spurs →
  7 ice crystal blade with back wings → 8 big purple double crescent, gold edges, halo, stars.
* **cam** (zither): 1 plain plank, three hemp strings → 2 dark wood, waist notch, bone bridges and studs, red tassels →
  3 jade board, bronze rims → 4 red lacquer, gold rims, cloud-carved gold head with teal gem → 5 violet board, glowing strings, crystal →
  6 black board, ember strings, flames from the tail → 7 frost-blue board, wings at the head → 8 purple star-field board, gold strings, gold ring.
  Every zither has one movable bridge per string in a slanting row (the zither's tell-tale) and a tassel hanging off the tail edge.

## Files

| file | runs in | what |
|---|---|---|
| `geom.py` | Blender | material library + `W` builder (box, cyl, seg, sph, ico, poly, strip, ring, tor), pose meshes, ornaments |
| `models.py` | Blender | one function per type, parameters per grade; `make(id)`, `build_one(id, dir)` |
| `scene.py` | Blender | writes the 48 `.blend` files, renders the icon atlas through `kit.render_icons` |
| `build.py` | venv python | the one command (QC + `art/preview/weapons_c.png`; `--layers` also renders the in-hand layers) |
| `preview_layers.py` | venv python | `art/preview/weapon_layers_c*.png` from the layer sheets (`composite.py`) |
| `zoom.py` | venv python | dev aid: icons at 5× for look rounds |

The in-hand layers use `art/src/weapon_layers` unchanged except for a backwards-compatible hook (`scene.py`: `pose_of` /
`set_pose`; models without pose meshes render byte-identically, checked on `kiem_1`) and the six new entries in `offsets.py`.

## Rebuild

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py                       # 48 models + atlas (~20 s)
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py --only kich_3,roi_5   # those blends, an atlas of only those
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py --layers --jobs 3     # + the 48 layers (~20 min) + previews
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapon_layers/build.py --only roi_4 --jobs 1   # one layer

Needs `art/blender/chars/rig_base.blend` (git-ignored; built by the character batch, or copied from the session that made it).

## For the programmers

* Wiring: `weapons.<type> = {layer: <type>_1, clip}` (kich/roi/phu `slash`, am_khi/luan `shoot`, cam `cast`) and
  `item_icons.by_weapon_type.<type> = "weapons_c"`.
* **Thrown weapons:** in `shoot`, `am_khi` and `luan` are **out of the hand on frames 3 (the strike, `events.hit`) and 4**, flying
  forward (≈0.26 / 0.5 m for the darts, ≈0.3 / 0.55 m for the chakram, which also spins), and back in the hand on frame 5. If the game
  draws its own projectile, start it from frame 4's position or hide the layer's frames 3–4.
* The whip reaches ≈0.8 m forward of the hand on slash frames 3–4 (the layer is shrunk a little by the fit pass where it would leave the frame).
* The zither is held in front of the chest only in `cast`; on the back in every other clip (including `die`).

## Look-fix log
