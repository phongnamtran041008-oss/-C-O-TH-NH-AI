# Đạo Thụ trong game — cây giáo trình thay cho lộ trình từng môn

> Viết ngày 2026-11-19, khi cây được nối vào luật chơi theo yêu cầu của tác giả ("hãy thay thế giúp tôi để
> cho khoá học chỉn chu"). Nội dung cây (nút, tầng, cần gì trước, ôn gì) ở `docs/GIAO_TRINH_CAY.md`; file
> này nói **luật chơi đọc cây thế nào**, và những chỗ tôi phải tự quyết để cây chạy được.

## Trước và sau

| | Trước | Sau |
|---|---|---|
| Thứ người chơi mở và vượt | Tầng n của một bí cảnh | Một **nút** của Đạo Thụ |
| Mở khi | Qua Thiên kiếp nhỏ của tầng n - 1 cùng bí cảnh | Mọi nút nó **cần trước** đã xong, kể cả nút của nhánh khác |
| Học môn nào trước | Hết môn này mới sang môn kia cũng được | Bốn nhánh toán đi song song; muốn lên tầng tu vi phải xong nút của cả bốn |
| Câu ôn lấy từ | Các tầng dưới của cùng bí cảnh | Các nút mà nút ấy **ôn lại** (có thể ở nhánh khác) |
| Kỹ năng hàn lâm bị loại | Vẫn nằm ở tầng ẩn | Không bao giờ được hỏi, ở bất cứ chế độ nào |
| Phần tuỳ chọn | Tầng ẩn 10 | **Bàng môn**: mở theo cùng luật nhưng không chặn gì |
| "Tầng" còn nghĩa gì | Đơn vị tiến độ | Chỉ còn là **địa chỉ của câu hỏi**: bậc khó, bài đọc Tàng Thư Các |

## Cách nối

Gần như mỗi nút toán là một phần các vi kỹ năng của **một** tầng (hai nút trải trên hai tầng). Nên một nút
được chia thành các **phần**: phần = (nút, bí cảnh, tầng, các vi kỹ năng của nút nằm ở tầng ấy). Một buổi
luyện hay một Thiên kiếp nhỏ diễn ra trên một phần. Nhờ vậy mọi luật học cũ — bậc thích ứng, cổng thuần
thục, Thiên kiếp nhỏ, chống lặp, tâm ma, bậc thang cho câu bậc 5 — giữ nguyên, chỉ thu hẹp vào các vi kỹ
năng của phần.

Mười hai luật (bản đầy đủ là hợp đồng dùng lúc làm, tóm lại ở đây):

1. **Phần.** Nhóm vi kỹ năng của nút theo tầng.
2. **Phần được vượt** khi qua Thiên kiếp nhỏ của chính phần ấy — hoặc theo luật cũ, tính cho cả tầng: một
   Thiên kiếp nhỏ đã qua từ trước khi có cây, hay bài kiểm tra đầu vào cho bỏ qua tầng ấy. Bản lưu cũ và
   bài kiểm tra đầu vào vì thế vẫn dùng được.
3. **Nút xong** khi mọi phần có câu hỏi của nó đã vượt; nút lập trình xong khi mọi bài tập của nó được giải
   đủ điểm. Nút **chưa có nội dung** ("đang biên soạn") được coi là xong — xem mục "Tôi tự quyết" bên dưới.
4. **Nút mở** khi chưa xong và mọi nút nó cần trước đã xong. Không còn luật "phải qua tầng dưới".
5. **Tầng tu vi trên cây**: Luyện Khí tầng k = mọi nút chính đạo có tầng <= k đã xong.
6. **Được hỏi gì**: trong buổi luyện của một phần chỉ hỏi vi kỹ năng của phần ấy, cộng câu ôn. Vi kỹ năng bị
   loại không bao giờ được hỏi. Vi kỹ năng bàng môn chỉ được hỏi trong buổi luyện của chính nút ấy, và trở
   lại sau khi người chơi đã xong nút.
7. **Ôn**: tỉ lệ và lịch ôn giữ nguyên; ứng viên là vi kỹ năng của các nút được ghi ở "ôn lại". Không có thì
   lấy từ các nút tổ tiên đã xong; không có nữa thì không ôn (như tầng 1 trước đây).
8. **Cổng và Thiên kiếp nhỏ** tính trên vi kỹ năng của phần. Bậc khó vẫn theo tầng.
9. **Ngoài buổi luyện** (bí cảnh, hầm ngục, cơ duyên, thủ thành, chiêu thức): "tầng của người chơi ở môn
   S" thành **tiền tuyến** của S — phần chính đạo đang mở đầu tiên theo thứ tự cây; không có thì phần đã
   vượt gần nhất; chưa có gì thì phần đầu tiên có câu hỏi.
10. **Bài tập lập trình** mở khi vi kỹ năng của nó thuộc một nút đang mở hoặc đã xong.
11. **Lối vào cũ** (bắt đầu theo bí cảnh + tầng) vẫn còn nhưng tuân theo cây; tầng chưa mở trả về lỗi
    `node_locked` kèm tên các nút phải xong trước.
12. **Chỗ nào từng đọc "tầng người chơi đã tới"** nay dùng một trong ba: tiền tuyến (cần câu hỏi), các tầng
    đã chạm tới (cần biết tầng nào được vào), hoặc tầng tu vi đang tu (ngưỡng mở khoá: chiêu "mở ở tầng 7"
    nay mở ở Luyện Khí tầng 7).

Mã nguồn: `server/app/systems/math_tree_progress.py` (nơi duy nhất trả lời "người chơi đang ở đâu trên
cây"), `server/app/systems/math_practice.py` (buổi luyện trên một phần), các đường `GET /math/tree`,
`POST /math/node/start`, `POST /math/node/trial`. Kiểm: `server/tests/test_math_tree_progress.py`, và phép
kiểm thứ 18 trong `tools/check_all.py` (mỗi phần đúng tầng, và một bản lưu trống đi tới được mọi nút chính
đạo).

## Trên màn hình

Màn Bí Cảnh Toán (`client/scenes/math_practice.py`, `client/scenes/math_tree.py`) nay là Đạo Thụ:

- Dòng đầu cho biết đang ở đâu, ví dụ "Luyện Khí tầng 2/9", kèm tiến độ trong tầng đang làm: "đã xong 1/4
  nút của tầng 3" (máy chủ tính trong `stage.progress` của `GET /math/tree`: các nút chính đạo của tầng đó
  đã xong trên các nút có nội dung; nút "Đang biên soạn" không tính vào cả hai số). Trên thẻ nhánh có nút
  ở bên phải thì chỗ hẹp, dòng này tự rút gọn hoặc ẩn.
- Thẻ **Nên học** liệt kê các nút chính đạo đang mở; sau đó mỗi nhánh một thẻ (Đại Số, Giải Tích, Xác
  Suất, Thuật Toán, Lập Trình, Thực Chiến), nút xếp theo tầng, bàng môn ở cuối.
- Mỗi dòng là một phần của nút: tên, bậc khó, tiến độ cổng thuần thục hoặc nút Thiên kiếp, nút Đọc (bài ở
  Tàng Thư Các), nút Luyện. Nút còn khoá ghi rõ cần xong nút nào; nút chưa có nội dung ghi "Đang biên soạn".
- Bấm vào tên nút mở **thẻ nút**: vì sao học, cần xong gì trước, ôn lại gì, học những gì, và **Nên học từ**
  — nguồn tốt nhất cho nút ấy lấy từ `server/data/math/sources/` (tên, tác giả, xem phần nào, ngôn ngữ,
  đường dẫn). Nút "Mở trang" mở đường dẫn bằng trình duyệt của máy; game không tự mở trang nào.
- Thẻ của nút lập trình có nút **Làm bài**: mở danh sách bài tập của riêng nút ấy trong màn bài tập lập
  trình (`client/scenes/math_code.py`), không cần qua nút "Bài tập" ở thẻ Đại Số.
- Câu ôn trên thẻ câu hỏi ghi tên nút đang được ôn ("Ôn lại: Tập hợp và ánh xạ"), kể cả khi nút ấy thuộc môn
  khác (`review_node_vi` trong thông tin câu hỏi). Chỉ buổi luyện cũ không có nút mới còn ghi "Ôn xoắn ốc: tầng N".
- Qua Thiên kiếp nhỏ của một nút thì màn kết quả nói nút nào vừa mở, kể cả nút của nhánh khác.

## Vùng đất Luyện Khí (Thiên Địa Đồ, nối ngày 2026-11-20)

Phần `lands` của `server/data/math/world_plan.json` đã nối vào game (`"wired_sections": ["combat", "lands", "weapons"]`).
Tám vùng đất của Luyện Khí có thật; Vân Hải Thiên Đảo (Trúc Cơ, đảo trên mây) vẫn `chua_co`.

| Vùng đất | Nhánh | Bản đồ (zone) | Cổng từ Trúc Lâm Thôn | Mở khi |
|---|---|---|---|---|
| Kiếm Trủng Sơn | Đại Số | `loan_so_coc` (bản đồ cũ) | Bắc | Ngay từ đầu |
| Lưu Vân Cốc | Giải Tích | `luu_van_coc` (mới) | Đông Bắc | Ngay từ đầu |
| Vạn Tượng Trạch | Xác Suất | `ho_nghien_muc` (bản đồ cũ) | Tây | Ngay từ đầu |
| Mê Đồ Lâm | Thuật Toán | `rung_muc_loang` (bản đồ cũ) | Đông | Ngay từ đầu |
| Thiên Công Phường | Lập Trình | `thien_cong_phuong` (mới) | Tây, phía trên | Tầng 1 và xong Python nhập môn |
| Linh Xạ Nguyên | Thực Chiến | `linh_xa_nguyen` (mới) | Đông, phía dưới | Tầng 2, xong Cấu trúc dữ liệu và Vectơ, ma trận |
| Lôi Kiếp Đài | (cả bốn nhánh toán) | `loi_kiep_dai` (mới) | Tây Bắc | Tầng 9 và xong dự án Luyện Khí |

- **Cửa vào**: máy chủ kiểm (`server/app/realtime/lands.py`, gọi từ `world.join`), cả khi đi qua cổng lẫn khi
  vào lại sau mất mạng. "Tu vi" ở đây là tầng trên Đạo Thụ và các nút đã xong; cảnh giới nhân vật không đổi
  gì. Chưa đủ thì không đi được và thấy một dòng tiếng Việt nói còn thiếu gì, ví dụ "Chưa vào được Linh Xạ
  Nguyên: cần tu vi Luyện Khí tầng 2 (con đang ở tầng 1) và học xong Vectơ và ma trận."
- **Quái của vùng nào hỏi toán của nhánh ấy.** Mỗi quái của vùng (`server/data/math/monsters.json`, khoá
  `land`, `branch`, `nodes`) đứng cho vài nút của Đạo Thụ; khi nó đánh trúng, câu hỏi lấy từ phần của các
  nút ấy mà người chơi đã mở hoặc đã xong, ở đúng bậc của người chơi. Chưa mở nút nào của nó thì hỏi chỗ
  người chơi đang học trong nhánh của vùng. Quái lỗi sai cũ ở Kiếm Trủng Sơn vẫn hỏi đúng vi kỹ năng của nó;
  Mực Con, Lân Hỏa Yêu, Mặc Hồ ở Mê Đồ Lâm nay hỏi Thuật Toán.
- **Thiên Kiếp Lôi Long** ở Lôi Kiếp Đài là thủ lĩnh: khiên chỉ vỡ khi Phản Đòn, khiên mọc lại ở 66% và 33%
  máu; mỗi đòn trúng hỏi lần lượt Đại Số, Giải Tích, Xác Suất, Thuật Toán, mỗi lần là câu khó nhất người chơi
  được hỏi ở nhánh đó. Thắng thì được ghi vào Yêu Quái Phổ (số lần hạ) và nhận thưởng theo luật rơi đồ (Trúc
  Cơ Đan chỉ rơi khi tu vi nhân vật đủ Luyện Khí tầng 7). Thắng không đổi cảnh giới nhân vật.
- **Chỗ đặt binh khí**: mỗi mục `weapons_placed` của vùng đã dựng có `"pos": [x, y]` (một ô đi được trên bản
  đồ, đúng chỗ `spot_vi` tả). Hai chỗ cần Đạp Kiếm Lướt (đỉnh núi bên kia vực ở Kiếm Trủng Sơn, mỏm đá trong
  mây trên thác ở Lưu Vân Cốc) đứng được nhưng đi bộ không tới: chỉ lướt trên kiếm mới tới (xem phần "Linh thú
  và thần thông Luyện Khí" ở dưới). Hệ thống binh khí (đợt khác) cho `GET /weapons`
  và `POST /weapons/claim`; game vẽ binh khí từ danh sách ấy và bấm E để nhặt; máy chủ chưa có hai đường ấy thì
  game không vẽ gì và không báo lỗi.
- Bộ kiểm (`server/app/learning/math_tree.py`, chạy trong `tools/check_all.py`) đòi: mỗi vùng đã dựng có đúng
  một zone, bản đồ có ở máy chủ và máy khách, mọi quái được nêu có sinh ra ở đó, quái của vùng chỉ đứng cho nút
  chính đạo của Luyện Khí thuộc nhánh của vùng (vùng Lập Trình, Thực Chiến: nút toán mà nhánh ấy ôn lại), và mọi
  `pos` là ô đi được.

## Binh khí trên các vùng đất

Phần binh khí của `world_plan.json` đã nối (`"wired_sections": ["combat", "lands", "weapons"]`, 2026-11-20); mở khoá
`nhat_vu_khi` (Luyện Khí tầng 1) và `nang_pham` (Luyện Khí tầng 4) là `"co"`. Luật ở
`server/app/systems/weapons.py`, đường `GET /weapons`, `POST /weapons/claim`, `/weapons/equip`,
`/weapons/unequip`, `GET/POST /weapons/upgrade` (`docs/API.md`).

- **Tu vi của yêu cầu là chỗ đứng trên Đạo Thụ.** Một chỗ đặt mở khi tầng trên cây tới tầng nó ghi, mọi nút nó
  ghi đã xong (nút "Đang biên soạn" tính là xong, như luật 3), vùng đất của nó đã mở (`opens` của vùng) và năng
  lực nó cần (`needs`, ví dụ Đạp Kiếm Lướt) đã có trong game. Chưa đủ thì danh sách nói thiếu gì, gọi nút bằng tên.
  Hai chỗ cần Đạp Kiếm Lướt mở từ khi thần thông ấy có (Luyện Khí tầng 6); ba chỗ cần Ngự Kiếm Phi Hành còn
  khoá cho tới khi Trúc Cơ được làm.
- **Một mô hình trang bị.** Nhặt rồi binh khí là một món ô Vũ khí như Kiếm Gỗ Đào; phẩm lưu thành độ hiếm
  (hạ = Phàm, trung = Linh, thượng = Huyền) nên túi đồ, sạp, Bảo Vật Phổ và lò cường hóa dùng được ngay; Công
  lấy từ kế hoạch: `atk` của bậc × `power` của phẩm. Đồ cũ (bút, kiếm gỗ, quạt, gậy) vẫn còn và vẫn đánh theo
  `weapon_kinds` của `balance/combat.json`.
- **Khi đánh**: loại binh khí quyết định tầm, nhịp đòn, hệ số và động tác (chém, thi pháp, bắn). Phản Đòn với câu
  thuộc nhánh của binh khí mạnh thêm 50%; Chùy (Lập Trình) và Cung (Thực Chiến) không có môn toán riêng nên mạnh
  thêm 15% với mọi câu.
- **Rèn nâng phẩm** ở Lò Toán, tab Nâng phẩm: hạ phẩm thành trung phẩm cho 4 Lõi Ma Trận, 3 Mực Tinh và 40 Linh
  Thạch (`crafting.json`, mục `upgrades`); hai thứ ấy quái thật rớt và đã rớt được từ trước Luyện Khí tầng 4
  (`tools/check_all.py` kiểm).
- **Trên màn hình**: túi đồ có tab Binh Khí (của mình: biểu tượng, loại, bậc, phẩm, Công, tác dụng, Mặc/Tháo; các
  chỗ đặt: nhặt được, đã nhặt, hay chưa mở và vì sao; bên phải là nhân vật cầm binh khí đang dùng). Mỗi bậc của
  mỗi loại có lớp vẽ trong tay riêng (`client/assets/v2/weapons/<loại>_<bậc>`) và biểu tượng cùng tên.
- **Điểm nhặt trên bản đồ**: vùng đất vẽ binh khí tại `pos` của từng chỗ đặt và bấm E để nhặt (xem phần
  "Vùng đất Luyện Khí" ở trên).

## Linh thú và thần thông Luyện Khí (nối ngày 2026-11-20)

Phần `beasts` (cùng luật thu phục `beast_taming`) và các thần thông Luyện Khí trong `unlocks` đã nối:
`"wired_sections": ["combat", "lands", "weapons", "beasts", "abilities"]`. Mọi mở khoá của Luyện Khí là `"co"`;
mọi mở khoá của cảnh giới sau (Ngự Kiếm Phi Hành trở đi) vẫn `"chua_co"` vì chưa có vùng đất nào ở đó. Kỳ Lân
Con (Vân Hải Thiên Đảo, Trúc Cơ) chờ vùng đất của nó. "Tu vi" vẫn là tầng trên Đạo Thụ.

| Linh thú | Vùng đất, chỗ | Hiện từ | Phản Đòn để thu | Quà khi đeo |
|---|---|---|---|---|
| Linh Hồ | Mê Đồ Lâm, ngõ cụt sâu trong rừng | Tầng 3 | 3 | Đánh hơi binh khí còn nằm trong 18 ô quanh mình (chấm trên bản đồ nhỏ, dòng chỉ hướng) |
| Huyền Quy | Vạn Tượng Trạch, đảo sương | Tầng 4 | 3 | Đòn trúng khi trả lời sai nhẹ đi 30% |
| Bạch Hạc | Lưu Vân Cốc, mỏm đá cao | Tầng 5 | 4 | Né Đòn hồi nhanh hơn 35% |
| Hỏa Tước | Kiếm Trủng Sơn, tổ sau vực | Tầng 6 và Đạp Kiếm Lướt | 4 | Đòn phản mạnh thêm 25%, có lửa |
| Tiểu Long | Thiên Công Phường, lò lớn | Tầng 8 | 5 | Cưỡi được, đi nhanh gấp 1,5 |

- **Thu phục theo luật đánh mới** (`server/app/realtime/beasts.py`): linh thú là một con quái của vùng chỉ hiện
  với người đủ tầng (và có thần thông nó cần, chưa thu nó); người khác không thấy, không bị nó đánh. Nó đánh có
  báo trước như quái; đòn trúng thì hỏi câu thuộc các nút mà quái của vùng ấy đứng cho. Nó không bao giờ chết.
  Mỗi Phản Đòn được đếm cho người trả lời; số đếm hiện trên đầu nó và ở giữa phía trên màn hình. Đủ
  `parries_to_tame` thì nó chịu phục người ấy, thôi đánh người ấy và chờ 90 giây. Thôi đánh giữa chừng (nó về
  chỗ) thì đếm lại từ đầu.
- **Phong Ấn Phù**: đứng gần linh thú đã chịu phục, bấm E (`POST /beasts/seal`, cần thần thông Thu phục linh
  thú, tầng 3). Mất một lá bùa. Bùa bán ở Sạp Tạp Hóa (60 Linh Thạch, 3 lá mỗi ngày); không quái nào rơi.
- **Một mô hình bạn đồng hành**: linh thú đã thu là một Linh Thú như mười hai con giáp (cùng bảng `pets`, cùng
  bảng Linh Thú, đeo một con một lúc, đi theo chủ), chỉ khác là không bao giờ ra ở Thiên Cơ Các và kỹ năng của
  nó là quà của kế hoạch (`gift`). Linh Thú Phổ vẫn là mười hai con giáp.
- **Bày pháp trận** (tầng 5, phím T): đặt một trận bán kính 56 px dưới chân trong 20 giây, hồi 30 giây; quái
  đứng trong trận lúc ra đòn thì vùng đánh đầy chậm gấp 1,75 (`server/app/realtime/abilities.py`).
- **Đạp Kiếm Lướt** (tầng 6, phím G): lướt tối đa 80 px theo hướng đang đi, qua ô nước và ô vực (mực) kể cả
  chỗ không đi bộ được; không qua tường đá, cây, nhà. Máy chủ kiểm lại từ chỗ người chơi thật sự đứng: chưa mở,
  đáp xuống ô không đứng được, hay vướng vật cản thì từ chối và không ai di chuyển. Hình học dùng chung ở
  `server/app/realtime/glide.py` (máy khách có bản chép y hệt).
- **Cưỡi linh thú** (tầng 8, phím R): đeo Tiểu Long rồi bấm R; máy chủ cho đi nhanh gấp `speed_mult` của quà,
  người chơi chỉ gửi phím bấm nên không xin được nhanh hơn. Người cưỡi ngồi xếp bằng trên lưng linh thú (lớn
  gấp đôi khi được cưỡi).
- Bộ kiểm (`math_tree.py`) đòi thêm: mỗi linh thú đã dựng ở một vùng đã dựng, `pos` là ô đi được, đi bộ tới
  được (hoặc nếu cần Đạp Kiếm Lướt thì đi bộ không tới mà một lần lướt tới được), số đánh và quà hợp lệ; số của
  pháp trận, lướt, cưỡi đủ và hợp lý; hai chỗ binh khí cần Đạp Kiếm Lướt thật sự lướt tới được.


## Tôi tự quyết — bạn đổi được

| Việc | Tôi chọn | Vì sao | Muốn khác thì |
|---|---|---|---|
| Nút chưa có nội dung | Coi như xong, hiện "Đang biên soạn", không chặn gì | Một nút trống mà chặn thì mọi nút đứng sau nó không ai tới được (lúc Python nhập môn còn trống, nếu chặn thì không ai rời được tầng 1). Hiện 10 trên 19 nút lập trình/thực chiến/dự án của Luyện Khí chưa có nội dung: NumPy, tám nút thực chiến và nút dự án; chín nút lập trình còn lại đã có 3-5 bài | Viết nội dung cho nút: nó tự bắt đầu tính |
| Bài lập trình gắn vào vi kỹ năng nào | Mỗi bài gắn với vi kỹ năng mà toán của nó luyện, trong một nút toán mà nút lập trình đòi trước (hoặc mở cùng lúc với nút lập trình). Một nút lập trình chỉ dùng bài của **một** bí cảnh | Luật 10 (bài mở khi nút của vi kỹ năng mở hoặc xong) cho người chơi làm được mọi bài của một nút lập trình đang mở, không bao giờ bị khoá ngoài ý muốn. Nút "Làm bài" chỉ mở danh sách bài của một bí cảnh, nên không trộn bí cảnh trong một nút. Python nhập môn không có toán riêng nên mượn các vi kỹ năng đầu tiên của Đại Số: tập hợp, ánh xạ, tích Descartes | Nới luật 10: bài mở khi nút lập trình đang liệt kê nó mở (`problem_open`), rồi gắn bài tự do hơn; cho nút "Làm bài" đọc nhiều bí cảnh |
| Mô phỏng xác suất cho ra đúng cùng một kết quả | Bốn bài mô phỏng tự viết bộ sinh số ngẫu nhiên ngay trong đề (đồng dư tuyến tính, chia dư 2^31) thay vì dùng `random` | Kết quả của `random` đổi theo bản Python; đề tự viết thì mọi máy cho đúng một đáp án và máy chấm so chính xác được | Đổi sang dung sai thống kê: cần một ô sai số riêng cho từng bài trong dữ liệu bài tập |
| Tầng tu vi trên cây và cảnh giới nhân vật | **Không nối.** Tầng trên cây chỉ hiển thị; Tu Vi và cảnh giới nhân vật vẫn như cũ | Cách quy đổi là việc bạn chưa quyết | Nói cách quy đổi, tôi nối |
| Cảnh giới chưa viết | Vị trí dừng ở Luyện Khí tầng 9 | Mọi nút sau Luyện Khí đều chưa có nội dung; nếu không chặn thì xong Luyện Khí sẽ hiện thẳng "Đại Thừa tầng 3" | — |
| Thiên kiếp nhỏ của phần nhỏ | Số câu được sai = tối đa 1, nhưng không quá một phần tư số câu: phần 1-3 vi kỹ năng phải đúng hết | Trước đây mỗi tầng 5-6 câu, sai 1 vẫn qua. Phần của nút có khi chỉ 1-2 vi kỹ năng: giữ luật cũ thì sai một nửa, thậm chí sai hết, vẫn qua | Đổi trong `math_mastery.trial_allowed` |
| Tháp Số Phức (thủ thành) | Mở khi người chơi xong nút bàng môn Số phức | Tầng 2 của Đại Số chỉ còn nút bàng môn, nên theo luật 6 và 12 tháp ấy sẽ không bao giờ mở | — |
| Bài kiểm tra đầu vào | Giữ nguyên: vẫn hỏi theo cả tầng, kể cả vi kỹ năng bàng môn | Đổi cách hỏi là viết lại bài kiểm tra | Làm thành một việc riêng |
| Quái lỗi sai | Vẫn hỏi đúng vi kỹ năng của nó, kể cả khi nút ấy chưa mở | Nó không đọc vị trí của người chơi; vi kỹ năng bị loại thì vẫn không bao giờ hỏi | — |
| Ba vùng đất dùng lại bản đồ cũ | Giữ mã zone cũ (`loan_so_coc`, `ho_nghien_muc`, `rung_muc_loang`), chỉ đổi tên hiện ra; zones.json ghi `land` | Đổi mã thì mất chỗ đứng đã lưu của người chơi và gãy câu cá, nhiệm vụ, bí cảnh đang trỏ tới mã cũ | Đổi mã cùng lúc với một bước chuyển dữ liệu |
| Quái cũ ở vùng đất mới | Quái lỗi sai ở Kiếm Trủng Sơn và Mực Con, Lân Hỏa Yêu, Mặc Hồ ở Mê Đồ Lâm ở lại (nhiệm vụ đang đòi chúng); Mực Con, Lân Hỏa Yêu ở Vạn Tượng Trạch nhường chỗ cho Đầu Tử Oa, Hồ Lô Tinh | Giữ nhiệm vụ và các bài kiểm cũ chạy được; mọi quái trong vùng đều hỏi toán của nhánh vùng | Bỏ hẳn quái cũ: sửa nhiệm vụ rồi xoá vùng sinh của chúng trong `tools/gen_maps.py` |
| Quái vùng Lập Trình, Thực Chiến hỏi gì | Phần toán mà các nút của nhánh ấy ôn lại (`reinforces`) | Nút của hai nhánh này là bài code, không có câu hỏi trắc nghiệm | Cho quái ra một đoạn code ngắn để đọc, khi có loại câu ấy |
| Mỗi nhánh một tinh anh | Phong Lang, Hồ Lô Tinh, Mộc Yêu, Ma Trận Thú, Cơ Quan Nhân Đầu Đàn (mới), Tâm Ma Chấp Niệm (mới) là tinh anh, có khiên chỉ vỡ khi Phản Đòn | Mỗi vùng có chỗ "do ... canh" trong `spot_vi` của binh khí | Đổi `rank` trong monsters.json |
| Trần rơi đồ | Bốn vùng mới trần Luyện Khí tầng 9; Mê Đồ Lâm giữ trần tầng 5 của Rừng Mực Loang | Không đổi cân bằng đã có | Đổi `source_caps` trong `server/data/loot_tiers.json` |
| Phẩm của binh khí | Lưu thành độ hiếm có sẵn (hạ = Phàm, trung = Linh, thượng = Huyền), Công theo `power` của kế hoạch | Một mô hình trang bị: túi, sạp, cường hóa, Bảo Vật Phổ dùng được ngay, không cần bảng mới | Đổi `rarity` của từng phẩm trong `qualities` |
| Binh khí và nhánh | Phản Đòn câu đúng nhánh của binh khí mạnh thêm 50%; Chùy, Cung (nhánh không có môn toán riêng) thêm 15% mọi câu | Một luật dễ thấy, cho người chơi lý do cầm binh khí hợp môn đang học | Đổi hai số `weapons.*_parry_bonus` |
| Nâng phẩm | 4 Lõi Ma Trận + 3 Mực Tinh + 40 Linh Thạch, chỉ hạ → trung | Lõi Ma Trận rớt từ Luyện Khí tầng 4, đúng lúc nâng phẩm mở; trung → thượng để dành cho chỗ đặt thượng phẩm | Sửa `crafting.json`, mục `upgrades` |
| Linh thú và Linh Thú con giáp | Một mô hình: linh thú thu phục thành một dòng của bảng `pets`, đeo một con một lúc như con giáp; không ra ở Thiên Cơ Các | Không có hai loại bạn đồng hành song song; bảng Linh Thú, đi theo chủ, người khác thấy đều dùng lại | Cho linh thú một ô riêng (đeo cùng lúc với con giáp) |
| Phong Ấn Phù lấy ở đâu | Sạp Tạp Hóa bán, 60 Linh Thạch, 3 lá mỗi ngày | Theo luật rơi đồ, sạp là nguồn không khoá theo tu vi; bùa chỉ dùng được từ tầng 3 nên không cho ai vượt cấp; không vướng trần của vùng | Cho tinh anh rơi bùa: thêm vào `drops` và một mốc trong `loot_tiers.json` |
| Vị trí linh thú | Linh Hồ cạnh ngõ cụt có Thương trung phẩm, Huyền Quy trên đảo sương, Bạch Hạc trên bãi đá cao, Hỏa Tước trong tổ bên kia vực cạnh Thiết Kiếm, Tiểu Long trong lò lớn | Đúng `where_vi`; Hỏa Tước dùng chính túi đá sau vực, nên phải lướt mới tới | Đổi `pos` của linh thú |
| Linh thú hỏi gì | Câu của các nút mà quái cùng vùng đứng cho | "Toán của nhánh vùng"; Tiểu Long ở vùng Lập Trình cũng có câu hỏi (phần toán mà Lập Trình ôn lại) | Cho linh thú `nodes` riêng |
| Cưỡi | Chỉ Tiểu Long cưỡi được (quà `mount`), nhanh gấp 1,5; người cưỡi ngồi tư thế đả tọa trên lưng nó, nó lớn gấp đôi khi được cưỡi | Kế hoạch ghi "Cưỡi được" là quà của Tiểu Long; bộ hình không có tư thế cưỡi riêng | Thêm quà `mount` cho linh thú khác |
| Lướt | Tối đa 80 px (5 ô), chỉ qua nước và vực, hồi 2,5 giây | Đủ qua hai ô vực ở Kiếm Trủng Sơn và hai ô thác ở Lưu Vân Cốc, không đủ bay qua cả hồ | Đổi `glide` của `dap_kiem_luot` |

## Chưa làm

- **Mọi thứ sau Luyện Khí** trong `world_plan.json`: chưa nối (`"wired": false`): Vân Hải Thiên Đảo, Kỳ Lân Con
  và các mở khoá từ Ngự Kiếm Phi Hành trở đi chờ Trúc Cơ. **Vùng đất, binh khí, linh thú và thần thông của
  Luyện Khí đã nối** (xem các phần trên). **Luật đánh quái mới cũng đã nối** (`"wired_sections": ["combat",
  "lands", "weapons", "beasts", "abilities"]`, ngày 2026-11-20): ở mọi vùng hoang chỉ hỏi khi bị quái đánh trúng, có Phản Đòn, thời gian nghỉ, vùng đánh tròn /
  quạt / thẳng và Né Đòn (mở ở Luyện Khí tầng 1). Bí cảnh, hầm ngục, thủ thành và cơ duyên giữ luật cũ. Phản
  Đòn được đếm khi thu phục linh thú (chưa đếm cho việc gì khác).
- **Nội dung cho nút thực chiến, dự án** và mọi cảnh giới sau Luyện Khí. Thiết kế cách làm ở
  `docs/THUC_CHIEN_TRONG_GAME.md`.
- **Bài NumPy** (nút lập trình NumPy, tầng 4 của Luyện Khí): chưa viết vì NumPy chưa được cài kèm game, và
  chủ dự án chưa quyết có bắt người chơi tự cài hay không. Nút vẫn hiện "Đang biên soạn", không chặn gì. Chín
  nút lập trình còn lại của Luyện Khí đã có 3-5 bài mỗi nút (`server/data/math/problems/`), đều đánh dấu
  chưa duyệt (`reviewed` không ghi, mặc định chưa duyệt), chờ một người đọc lại đề.
- **Luận Đạo Đài** (bài tự luận) đã gác lại: chủ dự án bỏ việc chấm bằng API (2026-11-20). Đề vẫn còn làm
  dữ liệu tham khảo, không có màn hình (`docs/LUAN_DAO_DAI.md`).
- **Vi kỹ năng "Hiệp phương sai, tương quan và hồi quy"** (nút chính đạo tầng 8) nằm ở tầng ẩn 10 của Xác
  Suất, chưa có câu hỏi: hiện là nút "đang biên soạn".
