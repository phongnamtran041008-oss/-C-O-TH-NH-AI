# Bảng duyệt câu hỏi: Giải Tích

Tạo bởi `python tools/math_review.py`. Đánh dấu đã duyệt bằng `"reviewed": true` trong `server/data/math/items/giai_tich.json`.

## Tầng 1: Hàm số, hàm hợp, hàm ngược và hàm sơ cấp

55 dạng câu (45 câu viết tay, 10 bộ sinh câu); 55 chưa duyệt.

### Hàm số và tập xác định (`gt_t1_ham_so`)

- `gt_t1_hs_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 2x + 1. Khi đó f(3) = 7.
  - **Đáp án:** Đúng
    1. Thay x = 3 vào công thức: f(3) = 2 . 3 + 1.
    2. 2 . 3 + 1 = 7, nên mệnh đề đúng.
- `gt_t1_hs_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập xác định của hàm số f(x) = 1 / (x - 2) là tập nào?
    - **(đúng)** R \ {2}
    - R
    - (2, +vô cùng)
    - R \ {-2}
  - **Đáp án:** R \ {2}
    1. Một phân thức có nghĩa khi mẫu khác 0.
    2. x - 2 = 0 khi x = 2, nên chỉ phải bỏ đi số 2.
    3. Tập xác định là R \ {2}.
- `gt_t1_hs_03` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quy tắc gán mỗi số x >= 0 với mọi số thực y thỏa y^2 = x là một hàm số từ [0, +vô cùng) vào R.
  - **Đáp án:** Sai
    1. Một hàm số phải gán cho mỗi x đúng một giá trị y.
    2. Với x = 4 có hai số y thỏa y^2 = 4 là y = 2 và y = -2.
    3. Quy tắc gán hai giá trị cho một x nên không phải là hàm số.
- `gt_t1_hs_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với tập xác định của nó.
  - **Đáp án (ghép đúng):**
    - sqrt(x) — [0, +vô cùng)
    - 1/x — R \ {0}
    - ln x — (0, +vô cùng)
    - x^3 — R
  - **Lời giải:**
    1. sqrt(x) cần x >= 0: tập [0, +vô cùng).
    2. 1/x cần mẫu khác 0: tập R \ {0}.
    3. ln x chỉ có nghĩa khi x > 0: tập (0, +vô cùng), không lấy số 0.
    4. x^3 tính được với mọi số thực: tập R.
- `gt_g1_gia_tri` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hàm số f(x) = -2x^2 + 3x - 7. Tính f(0).
  - **Đáp án:** -7
    1. Thay x = 0 vào mọi chỗ có x trong công thức.
    2. f(0) = (-2) . 0^2 + 3 . 0 + (-7).
    3. = 0 + 0 + (-7) = -7.
  - **Câu hỏi:** Cho hàm số f(x) = -4x^2 - 5x - 7. Tính f(1).
  - **Đáp án:** -16
    1. Thay x = 1 vào mọi chỗ có x trong công thức.
    2. f(1) = (-4) . 1^2 + (-5) . 1 + (-7).
    3. = -4 + (-5) + (-7) = -16.
  - **Câu hỏi:** Cho hàm số f(x) = -x^2 + 3x + 8. Tính f(-2).
  - **Đáp án:** -2
    1. Thay x = -2 vào mọi chỗ có x trong công thức.
    2. f(-2) = (-1) . (-2)^2 + 3 . (-2) + 8.
    3. = -4 + (-6) + 8 = -2.
- `gt_t1_hs_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập xác định của hàm số f(x) = sqrt(4 - x^2) là tập nào?
    - **(đúng)** [-2, 2]
    - (-2, 2)
    - (-vô cùng, 2]
    - [0, 2]
  - **Đáp án:** [-2, 2]
    1. Biểu thức dưới căn phải không âm: 4 - x^2 >= 0.
    2. Tức là x^2 <= 4, hay -2 <= x <= 2.
    3. Hai đầu mút được lấy vì sqrt(0) = 0 có nghĩa: tập xác định là [-2, 2].
- `gt_t1_hs_06` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f thỏa f(x + 1) = 2x + 5 với mọi số thực x. Tính f(3).
  - **Đáp án:** 9
    1. Cần chọn x sao cho x + 1 = 3, tức x = 2.
    2. Thay x = 2 vào đẳng thức: f(3) = 2 . 2 + 5 = 9.
- `gt_t1_hs_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm tập xác định của f(x) = sqrt(x - 1) / (x - 3).
  - **Lời giải đưa ra (có một bước sai):**
    1. Biểu thức dưới căn phải không âm: x - 1 >= 0, tức x >= 1.
    2. Mẫu phải khác 0: x - 3 khác 0, tức x khác 3.
    3. Kết hợp hai điều kiện: x > 1 và x khác 3.   **<- bước sai đầu tiên**
    4. Tập xác định là (1, 3) hợp (3, +vô cùng).
  - **Đáp án:** Bước 3: Kết hợp hai điều kiện: x > 1 và x khác 3.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: điều kiện thứ nhất là x >= 1, nên số 1 vẫn được lấy (sqrt(0) = 0 và mẫu tại 1 bằng -2, khác 0).
    2. Kết hợp đúng: x >= 1 và x khác 3.
    3. Tập xác định là [1, 3) hợp (3, +vô cùng).
- `gt_t1_hs_08` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai hàm f(x) = (x^2 - 1) / (x - 1) và g(x) = x + 1, mỗi hàm lấy trên tập xác định của nó, là cùng một hàm số.
  - **Đáp án:** Sai
    1. Hai hàm số bằng nhau khi chúng có cùng tập xác định và cùng giá trị tại mọi điểm.
    2. g xác định trên R, còn f không xác định tại x = 1 vì mẫu bằng 0.
    3. Tập xác định khác nhau nên đây là hai hàm khác nhau, dù f(x) = x + 1 với mọi x khác 1.
- `gt_t1_hs_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm tập xác định của f(x) = sqrt(x^2 - 5x + 6).
  - **Đáp án (thứ tự đúng):**
    1. Viết điều kiện: x^2 - 5x + 6 >= 0.
    2. Phân tích thành nhân tử: (x - 2)(x - 3) >= 0.
    3. Tích này không âm khi hai thừa số cùng dấu hoặc có một thừa số bằng 0.
    4. Giải ra x <= 2 hoặc x >= 3.
    5. Tập xác định là (-vô cùng, 2] hợp [3, +vô cùng).
  - **Lời giải:**
    1. Căn bậc hai chỉ có nghĩa khi biểu thức dưới căn không âm.
    2. x^2 - 5x + 6 = (x - 2)(x - 3); tích này âm chỉ khi x nằm giữa 2 và 3.
    3. Vậy tập xác định là (-vô cùng, 2] hợp [3, +vô cùng).
- `gt_g1_khong_xac_dinh` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm số f(x) = (x - 4) / (x^2 + x - 12) không xác định tại những giá trị x nào? Liệt kê các giá trị đó.
  - **Đáp án:** -4, 3  (thứ tự nào cũng được)
    1. Một phân thức chỉ không có nghĩa khi mẫu bằng 0; tử bằng bao nhiêu cũng không ảnh hưởng.
    2. Giải x^2 + x - 12 = 0: phân tích thành (x + 4)(x - 3) = 0.
    3. Mẫu bằng 0 tại x = -4 và x = 3, nên f không xác định tại -4, 3.
  - **Câu hỏi:** Hàm số f(x) = (x - 4) / (x^2 + 11x + 30) không xác định tại những giá trị x nào? Liệt kê các giá trị đó.
  - **Đáp án:** -6, -5  (thứ tự nào cũng được)
    1. Một phân thức chỉ không có nghĩa khi mẫu bằng 0; tử bằng bao nhiêu cũng không ảnh hưởng.
    2. Giải x^2 + 11x + 30 = 0: phân tích thành (x + 6)(x + 5) = 0.
    3. Mẫu bằng 0 tại x = -6 và x = -5, nên f không xác định tại -6, -5.
  - **Câu hỏi:** Hàm số f(x) = (x + 3) / (x^2 - 9) không xác định tại những giá trị x nào? Liệt kê các giá trị đó.
  - **Đáp án:** -3, 3  (thứ tự nào cũng được)
    1. Một phân thức chỉ không có nghĩa khi mẫu bằng 0; tử bằng bao nhiêu cũng không ảnh hưởng.
    2. Giải x^2 - 9 = 0: phân tích thành (x + 3)(x - 3) = 0.
    3. Mẫu bằng 0 tại x = -3 và x = 3, nên f không xác định tại -3, 3.

### Hàm chẵn, hàm lẻ, hàm tuần hoàn (`gt_t1_tinh_chat_ham`)

- `gt_t1_tc_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm số f(x) = x^2 + cos x, xác định trên R, là hàm chẵn.
  - **Đáp án:** Đúng
    1. Tính f(-x) = (-x)^2 + cos(-x).
    2. (-x)^2 = x^2 và cos(-x) = cos x, nên f(-x) = x^2 + cos x = f(x) với mọi x.
    3. Tập R đối xứng qua 0, nên f là hàm chẵn.
- `gt_t1_tc_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào sau đây là hàm lẻ trên R?
    - **(đúng)** f(x) = x^3 + sin x
    - f(x) = x^2 + 1
    - f(x) = x^3 + 1
    - f(x) = cos x
  - **Đáp án:** f(x) = x^3 + sin x
    1. Hàm lẻ: f(-x) = -f(x) với mọi x.
    2. (-x)^3 + sin(-x) = -x^3 - sin x = -(x^3 + sin x): hàm lẻ.
    3. x^2 + 1 và cos x là hàm chẵn; x^3 + 1 không chẵn không lẻ vì số hạng 1 không đổi dấu.
- `gt_t1_tc_03` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số (xác định trên R) với tính chẵn lẻ của nó.
  - **Đáp án (ghép đúng):**
    - x^4 - x^2 — hàm chẵn
    - x^5 + x — hàm lẻ
    - x^2 + x — không chẵn cũng không lẻ
  - **Lời giải:**
    1. x^4 - x^2 chỉ có số mũ chẵn nên f(-x) = f(x): hàm chẵn.
    2. x^5 + x chỉ có số mũ lẻ nên f(-x) = -f(x): hàm lẻ.
    3. x^2 + x có cả số mũ chẵn lẫn lẻ: f(1) = 2 nhưng f(-1) = 0, khác cả 2 lẫn -2.
- `gt_g1_chan_le` · bậc 1 (Nhập môn) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm số f(x) = -x^5 - 4x, xác định trên R, là hàm lẻ.
  - **Đáp án:** Đúng
    1. Hàm x^k là hàm chẵn khi k chẵn và là hàm lẻ khi k lẻ, vì (-x)^k = x^k hoặc -x^k.
    2. Hai số mũ ở đây là 5 và 1.
    3. Cả hai số mũ cùng lẻ, nên f(-x) = -f(x) với mọi x: f là hàm lẻ.
  - **Câu hỏi:** Hàm số f(x) = x^5 - 3x, xác định trên R, là hàm lẻ.
  - **Đáp án:** Đúng
    1. Hàm x^k là hàm chẵn khi k chẵn và là hàm lẻ khi k lẻ, vì (-x)^k = x^k hoặc -x^k.
    2. Hai số mũ ở đây là 5 và 1.
    3. Cả hai số mũ cùng lẻ, nên f(-x) = -f(x) với mọi x: f là hàm lẻ.
  - **Câu hỏi:** Hàm số f(x) = x^5 + 5x, xác định trên R, là hàm lẻ.
  - **Đáp án:** Đúng
    1. Hàm x^k là hàm chẵn khi k chẵn và là hàm lẻ khi k lẻ, vì (-x)^k = x^k hoặc -x^k.
    2. Hai số mũ ở đây là 5 và 1.
    3. Cả hai số mũ cùng lẻ, nên f(-x) = -f(x) với mọi x: f là hàm lẻ.
- `gt_t1_tc_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f là hàm lẻ trên R và f(2) = 5. Tính f(-2) + f(0).
  - **Đáp án:** -5
    1. Hàm lẻ nên f(-2) = -f(2) = -5.
    2. Lấy x = 0: f(0) = -f(0), nên 2f(0) = 0 và f(0) = 0.
    3. f(-2) + f(0) = -5 + 0 = -5.
- `gt_t1_tc_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = sin x + cos x thỏa f(x + 2pi) = f(x) với mọi số thực x, nên là hàm tuần hoàn.
  - **Đáp án:** Đúng
    1. sin và cos đều có chu kỳ 2pi: sin(x + 2pi) = sin x và cos(x + 2pi) = cos x.
    2. Cộng lại: f(x + 2pi) = f(x) với mọi x.
    3. Có một số T = 2pi > 0 như vậy nên f tuần hoàn.
- `gt_t1_tc_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét tính chẵn lẻ của f(x) = x^3 - x + 1 trên R.
  - **Lời giải đưa ra (có một bước sai):**
    1. Tập xác định R đối xứng qua 0.
    2. f(-x) = (-x)^3 - (-x) + 1 = -x^3 + x + 1.
    3. -x^3 + x + 1 = -(x^3 - x + 1) = -f(x).   **<- bước sai đầu tiên**
    4. Vậy f là hàm lẻ.
  - **Đáp án:** Bước 3: -x^3 + x + 1 = -(x^3 - x + 1) = -f(x).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai khi bỏ ngoặc: -(x^3 - x + 1) = -x^3 + x - 1, không phải -x^3 + x + 1.
    2. Kiểm tra bằng số: f(2) = 7 còn f(-2) = -5, khác cả 7 lẫn -7.
    3. f không chẵn cũng không lẻ.
- `gt_t1_tc_07` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chu kỳ cơ sở (chu kỳ dương nhỏ nhất) của f(x) = sin x . cos x là bao nhiêu?
    - **(đúng)** pi
    - 2pi
    - pi/2
    - 4pi
  - **Đáp án:** pi
    1. Dùng công thức nhân đôi: sin x . cos x = sin(2x) / 2.
    2. sin(2x) có chu kỳ cơ sở 2pi / 2 = pi; chia cho 2 không đổi chu kỳ.
    3. Chu kỳ cơ sở là pi.
- `gt_t1_tc_08` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh f(x) = x^3 . sin x là hàm chẵn trên R.
  - **Đáp án (thứ tự đúng):**
    1. Thay -x vào chỗ x: f(-x) = (-x)^3 . sin(-x).
    2. Dùng (-x)^3 = -x^3 và sin(-x) = -sin x.
    3. Được f(-x) = (-x^3)(-sin x) = x^3 . sin x = f(x).
    4. Kết luận: f là hàm chẵn.
  - **Lời giải:**
    1. x^3 là hàm lẻ, sin x là hàm lẻ.
    2. Tích của hai hàm lẻ là hàm chẵn vì hai dấu trừ triệt tiêu nhau.
    3. Vậy f(-x) = f(x) với mọi x.
- `gt_g1_chu_ky` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Chu kỳ cơ sở (chu kỳ dương nhỏ nhất) của f(x) = sin(4x + 3) là T = k . pi. Tìm k.
  - **Đáp án:** 1/2
    1. Hàm sin x có chu kỳ cơ sở 2pi.
    2. Nhân x với 4 làm đồ thị co lại 4 lần; cộng hằng số chỉ dịch đồ thị, không đổi chu kỳ.
    3. T = 2pi / 4 = 1/2 . pi, nên k = 1/2.
  - **Câu hỏi:** Chu kỳ cơ sở (chu kỳ dương nhỏ nhất) của f(x) = sin(-5x - 3) là T = k . pi. Tìm k.
  - **Đáp án:** 2/5
    1. Hàm sin x có chu kỳ cơ sở 2pi.
    2. Nhân x với -5 làm đồ thị co lại 5 lần; cộng hằng số chỉ dịch đồ thị, không đổi chu kỳ.
    3. T = 2pi / 5 = 2/5 . pi, nên k = 2/5.
  - **Câu hỏi:** Chu kỳ cơ sở (chu kỳ dương nhỏ nhất) của f(x) = sin(4x + 1) là T = k . pi. Tìm k.
  - **Đáp án:** 1/2
    1. Hàm sin x có chu kỳ cơ sở 2pi.
    2. Nhân x với 4 làm đồ thị co lại 4 lần; cộng hằng số chỉ dịch đồ thị, không đổi chu kỳ.
    3. T = 2pi / 4 = 1/2 . pi, nên k = 1/2.

### Hàm hợp (`gt_t1_ham_hop`)

- `gt_t1_hh_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x + 1 và g(x) = 2x. Khi đó f(g(x)) = g(f(x)) với mọi số thực x.
  - **Đáp án:** Sai
    1. f(g(x)) = f(2x) = 2x + 1.
    2. g(f(x)) = g(x + 1) = 2x + 2.
    3. Hai biểu thức luôn lệch nhau 1, nên mệnh đề sai: thứ tự lấy hàm hợp quan trọng.
