# API REST

Mọi endpoint trừ `/auth/register`, `/auth/login`, `/auth/reset_password`, `/server/info` cần header
`Authorization: Bearer <token>`. Lỗi luôn có dạng:

```json
{"error": {"code": "not_due", "message_vi": "Chưa đến giờ ôn, còn 412 giây nữa."}}
```

`message_vi` hiển thị thẳng cho người chơi; `code` để client xử lý.

## Tài khoản

| Method | Đường dẫn | Body | Trả về |
|---|---|---|---|
| POST | `/auth/register` | `{username, password}` | `{token, user_id, recovery_code}` — mã khôi phục chỉ hiện **một lần** |
| POST | `/auth/login` | `{username, password}` | `{token, user_id}` |
| POST | `/auth/reset_password` | `{username, recovery_code, new_password}` | `{token, recovery_code}` (mã mới) |
| POST | `/auth/change_password` | `{old_password, new_password}` | `{token}` |
| POST | `/auth/logout_all` | — | đăng xuất mọi thiết bị |
| GET | `/server/info` | — | phiên bản giao thức, giờ server, `time_scale`, thông báo bảo trì (chi tiết ở mục Giai đoạn 10) |
| GET | `/me` | — | Linh Thạch, Tiên Ngọc, lượt quay còn lại hôm nay |

## Gacha

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/gacha/banners` | — | tỉ lệ gốc, tỉ lệ thực tế có pity, bộ đếm pity của bạn |
| POST | `/gacha/roll` | `{banner: "bees"\|"pets", count: 1\|10, free: false, currency}` | lượt miễn phí mỗi ngày dùng ở `free_roll_banner` (Trứng Ong) |

## Câu hỏi (dùng chung cho mọi hệ thống)

Mọi chế độ hỏi câu toán qua cùng một dịch vụ phiên câu hỏi (`server/app/learning/quiz.py`). Câu hỏi trả về có dạng:

```json
{"session_id": "…", "context": "math", "qtype": "multiple_choice", "instruction_vi": "Chọn đáp án đúng",
 "prompt": {"text": "…"}, "input": "choice",
 "options": [{"id": "a", "text": "…"}, {"id": "b", "text": "…"}, …],
 "time_limit": 30.0, "math": {"subject": "…", "skill": "…", "floor": 1, "tier": 1, …},
 "expires_at": "…Z", "server_time": "…Z"}
```

`context` là chế độ đã hỏi (`math`, `math_combat`, `math_td`, `math_fishing`, `math_realm`, `math_skill`,
`math_dungeon`, `math_fortune`, `math_placement`, `math_meditate`, `math_tribulation`). Các loại câu (`qtype`),
cách trả lời của từng `input` và khối `math`: mục **M2: vòng câu hỏi toán** bên dưới.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| POST | `/quiz/answer` | `{session_id, answer}` | `{correct, timed_out, correct_option, reveal, …}` + kết quả theo ngữ cảnh (vd `math`, `combat`, `fishing`, `xp`) |

Đáp án không bao giờ nằm trong câu hỏi; chỉ được tiết lộ trong kết quả `/quiz/answer`. Mỗi câu chỉ trả lời
được một lần; quá hạn tính là sai. Máy chủ chỉ hỏi loại câu đã đăng ký cách chấm (`quiz.register_grader`).

## Giai đoạn 2

### Nhân vật và hướng dẫn

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/character/options` | — | màu tóc, kiểu tóc, dáng người được phép |
| POST | `/character/create` | `{display_name, appearance: {hair_color, hair_style, body}}` | 1 tài khoản 1 nhân vật; tên qua bộ lọc từ cấm |
| GET | `/character` | — | cảnh giới, vị trí, ngoại hình, trang phục |
| POST | `/character/position` | `{zone_id: "abode", x, y, facing}` | lưu vị trí trong động phủ |
| POST | `/tutorial` | `{step}` | bước hướng dẫn (chỉ tăng) |

`GET /me` có thêm `has_character`, `tutorial_step`, `daily_rolls_left`, `free_rolls_left`.

## Giai đoạn 3

Thế giới thời gian thực (đi lại, kênh, chat) đi qua WebSocket `/ws`: xem `docs/PROTOCOL.md`.

### Bạn bè, chặn, báo cáo

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/friends` | — | `{friends[], incoming[], outgoing[], max}`; mỗi người: `user_id`, `display_name`, `realm`, `online`, `zone_id`, `zone_name` |
| POST | `/friends/request` | `{display_name}` | gửi lời mời; nếu người kia đã mời mình thì thành bạn luôn |
| POST | `/friends/accept` | `{user_id}` | đồng ý lời mời của `user_id` |
| POST | `/friends/decline` | `{user_id}` | từ chối |
| POST | `/friends/remove` | `{user_id}` | hủy kết bạn (cả hai phía) |
| GET | `/blocks` | — | danh sách đã chặn |
| POST | `/blocks` | `{user_id}` | chặn (đồng thời hủy kết bạn; tin nhắn của người đó không đến nữa) |
| POST | `/blocks/remove` | `{user_id}` | bỏ chặn |
| POST | `/reports` | `{user_id, message, reason}` | báo cáo người chơi (tối đa 20 lần/ngày) |

### Máy chủ

| Method | Đường dẫn | Ghi chú |
|---|---|---|
| GET | `/server/stats` | số người online, kênh, thời gian tick (trung bình, p99, lớn nhất) và độ trễ tick; dùng cho `tools/load_bots.py` |

`POST /character/position` (động phủ) bị bỏ qua (`{"ok": false, "ignored": "in_world"}`) khi nhân vật đang đứng
trong thế giới chung, để một lần lưu đến muộn không kéo nhân vật về động phủ.

## Giai đoạn 4

Chiến đấu diễn ra qua WebSocket (`atk`, `skill`, câu hỏi `q`, xem `docs/PROTOCOL.md`); câu hỏi chiến đấu vẫn trả lời
bằng `POST /quiz/answer`, kết quả có thêm `combat`:
`{correct: true, shield_broken, damage, crit}` hoặc `{correct: false, mac_kich, hp, dead}`.

Mọi câu trả lời đúng có thêm `xp`: `{gained, xp, need, realm, stage, stage_up, bottleneck}` (Tu Vi theo ngữ cảnh,
số trong `balance/cultivation.json` → `xp_per_correct`).

### Tu luyện và Thiên Kiếp

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/cultivation` | — | `realm`, `realm_name`, `stage`, `label`, `xp`, `need`, `next_realm`, `pill`, `pill_name`, `has_pill`, `can_tribulation`, `tribulation_ready_in`, `stats` {`max_hp`, `max_qi`, `atk`, `def`, `crit`, `ink_res`, `weapon`}, `skills[]` |
| POST | `/cultivation/meditate` | — | một câu đả tọa (ngữ cảnh `meditate`), chỉ trong động phủ, mỗi 2 phút một câu. Lỗi: `not_home`, `meditate_wait`, `nothing_learned` |
| POST | `/cultivation/breakthrough/start` | — | bắt đầu (hoặc tiếp tục) Thiên Kiếp: `{question, resumed}`; câu có `number`, `total`. Lỗi: `no_tribulation`, `xp_not_full`, `no_pill`, `tribulation_wait` |

Thiên Kiếp: trả lời từng câu bằng `/quiz/answer`; kết quả có `next` (câu kế) cho tới câu 20, câu cuối có
`tribulation`: `{passed, correct, total, pass_pct}` + khi qua `{realm, label, jade}`, khi trượt `{xp_lost, retry_in}`; mỗi câu có `number`, `total`, `correct_so_far`. Câu quá hạn tính là sai; thoát
giữa chừng rồi gọi lại `start` thì tiếp tục từ câu đang dở.

### Túi đồ, trang bị, lò rèn

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/inventory` | — | `items[]` {`item_id`, `name_vi`, `kind`, `qty`, `desc_vi`, `usable`, `sell_price`}, `equipment[]` {`id`, `item_id`, `name_vi`, `slot`, `slot_vi`, `rarity`, `rarity_vi`, `color`, `enhance`, `stats`, `equipped`, `next_enhance`} |
| POST | `/inventory/use` | `{item_id}` | đan dược (chỉ khi đang ở thế giới chung; lỗi `not_in_world`, `pill_cooldown`) |
| POST | `/equipment/equip` | `{instance_id}` | mặc vào ô của món đó (món cũ tự tháo); trả `stats` mới |
| POST | `/equipment/unequip` | `{slot}` | tháo |
| POST | `/forge/enhance` | `{instance_id}` | `{success, item, spirit_stones, stats}`; thất bại chỉ mất nguyên liệu và Linh Thạch. Lỗi: `max_level`, `no_material`, `insufficient_funds` |

### Nhiệm vụ và Yêu Quái Phổ

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/quests` | — | `quests[]` {`id`, `chain`, `chain_vi`, `title_vi`, `desc_vi`, `state` (`active` \| `done`), `objective` {`type`, `target`, `n`, `target_vi`}, `progress`, `rewards_vi[]`} |
| POST | `/quests/talk` | `{npc}` | nói chuyện với NPC (phải đứng gần trong thế giới; lỗi `too_far`) → `{finished[]}` |
| POST | `/quests/claim` | `{quest_id}` | nhận thưởng nhiệm vụ đã xong → `{claimed, rewards, next}`. Lỗi: `no_quest`, `not_done` |
| GET | `/codex/monster` | — | `{found, total, entries[]}`; quái chưa gặp chỉ có `id`, `sprite`, `found: false` |

## Giai đoạn 5 — Linh Phong (ong linh)

Ong hộ vệ đánh quái trong thế giới chung (xem `docs/PROTOCOL.md`); mọi thứ khác qua REST. Mật được **tính lười**:
mỗi lần mở tổ / đổi vai trò, server tính phần làm ra từ lần trước tới nay (nhân `TIME_SCALE`).

