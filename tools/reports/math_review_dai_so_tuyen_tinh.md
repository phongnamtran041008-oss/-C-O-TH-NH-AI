# Bảng duyệt câu hỏi: Đại Số Tuyến Tính

Tạo bởi `python tools/math_review.py`. Đánh dấu đã duyệt bằng `"reviewed": true` trong `server/data/math/items/dai_so_tuyen_tinh.json`.

## Tầng 1: Tập hợp và ánh xạ

49 dạng câu (36 câu viết tay, 13 bộ sinh câu); 49 chưa duyệt.

### Tập hợp và phần tử (`dstt_t1_tap_hop`)

- `dstt_t1_th_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 3}. Số 2 thuộc A.
  - **Đáp án:** Đúng
    1. A được cho bằng cách liệt kê các phần tử 1, 2, 3.
    2. Số 2 có trong danh sách đó nên 2 thuộc A.
- `dstt_t1_th_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {a, b, c}. Tập nào sau đây là tập con của A?
    - **(đúng)** {a, c}
    - {a, d}
    - {d}
    - {a, b, c, d}
  - **Đáp án:** {a, c}
    1. B là tập con của A khi mọi phần tử của B đều thuộc A.
    2. Ba tập còn lại đều chứa d, mà d không thuộc A.
    3. Chỉ có {a, c} gồm toàn phần tử của A.
- `dstt_t1_th_03` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập A = {2, 4, 6, 8, 10} có bao nhiêu phần tử?
  - **Đáp án:** 5
    1. Đếm các phần tử được liệt kê: 2, 4, 6, 8, 10.
    2. Có 5 phần tử.
- `dstt_g1_thuoc` · bậc 1 (Nhập môn) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {2, 10, 13, 14}. Số 14 thuộc A.
  - **Đáp án:** Đúng
    1. Các phần tử của A là 2, 10, 13, 14.
    2. Số 14 có trong danh sách đó nên 14 thuộc A.
  - **Câu hỏi:** Cho A = {2, 3, 6, 15}. Số 14 thuộc A.
  - **Đáp án:** Sai
    1. Các phần tử của A là 2, 3, 6, 15.
    2. Số 14 không có trong danh sách đó nên 14 không thuộc A.
  - **Câu hỏi:** Cho A = {3, 6, 9, 10}. Số 12 thuộc A.
  - **Đáp án:** Sai
    1. Các phần tử của A là 3, 6, 9, 10.
    2. Số 12 không có trong danh sách đó nên 12 không thuộc A.
- `dstt_t1_th_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập A = {1, 2, 3} có bao nhiêu tập con, kể cả tập rỗng và chính A?
  - **Đáp án:** 8
    1. Khi lập một tập con, mỗi phần tử của A có 2 khả năng: được chọn hoặc không được chọn.
    2. A có 3 phần tử nên số tập con là 2^3 = 8.
- `dstt_t1_th_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, {2, 3}}. Số 2 là một phần tử của A.
  - **Đáp án:** Sai
    1. A có đúng hai phần tử: số 1 và tập {2, 3}.
    2. Số 2 là phần tử của tập {2, 3}, không phải là phần tử của A.
- `dstt_t1_th_06` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập rỗng là tập con của mọi tập hợp.
  - **Đáp án:** Đúng
    1. B là tập con của A khi không có phần tử nào của B nằm ngoài A.
    2. Tập rỗng không có phần tử nào, nên không thể có phần tử nằm ngoài A.
    3. Vậy tập rỗng là tập con của mọi tập hợp A.
- `dstt_g1_so_tap_con` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tập A = {2, 5, 10, 11} có bao nhiêu tập con, kể cả tập rỗng và chính A?
  - **Đáp án:** 16
    1. A có 4 phần tử.
    2. Khi lập một tập con, mỗi phần tử có 2 khả năng: được chọn hoặc không được chọn.
    3. Số tập con là 2^4 = 16.
  - **Câu hỏi:** Tập A = {2, 6, 12} có bao nhiêu tập con, kể cả tập rỗng và chính A?
  - **Đáp án:** 8
    1. A có 3 phần tử.
    2. Khi lập một tập con, mỗi phần tử có 2 khả năng: được chọn hoặc không được chọn.
    3. Số tập con là 2^3 = 8.
  - **Câu hỏi:** Tập A = {3, 6, 9, 10} có bao nhiêu tập con, kể cả tập rỗng và chính A?
  - **Đáp án:** 16
    1. A có 4 phần tử.
    2. Khi lập một tập con, mỗi phần tử có 2 khả năng: được chọn hoặc không được chọn.
    3. Số tập con là 2^4 = 16.

### Phép toán trên tập hợp (`dstt_t1_phep_toan_tap_hop`)

- `dstt_t1_pt_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 3, 4} và B = {3, 4, 5}. Liệt kê các phần tử của A giao B.
  - **Đáp án:** 3, 4  (thứ tự nào cũng được)
    1. A giao B gồm các phần tử thuộc cả A và B.
    2. Chỉ có 3 và 4 có mặt trong cả hai tập.
    3. A giao B = {3, 4}.
- `dstt_t1_pt_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2} và B = {2, 3}. A hợp B là tập nào?
    - **(đúng)** {1, 2, 3}
    - {2}
    - {1, 3}
    - {1}
  - **Đáp án:** {1, 2, 3}
    1. A hợp B gồm các phần tử thuộc A hoặc thuộc B.
    2. Gom các phần tử của hai tập, mỗi phần tử chỉ viết một lần: 1, 2, 3.
    3. A hợp B = {1, 2, 3}.
- `dstt_t1_pt_06` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {2, 4, 6, 8} và B = {6, 8, 10}. Ghép mỗi phép toán với tập kết quả của nó.
  - **Đáp án (ghép đúng):**
    - A hợp B — {2, 4, 6, 8, 10}
    - A giao B — {6, 8}
    - A \ B — {2, 4}
    - B \ A — {10}
  - **Lời giải:**
    1. A hợp B gồm các phần tử thuộc A hoặc thuộc B: {2, 4, 6, 8, 10}.
    2. A giao B gồm các phần tử thuộc cả A và B: {6, 8}.
    3. A \ B gồm các phần tử thuộc A mà không thuộc B: {2, 4}.
    4. B \ A gồm các phần tử thuộc B mà không thuộc A: chỉ còn {10}.
- `dstt_t1_pt_07` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 3, 4, 5}, B = {2, 4, 6} và C = {5, 7}. Sắp xếp các bước tìm (A giao B) hợp C.
  - **Đáp án (thứ tự đúng):**
    1. Làm phép trong ngoặc trước: tìm các phần tử thuộc cả A và B.
    2. Được A giao B = {2, 4}.
    3. Lấy hợp với C: (A giao B) hợp C = {2, 4} hợp {5, 7}.
    4. Kết quả là {2, 4, 5, 7}.
  - **Lời giải:**
    1. Phép trong ngoặc làm trước: A giao B gồm 2 và 4, vì đó là hai phần tử có mặt ở cả A và B.
    2. Sau đó hợp {2, 4} với C = {5, 7} bằng cách gộp các phần tử của hai tập.
    3. Vậy (A giao B) hợp C = {2, 4, 5, 7}.
- `dstt_g1_giao` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 8} và B = {1, 4, 6, 7}. Liệt kê các phần tử của A giao B.
  - **Đáp án:** 1  (thứ tự nào cũng được)
    1. A giao B gồm các phần tử thuộc cả A và B.
    2. Các phần tử có mặt trong cả hai tập: 1.
    3. A giao B = {1}.
  - **Câu hỏi:** Cho A = {2, 3, 9} và B = {5, 8, 9}. Liệt kê các phần tử của A giao B.
  - **Đáp án:** 9  (thứ tự nào cũng được)
    1. A giao B gồm các phần tử thuộc cả A và B.
    2. Các phần tử có mặt trong cả hai tập: 9.
    3. A giao B = {9}.
  - **Câu hỏi:** Cho A = {3, 8, 9} và B = {1, 2, 4, 5, 8}. Liệt kê các phần tử của A giao B.
  - **Đáp án:** 8  (thứ tự nào cũng được)
    1. A giao B gồm các phần tử thuộc cả A và B.
    2. Các phần tử có mặt trong cả hai tập: 8.
    3. A giao B = {8}.
- `dstt_g1_hop_dem` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 8} và B = {1, 4, 6, 7}. A hợp B có bao nhiêu phần tử?
  - **Đáp án:** 6
    1. A hợp B gồm các phần tử thuộc A hoặc thuộc B, mỗi phần tử chỉ tính một lần.
    2. A hợp B = {1, 2, 4, 6, 7, 8}.
    3. Có 6 phần tử.
  - **Câu hỏi:** Cho A = {2, 3, 9} và B = {5, 8, 9}. A hợp B có bao nhiêu phần tử?
  - **Đáp án:** 5
    1. A hợp B gồm các phần tử thuộc A hoặc thuộc B, mỗi phần tử chỉ tính một lần.
    2. A hợp B = {2, 3, 5, 8, 9}.
    3. Có 5 phần tử.
  - **Câu hỏi:** Cho A = {3, 8, 9} và B = {1, 2, 4, 5, 8}. A hợp B có bao nhiêu phần tử?
  - **Đáp án:** 7
    1. A hợp B gồm các phần tử thuộc A hoặc thuộc B, mỗi phần tử chỉ tính một lần.
    2. A hợp B = {1, 2, 3, 4, 5, 8, 9}.
    3. Có 7 phần tử.
- `dstt_t1_pt_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 3, 4, 5} và B = {2, 4, 6}. Liệt kê các phần tử của hiệu A \ B.
  - **Đáp án:** 1, 3, 5  (thứ tự nào cũng được)
    1. A \ B gồm các phần tử thuộc A nhưng không thuộc B.
    2. Bỏ khỏi A các phần tử 2 và 4 vì chúng thuộc B.
    3. A \ B = {1, 3, 5}.
- `dstt_t1_pt_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong tập nền U gồm các số nguyên từ 1 đến 10, cho A = {2, 4, 6, 8, 10}. Phần bù của A trong U có bao nhiêu phần tử?
  - **Đáp án:** 5
    1. Phần bù của A trong U gồm các phần tử của U không thuộc A.
    2. Đó là 1, 3, 5, 7, 9.
    3. Phần bù có 5 phần tử.
- `dstt_t1_pt_05` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi tập A và B, ta luôn có A \ B = B \ A.
  - **Đáp án:** Sai
    1. Chỉ cần một ví dụ để bác bỏ: lấy A = {1, 2} và B = {2}.
    2. A \ B = {1}, còn B \ A là tập rỗng.
    3. Hai kết quả khác nhau, nên phép hiệu không đổi chỗ được.
- `dstt_t1_pt_08` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính B \ A với A = {1, 2, 3, 4} và B = {3, 4, 5}. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Các phần tử chung của A và B là 3 và 4.
    2. B \ A giữ lại những phần tử của A không có trong B, tức là 1 và 2.   **<- bước sai đầu tiên**
    3. Vậy B \ A = {1, 2}.
  - **Đáp án:** Bước 2: B \ A giữ lại những phần tử của A không có trong B, tức là 1 và 2.
  - **Vì sao sai, và bước đúng:**
    1. B \ A là phần của B sau khi bỏ đi những phần tử cũng có trong A, chứ không phải phần của A. Bước 2 vừa tính A \ B.
    2. Đúng ra: bỏ 3 và 4 khỏi B = {3, 4, 5}, còn lại 5. Vậy B \ A = {5}, và A \ B = {1, 2} là một tập khác.
- `dstt_g1_hieu` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2, 8} và B = {1, 4, 6, 7}. Liệt kê các phần tử của hiệu A \ B.
  - **Đáp án:** 2, 8  (thứ tự nào cũng được)
    1. A \ B gồm các phần tử thuộc A nhưng không thuộc B.
    2. Bỏ khỏi A các phần tử cũng thuộc B: 1.
    3. A \ B = {2, 8}.
  - **Câu hỏi:** Cho A = {2, 3, 9} và B = {5, 8, 9}. Liệt kê các phần tử của hiệu A \ B.
  - **Đáp án:** 2, 3  (thứ tự nào cũng được)
    1. A \ B gồm các phần tử thuộc A nhưng không thuộc B.
    2. Bỏ khỏi A các phần tử cũng thuộc B: 9.
    3. A \ B = {2, 3}.
  - **Câu hỏi:** Cho A = {3, 8, 9} và B = {1, 2, 4, 5, 8}. Liệt kê các phần tử của hiệu A \ B.
  - **Đáp án:** 3, 9  (thứ tự nào cũng được)
    1. A \ B gồm các phần tử thuộc A nhưng không thuộc B.
    2. Bỏ khỏi A các phần tử cũng thuộc B: 8.
    3. A \ B = {3, 9}.

### Tích Descartes (`dstt_t1_tich_descartes`)