- `gt_t1_hh_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 và g(x) = x - 3. Biểu thức của f(g(x)) là gì?
    - **(đúng)** (x - 3)^2
    - x^2 - 3
    - x^2(x - 3)
    - x^2 - 9
  - **Đáp án:** (x - 3)^2
    1. f(g(x)) là f lấy tại g(x): bình phương cả biểu thức g(x).
    2. f(g(x)) = (g(x))^2 = (x - 3)^2.
    3. x^2 - 3 là g(f(x)), thứ tự ngược lại.
- `gt_t1_hh_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = sqrt(x) và g(x) = x^2 + 9. Tính f(g(4)).
  - **Đáp án:** 5
    1. Tính từ trong ra ngoài: g(4) = 16 + 9 = 25.
    2. f(g(4)) = f(25) = sqrt(25) = 5.
- `gt_t1_hh_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 2x và g(x) = x + 3. Ghép mỗi hàm hợp với biểu thức của nó.
  - **Đáp án (ghép đúng):**
    - f(g(x)) — 2x + 6
    - g(f(x)) — 2x + 3
    - f(f(x)) — 4x
    - g(g(x)) — x + 6
  - **Lời giải:**
    1. f(g(x)) = 2(x + 3) = 2x + 6.
    2. g(f(x)) = 2x + 3.
    3. f(f(x)) = 2 . 2x = 4x.
    4. g(g(x)) = (x + 3) + 3 = x + 6.
- `gt_g1_hop_gia_tri` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -2x + 3 và g(x) = x^2 - 4. Tính f(g(-1)).
  - **Đáp án:** 9
    1. Tính từ trong ra ngoài: g(-1) = (-1)^2 + (-4) = -3.
    2. f(g(-1)) = f(-3) = (-2) . (-3) + 3 = 9.
  - **Câu hỏi:** Cho f(x) = -4x - 5 và g(x) = x^2 - 4. Tính f(g(-1)).
  - **Đáp án:** 7
    1. Tính từ trong ra ngoài: g(-1) = (-1)^2 + (-4) = -3.
    2. f(g(-1)) = f(-3) = (-4) . (-3) + (-5) = 7.
  - **Câu hỏi:** Cho f(x) = -x + 3 và g(x) = x^2 + 3. Tính g(f(-2)).
  - **Đáp án:** 28
    1. Tính từ trong ra ngoài: f(-2) = (-1) . (-2) + 3 = 5.
    2. g(f(-2)) = g(5) = 5^2 + 3 = 28.
- `gt_t1_hh_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm h(x) = sin(x^2) viết được dưới dạng h(x) = f(g(x)) với cặp hàm nào?
    - **(đúng)** f(x) = sin x, g(x) = x^2
    - f(x) = x^2, g(x) = sin x
    - f(x) = sin x, g(x) = sin x
    - f(x) = x^2, g(x) = x^2
  - **Đáp án:** f(x) = sin x, g(x) = x^2
    1. Hàm trong là bước làm trước: bình phương x, nên g(x) = x^2.
    2. Hàm ngoài là bước làm sau: lấy sin, nên f(x) = sin x.
    3. Cặp f(x) = x^2, g(x) = sin x cho (sin x)^2, một hàm khác.
- `gt_t1_hh_06` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 3x - 1 và f(g(x)) = 6x + 5 với mọi số thực x. Tính g(2).
  - **Đáp án:** 6
    1. f(g(x)) = 3g(x) - 1, nên 3g(x) - 1 = 6x + 5.
    2. Giải ra g(x) = (6x + 6) / 3 = 2x + 2.
    3. g(2) = 2 . 2 + 2 = 6.
- `gt_t1_hh_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: cho f(x) = x^2 + 1 và g(x) = 2x - 3, tìm g(f(x)).
  - **Lời giải đưa ra (có một bước sai):**
    1. g(f(x)) nghĩa là thay f(x) vào chỗ của x trong g.
    2. g(f(x)) = 2(x^2 + 1) - 3.
    3. = 2x^2 + 1 - 3.   **<- bước sai đầu tiên**
    4. = 2x^2 - 2.
  - **Đáp án:** Bước 3: = 2x^2 + 1 - 3.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: nhân 2 vào ngoặc phải nhân cả số 1, 2(x^2 + 1) = 2x^2 + 2.
    2. Đúng là g(f(x)) = 2x^2 + 2 - 3 = 2x^2 - 1.
- `gt_t1_hh_08` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho h(x) = x + 1, g(x) = x^2 và f(x) = 3x - 2. Sắp xếp các bước tính f(g(h(1))).
  - **Đáp án (thứ tự đúng):**
    1. Tính hàm trong cùng: h(1) = 2.
    2. Tính tiếp g(h(1)) = g(2) = 4.
    3. Tính f(g(h(1))) = f(4) = 10.
    4. Kết quả là 10.
  - **Lời giải:**
    1. Hàm hợp được tính từ trong ra ngoài: h trước, rồi g, cuối cùng là f.
    2. h(1) = 2, g(2) = 4, f(4) = 3 . 4 - 2 = 10.
- `gt_t1_hh_09` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = sqrt(x) và g(x) = x - 4. Hàm hợp f(g(x)) xác định với mọi x >= 0.
  - **Đáp án:** Sai
    1. f(g(x)) = sqrt(x - 4) cần x - 4 >= 0, tức x >= 4.
    2. Chẳng hạn x = 1 >= 0 nhưng sqrt(1 - 4) = sqrt(-3) không có nghĩa.
    3. Tập xác định của hàm hợp là [4, +vô cùng), không phải [0, +vô cùng).
- `gt_g1_hop_he_so` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -3x + 3 và g(x) = -4x - 2. Hàm hợp f(g(x)) có dạng px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 12, 9
    1. f(g(x)) nghĩa là thay cả biểu thức g(x) vào chỗ của x trong f.
    2. f(g(x)) = (-3) . (-4x - 2) + 3.
    3. Nhân phân phối: 12x + 6 + 3 = 12x + 9.
    4. Vậy p = 12, q = 9.
  - **Câu hỏi:** Cho f(x) = -5x - 5 và g(x) = -4x - 1. Hàm hợp f(g(x)) có dạng px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 20, 0
    1. f(g(x)) nghĩa là thay cả biểu thức g(x) vào chỗ của x trong f.
    2. f(g(x)) = (-5) . (-4x - 1) + (-5).
    3. Nhân phân phối: 20x + 5 + (-5) = 20x.
    4. Vậy p = 20, q = 0.
  - **Câu hỏi:** Cho f(x) = -2x + 3 và g(x) = 4x - 4. Hàm hợp f(g(x)) có dạng px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -8, 11
    1. f(g(x)) nghĩa là thay cả biểu thức g(x) vào chỗ của x trong f.
    2. f(g(x)) = (-2) . (4x - 4) + 3.
    3. Nhân phân phối: -8x + 8 + 3 = -8x + 11.
    4. Vậy p = -8, q = 11.

### Hàm ngược (`gt_t1_ham_nguoc`)

- `gt_t1_hn_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f: R -> R, f(x) = x^2 có hàm ngược.
  - **Đáp án:** Sai
    1. Muốn có hàm ngược, mỗi giá trị chỉ được là ảnh của đúng một x (f phải là song ánh).
    2. f(2) = f(-2) = 4: giá trị 4 ứng với hai số khác nhau.
    3. Ngoài ra số âm như -1 không là ảnh của số nào. f không có hàm ngược trên R.
- `gt_t1_hn_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm ngược của f: R -> R, f(x) = x^3 là hàm nào?
    - **(đúng)** f^(-1)(x) = căn bậc ba của x
    - f^(-1)(x) = 1 / x^3
    - f^(-1)(x) = -x^3
    - f^(-1)(x) = x^3 / 3
  - **Đáp án:** f^(-1)(x) = căn bậc ba của x
    1. Đặt y = x^3 rồi giải theo x: x là căn bậc ba của y.
    2. Đổi tên biến: f^(-1)(x) là căn bậc ba của x.
    3. Chú ý f^(-1) là hàm ngược, không phải 1/f.
- `gt_t1_hn_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f có hàm ngược và f(2) = 7. Tính f^(-1)(7).
  - **Đáp án:** 2
    1. f^(-1)(7) là số x sao cho f(x) = 7.
    2. Đề cho f(2) = 7, và f có hàm ngược nên số đó là duy nhất.
    3. f^(-1)(7) = 2.
- `gt_t1_hn_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với hàm ngược của nó.
  - **Đáp án (ghép đúng):**
    - x + 5 — x - 5
    - 2x — x/2
    - e^x — ln x
    - x^3 — căn bậc ba của x
  - **Lời giải:**
    1. Hàm ngược làm ngược lại việc hàm đã làm.
    2. Cộng 5 thì ngược lại là trừ 5; nhân 2 thì ngược lại là chia 2.
    3. Lấy e mũ thì ngược lại là lấy ln; lập phương thì ngược lại là lấy căn bậc ba.
- `gt_g1_nguoc_bac_nhat` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = -4x + 9 có hàm ngược f^(-1)(x) = px + q. Nhập p, q theo đúng thứ tự (phân số viết a/b).
  - **Đáp án:** -1/4, 9/4
    1. Đặt y = -4x + 9 rồi giải theo x.
    2. -4x = y - 9, nên x = (y - 9) / (-4).
    3. Đổi tên biến: f^(-1)(x) = -(1/4)x + 9/4.
    4. Vậy p = -1/4, q = 9/4.
  - **Câu hỏi:** Hàm f(x) = -6x - 7 có hàm ngược f^(-1)(x) = px + q. Nhập p, q theo đúng thứ tự (phân số viết a/b).
  - **Đáp án:** -1/6, -7/6
    1. Đặt y = -6x - 7 rồi giải theo x.
    2. -6x = y - (-7), nên x = (y - (-7)) / (-6).
    3. Đổi tên biến: f^(-1)(x) = -(1/6)x - 7/6.
    4. Vậy p = -1/6, q = -7/6.
  - **Câu hỏi:** Hàm f(x) = -3x + 9 có hàm ngược f^(-1)(x) = px + q. Nhập p, q theo đúng thứ tự (phân số viết a/b).
  - **Đáp án:** -1/3, 3
    1. Đặt y = -3x + 9 rồi giải theo x.
    2. -3x = y - 9, nên x = (y - 9) / (-3).
    3. Đổi tên biến: f^(-1)(x) = -(1/3)x + 3.
    4. Vậy p = -1/3, q = 3.
- `gt_t1_hn_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 2x + 3. Tính f^(-1)(f^(-1)(13)).
  - **Đáp án:** 1
    1. Giải y = 2x + 3 theo x: f^(-1)(y) = (y - 3) / 2.
    2. f^(-1)(13) = (13 - 3) / 2 = 5.
    3. f^(-1)(5) = (5 - 3) / 2 = 1.