### Tổ ong

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/bees/species` | — | công khai: `{species: {id: {name_vi, rarity, rarity_vi, element, element_vi, skill, skill_vi, look, desc_vi}}}` (client vẽ ong của người khác) |
| GET | `/hive` | — | lần đầu tạo tổ và tặng 1 Trứng Ong Phàm. `level`, `level_max`, `cells`, `cells_max`, `columns`, `rows`, `open_cells[]` (ô theo thứ tự mở từ giữa ra), `next_cell` {`cell`, `spirit_stones`, `species_required`, `ok`}, `honey`, `wax`, `capacity`, `honey_per_hour`, `next_level` {chi phí, `capacity`, `honey_mult`, `decoration_vi`}, `decorations[]` {`id`, `name_vi`, `on`}, `bees[]`, `eggs[]` {`item_id`, `rarity`, `qty`}, `foods[]` {`food`, `name_vi`, `qty`}, `guard_slots`, `guard_used`, `species_found`, `species_total` |
| POST | `/hive/collect` | — | chuyển mật/sáp trong tổ (phần nguyên) vào túi: `{honey, wax, totals}`. Lỗi `no_honey` |
| POST | `/hive/hatch` | `{item_id}` | ấp một quả trứng: `{bee, new_species, milestones[]}`. Loài được chọn lúc nở (cùng độ hiếm, loài chưa có nặng gấp đôi). Lỗi `not_egg`, `no_egg`, `hive_full` |
| POST | `/hive/unlock_cell` | — | mở ô kế tiếp (Linh Thạch + mốc Ong Phổ). Lỗi `need_species`, `hive_max`, `insufficient_funds` |
| POST | `/hive/upgrade` | — | nâng cấp tổ (Linh Thạch, Sáp Ong, Gỗ Linh Mộc). Lỗi `no_material`, `hive_max_level` |
| POST | `/hive/decoration` | `{decoration, on}` | bật/tắt trang trí đã mở. Lỗi `decoration_locked` |

Mỗi ong trong `bees[]`: `id`, `species`, `name_vi`, `rarity`, `rarity_vi`, `rarity_color`, `element`, `element_vi`,
`level`, `xp`, `xp_next`, `bond`, `bond_max`, `role` (`hive` \| `guard`), `role_vi`, `slot`, `resonance_pct`,
`honey_per_hour`, `guard` {`hp`, `atk`, `cd`}, `skill`, `skill_vi`, `favorite_known`, `favorite`,
`favorite_hint_vi`, `look`, `desc_vi`.

### Ong

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| POST | `/bees/move` | `{bee_id, slot}` | đặt vào ô đã mở; ô có ong thì đổi chỗ. Trả lại `/hive`. Lỗi `cell_locked` |
| POST | `/bees/role` | `{bee_id, role}` | `hive` / `guard` (số ô theo cảnh giới: Phàm Nhân 0, Luyện Khí 2, Trúc Cơ 3, Kết Đan 4, Nguyên Anh 5, ... Đại Thừa 9). Lỗi `no_guard_slot`, `guard_full` |
| POST | `/bees/feed` | `{bee_id, food}` | `food` = món trong `balance/bees.json → feed` (`linh_mat`, `linh_qua`, `ca_nho`, linh thảo...), cá `fish_<loài>` hoặc đan cho ong → `{xp_gained, favorite, favorite_discovered, favorite_vi, levels_gained, level, xp, xp_next, bond, bond_gained}`. Món thích: kinh nghiệm ×2, thân thiết +8 (thường +2). Lỗi `no_food`, `bad_food` |
| POST | `/bees/release` | `{bee_id}` | thả ong, nhận Sáp Ong theo độ hiếm |
| GET | `/codex/bee` | — | Ong Phổ: `{found, total, entries[], milestones[]}`; loài chưa gặp chỉ có `id`, `rarity`, `found: false` |

### Gacha, túi đồ

- `POST /gacha/roll`: `banner: "bees"` mở; thêm `currency` (`spirit_stones` \| `immortal_jade`). Kết quả mỗi lượt
  `{rarity, item, name_vi, total}` (trứng vào túi). Lượt miễn phí mỗi ngày chỉ ở quầy Trứng Ong (`no_free_roll`).
- `POST /inventory/sell` `{item_id, qty}`: làng mua vật phẩm có `sell_price` (Linh Mật, Sáp Ong, Gỗ, Linh Quả, Mực Tinh).
  Lỗi `not_sellable`, `not_enough`.

## Giai đoạn 6 — Câu cá (mục 11)

Mọi kết quả do máy chủ quyết định. Một lượt câu: `cast` → (chờ `bite_in` giây) → `hook` → câu hỏi nếu cá từ Linh trở
lên (trả lời qua `/quiz/answer` như mọi câu khác, `context: "math_fishing"`) → chơi trò kéo cá → `reel`.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/fishing` | — | `{rod, bait, rods[], baits[], scales, conditions{zone, night, rain, hour}, casting}`. Lần đầu tặng Cần Trúc Thô. Mỗi cần: `id, name_vi, rarity, owned, equipped, level, stats{pull, line, luck, bite, zone}, price, min_realm, upgrade_cost`. Mỗi mồi: `id, name_vi, qty, buy, craft{from, makes, have}, equipped` |
| POST | `/fishing/equip` | `{rod?, bait?, no_bait?}` | chọn cần/mồi đang dùng. Lỗi `no_rod`, `no_bait` |
| POST | `/fishing/buy` | `{item_id, qty}` | mua cần (một lần) hoặc Giun Đất; phải đứng cạnh Ngư Ông. Lỗi `too_far`, `owned`, `not_sold`, `realm_too_low`, `not_enough` |
| POST | `/fishing/craft` | `{bait_id, times}` | Bánh Mật ← Linh Mật, Linh Quả Vụn ← Linh Quả, Mồi Mực ← Mực Tinh; cạnh Ngư Ông |
| POST | `/fishing/upgrade` | `{rod_id}` | nâng cần một cấp (tối đa 5) ở Lò Rèn (cạnh Thợ Rèn): Linh Thạch + Vảy Linh Ngư |
| POST | `/fishing/cast` | `{spot}` | `spot` = `abode` (ao động phủ, khi không đứng ngoài thế giới) \| `world` (máy chủ kiểm tra vị trí thật của nhân vật có sát mép nước). Dùng 1 mồi. → `{cast_id, bite_in, window, zone, pool, rod, bait, conditions, bait_left}`. Lỗi `not_here`, `no_bait`, `bait_needs_night`, `nothing_bites` |
| POST | `/fishing/hook` | `{cast_id}` | giật câu: `{stage: "early"}` (sớm), `"late"` (muộn), `"quiz"` + `{rarity, need, question}` hoặc `"reel"` + `{rarity, params, quiz_mult}`. Loài và kích thước chọn lúc này, không gửi cho client |
| POST | `/fishing/reel` | `{cast_id, toggles[]}` | `toggles`: các số bước (20 ms) mà nút đổi trạng thái, tăng dần, bắt đầu từ "nhả". Máy chủ chạy lại `fishing_sim.replay` → `{result: caught\|escaped\|snapped, steps}`; câu được thì thêm `fish{...}, size_cm, small, items[], new_species, personal_record, server_record, milestones[]`. Lỗi `too_fast` (nhanh hơn thời gian thật), `bad_input`, `no_cast`, `wrong_step` |
| POST | `/fishing/cancel` | — | thu cần |
| GET | `/codex/fish` | — | Ngư Phổ `{found, total, species[], milestones[]}`; loài chưa câu chỉ có `id, rarity, shape, hint_vi` |
| GET | `/fishing/records` | — | `{records: [{id, name_vi, rarity, top: [{name, size_cm, me}]}]}` — 3 con to nhất mỗi loài toàn máy chủ |
| GET | `/world/weather?zone=` | — | `{zone, night, rain, hour}` |

Khi trả lời câu hỏi câu cá, `/quiz/answer` có thêm `fishing`: `{stage: "quiz", next_question, right, need}` (cá Thiên
cần đúng 2 câu liên tiếp) hoặc `{stage: "reel", params, quiz_mult, right, need, rarity}`. Sai không bao giờ trừ máu.

`params` của trò kéo cá: `seed, zone, agility, range, seg_ms, gain, loss, start, lift, gravity, vmax, strain_up,
strain_down, max_ms` — đầu vào của `fishing_sim.Reel` (file giống hệt nhau ở `server/app/systems/` và `client/engine/`).
Cá câu được vào túi là `fish_<loài>` (bán được); cá Phàm quá nhỏ thành `ca_nho`; cá từ Linh trở lên cho `vay_linh_ngu`.

## Giai đoạn 7 — Tàng Thư Các (mục 9)

Thủ thành chỉ có Thủ Thành Toán
(`/math/td/*`, mục M10 bên dưới), vào từ cửa Thủ Thành của Động Phủ toán hoặc Cổng Thủ Thành ở Trúc Lâm Thôn.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/books` | — | Kệ phổ của Tàng Thư Các: `{books[{id, name_vi, found, total, pct, milestones[{pct, reward, reward_vi, ready, claimed}]}], titles[], frames[{id, name_vi}], title, frame, shop[{item_id, name_vi, desc_vi, price, kind, have, learned}], at_desk}`; `id` = `monster, bee, fish, treasure, pet` |
| POST | `/books/wear` | `{title?, frame?}` | đeo danh hiệu/khung đã có (`""` = bỏ). Lỗi `no_title`, `no_frame` |
| POST | `/books/buy` | `{item_id}` | mua đan phương ở kệ Thủ Thư (phải đứng cạnh bà ở Trúc Lâm Thôn). Lỗi `too_far`, `not_sold`, `not_enough`, `already_have` |
| GET | `/codex/treasure` | — | Bảo Vật Phổ `{found, total, entries[{id, kind, kind_vi, found, name_vi?, desc_vi?, first_at?}]}` |
| POST | `/books/claim` | `{book, pct}` | nhận mốc 25/50/75/100%. Lỗi `not_yet`, `claimed`, `bad_milestone` |

Kinh thư toán của Tàng Thư Các là `/math/library` (M4).

`GET /me` có thêm `title`, `frame`. `GET /codex/monster` có cả Mặc Quái của Thủ Thành Toán (`id` bắt
đầu bằng `td_`, `td: true`).

## Giai đoạn 8 — Luyện đan, Linh Thú, kinh tế (mục 12, 13)

Cân bằng tiền vào/ra: `docs/BALANCE.md`. Minigame canh lửa dùng `alchemy_fire.py` (file giống hệt nhau ở
`server/app/systems/` và `client/engine/`): kim chạy 0 → `bar` → 0 mỗi `period_ms`; client chỉ gửi kim đã chạy bao lâu
trước mỗi lần bấm, máy chủ tính lại vị trí kim và quyết định phẩm chất chỉ từ ba lần bấm.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/alchemy` | — | `{recipes[{id, name_vi, desc_vi, known, difficulty, fee, yield{ha, trung, thuong}, have_pills, min_realm, min_realm_vi, realm_ok, ingredients[{name_vi, qty, have}]?, ready?, sources_vi[]?}], furnace{level, name_vi, max, next{level, name_vi, cost, materials[], zone_bonus, extra_chance}?}, where: home\|public\|far, level_here, open (mẻ đang luyện)?, buffs[], quality[], brew_xp{ha, trung, thuong}}` |
| POST | `/alchemy/start` | `{recipe_id}` | lấy nguyên liệu + phí ngay, nhóm lửa → `{fire{session_id, recipe_id, name_vi, bar, periods[3], zones[3]{center, width, perfect}, furnace_level, expires_at}, resumed, used[]}`. Đang có mẻ dở cùng đan thì trả lại mẻ đó. Lỗi `no_recipe`, `no_ingredient`, `insufficient_funds`, `realm_low`, `too_far`, `fire_busy` |
| POST | `/alchemy/finish` | `{session_id, timings[3] (ms kim chạy)}` | → `{quality: phe\|ha\|trung\|thuong, quality_vi, points, best, hits[], positions[], made, extra, pill, total, xp (Tu Vi theo phẩm chất, null khi phế đan)}`. Hết hạn (15 phút) → `{quality: "phe", expired: true, made: 0}`. Lỗi `bad_timings`, `too_fast` (kim không thể chạy nhanh hơn thời gian thật), `finished` (409), `no_session` |
| POST | `/alchemy/furnace/upgrade` | — | nâng Đan Lô trong động phủ (chỉ ở nhà). Lỗi `not_home`, `max_level`, `no_material`, `insufficient_funds` |
| GET | `/pets` | — | `{pets[{id, pet_type, name_vi, zodiac_vi, rarity, rarity_vi, level, max_level, equipped, skill_vi, stats, look}], equipped, book[12]{id, found, zodiac_vi, rarity, (đã gặp:) name_vi, skill_vi, look}, found, total, looks{loài: look}}` |
| POST | `/pets/equip` | `{pet_id \| null}` | đeo một con (hoặc tháo); trả lại như `GET /pets`. Lỗi `no_pet` |
| GET | `/shop` | — | `{stock[{item_id, name_vi, desc_vi, price, daily, left, have}], equipment[{item_id, rarity, rarity_vi, color, name_vi, slot_vi, price, stats}], at_shop, sell_items[], sell_equipment[], spirit_stones}` |
| POST | `/shop/buy` | `{item_id, qty, rarity?}` | phải đứng cạnh Bà Chủ Sạp. `rarity` (`pham`/`linh`) để mua trang bị. Lỗi `too_far`, `not_sold`, `sold_out`, `daily_limit`, `insufficient_funds`, `bad_count` |
| POST | `/shop/sell_equipment` | `{instance_id}` | bán lại trang bị không mặc. Lỗi `equipped`, `too_far` |
| POST | `/friends/gift` | `{friend_id, item_id, qty}` | tặng bạn bè 1–5 món không ràng buộc, 5 lần/ngày. Người nhận được thông báo WebSocket `{t: "friend", event: "gift", item, name_vi, qty, user}`. Lỗi `not_friend`, `blocked`, `not_giftable`, `bad_count`, `gift_limit`, `not_enough` |

