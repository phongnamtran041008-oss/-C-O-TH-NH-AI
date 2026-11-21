# Chỉ Đường and Thiên Địa Đồ (the way to the place that fits your tu vi)

The lands grow to 320 x 240 tiles; at the client's 2x zoom the screen shows about 15 x 8.5 of them.
Chỉ Đường keeps a player from getting lost: they choose where to go - the place that fits their tu
vi, another land, home, the village - and an arrow round their character leads them there, along a
real path, through the right gates, out of the Động Phủ and back.

## What the player sees

| Key | Where | What |
|---|---|---|
| **N** | world, abode | the picker "Chỉ Đường" (HUD button `N` left of the minimap; in the abode the button "Chỉ Đường (N)" under the player card) |
| **H** | world | Về Động Phủ in one press (in the abode H stays the hive) |
| **M** | world | Thiên Địa Đồ, the big map (button `M` under `N`; in the abode M stays the math hall: the picker has "Mở Thiên Địa Đồ") |
| 1-9 | picker | choose a row; Esc or N closes |
| Tab | big map | this zone / the world; M or Esc closes |

None of them fires while the chat box is being typed in (`chatbox.typing`), like every other hotkey.

* **The picker**: "Khu hợp tu vi: ..." first (gold), with the one-line reason from the server; the
  other open lands (with "hợp Luyện Khí tầng 4-6" once their maps have khu); the locked lands, greyed,
  with the door's reason ("Chưa vào được ..."); Về Động Phủ (H); Về Trúc Lâm Thôn; Mở Thiên Địa Đồ (M);
  Tắt chỉ đường (while an arrow is set).
* **The arrow**: a gold arrow with a one-pixel dark outline and a shadow, drawn in the world layer
  (under the name tags), on an oval round the player's body, pointing along the next leg of the way
  and nudging back and forth. A pale blue arrow means "no way on foot" (see below) or "still
  searching". Under the zone label a plate gives the goal's name and the distance in **trượng**
  (1 trượng = 2 tiles = 32 px, along the path, plus a straight guess of the zones still to cross), and a
  second line: "qua cổng Kiếm Trủng Sơn" (the next gate), "đang dò đường...", "Không có lối đi bộ: thử
  Đạp Kiếm Lướt (G)", or in the abode "Tới cổng rồi, nhấn E để ra".
* **Arrival**: "Đã tới Kiếm Trủng Sơn." and the arrow goes away. "Về Động Phủ" ends at the abode's gate in
  the village ("Đã tới cổng Động Phủ. Bước qua cổng là về nhà."): stepping in is the player's own step.
* **The minimap** (top right, at most 100 x 64, the quest and guide trackers hang under it as before): a
  small map is shown whole; a big one is a window at one pixel per tile that follows the player. Gates,
  other players, the Linh Hồ's finds, the way (a gold line) and the goal (a blinking square, or a mark on
  the window's edge when it is outside) are on it.
* **Thiên Địa Đồ**: "Vùng này" - the zone in full, its khu tinted by band (green Ngoại Vi, gold Trung
  Vực, red Thâm Xứ, blue An Toàn) with their names and stages ("tầng 4-6", red when above the player's
  working stage), the gates with the zone they lead to, the named places (`poi`), the player and the
  way; a click on a khu leads there. "Thiên hạ" - every land round the village in the direction of its
  gate, open or locked (hover: why), the recommended one in gold; a click on an open land leads there.
* **The khu banner**: walking into a khu shows its name and "hợp Luyện Khí tầng 4-6" for 3 seconds, red
  with "cao hơn tu vi của con" when the khu starts above the player's working stage, "nơi an toàn" for a
  band 0 khu. It waits while toasts are up (they sit right under it) and makes way when one comes.

## The rule (server: `server/app/systems/navigation.py`, `GET /nav/destinations`)

"Tu vi" for places is the player's place in Đạo Thụ (`math_tree_progress`), never the cultivation realm.

1. For every branch, where the player is learning (`learning_of`, the one function to replace when
   the Lộ Trình gets a "next step" API): ds, gt, xs, tr - the node of the frontier of the branch's
   subject (R9); lt, ud (no subject) - their first open main node, else the last done one.
