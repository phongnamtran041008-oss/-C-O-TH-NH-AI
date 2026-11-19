# CHARS batch: the player cultivator (Đạo Sĩ), v2 — one body, one rig, eight realm looks

The 36 px chibi (v1) was rejected by the author. v2 follows the approved look-dev
(`lookdev/`): a slender young man ~3.4 heads tall, 96x96 frames, camera 15° above the
horizon, empty hands (weapons are separate layer sheets).

## Production brief (blender-director)

**Type:** player character, 8 swappable outfit sets on one body and rig (gear, not realm rewards)
**Target:** pygame, sprites through `tools/blender/kit` 1.4 — frame 96x96, pivot (48,82),
48 px per metre, elevation 15°, head bone snapped to the pixel grid, 3-tone cel, palette
**Style:** stylised low-poly — planar tapered forms (6-8 sided limbs, wedge torso, box fists,
octagonal head with a flat face), face parts sized in whole pixels (1 px = 1/48 m) with
`kit_priority`, layered clothes with their own materials so the kit draws inner lines
**Budget:** ~3-9 k tris per look (unsubdivided, flat shaded)
**Pivot:** ground point between the feet; faces -Y; 1 unit = 1 m (figure 1.0 m + topknot)
**Animation:** 10 clips, every bone keyed on every frame, legs baked from two-bone IK

Active skills: character-artist / chibi-style (proportion rules, separate garments), stylized-
style + pixel-art-style (planes, palette ramps, whole-pixel features), hair-groom (lock-based
hair), rigging (ARM_dao_si, sockets), animation (pose-to-pose, anticipation, follow-through),
cloth-sim (hand-keyed lag of hair, ribbons, sleeves, cape, hem), qa-review (gates below).

## Files

| file | runs in | what |
|---|---|---|
| `build.py` | venv | the one command: builds all scenes, renders + packs through the kit, QC, previews |
| `v2/v2_main.py` | Blender | builds one scene (`--look <id>` or `rig_base`), saves it, renders it |
| `v2/v2_rig.py` | Blender | v2 bone table (look-dev body + wing bones), frame / pivot / ppm / elevation |
| `v2/v2_looks.py` | Blender | the eight looks, armour, ribbons, ponytail, crown, edge lights, wings |
| `v2/v2_clips.py` | Blender | the ten clips |
| `lookdev/` | Blender + venv | the approved look-dev (body, face, hair, garment pieces reused by v2) |
| `rig.py`, `clips.py`, `geo.py` | Blender | pose solver + sockets + skinning, follow-through pass, mesh helpers |

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/build.py                 # everything
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/build.py --only dao_si_ket_dan
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/build.py --gate          # idle-only self-review gate
```

Outputs: `art/blender/chars/{rig_base,dao_si_*}.blend`; `client/assets/v2/chars/dao_si_*.png/.json`
(204 frames, 10 clips x 4 facings, `events.hit` = 3 on slash / cast / shoot, `render.ground_clips` = die);
`art/preview/chars_overview.png` (per look: reference row beside idle down/right/up, walk right,
slash strike right/down, cast release, fly, meditate, all 4x); `art/preview/chars_<realm>.png` (kit contact sheet per look).

## Numbers for the aura / FX batches

All looks: frame 96x96, pivot (48,82) = ground point under the feet, 48 px/m, camera 15°.
Standing figure (idle, facing down): top of the topknot 50-51 px above the pivot, body ~31 px
wide; the head centre is ~39 px above the pivot. Wing extents (idle down, bounding box):

| look | extra | idle-down box (x0,y0..x1,y1) | width x height above pivot |
|---|---|---|---|
| luyen_khi / truc_co / ket_dan / nguyen_anh | — | ~(33,31..64,85) | ~31 x 51 |
| hoa_than | halo ring 0.58 m across behind the head, open coat | (27,31..70,85) | 43 x 51 |
| luyen_hu | flame wings | (18,23..76,85) | 58 x 59 |
| hop_the | ice wings | (18,23..76,85) | 58 x 59 |
| dai_thua | cosmic wings | (18,23..76,85) | 58 x 59 |

On the slash hit frame the wings spread to ~71-73 px wide (x 10..83). Auras are not baked in.

## Scene layout

* `COL_dao_si`: `ARM_dao_si` (actions `idle walk slash cast shoot hit die meditate fly dodge`,
  frame 1 on; loops carry a closing key) and the sockets.
* `COL_body` (rig_base) or `COL_outfit_<id>`: meshes `SM_*` bound by Armature modifiers.
* Bones: root > mount, qi, hips > spine > chest > neck > head (> hair_01..03, ribbon_01/02 L/R,
  halo with a camera-facing driver); chest > upper_arm/forearm/hand L/R (+ sleeve), cape_01..03,
  wing arm wing_01 (upper arm) > wing_02 (forearm) > wing_03 (hand), L/R; hips > thigh/shin/foot L/R, hem_F/B/L/R. `.L` = the character's own left.

## Weapon layers: loading the rig and attaching a weapon

The sheets are rendered with **empty hands**. The right fist keeps a grip and a weapon
direction in every clip (`blade` aims: low-forward in idle, cocked over the shoulder in the
slash wind-up, fully extended forward on the hit frame, down-back in cast). Sockets:
`SOCKET_weapon_r` (right grip: a weapon modelled with its grip at the origin, length along +Z,
flat side -Y, parented with an identity local transform), `SOCKET_weapon_l` (bow hand; +Z is
up when the left arm is extended in `shoot`), `SOCKET_back`, `SOCKET_mount` (ground point under
the feet, raised by the `mount` bone in `fly`: put the flying sword there).

```python
# inside Blender, started with kit.launcher.run_blender(script, "<batch>",
#                                                     blend="art/blender/chars/rig_base.blend")
import bpy
import kit.api as kit
rig = bpy.data.objects["ARM_dao_si"]
sword = make_my_sword()                       # grip at origin, blade along +Z, flat side -Y
sword.parent = bpy.data.objects["SOCKET_weapon_r"]
sword.matrix_parent_inverse.identity()
sword.matrix_basis.identity()
kit.render_layer(sword, rig, "client/assets/v2/chars/dao_si_truc_co.json",
                 "client/assets/v2/weapons", "kiem_thep", name_vi="Kiếm Thép")
