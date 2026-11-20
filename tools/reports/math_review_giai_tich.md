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

## Tầng 4: Đạo hàm và vi phân

52 dạng câu (41 câu viết tay, 11 bộ sinh câu); 52 chưa duyệt.

### Đạo hàm theo định nghĩa (`gt_t4_dinh_nghia_dao_ham`)

- `gt_t4_dn_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f xác định quanh a: nếu f liên tục tại a thì f có đạo hàm tại a.
  - **Đáp án:** Sai
    1. Xét f(x) = |x| tại a = 0: f liên tục tại 0.
    2. Tỉ số (f(h) - f(0))/h = |h|/h bằng 1 khi h > 0 và bằng -1 khi h < 0.
    3. Hai giới hạn một phía khác nhau, nên f'(0) không tồn tại: mệnh đề sai. (Chiều ngược lại mới đúng: có đạo hàm thì liên tục.)
- `gt_t4_dn_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Theo định nghĩa, đạo hàm f'(a) là giới hạn nào (khi giới hạn đó tồn tại hữu hạn)?
    - **(đúng)** Giới hạn của (f(a + h) - f(a)) / h khi h -> 0
    - Giới hạn của f(a + h) - f(a) khi h -> 0
    - Giới hạn của (f(a + h) - f(a - h)) / h khi h -> 0
    - Giới hạn của f(a + h) / h khi h -> 0
  - **Đáp án:** Giới hạn của (f(a + h) - f(a)) / h khi h -> 0
    1. Đạo hàm là giới hạn của tỉ số số gia: số gia của hàm chia cho số gia của biến.
    2. f(a + h) - f(a) không chia cho h thì dần tới 0 với mọi hàm liên tục, không cho biết độ dốc.
    3. (f(a + h) - f(a - h)) / h dần tới 2f'(a), gấp đôi đạo hàm, vì số gia của biến ở đây là 2h.
- `gt_t4_dn_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 + 3x. Tính giới hạn của (f(2 + h) - f(2)) / h khi h -> 0.
  - **Đáp án:** 7
    1. f(2 + h) = 4 + 4h + h^2 + 6 + 3h = 10 + 7h + h^2 và f(2) = 10.
    2. (f(2 + h) - f(2)) / h = (7h + h^2) / h = 7 + h.
    3. Cho h -> 0 được 7, chính là f'(2).
- `gt_g4_ti_so_gia` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -2x^3 + 3x. Tính giới hạn của (f(-3 + h) - f(-3)) / h khi h -> 0.
  - **Đáp án:** -51
    1. Giới hạn này chính là định nghĩa của f'(-3).
    2. Khai triển: f(-3 + h) - f(-3) = (-2)[(-3 + h)^3 - (-3)^3] + 3h = (-2)(3 . 9 . h + 3 . (-3) . h^2 + h^3) + 3h.
    3. Chia cho h rồi cho h -> 0, các số hạng còn h biến mất: (-2) . 3 . 9 + 3 = -51.
    4. Kiểm tra bằng quy tắc: f'(x) = -6x^2 + 3, f'(-3) = -51.
  - **Câu hỏi:** Cho f(x) = -3x^3 - 5x. Tính giới hạn của (f(-3 + h) - f(-3)) / h khi h -> 0.
  - **Đáp án:** -86
    1. Giới hạn này chính là định nghĩa của f'(-3).
    2. Khai triển: f(-3 + h) - f(-3) = (-3)[(-3 + h)^3 - (-3)^3] + (-5)h = (-3)(3 . 9 . h + 3 . (-3) . h^2 + h^3) + (-5)h.
    3. Chia cho h rồi cho h -> 0, các số hạng còn h biến mất: (-3) . 3 . 9 + (-5) = -86.
    4. Kiểm tra bằng quy tắc: f'(x) = -9x^2 - 5, f'(-3) = -86.
  - **Câu hỏi:** Cho f(x) = -2x^3 + 3x. Tính giới hạn của (f(2 + h) - f(2)) / h khi h -> 0.
  - **Đáp án:** -21
    1. Giới hạn này chính là định nghĩa của f'(2).
    2. Khai triển: f(2 + h) - f(2) = (-2)[(2 + h)^3 - 2^3] + 3h = (-2)(3 . 4 . h + 3 . 2 . h^2 + h^3) + 3h.
    3. Chia cho h rồi cho h -> 0, các số hạng còn h biến mất: (-2) . 3 . 4 + 3 = -21.
    4. Kiểm tra bằng quy tắc: f'(x) = -6x^2 + 3, f'(2) = -21.
- `gt_t4_dn_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tiếp tuyến của đồ thị y = x^3 - 2x tại điểm có hoành độ x = 1 có phương trình y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 1, -2
    1. Tiếp điểm: y(1) = 1 - 2 = -1.
    2. Hệ số góc: y' = 3x^2 - 2, nên y'(1) = 1.
    3. Tiếp tuyến: y = 1 . (x - 1) + (-1) = x - 2, nên p = 1, q = -2.
- `gt_t4_dn_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: dùng định nghĩa, tính đạo hàm của f(x) = 1/x tại x = 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. Tỉ số số gia: (f(2 + h) - f(2)) / h = (1/(2 + h) - 1/2) / h.
    2. 1/(2 + h) - 1/2 = (2 - (2 + h)) / (2(2 + h)) = -h / (2(2 + h)).
    3. Chia cho h: tỉ số bằng -1 / (2(2 + h)).
    4. Cho h -> 0: f'(2) = -1/2.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Cho h -> 0: f'(2) = -1/2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: khi h -> 0, mẫu 2(2 + h) dần tới 2 . 2 = 4, không phải 2.
    2. Đúng là f'(2) = -1/4.
    3. Kiểm tra bằng công thức (1/x)' = -1/x^2: -1/4.
- `gt_t4_dn_06` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x . |x| có đạo hàm tại x = 0 và f'(0) = 0.
  - **Đáp án:** Đúng
    1. Dùng định nghĩa vì |x| không có đạo hàm tại 0: (f(h) - f(0)) / h = h . |h| / h = |h| với h khác 0.
    2. |h| -> 0 khi h -> 0 từ cả hai phía.
    3. Vậy f'(0) tồn tại và bằng 0: mệnh đề đúng.
- `gt_t4_dn_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính đạo hàm của f(x) = sqrt(x) tại x = 4 bằng định nghĩa.
  - **Đáp án (thứ tự đúng):**
    1. Viết tỉ số số gia: (sqrt(4 + h) - 2) / h.
    2. Nhân cả tử và mẫu với liên hợp sqrt(4 + h) + 2.
    3. Tử thành (4 + h) - 4 = h, nên tỉ số bằng 1 / (sqrt(4 + h) + 2) với h khác 0.
    4. Cho h -> 0: f'(4) = 1 / (2 + 2) = 1/4.
  - **Lời giải:**
    1. Thay h = 0 ngay vào tỉ số sẽ ra dạng 0/0, nên phải khử trước.
    2. Nhân liên hợp làm mất căn ở tử và rút gọn được h.
    3. Kết quả 1/4 khớp với công thức (sqrt(x))' = 1 / (2 sqrt(x)) tại x = 4.
- `gt_g4_tiep_tuyen` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tiếp tuyến của đồ thị y = -2x^2 + 4x + 6 tại điểm có hoành độ x = 3 có phương trình y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -8, 24
    1. Tiếp điểm: y(3) = 0.
    2. Hệ số góc là đạo hàm tại 3: y' = -4x + 4, nên p = y'(3) = -8.
    3. Tiếp tuyến y = (-8)(x - 3) + 0 = -8x + 24.
    4. Vậy p = -8, q = 24.
  - **Câu hỏi:** Tiếp tuyến của đồ thị y = -3x^2 - 4x - 5 tại điểm có hoành độ x = -1 có phương trình y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 2, -2
    1. Tiếp điểm: y(-1) = -4.
    2. Hệ số góc là đạo hàm tại -1: y' = -6x - 4, nên p = y'(-1) = 2.
    3. Tiếp tuyến y = 2(x - (-1)) + (-4) = 2x - 2.
    4. Vậy p = 2, q = -2.
  - **Câu hỏi:** Tiếp tuyến của đồ thị y = -2x^2 + 4x + 2 tại điểm có hoành độ x = -2 có phương trình y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 12, 10
    1. Tiếp điểm: y(-2) = -14.
    2. Hệ số góc là đạo hàm tại -2: y' = -4x + 4, nên p = y'(-2) = 12.
    3. Tiếp tuyến y = 12(x - (-2)) + (-14) = 12x + 10.
    4. Vậy p = 12, q = 10.

### Quy tắc tính đạo hàm (`gt_t4_quy_tac_tinh`)

- `gt_t4_qt_01` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với đạo hàm của nó (xét trên tập xác định).
  - **Đáp án (ghép đúng):**
    - x^5 — 5x^4
    - sin x — cos x
    - cos x — -sin x
    - e^x — e^x
    - ln x — 1/x
  - **Lời giải:**
    1. (x^n)' = n . x^(n - 1): (x^5)' = 5x^4.
    2. (sin x)' = cos x còn (cos x)' = -sin x: chú ý dấu trừ.
    3. e^x là hàm có đạo hàm bằng chính nó; (ln x)' = 1/x với x > 0.
- `gt_t4_qt_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 + 1)(x^3 - 2x). Tính f'(2).
  - **Đáp án:** 66
    1. Quy tắc tích: (uv)' = u'v + uv' với u = x^2 + 1, v = x^3 - 2x.
    2. Tại x = 2: u = 5, u' = 2x = 4, v = 8 - 4 = 4, v' = 3x^2 - 2 = 10.
    3. f'(2) = 4 . 4 + 5 . 10 = 66.
- `gt_t4_qt_03` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính đạo hàm của f(x) = x^2 . ln x với x > 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt u = x^2 và v = ln x.
    2. u' = 2x và v' = 1/x.
    3. f'(x) = u' . v' = 2x . (1/x) = 2.   **<- bước sai đầu tiên**
    4. Vậy f'(x) = 2 với mọi x > 0.
  - **Đáp án:** Bước 3: f'(x) = u' . v' = 2x . (1/x) = 2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: đạo hàm của tích không phải tích các đạo hàm.
    2. Đúng là (uv)' = u'v + uv' = 2x ln x + x^2 . (1/x) = 2x ln x + x.
    3. Chẳng hạn f'(1) = 0 + 1 = 1, khác 2.
- `gt_t4_qt_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai hàm u, v khả vi tại x mà v(x) và v'(x) đều khác 0: (u/v)'(x) = u'(x) / v'(x).
  - **Đáp án:** Sai
    1. Quy tắc thương đúng là (u/v)' = (u'v - uv') / v^2.
    2. Phản ví dụ: u = x, v = x tại x = 1: u/v = 1 nên (u/v)' = 0, còn u'/v' = 1/1 = 1.
    3. Mệnh đề sai.
- `gt_g4_da_thuc` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -2x^3 + 3x^2 - 7x - 1. Tính f'(-3).
  - **Đáp án:** -79
    1. Đạo hàm từng số hạng: (x^n)' = n . x^(n - 1), hằng số có đạo hàm 0.
    2. f'(x) = -6x^2 + 6x - 7.
    3. f'(-3) = -79.
  - **Câu hỏi:** Cho f(x) = -4x^3 - 5x^2 - 7x + 2. Tính f'(3).
  - **Đáp án:** -145
    1. Đạo hàm từng số hạng: (x^n)' = n . x^(n - 1), hằng số có đạo hàm 0.
    2. f'(x) = -12x^2 - 10x - 7.
    3. f'(3) = -145.
  - **Câu hỏi:** Cho f(x) = -x^3 + 3x^2 + 8x - 5. Tính f'(-1).
  - **Đáp án:** -1
    1. Đạo hàm từng số hạng: (x^n)' = n . x^(n - 1), hằng số có đạo hàm 0.
    2. f'(x) = -3x^2 + 6x + 8.
    3. f'(-1) = -1.
- `gt_t4_qt_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x^2 + 1) / (x - 1). Tính f'(2).
  - **Đáp án:** -1
    1. Quy tắc thương với u = x^2 + 1, v = x - 1: f'(x) = (2x(x - 1) - (x^2 + 1)) / (x - 1)^2.
    2. Rút gọn tử: 2x^2 - 2x - x^2 - 1 = x^2 - 2x - 1.
    3. f'(2) = (4 - 4 - 1) / 1^2 = -1.
- `gt_t4_qt_06` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đạo hàm của f(x) = x^2 . e^x là gì?
    - **(đúng)** (x^2 + 2x) e^x
    - 2x e^x
    - x^2 e^x
    - (2x + 1) e^x
  - **Đáp án:** (x^2 + 2x) e^x
    1. Quy tắc tích: (x^2)' . e^x + x^2 . (e^x)'.
    2. = 2x e^x + x^2 e^x.
    3. Đặt e^x làm nhân tử chung: (x^2 + 2x) e^x.
- `gt_t4_qt_07` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính đạo hàm của f(x) = x / (x^2 + 1).
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt u = x, v = x^2 + 1; u' = 1, v' = 2x.
    2. f'(x) = (u . v' - u' . v) / v^2.   **<- bước sai đầu tiên**
    3. = (x . 2x - (x^2 + 1)) / (x^2 + 1)^2.
    4. = (x^2 - 1) / (x^2 + 1)^2.
  - **Đáp án:** Bước 2: f'(x) = (u . v' - u' . v) / v^2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai thứ tự: quy tắc thương là (u'v - uv') / v^2, đảo thứ tự làm đổi dấu cả kết quả.
    2. Đúng là f'(x) = ((x^2 + 1) - 2x^2) / (x^2 + 1)^2 = (1 - x^2) / (x^2 + 1)^2.
    3. Kiểm tra: f'(0) = 1 > 0, đúng là f tăng gần 0 (f(x) xấp xỉ x).
- `gt_t4_qt_08` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính đạo hàm của f(x) = x^3 . ln x với x > 0.
  - **Đáp án (thứ tự đúng):**
    1. Nhận ra f là tích u . v với u = x^3 và v = ln x.
    2. Tính u' = 3x^2 và v' = 1/x.
    3. Áp dụng (uv)' = u'v + uv': f'(x) = 3x^2 ln x + x^3 . (1/x).
    4. Rút gọn: f'(x) = 3x^2 ln x + x^2 = x^2(3 ln x + 1).
  - **Lời giải:**
    1. Nhận dạng phép toán ngoài cùng (ở đây là phép nhân) để chọn quy tắc.
    2. Tính đạo hàm từng thừa số rồi lắp vào quy tắc tích.
    3. Cuối cùng rút gọn: x^3 . (1/x) = x^2.
- `gt_g4_thuong` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (-3x + 3) / (-3x - 1). Tính f'(-3).
  - **Đáp án:** 3/16
    1. Quy tắc thương: (u/v)' = (u'v - uv') / v^2.
    2. u = -3x + 3, u' = -3; v = -3x - 1, v' = -3.
    3. Tử: (-3)(-3x - 1) - (-3)(-3x + 3) = 12 (các số hạng chứa x triệt tiêu).
    4. f'(x) = 12 / (-3x - 1)^2, nên f'(-3) = 12 / 8^2 = 3/16.
  - **Câu hỏi:** Cho f(x) = (-5x - 5) / (-3x). Tính f'(3).
  - **Đáp án:** -5/27
    1. Quy tắc thương: (u/v)' = (u'v - uv') / v^2.
    2. u = -5x - 5, u' = -5; v = -3x, v' = -3.
    3. Tử: (-5)(-3x) - (-3)(-5x - 5) = -15 (các số hạng chứa x triệt tiêu).
    4. f'(x) = -15 / (-3x)^2, nên f'(3) = -15 / (-9)^2 = -5/27.
  - **Câu hỏi:** Cho f(x) = (4x + 1) / (3x + 4). Tính f'(-3).
  - **Đáp án:** 13/25
    1. Quy tắc thương: (u/v)' = (u'v - uv') / v^2.
    2. u = 4x + 1, u' = 4; v = 3x + 4, v' = 3.
    3. Tử: 4(3x + 4) - 3(4x + 1) = 13 (các số hạng chứa x triệt tiêu).
    4. f'(x) = 13 / (3x + 4)^2, nên f'(-3) = 13 / (-5)^2 = 13/25.

### Quy tắc dây chuyền (`gt_t4_day_chuyen`)

- `gt_t4_dc_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đạo hàm của f(x) = sin(3x) là gì?
    - **(đúng)** 3cos(3x)
    - cos(3x)
    - -3cos(3x)
    - 3cos x
  - **Đáp án:** 3cos(3x)
    1. Hàm ngoài sin u, hàm trong u = 3x có u' = 3.
    2. f'(x) = cos(u) . u' = cos(3x) . 3.
    3. Quên nhân 3 sẽ ra cos(3x), một lỗi rất hay gặp.
- `gt_t4_dc_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (2x - 1)^5. Tính f'(1).
  - **Đáp án:** 10
    1. f'(x) = 5(2x - 1)^4 . (2x - 1)' = 5(2x - 1)^4 . 2 = 10(2x - 1)^4.
    2. Tại x = 1: 2 . 1 - 1 = 1.
    3. f'(1) = 10 . 1^4 = 10.
- `gt_t4_dc_03` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: cho f(x) = e^(x^2 + 3x), tính f'(0).
  - **Lời giải đưa ra (có một bước sai):**
    1. f là hàm hợp: hàm ngoài e^u, hàm trong u = x^2 + 3x.
    2. Đạo hàm của e^u theo u là e^u.
    3. Vậy f'(x) = e^(x^2 + 3x).   **<- bước sai đầu tiên**
    4. f'(0) = e^0 = 1.
  - **Đáp án:** Bước 3: Vậy f'(x) = e^(x^2 + 3x).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 quên nhân đạo hàm của hàm trong u' = 2x + 3.
    2. Đúng là f'(x) = (2x + 3) e^(x^2 + 3x).
    3. f'(0) = 3 . e^0 = 3.
- `gt_t4_dc_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số thực x, đạo hàm của ln(x^2 + 1) là 2x / (x^2 + 1).
  - **Đáp án:** Đúng
    1. x^2 + 1 > 0 với mọi x, nên ln(x^2 + 1) xác định trên cả R.
    2. (ln u)' = u'/u với u = x^2 + 1, u' = 2x.
    3. Được 2x / (x^2 + 1): mệnh đề đúng.
- `gt_g4_day_chuyen_tf` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (-2x^2 - 3)^3. Khi đó f'(-2) = 2904.
  - **Đáp án:** Đúng
    1. Hàm trong u = -2x^2 - 3 có u' = -4x; tại x = -2: u = -11, u' = 8.
    2. f'(-2) = 3 . u^2 . u' = 3 . (-11)^2 . 8 = 2904.
    3. Số đã cho đúng bằng f'(-2): mệnh đề đúng.
  - **Câu hỏi:** Cho f(x) = (-3x^2 - 3)^2. Khi đó f'(1) = -12.
  - **Đáp án:** Sai
    1. Hàm trong u = -3x^2 - 3 có u' = -6x; tại x = 1: u = -6, u' = -6.
    2. f'(1) = 2 . u . u' = 2 . (-6) . (-6) = 72.
    3. Số -12 là kết quả khi quên nhân đạo hàm trong u': mệnh đề sai.
  - **Câu hỏi:** Cho f(x) = (-2x^2 + 4)^2. Khi đó f'(1) = 4.
  - **Đáp án:** Sai
    1. Hàm trong u = -2x^2 + 4 có u' = -4x; tại x = 1: u = 2, u' = -4.
    2. f'(1) = 2 . u . u' = 2 . 2 . (-4) = -16.
    3. Số 4 là kết quả khi quên nhân đạo hàm trong u': mệnh đề sai.
- `gt_g4_luy_thua_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (-2x - 3)^4. Tính f'(-2).
  - **Đáp án:** -8
    1. Hàm ngoài u^4, hàm trong u = -2x - 3 có u' = -2.
    2. Quy tắc dây chuyền: f'(x) = 4(-2x - 3)^3 . (-2).
    3. Tại x = -2: u = 1, nên f'(-2) = 4 . 1^3 . (-2) = -8.
  - **Câu hỏi:** Cho f(x) = (-3x - 3)^2. Tính f'(0).
  - **Đáp án:** 18
    1. Hàm ngoài u^2, hàm trong u = -3x - 3 có u' = -3.
    2. Quy tắc dây chuyền: f'(x) = 2(-3x - 3)^1 . (-3).
    3. Tại x = 0: u = -3, nên f'(0) = 2 . (-3)^1 . (-3) = 18.
  - **Câu hỏi:** Cho f(x) = (-2x + 4)^3. Tính f'(0).
  - **Đáp án:** -96
    1. Hàm ngoài u^3, hàm trong u = -2x + 4 có u' = -2.
    2. Quy tắc dây chuyền: f'(x) = 3(-2x + 4)^2 . (-2).
    3. Tại x = 0: u = 4, nên f'(0) = 3 . 4^2 . (-2) = -96.
- `gt_t4_dc_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = sqrt(x^2 + 9). Tính f'(4).
  - **Đáp án:** 4/5
    1. (sqrt(u))' = u' / (2 sqrt(u)) với u = x^2 + 9, u' = 2x.
    2. f'(x) = 2x / (2 sqrt(x^2 + 9)) = x / sqrt(x^2 + 9).
    3. f'(4) = 4 / sqrt(25) = 4/5.
- `gt_t4_dc_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = sin^2(3x), tức là (sin(3x))^2. Tính f'(pi/12).
  - **Đáp án:** 3
    1. Ba lớp: bình phương, rồi sin, rồi 3x. f'(x) = 2 sin(3x) . cos(3x) . 3.
    2. Dùng 2 sin a cos a = sin(2a): f'(x) = 3 sin(6x).
    3. f'(pi/12) = 3 sin(pi/2) = 3.
- `gt_t4_dc_07` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính đạo hàm của f(x) = cos(x^3).
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm ngoài cos u, hàm trong u = x^3.
    2. Đạo hàm của cos u theo u là sin u.   **<- bước sai đầu tiên**
    3. Đạo hàm của hàm trong: u' = 3x^2.
    4. f'(x) = 3x^2 . sin(x^3).
  - **Đáp án:** Bước 2: Đạo hàm của cos u theo u là sin u.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai dấu: (cos u)' = -sin u.
    2. Đúng là f'(x) = -3x^2 sin(x^3).
    3. Bước 3 thì đúng: lần này hàm trong đã được nhân vào.
- `gt_t4_dc_08` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với đạo hàm của nó (mỗi hàm lấy trên tập xác định).
  - **Đáp án (ghép đúng):**
    - e^(2x) — 2e^(2x)
    - sin(x^2) — 2x cos(x^2)
    - ln(3x) — 1/x
    - (x^2 + 1)^3 — 6x(x^2 + 1)^2
  - **Lời giải:**
    1. e^(2x): nhân thêm đạo hàm của 2x là 2.
    2. sin(x^2): cos(x^2) nhân với (x^2)' = 2x.
    3. ln(3x): 3 / (3x) = 1/x (cũng thấy được từ ln(3x) = ln 3 + ln x).
    4. (x^2 + 1)^3: 3(x^2 + 1)^2 . 2x = 6x(x^2 + 1)^2.
- `gt_t4_dc_09` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho g khả vi tại 1 với g(1) = 2, g'(1) = 3, và f khả vi tại 2 với f'(2) = 5. Đạo hàm của h(x) = f(g(x)) tại x = 1 bằng 15.
  - **Đáp án:** Đúng
    1. Quy tắc dây chuyền: h'(1) = f'(g(1)) . g'(1).
    2. f' phải lấy tại g(1) = 2, không phải tại 1: f'(2) = 5.
    3. h'(1) = 5 . 3 = 15: mệnh đề đúng.
- `gt_g4_ln_hop` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = ln(x^2 + 4x + 9). Tính f'(3).
  - **Đáp án:** 1/3
    1. (ln u)' = u' / u.
    2. u = x^2 + 4x + 9, u' = 2x + 4.
    3. Tại x = 3: u = 30 > 0 và u' = 10.
    4. f'(3) = 10 / 30 = 1/3.
  - **Câu hỏi:** Cho f(x) = ln(x^2 - 4x - 3). Tính f'(-1).
  - **Đáp án:** -3
    1. (ln u)' = u' / u.
    2. u = x^2 - 4x - 3, u' = 2x - 4.
    3. Tại x = -1: u = 2 > 0 và u' = -6.
    4. f'(-1) = -6 / 2 = -3.
  - **Câu hỏi:** Cho f(x) = ln(2x^2 + 4x + 3). Tính f'(2).
  - **Đáp án:** 12/19
    1. (ln u)' = u' / u.
    2. u = 2x^2 + 4x + 3, u' = 4x + 4.
    3. Tại x = 2: u = 19 > 0 và u' = 12.
    4. f'(2) = 12 / 19.

### Đạo hàm của hàm ngược và hàm cho bởi tham số (`gt_t4_ham_nguoc_tham_so`)

- `gt_t4_nt_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 + x tăng ngặt trên R. Tính (f^(-1))'(2).
  - **Đáp án:** 1/4
    1. Tìm x0 với f(x0) = 2: f(1) = 1 + 1 = 2, nên x0 = 1.
    2. f'(x) = 3x^2 + 1, nên f'(1) = 4.
    3. (f^(-1))'(2) = 1 / f'(1) = 1/4.
- `gt_t4_nt_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đạo hàm của y = arctan x (x thuộc R) là gì?
    - **(đúng)** 1 / (1 + x^2)
    - -1 / (1 + x^2)
    - 1 / sqrt(1 - x^2)
    - 1 / cos^2 x
  - **Đáp án:** 1 / (1 + x^2)
    1. y = arctan x nghĩa là x = tan y với y trong (-pi/2, pi/2).
    2. Đạo hàm hàm ngược: y' = 1 / (tan y)' = cos^2 y = 1 / (1 + tan^2 y).
    3. Thay tan y = x: y' = 1 / (1 + x^2).
- `gt_t4_nt_03` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: đường cong x = t^2 + 1, y = t^3; tính dy/dx tại t = 2.
  - **Lời giải đưa ra (có một bước sai):**
    1. x'(t) = 2t và y'(t) = 3t^2.
    2. dy/dx = x'(t) / y'(t) = 2t / (3t^2).   **<- bước sai đầu tiên**
    3. Tại t = 2: dy/dx = 4/12 = 1/3.
  - **Đáp án:** Bước 2: dy/dx = x'(t) / y'(t) = 2t / (3t^2).
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 đảo ngược tỉ số: dy/dx = y'(t) / x'(t).
    2. Tại t = 2: y' = 12, x' = 4.
    3. dy/dx = 12/4 = 3.
- `gt_g4_tham_so` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đường cong cho bởi x = -2t^2 - 3t, y = t^3 - 4t. Tính dy/dx tại t = 1.
  - **Đáp án:** 1/7
    1. dy/dx = y'(t) / x'(t) khi x'(t) khác 0.
    2. x'(t) = -4t - 3, y'(t) = 3t^2 - 4.
    3. Tại t = 1: x' = -7, y' = -1.
    4. dy/dx = -1 / (-7) = 1/7.
  - **Câu hỏi:** Đường cong cho bởi x = -3t^2 - 3t, y = -2t^3. Tính dy/dx tại t = -1.
  - **Đáp án:** -2
    1. dy/dx = y'(t) / x'(t) khi x'(t) khác 0.
    2. x'(t) = -6t - 3, y'(t) = -6t^2.
    3. Tại t = -1: x' = 3, y' = -6.
    4. dy/dx = -6 / 3 = -2.
  - **Câu hỏi:** Đường cong cho bởi x = -2t^2 + 4t, y = -t^3. Tính dy/dx tại t = 2.
  - **Đáp án:** 3
    1. dy/dx = y'(t) / x'(t) khi x'(t) khác 0.
    2. x'(t) = -4t + 4, y'(t) = -3t^2.
    3. Tại t = 2: x' = -4, y' = -12.
    4. dy/dx = -12 / (-4) = 3.
- `gt_t4_nt_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đường cong cho bởi x = t^2 - 2t, y = t^3 - 3t. Tiếp tuyến tại điểm ứng với t = 2 có phương trình y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 9/2, 2
    1. Điểm ứng với t = 2: x = 4 - 4 = 0, y = 8 - 6 = 2.
    2. x'(t) = 2t - 2 = 2 và y'(t) = 3t^2 - 3 = 9 tại t = 2, nên hệ số góc dy/dx = 9/2.
    3. Tiếp tuyến qua (0, 2): y = (9/2)x + 2, nên p = 9/2, q = 2.
- `gt_t4_nt_05` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đạo hàm của y = arcsin(2x) với |x| < 1/2 là gì?
    - **(đúng)** 2 / sqrt(1 - 4x^2)
    - 1 / sqrt(1 - 4x^2)
    - 2 / sqrt(1 - x^2)
    - 2 / (1 + 4x^2)
  - **Đáp án:** 2 / sqrt(1 - 4x^2)
    1. (arcsin u)' = u' / sqrt(1 - u^2), công thức có được từ đạo hàm hàm ngược của sin.
    2. Với u = 2x: u' = 2 và u^2 = 4x^2.
    3. y' = 2 / sqrt(1 - 4x^2).
- `gt_t4_nt_06` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^5 + 2x + 1 tăng ngặt trên R. Sắp xếp các bước tính (f^(-1))'(4).
  - **Đáp án (thứ tự đúng):**
    1. Tìm x0 với f(x0) = 4: thử x0 = 1, f(1) = 1 + 2 + 1 = 4.
    2. Tính f'(x) = 5x^4 + 2, nên f'(1) = 7.
    3. f'(1) khác 0 nên dùng được (f^(-1))'(4) = 1 / f'(1).
    4. Kết quả (f^(-1))'(4) = 1/7.
  - **Lời giải:**
    1. Không cần tìm công thức của f^(-1): chỉ cần điểm x0 mà f(x0) = 4.
    2. Đạo hàm hàm ngược tại y0 = f(x0) là 1 / f'(x0), với điều kiện f'(x0) khác 0.
- `gt_t4_nt_07` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: f(x) = x^3 + 2x - 1 tăng ngặt trên R, tính (f^(-1))'(2).
  - **Lời giải đưa ra (có một bước sai):**
    1. f(1) = 1 + 2 - 1 = 2, nên f^(-1)(2) = 1.
    2. f'(x) = 3x^2 + 2.
    3. (f^(-1))'(2) = 1 / f'(2).   **<- bước sai đầu tiên**
    4. f'(2) = 14, nên (f^(-1))'(2) = 1/14.
  - **Đáp án:** Bước 3: (f^(-1))'(2) = 1 / f'(2).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: f' phải lấy tại x0 = f^(-1)(2) = 1, không phải tại 2.
    2. (f^(-1))'(2) = 1 / f'(1) = 1 / 5.
- `gt_t4_nt_08` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với đường cong x = t^2, y = t^3 (t > 0), đạo hàm cấp hai d^2y/dx^2 bằng y''(t) / x''(t) = 3t.
  - **Đáp án:** Sai
    1. dy/dx = 3t^2 / (2t) = 3t/2, coi như một hàm của t.
    2. Lấy đạo hàm theo x: d^2y/dx^2 = (3t/2)'(t) / x'(t) = (3/2) / (2t) = 3 / (4t).
    3. 3/(4t) khác 3t (chẳng hạn t = 1 cho 3/4 và 3): mệnh đề sai. Không được chia y'' cho x''.
- `gt_g4_nguoc` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 + 2x + 3 tăng ngặt trên R nên có hàm ngược f^(-1). Tính (f^(-1))'(36).
  - **Đáp án:** 1/29
    1. Tìm x0 với f(x0) = 36: thử x0 = 3, f(3) = 36.
    2. f'(x) = 3x^2 + 2, nên f'(3) = 29 (khác 0).
    3. (f^(-1))'(36) = 1 / f'(3) = 1/29.
  - **Câu hỏi:** Hàm f(x) = x^3 + x - 5 tăng ngặt trên R nên có hàm ngược f^(-1). Tính (f^(-1))'(-35).
  - **Đáp án:** 1/28
    1. Tìm x0 với f(x0) = -35: thử x0 = -3, f(-3) = -35.
    2. f'(x) = 3x^2 + 1, nên f'(-3) = 28 (khác 0).
    3. (f^(-1))'(-35) = 1 / f'(-3) = 1/28.
  - **Câu hỏi:** Hàm f(x) = x^3 + 2x + 3 tăng ngặt trên R nên có hàm ngược f^(-1). Tính (f^(-1))'(6).
  - **Đáp án:** 1/5
    1. Tìm x0 với f(x0) = 6: thử x0 = 1, f(1) = 6.
    2. f'(x) = 3x^2 + 2, nên f'(1) = 5 (khác 0).
    3. (f^(-1))'(6) = 1 / f'(1) = 1/5.

### Vi phân và đạo hàm cấp cao (`gt_t4_vi_phan_cap_cao`)

- `gt_t4_vp_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^4 - 3x^2. Tính f''(1).
  - **Đáp án:** 6
    1. f'(x) = 4x^3 - 6x.
    2. f''(x) = 12x^2 - 6.
    3. f''(1) = 12 - 6 = 6.
- `gt_t4_vp_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vi phân của hàm y = x^3 là gì?
    - **(đúng)** dy = 3x^2 dx
    - dy = 3x^2
    - dy = x^3 dx
    - dy = 3x dx
  - **Đáp án:** dy = 3x^2 dx
    1. Vi phân: dy = y'(x) dx.
    2. y' = 3x^2, nên dy = 3x^2 dx.
    3. Thiếu dx thì đó là đạo hàm chứ không phải vi phân.
- `gt_t4_vp_03` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: dùng vi phân tính gần đúng sqrt(4.1).
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt f(x) = sqrt(x), x0 = 4, dx = 0.1.
    2. f'(x) = 1 / (2 sqrt(x)), nên f'(4) = 1/4.
    3. sqrt(4.1) xấp xỉ f(4) + f'(4) = 2 + 1/4 = 2.25.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: sqrt(4.1) xấp xỉ f(4) + f'(4) = 2 + 1/4 = 2.25.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 quên nhân với dx: công thức là f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx.
    2. sqrt(4.1) xấp xỉ 2 + (1/4) . 0.1 = 2.025.
    3. Kiểm tra: 2.025^2 = 4.100625, rất gần 4.1; còn 2.25^2 = 5.0625.
- `gt_t4_vp_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số nguyên n >= 1, đạo hàm cấp n của e^(2x) là 2^n e^(2x).
  - **Đáp án:** Đúng
    1. Mỗi lần lấy đạo hàm e^(2x) lại nhân thêm 2 (quy tắc dây chuyền).
    2. Sau n lần được 2 . 2 ... 2 = 2^n.
    3. Vậy (e^(2x))^(n) = 2^n e^(2x): mệnh đề đúng.
- `gt_g4_xap_xi` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng vi phân của f(x) = sqrt(x) tại x0 = 9 để tính gần đúng sqrt(10). Nhập kết quả (phân số a/b).
  - **Đáp án:** 19/6
    1. f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx, với x0 = 9 và dx = 1.
    2. f(x0) = 3; f'(x) = 1 / (2 sqrt(x)), nên f'(9) = 1/6.
    3. sqrt(10) xấp xỉ 3 + 1/6 . 1 = 19/6.
  - **Câu hỏi:** Dùng vi phân của f(x) = sqrt(x) tại x0 = 9 để tính gần đúng sqrt(6). Nhập kết quả (phân số a/b).
  - **Đáp án:** 5/2
    1. f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx, với x0 = 9 và dx = -3.
    2. f(x0) = 3; f'(x) = 1 / (2 sqrt(x)), nên f'(9) = 1/6.
    3. sqrt(6) xấp xỉ 3 + 1/6 . (-3) = 5/2.
  - **Câu hỏi:** Dùng vi phân của f(x) = sqrt(x) tại x0 = 100 để tính gần đúng sqrt(98). Nhập kết quả (phân số a/b).
  - **Đáp án:** 99/10
    1. f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx, với x0 = 100 và dx = -2.
    2. f(x0) = 10; f'(x) = 1 / (2 sqrt(x)), nên f'(100) = 1/20.
    3. sqrt(98) xấp xỉ 10 + 1/20 . (-2) = 99/10.
- `gt_t4_vp_05` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x . e^(2x). Tính f''(0).
  - **Đáp án:** 4
    1. f'(x) = e^(2x) + 2x e^(2x) = (1 + 2x) e^(2x).
    2. f''(x) = 2e^(2x) + (1 + 2x) . 2e^(2x) = (4 + 4x) e^(2x).
    3. f''(0) = 4.
- `gt_t4_vp_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 1 / (1 - x). Tính đạo hàm cấp năm f^(5)(0).
  - **Đáp án:** 120
    1. f(x) = (1 - x)^(-1); f'(x) = (1 - x)^(-2), f''(x) = 2(1 - x)^(-3): mỗi lần hai dấu trừ triệt tiêu.
    2. Tổng quát f^(n)(x) = n! / (1 - x)^(n + 1).
    3. f^(5)(0) = 5! = 120.
- `gt_t4_vp_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính gần đúng (1.02)^10 bằng vi phân.
  - **Đáp án (thứ tự đúng):**
    1. Đặt f(x) = x^10, x0 = 1, dx = 0.02.
    2. Tính f'(x) = 10x^9, nên f'(1) = 10.
    3. Dùng f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx.
    4. (1.02)^10 xấp xỉ 1 + 10 . 0.02 = 1.2.
  - **Lời giải:**
    1. Chọn x0 gần 1.02 mà f(x0) tính nhẩm được: x0 = 1.
    2. Vi phân thay số gia của hàm bằng f'(x0) . dx.
    3. Giá trị đúng là khoảng 1.219, nên 1.2 là xấp xỉ tốt khi dx nhỏ.
- `gt_t4_vp_08` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai hàm u, v có đạo hàm cấp hai trên R: (uv)'' = u''v + uv''.
  - **Đáp án:** Sai
    1. Lấy đạo hàm (uv)' = u'v + uv' thêm một lần: (uv)'' = u''v + 2u'v' + uv''.
    2. Mệnh đề bỏ mất số hạng 2u'v'.
    3. Phản ví dụ u = v = x: (x^2)'' = 2, còn u''v + uv'' = 0.
- `gt_t4_vp_09` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với đạo hàm cấp n của nó (n >= 1, xét x > 0).
  - **Đáp án (ghép đúng):**
    - e^(3x) — 3^n e^(3x)
    - x^n — n!
    - 1/x — (-1)^n n! / x^(n + 1)
    - ln x — (-1)^(n - 1) (n - 1)! / x^n
  - **Lời giải:**
    1. e^(3x): mỗi lần nhân thêm 3.
    2. x^n: sau n lần chỉ còn n(n - 1)...1 = n!.
    3. 1/x = x^(-1): mỗi lần đổi dấu và nhân thêm số mũ.
    4. ln x có đạo hàm 1/x, nên đạo hàm cấp n của ln x là đạo hàm cấp n - 1 của 1/x.
- `gt_g4_cap_cao` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = 1 / (x + 1). Tính đạo hàm cấp 2 f^(2)(0).
  - **Đáp án:** 2
    1. Viết f(x) = (x + 1)^(-1). Mỗi lần lấy đạo hàm, số mũ giảm 1 và xuất hiện thêm một thừa số bằng số mũ cũ.
    2. f^(n)(x) = (-1)^n . n! / (x + 1)^(n + 1).
    3. Với n = 2, x = 0: 1 . 2 / 1^3 = 2.
  - **Câu hỏi:** Cho f(x) = 1 / (x - 3). Tính đạo hàm cấp 2 f^(2)(1).
  - **Đáp án:** -1/4
    1. Viết f(x) = (x - 3)^(-1). Mỗi lần lấy đạo hàm, số mũ giảm 1 và xuất hiện thêm một thừa số bằng số mũ cũ.
    2. f^(n)(x) = (-1)^n . n! / (x - 3)^(n + 1).
    3. Với n = 2, x = 1: 1 . 2 / (-2)^3 = -1/4.
  - **Câu hỏi:** Cho f(x) = 1 / (x + 1). Tính đạo hàm cấp 3 f^(3)(0).
  - **Đáp án:** -6
    1. Viết f(x) = (x + 1)^(-1). Mỗi lần lấy đạo hàm, số mũ giảm 1 và xuất hiện thêm một thừa số bằng số mũ cũ.
    2. f^(n)(x) = (-1)^n . n! / (x + 1)^(n + 1).
    3. Với n = 3, x = 0: (-1) . 6 / 1^4 = -6.

## Tầng 5: Định lý về hàm khả vi, khai triển Taylor và quy tắc L'Hospital

55 dạng câu (44 câu viết tay, 11 bộ sinh câu); 55 chưa duyệt.

### Định lý Rolle, Lagrange và Cauchy (`gt_t5_rolle_lagrange`)

- `gt_t5_rl_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = |x| có f(-1) = f(1), nên theo định lý Rolle có c thuộc (-1, 1) với f'(c) = 0.
  - **Đáp án:** Sai
    1. Định lý Rolle còn cần f khả vi trên cả khoảng (-1, 1).
    2. |x| không có đạo hàm tại 0.
    3. Thật vậy f'(x) = -1 khi x < 0 và = 1 khi x > 0: không có c nào với f'(c) = 0. Mệnh đề sai.
