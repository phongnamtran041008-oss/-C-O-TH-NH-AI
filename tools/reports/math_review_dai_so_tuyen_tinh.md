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

## Tầng 4: Nhân ma trận

47 dạng câu (38 câu viết tay, 9 bộ sinh câu); 47 chưa duyệt.

### Tích vô hướng: một hàng nhân một cột (`dstt_t4_tich_vo_huong`)

- `dstt_t4_tvh_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích vô hướng của u = (1, -2, 3) và v = (4, 0, -1).
  - **Đáp án:** 1
    1. Nhân từng cặp tọa độ cùng vị trí: 1 . 4 = 4, (-2) . 0 = 0, 3 . (-1) = -3.
    2. Cộng các tích: 4 + 0 - 3 = 1.
- `dstt_t4_tvh_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích vô hướng của hai vectơ cùng số chiều là một vectơ.
  - **Đáp án:** Sai
    1. Tích vô hướng nhân từng cặp tọa độ rồi cộng tất cả lại.
    2. Kết quả là một số, không phải một vectơ. Ví dụ (1, 2) . (3, 4) = 3 + 8 = 11.
- `dstt_t4_tvh_05` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tích vô hướng của u = (1, 2) và v = (3, 4, 5) bằng bao nhiêu?
    - **(đúng)** Không xác định, vì hai vectơ khác số chiều
    - 11
    - 26
    - (3, 8, 5)
  - **Đáp án:** Không xác định, vì hai vectơ khác số chiều
    1. Tích vô hướng ghép tọa độ thứ k của u với tọa độ thứ k của v, nên hai vectơ phải có cùng số tọa độ.
    2. u thuộc R^2 còn v thuộc R^3: tọa độ 5 của v không có bạn để ghép.
    3. Vậy tích vô hướng này không xác định.
- `dstt_t4_tvh_06` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi tích vô hướng với giá trị của nó.
  - **Đáp án (ghép đúng):**
    - (1, 2) . (3, 4) — 11
    - (1, -1) . (1, 1) — 0
    - (2, 0, 1) . (1, 5, 3) — 5
    - (-1, 2, 2) . (2, 1, 3) — 6
  - **Lời giải:**
    1. Nhân từng cặp tọa độ cùng vị trí rồi cộng lại.
    2. (1, 2) . (3, 4) = 3 + 8 = 11; (1, -1) . (1, 1) = 1 - 1 = 0.
    3. (2, 0, 1) . (1, 5, 3) = 2 + 0 + 3 = 5; (-1, 2, 2) . (2, 1, 3) = -2 + 2 + 6 = 6.
- `dstt_g4_tich_vo_huong` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính tích vô hướng của u = (4, -4, -1) và v = (-4, 2, 2) trong R^3.
  - **Đáp án:** -26
    1. Nhân từng cặp tọa độ cùng vị trí rồi cộng lại.
    2. u . v = 4 . (-4) + (-4) . 2 + (-1) . 2 = -26.
  - **Câu hỏi:** Tính tích vô hướng của u = (-4, -4, 0) và v = (-3, 6, 5) trong R^3.
  - **Đáp án:** -12
    1. Nhân từng cặp tọa độ cùng vị trí rồi cộng lại.
    2. u . v = (-4) . (-3) + (-4) . 6 + 0 . 5 = -12.
  - **Câu hỏi:** Tính tích vô hướng của u = (4, 3, -3) và v = (0, 4, 2) trong R^3.
  - **Đáp án:** 6
    1. Nhân từng cặp tọa độ cùng vị trí rồi cộng lại.
    2. u . v = 4 . 0 + 3 . 4 + (-3) . 2 = 6.
- `dstt_t4_tvh_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm số thực m để u = (m, 2, -1) và v = (3, m, 4) có tích vô hướng bằng 0.
  - **Đáp án:** 4/5
    1. u . v = m . 3 + 2 . m + (-1) . 4 = 5m - 4.
    2. Giải 5m - 4 = 0 được m = 4/5.
    3. Thử lại: u = (4/5, 2, -1), v = (3, 4/5, 4): 12/5 + 8/5 - 4 = 0.
- `dstt_t4_tvh_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính tích vô hướng của u = (2, -3, 1) và v = (-1, 4, 5). Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Hai vectơ cùng thuộc R^3 nên tích vô hướng xác định.
    2. Các tích từng cặp tọa độ: 2 . (-1) = -2, (-3) . 4 = 12 và 1 . 5 = 5.   **<- bước sai đầu tiên**
    3. Cộng lại: u . v = -2 + 12 + 5 = 15.
  - **Đáp án:** Bước 2: Các tích từng cặp tọa độ: 2 . (-1) = -2, (-3) . 4 = 12 và 1 . 5 = 5.
  - **Vì sao sai, và bước đúng:**
    1. Số âm nhân số dương cho số âm: (-3) . 4 = -12, không phải 12.
    2. Đúng ra: u . v = -2 - 12 + 5 = -9.

### Điều kiện kích thước để nhân (`dstt_t4_dieu_kien_kich_thuoc`)

- `dstt_t4_kt_01` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A có cỡ 2 x 3 và B có cỡ 3 x 4. Tích AB có cỡ là gì?
    - **(đúng)** 2 x 4
    - 3 x 3
    - 4 x 2
    - Không nhân được
  - **Đáp án:** 2 x 4
    1. AB nhân được khi số cột của A bằng số hàng của B: ở đây cả hai bằng 3.
    2. AB lấy số hàng của A và số cột của B.
    3. AB có cỡ 2 x 4.
- `dstt_t4_kt_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B đều có cỡ 3 x 2. Tích AB xác định.
  - **Đáp án:** Sai
    1. AB cần số cột của A bằng số hàng của B.
    2. A có 2 cột còn B có 3 hàng.
    3. 2 khác 3 nên AB không xác định, dù hai ma trận cùng cỡ.
- `dstt_t4_kt_05` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi vế trái là tích của một ma trận cỡ bên trái với một ma trận cỡ bên phải. Ghép mỗi tích với cỡ của kết quả.
  - **Đáp án (ghép đúng):**
    - (2 x 3)(3 x 1) — 2 x 1
    - (1 x 3)(3 x 2) — 1 x 2
    - (3 x 1)(1 x 3) — 3 x 3
    - (1 x 3)(3 x 1) — 1 x 1
  - **Lời giải:**
    1. Tích (m x n)(n x p) có cỡ m x p: lấy số hàng của ma trận đầu và số cột của ma trận sau.
    2. (2 x 3)(3 x 1) cho 2 x 1; (1 x 3)(3 x 2) cho 1 x 2.
    3. (3 x 1)(1 x 3) cho 3 x 3, còn (1 x 3)(3 x 1) chỉ cho 1 x 1: đổi thứ tự là đổi cả cỡ.
- `dstt_g4_nhan_duoc` · bậc 2 (Cơ bản) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** A có cỡ 2 x 5 và B có cỡ 5 x 1. Tích AB xác định.
  - **Đáp án:** Đúng
    1. AB xác định khi số cột của A bằng số hàng của B.
    2. A có 5 cột, B có 5 hàng.
    3. 5 = 5 nên AB xác định và có cỡ 2 x 1.
  - **Câu hỏi:** A có cỡ 1 x 1 và B có cỡ 1 x 1. Tích AB xác định.
  - **Đáp án:** Đúng
    1. AB xác định khi số cột của A bằng số hàng của B.
    2. A có 1 cột, B có 1 hàng.
    3. 1 = 1 nên AB xác định và có cỡ 1 x 1.
  - **Câu hỏi:** A có cỡ 2 x 5 và B có cỡ 5 x 5. Tích AB xác định.
  - **Đáp án:** Đúng
    1. AB xác định khi số cột của A bằng số hàng của B.
    2. A có 5 cột, B có 5 hàng.
    3. 5 = 5 nên AB xác định và có cỡ 2 x 5.
- `dstt_t4_kt_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A có cỡ 2 x 5. Ma trận B phải có cỡ bao nhiêu để cả AB và BA đều xác định? Nhập số hàng rồi số cột của B, cách nhau bằng dấu phẩy.
  - **Đáp án:** 5, 2
    1. AB xác định cần số hàng của B bằng số cột của A, tức là 5.
    2. BA xác định cần số cột của B bằng số hàng của A, tức là 2.
    3. Vậy B có cỡ 5 x 2.
- `dstt_t4_kt_04` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi ma trận A (vuông hay không), tích A^T A luôn xác định.
  - **Đáp án:** Đúng
    1. Gọi A có cỡ m x n; khi đó A^T có cỡ n x m.
    2. A^T A là (n x m)(m x n): số cột của A^T là m, bằng số hàng của A.
    3. Vậy A^T A luôn xác định và có cỡ n x n.
- `dstt_t4_kt_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B đều có cỡ 2 x 3. Lời giải sau xét xem A B^T và A^T B có xác định không. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. B^T có cỡ 3 x 2 và A^T có cỡ 3 x 2.
    2. A B^T là (2 x 3)(3 x 2): nhân được, kết quả có cỡ 2 x 2.
    3. A^T B là (3 x 2)(2 x 3): không nhân được, vì số hàng của A^T là 3 khác số hàng của B là 2.   **<- bước sai đầu tiên**
    4. Vậy chỉ có A B^T xác định.
  - **Đáp án:** Bước 3: A^T B là (3 x 2)(2 x 3): không nhân được, vì số hàng của A^T là 3 khác số hàng của B là 2.
  - **Vì sao sai, và bước đúng:**
    1. Điều kiện nhân là số cột của ma trận đầu bằng số hàng của ma trận sau, không phải so số hàng với số hàng.
    2. Đúng ra: A^T có 2 cột và B có 2 hàng, nên A^T B xác định và có cỡ 3 x 3. Cả hai tích đều xác định.
- `dstt_t4_kt_07` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A có cỡ 2 x 3, B có cỡ 3 x 4 và C có cỡ 4 x 1. Sắp xếp các bước tìm cỡ của ABC.
  - **Đáp án (thứ tự đúng):**
    1. Xét AB: số cột của A là 3 bằng số hàng của B là 3, nên AB xác định.
    2. AB có cỡ 2 x 4.
    3. Xét (AB)C: số cột của AB là 4 bằng số hàng của C là 4, nên tích xác định.
    4. ABC có cỡ 2 x 1.
  - **Lời giải:**
    1. Nhân lần lượt từ trái sang phải, mỗi lần kiểm tra số cột của ma trận trước bằng số hàng của ma trận sau.
    2. AB có cỡ 2 x 4; nhân tiếp với C cỡ 4 x 1 được cỡ 2 x 1.
- `dstt_g4_co_tich_ba` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** A có cỡ 2 x 5, B có cỡ 5 x 1 và C có cỡ 1 x 3. Tích ABC có cỡ bao nhiêu? Nhập số hàng rồi số cột, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 3
    1. AB có cỡ 2 x 1, vì số cột của A bằng số hàng của B.
    2. (AB)C có cỡ 2 x 3, vì số cột của AB là 1 bằng số hàng của C.
    3. Kết quả: 2 hàng, 3 cột.
  - **Câu hỏi:** A có cỡ 1 x 1, B có cỡ 1 x 1 và C có cỡ 1 x 3. Tích ABC có cỡ bao nhiêu? Nhập số hàng rồi số cột, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 3
    1. AB có cỡ 1 x 1, vì số cột của A bằng số hàng của B.
    2. (AB)C có cỡ 1 x 3, vì số cột của AB là 1 bằng số hàng của C.
    3. Kết quả: 1 hàng, 3 cột.
  - **Câu hỏi:** A có cỡ 2 x 5, B có cỡ 5 x 5 và C có cỡ 5 x 2. Tích C^T B^T A^T có cỡ bao nhiêu? Nhập số hàng rồi số cột, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 2
    1. C^T có cỡ 2 x 5, B^T có cỡ 5 x 5, A^T có cỡ 5 x 2.
    2. Nhân lần lượt: C^T B^T có cỡ 2 x 5, rồi C^T B^T A^T có cỡ 2 x 2.
    3. Đó cũng là cỡ của (ABC)^T, vì C^T B^T A^T = (ABC)^T.
    4. Kết quả: 2 hàng, 2 cột.

### Nhân hai ma trận (`dstt_t4_nhan_ma_tran`)

- `dstt_t4_nm_01` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình và vectơ cột x có hai tọa độ 2 và -1. Tính Ax. Nhập hai tọa độ, cách nhau bằng dấu phẩy.
  - A = (3, 1); (-2, 4)  (từng hàng)
  - **Đáp án:** 5, -8
    1. Tọa độ thứ nhất của Ax là hàng 1 của A nhân x: 3 . 2 + 1 . (-1) = 5.
    2. Tọa độ thứ hai là hàng 2 của A nhân x: (-2) . 2 + 4 . (-1) = -8.
    3. Ax = (5, -8).
- `dstt_t4_nm_02` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Phần tử ở hàng 1, cột 2 của AB bằng 1 . 5 + 2 . 7.
  - A = (1, 2); (3, 4)  (từng hàng)
  - B = (5, 6); (7, 8)  (từng hàng)
  - **Đáp án:** Sai
    1. Phần tử ở hàng 1, cột 2 của AB là hàng 1 của A nhân cột 2 của B.
    2. Hàng 1 của A là (1, 2), cột 2 của B là (6, 8): phần tử đó là 1 . 6 + 2 . 8 = 22.
    3. 1 . 5 + 2 . 7 = 19 là phần tử ở hàng 1, cột 1 (dùng cột 1 của B).
- `dstt_t4_nm_05` · bậc 2 (Cơ bản) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Sắp xếp các bước tính phần tử c_21 của C = AB.
  - A = (2, -1); (0, 3)  (từng hàng)
  - B = (1, 4); (2, 1)  (từng hàng)
  - **Đáp án (thứ tự đúng):**
    1. c_21 là hàng 2 của A nhân cột 1 của B.
    2. Hàng 2 của A là (0, 3), cột 1 của B là (1, 2).
    3. Nhân từng cặp: 0 . 1 = 0 và 3 . 2 = 6.
    4. Cộng lại: c_21 = 6.
  - **Lời giải:**
    1. Chỉ số đầu của c_21 chọn hàng của A, chỉ số sau chọn cột của B.
    2. (0, 3) . (1, 2) = 0 + 6 = 6.
- `dstt_t4_nm_07` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Ghép mỗi vị trí của AB với phần tử ở đó.
  - A = (1, 2); (0, -1)  (từng hàng)
  - B = (3, 1); (2, 4)  (từng hàng)
  - **Đáp án (ghép đúng):**
    - hàng 1, cột 1 của AB — 7
    - hàng 1, cột 2 của AB — 9
    - hàng 2, cột 1 của AB — -2
    - hàng 2, cột 2 của AB — -4
  - **Lời giải:**
    1. Phần tử hàng i, cột j của AB là hàng i của A nhân cột j của B.
    2. Hàng 1 của A là (1, 2): với cột (3, 2) được 3 + 4 = 7, với cột (1, 4) được 1 + 8 = 9.
    3. Hàng 2 của A là (0, -1): với cột (3, 2) được -2, với cột (1, 4) được -4.
- `dstt_g4_phan_tu_tich` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho A cỡ 2 x 3 và B cỡ 3 x 2 như hình. Tính phần tử ở hàng 1, cột 2 của AB.
  - A = (-2, 5, -3); (0, -3, 3)  (từng hàng)
  - B = (3, 3); (2, -1); (-3, 3)  (từng hàng)
  - **Đáp án:** -20
    1. Phần tử hàng 1, cột 2 của AB là hàng 1 của A nhân cột 2 của B.
    2. Hàng 1 của A là (-2, 5, -3), cột 2 của B là (3, -1, 3).
    3. (-2) . 3 + 5 . (-1) + (-3) . 3 = -20.
  - **Câu hỏi:** Cho A cỡ 2 x 3 và B cỡ 3 x 2 như hình. Tính phần tử ở hàng 1, cột 2 của AB.
  - A = (-4, -3, -3); (1, -2, 0)  (từng hàng)
  - B = (0, 5); (-1, 5); (-4, 5)  (từng hàng)
  - **Đáp án:** -50
    1. Phần tử hàng 1, cột 2 của AB là hàng 1 của A nhân cột 2 của B.
    2. Hàng 1 của A là (-4, -3, -3), cột 2 của B là (5, 5, 5).
    3. (-4) . 5 + (-3) . 5 + (-3) . 5 = -50.
  - **Câu hỏi:** Cho A cỡ 2 x 3 và B cỡ 3 x 2 như hình. Tính phần tử ở hàng 2, cột 1 của AB.
  - A = (-1, 5, 4); (-2, 1, 5)  (từng hàng)
  - B = (3, 5); (-3, 5); (-4, 3)  (từng hàng)
  - **Đáp án:** -29
    1. Phần tử hàng 2, cột 1 của AB là hàng 2 của A nhân cột 1 của B.
    2. Hàng 2 của A là (-2, 1, 5), cột 1 của B là (3, -3, -4).
    3. (-2) . 3 + 1 . (-3) + 5 . (-4) = -29.
- `dstt_t4_nm_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A cỡ 2 x 3 và B cỡ 3 x 2 như hình. Tính AB. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (1, 0, 2); (-1, 3, 1)  (từng hàng)
  - B = (3, 1); (2, 1); (1, 0)  (từng hàng)
  - **Đáp án:** 5, 1, 4, 2
    1. AB có cỡ 2 x 2; phần tử hàng i, cột j là hàng i của A nhân cột j của B.
    2. Hàng 1: (1 . 3 + 0 . 2 + 2 . 1, 1 . 1 + 0 . 1 + 2 . 0) = (5, 1).
    3. Hàng 2: ((-1) . 3 + 3 . 2 + 1 . 1, (-1) . 1 + 3 . 1 + 1 . 0) = (4, 2).
- `dstt_t4_nm_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 3 có hàng thứ hai toàn số 0. Với mọi ma trận B vuông cấp 3, điều nào chắc chắn đúng?
    - **(đúng)** Hàng thứ hai của AB toàn số 0
    - Cột thứ hai của AB toàn số 0
    - AB là ma trận không
    - AB = BA
  - **Đáp án:** Hàng thứ hai của AB toàn số 0
    1. Hàng 2 của AB gồm các tích của hàng 2 của A với từng cột của B.
    2. Hàng 2 của A toàn số 0 nên mọi tích đó bằng 0: hàng 2 của AB toàn số 0.
    3. Các hàng khác của AB tùy B, nên AB không nhất thiết là ma trận không; cột 2 của AB cũng không nhất thiết bằng 0.
- `dstt_t4_nm_06` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính AB với A, B như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (3, 4)  (từng hàng)
  - B = (2, 0); (1, -1)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. A và B cùng cỡ 2 x 2 nên AB xác định và có cỡ 2 x 2.
    2. Nhân từng phần tử cùng vị trí: hàng 1 của AB là (1 . 2, 2 . 0) = (2, 0).   **<- bước sai đầu tiên**
    3. Hàng 2 của AB là (3 . 1, 4 . (-1)) = (3, -4).
  - **Đáp án:** Bước 2: Nhân từng phần tử cùng vị trí: hàng 1 của AB là (1 . 2, 2 . 0) = (2, 0).
  - **Vì sao sai, và bước đúng:**
    1. Phép nhân ma trận không nhân từng ô cùng vị trí: phần tử hàng i, cột j là hàng i của A nhân cột j của B.
    2. Đúng ra: hàng 1 của AB là (1 . 2 + 2 . 1, 1 . 0 + 2 . (-1)) = (4, -2), hàng 2 là (3 . 2 + 4 . 1, 3 . 0 + 4 . (-1)) = (10, -4).
- `dstt_g4_tich_2x2` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính AB. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-2, 5); (-3, 0)  (từng hàng)
  - B = (-3, 3); (3, 3)  (từng hàng)
  - **Đáp án:** 21, 9, 9, -9
    1. Phần tử hàng i, cột j của AB là hàng i của A nhân cột j của B.
    2. Hàng 1: ((-2) . (-3) + 5 . 3, (-2) . 3 + 5 . 3) = (21, 9).
    3. Hàng 2: ((-3) . (-3) + 0 . 3, (-3) . 3 + 0 . 3) = (9, -9).
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính AB. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-4, -3); (-3, 1)  (từng hàng)
  - B = (-2, 0); (0, 5)  (từng hàng)
  - **Đáp án:** 8, -15, 6, 5
    1. Phần tử hàng i, cột j của AB là hàng i của A nhân cột j của B.
    2. Hàng 1: ((-4) . (-2) + (-3) . 0, (-4) . 0 + (-3) . 5) = (8, -15).
    3. Hàng 2: ((-3) . (-2) + 1 . 0, (-3) . 0 + 1 . 5) = (6, 5).
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính AB. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-1, 5); (4, -2)  (từng hàng)
  - B = (1, 5); (3, 5)  (từng hàng)
  - **Đáp án:** 14, 20, -2, 10
    1. Phần tử hàng i, cột j của AB là hàng i của A nhân cột j của B.
    2. Hàng 1: ((-1) . 1 + 5 . 3, (-1) . 5 + 5 . 5) = (14, 20).
    3. Hàng 2: (4 . 1 + (-2) . 3, 4 . 5 + (-2) . 5) = (-2, 10).

### AB != BA (`dstt_t4_khong_giao_hoan`)

- `dstt_t4_gh_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai ma trận vuông cùng cấp A và B, ta có AB = BA.
  - **Đáp án:** Sai
    1. Chỉ cần một ví dụ để bác bỏ: A có hàng (1, 1) và (0, 1), B có hàng (1, 0) và (1, 1).
    2. AB có hàng (2, 1) và (1, 1), còn BA có hàng (1, 1) và (1, 2).
    3. AB khác BA: phép nhân ma trận không giao hoán.
- `dstt_t4_gh_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận vuông cấp 2 nào sau đây giao hoán với mọi ma trận vuông cấp 2? Mỗi ma trận được cho bởi hàng 1 rồi hàng 2.
    - **(đúng)** (5, 0) và (0, 5)
    - (1, 1) và (0, 1)
    - (0, 1) và (1, 0)
    - (1, 0) và (0, 2)
  - **Đáp án:** (5, 0) và (0, 5)
    1. (5, 0) và (0, 5) là 5I, và (5I)B = 5B = B(5I) với mọi B.
    2. Ba ma trận còn lại đều có một ma trận không giao hoán với nó; ví dụ ma trận chéo (1, 0) và (0, 2) nhân với B có hàng (0, 1) và (0, 0) cho hai kết quả khác nhau ở hai phía.
    3. Ta biết các bội của I là những ma trận giao hoán với mọi ma trận cùng cấp.
- `dstt_t4_gh_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính AB - BA. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (1, 1); (0, 1)  (từng hàng)
  - B = (1, 0); (1, 1)  (từng hàng)
  - **Đáp án:** 1, 0, 0, -1
    1. AB có hàng (1 + 1, 0 + 1) = (2, 1) và (0 + 1, 0 + 1) = (1, 1).
    2. BA có hàng (1, 1) và (1 + 0, 1 + 1) = (1, 2).
    3. AB - BA có hàng (1, 0) và (0, -1): khác ma trận không, nên AB khác BA.
- `dstt_t4_gh_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau khai triển (A + B)^2 với A, B là hai ma trận vuông cùng cấp. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. (A + B)^2 = (A + B)(A + B).
    2. Nhân phân phối: (A + B)(A + B) = A^2 + AB + BA + B^2.
    3. Gộp AB + BA = 2AB, nên (A + B)^2 = A^2 + 2AB + B^2.   **<- bước sai đầu tiên**
    4. Vậy hằng đẳng thức quen thuộc đúng cho mọi ma trận vuông cùng cấp.
  - **Đáp án:** Bước 3: Gộp AB + BA = 2AB, nên (A + B)^2 = A^2 + 2AB + B^2.
  - **Vì sao sai, và bước đúng:**
    1. AB và BA nói chung khác nhau, nên không gộp AB + BA thành 2AB được.
    2. Đúng ra: (A + B)^2 = A^2 + AB + BA + B^2. Chỉ khi AB = BA mới viết được A^2 + 2AB + B^2.
- `dstt_t4_gh_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có hai ma trận vuông cấp 2 là A và B sao cho AB là ma trận không nhưng BA không phải là ma trận không.
  - **Đáp án:** Đúng
    1. Lấy A có hàng (0, 1) và (0, 0), B có hàng (1, 0) và (0, 0).
    2. AB có hàng (0, 0) và (0, 0): là ma trận không.
    3. BA có hàng (0, 1) và (0, 0): khác ma trận không. Ví dụ này cũng cho thấy AB = 0 không kéo theo A = 0 hay B = 0.
- `dstt_t4_gh_06` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A và B như hình, trong đó x là một số thực. Tìm x để AB = BA.
  - A = (1, 2); (0, 3)  (từng hàng)
  - B = (x, 1); (0, 2)  (từng hàng)
  - **Đáp án:** 1
    1. AB có hàng (x, 1 + 4) = (x, 5) và (0, 6).
    2. BA có hàng (x, 2x + 3) và (0, 6).
    3. Hai ma trận bằng nhau khi 2x + 3 = 5, tức là x = 1.
- `dstt_g4_giao_hoan` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Ta có AB = BA.
  - A = (-1, -2); (1, -2)  (từng hàng)
  - B = (-2, -4); (2, -4)  (từng hàng)
  - **Đáp án:** Đúng
    1. AB có hàng (-2, 12) và (-6, 4).
    2. BA có hàng (-2, 12) và (-6, 4).
    3. Hai ma trận bằng nhau: A và B giao hoán.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Ta có AB = BA.
  - A = (-3, -2); (-2, 2)  (từng hàng)
  - B = (1, 1); (0, -3)  (từng hàng)
  - **Đáp án:** Sai
    1. AB có hàng (-3, 3) và (-2, -8).
    2. BA có hàng (-5, 0) và (6, -6).
    3. Hai ma trận khác nhau: phép nhân ma trận không giao hoán.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Ta có AB = BA.
  - A = (0, -1); (2, 4)  (từng hàng)
  - B = (-2, -3); (4, 1)  (từng hàng)
  - **Đáp án:** Sai
    1. AB có hàng (-4, -1) và (12, -2).
    2. BA có hàng (-6, -10) và (2, 0).
    3. Hai ma trận khác nhau: phép nhân ma trận không giao hoán.

### Tính chất của phép nhân ma trận (`dstt_t4_tinh_chat_nhan`)

- `dstt_t4_tc_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với A cỡ m x n và B cỡ n x p, ta luôn có (AB)^T = A^T B^T.
  - **Đáp án:** Sai
    1. Quy tắc đúng là (AB)^T = B^T A^T: chuyển vị thì đảo thứ tự.
    2. Khi m khác p, A^T B^T là (n x m)(p x n), thậm chí không nhân được.
    3. Cả khi các ma trận vuông, A^T B^T thường khác (AB)^T.
- `dstt_t4_tc_02` · bậc 2 (Cơ bản) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đẳng thức nào đúng với mọi ma trận A, B, C có cỡ phù hợp để các phép toán xác định?
    - **(đúng)** A(B + C) = AB + AC
    - A(B + C) = BA + CA
    - (AB)^T = A^T B^T
    - AB = BA
  - **Đáp án:** A(B + C) = AB + AC
    1. Phép nhân ma trận phân phối với phép cộng, nhưng phải giữ A ở bên trái: A(B + C) = AB + AC.
    2. Đưa A sang bên phải (BA + CA) là đổi thứ tự nhân, nói chung sai.
    3. (AB)^T = B^T A^T chứ không phải A^T B^T, và AB nói chung khác BA.
- `dstt_t4_tc_06` · bậc 2 (Cơ bản) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A, B, C là các ma trận có cỡ phù hợp và k là một số. Ghép mỗi biểu thức với biểu thức luôn bằng nó.
  - **Đáp án (ghép đúng):**
    - A(BC) — (AB)C
    - (AB)^T — B^T A^T
    - A(B + C) — AB + AC
    - (kA)B — k(AB)
  - **Lời giải:**
    1. Tính kết hợp: A(BC) = (AB)C.
    2. Chuyển vị một tích thì đảo thứ tự: (AB)^T = B^T A^T.
    3. Tính phân phối, A vẫn ở bên trái: A(B + C) = AB + AC. Một số k thì đưa ra ngoài được: (kA)B = k(AB).
- `dstt_t4_tc_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho A cỡ 1 x 2, B cỡ 2 x 1 và C cỡ 1 x 2 như hình. Tính ABC. Nhập các phần tử, cách nhau bằng dấu phẩy.
  - A = (1, 2)  (từng hàng)
  - B = (3); (1)  (từng hàng)
  - C = (2, -1)  (từng hàng)
  - **Đáp án:** 10, -5
    1. Phép nhân có tính kết hợp, nên tính AB trước cho gọn: AB = 1 . 3 + 2 . 1 = 5, là ma trận cỡ 1 x 1.
    2. (AB)C = 5 . (2, -1) = (10, -5).
    3. Tính A(BC) cũng ra (10, -5), nhưng phải lập BC cỡ 2 x 2 trước.
- `dstt_t4_tc_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B là hai ma trận vuông cùng cấp. Sắp xếp các bước rút gọn (A + B)(A - B) - (A^2 - B^2).
  - **Đáp án (thứ tự đúng):**
    1. Nhân phân phối, giữ đúng thứ tự từng tích: (A + B)(A - B) = A^2 - AB + BA - B^2.
    2. Trừ đi A^2 - B^2: còn lại -AB + BA.
    3. Viết gọn: (A + B)(A - B) - (A^2 - B^2) = BA - AB.
    4. Vậy hiệu này là ma trận không khi và chỉ khi AB = BA.
  - **Lời giải:**
    1. Phân phối được, nhưng mỗi tích phải giữ thứ tự: B nhân A ở bên phải là BA, không phải AB.
    2. Sau khi trừ, A^2 và B^2 triệt tiêu, chỉ còn BA - AB.
    3. Hằng đẳng thức (A + B)(A - B) = A^2 - B^2 chỉ đúng khi A và B giao hoán.
- `dstt_t4_tc_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính (AB)^T với A, B như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (0, 1)  (từng hàng)
  - B = (1, 0); (3, 1)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. AB có hàng 1 là (1 + 6, 0 + 2) = (7, 2) và hàng 2 là (0 + 3, 0 + 1) = (3, 1).
    2. Để tính (AB)^T, chuyển vị từng ma trận rồi nhân theo thứ tự cũ: (AB)^T = A^T B^T.   **<- bước sai đầu tiên**
    3. A^T B^T có hàng 1 là (1, 3) và hàng 2 là (2, 7).
    4. Vậy (AB)^T có hàng (1, 3) và (2, 7).
  - **Đáp án:** Bước 2: Để tính (AB)^T, chuyển vị từng ma trận rồi nhân theo thứ tự cũ: (AB)^T = A^T B^T.
  - **Vì sao sai, và bước đúng:**
    1. Chuyển vị một tích thì đảo thứ tự: (AB)^T = B^T A^T.
    2. Đúng ra: chuyển vị AB đã tính ở bước 1, được (AB)^T có hàng (7, 3) và (2, 1). Tính B^T A^T cũng ra đúng như vậy, còn A^T B^T là một ma trận khác.
- `dstt_g4_chuyen_vi_tich` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính phần tử ở hàng 2, cột 1 của B^T A^T.
  - A = (-2, 5); (-3, 0)  (từng hàng)
  - B = (-3, 3); (3, 3)  (từng hàng)
  - **Đáp án:** 9
    1. B^T A^T = (AB)^T, nên phần tử hàng i, cột j của nó là phần tử hàng j, cột i của AB.
    2. Cần hàng 1 của A nhân cột 2 của B: (-2, 5) . (3, 3).
    3. (-2) . 3 + 5 . 3 = 9.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính phần tử ở hàng 1, cột 2 của B^T A^T.
  - A = (-4, -3); (-3, 1)  (từng hàng)
  - B = (-2, 0); (0, 5)  (từng hàng)
  - **Đáp án:** 6
    1. B^T A^T = (AB)^T, nên phần tử hàng i, cột j của nó là phần tử hàng j, cột i của AB.
    2. Cần hàng 2 của A nhân cột 1 của B: (-3, 1) . (-2, 0).
    3. (-3) . (-2) + 1 . 0 = 6.
  - **Câu hỏi:** Cho hai ma trận A và B như hình. Tính phần tử ở hàng 1, cột 2 của B^T A^T.
  - A = (-1, 5); (4, -2)  (từng hàng)
  - B = (1, 5); (3, 5)  (từng hàng)
  - **Đáp án:** -2
    1. B^T A^T = (AB)^T, nên phần tử hàng i, cột j của nó là phần tử hàng j, cột i của AB.
    2. Cần hàng 2 của A nhân cột 1 của B: (4, -2) . (1, 3).
    3. 4 . 1 + (-2) . 3 = -2.

### Ma trận đơn vị và lũy thừa ma trận (`dstt_t4_luy_thua`)

- `dstt_t4_lt_01` · bậc 2 (Cơ bản) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với A vuông cấp n và I là ma trận đơn vị cấp n, ta có AI = IA = A.
  - **Đáp án:** Đúng
    1. Hàng i của A nhân cột j của I chỉ giữ lại a_ij, vì cột j của I có số 1 ở vị trí j và số 0 ở mọi chỗ khác.
    2. Vậy AI = A; lập luận tương tự với hàng của I cho IA = A.
    3. Ma trận đơn vị đóng vai trò số 1 trong phép nhân ma trận.
- `dstt_t4_lt_02` · bậc 2 (Cơ bản) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Tính A^2. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (0, 1); (0, 0)  (từng hàng)
  - **Đáp án:** 0, 0, 0, 0
    1. A^2 = A . A: hàng 1 của A là (0, 1), các cột của A là (0, 0) và (1, 0).
    2. Hàng 1 của A^2: (0 . 0 + 1 . 0, 0 . 1 + 1 . 0) = (0, 0); hàng 2 của A toàn số 0 nên hàng 2 của A^2 cũng vậy.
    3. A^2 là ma trận không, dù A khác ma trận không.
- `dstt_g4_binh_phuong` · bậc 2 (Cơ bản) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Tính A^2. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-1, -2); (1, -2)  (từng hàng)
  - **Đáp án:** -1, 6, -3, 2
    1. A^2 = A . A: nhân hàng của A với cột của A, không bình phương từng ô.
    2. Hàng 1: (-1, 6). Hàng 2: (-3, 2).
    3. Nhập theo từng hàng: -1, 6, -3, 2.
  - **Câu hỏi:** Cho ma trận A như hình. Tính A^2. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-3, -2); (-2, 2)  (từng hàng)
  - **Đáp án:** 13, 2, 2, 8
    1. A^2 = A . A: nhân hàng của A với cột của A, không bình phương từng ô.
    2. Hàng 1: (13, 2). Hàng 2: (2, 8).
    3. Nhập theo từng hàng: 13, 2, 2, 8.
  - **Câu hỏi:** Cho ma trận A như hình. Tính A^2. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (0, -1); (2, 4)  (từng hàng)
  - **Đáp án:** -2, -4, 8, 14
    1. A^2 = A . A: nhân hàng của A với cột của A, không bình phương từng ô.
    2. Hàng 1: (-2, -4). Hàng 2: (8, 14).
    3. Nhập theo từng hàng: -2, -4, 8, 14.
- `dstt_t4_lt_03` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận chéo A cấp 3 có đường chéo chính là 2, -1, 3. Tính A^4 và nhập ba phần tử trên đường chéo chính của nó, theo thứ tự.
  - **Đáp án:** 16, 1, 81
    1. Tích của hai ma trận chéo là ma trận chéo, với đường chéo là tích từng cặp phần tử.
    2. Vậy A^4 là ma trận chéo có đường chéo 2^4, (-1)^4, 3^4.
    3. Đó là 16, 1, 81.
- `dstt_t4_lt_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. A^2025 bằng ma trận nào?
  - A = (0, 1); (1, 0)  (từng hàng)
    - **(đúng)** A
    - I
    - Ma trận không
    - -A
  - **Đáp án:** A
    1. A^2 có hàng (0 . 0 + 1 . 1, 0 . 1 + 1 . 0) = (1, 0) và (0, 1): A^2 = I.
    2. 2025 = 2 . 1012 + 1, nên A^2025 = (A^2)^1012 . A = I . A.
    3. Vậy A^2025 = A.
- `dstt_t4_lt_05` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính tr(A^2) với A như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (3, 0)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. A là ma trận vuông cấp 2 nên A^2 = A . A xác định.
    2. Bình phương từng phần tử: A^2 có hàng (1, 4) và (9, 0).   **<- bước sai đầu tiên**
    3. Vậy tr(A^2) = 1 + 0 = 1.
  - **Đáp án:** Bước 2: Bình phương từng phần tử: A^2 có hàng (1, 4) và (9, 0).
  - **Vì sao sai, và bước đúng:**
    1. A^2 là tích ma trận A . A, không phải bình phương từng ô.
    2. Đúng ra: A^2 có hàng (1 + 6, 2 + 0) = (7, 2) và (3 + 0, 6 + 0) = (3, 6), nên tr(A^2) = 7 + 6 = 13.
- `dstt_t4_lt_06` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Sắp xếp các bước tìm phần tử ở hàng 1, cột 2 của A^3.
  - A = (1, 1); (0, 2)  (từng hàng)
  - **Đáp án (thứ tự đúng):**
    1. A^3 = A^2 . A, nên tính A^2 trước.
    2. A^2 = A . A có hàng (1, 3) và (0, 4).
    3. Nhân A^2 với A: A^3 có hàng (1, 7) và (0, 8).
    4. Phần tử ở hàng 1, cột 2 của A^3 là 7.
  - **Lời giải:**
    1. A^2: hàng 1 là (1 . 1 + 1 . 0, 1 . 1 + 1 . 2) = (1, 3), hàng 2 là (0, 4).
    2. A^3 = A^2 . A: hàng 1 là (1, 1 + 6) = (1, 7), hàng 2 là (0, 8).
    3. Phần tử cần tìm là 7. Không được lũy thừa từng ô: 1^3 = 1 khác 7.
- `dstt_g4_luy_thua_n` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần tử ở hàng 1, cột 2 của A^12.
  - A = (1, -3); (0, 1)  (từng hàng)
  - **Đáp án:** -36
    1. A^2 = A . A có phần tử ở hàng 1, cột 2 bằng -3 + (-3) = -6, các phần tử khác như của A.
    2. Mỗi lần nhân thêm A, phần tử ở hàng 1, cột 2 tăng thêm -3, còn đường chéo vẫn là 1.
    3. Vậy A^12 có phần tử ở hàng 1, cột 2 bằng 12 . (-3) = -36.
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần tử ở hàng 1, cột 2 của A^4.
  - A = (1, -5); (0, 1)  (từng hàng)
  - **Đáp án:** -20
    1. A^2 = A . A có phần tử ở hàng 1, cột 2 bằng -5 + (-5) = -10, các phần tử khác như của A.
    2. Mỗi lần nhân thêm A, phần tử ở hàng 1, cột 2 tăng thêm -5, còn đường chéo vẫn là 1.
    3. Vậy A^4 có phần tử ở hàng 1, cột 2 bằng 4 . (-5) = -20.
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần tử ở hàng 1, cột 2 của A^12.
  - A = (1, -2); (0, 1)  (từng hàng)
  - **Đáp án:** -24
    1. A^2 = A . A có phần tử ở hàng 1, cột 2 bằng -2 + (-2) = -4, các phần tử khác như của A.
    2. Mỗi lần nhân thêm A, phần tử ở hàng 1, cột 2 tăng thêm -2, còn đường chéo vẫn là 1.
    3. Vậy A^12 có phần tử ở hàng 1, cột 2 bằng 12 . (-2) = -24.

## Tầng 5: Hệ phương trình tuyến tính và khử Gauss

47 dạng câu (39 câu viết tay, 8 bộ sinh câu); 47 chưa duyệt.

### Viết hệ dưới dạng Ax = b (`dstt_t5_dang_ma_tran`)

- `dstt_t5_dmt_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ x + 2y - z = 3, 2x - y = 1, y + 4z = -2 (ẩn x, y, z) viết được dưới dạng Ax = b. Ma trận A là ma trận nào, cho bởi ba hàng?
    - **(đúng)** (1, 2, -1), (2, -1, 0), (0, 1, 4)
    - (1, 2, -1), (2, -1, 1), (1, 4, -2)
    - (1, 2, 0), (2, -1, 1), (-1, 0, 4)
    - (1, 2, 3), (2, -1, 1), (1, 4, -2)
  - **Đáp án:** (1, 2, -1), (2, -1, 0), (0, 1, 4)
    1. Mỗi phương trình cho một hàng của A; mỗi ẩn x, y, z cho một cột.
    2. Ẩn vắng mặt có hệ số 0: phương trình 2 không có z, phương trình 3 không có x.
    3. A có các hàng (1, 2, -1), (2, -1, 0), (0, 1, 4); vế phải b = (3, 1, -2) không nằm trong A.