- `dstt_t1_td_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2} và B = {a, b, c}. Tích Descartes A x B có bao nhiêu phần tử?
  - **Đáp án:** 6
    1. Mỗi phần tử của A x B là một cặp (x, y) với x thuộc A và y thuộc B.
    2. Có 2 cách chọn x và 3 cách chọn y.
    3. Số cặp là 2 . 3 = 6.
- `dstt_t1_td_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2} và B = {a, b}. Cặp (a, 1) thuộc A x B.
  - **Đáp án:** Sai
    1. Trong một cặp của A x B, thành phần đứng trước phải thuộc A, thành phần đứng sau phải thuộc B.
    2. Ở cặp (a, 1), thành phần đứng trước là a, không thuộc A.
    3. Cặp (a, 1) thuộc B x A chứ không thuộc A x B.
- `dstt_t1_td_05` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 2} và B = {a, b, c}. Ghép mỗi tích Descartes với số phần tử của nó.
  - **Đáp án (ghép đúng):**
    - A x B — 6
    - B x B — 9
    - A x A — 4
    - A x {0} — 2
  - **Lời giải:**
    1. Số phần tử của X x Y bằng số phần tử của X nhân số phần tử của Y.
    2. A có 2 phần tử, B có 3 phần tử, {0} có 1 phần tử.
    3. A x B: 2 . 3 = 6. B x B: 3 . 3 = 9. A x A: 2 . 2 = 4. A x {0}: 2 . 1 = 2.
- `dstt_g1_tich_dem` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {1, 4, 7} và B = {d, h}. Tích Descartes A x B có bao nhiêu phần tử?
  - **Đáp án:** 6
    1. Mỗi phần tử của A x B là một cặp (x, y) với x thuộc A và y thuộc B.
    2. Có 3 cách chọn x và 2 cách chọn y.
    3. Số cặp là 3 . 2 = 6.
  - **Câu hỏi:** Cho A = {1, 5} và B = {c, f}. Tích Descartes A x B có bao nhiêu phần tử?
  - **Đáp án:** 4
    1. Mỗi phần tử của A x B là một cặp (x, y) với x thuộc A và y thuộc B.
    2. Có 2 cách chọn x và 2 cách chọn y.
    3. Số cặp là 2 . 2 = 4.
  - **Câu hỏi:** Cho A = {1, 5, 7} và B = {a, d, g}. Tích Descartes A x B có bao nhiêu phần tử?
  - **Đáp án:** 9
    1. Mỗi phần tử của A x B là một cặp (x, y) với x thuộc A và y thuộc B.
    2. Có 3 cách chọn x và 3 cách chọn y.
    3. Số cặp là 3 . 3 = 9.
- `dstt_t1_td_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A = {0, 1}. Tập A x A là tập nào?
    - **(đúng)** {(0, 0), (0, 1), (1, 0), (1, 1)}
    - {(0, 1), (1, 0)}
    - {(0, 0), (1, 1)}
    - {0, 1}
  - **Đáp án:** {(0, 0), (0, 1), (1, 0), (1, 1)}
    1. A x A gồm mọi cặp (x, y) với x và y đều thuộc A.
    2. x có 2 cách chọn, y có 2 cách chọn, nên có 4 cặp.
    3. A x A = {(0, 0), (0, 1), (1, 0), (1, 1)}.
- `dstt_t1_td_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập A x B có 12 phần tử và A có 3 phần tử. B có bao nhiêu phần tử?
  - **Đáp án:** 4
    1. Số phần tử của A x B bằng số phần tử của A nhân với số phần tử của B.
    2. Gọi n là số phần tử của B: 3 . n = 12.
    3. n = 4.
- `dstt_t1_td_07` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau đếm số phần tử của A x B với A = {1, 2} và B = {x, y, z}. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. A có 2 phần tử và B có 3 phần tử.
    2. Mỗi phần tử của A ghép với mỗi phần tử của B, nên số cặp là |A| + |B| = 2 + 3 = 5.   **<- bước sai đầu tiên**
    3. Vậy A x B có 5 cặp có thứ tự.
  - **Đáp án:** Bước 2: Mỗi phần tử của A ghép với mỗi phần tử của B, nên số cặp là |A| + |B| = 2 + 3 = 5.
  - **Vì sao sai, và bước đúng:**
    1. Mỗi cách chọn thành phần đầu ghép được với mọi cách chọn thành phần sau, nên số cặp là tích chứ không phải tổng.
    2. Đúng ra: |A x B| = |A| . |B| = 2 . 3 = 6. Đó là (1, x), (1, y), (1, z), (2, x), (2, y), (2, z).
- `dstt_g1_tich_nguoc` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tập A x B có 9 phần tử và A có 3 phần tử. B có bao nhiêu phần tử?
  - **Đáp án:** 3
    1. Số phần tử của A x B bằng số phần tử của A nhân với số phần tử của B.
    2. Gọi n là số phần tử của B: 3 . n = 9.
    3. n = 3.
  - **Câu hỏi:** Tập A x B có 6 phần tử và A có 2 phần tử. B có bao nhiêu phần tử?
  - **Đáp án:** 3
    1. Số phần tử của A x B bằng số phần tử của A nhân với số phần tử của B.
    2. Gọi n là số phần tử của B: 2 . n = 6.
    3. n = 3.
  - **Câu hỏi:** Tập A x B có 12 phần tử và A có 3 phần tử. B có bao nhiêu phần tử?
  - **Đáp án:** 4
    1. Số phần tử của A x B bằng số phần tử của A nhân với số phần tử của B.
    2. Gọi n là số phần tử của B: 3 . n = 12.
    3. n = 4.

### Ánh xạ, ảnh và tạo ảnh (`dstt_t1_anh_xa`)

- `dstt_t1_ax_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ánh xạ f: R -> R, f(x) = 2x + 1. Tính f(3).
  - **Đáp án:** 7
    1. Thay x = 3 vào công thức của f.
    2. f(3) = 2 . 3 + 1 = 7.
- `dstt_t1_ax_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quy tắc cho mỗi số thực x ứng với mọi số thực y thỏa mãn y^2 = x là một ánh xạ từ R vào R.
  - **Đáp án:** Sai
    1. Một ánh xạ phải cho mỗi phần tử của tập nguồn đúng một ảnh.
    2. Với x = 4 có hai giá trị y = 2 và y = -2; với x = -1 thì không có y nào.
    3. Vậy quy tắc này không phải là ánh xạ.
- `dstt_g1_anh_bac_nhat` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ánh xạ f: R -> R, f(x) = -3x + 9. Tính f(-4).
  - **Đáp án:** 21
    1. Thay x = -4 vào công thức của f.
    2. f(-4) = (-3) . (-4) + 9 = 21.
  - **Câu hỏi:** Cho ánh xạ f: R -> R, f(x) = -5x - 7. Tính f(-4).
  - **Đáp án:** 13
    1. Thay x = -4 vào công thức của f.
    2. f(-4) = (-5) . (-4) + (-7) = 13.
  - **Câu hỏi:** Cho ánh xạ f: R -> R, f(x) = -2x + 9. Tính f(3).
  - **Đáp án:** 3
    1. Thay x = 3 vào công thức của f.
    2. f(3) = (-2) . 3 + 9 = 3.
- `dstt_t1_ax_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2 và A = {-2, -1, 0, 1, 2}. Liệt kê các phần tử của ảnh f(A).
  - **Đáp án:** 0, 1, 4  (thứ tự nào cũng được)
    1. f(A) gồm ảnh của mọi phần tử thuộc A.
    2. f(-2) = f(2) = 4, f(-1) = f(1) = 1, f(0) = 0.
    3. Mỗi giá trị chỉ viết một lần: f(A) = {0, 1, 4}.
- `dstt_t1_ax_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2. Liệt kê các phần tử của tạo ảnh của tập {4} qua f.
  - **Đáp án:** -2, 2  (thứ tự nào cũng được)
    1. Tạo ảnh của {4} gồm mọi x sao cho f(x) thuộc {4}, tức là x^2 = 4.
    2. Phương trình x^2 = 4 có hai nghiệm x = 2 và x = -2.
    3. Tạo ảnh cần tìm là {-2, 2}.
- `dstt_t1_ax_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2 - 1. Sắp xếp các bước tìm tạo ảnh của tập {3}.
  - **Đáp án (thứ tự đúng):**
    1. Tạo ảnh của {3} gồm mọi số thực x có f(x) = 3.
    2. Viết điều kiện đó thành phương trình x^2 - 1 = 3.
    3. Chuyển vế: x^2 = 4.
    4. Giải ra x = 2 hoặc x = -2.
    5. Vậy tạo ảnh của {3} là {-2, 2}.
  - **Lời giải:**
    1. Tạo ảnh của một tập Y là tập các x có f(x) thuộc Y; ở đây Y chỉ có số 3.
    2. f(x) = 3 nghĩa là x^2 - 1 = 3, tức x^2 = 4.
    3. Phương trình có hai nghiệm 2 và -2, nên tạo ảnh là {-2, 2}.
- `dstt_t1_ax_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm f(A) với f(x) = x^2 từ R vào R và A = {-2, -1, 0, 1, 2}. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ảnh của từng phần tử: f(-2) = 4, f(-1) = 1, f(0) = 0, f(1) = 1, f(2) = 4.
    2. Mỗi phần tử của A cho một ảnh và A có 5 phần tử, nên f(A) có đúng 5 phần tử.   **<- bước sai đầu tiên**
    3. Vậy f(A) = {4, 1, 0, 1, 4}, gồm 5 phần tử.
  - **Đáp án:** Bước 2: Mỗi phần tử của A cho một ảnh và A có 5 phần tử, nên f(A) có đúng 5 phần tử.
  - **Vì sao sai, và bước đúng:**
    1. Hai phần tử khác nhau được phép chung một ảnh, nên f(A) có thể ít phần tử hơn A. Ở đây f(-2) = f(2) và f(-1) = f(1).
    2. Đúng ra: trong một tập mỗi phần tử chỉ viết một lần, f(A) = {0, 1, 4}, gồm 3 phần tử.
- `dstt_g1_anh_tap` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2 - 1 và A = {-3, -2, 0, 3}. Liệt kê các phần tử của ảnh f(A).
  - **Đáp án:** -1, 3, 8  (thứ tự nào cũng được)
    1. f(A) gồm ảnh của mọi phần tử thuộc A.
    2. f(-3) = 8; f(-2) = 3; f(0) = -1; f(3) = 8.
    3. Mỗi giá trị chỉ viết một lần: f(A) = {-1, 3, 8}.
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2 - 3 và A = {-2, -1, 0, 1}. Liệt kê các phần tử của ảnh f(A).
  - **Đáp án:** -3, -2, 1  (thứ tự nào cũng được)
    1. f(A) gồm ảnh của mọi phần tử thuộc A.
    2. f(-2) = 1; f(-1) = -2; f(0) = -3; f(1) = -2.
    3. Mỗi giá trị chỉ viết một lần: f(A) = {-3, -2, 1}.
  - **Câu hỏi:** Cho f: R -> R, f(x) = x^2 và A = {-3, 0, 1, 3}. Liệt kê các phần tử của ảnh f(A).
  - **Đáp án:** 0, 1, 9  (thứ tự nào cũng được)
    1. f(A) gồm ảnh của mọi phần tử thuộc A.
    2. f(-3) = 9; f(0) = 0; f(1) = 1; f(3) = 9.
    3. Mỗi giá trị chỉ viết một lần: f(A) = {0, 1, 9}.

### Đơn ánh, toàn ánh, song ánh (`dstt_t1_don_toan_song_anh`)

- `dstt_t1_ds_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ f: R -> R, f(x) = x^2 là đơn ánh.
  - **Đáp án:** Sai
    1. Đơn ánh nghĩa là hai phần tử khác nhau luôn có ảnh khác nhau.
    2. Ở đây f(1) = f(-1) = 1 dù 1 khác -1.
    3. Vậy f không phải là đơn ánh.
- `dstt_t1_ds_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ f: A -> B là toàn ánh khi nào?
    - **(đúng)** Mỗi phần tử của B là ảnh của ít nhất một phần tử của A
    - Hai phần tử khác nhau của A luôn có ảnh khác nhau
    - Mỗi phần tử của A có đúng một ảnh trong B
    - A và B có cùng số phần tử
  - **Đáp án:** Mỗi phần tử của B là ảnh của ít nhất một phần tử của A
    1. Toàn ánh nghĩa là ảnh f(A) phủ kín B: phần tử nào của B cũng là ảnh của ít nhất một phần tử của A.
    2. Hai phần tử khác nhau có ảnh khác nhau là định nghĩa của đơn ánh.
    3. Mỗi phần tử của A có đúng một ảnh là điều ánh xạ nào cũng có.
