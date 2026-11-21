# Đại Địa Đồ: the whole world played (kiểm thử)

The six giant lands (320 x 240 tiles) and Lôi Kiếp Đài (120 x 90) walked by the Chỉ Đường arrow
alone, toured in pictures by a character at Luyện Khí tầng 9 with every land open, and measured.
2026-11-21, on this machine (Windows, Python 3.14, dummy video driver, other agents' suites running).
See also [CHI_DUONG.md](CHI_DUONG.md) (the arrow) and [DAI_DIA_DO.md](DAI_DIA_DO.md) (the lands).

| what | how to run it again |
|---|---|
| the walk of every land | `python -m client.tests.nav_walk [zone ...]` (about 40 s; a test: `test_nav_units.py::test_every_land_of_the_world_is_walked_by_the_arrow_and_home_again`) |
| the tour in pictures | `python -m client.tests.tour_world [dir] [zone ...]` (a real server; about 40 min) → `tools/reports/tour/` |
| the client numbers | `python -m client.tests.nav_perf [zone ...]` (a real server, one land at a time) |
| the server numbers | `python tools/bench_giant_map.py --zone all`, `--startup` (the synthetic land without `--zone`) |

## 1. Every place of every land, by the arrow alone

`client/tests/nav_walk.py` derives the lands from the maps (every map with `khu` or `poi` objects:
the six giant lands and Lôi Kiếp Đài) and, from the land's gate (`from_village`), walks to:

* the anchor of every khu (camps included);
* every `poi` but the gate itself; a poi standing in water (a lake's middle, a glide islet) is
  walked to its nearest shore that can be reached on foot (at most 10 tiles off; Hồ Nghiên Mực,
  Hồ Gương Cỏ, Hồ Lặng, Hồ Gương, Đầm Kiếm Rỉ: 4-6 tiles; the two glide islets of Vạn Tượng Trạch,
  Bãi Sen Ngọc and Đảo Lưu Ly: to their stone ledge);
* every weapon spot and beast world_plan.json places in the land;
* except what world_plan documents as needing Đạp Kiếm Lướt (`needs`) and a poi within 3 tiles
  of such a spot: Kiếm Trủng Sơn (Đỉnh Vạn Kiếm, Tổ Hỏa Tước, kiem_2, hoa_tuoc), Lưu Vân Cốc
  (Thác Mây · hồ đầu nguồn, Kim Sí Điểu, dao_2, kim_si_dieu);

then H from the deepest anchor (band 3, the longest way): through the land's gate, then across
Trúc Lâm Thôn from the land's arrival spawn to the gate of the Động Phủ - each leg by the arrow.

The walker holds the eight-direction keys a player would for each reading of the arrow, a tenth of
a second at a time, less when the aim is nearer (a player lets go on the spot). It fails a walk
that gets stuck (4 s without getting nearer by the field), whose arrow ever points through a solid
(the movement collider, every 2 px), whose feet ever stand on water, or that walks more than 1.6
times the way.

**Result: 144 walks, none failed.** Ratio walked / way 0.73-1.21 (the 1.21: Chợ Thợ Hoang, the street
grid of Thiên Công Phường, where the eight directions zig-zag a diagonal street).

| land | goals | farthest from the gate (walking time) | H home from (land + village) | the hard case |
|---|---|---|---|---|
| Kiếm Trủng Sơn | 21 | Bãi Kiếm Gãy 66 s | Đỉnh Vạn Kiếm 64 + 8 s | - |
| Lưu Vân Cốc | 17 | Thác Mây Đầu Nguồn 69 s | Thác Mây 70 + 10 s | the river's bridges |
| Mê Đồ Lâm | 19 | Cửu Vĩ Hồ 87 s, Thung Cực Tiểu 83 s, Tâm Mê Cung 80 s | Thung Cực Tiểu 83 + 8 s | the hedge maze `mdl_me_cung`: walked to its heart with ratio 1.00 |
| Vạn Tượng Trạch | 19 | Đảo Lưu Ly (shore) 84 s, Miếu Chìm 83 s | Miếu Chìm 84 + 8 s | the boardwalks: never a foot on water |
| Thiên Công Phường | 25 | Lò Lớn · Tiểu Long 78 s | Phố Đổ Nát 73 + 9 s | the street grid (ratio up to 1.21) |
| Linh Xạ Nguyên | 22 | Hồ Lặng (shore) 82 s | Đài Vấn Tâm 73 + 6 s | - |
| Lôi Kiếp Đài | 7 | Đài Lôi Linh Đông 17 s | Đài Lôi Linh Đông 18 + 11 s | - |

The search (grid and field) of a giant land took 150-290 ms spread over frames; one reading of the
way 0.05-0.18 ms.

### What the walk found and what was fixed

* **The arrow pointed through a corner** (4 walks in the first run: on the way home in Kiếm Trủng
  Sơn, to Lò Rèn Ba Miệng in Thiên Công Phường, to Đài Lôi Linh Tây on Lôi Kiếp Đài, to Hồ Lặng in
  Linh Xạ Nguyên). When the feet stand a few pixels beside the line of cells (after a diagonal
  step), no straight line to any cell ahead is clear, and the arrow fell back to the next cell: a
  line that grazes the corner of a prop. Fixed in `client/engine/navigator.py` (`Leg.read`): the
  arrow then points sideways onto the line of cells first (the foot of the perpendicular from the
  feet to the line from their cell to the next, never backward), unless that is within 1.5 px, and
  the next cell after that. The walkers (`nav_walk`, the flow tests' `follow_arrow`) tap a key when
  the aim is within the keys' 2 px dead zone, as a player nudges.

## 2. Arrival spawns in the gate camp

A player walking in from the village now sees the camp's banner first ("<camp> · An Toàn, nơi an
toàn"), then the khu beyond it. With B1's `camp(..., to_edge=...)` the gate camp's khu reaches the
map's edge at the gate:

| land | change | what moved |
|---|---|---|
| Vạn Tượng Trạch | `to_edge="e"` | the camp's khu rectangle: x 292-310 → 292-319 (nothing else) |
| Thiên Công Phường | `to_edge="e"` | the camp's khu rectangle: x 290-310 → 290-319 (nothing else) |
| Linh Xạ Nguyên | `to_edge="w"` | the camp's khu rectangle: x 8-28 → 0-28 (nothing else) |
| Mê Đồ Lâm | `to_edge="w"` | the camp's khu rectangle: x 48-64 → 0-64. The camp lies 44 tiles inside the gate, so its clearance (10 tiles) now covers the gate road: the three monster areas of the first quests moved out of it - Mực Con (ink_slime) from (15-33, 111-125) to (76-94, 111-125), just east of the camp on the road to Ngã Bảy, and from (15-33, 131-142) to (34-52, 138-149); Lân Hỏa Yêu (tone_wisp) from (15-33, 94-108) to (15-33, 86-100). The khu's anchor moved from Ngã Ba Đầu Tiên (30, 119), now inside the camp, to Hang Mặc Hồ (24, 149), and its description says where the three now are. The automatic areas of Bìa Rừng lost the cells the clearance took: Bìa Rừng has 2 Hoa Yêu and 4 Tri Chu Tinh instead of 4 and 5 (the land 157 monsters instead of 160; a denser fill breaks the density rule of check_maps) |

`client/tests/test_nav_units.py::test_each_land_s_arrival_spawns_lie_in_its_gate_camp` keeps it so,
and checks that no khu's anchor lies inside a camp (arriving there would show the camp's banner).

## 3. The tour in pictures (`tools/reports/tour/`)

A character "Du Lãm" at Luyện Khí tầng 9, every node of Đạo Thụ passed (every land open), on a real
server: per land the gate camp on arrival, the minimap crop, "Vùng này", a picture at every khu
banner on the way (the passes), the anchor of the nearest khu of each band (one screenful each), a
monster of that band under the mouse, the minimap deep inside, "Vùng này" again; once the picker
with everything open and "Thiên hạ". The three bands of every land were reached by the arrow in the
real game (none stalled); Lôi Kiếp Đài: its six named places, the boss terrace included.
`116`-`122`: "Vùng này" of every land drawn again after the label fixes below (offline, the player
at the gate).

What a player sees, judged:

* **Good**: every land greets the player with its camp's banner ("<camp> · An Toàn, nơi an toàn")
  (`003`, `022`, `039`, `053`, `071`, `091`); the arrow, the plate and the khu banners read well;
  band 2 and 3 monsters carry their pips and the tooltip names the band ("Trung Vực · hợp Luyện Khí
  tầng 4-6", `014`, `031`, `062`, `069`); no camp with a monster in it; no monster in a wall or in
  water in the pictures; the maze of Mê Đồ Lâm on the minimap (`089`) and its heart reached (`088`);
  the picker with everything open reads in full, nothing cut (`001`); "Thiên hạ" (`002`).
* **Fixed (navigation UI)**: on "Vùng này" the label of the village gate sat on the gate's own mark
  and on the player's mark ("Trúc L■m Thôn", `024`, `041`), the gate camps' names hid under the khu
  labels of a band 1 khu ("Lều Cửa Thảo Nguyên", `024`; "Trại Cổng Phường" too) and under "Con ở
  đây" (`005`). `client/scenes/world_map.py`: the gate's label goes beside its mark; the camp's and
  the gate's labels take the place where the fewest pixels of other labels, the gates' marks, the
  named places' diamonds and the player's mark lie (the khu labels reserved at their real width,
  not 60 px); "Con ở đây" has more places to go (`116`-`122`).
* **Fixed (the walkers)**: in the first runs the tour stalled twice with the arrow a pixel or two
  off (beside a pine in Mê Đồ Lâm, the well of Trại Bến Đầm): the flow tests' walker held no key
  inside the keys' dead zone; it now taps toward the aim, as a player nudges.
* **Fixed (the map)**: the anchor of Bìa Rừng Đa Lối fell inside the stretched gate camp (`076`
  is the new anchor, Hang Mặc Hồ, with its Mặc Hồ).
* **Left as they are** (not navigation; the names are the pictures):
  * the walk from Mê Đồ Lâm's gate to Hang Mặc Hồ crosses the bottom edge of the stretched camp
    twice, so its banners go camp, Bìa Rừng, camp, Bìa Rừng; harmless, and a smaller camp
    rectangle would bring the arrival banner problem back;
  * the walkable "stone" ground of Kiếm Trủng Sơn's peak and Lưu Vân Cốc's plateau and the cobbles
    of Thiên Công Phường (`049`, `067`, `069`, `100`) look like the cliff walls around them: a
    player may take open stone for a wall (art; B1's lands and the art pipeline);
  * monsters near the top of the screen are drawn under the zone label and the player card, and
    the quest tracker covers name tags at the right (`044`, `105`, `113`: HUD layout of world.py);
  * a world notice in the chat ("Mắc Ảnh Động sẽ mở cửa...", `105`) is red text over the ground
    bottom left (chat);
  * the dot below drops at text sizes 6-9 (known, `engine/text.py`).

## 4. Numbers on the real world

Client: `nav_perf` (a real server, the character at tầng 9 with every land open, following the
arrow from the gate to the farthest khu of band 3 for 40 s, every frame timed without the driver's
sleep). Server: `bench_giant_map.py --zone all` (the shipped map run as its own zone, its real
monsters; 1, 10 and 40 players spread over it, walking, 200 ticks of 50 ms) and `--startup`.
"old" is the same zone's map before Đại Địa Đồ (commit 660f7ef, about 60 x 40 tiles), on the same
bench.

| land | file KB (old) | zip KB (old) | map load ms (old) | world frame walking avg / 95% / worst ms | ground surfaces MB (old) | server channel ms (old) | monsters (old) | tick 1p avg/worst ms (old) | tick 10p | tick 40p |
|---|---|---|---|---|---|---|---|---|---|---|
| Kiếm Trủng Sơn | 2038 (112) | 132 (6) | 55-59 (24) | 4.6 / 6.3 / 26.7 | 24 (9.6) | 70 (58) | 221 (42) | 0.26/0.65 (0.22/0.66) | 0.81/1.50 (0.61/1.90) | 2.11/5.03 (2.52/6.22) |
| Lưu Vân Cốc | 1906 (110) | 127 (6) | 47-57 (29) | 5.1 / 6.4 / 13.5 | 24 (9.4) | 60 (54) | 182 (18) | 0.23/0.57 (0.11/0.28) | 0.74/1.60 (0.45/1.38) | 1.90/4.61 (2.11/6.27) |
| Mê Đồ Lâm | 2288 (116) | 145 (5) | 65-66 (25) | 5.0 / 6.2 / 9.6 | 24 (9.4) | 61 (61) | 159 (32) | 0.18/0.52 (0.18/0.32) | 0.69/1.21 (0.55/1.44) | 1.70/3.61 (2.43/5.44) |
| Vạn Tượng Trạch | 1532 (102) | 101 (5) | 48-60 (25) | 5.0 / 6.4 / 11.0 | 24 (8.3) | 64 (56) | 124 (16) | 0.15/0.43 (0.11/0.35) | 0.58/1.48 (0.38/1.20) | 1.51/3.83 (2.00/6.01) |
| Thiên Công Phường | 1549 (120) | 97 (6) | 41-48 (25) | 4.9 / 6.2 / 11.8 | 24 (8.8) | 64 (57) | 164 (17) | 0.13/0.46 (0.11/0.39) | 0.64/1.22 (0.38/1.16) | 1.87/5.34 (2.42/7.77) |
| Linh Xạ Nguyên | 1848 (101) | 123 (5) | 47-54 (25) | 4.6 / 5.4 / 10.6 | 24 (9.0) | 65 (49) | 162 (15) | 0.20/0.48 (0.10/0.33) | 0.66/1.70 (0.35/0.86) | 1.58/3.32 (1.94/4.98) |
| Lôi Kiếp Đài | 326 (63) | 11 (3) | 9-12 (22) | 4.9 / 6.2 / 15.8 | 23.5 (4.7) | 57 (55) | 3 (3) | 0.04/0.08 (0.05/0.14) | 0.25/0.60 (0.33/0.99) | 1.64/4.65 (2.00/5.20) |

(The monsters column is the live count of a fresh channel on the server, which can differ by a
few from the sum of the map's `count` - 157 for Mê Đồ Lâm.)

* **The rest of the client, per giant land**: the world standing still 4.0-5.5 ms a frame; the first
  arrow to the farthest khu of band 3 0.34-0.66 s after choosing it (23-24 frames); the grid 7-12 ms
  and the field 106-115 ms spread over frames (no slice over 5.2 ms); one reading 0.05-0.07 ms;
  the overview 6-9 ms once; the minimap 0.17-0.23 ms a frame; the big map opens in 20-27 ms and
  draws in 3.6-4.7 ms (worst 6.3); the walk grid 303 KB, a field 1.2 MB, the overview 225 KB, the
  big map's picture 185 KB. The ground chunks are capped by the tilemap's cache: 24 MB at most
  (15-16 MB measured on Thiên Công Phường and Linh Xạ Nguyên, whose walks drew fewer chunks).
* **The server's start-up** with every map preloaded (`World.preload`, 8 zones): 0.36 s (import of
  the app 0.92 s before it), 6-78 ms a zone; the 11.4 MB of maps parsed; the process at 97 MB.
  Before Đại Địa Đồ the six lands parsed in 2-3 ms each: the giant ones take 37-57 ms each, about
  0.25 s more in all, once, at start-up.
* **The web build** packs `client/assets/maps` into its zip archive: the ten maps are 11.4 MB on disk
  and 748 KB compressed (deflate 9, as the archive does); before, 0.94 MB and 47 KB. So the maps add
  about 0.7 MB to what a browser downloads (measured on the files; no browser run).

**Worse than on the old small maps, plainly**: the map files are 13-20 times larger on disk (2 MB
instead of 0.1 MB a land; 0.7 MB more in the web download); loading a land takes 40-66 ms instead of
about 25 ms; the ground surfaces of a land are 24 MB instead of 8-10 MB (the tilemap cache's cap);
the client's working set is about 20-25 MB larger (95-101 MB against 74-83 MB on the bench); the
server parses a land in 37-57 ms instead of 2-3 ms; a land holds 4-10 times the monsters. The
server's tick is not worse: with one player it is 0.13-0.26 ms against 0.10-0.22 ms, and with 40
players spread over a giant land it is lower (1.5-2.1 ms against 1.9-2.5 ms: the players are farther
apart, so fewer see each other). The world frame while walking stays at 4.6-5.1 ms on average.

## 5. The rare slow frames

The navigation work had traced 36-38 ms walking frames to the hotbar and the ability row scaling
their icons with `pygame.transform.scale` every frame. Measured with the two rows timed inside every
walking frame (`nav_perf`, `hud_rows_ms`, `slow_frames`), on Kiếm Trủng Sơn, Thiên Công Phường and
Mê Đồ Lâm, 4 300-4 500 frames each, the rows drawn the old way (`NAV_PERF_OLD_ICONS=1`): **0.36-0.42 ms
a frame on average, 1.3-1.5 ms at worst, and no frame over 25 ms at all.** The icon scaling is not the
cause of the slow frames; it costs well under half a millisecond. With the scaled icons kept
(`world.py` `hud_icon`, below) the rows cost 0.31-0.32 ms; the one frame over 25 ms in all seven lands
(26.7 ms on Kiếm Trủng Sơn) spent 18 ms in the rows once - the first drawing of a picture loaded
lazily from disk (a sheet's first use), not the scaling. The 36-38 ms frames of the earlier profile
were most likely such first uses and the network poll, under the other agents' suites.

The cache stays (it is small, the same pixels - `client/tests/test_hud_icons.py` compares the
pictures - and saves the scaling of up to eight icons a frame), but it is not a fix of anything a
player would notice; dropping its commit is harmless.

## 6. Defects in other agents' areas

See the final report of this work; in short: Kiếm Trủng Sơn and Lưu Vân Cốc walked clean (no map
defect); their stone ground reads as wall (art); the HUD covers monsters at the top of the screen.