- `dstt_t5_dmt_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hệ m phương trình tuyến tính, n ẩn viết dưới dạng Ax = b thì A có cỡ m x n và x có n tọa độ.
  - **Đáp án:** Đúng
    1. Mỗi phương trình là một hàng của A, nên A có m hàng.
    2. Mỗi ẩn là một cột của A, nên A có n cột; x là cột gồm n ẩn.
    3. Ax có cỡ (m x n)(n x 1) = m x 1, khớp với b có m tọa độ.
- `dstt_t5_dmt_05` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ẩn là x rồi y. Ghép mỗi hệ với ma trận bổ sung của nó, viết theo từng hàng (hệ số | vế phải).
  - **Đáp án (ghép đúng):**
    - x + y = 2 và x - y = 0 — (1, 1 | 2) và (1, -1 | 0)
    - x = 2 và y = 0 — (1, 0 | 2) và (0, 1 | 0)
    - x + y = 0 và x - y = 2 — (1, 1 | 0) và (1, -1 | 2)
    - y = 2 và x = 0 — (0, 1 | 2) và (1, 0 | 0)
  - **Lời giải:**
    1. Mỗi phương trình là một hàng: hệ số của x, hệ số của y, rồi vế phải sau dấu |.
    2. Ẩn vắng mặt có hệ số 0: x = 2 cho hàng (1, 0 | 2), y = 2 cho hàng (0, 1 | 2).
    3. Thứ tự hàng theo thứ tự phương trình, nên y = 2 và x = 0 cho (0, 1 | 2) rồi (1, 0 | 0).
- `dstt_g5_tim_b` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hệ Ax = b có ma trận hệ số A như hình (ẩn x, y, z) và nhận (x, y, z) = (-3, 0, -3) làm nghiệm. Tìm vế phải b. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
  - A = (-1, -2, 1); (-2, 4, 4); (4, 3, 0)  (từng hàng)
  - **Đáp án:** 0, -6, -12
    1. Vì (x, y, z) là nghiệm nên b = A nhân vectơ nghiệm: mỗi tọa độ của b là một hàng của A nhân với nghiệm.
    2. Hàng 1: (-1) . (-3) + (-2) . 0 + 1 . (-3) = 0.
    3. Hàng 2: (-2) . (-3) + 4 . 0 + 4 . (-3) = -6.
    4. Hàng 3: 4 . (-3) + 3 . 0 + 0 . (-3) = -12.
    5. b = (0, -6, -12).
  - **Câu hỏi:** Hệ Ax = b có ma trận hệ số A như hình (ẩn x, y, z) và nhận (x, y, z) = (1, 2, -2) làm nghiệm. Tìm vế phải b. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
  - A = (-3, -2, -2); (2, -1, 1); (1, 0, -3)  (từng hàng)
  - **Đáp án:** -3, -2, 7
    1. Vì (x, y, z) là nghiệm nên b = A nhân vectơ nghiệm: mỗi tọa độ của b là một hàng của A nhân với nghiệm.
    2. Hàng 1: (-3) . 1 + (-2) . 2 + (-2) . (-2) = -3.
    3. Hàng 2: 2 . 1 + (-1) . 2 + 1 . (-2) = -2.
    4. Hàng 3: 1 . 1 + 0 . 2 + (-3) . (-2) = 7.
    5. b = (-3, -2, 7).
  - **Câu hỏi:** Hệ Ax = b có ma trận hệ số A như hình (ẩn x, y, z) và nhận (x, y, z) = (-2, 2, 0) làm nghiệm. Tìm vế phải b. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
  - A = (0, -1, 2); (4, -2, -3); (4, 1, 0)  (từng hàng)
  - **Đáp án:** -2, -12, -6
    1. Vì (x, y, z) là nghiệm nên b = A nhân vectơ nghiệm: mỗi tọa độ của b là một hàng của A nhân với nghiệm.
    2. Hàng 1: 0 . (-2) + (-1) . 2 + 2 . 0 = -2.
    3. Hàng 2: 4 . (-2) + (-2) . 2 + (-3) . 0 = -12.
    4. Hàng 3: 4 . (-2) + 1 . 2 + 0 . 0 = -6.
    5. b = (-2, -12, -6).
- `dstt_t5_dmt_03` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A và vectơ b. Nếu u và v đều là nghiệm của Ax = b thì u - v là nghiệm của Ax = 0.
  - **Đáp án:** Đúng
    1. Phép nhân ma trận phân phối với phép trừ: A(u - v) = Au - Av.
    2. Au = b và Av = b, nên A(u - v) = b - b = 0.
    3. Vậy hai nghiệm của cùng một hệ chỉ khác nhau một nghiệm của hệ thuần nhất.
- `dstt_t5_dmt_04` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A và vectơ b khác 0. Nếu u và v đều là nghiệm của Ax = b thì u + v cũng là nghiệm của Ax = b.
  - **Đáp án:** Sai
    1. A(u + v) = Au + Av = b + b = 2b.
    2. b khác 0 nên 2b khác b.
    3. Vậy u + v không phải là nghiệm của Ax = b. Tổng hai nghiệm chỉ còn là nghiệm khi hệ thuần nhất.
- `dstt_t5_dmt_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ ba phương trình, hai ẩn x, y có ma trận bổ sung như hình (cột cuối là vế phải), trong đó k là một số. Tìm k để x = 1, y = 2 là nghiệm của hệ.
  - M = (1, 1, 3); (2, -1, 0); (k, 1, 5)  (từng hàng)
  - **Đáp án:** 3
    1. Hàng 1: 1 + 2 = 3 và hàng 2: 2 - 2 = 0 đều đúng với x = 1, y = 2.
    2. Hàng 3 là phương trình kx + y = 5; thay x = 1, y = 2: k + 2 = 5.
    3. Vậy k = 3.

### Ba phép biến đổi sơ cấp trên hàng (`dstt_t5_bien_doi_hang`)

- `dstt_t5_bdh_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phép nào sau đây KHÔNG phải là một phép biến đổi sơ cấp trên hàng?
    - **(đúng)** Nhân hàng 1 với 0
    - Đổi chỗ hàng 1 và hàng 3
    - Nhân hàng 2 với -3
    - Cộng 2 lần hàng 1 vào hàng 3
  - **Đáp án:** Nhân hàng 1 với 0
    1. Ba phép sơ cấp là: đổi chỗ hai hàng, nhân một hàng với một số khác 0, cộng bội của một hàng vào hàng khác.
    2. Nhân một hàng với 0 xóa mất một phương trình và không đảo ngược được, nên bị loại.
    3. Ba phép còn lại đều là phép sơ cấp.
- `dstt_t5_bdh_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi phép biến đổi sơ cấp trên hàng của ma trận bổ sung không làm thay đổi tập nghiệm của hệ.
  - **Đáp án:** Đúng
    1. Mỗi phép sơ cấp đều có phép ngược cũng là phép sơ cấp: đổi chỗ lại, chia cho số khác 0, trừ lại bội đã cộng.
    2. Một nghiệm của hệ cũ thỏa hệ mới, và nhờ phép ngược, nghiệm của hệ mới cũng thỏa hệ cũ.
    3. Vì vậy khử Gauss giữ nguyên tập nghiệm.
- `dstt_t5_bdh_06` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi ký hiệu biến đổi hàng với ý nghĩa của nó.
  - **Đáp án (ghép đúng):**
    - R1 <-> R3 — đổi chỗ hàng 1 và hàng 3
    - R2 <- 5R2 — nhân hàng 2 với 5
    - R3 <- R3 + 5R2 — cộng 5 lần hàng 2 vào hàng 3
    - R2 <- R2 + 5R3 — cộng 5 lần hàng 3 vào hàng 2
  - **Lời giải:**
    1. R_i <-> R_j đổi chỗ hai hàng; R_i <- kR_i nhân hàng i với k.
    2. R_i <- R_i + kR_j cộng k lần hàng j vào hàng i: hàng bị thay là hàng đứng bên trái mũi tên.
    3. Vì vậy R3 <- R3 + 5R2 sửa hàng 3, còn R2 <- R2 + 5R3 sửa hàng 2.
- `dstt_g5_cong_boi_hang` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Làm phép R1 <- R1 + R3. Nhập hàng 1 mới, cách nhau bằng dấu phẩy.
  - A = (-2, 5, -3); (0, -3, 3); (3, 3, 2)  (từng hàng)
  - **Đáp án:** 1, 8, -1
    1. Phép này chỉ thay hàng 1: lấy hàng 1 cộng 1 lần hàng 3; hàng 3 giữ nguyên.
    2. Hàng 1 là (-2, 5, -3), 1 lần hàng 3 là (3, 3, 2).
    3. Cộng từng tọa độ: (1, 8, -1).
  - **Câu hỏi:** Cho ma trận A như hình. Làm phép R3 <- R3 + 2R1. Nhập hàng 3 mới, cách nhau bằng dấu phẩy.
  - A = (-4, -3, -3); (1, -2, 0); (0, 5, -1)  (từng hàng)
  - **Đáp án:** -8, -1, -7
    1. Phép này chỉ thay hàng 3: lấy hàng 3 cộng 2 lần hàng 1; hàng 1 giữ nguyên.
    2. Hàng 3 là (0, 5, -1), 2 lần hàng 1 là (-8, -6, -6).
    3. Cộng từng tọa độ: (-8, -1, -7).
  - **Câu hỏi:** Cho ma trận A như hình. Làm phép R3 <- R3 + R1. Nhập hàng 3 mới, cách nhau bằng dấu phẩy.
  - A = (-1, 5, 4); (-2, 1, 5); (3, 5, -3)  (từng hàng)
  - **Đáp án:** 2, 10, 1
    1. Phép này chỉ thay hàng 3: lấy hàng 3 cộng 1 lần hàng 1; hàng 1 giữ nguyên.
    2. Hàng 3 là (3, 5, -3), 1 lần hàng 1 là (-1, 5, 4).
    3. Cộng từng tọa độ: (2, 10, 1).
- `dstt_t5_bdh_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau giải hệ x + 2y = 3, 3x + 4y = 5 bằng biến đổi hàng trên ma trận bổ sung. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận bổ sung có hàng 1 là (1, 2 | 3) và hàng 2 là (3, 4 | 5); để khử x ở hàng 2, làm R2 <- R2 - 3R1.
    2. 3R1 = (3, 6 | 9).
    3. R2 - 3R1 = (3 - 3, 4 - 6 | 5 + 9) = (0, -2 | 14).   **<- bước sai đầu tiên**
    4. Từ -2y = 14 được y = -7, rồi x = 3 - 2 . (-7) = 17.
  - **Đáp án:** Bước 3: R2 - 3R1 = (3 - 3, 4 - 6 | 5 + 9) = (0, -2 | 14).
  - **Vì sao sai, và bước đúng:**
    1. Ở cột vế phải phải trừ như mọi cột khác: 5 - 9 = -4, không phải 5 + 9.
    2. Đúng ra: hàng 2 thành (0, -2 | -4), nên y = 2 và x = 3 - 4 = -1. Thử lại: -1 + 4 = 3 và -3 + 8 = 5.
- `dstt_t5_bdh_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau khử Gauss hệ 2y = 4, x + y = 3 (ẩn x rồi y). Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận bổ sung có hàng 1 là (0, 2 | 4) và hàng 2 là (1, 1 | 3).
    2. Chia hàng 1 cho phần tử đầu tiên của nó để được số 1 ở góc trên bên trái.   **<- bước sai đầu tiên**
    3. Sau đó lấy R2 - R1 để khử x ở hàng 2.
    4. Hàng 2 thành (0, 0 | 0), nên hệ có vô số nghiệm.
  - **Đáp án:** Bước 2: Chia hàng 1 cho phần tử đầu tiên của nó để được số 1 ở góc trên bên trái.
  - **Vì sao sai, và bước đúng:**
    1. Phần tử đầu tiên của hàng 1 là 0, và không được chia cho 0. Khi trụ bằng 0 thì đổi chỗ với một hàng bên dưới có phần tử khác 0 ở cột đó.
    2. Đúng ra: đổi chỗ hai hàng, được (1, 1 | 3) và (0, 2 | 4). Từ đó y = 2, x = 1: hệ có nghiệm duy nhất.
- `dstt_t5_bdh_05` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Làm lần lượt hai phép: đổi chỗ hàng 1 và hàng 2, rồi R2 <- R2 - 2R1 (trên ma trận đã đổi chỗ). Nhập hàng 2 của kết quả, cách nhau bằng dấu phẩy.
  - A = (1, 3, -1); (2, 1, 4); (0, 1, 1)  (từng hàng)
  - **Đáp án:** -3, 1, -9
    1. Sau khi đổi chỗ: hàng 1 là (2, 1, 4), hàng 2 là (1, 3, -1).
    2. R2 - 2R1 = (1 - 4, 3 - 2, -1 - 8).
    3. Hàng 2 mới là (-3, 1, -9). Làm theo thứ tự khác sẽ ra kết quả khác.
- `dstt_t5_bdh_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Làm cùng lúc hai phép R1 <- R1 + R2 và R2 <- R2 + R1, mỗi phép đều dùng các hàng cũ, thì tập nghiệm của mọi hệ hai phương trình đều giữ nguyên.
  - **Đáp án:** Sai
    1. Làm cùng lúc như vậy thì cả hai hàng mới đều bằng R1 + R2 cũ: hệ chỉ còn một phương trình.
    2. Ví dụ hệ x = 1, y = 2 có nghiệm duy nhất; sau phép này cả hai hàng là x + y = 3, có vô số nghiệm.
    3. Phải làm từng phép một, mỗi phép chỉ thay một hàng.

### Khử Gauss về dạng bậc thang (`dstt_t5_bac_thang`)

- `dstt_t5_bt_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình có dạng bậc thang.
  - A = (1, 2, 0, 3); (0, 0, 1, 4); (0, 0, 0, 0)  (từng hàng)
  - **Đáp án:** Đúng
    1. Dạng bậc thang: hàng toàn số 0 nằm dưới cùng, và phần tử khác 0 đầu tiên của mỗi hàng nằm bên phải phần tử khác 0 đầu tiên của hàng trên.
    2. Hàng 1 bắt đầu ở cột 1, hàng 2 bắt đầu ở cột 3, hàng 3 toàn số 0 và nằm dưới cùng.
    3. A thỏa cả hai điều kiện.
- `dstt_t5_bt_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận nào sau đây, cho bởi ba hàng, có dạng bậc thang?
    - **(đúng)** (1, 2, 3), (0, 4, 5), (0, 0, 6)
    - (1, 2, 3), (0, 0, 5), (0, 4, 6)
    - (0, 0, 0), (1, 2, 3), (0, 1, 4)
    - (1, 2, 3), (2, 4, 5), (0, 0, 6)
  - **Đáp án:** (1, 2, 3), (0, 4, 5), (0, 0, 6)
    1. (1, 2, 3), (0, 4, 5), (0, 0, 6): các phần tử khác 0 đầu tiên ở cột 1, 2, 3, lùi dần sang phải.
    2. Ma trận thứ hai có hàng 3 bắt đầu ở cột 2, trước hàng 2 bắt đầu ở cột 3; ma trận thứ ba có hàng 0 nằm trên cùng.
    3. Ma trận cuối có hàng 2 bắt đầu ở cột 1, cùng cột với hàng 1.
- `dstt_t5_bt_03` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ x + y + z = 6, x + 2y + 3z = 14, x + 3y + 6z = 25 có ma trận bổ sung với các hàng (1, 1, 1 | 6), (1, 2, 3 | 14), (1, 3, 6 | 25). Sắp xếp các bước đưa nó về dạng bậc thang.
  - **Đáp án (thứ tự đúng):**
    1. Dùng hàng 1 khử x ở hai hàng dưới: R2 <- R2 - R1 và R3 <- R3 - R1.
    2. Được hàng 2 là (0, 1, 2 | 8) và hàng 3 là (0, 2, 5 | 19).
    3. Dùng hàng 2 khử y ở hàng 3: R3 <- R3 - 2R2.
    4. Hàng 3 thành (0, 0, 1 | 3): ma trận đã có dạng bậc thang.
  - **Lời giải:**
    1. Khử Gauss đi từng cột từ trái sang phải: trước hết làm cột x bằng 0 bên dưới trụ của hàng 1.
    2. Sau đó dùng trụ của hàng 2 để làm cột y bằng 0 ở hàng 3.
    3. Từ dạng bậc thang, thế ngược cho z = 3, y = 2, x = 1.
- `dstt_t5_bt_07` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cần đưa ma trận bổ sung M như hình về dạng bậc thang. Bước đầu tiên hợp lý là bước nào?
  - M = (0, 2, 1, 3); (1, 1, 0, 2); (2, 0, 1, 1)  (từng hàng)
    - **(đúng)** Đổi chỗ hàng 1 với hàng 2
    - Chia hàng 1 cho phần tử đầu tiên của nó
    - Bỏ hàng 1 đi
    - Nhân hàng 1 với 0
  - **Đáp án:** Đổi chỗ hàng 1 với hàng 2
    1. Trụ của cột 1 phải là một số khác 0 ở hàng 1, mà hàng 1 hiện bắt đầu bằng 0.
    2. Đổi chỗ với hàng 2, có phần tử đầu là 1, là phép sơ cấp và cho ngay trụ bằng 1.
    3. Không được chia cho 0, còn bỏ hàng hay nhân hàng với 0 làm mất một phương trình.
- `dstt_t5_bac_thang_91` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đệ tử giải hệ ba phương trình: (1) x + y + z = 6, (2) 2x + 3y + z = 11, (3) x - y + 2z = 5. Ma trận mở rộng của hệ là A.
  - A = (1, 1, 1, 6); (2, 3, 1, 11); (1, -1, 2, 5)  (từng hàng)
  - **Phần a** (Trắc nghiệm): a) Phép biến đổi nào khử được x khỏi phương trình (2)?
    - **(đúng)** (2) - 2*(1)
    - (2) - (1)
    - (2) + 2*(1)
    - (2) - 3*(1)
    - **Đáp án a:** (2) - 2*(1)
  - **Phần b** (Điền số): b) Khử Gauss rồi thế ngược. Nhập nghiệm x, y, z theo đúng thứ tự, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 1, 2, 3
  - **Phần c** (Đúng/Sai): c) Dạng bậc thang của A có ba phần tử trụ, nên hệ có đúng một nghiệm.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Phương trình (2) có 2x, phương trình (1) có x: lấy (2) - 2*(1) thì x mất, được y - z = -1.
    2. b) Lấy (3) - (1): -2y + z = -1. Cộng với y - z = -1: -y = -2, nên y = 2.
    3. b) Thế ngược: z = y + 1 = 3, rồi từ (1): x = 6 - 2 - 3 = 1. Nghiệm (1, 2, 3); thử lại cả ba phương trình đều đúng.
    4. c) Ba cột x, y, z đều có trụ (1, 1 và -1 sau khi khử), không có ẩn tự do: hệ có đúng một nghiệm. Mệnh đề đúng.
- `dstt_t5_bt_04` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khử Gauss ma trận A như hình chỉ bằng các phép R_i <- R_i + kR_j với hàng j nằm trên hàng i, không đổi chỗ hàng và không nhân hàng với số. Phần tử ở hàng 3, cột 3 của dạng bậc thang thu được bằng bao nhiêu?
  - A = (1, 2, 1); (2, 5, 3); (1, 3, 4)  (từng hàng)
  - **Đáp án:** 2
    1. R2 <- R2 - 2R1 cho (0, 1, 1); R3 <- R3 - R1 cho (0, 1, 3).
    2. R3 <- R3 - R2 cho (0, 0, 2).
    3. Dạng bậc thang có hàng (1, 2, 1), (0, 1, 1), (0, 0, 2): phần tử cần tìm là 2.
- `dstt_t5_bt_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau giải hệ x + 2y = 5, 2x + 3y = 8 bằng khử Gauss. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận bổ sung có hàng (1, 2 | 5) và (2, 3 | 8); khử x ở hàng 2 bằng R2 <- R2 - 2R1.
    2. Phần hệ số của hàng 2 thành (2 - 2, 3 - 4) = (0, -1).
    3. Cột vế phải không đổi khi biến đổi hàng, nên hàng 2 thành (0, -1 | 8).   **<- bước sai đầu tiên**
    4. Vậy y = -8 và x = 5 - 2 . (-8) = 21.
  - **Đáp án:** Bước 3: Cột vế phải không đổi khi biến đổi hàng, nên hàng 2 thành (0, -1 | 8).
  - **Vì sao sai, và bước đúng:**
    1. Phép biến đổi hàng làm trên cả hàng, kể cả vế phải: 8 - 2 . 5 = -2.
    2. Đúng ra: hàng 2 thành (0, -1 | -2), nên y = 2 và x = 5 - 4 = 1. Thử lại: 1 + 4 = 5 và 2 + 6 = 8.
- `dstt_t5_bt_06` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi ma trận chỉ có đúng một dạng bậc thang, dù khử Gauss theo cách nào.
  - **Đáp án:** Sai
    1. Nhân một hàng của dạng bậc thang với một số khác 0 vẫn được dạng bậc thang, mà là một ma trận khác.
    2. Ví dụ ma trận có hàng (1, 1) và (1, 3) cho được cả dạng (1, 1), (0, 2) lẫn dạng (1, 1), (0, 1).
    3. Chỉ dạng bậc thang rút gọn (trụ bằng 1, phía trên trụ toàn số 0) mới là duy nhất; còn vị trí các trụ thì luôn như nhau.

### Thế ngược tìm nghiệm (`dstt_t5_the_nguoc`)

- `dstt_t5_tn_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận bổ sung của hệ ẩn x, y, z đã ở dạng bậc thang, với các hàng (1, 1, 2 | 9), (0, 2, -1 | 1), (0, 0, 3 | 6). Tìm nghiệm. Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
  - **Đáp án:** 7/2, 3/2, 2
    1. Hàng 3: 3z = 6 nên z = 2.
    2. Hàng 2: 2y - z = 1 nên 2y = 3, y = 3/2.
    3. Hàng 1: x + y + 2z = 9 nên x = 9 - 3/2 - 4 = 7/2.
- `dstt_t5_tn_02` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận bổ sung của hệ ẩn x, y, z có dạng bậc thang với các hàng (1, -1, 1 | 2), (0, 1, 2 | 7), (0, 0, 2 | 4). Sắp xếp các bước thế ngược.
  - **Đáp án (thứ tự đúng):**
    1. Từ hàng 3: 2z = 4 nên z = 2.
    2. Thay z = 2 vào hàng 2: y + 4 = 7 nên y = 3.
    3. Thay y = 3 và z = 2 vào hàng 1: x - 3 + 2 = 2 nên x = 3.
    4. Nghiệm của hệ là (x, y, z) = (3, 3, 2).
  - **Lời giải:**
    1. Thế ngược đi từ phương trình cuối, chỉ có một ẩn, lên phương trình đầu.
    2. Mỗi bước dùng các ẩn đã tìm ở bước trước.
    3. Thử lại hàng 1: 3 - 3 + 2 = 2.
- `dstt_t5_tn_05` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Khi thế ngược trên dạng bậc thang có nghiệm duy nhất, ta giải phương trình cuối cùng trước tiên.
  - **Đáp án:** Đúng
    1. Ở dạng bậc thang, phương trình cuối chứa ít ẩn nhất, nên giải được ngay.
    2. Ẩn vừa tìm được thay vào phương trình ngay trên nó, rồi cứ thế đi lên.
    3. Vì vậy cách làm này gọi là thế ngược.
- `dstt_g5_giai_he_2` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải hệ -2x - 3y = -10 và -3y = -6. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 2
    1. Ma trận bổ sung có hàng (-2, -3 | -10) và (0, -3 | -6).
    2. Hàng 2 không có x; nhân nó với (-2) cho gọn: (0, 6 | 12).
    3. Từ hàng 2: y = 2.
    4. Thế vào hàng 1: (-2)x = -10 - (-3) . 2, nên x = 2.
  - **Câu hỏi:** Giải hệ -4x - 3y = -3 và -3x + y = 14. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - **Đáp án:** -3, 5
    1. Ma trận bổ sung có hàng (-4, -3 | -3) và (-3, 1 | 14).
    2. Khử x ở hàng 2: R2 <- (-4) . R2 - (-3) . R1, được (0, -13 | -65).
    3. Từ hàng 2: y = 5.
    4. Thế vào hàng 1: (-4)x = -3 - (-3) . 5, nên x = -3.
  - **Câu hỏi:** Giải hệ -x + 4y = 4 và -2x + y = -6. Nhập x rồi y, cách nhau bằng dấu phẩy.
  - **Đáp án:** 4, 2
    1. Ma trận bổ sung có hàng (-1, 4 | 4) và (-2, 1 | -6).
    2. Khử x ở hàng 2: R2 <- (-1) . R2 - (-2) . R1, được (0, 7 | 14).
    3. Từ hàng 2: y = 2.
    4. Thế vào hàng 1: (-1)x = 4 - 4 . 2, nên x = 4.
- `dstt_t5_tn_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận bổ sung của hệ ẩn x, y, z có dạng bậc thang với các hàng (1, 2, -1 | 3), (0, 1, 1 | 2), (0, 0, 0 | 0). Trong các nghiệm của hệ, tìm nghiệm có x = 5. Nhập x, y, z theo thứ tự.
  - **Đáp án:** 5, 0, 2
    1. z không có trụ nên là ẩn tự do: đặt z = t.
    2. Hàng 2: y = 2 - t. Hàng 1: x = 3 - 2(2 - t) + t = -1 + 3t.
    3. x = 5 cho t = 2, nên y = 0 và z = 2.
- `dstt_t5_tn_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ ẩn x, y, z có ma trận bổ sung dạng bậc thang với các hàng (2, 1, -1 | 3), (0, 1, 3 | 5), (0, 0, 2 | 4). Lời giải sau thế ngược. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàng 3: 2z = 4 nên z = 2.
    2. Hàng 2: y + 3 . 2 = 5 nên y = -1.
    3. Hàng 1: 2x + (-1) - 2 = 3, nên 2x = 3 - 1 - 2 = 0.   **<- bước sai đầu tiên**
    4. Vậy x = 0 và nghiệm là (0, -1, 2).
  - **Đáp án:** Bước 3: Hàng 1: 2x + (-1) - 2 = 3, nên 2x = 3 - 1 - 2 = 0.
  - **Vì sao sai, và bước đúng:**
    1. Chuyển -1 và -2 sang vế phải thì phải đổi dấu: 2x = 3 + 1 + 2.
    2. Đúng ra: 2x = 6, x = 3. Nghiệm là (3, -1, 2); thử lại hàng 1: 6 - 1 - 2 = 3.
- `dstt_t5_tn_06` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một đệ tử cần giải hệ x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14 bằng khử Gauss trên ma trận bổ sung, rồi thế ngược.
  - **Phần a** (Điền số): a) Làm R2 <- R2 - 2R1. Nhập hàng 2 mới, gồm ba hệ số rồi vế phải, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 0, 1, -1, -1
  - **Phần b** (Điền số): b) Làm tiếp R3 <- R3 - R1, rồi R3 <- R3 - R2. Khi đó hàng 3 chỉ còn ẩn z. Tìm z.
    - **Đáp án b:** 3
  - **Phần c** (Điền số): c) Thế ngược. Nhập nghiệm x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
    - **Đáp án c:** 1, 2, 3
  - **Lời giải:**
    1. a) R2 - 2R1 = (2 - 2, 3 - 2, 1 - 2 | 11 - 12) = (0, 1, -1 | -1).
    2. b) R3 - R1 = (0, 1, 2 | 8); trừ tiếp hàng 2 mới: (0, 0, 3 | 9), nên 3z = 9, z = 3.
    3. c) Hàng 2: y - z = -1 nên y = 2; hàng 1: x = 6 - 2 - 3 = 1. Thử lại: 2 + 6 + 3 = 11 và 1 + 4 + 9 = 14.
- `dstt_g5_giai_he_3` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Giải hệ ba phương trình, ba ẩn x, y, z có ma trận bổ sung M như hình (cột cuối là vế phải). Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
  - M = (1, 1, 3, -8); (-2, -1, -5, 11); (1, 2, 6, -19)  (từng hàng)
  - **Đáp án:** 3, -2, -3
    1. Khử Gauss, không cần đổi chỗ hàng: dùng hàng 1 khử x ở hàng 2 và 3, rồi dùng hàng 2 mới khử y ở hàng 3.
    2. Dạng bậc thang có các hàng (1, 1, 3 | -8), (0, 1, 1 | -5), (0, 0, 2 | -6).
    3. Thế ngược: z = -6/2 = -3, rồi y = -2, rồi x = 3.
    4. Nghiệm (x, y, z) = (3, -2, -3).
  - **Câu hỏi:** Giải hệ ba phương trình, ba ẩn x, y, z có ma trận bổ sung M như hình (cột cuối là vế phải). Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
  - M = (1, 0, 2, 3); (0, 1, -1, -4); (-1, 0, -1, -2)  (từng hàng)
  - **Đáp án:** 1, -3, 1
    1. Khử Gauss, không cần đổi chỗ hàng: dùng hàng 1 khử x ở hàng 2 và 3, rồi dùng hàng 2 mới khử y ở hàng 3.
    2. Dạng bậc thang có các hàng (1, 0, 2 | 3), (0, 1, -1 | -4), (0, 0, 1 | 1).
    3. Thế ngược: z = 1/1 = 1, rồi y = -3, rồi x = 1.
    4. Nghiệm (x, y, z) = (1, -3, 1).
  - **Câu hỏi:** Giải hệ ba phương trình, ba ẩn x, y, z có ma trận bổ sung M như hình (cột cuối là vế phải). Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
  - M = (1, -2, 2, 1); (2, -5, 2, 4); (1, -4, 0, 3)  (từng hàng)
  - **Đáp án:** 3, 0, -1
    1. Khử Gauss, không cần đổi chỗ hàng: dùng hàng 1 khử x ở hàng 2 và 3, rồi dùng hàng 2 mới khử y ở hàng 3.
    2. Dạng bậc thang có các hàng (1, -2, 2 | 1), (0, -1, -2 | 2), (0, 0, 2 | -2).
    3. Thế ngược: z = -2/2 = -1, rồi y = 0, rồi x = 3.
    4. Nghiệm (x, y, z) = (3, 0, -1).

### Biện luận số nghiệm (`dstt_t5_so_nghiem`)

- `dstt_t5_sn_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ ẩn x, y, z có ma trận bổ sung M như hình, đã ở dạng bậc thang (cột cuối là vế phải). Hệ có bao nhiêu nghiệm?
  - M = (1, 2, 3, 4); (0, 1, 1, 2); (0, 0, 0, 5)  (từng hàng)
    - **(đúng)** Vô nghiệm
    - Nghiệm duy nhất
    - Vô số nghiệm, với một ẩn tự do
    - Vô số nghiệm, với hai ẩn tự do
  - **Đáp án:** Vô nghiệm
    1. Hàng 3 nói 0x + 0y + 0z = 5, tức là 0 = 5.
    2. Không có bộ số nào thỏa phương trình đó.
    3. Một hàng (0, ..., 0 | khác 0) trong dạng bậc thang luôn có nghĩa là hệ vô nghiệm.
- `dstt_t5_sn_02` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi vế trái là ma trận bổ sung dạng bậc thang của một hệ hai ẩn, viết theo từng hàng. Ghép với số nghiệm của hệ.
  - **Đáp án (ghép đúng):**
    - (1, 2 | 3) và (0, 1 | 4) — nghiệm duy nhất
    - (1, 2 | 3) và (0, 0 | 4) — vô nghiệm
    - (1, 2 | 3) và (0, 0 | 0) — vô số nghiệm
  - **Lời giải:**
    1. (0, 1 | 4): mỗi ẩn có một trụ, nên nghiệm duy nhất (y = 4, x = -5).
    2. (0, 0 | 4) nghĩa là 0 = 4: vô nghiệm.
    3. (0, 0 | 0) là hàng thừa: còn một phương trình cho hai ẩn, y tự do, nên vô số nghiệm.
- `dstt_t5_sn_04` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hệ x + 2y = 3, 2x + 4y = m, với m là tham số khác 6. Hệ có bao nhiêu nghiệm?
    - **(đúng)** Vô nghiệm
    - Nghiệm duy nhất
    - Vô số nghiệm
    - Đúng hai nghiệm
  - **Đáp án:** Vô nghiệm
    1. R2 - 2R1 cho hàng (0, 0 | m - 6).
    2. Với m khác 6, hàng đó nói 0 = m - 6, một số khác 0.
    3. Vậy hệ vô nghiệm. (Khi m = 6 hệ có vô số nghiệm.)
- `dstt_g5_so_nghiem` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Hệ ẩn x, y, z có ma trận bổ sung M như hình, đã ở dạng bậc thang (cột cuối là vế phải). Hệ vô nghiệm.
  - M = (-1, -2, 4, 2); (0, 1, 3, -2); (0, 0, -3, 2)  (từng hàng)
  - **Đáp án:** Sai
    1. Đọc số nghiệm từ dạng bậc thang: hàng (0, 0, 0 | khác 0) thì vô nghiệm; nếu không, ẩn nào cũng có trụ thì nghiệm duy nhất, còn có ẩn tự do thì vô số nghiệm.
    2. Mỗi ẩn x, y, z đều có trụ và không có hàng (0, 0, 0 | khác 0), nên hệ có nghiệm duy nhất.
    3. Mệnh đề sai: hệ có nghiệm duy nhất.
  - **Câu hỏi:** Hệ ẩn x, y, z có ma trận bổ sung M như hình, đã ở dạng bậc thang (cột cuối là vế phải). Hệ có nghiệm duy nhất.
  - M = (-1, -1, 1, -1); (0, 2, 0, 4); (0, 0, -3, 4)  (từng hàng)
  - **Đáp án:** Đúng
    1. Đọc số nghiệm từ dạng bậc thang: hàng (0, 0, 0 | khác 0) thì vô nghiệm; nếu không, ẩn nào cũng có trụ thì nghiệm duy nhất, còn có ẩn tự do thì vô số nghiệm.
    2. Mỗi ẩn x, y, z đều có trụ và không có hàng (0, 0, 0 | khác 0), nên hệ có nghiệm duy nhất.
    3. Mệnh đề đúng.
  - **Câu hỏi:** Hệ ẩn x, y, z có ma trận bổ sung M như hình, đã ở dạng bậc thang (cột cuối là vế phải). Hệ vô nghiệm.
  - M = (-1, 4, -2, 4); (0, -3, 4, -1); (0, 0, 2, -2)  (từng hàng)
  - **Đáp án:** Sai
    1. Đọc số nghiệm từ dạng bậc thang: hàng (0, 0, 0 | khác 0) thì vô nghiệm; nếu không, ẩn nào cũng có trụ thì nghiệm duy nhất, còn có ẩn tự do thì vô số nghiệm.
    2. Mỗi ẩn x, y, z đều có trụ và không có hàng (0, 0, 0 | khác 0), nên hệ có nghiệm duy nhất.
    3. Mệnh đề sai: hệ có nghiệm duy nhất.
