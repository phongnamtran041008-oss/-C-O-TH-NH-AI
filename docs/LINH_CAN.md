# Linh căn (spirit roots)

Every cultivator carries one linh căn. It is tested at the Trắc Linh Thạch (the first test is free),
re-rolled with tẩy linh pills brewed at the furnace, and it changes how the player fights, learns and
brews. Data: `server/data/linh_can.json`; rules: `server/app/systems/linh_can.py`; routes:
`server/app/routers/linh_can_routes.py` (`docs/API.md`); client: `client/scenes/linh_can.py` (Trắc Linh Đài,
key C, HUD button Linh Căn); tests: `server/tests/test_linh_can.py`, `client/tests/test_linh_can_flow.py`.
`tools/check_all.py` runs `linh_can.validate()`.

## The design

* **Nine giai**, low to high: Phàm giai (`pham`, #C9C4B8), Hoàng giai (`hoang`, #C9A44A), Huyền giai (`huyen`, #4F8FD8), Địa giai (`dia`, #9B5FD0), Thiên giai (`thien`, #F2C230), Thánh giai (`thanh`, #FFE9A8), Tiên giai (`tien`, #5CE1E6), Thần giai (`than`, #FF6A3D), Hỗn Độn giai (`hon_don`, #A77BFF).
* **52 roots**: Phàm giai 9, Hoàng giai 8, Huyền giai 8, Địa giai 7, Thiên giai 6, Thánh giai 5, Tiên giai 4, Thần giai 3, Hỗn Độn giai 2. The taxonomy of the novels: tạp linh căn (many thin elements), tam and song linh căn, đơn linh căn
  named after the thiên can (Canh Kim, Ất Mộc, Nhâm Thủy, Bính Hỏa, Mậu Thổ), thiên linh căn, biến dị
  linh căn (lôi, băng, phong), dị linh căn (quang, ám, không gian, thời gian), special bodies (kiếm cốt,
  đan thể, ngự thú, trận đạo, kim thân), tuệ căn, and the đạo căn at the top (Hỗn Độn, Hồng Mông).
* **Every root does something different.** The first effect of a root is its primary one; no two roots of
  one giai share it. A higher giai means bigger numbers and more effects: one effect at Phàm giai, eight at
  Hỗn Độn giai. Values: base x giai scale (1.0, 1.4, 1.8, 2.3, 2.9, 3.6, 4.4, 5.3, 6.5) x weight of the slot
  (1.0, 0.6, 0.5, 0.4, 0.35...; Hỗn Độn 1.0, 0.8, 0.7...), each under its type cap; the JSON holds the
  resulting numbers and is the only source of truth.
* **Effects reach the live world through the stats.** `cultivation.current_stats()` ends with
  `linh_can.apply_stats()`: the % stat effects multiply công, thủ, sinh lực, linh lực after gear and the worn
  pet, bạo kích adds points, every other effect rides in `stats.lc_fx`, and `stats.lc` is the giai index (0 =
  none). The realtime `Player` keeps `stats` from the moment it joins (`world._load_combat`) and whenever the
  root changes (`linh_can._after_change` -> `cultivation.push_to_world`), so the tick reads `linh_can.fx(p,
  type)` without the database. The database side (quiz, alchemy, death penalty) reads `linh_can.value_db()`.
* **Gacha by pills.** Each tẩy linh pill has its own odds over the giai; better pills shift them upward. The
  player's cultivation realm (`Character.realm`/`realm_stage`, the axis of `systems/loot.py`) caps the giai;
  a roll above the cap is drawn again inside it (odds renormalised; a pill that cannot reach that low lands on
  the cap). Pity: after `every - 1` rolls in a row below the pill's floor, the next roll is at least the floor
  (clipped to the cap); a roll at or above the floor resets the count. The odds shown to the player are the
  capped ones; the giai ladder shows which giai are locked and the tu vi that opens them.
* **First awakening.** No row in `linh_can` = chưa trắc linh. `POST /linh-can/awaken` is free once (its own
  odds, capped too). Lộ Trình has the optional step `g_linh_can` (check type `linh_can`).
* **Keep or take.** A pill roll stores the new root as `pending`; the player keeps the old one or takes the
  new one (`POST /linh-can/choose`) before the next roll. A roll that gives the root already carried is kept
  at once (no choice to make). Every root revealed goes into the đồ giám (`discovered`).
* **The pills are brewed**, never bought: each has a recipe in `recipes.json` (đan phương `dp_*` sold on the
  library shelf of Tàng Thư Các, a fee, a `min_realm`) and materials dropped by the land monsters (and Tẩy
  Linh Thảo also at Bà Chủ Sạp). Every new item has a tier in `loot_tiers.json`. They cannot be used from the
  bag (`/inventory/use` answers `linh_can_pill`).

## Caps by cultivation realm

| From | Highest giai |
|---|---|
| Phàm Nhân | Huyền giai |
| Luyện Khí tầng 4 | Địa giai |
| Luyện Khí tầng 7 | Thiên giai |
| Trúc Cơ sơ kỳ | Thánh giai |
| Kết Đan sơ kỳ | Tiên giai |
| Nguyên Anh sơ kỳ | Thần giai |
| Hóa Thần sơ kỳ | Hỗn Độn giai |

## The pills

| Pill | Recipe | Min realm | Fee | Materials | Phàm giai | Hoàng giai | Huyền giai | Địa giai | Thiên giai | Thánh giai | Tiên giai | Thần giai | Hỗn Độn giai | Pity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tẩy Linh Đan (`tay_linh_dan`) | `dp_tay_linh` | luyen_khi | 30 | Tẩy Linh Thảo x3, Trúc Diệp Thảo x2, Mực Tinh x2 | 40% | 30% | 18% | 8% | 3% | 0.8% | 0.15% | 0.04% | 0.01% | 10 -> Huyền giai |
| Tẩy Tủy Đan (`tay_tuy_dan`) | `dp_tay_tuy` | luyen_khi | 80 | Linh Tủy Tinh x2, Tẩy Linh Thảo x3, Mặc Linh Chi x1 | 15% | 30% | 28% | 16% | 7% | 3% | 0.8% | 0.15% | 0.05% | 10 -> Địa giai |
| Thiên Linh Đan (`thien_linh_dan`) | `dp_thien_linh` | truc_co | 300 | Thiên Linh Quả x3, Linh Tủy Tinh x3, Tẩy Linh Thảo x4 | - | 10% | 25% | 30% | 20% | 10% | 4% | 0.8% | 0.2% | 10 -> Thiên giai |
| Tạo Hóa Đan (`tao_hoa_dan`) | `dp_tao_hoa` | kim_dan | 1000 | Lôi Kiếp Tinh Hạch x2, Thiên Linh Quả x4, Linh Tủy Tinh x4, Mặc Linh Chi x3 | - | - | 10% | 25% | 30% | 20% | 10% | 4% | 1% | 10 -> Thánh giai |
| Hỗn Độn Khai Thiên Đan (`khai_thien_dan`) | `dp_khai_thien` | hoa_than | 4000 | Hỗn Độn Thạch x2, Lôi Kiếp Tinh Hạch x3, Thiên Linh Quả x6 | - | - | - | 10% | 25% | 30% | 20% | 11% | 4% | 8 -> Tiên giai |
| First test (free) | - | - | - | - | 50% | 32% | 15% | 3% | - | - | - | - | - | - |

Where the materials drop (`server/data/math/monsters.json`, tier in `loot_tiers.json`):

* Hỗn Độn Thạch (`hon_don_thach`, from Luyện Khí tầng 9): Thiên Kiếp Lôi Long 12%
* Linh Tủy Tinh (`linh_tuy_tinh`, from Luyện Khí tầng 3): Ma Trận Thú 30%, Phong Lang 30%, Hồ Lô Tinh 30%, Mộc Yêu 30%
* Lôi Kiếp Tinh Hạch (`loi_kiep_tinh_hach`, from Luyện Khí tầng 8): Ma Trận Thú 4%, Thiên Kiếp Lôi Long 60%
* Mặc Linh Chi (`mac_linh_chi`, from Luyện Khí tầng 3): Lân Hỏa Yêu 8%, Mặc Hồ 50%, Mặc Ảnh 15%, Phong Lang 40%, Hồ Lô Tinh 40%, Tâm Ma 20%
* Mực Tinh (`muc_tinh`, from Phàm Nhân): Mực Con 50%, Lân Hỏa Yêu 60%, Mặc Hồ 100%, Mặc Ảnh 60%, Bút Yêu 70%, Nghiên Ma 100%, Ảnh Trùng Ma 30%, Bình Phương Ma 20%, Mô Đun Ma 35%, Chuyển Vị Ma 25%, Đối Xứng Ma 40%, Kiếm Linh 30%, Vân Xà 30%, Đầu Tử Oa 45%, Tri Chu Tinh 30%, Cơ Quan Nhân 40%
* Tẩy Linh Thảo (`tay_linh_thao`, from Luyện Khí tầng 1): Vân Xà 25%, Đầu Tử Oa 25%, Tri Chu Tinh 25%, Tâm Ma 20%
* Thiên Linh Quả (`thien_linh_qua`, from Luyện Khí tầng 6): Cơ Quan Nhân 6%, Cơ Quan Nhân Đầu Đàn 25%, Tâm Ma Chấp Niệm 25%
* Trúc Diệp Thảo (`truc_diep_thao`, from Phàm Nhân): Mực Con 30%, Lân Hỏa Yêu 30%, Vân Xà 45%, Tâm Ma 40%

## Effect types and where the server applies them

| Type | Unit | Cap | Text | Applied in |
|---|---|---|---|---|
| `atk_pct` | pct | 0.25 | Công +{v} | `systems/linh_can.apply_stats (cultivation.current_stats)` |
| `def_pct` | pct | 0.25 | Thủ +{v} | `systems/linh_can.apply_stats (cultivation.current_stats)` |
| `hp_pct` | pct | 0.25 | Sinh Lực tối đa +{v} | `systems/linh_can.apply_stats (cultivation.current_stats)` |
| `qi_pct` | pct | 0.3 | Linh Lực tối đa +{v} | `systems/linh_can.apply_stats (cultivation.current_stats)` |
| `crit` | point | 8.0 | Bạo kích +{v} | `systems/linh_can.apply_stats (cultivation.current_stats)` |
| `xp_pct` | pct | 0.2 | Tu Vi từ câu trả lời đúng +{v} | `learning/quiz.answer (Tu Vi of a right answer)` |
| `q_time` | sec | 4.0 | Mỗi câu hỏi thêm {v} để nghĩ | `learning/quiz.create_session (question time limit)` |
| `basic_dmg` | pct | 0.3 | Đòn thường +{v} sát thương | `realtime/combat.attack (a normal hit)` |
| `parry_dmg` | pct | 0.3 | Phản Đòn +{v} sát thương | `realtime/combat._parry (the counter hit)` |
| `stun_pct` | pct | 0.4 | Phản Đòn làm quái choáng lâu hơn {v} | `realtime/combat._parry (the stun)` |
| `qi_gain` | pct | 0.6 | Phản Đòn hồi thêm {v} Linh Lực | `realtime/combat._parry (linh lực gained)` |
| `heal_right` | pct | 0.06 | Phản Đòn hồi {v} Sinh Lực tối đa | `realtime/combat._parry (healed on a Phản Đòn)` |
| `wrong_guard` | pct | 0.3 | Trả lời sai: đòn trúng nhẹ đi {v} | `realtime/combat._parry (the blow of a wrong answer)` |
| `dodge_cd` | pct | 0.25 | Né Đòn hồi nhanh hơn {v} | `realtime/combat.dodge_cooldown` |
| `qi_regen` | pct | 0.7 | Linh Lực tự hồi nhanh hơn {v} | `realtime/combat.tick (linh lực regeneration)` |
| `death_guard` | pct | 0.45 | Tử vong mất ít Tu Vi hơn {v} | `realtime/combat._death_penalty` |
| `drop_luck` | pct | 0.3 | Quái rơi đồ nhiều hơn {v} | `realtime/combat._loot_bonus (drop_mult)` |
| `stones_pct` | pct | 0.35 | Linh thạch từ quái +{v} | `realtime/combat._loot_bonus (stones_pct)` |
| `chieu_kim` | pct | 0.3 | Chiêu hệ Kim +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_moc` | pct | 0.3 | Chiêu hệ Mộc +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_thuy` | pct | 0.3 | Chiêu hệ Thủy +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_hoa` | pct | 0.3 | Chiêu hệ Hỏa +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_tho` | pct | 0.3 | Chiêu hệ Thổ +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_loi` | pct | 0.3 | Chiêu hệ Lôi +{v} sát thương | `systems/math_skills._land (chiêu damage by element)` |
| `chieu_cd` | pct | 0.2 | Chiêu thức hồi nhanh hơn {v} | `systems/math_skills (cooldown of a cast)` |
| `qi_cost` | pct | 0.25 | Chiêu thức tốn ít Linh Lực hơn {v} | `systems/math_skills (linh lực of a cast)` |
| `glide_cd` | pct | 0.3 | Đạp Kiếm Lướt hồi nhanh hơn {v} | `realtime/abilities.request_glide (Đạp Kiếm Lướt cooldown)` |
| `tran_time` | pct | 0.4 | Pháp trận đứng lâu hơn {v} | `realtime/abilities.place_formation (how long the formation stands)` |
| `tame` | count | 2 | Thu phục linh thú bớt {v} lần Phản Đòn | `realtime/beasts.on_parry (Phản Đòn needed to tame)` |
| `alchemy_zone` | count | 6 | Luyện đan: vùng văn hỏa rộng thêm {v} | `systems/alchemy.start (văn hỏa zone width)` |
| `alchemy_extra` | pct | 0.15 | Luyện đan: thêm {v} cơ hội ra dư một viên | `systems/alchemy.finish (chance of one more pill)` |

## Every root

| Giai | Root | Hệ | Loại | Effects (primary first) |
|---|---|---|---|---|
| Phàm giai | Ngũ Hành Tạp Linh Căn (`ngu_hanh_tap`) | Kim, Mộc, Thủy, Hỏa, Thổ | Tạp linh căn | Sinh Lực tối đa +3% |
| Phàm giai | Tứ Linh Căn (`tu_linh_can`) | Kim, Mộc, Thủy, Thổ | Tạp linh căn | Thủ +3% |
| Phàm giai | Phế Linh Căn (`phe_linh_can`) | - | Phế linh căn | Tu Vi từ câu trả lời đúng +2% |
| Phàm giai | Kim Thổ Tạp Linh Căn (`kim_tho_tap`) | Kim, Thổ | Tạp linh căn | Công +3% |
| Phàm giai | Thủy Mộc Tạp Linh Căn (`thuy_moc_tap`) | Thủy, Mộc | Tạp linh căn | Linh Lực tự hồi nhanh hơn 10% |
| Phàm giai | Hỏa Thổ Tạp Linh Căn (`hoa_tho_tap`) | Hỏa, Thổ | Tạp linh căn | Trả lời sai: đòn trúng nhẹ đi 3% |
| Phàm giai | Vi Hỏa Linh Căn (`vi_hoa_linh_can`) | Hỏa | Đơn linh căn | Chiêu hệ Hỏa +4% sát thương |
| Phàm giai | Vi Thủy Linh Căn (`vi_thuy_linh_can`) | Thủy | Đơn linh căn | Chiêu hệ Thủy +4% sát thương |
| Phàm giai | Hậu Thổ Phàm Căn (`hau_tho_pham_can`) | Thổ | Tạp linh căn | Tử vong mất ít Tu Vi hơn 6% |
| Hoàng giai | Kim Mộc Thủy Tam Linh Căn (`kim_moc_thuy_tam`) | Kim, Mộc, Thủy | Tam linh căn | Linh Lực tối đa +6%; Chiêu hệ Thủy +3% sát thương |
| Hoàng giai | Hỏa Thổ Kim Tam Linh Căn (`hoa_tho_kim_tam`) | Hỏa, Thổ, Kim | Tam linh căn | Công +4%; Thủ +3% |
| Hoàng giai | Mộc Hỏa Thổ Tam Linh Căn (`moc_hoa_tho_tam`) | Mộc, Hỏa, Thổ | Tam linh căn | Sinh Lực tối đa +4%; Chiêu hệ Mộc +3% sát thương |
| Hoàng giai | Thủy Mộc Thổ Tam Linh Căn (`thuy_moc_tho_tam`) | Thủy, Mộc, Thổ | Tam linh căn | Phản Đòn hồi 1% Sinh Lực tối đa |
| Hoàng giai | Vi Lôi Linh Căn (`vi_loi_linh_can`) | Lôi | Biến dị linh căn | Chiêu hệ Lôi +6% sát thương |
| Hoàng giai | Vi Kim Linh Căn (`vi_kim_linh_can`) | Kim | Đơn linh căn | Chiêu hệ Kim +6% sát thương; Bạo kích +1 điểm |
| Hoàng giai | Tụ Tài Linh Căn (`tu_tai_linh_can`) | Thổ, Kim | Dị linh căn | Linh thạch từ quái +7% |
| Hoàng giai | Tĩnh Tâm Linh Căn (`tinh_tam_linh_can`) | Thủy | Tuệ căn | Mỗi câu hỏi thêm 0.5 giây để nghĩ |
| Huyền giai | Thủy Mộc Song Linh Căn (`thuy_moc_song`) | Thủy, Mộc | Song linh căn | Linh Lực tự hồi nhanh hơn 18%; Chiêu hệ Thủy +4% sát thương |
| Huyền giai | Kim Hỏa Song Linh Căn (`kim_hoa_song`) | Kim, Hỏa | Song linh căn | Đòn thường +7% sát thương; Chiêu hệ Hỏa +4% sát thương |
| Huyền giai | Thổ Kim Song Linh Căn (`tho_kim_song`) | Thổ, Kim | Song linh căn | Thủ +5%; Trả lời sai: đòn trúng nhẹ đi 3% |
| Huyền giai | Mộc Hỏa Song Linh Căn (`moc_hoa_song`) | Mộc, Hỏa | Song linh căn | Luyện đan: vùng văn hỏa rộng thêm 2; Chiêu hệ Hỏa +4% sát thương |
| Huyền giai | Thủy Thổ Song Linh Căn (`thuy_tho_song`) | Thủy, Thổ | Song linh căn | Sinh Lực tối đa +5%; Tử vong mất ít Tu Vi hơn 6% |
| Huyền giai | Tầm Bảo Linh Căn (`tam_bao_linh_can`) | Thổ, Kim | Dị linh căn | Quái rơi đồ nhiều hơn 7%; Linh thạch từ quái +5% |
| Huyền giai | Khinh Thân Linh Căn (`khinh_than_linh_can`) | Mộc | Dị linh căn | Né Đòn hồi nhanh hơn 5%; Đạp Kiếm Lướt hồi nhanh hơn 4% |
| Huyền giai | Ngự Thú Linh Căn (`ngu_thu_linh_can`) | Mộc | Đặc thù thể chất | Thu phục linh thú bớt 1 lần Phản Đòn; Phản Đòn hồi thêm 9% Linh Lực |
| Địa giai | Canh Kim Linh Căn (`canh_kim_linh_can`) | Kim | Đơn linh căn | Chiêu hệ Kim +9% sát thương; Bạo kích +1.5 điểm |
| Địa giai | Ất Mộc Linh Căn (`at_moc_linh_can`) | Mộc | Đơn linh căn | Chiêu hệ Mộc +9% sát thương; Phản Đòn hồi 1% Sinh Lực tối đa |
| Địa giai | Nhâm Thủy Linh Căn (`nham_thuy_linh_can`) | Thủy | Đơn linh căn | Chiêu hệ Thủy +9% sát thương; Linh Lực tối đa +6% |
| Địa giai | Bính Hỏa Linh Căn (`binh_hoa_linh_can`) | Hỏa | Đơn linh căn | Chiêu hệ Hỏa +9% sát thương; Đòn thường +6% sát thương |
| Địa giai | Mậu Thổ Linh Căn (`mau_tho_linh_can`) | Thổ | Đơn linh căn | Chiêu hệ Thổ +9% sát thương; Thủ +4%; Sinh Lực tối đa +3% |
| Địa giai | Đan Tâm Linh Căn (`dan_tam_linh_can`) | Hỏa, Mộc | Đặc thù thể chất | Luyện đan: thêm 5% cơ hội ra dư một viên; Luyện đan: vùng văn hỏa rộng thêm 1 |
| Địa giai | Trận Đạo Linh Căn (`tran_dao_linh_can`) | Thổ | Đặc thù thể chất | Pháp trận đứng lâu hơn 14%; Phản Đòn làm quái choáng lâu hơn 7% |
| Thiên giai | Thiên Lôi Linh Căn (`thien_loi_linh_can`) | Lôi | Biến dị linh căn | Chiêu hệ Lôi +12% sát thương; Phản Đòn +7% sát thương; Bạo kích +1.5 điểm |
| Thiên giai | Huyền Băng Linh Căn (`huyen_bang_linh_can`) | Băng | Biến dị linh căn | Phản Đòn làm quái choáng lâu hơn 14%; Chiêu hệ Thủy +7% sát thương; Trả lời sai: đòn trúng nhẹ đi 4% |
| Thiên giai | Thanh Phong Linh Căn (`thanh_phong_linh_can`) | Phong | Biến dị linh căn | Né Đòn hồi nhanh hơn 9%; Đạp Kiếm Lướt hồi nhanh hơn 7%; Chiêu hệ Mộc +6% sát thương |
| Thiên giai | Liệt Hỏa Thiên Linh Căn (`liet_hoa_thien_linh_can`) | Hỏa | Thiên linh căn | Chiêu hệ Hỏa +12% sát thương; Công +5%; Chiêu thức tốn ít Linh Lực hơn 4% |
| Thiên giai | Tiên Thiên Kiếm Cốt (`tien_thien_kiem_cot`) | Kim | Đặc thù thể chất | Đòn thường +12% sát thương; Phản Đòn +7% sát thương; Bạo kích +1.5 điểm |
| Thiên giai | Ngộ Đạo Tuệ Căn (`ngo_dao_tue_can`) | - | Tuệ căn | Tu Vi từ câu trả lời đúng +6%; Mỗi câu hỏi thêm 1 giây để nghĩ |
| Thánh giai | Thánh Quang Linh Căn (`thanh_quang_linh_can`) | Quang | Dị linh căn | Phản Đòn hồi 4% Sinh Lực tối đa; Sinh Lực tối đa +6%; Trả lời sai: đòn trúng nhẹ đi 5% |
| Thánh giai | U Minh Ám Linh Căn (`u_minh_am_linh_can`) | Ám | Dị linh căn | Bạo kích +3.5 điểm; Phản Đòn +9% sát thương; Tử vong mất ít Tu Vi hơn 11% |
| Thánh giai | Vạn Thú Thánh Căn (`van_thu_thanh_can`) | Mộc, Thổ | Đặc thù thể chất | Thu phục linh thú bớt 1 lần Phản Đòn; Phản Đòn hồi thêm 17% Linh Lực; Quái rơi đồ nhiều hơn 7% |
| Thánh giai | Thiên Đan Thánh Thể (`thien_dan_thanh_the`) | Hỏa, Mộc | Đặc thù thể chất | Luyện đan: thêm 7% cơ hội ra dư một viên; Luyện đan: vùng văn hỏa rộng thêm 2; Tu Vi từ câu trả lời đúng +4% |
| Thánh giai | Bất Diệt Kim Thân (`bat_diet_kim_than`) | Kim, Thổ | Đặc thù thể chất | Thủ +11%; Sinh Lực tối đa +6%; Tử vong mất ít Tu Vi hơn 11% |
| Tiên giai | Không Gian Linh Căn (`khong_gian_linh_can`) | Không Gian | Dị linh căn | Đạp Kiếm Lướt hồi nhanh hơn 18%; Né Đòn hồi nhanh hơn 8%; Pháp trận đứng lâu hơn 13%; Chiêu thức tốn ít Linh Lực hơn 5% |
| Tiên giai | Thời Gian Linh Căn (`thoi_gian_linh_can`) | Thời Gian | Dị linh căn | Mỗi câu hỏi thêm 2 giây để nghĩ; Chiêu thức hồi nhanh hơn 7%; Phản Đòn làm quái choáng lâu hơn 11%; Tu Vi từ câu trả lời đúng +4% |
| Tiên giai | Tiên Thiên Đạo Thể (`tien_thien_dao_the`) | - | Đạo căn | Tu Vi từ câu trả lời đúng +9%; Linh Lực tối đa +11%; Linh Lực tự hồi nhanh hơn 22%; Sinh Lực tối đa +5% |
| Tiên giai | Vạn Kiếm Quy Tông Kiếm Cốt (`van_kiem_kiem_cot`) | Kim | Đặc thù thể chất | Đòn thường +18% sát thương; Phản Đòn +11% sát thương; Bạo kích +2 điểm; Chiêu hệ Kim +7% sát thương |
| Thần giai | Tử Tiêu Thần Lôi Căn (`tu_tieu_than_loi_can`) | Lôi | Biến dị linh căn | Chiêu hệ Lôi +21% sát thương; Phản Đòn +13% sát thương; Phản Đòn làm quái choáng lâu hơn 13%; Bạo kích +2 điểm; Công +6% |
| Thần giai | Âm Dương Thần Căn (`am_duong_than_can`) | Quang, Ám | Đạo căn | Phản Đòn hồi 5% Sinh Lực tối đa; Trả lời sai: đòn trúng nhẹ đi 10%; Bạo kích +2.5 điểm; Linh Lực tự hồi nhanh hơn 21%; Tử vong mất ít Tu Vi hơn 11% |
| Thần giai | Ngũ Hành Thần Căn (`ngu_hanh_than_can`) | Kim, Mộc, Thủy, Hỏa, Thổ | Đạo căn | Chiêu hệ Kim +13% sát thương; Chiêu hệ Mộc +13% sát thương; Chiêu hệ Thủy +13% sát thương; Chiêu hệ Hỏa +13% sát thương; Chiêu hệ Thổ +13% sát thương; Chiêu thức tốn ít Linh Lực hơn 6% |
| Hỗn Độn giai | Hỗn Độn Linh Căn (`hon_don_linh_can`) | Hỗn Độn | Đạo căn | Tu Vi từ câu trả lời đúng +13%; Công +16%; Thủ +14%; Sinh Lực tối đa +12%; Linh Lực tối đa +13%; Chiêu thức hồi nhanh hơn 8%; Chiêu thức tốn ít Linh Lực hơn 10%; Quái rơi đồ nhiều hơn 13% |
| Hỗn Độn giai | Hồng Mông Đạo Căn (`hong_mong_dao_can`) | Hỗn Độn | Đạo căn | Phản Đòn +26% sát thương; Trả lời sai: đòn trúng nhẹ đi 16%; Mỗi câu hỏi thêm 2.5 giây để nghĩ; Tử vong mất ít Tu Vi hơn 23%; Phản Đòn hồi 3% Sinh Lực tối đa; Linh thạch từ quái +16%; Luyện đan: thêm 7% cơ hội ra dư một viên; Thu phục linh thú bớt 2 lần Phản Đòn |

## Art

The scene loads three families of FX through `art2.fx()` and falls back while they are missing:
`linh_can_<1..9>` (one-shot reveal burst of a giai; fallback `dot_pha`), `linh_can_tru_<1..9>` (looping light
pillar; fallback `aura_<realm>_back/front`), `trac_linh_thach` (the stone, looping; fallback the props
`pedestal_lit` + `crystal_2`). None of these ids is named in `wiring.json` until the sheets are on disk.
The players' entity record carries `lc` (giai index) for a coloured mark (`docs/PROTOCOL.md`).