- `gt_t1_hn_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f có hàm ngược, đồ thị của y = f(x) và đồ thị của y = f^(-1)(x) đối xứng nhau qua đường thẳng y = x.
  - **Đáp án:** Đúng
    1. Điểm (a, b) nằm trên đồ thị của f khi b = f(a), tức a = f^(-1)(b).
    2. Khi đó điểm (b, a) nằm trên đồ thị của f^(-1).
    3. Đổi chỗ hai tọa độ chính là lấy đối xứng qua đường y = x.
- `gt_t1_hn_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm hàm ngược của f(x) = (x + 1) / (x - 2), x khác 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt y = (x + 1) / (x - 2).
    2. Nhân chéo: y(x - 2) = x + 1.
    3. Khai triển: xy - 2y = x + 1.
    4. Chuyển vế: xy - x = 2y + 1, tức x(y - 1) = 2y + 1.
    5. Suy ra x = (2y + 1) / (y + 1).   **<- bước sai đầu tiên**
    6. Vậy f^(-1)(x) = (2x + 1) / (x + 1).
  - **Đáp án:** Bước 5: Suy ra x = (2y + 1) / (y + 1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 5 sai: chia hai vế cho (y - 1) chứ không phải (y + 1).
    2. Đúng là x = (2y + 1) / (y - 1), nên f^(-1)(x) = (2x + 1) / (x - 1).
    3. Kiểm tra: f(3) = 4 và (2 . 4 + 1) / (4 - 1) = 3.
- `gt_t1_hn_08` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét f(x) = x^2 chỉ trên [0, +vô cùng). Hàm ngược của nó là hàm nào?
    - **(đúng)** sqrt(x)
    - -sqrt(x)
    - 1 / x^2
    - x / 2
  - **Đáp án:** sqrt(x)
    1. Trên [0, +vô cùng), x^2 tăng ngặt nên có hàm ngược.
    2. Giải y = x^2 với x >= 0: chỉ lấy nghiệm không âm x = sqrt(y).
    3. f^(-1)(x) = sqrt(x).
- `gt_t1_hn_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm hàm ngược của f(x) = 3x - 6.
  - **Đáp án (thứ tự đúng):**
    1. Đặt y = 3x - 6.
    2. Chuyển vế: 3x = y + 6.
    3. Chia hai vế cho 3: x = (y + 6) / 3.
    4. Đổi tên biến: f^(-1)(x) = (x + 6) / 3.
  - **Lời giải:**
    1. Cách làm chung: viết y = f(x), giải theo x, rồi đổi tên y thành x.
    2. Ở đây được f^(-1)(x) = (x + 6) / 3.
    3. Kiểm tra: f(2) = 0 và f^(-1)(0) = 2.
- `gt_g1_nguoc_phan_thuc` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (-3x + 3) / (-3x - 1) có hàm ngược. Tính f^(-1)(-5).
  - **Đáp án:** -1/9
    1. f^(-1)(-5) là số x sao cho f(x) = -5.
    2. Giải (-3x + 3) / (-3x - 1) = -5: nhân chéo được -3x + 3 = (-5) . (-3x - 1).
    3. Chuyển các số hạng chứa x sang một vế: -18x = 2.
    4. x = -1/9, và mẫu -3x - 1 khác 0 tại đó, nên f^(-1)(-5) = -1/9.
  - **Câu hỏi:** Hàm f(x) = (-5x - 5) / (-3x) có hàm ngược. Tính f^(-1)(-4).
  - **Đáp án:** -5/17
    1. f^(-1)(-4) là số x sao cho f(x) = -4.
    2. Giải (-5x - 5) / (-3x) = -4: nhân chéo được -5x - 5 = (-4) . (-3x).
    3. Chuyển các số hạng chứa x sang một vế: -17x = 5.
    4. x = -5/17, và mẫu -3x khác 0 tại đó, nên f^(-1)(-4) = -5/17.
  - **Câu hỏi:** Hàm f(x) = (4x + 1) / (3x + 4) có hàm ngược. Tính f^(-1)(-5).
  - **Đáp án:** -21/19
    1. f^(-1)(-5) là số x sao cho f(x) = -5.
    2. Giải (4x + 1) / (3x + 4) = -5: nhân chéo được 4x + 1 = (-5) . (3x + 4).
    3. Chuyển các số hạng chứa x sang một vế: 19x = -21.
    4. x = -21/19, và mẫu 3x + 4 khác 0 tại đó, nên f^(-1)(-5) = -21/19.

### Các hàm sơ cấp cơ bản (`gt_t1_ham_so_cap`)

- `gt_t1_sc_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** ln(e^3) = 3.
  - **Đáp án:** Đúng
    1. ln là hàm ngược của e^x, nên ln(e^t) = t với mọi số thực t.
    2. Lấy t = 3: ln(e^3) = 3.
- `gt_t1_sc_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập giá trị của hàm y = e^x (x chạy trên R) là tập nào?
    - **(đúng)** (0, +vô cùng)
    - R
    - [0, +vô cùng)
    - (1, +vô cùng)
  - **Đáp án:** (0, +vô cùng)
    1. e^x luôn dương với mọi x, và không bao giờ bằng 0.
    2. Khi x -> -vô cùng thì e^x -> 0, khi x -> +vô cùng thì e^x -> +vô cùng.
    3. Mọi số dương đều đạt được (bằng e^(ln y)), nên tập giá trị là (0, +vô cùng).
- `gt_t1_sc_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** arcsin(1/2) = k . pi. Tìm k.
  - **Đáp án:** 1/6
    1. arcsin(1/2) là góc trong [-pi/2, pi/2] có sin bằng 1/2.
    2. sin(pi/6) = 1/2 và pi/6 nằm trong khoảng đó.
    3. arcsin(1/2) = pi/6, nên k = 1/6.
- `gt_t1_sc_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi giá trị lượng giác ngược với kết quả của nó.
  - **Đáp án (ghép đúng):**
    - arcsin(1) — pi/2
    - arccos(1) — 0
    - arctan(1) — pi/4
    - arccos(-1) — pi
  - **Lời giải:**
    1. arcsin cho góc trong [-pi/2, pi/2]: sin(pi/2) = 1.
    2. arccos cho góc trong [0, pi]: cos(0) = 1 và cos(pi) = -1.
    3. arctan cho góc trong (-pi/2, pi/2): tan(pi/4) = 1.
- `gt_t1_sc_10` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm y = ln x xác định với mọi số thực x.
  - **Đáp án:** Sai
    1. ln x chỉ có nghĩa khi x > 0.
    2. Chẳng hạn ln(0) và ln(-1) không có nghĩa trong tập số thực.
    3. Tập xác định của ln x là (0, +vô cùng).
- `gt_g1_logarit` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính log_3(9).
  - **Đáp án:** 2
    1. log_3(N) là số mũ phải đặt lên 3 để được N.
    2. 9 = 3^2.
    3. Vậy log_3(9) = 2.
  - **Câu hỏi:** Tính log_2(1/8).
  - **Đáp án:** -3
    1. log_2(N) là số mũ phải đặt lên 2 để được N.
    2. 1/8 = 1 / 2^3 = 2^(-3).
    3. Vậy log_2(1/8) = -3.
  - **Câu hỏi:** Tính log_3(9).
  - **Đáp án:** 2
    1. log_3(N) là số mũ phải đặt lên 3 để được N.
    2. 9 = 3^2.
    3. Vậy log_3(9) = 2.
- `gt_t1_sc_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính log_2(12) - log_2(3).
  - **Đáp án:** 2
    1. Hiệu hai lôgarit cùng cơ số là lôgarit của thương: log_2(12) - log_2(3) = log_2(12/3).
    2. 12/3 = 4 = 2^2.
    3. Kết quả là 2.
- `gt_t1_sc_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số thực x, arcsin(sin x) = x.
  - **Đáp án:** Sai
    1. arcsin luôn cho kết quả trong [-pi/2, pi/2].
    2. Lấy x = pi: sin(pi) = 0 và arcsin(0) = 0, khác pi.
    3. Đẳng thức chỉ đúng khi x thuộc [-pi/2, pi/2].
- `gt_t1_sc_07` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập xác định của y = arccos(x - 1) là tập nào?
    - **(đúng)** [0, 2]
    - [-1, 1]
    - [-2, 0]
    - (0, 2)
  - **Đáp án:** [0, 2]
    1. arccos(u) chỉ có nghĩa khi -1 <= u <= 1.
    2. Với u = x - 1: -1 <= x - 1 <= 1, tức 0 <= x <= 2.
    3. Tập xác định là [0, 2].
- `gt_t1_sc_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: giải phương trình ln x + ln(x - 1) = ln 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. Điều kiện: x > 0 và x - 1 > 0, tức x > 1.
    2. Dùng ln a + ln b = ln(ab): ln(x(x - 1)) = ln 2.
    3. Suy ra x(x - 1) = 2, tức x^2 - x - 2 = 0.
    4. Phương trình bậc hai có hai nghiệm x = 2 và x = -1.
    5. Cả hai nghiệm đều nhận.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 5: Cả hai nghiệm đều nhận.
  - **Vì sao sai, và bước đúng:**
    1. Bước 5 sai: phải đối chiếu với điều kiện x > 1 ở bước 1.
    2. x = -1 không thỏa x > 1 (ln(-1) không có nghĩa), nên bị loại.
    3. Phương trình chỉ có một nghiệm x = 2.
- `gt_t1_sc_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước giải phương trình 2^(x + 1) = 32.
  - **Đáp án (thứ tự đúng):**
    1. Viết 32 dưới dạng lũy thừa của 2: 32 = 2^5.
    2. Phương trình thành 2^(x + 1) = 2^5.
    3. Hàm 2^t tăng ngặt nên hai số mũ bằng nhau: x + 1 = 5.
    4. Vậy x = 4.
  - **Lời giải:**
    1. Đưa hai vế về cùng cơ số 2.
    2. Hàm mũ là đơn ánh nên được so số mũ: x + 1 = 5.
    3. Nghiệm x = 4; kiểm tra 2^5 = 32.
- `gt_g1_pt_logarit` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải phương trình log_2(x - 2) = 0.
  - **Đáp án:** 3
    1. Điều kiện: x - 2 > 0.
    2. log_2(A) = 0 nghĩa là A = 2^0 = 1.
    3. x - 2 = 1, nên x = 3.
    4. Kiểm tra điều kiện: x - 2 = 1 > 0, thỏa. Nghiệm x = 3.
  - **Câu hỏi:** Giải phương trình log_2(x - 5) = 0.
  - **Đáp án:** 6
    1. Điều kiện: x - 5 > 0.
    2. log_2(A) = 0 nghĩa là A = 2^0 = 1.
    3. x - 5 = 1, nên x = 6.
    4. Kiểm tra điều kiện: x - 5 = 1 > 0, thỏa. Nghiệm x = 6.
  - **Câu hỏi:** Giải phương trình log_2(x - 1) = 1.
  - **Đáp án:** 3
    1. Điều kiện: x - 1 > 0.
    2. log_2(A) = 1 nghĩa là A = 2^1 = 2.
    3. x - 1 = 2, nên x = 3.
    4. Kiểm tra điều kiện: x - 1 = 2 > 0, thỏa. Nghiệm x = 3.

## Tầng 2: Dãy số, giới hạn, vô cùng bé và vô cùng lớn

55 dạng câu (45 câu viết tay, 10 bộ sinh câu); 55 chưa duyệt.

### Giới hạn của dãy số (`gt_t2_gioi_han_day`)

- `gt_t2_ds_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy u_n = 1/n dần tới 0 khi n -> +vô cùng.
  - **Đáp án:** Đúng
    1. Với mọi số dương e nhỏ tùy ý, chỉ cần n > 1/e là 1/n < e.
    2. Vậy 1/n nhỏ hơn mọi số dương khi n đủ lớn: giới hạn bằng 0.
- `gt_t2_ds_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của dãy u_n = (1/2)^n khi n -> +vô cùng là gì?
    - **(đúng)** 0
    - 1/2
    - 1
    - +vô cùng
  - **Đáp án:** 0
    1. Với |q| < 1 thì q^n -> 0.
    2. Ở đây q = 1/2: các số hạng 1/2, 1/4, 1/8, ... nhỏ dần về 0.
    3. Giới hạn bằng 0.
- `gt_t2_ds_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của dãy u_n = 3 + 2/n khi n -> +vô cùng.
  - **Đáp án:** 3
    1. 2/n -> 0 khi n -> +vô cùng.
    2. Giới hạn của tổng bằng tổng các giới hạn: 3 + 0 = 3.
- `gt_t2_ds_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dãy số với hành vi của nó khi n -> +vô cùng.
  - **Đáp án (ghép đúng):**
    - 1/n^2 — dần tới 0
    - (n + 1)/n — dần tới 1
    - 2^n — dần tới +vô cùng
    - (-1)^n — không có giới hạn
  - **Lời giải:**
    1. 1/n^2 nhỏ dần về 0.
    2. (n + 1)/n = 1 + 1/n dần tới 1.
    3. 2^n tăng không bị chặn.
    4. (-1)^n nhảy qua lại giữa -1 và 1, không dần tới số nào.
- `gt_g2_day_huu_ty` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (4n - 4) / (3n) khi n -> +vô cùng.
  - **Đáp án:** 4/3
    1. Chia cả tử và mẫu cho n.
    2. Mọi số hạng có dạng (hằng số) / n^k với k >= 1 đều dần tới 0 khi n -> +vô cùng.
    3. Chỉ còn lại tỉ số hai hệ số của lũy thừa cao nhất: 4 / 3 = 4/3.
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (-5n - 4) / (3n + 1) khi n -> +vô cùng.
  - **Đáp án:** -5/3
    1. Chia cả tử và mẫu cho n.
    2. Mọi số hạng có dạng (hằng số) / n^k với k >= 1 đều dần tới 0 khi n -> +vô cùng.
    3. Chỉ còn lại tỉ số hai hệ số của lũy thừa cao nhất: -5 / 3 = -5/3.
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (4n + 3) / (2n + 2) khi n -> +vô cùng.
  - **Đáp án:** 2
    1. Chia cả tử và mẫu cho n.
    2. Mọi số hạng có dạng (hằng số) / n^k với k >= 1 đều dần tới 0 khi n -> +vô cùng.
    3. Chỉ còn lại tỉ số hai hệ số của lũy thừa cao nhất: 4 / 2 = 2.
- `gt_t2_ds_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của dãy u_n = sqrt(n^2 + 4n) - n khi n -> +vô cùng.
  - **Đáp án:** 2
    1. Nhân và chia cho biểu thức liên hợp sqrt(n^2 + 4n) + n.
    2. u_n = 4n / (sqrt(n^2 + 4n) + n).
    3. Chia tử và mẫu cho n: u_n = 4 / (sqrt(1 + 4/n) + 1) -> 4 / 2 = 2.
- `gt_t2_ds_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy u_n = (-1)^n / n có giới hạn bằng 0 khi n -> +vô cùng.
  - **Đáp án:** Đúng
    1. |u_n| = 1/n với mọi n.
    2. 1/n -> 0, nên |u_n| -> 0.
    3. Một dãy có |u_n| -> 0 thì u_n -> 0, dù dấu đổi liên tục.
- `gt_t2_ds_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của u_n = (2n^2 + n) / (n^3 + 1) khi n -> +vô cùng.
  - **Lời giải đưa ra (có một bước sai):**
    1. Chia cả tử và mẫu cho n^2.
    2. Tử thành 2 + 1/n, dần tới 2.
    3. Mẫu thành n + 1/n^2, dần tới 1.   **<- bước sai đầu tiên**
    4. Giới hạn bằng 2 / 1 = 2.
  - **Đáp án:** Bước 3: Mẫu thành n + 1/n^2, dần tới 1.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: n + 1/n^2 dần tới +vô cùng chứ không tới 1.
    2. Tử dần tới 2, mẫu dần tới +vô cùng, nên thương dần tới 0.
    3. Cách gọn hơn: bậc tử là 2, nhỏ hơn bậc mẫu là 3, nên giới hạn bằng 0.
- `gt_t2_ds_08` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy nào sau đây hội tụ (có giới hạn hữu hạn) khi n -> +vô cùng?
    - **(đúng)** u_n = n / (n + 1)
    - u_n = (-1)^n
    - u_n = n^2
    - u_n = sin(n . pi / 2)
  - **Đáp án:** u_n = n / (n + 1)
    1. n / (n + 1) = 1 / (1 + 1/n) -> 1: hội tụ.
    2. (-1)^n nhảy giữa -1 và 1; n^2 -> +vô cùng.
    3. sin(n . pi / 2) lặp lại 1, 0, -1, 0: không có giới hạn.
- `gt_t2_ds_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của u_n = (3n + 1) / (n - 2) khi n -> +vô cùng.
  - **Đáp án (thứ tự đúng):**
    1. Chia cả tử và mẫu cho n.
    2. Được u_n = (3 + 1/n) / (1 - 2/n).
    3. Khi n -> +vô cùng, 1/n -> 0 và 2/n -> 0.
    4. Giới hạn bằng 3 / 1 = 3.
  - **Lời giải:**
    1. Chia cho lũy thừa cao nhất của n ở mẫu để mọi số hạng còn lại hoặc là hằng số, hoặc dần tới 0.
    2. Kết quả là tỉ số hai hệ số của n: 3 / 1 = 3.
- `gt_g2_day_mu` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (-3^n + 3 . 2^n) / (3^n + 3 . 2^n) khi n -> +vô cùng.
  - **Đáp án:** -1
    1. Lũy thừa lớn nhất là 3^n: chia cả tử và mẫu cho 3^n.
    2. Còn lại (-1 + 3 . (2/3)^n) / (1 + 3 . (2/3)^n).
    3. Vì 0 < 2/3 < 1 nên (2/3)^n -> 0.
    4. Giới hạn bằng -1 / 1 = -1.
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (-4 . 6^n - 3 . 2^n) / (3 . 6^n - 2^n) khi n -> +vô cùng.
  - **Đáp án:** -4/3
    1. Lũy thừa lớn nhất là 6^n: chia cả tử và mẫu cho 6^n.
    2. Còn lại (-4 - 3 . (2/6)^n) / (3 - 1 . (2/6)^n).
    3. Vì 0 < 2/6 < 1 nên (2/6)^n -> 0.
    4. Giới hạn bằng -4 / 3 = -4/3.
  - **Câu hỏi:** Tính giới hạn của dãy u_n = (6^n + 3 . 3^n) / (5 . 6^n + 5 . 3^n) khi n -> +vô cùng.
  - **Đáp án:** 1/5
    1. Lũy thừa lớn nhất là 6^n: chia cả tử và mẫu cho 6^n.
    2. Còn lại (1 + 3 . (3/6)^n) / (5 + 5 . (3/6)^n).
    3. Vì 0 < 3/6 < 1 nên (3/6)^n -> 0.
    4. Giới hạn bằng 1 / 5 = 1/5.

### Giới hạn hàm số tại một điểm (`gt_t2_gioi_han_ham`)

- `gt_t2_gh_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của x^2 + 1 khi x -> 2 bằng 5.
  - **Đáp án:** Đúng
    1. Đa thức liên tục tại mọi điểm, nên chỉ cần thay số.
    2. 2^2 + 1 = 5.
- `gt_t2_gh_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thay x = 3 vào (x^2 - 9) / (x - 3) thì được dạng nào?
    - **(đúng)** 0/0
    - vô cùng / vô cùng
    - một số thực khác 0
    - 1 mũ vô cùng
  - **Đáp án:** 0/0
    1. Tử: 3^2 - 9 = 0. Mẫu: 3 - 3 = 0.
    2. Được dạng 0/0, một dạng vô định: chưa kết luận được, phải biến đổi tiếp.
- `gt_t2_gh_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (x^2 - 9) / (x - 3) khi x -> 3.
  - **Đáp án:** 6
    1. Dạng 0/0: phân tích tử x^2 - 9 = (x - 3)(x + 3).
    2. Với x khác 3, rút gọn được x + 3.
    3. Thay x = 3: 3 + 3 = 6.
- `gt_t2_gh_04` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi giới hạn với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - (x^2 - 1)/(x - 1) khi x -> 1 — 2
    - (x^2 + 3x)/x khi x -> 0 — 3
    - (x^3 - 8)/(x - 2) khi x -> 2 — 12
    - 2x + 4 khi x -> 0 — 4
  - **Lời giải:**
    1. (x^2 - 1)/(x - 1) = x + 1 -> 2.
    2. (x^2 + 3x)/x = x + 3 -> 3.
    3. (x^3 - 8)/(x - 2) = x^2 + 2x + 4 -> 4 + 4 + 4 = 12.
    4. 2x + 4 là đa thức: thay x = 0 được 4.
- `gt_g2_thay_so` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (-2x^2 - 6) / (x - 5) khi x -> 4.
  - **Đáp án:** 38
    1. Tại x = 4 mẫu bằng 1 . 4 + (-5) = -1, khác 0.
    2. Hàm phân thức liên tục tại mọi điểm mẫu khác 0, nên chỉ cần thay số.
    3. Tử bằng (-2) . 4^2 + (-6) = -38.
    4. Giới hạn = -38 / (-1) = 38.
  - **Câu hỏi:** Tính giới hạn của (-4x^2 - 6) / (-3x - 1) khi x -> -1.
  - **Đáp án:** -5
    1. Tại x = -1 mẫu bằng (-3) . (-1) + (-1) = 2, khác 0.
    2. Hàm phân thức liên tục tại mọi điểm mẫu khác 0, nên chỉ cần thay số.
    3. Tử bằng (-4) . (-1)^2 + (-6) = -10.
    4. Giới hạn = -10 / 2 = -5.
  - **Câu hỏi:** Tính giới hạn của (-x^2 - 4) / (2x + 3) khi x -> 4.
  - **Đáp án:** -20/11
    1. Tại x = 4 mẫu bằng 2 . 4 + 3 = 11, khác 0.
    2. Hàm phân thức liên tục tại mọi điểm mẫu khác 0, nên chỉ cần thay số.
    3. Tử bằng (-1) . 4^2 + (-4) = -20.
    4. Giới hạn = -20 / 11 = -20/11.
- `gt_t2_gh_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (sqrt(x + 4) - 2) / x khi x -> 0.
  - **Đáp án:** 1/4
    1. Dạng 0/0 có căn: nhân tử và mẫu với liên hợp sqrt(x + 4) + 2.
    2. Tử thành (x + 4) - 4 = x, nên biểu thức bằng 1 / (sqrt(x + 4) + 2) với x khác 0.
    3. Thay x = 0: 1 / (2 + 2) = 1/4.
- `gt_t2_gh_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f xác định quanh a và mọi số L: nếu giới hạn của f(x) khi x -> a bằng L thì f(a) = L.
  - **Đáp án:** Sai
    1. Giới hạn chỉ nói về các giá trị f(x) khi x gần a, x khác a; nó không nhìn f(a).
    2. Ví dụ f(x) = x khi x khác 0 và f(0) = 5: giới hạn tại 0 bằng 0 nhưng f(0) = 5.
    3. Khi f(a) bằng giới hạn, ta nói f liên tục tại a, đó là điều kiện thêm.
- `gt_t2_gh_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (x^2 - 4) / (x^2 - 3x + 2) khi x -> 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. Thay x = 2: tử và mẫu đều bằng 0, dạng 0/0.
    2. Phân tích tử: x^2 - 4 = (x - 2)(x + 2).
    3. Phân tích mẫu: x^2 - 3x + 2 = (x - 2)(x + 1).   **<- bước sai đầu tiên**
    4. Rút gọn: (x + 2) / (x + 1).
    5. Thay x = 2 được 4/3.
  - **Đáp án:** Bước 3: Phân tích mẫu: x^2 - 3x + 2 = (x - 2)(x + 1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: (x - 2)(x + 1) = x^2 - x - 2. Đúng là x^2 - 3x + 2 = (x - 2)(x - 1).
    2. Rút gọn đúng: (x + 2) / (x - 1).
    3. Thay x = 2: 4 / 1 = 4.
- `gt_t2_gh_08` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (x - 1) / (sqrt(x) - 1) khi x -> 1 bằng bao nhiêu?
    - **(đúng)** 2
    - 1
    - 0
    - 1/2
  - **Đáp án:** 2
    1. Viết x - 1 = (sqrt(x) - 1)(sqrt(x) + 1) với x >= 0.
    2. Rút gọn: biểu thức bằng sqrt(x) + 1 khi x khác 1.
    3. Thay x = 1: 1 + 1 = 2.
- `gt_t2_gh_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của (sqrt(x) - 3) / (x - 9) khi x -> 9.
  - **Đáp án (thứ tự đúng):**
    1. Thay x = 9 được dạng 0/0.
    2. Viết mẫu x - 9 = (sqrt(x) - 3)(sqrt(x) + 3).
    3. Rút gọn được 1 / (sqrt(x) + 3) với x khác 9.
    4. Thay x = 9: 1 / (3 + 3) = 1/6.
  - **Lời giải:**
    1. Khi gặp 0/0, tìm thừa số chung của tử và mẫu.
    2. x - 9 là hiệu hai bình phương của sqrt(x) và 3.
    3. Sau khi rút gọn, hàm liên tục tại 9 nên thay số: 1/6.
- `gt_g2_khu_00` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (x^2 - x - 12) / (x^2 + 7x + 12) khi x -> -3.
  - **Đáp án:** -7
    1. Thay x = -3: tử và mẫu đều bằng 0, dạng 0/0, chưa kết luận được.
    2. Cả tử và mẫu đều có nghiệm x = -3, nên đều chia hết cho (x + 3): tử = (x + 3)(x - 4), mẫu = (x + 3)(x + 4).
    3. Với x khác -3, rút gọn được (x - 4) / (x + 4).
    4. Thay x = -3: (-7) / (1) = -7.
  - **Câu hỏi:** Tính giới hạn của (x^2 + 9x + 20) / (x^2 + x - 20) khi x -> -5.
  - **Đáp án:** 1/9
    1. Thay x = -5: tử và mẫu đều bằng 0, dạng 0/0, chưa kết luận được.
    2. Cả tử và mẫu đều có nghiệm x = -5, nên đều chia hết cho (x + 5): tử = (x + 5)(x + 4), mẫu = (x + 5)(x - 4).
    3. Với x khác -5, rút gọn được (x + 4) / (x - 4).
    4. Thay x = -5: (-1) / (-9) = 1/9.
  - **Câu hỏi:** Tính giới hạn của (x^2 - 2x - 8) / (x^2 - x - 6) khi x -> -2.
  - **Đáp án:** 6/5
    1. Thay x = -2: tử và mẫu đều bằng 0, dạng 0/0, chưa kết luận được.
    2. Cả tử và mẫu đều có nghiệm x = -2, nên đều chia hết cho (x + 2): tử = (x + 2)(x - 4), mẫu = (x + 2)(x - 3).
    3. Với x khác -2, rút gọn được (x - 4) / (x - 3).
    4. Thay x = -2: (-6) / (-5) = 6/5.

### Giới hạn ở vô cùng và giới hạn vô cùng (`gt_t2_gioi_han_vo_cuc`)

- `gt_t2_vc_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của 1/x^2 khi x -> 0 bằng +vô cùng.
  - **Đáp án:** Đúng
    1. Khi x -> 0 (từ cả hai phía), x^2 dương và dần tới 0.
    2. 1 chia cho một số dương rất nhỏ thì rất lớn.
    3. Vậy 1/x^2 -> +vô cùng.
- `gt_t2_vc_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (2x^3 + 1) / (x^2 - 5) khi x -> +vô cùng là gì?
    - **(đúng)** +vô cùng
    - 2
    - 0
    - -vô cùng
  - **Đáp án:** +vô cùng
    1. Bậc tử là 3, lớn hơn bậc mẫu là 2.
    2. Chia tử và mẫu cho x^2: (2x + 1/x^2) / (1 - 5/x^2), tử -> +vô cùng, mẫu -> 1.
    3. Giới hạn là +vô cùng (hệ số cao nhất 2 dương).
- `gt_t2_vc_03` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với một phân thức P(x)/Q(x) khi x -> +vô cùng, ghép mỗi trường hợp với kết quả.
  - **Đáp án (ghép đúng):**
    - Bậc của P nhỏ hơn bậc của Q — giới hạn bằng 0
    - Bậc của P bằng bậc của Q — giới hạn bằng tỉ số hai hệ số cao nhất
    - Bậc của P lớn hơn bậc của Q — giới hạn là vô cùng
  - **Lời giải:**
    1. Chia tử và mẫu cho lũy thừa cao nhất của mẫu.
    2. Bậc tử nhỏ hơn: tử dần tới 0, mẫu dần tới một số khác 0.
    3. Bậc bằng nhau: chỉ còn hai hệ số cao nhất. Bậc tử lớn hơn: tử dần ra vô cùng.
- `gt_t2_vc_04` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (5 - 3x) / (2x + 1) khi x -> +vô cùng.
  - **Đáp án:** -3/2
    1. Chia tử và mẫu cho x: (5/x - 3) / (2 + 1/x).
    2. 5/x và 1/x dần tới 0.
    3. Giới hạn bằng -3 / 2.
- `gt_g2_vo_cuc_huu_ty` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (-3x^2 - 5x + 1) / (3x^2 + x + 4) khi x -> -vô cùng.
  - **Đáp án:** -1
    1. Chia cả tử và mẫu cho x^2, lũy thừa cao nhất của mẫu.
    2. Mọi số hạng dạng (hằng số) / x^k với k >= 1 dần tới 0 khi x -> -vô cùng.
    3. Bậc của tử bằng bậc của mẫu: giới hạn là tỉ số hai hệ số cao nhất -3 / 3 = -1.
  - **Câu hỏi:** Tính giới hạn của (-6x^2 - x - 4) / (-x^2 - 2x + 3) khi x -> +vô cùng.
  - **Đáp án:** 6
    1. Chia cả tử và mẫu cho x^2, lũy thừa cao nhất của mẫu.
    2. Mọi số hạng dạng (hằng số) / x^k với k >= 1 dần tới 0 khi x -> +vô cùng.
    3. Bậc của tử bằng bậc của mẫu: giới hạn là tỉ số hai hệ số cao nhất -6 / (-1) = 6.
  - **Câu hỏi:** Tính giới hạn của (-2x^2 + 3x + 1) / (5x^2 - 5x + 3) khi x -> +vô cùng.
  - **Đáp án:** -2/5
    1. Chia cả tử và mẫu cho x^2, lũy thừa cao nhất của mẫu.
    2. Mọi số hạng dạng (hằng số) / x^k với k >= 1 dần tới 0 khi x -> +vô cùng.
    3. Bậc của tử bằng bậc của mẫu: giới hạn là tỉ số hai hệ số cao nhất -2 / 5 = -2/5.
- `gt_t2_vc_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của 1/(x - 1) khi x -> 1 bằng +vô cùng.
  - **Đáp án:** Sai
    1. Khi x -> 1 từ bên phải, x - 1 > 0 nên 1/(x - 1) -> +vô cùng.
    2. Khi x -> 1 từ bên trái, x - 1 < 0 nên 1/(x - 1) -> -vô cùng.
    3. Hai phía khác nhau, nên không có giới hạn (kể cả giới hạn vô cùng) khi x -> 1.
- `gt_t2_vc_06` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 2 và x luôn lớn hơn 2, 1/(x - 2) dần tới đâu?
    - **(đúng)** +vô cùng
    - -vô cùng
    - 0
    - 1/2
  - **Đáp án:** +vô cùng
    1. Với x > 2, mẫu x - 2 dương và dần tới 0.
    2. 1 chia cho số dương rất nhỏ thì rất lớn và dương.
    3. Vậy 1/(x - 2) -> +vô cùng.
- `gt_t2_vc_07` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của x . (sqrt(x^2 + 1) - x) khi x -> +vô cùng.
  - **Đáp án:** 1/2
    1. Nhân và chia sqrt(x^2 + 1) - x cho liên hợp: sqrt(x^2 + 1) - x = 1 / (sqrt(x^2 + 1) + x).
    2. Biểu thức bằng x / (sqrt(x^2 + 1) + x).
    3. Chia tử và mẫu cho x (x > 0): 1 / (sqrt(1 + 1/x^2) + 1) -> 1/2.
- `gt_t2_vc_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của sqrt(x^2 + 2x) - x khi x -> +vô cùng.
  - **Lời giải đưa ra (có một bước sai):**
    1. Nhân và chia cho biểu thức liên hợp sqrt(x^2 + 2x) + x.
    2. Tử thành (x^2 + 2x) - x^2 = 2x.
    3. Biểu thức bằng 2x / (sqrt(x^2 + 2x) + x).
    4. Chia tử và mẫu cho x: 2 / (sqrt(1 + 2/x) + 1).
    5. Khi x -> +vô cùng, mẫu dần tới 1, nên giới hạn bằng 2.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 5: Khi x -> +vô cùng, mẫu dần tới 1, nên giới hạn bằng 2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 5 sai: sqrt(1 + 2/x) -> 1, nên mẫu sqrt(1 + 2/x) + 1 dần tới 2, không phải 1.
    2. Giới hạn đúng là 2 / 2 = 1.
- `gt_t2_vc_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của (x^2 + 1) / (3x^2 - x) khi x -> +vô cùng.
  - **Đáp án (thứ tự đúng):**
    1. Chia cả tử và mẫu cho x^2.
    2. Được (1 + 1/x^2) / (3 - 1/x).
    3. Khi x -> +vô cùng, 1/x^2 -> 0 và 1/x -> 0.
    4. Giới hạn bằng 1/3.
  - **Lời giải:**
    1. Tử và mẫu cùng bậc 2, nên chia cho x^2.
    2. Các số hạng còn chứa x ở mẫu đều dần tới 0.
    3. Còn lại tỉ số hai hệ số cao nhất: 1/3.
- `gt_g2_can_lien_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của sqrt(x^2 - 7x + 4) - x khi x -> +vô cùng.
  - **Đáp án:** -7/2
    1. Dạng vô cùng trừ vô cùng: nhân và chia cho biểu thức liên hợp sqrt(x^2 - 7x + 4) + x.
    2. Tử thành (x^2 - 7x + 4) - x^2 = -7x + 4.
    3. Chia tử và mẫu cho x: tử -> -7, mẫu = sqrt(1 + ...) + 1 -> 1 + 1 = 2.
    4. Giới hạn bằng -7 / 2 = -7/2.
  - **Câu hỏi:** Tính giới hạn của sqrt(x^2 - 7x + 1) - x khi x -> +vô cùng.
  - **Đáp án:** -7/2
    1. Dạng vô cùng trừ vô cùng: nhân và chia cho biểu thức liên hợp sqrt(x^2 - 7x + 1) + x.
    2. Tử thành (x^2 - 7x + 1) - x^2 = -7x + 1.
    3. Chia tử và mẫu cho x: tử -> -7, mẫu = sqrt(1 + ...) + 1 -> 1 + 1 = 2.
    4. Giới hạn bằng -7 / 2 = -7/2.
  - **Câu hỏi:** Tính giới hạn của sqrt(x^2 + 9x + 2) - x khi x -> +vô cùng.
  - **Đáp án:** 9/2
    1. Dạng vô cùng trừ vô cùng: nhân và chia cho biểu thức liên hợp sqrt(x^2 + 9x + 2) + x.
    2. Tử thành (x^2 + 9x + 2) - x^2 = 9x + 2.
    3. Chia tử và mẫu cho x: tử -> 9, mẫu = sqrt(1 + ...) + 1 -> 1 + 1 = 2.
    4. Giới hạn bằng 9 / 2 = 9/2.

### Hai giới hạn đáng nhớ (`gt_t2_gioi_han_dac_biet`)

- `gt_t2_db_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với x đo bằng radian, giới hạn của sin x / x khi x -> 0 bằng 1.
  - **Đáp án:** Đúng
    1. Đây là giới hạn đáng nhớ thứ nhất.
    2. Gần 0, đồ thị y = sin x gần như trùng đường y = x, nên tỉ số dần tới 1.
- `gt_t2_db_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (1 + 1/n)^n khi n -> +vô cùng bằng bao nhiêu?
    - **(đúng)** e
    - 1
    - +vô cùng
    - 0
  - **Đáp án:** e
    1. Đây là giới hạn đáng nhớ thứ hai, cũng là định nghĩa của số e (khoảng 2.718).
    2. Cơ số dần tới 1 nhưng số mũ dần ra vô cùng: dạng 1 mũ vô cùng, kết quả không phải 1.
- `gt_t2_db_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của sin(5x) / x khi x -> 0.
  - **Đáp án:** 5
    1. Viết sin(5x) / x = 5 . sin(5x) / (5x).
    2. Đặt u = 5x thì u -> 0, nên sin(5x) / (5x) -> 1.
    3. Giới hạn bằng 5 . 1 = 5.
- `gt_t2_db_04` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của sin x / x khi x -> +vô cùng bằng 1.
  - **Đáp án:** Sai
    1. Giới hạn bằng 1 chỉ đúng khi x -> 0.
    2. Khi x -> +vô cùng, |sin x / x| <= 1/x -> 0.
    3. Vậy giới hạn bằng 0.
- `gt_g2_sin_x` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của tan(3x) / (7x) khi x -> 0.
  - **Đáp án:** 3/7
    1. Dùng sin u / u -> 1 khi u -> 0 (và tan u / u -> 1, vì tan u = sin u / cos u).
    2. Khi x -> 0: tan(3x) ~ 3x, tức là tỉ số của chúng dần tới 1.
    3. Vậy giới hạn bằng 3 / 7 = 3/7.
  - **Câu hỏi:** Tính giới hạn của sin(-6x) / (-6x) khi x -> 0.
  - **Đáp án:** 1
    1. Dùng sin u / u -> 1 khi u -> 0 (và tan u / u -> 1, vì tan u = sin u / cos u).
    2. Khi x -> 0: sin(-6x) ~ -6x, tức là tỉ số của chúng dần tới 1.
    3. Vậy giới hạn bằng -6 / (-6) = 1.
  - **Câu hỏi:** Tính giới hạn của tan(3x) / (2x) khi x -> 0.
  - **Đáp án:** 3/2
    1. Dùng sin u / u -> 1 khi u -> 0 (và tan u / u -> 1, vì tan u = sin u / cos u).
    2. Khi x -> 0: tan(3x) ~ 3x, tức là tỉ số của chúng dần tới 1.
    3. Vậy giới hạn bằng 3 / 2 = 3/2.
- `gt_t2_db_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (1 - cos x) / x^2 khi x -> 0.
  - **Đáp án:** 1/2
    1. Dùng 1 - cos x = 2 sin^2(x/2).
    2. Biểu thức bằng 2 sin^2(x/2) / x^2 = (1/2) . [sin(x/2) / (x/2)]^2.
    3. sin(x/2) / (x/2) -> 1, nên giới hạn bằng 1/2.
- `gt_t2_db_06` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, hàm (1 + 3x)^(1/x) dần tới đâu?
    - **(đúng)** e^3
    - e
    - 3e
    - 1
  - **Đáp án:** e^3
    1. Dạng 1 mũ vô cùng. Đặt t = 3x thì t -> 0 và 1/x = 3/t.
    2. (1 + 3x)^(1/x) = [(1 + t)^(1/t)]^3.
    3. (1 + t)^(1/t) -> e khi t -> 0 (một cách viết khác của giới hạn đáng nhớ thứ hai), nên kết quả là e^3.
- `gt_t2_db_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (1 + 1/n)^(3n) khi n -> +vô cùng.
  - **Lời giải đưa ra (có một bước sai):**
    1. Khi n -> +vô cùng, cơ số 1 + 1/n dần tới 1.
    2. Vì cơ số dần tới 1, có thể thay cơ số bằng 1: (1 + 1/n)^(3n) gần bằng 1^(3n).   **<- bước sai đầu tiên**
    3. 1^(3n) = 1 với mọi n.
    4. Vậy giới hạn bằng 1.
  - **Đáp án:** Bước 2: Vì cơ số dần tới 1, có thể thay cơ số bằng 1: (1 + 1/n)^(3n) gần bằng 1^(3n).
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: số mũ 3n cũng dần ra vô cùng, đây là dạng vô định 1 mũ vô cùng, không được thay riêng cơ số.
    2. Đúng là (1 + 1/n)^(3n) = [(1 + 1/n)^n]^3 -> e^3.
- `gt_t2_db_08` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của x . sin(1/x) khi x -> 0 bằng 1.
  - **Đáp án:** Sai
    1. Đây không phải dạng sin u / u với u -> 0: khi x -> 0 thì 1/x -> vô cùng.
    2. Vì |sin(1/x)| <= 1 nên |x . sin(1/x)| <= |x| -> 0.
    3. Theo nguyên lý kẹp, giới hạn bằng 0.
- `gt_t2_db_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của (1 - cos 2x) / x^2 khi x -> 0.
  - **Đáp án (thứ tự đúng):**
    1. Dùng công thức 1 - cos 2x = 2 sin^2 x.
    2. Biểu thức bằng 2 . (sin x / x)^2.
    3. Khi x -> 0, sin x / x -> 1.
    4. Giới hạn bằng 2 . 1^2 = 2.
  - **Lời giải:**
    1. Biến 1 - cos về sin bình phương để xuất hiện sin x / x.
    2. Sau đó dùng giới hạn đáng nhớ sin x / x -> 1.
    3. Kết quả 2.
- `gt_g2_mu_e` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Khi n -> +vô cùng, dãy (1 + 1/n)^(-2n) dần tới e^k. Tìm k.
  - **Đáp án:** -2
    1. Giới hạn cơ bản: (1 + 1/m)^m -> e khi m -> vô cùng (m dương hay âm đều đúng).
    2. Đặt m = n, thì 1/n = 1/m và -2n = -2m, nên dãy bằng [(1 + 1/m)^m]^(-2).
    3. Phần trong ngoặc vuông dần tới e, nên dãy dần tới e^(-2): k = -2.
  - **Câu hỏi:** Khi n -> +vô cùng, dãy (1 - 3/n)^(-4n) dần tới e^k. Tìm k.
  - **Đáp án:** 12
    1. Giới hạn cơ bản: (1 + 1/m)^m -> e khi m -> vô cùng (m dương hay âm đều đúng).
    2. Đặt m = n/(-3), thì -3/n = 1/m và -4n = 12m, nên dãy bằng [(1 + 1/m)^m]^(12).
    3. Phần trong ngoặc vuông dần tới e, nên dãy dần tới e^(12): k = 12.
  - **Câu hỏi:** Khi n -> +vô cùng, dãy (1 + 2/n)^(-n) dần tới e^k. Tìm k.
  - **Đáp án:** -2
    1. Giới hạn cơ bản: (1 + 1/m)^m -> e khi m -> vô cùng (m dương hay âm đều đúng).
    2. Đặt m = n/2, thì 2/n = 1/m và -n = -2m, nên dãy bằng [(1 + 1/m)^m]^(-2).
    3. Phần trong ngoặc vuông dần tới e, nên dãy dần tới e^(-2): k = -2.

### Vô cùng bé, vô cùng lớn và tương đương (`gt_t2_vo_cung_be`)

- `gt_t2_vb_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, x^2 là vô cùng bé bậc cao hơn x.
  - **Đáp án:** Đúng
    1. a là vô cùng bé bậc cao hơn b khi a/b -> 0.
    2. x^2 / x = x -> 0 khi x -> 0.
    3. Vậy x^2 có bậc cao hơn x.
- `gt_t2_vb_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, vô cùng bé nào sau đây tương đương với x?
    - **(đúng)** sin x
    - x^2
    - 1 - cos x
    - 2x
  - **Đáp án:** sin x
    1. a tương đương b khi a/b -> 1.
    2. sin x / x -> 1, nên sin x tương đương x.
    3. x^2 / x -> 0, (1 - cos x) / x -> 0, còn 2x / x = 2, khác 1.
- `gt_t2_vb_03` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, ghép mỗi vô cùng bé với một vô cùng bé tương đương đơn giản của nó.
  - **Đáp án (ghép đúng):**
    - sin(3x) — 3x
    - 1 - cos x — x^2 / 2
    - e^(2x) - 1 — 2x
    - ln(1 + x^2) — x^2
  - **Lời giải:**
    1. sin u ~ u, e^u - 1 ~ u, ln(1 + u) ~ u khi u -> 0.
    2. Với u = 3x, 2x, x^2 lần lượt được 3x, 2x, x^2.
    3. 1 - cos x = 2 sin^2(x/2) ~ 2 (x/2)^2 = x^2 / 2.
- `gt_t2_vb_04` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm 1/x là một vô cùng lớn khi x -> 0.
  - **Đáp án:** Đúng
    1. Vô cùng lớn là đại lượng có trị tuyệt đối dần ra +vô cùng.
    2. Khi x -> 0, |1/x| = 1/|x| -> +vô cùng (dù dấu ở hai phía khác nhau).
    3. Vậy 1/x là vô cùng lớn.
- `gt_g2_vcb_cap` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, a(x) = -4x^5 - x là vô cùng bé cấp k so với x, nghĩa là a(x) / x^k dần tới một số khác 0. Tìm k.
  - **Đáp án:** 1
    1. Khi x -> 0, x^5 nhỏ hơn x rất nhiều (x^5 / x = x^4 -> 0).
    2. Số hạng quyết định là -x, nên đây là vô cùng bé cấp 1.
  - **Câu hỏi:** Khi x -> 0, a(x) = -3x^6 + x là vô cùng bé cấp k so với x, nghĩa là a(x) / x^k dần tới một số khác 0. Tìm k.
  - **Đáp án:** 1
    1. Khi x -> 0, x^6 nhỏ hơn x rất nhiều (x^6 / x = x^5 -> 0).
    2. Số hạng quyết định là x, nên đây là vô cùng bé cấp 1.
  - **Câu hỏi:** Khi x -> 0, a(x) = x^6 - 3x^5 là vô cùng bé cấp k so với x, nghĩa là a(x) / x^k dần tới một số khác 0. Tìm k.
  - **Đáp án:** 5
    1. Khi x -> 0, x^6 nhỏ hơn x^5 rất nhiều (x^6 / x^5 = x -> 0).
    2. Số hạng quyết định là -3x^5, nên đây là vô cùng bé cấp 5.
- `gt_t2_vb_05` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của [ln(1 + 3x) . sin(2x)] / x^2 khi x -> 0.
  - **Đáp án:** 6
    1. Khi x -> 0: ln(1 + 3x) ~ 3x và sin(2x) ~ 2x.
    2. Trong một tích, được thay từng thừa số bằng vô cùng bé tương đương: tử ~ 6x^2.
    3. Giới hạn = 6x^2 / x^2 = 6.
- `gt_t2_vb_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (tan x - sin x) / x^3 khi x -> 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Khi x -> 0: tan x ~ x và sin x ~ x.
    2. Thay vào tử: tan x - sin x ~ x - x = 0.   **<- bước sai đầu tiên**
    3. Vậy giới hạn bằng 0 / x^3 = 0.
  - **Đáp án:** Bước 2: Thay vào tử: tan x - sin x ~ x - x = 0.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: không được thay vô cùng bé tương đương trong một hiệu khi hai số hạng triệt tiêu nhau.
    2. Viết tan x - sin x = tan x . (1 - cos x) ~ x . x^2 / 2 (một tích, thay được).
    3. Giới hạn đúng là (x^3 / 2) / x^3 = 1/2.
- `gt_t2_vb_07` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> 0, so sánh a(x) = x^2 + x^3 và b(x) = sin(x^2).
    - **(đúng)** a và b tương đương
    - a là vô cùng bé bậc cao hơn b
    - b là vô cùng bé bậc cao hơn a
    - a/b không có giới hạn
  - **Đáp án:** a và b tương đương
    1. sin(x^2) ~ x^2 khi x -> 0.
    2. a/b = (x^2 + x^3) / sin(x^2), và (x^2 + x^3) / x^2 = 1 + x -> 1.
    3. Vậy a/b -> 1: a và b tương đương.
- `gt_t2_vb_08` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (sin x - x) / x^3 khi x -> 0 bằng 0.
  - **Đáp án:** Sai
    1. Thay sin x ~ x vào hiệu sin x - x cho 0, nhưng phép thay đó sai vì hai số hạng triệt tiêu nhau.
    2. Thật ra sin x - x ~ -x^3 / 6 khi x -> 0.
    3. Giới hạn bằng -1/6, không phải 0.
- `gt_t2_vb_09` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của (e^(2x) - 1) / ln(1 + 4x) khi x -> 0.
  - **Đáp án (thứ tự đúng):**
    1. Nhận ra dạng 0/0 khi x -> 0.
    2. Thay các vô cùng bé tương đương: e^(2x) - 1 ~ 2x và ln(1 + 4x) ~ 4x.
    3. Giới hạn bằng giới hạn của 2x / (4x).
    4. Rút gọn được 1/2.
  - **Lời giải:**
    1. Tử và mẫu đều là vô cùng bé, và đây là một thương nên được thay tương đương.
    2. 2x / (4x) = 1/2 với mọi x khác 0.
- `gt_g2_vcb_thay` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng vô cùng bé tương đương, tính giới hạn của tan(-2x) / arcsin(-5x) khi x -> 0.
  - **Đáp án:** 2/5
    1. Khi x -> 0: tan(-2x) ~ -2x và arcsin(-5x) ~ -5x.
    2. Trong một thương, được thay mỗi vô cùng bé bằng một vô cùng bé tương đương.
    3. Giới hạn = lim (-2x) / (-5x) = -2 / (-5) = 2/5.
  - **Câu hỏi:** Dùng vô cùng bé tương đương, tính giới hạn của arcsin(-x) / tan(-4x) khi x -> 0.
  - **Đáp án:** 1/4
    1. Khi x -> 0: arcsin(-x) ~ -x và tan(-4x) ~ -4x.
    2. Trong một thương, được thay mỗi vô cùng bé bằng một vô cùng bé tương đương.
    3. Giới hạn = lim (-x) / (-4x) = -1 / (-4) = 1/4.
  - **Câu hỏi:** Dùng vô cùng bé tương đương, tính giới hạn của tan(-x) / (e^(4x) - 1) khi x -> 0.
  - **Đáp án:** -1/4
    1. Khi x -> 0: tan(-x) ~ -x và (e^(4x) - 1) ~ 4x.
    2. Trong một thương, được thay mỗi vô cùng bé bằng một vô cùng bé tương đương.
    3. Giới hạn = lim (-x) / (4x) = -1 / 4 = -1/4.

## Tầng 3: Hàm liên tục và điểm gián đoạn

60 dạng câu (50 câu viết tay, 10 bộ sinh câu); 60 chưa duyệt.

### Liên tục tại một điểm (`gt_t3_lien_tuc_diem`)

- `gt_t3_ld_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (x^2 + 1) / (x - 3) liên tục tại x = 1.
  - **Đáp án:** Đúng
    1. Phân thức liên tục tại mọi điểm mà mẫu khác 0.
    2. Tại x = 1, mẫu bằng 1 - 3 = -2, khác 0.
    3. Vậy f liên tục tại 1.
- `gt_t3_ld_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f xác định quanh a và tại a. f liên tục tại a khi nào?
    - **(đúng)** Giới hạn của f khi x -> a tồn tại và bằng f(a)
    - f(a) có nghĩa
    - Giới hạn của f khi x -> a tồn tại
    - Giới hạn trái của f tại a tồn tại
  - **Đáp án:** Giới hạn của f khi x -> a tồn tại và bằng f(a)
    1. Liên tục cần đủ ba điều: f(a) có nghĩa, giới hạn tại a tồn tại, và hai số đó bằng nhau.
    2. Ba lựa chọn còn lại mỗi cái chỉ nói một phần.
- `gt_t3_ld_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = 3x^2 - 2x liên tục trên R. Tính giới hạn của f(x) khi x -> 2.
  - **Đáp án:** 8
    1. f liên tục tại 2 nên giới hạn tại 2 bằng f(2).
    2. f(2) = 3 . 4 - 2 . 2 = 8.
- `gt_t3_ld_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với điều đúng về nó tại x = 0.
  - **Đáp án (ghép đúng):**
    - f(x) = x^2 — liên tục tại 0
    - f(x) = sqrt(x) — chỉ xác định khi x >= 0
    - f(x) = |x| / x với x khác 0, f(0) = 1 — không có giới hạn tại 0
    - f(x) = sin x / x với x khác 0, f(0) = 2 — có giới hạn tại 0 nhưng giới hạn khác f(0)
  - **Lời giải:**
    1. x^2 là đa thức: liên tục tại 0.
    2. sqrt(x) không có nghĩa khi x < 0.
    3. |x| / x bằng -1 bên trái và 1 bên phải: hai phía khác nhau nên không có giới hạn.
    4. sin x / x -> 1 khác f(0) = 2.
- `gt_t3_ld_10` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = |x| liên tục tại x = 0.
  - **Đáp án:** Đúng
    1. f(0) = 0.
    2. Khi x -> 0 thì |x| -> 0 từ cả hai phía.
    3. Giới hạn bằng f(0), nên f liên tục tại 0 (dù đồ thị có góc nhọn ở đó).
- `gt_g3_lien_tuc_tf` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 - x - 12) / (x + 3) nếu x khác -3; f(-3) = -10. Hàm f liên tục tại x = -3.
  - **Đáp án:** Sai
    1. f(x) liên tục tại -3 khi giới hạn của f tại -3 bằng f(-3) = -10.
    2. Với x khác -3: tử = (x + 3)(x - 4), nên f(x) = x - 4.
    3. Giới hạn khi x -> -3 là -3 - 4 = -7.
    4. Giới hạn -7 khác f(-3) = -10, nên f không liên tục tại -3.
  - **Câu hỏi:** Cho f(x) = (x^2 + 9x + 20) / (x + 5) nếu x khác -5; f(-5) = -1. Hàm f liên tục tại x = -5.
  - **Đáp án:** Đúng
    1. f(x) liên tục tại -5 khi giới hạn của f tại -5 bằng f(-5) = -1.
    2. Với x khác -5: tử = (x + 5)(x + 4), nên f(x) = x + 4.
    3. Giới hạn khi x -> -5 là -5 - (-4) = -1.
    4. Giới hạn bằng f(-5), nên f liên tục tại -5.
  - **Câu hỏi:** Cho f(x) = (x^2 - 2x - 8) / (x + 2) nếu x khác -2; f(-2) = -7. Hàm f liên tục tại x = -2.
  - **Đáp án:** Sai
    1. f(x) liên tục tại -2 khi giới hạn của f tại -2 bằng f(-2) = -7.
    2. Với x khác -2: tử = (x + 2)(x - 4), nên f(x) = x - 4.
    3. Giới hạn khi x -> -2 là -2 - 4 = -6.
    4. Giới hạn -6 khác f(-2) = -7, nên f không liên tục tại -2.
- `gt_t3_ld_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai hàm f, g cùng liên tục tại a: các hàm f + g và f . g cũng liên tục tại a.
  - **Đáp án:** Đúng
    1. Giới hạn của tổng (tích) bằng tổng (tích) các giới hạn khi các giới hạn đó tồn tại.
    2. Giới hạn của f + g tại a là f(a) + g(a), đúng bằng giá trị của f + g tại a; với tích cũng vậy.
    3. Nên f + g và f . g liên tục tại a.
- `gt_t3_ld_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét tính liên tục tại 0 của f(x) = x . sin(1/x) với x khác 0, f(0) = 1.
  - **Lời giải đưa ra (có một bước sai):**
    1. Với x khác 0: |x . sin(1/x)| <= |x|.
    2. |x| -> 0 khi x -> 0, nên theo nguyên lý kẹp, giới hạn của f tại 0 bằng 0.
    3. Giới hạn bằng 0 còn f(0) = 1.
    4. Vậy f liên tục tại 0.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vậy f liên tục tại 0.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng: giới hạn tại 0 là 0, còn f(0) = 1.
    2. Bước 4 sai: giới hạn khác f(0) thì f không liên tục tại 0.
    3. Kết luận đúng: f gián đoạn tại 0 (gián đoạn khử được: gán lại f(0) = 0 thì liên tục).
- `gt_t3_ld_07` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (x^2 - 1) / (x^2 - x) không xác định tại x = 1. Gán f(1) = L thì f liên tục tại 1. Tìm L.
  - **Đáp án:** 2
    1. Cần L bằng giới hạn của f khi x -> 1.
    2. f(x) = (x - 1)(x + 1) / [x(x - 1)] = (x + 1) / x với x khác 0 và 1.
    3. Giới hạn khi x -> 1 là 2 / 1 = 2, nên L = 2.
- `gt_t3_ld_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào sau đây liên tục tại mọi điểm của R?
    - **(đúng)** f(x) = sin(x^2 + 1)
    - f(x) = 1 / (x^2 - 1)
    - f(x) = ln|x|
    - f(x) = tan x
  - **Đáp án:** f(x) = sin(x^2 + 1)
    1. sin(x^2 + 1) là hợp của đa thức và sin, cả hai liên tục trên R, nên liên tục trên R.
    2. 1 / (x^2 - 1) không xác định tại x = 1 và x = -1; ln|x| không xác định tại 0.
    3. tan x không xác định tại pi/2 + k pi.
- `gt_t3_ld_09` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 - 4) / (x - 2) với x khác 2 và f(2) = 4. Sắp xếp các bước xét tính liên tục của f tại 2.
  - **Đáp án (thứ tự đúng):**
    1. Với x khác 2, phân tích tử: f(x) = (x - 2)(x + 2) / (x - 2).
    2. Rút gọn được f(x) = x + 2 với x khác 2.
    3. Giới hạn của f khi x -> 2 bằng 2 + 2 = 4.
    4. So với f(2) = 4: giới hạn bằng giá trị tại điểm.
    5. Kết luận: f liên tục tại 2.
  - **Lời giải:**
    1. Tính giới hạn bằng cách rút gọn thừa số chung x - 2.
    2. Giới hạn 4 bằng f(2) = 4, nên f liên tục tại 2.