Thay đổi ở API cũ:

- `POST /gacha/roll {banner: "pets"}` đã mở: kết quả `[{rarity, pet_type, name_vi, zodiac_vi, look, pet_id, new, level, level_up?, stones?}]`.
- `POST /inventory/use` dùng được Tụ Linh / Kháng Mực / Ngộ Tính Đan → `{used, left, buff, seconds, buffs[]}`; Phong
  Vương Đan cho ong ăn qua `POST /bees/feed {food: "phong_vuong_dan"}`.
- `GET /cultivation` có thêm `buffs[{id, name_vi, seconds_left}]` và `pet` (con đang đeo). `GET /inventory`: mỗi
  trang bị có `sell_price`.
- `GET /quests` có thêm `daily[]` (việc hằng ngày, `chain: "daily"`, id `d<ngày>:<việc>`) và `daily_bonus{rewards_vi,
  claimed}`; nhận việc cuối cùng của ngày trả thêm `rewards.bonus`. Kiểu mục tiêu mới: `brew`,
  `answer`, `td_win`; `target: "*"` là bất kỳ.
- `GET /books`: thêm sổ `pet` (Linh Thú Phổ); mua đan phương đã có → `already_have`.

## Giai đoạn 9 — Bí cảnh (mục 14)

Vào bí cảnh, tổ đội và mọi thứ trong lượt chơi đi qua WebSocket (`docs/PROTOCOL.md`). REST chỉ có:

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/realms` | — | `{realms[{id, name_vi, kind: scheduled\|rift, math, floor, realm_ok, puzzles, rooms[], time_limit_minutes, desc_vi, entries_left, daily, party_min, open, opens_in, closes_in}], math_realms[...như trên, kind: math], party, queue{key, realm, waiting}?, puzzles{kind: {name_vi, how_vi}}, forge{fragments, stones, have, rarity, rarity_vi, set_vi, bonus_vi, pieces[{id, name_vi, slot_vi}]}}` |
| POST | `/realm/forge` | `{piece}` | 12 Mảnh Bảo Vật + 600 Linh Thạch → một món Mặc Ảnh phẩm Thiên → `{equipment, spirit_stones}`. Lỗi `not_enough`, `bad_piece` |

Thay đổi ở API cũ: `GET /fishing` — Cần Thiên Tơ có giá (Thiên Tằm Ti + Vảy Linh Ngư + Linh Thạch, cần Trúc Cơ). Chỉ số
nhân vật cộng thưởng đồ bộ (`equipment.json → sets`). Yêu Quái Phổ có thêm 3 quái bí cảnh.

## Giai đoạn 10 — Phát hành

| Method | Đường dẫn | Ghi chú |
|---|---|---|
| GET | `/server/info` | `{name, version, protocol_version, server_time, local_date, time_scale, env, maintenance_message, announcement, online, uptime_seconds, latest_client_version, client_download_url}`. Trình duyệt (`Accept: text/html`) nhận trang trạng thái HTML; `?format=json` / `?format=html` để ép kiểu |
| GET | `/` | chuyển tới `/server/info` |
| GET | `/healthz` | `{"ok": true}` cho kiểm tra sống của nơi chạy (Render, Docker); không chạm cơ sở dữ liệu |

`maintenance_message` và `announcement` đổi được lúc chạy bằng `/admin maintenance` và `/admin announce` (chat, xem
`docs/DEPLOY.md` mục F); `MAINTENANCE_MESSAGE` là giá trị sau khi khởi động lại. `latest_client_version` lấy từ
`LATEST_CLIENT_VERSION` (mặc định bằng `version`), `client_download_url` từ `CLIENT_DOWNLOAD_URL`.

Thay đổi ở API cũ: `POST /auth/register` cấp `is_admin` cho tên có trong `ADMIN_USERNAMES`. Tài khoản bị khóa nhận
`403 banned` ở mọi request có token và ở `/auth/login`. Câu trả lời Vấn Đạo (`/quiz/answer` và mọi nơi khác) được theo dõi:
200 câu đúng liền mỗi câu dưới 0,5 giây (`balance/quiz.json → bot_watch`) thì tài khoản bị đánh dấu (`suspicious_flag`) cho
quản trị viên xem, không tự cấm.

## Bản 1.1 — Thế giới LAN (tài khoản Firebase)

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| POST | `/auth/firebase` | `{id_token}` | ID token Firebase Authentication → `{token, user_id, username, created, is_admin}` (token phiên của thế giới này, dùng như token của `/auth/login`). Lần đầu tạo tài khoản cục bộ. Lỗi: `firebase_off` (404, máy chủ không đặt `FIREBASE_API_KEY`), `firebase_invalid_id_token` (401), `firebase_network` / `firebase_configuration_not_found` (503), `banned` (403) |

`GET /server/info` có thêm `auth` (`firebase` | `local`), `local_accounts` (bool) và `world_name` (thế giới LAN).
Khi `LOCAL_ACCOUNTS=0`, `/auth/register` và `/auth/login` trả `403 local_off`.
Biến môi trường mới: `FIREBASE_API_KEY`, `HOST_FIREBASE_UID` (người chủ thành quản trị viên), `LOCAL_ACCOUNTS`,
`LAN_BEACON`, `LAN_WORLD_NAME`, `LAN_HOST_NAME`, `FIREBASE_AUTH_EMULATOR_HOST` (thử nghiệm).

Tín hiệu LAN (không phải HTTP): UDP broadcast tới cổng 47654 mỗi 1,5 giây, nội dung JSON
`{"g": "khuvuon-lan", "v": <giao thức>, "name", "host", "port", "online"}`.

## Nhánh `toan-tu-tien` — M2: vòng câu hỏi toán

Một *buổi luyện* (`math_runs`) diễn ra trên một tầng của một bí cảnh toán. Mỗi câu hỏi là một phiên câu hỏi
`context: "math"` và được trả lời qua `/quiz/answer` như mọi câu hỏi khác; đáp án và lời giải chỉ được gửi về
sau khi trả lời.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/math/path` | — | `{subjects[{id, name_vi, order, floors[{floor, title_vi, hidden, tier_min, tier_max, questions, playable, skills[{id, name_vi}]}]}], run?, tiers{"1": "Nhập môn", …}}`. `run` là buổi luyện đang dở (nếu có). `questions` chỉ đếm câu máy chủ được phép hỏi (câu chưa duyệt chỉ tính khi `ALLOW_UNREVIEWED=1`) |
| POST | `/math/run/start` | `{subject_id, floor}` | mở buổi luyện mới ở bậc thấp nhất của tầng (buổi đang dở bị đóng). → `{run}`. Lỗi `no_floor` (404), `no_questions` (400) |
| POST | `/math/run/next` | `{run_id}` | → `{run, question}`. Nếu buổi còn một câu chưa trả lời và chưa hết giờ thì trả lại đúng câu đó. Lỗi `no_run` (404), `run_ended` (409), `no_questions` |
| POST | `/math/run/end` | `{run_id}` | đóng buổi luyện → `{run}` (bảng tổng kết) |

`run` = `{run_id, subject_id, floor, tier, tier_name_vi, tier_min, tier_max, combo, best_combo, asked, correct, xp_gained, ended}`.

`question` = phiên câu hỏi chung cộng `math{subject, subject_name_vi, skill, skill_name_vi, floor, tier, tier_name_vi}`:

| `qtype` | `input` | Câu trả lời gửi lên |
|---|---|---|
| `true_false` | `truefalse` | `{"value": true}` hoặc `{"value": false}` |
| `multiple_choice` | `choice` (`options[{id, text}]`, đã xáo) | `{"option": "a"}` |
| `numeric` | `number` | `{"text": "3/4"}` — số nguyên, số thập phân (dấu chấm), phân số `a/b`, hoặc nhiều số cách nhau bằng dấu phẩy; sai số cho phép `numeric_tolerance`, hoặc `tolerance` riêng của câu (M11 đợt 2, xem dưới bảng) |
| `matching` | `matching` (`prompt.left[]`, `prompt.right[]` đã xáo) | `{"pairs": [r0, r1, ...]}`: `pairs[k]` = vị trí (trong `right`) của vế phải ghép với vế trái thứ k; một hoán vị của `0..n-1` |
| `ordering` | `ordering` (`prompt.steps[]` đã xáo, không bao giờ hiện sẵn đúng thứ tự) | `{"order": [i0, i1, ...]}`: vị trí các bước (trong `steps`) theo thứ tự đúng của lời giải; một hoán vị của `0..n-1` |
| `find_mistake` (M11, từ bậc 2) | `find_mistake` (`prompt.lines[]`: 3-6 dòng của một lời giải, **giữ nguyên thứ tự, không xáo**) | `{"line": i}`: `i` là số nguyên (không phải `true`, `1.0`, chuỗi) từ 0 của dòng đầu tiên bị sai. Sai kiểu, thiếu khoá hay ngoài khoảng chỉ là câu sai, không phải lỗi. `reveal.answer_text` = `"Bước <i+1>: <dòng sai>"`, `reveal.solution_vi` nói vì sao sai và bước đúng |
| `tribulation` (Thiên kiếp, M11 đợt 2, chỉ bậc 4-5, 480 / 720 giây) | `tribulation` (`prompt.text` = tình huống chung, có thể kèm `prompt.matrices`; `prompt.parts[{text, input, options}]`: 2-4 phần theo thứ tự, `input` của mỗi phần là `truefalse`, `choice` hoặc `number`; `options` của phần `choice` đã xáo như một câu trắc nghiệm, các phần khác `null`) | `{"parts": [a0, a1, ...]}`: đúng một câu trả lời cho mỗi phần, theo đúng hình của loại phần ấy (`{"value": bool}`, `{"option": id}`, `{"text": "..."}`). Đúng chỉ khi **mọi** phần đúng, mỗi phần chấm theo luật của loại nó. Thiếu, thừa, sai kiểu phần nào cũng chỉ là câu sai, không phải lỗi. `reveal.answer_text` = `"a) ...; b) ..."`, `reveal.parts[{answer_text, key}]` (chỉ gửi sau khi trả lời) để thẻ nói từng phần đúng hay sai |

`tolerance` (M11 đợt 2): một câu `numeric`, hay một phần `numeric` của Thiên kiếp, có thể có sai số riêng
(0 < `tolerance` ≤ 1) cho đáp án là số thập phân đã làm tròn; đề nói rõ làm tròn thế nào. Khi có, nó thay
`numeric_tolerance` cho riêng câu ấy (nằm trong khoá đáp án); `reveal.answer_text` giữ số như viết (`12.35`).
Không có thì câu số vẫn chấm như cũ. Thiên kiếp không bao giờ được hỏi ở hầm ngục trừ Phòng Lôi Kiếp (tầng 7-9,
một câu là qua phòng), ở thủ thành toán (`td.json` `qtypes`) hay ở bí cảnh toán (`math_realm.QUICK_TYPES`); chiêu
Thiên Lôi Tuyệt Kỹ hỏi nó, và Hộ Thể kéo dài suốt thời gian của câu.

Hết giờ trên máy khách thì game gửi `{"timed_out": true}`; máy chủ cũng tự tính hết giờ theo `expires_at`
(`time_limit` + `network_grace`). Cả hai đều là một câu sai và làm mất chuỗi đúng, không mất gì khác.