- `dstt_g1_don_anh` · bậc 1 (Nhập môn) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ f: R -> R, f(x) = x^2 + 9 là đơn ánh.
  - **Đáp án:** Sai
    1. f(1) = f(-1) = 10 dù 1 khác -1.
    2. Có hai phần tử khác nhau cùng một ảnh, nên f không phải là đơn ánh.
  - **Câu hỏi:** Ánh xạ f: R -> R, f(x) = -4x - 7 là đơn ánh.
  - **Đáp án:** Đúng
    1. Nếu f(u) = f(v) thì -4u - 7 = -4v - 7, suy ra u = v.
    2. Hai phần tử khác nhau luôn có ảnh khác nhau, nên f là đơn ánh.
  - **Câu hỏi:** Ánh xạ f: R -> R, f(x) = x^2 + 9 là đơn ánh.
  - **Đáp án:** Sai
    1. f(1) = f(-1) = 10 dù 1 khác -1.
    2. Có hai phần tử khác nhau cùng một ảnh, nên f không phải là đơn ánh.
- `dstt_t1_ds_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ f: R -> R, f(x) = 2x + 3 thuộc loại nào?
    - **(đúng)** Song ánh
    - Đơn ánh nhưng không toàn ánh
    - Toàn ánh nhưng không đơn ánh
    - Không đơn ánh, không toàn ánh
  - **Đáp án:** Song ánh
    1. Đơn ánh: nếu 2a + 3 = 2b + 3 thì a = b.
    2. Toàn ánh: với mọi y, phương trình 2x + 3 = y có nghiệm x = (y - 3)/2.
    3. f vừa đơn ánh vừa toàn ánh nên là song ánh.
- `dstt_t1_ds_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu song ánh từ tập {1, 2, 3} vào chính nó?
  - **Đáp án:** 6
    1. Một song ánh từ {1, 2, 3} vào chính nó xếp ba ảnh khác nhau cho 1, 2, 3.
    2. Ảnh của 1 có 3 cách chọn, ảnh của 2 còn 2 cách, ảnh của 3 còn 1 cách.
    3. Số song ánh là 3 . 2 . 1 = 6.
- `dstt_t1_ds_05` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi ánh xạ dưới đây đi từ R vào R. Ghép mỗi ánh xạ với tính chất đúng của nó.
  - **Đáp án (ghép đúng):**
    - f(x) = 2x + 1 — song ánh
    - f(x) = x^2 — không đơn ánh, không toàn ánh
    - f(x) = e^x — đơn ánh nhưng không toàn ánh
    - f(x) = x^3 - x — toàn ánh nhưng không đơn ánh
  - **Lời giải:**
    1. 2x + 1 = y có đúng một nghiệm x = (y - 1)/2 với mọi y, nên f(x) = 2x + 1 là song ánh.
    2. x^2: f(1) = f(-1) nên không đơn ánh; số -1 không là ảnh của số nào nên không toàn ánh.
    3. e^x: hàm tăng nên đơn ánh, nhưng e^x luôn dương nên số 0 và các số âm không là ảnh, do đó không toàn ánh.
    4. x^3 - x: f(0) = f(1) = 0 nên không đơn ánh; là đa thức bậc ba nên nhận mọi giá trị thực, do đó toàn ánh.
- `dstt_g1_dem_don_anh` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Có bao nhiêu đơn ánh từ một tập có 2 phần tử vào một tập có 6 phần tử?
  - **Đáp án:** 30
    1. Ảnh của phần tử thứ nhất có 6 cách chọn.
    2. Đơn ánh không cho hai phần tử chung một ảnh, nên mỗi phần tử tiếp theo có ít hơn một cách chọn.
    3. Số đơn ánh là 6 . 5 = 30.
  - **Câu hỏi:** Có bao nhiêu đơn ánh từ một tập có 2 phần tử vào một tập có 2 phần tử?
  - **Đáp án:** 2
    1. Ảnh của phần tử thứ nhất có 2 cách chọn.
    2. Đơn ánh không cho hai phần tử chung một ảnh, nên mỗi phần tử tiếp theo có ít hơn một cách chọn.
    3. Số đơn ánh là 2 . 1 = 2.
  - **Câu hỏi:** Có bao nhiêu đơn ánh từ một tập có 2 phần tử vào một tập có 6 phần tử?
  - **Đáp án:** 30
    1. Ảnh của phần tử thứ nhất có 6 cách chọn.
    2. Đơn ánh không cho hai phần tử chung một ảnh, nên mỗi phần tử tiếp theo có ít hơn một cách chọn.
    3. Số đơn ánh là 6 . 5 = 30.

### Ánh xạ hợp và ánh xạ ngược (`dstt_t1_hop_va_nguoc`)

- `dstt_t1_hn_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x + 1 và g(x) = 2x. Tính g(f(3)).
  - **Đáp án:** 8
    1. Tính từ trong ra ngoài: f(3) = 3 + 1 = 4.
    2. g(f(3)) = g(4) = 2 . 4 = 8.
- `dstt_t1_hn_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ nào cũng có ánh xạ ngược.
  - **Đáp án:** Sai
    1. Chỉ song ánh mới có ánh xạ ngược.
    2. Ví dụ f: R -> R, f(x) = x^2 không có ánh xạ ngược vì f(1) = f(-1), và số -1 không là ảnh của số nào.
- `dstt_g1_hop_thanh` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = -2x + 3 và g(x) = -3x - 2. Tính g(f(-3)).
  - **Đáp án:** -29
    1. Tính từ trong ra ngoài: f(-3) = 9.
    2. g(f(-3)) = g(9) = -29.
  - **Câu hỏi:** Cho f(x) = -4x - 5 và g(x) = -3x - 1. Tính g(f(-2)).
  - **Đáp án:** -10
    1. Tính từ trong ra ngoài: f(-2) = 3.
    2. g(f(-2)) = g(3) = -10.
  - **Câu hỏi:** Cho f(x) = -x + 3 và g(x) = -2x - 1. Tính g(f(3)).
  - **Đáp án:** -1
    1. Tính từ trong ra ngoài: f(3) = 0.
    2. g(f(3)) = g(0) = -1.
- `dstt_t1_hn_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho song ánh f: R -> R, f(x) = 2x + 1. Tìm x sao cho f(x) = 7, tức là giá trị của ánh xạ ngược tại 7.
  - **Đáp án:** 3
    1. Giải phương trình 2x + 1 = 7.
    2. 2x = 6 nên x = 3.
    3. Ánh xạ ngược của f nhận giá trị 3 tại 7.
- `dstt_t1_hn_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x) = x^2 và g(x) = x + 1. Tính f(g(2)) - g(f(2)).
  - **Đáp án:** 4
    1. f(g(2)) = f(3) = 9.
    2. g(f(2)) = g(4) = 5.
    3. Hiệu là 9 - 5 = 4, cho thấy đổi thứ tự hợp thành thì kết quả có thể khác.
- `dstt_t1_hn_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho song ánh f: R -> R, f(x) = 3x - 2. Sắp xếp các bước tìm ánh xạ ngược g của f.
  - **Đáp án (thứ tự đúng):**
    1. Đặt y = 3x - 2 và tìm x theo y.
    2. Chuyển -2 sang vế trái: 3x = y + 2.
    3. Chia hai vế cho 3: x = (y + 2)/3.
    4. Vậy g(y) = (y + 2)/3, viết lại theo biến x là g(x) = (x + 2)/3.
    5. Thử lại: f(g(x)) = 3 . (x + 2)/3 - 2 = x.
  - **Lời giải:**
    1. Ánh xạ ngược đưa mỗi y về đúng số x có f(x) = y, nên ta giải phương trình y = 3x - 2 theo x.
    2. 3x = y + 2, rồi x = (y + 2)/3.
    3. Do đó g(x) = (x + 2)/3; thay vào f thấy f(g(x)) = x, đúng như mong đợi.
- `dstt_g1_nguoc` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho song ánh f: R -> R, f(x) = -3x + 9. Tìm x sao cho f(x) = 12, tức là giá trị của ánh xạ ngược tại 12.
  - **Đáp án:** -1
    1. Giải phương trình -3x + 9 = 12.
    2. -3x = 3 nên x = -1.
    3. Ánh xạ ngược của f nhận giá trị -1 tại 12.
  - **Câu hỏi:** Cho song ánh f: R -> R, f(x) = -5x - 7. Tìm x sao cho f(x) = -10, tức là giá trị của ánh xạ ngược tại -10.
  - **Đáp án:** 3/5
    1. Giải phương trình -5x - 7 = -10.
    2. -5x = -3 nên x = 3/5.
    3. Ánh xạ ngược của f nhận giá trị 3/5 tại -10.
  - **Câu hỏi:** Cho song ánh f: R -> R, f(x) = -2x + 9. Tìm x sao cho f(x) = 5, tức là giá trị của ánh xạ ngược tại 5.
  - **Đáp án:** 2
    1. Giải phương trình -2x + 9 = 5.
    2. -2x = -4 nên x = 2.
    3. Ánh xạ ngược của f nhận giá trị 2 tại 5.

## Tầng 2: Số phức

42 dạng câu (30 câu viết tay, 12 bộ sinh câu); 42 chưa duyệt.

### Dạng đại số của số phức (`dstt_t2_dang_dai_so`)

- `dstt_t2_ds_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số phức z = 5 có phần ảo bằng 0.
  - **Đáp án:** Đúng
    1. Viết z = 5 ở dạng a + bi: z = 5 + 0i.
    2. Hệ số của i là 0, nên phần ảo của z bằng 0. Mọi số thực đều là số phức có phần ảo bằng 0.
- `dstt_t2_ds_02` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đơn vị ảo i thỏa mãn i^2 bằng bao nhiêu?
    - **(đúng)** -1
    - 1
    - i
    - -i
  - **Đáp án:** -1
    1. Đơn vị ảo i được định nghĩa bởi tính chất i^2 = -1.
    2. Không có số thực nào có bình phương âm, vì vậy i không phải là số thực.
- `dstt_t2_ds_05` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi số phức với phần thực và phần ảo của nó.
  - **Đáp án (ghép đúng):**
    - z = 3 - 2i — phần thực 3, phần ảo -2
    - z = -2 + 3i — phần thực -2, phần ảo 3
    - z = 3i — phần thực 0, phần ảo 3
    - z = -2 — phần thực -2, phần ảo 0
  - **Lời giải:**
    1. Với z = a + bi (a, b thực), phần thực là a, phần ảo là b; phần ảo là số thực b, không kèm i.
    2. 3 - 2i có a = 3, b = -2. -2 + 3i có a = -2, b = 3.
    3. 3i = 0 + 3i có a = 0, b = 3. -2 = -2 + 0i có a = -2, b = 0.
- `dstt_g2_phan_thuc_ao` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho số phức z = -5 - 7i. Phần ảo của z bằng bao nhiêu?
  - **Đáp án:** -7
    1. Viết z ở dạng a + bi với a = -5 và b = -7.
    2. Phần thực là a; phần ảo là b, tức là hệ số của i (không kèm i).
    3. Phần ảo của z là -7.
  - **Câu hỏi:** Cho số phức z = -8 - 7i. Phần thực của z bằng bao nhiêu?
  - **Đáp án:** -8
    1. Viết z ở dạng a + bi với a = -8 và b = -7.
    2. Phần thực là a; phần ảo là b, tức là hệ số của i (không kèm i).
    3. Phần thực của z là -8.
  - **Câu hỏi:** Cho số phức z = -2 + 9i. Phần thực của z bằng bao nhiêu?
  - **Đáp án:** -2
    1. Viết z ở dạng a + bi với a = -2 và b = 9.
    2. Phần thực là a; phần ảo là b, tức là hệ số của i (không kèm i).
    3. Phần thực của z là -2.
- `dstt_t2_ds_03` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai số phức bằng nhau khi và chỉ khi chúng có cùng phần thực và cùng phần ảo.
  - **Đáp án:** Đúng
    1. Mỗi số phức viết được theo đúng một cách ở dạng a + bi với a, b là số thực.
    2. Vì vậy a + bi = c + di khi và chỉ khi a = c và b = d.
- `dstt_t2_ds_04` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số nào sau đây là số thuần ảo?
    - **(đúng)** -4i
    - 3
    - 2 + i
    - 1 - i
  - **Đáp án:** -4i
    1. Số thuần ảo là số phức có phần thực bằng 0 và phần ảo khác 0.
    2. -4i = 0 - 4i có phần thực 0 và phần ảo -4.
    3. Ba số còn lại đều có phần thực khác 0.