- `gt_g3_thac_trien` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (x^4 - 16) / (x + 2) không xác định tại x = -2. Phải gán f(-2) bằng bao nhiêu để f liên tục tại -2?
  - **Đáp án:** -32
    1. Cần f(-2) bằng giới hạn của f khi x -> -2.
    2. Tử = (x^4 - (-2)^4) chia hết cho x + 2: x^4 - a^4 = (x - a)(x^3 + ... + a^3), gồm 4 số hạng.
    3. Sau khi rút gọn, cho x -> -2: mỗi số hạng trong ngoặc dần tới (-2)^3 = -8.
    4. Giới hạn = 1 . 4 . (-8) = -32, nên gán f(-2) = -32.
  - **Câu hỏi:** Hàm f(x) = (x^2 - 16) / (x + 4) không xác định tại x = -4. Phải gán f(-4) bằng bao nhiêu để f liên tục tại -4?
  - **Đáp án:** -8
    1. Cần f(-4) bằng giới hạn của f khi x -> -4.
    2. Tử = (x^2 - (-4)^2) chia hết cho x + 4: x^2 - a^2 = (x - a)(x + a), gồm 2 số hạng.
    3. Sau khi rút gọn, cho x -> -4: mỗi số hạng trong ngoặc dần tới (-4) = -4.
    4. Giới hạn = 1 . 2 . (-4) = -8, nên gán f(-4) = -8.
  - **Câu hỏi:** Hàm f(x) = (2x^4 - 2) / (x + 1) không xác định tại x = -1. Phải gán f(-1) bằng bao nhiêu để f liên tục tại -1?
  - **Đáp án:** -8
    1. Cần f(-1) bằng giới hạn của f khi x -> -1.
    2. Tử = 2(x^4 - (-1)^4) chia hết cho x + 1: x^4 - a^4 = (x - a)(x^3 + ... + a^3), gồm 4 số hạng.
    3. Sau khi rút gọn, cho x -> -1: mỗi số hạng trong ngoặc dần tới (-1)^3 = -1.
    4. Giới hạn = 2 . 4 . (-1) = -8, nên gán f(-1) = -8.

