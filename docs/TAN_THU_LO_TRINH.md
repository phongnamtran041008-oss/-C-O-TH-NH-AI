# Tân thủ và Lộ Trình — hướng dẫn người chơi mới, bảng việc cần làm

> Viết ngày 2026-11-20 theo yêu cầu của tác giả: "làm phần hướng dẫn tân thủ cho người chơi biết cần phải
> làm gì, và bảng nhiệm vụ để họ biết phải làm gì tiếp theo, có sẵn hướng dẫn và lộ trình".

## Người chơi thấy gì

1. **Lời chào của Trúc Lão.** Lần đầu vào Động Phủ (hoặc lần đầu đăng nhập sau bản này), Trúc Lão nói năm
   câu: game này tu tiên bằng toán, Đạo Thụ là gì, một nút học ba bước, và bấm F1 để xem việc tiếp theo.
   Hết lời chào thì bảng Lộ Trình tự mở. Lời chào này **thay cho hướng dẫn gieo hạt của game học chữ cũ**.
2. **Ô "Việc tiếp theo" trên màn hình.** Góc trên bên phải ở Động Phủ, dưới bản đồ nhỏ khi ở ngoài. Luôn ghi
   bước đang làm, tiến độ và một dòng cách làm; khi có thưởng chờ nhận thì đổi thành "Nhận thưởng (n)". Bấm
   vào ô hoặc bấm **F1** để mở bảng.
3. **Bảng Lộ Trình** (F1), hai thẻ:
   - *Lộ trình*: bốn chương, mỗi chương là các bước. Mỗi bước ghi **làm gì, vì sao, bấm phím hay nút nào**,
     tiến độ, phần thưởng; nút *Đi tới* mở đúng màn hình cần dùng, nút *Cẩm nang* mở trang giải thích.
     Bước xong thì nhận thưởng một lần; xong mọi bước bắt buộc của chương thì có thưởng chương. Ô *Đang học*
     ghi nút Đạo Thụ nên học lúc này.
   - *Cẩm nang*: 13 trang ngắn — Đạo Thụ, buổi luyện, Cổng và Thiên kiếp nhỏ, tâm ma, Tàng Thư Các, Hầm
     Ngục, Thủ Thành, Cơ Duyên, chiêu thức, bài tập lập trình, phím tắt, một ngày tu luyện.
4. Khi một bước vừa xong, màn hình báo "Xong: ..." ngay sau việc vừa làm.

## Bốn chương

| Chương | Nội dung | Bước |
|---|---|---|
| Nhập Môn | 15 phút đầu: gặp Trúc Lão, mở bảng, mở Đạo Thụ, đọc trang sách đầu, buổi luyện đầu, đúng 5 câu, Thiên kiếp nhỏ đầu, xong nút đầu | 8 bắt buộc + kiểm tra đầu vào (tuỳ chọn) |
| Bốn Nhánh Toán | Nút đầu của Đại Số, Giải Tích, Xác Suất, Thuật Toán; 50 câu; 4 Thiên kiếp nhỏ | 6 bắt buộc + phá 3 tâm ma (tuỳ chọn) |
| Thực Chiến | Xuống làng, phá một Hầm Ngục, thắng một ải Thủ Thành, mở chiêu thức thứ tư | 4 bắt buộc + Cơ Duyên, bài lập trình (tuỳ chọn) |
| Đường Luyện Khí | Chín tầng Luyện Khí, **sinh tự động từ Đạo Thụ**: mỗi tầng liệt kê các nút chính đạo còn lại | 9 |

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