- `gt_t5_rl_02` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Áp dụng định lý Lagrange cho f(x) = x^3 trên đoạn [-1, 2]. Tìm điểm c thuộc (-1, 2) mà định lý nói tới.
  - **Đáp án:** 1
    1. (f(2) - f(-1)) / (2 - (-1)) = (8 + 1) / 3 = 3.
    2. f'(c) = 3c^2 = 3 cho c = 1 hoặc c = -1.
    3. c phải nằm trong khoảng mở (-1, 2): loại -1 (đầu mút), còn c = 1.
- `gt_t5_rl_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào sau đây thỏa mọi giả thiết của định lý Rolle trên đoạn [0, 2]?
    - **(đúng)** f(x) = x^2 - 2x
    - f(x) = |x - 1|
    - f(x) = 1 / (x - 1)
    - f(x) = x^2
  - **Đáp án:** f(x) = x^2 - 2x
    1. x^2 - 2x là đa thức (liên tục, khả vi) và f(0) = f(2) = 0: thỏa.
    2. |x - 1| không khả vi tại 1; 1/(x - 1) không xác định tại 1 nên không liên tục trên [0, 2].
    3. x^2 có f(0) = 0 khác f(2) = 4.
- `gt_t5_rl_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh phương trình x^3 + x - 1 = 0 có nhiều nhất một nghiệm thực.
  - **Đáp án (thứ tự đúng):**
    1. Giả sử phương trình có hai nghiệm a < b.
    2. f(x) = x^3 + x - 1 liên tục trên [a, b], khả vi trên (a, b), và f(a) = f(b) = 0.
    3. Theo định lý Rolle có c thuộc (a, b) với f'(c) = 0.
    4. Nhưng f'(c) = 3c^2 + 1 > 0, mâu thuẫn; vậy có nhiều nhất một nghiệm.
  - **Lời giải:**
    1. Đây là cách dùng Rolle để chứng minh tính duy nhất: hai nghiệm sinh ra một nghiệm của f'.
    2. f' luôn dương nên không thể có nghiệm, do đó không thể có hai nghiệm của f.
- `gt_t5_rl_09` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên đồ thị y = sqrt(x), tìm hoành độ c thuộc (1, 9) của điểm mà tiếp tuyến tại đó song song với dây cung nối hai điểm (1, 1) và (9, 3).
  - **Đáp án:** 4
    1. Đây chính là định lý Lagrange cho f(x) = sqrt(x) trên [1, 9]: hệ số góc dây cung (3 - 1) / (9 - 1) = 1/4.
    2. f'(c) = 1 / (2 sqrt(c)) = 1/4 cho sqrt(c) = 2.
    3. c = 4, nằm trong (1, 9).
- `gt_g5_lagrange` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Áp dụng định lý Lagrange cho f(x) = 2x^2 - 4x - 2 trên đoạn [-3, 5]. Tìm điểm c thuộc (-3, 5) mà định lý nói tới.
  - **Đáp án:** 1
    1. Cần c với f'(c) = (f(5) - f(-3)) / (5 - (-3)).
    2. f(5) = 28, f(-3) = 28, nên vế phải bằng 0.
    3. f'(c) = 4c + (-4) = 0 cho c = 1, đúng là trung điểm của đoạn.
    4. c = 1 nằm trong (-3, 5).
  - **Câu hỏi:** Áp dụng định lý Lagrange cho f(x) = -3x^2 - 4x - 1 trên đoạn [-2, 4]. Tìm điểm c thuộc (-2, 4) mà định lý nói tới.
  - **Đáp án:** 1
    1. Cần c với f'(c) = (f(4) - f(-2)) / (4 - (-2)).
    2. f(4) = -65, f(-2) = -5, nên vế phải bằng -10.
    3. f'(c) = -6c + (-4) = -10 cho c = 1, đúng là trung điểm của đoạn.
    4. c = 1 nằm trong (-2, 4).
  - **Câu hỏi:** Áp dụng định lý Lagrange cho f(x) = 2x^2 + 3x - 4 trên đoạn [1, 5]. Tìm điểm c thuộc (1, 5) mà định lý nói tới.
  - **Đáp án:** 3
    1. Cần c với f'(c) = (f(5) - f(1)) / (5 - 1).
    2. f(5) = 61, f(1) = 1, nên vế phải bằng 15.
    3. f'(c) = 4c + 3 = 15 cho c = 3, đúng là trung điểm của đoạn.
    4. c = 3 nằm trong (1, 5).
- `gt_g5_rolle_tf` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^2 + 4x + 1 thỏa mọi giả thiết của định lý Rolle trên đoạn [-3, -1].
  - **Đáp án:** Đúng
    1. Định lý Rolle cần: f liên tục trên [a, b], khả vi trên (a, b), và f(a) = f(b).
    2. f là đa thức nên hai điều đầu luôn đúng. Còn lại: f(-3) = -2, f(-1) = -2.
    3. Hai giá trị bằng nhau: f thỏa mọi giả thiết, mệnh đề đúng.
  - **Câu hỏi:** Hàm f(x) = x^2 + 8x - 4 thỏa mọi giả thiết của định lý Rolle trên đoạn [-5, -3].
  - **Đáp án:** Đúng
    1. Định lý Rolle cần: f liên tục trên [a, b], khả vi trên (a, b), và f(a) = f(b).
    2. f là đa thức nên hai điều đầu luôn đúng. Còn lại: f(-5) = -19, f(-3) = -19.
    3. Hai giá trị bằng nhau: f thỏa mọi giả thiết, mệnh đề đúng.
  - **Câu hỏi:** Hàm f(x) = x^2 - 2x + 3 thỏa mọi giả thiết của định lý Rolle trên đoạn [-2, 3].
  - **Đáp án:** Sai
    1. Định lý Rolle cần: f liên tục trên [a, b], khả vi trên (a, b), và f(a) = f(b).
    2. f là đa thức nên hai điều đầu luôn đúng. Còn lại: f(-2) = 11, f(3) = 6.
    3. Hai giá trị khác nhau: thiếu giả thiết f(a) = f(b), mệnh đề sai.
- `gt_t5_rl_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: dùng định lý Lagrange so sánh e^x với 1 + x khi x > 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Với x > 0, áp dụng định lý Lagrange cho f(t) = e^t trên [0, x].
    2. Có c thuộc (0, x) với e^x - 1 = e^c . x.
    3. Vì c > 0 nên e^c < 1.   **<- bước sai đầu tiên**
    4. Suy ra e^x - 1 < x, tức e^x < 1 + x.
  - **Đáp án:** Bước 3: Vì c > 0 nên e^c < 1.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: e^t tăng, nên c > 0 cho e^c > e^0 = 1.
    2. Do đó e^x - 1 = e^c . x > x, tức e^x > 1 + x với mọi x > 0.
    3. Kiểm tra: x = 1 cho e xấp xỉ 2.718 > 2.
- `gt_t5_rl_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f khả vi trên R, f(1) = 2 và 3 <= f'(x) <= 5 với mọi x. Theo định lý Lagrange, f(5) chắc chắn nằm trong đoạn [m, M]. Nhập m, M (đoạn hẹp nhất suy ra được) theo đúng thứ tự.
  - **Đáp án:** 14, 22
    1. Lagrange trên [1, 5]: f(5) - f(1) = f'(c) . (5 - 1) = 4f'(c) với c nào đó trong (1, 5).
    2. 3 <= f'(c) <= 5 nên 12 <= f(5) - 2 <= 20, tức 14 <= f(5) <= 22.
    3. Hai đầu đạt được, chẳng hạn f(x) = 3x - 1 cho f(5) = 14 và f(x) = 5x - 3 cho f(5) = 22: m = 14, M = 22.
- `gt_t5_rl_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f khả vi trên R mà |f'(x)| <= 2 với mọi x, ta có |f(5) - f(1)| <= 8.
  - **Đáp án:** Đúng
    1. Lagrange trên [1, 5]: f(5) - f(1) = f'(c) . 4 với c thuộc (1, 5).
    2. |f'(c)| <= 2 nên |f(5) - f(1)| <= 2 . 4 = 8.
    3. Mệnh đề đúng với mọi hàm như vậy.
- `gt_t5_rl_08` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = (x - 1)(x - 2)(x - 3)(x - 4). Phương trình f'(x) = 0 có bao nhiêu nghiệm thực?
    - **(đúng)** Đúng 3 nghiệm, mỗi khoảng (1, 2), (2, 3), (3, 4) có một nghiệm
    - Đúng 4 nghiệm
    - Đúng 2 nghiệm
    - Không có nghiệm thực
  - **Đáp án:** Đúng 3 nghiệm, mỗi khoảng (1, 2), (2, 3), (3, 4) có một nghiệm
    1. f(1) = f(2) = f(3) = f(4) = 0; Rolle trên [1, 2], [2, 3], [3, 4] cho mỗi khoảng ít nhất một nghiệm của f'.
    2. f là đa thức bậc 4 nên f' bậc 3, có nhiều nhất 3 nghiệm.
    3. Vậy f' có đúng 3 nghiệm, mỗi khoảng một nghiệm.
- `gt_g5_cauchy` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Áp dụng định lý Cauchy cho f(x) = x^3 và g(x) = x^2 trên đoạn [2, 7]. Tìm điểm c thuộc (2, 7) mà định lý nói tới.
  - **Đáp án:** 134/27
    1. Cần c với (f(b) - f(a)) / (g(b) - g(a)) = f'(c) / g'(c), và g'(x) = 2x khác 0 trên khoảng.
    2. Vế trái: (343 - 8) / (49 - 4) = 67/9.
    3. Vế phải: 3c^2 / (2c) = 3c/2.
    4. 3c/2 = 67/9 cho c = 134/27, nằm trong (2, 7).
  - **Câu hỏi:** Áp dụng định lý Cauchy cho f(x) = x^3 và g(x) = x^2 trên đoạn [1, 2]. Tìm điểm c thuộc (1, 2) mà định lý nói tới.
  - **Đáp án:** 14/9
    1. Cần c với (f(b) - f(a)) / (g(b) - g(a)) = f'(c) / g'(c), và g'(x) = 2x khác 0 trên khoảng.
    2. Vế trái: (8 - 1) / (4 - 1) = 7/3.
    3. Vế phải: 3c^2 / (2c) = 3c/2.
    4. 3c/2 = 7/3 cho c = 14/9, nằm trong (1, 2).
  - **Câu hỏi:** Áp dụng định lý Cauchy cho f(x) = x^3 và g(x) = x^2 trên đoạn [2, 7]. Tìm điểm c thuộc (2, 7) mà định lý nói tới.
  - **Đáp án:** 134/27
    1. Cần c với (f(b) - f(a)) / (g(b) - g(a)) = f'(c) / g'(c), và g'(x) = 2x khác 0 trên khoảng.
    2. Vế trái: (343 - 8) / (49 - 4) = 67/9.
    3. Vế phải: 3c^2 / (2c) = 3c/2.
    4. 3c/2 = 67/9 cho c = 134/27, nằm trong (2, 7).

### Khai triển Taylor (`gt_t5_taylor`)

- `gt_t5_ty_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đa thức Taylor bậc hai của f(x) = sqrt(x) quanh x = 4 là a0 + a1(x - 4) + a2(x - 4)^2. Nhập a0, a1, a2 theo đúng thứ tự.
  - **Đáp án:** 2, 1/4, -1/64
    1. a0 = f(4) = 2.
    2. f'(x) = (1/2) x^(-1/2), nên a1 = f'(4) = 1/4.
    3. f''(x) = -(1/4) x^(-3/2), f''(4) = -(1/4) . (1/8) = -1/32, nên a2 = f''(4) / 2! = -1/64.
- `gt_t5_ty_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong khai triển Taylor của f quanh x = a, số hạng chứa (x - a)^k là gì?
    - **(đúng)** f^(k)(a) / k! . (x - a)^k
    - f^(k)(a) . (x - a)^k
    - f^(k)(x) / k! . (x - a)^k
    - f(a) / k! . (x - a)^k
  - **Đáp án:** f^(k)(a) / k! . (x - a)^k
    1. Hệ số được chọn sao cho đa thức có cùng đạo hàm các cấp với f tại a.
    2. Đạo hàm cấp k của (x - a)^k là k!, nên phải chia cho k!.
    3. Đạo hàm lấy tại a (một số), không phải tại x.
- `gt_t5_ty_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số thực a, đa thức Taylor bậc 3 của p(x) = x^3 - 2x + 5 quanh x = a, khi khai triển ra, chính là p(x).
  - **Đáp án:** Đúng
    1. Đạo hàm cấp 4 trở lên của p đều bằng 0, nên phần dư sau bậc 3 bằng 0.
    2. Vậy p(x) bằng đúng đa thức Taylor bậc 3 của nó quanh mọi điểm a.
    3. Khai triển các lũy thừa của (x - a) ra sẽ thu lại x^3 - 2x + 5.
- `gt_t5_ty_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước viết khai triển Taylor bậc hai của f(x) = ln x quanh x = 1.
  - **Đáp án (thứ tự đúng):**
    1. Tính f(1) = ln 1 = 0.
    2. f'(x) = 1/x, nên f'(1) = 1.
    3. f''(x) = -1/x^2, nên f''(1) = -1.
    4. Ghép lại: ln x = (x - 1) - (x - 1)^2 / 2 + o((x - 1)^2).
  - **Lời giải:**
    1. Tính lần lượt giá trị, đạo hàm cấp một, cấp hai tại điểm khai triển.
    2. Hệ số của (x - 1)^2 là f''(1) / 2! = -1/2.
- `gt_g5_taylor_he_so` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Khai triển Taylor của p(x) = -2x^3 + 4x^2 + 6x - 7 quanh x = 1. Tìm hệ số của (x - 1).
  - **Đáp án:** 8
    1. Hệ số của (x - 1)^1 là p^(1)(1) / 1!.
    2. Lấy đạo hàm p đủ 1 lần rồi thay x = 1.
    3. Được p^(1)(1) = 8, chia cho 1 ra 8.
  - **Câu hỏi:** Khai triển Taylor của p(x) = -3x^3 - 4x^2 - 5x + 2 quanh x = -1. Tìm hệ số của (x + 1)^3.
  - **Đáp án:** -3
    1. Hệ số của (x + 1)^3 là p^(3)(-1) / 3!.
    2. Lấy đạo hàm p đủ 3 lần rồi thay x = -1.
    3. Được p^(3)(-1) = -18, chia cho 6 ra -3.
  - **Câu hỏi:** Khai triển Taylor của p(x) = -2x^3 + 4x^2 + 2x - 5 quanh x = 1. Tìm hệ số của (x - 1)^3.
  - **Đáp án:** -2
    1. Hệ số của (x - 1)^3 là p^(3)(1) / 3!.
    2. Lấy đạo hàm p đủ 3 lần rồi thay x = 1.
    3. Được p^(3)(1) = -12, chia cho 6 ra -2.
- `gt_t5_ty_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giá trị tại x = 1.1 của đa thức Taylor bậc 3 của f(x) = 1/x quanh x = 1 (nhập phân số hoặc số thập phân đúng).
  - **Đáp án:** 909/1000
    1. f^(k)(x) = (-1)^k k! / x^(k + 1), nên f^(k)(1) / k! = (-1)^k.
    2. Đa thức Taylor bậc 3: 1 - (x - 1) + (x - 1)^2 - (x - 1)^3.
    3. Với x - 1 = 0.1: 1 - 0.1 + 0.01 - 0.001 = 0.909 = 909/1000 (giá trị đúng 1/1.1 xấp xỉ 0.90909).
- `gt_t5_ty_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: viết khai triển Taylor bậc hai của e^x quanh x = 1.
  - **Lời giải đưa ra (có một bước sai):**
    1. f(x) = e^x có f^(k)(x) = e^x với mọi k, nên f^(k)(1) = e.
    2. Công thức: f(x) = f(1) + f'(1)(x - 1) + f''(1)(x - 1)^2 / 2! + o((x - 1)^2).
    3. Thay vào: e^x = e + e(x - 1) + e(x - 1)^2 + o((x - 1)^2).   **<- bước sai đầu tiên**
    4. Hệ số của (x - 1)^2 là e.
  - **Đáp án:** Bước 3: Thay vào: e^x = e + e(x - 1) + e(x - 1)^2 + o((x - 1)^2).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 quên chia cho 2! ở số hạng bậc hai.
    2. Đúng là e^x = e + e(x - 1) + (e/2)(x - 1)^2 + o((x - 1)^2).
    3. Hệ số của (x - 1)^2 là e/2.
- `gt_t5_ty_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi x thuộc [0, 1], sai số khi thay e^x bằng 1 + x + x^2/2 nhỏ hơn 1/2.
  - **Đáp án:** Đúng
    1. Phần dư dạng Lagrange: e^x - (1 + x + x^2/2) = e^c . x^3 / 3! với c nằm giữa 0 và x.
    2. Với x thuộc [0, 1]: e^c <= e < 3 và x^3 <= 1, nên sai số < 3/6 = 1/2.
    3. Mệnh đề đúng (sai số lớn nhất, tại x = 1, là e - 2.5 xấp xỉ 0.22).
- `gt_t5_ty_08` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đa thức Taylor bậc hai của f(x) = x . ln x quanh x = 1 là a0 + a1(x - 1) + a2(x - 1)^2. Nhập a0, a1, a2 theo đúng thứ tự.
  - **Đáp án:** 0, 1, 1/2
    1. f(1) = 1 . ln 1 = 0.
    2. f'(x) = ln x + 1 (quy tắc tích), nên f'(1) = 1.
    3. f''(x) = 1/x, nên f''(1) = 1 và a2 = 1/2! = 1/2.
- `gt_g5_taylor_ln` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Khai triển Taylor của f(x) = ln x quanh x = 1. Tìm hệ số của (x - 1)^3.
  - **Đáp án:** 1/3
    1. Hệ số của (x - 1)^3 là f^(3)(1) / 3!.
    2. f^(k)(x) = (-1)^(k + 1) (k - 1)! / x^k, nên hệ số = f^(k)(1) / k! = (-1)^(k + 1) / (k . 1^k).
    3. Với k = 3: hệ số bằng 1/3.
  - **Câu hỏi:** Khai triển Taylor của f(x) = ln x quanh x = 1. Tìm hệ số của (x - 1)^2.
  - **Đáp án:** -1/2
    1. Hệ số của (x - 1)^2 là f^(2)(1) / 2!.
    2. f^(k)(x) = (-1)^(k + 1) (k - 1)! / x^k, nên hệ số = f^(k)(1) / k! = (-1)^(k + 1) / (k . 1^k).
    3. Với k = 2: hệ số bằng -1/2.
  - **Câu hỏi:** Khai triển Taylor của f(x) = ln x quanh x = 2. Tìm hệ số của (x - 2)^3.
  - **Đáp án:** 1/24
    1. Hệ số của (x - 2)^3 là f^(3)(2) / 3!.
    2. f^(k)(x) = (-1)^(k + 1) (k - 1)! / x^k, nên hệ số = f^(k)(2) / k! = (-1)^(k + 1) / (k . 2^k).
    3. Với k = 3: hệ số bằng 1/24.

### Khai triển Maclaurin của các hàm cơ bản (`gt_t5_maclaurin`)

- `gt_t5_mc_01` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với phần đầu khai triển Maclaurin của nó.
  - **Đáp án (ghép đúng):**
    - e^x — 1 + x + x^2/2 + x^3/6 + ...
    - sin x — x - x^3/6 + x^5/120 - ...
    - cos x — 1 - x^2/2 + x^4/24 - ...
    - ln(1 + x) — x - x^2/2 + x^3/3 - ...
    - 1/(1 - x) — 1 + x + x^2 + x^3 + ...
  - **Lời giải:**
    1. e^x có mọi hệ số 1/k!.
    2. sin x chỉ có lũy thừa lẻ, cos x chỉ có lũy thừa chẵn, dấu đổi luân phiên.
    3. ln(1 + x) có hệ số (-1)^(k + 1)/k, không có giai thừa; 1/(1 - x) là cấp số nhân với mọi hệ số bằng 1.
- `gt_t5_mc_02` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hệ số của x^3 trong khai triển Maclaurin của f(x) = sin(2x).
  - **Đáp án:** -4/3
    1. sin u = u - u^3/6 + ... với u = 2x.
    2. u^3 = 8x^3, nên số hạng bậc ba là -8x^3/6.
    3. Hệ số bằng -8/6 = -4/3.
- `gt_t5_mc_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khai triển Maclaurin của sqrt(1 + x) tới x^2 là gì?
    - **(đúng)** 1 + x/2 - x^2/8 + o(x^2)
    - 1 + x/2 + x^2/8 + o(x^2)
    - 1 + x/2 - x^2/4 + o(x^2)
    - 1 + x - x^2/2 + o(x^2)
  - **Đáp án:** 1 + x/2 - x^2/8 + o(x^2)
    1. (1 + x)^a = 1 + a x + a(a - 1)/2 . x^2 + o(x^2) với a = 1/2.
    2. a(a - 1)/2 = (1/2)(-1/2)/2 = -1/8.
    3. Được 1 + x/2 - x^2/8 + o(x^2).
- `gt_t5_mc_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khai triển Maclaurin của cos x chỉ chứa các lũy thừa chẵn của x.
  - **Đáp án:** Đúng
    1. cos là hàm chẵn, nên mọi đạo hàm cấp lẻ của nó là hàm lẻ và bằng 0 tại x = 0.
    2. Hệ số của x^k bằng f^(k)(0)/k!, nên mọi hệ số của lũy thừa lẻ bằng 0.
    3. Mệnh đề đúng: cos x = 1 - x^2/2 + x^4/24 - ...
- `gt_g5_maclaurin` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hệ số của x^2 trong khai triển Maclaurin của f(x) = ln(1 + 2x).
  - **Đáp án:** -2
    1. Dùng khai triển ln(1 + u) = u - u^2/2 + u^3/3 - ... với u = 2x.
    2. Số hạng chứa x^2 đến từ u^2 = 2^2 x^2 = 4x^2.
    3. Hệ số của x^2 là -2.
  - **Câu hỏi:** Tìm hệ số của x^2 trong khai triển Maclaurin của f(x) = e^(-3x).
  - **Đáp án:** 9/2
    1. Dùng khai triển e^u = 1 + u + u^2/2! + u^3/3! + ... với u = -3x.
    2. Số hạng chứa x^2 đến từ u^2 = (-3)^2 x^2 = 9x^2.
    3. Hệ số của x^2 là 9/2.
  - **Câu hỏi:** Tìm hệ số của x^4 trong khai triển Maclaurin của f(x) = ln(1 + 2x).
  - **Đáp án:** -4
    1. Dùng khai triển ln(1 + u) = u - u^2/2 + u^3/3 - ... với u = 2x.
    2. Số hạng chứa x^4 đến từ u^4 = 2^4 x^4 = 16x^4.
    3. Hệ số của x^4 là -4.
- `gt_t5_mc_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hệ số của x^4 trong khai triển Maclaurin của f(x) = e^(x^2) . cos x.
  - **Đáp án:** 1/24
    1. e^(x^2) = 1 + x^2 + x^4/2 + o(x^4) và cos x = 1 - x^2/2 + x^4/24 + o(x^4).
    2. Các tích cho x^4: 1 . (1/24) + 1 . (-1/2) + (1/2) . 1.
    3. Cộng lại: 1/24 - 1/2 + 1/2 = 1/24.
- `gt_t5_mc_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: khai triển Maclaurin của ln(1 + 2x) tới x^3.
  - **Lời giải đưa ra (có một bước sai):**
    1. ln(1 + u) = u - u^2/2 + u^3/3 + o(u^3).
    2. Thay u = 2x: ln(1 + 2x) = 2x - 2x^2/2 + 2x^3/3 + o(x^3).   **<- bước sai đầu tiên**
    3. Rút gọn: ln(1 + 2x) = 2x - x^2 + 2x^3/3 + o(x^3).
  - **Đáp án:** Bước 2: Thay u = 2x: ln(1 + 2x) = 2x - 2x^2/2 + 2x^3/3 + o(x^3).
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: thay u = 2x thì u^2 = 4x^2 và u^3 = 8x^3, phải lũy thừa cả số 2.
    2. Đúng là ln(1 + 2x) = 2x - 4x^2/2 + 8x^3/3 + o(x^3) = 2x - 2x^2 + 8x^3/3 + o(x^3).
- `gt_t5_mc_07` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước dùng khai triển Maclaurin tính giới hạn của (e^x - 1 - x) / x^2 khi x -> 0.
  - **Đáp án (thứ tự đúng):**
    1. Viết e^x = 1 + x + x^2/2 + o(x^2).
    2. Tử: e^x - 1 - x = x^2/2 + o(x^2).
    3. Chia cho x^2: biểu thức bằng 1/2 + o(x^2)/x^2.
    4. Cho x -> 0, o(x^2)/x^2 -> 0: giới hạn bằng 1/2.
  - **Lời giải:**
    1. Khai triển tới bậc bằng bậc của mẫu (ở đây x^2).
    2. Các số hạng 1 và x bị trừ hết, chỉ còn số hạng bậc hai quyết định giới hạn.
- `gt_t5_mc_08` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 . sin x. Dùng khai triển Maclaurin, tính đạo hàm cấp năm f^(5)(0).
  - **Đáp án:** -20
    1. x^2 . sin x = x^2 (x - x^3/6 + o(x^3)) = x^3 - x^5/6 + o(x^5).
    2. Hệ số của x^5 là f^(5)(0) / 5! = -1/6.
    3. f^(5)(0) = -120/6 = -20.
- `gt_t5_mc_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x) = ln(1 + x) - x + x^2/2 với x > -1.
  - **Phần a** (Điền số): a) Tìm hệ số của x^3 trong khai triển Maclaurin của f.
    - **Đáp án a:** 1/3
  - **Phần b** (Điền số): b) Tính đạo hàm cấp ba f'''(0).
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) Giới hạn của f(x) / x^3 khi x -> 0 bằng 1/3.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) ln(1 + x) = x - x^2/2 + x^3/3 - ..., nên f(x) = x^3/3 + o(x^3): hệ số 1/3.
    2. b) Hệ số x^3 bằng f'''(0) / 3!, nên f'''(0) = 6 . (1/3) = 2.
    3. c) f(x) / x^3 = 1/3 + o(x^3)/x^3 -> 1/3: đúng.
- `gt_g5_maclaurin_tich` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hệ số của x^3 trong khai triển Maclaurin của f(x) = e^(-x) . sin(-2x).
  - **Đáp án:** 1/3
    1. Khai triển từng thừa số tới x^3, rồi nhân: hệ số của x^3 là tổng các tích (hệ số x^j của thừa số đầu) . (hệ số x^(3 - j) của thừa số sau).
    2. Hệ số của e^(-x): 1, -1, 1/2, -1/6 (từ x^0 tới x^3).
    3. Hệ số của sin(-2x): 0, -2, 0, 4/3.
    4. Cộng các tích: 1 . (4/3) + (1/2) . (-2) = 1/3.
  - **Câu hỏi:** Tìm hệ số của x^3 trong khai triển Maclaurin của f(x) = e^(-2x) . (1 - 2x)^1.
  - **Đáp án:** -16/3
    1. Khai triển từng thừa số tới x^3, rồi nhân: hệ số của x^3 là tổng các tích (hệ số x^j của thừa số đầu) . (hệ số x^(3 - j) của thừa số sau).
    2. Hệ số của e^(-2x): 1, -2, 2, -4/3 (từ x^0 tới x^3).
    3. Hệ số của (1 - 2x)^1: 1, -2, 0, 0.
    4. Cộng các tích: 2 . (-2) + (-4/3) . 1 = -16/3.
  - **Câu hỏi:** Tìm hệ số của x^3 trong khai triển Maclaurin của f(x) = e^(-x) . sin(-x).
  - **Đáp án:** -1/3
    1. Khai triển từng thừa số tới x^3, rồi nhân: hệ số của x^3 là tổng các tích (hệ số x^j của thừa số đầu) . (hệ số x^(3 - j) của thừa số sau).
    2. Hệ số của e^(-x): 1, -1, 1/2, -1/6 (từ x^0 tới x^3).
    3. Hệ số của sin(-x): 0, -1, 0, 1/6.
    4. Cộng các tích: 1 . (1/6) + (1/2) . (-1) = -1/3.

### Quy tắc L'Hospital (`gt_t5_lhospital`)

- `gt_t5_lh_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (x^3 - 1) / ln x khi x -> 1.
  - **Đáp án:** 3
    1. Thay x = 1: tử 0, mẫu ln 1 = 0, dạng 0/0.
    2. L'Hospital: giới hạn bằng giới hạn của 3x^2 / (1/x) = 3x^3.
    3. Thay x = 1 được 3.
- `gt_t5_lh_02` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (x^2 + 1) / (x + 1) khi x -> 1.
  - **Lời giải đưa ra (có một bước sai):**
    1. Thay x = 1: tử bằng 2, mẫu bằng 2.
    2. Dùng quy tắc L'Hospital: giới hạn bằng giới hạn của 2x / 1.   **<- bước sai đầu tiên**
    3. Thay x = 1 được 2.
  - **Đáp án:** Bước 2: Dùng quy tắc L'Hospital: giới hạn bằng giới hạn của 2x / 1.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: 2/2 không phải dạng vô định, nên không được dùng L'Hospital.
    2. Hàm liên tục tại 1 nên chỉ cần thay số: giới hạn bằng 2/2 = 1.
- `gt_t5_lh_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn nào sau đây được phép dùng ngay quy tắc L'Hospital?
    - **(đúng)** Giới hạn của sin x / x khi x -> 0
    - Giới hạn của cos x / x khi x -> 0
    - Giới hạn của (x + 1) / (x - 2) khi x -> 1
    - Giới hạn của (x + 1) / x^2 khi x -> 0
  - **Đáp án:** Giới hạn của sin x / x khi x -> 0
    1. L'Hospital chỉ dùng cho dạng 0/0 hoặc vô cùng/vô cùng.
    2. sin x / x tại 0 là dạng 0/0.
    3. cos x / x và (x + 1)/x^2 có tử dần tới số khác 0 còn mẫu dần tới 0; (x + 1)/(x - 2) tại 1 bằng -2, không vô định.
- `gt_t5_lh_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của ln x / x khi x -> +vô cùng bằng 0.
  - **Đáp án:** Đúng
    1. Dạng vô cùng/vô cùng.
    2. L'Hospital: giới hạn bằng giới hạn của (1/x) / 1 = 1/x.
    3. 1/x -> 0: mệnh đề đúng (ln x tăng chậm hơn x).
- `gt_t5_lh_08` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của x^2 / e^x khi x -> +vô cùng.
  - **Đáp án (thứ tự đúng):**
    1. Dạng vô cùng/vô cùng; dùng L'Hospital lần thứ nhất được 2x / e^x.
    2. Vẫn là dạng vô cùng/vô cùng; dùng L'Hospital lần thứ hai được 2 / e^x.
    3. Khi x -> +vô cùng, 2 / e^x -> 0.
    4. Vậy giới hạn ban đầu bằng 0.
  - **Lời giải:**
    1. Mỗi lần dùng L'Hospital phải kiểm tra lại dạng vô định.
    2. Bậc của đa thức giảm dần còn e^x giữ nguyên, nên e^x thắng mọi lũy thừa.
- `gt_g5_lhospital` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (x^4 - 16) / (x^2 - 4) khi x -> -2.
  - **Đáp án:** 8
    1. Thay x = -2: tử và mẫu đều bằng 0, dạng 0/0.
    2. L'Hospital: giới hạn bằng giới hạn của 4x^3 / (2x).
    3. Thay x = -2: 4 . (-2)^3 / (2 . (-2)) = 8.
  - **Câu hỏi:** Tính giới hạn của (x^2 - 4) / (x^3 + 8) khi x -> -2.
  - **Đáp án:** -1/3
    1. Thay x = -2: tử và mẫu đều bằng 0, dạng 0/0.
    2. L'Hospital: giới hạn bằng giới hạn của 2x / (3x^2).
    3. Thay x = -2: 2 . (-2) / (3 . (-2)^2) = -1/3.
  - **Câu hỏi:** Tính giới hạn của (x^4 - 1) / (x^5 + 1) khi x -> -1.
  - **Đáp án:** -4/5
    1. Thay x = -1: tử và mẫu đều bằng 0, dạng 0/0.
    2. L'Hospital: giới hạn bằng giới hạn của 4x^3 / (5x^4).
    3. Thay x = -1: 4 . (-1)^3 / (5 . (-1)^4) = -4/5.
- `gt_t5_lh_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (tan x - x) / x^3 khi x -> 0.
  - **Đáp án:** 1/3
    1. Dạng 0/0. Lần 1: (1/cos^2 x - 1) / (3x^2) = tan^2 x / (3x^2).
    2. tan x / x -> 1, nên tan^2 x / x^2 -> 1.
    3. Giới hạn bằng 1/3.
- `gt_t5_lh_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (e^x - 1) / x khi x -> 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Thay x = 0 được dạng 0/0.
    2. Đạo hàm của cả phân thức theo quy tắc thương: ((e^x - 1)/x)' = (x e^x - e^x + 1) / x^2.
    3. Theo L'Hospital, giới hạn ban đầu bằng giới hạn của (x e^x - e^x + 1) / x^2.   **<- bước sai đầu tiên**
    4. Dùng L'Hospital tiếp cho phân thức mới, được 1/2.
  - **Đáp án:** Bước 3: Theo L'Hospital, giới hạn ban đầu bằng giới hạn của (x e^x - e^x + 1) / x^2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 tính đúng đạo hàm của phân thức, nhưng bước 3 dùng nó: L'Hospital lấy đạo hàm riêng tử và riêng mẫu, không lấy đạo hàm cả phân thức.
    2. Đúng: giới hạn bằng giới hạn của e^x / 1 = 1.
- `gt_t5_lh_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vì giới hạn của (1 + cos x) / 1 khi x -> +vô cùng không tồn tại, giới hạn của (x + sin x) / x khi x -> +vô cùng cũng không tồn tại.
  - **Đáp án:** Sai
    1. L'Hospital chỉ nói: nếu giới hạn của f'/g' tồn tại thì giới hạn của f/g bằng nó. Khi f'/g' không có giới hạn, quy tắc không kết luận gì.
    2. Tính trực tiếp: (x + sin x)/x = 1 + sin x / x, và |sin x / x| <= 1/x -> 0.
    3. Giới hạn bằng 1, nên mệnh đề sai.
- `gt_t5_lh_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: xét L = giới hạn của (e^x - 1 - x - x^2/2) / x^3 khi x -> 0.
  - **Phần a** (Trắc nghiệm): a) Thay x = 0, giới hạn có dạng nào?
    - **(đúng)** 0/0
    - vô cùng/vô cùng
    - một số khác 0 chia cho 0
    - 1 mũ vô cùng
    - **Đáp án a:** 0/0
  - **Phần b** (Điền số): b) Phải dùng quy tắc L'Hospital bao nhiêu lần liên tiếp thì mẫu mới khác 0 tại x = 0?
    - **Đáp án b:** 3
  - **Phần c** (Điền số): c) Tính L.
    - **Đáp án c:** 1/6
  - **Lời giải:**
    1. a) Tử: 1 - 1 - 0 - 0 = 0, mẫu 0: dạng 0/0.
    2. b) Lần 1: (e^x - 1 - x) / (3x^2), vẫn 0/0. Lần 2: (e^x - 1) / (6x), vẫn 0/0. Lần 3: e^x / 6, mẫu là 6: cần 3 lần.
    3. c) L = e^0 / 6 = 1/6 (khớp với hệ số x^3 của e^x là 1/3! = 1/6).
- `gt_g5_lhospital_bac2` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của (1 - cos(-3x)) / (-x^2) khi x -> 0.
  - **Đáp án:** -9/2
    1. Thay x = 0 được dạng 0/0; lấy đạo hàm riêng tử và riêng mẫu cho tới khi hết dạng 0/0.
    2. Lần 1: -3sin(-3x) / (-2x), vẫn 0/0.
    3. Lần 2: 9cos(-3x) / (-2) -> -9/2.
  - **Câu hỏi:** Tính giới hạn của (e^(-3x) - 1 + 3x) / x^2 khi x -> 0.
  - **Đáp án:** 9/2
    1. Thay x = 0 được dạng 0/0; lấy đạo hàm riêng tử và riêng mẫu cho tới khi hết dạng 0/0.
    2. Lần 1: (-3e^(-3x) - (-3)) / (2x), vẫn 0/0.
    3. Lần 2: 9e^(-3x) / 2 -> 9/2.
  - **Câu hỏi:** Tính giới hạn của (1 - cos(-2x)) / (-x^2) khi x -> 0.
  - **Đáp án:** -2
    1. Thay x = 0 được dạng 0/0; lấy đạo hàm riêng tử và riêng mẫu cho tới khi hết dạng 0/0.
    2. Lần 1: -2sin(-2x) / (-2x), vẫn 0/0.
    3. Lần 2: 4cos(-2x) / (-2) -> -2.

### Các dạng vô định khác (`gt_t5_dang_vo_dinh`)

- `gt_t5_vd_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của x . ln x khi x -> 0+.
  - **Đáp án:** 0
    1. Dạng 0 . (-vô cùng): viết thành ln x / (1/x), dạng vô cùng/vô cùng.
    2. L'Hospital: (1/x) / (-1/x^2) = -x.
    3. -x -> 0, nên giới hạn bằng 0.
- `gt_t5_vd_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (1 + 2/x)^x khi x -> +vô cùng bằng bao nhiêu?
    - **(đúng)** e^2
    - 1
    - e
    - +vô cùng
  - **Đáp án:** e^2
    1. Dạng 1 mũ vô cùng: lấy ln được x . ln(1 + 2/x).
    2. ln(1 + 2/x) ~ 2/x khi x -> +vô cùng, nên x . ln(1 + 2/x) -> 2.
    3. Giới hạn bằng e^2. Trả lời 1 là coi 1 mũ vô cùng bằng 1, sai.
