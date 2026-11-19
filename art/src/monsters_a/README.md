# MONSTERS_A: six math-mistake monsters, modelled, rigged and animated in Blender

## Production brief (blender-director)

**Type:** creatures (monsters, 4 normal + 2 elite), each with a dị chủng colour variant
**Target:** pixel sprites for the pygame client (`client/assets/v2/monsters/`), rendered by the
shared kit (`tools/blender/kit/`): 35° orthographic camera, 38 px per metre, 3-tone cel shading
on the master palette, 1 px outline. Normal monsters are 48×48 (pivot 24,42), elites are 64×64
(pivot 32,56).
**Style:** chibi xianxia monsters, matching the author's reference sheets
(`art/reference/nhan_vat`, `vu_khi`, `phap_tran`): oversized heads and eyes, big simple
shapes, dark outlines, saturated glow only where it means something (eyes, runes, cores). There is
no text, no digits and no Chinese characters on any creature. The math reads through dots, grids and abstract
strokes.
**Poly budget:** under 3k triangles per creature (low-poly solids at sprite scale); no textures.
Colour comes from Principled base colours that the kit snaps to palette ramps.
**Pivot:** the ground point under the middle of the footprint (`rig.set_root_offset` puts long
bodies' footprint centre on it).
**Animation:** armature per body type and the six monster clips of contract §3: `idle` 4,
`walk` 6, `windup` 4, `attack` 4 (`events.hit` = 1, the impact frame), `hit` 2, `die` 6.
**Export:** kit `render_animated` sheets `<id>` and `<id>_di`, plus the `.blend` files.

### Active skills
1. blender-director: this brief, pipeline order, validation gate.
2. creature-artist / character-archetypes: anatomy logic per body type (floating blade spirit,
   stacked golem, quadrupeds, serpent chain, biped shade).
3. chibi-style / stylized-style / fantasy-worlds: proportions, shape language (blocks = stable
   golem / lion, triangles = sword, wolf tufts and blades), xianxia material honesty.
4. pixel-art-style: texel discipline. Features of at least 1 px (0.027 m), glow lines without a halo,
   compact silhouettes for 48 px.
5. rigging / animation: bone-parented hard parts, distance-weighted skins for soft parts (ghost,
   serpent, smoke), two-bone leg IK, pose tables with anticipation, follow-through and lag.
6. qa-review: fitcheck (frame and float/sink rules before rendering), kit QC, contact sheets
   compared against the reference.

### Pipeline (all scripted, nothing saved by hand)
- [x] Reference and planning (reference sheets read, kit contract and QC rules read)
- [x] Blockout and silhouette (workbench previews, then kit renders)
- [x] Modelling from numbers (`creatures.py`, `quadrupeds.py`, `serpent_shade.py`, helpers in `rig.py`)
- [x] Rig and animate (same files; `fitcheck.py` checks every frame against the frame and pivot rules)
- [x] Render, pack, QC and contact sheets through the kit (`scene.py`, `build.py`)

## Files

| File | What |
|---|---|
| `build.py` | venv entry point: one headless Blender per creature (parallel), then QC, contact sheets, overview |
| `scene.py` | inside Blender: build one creature, save `art/blender/monsters/<id>.blend`, render `<id>` and `<id>_di` through the kit |
| `rig.py` | materials with a normal and a dị chủng colour/ramp set (`apply_variant`), solids, tubes, extruded outlines, armature, rigid attach, distance-weighted skinning, pose tables in armature axes, clips, ground shadow, holdout ground |
| `creatures.py` | Kiếm Linh, Thạch Khôi, and the `BUILD` table (id → name_vi, frame size, builder) |
| `quadrupeds.py` | shared quadruped rig, leg IK and clip generator; Ma Trận Thú, Phong Lang |
| `serpent.py` | Vân Xà |
| `serpent_shade.py` | Tâm Ma |
| `bestiary_b.py` | MONSTERS_B: Đầu Tử Oa, Hồ Lô Tinh, Mộc Yêu, Cơ Quan Nhân |
| `spider.py` | Tri Chu Tinh (radial two-bone leg IK, quaternion poses) |
| `dragon.py` | Thiên Kiếp Lôi Long (boss, with the `special` clip) |
| `beasts.py` | the six catchable spirit beasts (kind "beast", `happy` and `sleep` clips, no dị chủng) |
| `pets.py` | the twelve zodiac pets of `server/data/creatures/pets.json` (kind "pet": idle, walk, happy, sleep) |
| `bee.py`, `bee_scene.py` | the spirit bee: one rig, one sheet per species of `server/data/creatures/bees.json` |
| `fitcheck.py` | Blender-side check: projects every deformed vertex through the kit camera for every frame and facing, and reports overhang past the frame edge and the lowest row versus the pivot (kit QC rule). Also prints the ground footprint centre |

```
python art/src/monsters_a/build.py                 # everything (about 8 min, 3 Blenders at once)
python art/src/monsters_a/build.py --set b         # only the MONSTERS_B half (--set a: the first half)
python art/src/monsters_a/build.py --set beasts    # the spirit beasts -> client/assets/v2/beasts, art/blender/beasts
python art/src/monsters_a/build.py --set pets      # the zodiac pets -> client/assets/v2/beasts/pet_<id>, art/preview/pets.png
python art/src/monsters_a/build.py --set bees      # the 18 bees -> client/assets/v2/beasts/bee_<id>, art/preview/bees.png
python art/src/monsters_a/build.py --only tam_ma   # one creature (comma list allowed)
python art/src/monsters_a/build.py --no-render     # .blend files only
blender -b art/blender/monsters/<id>.blend --python art/src/monsters_a/fitcheck.py
```

Outputs: `client/assets/v2/monsters/<id>.png/.json`, `<id>_di.png/.json`,
`art/blender/monsters/<id>.blend`, `art/preview/monsters_a_<id>.png` (every clip, both looks),
`art/preview/monsters_a.png` (idle / held windup / attack hit frame, facing down and right).
The second half writes `art/preview/monsters_b_<id>.png` and `art/preview/monsters_b.png`
(the boss row adds its `special` hit frame).

## Conventions

- Pose tables (`r`, `l`, `s` per bone) are written in **armature axes** and converted to each
  bone's frame in `rig.set_pose`: x = right of the picture when the creature faces the camera,
  y = behind the creature, z = up. A +x rotation tips an upright bone forward and swings a hanging
  bone's tip backward.
- Each sprite frame is one key: frame i of a clip is action frame i + 1. Loops repeat their first
  pose as a last key, so the kit's even sampling lands exactly on the keys.
- Dị chủng is a material variant. Every `MAT_` keeps `col_base` / `col_di`, emission and the
  `kit_ramp` / `kit_glow` per look; `rig.apply_variant("di")` switches them. The same rig and
  clips are rendered twice.
- Floating creatures (Kiếm Linh, Tâm Ma) carry a small ground shadow parented to the armature
  object. It keeps the sprite's lowest row on the pivot, as the kit QC requires, and shows the
  hover.
- The kit allows only a few pixels below the pivot in the steady clips. So the stances are chibi-compact,
  attacks lunge only a few centimetres, and the reach is shown by body extension. **The game is
  expected to move the monster or draw the hit zone; the sprite does not travel.**

## The creatures, and the attack shape each animation suggests

Tiles are 16 px = 0.42 m. Distances are measured from the monster's position (the pivot) in
the direction it faces.

### Kiếm Linh (`kiem_linh`, normal 48): linear-algebra land, sword-tomb mountain
The sword is the creature. A big chipped blade hangs point-down, with abstract dash runes and an
arrow chevron glowing down the fuller, so the blade *is* the vector arrow. It has a gold guard
with upswept horns and a red tassel. A small pale ghost wisp is wrapped round the hilt, with its
two glowing eyes just above the guard, a curled flame tip on top, ribbons spiralling down round
the blade and a wispy tail streaming back. It hovers over a small ground shadow. Rig: root,
body (hover), ghost (squash and stretch), two-bone tail, little arms, sword (pivot at the
guard), tassel. Windup: the blade pulls back and tilts its point at the target while the wisp
puffs up and the tail curls. Attack: a straight forward stab with the blade horizontal, the
wisp stretching behind it, then recovery to point-down. Die: the spirit thins away and the
empty sword drops point-first into the ground, left standing at a tilt like a grave marker
(holdout ground). Dị chủng: violet wisp, dark blade, flame-orange eyes and runes.
**Attack shape: line ahead, about 2 tiles long and 1 tile wide.**

### Thạch Khôi (`thach_khoi`, normal 48): stone golem
Body built as a 3×3 matrix of stone blocks (checkered grey stone and brown earth, one bone per
row), moss in the gaps and on the shoulders, a glowing core in the centre cell, a big block head
with glowing eye slits and a moss cap, oversized fists. Windup: both fists raised high overhead,
body leaning back, rows shifting. Attack: double-fist ground slam at its own feet, rows
jolting on impact. Die: knees buckle, the head topples, and the rows slide apart into a rubble
pile with the core still faintly lit. Dị chủng: obsidian blocks, rust lichen, flame core.
**Attack shape: circle around itself, radius about 1.5 tiles (the slam's shockwave).**

### Ma Trận Thú (`ma_tran_thu`, elite 64): guardian lion
Blocky jade guardian lion with glowing grid lines wrapping its chest and rump. Its mane is two
rings of square gold plates set like diamonds, it has a big square face with glowing eyes
under angry gold brows and a glowing line on the brow, gold leg cuffs and claws, and a square
plate tuft on the tail. Rig: spine (pelvis, chest), head, jaw, two-bone legs with level-keeping
paws (IK), two-bone tail. Windup: low crouch on coiled hind legs, head down, jaw parted, tail
up and lashing. Attack: a short hop forward (front paws reaching), then a pounce-bite with
the head driving down. Die: roars, buckles onto its belly, then crumbles away. Dị chủng:
violet stone, silver plates, cosmic grid.
**Attack shape: cone ahead, about 60°, 2 tiles long (pounce).**

### Vân Xà (`van_xa`, normal 48): calculus land, flowing-cloud valley
A water-blue serpent that rises from a small ground coil in a tall sine curve (three to four
bends, the calculus motif) to a big round chibi dragon-snake head. The head has gold horns,
cloud brows, crest and cheeks, long cloud whiskers, fangs and glowing eyes. Pale belly scales run
down the front, glowing flow dots dot the body, cloud puffs ride the back of the bends, and the
tail lifts off the coil and frays into mist. It is built upright because the camera allows
height and sideways sway but hardly any ground in front of the pivot. Rig: root (coil), tail,
ten body bones (one skinned tube), a head kept level against the sway, and a jaw. Idle and walk
run a travelling sine wave up the body. Windup: it rears up tall and coils back like a drawn
bow, mouth wide, tail rattling. Attack: a whip-fast lunge that snaps the body nearly straight
toward the target, jaw wide on the hit frame. Die: it sways, sags and folds down onto its coil
in a heap, head resting on top. Dị chủng: storm violet with grey cloud, thunder flow dots and
flame eyes.
**Attack shape: line ahead, about 2 tiles long (lunging bite).**

### Phong Lang (`phong_lang`, normal 48): wind wolf
Lean chibi wolf in pale steel-blue fur with a big head, tall ears, a long snout, amber
glowing eyes under slanted brows and a pale ruff. Glowing teal wind tufts stream back along
its spine, cheeks, crest and tail tip. Rig: the shared quadruped rig (IK legs, paws kept level).
Walk is a quick trot. Windup: low crouch, head down, jaw open, tail up. Attack: a hop and a
fast lunge-bite. Die: collapses and blows away. Dị chủng: dusk violet with thunder-blue tufts
and flame eyes.
**Attack shape: line ahead, about 3 tiles long (fast lunge; the game should move the wolf along it).**

### Tâm Ma (`tam_ma`, elite 64): inner demon, a mistake coming back
A dark-violet shadow copy of a chibi cultivator: big head, violet hair with a large bun, a pin
and trailing ribbons, bangs and side locks, hollow dark sockets with white-cyan glowing eyes, a
robe with a crossed collar, fold ridges and sash, wide sleeves with faintly glowing cuff trims,
and smoke instead of legs (a skinned three-bone smoke tail that curls, with side wisps). It holds
a shadow blade with glowing edges. Its materials start the cel light band earlier
(`kit_light`), so the dark body keeps a lit rim and internal form. Windup: blade raised straight up overhead, body twisted
and leaning back, off hand thrust forward to aim. Attack: the blade comes over the top and cuts
diagonally down across the body (hit frame), and the twist carries through. Die: it flinches,
sags, then swells and dissolves upward into nothing. Dị chủng: crimson shade with gold collar and
holy-gold eyes.
**Attack shape: cone ahead, about 90°, 1.5 tiles long (diagonal slash).**

---

# MONSTERS_B: the second half of the bestiary

Same pipeline, rules and helpers (kit v1.1: `pink` and `paper` ramps, flat contact shadows
with `kit_outline = 0`). Every creature has the six clips with a held, readable windup plus
a `_di` look; the boss adds `special` (8 frames, `events.hit` = 4).

| id | name_vi | frame | idea, rig and animation |
|---|---|---|---|
| `dau_tu_oa` | Đầu Tử Oa | 48 | Probability land: a fat marsh toad (scaled 1.3). Its warty back is three stacked die-shaped warts with dot pips (dots only, no numerals). It has bulging glowing eyes, a pale belly and a throat sac. The tongue is a bone stretched along its length. Idle: the sac pulses and the eyes blink. Walk: a hop cycle. **Windup: squats, tips its head up and the throat sac swells to twice its size.** Attack: the tongue lashes straight out, slightly upward. Die: deflates flat and the dice tumble off. Dị chủng: violet skin, gold dice, red pips. |
| `ho_lo_tinh` | Hồ Lô Tinh | 48 | A two-bulb calabash imp (scaled 1.15) with a red cord at the waist, a leaf-and-stem topknot, glowing eyes and a grin in the upper bulb, a cork, and stubby arms and feet. **Windup: rears back hugging itself, swelling, with the cork working loose.** Attack: the cork pops up, the gourd tips forward and sprays a cone of coloured glowing spirit beads (four glow colours). Die: arms, legs and eyes shrink away, leaving a plain gourd. Dị chủng: violet gourd, gold cord, cosmic eyes. |
| `tri_chu_tinh` | Tri Chu Tinh | 64 | Graph land: a spider (scaled 1.12) in a wide, arched stance. Eight two-bone legs fan out radially with high, wide knees (lighter knee joints, legs 2–3 px thick), and the feet are planted in a tight ring by a planar IK. A distinct cephalothorax carries a cluster of six glowing eyes and pale fangs, with a narrow waist before the lower abdomen. The abdomen carries a glowing graph of six nodes joined by eight edges, visible from above and behind. Walk: a tetrapod gait. **Windup: rears up with the front legs raised high and spread, fangs open and the abdomen cocked.** Attack: a pounce, the front legs stabbing down just ahead and the fangs snapping shut. Die: drops and folds its legs over its body. Dị chủng: red shell, gold graph, spirit eyes. |
| `moc_yeu` | Mộc Yêu | 48 | A walking stump: a faceted bark trunk with a cut top showing its rings, knot-hole eyes with green glowing pupils, a mouth hole and moss. Three two-bone root legs. A sapling crown branches like a tree diagram (one trunk, two branches, four twigs) with leaf clusters and two blossoms. Walk: a root waddle. **Windup: rises on its roots with the crown flung wide and high.** Attack: slams down, roots stabbing into the earth, crown whipping forward and leaves flying. Die: the crown wilts and droops and the eyes go out. Dị chủng: dark bark, crimson leaves, gold blossoms, flame eyes. |
| `co_quan_nhan` | Cơ Quan Nhân | 48 | Programming land: a chunky wood-and-bronze clockwork puppet (scaled 1.15). Its barrel chest of staves and bronze hoops has an open front window showing one big, clearly toothed gear (top pixel priority), a small second gear and a glowing core. A large wind-up key sits on its back, reading from the side and from behind. Big round lantern eyes sit in bronze rims; the limbs are thick with ball joints. Gears and key turn in every clip. Walk: a stiff marionette step. **Windup: arms flung straight out like a spinning top, torso twisted far back.** Attack: a full spin with the arms out. Die: sags into a sit, a gear pops loose and the eyes go dark. Dị chủng: iron, red fittings, cosmic eyes. |
| `loi_long` | Thiên Kiếp Lôi Long | 96 | The tribulation boss, filling about 80 % of the frame: a thick eastern dragon (about twice its first build) boiling up out of a dark storm cloud. Twenty skinned body bones: a rise, one full upright coil seen face-on as a ring, then a neck straightening over it to a big head with a long snout, an open jaw with teeth, big gold antler horns, a flowing white mane down the neck and long whiskers. Bright violet-white lightning fins run down the spine; two arms carry big gold claws. The base is a storm cloud of violet-grey billows over a flat dark underside, with lightning flickering inside and small bolts dropping from it, in two sets that blink alternately. **Windup: rears to the full frame height, head thrown back, jaw wide, arms spread, lightning crackling all round.** Attack: the head lunges down and forward in a bite. **Special: rears to the top of the frame, roars at the sky, and a bolt strikes down onto its horns (hit frame 4).** Die: the body slumps back down over its coil into the shrinking cloud. Dị chủng: red-gold fire dragon, black horns, flame lightning. |

### Attack shapes (MONSTERS_B)

| id | shape | size |
|---|---|---|
| `dau_tu_oa` | line ahead | ~2.5 tiles long, 1 wide (tongue lash) |
| `ho_lo_tinh` | cone ahead | ~60°, 2 tiles (bead spray) |
| `tri_chu_tinh` | line ahead | ~3 tiles (pounce; the game should move it along the line) |
| `moc_yeu` | circle around itself | radius ~1.5 tiles (root slam) |
| `co_quan_nhan` | cone ahead | ~120°, 1.5 tiles (spinning arm swipe; a near-circle is also fair) |
| `loi_long` attack | cone ahead | ~45°, 3 tiles (lunging bite) |
| `loi_long` special | circle at a target point | radius ~2 tiles, called down from the sky; the game chooses where (on the player), drawing the warning circle during frames 0–3 and striking on frame 4 |

---

# SPIRIT BEASTS (linh thú)

Companions the player tames and keeps, so they are built to be appealing: big heads, big
shiny eyes (iris, pupil and a white catch-light, all at top pixel priority), round, clean
silhouettes and a little spirit glow. Kind "beast", 48×48, four facings, one look each.
Output goes to `client/assets/v2/beasts/<id>.png/.json`, blends to `art/blender/beasts/`,
and previews to `art/preview/beasts.png` (idle, windup, attack, happy, sleep, facing down
and right) and `art/preview/beasts_<id>.png`.

Clips: `idle` 4, `walk` 6, `windup` 4, `attack` 4 (`events.hit` = 1), `hit` 2, `die` 6
(faints and lies down; it never vanishes), plus **`happy` 4** (a hop with quarter-turn
spins and happy squinting eyes, looping) and **`sleep` 4** (curled up with closed eyes,
breathing, looping). An `eyes` bone closes the eyes for blinks, sleep and fainting.

| id | name_vi | look | windup / attack |
|---|---|---|---|
| `linh_ho` | Linh Hồ | White spirit fox: big head, tall ears with blue tips and pink insides, gold glowing eyes, cheek fluff, and a huge fluffy tail tipped with blue spirit flame. Quadruped rig with IK legs. In sleep it curls up with its tail wrapped round. | crouches, tail up, jaw parted / pounce-bite |
| `huyen_quy` | Huyền Quy | Small black tortoise: domed jade shell with hexagon plates (a glowing one at the crown and glowing dots on the six around it), a sleepy kind face with heavy eyelids, a smile and pink blush, stubby legs. | pulls head and legs into the shell, which rises / the shell spins and bursts out |
| `bach_hac` | Bạch Hạc | White crane: red crown, black face patch and wingtips, black tail, golden beak, long grey legs with toes. Wings spread wide in `happy`; it sleeps on one leg with its head tucked back. | raises both wings high in a V, neck drawn back / a great downbeat gust |
| `hoa_tuoc` | Hỏa Tước | Round fire-sparrow chick, scaled 1.25: orange-red ball body with a gold belly, pink blush, a three-feather flame crest and a three-feather flame tail with glowing tips, little glowing wingtips and gold toes. | puffs up, crest flaring tall, wings out / spits a fireball straight ahead |
| `tieu_long` | Tiểu Long | Baby eastern dragon: jade green with a cream belly, a big head with gold antlers, cream mane puffs and whiskers, a glowing spine ridge, short legs with cream claws, and a tail curling up to a cream tuft. A ground runner the player will ride later. | crouches, tail up / pounce-bite |
| `ky_lan_con` | Kỳ Lân Con | Qilin foal: deer-like cream body on long legs, gold scale plates down the back, a single small jade horn, a cloud-flame mane, flaming fetlocks above gold hooves, a flame tail, gentle brown eyes and pink blush. | crouches / horn charge |

### Attack shapes (spirit beasts, fighting beside the player)

| id | shape | size |
|---|---|---|
| `linh_ho` | line ahead | ~2 tiles (pounce-bite) |
| `huyen_quy` | circle around itself | radius ~1 tile (shell spin) |
| `bach_hac` | cone ahead | ~60°, 2 tiles (wing gust) |
| `hoa_tuoc` | line ahead | ~3 tiles (fireball, a projectile the game spawns on frame 1) |
| `tieu_long` | line ahead | ~2 tiles (pounce-bite) |
| `ky_lan_con` | line ahead | ~2.5 tiles (horn charge; the game moves it along the line) |

---

# PETS (Linh Thú gacha: the twelve con giáp)

One sheet per species id in `server/data/creatures/pets.json`, named `pet_<species id>`:
`pet_chuot pet_trau pet_ho pet_meo pet_rong pet_ran pet_ngua pet_de pet_khi pet_ga pet_cho
pet_lon` in `client/assets/v2/beasts/`. Blends are in `art/blender/beasts/` and the preview is
`art/preview/pets.png`.

- **Kind "pet"**: 48×48, pivot (24,42), 38 px/m, four facings. The clips are `idle` 4,
  `walk` 6, `happy` 4 (a hop with quarter-turn spins and happy squinting eyes, looping) and
  `sleep` 4 (curled up with closed eyes, breathing, looping). The kit QC requires no combat
  clips for this kind.
- **Size:** the game draws beast and player sheets at the same scale per sheet pixel
  (compare `art/preview/game_hub_idle.png`), so a pet about 0.45 m tall stands at the
  player's knee-to-hip. The preview shows the Luyện Khí player at the same 3× beside the
  first row.
- **Build:** ten species share one chibi quadruped body on the IK leg rig, with per-species
  parts taken from the `look` data: ears (round / pointed / side / floppy / pig / monkey),
  tails (thin / tuft / long / fluffy / horse / curl / dragon), horns (ox / goat / antler),
  stripes, patch, mane, beard, monkey face and snout type. The rooster and the snake have
  their own rigs.
- **Eyes:** every pet has big eyes (iris, pupil, white catch-light, all at top pixel
  priority) and an eyes bone for blinking and sleeping.

| species | xianxia touch |
|---|---|
| `chuot` Chuột | big round ears, glowing spirit-blue tail tip |
| `trau` Trâu | broad muzzle, horns, gold nose ring, glowing gold brow mark |
| `ho` Hổ | stripes, glowing gold brow mark (an abstract diamond, no Chinese character) |
| `meo` Mèo | orange patches, red collar with a gold bell |
| `rong` Rồng | antlers, red mane, glowing green spine fins, a floating spirit pearl |
| `ran` Rắn | small coil and raised neck, glowing green dots along the back |
| `ngua` Ngựa | dark mane and tail, a flame wisp on the forelock |
| `de` Dê | curled horns, beard, red tassel on a horn |
| `khi` Khỉ | heart face, curled tail, gold circlet |
| `ga` Gà | red comb with a glowing tip, teal tail with a glowing tip |
| `cho` Chó | floppy ears, red collar tassel |
| `lon` Lợn | snout, curly tail, glowing green brow mark |

**Colours.** Each species uses its own `look` colours from pets.json. Each part is pinned to
the palette ramp that keeps that hue (`RAMPS` in `pets.py`; three body colours are nudged
within their hue in `TINT`). The data defines **no colour looks and no rarity variants**,
so each species has one sheet. If rarity looks are wanted later, they would work like the
monsters' `_di` (a second colour and ramp set on the same materials, a second render).

---

# BEES (Linh Phong)

**One sheet per species**: `client/assets/v2/beasts/bee_<species id>.png/.json` for all 18
species of `server/data/creatures/bees.json` (`bee_muc` … `bee_kim_o`). They come from one
rig (`bee.py`) rendered 18 times with each species' colours on the shared materials. The blend
is `art/blender/beasts/bee.blend` and the preview is `art/preview/bees.png` (every species at
4×, on dark and on the grass tiles of `base32.png`).

- **Frame:** 32×32 with the pivot (16,16) on the body centre; it flies, so there is no ground
  point. The camera is lowered to 12° (`elevation=12`) so the bee is seen side-on. The bee is
  about 0.5 m long, so about 19 px drawn. Kind "bee": QC asks for no clips.
- **Shape:** an abdomen with three stripe bands (short cylinders about 2 px wide, with 2 px of
  body colour between them), a dark round thorax, a head with one big eye and a light pixel,
  pale wings (the `wing` colour lightened 35%) standing above the back and beating between up
  and down, a stinger, and two antennae with element-glow tips. `TWEAK` in `bee.py` gives
  near-identical pairs a visible band or wing difference. `bees.png` starts with a 1× strip of
  all 18 on grass.
- **Facings:** `right` and `left` only.
- **Clips:** `fly` (4 frames at 12 fps, looping: the wings beat up, level, down, level
  with a little bob) and `sting` (2 frames at 12 fps: a lunge with the abdomen curled
  forward, then recoil; `events.sting.hit` = 0).
- **Look → model:** `body` colours the head and abdomen, `stripe` the three abdomen bands and the thorax,
  `wing` both wings, and `eye` both eyes. Every eye also gets a white catch-light. The
  antenna tips glow in the colour of the species' `element`:

| element | glow ramp |
|---|---|
| mac | cosmic |
| moc | verdant |
| thuy | spirit |
| hoa | flame |
| phong | ice |
| tho | holy |
| kim | holy |
| bang | ice |
| loi | thunder |
| quang | holy |

- **Why one sheet per species rather than a palette swap:** at 16 px the 3-tone shading,
  the outline (a darker shade of the colour it borders) and the stripe/body contrast all
  depend on which ramp each colour lands on. A flat key-colour swap of one sheet would keep
  the first species' shading for all of them. The look colours are snapped to the nearest
  palette ramp by the kit, so species with near colours (thảo / trà, thủy linh / vũ) differ
  mainly in stripe and eye.
