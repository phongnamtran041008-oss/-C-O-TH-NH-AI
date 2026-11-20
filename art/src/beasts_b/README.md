# BEASTS_B: six more spirit beasts (linh thú), modelled, rigged, animated and rendered in Blender

## Production brief (blender-director)

**Type:** creatures (companion spirit beasts), six, one look each
**Target:** pixel sprite sheets for the pygame client (`client/assets/v2/beasts/<id>.png/.json`),
rendered by the shared kit (`tools/blender/kit/`): kind "beast", 48×48, pivot (24,42), 38 px per
metre, orthographic camera 35°, four facings, three-tone cel shading on the master palette, 1 px
outline. Same scale conventions as the first six beasts (`art/src/monsters_a/beasts.py`).
**Style:** xianxia manhua spirit beasts at chibi-companion proportions: big heads, big readable
eyes with a catch-light, round appealing silhouettes, glow only where the creature has it (ear
tips, gem, coin, eyes of the toad, brow mark, tail tips, flame feather edges). No text, no
Chinese characters (the tiger's brow carries an abstract diamond and diagonal strokes, never a
bar pattern).
**Poly budget:** under 4k triangles per beast (simple solids and skinned tubes at sprite
scale); no textures, colour from Principled base colours pinned to palette ramps.
**Pivot:** ground point under the middle of the footprint (`set_root_offset` where a tilted
body sits back, as on the toad).
**Animation:** armature per body plan; the eight beast clips: `idle` 4 (6 fps, loop), `walk` 6
(10 fps; 11 for the quadrupeds, 12 for the scurrying mouse, as the first six vary), `windup` 4
(8), `attack` 4 (14, `events.attack.hit` = 1), `hit` 2 (12), `die` 6 (10; faints and lies
down, never vanishes), `happy` 4 (8, loop: hop + quarter-turn spins, squinting), `sleep` 4 (4,
loop). Each sprite frame is one key (rig.clip), loops repeat their first pose.
**Export:** kit `render_animated` → sheet + JSON; `.blend` per beast in `art/blender/beasts_b/`.

### Active skills
1. blender-director: this brief, pipeline order, the validation gate.
2. creature-artist: anatomy per body plan (lagomorph sit and hop, upright rodent, squat anuran
   with three legs, felid cub, slender vulpine, raptor chick); joint placement planned in the
   blockout so every gait is possible.
3. blender-modeler: everything from numbers (balls, cones, tubes, prisms), named `SM_`/`MAT_`/
   `ARM_`, one `COL_<id>` per beast.
4. rigging: rigid parts on bones, distance-weighted skins for soft parts (rabbit and toad front
   legs between a shoulder bone and a planted hand bone, mouse tail, the nine fox tails), the
   shared quadruped IK rig for tiger and fox.
5. animation: pose tables with anticipation (windups), follow-through (ears, tails, crest,
   wings lag a frame), squash and stretch on the hop cycles, treadmill feet (planted feet drift
   back, the game moves the beast).
6. pixel-art-style / stylized-style: texel discipline (features ≥ 1 px, eyes and marks at kit
   priority), shape language (round = friendly), limited palette, value contrast first.
7. fantasy-worlds / genre-rpg: xianxia material honesty (jade, gold, moonlight, flame) and
   a creature's region read through its colour and prop.
8. qa-review: kit QC, contact sheets, 5×/8× look rounds next to the existing six, honest verdict.

### Pipeline (all scripted, nothing saved by hand)
- [x] Reference and planning (ART_PIPELINE.md, kit README, monsters_a worked example, the
      existing beast previews and sheets)
- [x] Blockout and silhouette (first kit renders, judged at 5× and 8×)
- [x] Modelling from numbers (one module per beast)
- [x] Rig and animate (same modules; `common.py` holds the shared helpers)
- [x] Render, pack, QC and contact sheets through the kit (`scene.py`, `build.py`, `previews.py`)
- [x] Look-fix rounds (log below)

## Files

| File | What |
|---|---|
| `build.py` | venv entry point: one headless Blender per beast (at most 2 at once), then QC, contact sheets, overview, line-up, zooms |
| `scene.py` | inside Blender: build one beast, save `art/blender/beasts_b/<id>.blend`, render through the kit. `--clips a,b` renders a look-round subset into `art/render/beasts_b/wip/` (never the game folder); env `BEASTS_B_HIDE=name,name` drops parts in such a WIP render (debugging) |
| `common.py` | imports the monsters_a helpers read-only (`rig.py`, `beasts.py`, `quadrupeds.py`); adds `hexc`/`mat`/`glow`/`set_ramp`, `finish` (the eight clips), and `quad_poses` / `quad_extra_poses`: copies of `quad_clips` / `extra_quad_clips` that return the pose lists so a beast can decorate them |
| `ngoc_tho.py` … `kim_si_dieu.py` | one builder per beast (`build()` returns the armature) |
| `previews.py` | `art/preview/beasts_b.png`, `beasts_b_lineup.png`, `beasts_b_zoom_<id>.png`; `previews.py zoom <id>` (5× key frames), `previews.py close <id>` (8× faces into art/render), `previews.py wip <id>` |