- `gt_t5_vd_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai hàm u, v mà u(x) -> 1 và v(x) -> +vô cùng khi x -> +vô cùng, ta có u(x)^v(x) -> 1.
  - **Đáp án:** Sai
    1. 1 mũ vô cùng là một dạng vô định: kết quả phụ thuộc vào tốc độ.
    2. Phản ví dụ u = 1 + 1/x, v = x: (1 + 1/x)^x -> e, khác 1.
    3. Mệnh đề sai.
- `gt_t5_vd_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính giới hạn của x^x khi x -> 0+.
  - **Đáp án (thứ tự đúng):**
    1. Viết x^x = e^(x ln x) để đưa dạng 0 mũ 0 về một tích ở số mũ.
    2. Số mũ x ln x là dạng 0 . vô cùng; viết thành ln x / (1/x).
    3. L'Hospital: (1/x) / (-1/x^2) = -x -> 0.
    4. Vậy x^x -> e^0 = 1.
  - **Lời giải:**
    1. Dạng mũ: luôn đưa về e mũ một biểu thức, tính giới hạn số mũ trước.
    2. Hàm e^t liên tục nên giới hạn của e^(số mũ) là e^(giới hạn số mũ).
- `gt_g5_vo_dinh_tich` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của x . sin(4/x) khi x -> +vô cùng.
  - **Đáp án:** 4
    1. Đưa tích về một thương để có dạng 0/0 hoặc vô cùng/vô cùng.
    2. Dạng vô cùng . 0. Đặt t = 1/x -> 0+: x . sin(4/x) = sin(4t) / t.
    3. Dạng 0/0; L'Hospital: 4cos(4t) / 1 -> 4.
  - **Câu hỏi:** Tính giới hạn của x . sin(-5/x) khi x -> +vô cùng.
  - **Đáp án:** -5
    1. Đưa tích về một thương để có dạng 0/0 hoặc vô cùng/vô cùng.
    2. Dạng vô cùng . 0. Đặt t = 1/x -> 0+: x . sin(-5/x) = sin(-5t) / t.
    3. Dạng 0/0; L'Hospital: -5cos(-5t) / 1 -> -5.
  - **Câu hỏi:** Tính giới hạn của x . sin(4/x) khi x -> +vô cùng.
  - **Đáp án:** 4
    1. Đưa tích về một thương để có dạng 0/0 hoặc vô cùng/vô cùng.
    2. Dạng vô cùng . 0. Đặt t = 1/x -> 0+: x . sin(4/x) = sin(4t) / t.
    3. Dạng 0/0; L'Hospital: 4cos(4t) / 1 -> 4.
- `gt_t5_vd_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn của 1/sin^2 x - 1/x^2 khi x -> 0.
  - **Đáp án:** 1/3
    1. Dạng vô cùng trừ vô cùng: quy đồng được (x^2 - sin^2 x) / (x^2 sin^2 x).
    2. sin x = x - x^3/6 + o(x^3), nên sin^2 x = x^2 - x^4/3 + o(x^4) và tử = x^4/3 + o(x^4).
    3. Mẫu ~ x^4, nên giới hạn bằng 1/3.
- `gt_t5_vd_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính giới hạn của (cos x)^(1/x^2) khi x -> 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. Dạng 1 mũ vô cùng: viết (cos x)^(1/x^2) = e^(ln(cos x) / x^2).
    2. ln(cos x) = ln(1 + (cos x - 1)) ~ cos x - 1 ~ -x^2/2.
    3. Số mũ ln(cos x) / x^2 -> -1/2.
    4. Vậy giới hạn bằng -1/2.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vậy giới hạn bằng -1/2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 quên trả lại hàm mũ: -1/2 là giới hạn của số mũ, không phải của biểu thức.
    2. Giới hạn đúng là e^(-1/2) = 1 / sqrt(e).
- `gt_t5_vd_07` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của ((1 + x)^(1/x) - e) / x khi x -> 0 bằng k . e. Tìm k.
  - **Đáp án:** -1/2
    1. (1 + x)^(1/x) = e^(ln(1 + x)/x) và ln(1 + x)/x = 1 - x/2 + o(x).
    2. Nên (1 + x)^(1/x) = e . e^(-x/2 + o(x)) = e(1 - x/2 + o(x)).
    3. Tử = -e x/2 + o(x), chia cho x được -e/2: k = -1/2.
- `gt_t5_vd_08` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của x^(sin x) khi x -> 0+ bằng 1.
  - **Đáp án:** Đúng
    1. Dạng 0 mũ 0: x^(sin x) = e^(sin x . ln x).
    2. sin x ~ x, nên sin x . ln x có cùng giới hạn với x ln x, tức là 0.
    3. Giới hạn bằng e^0 = 1: mệnh đề đúng.
- `gt_t5_vd_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: xét L = giới hạn của (1 + 3/x)^(2x) khi x -> +vô cùng.
  - **Phần a** (Trắc nghiệm): a) Biểu thức có dạng vô định nào?
    - **(đúng)** 1 mũ vô cùng
    - 0 mũ 0
    - vô cùng mũ 0
    - 0 . vô cùng
    - **Đáp án a:** 1 mũ vô cùng
  - **Phần b** (Điền số): b) Tính ln L.
    - **Đáp án b:** 6
  - **Phần c** (Đúng/Sai): c) L > 400.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Cơ số 1 + 3/x -> 1, số mũ 2x -> +vô cùng: dạng 1 mũ vô cùng.
    2. b) ln của biểu thức = 2x . ln(1 + 3/x), và ln(1 + 3/x) ~ 3/x, nên ln L = 2 . 3 = 6.
    3. c) L = e^6 xấp xỉ 403.4 > 400: đúng.
- `gt_g5_vo_dinh_mu` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn của (1 + 3/x)^(-x) khi x -> +vô cùng bằng e^k. Tìm k.
  - **Đáp án:** -3
    1. Dạng 1 mũ vô cùng: lấy ln để đưa về tích, rồi về thương.
    2. ln của biểu thức = -x . ln(1 + 3/x), và ln(1 + 3/x) ~ 3/x khi x -> +vô cùng.
    3. Số mũ dần tới -3, nên giới hạn bằng e^(-3) và k = -3.
  - **Câu hỏi:** Giới hạn của (1 - 3x)^(-3/x) khi x -> 0 bằng e^k. Tìm k.
  - **Đáp án:** 9
    1. Dạng 1 mũ vô cùng: lấy ln để đưa về tích, rồi về thương.
    2. ln của biểu thức = -3 . ln(1 - 3x) / x, và ln(1 - 3x) ~ -3x.
    3. Số mũ dần tới 9, nên giới hạn bằng e^9 và k = 9.
  - **Câu hỏi:** Giới hạn của (1 + 2/x)^(-x) khi x -> +vô cùng bằng e^k. Tìm k.
  - **Đáp án:** -2
    1. Dạng 1 mũ vô cùng: lấy ln để đưa về tích, rồi về thương.
    2. ln của biểu thức = -x . ln(1 + 2/x), và ln(1 + 2/x) ~ 2/x khi x -> +vô cùng.
    3. Số mũ dần tới -2, nên giới hạn bằng e^(-2) và k = -2.

## Tầng 6: Đơn điệu, cực trị và khảo sát hàm số

57 dạng câu (46 câu viết tay, 11 bộ sinh câu); 57 chưa duyệt.

### Tính đơn điệu (`gt_t6_don_dieu`)

- `gt_t6_dd_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 - 12x + 1 nghịch biến trên đoạn [a, b] và đồng biến trên mỗi khoảng còn lại của R. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -2, 2
    1. f'(x) = 3x^2 - 12 = 3(x - 2)(x + 2).
    2. f'(x) < 0 khi -2 < x < 2 và f'(x) > 0 khi |x| > 2.
    3. f nghịch biến trên [-2, 2]: a = -2, b = 2.
- `gt_t6_dd_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f khả vi và đồng biến ngặt trên (a, b), ta có f'(x) > 0 với mọi x thuộc (a, b).
  - **Đáp án:** Sai
    1. Phản ví dụ: f(x) = x^3 đồng biến ngặt trên (-1, 1).
    2. Nhưng f'(0) = 0, không dương.
    3. Chiều đúng là ngược lại: f' > 0 trên khoảng thì f đồng biến ngặt; đồng biến ngặt chỉ cho f' >= 0.
- `gt_t6_dd_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x . e^(-x) đồng biến trên khoảng nào (lớn nhất có thể)?
    - **(đúng)** (-vô cùng, 1)
    - (1, +vô cùng)
    - (-vô cùng, 0)
    - R
  - **Đáp án:** (-vô cùng, 1)
    1. f'(x) = e^(-x) - x e^(-x) = (1 - x) e^(-x).
    2. e^(-x) > 0, nên dấu của f' là dấu của 1 - x.
    3. f' > 0 khi x < 1: f đồng biến trên (-vô cùng, 1) và nghịch biến trên (1, +vô cùng).
- `gt_t6_dd_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét tính đơn điệu của f(x) = 1/x và so sánh f(-1) với f(1).
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = -1/x^2 < 0 với mọi x khác 0.
    2. Vậy f nghịch biến trên từng khoảng (-vô cùng, 0) và (0, +vô cùng).
    3. Do đó f nghịch biến trên R \ {0}, nên -1 < 1 cho f(-1) > f(1).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Do đó f nghịch biến trên R \ {0}, nên -1 < 1 cho f(-1) > f(1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: nghịch biến trên từng khoảng không có nghĩa là nghịch biến trên hợp của chúng, vì hai khoảng bị ngắt tại 0.
    2. Thực tế f(-1) = -1 < 1 = f(1).
- `gt_g6_don_dieu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = 2x^3 + 15x^2 + 36x - 4 nghịch biến trên một đoạn [a, b] và đồng biến trên mỗi khoảng còn lại của R. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -3, -2
    1. f'(x) = 6x^2 + 30x + 36 = 6(x + 3)(x + 2).
    2. f'(x) = 0 tại x = -3 và x = -2.
    3. Hệ số 6 dương nên f' âm giữa hai nghiệm và dương ở ngoài.
    4. f nghịch biến trên [-3, -2]: a = -3, b = -2.
  - **Câu hỏi:** Hàm f(x) = -2x^3 - 21x^2 - 72x đồng biến trên một đoạn [a, b] và nghịch biến trên mỗi khoảng còn lại của R. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -4, -3
    1. f'(x) = -6x^2 - 42x - 72 = -6(x + 4)(x + 3).
    2. f'(x) = 0 tại x = -4 và x = -3.
    3. Hệ số -6 âm nên f' dương giữa hai nghiệm và âm ở ngoài.
    4. f đồng biến trên [-4, -3]: a = -4, b = -3.
  - **Câu hỏi:** Hàm f(x) = 2x^3 + 9x^2 + 12x + 4 nghịch biến trên một đoạn [a, b] và đồng biến trên mỗi khoảng còn lại của R. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -2, -1
    1. f'(x) = 6x^2 + 18x + 12 = 6(x + 2)(x + 1).
    2. f'(x) = 0 tại x = -2 và x = -1.
    3. Hệ số 6 dương nên f' âm giữa hai nghiệm và dương ở ngoài.
    4. f nghịch biến trên [-2, -1]: a = -2, b = -1.
- `gt_t6_dd_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 - 3x^2 + mx đồng biến trên R khi và chỉ khi m >= m0. Tìm m0.
  - **Đáp án:** 3
    1. f'(x) = 3x^2 - 6x + m; cần f'(x) >= 0 với mọi x.
    2. Tam thức có hệ số x^2 dương, nên điều kiện là biệt thức 36 - 12m <= 0.
    3. Tức m >= 3 (khi m = 3, f' = 3(x - 1)^2 chỉ bằng 0 tại x = 1, f vẫn đồng biến): m0 = 3.
- `gt_t6_dd_06` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh ln(1 + x) < x với mọi x > 0.
  - **Đáp án (thứ tự đúng):**
    1. Đặt g(x) = x - ln(1 + x) trên [0, +vô cùng).
    2. Tính g'(x) = 1 - 1/(1 + x) = x/(1 + x) > 0 với x > 0.
    3. Nên g đồng biến ngặt trên [0, +vô cùng).
    4. Với x > 0: g(x) > g(0) = 0, tức ln(1 + x) < x.
  - **Lời giải:**
    1. Chuyển bất đẳng thức về dạng g(x) > 0 với g(0) = 0.
    2. Đạo hàm dương cho g tăng, nên g(x) lớn hơn giá trị tại điểm đầu.
- `gt_t6_dd_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^5 + x^3 + x - 3 = 0 có đúng một nghiệm thực.
  - **Đáp án:** Đúng
    1. Đặt f(x) = x^5 + x^3 + x - 3: f'(x) = 5x^4 + 3x^2 + 1 > 0, nên f đồng biến ngặt trên R và có nhiều nhất một nghiệm.
    2. f(1) = 1 + 1 + 1 - 3 = 0, nên có nghiệm x = 1.
    3. Vậy có đúng một nghiệm: mệnh đề đúng.
- `gt_g6_dong_bien_tf` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 - 2x^2 + 3x + 1 đồng biến trên R.
  - **Đáp án:** Đúng
    1. f'(x) = 3x^2 - 4x + 3, một tam thức bậc hai có hệ số x^2 dương.
    2. f đồng biến trên R khi f'(x) >= 0 với mọi x, tức biệt thức của tam thức f'(x) không dương.
    3. Biệt thức = (-4)^2 - 4 . 3 . 3 = -20.
    4. Biệt thức <= 0 nên f' không âm (chỉ bằng 0 tại nhiều nhất một điểm): f đồng biến trên R, mệnh đề đúng.
  - **Câu hỏi:** Hàm f(x) = x^3 - 4x^2 - 5x + 1 đồng biến trên R.
  - **Đáp án:** Sai
    1. f'(x) = 3x^2 - 8x - 5, một tam thức bậc hai có hệ số x^2 dương.
    2. f đồng biến trên R khi f'(x) >= 0 với mọi x, tức biệt thức của tam thức f'(x) không dương.
    3. Biệt thức = (-8)^2 - 4 . 3 . (-5) = 124.
    4. Biệt thức > 0 nên f' âm giữa hai nghiệm của nó: f không đồng biến trên R, mệnh đề sai.
  - **Câu hỏi:** Hàm f(x) = x^3 - x^2 + 3x + 1 đồng biến trên R.
  - **Đáp án:** Đúng
    1. f'(x) = 3x^2 - 2x + 3, một tam thức bậc hai có hệ số x^2 dương.
    2. f đồng biến trên R khi f'(x) >= 0 với mọi x, tức biệt thức của tam thức f'(x) không dương.
    3. Biệt thức = (-2)^2 - 4 . 3 . 3 = -32.
    4. Biệt thức <= 0 nên f' không âm (chỉ bằng 0 tại nhiều nhất một điểm): f đồng biến trên R, mệnh đề đúng.

### Cực trị (`gt_t6_cuc_tri`)

- `gt_t6_ct_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^3 - 3x^2 + 2. Nhập giá trị cực đại rồi giá trị cực tiểu của f.
  - **Đáp án:** 2, -2
    1. f'(x) = 3x^2 - 6x = 3x(x - 2), bằng 0 tại x = 0 và x = 2.
    2. f' đổi dấu từ + sang - tại 0 (cực đại) và từ - sang + tại 2 (cực tiểu).
    3. f(0) = 2 và f(2) = 8 - 12 + 2 = -2.
- `gt_t6_ct_02` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm các điểm cực trị của f(x) = x^3.
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 3x^2.
    2. f'(x) = 0 chỉ khi x = 0.
    3. Vậy x = 0 là điểm cực trị duy nhất của f.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Vậy x = 0 là điểm cực trị duy nhất của f.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: f'(a) = 0 chỉ là điều kiện cần, chưa đủ để có cực trị.
    2. f'(x) = 3x^2 >= 0 không đổi dấu qua 0, nên f tăng trên cả R.
    3. f không có điểm cực trị nào.
- `gt_t6_ct_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f có đạo hàm cấp hai liên tục, f'(x0) = 0 và f''(x0) = -3. Kết luận nào đúng?
    - **(đúng)** x0 là điểm cực đại của f
    - x0 là điểm cực tiểu của f
    - x0 không phải điểm cực trị
    - (x0, f(x0)) là điểm uốn
  - **Đáp án:** x0 là điểm cực đại của f
    1. Dấu hiệu đạo hàm cấp hai: f'(x0) = 0 và f''(x0) < 0 thì x0 là điểm cực đại.
    2. f'' < 0 nghĩa là f' giảm qua x0, tức đổi dấu từ + sang -.
- `gt_t6_ct_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = |x| đạt cực tiểu tại x = 0, dù f'(0) không tồn tại.
  - **Đáp án:** Đúng
    1. f(x) = |x| >= 0 = f(0) với mọi x, nên 0 là điểm cực tiểu.
    2. f không có đạo hàm tại 0 (hai phía có hệ số góc -1 và 1).
    3. Điểm tới hạn gồm cả nơi f' bằng 0 lẫn nơi f' không tồn tại: mệnh đề đúng.
- `gt_g6_cuc_tri` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị cực tiểu của hàm số f(x) = 2x^3 + 15x^2 + 36x - 4.
  - **Đáp án:** -32
    1. f'(x) = 6(x + 3)(x + 2), bằng 0 tại x = -3 và x = -2.
    2. Hệ số 6 dương: f' đổi dấu từ + sang - tại -3 và từ - sang + tại -2.
    3. Điểm cực tiểu là x = -2; giá trị cực tiểu f(-2) = -32.
  - **Câu hỏi:** Tìm giá trị cực đại của hàm số f(x) = -2x^3 - 21x^2 - 72x.
  - **Đáp án:** 81
    1. f'(x) = -6(x + 4)(x + 3), bằng 0 tại x = -4 và x = -3.
    2. Hệ số -6 âm: f' đổi dấu từ - sang + tại -4 và từ + sang - tại -3.
    3. Điểm cực đại là x = -3; giá trị cực đại f(-3) = 81.
  - **Câu hỏi:** Tìm giá trị cực tiểu của hàm số f(x) = 2x^3 + 9x^2 + 12x + 4.
  - **Đáp án:** -1
    1. f'(x) = 6(x + 2)(x + 1), bằng 0 tại x = -2 và x = -1.
    2. Hệ số 6 dương: f' đổi dấu từ + sang - tại -2 và từ - sang + tại -1.
    3. Điểm cực tiểu là x = -1; giá trị cực tiểu f(-1) = -1.
- `gt_t6_ct_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^4 - 4x^3. Nhập số điểm cực trị của f, rồi giá trị cực tiểu của f.
  - **Đáp án:** 1, -27
    1. f'(x) = 4x^3 - 12x^2 = 4x^2(x - 3), bằng 0 tại x = 0 (nghiệm kép) và x = 3.
    2. Qua x = 0, f' không đổi dấu (âm hai bên): không phải cực trị. Qua x = 3, f' đổi từ - sang +: cực tiểu.
    3. Chỉ có 1 điểm cực trị; giá trị cực tiểu f(3) = 81 - 108 = -27.
- `gt_t6_ct_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét cực trị của f(x) = x^4 tại x = 0.
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 4x^3, nên f'(0) = 0.
    2. f''(x) = 12x^2, nên f''(0) = 0.
    3. Vì f''(0) = 0 nên x = 0 không phải điểm cực trị.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Vì f''(0) = 0 nên x = 0 không phải điểm cực trị.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: f''(0) = 0 thì dấu hiệu cấp hai không kết luận được gì, phải xét thêm.
    2. Xét dấu f'(x) = 4x^3: âm khi x < 0, dương khi x > 0.
    3. f' đổi từ - sang +, nên x = 0 là điểm cực tiểu (rõ ràng x^4 >= 0).
- `gt_t6_ct_07` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f khả vi quanh x0 và f'(x0) = 0. Ghép mỗi thông tin với kết luận đúng về x0.
  - **Đáp án (ghép đúng):**
    - f' đổi dấu từ + sang - khi đi qua x0 — x0 là điểm cực đại
    - f' đổi dấu từ - sang + khi đi qua x0 — x0 là điểm cực tiểu
    - f' cùng dấu dương ở hai bên x0 — x0 không phải điểm cực trị
    - f''(x0) = 0 và không biết gì thêm — chưa kết luận được, phải xét thêm
  - **Lời giải:**
    1. Dấu hiệu cấp một: f' đổi dấu từ + sang - cho cực đại, từ - sang + cho cực tiểu.
    2. f' không đổi dấu thì f đơn điệu qua x0: không có cực trị.
    3. f''(x0) = 0 làm dấu hiệu cấp hai bất lực: x^3, x^4 và -x^4 đều có f'(0) = f''(0) = 0 nhưng kết luận khác nhau.
- `gt_g6_so_cuc_tri` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm số f(x) = -3x^4 + 16x^3 - 18x^2 có bao nhiêu điểm cực trị?
  - **Đáp án:** 3
    1. f'(x) = -12x^3 + 48x^2 - 36x = -12x(x - 1)(x - 3).
    2. f' đổi dấu khi đi qua một nghiệm bội lẻ, không đổi dấu qua một nghiệm bội chẵn.
    3. Bội của các nghiệm: x = 0 bội 1, x = 1 bội 1, x = 3 bội 1.
    4. Số điểm cực trị: 3.
  - **Câu hỏi:** Hàm số f(x) = -3x^4 - 24x^3 - 54x^2 có bao nhiêu điểm cực trị?
  - **Đáp án:** 1
    1. f'(x) = -12x^3 - 72x^2 - 108x = -12x(x + 3)^2.
    2. f' đổi dấu khi đi qua một nghiệm bội lẻ, không đổi dấu qua một nghiệm bội chẵn.
    3. Bội của các nghiệm: x = -3 bội 2, x = 0 bội 1.
    4. Số điểm cực trị: 1.
  - **Câu hỏi:** Hàm số f(x) = -3x^4 + 8x^3 - 6x^2 có bao nhiêu điểm cực trị?
  - **Đáp án:** 1
    1. f'(x) = -12x^3 + 24x^2 - 12x = -12x(x - 1)^2.
    2. f' đổi dấu khi đi qua một nghiệm bội lẻ, không đổi dấu qua một nghiệm bội chẵn.
    3. Bội của các nghiệm: x = 0 bội 1, x = 1 bội 2.
    4. Số điểm cực trị: 1.

### Giá trị lớn nhất và nhỏ nhất trên đoạn (`gt_t6_gtln_gtnn`)

- `gt_t6_gl_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = x^2 - 4x + 1 trên đoạn [0, 5]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 6, -3
    1. f'(x) = 2x - 4 = 0 tại x = 2, nằm trong (0, 5); f(2) = -3.
    2. Hai đầu: f(0) = 1, f(5) = 25 - 20 + 1 = 6.
    3. So ba giá trị: GTLN = 6 (tại x = 5), GTNN = -3 (tại x = 2).
- `gt_t6_gl_02` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm GTLN và GTNN của f(x) = x^3 - 3x trên đoạn [0, 3].
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 3x^2 - 3 = 0 khi x = 1 hoặc x = -1.
    2. Chỉ x = 1 nằm trong [0, 3]; f(1) = -2.
    3. f''(1) = 6 > 0 nên x = 1 là điểm cực tiểu.
    4. Vậy GTNN là -2, còn trên [0, 3] hàm không có GTLN vì không có điểm cực đại.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vậy GTNN là -2, còn trên [0, 3] hàm không có GTLN vì không có điểm cực đại.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: trên một đoạn đóng còn phải xét hai đầu mút; hàm liên tục trên đoạn luôn có GTLN.
    2. f(0) = 0 và f(3) = 27 - 9 = 18.
    3. GTLN = 18 (tại x = 3), GTNN = -2 (tại x = 1).
- `gt_t6_gl_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giá trị nhỏ nhất của f(x) = x + 4/x trên khoảng (0, +vô cùng) là bao nhiêu?
    - **(đúng)** 4
    - 2
    - 5
    - Không có giá trị nhỏ nhất
  - **Đáp án:** 4
    1. f'(x) = 1 - 4/x^2 = 0 khi x = 2 (x > 0).
    2. f' < 0 trên (0, 2) và f' > 0 trên (2, +vô cùng): x = 2 là điểm cực tiểu duy nhất.
    3. Nên GTNN là f(2) = 2 + 2 = 4.
- `gt_t6_gl_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi hàm liên tục trên khoảng mở (0, 1) đều đạt giá trị lớn nhất trên khoảng đó.
  - **Đáp án:** Sai
    1. Định lý Weierstrass chỉ áp dụng cho đoạn đóng [a, b].
    2. Phản ví dụ: f(x) = x trên (0, 1) tiến gần 1 nhưng không đạt 1; f(x) = 1/x còn không bị chặn.
    3. Mệnh đề sai.
- `gt_g6_x_nghich` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = x + 4/x trên đoạn [5, 6]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 20/3, 29/5
    1. f'(x) = 1 - 4/x^2 = (x^2 - 4) / x^2, bằng 0 tại x = 2 (xét x > 0).
    2. x = 2 không nằm trong (5, 6): f đơn điệu trên đoạn.
    3. Hai đầu đoạn: f(5) = 29/5, f(6) = 20/3.
    4. GTLN = 20/3, GTNN = 29/5.
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = x + 1/x trên đoạn [1, 2]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 5/2, 2
    1. f'(x) = 1 - 1/x^2 = (x^2 - 1) / x^2, bằng 0 tại x = 1 (xét x > 0).
    2. x = 1 không nằm trong (1, 2): f đơn điệu trên đoạn.
    3. Hai đầu đoạn: f(1) = 2, f(2) = 5/2.
    4. GTLN = 5/2, GTNN = 2.
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = x + 4/x trên đoạn [5, 6]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 20/3, 29/5
    1. f'(x) = 1 - 4/x^2 = (x^2 - 4) / x^2, bằng 0 tại x = 2 (xét x > 0).
    2. x = 2 không nằm trong (5, 6): f đơn điệu trên đoạn.
    3. Hai đầu đoạn: f(5) = 29/5, f(6) = 20/3.
    4. GTLN = 20/3, GTNN = 29/5.
- `gt_t6_gl_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên đoạn [-1, 2], hàm trùng phương f(x) = x^4 - 2x^2 + 3 đạt giá trị lớn nhất M và giá trị nhỏ nhất m. Nhập M, m theo đúng thứ tự.
  - **Đáp án:** 11, 2
    1. f'(x) = 4x^3 - 4x = 4x(x - 1)(x + 1): các điểm tới hạn -1, 0, 1 (trong đó -1 là đầu mút).
    2. f(-1) = 2, f(0) = 3, f(1) = 2, f(2) = 16 - 8 + 3 = 11.
    3. GTLN = 11 (tại x = 2), GTNN = 2 (tại x = -1 và x = 1).
- `gt_t6_gl_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Từ một tấm tôn hình vuông cạnh 12, cắt bỏ ở bốn góc bốn hình vuông bằng nhau cạnh x rồi gấp lên thành một cái hộp không nắp. Tính thể tích lớn nhất của hộp.
  - **Đáp án:** 128
    1. Đáy là hình vuông cạnh 12 - 2x, chiều cao x, với 0 < x < 6: V(x) = x(12 - 2x)^2.
    2. V'(x) = (12 - 2x)^2 - 4x(12 - 2x) = (12 - 2x)(12 - 6x), bằng 0 tại x = 2 trong (0, 6).
    3. V' đổi dấu từ + sang - tại x = 2, nên đó là GTLN: V(2) = 2 . 8^2 = 128.
- `gt_t6_gl_07` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm GTLN và GTNN của một hàm f liên tục trên đoạn [a, b] và khả vi trên (a, b).
  - **Đáp án (thứ tự đúng):**
    1. Tính f'(x) và tìm các điểm trong (a, b) mà f'(x) = 0.
    2. Tính giá trị của f tại các điểm vừa tìm được.
    3. Tính thêm f(a) và f(b) ở hai đầu đoạn.
    4. So sánh tất cả các giá trị đã tính: số lớn nhất là GTLN, số nhỏ nhất là GTNN.
  - **Lời giải:**
    1. GTLN, GTNN trên đoạn đạt ở điểm tới hạn hoặc ở đầu mút.
    2. Không cần xét cực đại hay cực tiểu: chỉ cần so các giá trị.
- `gt_t6_gl_08` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giá trị lớn nhất của f(x) = x^3 - 3x trên đoạn [-2, 1] bằng 2.
  - **Đáp án:** Đúng
    1. f'(x) = 3x^2 - 3 = 0 tại x = -1 và x = 1 (x = 1 là đầu mút).
    2. f(-2) = -8 + 6 = -2, f(-1) = -1 + 3 = 2, f(1) = 1 - 3 = -2.
    3. GTLN = 2 tại x = -1: mệnh đề đúng.
- `gt_t6_gl_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x) = 2x^3 - 9x^2 + 12x + 1 xét trên đoạn [0, 3].
  - **Phần a** (Điền số): a) Nhập các nghiệm của f'(x) = 0 theo thứ tự tăng dần.
    - **Đáp án a:** 1, 2
  - **Phần b** (Trắc nghiệm): b) x = 1 là điểm gì của f?
    - **(đúng)** Điểm cực đại
    - Điểm cực tiểu
    - Không phải điểm cực trị
    - **Đáp án b:** Điểm cực đại
  - **Phần c** (Điền số): c) Nhập GTLN rồi GTNN của f trên [0, 3].
    - **Đáp án c:** 10, 1
  - **Lời giải:**
    1. a) f'(x) = 6x^2 - 18x + 12 = 6(x - 1)(x - 2): nghiệm 1 và 2.
    2. b) f' > 0 khi x < 1 và f' < 0 khi 1 < x < 2: f' đổi từ + sang -, nên x = 1 là cực đại.
    3. c) f(0) = 1, f(1) = 6, f(2) = 5, f(3) = 10. GTLN = 10 ở đầu mút x = 3 (lớn hơn cả giá trị cực đại 6), GTNN = 1 ở đầu mút x = 0.
- `gt_g6_gtln` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = 2x^3 + 3x^2 - 12x - 4 trên đoạn [-3, -2]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 16, 5
    1. f'(x) = 6(x + 2)(x - 1), bằng 0 tại x = -2 và x = 1.
    2. Điểm tới hạn nằm trong khoảng (-3, -2): không có.
    3. So các giá trị tại điểm tới hạn và hai đầu đoạn: f(-3) = 5, f(-2) = 16.
    4. GTLN = 16, GTNN = 5.
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = 2x^3 - 54x - 4 trên đoạn [-4, 2]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 104, -96
    1. f'(x) = 6(x + 3)(x - 3), bằng 0 tại x = -3 và x = 3.
    2. Điểm tới hạn nằm trong khoảng (-4, 2): -3.
    3. So các giá trị tại điểm tới hạn và hai đầu đoạn: f(-4) = 84, f(-3) = 104, f(2) = -96.
    4. GTLN = 104, GTNN = -96.
  - **Câu hỏi:** Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = 2x^3 + 3x^2 - 12x + 3 trên đoạn [-4, 0]. Nhập GTLN rồi GTNN.
  - **Đáp án:** 23, -29
    1. f'(x) = 6(x + 2)(x - 1), bằng 0 tại x = -2 và x = 1.
    2. Điểm tới hạn nằm trong khoảng (-4, 0): -2.
    3. So các giá trị tại điểm tới hạn và hai đầu đoạn: f(-4) = -29, f(-2) = 23, f(0) = 3.
    4. GTLN = 23, GTNN = -29.

### Lồi, lõm và điểm uốn (`gt_t6_loi_lom`)

- `gt_t6_ll_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm điểm uốn (x0, y0) của đồ thị y = x^3 - 6x^2 + 5. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** 2, -11
    1. y' = 3x^2 - 12x, y'' = 6x - 12.
    2. y'' = 0 tại x = 2 và đổi dấu từ - sang + qua đó.
    3. y(2) = 8 - 24 + 5 = -11: điểm uốn (2, -11).
- `gt_t6_ll_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f có đạo hàm cấp hai trên R: nếu f''(x0) = 0 thì (x0, f(x0)) là điểm uốn của đồ thị.
  - **Đáp án:** Sai
    1. Điểm uốn là nơi f'' đổi dấu (đồ thị đổi chiều cong), không chỉ nơi f'' bằng 0.
    2. Phản ví dụ f(x) = x^4: f''(0) = 0 nhưng f''(x) = 12x^2 >= 0 hai bên, đồ thị cong lên ở cả hai phía.
    3. Mệnh đề sai.
- `gt_t6_ll_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = x^4 - 6x^2 lõm (y'' < 0, cong xuống) trên khoảng nào?
    - **(đúng)** (-1, 1)
    - (-vô cùng, -1) và (1, +vô cùng)
    - (-sqrt(3), sqrt(3))
    - (0, +vô cùng)
  - **Đáp án:** (-1, 1)
    1. y' = 4x^3 - 12x, y'' = 12x^2 - 12 = 12(x - 1)(x + 1).
    2. y'' < 0 khi -1 < x < 1.
    3. (-sqrt(3), sqrt(3)) là nơi y' đổi dấu, dùng cho cực trị, không phải cho lồi lõm.
- `gt_t6_ll_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét lồi lõm của đồ thị y = x . e^x (lồi khi y'' > 0, lõm khi y'' < 0).
  - **Lời giải đưa ra (có một bước sai):**
    1. y' = e^x + x e^x = (x + 1) e^x.
    2. y'' = e^x + (x + 1) e^x = (x + 2) e^x.
    3. e^x > 0, nên y'' < 0 khi x > -2: đồ thị lõm trên (-2, +vô cùng).   **<- bước sai đầu tiên**
    4. Điểm uốn có hoành độ x = -2.
  - **Đáp án:** Bước 3: e^x > 0, nên y'' < 0 khi x > -2: đồ thị lõm trên (-2, +vô cùng).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai dấu: x > -2 cho x + 2 > 0, nên y'' > 0.
    2. Đúng là đồ thị lồi (cong lên) trên (-2, +vô cùng) và lõm trên (-vô cùng, -2).
    3. y'' đổi dấu tại x = -2 nên vẫn có điểm uốn (-2, -2e^(-2)).
- `gt_g6_diem_uon` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm điểm uốn (x0, y0) của đồ thị y = -x^3 + 3x^2 + 6x + 6. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** 1, 14
    1. y' = -3x^2 + 6x + 6, y'' = -6x + 6.
    2. y'' = 0 tại x = 1, và y'' là hàm bậc nhất nên đổi dấu qua 1.
    3. y(1) = 14: điểm uốn (1, 14).
  - **Câu hỏi:** Tìm điểm uốn (x0, y0) của đồ thị y = -2x^3 - 18x^2 - 5x - 1. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -3, -94
    1. y' = -6x^2 - 36x - 5, y'' = -12x - 36.
    2. y'' = 0 tại x = -3, và y'' là hàm bậc nhất nên đổi dấu qua -3.
    3. y(-3) = -94: điểm uốn (-3, -94).
  - **Câu hỏi:** Tìm điểm uốn (x0, y0) của đồ thị y = -x^3 + 3x^2 + 2x - 4. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** 1, 0
    1. y' = -3x^2 + 6x + 2, y'' = -6x + 6.
    2. y'' = 0 tại x = 1, và y'' là hàm bậc nhất nên đổi dấu qua 1.
    3. y(1) = 0: điểm uốn (1, 0).
- `gt_t6_ll_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm a, b để đồ thị y = ax^3 + bx^2 nhận điểm (1, 3) làm điểm uốn. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -3/2, 9/2
    1. Điểm (1, 3) nằm trên đồ thị: a + b = 3.
    2. y'' = 6ax + 2b phải bằng 0 tại x = 1: 6a + 2b = 0, tức b = -3a.
    3. a - 3a = 3 cho a = -3/2, b = 9/2; khi đó y'' = -9x + 9 đổi dấu qua 1 nên đúng là điểm uốn.
- `gt_t6_ll_06` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm các điểm uốn của đồ thị y = x^4 - 4x^3.
  - **Đáp án (thứ tự đúng):**
    1. Tính y'' = 12x^2 - 24x = 12x(x - 2).
    2. Giải y'' = 0 được x = 0 và x = 2.
    3. Xét dấu: y'' > 0 trên (-vô cùng, 0), y'' < 0 trên (0, 2), y'' > 0 trên (2, +vô cùng).
    4. y'' đổi dấu qua cả hai điểm: hai điểm uốn (0, 0) và (2, -16).
  - **Lời giải:**
    1. Nghiệm của y'' chỉ là ứng viên; phải kiểm tra y'' đổi dấu.
    2. y(2) = 16 - 32 = -16.
- `gt_t6_ll_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f có đạo hàm cấp hai trên (a, b): nếu f''(x) > 0 với mọi x thuộc (a, b) thì trên (a, b) đồ thị của f nằm phía trên mọi tiếp tuyến của nó (trừ tại tiếp điểm).
  - **Đáp án:** Đúng
    1. Khai triển Taylor quanh tiếp điểm x0: f(x) = f(x0) + f'(x0)(x - x0) + f''(c)(x - x0)^2 / 2.
    2. Hai số hạng đầu chính là tiếp tuyến; số hạng cuối dương khi x khác x0 vì f''(c) > 0.
    3. Nên đồ thị nằm trên tiếp tuyến: mệnh đề đúng.
- `gt_t6_ll_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x) = x^4 - 6x^2 + 8x.
  - **Phần a** (Điền số): a) Nhập các nghiệm của f''(x) = 0 theo thứ tự tăng dần.
    - **Đáp án a:** -1, 1
  - **Phần b** (Đúng/Sai): b) Đồ thị của f có đúng hai điểm uốn.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Nhập các nghiệm phân biệt của f'(x) = 0 theo thứ tự tăng dần.
    - **Đáp án c:** -2, 1
  - **Phần d** (Điền số): d) f có bao nhiêu điểm cực trị?
    - **Đáp án d:** 1
  - **Lời giải:**
    1. a) f'(x) = 4x^3 - 12x + 8, f''(x) = 12x^2 - 12 = 12(x - 1)(x + 1): nghiệm -1 và 1.
    2. b) f'' đổi dấu qua cả -1 và 1 (dương ngoài, âm trong): đúng hai điểm uốn.
    3. c) f'(x) = 4(x^3 - 3x + 2) = 4(x - 1)^2(x + 2): nghiệm -2 và 1 (1 là nghiệm kép).
    4. d) f' đổi dấu qua -2 (từ - sang +) nhưng không đổi dấu qua nghiệm kép 1: chỉ có 1 điểm cực trị, là cực tiểu tại x = -2.