```

`render_layer` reads frame, pivot, ppm, elevation, snap and ground clips from the character
json, so one weapon layer fits all eight looks. In `fly` the right hand makes a sword seal and
in `shoot` it draws a bowstring: a melee layer may hide itself there (`on_frame` hook).

## Self-review gates (what was looked at, what was fixed)

1. Look-dev rounds 1-4 (see the batch report): proportions, face, hair, Hóa Thần, shading.
2. Gate A (all eight, idle only, beside their reference rows): colours too pale (materials
   were written as sRGB values into linear inputs, and the light band was too wide) — v2
   colours are now written as sRGB and converted, and the light band narrowed to the
   upper-left planes; wings were narrow vertical fans — rebuilt as a wide V of 5-6 primaries +
   4-5 coverts with gaps, thin leading edges and small glowing tips; ice wings too dark.
3. Wing round (manager review: "fans of sticks"): wings rebuilt as a real wing - a three-bone
   arm (up-out, out-up, out-down; wrist above head height) with overlapping shingled feathers
   (7 primaries, 6 secondaries, 3 tertials, two covert rows), tone separation instead of gaps
   (A/B alternating, lighter coverts, dark roots, bright or glowing tips, glowing / gold leading
   edge). Hóa Thần: coat shortened to the knee and split up the back, teal sash, crown strands.
   Luyện Hư / Hợp Thể mid-tones lifted. rig_base rebuilt (it gained wing_03.L/R).
4. Full render: the coat exploded to 196 m in the die fall (solidify "even thickness" on folded
   cloth) — turned off; cape flare and hit recoil reduced so the up-facing sprite stays on the
   pivot. Kit QC: 0 problems.

## Village NPCs (`npcs/`) on the v2 body

Eight villagers on the player's body and rig (same bones, same 96x96 frame, pivot (48,82),
48 px/m, 15 degree camera, head snap): `shopkeeper alchemist smith librarian guide fisher
truc_lao villager` (the keys of `client/engine/sprites.py`). Each is an outfit plus a
torso-mesh variation (women narrower in the shoulders and chest, the smith broader, the
shopkeeper plump) applied to torso pieces only, so the skinning still follows the shared
bones. Clips per NPC (its own actions in its own scene): `idle` 4 with a gesture (nod, weight
shift, sway, head tilt, beard stroke, rocking), `walk` 8 (the old take shorter steps), `talk` 4
(an open hand rising and falling, head nods). Kit kind `npc` (QC asks only for these clips).

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/npcs/build_npcs.py [--only id ...] [--gate]

Outputs: `client/assets/v2/npcs/<id>.png/.json`, `art/blender/chars/npc_<id>.blend`,
`art/preview/npcs.png` (4x: idle down/right/up/left, walk mid-stride, talk; the Luyện Khí
player beside the first row for scale).
