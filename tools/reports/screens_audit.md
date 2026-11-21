# Screens audit

Written by `tools/audit_screens.py` (scales 2, 3); checks of `client/ui/audit.py` plus glyph / ellipsis / label (see the tool's docstring).

Before: the same tool and cases run on the scene code as it was before this work (commit 750b253).
Totals: **211 hard problems before, 0 after**, over 83 cases x 2 scales = 166 frames. "Meant cuts" are
cuts kept on purpose, each with its reason below (the whole text is one hover or one click away).
Some "before" numbers are low: the bag's weapon list was not clamped when scrolled past its end, so it
showed "1000-48/48" and only 8 of its rows; once clamped, 32 more problems of its last rows appeared and
were fixed too.

## How the cases are fed

- The maths hub, node card and summaries: payloads built from the server's own data and helpers
  (tree.json, the real parts, gates, sources, exercises, chiêu), with the longest node name and the
  longest `why_vi` of tree.json put on the current Chính đạo node, every branch tab, each tab scrolled to
  its end, a 9-node stage.
- Everything else (guide, placement, dungeon, tower defence, fortune, linh căn, achievements, công pháp,
  bag, shop, pets): real payloads. `tools/screens_data.py` runs the FastAPI app in the same process on a
  throw-away SQLite file (the real migration), makes one player with every stackable item of the
  catalog, one piece of every equipment, six Linh Thú and a linh căn, and GETs what each screen reads.
  The guide is also shown once Chính đạo leads (board entry and HUD tracker) with the longest node name.
- The code screens (exercise statement with the longest statement, a failing run with a long traceback,
  Xạ Trường scored exercise): the cases of `client/tests/test_code_editor.py`.

## What was found and fixed

- Hub, branch tabs (168): a long node name took two lines at size 8 in a 16 px row and ran into the rows
  above and below and over their click areas; "Tầng 5" / "Để sau" stacked 7 px apart overlapped.
  `fit_lines` (math_tree.py) gained a `height`: two lines are taken only at a size where they fit the
  row (one line at 8/7/6 first, then two lines at 5); the row's click area is the row's full height; the
  "Để sau" mark is one size smaller and both lines moved apart.
- Hub, Chính đạo stage list: the row now has the whole name as its tooltip (two columns of 9 nodes cut
  the longest name; it is whole in the card above).
- Summary after a Thiên kiếp nhỏ (6): lines were placed at a fixed pitch, so a wrapped "Nút mới mở: ..."
  list covered the next line. The lines now stack by their real height, a size smaller while they would
  not clear the button. (The tool's own case for the summary after a sitting also crashed on a node with
  no part; fixed in the tool.)
- Guide board (8): the selected row's size-9 title touched its description (moved 2 px); the Chính đạo
  chapter entry's two lines touched; the HUD tracker cut its hint with "..." - it now takes size 6 and,
  when still too long, a second line (the box grows, like it already did for a two-line title); a
  two-line node title starts one pixel lower so its marks clear the header. Cut stage-list names under
  the Chính đạo entry have a tooltip.
- Bag (10 + 32): a usable item that could also be sold drew BOTH "Dùng" and "Bán" on top of each other
  (an `elif` chain on `cond and ui.button(...)`); the page counter ran into "Đóng"; the weapon list was
  not clamped when scrolled; weapon and spot rows had their two lines touching; a gear row's stats line
  is shown a size smaller before any cut and is whole in its tooltip; a locked weapon's reason is whole
  on hover.
- Achievements (6): a card's name and description touched at scale 3 (name 1 px higher).
- Pets (6): the name / level of a card and of the detail panel touched (moved apart).
- Shop (5): an item's name and "còn n/n hôm nay" touched (moved 1 px).
- Tower defence (2): the "Ải giữ thành" heading touched the level buttons (buttons 1 px lower).
- Công pháp: the tool could not open it at first (it needs the world's icon drawing; the case now
  borrows `WorldScene.draw_mskill_icon`); long chiêu names in a 64 px cell get a tooltip.

## Screens not covered

- essay hall (Luận Đạo Đài): no scene in the client: essay grading by the API was dropped (2026-11-20), so there is nothing to open
- The question cards themselves are covered by `tools/audit_layout.py` (the whole bank), the lesson
  reader by its own paged layout tests; neither is repeated here.
- The world HUD apart from the guide tracker, the fishing / hive / alchemy / gacha screens and the
  character sheet are not in this audit (not asked; they hold little text).

## Hard problems per screen

| screen | frames | hard now | hard before | meant cuts | kinds now |
|---|---|---|---|---|---|
| achievements | 16 | 0 | 6 | 4 | - |
| bag | 12 | 0 | 10 | 16 | - |
| code | 4 | 0 | 0 | 0 | - |
| cong_phap | 2 | 0 | 0 | 9 | - |
| dungeon | 2 | 0 | 0 | 0 | - |
| fortune | 2 | 0 | 0 | 0 | - |
| guide | 42 | 0 | 8 | 2 | - |
| hub | 38 | 0 | 168 | 8 | - |
| linh_can | 4 | 0 | 0 | 0 | - |
| node_card | 14 | 0 | 0 | 0 | - |
| pets | 4 | 0 | 6 | 0 | - |
| placement | 2 | 0 | 0 | 0 | - |
| shop | 12 | 0 | 5 | 0 | - |
| summary | 6 | 0 | 6 | 0 | - |
| td | 4 | 0 | 2 | 0 | - |
| xa_truong | 2 | 0 | 0 | 0 | - |

## Hard problems left

None.

## Meant cuts (not hard)

- achievements: the reward list of a tier keeps to two lines beside the claim button; the whole list is the card's tooltip (4 texts, e.g. '1000 Linh Thạch, 5 Tiên Ngọc, Linh Tủy Tinh x2, Danh hiệu «.')
- bag: why a weapon is still locked, on its 18 px row: whole on hover (7 texts, e.g. 'Cần Luyện Khí tầng 3 trên Đạo Thụ (đang ở Luyện Khí tầng 0).')
- cong_phap: a chiêu name in its 64 px cell: whole on hover and in the details when picked (8 texts, e.g. 'Băng Phong T...')
- guide: the stage list under the Chính đạo entry in two columns (the tool puts the longest name there): whole in the entry's title and on hover (1 texts, e.g. '1. Thiên kiếp Trúc Cơ: một bài toán dữ liệ...')
- hub: a Chính đạo stage list row in two columns (the tool puts the longest name of the tree there): the whole name is in the card above it and on hover (1 texts, e.g. 'Thiên kiếp Trúc Cơ: một bài toán dữ liệu bảng từ...')