- `gt_g6_uon_tf` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị của f(x) = x^4 - 2x^3 + 5x^2 có hai điểm uốn.
  - **Đáp án:** Sai
    1. f''(x) = 12x^2 - 12x + 10, tam thức bậc hai có biệt thức (-12)^2 - 4 . 12 . 10 = -336.
    2. Biệt thức <= 0: f'' không đổi dấu (nghiệm kép, nếu có, không làm đổi dấu), nên đồ thị không có điểm uốn.
    3. Mệnh đề sai.
  - **Câu hỏi:** Đồ thị của f(x) = x^4 - 4x^3 - 3x^2 có hai điểm uốn.
  - **Đáp án:** Đúng
    1. f''(x) = 12x^2 - 24x - 6, tam thức bậc hai có biệt thức (-24)^2 - 4 . 12 . (-6) = 864.
    2. Biệt thức dương: f'' có hai nghiệm phân biệt và đổi dấu qua cả hai, nên đồ thị có hai điểm uốn.
    3. Mệnh đề đúng.
  - **Câu hỏi:** Đồ thị của f(x) = x^4 - x^3 + 5x^2 có hai điểm uốn.
  - **Đáp án:** Sai
    1. f''(x) = 12x^2 - 6x + 10, tam thức bậc hai có biệt thức (-6)^2 - 4 . 12 . 10 = -444.
    2. Biệt thức <= 0: f'' không đổi dấu (nghiệm kép, nếu có, không làm đổi dấu), nên đồ thị không có điểm uốn.
    3. Mệnh đề sai.

### Tiệm cận (`gt_t6_tiem_can`)

- `gt_t6_tc_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = (2x + 1) / (x - 3) có tiệm cận đứng x = x0 và tiệm cận ngang y = y0. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** 3, 2
    1. Mẫu bằng 0 tại x = 3, tử tại đó bằng 7 khác 0: y -> vô cùng, tiệm cận đứng x = 3.
    2. Khi x -> vô cùng, y -> 2/1 = 2: tiệm cận ngang y = 2.
- `gt_t6_tc_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tiệm cận xiên của đồ thị y = (x^2 + 1) / x là đường nào?
    - **(đúng)** y = x
    - y = x + 1
    - x = 0
    - Không có tiệm cận xiên
  - **Đáp án:** y = x
    1. Viết y = x + 1/x.
    2. 1/x -> 0 khi x -> vô cùng, nên y - x -> 0.
    3. Tiệm cận xiên y = x (x = 0 là tiệm cận đứng).
- `gt_t6_tc_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = (x^2 - 4) / (x - 2) có tiệm cận đứng x = 2.
  - **Đáp án:** Sai
    1. Với x khác 2: y = (x - 2)(x + 2) / (x - 2) = x + 2.
    2. Khi x -> 2, y -> 4, hữu hạn: x = 2 chỉ là điểm gián đoạn khử được.
    3. Tiệm cận đứng cần y -> vô cùng, nên mệnh đề sai.
- `gt_t6_tc_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm tiệm cận xiên của y = (2x^2 + 3x) / (x + 1).
  - **Lời giải đưa ra (có một bước sai):**
    1. Hệ số góc: a = giới hạn của y/x = giới hạn của (2x^2 + 3x) / (x^2 + x) khi x -> vô cùng, bằng 2.
    2. b = giới hạn của y - 2x = giới hạn của (2x^2 + 3x - 2x^2 - 2x) / (x + 1).
    3. Giới hạn đó là giới hạn của x / (x + 1), bằng 0.   **<- bước sai đầu tiên**
    4. Tiệm cận xiên: y = 2x.
  - **Đáp án:** Bước 3: Giới hạn đó là giới hạn của x / (x + 1), bằng 0.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: x / (x + 1) -> 1 khi x -> vô cùng, không phải 0.
    2. Vậy b = 1 và tiệm cận xiên là y = 2x + 1.
    3. Kiểm tra bằng phép chia: 2x^2 + 3x = (x + 1)(2x + 1) - 1.
- `gt_g6_tiem_can` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = (-3x + 3) / (-3x - 2) có tiệm cận đứng x = x0 và tiệm cận ngang y = y0. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -2/3, 1
    1. Mẫu bằng 0 tại x = -2/3, còn tử tại đó khác 0 (vì -3 . (-2) - 3 . (-3) khác 0), nên y -> vô cùng: tiệm cận đứng x = -2/3.
    2. Khi x -> vô cùng, y -> -3 / (-3) = 1: tiệm cận ngang y = 1.
    3. Đáp án: -2/3, 1.
  - **Câu hỏi:** Đồ thị y = (-5x - 5) / (-3x - 1) có tiệm cận đứng x = x0 và tiệm cận ngang y = y0. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -1/3, 5/3
    1. Mẫu bằng 0 tại x = -1/3, còn tử tại đó khác 0 (vì -5 . (-1) - (-5) . (-3) khác 0), nên y -> vô cùng: tiệm cận đứng x = -1/3.
    2. Khi x -> vô cùng, y -> -5 / (-3) = 5/3: tiệm cận ngang y = 5/3.
    3. Đáp án: -1/3, 5/3.
  - **Câu hỏi:** Đồ thị y = (-2x + 3) / (2x - 4) có tiệm cận đứng x = x0 và tiệm cận ngang y = y0. Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** 2, -1
    1. Mẫu bằng 0 tại x = 2, còn tử tại đó khác 0 (vì -2 . (-4) - 3 . 2 khác 0), nên y -> vô cùng: tiệm cận đứng x = 2.
    2. Khi x -> vô cùng, y -> -2 / 2 = -1: tiệm cận ngang y = -1.
    3. Đáp án: 2, -1.
- `gt_g6_tiem_can_xien` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = (-2x^2 + 4x + 6) / (x + 3) có tiệm cận xiên y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -2, 10
    1. Chia đa thức: -2x^2 + 4x + 6 = (x + 3)(-2x + 10) + (-24).
    2. Nên y = -2x + 10 + (-24) / (x + 3).
    3. Phần (-24) / (x + 3) -> 0 khi x -> vô cùng: tiệm cận xiên y = -2x + 10.
    4. p = -2, q = 10.
  - **Câu hỏi:** Đồ thị y = (-3x^2 - 4x - 5) / (x - 1) có tiệm cận xiên y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -3, -7
    1. Chia đa thức: -3x^2 - 4x - 5 = (x - 1)(-3x - 7) + (-12).
    2. Nên y = -3x - 7 + (-12) / (x - 1).
    3. Phần (-12) / (x - 1) -> 0 khi x -> vô cùng: tiệm cận xiên y = -3x - 7.
    4. p = -3, q = -7.
  - **Câu hỏi:** Đồ thị y = (-2x^2 + 4x + 2) / (x + 2) có tiệm cận xiên y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -2, 8
    1. Chia đa thức: -2x^2 + 4x + 2 = (x + 2)(-2x + 8) + (-14).
    2. Nên y = -2x + 8 + (-14) / (x + 2).
    3. Phần (-14) / (x + 2) -> 0 khi x -> vô cùng: tiệm cận xiên y = -2x + 8.
    4. p = -2, q = 8.
- `gt_t6_tc_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi x -> +vô cùng, đồ thị y = sqrt(x^2 + 2x) có tiệm cận xiên y = px + q. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 1, 1
    1. p = giới hạn của sqrt(x^2 + 2x) / x = giới hạn của sqrt(1 + 2/x) = 1.
    2. q = giới hạn của sqrt(x^2 + 2x) - x = giới hạn của 2x / (sqrt(x^2 + 2x) + x) = 2/2 = 1.
    3. Tiệm cận y = x + 1 (khi x -> -vô cùng thì lại là y = -x - 1).
- `gt_t6_tc_06` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với các tiệm cận của đồ thị của nó.
  - **Đáp án (ghép đúng):**
    - y = (x + 1) / (x - 2) — x = 2 và y = 1
    - y = x^2 / (x - 1) — x = 1 và y = x + 1
    - y = e^x — chỉ y = 0, khi x -> -vô cùng
    - y = ln x — chỉ x = 0, khi x -> 0+
  - **Lời giải:**
    1. (x + 1)/(x - 2): mẫu bằng 0 tại 2, bậc tử bằng bậc mẫu nên tiệm cận ngang y = 1.
    2. x^2/(x - 1) = x + 1 + 1/(x - 1): tiệm cận đứng x = 1, tiệm cận xiên y = x + 1.
    3. e^x -> 0 khi x -> -vô cùng; ln x -> -vô cùng khi x -> 0+.
- `gt_t6_tc_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = x + sin x có tiệm cận xiên y = x khi x -> +vô cùng.
  - **Đáp án:** Sai
    1. Tiệm cận xiên y = x cần y - x -> 0.
    2. y - x = sin x dao động mãi giữa -1 và 1, không dần tới 0.
    3. Dù y/x -> 1, đồ thị không có tiệm cận xiên: mệnh đề sai.

### Lược đồ khảo sát hàm số (`gt_t6_khao_sat`)

- `gt_t6_ks_01` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khảo sát f(x) = x^3 - 3x^2. Sắp xếp các bước, mỗi bước dùng kết quả của bước trước.
  - **Đáp án (thứ tự đúng):**
    1. Tính f'(x) = 3x^2 - 6x = 3x(x - 2).
    2. Từ dạng nhân tử: f' > 0 trên (-vô cùng, 0) và (2, +vô cùng), f' < 0 trên (0, 2).
    3. Từ bảng dấu của f': cực đại f(0) = 0, cực tiểu f(2) = -4.
    4. Từ hai điểm cực trị: đồ thị đi lên tới (0, 0), xuống tới (2, -4), rồi đi lên mãi.
  - **Lời giải:**
    1. Đạo hàm cho bảng dấu, bảng dấu cho cực trị, cực trị cho dáng đồ thị.
    2. f(2) = 8 - 12 = -4.
- `gt_t6_ks_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào đồng biến trên (-vô cùng, -1), nghịch biến trên (-1, 1), đồng biến trên (1, +vô cùng), với cực đại f(-1) = 2 và cực tiểu f(1) = -2?
    - **(đúng)** f(x) = x^3 - 3x
    - f(x) = -x^3 + 3x
    - f(x) = x^3 + 3x
    - f(x) = x^3 - 3x + 2
  - **Đáp án:** f(x) = x^3 - 3x
    1. x^3 - 3x có f' = 3(x - 1)(x + 1): dương ngoài [-1, 1], âm bên trong; f(-1) = 2, f(1) = -2.
    2. -x^3 + 3x có chiều biến thiên ngược lại; x^3 + 3x luôn đồng biến.
    3. x^3 - 3x + 2 có đúng chiều biến thiên nhưng f(-1) = 4, f(1) = 0.
- `gt_t6_ks_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đồ thị y = x^3 - 3x nhận gốc tọa độ O làm tâm đối xứng.
  - **Đáp án:** Đúng
    1. f(-x) = -x^3 + 3x = -f(x) với mọi x: f là hàm lẻ.
    2. Điểm (x, y) thuộc đồ thị thì (-x, -y) cũng thuộc đồ thị.
    3. Vậy đồ thị đối xứng qua O (O cũng là điểm uốn của nó).
- `gt_t6_ks_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^3 - 3x = 1 có bao nhiêu nghiệm thực?
  - **Đáp án:** 3
    1. f(x) = x^3 - 3x có cực đại f(-1) = 2 và cực tiểu f(1) = -2.
    2. Đường ngang y = 1 nằm giữa -2 và 2.
    3. Nên nó cắt đồ thị ở 3 điểm: mỗi khoảng đơn điệu một nghiệm.
- `gt_t6_ks_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm mọi số nguyên m để phương trình x^3 - 3x^2 = m có ba nghiệm thực phân biệt. Nhập các giá trị đó.
  - **Đáp án:** -3, -2, -1  (thứ tự nào cũng được)
    1. f(x) = x^3 - 3x^2 có f'(x) = 3x(x - 2): cực đại f(0) = 0, cực tiểu f(2) = -4.
    2. Ba nghiệm phân biệt khi đường ngang y = m nằm hẳn giữa hai giá trị cực trị: -4 < m < 0.
    3. Các số nguyên: -3, -2, -1 (m = 0 hoặc m = -4 chỉ cho hai nghiệm).
- `gt_t6_ks_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: khảo sát y = x^2 / (x - 1).
  - **Lời giải đưa ra (có một bước sai):**
    1. Tập xác định R \ {1}.
    2. y' = (x^2 - 2x) / (x - 1)^2, bằng 0 tại x = 0 và x = 2.
    3. Cực đại y(0) = 0, cực tiểu y(2) = 4.
    4. Tiệm cận đứng x = 1 và tiệm cận xiên y = x.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Tiệm cận đứng x = 1 và tiệm cận xiên y = x.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai ở tiệm cận xiên: chia đa thức được x^2 = (x - 1)(x + 1) + 1, nên y = x + 1 + 1/(x - 1).
    2. Tiệm cận xiên đúng là y = x + 1.
    3. Ba bước đầu đúng: y' = (2x(x - 1) - x^2)/(x - 1)^2 = (x^2 - 2x)/(x - 1)^2.
- `gt_t6_ks_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^3 + 3x có hai điểm cực trị.
  - **Đáp án:** Sai
    1. f'(x) = 3x^2 + 3 > 0 với mọi x.
    2. f' không bao giờ bằng 0 hay đổi dấu, nên f đồng biến trên R.
    3. f không có điểm cực trị nào: mệnh đề sai.
- `gt_t6_ks_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: khảo sát f(x) = (x^2 + 3) / (x - 1).
  - **Phần a** (Điền số): a) Tiệm cận xiên là y = px + q. Nhập p, q theo đúng thứ tự.
    - **Đáp án a:** 1, 1
  - **Phần b** (Điền số): b) Nhập các nghiệm của f'(x) = 0 theo thứ tự tăng dần.
    - **Đáp án b:** -1, 3
  - **Phần c** (Điền số): c) Nhập giá trị cực đại rồi giá trị cực tiểu của f.
    - **Đáp án c:** -2, 6
  - **Phần d** (Đúng/Sai): d) Giá trị cực đại của f nhỏ hơn giá trị cực tiểu của f.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Chia đa thức: x^2 + 3 = (x - 1)(x + 1) + 4, nên f(x) = x + 1 + 4/(x - 1): tiệm cận xiên y = x + 1.
    2. b) f'(x) = 1 - 4/(x - 1)^2 = 0 khi (x - 1)^2 = 4, tức x = -1 hoặc x = 3.
    3. c) f' đổi từ + sang - tại -1 và từ - sang + tại 3: cực đại f(-1) = 4/(-2) = -2, cực tiểu f(3) = 12/2 = 6.
    4. d) -2 < 6: đúng. Không có gì lạ, vì hai điểm nằm trên hai nhánh khác nhau của đồ thị, ngăn bởi tiệm cận đứng x = 1.
- `gt_g6_so_nghiem` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình 2x^3 + 3x^2 - 12x = -7 có bao nhiêu nghiệm thực phân biệt?
  - **Đáp án:** 2
    1. Đặt f(x) = 2x^3 + 3x^2 - 12x: f'(x) = 6(x + 2)(x - 1).
    2. f tăng trên (-vô cùng, -2], giảm trên [-2, 1], tăng trên [1, +vô cùng); cực đại f(-2) = 20, cực tiểu f(1) = -7.
    3. Số nghiệm là số giao điểm của đồ thị với đường ngang y = m: 3 khi m nằm giữa hai giá trị cực trị, 2 khi m bằng một trong hai, 1 khi m nằm ngoài.
    4. Với m = -7: 2 nghiệm.
  - **Câu hỏi:** Phương trình 2x^3 - 54x = 108 có bao nhiêu nghiệm thực phân biệt?
  - **Đáp án:** 2
    1. Đặt f(x) = 2x^3 - 54x: f'(x) = 6(x + 3)(x - 3).
    2. f tăng trên (-vô cùng, -3], giảm trên [-3, 3], tăng trên [3, +vô cùng); cực đại f(-3) = 108, cực tiểu f(3) = -108.
    3. Số nghiệm là số giao điểm của đồ thị với đường ngang y = m: 3 khi m nằm giữa hai giá trị cực trị, 2 khi m bằng một trong hai, 1 khi m nằm ngoài.
    4. Với m = 108: 2 nghiệm.
  - **Câu hỏi:** Phương trình 2x^3 + 3x^2 - 12x = -7 có bao nhiêu nghiệm thực phân biệt?
  - **Đáp án:** 2
    1. Đặt f(x) = 2x^3 + 3x^2 - 12x: f'(x) = 6(x + 2)(x - 1).
    2. f tăng trên (-vô cùng, -2], giảm trên [-2, 1], tăng trên [1, +vô cùng); cực đại f(-2) = 20, cực tiểu f(1) = -7.
    3. Số nghiệm là số giao điểm của đồ thị với đường ngang y = m: 3 khi m nằm giữa hai giá trị cực trị, 2 khi m bằng một trong hai, 1 khi m nằm ngoài.
    4. Với m = -7: 2 nghiệm.

## Tầng 7: Tích phân bất định và tích phân xác định

44 dạng câu (38 câu viết tay, 6 bộ sinh câu); 44 chưa duyệt.

### Nguyên hàm và bảng nguyên hàm (`gt_t7_nguyen_ham`)

- `gt_t7_ng_01` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm số với một nguyên hàm của nó (C là hằng số tùy ý). Hãy biến đổi hàm số trước khi tra bảng.
  - **Đáp án (ghép đúng):**
    - tan^2 x — tan x - x + C
    - sin^2 x — x/2 - sin(2x)/4 + C
    - cos^2 x — x/2 + sin(2x)/4 + C
    - 1/(x^2 + 4) — (1/2) arctan(x/2) + C
  - **Lời giải:**
    1. tan^2 x = 1/cos^2 x - 1, nên nguyên hàm là tan x - x + C.
    2. Hạ bậc: sin^2 x = (1 - cos(2x))/2 và cos^2 x = (1 + cos(2x))/2; nguyên hàm của cos(2x) là sin(2x)/2.
    3. 1/(x^2 + 4) = (1/4) . 1/(1 + (x/2)^2); đặt t = x/2 được (1/2) arctan(x/2) + C.
    4. Kiểm tra bằng cách lấy đạo hàm vế phải: luôn ra đúng hàm ở vế trái.
- `gt_t7_ng_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** F là nguyên hàm của f(x) = 3x^2 - 4x + 1/x^2 trên (0, +vô cùng) và F(1) = 2. Tính F(2).
  - **Đáp án:** 7/2
    1. Nguyên hàm tổng quát: F(x) = x^3 - 2x^2 - 1/x + C (vì nguyên hàm của x^(-2) là -x^(-1)).
    2. F(1) = 1 - 2 - 1 + C = C - 2 = 2, nên C = 4.
    3. F(2) = 8 - 8 - 1/2 + 4 = 7/2.
- `gt_t7_ng_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên tập R \ {0}, hàm G(x) = ln|x| + 1 khi x > 0 và G(x) = ln|x| - 3 khi x < 0 cũng là một nguyên hàm của 1/x, dù G - ln|x| không phải là một hằng số.
  - **Đáp án:** Đúng
    1. Với x > 0: G'(x) = (ln x)' = 1/x. Với x < 0: G'(x) = (ln(-x))' = -1/(-x) = 1/x.
    2. Vậy G'(x) = 1/x tại mọi điểm của R \ {0}: G là một nguyên hàm.
    3. R \ {0} gồm hai khoảng rời nhau, nên trên mỗi khoảng được cộng một hằng số riêng. 'Hai nguyên hàm sai khác một hằng số' chỉ đúng trên một khoảng. Mệnh đề đúng.
- `gt_g7_nguyen_ham_dk` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** F là nguyên hàm của f(x) = -3x^2 + 4x - 3/x^2 trên (0, +vô cùng) và F(1) = -1. Tính F(2).
  - **Đáp án:** -7/2
    1. Nguyên hàm tổng quát: F(x) = -x^3 + 2x^2 + 3/x + C (nguyên hàm của 1/x^2 là -1/x).
    2. F(1) = 4 + C = -1, nên C = -5.
    3. F(2) = 3/2 + (-5) = -7/2.
  - **Câu hỏi:** F là nguyên hàm của f(x) = -6x^2 - 4x - 3/x^2 trên (0, +vô cùng) và F(1) = 0. Tính F(2).
  - **Đáp án:** -43/2
    1. Nguyên hàm tổng quát: F(x) = -2x^3 - 2x^2 + 3/x + C (nguyên hàm của 1/x^2 là -1/x).
    2. F(1) = -1 + C = 0, nên C = 1.
    3. F(2) = -45/2 + 1 = -43/2.
  - **Câu hỏi:** F là nguyên hàm của f(x) = -3x^2 + 4x - 2/x^2 trên (0, +vô cùng) và F(1) = 0. Tính F(2).
  - **Đáp án:** -2
    1. Nguyên hàm tổng quát: F(x) = -x^3 + 2x^2 + 2/x + C (nguyên hàm của 1/x^2 là -1/x).
    2. F(1) = 3 + C = 0, nên C = -3.
    3. F(2) = 1 + (-3) = -2.
- `gt_t7_ng_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong 'chứng minh' sau, đi tới một điều vô lý.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_ng_02`, `gt_t7_ng_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. (sin^2 x)' = 2 sin x cos x = sin(2x), nên sin^2 x là một nguyên hàm của sin(2x) trên R.
    2. (-cos^2 x)' = 2 cos x sin x = sin(2x), nên -cos^2 x cũng là một nguyên hàm của sin(2x) trên R.
    3. Hai nguyên hàm của cùng một hàm trên R thì bằng nhau.   **<- bước sai đầu tiên**
    4. Do đó sin^2 x = -cos^2 x, tức sin^2 x + cos^2 x = 0 với mọi x.
  - **Đáp án:** Bước 3: Hai nguyên hàm của cùng một hàm trên R thì bằng nhau.
  - **Vì sao sai, và bước đúng:**
    1. Hai bước đầu đúng: lấy đạo hàm lại đều ra sin(2x).
    2. Bước 3 sai: trên một khoảng, hai nguyên hàm của cùng một hàm chỉ sai khác nhau một hằng số, không nhất thiết bằng nhau.
    3. Thật vậy sin^2 x - (-cos^2 x) = 1: hằng số đó là 1, không có điều vô lý nào.
- `gt_t7_ng_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f có f''(x) = e^x + 6x với mọi x, f(0) = 1 và f'(0) = 2. Biết f(1) = e + k, tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_vp_05`, `gt_t7_ng_02`
  - **Đáp án:** 2
    1. Lấy nguyên hàm lần một: f'(x) = e^x + 3x^2 + C1. f'(0) = 1 + C1 = 2 nên C1 = 1.
    2. Lấy nguyên hàm lần hai: f(x) = e^x + x^3 + x + C2. f(0) = 1 + C2 = 1 nên C2 = 0.
    3. f(1) = e + 1 + 1 = e + 2, nên k = 2.

### Phương pháp đổi biến (`gt_t7_doi_bien`)

- `gt_t7_db_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 1 của x(x^2 + 1)^3 dx.
  - **Đáp án:** 15/8
    1. Đặt u = x^2 + 1, du = 2x dx, nên x dx = du/2. Đổi cận: x = 0 thì u = 1, x = 1 thì u = 2.
    2. Tích phân = (1/2) . tích phân từ 1 đến 2 của u^3 du = (1/2) . [u^4/4] từ 1 đến 2.
    3. = (1/8)(16 - 1) = 15/8.
- `gt_t7_db_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến sqrt(3) của x^3 . sqrt(1 + x^2) dx.
  - **Đáp án:** 58/15
    1. Đặt u = 1 + x^2: du = 2x dx và x^2 = u - 1, nên x^3 dx = x^2 . x dx = (u - 1) du/2. Cận: u từ 1 đến 4.
    2. Tích phân = (1/2) . tích phân từ 1 đến 4 của (u^(3/2) - u^(1/2)) du = (1/2)[(2/5)u^(5/2) - (2/3)u^(3/2)] từ 1 đến 4.
    3. Tại 4: (2/5) . 32 - (2/3) . 8 = 64/5 - 16/3 = 112/15. Tại 1: 2/5 - 2/3 = -4/15.
    4. Kết quả: (1/2)(112/15 + 4/15) = 58/15.
- `gt_t7_db_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính tích phân từ 1 đến 2 của 2x . e^(x^2) dx.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt u = x^2, khi đó du = 2x dx.
    2. Tích phân trở thành tích phân từ 1 đến 2 của e^u du.   **<- bước sai đầu tiên**
    3. = [e^u] lấy từ 1 đến 2.
    4. = e^2 - e.
  - **Đáp án:** Bước 2: Tích phân trở thành tích phân từ 1 đến 2 của e^u du.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: đổi biến thì phải đổi cả cận theo u = x^2.
    2. x = 1 cho u = 1, x = 2 cho u = 4: tích phân từ 1 đến 4 của e^u du.
    3. Kết quả đúng là e^4 - e.
- `gt_g7_doi_bien` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 3 của x(x^2 + 1)^2 dx.
  - **Đáp án:** 333/2
    1. Đặt u = x^2 + 1: du = 2x dx, nên x dx = du/2. Đổi cận: x = 0 thì u = 1, x = 3 thì u = 10.
    2. Tích phân = (1/2) . tích phân từ 1 đến 10 của u^2 du = (1/2) . [u^3/3] từ 1 đến 10.
    3. = 1/6 . (1000 - 1) = 333/2.
  - **Câu hỏi:** Tính tích phân từ 0 đến 1 của x(x^2 + 1)^2 dx.
  - **Đáp án:** 7/6
    1. Đặt u = x^2 + 1: du = 2x dx, nên x dx = du/2. Đổi cận: x = 0 thì u = 1, x = 1 thì u = 2.
    2. Tích phân = (1/2) . tích phân từ 1 đến 2 của u^2 du = (1/2) . [u^3/3] từ 1 đến 2.
    3. = 1/6 . (8 - 1) = 7/6.
  - **Câu hỏi:** Tính tích phân từ 0 đến 3 của x(x^2 + 3) dx.
  - **Đáp án:** 135/4
    1. Đặt u = x^2 + 3: du = 2x dx, nên x dx = du/2. Đổi cận: x = 0 thì u = 3, x = 3 thì u = 12.
    2. Tích phân = (1/2) . tích phân từ 3 đến 12 của u du = (1/2) . [u^2/2] từ 3 đến 12.
    3. = 1/4 . (144 - 9) = 135/4.
- `gt_t7_db_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f liên tục và lẻ trên [-a, a] (a > 0). Sắp xếp các bước chứng minh tích phân từ -a đến a của f(x) dx bằng 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_db_03`, `gt_t7_db_01`
  - **Đáp án (thứ tự đúng):**
    1. Tách: tích phân từ -a đến a = tích phân từ -a đến 0 + tích phân từ 0 đến a.
    2. Trong tích phân từ -a đến 0 của f(x) dx, đặt x = -t: dx = -dt, x = -a ứng với t = a, x = 0 ứng với t = 0.
    3. Được tích phân từ a đến 0 của f(-t)(-dt) = tích phân từ 0 đến a của f(-t) dt.
    4. f lẻ nên f(-t) = -f(t): phần này bằng -(tích phân từ 0 đến a của f(t) dt).
    5. Cộng với phần còn lại (tên biến không quan trọng) được 0.
  - **Lời giải:**
    1. Ý chính: phép đổi biến x = -t lật đoạn [-a, 0] thành [0, a].
    2. Dấu trừ của dx = -dt dùng để đảo lại thứ tự hai cận.
    3. Tính lẻ biến phần bên trái thành đúng phần bên phải với dấu ngược lại.
- `gt_t7_db_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến 4 của 1/(1 + sqrt(x)) dx bằng a + b ln 3 với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_db_01`, `gt_t7_db_02`
  - **Đáp án:** 4, -2
    1. Đặt t = sqrt(x): x = t^2, dx = 2t dt; x từ 0 đến 4 ứng với t từ 0 đến 2.
    2. Tích phân = tích phân từ 0 đến 2 của 2t/(1 + t) dt = 2 . tích phân từ 0 đến 2 của (1 - 1/(1 + t)) dt.
    3. = 2[t - ln(1 + t)] từ 0 đến 2 = 2(2 - ln 3) = 4 - 2 ln 3.
    4. Vậy a = 4, b = -2.

### Tích phân từng phần (`gt_t7_tung_phan`)

- `gt_t7_tp_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 1 đến e của x ln x dx bằng a . e^2 + b với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** 1/4, 1/4
    1. Đặt u = ln x, dv = x dx: du = dx/x, v = x^2/2.
    2. Tích phân = [x^2/2 . ln x] từ 1 đến e - tích phân từ 1 đến e của x/2 dx = e^2/2 - [x^2/4] từ 1 đến e.
    3. = e^2/2 - (e^2/4 - 1/4) = e^2/4 + 1/4. Vậy a = 1/4, b = 1/4.
- `gt_t7_tp_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính nguyên hàm của x^2 . ln x (x > 0) bằng tích phân từng phần. Cách chọn u và dv nào cho ngay, sau một lần dùng công thức, một tích phân mới không còn chứa ln x?
    - **(đúng)** u = ln x, dv = x^2 dx
    - u = x^2, dv = ln x dx
    - u = x^2 ln x, dv = dx
    - u = x, dv = x ln x dx
  - **Đáp án:** u = ln x, dv = x^2 dx
    1. u = ln x cho du = dx/x, v = x^3/3; tích phân mới là nguyên hàm của v du = x^2/3 dx: không còn ln.
    2. u = x^2, dv = ln x dx cho v = x ln x - x, và v du = (x ln x - x) . 2x dx vẫn chứa ln x. Hai cách còn lại cũng để lại ln x trong tích phân mới.
    3. Quy tắc nhớ: chọn u là hàm mà đạo hàm đơn giản hơn (ln, arctan), dv là phần dễ lấy nguyên hàm.
- `gt_t7_tp_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm nguyên hàm của x cos x.
  - **Lời giải đưa ra (có một bước sai):**
    1. Đặt u = x, dv = cos x dx.
    2. Khi đó du = dx, v = sin x.
    3. Nguyên hàm = x sin x - nguyên hàm của sin x.
    4. = x sin x - cos x + C.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: = x sin x - cos x + C.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng theo công thức nguyên hàm của u dv = uv - nguyên hàm của v du.
    2. Bước 4 sai dấu: nguyên hàm của sin x là -cos x, nên trừ đi nó được + cos x.
    3. Đúng là x sin x + cos x + C; kiểm tra: (x sin x + cos x)' = sin x + x cos x - sin x = x cos x.
- `gt_g7_tung_phan` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến 1 của (-2x - 3) e^x dx bằng p . e + q với p, q hữu tỉ. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -3, 1
    1. Từng phần: u = -2x - 3, dv = e^x dx, nên du = -2 dx, v = e^x.
    2. Nguyên hàm: (-2x - 3) e^x - (-2) e^x = (-2x - 1) e^x.
    3. Tại x = 1: -3 . e. Tại x = 0: -1.
    4. Tích phân = -3 . e - (-1): p = -3, q = 1.
  - **Câu hỏi:** Tích phân từ 0 đến 1 của (-4x - 3) e^x dx bằng p . e + q với p, q hữu tỉ. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** -3, -1
    1. Từng phần: u = -4x - 3, dv = e^x dx, nên du = -4 dx, v = e^x.
    2. Nguyên hàm: (-4x - 3) e^x - (-4) e^x = (-4x + 1) e^x.
    3. Tại x = 1: -3 . e. Tại x = 0: 1.
    4. Tích phân = -3 . e - 1: p = -3, q = -1.
  - **Câu hỏi:** Tích phân từ 0 đến 1 của (-x + 4) e^x dx bằng p . e + q với p, q hữu tỉ. Nhập p, q theo đúng thứ tự.
  - **Đáp án:** 4, -5
    1. Từng phần: u = -x + 4, dv = e^x dx, nên du = -1 dx, v = e^x.
    2. Nguyên hàm: (-x + 4) e^x - (-1) e^x = (-x + 5) e^x.
    3. Tại x = 1: 4 . e. Tại x = 0: 5.
    4. Tích phân = 4 . e - 5: p = 4, q = -5.
- `gt_t7_tp_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến pi của e^x sin x dx bằng a . e^pi + b với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_tp_03`, `gt_t7_tp_01`
  - **Đáp án:** 1/2, 1/2
    1. Gọi J là nguyên hàm của e^x sin x. Từng phần hai lần (lần nào cũng chọn dv = e^x dx): J = e^x sin x - (e^x cos x + J).
    2. Phương trình J = e^x sin x - e^x cos x - J cho J = e^x(sin x - cos x)/2 + C.
    3. Tại pi: e^pi(0 - (-1))/2 = e^pi/2. Tại 0: (0 - 1)/2 = -1/2.
    4. Tích phân = e^pi/2 + 1/2: a = 1/2, b = 1/2.
- `gt_t7_tp_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đặt I_n = tích phân từ 0 đến 1 của x^n e^x dx (n là số tự nhiên). Sắp xếp các bước lập công thức truy hồi rồi tính I_2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_tp_02`, `gt_t7_tp_01`
  - **Đáp án (thứ tự đúng):**
    1. Với n >= 1, đặt u = x^n, dv = e^x dx: du = n x^(n-1) dx, v = e^x.
    2. Công thức từng phần: I_n = [x^n e^x] từ 0 đến 1 - n . tích phân từ 0 đến 1 của x^(n-1) e^x dx.
    3. Thay cận: [x^n e^x] từ 0 đến 1 = e - 0 = e, vì n >= 1.
    4. Được công thức truy hồi I_n = e - n I_(n-1).
    5. Từ I_0 = e - 1: I_1 = e - (e - 1) = 1, rồi I_2 = e - 2 . 1 = e - 2.
  - **Lời giải:**
    1. Mỗi lần dùng từng phần, lũy thừa của x giảm đi một: đó là lý do chọn u = x^n.
    2. Tích phân còn lại chính là I_(n-1), nên được công thức truy hồi.
    3. Kiểm tra I_2 bằng nguyên hàm (x^2 - 2x + 2)e^x: tại 1 được e, tại 0 được 2, hiệu e - 2.
- `gt_t7_tp_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: tính I = tích phân từ 0 đến 1 của arctan x dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_tp_02`, `gt_t7_db_01`, `gt_t7_tp_01`
  - **Phần a** (Trắc nghiệm): a) Chọn u và dv cho tích phân từng phần.
    - **(đúng)** u = arctan x, dv = dx
    - u = 1, dv = arctan x dx
    - u = x, dv = arctan x dx
    - Không dùng được từng phần
    - **Đáp án a:** u = arctan x, dv = dx
  - **Phần b** (Điền số): b) Sau một lần dùng công thức, phải tính thêm J = tích phân từ 0 đến 1 của x/(1 + x^2) dx. Biết J = k . ln 2, tìm k.
    - **Đáp án b:** 1/2
  - **Phần c** (Điền số): c) I = a . pi + b . ln 2 với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
    - **Đáp án c:** 1/4, -1/2
  - **Lời giải:**
    1. a) Chưa biết nguyên hàm của arctan x nhưng biết đạo hàm của nó: u = arctan x, dv = dx, nên du = dx/(1 + x^2), v = x.
    2. b) Đặt w = 1 + x^2, dw = 2x dx: J = (1/2)[ln w] từ 1 đến 2 = (1/2) ln 2, nên k = 1/2.
    3. c) I = [x arctan x] từ 0 đến 1 - J = arctan 1 - (1/2) ln 2 = pi/4 - (1/2) ln 2: a = 1/4, b = -1/2.

### Tích phân hàm hữu tỉ và lượng giác (`gt_t7_ham_huu_ty`)

- `gt_t7_ht_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 2 đến 3 của 1/(x^2 - 1) dx bằng a ln 2 + b ln 3 với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
  - **Đáp án:** -1/2, 1/2
    1. Tách: 1/(x^2 - 1) = (1/2)(1/(x - 1) - 1/(x + 1)).
    2. Nguyên hàm: (1/2) ln|(x - 1)/(x + 1)|. Tại 3: (1/2) ln(1/2); tại 2: (1/2) ln(1/3).
    3. Hiệu: (1/2)(ln(1/2) - ln(1/3)) = (1/2)(ln 3 - ln 2) = -(1/2) ln 2 + (1/2) ln 3.
- `gt_t7_ht_02` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phân thức với cách tách nó thành tổng các phân thức đơn giản.
  - **Đáp án (ghép đúng):**
    - (2x + 1)/((x - 1)(x + 2)) — 1/(x - 1) + 1/(x + 2)
    - 1/(x(x + 1)) — 1/x - 1/(x + 1)
    - 1/(x^2 - 4) — (1/4)/(x - 2) - (1/4)/(x + 2)
    - (x + 3)/(x(x + 1)) — 3/x - 2/(x + 1)
  - **Lời giải:**
    1. Viết A/(x - r) + B/(x - s), nhân hai vế với mẫu rồi thay x = r, x = s để tìm A, B.
    2. (2x + 1)/((x - 1)(x + 2)): x = 1 cho A = 3/3 = 1, x = -2 cho B = -3/(-3) = 1.
    3. (x + 3)/(x(x + 1)): x = 0 cho A = 3, x = -1 cho B = 2/(-1) = -2.
    4. 1/(x^2 - 4) = 1/((x - 2)(x + 2)): A = 1/4, B = -1/4.
- `gt_t7_ht_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến pi/2 của sin^2 x dx và tích phân từ 0 đến pi/2 của cos^2 x dx bằng nhau, và cùng bằng pi/4.
  - **Đáp án:** Đúng
    1. Hạ bậc: sin^2 x = (1 - cos(2x))/2, nên tích phân đầu = [x/2 - sin(2x)/4] từ 0 đến pi/2 = pi/4.
    2. Tương tự cos^2 x = (1 + cos(2x))/2 cho [x/2 + sin(2x)/4] từ 0 đến pi/2 = pi/4.
    3. Hai tích phân bằng nhau, tổng bằng tích phân của 1 trên [0, pi/2] là pi/2: mệnh đề đúng.
- `gt_t7_ht_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm nguyên hàm của 1/(x^2 + 2x + 5).
  - **Lời giải đưa ra (có một bước sai):**
    1. Mẫu không có nghiệm thực; viết x^2 + 2x + 5 = (x + 1)^2 + 4.
    2. Đặt t = x + 1, dt = dx: cần nguyên hàm của 1/(t^2 + 4).
    3. Dùng công thức nguyên hàm của 1/(t^2 + a^2) với a = 2.
    4. Được arctan((x + 1)/2) + C.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Được arctan((x + 1)/2) + C.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng: mẫu vô nghiệm thì đưa về tổng bình phương.
    2. Bước 4 quên hệ số 1/a: nguyên hàm của 1/(t^2 + a^2) là (1/a) arctan(t/a) + C.
    3. Đúng là (1/2) arctan((x + 1)/2) + C.
- `gt_t7_ht_07` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến pi/2 của sin^3 x . cos^2 x dx.
  - **Đáp án:** 2/15
    1. Lũy thừa của sin lẻ: tách sin^3 x = (1 - cos^2 x) sin x.
    2. Đặt u = cos x, du = -sin x dx; x từ 0 đến pi/2 ứng với u từ 1 đến 0.
    3. Tích phân = tích phân từ 0 đến 1 của (1 - u^2)u^2 du = 1/3 - 1/5 = 2/15.
- `gt_t7_ht_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x) = (x + 5)/(x^2 + x - 2) và I = tích phân từ 2 đến 3 của f(x) dx.
  - **Phần a** (Điền số): a) Viết f(x) = A/(x - 1) + B/(x + 2). Nhập A, B theo đúng thứ tự.
    - **Đáp án a:** 2, -1
  - **Phần b** (Điền số): b) I = a ln 2 + b ln 5 với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
    - **Đáp án b:** 4, -1
  - **Phần c** (Đúng/Sai): c) I > 0.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) x^2 + x - 2 = (x - 1)(x + 2). Nhân với mẫu: x + 5 = A(x + 2) + B(x - 1). x = 1 cho 6 = 3A, A = 2; x = -2 cho 3 = -3B, B = -1.
    2. b) I = [2 ln|x - 1| - ln|x + 2|] từ 2 đến 3 = (2 ln 2 - ln 5) - (0 - ln 4) = 4 ln 2 - ln 5.
    3. c) I = ln(16/5) > 0 vì 16/5 > 1 (cũng thấy ngay vì f > 0 trên [2, 3]): đúng.
