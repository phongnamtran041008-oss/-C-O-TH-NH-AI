# MONSTERS_D: six new monsters for three lands

## Production brief (blender-director)

**Type:** creatures, 4 normal-sized and 2 elites, each with a dị chủng colour variant.
**Target:** pixel sprites for the game client (`client/assets/v2/monsters/`), rendered by
the shared kit (`tools/blender/kit/`): 35° orthographic camera, 38 px per metre, 3-tone cel
shading on the master palette, 1 px outline. Normal monsters 48×48 (pivot 24,42), elites
64×64 (pivot 32,56).
**Style:** xianxia creatures in the MONSTERS_A/B look, held to the owner's bar for creature
art: the black silhouette must say what the creature is, believable anatomy and weight
(the ape and the horse above all), readable eyes or face, a windup that clearly differs
from the idle, anticipation and follow-through. Glow only where the creature has it (eyes,
furnace fire, flame mane and tail, embers). No text, no Chinese characters.
**Lands and moods:** Mê Đồ Lâm (maze forest: deep greens, a crimson bloom, a white ape),
Thiên Công Phường (workshop quarter: wood, bronze, gold gears, verdigris, furnace fire),
Linh Xạ Nguyên (archery grassland: straw, painted target red and white, a red horse of fire).
**Poly budget:** under 4k triangles per creature (simple solids at sprite scale); no
textures, colour from Principled base colours that the kit snaps to the palette.
**Pivot:** the ground point under the creature. The two big elites (and the furnace)
stand on a footprint wider than the kit's ground band; they slide away from the camera per
facing (see "Per-facing slide" below).
**Animation:** one armature per creature, the six monster clips of the contract: `idle` 4,
`walk` 6, `windup` 4 (held telegraph), `attack` 4 (`events.attack.hit` = 1), `hit` 2,
`die` 6; four facings.
**Export:** kit `render_animated` sheets `<id>` and `<id>_di`, plus `.blend` files in
`art/blender/monsters_d/` (git-ignored, rebuilt by `build.py`).

### Active skills
1. blender-director: this brief, pipeline order, validation gate.
2. creature-artist: anatomy first (skeleton -> masses -> forms): a gorilla's sloping back
   and long arms, a horse's withers, croup, forearm/knee/cannon and gaskin/hock/cannon,
   a hound's barrel chest and tucked waist; movement planned in the rig.
3. blender-modeler: everything modelled from numbers (no hand-saved state), `COL_`, `SM_`,
   `MAT_`, `ARM_` names.
4. rigging: bone-parented hard parts, one skinned stem tube (Hoa Yêu), planar two-bone IK
   for every planted limb (`common.Limb`: knees forward, hocks and ape elbows back), feet,
   hooves and knuckles held flat.
5. animation: pose tables with anticipation (crouch before the rear, coil before the
   lunge), follow-through and lag (mane and tail fire, leaves, straw arms, hat), a real
   four-beat walk for the horse, stiff stepped motion for the clockwork hound.
6. pixel-art-style / stylized-style: features at least 1 px (eyes 0.04 m+), kit priority on
   eyes, teeth and gears, shape language (round furnace, triangular fangs and petals,
   blocky hound), limited palette per creature.
7. fantasy-worlds / genre-rpg: material honesty per land, dị chủng as a clearly different
   rarer look (a second colour and ramp set on the same materials).
8. qa-review: `fitcheck.py` before every render, kit QC after, 5× zoom crops of key frames
   next to the player (`zoom.py`), at least three look-fix rounds per creature (log below).

## Files

| File | What |
|---|---|
| `build.py` | venv entry point: one headless Blender per creature (2 at once), optional fitcheck, QC, contact sheets, overview |
| `scene.py` | inside Blender: build one creature, save `art/blender/monsters_d/<id>.blend`, render `<id>` and `<id>_di` |
| `bestiary_d.py` | the `BUILD` table (id -> name_vi, frame size, builder) |
| `common.py` | planar two-bone IK in absolute bone angles (`ik2`, `Limb`), `posed`, oriented ellipsoids, the clip writer |
| `hoa_yeu.py`, `bach_vien.py`, `co_quan_thu.py`, `lo_linh.py`, `thao_nhan.py`, `xich_diem_ma.py` | one creature each: model, rig, clips |
| `fitcheck.py` | copy of MONSTERS_A's frame check, aware of the per-facing slide; prints the lowest row per facing and clip |
| `zoom.py` | zoomed crops of any clip/facing/frames, optionally with the player at the same scale |