- `dstt_t5_sn_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hệ x + y + z = 1, x + 2y + 3z = 2, 2x + 3y + mz = 3, với m là tham số. Tìm m để hệ có vô số nghiệm.
  - **Đáp án:** 4
    1. R2 - R1 = (0, 1, 2 | 1); R3 - 2R1 = (0, 1, m - 2 | 1).
    2. Trừ tiếp hàng 2: hàng 3 thành (0, 0, m - 4 | 0).
    3. m khác 4 thì nghiệm duy nhất; m = 4 thì hàng 3 là 0 = 0, z tự do, hệ có vô số nghiệm. Hệ không bao giờ vô nghiệm.
- `dstt_t5_sn_05` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu một hệ phương trình tuyến tính có hai nghiệm khác nhau thì nó có vô số nghiệm.
  - **Đáp án:** Đúng
    1. Gọi u, v là hai nghiệm khác nhau của Ax = b; khi đó A(v - u) = 0 và v - u khác 0.
    2. Với mọi số thực t: A(u + t(v - u)) = b + t . 0 = b, nên u + t(v - u) là nghiệm.
    3. Các t khác nhau cho các nghiệm khác nhau, nên có vô số nghiệm. Vì vậy một hệ tuyến tính không thể có đúng hai nghiệm.
- `dstt_t5_sn_06` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau biện luận số nghiệm của hệ x + y + z = 1, 2x + 2y + 2z = 3. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. Hệ có 2 phương trình và 3 ẩn.
    2. Số ẩn nhiều hơn số phương trình, nên hệ chắc chắn có vô số nghiệm.   **<- bước sai đầu tiên**
    3. Chẳng hạn chọn y = z = 0 thì x = 1 là một nghiệm.
  - **Đáp án:** Bước 2: Số ẩn nhiều hơn số phương trình, nên hệ chắc chắn có vô số nghiệm.
  - **Vì sao sai, và bước đúng:**
    1. Nhiều ẩn hơn phương trình chỉ loại trừ khả năng nghiệm duy nhất; hệ vẫn có thể vô nghiệm. Phải khử Gauss để biết.
    2. Đúng ra: R2 - 2R1 cho (0, 0, 0 | 1), tức 0 = 1, nên hệ vô nghiệm. (Bước 3 cũng sai: x = 1, y = z = 0 không thỏa phương trình 2.)
- `dstt_t5_sn_07` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét hệ x + 2y - z = 1, 2x + 5y + z = 4, 3x + 7y + mz = 6, với m là tham số. Khử Gauss: R2 <- R2 - 2R1, R3 <- R3 - 3R1, rồi R3 <- R3 - R2; hàng 3 thu được là (0, 0, m | 1).
  - **Phần a** (Trắc nghiệm): a) Khi m = 0, hệ có bao nhiêu nghiệm?
    - **(đúng)** Vô nghiệm
    - Nghiệm duy nhất
    - Vô số nghiệm
    - **Đáp án a:** Vô nghiệm
  - **Phần b** (Điền số): b) Khi m = 1, tìm nghiệm. Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 4, -1, 1
  - **Phần c** (Đúng/Sai): c) Có một giá trị m làm hệ có vô số nghiệm.
    - **Đáp án c:** Sai
  - **Lời giải:**
    1. Khử: R2 - 2R1 = (0, 1, 3 | 2), R3 - 3R1 = (0, 1, m + 3 | 3), trừ tiếp hàng 2 mới được (0, 0, m | 1).
    2. a) m = 0: hàng 3 là 0 = 1, hệ vô nghiệm.
    3. b) m = 1: z = 1, y = 2 - 3 = -1, x = 1 - 2 . (-1) + 1 = 4. Thử lại hàng 3 gốc: 12 - 7 + 1 = 6.
    4. c) Sai: m khác 0 cho nghiệm duy nhất z = 1/m, m = 0 cho vô nghiệm; vế phải của hàng 3 là 1 khác 0 nên không bao giờ có hàng 0 = 0.
- `dstt_t5_so_nghiem_91` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hệ có tham số m: (1) x + 2y - z = 1, (2) 2x + 5y + z = 4, (3) x + 3y + mz = 3. Con khử x khỏi (2) và (3), rồi khử y khỏi phương trình cuối.
  - **Phần a** (Điền số): a) Sau hai bước khử, phương trình cuối có dạng (m - k)*z = 0. Tìm k.
    - **Đáp án a:** 2
  - **Phần b** (Trắc nghiệm): b) Với m = 2, hệ có bao nhiêu nghiệm?
    - **(đúng)** Vô số nghiệm
    - Đúng một nghiệm
    - Vô nghiệm
    - **Đáp án b:** Vô số nghiệm
  - **Phần c** (Điền số): c) Với m = 5, nhập nghiệm x, y, z theo đúng thứ tự, cách nhau bằng dấu phẩy.
    - **Đáp án c:** -3, 2, 0
  - **Phần d** (Đúng/Sai): d) Có ít nhất một giá trị thực của m làm hệ vô nghiệm.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) (2) - 2*(1): y + 3z = 2. (3) - (1): y + (m + 1)z = 2. Trừ hai phương trình này: (m - 2)z = 0, nên k = 2.
    2. b) Với m = 2, phương trình cuối là 0 = 0: còn hai phương trình cho ba ẩn, z là ẩn tự do, hệ có vô số nghiệm.
    3. c) Với m = 5: 3z = 0 nên z = 0, rồi y = 2 - 3*0 = 2 và x = 1 - 2*2 + 0 = -3. Nghiệm (-3, 2, 0).
    4. d) Vế phải của (m - 2)z = 0 luôn bằng 0, nên không bao giờ ra 0 = c với c khác 0: hệ không vô nghiệm với m nào. Mệnh đề sai.
- `dstt_g5_tham_so` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho hệ x + 3y = -4 và -x + my = 2, với m là tham số. Tìm giá trị m để hệ KHÔNG có nghiệm duy nhất.
  - **Đáp án:** -3
    1. Khử x ở hàng 2: R2 <- 1 . R2 - (-1) . R1. Hệ số của y ở hàng 2 mới là 1 . m - (-1) . 3 = m + 3.
    2. Hệ có nghiệm duy nhất khi và chỉ khi hệ số đó khác 0, tức là y có trụ.
    3. Hệ số bằng 0 khi m = -3: khi đó hệ vô nghiệm hoặc vô số nghiệm.
  - **Câu hỏi:** Cho hệ -3x - 3y = 0 và -3x + my = -3, với m là tham số. Tìm giá trị m để hệ KHÔNG có nghiệm duy nhất.
  - **Đáp án:** -3
    1. Khử x ở hàng 2: R2 <- (-3) . R2 - (-3) . R1. Hệ số của y ở hàng 2 mới là (-3) . m - (-3) . (-3) = -3m - 9.
    2. Hệ có nghiệm duy nhất khi và chỉ khi hệ số đó khác 0, tức là y có trụ.
    3. Hệ số bằng 0 khi m = -3: khi đó hệ vô nghiệm hoặc vô số nghiệm.
  - **Câu hỏi:** Cho hệ -2x - 2y = 4 và 2x + my = 2, với m là tham số. Tìm giá trị m để hệ KHÔNG có nghiệm duy nhất.
  - **Đáp án:** 2
    1. Khử x ở hàng 2: R2 <- (-2) . R2 - 2 . R1. Hệ số của y ở hàng 2 mới là (-2) . m - 2 . (-2) = -2m + 4.
    2. Hệ có nghiệm duy nhất khi và chỉ khi hệ số đó khác 0, tức là y có trụ.
    3. Hệ số bằng 0 khi m = 2: khi đó hệ vô nghiệm hoặc vô số nghiệm.

### Hệ thuần nhất Ax = 0 (`dstt_t5_he_thuan_nhat`)

- `dstt_t5_htn_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi hệ thuần nhất Ax = 0 đều có ít nhất một nghiệm.
  - **Đáp án:** Đúng
    1. x = 0 (mọi ẩn bằng 0) luôn thỏa A . 0 = 0.
    2. Nghiệm đó gọi là nghiệm tầm thường.
    3. Vì vậy hệ thuần nhất không bao giờ vô nghiệm; câu hỏi chỉ là nó có nghiệm khác 0 hay không.
- `dstt_t5_htn_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một hệ thuần nhất có 3 phương trình và 5 ẩn. Điều nào chắc chắn đúng?
    - **(đúng)** Hệ có nghiệm khác nghiệm tầm thường
    - Hệ chỉ có nghiệm tầm thường
    - Hệ có thể vô nghiệm
    - Hệ có đúng hai nghiệm
  - **Đáp án:** Hệ có nghiệm khác nghiệm tầm thường
    1. Dạng bậc thang có nhiều nhất 3 trụ, vì chỉ có 3 hàng.
    2. 5 ẩn mà nhiều nhất 3 trụ thì có ít nhất 2 ẩn tự do.
    3. Cho ẩn tự do giá trị khác 0 được nghiệm khác 0. Hệ thuần nhất không bao giờ vô nghiệm.
- `dstt_g5_tam_thuong` · bậc 3 (Vận dụng) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A vuông cấp 3 như hình. Hệ thuần nhất Ax = 0 chỉ có nghiệm tầm thường x = 0.
  - A = (-2, 3, 1); (-2, 4, 0); (-2, 4, -2)  (từng hàng)
  - **Đáp án:** Đúng
    1. Khử Gauss ma trận A và đếm số trụ (số hàng khác không của dạng bậc thang).
    2. Dạng bậc thang có 3 hàng khác không.
    3. Đủ 3 trụ cho 3 ẩn, không có ẩn tự do: chỉ có nghiệm tầm thường.
  - **Câu hỏi:** Cho ma trận A vuông cấp 3 như hình. Hệ thuần nhất Ax = 0 chỉ có nghiệm tầm thường x = 0.
  - A = (-3, -1, 3); (3, -3, -3); (-3, 3, 3)  (từng hàng)
  - **Đáp án:** Sai
    1. Khử Gauss ma trận A và đếm số trụ (số hàng khác không của dạng bậc thang).
    2. Dạng bậc thang có 2 hàng khác không.
    3. Chỉ có 2 trụ cho 3 ẩn, còn một ẩn tự do: hệ có nghiệm khác 0.
  - **Câu hỏi:** Cho ma trận A vuông cấp 3 như hình. Hệ thuần nhất Ax = 0 chỉ có nghiệm tầm thường x = 0.
  - A = (-1, -2, 1); (-2, -3, 2); (2, 6, 0)  (từng hàng)
  - **Đáp án:** Đúng
    1. Khử Gauss ma trận A và đếm số trụ (số hàng khác không của dạng bậc thang).
    2. Dạng bậc thang có 3 hàng khác không.
    3. Đủ 3 trụ cho 3 ẩn, không có ẩn tự do: chỉ có nghiệm tầm thường.
- `dstt_t5_htn_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Hệ thuần nhất Ax = 0 (ẩn x, y, z) có vô số nghiệm. Tìm nghiệm có z = 1. Nhập x, y, z theo thứ tự.
  - A = (1, 2, -1); (2, 4, -2); (1, 3, 0)  (từng hàng)
  - **Đáp án:** 3, -1, 1
    1. R2 - 2R1 cho hàng 0; R3 - R1 cho (0, 1, 1). Đổi chỗ để hàng 0 xuống dưới cùng.
    2. z là ẩn tự do; hàng (0, 1, 1) cho y = -z; hàng 1 cho x = -2y + z = 3z.
    3. z = 1 cho nghiệm (3, -1, 1). Thử lại hàng 3: 3 - 3 + 0 = 0.
- `dstt_t5_htn_04` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước tìm nghiệm tổng quát của hệ thuần nhất x + y - z = 0, 2x + 3y + z = 0.
  - **Đáp án (thứ tự đúng):**
    1. R2 <- R2 - 2R1: hàng 2 thành (0, 1, 3 | 0).
    2. z không có trụ nên là ẩn tự do: đặt z = t.
    3. Từ hàng 2: y = -3t.
    4. Từ hàng 1: x = -y + z = 3t + t = 4t.
    5. Nghiệm tổng quát: (x, y, z) = t(4, -3, 1), với t là số thực bất kỳ.
  - **Lời giải:**
    1. Khử Gauss trước để thấy trụ nằm ở cột x và cột y.
    2. Ẩn không có trụ là ẩn tự do; thế ngược tính các ẩn có trụ theo nó.
    3. Thử lại với t = 1: 4 - 3 - 1 = 0 và 8 - 9 + 1 = 0.
- `dstt_g5_an_tu_do` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A cỡ 3 x 4 như hình. Hệ thuần nhất Ax = 0 có bốn ẩn. Khi giải bằng khử Gauss, có bao nhiêu ẩn tự do?
  - A = (6, 4, 6, -4); (4, -2, 4, -2); (-1, 4, -1, 0)  (từng hàng)
  - **Đáp án:** 2
    1. Khử Gauss ma trận A; mỗi hàng khác không của dạng bậc thang cho một trụ.
    2. Dạng bậc thang có 2 hàng khác không, tức là 2 ẩn có trụ.
    3. Số ẩn tự do là 4 - 2 = 2.
  - **Câu hỏi:** Cho ma trận A cỡ 3 x 4 như hình. Hệ thuần nhất Ax = 0 có bốn ẩn. Khi giải bằng khử Gauss, có bao nhiêu ẩn tự do?
  - A = (2, -6, -6, 0); (2, -6, -6, 0); (0, 0, 0, 0)  (từng hàng)
  - **Đáp án:** 3
    1. Khử Gauss ma trận A; mỗi hàng khác không của dạng bậc thang cho một trụ.
    2. Dạng bậc thang có 1 hàng khác không, tức là 1 ẩn có trụ.
    3. Số ẩn tự do là 4 - 1 = 3.
  - **Câu hỏi:** Cho ma trận A cỡ 3 x 4 như hình. Hệ thuần nhất Ax = 0 có bốn ẩn. Khi giải bằng khử Gauss, có bao nhiêu ẩn tự do?
  - A = (2, 6, -4, 8); (-3, -2, 2, -2); (4, 5, -4, 6)  (từng hàng)
  - **Đáp án:** 2
    1. Khử Gauss ma trận A; mỗi hàng khác không của dạng bậc thang cho một trụ.
    2. Dạng bậc thang có 2 hàng khác không, tức là 2 ẩn có trụ.
    3. Số ẩn tự do là 4 - 2 = 2.

## Tầng 6: Định thức, hạng và ma trận nghịch đảo

46 dạng câu (36 câu viết tay, 10 bộ sinh câu); 46 chưa duyệt.

### Định thức cấp 2 và cấp 3 (`dstt_t6_dinh_thuc_cap_2_3`)

- `dstt_t6_dt_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Định thức chỉ được định nghĩa cho ma trận vuông.
  - **Đáp án:** Đúng
    1. Định thức cấp n cộng các tích lấy đúng một phần tử ở mỗi hàng và mỗi cột.
    2. Điều đó cần số hàng bằng số cột.
    3. Ma trận cỡ 2 x 3 chẳng hạn không có định thức.
- `dstt_t6_dt_02` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A cấp 3 như hình, có hai số 0.
  - A = (1, 0, 2); (3, -1, 0); (0, 4, 1)  (từng hàng)
  - **Đáp án:** 23
    1. Theo quy tắc Sarrus, ba tích đường chéo xuống: 1 . (-1) . 1 = -1, 0 . 0 . 0 = 0, 2 . 3 . 4 = 24.
    2. Ba tích đường chéo lên: 2 . (-1) . 0 = 0, 1 . 0 . 4 = 0, 0 . 3 . 1 = 0.
    3. det A = (-1 + 0 + 24) - (0 + 0 + 0) = 23.
- `dstt_t6_dt_04` · bậc 3 (Vận dụng) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính định thức của A như hình bằng quy tắc Sarrus. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2, 3); (0, 1, 4); (5, 6, 0)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. Ba tích theo đường chéo xuống: 1 . 1 . 0 = 0, 2 . 4 . 5 = 40, 3 . 0 . 6 = 0.
    2. Ba tích theo đường chéo lên: 3 . 1 . 5 = 15, 1 . 4 . 6 = 24, 2 . 0 . 0 = 0.
    3. det A = (0 + 40 + 0) + (15 + 24 + 0) = 79.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: det A = (0 + 40 + 0) + (15 + 24 + 0) = 79.
  - **Vì sao sai, và bước đúng:**
    1. Theo Sarrus, các tích theo đường chéo lên phải được trừ đi, không cộng vào.
    2. Đúng ra: det A = (0 + 40 + 0) - (15 + 24 + 0) = 1.
- `dstt_t6_dt_05` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi ma trận cấp 2 bên trái được cho bởi hàng 1 rồi hàng 2. Ghép mỗi ma trận với định thức của nó.
  - **Đáp án (ghép đúng):**
    - (1, 2) và (3, 4) — -2
    - (2, 1) và (1, 2) — 3
    - (3, 6) và (1, 2) — 0
    - (0, 1) và (1, 0) — -1
    - (5, 2) và (2, 1) — 1
  - **Lời giải:**
    1. Định thức cấp 2 có hàng (a, b) và (c, d) là ad - bc.
    2. 1 . 4 - 2 . 3 = -2; 2 . 2 - 1 . 1 = 3; 3 . 2 - 6 . 1 = 0.
    3. 0 . 0 - 1 . 1 = -1; 5 . 1 - 2 . 2 = 1.
- `dstt_g6_dinh_thuc_3` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A cấp 3 như hình.
  - A = (-1, -2, 1); (-2, 4, 4); (4, 3, 0)  (từng hàng)
  - **Đáp án:** -42
    1. Quy tắc Sarrus: cộng ba tích theo đường chéo xuống, trừ ba tích theo đường chéo lên.
    2. Ba tích đường chéo xuống: 0, -32, -6; ba tích đường chéo lên: 16, -12, 0.
    3. det A = (0 + (-32) + (-6)) - (16 + (-12) + 0) = -42.
  - **Câu hỏi:** Tính định thức của ma trận A cấp 3 như hình.
  - A = (-3, -2, -2); (2, -1, 1); (1, 0, -3)  (từng hàng)
  - **Đáp án:** -25
    1. Quy tắc Sarrus: cộng ba tích theo đường chéo xuống, trừ ba tích theo đường chéo lên.
    2. Ba tích đường chéo xuống: -9, -2, 0; ba tích đường chéo lên: 2, 0, 12.
    3. det A = ((-9) + (-2) + 0) - (2 + 0 + 12) = -25.
  - **Câu hỏi:** Tính định thức của ma trận A cấp 3 như hình.
  - A = (0, -1, 2); (4, -2, -3); (4, 1, 0)  (từng hàng)
  - **Đáp án:** 36
    1. Quy tắc Sarrus: cộng ba tích theo đường chéo xuống, trừ ba tích theo đường chéo lên.
    2. Ba tích đường chéo xuống: 0, 12, 8; ba tích đường chéo lên: -16, 0, 0.
    3. det A = (0 + 12 + 8) - ((-16) + 0 + 0) = 36.
- `dstt_t6_dt_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A cấp 2 có hàng 1 là (x, 2) và hàng 2 là (3, x + 1), với x là một số thực. Tìm mọi x để det A = 0. Nhập các giá trị, cách nhau bằng dấu phẩy.
  - **Đáp án:** -3, 2  (thứ tự nào cũng được)
    1. det A = x(x + 1) - 2 . 3 = x^2 + x - 6.
    2. Phân tích: x^2 + x - 6 = (x - 2)(x + 3).
    3. det A = 0 khi x = 2 hoặc x = -3.
- `dstt_g6_tim_x_det` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình, trong đó x là một số thực. Tìm x để det A = -12.
  - A = (-1, x, 1); (-2, 4, 4); (4, 3, 0)  (từng hàng)
  - **Đáp án:** -1/8
    1. Khai triển theo hàng 1: x chỉ xuất hiện ở vị trí (1, 2), nên det A = x . C_12 + (phần còn lại).
    2. C_12 = 16; các số hạng còn lại cộng được -10 (bằng det A khi x = 0).
    3. Giải 16x + (-10) = -12: x = -1/8.
  - **Câu hỏi:** Cho ma trận A như hình, trong đó x là một số thực. Tìm x để det A = -7.
  - A = (-3, -2, -2); (2, -1, 1); (1, 0, x)  (từng hàng)
  - **Đáp án:** -3/7
    1. Khai triển theo hàng 3: x chỉ xuất hiện ở vị trí (3, 3), nên det A = x . C_33 + (phần còn lại).
    2. C_33 = 7; các số hạng còn lại cộng được -4 (bằng det A khi x = 0).
    3. Giải 7x + (-4) = -7: x = -3/7.
  - **Câu hỏi:** Cho ma trận A như hình, trong đó x là một số thực. Tìm x để det A = 3.
  - A = (0, -1, x); (4, -2, -3); (4, 1, 0)  (từng hàng)
  - **Đáp án:** -3/4
    1. Khai triển theo hàng 1: x chỉ xuất hiện ở vị trí (1, 3), nên det A = x . C_13 + (phần còn lại).
    2. C_13 = 12; các số hạng còn lại cộng được 12 (bằng det A khi x = 0).
    3. Giải 12x + 12 = 3: x = -3/4.

### Khai triển theo hàng hoặc cột (`dstt_t6_khai_trien`)

- `dstt_t6_kt_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Muốn tính định thức của ma trận A như hình bằng khai triển theo một hàng hoặc một cột, chọn hàng hoặc cột nào thì ít phép tính nhất?
  - A = (3, 1, 4); (0, 2, 0); (5, 1, 2)  (từng hàng)
    - **(đúng)** Hàng 2
    - Hàng 1
    - Cột 1
    - Cột 3
  - **Đáp án:** Hàng 2
    1. Mỗi số 0 trên hàng hoặc cột được chọn xóa đi một số hạng của khai triển.
    2. Hàng 2 là (0, 2, 0), có hai số 0: chỉ còn một số hạng. Cột 1 và cột 3 chỉ có một số 0, hàng 1 không có số 0 nào.
    3. det A = 2 . (-1)^(2 + 2) . (3 . 2 - 4 . 5) = 2 . (-14) = -28.
- `dstt_t6_kt_02` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A như hình bằng cách khai triển theo hàng có nhiều số 0 nhất.
  - A = (2, 0, 1); (1, 3, -1); (0, 0, 4)  (từng hàng)
  - **Đáp án:** 24
    1. Hàng 3 là (0, 0, 4): chỉ còn số hạng của a_33 = 4.
    2. Dấu ở vị trí (3, 3) là (-1)^6 = +1; định thức con M_33 có hàng (2, 0) và (1, 3), bằng 6.
    3. det A = 4 . 6 = 24.
- `dstt_t6_kt_03` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với ma trận vuông cấp 3, phần bù đại số C_23 bằng số đối của định thức con M_23.
  - **Đáp án:** Đúng
    1. Phần bù đại số là C_ij = (-1)^(i + j) M_ij.
    2. Với i = 2, j = 3: (-1)^5 = -1.
    3. Vậy C_23 = -M_23.
- `dstt_g6_phan_bu` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần bù đại số C_11.
  - A = (-2, 5, -3); (0, -3, 3); (3, 3, 2)  (từng hàng)
  - **Đáp án:** -15
    1. Bỏ hàng 1 và cột 1 của A: định thức con M_11 có hàng (-3, 3), (3, 2), bằng -15.
    2. Dấu ở vị trí (1, 1) là (-1)^(1 + 1) = 1.
    3. C_11 = 1 . (-15) = -15.
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần bù đại số C_31.
  - A = (-4, -3, -3); (1, -2, 0); (0, 5, -1)  (từng hàng)
  - **Đáp án:** -6
    1. Bỏ hàng 3 và cột 1 của A: định thức con M_31 có hàng (-3, -3), (-2, 0), bằng -6.
    2. Dấu ở vị trí (3, 1) là (-1)^(3 + 1) = 1.
    3. C_31 = 1 . (-6) = -6.
  - **Câu hỏi:** Cho ma trận A như hình. Tính phần bù đại số C_31.
  - A = (-1, 5, 4); (-2, 1, 5); (3, 5, -3)  (từng hàng)
  - **Đáp án:** 21
    1. Bỏ hàng 3 và cột 1 của A: định thức con M_31 có hàng (5, 4), (1, 5), bằng 21.
    2. Dấu ở vị trí (3, 1) là (-1)^(3 + 1) = 1.
    3. C_31 = 1 . 21 = 21.
- `dstt_t6_kt_04` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A cấp 4 như hình. Chọn hàng hoặc cột khai triển cho khéo.
  - A = (1, 0, 2, 0); (0, 3, 0, 0); (2, 1, 1, 4); (0, 0, 0, -1)  (từng hàng)
  - **Đáp án:** 9
    1. Hàng 2 chỉ có a_22 = 3 khác 0, dấu (-1)^4 = +1: det A = 3 . M_22, với M_22 là định thức cấp 3 có hàng (1, 2, 0), (2, 1, 4), (0, 0, -1).
    2. Khai triển M_22 theo hàng cuối (0, 0, -1): M_22 = -1 . (1 . 1 - 2 . 2) = 3.
    3. det A = 3 . 3 = 9.
- `dstt_t6_kt_05` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính định thức của A như hình bằng khai triển theo hàng 1. Bước đầu tiên bị sai là bước nào?
  - A = (0, 2, 0); (1, 3, 5); (4, 1, 2)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. Hàng 1 có hai số 0, nên khai triển theo hàng 1: chỉ còn số hạng của a_12 = 2.
    2. Định thức con M_12 (bỏ hàng 1, cột 2) có hàng (1, 5) và (4, 2), bằng 2 - 20 = -18.
    3. Phần bù đại số C_12 = M_12 = -18.   **<- bước sai đầu tiên**
    4. det A = 2 . (-18) = -36.
  - **Đáp án:** Bước 3: Phần bù đại số C_12 = M_12 = -18.
  - **Vì sao sai, và bước đúng:**
    1. Phần bù đại số mang dấu theo vị trí: C_12 = (-1)^(1 + 2) M_12 = -M_12.
    2. Đúng ra: C_12 = 18 và det A = 2 . 18 = 36.
- `dstt_t6_kt_06` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Sắp xếp các bước tính det A bằng khai triển.
  - A = (2, 0, 1); (3, 0, -1); (1, 4, 5)  (từng hàng)
  - **Đáp án (thứ tự đúng):**
    1. Cột 2 có hai số 0, nên khai triển theo cột 2.
    2. Chỉ còn số hạng của a_32 = 4.
    3. Định thức con M_32: bỏ hàng 3 và cột 2, được ma trận có hàng (2, 1) và (3, -1), định thức -2 - 3 = -5.
    4. Dấu ở vị trí (3, 2) là (-1)^(3 + 2) = -1, nên C_32 = 5.
    5. det A = 4 . 5 = 20.
  - **Lời giải:**
    1. Chọn cột có nhiều số 0 nhất, rồi chỉ tính các số hạng của phần tử khác 0.
    2. Mỗi số hạng là phần tử nhân phần bù đại số của nó, với dấu (-1)^(i + j).
    3. det A = a_32 . C_32 = 4 . 5 = 20.
- `dstt_g6_khai_trien_4` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A cấp 4 như hình.
  - A = (0, 0, 0, -1); (-2, 1, 1, 1); (3, 1, -1, -2); (1, -2, 1, 1)  (từng hàng)
  - **Đáp án:** -9
    1. Hàng 1 chỉ có một phần tử khác 0 là a_14 = -1: khai triển theo hàng đó.
    2. Định thức con M_14 (bỏ hàng 1, cột 4) có hàng (-2, 1, 1), (3, 1, -1), (1, -2, 1); theo Sarrus nó bằng -9.
    3. Dấu (-1)^(1 + 4) = -1, nên det A = -1 . (-1) . (-9) = -9.
  - **Câu hỏi:** Tính định thức của ma trận A cấp 4 như hình.
  - A = (-2, -2, -2, 0); (-1, 3, 3, 0); (0, 2, -1, 2); (0, 0, 0, 3)  (từng hàng)
  - **Đáp án:** 72
    1. Hàng 4 chỉ có một phần tử khác 0 là a_44 = 3: khai triển theo hàng đó.
    2. Định thức con M_44 (bỏ hàng 4, cột 4) có hàng (-2, -2, -2), (-1, 3, 3), (0, 2, -1); theo Sarrus nó bằng 24.
    3. Dấu (-1)^(4 + 4) = 1, nên det A = 3 . 1 . 24 = 72.
  - **Câu hỏi:** Tính định thức của ma trận A cấp 4 như hình.
  - A = (-1, 2, 2, -1); (0, 0, 0, 2); (2, -2, 2, -2); (1, 0, 2, -1)  (từng hàng)
  - **Đáp án:** 8
    1. Hàng 2 chỉ có một phần tử khác 0 là a_24 = 2: khai triển theo hàng đó.
    2. Định thức con M_24 (bỏ hàng 2, cột 4) có hàng (-1, 2, 2), (2, -2, 2), (1, 0, 2); theo Sarrus nó bằng 4.
    3. Dấu (-1)^(2 + 4) = 1, nên det A = 2 . 1 . 4 = 8.

### Tính chất của định thức (`dstt_t6_tinh_chat_dinh_thuc`)

- `dstt_t6_tcd_01` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đổi chỗ hai hàng của một ma trận vuông thì định thức thay đổi thế nào?
    - **(đúng)** Đổi dấu
    - Không đổi
    - Nhân đôi
    - Trở thành 0
  - **Đáp án:** Đổi dấu
    1. Mỗi lần đổi chỗ hai hàng, định thức đổi dấu.
    2. Ví dụ ma trận có hàng (1, 0) và (0, 1) có định thức 1; đổi chỗ hai hàng được hàng (0, 1) và (1, 0), định thức -1.
    3. Khi khử Gauss, mỗi lần đổi chỗ hàng phải nhớ đổi dấu một lần.
- `dstt_t6_tcd_05` · bậc 3 (Vận dụng) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 3 có det A = 5. Ghép mỗi cách biến đổi A với định thức của ma trận thu được.
  - **Đáp án (ghép đúng):**
    - đổi chỗ hàng 1 và hàng 2 — -5
    - nhân hàng 2 với 3 — 15
    - cộng 4 lần hàng 1 vào hàng 3 — 5
    - nhân cả ma trận với 2 — 40
  - **Lời giải:**
    1. Đổi chỗ hai hàng: định thức đổi dấu, được -5.
    2. Nhân một hàng với 3: định thức nhân 3, được 15. Cộng bội của một hàng vào hàng khác: định thức không đổi, vẫn 5.
    3. Nhân cả ma trận cấp 3 với 2 là nhân ba hàng với 2: định thức nhân 2^3 = 8, được 40.
- `dstt_g6_tinh_chat` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 2 có det A = -3. Tính det(A^2).
  - **Đáp án:** 9
    1. Định thức nhân tính: det(A^2) = det A . det A.
    2. det(A^2) = (-3)^2 = 9.
  - **Câu hỏi:** A là ma trận vuông cấp 2 có det A = -3. Tính det(2A).
  - **Đáp án:** -12
    1. 2A nhân cả 2 hàng của A với 2, mỗi hàng nhân định thức với 2.
    2. det(2A) = 2^2 . (-3) = -12.
  - **Câu hỏi:** A là ma trận vuông cấp 2 có det A = 5. Tính det(A^T).
  - **Đáp án:** 5
    1. Chuyển vị không đổi định thức.
    2. det(A^T) = det A = 5.
- `dstt_t6_tcd_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai ma trận vuông cùng cấp A và B, ta có det(A + B) = det A + det B.
  - **Đáp án:** Sai
    1. Định thức không cộng tính. Lấy A = B = I cấp 2.
    2. det(A + B) = det(2I) = 2 . 2 = 4, còn det A + det B = 1 + 1 = 2.
    3. Định thức nhân tính, det(AB) = det A . det B, chứ không cộng tính.
- `dstt_t6_tcd_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 3 có det A = 2. Lời giải sau tính det(3A). Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. 3A nhận được từ A bằng cách nhân mọi phần tử với 3, tức là nhân cả ba hàng với 3.
    2. Nhân ma trận với 3 thì định thức nhân với 3, nên det(3A) = 3 . det A.   **<- bước sai đầu tiên**
    3. Vậy det(3A) = 3 . 2 = 6.
  - **Đáp án:** Bước 2: Nhân ma trận với 3 thì định thức nhân với 3, nên det(3A) = 3 . det A.
  - **Vì sao sai, và bước đúng:**
    1. Nhân một hàng với 3 thì định thức nhân với 3; 3A nhân cả ba hàng, nên định thức nhân với 3 ba lần.
    2. Đúng ra: det(3A) = 3^3 . det A = 27 . 2 = 54. Nói chung det(kA) = k^n det A với A vuông cấp n.
- `dstt_t6_tcd_04` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B là hai ma trận vuông cấp 3 có det A = 2 và det B = -3. Tính det(2 A^T B^2).
  - **Đáp án:** 144
    1. Định thức nhân tính: det(2 A^T B^2) = det(2I) . det(A^T) . det(B)^2, với det(2I) = 2^3 = 8.
    2. det(A^T) = det A = 2 và det(B)^2 = 9.
    3. Kết quả: 8 . 2 . 9 = 144.
- `dstt_t6_tcd_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tính định thức của ma trận A như hình bằng khử Gauss, nhớ theo dõi các phép làm thay đổi định thức.
  - A = (0, 1, 2); (1, 3, 1); (2, 5, 4)  (từng hàng)
  - **Đáp án:** -4
    1. Trụ ở hàng 1 bằng 0: đổi chỗ hàng 1 và hàng 2 (định thức đổi dấu). Được hàng (1, 3, 1), (0, 1, 2), (2, 5, 4).
    2. R3 <- R3 - 2R1 cho (0, -1, 2); R3 <- R3 + R2 cho (0, 0, 4). Hai phép này không đổi định thức.
    3. Ma trận tam giác có định thức 1 . 1 . 4 = 4; đổi dấu vì lần đổi chỗ hàng: det A = -4.
- `dstt_t6_tcd_07` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai ma trận vuông cùng cấp A và B, ta có det(AB) = det(BA), kể cả khi AB khác BA.
  - **Đáp án:** Đúng
    1. det(AB) = det A . det B và det(BA) = det B . det A.
    2. Hai tích số đó bằng nhau vì phép nhân số giao hoán.
    3. Vậy AB và BA có thể khác nhau nhưng luôn có cùng định thức.

### Hạng của ma trận (`dstt_t6_hang`)

- `dstt_t6_hg_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình đã ở dạng bậc thang. Hạng của A bằng bao nhiêu?
  - A = (1, 2, 0, 1); (0, 0, 3, 1); (0, 0, 0, 0)  (từng hàng)
  - **Đáp án:** 2
    1. Hạng là số hàng khác không của một dạng bậc thang.
    2. Hàng 1 và hàng 2 khác không, hàng 3 toàn số 0.
    3. rank A = 2.
- `dstt_t6_hg_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có ma trận cỡ 3 x 5 có hạng bằng 4.
  - **Đáp án:** Sai
    1. Dạng bậc thang của ma trận cỡ 3 x 5 có nhiều nhất 3 hàng khác không.
    2. Nên hạng của nó nhiều nhất là 3.
    3. Nói chung hạng của ma trận cỡ m x n không vượt quá số nhỏ hơn trong hai số m và n.
- `dstt_g6_hang` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hạng của ma trận A cỡ 4 x 3 như hình.
  - A = (2, -6, 0); (4, -2, -2); (-3, -1, 2); (-3, -1, 2)  (từng hàng)
  - **Đáp án:** 2
    1. Khử Gauss đưa A về dạng bậc thang; hạng là số hàng khác không của dạng đó.
    2. Dạng bậc thang của A có 2 hàng khác không; các hàng còn lại bị khử thành 0 vì chúng là tổ hợp của các hàng khác.
    3. rank A = 2.
  - **Câu hỏi:** Tìm hạng của ma trận A cỡ 4 x 3 như hình.
  - A = (0, -2, -1); (0, 2, 1); (0, 2, 1); (0, 4, 2)  (từng hàng)
  - **Đáp án:** 1
    1. Khử Gauss đưa A về dạng bậc thang; hạng là số hàng khác không của dạng đó.
    2. Dạng bậc thang của A có 1 hàng khác không; các hàng còn lại bị khử thành 0 vì chúng là tổ hợp của các hàng khác.
    3. rank A = 1.
  - **Câu hỏi:** Tìm hạng của ma trận A cỡ 4 x 3 như hình.
  - A = (4, 0, 0); (-2, 2, -1); (4, -2, 1); (4, -8, 4)  (từng hàng)
  - **Đáp án:** 2
    1. Khử Gauss đưa A về dạng bậc thang; hạng là số hàng khác không của dạng đó.
    2. Dạng bậc thang của A có 2 hàng khác không; các hàng còn lại bị khử thành 0 vì chúng là tổ hợp của các hàng khác.
    3. rank A = 2.
- `dstt_t6_hg_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A cấp 3 có các hàng (1, 2, 3), (2, 4, m) và (1, 1, 1), với m là tham số. Tìm m để rank A = 2.
  - **Đáp án:** 6
    1. R2 - 2R1 cho (0, 0, m - 6); R3 - R1 cho (0, -1, -2).
    2. Đổi chỗ hai hàng đó: dạng bậc thang có hàng (1, 2, 3), (0, -1, -2), (0, 0, m - 6).
    3. rank A = 2 khi và chỉ khi hàng cuối toàn số 0, tức là m = 6; với m khác 6 thì rank A = 3.
- `dstt_t6_hg_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm hạng của ma trận A như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2, 1); (2, 4, 2); (1, 0, 3)  (từng hàng)
  - **Lời giải đưa ra (có một bước sai):**
    1. A có ba hàng và không có hàng nào toàn số 0.
    2. Hạng là số hàng khác không, nên rank A = 3.   **<- bước sai đầu tiên**
    3. Vì rank A bằng cấp của A nên det A khác 0.
  - **Đáp án:** Bước 2: Hạng là số hàng khác không, nên rank A = 3.
  - **Vì sao sai, và bước đúng:**
    1. Hạng là số hàng khác không của dạng bậc thang, nên phải khử Gauss trước rồi mới đếm.
    2. Đúng ra: R2 - 2R1 là hàng 0, R3 - R1 = (0, -2, 2). Dạng bậc thang có hai hàng khác không, nên rank A = 2 (và det A = 0).
- `dstt_t6_hg_05` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A là ma trận vuông cấp 4 có rank A = 3. Điều nào chắc chắn đúng?
    - **(đúng)** det A = 0
    - A khả nghịch
    - Hệ Ax = 0 chỉ có nghiệm tầm thường
    - A có đúng 3 hàng khác không
  - **Đáp án:** det A = 0
    1. rank A = 3 < 4 nên dạng bậc thang của A có một hàng 0, và định thức của nó bằng 0; biến đổi hàng chỉ nhân định thức với số khác 0, nên det A = 0.
    2. Vì vậy A không khả nghịch và Ax = 0 có nghiệm khác 0 (một ẩn tự do).
    3. A có thể có cả 4 hàng khác không, ví dụ khi hàng 4 bằng tổng hàng 1 và hàng 2.

### Ma trận nghịch đảo (`dstt_t6_nghich_dao`)

- `dstt_t6_nd_01` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một ma trận vuông A khả nghịch khi và chỉ khi det A khác 0.
  - **Đáp án:** Đúng
    1. Nếu AB = I thì det A . det B = det I = 1, nên det A khác 0.
    2. Ngược lại, khi det A khác 0, khử Gauss-Jordan đưa A về I và cho ra A^(-1).
    3. Đây là cách nhanh nhất để biết một ma trận có khả nghịch hay không.
- `dstt_t6_nd_02` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận vuông cấp 2 nào sau đây, cho bởi hàng 1 rồi hàng 2, KHÔNG khả nghịch?
    - **(đúng)** (2, 4) và (1, 2)
    - (2, 4) và (1, 3)
    - (1, 0) và (0, -1)
    - (0, 1) và (1, 0)
  - **Đáp án:** (2, 4) và (1, 2)
    1. Một ma trận vuông khả nghịch khi và chỉ khi định thức khác 0.
    2. (2, 4) và (1, 2): 2 . 2 - 4 . 1 = 0, nên không khả nghịch (hàng 1 gấp đôi hàng 2).
    3. Ba ma trận còn lại có định thức 2, -1 và -1.
- `dstt_t6_nd_04` · bậc 3 (Vận dụng) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Sắp xếp các bước tìm A^(-1) bằng khử Gauss-Jordan.
  - A = (1, 2); (3, 7)  (từng hàng)
  - **Đáp án (thứ tự đúng):**
    1. Lập ma trận (A | I): hàng (1, 2 | 1, 0) và (3, 7 | 0, 1).
    2. R2 <- R2 - 3R1: hàng 2 thành (0, 1 | -3, 1).
    3. R1 <- R1 - 2R2: hàng 1 thành (1, 0 | 7, -2).
    4. Bên trái đã là I, nên A^(-1) có hàng (7, -2) và (-3, 1).
  - **Lời giải:**
    1. Biến đổi hàng trên cả (A | I) cho đến khi bên trái thành I; khi đó bên phải là A^(-1).
    2. Khử bên dưới trụ trước, rồi khử bên trên trụ.
    3. Thử lại: A . A^(-1) có hàng (7 - 6, -2 + 2) = (1, 0) và (21 - 21, -6 + 7) = (0, 1).