### Giới hạn một phía và liên tục một phía (`gt_t3_mot_phia`)

- `gt_t3_mp_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = sqrt(x) liên tục phải tại x = 0.
  - **Đáp án:** Đúng
    1. f(0) = 0.
    2. Khi x -> 0 với x > 0, sqrt(x) -> 0.
    3. Giới hạn phải bằng f(0), nên f liên tục phải tại 0 (bên trái f không xác định).
- `gt_t3_mp_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 nếu x < 1; f(x) = 3 - x nếu x >= 1. Tính giới hạn phải của f tại x = 1.
  - **Đáp án:** 2
    1. Giới hạn phải chỉ dùng các x > 1, tức công thức 3 - x.
    2. Cho x -> 1: 3 - 1 = 2.
- `gt_t3_mp_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của f khi x -> a tồn tại (hữu hạn) khi và chỉ khi điều nào xảy ra?
    - **(đúng)** Giới hạn trái và giới hạn phải tại a cùng tồn tại và bằng nhau
    - Giới hạn trái tại a tồn tại
    - f(a) có nghĩa
    - Giới hạn phải tại a bằng f(a)
  - **Đáp án:** Giới hạn trái và giới hạn phải tại a cùng tồn tại và bằng nhau
    1. x tiến tới a từ cả hai phía, nên cả hai phía phải cho cùng một số.
    2. f(a) không ảnh hưởng tới việc giới hạn có tồn tại hay không.
- `gt_t3_mp_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x + 1 nếu x < 0; f(0) = 5; f(x) = x^2 + 3 nếu x > 0. Ghép mỗi đại lượng với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - Giới hạn trái tại 0 — 1
    - Giới hạn phải tại 0 — 3
    - f(0) — 5
    - f(-2) — -1
  - **Lời giải:**
    1. Giới hạn trái dùng x + 1: 0 + 1 = 1.
    2. Giới hạn phải dùng x^2 + 3: 0 + 3 = 3.
    3. f(0) = 5 được cho riêng; f(-2) = -2 + 1 = -1.
