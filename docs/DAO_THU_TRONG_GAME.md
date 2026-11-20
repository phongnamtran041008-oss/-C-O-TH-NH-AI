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

## Binh khí trên các vùng đất

Phần binh khí của `world_plan.json` đã nối (`"wired_sections": ["combat", "weapons"]`, 2026-11-20); mở khoá
`nhat_vu_khi` (Luyện Khí tầng 1) và `nang_pham` (Luyện Khí tầng 4) là `"co"`. Luật ở
`server/app/systems/weapons.py`, đường `GET /weapons`, `POST /weapons/claim`, `/weapons/equip`,
`/weapons/unequip`, `GET/POST /weapons/upgrade` (`docs/API.md`).

- **Tu vi của yêu cầu là chỗ đứng trên Đạo Thụ.** Một chỗ đặt mở khi tầng trên cây tới tầng nó ghi, mọi nút nó
  ghi đã xong (nút "Đang biên soạn" tính là xong, như luật 3), vùng đất của nó đã mở (`opens` của vùng) và năng
  lực nó cần (`needs`, ví dụ Đạp Kiếm Lướt) đã có trong game. Chưa đủ thì danh sách nói thiếu gì, gọi nút bằng tên.
  Bốn chỗ cần Đạp Kiếm Lướt hay Ngự Kiếm Phi Hành vì thế còn khoá cho tới khi năng lực ấy được làm.
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
- **Chưa có ở đây**: điểm nhặt trên bản đồ (phiên vùng đất vẽ và gọi `POST /weapons/claim`).

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
| Phẩm của binh khí | Lưu thành độ hiếm có sẵn (hạ = Phàm, trung = Linh, thượng = Huyền), Công theo `power` của kế hoạch | Một mô hình trang bị: túi, sạp, cường hóa, Bảo Vật Phổ dùng được ngay, không cần bảng mới | Đổi `rarity` của từng phẩm trong `qualities` |
| Binh khí và nhánh | Phản Đòn câu đúng nhánh của binh khí mạnh thêm 50%; Chùy, Cung (nhánh không có môn toán riêng) thêm 15% mọi câu | Một luật dễ thấy, cho người chơi lý do cầm binh khí hợp môn đang học | Đổi hai số `weapons.*_parry_bonus` |
| Nâng phẩm | 4 Lõi Ma Trận + 3 Mực Tinh + 40 Linh Thạch, chỉ hạ → trung | Lõi Ma Trận rớt từ Luyện Khí tầng 4, đúng lúc nâng phẩm mở; trung → thượng để dành cho chỗ đặt thượng phẩm | Sửa `crafting.json`, mục `upgrades` |

## Chưa làm

- **Vùng đất, linh thú và các mở khoá theo tu vi khác** trong `world_plan.json`: chưa có dòng code
  nào dùng (`"wired": false`). **Binh khí đã nối** (mục "Binh khí trên các vùng đất" ở trên). **Luật đánh quái mới thì đã nối** (`"wired_sections": ["combat"]`, ngày
  2026-11-20): ở mọi vùng hoang chỉ hỏi khi bị quái đánh trúng, có Phản Đòn, thời gian nghỉ, vùng đánh tròn /
  quạt / thẳng và Né Đòn (mở ở Luyện Khí tầng 1). Bí cảnh, hầm ngục, thủ thành và cơ duyên giữ luật cũ. Còn
  thiếu của phần này: `phap_tran` (pháp trận làm quái ra đòn chậm) và việc thuần phục linh thú bằng Phản Đòn
  (`parries_to_tame`) chờ đợt linh thú; số đòn Phản Đòn chưa được đếm ở đâu cả.
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
