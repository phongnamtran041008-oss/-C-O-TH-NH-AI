# Tân thủ và Lộ Trình — hướng dẫn người chơi mới, bảng việc cần làm

> Viết ngày 2026-11-20 theo yêu cầu của tác giả: "làm phần hướng dẫn tân thủ cho người chơi biết cần phải
> làm gì, và bảng nhiệm vụ để họ biết phải làm gì tiếp theo, có sẵn hướng dẫn và lộ trình".

## Người chơi thấy gì

1. **Lời chào của Trúc Lão.** Lần đầu vào Động Phủ (hoặc lần đầu đăng nhập sau bản này), Trúc Lão nói năm
   câu: game này tu tiên bằng toán, Đạo Thụ là gì, một nút học ba bước, và bấm F1 để xem việc tiếp theo.
   Hết lời chào thì bảng Lộ Trình tự mở. Lời chào này **thay cho hướng dẫn gieo hạt của game học chữ cũ**.
2. **Ô "Việc tiếp theo" trên màn hình.** Góc trên bên phải ở Động Phủ, dưới bản đồ nhỏ khi ở ngoài. Trước khi
   nghe lời chào và mở bảng: bước đang làm và một dòng cách làm. Sau đó **luôn là Chính đạo** (xem dưới): tên
   nút, bước của nó và tiến độ; có thưởng chờ nhận thì góc phải ghi "Nhận n". Bấm vào ô hoặc bấm **F1** để mở bảng.
3. **Bảng Lộ Trình** (F1), hai thẻ:
   - *Lộ trình*: bốn chương, mỗi chương là các bước. Mỗi bước ghi **làm gì, vì sao, bấm phím hay nút nào**,
     tiến độ, phần thưởng; nút *Đi tới* mở đúng màn hình cần dùng, nút *Cẩm nang* mở trang giải thích.
     Bước xong thì nhận thưởng một lần; xong mọi bước bắt buộc của chương thì có thưởng chương. Ô *Đang học*
     ghi nút Đạo Thụ nên học lúc này.
   - *Cẩm nang*: 14 trang ngắn — Chính đạo, Đạo Thụ, buổi luyện, Cổng và Thiên kiếp nhỏ, tâm ma, Tàng Thư Các, Hầm
     Ngục, Thủ Thành, Cơ Duyên, chiêu thức, bài tập lập trình, phím tắt, một ngày tu luyện.
4. Khi một bước vừa xong, màn hình báo "Xong: ..." ngay sau việc vừa làm.

## Chính đạo là nhiệm vụ chính

> Thêm ngày 2026-11-21 theo yêu cầu của tác giả: "nhiệm vụ chính phải là lộ trình học đúng cho người chơi, để họ
> không học lan man".

- **Một con đường.** `server/data/math/tree.json` có thêm `main_path`: mọi nút chính đạo xếp thành **một thứ tự
  duy nhất** — cảnh giới, tầng, rồi thứ tự trong tầng. Nút luôn đứng sau nút nó cần; nút lập trình / thực chiến
  đứng **ngay sau phần toán nó dùng** (Vectơ và ma trận bằng code ngay sau Nhân ma trận, k láng giềng ngay sau
  đó; Đạo hàm số ngay sau Cực trị; PCA nén dữ liệu ngay sau PCA và SVD...). `tools/check_tree.py` từ chối thứ tự
  sai; `docs/GIAO_TRINH_CAY.md` đánh số từng tầng theo thứ tự ấy.
- **Một việc.** Máy chủ tính `main`: nút đầu tiên trên đường chưa xong và bước của nó — **Hiểu** (Học bài, mở
  bài ở Tàng Thư Các), **Luyện** (tới khi Cổng mở), **Vượt cổng** (Độ Thiên kiếp nhỏ); nút lập trình là **Làm
  bài tập**. Mở bài đọc được ghi vào `users.flags["path"]`; ai đã có câu trả lời trên phần ấy (bản lưu cũ) coi
  như đã đọc, nên không ai bị bắt quay lại.
- **Đạo Thụ mở ra ở thẻ Chính đạo**: một thẻ lớn ghi đủ tên nút, vì sao người làm AI cần nó, ba ô Hiểu > Luyện >
  Vượt cổng, và **một** nút đỏ (cũng là phím Enter). Dưới thẻ là các nút của tầng theo thứ tự: đã xong / đang học
  / để sau. Các thẻ nhánh vẫn còn để xem cả cây; nút đang mở mà đi trước chỗ người chơi đứng có dấu "Để sau"
  nhưng không bị khoá.
