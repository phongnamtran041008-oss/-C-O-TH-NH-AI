# Thành Tựu

Tác giả: "Mình muốn có thành tựu." Và: xem truyện tranh tu tiên còn thiếu gì thì làm, làm kỹ, làm đẹp. Đây là
một trò ôn toán cho ngành AI, nên thành tựu trước hết làm người chơi tự hào về việc *học* (trả lời đúng khi bị
dồn ép, liền mạch không sai, nút Đạo Thụ, bài lập trình, Xạ Trường), rồi mới tới chiến đấu, sưu tầm, khám phá.

Mã: `server/app/systems/achievements.py`. Dữ liệu: `server/data/achievements.json`. Đường REST:
`server/app/routers/achievement_routes.py` (`docs/API.md`). Tin websocket `achievement` (`docs/PROTOCOL.md`).
Client: `client/scenes/achievements.py` (Thành Tựu Lục, phím V), `client/ui/achievement_toast.py` (dải vàng).
Kiểm: `achievements.validate()` trong `tools/check_all.py`; test `server/tests/test_achievements.py`,
`client/tests/test_achievement_flow.py` (ảnh ở `art/preview/thanh_tuu_*.png`).

## Cách đếm

- **Một cửa vào.** Nơi việc xảy ra gọi `achievements.on_event(db, uid, event, n, **ctx)` (đã có phiên CSDL) hoặc
  `achievements.bump(uid, event, n, **ctx)` (vòng tick của thế giới: Phản Đòn, lướt kiếm, vào vùng; gom trong bộ
  nhớ, khoảng một giây sau mới ghi một lần, nên một trận đánh không tốn truy vấn mỗi đòn). Mỗi lời gọi một dòng.
- **Bộ đếm, không quét.** `achievement_counters` giữ một số cho mỗi người chơi và mỗi khóa: tổng (`kill`), tổng có
  lọc (`kill|rank=boss`), giá trị tốt nhất (`answer_streak`, `cult`), và với đếm khác loại thì một dòng đánh dấu
  cho mỗi giá trị (`zones#loi_kiep_dai`). Chỉ ghi khóa mà có thành tựu đọc. Vượt mốc được nhận ra từ giá trị cũ và
  mới; chỉ lúc đó mới đọc dòng `achievements`.
- **Không dùng SAVEPOINT**: với pysqlite một SAVEPOINT mở đầu giao dịch sẽ tự commit khi RELEASE, nên dòng mới được
  thêm bằng `INSERT ... ON CONFLICT DO NOTHING` (SQLite và PostgreSQL), cùng giao dịch với việc được đếm.
- **Báo cho người chơi.** Bậc vừa đạt được lưu với `seen` thấp hơn `tier`. Tin `{"t": "achievement"}` chỉ được gửi
  sau khi giao dịch commit (nghe sự kiện `after_commit` của SQLAlchemy; rollback thì bỏ). Client hiện dải vàng rồi
  gửi `POST /achievements/seen`; lúc đăng nhập client hỏi `GET /achievements/new` để lấy những gì đạt khi vắng mặt.
  Không mất, không báo hai lần (client cũng nhớ khóa `id:tier` trong phiên).
- **Người chơi cũ.** Lần đầu xem (GET `/achievements` hoặc `/achievements/new`) máy chủ điền bộ đếm từ những gì
  CSDL đã biết: cảnh giới, số quái đã hạ trong Yêu Quái Phổ, binh khí, linh thú, linh căn, Thiên kiếp nhỏ đã qua,
  nút Đạo Thụ, lò đan. Những bậc đạt nhờ vậy mở lặng lẽ (không dải vàng) nhưng vẫn nhận thưởng được. Mỗi lần xem
  còn đối chiếu lại: thành tựu thêm ở bản sau bắt đầu đúng chỗ người chơi đang đứng.

## Sự kiện (RAW) và nơi gửi

| Sự kiện | Nơi gửi | Bộ đếm |
|---|---|---|
| `answer` | learning/quiz.answer | answer_right (theo context), answer_fast, answer_streak, answer_clutch, answer_night, answer_comeback |
| `quest` | systems/quests.on_event (kill, meditate, fish, td_win) | kill (rank, subject, land, monster), kill_kinds, meditate, fish, td_win |
| `cult` | systems/cultivation.add_xp (a stage or realm up) | cult |
| `tribulation` | systems/cultivation.tribulation_handler (Thiên Kiếp passed) | tribulation, cult |
| `trial` | systems/math_practice._trial_after_answer (a Thiên kiếp nhỏ passed) | trial_pass, tree_nodes |
| `code` | systems/math_code.judge (Nộp bài) | code_solved, xa_truong, xa_truong_top |
| `gear` | systems/items.grant_equipment (every piece of equipment granted) | weapon_get (type, quality), weapon_types |
| `weapon_claim` | systems/weapons.claim | weapon_claim |
| `weapon_forge` | systems/weapons.upgrade | weapon_forge (quality) |
| `beast_tame` | systems/beasts.seal | beast_tame (beast) |
| `linh_can` | systems/linh_can.awaken / roll / choose | lc_giai, lc_carry, lc_book, lc_test |
| `brew` | systems/alchemy.finish | brew (quality), pill_made |
| `furnace` | systems/alchemy.upgrade_furnace | furnace |
| `currency` | systems/inventory.change_currency | stones_earned, stones_spent, jade_earned (trừ thưởng của chính Thành Tựu) |
| `realm_clear` | systems/secret_realm.claim_chest | realm_clear |
| `kill_flawless` | realtime/combat.kill (bump) | kill_flawless (rank) |
| `parry` | realtime/combat._parry (bump) | parry, parry_combo |
| `death` | realtime/combat.die (bump) | death |
| `zone` | realtime/world.put (bump) | zones, lands (land) |
| `glide` | realtime/abilities.apply_glide (bump) | glide |
| `formation` | realtime/abilities.place_formation (bump) | formation |
| `ride` | realtime/abilities.apply_ride (bump) | ride |
Mỗi sự kiện phải có một nơi gửi thật trong `server/app` (`validate()` tìm lời gọi trong mã). Khi chạy cả bộ test
máy chủ, `conftest.py` kiểm thêm rằng mỗi sự kiện đã được một test gửi (`achievements.FIRED`).