- `dstt_g6_nghich_dao_2` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Tìm ma trận nghịch đảo của A như hình. Nhập bốn phần tử của A^(-1) theo từng hàng, cách nhau bằng dấu phẩy (phân số viết a/b).
  - A = (2, -1); (-3, 3)  (từng hàng)
  - **Đáp án:** 1, 1/3, 1, 2/3
    1. det A = 2 . 3 - (-1) . (-3) = 3, khác 0, nên A khả nghịch.
    2. Với ma trận cấp 2: đổi chỗ hai phần tử trên đường chéo chính, đổi dấu hai phần tử còn lại, rồi chia cho det A = 3.
    3. A^(-1) có hàng (1, 1/3) và (1, 2/3).
  - **Câu hỏi:** Tìm ma trận nghịch đảo của A như hình. Nhập bốn phần tử của A^(-1) theo từng hàng, cách nhau bằng dấu phẩy (phân số viết a/b).
  - A = (3, 1); (2, 2)  (từng hàng)
  - **Đáp án:** 1/2, -1/4, -1/2, 3/4
    1. det A = 3 . 2 - 1 . 2 = 4, khác 0, nên A khả nghịch.
    2. Với ma trận cấp 2: đổi chỗ hai phần tử trên đường chéo chính, đổi dấu hai phần tử còn lại, rồi chia cho det A = 4.
    3. A^(-1) có hàng (1/2, -1/4) và (-1/2, 3/4).
  - **Câu hỏi:** Tìm ma trận nghịch đảo của A như hình. Nhập bốn phần tử của A^(-1) theo từng hàng, cách nhau bằng dấu phẩy (phân số viết a/b).
  - A = (0, 4); (-1, -1)  (từng hàng)
  - **Đáp án:** -1/4, -1, 1/4, 0
    1. det A = 0 . (-1) - 4 . (-1) = 4, khác 0, nên A khả nghịch.
    2. Với ma trận cấp 2: đổi chỗ hai phần tử trên đường chéo chính, đổi dấu hai phần tử còn lại, rồi chia cho det A = 4.
    3. A^(-1) có hàng (-1/4, -1) và (1/4, 0).
- `dstt_t6_nd_03` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** A và B là hai ma trận vuông cùng cấp, đều khả nghịch. Lời giải sau tìm (AB)^(-1). Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. det(AB) = det A . det B khác 0, nên AB khả nghịch.
    2. Nghịch đảo của một tích là tích các nghịch đảo theo cùng thứ tự: (AB)^(-1) = A^(-1) B^(-1).   **<- bước sai đầu tiên**
    3. Vậy để tìm (AB)^(-1), chỉ cần nhân A^(-1) với B^(-1).
  - **Đáp án:** Bước 2: Nghịch đảo của một tích là tích các nghịch đảo theo cùng thứ tự: (AB)^(-1) = A^(-1) B^(-1).
  - **Vì sao sai, và bước đúng:**
    1. Nghịch đảo của một tích thì đảo thứ tự, giống như chuyển vị: (AB)^(-1) = B^(-1) A^(-1).
    2. Kiểm tra: (AB)(B^(-1) A^(-1)) = A (B B^(-1)) A^(-1) = A A^(-1) = I. Còn (AB)(A^(-1) B^(-1)) nói chung không bằng I vì không đổi chỗ được.
- `dstt_t6_nd_05` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu ma trận vuông A khả nghịch thì A^T cũng khả nghịch và (A^T)^(-1) = (A^(-1))^T.
  - **Đáp án:** Đúng
    1. Chuyển vị đẳng thức A A^(-1) = I, dùng quy tắc chuyển vị của tích: (A^(-1))^T A^T = I^T = I.
    2. Tương tự, chuyển vị A^(-1) A = I được A^T (A^(-1))^T = I.
    3. Vậy (A^(-1))^T là nghịch đảo của A^T.
- `dstt_t6_nd_06` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận tam giác dưới A như hình. Tìm A^(-1) bằng khử Gauss-Jordan và nhập hàng 3 của A^(-1), cách nhau bằng dấu phẩy.
  - A = (1, 0, 0); (2, 1, 0); (0, 3, 1)  (từng hàng)
  - **Đáp án:** 6, -3, 1
    1. Lập (A | I). R2 <- R2 - 2R1: hàng 2 thành (0, 1, 0 | -2, 1, 0).
    2. R3 <- R3 - 3R2 (dùng hàng 2 mới): hàng 3 thành (0, 0, 1 | 6, -3, 1).
    3. Bên trái đã là I, nên hàng 3 của A^(-1) là (6, -3, 1). Thử lại: hàng 3 của A là (0, 3, 1), nhân các cột của A^(-1) cho (0, 0, 1).
- `dstt_t6_nd_07` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tông môn giao cho con ma trận A như hình và yêu cầu xét nghịch đảo của nó.
  - A = (1, 1, 0); (0, 1, 1); (1, 0, 2)  (từng hàng)
  - **Phần a** (Điền số): a) Tính det A.
    - **Đáp án a:** 3
  - **Phần b** (Đúng/Sai): b) A khả nghịch.
    - **Đáp án b:** Đúng
  - **Phần c** (Điền số): c) Tìm phần tử ở hàng 1, cột 1 của A^(-1).
    - **Đáp án c:** 2/3
  - **Phần d** (Điền số): d) Tính det(A^(-1)).
    - **Đáp án d:** 1/3
  - **Lời giải:**
    1. a) Khai triển theo hàng 1: det A = 1 . (1 . 2 - 1 . 0) - 1 . (0 . 2 - 1 . 1) + 0 = 2 + 1 = 3.
    2. b) det A = 3 khác 0 nên A khả nghịch.
    3. c) Phần tử hàng 1, cột 1 của A^(-1) là C_11 / det A, với C_11 = det của (1, 1) và (0, 2) = 2; được 2/3.
    4. d) det(A^(-1)) = 1 / det A = 1/3.
- `dstt_g6_kha_nghich` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A vuông cấp 3 như hình là ma trận khả nghịch.
  - A = (-2, 3, 1); (-2, 4, 0); (-2, 4, -2)  (từng hàng)
  - **Đáp án:** Đúng
    1. A khả nghịch khi và chỉ khi det A khác 0.
    2. Theo Sarrus (hoặc khử Gauss), det A = 4.
    3. det A khác 0 nên A khả nghịch: mệnh đề đúng.
  - **Câu hỏi:** Ma trận A vuông cấp 3 như hình là ma trận khả nghịch.
  - A = (-3, 3, -3); (-1, -3, 3); (3, -3, 3)  (từng hàng)
  - **Đáp án:** Sai
    1. A khả nghịch khi và chỉ khi det A khác 0.
    2. Theo Sarrus (hoặc khử Gauss), det A = 0.
    3. det A = 0 (một cột là tổ hợp của hai cột kia), nên A không khả nghịch: mệnh đề sai.
  - **Câu hỏi:** Ma trận A vuông cấp 3 như hình là ma trận khả nghịch.
  - A = (-1, -2, 1); (-2, -3, 2); (2, 6, 0)  (từng hàng)
  - **Đáp án:** Đúng
    1. A khả nghịch khi và chỉ khi det A khác 0.
    2. Theo Sarrus (hoặc khử Gauss), det A = -2.
    3. det A khác 0 nên A khả nghịch: mệnh đề đúng.

### Giải hệ bằng nghịch đảo và quy tắc Cramer (`dstt_t6_giai_he_nghich_dao`)

- `dstt_t6_gn_01` · bậc 3 (Vận dụng) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ Ax = b có A khả nghịch, với A^(-1) là ma trận B như hình và b = (3, 4). Tìm nghiệm x. Nhập hai tọa độ, cách nhau bằng dấu phẩy.
  - B = (2, -1); (-1, 1)  (từng hàng)
  - **Đáp án:** 2, 1
    1. Nhân hai vế của Ax = b với A^(-1) bên trái: x = A^(-1) b.
    2. Tọa độ 1: 2 . 3 + (-1) . 4 = 2. Tọa độ 2: (-1) . 3 + 1 . 4 = 1.
    3. x = (2, 1).
- `dstt_t6_gn_02` · bậc 3 (Vận dụng) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quy tắc Cramer dùng được cho mọi hệ n phương trình, n ẩn.
  - **Đáp án:** Sai
    1. Quy tắc Cramer chia cho det A, nên chỉ dùng được khi det A khác 0.
    2. Ví dụ hệ x + y = 1, 2x + 2y = 2 có det A = 0 và có vô số nghiệm: Cramer không áp dụng được.
    3. Khi det A = 0 phải khử Gauss để biện luận.
- `dstt_t6_gn_05` · bậc 3 (Vận dụng) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hệ Ax = b có A vuông và khả nghịch. Nghiệm của hệ là gì?
    - **(đúng)** x = A^(-1) b
    - x = b A^(-1)
    - x = A b
    - x = b chia cho A theo từng phần tử
  - **Đáp án:** x = A^(-1) b
    1. Nhân hai vế với A^(-1) ở bên trái: A^(-1) A x = A^(-1) b, tức là x = A^(-1) b.
    2. b A^(-1) là (n x 1)(n x n), không nhân được; A b không phải là nghiệm.
    3. Không có phép chia ma trận theo từng phần tử để giải hệ.
- `dstt_g6_cramer` · bậc 3 (Vận dụng) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dùng quy tắc Cramer để tìm y của hệ -2x + 5y = -5 và -3x = 1.
  - **Đáp án:** -17/15
    1. det A = (-2) . 0 - 5 . (-3) = 15, khác 0, nên dùng được quy tắc Cramer.
    2. Thay cột 2 của A bằng vế phải: ma trận có hàng (-2, -5), (-3, 1), định thức -17.
    3. y = -17/15 = -17/15.
  - **Câu hỏi:** Dùng quy tắc Cramer để tìm y của hệ -4x - 3y = -4 và -3x + y = 5.
  - **Đáp án:** 32/13
    1. det A = (-4) . 1 - (-3) . (-3) = -13, khác 0, nên dùng được quy tắc Cramer.
    2. Thay cột 2 của A bằng vế phải: ma trận có hàng (-4, -4), (-3, 5), định thức -32.
    3. y = -32/(-13) = 32/13.
  - **Câu hỏi:** Dùng quy tắc Cramer để tìm y của hệ -x + 5y = -1 và 4x - 2y = 3.
  - **Đáp án:** -1/18
    1. det A = (-1) . (-2) - 5 . 4 = -18, khác 0, nên dùng được quy tắc Cramer.
    2. Thay cột 2 của A bằng vế phải: ma trận có hàng (-1, -1), (4, 3), định thức 1.
    3. y = 1/(-18) = -1/18.
- `dstt_t6_gn_03` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hệ x + y + z = 6, 2y + z = 7, x + 3z = 10 (det A = 5). Theo quy tắc Cramer, lập A_2 bằng cách thay cột 2 của A bằng vế phải. Tính det A_2 rồi y. Nhập det A_2 và y, cách nhau bằng dấu phẩy.
  - **Đáp án:** 10, 2
    1. A có hàng (1, 1, 1), (0, 2, 1), (1, 0, 3); thay cột 2 bằng (6, 7, 10): A_2 có hàng (1, 6, 1), (0, 7, 1), (1, 10, 3).
    2. Khai triển theo cột 1: det A_2 = 1 . (21 - 10) + 1 . (6 - 7) = 11 - 1 = 10.
    3. y = det A_2 / det A = 10/5 = 2. (Nghiệm đầy đủ là x = 1, y = 2, z = 3.)
- `dstt_t6_gn_04` · bậc 4 (Nâng cao) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm x của hệ x + 2y = 5, 3x + 4y = 6 bằng quy tắc Cramer. Bước đầu tiên bị sai là bước nào?
  - **Lời giải đưa ra (có một bước sai):**
    1. det A = 1 . 4 - 2 . 3 = -2, khác 0, nên dùng được quy tắc Cramer.
    2. Để tìm x, thay hàng 1 của A bằng vế phải: được ma trận có hàng (5, 6) và (3, 4).   **<- bước sai đầu tiên**
    3. Định thức đó bằng 20 - 18 = 2, nên x = 2/(-2) = -1.
  - **Đáp án:** Bước 2: Để tìm x, thay hàng 1 của A bằng vế phải: được ma trận có hàng (5, 6) và (3, 4).
  - **Vì sao sai, và bước đúng:**
    1. Quy tắc Cramer thay CỘT của ẩn cần tìm bằng vế phải, không thay hàng.
    2. Đúng ra: thay cột 1 được hàng (5, 2) và (6, 4), định thức 20 - 12 = 8, nên x = 8/(-2) = -4. Khi đó y = 9/2; thử lại: -4 + 9 = 5 và -12 + 18 = 6.
- `dstt_t6_gn_06` · bậc 4 (Nâng cao) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét hệ x + 2y = 5, 3x + my = 7, với m là tham số.
  - **Phần a** (Điền số): a) Tìm m để định thức của ma trận hệ số bằng 0.
    - **Đáp án a:** 6
  - **Phần b** (Trắc nghiệm): b) Với giá trị m vừa tìm, hệ có bao nhiêu nghiệm?
    - **(đúng)** Vô nghiệm
    - Nghiệm duy nhất
    - Vô số nghiệm
    - **Đáp án b:** Vô nghiệm
  - **Phần c** (Điền số): c) Khi m = 4, giải hệ bằng quy tắc Cramer. Nhập x, y theo thứ tự, cách nhau bằng dấu phẩy.
    - **Đáp án c:** -3, 4
  - **Lời giải:**
    1. a) det A = 1 . m - 2 . 3 = m - 6, bằng 0 khi m = 6.
    2. b) m = 6: R2 - 3R1 cho (0, 0 | 7 - 15) = (0, 0 | -8), tức 0 = -8, nên hệ vô nghiệm.
    3. c) m = 4: det A = -2; det A_1 = 5 . 4 - 2 . 7 = 6 nên x = -3; det A_2 = 1 . 7 - 5 . 3 = -8 nên y = 4. Thử lại: -3 + 8 = 5 và -9 + 16 = 7.
- `dstt_g6_giai_he_nd` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình có det A = -1. Giải hệ Ax = b với b = (-1, -3, 3) bằng cách tìm A^(-1). Nhập ba tọa độ của x, cách nhau bằng dấu phẩy.
  - A = (1, 1, 3); (-2, -1, -5); (1, 2, 3)  (từng hàng)
  - **Đáp án:** 22, 4, -9
    1. A khả nghịch vì det A khác 0, nên x = A^(-1) b.
    2. Khử Gauss-Jordan trên (A | I) (hoặc lấy phần phụ hợp chia cho det A): A^(-1) có hàng (-7, -3, 2), (-1, 0, 1), (3, 1, -1).
    3. Nhân A^(-1) với b: x = (22, 4, -9). Thử lại: A x = (-1, -3, 3) = b.
  - **Câu hỏi:** Ma trận A như hình có det A = 1. Giải hệ Ax = b với b = (-4, -2, 2) bằng cách tìm A^(-1). Nhập ba tọa độ của x, cách nhau bằng dấu phẩy.
  - A = (1, 0, 2); (0, 1, -1); (-1, 0, -1)  (từng hàng)
  - **Đáp án:** 0, -4, -2
    1. A khả nghịch vì det A khác 0, nên x = A^(-1) b.
    2. Khử Gauss-Jordan trên (A | I) (hoặc lấy phần phụ hợp chia cho det A): A^(-1) có hàng (-1, 0, -2), (1, 1, 1), (1, 0, 1).
    3. Nhân A^(-1) với b: x = (0, -4, -2). Thử lại: A x = (-4, -2, 2) = b.
  - **Câu hỏi:** Ma trận A như hình có det A = -1. Giải hệ Ax = b với b = (3, 0, 4) bằng cách tìm A^(-1). Nhập ba tọa độ của x, cách nhau bằng dấu phẩy.
  - A = (1, -2, 2); (2, -3, 2); (1, 0, -3)  (từng hàng)
  - **Đáp án:** -35, -32, -13
    1. A khả nghịch vì det A khác 0, nên x = A^(-1) b.
    2. Khử Gauss-Jordan trên (A | I) (hoặc lấy phần phụ hợp chia cho det A): A^(-1) có hàng (-9, 6, -2), (-8, 5, -2), (-3, 2, -1).
    3. Nhân A^(-1) với b: x = (-35, -32, -13). Thử lại: A x = (3, 0, 4) = b.

## Tầng 7: Không gian vectơ

36 dạng câu (32 câu viết tay, 4 bộ sinh câu); 36 chưa duyệt.

### Không gian vectơ và các tiên đề (`dstt_t7_khong_gian_vecto`)

- `dstt_t7_kgv_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập R^2 với phép cộng thông thường và phép nhân với số định nghĩa bởi k.(x, y) = (kx, 0) là một không gian vectơ.
  - **Đáp án:** Sai
    1. Tiên đề nhân với số 1 đòi hỏi 1.u = u với mọi u.
    2. Ở đây 1.(1, 2) = (1, 0), khác (1, 2).
    3. Một tiên đề bị vi phạm nên đây không phải là không gian vectơ: mệnh đề sai.
- `dstt_t7_kgv_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập V = {(x, y) trong R^2 : x > 0} với phép cộng và phép nhân với số thông thường không phải là không gian vectơ. Lý do nào đúng?
    - **(đúng)** Nhân (1, 0) với số -1 được (-1, 0), không thuộc V
    - Phép cộng trên V không có tính giao hoán
    - V không chứa vectơ nào
    - Tổng của hai vectơ thuộc V có thể không thuộc V
  - **Đáp án:** Nhân (1, 0) với số -1 được (-1, 0), không thuộc V
    1. Tổng hai vectơ có hoành độ dương vẫn có hoành độ dương, và phép cộng vẫn giao hoán.
    2. Nhưng nhân với số âm làm hoành độ âm: (-1).(1, 0) = (-1, 0) không thuộc V.
    3. V không đóng với phép nhân với số (nó cũng không chứa (0, 0)), nên không là không gian vectơ.
- `dstt_t7_kgv_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi tập bên trái đi cùng các phép toán đã nêu (phép toán thông thường nếu không nói gì). Ghép mỗi tập với điều đúng về nó.
  - **Đáp án (ghép đúng):**
    - R^2 — Là không gian vectơ
    - R^2, phép cộng thông thường, k.(x, y) = (kx, 0) — Sai tiên đề 1u = u
    - {(x, y) : x >= 0 và y >= 0} — Không đóng với phép nhân với số âm
    - {(x, y) : x và y là số nguyên} — Không đóng với phép nhân với số 1/2
  - **Lời giải:**
    1. R^2 với các phép toán thông thường là không gian vectơ mẫu.
    2. Phép nhân k.(x, y) = (kx, 0) cho 1.(1, 2) = (1, 0): sai tiên đề 1u = u.
    3. Góc phần tư thứ nhất đóng với phép cộng và nhân với số dương, nhưng (-1).(1, 1) = (-1, -1) ra ngoài.
    4. Tập các điểm nguyên đóng với phép cộng và nhân với số nguyên, nhưng (1/2).(1, 0) = (1/2, 0) ra ngoài.
- `dstt_t7_kgv_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau chứng minh rằng trong mọi không gian vectơ, (-1)u là vectơ đối của u. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_vt_03`, `dstt_t7_kgv_01`, `dstt_t7_kgv_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Cần chỉ ra u + (-1)u = 0; khi đó (-1)u là vectơ đối của u, vì vectơ đối là duy nhất.
    2. Theo tiên đề 1u = u: u + (-1)u = 1u + (-1)u.
    3. Theo tiên đề (kl)u = k(lu): 1u + (-1)u = (1 . (-1))u = (-1)u.   **<- bước sai đầu tiên**
    4. Vậy u + (-1)u = (-1)u, nên u = 0.
  - **Đáp án:** Bước 3: Theo tiên đề (kl)u = k(lu): 1u + (-1)u = (1 . (-1))u = (-1)u.
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 dùng sai tiên đề: tổng 1u + (-1)u là tổng của hai vectơ, không phải tích hai số.
    2. Tiên đề đúng là (k + l)u = ku + lu: 1u + (-1)u = (1 + (-1))u = 0u = 0.
    3. Vậy u + (-1)u = 0, tức (-1)u = -u.
- `dstt_t7_kgv_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh rằng trong mọi không gian vectơ, 0u = 0 (số 0 nhân với vectơ u cho vectơ không).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_vt_03`, `dstt_t7_kgv_02`
  - **Đáp án (thứ tự đúng):**
    1. Theo tiên đề phân phối với phép cộng số: 0u = (0 + 0)u = 0u + 0u.
    2. Cộng vectơ đối -(0u) vào cả hai vế của đẳng thức vừa có.
    3. Vế trái thành 0; vế phải, nhờ tính kết hợp, thành 0u + (0u + (-(0u))) = 0u + 0 = 0u.
    4. Hai vế bằng nhau, nên 0u = 0.
  - **Lời giải:**
    1. Mở đầu bằng 0 = 0 + 0 và tiên đề (k + l)u = ku + lu để có 0u = 0u + 0u.
    2. Rồi cộng vectơ đối của 0u vào hai vế: một bên còn 0, bên kia còn 0u.
    3. Từ đó 0u = 0.

### Không gian con (`dstt_t7_khong_gian_con`)

- `dstt_t7_kgc_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập W = {(x, y, z) trong R^3 : x - 2y + z = 0} là một không gian con của R^3.
  - **Đáp án:** Đúng
    1. (0, 0, 0) thỏa phương trình nên thuộc W.
    2. Nếu u, v thỏa x - 2y + z = 0 thì u + v và ku cũng thỏa, vì vế trái tuyến tính và vế phải bằng 0.
    3. W đóng với hai phép toán: là không gian con. Mệnh đề đúng.
- `dstt_t7_kgc_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập W = {(x, y) trong R^2 : xy = 0} (hợp của hai trục tọa độ) là một không gian con của R^2.
  - **Đáp án:** Sai
    1. (1, 0) và (0, 1) đều thuộc W.
    2. Tổng (1, 1) có xy = 1 khác 0, nên không thuộc W.
    3. W không đóng với phép cộng: không là không gian con. Mệnh đề sai.
- `dstt_t7_kgc_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập nào sau đây là không gian con của R^3?
    - **(đúng)** {(x, y, z) : x = 2y và z = 0}
    - {(x, y, z) : x + y + z = 1}
    - {(x, y, z) : x >= 0}
    - {(x, y, z) : x = y^2}
  - **Đáp án:** {(x, y, z) : x = 2y và z = 0}
    1. {x = 2y, z = 0} là tập nghiệm của một hệ thuần nhất, nên là không gian con.
    2. x + y + z = 1 không chứa (0, 0, 0); x >= 0 không đóng với nhân số âm.
    3. x = y^2: (1, 1, 0) thuộc tập nhưng 2(1, 1, 0) = (2, 2, 0) thì không, vì 2 khác 4.
- `dstt_t7_kgc_04` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với m là tham số, xét W = {(x, y, z) trong R^3 : x + 2y - z = m - 3}. Tìm giá trị của m để W là một không gian con của R^3.
  - **Đáp án:** 3
    1. Không gian con phải chứa (0, 0, 0): thay vào được 0 = m - 3, nên m = 3.
    2. Với m = 3, W là tập nghiệm của phương trình thuần nhất x + 2y - z = 0, đóng với phép cộng và phép nhân với số.
    3. Vậy m = 3.
- `dstt_t7_kgc_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau xét W = {(x, y, z) trong R^3 : x + y = 1} có là không gian con của R^3 không. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t7_kgc_04`
  - **Lời giải đưa ra (có một bước sai):**
    1. Lấy u = (x1, y1, z1) và v = (x2, y2, z2) thuộc W, tức x1 + y1 = 1 và x2 + y2 = 1.
    2. Hai tọa độ đầu của u + v cộng lại bằng (x1 + y1) + (x2 + y2) = 2.
    3. Với số k bất kỳ, hai tọa độ đầu của ku cộng lại bằng k(x1 + y1) = k.
    4. Vì u + v và ku đều là bộ ba số thực (x, y, z), W đóng với hai phép toán và là không gian con.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vì u + v và ku đều là bộ ba số thực (x, y, z), W đóng với hai phép toán và là không gian con.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: để thuộc W, tổng hai tọa độ đầu phải bằng 1, không chỉ là một bộ ba số thực.
    2. Bước 2 cho tổng bằng 2, khác 1, nên u + v không thuộc W; W cũng không chứa (0, 0, 0).
    3. Vậy W không phải là không gian con của R^3.
- `dstt_t7_kgc_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** W1 và W2 là hai không gian con của không gian vectơ V. Sắp xếp các bước chứng minh W1 giao W2 cũng là không gian con của V.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_01`, `dstt_t7_kgc_03`
  - **Đáp án (thứ tự đúng):**
    1. Lấy u, v thuộc W1 giao W2 và một số k bất kỳ.
    2. Vì u, v thuộc W1 và W1 là không gian con, nên u + v và ku thuộc W1.
    3. Lý luận như vậy với W2: u + v và ku cũng thuộc W2.
    4. Do đó u + v và ku thuộc W1 giao W2: giao đóng với phép cộng và phép nhân với số.
    5. Thêm nữa vectơ 0 thuộc cả hai không gian con nên giao khác rỗng; vậy W1 giao W2 là không gian con.
  - **Lời giải:**
    1. Kiểm tra tiêu chuẩn không gian con cho W1 giao W2: lấy hai phần tử và một số.
    2. Dùng tính đóng của W1, rồi của W2, để thấy tổng và tích thuộc cả hai.
    3. Kết luận, nhớ thêm rằng giao chứa 0 nên khác rỗng.
- `dstt_t7_kgc_07` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^4 với tọa độ (x, y, z, t), xét W = {(x, y, z, t) : x + y - z = 0 và y + 2t = 0}.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_04`, `dstt_t7_kgc_01`, `dstt_g5_an_tu_do`
  - **Phần a** (Đúng/Sai): a) W là một không gian con của R^4.
    - **Đáp án a:** Đúng
  - **Phần b** (Điền số): b) Tìm số chiều của W.
    - **Đáp án b:** 2
  - **Phần c** (Điền số): c) Vectơ (a, -2, 1, 1) thuộc W. Tìm a.
    - **Đáp án c:** 3
  - **Lời giải:**
    1. a) W là tập nghiệm của một hệ thuần nhất hai phương trình, nên là không gian con. Đúng.
    2. b) Hai phương trình độc lập (ma trận hệ số có hạng 2), bốn ẩn: số ẩn tự do là 4 - 2 = 2, nên dim W = 2.
    3. c) Phương trình thứ hai: -2 + 2 . 1 = 0, thỏa. Phương trình thứ nhất: a - 2 - 1 = 0, nên a = 3.

### Tổ hợp tuyến tính và bao tuyến tính (`dstt_t7_to_hop_tuyen_tinh`)

- `dstt_t7_thtt_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho u = (1, 0, 2), v = (2, 1, 3) và w = (4, 1, 7) trong R^3. Tìm a, b sao cho w = au + bv. Nhập a rồi b, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 1
    1. Viết theo từng tọa độ: a + 2b = 4, b = 1 và 2a + 3b = 7.
    2. Từ phương trình thứ hai b = 1, thế vào phương trình đầu: a = 2.
    3. Kiểm tra phương trình thứ ba: 2 . 2 + 3 . 1 = 7, đúng. Vậy a = 2, b = 1.
- `dstt_t7_thtt_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Vectơ (1, 2, 4) thuộc span{(1, 0, 1), (0, 1, 1)} trong R^3.
  - **Đáp án:** Sai
    1. a(1, 0, 1) + b(0, 1, 1) = (a, b, a + b).
    2. Muốn bằng (1, 2, 4) thì a = 1, b = 2 và a + b = 4; nhưng 1 + 2 = 3.
    3. Hệ vô nghiệm, nên vectơ đó không thuộc span: mệnh đề sai.
- `dstt_g7_to_hop` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3 cho u = (0, 1, 3), v = (2, -2, -1) và w = (4, -5, m). Tìm m để w thuộc span{u, v}.
  - **Đáp án:** -5
    1. w thuộc span{u, v} khi có a, b với au + bv = w. Hai tọa độ đầu cho hệ 2b = 4 và a - 2b = -5.
    2. Hệ này có định thức -2 khác 0, nghiệm duy nhất a = -1, b = 2.
    3. Tọa độ thứ ba phải khớp: m = (-1) . 3 + 2 . (-1) = -5.
  - **Câu hỏi:** Trong R^3 cho u = (3, 1, 1), v = (1, 1, 2) và w = (8, 4, m). Tìm m để w thuộc span{u, v}.
  - **Đáp án:** 6
    1. w thuộc span{u, v} khi có a, b với au + bv = w. Hai tọa độ đầu cho hệ 3a + b = 8 và a + b = 4.
    2. Hệ này có định thức 2 khác 0, nghiệm duy nhất a = 2, b = 2.
    3. Tọa độ thứ ba phải khớp: m = 2 . 1 + 2 . 2 = 6.
  - **Câu hỏi:** Trong R^3 cho u = (2, 3, -1), v = (0, 1, 3) và w = (2, 5, m). Tìm m để w thuộc span{u, v}.
  - **Đáp án:** 5
    1. w thuộc span{u, v} khi có a, b với au + bv = w. Hai tọa độ đầu cho hệ 2a = 2 và 3a + b = 5.
    2. Hệ này có định thức 2 khác 0, nghiệm duy nhất a = 1, b = 2.
    3. Tọa độ thứ ba phải khớp: m = 1 . (-1) + 2 . 3 = 5.
- `dstt_t7_thtt_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho u = (1, 1, 0), v = (0, 1, 1) và w = (1, m, 2) trong R^3, với m là tham số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g5_giai_he_2`, `dstt_t7_thtt_01`, `dstt_g7_to_hop`
  - **Phần a** (Điền số): a) Tìm m để w thuộc span{u, v}.
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Với m vừa tìm, nhập a rồi b sao cho w = au + bv, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 1, 2
  - **Phần c** (Đúng/Sai): c) Với m = 0, span{u, v, w} là toàn bộ R^3.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) au + bv = (a, a + b, b). Tọa độ đầu và cuối cho a = 1, b = 2; khi đó tọa độ giữa là m = a + b = 3.
    2. b) a = 1, b = 2: u + 2v = (1, 3, 2) = w.
    3. c) Với m = 0, ma trận có các hàng u, v, w = (1, 0, 2) có định thức 1 . (2 - 0) - 1 . (0 - 1) + 0 = 3, khác 0: ba vectơ độc lập, sinh ra R^3. Đúng.
- `dstt_t7_thtt_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau xét (3, 1, 5) có thuộc span{(1, 2, 1), (2, 3, 3)} không. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t5_sn_04`, `dstt_t7_thtt_02`, `dstt_t7_thtt_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Cần a, b với a(1, 2, 1) + b(2, 3, 3) = (3, 1, 5), tức a + 2b = 3, 2a + 3b = 1 và a + 3b = 5.
    2. Trừ phương trình đầu khỏi phương trình cuối: b = 2, nên a = 3 - 4 = -1.
    3. Hai phương trình vừa dùng đều thỏa với a = -1, b = 2.
    4. Vậy (3, 1, 5) = -(1, 2, 1) + 2(2, 3, 3), nên vectơ đó thuộc span.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Vậy (3, 1, 5) = -(1, 2, 1) + 2(2, 3, 3), nên vectơ đó thuộc span.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 kết luận khi chưa thử phương trình thứ hai.
    2. Với a = -1, b = 2: 2a + 3b = -2 + 6 = 4, khác 1. Hệ ba phương trình vô nghiệm.
    3. Thật vậy -(1, 2, 1) + 2(2, 3, 3) = (3, 4, 5), không phải (3, 1, 5). Vectơ đó không thuộc span.

### Độc lập và phụ thuộc tuyến tính (`dstt_t7_doc_lap_tuyen_tinh`)

- `dstt_t7_dltt_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm m để ba vectơ (1, 2, 1), (0, 1, 3) và (2, m, 5) của R^3 phụ thuộc tuyến tính.
  - **Đáp án:** 5
    1. Ba vectơ của R^3 phụ thuộc tuyến tính khi ma trận có ba hàng là chúng có định thức bằng 0.
    2. Khai triển theo hàng 1: 1 . (5 - 3m) - 2 . (0 - 6) + 1 . (0 - 2) = 15 - 3m.
    3. 15 - 3m = 0 khi m = 5.
- `dstt_t7_dltt_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho u, v, w độc lập tuyến tính trong một không gian vectơ. Họ nào sau đây phụ thuộc tuyến tính?
    - **(đúng)** u - v, v - w, w - u
    - u + v, v + w, w + u
    - u, u + v, u + v + w
    - 2u, 3v, w
  - **Đáp án:** u - v, v - w, w - u
    1. (u - v) + (v - w) + (w - u) = 0 là một quan hệ với hệ số 1, 1, 1 không đồng thời bằng 0: họ đầu phụ thuộc.
    2. Các họ khác: viết a(u + v) + b(v + w) + c(w + u) = 0 ra theo u, v, w thì hệ a + c = a + b = b + c = 0 chỉ có nghiệm 0; tương tự cho hai họ còn lại.
    3. Vậy chỉ họ u - v, v - w, w - u phụ thuộc tuyến tính.
- `dstt_g7_doc_lap` · bậc 4 (Nâng cao) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3, họ u = (2, 0, 3), v = (-2, -3, 0), w = (-4, 2, 2) độc lập tuyến tính.
  - **Đáp án:** Đúng
    1. Ba vectơ của R^3 độc lập tuyến tính khi và chỉ khi ma trận có ba hàng u, v, w có định thức khác 0 (hệ au + bv + cw = 0 chỉ có nghiệm tầm thường).
    2. Định thức đó bằng -60, khác 0.
    3. Vậy họ u, v, w độc lập tuyến tính: mệnh đề đúng.
  - **Câu hỏi:** Trong R^3, họ u = (3, -3, -3), v = (-3, -1, 3), w = (-6, 2, 6) độc lập tuyến tính.
  - **Đáp án:** Sai
    1. Ba vectơ của R^3 độc lập tuyến tính khi và chỉ khi ma trận có ba hàng u, v, w có định thức khác 0 (hệ au + bv + cw = 0 chỉ có nghiệm tầm thường).
    2. Định thức đó bằng 0.
    3. Thật vậy w = -u + v, nên -u + v - w = 0 là một quan hệ không tầm thường: họ phụ thuộc tuyến tính, mệnh đề sai.
  - **Câu hỏi:** Trong R^3, họ u = (1, -2, -1), v = (1, 0, 2), w = (-3, -4, 3) độc lập tuyến tính.
  - **Đáp án:** Đúng
    1. Ba vectơ của R^3 độc lập tuyến tính khi và chỉ khi ma trận có ba hàng u, v, w có định thức khác 0 (hệ au + bv + cw = 0 chỉ có nghiệm tầm thường).
    2. Định thức đó bằng 30, khác 0.
    3. Vậy họ u, v, w độc lập tuyến tính: mệnh đề đúng.
- `dstt_t7_dltt_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** u, v, w độc lập tuyến tính. Sắp xếp các bước chứng minh u + v, v + w, w + u cũng độc lập tuyến tính.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_dltt_02`, `dstt_g5_tam_thuong`
  - **Đáp án (thứ tự đúng):**
    1. Giả sử a(u + v) + b(v + w) + c(w + u) = 0.
    2. Gom theo u, v, w: (a + c)u + (a + b)v + (b + c)w = 0.
    3. Vì u, v, w độc lập tuyến tính nên a + c = 0, a + b = 0 và b + c = 0.
    4. Cộng ba đẳng thức được 2(a + b + c) = 0, nên a + b + c = 0.
    5. Trừ lần lượt từng đẳng thức: b = 0, c = 0, a = 0; vậy họ mới độc lập tuyến tính.
  - **Lời giải:**
    1. Bắt đầu từ một tổ hợp tuyến tính bằng 0, gom hệ số theo u, v, w.
    2. Dùng tính độc lập của u, v, w để có hệ ba phương trình với a, b, c.
    3. Giải hệ thấy a = b = c = 0.
- `dstt_t7_dltt_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau xét họ u = (1, 2, 3), v = (2, 4, 6), w = (0, 1, 1) trong R^3. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t5_htn_03`, `dstt_t7_dltt_01`, `dstt_g7_doc_lap`
  - **Lời giải đưa ra (có một bước sai):**
    1. Xét au + bv + cw = 0, tức a + 2b = 0, 2a + 4b + c = 0 và 3a + 6b + c = 0.
    2. Từ phương trình đầu: a = -2b. Thế vào phương trình thứ hai: c = 0.
    3. Thế vào phương trình thứ ba cũng được c = 0.
    4. Hệ chỉ có nghiệm a = b = c = 0, nên họ độc lập tuyến tính.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Hệ chỉ có nghiệm a = b = c = 0, nên họ độc lập tuyến tính.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 sai: các bước trên chỉ cho c = 0 và a = -2b, còn b tùy ý.
    2. Chọn b = 1 được a = -2: -2u + v + 0w = 0 (thật vậy v = 2u).
    3. Hệ có nghiệm khác 0, nên họ phụ thuộc tuyến tính.
- `dstt_t7_dltt_06` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi ba vectơ u, v, w của R^3: nếu u, v, w phụ thuộc tuyến tính thì w là tổ hợp tuyến tính của u và v.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_dltt_02`, `dstt_g7_doc_lap`
  - **Đáp án:** Sai
    1. Phụ thuộc tuyến tính chỉ nói có MỘT vectơ là tổ hợp của các vectơ còn lại, không nhất thiết là w.
    2. Phản ví dụ: u = (1, 0, 0), v = (2, 0, 0), w = (0, 1, 0). Họ phụ thuộc vì v = 2u.
    3. Nhưng mọi tổ hợp của u, v có tọa độ thứ hai bằng 0, nên w không là tổ hợp của u, v. Mệnh đề sai.

### Cơ sở và số chiều (`dstt_t7_co_so_so_chieu`)

- `dstt_t7_csc_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm số chiều của không gian nghiệm của hệ thuần nhất x + y + z + t = 0, x - y + 2z = 0 (bốn ẩn x, y, z, t).
  - **Đáp án:** 2
    1. Ma trận hệ số có hai hàng (1, 1, 1, 1) và (1, -1, 2, 0), không tỉ lệ, nên có hạng 2.
    2. Số ẩn tự do bằng số ẩn trừ hạng: 4 - 2 = 2.
    3. Số chiều của không gian nghiệm bằng số ẩn tự do: 2.
- `dstt_t7_csc_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ba vectơ (1, 1, 0), (0, 1, 1), (1, 0, 1) lập thành một cơ sở của R^3.
  - **Đáp án:** Đúng
    1. Ba vectơ trong R^3 (có số chiều 3) là cơ sở khi và chỉ khi chúng độc lập tuyến tính.
    2. Ma trận có ba hàng đó có định thức 1 . (1 - 0) - 1 . (0 - 1) + 0 = 2, khác 0.
    3. Vậy chúng độc lập, và là một cơ sở của R^3. Mệnh đề đúng.