- `gt_t3_mp_10` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f và mọi điểm a: nếu giới hạn trái và giới hạn phải của f tại a đều tồn tại nhưng khác nhau thì f không có giới hạn tại a.
  - **Đáp án:** Đúng
    1. Giới hạn tại a tồn tại khi và chỉ khi hai giới hạn một phía tồn tại và bằng nhau.
    2. Hai giới hạn một phía khác nhau thì điều kiện đó không thỏa.
- `gt_g3_mot_phia` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -3x - 2 nếu x < -2; f(x) = -3x^2 + 1 nếu x >= -2. Nhập giới hạn trái rồi giới hạn phải của f tại x = -2.
  - **Đáp án:** 4, -11
    1. Giới hạn trái dùng công thức của phía x < -2: (-3) . (-2) + (-2) = 4.
    2. Giới hạn phải dùng công thức của phía x >= -2: (-3) . (-2)^2 + 1 = -11.
    3. Đáp án: 4, -11.
  - **Câu hỏi:** Cho f(x) = -4x - 5 nếu x < 3; f(x) = -3x^2 - 1 nếu x >= 3. Nhập giới hạn trái rồi giới hạn phải của f tại x = 3.
  - **Đáp án:** -17, -28
    1. Giới hạn trái dùng công thức của phía x < 3: (-4) . 3 + (-5) = -17.
    2. Giới hạn phải dùng công thức của phía x >= 3: (-3) . 3^2 + (-1) = -28.
    3. Đáp án: -17, -28.
  - **Câu hỏi:** Cho f(x) = -2x - 1 nếu x < -2; f(x) = 2x^2 + 1 nếu x >= -2. Nhập giới hạn trái rồi giới hạn phải của f tại x = -2.
  - **Đáp án:** 3, 9
    1. Giới hạn trái dùng công thức của phía x < -2: (-2) . (-2) + (-1) = 3.
    2. Giới hạn phải dùng công thức của phía x >= -2: 2 . (-2)^2 + 1 = 9.
    3. Đáp án: 3, 9.
- `gt_t3_mp_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 - 1) / |x - 1| với x khác 1. Nhập giới hạn trái rồi giới hạn phải của f tại x = 1.
  - **Đáp án:** -2, 2
    1. Khi x < 1: |x - 1| = -(x - 1), nên f(x) = (x - 1)(x + 1) / [-(x - 1)] = -(x + 1) -> -2.
    2. Khi x > 1: |x - 1| = x - 1, nên f(x) = x + 1 -> 2.
    3. Đáp án: -2, 2.
- `gt_t3_mp_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 1 / (1 + 2^(1/x)) với x khác 0. Giới hạn trái của f tại 0 bằng 1.
  - **Đáp án:** Đúng
    1. Khi x -> 0 với x < 0, 1/x -> -vô cùng.
    2. Do đó 2^(1/x) -> 0.
    3. f(x) -> 1 / (1 + 0) = 1. (Bên phải thì 2^(1/x) -> +vô cùng và f -> 0.)