`/quiz/answer` trả thêm cho câu toán: `reveal{answer_text, solution_vi[]}`, `xp` (Tu Vi theo bậc, chỉ khi đúng) và
`math{tier, timed_out, xp_base, tier_change (-1/0/+1), run}`.

### M3: ngân hàng câu tầng 1-3, bộ sinh câu, câu song song

- `GET /math/path`: mỗi tầng có thêm `generators` (số bộ sinh câu); `questions` giờ là số *dạng câu* (câu viết
  tay + bộ sinh câu). Tầng 1-3 của Đại Số Tuyến Tính `playable`.
- `question.prompt` có thể kèm `matrices[{name, rows[][]}]` (mỗi phần tử là chuỗi: số, phân số `a/b` hoặc một
  chữ thường như `x`); game tự vẽ, lời đề chỉ gọi tên ("ma trận A như hình").
- `question.math.parallel` = `true` khi đây là câu song song của một ý vừa sai (luật 6, "tâm ma").
- `/quiz/answer` → `math` có thêm `parallel` (câu vừa trả lời là câu song song) và `parallel_waiting` (ý này
  đang chờ quay lại: vừa trả lời sai hoặc hết giờ).
- Câu do bộ sinh câu tạo ra được lưu với `quiz_sessions.item_id` = mã bộ sinh câu; bộ số nằm trong dấu vân tay
  (`math_answers.fingerprint`).

### M4: Tàng Thư Các của bí cảnh toán

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/math/library` | — | `{subjects[{id, name_vi, order, documents[{id, title_vi, floor, summary_vi, skills[], sections[]}]}]}` |
| GET | `/math/library/{doc_id}` | — | một bài đọc đã tách sẵn thành khối. Lỗi `no_doc` (404) |

Bài đọc: `{id, title_vi, subject, floor, skills[], summary_vi, blocks[]}`. Mỗi khối có `type`:

| `type` | Nội dung | Game vẽ bằng |
|---|---|---|
| `section` | `title_vi`, `skill` | tiêu đề một mục, ứng với một vi kỹ năng |
| `heading` | `title_vi` | tiêu đề nhỏ |
| `text` | `text` | một đoạn văn |
| `bullets` / `steps` | `items[]` | gạch đầu dòng / các bước có đánh số |
| `formula` | `key`, `tex`, `alt`, `w`, `h` | ảnh `client/assets/formulas/<key>.png` vẽ rộng `w` cao `h` đơn vị nền; thiếu ảnh thì hiện `alt` |
| `matrices` | `matrices[{name, rows[][]}]` | game tự vẽ ngoặc vuông và các số |
| `note` | `text` | lời nhắc của Trúc Lão |

- `GET /math/path`: mỗi tầng có thêm `doc_id` (bài đọc của tầng, hoặc `null`).
- `question.math.doc` = `{id, title_vi, block}`: bài đọc giải thích vi kỹ năng của câu hỏi và số thứ tự khối
  để mở đúng mục. `null` khi chưa có bài đọc.

### M5: cổng thuần thục, Thiên kiếp nhỏ, ôn xoắn ốc

Tầng 1 của một bí cảnh mở sẵn; tầng trên chỉ mở khi tầng dưới đã **qua** (vượt Thiên kiếp nhỏ của nó).
Tầng ẩn 10 chờ tầng 9. Mở buổi luyện ở tầng chưa mở → lỗi `floor_locked` (403).

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| POST | `/math/trial/start` | `{subject_id, floor}` | mở **Thiên kiếp nhỏ** của tầng: mỗi vi kỹ năng một câu, đều ở bậc cao nhất của tầng. → `{run, gate}`. Lỗi `gate_not_met` (409, kèm tên vi kỹ năng cần ôn), `floor_locked` (403), `no_floor` (404), `no_questions` (400) |

- `GET /math/path`: mỗi bí cảnh có thêm `cleared[]` (các tầng đã qua) và `next_floor` (tầng đang đi, `null`
  khi đã xong hết tầng chính). Mỗi tầng có thêm:
  `state` (`locked` | `open` | `cleared`), `has_questions` (tầng có câu hỏi hay chưa — `playable` giờ còn đòi
  tầng đã mở), `trial_total` (số câu của Thiên kiếp nhỏ) và `gate` (`null` khi tầng còn khoá hoặc chưa có câu):

  `gate` = `{floor, ok, weak[], skills[{skill, tier, top_tier, at_top, answered, correct, needed, window, ok}]}`
  — `tier` là bậc cao nhất đang mở của vi kỹ năng đó, `ok` khi `tier == top_tier` và trong `window` câu gần nhất
  ở bậc ấy có ít nhất `needed` câu đúng (mặc định 4/5 = 80%). Cổng mở khi mọi vi kỹ năng `ok`.
- `run` có thêm `mode` (`practice` | `trial`), `review_asked` (số câu ôn tầng dưới trong buổi), `passed`
  (`null` khi chưa ngã ngũ) và — khi là Thiên kiếp nhỏ — `trial{total, left, wrong, max_wrong}`.
- `question.math.review` = `true` khi đây là câu ôn xoắn ốc lấy từ **tầng dưới**; `question.math.floor` khi đó
  là tầng của câu, không phải tầng đang luyện. Khoảng mỗi 4 câu có một câu như vậy (`spiral_review.share_max`).
- `/quiz/answer` → `math` có thêm `review` và, trong Thiên kiếp nhỏ,
  `trial{total, asked, correct, left, passed, unlocked}`: `passed` là `null` khi còn câu, `true`/`false` khi đã
  ngã ngũ (thi trượt dừng ngay, không bắt làm nốt), `unlocked` là tầng vừa mở ra.
- Trong Thiên kiếp nhỏ không có câu song song (tâm ma) và không có câu ôn; bậc không lên xuống theo chuỗi
  đúng/sai (`tier_change` luôn 0).

### M6: bài tập lập trình

Bài làm **chạy trên máy người học**, không chạy trên máy chủ (kế hoạch 5.2). Máy chủ chỉ gửi đi *dữ liệu vào*:
đề bài kèm ví dụ, và khi nộp bài thì dữ liệu vào của test ẩn. Đáp án của test ẩn và lời giải mẫu không bao giờ
rời máy chủ. Game gửi về những gì chương trình đã in ra, máy chủ so đáp án và quyết định AC / WA / TLE / RE / CE.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/math/problems?subject_id=&floor=` | — | `{subject_id, name_vi, floors[{floor, title_vi, problems[{id, title_vi, skill, floor, tier, tests, reviewed, best}]}]}`. `floor` là tuỳ chọn; tầng chưa mở không có trong danh sách. `best` = lần nộp tốt nhất `{verdict, passed, total, ms, xp_gained}` hoặc `null` |
| GET | `/math/problem/{id}` | — | đề bài và ví dụ. `tests` chỉ là **số lượng** test ẩn. Lỗi `no_problem` (404), `floor_locked` (403) |
| POST | `/math/problem/{id}/tests` | — | Nộp bài bước 1 → `{attempt_id, total, time_limit_ms, inputs[]}`: dữ liệu vào của test ẩn, để chạy trên máy người học. Lần nộp chưa chấm thì dùng lại, không mở thêm |
| POST | `/math/problem/{id}/judge` | `{outputs[], status, times_ms[], code, error, attempt_id?}` | chấm. Có `attempt_id` là **Nộp bài** (test ẩn, có Tu Vi); không có là **Chạy thử** (ví dụ, không Tu Vi, không ghi lại). Lỗi `no_attempt` (404), `already_judged` (409), `bad_status`, `too_many_outputs`, `output_too_long`, `code_too_long` (400) |

`problem` = `{id, subject, subject_name_vi, skill, skill_name_vi, floor, tier, tier_name_vi, title_vi,
statement_vi[], input_vi, output_vi, limits_vi, checker ("exact" | "float"), time_limit_ms, samples[{in, out,
note_vi}], tests (số test ẩn), think_limit_s, reviewed}`.

`status` là kết quả của chính lần chạy trên máy người học: `ok` (chạy hết), `ce` (không biên dịch được),
`re` (lỗi lúc chạy), `tle` (quá giờ). Lần chạy dừng ở test đầu tiên bị hỏng, nên `outputs` có thể ngắn hơn
`total`.

Kết quả chấm = `{verdict, passed, total, share, ms, error, tests[{test, verdict, ms}]}`, với `verdict` của từng
test là `AC`, `WA`, `TLE`, `RE`, `CE` hoặc `-` (chưa chạy tới). Khi nộp bài còn có `xp`, `xp_gained` và `best`.

- `GET /math/path`: mỗi bí cảnh có thêm `problems` = số bài tập người chơi mở được lúc này (các tầng đã mở).
- Tu Vi: bậc của bài đáng `xp_per_correct` của bậc đó, nhân với tỉ lệ test đạt, và **chỉ trả phần hơn** so với
  lần tốt nhất trước đó - nộp lại cùng một bài làm không ăn thêm Tu Vi.

### M7: quái lỗi sai và Lò Toán

Quái trong Loạn Số Cốc là **lỗi sai**: mỗi con giữ một vi kỹ năng, và Mặc Thuẫn của nó chỉ xuống khi
người chơi trả lời đúng một câu toán của vi kỹ năng ấy. Câu hỏi đi qua đúng đường cũ: gói `q` trên
WebSocket rồi `POST /quiz/answer`, chỉ khác `context` là `math_combat` và trong gói có khối `math`
(giống câu ở Động Phủ) kèm hai khoá riêng:

- `math.mistake_vi`: lỗi con quái ấy mắc, hiện trên thẻ.
- `math.monster_vi`: tên nó.

**Bậc câu hỏi không do con quái quyết định.** Máy chủ đọc nhật ký trả lời của chính người chơi ở vi kỹ
năng ấy (`math_answers`) rồi hỏi ở bậc cao nhất đã mở (luật 3.3), nên con quái còn dạy được khi người
chơi khá lên. Câu trả lời được ghi vào `math_answers` với `run_id = NULL`: luật học đọc nhật ký ấy, nên
đánh quái ngoài thế giới cũng tính vào bậc đã mở và vào cổng thuần thục. Luật 6 ("tâm ma") **không** chạy
ở đây: câu song song không có buổi luyện nào để quay về.

Khi chưa có câu nào cho vi kỹ năng ấy ở bậc của người chơi, máy chủ gửi `{"t": "error", "code":
"no_math_question"}` và con quái giữ khiên.