2. For every land the player may walk into (`lands.refusal`, so exactly the world's doors), that
   branch's stage as a stage of the land's realm (a frontier in a later realm counts as tầng 9).
3. **Recommended** = the land whose branch has the lowest stage; ties in the order ds, gt, xs, tr, lt,
   ud (the four math branches before the exercise lands). Lôi Kiếp Đài wins over everything once it is
   open and the player has reached the last stage of the realm. A newcomer learns tầng 1 everywhere:
   Kiếm Trủng Sơn (ds).
4. **The place inside the land** (`fit_khu`): the khu whose `[stage_min, stage_max]` holds the stage
   (the first in map order); with none holding it, the deepest khu below it, else the shallowest; a khu
   of band 0 is never a goal. The point to walk to is the khu's `anchor`. A map with no khu (all of
   today's maps) gives the land itself, walked to at its `from_village` spawn - the arrow then ends at
   the gate, and gets finer by itself the day the map gains khu.
5. Every other open land is an alternative with its own fitting khu; the locked lands come with the
   door's reason; home and the village complete the list. The shape is in `docs/API.md`.

## The way (client)

* `client/engine/navigator.py` - **in a zone**: a grid of foot positions every 8 px (cell (cx, cy) =
  the feet at (8 cx, 8 cy + 3), so the middle of a one-tile corridor is a cell), walkable when the
  movement foot box (10 x 6, `engine/movement.py`) made 2 px taller touches no solid - rasterised from
  the solid rectangles row by row; then a breadth-first **distance field from the goal** (the walkable
  cells of a gate, or round a point) over the whole map. A player who strays needs no new search: the
  way is read again from wherever they stand (`Leg.read`): down the field, the arrow pointing at the
  farthest of the next 14 cells that can be walked to in a straight line (each point on the line has
  its 2 x 2 surrounding cells walkable, whose boxes hold the foot box). A player where the field never
  reached (an island reached by Đạp Kiếm Lướt) gets a straight arrow and the hint. Building the grid and
  the field are generators run 3 ms per frame. **From zone to zone**: the gates of every shipped map
  (`portal` objects, and the abode's `interact` object with action `exit`) form a graph; the route is a
  breadth-first search over zones; after each zone change (a new world scene) the next leg is planned
  by itself, since the state lives on the game (`client/engine/chi_duong.py`, `chi_duong.of(game)`).
* Timings (this machine, Python 3.14): a 320 x 240 tile perfect maze (9 455 solids, 186 000 reachable
  cells): grid 13 ms + field 50 ms, spread over 16 frames, the longest slice 3.5 ms; an open giant land
  with a river and 2 500 rocks in the real game loop: 40-52 frames of about 3 ms (0.13-0.15 s in all);
  one reading 0.3 ms.

## Files

* server: `server/app/systems/navigation.py` (the rule), `server/app/routers/nav_routes.py`
  (`GET /nav/destinations`), one line in `server/app/main.py`; reads `realtime/dia_do.py` (khu),
  `realtime/lands.py` (doors), `systems/math_tree_progress.py` (the frontier).
* client: `client/engine/navigator.py` (grid, field, legs, gates), `client/engine/chi_duong.py` (the
  destination and the way across zones, the khu watch), `client/engine/minimap.py` (overview from the
  tile colours, the minimap window), `client/ui/nav_arrow.py` (the arrow), `client/ui/nav_hud.py`
  (plate, banner, keys and buttons), `client/scenes/world_map.py` (the picker and Thiên Địa Đồ),
  `client/strings_nav_vi.py` (every new on-screen string); hooks in `client/scenes/world.py`
  (`_build_minimap`, the minimap HUD block, one call after drawing the world, one in the HUD) and
  `client/scenes/abode.py` (the same two calls).
* tests: `server/tests/test_navigation.py` (the rule on synthetic lands and khu, the route);
  `client/tests/test_nav_units.py` (grid against the collider, corridors, round a wall, a maze walked by
  the arrow, straying, an island, a giant map in budget, the zone route, a synthetic .tmj with khu: the
  banner, the khu goal, the overview, the minimap window, the arrow sprites, the font);
  `client/tests/test_nav_flow.py` (the real client and server: picker, arrow through the village gate
  into Kiếm Trủng Sơn, the big map and its clicks, the khu banners, H home to the abode gate, out of
  the abode by E to the village; and a synthetic giant land, `client/tests/nav_giant.py`).
  `python -m client.tests.test_nav_flow tools/reports/nav` writes the screenshots.