- `gt_g7_tach_phan_thuc` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Viết (-2x + 5) / ((x + 2)(x - 1)) = A/(x + 2) + B/(x - 1). Nhập A, B theo đúng thứ tự.
  - **Đáp án:** -3, 1
    1. Nhân hai vế với mẫu: -2x + 5 = A(x - 1) + B(x + 2).
    2. Thay x = -2: 9 = A . (-3), nên A = -3.
    3. Thay x = 1: 3 = B . 3, nên B = 1.
  - **Câu hỏi:** Viết (-6x) / ((x + 3)(x - 3)) = A/(x + 3) + B/(x - 3). Nhập A, B theo đúng thứ tự.
  - **Đáp án:** -3, -3
    1. Nhân hai vế với mẫu: -6x = A(x - 3) + B(x + 3).
    2. Thay x = -3: 18 = A . (-6), nên A = -3.
    3. Thay x = 3: -18 = B . 6, nên B = -3.
  - **Câu hỏi:** Viết (6) / ((x + 2)(x - 1)) = A/(x + 2) + B/(x - 1). Nhập A, B theo đúng thứ tự.
  - **Đáp án:** -2, 2
    1. Nhân hai vế với mẫu: 6 = A(x - 1) + B(x + 2).
    2. Thay x = -2: 6 = A . (-3), nên A = -2.
    3. Thay x = 1: 6 = B . 3, nên B = 2.
- `gt_t7_ht_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến 1 của (x^2 + 3x + 4)/((x + 1)(x^2 + 1)) dx bằng a ln 2 + b . pi với a, b hữu tỉ. Nhập a, b theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_ht_02`, `gt_t7_ht_04`, `gt_t7_ht_01`
  - **Đáp án:** 1, 3/4
    1. Tách: (x^2 + 3x + 4)/((x + 1)(x^2 + 1)) = A/(x + 1) + (Bx + C)/(x^2 + 1).
    2. x = -1: A = (1 - 3 + 4)/2 = 1. Khi đó x^2 + 3x + 4 - (x^2 + 1) = 3x + 3 = (Bx + C)(x + 1), nên B = 0, C = 3.
    3. Tích phân = [ln(x + 1) + 3 arctan x] từ 0 đến 1 = ln 2 + 3pi/4.
    4. Vậy a = 1, b = 3/4.
- `gt_t7_ht_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng phép đặt t = tan(x/2), tính tích phân từ 0 đến pi/2 của 1/(1 + sin x) dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_ht_07`, `gt_t7_db_01`
  - **Đáp án:** 1
    1. Với t = tan(x/2): sin x = 2t/(1 + t^2), dx = 2 dt/(1 + t^2); x từ 0 đến pi/2 ứng với t từ 0 đến 1.
    2. 1 + sin x = (1 + t)^2/(1 + t^2), nên hàm dưới dấu tích phân thành 2/(1 + t)^2.
    3. Tích phân từ 0 đến 1 của 2/(1 + t)^2 dt = [-2/(1 + t)] từ 0 đến 1 = -1 + 2 = 1.

### Tích phân xác định và công thức Newton-Leibniz (`gt_t7_newton_leibniz`)

- `gt_t7_nl_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 3 của |x^2 - 2x| dx.
  - **Đáp án:** 8/3
    1. x^2 - 2x = x(x - 2) âm trên (0, 2) và dương trên (2, 3): phải tách tại x = 2.
    2. Tích phân từ 0 đến 2 của (2x - x^2) dx = 4 - 8/3 = 4/3.
    3. Tích phân từ 2 đến 3 của (x^2 - 2x) dx = [x^3/3 - x^2] từ 2 đến 3 = 0 - (8/3 - 4) = 4/3.
    4. Tổng: 8/3.
- `gt_t7_nl_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hàm f liên tục trên [0, 1]: tích phân từ 0 đến 1 của f(x) dx = tích phân từ 0 đến 1 của f(1 - x) dx.
  - **Đáp án:** Đúng
    1. Trong vế phải đặt t = 1 - x: dx = -dt, x = 0 ứng với t = 1, x = 1 ứng với t = 0.
    2. Vế phải = tích phân từ 1 đến 0 của f(t)(-dt) = tích phân từ 0 đến 1 của f(t) dt.
    3. Tên biến lấy tích phân không quan trọng, nên hai vế bằng nhau: mệnh đề đúng.
- `gt_t7_nl_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giá trị trung bình của f(x) = sin x trên đoạn [0, pi], tức (1/(b - a)) . tích phân từ a đến b của f(x) dx, bằng bao nhiêu?
    - **(đúng)** 2/pi
    - 1/2
    - 2
    - 1/pi
  - **Đáp án:** 2/pi
    1. Tích phân từ 0 đến pi của sin x dx = [-cos x] từ 0 đến pi = 1 + 1 = 2.
    2. Chia cho độ dài đoạn b - a = pi.
    3. Giá trị trung bình là 2/pi (xấp xỉ 0.64). Đáp án 2 là quên chia cho pi.
- `gt_t7_nl_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính tích phân từ -1 đến 1 của 1/x^2 dx.
  - **Lời giải đưa ra (có một bước sai):**
    1. Một nguyên hàm của 1/x^2 là -1/x.
    2. Theo công thức Newton-Leibniz, tích phân bằng (-1/1) - (-1/(-1)).   **<- bước sai đầu tiên**
    3. = -1 - 1 = -2.
    4. Vậy tích phân bằng -2.
  - **Đáp án:** Bước 2: Theo công thức Newton-Leibniz, tích phân bằng (-1/1) - (-1/(-1)).
  - **Vì sao sai, và bước đúng:**
    1. Bước 1 đúng trên mỗi khoảng không chứa 0.
    2. Bước 2 sai: Newton-Leibniz cần hàm liên tục trên cả đoạn [-1, 1], mà 1/x^2 không xác định và không bị chặn quanh 0.
    3. Một hàm dương không thể có tích phân âm; thực ra tích phân này phân kỳ (xem tích phân suy rộng ở tầng 8).
- `gt_g7_tri_tuyet_doi` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 3 của |x^2 - x| dx.
  - **Đáp án:** 29/6
    1. x^2 - x = x(x - 1) âm trên (0, 1) và dương trên (1, 3): tách tại x = 1.
    2. Tích phân từ 0 đến 1 của -(x^2 - x) dx = 1/6.
    3. Tích phân từ 1 đến 3 của (x^2 - x) dx = 14/3.
    4. Tổng: 29/6.
  - **Câu hỏi:** Tính tích phân từ 0 đến 2 của |x^2 - x| dx.
  - **Đáp án:** 1
    1. x^2 - x = x(x - 1) âm trên (0, 1) và dương trên (1, 2): tách tại x = 1.
    2. Tích phân từ 0 đến 1 của -(x^2 - x) dx = 1/6.
    3. Tích phân từ 1 đến 2 của (x^2 - x) dx = 5/6.
    4. Tổng: 1.
  - **Câu hỏi:** Tính tích phân từ 0 đến 4 của |x^2 - 2x| dx.
  - **Đáp án:** 8
    1. x^2 - 2x = x(x - 2) âm trên (0, 2) và dương trên (2, 4): tách tại x = 2.
    2. Tích phân từ 0 đến 2 của -(x^2 - 2x) dx = 4/3.
    3. Tích phân từ 2 đến 4 của (x^2 - 2x) dx = 20/3.
    4. Tổng: 8.
- `gt_t7_nl_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Giới hạn khi n -> +vô cùng của tổng S_n = n/(n^2 + 1^2) + n/(n^2 + 2^2) + ... + n/(n^2 + n^2) bằng k . pi. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_03`, `gt_t7_nl_01`
  - **Đáp án:** 1/4
    1. Viết số hạng thứ i: n/(n^2 + i^2) = (1/n) . 1/(1 + (i/n)^2).
    2. S_n là tổng Riemann của f(x) = 1/(1 + x^2) trên [0, 1] với các điểm chia i/n, mỗi đoạn dài 1/n.
    3. f liên tục nên S_n -> tích phân từ 0 đến 1 của 1/(1 + x^2) dx = arctan 1 = pi/4.
    4. k = 1/4.
- `gt_t7_nl_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh tích phân I từ 0 đến pi/2 của sin x/(sin x + cos x) dx bằng pi/4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_db_03`
  - **Đáp án (thứ tự đúng):**
    1. Gọi J = tích phân từ 0 đến pi/2 của cos x/(sin x + cos x) dx.
    2. Trong I đặt x = pi/2 - t: sin x = cos t, cos x = sin t, dx = -dt, và hai cận đổi chỗ cho nhau.
    3. Đảo lại hai cận để bỏ dấu trừ, được I = J.
    4. Cộng hai tích phân: I + J = tích phân từ 0 đến pi/2 của 1 dx = pi/2.
    5. Từ I = J và I + J = pi/2 suy ra I = pi/4.
  - **Lời giải:**
    1. Không cần tìm nguyên hàm: phép đổi biến x = pi/2 - t đổi sin và cos cho nhau.
    2. Cách này dựa trên đẳng thức tích phân của f(x) bằng tích phân của f(a + b - x) trên [a, b].
    3. Tổng I + J dễ tính vì tử và mẫu bằng nhau.
- `gt_t7_nl_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x) = x^2 nếu 0 <= x <= 1; f(x) = 2 - x nếu 1 < x <= 2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_t7_nl_03`
  - **Phần a** (Điền số): a) Tính tích phân từ 0 đến 2 của f(x) dx.
    - **Đáp án a:** 5/6
  - **Phần b** (Điền số): b) Tính giá trị trung bình của f trên [0, 2].
    - **Đáp án b:** 5/12
  - **Phần c** (Đúng/Sai): c) Có điểm c thuộc [0, 2] mà f(c) bằng đúng giá trị trung bình ở câu b.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Tách tại 1: tích phân từ 0 đến 1 của x^2 dx = 1/3, tích phân từ 1 đến 2 của (2 - x) dx = 1/2. Tổng 5/6.
    2. b) Chia cho độ dài đoạn: (5/6)/2 = 5/12.
    3. c) Hai mảnh nối liền tại x = 1 (cùng giá trị 1), nên f liên tục trên [0, 2] và theo định lý giá trị trung bình của tích phân có c như vậy; chẳng hạn c = sqrt(5/12) thuộc [0, 1]. Đúng.

### Tích phân với cận biến thiên (`gt_t7_can_bien_thien`)

- `gt_t7_cb_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho F(x) = tích phân từ x đến x^3 của 1/(1 + t^2) dt. Tính F'(1).
  - **Đáp án:** 1
    1. Với G là một nguyên hàm của 1/(1 + t^2): F(x) = G(x^3) - G(x).
    2. Dây chuyền: F'(x) = 3x^2 . 1/(1 + x^6) - 1/(1 + x^2).
    3. F'(1) = 3/2 - 1/2 = 1.
- `gt_t7_cb_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính giới hạn khi x -> 0 của (tích phân từ 0 đến x của sin(t^2) dt) / x^3.
  - **Đáp án:** 1/3
    1. Tử và mẫu cùng dần tới 0: dạng 0/0, dùng L'Hospital.
    2. Đạo hàm của tử là sin(x^2) (định lý cơ bản), của mẫu là 3x^2.
    3. sin(x^2)/(3x^2) -> 1/3 vì sin u/u -> 1.
- `gt_t7_cb_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho G(x) = tích phân từ 0 đến x của (t - 1)(t - 3) dt. G đạt cực đại địa phương tại điểm nào?
    - **(đúng)** x = 1
    - x = 3
    - x = 0
    - x = 2
  - **Đáp án:** x = 1
    1. G'(x) = (x - 1)(x - 3), bằng 0 tại x = 1 và x = 3.
    2. G' dương khi x < 1, âm khi 1 < x < 3, dương khi x > 3.
    3. G' đổi dấu từ + sang - tại x = 1: cực đại; tại x = 3 là cực tiểu.
- `gt_t7_cb_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính đạo hàm của F(x) = tích phân từ 0 đến x^2 của cos t dt.
  - **Lời giải đưa ra (có một bước sai):**
    1. Viết F(x) = G(x^2) với G(u) = tích phân từ 0 đến u của cos t dt.
    2. Theo định lý cơ bản của giải tích, G'(u) = cos u.
    3. Theo quy tắc dây chuyền, F'(x) = G'(x^2).   **<- bước sai đầu tiên**
    4. Vậy F'(x) = cos(x^2).
  - **Đáp án:** Bước 3: Theo quy tắc dây chuyền, F'(x) = G'(x^2).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 thiếu đạo hàm của hàm trong: F'(x) = G'(x^2) . (x^2)' = G'(x^2) . 2x.
    2. Đúng là F'(x) = 2x cos(x^2).
    3. Kiểm tra: F(x) = sin(x^2), và (sin(x^2))' = 2x cos(x^2).
- `gt_t7_cb_06` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm F(x) = tích phân từ 0 đến x của e^(-t^2) dt lồi (F'' > 0) trên khoảng (0, +vô cùng).
  - **Đáp án:** Sai
    1. Định lý cơ bản: F'(x) = e^(-x^2).
    2. F''(x) = -2x e^(-x^2), âm với mọi x > 0.
    3. Vậy F lõm (F'' < 0) trên (0, +vô cùng): mệnh đề sai.
- `gt_g7_can_bien` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho F(x) = tích phân từ x đến x^2 của (t^2 - 2t + 1) dt. Tính F'(-2).
  - **Đáp án:** -45
    1. Với g(t) là hàm dưới dấu tích phân và G là một nguyên hàm của g: F(x) = G(x^2) - G(x).
    2. Dây chuyền: F'(x) = g(x^2) . 2x - g(x).
    3. g(4) = 9 và g(-2) = 9.
    4. F'(-2) = 9 . (-4) - 9 = -45.
  - **Câu hỏi:** Cho F(x) = tích phân từ x đến x^2 của (t^2 + 3t + 3) dt. Tính F'(-2).
  - **Đáp án:** -125
    1. Với g(t) là hàm dưới dấu tích phân và G là một nguyên hàm của g: F(x) = G(x^2) - G(x).
    2. Dây chuyền: F'(x) = g(x^2) . 2x - g(x).
    3. g(4) = 31 và g(-2) = 1.
    4. F'(-2) = 31 . (-4) - 1 = -125.
  - **Câu hỏi:** Cho F(x) = tích phân từ x đến x^2 của (t^2 - 2t + 1) dt. Tính F'(-1).
  - **Đáp án:** -4
    1. Với g(t) là hàm dưới dấu tích phân và G là một nguyên hàm của g: F(x) = G(x^2) - G(x).
    2. Dây chuyền: F'(x) = g(x^2) . 2x - g(x).
    3. g(1) = 0 và g(-1) = 4.
    4. F'(-1) = 0 . (-2) - 4 = -4.
- `gt_t7_cb_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f liên tục trên R thỏa f(x) = 1 + 2 . (tích phân từ 0 đến x của t f(t) dt) với mọi x. Tính ln f(2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_cb_01`, `gt_t7_cb_04`
  - **Đáp án:** 4
    1. Vế phải khả vi nên f khả vi; đạo hàm hai vế: f'(x) = 2x f(x). Thay x = 0 vào đẳng thức: f(0) = 1.
    2. f(x) = e^(x^2) thỏa cả hai điều kiện, và là hàm duy nhất: với g(x) = f(x) e^(-x^2) thì g' = (f' - 2x f) e^(-x^2) = 0, nên g là hằng số g(0) = 1.
    3. f(2) = e^4, nên ln f(2) = 4.
- `gt_t7_cb_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: tìm hàm liên tục f và hằng số a sao cho tích phân từ a đến x của f(t) dt = x^2 - 2x - 3 với mọi x.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_cb_04`, `gt_t7_cb_01`
  - **Phần a** (Điền số): a) Tính f(4).
    - **Đáp án a:** 6
  - **Phần b** (Điền số): b) Nhập mọi giá trị có thể của a.
    - **Đáp án b:** -1, 3  (thứ tự nào cũng được)
  - **Phần c** (Đúng/Sai): c) Với mỗi giá trị a ở câu b, đẳng thức đúng với mọi x.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Đạo hàm hai vế theo x: f(x) = 2x - 2, nên f(4) = 6.
    2. b) Thay x = a: vế trái là tích phân trên đoạn rỗng, bằng 0. Vậy a^2 - 2a - 3 = 0, tức (a + 1)(a - 3) = 0: a = -1 hoặc a = 3.
    3. c) Với f(t) = 2t - 2: tích phân từ a đến x = (x^2 - 2x) - (a^2 - 2a) = x^2 - 2x - 3 vì a^2 - 2a = 3 với cả hai giá trị: đúng.

## Tầng 8: Ứng dụng của tích phân và tích phân suy rộng

43 dạng câu (37 câu viết tay, 6 bộ sinh câu); 43 chưa duyệt.

### Diện tích hình phẳng (`gt_t8_dien_tich`)

- `gt_t8_dt_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính diện tích miền phẳng giới hạn bởi parabol y = x^2 và đường thẳng y = 2x + 3.
  - **Đáp án:** 32/3
    1. Giao điểm: x^2 = 2x + 3, tức (x + 1)(x - 3) = 0: x = -1 và x = 3.
    2. Trên (-1, 3) đường thẳng nằm trên parabol (thử x = 0: 3 > 0).
    3. S = tích phân từ -1 đến 3 của (2x + 3 - x^2) dx = [x^2 + 3x - x^3/3] từ -1 đến 3 = 9 - (-5/3) = 32/3.
- `gt_t8_dt_02` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính diện tích miền giới hạn bởi y = x^3 và y = x.
  - **Lời giải đưa ra (có một bước sai):**
    1. Giao điểm: x^3 = x khi x = -1, x = 0, x = 1.
    2. Diện tích S = tích phân từ -1 đến 1 của (x - x^3) dx.   **<- bước sai đầu tiên**
    3. Hàm x - x^3 lẻ nên tích phân trên đoạn đối xứng bằng 0.
    4. Vậy S = 0: hai đường không bao miền nào.
  - **Đáp án:** Bước 2: Diện tích S = tích phân từ -1 đến 1 của (x - x^3) dx.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai: diện tích là tích phân của |x - x^3|, và x - x^3 đổi dấu tại 0 (dương trên (0, 1), âm trên (-1, 0)).
    2. Đúng là S = 2 . tích phân từ 0 đến 1 của (x - x^3) dx = 2(1/2 - 1/4) = 1/2.
    3. Tích phân có dấu có thể bằng 0 dù diện tích dương: hai phần bù trừ nhau.
- `gt_t8_dt_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Diện tích miền giới hạn bởi y = ln x, trục Ox và đường thẳng x = e bằng bao nhiêu?
    - **(đúng)** 1
    - e - 1
    - e
    - 1/2
  - **Đáp án:** 1
    1. ln x = 0 tại x = 1 và ln x >= 0 trên [1, e]: miền nằm trên [1, e].
    2. S = tích phân từ 1 đến e của ln x dx; từng phần với u = ln x, dv = dx: [x ln x - x] từ 1 đến e.
    3. = (e - e) - (0 - 1) = 1.
- `gt_g8_dien_tich` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính diện tích miền giới hạn bởi parabol y = -2x^2 + 6x - 4 và trục Ox.
  - **Đáp án:** 1/3
    1. Parabol cắt Ox tại x = 1 và x = 2; giữa hai điểm đó nó nằm trên trục Ox.
    2. S = |tích phân từ 1 đến 2 của (-2)(x - 1)(x - 2) dx|.
    3. Với mọi parabol a(x - r)(x - s): tích phân từ r đến s bằng -a(s - r)^3/6, nên S = |a|(s - r)^3/6.
    4. S = 2 . 1^3 / 6 = 1/3.
  - **Câu hỏi:** Tính diện tích miền giới hạn bởi parabol y = -3x^2 - 15x - 18 và trục Ox.
  - **Đáp án:** 1/2
    1. Parabol cắt Ox tại x = -3 và x = -2; giữa hai điểm đó nó nằm trên trục Ox.
    2. S = |tích phân từ -3 đến -2 của (-3)(x + 3)(x + 2) dx|.
    3. Với mọi parabol a(x - r)(x - s): tích phân từ r đến s bằng -a(s - r)^3/6, nên S = |a|(s - r)^3/6.
    4. S = 3 . 1^3 / 6 = 1/2.
  - **Câu hỏi:** Tính diện tích miền giới hạn bởi parabol y = -2x^2 + 8x - 6 và trục Ox.
  - **Đáp án:** 8/3
    1. Parabol cắt Ox tại x = 1 và x = 3; giữa hai điểm đó nó nằm trên trục Ox.
    2. S = |tích phân từ 1 đến 3 của (-2)(x - 1)(x - 3) dx|.
    3. Với mọi parabol a(x - r)(x - s): tích phân từ r đến s bằng -a(s - r)^3/6, nên S = |a|(s - r)^3/6.
    4. S = 2 . 2^3 / 6 = 8/3.
- `gt_t8_dt_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính diện tích miền giới hạn bởi parabol y^2 = 2x và đường thẳng y = x - 4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_dt_01`, `gt_t8_dt_02`
  - **Đáp án:** 18
    1. Viết theo y: x = y^2/2 (parabol) và x = y + 4 (đường thẳng). Giao điểm: y^2/2 = y + 4, tức y^2 - 2y - 8 = 0: y = -2 và y = 4.
    2. Với y giữa -2 và 4, đường thẳng nằm bên phải parabol (y = 0: 4 > 0).
    3. S = tích phân từ -2 đến 4 của (y + 4 - y^2/2) dy = [y^2/2 + 4y - y^3/6] từ -2 đến 4 = 40/3 - (-14/3) = 18.
    4. Lấy tích phân theo x sẽ phải tách miền tại x = 2; lấy theo y chỉ cần một tích phân.
- `gt_t8_dt_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với k < 2, đường thẳng y = kx và parabol y = 2x - x^2 bao một miền có diện tích 9/2. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_dt_01`, `gt_t8_dt_03`
  - **Đáp án:** -1
    1. Giao điểm: kx = 2x - x^2, tức x(x - (2 - k)) = 0: x = 0 và x = 2 - k > 0.
    2. Giữa hai giao điểm parabol nằm trên: S = tích phân từ 0 đến 2 - k của ((2 - k)x - x^2) dx = (2 - k)^3/2 - (2 - k)^3/3 = (2 - k)^3/6.
    3. (2 - k)^3/6 = 9/2 cho (2 - k)^3 = 27, nên 2 - k = 3 và k = -1.
- `gt_t8_dt_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: xét miền giới hạn bởi hai đường y = x^3 - 3x và y = x.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_dt_02`, `gt_t8_dt_01`
  - **Phần a** (Điền số): a) Nhập hoành độ các giao điểm của hai đường.
    - **Đáp án a:** -2, 0, 2  (thứ tự nào cũng được)
  - **Phần b** (Trắc nghiệm): b) Trên khoảng (0, 2), đường nào nằm trên?
    - **(đúng)** y = x
    - y = x^3 - 3x
    - Hai đường cắt nhau trong khoảng này
    - **Đáp án b:** y = x
  - **Phần c** (Điền số): c) Tính tổng diện tích miền bị bao.
    - **Đáp án c:** 8
  - **Lời giải:**
    1. a) x^3 - 3x = x khi x^3 - 4x = x(x - 2)(x + 2) = 0: x = -2, 0, 2.
    2. b) Tại x = 1: đường thẳng cho 1, đường bậc ba cho -2, và trên (0, 2) không có giao điểm nào nữa: y = x nằm trên.
    3. c) Hiệu x - (x^3 - 3x) = 4x - x^3 là hàm lẻ, nên hai mảnh có diện tích bằng nhau: S = 2 . tích phân từ 0 đến 2 của (4x - x^3) dx = 2(8 - 4) = 8.

### Thể tích vật thể tròn xoay (`gt_t8_the_tich`)

- `gt_t8_tt_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quay miền giới hạn bởi y = sqrt(x), trục Ox và đường thẳng x = 4 quanh trục Ox. Thể tích vật tròn xoay bằng k . pi. Tìm k.
  - **Đáp án:** 8
    1. Mặt cắt tại x là hình tròn bán kính y = sqrt(x), diện tích pi . x.
    2. V = pi . tích phân từ 0 đến 4 của x dx = pi . 16/2 = 8pi.
    3. k = 8.
- `gt_t8_tt_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quay miền giới hạn bởi y = x và y = x^2 quanh trục Ox. Thể tích bằng k . pi. Tìm k.
  - **Đáp án:** 2/15
    1. Hai đường cắt nhau tại x = 0 và x = 1; trên (0, 1) có x > x^2.
    2. Mặt cắt là hình vành khăn: bán kính ngoài x, bán kính trong x^2, diện tích pi(x^2 - x^4).
    3. V = pi . tích phân từ 0 đến 1 của (x^2 - x^4) dx = pi(1/3 - 1/5) = 2pi/15, nên k = 2/15.
- `gt_t8_tt_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: quay miền giữa y = 2x và y = x^2 (0 <= x <= 2) quanh trục Ox, tính thể tích.
  - **Lời giải đưa ra (có một bước sai):**
    1. Trên (0, 2) có 2x > x^2: đường y = 2x nằm ngoài, y = x^2 nằm trong.
    2. Mặt cắt tại x là hình vành khăn, bán kính ngoài 2x, bán kính trong x^2.
    3. Diện tích mặt cắt bằng pi(2x - x^2)^2.   **<- bước sai đầu tiên**
    4. V = pi . tích phân từ 0 đến 2 của (2x - x^2)^2 dx = 16pi/15.
  - **Đáp án:** Bước 3: Diện tích mặt cắt bằng pi(2x - x^2)^2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: diện tích vành khăn là pi(R^2 - r^2), không phải pi(R - r)^2.
    2. Đúng là pi((2x)^2 - (x^2)^2) = pi(4x^2 - x^4).
    3. V = pi(32/3 - 32/5) = 64pi/15.
- `gt_t8_tt_04` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quay miền vô hạn giới hạn bởi y = 1/x, trục Ox và nửa đường x >= 1 quanh trục Ox được một vật có thể tích hữu hạn, bằng pi.
  - **Đáp án:** Đúng
    1. V = pi . tích phân từ 1 đến +vô cùng của 1/x^2 dx, một tích phân suy rộng.
    2. Tích phân từ 1 đến R của 1/x^2 dx = 1 - 1/R -> 1 khi R -> +vô cùng.
    3. Vậy V = pi, hữu hạn (dù diện tích của miền, tích phân của 1/x, là vô hạn): mệnh đề đúng.
- `gt_t8_tt_tk_01` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: miền D giới hạn bởi y = x^2 và y = 2x.
  - **Phần a** (Điền số): a) Tính diện tích của D.
    - **Đáp án a:** 4/3
  - **Phần b** (Điền số): b) Quay D quanh trục Ox được thể tích k . pi. Tìm k.
    - **Đáp án b:** 64/15
  - **Phần c** (Đúng/Sai): c) Thể tích ở câu b bằng pi . tích phân từ 0 đến 2 của (2x - x^2)^2 dx.
    - **Đáp án c:** Sai
  - **Lời giải:**
    1. a) Giao điểm x = 0, x = 2; S = tích phân từ 0 đến 2 của (2x - x^2) dx = 4 - 8/3 = 4/3.
    2. b) Vành khăn: V = pi . tích phân từ 0 đến 2 của (4x^2 - x^4) dx = pi(32/3 - 32/5) = 64pi/15.
    3. c) Công thức đó lấy bình phương của hiệu thay vì hiệu các bình phương; nó cho 16pi/15, khác 64pi/15: sai.
- `gt_g8_the_tich` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Quay miền giới hạn bởi y = x^2, trục Ox và đường thẳng x = 1 quanh trục Ox. Thể tích bằng k . pi. Tìm k.
  - **Đáp án:** 1/5
    1. Mặt cắt tại x là hình tròn bán kính y, diện tích pi . y^2 = pi . x^4.
    2. V = pi . tích phân từ 0 đến 1 của x^4 dx = pi . 1 . 1^5 / 5.
    3. k = 1/5.
  - **Câu hỏi:** Quay miền giới hạn bởi y = sqrt(x), trục Ox và đường thẳng x = 1 quanh trục Ox. Thể tích bằng k . pi. Tìm k.
  - **Đáp án:** 1/2
    1. Mặt cắt tại x là hình tròn bán kính y, diện tích pi . y^2 = pi . x.
    2. V = pi . tích phân từ 0 đến 1 của x dx = pi . 1 . 1^2 / 2.
    3. k = 1/2.
  - **Câu hỏi:** Quay miền giới hạn bởi y = x^2, trục Ox và đường thẳng x = 1 quanh trục Ox. Thể tích bằng k . pi. Tìm k.
  - **Đáp án:** 1/5
    1. Mặt cắt tại x là hình tròn bán kính y, diện tích pi . y^2 = pi . x^4.
    2. V = pi . tích phân từ 0 đến 1 của x^4 dx = pi . 1 . 1^5 / 5.
    3. k = 1/5.
- `gt_t8_tt_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quay miền giới hạn bởi y = sin x, trục Ox với 0 <= x <= pi quanh trục Oy. Thể tích bằng k . pi^2. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_tp_03`, `gt_t8_tt_01`
  - **Đáp án:** 2
    1. Quay quanh Oy, dùng phương pháp vỏ trụ: dải đứng tại x cao sin x, quay thành vỏ trụ bán kính x, thể tích 2pi . x . sin x . dx.
    2. V = 2pi . tích phân từ 0 đến pi của x sin x dx.
    3. Từng phần: tích phân của x sin x = -x cos x + sin x; từ 0 đến pi được pi.
    4. V = 2pi . pi = 2pi^2, nên k = 2.
- `gt_t8_tt_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh hình nón bán kính đáy r, chiều cao h có thể tích pi r^2 h / 3.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_tt_01`, `gt_t8_tt_02`
  - **Đáp án (thứ tự đúng):**
    1. Đặt đỉnh nón tại gốc tọa độ, trục nón trên Ox: nón là vật tròn xoay khi quay đoạn y = (r/h)x, 0 <= x <= h quanh Ox.
    2. Mặt cắt tại x là hình tròn bán kính (r/h)x, diện tích pi r^2 x^2 / h^2.
    3. V = tích phân từ 0 đến h của pi r^2 x^2 / h^2 dx.
    4. = (pi r^2 / h^2) . h^3 / 3 = pi r^2 h / 3.
  - **Lời giải:**
    1. Chọn hệ tọa độ sao cho mặt cắt đơn giản nhất.
    2. Bán kính mặt cắt tỉ lệ với khoảng cách tới đỉnh, nên là đường thẳng y = (r/h)x.
    3. Thể tích = tích phân diện tích mặt cắt.

### Độ dài đường cong (`gt_t8_do_dai_cung`)

- `gt_t8_dd_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính độ dài cung y = (2/3) x^(3/2) với 0 <= x <= 3.
  - **Đáp án:** 14/3
    1. y' = x^(1/2), nên 1 + (y')^2 = 1 + x.
    2. L = tích phân từ 0 đến 3 của sqrt(1 + x) dx = [(2/3)(1 + x)^(3/2)] từ 0 đến 3.
    3. = (2/3)(8 - 1) = 14/3.