Từ luật vùng hoang (mục "Luật vùng hoang" bên dưới), câu của quái lỗi sai đến khi **đòn của nó trúng người
chơi**, không còn đến khi đánh nó; câu hỏi và cách chọn bậc thì giữ nguyên.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/math/craft` | — | `{recipes[], spirit_stones}`. Mỗi công thức: `{id, name_vi, floor, fee, rarity, desc_vi, makes{item_id, name_vi, slot, stats}, ingredients[{item_id, name_vi, qty, have, enough}], notes[{...}], can}` |
| POST | `/math/craft` | `{recipe_id}` | rèn. Lỗi `no_recipe` (404), `need_note`, `need_material`, `no_stones` (400) |

`ingredients` bị tiêu, `notes` (ghi chú lỗi sai) **chỉ bị kiểm tra** - chúng vẫn ở trong túi sau khi rèn,
như đan phương. `rarity` ghi cố định trong công thức, không rút thăm.

- `POST /inventory/use` với một ghi chú lỗi sai (`kind: "note"`) không tiêu nó: trả về
  `{read, skill, doc{id, title_vi, block}}` để game mở đúng mục trong Tàng Thư Các.
- `GET /inventory`: vật phẩm `kind: "note"` có `usable: true`.
- `GET /codex/monster`: mỗi con có thêm `mistake_vi` (rỗng với Mặc Quái cũ).

### M9: chiêu thức gắn câu hỏi

Mỗi chiêu (`server/data/math/skills.json`) **được thi triển bằng cách trả lời một câu toán thuộc loại của
nó** (`qtypes`). Đúng → chiêu trúng. Sai hoặc hết giờ → "chiêu hụt": không gây sát thương, combo về 0,
**không có Mặc Kích**; chỉ mất linh khí và thời gian hồi đã tiêu. Trong lúc trả lời người chơi có Hộ Thể
như Vấn Đạo và dùng chung một ô câu hỏi (mỗi lúc chỉ một câu).

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/math/skills` | — | `{combo{per_streak, max_mult}, open_floor, skills[]}`, theo đúng thứ tự trong `skills.json`. Mỗi chiêu: `{id, name_vi, kind_vi, element, qtypes[], qtype_vi, min_tier, qi, cooldown, range, effect, power, anim, fx, desc_vi, unlock{floor}, unlocked, locked_vi}`, cộng `radius, slow, duration` (chiêu `area`) hoặc `radius, duration, reduce, heal_pct` (chiêu `ward`) |

**Mở khoá chỉ theo lộ trình học**: `open_floor` là tầng chính thấp nhất chưa qua Thiên kiếp nhỏ (tầng cuối
nếu đã qua hết), lấy cao nhất giữa các môn; chiêu mở khi `open_floor >= unlock.floor`. Không gắn với cảnh
giới tu luyện. Chiêu bị khoá có `locked_vi` (ví dụ "Mở khi lộ trình học tới tầng 7 (con đang ở tầng 1).").
`thien_loi_tuyet_ky` hiện **luôn khoá**: loại `tribulation` chưa chơi được và bậc 4 chỉ có từ tầng 5 (M11).

**Câu nào được hỏi**: loại thuộc `qtypes`; nếu mục tiêu là quái lỗi sai thì hỏi vi kỹ năng của chính nó,
không có thì vi kỹ năng khác cùng tầng; không có mục tiêu (chiêu `ward`) hoặc mục tiêu là Mặc Quái cũ thì
hỏi ở `open_floor` của môn đầu tiên có câu (thiếu thì xuống tầng dưới). Bậc là bậc của chính người chơi ở
vi kỹ năng ấy, **không bao giờ cao hơn**; không có câu ở bậc đó thì lấy bậc thấp hơn gần nhất, không dưới
`min_tier`. Câu trả lời được ghi vào `math_answers` với `run_id = NULL` (tính cho lộ trình học) và được
Tu Vi theo bậc như M7.

**Sát thương** mỗi con quái trúng: `base_damage × power × combo_mult × (fast_answer_crit_mult nếu trả lời
trong fast_answer_fraction thời gian)` (hai số sau ở `balance/combat.json`, như Ngộ Đạo). `combo_mult =
min(max_mult, 1 + per_streak × n)`, `n` = số câu chiêu đúng liên tiếp **trước** câu này (câu đúng đầu tiên
×1.0, câu thứ hai ×1.1, ... tối đa ×1.5). Combo theo từng người, chỉ trong bộ nhớ, về 0 khi hụt, khi ngã
xuống và khi rời thế giới. Chiêu trúng phá Mặc Thuẫn của mục tiêu như một câu Vấn Đạo đúng; với khiên
nhóm của boss bí cảnh nó chỉ tính là câu đúng của **một** người (vẫn cần đủ N người).

- `damage`: một mục tiêu trong `range`.
- `area`: mọi quái trong `radius` quanh mục tiêu trúng đòn và chậm còn `slow` × tốc độ trong `duration` giây
  (chỉ khiên của mục tiêu bị phá; con khác còn khiên chỉ bị trầy 1 máu, và bị cuốn vào trận đấu).
- `ward`: không cần mục tiêu; người thi triển và đồng đội tổ đội đứng trong `radius` chịu ít hơn `reduce`
  sát thương trong `duration` giây và hồi `heal_pct`% máu tối đa.

WebSocket, client → server:

    {"t": "mskill", "k": "<id chiêu>", "id": "<eid quái>" | null}

Bị từ chối (không mất gì): `{"t": "mcast", "k", "ok": false, "code", "message_vi"}`, `code` ∈ `unknown`,
`locked`, `cooldown`, `no_qi`, `no_target`, `too_far`, `answering`, `cannot`, `tier_low` (bậc đã mở thấp
hơn `min_tier` hoặc chỉ có câu ở bậc cao hơn), `no_question` (chưa có câu loại này). `unknown`, `cannot`,
`answering` trả về ngay; các mã khác đến sau khi máy chủ đọc lộ trình và soạn câu.

Được nhận (linh khí bị trừ, bắt đầu hồi chiêu), theo thứ tự:

    {"t": "mcast", "k", "ok": true, "ready_in": <giây hồi>, "qi": <linh khí còn lại>}
    {"t": "q", "mid": <eid | null>, "q": <phiên câu hỏi, context "math_skill">, "first_meet": false,
     "cast": {"k", "name_vi"}}

Gói `q` giống hệt câu Vấn Đạo (khối `math` có thêm `cast_vi`, và `mistake_vi`, `monster_vi` khi mục tiêu là
quái lỗi sai), trả lời bằng `POST /quiz/answer` như mọi câu. Kết quả có khối `math` như M7 và:

    "combat": {"cast", "correct", "missed", "timed_out", "damage", "crit", "combo", "combo_mult",
               "shield_broken", "monster_hp", "killed"}

`monster_hp` là phần trăm máu còn lại (0 với `ward`, không có mục tiêu). Chiêu `ward` có thêm
`ward{players, heal, duration, reduce}`; khiên nhóm chưa đủ người có thêm `shield_progress[có, cần]` và
`damage: 0`. Khi thế giới đã đổi trong lúc trả lời (mục tiêu chết hoặc bỏ đi, người chơi ngã, đổi vùng)
khối này chỉ là `{"cast", "stale": true}` và không gì được gây ra; nếu người chơi đã rời thế giới thì
không có khối `combat`. Hết giờ được chấm như câu sai, cũng không có Mặc Kích. Sau chiêu hụt vào quái còn
khiên, con quái hỏi câu Vấn Đạo của nó sau `next_question_delay` giây như thường lệ. Câu trả lời đúng
của người khác phá khiên **không** huỷ câu chiêu đang mở: chiêu vẫn trúng khi trả lời đúng.

Sự kiện kênh (trong `fx` của `snap`, ai ở gần cũng thấy):

- `{"k": "mcast", "by", "s", "anim", "x", "y"}`: bắt đầu vận chiêu (câu hỏi vừa mở).
- `{"k": "mskill", "by", "s", "fx", "anim", "ok": 1|0, "x", "y", "tx", "ty", "r", "combo"}`: chiêu trúng
  (`ok: 1`) hoặc hụt (`ok: 0`); `tx, ty` khi có mục tiêu, `r` với `area`/`ward`. Đòn đánh vẫn đi kèm
  các sự kiện `hit`, `shield`, `gshield`, `heal`, `die` như cũ.

Tất cả những điều trên (chiêu ra bằng một câu hỏi, chiêu hụt, combo theo câu chiêu đúng) nay chỉ còn ở **bí
cảnh**. Ở vùng hoang chiêu ra tự do: xem mục dưới.

### Luật vùng hoang: chỉ hỏi khi bị quái đánh trúng

Phần `combat` của `server/data/math/world_plan.json` (`"wired_sections": ["combat"]`; `"wired"` vẫn là `false`
vì vùng đất, binh khí, linh thú chưa nối). Mọi con số đọc từ đó. Giao thức WebSocket: `docs/PROTOCOL.md`.

- **Đánh thường và chiêu thức không hỏi gì.** `mskill` ở vùng hoang được nhận rồi trúng ngay:
  `{"t": "mcast", "k", "ok": true, "free": true, "ready_in", "qi", "result": <khối combat như trên>}`, kèm sự
  kiện `mskill` (`ok: 1`). Từ chối như trên (`locked` luôn được nói trước `cooldown`/`no_qi`/`no_target`), mọi mã
  đến sau khi máy chủ đọc lộ trình. Sát thương = `base_damage × power × combo_mult(n)`, n = số **Phản Đòn liên
  tiếp** (về 0 khi trả lời sai, hết giờ, chết, rời thế giới); không có chí mạng "trả lời nhanh". Chiêu không phá
  Mặc Thuẫn của tinh anh: chỉ Phản Đòn phá được. Mở khoá chiêu vẫn theo Đạo Thụ như M9.
- **Câu hỏi của một đòn trúng** đến như gói `q` có `hit` = `{dmg, monster_vi, rest}`, context `math_combat`, chọn
  đúng như M7: quái lỗi sai hỏi vi kỹ năng của nó ở bậc người chơi đã mở (không vượt trần của tầng), Mặc Quái
  hỏi ở phần Đạo Thụ của chính người chơi. Câu trả lời ghi vào `math_answers` (`run_id = NULL`), nên tính vào bậc
  đã mở, cổng thuần thục và lịch ôn xoắn ốc. Kết quả của `POST /quiz/answer`:

      đúng (Phản Đòn): "combat": {"parry": true, "correct": true, "damage", "shield_broken", "stun",
                                  "qi_gain", "combo", "rest", "monster_hp", "killed"}   (+ "gone": true khi quái đã chết)
      sai / hết giờ:   "combat": {"parry": false, "correct": false, "damage_taken", "hp", "dead",
                                  "shows_solution": true, "rest"}

  Tu vi của câu đúng đến qua `xp` như mọi câu (theo bậc). Trả lời sai không còn là Mặc Kích (`mac_kich_pct`): đòn
  của con quái trúng nguyên vẹn. Hết giờ được vòng tick chấm là sai. Không có câu nào để hỏi
  (`no_math_question`): đòn trúng nửa máu và bắt đầu thời gian nghỉ.

### Binh khí của Thiên Địa Đồ

Các phần `grades`, `qualities`, `weapon_types`, `weapons`, `weapons_placed` của `server/data/math/world_plan.json`
(`"wired_sections"` có `"weapons"`), luật ở `server/app/systems/weapons.py`. Một binh khí là `<loại>_<bậc>`
(`kiem_1` = Mộc Kiếm); id của một chỗ đặt là `<binh khí>_<phẩm>` (`kiem_1_ha`), hoặc `id` của mục nếu kế hoạch
ghi. Nhặt rồi nó là **một món trang bị như mọi món khác** (ô `weapon`, `kind` = id binh khí): `GET /inventory`
liệt kê nó trong `equipment`, `/equipment/equip` cũng mặc được, Lò Rèn cường hóa được, sạp mua lại được. Phẩm
lưu thành độ hiếm (hạ = `pham`, trung = `linh`, thượng = `huyen`); Công = `atk` của bậc × `power` của phẩm
(× cường hóa). Mỗi món như vậy trong `equipment` có thêm khối `weapon` = `{weapon, name_vi, type, type_vi, grade,
grade_vi, quality, quality_vi, atk, branch, branch_vi, clip, effect_vi, why_vi, upgradable}`.

"Tu vi" của yêu cầu là **chỗ đứng trên Đạo Thụ** (`math_tree_progress`), không phải cảnh giới nhân vật.