```
python art/src/beasts_b/build.py                     # all six (about 3 min, 2 Blenders)
python art/src/beasts_b/build.py --only kim_thiem    # one (comma list allowed)
python art/src/beasts_b/build.py --no-render         # .blend files only
python art/src/beasts_b/build.py --only x --clips idle,walk   # look round
python art/src/beasts_b/previews.py zoom             # 5x key frames of all six
blender -b art/blender/beasts_b/<id>.blend --python art/src/monsters_a/fitcheck.py
```

## The beasts

| id | name_vi | body plan / rig | look | windup / attack | attack shape (suggested) |
|---|---|---|---|---|---|
| `ngoc_tho` | Ngọc Thố | sitting rabbit: hips (squash/stretch), chest, head, two-bone ears, skinned front legs between shoulder and planted paw bones, root feet | white fur, dark shiny eyes, pink nose and ears, glowing jade ear tips, gold crescent mark on the brow, red cord with a jade bead | rears up on the hind feet, paws up like a boxer / hop-lunge and double paw strike | line ahead, ~1.5 tiles |
| `tam_bao_thu` | Tầm Bảo Thử | upright mouse: hips, chest, head, round ears, arms (the gem rides the left arm), root feet, three-bone skinned tail | warm chestnut fur, coin-gold belly, round pink ears, white whiskers, buck teeth, glowing spirit gem hugged to the belly, red treasure pouch with a gold tie, pink curling tail | hoists the gem above its head / bonks forward, the gem flaring on the hit | line ahead, ~1 tile |
| `kim_thiem` | Bích Nhãn Kim Thiềm | squat toad tilted nose-up 12° on straight front legs: body, head, jaw, throat sac, eyes, coin bone, skinned front legs to planted hands, ONE hind leg in the middle | deep amber-gold warty skin with bright gold warts, cream belly and throat, glowing jade eyes with slit pupils on top domes, a wide smile, a glowing square-holed coin in its lips, three coins down its back | puffs up, throat sac swelling / spits the coin straight ahead (a new one appears) | line ahead, ~2 tiles (coin projectile) |
| `bach_ho_con` | Bạch Hổ Con | shared quadruped rig (IK legs, level paws), eyes bone | chunky white cub, round head with cheek ruffs, dark-backed round ears, blue eyes, pink nose, glowing ice brow diamond, tapered back stripes, brow strokes, leg stripes, ringed tail with a dark tip, big paws | crouch with a cat's butt-wiggle / pounce-bite | line ahead, ~2 tiles |
| `cuu_vi_ho` | Cửu Vĩ Hồ | shared quadruped rig + nine two-bone skinned tails fanned ±92° | slender white fox, gold almond eyes, red kitsune liner and brow mark, tall ears with gold insides; nine tails alternating cream and gold with glowing gold tips: a sunburst behind the head from the front, a rising plume in profile; tails sway out of phase in every clip, tips lagging | crouch, fan flaring / pounce-bite with the fan swept back | cone ahead, ~60°, 2 tiles |
| `kim_si_dieu` | Kim Sí Điểu | bird biped (like bach_hac): body, neck, head, crest, two-bone wings (covert pad + five primaries on the hand), tail fan, two-bone legs | gold raptor chick with a cream chest, hooked steel-blue beak, dark eyes under a stern brow, swept red crest; deep-gold and gold primaries and tail feathers with flame-bright glowing tips | wings flung up in a great V, crest raised / forward wing sweep and lunging peck | cone ahead, ~60°, 1.5 tiles |

## Look rounds (what was wrong before each change)

Judged at 5× (`beasts_b_zoom_<id>.png`) and 8× (`previews.py close`), next to the first six.

### Ngọc Thố
1. Head too small (a doll on a body); ears thin sprouts with big saturated green "leaf" tips;
   the crescent poked out like a yellow beak and read as a mouth smear; eyes invisible in
   profile; die overflowed the frame bottom, hit/up sank. → head 0.15→0.17 wide, broader and
   longer ears, glow tips smaller and halo 0 (pale jade, "soft"), crescent flush on the brow.
2. Eyes rendered as brown smudges: `rig.apply_variant` re-applies `ramp_base`, so a plain
   `kit_ramp` override was lost (the iris fell to "earth"). → `common.set_ramp`; die became the
   bunny flop onto its side, hit lean reduced.
3. Jade irises read as green specks at the cheek edge, the white face had no dark accent. →
   big dark eyes with a white shine, pink blush.