- `gt_t8_dd_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính độ dài đường cong tham số x = t^2, y = (2/3) t^3 với 0 <= t <= sqrt(8).
  - **Đáp án:** 52/3
    1. x'(t) = 2t, y'(t) = 2t^2: x'^2 + y'^2 = 4t^2(1 + t^2), căn bậc hai là 2t sqrt(1 + t^2) (t >= 0).
    2. L = tích phân từ 0 đến sqrt(8) của 2t sqrt(1 + t^2) dt; đặt u = 1 + t^2 được [(2/3)(1 + t^2)^(3/2)] từ 0 đến sqrt(8).
    3. = (2/3)(27 - 1) = 52/3.
- `gt_t8_dd_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Độ dài cung của đường cong nào trên đoạn 0 <= x <= 1 bằng tích phân từ 0 đến 1 của sqrt(1 + 4x^2) dx?
    - **(đúng)** y = x^2
    - y = 2x
    - y = x^2 / 2
    - y = 4x^3
  - **Đáp án:** y = x^2
    1. Độ dài cung là tích phân của sqrt(1 + (y')^2), nên cần (y')^2 = 4x^2.
    2. y = x^2 có y' = 2x: đúng. y = 2x cho sqrt(5), y = x^2/2 cho sqrt(1 + x^2), y = 4x^3 cho sqrt(1 + 144x^4).
    3. Chú ý: công thức dùng đạo hàm y', không dùng chính y.
- `gt_t8_dd_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tính độ dài cung y = x^2/2 - (ln x)/4 với 1 <= x <= e.
  - **Lời giải đưa ra (có một bước sai):**
    1. y' = x - 1/(4x).
    2. 1 + (y')^2 = 1 + x^2 - 1/2 + 1/(16x^2) = (x + 1/(4x))^2.
    3. L = tích phân từ 1 đến e của (x + 1/(4x)) dx.
    4. = [x^2/2 + 4 ln x] từ 1 đến e.   **<- bước sai đầu tiên**
    5. = e^2/2 + 4 - 1/2 = e^2/2 + 7/2.
  - **Đáp án:** Bước 4: = [x^2/2 + 4 ln x] từ 1 đến e.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng: bình phương của hiệu cộng thêm 1 thành bình phương của tổng.
    2. Bước 4 sai: nguyên hàm của 1/(4x) là (1/4) ln x, không phải 4 ln x.
    3. Đúng là L = [x^2/2 + (ln x)/4] từ 1 đến e = e^2/2 + 1/4 - 1/2 = e^2/2 - 1/4.
- `gt_g8_do_dai` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính độ dài cung y = (2/3) x^(3/2) với 3 <= x <= 24.
  - **Đáp án:** 78
    1. y' = x^(1/2), nên 1 + (y')^2 = 1 + x.
    2. L = tích phân từ 3 đến 24 của sqrt(1 + x) dx = [(2/3)(1 + x)^(3/2)] từ 3 đến 24.
    3. 1 + 24 = 5^2 và 1 + 3 = 2^2, nên L = (2/3)(125 - 8) = 78.
  - **Câu hỏi:** Tính độ dài cung y = (2/3) x^(3/2) với 0 <= x <= 35.
  - **Đáp án:** 430/3
    1. y' = x^(1/2), nên 1 + (y')^2 = 1 + x.
    2. L = tích phân từ 0 đến 35 của sqrt(1 + x) dx = [(2/3)(1 + x)^(3/2)] từ 0 đến 35.
    3. 1 + 35 = 6^2 và 1 + 0 = 1^2, nên L = (2/3)(216 - 1) = 430/3.
  - **Câu hỏi:** Tính độ dài cung y = (2/3) x^(3/2) với 3 <= x <= 24.
  - **Đáp án:** 78
    1. y' = x^(1/2), nên 1 + (y')^2 = 1 + x.
    2. L = tích phân từ 3 đến 24 của sqrt(1 + x) dx = [(2/3)(1 + x)^(3/2)] từ 3 đến 24.
    3. 1 + 24 = 5^2 và 1 + 3 = 2^2, nên L = (2/3)(125 - 8) = 78.
- `gt_t8_dd_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính độ dài toàn bộ đường astroid x = cos^3 t, y = sin^3 t, 0 <= t <= 2pi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_dd_02`, `gt_t8_dd_03`
  - **Đáp án:** 6
    1. x' = -3cos^2 t sin t, y' = 3sin^2 t cos t: x'^2 + y'^2 = 9 sin^2 t cos^2 t (cos^2 t + sin^2 t) = 9 sin^2 t cos^2 t.
    2. Căn bậc hai là 3|sin t cos t|: phải giữ trị tuyệt đối, vì sin t cos t đổi dấu.
    3. Đường cong đối xứng qua hai trục: L = 4 . tích phân từ 0 đến pi/2 của 3 sin t cos t dt = 4 . 3 . (1/2) = 6.
    4. Bỏ trị tuyệt đối và lấy tích phân thẳng trên [0, 2pi] sẽ ra 0, vô lý.
- `gt_t8_dd_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính độ dài một nhịp của đường cycloid x = t - sin t, y = 1 - cos t, 0 <= t <= 2pi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_dd_02`, `gt_t8_dd_01`
  - **Đáp án:** 8
    1. x' = 1 - cos t, y' = sin t: x'^2 + y'^2 = 1 - 2cos t + cos^2 t + sin^2 t = 2 - 2cos t.
    2. Hạ bậc: 2 - 2cos t = 4 sin^2(t/2), và sin(t/2) >= 0 trên [0, 2pi], nên căn bậc hai là 2 sin(t/2).
    3. L = tích phân từ 0 đến 2pi của 2 sin(t/2) dt = [-4 cos(t/2)] từ 0 đến 2pi = 4 + 4 = 8.

### Tích phân suy rộng cận vô hạn (`gt_t8_suy_rong_loai_1`)

- `gt_t8_l1_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 1 đến +vô cùng của ln x / x^2 dx.
  - **Đáp án:** 1
    1. Từng phần với u = ln x, dv = dx/x^2: v = -1/x, nên nguyên hàm là -ln x / x - 1/x.
    2. Tích phân từ 1 đến R = (-ln R / R - 1/R) - (0 - 1) = 1 - (ln R + 1)/R.
    3. ln R / R -> 0 khi R -> +vô cùng (L'Hospital), nên tích phân hội tụ và bằng 1.
- `gt_t8_l1_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ -vô cùng đến +vô cùng của 1/(1 + x^2) dx bằng bao nhiêu?
    - **(đúng)** pi
    - pi/2
    - 2pi
    - Phân kỳ
  - **Đáp án:** pi
    1. Tách tại 0 thành hai tích phân suy rộng, mỗi cái có một cận vô hạn.
    2. Tích phân từ 0 đến R của 1/(1 + x^2) = arctan R -> pi/2; tương tự nửa bên trái cũng -> pi/2.
    3. Cả hai hội tụ, tổng là pi.
- `gt_t8_l1_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét tích phân từ -vô cùng đến +vô cùng của x dx.
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm f(x) = x là hàm lẻ.
    2. Theo định nghĩa, tích phân này bằng giới hạn khi R -> +vô cùng của tích phân từ -R đến R của x dx.   **<- bước sai đầu tiên**
    3. Với mọi R, tích phân từ -R đến R của x dx = 0.
    4. Vậy tích phân hội tụ và bằng 0.
  - **Đáp án:** Bước 2: Theo định nghĩa, tích phân này bằng giới hạn khi R -> +vô cùng của tích phân từ -R đến R của x dx.
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 sai định nghĩa: tích phân trên (-vô cùng, +vô cùng) hội tụ khi tích phân từ 0 đến +vô cùng và tích phân từ -vô cùng đến 0 cùng hội tụ, với hai giới hạn độc lập.
    2. Tích phân từ 0 đến R của x dx = R^2/2 -> +vô cùng, nên tích phân đã cho phân kỳ.
    3. Cắt đối xứng [-R, R] chỉ cho 'giá trị chính', không phải tích phân suy rộng.
- `gt_t8_l1_04` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến +vô cùng của sin x dx hội tụ.
  - **Đáp án:** Sai
    1. Tích phân từ 0 đến R của sin x dx = 1 - cos R.
    2. Khi R -> +vô cùng, cos R dao động giữa -1 và 1, nên 1 - cos R không có giới hạn.
    3. Tích phân phân kỳ (dù không ra vô cùng): mệnh đề sai.
- `gt_g8_suy_rong` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 1 đến +vô cùng của 5/x^3 dx.
  - **Đáp án:** 5/2
    1. Tích phân từ 1 đến R của 5x^(-3) dx = [5 . x^(-2) / (-2)] từ 1 đến R.
    2. = 5/2 . (1/1^2 - 1/R^2).
    3. Khi R -> +vô cùng, 1/R^2 -> 0: tích phân hội tụ và bằng 5/2.
  - **Câu hỏi:** Tính tích phân từ 1 đến +vô cùng của 1/x^3 dx.
  - **Đáp án:** 1/2
    1. Tích phân từ 1 đến R của 1x^(-3) dx = [1 . x^(-2) / (-2)] từ 1 đến R.
    2. = 1/2 . (1/1^2 - 1/R^2).
    3. Khi R -> +vô cùng, 1/R^2 -> 0: tích phân hội tụ và bằng 1/2.
  - **Câu hỏi:** Tính tích phân từ 3 đến +vô cùng của 5/x^2 dx.
  - **Đáp án:** 5/3
    1. Tích phân từ 3 đến R của 5x^(-2) dx = [5 . x^(-1) / (-1)] từ 3 đến R.
    2. = 5 . (1/3 - 1/R).
    3. Khi R -> +vô cùng, 1/R -> 0: tích phân hội tụ và bằng 5/3.
- `gt_t8_l1_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến +vô cùng của e^(-x) sin x dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_tp_03`, `gt_t8_l1_01`
  - **Đáp án:** 1/2
    1. Từng phần hai lần (như với e^x sin x): một nguyên hàm là -e^(-x)(sin x + cos x)/2. Kiểm tra bằng đạo hàm.
    2. Tích phân từ 0 đến R = -e^(-R)(sin R + cos R)/2 + 1/2.
    3. |sin R + cos R| <= 2 và e^(-R) -> 0, nên số hạng đầu -> 0: tích phân bằng 1/2.
- `gt_t8_l1_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 2 đến +vô cùng của 1/(x^2 - 1) dx bằng k . ln 3. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_ht_01`, `gt_t8_l1_01`
  - **Đáp án:** 1/2
    1. Tách: 1/(x^2 - 1) = (1/2)(1/(x - 1) - 1/(x + 1)); nguyên hàm (1/2) ln((x - 1)/(x + 1)) với x > 1.
    2. Tích phân từ 2 đến R = (1/2) ln((R - 1)/(R + 1)) - (1/2) ln(1/3).
    3. (R - 1)/(R + 1) -> 1 nên số hạng đầu -> 0: tích phân = (1/2) ln 3, k = 1/2.
    4. Chú ý: tách riêng thành hai tích phân của 1/(x - 1) và 1/(x + 1) thì cả hai đều phân kỳ; phải gộp lại rồi mới cho R -> +vô cùng.

### Tích phân suy rộng của hàm không bị chặn (`gt_t8_suy_rong_loai_2`)

- `gt_t8_l2_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 1 của ln x dx (hàm không bị chặn gần 0).
  - **Đáp án:** -1
    1. Xét tích phân từ a đến 1 với 0 < a < 1: nguyên hàm x ln x - x cho (0 - 1) - (a ln a - a).
    2. Khi a -> 0+: a ln a -> 0 (dạng 0 . vô cùng, L'Hospital) và a -> 0.
    3. Tích phân hội tụ và bằng -1.
- `gt_t8_l2_02` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 9 của 1/(x - 1)^(2/3) dx, trong đó (x - 1)^(2/3) là bình phương của căn bậc ba của x - 1.
  - **Đáp án:** 9
    1. Hàm không bị chặn tại x = 1, nằm bên trong đoạn: tách thành tích phân từ 0 đến 1 và từ 1 đến 9.
    2. Nguyên hàm: 3(x - 1)^(1/3) (căn bậc ba có nghĩa cả khi x - 1 âm), liên tục tại x = 1.
    3. Phần trái: 3(0 - (-1)) = 3. Phần phải: 3(2 - 0) = 6. Cả hai hội tụ, tổng 9.
- `gt_t8_l2_04` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân suy rộng từ 0 đến 1 của 1/sqrt(1 - x^2) dx hội tụ và bằng pi/2.
  - **Đáp án:** Đúng
    1. Hàm không bị chặn khi x -> 1-; xét tích phân từ 0 đến b với b < 1: arcsin b - arcsin 0 = arcsin b.
    2. arcsin liên tục tại 1, nên arcsin b -> arcsin 1 = pi/2 khi b -> 1-.
    3. Tích phân hội tụ và bằng pi/2: mệnh đề đúng.
- `gt_g8_loai_2` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích phân từ 0 đến 9 của 1/sqrt(x) dx (hàm không bị chặn gần 0).
  - **Đáp án:** 6
    1. Xét tích phân từ a đến 9 với a -> 0+. Nguyên hàm của x^(-1/2) là x^(1/2) / (1/2).
    2. a^(1/2) -> 0 vì số mũ dương, nên tích phân hội tụ.
    3. Giá trị: 1 . 9^(1/2) / (1/2) = 1 . 3 / (1/2) = 6.
  - **Câu hỏi:** Tính tích phân từ 0 đến 1 của 1/sqrt(x) dx (hàm không bị chặn gần 0).
  - **Đáp án:** 2
    1. Xét tích phân từ a đến 1 với a -> 0+. Nguyên hàm của x^(-1/2) là x^(1/2) / (1/2).
    2. a^(1/2) -> 0 vì số mũ dương, nên tích phân hội tụ.
    3. Giá trị: 1 . 1^(1/2) / (1/2) = 1 . 1 / (1/2) = 2.
  - **Câu hỏi:** Tính tích phân từ 0 đến 9 của 2/sqrt(x) dx (hàm không bị chặn gần 0).
  - **Đáp án:** 12
    1. Xét tích phân từ a đến 9 với a -> 0+. Nguyên hàm của x^(-1/2) là x^(1/2) / (1/2).
    2. a^(1/2) -> 0 vì số mũ dương, nên tích phân hội tụ.
    3. Giá trị: 2 . 9^(1/2) / (1/2) = 2 . 3 / (1/2) = 12.
- `gt_t8_l2_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét I = tích phân từ 0 đến 1 của ln x / sqrt(x) dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t5_vd_01`, `gt_t8_l2_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm không bị chặn gần 0, nên I = giới hạn khi a -> 0+ của tích phân từ a đến 1.
    2. Từng phần: u = ln x, dv = x^(-1/2) dx, nên du = dx/x, v = 2 sqrt(x).
    3. Tích phân từ a đến 1 = [2 sqrt(x) ln x] từ a đến 1 - tích phân từ a đến 1 của 2 x^(-1/2) dx.
    4. Khi a -> 0+, ln a -> -vô cùng nên 2 sqrt(a) ln a -> -vô cùng.   **<- bước sai đầu tiên**
    5. Vậy I phân kỳ.
  - **Đáp án:** Bước 4: Khi a -> 0+, ln a -> -vô cùng nên 2 sqrt(a) ln a -> -vô cùng.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: 2 sqrt(a) ln a có dạng 0 . vô cùng; viết thành 2 ln a / a^(-1/2) và dùng L'Hospital được -4 sqrt(a) -> 0.
    2. Phần còn lại: tích phân từ a đến 1 của 2 x^(-1/2) dx = 4 - 4 sqrt(a) -> 4.
    3. Vậy I = 0 - 4 = -4: tích phân hội tụ.
- `gt_t8_l2_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến 2 của 1/sqrt(2x - x^2) dx (hàm không bị chặn ở cả hai đầu) bằng k . pi. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_l2_04`, `gt_t8_l2_02`
  - **Đáp án:** 1
    1. Hoàn thành bình phương: 2x - x^2 = 1 - (x - 1)^2, nên nguyên hàm là arcsin(x - 1).
    2. Tách tại x = 1: phần từ 0 đến 1 cho arcsin 0 - arcsin(-1) = pi/2 (giới hạn khi cận dưới -> 0+), phần từ 1 đến 2 cho arcsin 1 - arcsin 0 = pi/2.
    3. Cả hai hội tụ: tổng là pi, nên k = 1.

### Tiêu chuẩn hội tụ (`gt_t8_tieu_chuan_hoi_tu`)

- `gt_t8_hc_01` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi tích phân từ 1 đến +vô cùng với hàm 1/x^p dùng để so sánh và kết luận đúng.
  - **Đáp án (ghép đúng):**
    - tích phân của 1/(x^2 + x) dx — giống 1/x^2: hội tụ
    - tích phân của sqrt(x)/(x^2 + 1) dx — giống 1/x^(3/2): hội tụ
    - tích phân của x/(x^2 + 1) dx — giống 1/x: phân kỳ
    - tích phân của 1/(x^(1/3) + 1) dx — giống 1/x^(1/3): phân kỳ
  - **Lời giải:**
    1. Khi x -> +vô cùng chỉ giữ lũy thừa cao nhất ở tử và mẫu: 1/(x^2 + x) ~ 1/x^2, sqrt(x)/(x^2 + 1) ~ x^(1/2)/x^2 = 1/x^(3/2).
    2. x/(x^2 + 1) ~ 1/x và 1/(x^(1/3) + 1) ~ 1/x^(1/3).
    3. Tiêu chuẩn so sánh giới hạn: tỉ số với 1/x^p dần tới 1, nên cùng hội tụ hay cùng phân kỳ với tích phân của 1/x^p, hội tụ khi và chỉ khi p > 1.
- `gt_t8_hc_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 1 đến +vô cùng của sin^2 x / x^2 dx hội tụ.
  - **Đáp án:** Đúng
    1. Hàm dưới dấu tích phân không âm và 0 <= sin^2 x / x^2 <= 1/x^2 với mọi x >= 1.
    2. Tích phân từ 1 đến +vô cùng của 1/x^2 dx hội tụ (p = 2 > 1).
    3. Theo tiêu chuẩn so sánh, tích phân đã cho hội tụ: mệnh đề đúng.
- `gt_t8_hc_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với p > 0, tích phân từ 1 đến +vô cùng của x^2 / (x^p + 1) dx hội tụ khi và chỉ khi p > p0. Tìm p0.
  - **Đáp án:** 3
    1. Khi x -> +vô cùng: x^2/(x^p + 1) ~ x^2/x^p = 1/x^(p - 2) (với p > 0 thì x^p -> +vô cùng).
    2. Theo tiêu chuẩn so sánh giới hạn, tích phân hội tụ khi và chỉ khi p - 2 > 1.
    3. Tức p > 3: p0 = 3.
- `gt_g8_hoi_tu_tf` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 1 đến +vô cùng của x/(x^4 + 1) dx hội tụ.
  - **Đáp án:** Đúng
    1. Khi x -> +vô cùng: x/(x^4 + 1) ~ 1/x^3 (tỉ số của chúng dần tới 1).
    2. Theo tiêu chuẩn so sánh giới hạn, tích phân hội tụ khi và chỉ khi tích phân của 1/x^3 hội tụ, tức 3 > 1.
    3. 3 > 1: tích phân hội tụ, mệnh đề đúng.
  - **Câu hỏi:** Tích phân từ 1 đến +vô cùng của 1/(x + 1) dx hội tụ.
  - **Đáp án:** Sai
    1. Khi x -> +vô cùng: 1/(x + 1) ~ 1/x (tỉ số của chúng dần tới 1).
    2. Theo tiêu chuẩn so sánh giới hạn, tích phân hội tụ khi và chỉ khi tích phân của 1/x hội tụ, tức 1 > 1.
    3. 1 <= 1: tích phân phân kỳ, mệnh đề sai.
  - **Câu hỏi:** Tích phân từ 1 đến +vô cùng của x/(x^4 + 1) dx hội tụ.
  - **Đáp án:** Đúng
    1. Khi x -> +vô cùng: x/(x^4 + 1) ~ 1/x^3 (tỉ số của chúng dần tới 1).
    2. Theo tiêu chuẩn so sánh giới hạn, tích phân hội tụ khi và chỉ khi tích phân của 1/x^3 hội tụ, tức 3 > 1.
    3. 3 > 1: tích phân hội tụ, mệnh đề đúng.
- `gt_t8_hc_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lập luận sau (kết luận cuối cùng tình cờ đúng). Đề bài: xét sự hội tụ của tích phân từ 1 đến +vô cùng của 1/(x + sqrt(x)) dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_hc_02`, `gt_t8_hc_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Với x >= 1: x + sqrt(x) >= x > 0.
    2. Suy ra 0 < 1/(x + sqrt(x)) <= 1/x.
    3. Tích phân của 1/x từ 1 đến +vô cùng phân kỳ, nên theo tiêu chuẩn so sánh, tích phân đã cho phân kỳ.   **<- bước sai đầu tiên**
    4. Kết luận: tích phân phân kỳ.
  - **Đáp án:** Bước 3: Tích phân của 1/x từ 1 đến +vô cùng phân kỳ, nên theo tiêu chuẩn so sánh, tích phân đã cho phân kỳ.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 dùng sai chiều: nhỏ hơn một hàm có tích phân phân kỳ thì không kết luận được gì.
    2. Lập luận đúng: x + sqrt(x) <= 2x với x >= 1, nên 1/(x + sqrt(x)) >= 1/(2x), mà tích phân của 1/(2x) phân kỳ.
    3. Hoặc so sánh giới hạn: tỉ số với 1/x dần tới 1. Tích phân thật sự phân kỳ, nhưng bước 3 không chứng minh được điều đó.
- `gt_t8_hc_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến +vô cùng của 1/(sqrt(x)(1 + x)) dx có hội tụ không, và vì sao?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_hc_03`, `gt_t8_hc_01`
    - **(đúng)** Hội tụ, vì gần 0 hàm giống 1/x^(1/2) và ở +vô cùng giống 1/x^(3/2)
    - Phân kỳ, vì hàm không xác định tại x = 0
    - Phân kỳ, vì gần 0 hàm giống 1/x^(1/2)
    - Hội tụ, chỉ vì hàm dần tới 0 khi x -> +vô cùng
  - **Đáp án:** Hội tụ, vì gần 0 hàm giống 1/x^(1/2) và ở +vô cùng giống 1/x^(3/2)
    1. Tích phân suy rộng ở cả hai đầu: tách tại 1 và xét riêng từng phần.
    2. Gần 0: 1/(sqrt(x)(1 + x)) ~ 1/x^(1/2), và tích phân từ 0 đến 1 của 1/x^p hội tụ khi p < 1. Ở +vô cùng: ~ 1/x^(3/2), hội tụ vì 3/2 > 1.
    3. Hàm dần tới 0 chưa đủ (1/x cũng dần tới 0). Thực ra tích phân bằng pi (đặt x = t^2).
- `gt_t8_hc_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích phân từ 0 đến +vô cùng của 1/(x^p (1 + x)) dx hội tụ khi và chỉ khi a < p < b. Nhập a, b theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_hc_03`, `gt_t8_l2_02`
  - **Đáp án:** 0, 1
    1. Tách tại 1. Gần 0: hàm ~ 1/x^p, tích phân từ 0 đến 1 hội tụ khi và chỉ khi p < 1.
    2. Ở +vô cùng: hàm ~ 1/x^(p + 1), tích phân từ 1 đến +vô cùng hội tụ khi và chỉ khi p + 1 > 1, tức p > 0.
    3. Cả hai cùng hội tụ khi 0 < p < 1: a = 0, b = 1.
- `gt_t8_hc_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: xét I = tích phân từ 1 đến +vô cùng của 1/(x(x^2 + 1)) dx.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t8_hc_01`, `gt_t7_ht_01`, `gt_t8_l1_01`
  - **Phần a** (Trắc nghiệm): a) So sánh với hàm nào để biết I hội tụ?
    - **(đúng)** 1/x^3: hội tụ
    - 1/x: phân kỳ
    - 1/x^2: phân kỳ
    - Không so sánh được
    - **Đáp án a:** 1/x^3: hội tụ
  - **Phần b** (Điền số): b) I = k . ln 2. Tìm k.
    - **Đáp án b:** 1/2
  - **Phần c** (Đúng/Sai): c) I nhỏ hơn tích phân từ 1 đến +vô cùng của 1/x^3 dx.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) 1/(x(x^2 + 1)) ~ 1/x^3 khi x -> +vô cùng, và p = 3 > 1: hội tụ.
    2. b) Tách: 1/(x(x^2 + 1)) = 1/x - x/(x^2 + 1). Nguyên hàm ln x - (1/2) ln(x^2 + 1) = (1/2) ln(x^2/(x^2 + 1)) -> 0 khi x -> +vô cùng; tại 1 bằng (1/2) ln(1/2). Vậy I = (1/2) ln 2, k = 1/2.
    3. c) Tích phân của 1/x^3 từ 1 đến +vô cùng là 1/2, còn I = (1/2) ln 2 xấp xỉ 0.347 < 1/2 (cũng thấy ngay vì 1/(x(x^2 + 1)) < 1/x^3): đúng.

## Tầng 9: Hàm nhiều biến

43 dạng câu (36 câu viết tay, 7 bộ sinh câu); 43 chưa duyệt.

### Miền xác định, giới hạn và liên tục (`gt_t9_gioi_han_lien_tuc`)

- `gt_t9_gh_01` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét giới hạn của f(x, y) = xy/(x^2 + y^2) khi (x, y) -> (0, 0). Khẳng định nào đúng?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t3_mp_05`, `gt_t5_vd_05`
    - **(đúng)** Không tồn tại, vì dọc đường y = kx giới hạn bằng k/(1 + k^2), phụ thuộc k
    - Bằng 0, vì dọc hai trục tọa độ f luôn bằng 0
    - Bằng 1/2
    - Bằng 0, vì tử có bậc hai bằng bậc của mẫu
  - **Đáp án:** Không tồn tại, vì dọc đường y = kx giới hạn bằng k/(1 + k^2), phụ thuộc k
    1. Dọc y = kx (x khác 0): f = kx^2/(x^2 + k^2 x^2) = k/(1 + k^2), không phụ thuộc x.
    2. k = 0 cho 0 nhưng k = 1 cho 1/2: hai đường đi tới (0, 0) cho hai giới hạn khác nhau.
    3. Vậy giới hạn không tồn tại. Hai trục chỉ là hai đường trong vô số đường, không đủ để kết luận.
- `gt_t9_gh_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^2 y^2 / (x^2 + y^2) khi (x, y) khác (0, 0) và f(0, 0) = a. Tìm a để f liên tục tại (0, 0).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t3_ld_07`, `gt_t5_lh_05`
  - **Đáp án:** 0
    1. Cần a bằng giới hạn của f khi (x, y) -> (0, 0), nếu giới hạn đó tồn tại.
    2. Vì x^2 <= x^2 + y^2 nên 0 <= f(x, y) = (x^2/(x^2 + y^2)) . y^2 <= y^2.
    3. y^2 -> 0, nên theo nguyên lý kẹp giới hạn bằng 0 (theo mọi cách tiến về gốc). Vậy a = 0.
- `gt_t9_gh_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét giới hạn của f(x, y) = x^2 y / (x^4 + y^2) khi (x, y) -> (0, 0).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t3_mp_05`, `gt_t5_vd_05`
  - **Lời giải đưa ra (có một bước sai):**
    1. Dọc trục Ox (y = 0, x khác 0): f = 0, nên giới hạn dọc trục này là 0.
    2. Dọc đường y = kx với k khác 0: f = kx/(x^2 + k^2) -> 0 khi x -> 0.
    3. Mọi đường thẳng qua gốc đều cho giới hạn 0, nên giới hạn của f bằng 0.   **<- bước sai đầu tiên**
    4. Vậy f liên tục tại (0, 0) nếu gán f(0, 0) = 0.
  - **Đáp án:** Bước 3: Mọi đường thẳng qua gốc đều cho giới hạn 0, nên giới hạn của f bằng 0.
  - **Vì sao sai, và bước đúng:**
    1. Hai bước đầu tính đúng.
    2. Bước 3 sai: đi theo mọi đường thẳng vẫn chưa phải là đi theo mọi cách. Dọc parabol y = x^2: f = x^4/(2x^4) = 1/2.
    3. Hai cách tiến cho 0 và 1/2, nên giới hạn không tồn tại, và không gán được giá trị nào để f liên tục tại (0, 0).
- `gt_t9_gh_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điểm (1, 1) thuộc miền xác định của hàm f(x, y) = ln(y - x^2) + sqrt(4 - x^2 - y^2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t3_ld_08`, `gt_t3_ld_07`, `gt_t5_vd_05`
  - **Đáp án:** Sai
    1. Miền xác định cần đồng thời y - x^2 > 0 (ln) và 4 - x^2 - y^2 >= 0 (căn).
    2. Tại (1, 1): y - x^2 = 0, không dương, nên ln(y - x^2) không có nghĩa (điều kiện thứ hai thì thỏa: 4 - 2 = 2 >= 0).
    3. Điểm nằm trên biên y = x^2, không thuộc miền xác định: mệnh đề sai.
- `gt_t9_gh_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Miền xác định của f(x, y) = sqrt(9 - x^2 - y^2) / sqrt(x^2 + y^2 - 1) là một hình vành khăn trong mặt phẳng. Diện tích của nó bằng k . pi. Tìm k.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t3_ld_08`, `gt_t8_dt_01`
  - **Đáp án:** 8
    1. Tử cần 9 - x^2 - y^2 >= 0, tức x^2 + y^2 <= 9. Mẫu là căn ở mẫu số nên cần x^2 + y^2 - 1 > 0.
    2. Miền: 1 < x^2 + y^2 <= 9, vành khăn giữa đường tròn bán kính 1 (bỏ biên) và bán kính 3 (lấy biên).
    3. Diện tích: pi . 3^2 - pi . 1^2 = 8pi, nên k = 8 (biên không làm đổi diện tích).

### Đạo hàm riêng (`gt_t9_dao_ham_rieng`)

- `gt_t9_dr_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^3 y^2 - 2xy + sin(xy). Tính f_xy(1, 0), với f_xy = (f_x)_y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_qt_05`, `gt_t4_vp_05`, `gt_t6_ll_05`
  - **Đáp án:** -1
    1. Giữ y cố định: f_x = 3x^2 y^2 - 2y + y cos(xy).
    2. Lấy đạo hàm theo y (giữ x cố định): f_xy = 6x^2 y - 2 + cos(xy) - xy sin(xy).
    3. Tại (1, 0): 0 - 2 + cos 0 - 0 = -1.
- `gt_t9_dr_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = xy(x^2 - y^2)/(x^2 + y^2) khi (x, y) khác (0, 0) và f(0, 0) = 0. Khi đó f_xy(0, 0) = f_yx(0, 0), với f_xy = (f_x)_y và f_yx = (f_y)_x.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dn_06`, `gt_t5_vd_05`
  - **Đáp án:** Sai
    1. Dùng định nghĩa: f_x(0, y) = giới hạn của (f(h, y) - f(0, y))/h = y(h^2 - y^2)/(h^2 + y^2) -> -y khi h -> 0 (với y khác 0; và f_x(0, 0) = 0). Vậy f_x(0, y) = -y, nên f_xy(0, 0) = -1.
    2. Tương tự f_y(x, 0) = x(x^2 - 0)/x^2 = x, nên f_yx(0, 0) = 1.
    3. -1 khác 1: mệnh đề sai. Định lý Schwarz không áp dụng vì các đạo hàm riêng cấp hai không liên tục tại (0, 0).
- `gt_t9_dr_03` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^2 y + y^3. Ghép mỗi đạo hàm riêng với biểu thức của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_qt_06`, `gt_t4_vp_05`, `gt_t6_ll_05`
  - **Đáp án (ghép đúng):**
    - f_x — 2xy
    - f_y — x^2 + 3y^2
    - f_xx — 2y
    - f_yy — 6y
    - f_xy — 2x
  - **Lời giải:**
    1. f_x: giữ y cố định, (x^2 y)' = 2xy và y^3 là hằng số: f_x = 2xy.
    2. f_y: giữ x cố định: x^2 + 3y^2.
    3. Lấy đạo hàm tiếp: f_xx = (2xy)_x = 2y, f_yy = (x^2 + 3y^2)_y = 6y, f_xy = (2xy)_y = 2x (bằng f_yx = (x^2 + 3y^2)_x = 2x).
- `gt_t9_dr_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hằng số a để hàm u(x, y) = x^3 + a x y^2 thỏa phương trình Laplace u_xx + u_yy = 0 tại mọi điểm.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_vp_05`, `gt_t6_ll_05`
  - **Đáp án:** -3
    1. u_x = 3x^2 + a y^2, nên u_xx = 6x.
    2. u_y = 2axy, nên u_yy = 2ax.
    3. u_xx + u_yy = (6 + 2a)x = 0 với mọi x khi và chỉ khi a = -3.
- `gt_t9_dr_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: cho f(x, y) = x^y với x > 0, tính f_x và f_y tại (2, 3).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_qt_06`, `gt_g4_ln_hop`, `gt_t5_vd_08`
  - **Lời giải đưa ra (có một bước sai):**
    1. Với x > 0 viết được f(x, y) = x^y = e^(y ln x).
    2. Tính f_x: giữ y cố định, f là hàm lũy thừa của x, nên f_x = y x^(y - 1).
    3. Tính f_y: giữ x cố định, f cũng là hàm lũy thừa, nên f_y = x y^(x - 1).   **<- bước sai đầu tiên**
    4. Tại (2, 3): f_x = 3 . 2^2 = 12 và f_y = 2 . 3^1 = 6.
  - **Đáp án:** Bước 3: Tính f_y: giữ x cố định, f cũng là hàm lũy thừa, nên f_y = x y^(x - 1).
  - **Vì sao sai, và bước đúng:**
    1. Bước 2 đúng: khi y cố định, x^y là lũy thừa của x.
    2. Bước 3 sai: khi x cố định, x^y là hàm mũ của y, không phải lũy thừa. Từ e^(y ln x): f_y = ln x . e^(y ln x) = x^y ln x.
    3. Đúng là f_y(2, 3) = 8 ln 2.
- `gt_g9_dao_ham_rieng` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = -2x^3y + xy - 3y^2. Tính f_xx(2, 2).
  - **Đáp án:** -48
    1. f_x = -6x^2y + y (giữ biến còn lại cố định).
    2. f_xx = -12xy.
    3. Tại (2, 2): f_xx = -48.
  - **Câu hỏi:** Cho f(x, y) = -3xy^2 + 2xy + 3y^2. Tính f_xx(-1, 1).
  - **Đáp án:** 0
    1. f_x = -3y^2 + 2y (giữ biến còn lại cố định).
    2. f_xx = 0.
    3. Tại (-1, 1): f_xx = 0.
  - **Câu hỏi:** Cho f(x, y) = -2x^3y^3 - 2xy - y^2. Tính f_yy(2, -2).
  - **Đáp án:** 190
    1. f_y = -6x^3y^2 - 2x - 2y (giữ biến còn lại cố định).
    2. f_yy = -12x^3y - 2.
    3. Tại (2, -2): f_yy = 190.

### Vi phân toàn phần, hàm ẩn và công thức Taylor (`gt_t9_vi_phan_ham_an`)

- `gt_t9_vp_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng vi phân toàn phần của f(x, y) = sqrt(x^2 + y^2) tại (3, 4), tính gần đúng sqrt(3.02^2 + 3.97^2). Nhập đúng giá trị của phép tính gần đúng đó (một số thập phân).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_vp_07`, `gt_t5_ty_05`
  - **Đáp án:** 1247/250
    1. f(3, 4) = 5; f_x = x/sqrt(x^2 + y^2) = 3/5 và f_y = 4/5 tại (3, 4).
    2. Số gia: dx = 0.02, dy = -0.03. df = (3/5)(0.02) + (4/5)(-0.03) = 0.012 - 0.024 = -0.012.
    3. Gần đúng: 5 - 0.012 = 4.988 (giá trị thật xấp xỉ 4.98812).
- `gt_t9_vp_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^2 + xy + y^3 = 3 xác định một hàm ẩn y = y(x) gần điểm (1, 1). Nhập y'(1) rồi y''(1) theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_nt_06`, `gt_t4_nt_04`, `gt_t6_ll_05`
  - **Đáp án:** -3/4, -31/32
    1. Đạo hàm hai vế theo x: 2x + y + x y' + 3y^2 y' = 0. Tại (1, 1): 3 + 4y' = 0, nên y'(1) = -3/4.
    2. Đạo hàm thêm lần nữa: 2 + 2y' + x y'' + 6y (y')^2 + 3y^2 y'' = 0.
    3. Tại (1, 1) với y' = -3/4: 2 - 3/2 + 6 . 9/16 + 4y'' = 0, tức 1/2 + 27/8 + 4y'' = 0.
    4. 4y'' = -31/8, nên y''(1) = -31/32.
- `gt_t9_vp_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khai triển Taylor bậc hai của f(x, y) = e^x ln(1 + y) tại (0, 0) có phần bậc hai là A x^2 + B xy + C y^2. Nhập A, B, C theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t5_ty_08`, `gt_t5_mc_05`
  - **Đáp án:** 0, 1, -1/2
    1. Nhân hai khai triển một biến: e^x = 1 + x + x^2/2 + ..., ln(1 + y) = y - y^2/2 + ...
    2. Tích, giữ các số hạng bậc tổng <= 2: (1 + x)(y - y^2/2) = y + xy - y^2/2 + (bậc ba trở lên).
    3. Không có x^2 (mọi số hạng đều chứa y): A = 0, B = 1, C = -1/2.
    4. Kiểm tra bằng đạo hàm: f_xx(0,0) = 0, f_xy(0,0) = 1, f_yy(0,0) = -1, và hệ số là f_xx/2, f_xy, f_yy/2.
- `gt_t9_vp_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** F(x, y) có các đạo hàm riêng liên tục, F(x0, y0) = 0 và F_y(x0, y0) khác 0. Sắp xếp các bước tìm đạo hàm của hàm ẩn y = y(x) xác định bởi F(x, y) = 0 gần (x0, y0).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t6_ll_05`
  - **Đáp án (thứ tự đúng):**
    1. Theo định lý hàm ẩn, gần x0 có hàm khả vi y(x) với y(x0) = y0 và F(x, y(x)) = 0.
    2. Đạo hàm hai vế theo x bằng quy tắc dây chuyền: F_x + F_y . y'(x) = 0.
    3. F_y khác 0 gần (x0, y0) vì nó liên tục, nên chia được cho F_y.
    4. Kết luận: y'(x) = -F_x / F_y.
  - **Lời giải:**
    1. Điều kiện F_y khác 0 vừa bảo đảm hàm ẩn tồn tại vừa cho phép chia.
    2. Quy tắc dây chuyền cho hàm hai biến: x đi vào F trực tiếp và qua y(x).
    3. Ví dụ x^2 + y^2 = 25 tại (3, 4): y' = -2x/(2y) = -3/4.
- `gt_t9_vp_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vi phân toàn phần của z = x^2 y + ln y (y > 0) là gì?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_qt_06`, `gt_t5_ty_05`
    - **(đúng)** dz = 2xy dx + (x^2 + 1/y) dy
    - dz = 2xy dx + x^2 dy
    - dz = (2xy + x^2 + 1/y)(dx + dy)
    - dz = 2x dx + (1/y) dy
  - **Đáp án:** dz = 2xy dx + (x^2 + 1/y) dy
    1. dz = z_x dx + z_y dy.
    2. z_x = 2xy (ln y là hằng số khi giữ y cố định), z_y = x^2 + 1/y.
    3. Vậy dz = 2xy dx + (x^2 + 1/y) dy; đáp án thứ hai quên ln y, đáp án thứ ba cộng nhầm hai đạo hàm riêng.
- `gt_t9_vp_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: phương trình x^2 + y^2 + z^2 = 9 xác định z = z(x, y) gần điểm P(1, 2, 2) của mặt cầu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_nt_04`, `gt_t5_ty_08`
  - **Phần a** (Điền số): a) Tính z_x tại (1, 2).
    - **Đáp án a:** -1/2
  - **Phần b** (Điền số): b) Tính z_y tại (1, 2).
    - **Đáp án b:** -1
  - **Phần c** (Điền số): c) Mặt phẳng tiếp xúc tại P có phương trình x + 2y + 2z = d. Tìm d.
    - **Đáp án c:** 9
  - **Lời giải:**
    1. a) Với F = x^2 + y^2 + z^2 - 9: z_x = -F_x/F_z = -2x/(2z) = -x/z = -1/2 tại P.
    2. b) z_y = -y/z = -2/2 = -1.
    3. c) Mặt phẳng tiếp xúc: z - 2 = -(1/2)(x - 1) - (y - 2). Nhân 2: 2z - 4 = -x + 1 - 2y + 4, tức x + 2y + 2z = 9. (Đúng như hình học: pháp tuyến của mặt cầu là bán kính (1, 2, 2).)
- `gt_g9_ham_an` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình x^2 - 2xy - 2y^2 = -3 xác định một hàm ẩn y = y(x) gần điểm (1, -2). Tính y'(1).
  - **Đáp án:** -1
    1. Với F(x, y) = x^2 - 2xy - 2y^2 - (-3): F_x = 2x - 2y, F_y = -2x - 4y.
    2. Tại (1, -2): F_x = 6, F_y = 6 (khác 0, nên hàm ẩn tồn tại).
    3. y' = -F_x / F_y = -1.
  - **Câu hỏi:** Phương trình x^2 + 3xy - 2y^2 = 8 xác định một hàm ẩn y = y(x) gần điểm (-2, -2). Tính y'(-2).
  - **Đáp án:** 5
    1. Với F(x, y) = x^2 + 3xy - 2y^2 - 8: F_x = 2x + 3y, F_y = 3x - 4y.
    2. Tại (-2, -2): F_x = -10, F_y = 2 (khác 0, nên hàm ẩn tồn tại).
    3. y' = -F_x / F_y = 5.
  - **Câu hỏi:** Phương trình x^2 - 2xy - y^2 = -7 xác định một hàm ẩn y = y(x) gần điểm (1, 2). Tính y'(1).
  - **Đáp án:** -1/3
    1. Với F(x, y) = x^2 - 2xy - y^2 - (-7): F_x = 2x - 2y, F_y = -2x - 2y.
    2. Tại (1, 2): F_x = -2, F_y = -6 (khác 0, nên hàm ẩn tồn tại).
    3. y' = -F_x / F_y = -1/3.

### Cực trị của hàm hai biến (`gt_t9_cuc_tri`)

- `gt_t9_ct_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x, y) = x^3 + y^3 - 3xy có đúng một điểm cực tiểu địa phương. Tìm giá trị cực tiểu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_g6_cuc_tri`, `gt_t6_ct_05`
  - **Đáp án:** -1
    1. Điểm dừng: f_x = 3x^2 - 3y = 0, f_y = 3y^2 - 3x = 0. Từ y = x^2 được x^4 = x: x = 0 hoặc x = 1. Hai điểm dừng (0, 0) và (1, 1).
    2. f_xx = 6x, f_yy = 6y, f_xy = -3; D = f_xx f_yy - f_xy^2.
    3. Tại (0, 0): D = -9 < 0, điểm yên ngựa. Tại (1, 1): D = 36 - 9 = 27 > 0 và f_xx = 6 > 0: cực tiểu.
    4. Giá trị cực tiểu f(1, 1) = 1 + 1 - 3 = -1.
- `gt_t9_ct_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Điểm dừng (0, 0) của f(x, y) = x^2 + 4xy + y^2 là điểm gì?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ct_03`, `gt_t6_ct_07`
    - **(đúng)** Điểm yên ngựa
    - Cực tiểu
    - Cực đại
    - Chưa kết luận được vì D = 0
  - **Đáp án:** Điểm yên ngựa
    1. f_xx = 2, f_yy = 2, f_xy = 4: D = 2 . 2 - 4^2 = -12 < 0.
    2. D < 0 nghĩa là điểm yên ngựa, dù f_xx và f_yy đều dương.
    3. Kiểm tra: dọc y = x, f = 6x^2 >= 0; dọc y = -x, f = -2x^2 <= 0. f nhận cả giá trị dương lẫn âm quanh gốc.
- `gt_t9_ct_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: xét cực trị của f(x, y) = x^4 + y^4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ct_06`, `gt_t6_ct_07`
  - **Lời giải đưa ra (có một bước sai):**
    1. f_x = 4x^3, f_y = 4y^3: điểm dừng duy nhất là (0, 0).
    2. f_xx = 12x^2, f_yy = 12y^2, f_xy = 0: cả ba bằng 0 tại (0, 0).
    3. D = f_xx f_yy - f_xy^2 = 0 tại (0, 0).
    4. D = 0 nên (0, 0) không phải điểm cực trị.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: D = 0 nên (0, 0) không phải điểm cực trị.
  - **Vì sao sai, và bước đúng:**
    1. Ba bước đầu đúng.
    2. Bước 4 sai: D = 0 nghĩa là dấu hiệu đạo hàm cấp hai không kết luận được, không có nghĩa là không có cực trị.
    3. Xét trực tiếp: f(x, y) >= 0 = f(0, 0) với mọi (x, y), nên (0, 0) là cực tiểu (cả toàn cục).
- `gt_t9_ct_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^3 - 3x + y^2 - 4y. Nhập số điểm cực trị của f, rồi giá trị cực tiểu của f.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_g6_cuc_tri`, `gt_t6_ct_05`
  - **Đáp án:** 1, -6
    1. f_x = 3x^2 - 3 = 0 cho x = 1 hoặc x = -1; f_y = 2y - 4 = 0 cho y = 2. Hai điểm dừng (1, 2), (-1, 2).
    2. f_xx = 6x, f_yy = 2, f_xy = 0. Tại (1, 2): D = 12 > 0, f_xx > 0: cực tiểu. Tại (-1, 2): D = -12 < 0: yên ngựa.
    3. Chỉ có 1 điểm cực trị; giá trị cực tiểu f(1, 2) = 1 - 3 + 4 - 8 = -6.
- `gt_t9_ct_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với f(x, y) = 2x^2 + 2xy + y^2 - 2x + 1, ta có f(x, y) >= 0 với mọi (x, y) thuộc R^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_05`, `gt_t6_ct_07`
  - **Đáp án:** Đúng
    1. Điểm dừng: f_x = 4x + 2y - 2 = 0, f_y = 2x + 2y = 0, nên x = 1, y = -1, và f(1, -1) = 2 - 2 + 1 - 2 + 1 = 0.
    2. Ma trận đạo hàm cấp hai [4, 2; 2, 2] có f_xx = 4 > 0 và D = 8 - 4 = 4 > 0 tại mọi điểm: f là hàm bậc hai lồi, điểm dừng là cực tiểu toàn cục.
    3. Cũng thấy trực tiếp: f = (x + y)^2 + (x - 1)^2 >= 0. Mệnh đề đúng.
