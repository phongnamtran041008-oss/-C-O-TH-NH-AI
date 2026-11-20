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

- Dòng đầu cho biết đang ở đâu, ví dụ "Luyện Khí tầng 2/9".
- Thẻ **Nên học** liệt kê các nút chính đạo đang mở; sau đó mỗi nhánh một thẻ (Đại Số, Giải Tích, Xác
  Suất, Thuật Toán, Lập Trình, Thực Chiến), nút xếp theo tầng, bàng môn ở cuối.
- Mỗi dòng là một phần của nút: tên, bậc khó, tiến độ cổng thuần thục hoặc nút Thiên kiếp, nút Đọc (bài ở
  Tàng Thư Các), nút Luyện. Nút còn khoá ghi rõ cần xong nút nào; nút chưa có nội dung ghi "Đang biên soạn".
- Bấm vào tên nút mở **thẻ nút**: vì sao học, cần xong gì trước, ôn lại gì, học những gì, và **Nên học từ**
  — nguồn tốt nhất cho nút ấy lấy từ `server/data/math/sources/` (tên, tác giả, xem phần nào, ngôn ngữ,
  đường dẫn). Nút "Mở trang" mở đường dẫn bằng trình duyệt của máy; game không tự mở trang nào.
- Qua Thiên kiếp nhỏ của một nút thì màn kết quả nói nút nào vừa mở, kể cả nút của nhánh khác.

## Tôi tự quyết — bạn đổi được

| Việc | Tôi chọn | Vì sao | Muốn khác thì |
|---|---|---|---|
| Nút chưa có nội dung | Coi như xong, hiện "Đang biên soạn", không chặn gì | Nút Python nhập môn ở tầng 1 chưa có bài: nếu chặn thì không ai rời được tầng 1. Hiện 17 trên 19 nút lập trình/thực chiến/dự án của Luyện Khí chưa có nội dung | Viết nội dung cho nút: nó tự bắt đầu tính |
| Tầng tu vi trên cây và cảnh giới nhân vật | **Không nối.** Tầng trên cây chỉ hiển thị; Tu Vi và cảnh giới nhân vật vẫn như cũ | Cách quy đổi là việc bạn chưa quyết | Nói cách quy đổi, tôi nối |
| Cảnh giới chưa viết | Vị trí dừng ở Luyện Khí tầng 9 | Mọi nút sau Luyện Khí đều chưa có nội dung; nếu không chặn thì xong Luyện Khí sẽ hiện thẳng "Đại Thừa tầng 3" | — |
| Thiên kiếp nhỏ của phần nhỏ | Số câu được sai = tối đa 1, nhưng không quá một phần tư số câu: phần 1-3 vi kỹ năng phải đúng hết | Trước đây mỗi tầng 5-6 câu, sai 1 vẫn qua. Phần của nút có khi chỉ 1-2 vi kỹ năng: giữ luật cũ thì sai một nửa, thậm chí sai hết, vẫn qua | Đổi trong `math_mastery.trial_allowed` |
| Tháp Số Phức (thủ thành) | Mở khi người chơi xong nút bàng môn Số phức | Tầng 2 của Đại Số chỉ còn nút bàng môn, nên theo luật 6 và 12 tháp ấy sẽ không bao giờ mở | — |
| Bài kiểm tra đầu vào | Giữ nguyên: vẫn hỏi theo cả tầng, kể cả vi kỹ năng bàng môn | Đổi cách hỏi là viết lại bài kiểm tra | Làm thành một việc riêng |
| Quái lỗi sai | Vẫn hỏi đúng vi kỹ năng của nó, kể cả khi nút ấy chưa mở | Nó không đọc vị trí của người chơi; vi kỹ năng bị loại thì vẫn không bao giờ hỏi | — |

## Chưa làm

- **Binh khí, vùng đất, linh thú và các mở khoá theo tu vi khác** trong `world_plan.json`: chưa có dòng code
  nào dùng (`"wired": false`). **Luật đánh quái mới thì đã nối** (`"wired_sections": ["combat"]`, ngày
  2026-11-20): ở mọi vùng hoang chỉ hỏi khi bị quái đánh trúng, có Phản Đòn, thời gian nghỉ, vùng đánh tròn /
  quạt / thẳng và Né Đòn (mở ở Luyện Khí tầng 1). Bí cảnh, hầm ngục, thủ thành và cơ duyên giữ luật cũ. Còn
  thiếu của phần này: `phap_tran` (pháp trận làm quái ra đòn chậm) và việc thuần phục linh thú bằng Phản Đòn
  (`parries_to_tame`) chờ đợt linh thú; số đòn Phản Đòn chưa được đếm ở đâu cả.
- **Nội dung cho nút lập trình, thực chiến, dự án** và mọi cảnh giới sau Luyện Khí. Thiết kế cách làm ở
  `docs/THUC_CHIEN_TRONG_GAME.md`.
- **Luận Đạo Đài** (bài tự luận) có bộ máy chấm nhưng chưa có màn hình (`docs/LUAN_DAO_DAI.md`).
- **Bài tập của nút lập trình** hiện trên thẻ nút nhưng chỉ làm được từ nút "Bài tập" ở thẻ Đại Số; thẻ
  nút chưa có nút "Làm bài".
- **Câu ôn** trên thẻ câu hỏi vẫn ghi "Ôn xoắn ốc: tầng N"; nay câu ôn có thể đến từ môn khác, nên ghi tên
  nút được ôn thì đúng hơn.
- **Dòng "đang ở đâu"** chỉ đổi khi xong mọi nút chính đạo của một tầng ở cả bốn nhánh, nên đứng yên khá
  lâu sau nút đầu tiên. Có thể thêm "đã xong 1/4 nút của tầng 1".
- **Vi kỹ năng "Hiệp phương sai, tương quan và hồi quy"** (nút chính đạo tầng 8) nằm ở tầng ẩn 10 của Xác
  Suất, chưa có câu hỏi: hiện là nút "đang biên soạn".