4. Profile had no eye (cheek fluff covered it); both ears overlapped into one stick. → tried
   side-set eyes (worse: smaller from the front, still hidden), went back to front eyes placed
   exactly on the head surface; asymmetric ear rest (left stands, right leans back).

### Tầm Bảo Thử
1. Ears seen edge-on in profile read as a horn; whiskers + dark eyes read as goggles and a
   moustache; drab grey-brown fur; die toppled toward the camera; attack/down sank. → warm
   wood-ramp fur, one pale whisker pair low on the snout, die shifted to stay centred.
2. No face in profile (no snout, head like a hood); ears turned too far became pointy. → a real
   pointed snout, pink nose at the tip, bigger round ears turned 25° and set back, bigger gold belly.
3. The far ear still a spike in profile; sleep bowed too far forward (frame edge). → ears lower
   and wider; sleep posture upright.
4. The hoisted gem vanished: short arms put it inside the head at 112°. → `gem_up` slides the
   gem along the turned arm so it rises above the brow (windup and happy).

### Bích Nhãn Kim Thiềm
1. One pale gold everywhere: body, head and warts merged into a lump; the mouth coin did not
   read from the front; the body was too long so up/down sank 5-6 px. → deep amber-gold skin
   with bright gold warts, a glowing mouth coin, taller eye domes, a shorter body, tucked toes.
2. Mouth line invisible; hit/up and attack/down still sank. → thicker smile, less squash and
   pitch in hit and spit.
3. Profile a shapeless lump. → 12° nose-up rest tilt on straight front legs: the sitting
   toad's wedge, with the cream throat showing.
4. The tilt pushed the haunch back (walk/up, windup/up sank). → root offset 1.2 cm forward,
   hind foot only skims in the hop, smaller splat.

### Bạch Hổ Con
1. Evenly spaced vertical stripes read as a zebra / ribcage; a big dark "eye" smear on the
   side of the head in profile; pale ice-glow irises vanished on white fur; long thin legs (a
   kitten on stilts). → shorter thick legs and heavier body, fewer tapered stripes on the upper
   flanks only, saturated blue eyes with dark pupils (the aura stays in the glowing brow diamond).
2. The dark mark stayed; the tail stood up behind the head like an antenna. → tail sweeps
   back and low.
3. Hunted the mark with WIP renders that drop parts (`BEASTS_B_HIDE`): not the pupils, not the
   stripes, not the ruffs — the lower half of each dark ear disc poked out of the side of the
   head. → ears re-placed on the crown.

### Cửu Vĩ Hồ
1. From the front the nine tails formed a flat disc at head height (a straw hat); in profile
   an edge-on brush; gold socks read as hooves (a goat); grey ruff read as a collar; die/up
   touched the edge. → tails rebuilt as a tall plume that opens into a semicircle; cream paws
   and ruff.
2. Profile now a rising plume, but the front fan was one pleated paper fan that swallowed the
   head. → bundle goes back before rising, ±92° spread, slimmer bases, narrower glowing tips
   (gaps between tips), alternating tail values.
3. Nine tips now separate, but the head was the same cream as the fan and dissolved into it. →
   white body (the "white" of white-gold), tails alternating cream and gold.
4. Face too small to read from the front. → bigger head, eyes, ears and kitsune marks; fan
   centre lowered.

### Kim Sí Điểu
1. A yellow chick / chocobo with a rooster comb: folded wings hidden in an egg body, flame tips
   invisible on gold, a one-pixel beak, die clipped. → longer primaries crossing past the tail,
   deep-gold/gold alternating feathers with bright flame tips and a 1 px halo, a big hooked
   beak, crest swept back.
2. From the front the folded wings hid inside the body; die clipped down/left. → wings set out
   on the flanks, tail lifted when it sits, gentler topple.
3. Glowing amber eyes vanished on the gold face. → dark eyes with a white shine.
4. Still no eyes from the front: the brow boxes sat in front of and above them and covered
   them from the 35° camera. → brows moved back and up; die wings kept up.

## Still weak (honest)

- **Kim Thiềm** is small (about the size of Huyền Quy; a 1.10-1.15 scale was tried after the
  line-up and failed the standing rule in the up facing, so it stays 1.0) and its profile is a lumpy wedge; the
  third leg reads only from behind / in the hop. The coin's square hole is a single dark pixel
  at best; at 1× the coin reads as a bright glint.
- **Tầm Bảo Thử** in profile: the far ear still shows as a short spike above the head and the
  snout is small; the front view is the strong one.
- **Kim Sí Điểu** keeps a little of the chick in its egg-shaped body from the front (a young
  roc, but the "proud" read comes mostly from the profile, beak and crest); its sleep and die
  silhouettes are blobby.
- **Cửu Vĩ Hồ** legs are straight columns (the shared rig's stance); from behind the fan covers
  most of the body.
- Faces are 3-4 px features: they read at 3× and up; at 1× the eyes are 1-2 px like the first six.