- `gt_t9_ct_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: cho f(x, y) = x^3 - 12x + y^3 - 3y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_g6_cuc_tri`, `gt_g6_so_cuc_tri`, `gt_t6_ct_05`
  - **Phần a** (Điền số): a) f có bao nhiêu điểm dừng?
    - **Đáp án a:** 4
  - **Phần b** (Điền số): b) Trong đó có bao nhiêu điểm cực trị địa phương?
    - **Đáp án b:** 2
  - **Phần c** (Điền số): c) Tìm giá trị cực đại của f.
    - **Đáp án c:** 18
  - **Lời giải:**
    1. a) f_x = 3x^2 - 12 = 0 cho x = 2 hoặc -2; f_y = 3y^2 - 3 = 0 cho y = 1 hoặc -1. Ghép lại: 4 điểm dừng.
    2. b) f_xx = 6x, f_yy = 6y, f_xy = 0, D = 36xy. D > 0 khi x, y cùng dấu: (2, 1) cực tiểu (f_xx > 0), (-2, -1) cực đại (f_xx < 0). Hai điểm còn lại D < 0: yên ngựa. Có 2 điểm cực trị.
    3. c) f(-2, -1) = -8 + 24 - 1 + 3 = 18.
- `gt_g9_cuc_tri_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Điểm (-1, -3) là điểm dừng duy nhất của f(x, y) = -2x^2 - 3xy + 2y^2 - 13x + 9y, và f đạt cực đại địa phương tại đó.
  - **Đáp án:** Sai
    1. f_xx = -4, f_yy = 4, f_xy = -3 tại mọi điểm.
    2. D = f_xx f_yy - f_xy^2 = -16 - 9 = -25.
    3. D < 0: điểm yên ngựa, không phải cực trị.
    4. Mệnh đề sai.
  - **Câu hỏi:** Điểm (-1, 3) là điểm dừng duy nhất của f(x, y) = -3x^2 - 3xy - 3y^2 + 3x + 15y, và f đạt cực tiểu địa phương tại đó.
  - **Đáp án:** Sai
    1. f_xx = -6, f_yy = -6, f_xy = -3 tại mọi điểm.
    2. D = f_xx f_yy - f_xy^2 = 36 - 9 = 27.
    3. D > 0 và f_xx = -6 < 0: cực đại.
    4. Mệnh đề sai.
  - **Câu hỏi:** Điểm (-2, -1) là điểm dừng duy nhất của f(x, y) = -2x^2 + 4xy + 2y^2 - 4x + 12y, và f đạt cực đại địa phương tại đó.
  - **Đáp án:** Sai
    1. f_xx = -4, f_yy = 4, f_xy = 4 tại mọi điểm.
    2. D = f_xx f_yy - f_xy^2 = -16 - 16 = -32.
    3. D < 0: điểm yên ngựa, không phải cực trị.
    4. Mệnh đề sai.
- `gt_g9_diem_dung` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x, y) = -2x^2 - 3xy + 2y^2 - 13x + 9y có đúng một điểm dừng (x0, y0). Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -1, -3
    1. f_x = -4x - 3y - 13 = 0 và f_y = -3x + 4y + 9 = 0.
    2. Định thức của hệ: -4 . 4 - (-3)^2 = -25, khác 0: nghiệm duy nhất.
    3. Giải hệ được x0 = -1, y0 = -3 (thay lại vào hai phương trình để kiểm tra).
  - **Câu hỏi:** Hàm f(x, y) = -3x^2 - 3xy - 3y^2 + 3x + 15y có đúng một điểm dừng (x0, y0). Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -1, 3
    1. f_x = -6x - 3y + 3 = 0 và f_y = -3x - 6y + 15 = 0.
    2. Định thức của hệ: -6 . (-6) - (-3)^2 = 27, khác 0: nghiệm duy nhất.
    3. Giải hệ được x0 = -1, y0 = 3 (thay lại vào hai phương trình để kiểm tra).
  - **Câu hỏi:** Hàm f(x, y) = -2x^2 + 4xy + 2y^2 - 4x + 12y có đúng một điểm dừng (x0, y0). Nhập x0, y0 theo đúng thứ tự.
  - **Đáp án:** -2, -1
    1. f_x = -4x + 4y - 4 = 0 và f_y = 4x + 4y + 12 = 0.
    2. Định thức của hệ: -4 . 4 - 4^2 = -32, khác 0: nghiệm duy nhất.
    3. Giải hệ được x0 = -2, y0 = -1 (thay lại vào hai phương trình để kiểm tra).

### Cực trị có điều kiện (`gt_t9_cuc_tri_dieu_kien`)

- `gt_t9_cd_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị lớn nhất và nhỏ nhất của f(x, y) = x + 2y trên đường tròn x^2 + y^2 = 5. Nhập GTLN rồi GTNN.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ct_01`, `gt_t6_gl_05`
  - **Đáp án:** 5, -5
    1. Lagrange: grad f = lambda . grad g với g = x^2 + y^2: 1 = 2 lambda x, 2 = 2 lambda y, nên y = 2x.
    2. Thay vào ràng buộc: x^2 + 4x^2 = 5, x = 1 hoặc x = -1: hai điểm (1, 2) và (-1, -2).
    3. f(1, 2) = 5, f(-1, -2) = -5. Đường tròn đóng và bị chặn nên f đạt GTLN 5 và GTNN -5.
- `gt_t9_cd_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm giá trị nhỏ nhất của x^2 + y^2 + z^2 với điều kiện x + 2y + 2z = 9.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ct_01`, `gt_t6_gl_05`
  - **Đáp án:** 9
    1. Lagrange: (2x, 2y, 2z) = lambda (1, 2, 2), nên (x, y, z) = (lambda/2)(1, 2, 2).
    2. Thay vào ràng buộc: (lambda/2)(1 + 4 + 4) = 9, lambda/2 = 1: điểm (1, 2, 2).
    3. Giá trị: 1 + 4 + 4 = 9. Đây là bình phương khoảng cách từ gốc tới mặt phẳng: (9/sqrt(9))^2 = 9.
- `gt_t9_cd_03` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm cực trị của f(x, y) với điều kiện g(x, y) = 0 bằng phương pháp nhân tử Lagrange.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_07`, `gt_t6_gl_05`
  - **Đáp án (thứ tự đúng):**
    1. Lập hàm Lagrange L(x, y, lambda) = f(x, y) - lambda g(x, y).
    2. Viết hệ L_x = 0, L_y = 0 và g(x, y) = 0 (ba phương trình, ba ẩn).
    3. Giải hệ để được các điểm nghi ngờ (x, y), bỏ qua những điểm có grad g = 0 thì xét riêng.
    4. Tính f tại từng điểm nghi ngờ.
    5. Nếu đường ràng buộc đóng và bị chặn, giá trị lớn nhất trong số đó là GTLN, nhỏ nhất là GTNN.
  - **Lời giải:**
    1. Tại một điểm cực trị có điều kiện, grad f song song với grad g: đó là ý nghĩa của L_x = L_y = 0.
    2. Phương trình g = 0 bảo đảm điểm nằm trên đường ràng buộc.
    3. So sánh các giá trị như khi tìm GTLN, GTNN trên đoạn.
- `gt_t9_cd_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: tìm GTLN, GTNN của f(x, y) = xy trên đường tròn x^2 + y^2 = 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_02`, `gt_t6_gl_05`
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàm Lagrange: L = xy - lambda(x^2 + y^2 - 1).
    2. L_x = y - 2 lambda x = 0 và L_y = x - 2 lambda y = 0.
    3. Từ hai phương trình: y = 2 lambda x và x = 2 lambda y, nên x = 4 lambda^2 x. Nếu x = 0 thì y = 0, không nằm trên đường tròn; vậy x khác 0.
    4. Chia cho x: 4 lambda^2 = 1, nên lambda = 1/2.   **<- bước sai đầu tiên**
    5. Khi đó y = x, x = y = 1/sqrt(2) hoặc -1/sqrt(2), và f = 1/2 tại cả hai điểm: GTLN = GTNN = 1/2.
  - **Đáp án:** Bước 4: Chia cho x: 4 lambda^2 = 1, nên lambda = 1/2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 bỏ sót nghiệm: 4 lambda^2 = 1 cho lambda = 1/2 hoặc lambda = -1/2.
    2. lambda = -1/2 cho y = -x, hai điểm (1/sqrt(2), -1/sqrt(2)) và (-1/sqrt(2), 1/sqrt(2)) với f = -1/2.
    3. Đúng là GTLN = 1/2, GTNN = -1/2.
- `gt_t9_cd_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một tông môn cần đúc một hộp chứa linh thạch hình hộp chữ nhật không nắp, thể tích 32. Đáy x . y, cao z. Tìm diện tích vật liệu nhỏ nhất xy + 2xz + 2yz.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_06`, `gt_t6_gl_05`
  - **Đáp án:** 48
    1. Lagrange với ràng buộc xyz = 32: y + 2z = lambda yz, x + 2z = lambda xz, 2x + 2y = lambda xy.
    2. Nhân ba phương trình lần lượt với x, y, z: xy + 2xz = xy + 2yz = 2xz + 2yz (= 32 lambda). Từ hai đẳng thức đầu x = y; từ hai đẳng thức sau xy = 2xz, tức y = 2z.
    3. Vậy x = y = 2z; xyz = 4z^3 = 32 nên z = 2, x = y = 4.
    4. Diện tích: 16 + 16 + 16 = 48 (khi z -> 0 hoặc x -> 0 diện tích -> +vô cùng, nên đây là giá trị nhỏ nhất).
- `gt_t9_cd_tk_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: tìm cực trị của f(x, y) = x^2 + 2y^2 trên đường tròn x^2 + y^2 = 4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ct_01`, `gt_t6_gl_05`
  - **Phần a** (Điền số): a) Hệ Lagrange (grad f = lambda . grad g, và ràng buộc) có bao nhiêu nghiệm (x, y)?
    - **Đáp án a:** 4
  - **Phần b** (Điền số): b) Tìm GTLN của f trên đường tròn.
    - **Đáp án b:** 8
  - **Phần c** (Điền số): c) Tìm GTNN của f trên đường tròn.
    - **Đáp án c:** 4
  - **Lời giải:**
    1. a) 2x = 2 lambda x và 4y = 2 lambda y. Phương trình đầu: x = 0 hoặc lambda = 1. x = 0 cho y = 2 hoặc -2. lambda = 1 làm phương trình sau thành 4y = 2y, y = 0, nên x = 2 hoặc -2. Tổng cộng 4 điểm.
    2. b) Tại (0, 2) và (0, -2): f = 8. Đây là GTLN.
    3. c) Tại (2, 0) và (-2, 0): f = 4, GTNN. Kiểm tra: f = 4 + y^2 trên đường tròn, với 0 <= y^2 <= 4.
- `gt_g9_lagrange` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm GTLN và GTNN của f(x, y) = 5x - 12y trên đường tròn x^2 + y^2 = 1. Nhập GTLN rồi GTNN.
  - **Đáp án:** 13, -13
    1. Lagrange: (5, -12) = lambda . (2x, 2y), nên (x, y) cùng phương với (5, -12).
    2. Trên đường tròn bán kính 1, độ dài của (5, -12) là 13: hai điểm (5/13, -12/13) và (-5/13, 12/13).
    3. f(5/13, -12/13) = 5 . (5/13) + (-12) . (-12/13) = 13; tại điểm đối xứng f = -13.
    4. GTLN = 13, GTNN = -13 (bằng bán kính 1 nhân độ dài 13 của (5, -12), với dấu cộng và trừ).
  - **Câu hỏi:** Tìm GTLN và GTNN của f(x, y) = 3x + 4y trên đường tròn x^2 + y^2 = 4. Nhập GTLN rồi GTNN.
  - **Đáp án:** 10, -10
    1. Lagrange: (3, 4) = lambda . (2x, 2y), nên (x, y) cùng phương với (3, 4).
    2. Trên đường tròn bán kính 2, độ dài của (3, 4) là 5: hai điểm (6/5, 8/5) và (-6/5, -8/5).
    3. f(6/5, 8/5) = 3 . (6/5) + 4 . (8/5) = 10; tại điểm đối xứng f = -10.
    4. GTLN = 10, GTNN = -10 (bằng bán kính 2 nhân độ dài 5 của (3, 4), với dấu cộng và trừ).
  - **Câu hỏi:** Tìm GTLN và GTNN của f(x, y) = 12x - 5y trên đường tròn x^2 + y^2 = 9. Nhập GTLN rồi GTNN.
  - **Đáp án:** 39, -39
    1. Lagrange: (12, -5) = lambda . (2x, 2y), nên (x, y) cùng phương với (12, -5).
    2. Trên đường tròn bán kính 3, độ dài của (12, -5) là 13: hai điểm (36/13, -15/13) và (-36/13, 15/13).
    3. f(36/13, -15/13) = 12 . (36/13) + (-5) . (-15/13) = 39; tại điểm đối xứng f = -39.
    4. GTLN = 39, GTNN = -39 (bằng bán kính 3 nhân độ dài 13 của (12, -5), với dấu cộng và trừ).

### Gradient, Jacobian và lan truyền ngược (`gt_t9_gradient_lan_truyen`)

- `gt_t9_gr_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = x^2 y + y^3. Tính đạo hàm của f tại (1, 2) theo hướng vector đơn vị u = (3/5, 4/5).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Đáp án:** 64/5
    1. grad f = (2xy, x^2 + 3y^2) = (4, 13) tại (1, 2).
    2. Đạo hàm theo hướng u = grad f . u (tích vô hướng), vì f khả vi.
    3. = 4 . 3/5 + 13 . 4/5 = 12/5 + 52/5 = 64/5.
- `gt_t9_gr_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tại điểm (1, 1), hàm f(x, y) = x^2 + 2y^2 tăng nhanh nhất theo hướng nào, và tốc độ tăng lớn nhất là bao nhiêu?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
    - **(đúng)** Theo hướng (1, 2), tốc độ 2 sqrt(5)
    - Theo hướng (1, 1), tốc độ 2 sqrt(5)
    - Theo hướng (1, 2), tốc độ 6
    - Theo hướng (2, 1), tốc độ sqrt(5)
  - **Đáp án:** Theo hướng (1, 2), tốc độ 2 sqrt(5)
    1. grad f = (2x, 4y) = (2, 4) tại (1, 1), cùng hướng với (1, 2).
    2. Đạo hàm theo hướng u = |grad f| . cos(góc giữa grad f và u), lớn nhất khi u cùng hướng grad f.
    3. Tốc độ lớn nhất là |grad f| = sqrt(4 + 16) = 2 sqrt(5). (6 là tổng 2 + 4, không phải độ dài.)
- `gt_t9_gr_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho phép biến đổi (u, v) = (x^2 - y^2, 2xy). Tính định thức của ma trận Jacobian [u_x, u_y; v_x, v_y] tại (1, 2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_05`, `gt_t7_cb_04`
  - **Đáp án:** 20
    1. u_x = 2x, u_y = -2y, v_x = 2y, v_y = 2x.
    2. Tại (1, 2): ma trận Jacobian [2, -4; 4, 2].
    3. Định thức: 2 . 2 - (-4) . 4 = 4 + 16 = 20 (tổng quát là 4(x^2 + y^2)).
- `gt_t9_gr_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một nơ-ron nhỏ: z = w1 x1 + w2 x2 + b, a = max(0, z) (ReLU), hàm mất mát L = (a - t)^2. Với x1 = 1, x2 = 2, w1 = 3, w2 = -1, b = 1, t = 5: lan truyền xuôi rồi lan truyền ngược. Nhập L, dL/dw1, dL/dw2, dL/db theo đúng thứ tự.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Đáp án:** 9, -6, -12, -6
    1. Xuôi: z = 3 . 1 + (-1) . 2 + 1 = 2, a = max(0, 2) = 2, L = (2 - 5)^2 = 9.
    2. Ngược: dL/da = 2(a - t) = -6. Vì z = 2 > 0, da/dz = 1, nên dL/dz = -6.
    3. dz/dw1 = x1 = 1, dz/dw2 = x2 = 2, dz/db = 1.
    4. Quy tắc dây chuyền: dL/dw1 = -6, dL/dw2 = -12, dL/db = -6.
- `gt_t9_gr_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Thiên kiếp: đồ thị tính toán u = x . y, v = u + z, f = v^2 với x = 1, y = 2, z = -4.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Phần a** (Điền số): a) Lan truyền xuôi: tính f.
    - **Đáp án a:** 4
  - **Phần b** (Điền số): b) Tính df/dv tại các giá trị đó.
    - **Đáp án b:** -4
  - **Phần c** (Điền số): c) Lan truyền ngược: nhập df/dx, df/dy, df/dz theo đúng thứ tự.
    - **Đáp án c:** -8, -4, -4
  - **Lời giải:**
    1. a) u = 1 . 2 = 2, v = 2 + (-4) = -2, f = (-2)^2 = 4.
    2. b) df/dv = 2v = -4.
    3. c) dv/du = 1, dv/dz = 1, du/dx = y = 2, du/dy = x = 1. Nhân dọc đường đi: df/dx = -4 . 1 . 2 = -8, df/dy = -4 . 1 . 1 = -4, df/dz = -4 . 1 = -4. Kiểm tra: f = (xy + z)^2 có f_x = 2(xy + z)y = -8.
- `gt_t9_gr_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm bước đầu tiên bị sai trong lời giải sau. Đề bài: đồ thị tính toán a = x . y, f = a + x^2 với x = 3, y = 2; tính df/dx và df/dy bằng lan truyền ngược.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Lời giải đưa ra (có một bước sai):**
    1. Lan truyền xuôi: a = 3 . 2 = 6, f = 6 + 9 = 15.
    2. df/da = 1 và da/dx = y = 2.
    3. x chỉ đi vào f qua nút a, nên df/dx = df/da . da/dx = 2.   **<- bước sai đầu tiên**
    4. df/dy = df/da . da/dy = 1 . x = 3.
  - **Đáp án:** Bước 3: x chỉ đi vào f qua nút a, nên df/dx = df/da . da/dx = 2.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 sai: x đi vào f theo hai đường, qua a và trực tiếp qua số hạng x^2.
    2. Lan truyền ngược phải cộng đóng góp của mọi đường: df/dx = 1 . y + 2x = 2 + 6 = 8.
    3. Kiểm tra: f = xy + x^2 có f_x = y + 2x = 8 tại (3, 2). df/dy = 3 thì đúng.
- `gt_t9_gr_07` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với f(x, y) = x^2 + y^2, đạo hàm của f tại (3, 4) theo hướng vector đơn vị u = (4/5, -3/5) bằng 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Đáp án:** Đúng
    1. grad f = (2x, 2y) = (6, 8) tại (3, 4).
    2. Đạo hàm theo hướng: 6 . 4/5 + 8 . (-3/5) = 24/5 - 24/5 = 0.
    3. Hướng u vuông góc với grad f, tức tiếp xúc với đường mức x^2 + y^2 = 25 tại (3, 4): f không đổi theo hướng đó. Mệnh đề đúng.
- `gt_t9_gr_08` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho z = u^2 v với u = x + y, v = xy. Dùng quy tắc dây chuyền (ma trận Jacobian của (u, v) theo (x, y)), tính z_x tại (x, y) = (1, 2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t4_dc_05`, `gt_t4_dc_09`, `gt_t7_cb_04`
  - **Đáp án:** 30
    1. Tại (1, 2): u = 3, v = 2. z_u = 2uv = 12, z_v = u^2 = 9.
    2. u_x = 1, v_x = y = 2.
    3. z_x = z_u . u_x + z_v . v_x = 12 . 1 + 9 . 2 = 30.
    4. Kiểm tra: z = (x + y)^2 xy; z_x = 2(x + y)xy + (x + y)^2 y = 12 + 18 = 30.
- `gt_g9_dao_ham_huong` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = -2x^2 + xy + 3y^2 + 3x. Tính đạo hàm của f tại (-2, 0) theo hướng vector đơn vị u = (3/5, 4/5).
  - **Đáp án:** 5
    1. grad f = (f_x, f_y) = (-4x + y + 3, x + 6y).
    2. Tại (-2, 0): grad f = (11, -2).
    3. Đạo hàm theo hướng = grad f . u = 11 . (3/5) + (-2) . (4/5) = 5.
  - **Câu hỏi:** Cho f(x, y) = 3x^2 + 3xy - 3y^2 - 3x. Tính đạo hàm của f tại (-2, 0) theo hướng vector đơn vị u = (-4/5, -3/5).
  - **Đáp án:** 78/5
    1. grad f = (f_x, f_y) = (6x + 3y - 3, 3x - 6y).
    2. Tại (-2, 0): grad f = (-15, -6).
    3. Đạo hàm theo hướng = grad f . u = (-15) . (-4/5) + (-6) . (-3/5) = 78/5.
  - **Câu hỏi:** Cho f(x, y) = -2x^2 + xy + y^2 - 2x. Tính đạo hàm của f tại (0, 2) theo hướng vector đơn vị u = (5/13, 12/13).
  - **Đáp án:** 48/13
    1. grad f = (f_x, f_y) = (-4x + y - 2, x + 2y).
    2. Tại (0, 2): grad f = (0, 4).
    3. Đạo hàm theo hướng = grad f . u = 0 . (5/13) + 4 . (12/13) = 48/13.
- `gt_g9_lan_truyen` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Mô hình z = w . x + b với hàm mất mát L = (z - t)^2. Cho w = -2, b = 1, x = -3, t = -1. Lan truyền xuôi rồi ngược: nhập L, dL/dw, dL/db theo đúng thứ tự.
  - **Đáp án:** 64, -48, 16
    1. Xuôi: z = -2 . (-3) + 1 = 7, L = (7 - (-1))^2 = 64.
    2. Ngược: dL/dz = 2(z - t) = 16; dz/dw = x = -3, dz/db = 1.
    3. Dây chuyền: dL/dw = 16 . (-3) = -48, dL/db = 16.
  - **Câu hỏi:** Mô hình z = w . x + b với hàm mất mát L = (z - t)^2. Cho w = -3, b = -3, x = -3, t = 0. Lan truyền xuôi rồi ngược: nhập L, dL/dw, dL/db theo đúng thứ tự.
  - **Đáp án:** 36, -36, 12
    1. Xuôi: z = -3 . (-3) + (-3) = 6, L = (6 - 0)^2 = 36.
    2. Ngược: dL/dz = 2(z - t) = 12; dz/dw = x = -3, dz/db = 1.
    3. Dây chuyền: dL/dw = 12 . (-3) = -36, dL/db = 12.
  - **Câu hỏi:** Mô hình z = w . x + b với hàm mất mát L = (z - t)^2. Cho w = -1, b = 1, x = 1, t = 5. Lan truyền xuôi rồi ngược: nhập L, dL/dw, dL/db theo đúng thứ tự.
  - **Đáp án:** 25, -10, -10
    1. Xuôi: z = -1 . 1 + 1 = 0, L = (0 - 5)^2 = 25.
    2. Ngược: dL/dz = 2(z - t) = -10; dz/dw = x = 1, dz/db = 1.
    3. Dây chuyền: dL/dw = -10 . 1 = -10, dL/db = -10.

## Tầng 10: Tài Năng: số thực, khả tích, hàm lồi và không gian metric

60 dạng câu (53 câu viết tay, 7 bộ sinh câu); 60 chưa duyệt.

### Tiên đề của tập số thực (`gt_t10_tien_de_so_thuc`)

- `gt_t10_ts_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập A = {1 - 1/n : n = 1, 2, 3, ...} (các số 0, 1/2, 2/3, 3/4, ...). Tìm cận trên đúng sup A. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_03`, `gt_t6_gl_05`
  - **Đáp án:** 1
    1. Mọi số hạng 1 - 1/n đều nhỏ hơn 1, nên 1 là một cận trên.
    2. Cận trên nhỏ hơn 1 không có: với 1 - e (e > 0) luôn có n đủ lớn để 1 - 1/n > 1 - e. Vậy sup A = 1, dù 1 không thuộc A.
- `gt_t10_ts_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập B = {3 + 2/n : n = 1, 2, 3, ...}. Tìm cận dưới đúng inf B. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_03`, `gt_t6_gl_05`
  - **Đáp án:** 3
    1. Mọi số hạng 3 + 2/n đều lớn hơn 3, nên 3 là một cận dưới.
    2. Với e > 0 luôn có n để 2/n < e, tức 3 + 2/n < 3 + e: không có cận dưới nào lớn hơn 3. Vậy inf B = 3, không đạt được (3 không thuộc B).
- `gt_t10_ts_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập C = {(-1)^n + 1/n : n = 1, 2, 3, ...}. Tìm sup C. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_03`, `gt_t6_gl_05`
  - **Đáp án:** 3/2
    1. Với n lẻ số hạng là -1 + 1/n <= 0. Với n chẵn là 1 + 1/n, giảm dần khi n tăng: 3/2 (n = 2), 5/4 (n = 4), ...
    2. Số lớn nhất là 3/2 tại n = 2 và mọi số hạng khác đều nhỏ hơn, nên sup C = max C = 3/2 (đạt được). (Còn inf C = -1 không đạt được.)
- `gt_t10_ts_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi tập con khác rỗng của tập các số hữu tỉ Q mà bị chặn trên (bởi một số hữu tỉ) đều có cận trên đúng là một số hữu tỉ.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Đáp án:** Sai
    1. Phản ví dụ: A = {x thuộc Q : x^2 < 2} khác rỗng và bị chặn trên bởi 2, nhưng cận trên đúng của nó là sqrt(2), không phải số hữu tỉ.
    2. Tính chất "mọi tập khác rỗng bị chặn trên đều có sup" (tiên đề cận trên đúng) là điều làm R khác Q. Mệnh đề sai.
- `gt_t10_ts_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu A là tập khác rỗng, bị chặn trên của R thì sup A luôn thuộc A.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Đáp án:** Sai
    1. Phản ví dụ: A = (0, 1). sup A = 1 nhưng 1 không thuộc A (A không có phần tử lớn nhất).
    2. sup A thuộc A chỉ khi A có phần tử lớn nhất; khi đó sup A = max A. Mệnh đề sai.
- `gt_t10_ts_06` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = (-2, 3) = {x : -2 < x < 3}. Khẳng định đúng là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_03`, `gt_t6_gl_05`
    - **(đúng)** sup A = 3 và 3 không thuộc A, nên A không có phần tử lớn nhất
    - A không có sup vì A không có phần tử lớn nhất
    - sup A = 2.999... là một số nhỏ hơn 3
    - sup A = 3 và 3 thuộc A
  - **Đáp án:** sup A = 3 và 3 không thuộc A, nên A không có phần tử lớn nhất
    1. 3 là một cận trên của A (mọi x < 3), và mọi số nhỏ hơn 3 không còn là cận trên, nên sup A = 3; 3 không thuộc A vì A là khoảng mở, nên không có max.
    2. Có sup mà không có max là chuyện bình thường: tiên đề cận trên đúng chỉ đòi tập khác rỗng, bị chặn trên, không đòi có phần tử lớn nhất.
    3. Không có "số lớn nhất nhỏ hơn 3": giữa mọi số a < 3 và 3 còn có (a + 3)/2. 2.999... chính là 3.
    4. 3 không thuộc A vì A chỉ gồm các x < 3 ngặt.
- `gt_t10_ts_07` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chứng minh tập A = {1 - 1/n : n = 1, 2, ...} có cận trên đúng bằng 1, và nói 1 có thuộc A không. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Lời giải đưa ra (có một bước sai):**
    1. Mọi phần tử 1 - 1/n đều nhỏ hơn 1 nên 1 là cận trên của A.
    2. Với mọi e > 0 có n với 1/n < e (tính Archimedes), khi đó 1 - 1/n > 1 - e nên 1 - e không phải cận trên.
    3. Vậy 1 là cận trên nhỏ nhất, sup A = 1.
    4. Do đó 1 thuộc A và là giá trị lớn nhất của A.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Do đó 1 thuộc A và là giá trị lớn nhất của A.
  - **Vì sao sai, và bước đúng:**
    1. Ba dòng đầu đúng. Dòng cuối suy từ sup sang max, nhưng 1 - 1/n < 1 với mọi n (dòng 1), nên 1 không thuộc A.
    2. Đúng: sup A = 1 không đạt được; A không có phần tử lớn nhất.
- `gt_t10_ts_08` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi tập với cận trên đúng và cận dưới đúng của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Đáp án (ghép đúng):**
    - A = (0, 1) — sup = 1 và inf = 0, cả hai không thuộc A
    - A = {1/n : n = 1, 2, ...} — sup = 1 thuộc A (là max), inf = 0 không thuộc A
    - A = [2, 5) — sup = 5 không thuộc A, inf = 2 thuộc A (là min)
    - A = {x : x^2 <= 9} — sup = 3 và inf = -3, cả hai thuộc A
  - **Lời giải:**
    1. Khoảng mở mất cả hai đầu mút; [2, 5) giữ đầu trái; x^2 <= 9 cho đoạn [-3, 3] đóng.
    2. {1/n}: 1/n giảm về 0 nhưng không bao giờ bằng 0, còn giá trị lớn nhất 1 đạt tại n = 1.
- `gt_t10_ts_09` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh sup A = 1 cho A = {n/(n + 1) : n = 1, 2, ...}, rồi kết luận 1 không thuộc A.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Đáp án (thứ tự đúng):**
    1. Viết n/(n + 1) = 1 - 1/(n + 1) < 1 với mọi n, nên 1 là một cận trên của A.
    2. Cho e > 0 bất kỳ. Theo tính Archimedes chọn n sao cho 1/(n + 1) < e.
    3. Với n đó n/(n + 1) = 1 - 1/(n + 1) > 1 - e, nên 1 - e không là cận trên của A.
    4. Vậy 1 là cận trên nhỏ nhất: sup A = 1.
    5. Vì n/(n + 1) < 1 với mọi n, số 1 không thuộc A: sup A không đạt được.
  - **Lời giải:**
    1. Một chứng minh sup gồm hai nửa: là cận trên, và không có cận trên nhỏ hơn (bước tìm n cho mỗi e).
    2. Điều cuối (1 không thuộc A) dùng lại bất đẳng thức n/(n + 1) < 1 của bước đầu.
- `gt_t10_ts_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét A = {n/(n + 1) : n = 1, 2, 3, ...} (các số 1/2, 2/3, 3/4, ...).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Phần a** (Điền số): a) Tìm sup A.
    - **Đáp án a:** 1
  - **Phần b** (Đúng/Sai): b) sup A thuộc A.
    - **Đáp án b:** Sai
  - **Phần c** (Điền số): c) Tìm inf A.
    - **Đáp án c:** 1/2
  - **Phần d** (Đúng/Sai): d) inf A thuộc A.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) n/(n + 1) = 1 - 1/(n + 1) tăng dần và tiến tới 1 từ dưới: sup A = 1.
    2. b) Mọi phần tử đều nhỏ hơn 1 ngặt nên 1 không thuộc A.
    3. c) Dãy tăng nên số hạng nhỏ nhất là số hạng đầu n = 1: 1/2. Vậy inf A = 1/2.
    4. d) 1/2 là số hạng đầu, thuộc A: inf A = min A.
- `gt_t10_ts_11` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét A = {x thuộc Q : x^2 < 2} (các số hữu tỉ có bình phương nhỏ hơn 2) như một tập con của R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_04`, `gt_t6_gl_05`
  - **Phần a** (Đúng/Sai): a) A bị chặn trên.
    - **Đáp án a:** Đúng
  - **Phần b** (Điền số): b) Số nguyên dương nhỏ nhất là cận trên của A là bao nhiêu?
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) Cận trên đúng của A trong tập Q (chỉ xét các cận trên hữu tỉ) tồn tại.
    - **Đáp án c:** Sai
  - **Phần d** (Đúng/Sai): d) Cận trên đúng của A trong R tồn tại.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Mọi x thuộc A có x^2 < 2 < 4 nên x < 2: 2 là cận trên.
    2. b) 1 không là cận trên vì 7/5 thuộc A (49/25 < 2) mà 7/5 > 1; 2 là cận trên. Vậy số nguyên dương nhỏ nhất là 2.
    3. c) Trong Q không có cận trên nhỏ nhất: cận trên hữu tỉ nào cũng lớn hơn sqrt(2) ngặt, và luôn có số hữu tỉ khác nhỏ hơn nó mà vẫn lớn hơn sqrt(2).
    4. d) Trong R tiên đề cận trên đúng cho sup A = sqrt(2).
- `gt_g10_sup_inf` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tập A = {1 - 5/n : n = 1, 2, 3, ...}. Tìm cận trên đúng sup A. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 1
    1. Dãy 1 - 5/n tăng dần theo n: số hạng đầu (n = 1) là -4, và giới hạn khi n lớn là 1 (không bao giờ đạt được vì 5/n khác 0).
    2. sup A = 1 (giá trị này không thuộc tập, nhưng vẫn là cận đúng).
  - **Câu hỏi:** Tập A = {-2 - 1/n : n = 1, 2, 3, ...}. Tìm cận trên đúng sup A. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -2
    1. Dãy -2 - 1/n tăng dần theo n: số hạng đầu (n = 1) là -3, và giới hạn khi n lớn là -2 (không bao giờ đạt được vì 1/n khác 0).
    2. sup A = -2 (giá trị này không thuộc tập, nhưng vẫn là cận đúng).
  - **Câu hỏi:** Tập A = {2 + 4/n : n = 1, 2, 3, ...}. Tìm cận trên đúng sup A. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 6
    1. Dãy 2 + 4/n giảm dần theo n: số hạng đầu (n = 1) là 6, và giới hạn khi n lớn là 2 (không bao giờ đạt được vì 4/n khác 0).
    2. sup A = 6 (giá trị này thuộc tập (là max)).

### Giới hạn trên và giới hạn dưới (`gt_t10_gioi_han_tren_duoi`)

- `gt_t10_gh_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = (-1)^n (1 + 1/n), n = 1, 2, 3, ... Tìm giới hạn trên limsup a_n, tức giới hạn lớn nhất của các dãy con hội tụ. Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_tc_05`, `gt_t3_mp_05`
  - **Đáp án:** 1
    1. Dãy con chỉ số chẵn: a_(2k) = 1 + 1/(2k) tiến tới 1. Dãy con chỉ số lẻ: a_(2k+1) = -(1 + 1/(2k+1)) tiến tới -1.
    2. Mọi dãy con hội tụ của (a_n) có giới hạn 1 hoặc -1, nên limsup = max = 1 (còn liminf = -1). Dãy không hội tụ vì hai giới hạn này khác nhau.
- `gt_t10_gh_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = cos(2 n pi/3), n = 1, 2, 3, ... (các số -1/2, -1/2, 1, -1/2, -1/2, 1, ...). Tìm giới hạn dưới liminf a_n. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_tc_05`, `gt_t3_mp_05`
  - **Đáp án:** -1/2
    1. Dãy lặp chu kỳ 3 với các giá trị cos(2 pi/3) = -1/2, cos(4 pi/3) = -1/2, cos(2 pi) = 1.
    2. Các dãy con hội tụ chỉ có thể có giới hạn -1/2 hoặc 1, nên liminf = -1/2 và limsup = 1.
- `gt_t10_gh_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy (a_n) bị chặn. Khi đó limsup a_n = liminf a_n khi và chỉ khi (a_n) hội tụ.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_ld_05`
  - **Đáp án:** Đúng
    1. Nếu a_n tiến tới L thì mọi dãy con đều tiến tới L, nên limsup = liminf = L.
    2. Ngược lại, limsup = liminf = L với dãy bị chặn nghĩa là mọi dãy con hội tụ đều có giới hạn L, và mọi số hạng, trừ hữu hạn, nằm gần L: dãy hội tụ về L. Mệnh đề đúng.
- `gt_t10_gh_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai dãy bị chặn (a_n), (b_n): limsup (a_n + b_n) = limsup a_n + limsup b_n.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_ld_05`
  - **Đáp án:** Sai
    1. Phản ví dụ: a_n = (-1)^n và b_n = -(-1)^n = (-1)^(n+1). Khi đó a_n + b_n = 0 nên limsup (a_n + b_n) = 0, còn limsup a_n + limsup b_n = 1 + 1 = 2.
    2. Chỉ có bất đẳng thức limsup (a_n + b_n) <= limsup a_n + limsup b_n. Dấu bằng xảy ra khi một trong hai dãy hội tụ. Mệnh đề sai.
- `gt_t10_gh_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = (-1)^n + 1/n (n = 1, 2, ...). Cặp (limsup a_n, liminf a_n) là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
    - **(đúng)** (1, -1)
    - (3/2, -1)
    - (0, 0)
    - (1, 1)
  - **Đáp án:** (1, -1)
    1. Dãy con chẵn 1 + 1/(2k) tiến tới 1, dãy con lẻ -1 + 1/(2k+1) tiến tới -1: limsup = 1 và liminf = -1.
    2. (3/2, -1): lấy 3/2 là sup của tập các số hạng (đạt tại n = 2) thay vì giới hạn lớn nhất của dãy con; limsup chỉ quan tâm các số hạng ở rất xa.
    3. (0, 0): nhầm với giới hạn của 1/n, bỏ phần (-1)^n không hội tụ.
    4. (1, 1): nghĩ rằng giới hạn trên bằng giới hạn dưới; chúng bằng nhau chỉ khi dãy hội tụ.
- `gt_t10_gh_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tìm limsup và liminf của a_n = (-1)^n n/(n + 1). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
  - **Lời giải đưa ra (có một bước sai):**
    1. Dãy con chẵn: a_(2k) = 2k/(2k + 1) tiến tới 1.
    2. Dãy con lẻ: a_(2k+1) = -(2k + 1)/(2k + 2) tiến tới -1.
    3. Hai dãy con có giới hạn khác nhau, nên dãy không có limsup và liminf.   **<- bước sai đầu tiên**
    4. Kết luận: (a_n) phân kỳ.
  - **Đáp án:** Bước 3: Hai dãy con có giới hạn khác nhau, nên dãy không có limsup và liminf.
  - **Vì sao sai, và bước đúng:**
    1. Một dãy bị chặn luôn có limsup và liminf (là giới hạn lớn nhất và nhỏ nhất của các dãy con hội tụ). Hai giới hạn khác nhau không làm mất chúng, mà cho limsup = 1 và liminf = -1.
    2. Dòng cuối đúng, nhưng vì lý do khác: limsup khác liminf nên dãy phân kỳ.
- `gt_t10_gh_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dãy với cặp (limsup, liminf) của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
  - **Đáp án (ghép đúng):**
    - a_n = (-1)^n — limsup = 1, liminf = -1
    - a_n = 2 + 1/n — limsup = liminf = 2
    - a_n = 3 + 2 (-1)^n — limsup = 5, liminf = 1
    - a_n = n modulo 3, tức 1, 2, 0, 1, 2, 0, ... — limsup = 2, liminf = 0
  - **Lời giải:**
    1. (-1)^n nhận hai giá trị 1, -1 vô hạn lần. 3 + 2 (-1)^n nhận 5 (n chẵn) và 1 (n lẻ).
    2. 2 + 1/n hội tụ về 2 nên limsup = liminf = 2.
    3. n modulo 3 lặp ba giá trị 1, 2, 0: giá trị lớn nhất 2, nhỏ nhất 0, đều xuất hiện vô hạn lần.
