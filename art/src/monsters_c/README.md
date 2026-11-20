# MONSTERS_C: seven new monsters, modelled, rigged, animated and rendered in Blender

## Production brief (blender-director)

**Type:** creatures: 4 normal (48×48, pivot 24,42) and 3 elite (64×64, pivot 32,56), each with a
dị chủng colour variant (`<id>_di`, same model, a second material colour/ramp set).
**Target:** pixel sprites for the game client (`client/assets/v2/monsters/`), rendered only
through the shared kit (`tools/blender/kit/`): 35° orthographic camera, 38 px per metre, 3-tone
cel shading on the master palette, 1 px outline, glow only where the creature has it.
**Style:** xianxia monsters at the MONSTERS_A bar. Readable black silhouettes, believable
anatomy (real pangolin, crocodile, raptor and butterfly reference), big simple shapes, glowing
eyes or face where there is one. No text, digits or Chinese characters anywhere.
**Lands:** Kiếm Trủng Sơn (steel, rust red, sword shards), Lưu Vân Cốc (cloud white, sky blue,
thunder), Vạn Tượng Trạch (blood red, marsh green, pale ghost fire), Lôi Kiếp Đài (thunder).
**Poly budget:** under 4k triangles per creature (low-poly solids at sprite scale); no textures.
Colour comes from Principled base colours given as **palette hex codes** (`common.hx`), so every
material lands on the palette entry that was meant (see "My choices").
**Pivot:** the ground point under the middle of the footprint; hovering creatures carry a flat
contact shadow there (like Kiếm Linh).
**Animation:** one armature per creature, the six contract clips: `idle` 4, `walk` 6, `windup` 4
(held telegraph), `attack` 4 (`events.attack.hit` = 1, the impact frame), `hit` 2, `die` 6;
four facings.
**Export:** kit `render_animated` sheets `<id>` and `<id>_di`; `.blend` files in
`art/blender/monsters_c/`.

### Active skills
1. blender-director: this brief, pipeline order, the validation gate.
2. creature-artist: anatomy grounding per body type (pangolin, crocodile, raptor, butterfly,
   hollow armour, lantern, ball lightning), silhouette tested from the 35° gameplay camera, rig
   joints planned during blockout.
3. blender-modeler: everything built from numbers in scripts (`plate`, `tube`, `ball`, `aim`),
   `COL_` / `SM_` / `MAT_` / `ARM_` naming, nothing saved by hand.
4. rigging: bone-parented hard parts, distance-weighted skins for soft parts (tails, cape, wisps),
   two-bone leg IK (MONSTERS_A `quadrupeds.Legs`), quaternion poses for the tilted lightning rings.
