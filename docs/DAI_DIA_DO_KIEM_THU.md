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