- `dstt_t7_csc_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi không gian con của R^3 với số chiều của nó.
  - **Đáp án (ghép đúng):**
    - span{(1, 2, 3), (2, 4, 6)} — 1
    - {(x, y, z) : x + y + z = 0} — 2
    - span{(1, 0, 0), (0, 1, 0), (1, 1, 1)} — 3
    - {(x, y, z) : x = y = z = 0} — 0
  - **Lời giải:**
    1. (2, 4, 6) = 2(1, 2, 3), nên span đầu là một đường thẳng: số chiều 1.
    2. Mặt phẳng x + y + z = 0: một phương trình, ba ẩn, hai ẩn tự do: số chiều 2.
    3. (1, 0, 0), (0, 1, 0), (1, 1, 1) có định thức khác 0 nên sinh ra R^3: số chiều 3.
    4. Không gian chỉ gồm vectơ 0 có số chiều 0.
- `dstt_t7_csc_07` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho u1 = (1, 2, 1), u2 = (2, 4, 2), u3 = (0, 1, 1) trong R^3. Sắp xếp các bước tìm một cơ sở và số chiều của span{u1, u2, u3}.
  - **Đáp án (thứ tự đúng):**
    1. Đặt u1, u2, u3 làm ba cột của ma trận A: các hàng của A là (1, 2, 0), (2, 4, 1), (1, 2, 1).
    2. R2 - 2R1 và R3 - R1 cho các hàng (1, 2, 0), (0, 0, 1), (0, 0, 1).
    3. R3 - R2 cho hàng 0: dạng bậc thang có trụ ở cột 1 và cột 3.
    4. Lấy cột 1 và cột 3 của A ban đầu: u1, u3 là một cơ sở, và số chiều của span bằng 2.
  - **Lời giải:**
    1. Các vectơ đặt làm cột, khử Gauss để tìm các cột có trụ.
    2. Trụ ở cột 1 và cột 3 (u2 = 2u1 không cho trụ mới).
    3. Các cột có trụ của CHÍNH A, tức u1 và u3, là một cơ sở; số chiều 2.
- `dstt_g7_so_chieu` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^4 cho u1 = (0, 1, -2, 0), u2 = (1, -2, -2, 2), u3 = (0, 0, 0, 1). Tìm số chiều của W = span{u1, u2, u3}.
  - **Đáp án:** 3
    1. dim W bằng hạng của ma trận có các hàng là các vectơ đã cho.
    2. Khử Gauss ma trận đó (các phép biến đổi hàng không làm đổi bao tuyến tính của các hàng).
    3. Dạng bậc thang còn 3 hàng khác 0, nên dim W = 3.
  - **Câu hỏi:** Trong R^3 cho u1 = (0, 1, -3), u2 = (-1, -3, 1), u3 = (1, 1, 2), u4 = (0, 0, 1). Tìm số chiều của W = span{u1, u2, u3, u4}.
  - **Đáp án:** 3
    1. dim W bằng hạng của ma trận có các hàng là các vectơ đã cho.
    2. Khử Gauss ma trận đó (các phép biến đổi hàng không làm đổi bao tuyến tính của các hàng).
    3. Dạng bậc thang còn 3 hàng khác 0, nên dim W = 3. Các vectơ còn lại là tổ hợp tuyến tính của các vectơ ứng với hàng trụ.
  - **Câu hỏi:** Trong R^3 cho u1 = (0, 0, 2), u2 = (0, 0, 1), u3 = (0, 1, 1). Tìm số chiều của W = span{u1, u2, u3}.
  - **Đáp án:** 2
    1. dim W bằng hạng của ma trận có các hàng là các vectơ đã cho.
    2. Khử Gauss ma trận đó (các phép biến đổi hàng không làm đổi bao tuyến tính của các hàng).
    3. Dạng bậc thang còn 2 hàng khác 0, nên dim W = 2. Các vectơ còn lại là tổ hợp tuyến tính của các vectơ ứng với hàng trụ.
- `dstt_t7_csc_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^4 cho u1 = (1, 2, 0, 1), u2 = (2, 4, 1, 3), u3 = (0, 0, 1, 1), u4 = (1, 2, 1, 2) và W = span{u1, u2, u3, u4}.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_hang`, `dstt_t7_csc_02`, `dstt_g7_so_chieu`
  - **Phần a** (Điền số): a) Tìm dim W.
    - **Đáp án a:** 2
  - **Phần b** (Trắc nghiệm): b) Họ nào sau đây là một cơ sở của W?
    - **(đúng)** u1, u3
    - u1, u2, u3
    - u3
    - u1, u2, u3, u4
    - **Đáp án b:** u1, u3
  - **Phần c** (Điền số): c) Viết u2 = a u1 + b u3. Nhập a rồi b, cách nhau bằng dấu phẩy.
    - **Đáp án c:** 2, 1
  - **Lời giải:**
    1. a) Khử Gauss ma trận có bốn hàng u1, ..., u4: R2 - 2R1 = (0, 0, 1, 1) = u3 và R4 - R1 = (0, 0, 1, 1); trừ tiếp còn hai hàng khác 0. dim W = 2.
    2. b) u1 và u3 không tỉ lệ nên độc lập, và có đúng dim W = 2 vectơ: là một cơ sở. Họ ba hoặc bốn vectơ phụ thuộc; một vectơ không đủ sinh W.
    3. c) 2u1 + u3 = (2, 4, 0, 2) + (0, 0, 1, 1) = (2, 4, 1, 3) = u2, nên a = 2, b = 1.
- `dstt_t7_csc_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm một cơ sở và số chiều của W = {(x, y, z) trong R^3 : x - 2y + 3z = 0}. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t5_htn_04`, `dstt_t7_csc_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. W là không gian nghiệm của một phương trình thuần nhất ba ẩn.
    2. Chọn y, z làm ẩn tự do; khi đó x = 2y - 3z.
    3. Mỗi vectơ của W có dạng (2y - 3z, y, z) = y(2, 1, 0) + z(-3, 0, 1).
    4. Hai vectơ (2, 1, 0) và (-3, 0, 1) độc lập tuyến tính, nên chúng là một cơ sở của W.
    5. Vậy dim W = 3, bằng số ẩn của phương trình.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 5: Vậy dim W = 3, bằng số ẩn của phương trình.
  - **Vì sao sai, và bước đúng:**
    1. Số chiều là số vectơ trong một cơ sở, không phải số ẩn.
    2. Cơ sở tìm được ở bước 4 có hai vectơ, nên dim W = 2 (bằng số ẩn tự do, 3 - 1).
    3. W là một mặt phẳng qua gốc trong R^3.
- `dstt_t7_csc_06` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3 cho U = span{(1, 0, 1), (0, 1, 1)} và W = {(x, y, z) : x + y + z = 0}. Tìm dim(U giao W) rồi dim(U + W). Nhập hai số, cách nhau bằng dấu phẩy.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_csc_03`, `dstt_t7_csc_01`, `dstt_g7_so_chieu`
  - **Đáp án:** 1, 3
    1. Mỗi vectơ của U có dạng a(1, 0, 1) + b(0, 1, 1) = (a, b, a + b). Nó thuộc W khi a + b + (a + b) = 0, tức b = -a.
    2. Vậy U giao W = {(a, -a, 0)} = span{(1, -1, 0)}, có số chiều 1.
    3. dim U = 2 và dim W = 2, nên dim(U + W) = 2 + 2 - 1 = 3: U + W = R^3.

### Tọa độ và ma trận chuyển cơ sở (`dstt_t7_toa_do`)

- `dstt_t7_td_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong không gian các đa thức bậc không quá 2, tìm tọa độ của p(x) = 5 + 4x + x^2 trong cơ sở 1, 1 + x, 1 + x + x^2. Nhập ba tọa độ theo thứ tự đó, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 3, 1
    1. Tìm a, b, c với a . 1 + b(1 + x) + c(1 + x + x^2) = 5 + 4x + x^2.
    2. So sánh hệ số: x^2 cho c = 1; x cho b + c = 4, nên b = 3; hệ số tự do cho a + b + c = 5, nên a = 1.
    3. Tọa độ là (1, 3, 1).
- `dstt_t7_td_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^2, cơ sở B gồm b1 = (1, 1) và b2 = (1, -1). Vectơ x có tọa độ (3, 1) trong B. Vectơ x là vectơ nào?
    - **(đúng)** (4, 2)
    - (3, 1)
    - (2, 4)
    - (4, -2)
  - **Đáp án:** (4, 2)
    1. Tọa độ (3, 1) trong B nghĩa là x = 3 b1 + 1 b2.
    2. x = 3(1, 1) + (1, -1) = (4, 2).
    3. Chú ý: (3, 1) là tọa độ, không phải chính vectơ x.
- `dstt_g7_toa_do` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Các vectơ b1 = (1, 1, -1), b2 = (1, 2, 0), b3 = (0, -1, 0) lập thành một cơ sở của R^3. Tìm tọa độ của x = (-2, -4, -1) trong cơ sở đó. Nhập ba tọa độ theo thứ tự b1, b2, b3, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, -3, -1
    1. Tọa độ (a, b, c) thỏa a b1 + b b2 + c b3 = x: một hệ ba phương trình, ba ẩn, ma trận hệ số có các cột là b1, b2, b3.
    2. Giải hệ bằng khử Gauss.
    3. Nghiệm: (1, -3, -1). Thử lại: b1 - 3b2 - b3 = (-2, -4, -1).
  - **Câu hỏi:** Các vectơ b1 = (1, -1, -1), b2 = (0, 1, -1), b3 = (-1, 1, 2) lập thành một cơ sở của R^3. Tìm tọa độ của x = (1, 0, -4) trong cơ sở đó. Nhập ba tọa độ theo thứ tự b1, b2, b3, cách nhau bằng dấu phẩy.
  - **Đáp án:** -1, 1, -2
    1. Tọa độ (a, b, c) thỏa a b1 + b b2 + c b3 = x: một hệ ba phương trình, ba ẩn, ma trận hệ số có các cột là b1, b2, b3.
    2. Giải hệ bằng khử Gauss.
    3. Nghiệm: (-1, 1, -2). Thử lại: -b1 + b2 - 2b3 = (1, 0, -4).
  - **Câu hỏi:** Các vectơ b1 = (1, -1, 1), b2 = (-1, 2, 0), b3 = (0, 2, 3) lập thành một cơ sở của R^3. Tìm tọa độ của x = (-2, 6, 3) trong cơ sở đó. Nhập ba tọa độ theo thứ tự b1, b2, b3, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 2, 1
    1. Tọa độ (a, b, c) thỏa a b1 + b b2 + c b3 = x: một hệ ba phương trình, ba ẩn, ma trận hệ số có các cột là b1, b2, b3.
    2. Giải hệ bằng khử Gauss.
    3. Nghiệm: (0, 2, 1). Thử lại: 2b2 + b3 = (-2, 6, 3).
- `dstt_t7_td_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^2 có hai cơ sở B = {b1 = (1, 0), b2 = (1, 1)} và B' = {c1 = (2, 1), c2 = (1, 2)}. Gọi P là ma trận có cột j là tọa độ của c_j trong cơ sở B.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_nghich_dao_2`, `dstt_t7_td_02`, `dstt_g7_toa_do`
  - **Phần a** (Điền số): a) Tìm P. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 1, -1, 1, 2
  - **Phần b** (Điền số): b) Vectơ x có tọa độ (1, 1) trong B'. Tìm tọa độ của x trong B, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 0, 3
  - **Phần c** (Đúng/Sai): c) Với mọi x, tọa độ của x trong B' bằng P^(-1) nhân tọa độ của x trong B.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) c1 = a b1 + b b2 = (a + b, b) = (2, 1) cho b = 1, a = 1. c2 = (1, 2) cho b = 2, a = -1. Hai cột (1, 1) và (-1, 2): P có hàng (1, -1) và (1, 2).
    2. b) [x]_B = P [x]_B' = P(1, 1) = (0, 3). Thử lại: x = c1 + c2 = (3, 3) = 0 b1 + 3 b2.
    3. c) Vì [x]_B = P [x]_B' và P khả nghịch (det P = 3), nhân P^(-1) bên trái được [x]_B' = P^(-1) [x]_B. Đúng.
- `dstt_t7_td_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm tọa độ của x = (5, 3) trong cơ sở b1 = (2, 1), b2 = (3, 2) của R^2. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_nghich_dao_2`, `dstt_t7_td_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. Tọa độ cần tìm là cặp (a, b) với a b1 + b b2 = x.
    2. Đặt P là ma trận có hàng 1 là b1 và hàng 2 là b2, tức P có hàng (2, 1) và (3, 2); khi đó P(a, b) = x.   **<- bước sai đầu tiên**
    3. det P = 1, nên P^(-1) có hàng (2, -1) và (-3, 2).
    4. (a, b) = P^(-1) x = (2 . 5 - 1 . 3, -3 . 5 + 2 . 3) = (7, -9).
  - **Đáp án:** Bước 2: Đặt P là ma trận có hàng 1 là b1 và hàng 2 là b2, tức P có hàng (2, 1) và (3, 2); khi đó P(a, b) = x.
  - **Vì sao sai, và bước đúng:**
    1. a b1 + b b2 = P(a, b) khi b1, b2 là các CỘT của P, không phải các hàng.
    2. P đúng có hàng (2, 3) và (1, 2), P^(-1) có hàng (2, -3) và (-1, 2), nên (a, b) = (10 - 9, -5 + 6) = (1, 1).
    3. Thử lại: (2, 1) + (3, 2) = (5, 3). Còn 7(2, 1) - 9(3, 2) = (-13, -11), sai.

## Tầng 8: Ánh xạ tuyến tính và ma trận của nó

38 dạng câu (33 câu viết tay, 5 bộ sinh câu); 38 chưa duyệt.

### Ánh xạ tuyến tính (`dstt_t8_anh_xa_tuyen_tinh`)

- `dstt_t8_axtt_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ f: R^2 -> R^2, f(x, y) = (x + y, x - 1) là ánh xạ tuyến tính.
  - **Đáp án:** Sai
    1. Ánh xạ tuyến tính luôn biến 0 thành 0, vì f(0) = f(0 . 0) = 0 . f(0) = 0.
    2. Ở đây f(0, 0) = (0, -1), khác (0, 0).
    3. Vậy f không tuyến tính: mệnh đề sai.
- `dstt_t8_axtt_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ nào sau đây từ R^2 vào R là ánh xạ tuyến tính?
    - **(đúng)** f(x, y) = 3x - 2y
    - f(x, y) = xy
    - f(x, y) = x + y + 1
    - f(x, y) = |x| + y
  - **Đáp án:** f(x, y) = 3x - 2y
    1. 3x - 2y là tổ hợp tuyến tính của x và y: f(u + v) = f(u) + f(v) và f(ku) = k f(u).
    2. xy không tuyến tính: f(2(1, 1)) = 4 nhưng 2 f(1, 1) = 2. x + y + 1 có f(0, 0) = 1 khác 0.
    3. |x| + y: f(-1, 0) = 1 nhưng -f(1, 0) = -1.
- `dstt_t8_axtt_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phép biến đổi tuyến tính của mặt phẳng R^2 với công thức của nó.
  - **Đáp án (ghép đúng):**
    - Chiếu vuông góc lên trục Ox — (x, y) -> (x, 0)
    - Đối xứng qua trục Ox — (x, y) -> (x, -y)
    - Quay 90 độ ngược chiều kim đồng hồ quanh gốc — (x, y) -> (-y, x)
    - Đối xứng qua đường thẳng y = x — (x, y) -> (y, x)
  - **Lời giải:**
    1. Chiếu lên Ox giữ hoành độ, xóa tung độ: (x, 0).
    2. Đối xứng qua Ox đổi dấu tung độ: (x, -y). Đối xứng qua y = x đổi chỗ hai tọa độ: (y, x).
    3. Quay 90 độ ngược chiều kim đồng hồ đưa (1, 0) đến (0, 1) và (0, 1) đến (-1, 0): (x, y) -> (-y, x).
- `dstt_g8_anh_vecto` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có f(2, 1) = (-3, 0) và f(1, 1) = (-3, 3). Tính f(3, 2). Nhập hai tọa độ, cách nhau bằng dấu phẩy.
  - **Đáp án:** -6, 3
    1. Viết (3, 2) = a(2, 1) + b(1, 1); giải hệ hai ẩn được a = 1, b = 1.
    2. Vì f tuyến tính: f(3, 2) = 1 . (-3, 0) + 1 . (-3, 3).
    3. = (-6, 3).
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có f(1, 1) = (-2, 2) và f(3, 2) = (2, 4). Tính f(5, 3). Nhập hai tọa độ, cách nhau bằng dấu phẩy.
  - **Đáp án:** 6, 6
    1. Viết (5, 3) = a(1, 1) + b(3, 2); giải hệ hai ẩn được a = -1, b = 2.
    2. Vì f tuyến tính: f(5, 3) = (-1) . (-2, 2) + 2 . (2, 4).
    3. = (6, 6).
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có f(1, 2) = (-2, 1) và f(1, 3) = (3, -3). Tính f(-1, -5). Nhập hai tọa độ, cách nhau bằng dấu phẩy.
  - **Đáp án:** -13, 11
    1. Viết (-1, -5) = a(1, 2) + b(1, 3); giải hệ hai ẩn được a = 2, b = -3.
    2. Vì f tuyến tính: f(-1, -5) = 2 . (-2, 1) + (-3) . (3, -3).
    3. = (-13, 11).
- `dstt_t8_axtt_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f: R^2 -> R^2 tuyến tính có f(1, 2) = (3, 1) và f(2, 3) = (1, 0). Lời giải sau tính f(1, 0). Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g5_giai_he_2`, `dstt_g8_anh_vecto`
  - **Lời giải đưa ra (có một bước sai):**
    1. Viết (1, 0) = a(1, 2) + b(2, 3): a + 2b = 1 và 2a + 3b = 0.
    2. Giải hệ: a = -3, b = 2.
    3. Vì f tuyến tính, f(1, 0) chính là cặp hệ số vừa tìm: f(1, 0) = (-3, 2).   **<- bước sai đầu tiên**
    4. Thử lại: -3(1, 2) + 2(2, 3) = (1, 0), đúng.
  - **Đáp án:** Bước 3: Vì f tuyến tính, f(1, 0) chính là cặp hệ số vừa tìm: f(1, 0) = (-3, 2).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 nhầm tọa độ của (1, 0) với ảnh của nó.
    2. Đúng ra: f(1, 0) = -3 f(1, 2) + 2 f(2, 3) = -3(3, 1) + 2(1, 0) = (-9, -3) + (2, 0).
    3. Vậy f(1, 0) = (-7, -3).
- `dstt_t8_axtt_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^3 -> R^2 có f(1, 0, 0) = (1, 2), f(1, 1, 0) = (0, 1) và f(1, 1, 1) = (2, 2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_axtt_01`, `dstt_g8_anh_vecto`, `dstt_g6_hang`
  - **Phần a** (Điền số): a) Tìm f(0, 1, 0). Nhập hai tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án a:** -1, -1
  - **Phần b** (Điền số): b) Tìm f(2, 3, -1). Nhập hai tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** -3, 0
  - **Phần c** (Đúng/Sai): c) f là toàn ánh.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) (0, 1, 0) = (1, 1, 0) - (1, 0, 0), nên f(0, 1, 0) = (0, 1) - (1, 2) = (-1, -1). Tương tự f(0, 0, 1) = f(1, 1, 1) - f(1, 1, 0) = (2, 1).
    2. b) f(2, 3, -1) = 2 f(1, 0, 0) + 3 f(0, 1, 0) - f(0, 0, 1) = (2, 4) + (-3, -3) - (2, 1) = (-3, 0).
    3. c) Ma trận chính tắc có ba cột (1, 2), (-1, -1), (2, 1); hai cột đầu có định thức 1 . (-1) - (-1) . 2 = 1 khác 0, nên hạng 2 = dim R^2: f toàn ánh. Đúng.
- `dstt_t8_axtt_06` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi ánh xạ tuyến tính f: V -> W: nếu u1, ..., uk độc lập tuyến tính trong V thì f(u1), ..., f(uk) độc lập tuyến tính trong W.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_axtt_02`, `dstt_t7_dltt_02`
  - **Đáp án:** Sai
    1. Phản ví dụ: ánh xạ không f(u) = 0 là tuyến tính.
    2. Với u1 = (1, 0) độc lập trong R^2, ảnh f(u1) = 0, mà họ chỉ gồm vectơ 0 thì phụ thuộc tuyến tính.
    3. Mệnh đề chỉ đúng khi f đơn ánh. Mệnh đề sai.

### Nhân Ker f và ảnh Im f (`dstt_t8_nhan_va_anh`)

- `dstt_t8_nva_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^3 -> R^2, f(x, y, z) = (x - y, y - z). Tìm vectơ của Ker f có tọa độ thứ nhất bằng 1. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 1, 1
    1. Ker f gồm các vectơ có f(x, y, z) = (0, 0): x - y = 0 và y - z = 0.
    2. Vậy x = y = z: Ker f = span{(1, 1, 1)}.
    3. Vectơ có tọa độ đầu bằng 1 là (1, 1, 1).
- `dstt_t8_nva_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với f: R^2 -> R^2, f(x, y) = (x + 2y, 2x + 4y), vectơ (1, 3) thuộc Im f.
  - **Đáp án:** Sai
    1. f(x, y) = (x + 2y)(1, 2), nên mọi ảnh đều là bội của (1, 2): Im f = span{(1, 2)}.
    2. (1, 3) không là bội của (1, 2), vì 3 khác 2 . 1.
    3. Vậy (1, 3) không thuộc Im f: mệnh đề sai.
- `dstt_t8_nva_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^3 -> R^3, f(v) = Av, với ma trận A như hình. Trong tọa độ (x, y, z) của R^3, Im f là tập nào?
  - A = (1, 2, 3); (0, 1, 1); (1, 3, 4)  (từng hàng)
    - **(đúng)** Mặt phẳng z = x + y
    - Toàn bộ R^3
    - Đường thẳng span{(1, 0, 1)}
    - Mặt phẳng x + y + z = 0
  - **Đáp án:** Mặt phẳng z = x + y
    1. Im f được sinh bởi ba cột (1, 0, 1), (2, 1, 3), (3, 1, 4) của A; cột ba bằng tổng hai cột đầu.
    2. Hai cột đầu không tỉ lệ, nên Im f là mặt phẳng span{(1, 0, 1), (2, 1, 3)}.
    3. Cả hai vectơ đều có tọa độ thứ ba bằng tổng hai tọa độ đầu, nên mặt phẳng đó là z = x + y.
- `dstt_t8_nva_08` · bậc 4 (Nâng cao) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^3 -> R^2, f(x, y, z) = (x + y - z, 2x + 2y - 2z). Sắp xếp các bước tìm một cơ sở của Ker f.
  - **Đáp án (thứ tự đúng):**
    1. Ker f là tập nghiệm của hệ x + y - z = 0, 2x + 2y - 2z = 0.
    2. Phương trình thứ hai gấp đôi phương trình đầu, nên hệ chỉ còn x + y - z = 0.
    3. Chọn y, z làm ẩn tự do: x = -y + z.
    4. (x, y, z) = y(-1, 1, 0) + z(1, 0, 1), nên Ker f có cơ sở (-1, 1, 0), (1, 0, 1).
  - **Lời giải:**
    1. Viết điều kiện f(v) = 0 thành một hệ thuần nhất.
    2. Bỏ phương trình thừa, giải theo các ẩn tự do.
    3. Mỗi ẩn tự do cho một vectơ cơ sở: dim Ker f = 2.
- `dstt_t8_nva_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^4 -> R^3, f(v) = Av, với ma trận A như hình.
  - A = (1, 2, 0, 1); (0, 0, 1, 1); (1, 2, 1, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t5_htn_03`, `dstt_t8_nva_01`, `dstt_t8_nva_03`
  - **Phần a** (Điền số): a) Tìm dim Ker f.
    - **Đáp án a:** 2
  - **Phần b** (Trắc nghiệm): b) Vectơ nào sau đây thuộc Ker f?
    - **(đúng)** (-3, 1, -1, 1)
    - (1, 1, 1, 1)
    - (2, -1, 1, 0)
    - (0, 0, 1, -1)
    - **Đáp án b:** (-3, 1, -1, 1)
  - **Phần c** (Đúng/Sai): c) Trong tọa độ (x, y, z) của R^3, Im f là mặt phẳng z = x + y.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) Hàng 3 bằng hàng 1 cộng hàng 2, nên rank A = 2 và dim Ker f = 4 - 2 = 2. Ker f: x1 + 2x2 + x4 = 0, x3 + x4 = 0, cơ sở (-2, 1, 0, 0) và (-1, 0, -1, 1).
    2. b) (-3, 1, -1, 1) là tổng hai vectơ cơ sở đó: -3 + 2 + 1 = 0 và -1 + 1 = 0. Ba vectơ kia không thỏa một trong hai phương trình.
    3. c) Bốn cột (1, 0, 1), (2, 0, 2), (0, 1, 1), (1, 1, 2) đều có tọa độ thứ ba bằng tổng hai tọa độ đầu, và dim Im f = rank A = 2: Im f là mặt phẳng z = x + y. Đúng.
- `dstt_t8_nva_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f: V -> W là ánh xạ tuyến tính. Sắp xếp các bước chứng minh Ker f là một không gian con của V.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_01`, `dstt_t8_nva_01`
  - **Đáp án (thứ tự đúng):**
    1. Cần Ker f khác rỗng và đóng với hai phép toán. Trước hết, f(0) = f(0 . 0) = 0 . f(0) = 0, nên 0 thuộc Ker f.
    2. Tiếp theo, lấy u, v thuộc Ker f và một số k: f(u) = 0 và f(v) = 0.
    3. Vì f tuyến tính: f(u + v) = f(u) + f(v) = 0 và f(ku) = k f(u) = 0.
    4. Vậy u + v và ku thuộc Ker f, nên Ker f là không gian con của V.
  - **Lời giải:**
    1. Kiểm tra 0 thuộc Ker f nhờ tính tuyến tính.
    2. Lấy hai phần tử của Ker f, dùng hai điều kiện tuyến tính để thấy tổng và bội của chúng cũng có ảnh bằng 0.
    3. Kết luận theo tiêu chuẩn không gian con.
- `dstt_t8_nva_07` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm một cơ sở của Im f, với f(v) = Av và ma trận A như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 0, 1); (2, 1, 3); (1, 1, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_hang`, `dstt_t8_nva_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Im f được sinh bởi các cột của A: (1, 2, 1), (0, 1, 1), (1, 3, 2).
    2. Khử Gauss trên A: R2 - 2R1 và R3 - R1 cho các hàng (1, 0, 1), (0, 1, 1), (0, 1, 1); rồi R3 - R2 cho hàng 0.
    3. Trụ nằm ở cột 1 và cột 2, nên dim Im f = 2.
    4. Một cơ sở của Im f là hai hàng khác 0 của dạng bậc thang: (1, 0, 1) và (0, 1, 1).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Một cơ sở của Im f là hai hàng khác 0 của dạng bậc thang: (1, 0, 1) và (0, 1, 1).
  - **Vì sao sai, và bước đúng:**
    1. Biến đổi hàng làm thay đổi không gian cột, nên hàng của dạng bậc thang không nằm trong Im f nói chung: (1, 0, 1) không phải là tổ hợp của các cột của A.
    2. Đúng ra: trụ ở cột 1 và 2 cho biết lấy cột 1 và cột 2 của chính A.
    3. Một cơ sở của Im f là (1, 2, 1) và (0, 1, 1).

### Định lý số chiều (`dstt_t8_dinh_ly_so_chieu`)

- `dstt_t8_dlsc_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^5 -> R^3 là toàn ánh. Tìm dim Ker f.
  - **Đáp án:** 2
    1. f toàn ánh nên Im f = R^3, dim Im f = 3.
    2. Định lý số chiều: dim Ker f + dim Im f = dim R^5 = 5.
    3. dim Ker f = 5 - 3 = 2.
- `dstt_t8_dlsc_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Có một ánh xạ tuyến tính f: R^3 -> R^4 là toàn ánh.
  - **Đáp án:** Sai
    1. dim Im f = 3 - dim Ker f <= 3.
    2. Toàn ánh cần dim Im f = 4.
    3. Không thể, nên mệnh đề sai.
- `dstt_t8_dlsc_03` · bậc 4 (Nâng cao) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi ánh xạ tuyến tính f với kết luận đúng về nó.
  - **Đáp án (ghép đúng):**
    - f: R^4 -> R^4 có dim Ker f = 0 — Song ánh
    - f: R^3 -> R^5 có dim Ker f = 0 — Đơn ánh nhưng không toàn ánh
    - f: R^5 -> R^3 có dim Ker f = 2 — Toàn ánh nhưng không đơn ánh
    - f: R^4 -> R^3 có dim Ker f = 2 — Không đơn ánh và không toàn ánh
  - **Lời giải:**
    1. Đơn ánh khi dim Ker f = 0; toàn ánh khi dim Im f bằng số chiều không gian đích; dim Im f = dim nguồn - dim Ker f.
    2. R^4 -> R^4, Ker 0: Im có số chiều 4, song ánh. R^3 -> R^5, Ker 0: đơn ánh, Im chỉ có số chiều 3 < 5.
    3. R^5 -> R^3, Ker 2: Im có số chiều 3, toàn ánh nhưng không đơn ánh. R^4 -> R^3, Ker 2: Im có số chiều 2 < 3, không đơn ánh, không toàn ánh.
- `dstt_g8_so_chieu_nhan` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^4 -> R^4 cho bởi f(x) = Ax, với ma trận A như hình. Tìm dim Im f.
  - A = (0, 1, 1, -2); (0, 0, 0, 1); (-1, 1, 1, -5); (1, 1, 1, 1)  (từng hàng)
  - **Đáp án:** 3
    1. dim Im f bằng hạng của A (Im f được sinh bởi các cột của A).
    2. Khử Gauss: dạng bậc thang của A còn 3 hàng khác 0, nên rank A = 3 = dim Im f.
    3. Định lý số chiều: dim Ker f = 4 - 3 = 1.
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^4 -> R^3 cho bởi f(x) = Ax, với ma trận A như hình. Tìm dim Ker f.
  - A = (2, 0, -2, 0); (1, 0, -1, 0); (-1, 0, 1, 0)  (từng hàng)
  - **Đáp án:** 3
    1. dim Im f bằng hạng của A (Im f được sinh bởi các cột của A).
    2. Khử Gauss: dạng bậc thang của A còn 1 hàng khác 0, nên rank A = 1 = dim Im f.
    3. Định lý số chiều: dim Ker f = 4 - 1 = 3.
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^4 -> R^4 cho bởi f(x) = Ax, với ma trận A như hình. Tìm dim Ker f.
  - A = (0, 1, 1, -4); (0, 1, 3, -1); (0, 0, 0, 1); (0, 0, 1, 3)  (từng hàng)
  - **Đáp án:** 1
    1. dim Im f bằng hạng của A (Im f được sinh bởi các cột của A).
    2. Khử Gauss: dạng bậc thang của A còn 3 hàng khác 0, nên rank A = 3 = dim Im f.
    3. Định lý số chiều: dim Ker f = 4 - 3 = 1.
- `dstt_t8_dlsc_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f: R^3 -> R^3 là ánh xạ tuyến tính có ma trận chính tắc A với rank A = 2. Lời giải sau xét f. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_dlsc_02`, `dstt_g8_so_chieu_nhan`
  - **Lời giải đưa ra (có một bước sai):**
    1. dim Im f = rank A = 2.
    2. Theo định lý số chiều, dim Ker f = 3 - 2 = 1.
    3. Ker f khác {0}, nên f không đơn ánh.
    4. Một ánh xạ không đơn ánh vẫn có thể là toàn ánh, nên chưa kết luận được f có toàn ánh hay không.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Một ánh xạ không đơn ánh vẫn có thể là toàn ánh, nên chưa kết luận được f có toàn ánh hay không.
  - **Vì sao sai, và bước đúng:**
    1. Bước 4 bỏ qua điều đã có ở bước 1: dim Im f = 2 < 3 = dim R^3.
    2. Vậy Im f khác R^3 và f không toàn ánh.
    3. Với ánh xạ từ một không gian vào chính nó (số chiều hữu hạn), đơn ánh, toàn ánh và song ánh là một.
- `dstt_t8_dlsc_05` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^4 -> R^3, f(x, y, z, t) = (x + y, y + z, z + t).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_nva_01`, `dstt_t8_dlsc_01`, `dstt_g8_so_chieu_nhan`
  - **Phần a** (Điền số): a) Tìm dim Im f.
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Tìm dim Ker f.
    - **Đáp án b:** 1
  - **Phần c** (Điền số): c) Tìm vectơ của Ker f có tọa độ thứ hai bằng 1. Nhập bốn tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án c:** -1, 1, -1, 1
  - **Phần d** (Đúng/Sai): d) f là toàn ánh.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Ma trận chính tắc có hàng (1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1), đã ở dạng bậc thang với ba trụ: rank = 3 = dim Im f.
    2. b) Định lý số chiều: dim Ker f = 4 - 3 = 1.
    3. c) x + y = 0, y + z = 0, z + t = 0 với y = 1: x = -1, z = -1, t = 1. Vectơ (-1, 1, -1, 1).
    4. d) dim Im f = 3 = dim R^3, nên Im f = R^3: f toàn ánh. Đúng.
- `dstt_t8_dlsc_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f: V -> V là ánh xạ tuyến tính, dim V = n hữu hạn. Sắp xếp các bước chứng minh: nếu f đơn ánh thì f toàn ánh.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_dlsc_03`, `dstt_t8_dlsc_01`
  - **Đáp án (thứ tự đúng):**
    1. f đơn ánh nên Ker f = {0}, tức dim Ker f = 0.
    2. Theo định lý số chiều, dim Im f = n - dim Ker f = n.
    3. Im f là một không gian con của V có cùng số chiều n với V.
    4. Không gian con có số chiều bằng không gian chứa nó thì trùng với nó, nên Im f = V.
    5. Vậy f là toàn ánh.
  - **Lời giải:**
    1. Đơn ánh cho nhân tầm thường.
    2. Định lý số chiều cho dim Im f = n.
    3. Không gian con n chiều của không gian n chiều là toàn bộ không gian, nên f toàn ánh.

### Ma trận của ánh xạ tuyến tính (`dstt_t8_ma_tran_anh_xa`)

- `dstt_t8_mtax_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^2 -> R^3, f(x, y) = (2x - y, x + 3y, y). Tìm ma trận chính tắc của f (cỡ 3 x 2). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, -1, 1, 3, 0, 1
    1. Cột 1 là f(1, 0) = (2, 1, 0), cột 2 là f(0, 1) = (-1, 3, 1).
    2. Ma trận có hàng (2, -1), (1, 3), (0, 1).
    3. Thử lại: nhân ma trận đó với (x, y) được đúng (2x - y, x + 3y, y).
- `dstt_t8_mtax_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên không gian P_2 các đa thức bậc không quá 2, xét f(p) = p' (đạo hàm). Ma trận của f trong cơ sở 1, x, x^2 (cho bởi ba hàng) là ma trận nào?
    - **(đúng)** Hàng (0, 1, 0), (0, 0, 2), (0, 0, 0)
    - Hàng (0, 0, 0), (1, 0, 0), (0, 2, 0)
    - Hàng (1, 0, 0), (0, 2, 0), (0, 0, 0)
    - Hàng (0, 1, 0), (0, 0, 1), (0, 0, 0)
  - **Đáp án:** Hàng (0, 1, 0), (0, 0, 2), (0, 0, 0)
    1. Cột j là tọa độ của ảnh của vectơ cơ sở thứ j: f(1) = 0, f(x) = 1, f(x^2) = 2x.
    2. Tọa độ: (0, 0, 0), (1, 0, 0), (0, 2, 0); đặt làm ba cột.
    3. Các hàng là (0, 1, 0), (0, 0, 2), (0, 0, 0). Phương án thứ hai là ma trận chuyển vị (đặt ảnh làm hàng).
- `dstt_g8_ma_tran_co_so` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^3 -> R^2, f(x, y, z) = (-x + 2y - 2z, -2y + z), và cơ sở b1 = (1, 0, 0), b2 = (0, 1, 1), b3 = (-1, -1, 0) của R^3. Tìm ma trận của f đối với cơ sở đó của R^3 và cơ sở chính tắc của R^2 (cỡ 2 x 3). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** -1, 0, -1, 0, -1, 2
    1. Cột thứ j của ma trận là tọa độ của f(b_j) trong cơ sở đích; với cơ sở chính tắc của R^2, đó chính là f(b_j).
    2. f(b1) = (-1, 0), f(b2) = (0, -1), f(b3) = (-1, 2).
    3. Đặt ba vectơ đó thành ba cột: hàng 1 là (-1, 0, -1), hàng 2 là (0, -1, 2).
  - **Câu hỏi:** Cho f: R^3 -> R^2, f(x, y, z) = (-2x - 2y - 2z, -y + 3z), và cơ sở b1 = (1, 1, 0), b2 = (1, 2, 0), b3 = (-1, 0, 1) của R^3. Tìm ma trận của f đối với cơ sở đó của R^3 và cơ sở chính tắc của R^2 (cỡ 2 x 3). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** -4, -6, 0, -1, -2, 3
    1. Cột thứ j của ma trận là tọa độ của f(b_j) trong cơ sở đích; với cơ sở chính tắc của R^2, đó chính là f(b_j).
    2. f(b1) = (-4, -1), f(b2) = (-6, -2), f(b3) = (0, 3).
    3. Đặt ba vectơ đó thành ba cột: hàng 1 là (-4, -6, 0), hàng 2 là (-1, -2, 3).
  - **Câu hỏi:** Cho f: R^3 -> R^2, f(x, y, z) = (-x + 2y + 2z, -x + 2z), và cơ sở b1 = (1, 0, 1), b2 = (-1, 1, 0), b3 = (1, -1, 1) của R^3. Tìm ma trận của f đối với cơ sở đó của R^3 và cơ sở chính tắc của R^2 (cỡ 2 x 3). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** 1, 3, -1, 1, 1, 1
    1. Cột thứ j của ma trận là tọa độ của f(b_j) trong cơ sở đích; với cơ sở chính tắc của R^2, đó chính là f(b_j).
    2. f(b1) = (1, 1), f(b2) = (3, 1), f(b3) = (-1, 1).
    3. Đặt ba vectơ đó thành ba cột: hàng 1 là (1, 3, -1), hàng 2 là (1, 1, 1).
- `dstt_t8_mtax_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^2 -> R^2, f(x, y) = (x + y, 2y), và cơ sở B = {b1 = (1, 0), b2 = (1, 1)} (dùng B cho cả hai phía).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_td_02`, `dstt_t8_mtax_01`, `dstt_g8_ma_tran_co_so`
  - **Phần a** (Điền số): a) Tìm tọa độ của f(b2) trong cơ sở B. Nhập hai số, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 0, 2
  - **Phần b** (Điền số): b) Tìm ma trận của f trong cơ sở B. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 1, 0, 0, 2
  - **Phần c** (Đúng/Sai): c) Ma trận chính tắc của f cũng là ma trận chéo.
    - **Đáp án c:** Sai
  - **Lời giải:**
    1. a) f(b2) = f(1, 1) = (2, 2) = 0 b1 + 2 b2, tọa độ (0, 2).
    2. b) f(b1) = (1, 0) = 1 b1 + 0 b2, tọa độ (1, 0). Hai cột (1, 0) và (0, 2): ma trận chéo có hàng (1, 0), (0, 2).
    3. c) Ma trận chính tắc có cột f(1, 0) = (1, 0) và f(0, 1) = (1, 2): hàng (1, 1), (0, 2), không chéo. Sai.
- `dstt_t8_mtax_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f: R^2 -> R^2, f(x, y) = (3x - y, x + y). Lời giải sau lập ma trận của f trong cơ sở B = {b1 = (1, 1), b2 = (1, 2)} (dùng B cho cả hai phía). Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_td_02`, `dstt_g8_ma_tran_co_so`
  - **Lời giải đưa ra (có một bước sai):**
    1. f(b1) = f(1, 1) = (2, 2) và f(b2) = f(1, 2) = (1, 3).
    2. Cột 1 của ma trận cần tìm là f(b1) = (2, 2), cột 2 là f(b2) = (1, 3).   **<- bước sai đầu tiên**
    3. Vậy ma trận của f trong cơ sở B có hàng (2, 1) và (2, 3).
  - **Đáp án:** Bước 2: Cột 1 của ma trận cần tìm là f(b1) = (2, 2), cột 2 là f(b2) = (1, 3).
  - **Vì sao sai, và bước đúng:**
    1. Cột j phải là TỌA ĐỘ của f(b_j) trong cơ sở B, không phải chính f(b_j).
    2. f(b1) = (2, 2) = 2 b1 + 0 b2, tọa độ (2, 0); f(b2) = (1, 3) = -b1 + 2 b2, tọa độ (-1, 2).
    3. Ma trận đúng có hàng (2, -1) và (0, 2).
- `dstt_t8_mtax_05` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên không gian P_2 các đa thức bậc không quá 2, xét f(p)(x) = p(x + 1). Tìm ma trận của f trong cơ sở 1, x, x^2. Nhập chín phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_mtax_02`, `dstt_t8_mtax_01`
  - **Đáp án:** 1, 1, 1, 0, 1, 2, 0, 0, 1
    1. Ảnh các vectơ cơ sở: f(1) = 1, f(x) = x + 1, f(x^2) = (x + 1)^2 = 1 + 2x + x^2.
    2. Tọa độ trong 1, x, x^2: (1, 0, 0), (1, 1, 0), (1, 2, 1); đặt làm ba cột.
    3. Ma trận có hàng (1, 1, 1), (0, 1, 2), (0, 0, 1).

### Hợp ánh xạ và tích ma trận (`dstt_t8_hop_anh_xa`)

- `dstt_t8_hop_01` · bậc 4 (Nâng cao) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = (x + y, y) và g(x, y) = (2x, x - y), hai ánh xạ R^2 -> R^2. Tìm ma trận chính tắc của g o f (làm f trước). Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** 2, 2, 1, 0
    1. g(f(x, y)) = g(x + y, y) = (2x + 2y, (x + y) - y) = (2x + 2y, x).
    2. Ma trận chính tắc có hàng (2, 2) và (1, 0).
    3. Cũng là tích A_g A_f, với A_g có hàng (2, 0), (1, -1) và A_f có hàng (1, 1), (0, 1).
- `dstt_t8_hop_02` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi hai ánh xạ tuyến tính f, g: R^2 -> R^2 có ma trận chính tắc lần lượt là A và B, ánh xạ hợp g o f (làm f trước) có ma trận chính tắc AB.
  - **Đáp án:** Sai
    1. (g o f)(x) = g(f(x)) = B(Ax) = (BA)x: ma trận là BA, ma trận của ánh xạ làm sau đứng bên trái.
    2. BA và AB nói chung khác nhau, ví dụ A có hàng (1, 1), (0, 1) và B có hàng (1, 0), (1, 1).
    3. Mệnh đề sai.
- `dstt_t8_hop_03` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có ma trận chính tắc A với det A = 0. Điều nào chắc chắn đúng?
    - **(đúng)** f không phải là đẳng cấu
    - f là song ánh
    - f o f là đẳng cấu
    - Ker f = {0}
  - **Đáp án:** f không phải là đẳng cấu
    1. det A = 0 nên A không khả nghịch: f không có ánh xạ ngược, không là đẳng cấu.
    2. Ker f khác {0} (hệ Ax = 0 có nghiệm khác 0), nên f không đơn ánh, càng không song ánh.
    3. f o f có ma trận A^2 với det = 0, cũng không là đẳng cấu.
- `dstt_g8_hop` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho f(x, y) = (-2x + y, 3x + 3y) và g(x, y) = (3x - 3y, -x - 3y). Tìm ma trận chính tắc của f o g (làm g trước). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** -7, 3, 6, -18
    1. Ma trận chính tắc: A_f có hàng (-2, 1), (3, 3); A_g có hàng (3, -3), (-1, -3).
    2. Ánh xạ làm g trước có ma trận A_f A_g (ma trận của ánh xạ làm sau đứng bên trái).
    3. A_f A_g có hàng (-7, 3) và (6, -18).
  - **Câu hỏi:** Cho f(x, y) = (3x + 3y, -3x - 3y) và g(x, y) = (-3x - y, 3x - 2y). Tìm ma trận chính tắc của f o g (làm g trước). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, -9, 0, 9
    1. Ma trận chính tắc: A_f có hàng (3, 3), (-3, -3); A_g có hàng (-3, -1), (3, -2).
    2. Ánh xạ làm g trước có ma trận A_f A_g (ma trận của ánh xạ làm sau đứng bên trái).
    3. A_f A_g có hàng (0, -9) và (0, 9).
  - **Câu hỏi:** Cho f(x, y) = (-2x + y, x - 2y) và g(x, y) = (-x + y, 2y). Tìm ma trận chính tắc của g o f (làm f trước). Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - **Đáp án:** 3, -3, 2, -4
    1. Ma trận chính tắc: A_f có hàng (-2, 1), (1, -2); A_g có hàng (-1, 1), (0, 2).
    2. Ánh xạ làm f trước có ma trận A_g A_f (ma trận của ánh xạ làm sau đứng bên trái).
    3. A_g A_f có hàng (3, -3) và (2, -4).
- `dstt_t8_hop_04` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho hai ánh xạ R^2 -> R^2: f(x, y) = (x + 2y, y) và g(x, y) = (x, 3x + y), với ma trận chính tắc A_f, A_g.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g4_tich_2x2`, `dstt_t8_hop_01`, `dstt_t6_nd_03`
  - **Phần a** (Điền số): a) Tìm ma trận chính tắc của g o f (làm f trước). Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 1, 2, 3, 7
  - **Phần b** (Điền số): b) Tìm ma trận chính tắc của f o g (làm g trước). Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 7, 2, 3, 1
  - **Phần c** (Đúng/Sai): c) g o f là đẳng cấu, và ánh xạ ngược của nó có ma trận chính tắc (A_f)^(-1) (A_g)^(-1).
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) g(f(x, y)) = g(x + 2y, y) = (x + 2y, 3x + 7y): hàng (1, 2), (3, 7). Đây là A_g A_f.
    2. b) f(g(x, y)) = f(x, 3x + y) = (7x + 2y, 3x + y): hàng (7, 2), (3, 1). Khác câu a.
    3. c) det(A_g A_f) = 7 - 6 = 1 khác 0 nên g o f là đẳng cấu, và (g o f)^(-1) = f^(-1) o g^(-1) có ma trận (A_g A_f)^(-1) = (A_f)^(-1) (A_g)^(-1). Đúng.
- `dstt_t8_hop_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm ánh xạ ngược của f: R^2 -> R^2, f(x, y) = (2x + y, x + y). Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_nghich_dao_2`, `dstt_t8_hop_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận chính tắc A của f có hàng (2, 1) và (1, 1); det A = 1 khác 0 nên f là đẳng cấu.
    2. Ma trận của f^(-1) là A^T, có hàng (2, 1) và (1, 1).   **<- bước sai đầu tiên**
    3. Vậy f^(-1)(x, y) = (2x + y, x + y), tức f^(-1) = f.
  - **Đáp án:** Bước 2: Ma trận của f^(-1) là A^T, có hàng (2, 1) và (1, 1).
  - **Vì sao sai, và bước đúng:**
    1. Ma trận của f^(-1) là A^(-1), không phải A^T (hai cái chỉ trùng nhau khi A trực giao).
    2. A^(-1) = (1/1) . hàng (1, -1), (-1, 2), nên f^(-1)(x, y) = (x - y, -x + 2y).
    3. Thử lại: f(1, -1) = (1, 0), đúng với f^(-1)(1, 0) = (1, -1).

### Đổi cơ sở và ma trận đồng dạng (`dstt_t8_doi_co_so`)

- `dstt_t8_dcs_01` · bậc 4 (Nâng cao) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu hai ma trận vuông A và B đồng dạng (B = P^(-1) A P với P khả nghịch) thì det B = det A và tr B = tr A.
  - **Đáp án:** Đúng
    1. det B = det(P^(-1)) det A det P = det A, vì det(P^(-1)) det P = 1.
    2. tr(XY) = tr(YX), nên tr(P^(-1)(AP)) = tr((AP)P^(-1)) = tr A.
    3. Mệnh đề đúng: định thức và vết không phụ thuộc cơ sở.
- `dstt_t8_dcs_02` · bậc 4 (Nâng cao) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^n -> R^n có ma trận chính tắc A. P là ma trận có các cột là các vectơ của một cơ sở mới B. Ma trận của f trong cơ sở B là ma trận nào?
    - **(đúng)** P^(-1) A P
    - P A P^(-1)
    - P^T A P
    - A P
  - **Đáp án:** P^(-1) A P
    1. P đổi tọa độ trong B sang tọa độ chính tắc: v = P [v]_B.
    2. Lấy [v]_B, đổi sang chính tắc (nhân P), tác động f (nhân A), đổi về B (nhân P^(-1)).
    3. Vậy ma trận trong B là P^(-1) A P.
- `dstt_g8_doi_co_so` · bậc 4 (Nâng cao) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới b1 = (2, 1), b2 = (1, 1) là hai cột của P. Tìm ma trận B của f trong cơ sở b1, b2. Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-2, 1); (-2, 4)  (từng hàng)
  - P = (2, 1); (1, 1)  (từng hàng)
  - **Đáp án:** -3, -3, 3, 5
    1. B = P^(-1) A P.
    2. det P = 1, nên P^(-1) có hàng (1, -1) và (-1, 2).
    3. AP có hàng (-3, -1) và (0, 2).
    4. B = P^(-1)(AP) có hàng (-3, -3) và (3, 5).
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới b1 = (1, 1), b2 = (1, 0) là hai cột của P. Tìm ma trận B của f trong cơ sở b1, b2. Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (2, -1); (1, 1)  (từng hàng)
  - P = (1, 1); (1, 0)  (từng hàng)
  - **Đáp án:** 2, 1, -1, 1
    1. B = P^(-1) A P.
    2. det P = -1, nên P^(-1) có hàng (0, 1) và (1, -1).
    3. AP có hàng (1, 2) và (2, 1).
    4. B = P^(-1)(AP) có hàng (2, 1) và (-1, 1).
  - **Câu hỏi:** Ánh xạ tuyến tính f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới b1 = (3, 2), b2 = (2, 1) là hai cột của P. Tìm ma trận B của f trong cơ sở b1, b2. Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy.
  - A = (-1, 4); (0, 1)  (từng hàng)
  - P = (3, 2); (2, 1)  (từng hàng)
  - **Đáp án:** -1, 0, 4, 1
    1. B = P^(-1) A P.
    2. det P = -1, nên P^(-1) có hàng (-1, 2) và (2, -3).
    3. AP có hàng (5, 2) và (2, 1).
    4. B = P^(-1)(AP) có hàng (-1, 0) và (4, 1).