- `dstt_t2_ds_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm phần ảo của z = 3 - 4i rồi bình phương nó. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Viết z = 3 + (-4)i, nên phần thực của z là 3.
    2. Phần ảo là cả cụm đứng trước dấu của i, tức là phần ảo của z là -4i.   **<- bước sai đầu tiên**
    3. Bình phương phần ảo: (-4i)^2 = 16 i^2 = -16.
  - **Đáp án:** Bước 2: Phần ảo là cả cụm đứng trước dấu của i, tức là phần ảo của z là -4i.
  - **Vì sao sai, và bước đúng:**
    1. Phần ảo là một số thực, là hệ số đứng trước i, chứ không có chữ i trong nó. Phần ảo của 3 - 4i là -4.
    2. Đúng ra: (-4)^2 = 16.
- `dstt_g2_luy_thua_i` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính i^13. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 1
    1. Lũy thừa của i lặp lại theo chu kỳ 4: i^1 = i, i^2 = -1, i^3 = -i, i^4 = 1.
    2. 13 chia 4 dư 1, nên i^13 = i^1 = i.
    3. Phần thực là 0, phần ảo là 1.
  - **Câu hỏi:** Tính i^60. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 0
    1. Lũy thừa của i lặp lại theo chu kỳ 4: i^1 = i, i^2 = -1, i^3 = -i, i^4 = 1.
    2. 60 chia hết cho 4, nên i^60 = 1.
    3. Phần thực là 1, phần ảo là 0.
  - **Câu hỏi:** Tính i^20. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 0
    1. Lũy thừa của i lặp lại theo chu kỳ 4: i^1 = i, i^2 = -1, i^3 = -i, i^4 = 1.
    2. 20 chia hết cho 4, nên i^20 = 1.
    3. Phần thực là 1, phần ảo là 0.

### Cộng, trừ, nhân số phức (`dstt_t2_cong_nhan`)

- `dstt_t2_cn_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tổng (2 + 3i) + (1 - 3i) là một số thực.
  - **Đáp án:** Đúng
    1. Cộng phần thực: 2 + 1 = 3. Cộng phần ảo: 3 + (-3) = 0.
    2. Tổng là 3, có phần ảo bằng 0, nên là một số thực.
- `dstt_t2_cn_04` · bậc 1 (Nhập môn) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tính tích (2 + 3i)(1 - i).
  - **Đáp án (thứ tự đúng):**
    1. Nhân phân phối: (2 + 3i)(1 - i) = 2 - 2i + 3i - 3i^2.
    2. Thay i^2 = -1: được 2 - 2i + 3i + 3.
    3. Gộp phần thực và phần ảo: (2 + 3) + (-2 + 3)i.
    4. Kết quả là 5 + i.
  - **Lời giải:**
    1. Nhân từng số hạng của ngoặc thứ nhất với từng số hạng của ngoặc thứ hai: 2 . 1, 2 . (-i), 3i . 1, 3i . (-i).
    2. Số hạng -3i^2 bằng +3 vì i^2 = -1.
    3. Phần thực 2 + 3 = 5, phần ảo -2 + 3 = 1, nên tích là 5 + i.
- `dstt_g2_cong_tru` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho z = -5 - 7i và w = -1 - 6i. Tính z - w. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -4, -1
    1. Trừ riêng phần thực với phần thực, phần ảo với phần ảo.
    2. Phần thực: (-5) - (-1) = -4. Phần ảo: (-7) - (-6) = -1.
    3. z - w = -4 - i.
  - **Câu hỏi:** Cho z = -8 - 7i và w = -7 + 3i. Tính z + w. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -15, -4
    1. Cộng riêng phần thực với phần thực, phần ảo với phần ảo.
    2. Phần thực: (-8) + (-7) = -15. Phần ảo: (-7) + 3 = -4.
    3. z + w = -15 - 4i.
  - **Câu hỏi:** Cho z = -2 + 9i và w = -5 + 3i. Tính z - w. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 3, 6
    1. Trừ riêng phần thực với phần thực, phần ảo với phần ảo.
    2. Phần thực: (-2) - (-5) = 3. Phần ảo: 9 - 3 = 6.
    3. z - w = 3 + 6i.
- `dstt_t2_cn_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số phức z và w, ta có zw = wz.
  - **Đáp án:** Đúng
    1. Với z = a + bi và w = c + di: zw = (ac - bd) + (ad + bc)i.
    2. Đổi chỗ z và w thì được (ca - db) + (cb + da)i, vẫn là số đó.
    3. Phép nhân số phức có tính giao hoán.
- `dstt_t2_cn_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính (1 + i)^2. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 2
    1. (1 + i)^2 = 1 + 2i + i^2.
    2. Vì i^2 = -1 nên kết quả là 1 + 2i - 1 = 2i.
    3. Phần thực là 0, phần ảo là 2.
- `dstt_g2_nhan` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính (-3 + 5i)(-4 - i). Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 17, -17
    1. Nhân từng số hạng. Không chứa i: (-3) . (-4) = 12. Chứa i: (-3) . (-1) + 5 . (-4) = -17. Chứa i^2: 5 . (-1) = -5.
    2. Vì i^2 = -1, số hạng chứa i^2 đổi dấu rồi nhập vào phần thực: 12 - (-5) = 17.
    3. Kết quả: 17 - 17i.
  - **Câu hỏi:** Tính (-5 - 4i)(-4 + i). Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 24, 11
    1. Nhân từng số hạng. Không chứa i: (-5) . (-4) = 20. Chứa i: (-5) . 1 + (-4) . (-4) = 11. Chứa i^2: (-4) . 1 = -4.
    2. Vì i^2 = -1, số hạng chứa i^2 đổi dấu rồi nhập vào phần thực: 20 - (-4) = 24.
    3. Kết quả: 24 + 11i.
  - **Câu hỏi:** Tính (-2 + 5i)(4 - 3i). Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 7, 26
    1. Nhân từng số hạng. Không chứa i: (-2) . 4 = -8. Chứa i: (-2) . (-3) + 5 . 4 = 26. Chứa i^2: 5 . (-3) = -15.
    2. Vì i^2 = -1, số hạng chứa i^2 đổi dấu rồi nhập vào phần thực: -8 - (-15) = 7.
    3. Kết quả: 7 + 26i.

### Số phức liên hợp và môđun (`dstt_t2_lien_hop_modun`)

- `dstt_t2_lh_01` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số phức liên hợp của z = 3 - 4i là số nào?
    - **(đúng)** 3 + 4i
    - -3 - 4i
    - -3 + 4i
    - 4 - 3i
  - **Đáp án:** 3 + 4i
    1. Số phức liên hợp của a + bi là a - bi: giữ phần thực, đổi dấu phần ảo.
    2. Với z = 3 - 4i, phần thực 3 giữ nguyên, phần ảo -4 đổi thành 4.
    3. Số phức liên hợp là 3 + 4i.
- `dstt_t2_lh_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Môđun của một số phức luôn là một số thực không âm.
  - **Đáp án:** Đúng
    1. Môđun của a + bi là căn bậc hai của a^2 + b^2.
    2. a^2 + b^2 là số thực không âm, nên căn bậc hai của nó là số thực không âm.
    3. Về hình học, môđun là khoảng cách từ điểm biểu diễn z đến gốc tọa độ.
- `dstt_t2_lh_05` · bậc 1 (Nhập môn) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi số phức với môđun của nó.
  - **Đáp án (ghép đúng):**
    - 3 + 4i — 5
    - 5 - 12i — 13
    - -6 + 8i — 10
    - -2i — 2
  - **Lời giải:**
    1. Môđun của a + bi là căn bậc hai của a^2 + b^2.
    2. 3^2 + 4^2 = 25 nên môđun là 5. 5^2 + 12^2 = 169 nên môđun là 13.
    3. 6^2 + 8^2 = 100 nên môđun là 10. -2i = 0 - 2i có 0^2 + 2^2 = 4 nên môđun là 2.
- `dstt_g2_modun` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính môđun của số phức z = 5 - 12i.
  - **Đáp án:** 13
    1. Môđun của z = a + bi là căn bậc hai của a^2 + b^2.
    2. a^2 + b^2 = 25 + 144 = 169.
    3. |z| = 13.
  - **Câu hỏi:** Tính môđun của số phức z = -4 + 3i.
  - **Đáp án:** 5
    1. Môđun của z = a + bi là căn bậc hai của a^2 + b^2.
    2. a^2 + b^2 = 16 + 9 = 25.
    3. |z| = 5.
  - **Câu hỏi:** Tính môđun của số phức z = 8 - 15i.
  - **Đáp án:** 17
    1. Môđun của z = a + bi là căn bậc hai của a^2 + b^2.
    2. a^2 + b^2 = 64 + 225 = 289.
    3. |z| = 17.
- `dstt_t2_lh_03` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên mặt phẳng phức, điểm biểu diễn z và điểm biểu diễn số phức liên hợp của z đối xứng nhau qua trục thực.
  - **Đáp án:** Đúng
    1. z = a + bi được biểu diễn bởi điểm (a, b).
    2. Số phức liên hợp a - bi được biểu diễn bởi điểm (a, -b).
    3. Hai điểm (a, b) và (a, -b) đối xứng nhau qua trục hoành, tức là trục thực.
- `dstt_t2_lh_04` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi số phức z và w, ta có |z + w| = |z| + |w|.
  - **Đáp án:** Sai
    1. Chỉ cần một ví dụ để bác bỏ: lấy z = 1 và w = -1.
    2. |z + w| = |0| = 0, còn |z| + |w| = 1 + 1 = 2.
    3. Nói chung chỉ có bất đẳng thức |z + w| nhỏ hơn hoặc bằng |z| + |w|.
- `dstt_g2_lien_hop` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho z = -5 + 3i. Tính tích của z với số phức liên hợp của nó.
  - **Đáp án:** 34
    1. Số phức liên hợp của z là -5 - 3i.
    2. Tích của a + bi với a - bi bằng a^2 + b^2.
    3. 25 + 9 = 34.
  - **Câu hỏi:** Cho z = 7 + 7i. Tính tích của z với số phức liên hợp của nó.
  - **Đáp án:** 98
    1. Số phức liên hợp của z là 7 - 7i.
    2. Tích của a + bi với a - bi bằng a^2 + b^2.
    3. 49 + 49 = 98.
  - **Câu hỏi:** Cho z = -4 + 3i. Tính tích của z với số phức liên hợp của nó.
  - **Đáp án:** 25
    1. Số phức liên hợp của z là -4 - 3i.
    2. Tích của a + bi với a - bi bằng a^2 + b^2.
    3. 16 + 9 = 25.

### Chia số phức (`dstt_t2_chia`)

- `dstt_t2_ch_01` · bậc 1 (Nhập môn) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính 1 / i. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, -1
    1. Nhân cả tử và mẫu với -i: mẫu thành i . (-i) = 1.
    2. Tử thành 1 . (-i) = -i.
    3. 1 / i = -i: phần thực là 0, phần ảo là -1.
- `dstt_t2_ch_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Để chia hai số phức, ta có thể nhân cả tử và mẫu với số phức liên hợp của mẫu.
  - **Đáp án:** Đúng
    1. Nhân cả tử và mẫu với cùng một số khác 0 thì thương không đổi.
    2. Mẫu nhân với số phức liên hợp của nó thành a^2 + b^2, là một số thực dương.
    3. Khi mẫu đã là số thực, chỉ còn việc chia phần thực và phần ảo của tử cho số đó.
- `dstt_g2_chia_i` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính (-5 - 7i) / i. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -7, 5
    1. Nhân cả tử và mẫu với -i, là số phức liên hợp của i: mẫu thành i . (-i) = 1.
    2. Tử thành (-5 - 7i) . (-i) = -7 + 5i.
    3. Phần thực là -7, phần ảo là 5.
  - **Câu hỏi:** Tính (-8 - 7i) / i. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -7, 8
    1. Nhân cả tử và mẫu với -i, là số phức liên hợp của i: mẫu thành i . (-i) = 1.
    2. Tử thành (-8 - 7i) . (-i) = -7 + 8i.
    3. Phần thực là -7, phần ảo là 8.
  - **Câu hỏi:** Tính (-2 + 9i) / i. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 9, 2
    1. Nhân cả tử và mẫu với -i, là số phức liên hợp của i: mẫu thành i . (-i) = 1.
    2. Tử thành (-2 + 9i) . (-i) = 9 + 2i.
    3. Phần thực là 9, phần ảo là 2.
- `dstt_t2_ch_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nghịch đảo của z = 1 + i, tức là 1 / (1 + i), là số nào?
    - **(đúng)** 1/2 - (1/2)i
    - 1 - i
    - 1/2 + (1/2)i
    - -1 - i
  - **Đáp án:** 1/2 - (1/2)i
    1. Nhân cả tử và mẫu với số phức liên hợp của mẫu là 1 - i.
    2. Mẫu: (1 + i)(1 - i) = 1 + 1 = 2. Tử: 1 - i.
    3. 1 / (1 + i) = (1 - i)/2 = 1/2 - (1/2)i.
- `dstt_t2_ch_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phép chia số phức với kết quả của nó.
  - **Đáp án (ghép đúng):**
    - (2 + 4i) / 2 — 1 + 2i
    - 2 / i — -2i
    - (1 + i) / (1 - i) — i
    - 5 / (2 + i) — 2 - i
    - 10 / (1 - 3i) — 1 + 3i
  - **Lời giải:**
    1. Chia cho số thực 2: chia cả phần thực lẫn phần ảo, được 1 + 2i.
    2. 2 / i: nhân tử và mẫu với -i, được -2i / 1 = -2i.
    3. (1 + i) / (1 - i): nhân tử và mẫu với 1 + i, được (1 + i)^2 / 2 = 2i / 2 = i.
    4. 5 / (2 + i): nhân với 2 - i, được 5(2 - i) / 5 = 2 - i.
    5. 10 / (1 - 3i): nhân với 1 + 3i, được 10(1 + 3i) / 10 = 1 + 3i.
