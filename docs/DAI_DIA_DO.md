# Đại Địa Đồ: authoring a giant land

The lands of Luyện Khí are giant maps (320 x 240 tiles of 16 px, a screenful at the client's 2x
zoom is about 15 x 8.5 tiles). A land is cut into **khu** by band of tu vi; the server scales its
monsters by band, the navigation arrow and the big map read the khu and the points of interest.
This guide is everything needed to build one more land without touching a shared file beyond
what is listed in [The checklist](#the-checklist).

The two exemplars: `tools/mapgen/lands/loan_so_coc.py` (Kiếm Trủng Sơn, a sword-grave mountain)
and `tools/mapgen/lands/luu_van_coc.py` (Lưu Vân Cốc, a valley with one winding stream). Read
one of them next to this page.

## The maps of the world

`tools/check_maps.py` checks that every map has the size listed here. A land that grows changes
its row in the same commit.

| map | name | size | kind |
|---|---|---|---|
| `abode` | Động Phủ | 40 x 24 | private |
| `truc_lam_thon` | Trúc Lâm Thôn | 56 x 36 | hub |
| `rung_muc_loang` | Mê Đồ Lâm | 320 x 240 | land, giant |
| `ho_nghien_muc` | Vạn Tượng Trạch | 320 x 240 | land, giant |
| `loan_so_coc` | Kiếm Trủng Sơn | 320 x 240 | land, giant |
| `luu_van_coc` | Lưu Vân Cốc | 320 x 240 | land, giant |
| `thien_cong_phuong` | Thiên Công Phường | 320 x 240 | land, giant |
| `linh_xa_nguyen` | Linh Xạ Nguyên | 320 x 240 | land, giant |
| `loi_kiep_dai` | Lôi Kiếp Đài | 120 x 90 | boss arena, no khu |
| `bi_canh` | Bí Cảnh | 66 x 32 | instance |

## Commands

```
python tools/gen_maps.py                       # every map (client/assets/maps + server/maps, byte-identical)
python tools/gen_maps.py loan_so_coc           # only the maps named (their ZONE)
python tools/check_maps.py                     # every map checked (also run by tools/check_all.py)
python tools/check_maps.py --report            # + the khu table of every banded map
python tools/preview_map.py <zone> out.png --scale 3            # the overview
python tools/preview_map.py <zone> out.png --crop x,y,30,17     # real tiles and props at 2x zoom
```

A giant land takes about 10 s to generate. The maps are generated, never edited by hand: after a
run `git status` must show only the maps whose code changed (a map with more than 20 000 tiles is
written without indentation, the others as before).

## The package

```
tools/gen_maps.py            the entry point (unchanged CLI)
tools/mapgen/__init__.py     finds the land modules, writes the two copies
tools/mapgen/builder.py      MapBuilder: ground grid, objects, collision -> Tiled JSON
tools/mapgen/giant.py        DaiDiaDo: the toolkit of the giant lands (this page)
tools/mapgen/lands/<map>.py  one map each: ZONE = "<map>", build() -> dict
```

A new module in `tools/mapgen/lands/` is found on its own; there is no list to register it in. To
enlarge an existing small land, replace the body of its module (its `ZONE` stays). Keep the
small map's places (see [What a land keeps](#what-a-land-keeps)).

## The contract of a map (frozen)

Read `server/app/realtime/dia_do.py`. Objects of the `objects` layer, every property a string:

* `khu` - its rectangle is the khu (pixels). `khu` (id, unique in the whole world, prefix it with
  the land: `kts_`, `lvc_`...), `name_vi`, `band` ("1".."3"; "0" a safe place), `realm`,
  `stage_min`, `stage_max`, `anchor_x`, `anchor_y` (pixels, a walkable point reached on foot
  from `spawn`: where Chỉ Đường leads), `desc_vi`, `safe`. Where two khu overlap, the one listed
  first wins: the camps come first.
* `monster_area` - `monster`, `count`, and on a banded map `khu`, `band`, `realm`.
* `poi` - `poi` (gate, camp, bi_canh, npc, beast, boss, landmark), `name_vi`; its centre is where
  it is.
* the map property `dai_dia_do` = "true" on a giant land.

`DaiDiaDo.finish()` writes all of these from what the module declared; a module never writes a
`khu` or `poi` object by hand.

## Bands in the game

`server/data/math/dia_do.json`, read by `server/app/realtime/dia_do.py`:

| band | name | stages | hp | atk | def | xp | stones | loot cap |
|---|---|---|---|---|---|---|---|---|
| 0 | An Toàn (a camp) | - | - | - | - | - | - | no monster |
| 1 | Ngoại Vi | 1-3 | x1.0 | x1.0 | x1.0 | x1.0 | x1.0 | `luyen_khi:3` |
| 2 | Trung Vực | 4-6 | x1.15 | x1.1 | x1.1 | x1.2 | x1.2 | `luyen_khi:6` |
| 3 | Thâm Xứ | 7-9 | x1.3 | x1.2 | x1.2 | x1.45 | x1.45 | `luyen_khi:9` |

* A monster takes the band of its `monster_area`; a monster of a map without bands has band 0
  and behaves exactly as before.
* Its numbers are scaled where they are read (`Monster.info` in `realtime/ai.py`; xp and stones
  of the kill in `realtime/combat.py`); band 1 is the old monster unchanged.
* Its drops stay within the band's cap and the zone's own cap, whichever is lower
  (`systems/loot.py` `band_within`, `band_allows`): an item above the cap is simply not part of
  what that band drops (not reported as locked); gear rarity and weapon drops are capped the same
  way. A ghi chú lỗi sai always drops.
* `full()` sends the band as `"kv"` (docs/PROTOCOL.md).
* A land creature in a banded khu asks first those of its own `nodes` whose stage lies in the
  band, when the player may practise one of them; otherwise the old rules (`realtime/lands.py`).
  A quái lỗi sai keeps its own micro-skill.

## Distribution of the monsters (the rules)

The numbers are in `dia_do.json` `distribution`; `tools/check_maps.py` enforces them.

1. Every khu of band 1-3 has **at least two kinds** of monster.
2. **Band 1** gets the creatures of the low stages (normal rank); **band 2** the middle
   creatures and a few elites; **band 3** the high-stage creatures and the elites. A creature
   whose `nodes` span several bands may live in several (Thiết Giáp Thú: stages 3, 5 and 7), and
   then asks the nodes of the band it stands in.
3. **Elites are rare**: one elite per area (`count` 1), at most `max_elites_per_khu` (8) per khu.
4. **No boss in a wild land** (Lôi Kiếp Đài, the boss arena, has no bands).
5. **Nothing spawns within `clearance_tiles` (10) tiles** of a gate (portal), a spawn or a camp.
6. **Density**: about one monster per `tiles_per_monster` (150-250) walkable tiles inside the
   monster areas of a khu (an area of 2 or more: 112-375 each).
7. **At most `max_monsters_per_land` (260) monsters per map** (the server's budget).
8. **An area fits in the leash**: a monster dragged more than `leash_radius` (260 px,
    `server/data/balance/combat.json`) from the middle of its area gives up the fight, so no
    point of an area may lie further than 0.8 x that from its middle: at most about 20 x 15
    tiles. Make many small areas, never one big one (`monster_area` refuses a bigger one).
9. **A land's creatures stay in their land** (`land` in `server/data/math/monsters.json`).
10. **The nine quái lỗi sai** (`dstt_*`) stay in Kiếm Trủng Sơn, band 1, grouped by their floor
   (Loạn Số Cốc: floor 1 nearest the gate camp, floor 3 at the far end).
11. A land that has no normal creature of tầng 7-9 (Lưu Vân Cốc) fills band 3 with its elites
    only, one per area, a handful per khu; a later creature of those stages goes there.

## The toolkit (`tools/mapgen/giant.py`)

Coordinates are tiles; a rectangle `(x0, y0, x1, y1)` includes both corners. Everything is
deterministic from the seed given to `DaiDiaDo(zone, name_vi, w, h, seed)`. Call the steps in this
order (each one reads what the ones before wrote):

| step | call | what it does |
|---|---|---|
| 1 | `m.khu(id, name_vi, band, rect, theme, anchor, desc_vi)` | a khu of band 1..3; `anchor` a tile on a road (use the tile of its road node); stages come from `dia_do.json` |
| 2 | `m.paint(warp=7, scale=26)` | every tile gets the ground of its khu's theme; borders wobble by `warp` tiles (domain warp), so no khu looks like a rectangle |
| 2 | `m.camp(id, name_vi, center, r, desc_vi, label_vi)` | a rest camp: band 0 khu (listed first), plaza with lanterns, a well, mats; a road node of the same id, a poi, a clearance zone |
| 3 | `m.river(points, width=3)` | water along a line of tile points, stone banks; roads bridge it |
| 3 | `m.lake(cx, cy, rx, ry)` / `m.blob(...)` | a noisy ellipse of water / the tiles of one |
| 3 | `m.chasm(tiles)`, `m.wall(tiles)`, `m.open_tiles(tiles, key)` | solid ink, solid ground of another kind, make walkable again |
| 3 | `m.keep_rect(x0, y0, x1, y1)` | no barrier and no scatter there (a landmark's ground) |
| 4 | `m.barriers({(a, b): kind}, default="trees")` | a wall on the border of every pair of neighbouring khu: `trees`, `pines`, `dead_trees` (2 tiles), `cliff`, `chasm` (4 tiles), `water`, `open` |
| 5 | `m.node(id, tile, label_vi, sign=True)` | a place the roads join; `label_vi` is what signposts elsewhere say about it |
| 5 | `m.network([(a, b, "main" or "trail", chasm_ok)])` | A* roads: a road through water is a bridge, through a wall a pass (wider by one tile), through a chasm a land bridge (only with `chasm_ok`); roads reuse roads, so forks appear on their own |
| 5 | `m.carve(tiles, style)` | paint a road by hand (the last tiles through the gate) |
| 6 | `m.thing`, `m.sign`, `m.building`, `m.npc`, `m.obj`, `m.tree` | the module's own places (MapBuilder); `m.poi(kind, name_vi, x, y)` / `m.landmark(...)` |
| 7 | `m.signposts()` | a sign by every node with `sign=True` and 2+ roads: one line per way out, "Bắc → Trại Luyện Kiếm · cửa Trung Vực" (the fonts draw `→` but not the other arrows: directions are words) |
| 8 | `m.monster_area(khu, monster, rect, count, name)` | one area by hand (band, khu, realm from the khu) |
| 8 | `m.monsters(khu, [(kind, weight)], [(elite, n)], cell=(18, 14), tiles_per=210, skip=None, max_areas=None)` | fills a khu: cells kept when clear of gates, spawns and camps, mostly walkable, reachable and on the khu's own side of its border; kinds take the cells by weight; `elites` add n one-elite areas |
| 9 | `m.dress_barriers()` then `m.scatter()` | the trees and boulders on the walls; props over every walkable tile by the theme's density map (sparse in the open, dense in noise clumps; solid props keep off the roads) |
| 10 | `m.finish(extra_props, ring=sprite, gaps={(side, tile)})` | the ring of trees around the map open at the gate, the collision of every solid tile (merged rectangles), the khu and poi objects, the budget check |

The gate, its portal and the spawns are written with `m.gate(...)` (or `m.obj(...)` when the old
map named its portal differently), after `scatter()`, with a `poi("gate", ...)`.

**Arrival spawns lie in the gate camp.** On a map with khu every spawn (`spawn`, `from_village`,
any other) must lie inside a band 0 khu, so a player walking in sees the camp's name first and
never "band 1, then the camp, then band 1 again" (`check_maps` enforces it). Give the gate camp
`to_edge` toward the gate: `m.camp("kts_trai_cong", ..., to_edge="s")` stretches its khu to that
edge of the map, over the gate and the spawns.

**Gotchas.** `open_tiles(tiles)` over ink or water only makes the tiles walkable: pass a repaint
key (`open_tiles(tiles, "stone0")`), or the ground still shows ink or water. `keep_rect` before
`scatter()` gives a clearing (the client tests stand players in the middle of some monster areas).

### More helpers: `tools/mapgen/lands/_xay_dung.py`

Built by the authors of Thiên Công Phường, Linh Xạ Nguyên and Lôi Kiếp Đài on top of giant.py
(which they did not change). A module whose name starts with `_` is not a map. Import from it:

| helper | what it does |
|---|---|
| `streets(m, khu, pitch, keep_p, offset, min_run)` | a grid of paved 2-tile streets over a khu, one every `pitch` tiles; each stretch survives with chance `keep_p` (a ruin keeps few); returns the street lines |
| `blocks(k, xs, ys, inset)` | the rectangles between those streets |
| `fill_block(m, rect, ri, plan)` | furnish a block: `plan` = [(chance, kind, name)], kind a building of `BUILDINGS` or a prop of `PROPS` |
| `try_building`, `try_thing`, `clear_box` | place one building or prop where the box is free (in region `ri`) |
| `lane(m, tiles, key)` | hand-painted walkway tiles that count as road (planks, a stair) |
| `fence(m, tiles, ground, sprite, every)` | solid tiles with a picket picture |
| `outline(x0, y0, x1, y1)`, `solid_ring(m, tiles, key)` | the border of a rectangle; solid wall tiles that are no barrier (roads go round) |
| `finish_unbanded(m, extra_props, ring, gaps)` | `finish()` for a giant-toolkit map that must have **no khu**: a boss arena (Lôi Kiếp Đài) keeps its monsters exactly as before, its monster areas written by the module |
| `PROPS` keys `x_anvil`, `x_board`, `x_mat` | extra scatter props of the city lands |

A boss arena has no khu, no bands and no camps: build it with the toolkit, finish it with
`finish_unbanded`, and write its monster areas with `m.obj(..., "monster_area", ...)` as the small
maps did (`monster_area()` needs a khu).

### Themes

`THEMES` in giant.py: `dong_co` (meadow), `dong_hoa` (flowers and peach), `chan_nui` (foothill:
grass, dark patches, pines, a few sword graves), `rung_thong` (pine wood), `rung_toi` (dark wood of
dead trees), `thach_lam` (stone forest), `bai_kiem` (field of sword graves, paved roads),
`dinh_nui` (bare peak), `dat_hoang` (waste of dirt and stone, paved roads), `cao_nguyen` (stone
plateau in the clouds), `bai_suoi` (river banks). A land adds its own in its module:

```python
m.themes["suon_kim"] = Theme("suon_kim", ground_fn, open_props, dense_props,
                             open_density, dense_density, clump_scale, clump_cut, road=())
```

`ground_fn(P, D, r) -> TILESET key`: P a large-patch noise, D a detail noise (both 0..1), r a
random per tile. Change tiles that look alike at random (grass0/1/2, dark_grass0/1); change tiles
that look different only by P or D thresholds, so they come in patches. Never put `ink` or
`water` on walkable ground (they look like liquid). Props are names of `PROPS`: tree, pine,
peach, dead_tree, rock, boulder, bush, tall_grass, stump, log, crystal, cloud, grave, bamboo,
lantern. Every sprite there has a picture (`client/engine/sprites.py` or
`client/assets/v2/wiring.json`); a new sprite needs a picture first (the validator refuses a
sprite with none).

## What a land keeps

When a small land grows, everything other data points at moves with it:

* the spawns `spawn` and `from_village`, the portal back to the village with the same
  `target` / `target_spawn` (the village map does not change);
* every `interact` (actions), `sign`, `npc`, `char`;
* `world_plan.json`: `weapons_placed[].pos` and `beasts[].pos` of the land (tiles), their
  `spot_vi` / `where_vi`, and the land's `desc_vi`. A spot that `needs` Đạp Kiếm Lướt must not be
  reachable on foot and must be reached by one glide of at most 80 px over water or ink from a
  walkable tile (copy the peak of Kiếm Trủng Sơn or the pool of Lưu Vân Cốc: a 3 x 2 islet in a
  ring of ink or water two tiles wide, a ledge of stone south of it);
* the creatures of the land (`monsters` of its world_plan entry) all spawn somewhere;
* tests that hard-code a place of the map: grep `server/tests` and `client/tests` for the zone,
  the land id and its beast and weapon ids. Derive places from world_plan or the map instead of
  writing tiles into tests.

## Beautiful when walked

* Every screenful (15 x 8.5 tiles) needs something to look at and a readable way on: a road, a
  sign, a landmark, a clump of trees, a change of ground. No empty carpet of one tile; no noise
  soup either.
* Walls read as walls: a cliff is boulders on stone, a tree line trees on dark grass, a chasm ink.
  Players go deeper only through passes; a camp waits after each wall.
* A landmark worth walking to in every khu (a shrine, a lake, a ring of graves, a crag).
* Look at the overview and at a few crops at real size before calling a land done
  (`tools/preview_map.py`), and commit the overview under `tools/reports/maps/<zone>.png`.

## The checklist

1. `tools/mapgen/lands/<map>.py`: `ZONE`, `SIZE`, `build()` with the steps above.
2. Its row in the table of this page (the size).
3. `server/data/math/world_plan.json`: the positions and descriptions of the land's weapons and
   beasts, its `desc_vi`.
4. `python tools/gen_maps.py <map>`; `git status` shows only that map (two copies).
5. `python tools/check_maps.py --report`: OK, the khu table as intended, every spawn inside the gate camp.
6. `python tools/preview_map.py <map> tools/reports/maps/<map>.png --scale 3`, and look at it and
   at crops.
7. The tests of the land (grep), `python tools/check_all.py`.

The only shared files a new land touches are the row of the table above and its entries of
world_plan.json.