The helpers of `art/src/monsters_a/` (`rig.py` solids, materials, armature, attach, skin,
pose tables and clips; `quadrupeds.py` quadruped rig and gait) are imported from that
folder unchanged.

```
python art/src/monsters_d/build.py                       # all six (about 6 min, 2 Blenders)
python art/src/monsters_d/build.py --only lo_linh        # one (comma list allowed)
python art/src/monsters_d/build.py --fit                 # also print the fitcheck of each .blend
python art/src/monsters_d/build.py --no-render           # .blend files only
python art/src/monsters_d/zoom.py out.png bach_vien:windup:right xich_diem_ma:walk:left --scale 5 --player
```

Outputs: `client/assets/v2/monsters/<id>.png/.json`, `<id>_di.png/.json`;
`art/preview/monsters_d_<id>.png` (every clip × every facing, both looks, 3×);
`art/preview/monsters_d.png` (all six facing right, every clip, both looks, with the player).

## Per-facing slide (big footprints)

The kit QC holds the lowest drawn row of the standing clips within 5 px of the pivot. Seen
from 35°, a hoof 0.3 m in front of the origin already draws 8 px under it, so a horse, a
gorilla or a tripod built at a believable size cannot stand centred on the pivot in every
facing. Rather than squeezing their legs together (which is what made earlier creatures look
deformed), the armature object slides straight away from the camera for each facing
(`shift_down`, `shift_up`, `shift_side` custom properties, metres; a clip may override one:
`shift_down_windup` for the rearing horse). The limbs nearest the camera stand on the pivot
row and the far ones draw higher, as they should. Cost: when one of these creatures turns
from a side facing to face the camera, its sprite moves 2–5 px up; the game's position for it
is its near feet, not the middle of its footprint. Bạch Viên, Xích Diễm Mã and Thảo Nhân
also carry a flat contact shadow (`rig.shadow`, `kit_outline = 0`): it grounds them and keeps
the middle of the lowest rows on the pivot while a foot is in the air (the kit's feet-drift
rule), and lets the dummy hop.

| id | down | up | side |
|---|---|---|---|
| `bach_vien` | 0.09 | 0.09 | 0.11 |
| `lo_linh` | 0.04 | 0.04 | 0.04 |
| `xich_diem_ma` | 0.21 (windup 0.08) | 0.18 | 0.03 |

## The creatures

Each entry gives what the creature is, how it moves and the attack shape its animation
suggests (tiles are 16 px = 0.42 m), then the look-fix log: what was wrong at 4-5× zoom
before each change.

### Hoa Yêu (`hoa_yeu`, normal 48), Mê Đồ Lâm
A crimson seven-petal bloom on a thick thorny stem rising from a gnarled root crown on four
creeping root-feet, two broad leaves for arms. In the heart of the bloom a dark-red face:
two slanted glowing eyes over a wide maw ringed with white fangs; a green calyx and sepals
behind give the bloom a head's mass from the side. Idle sways in a wave up the stem; walk
creeps on the roots one at a time; **windup coils the stem back and flares the bloom wide
open**; attack is a whip lunge that snaps the petals shut on the hit frame; die wilts the
stem sideways and lays the bloom down. Dị chủng: violet bloom, teal stem and leaves, flame
eyes. **Attack shape: line ahead, ~1.5 tiles (lunging bite).**

- Round 1: too small for its frame; flat prism petals and lone pale spots read as noise;
  teeth and eyes did not read; the bloom was a red sliver from the side; the root bulb read
  as a flowerpot; die overflowed. -> thick spoon-shaped petals, spots removed, bigger fangs
  and maw, scale 1.2, softer lunge, die falls sideways.
- Round 2: the face was a yellow smear (eyes on a gold heart); top of the frame cut; the bloom
  still a blade from the side in two walk frames. -> heart turned dark red so the eyes glow
  against it, eyes above a separate fanged maw (a face), scale 1.1, petals cupped 50°,
  bloom pitch in the walk halved.
- Round 3: the bulb still read as a pot (tan, flat top); die touched the frame. -> a dark
  gnarled root crown with knobs where the roots leave, lighter roots, die droop reduced.
- Still weak: seen exactly side-on the bloom is a narrow cup, a few px wide; it is small next
  to the player (a normal monster, ~30 px tall).