5. animation: pose tables with anticipation, follow-through and lag (hind wings, hands of the
   hawk's wings, tassels, capes and tails trail by a frame); loops close on themselves.
6. pixel-art-style: texel discipline - features at least 1 px (0.027 m), thin glowing lines
   without halo, compact silhouettes for 48 px.
7. stylized-style / fantasy-worlds / genre-rpg: shape language (round friendly butterfly,
   triangular hawk and crocodile, blocky armour), land colour identity, `_di` as the rarer look.
8. qa-review: fit checks before rendering, kit QC, contact sheets, 5× zoom crops, look rounds.

### Pipeline (all scripted)
- [x] Reference and planning (contract, kit API, MONSTERS_A worked example and previews)
- [x] Blockout and silhouette (kit renders from the first pass: about 20 s per creature)
- [x] Modelling from numbers, rig and clips (one file per creature)
- [x] Fit checks (`--fit`, `fitdir.py`), kit QC, contact sheets, zoom crops
- [x] Look-fix rounds (logged below)

## Files

| File | What |
|---|---|
| `build.py` | venv entry point: one headless Blender per creature (at most 2 at once), then QC, contact sheets, overview |
| `scene.py` | inside Blender: build one creature, save `art/blender/monsters_c/<id>.blend`, optional fit check, render `<id>` and `<id>_di` |
| `creatures_c.py` | the table id → (name_vi, frame size, builder, render options) |
| `common.py` | imports the MONSTERS_A helpers read-only; adds `hx` (palette hex → linear colour), `plate` (flat outlined plates: wings, feathers, scales, blades), `zigzag`/`bolt` (lightning), `hover_shadow`, `about` (turn the whole creature about a point), `write_clips` |
| `pangolin.py` | Thiết Giáp Thú |
| `ghost_swordsman.py` | Vong Hồn Kiếm Sĩ |
| `butterfly.py` | Vân Điệp |
| `hawk.py` | Lôi Ưng |
| `lantern.py` | U Minh Đăng |
| `crocodile.py` | Huyết Ngạc |
| `ball_lightning.py` | Lôi Linh |
| `zoom.py` | 5× crops of key frames (or `--all` frames) with optional existing monsters beside them, into `art/render/monsters_c/zoom_<id>.png` |
| `fitdir.py` | Blender-side: per frame and facing, the lowest projected row and side extents of one clip, with the part that is lowest (for balancing lying poses) |

```
python art/src/monsters_c/build.py                       # everything (about 6 min, 2 Blenders)
python art/src/monsters_c/build.py --only loi_ung         # one creature (comma list allowed)
python art/src/monsters_c/build.py --no-render --fit      # .blend files + fit check only
python art/src/monsters_c/zoom.py huyet_ngac --vs ma_tran_thu
blender -b art/blender/monsters_c/<id>.blend --python art/src/monsters_c/fitdir.py -- die
```

Outputs: `client/assets/v2/monsters/<id>.png/.json` and `<id>_di.png/.json`,
`art/preview/monsters_c_<id>.png` (every clip × every facing, both looks, 3×),
`art/preview/monsters_c.png` (all seven, every frame of every clip facing right, both looks,
with the Luyện Khí player at the same scale on the ground line).

## The creatures

Distances are measured from the monster's position (the pivot) in the direction it faces;
a tile is 16 px = 0.42 m. The sprite never travels far: the game moves the monster.

| id | frame | what it is | windup (held) → attack (`hit` = 1) | die | attack shape | dị chủng |
|---|---|---|---|---|---|---|
| `thiet_giap_thu` Thiết Giáp Thú | 48 | Pangolin with an arched back shingled in rows of broken steel blade-tip shards, a row of blade stubs on the spine, a sword hilt still stuck in its back, a small conical head with glowing eyes and a flicking tongue, digging claws and a thick shard-covered tail. Scaled 0.82. | hunches, then rolls into a ball of blades (tail band wrapped over it, eyes peeking out), rocked back and shivering → the ball rolls forward and slams, squashed (hit), bursts open into a low ram stance, settles | staggers, rolls up, tips over onto its side, eyes shut | line ahead, ~1.5 tiles (rolling ram) | gold shards, black skin, flame eyes |
| `vong_hon_kiem_si` Vong Hồn Kiếm Sĩ | 64 | Hollow armour on a glowing spirit wisp (no legs): general's helmet with red plume and gold crescent, empty black face with two cold eyes, lamellar cuirass with a gold heart-mirror, layered pauldrons, torn blood-red cape and tabard, a sword snapped a third of the way down. | thrust stance: sword shoulder twisted back, blade levelled at the hip, free hand aiming, eyes flaring → a straight lunging thrust, arm fully extended (hit), held, recovers | the spirit leaves; the armour drops straight down into a heap, helmet tipping off, cape draped over it, the broken sword left standing in the earth beside it | line ahead, ~2 tiles | black armour with gold, violet cloth, flame-orange ghost, gold eyes |
| `van_diep` Vân Điệp | 48 | Cloud butterfly: wide cloud-white forewings and swallowtailed hindwings with blue veins and a glowing cloud-curl spiral on each, furry thorax, big dark eyes with a catch-light, curled antennae with glowing tips, a short body thinning into mist. Hovers over a contact shadow. | a threat display: wings opened and turned flat toward the target so the four glowing curls face it like great eyes, body reared back → a downward wing clap throwing a puff of cloud forward (hit) | flutters down and settles on the ground, wings closed upright, the mist gone | cone ahead, ~60°, 1.5 tiles (gust) | peach-pink wings, violet veins, gold curls |
| `loi_ung` Lôi Ưng | 64 | Thunder hawk hovering on wingbeats: storm-blue back and broad two-bone wings with five separate primaries fanned like fingers, lightning glowing at every primary and crest tip, pale chest with bars, dark hood with a pale throat, hooked gold beak, fierce eye and brow, fanned tail, gold legs and dark talons. | rises and folds its wings tight into a stoop, pitched head-down, talons drawn up, bolts crackling round it → dives, flares its wings to brake and rakes with talons thrust forward (hit), beats back up | tumbles down and lies on its breast, wings folded | line ahead, ~2.5 tiles (dive; the game moves it) | black and crimson, gold lightning, flame eye |
| `u_minh_dang` U Minh Đăng | 48 | Ghost lantern: an old paper lantern with dark ribs and lacquered caps, a ring on top, a torn patch, slanted glowing eyes and a jagged grin burning through the paper, a pale ghost flame curling out of the top, three red tassels with gold beads, a wisp tail. Hovers. | draws a breath: swells, tilts back, flame sucked down small and hard, eyes narrowed → lunges, the grin gapes and the flame flares out in a burst of ghost fire (hit) | the flame gutters out, the eyes go dark, it drops and rolls onto its side | cone ahead, ~45°, 1.5 tiles (fire breath) | violet lantern, black ribs, green ghost fire, gold tassels |
| `huyet_ngac` Huyết Ngạc | 64 | Blood-red marsh crocodile, chibi-long (1.2 m, scaled 0.8): broad flat skull with raised eye turrets and glowing eyes, heavy lower jaw, a toothy grin even when shut, two rows of dark scutes, moss on its back, sprawling clawed legs on IK, a tall crested tail swept round to one side like a basking croc. Carries its head raised. | rears its front, throws its head back and gapes, jaws wide, pink mouth and teeth, tail curled hard aside → lunges and snaps shut (hit), wrenches its head sideways (start of a death roll), settles | a last thrash with jaws to the sky, then sinks into the marsh tail first inside rings of mud ripples | cone ahead, ~45°, 1.5 tiles (snap) | black with a red crest, grey belly, green eyes |
| `loi_linh` Lôi Linh | 48 | Ball-lightning sprite: a shaded storm-blue core with glowing cracks and a white-hot face (slanted eyes and grin set in dark sockets), short crackling spikes, two broken rings of zigzag lightning orbiting on tilted axes with sparks at their ends, sparks trailing when it moves. Hovers. | charges: swells, rings pulled in tight and spinning hard, spikes standing long, eyes narrowed → discharges: bolts lash forward (one to the ground just ahead, two level), rings blown outward (hit) | flickers, shrinks and pops to nothing over its shadow | line ahead, ~2 tiles (bolts) | gold core and holy-gold lightning, red sockets |

## Look-fix rounds (what was wrong before each change)

Every round: kit render of the base look, `zoom.py` 3–5× crops of the key frames (idle, walk,
held windup, attack hit frame, hit, die) in all four facings next to Phong Lang, Kiếm Linh,
Ma Trận Thú or Tâm Ma, plus `--fit` / `fitdir.py` / kit QC.

**All seven, round 3 (colour):** every material snapped one or two entries too light: salmon
croc and cape, pale pangolin, grey "white" wings. Cause: the kit reads Base Color as linear and
converts to sRGB before snapping, and I had typed sRGB values. Fix: `common.hx("#rrggbb")`
gives the palette entry's linear value; every material was re-pinned to the entry meant.

**Thiết Giáp Thú**
1. Side view was a long flat fish; shards were ~3 px white specks reading as feathers or chain
   mail; front view a faceless egg; the curled windup a tangle with skin showing; it filled the
   frame edge to edge. → arched body, bigger and darker shards, bigger head, a dedicated rolled
   ball form on its own bone, `arm.scale` 0.88.
2. Still a long slab (armadillo / pill bug), bigger than Phong Lang (the scale had not applied:
   `attach`/`skin` keep world size, so the scale must be set after parenting), hunch frame
   under the ground. → shorter, taller arched body, tail arcing up, scale 0.82 set last.
3. Tail thin from the side, back not arched enough; ball frames 5–6 px low and touching the
   bottom edge (shards stick out past the ball, the tail band hangs low). → domed back profile,
   thick five-row tail, ball lifted onto its shards, tail band moved over the top.
4. (5× after the colour fix) shard checker read as noise; eyes' halo merged with the claws into
   one yellow blob; head too small to show a face from the front. → shard materials alternate
   by row, eyes without halo, bigger head. Ram pose then dipped the bigger snout 5 px low → head
   raised in the ram.

**Vong Hồn Kiếm Sĩ**
1. Face plate inside the helmet (no face, no eyes from the front); cape salmon and flooding the
   back view; the sword pointed up and back in windup and thrust (the wrist angles added up past
   vertical). → face and eyes brought forward, cape darker, wrist angles recomputed so the blade
   is level.
2. The thrust left the frame sideways (body lunge + arm + blade > 31 px); the death heap toppled
   toward the camera and left the frame. → shorter broken blade, less lunge (the game moves it),
   armour collapses straight down.
3. Arms and sword of the heap still reached the frame bottom from the side, the neck glow stayed
   lit after death. → arms fall inward, the sword is left standing in the earth beside the heap
   (Kiếm Trủng Sơn grave marker), neck glow on its own `soul` bone that fades.
4. (5×) eyes read, thrust reads, black-gold `_di` strong. Windup blade only half visible behind
   the hip from the side: accepted (the levelled stance and aiming hand carry the telegraph).

**Vân Điệp**
1. Idle frame 0 caught the wings near vertical: a thin "Y" from the front (a flower or candle);
   the mist abdomen a long cyan stick (a lollipop); head and eyes invisible; antennae only from
   behind; swept-back windup edge-on. → beat kept in the open range, short abdomen, bigger head
   and eyes with a catch-light, taller antennae, whiter wings (light band earlier).
2. New flat "display" windup foreshortened to a line by the 35° camera. → the wings twist about
   their span so their faces turn to the target.
3. Lying-flat death left the frame (a flat wing toward the camera). → it settles with wings
   closed upright.
4. (5×) display and wide frames read well. Weak: side views at the top of the beat, where
   forewing and hindwing overlap, look crumpled; the swallowtail is lost at 48 px.

**Lôi Ưng**
1. Primaries merged into one paddle; lightning-tip halos rimmed every wing edge in lavender; all
   one blue; tiny head; tail long like a cat's; the stoop windup a blob from the front. →
   narrower primaries fanned 0–57° with gaps, small tips without halo, white chest and head on a
   dark slate back, bigger head with eye stripe and brow, shorter tail, more and bigger charge
   bolts.
2. Death on its side with spread wings left the frame from behind. → wings folded; then lying on
   its breast, centred between the facing that sees the head and the one that sees the tail
   (`fitdir.py`).
3. (5×) white head on white chest read as an owl or penguin from the front. → dark hood, pale
   throat, dark eye stripe.

**U Minh Đăng**
1. Face glow and its halo blurred eyes and mouth into a cyan mask and leaked round the outline;
   tassels were specks. → no halo on the face, smaller separated eyes, narrower grin, longer
   tassels, slightly taller lantern, a curled flame.
2. Attack flare cut at the top facing away; lying tassels pointed at the camera. → flare aimed
   more forward, tassels crumple in death.
3. (5×) reads at a glance. Weak: at 1× the eyes and grin sometimes merge into one cyan band.

**Huyết Ngạc**
1. Fit check: on a 64 px elite only ~7 px fit below the pivot, so a long croc facing the camera
   is cut by the frame bottom. → chibi-long proportions, scale 0.8, head carried raised, tail
   swept round to one side, rearing gape for the windup (upper jaw thrown up, lower jaw level).
2. Salmon-orange from an early light band (and the linear-colour error); jaw 1–2 px out of frame;
   belly-up death left the frame. → deep blood red, higher head, shorter snap lunge.
3. Every lying death reached the frame bottom from some side. → it sinks into the marsh jaws
   first to the sky, tail going under first, inside mud ripple rings (fits its taunt about the
   mud); balanced with `fitdir.py`.
4. (5×) reads as a croc from the side at once. Tried to bring it inside the normal 5 px standing
   rule (narrower foot splay, higher head, centre moved back): it reaches 5–7 px, snout from the
   front against tail from behind. Kept as declared ground clips.

**Lôi Linh**
1. A white puff: core flat white, dark face lost, six orbiting arcs plus haloed sparks made a
   fuzzy cloud. → two rings, wider, sparks without halo, dimmer core, white-hot face.
2. The glow ramp maps a whole sphere to its core colour, so the face vanished again. → the core
   is a solid shaded storm-blue sphere with a metal glint and glowing cracks; the arcs and
   spikes carry the lightning.
3. (5×) reads as ball lightning; face only specks, sprite small. → core 0.13 → 0.15 m, rings
   wider, bigger eyes and grin set in dark sockets.
4. Weak: the face is partly hidden whenever a ring passes in front of it.

## My choices

- **Colours as palette hex (`hx`).** The kit converts Base Color from linear to sRGB before
  snapping; MONSTERS_A typed sRGB-looking numbers, which land one or two entries lighter than
  they look. This batch names the palette entry it wants, so a material lands exactly there.
- **Huyết Ngạc declares all six clips as `ground_clips`** (kit option, written to
  `render.ground_clips`). QC then allows its lowest row up to 16 px below the pivot instead
  of 5. Its body is long and low; seen from 35° the snout (facing the camera) or the tail
  (facing away) honestly draws 5–7 px below the pivot. Feet jitter and sideways-drift rules
  still apply and pass. Everything else in the batch passes the standard rule.
- **Croc carries its head raised**, and its tail is swept round to one side: the frame
  (64 px, pivot y 56) leaves only ~7 px below the pivot, so a croc with its jaw on the ground
  cannot face the camera without being cut.
- **Croc dies by sinking into the marsh**, the hawk by lying on its breast, the armour by
  collapsing straight down: any long body lying flat reaches the frame bottom in one of the four
  facings.
- **Pangolin curl = a separate rolled-ball form** on its own bone, swapped in by bone scale
  (the walking body is scaled away): a believable rolled pangolin cannot come from bending the
  walking body's rigid shards.
- **Butterfly windup is a threat display** (wings turned to face the target, curls like eyes)
  rather than wings swept back, which vanish edge-on from the 35° camera.
- **Lôi Linh's core is solid, not glow**: a glowing sphere renders as a flat disc that hides the
  face; the lightning lives in the rings, spikes and cracks.
- **Ghost wisp, ghost flame and the butterfly's mist glow** (the contract's "glow only where the
  creature has it"); armour, paper, feathers, scales are solid.
- **Scales:** pangolin 0.82, crocodile 0.8 (`arm.scale`, set after parenting); sizes chosen
  against Phong Lang (48) and Ma Trận Thú / Tâm Ma (64) at the same zoom.
- **Attack hit frame = 1** for all seven (MONSTERS_A convention), attack shapes as in the table.
- `fitdir.py` and `zoom.py` are tools of this batch; `art/src/monsters_a/` is untouched (its
  `rig.py`, `quadrupeds.py` and `fitcheck.py` are imported read-only).