- `dstt_t2_ch_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính (1 + 2i) / (3 - i). Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Mẫu là 3 - i, tử là 1 + 2i; cần làm cho mẫu hết phần ảo.
    2. Nhân cả tử và mẫu với liên hợp của tử, tức là với 1 - 2i.   **<- bước sai đầu tiên**
    3. Tử: (1 + 2i)(1 - 2i) = 1 + 4 = 5.
    4. Mẫu: (3 - i)(1 - 2i) = 3 - 6i - i + 2i^2 = 1 - 7i.
  - **Đáp án:** Bước 2: Nhân cả tử và mẫu với liên hợp của tử, tức là với 1 - 2i.
  - **Vì sao sai, và bước đúng:**
    1. Mục đích là làm mẫu hết phần ảo, nên phải nhân với liên hợp của mẫu. Nhân với liên hợp của tử không làm mẫu thành số thực, như bước 4 cho thấy.
    2. Đúng ra: nhân với 3 + i. Tử (1 + 2i)(3 + i) = 3 + i + 6i + 2i^2 = 1 + 7i, mẫu (3 - i)(3 + i) = 10. Vậy kết quả là (1 + 7i)/10.
- `dstt_g2_chia` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính (-4 + 4i) / (-3 + i). Nhập phần thực và phần ảo (có thể là phân số), cách nhau bằng dấu phẩy.
  - **Đáp án:** 8/5, -4/5
    1. Nhân cả tử và mẫu với số phức liên hợp của mẫu là -3 - i.
    2. Mẫu: 9 + 1 = 10.
    3. Tử: (-4 + 4i)(-3 - i) = 16 - 8i.
    4. Chia cho 10: phần thực 8/5, phần ảo -4/5.
  - **Câu hỏi:** Tính (-6 - 5i) / (-3 + 2i). Nhập phần thực và phần ảo (có thể là phân số), cách nhau bằng dấu phẩy.
  - **Đáp án:** 8/13, 27/13
    1. Nhân cả tử và mẫu với số phức liên hợp của mẫu là -3 - 2i.
    2. Mẫu: 9 + 4 = 13.
    3. Tử: (-6 - 5i)(-3 - 2i) = 8 + 27i.
    4. Chia cho 13: phần thực 8/13, phần ảo 27/13.
  - **Câu hỏi:** Tính (-3 + 4i) / (-2 + 2i). Nhập phần thực và phần ảo (có thể là phân số), cách nhau bằng dấu phẩy.
  - **Đáp án:** 7/4, -1/4
    1. Nhân cả tử và mẫu với số phức liên hợp của mẫu là -2 - 2i.
    2. Mẫu: 4 + 4 = 8.
    3. Tử: (-3 + 4i)(-2 - 2i) = 14 - 2i.
    4. Chia cho 8: phần thực 7/4, phần ảo -1/4.

### Dạng lượng giác và công thức Moivre (`dstt_t2_dang_luong_giac`)

- `dstt_t2_lg_01` · bậc 1 (Nhập môn) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số phức z = i có môđun và acgumen là bao nhiêu?
    - **(đúng)** Môđun 1, acgumen 90 độ
    - Môđun 1, acgumen 0 độ
    - Môđun 0, acgumen 90 độ
    - Môđun 1, acgumen 180 độ
  - **Đáp án:** Môđun 1, acgumen 90 độ
    1. z = i được biểu diễn bởi điểm (0, 1).
    2. Khoảng cách từ điểm đó đến gốc tọa độ là 1, nên môđun bằng 1.
    3. Điểm đó nằm trên tia dương của trục ảo, nên acgumen là 90 độ.
- `dstt_g2_acgumen` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm acgumen của số phức z = 5i, tính bằng độ, trong khoảng từ 0 đến dưới 360.
  - **Đáp án:** 90
    1. Điểm biểu diễn z trên mặt phẳng phức là (0, 5).
    2. Điểm này nằm trên tia dương của trục ảo.
    3. Góc quay từ tia dương của trục thực đến tia đó là 90 độ.
  - **Câu hỏi:** Tìm acgumen của số phức z = 1, tính bằng độ, trong khoảng từ 0 đến dưới 360.
  - **Đáp án:** 0
    1. Điểm biểu diễn z trên mặt phẳng phức là (1, 0).
    2. Điểm này nằm trên tia dương của trục thực.
    3. Góc quay từ tia dương của trục thực đến tia đó là 0 độ.
  - **Câu hỏi:** Tìm acgumen của số phức z = -5 + 5i, tính bằng độ, trong khoảng từ 0 đến dưới 360.
  - **Đáp án:** 135
    1. Điểm biểu diễn z trên mặt phẳng phức là (-5, 5).
    2. Điểm này nằm trên tia phân giác của góc phần tư thứ hai.
    3. Góc quay từ tia dương của trục thực đến tia đó là 135 độ.
- `dstt_t2_lg_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi nhân hai số phức ở dạng lượng giác, môđun nhân với nhau còn acgumen cộng với nhau.
  - **Đáp án:** Đúng
    1. Với z có môđun r, acgumen a và w có môđun s, acgumen b, nhân ra rồi dùng công thức cộng của cos và sin.
    2. Tích zw có môđun r . s và acgumen a + b.
    3. Đây là lý do dạng lượng giác tiện cho phép nhân và lũy thừa.
- `dstt_t2_lg_03` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số phức z có môđun 2 và acgumen 30 độ. Môđun của z^3 bằng bao nhiêu?
  - **Đáp án:** 8
    1. Theo công thức Moivre, lũy thừa bậc n có môđun bằng môđun ban đầu lũy thừa n.
    2. Môđun của z^3 là 2^3 = 8.
    3. Acgumen của z^3 là 3 . 30 = 90 độ, nhưng câu hỏi chỉ cần môđun.
- `dstt_t2_lg_04` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho z = 2(cos 30 độ + i sin 30 độ). Sắp xếp các bước tính z^3 bằng công thức Moivre.
  - **Đáp án (thứ tự đúng):**
    1. Theo công thức Moivre: z^3 = 2^3 (cos(3 . 30 độ) + i sin(3 . 30 độ)).
    2. Tính ra: z^3 = 8(cos 90 độ + i sin 90 độ).
    3. Thay cos 90 độ = 0 và sin 90 độ = 1: z^3 = 8(0 + i).
    4. Vậy z^3 = 8i.
  - **Lời giải:**
    1. Công thức Moivre: lũy thừa n của r(cos a + i sin a) có môđun r^n và acgumen n . a.
    2. Ở đây r = 2, a = 30 độ, n = 3: môđun 8, acgumen 90 độ.
    3. cos 90 độ = 0, sin 90 độ = 1, nên z^3 = 8i.
- `dstt_t2_lg_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính z^4 với z = 1 + i. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. z = 1 + i có môđun r = sqrt(2) và acgumen 45 độ.
    2. Theo công thức Moivre, z^4 = r^4 (cos 45 + i sin 45), chỉ cần nâng môđun lên lũy thừa 4.   **<- bước sai đầu tiên**
    3. r^4 = 4, nên z^4 = 4(cos 45 + i sin 45) = 2 sqrt(2) + 2 sqrt(2) i.
  - **Đáp án:** Bước 2: Theo công thức Moivre, z^4 = r^4 (cos 45 + i sin 45), chỉ cần nâng môđun lên lũy thừa 4.
  - **Vì sao sai, và bước đúng:**
    1. Công thức Moivre nâng môđun lên lũy thừa n và nhân acgumen với n: z^4 = r^4 (cos 4.45 + i sin 4.45).
    2. Đúng ra: z^4 = 4(cos 180 + i sin 180) = -4. Thử lại: (1 + i)^2 = 2i, nên (1 + i)^4 = (2i)^2 = -4.
- `dstt_g2_moivre` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng dạng lượng giác và công thức Moivre, tính (1 - i)^3. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -2, -2
    1. 1 - i có môđun là căn bậc hai của 2 và acgumen 315 độ.
    2. Theo công thức Moivre, lũy thừa bậc 3 có môđun (căn bậc hai của 2)^3 và acgumen 3 . 315 = 945 độ, cùng hướng với góc 225 độ.
    3. Kết quả: -2 - 2i.
  - **Câu hỏi:** Dùng dạng lượng giác và công thức Moivre, tính (1 + i)^3. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** -2, 2
    1. 1 + i có môđun là căn bậc hai của 2 và acgumen 45 độ.
    2. Theo công thức Moivre, lũy thừa bậc 3 có môđun (căn bậc hai của 2)^3 và acgumen 3 . 45 = 135 độ, cùng hướng với góc 135 độ.
    3. Kết quả: -2 + 2i.
  - **Câu hỏi:** Dùng dạng lượng giác và công thức Moivre, tính (1 - i)^10. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, -32
    1. 1 - i có môđun là căn bậc hai của 2 và acgumen 315 độ.
    2. Theo công thức Moivre, lũy thừa bậc 10 có môđun (căn bậc hai của 2)^10 và acgumen 10 . 315 = 3150 độ, cùng hướng với góc 270 độ.
    3. Kết quả: -32i.

### Căn bậc n của số phức (`dstt_t2_can_bac_n`)

- `dstt_t2_cb_01` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với n là số nguyên dương, mọi số phức khác 0 có đúng n căn bậc n phân biệt.
  - **Đáp án:** Đúng
    1. Viết số đó ở dạng lượng giác với môđun r và acgumen a.
    2. Các căn bậc n có cùng môđun là căn bậc n của r, và có acgumen (a + 360k)/n độ với k = 0, 1, ..., n - 1.
    3. n giá trị của k cho n căn khác nhau.
- `dstt_t2_cb_02` · bậc 1 (Nhập môn) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Số -4 không có căn bậc hai nào trong tập số phức.
  - **Đáp án:** Sai
    1. (2i)^2 = 4 . i^2 = -4 và (-2i)^2 = -4.
    2. Vậy -4 có hai căn bậc hai là 2i và -2i.
    3. Chỉ trong tập số thực thì -4 mới không có căn bậc hai.
- `dstt_g2_so_nghiem` · bậc 1 (Nhập môn) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phương trình z^4 = 3 + 6i có bao nhiêu nghiệm phức phân biệt?
  - **Đáp án:** 4
    1. Nghiệm của phương trình là các căn bậc n của vế phải.
    2. Mọi số phức khác 0 có đúng n căn bậc n phân biệt.
    3. Vế phải khác 0 nên phương trình có 4 nghiệm phân biệt.
  - **Câu hỏi:** Phương trình z^2 = -5 - 5i có bao nhiêu nghiệm phức phân biệt?
  - **Đáp án:** 2
    1. Nghiệm của phương trình là các căn bậc n của vế phải.
    2. Mọi số phức khác 0 có đúng n căn bậc n phân biệt.
    3. Vế phải khác 0 nên phương trình có 2 nghiệm phân biệt.
  - **Câu hỏi:** Phương trình z^5 = 3 + 2i có bao nhiêu nghiệm phức phân biệt?
  - **Đáp án:** 5
    1. Nghiệm của phương trình là các căn bậc n của vế phải.
    2. Mọi số phức khác 0 có đúng n căn bậc n phân biệt.
    3. Vế phải khác 0 nên phương trình có 5 nghiệm phân biệt.
- `dstt_t2_cb_03` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sáu căn bậc sáu của một số phức khác 0 nằm ở đâu trên mặt phẳng phức?
    - **(đúng)** Ở sáu đỉnh của một lục giác đều có tâm là gốc tọa độ
    - Trên một đường thẳng đi qua gốc tọa độ
    - Trên trục thực
    - Ở sáu điểm có cùng phần thực
  - **Đáp án:** Ở sáu đỉnh của một lục giác đều có tâm là gốc tọa độ
    1. Sáu căn có cùng môđun, nên cùng nằm trên một đường tròn có tâm là gốc tọa độ.
    2. Acgumen của hai căn liên tiếp hơn kém nhau 360/6 = 60 độ.
    3. Sáu điểm cách đều nhau trên đường tròn là sáu đỉnh của một lục giác đều.
- `dstt_t2_cb_04` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong bốn căn bậc bốn của 16, liệt kê các căn là số thực.
  - **Đáp án:** -2, 2  (thứ tự nào cũng được)
    1. Bốn căn bậc bốn của 16 có môđun 2 và acgumen 0, 90, 180, 270 độ.
    2. Đó là 2, 2i, -2 và -2i.
    3. Các căn là số thực: 2 và -2.
- `dstt_t2_cb_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm các căn bậc hai của số phức 2i.
  - **Đáp án (thứ tự đúng):**
    1. Gọi một căn bậc hai của 2i là w = x + yi, với x, y là số thực.
    2. Bình phương: w^2 = x^2 - y^2 + 2xyi.
    3. So sánh w^2 với 2i = 0 + 2i: x^2 - y^2 = 0 và 2xy = 2.
    4. Từ xy = 1 thì x, y cùng dấu; kết hợp x^2 = y^2 được y = x, nên x^2 = 1.
    5. Có x = 1 hoặc x = -1, nên hai căn bậc hai của 2i là 1 + i và -1 - i.
  - **Lời giải:**
    1. Hai số phức bằng nhau khi phần thực bằng nhau và phần ảo bằng nhau.
    2. x^2 - y^2 = 0 cho y = x hoặc y = -x; 2xy = 2 loại trường hợp y = -x vì khi đó 2xy = -2x^2 không dương.
    3. Thử lại: (1 + i)^2 = 1 + 2i - 1 = 2i và (-1 - i)^2 = 2i.