| Method | Đường dẫn | Body | Ghi chú |
|---|---|---|---|
| GET | `/weapons` | — | `{weapons[], equipped, placed[], tu_vi{realm, realm_vi, stage}, can_claim, can_upgrade}`. `weapons`: mọi món ô vũ khí của người chơi (dạng `equipment` của `/inventory`; món của Thiên Địa Đồ có khối `weapon`); `equipped`: id món đang cầm hoặc `null`. `placed`: mọi chỗ đặt, theo thứ tự kế hoạch: `{id, weapon, quality, land, pos, state, reason_vi, name_vi, quality_vi, type, type_vi, grade, grade_vi, atk, branch, branch_vi, clip, effect_vi, why_vi, land_vi, spot_vi, requires{realm, realm_vi, stage, nodes[{id, name_vi}], needs}}`. `state`: `available`, `taken` hoặc `locked`; `reason_vi` (rỗng khi không khoá) nói thiếu gì: tầng Đạo Thụ, tên các nút chưa xong, vùng đất chưa mở, năng lực chưa có. `pos` = `[x, y]` chép từ mục của kế hoạch, không có thì `null` |
| POST | `/weapons/claim` | `{id, land?}` | nhặt một lần. `land` (tuỳ chọn): vùng người chơi đang đứng; có thì phải đúng vùng của chỗ đặt. Trả `{claimed, equipment, placed}`. Lỗi `no_weapon` (404), `taken`, `wrong_land`, `locked` (400, `message_vi` = lý do) |
| POST | `/weapons/equip` | `{instance_id}` | qua đúng đường `/equipment/equip`: `{equipped, stats}`; `stats.weapon` = id binh khí. Lỗi `no_item` (404), `not_weapon` (400) |
| POST | `/weapons/unequip` | — | tháo ô vũ khí: `{stats}` |
| GET | `/weapons/upgrade` | — | Rèn nâng phẩm ở Lò Toán: `{open, reason_vi, name_vi, desc_vi, fee, from, from_vi, to, to_vi, ingredients[{item_id, name_vi, qty, have, enough}], can, candidates[], spirit_stones}`; `candidates` = món hạ phẩm của Thiên Địa Đồ (dạng `equipment`) kèm `after` (khối `weapon` ở phẩm mới) và `after_atk` |
| POST | `/weapons/upgrade` | `{instance_id}` | hạ phẩm → trung phẩm, giữ bậc và cường hóa: `{upgraded, item, stats, spirit_stones}`. Lỗi `locked` (chưa tới Luyện Khí tầng 4 trên Đạo Thụ), `not_plan_weapon`, `wrong_quality`, `need_material`, `no_stones` (400), `no_item` (404) |

Lỗi theo dạng chung `{"error": {"code", "message_vi"}}`.

Khi đánh: loại binh khí quyết định đòn thường (`range`, `cooldown`, `mult` của `weapon_types`) và động tác (`clip`:
`slash`, `cast`, `shoot`). Phản Đòn (luật vùng hoang) với câu thuộc đúng nhánh của binh khí mạnh thêm
`weapons.own_branch_parry_bonus` (Kiếm với câu Đại Số...); binh khí của nhánh không có môn toán riêng (Chùy - Lập
Trình, Cung - Thực Chiến, Trượng, Phiến) mạnh thêm `weapons.any_branch_parry_bonus` với mọi câu. Khối `combat` của
Phản Đòn có thêm `"weapon_bonus": true|false`.

### Linh thú của Thiên Địa Đồ

Phần `beasts` và `beast_taming` của `world_plan.json` (`"wired_sections"` có `"beasts"`), luật ở
`server/app/systems/beasts.py` (dữ liệu, phong ấn) và `server/app/realtime/beasts.py` (linh thú ngoài vùng đất).
Thu rồi linh thú là một Linh Thú như con giáp: `GET /pets` liệt kê nó (`"tamed": true`, `skill_vi` = quà của nó),
`POST /pets/equip` đeo nó; Linh Thú Phổ (`book`, `total`) vẫn chỉ là mười hai con giáp.

| | Đường | Gửi | Trả về |
|---|---|---|---|
| GET | `/beasts` | — | `{beasts[], rule_vi, talisman{item, name_vi, have}, can_seal, tu_vi{realm, stage}}`. `beasts`: `{id, name_vi, land, land_vi, zone, where_vi, pos, requires, needs, parries_to_tame, gift, gift_vi, state, reason_vi}`; `state`: `locked` (chưa đủ tầng / thần thông, `reason_vi` nói thiếu gì), `open`, `tamed` |
| POST | `/beasts/seal` | `{id}` (id của linh thú trong thế giới, ví dụ `b1_huyen_quy`) | dùng một Phong Ấn Phù lên linh thú đứng gần đã chịu phục mình: `{sealed, name_vi, pet, message_vi}` (`pet` như một mục của `/pets`). Lỗi (400): `not_here` (không thấy nó ở vùng này), `not_yielded` (chưa đủ Phản Đòn), `too_far`, `locked` (chưa mở Thu phục linh thú), `no_talisman`, `tamed`; `no_beast` (404) |
| GET | `/beasts/sniff` | — | quà của Linh Hồ (đang đeo): binh khí còn nằm trong vùng này trong `radius_tiles` ô, gần nhất trước: `{radius_tiles, found[{id, kind: "weapon", name_vi, pos, distance_tiles, way_vi}]}`. Lỗi (400): `not_in_world`, `no_nose` (không đeo linh thú biết đánh hơi) |

Phong Ấn Phù (`phong_an_phu`) bán ở Sạp Tạp Hóa (`GET /shop`). Thần thông (pháp trận, Đạp Kiếm Lướt, cưỡi) đi
qua WebSocket: `docs/PROTOCOL.md`.

## M10 — Cơ duyên (sự kiện ngẫu nhiên sau câu đúng)

Dữ liệu: `server/data/math/fortune.json` (`_comment` giải thích từng trường). Mã: `app/systems/math_fortune.py`.
Mỗi câu toán trả lời đúng (buổi luyện, quái lỗi sai, chiêu thức, các chế độ khác; câu của chính cơ duyên
không tính) cộng một vào bộ đếm; chạm ngưỡng thì bộ đếm về 0 và gieo xem có cơ duyên không. Một lúc chỉ có
một lời mời mở, mỗi ngày (giờ máy chủ, UTC+7) tối đa `daily_limit` lời mời. Trạng thái nằm trong
`users.flags["math_fortune"]`. Câu hỏi luôn lấy qua `math_ask` (bậc của chính người chơi, không bao giờ cao hơn).

- `GET /math/fortune` -> `{"offer": {id, kind: "elder"|"chest", name_vi, intro_vi, accepted, expires_in,
  progress: [đã đúng, tổng]} | null, "today": {offers, limit}, "progress": {right, need}, "log": [{at, event,
  name_vi, kind, outcome: won|lost|declined|expired|timeout, rewards?}], "how_vi"}`. Lời mời hết hạn tự biến mất.
- Lời mời hiện ra trong phản hồi `POST /quiz/answer` của câu đúng đã khiến nó xuất hiện:
  `math.fortune_offer` (cùng dạng `offer` ở trên). Máy khách báo bằng `scenes/math_fortune.notice(game, res)`.
- `POST /math/fortune/accept` -> `{"question": <phiên câu hỏi, context "math_fortune">, "fortune": offer}`;
  nhận lần nữa trả lại đúng câu đang chờ. Khi không còn câu nào để hỏi: `{"question": null, "ended": true,
  "message_vi"}` (không lỗi, không mất gì). 404 `no_offer` nếu không có lời mời.
- `POST /math/fortune/decline` -> như `GET /math/fortune`. 409 `accepted` nếu đã nhận rồi.
- Trả lời câu của cơ duyên: `POST /quiz/answer` như mọi câu. Phản hồi có thêm khối `fortune`:
  `{event, kind, name_vi, progress: [i, n], done, won, rewards: {spirit_stones, items: [{item, qty, rare,
  name_vi}]} | null, next: <phiên câu hỏi tiếp> | null, text_vi (khi done), stale}`. Sai, hết giờ hay quá
  `play_seconds` thì kết thúc, không thưởng, không phạt. Lão nhân ra đề (`elder`) hỏi một câu khó nhất người chơi
  được phép gặp; rương đề (`chest`) hỏi `count` câu thuộc các dạng đã nêu, phải đúng hết.

## M10 — Hầm ngục (sinh theo hạt giống, mỗi phòng một dạng câu)

Dữ liệu: `server/data/math/dungeon.json` (`_comment` giải thích từng trường). Mã: `app/systems/math_dungeon.py`,
bảng `math_dungeon_runs` (migration `0014_math_dungeon`). Bản đồ của một hầm (số phòng, dạng câu và thứ tự
từng phòng, vi kỹ năng mỗi phòng hỏi, kẻ canh giữ, rương cuối) là một hàm thuần của (hạt giống, môn, tầng):
cùng hạt giống thì cùng hầm. Câu hỏi bên trong không thuộc hạt giống: lấy qua `math_ask` lúc vào phòng (bậc
của chính người chơi, không bao giờ cao hơn; chống lặp theo nhật ký của người chơi). Chỉ sinh phòng hỏi được
cho bất kỳ ai đứng ở tầng đó (dạng câu + vi kỹ năng có câu ở bậc thấp nhất của tầng). Phòng cuối là trấn thủ:
câu khó nhất người chơi được hỏi ở dạng đó (`highest`). Mỗi phòng thường cần `questions_per_room` câu đúng,
phòng trấn thủ `warden_questions`. Câu sai hoặc hết giờ mất một tâm lực; hết tâm lực là thua; thứ đã nhận
không mất. `rewards_per_day` hầm đầu tiên mỗi ngày (UTC) có Linh Thạch và vật liệu; sau đó vẫn chơi, vẫn có Tu Vi.

- `GET /math/dungeon` -> `{subject_id, subject_name_vi, floors: [{floor, title_vi, open, locked_vi}], own_floor,
  run: <run> | null, hearts, rewards_left, rewards_per_day, seed_max}`. Câu của hầm đang mở đã hết giờ mà chưa
  trả lời thì được chấm như hết giờ ngay lúc này (mất tâm lực).
- `GET /math/dungeon/layout?seed=&floor=` -> `{"layout": {seed, subject_id, floor, floor_title_vi, rooms:
  [{index, kind, name_vi, short_vi, desc_vi, qtype_vi, skill, skill_name_vi, guardian_vi, flavour_vi, warden,
  need}], room_reward: {stones, items}, chest: {name_vi, stones, items: [{item_id, name_vi, qty}]}}}`: xem trước,
  không vào hầm. `floor` mặc định là tầng của người chơi.
- `POST /math/dungeon/start {seed?, floor?}` -> `{"run": <run>}`. Không có `seed` thì máy chủ tự rút (0..`seed_max`)
  và trả về. Tầng chưa tới: 403 `floor_locked`; tầng chưa có câu: 400 `no_questions`; hạt giống ngoài khoảng:
  400 `bad_seed`. Hầm đang mở (nếu có) bị bỏ (`abandoned`).
- `<run>` = `{run_id, seed, subject_id, subject_name_vi, floor, floor_title_vi, rooms: [... như layout, thêm
  state: cleared|current|ahead|lost|left, progress], room, rooms_cleared, total_rooms, hearts, max_hearts,
  state: open|cleared|failed|abandoned, ended, asked, correct, xp_gained, stones_gained, items_gained,
  rewarded, room_reward, chest, chest_opened}`.
- `POST /math/dungeon/next {run_id}` -> `{"run", "question": <phiên câu hỏi, context "math_dungeon"> | null}`: vào
  phòng hiện tại / câu tiếp của phòng; câu đang chờ thì trả lại đúng câu đó. `question: null` khi một câu hết
  giờ vừa được chấm đã làm hết tâm lực. Khối `math` của câu có thêm `dungeon: {room, rooms, name_vi,
  guardian_vi, warden}`. Hầm đã kết thúc: 409 `run_ended`.
