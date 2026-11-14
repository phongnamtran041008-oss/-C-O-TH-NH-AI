# Ảnh công thức trong Tàng Thư Các

Mỗi tệp `.png` trong thư mục này là một công thức toán của bài đọc trong
`server/data/math/library/`, được dựng sẵn bằng `python tools/build_formulas.py` để lúc
chơi game không cần phông chữ toán, không cần mạng và không cần công cụ dựng công thức.
Tên tệp là mã băm của chính công thức đó; `server/data/math/formulas.json` ghi công thức,
dạng chữ thường và kích thước của từng ảnh.

Nội dung công thức (chọn công thức nào, viết ra sao) là của dự án này, cùng giấy phép với
phần nội dung còn lại — xem `CREDITS.md`.

Nét chữ trong ảnh do **MathJax** vẽ, nên các đường nét đó là phông toán của MathJax:

- MathJax — Apache License 2.0 — https://github.com/mathjax/MathJax
  Phông toán của MathJax dẫn xuất từ phông TeX của American Mathematical Society,
  phát hành theo Apache License 2.0 và SIL Open Font License 1.1.

Công cụ chỉ dùng lúc dựng ảnh, **không** đi kèm game và không có mặt trong thư mục này:

- resvg / @resvg/resvg-js — Mozilla Public License 2.0 — https://github.com/linebender/resvg

Toàn văn Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0
Toàn văn SIL OFL 1.1: https://openfontlicense.org
Toàn văn MPL 2.0: https://www.mozilla.org/MPL/2.0/