### Bạch Viên (`bach_vien`, elite 64), Mê Đồ Lâm
A great white knuckle-walking ape: high shoulders and hump, back sloping to a low rump, long
massive arms down to the knuckles, the head slung forward. Grey face, chest, hands and feet;
long white eyebrows sweeping back and a white beard (the wise old ape), small gold eyes, a
scar across its right eye, a string of dark prayer beads with one jade bead. Idle breathes
and looks about; walk is a four-beat knuckle-walk (left hand, right foot, right hand, left
foot) with rolling shoulders; **windup rears up with both fists raised over its head and the
mouth open**; attack brings both fists down in a ground slam just in front (hit frame 1);
die sinks onto its haunches and slumps. A flat contact shadow under it. Dị chủng: charcoal
fur, red face and hands, flame eyes, gold beads. **Attack shape: circle in front of it,
radius ~1.5 tiles (the slam's shockwave); a near circle around itself is also fair.**

- Round 1: a stack of white balls: upright like a snowman, arms hidden in the body, head on
  top, no face from the side. -> new skeleton on gorilla lines: pelvis low and back, chest
  forward, hump, head slung forward under the hump line, arms reaching down ahead of the legs.
- Round 2: hunch reads, but it was smaller than the player and the face vanished in the
  fur. -> scale 1.45 with the per-facing slide (so the knuckles do not have to bunch under
  the chest), limbs on their own material so the kit draws inner lines where an arm crosses
  the body, a bigger grey face and muzzle.
- Round 3: the white fur flattened into one tone; the windup and the attack swing cut the
  top of the frame; walk failed the feet-drift rule. -> fur based one tone darker (so the
  light tone only lands on lit planes), lower overhead fists, a bent-arm swing frame, the
  contact shadow, die slump pulled back into the frame.
- Still weak: at 1× the white base still reads as a soft white mass, its face is a few
  pixels with one gold eye from the side (the dị chủng reads better); die is a slump onto the
  haunches rather than a full topple (a full fall runs out of the frame).

### Cơ Quan Thú (`co_quan_thu`, normal 48), Thiên Công Phường
A clockwork hound, sibling of Cơ Quan Nhân (same woods, bronze, gold gear and lantern
eyes, same dị chủng): two barrels of wooden staves bound with dark bronze hoops, a
tucked waist, a gold gear standing on its back that turns all the time, a wind-up key in its
rump, a wooden skull with a long bronze muzzle and teeth, lantern eyes in rims, bronze plate
ears, wooden legs on bronze ball joints, a two-joint bronze tail. Motion is stiff and stepped:
the head ticks between poses, the trot moves diagonal pairs with little knee bend; **windup
crouches on its haunches, head low, jaw wide, tail rigid, the gear racing**; attack leaps
and snaps (hit frame 1); die runs down, splays and the gear pops off its axle. Dị chủng:
iron, red fittings, violet eyes. **Attack shape: line ahead, ~2 tiles (leap and snap).**

- Round 1: read as a bull/boar: head a box, snout short, everything gold, eyes hidden behind
  the muzzle from the front, feet failing the ground band in the front facing. -> longer
  bronze muzzle, taller pointed ears, longer legs, a tucked waist between the barrels, eyes
  raised above the muzzle, legs and feet pulled in.
- Round 2: dog silhouette reads; still gold all over; the back gear a lumpy blob; die
  overflowed. -> ears, hoops, feet and tail to dark bronze; gear with 6 big teeth and a dark
  hub; head turned aside in the die.
- Round 3: the gear still caught metal speckles; it sat half inside the back. -> flat
  (non-metal) gold gear, raised on a taller mount.
- Still weak: it stays a golden creature like its sibling; the gear reads as a gear only at
  zoom; from the front it is a narrow column.

### Lò Linh (`lo_linh`, elite 64), Thiên Công Phường
A living alchemy furnace: a round bronze ding with a band of green patina and gold bosses,
two loop handles on the rim, a dark beast-mask on its front with two slanted glowing eyes,
a heavy brow and three bronze fangs; shoulder vents puffing white steam; three stubby
clawed beast-legs; a domed lid hinged at the back with a flame-bud finial; fire inside.
Idle simmers (flicker, lid rattle, puffs); walk is a rolling waddle, one leg at a time;
**windup throws the lid open and the fire rises above the rim**; attack lurches forward and
blasts a jet of fire from the open mouth (hit frame 1), then slams the lid; die: the lid
blows off, the fire dies and the pot tips over, the lid lying behind it. Dị chủng: black
iron with red bands and blue spirit fire. **Attack shape: cone ahead, ~45°, 2 tiles (the
blast); the windup's rising fire also suits a small circle around itself.**

- Round 1: all gold, the eye vents lost in the bronze, smoke puffs read as grey horns, legs
  hidden under the belly, the jet a flat bar cut by the frame. -> deep bronze base, a dark
  mask plate behind the eyes, fewer and bigger white steam puffs, the pot raised on longer
  angled legs, a shorter rounded jet.
- Round 2: face reads, but the pot was small next to the player, the die never visibly
  tipped in the side views and a back leg lifting made the up-facing walk jitter. -> scale
  1.5 with the per-facing slide, a diagonal tip in the die, lower leg lift.
- Round 3: the open lid, the fire and the jet cut the top and sides of the frame. -> scale
  1.42, lid opens 42-48°, smaller fire and jet, shorter finial.
- Still weak: the bronze reads gold-yellow (the gold ramp is the only bronze); in the side
  view the waddle is small.

### Thảo Nhân (`thao_nhan`, normal 48), Linh Xạ Nguyên
A straw archery dummy come alive: a straw bundle bound with rope, a frayed straw skirt, one
wooden pole-leg, a painted target (white and red rings) on its chest with arrows stuck in it,
another in its shoulder and one through its hat; straw arms on a crossbar with frayed
hands; a sackcloth face with glowing eyes and a stitched grin; a patched conical hat. It hops
on its pole (a flat contact shadow stays on the ground under it); **windup squats on its pole,
leans back and throws both arms up and wide**; attack springs forward and slaps both arms
down (hit frame 1); die: the hat flies off, the body slides down the pole and keels over.
Dị chủng: charred straw, violet target, dark red hat, violet eyes. **Attack shape: cone
ahead, ~90°, 1 tile (double arm slap).**

- Round 1: reads as a scarecrow with a target, but the hat hid the face from the 35° camera,
  the di hat came out pale blue-white, straw ridges were noisy and the die fell out of the
  frame. -> smaller hat raised and tipped back, dark red di hat, four ridges, smaller fall.
- Round 2: arms had been raising when they should droop (rotation sign) and the fall still
  touched the frame. -> arm helper rewritten in (raise, forward) terms, fall reduced again.
- Round 3: die still touched the bottom in two facings. -> the body squashes down the pole
  more and tips less.
- Still weak: thin from the side; the face is 3-4 px; it is the smallest of the six.

### Xích Diễm Mã (`xich_diem_ma`, elite 64), Linh Xạ Nguyên
A lean red-bronze horse with a mane, forelock and tail of fire, built on horse anatomy:
deep chest and sloping shoulder, withers above the croup, round rump and haunch, a long
arched neck, a wedge head (wide cheek, long face, dark muzzle, pointed ears, ember eyes);
forelegs with forearm, knee, cannon, fetlock, pastern and hoof; hind legs with the gaskin
angled back to the hock and a near-vertical cannon; dark socks and hooves, an ember puff at
each hoof as it lands, a flat contact shadow. Idle breathes with flickering fire; walk is a
real four-beat walk (left hind, left fore, right hind, right fore) with the head nodding at
each fore footfall; **windup rears onto the hind legs, forelegs tucked, mane flaring**;
attack drops into a charge, neck stretched, forelegs striking (hit frame 1); die buckles to
its knees and lies down as the fire dies. Dị chủng: black coat, gold hooves, blue spirit
fire. **Attack shape: line ahead, ~3 tiles (the charge; the game should move it along).**

- Round 1: the horse read at once (side view); too big: head, tail and the rear cut by the
  frame; the near hooves sank 6-10 px below the pivot facing the camera. -> scale 1.2, the
  per-facing slide (0.23 m), a shallower rear.
- Round 2: in the front view a thin stick; the rear and the charge still clipped; rearing
  left only the hind hooves on the ground, so the slide made it float. -> wider barrel,
  chest, rump and leg track, a clip override of the slide for the windup, a windup that
  starts with the forelegs already lifting.
- Round 3: kit QC: head and tail of the charge and the die touching the sides, the up-facing
  rear touching the top, and the walk failing the feet-drift rule (one hoof in the air moves
  the middle of the lowest rows). -> scale 1.15, a contact shadow on its own bone (drawn in
  during the rear), shorter neck stretch and a lower tail in the charge and the die.
- Still weak: from the front it is narrow (a horse is); the head is small at 1×; the lying
  pose of the die is stiff.
