# Ghi công (Credits)

Khu Vườn Tu Tiên dùng các dữ liệu và công cụ mở sau. Cảm ơn những người đã xây dựng chúng.

## Dữ liệu ngôn ngữ

- **CC-CEDICT** — từ điển Trung–Anh do cộng đồng duy trì, phát hành bởi MDBG.
  Giấy phép: Creative Commons Attribution-ShareAlike 4.0 International
  (https://creativecommons.org/licenses/by-sa/4.0/).
  Trang chủ: https://cc-cedict.org/wiki/ · Tải về: https://www.mdbg.net/chinese/dictionary?page=cc-cedict
  Dựa trên CEDICT — Copyright (C) 1997, 1998 Paul Andrew Denisowski.
  Bản dùng trong lần dựng hiện tại: export ngày 2023-11-07 (xem `tools/raw/SOURCES.md`).
- **complete-hsk-vocabulary** (Yanis Zafirópulos, https://github.com/drkameleon/complete-hsk-vocabulary)
  — danh sách từ HSK 3.0. Giấy phép MIT.
- **Make Me a Hanzi** (Shaunak Kishore, https://github.com/skishore/makemeahanzi) — tệp `dictionary.txt`
  (bộ thủ, cấu tạo chữ), dẫn xuất từ Unihan và CJKlib. Giấy phép GNU LGPL phiên bản 3 trở lên.

**Giấy phép của dữ liệu từ vựng trong game:** các tệp `server/data/words/*.json`,
`server/data/sentences.json`, `combos.json`, `tone_mishaps.json`, `creatures/bees.json` (tên Hán và pinyin của ong), `creatures/fish.json` (tên Hán, pinyin, nghĩa tiếng Anh của cá) chứa nội dung dẫn xuất từ CC-CEDICT,
nên được phát hành theo cùng giấy phép **CC BY-SA 4.0**. Phần dẫn xuất từ Make Me a Hanzi giữ giấy phép
LGPL-3.0+.

Nghĩa tiếng Việt, câu ví dụ, câu luyện tập và truyện thành ngữ do AI viết dựa trên nghĩa tiếng Anh của
CC-CEDICT và **cần người duyệt** (cờ `meaning_vi_reviewed`, `example_reviewed`, `reviewed`).

## Lộ trình toán (nhánh `toan-tu-tien`)

Thứ tự và tên các tầng của mỗi bí cảnh toán đi theo **tên chương, mục** trong đề cương học phần công khai
của Đại học Bách khoa Hà Nội (HUST). Game chỉ dùng tên chương/mục làm khung; tên và mô tả vi kỹ năng,
câu hỏi, lời giải và tài liệu đều tự viết, không chép nội dung đề cương hay giáo trình.

- Đại Số Tuyến Tính (`server/data/math/dai_so_tuyen_tinh.json`): MI1144 Đại số (tầng 1–9),
  https://fami.hust.edu.vn/wp-content/uploads/MI1144-Decuong-Daiso-VN.pdf ; MI1141 Đại số, hệ tài năng
  (tầng ẩn 10), https://fami.hust.edu.vn/wp-content/uploads/MI1141-Decuong-Daiso-Tainang.pdf
- Ba bí cảnh còn lại (Giải Tích, Xác Suất và Thống Kê, Tối Ưu và Toán Rời Rạc) mới có tên và mã học phần
  trong `server/data/math/subjects.json`, chưa có nội dung. Đề cương của từng bí cảnh sẽ được ghi ở đây
  khi viết tới.

Các mục đánh dấu `"extension": "ai"` (ví dụ phép chiếu, PCA/SVD) là phần thêm cho lộ trình AI, không
nằm trong đề cương.

Ngân hàng câu hỏi (`server/data/math/items/`, `server/app/learning/math_gen/`) do AI viết: câu hỏi, đáp án
và lời giải đều tự soạn, không chép đề bài hay lời giải từ giáo trình, đề cương hay sách nào. Đáp án của
các bộ sinh câu được tính lại bằng SymPy; mọi câu **cần người duyệt** (cờ `reviewed`, bảng duyệt
`tools/reports/math_review_<bí cảnh>.md`).

## Phần mềm

FastAPI, SQLAlchemy, Alembic, bcrypt, PyJWT, Uvicorn, websockets, httpx, pygame-ce, pytest (các giấy phép
MIT/BSD/Apache/LGPL tương ứng). SymPy (BSD) và fontTools (MIT) chỉ dùng lúc kiểm tra nội dung
(`tools/math_verify.py`, `tools/check_all.py`, `server/requirements-dev.txt`), không đi kèm game hay máy chủ.

Ảnh công thức trong Tàng Thư Các được dựng sẵn bằng **MathJax** (Apache-2.0) và **resvg** (MPL-2.0) qua
`tools/formulas`; cả hai chỉ chạy lúc dựng nội dung, không nằm trong game. Nét chữ trong các ảnh đó là phông
toán của MathJax, dẫn xuất từ phông TeX của American Mathematical Society, phát hành theo **Apache-2.0** và
**SIL OFL 1.1**; giấy phép đi kèm trong `client/assets/formulas/LICENSES.md`.

## Phông chữ

- **Noto Sans SC** (Google / Adobe, https://github.com/notofonts/noto-cjk) — SIL Open Font License 1.1.
  Game dùng bản cắt gọn (subset) do `tools/fetch_assets.py` tạo; giấy phép đi kèm trong
  `client/assets/fonts/NotoSansSC-LICENSE.txt`.
- **VT323** (Peter Hull, The VT323 Project Authors, https://github.com/google/fonts/tree/main/ofl/vt323) —
  SIL Open Font License 1.1, giấy phép trong `client/assets/fonts/VT323-OFL.txt`.

## Hình ảnh và âm thanh

Toàn bộ hình pixel (nhân vật, dân làng, Mặc Quái gồm Mặc Hồ, vũ khí, hiệu ứng chiến đấu và sấm Thiên Kiếp, cây, nhà cửa, đạo cụ, bản đồ Trúc Lâm Thôn và Rừng Mực Loang) và âm thanh hiệu ứng được tạo bằng code trong dự án,
không dùng gói asset bên ngoài. Phát âm từ vựng (nếu có) tạo bằng `edge-tts` giọng `zh-CN-XiaoxiaoNeural`.
