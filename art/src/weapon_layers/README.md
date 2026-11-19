# WEAPON_LAYERS: the 64 weapons in the hand + the flying sword

## Production brief (blender-director)

**Type:** sprite layers. Each weapon model (`art/blender/weapons/<id>.blend`, WEAPONS_A / WEAPONS_B) is
parented to the player rig (`art/blender/chars/rig_base.blend`) and rendered through the ten character
clips in four facings. Plus three flying swords modelled here.
**Target:** pygame 480x270; 96x96 frames, pivot (48,82), 48 px/m, camera 15 degrees, head snap, exactly the grid of
`client/assets/v2/chars/dao_si_*.png` (so one layer fits all eight outfits)
**Style:** the kit's 3-tone toon on the master palette (`tools/blender/kit`); nothing is drawn by hand
**Export:** `client/assets/v2/weapons/<weapon_id>.png/.json` (67 sheets: 64 weapons + `phi_kiem_1..3`),
flying-sword scenes in `art/blender/weapon_layers/phi_kiem_*.blend`
**Pivot:** same as the character; **Animation:** the rig's own clips, weapon follows a socket
**Skills used:** blender-director, animation (anticipation / strike / recovery on the weapon), rigging
(sockets, carry empties, re-parenting between sockets), pixel-art-style, qa-review

## Files

| file | runs in | what |
|---|---|---|
| `build.py` | venv python | the one command (`--only id,id`, `--jobs N`, `--flying`, `--dev --clips a,b --dirs x,y` for quick looks into `art/render/weapon_layers/dev`) |
| `scene.py` | Blender | loads each weapon, carries, fit, hook, `kit.render_layer` |
| `offsets.py` | plain Python | the hand / back rule and every per-clip, per-frame carry (the thing you edit) |
| `flying.py` | Blender | builds and renders `phi_kiem_1..3` |
| `composite.py`, `preview.py` | venv python (pygame) | draw layers over character sheets; the two contact sheets |

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapon_layers/build.py --jobs 8     # everything (~25 min), QC, previews
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapon_layers/build.py --only kiem_3,cung_5
```

(Rendering needs the character sheets to exist; the preview only runs on a full build. Run
`python art/src/weapon_layers/preview.py` to redo the contact sheets alone.)

## Hand / back rule

| type | right fist (`SOCKET_weapon_r`) | left fist (`SOCKET_weapon_l`) | on the back (`SOCKET_back`) |
|---|---|---|---|
| `kiem` `dao` `chuy` | idle walk slash cast hit die dodge | | shoot fly meditate |
| `thuong` (spear) | idle walk slash cast hit die dodge | | shoot fly meditate |
| `truong` (staff) `phien` (fan) `ho_lo` (gourd) | idle walk **cast** slash hit die dodge | | shoot fly meditate |
| `cung` (bow) | | idle walk **shoot** hit die dodge | slash cast fly meditate |

`cast` is the attack of staff, fan and gourd (raised, then pointed forward on the strike frame);
`shoot` is the bow's. Nothing is ever empty: where the hand is busy with another job the weapon sits on the back
(the fan and gourd hang at the right hip/back so they stick out of the silhouette).

How the weapon is placed (all in `offsets.py`): a carry spec per clip frame, either an offset from the
socket (`rot`, `loc`) or an `aim` direction in the character's frame while following the hand's position
(used for cast / die / carry poses, where the hand's own twist is wrong). `die` ends with the weapon lying on
the ground beside the body. 
**Scale factors applied at attach time** (the model files are untouched; `offsets.TYPE_SCALE`): `kiem` 0.85,
`dao` 0.85, `chuy` 0.85, `phien` 1.3, every other type 1.0. A kiem comes out 0.6-0.75 m from fist to tip.
The flying sword is modelled 1.45x (it is drawn under the feet, banked 48 degrees about its length so the 15 degree
camera sees the blade instead of a 2 px line).

**Fit pass** (`scene.py: fit_plan`): before rendering, every frame of every clip is checked in all four facings;
if any weapon pixel would come within 2 px of the frame edge (2.5 px), the hand slides along the shaft (spear and staff
only, so the grip moves like a real thrust) or the weapon shrinks (down to 0.6), and the slide is smoothed along
the clip so it does not jitter. This is what keeps the long spear inside the frame.

## How the game draws it

Character first, then the layer, same frame index (`weapon.json` has the same `clips`, `frames`, `events` and
pivot as the character sheet; the body is a holdout, so the layer is transparent where the body hides the weapon):

```python
screen.blit(char_frame, pos)
screen.blit(weapon_frame, pos)          # layers/weapons/<weapon_id>, same clip/dir/index
```

**Flying sword (`phi_kiem_1..3`) is the opposite: draw it first, the character on top.** It exists for the
`fly` clip only (4 frames x 4 facings, same pivot), lies flat under the feet pointing the way the character
faces, and has no body holdout. Grade 1 spirit cyan (available from Truc Co), 2 gold flame, 3 cosmic violet.
Because `kit.render_animated` takes any clip subset (QC only demands all ten for kind `player`), the flying
sword sheets contain just `fly`; no hovering companion blade was needed for the other clips.

```python
screen.blit(sword_frame, pos); screen.blit(char_frame, pos)
```

## Look-fix log

Round 0 (obsolete, 64 px chibi rig, thrown away when the author rejected it): the pipeline itself was built and
looked at there (hand/back rules, fit pass, flying sword).

Rounds on the new 96 px rig, each judged on composites over the character sheets:

1. First composites (kiem_1, kiem_5 and the representatives of every type, 4 facings, all ten clips):
   * flying sword was a 10 px blob: the rig is in the render as a holdout (for the head snap) so the turntable turned
     the sword twice. Fixed by undoing the turn in the hook. It was then a 2 px line from the 15 degree camera:
     banked 48 degrees, enlarged 1.45x, trail made thin streaks (bright, no halo), blade body dark so the glow edge reads.
   * cast wind-up put the blade across the chest and the mouth (sword, staff, hammer, spear): the blade now leaves
     the hand up and outward past the right shoulder (aim (-0.55,-0.1,0.83)).
   * the fan was a few glints in the fist: scaled 1.3 and turned so its broad side faces 45 degrees out.
   * fit pass: the hand is allowed to slide only on spear / staff; swords and hammers shrink instead (a sliding
     hand put the guard far from the fist).
2. Second composites (`art/preview/weapon_layers*.png`): the staff strike pointed straight at the viewer like a rifle
   across the chest, the gourd likewise: staff and gourd strike aims raised to 0.72-0.75 (pointing forward-up). Rebuilt
   all 16 staffs and gourds.

Still weak: fans and gourds are small items, readable mostly by colour; on the three winged looks the back carry
sits among the wings; flying sword seen straight on (facing down / up) is a foreshortened shape under the feet.
