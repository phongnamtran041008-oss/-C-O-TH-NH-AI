# ICONS batch: manuals, pills and bottles, spirit herbs, gear, misc

Five 32x32 icon atlases for "Toán tu tiên", every icon a real Blender model (bmesh primitives,
bevels, lathes, extrusions; one root empty `SM_<id>` with one mesh per material) rendered and
packed only through the kit (`kit.render_icons`). Output goes to `client/assets/v2/icons/`:

| Atlas | Icons | Source module |
|---|---|---|
| `cong_phap` | 24 manuals (8 grades x book / scroll / slips-or-tome) | `books.py` |
| `dan_duoc` | 16 (8 pills on dishes + 8 containers) | `medicine.py` |
| `linh_thao` | 12 spirit herbs | `herbs.py` |
| `trang_bi` | 24 gear (6 slots x tiers 1, 3, 5, 7) | `gear.py` |
| `misc` | 10 (stones, egg, talisman, chests, key, token, breakthrough pill) | `misc.py` |

## Production brief (blender-director)

* **Type:** hero-ish props, one object per icon. **Target:** game, 32x32 pixel icons (26 px drawn).
* **Style:** pixel-art-style + stylized-style, chibi-chunky silhouettes, three-tone cel look done by
  the kit; xianxia fantasy-worlds language (jade, bronze, gold, clouds, yin-yang, flames, ice
  wings, galaxies). **No Chinese characters anywhere**: cover emblems, seals and "writing" are
  abstract strokes (dash rows, rings, crossed bars, flames, snowflakes, gems).
* **Camera/pose:** kit icon camera, upright items at `angle=0`, scrolls/keys diagonal.
* **Poly budget:** 100-1500 tris per icon (see `tris` custom property on each root).
* **Textures:** none; flat Principled materials (base colour, metallic, emission) that the kit
  quantises to `art/palette.json`. Materials are shared by name (`MAT_<name>`, defined once in
  `lib.py`, with the kit properties `kit_ramp`, `kit_glow`, `kit_priority`).
* **Grade language (same as the weapons):** 1 crude and earthy (clay, cloth, rough wood) / 2 plain
  iron-blue / 3 jade green + bronze / 4 gold trim + teal gem / 5 spirit cyan-violet glow /
  6 flame / 7 ice with small wings / 8 cosmic purple with stars and gold. Low grades are dull
  and carry no emission; glow grades use emission only on the parts that should glow, with solid
  non-glowing bodies underneath so the form stays readable.
* **Pipeline phases:** blockout (primitives) -> silhouette check at 26 px -> secondary forms
  (trims, gems, emblems) -> materials (ramp forcing where the palette needs it) -> kit render ->
  look-and-fix rounds on the contact sheets.
* **Skills used:** blender-director, prop-artist, hard-surface (bevels, panel logic on gear and
  chests), pixel-art-style (feature >= 2 px, no 1 px gaps: the kit removes single-pixel holes,
  so finger gaps and slat gaps are explicit dark lines or >= 2 px wide), materials (ramp
  mapping, emission), stylized-style (shape language, exaggeration), fantasy-worlds, qa-review.

### Modelling notes learned

* Objects are modelled 0.3-0.6 m big; the kit fits each icon to 26 px, so 0.02 m = about 1 px.
  Gaps and details narrower than ~0.04 m disappear (speckle clean-up); lines that must stay get a
  material with `kit_priority` (`ink`, `teal`, `star`, ...).
* The paper colour has no ramp of its own: parchment = the `gold` ramp (pale highlight), rolls and
  covers = `wood`.  `purple` must not be emissive for covers (it washed out to white).
* Flat plants/open books are tilted back 30-35 degrees inside the model so the 35 degree
  camera sees them face-on.

## Grade words and naming scheme (cong_phap, dan_duoc)

Grade word by grade: 1 Phàm, 2 Hoàng, 3 Huyền, 4 Địa, 5 Linh, 6 Bảo, 7 Tiên, 8 Thiên.
`name_vi` = grade word + form word: **Thư** (`sach_<g>`, closed book), **Quyển** (`cuon_<g>`,
scroll), **Giản** (`gian_<g>`, slips; grades 1-2 bamboo, 3-4 jade, 5 glowing spirit jade,
6-8 floating open tome with swirling qi in flame / ice / cosmic). Pills `dan_<g>` = "<grade> Đan",
containers `binh_<g>` = "<grade> Bình". Gear = slot word + tier word (Vải Thô, Bích Lụa,
Linh Quang, Băng Dực). Herb and misc names are listed below.