- `gt_t10_gh_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = (2 + (-1)^n)(1 + 1/n). Sắp xếp các bước tìm limsup và liminf.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
  - **Đáp án (thứ tự đúng):**
    1. Tách n chẵn và n lẻ: 2 + (-1)^n bằng 3 khi n chẵn, bằng 1 khi n lẻ.
    2. Dãy con chẵn: a_n = 3 (1 + 1/n) tiến tới 3.
    3. Dãy con lẻ: a_n = 1 . (1 + 1/n) tiến tới 1.
    4. Mọi số hạng thuộc một trong hai dãy con này, nên mọi dãy con hội tụ của (a_n) có giới hạn 1 hoặc 3.
    5. limsup a_n = lớn nhất = 3 và liminf a_n = nhỏ nhất = 1.
  - **Lời giải:**
    1. Tách dãy thành các dãy con có giới hạn, chứng tỏ không còn giới hạn nào khác, rồi lấy lớn nhất và nhỏ nhất.
    2. Bước 4 quan trọng: nếu bỏ sót một dãy con thì có thể bỏ sót một giới hạn.
- `gt_t10_gh_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = (-1)^n (1 + 1/n), n = 1, 2, 3, ...
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
  - **Phần a** (Điền số): a) Giới hạn của dãy con chỉ số chẵn a_(2k).
    - **Đáp án a:** 1
  - **Phần b** (Điền số): b) Giới hạn của dãy con chỉ số lẻ a_(2k+1).
    - **Đáp án b:** -1
  - **Phần c** (Điền số): c) limsup a_n.
    - **Đáp án c:** 1
  - **Phần d** (Đúng/Sai): d) Dãy (a_n) hội tụ.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) a_(2k) = 1 + 1/(2k) tiến tới 1.
    2. b) a_(2k+1) = -(1 + 1/(2k+1)) tiến tới -1.
    3. c) Chỉ có hai giới hạn dãy con (1 và -1), nên limsup = 1 (và liminf = -1).
    4. d) limsup = 1 khác liminf = -1, nên dãy không hội tụ.
- `gt_t10_gh_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = sin(n pi/2), n = 1, 2, 3, ... (các số 1, 0, -1, 0, 1, 0, -1, 0, ...).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_dd_07`, `gt_t3_mp_05`
  - **Phần a** (Đúng/Sai): a) Dãy (a_n) hội tụ.
    - **Đáp án a:** Sai
  - **Phần b** (Điền số): b) limsup a_n.
    - **Đáp án b:** 1
  - **Phần c** (Điền số): c) liminf a_n.
    - **Đáp án c:** -1
  - **Phần d** (Đúng/Sai): d) Với mọi dãy bị chặn, liminf <= limsup.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Dãy lặp 1, 0, -1, 0 nên có các dãy con hằng 1, 0, -1: không hội tụ.
    2. b) Các giới hạn dãy con là 1, 0, -1: lớn nhất là 1.
    3. c) Nhỏ nhất là -1.
    4. d) liminf là giới hạn nhỏ nhất và limsup là lớn nhất của cùng một tập các giới hạn dãy con (khác rỗng với dãy bị chặn), nên liminf <= limsup.
- `gt_g10_gioi_han_tren` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dãy a_n = 1 - 4(-1)^n (1 + 1/n), n = 1, 2, 3, ... Tìm giới hạn trên limsup của a_n, tức giới hạn lớn nhất của các dãy con hội tụ. Nhập một số.
  - **Đáp án:** 5
    1. Dãy con chỉ số chẵn: a_(2k) = 1 + (-4)(1 + 1/(2k)) tiến tới -3. Dãy con chỉ số lẻ: a_(2k+1) = 1 - (-4)(1 + 1/(2k+1)) tiến tới 5.
    2. Chỉ có hai giới hạn dãy con: -3 và 5; lớn nhất là 5, nhỏ nhất là -3.
    3. limsup a_n = 5.
  - **Câu hỏi:** Dãy a_n = -2 + (-1)^n (1 + 1/n), n = 1, 2, 3, ... Tìm giới hạn trên limsup của a_n, tức giới hạn lớn nhất của các dãy con hội tụ. Nhập một số.
  - **Đáp án:** -1
    1. Dãy con chỉ số chẵn: a_(2k) = -2 + (1)(1 + 1/(2k)) tiến tới -1. Dãy con chỉ số lẻ: a_(2k+1) = -2 - (1)(1 + 1/(2k+1)) tiến tới -3.
    2. Chỉ có hai giới hạn dãy con: -1 và -3; lớn nhất là -1, nhỏ nhất là -3.
    3. limsup a_n = -1.
  - **Câu hỏi:** Dãy a_n = 2 + 5(-1)^n (1 + 1/n), n = 1, 2, 3, ... Tìm giới hạn trên limsup của a_n, tức giới hạn lớn nhất của các dãy con hội tụ. Nhập một số.
  - **Đáp án:** 7
    1. Dãy con chỉ số chẵn: a_(2k) = 2 + (5)(1 + 1/(2k)) tiến tới 7. Dãy con chỉ số lẻ: a_(2k+1) = 2 - (5)(1 + 1/(2k+1)) tiến tới -3.
    2. Chỉ có hai giới hạn dãy con: 7 và -3; lớn nhất là 7, nhỏ nhất là -3.
    3. limsup a_n = 7.

### Điều kiện khả tích Riemann (`gt_t10_kha_tich_riemann`)

- `gt_t10_kt_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^2 trên [0, 2], phân hoạch P = {0, 1, 2}. Tính tổng Darboux trên U(f, P) = tổng của (sup f trên đoạn con) x (độ dài đoạn con). Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_g7_tri_tuyet_doi`
  - **Đáp án:** 5
    1. f tăng trên [0, 2] nên sup trên mỗi đoạn con lấy ở mút phải: trên [0, 1] là f(1) = 1, trên [1, 2] là f(2) = 4.
    2. U(f, P) = 1 . 1 + 4 . 1 = 5. (Tổng Darboux dưới L(f, P) = 0 . 1 + 1 . 1 = 1; tích phân 8/3 nằm giữa 1 và 5.)
- `gt_t10_kt_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^2 trên [0, 2], phân hoạch P gồm 4 đoạn con bằng nhau. Tính U(f, P) - L(f, P). Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_g7_tri_tuyet_doi`
  - **Đáp án:** 2
    1. f tăng nên trên đoạn [x_(k-1), x_k] sup = f(x_k) và inf = f(x_(k-1)): U - L = tổng (f(x_k) - f(x_(k-1))) . h với h = 1/2.
    2. Tổng thu gọn (các số hạng triệt tiêu từng cặp): U - L = h (f(2) - f(0)) = 1/2 . 4 = 2. Giảm h thì U - L giảm: đó là cơ chế chứng minh khả tích.
- `gt_t10_kt_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm Dirichlet D trên [0, 1] (D(x) = 1 nếu x hữu tỉ, D(x) = 0 nếu x vô tỉ) khả tích Riemann.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
  - **Đáp án:** Sai
    1. Mọi đoạn con, dù nhỏ đến đâu, đều chứa cả số hữu tỉ và số vô tỉ: sup = 1 và inf = 0 trên mỗi đoạn con.
    2. Vậy U(D, P) = 1 và L(D, P) = 0 với mọi phân hoạch P, hiệu U - L = 1 không bao giờ nhỏ hơn mọi e > 0. Mệnh đề sai.
- `gt_t10_kt_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi hàm bị chặn trên [a, b] và chỉ gián đoạn tại hữu hạn điểm đều khả tích Riemann trên [a, b].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
  - **Đáp án:** Đúng
    1. Chỉ cần bao các điểm gián đoạn bằng các đoạn con rất ngắn (tổng độ dài < e): phần đóng góp vào U - L không quá (sup - inf) . e vì f bị chặn.
    2. Trên phần còn lại f liên tục từng khúc nên U - L cũng nhỏ. Mệnh đề đúng.
- `gt_t10_kt_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f bị chặn trên [a, b] khả tích Riemann khi và chỉ khi
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
    - **(đúng)** với mọi e > 0 có phân hoạch P để U(f, P) - L(f, P) < e
    - f liên tục trên [a, b]
    - f chỉ cần bị chặn trên [a, b]
    - f có đạo hàm tại mọi điểm của [a, b]
  - **Đáp án:** với mọi e > 0 có phân hoạch P để U(f, P) - L(f, P) < e
    1. Đó là tiêu chuẩn Darboux (Riemann): tổng trên và tổng dưới có thể kéo sát nhau tuỳ ý.
    2. Liên tục chỉ là điều kiện đủ, không cần: hàm bậc thang (gián đoạn ở vài điểm) vẫn khả tích.
    3. Bị chặn chỉ là điều kiện cần: hàm Dirichlet bị chặn nhưng không khả tích.
    4. Có đạo hàm là điều kiện đủ (kéo theo liên tục) nhưng không cần, vì |x| không có đạo hàm tại 0 mà vẫn khả tích.
- `gt_t10_kt_06` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Với f(x) = x trên [0, 1] chia thành n đoạn bằng nhau, tính U_n - L_n để chứng tỏ f khả tích. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_g7_tri_tuyet_doi`
  - **Lời giải đưa ra (có một bước sai):**
    1. Trên đoạn thứ k, hàm x tăng nên sup lấy ở mút phải k/n và inf ở mút trái (k - 1)/n.
    2. U_n = tổng k/n . 1/n = (1/n^2)(1 + 2 + ... + n) = (1/n^2) . n^2/2 = 1/2.   **<- bước sai đầu tiên**
    3. L_n = (1/n^2)(0 + 1 + ... + (n - 1)) = (n - 1)/(2n).
    4. U_n - L_n = 1/2 - (n - 1)/(2n) = 1/(2n), tiến tới 0 nên f khả tích.
  - **Đáp án:** Bước 2: U_n = tổng k/n . 1/n = (1/n^2)(1 + 2 + ... + n) = (1/n^2) . n^2/2 = 1/2.
  - **Vì sao sai, và bước đúng:**
    1. 1 + 2 + ... + n = n(n + 1)/2, không phải n^2/2. Do đó U_n = (n + 1)/(2n).
    2. Đúng: U_n - L_n = (n + 1)/(2n) - (n - 1)/(2n) = 1/n, tiến tới 0 nên f khả tích, và cả U_n, L_n đều tiến tới 1/2 = tích phân.
- `gt_t10_kt_07` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm trên [0, 1] với kết luận về tính khả tích Riemann của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
  - **Đáp án (ghép đúng):**
    - f(x) = x^2 — Khả tích vì liên tục
    - f(x) = 1 nếu x <= 1/2 và f(x) = 0 nếu x > 1/2 — Khả tích dù gián đoạn tại 1/2 (hữu hạn điểm gián đoạn, bị chặn)
    - f(x) = 1/x với x > 0 và f(0) = 0 — Không khả tích vì không bị chặn
    - Hàm Dirichlet — Không khả tích: U = 1 và L = 0 với mọi phân hoạch
  - **Lời giải:**
    1. Liên tục trên đoạn đóng thì khả tích; hàm bậc thang khả tích; hàm không bị chặn thì không khả tích Riemann.
    2. Hàm Dirichlet bị chặn nhưng gián đoạn ở mọi điểm.
- `gt_t10_kt_08` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^2 trên [0, 2], phân hoạch P = {0, 1, 2}. Sắp xếp các bước tính U(f, P) và L(f, P).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_g7_tri_tuyet_doi`
  - **Đáp án (thứ tự đúng):**
    1. P chia [0, 2] thành hai đoạn dài 1: [0, 1] và [1, 2].
    2. f(x) = x^2 tăng trên [0, 2], nên trên mỗi đoạn sup ở mút phải và inf ở mút trái.
    3. Trên [0, 1]: sup = 1, inf = 0. Trên [1, 2]: sup = 4, inf = 1.
    4. U(f, P) = 1 . 1 + 4 . 1 = 5 và L(f, P) = 0 . 1 + 1 . 1 = 1.
    5. Kiểm tra: L(f, P) = 1 <= tích phân = 8/3 <= U(f, P) = 5.
  - **Lời giải:**
    1. Chọn phân hoạch, xác định sup và inf từng đoạn, rồi nhân với độ dài và cộng lại.
    2. Bước kiểm tra cuối: tích phân luôn nằm giữa tổng dưới và tổng trên của mọi phân hoạch.
- `gt_t10_kt_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = 3x + 1 trên [0, 2], phân hoạch P = {0, 1, 2}.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_01`, `gt_g7_tri_tuyet_doi`
  - **Phần a** (Điền số): a) Tính tổng Darboux trên U(f, P).
    - **Đáp án a:** 11
  - **Phần b** (Điền số): b) Tính tổng Darboux dưới L(f, P).
    - **Đáp án b:** 5
  - **Phần c** (Đúng/Sai): c) Tích phân của f trên [0, 2] (bằng 8) nằm giữa L(f, P) và U(f, P).
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Tính U(f, P) - L(f, P).
    - **Đáp án d:** 6
  - **Lời giải:**
    1. a) f tăng: sup trên [0, 1] là f(1) = 4, trên [1, 2] là f(2) = 7: U = 4 + 7 = 11.
    2. b) inf trên [0, 1] là f(0) = 1, trên [1, 2] là f(1) = 4: L = 1 + 4 = 5.
    3. c) Tích phân của 3x + 1 trên [0, 2] là 3 . 2 + 2 = 8, và 5 <= 8 <= 11.
    4. d) U - L = 11 - 5 = 6 = h (f(2) - f(0)) = 1 . 6.
- `gt_t10_kt_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm Dirichlet D trên [0, 1] (D = 1 trên các số hữu tỉ, D = 0 trên các số vô tỉ) và một phân hoạch P bất kỳ của [0, 1].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
  - **Phần a** (Điền số): a) Tính U(D, P).
    - **Đáp án a:** 1
  - **Phần b** (Điền số): b) Tính L(D, P).
    - **Đáp án b:** 0
  - **Phần c** (Đúng/Sai): c) D khả tích Riemann trên [0, 1].
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Giá trị nhỏ nhất của U(D, P) - L(D, P) trên mọi phân hoạch P là bao nhiêu?
    - **Đáp án d:** 1
  - **Lời giải:**
    1. a) Mỗi đoạn con có số hữu tỉ nên sup = 1; U = tổng 1 . (độ dài) = độ dài [0, 1] = 1.
    2. b) Mỗi đoạn con có số vô tỉ nên inf = 0, L = 0.
    3. c) U - L = 1 với mọi P, không nhỏ hơn mọi e > 0: D không khả tích (nhưng khả tích Lebesgue với tích phân 0).
    4. d) Hiệu luôn bằng 1, nên giá trị nhỏ nhất là 1.
- `gt_t10_kt_11` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu |f| khả tích Riemann trên [a, b] thì f cũng khả tích Riemann trên [a, b].
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t7_nl_01`
  - **Đáp án:** Sai
    1. Phản ví dụ: f(x) = 1 nếu x hữu tỉ và f(x) = -1 nếu x vô tỉ trên [0, 1]. Khi đó |f| = 1 hằng nên khả tích, nhưng f = 2D - 1 (D là hàm Dirichlet) không khả tích.
    2. Chiều ngược lại đúng: f khả tích thì |f| khả tích. Mệnh đề sai.
- `gt_g10_tong_darboux` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = 27 - 4x trên [0, 6], phân hoạch P = {0, 3, 6}. Tính tổng Darboux trên U(f, P) (U = tổng của sup f trên mỗi đoạn con x độ dài đoạn con, L tương tự với inf). Nhập một số.
  - **Đáp án:** 126
    1. f(x) = 27 - 4x giảm trên [0, 6], nên trên mỗi đoạn con sup lấy ở mút trái và inf ở mút phải.
    2. Trên các đoạn con [0, 3], [3, 6]: sup = 27, 15; inf = 15, 3.
    3. U = 27 . 3 + 15 . 3 = 126; L = 15 . 3 + 3 . 3 = 54.
  - **Câu hỏi:** f(x) = 3x + 2 trên [0, 2], phân hoạch P = {0, 1, 2}. Tính tổng Darboux trên U(f, P) (U = tổng của sup f trên mỗi đoạn con x độ dài đoạn con, L tương tự với inf). Nhập một số.
  - **Đáp án:** 13
    1. f(x) = 3x + 2 tăng trên [0, 2], nên trên mỗi đoạn con sup lấy ở mút phải và inf ở mút trái.
    2. Trên các đoạn con [0, 1], [1, 2]: sup = 5, 8; inf = 2, 5.
    3. U = 5 . 1 + 8 . 1 = 13; L = 2 . 1 + 5 . 1 = 7.
  - **Câu hỏi:** f(x) = 6 - x trên [0, 6], phân hoạch P = {0, 2, 3, 4, 6}. Tính tổng Darboux dưới L(f, P) (U = tổng của sup f trên mỗi đoạn con x độ dài đoạn con, L tương tự với inf). Nhập một số.
  - **Đáp án:** 13
    1. f(x) = 6 - x giảm trên [0, 6], nên trên mỗi đoạn con sup lấy ở mút trái và inf ở mút phải.
    2. Trên các đoạn con [0, 2], [2, 3], [3, 4], [4, 6]: sup = 6, 4, 3, 2; inf = 4, 3, 2, 0.
    3. U = 6 . 2 + 4 . 1 + 3 . 1 + 2 . 2 = 23; L = 4 . 2 + 3 . 1 + 2 . 1 + 0 . 2 = 13.

### Hàm lồi (`gt_t10_ham_loi`)

- `gt_t10_hl_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^3 - 3x^2 + 1. Tìm số a nhỏ nhất để f là hàm lồi (f'' >= 0) trên [a, +vô cùng). Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_05`, `gt_g6_diem_uon`
  - **Đáp án:** 1
    1. f'(x) = 3x^2 - 6x và f''(x) = 6x - 6.
    2. f''(x) >= 0 khi và chỉ khi x >= 1: f lồi trên [1, +vô cùng) và lõm trên (-vô cùng, 1]; a = 1 (điểm uốn).
- `gt_t10_hl_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = |x| là hàm lồi trên R, dù f không có đạo hàm tại 0.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_g6_uon_tf`
  - **Đáp án:** Đúng
    1. Theo định nghĩa lồi: f(lx + (1 - l)y) <= l f(x) + (1 - l) f(y) với 0 <= l <= 1. Bất đẳng thức tam giác cho |lx + (1 - l)y| <= l|x| + (1 - l)|y|.
    2. Lồi không đòi hỏi khả vi. Mệnh đề đúng.
- `gt_t10_hl_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vì f(x) = x^4 có f''(0) = 0 nên f không là hàm lồi trên R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_t6_ll_01`
  - **Đáp án:** Sai
    1. f''(x) = 12 x^2 >= 0 với mọi x, nên f lồi trên R; f'' chỉ bằng 0 tại một điểm riêng lẻ, không đổi dấu: 0 không phải điểm uốn.
    2. Điều kiện lồi là f'' >= 0 (không âm), không phải f'' > 0. Mệnh đề sai.
- `gt_t10_hl_04` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dùng bất đẳng thức Jensen cho hàm lồi f(x) = e^x với ba số x, y, z, rồi đặt x = ln a, y = ln b, z = ln c (a, b, c > 0). Ta được bất đẳng thức nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_g6_uon_tf`
    - **(đúng)** (a + b + c)/3 >= (abc)^(1/3)
    - (a + b + c)/3 <= (abc)^(1/3)
    - (a + b + c)/3 >= abc
    - (a + b + c)/3 >= (a^2 + b^2 + c^2)/3
  - **Đáp án:** (a + b + c)/3 >= (abc)^(1/3)
    1. Jensen cho hàm lồi: f((x + y + z)/3) <= (f(x) + f(y) + f(z))/3, tức e^((ln a + ln b + ln c)/3) = (abc)^(1/3) <= (a + b + c)/3: bất đẳng thức giữa trung bình cộng và trung bình nhân.
    2. (a + b + c)/3 <= (abc)^(1/3) đảo chiều Jensen (đó là chiều của hàm lõm, như ln); thử a = 1, b = 1, c = 8: 10/3 > 2.
    3. (a + b + c)/3 >= abc bỏ căn bậc ba và không đúng (a = b = c = 2: 2 < 8).
    4. (a + b + c)/3 >= (a^2 + b^2 + c^2)/3 sai (a = b = c = 2: 2 < 4). Jensen cho hàm lồi x^2 chỉ cho ((a + b + c)/3)^2 <= (a^2 + b^2 + c^2)/3, một bất đẳng thức khác.
- `gt_t10_hl_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chứng minh f(x) = x^3 là hàm lồi trên R. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_05`, `gt_t6_ll_07`
  - **Lời giải đưa ra (có một bước sai):**
    1. f'(x) = 3x^2.
    2. f''(x) = 6x.
    3. f''(x) = 6x >= 0 với mọi x nên f lồi trên R.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: f''(x) = 6x >= 0 với mọi x nên f lồi trên R.
  - **Vì sao sai, và bước đúng:**
    1. 6x >= 0 chỉ khi x >= 0; với x < 0 thì f''(x) < 0. Vậy f chỉ lồi trên [0, +vô cùng) và lõm trên (-vô cùng, 0].
    2. x = 0 là điểm uốn của đồ thị x^3. Phản ví dụ về định nghĩa lồi: f((-1 + 0)/2) = -1/8 > (f(-1) + f(0))/2 = -1/2.
- `gt_t10_hl_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi hàm với kết luận về tính lồi của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_g6_uon_tf`
  - **Đáp án (ghép đúng):**
    - f(x) = e^x trên R — Lồi trên R
    - f(x) = ln x trên (0, +vô cùng) — Lõm trên (0, +vô cùng)
    - f(x) = x^3 trên R — Lồi trên [0, +vô cùng), lõm trên (-vô cùng, 0]
    - f(x) = sin x trên [0, pi] — Lõm trên [0, pi]
  - **Lời giải:**
    1. (e^x)'' = e^x > 0. (ln x)'' = -1/x^2 < 0. (x^3)'' = 6x. (sin x)'' = -sin x <= 0 trên [0, pi].
    2. Hàm lõm là hàm mà -f lồi.
- `gt_t10_hl_07` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh e^x >= 1 + x với mọi x bằng tính lồi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_g6_uon_tf`
  - **Đáp án (thứ tự đúng):**
    1. f(x) = e^x có f''(x) = e^x > 0 nên f lồi trên R.
    2. Tiếp tuyến của đồ thị f tại x = 0 là y = f(0) + f'(0) x = 1 + x.
    3. Đồ thị của một hàm lồi khả vi nằm trên mọi tiếp tuyến của nó.
    4. Vậy e^x >= 1 + x với mọi x, dấu bằng đúng tại x = 0.
  - **Lời giải:**
    1. Lồi cho tiếp tuyến nằm dưới đồ thị: dùng đúng một tiếp tuyến cụ thể (tại 0) để ra bất đẳng thức.
    2. Dấu bằng chỉ tại tiếp điểm vì f'' > 0 ngặt.
- `gt_t10_hl_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^3 - 6x^2 + 2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_05`, `gt_g6_diem_uon`
  - **Phần a** (Điền số): a) Tính f''(3).
    - **Đáp án a:** 6
  - **Phần b** (Điền số): b) Tìm hoành độ điểm uốn của đồ thị.
    - **Đáp án b:** 2
  - **Phần c** (Đúng/Sai): c) f là hàm lồi trên R.
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Tính f(2), tung độ của điểm uốn.
    - **Đáp án d:** -14
  - **Lời giải:**
    1. a) f'(x) = 3x^2 - 12x, f''(x) = 6x - 12, nên f''(3) = 6.
    2. b) f'' đổi dấu tại 6x - 12 = 0, tức x = 2: lõm trên (-vô cùng, 2], lồi trên [2, +vô cùng).
    3. c) f''(0) = -12 < 0 nên f không lồi trên R.
    4. d) f(2) = 8 - 24 + 2 = -14.
- `gt_t10_hl_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^2 (lồi), x = 1, y = 5 và hệ số l = 1/4 trong bất đẳng thức Jensen f(l x + (1 - l) y) <= l f(x) + (1 - l) f(y).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_g6_uon_tf`
  - **Phần a** (Điền số): a) Tính vế trái f(l x + (1 - l) y).
    - **Đáp án a:** 16
  - **Phần b** (Điền số): b) Tính vế phải l f(x) + (1 - l) f(y).
    - **Đáp án b:** 19
  - **Phần c** (Đúng/Sai): c) Hai kết quả phù hợp với bất đẳng thức Jensen.
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Tính hiệu (vế phải) - (vế trái).
    - **Đáp án d:** 3
  - **Lời giải:**
    1. a) l x + (1 - l) y = 1/4 + 15/4 = 4, f(4) = 16.
    2. b) 1/4 . 1 + 3/4 . 25 = 1/4 + 75/4 = 19.
    3. c) 16 <= 19: đúng với hàm lồi.
    4. d) 19 - 16 = 3. Với f(x) = x^2 hiệu bằng l (1 - l)(x - y)^2 = 3/16 . 16 = 3, và bằng 0 chỉ khi x = y hay l = 0, 1.
- `gt_t10_hl_10` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích của hai hàm lồi trên R luôn là một hàm lồi.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_ll_07`, `gt_t6_ll_01`
  - **Đáp án:** Sai
    1. Phản ví dụ: f(x) = x và g(x) = -x đều lồi (hàm tuyến tính), nhưng tích f g = -x^2 là hàm lõm.
    2. Tổng của hai hàm lồi thì lồi; tích thì không bảo toàn tính lồi. Mệnh đề sai.
- `gt_g10_diem_uon_so` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** f(x) = x^3 + 9x^2 + 6x - 4. Tìm số x0 nhỏ nhất sao cho f là hàm lồi (f'' >= 0) trên [x0, +vô cùng). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -3
    1. f''(x) = 6x + 18.
    2. f''(x) >= 0 khi x >= -3 (nghiệm của f'' = 0, vì hệ số 6 dương). Vậy x0 = -3, hoành độ điểm uốn.
  - **Câu hỏi:** f(x) = x^3 - 7x^2 - 5x. Tìm số x0 nhỏ nhất sao cho f là hàm lồi (f'' >= 0) trên [x0, +vô cùng). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 7/3
    1. f''(x) = 6x - 14.
    2. f''(x) >= 0 khi x >= 7/3 (nghiệm của f'' = 0, vì hệ số 6 dương). Vậy x0 = 7/3, hoành độ điểm uốn.
  - **Câu hỏi:** f(x) = x^3 + 9x^2 + 2x - 3. Tìm số x0 nhỏ nhất sao cho f là hàm lồi (f'' >= 0) trên [x0, +vô cùng). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -3
    1. f''(x) = 6x + 18.
    2. f''(x) >= 0 khi x >= -3 (nghiệm của f'' = 0, vì hệ số 6 dương). Vậy x0 = -3, hoành độ điểm uốn.
- `gt_g10_jensen_hieu` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hàm f(x) = x^2 lồi trên R. Với x = 1, y = 7 và hệ số l = 3/4, tính hiệu l f(x) + (1 - l) f(y) - f(l x + (1 - l) y), vế phải trừ vế trái của bất đẳng thức Jensen. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 27/4
    1. l x + (1 - l) y = 3/4 . 1 + 1/4 . 7 = 5/2, nên f(l x + (1 - l) y) = 25/4.
    2. l f(x) + (1 - l) f(y) = 3/4 . 1 + 1/4 . 49 = 13.
    3. Hiệu = 13 - 25/4 = 27/4, không âm đúng như Jensen cho hàm lồi.
  - **Câu hỏi:** Hàm f(x) = x^2 lồi trên R. Với x = 1, y = 3 và hệ số l = 1/2, tính hiệu l f(x) + (1 - l) f(y) - f(l x + (1 - l) y), vế phải trừ vế trái của bất đẳng thức Jensen. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 1
    1. l x + (1 - l) y = 1/2 . 1 + 1/2 . 3 = 2, nên f(l x + (1 - l) y) = 4.
    2. l f(x) + (1 - l) f(y) = 1/2 . 1 + 1/2 . 9 = 5.
    3. Hiệu = 5 - 4 = 1, không âm đúng như Jensen cho hàm lồi.
  - **Câu hỏi:** Hàm f(x) = x^2 lồi trên R. Với x = 2, y = 5 và hệ số l = 3/4, tính hiệu l f(x) + (1 - l) f(y) - f(l x + (1 - l) y), vế phải trừ vế trái của bất đẳng thức Jensen. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 27/16
    1. l x + (1 - l) y = 3/4 . 2 + 1/4 . 5 = 11/4, nên f(l x + (1 - l) y) = 121/16.
    2. l f(x) + (1 - l) f(y) = 3/4 . 4 + 1/4 . 25 = 37/4.
    3. Hiệu = 37/4 - 121/16 = 27/16, không âm đúng như Jensen cho hàm lồi.

### Không gian metric và không gian định chuẩn (`gt_t10_khong_gian_metric`)

- `gt_t10_mt_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^2 với khoảng cách d_1(u, v) = |u1 - v1| + |u2 - v2| (khoảng cách taxi), tính d_1(u, v) với u = (1, 2) và v = (4, -2). Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_05`, `gt_t7_nl_02`
  - **Đáp án:** 7
    1. u - v = (-3, 4), nên d_1 = |-3| + |4| = 7.
    2. Khoảng cách Euclid của hai điểm này là sqrt(9 + 16) = 5, nhỏ hơn: d_1 >= d_2 với mọi cặp điểm.
- `gt_t10_mt_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3 với khoảng cách d_inf(u, v) = lớn nhất của |u_i - v_i|, tính d_inf(u, v) với u = (-3, 5, 0) và v = (2, 1, 4). Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_05`, `gt_t7_nl_02`
  - **Đáp án:** 5
    1. Hiệu từng thành phần: |-3 - 2| = 5, |5 - 1| = 4, |0 - 4| = 4.
    2. d_inf = lớn nhất = 5.
- `gt_t10_mt_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chuẩn Euclid của vectơ x = (3, -4, 12) trong R^3 là ||x||_2 = sqrt(x1^2 + x2^2 + x3^2). Tính ||x||_2. Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t6_gl_05`, `gt_t7_nl_02`
  - **Đáp án:** 13
    1. ||x||_2^2 = 9 + 16 + 144 = 169.
    2. ||x||_2 = sqrt(169) = 13. (Chuẩn tổng ||x||_1 = 19 và chuẩn max ||x||_inf = 12 cho kết quả khác.)
- `gt_t10_mt_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** d(x, y) = (x - y)^2 là một khoảng cách (metric) trên R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Đáp án:** Sai
    1. Bất đẳng thức tam giác d(x, z) <= d(x, y) + d(y, z) bị vi phạm: với x = 0, y = 1, z = 2 thì d(0, 2) = 4 còn d(0, 1) + d(1, 2) = 1 + 1 = 2.
    2. Hai tiên đề đầu (không âm, bằng 0 khi x = y; đối xứng) vẫn đúng, nhưng thiếu bất đẳng thức tam giác. Mệnh đề sai.
- `gt_t10_mt_05` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** d(x, y) = |x^2 - y^2| là một khoảng cách (metric) trên R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Đáp án:** Sai
    1. Một metric phải có d(x, y) = 0 chỉ khi x = y. Ở đây d(1, -1) = |1 - 1| = 0 nhưng 1 khác -1.
    2. (Trên [0, +vô cùng) thì d là metric, vì x -> x^2 là đơn ánh ở đó.) Mệnh đề sai trên R.
- `gt_t10_mt_06` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hàm nào dưới đây là một khoảng cách (metric) trên R?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
    - **(đúng)** d(x, y) = |x - y|/(1 + |x - y|)
    - d(x, y) = (x - y)^2
    - d(x, y) = x - y
    - d(x, y) = |x^2 - y^2|
  - **Đáp án:** d(x, y) = |x - y|/(1 + |x - y|)
    1. |x - y|/(1 + |x - y|) không âm, bằng 0 khi x = y, đối xứng, và thoả bất đẳng thức tam giác (vì t -> t/(1 + t) tăng và g(s + t) <= g(s) + g(t)); đó là metric bị chặn bởi 1.
    2. (x - y)^2 vi phạm bất đẳng thức tam giác: d(0, 2) = 4 > d(0, 1) + d(1, 2) = 2.
    3. x - y âm khi x < y và không đối xứng (d(1, 0) = 1 nhưng d(0, 1) = -1).
    4. |x^2 - y^2| bằng 0 với x = 1, y = -1 dù x khác y.
- `gt_t10_mt_07` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chứng minh d(x, y) = (x - y)^2 là metric trên R. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Lời giải đưa ra (có một bước sai):**
    1. d(x, y) >= 0, và d(x, y) = 0 khi và chỉ khi x = y.
    2. d đối xứng vì (x - y)^2 = (y - x)^2.
    3. Tam giác: (x - z)^2 = ((x - y) + (y - z))^2 = (x - y)^2 + (y - z)^2, tức d(x, z) = d(x, y) + d(y, z).   **<- bước sai đầu tiên**
    4. Vậy d là một metric trên R.
  - **Đáp án:** Bước 3: Tam giác: (x - z)^2 = ((x - y) + (y - z))^2 = (x - y)^2 + (y - z)^2, tức d(x, z) = d(x, y) + d(y, z).
  - **Vì sao sai, và bước đúng:**
    1. Khai triển thiếu số hạng giữa: ((x - y) + (y - z))^2 = (x - y)^2 + 2 (x - y)(y - z) + (y - z)^2.
    2. Khi (x - y)(y - z) > 0 số hạng 2 (x - y)(y - z) dương nên d(x, z) > d(x, y) + d(y, z): với x = 0, y = 1, z = 2 có 4 > 2. d không là metric.
- `gt_t10_mt_08` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dãy với kết luận về tính Cauchy và tính hội tụ của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Đáp án (ghép đúng):**
    - x_n = 1/n trong R — Dãy Cauchy, hội tụ về 0
    - x_n = (-1)^n trong R — Không là dãy Cauchy: hai số hạng liên tiếp cách nhau 2
    - Các số thập phân gần đúng sqrt(2): 1, 1.4, 1.41, 1.414, ... trong Q — Dãy Cauchy trong Q nhưng không hội tụ trong Q
    - x_n = n trong R — Không là dãy Cauchy (không bị chặn)
  - **Lời giải:**
    1. Dãy Cauchy là dãy mà các số hạng xa tuỳ ý rồi thì gần nhau tuỳ ý. Trong R mọi dãy Cauchy hội tụ (R đầy đủ); trong Q thì không.
    2. |(-1)^(n+1) - (-1)^n| = 2 không bé hơn mọi e; |x_(n+1) - x_n| = 1 với x_n = n.
- `gt_t10_mt_09` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh mọi dãy hội tụ trong một không gian metric đều là dãy Cauchy.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Đáp án (thứ tự đúng):**
    1. Giả sử x_n tiến tới L và cho e > 0.
    2. Chọn N sao cho d(x_n, L) < e/2 với mọi n >= N.
    3. Với m, n >= N, bất đẳng thức tam giác cho d(x_m, x_n) <= d(x_m, L) + d(L, x_n).
    4. Vế phải nhỏ hơn e/2 + e/2 = e, nên d(x_m, x_n) < e với mọi m, n >= N: (x_n) là dãy Cauchy.
  - **Lời giải:**
    1. Chọn e/2 trước để tổng cuối vừa bằng e; bất đẳng thức tam giác là chỗ duy nhất dùng đến tính chất của metric.
    2. Chiều ngược lại (Cauchy thì hội tụ) chỉ đúng trong không gian đầy đủ như R, không đúng trong Q.
- `gt_t10_mt_10` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3 cho u = (1, 0, 2) và v = (4, 4, -10). Ba khoảng cách d_1 (tổng |u_i - v_i|), d_2 (Euclid) và d_inf (lớn nhất |u_i - v_i|).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Phần a** (Điền số): a) Tính d_1(u, v).
    - **Đáp án a:** 19
  - **Phần b** (Điền số): b) Tính d_2(u, v).
    - **Đáp án b:** 13
  - **Phần c** (Điền số): c) Tính d_inf(u, v).
    - **Đáp án c:** 12
  - **Phần d** (Đúng/Sai): d) Với mọi hai điểm của R^n, d_inf <= d_2 <= d_1.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) u - v = (-3, -4, 12): 3 + 4 + 12 = 19.
    2. b) sqrt(9 + 16 + 144) = sqrt(169) = 13.
    3. c) max(3, 4, 12) = 12.
    4. d) Gọi m là thành phần lớn nhất: d_inf = m, d_2 = sqrt(tổng bình phương) >= m, và d_1 = tổng |.| >= sqrt(tổng bình phương) vì (tổng |a_i|)^2 >= tổng a_i^2.
- `gt_t10_mt_11` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên tập X = {a, b, c} xét khoảng cách rời rạc: d(x, y) = 0 nếu x = y và d(x, y) = 1 nếu x khác y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `gt_t7_nl_02`, `gt_t3_ld_05`
  - **Phần a** (Điền số): a) Tính d(a, b).
    - **Đáp án a:** 1
  - **Phần b** (Đúng/Sai): b) Bất đẳng thức tam giác d(x, z) <= d(x, y) + d(y, z) đúng với mọi x, y, z thuộc X.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Quả cầu mở B(a, 1) = {x : d(a, x) < 1} có bao nhiêu phần tử?
    - **Đáp án c:** 1
  - **Phần d** (Đúng/Sai): d) Dãy x_n = 1/n (trong R) là dãy Cauchy khi dùng khoảng cách rời rạc d trên R.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) a khác b nên d(a, b) = 1.
    2. b) Nếu x = z thì vế trái 0. Nếu x khác z thì vế trái 1 và vì y không thể cùng bằng x và z, ít nhất một trong d(x, y), d(y, z) bằng 1: vế phải >= 1.
    3. c) d(a, x) < 1 nghĩa là d(a, x) = 0, tức x = a: quả cầu chỉ có một điểm {a}.
    4. d) Với d rời rạc, d(1/m, 1/n) = 1 khi m khác n, không bé hơn e = 1/2: dãy không là Cauchy. (Dãy Cauchy với metric rời rạc là dãy cuối cùng hằng.)
- `gt_g10_chuan_vecto` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^2, tính khoảng cách d_1 (tổng |u_i - v_i|) giữa u = (2, 5) và v = (-4, -3). Nhập một số.
  - **Đáp án:** 14
    1. u - v = (6, 8).
    2. d1 = 6 + 8 = 14.
  - **Câu hỏi:** Trong R^2, tính khoảng cách d_1 (tổng |u_i - v_i|) giữa u = (-1, 4) và v = (2, 0). Nhập một số.
  - **Đáp án:** 7
    1. u - v = (-3, 4).
    2. d1 = 3 + 4 = 7.
  - **Câu hỏi:** Trong R^2, tính khoảng cách d_1 (tổng |u_i - v_i|) giữa u = (2, -1) và v = (10, 5). Nhập một số.
  - **Đáp án:** 14
    1. u - v = (-8, -6).
    2. d1 = 8 + 6 = 14.
- `gt_g10_metric_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** d(x, y) = |x^2 - y^2| là một khoảng cách (metric) trên tập số thực R.
  - **Đáp án:** Sai
    1. Bằng 0 với x = 1, y = -1 dù x khác y.
    2. Mệnh đề sai.
  - **Câu hỏi:** d(x, y) = |x - y| là một khoảng cách (metric) trên tập số thực R.
  - **Đáp án:** Đúng
    1. Đây là khoảng cách thông thường trên R.
    2. Mệnh đề đúng.
  - **Câu hỏi:** d(x, y) = |x - y|/(1 + |x - y|) là một khoảng cách (metric) trên tập số thực R.
  - **Đáp án:** Đúng
    1. Không âm, bằng 0 khi x = y, đối xứng, và thoả bất đẳng thức tam giác (t -> t/(1 + t) tăng và g(s + t) <= g(s) + g(t)).
    2. Mệnh đề đúng.