## Phần thưởng theo tu vi

Linh thạch, tiên ngọc, vật phẩm có mốc trong `loot_tiers.json` và danh hiệu. Mỗi bậc có `req` (một cảnh giới tu
luyện, mặc định là mốc cao nhất của các vật phẩm trong thưởng; với thành tựu cảnh giới là chính cảnh giới ấy):
chưa tới `req` thì bậc đã đạt nhưng thưởng chờ (`403 locked`, "Nhận hết" bỏ qua). `validate()` giữ mọi vật phẩm
không vượt `req` của bậc. Danh hiệu trao ngay khi đạt (ghi vào `users.flags.titles`, như danh hiệu của Tàng Thư
Các) và mang bằng `POST /books/wear`; `books._earnable()` nhận cả danh hiệu của Thành Tựu.

## Đạo Tâm và các mốc

Mỗi bậc cho điểm Đạo Tâm, tính ngay khi đạt. Các mốc:

| Đạo Tâm | Thưởng |
|---|---|
| 50 | 500 Linh Thạch, Hồi Huyết Đan x5 |
| 150 | 1500 Linh Thạch, 10 Tiên Ngọc, Danh hiệu «Đạo Tâm Sơ Thành» |
| 400 | 4000 Linh Thạch, 25 Tiên Ngọc |
| 800 | 8000 Linh Thạch, 50 Tiên Ngọc, Danh hiệu «Đạo Tâm Kiên Định» |
| 1500 | 15000 Linh Thạch, 100 Tiên Ngọc |
| 2500 | 25000 Linh Thạch, 200 Tiên Ngọc, Danh hiệu «Đạo Tâm Thông Minh» |
| 4000 | 50000 Linh Thạch, 400 Tiên Ngọc, Danh hiệu «Đạo Tâm Viên Mãn» |
Tổng điểm có thể đạt: 6280.

## Bảng thành tựu (100)

Ẩn = thẻ Bí Ẩn, hiện "???" và một câu gợi ý cho tới khi đạt. Bậc: mốc / tên bậc / Đạo Tâm / thưởng.