- `dstt_g2_can_bac_hai` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Số phức w = -21 + 20i có hai căn bậc hai. Tìm căn có phần thực dương. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 5
    1. Gọi căn cần tìm là x + yi. Bình phương lên: x^2 - y^2 bằng phần thực của w và 2xy bằng phần ảo của w.
    2. x^2 - y^2 = -21 và 2xy = 20. Thêm nữa x^2 + y^2 = |w| = 29.
    3. Suy ra x^2 = 4 và y^2 = 25. Lấy x = 2 dương thì y = 5 để 2xy = 20.
    4. Căn cần tìm là 2 + 5i.
  - **Câu hỏi:** Số phức w = -15 - 8i có hai căn bậc hai. Tìm căn có phần thực dương. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, -4
    1. Gọi căn cần tìm là x + yi. Bình phương lên: x^2 - y^2 bằng phần thực của w và 2xy bằng phần ảo của w.
    2. x^2 - y^2 = -15 và 2xy = -8. Thêm nữa x^2 + y^2 = |w| = 17.
    3. Suy ra x^2 = 1 và y^2 = 16. Lấy x = 1 dương thì y = -4 để 2xy = -8.
    4. Căn cần tìm là 1 - 4i.
  - **Câu hỏi:** Số phức w = -21 + 20i có hai căn bậc hai. Tìm căn có phần thực dương. Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 5
    1. Gọi căn cần tìm là x + yi. Bình phương lên: x^2 - y^2 bằng phần thực của w và 2xy bằng phần ảo của w.
    2. x^2 - y^2 = -21 và 2xy = 20. Thêm nữa x^2 + y^2 = |w| = 29.
    3. Suy ra x^2 = 4 và y^2 = 25. Lấy x = 2 dương thì y = 5 để 2xy = 20.
    4. Căn cần tìm là 2 + 5i.

## Tầng 3: Vectơ trong R^n và ma trận

45 dạng câu (33 câu viết tay, 12 bộ sinh câu); 45 chưa duyệt.

### Vectơ trong R^n (`dstt_t3_vecto_rn`)

- `dstt_t3_vt_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai vectơ u = (1, 2) và v = (1, 2, 0) cộng được với nhau.
  - **Đáp án:** Sai
    1. Phép cộng vectơ cộng từng tọa độ tương ứng, nên hai vectơ phải có cùng số tọa độ.
    2. u thuộc R^2 còn v thuộc R^3.
    3. Hai vectơ khác số chiều không cộng được với nhau.
- `dstt_t3_vt_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vectơ (4, -1, 0, 7) thuộc không gian nào?
    - **(đúng)** R^4
    - R^3
    - R^7
    - R^2
  - **Đáp án:** R^4
    1. Số chiều của vectơ là số tọa độ của nó.
    2. Vectơ này có 4 tọa độ: 4, -1, 0 và 7.
    3. Tọa độ bằng 0 vẫn được tính, nên vectơ thuộc R^4.
- `dstt_t3_vt_04` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho u = (1, -2, 0) và v = (2, 1, -1) trong R^3. Sắp xếp các bước tìm vectơ x sao cho x + 2u = v.
  - **Đáp án (thứ tự đúng):**
    1. Trừ 2u ở cả hai vế: x = v - 2u.
    2. Thay u và v vào: x = (2, 1, -1) - 2(1, -2, 0).
    3. Nhân 2 với từng tọa độ của u: x = (2, 1, -1) - (2, -4, 0).
    4. Trừ từng tọa độ: x = (0, 5, -1).
  - **Lời giải:**
    1. Phương trình vectơ được biến đổi như phương trình số: x = v - 2u.
    2. 2u = (2, -4, 0), rồi v - 2u = (2 - 2, 1 + 4, -1 - 0) = (0, 5, -1).
    3. Thử lại: x + 2u = (0 + 2, 5 - 4, -1 + 0) = (2, 1, -1) = v.
- `dstt_t3_vt_05` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính 3u - 2v với u = (1, 2, 3) và v = (2, -1, 0) trong R^3. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. 3u = (3, 6, 9) và 2v = (4, -2, 0).
    2. Trừ từng tọa độ: 3u - 2v = (3 - 4, 6 - 2, 9 - 0).   **<- bước sai đầu tiên**
    3. Vậy 3u - 2v = (-1, 4, 9).
  - **Đáp án:** Bước 2: Trừ từng tọa độ: 3u - 2v = (3 - 4, 6 - 2, 9 - 0).
  - **Vì sao sai, và bước đúng:**
    1. Tọa độ thứ hai của 2v là -2, nên phải lấy 6 - (-2), không phải 6 - 2. Trừ một số âm là cộng số dương.
    2. Đúng ra: 3u - 2v = (3 - 4, 6 + 2, 9 - 0) = (-1, 8, 9).
- `dstt_g3_to_hop_vecto` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho u = (-3, 4, -4) và v = (-1, -4, 2) trong R^3. Tính u + v. Nhập các tọa độ theo thứ tự, cách nhau bằng dấu phẩy.
  - **Đáp án:** -4, 0, -2
    1. Nhân từng tọa độ: u = (-3, 4, -4) và v = (-1, -4, 2).
    2. Cộng hai vectơ đó theo từng tọa độ tương ứng.
    3. Kết quả: (-4, 0, -2).
  - **Câu hỏi:** Cho u = (-5, -4, -4) và v = (0, -3, 5) trong R^3. Tính -u - v. Nhập các tọa độ theo thứ tự, cách nhau bằng dấu phẩy.
  - **Đáp án:** 5, 7, -1
    1. Nhân từng tọa độ: -u = (5, 4, 4) và -v = (0, 3, -5).
    2. Cộng hai vectơ đó theo từng tọa độ tương ứng.
    3. Kết quả: (5, 7, -1).
  - **Câu hỏi:** Cho u = (-2, 4, 3) và v = (-3, 0, 4) trong R^3. Tính u + 3v. Nhập các tọa độ theo thứ tự, cách nhau bằng dấu phẩy.
  - **Đáp án:** -11, 4, 15
    1. Nhân từng tọa độ: u = (-2, 4, 3) và 3v = (-9, 0, 12).
    2. Cộng hai vectơ đó theo từng tọa độ tương ứng.
    3. Kết quả: (-11, 4, 15).
- `dstt_t3_vt_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi vectơ u, v trong R^n và mọi số thực a, ta có a(u + v) = au + av.
  - **Đáp án:** Đúng
    1. Tọa độ thứ k của a(u + v) là a(u_k + v_k).
    2. Tọa độ thứ k của au + av là au_k + av_k.
    3. Hai số đó bằng nhau theo tính phân phối của số thực, và điều này đúng với mọi k.
- `dstt_g3_vecto_an` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho u = (2, 2, 2) và v = (11, 2, 11) trong R^3. Tìm vectơ x thỏa mãn -3x + u = v. Nhập các tọa độ của x, cách nhau bằng dấu phẩy.
  - **Đáp án:** -3, 0, -3
    1. Chuyển u sang vế phải: -3x = v - u = (9, 0, 9).
    2. Chia từng tọa độ cho -3: x = (-3, 0, -3).
  - **Câu hỏi:** Cho u = (-3, 5, -1) và v = (9, 17, -5) trong R^3. Tìm vectơ x thỏa mãn -4x + u = v. Nhập các tọa độ của x, cách nhau bằng dấu phẩy.
  - **Đáp án:** -3, -3, 1
    1. Chuyển u sang vế phải: -4x = v - u = (12, 12, -4).
    2. Chia từng tọa độ cho -4: x = (-3, -3, 1).
  - **Câu hỏi:** Cho u = (4, 2, 5) và v = (-8, 8, 2) trong R^3. Tìm vectơ x thỏa mãn -3x + u = v. Nhập các tọa độ của x, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, -2, 1
    1. Chuyển u sang vế phải: -3x = v - u = (-12, 6, -3).
    2. Chia từng tọa độ cho -3: x = (4, -2, 1).

### Kích thước ma trận và phần tử a_ij (`dstt_t3_kich_thuoc_phan_tu`)

- `dstt_t3_kt_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một ma trận có 2 hàng và 3 cột có cỡ là gì?
    - **(đúng)** 2 x 3
    - 3 x 2
    - 6 x 1
    - 2 x 2
  - **Đáp án:** 2 x 3
    1. Cỡ của ma trận được viết là số hàng x số cột.
    2. Ma trận có 2 hàng và 3 cột nên có cỡ 2 x 3.
- `dstt_t3_kt_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong ký hiệu a_ij, chỉ số i là số thứ tự của hàng và j là số thứ tự của cột.
  - **Đáp án:** Đúng
    1. Quy ước chung: chỉ số thứ nhất chỉ hàng, chỉ số thứ hai chỉ cột.
    2. Ví dụ a_23 là phần tử ở hàng 2, cột 3.
- `dstt_t3_kt_04` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Ghép mỗi phần tử của A với giá trị của nó.
  - A = (7, -1, 0); (2, 5, 9)  (từng hàng)
  - **Đáp án (ghép đúng):**
    - a_12 — -1
    - a_21 — 2
    - a_13 — 0
    - a_23 — 9
    - a_22 — 5
  - **Lời giải:**
    1. a_ij là phần tử ở hàng i, cột j: chỉ số thứ nhất là hàng, chỉ số thứ hai là cột.
    2. Hàng 1 của A là (7, -1, 0) nên a_12 = -1 và a_13 = 0.
    3. Hàng 2 của A là (2, 5, 9) nên a_21 = 2, a_22 = 5 và a_23 = 9.
- `dstt_t3_kt_06` · bậc 2 (Cơ bản) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm a_32 của ma trận A như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2, 3); (4, 5, 6); (7, 8, 9); (10, 11, 12)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận A có 4 hàng và 3 cột, nên có cỡ 4 x 3.
    2. Trong a_32, chỉ số thứ nhất là cột và chỉ số thứ hai là hàng, nên đó là phần tử ở cột 3, hàng 2.   **<- bước sai đầu tiên**
    3. Hàng 2 của A là (4, 5, 6), và cột 3 của hàng ấy là 6.
    4. Vậy a_32 = 6.
  - **Đáp án:** Bước 2: Trong a_32, chỉ số thứ nhất là cột và chỉ số thứ hai là hàng, nên đó là phần tử ở cột 3, hàng 2.
  - **Vì sao sai, và bước đúng:**
    1. Chỉ số thứ nhất của a_ij là hàng, chỉ số thứ hai là cột. Hàng luôn đứng trước.
    2. Đúng ra: a_32 nằm ở hàng 3, cột 2. Hàng 3 là (7, 8, 9) và cột 2 của nó là 8. Vậy a_32 = 8.
- `dstt_g3_phan_tu` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử a_14 bằng bao nhiêu?
  - A = (-7, -1, -6, 6); (5, 6, 3, -3)  (từng hàng)
  - **Đáp án:** 6
    1. Trong a_14, chỉ số thứ nhất là hàng, chỉ số thứ hai là cột.
    2. Hàng 1 của A là (-7, -1, -6, 6).
    3. Phần tử thứ 4 của hàng đó là 6.
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử a_21 bằng bao nhiêu?
  - A = (-7, 2); (-4, 0)  (từng hàng)
  - **Đáp án:** -4
    1. Trong a_21, chỉ số thứ nhất là hàng, chỉ số thứ hai là cột.
    2. Hàng 2 của A là (-4, 0).
    3. Phần tử thứ 1 của hàng đó là -4.
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử a_14 bằng bao nhiêu?
  - A = (-3, 6, 8, 8); (6, 3, -5, -2)  (từng hàng)
  - **Đáp án:** 8
    1. Trong a_14, chỉ số thứ nhất là hàng, chỉ số thứ hai là cột.
    2. Hàng 1 của A là (-3, 6, 8, 8).
    3. Phần tử thứ 4 của hàng đó là 8.
- `dstt_t3_kt_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một ma trận vuông có tất cả 49 phần tử. Nó có bao nhiêu hàng?
  - **Đáp án:** 7
    1. Ma trận vuông cấp n có n hàng, n cột và n . n phần tử.
    2. n . n = 49 nên n = 7.
