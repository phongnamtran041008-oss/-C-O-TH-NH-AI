# WEAPONS_A (kiem, dao, thuong, chuy x 8 grades)

## Production brief

**Type:** hero props (hand weapons), 4 types x 8 grades = 32 models
**Target:** game icons (32x32 atlas, 26 px drawn) now; later parented to the character hand for layers
**Style:** stylized / chibi-exaggerated, pixel art from 3D (kit toon + master palette)
**Poly budget:** 250-1100 tris each (all flat-shaded, chunky bevels), 1-12 Principled materials
**Pivot:** grip at origin, length +Z, flat side faces -Y, 1 unit = 1 m (sword ~0.8, sabre ~0.8, spear ~1.6 with head, hammer ~0.9)
**Animation:** none (static)
**Export:** `art/blender/weapons/<id>.blend`, root empty `SM_<id>` (custom props `name_vi`, `grade`, `type`), one mesh per material `SM_<id>_<mat>`, materials `MAT_<key>`

Skills used: blender-director, hard-surface (bevelled solids, guards), prop-artist (scale, pivots),
pixel-art-style, materials, stylized-style, fantasy-worlds, asset-optimization, qa-review.

Grade themes (shared by all weapon batches): 1 crude wood/hemp, 2 plain iron + red cord, 3 jade + bronze,
4 ornate steel + gold + teal gem, 5 spirit cyan-violet + gold guard (emissive), 6 flame
(emissive, blackened gold), 7 ice + small wing guard (emissive), 8 cosmic purple + gold core + stars.
Shape changes per grade: blade profile (plain, leaf, wide, crystal jag, flame teeth, long), guard
(bar, bent bar, curl, crescent + gem, wings, claws, feathers, horns), pommel and tassels, head shapes
for spear and hammer.

## Files

* `models.py` - numbers-and-code models (runs in Blender). `W` = tiny geometry kit (box, cyl, sph, ico, poly extrude with bevel).
* `scene.py` - runs inside Blender: builds + saves each .blend, then `kit.render_icons`.
* `build.py` - entry point (venv python), then kit QC and the contact sheet.
* `quick_preview.py` - dev aid only (EEVEE look at the raw models); final art is kit only.

## Rebuild

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_a/build.py             # everything (~15 s)
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_a/build.py --only kiem_3,dao_5

(`--only` rebuilds those .blends and an atlas holding only those icons; run without it for the full atlas.)

Outputs: `art/blender/weapons/<id>.blend`, `client/assets/v2/icons/weapons_a.png|json`, `art/preview/weapons_a.png`
(types in columns, grades in rows, 3x).
