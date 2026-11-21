# Quái của bí cảnh: who a run fields

Which creatures a run of a bí cảnh fields depends on **which bí cảnh it is** (its theme) and on
**the tu vi of the party** (its band). Everything is data: the `quai` block of each realm of
`server/data/realms.json`, read by `server/app/systems/realm_quai.py`; the live run
(`server/app/realtime/realm.py`) asks it for the plan once, when the run opens.

Questions never come from these creatures: every player is asked at their own floor and tier
(`math_ask.pick_own`, `server/app/systems/math_realm.py`). A creature only decides the fight
around the question: its body, its numbers, its drops.

## The band of a party

* A player's band is their place in Đạo Thụ (`lands.TreePos`, read fresh from the database when
  the run opens): the stage being learned, i.e. the stage reached + 1, in Luyện Khí, cut like the
  giant lands (`server/data/math/dia_do.json`): tầng 1-3 **Ngoại Vi** (1), 4-6 **Trung Vực**
  (2), 7-9 **Thâm Xứ** (3). Beyond Luyện Khí: Thâm Xứ. A newcomer: Ngoại Vi.
* The party's band is **the weakest member's**, so nobody is dragged into a run above them.
* A rift also answers to the khu it tore open in: its band is the lower of the party's and the
  khu's (a strong party at a rift in Ngoại Vi meets Ngoại Vi's creatures).
