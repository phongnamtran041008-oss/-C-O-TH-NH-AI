# Ghi công (Credits)

Toán Tu Tiên dùng các dữ liệu và công cụ mở sau. Cảm ơn những người đã xây dựng chúng.

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

Tầng ẩn 10 của bốn môn cũng do AI viết, từng câu một: Đại Số (cấu trúc đại số, dạng song tuyến tính; theo tên mục của
MI1141), Giải Tích (số thực, khả tích, hàm lồi, không gian metric; MI1111), Xác Suất và Thống Kê (hàm của biến ngẫu
nhiên, tương quan, hồi quy; MI3030, MI3350) và Tối Ưu - Rời Rạc (phương pháp tính; MI2044). Chỉ tên mục và tên khái
niệm được lấy từ các đề cương đó; định nghĩa và định lý nền (tiên đề cận trên đúng, tổng Darboux, bất đẳng thức
Jensen, định lý Lagrange về nhóm con, bình phương tối thiểu, quy tắc lan truyền sai số, phép lặp Newton) là kiến thức
chuẩn của môn, được viết lại bằng lời và ví dụ riêng, không chép văn bản của sách nào. Ngoài các bộ sinh câu, mọi đáp
số của câu viết tay ở tầng này cũng được SymPy tính lại (`tools/math_verify_<môn>_t10.py`).

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
không dùng gói asset bên ngoài.

## Model 3D cho icon (M8)

Model low-poly tải từ Poly Pizza (https://poly.pizza) bằng `tools/fetch_models.py`; icon trong game là ảnh render từ chúng.
CC0 thì không bắt buộc ghi công, nhưng vẫn ghi ở đây cho đủ dấu vết; CC-BY thì **bắt buộc** giữ dòng ghi công.

- cong_phap/cuon_thu: "Scroll" — Poly (CC-BY) — https://poly.pizza/m/arIYNl9gMyr
- cong_phap/cuon_thu: "Scroll" — Quaternius (CC0) — https://poly.pizza/m/MWGB9nxMIc
- cong_phap/sach: "Open Book" — Quaternius (CC0) — https://poly.pizza/m/FsCIGEfTEs
- cong_phap/sach: "Book Stack" — Danni (CC-BY) — https://poly.pizza/m/1WggoIFq8tx
- dan_duoc/dan: "Potion Bottle - Game Asset" — Don (CC-BY) — https://poly.pizza/m/dOREefQfDQu
- dan_duoc/dan: "Potion Bottle" — Quaternius (CC0) — https://poly.pizza/m/WJxYta4Z96
- dan_duoc/dan: "Complex Health Potion" — Garrett (CC-BY) — https://poly.pizza/m/5DvOJDIgDYu
- dan_duoc/linh_thao: "Mushroom" — jeremy (CC-BY) — https://poly.pizza/m/2DAaKHD48ZP
- dan_duoc/linh_thao: "Bamboo" — Zsky (CC-BY) — https://poly.pizza/m/mKh1dBFt9p
- dan_duoc/lo_dan: "Cauldron" — Quaternius (CC0) — https://poly.pizza/m/QaWJOPa6Gt
- trang_bi/ao_giap: "Áo giáp" — tự dựng trong Blender (own work) — tools/blender/build_items.py
- trang_bi/day_chuyen: "Necklace" — Quaternius (CC0) — https://poly.pizza/m/Jvhs8DCNDZ
- trang_bi/gang: "Glove" — Quaternius (CC0) — https://poly.pizza/m/l1zv4LaA4I
- trang_bi/giay: "Boots" — Poly (CC-BY) — https://poly.pizza/m/7HbqG8RwRcA
- trang_bi/khien: "Shield" — Quaternius (CC0) — https://poly.pizza/m/srN1KGAO7f
- trang_bi/khien: "Shield" — Quaternius (CC0) — https://poly.pizza/m/xoHSnOjsBG
- trang_bi/mu: "Wizard hat" — Poly (CC-BY) — https://poly.pizza/m/7VVumyY7L_u
- trang_bi/mu: "Witch Hat" — J-Toastie (CC-BY) — https://poly.pizza/m/fy1Elzr3nl
- trang_bi/nhan: "Halo" — Poly (CC-BY) — https://poly.pizza/m/5jiuuz7sOV_
- vu_khi/bua: "Mace" — Poly (CC-BY) — https://poly.pizza/m/40LBkajLUig
- vu_khi/bua: "d20 mace" — Robin (CC-BY) — https://poly.pizza/m/32NZ3FY4yo-
- vu_khi/cung: "Bow" — Zsky (CC-BY) — https://poly.pizza/m/XkJVO6cACA
- vu_khi/cung: "Wooden Bow" — Quaternius (CC0) — https://poly.pizza/m/QnpqjLSKFU
- vu_khi/dao: "Katana" — dook (CC-BY) — https://poly.pizza/m/zV3WXbyjMf
- vu_khi/dao: "Katana" — Pichuliru (CC0) — https://poly.pizza/m/15A7InejC7
- vu_khi/ho_lo: "Hồ lô" — tự dựng trong Blender (own work) — tools/blender/build_items.py
- vu_khi/kiem: "Sword" — Quaternius (CC0) — https://poly.pizza/m/9lLmH8Et4K
- vu_khi/kiem: "Short Sword" — joney_lol (CC-BY) — https://poly.pizza/m/8euoHHy9Le
- vu_khi/kiem: "Katana Sword" — Nick (CC-BY) — https://poly.pizza/m/7Ly4_Ou8HXK
- vu_khi/quat: "Quạt xếp" — tự dựng trong Blender (own work) — tools/blender/build_items.py
- vu_khi/thuong: "Spear" — Quaternius (CC0) — https://poly.pizza/m/fH1zmvjPNx
- vu_khi/thuong: "Pike" — joney_lol (CC-BY) — https://poly.pizza/m/CcIAY7h9aE
- vu_khi/truong: "Staff" — Zsky (CC-BY) — https://poly.pizza/m/DZpBi0DSgZ
- vu_khi/truong: "Staff" — Quaternius (CC0) — https://poly.pizza/m/PnGRvO4Lwd