- `dstt_g3_cong_thuc_hang` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A cỡ 2 x 3 có a_ij = 2i - 3j. Tính tổng các phần tử ở hàng 2.
  - **Đáp án:** -6
    1. Hàng 2 gồm các phần tử có i = 2 và j chạy từ 1 đến 3.
    2. Các phần tử đó là 1, -2, -5.
    3. Tổng là -6.
  - **Câu hỏi:** Ma trận A cỡ 2 x 3 có a_ij = i - j. Tính tổng các phần tử ở hàng 1.
  - **Đáp án:** -3
    1. Hàng 1 gồm các phần tử có i = 1 và j chạy từ 1 đến 3.
    2. Các phần tử đó là 0, -1, -2.
    3. Tổng là -3.
  - **Câu hỏi:** Ma trận A cỡ 2 x 3 có a_ij = 2i + 2j. Tính tổng các phần tử ở hàng 2.
  - **Đáp án:** 24
    1. Hàng 2 gồm các phần tử có i = 2 và j chạy từ 1 đến 3.
    2. Các phần tử đó là 6, 8, 10.
    3. Tổng là 24.

### Cộng ma trận và nhân với một số (`dstt_t3_cong_nhan_vo_huong`)

- `dstt_t3_cm_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cộng được một ma trận cỡ 2 x 3 với một ma trận cỡ 3 x 2.
  - **Đáp án:** Sai
    1. Phép cộng ma trận cộng từng cặp phần tử ở cùng vị trí.
    2. Vì vậy hai ma trận phải cùng cỡ: cùng số hàng và cùng số cột.
    3. 2 x 3 và 3 x 2 là hai cỡ khác nhau dù cùng có 6 phần tử.
- `dstt_t3_cm_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với hai ma trận cùng cỡ A và B, ta luôn có A + B = B + A.
  - **Đáp án:** Đúng
    1. Phần tử ở hàng i, cột j của A + B là a_ij + b_ij.
    2. Phần tử ở cùng vị trí của B + A là b_ij + a_ij.
    3. Hai số đó bằng nhau vì phép cộng số thực giao hoán.
- `dstt_g3_cong_ma_tran` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A + B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-2, -4); (2, -3)  (từng hàng)
  - B = (9, 8); (9, 6)  (từng hàng)
  - **Đáp án:** 7, 4, 11, 3
    1. Cộng từng cặp phần tử ở cùng vị trí.
    2. Hàng 1: (7, 4). Hàng 2: (11, 3).
    3. Nhập theo từng hàng: 7, 4, 11, 3.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A + B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-5, -4); (-4, 5)  (từng hàng)
  - B = (-1, 3); (2, 0)  (từng hàng)
  - **Đáp án:** -6, -1, -2, 5
    1. Cộng từng cặp phần tử ở cùng vị trí.
    2. Hàng 1: (-6, -1). Hàng 2: (-2, 5).
    3. Nhập theo từng hàng: -6, -1, -2, 5.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A + B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (1, -2); (5, 9)  (từng hàng)
  - B = (-4, -6); (9, 2)  (từng hàng)
  - **Đáp án:** -3, -8, 14, 11
    1. Cộng từng cặp phần tử ở cùng vị trí.
    2. Hàng 1: (-3, -8). Hàng 2: (14, 11).
    3. Nhập theo từng hàng: -3, -8, 14, 11.
- `dstt_t3_cm_03` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận cỡ 2 x 2 và 3A là ma trận không. Kết luận nào đúng?
    - **(đúng)** A là ma trận không
    - A là ma trận đơn vị
    - A là ma trận chéo khác ma trận không
    - Chưa đủ thông tin để kết luận
  - **Đáp án:** A là ma trận không
    1. Mỗi phần tử của 3A bằng 3 lần phần tử tương ứng của A.
    2. 3 . a_ij = 0 chỉ khi a_ij = 0.
    3. Mọi phần tử của A đều bằng 0, nên A là ma trận không.
- `dstt_t3_cm_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Sắp xếp các bước tìm ma trận X sao cho 2X + B = A.
  - A = (1, 2); (0, -1)  (từng hàng)
  - B = (3, 0); (1, 1)  (từng hàng)
  - **Đáp án (thứ tự đúng):**
    1. Chuyển B sang vế phải: 2X = A - B.
    2. Thay A và B: 2X có hàng 1 là (1 - 3, 2 - 0) và hàng 2 là (0 - 1, -1 - 1).
    3. Tính các hiệu: 2X có hàng 1 là (-2, 2) và hàng 2 là (-1, -2).
    4. Chia mọi phần tử cho 2: X có hàng 1 là (-1, 1) và hàng 2 là (-1/2, -1).
  - **Lời giải:**
    1. Cộng và nhân ma trận với một số làm theo từng vị trí, nên biến đổi như phương trình số: 2X = A - B, rồi X = (1/2)(A - B).
    2. A - B có hàng (-2, 2) và (-1, -2); chia cho 2 được X có hàng (-1, 1) và (-1/2, -1).
    3. Thử lại: 2X có hàng (-2, 2) và (-1, -2); cộng B được hàng (1, 2) và (0, -1), đúng bằng A.
- `dstt_g3_to_hop_ma_tran` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Phần tử ở hàng 2, cột 2 của 2A - 3B bằng bao nhiêu?
  - A = (-3, 4, -4); (-1, -4, 2)  (từng hàng)
  - B = (2, 2, 5); (1, -2, -4)  (từng hàng)
  - **Đáp án:** -2
    1. Chỉ cần phần tử ở hàng 2, cột 2 của mỗi ma trận: a_22 = -4 và b_22 = -2.
    2. 2 . (-4) + (-3) . (-2) = -2.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Phần tử ở hàng 1, cột 2 của -2A + 3B bằng bao nhiêu?
  - A = (-5, -4, -4); (0, -3, 6)  (từng hàng)
  - B = (5, -1, -1); (4, -2, 4)  (từng hàng)
  - **Đáp án:** 5
    1. Chỉ cần phần tử ở hàng 1, cột 2 của mỗi ma trận: a_12 = -4 và b_12 = -1.
    2. (-2) . (-4) + 3 . (-1) = 5.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Phần tử ở hàng 1, cột 1 của 2A - B bằng bao nhiêu?
  - A = (-2, 4, 3); (-3, 0, 4)  (từng hàng)
  - B = (2, 5, 4); (-4, 4, -5)  (từng hàng)
  - **Đáp án:** -6
    1. Chỉ cần phần tử ở hàng 1, cột 1 của mỗi ma trận: a_11 = -2 và b_11 = 2.
    2. 2 . (-2) + (-1) . 2 = -6.

### Ma trận chuyển vị A^T (`dstt_t3_chuyen_vi`)

- `dstt_t3_cv_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A có cỡ 2 x 5. A^T có cỡ là gì?
    - **(đúng)** 5 x 2
    - 2 x 5
    - 5 x 5
    - 2 x 2
  - **Đáp án:** 5 x 2
    1. Chuyển vị đổi hàng thành cột và cột thành hàng.
    2. A có 2 hàng và 5 cột, nên A^T có 5 hàng và 2 cột.
    3. A^T có cỡ 5 x 2.
- `dstt_t3_cv_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chuyển vị hai lần thì trở về ma trận ban đầu: (A^T)^T = A.
  - **Đáp án:** Đúng
    1. Phần tử ở hàng i, cột j của A^T là a_ji.
    2. Chuyển vị lần nữa, phần tử ở hàng i, cột j lại là a_ij.
    3. Mọi phần tử trở về chỗ cũ, nên (A^T)^T = A.
- `dstt_t3_cv_05` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Ghép mỗi phần tử của A^T với giá trị của nó (hàng trước, cột sau).
  - A = (1, -3, 0); (2, 8, 5)  (từng hàng)
  - **Đáp án (ghép đúng):**
    - hàng 1, cột 2 của A^T — 2
    - hàng 2, cột 1 của A^T — -3
    - hàng 2, cột 2 của A^T — 8
    - hàng 3, cột 1 của A^T — 0
    - hàng 3, cột 2 của A^T — 5
  - **Lời giải:**
    1. Phần tử ở hàng i, cột j của A^T là phần tử ở hàng j, cột i của A.
    2. A^T cỡ 3 x 2 có hàng 1 là (1, 2), hàng 2 là (-3, 8), hàng 3 là (0, 5).
    3. Từ đó đọc ra: hàng 1 cột 2 là 2, hàng 2 cột 1 là -3, hàng 2 cột 2 là 8, hàng 3 cột 1 là 0, hàng 3 cột 2 là 5.
- `dstt_g3_chuyen_vi_phan_tu` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử ở hàng 2, cột 3 của A^T bằng bao nhiêu?
  - A = (9, -7); (-1, -6); (6, 5)  (từng hàng)
  - **Đáp án:** 5
    1. Chuyển vị đổi hàng thành cột: phần tử ở hàng i, cột j của A^T là phần tử ở hàng j, cột i của A.
    2. Cần lấy phần tử ở hàng 3, cột 2 của A.
    3. Đó là 5.
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử ở hàng 3, cột 1 của A^T bằng bao nhiêu?
  - A = (-7, -7, 2); (-4, 0, -1)  (từng hàng)
  - **Đáp án:** 2
    1. Chuyển vị đổi hàng thành cột: phần tử ở hàng i, cột j của A^T là phần tử ở hàng j, cột i của A.
    2. Cần lấy phần tử ở hàng 1, cột 3 của A.
    3. Đó là 2.
  - **Câu hỏi:** Cho ma trận A như hình. Phần tử ở hàng 1, cột 3 của A^T bằng bao nhiêu?
  - A = (9, 8); (-5, 2); (6, 9)  (từng hàng)
  - **Đáp án:** 6
    1. Chuyển vị đổi hàng thành cột: phần tử ở hàng i, cột j của A^T là phần tử ở hàng j, cột i của A.
    2. Cần lấy phần tử ở hàng 3, cột 1 của A.
    3. Đó là 6.
- `dstt_t3_cv_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với hai ma trận cùng cỡ A và B, ta có (A + B)^T = A^T + B^T.
  - **Đáp án:** Đúng
    1. Phần tử ở hàng i, cột j của (A + B)^T là phần tử ở hàng j, cột i của A + B, tức là a_ji + b_ji.
    2. Phần tử ở hàng i, cột j của A^T + B^T cũng là a_ji + b_ji.
    3. Hai ma trận có mọi phần tử bằng nhau nên bằng nhau.
- `dstt_t3_cv_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận nào cũng cộng được với ma trận chuyển vị của chính nó.
  - **Đáp án:** Sai
    1. A cỡ m x n thì A^T cỡ n x m.
    2. Hai ma trận chỉ cộng được khi cùng cỡ, tức là khi m = n.
    3. Ví dụ A cỡ 2 x 3 không cộng được với A^T cỡ 3 x 2. Chỉ ma trận vuông mới cộng được với chuyển vị của nó.
- `dstt_t3_cv_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính (A + 2B)^T với A, B như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (3, 4)  (từng hàng)
  - B = (0, 1); (2, 0)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. Chuyển vị đi qua phép cộng và phép nhân với một số, nên xử lý được từng hạng tử.
    2. Ta chỉ cần chuyển vị A: (A + 2B)^T = A^T + 2B.   **<- bước sai đầu tiên**
    3. A^T = ((1, 3), (2, 4)), còn 2B = ((0, 2), (4, 0)).
    4. Cộng lại: A^T + 2B = ((1, 5), (6, 4)).
  - **Đáp án:** Bước 2: Ta chỉ cần chuyển vị A: (A + 2B)^T = A^T + 2B.
  - **Vì sao sai, và bước đúng:**
    1. Chuyển vị phải làm cho từng hạng tử, không chỉ cho hạng tử đầu: (A + 2B)^T = A^T + 2B^T.
    2. Đúng ra: B^T = ((0, 2), (1, 0)), nên 2B^T = ((0, 4), (2, 0)). Cộng với A^T được ((1, 7), (4, 4)). Kiểm tra: A + 2B = ((1, 4), (7, 4)), chuyển vị của nó đúng là ((1, 7), (4, 4)).
- `dstt_g3_chuyen_vi_tong` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A^T + B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-2, -4); (2, -3)  (từng hàng)
  - B = (9, 8); (9, 6)  (từng hàng)
  - **Đáp án:** 7, 10, 5, 3
    1. Các cột của A thành các hàng của A^T: hàng 1 là (-2, 2), hàng 2 là (-4, -3).
    2. Cộng từng phần tử với B: hàng 1 là (7, 10), hàng 2 là (5, 3).
    3. Nhập theo từng hàng: 7, 10, 5, 3.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A^T - B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-1, 3); (2, 0)  (từng hàng)
  - B = (-5, -1); (7, 6)  (từng hàng)
  - **Đáp án:** 4, 3, -4, -6
    1. Các cột của A thành các hàng của A^T: hàng 1 là (-1, 2), hàng 2 là (3, 0).
    2. Trừ từng phần tử với B: hàng 1 là (4, 3), hàng 2 là (-4, -6).
    3. Nhập theo từng hàng: 4, 3, -4, -6.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính A^T + B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (1, -2); (5, 9)  (từng hàng)
  - B = (-4, -6); (9, 2)  (từng hàng)
  - **Đáp án:** -3, -1, 7, 11
    1. Các cột của A thành các hàng của A^T: hàng 1 là (1, 5), hàng 2 là (-2, 9).
    2. Cộng từng phần tử với B: hàng 1 là (-3, -1), hàng 2 là (7, 11).
    3. Nhập theo từng hàng: -3, -1, 7, 11.