- **Ô Việc tiếp theo** (sau hai bước chào) luôn ghi "Chính đạo 2/5 · F1", tên nút, và bước ("Luyện · Cổng 1/4").
  **Bảng F1** mở ở mục *Chính đạo*: cùng việc ấy, nút *Đi tới* làm đúng việc của nút đỏ trong Đạo Thụ.
- **Luyện thêm.** Hầm Ngục, Thủ Thành, Cơ Duyên nằm nhỏ ở đáy Đạo Thụ dưới chữ "Luyện thêm"; các bước của chúng
  trên bảng đều là tuỳ chọn. *Chưa làm:* chúng vẫn hỏi theo luật cũ — Hầm Ngục và Thủ Thành hỏi mọi nút chính đạo
  **đang mở** (kể cả nút đang mở mà người chơi chưa tới trên Chính đạo, ví dụ nút đầu của Giải Tích khi người chơi
  mới ở nút 1), Cơ Duyên hỏi phần mở đầu tiên của môn Đại Số. Giới hạn vào "đã xong hoặc đang học" làm hỏng 9 bài
  kiểm thử của hai chế độ ấy (tầng hầm và tháp mở theo nút "đang mở"), nên để phiên giữ hai chế độ ấy quyết.

## Bốn chương

| Chương | Nội dung | Bước |
|---|---|---|
| Nhập Môn | 15 phút đầu: gặp Trúc Lão, mở bảng, mở Đạo Thụ, đọc bài đầu (Học bài), buổi luyện đầu, đúng 5 câu, Thiên kiếp nhỏ đầu, xong nút đầu | 8 bắt buộc + kiểm tra đầu vào (tuỳ chọn) |
| Chính Đạo Tầng Một | Năm nút của tầng 1 **đúng thứ tự Chính đạo**: Tập hợp và ánh xạ, Logic và quy tắc đếm, Python nhập môn, Hàm số, Sự kiện và phép đếm; 50 câu; 4 Thiên kiếp nhỏ | 7 bắt buộc + phá 3 tâm ma (tuỳ chọn) |
| Luyện Thêm | Xuống làng, mở chiêu thức thứ tư; Hầm Ngục, Thủ Thành, Cơ Duyên, bài lập trình, trắc linh căn là tuỳ chọn | 2 bắt buộc + 5 tuỳ chọn |
| Đường Luyện Khí | Chín tầng Luyện Khí, **sinh tự động từ Đạo Thụ**: mỗi tầng liệt kê các nút chính đạo còn lại | 9 |

Id của chương và bước không đổi (thưởng đã nhận lưu theo id). Bốn bước "nút đầu mỗi nhánh" giờ kiểm đúng nút ấy
(`node_done`) và xếp theo Chính đạo; bước mới `g_node_lt` (Python nhập môn). Bước nào đã nhận thưởng vẫn là đã
nhận.

## Cách hoạt động

- **Mọi tiến độ được suy ra từ dữ liệu đã có** (câu đã trả lời, buổi luyện, Thiên kiếp đã qua, vị trí trên Đạo
  Thụ, lượt hầm ngục, sao thủ thành, bài lập trình đã giải...). Không hệ thống nào khác phải gọi sang đây,
  nên bản lưu cũ mở lên là thấy ngay các bước đã làm và nhận được thưởng của chúng.
- Chỉ năm việc do máy người chơi báo lên, vì máy chủ không tự biết: đã nghe lời chào, đã mở bảng, đã mở Đạo
  Thụ, đã mở một trang Tàng Thư, đã xuống làng.
- Trạng thái của người chơi nằm trong `users.flags["guide"]` (`claimed`, `seen`): **không có bảng mới, không
  có migration**. Thưởng không thể trả hai lần kể cả khi hai yêu cầu tới cùng lúc (ghi có điều kiện vào cột
  flags, thêm một dòng đánh dấu trong sổ `audit_log`).
- Nội dung ở một file: `server/data/guide.json` (lời chào, chương, bước, phần thưởng, cẩm nang). Sửa chữ hay
  thưởng không cần đụng code. `python tools/check_guide.py` (cũng nằm trong `tools/check_all.py`) kiểm loại
  kiểm tra, mã `goto`, độ dài chữ để vừa khung, và mọi ký tự đều vẽ được bằng font của game.