- `dstt_t8_dcs_03` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới b1 = (1, 1), b2 = (2, 1) là hai cột của P như hình.
  - A = (4, -2); (1, 1)  (từng hàng)
  - P = (1, 2); (1, 1)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_nghich_dao_2`, `dstt_t8_dcs_02`, `dstt_g8_doi_co_so`
  - **Phần a** (Điền số): a) Tính A b1. Nhập hai tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 2, 2
  - **Phần b** (Điền số): b) Tìm B = P^(-1) A P. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 2, 0, 0, 3
  - **Phần c** (Đúng/Sai): c) det B = det A.
    - **Đáp án c:** Đúng
  - **Lời giải:**
    1. a) A b1 = (4 - 2, 1 + 1) = (2, 2) = 2 b1.
    2. b) A b2 = (8 - 2, 2 + 1) = (6, 3) = 3 b2. Trong cơ sở b1, b2: f(b1) có tọa độ (2, 0), f(b2) có tọa độ (0, 3), nên B có hàng (2, 0), (0, 3). Kiểm tra bằng P^(-1) có hàng (-1, 2), (1, -1).
    3. c) det A = 4 + 2 = 6 = 2 . 3 = det B. Đúng (hai ma trận đồng dạng).
- `dstt_t8_dcs_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tính ma trận B = P^(-1) A P của f trong cơ sở mới, với A, P như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (0, 3)  (từng hàng)
  - P = (1, 1); (0, 1)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t8_dcs_02`, `dstt_t6_nd_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. det P = 1, nên P^(-1) có hàng (1, -1) và (0, 1).
    2. AP có hàng (1, 3) và (0, 3).
    3. B = (AP) P^(-1): nhân AP với P^(-1) được hàng (1, 2) và (0, 3).   **<- bước sai đầu tiên**
    4. Vậy B = A: đổi cơ sở không làm ma trận thay đổi.
  - **Đáp án:** Bước 3: B = (AP) P^(-1): nhân AP với P^(-1) được hàng (1, 2) và (0, 3).
  - **Vì sao sai, và bước đúng:**
    1. Bước 3 nhân sai thứ tự: B = P^(-1)(AP), P^(-1) đứng bên trái.
    2. P^(-1)(AP) có hàng (1 - 0, 3 - 3) = (1, 0) và (0, 3).
    3. B có hàng (1, 0), (0, 3): trong cơ sở mới, ma trận của f là ma trận chéo.

## Tầng 9: Giá trị riêng, không gian Euclide và dạng toàn phương

36 dạng câu (30 câu viết tay, 6 bộ sinh câu); 36 chưa duyệt.

### Giá trị riêng và vectơ riêng (`dstt_t9_tri_rieng`)

- `dstt_t9_tr_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Giá trị riêng được ký hiệu là t, đa thức đặc trưng p(t) = det(A - tI).
  - A = (4, 1); (2, 3)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_tim_x_det`, `dstt_t5_htn_03`, `dstt_t8_nva_01`
  - **Phần a** (Điền số): a) p(t) = t^2 + bt + c. Nhập b rồi c, cách nhau bằng dấu phẩy.
    - **Đáp án a:** -7, 10
  - **Phần b** (Điền số): b) Nhập các giá trị riêng của A, theo thứ tự bất kỳ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 2, 5  (thứ tự nào cũng được)
  - **Phần c** (Điền số): c) Vectơ riêng ứng với giá trị riêng lớn hơn có dạng (1, y). Tìm y.
    - **Đáp án c:** 1
  - **Lời giải:**
    1. a) p(t) = (4 - t)(3 - t) - 2 . 1 = t^2 - 7t + 10, nên b = -7, c = 10.
    2. b) t^2 - 7t + 10 = (t - 2)(t - 5): giá trị riêng 2 và 5.
    3. c) Với t = 5: A - 5I có hàng (-1, 1), (2, -2); phương trình -x + y = 0 cho y = x, vectơ riêng (1, 1). Thử lại A(1, 1) = (5, 5).
- `dstt_t9_tr_02` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm giá trị riêng và vectơ riêng của ma trận A như hình. Bước đầu tiên bị sai là bước nào?
  - A = (1, 2); (3, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_dt_03`, `dstt_t5_htn_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Giá trị riêng là các số t làm A - tI không khả nghịch, tức det(A - tI) = 0.
    2. det(A - tI) = (1 - t)(2 - t) - 2 . 3 = t^2 - 3t - 4.
    3. t^2 - 3t - 4 = (t - 4)(t + 1), nên giá trị riêng là 4 và -1.
    4. Với t = -1: (A + I)x = 0 cho 2x + 2y = 0, nên một vectơ riêng là (1, 1).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Với t = -1: (A + I)x = 0 cho 2x + 2y = 0, nên một vectơ riêng là (1, 1).
  - **Vì sao sai, và bước đúng:**
    1. Phương trình 2x + 2y = 0 cho y = -x, nên (1, 1) không thỏa: 2 + 2 = 4 khác 0.
    2. Vectơ riêng ứng với -1 là (1, -1): A(1, -1) = (1 - 2, 3 - 2) = (-1, 1) = -1 . (1, -1).
    3. Ba bước đầu đúng.
- `dstt_t9_tr_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi ma trận vuông khả nghịch A: nếu t là một giá trị riêng của A thì t khác 0 và 1/t là một giá trị riêng của A^(-1).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_tcd_04`
  - **Đáp án:** Đúng
    1. Nếu t = 0 thì Av = 0 với v khác 0, trái với A khả nghịch; vậy t khác 0.
    2. Từ Av = tv, nhân A^(-1) vào hai vế: v = t A^(-1) v, nên A^(-1) v = (1/t) v.
    3. v khác 0 nên 1/t là giá trị riêng của A^(-1). Mệnh đề đúng.
- `dstt_t9_tr_04` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A cấp 3 có ba giá trị riêng 1, 2 và -3. Tính det(A^2 + I).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_vet_04`, `dstt_t6_tcd_04`
  - **Đáp án:** 100
    1. Nếu Av = tv thì (A^2 + I)v = (t^2 + 1)v: giá trị riêng của A^2 + I là t^2 + 1.
    2. Với t = 1, 2, -3 được 2, 5, 10 (A cấp 3 có đúng ba giá trị riêng này nên A^2 + I có đúng ba giá trị riêng 2, 5, 10).
    3. Định thức bằng tích các giá trị riêng: 2 . 5 . 10 = 100.
- `dstt_t9_tr_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh: hai vectơ riêng u, v của A ứng với hai giá trị riêng khác nhau a, b thì độc lập tuyến tính.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_dltt_02`, `dstt_t5_htn_03`
  - **Đáp án (thứ tự đúng):**
    1. Có Au = au, Av = bv với u, v khác 0 và a khác b; giả sử c1 u + c2 v = 0.
    2. Nhân A vào hai vế: c1 a u + c2 b v = 0.
    3. Lấy đẳng thức này trừ a lần đẳng thức c1 u + c2 v = 0: c2 (b - a) v = 0.
    4. Vì b - a khác 0 và v khác 0 nên c2 = 0.
    5. Khi đó c1 u = 0 mà u khác 0, nên c1 = 0: u, v độc lập tuyến tính.
  - **Lời giải:**
    1. Viết một tổ hợp bằng 0, nhân A vào để có đẳng thức thứ hai.
    2. Khử u giữa hai đẳng thức, còn lại c2 (b - a) v = 0, nên c2 = 0.
    3. Rồi c1 = 0.
- `dstt_t9_tr_06` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A cấp 2 có tr A = 5 và det A = 6. Các giá trị riêng của A^2 - A là gì?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_vet_04`, `dstt_g6_tim_x_det`
    - **(đúng)** 2 và 6
    - 4 và 9
    - 1 và 2
    - 2 và 3
  - **Đáp án:** 2 và 6
    1. Giá trị riêng của A là nghiệm của t^2 - 5t + 6 = 0, tức 2 và 3.
    2. Nếu Av = tv thì (A^2 - A)v = (t^2 - t)v.
    3. Với t = 2 và t = 3: 4 - 2 = 2 và 9 - 3 = 6.
- `dstt_g9_tri_rieng` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình có ba giá trị riêng khác nhau, đều là số nguyên. Tìm chúng. Nhập ba giá trị riêng, cách nhau bằng dấu phẩy, theo thứ tự bất kỳ.
  - A = (4, 1, 1); (-3, 0, -1); (3, 3, 4)  (từng hàng)
  - **Đáp án:** 1, 3, 4  (thứ tự nào cũng được)
    1. Giá trị riêng là nghiệm của đa thức đặc trưng p(t) = det(A - tI), một đa thức bậc 3.
    2. Kiểm tra nhanh: tổng ba giá trị riêng bằng vết tr A = 8, tích bằng det A = 12.
    3. Nghiệm nguyên của p(t) là ước của hệ số tự do det A: thử các ước đó, rồi chia đa thức.
    4. Ba giá trị riêng: 1, 3, 4.
  - **Câu hỏi:** Ma trận A như hình có ba giá trị riêng khác nhau, đều là số nguyên. Tìm chúng. Nhập ba giá trị riêng, cách nhau bằng dấu phẩy, theo thứ tự bất kỳ.
  - A = (-4, 2, 7); (-3, 1, 3); (-2, 2, 5)  (từng hàng)
  - **Đáp án:** -2, 1, 3  (thứ tự nào cũng được)
    1. Giá trị riêng là nghiệm của đa thức đặc trưng p(t) = det(A - tI), một đa thức bậc 3.
    2. Kiểm tra nhanh: tổng ba giá trị riêng bằng vết tr A = 2, tích bằng det A = -6.
    3. Nghiệm nguyên của p(t) là ước của hệ số tự do det A: thử các ước đó, rồi chia đa thức.
    4. Ba giá trị riêng: -2, 1, 3.
  - **Câu hỏi:** Ma trận A như hình có ba giá trị riêng khác nhau, đều là số nguyên. Tìm chúng. Nhập ba giá trị riêng, cách nhau bằng dấu phẩy, theo thứ tự bất kỳ.
  - A = (-5, -4, 2); (10, 8, -3); (-4, -2, 3)  (từng hàng)
  - **Đáp án:** 1, 2, 3  (thứ tự nào cũng được)
    1. Giá trị riêng là nghiệm của đa thức đặc trưng p(t) = det(A - tI), một đa thức bậc 3.
    2. Kiểm tra nhanh: tổng ba giá trị riêng bằng vết tr A = 6, tích bằng det A = 6.
    3. Nghiệm nguyên của p(t) là ước của hệ số tự do det A: thử các ước đó, rồi chia đa thức.
    4. Ba giá trị riêng: 1, 2, 3.

### Chéo hóa ma trận (`dstt_t9_cheo_hoa`)

- `dstt_t9_ch_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chéo hóa ma trận A như hình: tìm P khả nghịch và D chéo với A = P D P^(-1).
  - A = (5, -2); (4, -1)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_nghich_dao_2`, `dstt_t8_dcs_01`, `dstt_g8_doi_co_so`
  - **Phần a** (Điền số): a) Nhập các giá trị riêng của A, theo thứ tự bất kỳ, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 1, 3  (thứ tự nào cũng được)
  - **Phần b** (Trắc nghiệm): b) D có đường chéo 1 rồi 3. Ma trận P nào (cho bởi hai cột) thỏa A = P D P^(-1)?
    - **(đúng)** Cột (1, 2) rồi cột (1, 1)
    - Cột (1, 1) rồi cột (1, 2)
    - Cột (2, 1) rồi cột (1, 1)
    - Cột (1, 2) rồi cột (1, -1)
    - **Đáp án b:** Cột (1, 2) rồi cột (1, 1)
  - **Phần c** (Điền số): c) Dùng A^5 = P D^5 P^(-1), tính phần tử ở hàng 1, cột 1 của A^5.
    - **Đáp án c:** 485
  - **Lời giải:**
    1. a) p(t) = (5 - t)(-1 - t) + 8 = t^2 - 4t + 3 = (t - 1)(t - 3): giá trị riêng 1 và 3.
    2. b) t = 1: A - I có hàng (4, -2), (4, -2), nên 2x = y, vectơ riêng (1, 2). t = 3: A - 3I có hàng (2, -2), (4, -4), vectơ riêng (1, 1). Cột của P theo thứ tự của D: (1, 2) rồi (1, 1).
    3. c) P^(-1) có hàng (-1, 1), (2, -1); D^5 có đường chéo 1, 243. Phần tử (1, 1) của P D^5 P^(-1) = 1 . 1 . (-1) + 1 . 243 . 2 = 485.
- `dstt_t9_ch_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình chéo hóa được trên R.
  - A = (2, 1); (0, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_hang`, `dstt_g8_so_chieu_nhan`
  - **Đáp án:** Sai
    1. A tam giác nên giá trị riêng duy nhất là 2, bội 2.
    2. A - 2I có hàng (0, 1), (0, 0), hạng 1: không gian riêng chỉ có số chiều 2 - 1 = 1.
    3. Không đủ hai vectơ riêng độc lập, nên A không chéo hóa được. Mệnh đề sai.
- `dstt_t9_ch_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau xét ma trận A như hình có chéo hóa được không. Bước đầu tiên bị sai là bước nào?
  - A = (1, 1, 0); (0, 1, 0); (0, 0, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_hang`, `dstt_g8_so_chieu_nhan`
  - **Lời giải đưa ra (có một bước sai):**
    1. A tam giác trên nên giá trị riêng là 1 (bội 2) và 2 (bội 1).
    2. Với t = 1: A - I có hàng (0, 1, 0), (0, 0, 0), (0, 0, 1), hạng 2.
    3. Không gian riêng ứng với t = 1 có số chiều 3 - 2 = 1.
    4. Tổng số chiều các không gian riêng là 1 + 1 = 2, nên A chéo hóa được.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 4: Tổng số chiều các không gian riêng là 1 + 1 = 2, nên A chéo hóa được.
  - **Vì sao sai, và bước đúng:**
    1. Chéo hóa được cần tổng số chiều các không gian riêng bằng cấp của ma trận, ở đây là 3.
    2. Tổng chỉ là 2 < 3 (không gian riêng của t = 1 có số chiều 1, nhỏ hơn bội 2).
    3. Vậy A không chéo hóa được.
- `dstt_t9_ch_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi ma trận vuông cấp n có n giá trị riêng thực khác nhau đều chéo hóa được trên R.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_dltt_02`, `dstt_t8_dcs_02`
  - **Đáp án:** Đúng
    1. Mỗi giá trị riêng cho ít nhất một vectơ riêng.
    2. Các vectơ riêng ứng với các giá trị riêng khác nhau thì độc lập tuyến tính, nên có n vectơ riêng độc lập.
    3. Đặt chúng làm các cột của P thì P^(-1) A P chéo. Mệnh đề đúng.
- `dstt_t9_ch_05` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi ma trận cấp 2 bên trái cho bởi hàng 1 rồi hàng 2. Ghép mỗi ma trận với điều đúng về nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g6_tim_x_det`, `dstt_g8_so_chieu_nhan`
  - **Đáp án (ghép đúng):**
    - (1, 0), (0, 2) — Đã là ma trận chéo
    - (1, 1), (0, 1) — Có giá trị riêng thực nhưng không chéo hóa được
    - (0, -1), (1, 0) — Không có giá trị riêng thực
    - (1, 2), (0, 3) — Chéo hóa được nhưng chưa phải ma trận chéo
  - **Lời giải:**
    1. (1, 0), (0, 2) đã chéo.
    2. (1, 1), (0, 1): giá trị riêng 1 bội 2 nhưng không gian riêng chỉ một chiều. (1, 2), (0, 3): hai giá trị riêng khác nhau 1 và 3, chéo hóa được.
    3. (0, -1), (1, 0): p(t) = t^2 + 1 vô nghiệm thực (phép quay 90 độ).
- `dstt_g9_cheo_hoa` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận A như hình chéo hóa được trên R (có P khả nghịch, thực, và D chéo với A = P D P^(-1)).
  - A = (-3, 1); (-2, 0)  (từng hàng)
  - **Đáp án:** Đúng
    1. p(t) = t^2 - (-3)t + 2, có hai nghiệm thực phân biệt -2 và -1.
    2. Ma trận cấp 2 có hai giá trị riêng thực phân biệt thì có hai vectơ riêng độc lập.
    3. Vậy A chéo hóa được trên R: mệnh đề đúng.
  - **Câu hỏi:** Ma trận A như hình chéo hóa được trên R (có P khả nghịch, thực, và D chéo với A = P D P^(-1)).
  - A = (2, 1); (-1, 0)  (từng hàng)
  - **Đáp án:** Sai
    1. p(t) = (t - 1)^2: giá trị riêng duy nhất 1, bội 2.
    2. A - (1)I khác ma trận không nên có hạng 1; không gian riêng chỉ có số chiều 1.
    3. Không đủ hai vectơ riêng độc lập: A không chéo hóa được, mệnh đề sai.
  - **Câu hỏi:** Ma trận A như hình chéo hóa được trên R (có P khả nghịch, thực, và D chéo với A = P D P^(-1)).
  - A = (-2, 3); (-6, 7)  (từng hàng)
  - **Đáp án:** Đúng
    1. p(t) = t^2 - 5t + 4, có hai nghiệm thực phân biệt 1 và 4.
    2. Ma trận cấp 2 có hai giá trị riêng thực phân biệt thì có hai vectơ riêng độc lập.
    3. Vậy A chéo hóa được trên R: mệnh đề đúng.
- `dstt_g9_luy_thua` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A như hình. Chéo hóa A rồi tính phần tử ở hàng 2, cột 2 của A^3.
  - A = (0, 2); (-1, -3)  (từng hàng)
  - **Đáp án:** -15
    1. p(t) = det(A - tI) có hai nghiệm -2 và -1; giải (A - tI)x = 0 cho mỗi giá trị được hai vectơ riêng, đặt làm hai cột của P: P có hàng (1, 2), (-1, -1).
    2. A = P D P^(-1) với D chéo (-2, -1), P^(-1) có hàng (-1, -2), (1, 1).
    3. A^3 = P D^3 P^(-1), với D^3 chéo (-8, -1).
    4. A^3 có hàng (6, 14) và (-7, -15); phần tử cần tìm là -15.
  - **Câu hỏi:** Cho ma trận A như hình. Chéo hóa A rồi tính phần tử ở hàng 2, cột 2 của A^4.
  - A = (4, 6); (-3, -5)  (từng hàng)
  - **Đáp án:** 31
    1. p(t) = det(A - tI) có hai nghiệm -2 và 1; giải (A - tI)x = 0 cho mỗi giá trị được hai vectơ riêng, đặt làm hai cột của P: P có hàng (1, 2), (-1, -1).
    2. A = P D P^(-1) với D chéo (-2, 1), P^(-1) có hàng (-1, -2), (1, 1).
    3. A^4 = P D^4 P^(-1), với D^4 chéo (16, 1).
    4. A^4 có hàng (-14, -30) và (15, 31); phần tử cần tìm là 31.
  - **Câu hỏi:** Cho ma trận A như hình. Chéo hóa A rồi tính phần tử ở hàng 1, cột 1 của A^6.
  - A = (5, 6); (-3, -4)  (từng hàng)
  - **Đáp án:** 127
    1. p(t) = det(A - tI) có hai nghiệm -1 và 2; giải (A - tI)x = 0 cho mỗi giá trị được hai vectơ riêng, đặt làm hai cột của P: P có hàng (1, 2), (-1, -1).
    2. A = P D P^(-1) với D chéo (-1, 2), P^(-1) có hàng (-1, -2), (1, 1).
    3. A^6 = P D^6 P^(-1), với D^6 chéo (1, 64).
    4. A^6 có hàng (127, 126) và (-63, -62); phần tử cần tìm là 127.

### Không gian Euclide và trực giao hóa (`dstt_t9_khong_gian_euclide`)

- `dstt_t9_kge_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trực giao hóa Gram-Schmidt (không chuẩn hóa) u1 = (1, 1, 0), u2 = (1, 0, 1), u3 = (0, 1, 1) với tích vô hướng thông thường: v1 = u1, rồi v2, rồi v3.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_csc_02`
  - **Phần a** (Điền số): a) Tính hệ số u2 . v1 / (v1 . v1).
    - **Đáp án a:** 1/2
  - **Phần b** (Điền số): b) Tìm v2. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 1/2, -1/2, 1
  - **Phần c** (Điền số): c) Tìm v3. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án c:** -2/3, 2/3, 2/3
  - **Phần d** (Đúng/Sai): d) v1, v2, v3 đôi một vuông góc.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) u2 . v1 = 1 và v1 . v1 = 2: hệ số 1/2.
    2. b) v2 = u2 - (1/2) v1 = (1, 0, 1) - (1/2, 1/2, 0) = (1/2, -1/2, 1).
    3. c) u3 . v1 = 1, u3 . v2 = 1/2, v2 . v2 = 3/2. v3 = u3 - (1/2) v1 - (1/3) v2 = (0, 1, 1) - (1/2, 1/2, 0) - (1/6, -1/6, 1/3) = (-2/3, 2/3, 2/3).
    4. d) v1 . v2 = 0, v1 . v3 = 0, v2 . v3 = -1/3 - 1/3 + 2/3 = 0. Đúng.
- `dstt_t9_kge_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm a, b để w = (1, a, b) vuông góc với cả u = (1, 1, 1) và v = (1, 2, 3), rồi tính ||w||^2. Nhập a, b, ||w||^2, cách nhau bằng dấu phẩy.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t5_htn_03`
  - **Đáp án:** -2, 1, 6
    1. w . u = 1 + a + b = 0 và w . v = 1 + 2a + 3b = 0.
    2. Từ phương trình đầu a = -1 - b; thế vào: 1 - 2 - 2b + 3b = 0, nên b = 1 và a = -2.
    3. w = (1, -2, 1), ||w||^2 = 1 + 4 + 1 = 6.
- `dstt_t9_kge_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau trực giao hóa Gram-Schmidt u1 = (1, 2), u2 = (3, 1) trong R^2 (không chuẩn hóa). Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_04`, `dstt_t7_td_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. v1 = u1 = (1, 2).
    2. u2 . v1 = 3 + 2 = 5 và ||v1|| = căn(5).
    3. v2 = u2 - (u2 . v1 / ||v1||) v1 = (3, 1) - căn(5) . (1, 2).   **<- bước sai đầu tiên**
    4. Vậy v2 = (3 - căn(5), 1 - 2căn(5)).
  - **Đáp án:** Bước 3: v2 = u2 - (u2 . v1 / ||v1||) v1 = (3, 1) - căn(5) . (1, 2).
  - **Vì sao sai, và bước đúng:**
    1. Hệ số chiếu chia cho ||v1||^2 = v1 . v1 = 5, không phải cho ||v1||.
    2. v2 = (3, 1) - (5/5)(1, 2) = (2, -1).
    3. Thử lại: v2 . v1 = 2 - 2 = 0.
- `dstt_t9_kge_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^n với tích vô hướng thông thường, với mọi hai vectơ u, v vuông góc với nhau ta có ||u + v|| = ||u|| + ||v||.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t6_tcd_02`
  - **Đáp án:** Sai
    1. Với u, v vuông góc, định lý Pythagore cho ||u + v||^2 = ||u||^2 + ||v||^2 (bình phương, không phải độ dài).
    2. Phản ví dụ: u = (1, 0), v = (0, 1): ||u + v|| = căn(2), còn ||u|| + ||v|| = 2.
    3. Mệnh đề sai (chỉ đúng khi một trong hai vectơ bằng 0).
- `dstt_t9_kge_05` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước chứng minh bất đẳng thức Cauchy-Schwarz |u . v| <= ||u|| ||v|| trong R^n.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_kgv_01`
  - **Đáp án (thứ tự đúng):**
    1. Nếu v = 0 thì hai vế đều bằng 0; xét v khác 0.
    2. Với mọi số thực s: 0 <= ||u - sv||^2 = ||u||^2 - 2s(u . v) + s^2 ||v||^2.
    3. Vế phải là một tam thức bậc hai theo s, không âm với mọi s.
    4. Nên biệt thức của nó không dương: 4(u . v)^2 - 4||u||^2 ||v||^2 <= 0.
    5. Lấy căn hai vế: |u . v| <= ||u|| ||v||.
  - **Lời giải:**
    1. Loại trường hợp v = 0.
    2. Khai triển ||u - sv||^2 >= 0 thành một tam thức bậc hai theo s.
    3. Tam thức không âm với mọi s nên biệt thức <= 0, đó chính là bất đẳng thức cần chứng minh.
- `dstt_g9_gram_schmidt` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trực giao hóa Gram-Schmidt (không chuẩn hóa) ba vectơ u1 = (-1, 2, -1), u2 = (2, 2, -1), u3 = (2, 1, 0) của R^3, với tích vô hướng thông thường: v1 = u1, rồi v2, rồi v3. Nhập ba tọa độ của v3 (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** 0, 1/5, 2/5
    1. v1 = u1 = (-1, 2, -1).
    2. v2 = u2 - (u2 . v1 / v1 . v1) v1 = u2 - (1/2) v1 = (5/2, 1, -1/2).
    3. v3 = u3 - (u3 . v1 / v1 . v1) v1 - (u3 . v2 / v2 . v2) v2, với hai hệ số 0 và 4/5.
    4. v3 = (0, 1/5, 2/5); thử lại v3 . v1 = 0 và v3 . v2 = 0.
  - **Câu hỏi:** Trực giao hóa Gram-Schmidt (không chuẩn hóa) ba vectơ u1 = (0, 2, 2), u2 = (1, 2, 1), u3 = (-1, -1, 1) của R^3, với tích vô hướng thông thường: v1 = u1, rồi v2, rồi v3. Nhập ba tọa độ của v3 (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** 1/3, -1/3, 1/3
    1. v1 = u1 = (0, 2, 2).
    2. v2 = u2 - (u2 . v1 / v1 . v1) v1 = u2 - (3/4) v1 = (1, 1/2, -1/2).
    3. v3 = u3 - (u3 . v1 / v1 . v1) v1 - (u3 . v2 / v2 . v2) v2, với hai hệ số 0 và -4/3.
    4. v3 = (1/3, -1/3, 1/3); thử lại v3 . v1 = 0 và v3 . v2 = 0.
  - **Câu hỏi:** Trực giao hóa Gram-Schmidt (không chuẩn hóa) ba vectơ u1 = (0, 0, 1), u2 = (2, -1, -1), u3 = (2, 1, 0) của R^3, với tích vô hướng thông thường: v1 = u1, rồi v2, rồi v3. Nhập ba tọa độ của v3 (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** 4/5, 8/5, 0
    1. v1 = u1 = (0, 0, 1).
    2. v2 = u2 - (u2 . v1 / v1 . v1) v1 = u2 - (-1) v1 = (2, -1, 0).
    3. v3 = u3 - (u3 . v1 / v1 . v1) v1 - (u3 . v2 / v2 . v2) v2, với hai hệ số 0 và 3/5.
    4. v3 = (4/5, 8/5, 0); thử lại v3 . v1 = 0 và v3 . v2 = 0.

### Dạng toàn phương (`dstt_t9_dang_toan_phuong`)

- `dstt_t9_dtp_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét dạng toàn phương q(x, y) = 2x^2 + 2xy + 2y^2 trên R^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g3_doi_xung_dien`, `dstt_t8_dcs_02`, `dstt_g8_doi_co_so`
  - **Phần a** (Điền số): a) Tìm ma trận đối xứng A với q(v) = v^T A v. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 2, 1, 1, 2
  - **Phần b** (Điền số): b) Nhập các giá trị riêng của A, theo thứ tự bất kỳ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 1, 3  (thứ tự nào cũng được)
  - **Phần c** (Trắc nghiệm): c) Qua một phép đổi biến trực giao, q có dạng chính tắc nào?
    - **(đúng)** X^2 + 3Y^2
    - 2X^2 + 2Y^2
    - X^2 - 3Y^2
    - 2X^2 + Y^2
    - **Đáp án c:** X^2 + 3Y^2
  - **Phần d** (Đúng/Sai): d) q xác định dương.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Hệ số của xy là 2, chia đôi đặt vào hai ô ngoài đường chéo: A có hàng (2, 1), (1, 2).
    2. b) p(t) = (2 - t)^2 - 1 = (t - 1)(t - 3): giá trị riêng 1 và 3.
    3. c) Đổi sang cơ sở trực chuẩn gồm vectơ riêng, q = 1 . X^2 + 3 . Y^2.
    4. d) Cả hai giá trị riêng dương, nên q(v) > 0 với mọi v khác 0: xác định dương. Đúng.
- `dstt_t9_dtp_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với m là tham số thực, dạng toàn phương q(x, y) = x^2 + 4xy + m y^2 xác định dương khi nào? Nhập số nguyên m nhỏ nhất làm q xác định dương.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g3_doi_xung_dien`, `dstt_g6_tim_x_det`
  - **Đáp án:** 5
    1. Ma trận đối xứng của q có hàng (1, 2), (2, m).
    2. Tiêu chuẩn Sylvester: D1 = 1 > 0 và D2 = m - 4 > 0, tức m > 4.
    3. Số nguyên nhỏ nhất lớn hơn 4 là 5.
- `dstt_t9_dtp_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau xét dấu dạng toàn phương q(x, y, z) = x^2 + 2y^2 + z^2 + 2xy + 4yz. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g3_doi_xung_dien`, `dstt_t6_dt_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Ma trận đối xứng của q có hàng (1, 2, 0), (2, 2, 4), (0, 4, 1).   **<- bước sai đầu tiên**
    2. D1 = 1 > 0 nhưng D2 = 1 . 2 - 2 . 2 = -2 < 0.
    3. Vậy q không xác định dương.
  - **Đáp án:** Bước 1: Ma trận đối xứng của q có hàng (1, 2, 0), (2, 2, 4), (0, 4, 1).
  - **Vì sao sai, và bước đúng:**
    1. Hệ số của xy và yz phải chia đôi trước khi đặt vào hai ô đối xứng.
    2. Ma trận đúng có hàng (1, 1, 0), (1, 2, 2), (0, 2, 1): D1 = 1, D2 = 1, D3 = -3.
    3. D3 < 0 nên q vẫn không xác định dương, nhưng kết luận phải đến từ ma trận đúng.