### Vết của ma trận vuông (`dstt_t3_vet`)

- `dstt_t3_vet_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vết chỉ được định nghĩa cho ma trận vuông.
  - **Đáp án:** Đúng
    1. Vết là tổng các phần tử a_11, a_22, ..., a_nn trên đường chéo chính.
    2. Đường chéo chính đi từ góc trên bên trái đến góc dưới bên phải chỉ có ở ma trận vuông.
- `dstt_t3_vet_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vết của ma trận đơn vị cấp 5 bằng bao nhiêu?
  - **Đáp án:** 5
    1. Ma trận đơn vị cấp 5 có 5 phần tử trên đường chéo chính, tất cả bằng 1.
    2. Vết là 1 + 1 + 1 + 1 + 1 = 5.
- `dstt_g3_vet` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Tính vết tr(A).
  - A = (-5, 9, -7); (-1, -6, 6); (5, 6, 3)  (từng hàng)
  - **Đáp án:** -8
    1. Vết là tổng các phần tử trên đường chéo chính.
    2. Đường chéo chính của A: -5, -6, 3.
    3. tr(A) = -8.
  - **Câu hỏi:** Cho ma trận A như hình. Tính vết tr(A).
  - A = (-8, -7, -7); (2, -4, 0); (-1, -3, -8)  (từng hàng)
  - **Đáp án:** -20
    1. Vết là tổng các phần tử trên đường chéo chính.
    2. Đường chéo chính của A: -8, -4, -8.
    3. tr(A) = -20.
  - **Câu hỏi:** Cho ma trận A như hình. Tính vết tr(A).
  - A = (-2, 9, 8); (-5, 2, 6); (9, -7, -9)  (từng hàng)
  - **Đáp án:** -9
    1. Vết là tổng các phần tử trên đường chéo chính.
    2. Đường chéo chính của A: -2, 2, -9.
    3. tr(A) = -9.
- `dstt_t3_vet_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với hai ma trận vuông cùng cấp A và B, ta có tr(A + B) = tr(A) + tr(B).
  - **Đáp án:** Đúng
    1. Phần tử thứ k trên đường chéo chính của A + B là a_kk + b_kk.
    2. Cộng theo k: tổng các a_kk + b_kk bằng tổng các a_kk cộng với tổng các b_kk.
    3. Đó chính là tr(A) + tr(B).
- `dstt_t3_vet_04` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 3 có tr(A) = 4, và I là ma trận đơn vị cấp 3. Tính tr(2A + I).
  - **Đáp án:** 11
    1. Vết có tính tuyến tính: tr(2A + I) = 2 . tr(A) + tr(I).
    2. tr(I) = 3 vì đường chéo chính của I gồm ba số 1.
    3. tr(2A + I) = 2 . 4 + 3 = 11.
- `dstt_t3_vet_05` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B là hai ma trận vuông cấp 3 có tr(A) = 5 và tr(B) = -2. Sắp xếp các bước tính tr(3A - 2B + I_3).
  - **Đáp án (thứ tự đúng):**
    1. Vết của một tổng bằng tổng các vết: tr(3A - 2B + I_3) = tr(3A) + tr(-2B) + tr(I_3).
    2. Đưa hệ số ra ngoài vết: = 3 tr(A) - 2 tr(B) + tr(I_3).
    3. Thay số, với tr(I_3) = 3: = 3 . 5 - 2 . (-2) + 3.
    4. Tính ra: 15 + 4 + 3 = 22.
  - **Lời giải:**
    1. Vết cộng các phần tử trên đường chéo chính, nên tr(X + Y) = tr(X) + tr(Y) và tr(kX) = k tr(X).
    2. Ma trận đơn vị I_3 có ba số 1 trên đường chéo nên tr(I_3) = 3.
    3. tr(3A - 2B + I_3) = 3 . 5 - 2 . (-2) + 3 = 15 + 4 + 3 = 22.
- `dstt_t3_vet_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính tr(2A - B) với A, B như hình. Bước đầu tiên bị sai là bước nào?
  - A = (2, 1); (0, 3)  (từng hàng)
  - B = (1, 4); (5, 2)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. tr(A) = 2 + 3 = 5 và tr(B) = 1 + 2 = 3.
    2. Vết có tính tuyến tính, nên đặt 2 làm thừa số chung: tr(2A - B) = 2(tr(A) - tr(B)).   **<- bước sai đầu tiên**
    3. Vậy tr(2A - B) = 2(5 - 3) = 4.
  - **Đáp án:** Bước 2: Vết có tính tuyến tính, nên đặt 2 làm thừa số chung: tr(2A - B) = 2(tr(A) - tr(B)).
  - **Vì sao sai, và bước đúng:**
    1. Tuyến tính nghĩa là tr(kA + B) = k.tr(A) + tr(B): số 2 chỉ nhân với A, không nhân với B.
    2. Đúng ra: tr(2A - B) = 2.5 - 3 = 7. Kiểm tra: 2A - B = ((3, -2), (-5, 4)), có vết 3 + 4 = 7.
- `dstt_g3_vet_to_hop` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính tr(-2A - 3B).
  - A = (-2, -4); (2, -3)  (từng hàng)
  - B = (9, 8); (9, 6)  (từng hàng)
  - **Đáp án:** -35
    1. Vết có tính tuyến tính, nên chỉ cần tr(A) = -5 và tr(B) = 15.
    2. tr(-2A - 3B) = (-2) . (-5) + (-3) . 15 = -35.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính tr(3A - 3B).
  - A = (-5, -4); (-4, 5)  (từng hàng)
  - B = (-1, 3); (2, 0)  (từng hàng)
  - **Đáp án:** 3
    1. Vết có tính tuyến tính, nên chỉ cần tr(A) = 0 và tr(B) = -1.
    2. tr(3A - 3B) = 3 . 0 + (-3) . (-1) = 3.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính tr(3A - B).
  - A = (1, -2); (5, 9)  (từng hàng)
  - B = (-4, -6); (9, 2)  (từng hàng)
  - **Đáp án:** 32
    1. Vết có tính tuyến tính, nên chỉ cần tr(A) = 10 và tr(B) = -2.
    2. tr(3A - B) = 3 . 10 + (-1) . (-2) = 32.

### Các ma trận đặc biệt (`dstt_t3_ma_tran_dac_biet`)

- `dstt_t3_db_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận đơn vị cấp 4 có bao nhiêu phần tử bằng 0?
  - **Đáp án:** 12
    1. Ma trận đơn vị cấp 4 có 4 . 4 = 16 phần tử.
    2. 4 phần tử trên đường chéo chính bằng 1, các phần tử còn lại bằng 0.
    3. Số phần tử bằng 0 là 16 - 4 = 12.
- `dstt_t3_db_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi ma trận chéo đều là ma trận đối xứng.
  - **Đáp án:** Đúng
    1. Ma trận chéo có a_ij = 0 với mọi i khác j.
    2. Khi đó a_ij = a_ji = 0 với mọi i khác j, đúng điều kiện của ma trận đối xứng.
- `dstt_t3_db_03` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình là ma trận đơn vị.
  - A = (1, 0, 0); (0, 1, 0); (0, 0, 0)  (từng hàng)
  - **Đáp án:** Sai
    1. Ma trận đơn vị có mọi phần tử trên đường chéo chính bằng 1 và mọi phần tử khác bằng 0.
    2. Ở đây a_33 = 0 chứ không phải 1.
    3. A là ma trận chéo nhưng không phải là ma trận đơn vị.
- `dstt_g3_dac_biet` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng.
  - A = (2, -4, 0); (-4, 7, -5); (-2, -5, 2)  (từng hàng)
  - **Đáp án:** Sai
    1. Ma trận vuông là đối xứng khi a_ij = a_ji với mọi i, j.
    2. a_13 = 0 nhưng a_31 = -2.
    3. Có một cặp khác nhau nên A không đối xứng.
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng.
  - A = (6, 5, 7); (5, 7, -4); (7, -4, 5)  (từng hàng)
  - **Đáp án:** Đúng
    1. Ma trận vuông là đối xứng khi a_ij = a_ji với mọi i, j.
    2. Kiểm tra ba cặp: a_12 = a_21 = 5, a_13 = a_31 = 7, a_23 = a_32 = -4.
    3. Mọi cặp đều bằng nhau nên A đối xứng.
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng.
  - A = (2, -4, -1); (-2, 5, 3); (-1, 3, 4)  (từng hàng)
  - **Đáp án:** Sai
    1. Ma trận vuông là đối xứng khi a_ij = a_ji với mọi i, j.
    2. a_12 = -4 nhưng a_21 = -2.
    3. Có một cặp khác nhau nên A không đối xứng.
- `dstt_t3_db_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận đối xứng nào cũng có các phần tử nằm ngoài đường chéo chính bằng 0.
  - **Đáp án:** Sai
    1. Đối xứng chỉ đòi hỏi a_ij = a_ji, không đòi hỏi chúng bằng 0.
    2. Ví dụ ma trận cấp 2 có hàng 1 là (1, 2) và hàng 2 là (2, 3) đối xứng nhưng có a_12 = a_21 = 2.
    3. Có phần tử ngoài đường chéo chính bằng 0 hết là tính chất của ma trận chéo.
- `dstt_t3_db_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận vuông A là đối xứng khi và chỉ khi A^T = A.
  - **Đáp án:** Đúng
    1. Phần tử ở hàng i, cột j của A^T là a_ji.
    2. A^T = A nghĩa là a_ji = a_ij với mọi i, j.
    3. Đó chính là định nghĩa của ma trận đối xứng.
- `dstt_t3_db_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một ma trận tam giác trên cấp 3 có nhiều nhất bao nhiêu phần tử khác 0?
  - **Đáp án:** 6
    1. Ma trận tam giác trên có mọi phần tử nằm dưới đường chéo chính bằng 0.
    2. Cấp 3 có 9 phần tử, trong đó 3 phần tử nằm dưới đường chéo chính.
    3. Nhiều nhất 9 - 3 = 6 phần tử có thể khác 0.
- `dstt_t3_db_07` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi ma trận cấp 2 bên trái được cho bởi hàng 1 rồi hàng 2. Ghép mỗi ma trận với mô tả đúng của nó.
  - **Đáp án (ghép đúng):**
    - (1, 0) và (0, 1) — ma trận đơn vị
    - (2, 0) và (0, 5) — ma trận chéo nhưng không là ma trận đơn vị
    - (1, 3) và (0, 2) — tam giác trên nhưng không là ma trận chéo
    - (1, 3) và (3, 2) — đối xứng nhưng không là ma trận chéo
  - **Lời giải:**
    1. Ma trận chéo có mọi phần tử ngoài đường chéo chính bằng 0; ma trận đơn vị là ma trận chéo có đường chéo toàn số 1.
    2. (1, 0) và (0, 1) là ma trận đơn vị; (2, 0) và (0, 5) là ma trận chéo nhưng đường chéo không toàn số 1.
    3. (1, 3) và (0, 2) có a_21 = 0 nhưng a_12 = 3, nên là tam giác trên, không chéo và không đối xứng.
    4. (1, 3) và (3, 2) có a_12 = a_21 = 3, nên đối xứng nhưng không chéo, cũng không tam giác trên.
- `dstt_g3_doi_xung_dien` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng. Tìm x và y. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - A = (7, -2, x); (y, 7, 7); (3, 7, -4)  (từng hàng)
  - **Đáp án:** 3, -2
    1. Ma trận đối xứng có a_ij = a_ji với mọi i, j.
    2. x nằm ở hàng 1, cột 3 nên x = a_31 = 3.
    3. y nằm ở hàng 2, cột 1 nên y = a_12 = -2.
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng. Tìm x và y. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - A = (0, -5, 9); (-5, 8, x); (y, 8, -3)  (từng hàng)
  - **Đáp án:** 8, 9
    1. Ma trận đối xứng có a_ij = a_ji với mọi i, j.
    2. x nằm ở hàng 2, cột 3 nên x = a_32 = 8.
    3. y nằm ở hàng 3, cột 1 nên y = a_13 = 9.
  - **Câu hỏi:** Ma trận A như hình là ma trận đối xứng. Tìm x và y. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - A = (-3, 1, 3); (1, 0, x); (y, 2, 9)  (từng hàng)
  - **Đáp án:** 2, 3
    1. Ma trận đối xứng có a_ij = a_ji với mọi i, j.
    2. x nằm ở hàng 2, cột 3 nên x = a_32 = 2.
    3. y nằm ở hàng 3, cột 1 nên y = a_13 = 3.