Mã nguồn: `server/app/systems/guide.py`, `server/app/routers/guide_routes.py` (`GET /guide`,
`POST /guide/claim`, `POST /guide/seen` — xem `docs/API.md`), `client/scenes/guide.py`. Kiểm:
`server/tests/test_guide.py`, `client/tests/test_guide_units.py`, `client/tests/test_guide_flow.py`
(chạy `python -m client.tests.test_guide_flow <thư mục>` để chụp lại các màn hình).

Chỗ nối vào file dùng chung đều nhỏ và chỉ thêm: `client/main.py` (tải bảng, báo "đã thấy", mở bảng),
`client/scenes/abode.py` và `world.py` (vẽ ô, phím F1, tắt hướng dẫn cũ), một dòng ở `math_library.py` và
`math_practice.py`, một khối chữ cuối `client/strings_vi.py`, hai dòng ở `server/app/main.py`, phép kiểm thứ
19 trong `tools/check_all.py`.

## Tôi tự quyết — bạn đổi được

| Việc | Tôi chọn | Vì sao | Muốn khác thì |
|---|---|---|---|
| Phím mở bảng | F1 | Phím "trợ giúp" quen thuộc, chưa ai dùng | Đổi ở `abode.py`, `world.py` và chữ trong `guide.json` |
| Hướng dẫn gieo hạt cũ | Đã xoá hẳn khi gộp với nhánh dọn game học chữ (2026-11-20); `guide.WELCOME` chỉ còn là công tắc bật/tắt lời chào mới | Bạn đã quyết xoá game học chữ; người mới không nên được dạy gieo hạt | Không còn gì để bật lại; `WELCOME = False` chỉ tắt lời chào (các bài test cũ dùng) |
| Phần thưởng | Chỉ Linh Thạch và Tu Vi: bước 20–120 Linh Thạch, 10–50 Tu Vi; thưởng chương 120/200/280 Linh Thạch kèm 5/7/10 Tiên Ngọc; chín tầng Luyện Khí 100→300 Linh Thạch, 40→150 Tu Vi, tầng 9 thêm 10 Tiên Ngọc | Đủ để thấy có thưởng, không làm lệch kinh tế. Tổng cả bảng (kể cả bước tuỳ chọn) là 3.695 Linh Thạch, 1.390 Tu Vi, 32 Tiên Ngọc | Sửa số trong `guide.json` |
| Bước không khoá nhau | Bước nào đủ điều kiện là xong, không cần theo thứ tự | Tiến độ suy ra từ dữ liệu; người chơi cũ không bị bắt làm lại | — |
| Bước tuỳ chọn | Kiểm tra đầu vào, phá 3 tâm ma, Cơ Duyên, bài lập trình | Người không sai câu nào thì không có tâm ma; Cơ Duyên là ngẫu nhiên; lập trình cần máy có Python | Bỏ `"optional": true` |
| Bảng Nhiệm vụ cũ (phím J) | Giữ nguyên, không đụng | Các chuỗi ở đó thuộc game cũ, do phiên dọn game cũ xử lý | Khi dọn xong có thể gộp J vào F1 |

## Chưa làm

- **Việc hằng ngày** có thưởng (ví dụ "hôm nay luyện một buổi"): hiện chỉ là trang cẩm nang *Một ngày tu
  luyện*. Nhiệm vụ ngày cũ (phím J) vẫn đếm theo game học chữ.
- **Chương sau Luyện Khí**: thêm một chương `"generated": "tree_stages"` với `realm` khác là có, khi các cảnh
  giới ấy có nội dung.
- **Chưa ai chơi tay**: mọi thứ được kiểm bằng test tự động và ảnh chụp màn hình. Chưa kiểm: nhận thưởng
  chương từ giao diện, nút *Đi tới* của Hầm Ngục / Thủ Thành / Cơ Duyên / Tàng Thư, lời chào khi người chơi
  đăng nhập lại đang đứng ở ngoài làng, và máy chủ PostgreSQL (test chạy trên SQLite).
- **Bản web (M12)**: trình duyệt dùng F1 cho trợ giúp của nó; lúc làm bản web cần thêm phím khác.
- Nút dưới màn hình Động Phủ vẫn còn các mục của game cũ (Ghép câu, Tổ ong, Thiên Cơ); cẩm nang không nhắc
  tới chúng.