- `POST /math/dungeon/abandon {run_id}` -> `{"run"}`: rời hầm, giữ những gì đã nhận.
- `GET /math/dungeon/run/{run_id}` -> `{"run"}`: một hầm của người chơi (màn kết quả đọc số cuối ở đây).
- Trả lời: `POST /quiz/answer` như mọi câu. Khối `math` như M7 (ghi vào `math_answers`, `run_id = NULL`), và
  `dungeon: {correct, room, room_cleared, reward: {stones, items, withheld} | null, chest: (cùng dạng) | null,
  heart_lost, run}`; câu của hầm đã rời / đã chấm: `dungeon: {stale: true, run}` (chỉ ghi vào nhật ký học).

## M10 — Thủ thành toán (tháp ứng với mảng toán)

Thủ thành chạy ở client bằng `td_sim.py` (file giống hệt nhau ở `server/app/systems/` và `client/engine/`). Máy
chủ chọn hạt giống, gửi mọi số liệu, tự hỏi và chấm mọi câu hỏi, rồi chạy lại nhật ký của client trước khi trao
thưởng (`systems/td.py`). Lượt đang chơi ở bảng `td_runs`, sao ở `td_progress` (mã ải bắt đầu bằng `math_`; dòng
còn sót của Ải Thủ Vườn cũ không bao giờ hiện hay chơi tiếp, và bị xoá khi người chơi vào ải mới). Dữ liệu:
`server/data/math/td.json`. Mỗi tháp có một mảng toán (`subject`, `floor`, `skills`); tháp dùng được khi mảng có
câu và người chơi đã tới tầng ấy (`math_ask.open_floor`). Đặt tháp và nâng tháp mỗi lần cần một câu đúng của
mảng ấy, ở bậc của chính người chơi (không bao giờ cao hơn); sai / hết giờ thì không đặt / không nâng, Linh Khí
của lần thử không hoàn lại, ngoài ra không mất gì. Mọi câu ghi vào `math_answers`
với `run_id = NULL` và cho Tu Vi theo bậc.

- `GET /math/td` -> `{levels: [{id, name_vi, desc_vi, waves, unlocked, locked_vi, stars, best_wave, monsters,
  first_rewards: [{spirit_stones, items?: [{item, qty, name_vi}]} ×3]}], towers: [<tower>], roles, active_run:
  {run_id, level_id, name_vi, waves} | null, stars_need, daily_left, daily_max}`.
- `<tower>` = `{id, name_vi, label, role, desc_vi, power, cost, subject, subject_name_vi, floor, available,
  locked_vi}`; `locked_vi` nói vì sao chưa dựng được (tầng chưa tới, hoặc môn / tầng chưa có câu hỏi).
- `POST /math/td/start {level_id}` -> `{run_id, level_id, params, step_ms, max_speed, name_vi, monsters, towers}`.
  `params` = mọi số `td_sim` cần: lưới, đường đi, đá, Linh Mạch, `qi` (Khỉ đeo theo cộng thêm Linh Khí lúc
  vào ải), nâng cấp, `roles`, `monsters`, `waves`, `seed` và `plants` = các tháp dựng được (`{role, label, name_vi,
  power}`). Lượt đang dở bị thay. Lỗi: 404 `no_level`, 400 `locked`, 400 `no_tower`.
- `POST /math/td/question {run_id, kind, tower_id?}` -> một phiên câu hỏi `context: "math_td"` (khối `math` như
  M7) cộng `math_td: {kind, tower, power}`. `kind` = `place` / `upgrade` (câu về mảng của `tower_id`), `break`
  (đầu mỗi lúc nghỉ) / `tu_khi` (nút Tụ Khí): câu ở tầng của chính người chơi. `power` = hệ số sức mạnh theo bậc
  (`tier_power`) mà tháp nhận nếu trả lời đúng. Lỗi: 400 `no_tower` (tháp không mở trong lượt này), 400
  `no_question`, 400 `too_many`, 404 `no_run`.
- Trả lời: `POST /quiz/answer`. Kết quả có `math` (như M7) và `math_td: {kind, tower, ok, power, qi}`.
- Sự kiện trong nhật ký (mỗi sự kiện có `s` = số bước 50 ms lúc nó xảy ra; giữa các đợt thời gian không trôi):
  `{"k": "place", x, y, w, q}`: `q` bắt buộc là một câu `place` về đúng tháp `w`; câu đúng thì tháp đứng lên với
  `power` của câu, câu sai thì chỉ trừ Linh Khí. `{"k": "up", x, y, q}`: câu `upgrade` về đúng tháp ấy; đúng thì
  lên cấp và giữ `power` cao nhất. `{"k": "sell", x, y}`, `{"k": "qi", q}` (câu `break` / `tu_khi`), `{"k":
  "wave"}`. `q` là `session_id`; máy chủ dùng kết quả đúng/sai nó đã chấm. Mỗi câu chỉ dùng được một lần.
- `POST /math/td/event {run_id, start, events}`: lưu phần nhật ký từ chỉ số `start` -> `{saved}`; gửi lại đoạn đã
  lưu phải giống hệt (lỗi `log_conflict`, `log_gap`, `bad_log`, `too_many`). `POST /math/td/resume`: như
  `/math/td/start` cộng `events` (đã lưu) và `answers{session_id: {kind, word, ok, power}}`; câu hỏi sau lần lưu
  cuối bị bỏ (lỗi `no_run`). `POST /math/td/cancel`: bỏ lượt (không thưởng).
- `POST /math/td/finish {run_id, events, claim}` -> `{result, core_hp, wave, steps, waves_cleared, stars,
  prev_stars, new_stars, rewards, daily_left, next_level}`. Máy chủ chơi lại nhật ký với câu trả lời nó đã ghi;
  nhật ký có tháp không do câu đúng nào dựng nên, kết quả không khớp hay nhanh hơn thời gian thật: 400
  (`bad_log`, `log_mismatch`, `too_fast`) và lượt bị xoá. Thưởng: lần đầu đạt mỗi sao nhận `first_rewards` của
  ải; thắng lại nhận `replay_stones` Linh Thạch, tối đa `daily_rewarded_plays` lần mỗi ngày; thua không có thưởng.
  Lượt thắng tính cho nhiệm vụ `td_win`; Mặc Quái gặp được ghi vào Yêu Quái Phổ (`td_<loài>`). Lỗi thêm:
  `unfinished` (ải chưa kết thúc), `no_run`.

## M10 — Bí cảnh toán (tổ đội)

Bí cảnh của giai đoạn 9 (ghép đội, khe nứt, mỗi lượt một bản, phòng, hồn ma, khiên nhóm của boss, phần thưởng)
dùng lại nguyên vẹn, chỉ đổi *câu được hỏi*. Từ đợt xoá game chữ cũ, **mọi** bí cảnh trong `server/data/realms.json`
là bí cảnh toán; `kind` chỉ nói cách vào: `math` (Toán Trận Bí Cảnh `toan_tran`, mở suốt ở Cổng Bí Cảnh, một mình
hay cả đội), `scheduled` (Mặc Ảnh Động `mac_anh_dong`, giờ mở cửa, tổ đội 2-5, ba gian Trận Nhãn rồi boss), `rift`
(Khe Nứt Mực `khe_nut_muc`, chỉ vào qua khe nứt, tổ đội 2-5, một gian Trận Nhãn rồi boss). Không còn phòng câu đố chữ. Mọi câu — của Mặc Quái, của ấn Trận Nhãn, của boss — lấy bằng `math_ask.pick_own`: tầng và
bậc của chính người trả lời, không bao giờ theo tầng của quái hay của phòng. Câu có `context: "math_realm"` (khối
`math` như M7, thêm `realm_asker`: `monster` / `seal` / `boss`), trả lời qua `POST /quiz/answer`, ghi vào
`math_answers` với `run_id = NULL`, Tu Vi theo bậc; hết giờ là câu sai, ngoài ra không mất gì.

- `GET /realms`: mỗi hàng là `{id, name_vi, kind, math: true, floor, rooms, puzzles (số gian trước boss),
  time_limit_minutes, party_min, realm_ok, entries_left, daily, open, opens_in?, closes_in?, desc_vi}`; `realms` là
  hai bí cảnh tổ đội (`rift`, `scheduled`), `math_realms` là bí cảnh `math`. `floor` = tầng câu hỏi của người chơi
  (0: chưa có tầng nào có câu, `realm_ok` false). `puzzles` (bản giải thích) chỉ còn `seal` và `boss`.
- WebSocket `{"t": "realm", "op": "enter", "realm": "toan_tran"}` ở Cổng Bí Cảnh: một mình (không cần tổ đội,
  `party_min` 1) hoặc đội trưởng dẫn cả đội; không có giờ mở cửa, không đòi cảnh giới. Ai không có tầng nào có
  câu hỏi thì cả đội bị từ chối: lỗi `no_math_question`, không mất lượt. `op: "queue"` cũng dùng được.
- `realm start`: `run.math: true`, mỗi `members[]` có `floor`. `realm room`: thêm `place` (gian của bản đồ
  `bi_canh` mà phòng mượn) và `math`.
- Phòng `seal` (Trận Nhãn): `puzzle = {kind: "seal", seal_kind, seals: [{name, broken, busy}], broken, need,
  missing: [uid], solved, fails}`. Đứng lên một ấn chưa vỡ (`name` là tên đồ vật bản đồ) thì máy chủ gửi
  `{"t": "q", "mid": null, "seal": name, "q": ...}`; Hộ Thể khi đang trả lời. Kết quả `POST /quiz/answer` có
  `realm: {seal, broken, count?, need?, hurt?, hp?}` (hoặc `stale`). Mọi người nhận `{"t": "realm", "event":
  "seal", "ok", "by"}` và `{"k": "pz", "e": "ask" | "seal"}` trong snapshot. Cửa mở khi đã vỡ `need` ấn
  (`seal.base` + `seal.per_member` cho mỗi thành viên khác hỏi được, tối đa số ấn của gian) và ít nhất
  min(số thành viên, need) người khác nhau đã phá một ấn. Người đã phá một ấn bị từ chối ấn tiếp theo nếu lấy
  nó thì không đủ ấn cho người chưa phá: `{"t": "realm", "event": "hint", "code": "seal_share"}`.
- Boss: mỗi người được hỏi "bài tổng hợp" của mình (`pick_own(highest=True)`); khiên lớn cần mỗi người còn sống
  (trừ người không có câu nào) trả lời đúng một câu. Dạng boss muốn hỏi (`boss_question.prefer:
  "find_mistake"`, Tìm chỗ sai) chơi được từ M11; ai không có câu dạng ấy ở bậc của mình thì nhận bài tổng hợp,
  không bao giờ là một Thiên kiếp (M11 đợt 2: một câu 8-12 phút không hợp với bí cảnh 15-20 phút).
- Người chơi mà ngân hàng không có câu: `{"t": "error", "code": "no_math_question"}`; phòng và khiên boss không
  chờ người đó.
- Thưởng: như bí cảnh cũ (`realm loot`), nhưng chỉ Linh Thạch, vật liệu của `data/math/drops.json` và Linh Quả
  (`room_loot_by_realm.<id>`, `chest.<id>` trong `balance/realm.json`, cho cả ba bí cảnh), không Tu Vi, không Ngọc.
  Mảnh Bảo Vật được phép lại từ 2026-11-20 (rương Mặc Ảnh Động). Mọi món đều theo mốc tu vi
  (`data/loot_tiers.json`): món chưa mở không trao mà nằm trong `locked: [{name_vi, need_vi}]` của gói loot.
- Tin `ract` (đánh đồ vật trong phòng câu đố chữ) đã bỏ khỏi giao thức (2026-11-20).

## M11 — Sảnh toán bốn bí cảnh, bài kiểm tra đầu vào (agent HUB)