## Build

```
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/icons/build.py                  # everything
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/icons/build.py --only misc,linh_thao
"/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/icons/build.py --only trang_bi --dev ao_1,gang_3 --scale 8
```

`--only` rewrites just the named atlases (and their `.blend` and contact sheet); other atlases
in the folder, ours or other batches', are never touched. `--dev` renders a few ids into
`art/render/icons_dev/` (git-ignored) for looking. A full build takes about 30 s. Rebuilding gives
byte-identical PNGs. QC (`kit.qc.check_file`) runs on each atlas; contact sheets (3x, dark
background, one row per grade) are `art/preview/icons_<atlas>.png`. The `.blend` files are
`art/blender/icons/<atlas>.blend`.

Files: `lib.py` (materials, geometry kit `W`, leaf / swirl helpers), `books.py`, `medicine.py`,
`herbs.py`, `gear.py`, `misc.py`, `scene.py` (inside Blender), `build.py` (venv python).

## Look-and-fix log (against the reference sheets)

Round 1 (first full contact sheets):
* paper and scroll rolls were one saturated yellow -> sheets stay on the pale `gold` ramp, rolls
  moved to `wood` tan; cover purple washed out to white (it was marked glowing) -> solid `purple`.
* books were flat tiles with no spine -> spun 28 degrees, thicker (0.10 m), spine band, cord loops
  on the low grades.
* bamboo/jade slips fused into a door -> explicit 0.018 m gaps between slats.
* open floating tomes were a dark blob (modelled upright, then tilted the wrong way) -> tilted
  back 35 degrees, cream pages; swirling qi now two arcs behind the book instead of a ring in
  front of it.
* pills/vials on grades 5-7 were entirely glowing, so the body vanished -> solid bodies, glow
  only on swirls, flames, gems and thin auras (as in the reference).
Round 2:
* chests: bands and body had the same colour -> dark wood with dark-gold bands; open chest lid
  now swings up behind (hinge at the back edge), gold heap glows.
* boots read as one block -> two boots side by side, toes toward the camera, 3/4 spin.
* gloves: fingers fused because the kit removes 1 px gaps -> `ink` (priority) lines between the
  fingers, wider palm, separate thumb.
* ice lotus / thunder vine / flame flower were white blobs -> solid petals with glow only in the
  core, zig-zag bolt made from fat segments, six separated flame petals.
* ginseng too thin -> fatter root, ringed, bigger leaves; spirit stone 3 was white -> body glow
  strength lowered so the cyan edge colour shows.
Round 3 (final): book size inside the qi swirl (1.5x), straw hat to tan, ring bezels, rechecked
all five sheets; QC passes, two full rebuilds are byte-identical.

Still weak: the floating tomes (6-8) are small inside their qi ring; `ao` tier 1 reads as a plain
shirt; the glove is a back-of-hand view only; misc sheet has gaps because it is grouped by
grade (1, 2, 3, 5, 6).

## id / name table

### cong_phap (24)

| id | name_vi | grade |
|---|---|---|
| `sach_1` | Phàm Thư | 1 |
| `cuon_1` | Phàm Quyển | 1 |
| `gian_1` | Phàm Giản | 1 |
| `sach_2` | Hoàng Thư | 2 |
| `cuon_2` | Hoàng Quyển | 2 |
| `gian_2` | Hoàng Giản | 2 |
| `sach_3` | Huyền Thư | 3 |
| `cuon_3` | Huyền Quyển | 3 |
| `gian_3` | Huyền Giản | 3 |
| `sach_4` | Địa Thư | 4 |
| `cuon_4` | Địa Quyển | 4 |
| `gian_4` | Địa Giản | 4 |
| `sach_5` | Linh Thư | 5 |
| `cuon_5` | Linh Quyển | 5 |
| `gian_5` | Linh Giản | 5 |
| `sach_6` | Bảo Thư | 6 |
| `cuon_6` | Bảo Quyển | 6 |
| `gian_6` | Bảo Giản | 6 |
| `sach_7` | Tiên Thư | 7 |
| `cuon_7` | Tiên Quyển | 7 |
| `gian_7` | Tiên Giản | 7 |
| `sach_8` | Thiên Thư | 8 |
| `cuon_8` | Thiên Quyển | 8 |
| `gian_8` | Thiên Giản | 8 |