* The gate shows it under every bí cảnh: "Bí cảnh theo tu vi tổ đội: Trung Vực" (alone: "theo
  tu vi của con"), from `GET /realms` (`band`, `band_vi`, `band_party`).

## What the band changes

* the rows below: which creatures, how many, an elite from Trung Vực on;
* every monster of the run carries the band like a monster of a banded khu (`ai.Monster.band`):
  hp, atk, def, xp and stones x the band's `mult` (x1.0 / x1.15 / x1.3 hp...), the boss
  included, so the boss is a little tougher in a deeper band; `"kv"` on the wire;
* its drops stay within the band's `loot_cap` (`luyen_khi:3` / `:6` / `:9`) and the bí cảnh's own
  cap (`server/data/loot_tiers.json` `source_caps`), whichever is lower (realtime/combat.py);
* the room loot and the final chest: stones x the band's `mult.stones`, no item above the band's
  cap. The chest's `treasures` (Linh Quả, its only source) and the Mảnh Bảo Vật of Mặc Ảnh Động
  are bounded by the bí cảnh's own cap and the player's own tu vi only, as before.

## The table

Counts are per room; "a, b x3" means three creatures drawn from a and b, every kind once before
any twice. The boss's hp is its kind's hp x `hp_mult` x (1 + 0.4 per extra member) x the band's
hp mult.

### Mặc Ảnh Động (theme `muc`: the ink cave of Nghiên Ma, the old Mặc Quái)

| band | room 1 (ấn đá) | room 2 (hàng ấn) | room 3 (cột ấn) | boss | loot cap |
|---|---|---|---|---|---|
| 1 Ngoại Vi | Mực Con, Lân Hỏa Yêu x3 | Mực Con, Lân Hỏa Yêu, Mặc Ảnh x3 | Lân Hỏa Yêu, Mặc Ảnh x3 | Nghiên Ma x1.0 | luyen_khi:3 (treasures: realm uncapped) |
| 2 Trung Vực | Lân Hỏa Yêu, Mặc Ảnh x3 | Mặc Ảnh, Bút Yêu x3 | Mặc Ảnh, Bút Yêu x3 + **Mặc Hồ** | Nghiên Ma x1.0 | luyen_khi:6 |
| 3 Thâm Xứ | Lân Hỏa Yêu, Mặc Ảnh, Bút Yêu x4 | Mặc Ảnh, Bút Yêu x4 | Bút Yêu, Mặc Ảnh x4 + **Mặc Hồ** | Nghiên Ma x1.0 | luyen_khi:9 |

### Khe Nứt Mực (theme `land`: a rift spills the creatures of its land)

| band | the room (ấn đá) | boss | loot cap |
|---|---|---|---|
| 1 Ngoại Vi | 2 of the land's normals | Nghiên Ma Non (Nghiên Ma x0.5) | luyen_khi:3 |
| 2 Trung Vực | 3 of the land's normals | Nghiên Ma Non x0.5 | luyen_khi:6 |
| 3 Thâm Xứ | 3 of the land's normals + 1 of its elites | Nghiên Ma Non x0.5 | luyen_khi:9 |

Where the creatures come from (`realm_quai.land_pool`):

* opened inside a khu of band 1-3: at the khu's own band, **that khu's** creatures (its
  `monster_area`s); a weaker party: the land's areas of the party's band;
* opened elsewhere on a banded land (a camp, between two khu): the land's areas of the band;
* on a land without bands (an old small map): every creature of the zone;
* a band whose khu hold elites only (Lưu Vân Cốc's Thâm Xứ) takes its normals from the band
  below; a zone with no creature at all falls back to the ink family (Mực Con, Lân Hỏa Yêu,
  Mặc Hồ: it is a Khe Nứt Mực).

Rifts open in every wild land of Luyện Khí (`balance/realm.json` `rift.zones`), at most three
at once. Examples today: Kiếm Trủng Sơn Ngoại Vi gives Kiếm Linh and Thiết Giáp Thú (in Loạn
Số Cốc: its quái lỗi sai), Thâm Xứ Thiết Giáp Thú + Ma Trận Thú; Lưu Vân Cốc Ngoại Vi Vân Xà and
Vân Điệp, Thâm Xứ the same + Lôi Ưng or Phong Lang; Thiên Công Phường Cơ Quan Thú, Cơ Quan Nhân
(+ Cơ Quan Nhân Đầu Đàn or Lò Linh); Linh Xạ Nguyên Thảo Nhân, Tâm Ma (+ an elite); Mê Đồ Lâm and
Vạn Tượng Trạch whatever their maps field.

### Toán Trận Bí Cảnh (theme `tran`: a trial array of quái lỗi sai)

| band | room 1 (ấn đá) | room 2 (hàng ấn) | boss (Trận Tâm) | loot cap |
|---|---|---|---|---|
| 1 Ngoại Vi (floor 1) | Phần Tử Ma, Nghịch Hiệu Ma x2 | Phần Tử Ma, Nghịch Hiệu Ma x2 | Trận Chủ Ảnh Trùng Ma | luyen_khi:3 |
| 2 Trung Vực (floors 1-2) | Phần Tử Ma, Nghịch Hiệu Ma, Phần Ảo Ma x3 | Phần Ảo Ma, Bình Phương Ma x2 + **Ảnh Trùng Ma** | Trận Chủ Mô Đun Ma | luyen_khi:6 |
| 3 Thâm Xứ (floors 1-3) | Phần Tử Ma, Phần Ảo Ma, Bình Phương Ma x3 | Bình Phương Ma, Chỉ Số Ma, Chuyển Vị Ma x3 + **Mô Đun Ma** | Trận Chủ Đối Xứng Ma | luyen_khi:9 |

The Trận Chủ is the elite quái lỗi sai of the band's deepest floor holding the array: its own
body, picture and ghi chú lỗi sai, with the boss numbers of Nghiên Ma (`stats_from`: hp, group
shield, its phases) x0.6. The elite of the floor below guards the last room (the warden); in
Ngoại Vi the only floor-1 elite is the Trận Chủ itself, so there is no warden.

## The rules (checked by `realm_quai.validate`, inside `math_realm.validate`, run by `tools/check_all.py`)

1. Every bí cảnh has a `theme` and a row for **every band**, with one room row per room of its
   `math.rooms`.
2. Every fielded creature exists (`catalog.monsters`) and has its picture
   (`client/assets/v2/wiring.json` `monsters` -> a sheet on disk). No new art, no new creature.
3. **No creature of another theme**: `muc` fields only the ink family
   (`data/creatures/monsters.json`); `tran` only quái lỗi sai, of floors 1..band; a rift only the
   creatures of its own land (`land` of `data/math/monsters.json`), or the ink fallback.
4. Room `kinds` are normals; an `elite` is an elite, never in band 1; Lôi Kiếp Đài's creatures
   stay in their arena.
5. The boss has a body with a picture and a group shield (its own or that of `stats_from`).
6. A deeper band never fields fewer creatures than the band before it.
7. A rift fields something in every band wherever it may open (every khu anchor of every rift
   zone, and outside any khu).
8. Loot: `loot.validate` counts every creature any band or rift may field in the bí cảnh's cap
   (`realm_quai.fielded`); a chest's `treasures` must be part of its table.

## Adding a bí cảnh or a band row

Write its `quai` block (copy one above), run `python tools/check_all.py` and
`pytest tests/test_realm_quai.py`. A new land's creatures reach the rift on their own once the land
is in `rift.zones` and its map has `monster_area`s.

## Hầm ngục and thủ thành

Looked at, left alone: the hầm ngục's guardians and wardens are names and flavour only (no
creature is fielded, `data/math/dungeon.json`); the thủ thành has one level whose waves are its
own board creatures (`muc_con`...: ink, matching its "cổng mực" story) and asks every tower's
question at the player's own floor, so there is nothing to distribute by theme or band yet.