- `dstt_t9_dtp_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng toàn phương q(x, y) = x^2 - 4xy + y^2 trên R^2 xác định dương.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g3_doi_xung_dien`, `dstt_g6_tim_x_det`
  - **Đáp án:** Sai
    1. Ma trận đối xứng có hàng (1, -2), (-2, 1); D1 = 1 > 0 nhưng D2 = 1 - 4 = -3 < 0.
    2. Thật vậy q(1, 1) = 1 - 4 + 1 = -2 < 0.
    3. q không xác định dương (nó không xác định dấu). Mệnh đề sai.
- `dstt_t9_dtp_05` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dạng toàn phương q(x, y) trên R^2 với loại của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_dcs_01`
  - **Đáp án (ghép đúng):**
    - x^2 + y^2 — Xác định dương
    - -x^2 - 2y^2 — Xác định âm
    - x^2 - y^2 — Không xác định dấu
    - x^2 + 2xy + y^2 — Nửa xác định dương nhưng không xác định dương
  - **Lời giải:**
    1. x^2 + y^2 > 0 khi (x, y) khác 0; -x^2 - 2y^2 < 0 khi (x, y) khác 0.
    2. x^2 - y^2 nhận cả giá trị dương (1, 0) và âm (0, 1).
    3. x^2 + 2xy + y^2 = (x + y)^2 >= 0 nhưng bằng 0 tại (1, -1) khác 0; ma trận có giá trị riêng 2 và 0.
- `dstt_g9_xac_dinh` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dạng toàn phương q(x, y, z) = 2x^2 + 4y^2 + 4z^2 - 4xy - 4yz trên R^3 xác định dương.
  - **Đáp án:** Đúng
    1. Ma trận đối xứng của q có hàng (2, -2, 0), (-2, 4, -2), (0, -2, 4) (hệ số của xy, xz, yz chia đôi).
    2. Các định thức con chính: D1 = 2, D2 = 4, D3 = 8.
    3. Cả ba đều dương: theo tiêu chuẩn Sylvester, q xác định dương. Mệnh đề đúng.
  - **Câu hỏi:** Dạng toàn phương q(x, y, z) = -x^2 - y^2 - z^2 - 2xy + 6xz - 4yz trên R^3 xác định dương.
  - **Đáp án:** Sai
    1. Ma trận đối xứng của q có hàng (-1, -1, 3), (-1, -1, -2), (3, -2, -1) (hệ số của xy, xz, yz chia đôi).
    2. Các định thức con chính: D1 = -1, D2 = 0, D3 = 25.
    3. D1 = -1 không dương, nên theo tiêu chuẩn Sylvester q không xác định dương. Mệnh đề sai.
  - **Câu hỏi:** Dạng toàn phương q(x, y, z) = 2x^2 + 3y^2 + 3z^2 + 4xy - 4xz - 4yz trên R^3 xác định dương.
  - **Đáp án:** Đúng
    1. Ma trận đối xứng của q có hàng (2, 2, -2), (2, 3, -2), (-2, -2, 3) (hệ số của xy, xz, yz chia đôi).
    2. Các định thức con chính: D1 = 2, D2 = 2, D3 = 2.
    3. Cả ba đều dương: theo tiêu chuẩn Sylvester, q xác định dương. Mệnh đề đúng.

### Phép chiếu trực giao (`dstt_t9_phep_chieu`)

- `dstt_t9_pc_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chiếu vuông góc b = (2, 3, 4) lên đường thẳng span{a} với a = (1, 1, 1) trong R^3.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_kgc_01`
  - **Phần a** (Điền số): a) Tính hệ số (a . b) / (a . a).
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Tìm hình chiếu p. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 3, 3, 3
  - **Phần c** (Điền số): c) Tìm phần dư r = b - p. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
    - **Đáp án c:** -1, 0, 1
  - **Phần d** (Đúng/Sai): d) r vuông góc với a.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) a . b = 2 + 3 + 4 = 9, a . a = 3: hệ số 3.
    2. b) p = 3a = (3, 3, 3).
    3. c) r = (2, 3, 4) - (3, 3, 3) = (-1, 0, 1).
    4. d) r . a = -1 + 0 + 1 = 0. Đúng: phần dư luôn vuông góc với đường thẳng được chiếu lên.
- `dstt_t9_pc_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tìm hình chiếu vuông góc của b = (1, 2, 6) lên mặt phẳng W = {(x, y, z) : x + y + z = 0} của R^3. Nhập ba tọa độ, cách nhau bằng dấu phẩy.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_kgc_04`
  - **Đáp án:** -2, -1, 3
    1. W có vectơ pháp tuyến n = (1, 1, 1); phần dư b - p nằm dọc theo n.
    2. b - p = (b . n / n . n) n = (9/3) n = (3, 3, 3).
    3. p = (1, 2, 6) - (3, 3, 3) = (-2, -1, 3); thử lại -2 - 1 + 3 = 0.
- `dstt_t9_pc_03` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Lời giải sau tìm hình chiếu vuông góc của b = (1, 2, 3) lên W = span{a1, a2} trong R^3. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_csc_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. W = span{a1, a2} với a1 = (1, 0, 0) và a2 = (1, 1, 0).
    2. Chiếu b lên từng vectơ: (b . a1 / a1 . a1) a1 = (1, 0, 0) và (b . a2 / a2 . a2) a2 = (3/2, 3/2, 0).
    3. Hình chiếu lên W là tổng hai hình chiếu đó: (5/2, 3/2, 0).   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Hình chiếu lên W là tổng hai hình chiếu đó: (5/2, 3/2, 0).
  - **Vì sao sai, và bước đúng:**
    1. Cộng các hình chiếu lên từng vectơ chỉ đúng khi các vectơ đó đôi một vuông góc; ở đây a1 . a2 = 1 khác 0.
    2. W chính là mặt phẳng z = 0 (trực giao hóa: a2 - a1 = (0, 1, 0)), nên hình chiếu là (1, 2, 0).
    3. Thử lại: b - (1, 2, 0) = (0, 0, 3) vuông góc với a1 và a2, còn b - (5/2, 3/2, 0) thì không.
- `dstt_t9_pc_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^n với tích vô hướng thông thường, nếu p là hình chiếu vuông góc của b lên một không gian con W thì ||p|| <= ||b||.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_t7_kgc_01`
  - **Đáp án:** Đúng
    1. b = p + r với r = b - p vuông góc với W, nên vuông góc với p.
    2. Pythagore: ||b||^2 = ||p||^2 + ||r||^2 >= ||p||^2.
    3. Vậy ||p|| <= ||b||. Mệnh đề đúng.
- `dstt_t9_pc_05` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ma trận P của phép chiếu vuông góc lên đường thẳng span{a} trong R^2, với a = (1, 2), là ma trận nào? (Mỗi ma trận cho bởi hàng 1 rồi hàng 2.)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tvh_03`, `dstt_g4_tich_2x2`, `dstt_t7_td_02`
    - **(đúng)** (1/5) nhân ma trận hàng (1, 2), (2, 4)
    - Ma trận hàng (1, 2), (2, 4)
    - (1/5) nhân ma trận hàng (4, -2), (-2, 1)
    - (1/căn(5)) nhân ma trận hàng (1, 2), (2, 4)
  - **Đáp án:** (1/5) nhân ma trận hàng (1, 2), (2, 4)
    1. Hình chiếu của b là (a . b / a . a) a = a (a^T b) / (a^T a), nên P = a a^T / (a^T a).
    2. a a^T có hàng (1, 2), (2, 4) và a^T a = 5.
    3. P = (1/5) . hàng (1, 2), (2, 4). Thử lại P^2 = P và P a = a. Ma trận thứ ba là phép chiếu lên đường vuông góc với a.
- `dstt_g9_chieu` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong R^3 với tích vô hướng thông thường, cho W = span{a1, a2} với a1 = (2, 0, -1), a2 = (2, -1, -2), và b = (0, 0, 2). Tìm hình chiếu trực giao p của b lên W. Nhập ba tọa độ (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** -4/9, 8/9, 10/9
    1. W là một mặt phẳng qua gốc; một vectơ pháp tuyến của nó là n = (-1, 2, -2) (vuông góc với cả a1 và a2).
    2. Phần dư b - p nằm dọc theo n: b - p = (b . n / n . n) n = (-4/9) n.
    3. p = b - (-4/9) n = (-4/9, 8/9, 10/9); thử lại p . n = 0.
  - **Câu hỏi:** Trong R^3 với tích vô hướng thông thường, cho W = span{a1, a2} với a1 = (1, 0, -1), a2 = (0, -1, 1), và b = (2, 3, -1). Tìm hình chiếu trực giao p của b lên W. Nhập ba tọa độ (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** 2/3, 5/3, -7/3
    1. W là một mặt phẳng qua gốc; một vectơ pháp tuyến của nó là n = (-1, -1, -1) (vuông góc với cả a1 và a2).
    2. Phần dư b - p nằm dọc theo n: b - p = (b . n / n . n) n = (-4/3) n.
    3. p = b - (-4/3) n = (2/3, 5/3, -7/3); thử lại p . n = 0.
  - **Câu hỏi:** Trong R^3 với tích vô hướng thông thường, cho W = span{a1, a2} với a1 = (0, 1, -1), a2 = (-2, 0, -1), và b = (0, 2, 1). Tìm hình chiếu trực giao p của b lên W. Nhập ba tọa độ (phân số viết a/b), cách nhau bằng dấu phẩy.
  - **Đáp án:** 2/3, 2/3, -1/3
    1. W là một mặt phẳng qua gốc; một vectơ pháp tuyến của nó là n = (-1, 2, 2) (vuông góc với cả a1 và a2).
    2. Phần dư b - p nằm dọc theo n: b - p = (b . n / n . n) n = (6/9) n.
    3. p = b - (2/3) n = (2/3, 2/3, -1/3); thử lại p . n = 0.

### Làm quen PCA và SVD (`dstt_t9_pca_svd`)

- `dstt_t9_pca_01` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Bốn điểm dữ liệu (2, 1), (-2, -1), (1, 2), (-1, -2) đã có trung bình bằng 0; X là ma trận dữ liệu như hình, mỗi hàng một điểm. Phân tích thành phần chính (PCA) dùng S = X^T X.
  - X = (2, 1); (-2, -1); (1, 2); (-1, -2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_g4_tich_2x2`, `dstt_g6_tim_x_det`, `dstt_t8_dcs_02`
  - **Phần a** (Điền số): a) Tính S = X^T X. Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy.
    - **Đáp án a:** 10, 8, 8, 10
  - **Phần b** (Điền số): b) Nhập các giá trị riêng của S, theo thứ tự bất kỳ, cách nhau bằng dấu phẩy.
    - **Đáp án b:** 2, 18  (thứ tự nào cũng được)
  - **Phần c** (Trắc nghiệm): c) Hướng của thành phần chính thứ nhất là hướng của vectơ nào?
    - **(đúng)** (1, 1)
    - (1, -1)
    - (1, 0)
    - (0, 1)
    - **Đáp án c:** (1, 1)
  - **Phần d** (Điền số): d) Giữ lại chỉ thành phần chính thứ nhất thì giữ được bao nhiêu phần của tổng phương sai? Nhập một phân số a/b.
    - **Đáp án d:** 9/10
  - **Lời giải:**
    1. a) Tổng bình phương hoành độ 4 + 4 + 1 + 1 = 10, tung độ cũng 10, tổng tích 2 + 2 + 2 + 2 = 8: S có hàng (10, 8), (8, 10).
    2. b) p(t) = (10 - t)^2 - 64 = (t - 2)(t - 18): giá trị riêng 18 và 2.
    3. c) Với t = 18: S - 18I có hàng (-8, 8), (8, -8), vectơ riêng (1, 1): dữ liệu trải dài nhất theo đường y = x.
    4. d) Phần giữ lại là 18 / (18 + 2) = 9/10.
- `dstt_t9_pca_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Cho ma trận A cỡ 3 x 2 như hình. Tính A^T A, rồi nhập các giá trị kỳ dị của A từ lớn đến bé, cách nhau bằng dấu phẩy.
  - A = (1, 4); (2, -4); (2, 2)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_nm_03`, `dstt_g6_tim_x_det`
  - **Đáp án:** 6, 3
    1. Giá trị kỳ dị của A là căn bậc hai của các giá trị riêng của A^T A.
    2. Hai cột (1, 2, 2) và (4, -4, 2) vuông góc (4 - 8 + 4 = 0), có bình phương độ dài 9 và 36: A^T A có hàng (9, 0), (0, 36).
    3. Giá trị riêng 36 và 9, nên giá trị kỳ dị là 6 và 3.
- `dstt_t9_pca_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với mọi ma trận thực A, mọi giá trị riêng của A^T A đều là số thực không âm, nên các giá trị kỳ dị của A là các số thực không âm.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_kt_04`, `dstt_t8_dcs_01`
  - **Đáp án:** Đúng
    1. A^T A đối xứng nên có các giá trị riêng thực.
    2. Nếu A^T A v = t v với v khác 0 thì t ||v||^2 = v^T A^T A v = ||Av||^2 >= 0, nên t >= 0.
    3. Giá trị kỳ dị là căn bậc hai của các t đó, nên thực và không âm. Mệnh đề đúng.
- `dstt_t9_pca_04` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước giảm số chiều của một bảng dữ liệu X (mỗi hàng một điểm, n điểm) bằng PCA.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_nm_03`, `dstt_t8_dcs_02`
  - **Đáp án (thứ tự đúng):**
    1. Trừ mỗi cột cho trung bình của cột đó để dữ liệu có tâm ở gốc.
    2. Lập ma trận hiệp phương sai C = X^T X / n từ dữ liệu đã trừ trung bình.
    3. Tìm các giá trị riêng và vectơ riêng của C.
    4. Sắp xếp giá trị riêng từ lớn đến bé và giữ k vectơ riêng đầu tiên.
    5. Chiếu mỗi điểm dữ liệu lên không gian sinh bởi k vectơ riêng đó.
  - **Lời giải:**
    1. Trừ trung bình trước, nếu không ma trận hiệp phương sai sai.
    2. Lập C rồi tìm giá trị riêng, vectơ riêng của nó.
    3. Giữ các hướng có phương sai lớn nhất (giá trị riêng lớn nhất) rồi chiếu dữ liệu lên các hướng đó.

## Tầng 10: Tài Năng: cấu trúc đại số và dạng song tuyến tính

58 dạng câu (48 câu viết tay, 10 bộ sinh câu); 58 chưa duyệt.

### Quan hệ hai ngôi (`dstt_t10_quan_he`)

- `dstt_t10_qh_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên tập A = {1, 2, ..., 12} xét quan hệ a ~ b khi a - b chia hết cho 5. Quan hệ này là quan hệ tương đương. Lớp tương đương của số 3 có bao nhiêu phần tử? Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Đáp án:** 2
    1. Lớp của 3 gồm mọi b trong A có 3 - b chia hết cho 5, tức b có cùng số dư 3 khi chia cho 5.
    2. Trong 1..12 các số đó là 3 và 8 (13 đã vượt quá 12; và 3 - 5 = -2 không thuộc A). Vậy lớp có 2 phần tử.
    3. Đếm theo số dư: số dư 1, 2 cho ba số (1, 6, 11 và 2, 7, 12), số dư 3 và 4 cho hai số, số dư 0 cho hai số (5, 10); tổng 3 + 3 + 2 + 2 + 2 = 12.
- `dstt_t10_qh_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Quan hệ a <= b trên tập các số thực R là một quan hệ tương đương.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Đáp án:** Sai
    1. Quan hệ tương đương phải phản xạ, đối xứng và bắc cầu. Quan hệ <= phản xạ và bắc cầu, nhưng không đối xứng: 1 <= 2 mà 2 <= 1 sai.
    2. Nó là quan hệ thứ tự (phản xạ, phản đối xứng, bắc cầu), và thứ tự toàn phần vì hai số thực bất kỳ đều so sánh được. Mệnh đề sai.
- `dstt_t10_qh_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên tập A = {1, 2, 3, 4, 5, 6} xét quan hệ a R b khi a chia hết b (a là ước của b). Quan hệ R là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgv_01`
    - **(đúng)** quan hệ thứ tự bộ phận: phản xạ, phản đối xứng, bắc cầu, nhưng không đối xứng và không toàn phần
    - quan hệ tương đương
    - quan hệ thứ tự toàn phần: hai phần tử bất kỳ đều so sánh được
    - chỉ phản xạ, không bắc cầu
  - **Đáp án:** quan hệ thứ tự bộ phận: phản xạ, phản đối xứng, bắc cầu, nhưng không đối xứng và không toàn phần
    1. Phản xạ (a chia hết a); phản đối xứng (a | b và b | a thì a = b); bắc cầu (a | b và b | c thì a | c). Không toàn phần: 2 và 3 không so sánh được (2 không chia hết 3 và 3 không chia hết 2).
    2. Quan hệ tương đương phải đối xứng: 1 | 2 nhưng 2 không chia hết 1, nên R không đối xứng.
    3. Quan hệ thứ tự toàn phần đòi hỏi mọi cặp so sánh được, nhưng (2, 3) và (4, 6) không so sánh được.
    4. Chỉ phản xạ, không bắc cầu là sai: R có bắc cầu, vì nếu a | b và b | c thì c = b k = a m k, nên a | c.
- `dstt_t10_qh_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Trên R xét quan hệ x R y khi |x - y| < 1. Hỏi R có phải quan hệ tương đương không. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Lời giải đưa ra (có một bước sai):**
    1. Phản xạ: |x - x| = 0 < 1 nên x R x.
    2. Đối xứng: |x - y| = |y - x| nên x R y kéo theo y R x.
    3. Bắc cầu: |x - y| < 1 và |y - z| < 1, cộng lại được |x - z| < 1 nên x R z.   **<- bước sai đầu tiên**
    4. Vậy R là quan hệ tương đương.
  - **Đáp án:** Bước 3: Bắc cầu: |x - y| < 1 và |y - z| < 1, cộng lại được |x - z| < 1 nên x R z.
  - **Vì sao sai, và bước đúng:**
    1. Cộng hai bất đẳng thức cho |x - y| + |y - z| < 2, và |x - z| <= |x - y| + |y - z| chỉ cho |x - z| < 2, không phải < 1.
    2. Phản ví dụ: x = 0, y = 3/5, z = 6/5. Khi đó 0 R 3/5 và 3/5 R 6/5 nhưng |0 - 6/5| = 6/5 > 1, nên 0 và 6/5 không có quan hệ R: R không bắc cầu, không phải quan hệ tương đương.
- `dstt_t10_qh_05` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi quan hệ với loại của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Đáp án (ghép đúng):**
    - a ~ b khi a - b chia hết cho 3, trên Z — Quan hệ tương đương
    - a <= b, trên R — Quan hệ thứ tự toàn phần
    - a | b (a chia hết b), trên các số nguyên dương — Quan hệ thứ tự bộ phận, không toàn phần
    - a R b khi a khác b, trên R — Đối xứng nhưng không phản xạ và không bắc cầu
  - **Lời giải:**
    1. a - b chia hết cho 3: phản xạ, đối xứng, bắc cầu (lớp là ba số dư 0, 1, 2).
    2. <= và | phản xạ, phản đối xứng, bắc cầu; <= so sánh được mọi cặp, | thì không (2 và 3).
    3. a khác b: đối xứng; không phản xạ vì a khác a sai; không bắc cầu vì 1 R 2 và 2 R 1 mà 1 R 1 sai.
- `dstt_t10_qh_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên Z xét a R b khi a - b chia hết cho 3. Sắp xếp các bước chứng minh R có tính bắc cầu.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Đáp án (thứ tự đúng):**
    1. Giả sử a R b và b R c, tức a - b = 3k và b - c = 3m với k, m nguyên.
    2. Cộng hai đẳng thức: (a - b) + (b - c) = 3k + 3m.
    3. Vế trái rút gọn thành a - c, vế phải là 3(k + m).
    4. k + m là số nguyên nên a - c chia hết cho 3, tức a R c.
  - **Lời giải:**
    1. Một chứng minh bắc cầu luôn đi từ giả thiết (hai quan hệ nối tiếp) đến kết luận (quan hệ giữa hai đầu).
    2. Chỉ cần k, m nguyên: tổng của hai số nguyên vẫn là số nguyên.
- `dstt_t10_qh_07` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên A = {1, 2, 3} cho quan hệ R gồm các cặp (1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3), (3, 2).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Phần a** (Đúng/Sai): a) R có tính phản xạ.
    - **Đáp án a:** Đúng
  - **Phần b** (Đúng/Sai): b) R có tính đối xứng.
    - **Đáp án b:** Đúng
  - **Phần c** (Đúng/Sai): c) R có tính bắc cầu.
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Cần thêm ít nhất bao nhiêu cặp vào R để được một quan hệ tương đương?
    - **Đáp án d:** 2
  - **Lời giải:**
    1. a) Có đủ (1, 1), (2, 2), (3, 3).
    2. b) Mỗi cặp có cặp đảo: (1, 2) và (2, 1), (2, 3) và (3, 2).
    3. c) 1 R 2 và 2 R 3 nhưng (1, 3) không có trong R: không bắc cầu.
    4. d) Thêm (1, 3) thì để đối xứng phải thêm (3, 1); khi đó R là toàn bộ A x A (9 cặp), là quan hệ tương đương với một lớp. Cần thêm đúng 2 cặp; không thể ít hơn vì thiếu (1, 3) thì mất bắc cầu.
- `dstt_t10_qh_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Một quan hệ trên A = {1, 2, 3} là một tập con của A x A, tập có 9 cặp.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Phần a** (Điền số): a) Có bao nhiêu quan hệ phản xạ trên A?
    - **Đáp án a:** 64
  - **Phần b** (Điền số): b) Có bao nhiêu quan hệ đối xứng trên A?
    - **Đáp án b:** 64
  - **Phần c** (Điền số): c) Có bao nhiêu quan hệ tương đương trên A?
    - **Đáp án c:** 5
  - **Phần d** (Đúng/Sai): d) Số quan hệ tương đương trên A bằng số cách chia A thành các tập con khác rỗng, đôi một rời nhau.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) Ba cặp (1, 1), (2, 2), (3, 3) bắt buộc phải có; sáu cặp còn lại tuỳ ý: 2^6 = 64.
    2. b) Ba cặp trên đường chéo tuỳ ý (2^3) và ba cặp không thứ tự {1, 2}, {1, 3}, {2, 3} mỗi cặp hoặc có cả hai chiều hoặc không có (2^3): 2^3 . 2^3 = 64.
    3. c) Mỗi quan hệ tương đương ứng với một phân hoạch của A: một lớp {1, 2, 3}; hai lớp (ba cách chọn phần tử đứng riêng); ba lớp {1}, {2}, {3}. Tổng 1 + 3 + 1 = 5 (đếm vét cạn trên mọi 512 quan hệ cũng được 5).
    4. d) Đúng, đó chính là tương ứng giữa quan hệ tương đương và phân hoạch.
- `dstt_t10_qh_09` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mỗi quan hệ tương đương trên một tập A chia A thành các lớp tương đương đôi một rời nhau có hợp là A; ngược lại, mỗi cách chia A thành các tập con khác rỗng đôi một rời nhau cho một quan hệ tương đương (hai phần tử tương đương khi cùng một tập).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t7_kgc_02`
  - **Đáp án:** Đúng
    1. Hai lớp tương đương hoặc trùng nhau hoặc rời nhau (nếu có phần tử chung thì nhờ đối xứng và bắc cầu hai lớp trùng nhau), và mỗi phần tử thuộc lớp của chính nó nhờ phản xạ.
    2. Ngược lại "cùng một tập con" là phản xạ, đối xứng và bắc cầu. Mệnh đề đúng.
- `dstt_g10_quan_he_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trên A = {1, 2, 3, 4} cho quan hệ R gồm các cặp (1, 3), (2, 2), (2, 4), (3, 1), (3, 3), (4, 4). R là một quan hệ tương đương.
  - **Đáp án:** Sai
    1. Thiếu cặp (1, 1): không phản xạ.
    2. Có cặp (2, 4) nhưng thiếu cặp đảo (4, 2): không đối xứng.
    3. (1, 3) và (3, 1) thuộc R (b = c = 3) nhưng (1, 1) không thuộc R: không bắc cầu.
    4. Quan hệ tương đương đòi hỏi cả ba tính chất: có tính chất không thoả, mệnh đề sai.
  - **Câu hỏi:** Trên A = {1, 2, 3, 4} cho quan hệ R gồm các cặp (1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (2, 4), (3, 3), (4, 2), (4, 4). R có tính chất đối xứng.
  - **Đáp án:** Sai
    1. Có cặp (1, 4) nhưng thiếu cặp đảo (4, 1): không đối xứng.
    2. Mệnh đề sai.
  - **Câu hỏi:** Trên A = {1, 2, 3, 4} cho quan hệ R gồm các cặp (1, 1), (1, 4), (2, 2), (2, 3), (3, 2), (3, 3), (4, 1), (4, 4). R là một quan hệ tương đương.
  - **Đáp án:** Đúng
    1. Mọi cặp (a, a) đều có trong R: phản xạ.
    2. Mỗi cặp (a, b) đều đi với cặp đảo (b, a): đối xứng.
    3. Mỗi khi (a, b) và (b, c) cùng thuộc R thì (a, c) cũng thuộc R: bắc cầu.
    4. Quan hệ tương đương đòi hỏi cả ba tính chất: cả ba đều có, mệnh đề đúng.
- `dstt_g10_so_lop` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trên tập A = {1, 2, ..., 8} xét quan hệ a ~ b khi a - b chia hết cho 4. Đây là một quan hệ tương đương. Có bao nhiêu lớp tương đương? Nhập một số.
  - **Đáp án:** 4
    1. Hai số cùng lớp khi cùng số dư trong phép chia cho 4; các số dư có thể là 0, 1, ..., 3.
    2. Với A = 1..8 (ít nhất 4 số liên tiếp) mọi số dư đều xuất hiện: có 4 lớp.
  - **Câu hỏi:** Trên tập A = {1, 2, ..., 7} xét quan hệ a ~ b khi a - b chia hết cho 3. Đây là một quan hệ tương đương. Lớp tương đương của số 1 có bao nhiêu phần tử? Nhập một số.
  - **Đáp án:** 3
    1. Lớp của 1 gồm mọi b trong A có cùng số dư với 1 khi chia cho 3 (số dư 1): 1, 4, 7.
    2. Có 3 phần tử.
  - **Câu hỏi:** Trên tập A = {1, 2, ..., 10} xét quan hệ a ~ b khi a - b chia hết cho 4. Đây là một quan hệ tương đương. Có bao nhiêu cặp có thứ tự (a, b) thuộc A x A mà a ~ b? Nhập một số.
  - **Đáp án:** 26
    1. Mỗi lớp có k phần tử cho k . k cặp (a, b) cùng lớp (cả a = b và hai chiều). Kích thước các lớp: 3, 3, 2, 2.
    2. Tổng bình phương kích thước: 3^2 + 3^2 + 2^2 + 2^2 = 26.

### Phép toán hai ngôi (`dstt_t10_phep_toan_hai_ngoi`)

- `dstt_t10_pt_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b - 3. Tìm phần tử trung hoà e, tức số e có a * e = e * a = a với mọi a. Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t7_kgv_02`
  - **Đáp án:** 3
    1. a * e = a + e - 3 = a suy ra e - 3 = 0, tức e = 3: a bị triệt tiêu hai vế nên e không phụ thuộc a.
    2. Phép toán giao hoán nên e * a = a * e = a cũng đúng. Kiểm tra: a * 3 = a + 3 - 3 = a.
- `dstt_t10_pt_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b + ab, có phần tử trung hoà là 0. Tìm phần tử ngược của số 2, tức số b có 2 * b = 0. Nhập một số hoặc phân số tối giản.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_03`
  - **Đáp án:** -2/3
    1. 2 * b = 2 + b + 2b = 2 + 3b. Đặt bằng phần tử trung hoà 0: 2 + 3b = 0.
    2. b = -2/3. Kiểm tra: 2 * (-2/3) = 2 - 2/3 - 4/3 = 0. Phần tử ngược của một phần tử phải đem về phần tử trung hoà của chính phép toán (0 ở đây), không phải về 1.
- `dstt_t10_pt_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Phép toán a * b = a + 2b trên R có tính giao hoán và có tính kết hợp.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t7_kgv_01`
  - **Đáp án:** Sai
    1. Không giao hoán: 1 * 0 = 1 nhưng 0 * 1 = 2.
    2. Không kết hợp: (a * b) * c = a + 2b + 2c còn a * (b * c) = a + 2b + 4c, khác nhau khi c khác 0. Mệnh đề sai (cả hai vế đều sai).
- `dstt_t10_pt_04` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét phép toán a * b = a - b trên tập các số nguyên Z. Khẳng định đúng là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t7_kgv_02`
    - **(đúng)** Phép toán không giao hoán, không kết hợp; số 0 chỉ là trung hoà bên phải (a * 0 = a) chứ không bên trái
    - Phép toán kết hợp vì phép cộng kết hợp
    - Số 0 là phần tử trung hoà hai phía
    - Phép toán giao hoán vì |a - b| = |b - a|
  - **Đáp án:** Phép toán không giao hoán, không kết hợp; số 0 chỉ là trung hoà bên phải (a * 0 = a) chứ không bên trái
    1. a * b = a - b và b * a = b - a khác nhau (3 * 1 = 2, 1 * 3 = -2). (a * b) * c = a - b - c còn a * (b * c) = a - (b - c) = a - b + c: khác khi c khác 0. a * 0 = a nhưng 0 * a = -a.
    2. Phép trừ không kết hợp: (5 - 3) - 1 = 1 nhưng 5 - (3 - 1) = 3; tính kết hợp của phép cộng không chuyển sang phép trừ.
    3. 0 * a = 0 - a = -a khác a (trừ a = 0), nên 0 không trung hoà bên trái.
    4. Giá trị tuyệt đối đối xứng nhưng a - b thì không: 3 - 1 khác 1 - 3.
- `dstt_t10_pt_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Trên R xét phép toán a * b = (a + b)/2 (trung bình cộng). Xét tính kết hợp. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t6_nd_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. (a * b) * c = ((a + b)/2 + c)/2 = (a + b + 2c)/4.
    2. a * (b * c) = (a + (b + c)/2)/2 = (2a + b + c)/4.
    3. Hai kết quả cùng có a, b, c nhân với các hệ số cộng lại bằng nhau, nên (a * b) * c = a * (b * c).   **<- bước sai đầu tiên**
    4. Vậy phép toán * có tính kết hợp.
  - **Đáp án:** Bước 3: Hai kết quả cùng có a, b, c nhân với các hệ số cộng lại bằng nhau, nên (a * b) * c = a * (b * c).
  - **Vì sao sai, và bước đúng:**
    1. Hai biểu thức (a + b + 2c)/4 và (2a + b + c)/4 chỉ bằng nhau khi a = c: các hệ số của a (1/4 và 1/2) và của c (1/2 và 1/4) khác nhau.
    2. Phản ví dụ: a = 1, b = 3, c = 7. (1 * 3) * 7 = 2 * 7 = 9/2 nhưng 1 * (3 * 7) = 1 * 5 = 3. Phép toán không kết hợp.
- `dstt_t10_pt_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi phép toán với đặc điểm của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t7_kgv_01`
  - **Đáp án (ghép đúng):**
    - a * b = a + b trên R — Trung hoà 0, mỗi số a có phần tử ngược -a
    - a * b = a . b (nhân thường) trên R — Trung hoà 1, số 0 không có phần tử ngược
    - a * b = a + b + ab trên R — Trung hoà 0, số -1 không có phần tử ngược
    - a * b = max(a, b) trên các số tự nhiên N (có 0) — Trung hoà 0, chỉ số 0 có phần tử ngược
  - **Lời giải:**
    1. a + b + ab: a * 0 = a; phần tử ngược của a là -a/(1 + a), không tồn tại khi a = -1.
    2. max(a, b) = 0 chỉ xảy ra khi a = b = 0, nên mọi số khác 0 không có phần tử ngược.
    3. Nhân thường: 1 là trung hoà; 0 . b = 0 khác 1 với mọi b.
- `dstt_t10_pt_07` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên R xét a * b = a + b + ab. Sắp xếp các bước tìm phần tử ngược của số 2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_03`
  - **Đáp án (thứ tự đúng):**
    1. Tìm phần tử trung hoà: a * e = a + e + ae = a cho e(1 + a) = 0 với mọi a, nên e = 0.
    2. Gọi b là phần tử ngược của 2, tức 2 * b = e = 0.
    3. Viết 2 * b = 2 + b + 2b = 2 + 3b.
    4. Giải 2 + 3b = 0 được b = -2/3.
    5. Kiểm tra: 2 * (-2/3) = 2 - 2/3 - 4/3 = 0, và phép toán giao hoán nên (-2/3) * 2 cũng bằng 0.
  - **Lời giải:**
    1. Phần tử ngược chỉ có nghĩa sau khi biết phần tử trung hoà, vì nó đưa về phần tử trung hoà.
    2. Bước kiểm tra cuối dựa vào giao hoán để chỉ cần thử một phía.
- `dstt_t10_pt_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b - 2ab (giao hoán, kết hợp).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t6_nd_03`
  - **Phần a** (Điền số): a) Tính 3 * 4.
    - **Đáp án a:** -17
  - **Phần b** (Điền số): b) Tìm phần tử trung hoà e.
    - **Đáp án b:** 0
  - **Phần c** (Điền số): c) Tìm phần tử ngược của 3.
    - **Đáp án c:** 3/5
  - **Phần d** (Đúng/Sai): d) Mọi số thực đều có phần tử ngược.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) 3 * 4 = 3 + 4 - 2 . 3 . 4 = 7 - 24 = -17.
    2. b) a * e = a + e - 2ae = a cho e(1 - 2a) = 0 với mọi a, nên e = 0.
    3. c) 3 * b = 3 + b - 6b = 3 - 5b = 0 cho b = 3/5. Kiểm tra: 3 * 3/5 = 3 + 3/5 - 18/5 = 0.
    4. d) a * b = 0 cho a + b(1 - 2a) = 0; khi a = 1/2 thì 1/2 = 0 vô lý, nên số 1/2 không có phần tử ngược.
- `dstt_t10_pt_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trên Z xét phép toán a * b = a + b + 1.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t7_kgv_02`
  - **Phần a** (Đúng/Sai): a) Phép toán * có tính kết hợp.
    - **Đáp án a:** Đúng
  - **Phần b** (Điền số): b) Tìm phần tử trung hoà.
    - **Đáp án b:** -1
  - **Phần c** (Điền số): c) Tìm phần tử ngược của 5.
    - **Đáp án c:** -7
  - **Phần d** (Đúng/Sai): d) Z với phép toán * là một nhóm.
    - **Đáp án d:** Đúng
  - **Lời giải:**
    1. a) (a * b) * c = (a + b + 1) + c + 1 = a + b + c + 2 và a * (b * c) = a + (b + c + 1) + 1 = a + b + c + 2.
    2. b) a * e = a + e + 1 = a cho e = -1.
    3. c) 5 * b = 5 + b + 1 = -1 (phải bằng phần tử trung hoà -1) cho b = -7. Kiểm tra: 5 + (-7) + 1 = -1.
    4. d) Kết hợp, có trung hoà -1, và phần tử ngược của a là -a - 2 (a + (-a - 2) + 1 = -1) cũng là số nguyên. Vậy (Z, *) là nhóm (giao hoán), đồng cấu với (Z, +) qua a -> a + 1.