Luật 7 của lộ trình: bài kiểm tra đầu vào, tùy chọn, mỗi bí cảnh một lần. Luật chi tiết nằm ở docstring của
`server/app/systems/math_placement.py`, mọi con số ở `balance/math.json` → `placement_test` (`min_questions` 10,
`max_questions` 15, `per_floor` 5, `pass_pct` 80, `retake_after_days` 7). Một lần làm là một `math_runs` với
`mode: "placement"`; câu hỏi có `context: "math_placement"`, trả lời qua `POST /quiz/answer`, ghi vào
`math_answers` với `run_id` của lần làm đó; Tu Vi theo bậc như mọi câu, không tâm ma, không đổi bậc, không cơ duyên.

- `GET /math/placement?subject_id=` → `{subject_id, subject_name_vi, status: "offered" | "in_progress" | "done" |
  "unavailable", offered, reason: null | "few_floors" | "cleared" | "done" | "retake", planned, written_floors[],
  pass_pct, run?, progress?, result?}`. `progress = {total, asked, correct, left, decided, start_floor,
  floors[{floor, planned, asked, correct, needed, met}]}` (`met`: true / false / null = chưa rõ). `result =
  {start_floor, abandoned, skipped[], asked, correct, floors[{floor, planned, asked, correct, needed, met}],
  finished_at, retake_at}`. Được mời khi: chưa qua Thiên kiếp nhỏ tầng nào của bí cảnh, chưa có lần làm nào (hoặc
  lần trước xếp ở tầng 1 / bỏ dở, đã qua `retake_after_days` ngày), và bí cảnh có ít nhất 2 tầng chính có câu.
  Lỗi `no_subject` (404).
- `POST /math/placement/start {subject_id}` → `{run, progress}`; `run.placement = {total, asked, correct, left,
  decided, start_floor}`. Không được mời: `placement_not_offered` (409). Không kết thúc buổi luyện đang dở.
- `POST /math/placement/next {run_id}` → `{run, question, progress}`: câu đang mở (nếu còn giờ) hoặc câu tiếp theo
  của kế hoạch (tầng thấp lên cao, trong một tầng bậc thấp lên cao). Câu không ai trả lời mà hết giờ được tính là
  sai (hết giờ) ngay lúc này. Đã có kết quả thì `question: null` và có thêm `result`. Lỗi `no_run` (404),
  `run_ended` (409).
- `POST /math/placement/abandon {run_id}` → trạng thái như `GET /math/placement`: bỏ dở, không tầng nào được miễn.
  `POST /math/run/end` trên lần làm này cũng là bỏ dở; `POST /math/run/next` trên nó: `wrong_mode` (409).
- Kết quả `POST /quiz/answer` của câu kiểm tra: `math = {tier, timed_out, parallel: false, parallel_waiting:
  false, review: false, tier_change: 0, xp_base, placement: progress, run, placement_result?}`;
  `placement_result` (như `result`) có mặt khi câu này quyết định kết quả. Dừng sớm ngay khi một tầng không thể
  đạt mức nữa.
- `GET /math/path`: mỗi bí cảnh có thêm `placement = {status, offered, planned, run_id, start_floor, abandoned}`;
  mỗi tầng có thêm `cleared_by: null | "trial" | "placement"`. `cleared[]` và `next_floor` tính cả các tầng được
  miễn, và mọi chế độ hỏi "người chơi đang ở tầng nào" (`math_ask.open_floor`: bí cảnh, hầm ngục, cơ duyên, thủ
  thành, chiêu thức) đọc cùng một nguồn `math_practice.cleared_floors`. `run` (buổi đang dở) không bao giờ là một
  lần kiểm tra đầu vào.

## M11 đợt 2 — Bậc thang của câu bậc 5, kiểm tra đầu vào cho chín tầng (agent LADDER)

**Luật 8, bậc thang** (luật chi tiết: docstring của `server/app/systems/math_practice.py`; dữ liệu: `ladder` của
câu viết tay bậc 5, xem `server/app/learning/math_items.py`). Bảng mới `math_ladders` (migration
`0015_math_ladder`), cột mới `math_runs.ladders`.

- `run` (mọi chỗ trả về `run_view`) có thêm `ladders`: số bậc thang đã leo xong trong buổi luyện này.
- Câu hỏi là một bậc thang: `question.math.ladder = {of, step, steps}` (`of` = id câu bậc 5 vừa sai, `step` = bậc
  này, đếm từ 1). Câu thường không có khoá này.
- Kết quả `POST /quiz/answer` trong buổi luyện (`context: "math"`, `mode: "practice"`):
  - câu bậc 5 viết tay trả lời sai (hoặc hết giờ) mở bậc thang: `math.ladder = {of, step: 0, steps, started:
    true, rung: false, done: false}`;
  - trả lời một bậc: `math.ladder = {of, step, steps, rung: true, done, missed, returns}` (`step` = số bậc đã
    trả lời, `missed` = số bậc sai, `returns` = câu bậc 5 sẽ quay lại ngay câu sau, tức bậc thang leo sạch);
  - câu khác: không có `math.ladder`.
- Thứ tự câu của buổi luyện: bậc tiếp theo của bậc thang đang leo ở tầng này → câu song song của lỗi sai (tâm ma;
  lỗi bậc 5 bị giữ lại khi bậc thang chưa xong, hoặc khi đã sai một bậc thì chờ buổi sau; leo sạch thì nó đi
  trước) → câu ôn → câu thường. Thiên kiếp nhỏ, kiểm tra đầu vào và các chế độ khác không mở bậc thang.

**Kiểm tra đầu vào cho chín tầng** (luật chi tiết: docstring của `server/app/systems/math_placement.py`).
`balance/math.json` → `placement_test` thêm `block_min` 3; `per_floor` 5 nay là số câu nhiều nhất của một khối.

- Leo theo khối: mỗi tầng được hỏi một khối `block` câu (bậc thấp lên cao); đạt thì nhảy `stride` tầng có câu,
  không đạt thì dừng và lùi từng tầng để xác nhận những tầng đã nhảy qua. 3 tầng: khối 4 câu, mọi tầng; 6 tầng:
  khối 3, tầng 1-3-5-6; 9 tầng: khối 3, tầng 1-4-7-9. Không lần làm nào quá `max_questions`.
- `GET /math/placement`: thêm `block`, `stride`; `planned` = số câu nhiều nhất một lần làm có thể hỏi.
  `progress` thêm `block`, `stride`; `total` = số câu nhiều nhất, `left` = số câu còn có thể hỏi nhiều nhất;
  `progress.floors[]` = các khối đã hỏi, theo thứ tự hỏi. `result.floors[]` = chỉ các tầng đã được hỏi, tầng thấp
  trước; tầng nhảy qua nằm trong `skipped[]`.
- Câu Thiên kiếp (`tribulation`) không bao giờ là câu kiểm tra đầu vào; tầng chỉ có câu Thiên kiếp không tính là
  tầng có câu.

## Lộ trình tân thủ (guide)

Dữ liệu: `server/data/guide.json` (chương → bước, Cẩm nang, lời chào của Trúc Lão). Mã: `app/systems/guide.py`,
`app/routers/guide_routes.py`. Kiểm: `python tools/check_guide.py` (cũng chạy trong `tools/check_all.py`).
Tiến độ của mọi bước **suy ra từ dữ liệu đã có** (câu trả lời, buổi luyện, Thiên kiếp nhỏ, vị trí trên Đạo Thụ,
hầm ngục, thủ thành, cơ duyên, bài tập, cảnh giới); máy khách chỉ báo vài việc "đã xem". Trạng thái riêng của
người chơi nằm trong `users.flags["guide"] = {claimed: [id], seen: [key]}`. Bước không bao giờ bị khoá: bản lưu
cũ có thể thấy nhiều bước đã xong và nhận hết. Kiểu kiểm tra: `seen`, `math_answers`, `practice_runs`,
`trials_passed`, `nodes_done`, `node_done`, `tree_stage`, `placement_done`, `mistakes_cleared`,
`dungeon_cleared`, `td_wins`, `fortune_won`, `code_solved`, `skills_unlocked`, `realm` (tham số và ý nghĩa: docstring
và `CHECKS` của `guide.py`).

- `GET /guide` -> `{title_vi, welcome: {seen, speaker_vi, lines_vi[]}, chapters[{id, title_vi, intro_vi, done,
  total, state: "active" | "done" | "claimed", rewards_vi[], steps[{id, chapter_id, title_vi, desc_vi, how_vi[],
  goto: "math" | "library" | "dungeon" | "td" | "fortune" | "char" | null, help: <id trang Cẩm nang> | null,
  optional, state: "active" | "done" | "claimed", progress, count, rewards_vi[], nodes[]}]}], current: {chapter_id,
  step_id, title_vi, hint_vi, progress, count, goto} | null, claimable, study: {action: "resume" | "practice" |
  "trial" | "code", node_id, name_vi, branch_vi, floor, text_vi} | null, stage: {realm, realm_name_vi, stage,
  stages}, handbook[{id, title_vi, lines_vi[]}]}`.
  - Bước `done` = đã đạt, chưa nhận thưởng. Chương `done` = mọi bước bắt buộc đã xong, chưa nhận thưởng chương;
    chương không có thưởng đi thẳng từ `active` sang `claimed`. `done`/`total` của chương chỉ đếm bước bắt buộc.
  - Bước `optional` không chặn `current` và thưởng chương. `current` = bước bắt buộc đầu tiên (theo thứ tự
    file) còn `active`; `hint_vi` = dòng đầu của `how_vi`. `claimable` = số bước + chương đang `done`.
  - Chương sinh từ Đạo Thụ (`"generated": "tree_stages"`): một bước mỗi tầng của cảnh giới, id
    `<id chương>_s<k>`; xong khi tầng đạt được trên cây >= k; `progress/count` = số nút chính đạo có nội dung
    đã xong / tổng số nút ấy của các tầng 1..k (nút "đang biên soạn" không tính); `nodes[] = [{id, name_vi,
    branch, branch_vi, state: "open" | "done" | "locked" | "vacant"}]` = các nút chính đạo của đúng tầng k. Bước
    thường: `nodes: []`.
  - `study` = học gì trên Đạo Thụ lúc này: buổi luyện / Thiên kiếp nhỏ đang dở -> `resume`; không thì nút chính
    đạo đang mở đầu tiên (thứ tự cây), phần đầu tiên chưa vượt: `trial` nếu cổng thuần thục của phần ấy đã mở,
    không thì `practice`; nút chỉ còn bài tập lập trình -> `code` (`floor` = tầng của bài đầu tiên chưa giải).
    Không có nút nào mở: `null`.
- `POST /guide/claim {id}` (id bước hoặc chương) -> `{claimed, rewards: {spirit_stones?, immortal_jade? (số dư
  mới), xp?: <kết quả add_xp>, items[{item, name_vi, qty, total}], equipment: []}, guide: <như GET /guide>}`.
  Lỗi `no_step` (404), `not_done` (400), `already_claimed` (400), `busy` (409, hiếm: cờ bị đổi liên tục, thử lại).
  Mỗi lần nhận để lại một dòng `audit_log` (`reason: "guide"`, `ref_id` = id); cờ được ghi bằng so-sánh-rồi-đổi
  trên cả cột `flags`, nên hai yêu cầu cùng lúc chỉ trả thưởng một lần.
- `POST /guide/seen {key}` -> `{guide: <như GET /guide>}`. Khoá nhận: `welcome`, `board`, và mọi `key` mà một
  bước `seen` của guide.json dùng (máy khách gửi `math_hub`, `library_doc`, `village`); khoá khác: `bad_key`
  (400). Gửi lại không sao.