- `gt_t3_mp_07` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm giới hạn trái và giới hạn phải tại 0 của f(x) = |x| / (x^2 + x).
  - **Lời giải đưa ra (có một bước sai):**
    1. Với x > 0: |x| = x, nên f(x) = x / (x^2 + x) = 1 / (x + 1).
    2. Giới hạn phải tại 0 bằng 1.
    3. Với x < 0 (gần 0): |x| = -x, nên f(x) = -x / (x^2 + x) = 1 / (x + 1).   **<- bước sai đầu tiên**
    4. Giới hạn trái tại 0 bằng 1, nên f có giới hạn 1 tại 0.
  - **Đáp án:** Bước 3: Với x < 0 (gần 0): |x| = -x, nên f(x) = -x / (x^2 + x) = 1 / (x + 1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai dấu: -x / [x(x + 1)] = -1 / (x + 1).
    2. Giới hạn trái đúng là -1, khác giới hạn phải 1.
    3. f không có giới hạn tại 0.
- `gt_t3_mp_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 2x + 1 nếu x < 2; f(2) = 7; f(x) = x^2 + 1 nếu x > 2. Khẳng định nào đúng?
    - **(đúng)** f có giới hạn bằng 5 tại 2 nhưng không liên tục tại 2
    - f liên tục tại 2
    - f không có giới hạn tại 2
    - f liên tục trái tại 2
  - **Đáp án:** f có giới hạn bằng 5 tại 2 nhưng không liên tục tại 2
    1. Giới hạn trái: 2 . 2 + 1 = 5. Giới hạn phải: 2^2 + 1 = 5.
    2. Hai phía bằng nhau nên f có giới hạn 5 tại 2.
    3. Nhưng f(2) = 7 khác 5, nên f không liên tục tại 2, kể cả liên tục trái hay phải.
- `gt_t3_mp_09` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn phải tại 3 của f(x) = (x^2 - 3x) / |x - 3|.
  - **Đáp án (thứ tự đúng):**
    1. Khi x > 3 thì x - 3 > 0, nên |x - 3| = x - 3.
    2. Khi đó f(x) = x(x - 3) / (x - 3).
    3. Rút gọn: f(x) = x với x > 3.
    4. Giới hạn phải tại 3 bằng 3.
  - **Lời giải:**
    1. Giới hạn phải chỉ xét x > 3, nên bỏ được dấu giá trị tuyệt đối với dấu cộng.
    2. Sau khi rút gọn, cho x -> 3 được 3.
- `gt_g3_tri_tuyet_doi` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -3|x + 2| . (x + 4) / (x + 2) với x khác -2. Nhập giới hạn trái rồi giới hạn phải của f tại x = -2.
  - **Đáp án:** 6, -6
    1. Khi x < -2: |x + 2| = -(x + 2), nên f(x) = 3 . (x + 4).
    2. Khi x > -2: |x + 2| = x + 2, nên f(x) = (-3) . (x + 4).
    3. Cho x -> -2: giới hạn trái = 3 . 2 = 6, giới hạn phải = (-3) . 2 = -6.
  - **Câu hỏi:** Cho f(x) = -3|x + 4| . (x - 4) / (x + 4) với x khác -4. Nhập giới hạn trái rồi giới hạn phải của f tại x = -4.
  - **Đáp án:** -24, 24
    1. Khi x < -4: |x + 4| = -(x + 4), nên f(x) = 3 . (x - 4).
    2. Khi x > -4: |x + 4| = x + 4, nên f(x) = (-3) . (x - 4).
    3. Cho x -> -4: giới hạn trái = 3 . (-8) = -24, giới hạn phải = (-3) . (-8) = 24.
  - **Câu hỏi:** Cho f(x) = 2|x + 1| . (x + 4) / (x + 1) với x khác -1. Nhập giới hạn trái rồi giới hạn phải của f tại x = -1.
  - **Đáp án:** -6, 6
    1. Khi x < -1: |x + 1| = -(x + 1), nên f(x) = (-2) . (x + 4).
    2. Khi x > -1: |x + 1| = x + 1, nên f(x) = 2 . (x + 4).
    3. Cho x -> -1: giới hạn trái = (-2) . 3 = -6, giới hạn phải = 2 . 3 = 6.

### Tìm tham số để hàm liên tục (`gt_t3_tim_tham_so`)

- `gt_t3_ts_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = sin(4x) / x nếu x khác 0; f(0) = a. Tìm a để f liên tục tại 0.
  - **Đáp án:** 4
    1. Cần a bằng giới hạn của f khi x -> 0.
    2. sin(4x) / x = 4 . sin(4x) / (4x) -> 4 . 1 = 4.
    3. Vậy a = 4.
- `gt_t3_ts_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x + 2 nếu x < 1; f(x) = 3x nếu x >= 1 liên tục trên R.
  - **Đáp án:** Đúng
    1. Mỗi mảnh là đa thức nên liên tục trên khoảng của nó; chỉ cần xét x = 1.
    2. Giới hạn trái: 1 + 2 = 3. Giới hạn phải và f(1): 3 . 1 = 3.
    3. Ba số bằng nhau, nên f liên tục tại 1, do đó trên R.
- `gt_t3_ts_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = ax + 1 nếu x < 2; f(x) = x^2 nếu x >= 2. Giá trị nào của a làm f liên tục trên R?
    - **(đúng)** 3/2
    - 2
    - 1/2
    - 5/2
  - **Đáp án:** 3/2
    1. Chỉ cần hai mảnh nối liền tại x = 2.
    2. Giới hạn trái: 2a + 1. Giới hạn phải và f(2): 4.
    3. 2a + 1 = 4 cho a = 3/2.
- `gt_t3_ts_04` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm a để f(x) = (x^2 - 9) / (x - 3) nếu x khác 3, f(3) = a, liên tục tại 3.
  - **Lời giải đưa ra (có một bước sai):**
    1. Cần a bằng giới hạn của f khi x -> 3.
    2. Với x khác 3: f(x) = (x - 3)(x + 3) / (x - 3) = x - 3.   **<- bước sai đầu tiên**
    3. Giới hạn khi x -> 3 bằng 0.
    4. Vậy a = 0.
  - **Đáp án:** Bước 2: Với x khác 3: f(x) = (x - 3)(x + 3) / (x - 3) = x - 3.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: rút gọn (x - 3)(x + 3) / (x - 3) còn lại x + 3, không phải x - 3.
    2. Giới hạn đúng là 3 + 3 = 6, nên a = 6.
- `gt_t3_ts_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 + a nếu x <= 1; f(x) = 2x + 3 nếu x > 1. Sắp xếp các bước tìm a để f liên tục trên R.
  - **Đáp án (thứ tự đúng):**
    1. Hai mảnh đều là đa thức, nên chỉ cần xét điểm nối x = 1.
    2. Giới hạn trái tại 1 bằng f(1) = 1 + a, còn giới hạn phải bằng 2 . 1 + 3 = 5.
    3. Cho hai số đó bằng nhau: 1 + a = 5.
    4. Giải được a = 4.
  - **Lời giải:**
    1. Bên trong mỗi khoảng f là đa thức nên liên tục.
    2. Tại x = 1, hai mảnh phải cho cùng một giá trị: 1 + a = 5, nên a = 4.
- `gt_g3_tham_so` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 - x - 12) / (x + 3) nếu x khác -3; f(-3) = m. Tìm m để f liên tục trên R.
  - **Đáp án:** -7
    1. Tại mọi x khác -3, f là phân thức có mẫu khác 0 nên liên tục; chỉ cần xét x = -3.
    2. Tử có nghiệm -3: x^2 - x - 12 = (x + 3)(x - 4).
    3. Với x khác -3, f(x) = x - 4, nên giới hạn tại -3 là -7.
    4. Cần m = f(-3) = -7.
  - **Câu hỏi:** Cho f(x) = (x^2 + 9x + 20) / (x + 5) nếu x khác -5; f(-5) = m. Tìm m để f liên tục trên R.
  - **Đáp án:** -1
    1. Tại mọi x khác -5, f là phân thức có mẫu khác 0 nên liên tục; chỉ cần xét x = -5.
    2. Tử có nghiệm -5: x^2 + 9x + 20 = (x + 5)(x + 4).
    3. Với x khác -5, f(x) = x + 4, nên giới hạn tại -5 là -1.
    4. Cần m = f(-5) = -1.
  - **Câu hỏi:** Cho f(x) = (x^2 - 2x - 8) / (x + 2) nếu x khác -2; f(-2) = m. Tìm m để f liên tục trên R.
  - **Đáp án:** -6
    1. Tại mọi x khác -2, f là phân thức có mẫu khác 0 nên liên tục; chỉ cần xét x = -2.
    2. Tử có nghiệm -2: x^2 - 2x - 8 = (x + 2)(x - 4).
    3. Với x khác -2, f(x) = x - 4, nên giới hạn tại -2 là -6.
    4. Cần m = f(-2) = -6.
- `gt_t3_ts_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (sqrt(x + 1) - 1) / x nếu x >= -1 và x khác 0; f(0) = a. Tìm a để f liên tục tại 0.
  - **Đáp án:** 1/2
    1. Nhân tử và mẫu với liên hợp sqrt(x + 1) + 1: tử thành (x + 1) - 1 = x.
    2. f(x) = 1 / (sqrt(x + 1) + 1) với x khác 0.
    3. Giới hạn khi x -> 0 là 1 / 2, nên a = 1/2.
- `gt_t3_ts_07` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 nếu x < 1; f(x) = ax + b nếu 1 <= x <= 2; f(x) = 2x + 1 nếu x > 2. Tìm a, b để f liên tục trên R. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** 4, -3
    1. Tại x = 1: giới hạn trái là 1, f(1) = a + b, nên a + b = 1.
    2. Tại x = 2: f(2) = 2a + b, giới hạn phải là 2 . 2 + 1 = 5, nên 2a + b = 5.
    3. Trừ hai phương trình: a = 4, rồi b = 1 - 4 = -3.
- `gt_t3_ts_08` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Không có số thực a nào làm hàm f(x) = 1 / (x - 1) nếu x khác 1, f(1) = a, liên tục tại 1.
  - **Đáp án:** Đúng
    1. Muốn liên tục tại 1, giới hạn của f tại 1 phải tồn tại hữu hạn.
    2. Khi x -> 1, 1/(x - 1) dần ra -vô cùng bên trái và +vô cùng bên phải: không có giới hạn hữu hạn.
    3. Nên không số a nào làm được.
- `gt_t3_ts_09` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (1 - cos x) / x^2 nếu x khác 0; f(0) = a. Giá trị nào của a làm f liên tục tại 0?
    - **(đúng)** 1/2
    - 1
    - 0
    - 2
  - **Đáp án:** 1/2
    1. Cần a bằng giới hạn của f khi x -> 0.
    2. 1 - cos x ~ x^2 / 2 khi x -> 0.
    3. Giới hạn bằng 1/2, nên a = 1/2.
- `gt_t3_ts_10` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm m để f(x) = mx^2 + 1 nếu x < 2; f(x) = 3x - m nếu x >= 2, liên tục trên R.
  - **Lời giải đưa ra (có một bước sai):**
    1. Mỗi mảnh là đa thức, chỉ cần xét điểm nối x = 2.
    2. Giới hạn trái tại 2: 4m + 1.
    3. Giới hạn phải tại 2 và f(2): 6 - m.
    4. Cho bằng nhau: 4m + 1 = 6 - m, nên 3m = 5.   **<- bước sai đầu tiên**
    5. Vậy m = 5/3.
  - **Đáp án:** Bước 4: Cho bằng nhau: 4m + 1 = 6 - m, nên 3m = 5.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai khi chuyển vế: 4m + m = 6 - 1, tức 5m = 5.
    2. Đúng là m = 1. Kiểm tra: 4 . 1 + 1 = 5 và 6 - 1 = 5.
- `gt_g3_tham_so_hai_nhanh` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -3x - 2 nếu x < -2; f(x) = mx^2 - 5 nếu x >= -2. Tìm m để f liên tục trên R.
  - **Đáp án:** 9/4
    1. Mỗi mảnh là đa thức nên liên tục; chỉ cần hai mảnh nối liền tại x = -2.
    2. Giới hạn trái: (-3) . (-2) + (-2) = 4.
    3. Giới hạn phải và f(-2): m . (-2)^2 + (-5) = 4m + (-5).
    4. Cho bằng nhau: 4m = 9, nên m = 9/4.
  - **Câu hỏi:** Cho f(x) = -3x - 5 nếu x < -3; f(x) = mx^2 - 1 nếu x >= -3. Tìm m để f liên tục trên R.
  - **Đáp án:** 5/9
    1. Mỗi mảnh là đa thức nên liên tục; chỉ cần hai mảnh nối liền tại x = -3.
    2. Giới hạn trái: (-3) . (-3) + (-5) = 4.
    3. Giới hạn phải và f(-3): m . (-3)^2 + (-1) = 9m + (-1).
    4. Cho bằng nhau: 9m = 5, nên m = 5/9.
  - **Câu hỏi:** Cho f(x) = -2x - 1 nếu x < -2; f(x) = mx^2 + 3 nếu x >= -2. Tìm m để f liên tục trên R.
  - **Đáp án:** 0
    1. Mỗi mảnh là đa thức nên liên tục; chỉ cần hai mảnh nối liền tại x = -2.
    2. Giới hạn trái: (-2) . (-2) + (-1) = 3.
    3. Giới hạn phải và f(-2): m . (-2)^2 + 3 = 4m + 3.
    4. Cho bằng nhau: 4m = 0, nên m = 0.

### Phân loại điểm gián đoạn (`gt_t3_phan_loai_gian_doan`)

- `gt_t3_pl_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = sin x / x không xác định tại 0, và x = 0 là điểm gián đoạn khử được của nó.
  - **Đáp án:** Đúng
    1. Gián đoạn khử được: giới hạn tại điểm đó tồn tại hữu hạn, nhưng f không xác định ở đó hoặc f khác giới hạn.
    2. sin x / x -> 1 khi x -> 0, hữu hạn.
    3. Gán thêm f(0) = 1 thì f liên tục: khử được.
- `gt_t3_pl_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** x = 0 là điểm gián đoạn loại gì của f(x) = |x| / x (x khác 0)?
    - **(đúng)** Loại một, có bước nhảy
    - Khử được
    - Loại hai
    - Không gián đoạn
  - **Đáp án:** Loại một, có bước nhảy
    1. Bên trái f(x) = -1, bên phải f(x) = 1.
    2. Hai giới hạn một phía hữu hạn nhưng khác nhau: gián đoạn loại một.
    3. Bước nhảy là 1 - (-1) = 2.
- `gt_t3_pl_03` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với tình trạng của nó tại x = 0.
  - **Đáp án (ghép đúng):**
    - sin x / x — gián đoạn khử được
    - |x| / x — gián đoạn loại một có bước nhảy
    - 1 / x — gián đoạn loại hai
    - x^2 — liên tục tại 0
  - **Lời giải:**
    1. sin x / x có giới hạn 1 hữu hạn tại 0: khử được.
    2. |x| / x có hai giới hạn một phía -1 và 1: loại một.
    3. 1/x dần ra vô cùng: loại hai. x^2 là đa thức nên liên tục.
- `gt_t3_pl_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (x^2 - 4) / (x^2 - 5x + 6) có hai điểm gián đoạn x = 2 và x = 3. Tính giới hạn của f tại điểm gián đoạn khử được.
  - **Đáp án:** -4
    1. Tử = (x - 2)(x + 2), mẫu = (x - 2)(x - 3).
    2. Tại x = 3 tử bằng 5 khác 0 nên f -> vô cùng: không khử được. Điểm khử được là x = 2.
    3. Rút gọn (x + 2) / (x - 3); tại x = 2 được 4 / (-1) = -4.
- `gt_t3_pl_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: phân loại điểm gián đoạn x = 1 của f(x) = 1 / (x - 1)^2.
  - **Lời giải đưa ra (có một bước sai):**
    1. f không xác định tại x = 1, nên x = 1 là điểm gián đoạn.
    2. Khi x -> 1, (x - 1)^2 -> 0 và luôn dương, nên f -> +vô cùng từ cả hai phía.
    3. Hai giới hạn một phía bằng nhau (đều là +vô cùng), nên đây là gián đoạn khử được.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Hai giới hạn một phía bằng nhau (đều là +vô cùng), nên đây là gián đoạn khử được.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: gián đoạn khử được cần giới hạn hữu hạn.
    2. Ở đây giới hạn là +vô cùng, nên x = 1 là điểm gián đoạn loại hai.
- `gt_g3_buoc_nhay` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -3x - 2 nếu x < -2; f(x) = -3x + 1 nếu x >= -2. x = -2 là điểm gián đoạn loại một. Tính bước nhảy: giới hạn phải trừ giới hạn trái.
  - **Đáp án:** 3
    1. Giới hạn trái: (-3) . (-2) + (-2) = 4.
    2. Giới hạn phải: (-3) . (-2) + 1 = 7.
    3. Hai giới hạn đều hữu hạn nhưng khác nhau: gián đoạn loại một.
    4. Bước nhảy = 7 - 4 = 3.
  - **Câu hỏi:** Cho f(x) = -4x - 5 nếu x < 3; f(x) = -3x - 1 nếu x >= 3. x = 3 là điểm gián đoạn loại một. Tính bước nhảy: giới hạn phải trừ giới hạn trái.
  - **Đáp án:** 7
    1. Giới hạn trái: (-4) . 3 + (-5) = -17.
    2. Giới hạn phải: (-3) . 3 + (-1) = -10.
    3. Hai giới hạn đều hữu hạn nhưng khác nhau: gián đoạn loại một.
    4. Bước nhảy = -10 - (-17) = 7.
  - **Câu hỏi:** Cho f(x) = -2x - 1 nếu x < -2; f(x) = 4x + 4 nếu x >= -2. x = -2 là điểm gián đoạn loại một. Tính bước nhảy: giới hạn phải trừ giới hạn trái.
  - **Đáp án:** -7
    1. Giới hạn trái: (-2) . (-2) + (-1) = 3.
    2. Giới hạn phải: 4 . (-2) + 4 = -4.
    3. Hai giới hạn đều hữu hạn nhưng khác nhau: gián đoạn loại một.
    4. Bước nhảy = -4 - 3 = -7.
- `gt_t3_pl_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = sin(1/x) không xác định tại 0, và x = 0 là điểm gián đoạn loại hai của nó.
  - **Đáp án:** Đúng
    1. Khi x -> 0 từ bên phải, 1/x chạy ra +vô cùng nên sin(1/x) dao động mãi giữa -1 và 1.
    2. Giới hạn phải không tồn tại (bên trái cũng vậy).
    3. Có một giới hạn một phía không tồn tại hữu hạn: gián đoạn loại hai.
- `gt_t3_pl_07` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** x = 0 là điểm gián đoạn loại gì của f(x) = e^(1/x) (x khác 0)?
    - **(đúng)** Loại hai
    - Khử được
    - Loại một, có bước nhảy
    - Không gián đoạn
  - **Đáp án:** Loại hai
    1. Bên trái: 1/x -> -vô cùng nên e^(1/x) -> 0.
    2. Bên phải: 1/x -> +vô cùng nên e^(1/x) -> +vô cùng.
    3. Giới hạn phải không hữu hạn, nên đây là gián đoạn loại hai.
- `gt_t3_pl_08` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = arctan(1/x) với x khác 0. Bước nhảy tại 0 (giới hạn phải trừ giới hạn trái) bằng k . pi. Tìm k.
  - **Đáp án:** 1
    1. Bên phải: 1/x -> +vô cùng nên arctan(1/x) -> pi/2.
    2. Bên trái: 1/x -> -vô cùng nên arctan(1/x) -> -pi/2.
    3. Bước nhảy = pi/2 - (-pi/2) = pi, nên k = 1.
- `gt_t3_pl_09` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước phân loại các điểm gián đoạn của f(x) = (x^2 - 1) / (x^2 + x).
  - **Đáp án (thứ tự đúng):**
    1. Mẫu x^2 + x = x(x + 1) bằng 0 tại x = 0 và x = -1: đó là hai điểm gián đoạn.
    2. Tử x^2 - 1 = (x - 1)(x + 1) cũng có thừa số x + 1.
    3. Rút gọn: với x khác 0 và -1, f(x) = (x - 1) / x.
    4. Kết luận: tại x = -1 giới hạn là (-2)/(-1) = 2 nên khử được; tại x = 0 tử -> -1, mẫu -> 0 nên loại hai.
  - **Lời giải:**
    1. Điểm gián đoạn của phân thức là nơi mẫu bằng 0.
    2. Thừa số chung rút gọn được cho gián đoạn khử được; nơi mẫu vẫn bằng 0 sau khi rút gọn cho gián đoạn loại hai.
- `gt_t3_pl_10` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: cho f(x) = x + 1 nếu x < 0; f(x) = x^2 + 1 nếu x >= 0, phân loại điểm x = 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Giới hạn trái tại 0: 0 + 1 = 1.
    2. Giới hạn phải tại 0: 0^2 + 1 = 1.
    3. f(0) = 0^2 + 1 = 1.
    4. Hai mảnh có công thức khác nhau, nên f gián đoạn loại một tại 0.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Hai mảnh có công thức khác nhau, nên f gián đoạn loại một tại 0.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: công thức khác nhau không có nghĩa là gián đoạn.
    2. Giới hạn trái, giới hạn phải và f(0) đều bằng 1, nên f liên tục tại 0.
- `gt_g3_khu_duoc` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = (x^2 + 7x + 12) / (x^2 - x - 12) có hai điểm gián đoạn. Nhập điểm gián đoạn khử được rồi giới hạn của f tại điểm đó.
  - **Đáp án:** -3, -1/7
    1. Mẫu = (x + 3)(x - 4) bằng 0 tại x = -3 và x = 4.
    2. Tử = (x + 3)(x + 4) cũng bằng 0 tại x = -3, nhưng khác 0 tại x = 4.
    3. Tại x = 4: tử khác 0, mẫu -> 0, nên f -> vô cùng: gián đoạn loại hai.
    4. Tại x = -3: rút gọn được (x + 4) / (x - 4), giới hạn (1) / (-7) = -1/7 hữu hạn: gián đoạn khử được.
    5. Đáp án: -3, -1/7.
  - **Câu hỏi:** Hàm f(x) = (x^2 + x - 20) / (x^2 + 9x + 20) có hai điểm gián đoạn. Nhập điểm gián đoạn khử được rồi giới hạn của f tại điểm đó.
  - **Đáp án:** -5, 9
    1. Mẫu = (x + 5)(x + 4) bằng 0 tại x = -5 và x = -4.
    2. Tử = (x + 5)(x - 4) cũng bằng 0 tại x = -5, nhưng khác 0 tại x = -4.
    3. Tại x = -4: tử khác 0, mẫu -> 0, nên f -> vô cùng: gián đoạn loại hai.
    4. Tại x = -5: rút gọn được (x - 4) / (x + 4), giới hạn (-9) / (-1) = 9 hữu hạn: gián đoạn khử được.
    5. Đáp án: -5, 9.
  - **Câu hỏi:** Hàm f(x) = (x^2 - x - 6) / (x^2 - 2x - 8) có hai điểm gián đoạn. Nhập điểm gián đoạn khử được rồi giới hạn của f tại điểm đó.
  - **Đáp án:** -2, 5/6
    1. Mẫu = (x + 2)(x - 4) bằng 0 tại x = -2 và x = 4.
    2. Tử = (x + 2)(x - 3) cũng bằng 0 tại x = -2, nhưng khác 0 tại x = 4.
    3. Tại x = 4: tử khác 0, mẫu -> 0, nên f -> vô cùng: gián đoạn loại hai.
    4. Tại x = -2: rút gọn được (x - 3) / (x - 4), giới hạn (-5) / (-6) = 5/6 hữu hạn: gián đoạn khử được.
    5. Đáp án: -2, 5/6.

### Hàm liên tục trên đoạn và giá trị trung gian (`gt_t3_lien_tuc_doan`)

- `gt_t3_lk_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f liên tục trên đoạn [a, b] mà f(a) . f(b) < 0, phương trình f(x) = 0 có ít nhất một nghiệm trong khoảng (a, b).
  - **Đáp án:** Đúng
    1. f(a) . f(b) < 0 nghĩa là f(a) và f(b) trái dấu, nên 0 nằm giữa hai giá trị đó.
    2. Theo định lý giá trị trung gian, hàm liên tục nhận mọi giá trị giữa f(a) và f(b).
    3. Vậy có c trong (a, b) với f(c) = 0.
- `gt_t3_lk_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét p(x) = x^3 - 3x + 1. Trong các khoảng sau, p(x) = 0 có nghiệm trong khoảng nào?
    - **(đúng)** (0, 1)
    - (-1, 0)
    - (2, 3)
    - (3, 4)
  - **Đáp án:** (0, 1)
    1. p(0) = 1 > 0 và p(1) = -1 < 0: trái dấu, nên có nghiệm trong (0, 1).
    2. p(-1) = 3 và p(0) = 1; p(2) = 3, p(3) = 19, p(4) = 53: các khoảng còn lại có hai đầu cùng dấu.
    3. p có đúng ba nghiệm thực, ở gần -1.88, 0.35 và 1.53, không nghiệm nào nằm trong ba khoảng kia.
- `gt_t3_lk_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f liên tục trên [0, 4] với f(0) = -2 và f(4) = 6. Định lý giá trị trung gian bảo đảm f(x) = c có nghiệm trong [0, 4] với mọi c thuộc đoạn [m, M]. Nhập m, M theo đúng thứ tự.
  - **Đáp án:** -2, 6
    1. Định lý chỉ dùng hai giá trị ở hai đầu mút: f(0) = -2 và f(4) = 6.
    2. Mọi c nằm giữa -2 và 6 đều được f nhận tại một điểm của [0, 4].
    3. Vậy m = -2, M = 6.
- `gt_t3_lk_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp chia đôi cho f(x) = x^2 - 2 trên [1, 2]. Ghép mỗi đại lượng với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - f(1) — -1
    - f(2) — 2
    - f(1.5) — 0.25
    - Khoảng chứa nghiệm sau một bước chia đôi — (1, 1.5)
  - **Lời giải:**
    1. f(1) = 1 - 2 = -1 và f(2) = 4 - 2 = 2: trái dấu, có nghiệm trong (1, 2).
    2. Điểm giữa 1.5: f(1.5) = 2.25 - 2 = 0.25 > 0.
    3. f(1) < 0 < f(1.5), nên nghiệm nằm trong (1, 1.5).
- `gt_t3_lk_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: chứng minh x^5 + x - 1 = 0 có nghiệm trong (0, 1).
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt p(x) = x^5 + x - 1; p là đa thức nên liên tục trên [0, 1].
    2. p(0) = -1 < 0.
    3. p(1) = 1 + 1 - 1 = 1 > 0.
    4. p(0) . p(1) > 0, nên theo định lý giá trị trung gian có nghiệm trong (0, 1).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: p(0) . p(1) > 0, nên theo định lý giá trị trung gian có nghiệm trong (0, 1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: p(0) . p(1) = (-1) . 1 = -1 < 0.
    2. Chính vì tích âm (hai đầu trái dấu) mới dùng được định lý giá trị trung gian; kết luận có nghiệm vẫn đúng.
- `gt_g3_doi_dau` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^3 + 2x + 6 = 0 có một nghiệm nằm trong khoảng (-3, -2).
  - **Đáp án:** Sai
    1. p(x) = x^3 + 2x + 6 liên tục trên R; vì p'(x) = 3x^2 + 2 > 0 nên p tăng ngặt và có đúng một nghiệm.
    2. p(-3) = -27 và p(-2) = -6.
    3. Hai giá trị cùng dấu; p tăng ngặt nên p không đổi dấu trên (-3, -2), không có nghiệm ở đó.
  - **Câu hỏi:** Phương trình x^3 + x - 25 = 0 có một nghiệm nằm trong khoảng (-3, -2).
  - **Đáp án:** Sai
    1. p(x) = x^3 + x - 25 liên tục trên R; vì p'(x) = 3x^2 + 1 > 0 nên p tăng ngặt và có đúng một nghiệm.
    2. p(-3) = -55 và p(-2) = -35.
    3. Hai giá trị cùng dấu; p tăng ngặt nên p không đổi dấu trên (-3, -2), không có nghiệm ở đó.
  - **Câu hỏi:** Phương trình x^3 + 2x + 7 = 0 có một nghiệm nằm trong khoảng (-2, -1).
  - **Đáp án:** Đúng
    1. p(x) = x^3 + 2x + 7 liên tục trên R; vì p'(x) = 3x^2 + 2 > 0 nên p tăng ngặt và có đúng một nghiệm.
    2. p(-2) = -5 và p(-1) = 4.
    3. Hai giá trị trái dấu, nên theo định lý giá trị trung gian có nghiệm trong (-2, -1).
- `gt_t3_lk_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phương pháp chia đôi cho p(x) = x^3 - 2 trên [1, 2]. Sau hai bước chia đôi, nghiệm nằm trong khoảng (a, b). Nhập a, b theo đúng thứ tự (phân số viết a/b hoặc số thập phân).
  - **Đáp án:** 5/4, 3/2
    1. p(1) = -1 < 0 và p(2) = 6 > 0.
    2. Bước 1, điểm giữa 1.5: p(1.5) = 3.375 - 2 = 1.375 > 0, nên giữ (1, 1.5).
    3. Bước 2, điểm giữa 1.25: p(1.25) = 1.953125 - 2 < 0, nên giữ (1.25, 1.5).
    4. Đáp án: 5/4, 3/2.
- `gt_t3_lk_07` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = 1/x có f(-1) = -1 < 0 < 1 = f(1), nên phương trình 1/x = 0 có nghiệm trong (-1, 1).
  - **Đáp án:** Sai
    1. Định lý giá trị trung gian cần f liên tục trên cả đoạn [-1, 1].
    2. 1/x không xác định tại 0, nên không liên tục trên [-1, 1].
    3. Thật vậy 1/x không bao giờ bằng 0: mệnh đề sai.
- `gt_t3_lk_08` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào sau đây chắc chắn đạt giá trị lớn nhất trên miền đã cho?
    - **(đúng)** f(x) = x^2 trên [0, 3]
    - f(x) = x trên (0, 1)
    - f(x) = 1/x trên (0, 1]
    - f(x) = x trên [0, +vô cùng)
  - **Đáp án:** f(x) = x^2 trên [0, 3]
    1. Hàm liên tục trên một đoạn đóng, bị chặn thì đạt giá trị lớn nhất và nhỏ nhất (định lý Weierstrass).
    2. x^2 liên tục trên [0, 3]: đạt lớn nhất 9 tại x = 3.
    3. x trên (0, 1) tiến gần 1 nhưng không đạt; 1/x trên (0, 1] và x trên [0, +vô cùng) không bị chặn trên.
- `gt_t3_lk_09` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh phương trình cos x = x có nghiệm trong (0, pi/2).
  - **Đáp án (thứ tự đúng):**
    1. Chuyển về một vế: đặt g(x) = cos x - x.
    2. g là hiệu của hai hàm liên tục nên liên tục trên [0, pi/2].
    3. Vì g liên tục, chỉ cần xét dấu ở hai đầu: g(0) = 1 > 0 và g(pi/2) = -pi/2 < 0.
    4. g đổi dấu, nên theo định lý giá trị trung gian có c trong (0, pi/2) với g(c) = 0, tức cos c = c.
  - **Lời giải:**
    1. Đưa phương trình về dạng g(x) = 0 rồi dùng định lý giá trị trung gian cho g.
    2. Cần đủ hai điều: g liên tục trên đoạn, và g trái dấu ở hai đầu.
- `gt_t3_lk_10` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^3 + x - 3 = 0 có đúng một nghiệm thực. Chia đôi một lần đoạn [1, 2], nghiệm nằm trong khoảng (a, b). Nhập a, b theo đúng thứ tự (phân số viết a/b hoặc số thập phân).
  - **Đáp án:** 1, 3/2
    1. p(x) = x^3 + x - 3: p(1) = -1 < 0 và p(2) = 7 > 0.
    2. Điểm giữa 1.5: p(1.5) = 3.375 + 1.5 - 3 = 1.875 > 0.
    3. p(1) < 0 < p(1.5), nên nghiệm nằm trong (1, 1.5): a = 1, b = 3/2.
- `gt_g3_khoang_nghiem` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^3 + 2x + 6 = 0 có đúng một nghiệm thực. Tìm số nguyên k sao cho nghiệm đó nằm trong khoảng (k, k + 1).
  - **Đáp án:** -2
    1. p(x) = x^3 + 2x + 6 tăng ngặt (p'(x) = 3x^2 + 2 > 0), nên chỉ đổi dấu một lần.
    2. Tính p tại các số nguyên liên tiếp cho tới khi thấy đổi dấu.
    3. p(-2) = -6 < 0 và p(-1) = 3 > 0.
    4. Theo định lý giá trị trung gian, nghiệm nằm trong (-2, -1): k = -2.
  - **Câu hỏi:** Phương trình x^3 + x - 25 = 0 có đúng một nghiệm thực. Tìm số nguyên k sao cho nghiệm đó nằm trong khoảng (k, k + 1).
  - **Đáp án:** 2
    1. p(x) = x^3 + x - 25 tăng ngặt (p'(x) = 3x^2 + 1 > 0), nên chỉ đổi dấu một lần.
    2. Tính p tại các số nguyên liên tiếp cho tới khi thấy đổi dấu.
    3. p(2) = -15 < 0 và p(3) = 5 > 0.
    4. Theo định lý giá trị trung gian, nghiệm nằm trong (2, 3): k = 2.
  - **Câu hỏi:** Phương trình x^3 + 2x + 7 = 0 có đúng một nghiệm thực. Tìm số nguyên k sao cho nghiệm đó nằm trong khoảng (k, k + 1).
  - **Đáp án:** -2
    1. p(x) = x^3 + 2x + 7 tăng ngặt (p'(x) = 3x^2 + 2 > 0), nên chỉ đổi dấu một lần.
    2. Tính p tại các số nguyên liên tiếp cho tới khi thấy đổi dấu.
    3. p(-2) = -5 < 0 và p(-1) = 4 > 0.
    4. Theo định lý giá trị trung gian, nghiệm nằm trong (-2, -1): k = -2.