- `dstt_t10_pt_10` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Nếu một phép toán hai ngôi trên một tập có phần tử trung hoà thì phần tử trung hoà đó là duy nhất.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t7_kgv_01`
  - **Đáp án:** Đúng
    1. Giả sử e và e' đều là phần tử trung hoà. Vì e trung hoà nên e * e' = e'; vì e' trung hoà nên e * e' = e.
    2. Suy ra e = e'. Mệnh đề đúng (không cần giao hoán hay kết hợp).
- `dstt_g10_ket_hop_tf` · bậc 5 (Thử thách) · Đúng/Sai · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Phép toán hai ngôi a * b = a + 2b - 2 trên R có tính chất giao hoán.
  - **Đáp án:** Sai
    1. a * b = a + 2b - 2. Đổi chỗ: b * a = 2a + b - 2.
    2. Hiệu a * b - b * a = (1 - 2)(a - b) = -1(a - b).
    3. Hiệu khác 0 khi a khác b: ví dụ a = 1, b = 0 cho a * b = -1 và b * a = 0. Mệnh đề sai.
  - **Câu hỏi:** Phép toán hai ngôi a * b = -2 trên R có tính chất giao hoán.
  - **Đáp án:** Đúng
    1. a * b = -2. Đổi chỗ: b * a = -2.
    2. Hiệu a * b - b * a = (0 - 0)(a - b) = 0(a - b).
    3. Hiệu bằng 0 với mọi a, b vì hệ số của a và của b bằng nhau. Mệnh đề đúng.
  - **Câu hỏi:** Phép toán hai ngôi a * b = a + 2b + 1 trên R có tính chất kết hợp.
  - **Đáp án:** Sai
    1. a * b = a + 2b + 1.
    2. (a * b) * c = a + 2b + 2c + 2.
    3. a * (b * c) = a + 2b + 4c + 3.
    4. Hai vế khác nhau ở ít nhất một hệ số hoặc hằng số (a: p^2 so với p; c: q so với q^2; hằng số: pr + r so với qr + r), nên có a, b, c làm chúng khác nhau. Mệnh đề sai.
- `dstt_g10_trung_hoa` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b - 5, giao hoán và kết hợp, có phần tử trung hoà. Tìm phần tử ngược của -2, tức số y có -2 * y bằng phần tử trung hoà. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 12
    1. Phần tử trung hoà là e = 5 (a + e - 5 = a).
    2. x * y = e: -2 + y - 5 = 5 cho y = 12.
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b - 5. Tìm phần tử trung hoà e (a * e = e * a = a với mọi a). Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 5
    1. a * e = a + e - 5 = a cho e = 5; phép toán giao hoán nên e * a cũng bằng a.
  - **Câu hỏi:** Trên R xét phép toán a * b = a + b + 3, giao hoán và kết hợp, có phần tử trung hoà. Tìm phần tử ngược của -4, tức số y có -4 * y bằng phần tử trung hoà. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -2
    1. Phần tử trung hoà là e = -3 (a + e + 3 = a).
    2. x * y = e: -4 + y + 3 = -3 cho y = -2.

### Nhóm và nhóm con (`dstt_t10_nhom`)

- `dstt_t10_nh_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong nhóm cộng Z_12 (các số dư modulo 12, phép cộng modulo 12), phần tử 8 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để cộng 8 với chính nó k lần được 0? Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgv_02`, `dstt_t6_nd_01`
  - **Đáp án:** 3
    1. Các bội của 8 modulo 12: 8, 16 = 4, 24 = 0. Vậy k = 3.
    2. Công thức: cấp của a trong Z_n là n/gcd(a, n) = 12/gcd(8, 12) = 12/4 = 3.
- `dstt_t10_nh_02` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Các phần tử khả nghịch của Z_18 (các a trong 1..17 có a . b = 1 modulo 18 với một b nào đó) lập thành một nhóm với phép nhân modulo 18. Nhóm đó có bao nhiêu phần tử? Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t7_kgv_02`
  - **Đáp án:** 6
    1. a khả nghịch modulo 18 khi và chỉ khi gcd(a, 18) = 1.
    2. Các số đó: 1, 5, 7, 11, 13, 17, có 6 số (phi(18) = 18 . (1 - 1/2)(1 - 1/3) = 6). Số 2, 3, 4, ... có ước chung với 18 nên không khả nghịch.
- `dstt_t10_nh_03` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Tập {1, 2, 3, 4, 5} với phép nhân modulo 6 là một nhóm.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgv_01`, `dstt_t6_nd_05`
  - **Đáp án:** Sai
    1. Phép nhân modulo 6 không đóng trên tập này: 2 . 3 = 6, và 6 chia 6 dư 0, không thuộc tập.
    2. Cũng không cần xét tiếp: một nhóm đòi hỏi phép toán đóng. (Nhóm đúng là {1, 5}: các phần tử khả nghịch modulo 6.) Mệnh đề sai.
- `dstt_t10_nh_04` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** G là một nhóm có đúng 12 phần tử. Cấp của một nhóm con của G có thể là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t7_kgv_01`
    - **(đúng)** 6
    - 8
    - 5
    - 24
  - **Đáp án:** 6
    1. Theo định lý Lagrange, cấp của nhóm con chia hết cấp của nhóm: 6 chia hết 12 nên có thể xảy ra (ví dụ Z_12 có nhóm con cấp 6).
    2. 8 nhỏ hơn 12 nhưng không chia hết 12 (12 : 8 không nguyên), nên không thể là cấp của một nhóm con.
    3. 5 cũng không chia hết 12.
    4. 24 lớn hơn số phần tử của G: một nhóm con là tập con nên không có nhiều phần tử hơn G.
- `dstt_t10_nh_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Chứng minh H = {2k : k nguyên} (các số nguyên chẵn) là nhóm con của (Z, +). Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t6_nd_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. H khác rỗng vì 0 = 2 . 0 thuộc H.
    2. Đóng với phép toán: 2a + 2b = 2(a + b) cũng thuộc H.
    3. Phần tử ngược: phần tử ngược của 2a là 1/(2a), cũng thuộc H.   **<- bước sai đầu tiên**
    4. Vậy H là nhóm con.
  - **Đáp án:** Bước 3: Phần tử ngược: phần tử ngược của 2a là 1/(2a), cũng thuộc H.
  - **Vì sao sai, và bước đúng:**
    1. Phép toán của nhóm là phép cộng, nên phần tử ngược của 2a là -2a (cộng với 2a được 0), không phải 1/(2a) - đó là nghịch đảo của phép nhân, và 1/(2a) thậm chí không phải số nguyên.
    2. Đúng: -2a = 2(-a) thuộc H. Với ba điều kiện (khác rỗng, đóng, có ngược) H là nhóm con.
- `dstt_t10_nh_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi cấu trúc với kết luận đúng về nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_05`, `dstt_t4_gh_05`
  - **Đáp án (ghép đúng):**
    - (Z, +): số nguyên với phép cộng — Nhóm giao hoán vô hạn
    - (Z, x): số nguyên với phép nhân thường — Không phải nhóm: số 2 không có phần tử ngược trong Z
    - Các số hữu tỉ khác 0 với phép nhân — Nhóm giao hoán
    - Ma trận vuông cấp 2 khả nghịch với phép nhân ma trận — Nhóm không giao hoán
  - **Lời giải:**
    1. (Z, x) có trung hoà 1 nhưng chỉ 1 và -1 có phần tử ngược trong Z.
    2. Số hữu tỉ khác 0: a/b có nghịch đảo b/a cũng hữu tỉ khác 0.
    3. Ma trận khả nghịch cấp 2: tích và nghịch đảo của ma trận khả nghịch vẫn khả nghịch, nhưng AB khác BA nói chung.
- `dstt_t10_nh_07` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong nhóm các phần tử khác 0 của Z_7 với phép nhân modulo 7 (cấp 6), sắp xếp các bước tìm cấp của phần tử 3.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t7_kgv_01`
  - **Đáp án (thứ tự đúng):**
    1. Tính các lũy thừa liên tiếp của 3 modulo 7: 3^1 = 3.
    2. 3^2 = 9, và 9 - 7 = 2, nên 3^2 = 2.
    3. 3^3 = 2 . 3 = 6.
    4. 3^6 = (3^3)^2 = 6^2 = 36, và 36 - 35 = 1, nên 3^6 = 1.
    5. Cấp của 3 chia hết cho 6, nên thuộc {1, 2, 3, 6}; vì 3^1, 3^2, 3^3 đều khác 1 nên cấp là 6.
  - **Lời giải:**
    1. Cấp của một phần tử chia hết cấp của nhóm (6), nên chỉ cần thử các ước 1, 2, 3 trước khi dừng ở 6.
    2. Vì cấp 3 bằng cấp của cả nhóm, 3 sinh ra cả nhóm (nhóm này là nhóm xyclic).
- `dstt_t10_nh_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét nhóm cộng Z_12 (số dư modulo 12 với phép cộng modulo 12).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t6_nd_01`
  - **Phần a** (Điền số): a) Cấp của phần tử 8.
    - **Đáp án a:** 3
  - **Phần b** (Điền số): b) Nhóm con sinh bởi 8 có bao nhiêu phần tử?
    - **Đáp án b:** 3
  - **Phần c** (Điền số): c) Có bao nhiêu phần tử sinh ra cả nhóm Z_12?
    - **Đáp án c:** 4
  - **Phần d** (Đúng/Sai): d) Z_12 có một nhóm con có đúng 5 phần tử.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) 12/gcd(8, 12) = 3.
    2. b) Nhóm con sinh bởi 8 là {0, 8, 4}: số phần tử bằng cấp của 8, tức 3.
    3. c) a sinh Z_12 khi và chỉ khi gcd(a, 12) = 1: các số 1, 5, 7, 11, tức phi(12) = 4.
    4. d) Mọi nhóm con của Z_12 là nhóm xyclic có cấp chia hết 12 (1, 2, 3, 4, 6, 12); 5 không chia hết 12 nên không có nhóm con cấp 5 (định lý Lagrange).
- `dstt_t10_nh_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét nhóm G gồm các phần tử khả nghịch của Z_9 với phép nhân modulo 9.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t6_nd_01`
  - **Phần a** (Điền số): a) G có bao nhiêu phần tử?
    - **Đáp án a:** 6
  - **Phần b** (Điền số): b) Cấp của phần tử 2 là bao nhiêu?
    - **Đáp án b:** 6
  - **Phần c** (Đúng/Sai): c) G là nhóm xyclic (có một phần tử sinh ra cả nhóm).
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Có bao nhiêu phần tử sinh ra G?
    - **Đáp án d:** 2
  - **Lời giải:**
    1. a) Các số trong 1..8 nguyên tố cùng nhau với 9: 1, 2, 4, 5, 7, 8; phi(9) = 6.
    2. b) Lũy thừa của 2 modulo 9: 2, 4, 8, 7, 5, 1: cấp 6.
    3. c) 2 có cấp 6 bằng số phần tử của G nên 2 sinh ra G: G là xyclic.
    4. d) Phần tử sinh là a = 2^k với gcd(k, 6) = 1, tức k = 1 và 5: 2 và 2^5 = 5. Có phi(6) = 2 phần tử sinh.
- `dstt_t10_nh_10` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hợp của hai nhóm con bất kỳ của một nhóm luôn là một nhóm con.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t7_kgc_02`, `dstt_t7_kgc_01`
  - **Đáp án:** Sai
    1. Phản ví dụ trong (Z, +): H = các bội của 2 và K = các bội của 3 đều là nhóm con. Nhưng 2 và 3 thuộc H hợp K, còn 2 + 3 = 5 thì không: hợp không đóng với phép toán.
    2. Giao của hai nhóm con thì luôn là nhóm con. Mệnh đề sai.
- `dstt_g10_cap_cong` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong nhóm cộng Z_16 (số dư modulo 16, phép cộng modulo 16), phần tử 10 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 10 cộng với chính nó k lần được 0? Nhập một số.
  - **Đáp án:** 8
    1. Cấp của a trong Z_n là n/gcd(a, n): gcd(10, 16) = 2.
    2. Cấp = 16/2 = 8. (Kiểm tra: 8 . 10 = 80 = 5 . 16, chia hết 16.)
  - **Câu hỏi:** Trong nhóm cộng Z_11 (số dư modulo 11, phép cộng modulo 11), phần tử 2 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 2 cộng với chính nó k lần được 0? Nhập một số.
  - **Đáp án:** 11
    1. Cấp của a trong Z_n là n/gcd(a, n): gcd(2, 11) = 1.
    2. Cấp = 11/1 = 11. (Kiểm tra: 11 . 2 = 22 = 2 . 11, chia hết 11.)
  - **Câu hỏi:** Trong nhóm cộng Z_23 (số dư modulo 23, phép cộng modulo 23), phần tử 19 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 19 cộng với chính nó k lần được 0? Nhập một số.
  - **Đáp án:** 23
    1. Cấp của a trong Z_n là n/gcd(a, n): gcd(19, 23) = 1.
    2. Cấp = 23/1 = 23. (Kiểm tra: 23 . 19 = 437 = 19 . 23, chia hết 23.)
- `dstt_g10_cap_nhan` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong nhóm các phần tử khác 0 của Z_7 với phép nhân modulo 7, phần tử 6 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 6^k = 1? Nhập một số.
  - **Đáp án:** 2
    1. Các lũy thừa liên tiếp của 6 modulo 7: 6, 1.
    2. Lũy thừa đầu tiên bằng 1 là số mũ 2, nên cấp là 2 (và chia hết cấp 6 của nhóm).
  - **Câu hỏi:** Trong nhóm các phần tử khác 0 của Z_5 với phép nhân modulo 5, phần tử 2 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 2^k = 1? Nhập một số.
  - **Đáp án:** 4
    1. Các lũy thừa liên tiếp của 2 modulo 5: 2, 4, 3, 1.
    2. Lũy thừa đầu tiên bằng 1 là số mũ 4, nên cấp là 4 (và chia hết cấp 4 của nhóm).
  - **Câu hỏi:** Trong nhóm các phần tử khác 0 của Z_7 với phép nhân modulo 7, phần tử 6 có cấp bao nhiêu, tức số nguyên dương k nhỏ nhất để 6^k = 1? Nhập một số.
  - **Đáp án:** 2
    1. Các lũy thừa liên tiếp của 6 modulo 7: 6, 1.
    2. Lũy thừa đầu tiên bằng 1 là số mũ 2, nên cấp là 2 (và chia hết cấp 6 của nhóm).

### Vành và trường (`dstt_t10_vanh_truong`)

- `dstt_t10_vt_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong vành Z_12, một ước của 0 là một phần tử a khác 0 có a . b = 0 (modulo 12) với một b khác 0 nào đó. Z_12 có bao nhiêu ước của 0? Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Đáp án:** 7
    1. a là ước của 0 khi gcd(a, 12) > 1 (và a khác 0); a khả nghịch khi gcd(a, 12) = 1, và phần tử khả nghịch thì không thể là ước của 0.
    2. Có 11 phần tử khác 0, trong đó phi(12) = 4 phần tử khả nghịch (1, 5, 7, 11); còn lại 11 - 4 = 7 ước của 0: 2, 3, 4, 6, 8, 9, 10 (ví dụ 3 . 4 = 12 = 0).
- `dstt_t10_vt_02` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Với n >= 2, vành Z_n (số dư modulo n với cộng và nhân modulo n) là một trường khi và chỉ khi n là số nguyên tố.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Đáp án:** Đúng
    1. Nếu n nguyên tố thì mọi a khác 0 có gcd(a, n) = 1 nên khả nghịch (đẳng thức Bezout): Z_n là trường.
    2. Nếu n = rs hợp số (1 < r, s < n) thì r . s = 0 với r, s khác 0 nên r là ước của 0, không khả nghịch: không phải trường. Mệnh đề đúng.
- `dstt_t10_vt_03` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Trong các cấu trúc sau với phép cộng và nhân thông thường (hay modulo), cấu trúc nào là một trường?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
    - **(đúng)** Z_7 (số dư modulo 7)
    - Z (số nguyên)
    - Z_6 (số dư modulo 6)
    - Ma trận vuông cấp 2 với các số thực
  - **Đáp án:** Z_7 (số dư modulo 7)
    1. Z_7 là trường vì 7 nguyên tố: mọi phần tử khác 0 có phần tử nghịch đảo modulo 7.
    2. Z không phải trường: 2 không có nghịch đảo nhân trong Z (1/2 không phải số nguyên).
    3. Z_6 không phải trường: 2 . 3 = 6 = 0 với 2, 3 khác 0 nên 2 và 3 là ước của 0, không khả nghịch.
    4. Ma trận vuông cấp 2: nhân không giao hoán, và có ma trận khác 0 không khả nghịch (det bằng 0) nên cũng có ước của 0.
- `dstt_t10_vt_04` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Hỏi Z_8 (số dư modulo 8, phép cộng và nhân modulo 8) có phải là một trường không. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_03`
  - **Lời giải đưa ra (có một bước sai):**
    1. Z_8 với cộng và nhân modulo 8 là vành giao hoán có đơn vị 1.
    2. Ta thử: 3 . 3 = 9 = 1, 5 . 5 = 25 = 1, 7 . 7 = 49 = 1 (modulo 8), nên 3, 5, 7 khả nghịch.
    3. Vậy mọi phần tử khác 0 đều khả nghịch, nên Z_8 là trường.   **<- bước sai đầu tiên**
  - **Đáp án:** Bước 3: Vậy mọi phần tử khác 0 đều khả nghịch, nên Z_8 là trường.
  - **Vì sao sai, và bước đúng:**
    1. Mới thử một số phần tử (3, 5, 7), chưa thử 2, 4, 6. Thực ra 2 . 4 = 8 = 0 với 2 và 4 khác 0, nên 2 và 4 là ước của 0 và không khả nghịch (nếu 2b = 1 thì nhân 4 hai vế: 0 = 4 mâu thuẫn).
    2. Đúng: Z_8 là vành giao hoán nhưng không phải trường (8 không nguyên tố). Muốn là trường phải kiểm tra mọi phần tử khác 0, hoặc dùng tiêu chuẩn n nguyên tố.
- `dstt_t10_vt_05` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi cấu trúc với đặc điểm của nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_gh_05`, `dstt_t6_nd_05`
  - **Đáp án (ghép đúng):**
    - Z (số nguyên) — Vành giao hoán không có ước của 0, nhưng không phải trường
    - Q (số hữu tỉ) — Trường: mọi phần tử khác 0 có nghịch đảo
    - Z_6 (số dư modulo 6) — Vành giao hoán có ước của 0 (2 . 3 = 0)
    - Ma trận vuông cấp 2 với số thực — Vành không giao hoán
  - **Lời giải:**
    1. Z: tích của hai số nguyên khác 0 khác 0, nhưng chỉ 1 và -1 có nghịch đảo.
    2. Z_6: 2 . 3 = 0 modulo 6 nên có ước của 0 và không là trường.
    3. Ma trận cấp 2: AB khác BA nói chung, và có ước của 0.
- `dstt_t10_vt_06` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Chứng minh Z_p với p nguyên tố là trường: sắp xếp các bước chứng minh mọi phần tử a khác 0 của Z_p có nghịch đảo.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Đáp án (thứ tự đúng):**
    1. Lấy a trong 1..p-1; vì p nguyên tố và p không chia hết a nên gcd(a, p) = 1.
    2. Theo đẳng thức Bezout có các số nguyên u, v với u a + v p = 1.
    3. Lấy phần dư modulo p hai vế: u a = 1 (modulo p), vì v p chia hết cho p.
    4. Vậy u (lấy modulo p) là nghịch đảo của a, nên mọi phần tử khác 0 khả nghịch.
  - **Lời giải:**
    1. Mỗi bước dùng kết quả của bước trước: gcd = 1, rồi Bezout, rồi đổi sang modulo p, rồi kết luận.
    2. Tính chất kết hợp, giao hoán, phân phối của Z_p thừa hưởng từ Z; điều cần chứng minh riêng là sự tồn tại nghịch đảo.
- `dstt_t10_vt_07` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét vành Z_10 (số dư modulo 10, cộng và nhân modulo 10).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Phần a** (Điền số): a) Có bao nhiêu phần tử khả nghịch?
    - **Đáp án a:** 4
  - **Phần b** (Điền số): b) Có bao nhiêu ước của 0 (phần tử a khác 0 có a . b = 0 với một b khác 0)?
    - **Đáp án b:** 5
  - **Phần c** (Đúng/Sai): c) Z_10 là một trường.
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Tìm nghịch đảo của 3 trong Z_10.
    - **Đáp án d:** 7
  - **Lời giải:**
    1. a) Các a trong 1..9 có gcd(a, 10) = 1: 1, 3, 7, 9, tức phi(10) = 4.
    2. b) Mọi phần tử khác 0 hoặc khả nghịch hoặc là ước của 0: 9 - 4 = 5 ước của 0 (2, 4, 5, 6, 8; ví dụ 2 . 5 = 10 = 0).
    3. c) Có ước của 0 nên không phải trường (10 = 2 . 5 không nguyên tố).
    4. d) 3 . 7 = 21 = 1 modulo 10 nên nghịch đảo của 3 là 7.
- `dstt_t10_vt_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Xét trường Z_7 (số dư modulo 7).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Phần a** (Điền số): a) Tìm nghịch đảo của 3.
    - **Đáp án a:** 5
  - **Phần b** (Điền số): b) Giải 3x = 4 trong Z_7 (nhập x trong 0..6).
    - **Đáp án b:** 6
  - **Phần c** (Điền số): c) Phương trình x^2 = 1 có bao nhiêu nghiệm trong Z_7?
    - **Đáp án c:** 2
  - **Phần d** (Đúng/Sai): d) Trong vành Z_8, phương trình x^2 = 1 cũng chỉ có hai nghiệm.
    - **Đáp án d:** Sai
  - **Lời giải:**
    1. a) 3 . 5 = 15 = 1 modulo 7 nên nghịch đảo của 3 là 5.
    2. b) Nhân hai vế với 5: x = 5 . 4 = 20 = 6. Kiểm tra: 3 . 6 = 18 = 4 modulo 7.
    3. c) x^2 - 1 = (x - 1)(x + 1) = 0, trong trường tích bằng 0 khi một thừa số bằng 0, nên x = 1 hoặc x = 6: 2 nghiệm.
    4. d) Trong Z_8 có bốn nghiệm 1, 3, 5, 7 (3^2 = 9 = 1). Vành có ước của 0 thì một đa thức bậc hai có thể có nhiều hơn hai nghiệm.
- `dstt_t10_vt_09` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi vành giao hoán có đơn vị mà không có ước của 0 đều là một trường.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t6_nd_01`, `dstt_t6_nd_05`
  - **Đáp án:** Sai
    1. Phản ví dụ: Z là vành giao hoán có đơn vị, không có ước của 0 (tích hai số nguyên khác 0 khác 0), nhưng 2 không có nghịch đảo trong Z nên Z không phải trường.
    2. Chiều ngược lại đúng: trường thì không có ước của 0. (Với vành hữu hạn thì điều khẳng định trên đúng; với vành vô hạn như Z thì sai.) Mệnh đề sai.
- `dstt_g10_dem_don_vi` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong nhóm cộng Z_14, có bao nhiêu phần tử sinh ra cả nhóm? Nhập một số.
  - **Đáp án:** 6
    1. a sinh Z_14 khi và chỉ khi gcd(a, 14) = 1 (cấp của a là 14/gcd(a, 14) phải bằng 14).
    2. Có 6 số a trong 1..13 thoả điều đó (phi(14) = 6).
  - **Câu hỏi:** Các phần tử khả nghịch của Z_9 (a trong 1..8 có a . b = 1 modulo 9 với một b nào đó) lập thành một nhóm với phép nhân modulo 9. Nhóm đó có bao nhiêu phần tử? Nhập một số.
  - **Đáp án:** 6
    1. a khả nghịch modulo 9 khi và chỉ khi gcd(a, 9) = 1.
    2. Có 6 số như vậy trong 1..8: 1, 2, 4, 5, 7, 8.
  - **Câu hỏi:** Trong nhóm cộng Z_21, có bao nhiêu phần tử sinh ra cả nhóm? Nhập một số.
  - **Đáp án:** 12
    1. a sinh Z_21 khi và chỉ khi gcd(a, 21) = 1 (cấp của a là 21/gcd(a, 21) phải bằng 21).
    2. Có 12 số a trong 1..20 thoả điều đó (phi(21) = 12).
- `dstt_g10_nghich_dao_mod` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Trong vành Z_15 (số dư modulo 15), tìm nghịch đảo của 11, tức số b trong 1..14 có 11 . b = 1 modulo 15. Nhập một số.
  - **Đáp án:** 11
    1. gcd(11, 15) = 1 nên 11 khả nghịch modulo 15; tìm b với 11 b - 15 t = 1 (đẳng thức Bezout).
    2. b = 11: 11 . 11 = 121 = 8 . 15 + 1, tức bằng 1 modulo 15.
  - **Câu hỏi:** Trong vành Z_10 (số dư modulo 10), tìm nghịch đảo của 3, tức số b trong 1..9 có 3 . b = 1 modulo 10. Nhập một số.
  - **Đáp án:** 7
    1. gcd(3, 10) = 1 nên 3 khả nghịch modulo 10; tìm b với 3 b - 10 t = 1 (đẳng thức Bezout).
    2. b = 7: 3 . 7 = 21 = 2 . 10 + 1, tức bằng 1 modulo 10.
  - **Câu hỏi:** Trong vành Z_22 (số dư modulo 22), tìm nghịch đảo của 21, tức số b trong 1..21 có 21 . b = 1 modulo 22. Nhập một số.
  - **Đáp án:** 21
    1. gcd(21, 22) = 1 nên 21 khả nghịch modulo 22; tìm b với 21 b - 22 t = 1 (đẳng thức Bezout).
    2. b = 21: 21 . 21 = 441 = 20 . 22 + 1, tức bằng 1 modulo 22.

### Dạng tuyến tính và song tuyến tính (`dstt_t10_dang_song_tuyen_tinh`)

- `dstt_t10_ds_01` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng song tuyến tính f trên R^2 có ma trận A như hình, nghĩa là f(x, y) = x^T A y. Tính f(u, v) với u = (1, 2) và v = (3, -1). Nhập một số.
  - A = (2, -1); (3, 4)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_nm_03`, `dstt_t8_mtax_01`
  - **Đáp án:** 17
    1. A v = (2 . 3 + (-1)(-1), 3 . 3 + 4 . (-1)) = (7, 5).
    2. f(u, v) = u^T (A v) = 1 . 7 + 2 . 5 = 17. Thứ tự quan trọng: f(v, u) = v^T A u = 3 . 0 + (-1) . 11 = -11 khác f(u, v), vì A không đối xứng.
- `dstt_t10_ds_02` · bậc 5 (Thử thách) · Trắc nghiệm · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng song tuyến tính trên R^2: f(x, y) = x1 y1 + 2 x1 y2 + 3 x2 y1 + 4 x2 y2. Ma trận A của f (f(x, y) = x^T A y), viết hàng 1 rồi hàng 2, là
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_tc_05`, `dstt_t8_mtax_01`
    - **(đúng)** (1, 2) và (3, 4)
    - (1, 3) và (2, 4)
    - (1, 5/2) và (5/2, 4)
    - (1, 2) và (2, 4)
  - **Đáp án:** (1, 2) và (3, 4)
    1. Phần tử a_ij của A là hệ số của x_i y_j: a_11 = 1, a_12 = 2 (x1 y2), a_21 = 3 (x2 y1), a_22 = 4. Vậy hàng 1 là (1, 2) và hàng 2 là (3, 4).
    2. (1, 3) và (2, 4) là chuyển vị: nhầm chỉ số hàng với chỉ số cột (hệ số của x1 y2 phải ở hàng 1, cột 2).
    3. (1, 5/2) và (5/2, 4) là ma trận đối xứng của dạng toàn phương q(x) = f(x, x) = x1^2 + 5 x1 x2 + 4 x2^2: lấy trung bình hai hệ số chéo 2 và 3; nhưng đó là ma trận của dạng đối xứng hoá, không phải của f.
    4. (1, 2) và (2, 4) lặp hệ số 2 ở cả hai ô chéo, bỏ quên hệ số 3 của x2 y1.
- `dstt_t10_ds_03` · bậc 5 (Thử thách) · Điền số · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng song tuyến tính trên R^2: f(x, y) = 2 x1 y1 + 3 x1 y2 - x2 y1 + 4 x2 y2. Đặt q(x) = f(x, x), dạng toàn phương của nó, thu gọn thành q = a x1^2 + b x1 x2 + c x2^2. Tìm b. Nhập một số.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_nm_03`, `dstt_t8_mtax_01`
  - **Đáp án:** 2
    1. q(x) = f(x, x) = 2 x1^2 + 3 x1 x2 - x2 x1 + 4 x2^2.
    2. Gộp hai số hạng chéo: 3 x1 x2 - x1 x2 = 2 x1 x2, nên q = 2 x1^2 + 2 x1 x2 + 4 x2^2 và b = 2 (= 3 + (-1), tổng hai hệ số x1 y2 và x2 y1).
- `dstt_t10_ds_04` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Mọi dạng song tuyến tính f trên R^n đều đối xứng, tức f(x, y) = f(y, x) với mọi x, y.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_hop_02`
  - **Đáp án:** Sai
    1. Phản ví dụ: f(x, y) = x1 y2 trên R^2 có f(e1, e2) = 1 nhưng f(e2, e1) = 0.
    2. f đối xứng khi và chỉ khi ma trận của nó đối xứng (A^T = A). Dạng song tuyến tính nói chung chỉ tuyến tính theo từng biến, không đòi hỏi đối xứng. Mệnh đề sai.
- `dstt_t10_ds_05` · bậc 5 (Thử thách) · Tìm chỗ sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Đề: Tìm ma trận đối xứng B của dạng toàn phương q(x) = x1^2 + 6 x1 x2 + 5 x2^2, tức q(x) = x^T B x. Lời giải dưới đây có chỗ sai. Bước đầu tiên bị sai là bước nào?
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_mtax_01`
  - **Lời giải đưa ra (có một bước sai):**
    1. B là ma trận đối xứng cấp 2: B = [b11, b12; b12, b22].
    2. Các hệ số của x1^2 và x2^2 là phần tử đường chéo: b11 = 1, b22 = 5.
    3. Hệ số của x1 x2 là 6 nên b12 = b21 = 6.   **<- bước sai đầu tiên**
    4. Vậy B = [1, 6; 6, 5].
  - **Đáp án:** Bước 3: Hệ số của x1 x2 là 6 nên b12 = b21 = 6.
  - **Vì sao sai, và bước đúng:**
    1. Khai triển x^T B x = b11 x1^2 + 2 b12 x1 x2 + b22 x2^2: số hạng x1 x2 nhận từ cả hai ô b12 và b21, nên hệ số 6 = 2 b12, và b12 = 3.
    2. Đúng: B = [1, 3; 3, 5]. Kiểm tra bằng q(1, 1) = 1 + 6 + 5 = 12 = tổng các phần tử của B (1 + 3 + 3 + 5).
- `dstt_t10_ds_06` · bậc 5 (Thử thách) · Ghép cặp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Ghép mỗi dạng trên R^2 với nhận xét đúng về nó.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_hop_02`
  - **Đáp án (ghép đúng):**
    - f(x, y) = x1 y2 - x2 y1 — Phản đối xứng: f(y, x) = -f(x, y), và f(x, x) = 0
    - f(x, y) = x1 y1 + x2 y2 — Đối xứng, ma trận đơn vị (tích vô hướng thông thường)
    - q(x) = x1^2 - x2^2 — Dạng toàn phương có ma trận đường chéo (1, -1), nhận cả giá trị dương lẫn âm
    - f(x, y) = x1 y2 — Không đối xứng; dạng toàn phương q(x) = x1 x2 có ma trận đối xứng với hai ô chéo bằng 1/2
  - **Lời giải:**
    1. x1 y2 - x2 y1 là định thức của hai vectơ: đổi chỗ x, y đổi dấu.
    2. x^T I y = x1 y1 + x2 y2.
    3. q(1, 0) = 1 dương, q(0, 1) = -1 âm: dạng không xác định dấu.
    4. f(x, x) = x1 x2; chia đôi hệ số 1 của x1 x2 vào hai ô chéo.
- `dstt_t10_ds_07` · bậc 5 (Thử thách) · Sắp xếp bước giải · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Sắp xếp các bước viết ma trận đối xứng B của dạng toàn phương q(x) = 3 x1^2 - 8 x1 x2 + 5 x2^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_mtax_01`
  - **Đáp án (thứ tự đúng):**
    1. Đường chéo của B lấy từ hệ số của x1^2 và x2^2: b11 = 3 và b22 = 5.
    2. Hệ số -8 của x1 x2 được chia đều cho hai ô đối xứng: b12 = b21 = -8/2 = -4.
    3. Ma trận đối xứng B có hàng 1 là (3, -4) và hàng 2 là (-4, 5).
    4. Kiểm tra: q(2, 1) = 12 - 16 + 5 = 1, và x^T B x = 3 . 4 + 2 . (-4) . 2 . 1 + 5 . 1 = 1.
  - **Lời giải:**
    1. Đường chéo trước, rồi ô ngoài đường chéo bằng một nửa hệ số chéo, rồi ghép ma trận, rồi kiểm tra bằng một điểm.
    2. x^T B x = b11 x1^2 + 2 b12 x1 x2 + b22 x2^2, nên b12 = (hệ số của x1 x2)/2.
- `dstt_t10_ds_08` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng song tuyến tính f trên R^2 có ma trận A như hình, f(x, y) = x^T A y.
  - A = (1, 2); (0, 3)  (từng hàng)
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t4_nm_03`, `dstt_t8_mtax_01`
  - **Phần a** (Điền số): a) Tính f((1, 1), (1, -1)).
    - **Đáp án a:** -4
  - **Phần b** (Điền số): b) Tính f((1, -1), (1, 1)).
    - **Đáp án b:** 0
  - **Phần c** (Đúng/Sai): c) f là dạng đối xứng.
    - **Đáp án c:** Sai
  - **Phần d** (Điền số): d) Tính q(1, 1) = f((1, 1), (1, 1)).
    - **Đáp án d:** 6
  - **Lời giải:**
    1. a) A (1, -1) = (1 - 2, -3) = (-1, -3); f = 1 . (-1) + 1 . (-3) = -4.
    2. b) A (1, 1) = (3, 3); f = 1 . 3 + (-1) . 3 = 0.
    3. c) a) và b) cho hai kết quả khác nhau khi đổi chỗ hai vectơ (-4 và 0), nên f không đối xứng; cũng vì a_12 = 2 khác a_21 = 0.
    4. d) A (1, 1) = (3, 3) và q(1, 1) = 3 + 3 = 6 (cũng bằng tổng các phần tử của A).
- `dstt_t10_ds_09` · bậc 5 (Thử thách) · Thiên kiếp · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Dạng toàn phương trên R^2: q(x) = 2 x1^2 - 6 x1 x2 + 5 x2^2.
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_mtax_01`
  - **Phần a** (Điền số): a) Ma trận đối xứng B của q có b12 bằng bao nhiêu?
    - **Đáp án a:** -3
  - **Phần b** (Điền số): b) Tính định thức của B.
    - **Đáp án b:** 1
  - **Phần c** (Đúng/Sai): c) q xác định dương (q(x) > 0 với mọi x khác 0).
    - **Đáp án c:** Đúng
  - **Phần d** (Điền số): d) Tính q(3, 2).
    - **Đáp án d:** 2
  - **Lời giải:**
    1. a) Hệ số -6 của x1 x2 chia đôi: b12 = b21 = -3, nên B = [2, -3; -3, 5].
    2. b) det B = 2 . 5 - (-3)(-3) = 10 - 9 = 1.
    3. c) Tiêu chuẩn Sylvester cho ma trận đối xứng cấp 2: b11 = 2 > 0 và det B = 1 > 0 nên B, và q, xác định dương.
    4. d) q(3, 2) = 2 . 9 - 6 . 6 + 5 . 4 = 18 - 36 + 20 = 2.
- `dstt_t10_ds_10` · bậc 5 (Thử thách) · Đúng/Sai · viết tay · CHƯA DUYỆT
  - **Câu hỏi:** Hai dạng song tuyến tính khác nhau có thể có cùng một dạng toàn phương q(x) = f(x, x).
  - **Thang câu (luật 8, hỏi theo thứ tự sau khi sai):** `dstt_t3_db_05`, `dstt_t8_hop_02`
  - **Đáp án:** Đúng
    1. Lấy f(x, y) = x1 y2 và g(x, y) = x2 y1 trên R^2: f khác g (f(e1, e2) = 1 còn g(e1, e2) = 0) nhưng f(x, x) = x1 x2 = g(x, x).
    2. Dạng toàn phương chỉ "thấy" phần đối xứng (f(x, y) + f(y, x))/2 của f. Mệnh đề đúng.
- `dstt_g10_he_so_cheo` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dạng toàn phương trên R^2: q(x) = -2 x1^2 - 6 x1 x2, tức q(x) = x^T B x với B là ma trận đối xứng. Tìm phần tử b12 của B. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** -3
    1. x^T B x = b11 x1^2 + 2 b12 x1 x2 + b22 x2^2, nên hệ số của x1 x2 bằng 2 b12.
    2. b12 = -6/2 = -3.
  - **Câu hỏi:** Dạng toàn phương trên R^2: q(x) = -4 x1^2 - 6 x1 x2 - 3 x2^2, tức q(x) = x^T B x với B là ma trận đối xứng. Tính định thức của B. Nhập một số hoặc phân số tối giản.
  - **Đáp án:** 3
    1. B có đường chéo -4, -3 và b12 = b21 = -6/2 = -3.
    2. det B = -4 . -3 - (-3)^2 = 3.
  - **Câu hỏi:** Dạng toàn phương trên R^2: q(x) = -x1^2 - 4 x1 x2 + x2^2, tức q(x) = x^T B x với B là ma trận đối xứng. Tính q(0, 2). Nhập một số.
  - **Đáp án:** 4
    1. Thay x1 = 0, x2 = 2 vào q: -1 . (0)^2 + (-4) . (0) . (2) + 1 . (2)^2 = 4.
- `dstt_g10_ma_tran_song_tuyen` · bậc 5 (Thử thách) · Điền số · bộ sinh câu, 3 mẫu · CHƯA DUYỆT
  - **Câu hỏi:** Dạng song tuyến tính f trên R^2 có ma trận A như hình, nghĩa là f(x, y) = x^T A y. Tính f(u, v) với u = (4, 4) và v = (4, 3). Nhập một số.
  - A = (5, -3); (0, -3)  (từng hàng)
  - **Đáp án:** 8
    1. A v = (11, -9) (mỗi thành phần là hàng của A nhân với v).
    2. f(u, v) = u^T (A v) = (4) . (11) + (4) . (-9) = 8.
  - **Câu hỏi:** Dạng song tuyến tính f trên R^2 có ma trận A như hình, nghĩa là f(x, y) = x^T A y. Tính f(u, v) với u = (1, 1) và v = (0, -3). Nhập một số.
  - A = (-3, -3); (1, -2)  (từng hàng)
  - **Đáp án:** 15
    1. A v = (9, 6) (mỗi thành phần là hàng của A nhân với v).
    2. f(u, v) = u^T (A v) = (1) . (9) + (1) . (6) = 15.
  - **Câu hỏi:** Dạng song tuyến tính f trên R^2 có ma trận A như hình, nghĩa là f(x, y) = x^T A y. Tính f(u, v) với u = (4, -2) và v = (-3, 4). Nhập một số.
  - A = (5, 4); (-2, 1)  (từng hàng)
  - **Đáp án:** -16
    1. A v = (1, 10) (mỗi thành phần là hàng của A nhân với v).
    2. f(u, v) = u^T (A v) = (4) . (1) + (-2) . (10) = -16.
