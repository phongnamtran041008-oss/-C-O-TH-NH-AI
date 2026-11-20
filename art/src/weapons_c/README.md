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
  forward of the right hand, which `shoot` (the bow clip) has drawn back to the chest (≈0.42 / 0.62 m for the darts, ≈0.45 / 0.62 m for the chakram, which also spins), and back in the hand on frame 5. If the game
  draws its own projectile, start it from frame 4's position or hide the layer's frames 3–4.
* The whip reaches ≈0.8 m forward of the hand on slash frames 3–4 (the layer is shrunk a little by the fit pass where it would leave the frame).
* The zither is held in front of the chest only in `cast`; on the back in every other clip (including `die`).

## Look-fix log

Judged at 3× (contact sheets) and 5× (`zoom.py`) next to `art/reference/vu_khi/vu_khi_8_loai_10_bac.webp`,
`art/preview/weapons_a.png`, `weapons_b.png` and `weapon_layers*.png`.

1. **Icons, first render.** Wrong: the kích's crescent was invisible (a band hugging the shaft, same colour as the point), so it
   read as a spear; the whip was noisy squiggles; the ám khí a blob; the zither a plank / scroll with no strings.
   Causes found: (a) `kit.render_icons` draws every descendant of the object given, so passing the root drew all
   three whip poses (and both dart poses) on top of each other — now only the default pose's meshes are passed;
   (b) the crescent's edge arc was nearly parallel to its back — rebuilt as two circles meeting at the horn tips (a true
   crescent moon, horns pointing away from the shaft), much bigger (R 0.21–0.29 m), standing off the shaft on two bars,
   shaft shortened 0.16 m; (c) dart blades were twice as wide as meant (half-width parameter) and converged on one point —
   slimmer blades, bases spread across the fist; (d) zither strings were 0.4 px wide and, with priority, painted the whole
   board — 3–4 strings on a 0.26 m board, darker boards, one bridge per string in a slanting row, a side tassel, and the
   icon laid flat (strings at 72° or 45° became stair-step lattices; level they are clean lines).
2. **Icons, second render.** Wrong: grades 5–8 of the darts and the whip still merged into feathery fans — the 1 px glow
   halo of each emissive blade filled the 1–2 px gaps between them (they read as a fan, i.e. the wrong weapon). Added halo-free
   twins of the glow materials (`*_n`, `kit_halo = 0`) for parts that sit close together; fewer, wider-spaced darts on
   glowing grades. Also: the double-bit axe read as a hammer (white rectangles) — narrower neck, taller bits, darker iron
   body so the bright edge reads; the ice zither was one white bar (emissive board) — frost-blue board.
3. **Layers, first composites** (representatives, Luyện Khí). Whip, axe, chakram and darts read; the zither in `cast` sat at
   hip level like a low table and was hidden on the back when facing down — raised to the chest, back carry turned
   diagonally so both ends show. QC: the zither's `die` frames touched the bottom edge (still strapped on as the body falls)
   — it now slips off and lies beside the body; roi_1's lash was entirely behind the body facing up on the strike — the lash
   now leaves at a slight outward angle.
4. **Layers, all 48** (`weapon_layers_c_all.png`, `_dai_thua.png`). Wrong: the thrown darts / chakram appeared over the
   torso on the strike frame — `shoot` is the bow clip, the right hand is drawn back to the chest when it releases. Flight
   offsets increased (they are counted from the chest). Grade-8 whip coil was cluttered by star specks — specks kept only on
   the swung / lashed chain.

### Still below the reference (honest list)

* **Kích icons**: at 26 px for a 1.6 m weapon the head is ~7 px; the crescents read as a cross / "(|)" shape, clearly not
  a spear, but nowhere near the crisp halberd heads the reference can afford. In the hand (2× the scale) they read well.
* **Zither icon** reads as a stringed board seen flat (strings, bridges, tassels) but is a thin 8 px strip; the
  reference has no zither to compare with. In `cast` it is a board with strings in front of the chest — it reads as an
  instrument being played, but small.
* **Thrown weapons on the strike frame** still overlap the chest (frame 4 is clearly in flight); pushing them further makes
  the fit pass shrink them.
* **Whip icon** is a loop with a handle — readable, but the grade-8 one is busy; the nine-section links read as beads at 26 px.
* The luân grade 1–3 icons are plain rings: a chakram without blades reads as a ring (deliberately crude at grade 1; grade 2
  teeth and grade 3 blades are only 1–2 px).
* On the winged realms (Luyện Hư, Hợp Thể, Đại Thừa) the back carry (zither, darts, chakram) is largely hidden by the wings,
  same as the existing types.