| Loại | id | Tên | Bộ đếm | Bậc |
|---|---|---|---|---|
| Tu Luyện | `cult_luyen_khi` | Dẫn Khí Nhập Thể | `cult` | Luyện Khí tầng 1 / Dẫn Khí Nhập Thể / 5 / 100 Linh Thạch, Hồi Khí Đan x3 (cần Luyện Khí tầng 1)<br>Luyện Khí tầng 5 / Khí Hải Sơ Thành / 10 / 300 Linh Thạch, Tẩy Linh Thảo x2 (cần Luyện Khí tầng 1)<br>Luyện Khí tầng 9 / Luyện Khí Viên Mãn / 20 / 600 Linh Thạch, Tẩy Linh Đan x1 (cần Luyện Khí tầng 1) |
| Tu Luyện | `cult_truc_co` | Trúc Cơ Thành Công | `cult` | Trúc Cơ sơ kỳ / Trúc Cơ Sơ Kỳ / 5 / 1000 Linh Thạch, 5 Tiên Ngọc, Linh Tủy Tinh x2, Danh hiệu «Trúc Cơ Tu Sĩ» (cần Luyện Khí tầng 3)<br>Trúc Cơ trung kỳ / Trúc Cơ Trung Kỳ / 10 / 1500 Linh Thạch<br>Trúc Cơ hậu kỳ / Trúc Cơ Hậu Kỳ / 20 / 2000 Linh Thạch, 10 Tiên Ngọc, Thiên Linh Quả x2 (cần Luyện Khí tầng 6) |
| Tu Luyện | `cult_kim_dan` | Kết Thành Kim Đan | `cult` | Kết Đan sơ kỳ / Kim Đan Sơ Thành / 5 / 3000 Linh Thạch, 15 Tiên Ngọc, Thiên Linh Đan x1, Danh hiệu «Kim Đan Chân Nhân» (cần Trúc Cơ sơ kỳ)<br>Kết Đan hậu kỳ / Kim Đan Đại Thành / 10 / 4000 Linh Thạch, 15 Tiên Ngọc |
| Tu Luyện | `cult_nguyen_anh` | Nguyên Anh Xuất Khiếu | `cult` | Nguyên Anh sơ kỳ / Nguyên Anh Sơ Sinh / 5 / 5000 Linh Thạch, 20 Tiên Ngọc, Tạo Hóa Đan x1 (cần Kết Đan sơ kỳ)<br>Nguyên Anh hậu kỳ / Nguyên Anh Viên Mãn / 10 / 6000 Linh Thạch, 20 Tiên Ngọc |
| Tu Luyện | `cult_hoa_than` | Hóa Thần Thông Huyền | `cult` | Hóa Thần sơ kỳ / Hóa Thần Thông Huyền / 5 / 8000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Hóa Thần Tôn Giả» |
| Tu Luyện | `cult_luyen_hu` | Luyện Hư Hợp Đạo | `cult` | Luyện Hư sơ kỳ / Luyện Hư Hợp Đạo / 5 / 10000 Linh Thạch, 40 Tiên Ngọc |
| Tu Luyện | `cult_hop_the` | Hợp Thể Thiên Nhân | `cult` | Hợp Thể sơ kỳ / Hợp Thể Thiên Nhân / 5 / 12000 Linh Thạch, 50 Tiên Ngọc |
| Tu Luyện | `cult_dai_thua` | Đại Thừa Chi Cảnh | `cult` | Đại Thừa sơ kỳ / Đại Thừa Sơ Kỳ / 160 / 15000 Linh Thạch, 60 Tiên Ngọc, Danh hiệu «Đại Thừa Chân Quân»<br>Đại Thừa hậu kỳ / Đại Thừa Viên Mãn / 250 / 20000 Linh Thạch, 100 Tiên Ngọc, Danh hiệu «Vô Thượng Chí Tôn» |
| Tu Luyện | `tribulation` | Nghịch Thiên Độ Kiếp | `tribulation` | 1 / Vượt Kiếp Đầu / 5 / 500 Linh Thạch<br>3 / Tam Độ Lôi Kiếp / 10 / 1500 Linh Thạch, 10 Tiên Ngọc<br>6 / Lục Kiếp Bất Hoại / 20 / 3000 Linh Thạch, 25 Tiên Ngọc, Danh hiệu «Lôi Kiếp Bất Diệt» |
| Tu Luyện | `meditate` | Tĩnh Tọa Ngộ Tâm | `meditate` | 10 / Tĩnh Tâm / 5 / 100 Linh Thạch, Hồi Huyết Đan x3<br>100 / Nhập Định / 10 / 600 Linh Thạch<br>500 / Thiền Tâm Như Nước / 20 / 2000 Linh Thạch |
| Tu Luyện | `tree_nodes` | Đạo Thụ Khai Hoa | `tree_nodes` | 1 / Mầm Đạo / 10 / 100 Linh Thạch<br>5 / Cành Non / 20 / 400 Linh Thạch, 5 Tiên Ngọc<br>15 / Tán Lá / 40 / 1200 Linh Thạch, 10 Tiên Ngọc<br>40 / Đại Thụ / 80 / 3000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Người Vun Đạo Thụ»<br>80 / Đạo Thụ Thông Thiên / 160 / 6000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Đạo Thụ Thông Thiên» |
| Tu Luyện | `trial_pass` | Vượt Thiên Kiếp Nhỏ | `trial_pass` | 1 / Qua Kiếp Đầu / 10 / 150 Linh Thạch, Hồi Huyết Đan x2<br>10 / Thập Kiếp / 20 / 800 Linh Thạch, 5 Tiên Ngọc<br>30 / Tam Thập Kiếp / 40 / 2000 Linh Thạch, 15 Tiên Ngọc<br>60 / Lục Thập Kiếp / 80 / 4000 Linh Thạch, 30 Tiên Ngọc |
| Ngộ Đạo | `answer_right` | Vấn Đạo Cầu Chân | `answer_right` | 10 / Sơ Khai Linh Trí / 5 / 100 Linh Thạch, Hồi Huyết Đan x3<br>100 / Học Hải Vô Nhai / 15 / 500 Linh Thạch, 5 Tiên Ngọc<br>500 / Bác Lãm Quần Thư / 30 / 1500 Linh Thạch, 10 Tiên Ngọc<br>2.000 / Thông Thiên Triệt Địa / 60 / 4000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Bác Học Chân Nhân»<br>10.000 / Vạn Pháp Quy Tông / 120 / 10000 Linh Thạch, 80 Tiên Ngọc, Danh hiệu «Vạn Pháp Quy Tông» |
| Ngộ Đạo | `answer_streak` | Liên Hoàn Ngộ Đạo | `answer_streak` | 5 / Ngũ Liên / 5 / 100 Linh Thạch<br>10 / Thập Liên / 10 / 300 Linh Thạch<br>20 / Nhị Thập Liên / 25 / 800 Linh Thạch, 5 Tiên Ngọc<br>50 / Ngũ Thập Liên / 60 / 2500 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Tâm Như Chỉ Thủy»<br>100 / Bách Liên Bất Bại / 120 / 6000 Linh Thạch, 50 Tiên Ngọc, Danh hiệu «Đạo Tâm Bất Động» |
| Ngộ Đạo | `answer_fast` | Tâm Nhanh Như Điện | `answer_fast` | 10 / Nhanh Trí / 5 / 100 Linh Thạch<br>100 / Điện Quang Hỏa Thạch / 10 / 600 Linh Thạch, 5 Tiên Ngọc<br>500 / Thần Tốc / 20 / 2000 Linh Thạch, 15 Tiên Ngọc<br>2.000 / Nhất Niệm Vạn Lý / 40 / 5000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Nhất Niệm Thông Thiên» |
| Ngộ Đạo | `ans_practice` | Khổ Luyện Tàng Kinh | `answer_right` context=math | 50 / Siêng Năng / 5 / 200 Linh Thạch, Hồi Huyết Đan x3<br>300 / Khổ Luyện / 10 / 1000 Linh Thạch<br>1.500 / Thiết Trụ Ma Thành Châm / 20 / 3000 Linh Thạch |
| Ngộ Đạo | `ans_combat` | Lâm Trận Bất Loạn | `answer_right` context=math_combat | 20 / Bình Tĩnh / 5 / 200 Linh Thạch<br>200 / Lâm Nguy Bất Loạn / 10 / 1200 Linh Thạch, 5 Tiên Ngọc<br>1.000 / Thái Sơn Băng Tiền / 20 / 4000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Thái Sơn Bất Động» |
| Ngộ Đạo | `ans_tribulation` | Lôi Hạ Ngộ Đạo | `answer_right` context=math_tribulation | 10 / Sấm Bên Tai / 5 / 300 Linh Thạch<br>60 / Lôi Đình Ngộ Đạo / 10 / 1500 Linh Thạch, 10 Tiên Ngọc |
| Ngộ Đạo | `ans_dungeon` | Hầm Ngục Giải Đề | `answer_right` context=math_dungeon | 20 / Kẻ Dò Đường / 5 / 200 Linh Thạch<br>150 / Chủ Nhân Hầm Ngục / 10 / 1200 Linh Thạch |
| Ngộ Đạo | `ans_td` | Thủ Thành Toán Sư | `answer_right` context=math_td | 20 / Thợ Dựng Tháp / 5 / 200 Linh Thạch<br>150 / Toán Sư Giữ Thành / 10 / 1200 Linh Thạch |
| Ngộ Đạo | `ans_fortune` | Cơ Duyên Tự Đến | `answer_right` context=math_fortune | 10 / Có Duyên / 5 / 200 Linh Thạch<br>80 / Phúc Duyên Thâm Hậu / 10 / 1000 Linh Thạch |
| Ngộ Đạo | `ans_skill` | Chiêu Thức Như Ý | `answer_right` context=math_skill | 20 / Ra Chiêu / 5 / 200 Linh Thạch<br>200 / Chiêu Chiêu Trúng Đích / 10 / 1200 Linh Thạch, 5 Tiên Ngọc<br>1.000 / Tâm Kiếm Hợp Nhất / 20 / 4000 Linh Thạch, 20 Tiên Ngọc |
| Ngộ Đạo | `ans_fishing` | Câu Đề Bên Hồ | `answer_right` context=math_fishing | 10 / Thả Câu / 5 / 100 Linh Thạch<br>100 / Lão Ngư Thông Toán / 10 / 800 Linh Thạch |
| Ngộ Đạo | `ans_meditate` | Tọa Thiền Vấn Tâm | `answer_right` context=math_meditate | 10 / Vấn Tâm / 5 / 100 Linh Thạch<br>100 / Minh Tâm Kiến Tánh / 10 / 800 Linh Thạch |
| Ngộ Đạo | `ans_realm` | Trận Nhãn Phá Giải | `answer_right` context=math_realm | 10 / Phá Trận / 5 / 200 Linh Thạch<br>100 / Trận Pháp Đại Sư / 10 / 1200 Linh Thạch |
| Ngộ Đạo | `ans_placement` | Khảo Hạch Nhập Môn | `answer_right` context=math_placement | 10 / Khảo Hạch Nhập Môn / 5 / 200 Linh Thạch |
| Ngộ Đạo | `code_solved` | Kiếm Tu Mã Đạo | `code_solved` | 1 / Dòng Lệnh Đầu / 10 / 200 Linh Thạch<br>5 / Ngũ Bài Đắc Đạo / 20 / 1000 Linh Thạch, 5 Tiên Ngọc<br>15 / Mã Đạo Tinh Thông / 40 / 3000 Linh Thạch, 15 Tiên Ngọc<br>40 / Mã Thánh / 80 / 8000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Mã Đạo Chân Tiên» |
| Ngộ Đạo | `xa_truong` | Xạ Trường Trúng Đích | `xa_truong` | 1 / Trúng Bia / 5 / 300 Linh Thạch<br>5 / Thiện Xạ / 10 / 2000 Linh Thạch, 10 Tiên Ngọc |
| Ngộ Đạo | `xa_truong_top` | Bách Phát Bách Trúng | `xa_truong_top` | 1 / Thượng Phẩm Xạ Thủ / 5 / 800 Linh Thạch, 5 Tiên Ngọc<br>3 / Thần Tiễn Thủ / 10 / 3000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Bách Phát Bách Trúng» |
| Chiến Đấu | `kill` | Trảm Yêu Trừ Ma | `kill` | 1 / Sơ Thí Đao Phong / 5 / 50 Linh Thạch, Hồi Huyết Đan x2<br>50 / Trảm Yêu Bách Lý / 15 / 400 Linh Thạch<br>500 / Ngàn Yêu Bạt Vía / 30 / 2000 Linh Thạch, 10 Tiên Ngọc<br>2.000 / Vạn Yêu Khiếp Đảm / 60 / 5000 Linh Thạch, 25 Tiên Ngọc, Danh hiệu «Yêu Ma Khắc Tinh»<br>10.000 / Sát Thần / 120 / 12000 Linh Thạch, 60 Tiên Ngọc, Danh hiệu «Sát Thần Vô Song» |
| Chiến Đấu | `kill_elite` | Tinh Anh Khắc Tinh | `kill` rank=elite | 10 / Phá Tinh Anh / 5 / 300 Linh Thạch<br>100 / Bách Tinh Anh / 10 / 1500 Linh Thạch, 10 Tiên Ngọc<br>500 / Tinh Anh Khiếp Sợ / 20 / 5000 Linh Thạch, 25 Tiên Ngọc |
| Chiến Đấu | `kill_boss` | Trảm Thủ Lĩnh | `kill` rank=boss | 1 / Thí Thủ Lĩnh / 10 / 500 Linh Thạch, 5 Tiên Ngọc<br>10 / Thập Vương Bại / 30 / 3000 Linh Thạch, 20 Tiên Ngọc<br>50 / Thí Vương Giả / 80 / 10000 Linh Thạch, 50 Tiên Ngọc, Danh hiệu «Thí Vương Giả» |
| Chiến Đấu | `kill_dstt` | Diệt Ma Đại Số | `kill` subject=dai_so_tuyen_tinh | 20 / Phá Ma Ma Trận / 5 / 300 Linh Thạch<br>200 / Đại Số Thanh Tẩy / 10 / 2000 Linh Thạch |
| Chiến Đấu | `kill_kiem_trung` | Kiếm Trủng Trảm Linh | `kill` land=kiem_trung_son | 20 / Vào Kiếm Trủng / 5 / 300 Linh Thạch<br>200 / Kiếm Trủng Chi Chủ / 10 / 2000 Linh Thạch |
| Chiến Đấu | `kill_luu_van` | Lưu Vân Quét Mây | `kill` land=luu_van_coc | 20 / Vén Mây / 5 / 300 Linh Thạch<br>200 / Lưu Vân Thanh Bình / 10 / 2000 Linh Thạch |
| Chiến Đấu | `kill_me_do` | Mê Độ Phá Chướng | `kill` land=me_do_lam | 20 / Lạc Lối Không Sợ / 5 / 300 Linh Thạch<br>200 / Mê Độ Thông Lộ / 10 / 2000 Linh Thạch |
| Chiến Đấu | `kill_tam_ma` | Trảm Tâm Ma | `kill` monster=tam_ma | 1 / Đối Diện Tâm Ma / 5 / 500 Linh Thạch<br>20 / Tâm Ma Tận Diệt / 10 / 2500 Linh Thạch, 10 Tiên Ngọc |
| Chiến Đấu | `kill_loi_long` | Đồ Long Giả | `kill` monster=loi_long | 1 / Đồ Long / 40 / 2000 Linh Thạch, 10 Tiên Ngọc, Danh hiệu «Đồ Long Giả»<br>5 / Ngũ Long Phục Thủ / 100 / 8000 Linh Thạch, 40 Tiên Ngọc |
| Chiến Đấu | `parry` | Lấy Nhu Chế Cương | `parry` | 10 / Sơ Học Phản Kích / 5 / 100 Linh Thạch<br>100 / Lấy Nhu Chế Cương / 20 / 800 Linh Thạch, 5 Tiên Ngọc<br>1.000 / Tứ Lạng Bạt Thiên Cân / 50 / 4000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Phản Kích Đại Sư»<br>5.000 / Phản Thiên Nghịch Mệnh / 120 / 10000 Linh Thạch, 60 Tiên Ngọc, Danh hiệu «Nghịch Mệnh Chi Nhân» |
| Chiến Đấu | `parry_combo` | Chiêu Liên Hoàn | `parry_combo` | 3 / Tam Liên Kích / 5 / 100 Linh Thạch<br>5 / Ngũ Liên Kích / 10 / 400 Linh Thạch<br>10 / Thập Liên Kích / 20 / 1500 Linh Thạch, 10 Tiên Ngọc<br>20 / Nhị Thập Liên Kích / 40 / 5000 Linh Thạch, 30 Tiên Ngọc |
| Chiến Đấu | `kill_flawless` | Toàn Thân Nhi Thoái | `kill_flawless` | 1 / Không Một Vết Xước / 5 / 100 Linh Thạch<br>25 / Bạch Y Bất Nhiễm / 10 / 1000 Linh Thạch, 5 Tiên Ngọc<br>200 / Thân Như Kim Cương / 20 / 5000 Linh Thạch, 25 Tiên Ngọc |
| Chiến Đấu | `kill_flawless_elite` | Tinh Anh Không Chạm | `kill_flawless` rank=elite | 5 / Né Tinh Anh / 5 / 500 Linh Thạch<br>50 / Tinh Anh Vô Dụng / 10 / 3000 Linh Thạch |
| Sưu Tầm | `weapon_get` | Binh Khí Trong Tay | `weapon_get` | 1 / Binh Khí Đầu Tiên / 5 / 100 Linh Thạch<br>10 / Thập Binh / 10 / 800 Linh Thạch, 5 Tiên Ngọc<br>50 / Bách Binh Tàng / 20 / 3000 Linh Thạch, 15 Tiên Ngọc |
| Sưu Tầm | `weapon_types` | Bách Binh Phổ | `weapon_types` | 3 / Tam Binh / 5 / 300 Linh Thạch<br>5 / Ngũ Binh / 10 / 1000 Linh Thạch, 5 Tiên Ngọc<br>8 / Bát Binh Tề Tựu / 20 / 3000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Bách Binh Chi Chủ» |
| Sưu Tầm | `weapon_q_ha` | Hạ Phẩm Nhập Thủ | `weapon_get` quality=ha | 1 / Hạ Phẩm Nhập Thủ / 5 / 100 Linh Thạch<br>5 / Ngũ Binh Hạ Phẩm / 10 / 400 Linh Thạch, 2 Tiên Ngọc |
| Sưu Tầm | `weapon_q_trung` | Trung Phẩm Binh Khí | `weapon_get` quality=trung | 1 / Trung Phẩm Binh Khí / 10 / 400 Linh Thạch<br>5 / Ngũ Binh Trung Phẩm / 20 / 1600 Linh Thạch, 8 Tiên Ngọc |
| Sưu Tầm | `weapon_q_thuong` | Thượng Phẩm Thần Binh | `weapon_get` quality=thuong | 1 / Thượng Phẩm Thần Binh / 15 / 900 Linh Thạch<br>5 / Ngũ Binh Thượng Phẩm / 30 / 3600 Linh Thạch, 18 Tiên Ngọc |
| Sưu Tầm | `weapon_q_cuc` | Cực Phẩm Bảo Khí | `weapon_get` quality=cuc | 1 / Cực Phẩm Bảo Khí / 20 / 1600 Linh Thạch<br>5 / Ngũ Binh Cực Phẩm / 40 / 6400 Linh Thạch, 32 Tiên Ngọc |
| Sưu Tầm | `weapon_q_tuyet` | Tuyệt Phẩm Tiên Khí | `weapon_get` quality=tuyet | 1 / Tuyệt Phẩm Tiên Khí / 25 / 2500 Linh Thạch<br>5 / Ngũ Binh Tuyệt Phẩm / 50 / 10000 Linh Thạch, 50 Tiên Ngọc |
| Sưu Tầm | `weapon_t_kiem` | Kiếm Tu Chi Đạo | `weapon_get` type=kiem | 1 / Kiếm Tu Chi Đạo / 5 / 150 Linh Thạch<br>5 / Kiếm Tu Chi Đạo Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_dao` | Đao Khách Giang Hồ | `weapon_get` type=dao | 1 / Đao Khách Giang Hồ / 5 / 150 Linh Thạch<br>5 / Đao Khách Giang Hồ Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_ho_lo` | Hồ Lô Tiên Ông | `weapon_get` type=ho_lo | 1 / Hồ Lô Tiên Ông / 5 / 150 Linh Thạch<br>5 / Hồ Lô Tiên Ông Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_thuong` | Thương Thần Xuất Thế | `weapon_get` type=thuong | 1 / Thương Thần Xuất Thế / 5 / 150 Linh Thạch<br>5 / Thương Thần Xuất Thế Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_chuy` | Chùy Bá Sơn Hà | `weapon_get` type=chuy | 1 / Chùy Bá Sơn Hà / 5 / 150 Linh Thạch<br>5 / Chùy Bá Sơn Hà Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_cung` | Thần Tiễn Truy Phong | `weapon_get` type=cung | 1 / Thần Tiễn Truy Phong / 5 / 150 Linh Thạch<br>5 / Thần Tiễn Truy Phong Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_truong` | Trượng Pháp Huyền Môn | `weapon_get` type=truong | 1 / Trượng Pháp Huyền Môn / 5 / 150 Linh Thạch<br>5 / Trượng Pháp Huyền Môn Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_t_phien` | Phiến Sĩ Phong Lưu | `weapon_get` type=phien | 1 / Phiến Sĩ Phong Lưu / 5 / 150 Linh Thạch<br>5 / Phiến Sĩ Phong Lưu Đại Thành / 10 / 800 Linh Thạch |
| Sưu Tầm | `weapon_forge` | Lò Rèn Hừng Hực | `weapon_forge` | 1 / Nhóm Lò / 5 / 300 Linh Thạch<br>10 / Thợ Rèn / 10 / 2000 Linh Thạch, 10 Tiên Ngọc<br>30 / Đại Sư Rèn Binh / 20 / 6000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Thần Tượng Rèn Binh» |
| Sưu Tầm | `beast_tame` | Ngự Thú Sư | `beast_tame` | 1 / Thu Phục Đầu Tiên / 10 / 500 Linh Thạch, 5 Tiên Ngọc<br>3 / Tam Thú Tùy Thân / 30 / 2000 Linh Thạch, 15 Tiên Ngọc<br>6 / Lục Thú Quy Tâm / 80 / 6000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Vạn Thú Chi Chủ» |
| Sưu Tầm | `beast_linh_ho` | Linh Hồ Quy Tâm | `beast_tame` beast=linh_ho | 1 / Linh Hồ Quy Tâm / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `beast_huyen_quy` | Huyền Quy Hộ Thể | `beast_tame` beast=huyen_quy | 1 / Huyền Quy Hộ Thể / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `beast_bach_hac` | Bạch Hạc Tùy Phong | `beast_tame` beast=bach_hac | 1 / Bạch Hạc Tùy Phong / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `beast_hoa_tuoc` | Hỏa Tước Phần Thiên | `beast_tame` beast=hoa_tuoc | 1 / Hỏa Tước Phần Thiên / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `beast_tieu_long` | Tiểu Long Tọa Kỵ | `beast_tame` beast=tieu_long | 1 / Tiểu Long Tọa Kỵ / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `beast_ky_lan_con` | Kỳ Lân Giáng Thế | `beast_tame` beast=ky_lan_con | 1 / Kỳ Lân Giáng Thế / 15 / 800 Linh Thạch, 5 Tiên Ngọc |
| Sưu Tầm | `lc_giai` | Linh Căn Phẩm Giai | `lc_giai` | 1 / Phàm Căn / 5 / 100 Linh Thạch<br>2 / Hoàng Căn / 5 / 200 Linh Thạch, Tẩy Linh Thảo x2 (cần Luyện Khí tầng 1)<br>3 / Huyền Căn / 10 / 400 Linh Thạch<br>4 / Địa Căn / 20 / 800 Linh Thạch, 5 Tiên Ngọc, Tẩy Linh Đan x1 (cần Luyện Khí tầng 1)<br>5 / Thiên Căn / 30 / 1500 Linh Thạch, 10 Tiên Ngọc, Tẩy Tủy Đan x1 (cần Luyện Khí tầng 4)<br>6 / Thánh Căn / 50 / 3000 Linh Thạch, 20 Tiên Ngọc<br>7 / Tiên Căn / 80 / 5000 Linh Thạch, 40 Tiên Ngọc<br>8 / Thần Căn / 120 / 8000 Linh Thạch, 60 Tiên Ngọc<br>9 / Hỗn Độn Căn / 200 / 12000 Linh Thạch, 100 Tiên Ngọc, Danh hiệu «Hỗn Độn Linh Thể» |
| Sưu Tầm | `lc_carry` | Thiên Phú Gia Thân | `lc_carry` | 4 / Địa Phẩm Gia Thân / 5 / 800 Linh Thạch, 5 Tiên Ngọc<br>5 / Thiên Phẩm Gia Thân / 10 / 2000 Linh Thạch, 15 Tiên Ngọc, Danh hiệu «Thiên Chi Kiêu Tử»<br>7 / Tiên Phẩm Gia Thân / 20 / 6000 Linh Thạch, 40 Tiên Ngọc |
| Sưu Tầm | `lc_book` | Linh Căn Đồ Giám | `lc_book` | 5 / Ngũ Căn Nhập Giám / 10 / 200 Linh Thạch<br>15 / Thập Ngũ Căn / 20 / 1000 Linh Thạch, 5 Tiên Ngọc<br>30 / Tam Thập Căn / 50 / 3000 Linh Thạch, 20 Tiên Ngọc<br>52 / Đồ Giám Viên Mãn / 150 / 10000 Linh Thạch, 80 Tiên Ngọc, Danh hiệu «Linh Căn Bác Sĩ» |
| Sưu Tầm | `lc_test` | Tẩy Linh Bất Khuất | `lc_test` | 5 / Ngũ Lần Tẩy Linh / 5 / 300 Linh Thạch, Tẩy Linh Thảo x2 (cần Luyện Khí tầng 1)<br>20 / Nhị Thập Tẩy Linh / 10 / 1200 Linh Thạch<br>50 / Nghịch Thiên Cải Mệnh / 20 / 4000 Linh Thạch |
| Sưu Tầm | `kill_kinds` | Yêu Quái Phổ | `kill_kinds` | 5 / Ngũ Loài / 5 / 300 Linh Thạch<br>12 / Thập Nhị Loài / 10 / 1500 Linh Thạch, 10 Tiên Ngọc<br>20 / Bách Yêu Đồ Phổ / 20 / 5000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Bách Yêu Thông» |
| Sưu Tầm | `pill_made` | Đan Hương Ngào Ngạt | `pill_made` | 10 / Đan Đồng / 5 / 200 Linh Thạch<br>100 / Đan Sư / 10 / 1500 Linh Thạch, 10 Tiên Ngọc<br>500 / Đan Đạo Tông Sư / 20 / 6000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Đan Đạo Tông Sư» |
| Sưu Tầm | `brew_thuong` | Thượng Phẩm Đan | `brew` quality=thuong | 1 / Mẻ Thượng Phẩm / 5 / 300 Linh Thạch<br>10 / Thập Mẻ Thượng Phẩm / 10 / 1500 Linh Thạch, 5 Tiên Ngọc<br>50 / Lửa Trong Lòng Bàn Tay / 20 / 5000 Linh Thạch, 20 Tiên Ngọc |
| Sưu Tầm | `fish` | Ngư Ông Đắc Lợi | `fish` | 10 / Cần Câu Mới / 5 / 100 Linh Thạch<br>100 / Lão Ngư / 10 / 800 Linh Thạch<br>500 / Ngư Ông Đắc Đạo / 20 / 3000 Linh Thạch |
| Khám Phá | `lands` | Hành Tẩu Thiên Địa Đồ | `lands` | 2 / Rời Thôn / 10 / 200 Linh Thạch<br>5 / Ngũ Phương / 30 / 1500 Linh Thạch, 10 Tiên Ngọc<br>9 / Cửu Châu Du Ký / 80 / 5000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Hành Giả Thiên Địa» |
| Khám Phá | `zones` | Vân Du Tứ Hải | `zones` | 3 / Bước Chân Đầu / 5 / 150 Linh Thạch<br>6 / Lữ Khách / 10 / 800 Linh Thạch<br>9 / Vân Du Bốn Biển / 20 / 3000 Linh Thạch |
| Khám Phá | `land_kiem_trung_son` | Đặt Chân Kiếm Trủng | `lands` land=kiem_trung_son | 1 / Đặt Chân Kiếm Trủng / 10 / 500 Linh Thạch |
| Khám Phá | `land_linh_xa_nguyen` | Đặt Chân Linh Xà Nguyên | `lands` land=linh_xa_nguyen | 1 / Đặt Chân Linh Xà Nguyên / 10 / 500 Linh Thạch |
| Khám Phá | `land_loi_kiep_dai` | Leo Lên Lôi Kiếp Đài | `lands` land=loi_kiep_dai | 1 / Leo Lên Lôi Kiếp Đài / 10 / 500 Linh Thạch |
| Khám Phá | `glide` | Đạp Kiếm Lướt Gió | `glide` | 10 / Ngự Kiếm Sơ Học / 5 / 100 Linh Thạch<br>100 / Kiếm Lướt Như Gió / 10 / 800 Linh Thạch, 5 Tiên Ngọc<br>1.000 / Ngự Kiếm Phi Tiên / 20 / 4000 Linh Thạch, 20 Tiên Ngọc, Danh hiệu «Ngự Kiếm Phi Tiên» |
| Khám Phá | `formation` | Bày Trận Giữ Mình | `formation` | 5 / Trận Đồ Sơ Khai / 5 / 100 Linh Thạch<br>50 / Trận Pháp Sư / 10 / 800 Linh Thạch<br>300 / Trận Đạo Tông Sư / 20 / 4000 Linh Thạch |
| Khám Phá | `ride` | Cưỡi Linh Thú | `ride` | 1 / Lên Lưng Linh Thú / 5 / 300 Linh Thạch<br>50 / Kỵ Sĩ Linh Thú / 10 / 2000 Linh Thạch |
| Khám Phá | `weapon_claim` | Nhặt Bảo Ven Đường | `weapon_claim` | 1 / Nhặt Bảo / 5 / 200 Linh Thạch<br>5 / Mắt Tinh / 10 / 1000 Linh Thạch, 5 Tiên Ngọc<br>15 / Thám Bảo / 20 / 3000 Linh Thạch, 15 Tiên Ngọc<br>27 / Thiên Địa Thu Tàng / 40 / 8000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Thiên Hạ Thám Bảo» |
| Khám Phá | `realm_clear` | Bí Cảnh Đoạt Bảo | `realm_clear` | 1 / Vào Bí Cảnh / 5 / 300 Linh Thạch<br>10 / Thập Lần Đoạt Bảo / 10 / 2000 Linh Thạch, 10 Tiên Ngọc<br>50 / Bí Cảnh Chi Vương / 20 / 6000 Linh Thạch, 30 Tiên Ngọc |
| Khám Phá | `td_win` | Thủ Thành Bất Phá | `td_win` | 1 / Giữ Thành / 5 / 200 Linh Thạch<br>10 / Thập Thắng / 10 / 1500 Linh Thạch, 5 Tiên Ngọc<br>50 / Kim Thành Thang Trì / 20 / 5000 Linh Thạch, 20 Tiên Ngọc |
| Tài Phú | `stones_earned` | Linh Thạch Như Sơn | `stones_earned` | 1.000 / Túi Nặng / 5 / 100 Linh Thạch<br>10.000 / Rương Đầy / 15 / 500 Linh Thạch, 5 Tiên Ngọc<br>100.000 / Kho Như Núi / 40 / 2000 Linh Thạch, 20 Tiên Ngọc<br>1.000.000 / Phú Khả Địch Quốc / 100 / 10000 Linh Thạch, 60 Tiên Ngọc, Danh hiệu «Phú Giáp Nhất Phương» |
| Tài Phú | `stones_spent` | Vung Tay Hào Phóng | `stones_spent` | 1.000 / Biết Tiêu / 5 / 100 Linh Thạch<br>10.000 / Hào Phóng / 10 / 600 Linh Thạch, 5 Tiên Ngọc<br>100.000 / Tán Tài Như Thổ / 20 / 3000 Linh Thạch, 20 Tiên Ngọc |
| Tài Phú | `jade_earned` | Tiên Ngọc Lấp Lánh | `jade_earned` | 10 / Viên Ngọc Đầu / 5 / 300 Linh Thạch<br>100 / Trăm Viên Ngọc / 10 / 1500 Linh Thạch<br>500 / Ngọc Khố / 20 / 5000 Linh Thạch |
| Tài Phú | `furnace` | Lò Đan Thăng Cấp | `furnace` | 2 / Lò Mới / 5 / 500 Linh Thạch<br>3 / Lò Thượng Hạng / 10 / 2000 Linh Thạch, 10 Tiên Ngọc |
| Tài Phú | `weapon_forge_cuc` | Đổ Vốn Vào Lò Rèn | `weapon_forge` quality=cuc | 1 / Cực Phẩm Xuất Lò / 30 / 2000 Linh Thạch, 10 Tiên Ngọc<br>5 / Ngũ Cực Phẩm / 80 / 8000 Linh Thạch, 40 Tiên Ngọc |
| Bí Ẩn (ẩn) | `secret_clutch` | Ngàn Cân Treo Sợi Tóc | `answer_clutch` | 1 / Treo Sợi Tóc / 15 / 300 Linh Thạch<br>20 / Sống Trên Lưỡi Dao / 40 / 2000 Linh Thạch, 10 Tiên Ngọc |
| Bí Ẩn (ẩn) | `secret_night` | Đêm Khuya Đọc Kinh | `answer_night` | 10 / Đêm Khuya Đọc Kinh / 20 / 800 Linh Thạch, 5 Tiên Ngọc |
| Bí Ẩn (ẩn) | `secret_comeback` | Thất Bại Là Mẹ Thành Công | `answer_comeback` | 1 / Đứng Dậy / 15 / 300 Linh Thạch<br>10 / Ngã Bảy Lần Đứng Dậy Tám / 30 / 1500 Linh Thạch |
| Bí Ẩn (ẩn) | `secret_death` | Ngã Xuống Rồi Đứng Lên | `death` | 1 / Lần Ngã Đầu / 5 / 100 Linh Thạch, Hồi Huyết Đan x5<br>20 / Bất Khuất / 20 / 1000 Linh Thạch |
| Bí Ẩn (ẩn) | `secret_flawless_boss` | Bất Nhiễm Trần Ai | `kill_flawless` rank=boss | 1 / Bất Nhiễm Trần Ai / 80 / 5000 Linh Thạch, 30 Tiên Ngọc, Danh hiệu «Bất Nhiễm Trần Ai» |
| Bí Ẩn (ẩn) | `secret_combo` | Nghịch Thiên Liên Kích | `parry_combo` | 30 / Nghịch Thiên Liên Kích / 100 / 6000 Linh Thạch, 40 Tiên Ngọc, Danh hiệu «Liên Kích Vô Song» |
| Bí Ẩn (ẩn) | `secret_hon_don` | Hỗn Độn Chi Thể | `lc_carry` | 9 / Hỗn Độn Chi Thể / 250 / 20000 Linh Thạch, 150 Tiên Ngọc, Danh hiệu «Hỗn Độn Chi Thể» (cần Hóa Thần sơ kỳ) |
| Bí Ẩn (ẩn) | `secret_tuyet` | Tuyệt Phẩm Xuất Thế | `weapon_forge` quality=tuyet | 1 / Tuyệt Phẩm Xuất Thế / 150 / 10000 Linh Thạch, 80 Tiên Ngọc, Danh hiệu «Thần Binh Chủ Nhân» |
| Bí Ẩn (ẩn) | `secret_phe_dan` | Lò Đan Bốc Khói | `brew` quality=phe | 5 / Lò Đan Bốc Khói / 10 / 500 Linh Thạch, Hồi Huyết Đan x3 |
| Bí Ẩn (ẩn) | `secret_streak` | Vô Thượng Đạo Tâm | `answer_streak` | 200 / Vô Thượng Đạo Tâm / 200 / 15000 Linh Thạch, 100 Tiên Ngọc, Danh hiệu «Vô Thượng Đạo Tâm» |
| Bí Ẩn (ẩn) | `secret_ky_lan` | Điềm Lành Giáng Thế | `beast_tame` | 6 / Điềm Lành Giáng Thế / 60 / 3000 Linh Thạch, 30 Tiên Ngọc |

## Thêm một thành tựu

1. Thêm một mục vào `achievements.json`: `id`, `category`, `name_vi`, `desc_vi`, `counter` (một khóa của
   `achievements.COUNTERS`), `where` tuỳ chọn (một trường lọc), `icon` (`[bộ, id]` có trong
   `client/assets/v2/icons`), `tiers` (mốc tăng dần, `points`, `reward`, `name_vi`, `req` tuỳ chọn); thành tựu ẩn
   thêm `hidden`, `reveal_vi`, `hint_vi`.
2. Cần đếm điều mới thì thêm bộ đếm vào `COUNTERS`, nếu cần một sự kiện mới vào `RAW` và `_expand_static`, rồi một
   dòng gọi ở nơi việc xảy ra.
3. `python tools/check_all.py`: `validate()` báo id/tên trùng, mốc không tăng, vật phẩm vượt tu vi, icon thiếu,
   sự kiện không có nơi gửi, giá trị lọc lạ (đọc từ catalog: quái, binh khí, linh thú... mới tự được nhận).