### dan_duoc (16)

| id | name_vi | grade |
|---|---|---|
| `dan_1` | Phàm Đan | 1 |
| `binh_1` | Phàm Bình | 1 |
| `dan_2` | Hoàng Đan | 2 |
| `binh_2` | Hoàng Bình | 2 |
| `dan_3` | Huyền Đan | 3 |
| `binh_3` | Huyền Bình | 3 |
| `dan_4` | Địa Đan | 4 |
| `binh_4` | Địa Bình | 4 |
| `dan_5` | Linh Đan | 5 |
| `binh_5` | Linh Bình | 5 |
| `dan_6` | Bảo Đan | 6 |
| `binh_6` | Bảo Bình | 6 |
| `dan_7` | Tiên Đan | 7 |
| `binh_7` | Tiên Bình | 7 |
| `dan_8` | Thiên Đan | 8 |
| `binh_8` | Thiên Bình | 8 |

### linh_thao (12)

| id | name_vi | grade |
|---|---|---|
| `co_linh` | Cỏ Linh | 1 |
| `nam_do` | Nấm Đỏ | 2 |
| `nhan_sam` | Nhân Sâm | 3 |
| `qua_do` | Quả Chu Hồng | 3 |
| `chuong_xanh` | Hoa Chuông Lam | 4 |
| `sen_ngoc` | Sen Ngọc | 4 |
| `day_loi` | Dây Lôi Đằng | 5 |
| `hoa_diem` | Hỏa Diệm Hoa | 6 |
| `lan_nguyet` | Nguyệt Lan | 7 |
| `sen_bang` | Băng Liên | 7 |
| `qua_tinh` | Quả Tinh Tú | 8 |
| `la_long` | Long Lân Diệp | 8 |

### trang_bi (24)

| id | name_vi | grade |
|---|---|---|
| `ao_1` | Áo Vải Thô | 1 |
| `mu_1` | Mũ Vải Thô | 1 |
| `giay_1` | Giày Vải Thô | 1 |
| `gang_1` | Găng Vải Thô | 1 |
| `nhan_1` | Nhẫn Vải Thô | 1 |
| `day_chuyen_1` | Dây Chuyền Vải Thô | 1 |
| `ao_3` | Áo Bích Lụa | 3 |
| `mu_3` | Mũ Bích Lụa | 3 |
| `giay_3` | Giày Bích Lụa | 3 |
| `gang_3` | Găng Bích Lụa | 3 |
| `nhan_3` | Nhẫn Bích Lụa | 3 |
| `day_chuyen_3` | Dây Chuyền Bích Lụa | 3 |
| `ao_5` | Áo Linh Quang | 5 |
| `mu_5` | Mũ Linh Quang | 5 |
| `giay_5` | Giày Linh Quang | 5 |
| `gang_5` | Găng Linh Quang | 5 |
| `nhan_5` | Nhẫn Linh Quang | 5 |
| `day_chuyen_5` | Dây Chuyền Linh Quang | 5 |
| `ao_7` | Áo Băng Dực | 7 |
| `mu_7` | Mũ Băng Dực | 7 |
| `giay_7` | Giày Băng Dực | 7 |
| `gang_7` | Găng Băng Dực | 7 |
| `nhan_7` | Nhẫn Băng Dực | 7 |
| `day_chuyen_7` | Dây Chuyền Băng Dực | 7 |

### misc (10)

| id | name_vi | grade |
|---|---|---|
| `linh_thach_1` | Hạ Phẩm Linh Thạch | 1 |
| `linh_thach_2` | Trung Phẩm Linh Thạch | 3 |
| `linh_thach_3` | Thượng Phẩm Linh Thạch | 5 |
| `trung_linh_thu` | Trứng Linh Thú | 3 |
| `phong_an_phu` | Phong Ấn Phù | 3 |
| `ruong_dong` | Rương Đồng | 3 |
| `ruong_mo` | Rương Đồng Mở | 3 |
| `chia_khoa` | Chìa Khóa | 2 |
| `ngu_kiem_lenh` | Ngự Kiếm Lệnh | 5 |
| `pha_canh_dan` | Phá Cảnh Đan | 6 |
