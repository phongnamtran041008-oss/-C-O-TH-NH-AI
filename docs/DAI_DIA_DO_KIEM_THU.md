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
