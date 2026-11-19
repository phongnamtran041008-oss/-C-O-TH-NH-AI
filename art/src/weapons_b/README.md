# WEAPONS_B - staff, bow, fan, gourd (4 types x 8 grades = 32 weapons)

## Production brief (blender-director)

**Type:** hero props (hand-held weapons) - `prop-artist` + `hard-surface` (fittings, bevel-free chunky forms)
**Target:** game, pixel-art icons 32x32 (about 26 px, diagonal) and, later, weapon-in-hand layers
**Style:** `stylized-style` / `pixel-art-style` / `fantasy-worlds` (xianxia): chibi-thick, big readable shapes
**Poly budget:** 400 - 2700 tris per weapon (they are rendered at 6x then scaled down; silhouette matters, not density)
**Texture budget:** none - plain Principled materials (base colour, metal, roughness, emission); 2-6 materials each
**Export:** one `.blend` per weapon, `art/blender/weapons/<id>.blend`, root mesh object `SM_<id>`
**Pivot / convention:** grip at the origin, length along +Z, broad side facing -Y, 1 unit = 1 m
(character 1.0 m: staff about 1.1, bow about 0.9-1.0, open fan 0.45 wide, gourd 0.44 tall incl. stopper)
**Animation:** none

### Grade themes (shared by every weapon batch)

| Grade | Realm | Theme | Prefix |
|---|---|---|---|
| 1 | Luyen Khi | crude wood / dried gourd / paper, hemp, no shine | Moc |
| 2 | Truc Co | plain iron fittings, red cord | Thiet |
| 3 | Ket Dan | jade green, bronze fittings | Bich Ngoc |
| 4 | Nguyen Anh | gold trim, teal gem, faint glow | Kim Lam |
| 5 | Hoa Than | spirit light, cyan-violet glow, gold (emissive) | Linh Quang |
| 6 | Luyen Hu | flame, blackened gold (emissive); fan = phoenix, gourd holds fire | Hoa Diem |
| 7 | Hop The | ice crystal blue, small wings, frost, mist (emissive) | Bang Duc |
| 8 | Dai Thua | cosmic purple, star specks, gold core (emissive) | Tinh Khong |

### Shape progression per type (each grade changes the silhouette, not just the colour)

* **truong** 1 crooked forked branch -> 2 iron cap + ball -> 3 jade orb in three bronze claws -> 4 gold crescent + teal diamond ->
  5 glowing orb in gold ring with crystal crown -> 6 burning core with flames and black horns -> 7 long ice crystal with wing feathers ->
  8 cosmic sphere, gold core, two orbit rings, stars.
* **cung** 1 plain wood bow -> 2 iron tips, red grip cord -> 3 jade limbs, bronze fittings -> 4 gold thorn horns + teal gem ->
  5 crystal tips, glowing ring at grip -> 6 flames along the back, burning string -> 7 ice limbs with feather wings at the grip ->
  8 gold core ring, star specks, glow wings.
* **phien** 1 paper/bamboo -> 2 grey paper, iron ribs, red tassel -> 3 jade pleats, bronze rim -> 4 plum/gold, teal hub, gold disc ->
  5 glowing feather fan -> 6 phoenix feathers with a tall flame tail -> 7 ice pleats with wing feathers at the handle -> 8 star-field fan, gold rim.
* **ho_lo** 1 dried calabash -> 2 iron bands, red cord -> 3 slim jade bottle, bronze rings -> 4 gold bands, teal belly gem ->
  5 glowing body, light motes -> 6 black body, glowing belly, flames from the neck -> 7 ice body, wings, mist puffs -> 8 star body, gold core ring.

## Files

| File | What |
|---|---|
| `geom.py` | bmesh helpers (cylinders, spheres, tori, flat plates, feathers); one mesh per weapon, one slot per material |
| `weapons.py` | the 32 weapons: palettes + one function per type, shape branches per grade |
| `make_blends.py` | runs inside Blender: writes `art/blender/weapons/<id>.blend` |
| `quick_preview.py` | Workbench look-check only (modelling aid, not the final look) |
| `build.py` | the whole pipeline: blends -> kit render -> icon atlas + contact sheet |

## Rebuild

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_b/build.py            # everything
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_b/build.py --only cung_5
```
